# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Step 01_03_02 -- True 1v1 Match Identification: aoestats
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_03 -- Systematic Data Profiling
# **Dataset:** aoestats
# **Question:** Which matches are genuine 1v1 (exactly 2 active players),
# how does num_players relate to actual player counts, and how does the
# true 1v1 set compare to leaderboard='random_map'?
# **Invariants applied:**
# - #6 (reproducibility -- all SQL stored verbatim in markdown artifact)
# - #7 (no magic numbers -- all thresholds from census/profile JSON)
# - #9 (step scope: profiling only -- no cleaning or feature decisions)
# **Predecessor:** 01_03_01 (Systematic Data Profiling -- complete)
# **Step scope:** Identification and counting only. No filtering, cleaning,
# or subsetting decisions.

# %%
import json
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir, setup_notebook_logging

matplotlib.use("Agg")
logger = setup_notebook_logging(__name__)

# %%
db = get_notebook_db("aoe2", "aoestats")

# %%
reports_dir = get_reports_dir("aoe2", "aoestats")
profiling_dir = reports_dir / "artifacts" / "01_exploration" / "03_profiling"
profiling_dir.mkdir(parents=True, exist_ok=True)

census_path = reports_dir / "artifacts" / "01_exploration" / "02_eda" / "01_02_04_univariate_census.json"
with open(census_path) as f:
    census = json.load(f)

profile_path = profiling_dir / "01_03_01_systematic_profile.json"
with open(profile_path) as f:
    profile_01_03_01 = json.load(f)

# %%
# Validate census keys needed for this step
assert "num_players_distribution" in census, "Missing census key: num_players_distribution"
assert "categorical_matches" in census, "Missing census key: categorical_matches"
assert "leaderboard" in census["categorical_matches"], "Missing census key: categorical_matches.leaderboard"
assert "players_per_match" in census and len(census["players_per_match"]) > 0, (
    "Missing or empty census key 'players_per_match' -- "
    "re-run 01_02_04 census before proceeding"
)

# Validate profile keys
assert "dataset_level" in profile_01_03_01, "Missing profile key: dataset_level"
assert "matches_without_players" in profile_01_03_01["dataset_level"], (
    "Missing profile key: dataset_level.matches_without_players"
)

# I7: Extract constants from prior artifacts -- no magic numbers
MATCHES_TOTAL = profile_01_03_01["dataset_level"]["matches_raw_rows"]
PLAYERS_TOTAL = profile_01_03_01["dataset_level"]["players_raw_rows"]
MATCHES_WITHOUT_PLAYERS = profile_01_03_01["dataset_level"]["matches_without_players"]

# I7: num_players distribution from census
NUM_PLAYERS_DIST = {
    int(entry["num_players"]): int(entry["row_count"])
    for entry in census["num_players_distribution"]
}
# Census-derived: num_players=2 count
NUM_PLAYERS_2_CENSUS = NUM_PLAYERS_DIST.get(2, 0)

# I7: leaderboard distribution from census
LEADERBOARD_DIST = {
    entry["leaderboard"]: int(entry["cnt"])
    for entry in census["categorical_matches"]["leaderboard"]["top_values"]
}
RANKED_1V1_CENSUS = LEADERBOARD_DIST.get("random_map", 0)

print(f"MATCHES_TOTAL = {MATCHES_TOTAL:,}")
print(f"PLAYERS_TOTAL = {PLAYERS_TOTAL:,}")
print(f"MATCHES_WITHOUT_PLAYERS = {MATCHES_WITHOUT_PLAYERS:,}")
print(f"NUM_PLAYERS_2_CENSUS = {NUM_PLAYERS_2_CENSUS:,}")
print(f"RANKED_1V1_CENSUS = {RANKED_1V1_CENSUS:,}")
print(f"NUM_PLAYERS_DIST = {NUM_PLAYERS_DIST}")

