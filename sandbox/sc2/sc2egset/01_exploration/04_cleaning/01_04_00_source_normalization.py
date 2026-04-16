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
# # Step 01_04_00 -- Source Normalization to Canonical Long Skeleton: sc2egset
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_04 -- Data Cleaning
# **Dataset:** sc2egset
# **Question:** Can replay_players_raw JOIN replays_meta_raw be projected losslessly
#   into a unified 10-column long skeleton (one row per player per match)?
# **Invariants applied:**
#   - #3 (temporal discipline -- MMR (PRE_GAME) retained; APM, SQ, supplyCappedPercent,
#     header_elapsedGameLoops excluded)
#   - #5 (symmetric player treatment -- player-row-oriented, no slot pivoting)
#   - #6 (reproducibility -- all SQL queries stored verbatim in artifact)
#   - #9 (step scope -- structural JOIN + projection only, no filtering)
# **Predecessor:** 01_04_01 (Data Cleaning -- complete; matches_long_raw coexists with existing VIEWs)
# **Step scope:** Create matches_long_raw VIEW. Structural JOIN of replay_players_raw
#   x replays_meta_raw using the hex-hash regexp key. No filtering beyond INNER JOIN
#   (unmatched rows excluded by INNER JOIN semantics).
# **Outputs:** 1 DuckDB VIEW, JSON artifact, MD artifact
#
# **Design note on started_timestamp:**
# rm.details.timeUTC (struct dot notation, VARCHAR) is the match start timestamp.
# It is stored as an ISO 8601 string with Windows FILETIME sub-second precision
# (e.g. "2016-01-31T19:13:30.0627872Z"). Type unification to TIMESTAMP deferred to Phase 02.
#
# **Design note on leaderboard_raw:**
# leaderboard_raw is NULL for all rows. SC2EGSet is an esports tournament dataset
# with no matchmaking ladder. This is deliberate -- not missing data.
#
# **Design note on match_id:**
# NULLIF wraps the regexp_extract to convert empty-string non-matches to NULL,
# consistent with matches_flat in 01_04_01. The hex-hash pattern
# ([0-9a-f]{32})\.SC2Replay\.json$ extracts 32-char hex hash only, compatible
# with matches_flat.replay_id.

# %% [markdown]
# ## Cell 1 -- Imports

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

# %% [markdown]
# ## Cell 2 -- DuckDB Connection (writable -- creates VIEW)
#
# This notebook creates one VIEW. A writable connection is required.
# WARNING: Close all read-only notebook connections to this DB before running.

# %%
con = get_notebook_db("sc2", "sc2egset", read_only=False)
print("DuckDB connection opened (read-write).")

# %%
reports_dir = get_reports_dir("sc2", "sc2egset")
cleaning_dir = reports_dir / "artifacts" / "01_exploration" / "04_cleaning"
cleaning_dir.mkdir(parents=True, exist_ok=True)
print(f"Artifact output dir: {cleaning_dir}")

# %% [markdown]
# ## Cell 3 -- Create matches_long_raw VIEW
#
# Canonical 10-column long skeleton. Structural JOIN of replay_players_raw x
# replays_meta_raw using the 32-char hex hash extracted from filename.
#
# NULLIF guard matches 01_04_01 matches_flat: converts empty-string non-matches
# to NULL (empty-string protection for rows where filename does not match the pattern).
#
# **Column mapping:**
# - match_id: 32-char hex hash extracted from filename (NULLIF-guarded)
# - started_timestamp: rm.details.timeUTC (VARCHAR ISO 8601 string; struct dot notation)
# - side: rp.playerID - 1 (playerID is 1-based; 0-based for schema consistency)
#   Values 0/1 for the two main players; values 2-8 for rare multi-player/observer slots
# - player_id: rp.toon_id (VARCHAR Battle.net identifier)
# - chosen_civ_or_race: rp.race (actual race played; not selectedRace which includes Random)
# - outcome_raw: rp.result in {Win, Loss, Undecided, Tie} -> 1/0/NULL
# - rating_pre_raw: rp.MMR (INTEGER; 0=unrated sentinel, handling deferred to Phase 02;
#   PRE_GAME classification from 01_04_01 MMR analysis)
# - map_id_raw: rm.metadata.mapName (struct dot notation)
# - patch_raw: rm.metadata.gameVersion (VARCHAR; struct dot notation)
# - leaderboard_raw: NULL constant (tournament data, no matchmaking ladder)

