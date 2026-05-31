---
title: "SC2EGSet Step 02_03_01 V3 scaffold (Layer-1 planning PR; strict-< temporal-discipline validator; immediately-next scaffold rung after PR #276 V1)"
category: A
branch: feat/sc2egset-02-03-01-v3-temporal-discipline-plan
base_ref: master
base_sha: 37c3a8855af038bd1bd4eefbdbd03497da323d47
predecessor_pr: 276
predecessor_pr_merge_sha: 37c3a8855af038bd1bd4eefbdbd03497da323d47
dataset: sc2egset
phase: "02"
pipeline_section: "02_03 — Temporal Features, Windows, Decay, Cold Starts"
invariants_touched: [I3, I5, I6, I7, I8, I9, I10]
draft_pr_files:
  - planning/current_plan.md
  - planning/current_plan.critique.md
future_execution_files:
  - src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_discipline.py
  - tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_temporal_discipline.py
  - sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_v3_scaffold.py
  - sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_v3_scaffold.ipynb
  - pyproject.toml
  - CHANGELOG.md
  - planning/INDEX.md
future_execution_file_count: 7
target_version_bump: "3.88.0 -> 3.89.0"
critique_required: true
research_log_ref: null
date: 2026-05-31
v1_predecessor_pr: 276
v1_predecessor_sha: 37c3a8855af038bd1bd4eefbdbd03497da323d47
v3_immediately_next_committed_by:
  - "validate_temporal_feature_grid.py docstring lines 3-4 (V3 separation clause)"
  - "CHANGELOG [3.88.0] Notes entry (V3 deferred to IMMEDIATELY-NEXT scaffold rung per NIT-2 of PR #275 plan)"
  - "PR #275 plan NIT-2 commitment"
reviewer_adversarial_round1: APPROVE-WITH-NITS
reviewer_adversarial_blockers: 0
reviewer_adversarial_nits: 5
nits_applied: [N-A, N-B, N-C, N-D, N-E]
---

## Scope

