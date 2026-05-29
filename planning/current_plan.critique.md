---
title: "Reviewer-adversarial critique — SC2EGSet Step 02_02_01 source-anchor / column-naming / direction-policy adjudication planning PR"
plan_ref: planning/current_plan.md
category: A
branch: feat/sc2egset-02-02-01-symmetry-difference-adjudication
base_ref: master
base_sha: 9abcd6bc62e1de21172970baf84aa863c4423a1b
dataset: sc2egset
phase: "02"
adversarial_cap: 3
rounds_run: 2
final_verdict: APPROVE-WITH-NITS
blockers: 0
nits: 6
date: 2026-05-29
---

## Adjudication outcomes (cross-reference)

The planner selected **Outcome A** — `02_02_01` feature-scope / source-anchor / transform-policy adjudication planning PR — and rejected B–G with repo-evidence justification (`planning/current_plan.md` §"Problem Statement" + Round 1 chat-side rejection of B–G). The reviewer ratified Outcome A in both rounds.

## Round 1 — verdict: HOLD (3 blockers)

Round 1 plan was the initial Round-1 draft (recorded at `.github/tmp/planner_output.md`). Reviewer passed 8 of 11 hard checks and identified three methodology BLOCKERs:

### Round 1 BLOCKERs

- **B1 — F4 "Matchup history pair operations" methodologically vacuous.** `matchup_h2h_focal_win_rate` is the only matchup-rate column in the audited 24-tuple; there is no `matchup_h2h_opponent_win_rate` audited counterpart. Treating it as a paired focal/opponent operation with "implicit complement `1 - matchup_h2h_focal_win_rate`" yields `2*focal - 1`, an affine transform of the same column — zero linear-model information gain, zero tree-splitting effect.
- **B2 — A14 algebra error.** Round 1 stated "drop `product` because mean * 2 = sum." Correct algebra: `sum = 2*mean`, so `sum` (not `product`) is redundant with `mean`. `product = focal * opponent` is a genuine multiplicative interaction.
- **B3 — `abs_diff` exclusion incompatible with LogReg under Invariant I8.** I8's cross-game protocol requires LogReg. For LogReg, `|focal - opponent|` is NOT a linear function of `(focal - opponent)` and CANNOT be recovered from the signed term. Round 1's "tree models can route the sign" rationale leaves LogReg without a symmetric-magnitude basis vector.

### Round 1 NITs

- **N1** — Validator name-direction ambiguity in F4 templates; mooted if F4 is dropped.
- **N2** — MD §3 row-count language should distinguish documentary future-materialisation gate from runtime promise.

### Round 1 item-by-item passes (8 of 11)

`Q1 PASS` adjudication-vs-validator boundary · `Q2 PASS` direct-materialization premature · `Q3 PASS` filename / path conventions match PR #234 / PR #242 precedent · `Q4 PASS` source-column traceability enforceable via validator's frozen 7-tuple / 24-tuple constants · `Q5 PASS` slot-bias regex coverage sufficient · `Q6 PASS` race-pair deferral to 02_05 correct per manual §6 · `Q7 PASS` `reconstructed_rating` exclusion airtight via validator's `BLOCKED_FAMILY_FRAGMENTS` · `Q8 PASS` no status / research_log / ROADMAP / Phase-03 work planned · `Q9 PASS` no feature artifact / audit artifact planned · `Q10 FAIL` CSV/MD content unsound (encodes B1/B2) · `Q11 FAIL` blockers present.

Round 1 final stamp: **HOLD — REDESIGN BEFORE EXECUTION.**

## Round 2 — verdict: APPROVE-WITH-NITS (0 blockers, 6 nits)

Round 2 plan revised per user-bound resolutions (drop F4 as pair operation; fix A14 algebra; include `abs_diff` for numeric pairs). Reviewer confirmed all three Round 1 BLOCKERs resolved, validated four Round-2 collateral changes, audited methodology defensibility, and engaged with all eight planner-self-flagged Round 2 risks.

### Round 2 BLOCKERs

**None.**

### Round 2 resolution-of-Round-1 checks (5 of 5 PASS)

