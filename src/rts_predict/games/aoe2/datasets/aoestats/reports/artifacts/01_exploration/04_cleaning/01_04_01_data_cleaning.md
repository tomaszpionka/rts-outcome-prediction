# 01_04_01 Data Cleaning -- aoestats

**Dataset:** aoestats | **Step:** 01_04_01 | **Date:** 2026-04-16

## Cleaning Registry

| Rule | Condition | Action | Impact |
|------|-----------|--------|--------|
| R00 | Scope definition for player feature computation source | CREATE VIEW player_history_all -- all game types, all leaderboards | 107,626,399 rows in feature computation source |
| R01 | profile_id IS DOUBLE in players_raw | CAST to BIGINT in analytical VIEWs | 0 rows affected; all values exact integers in safe range |
| R02 | player_count != 2 OR leaderboard != 'random_map' | EXCLUDE from matches_1v1_clean VIEW (prediction target only) | 17,815,944 matches retained in prediction VIEW |
| R03 | game_id in matches_raw with no rows in players_raw | EXCLUDE (implicit via INNER JOIN in matches_1v1_clean and player_history_all VIEWs) | 212,890 matches (0.69%) |
| R04 | game_type = 'random_map' (100%), game_speed = 'normal' (100%) | EXCLUDE columns from VIEWs | 0 rows; 2 columns removed |
| R05 | starting_age: 99.99994% 'dark', 19 rows 'standard' | EXCLUDE column from VIEWs | 0 rows; 1 column removed |
| R06 | new_rating is POST-GAME (computed after match completes) | EXCLUDE from both VIEWs (I3 violation) | 0 rows; 1 column per player excluded from both VIEWs |
| R07 | game_id has 2 player rows with identical team values | VERIFIED 0-IMPACT ASSERTION. COUNT(DISTINCT team) = 2 predicate in ranked_1v1 CTE handles this. | same_team_game_count = 0 (assertion confirmed; no exclusion needed) |
| R08 | p0_winner = p1_winner (both True or both False) | EXCLUDE from matches_1v1_clean (WHERE p0.winner != p1.winner predicate) | 997 rows excluded from matches_1v1_clean |

## CONSORT Flow (matches_1v1_clean)

- Stage 0 (all matches): 30,690,651
- Stage 1 (has player rows): 30,477,761
- Stage 2 (structural 1v1): 18,438,769
- Stage 3 (ranked 1v1, distinct teams): 17,815,944
- Stage 4 (final VIEW, inconsistent winners excluded): 17,814,947
- player_history_all rows: 107,626,399

## Temporal Schema Analysis

- Total weeks analysed: 171
- Last week with opening > 1%: 2024-03-10
- First week with opening = 0%: 2024-03-17
- Feature-inclusion decision deferred to Phase 02 (I9).

## Same-Team Assertion

- same_team_game_count: 0
- Outcome: 0-impact assertion verified. No same-team games found.

## Team-Assignment Asymmetry (I5 Warning)

- t1_wins: 9,311,364
- t0_wins: 8,503,583
- t1_win_pct: 52.27%

**WARNING:** p0 (team=0) and p1 (team=1) are NOT symmetric player slots.
Downstream 01_05+ feature engineering MUST apply player-slot randomisation.

## Post-Cleaning Validation Results

- ratings_raw_exists: 0 (PASS)
- inconsistent winner rows: 0 (PASS)
- p0_profile_id, p1_profile_id, profile_id: all BIGINT (PASS)

## NULL Audit

### matches_1v1_clean

Total rows: 17,814,947

| Column | NULL Count | NULL % |
|--------|-----------|--------|
| game_id | 0 | 0.0% |
| started_timestamp | 0 | 0.0% |
| leaderboard | 0 | 0.0% |
| map | 0 | 0.0% |
| mirror | 0 | 0.0% |
| num_players | 0 | 0.0% |
| patch | 0 | 0.0% |
| raw_match_type | 7,055 | 0.0396% |
| replay_enhanced | 0 | 0.0% |
| avg_elo | 0 | 0.0% |
| team_0_elo | 0 | 0.0% |
| team_1_elo | 0 | 0.0% |
| p0_profile_id | 0 | 0.0% |
| p0_civ | 0 | 0.0% |
| p0_old_rating | 0 | 0.0% |
| p0_winner | 0 | 0.0% |
| p1_profile_id | 0 | 0.0% |
| p1_civ | 0 | 0.0% |
| p1_old_rating | 0 | 0.0% |
| p1_winner | 0 | 0.0% |
| team1_wins | 0 | 0.0% |

