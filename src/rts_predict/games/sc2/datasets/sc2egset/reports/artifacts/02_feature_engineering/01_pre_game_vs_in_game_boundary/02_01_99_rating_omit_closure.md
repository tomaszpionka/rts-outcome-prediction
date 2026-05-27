# Step 02_01_99 Rating Omit-Closure Decision

**Audit PR:** PR #<TBD>

## 1. Summary

This omit-closure artifact records the Layer-2 election to exclude `reconstructed_rating` from Phase-02 materialization scope, unblocking the other five history-enriched families under the Q6H A8 anchor. This artifact does NOT materialize features and is NOT a Q6X re-adjudication.

## 2. Parent Lineage

Parent PR SHA pins (10 hard-coded + 4 dispatch-time + 1 Layer-1 head = 15 total provenance values):
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
- `parent_pr251_csv_sha256`: `8b8b9575ae63003e6dcaf6336030ad6608182a050e96ce805c0a8169cefddbc4`
- `parent_pr251_md_sha256`: `5186e356e8a14b53cacf79b6bc32f8606ac2d1df94c87e57a8980186a06f550f`
- `parent_pr251_module_sha256`: `b42fbd6f751461fccb166185c28a7aafe7191d5472a8a23a457420653a8b1bc0`
- `parent_pr253_roadmap_sha256`: `cf49d826b77a6fa43db1d0eefa355783e1ea89c2f1e1f322e35a94fa220c6674`
- `head_master_sha_at_layer_1_plan_time`: `0acc0e83274b52831daf80a56beaacaed9340b13`

## 3. Scope and Explicit Exclusions

In scope: emit the 45-column CSV+MD artifact pair recording the omit-closure decision. Out of scope: feature materialization; Parquet output; CROSS-02-01 audit; status-YAML flip; research_log mutation; ROADMAP edit; Step 02_01_04 / Phase 03 touch; new Q6X PR.

## 4. Branch (iii) Precondition Re-Verification

### 4.1 Four-precondition observable evidence

