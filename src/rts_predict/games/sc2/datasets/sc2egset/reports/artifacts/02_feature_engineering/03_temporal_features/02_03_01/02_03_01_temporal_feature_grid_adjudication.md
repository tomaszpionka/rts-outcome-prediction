# Step 02_03_01 temporal feature grid adjudication

Layer-2 decision-record output. No feature materialization. No concrete numerical winners pinned (Invariant I7). V1 + V3 preflights both PASS.

## 1. Scope

Adjudication of the SC2EGSet `02_03_01` temporal feature grid: Q1 window-type kinds, Q2 decay-type kinds, Q3 cold-start-type kinds, Q4 tracker `source_event_family` categories, Q5 in-game snapshot deferral boundary, Q6 cross-spec role separation, Q7 V1+V3 preflight gate, Q8 cross-game portability (syntactic-only).

## 2. Preflight gates

- V1 preflight: V1 PASS via `validate_predecessor_artifact_provenance(repo_root)`.
- V3 preflight: V3 PASS via `validate_temporal_discipline(repo_root)`.

## 3. SHA-pin provenance

| Pin column | SHA256 |
|---|---|
| `parent_02_01_02_parquet_sha256` | `24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39` |
| `parent_02_01_03_parquet_sha256` | `053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071` |
| `parent_02_01_99_csv_sha256` | `831a622c6e0a98c9642e466d5c9dced0fb6b621a6d58e3008a1b0218dd03c370` |
| `parent_02_02_01_parquet_sha256` | `c4b48601ee0ff800f4b823af270faf03571a637ce07c51a0ef6d072691896ff3` |
| `v1_validator_module_sha256` | `7945fc7fc7cf3500390c647c977702a14c3d5ab03c4ee7bbaf04d6bbe1033545` |
| `v3_validator_module_sha256` | `8e33b7ae0968cbaafa08c33b51e62196e7d4f19cadcd48b3b8d03b6aa2ae2a87` |
| `cross_02_02_spec_sha256` | `86af792370272e611f048aae0c48c9cc595eb4b44c1db38c0bb4ecea0ff1b289` |
| `cross_02_03_spec_sha256` | `59e3227307c51ad09fb12b485caec36aa54413d175cb46acc382c06fbb8ac546` |
| `tracker_eligibility_csv_sha256` | `11bd4b9ef7c80657a027db3831313c1d74c39b85834c25ecdfa78506e8ad8d22` |

## 4. Invariant I3 — strict history cutoff

Invariant I3 mandates `history_time < T` strictly (not `<=`) for all history features targeting game T. V3 enforces this at schema level (`started_at: timestamp[us]` anchor; strict-< naming convention). Every decision row carries the `invariant_i3_cited` column.

## 5. Cross-spec citations

- CROSS-02-02 §10 candidate family inventory: G-L-1 (fixed-game-count window), G-L-2 (fixed-calendar-duration window), G-L-3 (exponential decay), G-L-4 (step-function decay), G-L-5 (minimum-prior cold-start gate), G-L-6 (pseudocount smoothing), G-L-7 (combined gate + smoothing).
- CROSS-02-03 §4 post-selection audit predicate dimensions: D5 (cutoff operator correctness), D6 (target-game exclusion), D7 (post-game token exclusion).

CROSS-02-02 = source of candidate family inventory; CROSS-02-03 = source of post-selection audit predicate. These are distinct roles.

## 6. Tracker `source_event_family` cross-reference (15-family)

One row per row in `tracker_events_feature_eligibility.csv` (15 rows). Q4 decision rows aggregate per `source_event_family` (worst-case across `status_in_game_snapshot`): BLOCKED > ELIGIBLE_WITH_CAVEAT > ELIGIBLE. The `family_kind` cell is emitted verbatim from the CSV — `UnitInit / UnitDone` keeps its internal whitespace.

