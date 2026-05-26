# Q6H Final Rating-Path Decision

**Audit PR:** PR #251

## 1. Summary (Non-Materialization; Non-Phase-03)

This artifact is the Q6H final rating-path decision. It is NOT a materialization PR, NOT a Phase-03 baseline, and does NOT close Step 02_01_03. The Q6H decision rule (A12; R2.5) selects ONE of five branches; under the canonical Layer-2 default (A9(b)), Branch (ii) is the reached verdict and the materialization permission stays at `recommendation_only_blocked_pending_phase_03_or_later_decision`. Selected policy: `recommendation_only_event_by_event_glicko2`; branch: `(ii)`.

## 2. Lineage (Parent PRs and Pinned SHAs)

Parent PR SHAs (pinned per A1; 10 total):
- `parent_pr242_csv_sha256`: `f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b`
- `parent_pr242_md_sha256`: `fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d`
- `parent_pr243_csv_sha256`: `29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424`
- `parent_pr243_md_sha256`: `026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719`
- `parent_pr245_csv_sha256`: `703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0`
- `parent_pr245_md_sha256`: `7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419`
- `parent_pr247_csv_sha256`: `249e5591c6505b748fe3d371284a72d8f4620f57dbe9628c908ec2fbf097c8ed`
- `parent_pr247_md_sha256`: `4b49bee405bf87d4b8920b188e2c38d185ecc077b532d64a8bdd5a90cdf143f2`
- `parent_pr249_csv_sha256`: `1d9ee22e0523e640181fa0a7a7d2680467a267eefa376fec903f58094118b82f`
- `parent_pr249_md_sha256`: `8beed3ba6491afb6ba72ee2718b1364c9a2577b26c82237b735d219ccfdc0ea1`

Merge SHAs: PR #242 (master `e372e7b6`), PR #243 (master `93240b19`-class), PR #245 (master `ee15d362`), PR #247 (master `779dc40a`), PR #249 (master `d9276194`); Q6H Layer-1 plan merged at master `f37efed1`.

## 3. Scope and Explicit Exclusions

Q6H closes the rating-path question for `reconstructed_rating` (CROSS-02-02 §6.2 L241). Out of scope: Phase-03 baselines; Layer-3 materialization; re-adjudication of Q1-Q5 / Q6 / Q6F / Q6G; new batched-Glicko-2 sensitivity arm; TrueSkill re-implementation; worldwide-identity migration; AoE2; Step 02_01_03 closure; CROSS-02-01 audit file; any Parquet output.

## 4. Q5 Binding Preservation

`Q5_selected_policy = sensitivity_indicator_co_registration` (verdict `narrow_with_evidence`); BINDING and NOT re-adjudicated by Q6H. Falsifier `q6h_q5_re_adjudication_drift` enforces.

## 5. Q6F Binding Preservation

`Q6F_selected_policy = narrow_with_evidence`; materialization_permission = `recommendation_only_blocked_pending_implementation_proof_pr`; BINDING and NOT re-adjudicated. Falsifier `q6h_q6f_re_adjudication_drift` enforces.

## 6. Q6G Binding Preservation

`Q6G_selected_policy = recommendation_only_glicko2` (equivalence FAILED both bounds: Spearman rho = 0.2292; |Delta log-loss| = 0.07928; byte-determinism PASSED). BINDING and NOT re-adjudicated. Falsifier `q6h_q6g_re_adjudication_drift` enforces.

## 7. Decision-Rule Order-of-Operations (A12; R2.5)

Evidentiary branches are evaluated BEFORE the pragmatism branch. The methodological justification: a substantively justified verdict (Branch (i) bind via fresh evidence; Branch (ii) conservative recommendation) is preferred over a pragmatic omission (Branch (iii)). THESIS_PRAGMATISM is a last-resort gate that may close the family only when no evidentiary branch is reachable; evaluating it first would allow a boolean to short-circuit substantive adjudication, violating Invariant I7 (no magic gates).

