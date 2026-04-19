# Adversarial Review — planning/current_plan.md (Pass 1)

**Plan:** `planning/current_plan.md` (Phase 01 Decision Gates, 01_06 bundled PR)
**Phase:** 01 / Pipeline Section 01_06 (all 3 datasets)
**Category:** A (science)
**Date:** 2026-04-19
**Branch:** `feat/phase01-decision-gates-01-06`
**Reviewer:** reviewer-adversarial (pre-execution, methodology adversary)

## Verdict: **REVISE BEFORE EXECUTION**

Three BLOCKERs (§4.3 row missing in WRITING_STATUS.md; sc2egset "Role: TBD" flag missing; retroactive 01_05_09 insertion violates PIPELINE_SECTION_STATUS derivation chain) will cause either visible verification failures or silent misedits during execution. Three MAJORs (cross-dataset rollup under-specification; verdict taxonomy honesty; role-assignment dimension gap) will land methodology issues that a thesis examiner can falsify at defence.

All fixes are scoped to the plan document itself and require no prerequisite data work.

## Lens assessments

- **Temporal discipline:** SOUND — 01_06 consumes completed 01_01–01_05 artifacts only; the plan's Assumption explicitly forbids re-running analyses.
- **Statistical methodology:** AT RISK — T08 cross-dataset rollup does not specify how three heterogeneous ICC scales (0.0463 / 0.003013 / 0.0268) are reconciled. T01 §3 asks for "role-assignment criteria" but does not name metrics.
- **Feature engineering:** SOUND (in scope) — no new feature computation in 01_06.
- **Thesis defensibility:** WEAK — §4.3 unblock claim lands against a non-existent row; role-assignment dimension set not enumerated; retroactive step insertion not reconciled with status-chain invariant.
- **Cross-game comparability:** AT RISK — T08 role assignment is prose rather than falsifiable evidence.

## BLOCKERS

### BLOCKER 1 — Thesis §4.3 row referenced in plan does not exist in WRITING_STATUS.md

- **Location:** plan Scope (line 52), Problem Statement (line 111), Gate Condition (line 827), T12 step 1.
- **Evidence:** `grep -n "§4\.3" thesis/WRITING_STATUS.md` → **No matches found**. Chapter 4 rows present: §4.1 (+§4.1.1), §4.1.2, §4.1.3, §4.1.4, §4.2.1, §4.2.2, §4.2.3, §4.4.4, §4.4.5, §4.4.6. No §4.3 row.
- **Why load-bearing:** T12 verification gate ("§4.3 row = DRAFTABLE") cannot pass. An executor performing a row-flip edit on a non-existent row either no-ops or writes to the wrong row silently.
- **Fix:** resolve row identity before execution. Either (a) rename T12's target to the actual Chapter 4 row(s) whose "Feeds from" or flags depend on 01_06 (likely §4.1 line 64 which explicitly notes "sections 01_05 (Temporal & Panel EDA), 01_06 (Decision Gates) deferred"), or (b) add the missing §4.3 row to WRITING_STATUS.md explicitly in T12's file scope.

### BLOCKER 2 — sc2egset ROADMAP has no "Role: TO BE DETERMINED" flag

- **Location:** T02 Instructions Step 3.
- **Evidence:** `head -25 src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` returns headers but no "Role:" or "TO BE DETERMINED" blockquote. Contrast with aoestats line 12 and aoe2companion line 12 which both carry `> **Role: TO BE DETERMINED.**`. sc2egset was authored without this flag.
- **Why load-bearing:** T02 says "Update ... Role: TBD flag" — but there is no flag to update. Executor either aborts or inserts a block in an ad-hoc position.
- **Fix:** T02 must either (a) instruct executor to *create* the Role block in sc2egset (specify insertion location and content, matching aoestats/aoe2companion layout), or (b) document sc2egset's role is asserted only in the cross-dataset rollup (skipping the per-dataset ROADMAP flag) with justification for divergence.

### BLOCKER 3 — Retroactive 01_05_09 insertion regresses PIPELINE_SECTION_STATUS derivation mid-PR

