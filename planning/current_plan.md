---
title: "SC2EGSet Step 02_02_01 ROADMAP-only stub (Layer-1 planning PR)"
category: A
branch: feat/sc2egset-02-02-01-roadmap-stub
base_ref: master
base_sha: 2c9080ae0d02e8733f60b974ef9f0c0ced36c849
predecessor_pr: 262
predecessor_pr_merge_sha: 2c9080ae0d02e8733f60b974ef9f0c0ced36c849
draft_pr_files:
  - planning/current_plan.md
  - planning/current_plan.critique.md
future_execution_files:
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
  - planning/INDEX.md
  - CHANGELOG.md
  - pyproject.toml
future_execution_file_count: 4
target_version_bump: "3.82.1 -> 3.83.0"
date: "2026-05-29"
---

## Scope

Author a Category A Layer-1 planning artifact for SC2EGSet Pipeline Section
`02_02 — Symmetry & Difference Features`. PR #262 (merged 2026-05-29 at master
`2c9080ae`) formally closed Step `02_01_03`; `02_01` is now complete in both
STEP_STATUS (`02_01_03: complete`, `completed_at: "2026-05-28"`, L205-L209) and
PIPELINE_SECTION_STATUS (`02_01: complete`, L51-L54). The next atomic unit per
`docs/PHASES.md` Phase 02 table is `02_02`, whose first step we open with a
ROADMAP-only stub.

**Two-PR sequence.**

1. **THIS Layer-1 planning PR** writes only two files:
   - `planning/current_plan.md` (this document);
   - `planning/current_plan.critique.md` (reviewer-adversarial output).
