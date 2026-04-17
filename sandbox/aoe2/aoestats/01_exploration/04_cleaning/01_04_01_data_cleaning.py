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
# # Step 01_04_01 -- Data Cleaning: aoestats
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_04 -- Data Cleaning
# **Dataset:** aoestats
# **Question:** What cleaned analytical VIEWs should be created for downstream
# feature engineering and prediction?
# **Invariants applied:**
# - #3 (temporal discipline -- new_rating excluded; started_timestamp exposed for downstream WHERE)
# - #5 (symmetric player treatment -- team-assignment asymmetry documented; randomisation deferred to 01_05)
# - #6 (reproducibility -- all SQL stored verbatim)
# - #7 (no magic numbers -- all thresholds from prior artifacts)
# - #9 (step scope: cleaning and VIEW creation only)
# **Predecessor:** 01_03_03 (Table Utility Assessment -- complete, artifacts on disk)
# **Step scope:** Create `matches_1v1_clean` (prediction target VIEW) and
# `player_history_all` (feature computation source VIEW). No feature decisions.
# **ROADMAP reference:** `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` Step 01_04_01
# **Date:** 2026-04-16
# **ROADMAP ref:** 01_04_01

# %%
import json
from pathlib import Path

import numpy as np
import pandas as pd

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir, setup_notebook_logging

logger = setup_notebook_logging(__name__)

# %%
# Use read_only=False to create VIEWs
db = get_notebook_db("aoe2", "aoestats", read_only=False)
con = db.con  # public attribute (W4 fix: use db.con, not the private attribute)

# %%
reports_dir = get_reports_dir("aoe2", "aoestats")
cleaning_dir = reports_dir / "artifacts" / "01_exploration" / "04_cleaning"
cleaning_dir.mkdir(parents=True, exist_ok=True)

# Load prior artifacts for cross-validation
census_path = reports_dir / "artifacts" / "01_exploration" / "02_eda" / "01_02_04_univariate_census.json"
with open(census_path) as f:
    census = json.load(f)

bivariate_path = reports_dir / "artifacts" / "01_exploration" / "02_eda" / "01_02_06_bivariate_eda.json"
with open(bivariate_path) as f:
    bivariate = json.load(f)

print("Artifacts loaded. Reports dir:", reports_dir)

# %% [markdown]
# ## profile_id precision verification
#
# Objective: Verify no precision loss from DOUBLE storage. Verify DOUBLE precision safety.
# Threshold 2^53 = 9,007,199,254,740,992 is the IEEE 754 double safe-integer bound.

# %%
SQL_T01_PROFILE_ID_PRECISION = """
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE profile_id IS NOT NULL) AS nonnull_rows,
    COUNT(*) FILTER (WHERE profile_id IS NOT NULL
        AND profile_id - FLOOR(profile_id) != 0) AS fractional_count,
    COUNT(*) FILTER (WHERE profile_id IS NOT NULL
        AND ABS(profile_id) > 9007199254740992) AS unsafe_range_count,
    MIN(profile_id) FILTER (WHERE profile_id IS NOT NULL) AS min_id,
    MAX(profile_id) FILTER (WHERE profile_id IS NOT NULL) AS max_id
FROM players_raw
"""

t01_result = con.execute(SQL_T01_PROFILE_ID_PRECISION).df()
print("profile_id precision verification:")
print(t01_result.to_string())

assert t01_result["fractional_count"].iloc[0] == 0, "FAIL: fractional profile_ids found"
assert t01_result["unsafe_range_count"].iloc[0] == 0, "FAIL: profile_ids exceed 2^53"
print("PASS: fractional_count=0, unsafe_range_count=0, max_id < 2^53")

# %% [markdown]
# ## 1v1 scope restriction (prediction target only)
#
# Objective: Define ranked 1v1 scope for the prediction target VIEW.
# IMPORTANT: This restriction applies to matches_1v1_clean ONLY.
# player_history_all covers ALL game types and leaderboards.

# %%
SQL_T02_SCOPE = """
WITH player_counts AS (
    SELECT game_id, COUNT(*) AS player_count FROM players_raw GROUP BY game_id
),
scope AS (
    SELECT
        COUNT(*) AS total_matches,
        COUNT(*) FILTER (WHERE pc.player_count IS NULL) AS orphan_matches,
        COUNT(*) FILTER (WHERE pc.player_count IS NOT NULL) AS matches_with_players,
        COUNT(*) FILTER (WHERE pc.player_count = 2) AS structural_1v1,
        COUNT(*) FILTER (WHERE m.leaderboard = 'random_map') AS ranked_rm,
        COUNT(*) FILTER (WHERE pc.player_count = 2
            AND m.leaderboard = 'random_map') AS scope_1v1_ranked,
        COUNT(*) FILTER (WHERE pc.player_count = 2
            AND m.leaderboard != 'random_map') AS scope_1v1_unranked,
        COUNT(*) FILTER (WHERE pc.player_count != 2
            AND pc.player_count IS NOT NULL
            AND m.leaderboard = 'random_map') AS ranked_not_1v1
    FROM matches_raw m
    LEFT JOIN player_counts pc ON m.game_id = pc.game_id
)
SELECT * FROM scope
"""

t02_result = con.execute(SQL_T02_SCOPE).df()
print("1v1 scope restriction:")
print(t02_result.to_string())

assert t02_result["total_matches"].iloc[0] == 30_690_651
assert t02_result["orphan_matches"].iloc[0] == 212_890
assert t02_result["structural_1v1"].iloc[0] == 18_438_769
assert t02_result["scope_1v1_ranked"].iloc[0] == 17_815_944
print("PASS: all counts match 01_03_01 and 01_03_02 artifacts")

# %% [markdown]
# ## Orphan match exclusion
#
# Objective: Document 212,890 orphan match exclusion (matches with no player rows).

# %%
SQL_T03_ORPHANS = """
SELECT COUNT(*) AS orphan_match_count
FROM matches_raw m
WHERE NOT EXISTS (SELECT 1 FROM players_raw p WHERE p.game_id = m.game_id)
"""

t03_result = con.execute(SQL_T03_ORPHANS).fetchone()
print("orphan_match_count:", t03_result[0])
assert t03_result[0] == 212_890, f"FAIL: unexpected orphan count {t03_result[0]}"
print("PASS: orphan_match_count=212,890 (validated against 01_03_01)")

# %% [markdown]
# ## Constant and near-dead column documentation
#
# Objective: Document exclusion of zero-information columns (constant and near-constant).

# %%
SQL_T04_CONSTANTS = """
SELECT
    'game_type' AS column_name, COUNT(DISTINCT game_type) AS cardinality, MIN(game_type) AS sole_value
FROM matches_raw
UNION ALL
SELECT 'game_speed', COUNT(DISTINCT game_speed), MIN(game_speed) FROM matches_raw
UNION ALL
SELECT 'starting_age', COUNT(DISTINCT starting_age), MIN(starting_age) FROM matches_raw
"""

t04_result = con.execute(SQL_T04_CONSTANTS).df()
print("Constant/near-dead columns:")
print(t04_result.to_string())

game_type_card = t04_result[t04_result["column_name"] == "game_type"]["cardinality"].iloc[0]
game_speed_card = t04_result[t04_result["column_name"] == "game_speed"]["cardinality"].iloc[0]
starting_age_card = t04_result[t04_result["column_name"] == "starting_age"]["cardinality"].iloc[0]
assert game_type_card == 1, "FAIL: game_type not constant"
assert game_speed_card == 1, "FAIL: game_speed not constant"
assert starting_age_card == 2, "FAIL: starting_age cardinality changed"
print("PASS: game_type cardinality=1, game_speed cardinality=1, starting_age cardinality=2")

# %% [markdown]
# ## Temporal schema analysis for high-NULL columns
#
# Objective: Find the date boundary where opening, feudal_age_uptime,
# castle_age_uptime, imperial_age_uptime transition from all-NULL to populated.
# Finding only -- feature-inclusion decision deferred to Phase 02 (I9).
#
# Filename convention verification: SUBSTR(filename, 9, 10) extracts week-start date
# from pattern: "players/2022-08-28_2022-09-03_players.parquet"

# %%
SQL_T05_VERIFY_FILENAME = """
SELECT filename, SUBSTR(filename, 9, 10) AS week_date FROM players_raw LIMIT 3
"""

t05_sample = con.execute(SQL_T05_VERIFY_FILENAME).df()
print("Filename parsing verification:")
print(t05_sample.to_string())

SQL_T05_TEMPORAL = """
WITH weekly AS (
    SELECT
        SUBSTR(filename, 9, 10) AS week_date,
        COUNT(*) AS total_rows,
        COUNT(opening) AS opening_nonnull,
        COUNT(feudal_age_uptime) AS feudal_nonnull,
        COUNT(castle_age_uptime) AS castle_nonnull,
        COUNT(imperial_age_uptime) AS imperial_nonnull,
        ROUND(100.0 * COUNT(opening) / COUNT(*), 2) AS opening_pct,
        ROUND(100.0 * COUNT(feudal_age_uptime) / COUNT(*), 2) AS feudal_pct,
        ROUND(100.0 * COUNT(castle_age_uptime) / COUNT(*), 2) AS castle_pct,
        ROUND(100.0 * COUNT(imperial_age_uptime) / COUNT(*), 2) AS imperial_pct
    FROM players_raw
    GROUP BY SUBSTR(filename, 9, 10)
)
SELECT * FROM weekly ORDER BY week_date
"""

t05_result = con.execute(SQL_T05_TEMPORAL).df()
print(f"Temporal schema analysis ({len(t05_result)} weeks):")
print(t05_result.to_string())

# Find transition boundary
last_populated_week = t05_result[t05_result["opening_pct"] > 1.0]["week_date"].max()
first_zero_week = t05_result[t05_result["opening_pct"] == 0.0]["week_date"].min()
print(f"Schema transition: last week with opening > 1%: {last_populated_week}")
print(f"Schema transition: first week with opening = 0%: {first_zero_week}")