# %%
sql_queries = {}
result = {
    "step": "01_03_02",
    "dataset": "aoestats",
    "constants_source": {
        "MATCHES_TOTAL": {"value": MATCHES_TOTAL, "source": "01_03_01_systematic_profile.json > dataset_level.matches_raw_rows"},
        "PLAYERS_TOTAL": {"value": PLAYERS_TOTAL, "source": "01_03_01_systematic_profile.json > dataset_level.players_raw_rows"},
        "MATCHES_WITHOUT_PLAYERS": {"value": MATCHES_WITHOUT_PLAYERS, "source": "01_03_01_systematic_profile.json > dataset_level.matches_without_players"},
        "NUM_PLAYERS_2_CENSUS": {"value": NUM_PLAYERS_2_CENSUS, "source": "01_02_04_univariate_census.json > num_players_distribution[num_players=2].row_count"},
        "RANKED_1V1_CENSUS": {"value": RANKED_1V1_CENSUS, "source": "01_02_04_univariate_census.json > categorical_matches.leaderboard.top_values[random_map].cnt"},
    },
}

# %% [markdown]
# ## Q1: Active Player Definition
#
# The players_raw schema has 14 columns. There is no slot, is_observer, status,
# or type column. The team column has cardinality 2 (values 0 and 1). Every row
# has a non-NULL winner (BOOLEAN), non-NULL civ (VARCHAR), and non-NULL team.
# profile_id has 1,185 NULLs (0.0011%).
#
# **Conclusion:** Every row in players_raw represents an active player. There
# is no schema-level mechanism to represent spectators or observers.

# %%
sql_active_player_diagnostic = """
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE winner IS NULL)     AS winner_null,
    COUNT(*) FILTER (WHERE civ IS NULL)        AS civ_null,
    COUNT(*) FILTER (WHERE team IS NULL)        AS team_null,
    COUNT(*) FILTER (WHERE profile_id IS NULL)  AS profile_id_null,
    COUNT(*) FILTER (WHERE game_id IS NULL)     AS game_id_null,
    -- Check if there are any rows where ALL of winner, civ, team are NULL
    -- (would suggest empty/observer slots)
    COUNT(*) FILTER (
        WHERE winner IS NULL AND civ IS NULL AND team IS NULL
    ) AS all_key_null,
    -- Check team value range
    MIN(team) AS team_min,
    MAX(team) AS team_max,
    COUNT(DISTINCT team) AS team_distinct
FROM players_raw
"""
sql_queries["active_player_diagnostic"] = sql_active_player_diagnostic
diag_df = db.fetch_df(sql_active_player_diagnostic)
print(diag_df.T.to_string())

result["q1_active_player_diagnostic"] = {
    "total_rows": int(diag_df["total_rows"].iloc[0]),
    "winner_null": int(diag_df["winner_null"].iloc[0]),
    "civ_null": int(diag_df["civ_null"].iloc[0]),
    "team_null": int(diag_df["team_null"].iloc[0]),
    "profile_id_null": int(diag_df["profile_id_null"].iloc[0]),
    "game_id_null": int(diag_df["game_id_null"].iloc[0]),
    "all_key_null": int(diag_df["all_key_null"].iloc[0]),
    "team_min": int(diag_df["team_min"].iloc[0]),
    "team_max": int(diag_df["team_max"].iloc[0]),
    "team_distinct": int(diag_df["team_distinct"].iloc[0]),
}
result["q1_conclusion"] = (
    "Every row in players_raw is an active player. "
    "No observer/spectator marker columns exist. "
    "winner is never NULL, civ is never NULL, team has values {0, 1} only."
)
print(f"\nQ1 conclusion: {result['q1_conclusion']}")

# %% [markdown]
# ## Q2: num_players vs Actual Player Count
#
# Cross-reference matches_raw.num_players against COUNT(players_raw rows) per
# game_id. The 01_03_01 linkage check found 212,890 matches with no player
# rows. These will show as actual_count=0 in the cross-tabulation.

