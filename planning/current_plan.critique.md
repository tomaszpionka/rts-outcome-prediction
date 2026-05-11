# Plan critique — SC2EGSet Step 02_01_01 provisional registry artifact (validated through V-9)

---
target_plan: planning/current_plan.md
target_branch: phase02/sc2egset-registry-artifact-provisional-v9
target_commit_at_review: f20ccd4f (empty bootstrap commit on top of master 396f162c)
draft_pr_number: 216
draft_pr_url: "https://github.com/tomaszpionka/rts-outcome-prediction/pull/216"
reviewers:
  - reviewer-deep
  - reviewer-adversarial
reviewer_date: 2026-05-10
critique_round: 1
combined_verdict: PASS-WITH-FIXES (mechanical) + APPROVE-WITH-CONDITIONS (mechanical) — fixes applied; ready for T01
fixes_applied: 8
fixes_skipped: 3
---

## Combined verdict — round 1

Both reviewers were dispatched in parallel against `planning/current_plan.md` at branch HEAD `f20ccd4f` (empty bootstrap commit on top of master `396f162c`). Both returned non-blocking verdicts; all required fixes were mechanical wording / numbering / factual-citation items, none touching load-bearing methodology.

| Reviewer | Verdict | Required fixes | Skipped |
|---|---|---|---|
| reviewer-deep | PASS-WITH-FIXES | F1, F2, F3, F4, F5, F6, F7 | F1 (verified correct via INDEX.md row 11), F4 (cascading scope; non-blocking), F7 (low-priority advisory) |
| reviewer-adversarial | APPROVE-WITH-CONDITIONS | C1 (HARD), C2, C3, C4 | none |

Fixes applied to the plan in this same `docs(planning)` commit:
- **C1** (HARD-BLOCKING per adversarial; factual error in disclaimer D8 row): `full_replay_min_loop_blocked` is NOT a column on `tracker_events_feature_eligibility.csv` — it is a token in the `upstream_verdicts` cell of the `time_to_first_expansion_loop` row. Verified via `head -1` on the CSV (12 columns total; no `full_replay_min_loop_blocked` column). Disclaimer D8 row commitment-path cell rewritten to cite `upstream_verdicts cell, which records full_replay_min_loop_blocked=True verdict`.
- **C2**: §Problem Statement (d) docstring sentence — replaced "at least one of the three ROADMAP `continue_predicate` clauses ... is not yet satisfied" (which implies one MAY be satisfied) with "BOTH the CROSS-02-01-v1.0.1 post-materialization audit re-run AND the per-family CROSS-02-03-v1.0.1 §10 verdict for every registry row remain unsatisfied" (factually accurate; both clauses 2 + 3 are unsatisfied at this artifact PR).
- **C3**: T10 §Operation §Stop condition — clarified that reviewer-deep `PASS-WITH-FIXES` is non-blocking IF fixes are addressed in a follow-up commit before T11; `BLOCKER` (deep) and `BLOCKED` (adversarial) are equivalent halt severities.
- **C4 + F6**: T01 §Instructions §4 (provenance block specification) — `executed_at` field now uses `datetime.now(timezone.utc).date().isoformat()` (timezone-explicit UTC; not local-tz `date.today()`); the provenance block MUST include the disclosure sentence about same-UTC-day byte-identicality vs cross-UTC-day metadata drift.
- **F2** (3-place phrasing consistency): Gate Condition 3, Acceptance criteria 2, Validation gates 2 all rewritten to "26 data rows + 1 header row = 27 lines total; 14 columns".
- **F3**: T02 §Operation step 1 — "already done at PR #215 merge. Verify." replaced with "Live check during plan authoring confirmed line 477 still reads `(V-1 through V-8)` on master `396f162c` ... **This is a real edit, NOT a verify-only.**". Verified by parent via `sed -n '477p'` on the notebook .py.
- **F5**: T06 §Stop condition — explicit grep test added: `grep -c "^### " 02_01_01_feature_family_registry.md` returning exactly `5`.