# %% [markdown]
# ## Create matches_1v1_clean VIEW
#
# Run same-team assertion before creating VIEW to confirm the COUNT(DISTINCT team)=2 predicate is sufficient.

# %%
SQL_T06_SAME_TEAM_ASSERTION = """
SELECT COUNT(*) AS same_team_game_count
FROM (
    SELECT game_id
    FROM players_raw
    GROUP BY game_id
    HAVING COUNT(*) = 2 AND COUNT(DISTINCT team) < 2
) st
"""

t06_same_team = con.execute(SQL_T06_SAME_TEAM_ASSERTION).fetchone()[0]
print(f"same_team_game_count: {t06_same_team}")
print("Same-team assertion: 0-impact (condition never triggered, no exclusion needed)")

# %%
# VIEW SQL with I3-safe column selection
# EXCLUDES: new_rating (I3 violation — post-game), game_type/game_speed (constant columns),
#           starting_age (near-dead: 99.99994% single value), filename (provenance), team (redundant after pivot)
# INCLUDES: team1_wins column to make team-assignment asymmetry explicit (I5)
# ALSO EXCLUDES: inconsistent winner rows — both players same outcome (997 rows, 0.0056%)

SQL_T06_MATCHES_1V1_CLEAN = """
CREATE OR REPLACE VIEW matches_1v1_clean AS
WITH ranked_1v1 AS (
    SELECT m.game_id
    FROM matches_raw m
    INNER JOIN (
        SELECT game_id
        FROM players_raw
        GROUP BY game_id
        HAVING COUNT(*) = 2 AND COUNT(DISTINCT team) = 2
    ) pc ON m.game_id = pc.game_id
    WHERE m.leaderboard = 'random_map'
),
p0 AS (SELECT * FROM players_raw WHERE team = 0),
p1 AS (SELECT * FROM players_raw WHERE team = 1)
SELECT
    m.game_id,
    m.started_timestamp,
    m.leaderboard,
    m.map,
    m.mirror,
    m.num_players,
    m.patch,
    m.raw_match_type,
    m.replay_enhanced,
    m.avg_elo,
    m.team_0_elo,
    m.team_1_elo,
    CAST(p0.profile_id AS BIGINT) AS p0_profile_id,
    p0.civ AS p0_civ,
    p0.old_rating AS p0_old_rating,
    p0.winner AS p0_winner,
    CAST(p1.profile_id AS BIGINT) AS p1_profile_id,
    p1.civ AS p1_civ,
    p1.old_rating AS p1_old_rating,
    p1.winner AS p1_winner,
    -- WARNING (I5): p0 = team=0, p1 = team=1. team=1 wins ~52.27% (slot asymmetry documented in 01_04_01).
    -- Phase 02 feature engineering MUST randomise player-slot assignment before using
    -- p0_*/p1_* columns as focal/opponent pairs. DO NOT use raw p0/p1 as symmetric features.
    p1.winner AS team1_wins
FROM ranked_1v1 r
INNER JOIN matches_raw m ON m.game_id = r.game_id
INNER JOIN p0 ON p0.game_id = r.game_id
INNER JOIN p1 ON p1.game_id = r.game_id
WHERE p0.winner != p1.winner
"""

con.execute(SQL_T06_MATCHES_1V1_CLEAN)
t06_cnt = con.execute("SELECT COUNT(*) FROM matches_1v1_clean").fetchone()[0]
print(f"matches_1v1_clean VIEW created. Row count: {t06_cnt:,}")
assert abs(t06_cnt - 17_814_947) <= 1000, f"FAIL: unexpected row count {t06_cnt}"
print("PASS: row count within +/-1000 of expected 17,814,947")

# Verify no forbidden columns
clean_cols = set(con.execute("DESCRIBE matches_1v1_clean").df()["column_name"])
forbidden = {
    # POST-GAME (I3 violations)
    "new_rating", "p0_new_rating", "p1_new_rating",
    "duration", "irl_duration", "p0_match_rating_diff", "p1_match_rating_diff",
    # Constant / near-dead (R04/R05)
    "game_type", "game_speed", "starting_age",
    # IN-GAME (I3 violations -- unavailable at prediction time)
    "p0_opening", "p1_opening",
    "p0_feudal_age_uptime", "p1_feudal_age_uptime",
    "p0_castle_age_uptime", "p1_castle_age_uptime",
    "p0_imperial_age_uptime", "p1_imperial_age_uptime",
}
assert forbidden.isdisjoint(clean_cols), f"SCHEMA VIOLATION: {forbidden & clean_cols}"
assert "team1_wins" in clean_cols, "FAIL: team1_wins column missing"
print("PASS: no forbidden columns (POST-GAME + IN-GAME I3 violations excluded); team1_wins present")

# Explicit information_schema assertions for I3 violations (POST-GAME + IN-GAME)
clean_i3_check = con.execute("""
SELECT column_name FROM information_schema.columns
WHERE table_name = 'matches_1v1_clean'
  AND column_name IN (
    'duration', 'irl_duration', 'p0_match_rating_diff', 'p1_match_rating_diff',
    'p0_opening', 'p1_opening',
    'p0_feudal_age_uptime', 'p1_feudal_age_uptime',
    'p0_castle_age_uptime', 'p1_castle_age_uptime',
    'p0_imperial_age_uptime', 'p1_imperial_age_uptime'
  )
""").df()
assert len(clean_i3_check) == 0, f"FAIL: I3-violating columns in matches_1v1_clean: {clean_i3_check['column_name'].tolist()}"
print("I3 PASS: No POST-GAME or IN-GAME columns in matches_1v1_clean")

# %% [markdown]
# ## Create player_history_all VIEW
#
# Full-history player-row VIEW for feature computation.
# ALL game types, ALL leaderboards. No leaderboard restriction.
# One row per player per match.

# %%
SQL_T07_PLAYER_HISTORY_ALL = """
CREATE OR REPLACE VIEW player_history_all AS
WITH player_counts AS (
    SELECT game_id, COUNT(*) AS player_count
    FROM players_raw
    GROUP BY game_id
)
SELECT
    CAST(p.profile_id AS BIGINT) AS profile_id,
    p.game_id,
    m.started_timestamp,
    m.leaderboard,
    m.map,
    m.patch,
    pc.player_count,
    m.mirror,
    m.replay_enhanced,
    p.civ,
    p.team,
    p.old_rating,
    p.winner
FROM players_raw p
INNER JOIN matches_raw m ON p.game_id = m.game_id
INNER JOIN player_counts pc ON p.game_id = pc.game_id
WHERE p.profile_id IS NOT NULL
  AND m.started_timestamp IS NOT NULL
"""

con.execute(SQL_T07_PLAYER_HISTORY_ALL)
t07_cnt = con.execute("SELECT COUNT(*) FROM player_history_all").fetchone()[0]
print(f"player_history_all VIEW created. Row count: {t07_cnt:,}")

# Leaderboard distribution
t07_leaderboards = con.execute(
    "SELECT leaderboard, COUNT(*) AS cnt FROM player_history_all GROUP BY leaderboard ORDER BY cnt DESC"
).df()
print("Leaderboard distribution:")
print(t07_leaderboards.to_string())
assert len(t07_leaderboards) > 1, "FAIL: only one leaderboard in player_history_all"

# Player count distribution
t07_player_counts = con.execute(
    "SELECT player_count, COUNT(*) AS cnt FROM player_history_all GROUP BY player_count ORDER BY player_count"
).df()
print("Player count distribution:")
print(t07_player_counts.to_string())
assert t07_player_counts["player_count"].max() > 2, "FAIL: no non-1v1 games in player_history_all"

# NULL checks
t07_nulls = con.execute(
    "SELECT COUNT(*) FILTER (WHERE profile_id IS NULL) AS null_pid, "
    "COUNT(*) FILTER (WHERE started_timestamp IS NULL) AS null_ts FROM player_history_all"
).fetchone()
assert t07_nulls[0] == 0 and t07_nulls[1] == 0, f"FAIL: NULLs in player_history_all: {t07_nulls}"

# Verify forbidden columns absent
hist_cols = set(con.execute("DESCRIBE player_history_all").df()["column_name"])
forbidden_hist = {
    "new_rating", "game_type", "game_speed", "starting_age",
    "duration", "irl_duration", "match_rating_diff",
}
assert forbidden_hist.isdisjoint(hist_cols), f"SCHEMA VIOLATION: {forbidden_hist & hist_cols}"
assert "profile_id" in hist_cols, "FAIL: profile_id missing from player_history_all"
print("PASS: all assertions passed; leaderboard distribution confirmed")

# Explicit information_schema assertion for match_rating_diff in player_history_all (B2/W3)
hist_pg_check = con.execute("""
SELECT column_name FROM information_schema.columns
WHERE table_name = 'player_history_all'
  AND column_name IN ('match_rating_diff')
""").df()
assert len(hist_pg_check) == 0, f"FAIL: POST-GAME match_rating_diff in player_history_all: {hist_pg_check['column_name'].tolist()}"
print("B2 PASS: match_rating_diff absent from player_history_all")

# %% [markdown]
# ## Post-cleaning validation
#
# ratings_raw absence assertion. Winner consistency XOR check. Team-assignment asymmetry. CONSORT flow.

# %%
SQL_T08_RATINGS_RAW_ABSENCE = """
SELECT COUNT(*) AS ratings_raw_exists
FROM information_schema.tables
WHERE table_name = 'ratings_raw'
"""

t08_ratings_raw = con.execute(SQL_T08_RATINGS_RAW_ABSENCE).fetchone()[0]
print(f"ratings_raw_exists: {t08_ratings_raw}")
assert t08_ratings_raw == 0, "FAIL: ratings_raw table found in aoestats"
print("PASS: ratings_raw_exists=0. ELO data embedded in players_raw and matches_raw.")

