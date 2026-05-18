---
plan_ref: planning/current_plan.md
created: 2026-05-18
reviewer_model: claude-opus-4-7 (reviewer-deep — user-directed substitute plan gate)
category: F
---

# Critique: bibliography canonicalization (plan-review provenance)

> **Reviewer substitution (user-directed, binding).** reviewer-deep is the
> mandatory gate (T01 plan + T03 final); reviewer-adversarial is
> conditional (escalation triggers in plan §"Reviewer routing").
> `critique_required: false` substituted by this mandatory reviewer-deep
> plan review (user Q5). Mirrors PR #221–#224.

**Plan under review:** `planning/current_plan.md`
**Branch:** `docs/thesis-bibliography-canonicalization` | **PR:** #225 (draft)
**Base:** `e095025a76660873c3bbff2c83377044ed095283` (master, PR #224 merged, v3.59.0) | **Bootstrap:** `1981e422`

## Invariants & temporal discipline

Bibliographic-metadata canonicalization: zero dataset/feature/model/
notebook/artifact touch. Scientific invariants #1–#9 **n-a**
(`invariants_touched: []` accurate). Temporal-discipline assessment:
**n-a** (no `.shift()`/window/normalization; no prediction at any T).

## Round 1 — reviewer-deep plan gate (2026-05-18): PASS-WITH-NITS

No blockers. Plan structurally sound for a highest-sensitivity bib-only
Cat-F PR; scope triple-bound against any `thesis/chapters/**` or
`thesis/reviews_and_others/**` edit; `Wu2017` deletion grep-gated and
the SOLE key removal (`@` 107→106); `Dimitriadis2024`/`Bialecki2023`
quadruple-gated verify-first (no sub-80 / no identity-open overwrite);
`Herbrich2007` framed as key/style drift NOT a year-error (2007
defensible — MSR "NeurIPS 20, January 2007"); planning-drift RC 0;
PR #223 parenthetical-heading defect not repeated; prior #221–#224
reviewer-deep gates all PASSED.

**Independent decisive finding — `Dimitriadis2024` identity CLOSED at
≥80 (the T02.3 deliverable, performed early at the gate):** DOI
`10.1016/j.ijforecast.2023.09.007` is the **same "triptych" work** as
the repo's `Dimitriadis2024` (identical title; arXiv:2301.10803 is its
preprint), published *Int. J. Forecasting* **40(3):1101–1122 with
Peter Vogel added as 4th author**. The repo bib's `40(1):189–210,
3 authors, no DOI` is the early/incorrect metadata. Four concurring
sources (Crossref + RePEc + ScienceDirect + arXiv). This **validates**
(does not contradict) the plan's identity-first safety design and
**closes** the user's Q3 collision: it stays the triptych record →
per the user's Q3 step (2) it is corrected to the published version
(40(3):1101–1122 + DOI + Vogel 4th author) at T03. No new key; no
overwrite of a different work.

**Independent finding — `Bialecki2023` author concern does NOT
reproduce:** Crossref + PMC (PMC10491788) + arXiv (2207.03428) all
return the identical 8-author ordered list already at
`thesis/references.bib:5-13` → `status=ok`, `action=keep/verify`, NO
bib edit. The plan handles this correctly (fix only if ≥80 *as a
change*); no spurious "fix" is to be manufactured.

reviewer-adversarial NOT triggered (no §"Reviewer routing" trigger
fired). Adversarial cap: 1 of max 3 rounds used.

## Binding conditions to fold into the T02 report (reviewer-deep nits 1–4)

1. Per-key table records the **counted** `Wu2017MSC` citation total
   (8 lines on disk: appendix 3 + Ch2 2 + Ch3 1 + Ch4 2), not the
   plan's narrative "7×". (Safety gate keys on the exact *zero*
   `[Wu2017]` count — unaffected.)
2. The "Stale prior-audit statements superseded" section states the
   **closed** `Dimitriadis2024` identity: DOI
   `10.1016/j.ijforecast.2023.09.007` = the same triptych paper,
   published 40(3):1101–1122 with Peter Vogel as 4th author
   (arXiv:2301.10803 preprint); supersede the prior
   `literature_verification_log.md:78` 40(1):189–210/no-DOI statement.
   Phrase it as CLOSED, not an open "may be a different paper".
3. The `Bialecki2023` report row records the official author list
   matches the current bib exactly → `status=ok`, no bib edit.
4. The `Elo1978` report row + schema-specifics call out the
   "Chessplayers" (one word, current bib `references.bib:129`) vs
   "Chess Players" (two words, plan/appendix) title-form decision with
   its confidence — not a silent normalization.

## Gate status

**T01 plan gate: PASS-WITH-NITS** (0 blockers; 4 nits = binding T02
report-content conditions, none gates execution). reviewer-adversarial
NOT triggered. Cleared to proceed to T02 → T05. The `Dimitriadis2024`
identity is closed ≥80 to the same triptych work → T03 applies the
published-version correction (40(3):1101–1122 + DOI + Vogel) per the
user's Q3 step (2); `Bialecki2023` = no edit (matches).
