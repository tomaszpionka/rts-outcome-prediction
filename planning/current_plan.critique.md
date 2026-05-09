# Plan critique — SC2EGSet Step 02_01_01 V-1 strict + V-7 (Option C)

---
target_plan: planning/current_plan.md
target_branch: phase02/sc2egset-feature-registry-v1-strict-and-v7-cold-start
target_commit_at_review: 4c243158 (branch HEAD; master @ 18d30a81)
reviewer: reviewer-deep
reviewer_date: 2026-05-08
critique_round: 1
verdict: PASS-WITH-FIXES
---

## §Summary verdict

The plan is methodologically sound: V-1 strict refinement and V-7 controlled-vocabulary/sentinel discipline are well-scoped, the conjunction carve-out (`prediction_setting == "blocked_or_deferred"` AND `status == "blocked_until_additional_validation"` → `"blocked"` sentinel; everything else → `G-CS-1..G-CS-6`) is faithful to the user's resolution, and the bundle (V-1 strict + V-7 in one PR) is genuinely cohesive — both extend `validate_registry_skeleton` in `validate_registry_skeleton.py`, both are validation-module additions per `data-analysis-lineage.md` §"Non-batching rule" sequence step 6, both share the `valid_skeleton` test fixture, and both bind the same CHANGELOG roll to 3.49.0. Live re-verification of the merged 26-row skeleton confirms 0 V-1 strict violations and 23 G-CS-N + 3 sentinel rows under the strict conjunction, with no `prediction_setting`-only or `status`-only mismatches. However, the plan contains one factual error about the **test fixture** state that, if executed literally, will cause every existing test using `valid_skeleton` to fail at the new V-7 step. This is not a methodology defect — it is a plan-text accuracy defect — and it is mechanically fixable. Three smaller mechanical fixes round out the required-fix list. None of the required fixes are scientific risks, and reviewer-adversarial is NOT required (no methodology BLOCKER).

## §Re-verification of plan §Verification claims

| Claim | Method | Result |
|-------|--------|--------|
| **V-1 strict: 0 violations on all 26 rows** (segment 0 = "sc2egset", segment 1 = `prediction_setting`) | Live evaluation of the merged `SKELETON` from the on-disk notebook .py at `4c243158` | **PASS** — 26 rows scanned; for every row `parts = feature_family_id.split(".")` has len ≥ 3, `parts[0] == "sc2egset"`, and `parts[1] == row["prediction_setting"]`. 0 violations. |
| **V-7 conjunction: 23 G-CS-N rows; 3 carve-out rows with `cold_start_handling == "blocked"` AND `prediction_setting == "blocked_or_deferred"` AND `status == "blocked_until_additional_validation"`; 0 prediction_setting-only or status-only mismatches** | Live evaluation of the merged `SKELETON` | **PASS** — 23 non-carve-out rows carry G-CS-N tokens (none carry `"blocked"`, none carry numeric tokens); 3 rows satisfy the carve-out conjunction and all 3 carry `cold_start_handling="blocked"`; ps-only mismatches: 0; status-only mismatches: 0; numeric-token violations: 0. The unmodified 26-row skeleton passes the stricter V-7 as planned. |
| **Narrative target line 128** (`"gates G-CS-1..G-CS-6 — no magic numbers per Invariant I7)"`) | `awk 'NR==128'` against on-disk notebook .py | **PASS** — line 128 is exactly `#   gates G-CS-1..G-CS-6 — no magic numbers per Invariant I7)`. |
| **Narrative target line 258** (code-cell prelude comment immediately above `_COLS`) | `awk 'NR==258'` | **PASS** — line 258 is `# Cold-start handling values use only the gate vocabulary G-CS-1..G-CS-6`; `_COLS` is at line 261. The plan's "immediately above `_COLS`" is accurate. |
| **Narrative target line 486** (markdown cell, "Checks NOT in scope" list) | `awk 'NR==485..488'` | **PASS-WITH-NOTE** — the "Checks NOT in scope" comment block spans lines 485–488. Line 485 is the header (`# Checks NOT in scope of this scaffold PR (deferred to subsequent validation`), line 486 is `# modules): cold-start gate vocabulary check (G-CS-1..G-CS-6), per-player`. The plan refers to "Line 486" but presents the "Before" content as the entire 4-line block. The replacement is structurally correct; the line-number label is mildly imprecise (the block STARTS at 485) but this is non-blocker. The executor will replace the right text either way. |
| **Print-banner line 495** (`print("validate_registry_skeleton: ALL PASS (V-1 through V-6)")` → V-7) | `awk 'NR==495'` | **PASS** — line 495 is exactly the print line; V-6 → V-7 substitution lands cleanly. |