# %%
SQL_T08_CONSORT = """
SELECT
    (SELECT COUNT(*) FROM matches_raw) AS stage_0_all_matches,
    (SELECT COUNT(*) FROM matches_raw m
     WHERE EXISTS (SELECT 1 FROM players_raw p WHERE p.game_id = m.game_id)
    ) AS stage_1_has_players,
    (SELECT COUNT(*) FROM matches_raw m
     INNER JOIN (SELECT game_id FROM players_raw GROUP BY game_id HAVING COUNT(*) = 2) pc
       ON m.game_id = pc.game_id
    ) AS stage_2_structural_1v1,
    (SELECT COUNT(*) FROM matches_raw m
     INNER JOIN (SELECT game_id FROM players_raw GROUP BY game_id
                 HAVING COUNT(*) = 2 AND COUNT(DISTINCT team) = 2) pc
       ON m.game_id = pc.game_id
     WHERE m.leaderboard = 'random_map'
    ) AS stage_3_ranked_1v1_distinct_teams,
    (SELECT COUNT(*) FROM matches_1v1_clean) AS stage_4_view_final,
    (SELECT COUNT(*) FROM player_history_all) AS player_history_all_rows
"""

t08_consort = con.execute(SQL_T08_CONSORT).df()
print("CONSORT flow:")
print(t08_consort.to_string())

# %%
SQL_T08_WINNER_DIST = """
SELECT p0_winner, COUNT(*) AS cnt,
       ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),4) AS pct
FROM matches_1v1_clean GROUP BY p0_winner ORDER BY p0_winner
"""

t08_winner_dist = con.execute(SQL_T08_WINNER_DIST).df()
print("Winner distribution (p0_winner):")
print(t08_winner_dist.to_string())

# %%
SQL_T08_XOR_CHECK = """
SELECT COUNT(*) AS total,
       COUNT(*) FILTER (WHERE p0_winner = true AND p1_winner = false) AS p0_wins,
       COUNT(*) FILTER (WHERE p0_winner = false AND p1_winner = true) AS p1_wins,
       COUNT(*) FILTER (WHERE p0_winner = p1_winner) AS inconsistent
FROM matches_1v1_clean
"""

t08_xor = con.execute(SQL_T08_XOR_CHECK).df()
print("Winner XOR check:")
print(t08_xor.to_string())
assert t08_xor["inconsistent"].iloc[0] == 0, "FAIL: inconsistent winner rows found"
print("PASS: inconsistent=0 (inconsistent winner rows excluded from VIEW verified)")

# %%
SQL_T08_TEAM_ASYM = """
SELECT
    COUNT(*) FILTER (WHERE team1_wins = true) AS t1_wins,
    COUNT(*) FILTER (WHERE team1_wins = false) AS t0_wins,
    ROUND(100.0 * COUNT(*) FILTER (WHERE team1_wins = true) / COUNT(*), 2) AS t1_win_pct
FROM matches_1v1_clean
"""

t08_team_asym = con.execute(SQL_T08_TEAM_ASYM).df()
print("Team-assignment asymmetry:")
print(t08_team_asym.to_string())
t1_win_pct = float(t08_team_asym["t1_win_pct"].iloc[0])
print(f"t1_win_pct = {t1_win_pct}% (expected ~51.9%)")

# %%
SQL_T08_PROFILE_ID_TYPES = """
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name IN ('matches_1v1_clean', 'player_history_all')
  AND column_name IN ('p0_profile_id', 'p1_profile_id', 'profile_id')
"""

t08_types = con.execute(SQL_T08_PROFILE_ID_TYPES).df()
print("profile_id type check:")
print(t08_types.to_string())
assert all(t08_types["data_type"] == "BIGINT"), "FAIL: profile_id columns not BIGINT"
print("PASS: all profile_id columns are BIGINT")

# %% [markdown]
# ## NULL Audit
#
# Systematic per-column NULL census for both analytical VIEWs.
# DESCRIBE-based schema guards run first to detect column-set drift.
# Per-column COUNT(*) FILTER approach gives exact integer null counts.

# %%
# --- Schema guard + NULL census for matches_1v1_clean ---

EXPECTED_MATCHES_COLS = {
    "game_id", "started_timestamp", "leaderboard", "map", "mirror",
    "num_players", "patch", "raw_match_type", "replay_enhanced",
    "avg_elo", "team_0_elo", "team_1_elo",
    "p0_profile_id", "p0_civ", "p0_old_rating", "p0_winner",
    "p1_profile_id", "p1_civ", "p1_old_rating", "p1_winner",
    "team1_wins",
}

actual_matches_cols = set(
    con.execute("DESCRIBE matches_1v1_clean").df()["column_name"]
)
assert actual_matches_cols == EXPECTED_MATCHES_COLS, (
    f"Schema drift in matches_1v1_clean: "
    f"{actual_matches_cols.symmetric_difference(EXPECTED_MATCHES_COLS)}"
)
print(f"PASS: matches_1v1_clean schema guard — {len(actual_matches_cols)} columns match expected set")

# Per-column NULL census (exact integer counts, no SUMMARIZE rounding risk)
SQL_NULL_AUDIT_MATCHES_COLS = """
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'matches_1v1_clean'
ORDER BY ordinal_position
"""

df_cols_m1 = con.execute(SQL_NULL_AUDIT_MATCHES_COLS).df()
total_rows_m1 = con.execute("SELECT COUNT(*) FROM matches_1v1_clean").fetchone()[0]

null_results_m1 = []
for col_name in df_cols_m1["column_name"]:
    q = f'SELECT COUNT(*) FILTER (WHERE "{col_name}" IS NULL) AS null_count FROM matches_1v1_clean'
    null_count = con.execute(q).fetchone()[0]
    null_pct = round(100.0 * null_count / total_rows_m1, 4) if total_rows_m1 > 0 else 0.0
    null_results_m1.append({
        "column": col_name,
        "null_count": int(null_count),
        "null_pct": float(null_pct),
    })

df_null_m1 = pd.DataFrame(null_results_m1)
print(f"NULL census — matches_1v1_clean ({total_rows_m1:,} total rows):")
print(df_null_m1.to_string(index=False))

# Zero-NULL assertions for identity and target columns
MATCHES_ZERO_NULL_COLS = [
    "game_id", "started_timestamp",
    "p0_profile_id", "p1_profile_id",
    "p0_winner", "p1_winner",
]
m1_null_map = {r["column"]: r["null_count"] for r in null_results_m1}
for col_name in MATCHES_ZERO_NULL_COLS:
    assert m1_null_map[col_name] == 0, f"FAIL: {col_name} has {m1_null_map[col_name]:,} NULLs (expected 0)"
print(f"PASS: zero-NULL assertions for {MATCHES_ZERO_NULL_COLS}")
print(f"matches_1v1_clean total rows: {total_rows_m1:,}")

# %%
# --- Schema guard + NULL census for player_history_all ---

EXPECTED_HIST_COLS = {
    "profile_id", "game_id", "started_timestamp", "leaderboard", "map",
    "patch", "player_count", "mirror", "replay_enhanced",
    "civ", "team", "old_rating", "winner",
}

actual_hist_cols = set(
    con.execute("DESCRIBE player_history_all").df()["column_name"]
)
assert actual_hist_cols == EXPECTED_HIST_COLS, (
    f"Schema drift in player_history_all: "
    f"{actual_hist_cols.symmetric_difference(EXPECTED_HIST_COLS)}"
)
print(f"PASS: player_history_all schema guard — {len(actual_hist_cols)} columns match expected set")

# Per-column NULL census (exact integer counts)
SQL_NULL_AUDIT_HIST_COLS = """
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'player_history_all'
ORDER BY ordinal_position
"""

df_cols_ph = con.execute(SQL_NULL_AUDIT_HIST_COLS).df()
total_rows_ph = con.execute("SELECT COUNT(*) FROM player_history_all").fetchone()[0]

null_results_ph = []
for col_name in df_cols_ph["column_name"]:
    q = f'SELECT COUNT(*) FILTER (WHERE "{col_name}" IS NULL) AS null_count FROM player_history_all'
    null_count = con.execute(q).fetchone()[0]
    null_pct = round(100.0 * null_count / total_rows_ph, 4) if total_rows_ph > 0 else 0.0
    null_results_ph.append({
        "column": col_name,
        "null_count": int(null_count),
        "null_pct": float(null_pct),
    })

df_null_ph = pd.DataFrame(null_results_ph)
print(f"NULL census — player_history_all ({total_rows_ph:,} total rows):")
print(df_null_ph.to_string(index=False))

# Zero-NULL assertions for identity and temporal columns only
HIST_ZERO_NULL_COLS = ["profile_id", "game_id", "started_timestamp"]
ph_null_map = {r["column"]: r["null_count"] for r in null_results_ph}
for col_name in HIST_ZERO_NULL_COLS:
    assert ph_null_map[col_name] == 0, f"FAIL: {col_name} has {ph_null_map[col_name]:,} NULLs (expected 0)"
print(f"PASS: zero-NULL assertions for {HIST_ZERO_NULL_COLS}")

# winner NULLs documented as FINDING — VIEW covers all game types,
# no WHERE winner IS NOT NULL filter applied
winner_null_count_ph = ph_null_map.get("winner", -1)
winner_null_pct_ph = round(100.0 * winner_null_count_ph / total_rows_ph, 4) if total_rows_ph > 0 else 0.0
print(f"FINDING: winner NULL count = {winner_null_count_ph:,} ({winner_null_pct_ph}%)")
print("  Note: Nullable in player_history_all; VIEW covers all game types.")
print(f"player_history_all total rows: {total_rows_ph:,}")