- **R-B1 PASS** — F4 dropped in §Scope, Candidate feature families table, A20 binding, T01 instructions remove `BINDING_MATCHUP_HISTORY_PAIR_OPERATIONS`, halting falsifier `binding_matchup_history_pair_operations_symbol_present` added, gate clauses #2 + #18 added, tests `test_binding_matchup_history_pair_operations_symbol_absent` + `test_no_matchup_h2h_pair_candidate_in_difference_family`. No surviving reference treats F4 as a binding family.
- **R-B2 PASS** — A14 algebra is correct (`sum = 2*mean` cited; per-transform decisions independent: `mean` BIND / `abs_diff` BIND / `sum` EXCLUDE / `product` DEFER-TO-02_05 / `ratio` EXCLUDE); CSV column `symmetric_pair_aggregate_scope_decision` carries Round 2 string; MD §9.1–§9.4 each carry their own subsection; OQ7 + OQ11 record decision and re-open trigger; gate clauses #1, #20, #21 enforce.
- **R-B3 PASS** — `BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS = ("mean", "abs_diff")`; F3 family table row renamed to "Symmetric pair absolute difference" with name template `<stem>_pair_abs_diff`; T01 spec construction emits one `_pair_abs_diff` candidate per numeric pair; Literature Context Invariant I8 anchor justifies inclusion; tests + gate clause #19 enforce count.
- **R-N1 PASS** — A21 excludes the unary `2x-1` rescaling from the binding 02_02 set; informational only; test asserts no `matchup_h2h_focal_advantage` candidate constructed.
- **R-N2 PASS** — MD §3 head sentence carries the exact wording "documentary future-materialisation gate, not a runtime promise for the adjudication PR"; gate clause #8 greps for it; test `test_row_count_44418_is_documentary_not_runtime_promise` asserts presence.

### Round 2 collateral changes (4 of 4 PASS)

