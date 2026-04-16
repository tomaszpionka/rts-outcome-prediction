---
category: A
branch: feat/data-cleaning-01-04
date: 2026-04-16
planner_model: claude-opus-4-6
dataset: aoe2companion
phase: "01"
pipeline_section: "01_04 — Data Cleaning"
invariants_touched: [3, 5, 6, 7, 9]
critique_required: true
source_artifacts:
  - "reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.json"
  - "reports/artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.json"
  - "reports/artifacts/01_exploration/03_profiling/01_03_02_true_1v1_profile.json"
  - "reports/artifacts/01_exploration/03_profiling/01_03_03_table_utility_assessment.json"
  - "data/db/db.duckdb (matches_raw, ratings_raw)"
research_log_ref: "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md"
revision: 2
revision_date: 2026-04-16
revision_reason: "Fix BLOCKER F01 (rowid), BLOCKER F02 (V2 columns), WARNING W01 (NULL temporal), add player_history_all VIEW, add prediction-vs-feature scope constraint"
---

# Plan: aoe2companion 01_04_01 — Data Cleaning (revision 2)

## Scope

**Phase/Step:** 01 / 01_04_01
**Branch:** feat/data-cleaning-01-04
**Predecessor:** 01_03_03 (Table Utility Assessment — complete, artifacts on disk)

<!-- REVISED — scope paragraph rewritten to reflect dual-VIEW output and prediction-vs-feature scope -->

Build a data cleaning notebook that applies non-destructive cleaning to
`matches_raw` (277,099,059 rows) per Manual Section 4. The notebook
establishes a cleaning registry of rules R00–R05, adds exclusion flag
columns to cleaned DuckDB VIEWs, and produces a CONSORT-style row-count
flow from raw to clean data. All raw data remains untouched; cleaning is
expressed as VIEW-layer filters over `matches_raw`. `ratings_raw` receives
a single outlier-capping rule (R05) applied via a separate VIEW
(`ratings_clean`).

Two primary VIEWs are produced:

1. **`matches_1v1_clean`** — the prediction target VIEW: rm_1v1 + qp_rm_1v1
   matches only, fully deduplicated, won-complementary, with POST-GAME
   columns excluded. This VIEW defines which matches will be predicted.

2. **`player_history_all`** — the feature computation source VIEW: all game
   types, player-row-oriented (one row per player per match), minimally
   filtered (anonymous rows excluded, deduplicated). This VIEW serves as
   the input for player-level aggregate features in 01_05 feature
   engineering. It covers the player's full recorded game history without
   game-type restriction.

**Design constraint — prediction scope != feature scope:** The thesis
predicts only 1v1 match outcomes. However, player-level features (win rate,
civ proficiency, match volume, ELO trajectory, etc.) are computed from the
player's full recorded game history — all game types — not restricted to
1v1 only. Rationale: the dataset already has selection bias (only online
registered games). Restricting feature computation to 1v1 compounds that
bias without eliminating it. Team games, unranked games, and other ladder
types all provide valid signal about player skill and tendencies. The
thesis honest framing: *features are computed from all available recorded
game history; selection bias from the online-registration data collection
boundary is a known limitation.* Temporal discipline (I3) still applies to
all game types: features for match T at time t use only games completed
before time t, regardless of game type.

## Problem Statement

Steps 01_02 and 01_03 identified five categories of data quality issues
that must be resolved before feature engineering (Phase 02):

1. **Scope mismatch.** The thesis predicts 1v1 ranked match outcomes.
   matches_raw contains all game modes (team, FFA, unranked).
   277M rows must be narrowed to the ~61M rows in rm_1v1
   (internalLeaderboardId=6) and qp_rm_1v1 (internalLeaderboardId=18)
   for the prediction target. Separately, all game types must remain
   accessible for feature computation.

2. **Duplicates.** 8,812,005 excess rows (matchId, profileId) pairs
   exist. Stratified analysis by profileId=-1 is required before
   removal. 01_03_02 found profileId=-1 as status='player' affects
   only 19,232 rows total (8,993 matches), with exactly 1 row in rm_1v1.

