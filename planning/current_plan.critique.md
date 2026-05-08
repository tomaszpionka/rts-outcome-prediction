# Plan Critique — SC2EGSet Step 02_01_01 Notebook Scaffold

**Reviewer:** reviewer-deep (claude-opus-4-7)
**Date:** 2026-05-07
**Plan:** planning/current_plan.md — phase02/sc2egset-feature-registry-scaffold
**Verdict:** PASS-WITH-FIXES

## Verdict summary

The plan correctly implements lineage sequence step 2 only (notebook scaffold + one validation module), defers steps 3–9, separates the scaffold and release commits, and locks all three open questions to defensible defaults. The 26-row composition (5+6+4+7+1+3) checks out against CROSS-02-02-v1.0.1 §6 and the tracker eligibility CSV (5+7+3=15 confirmed by direct row count). V-1 through V-6 are correctly scoped for a first validation module and the SC2-specific subtleties (slot_identity_consistency reclassification, tracker-never-pre-game, strict-< with details_timeUTC) are honored. The reviewer-deep gate is correctly the default and reviewer-adversarial is correctly conditional. None of the five required fixes are scientific risks — all are mechanical accuracy corrections to the plan text itself.

## Blockers

None.

## Required fixes before execution

1. **§Status — branch existence.** The branch `phase02/sc2egset-feature-registry-scaffold` already exists (carries planning commits `cba28e30` and `bed813e4`). Fix the plan line that states the branch "does not yet exist" to: "The current branch `phase02/sc2egset-feature-registry-scaffold` already exists with two planning-only commits (`cba28e30`, `bed813e4`); execution begins on that branch with the next commit being the scaffold commit."

2. **§Commit Granularity item 1 — HEAD reference.** Plan references HEAD planning commit as `cba28e30` but the actual branch HEAD is `bed813e4` (the second planning commit). Update to reflect HEAD = `bed813e4` so the scaffold commit lands on the correct parent.

3. **§Reviewer Gate — cite the specific carve-out.** The line "No `planning/current_plan.critique.md` required before execution" should cite `.claude/rules/data-analysis-lineage.md` line 24 explicitly: "per `.claude/rules/data-analysis-lineage.md` line 24, this active Phase 02 readiness PR does not invoke reviewer-adversarial upfront; the reviewer-deep critique fulfills the Cat A critique slot for `planning/current_plan.critique.md`."

4. **V-1 — add `dataset_tag == 'sc2egset'` literal assertion.** The 13-column list includes `dataset_tag` but V-1 does not assert its value. Add: "Assert every row has `dataset_tag == 'sc2egset'`" to V-1. This is a single-dataset skeleton; one extra assertion prevents stray multi-dataset rows from passing silently.

5. **§Forbidden Files — expand `reports/specs/02_0*.md` glob.** Name the four locked specs explicitly: `reports/specs/02_00_feature_input_contract.md`, `reports/specs/02_01_leakage_audit_protocol.md`, `reports/specs/02_02_feature_engineering_plan.md`, `reports/specs/02_03_temporal_feature_audit_protocol.md`. Shell glob `02_0*.md` is ambiguous.

## Warnings

**W1.** T05 `git status` check should also explicitly confirm that `pyproject.toml` and `CHANGELOG.md` are NOT staged in the scaffold commit. §Commit Granularity already enforces separation but a belt-and-suspenders check prevents silent drift.

**W2.** T07 "If coverage required new tests, include test file in commit" makes commit scope non-deterministic. Coverage currently sits at ~95%; a test for `validate_registry_skeleton` is almost certainly needed. Recommend making the test file mandatory (not conditional) so commit scope is fixed before execution.

**W3.** T03 cell 3 correctly omits `ARTIFACTS_DIR.mkdir()`. Add an explicit note in the plan: "Deviation from `notebook_template.yaml` `cell_03_paths` (which mandates `mkdir`) — justified because no artifact is produced in this scaffold-only PR."

**W4.** OQ3 resolution should specify that the `Commit` frontmatter field is populated with the *parent* short hash at T03 author time (current HEAD `bed813e4`), not the scaffold commit's own hash (unknown until after `git commit`). Document in T03.