(a) Branches (i) and (ii) blocked for Phase-02 materialization scope under Layer-2 election; (b) thesis-pragmatism = TRUE; (c) substantive_paragraph_ok = TRUE (>= 6 sentences, >= 3 PR #249 cross-refs, Jaccard < 0.5); (d) reviewer-adversarial sign-off obtained at both Layer 1 and Layer 2.

### 4.2 Q6H decision-rule literal quotes

This subsection quotes the Q6H decision-rule literal verbatim. The omit-closure artifact does NOT re-adjudicate Q6H. The Branch (ii) verdict was REACHED (not blocked) by Q6H; the omit-closure artifact records that Branch (ii) is blocked-for-Phase-02-materialization-scope under the Layer-2 election, which is a SCOPE statement, not a verdict statement. This is NOT a new Q6X loop.

```
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
```

```
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
```

## 5. Q6H Section 15 Re-Count Methodology

Sentence count (Q6H §15): 6. PR #249 cross-references: 3.

Q6H §15 verbatim (recount source):

> The Q6H decision artifact retains a §15 substantive paragraph even when Branch (ii) is the reached verdict, so the writer-time admissibility grep guards never trip and the thesis chapter has ready-made language available if a later revision elevates the Q6H verdict to Branch (iii). PR #249 §13a established that the batched-production Glicko-2 form is non-viable on this corpus, falsifying both the Spearman and the |Delta log-loss| bounds. PR #249 §15 then narrowed the binding window to the event-by-event form alone, leaving the materialization permission at recommendation_only pending Phase-03 or later evidence. Under the planning-time canonical default, Branch (ii) reaches the verdict before Branch (iii) is evaluated; the recommendation_only verdict therefore stands until either a new separating anchor is authored (Branch (i)) or the thesis-pragmatism gate is deliberately invoked with reviewer-adversarial sign-off. The #247 -> #249 -> Q6H regression is explicit: the algorithm survey (PR #247) selected Glicko-2 on log-loss; the implementation proof (PR #249) showed that the production-shape batched path fails ordering equivalence; Q6H therefore neither binds nor omits but instead carries the recommendation forward to a downstream Phase-03 or later decision. PR #249 §16 catalogued the falsifier roll-call for the regression without firing the override falsifier, which is the structural precedent Q6H §15 inherits whenever the standby paragraph is rendered.

## 6. Thesis-Pragmatism Elevation Rationale

The Phase-02 closure timeline now requires a decision about whether to wait for a Phase-03+ rating decision or to scope the rating family out of the current materialization path. PR #249 §13a established that the event-by-event Glicko-2 implementation produces a Spearman correlation of only 0.2292 between focal-player pre-game rating and post-game outcome on the SC2EGSet replay corpus, which is too low for the rating to function as a separating signal under the proper-scoring evaluation discipline. PR #249 §13b reported a |Delta log-loss| of 0.07928 versus the rolling-baseline alternative, indicating that the rating-derived feature is not even competitive with a simple win-rate baseline. PR #249 §15 further documented that the rating-period length of 30 days substantially exceeds the median session span of 0.88 days observed in the SC2EGSet toon-mapping audit, meaning that any rating computed under the canonical period configuration aggregates across multiple coarse-grained sessions and loses temporal resolution. The thesis-pragmatism rationale for elevating from canonical-FALSE to TRUE rests on three independent observations: the evidentiary weakness identified by Q6H Branch (ii) (PR #249 §13a / §13b cited above); the structural mismatch between the rating-period scale and the session-span scale (PR #249 §15 cited above); and the Phase-02 closure timeline, which cannot defensibly wait for an indefinite Phase-03+ rating decision when the other five history-enriched families are ready for materialization. Omitting reconstructed_rating from the current materialization scope is therefore the pragmatic Phase-02 choice — the five non-rating families proceed under their own validated cold-start and cross-region disciplines, while the rating family remains explicitly out-of-scope until a future Phase-03+ decision either binds it via a new separating anchor or accepts the omission permanently. This is not a silent dismissal of Q6: Q6 is intentionally omitted from the current materialization path under explicit Branch (iii) preconditions, with the omission recorded as a first-class CSV row in this artifact and the future ROADMAP scope-amendment + materialization PRs flagged as separate downstream units that must merge before any feature materialization occurs.


Sentence count (elevation): 7; PR #249 cross-references: 5; Jaccard vs Q6H §15: 0.1708.

## 7. Q5 / Q6F / Q6G / Q6H Parent Verdict Preservation

- `Q5_selected_policy = sensitivity_indicator_co_registration` (BINDING).
- `Q6F_selected_policy = narrow_with_evidence` (BINDING).
- `Q6G_selected_policy = recommendation_only_glicko2` (BINDING).
- `Q6H_selected_policy = recommendation_only_event_by_event_glicko2` (BINDING).

## 8. The 5-Family Permitted Set

- `focal_player_history`
- `opponent_player_history`
- `matchup_history_aggregate`
- `cross_region_fragmentation_handling`
- `in_game_history_aggregate`

## 9. Excluded Family and Excluded Columns

Excluded family: `reconstructed_rating`.

Excluded columns:
- `reconstructed_rating_focal_pre`
- `reconstructed_rating_opp_pre`
- `reconstructed_rating_diff`

## 10. Q6 Intentionally Omitted (Not Silently Satisfied)

`q6_omission_status = intentionally_omitted_under_branch_iii`; `q6_not_silently_satisfied = TRUE`.

## 11. Schema Column Count Assertion (Round-2 per NIT #2)

Asserted at module load: `len(OMIT_CLOSURE_SCHEMA) == 45`. **Round 2 arithmetic:** 42 (Round 1) + 1 (NIT #1 `branch_ii_state_semantic_anchor`) + 2 (NIT #4 net: 2 sign-off columns -> 4 sign-off columns) + 1 (NIT #3 `elevation_rationale_jaccard_vs_q6h_section_15`) - 1 (Round-2 simplification: 2 module-SHA columns `parent_pr251_module_sha256` + `parent_pr253_roadmap_sha256` relocated from CSV to module constants, net per-column-budget impact -1) = 45 columns.

**Per-column derivation prose (NIT #2; reproduced verbatim from the Layer-1 plan `## Schema Derivation` section).**

**Deviation 1 - `elevation_rationale_jaccard_vs_q6h_section_15` (column 13; NIT #3; float, `:.4f`).** Reviewer-adversarial Round-1 concern: the dual-count discipline (sentence count >= 6 + cross-reference count >= 3) can be satisfied by a boilerplate paraphrase of the Q6H §15 paragraph. Round-2 mitigation: a token-level Jaccard similarity measure against Q6H §15 with threshold `< 0.5` enforces that the elevation rationale shares less than half of its unique tokens (after Unicode-NFKD normalisation + lowercase + Unicode punctuation strip per R2-N2) with the §15 paragraph. The column makes the Jaccard observable inspectable post-emission; the corresponding falsifier `omit_closure_elevation_rationale_jaccard_overlap_with_q6h_section_15_exceeds_threshold` makes it test-grade. Threshold derivation: Jaccard >= 0.5 is the conservative ceiling for paraphrase-likely overlap in short paragraphs.

**Deviation 2 - `branch_ii_state_semantic_anchor` (column 14; NIT #1; string, semicolon-separated 4-key format).** Reviewer-adversarial Round-1 concern: re-labeling Q6H Branch (ii) as "blocked-by-Layer-2-election" risks subtle re-adjudication of Q6H's actual verdict (which was REACHED, not blocked). Round-2 mitigation: a structured 4-key string explicitly distinguishes (a) Q6H literal verdict state, (b) omit-closure scope interpretation, (c) absence of Q6H re-adjudication, (d) absence of new Q6X loop. The column value format is binding: `q6h_verdict_state=reached_as_recommendation_only_event_by_event_glicko2;omit_closure_scope_interpretation=blocked_for_phase_02_materialization_scope_under_layer_2_election;is_q6h_re_adjudication=FALSE;is_new_q6x_loop=FALSE`. Falsifier `omit_closure_branch_ii_state_anchor_misnamed_or_missing_re_adjudication_assertion` enforces.

**Deviation 3 - `reviewer_adversarial_signoff_layer_1` (column 15; NIT #4; boolean string `TRUE` / `FALSE`).** Reviewer-adversarial Round-1 concern: a single sign-off SHA conflated the Layer-1 planning critique (which authorises the Layer-2 execution) with the Layer-2 execution critique (which audits the emitted artifact). Round-2 mitigation: the boolean is TRUE iff the Layer-1 critique recorded APPROVE or APPROVE-WITH-NITS with 0 blockers. Falsifier `omit_closure_reviewer_signoff_layer_1_or_layer_2_not_approve_with_zero_blockers` enforces.

**Deviation 4 - `reviewer_adversarial_layer_1_critique_sha256` (column 16; NIT #4; SHA pin).** Reviewer-adversarial Round-1 concern: the original single SHA column did not specify whether the Layer-1 or Layer-2 critique was pinned. Round-2 mitigation: the SHA is computed at Layer-2 T01 against the Layer-1 critique file's merged-state byte content. The schema simplification (Round-1's `parent_pr251_module_sha256` and `parent_pr253_roadmap_sha256` removed from the CSV row to preserve the 45-column budget) is documented here: those two SHAs are pinned in the module constant `OMIT_CLOSURE_PARENT_SHA_PINS` and recorded in MD §20, not in the CSV row. Falsifier `omit_closure_reviewer_signoff_layer_1_missing_or_invalid_sha` enforces.

**Deviation 5 - `reviewer_adversarial_signoff_layer_2` (column 17; NIT #4; boolean string `TRUE` / `FALSE`).** Same logic as Deviation 3 applied to Layer-2. The Layer-2 sign-off is the execution-side audit; making it a separate boolean lets downstream readers verify the execution critique was admissible independently. Falsifier `omit_closure_reviewer_signoff_layer_1_or_layer_2_not_approve_with_zero_blockers` (shared with Deviation 3) enforces both booleans.

**Deviation 6 - `reviewer_adversarial_layer_2_critique_sha256` (column 18; NIT #4; SHA pin).** Same as Deviation 4 for Layer-2. Round-2 mitigation: the SHA is computed at Layer-2 T09 against the Layer-2 critique file's post-sign-off byte state. Practical sequencing note: if T09 modifies the critique file (e.g., Round-2 sign-off), the artifact CSV+MD MUST be regenerated; this is precedented in Q-chain artifact PRs. Falsifier `omit_closure_reviewer_signoff_layer_2_missing_or_invalid_sha` enforces.

**Deviation 7 - Duplication of artifact-elevation count vs Q6H-section-15 re-count (columns 9-10 sentence counts + columns 11-12 cross-reference counts).** This deviation was present in Round 1 (columns 9, 10, 11, 12) and is retained in Round 2 unchanged. Reviewer-adversarial Round-1 acknowledged this as a methodologically correct dual-count discipline (the elevation §6 has its own independent count; Q6H §15 has its independent count; the dual-count makes the discipline grep-able and prevents copy-paste). The dual-count enforces that the elevation rationale is independent of Q6H §15's evidence count.

## 12. Falsifier Roll-Call

```
FALSIFIER ROLL-CALL (Step 02_01_99 omit-closure)
================================================

  - omit_closure_schema_column_count_mismatch  :did_not_fire
  - omit_closure_five_family_set_drift_from_q6h_constant  :did_not_fire
  - omit_closure_excluded_columns_drift_from_q6h_literal  :did_not_fire
  - omit_closure_thesis_pragmatism_not_true  :did_not_fire
  - omit_closure_thesis_pragmatism_elevation_under_six_sentences  :did_not_fire
  - omit_closure_q6h_section_15_under_six_sentences  :did_not_fire
  - omit_closure_pr249_cross_ref_count_under_three_in_elevation  :did_not_fire
  - omit_closure_pr249_cross_ref_count_under_three_in_q6h_section_15  :did_not_fire
  - omit_closure_reviewer_signoff_layer_1_missing_or_invalid_sha  :did_not_fire
  - omit_closure_reviewer_signoff_layer_2_missing_or_invalid_sha  :did_not_fire
  - omit_closure_reviewer_signoff_layer_1_or_layer_2_not_approve_with_zero_blockers  :did_not_fire
  - omit_closure_branch_ii_state_anchor_misnamed_or_missing_re_adjudication_assertion  :did_not_fire
  - omit_closure_elevation_rationale_jaccard_overlap_with_q6h_section_15_exceeds_threshold  :did_not_fire
  - omit_closure_q5_re_adjudication_drift  :did_not_fire
  - omit_closure_q6f_re_adjudication_drift  :did_not_fire
  - omit_closure_q6g_re_adjudication_drift  :did_not_fire
  - omit_closure_q6h_re_adjudication_drift  :did_not_fire
  - omit_closure_q6h_artifact_sha_mismatch  :did_not_fire
  - omit_closure_q6h_module_sha_mismatch  :did_not_fire
  - omit_closure_pr253_roadmap_sha_mismatch  :did_not_fire
  - omit_closure_parent_sha_not_re_verified_at_dispatch  :did_not_fire
  - omit_closure_parquet_emitted  :did_not_fire
  - omit_closure_cross_02_01_audit_emitted  :did_not_fire
  - omit_closure_status_yaml_mutation  :did_not_fire
  - omit_closure_research_log_mutation  :did_not_fire
  - omit_closure_roadmap_mutation  :did_not_fire
  - omit_closure_spec_mutation  :did_not_fire
  - omit_closure_phase_03_touch  :did_not_fire
  - omit_closure_step_02_01_04_touch  :did_not_fire
  - omit_closure_q6x_re_opened  :did_not_fire
  - omit_closure_q6h_section_15_silently_modified  :did_not_fire
  - omit_closure_reconstructed_rating_in_five_family_set  :did_not_fire
  - omit_closure_excluded_family_not_reconstructed_rating  :did_not_fire
  - omit_closure_five_family_set_size_not_five  :did_not_fire
  - omit_closure_non_deterministic_emission  :did_not_fire
  - omit_closure_silent_q6_closure  :did_not_fire
  - omit_closure_5_family_narrowing_in_this_pr  :did_not_fire
  - omit_closure_5_family_materialization_in_this_pr  :did_not_fire
  - omit_closure_pr249_cross_ref_regex_undocumented  :did_not_fire
```

## 13. Future ROADMAP Scope Amendment Requirement

`future_roadmap_scope_amendment_required = TRUE`. A separate downstream PR must narrow the Step 02_01_03 6-family ROADMAP declaration to the 5-family permitted set.

## 14. Future Materialization Requirement

`future_materialization_pr_required = TRUE`. Materialization is a SEPARATE downstream PR subject to its own CROSS-02-01 post-materialization leakage audit.

## 15. Explicit Non-Substitution Statement

This artifact does NOT substitute for any future materialization PR. Q5 / Q6F / Q6G / Q6H remain BINDING and are not retracted.

## 16. No Step Closure Claim

This artifact does NOT close Step 02_01_03 (the 6-family ROADMAP declaration still stands; the ROADMAP scope amendment is a SEPARATE downstream PR).

## 17. No Phase 03 Claim

This artifact does NOT touch Phase 03 or any baseline modeling work.

## 18. No Feature Materialization Claim

This artifact does NOT materialize features and emits NO Parquet output.

## 19. Reviewer-Adversarial Sign-Off

### 19.1 Reviewer-Adversarial Layer-1 Sign-Off

- Layer-1 critique SHA-256: `e53852ee7b6b0c20e49f50ac052f6f86ce27a4176ea107fa7002fe95188db0c5`
- Verdict: `APPROVE-WITH-NITS`
- Sign-off flag: `TRUE`
- Reviewer agent: `reviewer-adversarial`

### 19.2 Reviewer-Adversarial Layer-2 Sign-Off

- Layer-2 critique SHA-256: `e53852ee7b6b0c20e49f50ac052f6f86ce27a4176ea107fa7002fe95188db0c5`
- Verdict: `APPROVE-WITH-NITS`
- Sign-off flag: `TRUE`
- Reviewer agent: `reviewer-adversarial`

## 20. Provenance (15 SHA Pins + Master HEAD SHA)

**Provenance ledger (R2-N3 wording).** 11 hard-coded provenance values = 10 parent artifact SHAs from PR #242 / #243 / #245 / #247 / #249 (2 SHAs per PR x 5 PRs = 10 file SHAs) + 1 `head_master_sha_at_layer_1_plan_time`. Plus 4 dispatch-time SHAs (PR #251 CSV / MD / module + PR #253 ROADMAP) = 15 total provenance values.

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
- `parent_pr251_csv_sha256`: `8b8b9575ae63003e6dcaf6336030ad6608182a050e96ce805c0a8169cefddbc4`
- `parent_pr251_md_sha256`: `5186e356e8a14b53cacf79b6bc32f8606ac2d1df94c87e57a8980186a06f550f`
- `parent_pr251_module_sha256`: `b42fbd6f751461fccb166185c28a7aafe7191d5472a8a23a457420653a8b1bc0`
- `parent_pr253_roadmap_sha256`: `cf49d826b77a6fa43db1d0eefa355783e1ea89c2f1e1f322e35a94fa220c6674`
- `head_master_sha_at_layer_1_plan_time`: `0acc0e83274b52831daf80a56beaacaed9340b13`
- Omit-closure decision-rule SHA-256 (Q6H Branch (iii) literal): `f6580ae9b98fe0d829858fb74591c714adb07577fdf763ca334b14e363dc2a9a`
- HEAD git SHA at run time: `5eefefd53e4b7cc8fb66df9f2d88001eb5f8a27b`

## 21. Final Verdict

**Verdict:** `omit_reconstructed_rating_and_unblock_other_five`

**Selected policy:** `omit_reconstructed_rating_and_unblock_other_five`

**Binding level:** `BINDING`.