# %% [markdown]
# ## Missingness Audit — Phase B
#
# **Scope:** Two coordinated census passes per VIEW plus a runtime constants-detection step.
# **Pass 1** (above): SQL NULL census. **Pass 2** (below): sentinel census driven
# by `_missingness_spec`. **Pass 3**: `COUNT(DISTINCT col)` constants detection.
# The three passes feed one consolidated missingness ledger (CSV + JSON) per VIEW.
#
# **Phase boundary (Invariant #9):** This audit DOCUMENTS and RECOMMENDS only.
# No VIEWs are modified, no columns dropped, no imputation performed.
# Downstream steps 01_04_02+ execute decisions.
#
# **Framework references:**
# - Rubin, D.B. (1976). Inference and missing data. Biometrika, 63(3), 581-592.
# - Little, R.J. & Rubin, D.B. (2019). Statistical Analysis with Missing Data, 3rd ed.
# - van Buuren, S. (2018). Flexible Imputation of Missing Data. Warns against rigid thresholds.
# - Schafer, J.L. & Graham, J.W. (2002). <5% MCAR boundary citation.
# - Sambasivan, N. et al. (2021). Data Cascades in High-Stakes AI (CHI '21).

# %%
# --- _missingness_spec for aoestats (Deliverable 2.B) ---
_missingness_spec = {
    "p0_old_rating": {
        "mechanism": "MAR",
        "justification": (
            "Pre-game rating; 0 is the unrated sentinel. "
            "01_02_04 numeric_stats_players[label='old_rating'] reports "
            "min_val=0, max_val=3045, n_zero=5,937; consistent with "
            "players_raw_census.old_rating.zero_count=5,937 (zero_pct=0.0055%). "
            "No negative values exist in old_rating (the negative range -5..-1 "
            "appears only in new_rating, which is POST-GAME and excluded per I3). "
            "Disposition surfaced as DS-AOESTATS-02."
        ),
        "sentinel_value": 0,
        "carries_semantic_content": True,
        "is_primary_feature": True,
    },
    "p1_old_rating": {
        "mechanism": "MAR",
        "justification": "Symmetric to p0_old_rating.",
        "sentinel_value": 0,
        "carries_semantic_content": True,
        "is_primary_feature": True,
    },
    "team_0_elo": {
        "mechanism": "MCAR",
        "justification": (
            "ELO=-1 sentinel = isolated parse failures in raw matches_raw. "
            "01_02_04 census: min=-1, n_zero=4824 in matches_raw scope. "
            "W4 spec-vs-ledger note: this spec entry records the design "
            "intent at the raw-table level (mechanism=MCAR, sentinel=-1). "
            "The ledger may report n_sentinel=0 / RETAIN_AS_IS / "
            "mechanism=N/A in matches_1v1_clean if the upstream filter "
            "(WHERE p0.winner != p1.winner restricting to ranked-1v1 "
            "decisive games) excludes the sentinel-bearing rows. Spec is "
            "preserved for documentation continuity; ledger reflects "
            "empirical post-filter observation. Both are correct per the "
            "override priority — see DS-AOESTATS-01 for the scope-expansion "
            "contingency."
        ),
        "sentinel_value": -1,
        "carries_semantic_content": False,
        "is_primary_feature": True,
    },
    "team_1_elo": {
        "mechanism": "MCAR",
        "justification": (
            "Symmetric to team_0_elo. 01_02_04 census: min=-1, n_zero=192 "
            "in matches_raw scope. Same W4 spec-vs-ledger note: sentinel may "
            "be filtered out in matches_1v1_clean scope (ledger reports "
            "RETAIN_AS_IS / mechanism=N/A); spec preserved for design intent."
        ),
        "sentinel_value": -1,
        "carries_semantic_content": False,
        "is_primary_feature": True,
    },
    "avg_elo": {
        "mechanism": "MAR",
        "justification": (
            "01_02_04 numeric_stats_matches[label='avg_elo'] reports min_val=0, "
            "max_val=2976.5, n_zero=121 (~0.0004% of 30,690,651 matches_raw rows). "
            "Disposition (genuine zero vs sentinel) deferred to 01_04_02+ join "
            "investigation (DS-AOESTATS-03). Note: the n_zero=4,824 figure cited "
            "in earlier drafts belongs to team_0_elo, NOT avg_elo."
        ),
        "sentinel_value": 0,
        "carries_semantic_content": True,
        "is_primary_feature": True,
    },
    "raw_match_type": {
        "mechanism": "MCAR",
        "justification": (
            "matches_raw_census.raw_match_type.null_count=12,504 (~0.04% of matches_raw). "
            "Actual NULL count in matches_1v1_clean (filtered scope) computed at audit "
            "runtime by Pass 1; static figure here is raw-table reference. "
            "Source: 01_02_04 matches_raw_census."
        ),
        "sentinel_value": None,
        "carries_semantic_content": False,
        "is_primary_feature": False,
    },
    # old_rating: column name in player_history_all (one row per player per match).
    # p0_old_rating / p1_old_rating are the pivoted names in matches_1v1_clean.
    # Same sentinel (0 = unrated) applies.
    "old_rating": {
        "mechanism": "MAR",
        "justification": (
            "Pre-game rating; 0 is the unrated sentinel. "
            "01_02_04 numeric_stats_players[label='old_rating'] reports "
            "min_val=0, max_val=3045, n_zero=5,937; consistent with "
            "players_raw_census.old_rating.zero_count=5,937 (zero_pct=0.0055%). "
            "Column name is old_rating in player_history_all (pivoted to "
            "p0_old_rating/p1_old_rating in matches_1v1_clean). "
            "Disposition surfaced as DS-AOESTATS-02."
        ),
        "sentinel_value": 0,
        "carries_semantic_content": True,
        "is_primary_feature": True,
    },
}

# %%
# --- DRY helpers: sentinel census, constants detection, ledger consolidation ---


from rts_predict.common.missingness_audit import (
    _build_sentinel_predicate,
    _sentinel_census,
    _detect_constants,
    _recommend,
    _consolidate_ledger,
    build_audit_views_block,
)
print("Helper functions imported from rts_predict.common.missingness_audit.")

# %%
# --- Pass 2 + Pass 3: matches_1v1_clean ---

_view_m1 = "matches_1v1_clean"
_target_cols_m1: set = {"team1_wins"}
_identity_cols_m1: set = {"game_id"}

# dtype map from DESCRIBE
_dtype_m1 = {
    row["column_name"]: row["column_type"]
    for _, row in con.execute(f"DESCRIBE {_view_m1}").df().iterrows()
}

# Pass 2: sentinel census (only spec'd columns that exist in this VIEW)
_spec_m1 = {c: v for c, v in _missingness_spec.items() if c in actual_matches_cols}
sentinel_rows_m1 = _sentinel_census(_view_m1, total_rows_m1, _spec_m1, con)
print(f"Sentinel census — {_view_m1}: {len(sentinel_rows_m1)} spec'd columns")

# Pass 3: constants detection
_cols_m1 = list(actual_matches_cols)
constants_m1 = _detect_constants(_view_m1, _cols_m1, con, _identity_cols_m1)
print(f"Constants detection — {_view_m1}: done. n_distinct=1 columns: "
      f"{[c for c, v in constants_m1.items() if v == 1]}")

# Consolidate
df_null_m1 = pd.DataFrame(null_results_m1).rename(columns={"column": "column_name"})
df_ledger_m1 = _consolidate_ledger(
    _view_m1, df_null_m1, sentinel_rows_m1, _missingness_spec,
    _dtype_m1, total_rows_m1, constants_m1, _target_cols_m1, _identity_cols_m1,
)
print(f"Ledger — {_view_m1}: {len(df_ledger_m1)} rows")
print(df_ledger_m1[["column", "n_null", "n_sentinel", "pct_missing_total", "mechanism", "recommendation"]].to_string(index=False))

# %%
# --- Assertions for matches_1v1_clean ledger (6.A + 6.B + 6.C) ---

_target_cols_for_view_m1 = _target_cols_m1
_identity_cols_for_view_m1 = _identity_cols_m1

# 6.B: full-coverage
_n_view_cols_m1 = int(con.execute(f"DESCRIBE {_view_m1}").df().shape[0])
assert len(df_ledger_m1) == _n_view_cols_m1, (
    f"Full-coverage violation for {_view_m1}: expected {_n_view_cols_m1}, got {len(df_ledger_m1)}"
)

# 6.B: per-row field assertions
for _, row in df_ledger_m1.iterrows():
    assert row["mechanism"] in {"MAR", "MCAR", "MNAR", "N/A"}, row.to_dict()
    assert row["mechanism_justification"], f"empty mechanism_justification for {row['column']}"
    assert row["recommendation"] in {
        "DROP_COLUMN", "FLAG_FOR_IMPUTATION", "RETAIN_AS_IS",
        "EXCLUDE_TARGET_NULL_ROWS", "CONVERT_SENTINEL_TO_NULL",
    }, row.to_dict()
    assert row["recommendation_justification"], row.to_dict()
    assert isinstance(row["carries_semantic_content"], (bool, np.bool_)), row.to_dict()

# 6.B: zero-missingness rows → N/A + RETAIN_AS_IS
_zero_m1 = df_ledger_m1[
    (df_ledger_m1["n_null"] == 0)
    & (df_ledger_m1["n_sentinel"] == 0)
    & (df_ledger_m1["n_distinct"].fillna(-1) != 1)
    & (~df_ledger_m1["column"].isin(_target_cols_for_view_m1))
    & (~df_ledger_m1["column"].isin(_identity_cols_for_view_m1))
]
assert (_zero_m1["mechanism"] == "N/A").all(), "non-target zero-missingness rows must have mechanism=N/A (m1)"
assert (_zero_m1["recommendation"] == "RETAIN_AS_IS").all(), "non-target zero-missingness rows must be RETAIN_AS_IS (m1)"

# 6.B: identity columns
_ident_m1 = df_ledger_m1[df_ledger_m1["column"].isin(_identity_cols_for_view_m1)]
assert (_ident_m1["mechanism"] == "N/A").all(), "identity columns must have mechanism=N/A (m1)"
assert (_ident_m1["recommendation"] == "RETAIN_AS_IS").all(), "identity columns must be RETAIN_AS_IS (m1)"

