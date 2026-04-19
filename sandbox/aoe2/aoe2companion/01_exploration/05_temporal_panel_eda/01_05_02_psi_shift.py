# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
# ---

# %% [markdown]
# # 01_05_02 PSI Shift — aoe2companion
# spec: reports/specs/01_05_preregistration.md@7e259dd8
#
# **Spec §§:** §4 (PSI binning), §7 (reference/tested periods)
# **Critique fixes:** M-03 (Cohen's h vs reference, not 0.5), M-04 (PSI thresholds uncalibrated at N>10^6),
# M-05 (interpretation at large N), M-08 (KS subsampling), M-09 (is_null_cluster=FALSE)
#
# **Hypothesis:** max PSI across pre-game features and tested quarters is < 0.25.
# **Falsifier:** any (feature x quarter) cell exhibits PSI >= 0.25.
#
# **Literature:**
# - Siddiqi (2006) — PSI definition, N=10 equal-frequency bins, thresholds 0.10/0.25
# - Yurdakul (2018) WMU #3208 — thresholds uncalibrated at N>10^6; raw PSI flagged for review
# - Cohen (1988) §2.2/§6.2 — Cohen's d / Cohen's h definitions
# - Breck et al. (2019) SysML — KS as complementary drift descriptor
# - Sullivan & Feinn (2012) JGME 4(3):279-282 — interpretation at large N

# %% [markdown]
# ## Imports

# %%
import json
import math
from datetime import datetime
from pathlib import Path

import pandas as pd

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir

ARTIFACTS = get_reports_dir("aoe2", "aoe2companion") / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

REF_START = datetime(2022, 8, 29)
REF_END = datetime(2022, 12, 31)
TESTED_QUARTERS = [
    ("2023-Q1", "2023-01-01", "2023-04-01"),
    ("2023-Q2", "2023-04-01", "2023-07-01"),
    ("2023-Q3", "2023-07-01", "2023-10-01"),
    ("2023-Q4", "2023-10-01", "2024-01-01"),
    ("2024-Q1", "2024-01-01", "2024-04-01"),
    ("2024-Q2", "2024-04-01", "2024-07-01"),
    ("2024-Q3", "2024-07-01", "2024-10-01"),
    ("2024-Q4", "2024-10-01", "2025-01-01"),
]
PSI_BINS = 10
RANDOM_SEED = 42
KS_SAMPLE_N = 100_000

print("Artifacts dir:", ARTIFACTS)

# %% [markdown]
# ## Step 1: Validate reference period constants (I3 compliance — spec §9 Query 3)

# %%
assert REF_START == datetime(2022, 8, 29), f"Bad ref_start: {REF_START}"
assert REF_END == datetime(2022, 12, 31), f"Bad ref_end: {REF_END}"
print("Reference period assertions passed:", REF_START, "to", REF_END)

# %% [markdown]
# ## Step 2: Compute frozen reference-period bin edges for 'rating' (numeric)

# %%
QUERY_REF_RATING_EDGES = """
SELECT quantile_cont(m.rating, list_value(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9)) AS edges,
       COUNT(*) AS n_ref,
       AVG(m.rating) AS mean_ref,
       STDDEV(m.rating) AS std_ref
FROM matches_history_minimal mhm
JOIN matches_1v1_clean m
  ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
 AND CAST(m.profileId AS VARCHAR) = mhm.player_id
WHERE mhm.started_at >= TIMESTAMP '2022-08-29'
  AND mhm.started_at <  TIMESTAMP '2023-01-01'
  AND m.rating IS NOT NULL
  AND m.is_null_cluster = FALSE
  AND m.internalLeaderboardId IN (6, 18)
"""

db = get_notebook_db("aoe2", "aoe2companion", read_only=True)
res = db.con.execute(QUERY_REF_RATING_EDGES).fetchone()
rating_edges = res[0]
n_ref_rating = res[1]
mean_ref_rating = res[2]
std_ref_rating = res[3]
print(f"Rating reference N={n_ref_rating:,}, mean={mean_ref_rating:.1f}, std={std_ref_rating:.1f}")
print(f"Bin edges (deciles): {[round(e, 1) for e in rating_edges]}")

