# Q6G Rating-Implementation Proof

**Audit PR:** PR #249

## 1. Non-Materialization Disclaimer

This artifact is the Q6G rating-implementation PROOF only. It does NOT materialize any rating value, does NOT write any Parquet, does NOT run the CROSS-02-01 post-materialization leakage audit, does NOT close Step 02_01_03, does NOT update any status YAML, and does NOT touch the dataset research_log or ROADMAP. The per-path metrics and equivalence / determinism statistics in this artifact are EVALUATION TRACES of forward-only rating predictions; they are Q6G-internal and are NOT Phase-03 baseline modelling results.

## 2. Parent PR #242 Lineage

- CSV SHA256: `f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv`)
- MD  SHA256: `fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md`)

## 3. Parent PR #243 Lineage (Q5 Preserved)

- CSV SHA256: `29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.csv`)
- MD  SHA256: `026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.md`)

Q5_selected_policy = `sensitivity_indicator_co_registration`; verdict = `narrow_with_evidence`. This proof does NOT re-adjudicate Q5.

## 4. Parent PR #245 Lineage (Q6 Discharged)

- CSV SHA256: `703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.csv`)
- MD  SHA256: `7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.md`)

PR #245 closed Q6 with verdict `deferred_blocker` and materialization_permission `blocked_pending_algorithm_survey_pr`. PR #247 (Q6F) discharged the algorithm-survey deferral with `Q6F_selected_policy = narrow_with_evidence`.

## 5. Parent PR #247 Lineage (Q6F -> this proof)

- CSV SHA256: `249e5591c6505b748fe3d371284a72d8f4620f57dbe9628c908ec2fbf097c8ed` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.csv`)
- MD  SHA256: `4b49bee405bf87d4b8920b188e2c38d185ecc077b532d64a8bdd5a90cdf143f2` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.md`)

`Q6F_selected_policy = narrow_with_evidence`; materialization_permission = `recommendation_only_blocked_pending_implementation_proof_pr`. This Q6G implementation-proof PR is the direct unblock condition for the `_blocked_pending_implementation_proof_pr` clause. The Q6F verdict is BINDING and is NOT re-adjudicated by this proof.

## 6. Q6G-Only Scope

Q6G is the Layer-2 implementation proof for the Glicko-2 candidate. It is NOT Phase-03 baseline modelling. The metrics are evaluation traces, not features. It does NOT train any downstream classifier. The outcome of each PHA row is used only to score the forward-only prediction and to update the rating state for FUTURE rows; it is never read as a feature input for predicting its own match. Q6G is also NOT feature materialization: Layer-3 materialization is a SEPARATE PR contingent on the Q6G verdict.

## 7. Glicko-2 Single-Candidate Justification (A5)

PR #247 section 11 ranked Glicko-2 lowest by log-loss among the 4 included candidates (Glicko-2 = 0.6255 vs TrueSkill = 0.6291); the minimum-unblock unit is to prove the chosen candidate's implementation. Q6G proves Glicko-2 specifically. TrueSkill is NOT re-implemented in Q6G. If Q6G's verdict is `defer_to_two_candidate_implementation_comparison`, a separate Q6H PR would implement TrueSkill alongside.

## 8. Algorithm Specification

Glicko-2 (Glickman 2012). Internal scale mapping: r -> (r - 1500) / 173.7178 to convert rating from Glicko scale to Glicko-2 internal mu units; RD -> RD / 173.7178 to convert rating deviation to Glicko-2 phi units; sigma is the volatility. Event-by-event simplification (Row 1): each match treated as a single-observation rating period; sigma held constant; the full batched volatility update is deferred to Row 2's batched path. Batched-production shape (Row 2): rating-period batching per Glickman 2012 section 3 equations 4-9 with rating_period_days=30 (A22) and iteration_tol=1e-6. Symbols mu, sigma, RD, phi, tau refer to the Glicko-2 player state and system constant as defined in Glickman 2012.

## 9. Forward-Only Update Semantics + Strict-`<` Filter Inheritance

