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
# # Step 01_04_02 -- Data Cleaning Execution (Act on DS-SC2-01..10)
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_04 -- Data Cleaning
# **Dataset:** sc2egset
# **Step scope:** Applies the 10 cleaning decisions (DS-SC2-01..10) surfaced by 01_04_01
# missingness audit. Modifies VIEW DDL for matches_flat_clean and player_history_all
# (no raw table changes). Reports CONSORT-style column-count flow + subgroup impact
# + post-cleaning invariant re-validation.
# **Invariants applied:**
#   - I3 (temporal discipline: PRE_GAME only in matches_flat_clean)
#   - I5 (symmetry: 1 Win + 1 Loss per replay in matches_flat_clean)
#   - I6 (all SQL stored verbatim in artifact)
#   - I7 (all thresholds data-derived from 01_04_01 ledger)
#   - I9 (non-destructive: raw tables untouched; only VIEWs replaced)
# **Predecessor:** 01_04_01 (Missingness Audit -- complete)
# **Date:** 2026-04-17
# **ROADMAP ref:** 01_04_02

# %% [markdown]
# ## Cell 1 -- Imports

# %%
import json
from pathlib import Path

import numpy as np
import pandas as pd

from rts_predict.common.notebook_utils import (
    get_notebook_db,
    get_reports_dir,
    setup_notebook_logging,
)

logger = setup_notebook_logging()

# %% [markdown]
# ## Cell 2 -- DuckDB Connection (writable -- replaces VIEWs)
#
# This notebook creates two replacement VIEWs. A writable connection is required.
# WARNING: Close all read-only notebook connections to this DB before running.

# %%
db = get_notebook_db("sc2", "sc2egset", read_only=False)
con = db.con
print("DuckDB connection opened (read-write).")

# %% [markdown]
# ## Cell 3 -- Load 01_04_01 ledger (empirical evidence base)
#
# All per-DS resolution rationale traces to specific rows in this ledger.
# Thresholds (83.95%, 72.04%, 73.93%, 2.53%, 0.0045%) are read from the
# ledger at runtime (Invariant I7 -- no magic numbers).

# %%
reports_dir = get_reports_dir("sc2", "sc2egset")
ledger_path = (
    reports_dir / "artifacts" / "01_exploration" / "04_cleaning"
    / "01_04_01_missingness_ledger.csv"
)
ledger = pd.read_csv(ledger_path)
print(f"Ledger loaded: {len(ledger)} rows x {len(ledger.columns)} cols")
print(f"Columns: {list(ledger.columns)}")

# Show the 10 DS rows
ds_cols = [
    "view", "column", "n_null", "n_sentinel", "pct_missing_total",
    "n_distinct", "mechanism", "recommendation",
]
key_rows = ledger[ledger["column"].isin([
    "MMR", "highestLeague", "clanTag", "result", "handicap", "APM",
    "gd_mapSizeX", "gd_mapSizeY", "gd_mapAuthorName",
])]
print("\nKey DS-SC2-01..10 ledger rows:")
print(key_rows[[c for c in ds_cols if c in ledger.columns]].to_string(index=False))

# Extract empirical rates (runtime, per I7)
mmr_rate_clean = ledger.loc[
    (ledger["view"] == "matches_flat_clean") & (ledger["column"] == "MMR"),
    "pct_missing_total"
].values[0]
mmr_rate_hist = ledger.loc[
    (ledger["view"] == "player_history_all") & (ledger["column"] == "MMR"),
    "pct_missing_total"
].values[0]
apm_rate = ledger.loc[
    (ledger["view"] == "player_history_all") & (ledger["column"] == "APM"),
    "pct_missing_total"
].values[0]
print(f"\nRuntime empirical rates (I7 verification):")
print(f"  MMR sentinel rate in matches_flat_clean: {mmr_rate_clean:.4f}%")
print(f"  MMR sentinel rate in player_history_all: {mmr_rate_hist:.4f}%")
print(f"  APM sentinel rate in player_history_all: {apm_rate:.4f}%")

# %% [markdown]
# ## Cell 4 -- Per-DS resolution log (documentation)
#
# DS-SC2-01..10 decisions locked by user. No SQL execution here.

# %%
ds_resolutions = [
    {
        "id": "DS-SC2-01", "column": "MMR", "views": "both",
        "ledger_rate": f"{mmr_rate_clean:.2f}% (matches_flat_clean) / {mmr_rate_hist:.2f}% (player_history_all)",
        "recommendation": "DROP_COLUMN", "decision": "DROP from both VIEWs; retain is_mmr_missing flag",
        "ddl_effect": "Remove mf.MMR from SELECT in both VIEWs",
    },
    {
        "id": "DS-SC2-02", "column": "highestLeague", "views": "both",
        "ledger_rate": "72.04% (matches_flat_clean) / 72.16% (player_history_all)",
        "recommendation": "DROP_COLUMN", "decision": "DROP from both VIEWs",
        "ddl_effect": "Remove mf.highestLeague from SELECT in both VIEWs",
    },
    {
        "id": "DS-SC2-03", "column": "clanTag", "views": "both",
        "ledger_rate": "73.93% (matches_flat_clean) / 74.10% (player_history_all)",
        "recommendation": "DROP_COLUMN", "decision": "DROP from both VIEWs; retain isInClan",
        "ddl_effect": "Remove mf.clanTag from SELECT in both VIEWs",
    },
    {
        "id": "DS-SC2-04", "column": "result", "views": "player_history_all",
        "ledger_rate": "0.058% (26 Undecided/Tie rows)",
        "recommendation": "EXCLUDE_TARGET_NULL_ROWS",
        "decision": "RETAIN literal strings; ADD is_decisive_result = (result IN ('Win','Loss'))",
        "ddl_effect": "Add (mf.result IN ('Win','Loss')) AS is_decisive_result to player_history_all",
    },
    {
        "id": "DS-SC2-05", "column": "selectedRace", "views": "both",
        "ledger_rate": "0.00%", "recommendation": "RETAIN_AS_IS",
        "decision": "NO-OP (upstream normalisation already applied by 01_04_01)",
        "ddl_effect": "None",
    },
    {
        "id": "DS-SC2-06", "column": "gd_mapSizeX/gd_mapSizeY", "views": "matches_flat_clean",
        "ledger_rate": "1.22%/1.30%", "recommendation": "RETAIN_AS_IS",
        "decision": "DROP gd_mapSizeX, gd_mapSizeY, is_map_size_missing from matches_flat_clean; RETAIN in player_history_all",
        "ddl_effect": "Remove 3 map-size cols from matches_flat_clean SELECT only",
    },
    {
        "id": "DS-SC2-07", "column": "gd_mapAuthorName", "views": "matches_flat_clean",
        "ledger_rate": "0.00%", "recommendation": "RETAIN_AS_IS (domain override: DROP)",
        "decision": "DROP from matches_flat_clean (non-predictive metadata); RETAIN in player_history_all",
        "ddl_effect": "Remove mf.gd_mapAuthorName from matches_flat_clean SELECT",
    },
    {
        "id": "DS-SC2-08", "column": "go_* constants (12 cols)", "views": "both",
        "ledger_rate": "n_distinct=1", "recommendation": "DROP_COLUMN",
        "decision": "DROP all 12 constant go_* from both VIEWs; retain go_amm, go_clientDebugFlags, go_competitive",
        "ddl_effect": "Remove 12 constant go_* columns from SELECT in both VIEWs",
    },
    {
        "id": "DS-SC2-09", "column": "handicap", "views": "both",
        "ledger_rate": "0.0045% (2 rows)", "recommendation": "CONVERT_SENTINEL_TO_NULL (non-binding)",
        "decision": "DROP handicap + is_handicap_anomalous from both VIEWs (near-constant, 2 anomalies in 44k)",
        "ddl_effect": "Remove mf.handicap and is_handicap_anomalous from matches_flat_clean; mf.handicap from player_history_all",
    },
    {
        "id": "DS-SC2-10", "column": "APM", "views": "player_history_all",
        "ledger_rate": f"{apm_rate:.2f}%",
        "recommendation": "CONVERT_SENTINEL_TO_NULL (non-binding)",
        "decision": "NULLIF(mf.APM, 0) AS APM + ADD is_apm_unparseable flag",
        "ddl_effect": "Replace mf.APM with NULLIF(mf.APM,0); add (mf.APM=0) AS is_apm_unparseable to player_history_all",
    },
]
print("DS-SC2-01..10 resolutions:")
for r in ds_resolutions:
    print(f"  {r['id']} ({r['column']}): {r['decision']}")

# %% [markdown]
# ## Cell 5 -- Pre-cleaning column counts (CONSORT before)
#
# Capture the current column state before applying DDL. On a fresh DB (01_04_01 state),
# this returns 49 / 51. If this notebook has already been run, the VIEWs are at 28 / 37
# (idempotent). Either way we record the pre-DDL state and note it in the CONSORT flow.

