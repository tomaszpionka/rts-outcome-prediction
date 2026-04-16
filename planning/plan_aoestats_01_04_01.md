---
category: A
branch: feat/data-cleaning-01-04
date: 2026-04-16
planner_model: claude-opus-4-6
dataset: aoestats
phase: "01"
pipeline_section: "01_04 — Data Cleaning"
invariants_touched: [3, 5, 6, 7, 9]
critique_required: true
source_artifacts:
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.json"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/03_profiling/01_03_02_true_1v1_profile.json"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/03_profiling/01_03_03_table_utility.json"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.json"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_06_bivariate_eda.json"
  - "planning/fixes_and_next_steps.md"
research_log_ref: "src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md"
revision_history:
  - "v1: original plan"
  - "v2: post-critique revision addressing W01 (team-assignment asymmetry / I5), W02 (same-team assertion), W03 (ratings_raw absence assertion); added player_history_all VIEW; added prediction-scope != feature-scope clarification"
---

# Plan: aoestats 01_04_01 — Data Cleaning (v2 — post-critique)

## Scope

**Phase/Step:** 01 / 01_04_01
**Branch:** feat/data-cleaning-01-04
**Predecessor:** 01_03_03 (Table Utility Assessment — complete, artifacts on disk)

Create the cleaned analytical VIEWs in DuckDB for downstream feature
engineering. Two VIEWs produced:

1. **`matches_1v1_clean`** — wide-format analytical VIEW (one row per 1v1
   match, p0/p1 column pairs). This defines the **prediction target scope**:
   ranked 1v1 matches only.

2. **`player_history_all`** — long-format player-row VIEW across ALL game
   types and leaderboards. This defines the **feature computation source**:
   each player's full recorded game history, unrestricted by game type.

Covers: profile_id DOUBLE precision verification, 1v1 scope restriction
(prediction target only), orphan match exclusion, constant/near-dead column
documentation, temporal NULL stratification for schema-change columns,
same-team assertion, team-assignment asymmetry documentation,
VIEW creation with I3-safe column selection, ratings_raw absence assertion,
and post-cleaning validation. Non-destructive: raw tables are never modified;
all filtering is via VIEW predicates.

## Problem Statement

Two ESSENTIAL raw tables: `matches_raw` (30,690,651 rows) and `players_raw`
(107,627,584 rows). Pre-game features are split: matches_raw holds the
temporal anchor (`started_timestamp`), map, leaderboard, patch; players_raw
holds the target (`winner`), pre-game rating (`old_rating`), civilization
(`civ`), player identity (`profile_id`). All downstream work requires:

- A wide-format analytical VIEW restricted to the 1v1 prediction target scope.
- A long-format player-row VIEW covering all game types for full-history
  feature computation.

**Scope distinction (thesis design constraint):** The thesis predicts only
1v1 match outcomes (`matches_1v1_clean`). However, player-level features
(win rate, civ proficiency, match volume, ELO trajectory, etc.) are computed
from each player's FULL recorded game history across all game types and
leaderboards (`player_history_all`). Rationale: the dataset already has
selection bias (only online registered games). Restricting feature computation
to 1v1 would compound that bias without eliminating it. Team games, unranked
games, and other ladder types all provide valid signal about player skill and
tendencies. Honest thesis framing: features are computed from all available
recorded game history; selection bias from the online-registration data
collection boundary is a known limitation. Temporal discipline (I3) still
applies to all game types: features for match T at time t use only games
completed strictly before time t, regardless of game type.

Seven data quality issues deferred to this step, plus three critique-flagged issues:

1. `profile_id` stored as DOUBLE (float64) — precision loss risk for IDs > 2^53
2. Only 60.08% of matches are structurally 1v1 (exactly 2 player rows)
3. 212,890 orphan matches (0.69%) with no player rows
4. Two constant columns carry zero information: `game_type`='random_map',
   `game_speed`='normal'