2. **FUTURE Layer-2 execution PR on the same branch** performs four file edits:
   - `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (add one
     `### Step 02_02_01 — ...` block between the existing `### Step 02_01_99`
     block and the `## Phase 03 — Splitting & Baselines (placeholder)` heading);
   - `planning/INDEX.md` (archive PR #262 row + this PR row + new active line);
   - `CHANGELOG.md` (append `## [3.83.0]` block under `[Unreleased]`);
   - `pyproject.toml` (bump `version = "3.82.1"` -> `version = "3.83.0"`).

**Explicitly out of scope** for both PRs:
- feature value materialization (no Parquet, no CSV, no MD report under
  `reports/artifacts/02_02_01/` or `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`);
- notebook scaffold; one-validation-module pass; full validator suite;
- STEP_STATUS.yaml additions for `02_02_01` (closure comes after future
  materialization PRs per the `02_01` ladder);
- PIPELINE_SECTION_STATUS.yaml `02_02` row addition (defer until first `02_02`
  step transitions — see OQ3 / Outcome-E justification below);
- PHASE_STATUS.yaml mutation (Phase 02 stays `in_progress`);
- ROADMAP changes to any other Step or Pipeline Section (no edits to
  Steps `02_01_01`, `02_01_02`, `02_01_03`, `02_01_99`, or the §02_01_03
  amendment back-references);
- root `reports/research_log.md` edit;
- per-dataset `research_log.md` edit (`.claude/rules/data-analysis-lineage.md`
  non-batching rule sequence step 1 — ROADMAP stub PR produces no
  research_log entry; see PR #239 / PR #253 precedent);
- thesis chapters, bib, appendix, `docs/**`, `.claude/**`, `data/**`;
- any AoE2 path under `src/rts_predict/games/aoe2/**`;
- Step `02_02_02+`; Step `02_01_04`; Phase 03; any baseline modeling.

## Problem Statement

Three repo-evidence facts force opening `02_02`:

1. **Phase 02 work continues.** `docs/PHASES.md` Phase 02 lists eight pipeline
   sections (`02_01` through `02_08`). After PR #262 closure, `02_01` is the
   only one materialized in either STEP_STATUS / PIPELINE_SECTION_STATUS.
   PHASE_STATUS Phase 02 = `in_progress`; Phase 03 = `not_started`. The next
   sectional unit by `docs/PHASES.md` ordering is `02_02 — Symmetry &
   Difference Features`.

2. **Methodological motivation.** SC2EGSet two-player matchups (1v1 random map)
   produce feature rows with arbitrary slot ordering. The
   `02_FEATURE_ENGINEERING_MANUAL.md` §3 ("Symmetry in Pairwise Prediction
   Demands Difference Features") declares that a model treating
   `[player1_features, player2_features]` as a standard concatenation will
   learn different weights for each slot, violating the fundamental requirement
   that `P(A wins vs B) = 1 - P(B wins vs A)`. Invariant I5
   (`scientific-invariants.md` L156-L170) makes this binding for this thesis:
   "Both players in every game must be treated identically by the feature
   pipeline ... The model input is always structured as
   `(focal_player_features, opponent_features, context_features)` and this
   structure is identical regardless of which player is focal." The
   `02_01_03_history_enriched_pre_game_features.parquet` artifact already
   implements focal/opponent symmetric column generation; `02_02` operationalises
   the next step — symmetric/difference representations layered on top of
   focal/opponent pair columns.

3. **Non-batching discipline.** `.claude/rules/data-analysis-lineage.md`
   "Non-batching rule for empirical work" sequence step 1 ("ROADMAP stub
   only") and "Feature-engineering discipline" ("Feature-engineering contracts
   and protocols may define planned feature families, grains, prediction
   settings, and leakage checks. They must not silently execute feature
   generation.") mandate that opening `02_02` start with a ROADMAP-only stub
   that declares the planned families and gates — no scaffold, no validator,
   no artifact. The precedent ladder is verified at PR #232 (Step 02_01_02
   stub), PR #239 (Step 02_01_03 stub), and PR #253 (Step 02_01_99 stub) —
   each was ROADMAP-only with no PIPELINE_SECTION_STATUS row addition.

## Assumptions & Unknowns

- **A1 (Outcome A justified).** Outcomes B-F rejected on repo evidence (see
  reviewer-adversarial §1 in `current_plan.critique.md`). A is the only
  sequence-step-1-compliant outcome.
- **A2 (Position after 02_01_99 stub).** Insert the new
  `### Step 02_02_01 — ...` block immediately after `### Step 02_01_99` (and
  its amendment back-reference at L2837-L2849), before
  `## Phase 03 — Splitting & Baselines (placeholder)` at L2853. Justification:
  sectional ascending order; 02_01_99 is the existing terminal 02_01 block;
  02_02_01 opens the next pipeline section.
- **A3 (Predecessor token `"02_01_03"`).** Single-string scalar matching the
  ROADMAP idiom (L2360, L2691). Inputs for any future 02_02 materialization
  are the `02_01_03` Parquet + audit pair; those are 02_01_03 outputs.
  02_01_99 is a sibling decision-lineage stub, not a feature input.
- **A4 (minor version bump `3.82.1 -> 3.83.0`).** Per
  `.claude/rules/git-workflow.md` ("minor for feat/refactor/docs, patch for
  fix/test/chore"). This is a `feat/` branch opening a new pipeline section —
  pattern-matches PR #232 (`3.66.0 -> 3.67.0`, Step 02_01_02 stub), PR #239
  (`3.70.1 -> 3.71.0`, Step 02_01_03 stub), PR #253 (`3.78.0 -> 3.79.0`,
  Step 02_01_99 stub). All three precedents bumped minor for a ROADMAP-only
  stub. The version bump itself lands in the **Layer-2 execution PR**, not in
  this Layer-1 planning PR.
- **A5 (upstream evidence is byte-stable).**
  `02_01_03_history_enriched_pre_game_features.parquet` (2,451,869 B),
  `02_01_02_pre_game_features.parquet` (719,068 B), and
  `reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}`
  (13,054 / 20,694 B) on master `2c9080ae`. The future Layer-2 stub does not
  consume their values, only declares them as planned upstream inputs.
- **A6 (Focal/opponent column convention already proven on disk).** PR #259
  materialized the 02_01_03 Parquet covering five families with `focal_*` and
  `opponent_*` symmetric pairs. The future 02_02 work declares planned
  pair-difference / pair-product / symmetric-encoder operations on top of
  those columns; column identity carries over. Specific row/column counts
  are properties of the 02_01_03 artifact and are re-measured by Layer-2 at
  execution time rather than hard-coded as Layer-1 gates.
- **A7 (Slot bias avoidance).** Difference features must be computed as
  `focal_value - opponent_value`, never `player_1_value - player_2_value`.
  Player slot assignment in SC2EGSet is data-dependent (RISK-24 falsifier
  enumerated in PR #259 notebook); encoding `player_1 - player_2` would
  invent slot-skill correlation.
- **A8 (Cross-region indicator handling carries lineage).** Any 02_02 family
  that consumes `cross_region_fragmentation_handling` columns from the
  02_01_03 Parquet must respect PR #243 Q5 cross-region adjudication and
  PR #255 omit-closure scope (sensitivity-indicator co-registration arm
  selected — preserved verbatim in PR #259 materialization). The 02_02 work
  inherits this co-registration unchanged; it does not re-process the
  cross-region indicator as a difference-feature input.
- **A9 (`reconstructed_rating` family stays excluded).** PR #255 omit-closure
  + PR #257 amendment + PR #259 materialization unanimously excluded the
  `reconstructed_rating` family; 02_02 must not silently re-include
  `reconstructed_rating_focal_pre`, `reconstructed_rating_opp_pre`, or
  `reconstructed_rating_diff` under a difference-feature pretence.
- **A10 (PIPELINE_SECTION_STATUS row deferred).** The `02_02` row addition
  is deferred to a future PR (not this Layer-2 ROADMAP stub) per the verified
  `02_01` precedent: section row first landed in PR #230 (closure of the
  section's first step), not in the section's stub PR. See OQ3.
- **A11 (Branch retained on Layer-2 same as Layer-1).** Both PRs ride
  `feat/sc2egset-02-02-01-roadmap-stub`; mirrors PR #238 -> #239 ladder
  (same branch hosting plan PR then stub PR).
- **A12 (CHANGELOG PR-number placeholder).** Layer-2 CHANGELOG header uses
  `PR #<TBD>`, swept to the real number by a follow-up housekeeping commit
  pre-merge (mirrors `c4a3861b` "normalize PR #<TBD> placeholders to PR #262"
  and `f0a3f551` for PR #260).
- **A13 (02_02 vs 02_05 scope boundary).** Race-pair encoded interactions are
  the canonical `02_05` (Categorical Encoding & Interactions) example per
  manual §6. The future 02_02 ROADMAP block lists race-pair interactions as a
  **candidate** family with explicit "may defer to 02_05" annotation; the
  decision is taken in the Layer-2 source-anchor adjudication PR analogous to
  PR #234, not in this stub.

## Literature Context

Two anchors from the methodology manuals:

`02_FEATURE_ENGINEERING_MANUAL.md` §3 ("Symmetry in Pairwise Prediction
Demands Difference Features") establishes the Bradley-Terry connection:
each player `i` has latent strength `beta_i`, and the logit of win
probability equals the difference of latent strengths. For tabular logistic
regression or gradient boosting, "difference features are the clear default"
because they are antisymmetric under slot swap and reduce dimensionality by
half while preserving information. The manual identifies four representations
(difference, ratio, canonical ordering with concatenation, symmetric
kernels) and recommends differences for thesis-grade tabular work. Section
6 of the same manual catalogues categorical-pair interaction encoding
(`race x opponent_race`) as the standard pre-game pair feature — and this
interaction-encoding scope belongs to Pipeline Section `02_05`, not `02_02`;
the 02_02 stub annotates race-pair candidates accordingly.

`.claude/scientific-invariants.md` Invariant I5 (L156-L170) binds this
thesis: "Both players in every game must be treated identically by the
feature pipeline ... The model input is always structured as
`(focal_player_features, opponent_features, context_features)` and this
structure is identical regardless of which player is focal." Invariant I3
(L130-L148) binds the temporal cutoff that any symmetric/difference feature
inherits: `history_time < target_time` strict, normalization scoped to
training folds. `.claude/ml-protocol.md` enumerates the three leakage
failure modes that 02_02 design must not break (rolling aggregates that
include game T, head-to-head that includes game T, co-occurring matches).
`reports/specs/02_03_temporal_feature_audit_protocol.md` is the downstream
temporal-window/decay/cold-start audit spec that 02_02 difference features
will eventually feed into; it is read at Layer-1 so the stub's exclusion
clauses do not silently encroach on `02_03` scope.

## Execution Steps

**Layer-1 (THIS PR — planning-only):**

L1.1 Read `.claude/scientific-invariants.md`, `.claude/ml-protocol.md`,
`.claude/rules/data-analysis-lineage.md`, `.claude/rules/git-workflow.md`,
`docs/PHASES.md`, `docs/TAXONOMY.md`,
`docs/ml_experiment_lifecycle/02_FEATURE_ENGINEERING_MANUAL.md`,
`reports/specs/02_00_feature_input_contract.md`,
`reports/specs/02_01_leakage_audit_protocol.md`,
`reports/specs/02_02_feature_engineering_plan.md`,
`reports/specs/02_03_temporal_feature_audit_protocol.md` (added per
reviewer-adversarial nit N4), the dataset's PHASE_STATUS /
PIPELINE_SECTION_STATUS / STEP_STATUS / ROADMAP / research_log, the master
HEAD diff for PR #262, the `02_01_03` audit and Parquet metadata (no value
reads). All read-only.

L1.2 Confirm verified state matches the lookup-PASS section of the
predecessor prompt: master HEAD `2c9080ae`, pyproject `3.82.1`,
STEP_STATUS 02_01_03 complete `completed_at` 2026-05-28, no 02_01_99 or
02_02_01 STEP_STATUS row, ROADMAP §02_01_99 still present (L2622-L2849),
audit artifacts byte-stable.

L1.3 Author `planning/current_plan.md` (this document). Pre-commit hook
sanity (`feedback_plan_required_sections.md`): the document MUST have
`## Scope`, `## Problem Statement`, `## Assumptions & Unknowns`,
`## Literature Context`, `## Execution Steps`, `## File Manifest`,
`## Gate Condition`, `## Open Questions`. Verified inline.

L1.4 Author `planning/current_plan.critique.md` (reviewer-adversarial
verdict + the 6 strong endorsements and 4 nits applied during Layer-1
materialization).

L1.5 Open draft PR with exactly those two files. Branch
`feat/sc2egset-02-02-01-roadmap-stub` off master `2c9080ae`. PR body in
`.github/tmp/pr.txt` per `feedback_pr_body_file.md`; delete after PR
opens (`feedback_pr_body_cleanup.md`).

**Layer-2 (FUTURE execution PR — same branch — DO NOT execute now):**

L2.1 Insert exactly ONE new `### Step 02_02_01 — Symmetry & difference
feature-family ROADMAP-only stub (sc2egset)` block in
`src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` between
the existing `### Step 02_01_99` block (which ends at L2835 closing
backtick fence + L2837-L2849 amendment back-reference + L2851 `---`) and
the `## Phase 03 — Splitting & Baselines (placeholder)` heading at L2853.
The new block MUST contain the 12 required content items enumerated in
the "Required content for the future ROADMAP `02_02_01` block" section
of this plan (one fenced yaml block matching the schema used at L2624 for
Step 02_01_99 and L2276 for Step 02_01_03). Forbidden actions: edit any
other Step block, edit the amendment back-reference, change section
ordering, add a `## Pipeline Section 02_02` heading (the ROADMAP keeps
step blocks at H3 directly under the `## Phase 02` heading; verify
against L2099 and L2274 — no intermediate section heading exists at H3
or H4 in the current file).

L2.2 (CONDITIONAL — does NOT fire under Outcome-E adjudication.) NO
`02_02` row addition to `PIPELINE_SECTION_STATUS.yaml` in this Layer-2
PR. Justification: PIPELINE_SECTION_STATUS 02_01 first landed in PR #230
(closure of 02_01_01), not in PR #232 (stub). The verified pattern is
section-row-on-first-transition, not section-row-on-stub. The future
02_02 section row will land when the future first 02_02 materialization
step closes (analogous to PR #230 for 02_01).

L2.3 Update `planning/INDEX.md`:
   - Move current Active plan line (PR #262 row) into the Archive table
     above the existing PR #260 chore row.
   - Add a new Archive row for THIS Layer-1 planning PR with its merge
     SHA (filled at Layer-2 dispatch time).
   - Set new Active plan line to
     `feat/sc2egset-02-02-01-roadmap-stub (YYYY-MM-DD) — Category A:
     Layer-2 ROADMAP-only execution PR for SC2EGSet Step 02_02_01 stub
     ...`. Mirror PR #239's archive row format.

L2.4 Bump `pyproject.toml` line 3: `version = "3.82.1"` ->
`version = "3.83.0"`. Single edit.

L2.5 Append `## [3.83.0]` block to `CHANGELOG.md` immediately under the
`[Unreleased]` block (above the `[3.82.1]` block at L22). Header:
`## [3.83.0] — YYYY-MM-DD (PR #<TBD>: feat/sc2egset-02-02-01-roadmap-stub)`.
Required subsections: `### Added` (with bullet listing the 02_02_01
ROADMAP stub and the new pipeline section opened), `### Changed` (empty
or omitted), `### Notes` (with the explicit no-feature, no-status-flip,
no-research-log, no-PIPELINE_SECTION_STATUS-02_02-row sentences, and
the `02_01_03` upstream Parquet + audit byte-unchanged statements,
mirroring PR #262 CHANGELOG L33-L40 format).

L2.6 NO other file touched. NO STEP_STATUS.yaml row for `02_02_01`. NO
PIPELINE_SECTION_STATUS row for `02_02`. NO PHASE_STATUS mutation. NO
research_log.md (dataset OR root) entry. NO source `.py`, test `.py`,
notebook `.py`/`.ipynb`, artifact (Parquet/CSV/MD/JSON), spec under
`reports/specs/`, cleaning-layer YAML, AoE2 path, thesis chapter, bib,
docs, `.claude`, data path.

For each Layer-2 step, the executor must:
- diff-cap the new ROADMAP block to a single fenced yaml block following
  the schema at L2276 (02_01_03) and L2624 (02_01_99);
- grep-discover the anchor strings before each edit (`### Step 02_01_99`,
  `## Phase 03 — Splitting & Baselines (placeholder)`, `[Unreleased]`,
  `[3.82.1]`, `version = "3.82.1"`, the planning/INDEX.md Active plan
  line);
- run pre-commit hooks once before commit; ruff / mypy run automatically
  on `.py` touch and will not fire on this PR's no-`.py` diff.

## File Manifest

### THIS Layer-1 planning PR (exactly 2 files; ONLY after reviewer approval):

| Path | Action |
|---|---|
| `planning/current_plan.md` | create/overwrite |
| `planning/current_plan.critique.md` | create/overwrite |

### Future Layer-2 execution PR (exactly 4 files):

| Path | Action | Notes |
|---|---|---|
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | add ONE `### Step 02_02_01` block | Between L2851 `---` (after 02_01_99 amendment back-reference) and L2853 `## Phase 03 — Splitting & Baselines (placeholder)` |
| `planning/INDEX.md` | archive PR #262 + this Layer-1 PR; new Active line | Mirror PR #239 archive row format |
| `CHANGELOG.md` | append `## [3.83.0]` block | Under `[Unreleased]`, above `[3.82.1]` |
| `pyproject.toml` | bump version | `version = "3.82.1"` -> `version = "3.83.0"` |

### Forbidden in future Layer-2 (must NOT appear in diff):

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
  (no `02_02_01` row; closure follows future materialization)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
  (no `02_02` row; deferred to first 02_02 transition PR; Outcome-E
  adjudication)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`
  (Phase 02 stays `in_progress`)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
  (per data-analysis-lineage sequence step 1 — ROADMAP stub PR produces
  no research_log entry; PR #232, #239, #253 precedents)
- `reports/research_log.md` (root)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md`
- any artifact under `reports/artifacts/02_02_01/` or
  `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`
- any byte change to
  `reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}` or
  `02_01_03_history_enriched_pre_game_features.parquet`
- any source `.py`, test `.py`, notebook `.py`/`.ipynb`
- any spec under `reports/specs/` or schema YAML under
  `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/`
- any AoE2 path under `src/rts_predict/games/aoe2/**`
- any thesis chapter, bib, appendix under `thesis/**`
- any `docs/**`, `.claude/**`, or `data/**` path
- any Step block other than the new `02_02_01` block in ROADMAP.md
- the §02_01_03 materialization-scope-amendment back-references at
  L2837-L2849 (must remain byte-unchanged)

## Gate Condition

**Layer-1 gate (THIS PR):** satisfied iff ALL of:
1. PR diff = exactly two files (`planning/current_plan.md` +
   `planning/current_plan.critique.md`).
2. PR is open as draft.
3. `planning/current_plan.md` contains all eight required `##` sections
   (Scope, Problem Statement, Assumptions & Unknowns, Literature Context,
   Execution Steps, File Manifest, Gate Condition, Open Questions).
4. Reviewer-adversarial returns APPROVE or APPROVE-WITH-NITS with zero
   blockers; verdict recorded in `current_plan.critique.md`.

**Layer-2 gate (FUTURE execution PR):** satisfied iff ALL of:
1. PR diff = exactly four files (ROADMAP.md + planning/INDEX.md +
   CHANGELOG.md + pyproject.toml).
2. ROADMAP.md contains exactly ONE new `### Step 02_02_01 — ...` block
   at the declared position, containing the 12 required content items
   (enumerated below). All other Step blocks (02_01_01, 02_01_02,
   02_01_03, 02_01_99) and the §02_01_03 amendment back-reference
   (L2837-L2849) are byte-identical to master `2c9080ae`.
3. `pyproject.toml` reads `version = "3.83.0"`.
4. `CHANGELOG.md` has a new
   `## [3.83.0] — YYYY-MM-DD (PR #N: feat/sc2egset-02-02-01-roadmap-stub)`
   block under `[Unreleased]`, above `[3.82.1]`.
5. `planning/INDEX.md` Archive table contains rows for PR #262 (chore
   closure) and this Layer-1 PR; new Active line is the Layer-2 branch.
6. NO Parquet, CSV, MD, JSON artifact change anywhere.
7. NO `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`,
   `PHASE_STATUS.yaml`, or `research_log.md` (dataset / root) byte change.
8. NO source `.py`, test `.py`, notebook `.py`/`.ipynb`, spec, schema
   YAML, AoE2, thesis, docs, .claude, data path byte change.
9. Pre-commit hooks pass (ruff/mypy not triggered on no-`.py` diff;
   plan-section hook not triggered on non-plan diff).
10. `git log master..HEAD --stat` shows the standard two-commit pattern
    (feature commit + chore release-bump commit) per
    `.claude/rules/git-workflow.md`.

## Open Questions

- **OQ1 — 02_01_99 fate.** Retained in place. Deletion would mutate
  the 02_01_03 materialization-scope-amendment lineage (ROADMAP L2841-
  L2849 explicitly cross-references it). Deferral is not a recognised
  ROADMAP state — blocks are either present or absent. 02_01_99 already
  exists as a documented ROADMAP-only stub with no STEP_STATUS row;
  its continued presence has zero cost and preserves git-blame traceability
  to PR #253 / PR #255.

- **OQ2 — Predecessor token.** `02_01_03` selected (single string scalar
  matching ROADMAP L2360, L2691 convention). NOT `02_01` (no precedent
  for sectional predecessor token), NOT `02_01_99` (02_01_99 is a
  decision-lineage sibling, not a feature-input producer; its predecessor
  field reads `"02_01_03"` itself — L2691).

- **OQ3 — PIPELINE_SECTION_STATUS `02_02` row timing.** Deferred to a
  future PR, NOT this Layer-2 ROADMAP stub. Verified precedent: 02_01
  row first landed in PR #230 (closure of 02_01_01), not in PR #232
  (stub). The natural moment to add `02_02` is when the first 02_02
  step closes (mirrors 02_01 ladder). The header derivation rule on
  L11 — `in_progress` when ANY step is `in_progress` or `complete` —
  does NOT trigger on a ROADMAP-only stub.

- **OQ4 — Version bump policy.** Minor `3.82.1 -> 3.83.0` chosen against
  three internal precedents: PR #232 (`3.66.0 -> 3.67.0`), PR #239
  (`3.70.1 -> 3.71.0`), PR #253 (`3.78.0 -> 3.79.0`) — all minor for
  ROADMAP-only stubs on `feat/` branches. Patch (`3.82.2`) would be a
  policy break; chore-only is not appropriate (this is `feat/` opening
  a new pipeline section, not maintenance).

- **OQ5 — Pipeline-section heading inclusion in ROADMAP.** The repo
  ROADMAP file uses H2 for Phase headings only; Step blocks are H3
  directly. There is NO `## Pipeline Section 02_01` heading between
  the Phase 02 heading and the first 02_01 Step block (verified by
  inspecting L1905-L2099). The 02_02_01 block therefore appears as
  H3 directly without a wrapping `## Pipeline Section 02_02` heading.
  The `pipeline_section` field within the yaml block carries the
  pipeline-section name (`"02_02 — Symmetry & Difference Features"`),
  consistent with all prior 02_01 blocks (L2127, L2313, L2652).

- **OQ6 — 02_02 vs 02_05 scope boundary.** Race-pair encoded interactions
  are the canonical 02_05 (Categorical Encoding & Interactions) family
  per manual §6. The 02_02 stub item 9 lists race-pair interactions as
  a candidate with explicit "may defer to 02_05" annotation; the binding
  decision is taken at the Layer-2 source-anchor adjudication step
  analogous to PR #234, not in this stub. Reviewer-adversarial nit N2.

## Required content for the future ROADMAP `02_02_01` block (12 items)

The Layer-2 executor must produce a single fenced yaml block with these
12 mandatory items (one sentence each; not aspirational, definite scope):

1. `step_number: "02_02_01"` — grep-visible string.
2. `pipeline_section: "02_02 — Symmetry & Difference Features"` — exact
   string per `docs/PHASES.md` Phase 02 row 2.
3. `predecessors: "02_01_03"` — single string scalar matching ROADMAP
   idiom (Outcome-3 adjudication; see OQ2 above).
4. Statement in `description`: "ROADMAP-only stub declaring Step
   02_02_01 — the first step of Pipeline Section 02_02 (Symmetry &
   Difference Features). NO ARTIFACT is emitted in this ROADMAP-stub
   PR — this entry only declares the future step per
   `.claude/rules/data-analysis-lineage.md` 'Non-batching rule for
   empirical work' sequence step 1; the notebook scaffold + one
   validation module + any adjudication artifacts + materialization
   are produced by SEPARATE FUTURE PRs (sequence steps 2-9)."
5. Statement in `description` halt-clause section: "Phase 03 is BARRED
   by this stub; Step 02_02_02+ is BARRED; Step 02_01_04 is BARRED;
   no baseline modeling."
6. Methodological purpose (in `description` and `question`): "Transform
   focal/opponent paired features from Step 02_01_03's materialized
   Parquet into symmetric / difference representations that (a)
   eliminate slot-assignment bias per Invariant I5 (focal/opponent
   symmetry), (b) inherit Invariant I3 strict
   `history_time < target_time` cutoff already enforced upstream,
   (c) produce model-input columns suitable for downstream Phase 03
   splitting / Phase 04 modeling, (d) avoid encoding
   `player_1_value - player_2_value` (slot-dependent) in favour of
   `focal_value - opponent_value` (slot-orthogonal), (e) preserve row
   identity (`focal_match_id`, `focal_player_id`) and the `started_at`
   temporal anchor verbatim."
7. `manual_reference: "02_FEATURE_ENGINEERING_MANUAL.md, Section 3"`
   + `external_references` cite `docs/PHASES.md` Phase 02 row 2
   (`02_02`), `02_FEATURE_ENGINEERING_MANUAL.md §3` (symmetric/
   difference features), `reports/specs/02_02_feature_engineering_plan.md`
   §5.1 (focal/opponent symmetry, Invariant I5) and §10 G-L-8 (no
   row-order leakage from slot asymmetry), AND
   `reports/specs/02_03_temporal_feature_audit_protocol.md` (downstream
   temporal-window/decay/cold-start audit spec; explicitly scoped OUT
   of this stub — referenced so the stub's halt-clauses do not silently
   encroach on 02_03).
8. `inputs.prior_artifacts` pointers:
   - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet`;
   - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_features.parquet`;
   - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.{json,md}`;
   - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}`;
   - the §02_01_03 materialization-scope-amendment back-reference
     at L2525-L2618 (PR #257) and the PR #255 omit-closure artifact.
9. Candidate future feature families (declared as `planned, NOT created
   in this PR`):
   - **race-pair encoded interactions** (candidate; may defer to 02_05 —
     Categorical Encoding & Interactions per manual §6; binding decision
     to be taken in the Layer-2 source-anchor adjudication PR analogous
     to PR #234, NOT in this stub);
   - **focal/opponent numeric history difference features** (e.g.,
     `prior_win_rate_diff = focal_prior_win_rate - opponent_prior_win_rate`)
     over the 02_01_03 history-enriched columns;
   - **symmetric pair features** under each family (mean, sum, product,
     absolute-difference) for inspection purposes per
     `02_FEATURE_ENGINEERING_MANUAL.md §3` representation options;
   - **matchup-history interaction / difference features** combining
     matchup-conditional and per-player history columns;
   - **cross-region-fragmentation indicator handling per PR #243 /
     PR #255 lineage** (sensitivity-indicator co-registered alongside
     any difference feature; no strict-exclusion path; mirror PR #259
     materialization choice exactly).
10. Explicit exclusions (in `description` and `gate.halt_predicate`):
    - `reconstructed_rating` family and any `reconstructed_rating_*`
      column (per PR #255 omit-closure + PR #257 amendment + PR #259
      materialization);
    - target-match outcome (game T result) — Invariant I3 + G-L-3;
    - future-match features (any match strictly after target T) —
      Invariant I3 + G-L-7;
    - Phase 03 split-derived features (no split exists yet);
    - tracker-derived target-match features (Amendment 2 of PR #208
      + `tracker_events_feature_eligibility.csv`);
    - `player_1_value - player_2_value`-style slot-dependent differences
      (Invariant I5 + G-L-8 + RISK-24);
    - any new MMR scalar feature (PR #234 `is_mmr_missing` flag
      precedent stands).
11. `gate.continue_predicate` / future gates: input artifact SHA checks
    (02_01_02 + 02_01_03 Parquet + both 02_01_x audit pairs); exact row
    alignment with `02_01` artifacts (row count equal to the measured
    row count of the `02_01_03` Parquet artifact, re-measured by Layer-2
    execution rather than hard-coded — reviewer-adversarial nit N3);
    `02_01_02_pre_game_features.parquet` and
    `02_01_03_history_enriched_pre_game_features.parquet` byte-unchanged
    in any future 02_02 PR; no materialization in this stub; no
    status-YAML / research_log changes in this stub (beyond the Layer-2
    4-file manifest); Phase 03 barred until 02_02 closes; cross-region
    indicator handling must follow PR #243 / PR #255 lineage exactly;
    per-dataset Invariants I3, I5, I6, I7, I8, I9, I10 declared upheld
    with `how_upheld` bullets each.
12. Statement: "Future `02_02` execution requires a separate scaffold +
    one-validation-module + adjudication + materialization plan PR after
    this ROADMAP stub merges. The non-batching rule sequence
    (steps 2-9) is preserved exactly as it was for Step 02_01_02
    (PRs #232 -> #233 -> #234 -> #235 -> #236 -> #237) and Step 02_01_03
    (PRs #239 -> #241 -> #242 -> ... -> #259 -> #262). The stub does not
    pre-commit a specific future-PR ladder count; that ladder is shaped
    by the adjudication and review process."

---

## Reviewer-adversarial nits applied (Layer-1 materialization)

The four non-blocking nits from `current_plan.critique.md` are integrated
into this plan as follows:

- **N1 (drop AoE2 terminology):** item 9 first family reads
  "race-pair encoded interactions" — no `civilization` token anywhere in
  this plan body. SC2EGSet uses `race` exclusively.
- **N2 (annotate 02_02 vs 02_05 scope):** item 9 first family carries the
  explicit "candidate; may defer to 02_05 — Categorical Encoding &
  Interactions" annotation; matched by OQ6 and A13.
- **N3 (no hard-coded row count gate):** item 11 reads "row count equal
  to the measured row count of the `02_01_03` Parquet artifact,
  re-measured by Layer-2 execution rather than hard-coded." A6 updated
  to remove binding row-count claim.
- **N4 (read 02_03 temporal spec at Layer-1):** L1.1 explicitly lists
  `reports/specs/02_03_temporal_feature_audit_protocol.md`; item 7
  carries the spec into the future ROADMAP block's `external_references`
  with the scoped-out annotation.