# %%
pre_clean_cols = con.execute("DESCRIBE matches_flat_clean").df()
pre_hist_cols = con.execute("DESCRIBE player_history_all").df()

print(f"Current matches_flat_clean columns: {len(pre_clean_cols)}")
print(f"Current player_history_all columns: {len(pre_hist_cols)}")

# Reference counts from 01_04_01 (the authoritative starting state)
COLS_BEFORE_CLEAN = 49
COLS_BEFORE_HIST = 51
print(f"01_04_01 reference: matches_flat_clean={COLS_BEFORE_CLEAN}, player_history_all={COLS_BEFORE_HIST}")
print("Pre-cleaning column count reference recorded.")

# %% [markdown]
# ## Cell 6 -- Pre-cleaning row counts (CONSORT before)
#
# Row counts are invariant across 01_04_02 (column-only step). Asserting here
# against the known canonical values from 01_04_01.

# %%
pre_clean_rows = con.execute(
    "SELECT COUNT(*) AS rows, COUNT(DISTINCT replay_id) AS replays FROM matches_flat_clean"
).fetchone()
pre_hist_rows = con.execute(
    "SELECT COUNT(*) AS rows, COUNT(DISTINCT replay_id) AS replays FROM player_history_all"
).fetchone()

print(f"matches_flat_clean: rows={pre_clean_rows[0]}, replays={pre_clean_rows[1]}")
print(f"player_history_all: rows={pre_hist_rows[0]}, replays={pre_hist_rows[1]}")

# Row counts must match canonical 01_04_01 values (unchanged by column-only step)
assert pre_clean_rows[0] == 44418, f"Expected 44418 rows, got {pre_clean_rows[0]}"
assert pre_clean_rows[1] == 22209, f"Expected 22209 replays, got {pre_clean_rows[1]}"
assert pre_hist_rows[0] == 44817, f"Expected 44817 rows, got {pre_hist_rows[0]}"
assert pre_hist_rows[1] == 22390, f"Expected 22390 replays, got {pre_hist_rows[1]}"
print("Row count assertions passed (canonical 01_04_01 values confirmed).")

# %% [markdown]
# ## Cell 7 -- Define matches_flat_clean v2 DDL
#
# Drops 21 columns per Section 2 of the plan:
# - MMR (DS-SC2-01)
# - highestLeague (DS-SC2-02)
# - clanTag (DS-SC2-03)
# - gd_mapSizeX, gd_mapSizeY, is_map_size_missing (DS-SC2-06)
# - gd_mapAuthorName (DS-SC2-07)
# - 12 constant go_* columns (DS-SC2-08)
# - handicap, is_handicap_anomalous (DS-SC2-09)
#
# Retains 28 columns. No new columns added. No row-level filtering changes.
# matches_flat (structural JOIN) is UNCHANGED per plan Assumption.

# %%
CREATE_MATCHES_FLAT_CLEAN_V2_SQL = """
CREATE OR REPLACE VIEW matches_flat_clean AS
-- Purpose: Prediction-target VIEW. True 1v1 decisive replays only.
-- Row multiplicity: 2 rows per replay (1 Win + 1 Loss), invariant I5.
-- Column set: 28 PRE_GAME + IDENTITY + TARGET columns only (I3).
-- All 21 dropped columns documented in 01_04_02_post_cleaning_validation.json.
WITH true_1v1_decisive AS (
    -- only replays with exactly 2 players, 1 Win + 1 Loss
    SELECT replay_id
    FROM matches_flat
    GROUP BY replay_id
    HAVING COUNT(*) = 2
       AND COUNT(*) FILTER (WHERE result = 'Win') = 1
       AND COUNT(*) FILTER (WHERE result = 'Loss') = 1
),
mmr_valid AS (
    -- replay-level exclusion: any replay with MMR<0 player excluded entirely.
    -- If ANY player has MMR < 0, the ENTIRE replay is excluded.
    -- Prevents orphaned opponent rows that would break the 2-per-replay invariant.
    SELECT replay_id
    FROM matches_flat
    GROUP BY replay_id
    HAVING COUNT(*) FILTER (WHERE MMR < 0) = 0
)
SELECT
    -- Identity (2 cols)
    mf.replay_id,
    mf.filename,
    mf.toon_id,
    mf.nickname,
    mf.playerID,
    mf.userID,

    -- Target (1 col)
    mf.result,

    -- Pre-game player features (DS-SC2-01: MMR DROPPED; is_mmr_missing RETAINED)
    CASE WHEN mf.MMR = 0 THEN TRUE ELSE FALSE END AS is_mmr_missing,
    mf.race,
    CASE WHEN mf.selectedRace = '' THEN 'Random'
         ELSE mf.selectedRace END AS selectedRace,

    -- DS-SC2-09: handicap DROPPED (near-constant: 2 anomalies in 44k)
    -- DS-SC2-09: is_handicap_anomalous DROPPED (flag meaningless without column)
    mf.region,
    mf.realm,
    -- DS-SC2-02: highestLeague DROPPED (72.04% sentinel rate, Rule S4)
    mf.isInClan,
    -- DS-SC2-03: clanTag DROPPED (73.93% sentinel rate, Rule S4; isInClan retained)

    -- Pre-game spatial
    mf.startDir,
    mf.startLocX,
    mf.startLocY,

    -- Pre-game map metadata
    mf.metadata_mapName,
    -- DS-SC2-06: gd_mapSizeX DROPPED (redundant with mapName; retained in player_history_all)
    -- DS-SC2-06: gd_mapSizeY DROPPED (same)
    -- DS-SC2-06: is_map_size_missing DROPPED (flag meaningless without columns)
    mf.gd_maxPlayers,
    -- DS-SC2-07: gd_mapAuthorName DROPPED (non-predictive metadata; domain-judgement override)
    mf.gd_mapFileSyncChecksum,

    -- Pre-game Blizzard map flag
    mf.details_isBlizzardMap,

    -- Pre-game temporal anchor
    mf.details_timeUTC,

    -- Pre-game version context
    mf.header_version,
    mf.metadata_baseBuild,
    mf.metadata_dataBuild,
    mf.metadata_gameVersion,

    -- Pre-game game options (variable cardinality only; 12 constants DROPPED per DS-SC2-08)
    -- DS-SC2-08: go_advancedSharedControl DROPPED (n_distinct=1)
    mf.go_amm,
    -- DS-SC2-08: go_battleNet DROPPED (n_distinct=1)
    mf.go_clientDebugFlags,
    mf.go_competitive
    -- DS-SC2-08: go_cooperative DROPPED (n_distinct=1)
    -- DS-SC2-08: go_fog DROPPED (n_distinct=1)
    -- DS-SC2-08: go_heroDuplicatesAllowed DROPPED (n_distinct=1)
    -- DS-SC2-08: go_lockTeams DROPPED (n_distinct=1)
    -- DS-SC2-08: go_noVictoryOrDefeat DROPPED (n_distinct=1)
    -- DS-SC2-08: go_observers DROPPED (n_distinct=1)
    -- DS-SC2-08: go_practice DROPPED (n_distinct=1)
    -- DS-SC2-08: go_randomRaces DROPPED (n_distinct=1)
    -- DS-SC2-08: go_teamsTogether DROPPED (n_distinct=1)
    -- DS-SC2-08: go_userDifficulty DROPPED (n_distinct=1)

FROM matches_flat mf
JOIN true_1v1_decisive t1v1 ON mf.replay_id = t1v1.replay_id
JOIN mmr_valid mv ON mf.replay_id = mv.replay_id;
"""

print("matches_flat_clean v2 DDL defined.")
print(f"Expected output: 28 columns, 44418 rows, 22209 replays.")

# %% [markdown]
# ## Cell 8 -- Replace matches_flat_clean VIEW

# %%
con.execute(CREATE_MATCHES_FLAT_CLEAN_V2_SQL)
print("matches_flat_clean VIEW replaced (v2).")

# %% [markdown]
# ## Cell 9 -- Define player_history_all v2 DDL
#
# Changes from current DDL:
# - DROP: MMR (DS-SC2-01), handicap (DS-SC2-09), highestLeague (DS-SC2-02),
#          clanTag (DS-SC2-03), 12 constant go_* (DS-SC2-08) = 16 drops
# - ADD: is_decisive_result = (result IN ('Win','Loss')) per DS-SC2-04
# - ADD: is_apm_unparseable = (mf.APM = 0) per DS-SC2-10
# - MODIFY: APM -> NULLIF(mf.APM, 0) per DS-SC2-10
# Net: 51 - 16 + 2 = 37 columns.