3. **Internally inconsistent matches.** Matches where both rows have
   won=TRUE or both won=FALSE. These cannot serve as training examples
   in a binary classification task.

4. **NULL co-occurrence cluster.** ~428K rows with 10 boolean/numeric
   game-setting columns simultaneously NULL. Investigation needed to
   determine whether these are systematic bad data (API schema change)
   or recoverable.

5. **ratings_raw.games extreme outlier.** Max=1,775,260,795 vs
   p95=4,736 and median=546. This is a data error. Must be capped
   before any join with matches data.

Manual Section 4 requires: (a) a cleaning registry with Rule ID,
Condition, Action, Justification, Impact; (b) non-destructive cleaning
via exclusion flags and VIEWs; (c) CONSORT-style flow diagram; (d)
post-cleaning validation.

## Assumptions & Unknowns

- **Assumption:** `matches_raw.rating` is definitively PRE-GAME (01_03_03: 99.8%).
- **Assumption:** rm_1v1 (internalLeaderboardId=6) and qp_rm_1v1 (id=18) are the
  only in-scope leaderboards for the prediction target.
- **Assumption:** `matches_raw` is the sole source of match-level player data in
  aoe2companion. There is no separate `players_raw` table; player data is embedded
  in match rows (one row per player per match). The `ratings_raw`, `profiles_raw`,
  and `leaderboards_raw` tables are either CONDITIONALLY_USABLE or NOT_USABLE per
  01_03_03 findings.
- **Unknown:** Whether the NULL cluster (428K rows) is concentrated in a
  specific time period. Resolved by T04's temporal stratification query.
- **Unknown:** Exact p99.9 value for ratings_raw.games. Resolved by T05.

## Literature Context

Non-destructive cleaning via exclusion flags follows CRISP-DM Phase 3.
CONSORT-style flow adapted from Liu et al. (2020), CONSORT-AI Extension.
Rubin (1976) MCAR/MAR/MNAR informs the NULL cluster investigation.
The reforms checklist (Kapoor et al. 2023) Module 3 requires subgroup
impact breakdown.

---

## Execution Steps

### T01 — Scope restriction to 1v1 ranked leaderboards

<!-- REVISED — added explicit note about prediction target vs feature source scope -->

**Objective:** Filter matches_raw to rm_1v1 (internalLeaderboardId=6) and
qp_rm_1v1 (internalLeaderboardId=18) for the prediction target VIEW.
CONSORT stage 1. Produce rule R01.

**Important scope note:** This restriction defines the *prediction target
VIEW only* (`matches_1v1_clean`). The full `matches_raw` table — all game
types — remains accessible as the full-history feature computation source.
Task T06 creates `player_history_all` VIEW over the unrestricted table for
exactly this purpose. Downstream feature engineering (01_05) will use
`player_history_all` for player-level aggregates (win rate, civ proficiency,
match volume, ELO trajectory) while `matches_1v1_clean` defines which
matches receive predictions.

**SQL:**

```sql
-- R01: Scope restriction — count rows before/after
SELECT
    'total' AS scope,
    COUNT(*) AS n_rows,
    COUNT(DISTINCT matchId) AS n_matches
FROM matches_raw

UNION ALL

SELECT
    'in_scope_1v1' AS scope,
    COUNT(*) AS n_rows,
    COUNT(DISTINCT matchId) AS n_matches
FROM matches_raw
WHERE internalLeaderboardId IN (6, 18)

UNION ALL

SELECT
    'out_of_scope' AS scope,
    COUNT(*) AS n_rows,
    COUNT(DISTINCT matchId) AS n_matches
FROM matches_raw
WHERE internalLeaderboardId NOT IN (6, 18)
   OR internalLeaderboardId IS NULL;
```

