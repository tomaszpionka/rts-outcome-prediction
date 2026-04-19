# 01_05_06 DGP Duration Diagnostics — aoe2companion

spec: reports/specs/01_05_preregistration.md@7e259dd8

## I3 Guard

POST_GAME features (`duration_seconds`, `is_duration_suspicious`, `is_duration_negative`) are the
SOLE subject of this notebook. They do NOT appear in T03/T04 pre-game outputs (spec §10, I3).

## Interpretation at Large N (M-05)

Sullivan & Feinn (2012) JGME 4(3):279-282: at N~60M, confidence intervals on Cohen's d ≈ ±0.001.
Any drift is statistically detectable. Substantive thresholds: |d| < 0.2 negligible, ≥ 0.2 small, ≥ 0.5 medium.
All verdicts below apply substantive standards, not statistical significance.

## Results

| period    |   n_total |   n_clean |   median_dur_clean |   p95_clean |   suspicious_rate |   negative_rate |   cohen_d_clean |
|:----------|----------:|----------:|-------------------:|------------:|------------------:|----------------:|----------------:|
| reference |   4013828 |   4013758 |               1472 |        2575 |         1.744e-05 |       0         |        0        |
| 2023-Q1   |   3976434 |   3976414 |               1448 |        2576 |         5.03e-06  |       0         |       -0.030765 |
| 2023-Q2   |   3867538 |   3867518 |               1470 |        2588 |         5.17e-06  |       0         |       -0.010427 |
| 2023-Q3   |   3704278 |   3704274 |               1468 |        2598 |         1.08e-06  |       0         |       -0.014781 |
| 2023-Q4   |   3877280 |   3877278 |               1458 |        2579 |         5.2e-07   |       0         |       -0.034018 |
| 2024-Q1   |   4111394 |   4111394 |               1460 |        2574 |         0         |       0         |       -0.034773 |
| 2024-Q2   |   4119216 |   4119216 |               1419 |        2522 |         0         |       0         |       -0.08352  |
| 2024-Q3   |   4031764 |   4031764 |               1414 |        2534 |         0         |       0         |       -0.08792  |
| 2024-Q4   |   4120404 |   4120324 |               1415 |        2532 |         4.9e-07   |       1.893e-05 |       -0.092315 |

**Max |Cohen's d| (cleaned duration vs reference):** 0.0923

**Verdict:** confirmed

## Reconciliation note

aoec INVARIANTS §1 records: 142 suspicious rows (>86,400s), 342 strict-negative rows (clock-skew).
These are absolute counts from the 01_04_02 ADDENDUM. Per aoec INVARIANTS §3 reservoir-sample caveat:
counts may differ slightly on DB rebuild. The reference period counts above reflect the current DB state.

## SQL

```sql

SELECT
    COUNT(*) AS n_total,
    COUNT(*) FILTER (WHERE NOT is_duration_suspicious AND NOT is_duration_negative) AS n_clean,
    AVG(duration_seconds) AS mean_dur_raw,
    quantile_cont(duration_seconds, 0.5) AS median_dur_raw,
    quantile_cont(duration_seconds, 0.05) AS p05_raw,
    quantile_cont(duration_seconds, 0.95) AS p95_raw,
    quantile_cont(duration_seconds, 0.75) - quantile_cont(duration_seconds, 0.25) AS iqr_raw,
    AVG(duration_seconds) FILTER (WHERE NOT is_duration_suspicious AND NOT is_duration_negative) AS mean_dur_clean,
    quantile_cont(duration_seconds, 0.5)
        FILTER (WHERE NOT is_duration_suspicious AND NOT is_duration_negative) AS median_dur_clean,
    quantile_cont(duration_seconds, 0.95)
        FILTER (WHERE NOT is_duration_suspicious AND NOT is_duration_negative) AS p95_clean,
    STDDEV(duration_seconds)
        FILTER (WHERE NOT is_duration_suspicious AND NOT is_duration_negative) AS std_dur_clean,
    COUNT(*) FILTER (WHERE is_duration_suspicious) AS n_suspicious,
    COUNT(*) FILTER (WHERE is_duration_negative) AS n_negative,
    COUNT(*) FILTER (WHERE duration_seconds = 0) AS n_zero,
    COUNT(*) FILTER (WHERE is_duration_suspicious) * 1.0 / COUNT(*) AS suspicious_rate,
    COUNT(*) FILTER (WHERE is_duration_negative) * 1.0 / COUNT(*) AS negative_rate
FROM matches_1v1_clean
WHERE started >= TIMESTAMP '{ts_start}'
  AND started <  TIMESTAMP '{ts_end}'

```