5. One near-dead column: `starting_age` — 99.99994% 'dark', 19 rows 'standard'
6. Four columns with 86-91% NULLs from a schema change boundary in source data
   (`opening`, `feudal_age_uptime`, `castle_age_uptime`, `imperial_age_uptime`)
7. `new_rating` is POST-GAME and must be excluded from any analytical view (I3)
8. **[W01]** Team-assignment asymmetry: team=1 wins 51.86% of matches
   (elo_diff -18.48 vs -0.37 for team=0 wins) — I5 risk for wide-format VIEW
9. **[W02]** Same-team games: potential for both players on same team causing
   INNER JOIN fan-out or silent exclusion
10. **[W03]** aoestats has no `ratings_raw` table — must be explicitly asserted

## Assumptions & Unknowns

- **Assumption:** profile_id max value (24,853,897) is well below 2^53 — no
  precision loss expected. T01 verifies.
- **Assumption:** DuckDB VIEWs are the right abstraction (non-destructive,
  non-materialized).
- **Assumption:** 1v1 scope = structural 1v1 (player_count=2) AND leaderboard=
  'random_map'. The 622,825 structural-1v1 games from other leaderboards are
  excluded from the prediction target. They ARE included in `player_history_all`.
- **Assumption:** Feature computation from the player's full history (all game
  types) is methodologically sound. Selection bias from the online-registration
  data collection boundary is acknowledged as a limitation.
- **Unknown:** Exact temporal boundary where `opening`/age-uptime columns
  transition from all-NULL to populated. Resolved by T05.
- **Unknown:** Whether any game_ids have two player rows with the same team
  value. Resolved by T06 assertion.

## Literature Context

CRISP-DM Phase 3 (Data Preparation); Manual Section 4. Non-destructive
cleaning (Section 4.2). Cleaning registry with Rule ID, Condition, Action,
Justification, Impact (Section 4.1). CONSORT-AI Extension flow diagram
(Liu et al. 2020, Section 4.3). Post-cleaning re-validation (Section 4.4).

---

## Execution Steps

### T01 — profile_id DOUBLE precision verification

**Objective:** Verify no precision loss from DOUBLE storage. Produce note R01.

**SQL:**

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE profile_id IS NOT NULL) AS nonnull_rows,
    COUNT(*) FILTER (WHERE profile_id IS NOT NULL
        AND profile_id - FLOOR(profile_id) != 0) AS fractional_count,
    COUNT(*) FILTER (WHERE profile_id IS NOT NULL
        AND ABS(profile_id) > 9007199254740992) AS unsafe_range_count,
    MIN(profile_id) FILTER (WHERE profile_id IS NOT NULL) AS min_id,
    MAX(profile_id) FILTER (WHERE profile_id IS NOT NULL) AS max_id