## §Per-question findings

### 1. Verification re-check — **PASS**

Independent live re-evaluation of the merged `SKELETON` confirms every quantitative claim in the plan's §Verification block (0 V-1-strict violations; 23 G-CS-N + 3 sentinel under strict conjunction; 0 ps-only or status-only mismatches; 0 numeric-token rows). Narrative line numbers 128, 258, 495 are exact. Line 486 is the second line of a 4-line comment block whose header is at 485 — the replacement is correct in scope; only the line-number label is slightly imprecise. No falsifier failed.

### 2. Scope cohesion (V-1 strict + V-7 bundled) — **PASS**

This is genuine cohesion, not hidden batching. (a) Both modifications touch the same target file (`validate_registry_skeleton.py`); (b) both are validation-module additions under `data-analysis-lineage.md` §"Non-batching rule" sequence step 6 ("Next validation module"); (c) both share the `valid_skeleton` fixture pattern; (d) the user explicitly approved the Option-C hybrid bundle (per plan front-matter and §Open questions); (e) neither produces an artifact, neither updates STEP_STATUS / research_log / manifest. The plan does NOT bundle artifact generation, status updates, or manifest updates with the new validators — those remain firmly behind sequence step 7. PR #212's reviewer-deep critique noted V-1 strict as follow-up #1; this PR closes that follow-up with the V-7 work in the same logical breath. The non-batching rationale block in the plan addresses this explicitly and is defensible.

### 3. V-7 conjunction semantics defensibility — **PASS-WITH-NOTE**

The conjunction encoding (`is_carve_out = (ps == BLOCKED_PREDICTION_SETTING and st == BLOCKED_STATUS)`, then `cs == "blocked"` inside, `cs in COLD_START_GATE_VOCAB` outside) is faithful to the user's resolution. Failure messages name the offending `feature_family_id`, the actual `cold_start_handling`, the `prediction_setting`, and the `status` — adequately diagnostic. The edge cases the executor must keep in mind:
- **A row with `prediction_setting="blocked_or_deferred"` but `status` other than `"blocked_until_additional_validation"`** (e.g., `status="allowed"`). Conjunction fails → the else-branch demands `cs in {G-CS-1..G-CS-6}`. Plan's test 6 (`test_v7_carve_out_status_mismatch_fails`) covers this case with a row carrying `cs="blocked"` — failure message says "expected one of [G-CS-1, ...]". Correct.
- **A row with `prediction_setting != "blocked_or_deferred"` but `status="blocked_until_additional_validation"`**. Conjunction fails → else-branch demands G-CS-N vocabulary. Plan's tests do NOT explicitly cover this case. It is not a blocker (the same else-branch handles it), but a defensive parametrization in tests 6/7 to also exercise the symmetric mismatch is a non-blocker follow-up.
- The plan's stop condition for T02 anticipates that the numeric-token check rejects no existing G-CS-N value. Confirmed live: `float("G-CS-1")` through `float("G-CS-6")` all raise `ValueError`. Safe.

### 4. Numeric-token check soundness — **PASS-WITH-NOTE**

The plan's `try: float(cs); except ValueError: pass` correctly catches `"5"`, `"0.25"`, `"5."`, `".5"`, `" 5 "`, `"+1e3"`, `"inf"`, `"nan"`, `"NaN"`, `"1_000"` — all of which violate I7. It does NOT catch `"0x10"`, `""`, or arbitrary non-numeric strings. **In practice this is irrelevant** because the controlled-vocabulary branch catches every one of those: `"0x10"` and `""` are not in `{G-CS-1..G-CS-6}` and not equal to `"blocked"`, so the V-7 vocabulary/sentinel assertion fires. The numeric check is a redundant first-line defense whose job is producing a more diagnostic error message ("V-7 numeric token") for the most common I7 violation pattern (a bare number leaked into `cold_start_handling`). The plan should also catch `TypeError` (e.g., `cs is None`) — the current spec only mentions `ValueError`, but `float(None)` raises `TypeError`. **Minor fix**: use `except (ValueError, TypeError)`. This is a fix-grade item, not a blocker.

