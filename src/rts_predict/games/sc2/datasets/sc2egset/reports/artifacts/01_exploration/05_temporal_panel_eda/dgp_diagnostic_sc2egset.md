# Q8: DGP Diagnostics — duration_seconds (sc2egset)

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Date:** 2026-04-18

## Method

- POST_GAME_HISTORICAL diagnostic only (duration_seconds excluded from pre-game PSI per I3)
- Reference: 2022-08-29..2022-12-31
- Tested: 2023-Q1..2024-Q4 (8 quarters)
- M9 fix: JOIN matches_flat_clean for is_duration_suspicious per-quarter rate
- Cohen (1988) §2.2: d = (mean_q - mean_ref) / pooled_sd

## SQL (verbatim, I6)

```sql
-- M9 fix: JOIN matches_flat_clean to get is_duration_suspicious
WITH tagged AS (
  SELECT
    CASE
      WHEN m.started_at BETWEEN TIMESTAMP '2022-08-29' AND TIMESTAMP '2022-12-31'
           THEN 'reference'
      ELSE CAST(date_part('year', m.started_at) AS VARCHAR) || '-Q' ||
             CAST(date_part('quarter', m.started_at) AS VARCHAR)
    END AS period_tag,
    m.duration_seconds,
    mfc.is_duration_suspicious
  FROM matches_history_minimal m
  JOIN matches_flat_clean mfc ON substr(m.match_id, 11) = mfc.replay_id
  WHERE m.started_at >= TIMESTAMP '2022-08-29'
    AND m.started_at <  TIMESTAMP '2025-01-01'
)
SELECT
  period_tag,
  AVG(duration_seconds)                              AS mean_dur,
  MEDIAN(duration_seconds)                           AS median_dur,
  QUANTILE_CONT(duration_seconds, 0.05)              AS p5_dur,
  QUANTILE_CONT(duration_seconds, 0.95)              AS p95_dur,
  QUANTILE_CONT(duration_seconds, 0.75) -
    QUANTILE_CONT(duration_seconds, 0.25)            AS iqr_dur,
  STDDEV_SAMP(duration_seconds)                      AS sd_dur,
  COUNT(*)                                           AS n,
  AVG(CAST(is_duration_suspicious AS DOUBLE))        AS suspicious_rate
FROM tagged
GROUP BY period_tag
ORDER BY period_tag
```

## Per-period statistics

| period_tag   |   mean_dur |   median_dur |   p5_dur |   p95_dur |   iqr_dur |   sd_dur |    n |   suspicious_rate |
|:-------------|-----------:|-------------:|---------:|----------:|----------:|---------:|-----:|------------------:|
| 2023-Q1      |    771.819 |        673   |   392.85 |   1489.65 |    318.75 |  358.837 | 1040 |                 0 |
| 2023-Q2      |    716.179 |        655.5 |   333.55 |   1298.9  |    347    |  346.752 | 2792 |                 0 |
| 2023-Q3      |    928.303 |        818.5 |   401    |   2123    |    461    |  528.591 |  488 |                 0 |
| 2023-Q4      |    785.372 |        697   |   339    |   1475    |    427.5  |  376.907 | 2688 |                 0 |
| 2024-Q1      |    799.947 |        729   |   349    |   1563    |    390    |  366.137 |  748 |                 0 |
| 2024-Q2      |    707.096 |        630   |   288.1  |   1396.05 |    364    |  342.853 | 1748 |                 0 |
| 2024-Q3      |    819.794 |        750   |   387    |   1538    |    463.25 |  373.723 |  992 |                 0 |
| 2024-Q4      |    746.246 |        671   |   337    |   1348    |    412    |  326.467 |  684 |                 0 |
| reference    |    725.34  |        642   |   299    |   1388    |    419    |  358.853 | 6536 |                 0 |

## Cohen's d per tested quarter

| period_tag   |   mean_dur |   sd_dur |    n |    cohen_d |
|:-------------|-----------:|---------:|-----:|-----------:|
| 2023-Q1      |    771.819 |  358.837 | 1040 |  0.129523  |
| 2023-Q2      |    716.179 |  346.752 | 2792 | -0.0257845 |
| 2023-Q3      |    928.303 |  528.591 |  488 |  0.543956  |
| 2023-Q4      |    785.372 |  376.907 | 2688 |  0.164831  |
| 2024-Q1      |    799.947 |  366.137 |  748 |  0.207468  |
| 2024-Q2      |    707.096 |  342.853 | 1748 | -0.0513126 |
| 2024-Q3      |    819.794 |  373.723 |  992 |  0.261759  |
| 2024-Q4      |    746.246 |  326.467 |  684 |  0.0587387 |

## Verdict: FALSIFIED

Max |Cohen's d| = 0.5440. Quarters with |d| > 0.2: 3.
Max mean drift from reference: 28.0%.

## is_duration_suspicious (M9 fix)

Per-quarter suspicious_rate computed via JOIN matches_flat_clean.
Average suspicious_rate across overlap window: 0.0000
(0.0 = no suspicious durations; matches 01_04_03 ADDENDUM finding of zero outliers).