Author the Layer-1 planning artefact for the future Layer-2 **V3 scaffold PR** for Step `02_03_01` — strict-`<` temporal-discipline validator. This is the IMMEDIATELY-NEXT scaffold rung after V1 (PR #276, merged at master `37c3a8855af038bd1bd4eefbdbd03497da323d47`). The V3 rung was committed by:

1. The V1 module docstring in `validate_temporal_feature_grid.py` lines 3-4: "Future temporal-discipline checks (V3) must land in a separate validator module under a separate scaffold rung."
2. The CHANGELOG `[3.88.0]` Notes entry: "V3 (strict-`<` temporal-discipline) deferred to the IMMEDIATELY-NEXT scaffold rung per NIT-2 of PR #275 plan."
3. PR #275 plan NIT-2 commitment.

V3 scope: **DESIGN-TIME ONLY** (schema metadata + Parquet footer + file SHA + provenance docstring text). NO data-value reads. NO re-computation. NO source DuckDB queries. Separate from V1; V3 must NOT modify V1 or import V1 constants (per V1 docstring constraint).

This plan mirrors the PR #273 → PR #274 → PR #275 → PR #276 four-PR precedent for the V1 scaffold. The V3 Layer-1 (this PR) + V3 Layer-2 (future PR) pair is the strict analogue: Layer-1 writes only two files; Layer-2 performs the 7-file manifest declared in §File Manifest below.

**Two-PR sequence on this branch.**

1. **THIS Layer-1 planning PR** writes only two files:
   - `planning/current_plan.md` (this document);
   - `planning/current_plan.critique.md` (reviewer-adversarial Round 1 output).
2. **FUTURE Layer-2 V3 scaffold execution PR** performs the 7-file manifest declared in §File Manifest below (V3 validator module + mirrored test + jupytext-paired notebook pair + pyproject 3.88.0 → 3.89.0 minor bump + CHANGELOG block + planning/INDEX.md update). This mirrors the PR #275 → PR #276 7-file Layer-2 template.

**Out of scope (V3 design surface — declared here, enforced by Layer-2 falsifiers):**

- concrete temporal window sizes
- decay half-lives
- cold-start k-thresholds
- tracker_events family inclusion decision
- in-game temporal scope decision
- any feature materialization
- any artifact emission to `reports/artifacts/02_feature_engineering/03_temporal_features/**`
- any ROADMAP / STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS / dataset research_log / root research_log edits
- Phase 03 activation or baseline modeling
- any empirical AoE2 transferability claim

## Problem Statement

PR #276 (merged at master `37c3a8855af038bd1bd4eefbdbd03497da323d47`) shipped V1: the SHA-pin predecessor artifact provenance validator. V1 audits that the four predecessor Parquet/CSV artifacts exist at expected paths, have expected SHA256 hashes, carry expected identity columns, and have expected row counts. V1 does NOT validate any temporal feature grid.

The V1 module docstring explicitly commits: "Future temporal-discipline checks (V3) must land in a separate validator module under a separate scaffold rung." This commitment was mandated by PR #275 plan NIT-2 and is recorded in CHANGELOG `[3.88.0]` Notes.

Without V3, the adjudication PR will pin concrete window/decay/cold-start values without any tested temporal-discipline gate in the codebase. This creates a structural gap: Invariant I7 (no feature uses data with `history_time >= T` for target game T) would never be directly exercised at design time before concrete grid values are pinned. The temporal-discipline invariant is the core leakage guard for the entire Phase 02 feature engineering ladder.

V3 closes this gap by implementing a strict-`<` temporal-discipline validator at DESIGN TIME: given a Parquet feature grid and a sample of target game timestamps, V3 asserts that for every target game T, no feature column uses data from a record where `history_time >= T`. V3 is schema-level + provenance-level: it validates naming conventions, column presence (temporal anchor `started_at`), and cite-string provenance — NOT data values. Value-level leakage detection (post-materialization) is handled separately by CROSS-02-01 audits.

V3 is structurally and semantically distinct from V1:

- V1 audits predecessor artifact provenance (SHA-pin, identity columns, row counts).
- V3 audits temporal-discipline compliance (history-column naming convention, temporal-anchor presence, cite-string provenance).
- V3 must NOT import from V1 (per V1 docstring separation clause).
- V3 lives in a separate module: `validate_temporal_discipline.py`.

## Literature Context

Per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical work" step 2 ("Notebook scaffold + one validation module"), the scaffold declares scope and delivers exactly one validator; no feature materialisation, no artifact generation.

**Binding commitment from V1 docstring.** The V3 scaffold is not optional — it is the binding obligation declared by the V1 module docstring at `validate_temporal_feature_grid.py` lines 3-4:

> "Future temporal-discipline checks (V3) must land in a separate validator module under a separate scaffold rung."

This is the authoritative V3-next commitment. The CHANGELOG `[3.88.0]` Notes entry reinforces it: "V3 (strict-`<` temporal-discipline) deferred to the IMMEDIATELY-NEXT scaffold rung per NIT-2 of PR #275 plan."

**V3 is the IMMEDIATELY-NEXT rung; no adjudication before V3.** Without V3 landing before the adjudication PR, concrete window/decay/k-threshold values would be committed without a tested temporal-discipline gate. The ROADMAP `continue_predicate` at `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` lines 3372-3384 mandates that each scaffold rung precede adjudication. V3 is a scaffold rung; it must land before the adjudication PR.

**V3 scope: DESIGN-TIME ONLY.** V3 validates:

- History-column naming convention: columns named with the `*_prior_*` pattern are assumed history-window features; columns NOT following this convention in the feature grid are flagged.
- Temporal-anchor presence: the `started_at: timestamp[us]` column must be present in the feature grid schema.
- Cite-string provenance: the V3 module docstring must include 6 verbatim cite-strings from CROSS-02-03-v1.0.1 §1.2 audit dimensions D1/D2/D3/D4/D5/D6 (schema-level).

V3 does NOT open Parquet data rows for value inspection. It reads Parquet schema footer (column names + dtypes) and module docstring text only. This is the strict DESIGN-TIME scope.

**V3 is a schema-level complement to CROSS-02-01 value-level.** V3 is a schema-level design-time gate enforcing strict-`<` temporal discipline via history-naming convention, temporal-anchor presence, and cite-string provenance. Value-level leakage (sophisticated semantic leaks not detectable from schema metadata alone) is gated separately by post-materialization audits per CROSS-02-01-v1.0.1. V3 and CROSS-02-01 are complementary, not redundant. V3 catches the common contributor failure modes (forbidden column naming, missing temporal anchor, missing cite-strings); CROSS-02-01 catches sophisticated semantic leaks at the value layer.

**PR #276 version bump precedent.** PR #276 (`feat/sc2egset-02-03-01-scaffold-plan`) bumped `pyproject.toml` version `3.87.0 → 3.88.0` (minor; feat-class scaffold precedent), confirmed via `gh pr view 276 --json files --jq '.files[] | select(.path=="pyproject.toml")'`. The current version is `3.88.0` (post-PR #276 V1 scaffold). The Layer-2 V3 scaffold PR target bump is `3.88.0 → 3.89.0` (minor; same feat-class rule). PR #266 (`3.83.0 → 3.84.0`) and PR #276 (`3.87.0 → 3.88.0`) are both confirmed precedents.

**Per `.claude/rules/git-workflow.md`** "minor for feat/refactor/docs", a scaffold PR that opens a new validation rung is a feat-class minor bump. PR #266 (`3.83.0 → 3.84.0`), PR #241 (`3.71.0 → 3.72.0`), and PR #276 (`3.87.0 → 3.88.0`) confirmed this rule. Same rule applies to V3.

The three LOCKED cross-dataset specs relevant to Pipeline Section `02_03` are:

- **CROSS-02-00-v3.0.1** (LOCKED 2026-04-26; `reports/specs/02_00_feature_input_contract.md`): the cross-dataset feature input contract governing all Phase 02 steps.
- **CROSS-02-02-v1.0.1** (LOCKED 2026-05-06; `reports/specs/02_02_feature_engineering_plan.md`): the cross-dataset feature engineering plan listing temporal / window / decay / cold-start families.
- **CROSS-02-03-v1.0.1** (LOCKED 2026-05-06; `reports/specs/02_03_temporal_feature_audit_protocol.md`): the cross-dataset design-time temporal feature audit protocol; binds `[sc2egset, aoestats, aoe2companion]` for audit dimensions D1–D15. V3 validator cite-strings reference this spec.

**Q8 cross-game portability.** V3 is scoped to design-time schema validation only. Cross-game portability of the V3 design pattern is restricted to a syntactic-only observation: where the validator uses candidate-agnostic vocabulary (focal/opponent, history window, started_at, prior, target-game exclusion) rather than game-specific names, the design pattern is portable. No empirical AoE2 transferability claim is made; that determination is deferred to a future AoE2-specific Phase 02 step. This is verifiable by grep falsifiers H6 (cross-game-portable vocabulary) and H7 (Q8 syntactic-only guard) at Layer-2 execution.

## Assumptions & Unknowns

**A-1. V1 predecessor merge SHA.** PR #276 (V1 predecessor artifact provenance validator scaffold) merged at master `37c3a8855af038bd1bd4eefbdbd03497da323d47`. Layer-2 T01 must verify `git rev-parse master` matches this SHA before construction. If it differs, halt and report.

**A-2. V1 module byte-stability.** The `validate_temporal_feature_grid.py` file is byte-stable between Layer-1 merge and Layer-2 merge. V3 must NOT modify V1 (per V1 docstring separation clause). Layer-2 T01 must verify the V1 module SHA is unchanged before constructing V3.

**A-3. pyproject version baseline.** `pyproject.toml` declares `version = "3.88.0"` (post-PR #276). Layer-2 target bump: `3.88.0 → 3.89.0` (minor per `.claude/rules/git-workflow.md` feat-class rule; mirrors PR #276 `3.87.0 → 3.88.0` and PR #266 `3.83.0 → 3.84.0`).

**A-4. V3 validator module scope (strict-< temporal-discipline; DESIGN-TIME ONLY).** The V3 validator module shipped in the Layer-2 scaffold PR:

- Accepts a Parquet feature grid path and reads schema footer (column names + dtypes) only — NO data row reads.
- Validates history-column naming convention: `*_prior_*` pattern must be present for any column intended as a history feature; forbidden patterns (e.g., `*_current_*`, `*_target_*`) must be absent.
- Validates temporal-anchor presence: `started_at: timestamp[us]` must be in the schema.
- Validates cite-string provenance: module docstring must include verbatim cite-strings from CROSS-02-03-v1.0.1 §1.2 D1-D6.
- Does NOT compute any feature values. Does NOT query DuckDB. Does NOT read from `data/**`.
- Returns a typed result object (dataclass or NamedTuple) with `passed`, `halting_falsifier`, `schema_checked`, `temporal_anchor_present`, `history_naming_valid`, `cite_strings_present` fields.
- Must NOT import from `validate_temporal_feature_grid.py` (V1 separation clause).

**A-5. V3 uses cross-game-portable vocabulary only.** V3 validator function signatures, docstrings, and test module use cross-game-portable vocabulary only: `focal`/`opponent`, `history window`, `started_at`, `prior`, `target-game exclusion`. SC2-specific terms (`race`, `mineral`, `vespene`, `PlayerStats`, `tracker_events`, `toon_id`, `apm`, `sq`) and AoE2-specific terms (`civilization`, `civ`, `profile_id`, `leaderboard`) must not appear in public interfaces where avoidable. This is verifiable by grep falsifiers H6 and H7.

**A-6. PR #276 version bump verified.** `gh pr view 276 --json files --jq '.files[] | select(.path=="pyproject.toml")'` confirms PR #276 modified `pyproject.toml` with +1/-1 (version bump). The PR #276 CHANGELOG entry confirms version `3.87.0 → 3.88.0` minor. The current version `3.88.0` (post-PR #276) makes the Layer-2 target `3.88.0 → 3.89.0` minor. This precedent is confirmed and locked.

**A-7. PIPELINE_SECTION_STATUS NOT touched.** No `02_03` row added or modified by the V3 scaffold PR. The first-step-closure rule applies.

**A-8. STEP_STATUS NOT touched.** No `02_03_01` row added by the V3 scaffold PR. The `02_03_01` row is added only when the step closes (after materialization + leakage audit + U2.B closure PR).

**A-9. PHASE_STATUS.yaml NOT touched.** Phase 02 stays `in_progress`; Phase 03 stays `not_started`. No PHASE_STATUS row added or modified by the Layer-2 V3 scaffold execution PR. Phase 02 closure (and Phase 03 readiness) require future U2.B-style closure PR(s) downstream of adjudication + materialization rungs.

**A-10. planning/INDEX.md edits.** Two coupled edits:

1. **Active line rewrite.** Replace the current Active line (describing the now-merged Layer-2 V1 scaffold PR #276) with the new Active line for the Layer-2 V3 scaffold PR on `feat/sc2egset-02-03-01-v3-temporal-discipline-plan`. Required content: V3 scaffold scope; "no ROADMAP / status YAML / research_log / artifact / Phase 03"; version bump `3.88.0 → 3.89.0`; future PR number placeholder `PR #<TBD>`.
2. **Archive PR #276.** Insert a new row in the archive table for PR #276 (Layer-2 V1 scaffold for `02_03_01`; merge SHA `37c3a885`; date 2026-05-30; Category A).

**A-11. CHANGELOG block.** New `## [3.89.0] — <date> (PR #<TBD>: feat/sc2egset-02-03-01-v3-temporal-discipline-plan)` block inserted above the existing `## [3.88.0]` block. Block must contain `### Added` bullet for the V3 scaffold + one validation module and `### Notes` bullets (`**No feature materialization.**`, `**No STEP_STATUS row.**`, `**No PIPELINE_SECTION_STATUS row.**`, `**No PHASE_STATUS mutation.**`, `**No research_log entry.**`, `**No ROADMAP edit.**`, `**No Phase 03.**`, `**No baseline modeling.**`, `**No concrete window sizes, decay half-lives, or cold-start k-thresholds.**`).

**A-12. Branch slug.** `feat/sc2egset-02-03-01-v3-temporal-discipline-plan` (this Layer-1 planning PR branch). The future Layer-2 V3 scaffold PR may land on the same branch or a new branch — to be determined at Layer-2 planning time, mirroring the PR #275 → PR #276 precedent.

**A-13. No coverage gate impact for Layer-1.** Pre-commit hooks (`ruff` + `mypy`) run on `.py` file changes. The Layer-2 scaffold PR adds `.py` files; pytest coverage must be ≥ 35 tests and ≥ 95% branch coverage on the V3 validator module (per PR #276 precedent: ≥35 tests, ≥95% branch coverage). The Layer-1 planning PR (this PR) touches zero `.py` files; no pytest run required.

**A-14. tracker_events_feature_eligibility.csv byte-stability.** The file at `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv` is byte-stable between Layer-1 merge and Layer-2 merge. If the file mutates, the Layer-2 PR halts before push.

**A-15. Cross-game-portable vocabulary.** The V3 validator module, mirrored test, and notebook scaffold use cross-game-portable vocabulary only (focal/opponent, history window, started_at, prior, target-game exclusion) and do NOT name SC2-specific terms (race, mineral, vespene, PlayerStats, tracker_events, toon_id, apm, sq) or AoE2-specific terms (civilization, civ, profile_id, leaderboard) where avoidable. No empirical AoE2 transferability claim is made; that determination is deferred to a future AoE2-specific Phase 02 step. This is verifiable by grep falsifiers H6 (cross-game-portable vocabulary) and H7 (Q8 syntactic-only guard) at Layer-2 execution.

**Unknowns** (resolved at Layer-2 T01, not at Layer-1):

- **U-1.** The exact date of the Layer-2 V3 scaffold PR merge (enters CHANGELOG date header and planning/INDEX archive row).
- **U-2.** Whether the Layer-2 PR lands on the same branch as Layer-1 or a new branch. To be determined at Layer-2 planning time.
- **U-3.** Exact prose for the notebook scaffold's hypothesis + falsifier declaration cells. Bound by CROSS-02-03-v1.0.1 §1.2 "out of scope" list; exact prose drafted at Layer-2 T01.

## Execution Steps

The future Layer-2 V3 scaffold PR executes the following tasks based off `master@37c3a8855af038bd1bd4eefbdbd03497da323d47`. Each task is a delegated executor step.

**T01 — Verify base state (Sonnet executor).**

- Verify `git rev-parse master == 37c3a8855af038bd1bd4eefbdbd03497da323d47`.
- Verify `pyproject.toml` `version = "3.88.0"`.
- Verify STEP_STATUS has `02_02_01: complete` row; `02_03_01` row is absent (not yet closed).
- Verify PIPELINE_SECTION_STATUS has `02_02: complete` row; `02_03` row is absent.
- Verify PHASE_STATUS Phase 02 `in_progress` / Phase 03 `not_started`.
- Verify ROADMAP.md has `02_03_01` block (inserted by PR #274).
- Verify `reports/artifacts/02_02_01/leakage_audit_sc2egset.json` exists with `verdict=PASS`.
- Verify `validate_temporal_feature_grid.py` (V1) exists at canonical path and contains the V3-separation clause in its docstring.
- Verify `validate_temporal_discipline.py` does NOT yet exist (V3 creates it fresh).
- Verify `tracker_events_feature_eligibility.csv` exists at canonical path.
- Verify the V1 module SHA (record for byte-stability check in T02).

Stop condition: any precondition fails → HALT, escalate to user.

Allowed files: NONE for write — Read-only verification only.

Forbidden files: ALL.

Required validation report: short summary echoing the 11 verifications.

**T02 — Create V3 validator module (Sonnet executor; module docstring per NIT-E framing).**

Allowed files:
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_discipline.py`.

Forbidden files: ALL others. Explicitly forbidden: `validate_temporal_feature_grid.py` (V1; must remain byte-stable).

Create the V3 strict-`<` temporal-discipline validator. Module docstring must include VERBATIM the following framing statement (NIT-E):

"V3 is a schema-level design-time gate enforcing strict-`<` temporal discipline via history-naming convention, temporal-anchor presence, and cite-string provenance. Value-level leakage (sophisticated semantic leaks not detectable from schema metadata alone) is gated separately by post-materialization audits per CROSS-02-01-v1.0.1. V3 and CROSS-02-01 are complementary, not redundant. V3 catches the common contributor failure modes (forbidden column naming, missing temporal anchor, missing cite-strings); CROSS-02-01 catches sophisticated semantic leaks at the value layer."

Module must additionally:

- Include 6 verbatim cite-strings from CROSS-02-03-v1.0.1 §1.2 audit dimensions D1-D6.
- Validate history-column naming convention (`*_prior_*` pattern present; forbidden patterns absent).
- Validate temporal-anchor `started_at: timestamp[us]` presence in schema.
- Read Parquet schema footer only — NO data row reads, NO DuckDB queries.
- Use cross-game-portable vocabulary in all function signatures and docstrings (focal/opponent, history window, started_at, prior — not SC2-specific names where avoidable).
- Accept no concrete window sizes, decay half-lives, or cold-start k-thresholds as parameters.
- Return a typed result object (dataclass or NamedTuple) with `passed`, `halting_falsifier`, `schema_checked`, `temporal_anchor_present`, `history_naming_valid`, `cite_strings_present` fields.
- NOT import from `validate_temporal_feature_grid.py`.

Stop condition: any file outside allowed list touched; module imports from V1; module defines concrete grid values; module reads Parquet data rows; module uses forbidden vocabulary → HALT.

Required validation report: `git diff --stat` shows only the new V3 validator file; `grep -n 'V3 is a schema-level design-time gate' src/.../validate_temporal_discipline.py` returns the module docstring framing statement.

**T03 — Create mirrored test module (Sonnet executor).**

Allowed files:
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_temporal_discipline.py`.

Forbidden files: ALL others. Explicitly forbidden: `test_validate_temporal_feature_grid.py` (V1 tests; must remain byte-stable).

Create the mirrored test module. Tests must:

- Cover ≥ 35 tests with ≥ 95% branch coverage on `validate_temporal_discipline.py`.
- Include schema-valid and schema-invalid positive and negative controls.
- Include temporal-anchor presence/absence tests.
- Include history-column naming convention valid/invalid tests.
- Include cite-string presence/absence tests.
- Include a halt-priority test verifying first-failure-wins ordering.
- Include a test asserting V3 does NOT import from V1 (`validate_temporal_feature_grid`).
- Use `pytest.mark.parametrize` for boundary sweep tests.

Stop condition: any file outside allowed list touched; coverage below 95% → HALT.

Required validation report: `poetry run pytest tests/...test_validate_temporal_discipline.py -v --cov=rts_predict --cov-report=term-missing` passes with ≥ 35 tests, ≥ 95% branch coverage.

**T04 — Create jupytext-paired notebook scaffold (Sonnet executor).**

Allowed files:
- `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_v3_scaffold.py`
- `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_v3_scaffold.ipynb`

Forbidden files: ALL others.

Create the jupytext `py:percent` scaffold notebook. Notebook must:

- Follow sandbox/README.md hard rules: no inline definitions, 50-line cell cap, read-only DuckDB, jupytext percent-format.
- Declare hypothesis + falsifier + sanity-check up front in Markdown cells.
- Invoke the V3 validator (T02) with a sample Parquet schema and assert `passed=True` / `halting_falsifier=None` / `temporal_anchor_present=True` / `history_naming_valid=True` / `cite_strings_present=True`.
- Use `print()` for exploration output (not `logger`).
- NOT contain any `def`, `class`, or `lambda` in cells.
- NOT generate any artifact; no writes to `reports/artifacts/`.

Stop condition: notebook generates any artifact; notebook defines functions in cells; notebook uses forbidden vocabulary → HALT.

Required validation report: `jupytext --to notebook` produces a valid `.ipynb`; `nbconvert --execute` passes with no errors.

**T05 — Bump pyproject.toml (Sonnet executor).**

Allowed files:
- `pyproject.toml`.

Forbidden files: ALL others.

Edit: `version = "3.88.0"` → `version = "3.89.0"` (line 3; minor per feat-class rule).

Stop condition: any unintended file change → HALT.

Required validation report: `git diff pyproject.toml` shows only the version line change; `grep -RIn '__version__' src/` returns no matches.

**T06 — Add CHANGELOG.md [3.89.0] block (Sonnet executor).**

Allowed files:
- `CHANGELOG.md`.

Forbidden files: ALL others.

Insert `## [3.89.0] — <date> (PR #<TBD>: feat/sc2egset-02-03-01-v3-temporal-discipline-plan)` block between the existing `[Unreleased]` section and the existing `## [3.88.0]` block. Block content per A-11.

Stop condition: any unintended file change → HALT.

Required validation report: `git diff CHANGELOG.md` shows the new `[3.89.0]` block inserted above `[3.88.0]`; the `[Unreleased]` section and `[3.88.0]` block are byte-unchanged.

**T07 — Update planning/INDEX.md (Sonnet executor).**

Allowed files:
- `planning/INDEX.md`.

Forbidden files: ALL others.

Two coupled edits per A-10:

1. Replace the current Active line (describing PR #276) with the new Active line for the Layer-2 V3 scaffold PR.
2. Insert a new archive row immediately under the table header for PR #276.

Stop condition: any unintended file change → HALT.

Required validation report: `git diff planning/INDEX.md` shows the two intended edits and nothing else; `grep -n "37c3a885" planning/INDEX.md` returns the new PR #276 archive row.

**T08 — Local checks and wrap-up (Sonnet executor).**

Allowed: read-only verification, `git status`, `git log --stat`, `git diff --stat master..HEAD`.

Required checks:
- `git diff --stat master..HEAD` shows exactly 7 files in the manifest.
- `grep -nE '^## ' planning/current_plan.md | wc -l` returns 8.
- No forbidden vocabulary in V3 validator or test: grep falsifiers H6 and H7 from §Gate Condition both return zero matches in validator-design and test-scaffolding sections.
- Coverage: `poetry run pytest tests/.../test_validate_temporal_discipline.py --cov=rts_predict --cov-report=term-missing` → ≥ 35 tests, ≥ 95% branch coverage.
- No status YAML diff: `git diff --stat master..HEAD -- '**/STEP_STATUS.yaml' '**/PIPELINE_SECTION_STATUS.yaml' '**/PHASE_STATUS.yaml'` returns empty.
- No research_log diff: `git diff --stat master..HEAD -- '**/research_log.md'` returns empty.
- No ROADMAP diff: `git diff --stat master..HEAD -- 'src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md'` returns empty.
- V1 byte-stability: `git diff --stat master..HEAD -- 'src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_feature_grid.py'` returns empty.
- No V3 import of V1: `grep -n 'validate_temporal_feature_grid' src/.../validate_temporal_discipline.py` returns zero matches.

Stop condition: any check fails → HALT.

Required validation report: short summary echoing all checks; ready for commit/PR.

## File Manifest

This Layer-1 planning PR diff = exactly 2 files:
- `planning/current_plan.md` (this file)
- `planning/current_plan.critique.md` (reviewer-adversarial Round 1 output)

The future Layer-2 V3 scaffold PR diff = exactly 7 files (mirrors PR #276 7-file Layer-2 template):

| File | Action | Notes |
|---|---|---|
| `src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_discipline.py` | Create | V3 strict-`<` temporal-discipline validator. Module docstring per NIT-E framing: "V3 is a schema-level design-time gate enforcing strict-`<` temporal discipline via history-naming convention, temporal-anchor presence, and cite-string provenance. Value-level leakage (sophisticated semantic leaks not detectable from schema metadata alone) is gated separately by post-materialization audits per CROSS-02-01-v1.0.1. V3 and CROSS-02-01 are complementary, not redundant. V3 catches the common contributor failure modes (forbidden column naming, missing temporal anchor, missing cite-strings); CROSS-02-01 catches sophisticated semantic leaks at the value layer." Must NOT import from V1. Schema footer reads only. Cross-game-portable vocabulary. |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_temporal_discipline.py` | Create | Mirrored test module. ≥ 35 tests, ≥ 95% branch coverage. Schema-valid/invalid controls. Temporal-anchor tests. History-naming convention tests. Cite-string presence tests. Halt-priority test. V1-import-absence test. |
| `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_v3_scaffold.py` | Create | Jupytext `py:percent` scaffold. Hypothesis + falsifier declaration cells. V3 validator invocation. No artifact generation. No function/class/lambda definitions in cells. |
| `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_v3_scaffold.ipynb` | Create | Paired `.ipynb`. Outputs cleared before commit. Executes end-to-end via nbconvert with no errors. |
| `pyproject.toml` | Update | Version `3.88.0 → 3.89.0` (minor; feat-class scaffold precedent; PR #276 `3.87.0 → 3.88.0` and PR #266 `3.83.0 → 3.84.0` confirmed). |
| `CHANGELOG.md` | Update | Insert `## [3.89.0]` block between `[Unreleased]` and `[3.88.0]`. |
| `planning/INDEX.md` | Update | Active line rewrite + archive PR #276 row (merge SHA `37c3a885`). |

**Files that MUST remain byte-unchanged in Layer-2 (binding negative-space contract):**
- src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
- src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
- src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml
- src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml
- src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
- reports/research_log.md
- src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_feature_grid.py (V1; H1 falsifier's no-V1-import rule implies V1 cannot be edited as a side effect)
- src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/** (all subdirectories byte-stable)
- src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv
- reports/specs/02_00_feature_input_contract.md
- reports/specs/02_01_leakage_audit_protocol.md
- reports/specs/02_02_feature_engineering_plan.md
- reports/specs/02_03_temporal_feature_audit_protocol.md (CROSS-02-03 LOCKED 2026-05-06)
- docs/**
- .claude/**
- data/**
- src/rts_predict/games/aoe2/**
- thesis/**

## Gate Condition

The Layer-1 planning PR (this PR) is acceptable for merge when all of the following hold:

**G1.** `git diff --name-only HEAD` (relative to master) shows EXACTLY:
- `planning/current_plan.md`
- `planning/current_plan.critique.md`

**G2.** 8 required H2 headings literal match: `grep -cE '^## (Scope|Execution Steps|File Manifest|Problem Statement|Assumptions & Unknowns|Literature Context|Gate Condition|Open Questions)$' planning/current_plan.md` must equal 8.

**G3.** V3-next commitment cited: `grep -F 'IMMEDIATELY-NEXT scaffold rung' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'V3 is committed as the IMMEDIATELY-NEXT scaffold rung' planning/current_plan.md` returns ≥ 1 match (or equivalent wording confirming V3 is the immediately-next rung).

**G4.** NIT-E V3 docstring framing: `grep -F 'V3 is a schema-level design-time gate' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'CROSS-02-01 are complementary, not redundant' planning/current_plan.md` returns ≥ 1 match.

**G5.** V3 module separation clause documented: `grep -F 'validate_temporal_discipline.py' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'NOT import from' planning/current_plan.md` returns ≥ 1 match.

**G6.** Falsifiers documented: `grep -F 'H6' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'H7' planning/current_plan.md` returns ≥ 1 match.

**G7.** NIT-B byte-unchanged list: `grep -F 'Files that MUST remain byte-unchanged' planning/current_plan.md` returns ≥ 1 match.

**G8.** NIT-A out-of-scope list: `grep -F 'concrete temporal window sizes' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'empirical AoE2 transferability claim' planning/current_plan.md` returns ≥ 1 match.

**G9.** NIT-C A-15 vocabulary assumption: `grep -nF 'A-15' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'cross-game-portable vocabulary' planning/current_plan.md` returns ≥ 1 match.

**G10.** NIT-D A-9 PHASE_STATUS assumption: `grep -nF 'A-9' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'PHASE_STATUS.yaml NOT touched' planning/current_plan.md` returns ≥ 1 match.

**G11.** Round 2 re-gate trigger: if the materialized `planning/current_plan.md` fails any of the H6-H7 grep falsifiers or the 8-section literal-match check, the Layer-1 PR must escalate to reviewer-adversarial Round 2 on the materialized text. 3-round cap per `feedback_adversarial_cap_execution.md`. `grep -F 'Round 2' planning/current_plan.md` must return ≥ 1 match.

**Falsifier H6 (cross-game-portable vocabulary; NIT-C / A-15):** `grep -niE 'aoe2|civilization|aoestats|aoe2companion' planning/current_plan.md` — every match MUST be bounded as a forbidden-term constraint, a deferred-to-future-AoE2-specific context, a locked-spec citation, or a grep-falsifier definition; no unbounded transferability claim.

**Falsifier H7 (Q8 syntactic-only guard):** `grep -niE '\b(7|14|30|90|180)d\b|\b(7|10|14|30)_games?\b|half_life|k_threshold' planning/current_plan.md` — zero matches in validator-design or test-scaffolding sections. Matches permitted only in: (a) §Scope out-of-scope list, (b) §Gate Condition halt-clause, (c) grep-falsifier definitions.

**Layer-2 gate predicates (V3 falsifier chain H1-H7)** (applied by reviewer-adversarial before Layer-2 merge):

**H1. Predecessor existence + SHA byte-stability (V3 re-pins; no V1 import).** `git rev-parse master` must equal `37c3a8855af038bd1bd4eefbdbd03497da323d47`; V1 module (`validate_temporal_feature_grid.py`) SHA unchanged from Layer-1 merge; `grep -n 'validate_temporal_feature_grid' src/.../validate_temporal_discipline.py` returns zero matches (V3 does not import V1).

**H2. Temporal-anchor column `started_at: timestamp[us]` present.** `validate_temporal_discipline.py` validates `started_at` column presence and dtype in the feature grid schema footer. Test suite includes `started_at`-absent negative control.

**H3. History-column naming convention (`*_prior_*` present; forbidden patterns absent).** `validate_temporal_discipline.py` validates that any history-window column follows the `*_prior_*` naming convention and that forbidden patterns (e.g., `*_current_*`, `*_target_*` used as history columns) are absent.

**H4. Cross-spec citation provenance (6 verbatim cite-strings).** Module docstring includes 6 verbatim cite-strings from CROSS-02-03-v1.0.1 §1.2 audit dimensions D1-D6.

**H5. Forbidden-emission guard (V3 outputs dir must not exist).** `validate_temporal_discipline.py` asserts that the `reports/artifacts/02_feature_engineering/03_temporal_features/` directory does NOT exist at execution time (design-time gate; no materialization allowed). Test includes directory-absence assertion.

**H6. Cross-game-portable vocabulary.** `grep -niE 'race|mineral|vespene|PlayerStats|tracker_events|toon_id|apm_focal|apm_opp|sq_focal|sq_opp|civilization|civ\b|profile_id|leaderboard' src/.../validate_temporal_discipline.py` — zero matches in public function signatures and return-type fields. Permitted only in comments that name these as forbidden vocabulary examples.

**H7. Q8 syntactic-only guard.** `grep -niE 'aoe2|aoestats|aoe2companion|aoe2_.*transferab|transferab.*aoe2' src/.../validate_temporal_discipline.py tests/.../test_validate_temporal_discipline.py` — zero matches. No empirical AoE2 transferability claim in V3 source or test code.

**Halt conditions (Layer-2):**

**LG1.** `git diff --stat master..HEAD` shows exactly 7 files matching the §File Manifest.

**LG2.** `poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_temporal_discipline.py --cov=rts_predict --cov-report=term-missing` passes with ≥ 35 tests, ≥ 95% branch coverage.

**LG3.** `grep -nE 'V3 is a schema-level design-time gate' src/.../validate_temporal_discipline.py` returns the module docstring framing statement (NIT-E).

**LG4.** `grep -cE '^## \[3\.89\.0\]' CHANGELOG.md` returns 1.

**LG5.** `grep 'version' pyproject.toml | head -1` returns `version = "3.89.0"`.

**LG6.** `git diff --stat master..HEAD -- '**/STEP_STATUS.yaml' '**/PIPELINE_SECTION_STATUS.yaml' '**/PHASE_STATUS.yaml' '**/research_log.md' 'src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md' 'reports/research_log.md' 'src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/**' 'src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_feature_grid.py'` returns empty.

**LG7.** H6 + H7 falsifiers pass on V3 validator and test files (cross-game-portable vocabulary; no AoE2 empirical claim).

**Round 2 trigger:** If the materialized Layer-1 plan fails any of the H6/H7 grep falsifiers or the 8-section literal-match check (`grep -cE '^## (Scope|Execution Steps|File Manifest|Problem Statement|Assumptions & Unknowns|Literature Context|Gate Condition|Open Questions)$' planning/current_plan.md` must = 8), escalate to reviewer-adversarial Round 2. 3-round cap per `feedback_adversarial_cap_execution.md`.

## Open Questions

**Q1 — Adjudication sequencing.** V3 is committed as the IMMEDIATELY-NEXT scaffold rung before any adjudication PR. The adjudication PR (concrete window/decay/cold-start candidate selection) proceeds only after this V3 scaffold PR merges with a passing result. Plan default: V3 lands next; adjudication follows.

**Q2 — tracker_events families in 02_03.** V3 is agnostic to specific tracker families. The `tracker_events_feature_eligibility.csv` constrains which tracker families are eligible. V3 validates schema-level naming convention only; per-family eligibility is resolved at adjudication. Plan default: V3 scope references CROSS-02-03 and tracker eligibility CSV as gating artifacts; no tracker family included or excluded in V3.

**Q3 — Cold-start threshold selection.** Concrete cold-start k-thresholds are NOT pinned by V3. V3 accepts no k-threshold parameters. Threshold selection is deferred to the adjudication PR. Plan default: V3 comments note cold-start as a deferred parameter; no integer literals representing thresholds appear in module logic.

**Q4 — Window/decay parameter selection.** Concrete window sizes and decay half-lives are NOT pinned by V3. V3 is DESIGN-TIME ONLY; no concrete grid values in V3. Adjudication PR resolves these. Plan default: same as Q3 — deferred, zero concrete values in V3 scaffold.

**Q5 — AoE2 portability.** Cross-game portability of the V3 design pattern is restricted to a syntactic-only observation: where V3 uses candidate-agnostic vocabulary (focal/opponent, history window, started_at), the pattern is portable. No empirical AoE2 transferability claim. AoE2-specific transferability is deferred to a future AoE2-specific Phase 02 step. The CROSS-02-03 spec binds `[sc2egset, aoestats, aoe2companion]` for audit dimensions D1-D15; V3 cites CROSS-02-03 but makes no claim that V3's SC2EGSet execution validates AoE2 compliance. This is not a claim this plan makes — it is a deferral this plan records.

## Reviewer-adversarial Round 1 NITs applied (Layer-1 materialisation)

Round 1 verdict: **APPROVE-WITH-NITS**; 0 unresolved blockers; 5 NITs applied inline.
Full critique at `planning/current_plan.critique.md`.

| # | Severity | Concern | Fix applied in plan body |
|---|---|---|---|
| **N-A** | NIT | Explicit out-of-scope list absent from §Scope | §Scope now includes "Out of scope (V3 design surface — declared here, enforced by Layer-2 falsifiers):" bulleted list with 10 explicit exclusions: concrete temporal window sizes, decay half-lives, cold-start k-thresholds, tracker_events family inclusion, in-game temporal scope, any feature materialization, any artifact emission to `reports/artifacts/02_feature_engineering/03_temporal_features/**`, any status-chain YAML / research_log / ROADMAP edits, Phase 03 activation or baseline modeling, any empirical AoE2 transferability claim. |
| **N-B** | NIT | Layer-2 byte-unchanged negative-space contract absent from §File Manifest | §File Manifest adds "Files that MUST remain byte-unchanged in Layer-2 (binding negative-space contract):" list with 19 entries including V1 module, all status YAMLs, research_logs, artifacts, locked specs, docs/**, .claude/**, data/**, aoe2/**, thesis/**. |
| **N-C** | NIT | A-15 cross-game-portable vocabulary assumption needed explicit binding | §Assumptions & Unknowns A-15 adds verbatim binding: "The V3 validator module, mirrored test, and notebook scaffold use cross-game-portable vocabulary only (focal/opponent, history window, started_at, prior, target-game exclusion) and do NOT name SC2-specific terms (race, mineral, vespene, PlayerStats, tracker_events, toon_id, apm, sq) or AoE2-specific terms (civilization, civ, profile_id, leaderboard) where avoidable. No empirical AoE2 transferability claim is made; that determination is deferred to a future AoE2-specific Phase 02 step. This is verifiable by grep falsifiers H6 (cross-game-portable vocabulary) and H7 (Q8 syntactic-only guard) at Layer-2 execution." |
| **N-D** | NIT | A-9 PHASE_STATUS assumption needed explicit scope (not just mention) | §Assumptions & Unknowns A-9 now reads: "Phase 02 stays `in_progress`; Phase 03 stays `not_started`. No PHASE_STATUS row added or modified by the Layer-2 V3 scaffold execution PR. Phase 02 closure (and Phase 03 readiness) require future U2.B-style closure PR(s) downstream of adjudication + materialization rungs." |
| **N-E** | NIT | V3 module docstring framing (schema-level complement to CROSS-02-01 value-level) absent | §Execution Steps T02 now requires V3 module docstring to include VERBATIM: "V3 is a schema-level design-time gate enforcing strict-`<` temporal discipline via history-naming convention, temporal-anchor presence, and cite-string provenance. Value-level leakage (sophisticated semantic leaks not detectable from schema metadata alone) is gated separately by post-materialization audits per CROSS-02-01-v1.0.1. V3 and CROSS-02-01 are complementary, not redundant. V3 catches the common contributor failure modes (forbidden column naming, missing temporal anchor, missing cite-strings); CROSS-02-01 catches sophisticated semantic leaks at the value layer." §Literature Context also includes this framing. |