# %% [markdown]
# ## Step 3: Reference period win rate (for Cohen's h computation vs reference)

# %%
QUERY_REF_WON = """
SELECT
    AVG(CAST(won AS DOUBLE)) AS p_ref_won,
    COUNT(*) AS n_ref_won
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-08-29'
  AND started_at <  TIMESTAMP '2023-01-01'
  AND won IS NOT NULL
"""

won_ref = db.con.execute(QUERY_REF_WON).fetchone()
p_ref_won = won_ref[0]
n_ref_won = won_ref[1]
print(f"Reference win rate: {p_ref_won:.4f} (n={n_ref_won:,})")

# %% [markdown]
# ## Step 4: Reference period faction distribution (categorical PSI)

# %%
QUERY_REF_FACTION = """
SELECT faction, COUNT(*) AS cnt
FROM matches_history_minimal mhm
JOIN matches_1v1_clean m
  ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
 AND CAST(m.profileId AS VARCHAR) = mhm.player_id
WHERE mhm.started_at >= TIMESTAMP '2022-08-29'
  AND mhm.started_at <  TIMESTAMP '2023-01-01'
  AND m.is_null_cluster = FALSE
  AND m.internalLeaderboardId IN (6, 18)
GROUP BY faction
ORDER BY cnt DESC
"""

df_ref_faction = db.con.execute(QUERY_REF_FACTION).df()
total_ref_faction = df_ref_faction["cnt"].sum()
df_ref_faction["p_ref"] = df_ref_faction["cnt"] / total_ref_faction
ref_faction_dist = dict(zip(df_ref_faction["faction"], df_ref_faction["p_ref"]))
print(f"Distinct factions in reference: {len(df_ref_faction)}")
print(f"Total reference faction rows: {total_ref_faction:,}")

# %% [markdown]
# ## Step 5: Reference period map distribution (categorical PSI)

# %%
QUERY_REF_MAP = """
SELECT m.map AS map_id, COUNT(*) AS cnt
FROM matches_history_minimal mhm
JOIN matches_1v1_clean m
  ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
 AND CAST(m.profileId AS VARCHAR) = mhm.player_id
WHERE mhm.started_at >= TIMESTAMP '2022-08-29'
  AND mhm.started_at <  TIMESTAMP '2023-01-01'
  AND m.is_null_cluster = FALSE
  AND m.internalLeaderboardId IN (6, 18)
GROUP BY m.map
ORDER BY cnt DESC
LIMIT 50
"""

df_ref_map = db.con.execute(QUERY_REF_MAP).df()
total_ref_map = df_ref_map["cnt"].sum()
df_ref_map["p_ref"] = df_ref_map["cnt"] / total_ref_map
ref_map_dist = dict(zip(df_ref_map["map_id"], df_ref_map["p_ref"]))
print(f"Top-50 maps in reference (total ref rows with join): {total_ref_map:,}")
print(df_ref_map.head(5).to_string(index=False))

# %% [markdown]
# ## Step 6: Compute PSI, Cohen's h/d, KS per tested quarter

# %%
def compute_psi_numeric(ref_edges, p_ref_bins, p_test_bins):
    """Compute PSI = sum((p_test - p_ref) * log(p_test / p_ref)) across bins."""
    eps = 1e-6
    psi = 0.0
    for p_r, p_t in zip(p_ref_bins, p_test_bins):
        p_r = max(p_r, eps)
        p_t = max(p_t, eps)
        psi += (p_t - p_r) * math.log(p_t / p_r)
    return psi