# %%
sql_num_players_vs_actual = """
WITH player_counts AS (
    SELECT
        game_id,
        COUNT(*) AS actual_player_count
    FROM players_raw
    GROUP BY game_id
)
SELECT
    m.num_players,
    COALESCE(pc.actual_player_count, 0) AS actual_player_count,
    COUNT(*) AS match_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 4) AS pct
FROM matches_raw m
LEFT JOIN player_counts pc ON m.game_id = pc.game_id
GROUP BY m.num_players, COALESCE(pc.actual_player_count, 0)
ORDER BY m.num_players, actual_player_count
"""
sql_queries["num_players_vs_actual"] = sql_num_players_vs_actual
cross_df = db.fetch_df(sql_num_players_vs_actual)
print(cross_df.to_string(index=False))

# Store as list of dicts for JSON
result["q2_num_players_vs_actual_crosstab"] = cross_df.to_dict(orient="records")

# Compute alignment summary
total_matches = cross_df["match_count"].sum()
aligned = cross_df.loc[
    cross_df["num_players"] == cross_df["actual_player_count"],
    "match_count"
].sum()
mismatched = total_matches - aligned

result["q2_alignment_summary"] = {
    "total_matches": int(total_matches),
    "aligned_count": int(aligned),
    "aligned_pct": round(aligned / total_matches * 100, 4),
    "mismatched_count": int(mismatched),
    "mismatched_pct": round(mismatched / total_matches * 100, 4),
}
print(f"\nAlignment: {aligned:,} / {total_matches:,} ({result['q2_alignment_summary']['aligned_pct']}%)")
print(f"Mismatched: {mismatched:,} ({result['q2_alignment_summary']['mismatched_pct']}%)")

# %%
# Separate the mismatches into categories
orphaned = cross_df.loc[cross_df["actual_player_count"] == 0, "match_count"].sum()
np_ne_actual = cross_df.loc[
    (cross_df["num_players"] != cross_df["actual_player_count"])
    & (cross_df["actual_player_count"] > 0),
    "match_count"
].sum()

result["q2_mismatch_breakdown"] = {
    "orphaned_matches_no_players": int(orphaned),
    "num_players_ne_actual_with_players": int(np_ne_actual),
}
print(f"Orphaned (actual=0): {orphaned:,}")
print(f"num_players != actual (actual>0): {np_ne_actual:,}")

# Validate orphaned count against 01_03_01
assert abs(int(orphaned) - MATCHES_WITHOUT_PLAYERS) <= 1, (
    f"Orphaned count {orphaned} does not match 01_03_01 linkage integrity "
    f"({MATCHES_WITHOUT_PLAYERS}). Investigate."
)
print(f"\nOrphaned count validated against 01_03_01: {MATCHES_WITHOUT_PLAYERS:,}")

# %%
# Compute actual player counts per game_id (non-orphaned matches only)
sql_player_counts = """
SELECT
    actual_player_count,
    COUNT(*) AS num_matches
FROM (
    SELECT game_id, COUNT(*) AS actual_player_count
    FROM players_raw
    GROUP BY game_id
) sub
GROUP BY actual_player_count
ORDER BY actual_player_count
"""
sql_queries["player_counts_distribution"] = sql_player_counts
df_player_counts = db.fetch_df(sql_player_counts)
print(df_player_counts.to_string(index=False))

# W2 fix: Cross-validate against census players_per_match
# census["players_per_match"] uses "match_count" (not "count") per 01_02_04 artifact
census_count_2 = next(
    (entry["match_count"] for entry in census["players_per_match"] if entry["player_count"] == 2),
    None
)
assert census_count_2 is not None, "Census missing player_count=2 entry"
recomputed_2 = int(df_player_counts[df_player_counts["actual_player_count"] == 2]["num_matches"].iloc[0])
delta_pct = abs(recomputed_2 - census_count_2) / census_count_2 * 100
assert delta_pct <= 1.0, (
    f"player_count=2 mismatch exceeds 1%: "
    f"census={census_count_2:,}, recomputed={recomputed_2:,}, delta={delta_pct:.3f}%"
)
print(f"Cross-validation PASSED: census={census_count_2:,}, recomputed={recomputed_2:,} "
      f"(delta={recomputed_2 - census_count_2:+,}, {delta_pct:.3f}%)")

# %% [markdown]
# ## Q3: True 1v1 Count (Player-Count Method)
#
# A "true 1v1" match is one with exactly 2 rows in players_raw for that
# game_id. This is a structural criterion, independent of the leaderboard
# label.

