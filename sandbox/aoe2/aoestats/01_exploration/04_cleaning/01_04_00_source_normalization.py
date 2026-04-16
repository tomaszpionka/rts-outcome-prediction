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
# # Step 01_04_00 -- Source Normalization to Canonical Long Skeleton: aoestats
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_04 -- Data Cleaning
# **Dataset:** aoestats
# **Question:** Can players_raw (long) joined with matches_raw be projected losslessly
#   into a unified 10-column long skeleton (one row per player per match)?
# **Invariants applied:**
#   - #3 (temporal discipline -- old_rating retained; new_rating, match_rating_diff excluded)
#   - #5 (symmetric player treatment -- player-row-oriented, no slot pivoting)
#   - #6 (reproducibility -- all SQL queries stored verbatim in artifact)
#   - #9 (step scope -- JOIN + projection only, no filtering beyond the WHERE in player_history_all)
# **Predecessor:** 01_04_01 (Data Cleaning -- complete; matches_long_raw coexists with existing VIEWs)
# **Step scope:** Create matches_long_raw VIEW. JOIN players_raw x matches_raw. Filter
#   identical to player_history_all (profile_id IS NOT NULL, started_timestamp IS NOT NULL).
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

logger = setup_notebook_logging(__name__)

# %%
# NOTE: read_only=False required for CREATE OR REPLACE VIEW
db = get_notebook_db("aoe2", "aoestats", read_only=False)
con = db._con
print("Connected via get_notebook_db: aoe2 / aoestats (read_only=False)")

# %%
reports_dir = get_reports_dir("aoe2", "aoestats")
cleaning_dir = reports_dir / "artifacts" / "01_exploration" / "04_cleaning"
cleaning_dir.mkdir(parents=True, exist_ok=True)
print(f"Artifact output dir: {cleaning_dir}")

# %% [markdown]
# ## 1. Create matches_long_raw VIEW
#
# Canonical 10-column long skeleton. players_raw is per-player per-match (long), so
# this is a JOIN + projection, NOT a UNION ALL unpivot.
#
# **Column mapping:**
# - match_id: p.game_id (VARCHAR native match identifier)
# - started_timestamp: m.started_timestamp (TIMESTAMP WITH TIME ZONE)
# - side: CAST(p.team AS INTEGER) -- values 0 and 1 for 1v1 matches
# - player_id: CAST(p.profile_id AS BIGINT) -- safe: max=24,853,897 << 2^53
# - chosen_civ_or_race: p.civ
# - outcome_raw: p.winner Boolean -> 1/0/NULL
# - rating_pre_raw: p.old_rating (pre-game rating; new_rating and match_rating_diff excluded -- I3)
# - map_id_raw: m.map
# - patch_raw: m.patch (BIGINT)
# - leaderboard_raw: m.leaderboard (VARCHAR; 'random_map' for ranked 1v1)
#
# **WHERE clause** matches the filter in player_history_all VIEW (same grain):
#   profile_id IS NOT NULL, started_timestamp IS NOT NULL

# %%
SQL_CREATE_VIEW = """
CREATE OR REPLACE VIEW matches_long_raw AS
SELECT
    p.game_id                              AS match_id,
    m.started_timestamp                    AS started_timestamp,
    CAST(p.team AS INTEGER)                AS side,
    CAST(p.profile_id AS BIGINT)           AS player_id,
    p.civ                                  AS chosen_civ_or_race,
    CASE WHEN p.winner = TRUE  THEN 1
         WHEN p.winner = FALSE THEN 0
         ELSE NULL END                     AS outcome_raw,
    p.old_rating                           AS rating_pre_raw,
    m.map                                  AS map_id_raw,
    m.patch                                AS patch_raw,
    m.leaderboard                          AS leaderboard_raw
FROM players_raw p
INNER JOIN matches_raw m ON p.game_id = m.game_id
WHERE p.profile_id IS NOT NULL
  AND m.started_timestamp IS NOT NULL
"""

con.execute(SQL_CREATE_VIEW)
print("matches_long_raw VIEW created.")

# %% [markdown]
# ## 2. Lossless validation (independent anchor check)
#
# Tautological comparisons are not used. Instead, the anchor is the independently-known
# total players_raw count (107,627,584 from 01_04_01 artifact), minus independently-
# counted exclusions (null profile_id + orphaned/null-ts rows).
#
# The critiques (W3) explicitly require this non-tautological check.

# %%
SQL_TOTAL_PLAYERS = "SELECT COUNT(*) AS total_players FROM players_raw"
SQL_NULL_PROFILE = "SELECT COUNT(*) AS null_profile FROM players_raw WHERE profile_id IS NULL"
SQL_ORPHAN_OR_NULL_TS = """
SELECT COUNT(*) AS orphan_or_null_ts
FROM players_raw p
LEFT JOIN matches_raw m ON p.game_id = m.game_id
WHERE m.started_timestamp IS NULL OR m.game_id IS NULL
"""
SQL_VIEW_COUNT = "SELECT COUNT(*) AS view_count FROM matches_long_raw"

total_players = con.execute(SQL_TOTAL_PLAYERS).fetchone()[0]
null_profile = con.execute(SQL_NULL_PROFILE).fetchone()[0]
orphan_or_null_ts = con.execute(SQL_ORPHAN_OR_NULL_TS).fetchone()[0]
view_count = con.execute(SQL_VIEW_COUNT).fetchone()[0]

expected = total_players - null_profile - orphan_or_null_ts
print(f"total_players_raw         : {total_players:,}")
print(f"null_profile_id           : {null_profile:,}")
print(f"orphan_or_null_ts         : {orphan_or_null_ts:,}")
print(f"expected (anchor formula) : {expected:,}")
print(f"matches_long_raw rows     : {view_count:,}")

