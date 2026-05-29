# Adversarial Critique — SC2EGSet Step 02_02_01 scaffold + one validation module

**Plan reviewed:** `planning/current_plan.md` (Category A; branch
`feat/sc2egset-02-02-01-symmetry-difference-scaffold`; future version bump
3.83.0 → 3.84.0)
**Reviewer:** reviewer-adversarial (pre-execution gate)
**Verdict:** APPROVE-WITH-NITS
**Blocking issues:** 0
**Non-blocking nits:** 8 (all applied to plan body at Layer-1 materialisation)
**Confidence:** HIGH
**Date:** 2026-05-29
**Base SHA:** `7f2506edb993937084a613fbea6dc4edc2a51635`
**Predecessor PR:** #264 (merged 2026-05-29)

## Verdict reasoning

The atomic boundary (scaffold + ONE validator, NO materialisation, NO
adjudication, NO STEP_STATUS row) is correct per
`.claude/rules/data-analysis-lineage.md` "Non-batching rule" sequence step 2
and mirrors the PR #233 (`02_01_02`) / PR #241 (`02_01_03`) precedents.
Naming, scope discipline, invariant inheritance, and gate-condition shape
are sound. Eight non-blocking nits were raised across (a) two naming/style
corrections vs the planner-science draft (N1 branch idiom, N8 notebook
filename), (b) one CHANGELOG style precedent (N2 `### Notes` heading),
(c) two methodology sharpenings making the I5 promise structural rather
than soft (N3 slot-orthogonality regex/whitelist, N4 direction annotation),
(d) one inheritance-into-structure conversion (N5 audited-tuple
traceability), (e) one substring-vs-token correction (N6 boundary-aware
`POST_GAME_TOKEN_REGEX`), and (f) one mechanically-defensible-promise
sharpening (N7 filesystem absence vs emptiness).

Per user direction at Layer-1 dispatch (2026-05-29), all 8 nits were
applied to the plan body before this draft PR was materialised. The plan
records each nit's resolution in a labelled assumption (**A2** through
**A17**), threads it through T01/T02/T03/T04 execution instructions, and
binds it in the gate condition list (items 6 through 13). The remaining
methodology questions about scope boundaries (cross-region BOOLEAN-pair,
race-pair, symmetric-pair-aggregate) are correctly deferred to the future
source-anchor adjudication PR analogous to PR #234.

## Adjudication outcomes (planner choices, all approved)

- **Outcome A** — scaffold + one validation module planning PR. B–G
  rejected:
  - B (direct scaffold execution without planning) violates plan/review/
    execute discipline.
  - C (direct `02_02_01` materialisation planning) is barred by the
    ROADMAP halt_predicate (line ~3046) which requires scaffold-pass before
    materialisation.
  - D (status-chain update PR) is wrong because the `02_02`
    `PIPELINE_SECTION_STATUS` row first lands at step closure, not at
    scaffold open (PR #230 precedent at ROADMAP lines 3058–3060).
  - E (Phase 03 planning) is barred by `PHASE_STATUS.yaml`
    (Phase 02 = `in_progress`).
  - F (reopen `02_01` / Q5 / Q6 / Q6X / `reconstructed_rating`) has no
    defect to reopen (Q-chain PRs #242 / #245 / #247 / #249 / #251 +
    PR #253 / #255 / #257 / #259 / #262 closures frozen by ROADMAP
    halt_predicate).
  - G (hold) is unjustified — all predicates are consistent.
- **Branch** — `feat/sc2egset-02-02-01-symmetry-difference-scaffold` per
  PR #241 idiom (`feat/sc2egset-02-01-03-history-scaffold`); reviewer-
  adversarial N1.
- **Validator filename** —
  `validate_symmetry_difference_feature_materialization.py` per PR #233 /
  PR #241 precedent (validator carries family name from scaffold onward and
  never renames; stage marker lives in docstring).
- **Notebook filename** —
  `02_02_01_symmetry_difference_feature_materialization.{py,ipynb}` per
  `sandbox/README.md` single-notebook-per-Step contract and PR #259
  precedent (notebook overwritten in place at materialisation, not
  renamed); reviewer-adversarial N8.
- **Sandbox subdir** — `02_symmetry_and_difference_features/` (with
  `_and_`) per ROADMAP lines 2932 + 3100 verbatim.
