---
title: "SC2EGSet Step 02_02_01 symmetry/difference feature materialization + non-vacuous leakage audit (Layer-1 planning PR)"
category: A
branch: feat/sc2egset-02-02-01-symmetry-difference-materialization
base_ref: master
base_sha: b84ed6d6bf89414d33b7a1b9ee05f34e82d00457
predecessor_pr: 268
predecessor_pr_merge_sha: b84ed6d6bf89414d33b7a1b9ee05f34e82d00457
dataset: sc2egset
phase: "02"
pipeline_section: "02_02 — Symmetry & Difference Features"
invariants_touched: [I3, I5, I6, I7, I8, I9, I10]
draft_pr_files:
  - planning/current_plan.md
  - planning/current_plan.critique.md
future_execution_files:
  - src/rts_predict/games/sc2/datasets/sc2egset/materialize_symmetry_difference_features.py
  - tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_symmetry_difference_features.py
  - sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.py
  - sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.ipynb
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_features.parquet
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_02_01/leakage_audit_sc2egset.json
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_02_01/leakage_audit_sc2egset.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
  - planning/INDEX.md
  - CHANGELOG.md
  - pyproject.toml
future_execution_file_count: 11
target_version_bump: "3.85.0 -> 3.86.0"
critique_required: true
research_log_ref: null
date: 2026-05-30
---

## Scope

Execute `.claude/rules/data-analysis-lineage.md` "Non-batching rule for
empirical work" sequence steps 7 ("Only after all validation modules pass,
generate artifacts") and 8 ("Then research_log") in their materialization
specialisation. Precedent ladder: PR #235 (Layer-1 materialization plan) →
PR #236 (Layer-2 materialization execution + CROSS-02-01 audit) for Step
02_01_02; PR #258 (Layer-1 materialization plan) → PR #259 (Layer-2
materialization execution + CROSS-02-01 audit) for Step 02_01_03. PR #268
(merged 2026-05-29 at master `b84ed6d6bf89414d33b7a1b9ee05f34e82d00457`)
delivered the binding adjudication CSV+MD recording the 33-candidate feature
contract. The next atomic unit is the **actual feature value materialization**
plus the **post-materialization non-vacuous leakage audit** (CROSS-02-01-v1.0.1
§3 — `features_audited` enumerates the 33 emitted feature columns by name).

**Two-PR sequence on branch
`feat/sc2egset-02-02-01-symmetry-difference-materialization`.**

1. **THIS Layer-1 planning PR** writes only two files:
   - `planning/current_plan.md` (this document);
   - `planning/current_plan.critique.md` (reviewer-adversarial output).