**Cleaning rule R01:**
- Condition: `internalLeaderboardId NOT IN (6, 18) OR internalLeaderboardId IS NULL`
- Action: Exclude from prediction target VIEW (scope restriction); retain in `player_history_all`
- Justification: Thesis scope is 1v1 ranked Random Map prediction. 01_03_02
  confirmed rm_1v1 + qp_rm_1v1 captures 99.98% of structural 1v1 matches.
- Impact: ~216M rows excluded from prediction target (~78% of total). Verify
  in_scope approximately equals 61,071,799. All rows remain in feature source.

**Verification:** in_scope n_rows approximately equals 61,071,799; out_of_scope + in_scope = total.

---

### T02 — Duplicate analysis and deduplication rule

<!-- REVISED — replaced ORDER BY rowid with ORDER BY started (BLOCKER F01 fix) -->

**Objective:** Stratify duplicates in in-scope subset by profileId=-1 vs real
profileId. Produce rule R02.

**SQL:**

```sql
-- R02: Duplicate stratification (in-scope only)
WITH in_scope AS (
    SELECT *
    FROM matches_raw
    WHERE internalLeaderboardId IN (6, 18)
),
dup_groups AS (
    SELECT matchId, profileId, COUNT(*) AS row_count
    FROM in_scope
    GROUP BY matchId, profileId
    HAVING COUNT(*) > 1
)
SELECT
    CASE WHEN d.profileId = -1 THEN 'profileId_minus1' ELSE 'real_profileId' END AS stratum,
    COUNT(*) AS n_dup_groups,
    SUM(d.row_count) AS total_dup_rows,
    SUM(d.row_count) - COUNT(*) AS excess_rows
FROM dup_groups d
GROUP BY
    CASE WHEN d.profileId = -1 THEN 'profileId_minus1' ELSE 'real_profileId' END;
```

```sql
-- profileId=-1 investigation in 1v1 scope
SELECT
    COUNT(*) AS total_minus1_rows,
    COUNT(DISTINCT matchId) AS n_matches_with_minus1
FROM matches_raw
WHERE internalLeaderboardId IN (6, 18)
  AND profileId = -1;
```

**Cleaning rule R02:**
- Condition: Duplicate (matchId, profileId) rows; also any profileId=-1 rows
- Action: Keep first occurrence per matchId x profileId (by `started` timestamp,
  earliest wins); exclude all profileId=-1 rows (they carry no real player identity)
- Justification: aoe2companion API returns duplicate rows across daily dumps.
  01_03_02 showed profileId=-1 affects only 1 match in rm_1v1. Using `ORDER BY
  started` provides deterministic, semantically meaningful tie-breaking (earliest
  API dump wins). `rowid` is not reliable in DuckDB subquery context.
- Impact: Computed from query results.

**Verification:** profileId=-1 count in rm_1v1 is 0 or 1 (per 01_03_02).

---

### T03 — Match consistency check (won complement)

<!-- REVISED — replaced ORDER BY rowid with ORDER BY started (BLOCKER F01 fix) -->

**Objective:** Identify 2-row in-scope matches where won values are not
complementary. Produce rule R03.

**SQL:**

```sql
-- R03: Won consistency check (in-scope, 2-row matches only)
WITH in_scope_dedup AS (
    SELECT * EXCLUDE (rn)
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY matchId, profileId
                   ORDER BY started
               ) AS rn
        FROM matches_raw
        WHERE internalLeaderboardId IN (6, 18)
          AND profileId != -1
    ) sub
    WHERE rn = 1
),
match_pairs AS (
    SELECT
        matchId,
        COUNT(*) AS n_rows,
        COUNT(*) FILTER (WHERE won = TRUE) AS n_won_true,
        COUNT(*) FILTER (WHERE won = FALSE) AS n_won_false,
        COUNT(*) FILTER (WHERE won IS NULL) AS n_won_null
    FROM in_scope_dedup
    GROUP BY matchId
    HAVING COUNT(*) = 2
)
SELECT
    CASE
        WHEN n_won_true = 1 AND n_won_false = 1 THEN 'complementary'
        WHEN n_won_true = 2 THEN 'both_true'
        WHEN n_won_false = 2 THEN 'both_false'
        WHEN n_won_null > 0 THEN 'has_null'
        ELSE 'other'
    END AS won_pattern,
    COUNT(*) AS n_matches,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) AS pct
FROM match_pairs
GROUP BY won_pattern
ORDER BY n_matches DESC;
```

