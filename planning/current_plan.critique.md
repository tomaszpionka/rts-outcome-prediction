---
plan_ref: planning/current_plan.md
created: 2026-05-18
reviewer_model: claude-opus-4-7 (reviewer-deep — user-directed substitute plan gate)
category: F
---

# Critique: aoestats row-count + [POP:]-scope caveat (plan-review provenance)

> **Reviewer substitution (user-directed, binding).** reviewer-deep is the
> mandatory plan gate (T01) and final gate (T03); reviewer-adversarial is
> conditional (escalation trigger only). `critique_required: false`
> substituted by this mandatory reviewer-deep plan review. Mirrors
> PR #221 (M-1) / #222 (M-2). User selected Option A verbatim at plan
> approval ⇒ reviewer-adversarial NOT mandatorily pre-triggered.

**Plan under review:** `planning/current_plan.md`
**Branch:** `docs/thesis-aoestats-rowcount-scope-caveat` | **PR:** #223 (draft)
**Base:** `adf933031bb8c9d335d07d1e23d867603c244371` (master, PR #222 merged) | **Bootstrap:** `47286229`

## Invariants & temporal discipline

Pure prose-clarification PR: zero data/feature/model/notebook/artifact
mutation (read-only verification of an already-generated EDA artifact
only). Scientific invariants #1–#9 **n-a** (`invariants_touched: []`
accurate). Temporal-discipline assessment: **n-a**.

## Round 1 — reviewer-deep plan review (2026-05-18): PASS-WITH-NITS

No blockers. reviewer-deep **independently re-derived the load-bearing
on-disk artifact state**: `phase06_interface_aoestats.csv` = 137 lines =
1 header + 136 data rows; **136 `[POP:ranked_ladder]`**; 30
`[PRE-canonical_slot]`. Confirms the plan's CRITICAL FINDING — the
audit/brief prescription ("0 tags / not tag-carried / implicit-via-spec")
is STALE and FALSE post-F6 (and `WRITING_STATUS.md:67` still carries the
false pre-F6 text, confirming OQ-3's leave-as-historical containment).

The Option A NEW string is **on-disk-true and Tier-4-safe**: gives
"137 wierszy łącznie: 1 nagłówek + 136 wierszy danych"; states a token
IS present in all 136 data rows; contains NO "0 tags / not tag-carried"
claim; names the artifact token as the provisional `[POP:ranked_ladder]`
operationally superseded in the prose by the disciplined
`[POP:1v1_random_map]`; does NOT assert `[POP:ranked_ladder]` is correct
discipline (aligns with `cross_dataset_comparability_matrix.md` CX-17 /
Tier-4). OLD string unique at line 212 (line 428 uses a distinct
`136 wierszy danych` string → structurally untouched); sc2egset 35/35 +
aoe2companion 74/74 + dataset-conditional preserved; line-212/214
`[REVIEW]` flags outside the OLD string; R02 (`01_04_01_data_cleaning.md`)
and `02_00` grounding real and cited as provenance only; scope
structurally airtight; planning-drift RC 0; all Cat-F sections present;
T00–T05 coherent.

**Non-blocker nits — grep-battery counting-mode defects in the plan's
own verification commands (could cause FALSE gate failures if run
literally; the authoritative single-hunk `git diff` guard is correct):**
1. `grep -c '\[REVIEW:'` returns the LINE count (≈27, many flags share
   one long markdown paragraph line), not the occurrence count (34).
2. Post-edit `grep -c '136 wierszy danych'` legitimately goes 1 → 2
   because the NEW line-212 string contains that substring — "count
   unchanged vs base" is false as written.

**Resolution (applied at T01 as in-scope mechanical plan-doc fixes,
planning/current_plan.md only):** T02 "Verification (grep battery)" and
Gate Condition §2 amended — flag invariants now use OCCURRENCE counts
(`grep -o '\[REVIEW' …|wc -l`==34, `grep -o '\[UNVERIFIED' …|wc -l`==1);
the line-428-unchanged invariant now relies on the authoritative
single-hunk `git diff` guard (exactly one hunk at line 212, none at/near
428), with an explicit note that a raw `grep -c '136 wierszy danych'`
1→2 is expected and NOT a regression. planning-drift re-run RC 0 after
the amendment. No content/scope change; the edit OLD/NEW strings,
methodology, and Option-A decision are unchanged.

## Gate status

**T01 plan gate: PASS-WITH-NITS** (0 blockers; both nits resolved at T01
by amending the plan's verification battery only). Adversarial cap: 1 of
max 3 rounds used. reviewer-adversarial NOT triggered (escalation trigger
not met). Cleared to proceed to T02.

## Round 2 — reviewer-deep T03 final check (2026-05-18): APPROVE

No blockers; no escalation. Independently re-derived the on-disk
artifact: `phase06_interface_aoestats.csv` = 137 lines (1 header + 136
data rows); **136 `[POP:ranked_ladder]`**; 30 `[PRE-canonical_slot]` —
exactly the spec's prescribed truth; the audit/brief "0 tags /
not tag-carried" framing confirmed STALE/FALSE post-F6.

- Applied `04_data_and_methodology.md:212` is a **SHA256-byte-exact**
  match to the plan's Option-A NEW string; on-disk-true (states a token
  IS present in all 136 data rows; NO "0 tags / not tag-carried" claim);
  names `[POP:ranked_ladder]` as the provisional artifact token
  superseded in prose by disciplined `[POP:1v1_random_map]`; consistent
  with CX-17/Tier-4 (does not assert `[POP:ranked_ladder]` correct).
- Exactly ONE Ch4 hunk (§4.1.4 paragraph); sc2egset 35/35 +
  aoe2companion 74/74 + dataset-conditional preserved; trailing
  line-212 `[REVIEW]` + line-214 `[REVIEW]` flags byte-identical;
  `[REVIEW]`==34 / `[UNVERIFIED]`==1 base↔HEAD; **line 428
  byte-identical** (the raw `grep -c '136 wierszy danych'` 1→2 is the
  expected substring overlap, not a regression — single-hunk guard
  confirms).
- WRITING_STATUS §4.1.4 append strictly additive (prior cell content a
  verbatim prefix; table valid; no other row touched) and factually
  accurate with NO overclaim (no Phase 02/06 closure; line-212
  `[REVIEW]` flag stated open; pass2_evidence stated out of scope).
- Scope fully contained ⊆ manifest; `references.bib` /
  `REVIEW_QUEUE.md` / `pass2_evidence/**` / other chapters / specs /
  artifacts diff empty; CHANGELOG/pyproject correctly deferred to T04.
- Invariant trace: only I8 (population-scope honesty / dataset-conditional
  comparability) applies — the change **strengthens** it (true on-disk
  token replaces a false "0 tags" claim while preserving Tier-4
  discipline). All others n-a.

**Non-blocking follow-ups (deferred-by-plan, do NOT gate merge):**
(1) stale 2026-04-19 WRITING_STATUS §4.1.4 prefix prose + (2) stale
`pass2_evidence/**` "0 tags" audit text — both left as historical
evidence by explicit plan policy (OQ-3 / R-1); future Cat-E/F
reconciliation chore. (3) T04/T05 release hygiene pending.

## Gate status (final)

**T03 final gate: APPROVE / PASS** (0 blockers). Adversarial cap: 0
contested rounds (reviewer-adversarial NOT triggered — trigger a–d not
met). With M-1 (#221) + M-2 (#222) merged, M-3 closure via this PR brings
Chapters 1–4 to `ready_to_send_with_disclaimer` for supervisor handoff
(subject to retained review flags). Cleared to proceed to T04/T05.
