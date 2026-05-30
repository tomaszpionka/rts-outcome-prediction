---
title: "SC2EGSet Step 02_03_01 ROADMAP-only stub (Layer-1 planning PR; opens Pipeline Section 02_03 Temporal Features)"
category: A
branch: feat/sc2egset-02-03-01-roadmap-stub
base_ref: master
base_sha: cf60d2ab13aff428893b6ff45734110fb7f89348
predecessor_pr: 272
predecessor_pr_merge_sha: cf60d2ab13aff428893b6ff45734110fb7f89348
dataset: sc2egset
phase: "02"
pipeline_section: "02_03 — Temporal Features, Windows, Decay, Cold Starts"
invariants_touched: [I3, I5, I6, I7, I8, I9, I10]
draft_pr_files:
  - planning/current_plan.md
  - planning/current_plan.critique.md
future_execution_files:
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
  - pyproject.toml
  - CHANGELOG.md
  - planning/INDEX.md
future_execution_file_count: 4
target_version_bump: "3.86.1 -> 3.87.0"
critique_required: true
research_log_ref: null
date: 2026-05-30
---

## Scope

Author the Layer-1 planning artefact for the future Layer-2 **ROADMAP-only stub PR** that opens Pipeline Section `02_03` — Temporal Features, Windows, Decay, Cold Starts — by inserting a new `### Step 02_03_01` YAML block into `ROADMAP.md`. This mirrors the PR #263 → PR #264 section-opening precedent exactly (PR #263 was the Layer-1 planning PR for the `02_02_01` ROADMAP-only stub that opened Pipeline Section `02_02`; PR #264 was the 4-file Layer-2 execution PR).