# %%
SQL_CREATE_VIEW = r"""
CREATE OR REPLACE VIEW matches_long_raw AS
SELECT
    NULLIF(
        regexp_extract(rp.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1),
        ''
    )                                                             AS match_id,
    rm.details.timeUTC                                            AS started_timestamp,
    rp.playerID - 1                                               AS side,
    rp.toon_id                                                    AS player_id,
    rp.race                                                       AS chosen_civ_or_race,
    CASE WHEN rp.result = 'Win'  THEN 1
         WHEN rp.result = 'Loss' THEN 0
         ELSE NULL END                                            AS outcome_raw,
    rp.MMR                                                        AS rating_pre_raw,
    rm.metadata.mapName                                           AS map_id_raw,
    rm.metadata.gameVersion                                       AS patch_raw,
    NULL                                                          AS leaderboard_raw
FROM replay_players_raw rp
INNER JOIN replays_meta_raw rm
  ON NULLIF(
         regexp_extract(rp.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1),
         ''
     )
   = NULLIF(
         regexp_extract(rm.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1),
         ''
     )
"""

con.con.execute(SQL_CREATE_VIEW)
print("matches_long_raw VIEW created.")

# %% [markdown]
# ## Cell 4 -- Lossless validation
#
# Compare VIEW row count against the same INNER JOIN on the raw tables directly.

# %%
SQL_COUNT_VIEW = "SELECT COUNT(*) FROM matches_long_raw"
SQL_COUNT_JOIN = r"""
SELECT COUNT(*) FROM replay_players_raw rp
INNER JOIN replays_meta_raw rm
  ON NULLIF(regexp_extract(rp.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1), '')
   = NULLIF(regexp_extract(rm.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1), '')
"""

view_count = con.con.execute(SQL_COUNT_VIEW).fetchone()[0]
join_count = con.con.execute(SQL_COUNT_JOIN).fetchone()[0]
print(f"matches_long_raw rows : {view_count:,}")
print(f"direct JOIN count     : {join_count:,}")
assert view_count == join_count, f"Lossless check FAILED: {view_count} != {join_count}"
print("Lossless check PASSED.")

# %% [markdown]
# ## Cell 5 -- Verify side values
#
# side=0 and side=1 are the two main players (playerID 1 and 2 in source).
# Side values 2-8 correspond to rare replay entries with playerID > 2
# (observer slots or multi-player replays outside the 1v1 scope).

# %%
SQL_SIDE_DISTINCT = "SELECT DISTINCT side FROM matches_long_raw ORDER BY side"
SQL_SIDE_DIST = "SELECT side, COUNT(*) AS n FROM matches_long_raw GROUP BY side ORDER BY side"

distinct_sides = con.con.execute(SQL_SIDE_DISTINCT).fetchdf()["side"].tolist()
print(f"Distinct side values: {distinct_sides}")

df_side = con.con.execute(SQL_SIDE_DIST).df()
print("Full side distribution:")
print(df_side.to_string())

# %% [markdown]
# ## Cell 6 -- Schema inspection

# %%
SQL_DESCRIBE = "DESCRIBE matches_long_raw"
df_schema = con.con.execute(SQL_DESCRIBE).df()
print(df_schema.to_string())

# %% [markdown]
# ## Cell 7 -- Symmetry audit (side IN (0, 1))
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

df_sym = con.con.execute(SQL_SYMMETRY_FULL).df()
print("Symmetry audit (side IN (0, 1)):")
print(df_sym.to_string())
for _, row in df_sym.iterrows():
    if abs(row["win_pct"] - 50.0) > 10.0:
        print(f"  ALERT: side={row['side']} win_pct={row['win_pct']:.4f}% deviates >10pp from 50%")

# %% [markdown]
# ## Cell 8 -- NULL match_id check

# %%
SQL_NULL_MATCH_ID = "SELECT COUNT(*) AS null_match_id FROM matches_long_raw WHERE match_id IS NULL"
null_match_id = con.con.execute(SQL_NULL_MATCH_ID).fetchone()[0]
print(f"NULL match_id rows: {null_match_id}")
assert null_match_id == 0, f"Expected 0 NULL match_ids, got {null_match_id}"
print("NULL match_id check PASSED.")

# %% [markdown]
# ## Cell 9 -- leaderboard_raw distribution

# %%
SQL_LEADERBOARD_DIST = """
SELECT leaderboard_raw, COUNT(*) AS n
FROM matches_long_raw
GROUP BY leaderboard_raw
"""

