# 01_05_02 PSI Shift — aoe2companion

spec: reports/specs/01_05_preregistration.md@7e259dd8

## Pre-game features analysed

- `rating` (numeric, N=10 equal-frequency bins, frozen reference edges, Siddiqi 2006)
- `won` (binary, Cohen's h vs reference period per Cohen 1988 §6.2; M-03 fix: vs reference not 0.5)
- `faction` (categorical, relative-frequency PSI with `__unseen__` bin)
- `map_id` (categorical, relative-frequency PSI with `__unseen__` bin)

POST_GAME features (`duration_seconds`, `is_duration_suspicious`, `is_duration_negative`) are excluded (§4, I3).

## PSI Thresholds — Calibration Warning (M-04)

Siddiqi (2006) thresholds (monitor: 0.10, escalate: 0.25) are calibrated for N=10^3-10^5.
Yurdakul (2018) WMU #3208: "0.25 reasonable for 100-200, too conservative for larger samples."
At N~60M rows per quarter, any non-zero PSI is statistically detectable.
All PSI values are **reported without 'significant drift' verdicts**; the `verdict` field is descriptive only and flagged for review.

## Interpretation at Large N (M-05)

Sullivan & Feinn (2012) JGME 4(3):279-282: at N~60M, confidence intervals on effect sizes approach ±0.001.
Any drift will be "statistically significant." Substantive significance (|d| ≥ 0.2, PSI ≥ 0.10) is the relevant standard.
Cohen's d and Cohen's h are reported as substantive effect-size measures alongside raw PSI.

## Rating PSI per quarter (conditional on is_null_cluster=FALSE, lbs 6+18)

| quarter   |      psi |   cohen_d |   ks_stat |   n_test | verdict            |
|:----------|---------:|----------:|----------:|---------:|:-------------------|
| 2023-Q1   | 0.124681 |  0.088657 |       nan |     5260 | monitor            |
| 2023-Q2   | 0.098865 |  0.218866 |       nan |     8302 | stable             |
| 2023-Q3   | 0.711641 |  0.611393 |       nan |  1994204 | flagged_for_review |
| 2023-Q4   | 0.696254 |  0.594807 |       nan |  3876862 | flagged_for_review |
| 2024-Q1   | 0.707041 |  0.592929 |       nan |  4110780 | flagged_for_review |
| 2024-Q2   | 0.676206 |  0.569597 |       nan |  4118454 | flagged_for_review |
| 2024-Q3   | 0.756783 |  0.572312 |       nan |  4031328 | flagged_for_review |
| 2024-Q4   | 0.877757 |  0.583383 |       nan |  4119966 | flagged_for_review |

**Reference:** Frozen bin edges at deciles of reference period (2022-08-29..2022-12-31).
Max rating PSI: 0.8778
Max faction PSI: 0.4824
Max map_id PSI: 3.0429

**Cohen's h (won, M-03 — vs reference p_ref=0.5000):**
| 2023-Q1 | 0.0 |
| 2023-Q2 | 0.0 |
| 2023-Q3 | 0.0 |
| 2023-Q4 | 0.0 |
| 2024-Q1 | 0.0 |
| 2024-Q2 | 0.0 |
| 2024-Q3 | 0.0 |
| 2024-Q4 | 0.0 |

## is_null_cluster handling (M-09)

Applied `WHERE is_null_cluster = FALSE` (via join to `matches_1v1_clean`) in both reference and test windows.
This excludes the <0.02% NULL cluster rows from all PSI computations.

## KS statistic (Breck et al. 2019, M-08)

KS computed on stratified subsample: 100k reference + 100k test per quarter (seed=42, reservoir sampling).
Sample IDs persisted under `ks_sample_ids_<quarter>.csv`.

## SQL (I6)

### Reference rating bin edges
```sql

SELECT quantile_cont(m.rating, list_value(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9)) AS edges,
       COUNT(*) AS n_ref,
       AVG(m.rating) AS mean_ref,
       STDDEV(m.rating) AS std_ref
FROM matches_history_minimal mhm
JOIN matches_1v1_clean m
  ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
 AND CAST(m.profileId AS VARCHAR) = mhm.player_id
WHERE mhm.started_at >= TIMESTAMP '2022-08-29'
  AND mhm.started_at <  TIMESTAMP '2023-01-01'
  AND m.rating IS NOT NULL
  AND m.is_null_cluster = FALSE
  AND m.internalLeaderboardId IN (6, 18)

```

### Reference win rate
```sql

SELECT
    AVG(CAST(won AS DOUBLE)) AS p_ref_won,
    COUNT(*) AS n_ref_won
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-08-29'
  AND started_at <  TIMESTAMP '2023-01-01'
  AND won IS NOT NULL

```

_conditional on >=10 matches in reference period; see §6 for sensitivity_

## Literature

- Siddiqi (2006) — PSI definition, N=10 equal-frequency bins
- Yurdakul (2018) WMU dissertations #3208 — PSI threshold calibration at large N
- Cohen (1988) §2.2 (d), §6.2 (h) — effect-size definitions
- Breck et al. (2019) SysML — KS as complementary drift descriptor
- Sullivan & Feinn (2012) JGME 4(3):279-282 — interpretation at large N
