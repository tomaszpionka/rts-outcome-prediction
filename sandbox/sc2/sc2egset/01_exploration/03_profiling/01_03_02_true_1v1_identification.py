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
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Step 01_03_02 -- True 1v1 Match Identification
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_03 -- Systematic Data Profiling
# **Dataset:** sc2egset
# **Question:** Which of the 22,390 replays are genuine 1v1 matches?
# **Invariants applied:** #6 (all SQL stored verbatim), #7 (all thresholds
# data-derived from census), #9 (profiling only, no cleaning decisions)
# **Predecessor:** 01_03_01 (Systematic Data Profiling -- complete)
# **Type:** Read-only -- no DuckDB writes

# %% [markdown]
# ## Cell 2 -- Imports

# %%
import json
from pathlib import Path

import pandas as pd

from rts_predict.common.notebook_utils import (
    get_notebook_db,
    get_reports_dir,
    setup_notebook_logging,
)

logger = setup_notebook_logging()

# %% [markdown]
# ## Cell 3 -- DuckDB connection

# %%
conn = get_notebook_db("sc2", "sc2egset")

# %% [markdown]
# ## Cell 4 -- Census load and runtime constants (I7)

# %%
reports_dir = get_reports_dir("sc2", "sc2egset")
census_json_path = (
    reports_dir / "artifacts" / "01_exploration" / "02_eda"
    / "01_02_04_univariate_census.json"
)
with open(census_json_path) as f:
    census = json.load(f)

profile_json_path = (
    reports_dir / "artifacts" / "01_exploration" / "03_profiling"
    / "01_03_01_systematic_profile.json"
)
with open(profile_json_path) as f:
    profile = json.load(f)

# --- Runtime constants from census (Invariant #7) ---
RP_TOTAL_ROWS = census["null_census"]["replay_players_raw"]["total_rows"]
print(f"replay_players_raw total rows: {RP_TOTAL_ROWS}")

RM_TOTAL_ROWS = census["null_census"]["replays_meta_raw_filename"]["total_rows"]
print(f"replays_meta_raw total rows: {RM_TOTAL_ROWS}")

# Derive STANDARD_RACES dynamically from census -- I7: no magic numbers
STANDARD_RACES = sorted([
    entry['selectedRace']
    for entry in census['categorical_profiles']['selectedRace']
    if entry['selectedRace'] != '' and not entry['selectedRace'].startswith('BW')
])
# Assert expected values match (guard against census change)
assert set(STANDARD_RACES) == {'Prot', 'Zerg', 'Terr', 'Rand'}, \
    f"Unexpected STANDARD_RACES from census: {STANDARD_RACES}"
print(f"Standard races (derived from census at runtime): {STANDARD_RACES}")

# Non-2p results from census
non_2p_total = sum(r["cnt"] for r in census["non_2p_results"])
print(f"non_2p player rows (census): {non_2p_total}")

# Result distribution from census
result_dist = {r["result"]: r["cnt"] for r in census["result_distribution"]}
N_WIN = result_dist["Win"]
N_LOSS = result_dist["Loss"]
N_UNDECIDED = result_dist.get("Undecided", 0)
N_TIE = result_dist.get("Tie", 0)
print(f"Win: {N_WIN}, Loss: {N_LOSS}, Undecided: {N_UNDECIDED}, Tie: {N_TIE}")

# playerID cardinality from census
PLAYER_ID_CARDINALITY = census["cardinality"][3]["cardinality"]  # playerID entry
print(f"playerID cardinality: {PLAYER_ID_CARDINALITY}")

# Output directories
artifact_dir = (
    reports_dir / "artifacts" / "01_exploration" / "03_profiling"
)
artifact_dir.mkdir(parents=True, exist_ok=True)
print(f"Artifact dir: {artifact_dir}")

# %% [markdown]
# ## Cell 5 -- SQL queries dict (I6)