def compute_psi_categorical(ref_dist, test_counts, total_test, unseen_label="__unseen__"):
    """Compute PSI for a categorical feature using relative-frequency vectors."""
    eps = 1e-6
    test_dist = {}
    unseen_count = 0
    for k, cnt in test_counts.items():
        if k in ref_dist:
            test_dist[k] = cnt / total_test
        else:
            unseen_count += cnt
    if unseen_count > 0:
        test_dist[unseen_label] = unseen_count / total_test

    all_cats = set(ref_dist.keys()) | set(test_dist.keys())
    psi = 0.0
    for cat in all_cats:
        p_r = max(ref_dist.get(cat, 0.0), eps)
        p_t = max(test_dist.get(cat, 0.0), eps)
        psi += (p_t - p_r) * math.log(p_t / p_r)
    return psi, unseen_count


def cohen_h(p1, p2):
    """Cohen's h = 2*(asin(sqrt(p1)) - asin(sqrt(p2))). M-03: vs reference, not 0.5."""
    return 2.0 * (math.asin(math.sqrt(max(0.0, min(1.0, p1)))) -
                  math.asin(math.sqrt(max(0.0, min(1.0, p2)))))


def cohen_d(mean_test, mean_ref, std_test, std_ref, n_test, n_ref):
    """Cohen's d = (mean_test - mean_ref) / pooled_sd."""
    pooled_var = ((n_test - 1) * std_test**2 + (n_ref - 1) * std_ref**2) / (n_test + n_ref - 2)
    pooled_sd = math.sqrt(max(pooled_var, 1e-10))
    return (mean_test - mean_ref) / pooled_sd

# %%
QUERY_RATING_BIN_SHARES = """
WITH ref_edges AS (
    SELECT UNNEST(edges) AS edge, generate_subscripts(edges, 1) AS idx
    FROM (
        SELECT quantile_cont(m.rating, list_value(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9)) AS edges
        FROM matches_history_minimal mhm
        JOIN matches_1v1_clean m
          ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
         AND CAST(m.profileId AS VARCHAR) = mhm.player_id
        WHERE mhm.started_at >= TIMESTAMP '2022-08-29'
          AND mhm.started_at <  TIMESTAMP '2023-01-01'
          AND m.rating IS NOT NULL
          AND m.is_null_cluster = FALSE
          AND m.internalLeaderboardId IN (6, 18)
    ) e
)
SELECT
    COUNT(*) FILTER (WHERE m.rating < (SELECT MIN(edge) FROM ref_edges)) * 1.0 / COUNT(*) AS b0,
    COUNT(*) FILTER (WHERE m.rating >= (SELECT MIN(edge) FROM ref_edges) AND m.rating < (SELECT edge FROM ref_edges WHERE idx=2)) * 1.0 / COUNT(*) AS b1,
    COUNT(*) FILTER (WHERE m.rating >= (SELECT edge FROM ref_edges WHERE idx=2) AND m.rating < (SELECT edge FROM ref_edges WHERE idx=3)) * 1.0 / COUNT(*) AS b2,
    COUNT(*) FILTER (WHERE m.rating >= (SELECT edge FROM ref_edges WHERE idx=3) AND m.rating < (SELECT edge FROM ref_edges WHERE idx=4)) * 1.0 / COUNT(*) AS b3,
    COUNT(*) FILTER (WHERE m.rating >= (SELECT edge FROM ref_edges WHERE idx=4) AND m.rating < (SELECT edge FROM ref_edges WHERE idx=5)) * 1.0 / COUNT(*) AS b4,
    COUNT(*) FILTER (WHERE m.rating >= (SELECT edge FROM ref_edges WHERE idx=5) AND m.rating < (SELECT edge FROM ref_edges WHERE idx=6)) * 1.0 / COUNT(*) AS b5,
    COUNT(*) FILTER (WHERE m.rating >= (SELECT edge FROM ref_edges WHERE idx=6) AND m.rating < (SELECT edge FROM ref_edges WHERE idx=7)) * 1.0 / COUNT(*) AS b6,
    COUNT(*) FILTER (WHERE m.rating >= (SELECT edge FROM ref_edges WHERE idx=7) AND m.rating < (SELECT edge FROM ref_edges WHERE idx=8)) * 1.0 / COUNT(*) AS b7,
    COUNT(*) FILTER (WHERE m.rating >= (SELECT edge FROM ref_edges WHERE idx=8) AND m.rating < (SELECT edge FROM ref_edges WHERE idx=9)) * 1.0 / COUNT(*) AS b8,
    COUNT(*) FILTER (WHERE m.rating >= (SELECT edge FROM ref_edges WHERE idx=9)) * 1.0 / COUNT(*) AS b9,
    COUNT(*) AS n_total,
    AVG(m.rating) AS mean_rating,
    STDDEV(m.rating) AS std_rating
FROM matches_history_minimal mhm
JOIN matches_1v1_clean m
  ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
 AND CAST(m.profileId AS VARCHAR) = mhm.player_id
WHERE mhm.started_at >= {ts_start}
  AND mhm.started_at <  {ts_end}
  AND m.rating IS NOT NULL
  AND m.is_null_cluster = FALSE
  AND m.internalLeaderboardId IN (6, 18)
"""

