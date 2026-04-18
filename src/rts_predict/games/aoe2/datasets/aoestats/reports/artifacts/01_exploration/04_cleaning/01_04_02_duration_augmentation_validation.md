# Step 01_04_02 ADDENDUM -- duration_seconds + is_duration_suspicious

**Generated:** 2026-04-18
**Dataset:** aoestats
**Addendum to:** 01_04_02 Data Cleaning Execution

## Summary

Extends `matches_1v1_clean` from 20 cols -> 22 cols by adding:
- `duration_seconds` BIGINT (POST_GAME_HISTORICAL): match duration in seconds.
  Derived from `matches_raw.duration` (Arrow duration[ns] -> BIGINT nanoseconds per DuckDB 1.5.1).
  Divisor: 1,000,000,000 (cites `aoestats/pre_ingestion.py:271`).
- `is_duration_suspicious` BOOLEAN: TRUE where `duration_seconds > 86400` (24h threshold).
  Threshold cites I8 cross-dataset contract and 01_04_03 Gate+5b empirical finding.

Row count: 17,814,947 (unchanged).

## Duration Statistics

| Metric | Value |
|---|---|
| total_rows | 17,814,947 |
| null_duration | 0 |
| min_duration_seconds | 3s |
| p50_duration_seconds | 2,455s (~40.9 min) |
| p99_duration_seconds | 5,729s (~95.5 min) |
| max_duration_seconds | 5,574,815s (~64.5 days) |
| suspicious_count (>86400s) | 28 |

## Suspicious Matches (duration_seconds > 86400)

| game_id | duration_seconds | duration_days | started_timestamp |
|---|---|---|---|
| 184213201 | 5,574,815 | 64.52 | 2022-10-07 23:52:25+02:00 |
| 210909036 | 709,915 | 8.22 | 2023-02-16 18:49:50+01:00 |
| 226137454 | 622,652 | 7.21 | 2023-04-13 20:00:19+02:00 |
| 241569078 | 370,496 | 4.29 | 2023-06-20 05:56:05+02:00 |
| 227257584 | 283,322 | 3.28 | 2023-04-18 01:03:34+02:00 |
| 244145426 | 271,351 | 3.14 | 2023-07-02 18:51:23+02:00 |
| 224419110 | 237,208 | 2.75 | 2023-04-07 00:48:16+02:00 |
| 235233012 | 166,736 | 1.93 | 2023-05-21 20:52:11+02:00 |
| 273616079 | 157,111 | 1.82 | 2023-11-22 20:46:53+01:00 |
| 184214845 | 155,873 | 1.80 | 2022-10-08 00:04:55+02:00 |
| 219924027 | 154,692 | 1.79 | 2023-03-20 13:12:40+01:00 |
| 242789766 | 153,291 | 1.77 | 2023-06-26 03:36:48+02:00 |
| 235404820 | 133,632 | 1.55 | 2023-05-22 16:04:08+02:00 |
| 273614808 | 126,968 | 1.47 | 2023-11-22 20:41:07+01:00 |
| 223818079 | 124,438 | 1.44 | 2023-04-04 15:17:54+02:00 |
| 238496974 | 120,967 | 1.40 | 2023-06-05 05:58:29+02:00 |
| 273656044 | 116,220 | 1.35 | 2023-11-23 00:05:56+01:00 |
| 273612539 | 114,978 | 1.33 | 2023-11-22 20:30:54+01:00 |
| 245201048 | 107,765 | 1.25 | 2023-07-07 20:13:28+02:00 |
| 254497180 | 106,738 | 1.24 | 2023-08-20 20:54:45+02:00 |
| 197011156 | 106,160 | 1.23 | 2022-12-22 00:50:30+01:00 |
| 220017180 | 104,047 | 1.20 | 2023-03-20 21:03:18+01:00 |
| 230860138 | 102,401 | 1.19 | 2023-05-03 04:22:02+02:00 |
| 244930104 | 100,200 | 1.16 | 2023-07-06 13:18:49+02:00 |
| 242215301 | 99,639 | 1.15 | 2023-06-23 16:28:15+02:00 |
| 221016323 | 96,412 | 1.12 | 2023-03-25 01:33:06+01:00 |
| 230239118 | 92,500 | 1.07 | 2023-04-30 19:26:03+02:00 |
| 239720673 | 88,448 | 1.02 | 2023-06-11 04:20:46+02:00 |

## Gate Results