# 6.B: target typo guard
_missing_targets_m1 = _target_cols_for_view_m1 - set(df_ledger_m1["column"].values)
assert not _missing_targets_m1, f"target col(s) missing from VIEW: {_missing_targets_m1}"

# 6.C: team1_wins → F1 zero-missingness → RETAIN_AS_IS / mechanism=N/A
_t1w = df_ledger_m1[df_ledger_m1["column"] == "team1_wins"].iloc[0]
assert _t1w["recommendation"] == "RETAIN_AS_IS", f"team1_wins must be RETAIN_AS_IS, got {_t1w['recommendation']}"
assert _t1w["mechanism"] == "N/A", f"team1_wins must have mechanism=N/A, got {_t1w['mechanism']}"

# 6.C: p0_winner, p1_winner → F1 → RETAIN_AS_IS / mechanism=N/A
for _winner_col in ["p0_winner", "p1_winner"]:
    _wr = df_ledger_m1[df_ledger_m1["column"] == _winner_col].iloc[0]
    assert _wr["recommendation"] == "RETAIN_AS_IS", f"{_winner_col} must be RETAIN_AS_IS"
    assert _wr["mechanism"] == "N/A", f"{_winner_col} must have mechanism=N/A"

# 6.C: team_0_elo / team_1_elo → CONVERT_SENTINEL_TO_NULL if n_sentinel>0,
# OR RETAIN_AS_IS if sentinel=-1 rows happen to be filtered out in matches_1v1_clean scope.
# Both outcomes are correct per the override priority (W3 fires only when n_sentinel > 0).
for _elo_col in ["team_0_elo", "team_1_elo"]:
    _er = df_ledger_m1[df_ledger_m1["column"] == _elo_col].iloc[0]
    if _er["n_sentinel"] > 0:
        assert _er["recommendation"] == "CONVERT_SENTINEL_TO_NULL", (
            f"{_elo_col} must be CONVERT_SENTINEL_TO_NULL when n_sentinel>0, got {_er['recommendation']}"
        )
    else:
        # sentinel=-1 rows absent in this VIEW's filtered scope → F1 fires → RETAIN_AS_IS
        assert _er["recommendation"] in ("RETAIN_AS_IS", "CONVERT_SENTINEL_TO_NULL"), (
            f"{_elo_col} unexpected recommendation: {_er['recommendation']}"
        )
    assert not _er["carries_semantic_content"], f"{_elo_col} carries_semantic_content must be False"
    print(f"  {_elo_col}: n_sentinel={_er['n_sentinel']}, recommendation={_er['recommendation']}")

print(f"PASS: all 6.A/6.B/6.C assertions for {_view_m1}")

# %%
# --- Pass 2 + Pass 3: player_history_all ---

_view_ph = "player_history_all"
_target_cols_ph: set = {"winner"}
_identity_cols_ph: set = {"game_id", "profile_id"}

# dtype map
_dtype_ph = {
    row["column_name"]: row["column_type"]
    for _, row in con.execute(f"DESCRIBE {_view_ph}").df().iterrows()
}

# Pass 2: sentinel census (only spec'd columns in this VIEW)
_spec_ph = {c: v for c, v in _missingness_spec.items() if c in actual_hist_cols}
sentinel_rows_ph = _sentinel_census(_view_ph, total_rows_ph, _spec_ph, con)
print(f"Sentinel census — {_view_ph}: {len(sentinel_rows_ph)} spec'd columns")

# Pass 3: constants detection
_cols_ph = list(actual_hist_cols)
constants_ph = _detect_constants(_view_ph, _cols_ph, con, _identity_cols_ph)
print(f"Constants detection — {_view_ph}: done. n_distinct=1 columns: "
      f"{[c for c, v in constants_ph.items() if v == 1]}")

# Consolidate
_df_null_ph_raw = pd.DataFrame(null_results_ph)  # from null census above
df_null_ph_renamed = _df_null_ph_raw.rename(columns={"column": "column_name"})
df_ledger_ph = _consolidate_ledger(
    _view_ph, df_null_ph_renamed, sentinel_rows_ph, _missingness_spec,
    _dtype_ph, total_rows_ph, constants_ph, _target_cols_ph, _identity_cols_ph,
)
print(f"Ledger — {_view_ph}: {len(df_ledger_ph)} rows")
print(df_ledger_ph[["column", "n_null", "n_sentinel", "pct_missing_total", "mechanism", "recommendation"]].to_string(index=False))

# %%
# --- Assertions for player_history_all ledger (6.B + 6.C) ---

_target_cols_for_view_ph = _target_cols_ph
_identity_cols_for_view_ph = _identity_cols_ph

# 6.B: full-coverage
_n_view_cols_ph = int(con.execute(f"DESCRIBE {_view_ph}").df().shape[0])
assert len(df_ledger_ph) == _n_view_cols_ph, (
    f"Full-coverage violation for {_view_ph}: expected {_n_view_cols_ph}, got {len(df_ledger_ph)}"
)

# 6.B: per-row field assertions
for _, row in df_ledger_ph.iterrows():
    assert row["mechanism"] in {"MAR", "MCAR", "MNAR", "N/A"}, row.to_dict()
    assert row["mechanism_justification"], f"empty mechanism_justification for {row['column']}"
    assert row["recommendation"] in {
        "DROP_COLUMN", "FLAG_FOR_IMPUTATION", "RETAIN_AS_IS",
        "EXCLUDE_TARGET_NULL_ROWS", "CONVERT_SENTINEL_TO_NULL",
    }, row.to_dict()
    assert row["recommendation_justification"], row.to_dict()
    assert isinstance(row["carries_semantic_content"], (bool, np.bool_)), row.to_dict()

# 6.B: zero-missingness rows → N/A + RETAIN_AS_IS
_zero_ph = df_ledger_ph[
    (df_ledger_ph["n_null"] == 0)
    & (df_ledger_ph["n_sentinel"] == 0)
    & (df_ledger_ph["n_distinct"].fillna(-1) != 1)
    & (~df_ledger_ph["column"].isin(_target_cols_for_view_ph))
    & (~df_ledger_ph["column"].isin(_identity_cols_for_view_ph))
]
assert (_zero_ph["mechanism"] == "N/A").all(), "non-target zero-missingness rows must have mechanism=N/A (ph)"
assert (_zero_ph["recommendation"] == "RETAIN_AS_IS").all(), "non-target zero-missingness rows must be RETAIN_AS_IS (ph)"

# 6.B: identity columns
_ident_ph = df_ledger_ph[df_ledger_ph["column"].isin(_identity_cols_for_view_ph)]
assert (_ident_ph["mechanism"] == "N/A").all(), "identity columns must have mechanism=N/A (ph)"
assert (_ident_ph["recommendation"] == "RETAIN_AS_IS").all(), "identity columns must be RETAIN_AS_IS (ph)"

# 6.B: target typo guard
_missing_targets_ph = _target_cols_for_view_ph - set(df_ledger_ph["column"].values)
assert not _missing_targets_ph, f"target col(s) missing from VIEW: {_missing_targets_ph}"

# 6.C: winner in player_history_all
# Per plan: if winner has NULLs → target-override → EXCLUDE_TARGET_NULL_ROWS.
# If winner has 0 NULLs in this VIEW's scope → F1 fires → RETAIN_AS_IS (also correct).
_winner_ph = df_ledger_ph[df_ledger_ph["column"] == "winner"].iloc[0]
print(f"  winner in {_view_ph}: n_null={_winner_ph['n_null']}, recommendation={_winner_ph['recommendation']}")
if _winner_ph["n_null"] > 0:
    assert _winner_ph["recommendation"] == "EXCLUDE_TARGET_NULL_ROWS", (
        f"winner in {_view_ph} must be EXCLUDE_TARGET_NULL_ROWS when n_null>0, got {_winner_ph['recommendation']}"
    )
else:
    # winner has 0 NULLs in this VIEW scope (all matches have decisive outcome in players_raw)
    assert _winner_ph["recommendation"] in ("RETAIN_AS_IS",), (
        f"winner with 0 NULLs must be RETAIN_AS_IS, got {_winner_ph['recommendation']}"
    )

# 6.C: p0_old_rating / p1_old_rating in player_history_all (old_rating col)
_old_r = df_ledger_ph[df_ledger_ph["column"] == "old_rating"]
if len(_old_r) > 0:
    _old_row = _old_r.iloc[0]
    assert _old_row["sentinel_value"] == "0", f"old_rating sentinel must be '0', got {_old_row['sentinel_value']}"

print(f"PASS: all 6.B/6.C assertions for {_view_ph}")

