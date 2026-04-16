# Step 01_04_00 -- Source Normalization to Canonical Long Skeleton

**Dataset:** sc2egset
**Date:** 2026-04-16
**View:** matches_long_raw

## Summary

Created `matches_long_raw` VIEW: canonical 10-column long skeleton, one row per
player per match. Structural INNER JOIN of replay_players_raw x replays_meta_raw
using the 32-char hex hash extracted from filename via regexp. No filtering beyond
INNER JOIN (unmatched rows excluded by INNER JOIN semantics).

## Row counts

| Source | Count |
|--------|-------|
| direct JOIN count | 44,817 |
| matches_long_raw | 44,817 |
| Lossless | PASS |

## Schema

| Column | Type | Nullable |
|--------|------|----------|
| match_id | VARCHAR | YES |
| started_timestamp | VARCHAR | YES |
| side | INTEGER | YES |
| player_id | VARCHAR | NO |
| chosen_civ_or_race | VARCHAR | YES |
| outcome_raw | INTEGER | YES |
| rating_pre_raw | INTEGER | YES |
| map_id_raw | VARCHAR | YES |
| patch_raw | VARCHAR | YES |
| leaderboard_raw | INTEGER | YES |

## Symmetry audit (side IN (0, 1))

| side | n_rows | n_wins | win_pct | n_null_outcome |
|------|--------|--------|---------|----------------|
| 0 | 22,390 | 11634 | 51.9607% | 13 |
| 1 | 22,387 | 10740 | 47.9743% | 13 |

Note: leaderboard_raw is NULL for all rows (tournament data, no matchmaking ladder).
No 1v1-scoped symmetry audit is applicable.

## leaderboard_raw distribution

All 44,817 rows have leaderboard_raw = NULL (expected -- tournament dataset).

## Invariants

- **I3:** MMR retained (PRE_GAME per 01_04_01); APM, SQ, supplyCappedPercent, header_elapsedGameLoops excluded.
- **I5:** Player-row-oriented VIEW; no slot pivoting; both players represented identically.
- **I6:** All SQL queries stored verbatim in the JSON artifact.
- **I9:** No features computed; no rows filtered beyond INNER JOIN unmatched exclusion.
