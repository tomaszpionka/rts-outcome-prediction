---
critique_role: reviewer-adversarial
critique_model: claude-opus-4-7[1m]
critique_date: 2026-05-26
plan_ref: planning/current_plan.md
plan_date: 2026-05-25
base_ref: 779dc40a36765d90034181fc3885ea32cab204e6
branch: feat/sc2egset-02-01-03-q6g-rating-implementation-proof
chosen_outcome: A
final_verdict: APPROVE-WITH-NITS
blockers: 0
nits_round_1_incorporated: 6 of 6
nits_round_2_remaining: 2 (R2-N1, R2-N2; both non-blocking)
adversarial_rounds_consumed: 2 of 3
parent_planning_pr: 246 (merged 2026-05-25; Q6F Layer-1)
parent_execution_pr: 247 (merged 2026-05-25; Q6F Layer-2; verdict narrow_with_evidence)
parent_q5_pr: 243 (Q5 BINDING preserved; sensitivity_indicator_co_registration)
parent_q6_pr: 245 (Q6 BINDING discharged by Q6F)
---

# Reviewer-Adversarial Critique — Q6G Layer-1 plan (Round 1 + Round 2)

This critique consolidates two adversarial rounds against the Q6G rating-implementation-proof Layer-1 plan. Round 1 (HOLD) identified a methodology BLOCKER and 6 NITs; the planner produced a Round 2 amendment incorporating all of them as binding methodology. Round 2 (APPROVE-WITH-NITS) verified each amendment is materially addressed and found 2 additional non-blocking nits.

Round 3 of the Layer-1 cap is reserved; it will be invoked only if the Layer-2 execution PR's reviewer surfaces a Layer-1-traceable defect.

---

## Round 1 — HOLD pending BLOCKER-1 resolution

**Reviewer:** `@reviewer-adversarial`
**Date:** 2026-05-25
**Verdict:** **HOLD** pending BLOCKER-1 resolution; otherwise APPROVE-WITH-NITS.

### Per-challenge findings (10 challenges)

**(1) Q6G as next atomic step.** PASS. The Q6F binding row (`02_01_03_q6f_rating_algorithm_survey.md` §12 lines 121, 129; §13 lines 194–205) sets `materialization_permission = recommendation_only_blocked_pending_implementation_proof_pr` for ALL six families, including `omit_reconstructed_rating`. The smaller "execute omit + unblock five" path still requires an implementation-proof PR — it cannot bypass Q6G's class. Outcome B is correctly rejected; OQ5 honestly parks the omit-closure question. No finding.

**(2) Materialization planning is still barred.** RESPECTED. Q6F MD §13 (lines 194–205) literally states "Materialization permission ... `recommendation_only_blocked_pending_implementation_proof_pr`" for all 6 families and "Future feature materialization is a SEPARATE PR (Layer-3) ... subject to its own CROSS-02-01 post-materialization leakage audit." A materialization-planning PR before the proof would be a verdict-text violation. Plan honors this.

**(3) Implementation-proof vs feature materialization boundary.** WARNING — boundary is sharp in text, fragile in artifact form. The plan's "small 5x3 markdown table" sample (OQ4 default) of rating mu values would BY CONSTRUCTION be a persisted, citable rating output. An examiner distinguishing "evaluation trace" from "feature materialization" sees the same tuple as both. → **Triggers NIT-N1.**

**(4) Glicko-2 defensible despite TrueSkill CI overlap.** AT RISK — proof-path `bind_glicko2_forward_only` may be unreachable. Q6F §11 table shows Glicko-2 log-loss CI [0.6216, 0.6302] vs TrueSkill [0.6246, 0.6342] — overlap of 0.0056 (about 0.9% of mid). Batched volatility correction (Glickman 2012 §7) does not systematically shift Glicko-2 log-loss in either direction at this sample size with `rating_period_days=30`. Realistic outcome is `recommendation_only_glicko2`, not `bind_now`. → **Triggers NIT-N2.**

