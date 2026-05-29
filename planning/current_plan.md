---
title: "SC2EGSet Step 02_02_01 scaffold + one validation module (Layer-1 planning PR)"
category: A
branch: feat/sc2egset-02-02-01-symmetry-difference-scaffold
base_ref: master
base_sha: 7f2506edb993937084a613fbea6dc4edc2a51635
predecessor_pr: 264
predecessor_pr_merge_sha: 7f2506edb993937084a613fbea6dc4edc2a51635
dataset: sc2egset
phase: "02"
pipeline_section: "02_02 — Symmetry & Difference Features"
invariants_touched: [I3, I5, I6, I7, I8, I9, I10]
draft_pr_files:
  - planning/current_plan.md
  - planning/current_plan.critique.md
future_execution_files:
  - src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py
  - tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_symmetry_difference_feature_materialization.py
  - sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.py
  - sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.ipynb
  - pyproject.toml
  - planning/INDEX.md
  - CHANGELOG.md
future_execution_file_count: 7
target_version_bump: "3.83.0 -> 3.84.0"
critique_required: true
research_log_ref: null
date: "2026-05-29"
---

## Scope

Execute `.claude/rules/data-analysis-lineage.md` "Non-batching rule for empirical
work" sequence step 2 ("Notebook scaffold + one validation module") for SC2EGSet
Step `02_02_01` (Pipeline Section `02_02 — Symmetry & Difference Features`).
PR #264 (merged 2026-05-29 at master `7f2506ed`) inserted the ROADMAP-only stub.
The next atomic unit is one scaffold + one validation module pass, mirroring
PR #233 for Step `02_01_02` and PR #241 for Step `02_01_03`.

**Two-PR sequence on branch `feat/sc2egset-02-02-01-symmetry-difference-scaffold`.**

1. **THIS Layer-1 planning PR** writes only two files:
   - `planning/current_plan.md` (this document);
   - `planning/current_plan.critique.md` (reviewer-adversarial output).
2. **FUTURE Layer-2 execution PR on the same branch** performs the 7-file
   manifest below (validator + mirrored test + jupytext notebook pair +
   `pyproject.toml` + `planning/INDEX.md` + `CHANGELOG.md`).

**Explicitly out of scope** for both PRs:

- feature value materialization (NO Parquet, NO CSV, NO MD/JSON artifact under
  `reports/artifacts/02_02_01/` or
  `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`);