```sql
-- Non-2-row match counts in scope after dedup
WITH in_scope_dedup AS (
    SELECT * EXCLUDE (rn)
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY matchId, profileId
                   ORDER BY started
               ) AS rn
        FROM matches_raw
        WHERE internalLeaderboardId IN (6, 18)
          AND profileId != -1
    ) sub
    WHERE rn = 1
),
match_sizes AS (
    SELECT matchId, COUNT(*) AS n_rows FROM in_scope_dedup GROUP BY matchId
)
SELECT
    CASE WHEN n_rows = 1 THEN '1_row'
         WHEN n_rows = 2 THEN '2_rows'
         ELSE '3_plus_rows' END AS size_bucket,
    COUNT(*) AS n_matches,
    SUM(n_rows) AS total_rows
FROM match_sizes
GROUP BY size_bucket
ORDER BY size_bucket;
```

**Cleaning rule R03:**
- Condition: 2-row match where won not complementary; also 1-row and 3+ row matches
- Action: Exclude entire match (both rows)
- Justification: Zero-sum 1v1 game requires exactly one winner. Non-complementary
  won is unresolvable. 01_03_02 found ~2.5M both_true and ~1.9M both_false across
  full table.
- Impact: Computed from query results.

---

### T04 — NULL co-occurrence cluster investigation

<!-- REVISED — added temporal stratification monthly breakdown (WARNING W01 fix) -->

**Objective:** Determine whether ~428K NULL cluster is systematic early-API
gap or scattered. Produce rule R04. Temporal stratification confirms or
refutes the schema-change-era hypothesis.

**SQL:**

```sql
-- R04: NULL cluster temporal stratification (in-scope)
WITH in_scope AS (
    SELECT * FROM matches_raw WHERE internalLeaderboardId IN (6, 18)
),
null_cluster AS (
    SELECT
        matchId, started,
        CASE
            WHEN allowCheats IS NULL AND lockSpeed IS NULL AND lockTeams IS NULL
             AND recordGame IS NULL AND sharedExploration IS NULL
             AND teamPositions IS NULL AND teamTogether IS NULL
             AND turboMode IS NULL AND fullTechTree IS NULL AND population IS NULL
            THEN TRUE ELSE FALSE
        END AS is_null_cluster
    FROM in_scope
)
SELECT is_null_cluster, COUNT(*) AS n_rows,
       MIN(started) AS min_date, MAX(started) AS max_date,
       COUNT(DISTINCT DATE_TRUNC('month', started)) AS n_months
FROM null_cluster
GROUP BY is_null_cluster;
```

```sql
-- R04 addendum: monthly breakdown of NULL cluster (W01 temporal stratification)
WITH in_scope AS (
    SELECT * FROM matches_raw WHERE internalLeaderboardId IN (6, 18)
),
null_cluster AS (
    SELECT
        started,
        CASE
            WHEN allowCheats IS NULL AND lockSpeed IS NULL AND lockTeams IS NULL
             AND recordGame IS NULL AND sharedExploration IS NULL
             AND teamPositions IS NULL AND teamTogether IS NULL
             AND turboMode IS NULL AND fullTechTree IS NULL AND population IS NULL
            THEN TRUE ELSE FALSE
        END AS is_null_cluster
    FROM in_scope
)
SELECT
    DATE_TRUNC('month', started) AS month,
    COUNT(*) FILTER (WHERE is_null_cluster) AS null_cluster_rows,
    COUNT(*) FILTER (WHERE NOT is_null_cluster) AS normal_rows,
    ROUND(100.0 * COUNT(*) FILTER (WHERE is_null_cluster) / COUNT(*), 2) AS null_pct
FROM null_cluster
GROUP BY DATE_TRUNC('month', started)
ORDER BY month;
```