# %%
sql_queries = {}

# %% [markdown]
# ## Cell 6 -- Players-per-replay distribution (T03)

# %%
sql_queries["players_per_replay"] = """
SELECT
    players_per_replay,
    COUNT(*) AS replay_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 4) AS pct
FROM (
    SELECT
        filename,
        COUNT(*) AS players_per_replay
    FROM replay_players_raw
    GROUP BY filename
)
GROUP BY players_per_replay
ORDER BY players_per_replay
"""

players_per_replay_df = conn.con.execute(sql_queries["players_per_replay"]).df()
print("=== Players per replay distribution ===")
print(players_per_replay_df.to_string(index=False))
total_replays_check = players_per_replay_df["replay_count"].sum()
print(f"\nTotal replays: {total_replays_check} (expected: {RM_TOTAL_ROWS})")
assert total_replays_check == RM_TOTAL_ROWS, (
    f"Replay count mismatch: {total_replays_check} != {RM_TOTAL_ROWS}"
)

# %% [markdown]
# ## Cell 7 -- Replays with non-2 player rows (detail) (T03)

# %%
sql_queries["non_2p_replay_detail"] = """
SELECT
    rp.filename,
    COUNT(*) AS player_row_count,
    LIST(rp.playerID ORDER BY rp.playerID) AS player_ids,
    LIST(rp.selectedRace ORDER BY rp.playerID) AS selected_races,
    LIST(rp.result ORDER BY rp.playerID) AS results,
    LIST(rp.nickname ORDER BY rp.playerID) AS nicknames,
    rm.initData.gameDescription.maxPlayers AS max_players_setting,
    rm.initData.gameDescription.gameOptions.observers AS observer_setting
FROM replay_players_raw rp
JOIN replays_meta_raw rm ON rp.filename = rm.filename
GROUP BY rp.filename, max_players_setting, observer_setting
HAVING COUNT(*) != 2
ORDER BY COUNT(*) DESC, rp.filename
"""

non_2p_detail_df = conn.con.execute(sql_queries["non_2p_replay_detail"]).df()
print(f"=== Replays with != 2 player rows: {len(non_2p_detail_df)} ===")
print(non_2p_detail_df.to_string(index=False))

# %% [markdown]
# ## Cell 8 -- max_players value distribution (T04)

# %%
sql_queries["max_players_distribution"] = """
SELECT
    initData.gameDescription.maxPlayers AS max_players,
    COUNT(*) AS replay_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 4) AS pct
FROM replays_meta_raw
GROUP BY max_players
ORDER BY max_players
"""

max_players_df = conn.con.execute(sql_queries["max_players_distribution"]).df()
print("=== max_players distribution ===")
print(max_players_df.to_string(index=False))

# %% [markdown]
# ## Cell 9 -- Observer setting distribution (T04)

# %%
sql_queries["observer_setting_distribution"] = """
SELECT
    initData.gameDescription.gameOptions.observers AS observer_setting,
    COUNT(*) AS replay_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 4) AS pct
FROM replays_meta_raw
GROUP BY observer_setting
ORDER BY observer_setting
"""

observer_df = conn.con.execute(sql_queries["observer_setting_distribution"]).df()
print("=== Observer setting distribution ===")
print(observer_df.to_string(index=False))

# %% [markdown]
# ## Cell 10 -- Cross-tabulation: max_players vs actual player row count (T04)

# %%
sql_queries["max_players_vs_actual"] = """
SELECT
    rm.initData.gameDescription.maxPlayers AS max_players,
    pc.players_per_replay,
    COUNT(*) AS replay_count
FROM replays_meta_raw rm
JOIN (
    SELECT filename, COUNT(*) AS players_per_replay
    FROM replay_players_raw
    GROUP BY filename
) pc ON rm.filename = pc.filename
GROUP BY max_players, players_per_replay
ORDER BY max_players, players_per_replay
"""