## Notes

**N1.** V-2 split count `5+7+3=15` verified by direct CSV read. Plan claim is exact.

**N2.** V-5: `source_table_or_event_family` in the skeleton may use prefixed form (`tracker_events_raw.UnitBorn`) while the CSV's `source_event_family` column uses bare form (`UnitBorn`). V-5 should use substring or explicit mapping comparison to avoid silent misses due to naming-format mismatch.

**N3.** V-6 should explicitly reject `started_at` as a `temporal_anchor` for `history_enriched_pre_game` rows — `started_at` is the cross-dataset alias; the sc2egset anchor is `details_timeUTC` per CROSS-02-03-v1.0.1 §5.1.

**N4.** OQ2 (`cross_region_fragmentation_handling`) consistent with CROSS-02-02-v1.0.1 §6.2 placement and `allowed_with_caveat` status. Locked correctly.

**N5.** `branch_note` in frontmatter correctly acknowledges non-canonical `phase02/` prefix as project precedent; this is not a TAXONOMY.md amendment.

**N6.** §Status correctly defers Step 02_01_01 STEP_STATUS entry to a subsequent PR.

**N7.** PR #211 IS already merged at master `6e220ad9` — verified. §Status correctly states "Do NOT re-merge PR #211."

## Scope checklist results

| # | Item | Result | Detail |
|---|------|--------|--------|
| 1 | data-analysis-lineage.md compliance | PASS | Implements only sequence step 2; steps 3–9 explicitly deferred in §Scope and §Deferral List. Frontmatter `lineage_sequence_step: 2` confirms intent. |
| 2 | No premature implementation | PASS | T01–T09 gated; planning commits are `docs(planning):` only. |
| 3 | Reviewer gate correctness | PASS | `reviewer_gate: "reviewer-deep"`; reviewer-adversarial conditional on methodology BLOCKER per data-analysis-lineage.md line 24. |
| 4 | Deferred items complete | PASS | CSV/MD artifact, STEP_STATUS.yaml, PIPELINE_SECTION_STATUS.yaml, PHASE_STATUS.yaml, research_log.md, notebook_regeneration_manifest.md all explicitly excluded. |
| 5 | Commit separation | PASS | Planning / scaffold / release are three separate commits with explicit file scope per §Commit Granularity. |
| 6 | Release wrap-up correct | PASS | 3.47.0 → 3.48.0; minor bump; deferred until T08 after T05/T06 pass. |
| 7 | V-1 through V-6 scope | PASS | Six checks correctly scoped; CSV 5+7+3=15 verified; blocked families correct; slot_identity_consistency `sanity_gate_not_model_input` with CSV value preserved; tracker-never-pre-game; strict `<` with `details_timeUTC`. |
| 8 | OQ defaults locked | PASS | OQ1 = `sc2egset.<setting>.<family>`; OQ2 = `history_enriched_pre_game` CONTEXT row; OQ3 = scaffold-creation HEAD short hash, no auto-update. |
| 9 | Branch prefix exception acknowledged | PASS | Frontmatter `branch_note` cites project precedent PRs #209-#211; substantive category A/feat confirmed. |
| 10 | PR #211 treated as already merged | PASS | §Status states "PR #211 is already merged" and "Do NOT re-merge PR #211." master HEAD matches claimed commit. |

## reviewer-adversarial required?

No. No methodology BLOCKER raised. All methodology choices trace directly to locked CROSS specs, the SC2EGSet ROADMAP Step 02_01_01 block, and the tracker eligibility CSV. The data-analysis-lineage.md line-24 carve-out directs that reviewer-adversarial not be invoked unless reviewer-deep raises a BLOCKER.

## Implementation may start?

Yes — after the five Required Fixes are applied to `planning/current_plan.md`. All five are mechanical accuracy fixes to the plan text (branch existence state, HEAD reference, reviewer-gate citation, V-1 literal assertion, forbidden-files glob expansion). None are scientific risks. Once the plan is updated and the fix-commit is on the branch, T01 may start.