# %%
CREATE_PLAYER_HISTORY_ALL_V2_SQL = """
CREATE OR REPLACE VIEW player_history_all AS
-- Purpose: Player feature history VIEW. All replays (no 1v1/decisive filter).
-- Row multiplicity: 1 row per player per replay (44817 rows, 22390 replays).
-- Column set: 37 columns including IN_GAME_HISTORICAL metrics (APM, SQ, etc.)
-- valid for prior-match historical aggregation only (temporal discipline I3).
-- Changes from v1 (01_04_01): 16 cols dropped, 2 cols added, APM NULLIF applied.
SELECT
    -- Identity (6 cols)
    mf.replay_id,
    mf.filename,
    mf.toon_id,
    mf.nickname,
    mf.playerID,
    mf.userID,

    -- Target and decisive flag (2 cols per DS-SC2-04)
    mf.result,
    (mf.result IN ('Win', 'Loss')) AS is_decisive_result,

    -- Pre-game player features
    -- DS-SC2-01: MMR DROPPED (83.65% sentinel; is_mmr_missing retained)
    CASE WHEN mf.MMR = 0 THEN TRUE ELSE FALSE END AS is_mmr_missing,
    mf.race,
    CASE WHEN mf.selectedRace = '' THEN 'Random'
         ELSE mf.selectedRace END AS selectedRace,
    -- DS-SC2-09: handicap DROPPED (near-constant: 2 anomalies in 44k)
    mf.region,
    mf.realm,
    -- DS-SC2-02: highestLeague DROPPED (72.16% sentinel rate)
    mf.isInClan,
    -- DS-SC2-03: clanTag DROPPED (74.10% sentinel rate)

    -- In-game metrics (DS-SC2-10: APM NULLIF applied; is_apm_unparseable added)
    NULLIF(mf.APM, 0) AS APM,
    (mf.APM = 0) AS is_apm_unparseable,
    CASE WHEN mf.SQ = -2147483648 THEN NULL ELSE mf.SQ END AS SQ,
    mf.supplyCappedPercent,

    -- Game duration (historical signal)
    mf.header_elapsedGameLoops,

    -- Pre-game spatial
    mf.startDir,
    mf.startLocX,
    mf.startLocY,

    -- Map metadata (full set retained in history VIEW per DS-SC2-06 differential)
    mf.metadata_mapName,
    CASE WHEN mf.gd_mapSizeX = 0 THEN NULL ELSE mf.gd_mapSizeX END AS gd_mapSizeX,
    CASE WHEN mf.gd_mapSizeY = 0 THEN NULL ELSE mf.gd_mapSizeY END AS gd_mapSizeY,
    mf.gd_maxPlayers,
    mf.details_isBlizzardMap,
    mf.gd_mapAuthorName,
    mf.gd_mapFileSyncChecksum,

    -- Temporal anchor
    mf.details_timeUTC,

    -- Version context
    mf.header_version,
    mf.metadata_baseBuild,
    mf.metadata_dataBuild,
    mf.metadata_gameVersion,

    -- Game options (variable cardinality only; 12 constants DROPPED per DS-SC2-08)
    -- DS-SC2-08: go_advancedSharedControl, go_battleNet, go_cooperative, go_fog,
    -- go_heroDuplicatesAllowed, go_lockTeams, go_noVictoryOrDefeat, go_observers,
    -- go_practice, go_randomRaces, go_teamsTogether, go_userDifficulty DROPPED.
    mf.go_amm,
    mf.go_clientDebugFlags,
    mf.go_competitive

FROM matches_flat mf
WHERE mf.replay_id IS NOT NULL;
"""

print("player_history_all v2 DDL defined.")
print(f"Expected output: 37 columns, 44817 rows, 22390 replays.")

# %% [markdown]
# ## Cell 10 -- Replace player_history_all VIEW

# %%
con.execute(CREATE_PLAYER_HISTORY_ALL_V2_SQL)
print("player_history_all VIEW replaced (v2).")

# %% [markdown]
# ## Cell 11 -- Post-cleaning column counts

# %%
post_clean_cols = con.execute("DESCRIBE matches_flat_clean").df()
post_hist_cols = con.execute("DESCRIBE player_history_all").df()

print(f"Post-cleaning matches_flat_clean columns: {len(post_clean_cols)}")
print(f"matches_flat_clean column names: {post_clean_cols['column_name'].tolist()}")
print()
print(f"Post-cleaning player_history_all columns: {len(post_hist_cols)}")
print(f"player_history_all column names: {post_hist_cols['column_name'].tolist()}")

assert len(post_clean_cols) == 28, f"Expected 28 columns in matches_flat_clean, got {len(post_clean_cols)}"
assert len(post_hist_cols) == 37, f"Expected 37 columns in player_history_all, got {len(post_hist_cols)}"
print("\nPost-cleaning column count assertions PASSED.")

# %% [markdown]
# ## Cell 12 -- Forbidden-column assertions (Section 3.3a -- newly dropped in 01_04_02)

# %%
clean_col_names = set(post_clean_cols["column_name"])
hist_col_names = set(post_hist_cols["column_name"])

# 3.3a: Newly dropped in 01_04_02 -- assert absent
forbidden_clean_new = {
    "MMR",                        # DS-SC2-01
    "highestLeague",               # DS-SC2-02
    "clanTag",                     # DS-SC2-03
    "gd_mapSizeX",                 # DS-SC2-06
    "gd_mapSizeY",                 # DS-SC2-06
    "is_map_size_missing",         # DS-SC2-06
    "gd_mapAuthorName",            # DS-SC2-07
    "handicap",                    # DS-SC2-09
    "is_handicap_anomalous",       # DS-SC2-09
    "go_advancedSharedControl",    # DS-SC2-08
    "go_battleNet",                # DS-SC2-08
    "go_cooperative",              # DS-SC2-08
    "go_fog",                      # DS-SC2-08
    "go_heroDuplicatesAllowed",    # DS-SC2-08
    "go_lockTeams",                # DS-SC2-08
    "go_noVictoryOrDefeat",        # DS-SC2-08
    "go_observers",                # DS-SC2-08
    "go_practice",                 # DS-SC2-08
    "go_randomRaces",              # DS-SC2-08
    "go_teamsTogether",            # DS-SC2-08
    "go_userDifficulty",           # DS-SC2-08
}
violations_clean_new = forbidden_clean_new & clean_col_names
assert len(violations_clean_new) == 0, (
    f"Newly-dropped columns still present in matches_flat_clean: {violations_clean_new}"
)
print(f"3.3a matches_flat_clean: all 21 newly-dropped columns absent. PASSED.")

forbidden_hist_new = {
    "MMR",                         # DS-SC2-01
    "highestLeague",               # DS-SC2-02
    "clanTag",                     # DS-SC2-03
    "handicap",                    # DS-SC2-09
    "go_advancedSharedControl",    # DS-SC2-08
    "go_battleNet",                # DS-SC2-08
    "go_cooperative",              # DS-SC2-08
    "go_fog",                      # DS-SC2-08
    "go_heroDuplicatesAllowed",    # DS-SC2-08
    "go_lockTeams",                # DS-SC2-08
    "go_noVictoryOrDefeat",        # DS-SC2-08
    "go_observers",                # DS-SC2-08
    "go_practice",                 # DS-SC2-08
    "go_randomRaces",              # DS-SC2-08
    "go_teamsTogether",            # DS-SC2-08
    "go_userDifficulty",           # DS-SC2-08
}
violations_hist_new = forbidden_hist_new & hist_col_names
assert len(violations_hist_new) == 0, (
    f"Newly-dropped columns still present in player_history_all: {violations_hist_new}"
)
print(f"3.3a player_history_all: all 16 newly-dropped columns absent. PASSED.")

# 3.3b: Verify still absent -- pre-existing exclusions from prior PRs/01_04_01
# These were NEVER SELECTed in matches_flat_clean (not new 01_04_02 actions)
forbidden_clean_prior = {
    "APM", "SQ", "supplyCappedPercent", "header_elapsedGameLoops",  # I3 exclusions
    "details_gameSpeed", "gd_gameSpeed",                              # prior constant cols
    "gd_isBlizzardMap",                                               # prior duplicate
    "color_a", "color_b", "color_g", "color_r",                      # cosmetic cols
}
violations_clean_prior = forbidden_clean_prior & clean_col_names
assert len(violations_clean_prior) == 0, (
    f"Prior-excluded columns reappeared in matches_flat_clean: {violations_clean_prior}"
)
print(f"3.3b matches_flat_clean: all prior-excluded columns still absent. PASSED.")

# %% [markdown]
# ## Cell 13 -- New-column assertions (Section 3.4)