cross_tab_df = conn.con.execute(sql_queries["max_players_vs_actual"]).df()
print("=== max_players vs actual player row count ===")
print(cross_tab_df.to_string(index=False))

# %% [markdown]
# ## Cell 11 -- Empty selectedRace profile (T05)

# %%
sql_queries["empty_race_profile"] = """
SELECT
    rp.filename,
    rp.playerID,
    rp.nickname,
    rp.selectedRace,
    rp.race,
    rp.result,
    rp.MMR,
    rp.APM,
    rp.highestLeague,
    rm.initData.gameDescription.maxPlayers AS max_players,
    rm.initData.gameDescription.gameOptions.observers AS observer_setting,
    pc.players_per_replay
FROM replay_players_raw rp
JOIN replays_meta_raw rm ON rp.filename = rm.filename
JOIN (
    SELECT filename, COUNT(*) AS players_per_replay
    FROM replay_players_raw
    GROUP BY filename
) pc ON rp.filename = pc.filename
WHERE rp.selectedRace = ''
ORDER BY pc.players_per_replay DESC, rp.filename, rp.playerID
"""

empty_race_df = conn.con.execute(sql_queries["empty_race_profile"]).df()
print(f"=== Empty selectedRace rows: {len(empty_race_df)} ===")
print(f"Unique replays with empty selectedRace: {empty_race_df['filename'].nunique()}")
print(f"\nPlayers_per_replay distribution for these rows:")
print(empty_race_df["players_per_replay"].value_counts().sort_index().to_string())
print(f"\nResult distribution for empty selectedRace:")
print(empty_race_df["result"].value_counts().to_string())
print(f"\nRace (resolved) distribution for empty selectedRace:")
print(empty_race_df["race"].value_counts().to_string())
print(f"\nAPM distribution for empty selectedRace:")
print(empty_race_df["APM"].describe().to_string())
print(f"\nMMR distribution for empty selectedRace:")
print(empty_race_df["MMR"].describe().to_string())
print(f"\nFirst 20 rows:")
print(empty_race_df.head(20).to_string(index=False))

# %% [markdown]
# ## Cell 12 -- BW race variant context (T06)

# %%
sql_queries["bw_race_context"] = """
SELECT
    rp.filename,
    rp.playerID,
    rp.selectedRace,
    rp.race,
    rp.result,
    rp.APM,
    pc.players_per_replay,
    rm.initData.gameDescription.maxPlayers AS max_players
FROM replay_players_raw rp
JOIN replays_meta_raw rm ON rp.filename = rm.filename
JOIN (
    SELECT filename, COUNT(*) AS players_per_replay
    FROM replay_players_raw
    GROUP BY filename
) pc ON rp.filename = pc.filename
WHERE rp.selectedRace IN ('BWTe', 'BWZe', 'BWPr')
ORDER BY rp.filename, rp.playerID
"""

bw_df = conn.con.execute(sql_queries["bw_race_context"]).df()
print(f"=== BW race variant rows: {len(bw_df)} ===")
print(bw_df.to_string(index=False))

# %% [markdown]
# ## Cell 13 -- Undecided/Tie replays in 1v1 context (T06)

# %%
sql_queries["undecided_tie_1v1_context"] = """
SELECT
    rp.filename,
    rp.playerID,
    rp.selectedRace,
    rp.result,
    pc.players_per_replay,
    rm.initData.gameDescription.maxPlayers AS max_players
FROM replay_players_raw rp
JOIN replays_meta_raw rm ON rp.filename = rm.filename
JOIN (
    SELECT filename, COUNT(*) AS players_per_replay
    FROM replay_players_raw
    GROUP BY filename
) pc ON rp.filename = pc.filename
WHERE rp.result IN ('Undecided', 'Tie')
ORDER BY rp.result, rp.filename, rp.playerID
"""