# %%
sql_true_1v1_count = """
WITH player_counts AS (
    SELECT
        game_id,
        COUNT(*) AS actual_player_count
    FROM players_raw
    GROUP BY game_id
    HAVING COUNT(*) = 2
)
SELECT COUNT(*) AS true_1v1_count
FROM player_counts
"""
sql_queries["true_1v1_count"] = sql_true_1v1_count
true_1v1_df = db.fetch_df(sql_true_1v1_count)
true_1v1_count = int(true_1v1_df["true_1v1_count"].iloc[0])
result["true_1v1_count"] = true_1v1_count
print(f"True 1v1 matches (exactly 2 player rows): {true_1v1_count:,}")

# %%
# B1 diagnostic: quantify how many game_ids might be misclassified due to
# the 489 duplicate player rows identified in 01_03_01.
# A game_id with 2 DISTINCT players but COUNT(*) = 3 would be excluded by
# the raw-count criterion. This query counts such cases.
duplicate_impact_sql = """
WITH raw_counts AS (
    SELECT game_id, COUNT(*) AS raw_count
    FROM players_raw
    GROUP BY game_id
),
distinct_counts AS (
    SELECT game_id, COUNT(DISTINCT profile_id) AS distinct_profiles
    FROM players_raw
    GROUP BY game_id
)
SELECT
    COUNT(*) FILTER (WHERE rc.raw_count = 2) AS matches_exactly_2_raw,
    COUNT(*) FILTER (WHERE dc.distinct_profiles = 2) AS matches_exactly_2_distinct,
    COUNT(*) FILTER (WHERE rc.raw_count != 2 AND dc.distinct_profiles = 2)
        AS recovered_by_dedup,
    COUNT(*) FILTER (WHERE rc.raw_count = 3 AND dc.distinct_profiles = 2)
        AS misclassified_count_3_but_2_distinct
FROM raw_counts rc
JOIN distinct_counts dc ON rc.game_id = dc.game_id
"""
sql_queries["duplicate_impact"] = duplicate_impact_sql
print("Duplicate impact diagnostic...")
df_dup_impact = db.fetch_df(duplicate_impact_sql).iloc[0]
print(f"  Matches with exactly 2 raw rows: {int(df_dup_impact['matches_exactly_2_raw']):,}")
print(f"  Matches with exactly 2 distinct profiles: {int(df_dup_impact['matches_exactly_2_distinct']):,}")
print(f"  Recovered by dedup (raw!=2 but distinct=2): {int(df_dup_impact['recovered_by_dedup']):,}")
print(f"  Specifically count=3 but 2 distinct (most likely dup case): "
      f"{int(df_dup_impact['misclassified_count_3_but_2_distinct']):,}")
duplicate_impact = df_dup_impact.to_dict()
result["duplicate_impact"] = duplicate_impact

# %%
sql_true_1v1_by_leaderboard = """
WITH player_counts AS (
    SELECT
        game_id,
        COUNT(*) AS actual_player_count
    FROM players_raw
    GROUP BY game_id
    HAVING COUNT(*) = 2
)
SELECT
    m.leaderboard,
    COUNT(*) AS match_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 4) AS pct_of_true_1v1
FROM matches_raw m
INNER JOIN player_counts pc ON m.game_id = pc.game_id
GROUP BY m.leaderboard
ORDER BY match_count DESC
"""
sql_queries["true_1v1_by_leaderboard"] = sql_true_1v1_by_leaderboard
true_1v1_lb_df = db.fetch_df(sql_true_1v1_by_leaderboard)
print(true_1v1_lb_df.to_string(index=False))
result["true_1v1_by_leaderboard"] = true_1v1_lb_df.to_dict(orient="records")