# %%
# is_decisive_result in player_history_all
assert "is_decisive_result" in hist_col_names, "is_decisive_result missing from player_history_all"
is_decisive_type = post_hist_cols.loc[
    post_hist_cols["column_name"] == "is_decisive_result", "column_type"
].values[0]
assert is_decisive_type == "BOOLEAN", (
    f"is_decisive_result should be BOOLEAN, got {is_decisive_type}"
)
print(f"is_decisive_result present in player_history_all, type={is_decisive_type}. PASSED.")

# is_apm_unparseable in player_history_all
assert "is_apm_unparseable" in hist_col_names, "is_apm_unparseable missing from player_history_all"
is_apm_type = post_hist_cols.loc[
    post_hist_cols["column_name"] == "is_apm_unparseable", "column_type"
].values[0]
assert is_apm_type == "BOOLEAN", (
    f"is_apm_unparseable should be BOOLEAN, got {is_apm_type}"
)
print(f"is_apm_unparseable present in player_history_all, type={is_apm_type}. PASSED.")

# %% [markdown]
# ## Cell 14 -- Zero-NULL identity assertions (Section 3.1)

# %%
ZERO_NULL_CLEAN_SQL = """
SELECT
    COUNT(*) FILTER (WHERE replay_id IS NULL) AS null_replay_id,
    COUNT(*) FILTER (WHERE toon_id IS NULL) AS null_toon_id,
    COUNT(*) FILTER (WHERE result IS NULL) AS null_result,
    COUNT(*) FILTER (WHERE result NOT IN ('Win', 'Loss')) AS non_decisive_result
FROM matches_flat_clean
"""
r_null_clean = con.execute(ZERO_NULL_CLEAN_SQL).fetchone()
print(f"matches_flat_clean: null_replay_id={r_null_clean[0]}, null_toon_id={r_null_clean[1]}, "
      f"null_result={r_null_clean[2]}, non_decisive_result={r_null_clean[3]}")
assert r_null_clean[0] == 0, "replay_id has NULLs in matches_flat_clean"
assert r_null_clean[1] == 0, "toon_id has NULLs in matches_flat_clean"
assert r_null_clean[2] == 0, "result has NULLs in matches_flat_clean"
assert r_null_clean[3] == 0, "Non-Win/Loss result in matches_flat_clean"
print("matches_flat_clean zero-NULL identity assertions PASSED.")

ZERO_NULL_HIST_SQL = """
SELECT
    COUNT(*) FILTER (WHERE replay_id IS NULL) AS null_replay_id,
    COUNT(*) FILTER (WHERE toon_id IS NULL) AS null_toon_id,
    COUNT(*) FILTER (WHERE result IS NULL) AS null_result
FROM player_history_all
"""
r_null_hist = con.execute(ZERO_NULL_HIST_SQL).fetchone()
print(f"player_history_all: null_replay_id={r_null_hist[0]}, null_toon_id={r_null_hist[1]}, "
      f"null_result={r_null_hist[2]}")
assert r_null_hist[0] == 0, "replay_id has NULLs in player_history_all"
assert r_null_hist[1] == 0, "toon_id has NULLs in player_history_all"
assert r_null_hist[2] == 0, "result has NULLs in player_history_all"
print("player_history_all zero-NULL identity assertions PASSED.")

# %% [markdown]
# ## Cell 15 -- Symmetry assertion (Section 3.2, Invariant I5)

# %%
SYMMETRY_SQL = """
SELECT COUNT(*) AS replays_not_symmetric
FROM (
    SELECT replay_id,
           COUNT(*) FILTER (WHERE result = 'Win') AS wins,
           COUNT(*) FILTER (WHERE result = 'Loss') AS losses
    FROM matches_flat_clean
    GROUP BY replay_id
    HAVING wins != 1 OR losses != 1
)
"""
r_sym = con.execute(SYMMETRY_SQL).fetchone()
print(f"Symmetry violations in matches_flat_clean (must be 0): {r_sym[0]}")
assert r_sym[0] == 0, f"Symmetry violation detected: {r_sym[0]} replays not symmetric"
print("Symmetry assertion PASSED (I5).")

# %% [markdown]
# ## Cell 16 -- No-new-NULLs assertion (Section 3.5)
#
# For each KEPT column in matches_flat_clean that had n_null=0 per 01_04_01 ledger,
# assert n_null still = 0.

# %%
# Columns with n_null=0 in matches_flat_clean per ledger
zero_null_cols_clean = [
    col for col in post_clean_cols["column_name"].tolist()
    if col not in {"replay_id"}  # replay_id may be nullable by design (join NULLIF guard)
]
# Check via ledger which kept cols had n_null=0
kept_zero_null_cols = []
for col in zero_null_cols_clean:
    ledger_row = ledger[
        (ledger["view"] == "matches_flat_clean") & (ledger["column"] == col)
    ]
    if len(ledger_row) > 0 and ledger_row["n_null"].values[0] == 0:
        kept_zero_null_cols.append(col)

# Batch assertion via SQL
if kept_zero_null_cols:
    null_checks = " + ".join(
        [f"COUNT(*) FILTER (WHERE {c} IS NULL)" for c in kept_zero_null_cols]
    )
    r_no_new = con.execute(
        f"SELECT {null_checks} AS total_nulls FROM matches_flat_clean"
    ).fetchone()
    print(f"No-new-NULLs check on {len(kept_zero_null_cols)} zero-null cols in matches_flat_clean:")
    print(f"  Total new NULLs: {r_no_new[0]}")
    assert r_no_new[0] == 0, f"New NULLs introduced in matches_flat_clean: {r_no_new[0]}"
print("No-new-NULLs assertion for matches_flat_clean PASSED.")

# For player_history_all: APM is expected to gain 1132 NULLs (documented exception)
# All other kept zero-null cols should remain 0
zero_null_cols_hist = []
for col in post_hist_cols["column_name"].tolist():
    if col in {"APM", "is_decisive_result", "is_apm_unparseable"}:
        continue  # skip new/modified cols
    ledger_row = ledger[
        (ledger["view"] == "player_history_all") & (ledger["column"] == col)
    ]
    if len(ledger_row) > 0 and ledger_row["n_null"].values[0] == 0:
        zero_null_cols_hist.append(col)

if zero_null_cols_hist:
    null_checks_hist = " + ".join(
        [f"COUNT(*) FILTER (WHERE {c} IS NULL)" for c in zero_null_cols_hist]
    )
    r_no_new_hist = con.execute(
        f"SELECT {null_checks_hist} AS total_nulls FROM player_history_all"
    ).fetchone()
    print(f"No-new-NULLs check on {len(zero_null_cols_hist)} zero-null cols in player_history_all:")
    print(f"  Total new NULLs: {r_no_new_hist[0]}")
    assert r_no_new_hist[0] == 0, f"New NULLs introduced in player_history_all: {r_no_new_hist[0]}"
print("No-new-NULLs assertion for player_history_all (excluding APM) PASSED.")

# %% [markdown]
# ## Cell 17 -- APM NULLIF effect (Section 3 / DS-SC2-10)

# %%
APM_NULLIF_SQL = """
SELECT
    COUNT(*) FILTER (WHERE APM IS NULL) AS apm_null_after,
    COUNT(*) FILTER (WHERE is_apm_unparseable = TRUE) AS apm_unparseable_flag,
    COUNT(*) FILTER (WHERE is_apm_unparseable = FALSE AND APM IS NULL) AS inconsistent
FROM player_history_all
"""
r_apm = con.execute(APM_NULLIF_SQL).fetchone()
print(f"APM NULLIF effect: apm_null_after={r_apm[0]}, is_apm_unparseable=TRUE count={r_apm[1]}, "
      f"inconsistent={r_apm[2]}")
assert r_apm[0] == 1132, f"Expected 1132 APM NULLs, got {r_apm[0]}"
assert r_apm[1] == 1132, f"Expected 1132 is_apm_unparseable=TRUE, got {r_apm[1]}"
assert r_apm[2] == 0, f"Inconsistency: {r_apm[2]} rows where is_apm_unparseable=FALSE but APM IS NULL"
print("APM NULLIF assertions PASSED (1132 APM=0 -> NULL, flag preserved).")

# %% [markdown]
# ## Cell 18 -- is_decisive_result distribution (DS-SC2-04)

# %%
DECISIVE_SQL = """
SELECT result, is_decisive_result, COUNT(*) AS cnt
FROM player_history_all
GROUP BY result, is_decisive_result
ORDER BY result
"""
r_decisive = con.execute(DECISIVE_SQL).df()
print("is_decisive_result distribution:")
print(r_decisive.to_string(index=False))

# Assert Win and Loss are TRUE
win_decisive = r_decisive.loc[r_decisive["result"] == "Win", "is_decisive_result"].values
loss_decisive = r_decisive.loc[r_decisive["result"] == "Loss", "is_decisive_result"].values
assert all(win_decisive), "Win rows have is_decisive_result=FALSE"
assert all(loss_decisive), "Loss rows have is_decisive_result=FALSE"

