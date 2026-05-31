---
plan: planning/current_plan.md
phase: 02
pipeline_section: 02_03
step: 02_03_01
category: A (feat/)
layer: 1
reviewer: reviewer-adversarial
round: 1
cap: 3
verdict: PROCEDURAL-HOLD
blockers: 0
nits: 4
nits_applied: [N-1, N-2, N-3, N-4]
carry_forwards: [A-15, H6, H7]
gate_status: pending-round-2
date: 2026-05-31
v3_predecessor_pr: 278
v3_predecessor_sha: 846a8ece127dd9b4c119f226008969019d7ddd8e
v1_predecessor_pr: 276
v1_predecessor_sha: 37c3a8855af038bd1bd4eefbdbd03497da323d47
adjudication_direct_rejected: true
branch_model: "Layer-2 lands on NEW branch feat/sc2egset-02-03-01-temporal-adjudication-execution"
---

# Reviewer-Adversarial Critique — Round 1 (02_03_01 ADJUDICATION Layer-1 Plan)

## Round 1 verdict

**Verdict: PROCEDURAL HOLD — substantive 0 blockers, 4 NITs applied inline.** The plan's methodological structure is sound. Both scaffold rungs (V1 PR #276, V3 PR #278) are correctly cited as the prerequisite for adjudication. Q7 (V1+V3 preflight gate) is the critical structural commitment. Q8 (syntactic-only cross-game portability) is correctly scoped. CROSS-02-02 vs CROSS-02-03 role non-conflation (Q6) is correctly declared. Four NITs (N-1 through N-4) were surfaced and applied inline by the executor before commit. Three carry-forwards from PR #277 (A-15, H6, H7) applied verbatim. Branch-model clarification (Layer-2 = NEW branch) applied inline.

**Round 1 of 3** (cap per `feedback_adversarial_cap_execution.md`). Round 2 triggers on the materialized plan text for file:line APPROVE/APPROVE-WITH-NITS verdict. Round 2 will verify all 12 validation checks including N-1 through N-4 grep predicates.

## What was verified (Round 1 basis)