| Gate | Status |
|---|---|
| gate_1_col_count_22 | PASS |
| gate_1b_last2_cols_correct | PASS |
| gate_2_row_count_17814947 | PASS |
| gate_3_duration_null_count_0 | PASS |
| gate_4_max_duration_le_1e9 | PASS |
| gate_5_suspicious_count_28_pm1 | PASS |

## SQL Queries (Invariant I6)

All DDL and assertion SQL stored verbatim in `01_04_02_duration_augmentation_validation.json`
under the `sql_queries` key.

### CREATE OR REPLACE VIEW matches_1v1_clean (v3, 22 cols)

```sql

CREATE OR REPLACE VIEW matches_1v1_clean AS
-- Purpose: Prediction-target VIEW. Ranked 1v1 decisive matches only.
-- Row multiplicity: 1 row per match (NOT 2-per-match like sc2egset matches_flat_clean).
-- Target column: team1_wins (BOOLEAN; 0/1 strict -- no Undecided/Tie analog in aoestats).
-- Column set: 22 cols (post ADDENDUM 2026-04-18: +duration_seconds, +is_duration_suspicious).
-- Predecessor: v2 (20 cols, 01_04_02 2026-04-17); all DS-AOESTATS-01..08 applied.
-- I3: duration_seconds is POST_GAME_HISTORICAL -- safe only for history aggregation (match_time < T).
-- I7: 86400s threshold = cross-dataset 24h canary (~25x p99); cites 01_04_03 Gate+5b.
-- I7: 1_000_000_000 divisor cites aoestats/pre_ingestion.py:271 (Arrow duration[ns] -> BIGINT).
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
    -- IDENTITY
    m.game_id,
    m.started_timestamp,

    -- DS-AOESTATS-08: leaderboard DROPPED (constant n_distinct=1 in this scope)
    m.map,
    m.mirror,
    -- DS-AOESTATS-08: num_players DROPPED (constant n_distinct=1 in this scope)
    m.patch,
    -- DS-AOESTATS-04: raw_match_type DROPPED (n_distinct=1; redundant with upstream filter)
    m.replay_enhanced,

    -- ELO (DS-AOESTATS-03: avg_elo NULLIF applied)
    NULLIF(m.avg_elo, 0) AS avg_elo,
    -- DS-AOESTATS-01: team_0_elo / team_1_elo RETAIN_AS_IS (sentinel=-1 absent in scope)
    m.team_0_elo,
    m.team_1_elo,

    -- Player 0 (DS-AOESTATS-02: NULLIF + is_unrated indicator)
    CAST(p0.profile_id AS BIGINT) AS p0_profile_id,
    p0.civ AS p0_civ,
    NULLIF(p0.old_rating, 0) AS p0_old_rating,
    (p0.old_rating = 0) AS p0_is_unrated,
    p0.winner AS p0_winner,

    -- Player 1 (DS-AOESTATS-02: symmetric NULLIF + is_unrated)
    CAST(p1.profile_id AS BIGINT) AS p1_profile_id,
    p1.civ AS p1_civ,
    NULLIF(p1.old_rating, 0) AS p1_old_rating,
    (p1.old_rating = 0) AS p1_is_unrated,
    p1.winner AS p1_winner,

    -- TARGET (DS-AOESTATS-05: RETAIN_AS_IS, F1 override)
    p1.winner AS team1_wins,

    -- ADDENDUM 2026-04-18: duration cols (POST_GAME_HISTORICAL; I3 safe for history only)
    -- Source: matches_raw.duration BIGINT NANOSECONDS (Arrow duration[ns] per DuckDB 1.5.1)
    -- I7 provenance: divisor 1_000_000_000 cites aoestats/pre_ingestion.py:271
    CAST(m.duration / 1000000000 AS BIGINT) AS duration_seconds,
    -- I7 provenance: 86400s = 24h cross-dataset canonical sanity bound (~25x p99, I8)
    (CAST(m.duration / 1000000000 AS BIGINT) > 86400) AS is_duration_suspicious
FROM ranked_1v1 r
INNER JOIN matches_raw m ON m.game_id = r.game_id
INNER JOIN p0 ON p0.game_id = r.game_id
INNER JOIN p1 ON p1.game_id = r.game_id
WHERE p0.winner != p1.winner;

```

## I7 Provenance

- **Divisor 1,000,000,000:** cites `aoestats/pre_ingestion.py:271`
  (Arrow `duration[ns]` -> BIGINT nanoseconds per DuckDB 1.5.1).
- **Threshold 86,400s (24h):** cross-dataset canonical sanity bound.
  ~25x p99 (5,729s) from 01_04_03 Gate+5b (research_log.md 2026-04-18).
  I8 contract: identical threshold in sc2egset and aoe2companion.
