# 01_04_01 Data Cleaning -- aoestats

**Dataset:** aoestats | **Step:** 01_04_01 | **Date:** 2026-04-16

## Cleaning Registry

| Rule | Condition | Action | Impact |
|------|-----------|--------|--------|
| R00 | Scope definition for player feature computation source | CREATE VIEW player_history_all -- all game types, all leaderboards | 107,626,399 rows in feature computation source |
| R01 | profile_id IS DOUBLE in players_raw | CAST to BIGINT in analytical VIEWs | 0 rows affected; all values exact integers in safe range |
| R02 | player_count != 2 OR leaderboard != 'random_map' | EXCLUDE from matches_1v1_clean VIEW (prediction target only) | 17,815,944 matches retained in prediction VIEW |
| R03 | game_id in matches_raw with no rows in players_raw | EXCLUDE (implicit via INNER JOIN in T06 and T07 VIEWs) | 212,890 matches (0.69%) |
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

## T05 Temporal Schema Analysis

- Total weeks analysed: 171
- Last week with opening > 1%: 2024-03-10
- First week with opening = 0%: 2024-03-17
- Feature-inclusion decision deferred to Phase 02 (I9).

## T06 Same-Team Assertion (W02)

- same_team_game_count: 0
- Outcome: 0-impact assertion verified. No same-team games found.

## T06 Team-Assignment Asymmetry (W01 / I5 Warning)

- t1_wins: 9,311,364
- t0_wins: 8,503,583
- t1_win_pct: 52.27%

**WARNING:** p0 (team=0) and p1 (team=1) are NOT symmetric player slots.
Downstream 01_05+ feature engineering MUST apply player-slot randomisation.

## T08 Validation Results

- ratings_raw_exists: 0 (PASS)
- inconsistent winner rows: 0 (PASS)
- p0_profile_id, p1_profile_id, profile_id: all BIGINT (PASS)

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
    CAST(p0.profile_id AS BIGINT) AS p0_profile_id,
    p0.civ AS p0_civ,
    p0.old_rating AS p0_old_rating,
    p0.match_rating_diff AS p0_match_rating_diff,
    p0.winner AS p0_winner,
    p0.opening AS p0_opening,
    p0.feudal_age_uptime AS p0_feudal_age_uptime,
    p0.castle_age_uptime AS p0_castle_age_uptime,
    p0.imperial_age_uptime AS p0_imperial_age_uptime,
    CAST(p1.profile_id AS BIGINT) AS p1_profile_id,
    p1.civ AS p1_civ,
    p1.old_rating AS p1_old_rating,
    p1.match_rating_diff AS p1_match_rating_diff,
    p1.winner AS p1_winner,
    p1.opening AS p1_opening,
    p1.feudal_age_uptime AS p1_feudal_age_uptime,
    p1.castle_age_uptime AS p1_castle_age_uptime,
    p1.imperial_age_uptime AS p1_imperial_age_uptime,
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
    p.match_rating_diff,
    p.winner
FROM players_raw p
INNER JOIN matches_raw m ON p.game_id = m.game_id
INNER JOIN player_counts pc ON p.game_id = pc.game_id
WHERE p.profile_id IS NOT NULL
  AND m.started_timestamp IS NOT NULL
```
