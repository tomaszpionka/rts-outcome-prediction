# SC2EGSet Step 02_01_03 -- Q6 Rating-Reconstruction Successor Adjudication

## §1 Non-Materialization Disclaimer

This artifact is a Q6 successor adjudication of the `reconstructed_rating` family's rating-policy choice for sc2egset Step 02_01_03. It does NOT materialize any rating value, does NOT write any Parquet, does NOT run the CROSS-02-01-v1.0.1 post-materialization leakage audit, does NOT close Step 02_01_03, and does NOT append to any status YAML or research_log. Materialization is BLOCKED pending the algorithm-survey PR named by the Q6_selected_policy row.

## §2 Parent PR #242 Lineage

This artifact upgrades the PR #242 parent adjudication's Q6 row (`Q6_rating_policy`, which closed as `verdict=deferred_blocker`). Verbatim Q6 rationale from PR #242 (`02_01_03_history_source_anchor_coldstart_adjudication.md` §Q6 row): 'deferred_blocker because: per N3, ~83.95% MMR-missing density (verified in the dataset research log; consistent with the registry CSV is_mmr_missing_flag family) makes algorithm choice first-order. Pinning Elo / Glicko / Glicko-2 / TrueSkill / a rolling-winrate baseline without empirical evidence of which family handles the unrated / no-rating-history regime best would violate Invariant I7. Four candidate citations exist (Elo 1978; Glickman 1999; Glickman 2012; Herbrich, Minka, Graepel 2006) but binding one over the others requires repo evidence not yet generated.' PR #242 byte-stable artifacts are referenced by SHA-256 on every row (`parent_pr242_csv_sha256`, `parent_pr242_md_sha256`). Pinned SHAs:

- PR #242 CSV: `f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b`
- PR #242 MD: `fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d`

## §3 Parent PR #243 Lineage (Q5 Preserved)

Q5 (`cross_region_fragmentation_handling`) was resolved by PR #243 with `Q5_selected_policy=sensitivity_indicator_co_registration`, verdict `narrow_with_evidence`. This artifact does NOT re-adjudicate Q5. The `q6_q5_re_adjudication_drift` falsifier halts the entrypoint before write if any row carries a Q5 verdict-bearing token in a verdict-bearing field. Pinned SHAs:

- PR #243 CSV: `29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424`
- PR #243 MD: `026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719`

## §4 Q6-Only Scope Statement

Scope: select one of the 6 `Q6_RATING_POLICY_CANDIDATES` (or re-defer with rigour) for the `reconstructed_rating` family. Out of scope: any materialization, any algorithm benchmark, any race-conditioned BTL / Bradley-Terry / Neural BTL (recorded in §5 as 'excluded methods considered' per N-1), any raw-MMR-where-present hybrid (rejected in §5 per N-2), any Q5 re-adjudication, any Q1-Q4 / Q7 / Q8 re-adjudication, any Step 02_01_03 closure, any Step 02_01_04 start, any Phase 03 work, any cross-dataset (aoe2, aoestats, aoe2companion) work.

## §5 Per-Candidate Decision Table

| decision_id | candidate_policy | verdict | rating_evidence_level | complexity | leakage_risk | materialization_permission |
|---|---|---|---|---|---|---|
| `Q6A_omit_reconstructed_rating` | `omit_reconstructed_rating` | `deferred_recommendation` | `in_repo_only` | `low` | `not_applicable` | `permitted_for_other_5_families_without_reconstructed_rating` |
| `Q6B_rolling_win_rate_or_bayesian_smoothed_baseline` | `rolling_win_rate_or_bayesian_smoothed_baseline` | `deferred_recommendation` | `in_repo_only` | `low` | `low_if_forward_only_enforced` | `permitted_for_all_6_families_with_pinned_hyperparameters_pr` |
| `Q6C_elo` | `elo` | `deferred_recommendation` | `in_repo_plus_citation` | `low` | `low_if_forward_only_enforced` | `permitted_for_all_6_families_with_pinned_hyperparameters_pr` |
| `Q6D_glicko_or_glicko_2` | `glicko_or_glicko_2` | `deferred_recommendation` | `in_repo_plus_citation` | `medium` | `medium_if_forward_only_enforced` | `permitted_for_all_6_families_with_pinned_hyperparameters_pr` |
| `Q6E_trueskill_or_trueskill_like` | `trueskill_or_trueskill_like` | `deferred_recommendation` | `in_repo_plus_citation` | `high` | `medium_if_forward_only_enforced` | `permitted_for_all_6_families_with_pinned_hyperparameters_pr` |
| `Q6F_deferred_with_algorithm_survey` | `deferred_blocker_with_algorithm_survey_required` | `deferred_blocker` | `deferred` | `not_applicable` | `not_applicable` | `blocked_pending_algorithm_survey_pr` |

### §5.1 Excluded Methods Considered (N-1 binding)

Methods listed in the dataset's `research_log.md` (lines 733-734 and 961) as part of the intended backtesting universe but EXPLICITLY EXCLUDED from the Q6 candidate set per planning binding nit (b):

- `aligulac_style_btl`
- `bradley_terry`
- `neural_btl`

**Rationale.** BTL and race-conditioned BTL collapse to Elo-with-race-prior in 1v1 (the sc2egset PHA scope is 1v1-decisive). Neural BTL requires its own training/eval pipeline that exceeds Q6 successor-adjudication scope and would be addressed under the algorithm-survey Step if Q6F is selected. These methods are NOT extended into `Q6_RATING_POLICY_CANDIDATES`; they are recorded in every row's `excluded_methods_considered` field (JSON form) so the examination defense trail is preserved.

### §5.2 Raw-MMR-where-present hybrid rejection (N-2 binding)

The hybrid candidate `raw_mmr_where_present_plus_is_mmr_missing` (use raw MMR for the 16.05% rated subset; cold-start the remaining 83.95%) is REJECTED. Rationale: violates Invariant I5 symmetric-treatment because rated-vs-unrated rows would be fed asymmetric features; the rated/unrated partition is correlated with skill (tournament players over-represented in the rated 16.05% per research_log lines 1576-1626); the partition-as-feature would leak corpus structure into the model. The N-2 rejection token is carried verbatim in the `raw_mmr_hybrid_rejection` field of every row.