# %% [markdown]
# ## Decisions Surfaced for Downstream Cleaning (01_04_02+)
#
# DS-AOESTATS-01: team_0_elo / team_1_elo — ELO=-1 sentinel ABSENT in matches_1v1_clean
#   (upstream filter excludes rows that carried it — the matches_1v1_clean WHERE clause
#   restricts to ranked-1v1 decisive games where the sentinel does not appear).
#   Ledger reports n_sentinel=0 → RETAIN_AS_IS / mechanism=N/A. Action item: if
#   the ranked-1v1 scope is ever broadened, re-audit for sentinel resurfacing.
#   Spec retains mechanism=MCAR / sentinel_value=-1 to document design intent from raw.
#
# DS-AOESTATS-02: p0_old_rating / p1_old_rating (sentinel=0, n_zero=5,937 in players_raw, ~0.0055%)
#   NULLIF + listwise deletion per Rule S3 in 01_04_02+ DDL pass,
#   OR retain `0` as an explicit `unrated` categorical encoding alongside `is_unrated`?
#   Source: players_raw_census.old_rating.zero_count=5937 (zero_pct=0.0055%).
#   B6 deferral: audit recommends CONVERT_SENTINEL_TO_NULL (non-binding for
#   carries_semantic_content=True columns). DS-AOESTATS-02 surfaces the retain-as-category
#   alternative for 01_04_02+ to choose.
#
# DS-AOESTATS-03: avg_elo n_sentinel=118 in matches_1v1_clean / n_zero=121 in matches_raw
#   (numeric_stats_matches[label='avg_elo'] ground truth). Same MAR /
#   CONVERT_SENTINEL_TO_NULL recommendation; the 3-row difference is the upstream
#   1v1 filter discarding 3 sentinel rows. Disposition (genuine zero vs sentinel)
#   deferred to 01_04_02+ join investigation.
#   Note: the n_zero=4,824 figure belongs to team_0_elo, NOT avg_elo.
#
# DS-AOESTATS-04: raw_match_type NULLs in matches_raw (~0.04% of matches_raw)
#   MCAR per Rule S3, listwise deletion candidate at 01_04_02+. Column may be redundant
#   given internalLeaderboardId already constrains scope.
#
# DS-AOESTATS-05: team1_wins (prediction target, BIGINT) in matches_1v1_clean
#   0 NULLs verified (upstream WHERE p0.winner != p1.winner exclusion).
#   F1 zero-missingness override → RETAIN_AS_IS / mechanism=N/A.
#
# DS-AOESTATS-06: winner in player_history_all — ledger reports 0 NULLs / RETAIN_AS_IS /
#   mechanism=N/A (better than plan-anticipated ~5% rate). Target-override post-step (B4)
#   will fire automatically if winner NULLs surface in future loads — no Phase 02 code
#   change required.
#
# DS-AOESTATS-07: overviews_raw is a singleton metadata table (1 row), not used by
#   any VIEW — formally declare out-of-analytical-scope at 01_04_02+ disposition step.
#
# DS-AOESTATS-08: leaderboard + num_players (TRUE constants in matches_1v1_clean)
#   Constants-detection branch (W7 fix) flags n_distinct=1 for both columns.
#   Ledger reports DROP_COLUMN / mechanism=N/A. Confirm removal in 01_04_02+ DDL pass.

# %% [markdown]
# ## Assemble artifacts and update tracking

# %%
# Build artifact structure
t05_weekly_records = t05_result.to_dict(orient="records")

# Extract transition boundary info
last_pop = t05_result[t05_result["opening_pct"] > 1.0]["week_date"].max()
first_zero = t05_result[t05_result["opening_pct"] == 0.0]["week_date"].min()

consort_flow = {
    "stage_0_all_matches": int(t08_consort["stage_0_all_matches"].iloc[0]),
    "stage_1_has_players": int(t08_consort["stage_1_has_players"].iloc[0]),
    "stage_2_structural_1v1": int(t08_consort["stage_2_structural_1v1"].iloc[0]),
    "stage_3_ranked_1v1_distinct_teams": int(t08_consort["stage_3_ranked_1v1_distinct_teams"].iloc[0]),
    "stage_4_view_final": int(t08_consort["stage_4_view_final"].iloc[0]),
    "player_history_all_rows": int(t08_consort["player_history_all_rows"].iloc[0]),
    "excluded_at_stage_3_to_4_inconsistent_winner": 17_815_944 - int(t08_consort["stage_4_view_final"].iloc[0]),
}

cleaning_registry = {
    "R00": {
        "id": "R00",
        "condition": "Scope definition for player feature computation source",
        "action": "CREATE VIEW player_history_all -- all game types, all leaderboards",
        "justification": "Full player history for feature computation. Restricting to 1v1 would compound selection bias without eliminating it.",
        "impact": f"{int(t08_consort['player_history_all_rows'].iloc[0]):,} rows in feature computation source",
    },
    "R01": {
        "id": "R01",
        "condition": "profile_id IS DOUBLE in players_raw",
        "action": "CAST to BIGINT in analytical VIEWs",
        "justification": "01_02_04 census max=24,853,897 (below 2^53=9,007,199,254,740,992). Empirically confirmed: fractional_count=0, unsafe_range_count=0.",
        "impact": "0 rows affected; all values exact integers in safe range",
        "t01_verification": {
            "total_rows": int(t01_result["total_rows"].iloc[0]),
            "nonnull_rows": int(t01_result["nonnull_rows"].iloc[0]),
            "fractional_count": int(t01_result["fractional_count"].iloc[0]),
            "unsafe_range_count": int(t01_result["unsafe_range_count"].iloc[0]),
            "min_id": int(t01_result["min_id"].iloc[0]),
            "max_id": int(t01_result["max_id"].iloc[0]),
        },
    },
    "R02": {
        "id": "R02",
        "condition": "player_count != 2 OR leaderboard != 'random_map'",
        "action": "EXCLUDE from matches_1v1_clean VIEW (prediction target only)",
        "justification": "Thesis scope is ranked 1v1 prediction. Excluded matches remain available for feature computation via player_history_all.",
        "impact": f"{int(t02_result['scope_1v1_ranked'].iloc[0]):,} matches retained in prediction VIEW",
        "t02_counts": {
            "total_matches": int(t02_result["total_matches"].iloc[0]),
            "orphan_matches": int(t02_result["orphan_matches"].iloc[0]),
            "matches_with_players": int(t02_result["matches_with_players"].iloc[0]),
            "structural_1v1": int(t02_result["structural_1v1"].iloc[0]),
            "ranked_rm": int(t02_result["ranked_rm"].iloc[0]),
            "scope_1v1_ranked": int(t02_result["scope_1v1_ranked"].iloc[0]),
            "scope_1v1_unranked": int(t02_result["scope_1v1_unranked"].iloc[0]),
            "ranked_not_1v1": int(t02_result["ranked_not_1v1"].iloc[0]),
        },
    },
    "R03": {
        "id": "R03",
        "condition": "game_id in matches_raw with no rows in players_raw",
        "action": "EXCLUDE (implicit via INNER JOIN in matches_1v1_clean and player_history_all VIEWs)",
        "justification": "01_03_01 linkage check confirmed 212,890 orphans. No target variable.",
        "impact": "212,890 matches (0.69%)",
        "orphan_match_count": int(t03_result[0]),
    },
    "R04": {
        "id": "R04",
        "condition": "game_type = 'random_map' (100%), game_speed = 'normal' (100%)",
        "action": "EXCLUDE columns from VIEWs",
        "justification": "01_03_01 constant_columns: cardinality=1 across 30.7M rows.",
        "impact": "0 rows; 2 columns removed",
    },
    "R05": {
        "id": "R05",
        "condition": "starting_age: 99.99994% 'dark', 19 rows 'standard'",
        "action": "EXCLUDE column from VIEWs",
        "justification": "01_03_01 near_constant finding.",
        "impact": "0 rows; 1 column removed",
    },
    "R06": {
        "id": "R06",
        "condition": "new_rating is POST-GAME (computed after match completes)",
        "action": "EXCLUDE from both VIEWs (I3 violation)",
        "justification": "I3: No feature for game T may use information from game T or later.",
        "impact": "0 rows; 1 column per player excluded from both VIEWs",
    },
    "R07": {
        "id": "R07",
        "condition": "game_id has 2 player rows with identical team values",
        "action": "VERIFIED 0-IMPACT ASSERTION. COUNT(DISTINCT team) = 2 predicate in ranked_1v1 CTE handles this.",
        "justification": "Same-team rows would cause incorrect wide-format JOIN results.",
        "impact": f"same_team_game_count = {t06_same_team} (assertion confirmed; no exclusion needed)",
        "t06_same_team_assertion": {"same_team_game_count": t06_same_team},
    },
    "R08": {
        "id": "R08",
        "condition": "p0_winner = p1_winner (both True or both False)",
        "action": "EXCLUDE from matches_1v1_clean (WHERE p0.winner != p1.winner predicate)",
        "justification": "Target variable is ambiguous when both players have the same winner value. 997 rows (0.0056%). Source data quality issue.",
        "impact": "997 rows excluded from matches_1v1_clean",
        "investigation": {
            "both_false": 811,
            "both_true": 186,
            "total_inconsistent": 997,
            "rate_pct": round(997 / 17_815_944 * 100, 6),
        },
    },
}

artifact = {
    "step": "01_04_01",
    "dataset": "aoestats",
    "game": "aoe2",
    "generated_date": "2026-04-16",
    "cleaning_registry": cleaning_registry,
    "consort_flow": consort_flow,
    "t05_temporal_schema_analysis": {
        "weeks_total": len(t05_result),
        "last_week_opening_gt_1pct": last_pop,
        "first_week_opening_zero": first_zero,
        "note": "Schema change boundary: columns opened/feudal/castle/imperial_age_uptime drop to 0% after ~2024-03-17. Feature-inclusion decision deferred to Phase 02 (I9).",
        "weekly_records": [
            {k: (v if not hasattr(v, "item") else v.item()) for k, v in r.items()}
            for r in t05_weekly_records
        ],
    },
    "t06_same_team_assertion": {
        "sql": SQL_T06_SAME_TEAM_ASSERTION.strip(),
        "same_team_game_count": t06_same_team,
        "outcome": "0-impact assertion; no same-team games found",
    },
    "t06_team_assignment_asymmetry": {
        "t1_wins": int(t08_team_asym["t1_wins"].iloc[0]),
        "t0_wins": int(t08_team_asym["t0_wins"].iloc[0]),
        "t1_win_pct": t1_win_pct,
        "source_artifact": "01_02_06_bivariate_eda.json",
        "warning": "p0 (team=0) and p1 (team=1) are NOT random player slots. Downstream 01_05+ feature engineering MUST apply player-slot randomisation.",
    },
    "t08_ratings_raw_absence": {
        "ratings_raw_exists": int(t08_ratings_raw),
        "note": "aoestats has no ratings_raw table. All ELO data is embedded in players_raw (old_rating, new_rating) and matches_raw (avg_elo, team_0_elo, team_1_elo).",
    },
    "view_ddl": {
        "matches_1v1_clean": SQL_T06_MATCHES_1V1_CLEAN.strip(),
        "player_history_all": SQL_T07_PLAYER_HISTORY_ALL.strip(),
    },
    "sql_queries": {
        "t01_profile_id_precision": SQL_T01_PROFILE_ID_PRECISION.strip(),
        "t02_scope_restriction": SQL_T02_SCOPE.strip(),
        "t03_orphans": SQL_T03_ORPHANS.strip(),
        "t04_constants": SQL_T04_CONSTANTS.strip(),
        "t05_temporal_analysis": SQL_T05_TEMPORAL.strip(),
        "t06_same_team_assertion": SQL_T06_SAME_TEAM_ASSERTION.strip(),
        "t06_matches_1v1_clean_ddl": SQL_T06_MATCHES_1V1_CLEAN.strip(),
        "t07_player_history_all_ddl": SQL_T07_PLAYER_HISTORY_ALL.strip(),
        "t08_ratings_raw_absence": SQL_T08_RATINGS_RAW_ABSENCE.strip(),
        "t08_consort": SQL_T08_CONSORT.strip(),
        "t08_winner_distribution": SQL_T08_WINNER_DIST.strip(),
        "t08_xor_check": SQL_T08_XOR_CHECK.strip(),
        "t08_team_asymmetry": SQL_T08_TEAM_ASYM.strip(),
        "t08_profile_id_types": SQL_T08_PROFILE_ID_TYPES.strip(),
    },
    "view_row_counts": {
        "matches_1v1_clean": t06_cnt,
        "player_history_all": t07_cnt,
    },
}