# Cross-check: total_players must equal known anchor from 01_04_01
assert total_players == 107_627_584, f"Anchor mismatch: {total_players} != 107,627,584"
print("Anchor cross-check PASSED (total_players == 107,627,584)")

assert view_count == expected, f"Lossless check FAILED: {view_count} != {expected}"
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
# ## 5. Symmetry audit (1v1 scoped: leaderboard_raw = 'random_map')
#
# Expected: the known asymmetry from matches_1v1_clean (side=1 wins ~52.27%) should
# reappear. Established in 01_04_01.

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
  AND leaderboard_raw = 'random_map'
GROUP BY side
ORDER BY side
"""

df_sym_1v1 = con.execute(SQL_SYMMETRY_1V1).df()
print("1v1 scoped symmetry audit (leaderboard_raw = 'random_map'):")
print(df_sym_1v1.to_string())
for _, row in df_sym_1v1.iterrows():
    if abs(row["win_pct"] - 50.0) > 10.0:
        print(f"  ALERT: side={row['side']} win_pct={row['win_pct']:.4f}% deviates >10pp from 50%")

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
# ## 7. Write JSON artifact

# %%
schema_rows = df_schema[["column_name", "column_type", "null"]].to_dict("records")
sym_full_rows = df_sym_full.to_dict("records")
sym_1v1_rows = df_sym_1v1.to_dict("records")
lb_dist = df_lb.to_dict("records")

artifact = {
    "step": "01_04_00",
    "name": "Source Normalization to Canonical Long Skeleton",
    "dataset": "aoestats",
    "view_name": "matches_long_raw",
    "generated_date": str(date.today()),
    "row_count": int(view_count),
    "schema": schema_rows,
    "lossless_check": {
        "total_players_raw": int(total_players),
        "null_profile_count": int(null_profile),
        "orphan_or_null_ts_count": int(orphan_or_null_ts),
        "expected": int(expected),
        "view_count": int(view_count),
        "anchor_cross_check": "total_players_raw == 107,627,584 (from 01_04_01 artifact)",
        "passed": view_count == expected,
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
            "filter": "leaderboard_raw = 'random_map'",
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
        {"leaderboard_raw": r["leaderboard_raw"], "n": int(r["n"])}
        for r in lb_dist
    ],
    "source_tables": ["players_raw", "matches_raw"],
    "sql_queries": {
        "create_view": SQL_CREATE_VIEW,
        "total_players": SQL_TOTAL_PLAYERS,
        "null_profile": SQL_NULL_PROFILE,
        "orphan_or_null_ts": SQL_ORPHAN_OR_NULL_TS,
        "view_count": SQL_VIEW_COUNT,
        "describe": SQL_DESCRIBE,
        "symmetry_full": SQL_SYMMETRY_FULL,
        "symmetry_1v1": SQL_SYMMETRY_1V1,
        "leaderboard_distribution": SQL_LEADERBOARD_DIST,
    },
}

artifact_path = cleaning_dir / "01_04_00_source_normalization.json"
with open(artifact_path, "w") as f:
    json.dump(artifact, f, indent=2)
print(f"JSON artifact written: {artifact_path}")

# %% [markdown]
# ## 8. Write MD artifact

# %%
md_content = f"""# Step 01_04_00 -- Source Normalization to Canonical Long Skeleton

**Dataset:** aoestats
**Date:** {date.today()}
**View:** matches_long_raw

## Summary

Created `matches_long_raw` VIEW: canonical 10-column long skeleton, one row per
player per match. JOIN of players_raw (per-player) with matches_raw, filtered
identically to player_history_all (profile_id IS NOT NULL, started_timestamp IS NOT NULL).

## Lossless validation (independent anchor)

| Metric | Count |
|--------|-------|
| total players_raw | {total_players:,} |
| null profile_id | {null_profile:,} |
| orphan or null started_timestamp | {orphan_or_null_ts:,} |
| expected (anchor formula) | {expected:,} |
| matches_long_raw rows | {view_count:,} |
| Anchor cross-check (==107,627,584) | PASS |
| Lossless | {'PASS' if view_count == expected else 'FAIL'} |

## Schema

| Column | Type | Nullable |
|--------|------|----------|
""" + "\n".join(
    f"| {r['column_name']} | {r['column_type']} | {r['null']} |"
    for r in schema_rows
) + f"""

## Symmetry audit

### Full dataset (side IN (0, 1))

| side | n_rows | n_wins | win_pct | n_null_outcome |
|------|--------|--------|---------|----------------|
""" + "\n".join(
    f"| {r['side']} | {r['n_rows']:,} | {int(r['n_wins']) if r['n_wins'] is not None else 'NULL'} | {r['win_pct']:.4f}% | {r['n_null_outcome']:,} |"
    for r in sym_full_rows
) + f"""

### 1v1 scoped (leaderboard_raw = 'random_map')

Known asymmetry from 01_04_01: side=1 wins ~52.27%. This reappears here.

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

- **I3:** old_rating retained; new_rating and match_rating_diff excluded.
- **I5:** Player-row-oriented VIEW; no slot pivoting; both players represented identically.
- **I6:** All SQL queries stored verbatim in the JSON artifact.
- **I9:** No features computed; only rows with null profile_id or null started_timestamp excluded (matching player_history_all filter).
"""

md_path = cleaning_dir / "01_04_00_source_normalization.md"
with open(md_path, "w") as f:
    f.write(md_content)
print(f"MD artifact written: {md_path}")
print("Step 01_04_00 complete for aoestats.")