FROM players_raw;
```

**Cleaning note R01:**
- Condition: `profile_id IS DOUBLE`
- Action: CAST to BIGINT in analytical VIEWs — safe if fractional_count=0 and
  unsafe_range_count=0
- Justification: 01_02_04 census max=24,853,897 (below 2^53); this confirms empirically.
- Impact: 0 rows affected (all values are exact integers in safe range).

**Verification:** fractional_count=0; unsafe_range_count=0; max_id < 9,007,199,254,740,992.

---

### T02 — 1v1 scope restriction (prediction target only)

<!-- REVISED: title clarified; scope note added -->

**Objective:** Define ranked 1v1 scope for the prediction target VIEW. Produce
rule R02 with CONSORT stage 1.

**IMPORTANT SCOPE NOTE:** This restriction defines the **prediction target VIEW
only** (`matches_1v1_clean`). The full `matches_raw` (all game types, all
leaderboards) and `players_raw` remain the full-history feature computation
source, exposed via `player_history_all` (T07). The 1v1 restriction does NOT
apply to feature computation scope for 01_05.

**SQL:**

```sql
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
SELECT * FROM scope;
```

**Expected counts:**
- total_matches = 30,690,651
- orphan_matches = 212,890
- structural_1v1 = 18,438,769
- scope_1v1_ranked = 17,815,944

**Cleaning rule R02:**
- Condition: `player_count != 2 OR leaderboard != 'random_map'`
- Action: EXCLUDE from `matches_1v1_clean` VIEW (prediction target only)
- Justification: Thesis scope is ranked 1v1 prediction. Excluded matches remain
  available for feature computation via `player_history_all`.
- Impact: 17,815,944 matches retained in prediction VIEW.

**Verification:** Cross-validate all counts within +/-1 row of 01_03_01 and 01_03_02 artifacts.

---

### T03 — Orphan match exclusion

**Objective:** Document 212,890 orphan match exclusion. Produce rule R03.

**SQL:**

```sql
SELECT COUNT(*) AS orphan_match_count
FROM matches_raw m
WHERE NOT EXISTS (SELECT 1 FROM players_raw p WHERE p.game_id = m.game_id);
```

**Cleaning rule R03:**
- Condition: game_id in matches_raw with no rows in players_raw
- Action: EXCLUDE (implicit via INNER JOIN in T06 and T07 VIEWs)
- Justification: 01_03_01 linkage check confirmed 212,890 orphans. No target variable.
- Impact: 212,890 matches (0.69%).

**Verification:** orphan_match_count = 212,890.

---

### T04 — Constant and near-dead column documentation

**Objective:** Document exclusion of zero-information columns. Produce rules R04, R05.

**SQL:**

```sql
SELECT
    'game_type' AS column_name, COUNT(DISTINCT game_type) AS cardinality, MIN(game_type) AS sole_value