### 5. Forbidden-files completeness — **PASS-WITH-FIXES**

The plan's §Files / Forbidden enumerates artifacts, status YAMLs, research_log, ROADMAP, the four locked specs by name, thesis tree, AoE2, data, docs, .claude, SKELETON tuples, and the tracker CSV. **Missing entries** that should be flagged:
1. **`src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md`** — the dataset-level invariants file exists and was not enumerated.
2. **`pyproject.toml` and `CHANGELOG.md` during T01–T07**. These are §Allowed but only at T08. The plan does not explicitly forbid them during T01–T07. Adding them under T01–T07 (as forbidden until T08) prevents the failure mode where the executor stages pyproject.toml in the T07 scaffold commit by accident.
3. **`planning/current_plan.md` and `planning/current_plan.critique.md`** during T07 (scaffold commit) and T08 (release commit). These already exist on the branch from earlier docs(planning) commits and should not appear in the T07/T08 staged set.

### 6. Task ordering and stop conditions — **PASS-WITH-NOTE**

T01 (V-1 strict code) → T02 (V-7 code) → T02b (tests) → T03 (notebook narrative) → T04 (ruff/mypy/jupytext-check) → T05 (pytest+coverage) → T06 (notebook execute) → T07 (scaffold commit) → T08 (release commit) → T09 (push+PR+reviewer). The ordering is sensible. One stop condition (T02b: "halt if the existing `valid_skeleton` fixture cannot be reused") rests on an incorrect premise — see finding #11/F1 below.

### 7. T07 commit scope (4 files in one commit) — **PASS**

T07 collapses into 1 scaffold/code commit (validation module + tests + notebook .py + .ipynb) versus PR #212's 4-commit pattern. The reduction is justified: PR #212 was a from-scratch scaffold whose pieces were independently meaningful; this PR adds two helpers + their tests + a 4-location narrative correction, all of which are tightly coupled. Splitting these would create commits that don't pass tests on their own. The plan's 4-files-one-commit rationale is sound.

### 8. Coverage gate (overall ≥ 95%, per-file ≥ 95%, new helpers 100%) — **PASS**

Live measurement at `4c243158` shows `validate_registry_skeleton.py` per-file coverage at **96.15%** (122 stmts, 3 uncovered: lines 243, 311, 317 — defensive branches). After T01 + T02 add roughly +20 statements, the new total is ≈142 stmts. If T02b's 10 new tests cover all 20 added lines (the plan asserts they will), per-file coverage becomes ≈ 139/142 ≈ **97.9%** — well above the 95% gate even with the existing 3 defensive branches still uncovered. The math holds.

### 9. PR #212 follow-up handling (defer parents[6] cleanup + defensive-branch coverage) — **PASS**

The plan's §Non-goals defers test-infra cleanup and the 3 defensive-branch lines (243, 311, 317) to a hygiene PR — only including them if T01/T02b modifications happen to relocate or affect those specific lines. Defensible: (a) neither item blocks correctness of the V-7 work, (b) batching them with V-7 would inflate scope, (c) PR #212 reviewer-deep filed them as follow-ups (not blockers), (d) the artifact PR is the natural place to consolidate hygiene.

### 10. PR-number substitution + INDEX.md update timing — **PASS-WITH-FIXES**

T09 scope correctly handles PR-number substitution as a separate commit. INDEX.md update is also placed in T09. **Two issues**:
- **INDEX.md is currently STALE**: the Active plan row still reads `phase02/sc2egset-feature-registry-scaffold (2026-05-07)`. PR #212 is merged but INDEX.md was not updated as part of PR #212. For this new plan, INDEX.md should be updated EARLIER — when the new plan file is committed (i.e., at the docs(planning) commit on the new branch), not at T09 after PR creation. T09 is too late: between the new docs(planning) commit and PR creation, INDEX.md will mislead any agent that reads it.
- The T09 step 5 instruction "append a row to the Archive table for the closed PR #212 (if not yet present)" is conditional on the row not being there. **It is not there** as of `4c243158`. The conditional language should resolve to a definite action since live state is known.