# %%
sql_true_1v1_by_num_players = """
WITH player_counts AS (
    SELECT
        game_id,
        COUNT(*) AS actual_player_count
    FROM players_raw
    GROUP BY game_id
    HAVING COUNT(*) = 2
)
SELECT
    m.num_players,
    COUNT(*) AS match_count
FROM matches_raw m
INNER JOIN player_counts pc ON m.game_id = pc.game_id
GROUP BY m.num_players
ORDER BY m.num_players
"""
sql_queries["true_1v1_by_num_players"] = sql_true_1v1_by_num_players
true_1v1_np_df = db.fetch_df(sql_true_1v1_by_num_players)
print(true_1v1_np_df.to_string(index=False))
result["true_1v1_by_num_players"] = true_1v1_np_df.to_dict(orient="records")

# %% [markdown]
# ## Q4: True 1v1 vs Ranked 1v1 (Leaderboard Filter)
#
# Compare two sets:
# - **Set A (True 1v1):** game_ids with exactly 2 player rows
# - **Set B (Ranked 1v1):** game_ids with leaderboard = 'random_map'
#
# Report: |A AND B|, |A NOT B|, |B NOT A|, |A|, |B|.

# %%
sql_set_comparison = """
WITH player_counts AS (
    SELECT
        game_id,
        COUNT(*) AS actual_player_count
    FROM players_raw
    GROUP BY game_id
),
classified AS (
    SELECT
        m.game_id,
        m.leaderboard,
        m.num_players,
        COALESCE(pc.actual_player_count, 0) AS actual_player_count,
        (COALESCE(pc.actual_player_count, 0) = 2)    AS is_true_1v1,
        (m.leaderboard = 'random_map')                AS is_ranked_1v1
    FROM matches_raw m
    LEFT JOIN player_counts pc ON m.game_id = pc.game_id
)
SELECT
    COUNT(*) AS total_matches,
    COUNT(*) FILTER (WHERE is_true_1v1)                               AS true_1v1,
    COUNT(*) FILTER (WHERE is_ranked_1v1)                             AS ranked_1v1,
    COUNT(*) FILTER (WHERE is_true_1v1 AND is_ranked_1v1)             AS overlap_both,
    COUNT(*) FILTER (WHERE is_true_1v1 AND NOT is_ranked_1v1)         AS true_only,
    COUNT(*) FILTER (WHERE NOT is_true_1v1 AND is_ranked_1v1)         AS ranked_only,
    COUNT(*) FILTER (WHERE NOT is_true_1v1 AND NOT is_ranked_1v1)     AS neither
FROM classified
"""
sql_queries["set_comparison"] = sql_set_comparison
set_df = db.fetch_df(sql_set_comparison)
print(set_df.T.to_string())

result["q4_set_comparison"] = {
    "total_matches": int(set_df["total_matches"].iloc[0]),
    "true_1v1": int(set_df["true_1v1"].iloc[0]),
    "ranked_1v1": int(set_df["ranked_1v1"].iloc[0]),
    "overlap_both": int(set_df["overlap_both"].iloc[0]),
    "true_only": int(set_df["true_only"].iloc[0]),
    "ranked_only": int(set_df["ranked_only"].iloc[0]),
    "neither": int(set_df["neither"].iloc[0]),
}

# Derived overlap metrics
overlap = result["q4_set_comparison"]["overlap_both"]
true_1v1_total = result["q4_set_comparison"]["true_1v1"]
ranked_total = result["q4_set_comparison"]["ranked_1v1"]
result["q4_overlap_metrics"] = {
    "jaccard_index": round(overlap / (true_1v1_total + ranked_total - overlap), 6) if (true_1v1_total + ranked_total - overlap) > 0 else 0,
    "overlap_pct_of_true": round(overlap / true_1v1_total * 100, 4) if true_1v1_total > 0 else 0,
    "overlap_pct_of_ranked": round(overlap / ranked_total * 100, 4) if ranked_total > 0 else 0,
}
print(f"\nJaccard index: {result['q4_overlap_metrics']['jaccard_index']}")
print(f"Overlap as % of true 1v1: {result['q4_overlap_metrics']['overlap_pct_of_true']}%")
print(f"Overlap as % of ranked 1v1: {result['q4_overlap_metrics']['overlap_pct_of_ranked']}%")