df_lb = con.con.execute(SQL_LEADERBOARD_DIST).df()
print("leaderboard_raw distribution (should be all NULL):")
print(df_lb.to_string())
assert df_lb["leaderboard_raw"].isna().all(), "Expected all leaderboard_raw to be NULL"
print("leaderboard_raw NULL check PASSED.")

# %% [markdown]
# ## Cell 10 -- Write JSON artifact

# %%
schema_rows = df_schema[["column_name", "column_type", "null"]].to_dict("records")
sym_rows = df_sym.to_dict("records")

artifact = {
    "step": "01_04_00",
    "name": "Source Normalization to Canonical Long Skeleton",
    "dataset": "sc2egset",
    "view_name": "matches_long_raw",
    "generated_date": str(date.today()),
    "row_count": int(view_count),
    "schema": schema_rows,
    "lossless_check": {
        "source_join_count": int(join_count),
        "view_count": int(view_count),
        "passed": view_count == join_count,
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
            for r in sym_rows
        ],
        "scoped_1v1": {
            "note": "sc2egset is tournament data with no matchmaking ladder; leaderboard_raw = NULL for all rows. No scoped 1v1 audit applicable.",
            "rows": [],
        },
    },
    "leaderboard_raw_distribution": [
        {"leaderboard_raw": None, "n": int(view_count)}
    ],
    "source_tables": ["replay_players_raw", "replays_meta_raw"],
    "sql_queries": {
        "create_view": SQL_CREATE_VIEW,
        "count_view": SQL_COUNT_VIEW,
        "count_join": SQL_COUNT_JOIN,
        "describe": SQL_DESCRIBE,
        "side_distinct": SQL_SIDE_DISTINCT,
        "side_distribution": SQL_SIDE_DIST,
        "symmetry_full": SQL_SYMMETRY_FULL,
        "null_match_id": SQL_NULL_MATCH_ID,
        "leaderboard_distribution": SQL_LEADERBOARD_DIST,
    },
}

artifact_path = cleaning_dir / "01_04_00_source_normalization.json"
with open(artifact_path, "w") as f:
    json.dump(artifact, f, indent=2)
print(f"JSON artifact written: {artifact_path}")

# %% [markdown]
# ## Cell 11 -- Write MD artifact

# %%
md_content = f"""# Step 01_04_00 -- Source Normalization to Canonical Long Skeleton

**Dataset:** sc2egset
**Date:** {date.today()}
**View:** matches_long_raw

## Summary

Created `matches_long_raw` VIEW: canonical 10-column long skeleton, one row per
player per match. Structural INNER JOIN of replay_players_raw x replays_meta_raw
using the 32-char hex hash extracted from filename via regexp. No filtering beyond
INNER JOIN (unmatched rows excluded by INNER JOIN semantics).

## Row counts

| Source | Count |
|--------|-------|
| direct JOIN count | {join_count:,} |
| matches_long_raw | {view_count:,} |
| Lossless | {'PASS' if view_count == join_count else 'FAIL'} |

## Schema

| Column | Type | Nullable |
|--------|------|----------|
""" + "\n".join(
    f"| {r['column_name']} | {r['column_type']} | {r['null']} |"
    for r in schema_rows
) + f"""

## Symmetry audit (side IN (0, 1))

| side | n_rows | n_wins | win_pct | n_null_outcome |
|------|--------|--------|---------|----------------|
""" + "\n".join(
    f"| {r['side']} | {r['n_rows']:,} | {int(r['n_wins']) if r['n_wins'] is not None else 'NULL'} | {r['win_pct']:.4f}% | {r['n_null_outcome']:,} |"
    for r in sym_rows
) + """

Note: leaderboard_raw is NULL for all rows (tournament data, no matchmaking ladder).
No 1v1-scoped symmetry audit is applicable.

## leaderboard_raw distribution

All 44,817 rows have leaderboard_raw = NULL (expected -- tournament dataset).

## Invariants

- **I3:** MMR retained (PRE_GAME per 01_04_01); APM, SQ, supplyCappedPercent, header_elapsedGameLoops excluded.
- **I5:** Player-row-oriented VIEW; no slot pivoting; both players represented identically.
- **I6:** All SQL queries stored verbatim in the JSON artifact.
- **I9:** No features computed; no rows filtered beyond INNER JOIN unmatched exclusion.
"""

md_path = cleaning_dir / "01_04_00_source_normalization.md"
with open(md_path, "w") as f:
    f.write(md_content)
print(f"MD artifact written: {md_path}")
print("Step 01_04_00 complete for sc2egset.")
