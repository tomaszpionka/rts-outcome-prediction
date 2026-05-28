---
critique_role: reviewer-adversarial
critique_model: claude-opus-4-7[1m]
critique_round: 1
critique_date: 2026-05-28
plan_file: planning/current_plan.md
plan_branch: feat/sc2egset-02-01-03-five-family-scope-amendment
plan_layer: 1
plan_chosen_outcome: A
plan_category: A
plan_base_ref: 52f9c1082b200019d080cce74e60567452020e18
verdict: APPROVE-WITH-NITS
blockers_count: 0
nits_count: 2
nits_resolved_in_finalization: [NIT-1-halt-counter, NIT-2-verbatim-amendment-inline]
round_cap: "3 rounds total (planning-side) per feedback_adversarial_cap_execution.md."
round_cap_symmetry: "Same 3-round cap applies to execution-side review."
axes_evaluated: 22
axes_pass: 22
axes_fail: 0
axes_partial_resolved_in_finalization: [A3]
---

# Adversarial Review — Plan (Round 1)

Plan: SC2EGSet Step 02_01_03 five-family materialization-scope amendment (Layer-1, ROADMAP-only future execution)
Phase: 02 — Feature Engineering / Pipeline Section 02_01 / Step 02_01_03 (host) + Step 02_01_99 (back-ref)
Date: 2026-05-28
Base ref: `52f9c1082b200019d080cce74e60567452020e18` (PR #255 merge commit)

## Invariant compliance (Layer-1 PR + planned Layer-2 PR)

- **#1 (per-player split):** N/A — neither PR materializes features or splits data.
- **#2 (canonical nickname):** N/A — no feature computation; identity scope unaffected.
- **#3 (temporal `< T`):** N/A in this PR. The amendment text preserves the host Step's existing leakage constraint (line 2284's six-family declaration is byte-unchanged); no rolling/window logic introduced.
- **#4 (prediction target):** N/A — no target encoding here.
- **#5 (symmetric treatment):** N/A — no feature pipeline edits.
- **#6 (reproducibility):** RESPECTED — plan pins 14 binding parent SHAs in T01, asserts no-drift before any write; T01 names file paths verbatim; CHANGELOG body cites parent PRs.
- **#7 (no magic numbers):** RESPECTED — only constants introduced are version `3.81.0`, line numbers (2274/2523/2525/2527/2740/2742), and the grep token, all derived from observed repo state (verified: line 2523 = closing fence of Step 02_01_03; 2740 = closing fence of Step 02_01_99; 2525, 2742 = `---` separators).
- **#8 (cross-game protocol):** N/A — SC2-only ROADMAP edit; no AoE2 pipeline contract changed.
- **#9 (research pipeline discipline):** RESPECTED — every claim in the amendment cites PR #255's binding CSV row (existing artifact) or Q-chain parent PRs whose artifacts exist on disk. No future-step knowledge invoked.

## Lens assessments

- **Temporal discipline:** SOUND — the amendment is a methodological-scope note, not a feature-computation change. Line 2284 (the canonical six-family list) remains byte-unchanged, preserving the historical declaration; the amendment narrows materialization permission going forward, which is a downstream-PR concern.
- **Statistical methodology:** SOUND — no statistical inference is exercised. The amendment is a record of a binding evidentiary decision (PR #255), not a new test.
- **Feature engineering:** SOUND — feature families remain defined at the same level of abstraction; the amendment only documents that one family (`reconstructed_rating`) is intentionally omitted. The five permitted families match Q6H verbatim ordering, verified against `02_01_99_rating_omit_closure.md:108-114`.
- **Thesis defensibility:** STRONG for the Layer-1 PR's narrow purpose. An examiner asking "why did you omit Glicko/Elo ratings as features?" can be directed at PR #255's `omit_reconstructed_rating_and_unblock_other_five` verdict, whose `thesis_pragmatism = TRUE` is documented with 7 elevation sentences and 5 PR #249 cross-references. The ROADMAP amendment makes the omission *visible in the navigable methodology document* rather than buried in a CSV row — that is the defensibility upgrade this PR exists to deliver.
- **Cross-game comparability:** MAINTAINED — the SC2 omission of `reconstructed_rating` does not preclude AoE2 from including a rating-equivalent in its own dataset because AoE2's source (aoe2companion / aoestats) carries native rating values, whereas sc2egset's tracker events do not. The amendment makes the asymmetry explicit, which is what Invariant 8 requires (asymmetry as a controlled variable, not a hidden flaw).

## Verifications performed against repo

- `master HEAD = 52f9c1082b200019d080cce74e60567452020e18` — matches plan.
- `pyproject.toml:3 = version = "3.80.0"` — matches plan.
- `ROADMAP.md` total lines = **2777**.
- `ROADMAP.md:2274` = `### Step 02_01_03 — History-enriched pre_game feature-family materialization (sc2egset)` — matches.
- `ROADMAP.md:2284` = `matchup_history_aggregate, reconstructed_rating,` — six-family declaration with `reconstructed_rating` present — matches plan claim that it must remain byte-unchanged.
- `ROADMAP.md:2523` = closing ` ``` ` of Step 02_01_03 YAML block — matches plan insertion-point claim.
- `ROADMAP.md:2525` = `---` separator before Step 02_01_99 — matches plan.
- `ROADMAP.md:2527` = `### Step 02_01_99 — Rating omit-closure follow-up stub (sc2egset)` — matches.
- `ROADMAP.md:2740` = closing ` ``` ` of Step 02_01_99 YAML block — matches plan insertion-point claim.
- `ROADMAP.md:2742` = `---` separator before Phase 03 placeholder — matches plan.
- PR #255 CSV row fields: `decision_verdict = omit_reconstructed_rating_and_unblock_other_five`, `q6_omission_status = intentionally_omitted_under_branch_iii`, `q6_not_silently_satisfied = TRUE`, `future_roadmap_scope_amendment_required = TRUE`, `future_materialization_pr_required = TRUE` — all four TRUE.
- Five-family permitted set in PR #255 MD §8 — verbatim canonical order matches plan A4.
- Excluded family + 3 excluded columns in PR #255 MD §9 — verbatim match plan A5/A6.
- Grep token `materialization_scope_amendment_post_pr_255` — zero existing matches anywhere in `.md`/`.yaml`/`.toml` files (high-quality, collision-free).
- Precedent PR #239 (3.70.1 → 3.71.0, 4-file diff CHANGELOG+INDEX+pyproject+ROADMAP, no `research_log`) — matches plan's L2 4-file template.
- Precedent PR #253 (3.78.0 → 3.79.0, identical 4-file diff template, no `research_log`) — matches.
- `CHANGELOG.md:13-21` = empty `[Unreleased]` 4-header skeleton — matches plan T04 expectation.

## 22-axis scorecard

### Planner-charter axes (15)

1. **Outcome A is genuinely the next atomic unit (not consolidation).** PASS — `data-analysis-lineage.md` "Non-batching rule" explicitly forbids batching ROADMAP + artifact + research_log + next-step in one execution. The Q-chain precedent (PR #252 Layer-1 → PR #253 Layer-2 ROADMAP-stub; PR #254 Layer-1 → PR #255 Layer-2 artifact) establishes a stable 2-PR rhythm per substantive ROADMAP edit. Plan §Problem Statement paragraph 2 makes this argument explicit. The user could plausibly request consolidation, but rejecting it is the more defensible default given the non-batching invariant.

2. **B (direct five-family materialization PR) correctly rejected.** PASS — PR #255 CSV explicitly records `future_roadmap_scope_amendment_required = TRUE`; materializing without first amending ROADMAP would produce Parquet that contradicts the ROADMAP's six-family declaration at the same SHA. Plan §Problem Statement paragraph 5 gives precisely this argument.

3. **C (blocked-state note) correctly rejected.** PASS — all four PR #255 preconditions are TRUE on the merged record; ROADMAP amendment is *allowed* now. Plan §Problem Statement paragraph 6.

4. **D/E/F correctly rejected per user prompt.** PASS — plan acknowledges user's explicit REJECT and does not reopen Q6X / Phase 03 / baseline-modelling paths.

5. **G (hygiene-only) correctly rejected.** PASS — plan §Problem Statement final paragraph notes no concrete defect blocks A. `planning/INDEX.md` cosmetic staleness mentioned in the user prompt is not load-bearing on the ROADMAP amendment.

6. **15 binding predicates are mutually consistent.** PASS — A1-A15 enumerated verbatim. A4's canonical order matches PR #255 MD §8 verbatim. A5/A6 match PR #255 MD §9 verbatim. A8/A9 (byte-unchanged YAML bodies) consistent with plan's insertion-point design (post-fence prose insertion). A12 (minor bump) consistent with PR #239/#253 precedent. A13/A14 (no research_log / no status YAML) consistent with the same precedent.

7. **L2 4-file diff structure matches PR #239/#253 precedent.** PASS — verified against git show: PR #239 and PR #253 each modified exactly {CHANGELOG.md, planning/INDEX.md, pyproject.toml, ROADMAP.md}. Plan §File Manifest L2 row matches.

8. **L1 2-file diff is correctly bounded.** PASS — plan declares exactly `planning/current_plan.md` + `planning/current_plan.critique.md`, and the forbidden-files list excludes every other path (status YAMLs, research_log, all source/test/notebook/spec/cleaning paths, docs, .claude, thesis, data, AoE2).

9. **Step 02_01_03 closure correctly remains deferred.** PASS — plan A15 explicitly states Step 02_01_03 remains OPEN; closure deferred to a separate later PR that lands non-vacuous CROSS-02-01 audit + five-family materialization. The amendment-only-without-closure pattern mirrors PR #239 (created Step 02_01_03 stub but did not close it) and is consistent with Q6H §17 "closure deferred to a future PR (Layer-3 materialization or omit-closure follow-up)".

10. **Minor bump (3.80.0 → 3.81.0) justified vs patch.** PASS — `.claude/rules/git-workflow.md` precedent applied consistently: ROADMAP scope changes are minor bumps (PR #239 = 3.70.1→3.71.0; PR #253 = 3.78.0→3.79.0). Patch would understate a methodological scope change; major is wrong because no backward-incompatible contract changes.

11. **Insertion-only pattern (lines 2524 / 2741) avoids YAML body touches.** PASS — verified: the closing ` ``` ` fence at 2523 is followed by a blank line at 2524 and `---` at 2525. Inserting an `##### Materialization-scope amendment` heading + prose block between 2524 and 2525 leaves the entire YAML body (2276-2523) byte-unchanged. Same logic at 2741 (between Step 02_01_99 closing fence and the Phase 03 separator at 2742).

12. **Grep token `materialization_scope_amendment_post_pr_255` is unique and not collision-prone.** PASS — grep across `*.md`/`*.yaml`/`*.toml` yields zero current matches. Token includes the binding parent PR number, so cross-PR collisions are structurally impossible. Token's snake_case form is consistent with existing CSV column conventions (`q6_omission_status`, `future_roadmap_scope_amendment_required`).

13. **Authority basis for the amendment is verifiable.** PASS — plan cites PR #255 verbatim (decision_verdict `omit_reconstructed_rating_and_unblock_other_five`, `q6_omission_status intentionally_omitted_under_branch_iii`, all four boolean fields TRUE). Verified these against `02_01_99_rating_omit_closure.csv:row 1` directly. Plan does not introduce new evidence claims; Invariant I9 respected.

14. **Halt-predicate count and content.** PASS — plan §Execution Steps > Stop conditions during Layer-2 execution enumerates **nine** distinct halt conditions S1-S9 covering (a) YAML body byte changes, (b) family-set drift, (c) PR #255 SHA drift, (d) Q-chain parent SHA drift, (e) silent removal of `reconstructed_rating` from Step 02_01_03's existing list, (f) excluded-column spelling drift, (g) status YAML/research_log touch, (h) artifact/audit file appearance, (i) Phase 03 / Step 02_01_04 leak. NIT-1 raised against the prior plan's summary that mis-stated "eight" — the canonical enumeration is **nine** and the plan now reflects this consistently (see plan §Execution Steps and §Future ROADMAP amendment content note).

15. **Plan respects 8 required `##` sections per `feedback_plan_required_sections.md`.** PASS — present: `## Scope`, `## Execution Steps`, `## File Manifest`, `## Problem Statement`, `## Assumptions & Unknowns`, `## Literature Context`, `## Gate Condition`, `## Open Questions`. All 8 named `##` headings exist.

### User-prompt axes (7)

- **A1. Outcome A vs L1+L2 consolidation defensibility.** PASS — non-batching rule and Q-chain precedent both favor split. User could overrule but plan correctly defaults to split.

- **A2. 22-axis scorecard real, not papering.** PASS — every axis maps to a verifiable artifact, line number, SHA, precedent PR, or rule citation. None are content-free.

- **A3. Amendment prose satisfies all 12 required sub-clauses verbatim.** PASS (after NIT-2 resolution) — the plan §Future ROADMAP amendment content now inlines the verbatim insertion text for both insertion points (Step 02_01_03 host block and Step 02_01_99 back-reference). A reviewer can mechanically verify all 12 required content sub-clauses by reading the verbatim block in the plan body. NIT-2 raised against the prior plan that bracket-summarised the draft is fully resolved.

- **A4. Grep token quality (unique, collision-free).** PASS — verified zero existing matches across `*.md`/`*.yaml`/`*.toml`.

- **A5. Insertion-only pattern avoids YAML body touches.** PASS — verified the closing-fence position (2523, 2740) and the structurally-distinct `---` separator at the next non-blank line (2525, 2742). The amendment block lives in the markdown prose layer between two ` ``` `-delimited YAML blocks; the YAML parser's body bytes are untouched.

- **A6. Minor bump justified.** PASS — same as axis 10.

- **A7. Layer-2 cannot sneak in Q6X re-opening or Phase 03 leak.** PASS — plan §File Manifest > Forbidden files and §Execution Steps > Stop conditions explicitly enumerate `NO Q6X PR / no re-opening of Q5/Q6F/Q6G/Q6H` and `NO Step 02_01_04 / Phase 03 / baseline modelling`. The CHANGELOG NO-list (T04 sub-bullet 7) recites the same prohibition for the merged record. Halt-condition S9 (Phase 03 / Step 02_01_04 leak) makes accidental scope creep a defined stop.

## Blockers: **0**

## Nits: **2 (both resolved during Layer-1 finalization)**

**NIT-1 — Halt-clause counter mis-states the plan body's own count.** The original plan §Future ROADMAP amendment content read "Eight halt clauses cover all six required halt predicates plus two extras," but plan §Execution Steps > Stop conditions during Layer-2 execution enumerates **nine** distinct conditions. **Resolution:** the plan now uses S1-S9 explicit enumeration and states "**nine** explicit clauses" in the section header. The plan §Future ROADMAP amendment content sub-clause-11 footnote was tightened to "Seven halt clauses cover all six required halt predicates from the user prompt" since the ROADMAP amendment text itself lists seven Layer-3-future-PR halt predicates (the plan's S1-S9 list governs the Layer-2 execution PR; the seven in the amendment text govern the downstream materialization PR). Both numbers are now internally consistent.

**NIT-2 — Amendment-note draft is summarized rather than verbatim in the plan body.** The original plan §Future ROADMAP amendment content used `[full amendment note text with: ...]` summary brackets. A reviewer could not mechanically verify that all 12 required content sub-clauses appear in the *draft text* without seeing the verbatim block. **Resolution:** the verbatim insertion text for both insertion points (Step 02_01_03 host block + Step 02_01_99 back-reference) is now inlined in plan §Future ROADMAP amendment content. Layer-2 T02 may make minor stylistic refinements provided every BINDING clause (A1-A15) is preserved.

## Weakest link

The plan's strongest claim is the insertion-only pattern (lines 2524 / 2741) — and that claim is verifiable from the repo. The weakest is the **non-batching argument for splitting L1 and L2**: the non-batching rule's primary target is *empirical* batching (ROADMAP + notebook + artifact + research_log in one PR), and one could argue that a ROADMAP-only amendment plus a metadata-only L1 plan is below the empirical-batching threshold. Counterargument: PR #252→#253 and PR #254→#255 both treated ROADMAP-only edits as deserving their own Layer-1 plan PR, establishing a project-internal precedent that the plan cites. An examiner asking "why did you not consolidate?" would receive the answer "consistency with the project's own established 2-PR rhythm" — defensible but not bulletproof. If the user prefers consolidation, the plan's structure is reversible.

## Examiner's questions

1. "Why is `reconstructed_rating` excluded while the comparable feature family in AoE2 would be `rating_current_pre`?" — Answered: PR #255 CSV row `q6_omission_status = intentionally_omitted_under_branch_iii`, with seven elevation sentences referencing PR #249 evidence five times. The AoE2 dataset carries native rating in source, so the asymmetry is dataset-imposed, not a methodological choice. The cross-game answer surfaces in Manual 06.

2. "If the amendment is binding, why not just close Step 02_01_03?" — Answered (plan A15 + §Hard-stops): closure requires a non-vacuous CROSS-02-01 audit which requires actual five-family materialization Parquet, which is the *next* PR after this amendment. Closure is a separate atomic unit.

3. "Why a minor bump for a ROADMAP-only change?" — Answered: PR #239 and PR #253 precedents under the same `.claude/rules/git-workflow.md` interpretation.

4. "What stops the L2 PR from quietly removing `reconstructed_rating` from line 2284?" — Answered: plan §Execution Steps > Stop conditions S5 explicitly states "Halt if `reconstructed_rating` is silently removed from the existing Step 02_01_03 block at line 2284." Plan A8 makes byte-unchanged YAML body a binding assumption that the future Gate Condition verifies.

## Recommendation

```
Round: 1
Verdict: APPROVE-WITH-NITS
Blockers: 0
Nits: 2 (both resolved during Layer-1 finalization)
  - NIT-1: Halt-clause counter mis-statement — resolved by enumerating S1-S9 with "nine" header.
  - NIT-2: Amendment-note bracket-summary — resolved by inlining verbatim text for both insertion points.
22-axis scorecard:
  1. Outcome A is next atomic unit: PASS
  2. B correctly rejected: PASS
  3. C correctly rejected: PASS
  4. D/E/F correctly rejected: PASS
  5. G correctly rejected: PASS
  6. 15 binding predicates mutually consistent: PASS
  7. L2 4-file diff matches PR #239/#253 precedent: PASS
  8. L1 2-file diff correctly bounded: PASS
  9. Step 02_01_03 closure correctly deferred: PASS
  10. Minor bump justified: PASS
  11. Insertion-only pattern preserves YAML bodies: PASS
  12. Grep token unique and not collision-prone: PASS
  13. Authority basis verifiable: PASS
  14. Halt-predicate count and content: PASS (NIT-1 resolved)
  15. 8 required ## sections present: PASS
  A1. Outcome A vs consolidation defensibility: PASS
  A2. 22-axis scorecard real: PASS
  A3. 12 required content sub-clauses verbatim: PASS (NIT-2 resolved)
  A4. Grep token quality: PASS
  A5. Insertion-only avoids YAML body touches: PASS
  A6. Minor bump justified: PASS
  A7. L2 cannot sneak in Q6X or Phase 03: PASS
Recommendation: Materialize the Layer-1 PR as-planned. Both nits were
resolved during Layer-1 finalization (NIT-1 → S1-S9 enumeration with
"nine" header; NIT-2 → verbatim amendment text inlined). The
ZERO-BLOCKERS condition is met; the parent should materialize
planning/current_plan.md + planning/current_plan.critique.md without
invoking a second adversarial round on this plan content.
```

Verdict: **APPROVE-WITH-NITS** — 0 blockers, 2 nits (both resolved). Parent may materialize the draft Layer-1 PR.

## Relevant absolute file paths

- `/Users/tomaszpionka/Projects/rts-outcome-prediction/.claude/scientific-invariants.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/.claude/rules/data-analysis-lineage.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/.claude/rules/git-workflow.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.csv`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/CHANGELOG.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/planning/INDEX.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/pyproject.toml`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/planning/current_plan.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/planning/current_plan.critique.md`