- **Location:** T04 / T07 / T09.
- **Evidence:** PIPELINE_SECTION_STATUS.yaml header declares `Pipeline section is complete when ALL its steps are complete`. Adding a `not_started` 01_05_09 step in T04 forces aoe2companion 01_05 to regress from `complete` to `in_progress`. Plan Gate Condition asserts end-state but plan does not sequence the transaction.
- **Why load-bearing:** Derivation-chain invariant violated at T04 completion. Mid-PR inconsistency.
- **Fix:** either (i) make T04 and T07 atomic (single task adds 01_05_09 + completes it inline), (ii) write 01_05_09 directly as `in_progress` in T04 with explicit log comment, or (iii) document that PIPELINE_SECTION_STATUS is refreshed atomically only in T09 and is stale between T04 and T09 — accept tolerated transient inconsistency explicitly.
- **Secondary concern:** **sc2egset** also lacks a declared 01_05_09 step but has `decision_gate_sc2egset.md` on disk without a Step owning it. If 01_05_09 symmetry is load-bearing, fix both (add retroactive 01_05_09 to sc2egset too), not just aoe2companion.

## MAJORS

### MAJOR 1 — T08 cross-dataset rollup specification is too shallow

- **Location:** T08 Instructions §1–§4, T01 §3.
- **Gap:** T08 §3 "Cross-dataset I8 compliance" is prose ("Which cross-checks are permitted"), not a method. T01 §3 asks for role-assignment criteria but names no metrics. A defensible T08 requires:
  - Quantitative comparison matrix (ICC, PSI, survivorship rates) with per-metric "comparable yes/no" annotation
  - Named criterion in T01 §3 for why 30.5M matches + rename-stable profileId qualifies aoe2companion as PRIMARY population-scale
  - Falsifier: what empirical state would force a role re-assignment?
- **Why load-bearing:** T08 is the load-bearing I8 artifact. An examiner opens it first.
- **Fix:** T01 §3 enumerates 2–4 comparable metrics + decision criterion; T08 copy-cites them by value.

### MAJOR 2 — Verdict taxonomy conflates "defence residuals" with READY_FULL

- **Location:** T01 §2.
- **Gap:** sc2egset has 5+ known limitations (uncohort-filtered PSI B2 fix, ICC INCONCLUSIVE 0.046 [0.006, 0.085], tournament-only population, I8 PARTIAL, 2023-Q3 duration drift |d|=0.544) yet predicted READY_FULL. aoe2companion has ICC FALSIFIED 0.003, I2 PARTIAL (rename rate 2.57% PARTIAL in perpetuity), 342 clock-skew rows retained — predicted READY_FULL. Taxonomy collapses "has PARTIAL-status invariants but no BLOCKER" into READY_FULL.
- **Why load-bearing:** Examiner: "Why is sc2egset 'ready if 5 items are still open in its decision memo?"
- **Fix:** add middle tier **READY_WITH_DECLARED_RESIDUALS** between READY_FULL and READY_CONDITIONAL. Or relabel all three datasets READY_CONDITIONAL with explicit flip-predicates.

### MAJOR 3 — Role-assignment dimension set not enumerated

- **Location:** T01 §3 ("One dataset can be PRIMARY on one dimension and SUPPLEMENTARY on another") — acknowledged but not enumerated.
- **Gap:** Plan introduces at least 3 dimensions (in-game event / population-scale / patch-level). Reviewer questions:
  - How many dimensions total? Skill-signal dimension? Patch-heterogeneity?
  - If sc2egset is SUPPLEMENTARY population-scale, is it also SUPPLEMENTARY on observed-scale ICC comparison?
  - Role hierarchy for the headline Phase 05 metric (AUC / Brier)?
- **Why load-bearing:** Cross-game comparability (I8) silently accumulates asymmetries.
- **Fix:** T01 §3 enumerates dimension set explicitly (3–5 dimensions). T08 §2 populates matrix (datasets × dimensions).

## MINORS