| # | feature_family | source_event_family | status_in_game_snapshot | aggregated_decision |
|---|---|---|---|---|
| 1 | `minerals_collection_rate_history_mean` | `PlayerStats` | `eligible_with_caveat` | `BLOCKED` |
| 2 | `army_value_at_5min_snapshot` | `PlayerStats` | `eligible_with_caveat` | `BLOCKED` |
| 3 | `supply_used_at_cutoff_snapshot` | `PlayerStats` | `eligible_with_caveat` | `BLOCKED` |
| 4 | `food_used_max_history` | `PlayerStats` | `eligible_with_caveat` | `BLOCKED` |
| 5 | `count_units_built_by_cutoff_loop` | `UnitBorn` | `eligible_for_phase02_now` | `ELIGIBLE_WITH_CAVEAT` |
| 6 | `time_to_first_expansion_loop` | `UnitBorn` | `eligible_with_caveat` | `ELIGIBLE_WITH_CAVEAT` |
| 7 | `count_units_killed_by_cutoff_loop` | `UnitDied` | `eligible_for_phase02_now` | `ELIGIBLE_WITH_CAVEAT` |
| 8 | `count_units_lost_by_cutoff_loop` | `UnitDied` | `eligible_with_caveat` | `ELIGIBLE_WITH_CAVEAT` |
| 9 | `morph_count_by_cutoff_loop` | `UnitTypeChange` | `eligible_for_phase02_now` | `ELIGIBLE` |
| 10 | `count_upgrades_by_cutoff_loop` | `Upgrade` | `eligible_with_caveat` | `ELIGIBLE_WITH_CAVEAT` |
| 11 | `mind_control_event_count` | `UnitOwnerChange` | `blocked_until_additional_validation` | `BLOCKED` |
| 12 | `army_centroid_at_cutoff_snapshot` | `UnitPositions` | `blocked_until_additional_validation` | `BLOCKED` |
| 13 | `building_construction_count_by_cutoff_loop` | `UnitInit / UnitDone` | `eligible_for_phase02_now` | `ELIGIBLE` |
| 14 | `slot_identity_consistency` | `PlayerSetup` | `eligible_for_phase02_now` | `ELIGIBLE` |
| 15 | `playerstats_cumulative_economy_fields` | `PlayerStats` | `blocked_until_additional_validation` | `BLOCKED` |

## 7. Q1 temporal window-type kinds (deferred)

Q1 enumerates window-type kinds (G-L-1 fixed-game-count, G-L-2 fixed-calendar-duration, G-L-3 exponential decay). Concrete numerical winner selection (specific game counts, day counts, half-life values) is DEFERRED to the future materialization PR per Invariant I7. The decision cell reads `DEFER_TO_MATERIALIZATION`.

## 8. Q2 decay-type kinds (deferred)

Q2 enumerates decay-type kinds (G-L-3 exponential, G-L-4 step-function). Concrete tau half-life values or step sizes are NOT pinned at adjudication; DEFERRED to materialization per Invariant I7.

## 9. Q3 cold-start-type kinds (deferred)

Q3 enumerates cold-start kinds (G-L-5 minimum-prior gate, G-L-6 pseudocount smoothing, G-L-7 combined). Concrete k-threshold values and pseudocount magnitudes are NOT pinned; DEFERRED to materialization per Invariant I7.

## 10. Q5 in-game snapshot deferral

In-game snapshot families are DEFERRED past `02_03_01`. The `02_03_01` adjudication step covers `pre_game` and `history_enriched_pre_game` prediction settings only. In-game snapshot adjudication proceeds in a later step.

## 11. Q6 cross-spec role separation

CROSS-02-02 = source of candidate family inventory; CROSS-02-03 = source of post-selection audit predicate. These are distinct roles.

## 12. Q7 preflight gate outcome

V1 PASS + V3 PASS recorded. Both preflights ran before the output directory was created (V1.H6 / V3.H5 paradox guard satisfied).

## 13. Q8 cross-game portability (syntactic-only)

The adjudicator's public API uses cross-game-portable vocabulary only (focal/opponent, history, prior, target-exclusion, candidate, winner, window-type, decay-type, cold-start-type). The design pattern is syntactically portable. The Q8 stance is SYNTACTIC_ONLY: no empirical cross-target claim is made; any second-game-target determination is deferred to a future second-game-specific Phase 02 step.

## 14. Decision CSV summary

Decision CSV has 16 body rows × 16 columns (7 base + 9 SHA-pin provenance). Every row carries identical SHA-pin values; the `family_kind`, `decision`, `rationale_g_l_ref`, `rationale_d_ref`, and `invariant_i3_cited` columns vary per Q-row.