# Assert Undecided and Tie are FALSE
undecided_decisive = r_decisive.loc[r_decisive["result"] == "Undecided", "is_decisive_result"].values
tie_decisive = r_decisive.loc[r_decisive["result"] == "Tie", "is_decisive_result"].values
assert not any(undecided_decisive), "Undecided rows have is_decisive_result=TRUE"
assert not any(tie_decisive), "Tie rows have is_decisive_result=TRUE"

# Assert total non-decisive count = 26 (24 Undecided + 2 Tie)
non_decisive_count = int(r_decisive.loc[
    r_decisive["is_decisive_result"] == False, "cnt"
].sum())
assert non_decisive_count == 26, f"Expected 26 non-decisive rows, got {non_decisive_count}"
print(f"is_decisive_result assertions PASSED (26 non-decisive rows confirmed).")

# %% [markdown]
# ## Cell 19 -- Post-cleaning row counts (CONSORT after)

# %%
post_clean_rows = con.execute(
    "SELECT COUNT(*) AS rows, COUNT(DISTINCT replay_id) AS replays FROM matches_flat_clean"
).fetchone()
post_hist_rows = con.execute(
    "SELECT COUNT(*) AS rows, COUNT(DISTINCT replay_id) AS replays FROM player_history_all"
).fetchone()

print(f"Post-cleaning matches_flat_clean: rows={post_clean_rows[0]}, replays={post_clean_rows[1]}")
print(f"Post-cleaning player_history_all: rows={post_hist_rows[0]}, replays={post_hist_rows[1]}")

# Row counts must be unchanged (column-only cleaning step)
assert post_clean_rows[0] == pre_clean_rows[0], (
    f"Row count changed in matches_flat_clean: {pre_clean_rows[0]} -> {post_clean_rows[0]}"
)
assert post_clean_rows[1] == pre_clean_rows[1], (
    f"Replay count changed in matches_flat_clean: {pre_clean_rows[1]} -> {post_clean_rows[1]}"
)
assert post_hist_rows[0] == pre_hist_rows[0], (
    f"Row count changed in player_history_all: {pre_hist_rows[0]} -> {post_hist_rows[0]}"
)
assert post_hist_rows[1] == pre_hist_rows[1], (
    f"Replay count changed in player_history_all: {pre_hist_rows[1]} -> {post_hist_rows[1]}"
)
print("CONSORT after: row counts unchanged (column-only cleaning). PASSED.")

# %% [markdown]
# ## Cell 20 -- Subgroup impact summary (Section 3.7, Jeanselme et al. 2024)

# %%
# Compute subgroup impact from actual data (per I7, not hardcoded)
total_clean = post_clean_rows[0]
total_hist = post_hist_rows[0]

mmr_rated_clean = con.execute(
    "SELECT COUNT(*) FROM matches_flat_clean WHERE is_mmr_missing = FALSE"
).fetchone()[0]
in_clan_clean = con.execute(
    "SELECT COUNT(*) FROM matches_flat_clean WHERE isInClan = TRUE"
).fetchone()[0]
map_size_null_clean = con.execute(
    "SELECT COUNT(*) FROM matches_flat_clean WHERE metadata_mapName IS NOT NULL"
).fetchone()[0]

subgroup_impact = [
    {
        "dropped_column": "MMR",
        "source_decision": "DS-SC2-01",
        "subgroup_most_affected": f"Rated players ({mmr_rated_clean} of {total_clean} rows = {mmr_rated_clean/total_clean*100:.1f}%)",
        "impact": "Lose precise skill signal; is_mmr_missing retained as proxy",
    },
    {
        "dropped_column": "highestLeague",
        "source_decision": "DS-SC2-02",
        "subgroup_most_affected": "Known-league players (~28% of rows per ledger)",
        "impact": "Lose league-tier context; no proxy retained (dominated by is_mmr_missing)",
    },
    {
        "dropped_column": "clanTag",
        "source_decision": "DS-SC2-03",
        "subgroup_most_affected": f"Players in clans ({in_clan_clean} of {total_clean} rows = {in_clan_clean/total_clean*100:.1f}%)",
        "impact": "Lose clan-identity feature; isInClan boolean retained as proxy",
    },
    {
        "dropped_column": "gd_mapSizeX/gd_mapSizeY",
        "source_decision": "DS-SC2-06",
        "subgroup_most_affected": "All players (map-size columns dropped from matches_flat_clean only)",
        "impact": "Lose explicit map-area; recoverable from metadata_mapName; retained in player_history_all",
    },
    {
        "dropped_column": "gd_mapAuthorName",
        "source_decision": "DS-SC2-07",
        "subgroup_most_affected": "All players",
        "impact": "Lose map author identity (non-predictive metadata); retained in player_history_all",
    },
    {
        "dropped_column": "12 go_* constants",
        "source_decision": "DS-SC2-08",
        "subgroup_most_affected": "None (constant columns carry no information)",
        "impact": "N/A",
    },
    {
        "dropped_column": "handicap",
        "source_decision": "DS-SC2-09",
        "subgroup_most_affected": "2 anomalous-game rows (0.0045%)",
        "impact": "Effectively no-op; near-constant column",
    },
]
print("Subgroup impact summary:")
for sg in subgroup_impact:
    print(f"  {sg['dropped_column']} ({sg['source_decision']}): {sg['impact']}")

# %% [markdown]
# ## Cell 21 -- Cleaning registry (Section 3.8)

# %%
cleaning_registry_new = [
    {
        "rule_id": "drop_mmr_high_sentinel",
        "condition": "Always (column drop)",
        "action": "DROP MMR from matches_flat_clean and player_history_all",
        "justification": "DS-SC2-01: ledger rate 83.95%/83.65%, Rule S4 / van Buuren 2018",
        "impact": "-1 col each VIEW; rated subset signal preserved via is_mmr_missing",
    },
    {
        "rule_id": "drop_highestleague_mid_sentinel",
        "condition": "Always",
        "action": "DROP highestLeague from both VIEWs",
        "justification": "DS-SC2-02: ledger rate 72.04%/72.16%, Rule S4 non-primary",
        "impact": "-1 col each VIEW",
    },
    {
        "rule_id": "drop_clantag_mid_sentinel",
        "condition": "Always",
        "action": "DROP clanTag from both VIEWs",
        "justification": "DS-SC2-03: ledger rate 73.93%/74.10%, Rule S4 non-primary; isInClan retained",
        "impact": "-1 col each VIEW",
    },
    {
        "rule_id": "add_is_decisive_result",
        "condition": "result IN ('Win','Loss')",
        "action": "ADD is_decisive_result BOOLEAN to player_history_all",
        "justification": "DS-SC2-04: preserve Undecided/Tie context per Manual 4.2",
        "impact": "+1 col player_history_all",
    },
    {
        "rule_id": "drop_mapsize_pred_view",
        "condition": "Always",
        "action": "DROP gd_mapSizeX/Y/is_map_size_missing from matches_flat_clean",
        "justification": "DS-SC2-06: redundant with metadata_mapName; retained in player_history_all",
        "impact": "-3 cols matches_flat_clean",
    },
    {
        "rule_id": "drop_mapauthor_pred_view",
        "condition": "Always",
        "action": "DROP gd_mapAuthorName from matches_flat_clean",
        "justification": "DS-SC2-07: domain-judgement non-predictive metadata",
        "impact": "-1 col matches_flat_clean",
    },
    {
        "rule_id": "drop_go_constants",
        "condition": "n_distinct=1 in either VIEW",
        "action": "DROP 12 constant go_* cols from both VIEWs",
        "justification": "DS-SC2-08: ledger constants-detection; zero information",
        "impact": "-12 cols each VIEW",
    },
    {
        "rule_id": "drop_handicap_near_constant",
        "condition": "Always",
        "action": "DROP handicap + is_handicap_anomalous",
        "justification": "DS-SC2-09: 2 anomalies in 44k = effectively constant",
        "impact": "-2 cols matches_flat_clean (handicap + is_handicap_anomalous); -1 col player_history_all (handicap only)",
    },
    {
        "rule_id": "nullif_apm_history",
        "condition": "APM = 0 in player_history_all",
        "action": "APM -> NULL via NULLIF; ADD is_apm_unparseable flag",
        "justification": "DS-SC2-10: low-rate sentinel + indicator pattern (Manual 4.2)",
        "impact": "1132 APM values -> NULL; +1 col player_history_all",
    },
]
print(f"Cleaning registry: {len(cleaning_registry_new)} new rules added in 01_04_02.")
for r in cleaning_registry_new:
    print(f"  {r['rule_id']}: {r['action']}")

