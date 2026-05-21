---
plan_ref: planning/current_plan.md
created: 2026-05-21
reviewer_model: reviewer-adversarial (Opus 4.7, Category A pre-execution gate)
category: A
plan_revision_chain: v1 (HOLD-REPLAN) → v2 (APPROVE-WITH-CONDITIONS) → v3 (this — APPROVE-WITH-NITS)
---

# Critique — v3 closure plan (bounded conditions check)

reviewer: reviewer-adversarial (Category A pre-execution gate; round 2 of 3-round cap)
base_ref: a14dc547bf19245ddc205048dbaf9cb6b11d9400
plan_target: planning/current_plan.md (materialized from /tmp/planner_plan_v3.md)

> Produced by reviewer-adversarial. Audience: Tomasz + viva preparation.
> Pre-execution Category A methodology gate per `.claude/rules/data-analysis-lineage.md`.
> This is round 2 of the 3-round adversarial cap (`feedback_adversarial_cap_execution.md`).

## Verdict

**APPROVE-WITH-NITS**

Both v2 BLOCKING conditions (C1 OQ1 schema-conformant value; C2 root research_log CROSS entry removed) are resolved pre-execution. No new methodology blockers introduced. The plan is methodologically defensible and may proceed to materialization. Per the 3-round cap, APPROVE-WITH-NITS closes the planning gate cleanly without forcing user adjudication. Four non-blocking nits are recorded for executor-time cleanup (none load-bearing).

## Round status

Round 2 of 3-round cap (`feedback_adversarial_cap_execution.md`).

- v1 (Outcome A) → HOLD-REPLAN (CROSS-02-01 §3/§5(c) artifact-presence requirement conflated with §5(a) vacuity).
- v2 (Outcome A′(i)) → APPROVE-WITH-CONDITIONS (2 blockers: C1 OQ1 new-string violation of §3 schema; C2 root research_log entry violates `.claude/ml-protocol.md`).
- v3 (this) → APPROVE-WITH-NITS. Both v2 blockers RESOLVED pre-execution.

## Source-of-truth note

The reviewer read the v3 plan at `/tmp/planner_plan_v3.md` (677 lines, 81196 bytes) as the authoritative target. The v3 plan was materialized to `planning/current_plan.md` on branch `feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit` (planning-only commit). `planning/current_plan.md` and `planning/current_plan.critique.md` on `master` were read only as historical context from merged PR #229 and were not treated as the current target plan.

## Bounded check matrix

| # | Bounded check | Result | Evidence (line numbers) |
|---:|---|---|---|
| 1 | C1 resolution (`normalization_fit_scope = "training_fold_only"`) | PASS | L172 JSON value `"normalization_fit_scope": "training_fold_only"`; L178 JSON `notes` carries v3 resolved-β rationale with symmetry argument citing `target_encoding_fold_awareness` + structural-check fields; L667 §11 OQ1 `"RESOLVED pre-execution; alternative beta chosen for schema-strict reading"`; L653 §10 R1 marked `"(LOW — downgraded from HIGH in v3 per BLOCKING condition C1 resolution)"`; full-file scan reveals no live `"N/A_no_features_materialized"` reference outside historical ledger contexts (L26 ledger, L115 U1 RESOLVED block prose, L321 CHANGELOG `Notes` historical citation, L400 §1 rationale). |
| 2 | C2 resolution (root `reports/research_log.md` removed) | PASS | L297-299 T05.b REMOVED-justification block citing `.claude/ml-protocol.md` lines 51-54 verbatim; L511-525 Q8 manifest is 10 entries (9 diff-touching + 1 transient), root `reports/research_log.md` absent; L523 v3 note confirms drop; L579-595 §6 manifest matches (9 diff + 1 transient, item 6 is per-dataset only); L59 Scope clause states "NO CROSS entry in root `reports/research_log.md` is added by THIS PR (per `.claude/ml-protocol.md` lines 51-54)"; L307-310 CHANGELOG `### Added` bullets list only per-dataset research_log (no root entry); L669 §11 OQ2 amended with per-dataset citation note ("Future aoestats / aoe2companion sessions ... may cite THIS PR's per-dataset research_log entry as the methodological precedent; no CROSS entry is added by THIS PR ..."). |
| 3 | Branch name (long form `feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit` propagated) | PASS | L2 `plan_id:`; L7 `branch:`; L46 ledger; L143 T01; L276 T05 research_log entry Branch field; L305 T06 CHANGELOG block header; L315 T06 planning/INDEX.md prescription; L333-334 T07; L383 T09 push command; L384 T09 PR title implied via commit message header L362. No `feat/sc2egset-02-01-01-closure-leakage-audit` (v2 short form) remains anywhere in v3. |
| 4 | Non-blocker nits 3, 4, 5 folded in | PASS | **Nit 3 (heredoc forbidden in T02a.2):** L183 "Do NOT use a `cat > … << 'EOF' … EOF` heredoc (zsh breaks heredoc-in-quoted-argument forms per memory `feedback_git_commit_format.md`)" — `python -c "import json; json.dump(...)"` is canonical method. **Nit 4 (MD sec 8 "Audit queries: none — vacuously satisfied"):** L210 standalone section 8 added with explicit "MUST appear as a standalone section per Nit 4 of the v2 reviewer-adversarial gate" prose; L403 §1 outcome adjudication confirms "the v3-added 'Audit queries: none — vacuously satisfied' sec 8 per Nit 4". **Nit 5 (explicit grep replaces visual-verify in T07):** L336 "Per v3 Nit 5, replace the v2 'visually verify' instruction with explicit bash checks: `grep -c \"5c7ef380\" planning/INDEX.md` and `grep -c \"a14dc547\" planning/INDEX.md` — each MUST return ≥ 1 AND the two SHAs MUST be on distinct rows". |
| 5 | No new methodology blockers introduced | PASS-WITH-NITS | (a) C1 fix is internally consistent: §3 PASS condition `"training_fold_only"` is met literally; JSON `notes` field carries the vacuous-satisfaction rationale; symmetry with peer fields (`target_encoding_fold_awareness`, structural checks) is explicit and defensible. (b) C2 fix has no orphan reference: full-file scan for "root research_log" / "CROSS entry" / "T05.b" finds only REMOVED-justification (L297-299), explanation in §1 rationale (L405), Q8 v3 note (L523), §6 v3 note (L594), and OQ2 amendment (L669) — no live citation as a deliverable. (c) Manifest count cascades correctly: §6 = 9 diff + 1 transient (L579-595); Q8 = 10 entries 9-diff + 1-transient (L511-525); T08 pre-merge validation step 2 cites "9 diff-touching files in the §6 manifest exactly (items 1–9; item 10 transient pair MUST NOT appear)" (L346); CHANGELOG `Notes` not enumerated against file-count but does not contradict; §Scope text (L59) no longer references root research_log. (d) All previously-PASSed v2 checks remain: C9 token (L473-481 Q3 unchanged), C10 halt (L221 falsifier halt), C11 manifest forbidden (L541 + L617 unchanged), C12 final gate (L647-649 unchanged), C3 cascade (L487-495 Q4 unchanged), C6 no overclaim (L571-577 §5 disclaimers unchanged), C7 disentanglement (L571 §5(1) sibling-but-distinct clause unchanged). See "Non-blocking nits" below for two minor wording-inconsistency observations. |
| 6 | Plan structure integrity | PASS | All 11 required sections present: §1 Outcome adjudication (L396), §2 Repo evidence (L414), §3 Q&A (L455), §4 Cascade analysis (L547), §5 Disclaimers (L567), §6 Allowed files (L579), §7 Forbidden files (L598), §8 Release-tail (L624), §9 Reviewer routing (L636), §10 Risks (L651), §11 Open questions (L665). §11 ends at L677 with the prescribed line "No blockers remain that prevent execution after `@reviewer-adversarial` pre-execution critique gate clearance." Plan length 677 lines (matches planner summary). |

