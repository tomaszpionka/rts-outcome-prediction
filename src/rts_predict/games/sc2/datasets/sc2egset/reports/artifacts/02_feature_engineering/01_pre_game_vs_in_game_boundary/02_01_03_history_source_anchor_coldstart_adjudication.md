# SC2EGSet Step 02_01_03 — History-Enriched Pre-Game Source / Anchor / Cold-Start Adjudication

## §1 Non-Overclaim Disclaimer

This artifact is an adjudication of 8 coupled pre-materialization questions for sc2egset Step 02_01_03 (tranche-2, 6 history-enriched pre_game families). It does NOT materialize any feature value, does NOT run the CROSS-02-01-v1.0.1 post-materialization leakage audit, does NOT close Step 02_01_03, and does NOT append to any status YAML or research_log. Materialization remains FUTURE.

## §2-§9 Per-Q Decisions

### Q1_source_layer — History-enriched pre_game source layer (target row + history row + asymmetry; divergence + extension annotated)

- **Verdict:** `extend_with_evidence`
- **Binding level:** `binding_for_materialization`
- **Scope:** `all_six_history_enriched_pre_game_families`

**Rationale / notes:**

Q1 binds the source layer for the 6 history-enriched pre_game families. Target = matches_flat_clean (RATIFY tranche-1 PR #234 Q1 binding; 1v1-scoped, 44,418 rows). History = player_history_all (all-game-types, 44,817 rows). Target/history asymmetry is asymmetric.

Verbatim spec evidence (Option A; RECOMMENDED; BINDING):
  (1) reports/specs/02_02_feature_engineering_plan.md §6.2 row 1 (focal_player_history): 'rolling/expanding aggregates over player_history_all rows for the focal toon_id: prior match count, prior win rate, time since prior match, race-conditional, map-conditional, matchup-conditional'.
  (2) reports/specs/02_02_feature_engineering_plan.md §6.2 row 4 (reconstructed_rating): 'derived from player_history_all filtered by I3 anchor'.
  (3) reports/specs/02_02_feature_engineering_plan.md §6.2 row 6 (in_game_history_aggregate): 'player_history_all APM / SQ / supplyCappedPercent / header_elapsedGameLoops (IN_GAME_HISTORICAL classification per CROSS-02-00 §5.4)'.
  (4) reports/specs/02_00_feature_input_contract.md §2.1 sc2egset row grain: '1 row per player per match (all game types; no 1v1 filter)'.
  (5) player_history_all.yaml provenance.scope: 'All replays (no 1v1/decisive filter). Includes non-1v1 and indecisive replays excluded from matches_flat_clean'.

Alternative B (REJECTED): symmetric — target and history both filtered to 1v1-only. Rejected because (a) the spec §6.2 row 1 binds history to player_history_all, not a 1v1-filtered subset; (b) the 83.95% MMR-missing density makes restricting history to 1v1-only leave cold-start gates G-CS-2/G-CS-3 with near-empty support sets for newcomers; (c) CROSS-02-02 §6.2 retains multi-game-type history precisely to mitigate this support-set sparsity; (d) the player_history_all.yaml provenance.scope note explicitly retains non-1v1 and indecisive replays for this purpose. Rejecting Alternative B would contradict the verbatim §6.2 rows 4 and 6 bindings.

**Evidence paths:**

```
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.md
reports/specs/02_00_feature_input_contract.md
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml
src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
```

### Q2_target_anchor — Target match temporal anchor for the strict-< history filter

- **Verdict:** `ratify_with_evidence`
- **Binding level:** `binding_for_materialization`
- **Scope:** `all_six_history_enriched_pre_game_families`
- **Target anchor:** `matches_history_minimal.started_at TIMESTAMP`

**Rationale / notes:**

RATIFY tranche-1 PR #234 Q2(a) BINDING: target_anchor = matches_history_minimal.started_at TIMESTAMP (canonical cross-dataset dtype per CROSS-02-00 §3.1; DESCRIBE TIMESTAMP confirmed; 0 nulls; 0 cross-row inconsistency). Phase-03 hold-out anchor (Q2(b) per PR #234) remains RECOMMENDATION ONLY for Phase 03 planning.

**Evidence paths:**

```
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv
src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml
reports/specs/02_00_feature_input_contract.md
```

### Q3_history_time_column — Historical row time column for strict-< filter (canonical TRY_CAST form)

- **Verdict:** `bind_now`
- **Binding level:** `binding_for_materialization`
- **Scope:** `all_six_history_enriched_pre_game_families`
- **History time column:** `player_history_all.details_timeUTC (TRY_CAST AS TIMESTAMP for comparison with target.started_at)`

**Rationale / notes:**

Strict-< filter expression (CANONICAL per B-X2): TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at. This is exactly STRICT_LT_HISTORY_FILTER. The ROADMAP §02_01_03 raw form 'ph.details_timeUTC < target.started_at' is recorded for provenance ONLY (as STRICT_LT_FILTER_ROADMAP_RAW); this adjudication explicitly NORMALIZES that raw form to the canonical TRY_CAST expression for chronological fidelity per matches_history_minimal.yaml (7 observed length variants 22-28 chars in upstream VARCHAR; lex comparison is NOT chronologically faithful). Deterministic ordering via (player_id_worldwide, TRY_CAST(ph.details_timeUTC AS TIMESTAMP), ph.replay_id). 1000-row TRY_CAST NULL-rate sanity probe required: q3_strict_lt_smoke_failed halts if any NULL.

**Evidence paths:**

```
src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml
src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml
reports/specs/02_00_feature_input_contract.md (§5.4 sc2egset PH details_timeUTC row)
src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md (§02_01_03 raw form: STRICT_LT_FILTER_ROADMAP_RAW)
```

### Q4_cold_start_policy — Cold-start policy per family (G-CS-2/3/4/5; G-CS-6 distinguished as materialization-time gate)

- **Verdict:** `extend_with_evidence`
- **Binding level:** `binding_for_materialization`
- **Scope:** `all_six_history_enriched_pre_game_families`
- **Cold-start policy:** `G-CS-2:scaffold_registry_gate_for_focal_player_history+opponent_player_history+in_game_history_aggregate|G-CS-3:scaffold_registry_gate_for_matchup_history_aggregate|G-CS-4:scaffold_registry_gate_for_reconstructed_rating|G-CS-5:scaffold_registry_gate_for_cross_region_fragmentation_handling|G-CS-6:materialization_time_fold_aware_fit_gate_per_invariant_I3_and_CROSS-02-02_section_9`

**Rationale / notes:**

Distinguishes: scaffold registry gates G-CS-2/3/4/5 (registry-time; bound here); G-CS-6 (materialization-time fold-aware fit gate per ROADMAP lines 2334-2338; DEFERRED to materialization PR); model-training Phase-03 cold-start handling (DEFERRED to Phase 03). ML-protocol three failure modes (rolling aggregates, head-to-head, co-occurring matches) explicitly forbidden; only match_time < T evidence used. Per B-X1 the notes field is EXEMPT from POST-GAME token scanning.

**Evidence paths:**

```
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
reports/specs/02_02_feature_engineering_plan.md (§9 G-CS-2..G-CS-6)
src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md (lines 2334-2338)
```

### Q5_cross_region_policy — Cross-region fragmentation operationalization (RISK-20)

- **Verdict:** `deferred_blocker`
- **Binding level:** `deferred_blocker`
- **Scope:** `sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling`
- **Cross-region policy:** `deferred_blocker`

**Rationale / notes:**

CROSS-02-02 §6.2 row 5 enumerates three options: strict_exclusion (drop cross-region players from train+test); dual_feature_path (maintain separate per-region history aggregates with explicit merge rules); sensitivity_indicator_co_registration (retain a binary is_cross_region indicator alongside the merged history). The retention impact of each option is empirically conditional; binding any here without a measurement study would pin a numeric without evidence (Invariant I7 violation). The PR #241 scaffold validator accepts allowed_with_caveat without pinning; this adjudication preserves that deferral as an explicit BINDING gate against materialization. MATERIALIZATION BLOCKED until Q5 is upgraded to bind_now in a successor adjudication PR with retention-measurement evidence.

**Evidence paths:**

```
reports/specs/02_02_feature_engineering_plan.md (§6.2 row 5)
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/06_decision_gates/risk_register_sc2egset.md (RISK-20)
src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py (_check_cross_region_caveat)
```

### Q6_rating_policy — Rating reconstruction model family for reconstructed_rating (G-CS-4)

- **Verdict:** `deferred_blocker`
- **Binding level:** `deferred_blocker`
- **Scope:** `sc2egset.history_enriched_pre_game.reconstructed_rating`
- **Rating policy:** `deferred_blocker`

**Rationale / notes:**

deferred_blocker because: per N3, ~83.95% MMR-missing density (verified in the dataset research log; consistent with the registry CSV is_mmr_missing_flag family) makes algorithm choice first-order. Pinning Elo / Glicko / Glicko-2 / TrueSkill / a rolling-winrate baseline without empirical evidence of which family handles the unrated / no-rating-history regime best would violate Invariant I7. Four candidate citations exist (Elo 1978; Glickman 1999; Glickman 2012; Herbrich, Minka, Graepel 2006) but binding one over the others requires repo evidence not yet generated. Forward-only constraint explicit: no target-match outcome; no future results; no global batch fit; per-game forward update only. Cold-start handled by initializing rating = literature-prior for new players (DEFERRED to materialization PR's training-fold-fit step); missingness handled by retaining is_mmr_missing as a separate companion feature (DEFERRED to materialization PR). Per B-X1 the notes field is EXEMPT from POST-GAME token scanning, so negated-prose phrases are allowed here. MATERIALIZATION BLOCKED until Q6 is upgraded to bind_now in a successor adjudication PR with rating-family empirical evaluation evidence satisfying the N-X3 strengthened gate (>=1 repo path + >=1 citation + forward-only wording + cold-start/missingness wording).

**Evidence paths:**

```
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
reports/specs/02_02_feature_engineering_plan.md (§6.2 row 4; §9 G-CS-4)
src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md (is_mmr_missing density 83.95%)
Elo (1978)
Glickman (1999)
Glickman (2012)
Herbrich, Minka, Graepel (2006)
```

### Q7_in_game_historical_policy — IN_GAME_HISTORICAL prior-match aggregation policy for in_game_history_aggregate

- **Verdict:** `bind_now`
- **Binding level:** `binding_for_materialization`
- **Scope:** `sc2egset.history_enriched_pre_game.in_game_history_aggregate`
- **In-game-historical policy:** `prior_match_only_strict_lt`
- **In-game-historical columns in scope:** `APM|SQ|supplyCappedPercent|header_elapsedGameLoops`

**Rationale / notes:**

CROSS-02-00 §5.4 Concern 8 / T15 record retains these 4 columns (APM|SQ|supplyCappedPercent|header_elapsedGameLoops) in scope for prior-match aggregation ONLY; never as direct game-T pre-game features. Source = player_history_all (per ROADMAP line 2367 + CROSS-02-02 §6.2 row 6). Strict-< filter expression (CANONICAL per B-X2): TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at. Aggregation only over rows where history_time < target_time (prior matches); never the target match itself. Distinct from in_game_snapshot tranche; aggregation pseudocount / window-size constants DEFERRED to materialization PR. Per B-X1 notes exempt from POST-GAME scan.

**Evidence paths:**

```
reports/specs/02_00_feature_input_contract.md (§5.4 sc2egset PH IN_GAME_HISTORICAL rows; Concern 8 / T15 record)
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv (row 12)
src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md (line 2367 inputs.duckdb_tables)
```

### Q8_matches_history_minimal_consumption — What matches_history_minimal is consumed for in the history-enriched pre_game tranche

- **Verdict:** `ratify_with_evidence`
- **Binding level:** `binding_for_materialization`
- **Scope:** `NOT_A_FEATURE_SOURCE_unless_explicitly_justified`

**Rationale / notes:**

MHM is consumed for (1) target row identity / started_at TIMESTAMP anchor per PR #234 Q2(a) BINDING (the canonical source of started_at joined back onto matches_flat_clean); (2) cold-start enumeration G-CS-2/3/4/5 (the support set of (focal_player, target.started_at) target rows over which prior history is counted). MHM is NOT a feature source — no MHM column becomes a feature column in the materialized output unless this adjudication row is updated in a successor PR with explicit justification. MHM column-level provenance recorded for examiner clarity; no MHM PRE_GAME column elevated to feature without successor-PR adjudication. Per B-X1 notes exempt from POST-GAME scan.

**Evidence paths:**

```
sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py (scaffold cell: What matches_history_minimal is consumed for)
src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md (inputs.duckdb_tables line 2366)
reports/specs/02_00_feature_input_contract.md (§5.1 sc2egset MHM column table)
```

## §10 Falsifier Roll-Call

Every falsifier from `HELPER_TO_FALSIFIER_KEY.values()`:

- `pr241_sha256_mismatch`: did_not_fire
- `provenance_sha_invalid`: did_not_fire
- `decision_count_mismatch`: did_not_fire
- `q1_single_row_violation`: did_not_fire
- `q1_source_layer_evidence_inconsistent`: did_not_fire
- `strict_lt_filter_divergence`: did_not_fire
- `q2_target_anchor_type_mismatch`: did_not_fire
- `q3_history_time_column_invalid`: did_not_fire
- `q3_strict_lt_smoke_failed`: did_not_fire
- `q4_cold_start_gates_incomplete`: did_not_fire
- `q4_cold_start_leakage`: did_not_fire
- `q5_cross_region_three_options_not_enumerated`: did_not_fire
- `q6_rating_default_deferred_violated`: did_not_fire
- `q6_rating_forward_only_missing`: did_not_fire
- `q7_in_game_historical_columns_drift`: did_not_fire
- `q7_no_target_match_tracker_missing`: did_not_fire
- `in_game_historical_strict_lt_violated`: did_not_fire
- `q8_mhm_documentation_missing`: did_not_fire
- `universal_post_game_token_in_scoped_field`: did_not_fire
- `universal_tracker_source_in_history`: did_not_fire
- `materialization_creep`: did_not_fire

### Verbatim canonical strict-< smoke SQL (Invariant I6)

```sql
SELECT COUNT(*) FROM player_history_all ph
JOIN matches_history_minimal target ON ph.toon_id = target.player_id
WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
  AND ph.replay_id = REPLACE(target.match_id, 'sc2egset::', '')
```

### Probe row counts

- `matches_flat_clean`: 44418
- `matches_flat_clean_distinct_replay_id`: 22209
- `matches_history_minimal`: 44418
- `player_history_all`: 44817

## §11 Lineage Position

Artifact #3 in the lineage chain for Step 02_01_03 readiness:
1. PR #239 ROADMAP stub.
2. PR #241 scaffold + validator.
3. THIS adjudication.
4. Future materialization plan.
5. Future materialization + CROSS-02-01 post-mat audit.
6. Future Step 02_01_03 closure PR.

## §12 Explicit Non-Substitution Statement

This artifact does NOT replace, weaken, or amend: (a) PR #229 §10 design-time verdict pair; (b) PR #230 vacuous CROSS-02-01 audit pair; (c) PR #234 tranche-1 adjudication; (d) PR #236 tranche-1 materialization + audit; (e) PR #237 tranche-1 closure; (f) PR #241 scaffold + validator; (g) the FUTURE materialization + post-materialization CROSS-02-01 audit (which do not yet exist).

## §13 Materialization Blocked Until Deferred-Blocker Resolved

If any decision row carries `verdict == "deferred_blocker"`, the future Layer-3 materialization PR must NOT proceed until that decision is upgraded to `bind_now` / `ratify_with_evidence` / `extend_with_evidence` / `narrow_with_evidence` in a successor adjudication PR. Q5 (cross-region) and Q6 (rating) are currently deferred_blocker.

## §14 No Step Closure Claim

Step 02_01_03 remains OPEN. This artifact does NOT add `02_01_03: complete` to `STEP_STATUS.yaml`. Closure is deferred to a separate post-materialization closure PR per the PR #237 tranche-1 closure precedent.