- source-anchor / column-naming binding adjudication (analogous to PR #234 /
  PR #242 for `02_01_02` and `02_01_03`); the candidate-family enumeration in
  the T03 notebook is CANDIDATE-only; the binding decision is taken in a
  separate future PR;
- STEP_STATUS.yaml additions for `02_02_01` (closure deferred to a future
  U2.B-style PR analogous to PR #237 / PR #262 post-materialisation);
- PIPELINE_SECTION_STATUS.yaml `02_02` row addition (deferred per PR #230
  precedent — section row first lands at step closure, not at scaffold);
- PHASE_STATUS.yaml mutation (Phase 02 stays `in_progress`; Phase 03 stays
  `not_started`);
- ROADMAP.md edits anywhere (the `02_02_01` block at lines 2853–3131 remains
  byte-identical; no edits to Steps `02_01_01`, `02_01_02`, `02_01_03`,
  `02_01_99`, or the §02_01_03 amendment back-references);
- root `reports/research_log.md` and per-dataset `research_log.md` edits
  (per data-analysis-lineage non-batching-rule sequence — research_log is
  appended only at step closure, sequence step 8; not at scaffold, sequence
  step 2);
- thesis chapters, bib, appendix, `docs/**`, `.claude/**`, `data/**`;
- any AoE2 path under `src/rts_predict/games/aoe2/**`;
- Step `02_02_02+`; Step `02_01_04`; Phase 03; any baseline modeling;
- reopen of Q5 / Q6 / Q6F / Q6G / Q6H / `reconstructed_rating` closure;
- new MMR scalar feature (PR #234 `is_mmr_missing` flag precedent stands);
- AoE2 `civilization` vocabulary (SC2EGSet uses `race` exclusively per
  Invariant I8 cross-game hygiene).

## Problem Statement

PR #264 inserted a ROADMAP-only stub for Step `02_02_01` opening Pipeline
Section `02_02 — Symmetry & Difference Features`. The stub authorises a
future scaffold + validator PR (ROADMAP `continue_predicate` at line ~3046:
"A future PR may begin the 02_02_01 scaffold + one validation module
(analogous to PR #241 for 02_01_03) only after this ROADMAP stub merges.")
but emits no notebook, no validator, no test, and no machine-checkable
candidate-feature enumeration.

Without that scaffold-stage design contract:

1. The next link in the lineage chain — the future source-anchor /
   column-naming adjudication PR analogous to PR #234, and after it the
   materialisation PR analogous to PR #259 — has no machine-checkable surface
   to bind against.
2. The candidate symmetric/difference feature family list lives only in
   ROADMAP prose, with no `direction` annotation per candidate and no
   audited-tuple traceability check.
3. The Bradley-Terry-grounded slot-orthogonality invariant (Invariant I5)
   has no structural enforcement at the model-input layer — it lives only as
   a row-level structural invariant in `02_01_03`'s symmetric `focal_*` /
   `opponent_*` column pairs.

`.claude/rules/data-analysis-lineage.md` "Non-batching rule" sequence step 2
prescribes exactly this unit: a notebook scaffold with one validation module,
executed and reviewed before any artifact generation. Both predecessors
followed this ladder (PR #233 for Step `02_01_02`; PR #241 for Step
`02_01_03`). The current gap is therefore the missing scaffold-stage
design-contract validator and notebook for Step `02_02_01`, which this plan
addresses.

This step is methodology-sensitive because `02_02` is the layer at which
Invariant I5 (focal/opponent symmetry) transitions from a row-level
structural invariant (already enforced upstream in `02_01_03`'s symmetric
`focal_*` / `opponent_*` column pairs) into a model-input invariant
(slot-orthogonal difference and symmetric pair features). The scaffold must
encode the Bradley-Terry argument from `02_FEATURE_ENGINEERING_MANUAL.md` §3
as machine-checkable falsifiers — chiefly the slot-orthogonality of every
candidate difference (`focal_value − opponent_value`, never
`player_1_value − player_2_value`) and the structural requirement that every
candidate column-name trace to an audited source column.

## Literature Context

`02_FEATURE_ENGINEERING_MANUAL.md` §3 ("Symmetry in Pairwise Prediction
Demands Difference Features", lines 43–59) establishes the Bradley-Terry
connection (Bradley & Terry 1952, "Rank analysis of incomplete block
designs: I. The method of paired comparisons"): for latent strengths β_i,
`P(i > j) = 1 / (1 + e^(β_j − β_i))`, so the logit of win probability equals
the **difference** of latent strengths. The manual at line 47 reads
"directly motivates difference features as the theoretically grounded
representation for pairwise prediction." Four representations are listed:
difference (preferred default), ratio, canonical-ordering-with-concatenation,
and symmetric kernels (Hue & Vert ICML 2010, "On learning with kernels for
unordered pairs"; Zaheer et al. 2017, "Deep Sets"). The scaffold MUST encode
"difference as default" as the binding falsifier shape for candidate
transforms; ratio / kernel families are CANDIDATE-only and deferred to GNN
comparison scope.

`.claude/scientific-invariants.md` Invariant I5 (lines 156–170) binds this
thesis: "Both players in every game must be treated identically by the
feature pipeline ... The model input is always structured as
`(focal_player_features, opponent_features, context_features)` and this
structure is identical regardless of which player is focal." The
slot-orthogonality falsifier (`focal_value − opponent_value`, never
`player_1_value − player_2_value`) is a direct binding of Invariant I5 at
the model-input layer.

Invariant I3 (lines 130–148) binds the temporal cutoff that any
symmetric/difference feature inherits: `history_time < target_time` strict;
normalization scoped to training folds. `.claude/ml-protocol.md` enumerates
the three leakage failure modes that `02_02` design must not break
(rolling aggregates including game T; head-to-head including game T;
co-occurring matches). The scaffold's leakage falsifier list MUST enumerate
all three as inherited-from-upstream and not re-introduced by any candidate
`02_02` transform.

Section 6 of the same manual catalogues categorical-pair interaction
encoding (`race × opponent_race`) as the standard pre-game pair feature —
and this interaction-encoding scope belongs to Pipeline Section `02_05`
(Categorical Encoding & Interactions), not `02_02`. The scaffold annotates
race-pair candidates as CANDIDATE-only with explicit `02_05` deferral; the
binding `02_02`-vs-`02_05` boundary decision is taken in the future
source-anchor adjudication PR analogous to PR #234, not in this scaffold.

`reports/specs/02_03_temporal_feature_audit_protocol.md` is the downstream
temporal-window/decay/cold-start audit spec that `02_02` difference features
will eventually feed into; referenced here so the scaffold's halt-clauses
do not silently encroach on `02_03` scope.

[OPINION] The scaffold should NOT enumerate ratio features
(`focal_value / opponent_value`) as CANDIDATE for the `02_01_03` history
columns because most history columns include zero-bounded denominators
(`opponent_prior_match_count = 0` at cold start; `opponent_prior_win_rate`
undefined when `opponent_prior_match_count = 0`). The Bradley-Terry argument
is satisfied by differences alone for the tabular Phase 04 scope. Ratio is
in the manual but is a model-driven choice (multiplicative relationships);
for log-transformed candidate columns the log-difference is exactly a
difference. The binding source-anchor adjudication PR may revisit.

## Assumptions & Unknowns

- **A1 (Outcome A justified).** Outcomes B–G rejected (see
  `current_plan.critique.md` §"Adjudication outcomes"). Outcome A is the only
  sequence-step-2-compliant outcome under
  `.claude/rules/data-analysis-lineage.md`.
- **A2 (Validator family naming, NOT scaffold-suffixed).** Both predecessor
  validators are named `validate_<family>_materialization.py` even at the
  scaffold stage (PR #233 → `validate_pre_game_feature_materialization.py`;
  PR #241 → `validate_history_enriched_pre_game_materialization.py`). The
  filename carries the family suffix from scaffold onward and never renames;
  the stage marker lives in the module docstring. Therefore the validator
  here is `validate_symmetry_difference_feature_materialization.py`, not
  `..._scaffold.py`.
- **A3 (Sandbox subdir = `02_symmetry_and_difference_features/`).** ROADMAP
  block lines 2932 and 3100 spell the future sandbox subdir with `_and_`
  (`02_symmetry_and_difference_features/`), not the shorter
  `02_symmetry_difference_features/`. Plan matches ROADMAP verbatim.
- **A4 (Notebook filename uses `_materialization` suffix per overwrite
  contract).** Reviewer-adversarial N8: per `sandbox/README.md`
  single-notebook-per-Step contract (cf. PR #259 CHANGELOG `### Added`:
  "PR #241 scaffold OVERWRITTEN in place per sandbox/README.md ..."), the
  notebook is overwritten at materialisation, not renamed. PR #241's
  notebook went straight to
  `02_01_03_history_enriched_pre_game_feature_materialization.{py,ipynb}` at
  scaffold time and was overwritten in place at PR #259. Plan matches.
- **A5 (Branch naming follows PR #241 idiom).** Reviewer-adversarial N1:
  PR #241 branch was `feat/sc2egset-02-01-03-history-scaffold` (step →
  family-token → `-scaffold`); PR #233 branch was
  `feat/sc2egset-02-01-02-pre-game-materialization-scaffold`. The chosen
  branch `feat/sc2egset-02-02-01-symmetry-difference-scaffold` matches the
  PR #241 idiom.
- **A6 (Version bump 3.83.0 → 3.84.0).** Minor; matches PR #233 / PR #241
  precedent for `feat/`-class scaffold lineage (PR #232: 3.66.0 → 3.67.0;
  PR #233: 3.67.0 → 3.68.0; PR #239: 3.70.1 → 3.71.0; PR #241: 3.71.0 →
  3.72.0). Per `.claude/rules/git-workflow.md` "minor for feat/refactor/docs."
  The bump lands in the Layer-2 execution PR, not in this Layer-1 planning PR.
- **A7 (Upstream artifacts are byte-stable at named SHAs).** Verified
  2026-05-29 SHA256:
  - `02_01_02_pre_game_features.parquet` =
    `24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39`
    (719,068 B);
  - `02_01_03_history_enriched_pre_game_features.parquet` =
    `053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071`
    (2,451,869 B).
  These SHAs MUST be embedded as module-level constants in T01's validator
  and re-checked at every notebook run. The two parent audit JSONs
  (`02_01_02/leakage_audit_sc2egset.json` and
  `02_01_03/leakage_audit_sc2egset.json`) are also present at their canonical
  paths and must be re-checked by `json.load()` (no Parquet reads).
- **A8 (Slot-orthogonality enforcement is structural, not substring).**
  Reviewer-adversarial N3: the validator MUST enforce slot-orthogonality via
  a token/regex frozenset covering `player_?\d+`, `slot_?\d+`, `p\d+`,
  `idx_?\d+`, `home`/`away`, `left`/`right`, `host`/`guest`, `a_minus_b` /
  `b_minus_a` — OR equivalently invert into a positive whitelist that
  requires every difference candidate's name to contain the exact token
  `focal_minus_opponent` or `_focal_minus_opponent_` and be derivable from a
  `focal_*` / `opponent_*` source-pair in the audited 24-tuple. A fixed
  literal blacklist (e.g., only blocking `player_1 - player_2`) is
  insufficient.
- **A9 (Direction annotation required per candidate).**
  Reviewer-adversarial N4: every future candidate feature must carry an
  explicit `direction: Literal["focal_minus_opponent", "symmetric"]`
  annotation. The validator MUST enforce that any candidate whose name
  contains `_diff` / `_minus_` has `direction == "focal_minus_opponent"`,
  and any candidate whose name contains `_pair_mean` / `_pair_sum` /
  `_pair_product` / `_abs_diff` has `direction == "symmetric"`. If a future
  source-anchor adjudication PR revises this requirement, it must do so
  explicitly and document the rationale.
- **A10 (Audited-tuple traceability required).** Reviewer-adversarial N5:
  every candidate column name must trace to source columns in the audited
  24-tuple from `02_01_03` (audit JSON `features_audited`) OR the 7-tuple
  from `02_01_02` (audit JSON `features_audited`). The validator MUST reject
  any candidate whose source-column basis cannot be located in those tuples.
  This converts I3 inheritance from a documentation promise into a
  structural promise: transforms cannot introduce new source semantics at
  the `02_02` layer.
- **A11 (POST_GAME_TOKENS must be boundary-aware).**
  Reviewer-adversarial N6: the leakage-token sweep MUST use boundary-aware
  regex `(?:^|_)<token>(?:_|$)`, not raw substring matching, to avoid
  false-positiving on `focal_prior_win_rate_decisive` (legitimate `win`
  substring) or `matchup_h2h_focal_win_rate` (legitimate `win` substring).
  Positive-control tests must verify these names do NOT fire the
  `target_leak_token_in_candidate` falsifier.
- **A12 (Artifact-free promise = filesystem absence).**
  Reviewer-adversarial N7: the artifact-free-promise check MUST assert
  filesystem **absence** of `reports/artifacts/02_02_01/` AND
  `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`,
  not directory emptiness. A `.DS_Store` / `.gitkeep` file inside an
  otherwise-empty directory would false-pass an emptiness check; absence is
  the only mechanically-defensible promise at scaffold stage.
- **A13 (`02_01_03` Parquet column space).** The Parquet contains:
  3 identity columns (`focal_match_id`, `focal_player_id`, and the third
  identity column listed in `02_01_03/leakage_audit_sc2egset.json`
  `projected_identity_columns`); 1 context anchor (`started_at`); 24
  audited features split across 5 families per
  `02_01_03/leakage_audit_sc2egset.json` `features_audited` (verbatim
  source-of-truth). The scaffold reads the audit JSON to source these
  tuples, never re-derives them.
- **A14 (Cross-region indicator handling preserves PR #243 / PR #255
  lineage).** Any `02_02` family that consumes
  `cross_region_fragmentation_handling` columns from the `02_01_03` Parquet
  must respect PR #243 Q5 cross-region adjudication and PR #255
  omit-closure scope (sensitivity-indicator co-registration arm selected —
  preserved verbatim in PR #259 materialisation). The `02_02` work inherits
  this co-registration unchanged; the cross-region indicator is a
  candidate symmetric/BOOLEAN-pair source, not a difference-feature input
  via numeric subtraction.
- **A15 (`reconstructed_rating` family stays excluded).** PR #255
  omit-closure + PR #257 amendment + PR #259 materialisation unanimously
  excluded the `reconstructed_rating` family; `02_02` must not silently
  re-include `reconstructed_rating_focal_pre`, `reconstructed_rating_opp_pre`,
  or `reconstructed_rating_diff` under a difference-feature pretence. The
  validator's `reconstructed_rating_in_candidates` falsifier enforces this
  structurally via the `BLOCKED_FAMILY_FRAGMENTS` constant.
- **A16 (PIPELINE_SECTION_STATUS `02_02` row deferred).** The `02_02` row
  addition is deferred to a future PR per the verified `02_01` precedent:
  section row first landed in PR #230 (closure of `02_01_01`), not in the
  section's stub or scaffold PR. The natural moment to add `02_02` is when
  the first `02_02` step closes (mirrors `02_01` ladder).
- **A17 (CHANGELOG subsection style = `### Notes` with bolded `**No X**`
  bullets).** Reviewer-adversarial N2: PR #264's `## [3.83.0]` block uses
  `### Added` and a literal `### Notes` subsection with bolded `**No X**` /
  `**No Y**` bullets. The Layer-2 CHANGELOG entry must mirror this style
  verbatim; "Excluded" or "Not changed" wording is a paraphrase that does
  NOT match repo convention.
- **A18 (CHANGELOG PR-number placeholder).** Layer-2 CHANGELOG header uses
  `PR #<TBD>` at PR-open time, swept to the real number by a follow-up
  housekeeping commit pre-merge (mirrors PR #264's `65cb8a93 chore: normalize
  PR #<TBD> placeholders to PR #264`).
- **U1 (Notebook authoring vs validator parameter signature).** The T01
  validator's three-parameter `designed_*_column_names` signature
  (mirroring `02_01_03`'s pattern) means the candidate-family enumeration
  lives in the notebook, not in the validator. This is deliberate (keeps the
  validator pure and artifact-free) but means the validator does NOT
  enforce a minimum/maximum count of candidate columns. The reviewer
  confirmed this is acceptable for scaffold stage.
- **U2 (Exact 16-test count vs predecessor coverage shape).** Predecessor
  `test_validate_history_enriched_pre_game_materialization.py` (PR #241) has
  ~20 tests; `test_validate_pre_game_feature_materialization.py` (PR #233)
  has ~18 tests. Target 16 tests as a tight lower bound; if T02
  parameterisation grows the count to 20–24 effective cases, that is
  acceptable. Resolves by: reviewer-deep at execution time.
- **U3 (Exact subset of difference families with strong methodological
  motivation).** The scaffold ENUMERATES candidate transforms per
  column-class but does not commit to a final list — the binding decision
  is in the future source-anchor adjudication PR (analogous to PR #234).
  Resolves by: future adjudication PR.

## Execution Steps

**Layer-1 (THIS PR — planning-only):**

L1.1 Read: `.claude/scientific-invariants.md`, `.claude/ml-protocol.md`,
`.claude/rules/data-analysis-lineage.md`, `.claude/rules/git-workflow.md`,
`.claude/rules/python-code.md`, `.claude/rules/sql-data.md`,
`docs/PHASES.md`, `docs/TAXONOMY.md`,
`docs/ml_experiment_lifecycle/02_FEATURE_ENGINEERING_MANUAL.md`,
`reports/specs/02_00_feature_input_contract.md`,
`reports/specs/02_01_leakage_audit_protocol.md`,
`reports/specs/02_02_feature_engineering_plan.md`,
`reports/specs/02_03_temporal_feature_audit_protocol.md`,
the dataset's `PHASE_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` /
`STEP_STATUS.yaml` / `ROADMAP.md` (especially the `02_02_01` block) /
`research_log.md`, the master HEAD diff for PR #264, the `02_01_02` and
`02_01_03` audit JSONs (no Parquet value reads), and the precedent validator
files `validate_pre_game_feature_materialization.py` (PR #233) and
`validate_history_enriched_pre_game_materialization.py` (PR #241) plus their
mirrored test files. All read-only.

L1.2 Confirm verified state matches the lookup-PASS section of the
predecessor prompt: master HEAD `7f2506ed`, pyproject `3.83.0`,
STEP_STATUS `02_01_03: complete`, no `02_02_01` row, ROADMAP `02_02_01`
block at lines 2853–3131 byte-unchanged, audit artifacts byte-stable at the
named SHAs.

L1.3 Author `planning/current_plan.md` (this document). Pre-commit hook
sanity (`feedback_plan_required_sections.md`): the document MUST have
`## Scope`, `## Problem Statement`, `## Literature Context`,
`## Assumptions & Unknowns`, `## Execution Steps`, `## File Manifest`,
`## Gate Condition`, `## Open Questions`. Verified inline.

L1.4 Author `planning/current_plan.critique.md` recording reviewer-adversarial
APPROVE-WITH-NITS (0 blockers, 8 nits) verdict, with each nit annotated as
APPLIED-TO-PLAN-BODY at Layer-1 materialisation.

L1.5 Open draft PR with exactly those two files. Branch
`feat/sc2egset-02-02-01-symmetry-difference-scaffold` off master `7f2506ed`.
PR body in `.github/tmp/pr.txt` per `feedback_pr_body_file.md`; delete after
PR opens (`feedback_pr_body_cleanup.md`).

**Layer-2 (FUTURE execution PR — same branch — DO NOT execute now):**

### T01 — Author the scaffold-stage design-contract validator

**Objective:** Create
`src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py`
— a pure-function validator module that enforces the `02_02_01` scaffold
design contract against the two byte-stable upstream Parquet artifacts and
against notebook-declared CANDIDATE column-name tuples with per-candidate
`direction` annotations. The module writes NO files, materialises NO
features, and returns a frozen dataclass result. The naming convention
matches the predecessor pattern (PR #233 / PR #241):
`validate_<family>_materialization.py` from scaffold onward; the docstring
carries the stage marker.

**Instructions:**

1. Module docstring opens with:
   `"""Validation module for SC2EGSet Step 02_02_01 symmetry & difference feature scaffold (scaffold-only).`
   Mirrors the predecessor `validate_pre_game_feature_materialization.py`
   line 1 wording.
2. Declare module-level constants (Invariant I7 — no magic numbers):
   - `INPUT_02_01_02_PARQUET_RELPATH: str` and `INPUT_02_01_03_PARQUET_RELPATH: str`
     — canonical relative paths from ROADMAP `inputs.prior_artifacts`.
   - `INPUT_02_01_02_PARQUET_SHA256: str = "24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39"`
     and `INPUT_02_01_03_PARQUET_SHA256: str = "053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071"`
     — measured 2026-05-29; bind I10 (relative-path provenance) and I9
     (prior-artifact dependency).
   - `EXPECTED_PARENT_AUDIT_JSON_RELPATHS: tuple[str, str]` — the two
     `leakage_audit_sc2egset.json` relpaths from ROADMAP `inputs.prior_artifacts`.
   - `IDENTITY_COLUMNS: tuple[str, ...]` — read literally from `02_01_03`
     audit JSON `projected_identity_columns`.
   - `CONTEXT_ANCHOR_COLUMNS: tuple[str, ...] = ("started_at",)` — read
     literally from `02_01_03` audit JSON `projected_context_columns`.
   - `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03: tuple[str, ...]` — the
     24-tuple from `02_01_03` audit JSON `features_audited`, frozen verbatim.
   - `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02: tuple[str, ...]` — the
     7-tuple from `02_01_02` audit JSON `features_audited`, frozen verbatim.
   - `BLOCKED_SLOT_TOKEN_REGEX: tuple[str, ...]` — regex pattern set
     enforcing **A8** (reviewer-adversarial N3). MUST cover at minimum:
     `r"(?:^|_)player_?\d+(?:_|$)"`, `r"(?:^|_)slot_?\d+(?:_|$)"`,
     `r"(?:^|_)p\d+(?:_|$)"`, `r"(?:^|_)idx_?\d+(?:_|$)"`,
     `r"(?:^|_)home(?:_|$)"`, `r"(?:^|_)away(?:_|$)"`,
     `r"(?:^|_)left(?:_|$)"`, `r"(?:^|_)right(?:_|$)"`,
     `r"(?:^|_)host(?:_|$)"`, `r"(?:^|_)guest(?:_|$)"`,
     `r"(?:^|_)a_minus_b(?:_|$)"`, `r"(?:^|_)b_minus_a(?:_|$)"`.
     Equivalent positive-whitelist option (per **A8** alternative): require
     every `direction == "focal_minus_opponent"` candidate's name to contain
     the literal token sequence `focal` and `opponent` (boundary-aware),
     and reject names that do not.
   - `BLOCKED_FAMILY_FRAGMENTS: tuple[str, ...] = ("reconstructed_rating", "reconstructed_rating_focal_pre", "reconstructed_rating_opp_pre", "reconstructed_rating_diff")`
     — PR #255 / PR #257 binding exclusion (per **A15**).
   - `POST_GAME_TOKENS: tuple[str, ...]` — copy the existing 10-tuple from
     `validate_history_enriched_pre_game_materialization.py` lines 100–111
     verbatim for consistency across validators.
   - `POST_GAME_TOKEN_REGEX: tuple[str, ...]` — boundary-aware variants
     `(?:^|_)<token>(?:_|$)` derived from `POST_GAME_TOKENS`, per **A11**
     (reviewer-adversarial N6). MUST be used in the falsifier sweep instead
     of raw `in` substring checks.
   - `FORBIDDEN_AOE2_VOCABULARY: tuple[str, ...] = ("civilization", "civ")`
     — Invariant I8 cross-game hygiene.
   - `TRACKER_SOURCE_PREFIX: str = "tracker_events_raw"` — copy from
     predecessor; tracker-derived target-match features stay banned at this
     layer.
   - `EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES: tuple[str, ...]` — paths
     under `reports/artifacts/02_02_01/` and
     `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`.
     Used by the artifact-free-promise check per **A12**
     (reviewer-adversarial N7).
   - `VALID_DIRECTION_LITERAL_VALUES: tuple[str, str] = ("focal_minus_opponent", "symmetric")`
     — the only two allowed values for the per-candidate `direction`
     annotation per **A9** (reviewer-adversarial N4).
3. Define a frozen dataclass `CandidateFeatureSpec` (or namedtuple)
   per **A9**:
   ```python
   @dataclass(frozen=True)
   class CandidateFeatureSpec:
       column_name: str
       direction: Literal["focal_minus_opponent", "symmetric"]
       source_columns: tuple[str, ...]  # must trace to audited tuples per A10
   ```
4. Define the result dataclass
   `SymmetryDifferenceScaffoldValidationResult` (frozen) with at least these
   fields:
   - `input_parquet_paths_present_ok: bool`
   - `input_parquet_sha256_ok: bool`
   - `parent_audit_json_paths_present_ok: bool`
   - `identity_columns_aligned_ok: bool`
   - `context_anchor_columns_aligned_ok: bool`
   - `upstream_feature_columns_aligned_ok: bool`
   - `direction_annotation_valid: tuple[CandidateFeatureSpec, ...]`
     (empty if all valid; non-empty lists offending candidates per **A9**)
   - `source_column_traceability_violations: tuple[CandidateFeatureSpec, ...]`
     (empty if all candidates' `source_columns` are in the audited tuples
     per **A10**)
   - `forbidden_reconstructed_rating_in_candidates: tuple[str, ...]`
   - `slot_dependent_token_violations: tuple[tuple[str, str], ...]`
     (column_name, matched_regex_pattern) — per **A8**
   - `target_leak_tokens_in_candidates: tuple[tuple[str, str], ...]`
     (column_name, matched_regex_pattern) — per **A11**
   - `aoe2_vocabulary_in_candidates: tuple[tuple[str, str], ...]`
   - `tracker_sourced_candidates: tuple[str, ...]`
   - `direction_name_consistency_violations: tuple[CandidateFeatureSpec, ...]`
     (e.g., name contains `_diff` / `_minus_` but
     `direction != "focal_minus_opponent"`) — per **A9**
   - `materialized_output_paths: tuple[str, ...] = field(default_factory=tuple)`
     — always `()`; verified by an absence-check per **A12**
   - `artifact_directory_absence_ok: bool` — per **A12**
   - `halting_falsifier: str | None`
   - `passed: bool`
5. Public function:
   ```python
   def validate_symmetry_difference_feature_materialization(
       input_02_01_02_parquet_path: Path | str,
       input_02_01_03_parquet_path: Path | str,
       parent_audit_json_paths: tuple[Path | str, Path | str],
       designed_difference_specs: tuple[CandidateFeatureSpec, ...],
       designed_symmetric_pair_specs: tuple[CandidateFeatureSpec, ...],
       designed_race_pair_candidate_specs: tuple[CandidateFeatureSpec, ...],
   ) -> SymmetryDifferenceScaffoldValidationResult:
   ```
   The function performs ONLY: (a) `Path.exists()` checks; (b)
   `hashlib.sha256` byte-stream check; (c) `json.load()` and equality check
   on `features_audited` / `projected_identity_columns` /
   `projected_context_columns`; (d) per-spec direction-annotation validity
   check per **A9**; (e) per-spec `source_columns` traceability check per
   **A10**; (f) regex-based slot-token sweep per **A8**; (g) boundary-aware
   regex sweep over `POST_GAME_TOKEN_REGEX` per **A11**; (h) AoE2 vocab
   sweep; (i) tracker-prefix sweep; (j) `BLOCKED_FAMILY_FRAGMENTS` sweep;
   (k) direction-name consistency check (e.g., `_diff` ↔
   `focal_minus_opponent`); (l) filesystem absence check on
   `EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES` per **A12**. It does NOT open
   any Parquet file, does NOT compute any aggregate, does NOT write any
   path.
6. Define private check helpers mirroring the shape of
   `validate_history_enriched_pre_game_materialization.py` helpers:
   `_check_input_artifacts_present`,
   `_check_input_artifact_sha256_byte_stability`,
   `_check_parent_audit_jsons_present`,
   `_check_identity_and_context_column_alignment`,
   `_check_upstream_feature_columns_alignment`,
   `_check_direction_annotation_validity` (per **A9**),
   `_check_source_column_traceability` (per **A10**),
   `_check_no_reconstructed_rating_in_candidates`,
   `_check_no_slot_dependent_tokens` (regex-based, per **A8**),
   `_check_no_target_leak_tokens_boundary_aware` (per **A11**),
   `_check_no_aoe2_vocabulary_in_candidates`,
   `_check_no_tracker_sourced_candidates`,
   `_check_direction_name_consistency` (per **A9**),
   `_check_artifact_directories_absent` (filesystem absence per **A12**).
   Each helper has a one-paragraph Google-style docstring naming the
   binding invariant / ROADMAP halt clause.
7. Halting-falsifier priority chain in this order (halt at first failure;
   structural-membership > byte-stability > content):
   `input_parquet_missing` → `input_parquet_sha_mismatch` →
   `parent_audit_json_missing` → `identity_columns_misaligned` →
   `context_anchor_misaligned` → `upstream_features_misaligned` →
   `artifact_directory_present` (per **A12**) →
   `direction_annotation_invalid` (per **A9**) →
   `source_column_traceability_violation` (per **A10**) →
   `reconstructed_rating_in_candidates` →
   `slot_dependent_token_present` (per **A8**) →
   `target_leak_token_in_candidate` (boundary-aware per **A11**) →
   `aoe2_vocabulary_in_candidate` → `tracker_sourced_candidate` →
   `direction_name_inconsistent`.
8. Use `logging.getLogger(__name__)`; no `print`; 100% type-hinted
   signatures; Google-style docstrings on every public symbol.

**Verification:**

- `source .venv/bin/activate && poetry run python -c "from rts_predict.games.sc2.datasets.sc2egset.validate_symmetry_difference_feature_materialization import validate_symmetry_difference_feature_materialization, CandidateFeatureSpec; print('import OK')"`
  returns `import OK`.
- `source .venv/bin/activate && poetry run ruff check src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py`
  exits 0.
- `source .venv/bin/activate && poetry run mypy src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py`
  exits 0.
- No `open(..., "w")` or `Path.write_*` call in the module (grep confirms
  only read mode and `hashlib.sha256` byte-stream reads of input parquets).

**File scope:**

- `src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py`

**Read scope:**

- `src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py`
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_pre_game_feature_materialization.py`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.json`

---

### T02 — Mirror the test module

**Objective:** Create
`tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_symmetry_difference_feature_materialization.py`
covering each helper's pass and fail branches, with explicit
positive-control tests for the `_win_rate_*` substring false-positive risk
flagged by reviewer-adversarial N6. Target ≥ 16 tests; coverage ≥ 95% on
the validator module.

**Instructions:**

1. Resolve repo-relative paths via `Path(__file__).resolve().parents[6]`
   (predecessor pattern) — never hard-code absolute paths.
2. Define a `_valid_candidate_specs()` fixture returning a structurally
   valid `(designed_difference_specs, designed_symmetric_pair_specs,
   designed_race_pair_candidate_specs)` triple where every
   `CandidateFeatureSpec` carries an explicit `direction` and
   `source_columns` that traces to the audited tuples. Example:
   ```python
   CandidateFeatureSpec(
       column_name="focal_minus_opponent_prior_match_count_diff",
       direction="focal_minus_opponent",
       source_columns=("focal_prior_match_count", "opponent_prior_match_count"),
   )
   ```
3. Enumerate at minimum these test categories (each at least 1 pass + 1
   fail except where noted):
   - **Module imports + constants exist** (1 combined test verifying every
     listed module-level constant is non-empty).
   - **Input artifact path existence** (pass + fail with `tmp_path`-redirected
     bogus path).
   - **Input artifact byte-stability** (pass + fail with one-byte-mutated
     tmp copy).
   - **Identity / context / upstream-feature alignment** (pass + fail with
     mutated tmp-copied audit JSON).
   - **Direction annotation validity per A9 / N4** (pass + fail with
     `direction="invalid"`).
   - **Direction-name consistency per A9 / N4** (pass + fail when
     `column_name` contains `_diff` but `direction == "symmetric"`).
   - **Source-column traceability per A10 / N5** (pass + fail when
     `source_columns` references a column NOT in the audited 24-tuple or
     7-tuple).
   - **Slot-orthogonality regex sweep per A8 / N3** (parameterised over the
     BLOCKED_SLOT_TOKEN_REGEX set; each pattern variant must FAIL when
     present in a candidate name; clean `focal_minus_opponent_*` names must
     PASS).
   - **Reconstructed-rating exclusion** (fail when any candidate name
     contains a `BLOCKED_FAMILY_FRAGMENTS` element).
   - **Target-leakage boundary-aware regex per A11 / N6** (parameterised
     over `POST_GAME_TOKEN_REGEX`). MUST include a **positive control test
     case** verifying that `focal_prior_win_rate_decisive` and
     `matchup_h2h_focal_win_rate` do NOT fire the falsifier (the boundary
     check correctly distinguishes the legitimate `win_rate` substring
     from a true `win` leak token).
   - **AoE2 vocabulary exclusion** (fail when `civilization` or `civ`
     appears as a boundary-aware token).
   - **Tracker-source exclusion** (fail when any
     `source_columns` element starts with `TRACKER_SOURCE_PREFIX`).
   - **Artifact-free promise per A12 / N7** — `test_artifact_directories_absent_at_call_time`
     (pass when neither `reports/artifacts/02_02_01/` nor
     `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`
     exists; fail when either exists, even if empty).
   - **No mutation under validator** — `test_validator_writes_no_files`
     (run validator under `tmp_path`-cwd, assert `tmp_path` directory
     listing is empty after the call; assert
     `result.materialized_output_paths == ()`).
   - **Halting falsifier priority chain** —
     `test_halting_falsifier_priority_first_failure_wins` (construct a
     fixture violating two falsifiers simultaneously and assert the
     higher-priority one fires first).
4. Use `pytest.raises(AssertionError, match=...)` for negative cases;
   `pytest.mark.parametrize` for regex sweeps; mirror PR #241 predecessor
   test-file idiom.

**Verification:**

- `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_symmetry_difference_feature_materialization.py -v`
  — all tests pass (≥ 16 effective cases).
- `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_symmetry_difference_feature_materialization.py -v --cov=rts_predict.games.sc2.datasets.sc2egset.validate_symmetry_difference_feature_materialization --cov-report=term-missing`
  — coverage ≥ 95% on the new module.
- `source .venv/bin/activate && poetry run ruff check tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_symmetry_difference_feature_materialization.py`
  exits 0.
- `source .venv/bin/activate && poetry run mypy tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_symmetry_difference_feature_materialization.py`
  exits 0.

**File scope:**

- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_symmetry_difference_feature_materialization.py`

**Read scope:**

- `src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py`
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py`
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_pre_game_feature_materialization.py`

---

### T03 — Author the jupytext-paired notebook scaffold

**Objective:** Create the jupytext-paired `.py` / `.ipynb` notebook pair at
`sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.{py,ipynb}`
(per **A3** / **A4** — sandbox subdir `_and_`-form; notebook filename uses
`_materialization` suffix per overwrite-in-place contract). The notebook
declares the assumption/falsifier/sanity-check up front, consumes the two
upstream Parquet artifacts read-only via DuckDB SQL (NEVER
`pandas.read_parquet` on the full table — `sql-data.md` "Notebook Query
Pattern"), enumerates the candidate symmetric/difference feature families per
manual §3, invokes the T01 validator with explicit
`CandidateFeatureSpec`-typed candidate lists, prints a markdown report, and
emits NO Parquet / NO audit JSON / NO status YAML edit / NO `research_log`
append.

**Instructions:**

1. Create the sandbox subdirectory
   `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/`.
2. Create
   `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.py`
   with the jupytext `py:percent` header (copy verbatim from the predecessor
   `02_01_03_history_enriched_pre_game_feature_materialization.py`
   lines 1–15).
3. First markdown cell: step heading
   `# Step 02_02_01 — Symmetry & difference feature scaffold + one validation module: sc2egset`,
   identical structure to the predecessor's header. Cite: branch name,
   predecessors `PR #259 → PR #262 → PR #263 → PR #264`, non-batching
   sequence steps 2–4 of 9 ("notebook scaffold + one validation module →
   execute and report → user review"), the binding ROADMAP block at lines
   2853–3131, and the "scaffold-stage only — no artifact emission"
   promise. State explicitly that the notebook filename uses the
   `_materialization` suffix because the per-step notebook is OVERWRITTEN
   at materialisation per `sandbox/README.md` single-notebook-per-Step
   contract (not renamed).
4. Second markdown cell — "Hypothesis + falsifier + sanity-check
   declaration" — mirror the predecessor structure. State:
   - **Assumption being tested:** every candidate symmetric/difference
     feature family enumerated below traces to a focal/opponent paired
     column in the byte-stable `02_01_02` or `02_01_03` Parquet artifacts
     via a named transform (difference, absolute difference, symmetric
     mean/sum/product, matchup-pair operation), every candidate carries an
     explicit `direction` annotation, and slot-orthogonality holds at the
     design-contract layer.
   - **Measurement claim:** the validator returns `passed = True` with
     `halting_falsifier = None`; `materialized_output_paths == ()`;
     `artifact_directory_absence_ok == True`; the two input artifact
     SHA256 values match the embedded constants; the two parent audit
     JSONs are present at their canonical paths; every candidate's
     `direction` is in `VALID_DIRECTION_LITERAL_VALUES`; every candidate's
     `source_columns` trace to the audited tuples.
   - **Falsifiers:** the 14-step halting chain from T01 (input parquet
     missing / SHA mismatch / parent audit missing / identity misaligned /
     context misaligned / upstream misaligned / artifact directory present
     / direction annotation invalid / source-column traceability violation /
     reconstructed_rating in candidates / slot-dependent token present /
     target leak token in candidate / AoE2 vocabulary in candidate /
     tracker-sourced candidate / direction-name inconsistent).
   - **Sanity check:** module-load echoes of every constant;
     `validator.passed is True`; `len(designed_difference_specs) >= 1`;
     no path under `reports/artifacts/02_02_01/` or
     `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`
     exists at notebook entry AND at notebook exit (artifact-free promise
     per **A12**).
   - **Expected artifact:** NONE for this scaffold notebook. The expected
     user-facing output is a printed markdown report block summarising the
     validator result and the candidate-family enumeration.
   - **Lineage source:** PR #264 ROADMAP stub authorises this scaffold;
     PR #259 binding-five-family materialisation provides the upstream
     column space; PR #262 closes Step `02_01_03`.
   - **Downstream decision:** the future source-anchor / column-naming
     adjudication PR (analogous to PR #234) consumes this scaffold's
     candidate-family enumeration and binds the final transform set; the
     subsequent materialisation PR (analogous to PR #259) emits the
     Parquet + CROSS-02-01 audit pair.
5. Third markdown cell:
   `## Context — PR #264 ROADMAP stub binding-input snapshot` — itemise the
   BINDING inputs verbatim from ROADMAP `inputs.prior_artifacts`, including
   the SHA256 of each input Parquet (as embedded in T01's validator).
6. Fourth markdown cell:
   `## Candidate symmetry & difference feature families (manual §3)` —
   enumerate as a markdown table. Each row carries the `direction`
   annotation per **A9**:
   - **Family 1 — numeric difference (Bradley-Terry default;
     `direction="focal_minus_opponent"`).** For each numeric `focal_*` /
     `opponent_*` pair column in `02_01_03`'s 24-tuple, candidate name
     `focal_minus_opponent_<base>_diff = focal_<base> - opponent_<base>`.
     Cite manual §3 line 51 ("difference features … preferred for most
     models").
   - **Family 2 — absolute difference
     (`direction="symmetric"`).** For each numeric pair, candidate name
     `<base>_abs_diff = abs(focal_<base> - opponent_<base>)`. Useful where
     the ordered difference produces sign cancellation in tree models
     without monotone constraints.
   - **Family 3 — symmetric pair mean / sum / product
     (`direction="symmetric"`).** For each numeric pair, candidates
     `<base>_pair_mean`, `<base>_pair_sum`, `<base>_pair_product` —
     invariant under focal/opponent swap; capture matchup-aggregate
     intensity. Cite manual §3 line 57 (Hue & Vert 2010 symmetric kernels
     — tabular approximation).
   - **Family 4 — matchup-history pair operations
     (`direction="focal_minus_opponent"`).** For
     `*_prior_win_rate_matchup_conditional` and
     `*_prior_win_rate_race_conditional` and
     `*_prior_win_rate_map_conditional`, candidates
     `matchup_history_focal_minus_opponent_diff`,
     `race_history_focal_minus_opponent_diff`,
     `map_history_focal_minus_opponent_diff`.
   - **Family 5 — cross-region BOOLEAN-pair handling
     (`direction="symmetric"`).** For
     `is_cross_region_fragmented_focal_history_any` and
     `is_cross_region_fragmented_opponent_history_any`, candidates
     `cross_region_either` (XOR / OR) and `cross_region_both` (AND).
     NEVER a numeric subtraction (BOOLEAN-pair semantics).
   - **Family 6 — race-pair encoded interaction — CANDIDATE-ONLY, possible
     `02_05` deferral.** The `race_pair` categorical from `02_01_02` is
     already a 9-class (3 races × 3 races) categorical; cite ROADMAP method
     clause ("the binding decision whether race-pair interactions belong in
     `02_02` or in `02_05` (Categorical Encoding & Interactions, manual §6)
     is taken in the future source-anchor adjudication PR analogous to
     PR #234, NOT in this scaffold"). Mark the candidate name as
     `race_pair__defer_to_02_05` with `direction="symmetric"` so the
     validator's falsifier set cleanly accepts it as a placeholder.
7. Fifth cell (Python code): import the T01 validator and `CandidateFeatureSpec`;
   assign three local lists `DESIGNED_DIFFERENCE_SPECS`,
   `DESIGNED_SYMMETRIC_PAIR_SPECS`,
   `DESIGNED_RACE_PAIR_CANDIDATE_SPECS` populated from the Family 1–6
   enumeration above with explicit `direction` and `source_columns`
   per spec; pass them to the validator.
8. Sixth cell (Python code): invoke the validator with all six
   parameters; `print(result)`; assert `result.passed is True`,
   `result.halting_falsifier is None`,
   `result.materialized_output_paths == ()`,
   `result.artifact_directory_absence_ok is True`.
9. Seventh markdown cell:
   `## Closing — scaffold + one validation module persisted; no artifact emitted`
   — itemise what was done (validator + test + notebook scaffold) and what
   was NOT done (the full ROADMAP halt_predicate at lines 3063–3121: no
   Parquet, no audit JSON, no STEP_STATUS / PIPELINE_SECTION_STATUS /
   PHASE_STATUS edit, no ROADMAP body edit, no `research_log` append, no
   Phase 03, no Step `02_01_04`, no Step `02_02_02+`, no reopen of
   Q5 / Q6 / Q6F / Q6G / Q6H / `reconstructed_rating`, no AoE2
   `civilization` term).
10. Round-trip the notebook via
    `source .venv/bin/activate && poetry run jupytext --to ipynb sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.py`
    to generate the paired `.ipynb`. Then execute via
    `source .venv/bin/activate && poetry run jupyter nbconvert --to notebook --execute --inplace sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.ipynb`
    to ensure round-trip integrity.

**Verification:**

- The notebook executes end-to-end without error and the last cell's
  stdout shows `passed: True`, `halting_falsifier: None`,
  `materialized_output_paths: ()`, `artifact_directory_absence_ok: True`.
- `[ ! -d src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_02_01 ]`
  exits 0 (filesystem absence per **A12** / N7).
- `[ ! -d src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features ]`
  exits 0 (filesystem absence per **A12** / N7).
- `git status` shows no diff on `STEP_STATUS.yaml`,
  `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`, `ROADMAP.md`,
  `research_log.md` (any dataset or root path).
- `source .venv/bin/activate && poetry run ruff check sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.py`
  exits 0.

**File scope:**

- `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.py`
- `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.ipynb`

**Read scope:**

- `src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.json`
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py`
- `sandbox/jupytext.toml`
- `sandbox/README.md`

---

### T04 — Update planning index, CHANGELOG, and version

**Objective:** Mechanical bookkeeping: archive the prior planning entry,
register the active plan, bump the minor version, and add the CHANGELOG row
using the literal `### Notes` style per **A17** (reviewer-adversarial N2).
No code; documentation only.

**Instructions:**

1. Bump `pyproject.toml` `version = "3.83.0"` → `version = "3.84.0"`
   (minor; per **A6**).
2. Update `planning/INDEX.md`:
   - Move the current "Active plan" line for
     `feat/sc2egset-02-02-01-roadmap-stub` to the Archive table with
     PR #264 merge SHA `7f2506ed`.
   - Add a new Archive row for this Layer-1 planning PR with its merge SHA
     (filled at Layer-2 dispatch time).
   - Set new Active plan line to
     `feat/sc2egset-02-02-01-symmetry-difference-scaffold (2026-05-29) —
     Category A: Layer-2 scaffold + one validation module execution PR for
     SC2EGSet Step 02_02_01 opening Pipeline Section 02_02 — Symmetry &
     Difference Features. Creates
     validate_symmetry_difference_feature_materialization.py + mirrored
     test + sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.{py,ipynb}
     notebook pair. NO Parquet, NO audit JSON, NO status YAML edit, NO
     ROADMAP edit, NO research_log append. SHA pins: 02_01_02 Parquet
     24db73fb…; 02_01_03 Parquet 053900e7…. 7-file tracked diff (validator
     + test + notebook .py + notebook .ipynb + pyproject + INDEX +
     CHANGELOG).`
3. Update `CHANGELOG.md` with a new
   `## [3.84.0] — 2026-05-29 (PR #<TBD>: feat/sc2egset-02-02-01-symmetry-difference-scaffold)`
   section under `[Unreleased]`, above `[3.83.0]`. Required subsections:
   - `### Added` — bullet listing the scaffold-stage validator module +
     test + jupytext notebook scaffold pair for Step `02_02_01`, with the
     concrete file paths.
   - `### Notes` (literal heading; per **A17** / N2) — bolded `**No X**` /
     `**No Y**` bullets mirroring PR #264's `## [3.83.0]` `### Notes`
     style. At minimum:
     - `**No feature value materialised.**` (no Parquet / CSV / MD / JSON
       under any `02_02_01` artifact path);
     - `**No source-anchor adjudication.**` (candidate enumeration is
       CANDIDATE-only; binding decision deferred to future PR analogous
       to PR #234);
     - `**No STEP_STATUS row added for 02_02_01.**` (closure deferred to
       future U2.B-style PR analogous to PR #237 / PR #262);
     - `**No PIPELINE_SECTION_STATUS row added for 02_02.**` (per PR #230
       precedent — section row lands at step closure, not scaffold);
     - `**No PHASE_STATUS mutation.**` (Phase 02 stays `in_progress`;
       Phase 03 stays `not_started`);
     - `**No ROADMAP edit.**` (block at lines 2853–3131 byte-unchanged);
     - `**No research_log append.**` (per data-analysis-lineage non-batching
       sequence — research_log appended only at step closure, sequence
       step 8);
     - `**No upstream artifact mutation.**` (both `02_01_02` and `02_01_03`
       Parquets byte-stable at named SHA256; both `02_01_x` audit JSONs
       byte-unchanged);
     - `**No reconstructed_rating re-introduction.**` (PR #255 / PR #257
       binding exclusion stands);
     - `**No AoE2 civilization vocabulary.**` (SC2EGSet uses `race` per
       Invariant I8 cross-game hygiene);
     - `**No Phase 03 / Step 02_01_04 / Step 02_02_02+ / baseline modeling.**`

**Verification:**

- `git diff pyproject.toml` shows exactly one line change:
  `version = "3.83.0"` → `version = "3.84.0"`.
- `git diff CHANGELOG.md` shows exactly one new `## [3.84.0]` section
  appended above `## [3.83.0]`, with a literal `### Notes` subsection per
  **A17**.
- `git diff planning/INDEX.md` shows one row removed from "Active plan", one
  row added to the Archive list (with merge SHA `7f2506ed` for PR #264 and
  the future merge SHA for this Layer-1 PR), one new "Active plan" row.
- `git status` shows ONLY the 7 manifest files (T01 validator, T02 test,
  T03 notebook `.py`, T03 notebook `.ipynb`, `pyproject.toml`,
  `planning/INDEX.md`, `CHANGELOG.md`) plus the new sandbox subdirectory
  itself (untracked at first; tracked when the notebook pair is `git add`-ed
  inside it). No other file modified.

**File scope:**

- `pyproject.toml`
- `planning/INDEX.md`
- `CHANGELOG.md`

**Read scope:**

- `CHANGELOG.md` (for the current `## [3.83.0]` row's `### Notes` style
  precedent — **A17**)
- `planning/INDEX.md` (for active-plan-line and archive-row style precedent)

For each Layer-2 step, the executor must:

- grep-discover anchor strings before each edit;
- run pre-commit hooks once before commit; ruff / mypy run automatically
  on `.py` touch;
- verify the 7-file diff at commit time; reject any 8th tracked entity.

## File Manifest

### THIS Layer-1 planning PR (exactly 2 files; ONLY after reviewer approval):

| Path | Action |
|---|---|
| `planning/current_plan.md` | create/overwrite |
| `planning/current_plan.critique.md` | create/overwrite |

### Future Layer-2 execution PR (exactly 7 files):

| Path | Action | Notes |
|---|---|---|
| `src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py` | Create | T01 — name carries `_materialization` family suffix per PR #233 / PR #241 precedent (**A2**) |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_symmetry_difference_feature_materialization.py` | Create | T02 — ≥ 16 tests; coverage ≥ 95% |
| `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.py` | Create | T03 — jupytext source; `_and_` subdir per **A3**; `_materialization` suffix per **A4** |
| `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.ipynb` | Create | T03 — paired notebook |
| `pyproject.toml` | Update | T04 — version 3.83.0 → 3.84.0 (**A6**) |
| `planning/INDEX.md` | Update | T04 — archive prior + add new Active line |
| `CHANGELOG.md` | Update | T04 — `## [3.84.0]` block with literal `### Notes` per **A17** |

### Forbidden in future Layer-2 (must NOT appear in diff):

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
  (no `02_02_01` row; closure deferred to future U2.B-style PR);
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
  (no `02_02` row; deferred per PR #230 precedent — **A16**);
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`
  (Phase 02 stays `in_progress`);
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
  (`02_02_01` block at lines 2853–3131 byte-unchanged);
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
  (per data-analysis-lineage non-batching sequence step 2 vs step 8);
- `reports/research_log.md` (root);
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md`;
- any artifact under `reports/artifacts/02_02_01/` or
  `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`
  (filesystem absence per **A12** / N7);
- any byte change to
  `reports/artifacts/02_01_02/leakage_audit_sc2egset.{json,md}`,
  `reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}`,
  `02_01_02_pre_game_features.parquet`, or
  `02_01_03_history_enriched_pre_game_features.parquet`;
- any source `.py` other than the T01 validator;
- any test `.py` other than the T02 test file;
- any notebook `.py` / `.ipynb` other than the T03 pair;
- any spec under `reports/specs/` or schema YAML under
  `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/`;
- any AoE2 path under `src/rts_predict/games/aoe2/**`;
- any thesis chapter, bib, appendix under `thesis/**`;
- any `docs/**`, `.claude/**`, or `data/**` path.

## Gate Condition

**Layer-1 gate (THIS PR):** satisfied iff ALL of:

1. PR diff = exactly two files
   (`planning/current_plan.md` + `planning/current_plan.critique.md`).
2. PR is open as draft.
3. `planning/current_plan.md` contains all eight required `##` sections
   (Scope, Problem Statement, Literature Context, Assumptions & Unknowns,
   Execution Steps, File Manifest, Gate Condition, Open Questions).
4. Reviewer-adversarial returns APPROVE or APPROVE-WITH-NITS with zero
   blockers; verdict recorded in `current_plan.critique.md`.

**Layer-2 gate (FUTURE execution PR):** satisfied iff ALL of:

1. **Validator runs as a script and prints PASS** — with the canonical
   candidate-specs fixture from T02, the validator returns `passed=True`,
   `halting_falsifier=None`, `materialized_output_paths=()`,
   `artifact_directory_absence_ok=True`.
2. **All ≥ 16 tests pass** —
   `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_symmetry_difference_feature_materialization.py -v`
   exits 0.
3. **Coverage ≥ 95% on the new validator** — coverage report on the new
   module shows ≥ 95% line coverage.
4. **Notebook executes end-to-end** — paired `.ipynb` round-trips via
   jupytext + executes via nbconvert; final cell's stdout shows
   `passed: True`, `halting_falsifier: None`,
   `materialized_output_paths: ()`, `artifact_directory_absence_ok: True`.
5. **Lint / type / pre-commit clean** —
   `ruff check src/ tests/ sandbox/` exits 0;
   `mypy src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_symmetry_difference_feature_materialization.py`
   exits 0; the pre-commit hook stack passes on every committed file.
6. **Diff is exactly the 7-file manifest** —
   `git diff --name-only origin/master..HEAD | sort` returns exactly the
   7 files listed in the File Manifest table (no scope-creep; no 8th
   tracked entity such as `.gitkeep`).
7. **Artifact-free promise upheld (filesystem absence per A12 / N7)** —
   `[ ! -d src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_02_01 ]`
   exits 0; `[ ! -d src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features ]`
   exits 0.
8. **Status / ROADMAP / research_log byte-unchanged** —
   `git diff origin/master..HEAD -- src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md reports/research_log.md`
   returns empty.
9. **Version bumped to 3.84.0** —
   `grep '^version = ' pyproject.toml` returns `version = "3.84.0"`.
10. **CHANGELOG `## [3.84.0]` entry with `### Notes` subsection** —
    `grep -c '^## \[3.84.0\]' CHANGELOG.md` returns `1`; and
    `grep -A 100 '^## \[3.84.0\]' CHANGELOG.md | grep -c '^### Notes$'`
    returns `1` (literal `### Notes` heading per **A17** / N2).
11. **Direction annotation + traceability enforced structurally** —
    the validator constants `VALID_DIRECTION_LITERAL_VALUES`,
    `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02`,
    `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03` exist, are non-empty, and
    are exercised by tests per **A9** / **A10** / N4 / N5.
12. **Boundary-aware POST_GAME_TOKEN_REGEX in use** — grep
    `(?:\\^|_)` (boundary-aware regex pattern) appears in the validator
    module per **A11** / N6; positive-control test for
    `focal_prior_win_rate_decisive` passes (does NOT fire the falsifier).
13. **Slot-orthogonality regex enforcement** — grep
    `BLOCKED_SLOT_TOKEN_REGEX` (or equivalent positive-whitelist enforcement)
    appears in the validator module per **A8** / N3.

## Open Questions

- **OQ1 — Outcome adjudication.** A (scaffold + one validator) chosen.
  B–G rejected on repo evidence (see `current_plan.critique.md`
  §"Adjudication outcomes").
- **OQ2 — Validator family-name suffix
  (`_materialization` vs `_scaffold`).** `_materialization` chosen per
  PR #233 / PR #241 precedent. The validator filename carries the
  family suffix from scaffold onward and never renames; the stage marker
  lives in the docstring. **A2**.
- **OQ3 — Notebook filename suffix
  (`_materialization` vs `_scaffold`).** `_materialization` chosen per
  `sandbox/README.md` single-notebook-per-Step contract + PR #259
  precedent (PR #241 scaffold notebook was already named
  `..._materialization.{py,ipynb}` and was overwritten in place at
  materialisation). Reviewer-adversarial N8. **A4**.
- **OQ4 — Sandbox subdirectory (`_and_`-form vs `_`-form).**
  `02_symmetry_and_difference_features/` chosen per ROADMAP lines 2932
  and 3100 verbatim. **A3**.
- **OQ5 — Branch name idiom.**
  `feat/sc2egset-02-02-01-symmetry-difference-scaffold` chosen per
  PR #241 idiom (`feat/sc2egset-02-01-03-history-scaffold`: step →
  family-token → `-scaffold`). Reviewer-adversarial N1. **A5**.
- **OQ6 — Version bump (minor vs patch).** Minor 3.83.0 → 3.84.0
  chosen per `feat/`-class scaffold precedent ladder (PR #232 / #233 /
  #239 / #241). Patch would be a policy break against three precedents.
  **A6**.
- **OQ7 — PIPELINE_SECTION_STATUS `02_02` row timing.** Deferred to
  future PR per PR #230 precedent. **A16**.
- **OQ8 — Race-pair candidate scope (02_02 vs 02_05).** Race-pair encoded
  interactions enumerated as CANDIDATE-only with explicit "may defer to
  02_05" annotation. Binding `02_02`-vs-`02_05` boundary decision taken in
  the future source-anchor adjudication PR analogous to PR #234.
  Reviewer-adversarial open methodology question O2.
- **OQ9 — Cross-region BOOLEAN-pair scope (02_02 vs 02_03).** Cross-region
  BOOLEAN-pair handling enumerated as Family 5 CANDIDATE in the T03
  notebook. The binding decision (does this belong in `02_02` or in
  `02_03+`?) is taken in the future source-anchor adjudication PR.
  Reviewer-adversarial open methodology question O1.
- **OQ10 — Symmetric pair mean/sum/product family scope (tabular vs GNN).**
  Family 3 (symmetric pair mean/sum/product) enumerated as CANDIDATE for
  tabular Phase 04 consideration. The binding decision (is this tabular
  scope or GNN-comparison scope?) is taken in the future source-anchor
  adjudication PR. Reviewer-adversarial open methodology question O3.
- **OQ11 — Ratio features excluded from CANDIDATE list.** Per the
  Literature Context [OPINION] paragraph, ratio features are not
  enumerated as CANDIDATE because most history columns have zero-bounded
  denominators (cold-start undefined values). If the future adjudication
  PR judges this too conservative, ratios can be added without validator
  change (the candidate-spec tuple is opaque to the validator's content
  beyond direction + source_columns checks).
- **OQ12 — Test count exact target.** 16 tests targeted as a tight lower
  bound; predecessor `test_validate_history_enriched_pre_game_materialization.py`
  (PR #241) has ~20 tests. If T02 parameterisation grows the effective
  count to 20–24, that is acceptable. Resolved at reviewer-deep at
  execution time.

---

## Reviewer-adversarial nits applied (Layer-1 materialisation)

The 8 non-blocking nits from `current_plan.critique.md` are integrated
into this plan body as follows:

- **N1 (branch name idiom):** branch field in frontmatter is
  `feat/sc2egset-02-02-01-symmetry-difference-scaffold`; **A5** records
  the PR #241 precedent justification.
- **N2 (CHANGELOG `### Notes` style):** T04 instructions require literal
  `### Notes` heading with bolded `**No X**` bullets mirroring PR #264's
  `## [3.83.0]` block; **A17** records the precedent justification.
- **N3 (slot-orthogonality regex/token enforcement):** T01 declares
  `BLOCKED_SLOT_TOKEN_REGEX` covering player_?\d+, slot_?\d+, p\d+,
  idx_?\d+, home/away, left/right, host/guest, a_minus_b/b_minus_a — OR
  positive-whitelist enforcement requiring `focal` + `opponent` tokens;
  **A8** records the assumption; gate condition 13 verifies.
- **N4 (direction annotation Literal):** T01 declares
  `VALID_DIRECTION_LITERAL_VALUES`; `CandidateFeatureSpec` requires
  `direction: Literal["focal_minus_opponent", "symmetric"]`; T02 includes
  pass + fail tests for invalid direction and direction-name
  inconsistency; **A9** records the assumption; gate condition 11 verifies.
- **N5 (audited-tuple traceability):** T01 declares
  `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02` (7-tuple) and
  `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03` (24-tuple);
  `CandidateFeatureSpec.source_columns` MUST trace to those tuples; T02
  includes pass + fail tests for traceability violations; **A10** records
  the assumption; gate condition 11 verifies.
- **N6 (POST_GAME_TOKENS boundary-aware):** T01 declares
  `POST_GAME_TOKEN_REGEX` derived from `POST_GAME_TOKENS` with
  `(?:^|_)<token>(?:_|$)` pattern; T02 includes positive-control tests for
  `focal_prior_win_rate_decisive` and `matchup_h2h_focal_win_rate` that
  must NOT fire; **A11** records the assumption; gate condition 12
  verifies.
- **N7 (artifact-free = filesystem absence):** T01 declares
  `EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES`; the
  `_check_artifact_directories_absent` helper asserts directory absence
  (not emptiness); T02 includes pass + fail tests; T03 sanity-check and
  closing markdown cells assert absence; **A12** records the assumption;
  gate condition 7 verifies.
- **N8 (notebook `_materialization` suffix):** T03 file paths in the
  manifest and instructions use
  `02_02_01_symmetry_difference_feature_materialization.{py,ipynb}`;
  **A4** records the `sandbox/README.md` single-notebook-per-Step
  contract justification.
