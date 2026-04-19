# Q2: PSI Quarterly — sc2egset

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Date:** 2026-04-18

## Method

- Primary: UNCOHORT-FILTERED (all overlap-window players). N in {5,10,20} = sensitivity (T05).
- Features: faction, opponent_faction, matchup (derived)
- Reference: 2022-08-29..2022-12-31 (3268 rows)
- Tested: 2023-Q1..2024-Q4 (8 quarters)
- PSI = Σ(p_tested - p_ref) * ln(p_tested/p_ref) with Laplace ε=1/n_ref=0.000306
- Literature: Siddiqi (2006), Yurdakul (2018) WMU #3208

## Critique fix B2

Primary PSI is uncohort-filtered because N>=10 cohort eliminates 4 of 8 tested quarters.
CROSS research-log entry documents this deviation. (User pre-authorized.)

## Verdict: FALSIFIED

Max PSI = 0.6959. Cells crossing 0.10: 16. Cells crossing 0.25: 7.

## SQL (verbatim, I6)

### Reference population
```sql
SELECT
  faction,
  opponent_faction,
  GREATEST(faction, opponent_faction) || 'v' || LEAST(faction, opponent_faction) AS matchup
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-08-29 00:00:00'
  AND started_at <  TIMESTAMP '2023-01-01 00:00:00'
```

### Tested quarters
```sql
SELECT
  CAST(date_part('year', started_at) AS VARCHAR) || '-Q' ||
    CAST(date_part('quarter', started_at) AS VARCHAR) AS quarter,
  faction,
  opponent_faction,
  GREATEST(faction, opponent_faction) || 'v' || LEAST(faction, opponent_faction) AS matchup
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2023-01-01 00:00:00'
  AND started_at <  TIMESTAMP '2025-01-01 00:00:00'
```

## PSI table

| quarter   | feature_name     |   psi_value |   n_ref |   n_tested |   unseen_count |
|:----------|:-----------------|------------:|--------:|-----------:|---------------:|
| 2023-Q1   | faction          |      0.1769 |    3268 |        520 |              0 |
| 2023-Q1   | opponent_faction |      0.1769 |    3268 |        520 |              0 |
| 2023-Q1   | matchup          |      0.3631 |    3268 |        520 |              0 |
| 2023-Q2   | faction          |      0.0012 |    3268 |       1396 |              0 |
| 2023-Q2   | opponent_faction |      0.0012 |    3268 |       1396 |              0 |
| 2023-Q2   | matchup          |      0.0246 |    3268 |       1396 |              0 |
| 2023-Q3   | faction          |      0.2786 |    3268 |        244 |              0 |
| 2023-Q3   | opponent_faction |      0.2786 |    3268 |        244 |              0 |
| 2023-Q3   | matchup          |      0.6959 |    3268 |        244 |              0 |
| 2023-Q4   | faction          |      0.0328 |    3268 |       1344 |              0 |
| 2023-Q4   | opponent_faction |      0.0328 |    3268 |       1344 |              0 |
| 2023-Q4   | matchup          |      0.0741 |    3268 |       1344 |              0 |
| 2024-Q1   | faction          |      0.1988 |    3268 |        374 |              0 |
| 2024-Q1   | opponent_faction |      0.1988 |    3268 |        374 |              0 |
| 2024-Q1   | matchup          |      0.4074 |    3268 |        374 |              0 |
| 2024-Q2   | faction          |      0.0607 |    3268 |        874 |              0 |
| 2024-Q2   | opponent_faction |      0.0607 |    3268 |        874 |              0 |
| 2024-Q2   | matchup          |      0.1817 |    3268 |        874 |              0 |
| 2024-Q3   | faction          |      0.1872 |    3268 |        496 |              0 |
| 2024-Q3   | opponent_faction |      0.1872 |    3268 |        496 |              0 |
| 2024-Q3   | matchup          |      0.3864 |    3268 |        496 |              0 |
| 2024-Q4   | faction          |      0.2199 |    3268 |        342 |              0 |
| 2024-Q4   | opponent_faction |      0.2199 |    3268 |        342 |              0 |
| 2024-Q4   | matchup          |      0.5444 |    3268 |        342 |              0 |

## Caption

(conditional on ≥10 matches in reference period; see §6 for sensitivity)
Actual: uncohort-filtered PRIMARY per B2 fix.

## KS omission note (critique m9)

KS statistic is omitted for sc2egset: no continuous pre-game feature exists in
`matches_history_minimal` (faction/opponent_faction/matchup are all categorical).
KS is applicable only to continuous features per spec §4 / Breck et al. (2019).
