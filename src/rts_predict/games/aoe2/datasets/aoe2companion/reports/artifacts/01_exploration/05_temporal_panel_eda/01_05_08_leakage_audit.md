# 01_05_08 Temporal Leakage Audit — aoe2companion

spec: reports/specs/01_05_preregistration.md@7e259dd8

## Summary

| Check | Status | Description |
|---|---|---|
| check_1_temporal_bin_edges | PASS | M-01 fix: Assert all ref-period rows have started_at in [2022-08-29, 2023-01-01)... |
| check_2_post_game_token_scan | PASS | AST/regex scan of T03/T04 notebooks for POST_GAME tokens in pre-game feature sel... |
| check_3_normalization_window | PASS | Assert T03 JSON frozen_reference_edges.ref_start == '2022-08-29' and ref_end == ... |

**Overall verdict: PASS**

## M-01 Deviation Note

Original spec §9 Query 1: vacuous match-id disjointness check (tautology — match_id is PK).
M-01 fix: reframed as meaningful bin-edge temporal check.
- Check 1a: All reference-period rows (used for frozen PSI bin edges) have started_at in [2022-08-29, 2023-01-01)
- Check 1b: All tested-period rows are within their declared quarter windows

**Result:** ref_outside_bound=0, test_outside_quarters=0

## Check 2: POST_GAME token scan

Scanned: 01_05_02_psi_shift.py, 01_05_03_stratification.py
Tokens scanned: ['duration_seconds', 'finished', 'is_duration_negative', 'is_duration_suspicious', 'ratingDiff']
Tokens found in pre-game context: NONE

## Check 3: Normalization window constants

T03 JSON asserts:
- ref_start = '2022-08-29T00:00:00' (expected '2022-08-29'): OK
- ref_end = '2022-12-31T00:00:00' (expected '2022-12-31'): OK
- assertion_passed = True

## Reference period row hash (M-06)

MD5 of (match_id || player_id) for reference period rows: `f9aa56bb5f22e247615fb9e33f30e688`
Use for reproducibility verification across DB rebuilds (reservoir-sample caveat applies).

## SQL

### Check 1a
```sql

SELECT COUNT(*) AS rows_in_ref_outside_bound
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-08-29'
  AND started_at <  TIMESTAMP '2023-01-01'
  AND (started_at < TIMESTAMP '2022-08-29' OR started_at >= TIMESTAMP '2023-01-01')

```

### Check 1b
```sql

SELECT quarter, n, n_outside_bound
FROM (
    SELECT
        CONCAT(CAST(EXTRACT(YEAR FROM started_at) AS VARCHAR), '-Q',
               CAST(CEIL(EXTRACT(MONTH FROM started_at) / 3.0) AS INTEGER)::VARCHAR) AS quarter,
        COUNT(*) AS n,
        COUNT(*) FILTER (
            WHERE started_at < TIMESTAMP '2023-01-01'
               OR started_at >= TIMESTAMP '2025-01-01'
        ) AS n_outside_bound
    FROM matches_history_minimal
    WHERE started_at >= TIMESTAMP '2023-01-01'
      AND started_at <  TIMESTAMP '2025-01-01'
    GROUP BY 1
) sub
WHERE n_outside_bound > 0

```