- **C1 PASS** — F5 BOOLEAN-pair naming rename to `cross_region_pair_{or,and,xor}` is substantive: the validator's `symmetric_tokens` list (`validate_symmetry_difference_feature_materialization.py:504-512`) explicitly contains `_pair_or`, `_pair_and`, `_pair_xor`. Round 2 naming aligns with these tokens exactly.
- **C2 PASS** — CSV 23-column choice (added `matchup_history_transform_decision`) makes the dropped-F4 decision machine-checkable via gate clause #18; without the column, gate clause #18 would require parsing MD §9.7 body.
- **C3 PASS** — Halting falsifier priority chain orders correctly: validator + parent SHA pins fire first; validator result-level falsifiers second; Round-2-anchored binding-constant falsifiers third; rendering / persistence falsifiers last.
- **C4 PASS** — 21 gate clauses enumerated; six Round-2-anchored clauses (#2, #8, #18, #19, #20, #21) are each machine-verifiable; all clauses independent and orthogonal.

### Round 2 methodology defensibility

- **D1 LogReg basis completeness — NIT (N6).** Argument that LogReg requires `abs_diff` is correct and examiner-defensible. Argument is incomplete only insofar as the joint `(focal_minus_opponent, pair_mean, pair_abs_diff)` basis does NOT cover quadratic / product effects — but those are explicitly deferred to 02_05 with re-open trigger.
- **D2 `product` deferral to 02_05 — NIT (N1, N2).** Decision defensible: Pipeline-Section discipline argues 02_05 placement; re-open trigger documented. Supporting algebra claim is loose (N1) and manual §6 citation overstates its authority for numeric cross-products (N2 — manual §6 line 135 explicitly notes trees capture interactions naturally).
- **D3 F5 either/both/xor independence — NIT (N3).** Independence claim holds for tree models but fails for LogReg with regularization: `A OR B = (A AND B) OR (A XOR B)` makes the design matrix rank-2 over the 2-dim Boolean source. Decision to keep all three still defensible (trees benefit), but rationale must not claim non-redundancy for all model classes.
- **D4 Validator `_abs_diff` symmetric override — PASS.** Verified in validator source: line 517 explicit comment ("`_abs_diff` ends with `_diff` but is symmetric — symmetric wins"); lines 518-520 code branch `if has_sym: if spec.direction != "symmetric": return False; continue` ensures symmetric tokens override the diff-suffix rule. F3 family naming WILL pass `direction_name_consistency_ok` at adjudication runtime.

### Planner-self-flagged Round 2 risks (8 of 8 PASS / NIT)

`P1 NIT (N3)` F5 transform retention · `P2 NIT (N2)` `product` 02_05 deferral · `P3 PASS` abs_diff per-pair sweep default-include with re-open in §9.3 + OQ13 · `P4 PASS` CSV 23-column choice machine-checkable · `P5 PASS` MD §3 N2 wording placement at row-policy head · `P6 PASS` F5 rename substantive · `P7 PASS` halting falsifier additions appropriate · `P8 PASS` Round 2 new open questions (OQ7 / OQ11 / OQ12 / OQ13) correctly framed as re-open anchors.

## Round 2 NITs (6 — non-blocking; applied at Layer-2 execution)

| # | Maps to | Concern | Applied at Layer-2 by |
|---|---|---|---|
| **N1** | A14 / OQ7 / Literature Context [OPINION on B2] | "`product` is not expressible from `(mean, abs_diff)` alone" should read "not LINEARLY expressible". Identity `focal * opponent = mean^2 - (abs_diff/2)^2` makes product a quadratic polynomial in `(mean, abs_diff)`. Decision unchanged. | Wording fix in `[OPINION on B2]` (Literature Context) and MD §9.2. |
| **N2** | A14 / D2 / manual §6 lines 133-135 | Manual §6 line 135 notes trees capture interactions naturally; the `product -> 02_05` deferral rationale should acknowledge the Pipeline-Section placement is a convention choice, not a methodological necessity. | Tighten last sentence of `[OPINION on B2]`. |
| **N3** | A13 / D3 / OQ4 | F5 independence argument holds for trees; under LogReg with regularization the design matrix is rank-2 over the 2-dim Boolean source. Decision to retain all three transforms stands; rationale must not claim non-redundancy for all model classes. | Add LogReg-redundancy footnote to A13 and to MD §4 caption. |
| **N4** | A21 / N1 (R1) / OQ8 | A21's prescriptive "tag unary as `symmetric` by convention" pre-empts a future design choice; reframe as open design question (a unary feature is, strictly, neither `focal_minus_opponent` nor `symmetric` under the binary Literal). | Soften A21 last paragraph; promote to OQ8 explicit re-open. |
| **N5** | U2 / Gate clause #19 / OQ13 | Gate clause #19 wording "(or whatever the exact pair count is at execution time)" softens a deterministic gate. Replace with internal-consistency assertion: `count(_pair_abs_diff specs) == len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS) == binding_difference_family_numeric_pair_count CSV column`. | Strengthen gate condition #19 and add corresponding consistency test. |
| **N6** | A14 / B3 anchor / D1 | LogReg / abs_diff argument is complete on the signed-vs-magnitude axis but does not cross-link to the `mean`-inclusion rationale. Recommend MD §9.3 explicitly note that the joint basis `(focal_minus_opponent, pair_mean, pair_abs_diff)` spans linear-in-signed-difference, linear-in-mean-level, and linear-in-symmetric-magnitude; quadratic effects (`focal^2`, `opponent^2`, `product`) remain unrecoverable without polynomial terms — these are the 02_05 deferral surface. | Add §9.3 cross-link paragraph in MD. |

All six nits are wording / cross-link refinements applied during Layer-2 adjudication execution. No Round 2 binding decision changes; no Round 3 adversarial pass needed.

## Adversarial cap status

- Round 1: HOLD — 3 BLOCKERs.
- Round 2: APPROVE-WITH-NITS — 0 BLOCKERs, 6 NITs.
- Round 3: **not required** (the 3-round symmetric cap permits Round 3 only if Round 2 returns HOLD).

## Files inspected by reviewer

- `.claude/scientific-invariants.md` (I3, I5, I8 anchors)
- `.claude/rules/data-analysis-lineage.md`
- `docs/ml_experiment_lifecycle/02_FEATURE_ENGINEERING_MANUAL.md` (§3 Bradley-Terry; §6 categorical interactions)
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py` (validator: 7-tuple at 105-113, 24-tuple at 116-141, symmetric tokens at 504-512, `_abs_diff` override at 517-520)
- `.github/tmp/planner_output.md` (Round 1 plan baseline)
- `.github/tmp/planner_output_r2.md` (Round 2 plan — full read)

## Sources cited

- Bradley & Terry 1952, *Biometrika*: "Rank Analysis of Incomplete Block Designs" — Bradley-Terry difference-feature argument grounding F1 / F2 / F3 binding direction policy.
- Hue & Vert ICML 2010: "On Learning with Kernels for Unordered Pairs" — symmetric kernel theory grounding F2 / F3 / F5 symmetric direction.
- Zaheer et al. 2017: "Deep Sets" — permutation-invariant set functions for symmetric features (referenced in `02_FEATURE_ENGINEERING_MANUAL.md` §3 line 56).
- Kuhn & Johnson 2019, *Feature Engineering and Selection*: Lasso-screening for polynomial / interaction features (referenced in `02_FEATURE_ENGINEERING_MANUAL.md` §6 line 135).