# %%
sql_ranked_not_true_1v1 = """
WITH player_counts AS (
    SELECT
        game_id,
        COUNT(*) AS actual_player_count
    FROM players_raw
    GROUP BY game_id
)
SELECT
    m.num_players,
    COALESCE(pc.actual_player_count, 0) AS actual_player_count,
    COUNT(*) AS match_count
FROM matches_raw m
LEFT JOIN player_counts pc ON m.game_id = pc.game_id
WHERE m.leaderboard = 'random_map'
  AND COALESCE(pc.actual_player_count, 0) != 2
GROUP BY m.num_players, COALESCE(pc.actual_player_count, 0)
ORDER BY match_count DESC
"""
sql_queries["ranked_not_true_1v1"] = sql_ranked_not_true_1v1
ranked_not_df = db.fetch_df(sql_ranked_not_true_1v1)
print("Ranked 1v1 (leaderboard='random_map') with != 2 player rows:")
print(ranked_not_df.to_string(index=False))
result["q4_ranked_not_true_1v1"] = ranked_not_df.to_dict(orient="records")

# %%
sql_true_not_ranked = """
WITH player_counts AS (
    SELECT
        game_id,
        COUNT(*) AS actual_player_count
    FROM players_raw
    GROUP BY game_id
    HAVING COUNT(*) = 2
)
SELECT
    m.leaderboard,
    COUNT(*) AS match_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 4) AS pct
FROM matches_raw m
INNER JOIN player_counts pc ON m.game_id = pc.game_id
WHERE m.leaderboard != 'random_map'
GROUP BY m.leaderboard
ORDER BY match_count DESC
"""
sql_queries["true_not_ranked"] = sql_true_not_ranked
true_not_df = db.fetch_df(sql_true_not_ranked)
print("True 1v1 (2 player rows) with leaderboard != 'random_map':")
print(true_not_df.to_string(index=False))
result["q4_true_not_ranked"] = true_not_df.to_dict(orient="records")

# %% [markdown]
# ## Edge Case: profile_id NULL Distribution by Match Type

# %%
sql_null_profile_by_type = """
WITH player_counts AS (
    SELECT
        game_id,
        COUNT(*) AS actual_player_count
    FROM players_raw
    GROUP BY game_id
)
SELECT
    m.leaderboard,
    COALESCE(pc.actual_player_count, 0) AS actual_player_count,
    COUNT(*) AS null_profile_rows
FROM players_raw p
INNER JOIN matches_raw m ON p.game_id = m.game_id
LEFT JOIN player_counts pc ON p.game_id = pc.game_id
WHERE p.profile_id IS NULL
GROUP BY m.leaderboard, COALESCE(pc.actual_player_count, 0)
ORDER BY null_profile_rows DESC
"""
sql_queries["null_profile_by_type"] = sql_null_profile_by_type
null_prof_df = db.fetch_df(sql_null_profile_by_type)
print("NULL profile_id rows by leaderboard and player count:")
print(null_prof_df.to_string(index=False))
result["null_profile_id_by_type"] = null_prof_df.to_dict(orient="records")

# %% [markdown]
# ## Summary and Synthesis

# %%
# Consolidate key counts into a summary dict
# Use existing result values -- no new queries needed
sc = result["q4_set_comparison"]

result["summary"] = {
    "total_matches_in_dataset": MATCHES_TOTAL,
    "matches_with_player_data": MATCHES_TOTAL - MATCHES_WITHOUT_PLAYERS,
    "matches_without_player_data": MATCHES_WITHOUT_PLAYERS,
    "true_1v1_count": result["true_1v1_count"],
    "ranked_1v1_count": sc["ranked_1v1"],
    "overlap": sc["overlap_both"],
    "true_1v1_pct_of_all": round(result["true_1v1_count"] / MATCHES_TOTAL * 100, 4),
    "ranked_1v1_pct_of_all": round(sc["ranked_1v1"] / MATCHES_TOTAL * 100, 4),
    "profiling_notes": (
        f"Player-count method (actual_player_count=2) and leaderboard proxy "
        f"(leaderboard='random_map') overlap analysis complete. "
        f"Orphaned game_ids (no player rows): see cross_table_linkage from 01_03_01. "
        f"Duplicate impact bounded by duplicate_impact diagnostic above."
    ),
}