2. **FUTURE Layer-2 execution PR on the same branch** performs the 11-file
   manifest below (materialization module + mirrored test + jupytext notebook
   pair (overwriting the PR #266 scaffold notebook in place) + Parquet + audit
   JSON + audit MD + dataset `research_log.md` non-closure append +
   `pyproject.toml` + `planning/INDEX.md` + `CHANGELOG.md`).

**Explicitly out of scope** for both PRs (this PR and the future Layer-2 PR):

- a second adjudication artifact pair (the PR #268 CSV+MD remains
  byte-identical; the materialization module imports the binding constants
  from `adjudicate_symmetry_difference_feature_scope.py` rather than
  re-declaring them);
- STEP_STATUS.yaml `02_02_01` row addition (closure deferred to a future
  U2.B-style PR analogous to PR #237 / PR #262 post-materialisation);
- PIPELINE_SECTION_STATUS.yaml `02_02` row addition (deferred per PR #230
  precedent — section row first lands at step closure, not at materialization);
- PHASE_STATUS.yaml mutation (Phase 02 stays `in_progress`; Phase 03 stays
  `not_started`);
- ROADMAP.md body edits (the `02_02_01` block at lines 2853–3131 remains
  byte-identical);
- root `reports/research_log.md` edit (per per-dataset-only research_log
  scoping; PR #259 precedent);
- thesis chapters, bib, appendix, `docs/**`, `.claude/**`, `data/**`;
- any AoE2 path under `src/rts_predict/games/aoe2/**`;
- Step `02_02_02+`; Step `02_01_04`; Phase 03; any baseline modeling;
- reopen of Q5 / Q6 / Q6F / Q6G / Q6H / `reconstructed_rating` closure;
- a new MMR scalar feature (PR #234 `is_mmr_missing` flag precedent stands);
- a new tracker-derived target-match feature (Invariant I3);
- AoE2 `civilization` vocabulary in any SC2EGSet artifact;
- any matchup-history pair operation (B1 ban from PR #267 / PR #268 stands);
- the `sum`, `product`, and `ratio` transforms over numeric focal/opponent
  pairs (per PR #268 `SUM_TRANSFORM_DECISION` / `PRODUCT_TRANSFORM_DECISION`
  / `RATIO_FAMILY_DECISION`);
- unary `2x − 1` rescaling over `matchup_h2h_focal_win_rate` (per PR #268
  `UNARY_TRANSFORM_DECISION = open_design_question`).

## Problem Statement

PR #268 produced the binding source-anchor / column-naming / direction-policy
adjudication: one CSV + one MD recording the 33-candidate feature contract
(`02_02_01_symmetry_difference_feature_adjudication.{csv,md}`). The module
`adjudicate_symmetry_difference_feature_scope.py` exports the binding
constants:

- `BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS` (10 `(focal_*, opponent_*)`
  tuples sourced from the 02_01_03 audited 24-tuple);
- `BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS = ("mean", "abs_diff")`;
- `BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES =
  ("is_cross_region_fragmented_focal_history_any",
   "is_cross_region_fragmented_opponent_history_any")`;
- `BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS = ("either", "both", "xor")`;
- `ROW_IDENTITY_JOIN_KEYS = ("focal_match_id", "focal_player",
  "opponent_player", "started_at")`.

These constants pin the future materialisation contract:
**33 feature columns** = 10 F1 (`focal_minus_opponent_<stem>_diff`) + 10 F2
(`<stem>_pair_mean`) + 10 F3 (`<stem>_pair_abs_diff`) + 3 F5
(`cross_region_pair_{or,and,xor}`); plus 3 identity columns
(`focal_match_id`, `focal_player`, `opponent_player`) + 1 context column
(`started_at`) = **37 total Parquet columns**.

Without a materialisation+audit PR that:

1. emits a Parquet artifact with exactly 37 columns and exactly 44,418 rows
   (matching the 02_01_03 audit's `row_count` and `distinct_focal_match_count
   = 22209`);
2. computes each feature column per its family rule (F1 signed subtraction;
   F2 arithmetic mean; F3 absolute difference; F5 Boolean `OR`/`AND`/`XOR`);
3. enforces row-identity alignment on
   `(focal_match_id, focal_player, opponent_player, started_at)` against the
   02_01_03 Parquet (one-to-one row alignment);
4. emits a non-vacuous CROSS-02-01-v1.0.1 §3 leakage audit JSON+MD whose
   `features_audited` enumerates the **exact 33 emitted feature column names**
   in deterministic order and proves each traces to the audited 7-tuple /
   24-tuple via the PR #268 adjudication contract;
5. proves byte-deterministic re-write (two consecutive runs produce
   byte-identical Parquet under fixed Parquet writer settings);
6. does not mutate any parent artifact (02_01_02 Parquet, 02_01_03 Parquet,
   their audit JSONs, the PR #268 CSV/MD, the PR #266 validator module);
7. appends a non-closure `research_log.md` entry recording `closure_status:
   still_open` / `materialization_state: materialized` /
   `leakage_audit_state: post_materialization_pass`;

the PR #268 adjudication remains a decision record without a corresponding
materialised feature artifact, and the Step 02_02 pipeline section cannot
progress toward closure.

This PR is the analogue of PR #258 → PR #259 for Step 02_01_03 (8-decision
adjudication → 24-feature materialization+audit), now applied to the
33-decision adjudication produced by PR #268.

## Literature Context

**Manual binding (must justify each cited).** Per `.claude/rules/data-analysis-
lineage.md` §"Feature-engineering discipline," each feature family in the
materialised output must already declare dataset, source table/event family,
prediction setting, feature table grain, temporal anchor, allowed cutoff rule,
leakage falsifier, cold-start behavior, and lineage artifact. The PR #268
adjudication CSV+MD discharges these declarations per-candidate at the spec
layer; this materialisation PR proves each declaration empirically at the
row layer.

`02_FEATURE_ENGINEERING_MANUAL.md` §3 lines 43–59 ("Symmetry in Pairwise
Prediction Demands Difference Features") establishes the Bradley-Terry
connection (Bradley & Terry 1952): for latent strengths β_i,
`P(i > j) = 1 / (1 + e^(β_j − β_i))`, so the logit of win probability equals
the **difference** of latent strengths. Line 51: "difference features … are
preferred for most models." This PR materialises F1 as the signed difference
`focal − opponent` per the manual default; the symmetric companions F2/F3
provide the magnitude / centre-of-mass basis required for Invariant I8's
LogReg cross-game constraint.

**Invariant I8 binds LogReg into the cross-game protocol (B3 anchor from PR
#267).** `.claude/scientific-invariants.md` Invariant I8 (lines 197–214)
requires LogReg, random forest, and gradient boosted trees on both SC2 and
AoE2. For LogReg the model is `logit P(focal wins) = w₀ + Σ w_k · φ_k(x_focal,
x_opponent)`. The PR #267 / PR #268 Round-2 anchor proves that `|focal −
opponent|` is NOT a linear function of `(focal − opponent)`, so the
materialisation MUST emit both F1 (`<stem>_diff`) and F3 (`<stem>_pair_abs_diff`)
for every numeric pair to give LogReg a symmetric-magnitude basis. F2
(`<stem>_pair_mean`) provides the centre-of-mass term: the joint basis
`(F1, F2, F3)` spans linear-in-signed-difference, linear-in-level, and
linear-in-symmetric-magnitude. Quadratic / product interactions remain the
02_05 deferral surface per PR #268 `PRODUCT_TRANSFORM_DECISION`.

`.claude/scientific-invariants.md` Invariant I5 (lines 156–170) binds: "The
model input is always structured as `(focal_player_features, opponent_features,
context_features)` and this structure is identical regardless of which player
is focal." The materialisation enforces I5 at the row layer: every F1
candidate is computed as `focal_col − opponent_col` (slot-orthogonal in the
focal-is-row-1 convention); F2/F3/F5 are computed as permutation-invariant
aggregates (mean / abs_diff / Boolean transforms). Hue & Vert (ICML 2010)
"On Learning with Kernels for Unordered Pairs" and Zaheer et al. (2017)
"Deep Sets" both ground symmetric aggregation as the canonical
permutation-invariant construction.

**Invariant I3 binds the temporal anchor unchanged.** The strict-`<` history
filter `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at` was applied
upstream in 02_01_03; every symmetry/difference transform is row-preserving
over the same `started_at` per row, so the cutoff is inherited unchanged. No
new temporal filter is introduced at the 02_02 layer.

**No new threshold (Invariant I7).** All 33 feature definitions are
algebraic transforms of two parent columns each; no thresholds, no rolling
windows, no cold-start defaults, no encoder fits. Every constant in the
materialisation module (column names, transform symbols, family tags) is
imported from `adjudicate_symmetry_difference_feature_scope.py` or declared
as a module-level UPPER_SNAKE constant with derivation comments.

## Assumptions & Unknowns

**A1. Predecessor merge SHA.** PR #268 merged at master
`b84ed6d6bf89414d33b7a1b9ee05f34e82d00457`. Layer-2 T01 must verify
`git rev-parse master` matches this SHA before construction.

**A2. pyproject version baseline.** `pyproject.toml` declares `version =
"3.85.0"`. Layer-2 target bump: `3.85.0 → 3.86.0` (minor per
`.claude/rules/git-workflow.md`: feat-class → minor; matches PR #259
precedent `3.81.0 → 3.82.0`).

**A3. 02_01_02 Parquet SHA-256 pin.**
`24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39` (from PR
#268 CSV). Layer-2 module recomputes and asserts equality.

**A4. 02_01_03 Parquet SHA-256 pin.**
`053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071` (from PR
#268 CSV). Layer-2 module recomputes and asserts equality.

**A5. 02_01_02 audit JSON canonical SHA-256 pin.**
`1da271c62a20bb2666863fd3737ea4fe6006cc9fec03e41ec11d013fb7e54c78` (canonical
serialisation = `json.dumps(obj, sort_keys=True, separators=(',', ':'))`
then SHA-256 of UTF-8 bytes).

**A6. 02_01_03 audit JSON canonical SHA-256 pin.**
`183b9000d23b5d601b995a61c5ff52aad3fd21ff164bf21f5095fbdf450c9a92`.

**A7. PR #268 adjudication CSV / MD SHA-256 pins.** Layer-2 T01 computes
both via raw-bytes SHA-256 at the start of the materialisation run and pins
them in the audit JSON `adjudication_artifact_sha256s` map. The pinned values
must match the on-disk files; mismatch is a halting falsifier.

**A8. Validator module SHA-256 pin.**
`d8f34760db2e216cd8b838ab510bd252e7474e0324e4df1bec5d609a293b1753` (from PR
#268 CSV `validator_module_sha256`). The PR #266 validator is read-only at
this layer.

**A9. Row count alignment (Round 1 / N2 corrected — defence-in-depth).** Two
independent assertions must both pass:

1. **Module-level constant pins** (precedent: PR #259's
   `EXPECTED_OUTPUT_ROW_COUNT: int = 44_418` at
   `materialize_history_enriched_pre_game_features.py:115`).
   - `EXPECTED_OUTPUT_ROW_COUNT: int = 44_418`
   - `EXPECTED_DISTINCT_FOCAL_MATCH_COUNT: int = 22_209`
2. **Runtime equality vs the 02_01_03 audit JSON** loaded at module init —
   assert `expected == audit_json['row_count']` AND
   `expected == audit_json['distinct_focal_match_count']`. If the audited
   value drifts (which would mean a 02_01_03 closure-ban violation upstream),
   both falsifier 12 (`output_row_count_drift`) AND falsifier 22
   (`audit_pinned_row_count_drift`) fire.

The output Parquet row count MUST equal both the module constant AND the
audited input row count. The two checks together prevent silent upstream
drift from passing through the materialisation gate.

**A10. Row-identity join keys.** The 4-tuple
`(focal_match_id, focal_player, opponent_player, started_at)` is the inner
join key. The 02_01_03 Parquet already has these as the row identity per
its own audit; this PR materialises the symmetry/difference candidates as
row-preserving transforms (no cross-row aggregation, no join semantics
beyond inheriting the upstream row identity).

**A11. Deterministic column order.** The 37-column output schema order is:
3 identity (in `ROW_IDENTITY_JOIN_KEYS` order minus `started_at`), 1 context
(`started_at`), then 33 features in F1 → F2 → F3 → F5 family order; within
each numeric family the order follows
`BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS`'s tuple order; F5 follows
`BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS`'s `(either, both, xor)` order
emitted as `cross_region_pair_or`, `cross_region_pair_and`,
`cross_region_pair_xor` (per validator's symmetric-token vocabulary
`{or, and, xor}`).

**A12. Deterministic row order.** The output Parquet row order MUST match
the 02_01_03 Parquet row order (no shuffle, no re-sort). This guarantees
byte-deterministic re-write.

**A13. NaN propagation.** For F1/F2/F3 numeric transforms, NaN in either
parent column propagates to NaN in the result (pandas default for arithmetic
operations). For F5 Boolean transforms, the source columns are non-nullable
Boolean per the 02_01_03 schema (`pq.read_schema` confirms `bool` not
`bool?`), so NaN cannot arise.

**A14. Parquet writer determinism (Round 1 / N4 corrected).** Use a fixed
Parquet writer configuration to guarantee byte-deterministic output AND
preserve dataset-wide encoding consistency with PR #259:
- `compression='zstd'` (matches PR #259's `COMPRESSION 'ZSTD'` via DuckDB
  COPY at `materialize_history_enriched_pre_game_features.py:1041–1052`;
  PyArrow's zstd encoder is deterministic; preserves cross-step audit
  consistency. Round 1 reviewer-adversarial N4 flagged the original `'snappy'`
  proposal as a precedent divergence; corrected here.);
- `version='2.6'` (deterministic);
- `data_page_version='2.0'` (deterministic);
- no statistics randomisation;
- column chunk write order matches DataFrame column order.
Layer-2 T01 must verify byte equality across two consecutive runs. The
`use_dictionary=False` override (OQ2) is defer-and-measure: T01 runs the
materialisation twice, hashes both Parquets, asserts equality; if unequal,
T01 adds the explicit override and re-runs.

**A15. No parent-mutation gate.** The Layer-2 module computes SHA-256 of
each parent artifact at the START of the run AND at the END, asserts
equality. If any parent SHA changes mid-run, the audit verdict is `FAIL`
and a halting falsifier `no_parent_mutation_check_failed` fires.

**A16. No status-YAML mutation.** Layer-2 T01 verifies (via `git diff --name-only`
in the test fixture sense; module-level assert) that the Layer-2 PR does NOT
modify `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, or
`PHASE_STATUS.yaml`. This is a Layer-2 test, not a runtime falsifier.

**A17. No ROADMAP mutation.** Same as A16 for `ROADMAP.md`.

**A18. F4 absence.** No `matchup_h2h_*_pair_*` column may be emitted (per
PR #268 `MATCHUP_HISTORY_TRANSFORM_DECISION = dropped_no_audited_opponent_counterpart`).
Layer-2 test asserts no emitted column matches the regex
`^matchup_h2h_.*_pair_(mean|abs_diff|sum|product|or|and|xor)$`.

**A19. F6 race-pair absence.** No race-pair categorical column may be
emitted (per PR #268 `RACE_PAIR_DECISION = defer_to_02_05`). Layer-2 test
asserts no emitted column matches `^race_pair_` or
`^.*race.*_pair_(mean|abs_diff|or|and|xor)$`.

**A20. No reconstructed_rating column.** Layer-2 test asserts no emitted
column matches `reconstructed_rating` (per PR #255 omit-closure).

**A21. No civilization vocabulary.** Layer-2 test asserts no emitted column
or audit prose contains the string `civilization` (Invariant I8 cross-game
hygiene; SC2EGSet uses `race` exclusively).

**A22. Coverage target.** Layer-2 mirrored test file targets ≥ 95% branch
coverage on `materialize_symmetry_difference_features.py` (matches PR #259's
95.04% precedent) and ≥ 40 distinct test cases. PR #259 had 175 tests; this
materialisation is structurally simpler (no SQL CTE chain) so 40 is a floor,
not a ceiling.

**Unknowns** (resolved at Layer-2 T01, not at Layer-1):

- **U1.** The exact line count of the materialisation module. PR #259 was
  2219 lines because of its 24-feature SQL CTE chain; this module is pure
  pandas/PyArrow over an existing Parquet, so the lower-bound estimate is
  ~600–1000 lines.
- **U2.** Whether the Parquet writer needs explicit `use_dictionary=False`
  to guarantee byte determinism on Boolean columns. Layer-2 T01 verifies
  empirically; if the default produces byte-identical output across runs,
  no override needed.
- **U3.** The exact set of additional `custom_extensions` fields in the
  audit JSON (beyond the CROSS-02-01-v1.0.1 §3 spec). PR #259's audit JSON
  used 16 custom fields including `feature_to_family_mapping`. This PR's
  audit needs at minimum `per_feature_traceability`,
  `adjudication_artifact_sha256s`, and
  `binding_difference_family_numeric_pair_count`; exact final set is a
  Layer-2 decision recorded in the audit JSON itself.

## Execution Steps

The future Layer-2 PR executes the following tasks on branch
`feat/sc2egset-02-02-01-symmetry-difference-materialization` based off
`master@b84ed6d6`. Each task is a delegated executor step with stop
conditions per `.claude/rules/data-analysis-lineage.md`.

**T01 — Materialisation module + mirrored test (Sonnet executor + Opus
guidance for the per-family computation rules).**

Files (allowed):
- `src/rts_predict/games/sc2/datasets/sc2egset/materialize_symmetry_difference_features.py`
  (NEW; ~600–1000 lines target);
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_symmetry_difference_features.py`
  (NEW; ≥ 40 tests, ≥ 95% branch coverage).

Files (forbidden):
- any path under `src/rts_predict/games/sc2/datasets/sc2egset/reports/`;
- `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml`;
- `ROADMAP.md`;
- `pyproject.toml` / `CHANGELOG.md` / `planning/INDEX.md`;
- any sandbox notebook;
- any `02_01_02` / `02_01_03` / PR #268 artifact;
- any path under `src/rts_predict/games/aoe2/`;
- root `reports/research_log.md`.

Module public API (frozen contract — see "Future module shape" below):
- `@dataclass(frozen=True) class SymmetryDifferenceMaterializationResult`
  with attributes listed below;
- `def run_symmetry_difference_feature_materialization(*, repo_root, ...)
  -> SymmetryDifferenceMaterializationResult`.

Imports from adjudicator (do NOT re-declare):
- `BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS`
- `BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS`
- `BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES`
- `BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS`
- `ROW_IDENTITY_JOIN_KEYS`

Computation rules (per family — verbatim formulas, no paraphrase):
- **F1 — `focal_minus_opponent_<stem>_diff`** for each
  `(focal_col, opponent_col)` in `BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS`:
  `df[name] = df[focal_col] - df[opponent_col]`. Stem derivation:
  `stem = focal_col.removeprefix("focal_")` (e.g.,
  `focal_prior_match_count → prior_match_count`).
- **F2 — `<stem>_pair_mean`** for each numeric pair:
  `df[name] = (df[focal_col] + df[opponent_col]) / 2.0`.
- **F3 — `<stem>_pair_abs_diff`** for each numeric pair:
  `df[name] = (df[focal_col] - df[opponent_col]).abs()`.
- **F5 — `cross_region_pair_or/and/xor`** over the Boolean source pair
  `(is_cross_region_fragmented_focal_history_any,
   is_cross_region_fragmented_opponent_history_any)`:
  `df["cross_region_pair_or"] = df[focal_bool] | df[opponent_bool]`;
  `df["cross_region_pair_and"] = df[focal_bool] & df[opponent_bool]`;
  `df["cross_region_pair_xor"] = df[focal_bool] ^ df[opponent_bool]`.

Halting falsifier chain (first non-PASS halts; raises
`SymmetryDifferenceMaterializationError`; suppresses Parquet+audit emission):
1. `validator_module_sha_pin_mismatch` (A8);
2. `parent_parquet_02_01_02_sha_mismatch` (A3);
3. `parent_parquet_02_01_03_sha_mismatch` (A4);
4. `parent_audit_02_01_02_canonical_sha_mismatch` (A5);
5. `parent_audit_02_01_03_canonical_sha_mismatch` (A6);
6. `adjudication_csv_sha_mismatch` (A7);
7. `adjudication_md_sha_mismatch` (A7);
8. `binding_numeric_pair_count_drift` (`len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS)
   != 10`);
9. `binding_symmetric_pair_aggregate_transforms_drift`
   (`BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS != ("mean", "abs_diff")`);
10. `binding_cross_region_pair_transforms_drift`
    (`BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS != ("either", "both", "xor")`);
11. `source_column_missing_in_02_01_03_parquet` (any source column from
    `BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS` or
    `BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES` not in
    `pq.read_schema(...).names`);
12. `output_row_count_drift` (≠ 44418);
13. `output_distinct_focal_match_count_drift` (≠ 22209);
14. `output_feature_column_count_drift` (≠ 33);
15. `output_total_column_count_drift` (≠ 37);
16. `identity_columns_not_byte_identical_to_02_01_03` (identity tuple
    `(focal_match_id, focal_player, opponent_player, started_at)` per row
    must equal the upstream Parquet row-for-row);
17. `forbidden_token_in_emitted_column_name` (regex sweep over the 33
    feature names: must not match `slot|player_1|player_2|home|away|p1|p2`
    boundary-aware OR `civilization` OR `reconstructed_rating` OR
    `matchup_h2h_.*_pair_` OR `_race_pair_`);
18. `parent_mutation_detected` (A15 — parent SHA at end ≠ parent SHA at start);
19. `audit_verdict_not_pass`;
20. `non_deterministic_re_write` (second run produces byte-different
    Parquet);
21. `per_feature_traceability_proof_failed` (each of the 33 features must
    map to either the 24-tuple via the adjudicator constants or to the
    bool-pair sources).

Test groups (≥ 40 tests, mapped to existing PR #266 / PR #268 test-naming
conventions):
- Module structure (5+ tests): public dataclass attribute set; public
  function signature; constants re-exported only as imports; no duplicate
  constant declarations.
- Binding-constant-import (4 tests): each of the 5 imported names is
  re-bound from the adjudicator module and equality-checked against the
  adjudicator's own value.
- Source-column traceability (10 tests, one per numeric pair + 1 for
  bool pair): each source column appears in the audited 24-tuple from the
  02_01_03 audit JSON.
- Per-family computation (12 tests): one synthetic-row test per family ×
  smallest representative pair (F1 sign, F2 average, F3 magnitude, F5
  truth-table for each of `OR`/`AND`/`XOR`).
- Output Parquet schema (3 tests): 37 column names; column dtypes
  (int64/double/bool); column order matches A11.
- Row count + distinct focal count (2 tests): equal to 44418 / 22209.
- Identity alignment (2 tests): row-by-row identity-tuple equality to
  02_01_03 Parquet on first 100 rows + last 100 rows (cheap sampling
  fixture).
- Leakage audit shape (5 tests): JSON keys per spec §3; MD has all 7
  required §-sections; `verdict == "PASS"`; `features_audited` has length
  33; `features_audited` list equals the deterministic A11 order.
- Per-feature traceability proof (1 test): all 33 entries in
  `per_feature_traceability` reference parent columns in
  `BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS` ∪
  `BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES`.
- Forbidden token absence (4 tests): regex sweep for `civilization`,
  `reconstructed_rating`, `matchup_h2h_.*_pair_`, slot-bias regex.
- Parent SHA invariance (4 tests): SHA of each parent artifact at end of
  run equals SHA at start.
- Determinism (1 test): second consecutive run produces byte-identical
  Parquet (hash both).
- Negative-path tests (3 tests): mutated parent SHA → halting falsifier;
  wrong row count synthetic input → halting falsifier; emitted column
  count ≠ 33 → halting falsifier.

T01 stop condition: pytest passes ≥ 95% branch coverage on the new module;
no edits to forbidden files; no Parquet / audit / status YAML / ROADMAP /
research_log / pyproject / CHANGELOG / INDEX touched yet.

T01 validation report (required from executor):
- count of new tests added;
- coverage percentage reported by pytest-cov;
- list of all halting falsifier names implemented;
- assertion that no forbidden file was touched.

**T02 — Sandbox notebook overwrite (Sonnet executor).**

Files (allowed):
- `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.py`
  (OVERWRITE the PR #266 scaffold file in place — precedent: PR #259
  overwrote the PR #241 scaffold notebook);
- `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.ipynb`
  (OVERWRITE; jupytext-paired regeneration).

Files (forbidden — explicit ban):
- `02_02_01_symmetry_difference_feature_adjudication.py` and `.ipynb` (the
  PR #268 adjudication notebook is NOT overwritten; these belong to PR
  #268 and remain byte-identical);
- any other file from T01 or T03–T05.

Notebook contract (matches PR #259 notebook pattern):
- markdown header with hypothesis, falsifier, sanity check, expected
  artifact, lineage source, downstream decision;
- one cell calling
  `run_symmetry_difference_feature_materialization(repo_root=Path.cwd())`;
- one cell printing the result dataclass (`feature_column_names`,
  `row_count`, `distinct_focal_match_count`, `validator_passed`,
  `leakage_audit_verdict`);
- one cell printing the 33-feature column names and their family tags;
- one cell printing first 5 rows of the output Parquet for visual sanity
  (sandbox-only; not used downstream).

T02 stop condition: jupytext-pair produces matching `.py` ↔ `.ipynb`; notebook
runs end-to-end (executor records elapsed time); no edits to forbidden
files.

**T03 — Parquet + audit JSON + audit MD generation (Opus execution —
load-bearing methodology).**

Files (allowed):
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_features.parquet`
  (NEW);
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_02_01/leakage_audit_sc2egset.json`
  (NEW; also creates the `02_02_01/` directory);
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_02_01/leakage_audit_sc2egset.md`
  (NEW).

Files (forbidden):
- the PR #268 adjudication CSV/MD;
- the 02_01_02 and 02_01_03 audit JSONs and Parquets;
- the validator module;
- the materialisation module from T01 (no edits after tests pass);
- any other file from T01, T02, T04, T05.

Execution: run T02 notebook in the executor session via
`source .venv/bin/activate && poetry run jupyter nbconvert --to notebook
--execute …`. Verify:
- Parquet exists; row count = 44418; column count = 37; dtypes per A13;
  deterministic re-write under A14;
- audit JSON conforms to the "Future leakage audit JSON requirements"
  section below;
- audit MD has all 7 §-sections per "Future audit MD" below;
- per-feature traceability list has length 33 and references only the 10
  numeric pairs + 1 Boolean pair source set;
- no parent file mutated (re-hash all parents and assert equality).

T03 stop condition: all three artifacts on disk; halt falsifier list in
audit JSON is empty; audit JSON `verdict == "PASS"`; second-run byte-equal
Parquet asserted by executor.

T03 validation report: SHA-256 of the Parquet; SHA-256 (canonical) of the
audit JSON; SHA-256 of the audit MD; row count; distinct focal match count;
sample 3 rows from the output (for human visual sanity).

**T04 — dataset `research_log.md` non-closure append (Sonnet executor).**

Files (allowed):
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
  (APPEND-ONLY; preserves PR #259 PR-#262 closure entries byte-shifted only).

Files (forbidden):
- root `reports/research_log.md`;
- any other file.

Append-block format (Round 1 / N5 corrected — mirrors PR #259's actual
Markdown bold-label entry at `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md:79–103`,
NOT a YAML block):

```markdown
## 2026-MM-DD — Materialize Step 02_02_01 symmetry/difference 33-feature contract + non-vacuous CROSS-02-01 audit

- **Category:** A (science / Phase 02 / materialization-execution)
- **Dataset:** sc2egset
- **Branch:** `feat/sc2egset-02-02-01-symmetry-difference-materialization`
- **PR:** `PR #<TBD>`
- **Step scope:** Step `02_02_01` — symmetry/difference feature materialisation for the 33 binding candidates authorised by PR #268 adjudication: F1 (10 numeric differences `focal_minus_opponent_<stem>_diff`) + F2 (10 symmetric pair means `<stem>_pair_mean`) + F3 (10 symmetric pair absolute differences `<stem>_pair_abs_diff`) + F5 (3 cross-region Boolean pair transforms `cross_region_pair_{or,and,xor}`). F4 (matchup history pair operations) DROPPED per B1 / PR #268 A20. F6 (race-pair categorical interactions) DEFERRED to 02_05 per PR #268 A12. `sum` EXCLUDED redundant; `product` DEFERRED to 02_05; `ratio` EXCLUDED; `reconstructed_rating` EXCLUDED per PR #255 omit-closure. Step closure is NOT claimed; closure flips are deferred to a separate U2.B-style PR per PR #237 / PR #262 precedent.
- **closure_status:** `still_open`
- **materialization_state:** `materialized`
- **leakage_audit_state:** `post_materialization_pass`
- **features_audited_count:** `33`
- **row_count:** `44418`
- **distinct_focal_match_count:** `22209`
- **artifact:** `02_02_01_symmetry_difference_features.parquet`
- **leakage_audit:** `reports/artifacts/02_02_01/leakage_audit_sc2egset.{json,md}`
- **What:** Persisted the Layer-2 deliverable authorised by merged PR #268 binding adjudication: (i) one Parquet feature table at the canonical reports path carrying 44418 rows × 37 projected columns — partitioned as 3 IDENTITY (`focal_match_id`, `focal_player`, `opponent_player`), 1 CONTEXT row-identity anchor (`started_at`), and 33 audited symmetry/difference feature columns in deterministic F1→F2→F3→F5 order; (ii) the FIRST non-vacuous CROSS-02-01-v1.0.1 post-materialization audit pair at `reports/artifacts/02_02_01/leakage_audit_sc2egset.{json,md}` with `features_audited` = exactly the 33 emitted feature column names, `verdict = PASS`, `future_leak_count = 0`, `post_game_token_violations = 0`, full SHA-256 provenance bonds for the parent artifacts (02_01_02 + 02_01_03 Parquets, 02_01_02 + 02_01_03 audit JSONs canonical, PR #268 adjudication CSV+MD, PR #266 validator module, materialisation module), per-feature traceability table proving each of the 33 columns derives from the audited 02_01_03 24-tuple (10 numeric pairs) or the audited Boolean cross-region pair, and the row-identity alignment proof against the 02_01_03 Parquet.
- **Why:** Discharges PR #268 adjudication's "decision-only" annotation by proving the contract on disk. The CROSS-02-01 §5 gate condition is now mechanically satisfied for Step `02_02_01`. Materialisation contract: F1 = signed `focal − opponent` (Bradley-Terry default per `02_FEATURE_ENGINEERING_MANUAL.md` §3); F2 = `(focal + opponent) / 2` (centre-of-mass symmetric aggregate); F3 = `|focal − opponent|` (LogReg symmetric-magnitude basis per Invariant I8); F5 = Boolean OR/AND/XOR over the cross-region indicator pair (point-indicator family per PR #268 A13).
- **How (reproducibility):** notebook at `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.{py,ipynb}` (jupytext py:percent canonical; PR #266 scaffold overwritten in place per `sandbox/README.md` single-notebook-per-Step contract); materialisation module at `src/rts_predict/games/sc2/datasets/sc2egset/materialize_symmetry_difference_features.py` carrying the public `run_symmetry_difference_feature_materialization(...)` entrypoint and the frozen `SymmetryDifferenceMaterializationResult` dataclass; tests at `tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_symmetry_difference_features.py` (≥40 named tests; ≥95% branch coverage on the materialisation module); module imports binding constants from `adjudicate_symmetry_difference_feature_scope.py` (no re-declaration); 22-step halting falsifier chain (SHA pins → count drifts → identity alignment → forbidden tokens → parent mutation → audit verdict → determinism); Parquet writer `compression='zstd'`, `version='2.6'`, `data_page_version='2.0'` (matches PR #259 ZSTD precedent); two consecutive runs produce byte-identical Parquet (SHA-256 equality asserted).
- **Findings:** all sanity checks pass — `COUNT(*) = 44418`; `COUNT(DISTINCT focal_match_id) = 22209`; 33 emitted feature column names match the deterministic F1→F2→F3→F5 binding order; no slot-bias token (BLOCKED_SLOT_TOKEN_REGEX); no POST_GAME token; no `civilization` vocabulary; no `reconstructed_rating` column; no `matchup_h2h_*_pair_*` column (F4 drop); no `race_pair_*` column (F6 deferral); no `*_pair_sum` or `*_pair_product` column; per-feature traceability proof: every emitted column traces to either `BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS` (10 pairs from 02_01_03 24-tuple) or `BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES`; parent SHA at end-of-run = parent SHA at start-of-run for every parent artifact (no mutation); second-run byte-equal Parquet verified.
- **What this means:** Step `02_02_01` has produced its first materialised feature artifact and its first non-vacuous leakage audit; the CROSS-02-01 §5 gate is mechanically cleared. Step `02_02_01` is **NOT** closed by this PR. Status YAML flips (`STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`) are deferred to a separate U2.B-style closure PR (per PR #237 / PR #262 precedent). The next 02_02 step (`02_02_02+`) remains DEFERRED; Phase 03 is NOT started; no baseline modelling.
- **Decisions taken:** materialise exactly the 33 candidates bound by PR #268; import (not re-declare) the 5 binding constants from `adjudicate_symmetry_difference_feature_scope.py`; preserve row identity byte-equal to 02_01_03 Parquet; ZSTD compression matching PR #259; 22-step halting falsifier chain; both module-constant (`EXPECTED_OUTPUT_ROW_COUNT = 44_418`) AND runtime audit-JSON equality check per Round 1 / N2; symbolic-formula `computation` field in per-feature traceability per Round 1 / N6; spec-literal `"pass"` value for `cutoff_time_filter_structural_check` per Round 1 / N1.
- **Decisions deferred:** Step `02_02_01` closure (separate U2.B-style PR; status YAML flips; closure-only research_log entry); Step `02_02_02+` (within-section progression); Step `02_01_04+`; Phase 03 splitting and baseline modeling; AoE2 work; any thesis chapter prose; F6 race-pair categorical interactions (02_05); `product` interaction (02_05); unary `2x−1` matchup rescaling (open design question).
- **Thesis mapping:** Chapter 4 §4.5 (feature engineering plan) — citable as the FIRST non-vacuous CROSS-02-01 post-materialization audit row for Step `02_02_01` alongside the PR #236 tranche-1 audit and the PR #259 02_01_03 audit. The future U2.B closure PR will add the step-closure row.
- **Open questions / follow-ups:** schedule the U2.B closure planner-science round for Step `02_02_01` (separate PR); whether Step `02_02_02+` planner-science may begin before the formal closure PR.
- **Acknowledged trade-offs:** F1+F2+F3 joint basis covers linear-in-{signed-difference, level, symmetric-magnitude} subspaces for LogReg per Invariant I8, but quadratic effects (`focal²`, `opponent²`, `focal × opponent`) remain unrecoverable without polynomial terms — those are the 02_05 deferral surface. F5 (`either, both, xor`) is rank-2 over the 2-dimensional Boolean source for LogReg with regularisation, but retained for tree models per PR #267 Round 2 N3.

Does NOT touch root `reports/research_log.md`. Does NOT touch ROADMAP. Does NOT touch `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml`. Does NOT touch any `02_01_02` / `02_01_03` / PR #268 adjudication artifact. Does NOT touch any source / test / notebook / spec / data / AoE2 / thesis / docs / `.claude` path outside the 11-file manifest.
```

T04 stop condition: append is byte-additive at end of file; no
historical entry rewritten; PR-#262 entry remains byte-identical except
for byte-shift caused by the new append.

**T05 — `pyproject.toml` + `CHANGELOG.md` + `planning/INDEX.md` (Sonnet
executor).**

Files (allowed):
- `pyproject.toml` (version bump `3.85.0 → 3.86.0`);
- `CHANGELOG.md` (move `[Unreleased]` body to `[3.86.0] — <date>
  (PR #<TBD>: feat/sc2egset-02-02-01-symmetry-difference-materialization)`;
  reset `[Unreleased]`; add `### Notes` with no-closure / no-status-flip /
  no-Phase-03 / no-baseline disclaimers);
- `planning/INDEX.md` (archive PR #267 + PR #268 with their merge SHAs
  `af8c3d98` and `b84ed6d6`; add new Active line).

CHANGELOG `[3.86.0]` content (template — Layer-2 executor fills in):
```
## [3.86.0] — YYYY-MM-DD (PR #<TBD>: feat/sc2egset-02-02-01-symmetry-difference-materialization)

### Added
- `materialize_symmetry_difference_features.py`: materialisation module
  emitting 33 feature columns (F1=10, F2=10, F3=10, F5=3) per the PR #268
  binding adjudication contract.
- `02_02_01_symmetry_difference_features.parquet`: 44,418 rows × 37
  cols (3 identity + 1 context + 33 features).
- `reports/artifacts/02_02_01/leakage_audit_sc2egset.{json,md}`: first
  non-vacuous CROSS-02-01-v1.0.1 §3 leakage audit for Step 02_02_01
  with per-feature traceability proof.
- Non-closure `research_log.md` entry recording materialisation state
  per PR #259 precedent.

### Changed
- Sandbox notebook `02_02_01_symmetry_difference_feature_materialization.{py,ipynb}`
  overwritten in place (PR #266 scaffold replaced by execution notebook).

### Notes
- Step 02_02_01 NOT closed by this PR (closure deferred to a separate
  U2.B-style PR per PR #237 / PR #262 precedent).
- No STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS flip.
- No Phase 03 work. No baseline modeling. No reopen of Q5 / Q6 / Q6F /
  Q6G / Q6H / `reconstructed_rating` closure.
- No AoE2 `civilization` vocabulary introduced. No new MMR scalar. No
  new tracker-derived target-match feature.
```

T05 stop condition: pre-commit hook (`ruff` + `mypy`) passes on the diff;
all listed files have one change each; no other files touched.

## File Manifest

The future Layer-2 PR's tracked diff is exactly these 11 files:

| # | Path | Scope | Forbidden content |
|---|------|-------|-------------------|
| 1 | `src/rts_predict/games/sc2/datasets/sc2egset/materialize_symmetry_difference_features.py` | NEW; per T01 | re-declaring `BINDING_*` constants (must import); SQL CTE chain; encoder fit; new MMR scalar; reconstructed_rating column; matchup pair operation; race pair; civilization token |
| 2 | `tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_symmetry_difference_features.py` | NEW; per T01 | training on real data; absolute paths in fixtures; non-deterministic test fixtures; coverage < 95% |
| 3 | `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.py` | OVERWRITE PR #266 scaffold | print-vs-logger violations on diagnostic one-liners; calls into the adjudicator module (must call only materialisation module) |
| 4 | `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.ipynb` | OVERWRITE; jupytext-paired | drift between `.py` and `.ipynb`; embedded data values that change run-to-run |
| 5 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_features.parquet` | NEW; per T03 | row count ≠ 44418; column count ≠ 37; non-deterministic re-write; missing identity columns |
| 6 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_02_01/leakage_audit_sc2egset.json` | NEW; per T03 | `features_audited` length ≠ 33; `verdict ≠ "PASS"`; missing per-feature traceability; missing parent SHA pins |
| 7 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_02_01/leakage_audit_sc2egset.md` | NEW; per T03 | missing §-sections; non-deterministic prose; no-closure disclaimer absent |
| 8 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` | APPEND-ONLY; per T04 | rewriting historical entries; missing required tokens (`closure_status`, `materialization_state`, etc.) |
| 9 | `pyproject.toml` | version bump 3.85.0 → 3.86.0 | any other field touched |
| 10 | `CHANGELOG.md` | `[3.86.0]` block + reset `[Unreleased]` | missing `### Notes` disclaimers; wrong date |
| 11 | `planning/INDEX.md` | archive PR #267 + PR #268; new Active line | rewriting existing rows; missing merge SHAs |

**Hard-forbidden** (any of these halts execution):
- `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`;
- `ROADMAP.md` (`02_02_01` block at lines 2853–3131 must remain
  byte-identical);
- root `reports/research_log.md`;
- thesis / docs / `.claude/` / data / AoE2 paths;
- PR #268 adjudication CSV/MD;
- the PR #266 validator module;
- the 02_01_02 / 02_01_03 Parquets and audit JSONs/MDs;
- the PR #268 adjudication notebook
  (`02_02_01_symmetry_difference_feature_adjudication.{py,ipynb}`);
- any new spec under `reports/specs/`;
- any cleaning-layer YAML.

## Future module shape

```python
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from rts_predict.games.sc2.datasets.sc2egset.adjudicate_symmetry_difference_feature_scope import (
    BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS,
    BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS,
    BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES,
    BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS,
    ROW_IDENTITY_JOIN_KEYS,
)


@dataclass(frozen=True)
class SymmetryDifferenceMaterializationResult:
    """Frozen materialisation state returned by the public function.

    Attributes:
        step: Always ``"02_02_01"``.
        output_parquet_path: Path to the emitted 37-col Parquet artifact.
        output_audit_json_path: Path to the emitted audit JSON.
        output_audit_md_path: Path to the emitted audit MD.
        feature_column_names: Tuple of 33 emitted feature column names
            in deterministic F1→F2→F3→F5 order (per A11).
        row_count: Always 44418 (asserted equal to 02_01_03 audit).
        distinct_focal_match_count: Always 22209 (asserted equal to
            02_01_03 audit).
        validator_passed: Always True at successful run (False would have
            halted via falsifier 1).
        leakage_audit_verdict: Always ``"PASS"`` at successful run.
        parent_artifact_sha256s: Mapping from canonical relpath to
            SHA-256 hex64.
        adjudication_csv_sha256: SHA-256 of the PR #268 CSV.
        adjudication_md_sha256: SHA-256 of the PR #268 MD.
        validator_module_sha256: SHA-256 of the PR #266 validator.
        materialize_module_sha256: SHA-256 of this module's file.
    """
    step: Literal["02_02_01"]
    output_parquet_path: Path
    output_audit_json_path: Path
    output_audit_md_path: Path
    feature_column_names: tuple[str, ...]
    row_count: int
    distinct_focal_match_count: int
    validator_passed: bool
    leakage_audit_verdict: Literal["PASS"]
    parent_artifact_sha256s: dict[str, str]
    adjudication_csv_sha256: str
    adjudication_md_sha256: str
    validator_module_sha256: str
    materialize_module_sha256: str


class SymmetryDifferenceMaterializationError(Exception):
    """Raised on any halting falsifier."""


def run_symmetry_difference_feature_materialization(
    *,
    repo_root: Path | str | None = None,
    output_parquet_path: Path | str | None = None,
    output_audit_json_path: Path | str | None = None,
    output_audit_md_path: Path | str | None = None,
) -> SymmetryDifferenceMaterializationResult:
    """Materialise the 33-candidate symmetry/difference feature Parquet.

    Steps:
      1. Resolve paths from repo_root defaults (canonical 02_02 subtree).
      2. SHA-pin parent artifacts (Parquets, audit JSONs, PR #268 CSV/MD,
         validator module); raise SymmetryDifferenceMaterializationError
         on any mismatch.
      3. Read 02_01_03 Parquet via pyarrow.
      4. Verify required source columns present (10 numeric pairs + 1
         Boolean pair).
      5. Compute F1, F2, F3, F5 transforms in deterministic column order.
      6. Assemble 37-col output DataFrame: identity + context + 33 features.
      7. Assert row count = 44418, distinct focal match count = 22209.
      8. Write Parquet with deterministic writer settings (A14).
      9. Verify second-run byte equality (re-write to temp; compare hashes).
     10. Re-hash parent artifacts; assert no mutation (A15).
     11. Emit leakage audit JSON (per spec below).
     12. Emit leakage audit MD (per spec below).
     13. Return frozen dataclass result.
    """
    ...
```

## Future leakage audit JSON requirements (non-vacuous)

The JSON must conform to the CROSS-02-01-v1.0.1 §3 spec and include the
following keys at minimum (matches PR #259 audit JSON shape adapted to the
33-candidate set):

```json
{
  "spec_version": "CROSS-02-01-v1",
  "dataset": "sc2egset",
  "phase_02_step": "02_02_01",
  "audit_date": "YYYY-MM-DD",
  "audit_pr": "PR #<TBD>",
  "verdict": "PASS",
  "future_leak_count": 0,
  "post_game_token_violations": 0,
  "normalization_fit_scope": "training_fold_only",
  "target_encoding_fold_awareness": "N/A_no_target_encoding",
  "cutoff_time_filter_structural_check": "pass",
  "reference_window_assertion": "pass",

  "features_audited": [<33 feature column names in F1→F2→F3→F5 order>],
  "features_audited_count": 33,

  "row_count": 44418,
  "distinct_focal_match_count": 22209,
  "feature_column_count": 33,

  "projected_identity_columns": [
    "focal_match_id", "focal_player", "opponent_player"
  ],
  "projected_context_columns": ["started_at"],

  "materialized_output_paths": [
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_features.parquet"
  ],
  "feature_parquet_path": "<same as materialized_output_paths[0]>",
  "feature_parquet_sha256": "<hex64>",
  "audit_json_path": "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_02_01/leakage_audit_sc2egset.json",
  "audit_md_path": "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_02_01/leakage_audit_sc2egset.md",

  "parent_artifact_shas": {
    "02_01_02_pre_game_features.parquet": "24db73fb…",
    "02_01_03_history_enriched_pre_game_features.parquet": "053900e7…",
    "02_01_02_leakage_audit_sc2egset_json_canonical": "1da271c6…",
    "02_01_03_leakage_audit_sc2egset_json_canonical": "183b9000…",
    "02_02_01_symmetry_difference_feature_adjudication.csv": "<measured>",
    "02_02_01_symmetry_difference_feature_adjudication.md": "<measured>"
  },
  "validator_module_sha256": "d8f34760…",
  "materialize_module_sha256": "<measured>",

  "binding_difference_family_numeric_pair_count": 10,
  "binding_symmetric_pair_aggregate_transforms": ["mean", "abs_diff"],
  "binding_cross_region_boolean_pair_transforms": ["either", "both", "xor"],

  "feature_to_family_mapping": {
    "focal_minus_opponent_prior_match_count_diff": "F1_difference",
    "prior_match_count_pair_mean": "F2_pair_mean",
    "prior_match_count_pair_abs_diff": "F3_pair_abs_diff",
    …
    "cross_region_pair_or": "F5_cross_region_pair",
    "cross_region_pair_and": "F5_cross_region_pair",
    "cross_region_pair_xor": "F5_cross_region_pair"
  },

  "per_feature_traceability": [
    {
      "feature": "focal_minus_opponent_prior_match_count_diff",
      "family": "F1_difference",
      "direction": "focal_minus_opponent",
      "source_columns": ["focal_prior_match_count", "opponent_prior_match_count"],
      "source_artifact": "02_01_03_history_enriched_pre_game_features.parquet",
      "traces_to_audited_24_tuple": true,
      "computation": "focal_prior_match_count - opponent_prior_match_count"
    },
    … (33 entries total; symbolic formula form per Round 1 / N6 — literal
       source-column names, NOT pandas-API expressions. Reproducible across
       pandas/PyArrow version drift; examiner-readable without source code.)
  ],

  "leakage_checks": {
    "slot_bias_token_match": null,
    "post_game_token_match": null,
    "tracker_raw_source_match": null,
    "reconstructed_rating_match": null,
    "future_match_or_phase_03_match": null,
    "civilization_aoe2_vocabulary_match": null,
    "matchup_h2h_pair_token_match": null,
    "race_pair_token_match": null
  },

  "no_parent_mutation_check": true,
  "deterministic_re_write_check": true,

  "leakage_falsifiers": [<list of all 21 halting falsifier names>],

  "custom_extensions": {
    "_comment": "Fields beyond CROSS-02-01-v1.0.1 Section 3 are enumerated here so examiners can distinguish spec-mandated fields from project extensions.",
    "fields": [
      "feature_to_family_mapping",
      "per_feature_traceability",
      "binding_difference_family_numeric_pair_count",
      "binding_symmetric_pair_aggregate_transforms",
      "binding_cross_region_boolean_pair_transforms",
      "leakage_falsifiers",
      "no_parent_mutation_check",
      "deterministic_re_write_check"
    ]
  },

  "notes": "Step 02_02_01 NOT closed by this PR; closure deferred to a U2.B-style PR per PR #237 / PR #262 precedent. All 33 feature columns are row-preserving algebraic transforms over the audited 02_01_03 24-tuple (10 numeric focal/opponent pairs) and the audited 02_01_03 Boolean cross-region pair; row identity (focal_match_id, focal_player, opponent_player, started_at) is byte-identical to the 02_01_03 Parquet on those columns. Invariant I3 cutoff inherited unchanged; no new temporal filter introduced at 02_02. Invariant I5 enforced row-by-row: F1 = focal − opponent (slot-orthogonal); F2/F3/F5 are permutation-invariant aggregates. Invariant I8 LogReg basis spans (F1, F2, F3) per Round-2 anchor. F4 matchup-history pair operation: DROPPED per B1 / PR #268. F6 race-pair: DEFERRED to 02_05 per PR #268. Product / sum / ratio: EXCLUDED / DEFERRED per PR #268."
}
```

## Future audit MD requirements

**Round 1 / N3 corrected:** This PR introduces a **new 7-section MD
structure** tailored to the 33-feature symmetry/difference family. PR #259's
audit MD has 4 sections (for 24 features, no per-feature traceability
sub-table) and PR #236's audit MD has 8 sections (for the 02_01_02 7-tuple
+ Q3 race adjudication appendix). The 7-section structure here is the
minimal coverage required for the "non-vacuous" CROSS-02-01-v1.0.1 §3
requirement across 33 features × per-feature traceability — not a literal
PR #259 precedent claim. The structure is:

- **§1 Input lineage (SHAs).** Table of parent artifacts with relative paths
  and SHA-256 pins (Parquets, audit JSONs, PR #268 CSV/MD, validator module).
- **§2 Row identity alignment proof.** Input row count from 02_01_03 audit
  (`44418`) vs output row count; distinct focal match count (`22209`);
  identity-tuple equality proof on first 100 + last 100 rows.
- **§3 Per-feature traceability table.** 33 rows: feature name, family,
  direction, source columns, computation formula, source artifact, "traces
  to audited 24-tuple"/"traces to audited bool-pair".
- **§4 Leakage check sweep (boundary-aware).** Each of the 8 token checks
  in `leakage_checks` with the regex pattern, the column-name sweep result,
  and the prose sweep result. All must be `null` (no match).
- **§5 Parent-non-mutation assertion.** Start-of-run SHAs vs end-of-run
  SHAs for each parent artifact. All must equal.
- **§6 Deterministic re-run statement.** Two consecutive runs produce
  byte-identical Parquet (verified by SHA-256 equality of the two output
  files).
- **§7 Explicit no-closure / no-status-YAML disclaimer.** Verbatim:
  "Step 02_02_01 is NOT closed by this PR. STEP_STATUS.yaml has no
  `02_02_01` row. PIPELINE_SECTION_STATUS.yaml has no `02_02` row.
  PHASE_STATUS.yaml is byte-unchanged. ROADMAP.md is byte-unchanged.
  Closure follows in a separate U2.B-style PR per PR #237 / PR #262
  precedent."

## Gate Condition

### Layer-1 gate (THIS planning PR)

PASS iff all of:

1. This PR's tracked diff is exactly two files (`planning/current_plan.md`,
   `planning/current_plan.critique.md`).
2. The reviewer-adversarial critique returns APPROVE or APPROVE-WITH-NITS
   with 0 BLOCKERs.
3. No file under `src/`, `tests/`, `sandbox/`, `reports/artifacts/`,
   `pyproject.toml`, `CHANGELOG.md`, `planning/INDEX.md`, `STEP_STATUS.yaml`,
   `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`, `ROADMAP.md`,
   `research_log.md` is modified by this PR.
4. `pyproject.toml` version remains `3.85.0` (no bump in the planning PR).
5. `planning/INDEX.md` is NOT modified by this PR (the Active line update
   and PR #267 / PR #268 archival happen in the future Layer-2 PR's T05).

### Layer-2 gate (FUTURE execution PR)

PASS iff all of:

1. Tracked diff is exactly 11 files per the File Manifest.
2. `materialize_symmetry_difference_features.py` imports the 5 binding
   constants from `adjudicate_symmetry_difference_feature_scope.py` and
   does not re-declare them.
3. The output Parquet has exactly 44,418 rows × 37 columns; the 33 feature
   column names in deterministic F1→F2→F3→F5 order match the
   `BINDING_*` constants.
4. The audit JSON has `verdict == "PASS"`, `features_audited_count == 33`,
   `row_count == 44418`, `distinct_focal_match_count == 22209`,
   `no_parent_mutation_check == true`, `deterministic_re_write_check == true`.
5. The audit JSON's `per_feature_traceability` list has 33 entries, each
   referencing only `BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS` sources or
   `BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES`.
6. The audit MD has all 7 §-sections; §7 contains the verbatim no-closure
   disclaimer.
7. The dataset `research_log.md` has a single new appended entry with
   `closure_status: still_open`, `materialization_state: materialized`,
   `leakage_audit_state: post_materialization_pass`,
   `features_audited_count: 33`, `row_count: 44418`.
8. `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml`
   / `ROADMAP.md` / root `reports/research_log.md` are byte-unchanged.
9. `pyproject.toml` version is `3.86.0`; `CHANGELOG.md` has the
   `[3.86.0]` block with required `### Notes` disclaimers.
10. `planning/INDEX.md` archives PR #267 (merge SHA `af8c3d98`) and PR #268
    (merge SHA `b84ed6d6`) and lists the new branch as Active.
11. Pre-commit hooks (`ruff`, `mypy`) clean; pytest passes with ≥ 95%
    branch coverage on the new module; ≥ 40 distinct tests added.
12. Re-running the materialisation notebook produces byte-identical
    Parquet (executor verifies via `sha256sum` comparison).
13. No `02_02_02+` / `02_01_04` / Phase-03 directory or file is created.
14. No baseline modelling code added.
15. No `civilization` token, no `reconstructed_rating` column, no MMR
    scalar, no tracker-derived target-match feature, no slot-bias
    column name introduced.
16. The PR #268 adjudication CSV/MD are byte-unchanged.
17. The PR #266 validator module is byte-unchanged.
18. The 02_01_02 and 02_01_03 Parquets and audit JSONs/MDs are byte-unchanged.
19. The PR #268 adjudication notebook
    (`02_02_01_symmetry_difference_feature_adjudication.{py,ipynb}`) is
    byte-unchanged. Only the PR #266 scaffold materialisation notebook is
    overwritten.

## Open Questions

Surfaced for reviewer-adversarial scrutiny:

**OQ1 — Audit JSON `cutoff_time_filter_structural_check` value (Round 1 / N1
RESOLVED).** Spec literal `"pass"` is required per CROSS-02-01-v1.0.1 §3 (PR
#236 + PR #259 audits both use the bare `"pass"` literal; PR #228 audit MD
line 39 verbatim quotes the spec requirement). The "no SQL filter at 02_02
layer; cutoff inherited unchanged from 02_01_03 strict-`<` filter" prose is
recorded in the audit JSON `notes` field and in the audit MD §4
(leakage-check sweep) preamble, not in the structural-check field value. The
audit JSON's `parent_artifact_shas` map already pins the 02_01_03 audit
JSON's canonical SHA-256, which transitively certifies inheritance.

**OQ2 — Parquet writer override scope.** Whether to set
`use_dictionary=False` for Boolean columns to guarantee byte determinism.
Default pyarrow behaviour is deterministic on the platforms tested. If
empirical testing in T01 shows determinism without the override, the
override is omitted. Reviewer should weigh: explicit-pin (defensive but
adds line of code) vs. measure-then-decide (simpler if determinism holds).

**OQ3 — Per-feature traceability `computation` string format (Round 1 / N6
RESOLVED).** Use **symbolic formula** with literal source-column names
(e.g., `"focal_prior_match_count - opponent_prior_match_count"`). Rationale:
the audit JSON is a thesis-citable artifact; encoding pandas-API syntax
(`df[focal_col] - df[opponent_col]`) would couple the audit to a particular
runtime API and require examiners to parse Python to evaluate the claim.
The symbolic form is reproducible across pandas/PyArrow version drift,
examiner-readable without source code, and machine-checkable against
`source_columns` (the formula must contain exactly the two listed columns
joined by the family operator). Invariant I6 "literal code, not description"
is honoured at the **module** layer (the materialisation function contains
the literal pandas code) while the **audit JSON** records the semantic claim.

**OQ4 — Feature column dtype policy for F1 over int64 parents.** The
parent columns `focal_prior_match_count` and `opponent_prior_match_count`
are `int64`; their signed difference can be negative but stays int64.
Proposed: keep int64 (no upcast). For F2 (`(int64 + int64) / 2.0`) the
result is float64 by pandas convention. For F3
(`abs(int64 - int64)`) the result is int64. Reviewer should confirm
that mixed int64/float64 in the 33-feature schema is acceptable for
downstream Phase 03/04 (sklearn pipelines handle both); if not, a
proposal would be to up-cast all numeric features to float64 for
schema homogeneity.

**OQ5 — Audit MD §3 row count.** The per-feature traceability table has
33 rows. Should §3 also display a per-family count summary (F1: 10, F2: 10,
F3: 10, F5: 3)? Proposed: yes, as a one-line preamble. Mirrors PR #259's
audit MD §1 prose pattern.

**OQ6 — Layer-2 executor model assignment.** Per `.claude/rules/data-analysis-
lineage.md` "Agent and model routing discipline":
- T01 (module + tests): SONNET executor sufficient — mechanical
  computation, all decisions resolved at adjudication layer.
- T02 (notebook overwrite): SONNET executor sufficient.
- T03 (artifact generation): **OPUS execution** required — Parquet writer
  determinism + audit JSON per-feature traceability are load-bearing
  methodological steps.
- T04 (research_log append): SONNET executor sufficient.
- T05 (pyproject + CHANGELOG + INDEX): SONNET executor sufficient.
Reviewer should confirm or contest this T01–T05 routing.

**OQ7 — `feature_to_family_mapping` redundancy.** The audit JSON's
`feature_to_family_mapping` and `per_feature_traceability` overlap (both
encode feature → family). Proposed: keep both for examiner clarity (the
mapping is searchable as a dict; the traceability list provides full
provenance per feature). Alternative: collapse to one. Reviewer should
decide.

**OQ8 — Layer-2 PR title.** Proposed: `feat(sc2egset): Step 02_02_01
materialise 33 symmetry/difference features + non-vacuous CROSS-02-01
audit (Layer-2)`. Mirrors PR #259 title pattern.

## Risks self-flagged for reviewer-adversarial

**R1 — Validator-passes-spec-but-runtime-fails.** The PR #266 validator
passes the candidate specs at construction time (passed=True per PR #268
CSV) but does not exercise the materialisation runtime. If the
materialisation produces a row count drift or identity-alignment failure,
the audit JSON `verdict` is `FAIL` and the run halts. Risk: this is the
first time the candidate specs hit a real Parquet read. Mitigation: T01
adds the 21-step halting falsifier chain; T01 test suite includes synthetic
failure injections; T03 verifies on real data before audit emission.

**R2 — Determinism gap on Boolean columns.** PyArrow Boolean column
encoding may use dictionary encoding by default. If two runs produce
different page boundaries, the Parquet bytes differ even if content is
identical. Mitigation: T01 includes a determinism test; T03 verifies via
SHA-256 comparison of two writes; if a difference is observed, T01 adds
explicit `use_dictionary=False` for Boolean columns and re-verifies.

**R3 — Notebook overwrite collision.** PR #266 scaffolded the
materialisation notebook (`02_02_01_symmetry_difference_feature_materialization.{py,ipynb}`)
with a placeholder body. PR #259 precedent: overwrite in place. Risk:
the PR #266 placeholder notebook may have content that the executor
should preserve. Mitigation: PR #266 scaffold contains only the
validator-execution skeleton, not materialisation logic; the overwrite is
full-content replacement, matching PR #259 → PR #241 precedent.

**R4 — Audit verbosity inflation.** 33 per-feature traceability entries +
8 leakage checks + 7 MD §-sections could push the audit JSON beyond
20 KB (PR #259's audit was 13 KB for 24 features). Risk: large artifacts
inflate the diff. Mitigation: this is expected (per-feature traceability
is the "non-vacuous" requirement); the size is intrinsic.

**R5 — Per-feature traceability proof falsifiability.** The per-feature
proof is a dict-list that the audit module constructs from the adjudicator
constants. Risk: if the adjudicator's `BINDING_*` constants change in a
future PR (e.g., a new pair added), this PR's emitted traceability would
silently drift. Mitigation: T01's halting falsifier chain pins the
`BINDING_*` tuple identity at runtime; falsifier 8/9/10 fires if the
counts/values drift.

**R6 — Row count assertion brittleness.** Asserting `row_count == 44418`
hard-codes the 02_01_03 audit value. If 02_01_03 is ever re-materialised
(it shouldn't be, but the closure ban is policy, not enforced), this
assertion would break. Mitigation: the assertion is correct policy; PR
#262 / PR #259 closure ban is the source of truth; if 02_01_03 changes,
this Step requires re-execution anyway.

**R7 — Coverage target under-specification.** ≥ 40 tests is a floor.
PR #259 had 175 tests for 24 features + SQL CTE chain; this module has
33 features + no SQL. Risk: ≥ 40 may be insufficient. Mitigation:
the actual target is ≥ 95% branch coverage; the 40-test floor is a
sanity check, not a target. Layer-2 executor should add tests until
coverage clears 95%, regardless of count.

**R8 — `OPUS execution` budget for T03.** OQ6 routes T03 to Opus
execution. Risk: this is one of three Opus-execution tasks (T01 binding-
constant import semantics, T03 artifact generation, plus the planner-side
Opus session itself). Mitigation: T01 is Opus-guided not Opus-executed
(routing per `.claude/rules/data-analysis-lineage.md` "if the
implementation step itself requires subtle reasoning"); only T03 needs
Opus runtime.

**R9 — Audit JSON `notes` field length.** The proposed `notes` field
(see audit JSON spec above) is verbose. Risk: lint may flag long single-
string fields. Mitigation: the `notes` field is examiner-facing; verbosity
is intentional; lint rules don't apply to JSON values.

**R10 — Materialisation module location.** Per project layout, the module
sits next to the adjudicator at `src/rts_predict/games/sc2/datasets/sc2egset/`.
Risk: alternative location `src/rts_predict/games/sc2/datasets/sc2egset/features/`
might be more organised. Mitigation: PR #259 precedent puts
`materialize_history_enriched_pre_game_features.py` at the same flat level
as `adjudicate_history_rating_reconstruction.py`; consistency wins.


## Reviewer-adversarial Round 1 nits applied (Layer-1 materialisation)

Round 1 verdict: **APPROVE-WITH-NITS** (0 blockers; 6 nits). Full critique at
`planning/current_plan.critique.md`. All six nits are wording / format fixes
applied inline in this plan body before Layer-2 execution begins:

| # | Maps to | Concern | Applied as |
|---|---|---|---|
| **N1** | OQ1 / audit JSON spec | `cutoff_time_filter_structural_check` value must be the spec-literal `"pass"`; the qualified value `"pass_inherited_from_02_01_03"` is not spec-allowed. Inheritance prose belongs in `notes` and audit MD §4-equivalent. | Audit JSON spec uses `"pass"`; inheritance note moved to JSON `notes` field. OQ1 rewritten to record the decision. |
| **N2** | A9 / R6 / Falsifier 12 | Row count assertion should be both module-level constant (precedent: PR #259) AND runtime equality against 02_01_03 audit JSON's `row_count` field. Defence-in-depth. | A9 declares `EXPECTED_OUTPUT_ROW_COUNT = 44_418` AND adds a runtime assertion against the audit JSON's `row_count`. Falsifier 12 splits into two checks. R6 rewritten. |
| **N3** | "Future audit MD requirements" | The 7-section structure is NOT a PR #259 precedent (PR #259 has 4 sections; PR #236 has 8). The structure itself is fine but the precedent claim is wrong. | "Future audit MD requirements" reworded: "this PR introduces a new 7-section structure tailored to the 33-feature symmetry/difference family; PR #259's 4-section structure was insufficient for per-feature traceability of 33 features." |
| **N4** | A14 / R2 / OQ2 | Parquet writer `compression='snappy'` diverges from PR #259's `COMPRESSION 'ZSTD'`. PyArrow analog should be `compression='zstd'` for dataset-wide encoding consistency. | A14 uses `compression='zstd'`; precedent citation added (PR #259 line 1041–1052 of materialise_history_enriched_pre_game_features.py). |
| **N5** | T04 | The proposed YAML-block research_log template does NOT match PR #259's actual Markdown-bold-label entry shape. | T04 template replaced with Markdown bold-label form mirroring PR #259's research_log lines 79–103. |
| **N6** | OQ3 / audit JSON per_feature_traceability | `computation` field as Python-expression string (`df[focal_col] - df[opponent_col]`) is brittle and pandas-API-coupled; symbolic formula with literal source-column names is more reproducible and examiner-friendly. | Audit JSON per-feature `computation` field uses symbolic formula (e.g., `"focal_prior_match_count - opponent_prior_match_count"`); OQ3 rewritten with the binding decision. |

All six fixes are reflected in the plan body above. None requires a planner
re-pass; Layer-2 execution can proceed without further adversarial review on
this plan.
