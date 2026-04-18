# Step 01_04_03 -- Minimal Cross-Dataset History View (aoe2companion)

**Generated:** 2026-04-18
**Dataset:** aoe2companion
**Game:** AoE2
**Step:** 01_04_03
**Predecessor:** 01_04_02 (Data Cleaning Execution)
**Schema version:** 9-col (ADDENDUM: duration_seconds added 2026-04-18)

## Summary

Created `matches_history_minimal` TABLE -- 9-column player-row-grain projection of
`matches_raw` (filtered to matches_1v1_clean scope; 2 rows per 1v1 match). Self-join
pattern (sc2egset PR #152 precedent). Canonical TIMESTAMP temporal dtype (pass-through;
matches_raw.started is already TIMESTAMP). Per-dataset-polymorphic faction
vocabulary (full AoE2 civ names). Cross-dataset-harmonized substrate for Phase 02+
rating-system backtesting. Pure non-destructive projection (I9).

**Implementation note (DuckDB 1.5.1 workaround):**
Three-step DDL -- (1) CREATE TABLE _good_match_ids; (2) CREATE TABLE _mhm_base
(includes duration_seconds); (3) CREATE TABLE matches_history_minimal via self-join;
(4) DROP staging tables.

**ADDENDUM:** Added `duration_seconds` BIGINT (column 8) between `won` and `dataset_tag`.
Source: EXTRACT(EPOCH FROM (r.finished - r.started)) in _mhm_base staging (in-place;
matches_raw already joined). NULL if r.finished is NULL (abandoned matches).
Gate +6 (HALTING): NULL fraction <= 1%.

aoec-specific notes:
- No UNION ALL pivot needed (natively 2-row per match).
- No slot-bias gate (no slot column; natively player-row).
- Zero-NULL gate for faction + opponent_faction (civ zero-NULL upstream per 01_04_02).
- matchId INTEGER -> variable decimal width; numeric-tail regex + round-trip cast (I7).

## Schema (9 columns)

| column | dtype | semantics |
|---|---|---|
| `match_id` | VARCHAR | `'aoe2companion::'` + decimal matchId (variable width) |
| `started_at` | TIMESTAMP | Pass-through from matches_raw.started (already TIMESTAMP) |
| `player_id` | VARCHAR | CAST(profileId AS VARCHAR) |
| `opponent_id` | VARCHAR | Opposing profileId (from self-join) |
| `faction` | VARCHAR | Full civ name (e.g., Franks, Mongols). PER-DATASET POLYMORPHIC |
| `opponent_faction` | VARCHAR | Opposing civ (same vocabulary as faction) |
| `won` | BOOLEAN | Focal player's outcome (complementary between the 2 rows) |
| `duration_seconds` | BIGINT | POST_GAME_HISTORICAL. EXTRACT(EPOCH FROM (finished - started)). NULL if finished IS NULL. |
| `dataset_tag` | VARCHAR | Constant `'aoe2companion'` |

## Row-count flow

| metric | value |
|---|---|
| Source matches_1v1_clean rows | 61062392 |
| matches_history_minimal total rows | 61062392 |
| distinct match_ids | 30531196 |
| matches with exactly 2 rows | 30531196 |
| matches with NOT 2 rows | 0 |

## duration_seconds stats (ADDENDUM gates)

| metric | value | gate |
|---|---|---|
| min_duration_seconds | -3041 | report only |
| max_duration_seconds | 3279303 | <= 1_000_000_000 (Gate +5a HALTING) |
| p50_duration_seconds | 1433.0 | report only |
| p99_duration_seconds | 3458.0899999961257 | report only |
| avg_duration_seconds | 1418.0 | report only |
| null_duration_seconds | 0 | report only (Gate +2) |
| null_fraction | 0.000000 (0.0000%) | <= 1% (Gate +6 HALTING) |
| non_positive_count | 358 | 0 (Gate +3) |
| outlier_count_gt_86400 | 142 | report only (Gate +5b) |

## matchId range (aoec-specific, exploratory)

| metric | value |
|---|---|
| min_match_id_val | 32255750 |
| max_match_id_val | 468020658 |
| max_decimal_digits | 9 |

## Faction vocabulary (per-dataset polymorphic, top 20)

| faction | count |
|---|---|
| `franks` | 3654980 |
| `mongols` | 3637382 |
| `britons` | 2307906 |
| `magyars` | 2083367 |
| `spanish` | 2049447 |
| `persians` | 1961939 |
| `khmer` | 1844759 |
| `huns` | 1835466 |
| `ethiopians` | 1809660 |
| `lithuanians` | 1808825 |
| `teutons` | 1736479 |
| `byzantines` | 1650466 |
| `turks` | 1631781 |
| `goths` | 1518255 |
| `mayans` | 1480704 |
| `portuguese` | 1467158 |
| `cumans` | 1370309 |
| `vietnamese` | 1358316 |
| `japanese` | 1282181 |
| `hindustanis` | 1261243 |

NOTE: aoe2companion faction vocabulary is full civilization names (e.g., Franks, Mongols).
Consumers MUST NOT treat faction as a single categorical feature across
datasets without game-conditional encoding.

## Temporal sanity (I3)

| metric | value |
|---|---|
| min_started_at | 2020-07-31 23:30:34 |
| max_started_at | 2026-04-04 23:58:58 |
| null_started_at (pass-through) | 0 |
| distinct_started_at | 26623674 |

## NULL counts

| column | null count | gate |
|---|---|---|
| match_id | 0 | 0 (GATE) |
| started_at | 0 | 0 (GATE; pass-through TIMESTAMP) |
| player_id | 0 | 0 (GATE) |
| opponent_id | 0 | 0 (GATE) |
| won | 0 | 0 (GATE) |
| duration_seconds | 0 | report only + Gate +6 |
| dataset_tag | 0 | 0 (GATE) |
| faction | 0 | 0 (GATE; civ zero-NULL upstream) |
| opponent_faction | 0 | 0 (GATE; civ zero-NULL upstream) |

## Gate verdict (18 gates; no slot-bias gate -- aoec natively player-row)

| check | result |
|---|---|
| Row count 61,062,392 = 2 x 30,531,196 | PASS |
| Column count 9 (Gate +1) | PASS |
| started_at dtype TIMESTAMP | PASS |
| duration_seconds dtype BIGINT | PASS |
| I5-analog NULL-safe symmetry violations (incl. duration) = 0 | PASS |
| Zero NULLs: match_id / player_id / opponent_id / won / dataset_tag | PASS |
| Zero NULLs: faction / opponent_faction (civ zero-NULL upstream) | PASS |
| Prefix violations = 0 (numeric-tail regex + round-trip cast) | PASS |
| dataset_tag distinct count = 1, value 'aoe2companion' | PASS |
| matches_with_not_2_rows = 0 | PASS |
| duration_seconds non-positive count (Gate +3 REPORT-ONLY for aoec) | 358 rows (clock skew) |
| duration_seconds max <= 1_000_000_000 (Gate +5a HALTING) | PASS |
| duration_seconds outlier_count_gt_86400 (Gate +5b REPORT-ONLY) | 142 rows |
| duration_seconds NULL fraction <= 1% (Gate +6 HALTING) | PASS |
| All assertions pass | PASS |

## Artifact

Validation JSON: `games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_03_minimal_history_view.json`