undecided_df = conn.con.execute(sql_queries["undecided_tie_1v1_context"]).df()
print(f"=== Undecided/Tie rows: {len(undecided_df)} ===")
print(f"Unique replays: {undecided_df['filename'].nunique()}")
print(f"\nPlayers_per_replay for Undecided/Tie replays:")
print(undecided_df["players_per_replay"].value_counts().sort_index().to_string())

# %% [markdown]
# ## Cell 14 -- Comprehensive replay classification (T07)

# %%
sql_queries["replay_classification"] = """
WITH per_replay AS (
    SELECT
        rp.filename,
        COUNT(*) AS player_row_count,
        COUNT(*) FILTER (
            WHERE rp.selectedRace IN ('Prot', 'Zerg', 'Terr', 'Rand')
        ) AS standard_race_count,
        COUNT(*) FILTER (WHERE rp.result IN ('Win', 'Loss')) AS decisive_count,
        COUNT(*) FILTER (WHERE rp.result = 'Win') AS win_count,
        COUNT(*) FILTER (WHERE rp.result = 'Loss') AS loss_count,
        COUNT(*) FILTER (WHERE rp.result = 'Undecided') AS undecided_count,
        COUNT(*) FILTER (WHERE rp.result = 'Tie') AS tie_count,
        COUNT(*) FILTER (WHERE rp.selectedRace = '') AS empty_race_count,
        COUNT(*) FILTER (
            WHERE rp.selectedRace IN ('BWTe', 'BWZe', 'BWPr')
        ) AS bw_race_count,
        rm.initData.gameDescription.maxPlayers AS max_players,
        rm.initData.gameDescription.gameOptions.observers AS observer_setting
    FROM replay_players_raw rp
    JOIN replays_meta_raw rm ON rp.filename = rm.filename
    GROUP BY rp.filename, max_players, observer_setting
)
SELECT
    filename,
    player_row_count,
    standard_race_count,
    decisive_count,
    win_count,
    loss_count,
    undecided_count,
    tie_count,
    empty_race_count,
    bw_race_count,
    max_players,
    observer_setting,
    CASE
        WHEN player_row_count = 2
             AND decisive_count = 2
             AND win_count = 1
             AND loss_count = 1
        THEN 'true_1v1_decisive'
        WHEN player_row_count < 2
        THEN 'non_1v1_too_few_players'
        WHEN player_row_count > 2
        THEN 'non_1v1_too_many_players'
        WHEN player_row_count = 2
             AND (undecided_count > 0 OR tie_count > 0)
        THEN 'true_1v1_indecisive'
        ELSE 'non_1v1_other'
    END AS classification
FROM per_replay
ORDER BY classification, filename
"""

classification_df = conn.con.execute(sql_queries["replay_classification"]).df()
print("=== Replay classification ===")
class_summary = classification_df["classification"].value_counts()
print(class_summary.to_string())
print(f"\nTotal classified: {len(classification_df)} (expected: {RM_TOTAL_ROWS})")
assert len(classification_df) == RM_TOTAL_ROWS, (
    f"Classification count mismatch: {len(classification_df)} != {RM_TOTAL_ROWS}"
)

# %% [markdown]
# ## Cell 15 -- Classification summary with detail counts (T07)