```sql
-- NULL cluster survival after R01+R02+R03
WITH in_scope_dedup AS (
    SELECT * EXCLUDE (rn)
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY matchId, profileId ORDER BY started) AS rn
        FROM matches_raw
        WHERE internalLeaderboardId IN (6, 18) AND profileId != -1
    ) sub
    WHERE rn = 1
),
valid_matches AS (
    SELECT matchId FROM in_scope_dedup
    GROUP BY matchId
    HAVING COUNT(*) = 2
       AND COUNT(*) FILTER (WHERE won = TRUE) = 1
       AND COUNT(*) FILTER (WHERE won = FALSE) = 1
)
SELECT
    CASE
        WHEN d.allowCheats IS NULL AND d.lockSpeed IS NULL AND d.lockTeams IS NULL
         AND d.recordGame IS NULL AND d.sharedExploration IS NULL
         AND d.teamPositions IS NULL AND d.teamTogether IS NULL
         AND d.turboMode IS NULL AND d.fullTechTree IS NULL AND d.population IS NULL
        THEN 'null_cluster' ELSE 'normal'
    END AS cluster_status,
    COUNT(*) AS n_rows,
    COUNT(DISTINCT d.matchId) AS n_matches
FROM in_scope_dedup d
INNER JOIN valid_matches v ON d.matchId = v.matchId
GROUP BY cluster_status;
```

**Decision logic:**
- If NULL cluster concentrated in <= 6 contiguous months AND < 5% of clean
  data: FLAG only (`is_null_cluster = TRUE`). Justification: temporal
  concentration confirms schema-change MNAR; affected columns near-constant
  in 1v1 ranked play (I9).
- If NULL cluster spans > 12 months or > 5% of clean data: investigate
  further before finalizing R04.
- **Empirical result to document:** Monthly breakdown stored in artifact JSON
  under `null_cluster_monthly_breakdown`.

**Cleaning rule R04:**
- Condition: All 10 game-settings columns simultaneously NULL
- Action: FLAG only (`is_null_cluster = TRUE`) — conditional on temporal concentration
- Justification: MNAR schema-change; temporal concentration verified monthly.
- Impact: Computed from query results.

---

### T05 — ratings_raw.games outlier capping

**Objective:** Define empirical cap for ratings_raw.games. Produce rule R05.

**SQL:**

```sql
SELECT
    COUNT(*) AS total_rows,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY games) AS p99,
    PERCENTILE_CONT(0.999) WITHIN GROUP (ORDER BY games) AS p999,
    PERCENTILE_CONT(0.9999) WITHIN GROUP (ORDER BY games) AS p9999,
    MAX(games) AS max_val,
    COUNT(*) FILTER (WHERE games > 50000) AS n_above_50k,
    COUNT(*) FILTER (WHERE games > 100000) AS n_above_100k,
    COUNT(*) FILTER (WHERE games > 1000000) AS n_above_1M
FROM ratings_raw;
```

**Cleaning rule R05:**
- Condition: `ratings_raw.games > {p999_value}` (computed above)
- Action: Winsorize to p99.9 in `ratings_clean` VIEW
- Justification: Max=1,775,260,795 is physically impossible; p99.9 derived empirically (I7).
- Impact: Computed from query results.

**VIEW definition:**

```sql
CREATE OR REPLACE VIEW ratings_clean AS
SELECT
    profile_id, LEAST(games, {p999_value}) AS games,
    rating, date, leaderboard_id, rating_diff, season, filename
FROM ratings_raw;
```

---

### T06 — Create player_history_all VIEW

<!-- REVISED — entirely new task (prediction scope != feature scope constraint) -->

**Objective:** Create a player-row-oriented VIEW over the full `matches_raw`
table (all game types) as the input for player-level aggregate feature
computation in 01_05. Applies only minimal quality filters. Produce rule R00.

