# Step 01_04_03 -- Minimal Cross-Dataset History View (aoestats)

**Generated:** 2026-04-18
**Dataset:** aoestats
**Game:** AoE2
**Step:** 01_04_03
**Predecessor:** 01_04_02 (Data Cleaning Execution)
**Schema version:** 9-col (ADDENDUM: duration_seconds added 2026-04-18)

## Summary

Created `matches_history_minimal` VIEW -- 9-column player-row-grain view of
`matches_1v1_clean` (2 rows per 1v1 match via UNION ALL pivot). Canonical TIMESTAMP
temporal dtype (via CAST from TIMESTAMPTZ AT TIME ZONE 'UTC'). Per-dataset-polymorphic
faction vocabulary (full AoE2 civ names, ~50 distinct). Cross-dataset-harmonized
substrate for Phase 02+ rating-system backtesting. Pure non-destructive projection (I9).

aoestats-specific: UNION ALL erases slot bias -- overall_won_rate = 0.5 exactly
(upstream slot asymmetry team=1 wins ~52.27% preserved at slot level only).

ADDENDUM: Added `duration_seconds` BIGINT (column 8) between `won` and `dataset_tag`.
Source: matches_raw.duration / 1_000_000_000 (Arrow duration[ns] -> BIGINT nanoseconds;
R1-BLOCKER-A1 fix: divide by 1e9 not 1e3). POST_GAME_HISTORICAL.

## Schema (9 columns)

| column | dtype | semantics |
|---|---|---|
| `match_id` | VARCHAR | `'aoestats::'` + game_id (VARCHAR passthrough; opaque, variable length) |
| `started_at` | TIMESTAMP | CAST(started_timestamp AT TIME ZONE 'UTC' AS TIMESTAMP); canonical cross-dataset type |
| `player_id` | VARCHAR | CAST(p{0,1}_profile_id AS VARCHAR); focal player |
| `opponent_id` | VARCHAR | Opposing player |
| `faction` | VARCHAR | Full civ name (Mongols, Franks, etc.). PER-DATASET POLYMORPHIC |
| `opponent_faction` | VARCHAR | Opposing civ (same vocabulary as faction) |
| `won` | BOOLEAN | Focal player's outcome (complementary between the 2 rows) |
| `duration_seconds` | BIGINT | POST_GAME_HISTORICAL. matches_raw.duration / 1_000_000_000 (nanoseconds to seconds). |
| `dataset_tag` | VARCHAR | Constant `'aoestats'` |

## Row-count flow

| metric | value |
|---|---|
| Source matches_1v1_clean rows (1/match) | 17814947 |
| matches_history_minimal total rows (2/match) | 35629894 |
| distinct match_ids | 17814947 |
| matches with exactly 2 rows | 17814947 |
| matches with NOT 2 rows | 0 |

## Slot-bias gate (aoestats-specific)

| metric | value |
|---|---|
| overall_won_rate (GATE: == 0.5) | 0.5 |
| slot0_rate (informational) | 0.49931509759753984 |
| slot1_rate (informational) | 0.5006849024024601 |

UNION ALL erases slot bias: every match contributes 1 won=TRUE + 1 won=FALSE.

## duration_seconds stats (ADDENDUM gates)

| metric | value | gate |
|---|---|---|
| min_duration_seconds | 3 | report only |
| max_duration_seconds | 5574815 | <= 1_000_000_000 (Gate +5a HALTING unit canary) |
| p50_duration_seconds | 2455.0 | report only |
| p99_duration_seconds | 5729.0 | report only |
| avg_duration_seconds | 2418.1 | report only |
| null_duration_seconds | 0 | report only (Gate +2) |
| non_positive_count | 0 | 0 (Gate +3) |
| outlier_count_gt_86400 | 56 | report only (Gate +5b, no halt) |

**Gate +5a** (HALTING -- unit canary): max <= 1_000_000_000s (~31.7 years). Catches nanosecond-unit regression (skipping /1e9 would yield ~1e12). PASS.

