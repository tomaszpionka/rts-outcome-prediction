# Step 01_04_00 -- Source Normalization to Canonical Long Skeleton

**Dataset:** aoestats
**Date:** 2026-04-16
**View:** matches_long_raw

## Summary

Created `matches_long_raw` VIEW: canonical 10-column long skeleton, one row per
player per match. JOIN of players_raw (per-player) with matches_raw, filtered
identically to player_history_all (profile_id IS NOT NULL, started_timestamp IS NOT NULL).

## Lossless validation (independent anchor)

| Metric | Count |
|--------|-------|
| total players_raw | 107,627,584 |
| null profile_id | 1,185 |
| orphan or null started_timestamp | 0 |
| expected (anchor formula) | 107,626,399 |
| matches_long_raw rows | 107,626,399 |
| Anchor cross-check (==107,627,584) | PASS |
| Lossless | PASS |

## Schema

| Column | Type | Nullable |
|--------|------|----------|
| match_id | VARCHAR | YES |
| started_timestamp | TIMESTAMP WITH TIME ZONE | YES |
| side | INTEGER | YES |
| player_id | BIGINT | YES |
| chosen_civ_or_race | VARCHAR | YES |
| outcome_raw | INTEGER | YES |
| rating_pre_raw | BIGINT | YES |
| map_id_raw | VARCHAR | YES |
| patch_raw | BIGINT | YES |
| leaderboard_raw | VARCHAR | YES |

## Symmetry audit

### Full dataset (side IN (0, 1))

| side | n_rows | n_wins | win_pct | n_null_outcome |
|------|--------|--------|---------|----------------|
| 0 | 53,813,160 | 26351008 | 48.9676% | 0 |
| 1 | 53,813,239 | 27459785 | 51.0279% | 0 |

### 1v1 scoped (leaderboard_raw = 'random_map')

Known asymmetry from 01_04_01: side=1 wins ~52.27%. This reappears here.

| side | n_rows | n_wins | win_pct | n_null_outcome |
|------|--------|--------|---------|----------------|
| 0 | 17,815,971 | 8503784 | 47.7312% | 0 |
| 1 | 17,815,944 | 9311550 | 52.2653% | 0 |

## leaderboard_raw distribution (top 10)

| leaderboard_raw | n |
|-----------------|---|
| team_random_map | 67,912,325 |
| random_map | 35,631,915 |
| co_team_random_map | 2,836,522 |
| co_random_map | 1,245,637 |

## Invariants

- **I3:** old_rating retained; new_rating and match_rating_diff excluded.
- **I5:** Player-row-oriented VIEW; no slot pivoting; both players represented identically.
- **I6:** All SQL queries stored verbatim in the JSON artifact.
- **I9:** No features computed; only rows with null profile_id or null started_timestamp excluded (matching player_history_all filter).
