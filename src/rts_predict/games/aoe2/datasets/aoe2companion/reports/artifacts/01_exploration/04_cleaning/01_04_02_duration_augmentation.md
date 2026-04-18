# Step 01_04_02 ADDENDUM -- Duration Augmentation: Post-Augmentation Validation

**Generated:** 2026-04-18
**Dataset:** aoe2companion
**Step:** 01_04_02 ADDENDUM -- duration_seconds + outlier flags

## Summary

Extends `matches_1v1_clean` VIEW from 48 to 51 columns by adding three duration-related
columns: `duration_seconds` BIGINT (POST_GAME_HISTORICAL), `is_duration_suspicious` BOOLEAN,
and `is_duration_negative` BOOLEAN. No raw tables modified (Invariant I9). Row counts
unchanged (column-only addendum). All 13 gate assertions pass.

**Threshold justification (I7):** 86,400s (24h) threshold from 01_04_03 Gate+5b empirical
precedent (~25x p99=3,458s); Tukey (1977) EDA sanity bound; I8 cross-dataset canonical
(identical across sc2egset/aoestats/aoe2companion).

**is_duration_negative semantics:** strict `< 0` (Q2 resolved). 16 zero-duration rows are
UNFLAGGED by both new flags (known state; Phase 02 handles these).

## CONSORT Column-Count Flow

| VIEW | Cols before | Cols added | Cols after | New columns |
|---|---|---|---|---|
| matches_1v1_clean | 48 | 3 | 51 | duration_seconds BIGINT, is_duration_suspicious BOOLEAN, is_duration_negative BOOLEAN |

## Duration Statistics

| Statistic | Value |
|---|---|
| min | -3,041s |
| p50 | 1,433s (~23 min) |
| p99 | 3,458s (~57 min) |
| max | 3,279,303s (~37 days -- bogus wall-clock abandoned match) |
| null_count | 0 (0.0% -- finished empirically non-NULL in 1v1 ranked scope) |
| suspicious_count (>86400) | 142 (142 expected; HALTING gate) |
| negative_count (strict <0) | 342 (342 expected; HALTING gate; clock skew) |
| zero_duration_count | 16 (16 expected; unflagged by both flags; known state) |

## Gate Results

| Gate | Result |
|---|---|
| gate_1_col_count_51 | PASS |
| gate_1_last3_duration_seconds_bigint | PASS |
| gate_1_last3_is_duration_suspicious_boolean | PASS |
| gate_1_last3_is_duration_negative_boolean | PASS |
| gate_2_row_count_61062392 | PASS |
| gate_2_match_count_30531196 | PASS |
| gate_3_null_fraction_leq_1pct | PASS |
| gate_4_max_duration_leq_1B | PASS |
| gate_5_suspicious_count_142 | PASS |
| gate_6_negative_count_342_strict_lt0 | PASS |
| gate_10_r03_complementarity_intact | PASS |
| gate_10_legacy_cols_present | PASS |
| i3_forbidden_cols_absent | PASS |

## SQL Queries (Invariant I6)

All DDL and assertion SQL stored verbatim in `01_04_02_duration_augmentation.json`
under the `sql_queries` key.
