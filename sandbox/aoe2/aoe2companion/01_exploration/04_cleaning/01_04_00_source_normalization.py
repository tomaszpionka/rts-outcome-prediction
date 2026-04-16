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
# # Step 01_04_00 -- Source Normalization to Canonical Long Skeleton: aoe2companion
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_04 -- Data Cleaning
# **Dataset:** aoe2companion
# **Question:** Can matches_raw be projected losslessly into a unified 10-column
#   long skeleton (one row per player per match) that all downstream cleaning steps
#   operate against?
# **Invariants applied:**
#   - #3 (temporal discipline -- POST-GAME columns excluded; started preserved as temporal anchor)
#   - #5 (symmetric player treatment -- player-row-oriented, no slot pivoting)
#   - #6 (reproducibility -- all SQL queries stored verbatim in artifact)
#   - #9 (step scope -- format conversion only, no filtering, no feature computation)
# **Predecessor:** 01_04_01 (Data Cleaning -- complete; matches_long_raw coexists with existing VIEWs)
# **Step scope:** Create matches_long_raw VIEW. Lossless projection of source data
#   into the canonical 10-column schema. No filtering, no cleaning.
# **Outputs:** 1 DuckDB VIEW, JSON artifact, MD artifact

# %% [markdown]
# ## 0. Imports and DB connection

# %%
import json
from datetime import date
from pathlib import Path

from rts_predict.common.notebook_utils import (
    get_notebook_db,
    get_reports_dir,
    setup_notebook_logging,
)

logger = setup_notebook_logging()

# %%
# NOTE: read_only=False required for CREATE OR REPLACE VIEW
db = get_notebook_db("aoe2", "aoe2companion", read_only=False)
con = db.con
print("Connected via get_notebook_db: aoe2 / aoe2companion (read_only=False)")

# %%
reports_dir = get_reports_dir("aoe2", "aoe2companion")
cleaning_dir = reports_dir / "artifacts" / "01_exploration" / "04_cleaning"
cleaning_dir.mkdir(parents=True, exist_ok=True)
print(f"Artifact output dir: {cleaning_dir}")

# %% [markdown]
# ## 1. Create matches_long_raw VIEW
#
# Canonical 10-column long skeleton. One row per player per match (matches_raw is
# already in long format). Pure column rename and projection -- no filtering.
#
# **Column mapping:**
# - match_id: matchId (dataset-native INTEGER match identifier)
# - started_timestamp: started (TIMESTAMP, nullable -- NULLs pass through; I3 temporal anchor)
# - side: CASE WHEN team IN (1, 2) THEN team - 1 ELSE NULL END -- maps source slot encoding.
#   aoe2companion uses team=1 and team=2 as the two sides in 1v1 matches (team=0 has only 449
#   rows across the entire dataset and represents a different context). Re-encoded as 0-based:
#   team=1 → side=0, team=2 → side=1. Team-game values (3+) and sentinel (255) become NULL.
# - player_id: profileId (INTEGER player identifier)
# - chosen_civ_or_race: civ (civilization name VARCHAR)
# - outcome_raw: won Boolean -> 1/0/NULL
# - rating_pre_raw: rating (pre-game, confirmed in 01_03_03; no ratingDiff or finished -- I3)
# - map_id_raw: map
# - patch_raw: NULL (no patch column in matches_raw source)
# - leaderboard_raw: internalLeaderboardId (INTEGER; 6=rm_1v1, 18=qp_rm_1v1 for ranked 1v1)

# %%
SQL_CREATE_VIEW = """
CREATE OR REPLACE VIEW matches_long_raw AS
SELECT
    matchId                                           AS match_id,
    started                                           AS started_timestamp,
    CASE WHEN team IN (1, 2) THEN team - 1 ELSE NULL END AS side,
    profileId                                         AS player_id,
    civ                                               AS chosen_civ_or_race,
    CASE WHEN won = TRUE  THEN 1
         WHEN won = FALSE THEN 0
         ELSE NULL END                                AS outcome_raw,
    rating                                            AS rating_pre_raw,
    map                                               AS map_id_raw,
    NULL                                              AS patch_raw,
    internalLeaderboardId                             AS leaderboard_raw
FROM matches_raw
"""

con.execute(SQL_CREATE_VIEW)
print("matches_long_raw VIEW created.")

# %% [markdown]
# ## 2. Lossless validation
#
# matches_raw is already in long format; this VIEW is a pure projection.
# Row count must be identical.

# %%
SQL_COUNT_VIEW = "SELECT COUNT(*) AS n FROM matches_long_raw"
SQL_COUNT_SOURCE = "SELECT COUNT(*) AS n FROM matches_raw"