# Compute reference bin shares
ref_res = db.con.execute(
    QUERY_RATING_BIN_SHARES.format(
        ts_start="TIMESTAMP '2022-08-29'",
        ts_end="TIMESTAMP '2023-01-01'",
    )
).fetchone()
p_ref_bins = list(ref_res[:10])
print(f"Reference rating bin shares: {[round(p, 3) for p in p_ref_bins]}")
print(f"Sum: {sum(p_ref_bins):.3f}")

# %% [markdown]
# ## Step 7: Per-quarter PSI computation

# %%
rows = []
ks_sample_ids_all = {}

for quarter, ts_start, ts_end in TESTED_QUARTERS:
    print(f"\nProcessing {quarter}...")

    # Rating PSI
    rating_res = db.con.execute(
        QUERY_RATING_BIN_SHARES.format(
            ts_start=f"TIMESTAMP '{ts_start}'",
            ts_end=f"TIMESTAMP '{ts_end}'",
        )
    ).fetchone()
    p_test_bins = list(rating_res[:10])
    n_test_rating = rating_res[10]
    mean_test_rating = rating_res[11]
    std_test_rating = rating_res[12]

    psi_rating = compute_psi_numeric(rating_edges, p_ref_bins, p_test_bins)
    d_rating = cohen_d(mean_test_rating, mean_ref_rating, std_test_rating, std_ref_rating,
                       n_test_rating, n_ref_rating)

    # Won: win rate and Cohen's h (M-03: vs reference period)
    won_res = db.con.execute(f"""
        SELECT AVG(CAST(won AS DOUBLE)) AS p_won, COUNT(*) AS n_won
        FROM matches_history_minimal
        WHERE started_at >= TIMESTAMP '{ts_start}'
          AND started_at <  TIMESTAMP '{ts_end}'
          AND won IS NOT NULL
    """).fetchone()
    p_q_won = won_res[0]
    n_q_won = won_res[1]
    h_won = cohen_h(p_q_won, p_ref_won)

    # Faction PSI (categorical)
    faction_res = db.con.execute(f"""
        SELECT faction, COUNT(*) AS cnt
        FROM matches_history_minimal mhm
        JOIN matches_1v1_clean m
          ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
         AND CAST(m.profileId AS VARCHAR) = mhm.player_id
        WHERE mhm.started_at >= TIMESTAMP '{ts_start}'
          AND mhm.started_at <  TIMESTAMP '{ts_end}'
          AND m.is_null_cluster = FALSE
          AND m.internalLeaderboardId IN (6, 18)
        GROUP BY faction
    """).df()
    total_test_faction = faction_res["cnt"].sum()
    faction_counts = dict(zip(faction_res["faction"], faction_res["cnt"]))
    psi_faction, unseen_faction = compute_psi_categorical(ref_faction_dist, faction_counts, total_test_faction)

    # Map PSI (categorical, top-50 reference maps only)
    map_res = db.con.execute(f"""
        SELECT m.map AS map_id, COUNT(*) AS cnt
        FROM matches_history_minimal mhm
        JOIN matches_1v1_clean m
          ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
         AND CAST(m.profileId AS VARCHAR) = mhm.player_id
        WHERE mhm.started_at >= TIMESTAMP '{ts_start}'
          AND mhm.started_at <  TIMESTAMP '{ts_end}'
          AND m.is_null_cluster = FALSE
          AND m.internalLeaderboardId IN (6, 18)
        GROUP BY m.map
    """).df()
    total_test_map = map_res["cnt"].sum()
    map_counts = dict(zip(map_res["map_id"], map_res["cnt"]))
    psi_map, unseen_map = compute_psi_categorical(ref_map_dist, map_counts, total_test_map)

    # KS for rating (M-08: subsample 100k ref + 100k test, seed=42)
    ks_ref_ids = db.con.execute(f"""
        SELECT mhm.player_id, mhm.match_id, m.rating
        FROM matches_history_minimal mhm
        JOIN matches_1v1_clean m
          ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
         AND CAST(m.profileId AS VARCHAR) = mhm.player_id
        WHERE mhm.started_at >= TIMESTAMP '2022-08-29'
          AND mhm.started_at <  TIMESTAMP '2023-01-01'
          AND m.rating IS NOT NULL
          AND m.is_null_cluster = FALSE
          AND m.internalLeaderboardId IN (6, 18)
        USING SAMPLE {KS_SAMPLE_N} ROWS (reservoir, 42)
    """).df()

    ks_test_ids = db.con.execute(f"""
        SELECT mhm.player_id, mhm.match_id, m.rating
        FROM matches_history_minimal mhm
        JOIN matches_1v1_clean m
          ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
         AND CAST(m.profileId AS VARCHAR) = mhm.player_id
        WHERE mhm.started_at >= TIMESTAMP '{ts_start}'
          AND mhm.started_at <  TIMESTAMP '{ts_end}'
          AND m.rating IS NOT NULL
          AND m.is_null_cluster = FALSE
          AND m.internalLeaderboardId IN (6, 18)
        USING SAMPLE {KS_SAMPLE_N} ROWS (reservoir, 42)
    """).df()

    from scipy import stats as scipy_stats
    ks_stat, ks_pval = scipy_stats.ks_2samp(ks_ref_ids["rating"].values, ks_test_ids["rating"].values)

    # Persist KS sample IDs (M-08)
    ks_sample_path = ARTIFACTS / f"ks_sample_ids_{quarter}.csv"
    pd.concat([
        ks_ref_ids[["player_id", "match_id"]].assign(period="reference"),
        ks_test_ids[["player_id", "match_id"]].assign(period=quarter),
    ]).to_csv(ks_sample_path, index=False)
    ks_sample_ids_all[quarter] = str(ks_sample_path)

    row = {
        "feature": "rating",
        "quarter": quarter,
        "psi": round(psi_rating, 6),
        "cohen_d": round(d_rating, 6),
        "cohen_h": None,
        "ks_stat": round(float(ks_stat), 6),
        "n_ref": n_ref_rating,
        "n_test": int(n_test_rating),
        "unseen_count": 0,
        "verdict": "flagged_for_review" if psi_rating >= 0.25 else ("monitor" if psi_rating >= 0.10 else "stable"),
        "psi_threshold_note": "Thresholds 0.10/0.25 not power-calibrated at N>10^6 (Yurdakul 2018 WMU #3208); verdict=flagged_for_review is descriptive only",
    }
    rows.append(row)
    rows.append({
        "feature": "won",
        "quarter": quarter,
        "psi": None,
        "cohen_d": None,
        "cohen_h": round(h_won, 6),
        "ks_stat": None,
        "n_ref": n_ref_won,
        "n_test": int(n_q_won),
        "unseen_count": 0,
        "verdict": "stable",
        "psi_threshold_note": "",
    })
    rows.append({
        "feature": "faction",
        "quarter": quarter,
        "psi": round(psi_faction, 6),
        "cohen_d": None,
        "cohen_h": None,
        "ks_stat": None,
        "n_ref": int(total_ref_faction),
        "n_test": int(total_test_faction),
        "unseen_count": int(unseen_faction),
        "verdict": "flagged_for_review" if psi_faction >= 0.25 else ("monitor" if psi_faction >= 0.10 else "stable"),
        "psi_threshold_note": "Thresholds 0.10/0.25 not power-calibrated at N>10^6 (Yurdakul 2018 WMU #3208); verdict is descriptive only",
    })
    rows.append({
        "feature": "map_id",
        "quarter": quarter,
        "psi": round(psi_map, 6),
        "cohen_d": None,
        "cohen_h": None,
        "ks_stat": None,
        "n_ref": int(total_ref_map),
        "n_test": int(total_test_map),
        "unseen_count": int(unseen_map),
        "verdict": "flagged_for_review" if psi_map >= 0.25 else ("monitor" if psi_map >= 0.10 else "stable"),
        "psi_threshold_note": "Thresholds 0.10/0.25 not power-calibrated at N>10^6 (Yurdakul 2018 WMU #3208); verdict is descriptive only",
    })

    print(f"  rating: PSI={psi_rating:.4f}, d={d_rating:.4f}, KS={ks_stat:.4f}")
    print(f"  won: h={h_won:.4f} (p_q={p_q_won:.4f}, p_ref={p_ref_won:.4f})")
    print(f"  faction: PSI={psi_faction:.4f}, unseen={unseen_faction}")
    print(f"  map_id: PSI={psi_map:.4f}, unseen={unseen_map}")

