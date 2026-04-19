# 01_05_01 Quarterly Grain — aoe2companion

spec: reports/specs/01_05_preregistration.md@7e259dd8

## Overlap window (2022-Q3 to 2024-Q4)

| Quarter | n_matches | n_player_rows |
|---|---|---|
| 2022-Q3 | 454,253 | 908,506 |
| 2022-Q4 | 1,773,250 | 3,546,500 |
| 2023-Q1 | 1,988,217 | 3,976,434 |
| 2023-Q2 | 1,933,769 | 3,867,538 |
| 2023-Q3 | 1,852,139 | 3,704,278 |
| 2023-Q4 | 1,938,640 | 3,877,280 |
| 2024-Q1 | 2,055,697 | 4,111,394 |
| 2024-Q2 | 2,059,608 | 4,119,216 |
| 2024-Q3 | 2,015,882 | 4,031,764 |
| 2024-Q4 | 2,060,202 | 4,120,404 |

**Low-volume quarters (<1000 matches):** NONE

## Reference period (2022-08-29..2022-12-31)

| n_matches | n_player_rows |
|---|---|
| 2,006,913 | 4,013,826 |

## Verdict

confirmed

All 10 overlap-window quarters have substantial rm_1v1 volume (minimum 454,253 matches).
The reference period contains 2,006,913 matches sufficient for stable PSI bin edges.

## SQL

### All quarters
```sql

SELECT
    CONCAT(CAST(EXTRACT(YEAR FROM started_at) AS VARCHAR), '-Q',
           CAST(CEIL(EXTRACT(MONTH FROM started_at) / 3.0) AS INTEGER)::VARCHAR) AS quarter,
    COUNT(DISTINCT match_id) AS n_matches,
    COUNT(*) AS n_player_rows
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2020-07-01'
  AND started_at <  TIMESTAMP '2026-05-01'
GROUP BY 1
ORDER BY 1

```

### Leaderboard-stratified (joined to matches_1v1_clean, is_null_cluster=FALSE)
```sql

SELECT
    CONCAT(CAST(EXTRACT(YEAR FROM mhm.started_at) AS VARCHAR), '-Q',
           CAST(CEIL(EXTRACT(MONTH FROM mhm.started_at) / 3.0) AS INTEGER)::VARCHAR) AS quarter,
    m.internalLeaderboardId AS leaderboard_id,
    COUNT(DISTINCT mhm.match_id) AS n_matches,
    COUNT(*) AS n_player_rows
FROM matches_history_minimal mhm
JOIN matches_1v1_clean m
  ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
 AND CAST(m.profileId AS VARCHAR) = mhm.player_id
WHERE mhm.started_at >= TIMESTAMP '2020-07-01'
  AND mhm.started_at <  TIMESTAMP '2026-05-01'
  AND m.internalLeaderboardId IN (6, 18)
  AND m.is_null_cluster = FALSE
GROUP BY 1, 2
ORDER BY 1, 2

```

### Reference period
```sql

SELECT
    COUNT(DISTINCT match_id) AS n_matches_ref,
    COUNT(*) AS n_player_rows_ref,
    MIN(started_at) AS first_ts,
    MAX(started_at) AS last_ts
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-08-29'
  AND started_at <  TIMESTAMP '2023-01-01'

```

_conditional on >=10 matches in reference period; see §6 for sensitivity_