1. **T06 file-scope typo** — plan line 502 contains an inline "correction" noting a path that should be under aoestats not aoe2companion. Remove the self-correction; keep only the correct line.
2. **T10 no-op audit trail missing** — conditional task writes no bytes if zero transitions. Add `.github/tmp/01_06/t10_noop.log` with evidence.
3. **Iterative execution not enforced** — T05/T06/T07 declare iterative mode but have no mid-sequence checkpoint. Add explicit pause/resume handoff ("after 01_06_01 completes, executor reports hypothesis-falsifier outcome to parent before proceeding to 01_06_02").
4. **T01 spec semver semantics unclear** — 01_05_preregistration.md had 5 semver bumps in one day. Clarify whether mid-execution amendments are expected or forbidden.
5. **.github/tmp/01_05/ purge scope** — correctly scoped to 6 files + directory; parent `.github/tmp/` preserved. No issue.

## Examiner's questions this plan should anticipate

1. **"Why is aoe2companion PRIMARY population-scale when its ICC is 0.003 (FALSIFIED skill-signal)?"** Cohort size ≠ signal strength. The thesis's core prediction task requires between-player variance. Labelling a 0.003-ICC dataset PRIMARY on any ML-relevant dimension risks a scope misclaim. T08 must either name the PRIMARY-population-scale dimension as purely sample-size and state the consequence ("we defer skill-signal analysis to sc2egset/aoestats"), or re-rank.
2. **"Where is the sc2egset in-game feature set defined?"** Phase 02 placeholders are empty. The PRIMARY-in-game role writes a check Phase 02 must cash later.
3. **"Is T08 §3 I8 compliance evidence-bound or rhetorical?"** As worded, it's rhetorical. Defending Chapter 4 will require the cross-check enumeration.
4. **"Why do three datasets have ~5 amendments to a 'locked' spec in one day?"** (pre-01_06 thesis-defence findings driving v1.0.2→v1.0.5). Not explained.

## Methodology risks (summary)

1. **BLOCKER** — §4.3 row does not exist; T12 gate cannot pass.
2. **BLOCKER** — sc2egset ROADMAP "Role" flag missing; T02 cannot execute as worded.
3. **BLOCKER** — Retroactive 01_05_09 violates status-chain unless T04/T07 atomic or T09 end-state-only. Symmetry: sc2egset also lacks 01_05_09 step.
4. **MAJOR** — T08 under-specified; risk of 3-row table + role paragraph failing examiner scrutiny.
5. **MAJOR** — Verdict taxonomy collapses residuals into READY_FULL; honesty cost at examination.
6. **MAJOR** — Role-assignment dimensions not enumerated; I8 comparability risk.
7. **WARNING** — Iterative execution is declared, not gated; drift toward batch execution not monitored.
8. **WARNING** — aoestats READY_CONDITIONAL flip-predicate couples F1 + I5-transition but aoestats INVARIANTS.md §5 notes I5 requires W4 (different workstream). If F1 lands without W4, I5 may not actually flip.

## Recommended next action

Per the 3-round adversarial cap symmetric (memory `feedback_adversarial_cap_execution.md`): this is round 1. Planner should revise T01, T02, T04/T07/T09 atomicity, T08 §2–§3 specificity, T12 target-row identity before dispatching any executor. One more round of adversarial review is warranted before execution, especially on BLOCKER 3's PIPELINE_SECTION_STATUS ordering.

---

# Pass 2 (post-revision) — 2026-04-19

## Verdict: **REVISE BEFORE EXECUTION (round 2 of 3)**

All Pass 1 BLOCKERs genuinely resolved at claim level. Pass 1 MAJORs all resolved with residuals. But the mechanism chosen for Pass 1 BLOCKER 3 introduced new issues that should be closed before execution.

### Pass 1 resolution audit — **all 10 findings RESOLVED**

| Pass 1 Finding | Pass 2 Status |
|---|---|
| BLOCKER 1 (§4.3 phantom) | RESOLVED — T12 targets §4.1/§4.1.3/§4.1.4 Notes cells |
| BLOCKER 2 (sc2egset Role flag) | RESOLVED — T02 creates verbatim block |
| BLOCKER 3 (status-chain regression) | PARTIALLY RESOLVED — see new BLOCKER 1 below |
| MAJOR 1 (T08 under-specified) | RESOLVED — 3×6 matrix + §3 + §4 cross-check enumeration |
| MAJOR 2 (verdict taxonomy) | RESOLVED — 4-tier taxonomy with READY_WITH_DECLARED_RESIDUALS |
| MAJOR 3 (role dimensions) | RESOLVED — 6 dimensions enumerated in T01 §3 |
| MINOR 1 (T06 typo) | RESOLVED |
| MINOR 2 (T10 no-op) | RESOLVED — 30-row audit log required |
| MINOR 3 (iterative execution) | RESOLVED — pause/resume checkpoints per task |
| MINOR 4 (spec semver thrash) | RESOLVED — spec-lock at v1.0 posture |