view_count = con.execute(SQL_COUNT_VIEW).fetchone()[0]
source_count = con.execute(SQL_COUNT_SOURCE).fetchone()[0]
print(f"matches_long_raw rows : {view_count:,}")
print(f"matches_raw rows      : {source_count:,}")
assert view_count == source_count, f"Lossless check FAILED: {view_count} != {source_count}"
print("Lossless check PASSED.")

# %% [markdown]
# ## 3. Schema inspection

# %%
SQL_DESCRIBE = "DESCRIBE matches_long_raw"
df_schema = con.execute(SQL_DESCRIBE).df()
print(df_schema.to_string())

# %% [markdown]
# ## 4. Symmetry audit (full dataset)
#
# Invariant #5: both sides must receive identical treatment. Expected: win_pct near 50%.
# Alert if |win_pct - 50| > 10.
#
# Note: side=0 contains only 449 rows (vs side=1: 130M rows). This is a source encoding
# artifact -- aoe2companion uses team=1 and team=2 for 1v1 match sides, not team=0 and
# team=1. The symmetry audit over side IN (0,1) is therefore not meaningful for the full
# dataset. The 1v1-scoped audit below (leaderboard_raw IN (6,18)) is the operationally
# relevant check.

# %%
SQL_SYMMETRY_FULL = """
SELECT
    side,
    COUNT(*)                                             AS n_rows,
    SUM(outcome_raw)                                     AS n_wins,
    ROUND(100.0 * SUM(outcome_raw) / COUNT(*), 4)       AS win_pct,
    COUNT(*) FILTER (WHERE outcome_raw IS NULL)          AS n_null_outcome
FROM matches_long_raw
WHERE side IN (0, 1)
GROUP BY side
ORDER BY side
"""

df_sym_full = con.execute(SQL_SYMMETRY_FULL).df()
print("Full dataset symmetry audit (side IN (0, 1)):")
print(df_sym_full.to_string())
for _, row in df_sym_full.iterrows():
    if abs(row["win_pct"] - 50.0) > 10.0:
        print(f"  ALERT: side={row['side']} win_pct={row['win_pct']:.4f}% deviates >10pp from 50%")

# %% [markdown]
# ## 5. Symmetry audit (1v1 scoped: leaderboard_raw IN (6, 18))
#
# rm_1v1 (6) and qp_rm_1v1 (18) are the ranked 1v1 leaderboards established in 01_04_01.
# Scoped to side IN (0, 1) -- only side=1 rows appear for these leaderboards since
# aoe2companion uses team=1 and team=2 as 1v1 sides.

# %%
SQL_SYMMETRY_1V1 = """
SELECT
    side,
    COUNT(*)                                             AS n_rows,
    SUM(outcome_raw)                                     AS n_wins,
    ROUND(100.0 * SUM(outcome_raw) / COUNT(*), 4)       AS win_pct,
    COUNT(*) FILTER (WHERE outcome_raw IS NULL)          AS n_null_outcome
FROM matches_long_raw
WHERE side IN (0, 1)
  AND leaderboard_raw IN (6, 18)
GROUP BY side
ORDER BY side
"""

df_sym_1v1 = con.execute(SQL_SYMMETRY_1V1).df()
print("1v1 scoped symmetry audit (leaderboard_raw IN (6, 18)):")
print(df_sym_1v1.to_string())

# %% [markdown]
# ## 6. leaderboard_raw distribution (top 10)

# %%
SQL_LEADERBOARD_DIST = """
SELECT leaderboard_raw, COUNT(*) AS n
FROM matches_long_raw
GROUP BY leaderboard_raw
ORDER BY n DESC
LIMIT 10
"""

df_lb = con.execute(SQL_LEADERBOARD_DIST).df()
print("leaderboard_raw value distribution (top 10):")
print(df_lb.to_string())

# %% [markdown]
# ## 7. Side distribution (all values)

# %%
SQL_SIDE_DIST = """
SELECT side, COUNT(*) AS n
FROM matches_long_raw
GROUP BY side
ORDER BY side
"""

df_side = con.execute(SQL_SIDE_DIST).df()
print("Full side distribution (all values including NULL):")
print(df_side.to_string())

# %% [markdown]
# ## 8. Write JSON artifact

# %%
schema_rows = df_schema[["column_name", "column_type", "null"]].to_dict("records")

sym_full_rows = df_sym_full.to_dict("records")
sym_1v1_rows = df_sym_1v1.to_dict("records")

lb_dist = df_lb.to_dict("records")