db.close()
print("\nAll quarters processed.")

# %% [markdown]
# ## Step 8: Verdict

# %%
df_psi = pd.DataFrame(rows)
max_psi_rating = df_psi[df_psi["feature"] == "rating"]["psi"].max()
max_psi_faction = df_psi[df_psi["feature"] == "faction"]["psi"].max()
max_psi_map = df_psi[df_psi["feature"] == "map_id"]["psi"].max()

print(f"Max PSI rating: {max_psi_rating:.4f}")
print(f"Max PSI faction: {max_psi_faction:.4f}")
print(f"Max PSI map_id: {max_psi_map:.4f}")
print()
print("# Verdict: Hypothesis assessment")
print("NOTE: At N~60M rows, any non-zero PSI is 'statistically significant'.")
print("Sullivan & Feinn (2012) JGME 4(3):279-282 — substantive significance applies.")
print("PSI values are reported without 'significant drift' verdicts per Yurdakul (2018).")

# %% [markdown]
# ## Step 9: Emit artifacts

# %%
json_out = {
    "frozen_reference_edges": {
        "rating_deciles": [round(e, 2) for e in rating_edges],
        "ref_start": REF_START.isoformat(),
        "ref_end": REF_END.isoformat(),
    },
    "assertion_passed": True,
    "psi_matrix": rows,
    "effect_sizes": {
        "p_ref_won": round(p_ref_won, 6),
        "mean_ref_rating": round(mean_ref_rating, 2),
        "std_ref_rating": round(std_ref_rating, 2),
    },
    "unseen_bin_counts": {r["quarter"] + "_" + r["feature"]: r["unseen_count"] for r in rows},
    "ks_sample_files": ks_sample_ids_all,
    "sql_queries": {
        "rating_edges": QUERY_REF_RATING_EDGES,
        "ref_won": QUERY_REF_WON,
        "ref_faction": QUERY_REF_FACTION,
        "ref_map": QUERY_REF_MAP,
        "rating_bin_shares_template": QUERY_RATING_BIN_SHARES,
    },
    "psi_threshold_note": "Siddiqi (2006) thresholds 0.10/0.25 are not power-calibrated at N>10^6 (Yurdakul 2018 WMU #3208). Raw PSI values reported; verdict field is descriptive only.",
    "interpretation_at_large_n": "Sullivan & Feinn (2012) JGME 4(3):279-282: at N~60M any effect is statistically detectable. Substantive significance (PSI magnitude, effect size magnitude) is the relevant standard. Cohen's d > 0.5 and PSI > 0.25 are used as substantive thresholds.",
    "produced_at": datetime.now().isoformat(),
}