Zero-NULL assertions passed: game_id, started_timestamp, p0_profile_id, p1_profile_id, p0_winner, p1_winner

### player_history_all

Total rows: 107,626,399

| Column | NULL Count | NULL % |
|--------|-----------|--------|
| profile_id | 0 | 0.0% |
| game_id | 0 | 0.0% |
| started_timestamp | 0 | 0.0% |
| leaderboard | 0 | 0.0% |
| map | 0 | 0.0% |
| patch | 0 | 0.0% |
| player_count | 0 | 0.0% |
| mirror | 0 | 0.0% |
| replay_enhanced | 0 | 0.0% |
| civ | 0 | 0.0% |
| team | 0 | 0.0% |
| old_rating | 0 | 0.0% |
| winner | 0 | 0.0% |

Zero-NULL assertions passed: profile_id, game_id, started_timestamp

**FINDING:** `winner` has 0 NULLs (0.0%). Expected: VIEW covers all game types including non-decisive matches.

## VIEW DDL

### matches_1v1_clean

```sql
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
```

### player_history_all

```sql
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
```

## Missingness Ledger

### matches_1v1_clean

Total rows: 17,814,947 | Ledger rows: 21

| Column | dtype | n_null | pct_null | sentinel_value | n_sentinel | pct_sentinel | pct_missing_total | mechanism | recommendation | carries_semantic | is_primary |
|--------|-------|--------|---------|----------------|-----------|-------------|------------------|-----------|---------------|-----------------|-----------|
| game_id | VARCHAR | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| started_timestamp | TIMESTAMP WITH TIME ZONE | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| leaderboard | VARCHAR | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | DROP_COLUMN | False | False |
| map | VARCHAR | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| mirror | BOOLEAN | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| num_players | BIGINT | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | DROP_COLUMN | False | False |
| patch | BIGINT | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| raw_match_type | DOUBLE | 7,055 | 0.0396 | nan | 0 | 0.0 | 0.0396 | MCAR | RETAIN_AS_IS | False | False |
| replay_enhanced | BOOLEAN | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| avg_elo | DOUBLE | 0 | 0.0 | 0 | 118 | 0.0007 | 0.0007 | MAR | CONVERT_SENTINEL_TO_NULL | True | True |
| team_0_elo | DOUBLE | 0 | 0.0 | -1 | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | True |
| team_1_elo | DOUBLE | 0 | 0.0 | -1 | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | True |
| p0_profile_id | BIGINT | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| p0_civ | VARCHAR | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| p0_old_rating | BIGINT | 0 | 0.0 | 0 | 4,730 | 0.0266 | 0.0266 | MAR | CONVERT_SENTINEL_TO_NULL | True | True |
| p0_winner | BOOLEAN | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| p1_profile_id | BIGINT | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| p1_civ | VARCHAR | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| p1_old_rating | BIGINT | 0 | 0.0 | 0 | 188 | 0.0011 | 0.0011 | MAR | CONVERT_SENTINEL_TO_NULL | True | True |
| p1_winner | BOOLEAN | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| team1_wins | BOOLEAN | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |

### player_history_all

Total rows: 107,626,399 | Ledger rows: 13

| Column | dtype | n_null | pct_null | sentinel_value | n_sentinel | pct_sentinel | pct_missing_total | mechanism | recommendation | carries_semantic | is_primary |
|--------|-------|--------|---------|----------------|-----------|-------------|------------------|-----------|---------------|-----------------|-----------|
| profile_id | BIGINT | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| game_id | VARCHAR | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| started_timestamp | TIMESTAMP WITH TIME ZONE | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| leaderboard | VARCHAR | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| map | VARCHAR | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| patch | BIGINT | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| player_count | BIGINT | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| mirror | BOOLEAN | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| replay_enhanced | BOOLEAN | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| civ | VARCHAR | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| team | BIGINT | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |
| old_rating | BIGINT | 0 | 0.0 | 0 | 5,937 | 0.0055 | 0.0055 | MAR | CONVERT_SENTINEL_TO_NULL | True | True |
| winner | BOOLEAN | 0 | 0.0 | nan | 0 | 0.0 | 0.0 | N/A | RETAIN_AS_IS | False | False |