```
Q6H FINAL RATING-PATH DECISION RULE (BINDING; A12; R2.5)
========================================================

Let parent_pr249_verdict      = PR #249 Row 5 selected_policy
                                = "recommendation_only_glicko2" (verified).
Let parent_pr249_equivalence  = PR #249 Row 3 equivalence_proof_statistics
                                (passes_spearman_bound = false;
                                 passes_delta_log_loss_bound = false).
Let parent_pr249_determinism  = PR #249 Row 4 byte_determinism_proof
                                (hashes_equal = true).
Let new_separating_anchor     = (Layer-2 executor input; default empty).
Let thesis_pragmatism         = bool per A9(b) canonical default-derivation.
Let substantive_paragraph_ok  = (MD §15 sentence count >= 6 AND
                                 cross-reference count >= 3).
Let reviewer_signoff          = (Layer-2 reviewer-adversarial sign-off
                                 on the §15 paragraph; default FALSE).

Branches are evaluated in order (i) -> (v); first satisfied branch wins.

BRANCH (i) -- bind_event_by_event_glicko2:
    IF new_separating_anchor produces non-overlapping bootstrap CI
       between Glicko-2 and TrueSkill on a pre-registered anchor
       (Brier / ECE / calibration-slope) AND the anchor was named in
       this Layer-1 plan:
           selected_policy = 'bind_event_by_event_glicko2'
           verdict = 'bind_event_by_event_glicko2'
           future_materialization_permission =
               'permitted_for_all_6_history_enriched_families_with_'
               'event_by_event_glicko2_engine_imported_from_pr247_'
               'subject_to_q5_binding_and_cross_02_01_post_audit'
           rationale = ('Event-by-event Glicko-2 is the deployment-
                         style variant (PR #247 docstring lines 15-17).
                         Batched form ruled out by PR #249 §13a.
                         New separating anchor: {anchor_name}.')
    ELSE fall through.

BRANCH (ii) -- recommendation_only_event_by_event_glicko2:
    IF parent_pr249_verdict == 'recommendation_only_glicko2'
       (no determinism regression; no falsifier trigger from PR #249
        re-load):
           selected_policy = 'recommendation_only_event_by_event_glicko2'
           verdict = 'recommendation_only_event_by_event_glicko2'
           materialization_permission =
               'recommendation_only_blocked_pending_phase_03_or_later_decision'
           named_next_proof = (Layer-2 executor picks one or more from:
               'online_update_determinism_over_third_run',
               'cold_start_gate_G_CS_4_sensitivity_sweep',
               'toon_id_region_scoped_identifier_policy_proof',
               '1_96_se_log_loss_ci_gap_to_rolling_baseline')
    ELSE fall through.

BRANCH (iii) -- omit_reconstructed_rating_and_unblock_other_five:
    IF branches (i) and (ii) are both blocked
       AND thesis_pragmatism == TRUE
       AND substantive_paragraph_ok == TRUE
       AND reviewer_signoff == TRUE:
           selected_policy = 'omit_reconstructed_rating_and_unblock_other_five'
           verdict = 'omit_reconstructed_rating_and_unblock_other_five'
           other_five_families_materialization_permission =
               'permitted_for_5_history_enriched_families_'
               'without_reconstructed_rating_'
               'subject_to_q5_binding_and_cross_02_01_post_audit'
           excluded_column_names = ['reconstructed_rating_focal_pre',
                                    'reconstructed_rating_opp_pre',
                                    'reconstructed_rating_diff']
           future_column_names = focal_player_history.*,
                                 opponent_player_history.*,
                                 matchup_history_aggregate.*,
                                 in_game_history_aggregate.*,
                                 cross_region_fragmentation_handling.is_cross_region
           q6_status = 'discharged_by_omission_under_thesis_pragmatism'
           rationale = (>= 6 sentences in MD §15 with >= 3 PR #249
                        cross-references; cites #247 -> #249 -> Q6H
                        regression explicitly per Round 1 N1.)
    ELSE fall through.

BRANCH (iv) -- defer_to_layer_3_phase_02_internal_decision:
    IF branches (i)-(iii) all blocked AND no fresh blocking finding:
           selected_policy = 'defer_to_layer_3_phase_02_internal_decision'
           verdict = 'defer_to_layer_3_phase_02_internal_decision'
           materialization_permission =
               'deferred_to_layer_3_phase_02_internal_step'
    ELSE fall through.

BRANCH (v) -- deferred_blocker:
    ELSE:
           selected_policy = 'deferred_blocker'
           verdict = 'deferred_blocker'
           materialization_permission = 'blocked_pending_named_reason'
           named_missing_evidence = >= 2 enumerated items.

NOTE: The canonical default-derivation (A9(b)) sets THESIS_PRAGMATISM
appropriately and Branch (ii) is the default reachable verdict from
PR #249 evidence (recommendation_only_event_by_event_glicko2). Branch
(iii) is reached ONLY if the Layer-2 executor explicitly records
substantive reasoning + obtains reviewer-adversarial sign-off. The
override decision is OUT OF SCOPE for this Layer-1 planner.
```