**(5) `omit_reconstructed_rating_and_unblock_other_five` must remain an outcome.** RESPECTED-as-needed. Q6F §12 explicitly preserves both `omit_reconstructed_rating_and_unblock_other_five` (decision rule branch 4) and `narrow_with_evidence` (branch 3) as outcomes. Removing proof-path C from Q6G would silently narrow the deterministic adjudication rule that Q6F published, which would itself be a Q6F re-adjudication.

**(6) Event-by-event Glicko-2 simplification.** **BLOCKER-class methodology nit.** PR #245 / Q6F §8 (Glicko-2 specification) states verbatim: "Event-by-event simplification ... Sigma held constant ... the full batched volatility update is deferred to a future Q6G PR." Q6G MUST implement batched Glicko-2 per Glickman (2012) Example §2–§7. Reporting BOTH variants is necessary but INSUFFICIENT: the plan must additionally prove an ordering-equivalence bound (Spearman ρ ≥ 0.99 OR Kendall τ ≥ 0.95 on per-player rating trajectories AND log-loss delta within ±1·SE). Without such a bound, Q6F's evidence (collected under the event-by-event simplification) does NOT transfer to a `bind_now` under the batched algorithm. → **BLOCKER-1.**

**(7) Q5 binding policy preserved.** RESPECTED. PR #243 MD line 22 binds `Q5_selected_policy = sensitivity_indicator_co_registration` with verdict `narrow_with_evidence`; line 213 explicitly notes "Q6 remains deferred." Plan §Assumption 6 + falsifier `q6g_q5_re_adjudication_drift` preserve. Verified.

**(8) Schema gaps.** WARNING — the proposed 34-column Q6G proof schema needs additions: `bootstrap_random_seed`, `rating_period_days` (separate column), `cold_start_threshold_n_games`, `numpy_rng_bit_generator`, `python_floating_point_summation_order_policy`, `glicko2_volatility_iteration_convergence_tol`. Q6F CSV uses 44 columns; Q6G uses 34. Justify the asymmetry, else the schema is arbitrary by examiner standards. → **Triggers NIT-N3.**

**(9) No status YAML / research_log / ROADMAP / Phase 03 mutations.** RESPECTED. Plan §Out-of-scope lists 26 falsifier-tied prohibitions explicitly covering all six mutation targets. The 2-file Layer-1 manifest verifiably excludes them. Verified.

