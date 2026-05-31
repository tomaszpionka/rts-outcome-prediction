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
verdict: HOLD-PROCEDURAL
blockers: 0
nits: 6
nits_applied: [NIT-A1, NIT-A2, NIT-A3, NIT-A4, NIT-A5, NIT-A6]
prior_nits_applied: [N-1, N-2, N-3, N-4]
carry_forwards: [A-15, H6, H7]
gate_status: pending-round-2
date: 2026-05-31
amendment_pr: "chore/sc2egset-02-03-01-adjudication-plan-provenance-amendment"
amendment_base_sha: "5764d524a5aa02a3e242485cd949873725b806c5"
v3_predecessor_pr: 278
v3_predecessor_sha: 846a8ece127dd9b4c119f226008969019d7ddd8e
v1_predecessor_pr: 276
v1_predecessor_sha: 37c3a8855af038bd1bd4eefbdbd03497da323d47
adjudication_direct_rejected: true
branch_model: "Layer-2 lands on NEW branch feat/sc2egset-02-03-01-temporal-adjudication-execution"
---

# Reviewer-Adversarial Critique — Round 1 Amendment (02_03_01 ADJUDICATION Layer-1 Plan)

## Round 1 Amendment verdict

**Verdict: HOLD-PROCEDURAL — substantive 0 BLOCKERs, 6 NIT-A fixes applied inline.** This critique file documents the Round 1 reviewer-adversarial findings that prompted the chore-class amendment PR (chore/sc2egset-02-03-01-adjudication-plan-provenance-amendment). All 12 fixes (6 planner Fixes 1-6 + 6 reviewer NIT-A1..NIT-A6) have been applied inline to `planning/current_plan.md` in this amendment.

