# Critique of planning/current_plan.md (PR #218 — TQ-02 + TQ-01)

**Plan under review:** `planning/current_plan.md` as of commit `d78beb07` (+ mechanical anchor #4 fix applied in the commit that lands this critique).
**PR:** [#218](https://github.com/tomaszpionka/rts-outcome-prediction/pull/218) — `thesis/sc2-tracker-eligibility-section-4-3`
**Base:** `master @ 0a933be6`
**Critique produced by:** `reviewer-adversarial` (Mode A, pre-execution plan critique), `reviewer-deep` (structural correctness + evidence-chain spot-check), parallel dispatch 2026-05-17
**Critique template:** `docs/templates/plan_critique_template.md` (Mode A)

---

## 1. Executive verdict

**PASS-WITH-NOTES (zero blockers).** Both reviewer-deep and reviewer-adversarial returned PASS-WITH-NOTES. The plan is structurally sound, evidence-chain complete on the 4 of 12 spot-checked anchors that bound the load-bearing claims (anchors 1, 2, 5, 6), and methodologically defensible. One mechanical evidence-path fix (anchor #4) has been applied in the commit that lands this critique. The reviewer-adversarial findings are NOT structural fixes to the plan — they are mandatory enhancements to the future T02 writer-thesis dispatch prompt.

**T02 dispatch may proceed** after the user resolves Open Questions Q-A (subsection numbering), Q-B (WRITING_STATUS line 75 inclusion), and Q-D (version-bump policy — already verified by reviewer-deep against the live `.claude/rules/git-workflow.md:14`).

## 2. Critical findings

**None at BLOCKER level.** The plan does not require Phase 02 / Step 02_01_01 closure, does not promote any `blocked_until_additional_validation` row, does not assert leakage-free materialized features, does not invent external citations beyond the pre-authorized `[Bialecki2023]` + `[BlizzardS2Protocol]` bibkeys, and does not bypass `reviewer-adversarial` at the final gate (T04). The forbidden-claim list is the strongest part of the plan.

## 3. Reviewer-deep findings (structural correctness + evidence chain)

| Finding | Severity | Status |
|---|---|---|
| Anchor #4 evidence path cites `sc2egset/reports/INVARIANTS.md:97` which contains PSI prose, NOT Amendment 2 wording. Correct source: `thesis/pass2_evidence/phase02_readiness_hardening.md:294` (verbatim); `thesis/pass2_evidence/methodology_risk_register.md:399, 404` (corroborating); `.claude/scientific-invariants.md:131` (I3 line). | NOTE → mechanical fix | **APPLIED** in the commit that lands this critique. |
| Q-D version-bump status downgrade — live `.claude/rules/git-workflow.md:14` confirms "minor for feat/refactor/docs"; Q-D recommended default `3.52.2 → 3.53.0` is verified. | NOTE | **Resolved** — user may treat Q-D as already verified. |
| Optional: CSV row line numbers (rows 11/12/15 = file lines 12/13/16 with header). | NOTE | Defer — reviewer-deep T03 will catch any drift. |
| Audit TQ-02 F-numbering drift in `phase01_phase02_writing_readiness_audit.md:699` (uses old F8 wording vs. correct F16). | NOTE | Defer — out of PR #218 scope; future audit-file repair. |

Reviewer-deep verdict: **PASS-WITH-NOTES.** All 4 spot-checked anchors (1, 2, 5, 6) verified empirically. PR diff scope is only `planning/current_plan.md`. No forbidden file touched. No thesis prose touched.

## 4. Reviewer-adversarial Mode A findings (methodology defensibility)

The reviewer-adversarial findings are **mandatory enhancements to the T02 writer-thesis dispatch prompt**, not structural plan fixes. They must be folded verbatim into the dispatch prompt before T02 fires.

### 4.1 Methodology defensibility per examiner scenario

| Scenario | Verdict | Risk |
|---|---|---|
| **A** — examiner asks "if tracker features are never pre-game, why is `slot_identity_consistency` in the eligibility CSV at all?" | **CONCERN** | The CSV `status_in_game_snapshot` for row 14 is `eligible_for_phase02_now`, the same value as 4 model-input rows. The new §4.3.3 must explicitly state that the `eligible_for_phase02_now` column is a *semantic eligibility* classification, not a *model-input* classification, and that the `notes_for_phase02` field distinguishes the 1 sanity-gate row from 4 model-input rows. |
| **B** — examiner asks "what's the difference between `eligible_for_phase02_now` and `eligible_with_caveat`?" | **PASS** | Required-claim #5 enforces the 5+7 partition and the "must contrast" list at T02 step 4 forces a contrast against `closed`. The dispatch should also note that `eligible_with_caveat` can be defensibly characterized as "eligible *under* the recorded per-row scope/caveat," not as a weaker eligibility tier. |
| **C** — examiner asks "why are 3 rows blocked? What changes when they become unblocked?" | **CONCERN** | All 3 blocked rows have `planned_for_phase02 = no` from the outset; the plan's framing "15 candidate tracker families: 12 planned-yes + 3 blocked" risks an examiner reading it as "3 *planned* families were blocked at validation time" when the on-disk truth is "3 candidate families were marked not-planned during V3/V4/V5/V6 because the source-confirmation gates failed." The dispatch must clarify this. |
| **D** — examiner asks "what does GATE-14A6 actually gate? Why `narrowed` not `closed`?" | **PASS** | Required-claim #2 mandates both the affirmative `narrowed` AND the negative `NOT closed`. Required-claim #8 mandates citing `full_tracker_scope_closed_predicate_satisfied = false`. Risk: `methodology_risk_register.md:399` uses "GATE-14A6 closed to `narrowed`" which is semantically loaded; the writer-thesis brief should explicitly forbid the "closed to narrowed" phrasing surface. |
| **E** — examiner asks "how does this interact with Phase 02 leakage audit?" | **PASS** | Required-claims #11/#12 + the "must cite" list item for `02_01_leakage_audit_protocol.md` force the writer to embed the non-supersession statement. Residual concern: the dispatch should require the writer to distinguish *semantic* eligibility validation from *column-level* leakage audit. |

### 4.2 Claim-surface refinements (mandatory for T02 dispatch prompt)

1. **Claim #2 (`narrowed`, NOT `closed`) — sharpen against the "closed to narrowed" phrasing.** Prefer the structurally equivalent *"GATE-14A6 outcome: `narrowed`; not `closed`"*; forbid the surface phrasing *"gate zamknięto"* / *"gate is closed"* without the explicit suffix.
2. **Claim #5 (5+7 partition).** The writer-thesis must plant one sentence stating that the 7 `eligible_with_caveat` per-row caveats are *heterogeneous in nature* (referencing the CSV `caveat` column as the per-row source of truth).
3. **Claim #7 (`slot_identity_consistency` sanity gate).** Writer-thesis must state explicitly that this row is the only `eligible_for_phase02_now` row whose `notes_for_phase02` flags it as non-model-input.
4. **Claim #8 (`full_tracker_scope_closed_predicate_satisfied: False`) — keep verbatim.** The CSV-side predicate name has examiner-defensibility value precisely because it is a machine-readable field; require it appear verbatim or in close Polish paraphrase.
5. **Required-claim #11 (non-supersession of leakage-free claim).** Require *constructive* phrasing — *"semantic eligibility validation under Step 01_03_05 does NOT substitute for column-level leakage audit under CROSS-02-01-v1.0.1; the latter remains mandatory at materialization"* — not implicational phrasing.
6. **Implicit forward-promise risk.** Add to Halt condition HALT-1: writer-thesis must include a `Cited-as-of-SHA` comment in the new §4.3.3 referencing the master @ `0a933be6` SHA.

### 4.3 Additional forbidden claims (mandatory for T02 dispatch prompt)

The existing 12-row forbidden-claim table is sound. Add:

- **F-new-13 (verb-level hedge-then-overclaim).** Forbid the patterns *"validates"*, *"demonstrates"*, *"proves"*, *"shows that"* in any sentence whose subject is Step 01_03_05 or GATE-14A6. Permit *"is consistent with"*, *"indicates that"*, *"supports"*, *"records"*.
- **F-new-14 (causality leak).** Forbid any sentence framing Step 01_03_05 results as causing or implying *future* model behavior (e.g., *"ponieważ Krok 01_03_05 zwalidował 12 rodzin, modele będą w stanie..."*). Permit only *forward-bounded* phrasing.
- **F-new-15 (in-game-snapshot ≠ in-game-state).** Forbid the claim that any tracker feature is an *"in-game state"* feature. The artifact's terminology is `status_in_game_snapshot` — a *snapshot* at a cutoff loop, NOT continuous state.
- **F-new-16 (eligibility CSV as feature catalog).** Forbid the claim or implication that `tracker_events_feature_eligibility.csv` is the *feature catalog*. The catalog is the Phase 02 §02_01 registry artifact, a different document. The eligibility CSV is a *classification of candidate families*, not a feature inventory.
- **F-new-17 (RISK-21 wording transplant).** Forbid verbatim transplant of the `methodology_risk_register.md:404` wording recommendation into §4.3.3. That paragraph is an English template for the risk register, not Polish prose for the methodology chapter.

### 4.4 Envelope-tightening recommendations for T02 writer-thesis dispatch

1. **Coupling rationale defended in PR body** — the dispatch should include a one-sentence rationale at the top of the PR body cover: *"§4.3.2 stale paragraph + new §4.3.3 share a single evidence base; splitting would leave §4.3.2 with a dangling forward-reference for one PR cycle."*
2. **Subsection numbering Q-A: recommend hard-binding to (a) `### 4.3.3` + renumber AoE2 → `### 4.3.4`.** Option (b) (embedded prose block) is examiner-vulnerable; forbid it. Option (c) re-opens the §4.3 hierarchy.
3. **WRITING_STATUS Q-B: recommend YES, with corrected wording.** Line 75 (verified) says *"§4.4 in-game feature subsection CANNOT reach FINAL status until SC2 `tracker_events` semantic validation executes (Step 01_03_05, not yet scheduled)."* The repair must replace *"Step 01_03_05, not yet scheduled"* with *"Step 01_03_05 complete 2026-05-05; GATE-14A6 outcome `narrowed`. The §4.4 subsection's FINAL status remains gated by Phase 02 materialization + CROSS-02-01-v1.0.1 audit, not by Step 01_03_05 alone."* — DO NOT over-correct toward "§4.4 unblocked."
4. **Bibkey constraint: `[BlizzardS2Protocol]` placement.** Verify the bibkey's first appearance in Chapter 4 before adding a new citation; if it already cites at line ~25 or ~222, the new §4.3.3 should reference it on a sub-claim (e.g., *"tracker events introduced in protocol version 2.0.8 per `[BlizzardS2Protocol]`"*) rather than at the same provenance locus.
5. **Adversarial round cap definition (T04).** Define "round" as one full pass over the new §4.3.3 prose (not just the changed sentences); partial-pass review can otherwise infinitely chase tail-fixes.
6. **CHANGELOG block phrasing (T05).** Phrase the CHANGELOG entry as a *user-readable description of the methodology change* (e.g., *"§4.3.3 (new): SC2 tracker eligibility framing; §4.3.2 paragraph repair (Step 01_03_05 complete; GATE-14A6 outcome `narrowed`)"*).
7. **Mode-C reviewer-adversarial scope (T04) — add sentence-level surface check.** "Does the prose introduce a sentence that an examiner could read as upgrading `narrowed` to `closed`?" Examiners read for upgrade in meaning, not in token.

## 5. Sign-off

**T02 dispatch may proceed** after the user resolves:

- **Q-A** (subsection numbering): recommend binding to `### 4.3.3` + renumber AoE2 → `### 4.3.4` (the plan's recommended default; option (b) introduces examiner-visible structural hedging).
- **Q-B** (WRITING_STATUS line 75): recommend YES, with the corrected wording specified in §4.4 item 3 above.
- **Q-D** (version-bump policy): **VERIFIED** — the plan's assumption (3.52.2 → 3.53.0 minor) matches `.claude/rules/git-workflow.md:14` per reviewer-deep; no further user resolution required.

**Mandatory folds into the T02 writer-thesis dispatch prompt:**

1. The 5 additional forbidden claims F-new-13 through F-new-17 (§4.3 above).
2. The 6 claim-surface refinements (§4.2 above).
3. The 7 envelope-tightening notes (§4.4 above).
4. Explicit clarification that the 3 blocked rows have `planned_for_phase02 = no` (Scenario C).
5. Explicit clarification that `slot_identity_consistency` is the only sanity gate among 5 `eligible_for_phase02_now` rows (Scenario A).
6. Hard prohibition on the "closed to narrowed" phrasing surface (Scenario D).

Open Question Q-C (V3 fixed-point divide-by-4096 surface) is correctly left to writer-thesis discretion. Open Question Q-E (table vs prose) is correctly left to writer-thesis discretion within the expected-length envelope.

The plan respects the canonical audit §10–§12 routing as the authoritative source. The plan does not overclaim coverage of PR #216 (provisional registry) or PR #217 (writing audit) — it correctly scopes itself to TQ-01 + TQ-02 only, deferring TQ-03 (Phase 02 registry methodology §4.5), TQ-04 (EsportsBench harmonization), and TQ-05 (aoestats CSV row-count) to future PRs.

## 6. Relevant file paths (for parent / writer-thesis dispatch persistence)

- `/Users/tomaszpionka/Projects/rts-outcome-prediction/planning/current_plan.md` — the amended plan with anchor #4 fix.
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/planning/current_plan.critique.md` — this file.
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/thesis/chapters/04_data_and_methodology.md` — T02 target; lines 324–333 are the §4.3.2 / future §4.3.3 scope.
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/thesis/WRITING_STATUS.md` — line 75 is the GATE-14A6 sentence verified; conditional on Q-B = YES.
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv` — 15-row contract; load-bearing.
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/01_03_05_tracker_events_semantic_validation.md` — lines 10–16 define `narrowed` / `closed` predicates; load-bearing.
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/thesis/pass2_evidence/phase02_readiness_hardening.md:294` — Amendment 2 verbatim wording (corrected anchor #4 source).
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/thesis/pass2_evidence/methodology_risk_register.md:399,404` — RISK-21 corroborating; **English template, NOT for verbatim Polish transplant** (F-new-17).
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/.claude/scientific-invariants.md:131` — I3 source ("No feature for game T may use information from game T or later").

---

**Status:** Critique complete. Parent session halts for user approval before T02 (writer-thesis) dispatch.