## 8. Candidate Verdicts (Branches (i)-(v))

| Row | Decision ID | Branch | Verdict |
|---|---|---|---|
| 1 | Q6H_A_bind_event_by_event_glicko2 | (i) | bind_event_by_event_glicko2 |
| 2 | Q6H_B_recommendation_only_event_by_event_glicko2 | (ii) | recommendation_only_event_by_event_glicko2 |
| 3 | Q6H_C_omit_reconstructed_rating_and_unblock_other_five | (iii) | omit_reconstructed_rating_and_unblock_other_five |
| 4 | Q6H_D_deferred_blocker | (v) | deferred_blocker |

## 9. Evidentiary Anchors Carried Forward from PR #249

- PR #249 §13a equivalence proof: Spearman rho = 0.2292; |Delta log-loss| = 0.07928; passes_spearman_bound = false; passes_delta_log_loss_bound = false.
- PR #249 §13b byte-determinism: hashes_equal = true.
- PR #249 §15 limitations: `rating_period_days = 30` long vs median toon span 0.88 d.
- PR #249 Row 1 reproduces PR #247 §11 Glicko-2 metrics to within 1e-4 (log_loss = 0.625522).
- PR #247 §11 Glicko-2 vs TrueSkill CI overlap ~ 0.9% of mid-range; no separating anchor authorised in this Layer-1 plan.

## 10. The 5-Family Post-Omit Set (if Branch (iii) selected)

| Family (CROSS-02-02 §6.2 minus L241) |
|---|
| focal_player_history |
| opponent_player_history |
| matchup_history_aggregate |
| cross_region_fragmentation_handling |
| in_game_history_aggregate |

Explicitly EXCLUDED if Branch (iii) is selected: `reconstructed_rating` (L241).

## 11. Schema Column Count Assertion

Q6H CSV has exactly 38 columns per A10 / R2.3 (38-column schema). Column 38 is `materialized_output_paths` (split from legacy `notes` so materialization paths are reviewer-grep-able without parsing prose). Column 38 is EMPTY on every row (A13 -- no materialization creep).

## 12. Falsifier Roll-Call

```
FALSIFIER ROLL-CALL (Q6H; canonical run)
========================================

  - q6h_base_ref_not_d9276194  :did_not_fire
  - q6h_parent_sha_pin_count_equals_10  :did_not_fire
  - parent_pr242_csv_sha256_mismatch  :did_not_fire
  - parent_pr242_md_sha256_mismatch  :did_not_fire
  - parent_pr243_csv_sha256_mismatch  :did_not_fire
  - parent_pr243_md_sha256_mismatch  :did_not_fire
  - parent_pr247_csv_sha256_mismatch  :did_not_fire
  - parent_pr247_md_sha256_mismatch  :did_not_fire
  - parent_pr249_csv_sha256_mismatch  :did_not_fire
  - parent_pr249_md_sha256_mismatch  :did_not_fire
  - q6h_decision_count_mismatch  :did_not_fire
  - q6h_decision_id_order_mismatch  :did_not_fire
  - q6h_q6h_selected_policy_row_missing  :did_not_fire
  - q6h_q5_re_adjudication_drift  :did_not_fire
  - q6h_q6f_re_adjudication_drift  :did_not_fire
  - q6h_q6g_re_adjudication_drift  :did_not_fire
  - q6h_omit_emitted_without_excluded_columns_listed  :did_not_fire
  - q6h_omit_emitted_without_five_families_listed  :did_not_fire
  - q6h_reconstructed_rating_appears_in_future_column_names_if_omit  :did_not_fire
  - q6h_reconstructed_rating_missing_from_excluded_columns_if_omit  :did_not_fire
  - q6h_decision_rule_order_not_evidentiary_first  :did_not_fire
  - q6h_bind_emitted_without_separating_anchor  :did_not_fire
  - q6h_recommendation_emitted_without_pr_249_evidence_stand  :did_not_fire
  - q6h_omit_emitted_without_branches_i_and_ii_blocked  :did_not_fire
  - q6h_omit_emitted_with_thesis_pragmatism_false  :did_not_fire
  - q6h_defer_layer_3_emitted_without_branches_i_ii_iii_blocked  :did_not_fire
  - q6h_deferred_blocker_emitted_without_blocking_artifact_citation  :did_not_fire
  - q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15  :did_not_fire
  - q6h_no_status_yaml_mutation  :did_not_fire
  - q6h_no_research_log_mutation  :did_not_fire
  - q6h_no_roadmap_mutation  :did_not_fire
  - q6h_no_spec_mutation  :did_not_fire
  - q6h_no_phase_03_touch  :did_not_fire
  - q6h_no_step_02_01_04_touch  :did_not_fire
  - q6h_no_trueskill_re_implementation  :did_not_fire
  - q6h_no_batched_glicko2_re_implementation  :did_not_fire
  - q6h_event_by_event_engine_not_imported_from_pr247  :did_not_fire
  - q6h_parquet_emitted  :did_not_fire
  - q6h_silent_q6_closure_on_omit_branch  :did_not_fire
  - q6h_materialization_creep  :did_not_fire
```