- PR #276 (V1 scaffold) merged at master `37c3a8855af038bd1bd4eefbdbd03497da323d47` — basis for A-1.
- PR #278 (V3 scaffold) merged at master `846a8ece127dd9b4c119f226008969019d7ddd8e` — basis for A-1.
- `validate_temporal_feature_grid.py` (V1) exists at canonical path — basis for A-2.
- `validate_temporal_discipline.py` (V3) exists at canonical path — basis for A-2.
- `adjudicate_temporal_feature_grid.py` does NOT yet exist — adjudicator creates it fresh.
- pyproject.toml `version = "3.89.0"` (post-PR #278) — basis for A-3, target `3.89.0 → 3.90.0`.
- CROSS-02-02-v1.0.1 (LOCKED 2026-05-06) confirmed at `reports/specs/02_02_feature_engineering_plan.md` — §10 G-L-1 through G-L-7 confirmed as inventory source.
- CROSS-02-03-v1.0.1 (LOCKED 2026-05-06) confirmed at `reports/specs/02_03_temporal_feature_audit_protocol.md` — §4 D5/D6/D7 confirmed as audit predicate source.
- tracker_events_feature_eligibility.csv present at canonical path — basis for A-14.
- Q8 syntactic-only scoping correctly declared — no empirical AoE2 transferability claim in plan draft.
- PHASE_STATUS Phase 02 `in_progress` / Phase 03 `not_started` — basis for A-9.
- A-16 PR-self-archive forbidden: present and binding in plan (carry-forward from PR #278 Round 2 BLOCKER remediation).
- Layer-2 branch-model clarification: Layer-2 NEW branch model explicitly declared in §File Manifest.

## NITs surfaced and applied

- **N-1 (Q7 verbatim grep predicates):** §Gate Condition lacked concrete grep predicates that the Layer-2 plan body MUST satisfy for Q7 binding. Applied inline: "Layer-2 plan-text grep falsifier predicates (binding)" subsection added with grep predicates for V1 PASS, V3 PASS, G-L-1 through G-L-7, D5/D6/D7, Invariant I3, and preflight. Failure of any = Q7 is paper-only; halt Layer-2 dispatch.

- **N-2 (Q6 CROSS-02-02 vs CROSS-02-03 non-conflation):** The verbatim non-conflation clause was absent from Q6 and the Q7 narrative. Applied inline: "CROSS-02-02 = source of candidate family inventory; CROSS-02-03 = source of post-selection audit predicate. These are distinct roles." present in §Open Questions Q6, §Literature Context, and §Problem Statement. §Gate Condition G6 binds this as a grep predicate.

- **N-3 (I7 plan-layer enforcement):** §Gate Condition lacked the plan-layer I7 enforcement subsection. Applied inline: "Layer-1 plan-layer I7 enforcement (no concrete numerical winners)" subsection added with grep falsifier. Q1-Q3 explicitly enumerate family KINDS, not winners. G8 gate predicate binds the I7 grep.

- **N-4 (PR-self-archive forbidden; PR #278 Round 2 carry-forward):** A-16 was absent. Applied inline: A-16 verbatim binding present in §Assumptions & Unknowns. T07 annotation forbids Layer-2 self-archive. G10 gate predicate binds A-16 presence.

## Carry-forwards applied verbatim

- **A-15 (cross-game-portable vocabulary; from PR #277 plan):** Present in §Assumptions & Unknowns A-15 with verbatim wording from PR #277.
- **H6 (cross-game-portable vocabulary grep falsifier; from PR #277 plan):** Present in §Gate Condition "Layer-2 falsifier predicates carried from PR #277 plan (binding)".
- **H7 (Q8 syntactic-only guard grep falsifier; from PR #277 plan):** Present in §Gate Condition same subsection.

## Blockers

None.

## Methodological findings

**Q7 V1+V3 preflight as structural gate is correctly positioned.** The adjudicator invoking V1 and V3 as preflight operations before any adjudication logic is the correct structural anchor. Without this, the adjudication could proceed even if the scaffold modules regressed, breaking the ROADMAP `continue_predicate` cascade.

**Q6 CROSS-02-02 vs CROSS-02-03 non-conflation is the key spec discipline concern.** Using CROSS-02-02 §10 for family inventory and CROSS-02-03 §4 for audit predicates are distinct roles. The non-conflation clause prevents a common failure mode where both specs are cited interchangeably, losing the traceability to each spec's authoritative role.

**I7 no-magic-numbers at Layer-1 is the correct deferral pattern.** Layer-1 describes family KINDS (window-type, decay-type, cold-start-type). Winner selection is deferred to Layer-2 materialization. This prevents premature over-specification at the planning layer.

**A-16 PR-self-archive prohibition is correctly binding.** The project-wide honest-lineage rule (from PR #278 Round 2 BLOCKER remediation) is correctly carried forward and applied to the Layer-2 execution PR's INDEX.md edit scope.

**Q8 syntactic-only is correctly enforced.** H7 falsifier covering adjudicator source, test, notebook, and decision MD is more comprehensive than the V3 equivalent (which covered only source and test). The expanded H7 scope is appropriate for an artifact-producing step.

**Adjudication-direct correctly rejected.** Even though both scaffold modules exist in the codebase, the Layer-2 must re-invoke them as preflight gates at execution time. This is the correct enforcement: codebase existence is not sufficient; execution-time invocation is required.

**Layer-2 NEW branch model is correct.** Mirroring PR #275 → PR #276 and PR #277 → PR #278 precedent. 9-file diff (not 11-file) because planning files merge with this Layer-1 PR.

## Round 2 gate scope

Round 2 reviewer-adversarial will verify (file:line APPROVE/APPROVE-WITH-NITS):

1. All 12 validation checks from Step 4 of the Layer-1 materialization protocol.
2. N-1 grep predicates present verbatim.
3. N-2 non-conflation clause present verbatim.
4. N-3 I7 grep falsifier present and the plan itself passes the I7 grep.
5. N-4 A-16 present with all three sub-conditions (Layer-2-archives-only-PR#278+Layer-1, no self-archive, 846a8ece SHA cited).
6. A-15 carry-forward verbatim present.
7. H6 + H7 carry-forwards verbatim present.
8. Branch-model clarification present (9-file, NEW branch, PR #275 → PR #276 + PR #277 → PR #278 precedents cited).
9. Q1-Q3 enumerate family KINDS only, no numerical winners.
10. Q8 syntactic-only preserved.
11. Phase 03 + baselines BARRED.
12. No ROADMAP / STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS / research_log / artifacts / specs / source / tests / notebooks / pyproject / CHANGELOG / planning/INDEX changed.

## Sources / verification trail

- `git rev-parse master` → `846a8ece127dd9b4c119f226008969019d7ddd8e` (V3 PR #278 merge SHA)
- `gh pr view 276 --json mergeCommit` → `37c3a8855af038bd1bd4eefbdbd03497da323d47` (V1 PR #276 merge SHA)
- `grep -E '^version = ' pyproject.toml` → `version = "3.89.0"` confirmed
- `ls src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_feature_grid.py` → exists (V1)
- `ls src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_discipline.py` → exists (V3)
- `ls src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_temporal_feature_grid.py` → does not exist (correct)
- `ls reports/specs/02_02_feature_engineering_plan.md` → CROSS-02-02-v1.0.1 LOCKED 2026-05-06 confirmed
- `ls reports/specs/02_03_temporal_feature_audit_protocol.md` → CROSS-02-03-v1.0.1 LOCKED 2026-05-06 confirmed
- `ls src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv` → exists confirmed
