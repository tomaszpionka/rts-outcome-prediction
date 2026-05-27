# Critique log — feat/sc2egset-02-01-99-rating-omit-closure-artifact (Layer-1, Round 2)

## Summary verdict

| Round | Verdict | Blockers | Nits | Plan length | Schema cols |
|-------|---------|----------|------|-------------|-------------|
| Round 1 (planning-side) | APPROVE-WITH-NITS | 0 | 4 (NIT-1 / NIT-2 / NIT-3 / NIT-4) | 939 lines | 42 |
| Round 2 (planning-side) | APPROVE-WITH-NITS | 0 | 3 (R2-N1 / R2-N2 / R2-N3 — Layer-2 dispatch requirements) | 998 lines | 45 |

All 4 Round-1 nits were resolved in Round 2 per explicit user directive (bake all schema/provenance-impacting nits into Layer-1 before materialization). The 3 Round-2 nits are surface-level (one arithmetic-prose clarification, one Unicode-safe tokenisation refinement, one parent-SHA label off-by-one) and are recorded below as **Layer-2 dispatch requirements**, not Layer-1 blockers. Per reviewer-adversarial Round-2 explicit recommendation, the 3-round adversarial cap is preserved for genuine blockers; Round 3 is NOT consumed on these cosmetic fixes.

Outcome A — Step `02_01_99` omit-closure artifact Layer-1 planning PR. Authority basis: Q6H `decide_history_rating_path.py` lines 457–481 (Branch (iii) literal); Q6H artifact MD §17 (two-path admission); PR #253 ROADMAP block `step_number: "02_01_99"` (≈ lines 2527–2740, `gate.artifact_check` / `gate.continue_predicate`).

---

## Round 1 reviewer-adversarial verdict (2026-05-27)