# %%
sql_queries["classification_summary"] = """
-- Summary aggregation over the per-replay classification
-- (derived from the replay_classification CTE above, re-executed for clarity)
WITH per_replay AS (
    SELECT
        rp.filename,
        COUNT(*) AS player_row_count,
        COUNT(*) FILTER (WHERE rp.result IN ('Win', 'Loss')) AS decisive_count,
        COUNT(*) FILTER (WHERE rp.result = 'Win') AS win_count,
        COUNT(*) FILTER (WHERE rp.result = 'Loss') AS loss_count,
        COUNT(*) FILTER (WHERE rp.result = 'Undecided') AS undecided_count,
        COUNT(*) FILTER (WHERE rp.result = 'Tie') AS tie_count,
        COUNT(*) FILTER (WHERE rp.selectedRace = '') AS empty_race_count,
        rm.initData.gameDescription.maxPlayers AS max_players
    FROM replay_players_raw rp
    JOIN replays_meta_raw rm ON rp.filename = rm.filename
    GROUP BY rp.filename, max_players
),
classified AS (
    SELECT *,
        CASE
            WHEN player_row_count = 2
                 AND decisive_count = 2
                 AND win_count = 1
                 AND loss_count = 1
            THEN 'true_1v1_decisive'
            WHEN player_row_count < 2
            THEN 'non_1v1_too_few_players'
            WHEN player_row_count > 2
            THEN 'non_1v1_too_many_players'
            WHEN player_row_count = 2
                 AND (undecided_count > 0 OR tie_count > 0)
            THEN 'true_1v1_indecisive'
            ELSE 'non_1v1_other'
        END AS classification
    FROM per_replay
)
SELECT
    classification,
    COUNT(*) AS replay_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 4) AS pct,
    MIN(player_row_count) AS min_players,
    MAX(player_row_count) AS max_players_actual,
    SUM(empty_race_count) AS total_empty_race_rows
FROM classified
GROUP BY classification
ORDER BY replay_count DESC
"""

summary_df = conn.con.execute(sql_queries["classification_summary"]).df()
print("=== Classification summary ===")
print(summary_df.to_string(index=False))

# %% [markdown]
# ## Cell 16 -- JSON artifact assembly (T08)

# %%
# Build JSON artifact
artifact = {
    "step": "01_03_02",
    "dataset": "sc2egset",
    "total_replay_count": int(RM_TOTAL_ROWS),
    "total_player_rows": int(RP_TOTAL_ROWS),
    "players_per_replay_distribution": players_per_replay_df.to_dict(orient="records"),
    "max_players_distribution": max_players_df.to_dict(orient="records"),
    "observer_setting_distribution": observer_df.to_dict(orient="records"),
    "max_players_vs_actual_cross_tab": cross_tab_df.to_dict(orient="records"),
    "empty_selectedRace_analysis": {
        "total_rows": len(empty_race_df),
        "unique_replays": int(empty_race_df["filename"].nunique()),
        "players_per_replay_distribution": (
            empty_race_df["players_per_replay"]
            .value_counts()
            .sort_index()
            .to_dict()
        ),
        "result_distribution": (
            empty_race_df["result"].value_counts().to_dict()
        ),
        "race_resolved_distribution": (
            empty_race_df["race"].value_counts().to_dict()
        ),
        "apm_stats": {
            k: float(v)
            for k, v in empty_race_df["APM"].describe().to_dict().items()
        },
    },
    "bw_race_analysis": {
        "total_rows": len(bw_df),
        "detail": bw_df.to_dict(orient="records"),
    },
    "undecided_tie_analysis": {
        "total_rows": len(undecided_df),
        "unique_replays": int(undecided_df["filename"].nunique()),
        "players_per_replay_distribution": (
            undecided_df["players_per_replay"]
            .value_counts()
            .sort_index()
            .to_dict()
        ),
    },
    "replay_classification": {
        "summary": summary_df.to_dict(orient="records"),
        "true_1v1_decisive_count": int(
            summary_df.loc[
                summary_df["classification"] == "true_1v1_decisive", "replay_count"
            ].iloc[0]
        ),
        "true_1v1_indecisive_count": int(
            summary_df.loc[
                summary_df["classification"] == "true_1v1_indecisive", "replay_count"
            ].sum()
        ),
    },
    "non_1v1_replay_detail": non_2p_detail_df.to_dict(orient="records"),
    "classification_criteria": {
        "true_1v1_decisive": "player_row_count == 2 AND win_count == 1 AND loss_count == 1",
        "non_1v1_too_few_players": "player_row_count < 2",
        "non_1v1_too_many_players": "player_row_count > 2",
        "true_1v1_indecisive": (
            "player_row_count == 2 AND (undecided_count > 0 OR tie_count > 0)"
        ),
        "non_1v1_other": "all remaining (should be 0 if classification is exhaustive)",
    },
    "standard_races_used": STANDARD_RACES,
    "sql_queries": sql_queries,
}