**Design rationale:**
- aoe2companion has no separate `players_raw` table. Player data is embedded
  directly in `matches_raw` (one row per player per match).
- No game-type restriction: all leaderboards included.
- I5 (symmetric player treatment): VIEW is keyed on `profileId`, one row per
  player per match. No wide-format pivoting.
- I3 (temporal discipline): VIEW exposes `started` as temporal anchor.
  Downstream queries add `WHERE ph.started < target_match.started`.
- POST-GAME columns `ratingDiff` and `finished` are excluded.
- `rating` retained (confirmed PRE-GAME, 01_03_03: 99.8%).
- Only `profileId = -1` rows excluded.

**SQL:**

```sql
CREATE OR REPLACE VIEW player_history_all AS
WITH deduped AS (
    SELECT * EXCLUDE (rn)
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY matchId, profileId
                   ORDER BY started
               ) AS rn
        FROM matches_raw
        WHERE profileId != -1
    ) sub
    WHERE rn = 1
)
SELECT
    matchId,
    profileId,
    name,
    started,
    leaderboard,
    internalLeaderboardId,
    map,
    civ,
    rating,
    color,
    slot,
    team,
    startingAge,
    gameMode,
    speed,
    won,
    country,
    status,
    verified,
    filename
FROM deduped;
```

**Columns explicitly excluded:**
- `ratingDiff` — POST-GAME (rating change after match; I3 leakage prevention)
- `finished` — POST-GAME (game end timestamp; I3 leakage prevention)

**Cleaning rule R00 (feature history scope):**
- Condition: Full `matches_raw`, all game types, excluding `profileId = -1` and duplicates
- Action: Create VIEW `player_history_all` as feature computation source
- Justification: Player features computed from full recorded history. Restricting
  to 1v1 would compound selection bias without eliminating it.
- Impact: ~268M rows (277M minus ~8.8M duplicates minus ~19K anonymous).

**Verification:**
- `SELECT COUNT(*), COUNT(DISTINCT matchId), COUNT(DISTINCT profileId) FROM player_history_all`
- No `ratingDiff` column: `SELECT column_name FROM information_schema.columns WHERE table_name='player_history_all' AND column_name = 'ratingDiff'` → 0 rows
- No `finished` column: same → 0 rows
- No `profileId = -1`: `SELECT COUNT(*) FROM player_history_all WHERE profileId = -1` → 0
- Leaderboard diversity: `SELECT DISTINCT leaderboard FROM player_history_all` shows all game types

**Schema YAML (write after verification):**

Write `src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/player_history_all.yaml`
using column list from `DESCRIBE player_history_all` output. Template:

```yaml
table: player_history_all
dataset: aoe2companion
game: aoe2
object_type: view
step: "01_04_01"
row_count: <fill from V6 COUNT(*)>
describe_artifact: src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json
generated_date: '<YYYY-MM-DD>'
columns:
  # Fill from DESCRIBE player_history_all — annotate each column with:
  #   description: human-readable purpose
  #   notes: I3 classification (PRE_GAME / CONTEXT / TARGET / IDENTITY)
  #          and any invariant references (e.g. "I3: temporal anchor")
provenance:
  source_tables: [matches_raw]
  filter: "profileId != -1; deduplicated by (matchId, profileId) ORDER BY started"
  scope: "All game types (no leaderboard restriction). Prediction scope != feature scope."
  created_by: sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_01_data_cleaning.py
invariants:
  - id: I3
    description: "POST-GAME columns ratingDiff and finished excluded. Temporal anchor
      (started) exposed for downstream WHERE ph.started < target_match.started."
  - id: I5
    description: "Player-row-oriented (one row per player per match). No slot-based
      pivoting. profileId is the identity key."
  - id: I6
    description: "VIEW DDL stored verbatim in 01_04_01_data_cleaning.json sql_queries."
  - id: I9
    description: "No features computed. VIEW is a filtered projection of matches_raw."
```

---

### T07 — Create matches_1v1_clean VIEW