for k, v in result["summary"].items():
    if isinstance(v, (int, float)):
        print(f"  {k}: {v:,}" if isinstance(v, int) else f"  {k}: {v}")
    else:
        print(f"  {k}: {v}")

# %%
# Bar chart: Venn-style breakdown
categories = ["Overlap\n(True AND Ranked)", "True 1v1 Only", "Ranked 1v1 Only", "Neither"]
values = [
    sc["overlap_both"],
    sc["true_only"],
    sc["ranked_only"],
    sc["neither"],
]
colors = ["#2ecc71", "#3498db", "#e67e22", "#95a5a6"]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(categories, values, color=colors, edgecolor="black", linewidth=0.5)

# Add count labels on bars
for bar, val in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + MATCHES_TOTAL * 0.005,
        f"{val:,.0f}\n({val / MATCHES_TOTAL * 100:.1f}%)",
        ha="center", va="bottom", fontsize=9,
    )

ax.set_ylabel("Number of Matches")
ax.set_title(
    "aoestats: True 1v1 vs Ranked 1v1 (leaderboard='random_map') Comparison\n"
    f"Total matches: {MATCHES_TOTAL:,}",
    fontsize=11,
)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))

plt.tight_layout()
chart_path = profiling_dir / "01_03_02_match_type_breakdown.png"
fig.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {chart_path}")

# %%
# Add SQL queries to result for reproducibility (I6)
result["sql_queries"] = sql_queries

json_path = profiling_dir / "01_03_02_true_1v1_profile.json"
with open(json_path, "w") as f:
    json.dump(result, f, indent=2, default=str)
print(f"Saved: {json_path} ({json_path.stat().st_size:,} bytes)")

# Gate validation: required keys
for key in ["true_1v1_count", "ranked_1v1_count", "overlap",
            "q2_num_players_vs_actual_crosstab", "profiling_notes", "duplicate_impact"]:
    # ranked_1v1_count and overlap are nested under different keys
    if key == "ranked_1v1_count":
        assert result["q4_set_comparison"]["ranked_1v1"] > 0, f"Missing/zero: {key}"
    elif key == "overlap":
        assert "overlap_both" in result["q4_set_comparison"], f"Missing: {key}"
    elif key == "profiling_notes":
        assert "profiling_notes" in result["summary"], f"Missing summary key: {key}"
    elif key == "duplicate_impact":
        assert "duplicate_impact" in result, f"Missing key: {key}"
    else:
        assert key in result, f"Missing key: {key}"
print("Gate validation: all required JSON keys present.")

# %%
md_lines = [
    "# Step 01_03_02 -- True 1v1 Match Identification: aoestats",
    "",
    f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}",
    f"**Dataset:** aoestats",
    f"**Invariants:** #6 (SQL verbatim), #7 (no magic numbers), #9 (profiling only)",
    "",
    "## Summary",
    "",
    f"| Metric | Count | % of Total |",
    f"|--------|-------|------------|",
    f"| Total matches | {MATCHES_TOTAL:,} | 100.0% |",
    f"| Matches with player data | {MATCHES_TOTAL - MATCHES_WITHOUT_PLAYERS:,} | {(MATCHES_TOTAL - MATCHES_WITHOUT_PLAYERS) / MATCHES_TOTAL * 100:.2f}% |",
    f"| Matches without player data | {MATCHES_WITHOUT_PLAYERS:,} | {MATCHES_WITHOUT_PLAYERS / MATCHES_TOTAL * 100:.2f}% |",
    f"| **True 1v1** (2 player rows) | **{result['true_1v1_count']:,}** | **{result['summary']['true_1v1_pct_of_all']}%** |",
    f"| Ranked 1v1 (leaderboard='random_map') | {sc['ranked_1v1']:,} | {result['summary']['ranked_1v1_pct_of_all']}% |",
    "",
    "## Q1: Active Player Definition",
    "",
    "Every row in players_raw is an active player. The schema has no observer/",
    "spectator marker columns. winner is never NULL, civ is never NULL, team",
    "has values {0, 1} only. profile_id has 1,185 NULLs (0.0011%).",
    "",
    "## Q2: num_players vs Actual Player Count",
    "",
    "### Cross-tabulation",
    "",
]