FROM matches_raw
UNION ALL
SELECT 'game_speed', COUNT(DISTINCT game_speed), MIN(game_speed) FROM matches_raw
UNION ALL
SELECT 'starting_age', COUNT(DISTINCT starting_age), MIN(starting_age) FROM matches_raw;
```

**Cleaning rule R04:**
- Condition: `game_type = 'random_map' (100%), game_speed = 'normal' (100%)`
- Action: EXCLUDE columns from VIEWs
- Justification: 01_03_01 constant_columns: cardinality=1 across 30.7M rows.
- Impact: 0 rows; 2 columns removed.

**Cleaning rule R05:**
- Condition: `starting_age`: 99.99994% 'dark', 19 rows 'standard'
- Action: EXCLUDE column from VIEWs
- Justification: 01_03_01 near_constant finding.
- Impact: 0 rows; 1 column removed.

---

### T05 — Temporal schema analysis for high-NULL columns

**Objective:** Find the date boundary where `opening`, `feudal_age_uptime`,
`castle_age_uptime`, `imperial_age_uptime` transition from all-NULL to populated.
Documents a FINDING (not a hard cleaning rule) — feature-inclusion decision is Phase 02.

**SQL:**

```sql
-- Weekly NULL rate stratification
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
SELECT * FROM weekly ORDER BY week_date;
```

Store finding in artifact JSON under `t05_temporal_schema_analysis`. Do NOT
make feature-inclusion decision (I9).

---

### T06 — Create matches_1v1_clean VIEW

<!-- REVISED: W01 (team-assignment asymmetry), W02 (same-team assertion) addressed -->

**Objective:** Create joined analytical VIEW in WIDE format (one row per match,
player_0 and player_1 columns). Produces rule R06 (I3: exclude new_rating)
and rule R07 (same-team game exclusion). Documents team-assignment asymmetry
(I5 concern) with explicit `team1_wins` column.

**W02 FIX — Same-team assertion (run BEFORE creating VIEW):**

```sql
-- Assert no game_ids have both players on the same team
SELECT COUNT(*) AS same_team_game_count
FROM (
    SELECT game_id
    FROM players_raw
    GROUP BY game_id
    HAVING COUNT(*) = 2 AND COUNT(DISTINCT team) < 2
) st;
```

If `same_team_game_count > 0`: add explicit exclusion predicate to the VIEW
CTE and log as Cleaning Rule R07 with CONSORT count. If `same_team_game_count = 0`:
document as verified assertion (R07 condition never triggered, 0 impact).

**Cleaning rule R07 (conditional):**
- Condition: `game_id has 2 player rows with identical team values`
- Action: EXCLUDE from matches_1v1_clean (if any exist); else document as 0-impact assertion
- Justification: Same-team rows cause incorrect wide-format JOIN results.
- Impact: Expected 0 rows.

**VIEW SQL:**

```sql
-- matches_1v1_clean: Prediction-target VIEW for ranked 1v1 matches.
-- Scope: prediction target ONLY. Feature computation uses player_history_all.
--
-- TEAM-ASSIGNMENT ASYMMETRY (W01 / I5 WARNING):
-- team=1 wins 51.86% of matches. Mean elo_diff (team_0_elo - team_1_elo):
--   when team=0 wins: -0.37; when team=1 wins: -18.48
-- Source: 01_02_06 bivariate EDA.
-- p0_*/p1_* column pairs are NOT symmetric player slots.
-- Downstream 01_05+ feature engineering MUST apply player-slot randomisation
-- before using p0_*/p1_* as symmetric features. See research_log entry.
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
    m.duration,
    m.irl_duration,
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
    -- Player 0 (team=0)
    CAST(p0.profile_id AS BIGINT) AS p0_profile_id,
    p0.civ AS p0_civ,
    p0.old_rating AS p0_old_rating,
    p0.match_rating_diff AS p0_match_rating_diff,
    p0.winner AS p0_winner,
    p0.opening AS p0_opening,
    p0.feudal_age_uptime AS p0_feudal_age_uptime,
    p0.castle_age_uptime AS p0_castle_age_uptime,
    p0.imperial_age_uptime AS p0_imperial_age_uptime,
    -- Player 1 (team=1)
    CAST(p1.profile_id AS BIGINT) AS p1_profile_id,
    p1.civ AS p1_civ,
    p1.old_rating AS p1_old_rating,
    p1.match_rating_diff AS p1_match_rating_diff,
    p1.winner AS p1_winner,
    p1.opening AS p1_opening,
    p1.feudal_age_uptime AS p1_feudal_age_uptime,
    p1.castle_age_uptime AS p1_castle_age_uptime,
    p1.imperial_age_uptime AS p1_imperial_age_uptime,
    -- Team-assignment asymmetry indicator (W01 / I5)
    p1.winner AS team1_wins