## Blocking issues

None. Both v2 BLOCKING conditions (C1 OQ1 schema-conformant value; C2 root research_log CROSS entry removed) are resolved pre-execution. The plan is methodologically defensible and may proceed to materialization.

## Non-blocking nits

These are wording-consistency observations only; they do not block APPROVE and do not require a v4 revision before materialization. The executor may either fold them at materialization time or defer to a post-merge cleanup PR.

1. **(N1) Stale "v2" self-references in §1 and Q3.** L84 ("This v3 plan resolves BOTH BLOCKING conditions...") is correct, but L400 says "(The v1 plan was earlier returned HOLD-REPLAN; the v2 plan implemented A'(i) faithfully via T02a; v3 corrects the residual two BLOCKING conditions in v2.)" and L475 reads "This v2 plan adopts the cleaner two-field approach" (should be "This v3 plan adopts ..."). Q4 L483 also still reads "(UPDATED per task instructions)" rather than "(unchanged in v3)". These are residual v2-era phrasing slips inherited verbatim; they are not load-bearing but make the v3 self-attribution slightly inconsistent.

2. **(N2) §1 outcome adjudication says MD has 8 sections, MD spec lists 8 numbered sections; T02a.4 stop condition still says "7 prescribed sections" (L225).** L403 correctly counts 8 ("The MD contains 8 sections ... and the v3-added 'Audit queries: none — vacuously satisfied' sec 8 per Nit 4"). MD spec at L193-210 lists sections 1-8 explicitly. But T02a.4 stop condition at L225 reads "MD contains all 7 prescribed sections" — should be "all 8 prescribed sections" to match the v3-added sec 8. The executor will catch this empirically (the MD will physically contain 8 sections), but the stop-condition string is a residual v2 count.

3. **(N3) T05 Decisions taken paragraph (L287) still describes the alternative-β rationale with the v3-edit-ledger phrasing "v3 RESOLVED pre-execution per the v2 reviewer-adversarial BLOCKING condition C1".** This is correct but verbose; reads as a self-referential trail. Not load-bearing.

4. **(N4) T07 SHA-disambiguation count check is correct but slightly under-specified.** L336 says `grep -c "5c7ef380"` and `grep -c "a14dc547"` must each return ≥ 1 AND the two SHAs must be on distinct rows. The "distinct rows" check is enforced via `grep -n` line-number-differ comparison. This is correct. However, the count `≥ 1` (rather than `= 1`) means an accidental duplicate row would silently pass. A `= 1` count would be slightly tighter; ≥ 1 + distinct-line-numbers is adequate.

None of N1-N4 constitutes a methodology flaw or schema violation. The executor may fix them as part of T02a/T05/T07 execution without altering plan scope.

## Safe next instruction

**APPROVE-WITH-NITS.** Parent may materialize `/tmp/planner_plan_v3.md` to `planning/current_plan.md` and create the draft PR on branch `feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit`. The 4 non-blocking nits (N1-N4) above are optional wording cleanups; the executor may either fold them at materialization time or carry them as a tiny follow-up cleanup. None requires a v4 plan revision or another adversarial round.

Per the 3-round cap (`feedback_adversarial_cap_execution.md`), this is the second and final adversarial round; APPROVE-WITH-NITS closes the planning gate cleanly without forcing user adjudication.

The draft PR may be opened immediately. Execution (T01..T09) requires a separate, explicit user approval turn after the draft PR is inspectable.
