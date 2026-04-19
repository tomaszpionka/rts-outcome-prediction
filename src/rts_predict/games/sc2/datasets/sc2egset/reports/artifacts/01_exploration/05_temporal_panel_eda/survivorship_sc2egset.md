# Q4: Triple Survivorship Analysis — sc2egset

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Date:** 2026-04-18

## SQL (verbatim, I6)

### Unconditional survivorship
```sql
WITH players_in_window AS (
  SELECT DISTINCT player_id
  FROM matches_history_minimal
  WHERE started_at >= TIMESTAMP '2022-07-01'
    AND started_at <  TIMESTAMP '2025-01-01'
),
quarter_tagged AS (
  SELECT
    player_id,
    CAST(date_part('year', started_at) AS VARCHAR) || '-Q' ||
      CAST(date_part('quarter', started_at) AS VARCHAR) AS quarter
  FROM matches_history_minimal
  WHERE started_at >= TIMESTAMP '2022-07-01'
    AND started_at <  TIMESTAMP '2025-01-01'
    AND player_id IN (SELECT player_id FROM players_in_window)
)
SELECT
  quarter,
  COUNT(DISTINCT player_id) AS n_active,
  (SELECT COUNT(*) FROM players_in_window) AS n_total_in_window,
  COUNT(DISTINCT player_id) * 1.0 /
    (SELECT COUNT(*) FROM players_in_window) AS fraction_active
FROM quarter_tagged
GROUP BY quarter
ORDER BY quarter
```

### Reference cohort
```sql
SELECT player_id, COUNT(*) AS n_ref_matches,
       MAX(started_at)::DATE - MIN(started_at)::DATE AS active_span_days
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-08-29'
  AND started_at <  TIMESTAMP '2023-01-01'
GROUP BY player_id
```

## Unconditional survivorship (overlap window)

| quarter   |   n_active |   n_total_in_window |   fraction_active | dataset_tag   |
|:----------|-----------:|--------------------:|------------------:|:--------------|
| 2022-Q3   |        183 |                 679 |         0.269514  | sc2egset      |
| 2022-Q4   |        188 |                 679 |         0.276878  | sc2egset      |
| 2023-Q1   |         36 |                 679 |         0.0530191 | sc2egset      |
| 2023-Q2   |        130 |                 679 |         0.191458  | sc2egset      |
| 2023-Q3   |         22 |                 679 |         0.0324006 | sc2egset      |
| 2023-Q4   |        122 |                 679 |         0.179676  | sc2egset      |
| 2024-Q1   |         24 |                 679 |         0.0353461 | sc2egset      |
| 2024-Q2   |         72 |                 679 |         0.106038  | sc2egset      |
| 2024-Q3   |         35 |                 679 |         0.0515464 | sc2egset      |
| 2024-Q4   |         24 |                 679 |         0.0353461 | sc2egset      |

## Sensitivity cohort sizes (N∈{5,10,20}, active_span>=30d)

|   n_threshold |   cohort_size | is_default   | small_cohort   | notes          |
|--------------:|--------------:|:-------------|:---------------|:---------------|
|             5 |             9 | False        | True           | [SMALL-COHORT] |
|            10 |             9 | True         | True           | [SMALL-COHORT] |
|            20 |             9 | False        | True           | [SMALL-COHORT] |

## Verdicts

- Hypothesis A (reference cohort N>=10 >= 50): FALSIFIED (cohort=9)
- Hypothesis B (all quarters non-empty): CONFIRMED (min_active=22)

## U4 resolution

Reference cohort N>=10 (span>=30d): **9 players**.
[SMALL-COHORT] Cohort small but non-trivial.

## Notes

- B2 fix: Primary PSI in T03 is UNCOHORT-FILTERED. Survivorship sensitivity here
  informs the conditional-label captioning only.
- Gelman & Hill (2007) §12.5: min-cluster-size 10 obs/player for random-intercept fits.
- M5 fix: Hypothesis grain-explicit: (a) reference N>=50; (b) per-quarter n_active > 0.