### §5.3 Q6F is a Legitimate Verdict (N-10 binding)

Selecting `Q6F_deferred_with_algorithm_survey` is a legitimate Q6 verdict, NOT a planning failure -- it preserves Invariant I7 ('no magic numbers') when comparative empirical evidence is genuinely insufficient. The Q6_selected_policy row binds Q6F per the planning T05 default recommendation (see §12 below).

## §6 Candidate Policy Comparison (4-axis)

| candidate | deployability | complexity | leakage_risk | evidence_level |
|---|---|---|---|---|
| `omit_reconstructed_rating` | `low` | `low` | `not_applicable` | `in_repo_only` |
| `rolling_win_rate_or_bayesian_smoothed_baseline` | `low` | `low` | `low_if_forward_only_enforced` | `in_repo_only` |
| `elo` | `low` | `low` | `low_if_forward_only_enforced` | `in_repo_plus_citation` |
| `glicko_or_glicko_2` | `medium` | `medium` | `medium_if_forward_only_enforced` | `in_repo_plus_citation` |
| `trueskill_or_trueskill_like` | `high` | `high` | `medium_if_forward_only_enforced` | `in_repo_plus_citation` |
| `deferred_blocker_with_algorithm_survey_required` | `not_applicable` | `not_applicable` | `not_applicable` | `deferred` |

## §7 MMR-Missingness Reaffirmation

MMR is missing in **83.95%** of `matches_flat_clean` rows (44418 total) and **83.65%** of `player_history_all` rows (44817 total). Cited verbatim from the dataset `research_log.md` lines 106 + 1135. This is not an outlier; it is structural (unrated professional corpus). The `is_mmr_missing` flag (CROSS-02-02 §6.2 row 'is_mmr_missing (PRE_GAME flag)' line 228) is the primary skill-signal proxy across the missing-MMR regime.

**Probe re-affirmation (this run):** MFC total=44418 / missing=37290; PHA total=44817 / missing=37489.

## §8 Rating-Method Literature Context

Algorithm primary sources (citation-only; no implementation):

- Elo (1978) -- The Rating of Chessplayers, Past and Present
- Glickman (1999) -- Parameter estimation in large dynamic paired comparison experiments
- Glickman (2012) -- The Glicko-2 system for rating players
- Herbrich, Minka, Graepel (2006) -- TrueSkill: A Bayesian Skill Rating System

## §9 Forward-Only Update Semantics (per candidate)

Deterministic ordering (binding on every candidate the future algorithm-survey Step evaluates): `(toon_id, TRY_CAST(ph.details_timeUTC AS TIMESTAMP), ph.replay_id)`. The strict-`<` filter `STRICT_LT_HISTORY_FILTER` (`TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at`) per PR #242 Q3 BIND_NOW applies to every candidate. Note on the grouping key: `player_history_all` does NOT carry a `player_id_worldwide` column on this dataset (verified by DESCRIBE at module-author time); the canonical PHA grouping key for sc2egset is `toon_id`; `player_id_worldwide` is constructed only at the MHM join layer per PR #242 Q2 BIND_NOW.

## §10 Cold-Start Policy per Candidate (G-CS-4)

Every candidate honours G-CS-4 (`reports/specs/02_02_feature_engineering_plan.md` §9 line 422): the first-match row for any player must not be silently dropped; missingness encoded as a `is_first_match` flag, imputed value with explicit imputation rule, or separate cold-start branch. Q6A satisfies trivially (omission). Q6B-E use literature priors (rating=1500 / mu-RD-sigma defaults / mu=25-sigma=25/3) with `is_first_match` co-registered. Q6F binds G-CS-4 in advance on every candidate evaluated by the algorithm-survey Step.

## §11 Leakage Constraints per Candidate (G-L-4)

Every candidate honours G-L-4 (`reports/specs/02_02_feature_engineering_plan.md` §10 line 455): no `pre_game` or `history_enriched_pre_game` feature may read game T's post-game rating delta or rating-after value. No global / batch fit. No future-match read. No target-match outcome read. Forward-only per-pair update.

## §12 Q6 Selected Policy Binding Row

**Selected:** `deferred_blocker_with_algorithm_survey_required`. **Verdict:** `deferred_blocker`. **Materialization permission:** `blocked_pending_algorithm_survey_pr`.

Rationale (verbatim from the Q6_selected_policy row): comparative back-testing AUC / log-loss evidence among the 4 non-trivial candidates (B/C/D/E) does NOT exist in any prior artifact; binding a single family without this evidence would violate Invariant I7. Per planning N-10, this is a legitimate verdict, NOT a planning failure -- it preserves I7 and triggers a dedicated algorithm-survey Step that will back-test the candidates over the unrated regime.