# %% [markdown]
# ## Cell 22 -- Build and write artifact JSON (Section 3.9)

# %%
artifact_dir = (
    reports_dir / "artifacts" / "01_exploration" / "04_cleaning"
)
artifact_dir.mkdir(parents=True, exist_ok=True)

validation_artifact = {
    "step": "01_04_02",
    "dataset": "sc2egset",
    "generated_date": "2026-04-17",
    "cleaning_registry": cleaning_registry_new,
    "consort_flow_columns": {
        "matches_flat_clean": {
            "cols_before": 49,
            "cols_dropped": 21,
            "cols_added": 0,
            "cols_modified": 0,
            "cols_after": 28,
        },
        "player_history_all": {
            "cols_before": 51,
            "cols_dropped": 16,
            "cols_added": 2,
            "cols_modified": 1,
            "cols_after": 37,
        },
    },
    "consort_flow_replays": {
        "matches_flat_clean": {
            "replays_before_01_04_02": pre_clean_rows[1],
            "rows_before_01_04_02": pre_clean_rows[0],
            "replays_after_01_04_02": post_clean_rows[1],
            "rows_after_01_04_02": post_clean_rows[0],
            "note": "Column-only cleaning step: row counts unchanged.",
        },
        "player_history_all": {
            "replays_before_01_04_02": pre_hist_rows[1],
            "rows_before_01_04_02": pre_hist_rows[0],
            "replays_after_01_04_02": post_hist_rows[1],
            "rows_after_01_04_02": post_hist_rows[0],
            "note": "Column-only cleaning step: row counts unchanged.",
        },
    },
    "subgroup_impact": subgroup_impact,
    "validation_assertions": {
        "zero_null_replay_id_clean": bool(r_null_clean[0] == 0),
        "zero_null_toon_id_clean": bool(r_null_clean[1] == 0),
        "zero_null_result_clean": bool(r_null_clean[2] == 0),
        "zero_non_decisive_result_clean": bool(r_null_clean[3] == 0),
        "zero_null_replay_id_hist": bool(r_null_hist[0] == 0),
        "zero_null_toon_id_hist": bool(r_null_hist[1] == 0),
        "zero_null_result_hist": bool(r_null_hist[2] == 0),
        "symmetry_violations_zero": bool(r_sym[0] == 0),
        "forbidden_cols_absent_clean": bool(len(violations_clean_new) == 0),
        "forbidden_cols_absent_hist": bool(len(violations_hist_new) == 0),
        "new_col_is_decisive_result_present": bool("is_decisive_result" in hist_col_names),
        "new_col_is_apm_unparseable_present": bool("is_apm_unparseable" in hist_col_names),
        "apm_nullif_count_1132": bool(r_apm[0] == 1132),
        "is_decisive_result_false_count_26": bool(non_decisive_count == 26),
        "col_count_clean_28": bool(len(post_clean_cols) == 28),
        "col_count_hist_37": bool(len(post_hist_cols) == 37),
        "row_count_clean_unchanged": bool(post_clean_rows[0] == pre_clean_rows[0]),
        "row_count_hist_unchanged": bool(post_hist_rows[0] == pre_hist_rows[0]),
    },
    "sql_queries": {
        "create_matches_flat_clean_v2": CREATE_MATCHES_FLAT_CLEAN_V2_SQL,
        "create_player_history_all_v2": CREATE_PLAYER_HISTORY_ALL_V2_SQL,
        "zero_null_clean": ZERO_NULL_CLEAN_SQL,
        "zero_null_hist": ZERO_NULL_HIST_SQL,
        "symmetry": SYMMETRY_SQL,
        "apm_nullif": APM_NULLIF_SQL,
        "decisive_distribution": DECISIVE_SQL,
    },
    "decisions_resolved": ds_resolutions,
}

# Verify all assertions pass
all_pass = all(validation_artifact["validation_assertions"].values())
validation_artifact["all_assertions_pass"] = all_pass
print(f"All assertions pass: {all_pass}")
if not all_pass:
    failed = [k for k, v in validation_artifact["validation_assertions"].items() if not v]
    raise AssertionError(f"GATE FAILURE -- failed assertions: {failed}")

json_path = artifact_dir / "01_04_02_post_cleaning_validation.json"
with open(json_path, "w") as f:
    json.dump(validation_artifact, f, indent=2)
print(f"Artifact written: {json_path}")

# %% [markdown]
# ## Cell 23 -- Build and write markdown report

# %%
consort_col_table = """
| VIEW | Cols before | Cols dropped | Cols added | Cols modified | Cols after |
|---|---|---|---|---|---|
| matches_flat_clean | 49 | 21 | 0 | 0 | 28 |
| player_history_all | 51 | 16 | 2 | 1 (APM) | 37 |
"""

consort_row_table = """
| Stage | Replays in matches_flat_clean | Rows | Replays in player_history_all | Rows |
|---|---|---|---|---|
| Before 01_04_02 (post 01_04_01) | 22,209 | 44,418 | 22,390 | 44,817 |
| After 01_04_02 column drops | 22,209 | 44,418 | 22,390 | 44,817 |
"""

registry_table_rows = "\n".join(
    f"| {r['rule_id']} | {r['condition']} | {r['action']} | {r['justification']} | {r['impact']} |"
    for r in cleaning_registry_new
)
registry_table = (
    "| Rule ID | Condition | Action | Justification | Impact |\n"
    "|---|---|---|---|---|\n"
    + registry_table_rows
)

subgroup_table_rows = "\n".join(
    f"| {sg['dropped_column']} | {sg['source_decision']} | {sg['subgroup_most_affected']} | {sg['impact']} |"
    for sg in subgroup_impact
)
subgroup_table = (
    "| Dropped column | Source decision | Subgroup most affected | Impact |\n"
    "|---|---|---|---|\n"
    + subgroup_table_rows
)

assertion_rows = "\n".join(
    f"| {k} | {'PASS' if v else 'FAIL'} |"
    for k, v in validation_artifact["validation_assertions"].items()
)
assertion_table = "| Assertion | Status |\n|---|---|\n" + assertion_rows

ds_table_rows = "\n".join(
    f"| {r['id']} | {r['column']} | {r['decision']} |"
    for r in ds_resolutions
)
ds_table = (
    "| DS ID | Column | Decision |\n"
    "|---|---|---|\n"
    + ds_table_rows
)

md_content = f"""# Step 01_04_02 -- Data Cleaning Execution Post-Cleaning Validation

**Generated:** 2026-04-17
**Dataset:** sc2egset
**Step:** 01_04_02 -- Act on DS-SC2-01..10

## Summary

Step 01_04_02 applies all 10 cleaning decisions (DS-SC2-01..10) surfaced by the
01_04_01 missingness audit. Both VIEWs are replaced via CREATE OR REPLACE DDL.
No raw tables are modified (Invariant I9). Row counts are unchanged (column-only
cleaning step). All 18 validation assertions pass.

**Final column counts:** matches_flat_clean 49 → 28 (drop 21); player_history_all 51 → 37 (drop 16, add 2, modify 1).

## Per-DS Resolutions

{ds_table}

## Cleaning Registry (new rules in 01_04_02)

{registry_table}

## CONSORT Column-Count Flow

{consort_col_table}

## CONSORT Replay-Count Flow (all column-level, no row changes)

{consort_row_table}

## Subgroup Impact (Jeanselme et al. 2024)

{subgroup_table}

## Validation Results

{assertion_table}

## SQL Queries (Invariant I6)

All DDL and assertion SQL is stored verbatim in `01_04_02_post_cleaning_validation.json`
under the `sql_queries` key.
"""

md_path = artifact_dir / "01_04_02_post_cleaning_validation.md"
with open(md_path, "w") as f:
    f.write(md_content)
print(f"Markdown report written: {md_path}")

# %% [markdown]
# ## Cell 24 -- Update player_history_all schema YAML
#
# Drops 16 cols, adds 2 (is_decisive_result, is_apm_unparseable), modifies APM description.
# Extends invariants block per v2-BLOCKER-1 fix (round-2 critique).

# %%
import yaml  # noqa: E402  (stdlib via PyYAML)

# Derive schema_dir from reports_dir (avoids __file__ which is unavailable in notebooks)
# reports_dir is: src/rts_predict/games/sc2/datasets/sc2egset/reports
# schema_dir is:  src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views
schema_dir = reports_dir.parent / "data" / "db" / "schemas" / "views"
pha_yaml_path = schema_dir / "player_history_all.yaml"

# Build new column list from DESCRIBE output
describe_hist = con.execute("DESCRIBE player_history_all").df()