FROM ranked_1v1 r
INNER JOIN matches_raw m ON m.game_id = r.game_id
INNER JOIN p0 ON p0.game_id = r.game_id
INNER JOIN p1 ON p1.game_id = r.game_id;
```

**Columns explicitly EXCLUDED:**
- `new_rating` (both players): POST-GAME, I3 violation (R06)
- `game_type`, `game_speed`: constant (R04)
- `starting_age`: near-dead (R05)
- `replay_summary_raw`: deferred to Phase 02
- `filename` (both tables): provenance
- `team` (both players): redundant after pivot

**Expected row count:** 17,815,944.

**Verification:**
- `SELECT COUNT(*) FROM matches_1v1_clean` = 17,815,944 (within +/-1)
- `DESCRIBE matches_1v1_clean`: no new_rating, game_type, game_speed, starting_age
- `p0_profile_id`, `p1_profile_id` are BIGINT
- `team1_wins` column exists and equals `p1_winner`
- `SELECT COUNT(*) FILTER (WHERE team1_wins) AS t1_wins, COUNT(*) FILTER (WHERE NOT team1_wins) AS t0_wins FROM matches_1v1_clean` — verify t1_wins > t0_wins (expected ~51.9%)

---

### T07 — Create player_history_all VIEW

<!-- REVISED: new task — full-history player-row VIEW for feature computation -->

**Objective:** Create a long-format player-row VIEW covering ALL game types
and leaderboards. One row per player per match. Input for player-level
aggregate feature computation in 01_05.

**Design rationale:**
- Player-row-oriented (not wide-format). I5 player-slot concern does not arise.
- No leaderboard/game-type restriction.
- Includes `player_count` and `leaderboard` for downstream stratification.
- Minimal quality filters: `profile_id IS NOT NULL`, `started_timestamp IS NOT NULL`.
- I3: VIEW exposes `started_timestamp`; downstream queries add
  `WHERE ph.started_timestamp < target_match.started_timestamp`.

**Cleaning rule R00:**
- Condition: scope definition for player feature computation source
- Action: CREATE VIEW `player_history_all` — all game types, all leaderboards.
- Justification: Full player history for feature computation; restricting to 1v1
  would compound selection bias without eliminating it.
- Impact: ~107.6M rows minus NULL profile_id (1,185) minus NULL started_timestamp.

**SQL:**

```sql
-- player_history_all: Full-history player-row VIEW for feature computation.
-- ALL game types, ALL leaderboards, ALL player counts.
-- One row per player per match.
--
-- I3 enforcement: Downstream feature queries MUST add
--   WHERE ph.started_timestamp < target_match.started_timestamp
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
    p.match_rating_diff,
    p.winner
FROM players_raw p
INNER JOIN matches_raw m ON p.game_id = m.game_id
INNER JOIN player_counts pc ON p.game_id = pc.game_id
WHERE p.profile_id IS NOT NULL
  AND m.started_timestamp IS NOT NULL;
```

**Columns excluded:**
- `new_rating`: POST-GAME, I3 violation (R06)
- `game_type`, `game_speed`, `starting_age`: constant/near-dead (R04/R05)
- `opening`, `feudal_age_uptime`, `castle_age_uptime`, `imperial_age_uptime`:
  IN-GAME, 86-91% NULL, feature-inclusion deferred to Phase 02 (I9)
- `replay_summary_raw`: PARTIAL UTILITY, deferred to Phase 02
- `filename` (both tables): provenance
- `duration`, `irl_duration`: POST-GAME

**Verification:**
- `SELECT COUNT(*) FROM player_history_all` — record in artifact
- `DESCRIBE player_history_all`: profile_id is BIGINT; no new_rating, duration, irl_duration
- `SELECT leaderboard, COUNT(*) FROM player_history_all GROUP BY leaderboard ORDER BY count DESC` — must show all leaderboards
- `SELECT player_count, COUNT(*) FROM player_history_all GROUP BY player_count ORDER BY player_count` — must include values > 2
- `SELECT COUNT(*) FILTER (WHERE profile_id IS NULL) FROM player_history_all` = 0
- `SELECT COUNT(*) FILTER (WHERE started_timestamp IS NULL) FROM player_history_all` = 0

**Schema YAML (write after verification):**

Write `src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/player_history_all.yaml`
using column list from `DESCRIBE player_history_all` output. Template:

```yaml
table: player_history_all
dataset: aoestats
game: aoe2
object_type: view
step: "01_04_01"
row_count: <fill from COUNT(*)>
describe_artifact: src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json
generated_date: '<YYYY-MM-DD>'
columns:
  # Fill from DESCRIBE player_history_all — annotate each column with:
  #   description: human-readable purpose
  #   notes: I3 classification (PRE_GAME / CONTEXT / TARGET / IDENTITY)
  #          and any invariant references
provenance:
  source_tables: [players_raw, matches_raw]
  filter: "profile_id IS NOT NULL; started_timestamp IS NOT NULL"
  scope: "All leaderboards and game types (no leaderboard restriction). Prediction scope != feature scope."
  created_by: sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_01_data_cleaning.py