Every per-row prediction uses rating state computed strictly from PHA records satisfying `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at` (verbatim from PR #242 / PR #247). The target outcome updates the rating state ONLY AFTER scoring the prediction. Stream ordering is `(focal_toon, TRY_CAST(details_timeUTC AS TIMESTAMP), replay_id)` -- deterministic; same-timestamp ties broken by `replay_id`.

## 10. Metric Definitions + Bootstrap Policy (A21)

Log-loss uses sorted_then_kahan compensated summation (NIT-N6); Brier is the mean squared error of the predicted probability; calibration error is expected calibration error (ECE) over 10 equal-width bins. Bootstrap CIs: deterministic percentile with BOOTSTRAP_RANDOM_SEED=42, BOOTSTRAP_BLOCK_COUNT=200, NUMPY_RNG_BIT_GENERATOR=PCG64 (A21).

Sample probabilities (Row 2 batched-production path; first 5 PHA rows in stream-deterministic order; probability-only per NIT-N1 / A20):

| pha_row_index | predicted_probability |
|---|---|
| 0 | 0.500000 |
| 1 | 0.500000 |
| 2 | 0.500000 |
| 3 | 0.500000 |
| 4 | 0.500000 |

## 11. Per-Path Metric Table (Rows 1 & 2)

| Path | Log-loss (CI) | Brier (CI) | Calibration Error |
|---|---|---|---|
| event_by_event_reference | 0.6255 (0.6216--0.6302) | 0.2177 (0.2160--0.2197) | 0.0349 |
| batched_production_shape | 0.7048 (0.7021--0.7079) | 0.2527 (0.2517--0.2538) | 0.0412 |

CSV column count = 39 (per NIT-N3); row count = 5.

## 12. Q6G Selected Policy Binding Row (Row 5)

- selected_policy: `recommendation_only_glicko2`
- verdict: `recommendation_only_glicko2`
- materialization_permission: `recommendation_only_glicko2_event_by_event_validated_batched_path_unproven_or_unequivalent`

Rationale (verbatim from CSV notes column):

```
Q6G SELECTED POLICY = recommendation_only_glicko2
VERDICT = recommendation_only_glicko2
MATERIALIZATION PERMISSION = recommendation_only_glicko2_event_by_event_validated_batched_path_unproven_or_unequivalent
RATIONALE: Event-by-event Glicko-2 implementation validated against PR #247 section 11; batched-production path Spearman rho = 0.2292 or |Delta log-loss| = 0.079283 (SE = 0.002190) failed A19's equivalence criterion. Q6F's CI overlap (0.9% of mid-range) is not strong enough to bind a batched path that is not provably equivalent to the event path on this corpus.
DECISION RULE (verbatim from Q6G_PROOF_DECISION_RULE): BLOCKER-1 (A19) + byte-determinism jointly necessary for bind_now; equivalence fail -> recommendation_only_glicko2 (NIT-N2 default); determinism fail -> deferred_blocker.
Q5 BINDING preserved (sensitivity_indicator_co_registration); Q6F BINDING preserved (narrow_with_evidence); raw_mmr_hybrid rejection re-affirmed; no TrueSkill re-implementation (A5).
```

Decision rule:

```
Q6G PROOF DECISION RULE (BLOCKER-1; A19; NIT-N2 default)
========================================================

Let R3 = Row 3's equivalence_proof_statistics dict.
Let R4 = Row 4's byte_determinism_proof_statistics dict.

Equivalence pass = R3.passes_spearman_bound AND R3.passes_delta_log_loss_bound
                   (BLOCKER-1; A19; Spearman rho >= 0.99 AND
                    |Delta log-loss| <= SE_log_loss_event).
Determinism pass = R4.hashes_equal.

IF NOT Determinism pass:
    selected_policy = 'deferred_blocker'
    verdict = 'deferred_blocker'
    materialization_permission =
        'blocked_pending_byte_determinism_failure_investigation'
    rationale = 'Glicko-2 batched-production engine is not byte-deterministic
                 on two identical runs; this disqualifies any materialization
                 decision.'

ELIF NOT Equivalence pass:
    # NIT-N2 default expected outcome.
    selected_policy = 'recommendation_only_glicko2'
    verdict = 'recommendation_only_glicko2'
    materialization_permission =
        'recommendation_only_glicko2_event_by_event_validated_'
        'batched_path_unproven_or_unequivalent'
    rationale = ('Event-by-event Glicko-2 implementation validated against
                  PR #247 section 11; batched-production path
                  Spearman rho = {R3.spearman_rho:.4f} or
                  |Delta log-loss| = {R3.abs_delta_log_loss:.6f}
                  (SE = {R3.se_log_loss_event:.6f}) failed A19's equivalence
                  criterion. Q6F CI overlap (0.9% of mid-range) is not
                  strong enough to bind a batched path that is not
                  provably equivalent to the event path on this corpus.')

ELIF Equivalence pass AND Determinism pass:
    selected_policy = 'bind_now'
    verdict = 'bind_now'
    materialization_permission =
        'permitted_for_all_6_families_with_pinned_glicko2_'
        'batched_production_implementation_and_hyperparameters_'
        'in_next_materialization_pr'
    rationale = ('Glicko-2 batched-production implementation is
                  byte-deterministic AND ordering-equivalent to the
                  event-by-event reference (Spearman rho = {R3.spearman_rho:.4f}
                  >= 0.99; |Delta log-loss| = {R3.abs_delta_log_loss:.6f}
                  <= SE = {R3.se_log_loss_event:.6f}). Q6F section 11 metrics
                  now transfer to the production path.')

No other verdict branch is reachable from Row 5 in Q6G's auto-derived rule;
defer_to_two_candidate_implementation_comparison and
omit_reconstructed_rating_and_unblock_other_five are NOT auto-emitted. The
Layer-2 executor may override the auto-derived verdict ONLY by writing
substantive reasoning in the PR description AND obtaining reviewer-
adversarial sign-off; the override decision is OUT OF SCOPE for this planner.
```

## 13. Materialization Permission Statement

Materialization permission for Step 02_01_03 reconstructed_rating family: `recommendation_only_glicko2_event_by_event_validated_batched_path_unproven_or_unequivalent`.

Future feature materialization is a SEPARATE PR (Layer-3) and is subject to its own CROSS-02-01 post-materialization leakage audit. This Q6G proof does NOT substitute for that audit.

AUTHORITY (BINDING; A19): PR #247 section 11 metrics transfer to a batched-Glicko-2 `bind_now` ONLY IF A19's equivalence criterion passes (Spearman rho >= 0.99 AND |Delta log-loss| <= SE_log_loss_event). Without equivalence, the Q6F numbers do NOT certify the production path.

## 13a. Equivalence Proof Result (BLOCKER-1; A19)

- spearman_rho: `0.229228`
- abs_delta_log_loss: `0.079283`
- se_log_loss_event: `0.002190`
- passes_spearman_bound (>= 0.99): `False`
- passes_delta_log_loss_bound (<= SE): `False`

## 13b. Byte-Determinism Proof Result

- run_a_sha256: `71e5411024c01eb40018a5c7d0959db8162074e57e99bb5b8532cde247e75d8b`
- run_b_sha256: `71e5411024c01eb40018a5c7d0959db8162074e57e99bb5b8532cde247e75d8b`
- hashes_equal: `True`

## 14. Non-Substitution Statement

This artifact does NOT replace PR #242, PR #243, PR #245, or PR #247. It is a successor adjudication that emits a Q6G verdict; it does not retract any prior verdict. Layer-3 materialization is a SEPARATE PR, with its own CROSS-02-01 post-materialization leakage audit.

## 15. Limitations (NIT-N4)

- `toon_id` is region-scoped per Invariant #2 branch (iii); rating fragmentation across region-migrating players is an accepted Q6G bias. A future worldwide-identity PR (out of scope here) would address it separately.
- Cold-start gate (G-CS-4): the first PHA row for any toon_id contributes nothing to metric computation but is counted in `cold_start_rate`. Cold-start rows do NOT participate in the A19 equivalence proof.
- PHA decisive-only (PR #242 Q1): Glicko-2's draw-margin parameter is inapplicable.

## 16. Falsifier Roll-Call

```
parent_pr242_csv_sha256_mismatch:did_not_fire
parent_pr242_md_sha256_mismatch:did_not_fire
parent_pr243_csv_sha256_mismatch:did_not_fire
parent_pr243_md_sha256_mismatch:did_not_fire
parent_pr245_csv_sha256_mismatch:did_not_fire
parent_pr245_md_sha256_mismatch:did_not_fire
parent_pr247_csv_sha256_mismatch:did_not_fire
parent_pr247_md_sha256_mismatch:did_not_fire
q6g_batched_event_ordering_equivalence_unproven:did_not_fire
q6g_bind_now_emitted_without_equivalence_pass:did_not_fire
q6g_raw_mu_or_sigma_persisted_in_md:did_not_fire
q6g_decision_count_mismatch:did_not_fire
q6g_decision_id_order_mismatch:did_not_fire
q6g_q6g_selected_policy_row_missing:did_not_fire
q6g_byte_determinism_failed:did_not_fire
q6g_rating_trace_persistence_violation:did_not_fire
q6g_q5_re_adjudication_drift:did_not_fire
q6g_q6f_re_adjudication_drift:did_not_fire
q6g_no_trueskill_re_implementation:did_not_fire
q6g_rating_period_days_not_30:did_not_fire
q6g_bootstrap_seed_not_42:did_not_fire
q6g_bootstrap_block_count_not_200:did_not_fire
q6g_bootstrap_method_not_deterministic_percentile:did_not_fire
q6g_numpy_rng_not_pcg64:did_not_fire
q6g_python_summation_policy_not_sorted_then_kahan:did_not_fire
q6g_glicko2_iteration_tol_not_1e_6:did_not_fire
q6g_materialization_creep:did_not_fire
q6g_parquet_emitted:did_not_fire
q6g_status_drift:did_not_fire
q6g_research_log_drift:did_not_fire
q6g_roadmap_drift:did_not_fire
q6g_spec_drift:did_not_fire
q6g_cleaning_layer_drift:did_not_fire
q6g_target_match_outcome_read_as_input:did_not_fire
q6g_future_match_leakage_referenced:did_not_fire
q6g_global_batch_fit_referenced:did_not_fire
q6g_no_post_game_token:did_not_fire
q6g_phase_03_baseline_creep:did_not_fire
q6g_step_02_01_04_creep:did_not_fire
q6g_event_reference_not_imported_from_pr247:did_not_fire
```

## 17. SHA Provenance

- PR #242 CSV SHA256: `f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b`
- PR #242 MD  SHA256: `fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d`
- PR #243 CSV SHA256: `29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424`
- PR #243 MD  SHA256: `026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719`
- PR #245 CSV SHA256: `703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0`
- PR #245 MD  SHA256: `7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419`
- PR #247 CSV SHA256: `249e5591c6505b748fe3d371284a72d8f4620f57dbe9628c908ec2fbf097c8ed`
- PR #247 MD  SHA256: `4b49bee405bf87d4b8920b188e2c38d185ecc077b532d64a8bdd5a90cdf143f2`

## 18. No Step 02_01_03 Closure / No Phase 03 Start

This PR does NOT close Step 02_01_03; closure is reserved for a future Layer-3 materialization PR (or a separate omit-and-unblock closure PR if Q6G selects `omit_reconstructed_rating_and_unblock_other_five`). Phase 03 remains `not_started` and no baseline modelling is performed in this PR.

## 19. Citation Provenance

- Glickman (1999) -- Parameter estimation in large dynamic paired comparison experiments. Applied Statistics 48: 377-394.
- Glickman (2012) -- Example of the Glicko-2 system. Boston University Technical Note.
- Efron, Tibshirani (1993) -- An Introduction to the Bootstrap. Chapman & Hall. Source for the percentile bootstrap (NIT-N6).
- Higham (2002) -- Accuracy and Stability of Numerical Algorithms, 2nd ed. SIAM. Source for Kahan / Neumaier compensated summation (NIT-N6 PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY = sorted_then_kahan).

