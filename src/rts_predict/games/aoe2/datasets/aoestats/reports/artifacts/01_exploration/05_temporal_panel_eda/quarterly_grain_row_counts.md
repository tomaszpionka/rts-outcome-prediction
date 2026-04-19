# Quarterly Grain Row Counts — aoestats

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Step:** 01_05_01

## SQL

```sql
WITH quarterly AS (
  SELECT
    DATE_TRUNC('quarter', started_at) AS quarter_start,
    CAST(YEAR(started_at) AS VARCHAR) || '-Q' || CAST(QUARTER(started_at) AS VARCHAR) AS quarter_iso,
    COUNT(*) AS row_count,
    COUNT(DISTINCT match_id) AS match_count,
    COUNT(DISTINCT player_id) AS player_count
  FROM matches_history_minimal
  WHERE started_at >= TIMESTAMP '2022-07-01'
    AND started_at < TIMESTAMP '2025-01-01'
  GROUP BY 1, 2
  ORDER BY 1
)
SELECT * FROM quarterly
```

## Results

| quarter_start       | quarter_iso   |   row_count |   match_count |   player_count |
|:--------------------|:--------------|------------:|--------------:|---------------:|
| 2022-07-01 00:00:00 | 2022-Q3       |       37632 |         18816 |          17325 |
| 2022-10-01 00:00:00 | 2022-Q4       |      159112 |         79556 |          44114 |
| 2023-01-01 00:00:00 | 2023-Q1       |      845564 |        422782 |          77695 |
| 2023-04-01 00:00:00 | 2023-Q2       |     3485606 |       1742803 |          95158 |
| 2023-07-01 00:00:00 | 2023-Q3       |     2802462 |       1401231 |          85312 |
| 2023-10-01 00:00:00 | 2023-Q4       |     3385088 |       1692544 |          89698 |
| 2024-01-01 00:00:00 | 2024-Q1       |     3586266 |       1793133 |          91572 |
| 2024-04-01 00:00:00 | 2024-Q2       |     3376140 |       1688070 |          88471 |
| 2024-07-01 00:00:00 | 2024-Q3       |     1382090 |        691045 |          61960 |
| 2024-10-01 00:00:00 | 2024-Q4       |     2942920 |       1471460 |          80808 |

## Falsifier verdict

**Q1 Falsifier:** PASSED
Minimum tested-quarter rows: 845,564 (2023-Q1)