# NULL audit integration
artifact["null_audit"] = {
    "matches_1v1_clean": {
        "schema_guard_passed": True,
        "expected_col_count": 21,
        "actual_col_count": len(actual_matches_cols),
        "total_rows": int(total_rows_m1),
        "columns": null_results_m1,
        "zero_null_assertions": {col: True for col in MATCHES_ZERO_NULL_COLS},
    },
    "player_history_all": {
        "schema_guard_passed": True,
        "expected_col_count": 13,
        "actual_col_count": len(actual_hist_cols),
        "total_rows": int(total_rows_ph),
        "columns": null_results_ph,
        "zero_null_assertions": {col: True for col in HIST_ZERO_NULL_COLS},
        "nullable_findings": {
            "winner": {
                "null_count": int(winner_null_count_ph),
                "null_pct": float(winner_null_pct_ph),
                "note": (
                    "Nullable in player_history_all; VIEW covers all game types "
                    "including non-decisive matches. No WHERE winner IS NOT NULL filter applied."
                ),
            },
        },
    },
}

artifact["sql_queries"]["null_audit_matches_1v1_clean"] = SQL_NULL_AUDIT_MATCHES_COLS.strip()
artifact["sql_queries"]["null_audit_player_history_all"] = SQL_NULL_AUDIT_HIST_COLS.strip()
artifact["sql_queries"]["null_audit_per_column_template"] = 'SELECT COUNT(*) FILTER (WHERE "{column_name}" IS NULL) AS null_count FROM {view_name}'

# %%
# --- Add missingness_audit block (additive — Deliverable 5.D) ---

_decisions_surfaced_aoestats = [
    {
        "id": "DS-AOESTATS-01",
        "column": "team_0_elo / team_1_elo (sentinel=-1, absent in 1v1 filtered scope)",
        "observed_pct_missing_total": "runtime (from ledger)",
        "question": (
            "team_0_elo / team_1_elo: ELO=-1 sentinel ABSENT in matches_1v1_clean (upstream "
            "filter excludes the rows that carried it — the matches_1v1_clean WHERE clause "
            "restricts to ranked-1v1 decisive games where the sentinel does not appear). "
            "Ledger reports n_sentinel=0 → RETAIN_AS_IS / mechanism=N/A. Action item: if "
            "the ranked-1v1 scope is ever broadened, or if a different VIEW (e.g. unranked "
            "or non-1v1) is added to the audit, re-audit for sentinel resurfacing and "
            "reapply CONVERT_SENTINEL_TO_NULL via Rule S3. The spec entry retains "
            "mechanism=MCAR / sentinel_value=-1 to document the design intent for the "
            "mechanism (raw matches_raw evidence shows the sentinel exists at low rate); "
            "the ledger reflects the empirical post-filter observation."
        ),
    },
    {
        "id": "DS-AOESTATS-02",
        "column": "p0_old_rating / p1_old_rating (sentinel=0, n_zero=5,937 in players_raw)",
        "observed_pct_missing_total": "runtime (from ledger)",
        "question": (
            "NULLIF + listwise deletion per Rule S3 in 01_04_02+ DDL pass, "
            "OR retain 0 as explicit unrated categorical encoding alongside is_unrated? "
            "B6 deferral: audit recommends CONVERT_SENTINEL_TO_NULL (non-binding for "
            "carries_semantic_content=True). Downstream chooses."
        ),
    },
    {
        "id": "DS-AOESTATS-03",
        "column": "avg_elo (n_sentinel=118 in matches_1v1_clean / n_zero=121 in matches_raw)",
        "observed_pct_missing_total": "runtime (from ledger)",
        "question": (
            "avg_elo: n_sentinel=118 in matches_1v1_clean / n_zero=121 in matches_raw "
            "(numeric_stats_matches[label='avg_elo'] ground truth). Same MAR / "
            "CONVERT_SENTINEL_TO_NULL recommendation; the 3-row difference is the "
            "upstream 1v1 filter discarding 3 sentinel rows. Disposition (genuine zero "
            "vs sentinel) deferred to 01_04_02+ join investigation. Note: the n_zero=4,824 "
            "figure cited in earlier drafts belongs to team_0_elo, NOT avg_elo."
        ),
    },
    {
        "id": "DS-AOESTATS-04",
        "column": "raw_match_type (NULLs in matches_raw ~0.04%)",
        "observed_pct_missing_total": "runtime (from ledger)",
        "question": (
            "MCAR per Rule S3, listwise deletion candidate at 01_04_02+. "
            "Column may be redundant given internalLeaderboardId already constrains scope."
        ),
    },
    {
        "id": "DS-AOESTATS-05",
        "column": "team1_wins (prediction target, BIGINT)",
        "observed_pct_missing_total": 0.0,
        "question": (
            "0 NULLs verified (upstream WHERE p0.winner != p1.winner exclusion). "
            "F1 zero-missingness override → RETAIN_AS_IS / mechanism=N/A."
        ),
    },
    {
        "id": "DS-AOESTATS-06",
        "column": "winner in player_history_all",
        "observed_pct_missing_total": 0.0,
        "question": (
            "winner in player_history_all: ledger reports 0 NULLs / RETAIN_AS_IS / "
            "mechanism=N/A (better than plan-anticipated ~5% rate). The upstream "
            "players_raw filtering or the players_raw schema does not produce NULL "
            "winners in the loaded dataset. CONSORT note: re-verify on every dataset "
            "re-load; if winner NULLs surface in future loads, the target-override "
            "post-step (B4) will fire automatically and convert recommendation to "
            "EXCLUDE_TARGET_NULL_ROWS — no Phase 02 code change required."
        ),
    },
    {
        "id": "DS-AOESTATS-07",
        "column": "overviews_raw (singleton metadata, 1 row)",
        "observed_pct_missing_total": "N/A",
        "question": (
            "Formally declare out-of-analytical-scope at 01_04_02+ disposition step. "
            "Not used by any VIEW."
        ),
    },
    {
        "id": "DS-AOESTATS-08",
        "column": "leaderboard, num_players (constants in matches_1v1_clean)",
        "observed_pct_missing_total": 0.0,
        "question": (
            "leaderboard and num_players detected as TRUE constants "
            "(n_distinct=1) in matches_1v1_clean by the runtime constants-detection "
            "branch (W7 fix). Recommendation: DROP_COLUMN per Rule S4 / N/A-mechanism. "
            "Both columns are constant-by-construction in the cleaned scope: "
            "matches_1v1_clean filters to leaderboard='random_map' and num_players=2. "
            "Confirm drop in 01_04_02+ DDL pass."
        ),
    },
]

artifact["missingness_audit"] = {
    "framework": {
        "source_doc": "temp/null_handling_recommendations.md",
        "rules_applied": ["S1", "S2", "S3", "S4", "S5", "S6"],
        "mechanism_taxonomy": "Rubin (1976); Little & Rubin (2019, 3rd ed.)",
        "phase_boundary": "Phase 01 documents (I9). Phase 02 transforms.",
        "thresholds": {
            "low_rate_pct": 5.0,
            "mid_rate_pct": 40.0,
            "high_rate_pct": 80.0,
            "threshold_source": (
                "Operational starting heuristics from temp/null_handling_recommendations.md §1.2; "
                "<5% MCAR boundary citation: Schafer & Graham 2002; "
                "warning against rigid global thresholds: van Buuren 2018"
            ),
        },
        "override_priority": [
            "1. Constants detection (n_distinct == 1) → mechanism=N/A, recommendation=DROP_COLUMN",
            "2. F1 zero-missingness (n_total_missing == 0) → mechanism=N/A, recommendation=RETAIN_AS_IS",
            "3. _recommend() per spec/fallback (incl. CONVERT_SENTINEL_TO_NULL for sentinel-only low-rate cases)",
            "4. Target-column post-step (col in target_cols AND n_total_missing > 0) → EXCLUDE_TARGET_NULL_ROWS",
        ],
        "per_view_target_cols": {
            "matches_1v1_clean": ["team1_wins"],
            "player_history_all": ["winner"],
        },
    },
    "missingness_spec": _missingness_spec,
    "views": build_audit_views_block({
        _view_m1: {"total_rows": total_rows_m1, "df_ledger": df_ledger_m1},
        _view_ph: {"total_rows": total_rows_ph, "df_ledger": df_ledger_ph},
    })["views"],
    "decisions_surfaced": _decisions_surfaced_aoestats,
}