The core methodological finding: the merged plan (PR #279, base SHA `5764d524`) declared only a 7-column CSV schema for the adjudication decision artifact. Thesis-grade artifact provenance requires SHA-pin columns for auditable byte-stability evidence linking the decision CSV rows to the exact predecessor artifact bytes and validator module bytes used during adjudication. This is the CSV provenance BLOCKER resolved by Fix 1 + NIT-A1.

**Round 1 of 3** (cap per `feedback_adversarial_cap_execution.md`). Round 2 triggers on the materialized amended plan text for file:line APPROVE/APPROVE-WITH-NITS verdict. Round 2 will verify all validation checks including G12-G17 (new gate predicates introduced by the amendment).

## What was verified (Round 1 Amendment basis)

- PR #279 merged at master `5764d524a5aa02a3e242485cd949873725b806c5` — amendment base SHA confirmed.
- PR #276 (V1 scaffold) at master `37c3a8855af038bd1bd4eefbdbd03497da323d47` — still present.
- PR #278 (V3 scaffold) at master `846a8ece127dd9b4c119f226008969019d7ddd8e` — still present.
- A-12 in merged plan: 7-column CSV only — CSV provenance BLOCKER confirmed.
- Q4: "eligible_for_phase02_now / eligible_with_caveat" present but no literal 9-category list — NIT-A2 confirmed.
- `.validate()` shorthand used at plan lines ~205, ~207, ~462 — NIT-A3 confirmed.
- No halt-priority chain enumeration; H7a/H7b not split — NIT-A4 confirmed.
- No ordering hazard guard (outputs dir vs preflight); no post-emission closure — NIT-A5 confirmed.
- H7 grep target list: `.ipynb` absent (`.py` only for notebook target) — NIT-A6 confirmed.
- All prior N-1..N-4 fixes confirmed present in merged plan.
- A-15 carry-forward verbatim confirmed present.
- H6 + H7 carry-forwards verbatim confirmed present.
- A-16 PR-self-archive forbidden confirmed present.
- Q8 syntactic-only confirmed no empirical AoE2 transferability claim.
- PHASE_STATUS Phase 02 `in_progress` / Phase 03 `not_started` — confirmed unchanged.

## NITs surfaced and applied (Round 1 Amendment)

- **NIT-A1 (CSV provenance BLOCKER resolution; paired with Fix 1):** A-12 declared only 7 columns. Thesis-grade artifact provenance requires SHA-pin columns for auditable byte-stability. Applied inline: A-12 expanded to 16-column minimum. 9 SHA-pin columns added with precise labels (`v1_validator_module_sha256`, `v3_validator_module_sha256` — not generic `v1_sha` / `v3_sha`) and hex-literal values for the 7 fixed-artifact SHAs (4 parent artifacts + 2 CROSS specs + tracker eligibility CSV). V1 and V3 module SHAs are computed at execution time via `hashlib.sha256` and embedded in EVERY row. File Manifest CSV row updated to reflect 16-column schema. G13 gate predicate added.

- **NIT-A2 (Q4 9-category literal list; paired with Fix 2):** Q4 asserted eligible families from the CSV but did not provide a literal list of the 9 source_event_family categories. Applied inline: Q4 now contains the literal sorted list per direct enumeration of tracker_events_feature_eligibility.csv column 2: PlayerSetup, PlayerStats, UnitBorn, UnitDied, UnitInit/UnitDone, UnitOwnerChange, UnitPositions, UnitTypeChange, Upgrade. MD §6 cross-reference now stated as 15-family (one row per CSV row). No "not 5" hedge needed (literal enumeration is self-sufficient). G14 gate predicate added.

- **NIT-A3 (actual repo symbols; paired with Fix 3):** `.validate()` shorthand was used in T02, Q7, A-4, and A-5 — no actual importable repo symbols. Applied inline: ALL `.validate()` occurrences replaced with actual repo symbols: `validate_predecessor_artifact_provenance(repo_root)` (V1, returning `ProvenanceCheckResult`) and `validate_temporal_discipline(repo_root)` (V3, returning `TemporalDisciplineCheckResult`). Adjudicator main entrypoint declared: `validate_temporal_feature_grid_adjudication(repo_root: Path) -> AdjudicationResult`. Q7 binding text corrected to use actual entrypoint names. `grep -F '.validate()' planning/current_plan.md` now returns 0 matches. G15 gate predicate added.

- **NIT-A4 (9-step halt chain; paired with Fix 4):** No halt-priority chain was enumerated; H7 was a single undivided predicate. Applied inline: 9-step halt-priority chain (H0 through H7b) added to §Gate Condition with first-failure-wins semantics. H7 split into H7a (forbidden output dir paradox guard, binding V1.H6 + V3.H5) and H7b (PR-self-archive forbidden, binding A-16). G16 gate predicate added.

- **NIT-A5 (ordering hazard + post-emission closure; paired with Fix 5):** No explicit sequence guarded the outputs-dir-before-preflight ordering hazard; no post-emission closure was declared. Applied inline: Adjudication sequence (8 steps) added to T02. Outputs directory creation (step 5) explicitly gated on preflight PASS (steps 1-3 completed). Post-emission closure at step 8: "return AdjudicationResult; no further writes (no research_log, no status YAML, no spec edits)". G12 gate predicate added.

- **NIT-A6 (.ipynb in H7 target list; paired with Fix 6):** H7 grep target list included `02_03_01_adjudication.py` but not `02_03_01_adjudication.ipynb`. The notebook executes the adjudicator and could contain empirical AoE2 transferability claims in cell outputs or markdown cells. Applied inline: H7 target list extended to 5 files, explicitly including `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_adjudication.ipynb`. G17 gate predicate added.

## Blockers

None (the CSV provenance gap was BLOCKER-class methodology but resolved by Fix 1 + NIT-A1 inline in this amendment; no outstanding blockers remain at amendment commit).

## Methodological findings

**CSV SHA-pin provenance is thesis-grade requirement.** A 7-column decision CSV without SHA-pin columns cannot provide auditable byte-stability evidence for the thesis record. The reviewer-adversarial flagged this as a BLOCKER-class gap: even if the artifacts exist on disk, without embedded SHA-pin columns there is no machine-verifiable link between the decision record and the exact predecessor artifact bytes used during adjudication. The 9-column SHA-pin extension (4 parent + V1 module + V3 module + 2 CROSS specs + tracker CSV) provides this link for every row in the decision CSV.

**V1/V3 module SHA precision matters.** Using `v1_validator_module_sha256` and `v3_validator_module_sha256` (NIT-A1) rather than generic `v1_sha` / `v3_sha` prevents ambiguity about which artifact the SHA refers to (module file vs Parquet vs test output).

**9-category literal list removes ambiguity.** "9 distinct source_event_family categories per direct enumeration" with the literal sorted list (NIT-A2) is the correct pattern: it is falsifiable (grep the CSV column 2), it does not require the reviewer to independently enumerate, and it binds the plan to a specific verified count without a "not 5" hedge.

**Repo symbol discipline prevents executor ambiguity.** `.validate()` shorthand (NIT-A3) would leave the Layer-2 executor to guess the importable symbol. The actual entrypoint `validate_predecessor_artifact_provenance(repo_root)` with its `ProvenanceCheckResult` return type and the adjudicator main entrypoint `validate_temporal_feature_grid_adjudication(repo_root: Path) -> AdjudicationResult` are unambiguous contracts.

**Halt-priority chain prevents partial-artifact paradoxes.** Without an explicit halt chain (NIT-A4), the adjudicator could create the outputs directory (H7a paradox) or emit partial artifacts before detecting a preflight failure. The 9-step chain with first-failure-wins semantics prevents these paradoxes. H7a (output dir paradox guard) and H7b (PR-self-archive) are distinct halt types requiring distinct handling logic; conflating them in a single H7 would obscure the binding to V1.H6 + V3.H5.

**Ordering hazard guard is execution-time safety.** NIT-A5 enforces that the outputs directory is NOT created until after both preflights pass (step 5 gated on step 3). Without this, a partial-PASS scenario (V1 passes, V3 fails) could leave a directory with no artifacts on disk, which would be indistinguishable from a stale artifact scenario.

**.ipynb is a first-class H7 target.** Jupyter notebooks (.ipynb) can contain empirical AoE2 transferability claims in markdown cells, code cells, or cell outputs. Excluding them from H7 grep (NIT-A6) would leave a falsifier gap. The H7 predicate must cover all 5 targets to be exhaustive.

## Preserved constraints (confirmed present after amendment)

- A-15 cross-game-portable vocabulary: confirmed present.
- A-16 PR-self-archive forbidden: confirmed present with three sub-conditions.
- H6 cross-game-portable vocabulary grep falsifier: confirmed present.
- H7 Q8 syntactic-only guard grep falsifier: updated (NIT-A6) and confirmed present.
- Q1-Q3 family KINDS only, no numerical winners: confirmed present.
- Q8 syntactic-only: confirmed present.
- Q6 non-conflation clause verbatim: confirmed present.
- G1-G11 gate predicates from PR #279: confirmed present and unmodified.
- V1 + V3 module byte-stability: confirmed (no .py files modified in this amendment).
- ROADMAP / STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS / research_log: confirmed absent from diff.
- Phase 03 barred: confirmed.
- Adjudication-direct rejected: confirmed.

## Round 2 gate scope

Round 2 reviewer-adversarial will verify (file:line APPROVE/APPROVE-WITH-NITS):

1. All G1-G17 gate predicates pass (G1-G11 from PR #279 + G12-G17 from this amendment).
2. NIT-A1: `parent_02_01_02_parquet_sha256` + `v1_validator_module_sha256` + `v3_validator_module_sha256` + `cross_02_02_spec_sha256` + `tracker_eligibility_csv_sha256` present in plan.
3. NIT-A1: All 7 hex-literal SHAs present: `24db73fb`, `053900e7`, `831a622c`, `c4b48601`, `86af7923`, `59e32273`, `11bd4b9e`.
4. NIT-A2: Literal list (PlayerSetup, PlayerStats, UnitBorn, UnitDied, UnitInit/UnitDone, UnitOwnerChange, UnitPositions, UnitTypeChange, Upgrade) and "9 distinct source_event_family categories per direct enumeration" present.
5. NIT-A3: `grep -F '.validate()' planning/current_plan.md` returns 0. `validate_predecessor_artifact_provenance(repo_root` and `validate_temporal_discipline(repo_root` each return ≥ 1 match.
6. NIT-A4: H7a and H7b present; H0-H6 each present.
7. NIT-A5: "invoke V1 preflight" + "invoke V3 preflight" + "return AdjudicationResult; no further writes" each return ≥ 1 match.
8. NIT-A6: `02_03_01_adjudication.ipynb` present in H7 target list.
9. Scope: exactly 2 files changed (planning/current_plan.md + planning/current_plan.critique.md). No src/, tests/, sandbox/, pyproject, CHANGELOG, planning/INDEX.md, artifacts, specs changed.
10. V1 + V3 modules byte-stable (git diff empty for both).
11. Prior N-1..N-4 + A-15 + H6 + carry-forwards still present and unmodified.
12. No empirical AoE2 transferability claim introduced.
13. No ROADMAP / STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS / research_log changes.
14. Phase 03 barred.
15. A-16 PR-self-archive forbidden preserved.

## Sources / verification trail

- `git rev-parse master` → `5764d524a5aa02a3e242485cd949873725b806c5` (PR #279 merge SHA; amendment base)
- `git rev-parse origin/master` → `5764d524a5aa02a3e242485cd949873725b806c5` confirmed
- `grep -c 'parent_02_01_02_parquet_sha256' planning/current_plan.md` → should return ≥ 1 post-amendment
- `grep -c 'v1_validator_module_sha256' planning/current_plan.md` → should return ≥ 1 post-amendment
- `grep -F '.validate()' planning/current_plan.md` → 0 post-amendment
- `grep -F 'H7a' planning/current_plan.md` → ≥ 1 post-amendment
- `grep -F '02_03_01_adjudication.ipynb' planning/current_plan.md` → ≥ 1 post-amendment
- `grep -F 'invoke V1 preflight' planning/current_plan.md` → ≥ 1 post-amendment
- `grep -F 'return AdjudicationResult; no further writes' planning/current_plan.md` → ≥ 1 post-amendment