### New issues introduced by Pass 2 revisions

### BLOCKER 1 (new) — Retroactive 01_05_09 creates Invariant #9 and naming asymmetry

1. **completed_at ambiguity.** T02 does not specify whether sc2egset's retroactive 01_05_09 carries `completed_at: 2026-04-18` (date on existing `decision_gate_sc2egset.md`) or T02 execution date. If executor writes T02 execution date, PR shows a step claiming same-day completion as the labelling PR — anomalous.
2. **Artifact naming divergence.** sc2egset artifact is `decision_gate_sc2egset.md`; aoestats is `01_05_09_gate_memo.md`; aoe2companion T07 output will be `01_05_09_gate_memo.md`. Plan silently accepts this naming asymmetry at the very layer it's trying to symmetrise. Either rename sc2egset or document.
3. **`PIPELINE_SECTION_STATUS.yaml` intentional falsehood.** Plan's "tolerated transient inconsistency" between T04 and T09 means aoe2companion's `PIPELINE_SECTION_STATUS.yaml` at any intermediate commit declares `01_05: complete` while its own header rule ("If this file disagrees with STEP_STATUS.yaml, this file is wrong") is contradicted by the presence of a `not_started` 01_05_09 step. A git-visible intermediate state where a YAML file lies per its own rule.

**Fix options:** (i) rename sc2egset artifact + atomize T04+T07 into one task, or (ii) T04 writes 01_05=in_progress (rederiving correctly), T07+T09 restores.

### MAJOR 1 (new) — D3 "months continuous" undefined

T01 §3 D3 uses "months of continuous cleaned-data" without defining continuous. sc2egset spans 2016–2024 (sparse tournament months); aoe2companion 2020-07→2026-04 (continuous); aoestats 134-month dense period. Under one definition sc2egset wins; under another aoe2companion wins.

**Fix:** T01 §3 D3 must specify SQL pattern (e.g., `COUNT(DISTINCT DATE_TRUNC('month', started)) WHERE match in cleaned table` with minimum density threshold).

### MAJOR 2 (new) — D2 FALSIFIED filter not defined

D2 says "PRIMARY if ICC ≥ 0.01 AND largest; SUPPLEMENTARY otherwise (including any FALSIFIED)". aoestats ICC 0.0268 clears 0.01 threshold but is SUPPLEMENTARY due to FALSIFIED label. But FALSIFIED definition differs across datasets (CI-straddle vs point-estimate-below). Rule unclear.

**Fix:** T01 §3 D2 must articulate two filters explicitly: (1) point estimate ≥ 0.01; (2) verdict NOT FALSIFIED per each dataset's INVARIANTS.md §5 or ICC-artifact `verdict` key.

### MAJOR 3 (new) — D4 co-PRIMARY conflates Branch (i) + Branch (iii)

sc2egset (Branch iii, 12% cross-region migration) and aoe2companion (Branch i, rename-stable) both labelled co-PRIMARY on D4 identity-rigor. Category error: non-equivalent identity problems.

**Fix options:** (a) T08 §3 D4 qualifies co-PRIMARY by sub-dimension ("aoe2companion PRIMARY on rename-stability; sc2egset PRIMARY on within-region rigor"), or (b) split D4 into D4a (rename-stability) and D4b (within-scope rigor).

### MAJOR 4 (new) — D6 in-game-events inflates sc2egset PRIMARY count

D6 is N/A for 2 of 3 datasets, making it not a cross-dataset comparability dimension but a feature flag of one dataset. Inflates sc2egset's apparent PRIMARY count (now 3 of 6: D2, D4 co-, D6).

**Fix:** rename D6 to "Controlled-asymmetry flag (I8 controlled variable)"; state explicitly that PRIMARY on D6 does NOT count toward sc2egset's role-weight in downstream T08 §5 discussion.