### 11. Reviewer routing (deep, not adversarial; deep again at gate) — **PASS**

Reviewer-deep is the active critique slot per `data-analysis-lineage.md` line 24 Phase 02 readiness carve-out (matching PR #212). V-7 introduces a controlled-vocabulary commitment (`{G-CS-1..G-CS-6}` ∪ `{"blocked"}` is the sole admissible cold-start handling for the rest of Phase 02 sc2egset). The plan is honest about this: it says V-7 validates "vocabulary/sentinel discipline only" and explicitly defers "the choice of which G-CS gate fits each family scientifically" to D3. Reviewer-deep is sufficient.

### 12. Honesty check — **PASS-WITH-FIXES**

The plan is mostly honest. The honesty defect is in the test-fixture claims, not the methodology: §Verification §2 mis-frames the existing `valid_skeleton` fixture as "already has 3 conjunction-satisfying rows with `cold_start_handling="blocked"`". The fixture's actual cold_start_handling on those rows is `"G-CS-1"` (the `_row()` default). T02b's stop condition similarly asserts "the fixture's 7 rows already satisfy stricter V-7 by construction" — also wrong. See blocker-grade fixture-update fix below.

## §Required fixes (PASS-WITH-FIXES)

The plan is approved subject to these mechanical fixes to the plan text. None are scientific; all are accuracy or completeness.

### F1 (most important) — Fixture must be updated. T02b instructions are incorrect about the existing fixture state.

**Where**: `planning/current_plan.md` T02b "Exact operation" section and §Verification §2.

**Problem**: The existing `valid_skeleton` fixture in `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py` lines 67–126 has THREE rows with `prediction_setting="blocked_or_deferred"` AND `status="blocked_until_additional_validation"` — these satisfy the V-7 carve-out conjunction. But ALL THREE rows inherit `cold_start_handling="G-CS-1"` from the `_row()` helper default at line 60. Under strict V-7 they MUST carry `cold_start_handling="blocked"`. As-is, every existing test that uses `valid_skeleton` (28 of the 30 existing tests) would fail at the new V-7 step.

**Fix**: T02b must explicitly include "Update the three carve-out rows in the `valid_skeleton` fixture to set `cold_start_handling='blocked'`". The simplest mechanical change is to extend the `_row()` helper to accept `cold_start_handling` as an optional kwarg, then call sites for the three blocked rows pass `cold_start_handling='blocked'`. Drop the §Verification §2 / T02b stop-condition claim "the fixture's 7 rows already satisfy stricter V-7 by construction" — replace with "the fixture is updated in T02b so the three carve-out rows carry `cold_start_handling='blocked'`."

**Severity**: PASS-WITH-FIXES (NOT a methodology blocker). Without this fix the executor will hit a stop condition (28 test failures) that the plan did not anticipate.

### F2 — `except (ValueError, TypeError)` not just `except ValueError`.

**Where**: `planning/current_plan.md` T02 §Body step 1.

**Problem**: `float(None)` raises `TypeError`, not `ValueError`. If `cold_start_handling` is ever `None`, the V-7 numeric check would propagate `TypeError` and abort with an unrelated message rather than producing a "V-7 numeric" diagnostic.

**Fix**: Replace `try: float(cs); except ValueError: ...` with `try: float(cs); except (ValueError, TypeError): ...`. Also assert `isinstance(cs, str)` first; the plan's prose mentions this — make sure that assertion lands BEFORE the `float()` call so the diagnostic is sharper.

**Severity**: Minor fix. Defensive.

### F3 — Forbidden-file list completeness.

**Where**: `planning/current_plan.md` §Files / Forbidden table.

**Fix**: Add three rows:
1. `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md`
2. `pyproject.toml` and `CHANGELOG.md` (during T01–T07; allowed only at T08)
3. `planning/current_plan.md` and `planning/current_plan.critique.md` (during T07–T08; must not be re-staged)

**Severity**: Hygiene fix. Earlier flagging is preferred.

### F4 — INDEX.md update timing — split into two updates.

**Where**: `planning/current_plan.md` T09 step 5.

**Problem**: INDEX.md is currently stale. The plan defers INDEX.md update to T09 (post-PR-create). Between the new `docs(planning):` commit authoring the new plan file and T09, INDEX.md will mislead any agent reading it.

**Fix**: Re-scope T09 step 5 to "Append the PR number to the active branch's row in INDEX.md" only. Add a new step (or instruct in §Files / Allowed planning) for the bulk update — archive the closed PR #212 entry; set active-plan row to the new branch — to land in the docs(planning) commit BEFORE T01 fires.

**Severity**: PASS-WITH-FIX. Coherence-of-state issue, not methodology.

## §Notes for the executor

- **N1** — The plan's stated insertion point for the new constants ("line ~107, just before `POST_OUTCOME_FORBIDDEN_TOKENS`") is actually between line 107 (which is `REJECTED_HISTORY_TEMPORAL_ANCHOR = "started_at"`) and the POST_OUTCOME_FORBIDDEN_TOKENS comment lead-in at line 109. Insert in that gap.
- **N2** — The plan's "Line 486" replacement rewrites the entire 4-line comment block (lines 485–488). Replace lines 485–488 in their entirety; do not replace only line 486 in isolation.
- **N3** — The numeric check rejects `"inf"`, `"nan"`, `"+1e3"`, `" 5 "`, `"1_000"`. Even tokens it doesn't catch (`"0x10"`, `""`) are caught by the controlled-vocabulary check downstream.
- **N4** — Plan T02b test 6 expects "V-7" failure on a row with `prediction_setting="blocked_or_deferred"` AND `status="allowed"` AND `cold_start_handling="blocked"`. Trace: conjunction fails (status wrong), else-branch demands `"blocked" in COLD_START_GATE_VOCAB` — false, V-7 fires with "expected one of [G-CS-1..G-CS-6]". Correct.
- **N5** — Plan T02b test 7 sets `prediction_setting="pre_game"` AND `status="allowed"` AND `cold_start_handling="blocked"`. Conjunction fails; else-branch demands G-CS-N; `"blocked"` not in vocab; V-7 fires correctly.
- **N6** — The symmetric mismatch (a non-blocked-or-deferred row with `status="blocked_until_additional_validation"` and `cold_start_handling="blocked"`) would also fail at V-7 (vocabulary branch). The plan does not test this; non-blocker; fold into a hygiene PR if desired.
- **N7** — When updating the fixture per F1, the existing `test_v3_blocked_family_wrong_status_fails` and `test_v3_missing_blocked_family_fails` will continue to pass because V-3 fires before V-7 in the orchestrator order (V-1 base, V-1 strict, V-2, V-3, V-4, V-5, V-6, V-7). Order matters; confirmed safe.
- **N8** — The current `_row()` helper has hard-coded `"cold_start_handling": "G-CS-1"`. To allow F1, parameterize the helper (cleaner) or set `cold_start_handling="blocked"` post-construction in the fixture.
- **N9** — Plan T08 step 1 confirmed: `pyproject.toml` line 3 currently reads `version = "3.48.0"`. Bump path is mechanical.
- **N10** — Plan T08 CHANGELOG mechanics: `[Unreleased]` exists at line 12 and is empty (after PR #212's roll-up). Substitution is clean.

## §Acceptance for plan-side close

This plan is approved for execution after the following are applied to `planning/current_plan.md`:

1. **F1** — Fixture update is added to T02b's exact operations. Either parameterize the `_row()` helper to accept `cold_start_handling`, or add a post-construction loop in the fixture to overwrite the three carve-out rows' `cold_start_handling` to `"blocked"`. Drop the inaccurate §Verification §2 claim that the fixture's 7 rows already satisfy strict V-7.
2. **F2** — `except (ValueError, TypeError)` in V-7 numeric-check spec.
3. **F3** — Three additions to §Files / Forbidden table (INVARIANTS.md, pyproject.toml/CHANGELOG.md during T01–T07, planning/*.md during T07–T08).
4. **F4** — Re-scope T09 INDEX.md update to PR-number append only; bulk INDEX.md update lands in the docs(planning) commit BEFORE T01 fires.

After applying F1–F4, the plan reads accurately and the executor can proceed without surprise. Reviewer-adversarial is NOT needed; no methodology BLOCKER was raised.