invariants:
  - id: I3
    description: "new_rating (POST-GAME) excluded. Temporal anchor (started_timestamp)
      exposed for downstream WHERE ph.started_timestamp < target_match.started_timestamp."
  - id: I5
    description: "Player-row-oriented (one row per player per match). No wide-format
      pivoting. profile_id is the identity key."
  - id: I6
    description: "VIEW DDL stored verbatim in 01_04_01_data_cleaning.json sql_queries."
  - id: I9
    description: "No features computed. VIEW is a JOIN projection of players_raw x matches_raw."
```

---

### T08 — Post-cleaning validation

<!-- REVISED: ratings_raw absence assertion added (W03); team1_wins check; player_history_all validation -->

**Objective:** Validate VIEW quality. CONSORT flow. Confirm I3 compliance.
Assert ratings_raw absence.

**W03 FIX — ratings_raw absence assertion:**

```sql
SELECT COUNT(*) AS ratings_raw_exists
FROM information_schema.tables
WHERE table_name = 'ratings_raw';
```

Verify `ratings_raw_exists = 0`. Document: "aoestats has no ratings_raw table.
All ELO data is embedded in players_raw (old_rating, new_rating) and
matches_raw (avg_elo, team_0_elo, team_1_elo)."

**CONSORT flow SQL:**

```sql
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
    (SELECT COUNT(*) FROM player_history_all) AS player_history_all_rows;
```

**Winner distribution:**

```sql
SELECT p0_winner, COUNT(*) AS cnt,
       ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),4) AS pct
FROM matches_1v1_clean GROUP BY p0_winner ORDER BY p0_winner;
```

**Winner consistency (XOR check):**

```sql
SELECT COUNT(*) AS total,
       COUNT(*) FILTER (WHERE p0_winner = true AND p1_winner = false) AS p0_wins,
       COUNT(*) FILTER (WHERE p0_winner = false AND p1_winner = true) AS p1_wins,
       COUNT(*) FILTER (WHERE p0_winner = p1_winner) AS inconsistent
FROM matches_1v1_clean;
```

Verify `inconsistent = 0`.

**Team-assignment asymmetry verification:**

```sql
SELECT
    COUNT(*) FILTER (WHERE team1_wins = true) AS t1_wins,
    COUNT(*) FILTER (WHERE team1_wins = false) AS t0_wins,
    ROUND(100.0 * COUNT(*) FILTER (WHERE team1_wins = true) / COUNT(*), 2) AS t1_win_pct
FROM matches_1v1_clean;
```

Record t1_win_pct in artifact. Expected ~51.9%.

**I3 column exclusion check:**

```python
clean_cols = set(con.execute("DESCRIBE matches_1v1_clean").df()['column_name'])
forbidden = {'new_rating', 'p0_new_rating', 'p1_new_rating',
             'game_type', 'game_speed', 'starting_age'}
assert forbidden.isdisjoint(clean_cols), f"Schema violation: {forbidden & clean_cols}"

hist_cols = set(con.execute("DESCRIBE player_history_all").df()['column_name'])
forbidden_hist = {'new_rating', 'game_type', 'game_speed', 'starting_age',
                  'duration', 'irl_duration'}
assert forbidden_hist.isdisjoint(hist_cols), f"Schema violation: {forbidden_hist & hist_cols}"
```

**Profile_id type check:**

```sql
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name IN ('matches_1v1_clean', 'player_history_all')
  AND column_name IN ('p0_profile_id', 'p1_profile_id', 'profile_id');