<!-- REVISED — replaced ORDER BY rowid with ORDER BY started (BLOCKER F01 fix); renumbered from T06 -->

**Objective:** Compose all prediction-target cleaning rules R01–R04 into
`matches_1v1_clean` VIEW.

**SQL:**

```sql
CREATE OR REPLACE VIEW matches_1v1_clean AS
WITH
deduped AS (
    SELECT * EXCLUDE (rn)
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY matchId, profileId
                   ORDER BY started
               ) AS rn
        FROM matches_raw
        WHERE internalLeaderboardId IN (6, 18)
          AND profileId != -1
    ) sub
    WHERE rn = 1
),
valid_match_ids AS (
    SELECT matchId FROM deduped
    GROUP BY matchId
    HAVING COUNT(*) = 2
       AND COUNT(*) FILTER (WHERE won = TRUE) = 1
       AND COUNT(*) FILTER (WHERE won = FALSE) = 1
),
cleaned AS (
    SELECT
        d.*,
        CASE
            WHEN d.allowCheats IS NULL AND d.lockSpeed IS NULL AND d.lockTeams IS NULL
             AND d.recordGame IS NULL AND d.sharedExploration IS NULL
             AND d.teamPositions IS NULL AND d.teamTogether IS NULL
             AND d.turboMode IS NULL AND d.fullTechTree IS NULL AND d.population IS NULL
            THEN TRUE ELSE FALSE
        END AS is_null_cluster
    FROM deduped d
    INNER JOIN valid_match_ids v ON d.matchId = v.matchId
)
SELECT * FROM cleaned;
```

**Verification:**
- `SELECT COUNT(*), COUNT(DISTINCT matchId) FROM matches_1v1_clean`
- won distribution exactly 50/50 (by construction of R03)
- Only internalLeaderboardId 6 and 18 present

---

### T08 — Post-cleaning validation and CONSORT flow

<!-- REVISED — V2 checks ratingDiff and finished instead of non-existent columns (BLOCKER F02 fix); added player_history_all validation -->

**Objective:** CONSORT flow counts, post-cleaning validation checks, artifact production.

**CONSORT flow SQL:**

```sql
WITH
stage_0_raw AS (SELECT COUNT(*) AS n_rows, COUNT(DISTINCT matchId) AS n_matches FROM matches_raw),
stage_1_scope AS (SELECT COUNT(*) AS n_rows, COUNT(DISTINCT matchId) AS n_matches
    FROM matches_raw WHERE internalLeaderboardId IN (6, 18)),
stage_2_dedup AS (SELECT COUNT(*) AS n_rows, COUNT(DISTINCT matchId) AS n_matches
    FROM (SELECT matchId, ROW_NUMBER() OVER (PARTITION BY matchId, profileId ORDER BY started) AS rn
          FROM matches_raw WHERE internalLeaderboardId IN (6, 18) AND profileId != -1) sub WHERE rn = 1),
stage_3_valid AS (SELECT COUNT(*) AS n_rows, COUNT(DISTINCT matchId) AS n_matches FROM matches_1v1_clean)
SELECT 'S0_raw' AS stage, n_rows, n_matches FROM stage_0_raw
UNION ALL SELECT 'S1_scope_restricted', n_rows, n_matches FROM stage_1_scope
UNION ALL SELECT 'S2_deduplicated', n_rows, n_matches FROM stage_2_dedup
UNION ALL SELECT 'S3_valid_complementary', n_rows, n_matches FROM stage_3_valid;
```

**Validation checks:**

