# Q6: Variance Decomposition & ICC — sc2egset

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Date:** 2026-04-18

## Method (B3 fix)

Three ICC estimators per critique fix B3:
1. **icc_lpm_observed_scale**: statsmodels.mixedlm (LPM; Lindstrom-Bates JASA 1988)
2. **icc_anova_observed_scale**: ANOVA-based ICC for binary outcomes (Wu/Crespi/Wong 2012 CCT 33(5):869-880)
3. **icc_glmm_latent_scale**: BinomialBayesMixedGLM attempt (Nakagawa et al. 2017)

## SQL (verbatim, I6)

```sql
SELECT player_id, CAST(won AS DOUBLE) AS won
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-07-01'
  AND started_at <  TIMESTAMP '2025-01-01'
  AND player_id IN (
    SELECT player_id FROM matches_history_minimal
    WHERE started_at >= TIMESTAMP '2022-08-29'
      AND started_at <  TIMESTAMP '2023-01-01'
    GROUP BY player_id HAVING COUNT(*) >= 10
  )
```

## Cohort

- 4034 observations, 152 players
- Cohort: N>=10 matches in reference period (2022-08-29..2022-12-31), no span filter
- Span filter removed: tournament structure means players appear in short events (3-5 days)
- reference cohort N>=10 without span filter: 152 players

## Results

| metric_name | icc | ci_low | ci_high |
|---|---|---|---|
| icc_lpm_observed_scale | 0.0456 | 0.0058 | 0.0854 |
| icc_anova_observed_scale | 0.0463 | 0.0283 | 0.0643 |
| icc_glmm_latent_scale | N/A | N/A | N/A |

## Verdict: INCONCLUSIVE

## Spec §8 interpretation caveat (B3 note)

LPM ICC is at observed scale. For Bernoulli outcomes, the canonical ICC is at latent
scale: tau^2/(tau^2+pi^2/3) (Nakagawa/Johnson/Schielzeth 2017 JRS Interface 14:20170213).
Observed-scale ICC underestimates if the model is non-linear at the margins.

## rating_pre secondary (A5)

N/A for sc2egset: matches_history_minimal does not expose rating_pre for this dataset.
MMR is available but 83.65% are zero-sentinels (not reported). Per spec §8, secondary
target requires non-NULL in >= 80% of rows. Condition not met.