**Rejection rationale for the 5 unselected candidates** (JSON, also stored in the row's `rejected_options` field):

```json
[{"candidate": "omit_reconstructed_rating", "reason": "rejected as the binding selection because permanent omission forecloses the rating signal in any future Step; the algorithm-survey Step may yet find that Glicko-2 or rolling-baseline materially helps. Recommended only as a contingency if the survey concludes no candidate clears the noise floor."}, {"candidate": "rolling_win_rate_or_bayesian_smoothed_baseline", "reason": "rejected as the binding selection because it is a baseline (no opponent strength) rather than a true rating; back-testing against opponent-strength-aware candidates (Elo / Glicko / TrueSkill) is required before binding."}, {"candidate": "elo", "reason": "rejected as the binding selection because Elo lacks inactivity decay (vs Glicko-RD) and the dataset's tournament rhythm penalises this; back-testing required to confirm or refute this prior."}, {"candidate": "glicko_or_glicko_2", "reason": "rejected as the binding selection NOT on methodology grounds (this is the \u00a76.2 row 4 spec-favoured path) but on evidence grounds: no comparative back-testing AUC / log-loss exists in any prior artifact. Recommended favourite for the algorithm-survey Step."}, {"candidate": "trueskill_or_trueskill_like", "reason": "rejected as the binding selection because TrueSkill degenerates to Glicko-like for 1v1; marginal expressiveness gain may not justify the Bayesian factor-graph implementation cost."}]
```

## §13 Materialization Permission Statement

Materialization for the `reconstructed_rating` family is BLOCKED pending the algorithm-survey PR. The future Layer-3 materialization PR for the 6 history-enriched pre_game families must NOT proceed until the algorithm-survey Step resolves the Q6F deferral with a binding selection. The per-family impact summary row encodes this constraint over all 6 families.

## §14 Non-Substitution Statement

This artifact does NOT replace PR #229, #230, #234, #236, #237, #239, #240, #241, #242, #243, or #244. It does NOT alter Q1-Q5 / Q7 / Q8 bindings from PR #242 / #243. It augments the PR #242 Q6 row only.

## §15 Falsifier Roll-Call

Every key from `FALSIFIER_PRIORITY_CHAIN` (status reported verbatim per PR #242 / #243 precedent):

- `parent_pr242_csv_sha256_mismatch`: did_not_fire
- `parent_pr242_md_sha256_mismatch`: did_not_fire
- `parent_pr243_csv_sha256_mismatch`: did_not_fire
- `parent_pr243_md_sha256_mismatch`: did_not_fire
- `pr241_sha256_mismatch`: did_not_fire
- `cross_02_02_spec_sha256_mismatch`: did_not_fire
- `feature_family_registry_csv_sha256_mismatch`: did_not_fire
- `dataset_research_log_sha256_mismatch`: did_not_fire
- `player_history_all_yaml_sha256_mismatch`: did_not_fire
- `matches_flat_clean_yaml_sha256_mismatch`: did_not_fire
- `matches_history_minimal_yaml_sha256_mismatch`: did_not_fire
- `q6_candidate_set_incomplete`: did_not_fire
- `q6_omit_candidate_missing`: did_not_fire
- `q6_deferred_blocker_candidate_missing`: did_not_fire
- `decision_count_mismatch`: did_not_fire
- `decision_id_order_mismatch`: did_not_fire
- `q6_post_game_token_in_scoped_field`: did_not_fire
- `q6_direct_target_match_outcome_referenced`: did_not_fire
- `q6_future_match_leakage_referenced`: did_not_fire
- `q6_global_batch_fit_referenced`: did_not_fire
- `q6_phase_03_baseline_creep`: did_not_fire
- `q6_forward_only_constraint_missing_for_non_omit_candidate`: did_not_fire
- `q6_cold_start_policy_missing_for_non_omit_candidate`: did_not_fire
- `q6_tie_policy_missing_for_non_omit_candidate`: did_not_fire
- `q6_hyperparameter_policy_missing_for_non_omit_candidate`: did_not_fire
- `q6_evidence_level_field_invalid`: did_not_fire
- `q6_complexity_deployability_invalid`: did_not_fire
- `q6_leakage_risk_invalid`: did_not_fire
- `q6_materialization_permission_invalid`: did_not_fire
- `q6_external_citation_missing_when_non_omit_selected`: did_not_fire
- `q6_mmr_missingness_summary_missing`: did_not_fire
- `q6_materialization_permission_drift`: did_not_fire
- `q6_q5_re_adjudication_drift`: did_not_fire
- `q6_status_yaml_drift`: did_not_fire
- `q6_research_log_drift`: did_not_fire
- `q6_roadmap_drift`: did_not_fire
- `q6_materialization_creep`: did_not_fire
- `universal_tracker_source_in_history`: did_not_fire
- `q6_per_family_impact_summary_missing`: did_not_fire
- `q6_selected_policy_row_missing`: did_not_fire
- `q6_selected_policy_not_in_candidate_set`: did_not_fire
- `q6_selected_policy_verdict_invalid`: did_not_fire
- `q6_per_family_impact_broadcast_incomplete`: did_not_fire
- `q6_excluded_methods_considered_incomplete`: did_not_fire
- `q6_raw_mmr_hybrid_rejection_token_missing`: did_not_fire

## §16 SHA Provenance

- `parent_pr242_csv_sha256`: `f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b`
- `parent_pr242_md_sha256`: `fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d`
- `parent_pr243_csv_sha256`: `29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424`
- `parent_pr243_md_sha256`: `026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719`
- `pr241_scaffold_validator_module_sha256`: `b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904`
- `cross_02_02_spec_sha256`: `86af792370272e611f048aae0c48c9cc595eb4b44c1db38c0bb4ecea0ff1b289`
- `feature_family_registry_csv_sha256`: `320b8b018982f12539a34512421f1b34359bb825f0d1410687492dfe5c6fed1f`
- `dataset_research_log_sha256`: `3290607dad93f9907818f6c0fe61200fcbaa0d9891d3dfbec677996cb58fb1c7`
- `player_history_all_yaml_sha256`: `7962dd910e0b72419e35a9895689cd4ae6a51c2be0bc6e5e0fe4a0ceb8f207d0`
- `matches_flat_clean_yaml_sha256`: `9f76c1912624535b7b7ac0d2fb767fd4b9791a1d808bf73f747416d557d6cb1f`
- `matches_history_minimal_yaml_sha256`: `4c700e1b1584186542d6c1c43f847c03ee8664ced948534143e605a05ae7e67f`

## §17 No Step 02_01_03 Closure / No Phase 03 Start

Step 02_01_03 remains OPEN. This artifact does NOT add `02_01_03: complete` to `STEP_STATUS.yaml`. Closure is deferred per the PR #237 tranche-1 closure precedent. Phase 03 work remains forbidden (PHASE_STATUS.yaml shows Phase 03 = `not_started`; ml-protocol §4 superseded `create_temporal_split()` is barred from any thesis experiment).

## §18 Per-Decision Sections

### Q6A_omit_reconstructed_rating -- Rating policy option (A) omit_reconstructed_rating -- drop the reconstructed_rating family entirely

- **Verdict:** `deferred_recommendation`
- **Binding level:** `recommendation_only`
- **Scope:** `sc2egset.history_enriched_pre_game.reconstructed_rating`
- **Candidate policy:** `omit_reconstructed_rating`
- **Selected policy:** `(per-candidate row)`
- **Rating model family:** `none`
- **Rating evidence level:** `in_repo_only`
- **Complexity / deployability:** `low`
- **Leakage risk:** `not_applicable`
- **Materialization permission:** `permitted_for_other_5_families_without_reconstructed_rating`

**Forward-only constraints:** not_applicable_omitted

**Cold-start policy (G-CS-4):** G-CS-4 trivially satisfied by omission plus is_mmr_missing flag

**Tie policy:** not_applicable_omitted

**Hyperparameter policy:** not_applicable_omitted

**MMR missingness summary:** MMR missing in 83.95% of matches_flat_clean rows (44418 total) and 83.65% of player_history_all rows (44817 total); is_mmr_missing flag co-registered per CROSS-02-02 §6.2 row 'is_mmr_missing (PRE_GAME flag)' line 228.

**Feature availability summary:**

```json
5 of 6 history-enriched pre_game families remain available for materialization (focal_player_history, opponent_player_history, matchup_history_aggregate, in_game_history_aggregate, cross_region_fragmentation_handling); the reconstructed_rating slot is permanently empty.
```

**Excluded methods considered (N-1):**

```json
["aligulac_style_btl", "bradley_terry", "neural_btl"]
```

**Raw-MMR-hybrid rejection (N-2):** raw_mmr_where_present_plus_is_mmr_missing: not-applicable for Q6A because omission obviates the hybrid question; see Q6_selected_policy row for the binding rejection.

**Rationale / notes:**

Q6A evaluates option omit_reconstructed_rating. Omission is the strongest cold-start posture: no synthetic rating is fabricated for first-match rows; G-CS-4 is trivially satisfied because no rating value is produced; the is_mmr_missing flag (CROSS-02-02 §6.2 row 'is_mmr_missing (PRE_GAME flag)' line 228) remains the primary skill-signal proxy across the 83.95% MMR-missing density. Cost: loses cross-player skill comparability; rolling-winrate features (focal_player_history, opponent_player_history) cannot distinguish 50% winrate against weak opponents from 50% winrate against strong opponents. Materialization permission for the 5 non-rating families is PRESERVED. No target-match outcome read; no future matches read; no global batch fit (vacuously). Methods listed in dataset research_log lines 733-734 + 961 as part of the substrate's intended backtesting universe but EXCLUDED from the Q6 candidate set per planning binding nit (b): aligulac_style_btl, bradley_terry, neural_btl. Rationale: BTL and race-conditioned BTL collapse to Elo-with-race-prior in 1v1 (the sc2egset PHA scope); Neural BTL requires its own training/eval pipeline that exceeds Q6 successor-adjudication scope and would be addressed under the algorithm-survey Step if Q6F is selected. JSON list (canonical form for excluded_methods_considered field): ["aligulac_style_btl", "bradley_terry", "neural_btl"]

**Evidence paths:**

```
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md
```

**Falsifiers (row-level):**

```
q6_post_game_token_in_scoped_field:did_not_fire
```

### Q6B_rolling_win_rate_or_bayesian_smoothed_baseline -- Rating policy option (B) rolling_win_rate_or_bayesian_smoothed_baseline -- forward-only Bayesian-smoothed winrate

- **Verdict:** `deferred_recommendation`
- **Binding level:** `recommendation_only`
- **Scope:** `sc2egset.history_enriched_pre_game.reconstructed_rating`
- **Candidate policy:** `rolling_win_rate_or_bayesian_smoothed_baseline`
- **Selected policy:** `(per-candidate row)`
- **Rating model family:** `bayesian_smoothed_rolling_win_rate`
- **Rating evidence level:** `in_repo_only`
- **Complexity / deployability:** `low`
- **Leakage risk:** `low_if_forward_only_enforced`
- **Materialization permission:** `permitted_for_all_6_families_with_pinned_hyperparameters_pr`

**Forward-only constraints:** STRICT_LT_HISTORY_FILTER per PR #242 Q3 BIND_NOW then running beta-binomial or empirical-bayes update; forward-only per-pair update chronologically ordered by TRY_CAST(ph.details_timeUTC AS TIMESTAMP) with ph.replay_id tiebreaker.

**Cold-start policy (G-CS-4):** G-CS-4 via global prior alpha=beta=1 (Laplace) with is_first_match flag co-registered.

**Tie policy:** not_applicable; PHA history already decisive per PR #242 Q1 history filter (no draw handling).

**Hyperparameter policy:** alpha_prior, beta_prior, window_length deferred to algorithm implementation proof PR (OQ2).

**MMR missingness summary:** MMR missing in 83.95% of matches_flat_clean rows (44418 total) and 83.65% of player_history_all rows (44817 total); is_mmr_missing flag co-registered per CROSS-02-02 §6.2 row 'is_mmr_missing (PRE_GAME flag)' line 228.

**Feature availability summary:**

```json
All 6 history-enriched pre_game families remain available for materialization (focal_player_history, opponent_player_history, matchup_history_aggregate, reconstructed_rating, in_game_history_aggregate, cross_region_fragmentation_handling) once the algorithm-implementation-proof PR pins hyperparameters.
```

**Excluded methods considered (N-1):**

```json
["aligulac_style_btl", "bradley_terry", "neural_btl"]
```

**Raw-MMR-hybrid rejection (N-2):** raw_mmr_where_present_plus_is_mmr_missing: rejected; see Q6_selected_policy row for the binding rationale.

**Rationale / notes:**

Q6B evaluates option rolling_win_rate_or_bayesian_smoothed_baseline. Bayesian-smoothed forward-only win rate as a rating proxy (no opponent strength; no draws). Baseline -- not a true rating: cannot distinguish a 50% winrate against weak opponents from a 50% winrate against strong opponents. Lowest leakage surface among non-omit candidates. Already implicit in CROSS-02-02 §6.2 row 1 (focal_player_history rolling features). Per-game forward update only; no global batch fit; no target-match outcome read. Methods listed in dataset research_log lines 733-734 + 961 as part of the substrate's intended backtesting universe but EXCLUDED from the Q6 candidate set per planning binding nit (b): aligulac_style_btl, bradley_terry, neural_btl. Rationale: BTL and race-conditioned BTL collapse to Elo-with-race-prior in 1v1 (the sc2egset PHA scope); Neural BTL requires its own training/eval pipeline that exceeds Q6 successor-adjudication scope and would be addressed under the algorithm-survey Step if Q6F is selected. JSON list (canonical form for excluded_methods_considered field): ["aligulac_style_btl", "bradley_terry", "neural_btl"]

**Evidence paths:**

```
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
```

**Falsifiers (row-level):**

```
q6_post_game_token_in_scoped_field:did_not_fire
```

### Q6C_elo -- Rating policy option (C) elo (Elo 1978) -- constant-K forward-only Elo update

- **Verdict:** `deferred_recommendation`
- **Binding level:** `recommendation_only`
- **Scope:** `sc2egset.history_enriched_pre_game.reconstructed_rating`
- **Candidate policy:** `elo`
- **Selected policy:** `(per-candidate row)`
- **Rating model family:** `elo_per_toon_id_grouped`
- **Rating evidence level:** `in_repo_plus_citation`
- **Complexity / deployability:** `low`
- **Leakage risk:** `low_if_forward_only_enforced`
- **Materialization permission:** `permitted_for_all_6_families_with_pinned_hyperparameters_pr`

**Forward-only constraints:** STRICT_LT_HISTORY_FILTER then per-pair forward update chronologically ordered by TRY_CAST(ph.details_timeUTC AS TIMESTAMP) with ph.replay_id tiebreaker; forward-only (no global batch fit).

**Cold-start policy (G-CS-4):** G-CS-4 via literature prior rating=1500 for first-match rows with is_first_match flag co-registered.

**Tie policy:** decisive only; PHA history already decisive per PR #242 Q1; no explicit draw handling.

**Hyperparameter policy:** K_factor and initial_rating deferred to algorithm implementation proof PR (OQ2).

**MMR missingness summary:** MMR missing in 83.95% of matches_flat_clean rows (44418 total) and 83.65% of player_history_all rows (44817 total); is_mmr_missing flag co-registered per CROSS-02-02 §6.2 row 'is_mmr_missing (PRE_GAME flag)' line 228.

**Feature availability summary:**

```json
All 6 history-enriched pre_game families remain available for materialization (focal_player_history, opponent_player_history, matchup_history_aggregate, reconstructed_rating, in_game_history_aggregate, cross_region_fragmentation_handling) once the algorithm-implementation-proof PR pins hyperparameters.
```

**Excluded methods considered (N-1):**

```json
["aligulac_style_btl", "bradley_terry", "neural_btl"]
```

**Raw-MMR-hybrid rejection (N-2):** raw_mmr_where_present_plus_is_mmr_missing: rejected; see Q6_selected_policy row for the binding rationale.

**Rationale / notes:**

Q6C evaluates option elo (Elo 1978). Simplest principled rating; forward-only per-pair update; logistic expectation; constant K. Lacks inactivity decay (vs Glicko-RD) -- a player inactive for months retains their last rating. May be a poor fit for the dataset's tournament rhythm where players appear in bursts. No target-match outcome read; no future matches read; no global batch fit. Methods listed in dataset research_log lines 733-734 + 961 as part of the substrate's intended backtesting universe but EXCLUDED from the Q6 candidate set per planning binding nit (b): aligulac_style_btl, bradley_terry, neural_btl. Rationale: BTL and race-conditioned BTL collapse to Elo-with-race-prior in 1v1 (the sc2egset PHA scope); Neural BTL requires its own training/eval pipeline that exceeds Q6 successor-adjudication scope and would be addressed under the algorithm-survey Step if Q6F is selected. JSON list (canonical form for excluded_methods_considered field): ["aligulac_style_btl", "bradley_terry", "neural_btl"]

**Evidence paths:**

```
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
Elo (1978) -- The Rating of Chessplayers, Past and Present
```

**Falsifiers (row-level):**

```
q6_post_game_token_in_scoped_field:did_not_fire
```

### Q6D_glicko_or_glicko_2 -- Rating policy option (D) glicko_or_glicko_2 (Glickman 1999, 2012) -- forward-only with RD inactivity decay

- **Verdict:** `deferred_recommendation`
- **Binding level:** `recommendation_only`
- **Scope:** `sc2egset.history_enriched_pre_game.reconstructed_rating`
- **Candidate policy:** `glicko_or_glicko_2`
- **Selected policy:** `(per-candidate row)`
- **Rating model family:** `glicko_or_glicko_2_per_toon_id_grouped`
- **Rating evidence level:** `in_repo_plus_citation`
- **Complexity / deployability:** `medium`
- **Leakage risk:** `medium_if_forward_only_enforced`
- **Materialization permission:** `permitted_for_all_6_families_with_pinned_hyperparameters_pr`

**Forward-only constraints:** STRICT_LT_HISTORY_FILTER then per-rating-period batched update internally; the rating period itself is a hyperparameter (deferred); forward-only (no global batch fit) across rating periods.

**Cold-start policy (G-CS-4):** G-CS-4 via literature prior mu=1500, RD=350, sigma=0.06 for first-match rows with is_first_match flag co-registered (Glicko-2 defaults; final values deferred).

**Tie policy:** decisive only; PHA history already decisive per PR #242 Q1; draw score 0.5 not used.

**Hyperparameter policy:** mu_prior, RD_prior, sigma_prior, tau, rating_period_days deferred to algorithm implementation proof PR (OQ2).

**MMR missingness summary:** MMR missing in 83.95% of matches_flat_clean rows (44418 total) and 83.65% of player_history_all rows (44817 total); is_mmr_missing flag co-registered per CROSS-02-02 §6.2 row 'is_mmr_missing (PRE_GAME flag)' line 228.

**Feature availability summary:**

```json
All 6 history-enriched pre_game families remain available for materialization (focal_player_history, opponent_player_history, matchup_history_aggregate, reconstructed_rating, in_game_history_aggregate, cross_region_fragmentation_handling) once the algorithm-implementation-proof PR pins hyperparameters.
```

**Excluded methods considered (N-1):**

```json
["aligulac_style_btl", "bradley_terry", "neural_btl"]
```

**Raw-MMR-hybrid rejection (N-2):** raw_mmr_where_present_plus_is_mmr_missing: rejected; see Q6_selected_policy row for the binding rationale.

**Rationale / notes:**

Q6D evaluates option glicko_or_glicko_2 (Glickman 1999, 2012). CROSS-02-02 §6.2 row 4 line 241 names 'Glicko-2 or analogous' first -- this is the spec-favoured path. Adds rating deviation (RD) that grows with inactivity -- matches the dataset's tournament rhythm where players appear in bursts. Glicko-2 additionally tracks rating volatility sigma. Rating-period batching is a within-period micro-leakage surface that must be carefully bounded; recorded honestly as medium leakage risk. No target-match outcome read; no future matches read; no global batch fit. Methods listed in dataset research_log lines 733-734 + 961 as part of the substrate's intended backtesting universe but EXCLUDED from the Q6 candidate set per planning binding nit (b): aligulac_style_btl, bradley_terry, neural_btl. Rationale: BTL and race-conditioned BTL collapse to Elo-with-race-prior in 1v1 (the sc2egset PHA scope); Neural BTL requires its own training/eval pipeline that exceeds Q6 successor-adjudication scope and would be addressed under the algorithm-survey Step if Q6F is selected. JSON list (canonical form for excluded_methods_considered field): ["aligulac_style_btl", "bradley_terry", "neural_btl"]

**Evidence paths:**

```
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
Glickman (1999) -- Parameter estimation in large dynamic paired comparison experiments
Glickman (2012) -- The Glicko-2 system for rating players
```

**Falsifiers (row-level):**

```
q6_post_game_token_in_scoped_field:did_not_fire
```

### Q6E_trueskill_or_trueskill_like -- Rating policy option (E) trueskill_or_trueskill_like (Herbrich, Minka, Graepel 2006) -- forward-only Bayesian skill rating

- **Verdict:** `deferred_recommendation`
- **Binding level:** `recommendation_only`
- **Scope:** `sc2egset.history_enriched_pre_game.reconstructed_rating`
- **Candidate policy:** `trueskill_or_trueskill_like`
- **Selected policy:** `(per-candidate row)`
- **Rating model family:** `trueskill_2006_1v1_subset_or_trueskill_through_time_per_toon_id_grouped`
- **Rating evidence level:** `in_repo_plus_citation`
- **Complexity / deployability:** `high`
- **Leakage risk:** `medium_if_forward_only_enforced`
- **Materialization permission:** `permitted_for_all_6_families_with_pinned_hyperparameters_pr`

**Forward-only constraints:** STRICT_LT_HISTORY_FILTER then per-rating-period forward Gaussian message-passing posterior update; forward-only (no global batch fit).

**Cold-start policy (G-CS-4):** G-CS-4 via literature prior mu=25, sigma=25/3 for first-match rows with is_first_match flag co-registered (TrueSkill defaults; final values deferred).

**Tie policy:** decisive only; PHA history already decisive per PR #242 Q1; draw margin zero or minimal.

**Hyperparameter policy:** mu_prior, sigma_prior, beta, tau, draw_margin deferred to algorithm implementation proof PR (OQ2).

**MMR missingness summary:** MMR missing in 83.95% of matches_flat_clean rows (44418 total) and 83.65% of player_history_all rows (44817 total); is_mmr_missing flag co-registered per CROSS-02-02 §6.2 row 'is_mmr_missing (PRE_GAME flag)' line 228.

**Feature availability summary:**

```json
All 6 history-enriched pre_game families remain available for materialization (focal_player_history, opponent_player_history, matchup_history_aggregate, reconstructed_rating, in_game_history_aggregate, cross_region_fragmentation_handling) once the algorithm-implementation-proof PR pins hyperparameters.
```

**Excluded methods considered (N-1):**

```json
["aligulac_style_btl", "bradley_terry", "neural_btl"]
```

**Raw-MMR-hybrid rejection (N-2):** raw_mmr_where_present_plus_is_mmr_missing: rejected; see Q6_selected_policy row for the binding rationale.

**Rationale / notes:**

Q6E evaluates option trueskill_or_trueskill_like (Herbrich, Minka, Graepel 2006). Gaussian skill prior; factor-graph message passing; handles multi-player FFA but degenerates to Elo-like for 1v1 -- the marginal expressiveness gain for sc2egset's 1v1-decisive PHA scope may not justify the Bayesian factor-graph implementation cost. Mature libraries exist (e.g., trueskill PyPI package) but the implementation complexity exceeds Glicko-2 for limited 1v1 payoff. No target-match outcome read; no future matches read; no global batch fit. Methods listed in dataset research_log lines 733-734 + 961 as part of the substrate's intended backtesting universe but EXCLUDED from the Q6 candidate set per planning binding nit (b): aligulac_style_btl, bradley_terry, neural_btl. Rationale: BTL and race-conditioned BTL collapse to Elo-with-race-prior in 1v1 (the sc2egset PHA scope); Neural BTL requires its own training/eval pipeline that exceeds Q6 successor-adjudication scope and would be addressed under the algorithm-survey Step if Q6F is selected. JSON list (canonical form for excluded_methods_considered field): ["aligulac_style_btl", "bradley_terry", "neural_btl"]

**Evidence paths:**

```
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
Herbrich, Minka, Graepel (2006) -- TrueSkill: A Bayesian Skill Rating System
```

**Falsifiers (row-level):**

```
q6_post_game_token_in_scoped_field:did_not_fire
```

### Q6F_deferred_with_algorithm_survey -- Rating policy option (F) deferred_blocker_with_algorithm_survey_required -- 'punt with rigour' verdict per N-10

- **Verdict:** `deferred_blocker`
- **Binding level:** `deferred_blocker`
- **Scope:** `sc2egset.history_enriched_pre_game.reconstructed_rating`
- **Candidate policy:** `deferred_blocker_with_algorithm_survey_required`
- **Selected policy:** `(per-candidate row)`
- **Rating model family:** `to_be_determined_after_algorithm_survey_step`
- **Rating evidence level:** `deferred`
- **Complexity / deployability:** `not_applicable`
- **Leakage risk:** `not_applicable`
- **Materialization permission:** `blocked_pending_algorithm_survey_pr`

**Forward-only constraints:** binding in advance: STRICT_LT_HISTORY_FILTER; no global batch fit; no target-match outcome read; no future-match read; the algorithm-survey Step must honour these for every candidate evaluated. Forward-only.

**Cold-start policy (G-CS-4):** G-CS-4 binding in advance for every candidate evaluated by the future algorithm-survey Step.

**Tie policy:** decisive only; PHA history already decisive per PR #242 Q1.

**Hyperparameter policy:** deferred pending algorithm-survey Step and a downstream algorithm-implementation-proof PR (OQ2).

**MMR missingness summary:** MMR missing in 83.95% of matches_flat_clean rows (44418 total) and 83.65% of player_history_all rows (44817 total); is_mmr_missing flag co-registered per CROSS-02-02 §6.2 row 'is_mmr_missing (PRE_GAME flag)' line 228.

**Feature availability summary:**

```json
5 of 6 history-enriched pre_game families (focal_player_history, opponent_player_history, matchup_history_aggregate, in_game_history_aggregate, cross_region_fragmentation_handling) are blocked pending the algorithm-survey PR; reconstructed_rating itself is blocked pending Q6 upgrade from this deferred verdict.
```

**Excluded methods considered (N-1):**

```json
["aligulac_style_btl", "bradley_terry", "neural_btl"]
```

**Raw-MMR-hybrid rejection (N-2):** raw_mmr_where_present_plus_is_mmr_missing: rejected; see Q6_selected_policy row for the binding rationale.

**Rationale / notes:**

deferred_blocker because: comparative empirical evidence to bind a single rating-model family does not exist in any prior artifact and would require its own algorithm-survey Step. Q6F evaluates option deferred_blocker_with_algorithm_survey_required. This is the 'punt with rigour' verdict: comparative empirical evidence (back-testing AUC / log-loss on the unrated regime) does NOT exist in any prior artifact and would require its own algorithm-survey Step. Selecting Q6F preserves Invariant I7 (no magic numbers for K, prior, RD, sigma, tau, rating_period) -- a legitimate Q6 verdict per planning N-10, NOT a planning failure. The survey would back-test all 4 non-trivial families (B/C/D/E) plus the excluded BTL family from a separate Step. Forward-only / cold-start / leakage constraints are binding in advance: any candidate evaluated by the survey must honour them. No target-match outcome read; no future matches read; no global batch fit. Methods listed in dataset research_log lines 733-734 + 961 as part of the substrate's intended backtesting universe but EXCLUDED from the Q6 candidate set per planning binding nit (b): aligulac_style_btl, bradley_terry, neural_btl. Rationale: BTL and race-conditioned BTL collapse to Elo-with-race-prior in 1v1 (the sc2egset PHA scope); Neural BTL requires its own training/eval pipeline that exceeds Q6 successor-adjudication scope and would be addressed under the algorithm-survey Step if Q6F is selected. JSON list (canonical form for excluded_methods_considered field): ["aligulac_style_btl", "bradley_terry", "neural_btl"]

**Evidence paths:**

```
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md
```

**Falsifiers (row-level):**

```
q6_post_game_token_in_scoped_field:did_not_fire
```

### Q6_selected_policy -- Q6 rating policy selection (BINDING row; verdict emerges from per-candidate evidence table)

- **Verdict:** `deferred_blocker`
- **Binding level:** `deferred_blocker`
- **Scope:** `sc2egset.history_enriched_pre_game.reconstructed_rating`
- **Candidate policy:** `(derived row)`
- **Selected policy:** `deferred_blocker_with_algorithm_survey_required`
- **Rating model family:** `to_be_determined_after_algorithm_survey_step`
- **Rating evidence level:** `deferred`
- **Complexity / deployability:** `not_applicable`
- **Leakage risk:** `not_applicable`
- **Materialization permission:** `blocked_pending_algorithm_survey_pr`

**Forward-only constraints:** binding in advance on every candidate the algorithm-survey Step evaluates: STRICT_LT_HISTORY_FILTER; no global batch fit; no target-match outcome read; no future-match read; forward-only per-pair update.

**Cold-start policy (G-CS-4):** G-CS-4 binding in advance on every candidate evaluated.

**Tie policy:** decisive only; PHA history already decisive per PR #242 Q1.

**Hyperparameter policy:** deferred pending algorithm-survey Step and the downstream algorithm-implementation-proof PR (OQ2).

**MMR missingness summary:** MMR missing in 83.95% of matches_flat_clean rows (44418 total) and 83.65% of player_history_all rows (44817 total); is_mmr_missing flag co-registered per CROSS-02-02 §6.2 row 'is_mmr_missing (PRE_GAME flag)' line 228.

**Feature availability summary:**

```json
5 of 6 history-enriched pre_game families (focal_player_history, opponent_player_history, matchup_history_aggregate, in_game_history_aggregate, cross_region_fragmentation_handling) are blocked pending the algorithm-survey PR; reconstructed_rating itself is blocked pending Q6 upgrade from this deferred verdict.
```

**Excluded methods considered (N-1):**

```json
["aligulac_style_btl", "bradley_terry", "neural_btl"]
```

**Raw-MMR-hybrid rejection (N-2):** The hybrid candidate 'raw_mmr_where_present_plus_is_mmr_missing' -- use raw MMR for the 16.05% rated subset and cold-start the unrated 83.95% -- is REJECTED. Rationale: violates Invariant I5 symmetric-treatment because rated-vs-unrated rows would be fed asymmetric features; the rated/unrated partition is correlated with skill (tournament players over-represented in the rated 16.05% per research_log lines 1576-1626); the partition-as-feature would leak corpus structure into the model. Use is_mmr_missing flag co-registration plus the Q6-selected reconstructed_rating (or omission) instead.

**Rejected options:**

```json
[{"candidate": "omit_reconstructed_rating", "reason": "rejected as the binding selection because permanent omission forecloses the rating signal in any future Step; the algorithm-survey Step may yet find that Glicko-2 or rolling-baseline materially helps. Recommended only as a contingency if the survey concludes no candidate clears the noise floor."}, {"candidate": "rolling_win_rate_or_bayesian_smoothed_baseline", "reason": "rejected as the binding selection because it is a baseline (no opponent strength) rather than a true rating; back-testing against opponent-strength-aware candidates (Elo / Glicko / TrueSkill) is required before binding."}, {"candidate": "elo", "reason": "rejected as the binding selection because Elo lacks inactivity decay (vs Glicko-RD) and the dataset's tournament rhythm penalises this; back-testing required to confirm or refute this prior."}, {"candidate": "glicko_or_glicko_2", "reason": "rejected as the binding selection NOT on methodology grounds (this is the \u00a76.2 row 4 spec-favoured path) but on evidence grounds: no comparative back-testing AUC / log-loss exists in any prior artifact. Recommended favourite for the algorithm-survey Step."}, {"candidate": "trueskill_or_trueskill_like", "reason": "rejected as the binding selection because TrueSkill degenerates to Glicko-like for 1v1; marginal expressiveness gain may not justify the Bayesian factor-graph implementation cost."}]
```

**Rationale / notes:**

Q6_selected_policy is the BINDING row for the Q6 successor adjudication. Selected: Q6F_deferred_with_algorithm_survey (deferred_blocker_with_algorithm_survey_required). Rationale: comparative back-testing AUC / log-loss evidence among the 4 non-trivial candidates (B/C/D/E) does NOT exist in any prior artifact; binding a single family without this evidence would violate Invariant I7 ('no magic numbers' applied to model-family choice). Per planning N-10, selecting Q6F is a legitimate verdict, NOT a planning failure -- it preserves I7 and triggers a dedicated algorithm-survey Step that will back-test the candidates over the unrated regime. Materialization permission: blocked_pending_algorithm_survey_pr (the future Layer-3 materialization PR must NOT proceed until the algorithm-survey Step resolves the selection). Q5 binding from PR #243 (Q5_selected_policy=sensitivity_indicator_co_registration, verdict=narrow_with_evidence) is preserved verbatim and not re-adjudicated. The hybrid candidate 'raw_mmr_where_present_plus_is_mmr_missing' -- use raw MMR for the 16.05% rated subset and cold-start the unrated 83.95% -- is REJECTED. Rationale: violates Invariant I5 symmetric-treatment because rated-vs-unrated rows would be fed asymmetric features; the rated/unrated partition is correlated with skill (tournament players over-represented in the rated 16.05% per research_log lines 1576-1626); the partition-as-feature would leak corpus structure into the model. Use is_mmr_missing flag co-registration plus the Q6-selected reconstructed_rating (or omission) instead. Methods listed in dataset research_log lines 733-734 + 961 as part of the substrate's intended backtesting universe but EXCLUDED from the Q6 candidate set per planning binding nit (b): aligulac_style_btl, bradley_terry, neural_btl. Rationale: BTL and race-conditioned BTL collapse to Elo-with-race-prior in 1v1 (the sc2egset PHA scope); Neural BTL requires its own training/eval pipeline that exceeds Q6 successor-adjudication scope and would be addressed under the algorithm-survey Step if Q6F is selected. JSON list (canonical form for excluded_methods_considered field): ["aligulac_style_btl", "bradley_terry", "neural_btl"]

**Evidence paths:**

```
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.md
```

**Falsifiers (row-level):**

```
q6_post_game_token_in_scoped_field:did_not_fire
q6_q5_re_adjudication_drift:did_not_fire
q6_materialization_creep:did_not_fire
```

### Q6_per_family_impact_summary -- Q6 per-family impact summary (derived row; broadcasts the Q6 selected_policy decision over the 6 history-enriched pre_game families)

- **Verdict:** `recommendation_only`
- **Binding level:** `recommendation_only`
- **Scope:** `all_six_history_enriched_pre_game_families`
- **Candidate policy:** `(derived row)`
- **Selected policy:** `deferred_blocker_with_algorithm_survey_required`
- **Rating model family:** `not_applicable_per_family_summary_row`
- **Rating evidence level:** `deferred`
- **Complexity / deployability:** `not_applicable`
- **Leakage risk:** `not_applicable`
- **Materialization permission:** `blocked_pending_algorithm_survey_pr`

**Forward-only constraints:** not_applicable_per_family_summary_row

**Cold-start policy (G-CS-4):** not_applicable_per_family_summary_row

**Tie policy:** not_applicable_per_family_summary_row

**Hyperparameter policy:** not_applicable_per_family_summary_row

**MMR missingness summary:** MMR missing in 83.95% of matches_flat_clean rows (44418 total) and 83.65% of player_history_all rows (44817 total); is_mmr_missing flag co-registered per CROSS-02-02 §6.2 row 'is_mmr_missing (PRE_GAME flag)' line 228.

**Feature availability summary:**

```json
{"focal_player_history": {"affected_by_q6": "no", "materialization_status": "blocked_pending_algorithm_survey_pr_per_q6f_selected"}, "opponent_player_history": {"affected_by_q6": "no", "materialization_status": "blocked_pending_algorithm_survey_pr_per_q6f_selected"}, "matchup_history_aggregate": {"affected_by_q6": "no", "materialization_status": "blocked_pending_algorithm_survey_pr_per_q6f_selected"}, "reconstructed_rating": {"affected_by_q6": "yes", "materialization_status": "blocked_pending_algorithm_survey_pr"}, "in_game_history_aggregate": {"affected_by_q6": "no", "materialization_status": "blocked_pending_algorithm_survey_pr_per_q6f_selected"}, "cross_region_fragmentation_handling": {"affected_by_q6": "no", "materialization_status": "blocked_pending_algorithm_survey_pr_per_q6f_selected"}}
```

**Excluded methods considered (N-1):**

```json
["aligulac_style_btl", "bradley_terry", "neural_btl"]
```

**Raw-MMR-hybrid rejection (N-2):** raw_mmr_where_present_plus_is_mmr_missing: rejection inherited from Q6_selected_policy row.

**Rationale / notes:**

Q6_per_family_impact_summary is the derived per-family broadcast row mirroring PR #243's Q5_per_family_impact_summary pattern. Q6 strictly affects only the reconstructed_rating family; the other 5 families' materialization is blocked downstream of the Q6F deferred verdict (the entire 6-family tranche is blocked pending the algorithm-survey PR because the planning Assumption 11 binding bundles the 6 families). If a future plan elects to decouple the 5 non-rating families and materialize them under a scope-narrowing Step (per OQ1), this summary row's status values would change. Q5 binding from PR #243 (Q5_selected_policy=sensitivity_indicator_co_registration, verdict=narrow_with_evidence) is preserved verbatim and not re-adjudicated.

**Evidence paths:**

```
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.csv
```

**Falsifiers (row-level):**

```
q6_per_family_impact_broadcast_incomplete:did_not_fire
```