Fixes skipped with rationale:
- **F1** (verify PR #213 lineage attribution as "V-1 strict + V-7"): Verified correct via `planning/INDEX.md` line 11 verbatim — "PR #213 ... SC2EGSet Step 02_01_01 V-1 strict + V-7 cold-start vocabulary/sentinel validation". No edit needed.
- **F4** (renumber T05 deliberate-gap → T06→T05 etc.): Reviewer-deep marked non-blocking ("worth fixing for cleanliness"). Renumber would touch ~15-20 cross-references throughout the plan; risk-vs-benefit unfavorable. T05 stays as a documented no-op slot. The audit-trail oddity (gap between T04 and T06) is a known small cost.
- **F7** (clarify `.github/tmp/commit.txt` per-task usage in §File Manifest): Low-priority advisory. The existing manifest row "scratch (created and removed within session per memory `feedback_git_commit_format`; not committed)" is sufficient; per-task usage is implicit in T07 / T08 / T09 / T11 stop conditions which each say "commit.txt removed".

After fixes, the plan is ready for T01. The 3-round adversarial cap is at round 1 of 3.

---

# Reviewer-deep — round 1 (PASS-WITH-FIXES)

## §Summary

All load-bearing methodology decisions verify against on-disk state. The closure-status framing is honest and consistent across all surfaces (disclaimer / research_log / CHANGELOG / PR body). The STEP_STATUS no-touch decision is well-justified by the conjunctive `continue_predicate` and the absent per-step `in_progress` vocabulary. The 26-row partition arithmetic checks (5+6+4+7+4=26). The disclaimer's V-N → D-N mapping table matches the validator's actual scope. The non-supersession block is verbatim CROSS-02-03-v1.0.1 §1.3.

The seven fixes below are mechanical wording corrections, not methodology issues. None should block T01.

## §Verified facts (reviewer-deep)

1. STEP_STATUS schema (Plan §c, lines 138-178): Confirmed — STEP_STATUS.yaml lacks any documented `in_progress` token in its comment block. All entries are `complete` + timestamps. No Phase 02 step entry exists. The "no-touch" rationale is sound.
2. PIPELINE_SECTION_STATUS (lines 1-22): Confirmed — three statuses `complete | in_progress | not_started`, "in_progress when ANY step is in_progress or complete". No Phase 02 pipeline section exists yet.
3. PHASE_STATUS (lines 1-11): Confirmed — three statuses `complete | in_progress | not_started`. Phase 02 = `not_started`.
4. ROADMAP `continue_predicate` (lines 2060-2066): Confirmed verbatim — conjunctive 3-clause: artifact-check + post-materialization audit re-run + per-family §10 verdict.
5. CROSS-02-03-v1.0.1 §1.3 (lines 61-78): Confirmed verbatim — "do not replace ... complementary, not redundant ... CROSS-02-03 audits definitions; CROSS-02-01-v1.0.1 audits materialized columns. Both gates are mandatory."
6. REQUIRED_COLUMNS count (validate_registry_skeleton.py lines 79-93): Confirmed exactly 13.
7. 26-row partition (5+6+4+7+4=26): Confirmed — SKELETON_PRE_GAME=5, SKELETON_HISTORY=6, SKELETON_IN_GAME_NOW=4, SKELETON_IN_GAME_CAVEAT=7, SKELETON_GATE_AND_BLOCKED=4. Sum = 26.
8. Manifest vocabulary docstring (lines 8-13): Confirmed five tokens: `confirmed_intact | not_yet_assessed | flagged_stale | regenerated_pending_log | phase_blocked`. The new token does not collide; alphabetical position immediately before `phase_blocked` is correct.
9. Validator scope (validate_registry_skeleton.py lines 14-59): V-1 through V-9 all present and described. The plan's V-N → CROSS-02-03 dimension mapping matches the validator docstring.

## §Mechanical fixes (F1–F7)

- **F1**: `non_batching_lineage_position` (frontmatter, line 36) attributes "V-1 strict + V-7" to PR #213. Verify against actual PR #213 contents.
- **F2**: 3-place phrasing inconsistency for "26 + header" across §Acceptance §2, §Gate §3, T06 stop condition.
- **F3**: T02 step 1 says "V-8 → V-9 already done at PR #215 merge. Verify." On-disk read of notebook line 477 still shows V-8. The "already done" claim is wrong. Mark as a real edit.
- **F4**: T05 is a deliberate no-op slot. Renumber T06→T05 etc. for cleanliness. Non-blocking.
- **F5**: T06 stop-condition `grep` test for "all five disclaimer subsections" should specify the literal `grep -c "^### "` expected count = 5.
- **F6**: T01 specifies `executed_at = date.today().isoformat()` for idempotency. Use `datetime.now(UTC).date().isoformat()` for timezone-explicit UTC.
- **F7**: `.github/tmp/commit.txt` Allowed table row should clarify per-task usage at T07, T08, T09, T11.

## §Honesty audit (reviewer-deep)

The plan's prose framing is consistently honest. No instance of overclaim or weaseling found. The phrase "this is provisional" appears in 4+ surfaces. The "STEP_STATUS untouched" claim appears in 6+ surfaces. The "CROSS-02-01-v1.0.1 post-materialization audit still mandatory" carries through commit message, CHANGELOG, PR body, and disclaimer.

## §Cross-game generalization (reviewer-deep)

The artifact is sc2egset-only. The disclaimer's per-dimension table correctly marks D10-sub-2 / D12 / D14 as N/A for sc2egset and defers to a future aoestats-side V-N PR. Cross-game framing readiness preserved.

## §Verdict — reviewer-deep

**PASS-WITH-FIXES.** Apply F1–F7 (mechanical), then proceed to T01. All four load-bearing methodology decisions (no-touch on STEP_STATUS; non-supersession of CROSS-02-01-v1.0.1; verbatim disclaimer; new manifest token) verify against on-disk state.

---

# Reviewer-adversarial — round 1 (APPROVE-WITH-CONDITIONS)

## §Lens assessments

- **Temporal discipline**: N/A — this artifact emits the registry skeleton's catalog row tuples; no feature value is computed and no per-game prediction occurs. The disclaimer's "Non-supersession" block correctly defers all temporal enforcement (D5/D6 in-game, D8) to the post-materialization audit (CROSS-02-01-v1.0.1 §2.1/§2.2).
- **Statistical methodology**: N/A — no statistical comparison is run.
- **Feature engineering soundness**: SOUND with one factual error (F-1 below). The `block` column choice (single CSV with partition tag) is consistent with §Open Questions Q8; the 26-row × 14-column shape matches `REQUIRED_COLUMNS + ["block"]`; cold-start vocabulary is asserted by V-7 (orthogonal to artifact emission); no magic numbers introduced.
- **Thesis defensibility**: STRONG. The disclaimer's five-section structure (V-N mapping, deferred dimensions, non-supersession, partial closure, commitment paths) survives an external examiner who asks "what does this artifact actually claim?" The registry-MD claim shape (`validated_through = V-9`, partial closure, non-supersession) is consistent across CSV-block, MD-disclaimer, research_log entry (T09), CHANGELOG bullet (T08), and PR body (T11).
- **Cross-game comparability**: MAINTAINED. The disclaimer correctly marks D10-sub-2 / D12 / D14 as "N/A for sc2egset", with D10-sub-2 explicitly deferred to "a future aoestats-side V-N PR".

## §Examiner's questions answered by the plan

1. *"Why is Step 02_01_01 not closed in STEP_STATUS after this artifact lands?"* — Answered in §Problem Statement (c) + disclaimer §"Step 02_01_01 closure status — partial" + research_log entry T09. The answer is a 4-point STEP_STATUS no-touch rationale with citations.
2. *"What does V-9 actually rule out, given that the spec authors already encoded `symmetric` everywhere?"* — Answered honestly in disclaimer paragraph after the V-N table: "structural guard against future drift, not a violation detector". Gives V-9 a defensible regression-prevention purpose without undermining its value.
3. *"Why is `validated_through = V-9` not a Phase 02 leakage-clearance claim on its own?"* — Answered in disclaimer §"Non-supersession" + §"Commitment path" — the artifact is citable in Chapter 4 §4.5 ONLY alongside the post-materialization audit artifact.

## §Prior-round condition compliance (7 conditions from the disclaimer-authoring round)

| # | Condition | Status |
|---|-----------|--------|
| 1 | V-9 PR ships standalone | SATISFIED — PR #215 merged at master `396f162c`. |
| 2 | Artifact PR is a separate plan/execute cycle | SATISFIED — this is the separate plan. |
| 3 | Artifact PR plan reviewed by reviewer-adversarial | SATISFIED — this dispatch. |
| 4 | Artifact MD includes verbatim disclaimer | SATISFIED — plan §"Disclaimer text — verbatim" reproduces all 5 elements. T01 step 4 forbids paraphrase; T02 enforces no SKELETON-literal modification. |
| 5 | STEP_STATUS.yaml MUST NOT flip to `complete`; preferably untouched | SATISFIED — §Problem Statement (c) commits to no-touch with full schema rationale; §Stop conditions #2 makes any STEP_STATUS diff a hard halt. |
| 6 | Manifest entry uses non-`confirmed_intact` status | SATISFIED — new token `partial_coverage_v9_baseline` introduced in §Problem Statement (d). |
| 7 | Path (a) commitment enumerated per deferred dimension in MD | SATISFIED — disclaimer §"What V-1..V-9 do NOT enforce" + §"Commitment path" tables enumerate D2 / D3 / D4-in_game / D5-in_game / D6-full / D8 / D9 / D10-sub-2 / D12 / D14 / D15 with per-row commitment paths. |

All 7 prior conditions met.

## §New findings (reviewer-adversarial)

- **F-1 (FACTUAL ERROR — disclaimer D8 row)**: The disclaimer claimed `full_replay_min_loop_blocked` was a column on the eligibility CSV. Verified: it is NOT a column (CSV has 12 columns; no `full_replay_min_loop_blocked` column). It IS a token in the `upstream_verdicts` cell of the `time_to_first_expansion_loop` row. **Hard-blocking** because the disclaimer is reproduced verbatim into the artifact MD; a citation slip ships into the artifact unless fixed in the plan first.
- **F-2 (METHODOLOGY GAP — manifest token semantics)**: The token `partial_coverage_v9_baseline` names ONE of the two unsatisfied `continue_predicate` clauses but elides the other. The 3-clause predicate has both clause 2 (post-materialization audit) AND clause 3 (per-family §10 verdict) unsatisfied. The token name encodes only clause 2. The plan's docstring sentence does enumerate both, but the token name itself is semantically lossy.
- **F-3 (REVIEWER ROUTING ASYMMETRY — T10)**: Verdict vocabulary asymmetry between reviewer-deep (`PASS / PASS-WITH-NOTES / FIX / BLOCKER`) and reviewer-adversarial (`PASS / PASS-WITH-NOTES / APPROVE-WITH-CONDITIONS / BLOCKED`). Plan should explicitly enumerate reviewer-deep `PASS-WITH-FIXES` semantics in T10 stop condition.
- **F-4 (IDEMPOTENCY HONESTY — Gate Condition 7 + T01 step 4)**: The plan accepts day-granularity for `executed_at` for byte-identical re-runs within the same UTC day. The artifact MD §Provenance block should declare this caveat verbatim so the reproducibility claim is examiner-defensible.
- **F-5 (DRIFT FROM PLANNER NUMBERING — T05)**: T05 is a no-op slot. Harmless; current plan has the explanatory note. Not a methodology blocker.

## §Conditions for approval (C1–C4)

- **C1**: §"Disclaimer text — verbatim" D8 row — change `full_replay_min_loop_blocked column` to `upstream_verdicts cell, which records the full_replay_min_loop_blocked=True verdict for V-7 time-to-first-event families`. Hard fix.
- **C2**: §Problem Statement (d) docstring sentence — strengthen "at least one of three" → "BOTH ... unsatisfied".
- **C3**: §T10 Stop condition — append reviewer-deep `PASS-WITH-FIXES` (non-blocking IF fixes addressed before T11) and `BLOCKER`/`BLOCKED` halt-equivalence.
- **C4**: T01 step 4 + §Gate Condition 5 — provenance block disclosure about same-UTC-day vs cross-UTC-day reproducibility.

## §Verdict — reviewer-adversarial

**APPROVE-WITH-CONDITIONS.** All 7 prior-round conditions met. C1 is hard-fix (factual error in verbatim-reproduced text). C2-C4 are methodology refinements that strengthen examiner-defensibility without changing the artifact's load-bearing claim shape. None requires a new V-N validator, a spec amendment, or a STEP_STATUS touch. The 3-round adversarial cap is at round 1; two more rounds available if the parent disagrees with C1.

---

# Acceptance for plan-side close

After parent's mechanical-fix application (C1, C2, C3, C4+F6, F2, F3, F5; F1/F4/F7 skipped with rationale), the plan is approved for execution. T01 may fire after this `docs(planning)` commit lands.

The executor at T01 should:
1. Land the artifact-emission cell + narrative-correction edits at T01 + T02.
2. Run the pre-commit-equivalent checks at T03 + T04.
3. Execute the notebook end-to-end at T06 (T05 is a no-op slot).
4. Commit artifacts (T07), release (T08), and lineage (T09) as separate commits per the plan.
5. Dispatch BOTH reviewer-deep AND reviewer-adversarial in parallel at T10 (post-execution gate).
6. Mark PR #216 ready at T11 only after both reviewers PASS / PASS-WITH-NOTES / APPROVE-WITH-CONDITIONS.

The non-batching lineage discipline (sequence step 7 — "Only after all validation modules pass, generate artifacts") is preserved. The artifact does NOT batch a new validator with the artifact emission, and does NOT touch the next Step (02_01_02). Closure of Step 02_01_01 is explicitly deferred to a future PR satisfying clauses 2 and 3 of the ROADMAP `continue_predicate`.