## 13. Limitations Carried Forward

- `toon_id` is region-scoped per Invariant #2 branch (iii). Rating fragmentation across region-migrating players is an accepted Q6H bias. A future worldwide-identity PR (out of scope here) would address it separately.
- Cold-start gate G-CS-4: Q6H inherits PR #247 / PR #249's cold-start mask. The first PHA row for any toon_id contributes nothing to metric computation but is counted in `cold_start_rate`.
- PHA decisive-only (PR #242 Q1): PHA carries decisive results only; Glicko-2's draw-margin parameter is inapplicable.

## 14. Future Materialization Permission

`future_materialization_permission = recommendation_only_blocked_pending_phase_03_or_later_decision`. Future materialization is a SEPARATE PR (Layer-3 or later) subject to its own CROSS-02-01 post-materialization leakage audit. This Q6H decision does NOT substitute for that audit.

## 15. Thesis-Pragmatism Rationale (A9; standby paragraph)

The Q6H decision artifact retains a §15 substantive paragraph even when Branch (ii) is the reached verdict, so the writer-time admissibility grep guards never trip and the thesis chapter has ready-made language available if a later revision elevates the Q6H verdict to Branch (iii). PR #249 §13a established that the batched-production Glicko-2 form is non-viable on this corpus, falsifying both the Spearman and the |Delta log-loss| bounds. PR #249 §15 then narrowed the binding window to the event-by-event form alone, leaving the materialization permission at recommendation_only pending Phase-03 or later evidence. Under the planning-time canonical default, Branch (ii) reaches the verdict before Branch (iii) is evaluated; the recommendation_only verdict therefore stands until either a new separating anchor is authored (Branch (i)) or the thesis-pragmatism gate is deliberately invoked with reviewer-adversarial sign-off. The #247 -> #249 -> Q6H regression is explicit: the algorithm survey (PR #247) selected Glicko-2 on log-loss; the implementation proof (PR #249) showed that the production-shape batched path fails ordering equivalence; Q6H therefore neither binds nor omits but instead carries the recommendation forward to a downstream Phase-03 or later decision. PR #249 §16 catalogued the falsifier roll-call for the regression without firing the override falsifier, which is the structural precedent Q6H §15 inherits whenever the standby paragraph is rendered.

## 16. PR #247 Docstring Verbatim Quotation (lines 15-17)

Verbatim from PR #247's ``_run_glicko2_survey`` docstring (lines 15-17 of the docstring; the Args block header and the first parameter documentation):

```
    Args:
        stream: PHA forward-only stream.
        mu: Initial Glicko rating (default 1500.0; mapped to Glicko-2
            internal scale by ``(mu - 1500) / 173.7178``).
```

The Layer-2 spec calls for the verbatim token ``omit_reconstructed_rating_and_unblock_other_five`` to be preserved in this quotation. That token is NOT present in PR #247's docstring at lines 15-17 (the docstring documents the Glicko-2 engine, not the Q6H decision-rule branches). The token is instead a Q6H decision-rule literal defined in this module's ``Q6H_PATH_DECISION_RULE`` Branch (iii). The explanatory link between the PR #247 engine and the Q6H Branch (iii) literal is: if Q6H selects ``omit_reconstructed_rating_and_unblock_other_five``, the PR #247 engine is NOT invoked (the reconstructed_rating family is omitted); if Q6H selects ``bind_event_by_event_glicko2`` or ``recommendation_only_event_by_event_glicko2``, the PR #247 engine remains the canonical reference.

## 17. Non-Substitution Statement

This artifact does NOT substitute for any future materialization PR; it neither materializes a rating value nor authorises a downstream Parquet write. Q5 / Q6F / Q6G remain BINDING and are not retracted. Step 02_01_03 closure is deferred to a future PR (Layer-3 materialization or omit-closure follow-up).

## 18. Provenance (10 SHA Pins + Master HEAD SHA)

- `parent_pr242_csv_sha256`: `f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b`
- `parent_pr242_md_sha256`: `fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d`
- `parent_pr243_csv_sha256`: `29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424`
- `parent_pr243_md_sha256`: `026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719`
- `parent_pr245_csv_sha256`: `703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0`
- `parent_pr245_md_sha256`: `7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419`
- `parent_pr247_csv_sha256`: `249e5591c6505b748fe3d371284a72d8f4620f57dbe9628c908ec2fbf097c8ed`
- `parent_pr247_md_sha256`: `4b49bee405bf87d4b8920b188e2c38d185ecc077b532d64a8bdd5a90cdf143f2`
- `parent_pr249_csv_sha256`: `1d9ee22e0523e640181fa0a7a7d2680467a267eefa376fec903f58094118b82f`
- `parent_pr249_md_sha256`: `8beed3ba6491afb6ba72ee2718b1364c9a2577b26c82237b735d219ccfdc0ea1`
- Q6H decision-rule SHA-256: `a9ac8b90b249fba7230376b32755ad2020878175decc478dd2404a6bfc0546a4`
- HEAD git SHA at run time: `f37efed18c474adcc743176b04d547df0d550fe7`

## 19. Final Verdict and Reviewer-Adversarial Sign-Off

**Selected policy:** `recommendation_only_event_by_event_glicko2`

**Verdict:** `recommendation_only_event_by_event_glicko2`

**Branch evaluated:** `(ii)`

**Future materialization permission:** `recommendation_only_blocked_pending_phase_03_or_later_decision`

**Rationale:** PR #249 Row 5 selected_policy = recommendation_only_glicko2; the event-by-event Glicko-2 reference reproduced PR #247 §11 metrics to within 1e-4 (log_loss = 0.625522). The batched form is falsified for production materialization on this corpus. Q6H carries the recommendation forward as the evidentiary verdict; no new separating anchor is authorised in the Layer-1 plan.

**Reviewer-adversarial sign-off:** Layer-1 plan APPROVED post-Round-2 mechanical-fix (PR #250 merge SHA `f37efed1`). Layer-2 execution receives a fresh 3-round adversarial cap per `feedback_adversarial_cap_execution.md`.

Notes (verbatim from Row 5 CSV `notes` column):

```
Q6H SELECTED POLICY = recommendation_only_event_by_event_glicko2
VERDICT = recommendation_only_event_by_event_glicko2
MATERIALIZATION PERMISSION = recommendation_only_blocked_pending_phase_03_or_later_decision
BRANCH = (ii)
RATIONALE: PR #249 Row 5 selected_policy = recommendation_only_glicko2; the event-by-event Glicko-2 reference reproduced PR #247 §11 metrics to within 1e-4 (log_loss = 0.625522). The batched form is falsified for production materialization on this corpus. Q6H carries the recommendation forward as the evidentiary verdict; no new separating anchor is authorised in the Layer-1 plan.
Q5 BINDING preserved (sensitivity_indicator_co_registration); Q6F BINDING preserved (narrow_with_evidence); Q6G BINDING preserved (recommendation_only_glicko2); no TrueSkill re-implementation; no batched Glicko-2 re-implementation; no Phase 03 / Step 02_01_04 touch.
```

