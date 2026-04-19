# 01_05_04 Survivorship — aoe2companion

spec: reports/specs/01_05_preregistration.md@7e259dd8

## Unconditional fraction_active per quarter

| quarter   |   n_active |   fraction_active |   n_ever_seen |
|:----------|-----------:|------------------:|--------------:|
| 2022-Q3   |      88755 |          0.209943 |        422757 |
| 2022-Q4   |      99734 |          0.235913 |        422757 |
| 2023-Q1   |     122482 |          0.289722 |        422757 |
| 2023-Q2   |     113815 |          0.269221 |        422757 |
| 2023-Q3   |     106336 |          0.25153  |        422757 |
| 2023-Q4   |     109471 |          0.258945 |        422757 |
| 2024-Q1   |     111508 |          0.263764 |        422757 |
| 2024-Q2   |     108177 |          0.255885 |        422757 |
| 2024-Q3   |     103385 |          0.244549 |        422757 |
| 2024-Q4   |     103175 |          0.244053 |        422757 |

**Spearman rho (monotonic attrition test):** 0.0667, p=0.8548

## Verdict (monotonic attrition)

falsified: rho=0.0667, p=0.8548

## Sensitivity Analysis (N thresholds: [5, 10, 20])

Sensitivity rows: 24

| n_threshold | n_players_cohort |
|---|---|
| 5 | 69,005 |
| 10 | 54,113 |
| 20 | 38,349 |

Default cohort (N=10): 54,113 players.

## Reservoir reproducibility caveat

Per aoec INVARIANTS §3: DuckDB `USING SAMPLE reservoir(N ROWS) REPEATABLE(seed)` is deterministic
only for fixed input row-order. `matches_raw` physical order may shift on rebuild.
Results are methodologically equivalent across rebuilds; bit-exact reproducibility is not guaranteed.
ICC sample profile IDs persisted under `icc_sample_profileIds_*.csv` (M-06).

## SQL

### Unconditional fraction_active
```sql

WITH players AS (
    SELECT DISTINCT player_id
    FROM matches_history_minimal
    WHERE started_at >= TIMESTAMP '2022-07-01'
      AND started_at <  TIMESTAMP '2025-01-01'
),
player_quarter AS (
    SELECT player_id,
           CONCAT(CAST(EXTRACT(YEAR FROM started_at) AS VARCHAR), '-Q',
                  CAST(CEIL(EXTRACT(MONTH FROM started_at)/3.0) AS INTEGER)::VARCHAR) AS quarter
    FROM matches_history_minimal
    WHERE started_at >= TIMESTAMP '2022-07-01'
      AND started_at <  TIMESTAMP '2025-01-01'
    GROUP BY 1, 2
)
SELECT quarter,
       COUNT(DISTINCT pq.player_id) AS n_active,
       COUNT(DISTINCT pq.player_id) * 1.0 / (SELECT COUNT(*) FROM players) AS fraction_active,
       (SELECT COUNT(*) FROM players) AS n_ever_seen
FROM player_quarter pq
GROUP BY quarter
ORDER BY quarter

```

_conditional on >=10 matches in reference period; see §6 for sensitivity_
(conditional on >=10 matches in reference period; see §6 for sensitivity)