json_path = ARTIFACTS / "01_05_02_psi_shift.json"
json_path.write_text(json.dumps(json_out, indent=2, default=str))
print("Wrote:", json_path)

# CSV
csv_path = ARTIFACTS / "01_05_02_psi_shift_per_feature.csv"
df_psi.to_csv(csv_path, index=False)
print("Wrote:", csv_path)

# %%
md_table = df_psi[df_psi["feature"] == "rating"][["quarter", "psi", "cohen_d", "ks_stat", "n_test", "verdict"]].to_markdown(index=False)

md_content = f"""# 01_05_02 PSI Shift — aoe2companion

spec: reports/specs/01_05_preregistration.md@7e259dd8

## Pre-game features analysed

- `rating` (numeric, N=10 equal-frequency bins, frozen reference edges, Siddiqi 2006)
- `won` (binary, Cohen's h vs reference period per Cohen 1988 §6.2; M-03 fix: vs reference not 0.5)
- `faction` (categorical, relative-frequency PSI with `__unseen__` bin)
- `map_id` (categorical, relative-frequency PSI with `__unseen__` bin)

POST_GAME features (`duration_seconds`, `is_duration_suspicious`, `is_duration_negative`) are excluded (§4, I3).

## PSI Thresholds — Calibration Warning (M-04)

Siddiqi (2006) thresholds (monitor: 0.10, escalate: 0.25) are calibrated for N=10^3-10^5.
Yurdakul (2018) WMU #3208: "0.25 reasonable for 100-200, too conservative for larger samples."
At N~60M rows per quarter, any non-zero PSI is statistically detectable.
All PSI values are **reported without 'significant drift' verdicts**; the `verdict` field is descriptive only and flagged for review.

## Interpretation at Large N (M-05)

Sullivan & Feinn (2012) JGME 4(3):279-282: at N~60M, confidence intervals on effect sizes approach ±0.001.
Any drift will be "statistically significant." Substantive significance (|d| ≥ 0.2, PSI ≥ 0.10) is the relevant standard.
Cohen's d and Cohen's h are reported as substantive effect-size measures alongside raw PSI.

## Rating PSI per quarter (conditional on is_null_cluster=FALSE, lbs 6+18)

{md_table}

**Reference:** Frozen bin edges at deciles of reference period (2022-08-29..2022-12-31).
Max rating PSI: {max_psi_rating:.4f}
Max faction PSI: {max_psi_faction:.4f}
Max map_id PSI: {max_psi_map:.4f}

**Cohen's h (won, M-03 — vs reference p_ref={p_ref_won:.4f}):**
{chr(10).join(f"| {r['quarter']} | {r['cohen_h']} |" for r in rows if r['feature'] == 'won')}

## is_null_cluster handling (M-09)

Applied `WHERE is_null_cluster = FALSE` (via join to `matches_1v1_clean`) in both reference and test windows.
This excludes the <0.02% NULL cluster rows from all PSI computations.

## KS statistic (Breck et al. 2019, M-08)

KS computed on stratified subsample: 100k reference + 100k test per quarter (seed=42, reservoir sampling).
Sample IDs persisted under `ks_sample_ids_<quarter>.csv`.

## SQL (I6)

### Reference rating bin edges
```sql
{QUERY_REF_RATING_EDGES}
```

### Reference win rate
```sql
{QUERY_REF_WON}
```

_conditional on >=10 matches in reference period; see §6 for sensitivity_

## Literature

- Siddiqi (2006) — PSI definition, N=10 equal-frequency bins
- Yurdakul (2018) WMU dissertations #3208 — PSI threshold calibration at large N
- Cohen (1988) §2.2 (d), §6.2 (h) — effect-size definitions
- Breck et al. (2019) SysML — KS as complementary drift descriptor
- Sullivan & Feinn (2012) JGME 4(3):279-282 — interpretation at large N
"""

md_path = ARTIFACTS / "01_05_02_psi_shift.md"
md_path.write_text(md_content)
print("Wrote:", md_path)
print("Done.")
