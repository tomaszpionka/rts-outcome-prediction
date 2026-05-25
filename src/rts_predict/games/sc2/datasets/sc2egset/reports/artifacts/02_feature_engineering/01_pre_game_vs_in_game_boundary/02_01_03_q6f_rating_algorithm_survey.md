# Q6F Rating-Algorithm Survey

**Audit PR:** PR #<TBD>

## 1. Non-Materialization Disclaimer

This artifact is the Q6F rating-algorithm SURVEY only. It does NOT materialize any rating value, does NOT write any Parquet, does NOT run the CROSS-02-01 post-materialization leakage audit, does NOT close Step 02_01_03, does NOT update any status YAML, and does NOT touch the dataset research_log or ROADMAP. The per-candidate metrics in this artifact are EVALUATION TRACES of forward-only rating predictions; they are Q6F-internal and are NOT Phase-03 baseline modelling results.

## 2. Parent PR #242 Lineage

- CSV SHA256: `f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv`)
- MD  SHA256: `fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md`)

## 3. Parent PR #243 Lineage (Q5 Preserved)

- CSV SHA256: `29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.csv`)
- MD  SHA256: `026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.md`)

Q5_selected_policy = `sensitivity_indicator_co_registration`; verdict = `narrow_with_evidence`. This survey does NOT re-adjudicate Q5.

## 4. Parent PR #245 Lineage (Q6 deferred_blocker -> this survey)

- CSV SHA256: `703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.csv`)
- MD  SHA256: `7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419` (`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.md`)

Quoted from PR #245 Q6_selected_policy row: '`deferred_blocker_with_algorithm_survey_required` because the comparative back-testing evidence among Elo / Glicko-2 / TrueSkill / rolling-baseline does not exist in any prior artifact and binding a winner would violate Invariant I7.' This Q6F survey is the direct unblock condition.

## 5. Q6F-Only Scope

Q6F is the Layer-2 algorithm survey. It is NOT Phase 03 baseline modelling. The metrics are evaluation traces, not features. It does NOT train logistic regression, gradient boosting, GNNs, or any downstream classifier. It does NOT use a train/test split or temporal CV. The outcome of each PHA row is used only to score the forward-only prediction and to update the rating state for FUTURE rows; it is never read as a feature input for predicting its own match.

## 6. Candidate Set + N-1 Rejection (BTL family)

BTL family (aligulac_style_btl, bradley_terry, neural_btl) acknowledged from dataset research_log lines 733-734 and 961 but EXCLUDED from this Q6F survey's executable candidate set per Layer-1 Assumption 8: in 1v1 decisive matches BTL collapses to Elo-with-race-prior (Elo already in the survey); Neural BTL requires a full model-training pipeline (Phase-03 scope; out of scope here). The Layer-2 executor may extend the candidate set in a follow-up survey PR with explicit substantive justification and citations.

Methods acknowledged-and-excluded: aligulac_style_btl, bradley_terry, neural_btl.

## 7. Candidate Set + N-2 Rejection (raw MMR hybrid)

raw_mmr_where_present_plus_is_mmr_missing: REJECTED unchanged from PR #245 N-2. The rated/unrated partition is correlated with skill (only ranked-ladder games carry MMR; unrated games predominantly are leaderboard-absent practice / custom games), so admitting raw_mmr as a feature plus is_mmr_missing as a flag would leak corpus structure under Invariant I5 (symmetric treatment). The Q6F survey does not re-open this rejection.

## 8. Algorithm Specifications per Candidate

### omit_reconstructed_rating