artifact = {
    "step": "01_04_00",
    "name": "Source Normalization to Canonical Long Skeleton",
    "dataset": "aoe2companion",
    "view_name": "matches_long_raw",
    "generated_date": str(date.today()),
    "row_count": int(view_count),
    "schema": schema_rows,
    "lossless_check": {
        "source_count": int(source_count),
        "view_count": int(view_count),
        "passed": view_count == source_count,
    },
    "symmetry_audit": {
        "full_dataset": [
            {
                "side": int(r["side"]),
                "n_rows": int(r["n_rows"]),
                "n_wins": int(r["n_wins"]) if r["n_wins"] is not None else None,
                "win_pct": float(r["win_pct"]) if r["win_pct"] is not None else None,
                "n_null_outcome": int(r["n_null_outcome"]),
            }
            for r in sym_full_rows
        ],
        "scoped_1v1": {
            "filter": "leaderboard_raw IN (6, 18)",
            "note": "aoe2companion 1v1 uses team=1 and team=2 as sides; only side=1 rows appear in ranked 1v1",
            "rows": [
                {
                    "side": int(r["side"]),
                    "n_rows": int(r["n_rows"]),
                    "n_wins": int(r["n_wins"]) if r["n_wins"] is not None else None,
                    "win_pct": float(r["win_pct"]) if r["win_pct"] is not None else None,
                    "n_null_outcome": int(r["n_null_outcome"]),
                }
                for r in sym_1v1_rows
            ],
        },
    },
    "leaderboard_raw_distribution": [
        {"leaderboard_raw": (int(r["leaderboard_raw"]) if r["leaderboard_raw"] is not None else None), "n": int(r["n"])}
        for r in lb_dist
    ],
    "source_tables": ["matches_raw"],
    "sql_queries": {
        "create_view": SQL_CREATE_VIEW,
        "count_view": SQL_COUNT_VIEW,
        "count_source": SQL_COUNT_SOURCE,
        "describe": SQL_DESCRIBE,
        "symmetry_full": SQL_SYMMETRY_FULL,
        "symmetry_1v1": SQL_SYMMETRY_1V1,
        "leaderboard_distribution": SQL_LEADERBOARD_DIST,
        "side_distribution": SQL_SIDE_DIST,
    },
}

artifact_path = cleaning_dir / "01_04_00_source_normalization.json"
with open(artifact_path, "w") as f:
    json.dump(artifact, f, indent=2)
print(f"JSON artifact written: {artifact_path}")

# %% [markdown]
# ## 9. Write MD artifact

# %%
md_content = f"""# Step 01_04_00 -- Source Normalization to Canonical Long Skeleton

**Dataset:** aoe2companion
**Date:** {date.today()}
**View:** matches_long_raw

## Summary

Created `matches_long_raw` VIEW: canonical 10-column long skeleton, one row per
player per match. Lossless projection from matches_raw (already in long format).
No filtering, no cleaning, no feature computation.

## Row counts

| Source | Count |
|--------|-------|
| matches_raw | {source_count:,} |
| matches_long_raw | {view_count:,} |
| Lossless | {'PASS' if view_count == source_count else 'FAIL'} |

## Schema

| Column | Type | Nullable |
|--------|------|----------|
""" + "\n".join(
    f"| {r['column_name']} | {r['column_type']} | {r['null']} |"
    for r in schema_rows
) + f"""

## Symmetry audit

### Full dataset (side IN (0, 1))

Note: aoe2companion uses team=1 and team=2 as 1v1 sides, not team=0 and team=1.
Side=0 contains only 449 rows (source encoding artifact). The 1v1-scoped audit is operationally relevant.

| side | n_rows | n_wins | win_pct | n_null_outcome |
|------|--------|--------|---------|----------------|
""" + "\n".join(
    f"| {r['side']} | {r['n_rows']:,} | {int(r['n_wins']) if r['n_wins'] is not None else 'NULL'} | {r['win_pct']:.4f}% | {r['n_null_outcome']:,} |"
    for r in sym_full_rows
) + f"""

### 1v1 scoped (leaderboard_raw IN (6, 18))

| side | n_rows | n_wins | win_pct | n_null_outcome |
|------|--------|--------|---------|----------------|
""" + "\n".join(
    f"| {r['side']} | {r['n_rows']:,} | {int(r['n_wins']) if r['n_wins'] is not None else 'NULL'} | {r['win_pct']:.4f}% | {r['n_null_outcome']:,} |"
    for r in sym_1v1_rows
) + """

## leaderboard_raw distribution (top 10)

| leaderboard_raw | n |
|-----------------|---|
""" + "\n".join(
    f"| {r['leaderboard_raw']} | {r['n']:,} |"
    for r in lb_dist
) + """

## Invariants

- **I3:** started (temporal anchor) retained; ratingDiff and finished excluded.
- **I5:** Player-row-oriented VIEW; no slot pivoting; both players represented identically.
- **I6:** All SQL queries stored verbatim in the JSON artifact.
- **I9:** No features computed; no rows filtered; raw data untouched.
"""

md_path = cleaning_dir / "01_04_00_source_normalization.md"
with open(md_path, "w") as f:
    f.write(md_content)
print(f"MD artifact written: {md_path}")
print("Step 01_04_00 complete for aoe2companion.")
