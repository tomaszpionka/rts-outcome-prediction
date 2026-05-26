---
critique_role: reviewer-adversarial
critique_model: claude-opus-4-7[1m]
critique_dates: [2026-05-26, 2026-05-26]
plan_ref: planning/current_plan.md
plan_date: 2026-05-26
base_ref: d9276194a1684542a04494ec02df44a5a3f2338e
branch: feat/sc2egset-02-01-03-q6h-rating-path-decision
chosen_outcome: A
round_1_verdict: HOLD
round_1_blockers: 3
round_1_warnings: 2
round_1_notes: 3
round_2_verdict: HOLD-WITH-MECHANICAL-FIX
round_2_blockers: 1 (R2.6 §"Problem Statement" Q6G metric inversion)
round_2_warnings: 0
round_2_notes: 2 (branch-name preference; Layer-2 manifest scope explicit)
round_2_mechanical_fix_status: applied by parent without consuming Round 3
final_verdict_post_mechanical_fix: APPROVE
adversarial_rounds_consumed: 2 of 3
parent_planning_pr: 248 (merged 2026-05-26; Q6G Layer-1)
parent_execution_pr: 249 (merged 2026-05-26; Q6G Layer-2; recommendation_only_glicko2)
parent_q5_pr: 243 (Q5 BINDING preserved)
parent_q6_pr: 245 (Q6 deferred_blocker; discharged by Q6F)
parent_q6f_pr: 247 (Q6F narrow_with_evidence; BINDING)
---

# Reviewer-Adversarial Critique — Q6H Layer-1 plan (Round 1 + Round 2)

This critique consolidates two adversarial rounds against the Q6H final
rating-path decision Layer-1 plan. Round 1 (HOLD) identified 3 BLOCKERs +
2 warnings + 3 notes; the planner produced a Round 2 amendment
incorporating all of them as binding methodology. Round 2
(HOLD-WITH-MECHANICAL-FIX) identified one residual textual error (R2.6)
that the parent applied directly without dispatching planner-science
Round 3 (the 3-round cap accounts only for substantive methodology rounds;
textual corrections do not consume a round).

Round 3 of the Layer-1 cap is reserved; it will be invoked only if the
Layer-2 execution PR's reviewer surfaces a Layer-1-traceable defect.

---

## Round 1 — HOLD pending R2.1 / R2.2 / R2.3 resolution

**Reviewer:** `@reviewer-adversarial`
**Date:** 2026-05-26
**Verdict:** **HOLD** pending 3 blockers; otherwise APPROVE-WITH-NITS.

### Round 1 BLOCKERs (3)

**R2.1 — 5-family / §6.2 line-range citation defect.** Plan asserted
"matches lines 238-243" of `reports/specs/02_02_feature_engineering_plan.md`,
but lines 238-243 contain SIX family rows: L238 `focal_player_history`,
L239 `opponent_player_history`, L240 `matchup_history_aggregate`,
**L241 `reconstructed_rating`**, L242 `cross_region_fragmentation_handling`,
L243 `in_game_history_aggregate`. The 5-family post-omit set is
**L238-240 + L242-243** (i.e., §6.2 minus L241). The verbatim citation
must be either `238-240, 242-243` OR `§6.2 minus reconstructed_rating at
L241`. Failing this, the plan's "unblock five" claim is internally
inconsistent.

**R2.2 — `THESIS_PRAGMATISM` flag admissibility (Invariant I9 / no magic
gates).** A boolean that flips the entire decision rule is a magic gate.
The plan must pin three things:
 (i) **exact admissibility criterion** — e.g., "substantive reasoning
     paragraph + reviewer-adversarial sign-off";
 (ii) **canonical default-derivation path** — e.g., "TRUE iff parent
     PR #249 chose `recommendation_only_glicko2` AND no execution evidence
     has been gathered between PR #249 merge and Q6H Layer-2 execution
     time";
 (iii) a **falsifier**
     `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15`
     with verbatim minimum-content rule (e.g., ≥ N sentences in MD §15;
     must cite PR #249 §15 finding-by-finding).

**R2.3 — Schema column count (37 vs 38).** Plan permitted 37 OR 38
columns ambiguously. Reviewer recommended **38** (split
`materialized_output_paths` out of legacy `notes` so materialization
paths are reviewer-grep-able without parsing prose). Add falsifier
`q6h_schema_column_count_equals_38`. Update the 4-location pinning
narrative (module constant, parametric test, gate clause, MD §11
assertion).

### Round 1 warnings (2; upgrade to blocker if not addressed)

**R2.4 — Adopt both invited falsifier additions.**
- `q6h_parquet_emitted` (Group 4 non-recurrence boundary).
- `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15`
  (= the R2.2 override falsifier).

**R2.5 — Decision-rule order-of-operations.** Evaluating
`THESIS_PRAGMATISM` first would short-circuit the bind / recommendation /
defer evaluation and reduce the decision rule to a boolean flip. The
methodologically defensible order is:
 (i) attempt bind → if proof obligations met;
 (ii) if bind blocked, recommendation_only_event_by_event_glicko2;
 (iii) if neither viable AND pragmatism gate TRUE, omit;
 (iv) else defer.
Justify the chosen order explicitly OR invert. Either acceptable; record
the choice with rationale.

### Round 1 notes (3; non-blocking)

- **N1.** Add a §15 paragraph in the Layer-2 MD reconciling the
  **#247 → #249 → Q6H sequence regression** (from "narrowed pending
  implementation proof" → "proof passed but `recommendation_only`" →
  "omitted under thesis-pragmatism" — examiner must see the regression
  as intentional, not silent walkback).
