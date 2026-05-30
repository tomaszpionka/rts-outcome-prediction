---
title: "SC2EGSet Step 02_03_01 SCAFFOLD + one validation module (Layer-1 planning PR; supersedes held adjudication-direct attempt)"
category: A
branch: feat/sc2egset-02-03-01-scaffold-plan
base_ref: master
base_sha: 6716aa1745b29cae50ed1323e3c2853987a47ca7
predecessor_pr: 274
predecessor_pr_merge_sha: 6716aa1745b29cae50ed1323e3c2853987a47ca7
dataset: sc2egset
phase: "02"
pipeline_section: "02_03 — Temporal Features, Windows, Decay, Cold Starts"
invariants_touched: [I3, I5, I6, I7, I8, I9, I10]
draft_pr_files:
  - planning/current_plan.md
  - planning/current_plan.critique.md
future_execution_files:
  - src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_feature_grid.py
  - tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_temporal_feature_grid.py
  - sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_scaffold.py
  - sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_scaffold.ipynb
  - pyproject.toml
  - CHANGELOG.md
  - planning/INDEX.md
future_execution_file_count: 7
target_version_bump: "3.87.0 -> 3.88.0"
critique_required: true
research_log_ref: null
date: 2026-05-30
supersedes: held-adjudication-direct-attempt
blocker_1_accepted: "scaffold-first is mandatory per merged ROADMAP continue_predicate at ROADMAP.md:3372-3384"
blocker_2_accepted: "Q8 cross-game portability reduced to syntactic-only; no SC2-specific names where avoidable; verifiable by grep"
---

## Scope

Author the Layer-1 planning artefact for the future Layer-2 **SCAFFOLD + one validation module PR** for Step `02_03_01` — Temporal Features, Windows, Decay, Cold Starts. This mirrors the PR #265 → PR #266 precedent exactly (PR #265 was the Layer-1 planning PR for the `02_02_01` scaffold + one validation module; PR #266 was the 7-file Layer-2 execution PR).

This plan supersedes a held adjudication-direct attempt. The reviewer-adversarial Round 1 issued a HOLD verdict with 2 BLOCKERs on the adjudication-direct attempt; both BLOCKERs were accepted by the user and resolved by shifting to scaffold-first per the merged ROADMAP `continue_predicate`:

- **BLOCKER 1 (accepted):** Scaffold-first is mandatory per the merged ROADMAP `continue_predicate` at `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md:3372-3378`. All three predecessor chains (`02_01_02` PR #233, `02_01_03` PR #241, `02_02_01` PR #266) used scaffold-then-adjudication. Adjudication-direct was REJECTED.
- **BLOCKER 2 (accepted):** Q8 cross-game portability reduced to syntactic-only (no SC2-specific names where avoidable; verifiable by grep). No empirical AoE2 transferability claim; deferred to future AoE2-specific Phase 02 step.

**Two-PR sequence on this branch.**

1. **THIS Layer-1 planning PR** writes only two files:
   - `planning/current_plan.md` (this document);
   - `planning/current_plan.critique.md` (reviewer-adversarial Round 1 output).
2. **FUTURE Layer-2 scaffold execution PR** performs the 7-file manifest declared in §File Manifest below (validator module + mirrored test + jupytext-paired notebook pair + pyproject 3.87.0 → 3.88.0 minor bump + CHANGELOG block + planning/INDEX.md update). This mirrors the PR #265 → PR #266 7-file Layer-2 template.

**Explicitly out of scope** for both PRs (this PR and the future Layer-2 PR):

- any feature materialisation, feature artifact, Parquet, audit JSON, audit MD;
- `STEP_STATUS.yaml` edits;
- `PIPELINE_SECTION_STATUS.yaml` edits;
- `PHASE_STATUS.yaml` edits (Phase 02 stays `in_progress`; Phase 03 stays `not_started`);
- root `reports/research_log.md` edits;
- dataset `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` edits;
- any `ROADMAP.md` edits (the stub merged in PR #274; ROADMAP is byte-stable in this PR);
- concrete temporal window sizes, decay half-lives, or cold-start k-thresholds (all deferred per the adjudication PR);
- any change to PR #263 / PR #264 / PR #265 / PR #266 / PR #268 / PR #270 / PR #272 / PR #274 artifacts;
- Step `02_03_02+`, Step `02_01_04`, Step `02_02_02+`, Phase 03, baseline modelling;
- any empirical AoE2 transferability claims (deferred to a future AoE2-specific Phase 02 step).

## Problem Statement

PR #274 (merged at master `6716aa1745b29cae50ed1323e3c2853987a47ca7`) inserted the `### Step 02_03_01` YAML block into `ROADMAP.md`, formally opening Pipeline Section `02_03`. The merged ROADMAP `continue_predicate` at lines 3372-3384 states that a scaffold PR may begin only after the ROADMAP stub merges. That precondition is now satisfied.

A prior adjudication-direct attempt was HELD (reviewer-adversarial Round 1, 2 BLOCKERs) because it skipped the mandatory scaffold rung. The ROADMAP `continue_predicate` is not a policy preference — it is the binding obligation declared by the merged ROADMAP, and it mandates the scaffold-then-adjudication sequence. Without the scaffold PR:

1. No validator module exists to gate the future adjudication PR against predecessor-artifact provenance;
2. No jupytext-paired notebook scaffold exists to receive the future empirical analysis;
3. The Layer-2 adjudication PR cannot demonstrate a "passing one-validation-module result" (the exact gating criterion stated in the `continue_predicate`);
4. The predecessor-artifact SHA-pin provenance record is never committed to the codebase as a typed, tested artifact.

This plan establishes the scaffold-first rung. The future adjudication PR for concrete window/decay/cold-start candidate selection proceeds only after this scaffold PR merges with a passing one-validation-module result.

## Literature Context

Per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical work" step 2 ("Notebook scaffold + one validation module"), the scaffold declares scope and delivers exactly one validator; no feature materialisation, no artifact generation.

**Binding ROADMAP obligation.** Scaffold-first is not a policy preference — it is the binding obligation declared by the merged ROADMAP at `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md:3372-3378`:

> A future PR may begin the 02_03_01 scaffold + one validation module
> (analogous to PR #241 for 02_01_03) only after this ROADMAP stub
> merges. A future PR may begin window/decay/cold-start candidate
> adjudication for 02_03 only after the scaffold PR merges with a
> passing one-validation-module result. A future materialization PR
> may proceed only after the adjudication PR(s) merge with concrete
> grid values justified by empirical evidence or cited precedent (no
> concrete grid values committed in this stub per OQ-1 deferral;
> H9 of the Layer-1 plan).

(Verbatim quote from `ROADMAP.md` lines 3372-3380. Full predicate runs to line 3384.)

**V1 shipped first; V3 committed as the immediately-next scaffold rung.** The one validation module shipped in the Layer-2 scaffold PR is V1 (SHA-pin predecessor artifact provenance anchor). V3 (strict-`<` temporal-discipline predicate) is committed as the IMMEDIATELY-NEXT scaffold rung (separate Layer-1 + Layer-2 PR pair), to land BEFORE any adjudication PR. Without this commitment, V1-first degrades to "V1 only forever" and the temporal-discipline invariant is never directly exercised at design time before concrete grid values are pinned. See §Open Questions Q1 for full rationale.

**PR #266 version bump precedent.** PR #266 (`feat/sc2egset-02-02-01-symmetry-difference-scaffold`) bumped `pyproject.toml` version `3.83.0 → 3.84.0` (minor; feat-class scaffold precedent), confirmed via `gh pr view 266 --json files --jq '.files[] | select(.path=="pyproject.toml")'`. The current version is `3.87.0` (post-PR #274 ROADMAP stub). The Layer-2 scaffold PR target bump is `3.87.0 → 3.88.0` (minor; same feat-class rule). This is the binding precedent per NIT-5 verification (see §Assumptions & Unknowns A-6).

**Per `.claude/rules/git-workflow.md`** "minor for feat/refactor/docs", a scaffold PR that opens a new validation rung is a feat-class minor bump. PR #266 (`3.83.0 → 3.84.0`) and PR #241 (`3.79.0 → 3.80.0`) confirmed this rule. Same rule applies here.

The three LOCKED cross-dataset specs relevant to Pipeline Section `02_03` are:

- **CROSS-02-00-v3.0.1** (LOCKED 2026-04-26; `reports/specs/02_00_feature_input_contract.md`): the cross-dataset feature input contract governing all Phase 02 steps.
- **CROSS-02-02-v1.0.1** (LOCKED 2026-05-06; `reports/specs/02_02_feature_engineering_plan.md`): the cross-dataset feature engineering plan listing temporal / window / decay / cold-start families.
- **CROSS-02-03-v1.0.1** (LOCKED 2026-05-06; `reports/specs/02_03_temporal_feature_audit_protocol.md`): the cross-dataset design-time temporal feature audit protocol; binds `[sc2egset, aoestats, aoe2companion]` for audit dimensions D1–D15.

The four parent artifact merge SHAs verified in STEP 1 are: PR #236 `39298c0afd3a23bfbd4603415314af784a672952`, PR #259 `5a62fc768a099eb73e449db081fdbac70a68a98e`, PR #255 `52f9c1082b200019d080cce74e60567452020e18`, PR #270 `eddd048992ce9aa4f444299ea342d9fdf7e2392b`. These are referenced in A-5 and must be re-verified by Layer-2 T01 before construction.

**Q8 cross-game portability.** The validator module is scoped to predecessor artifact provenance only (V1). Cross-game portability claims are restricted to syntactic-only observations: where the validator module uses candidate-agnostic vocabulary (e.g., focal/opponent, history window, decay, cold-start) rather than SC2-specific names, the design pattern is portable to a future AoE2-specific Phase 02 step. No empirical AoE2 transferability claim is made; that determination is deferred to a future AoE2-specific Phase 02 step. This is verifiable by grep falsifier F-Q8-syntactic (see §Gate Condition).

## Assumptions & Unknowns

**A-1. Predecessor ROADMAP stub merge SHA.** PR #274 (ROADMAP-only stub for Step 02_03_01) merged at master `6716aa1745b29cae50ed1323e3c2853987a47ca7`. Layer-2 T01 must verify `git rev-parse master` matches this SHA before construction.

**A-2. ROADMAP byte-stability.** The `ROADMAP.md` file is byte-stable in both the Layer-1 PR (this PR) and the Layer-2 scaffold PR. The ROADMAP was modified by PR #274; no further ROADMAP edits are permitted in the scaffold PR.

**A-3. pyproject version baseline.** `pyproject.toml` declares `version = "3.87.0"` (post-PR #274). Layer-2 target bump: `3.87.0 → 3.88.0` (minor per `.claude/rules/git-workflow.md` feat-class rule; mirrors PR #266 `3.83.0 → 3.84.0`).

**A-4. Validator module scope (V1 — predecessor artifact provenance).** The one validation module shipped in the Layer-2 scaffold PR audits predecessor artifact provenance only:

- SHA256 pins for all four predecessor Parquets/CSVs (PR #236, PR #259, PR #255, PR #270 merge SHAs).
- Identity column presence and dtype validation.
- Row count and column count plausibility checks.
- No temporal feature logic; no window computation; no decay half-life; no cold-start k-threshold.
- No tracker-derived feature in pre_game or history_enriched_pre_game prediction settings (Invariant I3 + Amendment 2 of PR #208).
- The module does NOT open the input Parquets for value reads; it validates provenance metadata only.

**A-5. Parent artifact merge SHAs (verified by executor in STEP 1 before authoring).** The four parent artifact merges that gate `02_03_01` readiness have been verified against `gh pr view <N> --json mergeCommit --jq .mergeCommit.oid`:

- PR #236 (`02_01_02` materialisation): `39298c0afd3a23bfbd4603415314af784a672952`
- PR #259 (`02_01_03` materialisation): `5a62fc768a099eb73e449db081fdbac70a68a98e`
- PR #255 (`02_01_99` omit-closure): `52f9c1082b200019d080cce74e60567452020e18`
- PR #270 (`02_02_01` materialisation): `eddd048992ce9aa4f444299ea342d9fdf7e2392b`

Layer-2 T01 must re-verify these SHAs before construction. If any SHA differs from the value above, halt and report.

**A-6. PR #266 version bump verified (NIT-5).** `gh pr view 266 --json files --jq '.files[] | select(.path=="pyproject.toml")'` confirms PR #266 modified `pyproject.toml` with +1/-1 (version bump). The PR #266 body confirms version `3.83.0 → 3.84.0` minor. The current version `3.87.0` (post-PR #274) makes the Layer-2 target `3.87.0 → 3.88.0` minor. This precedent is confirmed and locked.

**A-7. PIPELINE_SECTION_STATUS NOT touched.** No `02_03` row added by the Layer-2 scaffold PR. The first-step-closure rule applies: the section row lands when the FIRST step under that section closes (after materialisation + leakage audit + U2.B closure PR).

**A-8. STEP_STATUS NOT touched.** No `02_03_01` row added by the scaffold PR. The `02_03_01` row is added only when the step closes (after materialisation + leakage audit + U2.B closure PR).

**A-9. PHASE_STATUS.yaml NOT touched.** Phase 02 stays `in_progress`; Phase 03 stays `not_started`.

**A-10. planning/INDEX.md edits.** Two coupled edits:

1. **Active line rewrite.** Replace the current Active line (describing the now-merged Layer-2 stub PR #274) with the new Active line for the Layer-2 scaffold PR on `feat/sc2egset-02-03-01-scaffold-plan`. Required content: scaffold scope; "no ROADMAP / status YAML / research_log / artifact / Phase 03"; version bump `3.87.0 → 3.88.0`; future PR number placeholder `PR #<TBD>`.
2. **Archive PR #274.** Insert a new row in the archive table for PR #274 (Layer-2 ROADMAP-only stub for `02_03_01`; merge SHA `6716aa17`; date 2026-05-30; Category A).

**A-11. CHANGELOG block.** New `## [3.88.0] — <date> (PR #<TBD>: feat/sc2egset-02-03-01-scaffold-plan)` block inserted above the existing `## [3.87.0]` block. Block must contain `### Added` bullet for the scaffold + one validation module and `### Notes` bullets (`**No feature materialization.**`, `**No STEP_STATUS row.**`, `**No PIPELINE_SECTION_STATUS row.**`, `**No PHASE_STATUS mutation.**`, `**No research_log entry.**`, `**No ROADMAP edit.**`, `**No Phase 03.**`, `**No baseline modeling.**`, `**No concrete window sizes, decay half-lives, or cold-start k-thresholds.**`).

**A-12. Branch slug.** `feat/sc2egset-02-03-01-scaffold-plan` (this Layer-1 planning PR branch). The future Layer-2 scaffold PR may land on the same branch or a new branch — to be determined at Layer-2 planning time, mirroring the PR #265 → PR #266 precedent.

**A-13. No coverage gate impact.** Pre-commit hooks (`ruff` + `mypy`) run on `.py` file changes. The Layer-2 scaffold PR adds `.py` files; pytest coverage must be ≥ 35 tests and ≥ 95% branch coverage on the validator module (per PR #266 precedent: 62 tests, 95.28% branch coverage). The Layer-1 planning PR (this PR) touches zero `.py` files; no pytest run required.

**A-14. tracker_events_feature_eligibility.csv byte-stability.** The file at `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv` is byte-stable between Layer-1 merge and Layer-2 merge. If the file mutates between those commits, the Layer-2 PR halts before push. This file constrains which tracker-derived families may enter Pipeline Section `02_03` feature engineering (per `.claude/scientific-invariants.md` tracker-event discipline).

**A-15. Cross-game portable vocabulary.** The validator module and notebook scaffold use cross-game-portable vocabulary only (history windows, decay half-lives, cold-start thresholds, focal/opponent symmetry) and do NOT name SC2-specific terms where avoidable. AoE2-specific terms are fully absent. This is a binding requirement per Invariant I8 cross-game comparability, verifiable by grep falsifier F-candidate-agnostic (see §Gate Condition).

**Unknowns** (resolved at Layer-2 T01, not at Layer-1):

- **U-1.** The exact date of the Layer-2 scaffold PR merge (enters CHANGELOG date header and planning/INDEX archive row).
- **U-2.** Whether the Layer-2 PR lands on the same branch as Layer-1 or a new branch. To be determined at Layer-2 planning time.
- **U-3.** Exact prose for the notebook scaffold's hypothesis + falsifier declaration cells. Bound by CROSS-02-03-v1.0.1 §1.2 "out of scope" list; exact prose drafted at Layer-2 T01.

## Execution Steps

The future Layer-2 PR executes the following tasks based off `master@6716aa1745b29cae50ed1323e3c2853987a47ca7`. Each task is a delegated executor step.

**T01 — Verify base state (Sonnet executor).**

- Verify `git rev-parse master == 6716aa1745b29cae50ed1323e3c2853987a47ca7`.
- Verify `pyproject.toml` `version = "3.87.0"`.
- Verify STEP_STATUS has `02_02_01: complete` row.
- Verify PIPELINE_SECTION_STATUS has `02_02: complete` row.
- Verify PHASE_STATUS Phase 02 `in_progress` / Phase 03 `not_started`.
- Verify ROADMAP.md has `02_03_01` block (inserted by PR #274) and the `continue_predicate` text at lines 3372-3384.
- Verify `reports/artifacts/02_02_01/leakage_audit_sc2egset.json` exists with `verdict=PASS`.
- Verify the four parent SHAs from A-5 (re-run `gh pr view` and compare to pinned values).
- Verify `tracker_events_feature_eligibility.csv` exists at canonical path.
- Verify no existing `validate_temporal_feature_grid.py` or `test_validate_temporal_feature_grid.py` (scaffold creates these fresh).

Stop condition: any precondition fails → HALT, escalate to user.

Allowed files: NONE for write — Read-only verification only.

Forbidden files: ALL.

Required validation report: short summary echoing the 10 verifications.

**T02 — Create validator module (Sonnet executor; module docstring per NIT-3 Option B).**

Allowed files:
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_feature_grid.py`.

Forbidden files: ALL others.

Create the V1 predecessor artifact provenance validator. Module must:

- Include module docstring declaring verbatim: "This validator audits predecessor artifact provenance only (V1). It does NOT validate any temporal feature grid. Future temporal-discipline checks (V3) must land in a separate validator module under a separate scaffold rung."
- Implement SHA256 pin checks for all four predecessor Parquets/CSVs (PR #236, PR #259, PR #255, PR #270 merge SHAs as declared in A-5).
- Validate identity column presence and dtype.
- Validate row count and column count plausibility.
- Use cross-game-portable vocabulary in all function signatures and docstrings (focal/opponent, history window, cold-start — not SC2-specific names where avoidable).
- Accept no concrete window sizes, decay half-lives, or cold-start k-thresholds as parameters (V1 scope is provenance-only).
- Return a typed result object (dataclass or NamedTuple) with `passed`, `halting_falsifier`, `materialized_output_paths`, `artifact_directory_absence_ok` fields (per PR #266 validator precedent).

Stop condition: any file outside allowed list touched; module defines concrete grid values; module uses forbidden vocabulary → HALT.

Required validation report: `git diff --stat` shows only the new validator file; `grep -n 'temporal feature grid' src/.../validate_temporal_feature_grid.py` returns the module docstring declaration.

**T03 — Create mirrored test module (Sonnet executor).**

Allowed files:
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_temporal_feature_grid.py`.

Forbidden files: ALL others.

Create the mirrored test module. Tests must:

- Cover ≥ 35 tests with ≥ 95% branch coverage on `validate_temporal_feature_grid.py`.
- Include SHA-pin positive and negative controls.
- Include identity-column presence/absence tests.
- Include row-count plausibility boundary tests.
- Include a halt-priority test verifying first-failure-wins ordering.
- Include artifact-directory-absence tests asserting directory absence (not emptiness).
- Use `pytest.mark.parametrize` for boundary sweep tests.

Stop condition: any file outside allowed list touched; coverage below 95% → HALT.

Required validation report: `poetry run pytest tests/...test_validate_temporal_feature_grid.py -v --cov=rts_predict --cov-report=term-missing` passes with ≥ 35 tests, ≥ 95% branch coverage.

**T04 — Create jupytext-paired notebook scaffold (Sonnet executor).**

Allowed files:
- `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_scaffold.py`
- `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_scaffold.ipynb`

Forbidden files: ALL others.

Create the jupytext `py:percent` scaffold notebook. Notebook must:

- Follow sandbox/README.md hard rules: no inline definitions, 50-line cell cap, read-only DuckDB, jupytext percent-format.
- Declare hypothesis + falsifier + sanity-check up front in Markdown cells.
- Invoke the V1 validator (T02) and assert `passed=True` / `halting_falsifier=None` / `materialized_output_paths=()` / `artifact_directory_absence_ok=True`.
- Use `print()` for exploration output (not `logger`).
- NOT contain any `def`, `class`, or `lambda` in cells.
- NOT generate any artifact; no writes to `reports/artifacts/`.

Stop condition: notebook generates any artifact; notebook defines functions in cells; notebook uses forbidden vocabulary → HALT.

Required validation report: `jupytext --to notebook` produces a valid `.ipynb`; `nbconvert --execute` passes with no errors.

**T05 — Bump pyproject.toml (Sonnet executor).**

Allowed files:
- `pyproject.toml`.

Forbidden files: ALL others.

Edit: `version = "3.87.0"` → `version = "3.88.0"` (line 3; minor per feat-class rule).

Stop condition: any unintended file change → HALT.

Required validation report: `git diff pyproject.toml` shows only the version line change; `grep -RIn '__version__' src/` returns no matches.

**T06 — Add CHANGELOG.md [3.88.0] block (Sonnet executor).**

Allowed files:
- `CHANGELOG.md`.

Forbidden files: ALL others.

Insert `## [3.88.0] — <date> (PR #<TBD>: feat/sc2egset-02-03-01-scaffold-plan)` block between the existing `[Unreleased]` section and the existing `## [3.87.0]` block. Block content per A-11.

Stop condition: any unintended file change → HALT.

Required validation report: `git diff CHANGELOG.md` shows the new `[3.88.0]` block inserted above `[3.87.0]`; the `[Unreleased]` section and `[3.87.0]` block are byte-unchanged.

**T07 — Update planning/INDEX.md (Sonnet executor).**

Allowed files:
- `planning/INDEX.md`.

Forbidden files: ALL others.

Two coupled edits per A-10:

1. Replace the current Active line (describing PR #274) with the new Active line for the Layer-2 scaffold PR.
2. Insert a new archive row immediately under the table header for PR #274.

Stop condition: any unintended file change → HALT.

Required validation report: `git diff planning/INDEX.md` shows the two intended edits and nothing else; `grep -n "6716aa17" planning/INDEX.md` returns the new PR #274 archive row.

**T08 — Local checks and wrap-up (Sonnet executor).**

Allowed: read-only verification, `git status`, `git log --stat`, `git diff --stat master..HEAD`.

Required checks:
- `git diff --stat master..HEAD` shows exactly 7 files in the manifest.
- `grep -nE '^## ' planning/current_plan.md | wc -l` returns 8.
- No forbidden vocabulary in validator or test: grep falsifiers F-Q8-syntactic and F-candidate-agnostic from §Gate Condition both return zero matches in validator-design and test-scaffolding sections.
- Coverage: `poetry run pytest tests/.../test_validate_temporal_feature_grid.py --cov=rts_predict --cov-report=term-missing` → ≥ 35 tests, ≥ 95% branch coverage.
- No status YAML diff: `git diff --stat master..HEAD -- '**/STEP_STATUS.yaml' '**/PIPELINE_SECTION_STATUS.yaml' '**/PHASE_STATUS.yaml'` returns empty.
- No research_log diff: `git diff --stat master..HEAD -- '**/research_log.md'` returns empty.
- No ROADMAP diff: `git diff --stat master..HEAD -- 'src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md'` returns empty.

Stop condition: any check fails → HALT.

Required validation report: short summary echoing all checks; ready for commit/PR.

## File Manifest

This Layer-1 planning PR diff = exactly 2 files:
- `planning/current_plan.md` (this file)
- `planning/current_plan.critique.md` (reviewer-adversarial Round 1 output)

The future Layer-2 scaffold PR diff = exactly 7 files (mirrors PR #266 7-file Layer-2 template):

| File | Action | Notes |
|---|---|---|
| `src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_feature_grid.py` | Create | V1 predecessor artifact provenance validator. Module docstring per NIT-3 Option B: "This validator audits predecessor artifact provenance only (V1). It does NOT validate any temporal feature grid. Future temporal-discipline checks (V3) must land in a separate validator module under a separate scaffold rung." SHA256 pins for 4 predecessor artifacts. Typed result dataclass. Cross-game-portable vocabulary. No concrete window/decay/k-threshold values. |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_temporal_feature_grid.py` | Create | Mirrored test module. ≥ 35 tests, ≥ 95% branch coverage. Positive and negative SHA-pin controls. Identity-column presence/absence. Row-count boundary tests. Halt-priority ordering test. Directory-absence assertion. |
| `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_scaffold.py` | Create | Jupytext `py:percent` scaffold. Hypothesis + falsifier declaration cells. V1 validator invocation. No artifact generation. No function/class/lambda definitions in cells. |
| `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_scaffold.ipynb` | Create | Paired `.ipynb`. Outputs cleared before commit. Executes end-to-end via nbconvert with no errors. |
| `pyproject.toml` | Update | Version `3.87.0 → 3.88.0` (minor; feat-class scaffold precedent; PR #266 `3.83.0 → 3.84.0` confirmed). |
| `CHANGELOG.md` | Update | Insert `## [3.88.0]` block between `[Unreleased]` and `[3.87.0]`. |
| `planning/INDEX.md` | Update | Active line rewrite + archive PR #274 row (merge SHA `6716aa17`). |

**Files that MUST remain byte-unchanged** in the future Layer-2 scaffold PR:

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
- `reports/research_log.md` (root)
- All files under `reports/artifacts/02_01_02/`, `reports/artifacts/02_01_03/`, `reports/artifacts/02_02_01/`, `reports/artifacts/02_feature_engineering/**`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv`
- All files under `docs/`, `.claude/`, `data/`, `src/rts_predict/games/aoe2/`, `thesis/`
- Any existing `src/rts_predict/games/sc2/datasets/sc2egset/*.py` source files (scaffold creates the new validator fresh; does not modify existing source files)

## Gate Condition

The Layer-1 planning PR (this PR) is acceptable for merge when all of the following hold:

**G1.** `git diff --name-only HEAD` (relative to master) shows EXACTLY:
- `planning/current_plan.md`
- `planning/current_plan.critique.md`

**G2.** 8 required H2 headings literal match: `grep -cE '^## (Scope|Execution Steps|File Manifest|Problem Statement|Assumptions & Unknowns|Literature Context|Gate Condition|Open Questions)$' planning/current_plan.md` must equal 8.

**G3.** NIT-1 verbatim continue_predicate citation: `grep -F 'only after this ROADMAP stub' planning/current_plan.md` returns ≥ 1 match.

**G4.** NIT-2 V3-next commitment: `grep -F 'V3' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'next scaffold rung' planning/current_plan.md` returns ≥ 1 match.

**G5.** NIT-3 docstring constraint documented: `grep -F 'module docstring' planning/current_plan.md` returns ≥ 1 match.

**G6.** NIT-4 grep falsifiers documented: `grep -F 'F-Q8-syntactic' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'F-candidate-agnostic' planning/current_plan.md` returns ≥ 1 match.

**G7.** NIT-5 PR #266 version verification: `grep -F 'PR #266' planning/current_plan.md` returns ≥ 1 match.

**G8.** NIT-6 Round 2 re-gate trigger: if the materialized `planning/current_plan.md` fails any of the F-Q8-syntactic / F-candidate-agnostic grep falsifiers (NIT-4) or the 8-section literal-match check (`grep -cE '^## (Scope|Execution Steps|File Manifest|Problem Statement|Assumptions & Unknowns|Literature Context|Gate Condition|Open Questions)$' planning/current_plan.md` must = 8), the Layer-1 PR must escalate to reviewer-adversarial Round 2 on the materialized text. 3-round cap per `feedback_adversarial_cap_execution.md`. `grep -F 'Round 2' planning/current_plan.md` must return ≥ 1 match.

**Falsifier F-Q8-syntactic (NIT-4):** `grep -niE 'aoe2|civilization|aoestats|aoe2companion' planning/current_plan.md` — every match MUST be bounded as a forbidden-term constraint, a deferred-to-future-AoE2-specific context, a locked-spec citation, or a grep-falsifier definition; no unbounded transferability claim.

**Falsifier F-candidate-agnostic (NIT-4):** `grep -niE '\b(7|14|30|90|180)d\b|\b(7|10|14|30)_games?\b|half_life|k_threshold|tracker_events|PlayerStats|race|mineral|vespene' planning/current_plan.md` — zero matches in validator-design or test-scaffolding sections. Matches are permitted only in: (a) the §Gate Condition halt-clause list, (b) grep-falsifier definitions, (c) cross-spec citation blocks that name those terms as forbidden vocabulary.

**Layer-2 gate predicates** (applied by reviewer-adversarial before Layer-2 merge):

**LG1.** `git diff --stat master..HEAD` shows exactly 7 files matching the §File Manifest.

**LG2.** `poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_temporal_feature_grid.py --cov=rts_predict --cov-report=term-missing` passes with ≥ 35 tests, ≥ 95% branch coverage.

**LG3.** `grep -nE 'This validator audits predecessor artifact provenance only \(V1\)' src/.../validate_temporal_feature_grid.py` returns the module docstring declaration.

**LG4.** `grep -cE '^## \[3\.88\.0\]' CHANGELOG.md` returns 1.

**LG5.** `grep 'version' pyproject.toml | head -1` returns `version = "3.88.0"`.

**LG6.** `git diff --stat master..HEAD -- '**/STEP_STATUS.yaml' '**/PIPELINE_SECTION_STATUS.yaml' '**/PHASE_STATUS.yaml' '**/research_log.md' 'src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md' 'reports/research_log.md' 'src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/**'` returns empty.

**LG7.** F-candidate-agnostic falsifier on validator module: `grep -niE '\b(7|14|30|90|180)d\b|\b(7|10|14|30)_games?\b|half_life|k_threshold|tracker_events|PlayerStats|race|mineral|vespene' src/.../validate_temporal_feature_grid.py` — zero matches in non-docstring, non-comment code sections (these terms appear only in forbidden-vocabulary comments if at all).

**Halt conditions (Layer-2):**

**H1.** ROADMAP.md is modified in any way.

**H2.** Any of STEP_STATUS.yaml, PIPELINE_SECTION_STATUS.yaml, PHASE_STATUS.yaml, research_log.md are modified.

**H3.** The `tracker_events_feature_eligibility.csv` SHA at Layer-2 push differs from its SHA at Layer-1 merge.

**H4.** Any file outside the 7-file manifest appears in `git diff --stat master..HEAD`.

**H5.** The validator module contains concrete window size values (e.g., `7`, `14`, `30`, `90`, `180` as integer literals in function signatures or logic, not in comments/forbidden-vocabulary docstrings).

**H6.** Coverage on `validate_temporal_feature_grid.py` falls below 95% branch coverage or test count falls below 35.

**H7.** The notebook scaffold generates any artifact or defines functions in cells.

**H8.** F-candidate-agnostic falsifier fires in validator-design or test-scaffolding sections.

## Open Questions

**Q1 — V1 vs V3 sequence.** The one validation module shipped in the Layer-2 scaffold PR is V1 (SHA-pin predecessor artifact provenance anchor). V3 (strict-`<` temporal-discipline predicate — asserting that for each target game T, no feature uses data with `history_time >= T`) is the immediately-next scaffold rung committed by this plan.

**Commitment:** V1 is shipped first as foundational provenance anchor. V3 (strict-`<` temporal-discipline predicate) is committed as the IMMEDIATELY-NEXT scaffold rung (separate Layer-1 + Layer-2 PR pair), to land BEFORE any adjudication PR. Without this commitment, V1-first degrades to "V1 only forever" and the temporal-discipline invariant is never directly exercised at design time before concrete grid values are pinned.

The V3 scaffold rung will: (a) accept a sample of target game timestamps, (b) assert that no feature in the predecessor Parquets uses data with `history_time >= T` for those target games, (c) return a typed result with a per-game leakage report. V3 is NOT implemented in the Layer-2 scaffold PR; it is the contract for the PR immediately following this scaffold.

**Q2 — tracker_events families in 02_03.** The `tracker_events_feature_eligibility.csv` constrains which tracker families are eligible. The V1 validator is agnostic to specific tracker families; the adjudication PR resolves per-family eligibility. Plan default: scaffold scope references CROSS-02-03 and tracker eligibility CSV as gating artifacts; no tracker family included or excluded in the scaffold.

**Q3 — Cold-start threshold selection.** Concrete cold-start k-thresholds are NOT pinned by the scaffold. The V1 validator accepts no k-threshold parameters. Threshold selection is deferred to the adjudication PR. Plan default: scaffold comments note cold-start as a deferred parameter; no integer literals representing thresholds appear in module logic.

**Q4 — Window/decay parameter selection.** Concrete window sizes and decay half-lives are NOT pinned by the scaffold (per BLOCKER 2 resolution and OQ-1 deferral from the ROADMAP stub plan). The adjudication PR resolves these. Plan default: same as Q3 — deferred, zero concrete values in scaffold.

**Q5 — AoE2 portability.** Cross-game portability of the V1 validator design pattern is restricted to a syntactic-only observation: where the validator uses candidate-agnostic vocabulary (focal/opponent, history window, cold-start), the pattern is portable. No empirical AoE2 transferability claim. AoE2-specific transferability is deferred to a future AoE2-specific Phase 02 step. This is not a claim this plan makes — it is a deferral this plan records.

## Reviewer-adversarial Round 1 NITs applied (Layer-1 materialisation)

Round 1 verdict: **APPROVE-WITH-NITS**; 0 unresolved blockers; 6 NITs applied inline.
Full critique at `planning/current_plan.critique.md`.

| # | Severity | Concern | Fix applied in plan body |
|---|---|---|---|
| **N1** | NIT | continue_predicate citation absent | §Literature Context now quotes the merged ROADMAP `continue_predicate` VERBATIM from `ROADMAP.md:3372-3380` (full predicate runs to line 3384), framed as binding obligation not policy preference. |
| **N2** | NIT | V3-next commitment absent | §Literature Context and §Open Questions Q1 both explicitly commit: "V3 is committed as the IMMEDIATELY-NEXT scaffold rung (separate Layer-1 + Layer-2 PR pair), to land BEFORE any adjudication PR." |
| **N3** | NIT | Validator filename precision — Option B chosen | §File Manifest validator entry declares: module docstring verbatim "This validator audits predecessor artifact provenance only (V1). It does NOT validate any temporal feature grid. Future temporal-discipline checks (V3) must land in a separate validator module under a separate scaffold rung." Option B (extensible + docstring constraint) chosen over Option A (rename to validate_predecessor_artifact_provenance.py) because it allows V3 to land as a separate module under a clearly-scoped pattern. |
| **N4** | NIT | Q8 grep falsifiers absent from §Gate Condition | §Gate Condition adds Falsifier F-Q8-syntactic and Falsifier F-candidate-agnostic with full grep patterns. Layer-2 halt condition H8 added. |
| **N5** | NIT | PR #266 version bump precedent not cited | §Literature Context cites PR #266 `3.83.0 → 3.84.0` minor verified via `gh pr view 266`; §Assumptions & Unknowns A-6 records the verification. Layer-2 target locked to `3.87.0 → 3.88.0` minor. |
| **N6** | NIT | Round 2 re-gate trigger absent | §Gate Condition G8 adds explicit Round 2 escalation clause: if F-Q8-syntactic / F-candidate-agnostic grep falsifiers fail or 8-section check fails, escalate to reviewer-adversarial Round 2. 3-round cap per `feedback_adversarial_cap_execution.md`. |