**Gate +5b** (REPORT-ONLY): 56 rows have duration_seconds > 86400 (> 24h). These are raw-data corruption / abandoned matches. Outlier handling deferred to 01_04_02 augmentation follow-up PR. Pass-through at this step.

## Faction vocabulary (per-dataset polymorphic, top rows shown in full table)

| faction | count |
|---|---|
| `mongols` | 2265003 |
| `franks` | 2026638 |
| `magyars` | 1241182 |
| `britons` | 1233417 |
| `spanish` | 1179123 |
| `persians` | 1170753 |
| `ethiopians` | 1074509 |
| `khmer` | 1059050 |
| `lithuanians` | 1034419 |
| `huns` | 1015167 |
| `teutons` | 992269 |
| `turks` | 943042 |
| `byzantines` | 932024 |
| `goths` | 866697 |
| `portuguese` | 866560 |
| `mayans` | 818618 |
| `vietnamese` | 802481 |
| `cumans` | 798229 |
| `hindustanis` | 743151 |
| `japanese` | 724910 |
| `bulgarians` | 687951 |
| `malians` | 683157 |
| `chinese` | 658080 |
| `celts` | 655068 |
| `aztecs` | 638117 |
| `bohemians` | 624178 |
| `burgundians` | 624006 |
| `saracens` | 621252 |
| `incas` | 618112 |
| `poles` | 610246 |
| `vikings` | 599748 |
| `berbers` | 594412 |
| `sicilians` | 578332 |
| `italians` | 574629 |
| `malay` | 545978 |
| `slavs` | 529330 |
| `koreans` | 525268 |
| `tatars` | 506783 |
| `romans` | 476677 |
| `armenians` | 376649 |
| `gurjaras` | 375990 |
| `georgians` | 373825 |
| `burmese` | 364454 |
| `dravidians` | 289321 |
| `bengalis` | 286509 |
| `khitans` | 120186 |
| `wei` | 94624 |
| `wu` | 89910 |
| `shu` | 78213 |
| `jurchens` | 41647 |

NOTE: aoestats faction vocabulary is full AoE2 civilization names.
Consumers MUST NOT treat faction as a single categorical feature across
datasets without game-conditional encoding.

## Temporal sanity (I3)

| metric | value |
|---|---|
| min_started_at | 2022-08-29 00:04:05 |
| max_started_at | 2026-02-06 06:32:24 |
| null_started_at (CAST failures) | 0 |
| distinct_started_at | 15837208 |

## NULL counts

| column | null count | gate |
|---|---|---|
| match_id | 0 | 0 (GATE) |
| started_at | 0 | report only |
| player_id | 0 | 0 (GATE) |
| opponent_id | 0 | 0 (GATE) |
| won | 0 | 0 (GATE) |
| duration_seconds | 0 | report only (Gate +2) |
| dataset_tag | 0 | 0 (GATE) |
| faction | 0 | 0 (GATE) |
| opponent_faction | 0 | 0 (GATE) |

## Gate verdict

| check | result |
|---|---|
| Row count 35,629,894 = 2 x 17,814,947 | PASS |
| Column count 9 (Gate +1) | PASS |
| started_at dtype TIMESTAMP | PASS |
| duration_seconds dtype BIGINT | PASS |
| I5-analog NULL-safe symmetry violations (incl. duration) = 0 | PASS |
| match_id prefix violations = 0 | PASS |
| dataset_tag distinct count = 1 | PASS |
| Zero NULLs in 7 gated columns | PASS |
| SLOT-BIAS: AVG(won::INT) == 0.5 (tolerance 1e-9) | PASS |
| duration_seconds non-positive = 0 (Gate +3) | PASS |
| duration_seconds max <= 1_000_000_000 (Gate +5a HALTING unit canary) | PASS |
| duration_seconds outliers > 86400 (Gate +5b REPORT-ONLY) | 56 rows (no halt; deferred to 01_04_02 augmentation) |
| All assertions pass | PASS |

## Artifact

Validation JSON: `games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_03_minimal_history_view.json`