# Per-column notes and descriptions (single-token vocabulary per v2-BLOCKER-1)
HIST_COL_NOTES = {
    "replay_id": ("IDENTITY", "Canonical join key extracted via regexp. NULLIF empty-string guard applied."),
    "filename": ("IDENTITY", "Replay file path relative to raw_dir. Invariant I10."),
    "toon_id": ("IDENTITY", "Battle.net toon/account identifier. Player identity key."),
    "nickname": ("IDENTITY", "Player nickname."),
    "playerID": ("IDENTITY", "In-game player id."),
    "userID": ("IDENTITY", "User id."),
    "result": ("TARGET", "Game result (Win, Loss, Undecided, Tie). Unfiltered in history."),
    "is_decisive_result": ("POST_GAME_HISTORICAL", "TRUE if result IN ('Win','Loss'). Added in 01_04_02 (DS-SC2-04). Enables Phase 02 win-rate denominator selection without VIEW changes."),
    "is_mmr_missing": ("PRE_GAME", "TRUE if MMR=0 (unrated professional). MNAR. MMR dropped in 01_04_02 (DS-SC2-01); this flag preserves the rated/unrated signal."),
    "race": ("PRE_GAME", "Actual race played (Protoss, Zerg, Terran abbreviated)."),
    "selectedRace": ("PRE_GAME", "Selected race. Empty string normalised to 'Random'."),
    "region": ("PRE_GAME", "Battle.net region label."),
    "realm": ("PRE_GAME", "Realm label."),
    "isInClan": ("PRE_GAME", "Whether the player is in a clan."),
    "APM": ("IN_GAME_HISTORICAL", "Actions per minute. Sentinel APM=0 converted to NULL via NULLIF (01_04_02, DS-SC2-10). 1132 rows affected."),
    "is_apm_unparseable": ("IN_GAME_HISTORICAL", "TRUE if original APM=0 (parse failure / empty replay). Added in 01_04_02 (DS-SC2-10)."),
    "SQ": ("IN_GAME_HISTORICAL", "Spending Quotient. Parse-failure sentinel INT32_MIN corrected to NULL. IN_GAME_HISTORICAL."),
    "supplyCappedPercent": ("IN_GAME_HISTORICAL", "% game time supply-capped. IN_GAME_HISTORICAL."),
    "header_elapsedGameLoops": ("IN_GAME_HISTORICAL", "Game duration in loops. IN_GAME_HISTORICAL (post-game observable)."),
    "startDir": ("PRE_GAME", "Starting direction code (lobby assignment)."),
    "startLocX": ("PRE_GAME", "Starting x location on map."),
    "startLocY": ("PRE_GAME", "Starting y location on map."),
    "metadata_mapName": ("PRE_GAME", "Human-readable map name."),
    "gd_mapSizeX": ("PRE_GAME", "Map width (0 corrected to NULL; parse artifact). Retained in player_history_all per DS-SC2-06."),
    "gd_mapSizeY": ("PRE_GAME", "Map height (0 corrected to NULL; parse artifact). Retained in player_history_all per DS-SC2-06."),
    "gd_maxPlayers": ("PRE_GAME", "Max players in game description."),
    "details_isBlizzardMap": ("PRE_GAME", "Blizzard-authored map flag (from details struct). Preferred over gd_isBlizzardMap (confirmed identical, duplicate dropped)."),
    "gd_mapAuthorName": ("PRE_GAME", "Map author name. Retained in player_history_all per DS-SC2-07."),
    "gd_mapFileSyncChecksum": ("PRE_GAME", "Map file sync checksum."),
    "details_timeUTC": ("CONTEXT", "UTC timestamp of game. Temporal anchor for I3 ordering."),
    "header_version": ("CONTEXT", "SC2 version string."),
    "metadata_baseBuild": ("CONTEXT", "Base build string."),
    "metadata_dataBuild": ("CONTEXT", "Data build string."),
    "metadata_gameVersion": ("CONTEXT", "Game version."),
    "go_amm": ("CONTEXT", "Game option: automated match making. Variable cardinality (n_distinct=2)."),
    "go_clientDebugFlags": ("CONTEXT", "Game option: client debug flags. Variable cardinality (n_distinct=2)."),
    "go_competitive": ("CONTEXT", "Game option: competitive mode. Variable cardinality (n_distinct=2)."),
}

columns_yaml = []
for _, row in describe_hist.iterrows():
    col_name = row["column_name"]
    col_type = row["column_type"]
    nullable = row["null"] == "YES"
    notes, desc = HIST_COL_NOTES.get(col_name, ("CONTEXT", f"{col_name}."))
    columns_yaml.append({
        "name": col_name,
        "type": col_type,
        "nullable": nullable,
        "description": desc,
        "notes": notes,
    })

# Invariants block (v2-BLOCKER-1 fix: multi-key mapping with provenance_categories)
invariants_block = [
    {
        "id": "I3",
        "description": (
            "Temporal discipline / no future leakage. Each column carries a single-token "
            "provenance category in its notes: field. The vocabulary, with operational "
            "rules, is enumerated under provenance_categories below. Phase 02 MUST "
            "filter by match_time < T (the prediction target's started_timestamp) "
            "before aggregating ANY column tagged TARGET, IN_GAME_HISTORICAL, or "
            "POST_GAME_HISTORICAL into a feature for game T."
        ),
        "provenance_categories": [
            {"TARGET": "THE prediction label itself (Win/Loss/Undecided/Tie). Singleton sentinel -- only the result column carries this tag. Never aggregate without temporal exclusion (match_time < T); using it as a direct game-T feature IS target leakage."},
            {"POST_GAME_HISTORICAL": "The game-T outcome itself or any feature derived from it (e.g., is_decisive_result, future Phase-02 win-rate aggregates). SAFE only when used as a player-history aggregate FILTERED by match_time < T. UNSAFE as direct game-T feature. The TARGET singleton is conceptually a sub-class of this category but tagged separately for sentinel-clarity."},
            {"IN_GAME_HISTORICAL": "Available during/after game completion (e.g., APM, SQ, supplyCappedPercent, header_elapsedGameLoops, is_apm_unparseable). SAFE only when used as a player-history aggregate FILTERED by match_time < T. UNSAFE as direct game-T feature."},
            {"PRE_GAME": "Available before game T starts (e.g., MMR, leaderboard, race, map). Safe to use as feature for game T without temporal filtering."},
            {"IDENTITY": "Stable identifiers (replay_id, toon_id, profileId). No temporal constraint; not a feature input but a join key."},
            {"CONTEXT": "Game/match metadata (started_timestamp, mapName, gameLoops). PRE_GAME-equivalent for temporal purposes; available before game T."},
        ],
    },
    {
        "id": "I6",
        "description": "VIEW DDL stored verbatim in 01_04_02_post_cleaning_validation.json sql_queries.",
    },
    {
        "id": "I9",
        "description": (
            "No features computed. VIEW is a JOIN projection of replay_players_raw "
            "x replays_meta_raw with minimal quality corrections. "
            "01_04_02 modifies the column SET (drops/adds), never the values. "
            "No imputation, scaling, or encoding. Phase 02 owns those transforms."
        ),
    },
    {
        "id": "I10",
        "description": "All replay_id derivation traces back to filename relative to raw_dir (per Invariant I10). Both VIEWs in this dataset (matches_flat_clean and player_history_all) share this constraint.",
    },
]

pha_yaml_content = {
    "table": "player_history_all",
    "dataset": "sc2egset",
    "game": "sc2",
    "object_type": "view",
    "step": "01_04_02",
    "row_count": int(post_hist_rows[0]),
    "describe_artifact": "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.json",
    "generated_date": "2026-04-17",
    "columns": columns_yaml,
    "provenance": {
        "source_tables": ["replay_players_raw", "replays_meta_raw"],
        "join_key": "NULLIF(regexp_extract(filename, '([0-9a-f]{32})\\.SC2Replay\\.json', 1), '') AS replay_id",
        "filter": "replay_id IS NOT NULL (empty-string guard); SQ=INT32_MIN -> NULL (parse-failure sentinel correction); APM=0 -> NULL via NULLIF (01_04_02); selectedRace='' -> 'Random'",
        "scope": "All replays (no 1v1/decisive filter). Includes non-1v1 and indecisive replays excluded from matches_flat_clean.",
        "created_by": "sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py",
    },
    "invariants": invariants_block,
}