```sql
-- V1: Rating coverage
SELECT COUNT(*) AS total, COUNT(rating) AS n_non_null,
       ROUND(100.0*COUNT(rating)/COUNT(*),2) AS rating_coverage_pct
FROM matches_1v1_clean;

-- V2: No POST-GAME leakage columns in player_history_all (I3)
-- REVISED: checks actual aoe2companion POST-GAME columns per 01_03_03
SELECT column_name FROM information_schema.columns
WHERE table_name='player_history_all'
  AND column_name IN ('ratingDiff', 'finished');
-- Expected: 0 rows

-- V3: Rating sanity
SELECT COUNT(*) FILTER (WHERE rating < 0) AS n_negative FROM matches_1v1_clean;

-- V4: Leaderboard distribution
SELECT leaderboard, internalLeaderboardId, COUNT(*) AS n_rows
FROM matches_1v1_clean GROUP BY leaderboard, internalLeaderboardId;

-- V5: NULL cluster proportion
SELECT is_null_cluster, COUNT(*) AS n_rows,
       ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),4) AS pct
FROM matches_1v1_clean GROUP BY is_null_cluster;

-- V6: player_history_all basic counts
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT matchId) AS n_matches,
       COUNT(DISTINCT profileId) AS n_players, COUNT(DISTINCT leaderboard) AS n_leaderboards
FROM player_history_all;

-- V7: player_history_all has no anonymous players
SELECT COUNT(*) AS n_anonymous FROM player_history_all WHERE profileId = -1;
-- Expected: 0

-- V8: player_history_all leaderboard diversity
SELECT leaderboard, COUNT(*) AS n_rows FROM player_history_all
GROUP BY leaderboard ORDER BY n_rows DESC;
```

---

## File Manifest

| File | Action |
|------|--------|
| `sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_01_data_cleaning.py` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_01_data_cleaning.ipynb` | Create (jupytext-paired) |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/player_history_all.yaml` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md` | Update |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml` | Update |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` | Update |

## Gate Condition

- `01_04_01_data_cleaning.json` exists; contains cleaning_registry (R00–R05),
  consort_flow, post_cleaning_validation, sql_queries (all verbatim, I6).
- `matches_1v1_clean` VIEW queryable; returns rows.
- `player_history_all` VIEW queryable; returns rows; covers all leaderboard types.
- `ratings_clean` VIEW queryable; returns rows.
- won distribution in `matches_1v1_clean` is exactly 50/50.
- V2 (no POST-GAME leakage in `player_history_all`) returns 0 rows.
  Specifically: `ratingDiff` and `finished` absent from `player_history_all`.
- V7 confirms 0 anonymous rows in `player_history_all`.
- `null_cluster_monthly_breakdown` populated in artifact JSON.
- `schemas/views/player_history_all.yaml` exists; `object_type: view`; `row_count` populated.
- `STEP_STATUS.yaml` has `01_04_01: complete`.

## Out of Scope

- Feature engineering (Phase 02, I9).
- Rating imputation (Phase 02).
- Materialized tables — cleaning layer is VIEWs only.
- profiles_raw or leaderboards_raw cleaning (NOT_USABLE per 01_03_03).
- Computing player-level aggregate features from `player_history_all` (01_05 / Phase 02).

## Open Questions

- **Q1:** NULL cluster temporal concentration confirmed or scattered? Resolves by T04.
- **Q2:** Exact p99.9 value for ratings_raw.games? Resolves by T05.
- **Q3:** profileId=-1 count in rm_1v1? Resolves by T02.
- **Q4:** Player and match count in `player_history_all`? Resolves by T08 V6.

## Scientific Invariants

| # | Invariant | How upheld |
|---|-----------|------------|
| I3 | No post-game features | `player_history_all` excludes `ratingDiff` and `finished`. V2 validates. Downstream feature queries enforce temporal window via `started`. |
| I5 | Symmetric player treatment | `player_history_all` is player-row-oriented, keyed on `profileId`. No wide-format pivoting. Both players represented identically. |
| I6 | All SQL verbatim | Every query in T01–T08 stored as literal string in notebook and MD artifact. |
| I7 | No magic numbers | R01: IDs 6/18 from 01_03_02. R05: p99.9 computed empirically. R04 temporal threshold documented as decision logic. |
| I9 | Step scope | Cleaning only. `player_history_all` is a VIEW definition, not feature computation. |

---

**Adversarial critique required before execution begins.**
