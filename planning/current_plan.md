---
title: "SC2EGSet Step 02_01_01 — V-1 strict + V-7 cold-start vocabulary/sentinel validation"
category: A
branch: phase02/sc2egset-feature-registry-v1-strict-and-v7-cold-start
date: 2026-05-08
branch_prefix: phase02/
branch_name: phase02/sc2egset-feature-registry-v1-strict-and-v7-cold-start
pr_title: "feat(phase02): SC2EGSet 02_01_01 V-1 strict + V-7 cold-start vocabulary/sentinel validation"
base_ref: "master @ 18d30a81"
base_commit: 18d30a8174d1553d49034d720518da027a6c4551
target_version: "3.49.0"
version_current: "3.48.0"
version_bump_type: "minor (Category A feat)"
created_date: 2026-05-08
dataset: sc2egset
phase: "02"
pipeline_section: "02_01"
step: "02_01_01"
step_name: "Feature-family registry skeleton (sc2egset)"
lineage_sequence_step: 2
prior_pr_ref: "#212"
invariants_touched: [I3, I7, I8]
reviewer_gate_plan: reviewer-deep
reviewer_gate_post_execution: reviewer-deep
reviewer_adversarial_required: false
critique_required: true
spec_bindings:
  - CROSS-02-00-v3.0.1
  - CROSS-02-01-v1.0.1
  - CROSS-02-02-v1.0.1
  - CROSS-02-03-v1.0.1
non_batching_lineage_position: "Sequence step 2 continuation — additional validation module under data-analysis-lineage.md §6 'Next validation module'. Skeleton (sequence step 2 first pass) was delivered by PR #212; artifact generation (sequence step 7) remains deferred."
---

# Plan: SC2EGSet Step 02_01_01 — V-1 strict (`feature_family_id` segment check) + V-7 cold-start vocabulary/sentinel validation

## Problem Statement

PR #212 delivered the SC2EGSet Step 02_01_01 feature-family registry
scaffold — a 26-row in-memory skeleton plus the V-1..V-6 validation
module. Reviewer-deep on PR #212 raised follow-up #1 (V-1 stricter
`feature_family_id` ↔ `prediction_setting` segment alignment) as a
non-blocker hardening item. The merged registry skeleton also commits
to a controlled cold-start vocabulary (`G-CS-1..G-CS-6` from
CROSS-02-02-v1.0.1 §9.1, plus a `"blocked"` sentinel for blocked rows)
that is currently asserted only narratively, not by code.

This PR addresses both gaps in one cohesive validation-module
extension. Without V-1 strict, a future feature-engineering author could
silently mislabel a row's `prediction_setting` against its
`feature_family_id` (e.g., write `sc2egset.pre_game.foo` for a row whose
`prediction_setting` is `history_enriched_pre_game`) and the registry
would accept it, allowing temporal-leakage discipline downstream to
reason against an inconsistent label. Without V-7, a numeric pseudocount
or magic threshold could leak into `cold_start_handling` (Invariant I7
violation) and the registry would not catch it. Both V-1 strict and V-7
are vocabulary/structural checks — they do NOT validate which G-CS gate
fits each family scientifically (deferred to a future audit).

## Goal