### MINOR 6 — Artifact-naming decision required (see BLOCKER 1.2)
### MINOR 7 — T08 §1 verdict table conflicts weakly with Assumption ("Anticipated verdicts are predictions; executor verifies")

## Pass 2 overall

Approximately 6 targeted edits close all remaining gaps: T01 §3 (D2, D3, D4, D6 clarifications), T02 (completed_at + artifact naming), T04/T07/T09 (atomicity or explicit state-lie acknowledgment). Estimated effort: 20–40 minutes planner time, no code. Not a redesign.

Round 2 of 3 complete. Round 3 warranted on the 4 new issues above.

---

# Pass 3 (final, round 3 of 3) — 2026-04-19

## Verdict: **EXECUTE (after surgical amendment landed 2026-04-19)**

Pass 2's 4 issues (BLOCKER 1 retroactive asymmetry + MAJOR 1–4 dimension gaps) all RESOLVED. Pass 3 surfaced 1 new BLOCKER + 1 new MAJOR + 2 MINORs, all addressed by targeted planner amendments completed in the same session (no 4th adversarial round needed per reviewer's Path A recommendation).

### Pass 3 issues and surgical amendments applied

- **BLOCKER 1 (D2 F2 schema mismatch across ICC JSON artifacts)** —
  Fixed: spec §3 D2 F2 now reads from **INVARIANTS.md §5 row for the
  I8 invariant** as the single canonical verdict source, using the
  uniform token set `{HOLDS, PARTIAL, FALSIFIED, DEVIATES}`. The
  per-dataset ICC JSON artifacts (with inconsistent field names and
  value formats) are demoted to evidence status, not filter source.

- **MAJOR 1 (I7 threshold magic numbers)** — Fixed:
  - D2 F1 threshold 0.01 now cited to Koo & Li 2016 JCM §3.1 +
    Cicchetti 1994 (conventional ICC ignorable-variance floor).
  - D3 density floor N=100 now derived from binomial SE bound
    (SE ≤ 5% at N=100 per SE = √(p(1-p)/N) for p=0.5).

- **MINOR 8 (T07 checkpoint 1 atomicity vs pause/resume)** — Fixed:
  checkpoint 1 now explicitly requires a single atomic commit (memo +
  STEP_STATUS + PIPELINE_SECTION_STATUS) before executor pauses for
  parent check-in.

- **MINOR 9 (T12 literal-text matching ambiguity)** — Fixed: T12 Step
  1 instructs executor to **append unconditionally** to each §4.x
  Notes cell regardless of whether the existing text literally
  contains "01_06".

### Pass 2 resolution audit (final)

| Pass 2 Issue | Pass 3 Status |
|---|---|
| BLOCKER 1 (retroactive 01_05_09 asymmetry) | RESOLVED — git-mv + completed_at + T04 honest-state flip + T07 checkpoint 1 atomic restore |
| MAJOR 1 (D3 continuous undefined) | RESOLVED — SQL + density-floor justification |
| MAJOR 2 (D2 FALSIFIED filter undefined) | RESOLVED — F2 reads INVARIANTS.md §5 uniform token set |
| MAJOR 3 (D4 conflation) | RESOLVED — split into D4a/D4b |
| MAJOR 4 (D6 inflation) | RESOLVED — D6 reframed as asymmetry flag only, role tally excludes D6 |

### No further adversarial rounds required

The plan is **cleared for executor dispatch.** 3-round cap exhausted; remaining work is execution, not planning.

Residual non-blocking concerns carried into execution:

1. **D4b 15% threshold** (Pass 3 Examiner Question 3) — not cited in spec but sourced from INVARIANTS.md §2 per-dataset tolerance values. Acceptable deferral; if executor surfaces a challenge, halt + report to parent.
2. **Verdict transitions** — any mid-execution finding that flips an anticipated verdict from READY_WITH_DECLARED_RESIDUALS → READY_CONDITIONAL (or similar) is spec-allowed per T08 §1 "executor may override" clause.
3. **T10 empirical expectation** — zero INVARIANTS.md §5 transitions is the expected outcome; audit log captures the non-events.

Plan is ready for executor dispatch.