The future Layer-2 ROADMAP YAML block MUST use candidate-agnostic language for `outputs.report` and `gate.continue_predicate` (e.g., "audit report listing candidate window-and-decay grid options for downstream adjudication PR"), mirroring the §02_01_99 stub-as-question precedent (ROADMAP.md:2622+). Concrete grid values (window sizes, decay half-lives, cold-start k-thresholds) are deferred to a successor adjudication PR (analogous to PR #234 / PR #242).

The Layer-2 ROADMAP-stub execution PR will land on the SAME branch `feat/sc2egset-02-03-01-roadmap-stub` (no new branch creation), mirroring the PR #263 → PR #264 same-branch precedent.

**Two-PR sequence on branch `feat/sc2egset-02-03-01-roadmap-stub`.**

1. **THIS Layer-1 planning PR** writes only two files:
   - `planning/current_plan.md` (this document);
   - `planning/current_plan.critique.md` (reviewer-adversarial output).
2. **FUTURE Layer-2 ROADMAP-stub execution PR on the same branch** performs the 4-file manifest below (ROADMAP.md insertion + pyproject 3.86.1 → 3.87.0 minor bump + CHANGELOG block + planning/INDEX.md update).

**Explicitly out of scope** for both PRs (this PR and the future Layer-2 PR):

- any source / test / notebook / sandbox / spec / cleaning-layer YAML / data / AoE2 / thesis / docs / `.claude` path edits;
- any feature materialization, feature artifact, Parquet, audit JSON, audit MD;
- `STEP_STATUS.yaml` edits (no `02_03_01` row — the step is opened by stub, not closed; closure is a separate U2.B PR after the step completes);
- `PIPELINE_SECTION_STATUS.yaml` edits (no `02_03` row — same first-step-closure rule as PR #230 / PR #264: the section row lands when the FIRST step under that section closes, not when the section stub opens);
- `PHASE_STATUS.yaml` edits (Phase 02 stays `in_progress`; Phase 03 stays `not_started`);
- root `reports/research_log.md` edits;
- dataset `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` edits;
- any `02_01_02` / `02_01_03` / `02_02_01` artifact regeneration;
- Step `02_03_02+`, Step `02_01_04`, Step `02_02_02+`, Phase 03, baseline modelling;
- concrete temporal window sizes, decay half-lives, or cold-start k-thresholds (all deferred per OQ-1 / A-4);
- any change to PR #263 / PR #264 / PR #265 / PR #266 / PR #268 / PR #270 / PR #272 artifacts.

## Problem Statement

PR #272 (merged at master `cf60d2ab13aff428893b6ff45734110fb7f89348`) formally closed Step `02_02_01` by adding the `02_02_01: complete` row to `STEP_STATUS.yaml` and the `02_02: complete` row to `PIPELINE_SECTION_STATUS.yaml`. The dataset ROADMAP currently ends with the `02_02_01` block (lines 2853–3131) followed immediately by the `## Phase 03 — Splitting & Baselines (placeholder)` heading (line 3135). The `continue_predicate` of the `02_02_01` stub (ROADMAP.md:3045–3062) states:

> "A future PR may begin the 02_02_01 scaffold + one validation module..."

That predicate has now been satisfied (PR #266 scaffold → PR #268 adjudication → PR #270 materialisation → PR #272 closure all merged). The ROADMAP contains no `02_03_01` block yet. Pipeline Section `02_03` (Temporal Features, Windows, Decay, Cold Starts; `docs/PHASES.md` line 116) is unrepresented in the dataset ROADMAP.

Without the Step `02_03_01` stub:

1. The ROADMAP's Phase 02 section lacks the Pipeline Section `02_03` entry, creating a gap between the materialised sections (`02_01`, `02_02`) and the Phase 03 placeholder;
2. `PIPELINE_SECTION_STATUS.yaml` cannot record `02_03: in_progress` or `02_03: complete` until a ROADMAP step under `02_03` exists;
3. No future scaffold / adjudication / materialisation PR for temporal features can open (the ROADMAP `continue_predicate` structure requires a stub before scaffold);
4. Three LOCKED cross-dataset specs that govern Pipeline Section `02_03` — `CROSS-02-00-v3.0.1` (LOCKED 2026-04-26), `CROSS-02-02-v1.0.1` (LOCKED 2026-05-06), and `CROSS-02-03-v1.0.1` (LOCKED 2026-05-06) — are referenced by no ROADMAP step for this dataset.

This PR is the exact analogue of PR #263 for Step `02_02_01` stub, now applied to Step `02_03_01`.

## Literature Context

Modest for a ROADMAP-only stub. Per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical work" step 1 ("ROADMAP stub only"), the stub declares scope and defers execution; no notebook, no feature generation, no artifact.

Per `docs/PHASES.md` line 116, the canonical name for Pipeline Section `02_03` is "Temporal Features, Windows, Decay, Cold Starts". This name is used verbatim in the ROADMAP block's `pipeline_section` field.

Per `.claude/rules/git-workflow.md` "minor for feat/refactor/docs", a ROADMAP stub that opens a new Pipeline Section is a feat-class minor bump. PR #264 (3.82.1 → 3.83.0) confirmed this rule: the `02_02_01` stub PR was feat-class minor because it represented a new Phase 02 section opening. The same rule applies here: 3.86.1 → 3.87.0.

The three LOCKED cross-dataset specs relevant to Pipeline Section `02_03` are:

- **CROSS-02-00-v3.0.1** (LOCKED 2026-04-26; `reports/specs/02_00_feature_input_contract.md`): the cross-dataset feature input contract governing all Phase 02 steps — data grain, temporal anchor, allowed cutoff rule, leakage-falsifier requirements.
- **CROSS-02-02-v1.0.1** (LOCKED 2026-05-06; `reports/specs/02_02_feature_engineering_plan.md`): the cross-dataset feature engineering plan that lists the Phase 02 feature families including temporal / window / decay / cold-start families.
- **CROSS-02-03-v1.0.1** (LOCKED 2026-05-06; `reports/specs/02_03_temporal_feature_audit_protocol.md`): the cross-dataset design-time temporal feature audit protocol; binds `[sc2egset, aoestats, aoe2companion]` for audit dimensions D1–D15. This spec is the primary gating authority for Pipeline Section `02_03`.

The stub ROADMAP block must reference all three specs (mirroring the `02_02_01` stub's `external_references` list which cites `02_03_temporal_feature_audit_protocol.md` as downstream). The stub does NOT execute any audit against these specs; it registers scope and gates forward movement.

The `02_01_99` stub (ROADMAP.md:2622+) established that a stub may declare scope-as-question and defer the answer to a successor PR — the stub's `outputs.report` field used candidate-agnostic language, and concrete decisions were resolved in a successor adjudication PR. This is the binding precedent for OQ-1 (temporal window-and-decay grid deferral; see §Open Questions).

No new methodological claim is made by the stub PR; the binding science is deferred to the scaffold + adjudication + materialisation ladder.

## Assumptions & Unknowns

**A-1. Predecessor merge SHA.** PR #272 merged at master `cf60d2ab13aff428893b6ff45734110fb7f89348`. Layer-2 T01 must verify `git rev-parse master` matches this SHA before construction.

**A-2. pyproject version baseline.** `pyproject.toml` declares `version = "3.86.1"`. Layer-2 target bump: `3.86.1 → 3.87.0` (minor per `.claude/rules/git-workflow.md` feat-class rule; mirrors PR #264 `3.82.1 → 3.83.0`).

**A-3. ROADMAP insertion point.** The new `### Step 02_03_01` YAML block is inserted into `ROADMAP.md` between the existing `02_02_01` block closing line (```` ``` ```` at line 3131) and the `---` separator at line 3133 and the `## Phase 03 — Splitting & Baselines (placeholder)` heading (line 3135). Layer-2 T01 reads the file at construction time and resolves the exact line numbers; the insertion is immediately after the `---` separator that follows the `02_02_01` block.

**A-4. ROADMAP block shape (candidate-agnostic).** The inserted block follows the same YAML fenced-code structure as the `02_02_01` block (lines 2853–3131). Key fields:

- `step_number: "02_03_01"`
- `pipeline_section: "02_03 — Temporal Features, Windows, Decay, Cold Starts"` (verbatim per `docs/PHASES.md` line 116)
- `predecessors: ["02_02_01"]`
- `manual_reference: "02_FEATURE_ENGINEERING_MANUAL.md, Section 4"` (per `docs/PHASES.md` line 116 "§4")
- `outputs.report`: candidate-agnostic language (e.g., "audit report listing candidate window-and-decay grid options for downstream adjudication PR") — concrete window sizes, decay half-lives, and cold-start k-thresholds are NOT pinned in the stub (deferred per OQ-1 / §02_01_99 stub-as-question precedent)
- `gate.continue_predicate`: candidate-agnostic (e.g., referencing audit completion and downstream adjudication PR readiness, not specific grid values)
- `halt_predicate`: bans Phase 03, Step `02_03_02+`, Step `02_01_04`, Step `02_02_02+`, baseline modelling, concrete grid pinning in stub
- `thesis_mapping`: Chapter 4 §4.5 Feature engineering plan
- `research_log_entry`: NOT REQUIRED FOR ROADMAP-STUB PR per `.claude/rules/data-analysis-lineage.md` step 1

**A-5. Parent artifact merge SHAs (verified by executor in Step 1 before authoring).** The four parent artifact merges that gate `02_03_01` readiness have been verified against `gh pr view <N> --json mergeCommit --jq .mergeCommit.oid`:

- PR #236 (`02_01_02` materialisation): `39298c0afd3a23bfbd4603415314af784a672952`
- PR #259 (`02_01_03` materialisation): `5a62fc768a099eb73e449db081fdbac70a68a98e`
- PR #255 (`02_01_99` omit-closure): `52f9c1082b200019d080cce74e60567452020e18`
- PR #270 (`02_02_01` materialisation): `eddd048992ce9aa4f444299ea342d9fdf7e2392b`

Layer-2 T01 must re-verify these SHAs before construction. If any SHA differs from the value above, halt and report.

**A-6. PIPELINE_SECTION_STATUS NOT touched.** No `02_03` row is added by the Layer-2 stub PR. The first-step-closure rule (PR #230 precedent: section row lands when the FIRST step under that section closes, not when the section opens) applies equally here. PR #264 (the `02_02_01` stub execution PR) did NOT add a `02_02` row to `PIPELINE_SECTION_STATUS.yaml` — that row was added by PR #272 (the formal closure PR). The same deferral applies: the `02_03` row lands in the future formal closure PR after `02_03_01` materialises and passes the leakage audit.

**A-7. STEP_STATUS NOT touched.** No `02_03_01` row is added by the stub PR. The `02_03_01` row is added only when the step closes (after materialisation + leakage audit + U2.B closure PR), per PR #264 precedent.

**A-8. PHASE_STATUS.yaml NOT touched.** Phase 02 stays `in_progress`; Phase 03 stays `not_started`. PR #264 left PHASE_STATUS byte-unchanged; same rule applies here.

**A-9. planning/INDEX.md edits.** Two coupled edits:

1. **Active line rewrite.** Replace the current Active line (describing the now-merged Layer-2 PR #272 formal closure) with the new Active line for `feat/sc2egset-02-03-01-roadmap-stub`. Required content: stub scope; "no source / test / notebook / artifact / leakage-audit / status-YAML / research_log / Phase 03"; version bump `3.86.1 → 3.87.0`; future PR number placeholder `PR #<TBD>`.
2. **Archive PR #272.** Insert a new row in the archive table for PR #272 (Layer-2 formal closure of `02_02_01`; merge SHA `cf60d2ab`; date 2026-05-30; Category C).

**A-10. CHANGELOG block.** New `## [3.87.0] — <date> (PR #<TBD>: feat/sc2egset-02-03-01-roadmap-stub)` block inserted above the existing `## [3.86.1]` block. Block must contain `### Added` bullet for the ROADMAP stub insertion and `### Notes` bullets (`**No feature materialization.**`, `**No STEP_STATUS row.**`, `**No PIPELINE_SECTION_STATUS row.**`, `**No PHASE_STATUS mutation.**`, `**No research_log entry.**`, `**No source / test / notebook / artifact change.**`, `**No Phase 03.**`, `**No baseline modeling.**`, `**No concrete window sizes, decay half-lives, or cold-start k-thresholds.**`).

**A-11. Branch slug.** `feat/sc2egset-02-03-01-roadmap-stub` mirrors PR #263's `feat/sc2egset-02-02-01-roadmap-stub` (verified via `gh pr view 263 --json headRefName` → `feat/sc2egset-02-02-01-roadmap-stub`).

**A-12. No coverage gate impact.** The Layer-2 stub PR touches zero `.py` files; `pytest --cov` is not re-run as part of the stub manifest (no diff in `src/` or `tests/`). Pre-commit hooks (`ruff` + `mypy`) are no-op on YAML/MD/TOML edits per `.claude/rules/git-workflow.md` PR-Creation-Flow rule line 4 ("Run checks (skip if no .py files in diff)"). Empirically verified: PR #264 (4 files, no `.py` changes) and PR #263 (2 files, no `.py` changes) both passed pre-commit gates without invoking ruff/mypy/pytest on the stub diff. Same expectation here for the 4-file stub manifest.

**A-13. No artifact byte change.** All Parquet, CSV, MD, audit JSON, audit MD files under `reports/artifacts/02_01_02/`, `reports/artifacts/02_01_03/`, `reports/artifacts/02_02_01/`, and `reports/artifacts/02_feature_engineering/**` remain byte-stable in both Layer-1 and Layer-2 PRs.

**A-14. tracker_events_feature_eligibility.csv byte-stability.** The file at `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv` is byte-stable between Layer-1 merge and Layer-2 merge; if the file mutates between those commits, the Layer-2 PR halts before push. This file constrains which tracker-derived families may enter Pipeline Section `02_03` feature engineering (per `.claude/scientific-invariants.md` tracker-event discipline).

**A-15. Cross-game portable vocabulary.** Step `02_03_01` `outputs.report` description uses cross-game-portable vocabulary only (history windows, decay half-lives, cold-start k-thresholds, focal/opponent symmetry) and does NOT name SC2-specific terms (tracker_events, PlayerStats, race, mineral, vespene) or AoE2-specific terms (civilization). This is a binding requirement per Invariant I8 cross-game comparability.

**Unknowns** (resolved at Layer-2 T01, not at Layer-1):

- **U-1.** The exact line at which the `02_03_01` block inserts. Layer-2 T01 reads the file at construction time and confirms the `02_02_01` block ends at line 3131 (currently ```` ``` ````) before inserting. The `---` separator at line 3133 and the `## Phase 03` heading at line 3135 shift down by the insertion length.
- **U-2.** The exact Layer-2 stub PR merge date (enters CHANGELOG date header and planning/INDEX archive row).
- **U-3.** Wording of the `### Step 02_03_01` block body — specifically the `scope`, `outputs.report`, `continue_predicate`, and `halt_predicate` prose. Bound by CROSS-02-03-v1.0.1 §1.2 "out of scope" list and the `02_01_99` stub-as-question precedent; exact prose drafted at Layer-2 T01.

## Execution Steps

The future Layer-2 PR executes the following tasks on branch `feat/sc2egset-02-03-01-roadmap-stub` based off `master@cf60d2ab13aff428893b6ff45734110fb7f89348`. Each task is a delegated executor step.

**T01 — Verify base state (Sonnet executor).**

- Verify `git rev-parse master == cf60d2ab13aff428893b6ff45734110fb7f89348`.
- Verify `pyproject.toml` `version = "3.86.1"`.
- Verify STEP_STATUS has `02_02_01: complete` row (line ~210).
- Verify PIPELINE_SECTION_STATUS has `02_02: complete` row.
- Verify PHASE_STATUS Phase 02 `in_progress` / Phase 03 `not_started`.
- Verify ROADMAP.md ends `02_22_01` block at line ~3131 followed by `---` and `## Phase 03` placeholder; no `02_03_01` block present.
- Verify `reports/artifacts/02_02_01/leakage_audit_sc2egset.json` exists with `verdict=PASS`, `features_audited_count=33`, `row_count=44418`.
- Verify the four parent SHAs from A-5 (re-run `gh pr view` and compare to pinned values).
- Verify `tracker_events_feature_eligibility.csv` exists at canonical path.

Stop condition: any precondition fails → HALT, escalate to user.

Allowed files: NONE for write — Read-only verification only.

Forbidden files: ALL.

Required validation report: short summary echoing the 9 verifications.

**T02 — Insert ROADMAP.md stub block (Sonnet executor; Opus prose drafting for block body).**

Allowed files:
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`.

Forbidden files: ALL others.

Edit: insert the `### Step 02_03_01` YAML block between the `---` separator that follows the `02_02_01` closing ```` ``` ```` and the `## Phase 03 — Splitting & Baselines (placeholder)` heading. The block must:

- Use candidate-agnostic language for `outputs.report` and `gate.continue_predicate` (per A-4 / OQ-1 / §02_01_99 precedent).
- Reference CROSS-02-00-v3.0.1, CROSS-02-02-v1.0.1, and CROSS-02-03-v1.0.1 in `external_references`.
- Ban Phase 03, concrete grid values, Step `02_03_02+`, Step `02_01_04`, Step `02_02_02+`, baseline modelling in `halt_predicate`.
- Include `research_log_entry: NOT REQUIRED FOR THIS ROADMAP-STUB PR per .claude/rules/data-analysis-lineage.md "Non-batching rule" sequence (step 1 — ROADMAP stub only — produces no research_log entry).`
- NOT include SC2-specific or AoE2-specific vocabulary in `outputs.report` description (per A-15).

Stop condition: any unintended file change; `outputs.report` or `gate.continue_predicate` names concrete grid values → HALT.

Required validation report: `git diff --stat` shows only `ROADMAP.md +N/-0`; `grep -n '02_03_01' ROADMAP.md` returns the new block's `step_number`; `grep -c 'tracker_events\|PlayerStats\|race\|mineral\|vespene\|civilization' ROADMAP.md` delta is zero (no new SC2/AoE2-specific terms added in the new block's `outputs.report` section).

**T03 — Bump pyproject.toml (Sonnet executor).**

Allowed files:
- `pyproject.toml`.

Forbidden files: ALL others.

Edit: `version = "3.86.1"` → `version = "3.87.0"` (line 3; minor per feat-class rule).

Stop condition: any unintended file change → HALT.

Required validation report: `git diff pyproject.toml` shows only `-version = "3.86.1"` / `+version = "3.87.0"` on line 3; `grep -RIn '__version__' src/` returns no matches.

**T04 — Add CHANGELOG.md [3.87.0] block (Sonnet executor).**

Allowed files:
- `CHANGELOG.md`.

Forbidden files: ALL others.

Edit: insert a new `## [3.87.0] — <date> (PR #<TBD>: feat/sc2egset-02-03-01-roadmap-stub)` block between the existing `[Unreleased]` section and the existing `## [3.86.1]` block. Block content per A-10.

Stop condition: any unintended file change → HALT.

Required validation report: `git diff CHANGELOG.md` shows the new `[3.87.0]` block inserted above `[3.86.1]`; the `[Unreleased]` section and `[3.86.1]` block are byte-unchanged.

**T05 — Update planning/INDEX.md (Sonnet executor).**

Allowed files:
- `planning/INDEX.md`.

Forbidden files: ALL others.

Two coupled edits per A-9:

1. Replace the current Active line (describing PR #272) with the new Active line for `feat/sc2egset-02-03-01-roadmap-stub`.
2. Insert a new archive row immediately under the table header for PR #272 (Layer-2 formal closure of `02_02_01`; merge SHA `cf60d2ab`; date 2026-05-30; Category C).

Stop condition: any unintended file change → HALT.

Required validation report: `git diff planning/INDEX.md` shows the two intended edits and nothing else; `grep -n "cf60d2ab" planning/INDEX.md` returns the new PR #272 archive row.

**T06 — Local checks and wrap-up (Sonnet executor).**

Allowed: read-only verification, `git status`, `git log --stat`, `git diff --stat master..HEAD`.

Required checks:
- `git diff --stat master..HEAD` shows exactly 4 files: `ROADMAP.md +N/-0`, `pyproject.toml +1/-1`, `CHANGELOG.md +~15/-0`, `planning/INDEX.md +~2/-1`.
- `grep -n '02_03_01' ROADMAP.md` returns the new block's `step_number` line.
- No `.py` file diff: `git diff --stat master..HEAD -- '*.py'` returns empty.
- No artifact path diff: `git diff --stat master..HEAD -- 'src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/**'` returns empty.
- No sandbox notebook diff: `git diff --stat master..HEAD -- 'sandbox/**'` returns empty.
- No `STEP_STATUS.yaml` diff: `git diff --stat master..HEAD -- '**/STEP_STATUS.yaml'` returns empty.
- No `PIPELINE_SECTION_STATUS.yaml` diff: `git diff --stat master..HEAD -- '**/PIPELINE_SECTION_STATUS.yaml'` returns empty.
- No `PHASE_STATUS.yaml` diff: `git diff --stat master..HEAD -- '**/PHASE_STATUS.yaml'` returns empty.
- No root `reports/research_log.md` diff: `git diff --stat master..HEAD -- 'reports/research_log.md'` returns empty.
- No dataset `research_log.md` diff: `git diff --stat master..HEAD -- 'src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md'` returns empty.

Stop condition: any check fails → HALT.

Required validation report: short summary echoing the 10 verifications; ready for commit/PR.

## File Manifest

This Layer-1 planning PR diff = exactly 2 files:
- `planning/current_plan.md` (this file)
- `planning/current_plan.critique.md` (reviewer-adversarial output)

The future Layer-2 stub PR diff = exactly 4 files:

| File | Action | Approx line delta |
|---|---|---|
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | Insert `### Step 02_03_01` YAML block between `02_02_01` close and Phase 03 placeholder (A-3, A-4) | +~280 / -0 |
| `pyproject.toml` | Bump version `3.86.1 → 3.87.0` (A-2) | +1 / -1 |
| `CHANGELOG.md` | Insert `[3.87.0]` block between `[Unreleased]` and `[3.86.1]` (A-10) | +~15 / -0 |
| `planning/INDEX.md` | Active line rewrite + archive PR #272 (A-9) | +~2 / -1 |

**Files that MUST remain byte-unchanged** in the future Layer-2 stub PR:

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
- `reports/research_log.md` (root)
- All files under `reports/artifacts/02_01_02/`, `reports/artifacts/02_01_03/`, `reports/artifacts/02_02_01/`, `reports/artifacts/02_feature_engineering/**`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv`
- All `src/rts_predict/games/sc2/datasets/sc2egset/*.py` source files
- All `tests/rts_predict/games/sc2/datasets/sc2egset/test_*` test files
- All `sandbox/sc2/sc2egset/**` notebook files
- All files under `docs/`, `.claude/`, `data/`, `src/rts_predict/games/aoe2/`, `thesis/`

## Gate Condition

The Layer-2 stub PR is acceptable for merge when:

**G1.** `git diff --stat master..HEAD` shows exactly 4 files matching the File Manifest above.

**G2.** `grep -n '"02_03_01"' ROADMAP.md` returns exactly one match (the new block's `step_number` field).

**G3.** `grep -nF 'pipeline_section: "02_03' ROADMAP.md` returns exactly one match in the new block.

**G4.** `grep -nE '^## \[3\.87\.0\]' CHANGELOG.md` returns exactly one match between `[Unreleased]` and `[3.86.1]`.

**G5.** `grep version pyproject.toml | head -1` returns `version = "3.87.0"`.

**G6.** `git diff --stat master..HEAD -- '**/STEP_STATUS.yaml' '**/PIPELINE_SECTION_STATUS.yaml' '**/PHASE_STATUS.yaml' '**/research_log.md' '*.py' 'sandbox/**' 'reports/research_log.md' 'src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/**'` returns empty.

**G7.** The ROADMAP block body's `outputs.report` and `gate.continue_predicate` fields use candidate-agnostic language — `grep -E 'window_size|decay_half_life|k_threshold|[0-9]+_games|[0-9]+d_window' ROADMAP.md | grep 02_03_01` returns empty (no concrete grid values in the stub block).

**G8.** Pre-commit hooks pass (ruff/mypy run only on `.py` changes; stub PR touches zero `.py` files, so these are no-op).

**Halt conditions (any of the following → halt before merge):**

**H1.** ROADMAP.md diff adds any line containing `STEP_STATUS`, `PIPELINE_SECTION_STATUS`, or `PHASE_STATUS` mutation instructions.

**H2.** ROADMAP.md block's `outputs.report` or `gate.continue_predicate` names a concrete window size (e.g., `7d`, `30d`, `90d`, `180d`) or a concrete decay half-life or concrete k-threshold.

**H3.** The `tracker_events_feature_eligibility.csv` SHA at Layer-2 push differs from its SHA at Layer-1 merge. (Verify: `git diff master -- 'src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv'` returns empty.)

**H4.** Any file outside the 4-file manifest appears in `git diff --stat master..HEAD`.

**H5.** `git diff --stat master..HEAD -- '*.py'` is non-empty.

**H6.** `git diff --stat master..HEAD -- 'sandbox/**'` is non-empty.

**H7.** `git diff --stat master..HEAD -- 'src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/**'` is non-empty.

**H8.** `git diff --stat master..HEAD -- 'reports/research_log.md'` is non-empty (root research_log unchanged).

**H9.** The Layer-2 ROADMAP YAML block must not encode concrete window sizes, decay half-lives, or cold-start k-thresholds. If it does, halt — OQ-1 deferral is illusory and the Layer-2 PR must be downgraded to a successor adjudication PR.

**H10.** If the Layer-2 YAML block's `outputs.report` description names any SC2-specific or AoE2-specific term (tracker_events, PlayerStats, race, mineral, vespene, civilization), halt — this violates Invariant I8 cross-game comparability.

## Open Questions

**OQ-1 — Temporal window-and-decay grid deferral.** Concrete window sizes (e.g., 7-game, 30-game, 90-day), decay half-lives, and cold-start k-thresholds for Pipeline Section `02_03` temporal features are NOT decided by the ROADMAP stub. The stub uses candidate-agnostic language (per A-4 / binding constraint in §Scope). Concrete grid values are resolved in a successor adjudication PR (analogous to PR #234 / PR #242 for `02_01_02`/`02_01_03`). **Plan default: defer all concrete grid choices to the adjudication PR; the Layer-2 stub block's `outputs.report` references "candidate window-and-decay grid options" only.**

**OQ-2 — tracker_events families in 02_03.** `CROSS-02-03-v1.0.1` §3 governs audit of temporal feature families including tracker-derived time-series families. The `tracker_events_feature_eligibility.csv` (path: `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv`) constrains which tracker families are eligible. The stub block's scope declaration must remain agnostic about which tracker families will be included; the adjudication PR will resolve per-family eligibility. **Plan default: stub scope references CROSS-02-03 and tracker eligibility CSV as gating artifacts; no tracker family is included or excluded in the stub.**

**OQ-3 — in_game_history_aggregate families in 02_03 vs 02_01_03.** The `in_game_history_aggregate` family was materialised in PR #259 (`02_01_03`). Whether `02_03` introduces new in-game temporal features beyond those in `02_01_03` depends on the adjudication PR. The stub block need not resolve this; it only declares that Pipeline Section `02_03` opens. **Plan default: stub block's scope uses "temporal features beyond the 02_01_03 in-game history aggregate tranche" language — no specific family resolution.**

**OQ-4 — CROSS-02-02 vs CROSS-02-03 boundary.** CROSS-02-02-v1.0.1 defines the feature engineering plan including temporal families; CROSS-02-03-v1.0.1 is the design-time audit protocol for those families. The stub must reference both without conflating them. **Plan default: stub block lists both specs in `external_references` with separate citations; no conflation.**

## Reviewer-adversarial Round 1 NITs applied (Layer-1 materialisation)

Round 1 verdict: **APPROVE-WITH-NITS**; 0 unresolved blockers; 6 NITs applied inline.
Full critique at `planning/current_plan.critique.md`.

| # | Severity | Concern | Fix applied in plan body |
|---|---|---|---|
| **N1** | NIT | SHA pinning absent in draft | §Assumptions & Unknowns A-5 now pins all four parent artifact merge SHAs verbatim: PR #236 `39298c0afd3a23bfbd4603415314af784a672952`, PR #259 `5a62fc768a099eb73e449db081fdbac70a68a98e`, PR #255 `52f9c1082b200019d080cce74e60567452020e18`, PR #270 `eddd048992ce9aa4f444299ea342d9fdf7e2392b`. |
| **N2** | NIT | Missing byte-stability assumption for tracker_events_feature_eligibility.csv | §Assumptions & Unknowns A-14 added: tracker_events_feature_eligibility.csv byte-stable between L1 merge and L2 merge; L2 halts if file mutates. |
| **N3** | NIT | OQ-1 deferral viability not enforced | §Scope adds explicit constraint that L2 YAML block uses candidate-agnostic language; §Gate Condition adds H9 banning concrete grid values in L2 stub. |
| **N4** | NIT | I8 transferability not asserted | §Assumptions & Unknowns A-15 added: `outputs.report` uses cross-game portable vocabulary only; §Gate Condition adds H10 banning SC2/AoE2-specific terms in `outputs.report`. |
| **N5** | NIT | Required 8 H2 headings must be literal match | All 8 H2 headings verified literal match per `grep -nE '^## '` (applied post-write as validation step). |
| **N6** | NIT | Same-branch L2 not explicit in plan | §Scope adds explicit sentence: "The Layer-2 ROADMAP-stub execution PR will land on the SAME branch `feat/sc2egset-02-03-01-roadmap-stub` (no new branch creation), mirroring the PR #263 → PR #264 same-branch precedent." |