- **Version bump** — minor 3.83.0 → 3.84.0 per three precedents
  (PR #233 / PR #239 / PR #241 minor bumps on `feat/`-class scaffold
  PRs); lands in Layer-2, not Layer-1.

## Lens assessments

- **Temporal discipline:** SOUND. Plan declares Invariant I3 inheritance
  from `02_01_03` and per **A10** (N5) requires every candidate's
  `source_columns` to trace to the audited 24-tuple or 7-tuple — making
  I3 inheritance structural rather than asserted. Halt-clause bars
  target-game and future-match leakage explicitly (T01 falsifier chain).
- **Statistical methodology:** N/A — scaffold-stage PR; no metric / model /
  fold computed.
- **Feature engineering:** SOUND after nit application. I5 inheritance
  correctly declared at three layers: (a) row-level structural in upstream
  `02_01_03`'s `focal_*` / `opponent_*` pairs; (b) candidate-spec layer
  per **A9** (N4) requiring explicit `direction` annotation; (c) name-token
  layer per **A8** (N3) via regex/whitelist sweep. Difference-feature
  semantics aligned with Bradley-Terry per manual §3.
- **Thesis defensibility:** STRONG. Non-batching rule explicitly cited;
  precedent ladder (PR #232 / #233 / #234 / ... / #259 / #262 / #264)
  named per claim; the §02_01_03 amendment back-reference at ROADMAP
  L2837–L2849 preserved verbatim; the audited tuples constitute a frozen,
  testable source-of-truth.
- **Cross-game comparability:** MAINTAINED. `02_02` is dataset-agnostic
  per `docs/PHASES.md`; SC2EGSet scaffold uses `race` exclusively; the
  `FORBIDDEN_AOE2_VOCABULARY` constant structurally rejects
  `civilization` / `civ`.

## Findings

### Blockers

- *(none)*

### Nits (non-blocking) — ALL APPLIED to plan body

- **N1 — branch idiom (APPLIED).** Plan frontmatter and Layer-1 commit/PR
  metadata use `feat/sc2egset-02-02-01-symmetry-difference-scaffold`,
  matching PR #241's `feat/sc2egset-02-01-03-history-scaffold` idiom
  (step → family-token → `-scaffold`). Records as **A5**.
- **N2 — CHANGELOG `### Notes` style (APPLIED).** T04 instructions
  require literal `### Notes` subsection heading with bolded `**No X**` /
  `**No Y**` bullets, mirroring PR #264's `## [3.83.0]` `### Notes` block.
  Verified by gate condition 10. Records as **A17**.
- **N3 — slot-orthogonality regex/whitelist (APPLIED).** T01 declares
  `BLOCKED_SLOT_TOKEN_REGEX` covering `player_?\d+`, `slot_?\d+`,
  `p\d+`, `idx_?\d+`, `home`/`away`, `left`/`right`, `host`/`guest`,
  `a_minus_b`/`b_minus_a` — OR equivalent positive whitelist requiring
  `focal` + `opponent` boundary-aware tokens in every difference candidate
  name. T02 parameterises tests over the regex set. Verified by gate
  condition 13. Records as **A8**.
- **N4 — direction annotation Literal (APPLIED).** T01 declares
  `VALID_DIRECTION_LITERAL_VALUES = ("focal_minus_opponent", "symmetric")`;
  `CandidateFeatureSpec` requires `direction: Literal[...]`; T02 includes
  pass + fail tests for invalid direction and for direction-name
  inconsistency (e.g., name contains `_diff` but
  `direction == "symmetric"`). Verified by gate condition 11. Records as
  **A9**.
- **N5 — audited-tuple traceability (APPLIED).** T01 declares
  `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02` (7-tuple) and
  `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03` (24-tuple);
  `CandidateFeatureSpec.source_columns` MUST trace to those tuples; T02
  includes pass + fail tests. Verified by gate condition 11. Records as
  **A10**.
- **N6 — POST_GAME_TOKENS boundary-aware (APPLIED).** T01 declares
  `POST_GAME_TOKEN_REGEX` with `(?:^|_)<token>(?:_|$)` pattern derived
  from the predecessor `POST_GAME_TOKENS` 10-tuple; T02 includes
  positive-control tests asserting `focal_prior_win_rate_decisive` and
  `matchup_h2h_focal_win_rate` do NOT fire the falsifier. Verified by
  gate condition 12. Records as **A11**.
- **N7 — artifact-free = filesystem absence (APPLIED).** T01 declares
  `EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES`;
  `_check_artifact_directories_absent` asserts directory **absence** (not
  emptiness); T02 includes pass + fail tests; T03 sanity-check and
  closing-markdown cells assert absence; gate condition 7 verifies via
  shell `[ ! -d ... ]` checks. Records as **A12**.
- **N8 — notebook `_materialization` suffix (APPLIED).** T03 file paths
  in the manifest and instructions use
  `02_02_01_symmetry_difference_feature_materialization.{py,ipynb}` per
  `sandbox/README.md` single-notebook-per-Step contract + PR #259
  precedent. Records as **A4**.

### Strengths

- **S1 — Atomic boundary correct.** Deferring source-anchor adjudication
  (analogous to PR #234 / PR #242) to a future PR is correctly grounded in
  the merged ROADMAP stub's halt-clause and in the data-analysis-lineage
  non-batching rule. Going straight to materialisation would batch
  sequence steps 2 + 6 + 7, which the rule explicitly forbids.
- **S2 — Artifact-free validator semantics.** The "validator NEVER opens
  Parquet, NEVER writes files" promise is structurally correct for a
  scaffold-stage validator and matches the PR #241 precedent. Scaffold
  validators that touch real Parquet have historically been the source of
  test-suite fragility under data refreshes.
- **S3 — 14-step halting chain in priority order.** The halt order
  (input_parquet_missing → input_parquet_sha_mismatch → parent_audit_json_missing →
  identity_columns_misaligned → context_anchor_misaligned →
  upstream_features_misaligned → artifact_directory_present →
  direction_annotation_invalid → source_column_traceability_violation →
  reconstructed_rating_in_candidates → slot_dependent_token_present →
  target_leak_token_in_candidate → aoe2_vocabulary_in_candidate →
  tracker_sourced_candidate → direction_name_inconsistent) is well-ordered:
  structural existence first, then byte stability, then content semantics.
  Matches the pattern in
  `validate_history_enriched_pre_game_materialization.py`.
- **S4 — Race-pair scope boundary preserved.** Deferring race-pair encoded
  interactions to `02_05` as CANDIDATE-only, with explicit `02_02`-vs-`02_05`
  boundary disclosure, correctly inherits the ROADMAP block's binding
  (lines 2917–2921) and avoids encroaching on Pipeline Section `02_05`.
- **S5 — Status row deferral correctly cited.** The decision to NOT add
  a `PIPELINE_SECTION_STATUS` row for `02_02` and NOT add a `STEP_STATUS`
  row for `02_02_01` correctly mirrors PR #230 (verified: the `02_01` row
  landed at-step-closure of `02_01_01`, not at-step-open).
- **S6 — `reconstructed_rating` exclusion structurally enforced.** No
  reopening of Q5 / Q6 / Q6F / Q6G / Q6H or `reconstructed_rating` per
  the ROADMAP halt_predicate. The validator's
  `forbidden_reconstructed_rating_in_candidates` falsifier enforces this
  structurally via `BLOCKED_FAMILY_FRAGMENTS`.
- **S7 — Version bump 3.83.0 → 3.84.0 (minor) is consistent.** Matches
  PR #232 / PR #233 / PR #239 / PR #241 precedent for `feat/`-class
  scaffold lineage; explicitly correct and not a chore-class patch despite
  no user-facing surface.
- **S8 — Cross-game terminology hygiene preserved.** SC2EGSet uses `race`
  exclusively; no `civilization`. The `FORBIDDEN_AOE2_VOCABULARY`
  falsifier enforces this structurally per Invariant I8.

## Reasoning per challenge axis

1. **Is scaffold + ONE validator the next atomic unit after PR #264?**
   APPROVE. ROADMAP `continue_predicate` at line ~3046 explicitly authorises
   this exact unit ("A future PR may begin the 02_02_01 scaffold + one
   validation module ... only after this ROADMAP stub merges").
   `.claude/rules/data-analysis-lineage.md` sequence step 2 is exactly
   "Notebook scaffold + one validation module" — the next atomic unit after
   the ROADMAP stub (step 1). PR #233 / PR #241 followed this ladder.
2. **Is the Bradley-Terry candidate-family enumeration over-broad or
   under-broad?** APPROVE-WITH-DEFERRAL. Six families enumerated
   (numeric difference, absolute difference, symmetric pair mean/sum/product,
   matchup-history pair operations, cross-region BOOLEAN-pair, race-pair).
   Three open methodology questions (cross-region BOOLEAN-pair → `02_02`
   vs `02_03+`; race-pair → `02_02` vs `02_05`; symmetric pair
   mean/sum/product → tabular Phase 04 vs GNN-comparison scope) deferred
   to the future source-anchor adjudication PR. Ratio features correctly
   excluded from CANDIDATE list (zero-bounded denominators at cold start).
3. **Is the slot-orthogonality falsifier tight enough?** APPROVE-WITH-NITS
   (N3 applied). Token/regex-based blacklist OR positive whitelist enforced
   structurally. **A8** + gate condition 13 + T02 parameterised tests cover
   the slot vocabulary surface.
4. **Is Invariant I5 adequately bound?** APPROVE-WITH-NITS (N4 applied).
   Direction annotation `Literal["focal_minus_opponent", "symmetric"]`
   required per candidate; **A9** + gate condition 11 + T02 pass+fail tests
   enforce structurally rather than as documentation promise.
5. **Is Invariant I3 adequately inherited?** APPROVE-WITH-NITS (N5
   applied). Every candidate's `source_columns` must trace to the audited
   24-tuple or 7-tuple; **A10** + gate condition 11 + T02 pass+fail tests
   convert I3 inheritance into a structural promise.
6. **Is validator naming correctly adjudicated
   (`_materialization` vs `_scaffold`)?** APPROVE. PR #233 / PR #241
   precedent is unambiguous: validator filename carries the family suffix
   from scaffold onward; stage marker lives in docstring. **A2** records.
7. **Is sandbox subdirectory correctly named?** APPROVE.
   `02_symmetry_and_difference_features/` matches ROADMAP lines 2932 +
   3100 verbatim. **A3** records.
8. **Is branch name consistent with PR #241 precedent?** APPROVE-WITH-NIT
   (N1 applied). `feat/sc2egset-02-02-01-symmetry-difference-scaffold`
   matches PR #241's family-token-then-`-scaffold` idiom. **A5** records.
9. **Are 16 tests sufficient?** APPROVE. Predecessor
   `test_validate_history_enriched_pre_game_materialization.py` has ~20
   tests; ~18 for `test_validate_pre_game_feature_materialization.py`.
   Plan targets ≥ 16 as a tight lower bound; parameterisation may grow
   effective count to 20–24. Resolved at reviewer-deep at execution time
   (**OQ12**).
10. **Does POST_GAME_TOKENS substring matching risk false positives?**
    APPROVE-WITH-NIT (N6 applied). Boundary-aware
    `POST_GAME_TOKEN_REGEX = (?:^|_)<token>(?:_|$)` enforced;
    positive-control test cases verify `focal_prior_win_rate_decisive`
    and `matchup_h2h_focal_win_rate` do NOT fire the falsifier. **A11**
    records.
11. **Is the halt-falsifier priority chain in the right order?** APPROVE
    after re-ordering. Plan orders the 14-step chain so structural
    membership halts before content semantics; artifact-directory absence
    fires immediately after upstream-features alignment (before any
    candidate-spec content check), reflecting **A12** (artifact-free is a
    pre-condition, not a content invariant).
12. **Is the no-PIPELINE_SECTION_STATUS-edit decision correct?** APPROVE.
    PR #230 precedent verified: the `02_01` row landed at-step-closure of
    `02_01_01`, not at-step-open. **A16** records.
13. **Is the no-research_log decision correct?** APPROVE.
    `.claude/rules/data-analysis-lineage.md` non-batching sequence step 2
    (scaffold) does NOT append `research_log`; step 8 (formal closure) does.
14. **Is the version-bump policy minor consistent?** APPROVE. Four
    `feat/`-class scaffold precedents bump minor. **A6** records.
15. **Is the CHANGELOG subsection style correct?** APPROVE-WITH-NIT (N2
    applied). Literal `### Notes` heading enforced by T04 instructions and
    gate condition 10. **A17** records.
16. **Is the artifact-free promise mechanically verifiable?**
    APPROVE-WITH-NIT (N7 applied). Filesystem absence check
    (`[ ! -d ... ]`) per **A12** + gate condition 7. False-pass via
    `.gitkeep` / `.DS_Store` mechanically impossible against an absence
    check.
17. **Is the SHA256 pin policy sane?** APPROVE. Halt-on-mismatch semantics
    correct for byte-stability enforcement; gate condition 1 + T01
    constants + T02 pass+fail tests cover. If `02_01_02` or `02_01_03` is
    re-materialised between plan approval and execution, the embedded
    SHAs in T01 will not match and the scaffold notebook HALTS — exactly
    the intended behaviour.
18. **Does the 7-file diff gate prevent stray 8th tracked entities?**
    APPROVE. Gate condition 6 explicitly rejects an 8th tracked entity;
    the sandbox subdirectory itself becomes tracked only via the notebook
    pair inside it.
19. **Should this exist?** YES. The scaffold + ONE validator is the
    correct next atomic unit per `.claude/rules/data-analysis-lineage.md`
    sequence step 2. PR #233 / PR #241 followed exactly this ladder.
    Going directly to materialisation would batch sequence steps 2 + 6 + 7
    (rule violation). Going to a source-anchor adjudication PR first would
    invert PR #233 → PR #234 ordering.
20. **Will this survive examination?** YES — N3 + N4 + N5 + N6 applied,
    making slot-orthogonality, direction-annotation, audited-tuple
    traceability, and boundary-aware leak-token matching all structural
    rather than soft promises. External reviewers can verify the gate is
    a semantic-discipline gate, not just a name-discipline gate.
21. **What is the smallest defect that would invalidate the gate?** The
    cheapest passing-but-leaky path BEFORE nits applied: an executor names
    a candidate column `focal_minus_opponent_apm_diff` whose underlying
    semantics are `slot1_apm - slot2_apm`. The validator (a) does NOT open
    the Parquet at scaffold stage (correctly), (b) does NOT see the SQL/
    Python definition (no source-anchor binding yet — that's PR #234-analogue
    work), and (c) name-pattern-matches only. Without N4 + N5, the column
    name passes every falsifier. AFTER N4 + N5 applied (this plan): the
    candidate carries `direction="focal_minus_opponent"` and
    `source_columns=("slot1_apm","slot2_apm")` — and the traceability
    falsifier fires because `slot1_apm` and `slot2_apm` are NOT in the
    audited 24-tuple. Gate condition 11 verifies the constants exist and
    the tests pass. **Therefore: with N4 + N5 applied, the cheapest
    gate-defeating defect now requires the executor to manually edit the
    `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03` constant to insert
    fabricated source columns** — a far more visible and reviewable
    violation than name-discipline drift.

## Open methodology questions deferred to the future source-anchor adjudication PR

1. **O1 — Cross-region BOOLEAN-pair scope (Family 5).** Does cross-region
   BOOLEAN-pair handling belong in `02_02` (Symmetry & Difference Features)
   or in `02_03+` (Temporal Features / Boolean-pair encoding)? Enumerated
   as CANDIDATE in `02_02` Family 5; binding decision deferred to the
   future PR analogous to PR #234. The `02_01_03` precedent is that the
   cross-region indicator family was materialised as a paired BOOLEAN
   `is_cross_region_fragmented_{focal,opponent}_history_any`, which is
   structurally a focal/opponent pair (qualifies as `02_02` Symmetry).
2. **O2 — Race-pair categorical scope (Family 6).** Does race-pair
   encoded interaction belong in `02_02` or in `02_05`? ROADMAP block
   lines 2917–2921 defers this binding to the future PR-#234-analogue.
   The scaffold's enumeration as CANDIDATE-only with `02_05` deferral
   annotation is correct procedure, but the binding decision is owed.
3. **O3 — Symmetric pair mean/sum/product scope (Family 3).** Does
   symmetric pair aggregation (mean/sum/product) belong in tabular Phase 04
   scope at all, or is it more naturally a GNN-comparison-scope construct?
   Bradley-Terry argues that **difference** features are slot-orthogonal;
   symmetric pair aggregates (mean/sum/product) are weaker than differences
   for pairwise prediction but stronger than concatenation. Should be
   argued explicitly in the adjudication PR's
   `02_FEATURE_ENGINEERING_MANUAL.md §3` binding.
4. **O4 — Materialisation-stage I5 enforcement.** The scaffold-stage
   validator enforces I5 via name/direction/traceability checks on
   candidate specs (structural per **A8/A9/A10**). The future
   materialisation-stage validator must additionally enforce I5 on
   produced Parquet rows (e.g., assert that the materialised
   `focal_minus_opponent_apm_diff` column equals `focal_apm − opponent_apm`
   row-by-row). The materialisation-stage CROSS-02-01 audit must include
   `reconstructed_rating_in_candidates` as a structural falsifier on the
   actual Parquet column schema (not just the design contract).
5. **O5 — Ratio family inclusion.** Per the Literature Context [OPINION]
   paragraph in the plan, ratio features are not enumerated as CANDIDATE
   because most history columns have zero-bounded denominators (cold-start
   undefined values). If the future adjudication PR judges this too
   conservative, ratios can be added without validator change (the
   candidate-spec tuple is opaque to the validator's content beyond
   direction + source_columns checks).

## Files verified during review

- `/Users/tomaszpionka/Projects/rts-outcome-prediction/.claude/scientific-invariants.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/.claude/ml-protocol.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/.claude/rules/data-analysis-lineage.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/docs/PHASES.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/docs/ml_experiment_lifecycle/02_FEATURE_ENGINEERING_MANUAL.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/reports/specs/02_02_feature_engineering_plan.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/reports/specs/02_03_temporal_feature_audit_protocol.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
  (Step `02_02_01` block at lines 2853–3131)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
  (`02_01_03: complete`; no `02_02_01` row)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
  (`02_01: complete`; no `02_02` row)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`
  (Phase 02 = `in_progress`; Phase 03 = `not_started`)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py`
  (PR #241 scaffold-stage validator precedent)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/validate_pre_game_feature_materialization.py`
  (PR #233 scaffold-stage validator precedent)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_pre_game_feature_materialization.py`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json`
  (7 audited features)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.json`
  (24 audited features)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/CHANGELOG.md`
  (PR #264 `### Notes` precedent at the `## [3.83.0]` block)

## Three-question test answers

1. **Should this exist?** YES. Scaffold + ONE validator is the correct next
   atomic unit per `.claude/rules/data-analysis-lineage.md` sequence
   step 2. PR #233 (02_01_02) and PR #241 (02_01_03) ladders both followed
   exactly this sequence (ROADMAP stub → scaffold + 1 validator →
   adjudication → materialisation → audit → formal closure). Going
   directly to materialisation would batch sequence steps 2 + 6 + 7
   (rule violation). Going to source-anchor adjudication first would
   invert PR #233 → PR #234 ordering.
2. **Will this survive examination?** YES. With N3 + N4 + N5 + N6 + N7
   applied (all confirmed in plan body), the validator gate is a
   semantic-discipline gate rather than a name-discipline gate. An
   external reviewer can verify that: (a) every candidate carries an
   explicit `direction` Literal annotation enforced structurally; (b)
   every candidate's `source_columns` trace to the frozen audited 24-tuple
   or 7-tuple; (c) slot-orthogonality is enforced via regex/whitelist
   covering player/slot/p/idx/home/away/left/right/host/guest/a/b token
   variants; (d) boundary-aware `POST_GAME_TOKEN_REGEX` does not
   false-positive on legitimate `win_rate` substrings; (e) the
   artifact-free promise is mechanically defensible as filesystem absence.
3. **What is the smallest defect that would invalidate the gate?** With
   N4 + N5 applied, the cheapest gate-defeating defect now requires the
   executor to manually edit the
   `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02` or
   `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03` constant to insert
   fabricated source-column names — a visible, reviewable, git-blame-able
   violation rather than silent name-discipline drift. The pre-commit
   hook + reviewer-deep pass at Layer-2 execution time would catch it.

## Recommended next step

**Materialize the Layer-1 draft PR** (this critique recommends approval;
all 8 nits applied to plan body at Layer-1 materialisation per user
direction 2026-05-29). The draft PR must keep the diff scoped to exactly:

- `planning/current_plan.md`
- `planning/current_plan.critique.md`

No ROADMAP edit, no status YAML, no research_log, no CHANGELOG, no
pyproject, no INDEX, no source/test/notebook/artifact change in this
Layer-1 PR. Layer-2 execution (the actual scaffold + validator + notebook
materialisation, plus the 3 documentation/manifest files) runs in a
separate execution prompt on the same branch
(`feat/sc2egset-02-02-01-symmetry-difference-scaffold`).