**Reviewer agent:** reviewer-adversarial (Opus)
**Inputs reviewed:** Round-1 plan (`/tmp/plan_02_01_99/proposed_current_plan.md`; 939 lines; 42-column schema) + Q6H artifact pair (READ-ONLY) + Q6H decision module `decide_history_rating_path.py` (READ-ONLY) + PR #253 ROADMAP block (READ-ONLY) + Q-chain precedent ladder PR #244/#245/#246/#247/#248/#249/#250/#251/#252/#253.
**Base ref:** `a9cf552f346d8402fa4856fbee51fa34b0b0cefe` (PR #253 merge commit; master HEAD at Layer-1 plan time).
**Adversarial round:** 1 of 3 (planning-side); 3-round cap per `feedback_adversarial_cap_execution.md`.

### Round-1 axis-by-axis verdict (26 axes: 15 planner-charter + 11 user-prompt)

**Planner-charter axes (1–15):**

| # | Axis | Result |
|---|------|--------|
| 1 | Outcome A correctness as next atomic unit | PASS |
| 2 | Compressed Layer-2 9-file scope justified | PASS |
| 3 | Module name `close_history_rating_omit_path.py` closure-side | PASS |
| 4 | 5-family set completeness | PASS |
| 5 | No silent Branch (iii) elevation | PASS-WITH-NOTE |
| 6 | OQ7 wording bridge (blocked-by-Layer-2-election vs evidence-deficit) | PASS-WITH-NOTE |
| 7 | No silent 5-family materialization authorisation | PASS |
| 8 | Q5/Q6F/Q6G/Q6H BINDING preserved | PASS (10 hard-coded SHAs empirically verified vs current repo state) |
| 9 | No materialization in either PR | PASS |
| 10 | No Q6X re-opening | PASS |
| 11 | Phase 03 / Step 02_01_04 barred | PASS |
| 12 | Version bump 3.79.0 → 3.80.0 SemVer-correct | PASS |
| 13 | Canonical branch slug `02-01-99` (not `02-01-03b`) | PASS |
| 14 | Future Tests Contract implementable | PASS |
| 15 | No batching of ROADMAP+notebook+artifact+next-Step | PASS |

**User-prompt axes (A1–A11):**

| # | Axis | Result |
|---|------|--------|
| A1 | Omit-closure artifact = next atomic unit | PASS |
| A2 | Direct emission vs. Layer-1→Layer-2 | PASS |
| A3 | Branch (iii) preconditions explicit and testable | PASS |
| A4 | Q6 omission explicit not silent | PASS |
| A5 | Five-family set semicolon-separated and traceable | PASS |
| A6 | Q5/Q6F/Q6G/Q6H verbatim preservation + SHA pins + drift falsifiers | PASS |
| A7 | Another Q6X loop avoided | PASS |
| A8 | Materialization barred in both PRs AND CROSS-02-01 audit barred | PASS |
| A9 | Phase 03 barred | PASS |
| A10 | Layer-2 avoids status YAML and `research_log` changes | PASS (Q-chain no-research_log precedent empirically verified) |
| A11 | Blockers requiring HOLD | PASS — none identified |

### Round-1 verdict

```
ROUND-1 VERDICT: APPROVE-WITH-NITS (zero blockers, 4 nits)
PR MATERIALIZATION AUTHORISED: YES (subject to user election on whether to bake nits into Layer-1 via Round 2, or defer to Layer-2 dispatch).
RATIONALE: Outcome A is the correct next atomic unit after PR #253 per non-batching rule + Q-chain precedent; 26 axes all PASS or PASS-WITH-NOTE; the 4 nits are schema/provenance-impacting clarifications that can be folded in either at Layer-1 (Round 2 re-plan) or at Layer-2 dispatch (executor amendment) — both paths are methodologically valid.
```

### Round-1 blockers

NONE.

### Round-1 non-blocking nits (4)

**NIT #1 — Branch (iii) literal-precondition semantic discipline (OQ7 anchoring).**
The Q6H decision-rule literal at `decide_history_rating_path.py` lines 457–460 reads literally: "IF branches (i) and (ii) are both blocked AND thesis_pragmatism == TRUE AND substantive_paragraph_ok == TRUE AND reviewer_signoff == TRUE." But Q6H §19 records "Branch evaluated: (ii)" — Branch (ii) was REACHED (not blocked). The Round-1 plan's S-3 counter-argument distinguishes "blocked-for-materialization-scope-purposes" from "blocked-as-Q6H-verdict-state" — methodologically defensible but requires explicit terminology to avoid subtle re-adjudication of Q6H. **Recommended fix:** add a CSV column `branch_ii_state_semantic_anchor` with semicolon-separated 4-key value distinguishing the two state-readings, plus an MD §4.2 sub-section quoting the Q6H decision-rule literal verbatim.

**NIT #2 — Column-count rationale for 42 vs Q6H's 38.**
The Round-1 plan adds 4 columns beyond Q6H's 38-column precedent without a per-column derivation paragraph mapping each addition to a reviewer concern or lineage need. **Recommended fix:** add a new top-level plan section `## Schema Derivation` between `## Future Artifact Contract` and `## Future Tests Contract` with per-column rationale; reproduce in artifact MD §11 with ≥1 substantive sentence per added column.

**NIT #3 — Substantive-vs-paraphrase anti-boilerplate guardrail.**
The structural test (≥6 sentences + ≥3 PR #249 cross-references) does NOT distinguish substantive new argument from paraphrased Q6H §15 by token reordering. **Recommended fix:** add a falsifier `omit_closure_elevation_rationale_jaccard_overlap_with_q6h_section_15_exceeds_threshold` with a concrete threshold (e.g., token-level Jaccard < 0.5) and an explicit CSV column recording the computed Jaccard to 4 decimal places.

**NIT #4 — Reviewer-signoff SHA chicken-and-egg.**
A23 says the sign-off SHA is `sha256sum planning/current_plan.critique.md` at the artifact PR's commit time, but the critique file is written BEFORE the artifact in the Layer-2 diff. **Recommended fix:** split into two distinct SHA columns `reviewer_adversarial_layer_1_critique_sha256` (pinned at Layer-1 PR merge) + `reviewer_adversarial_layer_2_critique_sha256` (pinned at Layer-2 execution end), plus optionally split the boolean for grep-symmetry.

### Round-1 path forward (recorded)

User chose Option 2 (broaden Round 2 scope): bake ALL 4 nits into Round 2 BEFORE Layer-1 materialization. Justification: the nits are schema/provenance-impacting, and deferring them to Layer-2 would leave the Layer-1 plan with known inconsistencies that the Layer-2 executor must absorb. Baking them in at Layer-1 makes the plan self-consistent and reviewer-checkable in one round.

---

## Round 2 planner-science self-critique narrative

The Round-2 plan resolves the 4 Round-1 nits as follows. Full details in `planning/current_plan.md` `## Adversarial-Review Adjustments (Round 1 → Round 2)` section; summary below.

### NIT-1 resolution (column `branch_ii_state_semantic_anchor` at position 14)

A new CSV column `branch_ii_state_semantic_anchor` (semicolon-separated 4-key value) was added at position 14. Recommended value format:

```
q6h_verdict_state=reached_as_recommendation_only_event_by_event_glicko2;omit_closure_scope_interpretation=blocked_for_phase_02_materialization_scope_under_layer_2_election;is_q6h_re_adjudication=FALSE;is_new_q6x_loop=FALSE
```

A new BINDING assumption `A26` declares the column's canonical 4-key shape. A new falsifier key `omit_closure_branch_ii_state_anchor_misnamed_or_missing_re_adjudication_assertion` enforces the shape. Future artifact MD §4 expanded with a sub-section §4.2 "Branch (ii) verdict-state vs Branch (iii) precondition-state" that quotes the Q6H decision-rule literal at `decide_history_rating_path.py` lines 442–448 (Branch (ii) literal) and lines 457–481 (Branch (iii) literal) verbatim and explicitly asserts "this is NOT a re-adjudication of Q6H" AND "this is NOT a new Q6X loop."

### NIT-2 resolution (`## Schema Derivation` section)

A new top-level plan section `## Schema Derivation` was added between `## Future Artifact Contract` and `## Future Tests Contract`. It maps each of the 7 columns deviating from Q6H's 38-column schema to a reviewer concern or lineage need (NIT-1, NIT-3, NIT-4, dual-count discipline, dispatch-time SHA pinning). Per-column rationale is reproduced in artifact MD §11 with ≥1 substantive sentence per added column.

### NIT-3 resolution (column 13 `elevation_rationale_jaccard_vs_q6h_section_15` + falsifier + threshold 0.5)

A new CSV column `elevation_rationale_jaccard_vs_q6h_section_15` (float, 4 decimal places) was added at position 13. A new BINDING assumption `A29` declares the threshold = 0.5 and the deterministic tokenisation method (whitespace + lowercase + `str.translate(str.maketrans("", "", string.punctuation))` ASCII-only strip; **see R2-N2 below for Unicode-safe refinement**). A new falsifier key `omit_closure_elevation_rationale_jaccard_overlap_with_q6h_section_15_exceeds_threshold` fires IF `jaccard >= 0.5`. `_tokenize_for_jaccard()` and `_compute_jaccard()` functions are specified in T02 instructions. Test `test_omit_closure_elevation_rationale_jaccard_lt_threshold` is in T03 instructions. Pre-emit Jaccard verification in T04 HALTs the executor if the threshold is breached.

### NIT-4 resolution (columns 15-18: dual signoff SHA + dual boolean)

Round-1's single column `reviewer_adversarial_signoff_critique_sha256` + single boolean `reviewer_adversarial_signoff` were replaced with four columns at positions 15-18:

- `reviewer_adversarial_signoff_layer_1` (bool — TRUE iff Layer-1 critique recorded APPROVE/APPROVE-WITH-NITS with 0 blockers)
- `reviewer_adversarial_layer_1_critique_sha256` (sha256 — pinned at Layer-2 T01)
- `reviewer_adversarial_signoff_layer_2` (bool — TRUE iff Layer-2 critique recorded APPROVE/APPROVE-WITH-NITS with 0 blockers)
- `reviewer_adversarial_layer_2_critique_sha256` (sha256 — pinned at Layer-2 T09 after signoff, before artifact CSV finalization)

Net change: +2 columns (2 originals → 4 replacements). New BINDING assumptions `A27` (Layer-1 SHA timing discipline) + `A28` (Layer-2 SHA timing discipline). Three new falsifier keys (`omit_closure_reviewer_signoff_layer_1_missing_or_invalid_sha`, `omit_closure_reviewer_signoff_layer_2_missing_or_invalid_sha`, `omit_closure_reviewer_signoff_layer_1_or_layer_2_not_approve_with_zero_blockers`). Artifact MD §19 split into §19.1 Layer-1 Sign-Off + §19.2 Layer-2 Sign-Off. T01 instructions extended to compute Layer-1 SHA at execution-start. T09 instructions extended to compute Layer-2 SHA AFTER reviewer-adversarial signoff and BEFORE artifact CSV finalization (with a re-run loop for the sandbox notebook to regenerate the artifact CSV referencing the post-signoff SHA).

### Schema column count delta

- Round 1 schema: 42 columns.
- NIT #1: +1 (`branch_ii_state_semantic_anchor`).
- NIT #4 net: +2 (replaced 2 columns with 4 = +2 net; Round-2 schema also relocated 2 module-SHA columns out of the CSV to module constants, which reduces the gross column budget by 2 — see R2-N1 below).
- NIT #3: +1 (`elevation_rationale_jaccard_vs_q6h_section_15`).
- NIT #2: 0 (Schema Derivation is a plan section, not a schema column).

**Final Round-2 schema column count: 45 columns.** The enumeration in `## Future Artifact Contract` lists 45 columns in canonical order. `assert len(OMIT_CLOSURE_SCHEMA) == 45` is asserted at module load (T02) and in the test contract (T03).

---

## Round 2 reviewer-adversarial verdict (2026-05-27)

**Reviewer agent:** reviewer-adversarial (Opus)
**Inputs reviewed:** Round-2 plan (`/tmp/plan_02_01_99/round_2_plan.md`; 998 lines; 45-column schema) + Round-1 plan for diff comparison + this critique file's Round-1 record.
**Base ref:** `a9cf552f346d8402fa4856fbee51fa34b0b0cefe` (master HEAD at plan time; unchanged from Round 1).
**Adversarial round:** 2 of 3 (planning-side).

### Round-2 nit-resolution audit (8 sub-checks)

| Sub-check | Result | Evidence |
|-----------|--------|----------|
| R2-NIT-1 (NIT-1 baked in) | PASS | Column 14 + A26 + falsifier + MD §4.2 verbatim Q6H quotes (lines 442–448, 457–481) |
| R2-NIT-2 (NIT-2 baked in) | PASS | `## Schema Derivation` section between Future Artifact Contract and Future Tests Contract; 7 deviations mapped; MD §11 reproduction mandated |
| R2-NIT-3 (NIT-3 baked in) | PASS | Column 13 + A29 (threshold 0.5) + falsifier + `_tokenize_for_jaccard()` + `_compute_jaccard()` in T02 + test in T03 + pre-emit verification in T04 |
| R2-NIT-4 (NIT-4 baked in) | PASS | Columns 15-18 + A27 + A28 + 3 falsifiers + MD §19.1/§19.2 split + T01/T09 timing |
| R2-S1 (42 references ≤ 5) | PASS | 9 total `42` occurrences; all in Round-1-history narrative |
| R2-S2 (45 references in N+ schema-count contexts) | PASS | 27 total `45` occurrences across §Scope, §Future Artifact Contract, §Schema Derivation, T02 module, T03 test, §File Manifest, §Gate Condition, §Reviewer-Adversarial Charter, etc. |
| R2-S3 (column-count arithmetic) | PASS-WITH-NOTE | Schema enumeration is canonical and correct (45 cols); explanatory arithmetic in `## Adversarial-Review Adjustments` is slightly muddled — see R2-N1 below |
| R2-S4 (column ordering canonical) | PASS | 4 NIT-4 columns at positions 15-18 in single canonical order, self-consistent across §Future Artifact Contract, §Schema Derivation, §Gate Condition, §Reviewer-Adversarial Charter |

### Round-2 re-issued 26 Round-1 axes (under Round-2 conditions)

All 26 Round-1 axes re-issue as STILL PASS or RE-PASS under Round-2 conditions:

**Planner-charter (1–15):** 1 STILL PASS, 2 STILL PASS, 3 STILL PASS, 4 STILL PASS, **5 RE-PASS** (NIT-3 Jaccard falsifier strengthens), **6 RE-PASS** (NIT-1 anchor column strengthens), 7 STILL PASS, 8 STILL PASS, 9 STILL PASS, **10 RE-PASS** (NIT-1 `is_new_q6x_loop=FALSE` assertion strengthens), 11 STILL PASS, 12 STILL PASS, 13 STILL PASS, **14 RE-PASS** (5 new Round-2 tests added; estimate 55–85 total), 15 STILL PASS.

**User-prompt (A1–A11):** A1 STILL PASS, A2 STILL PASS, **A3 RE-PASS** (NIT-1 strengthens), A4 STILL PASS, A5 STILL PASS, A6 STILL PASS, **A7 RE-PASS** (NIT-1 strengthens), A8 STILL PASS, A9 STILL PASS, A10 STILL PASS, A11 STILL PASS.

### Round-2 NEW axes (R-16 .. R-22)

| # | Axis | Result |
|---|------|--------|
| R-16 | Anchor format defensibility (4-key semicolon vs 4-column split) | PASS — atomic + grep-able + matches `five_family_set`/`excluded_columns` precedent |
| R-17 | Dual signoff structural coherence (boolean+SHA pair) | PASS-WITH-NOTE — slightly redundant but user-mandated; not blocking |
| R-18 | Jaccard threshold defensibility (0.5) | PASS-WITH-NOTE — reasonable ceiling; lacks empirical calibration but T04 pre-emit verification is the right escape valve |
| R-19 | Jaccard tokenisation determinism | PASS-WITH-NOTE — ASCII punctuation strip is brittle to Unicode; see R2-N2 below |
| R-20 | T01/T09 timing discipline coherence | PASS — defensible end-to-end via T09 regeneration loop; bounded by 3-round cap |
| R-21 | Schema Derivation completeness | PASS — all 7 deviations mapped to reviewer concerns with substantive rationale |
| R-22 | Round-2 planner self-critique completeness | PASS — S-9/S-10/S-11 cover the 3 Round-2-likely-new-reviewer-concerns |

### Round-2 verdict

```
ROUND-2 VERDICT: APPROVE-WITH-NITS (zero blockers, 3 nits)
PR MATERIALIZATION AUTHORISED: YES
RATIONALE: All 4 Round-1 nits cleanly baked in; 45-column schema is self-consistent; 26 Round-1 axes + 7 Round-2 axes all PASS or PASS-WITH-NOTE; the 3 Round-2 nits are surface-level (arithmetic prose, Unicode tokenisation, parent-SHA label) and explicitly recommended for Layer-2 dispatch (not Round 3).
```

### Round-2 blockers

NONE.

### Round-2 non-blocking nits — recorded as **Layer-2 dispatch requirements** (NOT Layer-1 blockers)

Per user directive (verbatim): "Layer-2 must later address them before final execution gate. Do not use Round 3 for these nits. Preserve the final planning-side adversarial round for genuine blockers."

**R2-N1 — Schema arithmetic prose clarification (Layer-2 T02 amendment scope).**
The `## Adversarial-Review Adjustments` section's arithmetic line reads "42 + 1 + 2 + 1 = 45" which sums to 46 unless the reader independently knows Round 2 also relocated 2 module-SHA columns out of the CSV to module constants. The schema enumeration (cols 1–45) is canonical and correct; only the explanatory arithmetic is muddled.
**Layer-2 fix:** amend the arithmetic explanation to surface the Round-2 schema simplification: "42 + 1 (NIT #1) + 2 (NIT #4 net: 2 → 4) + 1 (NIT #3) − 1 (Round-2 simplification: 2 module-SHA columns relocated from CSV to module constants) = 45."
**Binding:** canonical 45-column schema remains BINDING; this nit is prose-only.

**R2-N2 — Unicode-safe Jaccard tokenisation (Layer-2 T02 amendment scope).**
A29 specifies `str.translate(str.maketrans("", "", string.punctuation))` which is ASCII-only. Unicode characters in Q6H §15 or rationale text (em-dash `—`, en-dash `–`, curly quotes `"` `"`, ellipsis `…`, non-breaking space) will NOT be stripped, potentially causing artificially low Jaccard scores (paraphrase passes via Unicode swap). Risk in practice is low (the executor authors both texts fresh from the same MD source) but the discipline should be deterministic and Unicode-safe.
**Layer-2 fix:** amend A29 and the `_tokenize_for_jaccard()` implementation to apply Unicode normalisation + Unicode punctuation stripping. Recommended pattern:
```python
import unicodedata
def _tokenize_for_jaccard(text: str) -> set[str]:
    lowered = unicodedata.normalize('NFKD', text).lower()
    stripped = ''.join(c for c in lowered if not unicodedata.category(c).startswith('P'))
    return set(stripped.split())
```
**Binding:** Jaccard threshold 0.5 remains BINDING; falsifier remains in roll-call.

**R2-N3 — Parent-SHA label off-by-one (Layer-2 T02 amendment scope).**
T01 step 8 wording says "Verify the 11 pinned parent SHAs (PR #242/#243/#245/#247/#249)". Those 5 PRs contribute exactly 10 SHAs (2 per PR × 5 PRs); the 11th provenance value is `head_master_sha_at_layer_1_plan_time` (NOT a parent-PR SHA).
**Layer-2 fix:** correct the T01 step 8 wording to: "Verify the 11 pinned provenance values: 10 parent SHAs from PR #242/#243/#245/#247/#249 (2 per PR × 5 PRs) + `head_master_sha_at_layer_1_plan_time` (1 master HEAD SHA pin)."
**Binding:** provenance count of 11 hard-coded entries remains BINDING; this nit is label-only.

### Round-2 informational notes

- The Round-2 plan is substantively stronger than Round-1: three new structural guardrails (Jaccard falsifier, semantic-anchor 4-key format, dual signoff timing) augment the substantive reviewer-adversarial guardrail without introducing new methodology risk.
- The "Round-2 schema simplification" (relocating 2 module-SHA columns out of the CSV) is currently a parenthetical comment; R2-N1 surfaces it explicitly.
- S-10 ("Is the dual sign-off discipline operationally feasible?") is the load-bearing planner self-critique; the 3-round cap bounds the T09 regeneration loop to 3 iterations, which is operationally tractable and precedented in Q-chain Layer-2 PRs.
- Round 3 should NOT be used; R2-N1/N2/N3 fold cleanly into Layer-2 dispatch.

---

## Layer-2 dispatch requirements (Round 2 nits to address BEFORE Layer-2 final execution gate)

Per user directive (verbatim, recorded for the Layer-2 planning round):

> Layer-2 must later address them before final execution gate:
>
> 1. **R2-N1**: fix/clarify schema arithmetic prose; canonical 45-column schema remains binding.
> 2. **R2-N2**: implement Unicode-safe tokenisation for the Jaccard anti-boilerplate falsifier: `unicodedata.normalize('NFKD', text)`, Unicode punctuation stripping, and deterministic token handling.
> 3. **R2-N3**: correct the parent-SHA label: 10 artifact SHAs from PR #242/#243/#245/#247/#249 plus `head_master_sha_at_layer_1_plan_time` = 11 provenance values.
>
> Do not use Round 3 for these nits. Preserve the final planning-side adversarial round for genuine blockers.

The Layer-2 planning round (separate downstream PR cycle that opens after this Layer-1 PR merges) MUST surface these as Round-1 binding nits to the Layer-2 planner-science prompt, so the Layer-2 plan addresses them in `## Adversarial-Review Adjustments` of the Layer-2 plan.

---

## Hard stops for this Layer-1 PR (per user directive, verbatim)

> Do not touch ROADMAP, status YAMLs, research_log, CHANGELOG, pyproject, INDEX, source/tests/notebooks/artifacts, Phase 03, Step 02_01_04, or any materialization output in this Layer-1 PR.

The 2-file diff:
- `planning/current_plan.md` (998 lines; Round-2 plan body)
- `planning/current_plan.critique.md` (this file)

No other repo file is modified.

---

## Execution-side Round 1 verdict (placeholder; T09 of the future Layer-2 PR)

To be filled in by reviewer-adversarial agent at T09 of the future Layer-2 omit-closure-artifact execution PR.

- **Verdict:** TBD
- **Blockers:** TBD
- **Notes:** TBD

---

## Execution-side Round 2 verdict (placeholder; only if execution-side Round 1 = HOLD)

- **Verdict:** TBD
- **Blockers:** TBD

---

## Execution-side Round 3 verdict (placeholder; only if execution-side Round 2 = HOLD)

- **Verdict:** TBD
- **Blockers:** TBD

If execution-side Round 3 verdict is HOLD, execution halts and escalates to user per `feedback_adversarial_cap_execution.md`.

---

## Final approval gate (Layer-1)

Round-1 verdict APPROVE-WITH-NITS + Round-2 verdict APPROVE-WITH-NITS authorise this Layer-1 planning PR to materialize (2-file commit + draft PR creation). The 3 Round-2 nits R2-N1/R2-N2/R2-N3 are explicitly recorded as **Layer-2 dispatch requirements**; they do NOT block this Layer-1 PR's materialization or merge. The 3-round adversarial cap is preserved with 1 round unused (held in reserve for genuine blockers if any emerge in a hypothetical re-plan trigger).

PR state: DRAFT. Not marked ready. Not merged. Layer-2 dispatch deferred to a separate downstream session.