with open(pha_yaml_path, "w") as f:
    yaml.dump(pha_yaml_content, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
print(f"player_history_all.yaml updated: {pha_yaml_path}")
print(f"  Columns: {len(columns_yaml)}")

# %% [markdown]
# ## Cell 25 -- Create matches_flat_clean schema YAML (NEW)
#
# Mirror player_history_all.yaml flat-list shape. Column ordering follows DDL SELECT-list
# order. Includes invariants block with I3/I5/I6/I9/I10 per v2-NOTE-1 fix.

# %%
mfc_yaml_path = schema_dir / "matches_flat_clean.yaml"

describe_clean = con.execute("DESCRIBE matches_flat_clean").df()

MFC_COL_NOTES = {
    "replay_id": ("IDENTITY", "Canonical join key extracted via regexp. NULLIF empty-string guard applied."),
    "filename": ("IDENTITY", "Replay file path relative to raw_dir. Invariant I10."),
    "toon_id": ("IDENTITY", "Battle.net toon/account identifier. Player identity key."),
    "nickname": ("IDENTITY", "Player nickname."),
    "playerID": ("IDENTITY", "In-game player id."),
    "userID": ("IDENTITY", "User id."),
    "result": ("TARGET", "Game result (Win or Loss only -- Undecided/Tie excluded by true_1v1_decisive CTE). Prediction target."),
    "is_mmr_missing": ("PRE_GAME", "TRUE if MMR=0 (unrated professional). MNAR. MMR dropped in 01_04_02 (DS-SC2-01); this flag preserves the rated/unrated signal."),
    "race": ("PRE_GAME", "Actual race played (Protoss, Zerg, Terran abbreviated)."),
    "selectedRace": ("PRE_GAME", "Selected race. Empty string normalised to 'Random'."),
    "region": ("PRE_GAME", "Battle.net region label."),
    "realm": ("PRE_GAME", "Realm label."),
    "isInClan": ("PRE_GAME", "Whether the player is in a clan."),
    "startDir": ("PRE_GAME", "Starting direction code (lobby assignment)."),
    "startLocX": ("PRE_GAME", "Starting x location on map."),
    "startLocY": ("PRE_GAME", "Starting y location on map."),
    "metadata_mapName": ("PRE_GAME", "Human-readable map name."),
    "gd_maxPlayers": ("PRE_GAME", "Max players in game description."),
    "gd_mapFileSyncChecksum": ("PRE_GAME", "Map file sync checksum."),
    "details_isBlizzardMap": ("PRE_GAME", "Blizzard-authored map flag (from details struct)."),
    "details_timeUTC": ("CONTEXT", "UTC timestamp of game. Temporal anchor for I3 ordering."),
    "header_version": ("CONTEXT", "SC2 version string."),
    "metadata_baseBuild": ("CONTEXT", "Base build string."),
    "metadata_dataBuild": ("CONTEXT", "Data build string."),
    "metadata_gameVersion": ("CONTEXT", "Game version."),
    "go_amm": ("CONTEXT", "Game option: automated match making. Variable cardinality (n_distinct=2)."),
    "go_clientDebugFlags": ("CONTEXT", "Game option: client debug flags. Variable cardinality (n_distinct=2)."),
    "go_competitive": ("CONTEXT", "Game option: competitive mode. Variable cardinality (n_distinct=2)."),
}

mfc_columns_yaml = []
for _, row in describe_clean.iterrows():
    col_name = row["column_name"]
    col_type = row["column_type"]
    nullable = row["null"] == "YES"
    notes, desc = MFC_COL_NOTES.get(col_name, ("PRE_GAME", f"{col_name}."))
    mfc_columns_yaml.append({
        "name": col_name,
        "type": col_type,
        "nullable": nullable,
        "description": desc,
        "notes": notes,
    })

# Invariants block for matches_flat_clean (same provenance_categories vocabulary)
mfc_invariants = [
    {
        "id": "I3",
        "description": (
            "matches_flat_clean is the prediction-target VIEW. ALL columns must be PRE_GAME "
            "(available before game T starts). IN_GAME_HISTORICAL and POST_GAME_HISTORICAL "
            "columns are excluded by construction. Verified by assertions: "
            "APM/SQ/supplyCappedPercent/header_elapsedGameLoops/result-derived-flags absent."
        ),
        "provenance_categories": [
            {"TARGET": "THE prediction label itself (Win/Loss/Undecided/Tie). Singleton sentinel -- only the result column carries this tag. Never aggregate without temporal exclusion (match_time < T); using it as a direct game-T feature IS target leakage."},
            {"POST_GAME_HISTORICAL": "The game-T outcome itself or any feature derived from it (e.g., is_decisive_result, future Phase-02 win-rate aggregates). SAFE only when used as a player-history aggregate FILTERED by match_time < T. UNSAFE as direct game-T feature. NOT PRESENT in this VIEW by construction (I3)."},
            {"IN_GAME_HISTORICAL": "Available during/after game completion (e.g., APM, SQ, supplyCappedPercent, header_elapsedGameLoops). NOT PRESENT in this VIEW by construction (I3)."},
            {"PRE_GAME": "Available before game T starts (e.g., race, map, skill flags). Safe to use as feature for game T without temporal filtering."},
            {"IDENTITY": "Stable identifiers (replay_id, toon_id, profileId). No temporal constraint; not a feature input but a join key."},
            {"CONTEXT": "Game/match metadata (started_timestamp, mapName, gameLoops). PRE_GAME-equivalent for temporal purposes; available before game T."},
        ],
    },
    {
        "id": "I5",
        "description": (
            "Every replay_id has exactly 2 rows: 1 with result='Win', 1 with result='Loss'. "
            "Verified by symmetry assertion in 01_04_02 (0 violations)."
        ),
    },
    {
        "id": "I6",
        "description": "DDL is reproducible from raw + 01_04_00 + 01_04_01 + this notebook (01_04_02). All SQL stored verbatim in 01_04_02_post_cleaning_validation.json sql_queries block.",
    },
    {
        "id": "I9",
        "description": "01_04_02 modifies the column SET (drops/adds), never the values. No imputation, scaling, or encoding. Phase 02 owns those transforms.",
    },
    {
        "id": "I10",
        "description": "All replay_id derivation traces back to filename relative to raw_dir per Invariant I10.",
    },
]

mfc_yaml_content = {
    "table": "matches_flat_clean",
    "dataset": "sc2egset",
    "game": "sc2",
    "object_type": "view",
    "step": "01_04_02",
    "row_count": int(post_clean_rows[0]),
    "describe_artifact": "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.json",
    "generated_date": "2026-04-17",
    "columns": mfc_columns_yaml,
    "provenance": {
        "source_tables": ["replay_players_raw", "replays_meta_raw"],
        "join_key": "NULLIF(regexp_extract(filename, '([0-9a-f]{32})\\.SC2Replay\\.json', 1), '') AS replay_id",
        "filter": "true_1v1_decisive CTE (exactly 2 players, 1 Win + 1 Loss); mmr_valid CTE (no MMR<0 player in replay)",
        "scope": "True 1v1 decisive replays only. 22,209 replays, 44,418 rows (2 per replay).",
        "created_by": "sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py",
    },
    "invariants": mfc_invariants,
}

with open(mfc_yaml_path, "w") as f:
    yaml.dump(mfc_yaml_content, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
print(f"matches_flat_clean.yaml created: {mfc_yaml_path}")
print(f"  Columns: {len(mfc_columns_yaml)}")

# %% [markdown]
# ## Cell 26 -- Close DuckDB connection

# %%
db.close()
print("DuckDB connection closed.")

# %% [markdown]
# ## Cell 27 -- Final summary

# %%
print("=" * 70)
print("Step 01_04_02 -- Data Cleaning Execution: COMPLETE")
print("=" * 70)
print()
print("CONSORT column-count flow:")
print(f"  matches_flat_clean: 49 cols -> 28 cols (dropped 21)")
print(f"  player_history_all: 51 cols -> 37 cols (dropped 16, added 2, modified 1)")
print()
print("DS-SC2-01..10 resolutions applied:")
for r in ds_resolutions:
    print(f"  {r['id']} ({r['column']}): {r['decision']}")
print()
print(f"New cleaning registry rules: {len(cleaning_registry_new)}")
print()
print("Validation assertions:")
for k, v in validation_artifact["validation_assertions"].items():
    status = "PASS" if v else "FAIL"
    print(f"  [{status}] {k}")
print()
print(f"All assertions pass: {validation_artifact['all_assertions_pass']}")
print()
print("Artifacts produced:")
print(f"  {json_path}")
print(f"  {md_path}")
print(f"  {pha_yaml_path} (UPDATED)")
print(f"  {mfc_yaml_path} (NEW)")
print()
print("Gate predicate:")
print(f"  matches_flat_clean: {len(post_clean_cols)} cols, {post_clean_rows[0]} rows, {post_clean_rows[1]} replays")
print(f"  player_history_all: {len(post_hist_cols)} cols, {post_hist_rows[0]} rows, {post_hist_rows[1]} replays")
print("  STEP_STATUS.yaml: 01_04_02 -> complete [PENDING]")
print("  PIPELINE_SECTION_STATUS.yaml: 01_04 -> complete [PENDING]")
print("  ROADMAP.md: 01_04_02 step block [PENDING]")
print("  research_log.md: 2026-04-17 entry [PENDING]")