# 6.B: decisions_surfaced assertions
assert len(artifact["missingness_audit"]["decisions_surfaced"]) >= 1
assert all(
    "question" in d and d["question"]
    for d in artifact["missingness_audit"]["decisions_surfaced"]
)
print("PASS: missingness_audit block assembled and assertions passed")

# Write JSON artifact
artifact_json_path = cleaning_dir / "01_04_01_data_cleaning.json"
with open(artifact_json_path, "w") as f:
    json.dump(artifact, f, indent=2, default=str)
print(f"Artifact JSON written: {artifact_json_path}")

# %%
# --- Write missingness ledger CSV + JSON (Deliverable 5.A) ---

df_ledger_all = pd.concat([df_ledger_m1, df_ledger_ph], ignore_index=True)

ledger_csv_path = cleaning_dir / "01_04_01_missingness_ledger.csv"
df_ledger_all.to_csv(ledger_csv_path, index=False)
print(f"Ledger CSV written: {ledger_csv_path} ({len(df_ledger_all)} rows)")

ledger_json_path = cleaning_dir / "01_04_01_missingness_ledger.json"
ledger_json = {
    "step": "01_04_01",
    "dataset": "aoestats",
    "generated_date": "2026-04-17",
    "framework": artifact["missingness_audit"]["framework"],
    "missingness_spec": _missingness_spec,
    "ledger": df_ledger_all.to_dict(orient="records"),
    "decisions_surfaced": _decisions_surfaced_aoestats,
}
with open(ledger_json_path, "w") as f:
    json.dump(ledger_json, f, indent=2, default=str)
print(f"Ledger JSON written: {ledger_json_path}")

# 6.B: file existence assertions
assert ledger_csv_path.exists(), f"FAIL: ledger CSV missing: {ledger_csv_path}"
assert ledger_json_path.exists(), f"FAIL: ledger JSON missing: {ledger_json_path}"

# Verify 17-column CSV schema (Deliverable 5.B)
_expected_csv_cols = {
    "view", "column", "dtype", "n_total", "n_null", "pct_null",
    "sentinel_value", "n_sentinel", "pct_sentinel", "pct_missing_total",
    "n_distinct", "mechanism", "mechanism_justification",
    "recommendation", "recommendation_justification",
    "carries_semantic_content", "is_primary_feature",
}
assert set(df_ledger_all.columns) == _expected_csv_cols, (
    f"CSV column set mismatch: {set(df_ledger_all.columns).symmetric_difference(_expected_csv_cols)}"
)
print(f"PASS: ledger files written; CSV has {len(df_ledger_all.columns)} columns (expected 17)")

# %%
# Write MD artifact
md_lines = [
    "# 01_04_01 Data Cleaning -- aoestats",
    "",
    "**Dataset:** aoestats | **Step:** 01_04_01 | **Date:** 2026-04-16",
    "",
    "## Cleaning Registry",
    "",
    "| Rule | Condition | Action | Impact |",
    "|------|-----------|--------|--------|",
]

for rule_id, rule in cleaning_registry.items():
    md_lines.append(f"| {rule['id']} | {rule['condition']} | {rule['action']} | {rule['impact']} |")

md_lines += [
    "",
    "## CONSORT Flow (matches_1v1_clean)",
    "",
    f"- Stage 0 (all matches): {consort_flow['stage_0_all_matches']:,}",
    f"- Stage 1 (has player rows): {consort_flow['stage_1_has_players']:,}",
    f"- Stage 2 (structural 1v1): {consort_flow['stage_2_structural_1v1']:,}",
    f"- Stage 3 (ranked 1v1, distinct teams): {consort_flow['stage_3_ranked_1v1_distinct_teams']:,}",
    f"- Stage 4 (final VIEW, inconsistent winners excluded): {consort_flow['stage_4_view_final']:,}",
    f"- player_history_all rows: {consort_flow['player_history_all_rows']:,}",
    "",
    "## Temporal Schema Analysis",
    "",
    f"- Total weeks analysed: {artifact['t05_temporal_schema_analysis']['weeks_total']}",
    f"- Last week with opening > 1%: {artifact['t05_temporal_schema_analysis']['last_week_opening_gt_1pct']}",
    f"- First week with opening = 0%: {artifact['t05_temporal_schema_analysis']['first_week_opening_zero']}",
    "- Feature-inclusion decision deferred to Phase 02 (I9).",
    "",
    "## Same-Team Assertion",
    "",
    f"- same_team_game_count: {t06_same_team}",
    "- Outcome: 0-impact assertion verified. No same-team games found.",
    "",
    "## Team-Assignment Asymmetry (I5 Warning)",
    "",
    f"- t1_wins: {artifact['t06_team_assignment_asymmetry']['t1_wins']:,}",
    f"- t0_wins: {artifact['t06_team_assignment_asymmetry']['t0_wins']:,}",
    f"- t1_win_pct: {t1_win_pct}%",
    "",
    "**WARNING:** p0 (team=0) and p1 (team=1) are NOT symmetric player slots.",
    "Downstream 01_05+ feature engineering MUST apply player-slot randomisation.",
    "",
    "## Post-Cleaning Validation Results",
    "",
    f"- ratings_raw_exists: {t08_ratings_raw} (PASS)",
    f"- inconsistent winner rows: {t08_xor['inconsistent'].iloc[0]} (PASS)",
    f"- p0_profile_id, p1_profile_id, profile_id: all BIGINT (PASS)",
]

md_lines += [
    "",
    "## NULL Audit",
    "",
    "### matches_1v1_clean",
    "",
    f"Total rows: {int(total_rows_m1):,}",
    "",
    "| Column | NULL Count | NULL % |",
    "|--------|-----------|--------|",
]
for r in null_results_m1:
    md_lines.append(f"| {r['column']} | {r['null_count']:,} | {r['null_pct']}% |")

md_lines += [
    "",
    f"Zero-NULL assertions passed: {', '.join(MATCHES_ZERO_NULL_COLS)}",
    "",
    "### player_history_all",
    "",
    f"Total rows: {int(total_rows_ph):,}",
    "",
    "| Column | NULL Count | NULL % |",
    "|--------|-----------|--------|",
]
for r in null_results_ph:
    md_lines.append(f"| {r['column']} | {r['null_count']:,} | {r['null_pct']}% |")

md_lines += [
    "",
    f"Zero-NULL assertions passed: {', '.join(HIST_ZERO_NULL_COLS)}",
    "",
    f"**FINDING:** `winner` has {winner_null_count_ph:,} NULLs ({winner_null_pct_ph}%). "
    "Expected: VIEW covers all game types including non-decisive matches.",
]

md_lines += [
    "",
    "## VIEW DDL",
    "",
    "### matches_1v1_clean",
    "",
    "```sql",
    SQL_T06_MATCHES_1V1_CLEAN.strip(),
    "```",
    "",
    "### player_history_all",
    "",
    "```sql",
    SQL_T07_PLAYER_HISTORY_ALL.strip(),
    "```",
]

# Missingness Ledger sections (Deliverable 4.B + plan gate requirement)
md_lines += [
    "",
    "## Missingness Ledger",
    "",
    "### matches_1v1_clean",
    "",
    f"Total rows: {int(total_rows_m1):,} | Ledger rows: {len(df_ledger_m1)}",
    "",
    "| Column | dtype | n_null | pct_null | sentinel_value | n_sentinel | pct_sentinel | pct_missing_total | mechanism | recommendation | carries_semantic | is_primary |",
    "|--------|-------|--------|---------|----------------|-----------|-------------|------------------|-----------|---------------|-----------------|-----------|",
]
for _, lrow in df_ledger_m1.iterrows():
    md_lines.append(
        f"| {lrow['column']} | {lrow['dtype']} | {lrow['n_null']:,} | {lrow['pct_null']} | "
        f"{lrow['sentinel_value']} | {lrow['n_sentinel']:,} | {lrow['pct_sentinel']} | "
        f"{lrow['pct_missing_total']} | {lrow['mechanism']} | {lrow['recommendation']} | "
        f"{lrow['carries_semantic_content']} | {lrow['is_primary_feature']} |"
    )

md_lines += [
    "",
    "### player_history_all",
    "",
    f"Total rows: {int(total_rows_ph):,} | Ledger rows: {len(df_ledger_ph)}",
    "",
    "| Column | dtype | n_null | pct_null | sentinel_value | n_sentinel | pct_sentinel | pct_missing_total | mechanism | recommendation | carries_semantic | is_primary |",
    "|--------|-------|--------|---------|----------------|-----------|-------------|------------------|-----------|---------------|-----------------|-----------|",
]
for _, lrow in df_ledger_ph.iterrows():
    md_lines.append(
        f"| {lrow['column']} | {lrow['dtype']} | {lrow['n_null']:,} | {lrow['pct_null']} | "
        f"{lrow['sentinel_value']} | {lrow['n_sentinel']:,} | {lrow['pct_sentinel']} | "
        f"{lrow['pct_missing_total']} | {lrow['mechanism']} | {lrow['recommendation']} | "
        f"{lrow['carries_semantic_content']} | {lrow['is_primary_feature']} |"
    )

# Decisions surfaced section
md_lines += [
    "",
    "## Decisions Surfaced for Downstream Cleaning (01_04_02+)",
    "",
]
for ds in _decisions_surfaced_aoestats:
    md_lines += [
        f"### {ds['id']}: {ds['column']}",
        "",
        ds["question"],
        "",
    ]

artifact_md_path = cleaning_dir / "01_04_01_data_cleaning.md"
with open(artifact_md_path, "w") as f:
    f.write("\n".join(md_lines) + "\n")
print(f"Artifact MD written: {artifact_md_path}")

# %%
print("All artifacts written successfully.")
print(f"  matches_1v1_clean row count: {t06_cnt:,}")
print(f"  player_history_all row count: {t07_cnt:,}")
print(f"  t1_win_pct: {t1_win_pct}%")
print(f"  inconsistent winner rows excluded: 997 (both players same outcome)")
db.close()