**(10) Defensibility weaknesses for the examiner.** AT RISK — three concerns:
- (i) The 4-proof-path adjudication relies on bootstrap CI re-evaluation but deepens dependence on a single resampling scheme; the plan should pre-commit to a deterministic bootstrap method and document the random seed before generation, not after. → **Triggers NIT-N6.**
- (ii) Player identity = `toon_id` (region-scoped) carries forward an examiner-objectionable asymmetry: ratings cannot follow players across region migrations. Without an explicit cited acknowledgement in §Limitations, the proof's own validity inherits Invariant #2 risk. → **Triggers NIT-N4.**
- (iii) The plan defers `rating_period_selection` to a literal 30-day default with no sensitivity sweep. For a thesis-grade proof, at minimum a {7d, 30d, 90d} sensitivity arm is required to refute "30d was a magic number" (Invariant #7). → **Triggers NIT-N5.**

### Round 1 BLOCKER

**BLOCKER-1 (Challenge 6):** Q6G must prove batched vs. event-by-event Glicko-2 ordering equivalence to a documented bound (Spearman ρ ≥ 0.99 AND |Δ log-loss| ≤ 1·SE). Add this as a binding acceptance criterion in the Layer-2 gate AND as a falsifier `q6g_batched_event_ordering_equivalence_unproven`. Failure of the bound forbids `bind_now`; fallback to `recommendation_only_glicko2`, `defer_to_two_candidate_implementation_comparison`, `omit_reconstructed_rating_and_unblock_other_five`, or `deferred_blocker`.

### Round 1 NITs (6)

- **NIT-N1** (Challenge 3) — MD §10 sample emission must be probability-only (5 floats in [0,1]); add falsifier `q6g_raw_mu_or_sigma_persisted_in_md` to make the materialization-boundary sharp.
- **NIT-N2** (Challenge 4) — Make `recommendation_only_glicko2` the default expected outcome in OQ1 prose; the data already weakly favors it.
- **NIT-N3** (Challenge 8) — Add 5 schema columns (`bootstrap_random_seed`, `rating_period_days`, `glicko2_iteration_tol`, `numpy_rng_bit_generator`, `python_floating_point_summation_order_policy`). Justify the schema delta against the Q6F CSV explicitly.
- **NIT-N4** (Challenge 10.ii) — Add §Limitations paragraph: "`toon_id` is region-scoped per Invariant #2 branch (iii); rating fragmentation across region-migrating players is an accepted bias for Q6G."
- **NIT-N5** (Challenge 10.iii) — Add OQ6: rating_period_days `{7, 30, 90}` sensitivity arm — emit OR cite Glickman 2012 §10 as accepted default.
- **NIT-N6** (Challenge 10.i) — Pre-commit to bootstrap method (BCa vs percentile) and seed in the Layer-1 plan; do not let the executor pick.

### Round 1 audit trail

- Round 1 of 3 adversarial cap consumed.
- Files cross-checked on master: Q6F MD §12–13 (lines 117–205); Q6F MD §8 (Glicko-2 line 74); Q6F CSV header (44 columns); PR #243 MD lines 22, 213; PR #245 MD §1, §6, §10, §12.

**Round 1 VERDICT: HOLD** pending BLOCKER-1 resolution; otherwise APPROVE-WITH-NITS.

---

## Round 2 — APPROVE-WITH-NITS (zero blockers)

**Reviewer:** `@reviewer-adversarial`
**Date:** 2026-05-26
**Verdict:** **APPROVE-WITH-NITS** (zero blockers; 6 of 6 Round 1 NITs incorporated; 2 new R2 non-blocking nits).

### Per-amendment verification

**BLOCKER-1:** PASS — A19 (lines 152–157 of `planning/current_plan.md`) binds Spearman ρ ≥ 0.99 AND |Δ log-loss| ≤ 1 SE with deterministic-percentile-bootstrap SE formula `(CI_high − CI_low) / (2 × 1.96)` from PR #247-derived CI. Falsifier `q6g_batched_event_ordering_equivalence_unproven` registered. Row 3 (`Q6G_C_glicko2_event_vs_batched_equivalence_proof`) is enumerated at line 123 and computed at T05 step 1 BEFORE Row 5's decision rule (T05 step 4). Guard falsifier `q6g_bind_now_emitted_without_equivalence_pass` is wired in T01 falsifier chain, T05 step 5, Gate clause (b3), and test `TestBlockerGuard_BindNowRequiresEquivalence`. Decision rule middle branch correctly falls back to `recommendation_only_glicko2` when either bound fails. Bounds are concrete numerics, not handwave.

**NIT-N1:** PASS — A20 (line 159) pins exactly 5 floats in [0,1] for MD §10. T06 step 4 implements the probability-only sample table; T06 step 5 implements the writer-time grep check. Gate clauses (a4) and (a5) enforce. Test `TestNIT_N1_MDSampleIsProbabilityOnly` covers. Falsifier `q6g_raw_mu_or_sigma_persisted_in_md` registered. MD §8 is the only allow-listed section for Glicko-2 symbols.

**NIT-N2:** PASS — OQ1 (line 743) names `recommendation_only_glicko2` as default expected outcome; quotes Q6F §11 CI overlap (Glicko-2 [0.6216–0.6302] vs TrueSkill [0.6246–0.6342], 0.9% of mid-range) at lines 67 and 416–419. Decision rule middle branch carries the explicit CI-overlap rationale string. Scope outcome #3 is labelled "NIT-N2 default expected outcome."

**NIT-N3:** PASS — A21 introduces the 5 constants; lines 261–265 enumerate columns 35–39 (`bootstrap_random_seed`, `rating_period_days`, `glicko2_iteration_tol`, `numpy_rng_bit_generator`, `python_floating_point_summation_order_policy`). Module assertion at T01 step 13 (`assert len(Q6G_PROOF_SCHEMA) == 39`), `TestModuleConstants`, Gate (c1) reconciling 4 places, MD §11 column-count assertion. Q6F-vs-Q6G schema delta explained (44 vs 39: 4-candidate CI block vs 2 proof-class JSON columns).

**NIT-N4:** PASS — Explicit `### Limitations` subsection inserted between Assumptions and Unknowns (lines 171–175); cites Invariant #2 branch (iii) verbatim; declares rating fragmentation across region-migrating players as accepted Q6G bias; mandates verbatim restatement in MD §15.

**NIT-N5:** PASS — OQ6 (line 748) records default = Glickman 2012 §10 (30 days, worked example) and explicitly defers `{7, 30, 90}` sensitivity arm to future Q6H or Layer-3-internal sensitivity step. A22 pins. §Out of scope lists explicitly. Falsifier `q6g_rating_period_days_not_30` registered.

**NIT-N6:** PASS — A21 (lines 161–167) pre-commits 5 constants: `BOOTSTRAP_METHOD = "deterministic_percentile"`, `BOOTSTRAP_RANDOM_SEED = 42`, `BOOTSTRAP_BLOCK_COUNT = 200`, `NUMPY_RNG_BIT_GENERATOR = "PCG64"`, `PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY = "sorted_then_kahan"`. T04 step 2 implements via PCG64 + percentile bootstrap. Percentile-over-BCa justification at line 197 (one paragraph; [OPINION] flagged; Efron & Tibshirani 1993 cited). Six dedicated falsifiers registered.

### Round-2-fresh challenges

**R2-NEW-1 (Spearman ordering determinism):** PASS — T03 step 7 pins sort key `(toon_id, timestamp, replay_id)` for the batched-path log-loss accumulation. T02 step 1 mandates the loader uses "same query as PR #247 §T02". T05 step 1 applies `~is_cold_start` mask identically to both paths before computing Spearman and uses `scipy.stats.spearmanr(...).statistic` with tie-averaged ranks. Determinism of the Spearman rank statistic is inherited from PR #247's stream ordering plus the explicit shared mask.

**R2-NEW-2 (CSV-level enforcement of `bind_now` precondition):** PASS — Gate clause (b3) is a CSV-level reviewer-runnable check: "If Row 5's `proof_verdict == 'bind_now'`, then Row 3's `passes_spearman_bound == True` AND `passes_delta_log_loss_bound == True` AND Row 4's `hashes_equal == True`." Because Row 3's JSON column and Row 4's JSON column are serialized in the CSV (schema columns 24 and 25), the future PR's reviewer-adversarial can verify by parsing the CSV directly — no Python required. T05 step 5 also enforces in code; defense-in-depth.

**R2-NEW-3 (Determinism failure ⇒ no `bind_now`):** PASS — Decision rule first branch (lines 402–407) explicitly handles `IF NOT Determinism pass → deferred_blocker` with materialization_permission `"blocked_pending_byte_determinism_failure_investigation"`. The rule short-circuits to `deferred_blocker` regardless of equivalence pass. Gate (b3) also requires `Row 4's hashes_equal == True` for `bind_now`, making both proofs jointly necessary. Test `TestDecisionRule_AllThreeBranches` covers (a)(b)(c).

**R2-NEW-4 (No TrueSkill re-implementation in Q6G):** PASS — TrueSkill re-implementation is forbidden in 4 places: A5 (line 108), forbidden file row (line 656), falsifier `q6g_no_trueskill_re_implementation` (line 727), test `TestNoTrueSkillReImplementation` (line 530). Scope outcome #2 explicitly defers TrueSkill implementation to a hypothetical future Q6H.

**R2-NEW-5 (Test target realism):** WARNING — Test target was raised from ≥120 to ≥150 (A15, T08). However, the test enumeration lists only 17 test classes. Reaching 150 tests requires about 9 parametrised assertions per class on average. This is realistic for the falsifier chain (38 keys → 38+ parametrised tests in `TestFalsifierChain` alone), but the plan does not commit a per-class minimum or parametrisation guarantee. → **Triggers R2-N1 (non-blocking).**

### Round 2 blockers

**None.**

### Round 2 non-blocking nits

- **R2-N1** (from R2-NEW-5): The 150-test floor lacks per-class minimums. Layer-2 reviewer-adversarial should re-verify test density (not just count) at Layer-2 Round 1. **Recommendation:** Layer-2 executor pre-commits per-class minimums (e.g., `TestFalsifierChain` ≥ 38, `TestEquivalenceProof_*` ≥ 10, `TestDecisionRule_*` ≥ 6). Non-blocking — coverage gate (95% branch) is the harder constraint and survives the absence of per-class counts. **No change to this Layer-1 plan required.**
- **R2-N2** (cosmetic): The traceability table row for BLOCKER-1 (line 762) maps to Gate clause (b3) and now explicitly notes "(`bind_now` permitted only if equivalence pass + determinism pass)" — the polish recommended by Round 2 is already inline. **Pre-commit by user directive incorporated.** Status: addressed in the plan as-written; no further action.

### Round 2 audit trail

- Adversarial cap consumed: Round 2 of 3.
- Round 1 BLOCKER status: **RESOLVED** (BLOCKER-1 bound to A19 + 2 falsifiers + Gate b3 + decision-rule guard + dedicated test `TestBlockerGuard_BindNowRequiresEquivalence`).
- Round 1 NIT statuses: **6 of 6 incorporated** as binding methodology (not as prose-only acknowledgements). Each amendment is traceable via the §Adversarial-Review Adjustments traceability table at lines 760–768 of `planning/current_plan.md`.
- Files cross-checked on master: `planning/current_plan.md` (this revision, lines 152–157, 159, 161–167, 171–175, 261–265, 668–688, 743, 748); PR #247 CSV (44 columns; SHA `249e5591...`); PR #247 MD (18 sections; SHA `4b49bee4...`); PR #243 CSV (`29d39522...`); PR #245 MD (§1, §6, §10, §12).

**Round 2 VERDICT: APPROVE-WITH-NITS** (zero blockers; 2 non-blocking R2 nits informational only; Layer-2 dispatch authorised).

---

## Cap accounting

- Round 1 of 3 Layer-1 adversarial cap: **consumed (HOLD).**
- Round 2 of 3 Layer-1 adversarial cap: **consumed (APPROVE-WITH-NITS).**
- Round 3 of 3 Layer-1 adversarial cap: **reserved** — invoke only if Layer-2 execution PR's reviewer-adversarial surfaces a Layer-1-traceable defect.
- Layer-2 execution PR has a fresh 3-round adversarial cap per `feedback_adversarial_cap_execution.md` (symmetric application).

## Final gate

This Layer-1 PR is mergeable when:

1. Diff contains exactly 2 files: `planning/current_plan.md` + `planning/current_plan.critique.md`.
2. Branch matches `feat/sc2egset-02-01-03-q6g-rating-implementation-proof`.
3. Base ref = `779dc40a36765d90034181fc3885ea32cab204e6` (or a fast-forward descendant).
4. Pre-commit hooks pass (planning-artifact validation; no `.py` touched).
5. PR is ready (not draft) at gate review time.
6. Reviewer-adversarial verdict: **APPROVE-WITH-NITS** (zero blockers) — recorded here.

The Layer-2 execution PR's gate conditions are enumerated in §Gate Condition of the plan body. Layer-2 dispatch is authorised after this Layer-1 PR merges.