- **N2.** Verbatim citation discipline for PR #247 docstring lines 15–17:
  preserve double-backticks and the verbatim token
  `omit_reconstructed_rating_and_unblock_other_five` exactly.
- **N3.** Optional Q6 status field token
  `q6_status = "discharged_by_omission_under_thesis_pragmatism"` pinned
  at Layer-1 to remove Layer-2 ambiguity on the omit branch.

### Round 1 audit trail

- Round 1 of 3 Layer-1 adversarial cap: **consumed (HOLD).**
- Files cross-checked on master at `d9276194`:
  `reports/specs/02_02_feature_engineering_plan.md` lines 234–243;
  PR #249 CSV / MD; PR #247 docstring; PR #245 §6 / §12.

**Round 1 VERDICT: HOLD** pending R2.1 + R2.2 + R2.3 resolution.

---

## Round 2 — HOLD-WITH-MECHANICAL-FIX (R2.6 textual correction)

**Reviewer:** `@reviewer-adversarial`
**Date:** 2026-05-26
**Verdict:** **HOLD-WITH-MECHANICAL-FIX** — 1 residual textual blocker
(R2.6); 0 warnings; 2 nits. Reviewer authorised the parent to execute the
textual correction directly without consuming Round 3.

### Round 1 resolutions verified

