# Step 01_04_00 -- Source Normalization to Canonical Long Skeleton

**Dataset:** aoe2companion
**Date:** 2026-04-16
**View:** matches_long_raw

## Summary

Created `matches_long_raw` VIEW: canonical 10-column long skeleton, one row per
player per match. Lossless projection from matches_raw (already in long format).
No filtering, no cleaning, no feature computation.

## Row counts

| Source | Count |
|--------|-------|
| matches_raw | 277,099,059 |
| matches_long_raw | 277,099,059 |
| Lossless | PASS |

## Schema

| Column | Type | Nullable |
|--------|------|----------|
| match_id | INTEGER | YES |
| started_timestamp | TIMESTAMP | YES |
| side | INTEGER | YES |
| player_id | INTEGER | YES |
| chosen_civ_or_race | VARCHAR | YES |
| outcome_raw | INTEGER | YES |
| rating_pre_raw | INTEGER | YES |
| map_id_raw | VARCHAR | YES |
| patch_raw | INTEGER | YES |
| leaderboard_raw | INTEGER | YES |

## Symmetry audit

### Full dataset (side IN (0, 1))

Note: aoe2companion uses team=1 and team=2 as 1v1 sides, not team=0 and team=1.
Side=0 contains only 449 rows (source encoding artifact). The 1v1-scoped audit is operationally relevant.

| side | n_rows | n_wins | win_pct | n_null_outcome |
|------|--------|--------|---------|----------------|
| 0 | 449 | 20 | 4.4543% | 301 |
| 1 | 130,369,073 | 64632796 | 49.5768% | 1,546,260 |

### 1v1 scoped (leaderboard_raw IN (6, 18))

| side | n_rows | n_wins | win_pct | n_null_outcome |
|------|--------|--------|---------|----------------|
| 1 | 29,921,254 | 14116649 | 47.1793% | 1,685 |

## leaderboard_raw distribution (top 10)

| leaderboard_raw | n |
|-----------------|---|
| 0 | 78,254,732 |
| 6 | 53,694,523 |
| 9 | 50,244,434 |
| 7 | 28,256,453 |
| 8 | 24,210,277 |
| 18 | 7,377,276 |
| 19 | 7,189,856 |
| 21 | 6,532,858 |
| 20 | 5,984,441 |
| 67 | 1,948,418 |

## Invariants

- **I3:** started (temporal anchor) retained; ratingDiff and finished excluded.
- **I5:** Player-row-oriented VIEW; no slot pivoting; both players represented identically.
- **I6:** All SQL queries stored verbatim in the JSON artifact.
- **I9:** No features computed; no rows filtered; raw data untouched.