# Validation
true_1v1_decisive_count = artifact["replay_classification"]["true_1v1_decisive_count"]
true_1v1_indecisive_count = artifact["replay_classification"]["true_1v1_indecisive_count"]
total_classified = sum(
    r["replay_count"] for r in artifact["replay_classification"]["summary"]
)
assert total_classified == RM_TOTAL_ROWS, (
    f"Classification total {total_classified} != {RM_TOTAL_ROWS}"
)
print(f"true_1v1_decisive: {true_1v1_decisive_count} / {RM_TOTAL_ROWS} "
      f"({100.0 * true_1v1_decisive_count / RM_TOTAL_ROWS:.2f}%)")
print(f"true_1v1_indecisive: {true_1v1_indecisive_count} / {RM_TOTAL_ROWS} "
      f"({100.0 * true_1v1_indecisive_count / RM_TOTAL_ROWS:.2f}%)")

# %% [markdown]
# ## Cell 16b -- Sample row preview for sanity check

# %%
# True 1v1 decisive: 2 players, 1 Win + 1 Loss
sample_true_sql = """
SELECT rp.filename, rp.playerID, rp.selectedRace, rp.result,
       rp.APM, rp.MMR, rp.SQ
FROM replay_players_raw rp
WHERE rp.filename IN (
    SELECT filename FROM replay_players_raw
    GROUP BY filename
    HAVING COUNT(*) = 2
       AND COUNT(*) FILTER (WHERE result = 'Win') = 1
       AND COUNT(*) FILTER (WHERE result = 'Loss') = 1
    LIMIT 5
)
ORDER BY rp.filename, rp.playerID
"""
sql_queries["sample_true_1v1"] = sample_true_sql
print("=== Sample: TRUE 1v1 decisive replays (2 players, 1 Win + 1 Loss) ===")
df_sample_true = conn.con.execute(sample_true_sql).df()
print(df_sample_true.to_string(index=False))

# %%
# Non-1v1: replays with player_row_count != 2 (all 11 shown — small enough)
sample_non1v1_sql = """
SELECT rp.filename, rp.playerID, rp.selectedRace, rp.result, rp.APM
FROM replay_players_raw rp
WHERE rp.filename IN (
    SELECT filename FROM replay_players_raw
    GROUP BY filename HAVING COUNT(*) != 2
)
ORDER BY rp.filename, rp.playerID
"""
sql_queries["sample_non_1v1"] = sample_non1v1_sql
print("=== Sample: NON-1v1 replays (player_row_count != 2) ===")
df_sample_non1v1 = conn.con.execute(sample_non1v1_sql).df()
print(df_sample_non1v1.to_string(index=False))

# %%
json_path = artifact_dir / "01_03_02_true_1v1_profile.json"
with open(json_path, "w") as f:
    json.dump(artifact, f, indent=2, default=str)
print(f"JSON artifact written to: {json_path}")

# %% [markdown]
# ## Cell 17 -- Markdown artifact (T08)