| Round 1 ref | Status | Evidence |
|-------------|--------|----------|
| R2.1 (5-family / §6.2 line-range) | **PASS** | Plan now says verbatim "§6.2 minus L241 reconstructed_rating; L238 + L239 + L240 + L242 + L243"; family-set assertion in A8 + Schema columns 14–18 + Falsifier Group 2 keys 7–10. |
| R2.2 (`THESIS_PRAGMATISM` admissibility) | **PASS** | Three pins (a)/(b)/(c) added at A9; Schema columns 21–22; Group 3 falsifier `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15`; Gate (b3) + (b4). |
| R2.3 (schema column count = 38) | **PASS** | A10 pins 38 columns; T01 step 7 enumerates them; Gate (c1); 4-place pinning at module / test / CSV header / MD §11. Column 38 `materialized_output_paths` split from column 37 `notes`. |
| R2.4 (invited falsifier additions) | **PASS** | Both keys present in Groups 3 and 4. Total chain count = 40 (≥ 37 R2.4 floor). |
| R2.5 (decision-rule order-of-operations) | **PASS** | §"Decision rule" pins evidentiary-first order (i)→(v) with methodological-justification paragraph; A12; Falsifier `q6h_decision_rule_order_not_evidentiary_first`. |
| N1 (#247 → #249 → Q6H regression sentence) | **PASS** | T04 step 4 grep-check; Gate (b3). |
| N2 (verbatim PR #247 docstring citation) | **PASS** | T04 step 5; Gate (b5); MD §16. |
| N3 (`q6_status` token) | **PASS** | Schema column 20; Branch (iii) emission; falsifier `q6h_silent_q6_closure_on_omit_branch`. |

### Round 2 blocker — R2.6

**R2.6 — §"Problem Statement" Q6G metric inversion.** The Round 2
amendment as initially produced by planner-science misreported Q6G's
equivalence outcome as PASSED (Spearman ρ = 0.9931; |Δ log-loss| = 0.0028;
SE = 0.0035). PR #249 master artifact at
`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.csv`
Row 3 actually has:

```
spearman_rho = 0.2292277763744191       (FAR below 0.99)
abs_delta_log_loss = 0.07928287850476923 (FAR above SE = 0.0021901391180403455)
passes_spearman_bound = false
passes_delta_log_loss_bound = false
```

The verdict `recommendation_only_glicko2` (Row 5) was the NIT-N2 default
expected outcome under the auto-derived rule when equivalence FAILS and
byte-determinism PASSES — **not** the consequence of passed equivalence
without a separating anchor.

The decision rule, falsifier set, schema, and gate clauses elsewhere in
the plan were derived correctly from the actual FAILED outcome and
required no revision. Only the §"Problem Statement" prose narrative was
inverted.

### Round 2 mechanical-fix authorisation

Because R2.6 is a textual correction (not a methodology change), the
3-round adversarial cap accounts only for substantive methodology
rounds; mechanical text correction does not consume a round. The parent
was authorised to execute the textual replacement directly using the
following verbatim §"Problem Statement" text:

> Q6G's batched-vs-event Glicko-2 equivalence proof FAILED both bounds on
> the sc2egset PHA corpus: Spearman ρ = 0.2292 (≪ 0.99 threshold) and
> |Δ log-loss| = 0.07928 (≫ 1·SE = 0.00219). The byte-determinism proof
> PASSED. Under the Q6G auto-derived decision rule
> (`equivalence fail → recommendation_only_glicko2` as NIT-N2 default;
> `determinism fail → deferred_blocker`), the emergent verdict was
> `Q6G_selected_policy = recommendation_only_glicko2`. […]

Parent confirmation: applied at `planning/current_plan.md` §"Problem
Statement" in this Round-2-mechanical-fix amendment.

### Round 2 nits (2; non-blocking)

- **R2-N1 (branch name preference).** Plan initially used branch
  `feat/sc2egset-02-01-03-q6h-reconstructed-rating-closure`; user prompt
  named `feat/sc2egset-02-01-03-q6h-rating-path-decision`. Repo precedent
  (PR #244, #246, #248) supports the user's `rating-path-decision`
  pattern. The parent uses `feat/sc2egset-02-01-03-q6h-rating-path-decision`.
- **R2-N2 (Layer-2 9-file manifest scope explicit).** The §"File
  Manifest" now declares the Layer-2 9-file block as forward-visibility-only
  ("NOT created in this PR") to remove the Round-2 reviewer's concern
  that the Layer-2 manifest scope might be ambiguous.

### Round 2 final verdict (post-mechanical-fix)

**APPROVE** (zero residual blockers; 2 non-blocking nits addressed in the
parent's materialization). Layer-1 PR may be opened as draft.

### Round 2 audit trail

- Adversarial cap consumed: Round 2 of 3.
- Round 1 BLOCKER status: **RESOLVED** (R2.1 + R2.2 + R2.3 incorporated
  as binding methodology with explicit traceability).
- Round 1 NIT statuses: **3 of 3 incorporated** as binding methodology.
- Round 2 BLOCKER status: **RESOLVED** (R2.6 textual correction applied
  by parent under reviewer-authorised mechanical-fix path).
- Round 3 of 3 Layer-1 adversarial cap: **reserved** — invoke only if
  Layer-2 execution PR's reviewer-adversarial surfaces a Layer-1-traceable
  defect.

---

## Cap accounting

- Round 1 of 3 Layer-1 adversarial cap: **consumed (HOLD).**
- Round 2 of 3 Layer-1 adversarial cap: **consumed (HOLD-WITH-MECHANICAL-FIX
  → APPROVE post-fix).**
- Round 3 of 3 Layer-1 adversarial cap: **reserved.**
- Layer-2 execution PR receives a fresh 3-round adversarial cap per
  `feedback_adversarial_cap_execution.md` (symmetric application).

## Final gate

This Layer-1 PR is mergeable when:

1. Diff contains exactly 2 files: `planning/current_plan.md` +
   `planning/current_plan.critique.md`.
2. Branch matches `feat/sc2egset-02-01-03-q6h-rating-path-decision`.
3. Base ref = `d9276194a1684542a04494ec02df44a5a3f2338e` (or a
   fast-forward descendant).
4. Pre-commit hooks pass (planning-artifact validation; no `.py` touched).
5. PR is ready (not draft) at gate review time.
6. Reviewer-adversarial verdict: **APPROVE** post-Round-2-mechanical-fix —
   recorded here.

The Layer-2 execution PR's gate conditions are enumerated in §"Gate
Condition" of the plan body. Layer-2 dispatch is authorised after this
Layer-1 PR merges.
