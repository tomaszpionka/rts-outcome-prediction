# Critique of planning/current_plan.md (PR #219 — TQ-03)

**Plan under review:** `planning/current_plan.md` as of commit `7e5157f2`.
**PR:** [#219](https://github.com/tomaszpionka/rts-outcome-prediction/pull/219) — `thesis/phase02-registry-methodology-section-4-5`
**Base:** `master @ f1add6ce`
**Critique produced by:** `reviewer-adversarial` (Mode A, pre-execution plan critique) + `reviewer-deep` (structural correctness + evidence-chain spot-check), parallel dispatch 2026-05-17
**Critique template:** `docs/templates/plan_critique_template.md` (Mode A)

---

## 1. Executive verdict

**PASS-WITH-NOTES (zero structural blockers).** Both reviewers cleared the plan: reviewer-deep returned PASS-WITH-NOTES (4 cosmetic non-blocker follow-ups); reviewer-adversarial returned PASS-WITH-NOTES (10 enhancement findings — 3 CONCERN-rated for T02 prompt, 7 NOTE-rated for FC additions and T04 sentence-surface checks). The plan is structurally complete, evidence-traced (21 anchors all SUPPORTED), and scope-disciplined. TAXONOMY.md correctly remains untouched. STATUS YAML no-touch framing is rigorous (forbids both flips and claims requiring flips). Non-batching lineage discipline upheld. Model routing places Opus on T02 + T04 + T01 reviewers. The 18 forbidden-claim items exceed the dispatch floor of 11.

**T02 dispatch may proceed** after user approves the dispatch-prompt enhancements (6 new FC items FC19–FC24 + 9 envelope tightenings). No replanning required.

## 2. Critical findings

**None at BLOCKER level.** The plan does not require Phase 02 / Step 02_01_01 / Section 02_01 closure; does not promote any of the 3 `blocked_until_additional_validation` tracker rows; does not assert leakage-free materialized features; does not claim AoE2 Phase 02 parity; does not invent external citations beyond `[Bialecki2023]`; does not modify any STATUS YAML, TAXONOMY entry, ROADMAP, or registry artifact; does not bypass reviewer-adversarial at T04.

## 3. Reviewer-deep findings (structural correctness + evidence chain)

| Finding | Severity | Status |
|---|---|---|
| Line-number imprecision in 2 citations: plan line 217 says "aoestats ROADMAP line 1748+" (Phase 02 header; actual "NOT DELIVERED" verbatim at line 1806); plan line 70 says "audit landed on master at `f1add6ce`" (actually PR #218 merge SHA, not audit-landing SHA) | NOTE — cosmetic | Defer (writer-thesis at T02 may tighten or ignore; underlying evidence unambiguous) |
| FC11 reads as half-prescription, half-prohibition ("only the audit-permitted framing is allowed") | NOTE | Track as reviewer-deep T03 watch item |
| Plan line 174 says "5 allowed files" but File Manifest lists 9 (counts depend on whether planning + ephemeral PR-body files are excluded) | NOTE — cosmetic | Defer (numerically consistent if planning + ephemeral excluded) |
| Pre-commit hook framework wording in T05 | NOTE — informational | reviewer-deep T05 post-commit verification |

Reviewer-deep verdict: **PASS-WITH-NOTES.** All 5 required + 6 bonus anchor spot-checks (1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 17, 19, 20, 21) verified empirically. PR diff scope is only `planning/current_plan.md`. No forbidden file touched. No thesis prose touched.

## 4. Reviewer-adversarial Mode A findings (methodology defensibility)

### 4.1 Examiner scenario findings (Scenarios A–F)

| Scenario | Verdict | Risk |
|---|---|---|
| **A** — "isn't this just a final feature catalog?" | **PASS WITH CONCERN** | Block-distribution citation (5+6+4+7+4 = 26) quietly conflates 4 `gate_and_blocked` rows with 3 `blocked_until_additional_validation` rows. Writer-thesis must disambiguate that `gate_and_blocked = 4` contains 3 `blocked` + 1 `sanity_gate_not_model_input` (`slot_identity_consistency`). |
| **B** — "if V-9 passed, why is Step still open?" | **PASS** | 3-clause `continue_predicate` framing is the strongest single defence. |
| **C** — "why write about Phase 02 before materializing features?" | **PASS** | "Must justify" alternatives-considered (defer §4.5 entirely) is named and rejected. |
| **D** — "why not do AoE2 registry first?" | **PASS-WITH-NOTES** | Reinforce: forbid "priority"/"first"/"lagging"/"behind"/"pending"/"will catch up" framing; use "differential per-dataset progress profile". |
| **E** — "does this leak future info?" | **PASS** | Registry is a declaration set, not a value set; I3 structurally inapplicable. |
| **F** — "are you hiding unresolved D-dimensions under a provisional label?" | **PASS WITH CONCERN** | "Provisional" needs glossing discipline against synonymy with "preliminary/draft/interim/near-final"; needs justification for being in Chapter 4 (methodology) vs Chapter 5 (results). |

### 4.2 Claim-surface refinements (10 risk findings; per-anchor stress test)

The 21 required claims hold up, but anchors 3, 10, 14, 15, 20, 21 carry MEDIUM examiner-vulnerable wording risk. Writer-thesis brief must absorb the following:

- **Anchor 3 (26×14 columns):** Frame the appended `block` column as "derived by the V-9 emitter for human-browse classification (not a validator output)" — not as "13 required + 1 extra appended" which invites examiner attack on post-hoc column appendage
- **Anchor 10 (manifest token at lines 12 + 73):** HIGH evidence-chain fragility — add `Cited-as-of-SHA` HTML comments per PR #218 precedent
- **Anchor 14 (STATUS YAML not flipped):** Forbid future-tense paraphrase ("could have been flipped but wasn't yet")
- **Anchor 15 (11 deferred dimensions including N/A rows):** Justify why N/A rows are inlined — methodology-load-bearing transparency, not redundant
- **Anchor 20 (AoE2 NOT yet comparable):** Forbid temporal-progression framing
- **Anchor 21 (cross-ref §4.3.3):** See Scenario A CONCERN — 4-vs-3 disambiguation

### 4.3 Additional forbidden claims (mandatory for T02 dispatch prompt)

The existing FC1–FC18 catalog is comprehensive against the F1–F18 audit, but 6 PR #219-specific gaps require additions:

- **FC19 — "registry-skeleton vs registry" terminological slippage.** Within §4.5, use ONE form consistently: *"rejestr rodzin cech (warstwa rejestru-skeletonu, V-9)"* OR *"artefakt rejestru rodzin cech na poziomie V-9"*. Do NOT alternate.
- **FC20 — "covers all D1–D15" leakage.** Forbid Polish equivalents *"pokrywa wszystkie wymiary D1–D15"* / *"adresuje wszystkie wymiary projektowe"*. Allowed phrasing: "mechanically enforces a subset of D1–D15 (D1, D5/D6 history-side, D7, D10-sub-1, D11, D13, D15); defers D2, D3, D4-in_game, D5-in_game, D6-full, D8, D9 to materialization + CROSS-02-01-v1.0.1; declares D10-sub-2, D12, D14, D15 as N/A or AoE2-side".
- **FC21 — implicit "Phase 02 ready" framing in cross-references.** Forbid Polish verbs *"zapewniona"*, *"zabezpieczona"*, *"gotowa"*, *"kompletna"* (or English "ready", "complete", "secured", "ensured") when describing Phase 02 status.
- **FC22 — "provisional" with positive valence.** Polish *"prowizoryczny"* MUST be paired at first usage with structural disqualifier ("satisfies clause 1 only of the 3-clause continue_predicate"). Do NOT use alongside "bliskie ukończenia", "prawie gotowe", "wstępne".
- **FC23 — English-loan-into-Polish technical drift.** The manifest token `partial_coverage_v9_baseline` is a code-level identifier — DO NOT translate. Use "token statusu `partial_coverage_v9_baseline`" or "określenie statusu w manifeście", NOT "token częściowego pokrycia poziomu V-9". (Elevates plan OQ6 default to forbidden-claim.)
- **FC24 — F-numbering drift recurrence.** F1–F18 canonical from audit §8. §4.5 prose MAY cite the audit in a footnote but MUST NOT renumber/refactor/re-label; use 'audit §8 row F-N' format verbatim.

### 4.4 Envelope-tightening recommendations for T02 writer-thesis dispatch (7) + T04 (2)

**For T02 dispatch:**

1. **Cited-as-of-SHA HTML comment discipline** (PR #218 precedent). Top of §4.5:
   ```
   <!-- Cited-as-of-SHA: master @ f1add6ce -->
   <!-- Registry CSV: <SHA-at-T02-time> -->
   <!-- Registry MD: <SHA-at-T02-time> -->
   <!-- notebook_regeneration_manifest.md: <SHA-at-T02-time> -->
   ```
2. **4-vs-3 `gate_and_blocked` row disambiguation** at point of citing block distribution.
3. **"Provisional" glossing discipline** at first usage with structural disqualifier; forbid synonymy with "preliminary/draft/interim/near-final".
4. **Why §4.5 lives in Chapter 4 not Chapter 5** — one-sentence "Must justify" rationale.
5. **No temporal-progression framing for AoE2 asymmetry** ("differential per-dataset progress profile" not "lagging/behind/pending/will catch up/priorities").
6. **Registry-skeleton vs registry terminological consistency** per FC19.
7. **F-number citation discipline** per FC24.

**For T04 reviewer-adversarial dispatch:**

8. **Sentence-level surface check for upgrade-in-meaning** (PR #218 critique precedent). Scan every sentence for paraphrases that subtly upgrade "provisional → effectively complete", "narrowed → effectively closed", "deferred → handled". NOT covered by grep-based forbidden-phrase checks.
9. **Cross-reference reading test.** Read §4.3.3 + §4.5 as continuous narrative; verify no sentence in §4.5 *combined with* §4.3.3 produces implicit "Phase 02 is ready" claim. The two sections must compose without leaking readiness.

## 5. Sign-off

**T02 dispatch may proceed** after the user explicitly approves the following dispatch-prompt enhancements:

1. The 6 additional forbidden claims FC19–FC24 to be folded into the writer-thesis forbidden-claim list verbatim
2. The 7 envelope tightenings for T02 + 2 envelope tightenings for T04 to be folded into the respective dispatch prompts
3. The Cited-as-of-SHA HTML comment discipline (PR #218 precedent)

**No replanning required.** The plan's 6-scenario defence framework, 21-anchor evidence chain, and 18-row forbidden-claim list are structurally sound; the enhancements are sentence-surface and terminological-drift refinements.

**Open Questions OQ1–OQ7:** all 7 have defensible recommended defaults; only OQ1 (Polish title) and OQ6 (manifest token translation) need user attention. OQ6 should be elevated to FC23 verbatim.

The plan respects PR #216 / PR #217 / PR #218 coupling correctly: cites PR #216 as load-bearing evidence without claiming closure, treats PR #217 audit as canonical routing source (not source of truth), cross-references PR #218 §4.3.3 read-only without re-deriving claims or collapsing `narrowed → closed`.

## 6. Relevant file paths

- `/Users/tomaszpionka/Projects/rts-outcome-prediction/planning/current_plan.md` — the reviewed plan
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/planning/current_plan.critique.md` — this file
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/thesis/chapters/04_data_and_methodology.md` — T02 target; insertion point after line 428 (end of §4.4.6)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/thesis/WRITING_STATUS.md` — line 75 GATE-14A6 (PR #218) must NOT be modified
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/thesis/chapters/REVIEW_QUEUE.md` — T02 Pending row append
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv` — 26 data rows × 14 columns verified
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md` — provisional disclaimer + V-1..V-9 description + deferred-dimension table verbatim
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/thesis/pass2_evidence/notebook_regeneration_manifest.md:12` + `:73` — `partial_coverage_v9_baseline` token (HIGH evidence-chain fragility per finding 4.2 anchor 10)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/docs/TAXONOMY.md` — "registry artifact" NOT defined; do NOT edit
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/reports/specs/02_01_leakage_audit_protocol.md` — CROSS-02-01-v1.0.1 LOCKED 2026-04-26

---

**Status:** All open conditions resolved by P01 commit on 2026-05-17. OQ1 title approved (no skeleton wording; `## 4.5` top-level heading). OQ6 elevated to FC23. FC19–FC24 user-approved and folded into T02/T03/T04 dispatch constraints. 9 envelope tightenings (7 for T02 + 2 for T04) approved. writer-thesis NOT yet invoked.
