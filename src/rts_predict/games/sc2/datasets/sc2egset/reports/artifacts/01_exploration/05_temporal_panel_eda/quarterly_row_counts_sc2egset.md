# Q1: Quarterly Grain & Overlap Window — sc2egset

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Date:** 2026-04-18

## Findings

- Full dataset: 34 quarters, 2016-Q1 to 2024-Q4
- Overlap window: 10 quarters (2022-Q3 to 2024-Q4), **10,076 rows / 5,038 matches**
- M1 correction: plan cited full-dataset N=22,209; overlap window is 10,076 rows / 5,038 matches
- Peak-to-trough in overlap: 11.7x (tournament cadence; irregular but not monotone)
- Verdict: CONFIRMED

## SQL (verbatim, I6)

```sql
-- spec §3 Q1 grain: quarterly aggregation with date_part to avoid float cast
-- B1 fix: date_part('quarter', started_at) yields integer 1-4 directly
WITH q AS (
  SELECT
    CAST(date_part('year', started_at) AS VARCHAR) || '-Q' ||
      CAST(date_part('quarter', started_at) AS VARCHAR) AS quarter,
    match_id, player_id
  FROM matches_history_minimal
)
SELECT quarter,
       COUNT(*)                               AS n_player_rows,
       COUNT(DISTINCT match_id)               AS n_matches,
       COUNT(DISTINCT player_id)              AS n_players
FROM q
GROUP BY quarter
ORDER BY quarter
```

## Overlap window per-quarter counts

| quarter   |   n_player_rows |   n_matches |   n_players | dataset_tag   |
|:----------|----------------:|------------:|------------:|:--------------|
| 2022-Q3   |            1642 |         821 |         183 | sc2egset      |
| 2022-Q4   |            2844 |        1422 |         188 | sc2egset      |
| 2023-Q1   |             520 |         260 |          36 | sc2egset      |
| 2023-Q2   |            1396 |         698 |         130 | sc2egset      |
| 2023-Q3   |             244 |         122 |          22 | sc2egset      |
| 2023-Q4   |            1344 |         672 |         122 | sc2egset      |
| 2024-Q1   |             374 |         187 |          24 | sc2egset      |
| 2024-Q2   |             874 |         437 |          72 | sc2egset      |
| 2024-Q3   |             496 |         248 |          35 | sc2egset      |
| 2024-Q4   |             342 |         171 |          24 | sc2egset      |

## Notes

- Hamilton (1994) §17.7: ADF/KPSS stationarity testing deferred; N=8 tested quarters
  far below T>=50 power threshold.
- B1 fix: `date_part('quarter', started_at)` used instead of `CEIL(.../ 3.0)` cast to avoid '3.0' label.
- M1 (critique): Reference-period bin size ~1,008 rows for N=10 bins on overlap data
  (not ~2,200 as cited in plan; plan cited full-dataset N).
