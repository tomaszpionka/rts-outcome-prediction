# Step 01_04_03 -- Minimal Cross-Dataset History View

**Generated:** 2026-04-18
**Dataset:** sc2egset
**Game:** SC2
**Step:** 01_04_03
**Predecessor:** 01_04_02 (Data Cleaning Execution)

## Summary

Created `matches_history_minimal` VIEW -- 8-column player-row-grain projection of
`matches_flat_clean` (2 rows per 1v1 match). Canonical TIMESTAMP temporal dtype
(via TRY_CAST of `details_timeUTC`). Per-dataset-polymorphic faction vocabulary.
Cross-dataset-harmonized substrate for Phase 02+ rating-system backtesting.
Pure non-destructive projection (I9).

## Schema (8 columns)

| column | dtype | semantics |
|---|---|---|
| `match_id` | VARCHAR | `'sc2egset::'` + 32-char hex replay_id (length = 42) |
| `started_at` | TIMESTAMP | TRY_CAST of details_timeUTC; canonical cross-dataset type |
| `player_id` | VARCHAR | Battle.net toon_id |
| `opponent_id` | VARCHAR | Opposing toon_id |
| `faction` | VARCHAR | Raw race stems `Prot`/`Terr`/`Zerg` (4-char; NOT full names). PER-DATASET POLYMORPHIC |
| `opponent_faction` | VARCHAR | Opposing race (same vocabulary as faction) |
| `won` | BOOLEAN | Focal player's outcome (complementary between the 2 rows) |
| `dataset_tag` | VARCHAR | Constant `'sc2egset'` |

## Row-count flow

| metric | value |
|---|---|
| Source matches_flat_clean rows | 44418 |
| Source distinct replay_ids | 22209 |
| matches_history_minimal total rows | 44418 |
| distinct match_ids | 22209 |
| matches with exactly 2 rows | 22209 |
| matches with NOT 2 rows | 0 |

## Faction vocabulary (per-dataset polymorphic)

| faction | count |
|---|---|
| `Prot` | 16121 |
| `Zerg` | 15527 |
| `Terr` | 12770 |

NOTE: sc2egset faction vocabulary is 4-char race stems (Prot/Terr/Zerg).
Consumers MUST NOT treat faction as a single categorical feature across
datasets without game-conditional encoding.

## Temporal sanity (I3)

| metric | value |
|---|---|
| min_started_at | 2016-01-07 02:21:46.002000 |
| max_started_at | 2024-12-01 23:48:45.251161 |
| null_started_at (TRY_CAST failures) | 0 |
| distinct_started_at | 22164 |

## NULL counts

| column | null count | gate |
|---|---|---|
| match_id | 0 | 0 (GATE) |
| started_at | 0 | report only |
| player_id | 0 | 0 (GATE) |
| opponent_id | 0 | 0 (GATE) |
| won | 0 | 0 (GATE) |
| dataset_tag | 0 | 0 (GATE) |
| faction | 0 | report only |
| opponent_faction | 0 | report only |

## Gate verdict

| check | result |
|---|---|
| Row count 44,418 = 2 x 22,209 | PASS |
| Column count 8 | PASS |
| started_at dtype TIMESTAMP | PASS |
| I5-analog NULL-safe symmetry violations (IS DISTINCT FROM) = 0 | PASS |
| match_id prefix violations = 0; length = 42 | PASS |
| dataset_tag distinct count = 1 | PASS |
| Zero NULLs in match_id / player_id / opponent_id / won / dataset_tag | PASS |
| All assertions pass | PASS |

## Artifact

Validation JSON: `games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_03_minimal_history_view.json`