- Initialization: not_applicable_carry_forward
- Hyperparameter policy: not_applicable_carry_forward
- Cold-start policy: Trivially satisfied: omission of the reconstructed_rating feature obviates cold-start (G-CS-4) for this family. is_mmr_missing co-registration is preserved per CROSS-02-02 §6.2.
- Tie policy: not_applicable_carry_forward
- Forward-only constraints: not_applicable_carry_forward
- Player identity policy: toon_id (PHA grouping key per PR #245 §9; PHA has no player_id_worldwide column on this dataset).

### rolling_win_rate_or_bayesian_smoothed_baseline

- Initialization: Laplace prior: alpha=1.0 wins + beta=1.0 losses; prior-implied P(focal wins) = 0.5 at cold-start.
- Hyperparameter policy: alpha=1.0, beta=1.0 (literature default; Laplace 1814 rule-of-succession). Expanding window over all strictly-prior PHA rows for the focal toon_id; no finite-window variant in this survey.
- Cold-start policy: G-CS-4: first match per focal toon_id is cold-start; prior-implied probability 0.5 is emitted; is_cold_start=True is flagged for downstream coverage_rate.
- Tie policy: Decisive-only (Win/Loss) per PR #242 Q1; same-timestamp ties broken by deterministic sort key (focal_toon, TRY_CAST(details_timeUTC AS TIMESTAMP), replay_id).
- Forward-only constraints: Prediction uses only strictly-prior PHA rows for the focal toon_id per STRICT_LT_HISTORY_FILTER. Rating state updated AFTER scoring; outcome never read as feature input for its own match.
- Player identity policy: toon_id (PHA grouping key per PR #245 §9; PHA has no player_id_worldwide column on this dataset).

### elo

- Initialization: Initial rating R0=1500 (Elo 1978 chess convention); applied to every previously-unseen toon_id.
- Hyperparameter policy: K-factor=24.0 (mid-point between chess-conservative K=20 and chess-default K=32; commonly used in aoe2-tournament Elo deployments). No tuning in this survey per Layer-1 Assumption 10.
- Cold-start policy: G-CS-4: first match per focal toon_id uses initial rating 1500; is_cold_start=True is flagged for downstream coverage_rate; predicted probability at cold-start is the expected-score function evaluated at the symmetric rating diff.
- Tie policy: Decisive-only (Win/Loss) per PR #242 Q1; same-timestamp ties broken by deterministic sort key.
- Forward-only constraints: Prediction uses focal and opponent ratings as of strictly-prior PHA rows per STRICT_LT_HISTORY_FILTER. Both players' ratings updated AFTER scoring; outcome never read as feature input for its own match.
- Player identity policy: toon_id (PHA grouping key per PR #245 §9; PHA has no player_id_worldwide column on this dataset).

### glicko_or_glicko_2

- Initialization: Initial mu=1500 (Glicko scale), RD=350, sigma=0.06 (Glickman 2012 reference defaults). Mapped to Glicko-2 internal scale by (mu - 1500) / 173.7178.
- Hyperparameter policy: mu=1500, RD=350, sigma=0.06, tau=0.5 (Glickman 2012 reference defaults). Event-by-event simplification: each match treated as a single-observation rating period. Sigma held constant in this simplification; the full batched volatility update is deferred to a future Q6G PR.
- Cold-start policy: G-CS-4: first match per focal toon_id uses prior mu=1500, RD=350; is_cold_start=True is flagged for downstream coverage_rate; predicted probability at cold-start is the symmetric E function evaluated at zero mu diff.
- Tie policy: Decisive-only (Win/Loss) per PR #242 Q1; same-timestamp ties broken by deterministic sort key.
- Forward-only constraints: Prediction uses focal and opponent (mu, RD) states as of strictly-prior PHA rows per STRICT_LT_HISTORY_FILTER. Both players' states updated AFTER scoring; outcome never read as feature input for its own match.
- Player identity policy: toon_id (PHA grouping key per PR #245 §9; PHA has no player_id_worldwide column on this dataset).

### trueskill_or_trueskill_like

- Initialization: Initial mu=25, sigma=25/3 (Herbrich, Minka, Graepel 2006 defaults; also Xbox Live deployment defaults).
- Hyperparameter policy: mu=25, sigma=25/3, beta=25/6, tau=25/300 (Herbrich, Minka, Graepel 2006 §4; literature default; cited in MD §8 per NIT-4), draw_margin=0 (PHA is decisive-only per PR #242 Q1).
- Cold-start policy: G-CS-4: first match per focal toon_id uses prior mu=25, sigma=25/3; is_cold_start=True is flagged for downstream coverage_rate; predicted probability at cold-start is the symmetric normal CDF evaluated at zero mu diff.
- Tie policy: Decisive-only (Win/Loss) per PR #242 Q1; draw_margin=0; same-timestamp ties broken by deterministic sort key.
- Forward-only constraints: Prediction uses focal and opponent (mu, sigma) states as of strictly-prior PHA rows per STRICT_LT_HISTORY_FILTER. Both players' states updated AFTER scoring; outcome never read as feature input for its own match. Dynamic factor tau is applied to pre-match variances each game.
- Player identity policy: toon_id (PHA grouping key per PR #245 §9; PHA has no player_id_worldwide column on this dataset).

### deferred_blocker_with_algorithm_survey_required

- Initialization: not_applicable_carry_forward
- Hyperparameter policy: not_applicable_carry_forward
- Cold-start policy: not_applicable_carry_forward
- Tie policy: not_applicable_carry_forward
- Forward-only constraints: not_applicable_carry_forward
- Player identity policy: toon_id (PHA grouping key per PR #245 §9; PHA has no player_id_worldwide column on this dataset).

## 9. Forward-Only Update Semantics

Every per-row prediction uses rating state computed strictly from PHA records satisfying `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at` (verbatim from PR #245). The target outcome updates the rating state ONLY AFTER scoring the prediction. Stream ordering is `(focal_toon, TRY_CAST(details_timeUTC AS TIMESTAMP), replay_id)` -- deterministic; same-timestamp ties broken by `replay_id`.

## 10. Metric Definitions

AUC (ROC) computed via the Mann-Whitney U formulation with tie-averaged ranks; log-loss is the mean negative log likelihood with predictions clipped to [1e-15, 1 - 1e-15]; Brier is the mean squared error of the predicted probability; calibration error is expected calibration error (ECE) over 10 equal-width bins. All metrics computed on the non-cold-start subset (mask `~is_cold_start`).

## 11. Per-Candidate Metric Table

| Candidate | AUC (CI) | Log-loss (CI) | Brier (CI) | Calibration Error |
|---|---|---|---|---|
| omit_reconstructed_rating | n/a (carry-forward) | n/a | n/a | n/a |
| rolling_win_rate_or_bayesian_smoothed_baseline | 0.5900 (0.5845--0.5950) | 0.6993 (0.6964--0.7027) | 0.2512 (0.2498--0.2527) | 0.0744 |
| elo | 0.6809 (0.6755--0.6856) | 0.6431 (0.6409--0.6458) | 0.2262 (0.2252--0.2274) | 0.0300 |
| glicko_or_glicko_2 | 0.7105 (0.7054--0.7153) | 0.6255 (0.6216--0.6302) | 0.2177 (0.2160--0.2197) | 0.0349 |
| trueskill_or_trueskill_like | 0.7109 (0.7060--0.7159) | 0.6291 (0.6246--0.6342) | 0.2185 (0.2167--0.2205) | 0.0436 |
| deferred_blocker_with_algorithm_survey_required | n/a (carry-forward) | n/a | n/a | n/a |

## 12. Q6F Selected Policy Binding Row

- selected_policy: `narrow_with_evidence`
- verdict: `narrow_with_evidence`
- materialization_permission: `recommendation_only_blocked_pending_implementation_proof_pr`

Rationale (verbatim from CSV notes column):

```
Q6F SELECTED POLICY = narrow_with_evidence
VERDICT = narrow_with_evidence
MATERIALIZATION PERMISSION = recommendation_only_blocked_pending_implementation_proof_pr
RATIONALE: Candidate glicko_or_glicko_2 achieved log-loss 0.625522 (CI upper bound 0.630180) strictly below the baseline CI lower bound (0.696358); however the other included opponent-strength candidates' CIs overlap with glicko_or_glicko_2's CI. Recording narrow_with_evidence: an implementation-proof PR is required before Layer-3 materialization to demonstrate byte-stable forward-only rating outputs and re-evaluate the inter-candidate ordering with a larger bootstrap.
DECISION RULE (verbatim): NIT-3 / OQ1 proper-score CI binding; AUC alone CANNOT bind a candidate.
Q5 BINDING preserved (sensitivity_indicator_co_registration); raw_mmr_hybrid_rejection re-affirmed; BTL family acknowledgement re-affirmed.
```

Decision rule:

```
Q6F SELECTION DECISION RULE (NIT-3 / OQ1; CI-based binding)
============================================================

Let M = {rolling_baseline, elo, glicko_or_glicko_2,
trueskill_or_trueskill_like}, the set of 4 included candidates.

Let baseline = the rolling_win_rate_or_bayesian_smoothed_baseline
candidate (Laplace-prior baseline; used as the no-opponent-strength
reference for proper-score improvement).

For each candidate c in M, compute:

    log_loss(c), log_loss_ci_low(c), log_loss_ci_high(c)
    brier(c),    brier_ci_low(c),    brier_ci_high(c)
    auc(c),      auc_ci_low(c),      auc_ci_high(c)

Lower log-loss and lower Brier are better. AUC is secondary and reported
with CI only; AUC alone cannot bind a candidate (NIT-3 / OQ1).

DECISION:

1. If max(M.log_loss_ci_high) < baseline.log_loss_ci_low AND
   max(M.brier_ci_high)    < baseline.brier_ci_low:
   --- impossible by construction since baseline IS in M's candidate
       set --- this branch is illustrative only ---

2. Let c* = argmin over c in M of log_loss(c).
   If log_loss_ci_high(c*) < log_loss_ci_low(c) for every c in M\{c*}
   AND brier_ci_high(c*) < brier_ci_low(c) for every c in M\{c*}:
       selected_policy = "bind_now"
       verdict = "bind_now"
       materialization_permission = "permitted_for_all_6_families_..."

3. Else if log_loss_ci_high(c*) < baseline.log_loss_ci_low
   AND brier_ci_high(c*) < baseline.brier_ci_low:
       selected_policy = "narrow_with_evidence"
       verdict = "narrow_with_evidence"
       materialization_permission = "recommendation_only_blocked_pending_implementation_proof_pr"

4. Else if the best candidate's log-loss is within CI overlap of the
   baseline (no proper-score improvement detectable):
       selected_policy = "omit_reconstructed_rating_and_unblock_other_five"
       verdict = "omit_reconstructed_rating_and_unblock_other_five"
       materialization_permission = "permitted_for_other_5_families_without_reconstructed_rating"

5. Else (fallback; ambiguous):
       selected_policy = "deferred_blocker"
       verdict = "deferred_blocker"
       materialization_permission = "blocked_pending_named_reason"

This rule supersedes any pinned numeric AUC threshold (NIT-3 cit.
Steyerberg 2009; Hosmer-Lemeshow 2013). AUC is reported with CI for
transparency but never used as the sole binding criterion.
```

## 13. Materialization Permission Statement

Materialization permission for Step 02_01_03: `recommendation_only_blocked_pending_implementation_proof_pr`. Per the per-family impact summary:

```
focal_player_history: recommendation_only_blocked_pending_implementation_proof_pr
opponent_player_history: recommendation_only_blocked_pending_implementation_proof_pr
matchup_history_aggregate: recommendation_only_blocked_pending_implementation_proof_pr
reconstructed_rating: recommendation_only_blocked_pending_implementation_proof_pr
in_game_history_aggregate: recommendation_only_blocked_pending_implementation_proof_pr
cross_region_fragmentation_handling: recommendation_only_blocked_pending_implementation_proof_pr
```

Future feature materialization is a SEPARATE PR (Layer-3) and is subject to its own CROSS-02-01 post-materialization leakage audit. This Q6F survey does NOT substitute for that audit.

## 14. Non-Substitution Statement

This artifact does NOT replace PR #242 (8-question parent adjudication), PR #243 (Q5 cross-region successor), or PR #245 (Q6 rating-reconstruction successor). It is a successor adjudication that emits a Q6F verdict; it does not retract any prior verdict.

## 15. Falsifier Roll-Call

```
parent_pr242_csv_sha256_mismatch:did_not_fire
parent_pr242_md_sha256_mismatch:did_not_fire
parent_pr243_csv_sha256_mismatch:did_not_fire
parent_pr243_md_sha256_mismatch:did_not_fire
parent_pr245_csv_sha256_mismatch:did_not_fire
parent_pr245_md_sha256_mismatch:did_not_fire
q6f_candidate_set_incomplete:did_not_fire
q6f_decision_count_mismatch:did_not_fire
q6f_decision_id_order_mismatch:did_not_fire
q6f_csv_byte_determinism_violation:did_not_fire
q6f_materialization_creep:did_not_fire
q6f_rating_trace_persistence_violation:did_not_fire
q6f_rating_object_persistence_violation:did_not_fire
q6f_parquet_emitted:did_not_fire
q6f_q5_re_adjudication_drift:did_not_fire
q6f_status_yaml_drift:did_not_fire
q6f_research_log_drift:did_not_fire
q6f_roadmap_drift:did_not_fire
q6f_spec_drift:did_not_fire
q6f_cleaning_layer_drift:did_not_fire
q6f_target_match_outcome_read_as_input:did_not_fire
q6f_future_match_leakage_referenced:did_not_fire
q6f_global_batch_fit_referenced:did_not_fire
q6f_phase_03_baseline_creep:did_not_fire
q6f_step_02_01_04_creep:did_not_fire
q6f_forward_only_constraint_missing_for_non_omit_candidate:did_not_fire
q6f_cold_start_policy_missing_for_non_omit_candidate:did_not_fire
q6f_tie_policy_missing_for_non_omit_candidate:did_not_fire
q6f_hyperparameter_policy_missing_for_non_omit_candidate:did_not_fire
q6f_selected_policy_row_missing:did_not_fire
q6f_selected_policy_verdict_invalid:did_not_fire
q6f_per_family_impact_summary_missing:did_not_fire
q6f_per_family_impact_broadcast_incomplete:did_not_fire
q6f_excluded_methods_considered_incomplete:did_not_fire
q6f_raw_mmr_hybrid_rejection_missing:did_not_fire
q6f_btl_family_acknowledgement_missing:did_not_fire
q6f_auc_alone_binding_violation:did_not_fire
q6f_trueskill_tau_unjustified:did_not_fire
```

## 16. SHA Provenance

- PR #242 CSV SHA256: `f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b`
- PR #242 MD  SHA256: `fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d`
- PR #243 CSV SHA256: `29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424`
- PR #243 MD  SHA256: `026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719`
- PR #245 CSV SHA256: `703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0`
- PR #245 MD  SHA256: `7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419`

## 17. No Step 02_01_03 Closure / No Phase 03 Start

This PR does NOT close Step 02_01_03; closure is reserved for a future Layer-3 materialization PR (or a separate omit-and-unblock closure PR if Q6F selected `omit_reconstructed_rating_and_unblock_other_five`). Phase 03 remains `not_started` and no baseline modelling is performed in this PR.

## 18. Citation Provenance

- Elo (1978) -- The Rating of Chessplayers, Past and Present. Arco Publishing, New York.
- Glickman (1999) -- Parameter estimation in large dynamic paired comparison experiments. Applied Statistics 48: 377-394.
- Glickman (2012) -- Example of the Glicko-2 system. Boston University Technical Note.
- Herbrich, Minka, Graepel (2006) -- TrueSkill: A Bayesian Skill Rating System. NIPS 2006: 569-576.
- Steyerberg (2009) -- Clinical Prediction Models. Springer, Chapter 15 on discrimination and calibration.
- Hosmer, Lemeshow, Sturdivant (2013) -- Applied Logistic Regression, 3rd ed., Wiley, Chapter 5 on assessment of fit.

<!-- per_family_impact_summary row decision_id: Q6F_per_family_impact_summary -->