```

All must be BIGINT.

---

### T09 — Assemble artifacts and update tracking

**Objective:** Write JSON and MD artifacts. Update STEP_STATUS.yaml, ROADMAP.md,
and research_log.md.

**Research log entry — MANDATORY (W01 follow-up):**

The research log entry MUST include:

> **TEAM-ASSIGNMENT ASYMMETRY (I5 WARNING FOR 01_05+):** In the
> `matches_1v1_clean` VIEW, p0 (team=0) and p1 (team=1) are NOT random
> player slots. Team=1 wins ~51.9% of 1v1 matches, with mean elo_diff
> (team_0_elo - team_1_elo) of -18.48 when team=1 wins vs -0.37 when
> team=0 wins (01_02_06 artifact). Downstream 01_05+ feature engineering
> MUST apply player-slot randomisation before using p0_*/p1_* column
> pairs as symmetric features. Without randomisation, any model will
> learn the team-assignment signal, not match skill. The `team1_wins`
> column is included in the VIEW to make this asymmetry explicit.

---

## File Manifest

| File | Action |
|------|--------|
| `sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_01_data_cleaning.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_01_data_cleaning.ipynb` | Create (jupytext-paired) |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/player_history_all.yaml` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md` | Update (prepend entry) |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml` | Update (add 01_04_01) |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` | Update (add 01_04_01 step definition) |

## Gate Condition

- `01_04_01_data_cleaning.json` exists; contains cleaning_registry (R00-R07),
  consort_flow, view_ddl (both VIEWs), sql_queries, t06_team_assignment_asymmetry,
  t08_ratings_raw_absence.
- VIEW `matches_1v1_clean` exists; returns ~17,815,944 rows.
- VIEW `player_history_all` exists; returns ~107.6M rows (minus NULL exclusions).
- `DESCRIBE matches_1v1_clean`: no new_rating, game_type, game_speed, starting_age.
- `DESCRIBE player_history_all`: no new_rating, game_type, game_speed, starting_age, duration, irl_duration.
- `p0_profile_id` and `p1_profile_id` are BIGINT; `profile_id` in player_history_all is BIGINT.
- `team1_wins` column exists in matches_1v1_clean.
- `inconsistent = 0` (winner consistency check).
- `ratings_raw_exists = 0` (no ratings_raw table in aoestats).
- Research log entry includes team-assignment asymmetry warning for 01_05+.
- `schemas/views/player_history_all.yaml` exists; `object_type: view`; `row_count` populated.
- STEP_STATUS.yaml: `01_04_01: complete`.

## Out of Scope

- Feature engineering (Phase 02, I9).
- Materialized tables.
- replay_summary_raw parsing (Phase 02).
- Player-slot randomisation: documented as I5 requirement for 01_05+; not
  implemented in 01_04 VIEWs.
- Feature-scope stratification (1v1-only vs all-history features): `player_history_all`
  includes `player_count` and `leaderboard` for downstream stratification;
  the stratification logic itself belongs to 01_05.

## Open Questions

- **Q1:** Same-team game_ids: any exist? T06 assertion resolves.
- **Q2:** `mirror` column: keep or exclude from views? Currently included as POST-GAME descriptive.
- **Q3:** Should `player_history_all` include `duration`/`irl_duration`? Currently excluded.
- **Q4:** age-uptime columns: feature-inclusion decision deferred to Phase 02 (I9).

## Scientific Invariants

| # | Invariant | How upheld |
|---|-----------|------------|
| I3 | No post-game features | new_rating excluded from both VIEWs (R06). Python assertion confirms. |
| I5 | Symmetric player treatment | Team-assignment asymmetry documented in DDL comment, team1_wins column, research_log. Randomisation deferred to 01_05 (documented as mandatory). |
| I6 | All SQL verbatim | Every query in T01-T09 stored as literal string in notebook and MD artifact. |
| I7 | No magic numbers | R02 scope: player_count=2 and leaderboard='random_map' from 01_03_02. R01 precision threshold 2^53 is the IEEE 754 double safe-integer bound. Team-assignment asymmetry magnitude from 01_02_06 artifact. |
| I9 | Step scope | Cleaning and VIEW creation only. Feature-inclusion decisions for opening/age uptimes explicitly deferred. |

---

**Adversarial critique required before execution begins.**