# %%
md_lines = [
    "# Step 01_03_02 -- True 1v1 Match Identification",
    "",
    "**Dataset:** sc2egset",
    "**Phase:** 01 -- Data Exploration",
    "**Pipeline Section:** 01_03 -- Systematic Data Profiling",
    f"**Total replays:** {RM_TOTAL_ROWS}",
    f"**Total player rows:** {RP_TOTAL_ROWS}",
    "",
    "---",
    "",
    "## Players-per-replay distribution",
    "",
    "```sql",
    sql_queries["players_per_replay"].strip(),
    "```",
    "",
    players_per_replay_df.to_markdown(index=False),
    "",
    "## max_players lobby setting distribution",
    "",
    "```sql",
    sql_queries["max_players_distribution"].strip(),
    "```",
    "",
    max_players_df.to_markdown(index=False),
    "",
    "## Observer setting distribution",
    "",
    "```sql",
    sql_queries["observer_setting_distribution"].strip(),
    "```",
    "",
    observer_df.to_markdown(index=False),
    "",
    "## max_players vs actual player row count (cross-tabulation)",
    "",
    "```sql",
    sql_queries["max_players_vs_actual"].strip(),
    "```",
    "",
    cross_tab_df.to_markdown(index=False),
    "",
    "## Empty selectedRace analysis",
    "",
    f"Total rows with selectedRace = '': {len(empty_race_df)}",
    f"Unique replays: {empty_race_df['filename'].nunique()}",
    "",
    "```sql",
    sql_queries["empty_race_profile"].strip(),
    "```",
    "",
    "### Result distribution for empty-selectedRace rows",
    "",
    empty_race_df["result"].value_counts().to_frame().to_markdown(),
    "",
    "### Race (resolved) distribution for empty-selectedRace rows",
    "",
    empty_race_df["race"].value_counts().to_frame().to_markdown(),
    "",
    "## BW race variant context",
    "",
    "```sql",
    sql_queries["bw_race_context"].strip(),
    "```",
    "",
    bw_df.to_markdown(index=False),
    "",
    "## Undecided/Tie replay context",
    "",
    "```sql",
    sql_queries["undecided_tie_1v1_context"].strip(),
    "```",
    "",
    f"Total Undecided/Tie rows: {len(undecided_df)}",
    f"Unique replays: {undecided_df['filename'].nunique()}",
    "",
    "## Replay classification summary",
    "",
    "```sql",
    sql_queries["classification_summary"].strip(),
    "```",
    "",
    summary_df.to_markdown(index=False),
    "",
    "### Classification criteria",
    "",
    "| Classification | Criterion |",
    "|----------------|-----------|",
    "| true_1v1_decisive | player_row_count == 2 AND win_count == 1 AND loss_count == 1 |",
    "| non_1v1_too_few_players | player_row_count < 2 |",
    "| non_1v1_too_many_players | player_row_count > 2 |",
    "| true_1v1_indecisive | player_row_count == 2 AND (undecided_count > 0 OR tie_count > 0) |",
    "| non_1v1_other | Residual category (should be 0) |",
    "",
    f"**true_1v1_decisive replays: {true_1v1_decisive_count} / {RM_TOTAL_ROWS} "
    f"({100.0 * true_1v1_decisive_count / RM_TOTAL_ROWS:.2f}%)**",
    "",
    "The `true_1v1_indecisive` category captures replays that ARE genuine 1v1 matches"
    " (exactly 2 player rows) but lack a decisive Win/Loss outcome (Undecided or Tie).",
    "These are excluded from the prediction pipeline because they have no usable"
    " prediction target -- not because of a game-format issue. The thesis-relevant"
    " population is `true_1v1_decisive`.",
    "",
    "---",
    "",
    "## Observations and thesis implications",
    "",
    "1. **Observation:** [to be filled based on execution results]",
    "   **Thesis implication:** [to be filled]",
    "   **Next action:** Feed classification to 01_04 (Data Cleaning).",
    "",
    "---",
    "",
    "*All SQL queries above are the exact code used to produce these results (I6).*",
    f"*Standard races {STANDARD_RACES} derived from 01_02_04 census (I7).*",
    "*This step classifies replays but does not drop any rows (I9).*",
]

md_path = artifact_dir / "01_03_02_true_1v1_profile.md"
with open(md_path, "w") as f:
    f.write("\n".join(md_lines))
print(f"MD artifact written to: {md_path}")
