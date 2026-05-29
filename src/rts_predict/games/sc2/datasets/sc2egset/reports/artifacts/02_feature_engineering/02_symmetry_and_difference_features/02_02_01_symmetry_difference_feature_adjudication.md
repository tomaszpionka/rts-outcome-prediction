## §1 — Non-materialization disclaimer

This document is a **decision-only adjudication artifact** for SC2EGSet Step 02_02_01 (symmetry \& difference feature scope). It does NOT:

- materialise any feature value (no Parquet under `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`);
- emit any CROSS-02-01 leakage audit (`leakage_audit_sc2egset.{json,md}`);
- modify any STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS YAML;
- modify any research_log / ROADMAP path.

Feature materialisation is a separate future Step 02_02 PR (analogue of PR #259 for Step 02_01_03).

Executed: 2026-05-29. Audit PR: PR #<TBD>.

## §2 — Input artifact lineage (paths + SHA-256)

All SHA-256 values are recomputed on every adjudication run and pinned in the CSV artifact. Parquet SHAs use raw file bytes; audit JSON SHAs use canonical serialisation (`sort_keys=True, separators=(',', ':')`).

| Artifact | Relative path | SHA-256 |
|---|---|---|
| 02_01_02 Parquet | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet` | `24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39` |
| 02_01_03 Parquet | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_features.parquet` | `053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071` |
| 02_01_02 audit JSON | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json` | `1da271c62a20bb2666863fd3737ea4fe6006cc9fec03e41ec11d013fb7e54c78` (canonical) |
| 02_01_03 audit JSON | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.json` | `183b9000d23b5d601b995a61c5ff52aad3fd21ff164bf21f5095fbdf450c9a92` (canonical) |
| Validator module | `src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py` | `d8f34760db2e216cd8b838ab510bd252e7474e0324e4df1bec5d609a293b1753` |

Lineage position: PR #264 (ROADMAP stub) -> PR #265 (Layer-1 scaffold plan) -> PR #266 (Layer-2 scaffold execution + validator) -> PR #267 (Layer-1 adjudication plan) -> THIS PR (Layer-2 adjudication execution; no materialisation)

## §3 — Row identity / alignment policy

The row-identity join keys for the future materialisation step are a documentary future-materialisation gate, not a runtime promise for the adjudication PR.

Join keys (from the 02_01_03 audit JSON `projected_identity_columns` + `projected_context_columns`):

| Key | Role |
|---|---|
| `focal_match_id` | Identity |
| `focal_player` | Identity |
| `opponent_player` | Identity |
| `started_at` | Context anchor (temporal) |

Row alignment policy: join on `focal_match_id + focal_player + opponent_player + started_at` against the 02_01_03 Parquet (44,418 rows × 24 audited features). Every symmetry/difference candidate column is derived purely from the same row's `focal_*` / `opponent_*` values — no cross-row aggregation at materialisation time.

## §4 — Candidate feature table

Total binding candidate count: **33** (F1=10 + F2=10 + F3=10 + F5=3).

> **Note (N3 / LogReg-redundancy of F5):** Under logistic regression with regularisation the F5 `(either, both, xor)` design matrix is rank-2 over the 2-dimensional Boolean source (`either = both ∨ xor`), so two of the three transforms suffice for linear models. The decision to retain all three transforms stands for tree-based models (non-redundant), but the rationale does not claim non-redundancy for all model classes.

| Candidate feature name | Family | Direction | Source columns | Traceability |
|---|---|---|---|---|
| `focal_minus_opponent_prior_match_count_diff` | F1_difference | focal_minus_opponent | focal_prior_match_count + opponent_prior_match_count | traced_to_audited_24_tuple |
| `focal_minus_opponent_prior_win_rate_decisive_diff` | F1_difference | focal_minus_opponent | focal_prior_win_rate_decisive + opponent_prior_win_rate_decisive | traced_to_audited_24_tuple |
| `focal_minus_opponent_days_since_prior_match_diff` | F1_difference | focal_minus_opponent | focal_days_since_prior_match + opponent_days_since_prior_match | traced_to_audited_24_tuple |
| `focal_minus_opponent_prior_win_rate_race_conditional_diff` | F1_difference | focal_minus_opponent | focal_prior_win_rate_race_conditional + opponent_prior_win_rate_race_conditional | traced_to_audited_24_tuple |
| `focal_minus_opponent_prior_win_rate_map_conditional_diff` | F1_difference | focal_minus_opponent | focal_prior_win_rate_map_conditional + opponent_prior_win_rate_map_conditional | traced_to_audited_24_tuple |
| `focal_minus_opponent_prior_win_rate_matchup_conditional_diff` | F1_difference | focal_minus_opponent | focal_prior_win_rate_matchup_conditional + opponent_prior_win_rate_matchup_conditional | traced_to_audited_24_tuple |
| `focal_minus_opponent_apm_prior_mean_diff` | F1_difference | focal_minus_opponent | focal_apm_prior_mean + opponent_apm_prior_mean | traced_to_audited_24_tuple |
| `focal_minus_opponent_sq_prior_mean_diff` | F1_difference | focal_minus_opponent | focal_sq_prior_mean + opponent_sq_prior_mean | traced_to_audited_24_tuple |
| `focal_minus_opponent_supply_capped_pct_prior_mean_diff` | F1_difference | focal_minus_opponent | focal_supply_capped_pct_prior_mean + opponent_supply_capped_pct_prior_mean | traced_to_audited_24_tuple |
| `focal_minus_opponent_elapsed_game_loops_prior_mean_diff` | F1_difference | focal_minus_opponent | focal_elapsed_game_loops_prior_mean + opponent_elapsed_game_loops_prior_mean | traced_to_audited_24_tuple |
| `prior_match_count_pair_mean` | F2_pair_mean | symmetric | focal_prior_match_count + opponent_prior_match_count | traced_to_audited_24_tuple |
| `prior_win_rate_decisive_pair_mean` | F2_pair_mean | symmetric | focal_prior_win_rate_decisive + opponent_prior_win_rate_decisive | traced_to_audited_24_tuple |
| `days_since_prior_match_pair_mean` | F2_pair_mean | symmetric | focal_days_since_prior_match + opponent_days_since_prior_match | traced_to_audited_24_tuple |
| `prior_win_rate_race_conditional_pair_mean` | F2_pair_mean | symmetric | focal_prior_win_rate_race_conditional + opponent_prior_win_rate_race_conditional | traced_to_audited_24_tuple |
| `prior_win_rate_map_conditional_pair_mean` | F2_pair_mean | symmetric | focal_prior_win_rate_map_conditional + opponent_prior_win_rate_map_conditional | traced_to_audited_24_tuple |
| `prior_win_rate_matchup_conditional_pair_mean` | F2_pair_mean | symmetric | focal_prior_win_rate_matchup_conditional + opponent_prior_win_rate_matchup_conditional | traced_to_audited_24_tuple |
| `apm_prior_mean_pair_mean` | F2_pair_mean | symmetric | focal_apm_prior_mean + opponent_apm_prior_mean | traced_to_audited_24_tuple |
| `sq_prior_mean_pair_mean` | F2_pair_mean | symmetric | focal_sq_prior_mean + opponent_sq_prior_mean | traced_to_audited_24_tuple |
| `supply_capped_pct_prior_mean_pair_mean` | F2_pair_mean | symmetric | focal_supply_capped_pct_prior_mean + opponent_supply_capped_pct_prior_mean | traced_to_audited_24_tuple |
| `elapsed_game_loops_prior_mean_pair_mean` | F2_pair_mean | symmetric | focal_elapsed_game_loops_prior_mean + opponent_elapsed_game_loops_prior_mean | traced_to_audited_24_tuple |
| `prior_match_count_pair_abs_diff` | F3_pair_abs_diff | symmetric | focal_prior_match_count + opponent_prior_match_count | traced_to_audited_24_tuple |
| `prior_win_rate_decisive_pair_abs_diff` | F3_pair_abs_diff | symmetric | focal_prior_win_rate_decisive + opponent_prior_win_rate_decisive | traced_to_audited_24_tuple |
| `days_since_prior_match_pair_abs_diff` | F3_pair_abs_diff | symmetric | focal_days_since_prior_match + opponent_days_since_prior_match | traced_to_audited_24_tuple |
| `prior_win_rate_race_conditional_pair_abs_diff` | F3_pair_abs_diff | symmetric | focal_prior_win_rate_race_conditional + opponent_prior_win_rate_race_conditional | traced_to_audited_24_tuple |
| `prior_win_rate_map_conditional_pair_abs_diff` | F3_pair_abs_diff | symmetric | focal_prior_win_rate_map_conditional + opponent_prior_win_rate_map_conditional | traced_to_audited_24_tuple |
| `prior_win_rate_matchup_conditional_pair_abs_diff` | F3_pair_abs_diff | symmetric | focal_prior_win_rate_matchup_conditional + opponent_prior_win_rate_matchup_conditional | traced_to_audited_24_tuple |
| `apm_prior_mean_pair_abs_diff` | F3_pair_abs_diff | symmetric | focal_apm_prior_mean + opponent_apm_prior_mean | traced_to_audited_24_tuple |
| `sq_prior_mean_pair_abs_diff` | F3_pair_abs_diff | symmetric | focal_sq_prior_mean + opponent_sq_prior_mean | traced_to_audited_24_tuple |
| `supply_capped_pct_prior_mean_pair_abs_diff` | F3_pair_abs_diff | symmetric | focal_supply_capped_pct_prior_mean + opponent_supply_capped_pct_prior_mean | traced_to_audited_24_tuple |
| `elapsed_game_loops_prior_mean_pair_abs_diff` | F3_pair_abs_diff | symmetric | focal_elapsed_game_loops_prior_mean + opponent_elapsed_game_loops_prior_mean | traced_to_audited_24_tuple |
| `cross_region_pair_or` | F5_cross_region_pair | symmetric | is_cross_region_fragmented_focal_history_any + is_cross_region_fragmented_opponent_history_any | traced_to_audited_02_01_03_bool_pair |
| `cross_region_pair_and` | F5_cross_region_pair | symmetric | is_cross_region_fragmented_focal_history_any + is_cross_region_fragmented_opponent_history_any | traced_to_audited_02_01_03_bool_pair |
| `cross_region_pair_xor` | F5_cross_region_pair | symmetric | is_cross_region_fragmented_focal_history_any + is_cross_region_fragmented_opponent_history_any | traced_to_audited_02_01_03_bool_pair |


## §5 — Direction policy

Direction policy per `planning/current_plan.md` A9 / Invariant I5:

- **`focal_minus_opponent`** (F1): signed arithmetic difference `focal_col − opponent_col`; name template `focal_minus_opponent_<stem>_diff`. Slot-orthogonal: the sign is meaningful only in the focal-is-row-1 convention (Invariant I5); slot-bias regex enforced by validator.

- **`symmetric`** (F2 / F3 / F5): focal/opponent-swap invariant aggregate (mean, abs_diff, or BOOLEAN transform). Name template `<stem>_pair_mean`, `<stem>_pair_abs_diff`, `cross_region_pair_{or,and,xor}`. Permutation-invariant by construction (Hue \& Vert ICML 2010; Zaheer et al. 2017 Deep Sets).

No canonical-ordering concatenation is used. Slot-bias (player_1 / slot / home / away / etc.) is incompatible with Invariant I5 and enforced by the validator's `BLOCKED_SLOT_TOKEN_REGEX` (12 boundary-aware patterns).

## §6 — Source-column traceability proof

All 10 numeric focal/opponent pairs are sourced from the 02_01_03 audited 24-tuple (`UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03` in the PR #266 validator). All F5 Boolean sources are in the same 24-tuple (`is_cross_region_fragmented_focal_history_any`, `is_cross_region_fragmented_opponent_history_any`).

Plan A20 estimated 11 numeric pairs; the audited 24-tuple yields 10. `matchup_h2h_count` is a single unpaired column (no `opponent` counterpart); `matchup_h2h_focal_win_rate` is also unpaired (B1 / Round 1 BLOCKER: framing it as a pair produces affine `2x−1`, zero information gain for both linear and tree models).

Validator traceability check (PR #266 `_check_source_column_traceability`) passes on every run: every `source_columns` element is in the union of the 7-tuple (02_01_02) and 24-tuple (02_01_03) audited columns.

## §7 — Validator result summary

- `validator_passed`: **True**
- `validator_halting_falsifier`: **None**
- Validator module: `src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py`
- Audit PR: PR #<TBD>

The PR #266 validator runs the 14-step halting-falsifier chain over the candidate specs and the upstream Parquet SHA-256 pins. A `passed=True` result is required for the CSV+MD to be written; if the validator fires any falsifier, the adjudicator raises `SymmetryDifferenceAdjudicationError` before writing any artifact.

## §8 — Race-pair deferral to 02_05

The F6 race-pair categorical interaction family (`race_pair` from the 02_01_02 7-tuple; `focal_race`, `opponent_race`) is deferred to Pipeline Section `02_05 — Categorical Encoding & Interactions` per `planning/current_plan.md` A12 / `02_FEATURE_ENGINEERING_MANUAL.md` §6.

Rationale: race-pair encoded interactions are categorical cross-products, not continuous-valued symmetric/difference transforms. The validator's `designed_race_pair_candidate_specs` parameter is passed as an empty tuple for this adjudication.

No race-pair candidate is emitted in the binding 33-candidate set.

## §9 — Excluded features / families

### §9.1 — `sum` exclusion

The `pair_sum` transform (`focal + opponent`) is excluded as redundant with `pair_mean` (§9.3 cross-links to this). The correct algebra is `sum = focal + opponent = 2 × mean`. Including both `sum` and `mean` in a linear model provides zero additional information (B2 / Round-2 fix). See also §9.3 for the joint-basis argument that places `mean` in the binding set.

### §9.2 — `product` deferral to 02_05

The `pair_product` transform (`focal × opponent`) is deferred to Pipeline Section `02_05 — Categorical Encoding & Interactions`. `product = focal × opponent` is not LINEARLY expressible from `(mean, abs_diff)` alone. The identity `focal × opponent = mean² − (abs_diff / 2)²` makes product a quadratic polynomial in `(mean, abs_diff)`; a linear-LogReg basis cannot recover it without polynomial terms.

`02_FEATURE_ENGINEERING_MANUAL.md` §6 line 135 explicitly acknowledges that tree-based models capture polynomial interactions natively. The placement of `product` in `02_05` is a **Pipeline-Section convention choice** (governance simplicity and interaction-feature grouping), not a methodological necessity. For tree-based models, the `product` interaction is recoverable from the raw `focal_*` / `opponent_*` inputs without an explicit feature; the 02_05 placement groups all multiplicative interactions together for clarity and reusability.

### §9.3 — `abs_diff` inclusion (cross-link to §9.1 and §5)

The `pair_abs_diff` transform (`|focal − opponent|`) is included in the binding set (F3; B3 / Round-2 fix). Cross-referencing §9.1 (`sum` excluded as redundant with `mean`) and §5 (direction policy): the joint triple `(focal_minus_opponent_<stem>_diff, <stem>_pair_mean, <stem>_pair_abs_diff)` jointly spans the **linear-in-signed-difference**, **linear-in-mean-level**, and **linear-in-symmetric-magnitude** subspaces required for LogReg under Invariant I8.

Quadratic effects (`focal²`, `opponent²`, `focal × opponent`) remain unrecoverable without polynomial terms — these are the 02_05 deferral surface (see §9.2). For tree-based models, `|focal − opponent|` is a piecewise-linear function of the signed difference and is recoverable; for LogReg it is not. Therefore `abs_diff` is the canonical symmetric-magnitude basis vector for every eligible numeric focal/opponent pair.

### §9.4 — Ratio family exclusion

excluded_zero_bounded_denominators_unless_log_transform_introduced_in_02_03.

Rationale: ratio features (`focal / opponent`) have zero-bounded denominators in this dataset (e.g., `opponent_prior_match_count = 0` for cold-start cases). Without a log transform introduced at Step 02_03 (Temporal Features, Windows, Decay, Cold Starts), the ratio is undefined or infinite. Deferred until a log transform is available.

### §9.5 — `reconstructed_rating` family exclusion

excluded_per_pr_255_omit_closure.

PR #255 omit-closure binds the exclusion of `reconstructed_rating_focal_pre`, `reconstructed_rating_opp_pre`, `reconstructed_rating_diff`. This adjudication does not re-introduce any reconstructed-rating column. The PR #266 validator's `BLOCKED_FAMILY_FRAGMENTS` constant enforces this structurally.

### §9.6 — Raw MMR scalar exclusion

excluded_per_pr_234_is_mmr_missing_binding_no_new_mmr_scalar.

PR #234 `is_mmr_missing` flag is the only MMR-related signal in the binding 24-tuple. No new raw MMR scalar is introduced. The `is_mmr_missing` BOOLEAN columns are in the 02_01_02 7-tuple, not the 02_01_03 24-tuple, and are not symmetric/difference candidates.

### §9.7 — Matchup-history pair operations exclusion (B1 / A20)

dropped_no_audited_opponent_counterpart_per_b1_round2.

`matchup_h2h_focal_win_rate` is the only matchup-rate column in the audited 24-tuple; there is no `matchup_h2h_opponent_win_rate` counterpart. Treating it as a pair with implicit complement `1 − matchup_h2h_focal_win_rate` produces the affine transform `2·focal − 1` (zero linear-model information gain; zero tree-splitting effect). The F4 family (matchup history pair operations) is therefore dropped entirely. See also §12 for the open unary design question (N4).

### §9.8 — `tracker_events_raw` direct sourcing exclusion

permitted_via_02_01_03_prior_mean_aggregates_only_never_via_tracker_events_raw_direct.

Tracker-derived features are never pre-game features (Invariant I3; CROSS-02-00 §5.4). This adjudication permits only prior-mean aggregates sourced via the 02_01_03 Parquet (which itself sources from `player_history_all`, not from `tracker_events_raw` directly). The PR #266 validator's `_check_tracker_sourced_violations` enforces this.

## §10 — Leakage controls

Temporal leakage controls are inherited from Step 02_01_03 (PR #259):

- Temporal anchor: `started_at` TIMESTAMP (CROSS-02-00 §3.1; PR #242 Q2(a)).
- Cutoff rule: `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at` (strict `<`; Invariant I3).
- Source: 02_01_03 Parquet (44,418 rows; SHA-pinned); no tracker-derived target-match feature.

At adjudication time, no materialisation occurs, so no new leakage falsifiers fire. The validator's halting chain covers:

- `input_parquet_sha_mismatch` — upstream Parquets byte-stable.
- `tracker_sourced_candidate` — no tracker-source prefix in source_columns.
- `target_leak_token_in_candidate` — boundary-aware POST_GAME token regex with `prior_win_rate` allowlist suppression.
- `direction_annotation_invalid` / `direction_name_inconsistent` — name-direction alignment verified.

## §11 — Future materialisation contract

The binding candidate list (33 candidates: F1=10 + F2=10 + F3=10 + F5=3) is the machine-checkable contract for the future Step 02_02 materialisation PR. That PR (analogue of PR #259) must:

1. Accept exactly 33 candidate column names (including 10 difference columns, 10 mean columns, 10 abs_diff columns, 3 cross-region BOOLEAN pair columns).
2. Use the 02_01_03 Parquet as its sole source (SHA-pinned).
3. Apply no new temporal cutoff (inherit strict `<` from 02_01_03).
4. Run the PR #266 validator with the binding specs from this adjudication.
5. Emit a CROSS-02-01 leakage audit JSON+MD pair.
6. Append to the dataset `research_log.md` (non-closure entry).

**Plan A20 note:** Plan A20 estimated 11 numeric pairs; the audited 24-tuple yields 10 (`matchup_h2h_count` is unpaired and excluded per A20). Total estimated 11 + 22 + 3 = 36 candidates from Plan U2; actual total is {total_candidate_count} candidates. This is the resolution of Plan U2 at notebook enumeration step.

## §12 — Out-of-scope disclaimers

The following items are explicitly out of scope for this adjudication PR:

- **No feature value materialised.** No Parquet.
- **No CROSS-02-01 leakage audit artifact.**
- **No STEP_STATUS row for 02_02_01.**
- **No PIPELINE_SECTION_STATUS row for 02_02.**
- **No PHASE_STATUS mutation.** Phase 02 stays `in_progress`.
- **No ROADMAP edit.** The 02_02_01 block (PR #264) remains byte-identical.
- **No research_log append.** (Non-batching sequence step 8; appended at closure.)
- **No Phase 03 / Step 02_01_04 / Step 02_02_02+ / baseline modelling.**
- **No `sum` or `product` transforms.** (B2 / Round-2 / A14: sum excluded redundant; product deferred to 02_05.)
- **No matchup-history pair operations.** (B1 / Round-2 / A20: F4 dropped.)
- **No reconstructed_rating.** (PR #255 omit-closure.)
- **No new MMR scalar.** (PR #234 `is_mmr_missing` flag stands.)
- **No tracker_events_raw direct sourcing.** (Invariant I3.)
- **No AoE2 civilization vocabulary.** (Invariant I8.)
- **No CROSS-02-01 audit artifact.** No `leakage_audit_sc2egset.{json,md}` under `reports/artifacts/02_02_01/`.

**Open design question OQ8 (unary transform — N4):** The potential unary transform `matchup_h2h_focal_advantage = 2·focal_win_rate − 1` rescales the single `matchup_h2h_focal_win_rate` column to `[−1, +1]`. This is an open design question: a unary feature is strictly neither `focal_minus_opponent` (no opponent column in the transform) nor `symmetric` (direction-dependent). No unary candidate is emitted in this adjudication. The decision remains undecided until a future PR (Phase 04 or a follow-up 02_02 micro-PR).

## §13 — Round 2 revision provenance

**Round 1 verdict:** HOLD — 3 BLOCKERs (B1 vacuous F4 pair, B2 algebra error on product redundancy, B3 abs_diff exclusion incompatible with LogReg under I8).

**Round 2 verdict:** APPROVE-WITH-NITS (0 BLOCKERs, 6 NITs). Plan merged via PR #267 (merge SHA `af8c3d98`). Round-2 reviewer-adversarial: `planning/current_plan.critique.md`.

**Blocker resolutions:**

- B1 resolved: F4 (matchup history pair operations) dropped entirely; `MATCHUP_HISTORY_TRANSFORM_DECISION` = `dropped_no_audited_opponent_counterpart_per_b1_round2`. Test: `test_binding_matchup_history_pair_operations_symbol_absent`.

- B2 resolved: Correct algebra `sum = 2 × mean`; `sum` excluded (redundant); `product` deferred to 02_05 (genuine multiplicative interaction). `SYMMETRIC_PAIR_AGGREGATE_SCOPE_DECISION` encodes both decisions. Test: `test_no_pair_sum_candidate_constructed` + `test_no_pair_product_candidate_constructed`.

- B3 resolved: `abs_diff` included as F3 family; `BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS = ("mean", "abs_diff")`. Test: `test_binding_symmetric_pair_aggregate_transforms_exactly_mean_abs_diff`.

**Nit applications (N1–N6):**

- **N1** (MD §9.2): Wording corrected to "not LINEARLY expressible from `(mean, abs_diff)` alone" (quadratic identity `focal × opponent = mean² − (abs_diff/2)²`).

- **N2** (MD §9.2): `02_FEATURE_ENGINEERING_MANUAL.md` §6 line 135 cited; Pipeline-Section placement acknowledged as convention choice, not methodological necessity.

- **N3** (MD §4 footnote): LogReg-redundancy of F5 `(either, both, xor)` acknowledged (rank-2 design matrix over 2-dim Boolean source); all three retained for tree models.

- **N4** (MD §12): Unary `matchup_h2h_focal_advantage = 2·focal − 1` recorded as open design question OQ8; no candidate emitted.

- **N5** (internal consistency): Deterministic assertion `count(abs_diff specs) == len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS) == CSV binding_difference_family_numeric_pair_count`. Tests: `test_internal_consistency_abs_diff_count_equals_constant_equals_csv_field` and `test_internal_consistency_total_candidate_count_matches_csv_field`.

- **N6** (MD §9.3): Joint-basis cross-link added: `(focal_minus_opponent_diff, pair_mean, pair_abs_diff)` spans linear-in-signed-difference, linear-in-mean-level, and linear-in-symmetric-magnitude; quadratic effects remain at 02_05.