Extend `validate_registry_skeleton()` (delivered by PR #212 with V-1..V-6) by:

1. **V-1 strict refinement** — assert that every row's `feature_family_id`
   matches the form `sc2egset.<prediction_setting>.<family>` AND that the
   second dot-segment equals `row["prediction_setting"]` verbatim. PR #212's
   V-1 already asserts the `sc2egset.` prefix and uniqueness; this PR adds
   the second-segment / prediction_setting alignment check, including a
   minimum-segment-count guard (`len(parts) >= 3`).
2. **V-7 cold-start vocabulary + sentinel validation** — assert that
   `cold_start_handling` is the literal sentinel `"blocked"` for rows whose
   carve-out conjunction holds (`prediction_setting == "blocked_or_deferred"`
   AND `status == "blocked_until_additional_validation"`), and a controlled
   vocabulary token from `{G-CS-1..G-CS-6}` for every other row. For ALL
   rows (no exception), reject numeric tokens (Invariant I7).

V-7 does NOT validate whether each active family has the scientifically
optimal G-CS gate; it validates vocabulary/sentinel discipline only. The
choice of which G-CS gate fits each family is deferred to future validation
modules (e.g., D3 in the deferred-D-list from PR #212).

The merged 26-row skeleton from PR #212 (sandbox notebook + paired ipynb)
remains untouched in row content. Only narrative text in markdown cells is
corrected to align with the resolved V-7 conjunction semantics. No new
artifacts are produced; no STEP_STATUS / PHASE_STATUS / research_log /
manifest edits are performed.

## Scope

This PR delivers an additional validation module continuation per
`.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical
work" (sequence step 6 — "Next validation module"). It bundles:

- one or two new internal check helpers added to
  `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`
  (`_check_v1_strict_id_segment_alignment` augmenting V-1, and
  `_check_v7_cold_start_vocabulary`);
- the new check calls wired into `validate_registry_skeleton()`;
- new tests in
  `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`
  covering V-1 strict failure modes, V-7 vocabulary success, V-7 sentinel
  success, V-7 conjunction failure modes, V-7 numeric token failure, V-7
  unknown token failure;
- a markdown-cell narrative correction in the merged skeleton notebook
  (clarifying that active/candidate rows use `G-CS-1..G-CS-6` while
  `blocked_or_deferred` rows under the conjunction use the `"blocked"`
  sentinel);
- jupytext `.py`/`.ipynb` re-sync;
- pyproject.toml + CHANGELOG.md release commit (3.48.0 → 3.49.0).

## Non-goals

- No row-content edits to the 26-row skeleton (the literal SKELETON_*
  list[dict] expressions in cells 7–11 of the notebook are immutable in
  this PR). Verification (below) confirms all 26 rows already satisfy the
  resolved V-1 strict and V-7 conjunction semantics; no row patching is
  required.
- No new validation modules beyond V-1 strict refinement and V-7
  vocabulary/sentinel.
- No D2/D3/D6/D8/D9/D10/D11/D12/D15 audit-dimension validators (those
  remain in the deferred follow-up bucket from PR #212).
- No registry CSV / MD artifact under
  `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
- No edits to `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`,
  `PHASE_STATUS.yaml`, the per-dataset `research_log.md`, the cross-game
  `reports/research_log.md`, the ROADMAP, the locked `02_*` specs, or the
  notebook regeneration manifest. All deferred to a subsequent
  artifacts/log/status/manifest PR per
  `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical
  work" steps 7–9.
- No DuckDB I/O. No tracker-CSV row-content modification.
- No AoE2 work; no thesis chapter prose.
- Step 02_01_01 itself is NOT closed by this PR.
- Test-infra cleanup (`parents[6]` repo-root magic at
  `tests/.../test_validate_registry_skeleton.py:24`) is deferred to a
  hygiene PR unless a NEW test added by T02b touches that line.
- Defensive-branch coverage / `# pragma: no cover` for
  `validate_registry_skeleton.py` lines 243, 311, 317 is deferred to a
  hygiene PR unless T01 / T02 modifications happen to relocate or affect
  those lines.

## Literature Context

- **CROSS-02-00-v3.0.1** (`reports/specs/02_00_feature_input_contract.md`):
  binding input contract for Phase 02 feature engineering. Defines the
  pre-game / history / in-game / sanity-gate / blocked prediction-
  setting taxonomy that V-1 strict's second-segment alignment depends on.
- **CROSS-02-01-v1.0.1** (`reports/specs/02_01_leakage_audit_protocol.md`):
  defines the post-materialization leakage audit; not directly
  exercised by V-1 strict / V-7 (which are pre-materialization
  structural checks) but cited here for completeness.
- **CROSS-02-02-v1.0.1 §9.1** (`reports/specs/02_02_feature_engineering_plan.md`):
  defines the controlled cold-start gate vocabulary `{G-CS-1, G-CS-2,
  G-CS-3, G-CS-4, G-CS-5, G-CS-6}`. V-7 binds this vocabulary as the
  authoritative set for active/candidate rows.
- **CROSS-02-03-v1.0.1 §4 D11** (`reports/specs/02_03_temporal_feature_audit_protocol.md`):
  defines audit dimension D11 (cold-start handling). V-7 partially
  fulfills D11's vocabulary/sentinel check; the "which G-CS gate fits
  each family scientifically" question is deferred to a future
  validation module.
- **PR #212** (merged 2026-05-08 at master `18d30a81`): delivered the
  scaffold and V-1..V-6. Reviewer-deep on PR #212 filed follow-up #1
  (V-1 stricter id-segment alignment), follow-up #3 (defensive-branch
  coverage), follow-up #2 (test infra `parents[6]`), and follow-up #4
  (`planning/INDEX.md` allowed scope). This PR closes follow-up #1;
  the others are explicitly deferred to a hygiene PR per §Non-goals.
- **`.claude/scientific-invariants.md`**: I3 (no future leakage), I7
  (no magic numbers), I8 (cold-start gates documented). V-1 strict
  binds to I3 indirectly (a mislabeled row would allow leakage past
  the wrong cutoff); V-7 binds I7 directly (numeric tokens forbidden)
  and I8 indirectly (cold-start gate vocabulary enforced).
- **`.claude/rules/data-analysis-lineage.md`** §"Non-batching rule":
  defines the 9-step empirical sequence. This PR is sequence step 6
  ("Next validation module") — see §Non-batching rationale.

## Assumptions & Unknowns

**Assumptions** (declared explicit so the executor can halt if any
becomes false during T01–T08):

1. The merged 26-row SKELETON in
   `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
   already satisfies V-1 strict (every row's `feature_family_id` second
   dot-segment equals its `prediction_setting`). Verified live by the
   planner during plan authoring (0 violations).
2. The merged 26-row SKELETON already satisfies V-7 under the
   conjunction carve-out: 23 model-input rows carry `G-CS-{1..6}`; 3
   blocked rows satisfy BOTH `prediction_setting == "blocked_or_deferred"`
   AND `status == "blocked_until_additional_validation"` AND carry
   `cold_start_handling == "blocked"`; 0 rows carry numeric tokens.
   Verified live by the planner (0 violations).
3. The narrative target lines in the notebook .py (128, 258, 486, 495)
   are stable across `master @ 18d30a81` and the new branch's HEAD.
   Verified by the planner against the on-disk file.
4. The existing `valid_skeleton` test fixture has 7 rows; 3 of them
   carry `prediction_setting == "blocked_or_deferred"` and
   `status == "blocked_until_additional_validation"` but currently
   inherit `cold_start_handling == "G-CS-1"` from the `_row()` helper
   default. T02b Step 0 (mandatory) updates these 3 fixture rows to
   `"blocked"` so V-7 passes on the fixture (per F1 from reviewer-deep
   critique).
5. `float()` cannot parse `G-CS-N` tokens (the leading `G-` prevents
   numeric coercion). Confirmed empirically.
6. `pyproject.toml` line 3 reads `version = "3.48.0"` at branch HEAD;
   T08 mechanically bumps to `"3.49.0"`. Confirmed by the planner.
7. CHANGELOG.md `[Unreleased]` block is empty after PR #212's roll-up.
   Confirmed by the planner.

**Unknowns** (must NOT block T01; surfaced for executor awareness):

1. Whether `float()` behavior on `"NaN"` / `"inf"` differs across
   Python versions in the project's CI matrix. Mitigation: V-7's
   numeric check runs on Python 3.12 (project standard); `float("NaN")`
   and `float("inf")` both succeed → V-7 fires (these are I7
   violations). The plan's `except (ValueError, TypeError)` is correct.
2. Whether reviewer-deep at T09 (post-execution gate) raises any
   methodology BLOCKER beyond the 4 fixes already applied to this
   plan. If so, T09 routes to reviewer-adversarial per the
   data-analysis-lineage carve-out.

## Gate Condition

This PR is mergeable to master when all of the following are
simultaneously true (mirrored in §Acceptance criteria):

1. `git diff master..HEAD --name-only` lists EXACTLY 8 files: the 4
   scaffold/code files (validation module + tests + notebook .py +
   .ipynb) plus `pyproject.toml` + `CHANGELOG.md` plus the planning
   files (`planning/current_plan.md`, `planning/current_plan.critique.md`,
   `planning/INDEX.md`). No forbidden file appears.
2. The notebook's `validate_registry_skeleton()` call output cell
   contains the literal string `"validate_registry_skeleton: ALL PASS
   (V-1 through V-7)"`.
3. `pytest tests/ -v --cov` passes with overall coverage ≥ 95% and
   `validate_registry_skeleton.py` per-file coverage ≥ 95%; the two
   new helpers (`_check_v1_strict_id_segment_alignment`,
   `_check_v7_cold_start_vocabulary`) show 100% line coverage.
4. `ruff check`, `mypy`, `jupytext --check` all clean.
5. The 26 SKELETON rows in the notebook .py are byte-identical to
   master `18d30a81` (no row literal modified).
6. Reviewer-deep at T09 returns `PASS` or `PASS-WITH-NOTES`. A
   `BLOCKER` methodology verdict halts T09 and routes to
   reviewer-adversarial per `.claude/rules/data-analysis-lineage.md`
   line 24 carve-out.
7. `pyproject.toml` shows `version = "3.49.0"`; `CHANGELOG.md` has a
   `[3.49.0]` block dated 2026-05-08 with the actual PR number `N`
   substituted (no `PR #TBD` remaining).

## File Manifest

### Allowed (this PR may touch only these)

| File | Touch type | Commit |
|------|-----------|--------|
| `planning/current_plan.md` | rewrite (this plan) | docs(planning) — already on branch when execution starts |
| `planning/current_plan.critique.md` | rewrite (reviewer-deep critique authored before execution) | docs(planning) |
| `planning/INDEX.md` | append archive row + update active row | docs(planning) |
| `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py` | append constants (`COLD_START_GATE_VOCAB`, `BLOCKED_SENTINEL`); add `_check_v1_strict_id_segment_alignment` and `_check_v7_cold_start_vocabulary` private helpers; wire calls into `validate_registry_skeleton()` | feat (T07 scaffold/code commit) |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py` | append new tests for V-1 strict + V-7 | feat (T07 commit) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` | edit markdown text inside cells at lines 128, 258, 486 (commentary only — no SKELETON_* literal change) and re-sync; update print-banner line at 495 (V-6 → V-7) | feat (T07 commit) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb` | regenerated by jupytext --sync after .py edit; commit alongside paired .py | feat (T07 commit) |
| `pyproject.toml` | bump `version = "3.48.0"` → `version = "3.49.0"` | chore(release) (T08 commit) |
| `CHANGELOG.md` | roll `[Unreleased]` → `[3.49.0] — 2026-05-08 (PR #N: phase02/sc2egset-feature-registry-v1-strict-and-v7-cold-start)`; insert empty `[Unreleased]` block; populate `[3.49.0]` Added section with V-1 strict + V-7 bullets | chore(release) (T08 commit); PR-number substitution post-create |
| `.github/tmp/commit.txt` | scratch (created and removed within session) | not committed |
| `.github/tmp/pr.txt` | scratch (created, used by `gh pr create --body-file`, removed after PR is created) | not committed |

### Forbidden (executor must HALT if `git status` lists any of these)

| Forbidden path | Reason |
|----------------|--------|
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/**` | No artifacts in this PR (lineage step deferred). |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` | Step 02_01_01 not closed by this PR. |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` | Pipeline-section roll-up deferred. |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` | Phase 02 status roll-up deferred. |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` | Per-dataset research log entry deferred. |
| `reports/research_log.md` | Cross-game research log entry deferred. |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | ROADMAP update deferred. |
| `reports/specs/02_00_feature_input_contract.md` | Locked spec — read-only. |
| `reports/specs/02_01_leakage_audit_protocol.md` | Locked spec — read-only. |
| `reports/specs/02_02_feature_engineering_plan.md` | Locked spec — read-only. |
| `reports/specs/02_03_temporal_feature_audit_protocol.md` | Locked spec — read-only. |
| `thesis/**` | No thesis prose in this PR. |
| `thesis/pass2_evidence/notebook_regeneration_manifest.md` | Manifest update deferred. |
| `src/rts_predict/games/aoe2/**` | No AoE2 work. |
| `data/**`, `**/data/**` | No raw / staging / db edits. |
| `docs/**` | No taxonomy / spec / methodology edits. |
| `.claude/**` | No agent / rule / invariant edits. |
| Any literal SKELETON_PRE_GAME / SKELETON_HISTORY / SKELETON_IN_GAME_NOW / SKELETON_IN_GAME_CAVEAT / SKELETON_GATE_AND_BLOCKED row tuple in the notebook .py | Skeleton row content is locked from PR #212. |
| `tracker_events_feature_eligibility.csv` | Upstream evidence — must NOT be modified. |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` | Per-dataset invariants file — must NOT be modified by this PR (F3 from reviewer-deep critique). |
| `pyproject.toml`, `CHANGELOG.md` **during T01–T07** | These are §Allowed only at T08 (release commit). Executor must HALT if either appears in `git status` while T01–T07 are running, to prevent accidental staging in the T07 scaffold commit (F3 from reviewer-deep critique). |
| `planning/current_plan.md`, `planning/current_plan.critique.md` **during T07–T08** | These already exist on the branch from earlier docs(planning) commits and must NOT appear in the T07 (scaffold) or T08 (release) staged sets. Executor must HALT on `git diff --cached --name-only` listing either path during T07 or T08 (F3 from reviewer-deep critique). |

## Verification before finalizing this plan (executed read-only by the planner)

1. **V-1 strict semantic check (live).** Inline-evaluated all 26 rows of
   the merged SKELETON. For every row, `feature_family_id.split(".")` has
   ≥ 3 segments, segment 0 is `"sc2egset"`, and segment 1 equals
   `row["prediction_setting"]` verbatim. Violations: 0.

2. **V-7 conjunction semantic check (live).**
   - 23 rows where `prediction_setting != "blocked_or_deferred"` carry
     `cold_start_handling ∈ {G-CS-1..G-CS-6}`. None carry numeric tokens.
   - 3 rows where `prediction_setting == "blocked_or_deferred"`: all 3
     also carry `status == "blocked_until_additional_validation"` (i.e.,
     the conjunction holds for every blocked row). All 3 carry
     `cold_start_handling == "blocked"`.
   - Rows with the `prediction_setting` only (status mismatch): 0.
   - Rows with the `status` only (prediction_setting mismatch): 0.
   - Result: stricter V-7 conjunction is satisfied by the unmodified
     skeleton. No skeleton row content needs to change.

3. **Narrative target locations (live).** The merged notebook .py
   (`sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`)
   contains three locations that paraphrase cold-start vocabulary in a way
   that is incomplete (does not call out the `"blocked"` sentinel):
   - **line 128** (markdown cell — Lineage source list, inside the
     `## Hypothesis, falsifiers, sanity checks, and stop conditions`
     block): "gates G-CS-1..G-CS-6 — no magic numbers per Invariant I7".
   - **line 258** (code-cell prelude comment immediately above the `_COLS`
     definition): "Cold-start handling values use only the gate vocabulary
     G-CS-1..G-CS-6 (CROSS-02-02-v1.0.1 §9); no numeric pseudocount,
     threshold, smoothing strength, or imputation constant appears
     (Invariant I7)."
   - **line 486** (markdown cell — Validation module intro, "Checks NOT in
     scope" list): "cold-start gate vocabulary check (G-CS-1..G-CS-6)".
   - The "Checks NOT in scope" line at 486 must be retained but qualified
     — V-7 of THIS PR does check vocabulary/sentinel, so the bullet must
     be removed or rewritten to reflect that V-7 now covers
     vocabulary/sentinel and that what remains deferred is the
     family-by-family gate-fit assessment (per-row optimal G-CS choice).

   T03 below specifies the exact replacement text for each location.

## Execution Steps

Each task lists: ID, allowed files, forbidden files, exact operation,
task-specific stop condition, validation report shape, executor model
assignment.

### T01 — Add V-1 strict refinement: id-second-segment alignment check

**Allowed files:**
`src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`.

**Forbidden files:** all entries in §Files / Forbidden, plus the test
file (T02b covers tests), notebook (T03 covers narrative), pyproject.toml
and CHANGELOG.md (T08 covers release).

**Exact operation:**

1. Append after existing module-level constants (line ~107, just before
   `POST_OUTCOME_FORBIDDEN_TOKENS`):

   ```python
   # CROSS-02-02-v1.0.1 OQ1 + 2026-05-08 V-1 strict refinement.
   # feature_family_id format: sc2egset.<prediction_setting>.<family>
   # The second dot-segment must equal row["prediction_setting"] verbatim.
   FEATURE_FAMILY_ID_MIN_SEGMENTS: int = 3
   ```

2. Add private function (signature):

   ```python
   def _check_v1_strict_id_segment_alignment(
       skeleton: list[dict[str, Any]],
   ) -> None:
       """V-1 strict: feature_family_id second segment must equal prediction_setting."""
   ```

   Body asserts, for each row:
   - `len(parts) >= FEATURE_FAMILY_ID_MIN_SEGMENTS` where
     `parts = row["feature_family_id"].split(".")`. On failure raise
     `AssertionError` with message containing `"V-1 strict"` and the
     offending feature_family_id.
   - `parts[1] == row["prediction_setting"]`. On failure raise
     `AssertionError` with message containing `"V-1 strict"`, the
     `feature_family_id`, the actual second-segment value, and the
     expected prediction_setting value.

3. Add a call to `_check_v1_strict_id_segment_alignment(skeleton)` inside
   `validate_registry_skeleton()`, immediately after the existing
   `_check_v1_schema_integrity(skeleton)` call (so V-1 base assertions
   run first; V-1 strict refinement piggybacks).

**Task-specific stop condition:** halt if (a) any of the existing V-1
through V-6 helpers must be modified to land V-1 strict (none should), or
(b) the existing test suite for V-1 fails after this change in a way not
explained by the new strict assertion.

**Validation report shape:** post-edit show diff of
`validate_registry_skeleton.py`; confirm only the two additions
(constant + helper + call); confirm no other helper signatures changed.

**Executor model:** Sonnet (mechanical specification; no methodology
inference required beyond the literal segment-equality check).

### T02 — Add V-7 cold-start vocabulary + sentinel validation

**Allowed files:**
`src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`.

**Forbidden files:** all entries in §Files / Forbidden, plus the test
file (T02b covers tests).

**Exact operation:**

1. Append after the `FEATURE_FAMILY_ID_MIN_SEGMENTS` constant added in
   T01 (and before `POST_OUTCOME_FORBIDDEN_TOKENS`):

   ```python
   # CROSS-02-02-v1.0.1 §9.1 cold-start gate controlled vocabulary
   # (G-CS-1..G-CS-6). Active model-input rows MUST carry one of these
   # tokens. The literal "blocked" sentinel is reserved for the V-7
   # carve-out (see BLOCKED_SENTINEL).
   COLD_START_GATE_VOCAB: frozenset[str] = frozenset(
       {"G-CS-1", "G-CS-2", "G-CS-3", "G-CS-4", "G-CS-5", "G-CS-6"}
   )

   # V-7 carve-out sentinel. Used ONLY for rows where the conjunction
   # (prediction_setting == "blocked_or_deferred" AND
   #  status == "blocked_until_additional_validation") holds. Outside
   # the conjunction the sentinel is forbidden; inside it is required.
   BLOCKED_SENTINEL: str = "blocked"

   # V-7 carve-out predicate components.
   BLOCKED_PREDICTION_SETTING: str = "blocked_or_deferred"
   BLOCKED_STATUS: str = "blocked_until_additional_validation"
   ```

2. Add private function:

   ```python
   def _check_v7_cold_start_vocabulary(
       skeleton: list[dict[str, Any]],
   ) -> None:
       """V-7: cold_start_handling vocabulary + sentinel under conjunction carve-out.

       For each row:
           - If prediction_setting == "blocked_or_deferred" AND
             status == "blocked_until_additional_validation":
               assert cold_start_handling == "blocked".
           - Else (every other row, including all model-input
             pre_game / history_enriched_pre_game / in_game_snapshot /
             sanity_gate rows):
               assert cold_start_handling in COLD_START_GATE_VOCAB.
       For ALL rows: assert cold_start_handling is NOT a numeric
       pseudocount / threshold / window / smoothing constant
       (Invariant I7 — no magic numbers).
       """
   ```

   Body, per row (let `cs = row["cold_start_handling"]`,
   `ps = row["prediction_setting"]`, `st = row["status"]`,
   `ffid = row["feature_family_id"]`):

   1. Numeric check (applies to every row): first assert `isinstance(cs,
      str)` (sharpens the diagnostic if `cs` is `None` or some other
      non-string). Then a try/except around `float(cs)` must raise
      `ValueError` OR `TypeError` — use `except (ValueError, TypeError):`
      because `float(None)` raises `TypeError`. On failure (i.e., when
      `float(cs)` succeeds, meaning `cs` is parseable as a number) raise
      `AssertionError` containing `"V-7"`, the `feature_family_id`, and
      the offending numeric token. (This guards integer strings like
      `"5"`, decimal strings like `"0.25"`, scientific `"+1e3"`, special
      `"inf"` / `"nan"`, and underscored `"1_000"`; the leading-`G-`
      prefix on `G-CS-N` tokens prevents `float()` from succeeding, so
      the controlled vocabulary remains valid.)
   2. Conjunction branch:
      `is_carve_out = (ps == BLOCKED_PREDICTION_SETTING and
                       st == BLOCKED_STATUS)`.
   3. If `is_carve_out`: assert `cs == BLOCKED_SENTINEL`. Failure
      message: `"V-7: carve-out row '{ffid}' (prediction_setting='{ps}',
      status='{st}') has cold_start_handling='{cs}'; expected literal
      '{BLOCKED_SENTINEL}'"`.
   4. Else: assert `cs in COLD_START_GATE_VOCAB`. Failure message:
      `"V-7: row '{ffid}' (prediction_setting='{ps}', status='{st}') has
      cold_start_handling='{cs}'; expected one of
      {sorted(COLD_START_GATE_VOCAB)} (controlled vocabulary)"`.

3. Add a call to `_check_v7_cold_start_vocabulary(skeleton)` inside
   `validate_registry_skeleton()`, after the existing
   `_check_v6_history_strict_lt(skeleton)` call. Order of public checks
   in the orchestrator after this PR will be: V-1 base, V-1 strict, V-2,
   V-3, V-4, V-5, V-6, V-7.

4. Update the module docstring "Scope (six checks implemented here):"
   list to "Scope (eight checks implemented here):" and append two
   bullets covering V-1 strict and V-7. Append matching docstring
   bullets to the public `validate_registry_skeleton` function. No
   prose about D-numbered audit dimensions is changed beyond reflecting
   that V-1 strict and V-7 are now in scope.

**Task-specific stop condition:** halt if (a) any of the existing V-1
base / V-2 / V-3 / V-4 / V-5 / V-6 helpers would need to be modified to
land V-7 (none should), (b) `_check_v7_cold_start_vocabulary` causes a
public-API-shape change to `validate_registry_skeleton()` (it must not),
(c) numeric-token check rejects any of the existing G-CS-N values (the
hyphenated `G-CS-N` form makes `float()` raise; this must be confirmed
post-implementation by a quick interactive test).

**Validation report shape:** post-edit show diff of
`validate_registry_skeleton.py`; confirm exactly the additions
specified; confirm `_check_v6_history_strict_lt` is unchanged in
signature/body; confirm the public-API function signature
`validate_registry_skeleton(skeleton, tracker_csv_path) -> None`
is unchanged.

**Executor model:** Sonnet (the V-7 design is fully resolved by the
plan; no further methodology inference is needed). If any spec lookup
or semantic re-interpretation arises during implementation, escalate to
Opus.

### T02b — Add tests for V-1 strict and V-7

**Allowed files:**
`tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`.

**Forbidden files:** all §Files / Forbidden entries plus
`validate_registry_skeleton.py` (T01/T02 done) and the notebook (T03).

**Exact operation:**

**Step 0 (REQUIRED first — F1 from reviewer-deep critique).** Update the
existing `valid_skeleton` fixture so its three `prediction_setting ==
"blocked_or_deferred"` rows carry `cold_start_handling == "blocked"`
(currently they inherit `"G-CS-1"` from the `_row()` default — under
strict V-7 they MUST carry the sentinel). Either:

- **Option A (preferred — cleaner):** Parameterize the `_row()` helper at
  ~line 39 of the test file to accept `cold_start_handling: str = "G-CS-1"`
  as an optional keyword argument; use the kwarg in the dict literal at
  ~line 60. Then update the three carve-out call sites in the
  `valid_skeleton` fixture (the rows whose `prediction_setting=
  "blocked_or_deferred"` and `status="blocked_until_additional_validation"`)
  to pass `cold_start_handling="blocked"` explicitly.
- **Option B (post-construction patch):** After the existing `_row()`
  calls in the fixture, iterate the constructed list and overwrite the
  `cold_start_handling` field to `"blocked"` on rows where both
  `prediction_setting == "blocked_or_deferred"` and `status ==
  "blocked_until_additional_validation"`. Return the modified list.

This step is mandatory: as-is, every existing test that uses
`valid_skeleton` (28 of the 30 existing tests) would fail at the new V-7
step because the fixture's three carve-out rows currently violate the
strict V-7 conjunction.

**Step 1 onwards.** Append the following test cases after the existing
V-6 tests. Use the **updated** `valid_skeleton` fixture; build perturbed
copies via `copy.deepcopy`. Each test must assert a specific
`pytest.raises(AssertionError, match=...)` regex matching `"V-1 strict"`
or `"V-7"` plus a fragment of the descriptive failure text.

Required tests (ten total):

1. `test_v1_strict_valid_skeleton_passes(valid_skeleton)` — happy path.
2. `test_v1_strict_id_too_few_segments_fails(valid_skeleton)` — set one
   row's `feature_family_id` to `"sc2egset.no_dot"` (only 2 segments).
   Expect `AssertionError` matching `"V-1 strict.*sc2egset.no_dot"` or
   the segment-count message.
3. `test_v1_strict_segment_mismatch_fails(valid_skeleton)` — set one
   row's `feature_family_id` to
   `"sc2egset.WRONG_SEGMENT.focal_player_history"` while leaving its
   `prediction_setting` as `"history_enriched_pre_game"`. Expect
   `AssertionError` matching `"V-1 strict.*WRONG_SEGMENT"`.
4. `test_v7_vocabulary_each_gcs_token_passes()` — parameterised loop
   over `["G-CS-1","G-CS-2","G-CS-3","G-CS-4","G-CS-5","G-CS-6"]`. For
   each token, build a minimal valid skeleton (use `_row` helper) where
   one model-input row carries that exact token; assert
   `validate_registry_skeleton` passes. (Use `pytest.mark.parametrize`
   with the six tokens; the fixture already has G-CS-1 by default — the
   loop swaps that single row's token.)
5. `test_v7_sentinel_under_conjunction_passes(valid_skeleton)` — the
   existing `valid_skeleton` already has 3 conjunction-satisfying rows
   with `cold_start_handling="blocked"`. Confirm passes (this is
   redundant with T02b#1 but documents the sentinel branch explicitly).
6. `test_v7_carve_out_status_mismatch_fails(valid_skeleton)` — pick one
   `blocked_or_deferred` row, set its `status` to `"allowed"` (so the
   conjunction does NOT hold), keep `cold_start_handling="blocked"`.
   Expect `AssertionError` matching `"V-7"` (the row no longer satisfies
   carve-out, so `"blocked"` is now an unknown vocabulary token —
   "expected one of \\['G-CS-1', ...\\]").
7. `test_v7_carve_out_prediction_setting_mismatch_fails(valid_skeleton)`
   — pick one `pre_game` (active) row, change its `cold_start_handling`
   to `"blocked"` while leaving `prediction_setting="pre_game"` and
   `status="allowed"`. Expect `AssertionError` matching `"V-7"`.
8. `test_v7_numeric_integer_token_fails(valid_skeleton)` — set one
   model-input row's `cold_start_handling` to `"5"`. Expect
   `AssertionError` matching `"V-7.*numeric"` or
   `"V-7.*cold_start_handling='5'"`.
9. `test_v7_numeric_decimal_token_fails(valid_skeleton)` — set one
   model-input row's `cold_start_handling` to `"0.25"`. Expect
   `AssertionError` matching `"V-7.*numeric"` or
   `"V-7.*cold_start_handling='0.25'"`.
10. `test_v7_unknown_token_fails(valid_skeleton)` — set one model-input
    row's `cold_start_handling` to `"G-CS-99"`. Expect `AssertionError`
    matching `"V-7.*G-CS-99"`.

**Task-specific stop condition:** halt if any test from PR #212 fails
in a way not caused by the new V-1 strict or V-7 assertions; halt if
Step 0 (fixture update) is skipped or partially applied (the three
carve-out rows MUST carry `cold_start_handling == "blocked"` after
Step 0; without that the entire pre-existing test suite would fail at
V-7 instead of being a clean "add tests, run, all pass" step).

**Validation report shape:** show diff of test file; confirm 10 tests
added; confirm no test deleted; confirm coverage for the new helpers in
the post-T05 coverage report is 100% on the added lines (`pytest --cov
--cov-report=term-missing` shows the two new private functions covered).

**Executor model:** Sonnet.

### T03 — Notebook narrative correction (markdown cells only)

**Allowed files:**
`sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`.

**Forbidden files:** all §Files / Forbidden entries; in particular do
NOT touch any literal SKELETON_PRE_GAME / SKELETON_HISTORY /
SKELETON_IN_GAME_NOW / SKELETON_IN_GAME_CAVEAT /
SKELETON_GATE_AND_BLOCKED row tuple.

**Exact operation:** correct three narrative passages by replacing the
text shown in the "Before" column with the text shown in the "After"
column. All three are inside markdown / code-comment cells, not inside
SKELETON literal tuples. Line numbers refer to the .py file as it
exists on master at `18d30a81`.

| Location | Before | After |
|----------|--------|-------|
| Line 128 (markdown cell, "Lineage source" sub-list, item starting `# - CROSS-02-02-v1.0.1 §6` continuing on line 127–128) | `gates G-CS-1..G-CS-6 — no magic numbers per Invariant I7)` | `gates G-CS-1..G-CS-6 for active and candidate rows; the literal "blocked" sentinel for blocked_or_deferred rows where status == "blocked_until_additional_validation" — no magic numbers per Invariant I7)` |
| Line 258 (code-cell prelude comment immediately above `_COLS`) | `# Cold-start handling values use only the gate vocabulary G-CS-1..G-CS-6\n# (CROSS-02-02-v1.0.1 §9); no numeric pseudocount, threshold, smoothing\n# strength, or imputation constant appears (Invariant I7).` | `# Cold-start handling values follow controlled discipline:\n# active and candidate rows use only the gate vocabulary G-CS-1..G-CS-6\n# (CROSS-02-02-v1.0.1 §9.1); blocked_or_deferred rows whose status is\n# "blocked_until_additional_validation" use the literal sentinel "blocked".\n# No numeric pseudocount, threshold, smoothing strength, or imputation\n# constant appears anywhere (Invariant I7).` |
| Line 486 (markdown cell, "Checks NOT in scope of this scaffold PR" list) | `# Checks NOT in scope of this scaffold PR (deferred to subsequent validation\n# modules): cold-start gate vocabulary check (G-CS-1..G-CS-6), per-player\n# construction symmetry (Invariant I5), candidate-leakage-mode coverage\n# against CROSS-02-01-v1.0.1, and audit dimensions D2/D3/D6/D8/D9/D10/D11/D12/D15.` | `# Checks IN scope as of this PR (V-1 strict + V-7): feature_family_id\n# second-segment alignment with prediction_setting, and cold-start\n# vocabulary/sentinel discipline (G-CS-1..G-CS-6 for active rows; literal\n# "blocked" sentinel under the carve-out conjunction).\n# Checks NOT YET in scope (deferred to subsequent validation modules):\n# per-row optimal G-CS gate fit (which gate suits each family\n# scientifically), per-player construction symmetry (Invariant I5),\n# candidate-leakage-mode coverage against CROSS-02-01-v1.0.1, and audit\n# dimensions D2/D3/D6/D8/D9/D10/D11/D12/D15.` |

After edits:
- Update the print-banner line at line 495 from
  `print("validate_registry_skeleton: ALL PASS (V-1 through V-6)")`
  to
  `print("validate_registry_skeleton: ALL PASS (V-1 through V-7)")`.
- Run `jupytext --sync sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
  to regenerate the paired `.ipynb`. Both `.py` and `.ipynb` must end
  up in the staged change set.

**Task-specific stop condition:** halt if a `git diff` of the notebook
.py shows any changed line outside the four locations enumerated above
(lines 128, 258, 486, 495), or any changed line inside a SKELETON_*
literal tuple.

**Validation report shape:** show `git diff --stat` for the notebook
.py and .ipynb (only those two files); show the four replaced
hunks with `git diff -U0`; confirm no SKELETON literal tuple changed.

**Executor model:** Sonnet (mechanical narrative replacement).

### T04 — Run pre-commit-equivalent checks

**Allowed files:** read-only across repo; no edits.

**Exact operations (single shell command per check, &&-chained where
appropriate):**

1. `source .venv/bin/activate && poetry run ruff check src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
2. `source .venv/bin/activate && poetry run mypy src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`
3. `source .venv/bin/activate && poetry run jupytext --check sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`

**Task-specific stop condition:** halt if ruff or mypy reports any
error; halt if jupytext check reports drift between .py and .ipynb (T03
must have re-synced).

**Validation report shape:** copy the verbatim ruff and mypy outputs;
confirm no errors; confirm jupytext --check exit status 0.

**Executor model:** Sonnet.

### T05 — Run pytest with coverage; verify ≥ 95%

**Allowed files:** read-only repo; create scratch `coverage.txt` then
delete.

**Exact operation:** `source .venv/bin/activate && poetry run pytest
tests/ -v --cov --cov-report=term-missing | tee coverage.txt`. Read
`coverage.txt`; confirm the suite passes; confirm overall coverage ≥
95% (the `[tool.coverage.report] fail_under = 95` gate enforces this).
Verify the new helpers in `validate_registry_skeleton.py` are listed at
100% line coverage in the term-missing report. Delete `coverage.txt`.

**Task-specific stop condition:** halt if any test fails; halt if
coverage drops below 95% (do NOT lower the gate); halt if either of
the two new helpers shows uncovered lines.

**Validation report shape:** quote the final pytest summary line, the
`coverage report` total, and the per-file coverage row for
`validate_registry_skeleton.py`; confirm `coverage.txt` was deleted.

**Executor model:** Sonnet.

### T06 — Execute the merged notebook and confirm ALL PASS

**Allowed files:** read-only outside the executed notebook pair.

**Exact operation:** `source .venv/bin/activate && poetry run jupyter
nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300
sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb`,
then `source .venv/bin/activate && poetry run jupytext --sync
sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`.

After execution:
- Confirm cell output banner reads literally
  `"validate_registry_skeleton: ALL PASS (V-1 through V-7)"` (T03's
  print-line update at line 495 must be picked up by execution).

**Task-specific stop condition:** halt if `validate_registry_skeleton`
raises any `AssertionError`; halt if the notebook execution shows a
banner that does not literally match `"ALL PASS (V-1 through V-7)"`;
halt if the post-run `git status` lists any file outside the allowed
list (e.g., an artifact under `reports/`).

**Validation report shape:** quote the print-cell output; show
`git status`; confirm only allowed files are dirty.

**Executor model:** Sonnet.

### T07 — Scaffold/code commit (validation module + tests + notebook narrative)

**Allowed files:** as enumerated in §Files / Allowed except
pyproject.toml and CHANGELOG.md (those land in T08).

**Exact operation:**

1. Stage exactly:
   - `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`
   - `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`
   - `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
   - `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb`
2. Write commit message to `.github/tmp/commit.txt` via the Write tool
   (no heredoc — heredocs break in zsh per project memory). Message
   body:

   ```
   feat(phase02): SC2EGSet 02_01_01 V-1 strict + V-7 cold-start vocab/sentinel

   Continues lineage sequence step 6 (next validation module) for SC2EGSet
   Step 02_01_01. Skeleton row content from PR #212 is unchanged.

   - V-1 strict: feature_family_id second dot-segment must equal
     prediction_setting verbatim; >=3 segments required.
   - V-7: cold_start_handling vocabulary + sentinel under conjunction
     carve-out (prediction_setting == "blocked_or_deferred" AND
     status == "blocked_until_additional_validation" -> literal "blocked";
     every other row -> G-CS-1..G-CS-6; numeric tokens forbidden everywhere).
   - Notebook narrative corrected at three markdown / comment locations
     (lines 128, 258, 486) plus print-banner update (line 495 V-6 -> V-7)
     to reflect the conjunction carve-out; SKELETON literal tuples
     untouched.
   - Tests cover V-1 strict failure modes, V-7 vocabulary success across
     each G-CS-N token, V-7 sentinel success under conjunction, V-7
     conjunction failure (status mismatch and prediction_setting mismatch),
     V-7 numeric token failure (integer + decimal), V-7 unknown-token
     failure (G-CS-99).

   Binds: CROSS-02-00-v3.0.1, CROSS-02-01-v1.0.1, CROSS-02-02-v1.0.1
   §9.1, CROSS-02-03-v1.0.1.
   ```
3. `git commit -F .github/tmp/commit.txt`. (Pre-commit hooks run ruff
   and mypy — they must pass; if a hook fails, fix and create a NEW
   commit, never `--amend`.)
4. Verify `git log -1 --name-only` lists exactly the four files.

**Task-specific stop condition:** halt if any of the four files is
missing from the commit; halt if any forbidden file is staged; halt if
a pre-commit hook fails (in which case fix the cause and re-stage —
never `--no-verify`, never `--amend`).

**Validation report shape:** show `git log -1 --stat`; confirm the four
files listed; confirm pre-commit hooks reported clean.

**Executor model:** Sonnet.

### T08 — Release commit (pyproject.toml + CHANGELOG.md)

**Allowed files:** `pyproject.toml`, `CHANGELOG.md`,
`.github/tmp/commit.txt`.

**Exact operation:**

1. Edit `pyproject.toml`: change `version = "3.48.0"` to
   `version = "3.49.0"`. Single source — do NOT add `__version__`
   anywhere.
2. Edit `CHANGELOG.md`:
   - Roll the existing `[Unreleased]` block heading to
     `[3.49.0] — 2026-05-08 (PR #N: phase02/sc2egset-feature-registry-v1-strict-and-v7-cold-start)`
     where `N` will be substituted post-`gh pr create`.
   - Insert a new empty `[Unreleased]` block above with subsections
     `### Added`, `### Changed`, `### Fixed`, `### Removed`.
   - Populate the new `[3.49.0]` Added section with two bullets:
     - "V-1 strict refinement: `feature_family_id` second dot-segment
       must equal `prediction_setting` verbatim (CROSS-02-02-v1.0.1
       OQ1)."
     - "V-7 cold-start vocabulary + sentinel: active rows use
       G-CS-1..G-CS-6; `blocked_or_deferred` rows under the conjunction
       (`prediction_setting == 'blocked_or_deferred'` AND
       `status == 'blocked_until_additional_validation'`) use the
       literal `\"blocked\"` sentinel; numeric tokens forbidden
       (Invariant I7)."
3. Stage exactly `pyproject.toml` and `CHANGELOG.md`. Write commit
   message to `.github/tmp/commit.txt`:

   ```
   chore(release): bump version to 3.49.0

   Roll [Unreleased] into [3.49.0] for
   phase02/sc2egset-feature-registry-v1-strict-and-v7-cold-start.
   ```
4. `git commit -F .github/tmp/commit.txt`. Verify
   `git log -1 --name-only` shows only `pyproject.toml` and
   `CHANGELOG.md`.
5. After PR is created (T09 below), substitute the actual PR number
   `N` in the `[3.49.0]` heading and commit as
   `chore(release): substitute PR number in CHANGELOG [3.49.0]`.

**Task-specific stop condition:** halt if any file other than
pyproject.toml and CHANGELOG.md is staged; halt if pre-commit hooks
fail.

**Validation report shape:** show `git log -1 --stat`; confirm exactly
two files; confirm `pyproject.toml` version is `"3.49.0"`.

**Executor model:** Sonnet.

### T09 — Push, create draft PR, run reviewer-deep, mark ready

**Allowed files:** `.github/tmp/pr.txt`,
`planning/INDEX.md` (active row update), `CHANGELOG.md` (PR-number
substitution after PR is created).

**Exact operation:**

1. `git push -u origin phase02/sc2egset-feature-registry-v1-strict-and-v7-cold-start`.
2. Write PR body to `.github/tmp/pr.txt` per
   `.github/pull_request_template.md` (must include `## Summary`,
   `## Test plan`, footer `🤖 Generated with [Claude Code](https://claude.com/claude-code)`).
3. `gh pr create --draft --title "feat(phase02): SC2EGSet 02_01_01 V-1 strict + V-7 cold-start vocabulary/sentinel validation" --body-file .github/tmp/pr.txt --base master`.
4. Capture PR number `N` from the gh output. Substitute `PR #N` into
   the `[3.49.0]` CHANGELOG heading; commit as
   `chore(release): substitute PR number in CHANGELOG [3.49.0]`; push.
5. **Append the PR number `N` to the active branch's row in
   `planning/INDEX.md`** (the bulk INDEX.md update — archiving the closed
   PR #212 entry and setting the active-plan row to this branch — was
   already performed in the docs(planning) commit that landed this plan
   on the branch BEFORE T01 fired, per F4 from reviewer-deep critique).
   T09 step 5 is therefore restricted to a small append: add `(PR #N)`
   to the active-plan row's description.
6. Dispatch `@reviewer-deep` with the PR URL and `base_ref = master`.
   The reviewer-deep agent reads `planning/current_plan.md`,
   `planning/current_plan.critique.md`, and the full diff.
7. If reviewer-deep returns `PASS` or `PASS-WITH-NOTES` →
   `gh pr ready <N>` and clean up `.github/tmp/`. If reviewer-deep
   raises a methodology BLOCKER → halt; the parent session must
   dispatch `@reviewer-adversarial` per
   `.claude/rules/data-analysis-lineage.md` line 24 carve-out.

**Task-specific stop condition:** halt if `git push` fails; halt if
`gh pr create` fails; halt if reviewer-deep reports BLOCKER methodology
(escalate to reviewer-adversarial — do NOT continue execution).

**Validation report shape:** PR URL; reviewer-deep verdict; final
`git status` clean; `.github/tmp/pr.txt` removed.

**Executor model:** Sonnet for mechanics; reviewer-deep (Opus) for
the gate.

## Validation gates

All must hold for merge:

1. `validate_registry_skeleton(SKELETON, tracker_csv_path=TRACKER_CSV)`
   on the unmodified merged 26-row skeleton returns without raising
   `AssertionError`. The notebook prints the updated banner
   `"validate_registry_skeleton: ALL PASS (V-1 through V-7)"`.
2. V-1 strict passes on the unmodified skeleton (verified during
   plan-phase verification; must remain green post-implementation).
3. V-7 stricter passes on the unmodified skeleton: 23 rows G-CS-N + 3
   rows `"blocked"` under conjunction; 0 violations. Verified during
   plan-phase verification; must remain green post-implementation.
4. The narrative correction is visible in `git diff master..HEAD` for
   the notebook .py at lines 128, 258, 486 and at the print-banner
   line.
5. `git diff master..HEAD --name-only` lists no forbidden file (see
   §Files / Forbidden).
6. Two implementation commits land on the branch (T07 scaffold/code +
   T08 release), plus an optional T09 PR-number-substitution commit.
   No `--amend` in any case.
7. Pytest suite passes; coverage ≥ 95% (`fail_under = 95` enforced);
   the two new helpers in `validate_registry_skeleton.py` are 100%
   covered.
8. Ruff, mypy, jupytext --check all clean.
9. Reviewer-deep verdict is `PASS` or `PASS-WITH-NOTES`. A `BLOCKER`
   methodology verdict halts execution and triggers reviewer-adversarial
   (per `.claude/rules/data-analysis-lineage.md` line 24).

## Release policy

Version 3.48.0 → **3.49.0**. Minor bump per `.claude/rules/git-workflow.md`
§"PR Creation Flow" (Category A feat). Single source of truth:
`pyproject.toml`. CHANGELOG roll under `[3.49.0] — 2026-05-08
(PR #N: phase02/sc2egset-feature-registry-v1-strict-and-v7-cold-start)`,
new empty `[Unreleased]` inserted at top.

## Reviewer routing

- **Plan-phase critique (required before execution begins).**
  Per the Cat A protocol, after this plan is approved, the parent
  session must commission `planning/current_plan.critique.md` from
  `reviewer-deep` (per the `.claude/rules/data-analysis-lineage.md`
  line-24 Phase 02 readiness carve-out — same routing as PR #212).
  Reviewer-adversarial is NOT the default critique gate here. The
  critique is a separate read-only deliverable and does NOT come from
  the planner-science agent that authored this plan.
- **Post-execution gate.** `reviewer-deep` (Opus) at T09 after the
  draft PR is created. Reads `planning/current_plan.md`,
  `planning/current_plan.critique.md`, the diff, and `base_ref = master`.
- **Reviewer-adversarial.** Invoked ONLY if reviewer-deep raises a
  methodology BLOCKER. Per `.claude/rules/data-analysis-lineage.md`
  line 24, this active Phase 02 readiness PR does not invoke
  reviewer-adversarial upfront unless the plan is amended or
  reviewer-deep raises a BLOCKER requiring adversarial methodology
  review.

## Non-batching rationale

Per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for
empirical work", each empirical Step proceeds:

1. ROADMAP stub only — done by PR #211.
2. Notebook scaffold + one validation module — done by PR #212.
3. Execute and report — done by PR #212.
4. User review — done.
5. Commit — done by PR #212.
6. **Next validation module** — *this PR* (V-1 strict + V-7).
7. Only after all validation modules pass, generate artifacts —
   deferred.
8. Then research_log / STEP_STATUS / manifest — deferred.
9. Then reviewer-deep — happens at T09 of this PR.

V-1 strict and V-7 are presented together because the user has
explicitly approved the bundle ("Option C hybrid"). They are
co-located in `validate_registry_skeleton.py`, share a common
test-fixture pattern, and bind a single CHANGELOG entry; bundling
them respects sequence step 6 ("Next validation module" — singular in
spirit but plural in practice when validators are tightly coupled).
This PR does NOT bundle artifact generation, status updates, or
manifest updates; those remain firmly behind step 7.

## Stop conditions

### Pre-implementation stop condition

Before T01 begins, the executor must verify the working tree is clean
on the freshly-created branch
`phase02/sc2egset-feature-registry-v1-strict-and-v7-cold-start`
(checked out from `master @ 18d30a81`); halt if `git status` lists any
modification or untracked file beyond `planning/current_plan.md` and
`planning/current_plan.critique.md`. (No methodological halt remains —
the V-7 conjunction semantics are resolved by the user in this plan.)

### Mid-implementation halt triggers

Halt and report to the parent session if any of the following occur
during T01–T08:

1. The verification computations in §Verification fail when re-run
   against the on-disk skeleton (e.g., a row's `prediction_setting` or
   `cold_start_handling` does not match what the plan stated, or a
   `blocked_or_deferred` row is found whose status is not
   `blocked_until_additional_validation`). In that case, the user's
   resolution may need refinement — do NOT patch the skeleton.
2. A pre-commit hook (ruff or mypy) fails; investigate and fix the
   underlying cause; create a NEW commit (never `--amend`).
3. Pytest fails or coverage falls below 95%; do NOT lower the gate;
   add tests / fix code.
4. The notebook execution at T06 prints an `AssertionError`; do NOT
   patch the print line — investigate which V-N failed and report
   the offending row(s).
5. `git status` lists any forbidden file (see §Files / Forbidden);
   stop staging immediately and surface the violation.
6. `gh pr create` fails or `git push` is rejected.
7. Reviewer-deep returns a methodology BLOCKER; halt T09 and route to
   reviewer-adversarial.

## Open Questions

None. All methodology decisions for this PR are resolved by the user's
2026-05-08 directive (V-1 strict semantics; V-7 conjunction carve-out
with literal `"blocked"` sentinel and `G-CS-1..G-CS-6` controlled
vocabulary; bundle as Option C hybrid; skeleton row content untouched;
narrative correction in T03 only). Reviewer-deep PASS-WITH-FIXES
verdict applied four mechanical fixes (F1 fixture-update step,
F2 widened ValueError/TypeError exception, F3 INVARIANTS.md +
pyproject/CHANGELOG + planning/* added to §Forbidden, F4 split
INDEX.md update timing) — see `planning/current_plan.critique.md`.

## Acceptance criteria

The PR is mergeable when ALL of the following are simultaneously true:

1. **V-7 stricter passes on the unmodified skeleton.** No
   SKELETON literal tuple is changed in `git diff master..HEAD`. The
   merged notebook executes ALL PASS through V-7. (Verification
   confirmed in plan phase: 23 G-CS-N + 3 sentinel; 0 violations.)
2. **V-1 strict passes on the unmodified skeleton.** Every `feature_family_id`
   has ≥ 3 dot-segments and segment 1 equals `prediction_setting`.
   (Verification confirmed in plan phase: 0 violations.)
3. **Narrative correction visible.** `git diff master..HEAD` for the
   notebook .py shows the three replacement hunks at lines 128, 258,
   486 (plus the print-banner line update from V-6 to V-7).
4. **Two implementation commits.** `git log master..HEAD --oneline`
   shows the T07 scaffold/code commit followed by the T08 release
   commit (and optionally a T09 PR-number-substitution commit). No
   `--amend`.
5. **No forbidden files in `git diff master..HEAD`.** The diff lists
   only files from §Files / Allowed.
6. **Coverage ≥ 95%.** `pytest --cov` reports overall ≥ 95%; the two
   new helpers in `validate_registry_skeleton.py` show 100% line
   coverage.
7. **Reviewer-deep verdict is PASS or PASS-WITH-NOTES.** No unresolved
   methodology BLOCKER. If a BLOCKER is raised, T09 halts and the
   parent session dispatches reviewer-adversarial.