## Decisions Surfaced for Downstream Cleaning (01_04_02+)

### DS-AOESTATS-01: team_0_elo / team_1_elo (sentinel=-1, absent in 1v1 filtered scope)

team_0_elo / team_1_elo: ELO=-1 sentinel ABSENT in matches_1v1_clean (upstream filter excludes the rows that carried it — the matches_1v1_clean WHERE clause restricts to ranked-1v1 decisive games where the sentinel does not appear). Ledger reports n_sentinel=0 → RETAIN_AS_IS / mechanism=N/A. Action item: if the ranked-1v1 scope is ever broadened, or if a different VIEW (e.g. unranked or non-1v1) is added to the audit, re-audit for sentinel resurfacing and reapply CONVERT_SENTINEL_TO_NULL via Rule S3. The spec entry retains mechanism=MCAR / sentinel_value=-1 to document the design intent for the mechanism (raw matches_raw evidence shows the sentinel exists at low rate); the ledger reflects the empirical post-filter observation.

### DS-AOESTATS-02: p0_old_rating / p1_old_rating (sentinel=0, n_zero=5,937 in players_raw)

NULLIF + listwise deletion per Rule S3 in 01_04_02+ DDL pass, OR retain 0 as explicit unrated categorical encoding alongside is_unrated? B6 deferral: audit recommends CONVERT_SENTINEL_TO_NULL (non-binding for carries_semantic_content=True). Downstream chooses.

### DS-AOESTATS-03: avg_elo (n_sentinel=118 in matches_1v1_clean / n_zero=121 in matches_raw)

avg_elo: n_sentinel=118 in matches_1v1_clean / n_zero=121 in matches_raw (numeric_stats_matches[label='avg_elo'] ground truth). Same MAR / CONVERT_SENTINEL_TO_NULL recommendation; the 3-row difference is the upstream 1v1 filter discarding 3 sentinel rows. Disposition (genuine zero vs sentinel) deferred to 01_04_02+ join investigation. Note: the n_zero=4,824 figure cited in earlier drafts belongs to team_0_elo, NOT avg_elo.

### DS-AOESTATS-04: raw_match_type (NULLs in matches_raw ~0.04%)

MCAR per Rule S3, listwise deletion candidate at 01_04_02+. Column may be redundant given internalLeaderboardId already constrains scope.

### DS-AOESTATS-05: team1_wins (prediction target, BIGINT)

0 NULLs verified (upstream WHERE p0.winner != p1.winner exclusion). F1 zero-missingness override → RETAIN_AS_IS / mechanism=N/A.

### DS-AOESTATS-06: winner in player_history_all

winner in player_history_all: ledger reports 0 NULLs / RETAIN_AS_IS / mechanism=N/A (better than plan-anticipated ~5% rate). The upstream players_raw filtering or the players_raw schema does not produce NULL winners in the loaded dataset. CONSORT note: re-verify on every dataset re-load; if winner NULLs surface in future loads, the target-override post-step (B4) will fire automatically and convert recommendation to EXCLUDE_TARGET_NULL_ROWS — no Phase 02 code change required.

### DS-AOESTATS-07: overviews_raw (singleton metadata, 1 row)

Formally declare out-of-analytical-scope at 01_04_02+ disposition step. Not used by any VIEW.

### DS-AOESTATS-08: leaderboard, num_players (constants in matches_1v1_clean)

leaderboard and num_players detected as TRUE constants (n_distinct=1) in matches_1v1_clean by the runtime constants-detection branch (W7 fix). Recommendation: DROP_COLUMN per Rule S4 / N/A-mechanism. Both columns are constant-by-construction in the cleaned scope: matches_1v1_clean filters to leaderboard='random_map' and num_players=2. Confirm drop in 01_04_02+ DDL pass.