# Add cross-tab table
cross_records = result["q2_num_players_vs_actual_crosstab"]
md_lines.append("| num_players | actual_player_count | match_count | pct |")
md_lines.append("|-------------|--------------------:|------------:|----:|")
for r in cross_records:
    md_lines.append(
        f"| {r['num_players']} | {r['actual_player_count']} "
        f"| {int(r['match_count']):,} | {r['pct']}% |"
    )

align = result["q2_alignment_summary"]
md_lines.extend([
    "",
    f"**Alignment:** {align['aligned_count']:,} / {align['total_matches']:,} "
    f"({align['aligned_pct']}%) of matches have num_players == actual player count.",
    f"**Mismatched:** {align['mismatched_count']:,} ({align['mismatched_pct']}%).",
    "",
    "## Q3: True 1v1 Count",
    "",
    f"**True 1v1 matches (exactly 2 player rows): {result['true_1v1_count']:,}**",
    "",
    "### By leaderboard",
    "",
    "| leaderboard | match_count | pct_of_true_1v1 |",
    "|-------------|------------:|----------------:|",
])
for r in result["true_1v1_by_leaderboard"]:
    md_lines.append(
        f"| {r['leaderboard']} | {int(r['match_count']):,} | {r['pct_of_true_1v1']}% |"
    )

md_lines.extend([
    "",
    "## Q4: True 1v1 vs Ranked 1v1 Comparison",
    "",
    "| Set | Count |",
    "|-----|------:|",
    f"| True 1v1 (A) | {sc['true_1v1']:,} |",
    f"| Ranked 1v1 (B) | {sc['ranked_1v1']:,} |",
    f"| A AND B (overlap) | {sc['overlap_both']:,} |",
    f"| A NOT B (true only) | {sc['true_only']:,} |",
    f"| B NOT A (ranked only) | {sc['ranked_only']:,} |",
    f"| Neither | {sc['neither']:,} |",
    "",
    f"**Jaccard index:** {result['q4_overlap_metrics']['jaccard_index']}",
    f"**Overlap as % of true 1v1:** {result['q4_overlap_metrics']['overlap_pct_of_true']}%",
    f"**Overlap as % of ranked 1v1:** {result['q4_overlap_metrics']['overlap_pct_of_ranked']}%",
    "",
    "### Ranked 1v1 with != 2 player rows (anomalies)",
])
if result["q4_ranked_not_true_1v1"]:
    md_lines.append("| num_players | actual_player_count | match_count |")
    md_lines.append("|-------------|--------------------:|------------:|")
    for r in result["q4_ranked_not_true_1v1"]:
        md_lines.append(
            f"| {r['num_players']} | {r['actual_player_count']} | {int(r['match_count']):,} |"
        )
else:
    md_lines.append("*No anomalies found.*")

md_lines.extend([
    "",
    "### True 1v1 from non-random_map leaderboards",
    "",
])
if result["q4_true_not_ranked"]:
    md_lines.append("| leaderboard | match_count | pct |")
    md_lines.append("|-------------|------------:|----:|")
    for r in result["q4_true_not_ranked"]:
        md_lines.append(
            f"| {r['leaderboard']} | {int(r['match_count']):,} | {r['pct']}% |"
        )
else:
    md_lines.append("*All true 1v1 matches are from random_map.*")

md_lines.extend([
    "",
    "## Visualization",
    "",
    "![Match type breakdown](01_03_02_match_type_breakdown.png)",
    "",
    "## SQL Queries (I6)",
    "",
])
for name, sql in sql_queries.items():
    md_lines.append(f"### {name}")
    md_lines.append("```sql")
    md_lines.append(sql.strip())
    md_lines.append("```")
    md_lines.append("")

md_path = profiling_dir / "01_03_02_true_1v1_profile.md"
md_path.write_text("\n".join(md_lines))
print(f"Saved: {md_path} ({md_path.stat().st_size:,} bytes)")
