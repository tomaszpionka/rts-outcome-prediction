---
plan_role: planner-science
plan_model: claude-opus-4-7[1m]
plan_date: 2026-05-25
date: 2026-05-26
plan_layer: 1 (planning-only; 2-file diff) — Round 2 amendment
chosen_outcome: A
branch: feat/sc2egset-02-01-03-q6g-rating-implementation-proof
future_layer2_version_bump: 3.76.0 -> 3.77.0
planning_pr_version_bump: none (planning-only; matches PR #240 / #244 / #246 precedent)
this_planning_pr_category: A
category: A
parent_planning_pr: 246 (merged 2026-05-25; Q6F Layer-1 plan)
parent_execution_pr: 247 (merged 2026-05-25; Q6F Layer-2 execution; verdict narrow_with_evidence; materialization recommendation_only_blocked_pending_implementation_proof_pr)
parent_q6_pr: 245 (merged; Q6_selected_policy = deferred_blocker_with_algorithm_survey_required; verdict deferred_blocker; BINDING)
parent_q5_pr: 243 (merged; Q5_selected_policy = sensitivity_indicator_co_registration; verdict narrow_with_evidence; BINDING)
parent_q1_q4_q7_q8_pr: 242 (merged; RATIFIED)
base_ref: 779dc40a36765d90034181fc3885ea32cab204e6
phase_status_at_plan_time: Phase 02 in_progress; Phase 03 not_started
step_status_at_plan_time: 02_01_01 complete; 02_01_02 complete; 02_01_03 in_progress (Q6F narrow_with_evidence → implementation-proof PR required)
non_batching_compliance: this Layer-1 plan does not author any Q6G implementation-proof module, validator, notebook, artifact, status YAML, or research_log; the Layer-2 PR is a separate dispatch
adversarial_round_cap: 3 (symmetric per feedback_adversarial_cap_execution.md); Round 1 consumed (HOLD); Round 2 consumed by upcoming dispatch on this amendment; Round 3 remaining
round_2_amendment: addresses BLOCKER-1 + NIT-N1..N6 verbatim
---
# Plan: SC2EGSet Step 02_01_03 — Q6G rating-implementation-proof Layer-1 (Round 2 amendment)

## Scope

This is the **Layer-1 planning-only PR** for the next atomic unit in SC2EGSet Step 02_01_03 after PR #247 merged. The outcome under planning is **A — Q6G rating-implementation-proof PR**.

The Layer-2 execution PR (named in the Future-Layer-2 manifest) will:

1. **Discharge the `recommendation_only_blocked_pending_implementation_proof_pr` materialization permission** that PR #247 (Q6F) emitted, by producing an implementation-proof artifact that:
   (a) re-runs the Glicko-2 forward-only engine on the PHA stream under **batched-update** (rating-period-batched per Glickman 2012 §3) semantics — the production-shaped path used at materialization — AND
   (b) **proves event-by-event vs. batched-update ordering equivalence** under a pre-pinned criterion (BLOCKER-1; see §Assumptions & Unknowns A19 and §Execution Steps T05);
   (c) emits **5 probability-only MD §10 samples** (NIT-N1) for byte-level inspection;
   (d) carries forward all Q6F prior bindings without re-adjudication (Q5, Q6F, Q1–Q4 / Q7 / Q8).
2. Persist **one (1) artifact pair** under `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`:
   - `02_01_03_q6g_rating_implementation_proof.csv` (**EXACTLY 39 columns** per NIT-N3; 5 rows: 4 substantive + 1 emergent verdict)
   - `02_01_03_q6g_rating_implementation_proof.md` (≥19 sections; §10 sample table emits **probability-only**, exactly 5 floats in [0, 1], NIT-N1)
3. Emit `Q6G_selected_policy` as an emergent row whose value is one of:
   - `bind_now` — Layer-3 materialization permitted with pinned Glicko-2 implementation & hyperparameters. **Permitted ONLY if** the BLOCKER-1 equivalence criterion (A19) passes.
   - `recommendation_only_glicko2` (NIT-N2 **default expected outcome**) — implementation proven correct for forward-only event-by-event ordering, but batched-vs-event equivalence is not strong enough to authorise a `bind_now` over the Q6F CI overlap (0.9% of mid-range).
   - `defer_to_two_candidate_implementation_comparison` — Q6G's single-candidate (Glicko-2) implementation proof is insufficient; a future Q6H PR must compare Glicko-2 vs TrueSkill implementations head-to-head.
   - `omit_reconstructed_rating_and_unblock_other_five` — implementation proof failed on the PHA corpus; reconstructed_rating column is permanently absent.
   - `deferred_blocker` — implementation proof produced an unrecoverable surprise that requires a different unblock; the Q6G row must name exact missing evidence.

This planning PR records:

- **2 files only**: `planning/current_plan.md` (this content; Round 2 amendment) + `planning/current_plan.critique.md` (reviewer-adversarial Round 2 stub).
- **NO version bump** in this PR (matches PR #240 / PR #244 / PR #246 planning-only precedent).
- **NO implementation-proof code**, **NO proof artifact**, **NO status YAML mutation**, **NO research_log entry**, **NO ROADMAP edit**, **NO Parquet output**, **NO CROSS-02-01 audit file**, **NO Step 02_01_03 closure**, **NO Phase 03 start**.

Branch: `feat/sc2egset-02-01-03-q6g-rating-implementation-proof`.

## Problem Statement

PR #247 (Q6F) selected `narrow_with_evidence` because the Glicko-2 candidate's log-loss CI (0.6216–0.6302) and TrueSkill's CI (0.6246–0.6342) **overlap** by 0.0056 (~0.9% of the mid-range), so no single candidate's proper-score improvement over the others is statistically separable on the sc2egset PHA corpus. The Q6F verdict's materialization permission is `recommendation_only_blocked_pending_implementation_proof_pr`. Q6F's §11 numbers therefore **do not** authorise a batched-update `bind_now` on their own (see A19 below).

The Q6G **implementation-proof** PR is the direct unblock condition for the `_blocked_pending_implementation_proof_pr` clause. It is **not** the only-possible unblock: the Q6G verdict may also defer to a Q6H two-candidate implementation comparison (Glicko-2 vs TrueSkill), or recommend omitting the rating column entirely.

Four distinct downstream artifacts must not be confused:

1. **The Q6G implementation-proof output (THIS planning's future Layer-2 PR).** Authors the byte-deterministic Glicko-2 production-shaped engine, the **event-vs-batched ordering-equivalence proof** (BLOCKER-1), the metric re-run, and the 5-probability sample table; picks `bind_now` / `recommendation_only_glicko2` / `defer_to_two_candidate_implementation_comparison` / `omit_reconstructed_rating_and_unblock_other_five` / `deferred_blocker`. **Does NOT materialize features.** **Does NOT train Phase-03 baselines.**
2. **The Layer-3 `reconstructed_rating` feature materialization PR.** Actually computes per-target-match Glicko-2 rating values, writes the 6-family Parquet, runs CROSS-02-01 audit. **OUT OF SCOPE** for Q6G.
3. **A possible Q6H two-candidate Glicko-2-vs-TrueSkill comparison PR.** Triggered only if Q6G selects `defer_to_two_candidate_implementation_comparison`. **OUT OF SCOPE** for Q6G.
4. **Phase 03 baseline / model-training cold-start (G-CS-6).** OUT OF SCOPE. Phase 03 remains barred per `PHASE_STATUS.yaml` (Phase 03 = `not_started`) and per `.claude/ml-protocol.md` §4.

### Why outcomes B–F are rejected

- **B — direct Layer-3 materialization (skip the implementation proof).** REJECTED: PR #247's materialization permission is `recommendation_only_blocked_pending_implementation_proof_pr`. Proceeding to Layer-3 materialization without the implementation proof would silently violate the Q6F-emitted gate.
- **C — direct two-candidate implementation comparison (Q6H now, skip Q6G).** REJECTED: Q6F selected Glicko-2 as the best-by-log-loss candidate; the minimum-unblock unit is to prove the chosen candidate's implementation is correct and equivalence-safe (BLOCKER-1), not to run a comparison that pre-supposes either candidate is implementation-ready.
- **D — Phase 03 baselines first.** REJECTED: identical rationale as Q6F's outcome-D rejection; the spec §6.2 row 4 still lists `reconstructed_rating` as part of the pre-game feature set, and Phase 03 may not consume an unproven feature.
- **E — hygiene-only PR first (e.g., addressing PR #247 cosmetic nits).** REJECTED: PR #247 merged as APPROVE-WITH-NITS with no methodology blockers; no real obstacle exists; a hygiene PR would delay Q6G without removing any obstacle.
- **F — hold (no PR; await user direction).** REJECTED: PR #247's Q6F verdict explicitly names the next required step as the `implementation-proof PR`; the user has standing direction; holding would forfeit a known-required step.

## Assumptions & Unknowns

### Assumptions (BINDING for the future Layer-2 execution PR)

The 22 assumptions below are BINDING. The Layer-2 executor must honour them verbatim; deviation requires a fresh planning round. Assumptions **A1–A18** mirror PR #246's structure (parent provenance + Q-binding + scope). Assumptions **A19–A22** are introduced or reshaped by Round 2 to incorporate BLOCKER-1 + NIT-N6.

1. **Parent provenance.** The 8 parent SHAs are pinned (PR #242 CSV/MD, PR #243 CSV/MD, PR #245 CSV/MD, PR #247 CSV/MD). The Layer-2 module must hard-code these as constants:
   - `parent_pr242_csv_sha256 = "f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b"`
   - `parent_pr242_md_sha256  = "fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d"`
   - `parent_pr243_csv_sha256 = "29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424"`
   - `parent_pr243_md_sha256  = "026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719"`
   - `parent_pr245_csv_sha256 = "703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0"`
   - `parent_pr245_md_sha256  = "7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419"`
   - `parent_pr247_csv_sha256 = "249e5591c6505b748fe3d371284a72d8f4620f57dbe9628c908ec2fbf097c8ed"`
   - `parent_pr247_md_sha256  = "4b49bee405bf87d4b8920b188e2c38d185ecc077b532d64a8bdd5a90cdf143f2"`

2. **Q5 BINDING.** `Q5_selected_policy = sensitivity_indicator_co_registration`, verdict `narrow_with_evidence`. Q6G honours Q5: cross-region history rows are NOT dropped; the `is_cross_region_fragmented` flag is a co-registered evidence dimension on each Q6G proof row's `cross_region_policy` field, not a filter. Falsifier `q6g_q5_re_adjudication_drift` halts the entrypoint if any Q6G row carries a Q5-verdict-bearing token in a verdict-bearing field.

3. **Q6F BINDING.** `Q6F_selected_policy = narrow_with_evidence`; `materialization_permission = recommendation_only_blocked_pending_implementation_proof_pr`. The Q6G proof does NOT re-adjudicate Q6F (does not change the inter-candidate ranking, does not retract `narrow_with_evidence`); it only emits a Q6G_selected_policy in its own right.

4. **Q1–Q4 / Q6 / Q7 / Q8 BINDING.** All ratified by PR #242 / PR #245 chain. Q6's `deferred_blocker_with_algorithm_survey_required` verdict was discharged by PR #247.

5. **Single candidate under proof = Glicko-2.** Pursuant to PR #247 §11's lowest log-loss (Glicko-2 = 0.625522 vs TrueSkill = 0.629127), Q6G proves Glicko-2's implementation specifically. TrueSkill is **not** re-implemented in Q6G. If the Q6G verdict is `defer_to_two_candidate_implementation_comparison`, a separate Q6H PR implements TrueSkill alongside.

6. **Strict-`<` filter inherited verbatim.** `STRICT_LT_HISTORY_FILTER = "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"` per PR #242 Q3 BIND_NOW. The Q6G engine must honour this filter for every prediction in event-by-event mode.

7. **Source layer.** PHA (`player_history_all`) is the rating-update signal source; PHA already restricts to decisive results per PR #242 Q1; same as Q6F.

8. **Target anchor for evaluation.** `matches_history_minimal.started_at TIMESTAMP` per PR #242 Q2 BIND_NOW; same as Q6F.

9. **Hyperparameter policy.** Glicko-2 defaults match Q6F verbatim: `mu=1500, RD=350, sigma=0.06, tau=0.5, rating_period_days=30` (Glickman 2012 reference; see A22). NO tuned variants in Q6G. Any tuning belongs in a future sensitivity PR (see OQ6).

10. **Player identity grouping key.** `toon_id` per PR #245; same as Q6F.

11. **Survey output rows.** EXACTLY 5 rows:
    - Row 1: `Q6G_A_glicko2_event_by_event_reference` (reference run; mirrors Q6F's Glicko-2 row metrics; serves as the equivalence-proof anchor).
    - Row 2: `Q6G_B_glicko2_batched_production_shape` (the production-shaped batched-update path; Glickman 2012 §3 rating-period batching).
    - Row 3: `Q6G_C_glicko2_event_vs_batched_equivalence_proof` (the BLOCKER-1 binding row; emits the ordering-equivalence statistics; see A19).
    - Row 4: `Q6G_D_glicko2_implementation_byte_determinism_proof` (byte-stability of the engine output across two independent runs with `BOOTSTRAP_RANDOM_SEED = 42`; emits the hash-equality outcome).
    - Row 5: `Q6G_selected_policy` (BINDING; emergent from rows 1–4).

12. **Materialization permission outcome matrix.**
    - if `Q6G_selected_policy.verdict == bind_now`:
      `materialization_permission = "permitted_for_all_6_families_with_pinned_glicko2_batched_production_implementation_and_hyperparameters_in_next_materialization_pr"`
      (PERMITTED ONLY IF A19's equivalence criterion passes; see §Gate Condition clause (b3).)
    - if `Q6G_selected_policy.verdict == recommendation_only_glicko2`:
      `materialization_permission = "recommendation_only_glicko2_event_by_event_validated_batched_path_unproven_or_unequivalent"`
    - if `Q6G_selected_policy.verdict == defer_to_two_candidate_implementation_comparison`:
      `materialization_permission = "blocked_pending_q6h_two_candidate_implementation_comparison_pr"`
    - if `Q6G_selected_policy.verdict == omit_reconstructed_rating_and_unblock_other_five`:
      `materialization_permission = "permitted_for_other_5_families_without_reconstructed_rating"`
    - if `Q6G_selected_policy.verdict == deferred_blocker`:
      `materialization_permission = "blocked_pending_<named_reason>"` (Q6G MUST name the exact missing evidence; "more data needed" is not acceptable).

13. **`materialized_output_paths` MUST be empty on every row.** No Q6G row may reference any Parquet path. Q6G is an adjudication-class artifact.

14. **No status YAML / research_log / ROADMAP mutation** (per PR #242 / #243 / #245 / #247 non-closure precedent). Closure of Step 02_01_03 is reserved for the Layer-3 materialization PR (or the named omit-and-unblock follow-up).

15. **Test target.** ≥150 tests; ≥95% branch coverage on the proof module (matches PR #247 Layer-2 floor).

16. **Read-only against DuckDB.** Q6G opens DuckDB in read-only mode; the only writes are the CSV+MD artifact pair plus `pytest tmp_path` fixtures. No DuckDB table is created, dropped, or altered.

17. **Evaluation traces are EPHEMERAL.** Per-game rating-history dictionaries live only in process memory; never persisted to `.parquet`/`.json`/`.npz`/`.pkl`. Falsifier `q6g_rating_trace_persistence_violation` checks the post-execution directory listing.

18. **No re-implementation of Q6F survey engines.** Q6G's `_run_glicko2_event_by_event` MUST import and re-use PR #247's exact Glicko-2 engine for Row 1; Row 2 implements the new batched path. This enforces that Row 1 is a true reference, not a re-author of the algorithm.

19. **BLOCKER-1 — event-by-event vs. batched-update ordering equivalence (BINDING).** Q6G MUST prove ordering equivalence between the event-by-event Glicko-2 path (Row 1) and the batched Glicko-2 path (Row 2) BEFORE the `bind_now` decision branch is reachable. The equivalence criterion is:
    - **Spearman ρ ≥ 0.99** between event-by-event and batched-Glicko-2 pre-match rating-state-induced predicted probabilities (computed at each PHA row's prediction point using each path's then-current rating state); the Spearman is computed on the full non-cold-start PHA stream and includes tied predictions resolved via tie-averaged ranks (same convention as PR #247 §10's AUC).
    - **|Δ log-loss| ≤ 1 standard error**, where the SE is the **deterministic percentile-bootstrap SE** derived from a 200-block bootstrap with `BOOTSTRAP_RANDOM_SEED = 42` (same seed and block count as PR #247 — direct comparability with Q6F). Δ log-loss is computed as `log_loss_batched_path − log_loss_event_path`; the test is `|Δ log_loss| ≤ SE_log_loss_event_path` where `SE_log_loss_event_path = (CI_high − CI_low) / (2 × 1.96)` from the 95% CI (deterministic bootstrap reproduces the SE that produced PR #247's [0.6216, 0.6302] interval).
    - **Named falsifier:** `q6g_batched_event_ordering_equivalence_unproven`. The helper emits the Spearman ρ value and |Δ log-loss| value into Row 3's `equivalence_proof_statistics` JSON column.
    - **Failure behavior:** if EITHER bound fails (Spearman ρ < 0.99 OR |Δ log-loss| > SE), Row 5's `Q6G_selected_policy.verdict` MUST be one of: `recommendation_only_glicko2`, `defer_to_two_candidate_implementation_comparison`, `omit_reconstructed_rating_and_unblock_other_five`, `deferred_blocker`. **`bind_now` is BARRED.**
    - **Authority statement (BINDING):** PR #247 §11 metrics transfer to a batched-Glicko-2 `bind_now` **ONLY IF** A19's equivalence criterion passes. Without equivalence, the Q6F numbers do not certify the production path. This authority statement must be quoted verbatim in MD §13.

20. **NIT-N1 — MD §10 sample emission is probability-only.** The Q6G MD §10 sample MUST be a row of **exactly 5 floats in [0, 1]** representing the first 5 PHA-row predicted-probability values (from Row 2's batched-path output, in deterministic stream order). NO raw `mu` value, NO raw `sigma`/`RD` value, NO rating-state struct, and NO `phi`/`tau` value may appear in the MD §10 sample table OR in any other section of the MD OR in any CSV cell. Named falsifier: `q6g_raw_mu_or_sigma_persisted_in_md`. The Layer-2 executor must run a grep-class check at validation time (`grep -E "mu=|sigma=|RD=|phi=|tau=" <md_path>` must return zero matches except inside MD §8 Algorithm Specification text where Glicko-2's symbols are defined as part of the algorithm description; that section's allowed scope is enforced by a one-section allow-list).

21. **NIT-N6 — bootstrap method policy (BINDING).** The bootstrap used to derive CIs and the equivalence-SE in A19 is the **deterministic percentile bootstrap** (NOT BCa). Constants:
    - `BOOTSTRAP_METHOD = "deterministic_percentile"`
    - `BOOTSTRAP_RANDOM_SEED = 42` (inherited from PR #247; direct comparability)
    - `BOOTSTRAP_BLOCK_COUNT = 200` (inherited from PR #247; direct comparability)
    - `NUMPY_RNG_BIT_GENERATOR = "PCG64"` (numpy default for `np.random.Generator`; pinned to remove platform variance)
    - `PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY = "sorted_then_kahan"` (sort PHA rows by `(toon_id, timestamp, replay_id)` then apply Kahan-Neumaier summation when accumulating per-block log-loss to reduce platform-specific round-off; pinned because Δ log-loss equivalence at the 1-SE bound is round-off-sensitive)
    These constants populate the 5 new schema columns introduced by NIT-N3 (see A22 / §File Manifest) and the `bootstrap_method_policy` field on every CSV row.

22. **NIT-N5 / OQ6 — `rating_period_days` is pinned at 30 (Glickman 2012 §10 default).** Q6G honours the Glickman 2012 worked-example default (30 days) verbatim. A `{7, 30, 90}` sensitivity arm is **OUT OF SCOPE** for Q6G and is deferred to a future Q6H or Layer-3-internal sensitivity step (see OQ6).

### Limitations (NIT-N4)

- **toon_id is region-scoped per Invariant #2 branch (iii).** Rating fragmentation across region-migrating players is an accepted Q6G bias. The Q6G proof does **not** refute this and does **not** claim worldwide-identity equivalence. A future worldwide-identity PR (out of scope here) would address it separately. This limitation must be re-stated verbatim in MD §15 "Limitations" subsection.
- **Cold-start gate (G-CS-4).** Q6G inherits PR #247's cold-start mask; the first PHA row for any toon_id contributes nothing to metric computation but is counted in `cold_start_rate`. Cold-start rows do NOT participate in the A19 equivalence proof.
- **PHA decisive-only.** Per PR #242 Q1, PHA carries decisive results only; Glicko-2's draw-margin parameter is inapplicable (mirrors Q6F).

### Unknowns (DEFERRED with explicit gating)

- **U1 — Final Q6G selected_policy.** Per NIT-N2: the **default expected outcome is `recommendation_only_glicko2`** UNLESS A19's equivalence criterion passes AND the implementation proof is otherwise clean. The Q6F §11 CI overlap (Glicko-2 [0.6216, 0.6302] vs TrueSkill [0.6246, 0.6342], overlap = 0.0056 ≈ 0.9% of mid) does not robustly favor `bind_now` on its own; A19's outcome decides whether `bind_now` is even reachable.
- **U2 — Exact Spearman ρ and |Δ log-loss| values.** Computed at execution time from the actual PHA stream.
- **U3 — Whether the batched-path metrics in Row 2 reproduce Row 1's metrics within bootstrap CI.** Expected yes by construction (Glicko-2's batched update is the canonical specification; event-by-event is the practical specialisation), but the proof is empirical.
- **U4 — Whether MD §8's allowed Glicko-2 symbol scope (mu, sigma, RD, phi, tau in the algorithm-specification text) is sufficient to author the section without leaking into §10's sample table.** Resolved by the NIT-N1 grep-check at T07 validation.

## Literature context

### Internal (BINDING; read before authoring Layer-2 module)

- `reports/specs/02_02_feature_engineering_plan.md` §6.2 row 4 line 241 (Glicko-2 spec-favoured framing); §9 G-CS-4 line 422 (cold-start); §10 G-L-4 line 455 (no post-game rating-after read). Identical to PR #246 internal-citation scope.
- PR #247 (Q6F) §11 verbatim per-candidate metric table (the four-CI block already constants-pinned in this plan's header) and §12 decision rule (CI-based binding; AUC alone cannot bind).
- PR #247 Q6F module's `STRICT_LT_HISTORY_FILTER`, `CITATION_GLICKMAN_2012`, and the existing `_run_glicko2_survey` function — Q6G's Row 1 reference path imports these verbatim per A18.
- PR #245 Q6_selected_policy row's notes (the framing under which the entire algorithm-survey-then-implementation-proof chain runs).

### External (CITATION-ONLY; the Layer-2 module pins these as constants)

- **Glickman (2012)** — "Example of the Glicko-2 system" (Boston University technical note). Authoritative source for §3 rating-period batching, §10 worked example with `rating_period_days = 30`, and the `mu/RD/sigma/tau` reference defaults. Pinned constant `CITATION_GLICKMAN_2012` (imported verbatim from PR #247's module).
- **Glickman (1999)** — "Parameter estimation in large dynamic paired comparison experiments." *Applied Statistics*, 48: 377–394. Source for the original Glicko reliability-deviation formulation. Pinned constant `CITATION_GLICKMAN_1999` (imported from PR #247).
- **Efron & Tibshirani (1993)** — *An Introduction to the Bootstrap*. Chapman & Hall. Source for percentile bootstrap (NIT-N6); cited for the methodological choice "deterministic percentile bootstrap" over BCa for paired classifier comparison. Pinned constant `CITATION_EFRON_TIBSHIRANI_1993`. **[OPINION]** flag: BCa is sometimes preferred for skewed bootstrap distributions, but the percentile bootstrap is sufficient for the |Δ log-loss| ≤ SE check at the granularity Q6G needs; A19 does not need higher-order accuracy.
- **Knuth (1981) / Higham (2002)** — *The Art of Computer Programming* Vol. 2 / *Accuracy and Stability of Numerical Algorithms* (2nd ed.). Source for Kahan / Neumaier summation (NIT-N6 `PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY`). Pinned constant `CITATION_KAHAN_SUMMATION_HIGHAM_2002`.

### When WebFetch is permitted

- For Glicko-2 §3 batched-update step-by-step equations (the Layer-2 executor may WebFetch the Glickman 2012 PDF for verifying the rating-period update formula against the implementation).
- NOT for the citation strings themselves (already pinned).
- NOT for "best rating_period_days for SC2" or any tuning query (per A9 + A22; sensitivity is out of scope).

## Execution Steps

The future Layer-2 execution PR runs T01–T09 in order. Each task lists files, function signatures (where load-bearing), validation report, stop condition, and Sonnet/Opus routing.

The non-batching rule (`data-analysis-lineage.md` §"Non-batching rule for empirical work") REQUIRES that the Layer-2 PR respect a per-step sequence (scaffold → validation module → executor checkpoint → artifacts → status update). T01–T08 do not generate any artifact except validation reports; the artifact pair is generated only at T06, after T03 (event reference + batched production engine), T04 (metrics), and T05 (equivalence proof + decision binding) are all checkpoint-committed.

### T01 — Proof module shell (constants + dataclasses + 39-column schema)

**Objective:** Stand up the Q6G proof module with constants, dataclasses, and the 39-column schema. No engine logic, no I/O.

**Instructions:**
1. Create `src/rts_predict/games/sc2/datasets/sc2egset/proof_glicko2_implementation.py` mirroring PR #247's module structure.
2. Define `Q6G_PROOF_ROWS: tuple[str, ...]` with the 5 canonical row labels per A11.
3. Define `Q6G_HYPERPARAMETER_DEFAULTS: dict[str, float]` (Glickman 2012 defaults; A9 + A22).
4. Import `STRICT_LT_HISTORY_FILTER`, `CITATION_GLICKMAN_2012`, `CITATION_GLICKMAN_1999`, and the existing `_run_glicko2_survey` function from PR #247's module verbatim (A18).
5. Define `CITATION_EFRON_TIBSHIRANI_1993` and `CITATION_KAHAN_SUMMATION_HIGHAM_2002` as new module constants.
6. Define `BOOTSTRAP_METHOD = "deterministic_percentile"`, `BOOTSTRAP_RANDOM_SEED = 42`, `BOOTSTRAP_BLOCK_COUNT = 200`, `NUMPY_RNG_BIT_GENERATOR = "PCG64"`, `PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY = "sorted_then_kahan"` (NIT-N6; A21).
7. Define `RATING_PERIOD_DAYS = 30`, `GLICKO2_ITERATION_TOL = 1e-6` (Glickman 2012 §3 stopping criterion default; NIT-N3 / A22).
8. Define `Q6G_PROOF_SCHEMA: tuple[str, ...]` with **EXACTLY 39 column names** per NIT-N3. The schema is:
   - **Shared / lineage (12 cols):** `decision_id`, `parent_decision_id`, `proof_row_label`, `included_in_proof`, `inclusion_or_rejection_reason`, `parent_pr242_csv_sha256`, `parent_pr242_md_sha256`, `parent_pr243_csv_sha256`, `parent_pr243_md_sha256`, `parent_pr245_csv_sha256`, `parent_pr245_md_sha256`, `parent_pr247_csv_sha256` + `parent_pr247_md_sha256` (count = 13 — re-check; correction below).
   - **Re-counted exact column list (39 total):**
     1. `decision_id`
     2. `parent_decision_id`
     3. `proof_row_label`
     4. `included_in_proof`
     5. `inclusion_or_rejection_reason`
     6. `glicko2_path_kind` ∈ {`event_by_event_reference`, `batched_production_shape`, `equivalence_proof`, `byte_determinism_proof`, `verdict_row`}
     7. `initialization_policy`
     8. `hyperparameter_policy`
     9. `cold_start_policy`
     10. `tie_policy`
     11. `player_identity_policy`
     12. `cross_region_policy`
     13. `forward_only_constraints`
     14. `log_loss`
     15. `log_loss_ci_low`
     16. `log_loss_ci_high`
     17. `brier`
     18. `brier_ci_low`
     19. `brier_ci_high`
     20. `calibration_error`
     21. `coverage_rate`
     22. `cold_start_rate`
     23. `runtime_summary`
     24. `equivalence_proof_statistics` (JSON: `{"spearman_rho": ..., "abs_delta_log_loss": ..., "se_log_loss_event": ..., "passes_spearman_bound": bool, "passes_delta_log_loss_bound": bool}` — populated only on Row 3; sentinel `"not_applicable"` on other rows)
     25. `byte_determinism_proof_statistics` (JSON: `{"run_a_sha256": ..., "run_b_sha256": ..., "hashes_equal": bool}` — populated only on Row 4; sentinel `"not_applicable"` on other rows)
     26. `selected_policy` (populated only on Row 5; sentinel on others)
     27. `proof_verdict` (populated only on Row 5; sentinel on others)
     28. `materialization_permission` (populated only on Row 5; sentinel on others)
     29. `raw_mmr_hybrid_rejection` (re-affirmed; verbatim from PR #245 N-2)
     30. `evidence_paths`
     31. `falsifiers`
     32. `audit_pr`
     33. `materialized_output_paths` (empty on every row; A13)
     34. `notes`
     35. `bootstrap_random_seed` (**NIT-N3**; pinned `42`; A21)
     36. `rating_period_days` (**NIT-N3**; pinned `30`; A22)
     37. `glicko2_iteration_tol` (**NIT-N3**; pinned `1e-6`)
     38. `numpy_rng_bit_generator` (**NIT-N3**; pinned `"PCG64"`; A21)
     39. `python_floating_point_summation_order_policy` (**NIT-N3**; pinned `"sorted_then_kahan"`; A21)
9. Define `Q6G_PARENT_SHAS: dict[str, str]` mapping the 8 parent SHA names to their pinned values (A1).
10. Define dataclass `RatingImplementationProofDecision` with **exactly 39 fields** matching `Q6G_PROOF_SCHEMA`.
11. Define dataclass `RatingImplementationProofResult` (top-level container; mirrors PR #247's `RatingAlgorithmSurveyResult`).
12. Define `FALSIFIER_PRIORITY_CHAIN: tuple[str, ...]` with ≥38 keys covering: 8 parent-SHA-mismatches; candidate-completeness (exactly 5 rows); byte-determinism; `q6g_batched_event_ordering_equivalence_unproven` (A19); `q6g_raw_mu_or_sigma_persisted_in_md` (A20); `q6g_materialization_creep`; `q6g_q5_re_adjudication_drift`; `q6g_q6f_re_adjudication_drift`; `q6g_status_drift`; `q6g_research_log_drift`; `q6g_roadmap_drift`; `q6g_no_post_game_token`; `q6g_no_target_match_outcome_read`; `q6g_no_future_match_read`; `q6g_no_global_batch_fit`; `q6g_no_phase_03_baseline_creep`; `q6g_no_trueskill_re_implementation` (A5); `q6g_rating_trace_persistence_violation` (A17); `q6g_rating_period_days_not_30` (A22); `q6g_bootstrap_seed_not_42` (A21); `q6g_bootstrap_block_count_not_200` (A21); `q6g_bootstrap_method_not_deterministic_percentile` (A21); `q6g_numpy_rng_not_pcg64` (A21); `q6g_python_summation_policy_not_sorted_then_kahan` (A21); `q6g_decision_count_mismatch` (must == 5); `q6g_decision_id_order_mismatch`; `q6g_q6g_selected_policy_row_missing`; `q6g_bind_now_emitted_without_equivalence_pass` (A19 BLOCKER-1 guard; raises if Row 5's verdict == `bind_now` AND Row 3's `passes_spearman_bound` is False OR `passes_delta_log_loss_bound` is False).
13. Module-load assert blocks: `assert len(Q6G_PROOF_SCHEMA) == 39`; `assert len(fields(RatingImplementationProofDecision)) == 39`; `assert len(Q6G_PROOF_ROWS) == 5`.

**Verification:**
- `source .venv/bin/activate && poetry run python -c "import rts_predict.games.sc2.datasets.sc2egset.proof_glicko2_implementation"` returns 0
- Module-load asserts pass (39 / 39 / 5).
- `grep -c '^    [a-z_].*:.* = field' src/rts_predict/games/sc2/datasets/sc2egset/proof_glicko2_implementation.py` ≥ 39 (dataclass field count proxy).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/proof_glicko2_implementation.py`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/survey_history_rating_algorithms.py` (PR #247; import-only)

**Routing:** Sonnet sufficient (mechanical scaffolding; schema fully specified above).

---

### T02 — Read-only PHA chronological loader + Q6F reference invocation

**Objective:** Re-load the PHA stream identically to PR #247, then invoke PR #247's event-by-event Glicko-2 engine to populate Row 1's reference metrics WITHOUT re-implementing the algorithm (A18).

**Instructions:**
1. Define `_load_pha_history_chronological(db_path: Path) -> pd.DataFrame` (read-only; same query as PR #247 §T02).
2. Define `_run_glicko2_event_by_event_reference(stream: pd.DataFrame) -> dict[str, Any]` that **calls** PR #247's `_run_glicko2_survey(stream)` and returns its output unchanged. NO re-implementation; this is a delegation wrapper.
3. Validate that the returned `(log_loss, brier, calibration_error)` match PR #247's §11 row to ≥ 4 decimal places (`0.6255`, `0.2177`, `0.0349`) within `1e-4` tolerance. Print mismatch and HALT if not.

**Verification:**
- Validation report shows Row 1 log-loss in `[0.6254, 0.6256]`, Brier in `[0.2176, 0.2178]` (matches PR #247 §11 within tolerance).
- Per-toon chronological monotonicity holds (same assertion as PR #247 §T02).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/proof_glicko2_implementation.py` (extends T01)

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/survey_history_rating_algorithms.py`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb` (read-only)

**Routing:** Sonnet sufficient (delegation + numerical sanity).

---

### T03 — Glicko-2 batched-update production-shape engine (Row 2)

**Objective:** Implement Glicko-2 in the production-shaped batched-update path (Glickman 2012 §3) — distinct from PR #247's event-by-event path. This is the only new algorithm code in Q6G.

**Instructions:**
1. Define `_run_glicko2_batched_production(stream: pd.DataFrame, mu: float = 1500, rd: float = 350, sigma: float = 0.06, tau: float = 0.5, rating_period_days: int = 30, iteration_tol: float = 1e-6) -> dict[str, Any]`.
2. The function partitions the PHA stream into rating-period blocks of `rating_period_days = 30` (A22; default Glickman 2012 §10 example), with period boundaries anchored at the earliest PHA timestamp.
3. Within a period, all matches involving a given `toon_id` are BATCHED and the player's `(mu, RD, sigma)` is updated once at the period boundary using Glickman 2012 §3 equations 4–9 (the canonical batched form), with convergence tolerance `iteration_tol = 1e-6`.
4. BETWEEN periods, the state advances forward; the period boundary MUST NOT cross the target match's `started_at` (enforced via the strict-`<` filter from A6).
5. The per-row prediction is computed using the rating state from the most recent CLOSED period strictly prior to the row's timestamp; this is the "production-shape" because it matches how a serving system would carry rating state from period to period.
6. Cold-start handling: identical to PR #247 (first-match-per-toon flagged `is_cold_start=True`, predicted probability = prior-implied 0.5).
7. Per-row summation when computing log-loss MUST use `PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY = "sorted_then_kahan"` (A21): sort PHA rows by `(toon_id, timestamp, replay_id)` then accumulate per-block log-loss via Kahan-Neumaier summation.
8. Return dict shape identical to PR #247's `_run_glicko2_survey`: `{"predicted_probabilities", "actuals", "is_cold_start", "rating_state_at_end", "runtime_ms"}`. The `rating_state_at_end` lives only in process memory (A17).

**Verification:**
- For a 2-player, 4-row synthetic fixture spanning 2 rating periods, manual hand-computed `(mu, RD)` after period 1 matches the engine output to `1e-4`.
- Per-toon chronological monotonicity of period assignment holds (no row assigned to a period earlier than a prior row's period for the same toon).
- Forward-only invariant: assert no row's predicted probability reads the row's own `result` (verified by deliberate-leak fixture).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/proof_glicko2_implementation.py` (extends T01–T02)

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/survey_history_rating_algorithms.py` (engine-shape reference only; NOT re-imported for the batched algorithm itself)

**Routing:** **Opus REQUIRED.** Subtle reasoning: (a) period boundary semantics and the strict-`<` filter interaction; (b) Kahan-Neumaier summation order is sensitive to per-block iteration order; (c) Glicko-2 §3 batched-update formula must match the source mathematically, not by copy-paste from a third-party package.

---

### T04 — Metric computation + deterministic percentile bootstrap CI

**Objective:** Compute the per-path metric block (log-loss / Brier / calibration-error / AUC) WITH deterministic percentile-bootstrap CIs for Rows 1 and 2, plus the Δ log-loss SE used by A19's equivalence criterion.

**Instructions:**
1. Define `_compute_proof_metrics(engine_output: dict[str, Any]) -> dict[str, float]` (mirrors PR #247 §T04 — log_loss, brier, calibration_error, coverage_rate, cold_start_rate, runtime_summary on non-cold-start subset).
2. Define `_compute_deterministic_percentile_ci(actuals: np.ndarray, probabilities: np.ndarray, metric_fn: Callable, *, seed: int = 42, block_count: int = 200, ci_level: float = 0.95, rng_bit_generator: str = "PCG64") -> tuple[float, float]`:
   - Construct `np.random.Generator(np.random.PCG64(seed))` (A21 `NUMPY_RNG_BIT_GENERATOR`).
   - Block-bootstrap by `toon_id` (block = all rows for one toon; preserves per-player chronology); 200 blocks resampled with replacement; recompute the metric on each resample.
   - Return the 2.5th and 97.5th percentile (percentile bootstrap; A21 `BOOTSTRAP_METHOD = "deterministic_percentile"`).
   - Determinism: identical seed + identical block count + identical input arrays MUST yield bit-identical CI tuples across two runs (verified at T08 by `TestDeterministicBootstrap`).
3. Use this function to populate Rows 1 and 2's `log_loss_ci_low/high`, `brier_ci_low/high` columns. AUC CI is **not** populated in Q6G (NIT-N3 dropped AUC from the schema; AUC alone cannot bind per Q6F §12; AUC is not part of the A19 equivalence criterion).
4. Define `_compute_event_log_loss_se(actuals: np.ndarray, probabilities: np.ndarray) -> float` returning `SE_log_loss_event = (log_loss_ci_high − log_loss_ci_low) / (2 × 1.96)`. This is the right-hand side of A19's |Δ log-loss| bound.

**Verification:**
- Bootstrap determinism: run `_compute_deterministic_percentile_ci` twice on the same fixture, assert tuple equality.
- For a golden-numbers fixture (probabilities `[0.6, 0.4, 0.5, 0.7]`, actuals `[1, 0, 1, 1]`), assert the log-loss point estimate matches hand-computed value to `1e-12`.
- For PR #247 Row "Glicko-2", the reproduced log-loss CI is `[0.621595, 0.630180]` within `1e-4` (re-derivation check).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/proof_glicko2_implementation.py` (extends T01–T03)

**Read scope:**
- (no new sibling reads)

**Routing:** Sonnet sufficient (numerical determinism + sklearn metrics; A21 constants pin every reproducibility lever).

---

### T05 — Equivalence proof + byte-determinism proof + Q6G_selected_policy decision

**Objective:** Produce Rows 3, 4, 5. Row 3 emits the A19 BLOCKER-1 binding equivalence statistics; Row 4 emits the byte-determinism proof; Row 5 emits `Q6G_selected_policy` under the decision rule below.

**Instructions:**
1. Define `_compute_event_vs_batched_equivalence_proof(event_output: dict, batched_output: dict) -> dict[str, Any]`:
   - Mask both paths to `~is_cold_start` (same mask each).
   - Compute `spearman_rho = scipy.stats.spearmanr(event_probabilities, batched_probabilities).statistic` (tie-averaged ranks).
   - Compute `abs_delta_log_loss = abs(log_loss(actuals, batched_probabilities) − log_loss(actuals, event_probabilities))`.
   - Compute `se_log_loss_event = _compute_event_log_loss_se(actuals, event_probabilities)` from T04.
   - Compute `passes_spearman_bound = (spearman_rho >= 0.99)`.
   - Compute `passes_delta_log_loss_bound = (abs_delta_log_loss <= se_log_loss_event)`.
   - Return `{"spearman_rho", "abs_delta_log_loss", "se_log_loss_event", "passes_spearman_bound", "passes_delta_log_loss_bound"}`.
2. Define `_compute_byte_determinism_proof(stream: pd.DataFrame) -> dict[str, Any]`:
   - Run `_run_glicko2_batched_production(stream)` twice with identical args.
   - SHA-256 the concatenated `predicted_probabilities` bytes (after `np.ascontiguousarray(... ).tobytes()`) for each run.
   - Return `{"run_a_sha256", "run_b_sha256", "hashes_equal": run_a_sha256 == run_b_sha256}`.
3. Define `_build_proof_decisions(...) -> tuple[RatingImplementationProofDecision, ...]` returning 5 decisions per A11. Populate:
   - **Row 1 (event reference):** metrics from T02 + T04; `glicko2_path_kind = "event_by_event_reference"`.
   - **Row 2 (batched production):** metrics from T03 + T04; `glicko2_path_kind = "batched_production_shape"`.
   - **Row 3 (equivalence proof):** `equivalence_proof_statistics` JSON from step 1; numeric metric cells = `"not_applicable"` sentinel; `glicko2_path_kind = "equivalence_proof"`.
   - **Row 4 (byte-determinism proof):** `byte_determinism_proof_statistics` JSON from step 2; numeric metric cells = `"not_applicable"` sentinel; `glicko2_path_kind = "byte_determinism_proof"`.
   - **Row 5 (verdict):** `glicko2_path_kind = "verdict_row"`; numeric metric cells = `"not_applicable"`; `selected_policy` / `proof_verdict` / `materialization_permission` derived per the decision rule below.
4. **Q6G decision rule (BINDING; inlined verbatim in module as constant `Q6G_PROOF_DECISION_RULE: str`):**

   ```text
   Let R3 = Row 3's equivalence_proof_statistics.
   Let R4 = Row 4's byte_determinism_proof_statistics.

   Equivalence pass = R3.passes_spearman_bound AND R3.passes_delta_log_loss_bound
                       (BLOCKER-1; A19; spearman ρ ≥ 0.99 AND |Δ log-loss| ≤ SE_event).
   Determinism pass = R4.hashes_equal.

   IF NOT Determinism pass:
       selected_policy = "deferred_blocker"
       verdict = "deferred_blocker"
       materialization_permission = "blocked_pending_byte_determinism_failure_investigation"
       rationale = "Glicko-2 batched-production engine is not byte-deterministic on two
                   identical runs; this disqualifies any materialization decision."

   ELIF NOT Equivalence pass:
       # NIT-N2 default expected outcome.
       selected_policy = "recommendation_only_glicko2"
       verdict = "recommendation_only_glicko2"
       materialization_permission = "recommendation_only_glicko2_event_by_event_validated_batched_path_unproven_or_unequivalent"
       rationale = f"Event-by-event Glicko-2 implementation validated against PR #247 §11;
                    batched-production path Spearman ρ = {R3.spearman_rho:.4f} or
                    |Δ log-loss| = {R3.abs_delta_log_loss:.6f} (SE = {R3.se_log_loss_event:.6f})
                    failed A19's equivalence criterion. Q6F's CI overlap (0.9% of mid-range)
                    is not strong enough to bind a batched path that is not provably equivalent
                    to the event path on this corpus."

   ELIF Equivalence pass AND Determinism pass:
       # NIT-N2: bind_now becomes reachable, but the planner remains
       # epistemically conservative -- Row 5 may emit bind_now only if
       # BOTH proofs pass cleanly.
       selected_policy = "bind_now"
       verdict = "bind_now"
       materialization_permission = "permitted_for_all_6_families_with_pinned_glicko2_batched_production_implementation_and_hyperparameters_in_next_materialization_pr"
       rationale = f"Glicko-2 batched-production implementation is byte-deterministic AND
                    ordering-equivalent to the event-by-event reference (Spearman ρ = {R3.spearman_rho:.4f}
                    ≥ 0.99; |Δ log-loss| = {R3.abs_delta_log_loss:.6f} ≤ SE = {R3.se_log_loss_event:.6f}).
                    Q6F §11 metrics now transfer to the production path."

   No other verdict branch is reachable from Row 5 in Q6G's scope; defer_to_two_candidate_implementation_comparison
   and omit_reconstructed_rating_and_unblock_other_five are NOT auto-emitted by this rule. The Layer-2 executor
   may override the auto-derived verdict ONLY by writing substantive reasoning in the PR description AND
   obtaining reviewer-adversarial sign-off; the override decision is OUT OF SCOPE for this planner.
   ```

5. Apply the BLOCKER-1 guard falsifier `q6g_bind_now_emitted_without_equivalence_pass`: assert that if Row 5's verdict == `bind_now`, then Row 3's `passes_spearman_bound` AND `passes_delta_log_loss_bound` must both be True. The falsifier helper raises `RatingImplementationProofError` with `falsifier_key = "q6g_bind_now_emitted_without_equivalence_pass"` if this invariant is violated.

**Verification:**
- 5 decisions emitted; canonical order matches A11.
- Row 5's verdict ∈ {`bind_now`, `recommendation_only_glicko2`, `deferred_blocker`} (the three Q6G-auto-reachable verdicts; executor-override into `defer_to_two_candidate_implementation_comparison` / `omit_reconstructed_rating_and_unblock_other_five` is recorded in PR description, not in this rule).
- Falsifier `q6g_bind_now_emitted_without_equivalence_pass` does NOT fire on the auto-derived verdict (validated by feeding a synthetic Row 3 with `passes_spearman_bound = False` and asserting auto-rule never emits `bind_now`).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/proof_glicko2_implementation.py` (extends T01–T04)

**Read scope:**
- (no new sibling reads)

**Routing:** **Opus REQUIRED.** Substantive reasoning: (a) the equivalence-proof statistics are the BLOCKER-1 binding evidence and require careful numeric reasoning about Spearman + paired |Δ| SE bounds; (b) any executor override of the auto-derived verdict requires Opus-level methodological writing; (c) the falsifier `q6g_bind_now_emitted_without_equivalence_pass` is the BLOCKER-1 enforcement mechanism and must be implemented as a hard assert, not a logged warning.

---

### T06 — Proof CSV + MD writer (probability-only §10 sample per NIT-N1)

**Objective:** Write byte-deterministic 39-column CSV + ≥19-section MD. MD §10 sample is **probability-only**, exactly 5 floats in [0, 1] (NIT-N1).

**Instructions:**
1. Define `write_q6g_proof_artifacts(result: RatingImplementationProofResult, csv_path: Path, md_path: Path) -> None`.
2. CSV writer: byte-deterministic (sort decisions by `decision_id`; `lineterminator="\n"`; `quoting=csv.QUOTE_MINIMAL`; explicit dialect mirroring PR #247).
3. MD writer: ≥19 sections; mirror PR #247's 18-section structure plus the new sections (§13a "Equivalence Proof Result (BLOCKER-1 / A19)", §13b "Byte-Determinism Proof Result", §15 "Limitations" per NIT-N4). The MD section list is enumerated under §File Manifest.
4. **MD §10 sample table (NIT-N1; A20):** A single markdown row with header `| pha_row_index | predicted_probability |` and exactly 5 data rows (PHA row indices 0–4 in stream-deterministic order, predicted probability values from Row 2's `batched_production` path, each formatted as `f"{p:.6f}"`). NO mu, NO sigma, NO RD, NO phi, NO tau anywhere in §10. NO rating-state dictionary anywhere in §10.
5. **NIT-N1 grep-check at writer time:** Before writing the MD, run a regex check over the prepared MD content: `re.search(r"\b(mu|sigma|RD|phi|tau)\s*=", md_content[md_section_10_offset:md_section_11_offset])` must return None. If it finds a match, raise `RatingImplementationProofError(falsifier_key="q6g_raw_mu_or_sigma_persisted_in_md")`. Glicko-2 symbol references are ALLOWED only within §8 (Algorithm Specification), enforced by writing §8 content from a separate template and asserting the symbol-allowed-scope.

**Verification:**
- Byte-stability: run writer twice, assert two outputs hash-identical.
- CSV column count == 39; CSV row count == 6 (1 header + 5 decisions).
- MD section count ≥ 19 (`grep -c "^## " <md_path>` ≥ 19).
- NIT-N1 grep-check: `grep -nE "\b(mu|sigma|RD|phi|tau)\s*=" <md_path>` returns matches only on lines inside the §8 algorithm-spec block (verified by line-range filter).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/proof_glicko2_implementation.py` (extends T01–T05)

**Read scope:**
- (no new sibling reads)

**Routing:** Sonnet sufficient (deterministic CSV + grep-verified MD writer; rules are mechanical).

---

### T07 — Sandbox jupytext notebook pair

**Objective:** Author the jupytext-paired sandbox notebook that exercises the Q6G public entrypoint and prints outputs for visual inspection.

**Instructions:**
1. Create `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.py` (jupytext-paired source) and `.../02_01_03_q6g_rating_implementation_proof.ipynb`.
2. Sandbox notebook contract (per `sandbox/README.md`): no `def`/`class`/`lambda` in cells; all logic imported from the proof module; outputs cleared before commit.
3. Cells exercise: (a) module import + constants; (b) PHA load + Row 1 reference invocation; (c) Row 2 batched run; (d) Row 3 equivalence-proof printout (Spearman ρ, |Δ log-loss|, SE); (e) Row 4 byte-determinism hash printout; (f) Row 5 verdict printout.
4. Per `feedback_notebook_print_vs_logger`: `print()` for data exploration of metric arrays; `logger` only for one-line diagnostics.

**Verification:**
- `source .venv/bin/activate && poetry run jupytext --execute sandbox/.../02_01_03_q6g_rating_implementation_proof.py` exits 0.
- Final cell prints Row 5's verdict.

**File scope:**
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.py`
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.ipynb`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/proof_glicko2_implementation.py`

**Routing:** Sonnet sufficient.

---

### T08 — Mirrored test file (≥150 tests; ≥95% branch coverage)

**Objective:** Implement the mirrored test suite covering every constant, every engine, every metric, the bootstrap determinism, the equivalence proof, the byte-determinism proof, the decision rule, and every falsifier — including the new BLOCKER-1 guard.

**Instructions:**
1. Create `tests/rts_predict/games/sc2/datasets/sc2egset/test_proof_glicko2_implementation.py`.
2. Test classes:
   - `TestModuleConstants` — `Q6G_PROOF_ROWS`, `Q6G_PROOF_SCHEMA` length **== 39** (NIT-N3), `Q6G_HYPERPARAMETER_DEFAULTS`, citation constants, `BOOTSTRAP_RANDOM_SEED == 42`, `BOOTSTRAP_BLOCK_COUNT == 200`, `BOOTSTRAP_METHOD == "deterministic_percentile"`, `NUMPY_RNG_BIT_GENERATOR == "PCG64"`, `PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY == "sorted_then_kahan"`, `RATING_PERIOD_DAYS == 30`, `GLICKO2_ITERATION_TOL == 1e-6`.
   - `TestParentSHAs` — verify the 8 pinned parent SHAs against the canonical strings (A1); mismatch case triggers `RatingImplementationProofError` with the correct falsifier key.
   - `TestEventByEventReferenceMatchesQ6F` — assert Row 1's log-loss / Brier / calibration_error match PR #247 §11 to `1e-4`.
   - `TestGlicko2BatchedProductionEngine` — synthetic 2-player, 4-row, 2-period fixture; hand-computed `(mu, RD)` after period 1; forward-only invariant via deliberate-leak fixture.
   - `TestDeterministicBootstrap` — call `_compute_deterministic_percentile_ci` twice with `seed=42`, `block_count=200`; assert bit-identical tuple; assert PCG64 generator.
   - `TestKahanSummationOrder` — assert that `PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY = "sorted_then_kahan"` produces a per-block log-loss that differs from naive-sum by ≥ `1e-12` on a fixture designed to expose round-off.
   - `TestEquivalenceProof_PassesBound` — synthetic stream where event and batched paths produce identical predictions; assert Spearman ρ == 1.0; assert |Δ log-loss| == 0.0; assert both bounds pass.
   - `TestEquivalenceProof_FailsBound` — synthetic stream where batched and event paths diverge; assert Spearman ρ < 0.99 OR |Δ log-loss| > SE; assert falsifier helper would BAR `bind_now`.
   - `TestByteDeterminismProof` — assert two runs hash-identical; assert hash differs after deliberate jitter (e.g., shuffled stream).
   - `TestDecisionRule_AllThreeBranches` — synthesise (a) Determinism fail → `deferred_blocker`; (b) Equivalence fail → `recommendation_only_glicko2`; (c) both pass → `bind_now`.
   - `TestBlockerGuard_BindNowRequiresEquivalence` — manually construct a `RatingImplementationProofResult` where Row 5 says `bind_now` but Row 3's `passes_spearman_bound` is False; assert `RatingImplementationProofError(falsifier_key="q6g_bind_now_emitted_without_equivalence_pass")` is raised on artifact write.
   - `TestArtifactWriter` — byte-stability via dual-write; CSV column count **== 39**; MD section count ≥ 19; NIT-N1 grep-check on emitted MD §10 returns zero raw symbol matches.
   - `TestNIT_N1_MDSampleIsProbabilityOnly` — parse §10 of the emitted MD; assert exactly 5 data rows; assert each value is a float in [0, 1]; assert no occurrence of `"mu"`, `"sigma"`, `"RD"`, `"phi"`, `"tau"` in §10 substring.
   - `TestFalsifierChain` — for each key in `FALSIFIER_PRIORITY_CHAIN` (≥ 38 keys), construct a failing fixture and assert matching helper raises with the correct `falsifier_key`.
   - `TestNoMaterializationCreep` — `materialized_output_paths` empty on every row; no `.parquet` written under `tmp_path` after a full proof run.
   - `TestNoTrueSkillReImplementation` — assert no symbol from PR #247's TrueSkill engine is referenced by Q6G module (A5; grep over the source).
   - `TestRatingTracePersistenceViolation` — assert no `.parquet` / `.json` / `.npz` / `.pkl` written by the proof run.
3. ≥150 tests; ≥95% branch coverage.

**Verification:**
- `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_proof_glicko2_implementation.py -v --cov=rts_predict.games.sc2.datasets.sc2egset.proof_glicko2_implementation --cov-branch --cov-report=term-missing`
- ≥150 tests pass; ≥95% branch coverage.

**File scope:**
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_proof_glicko2_implementation.py`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/proof_glicko2_implementation.py`

**Routing:** Sonnet sufficient (mechanical given T01–T06 are settled).

---

### T09 — Release tail

**Objective:** Bump version, append CHANGELOG, archive PR #247 in `planning/INDEX.md`, register the active Q6G PR.

**Instructions:**
1. `pyproject.toml`: version `3.76.0 → 3.77.0`.
2. `CHANGELOG.md`: new `## [3.77.0] - YYYY-MM-DD (PR #N: feat/sc2egset-02-01-03-q6g-rating-implementation-proof)` block enumerating every added file; verdict outcome string; Layer-2 reviewer-adversarial verdict reference.
3. `planning/INDEX.md`: archive PR #247 into Archive table; new Active entry pointing to the Q6G PR.

**Verification:**
- Pre-commit hooks pass (ruff, mypy, plan-section-check).
- `git status` shows only the expected files modified.

**File scope:**
- `pyproject.toml`
- `CHANGELOG.md`
- `planning/INDEX.md`

**Read scope:**
- (none — pure metadata updates)

**Routing:** Sonnet sufficient.

---

### Adversarial gate

The Layer-2 PR's final gate is `@reviewer-adversarial` (NOT `@reviewer-deep`) because the Q6G proof emits methodology-bearing quantitative findings (equivalence statistics + determinism hash) that will inform thesis chapters AND because Row 5's verdict is a binding adjudication. The 3-round adversarial cap resets for Layer-2 (symmetric application per `feedback_adversarial_cap_execution.md`).

## File Manifest

### Planning files (created in THIS Layer-1 planning-only PR — 2 files)

| File | Action |
|---|---|
| `planning/current_plan.md` | Create |
| `planning/current_plan.critique.md` | Create (reviewer-adversarial Round 2 stub) |

### Future Layer-2 execution files (created in the FUTURE Q6G implementation-proof PR — 9 files; NOT this PR)

| # | File | Action |
|---|---|---|
| 1 | `src/rts_predict/games/sc2/datasets/sc2egset/proof_glicko2_implementation.py` | Create |
| 2 | `tests/rts_predict/games/sc2/datasets/sc2egset/test_proof_glicko2_implementation.py` | Create |
| 3 | `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.py` | Create |
| 4 | `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.ipynb` | Create |
| 5 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.csv` | Create (39 cols × 6 rows incl. header) |
| 6 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.md` | Create (≥19 sections; §10 probability-only) |
| 7 | `planning/INDEX.md` | Update |
| 8 | `CHANGELOG.md` | Update |
| 9 | `pyproject.toml` | Update (version 3.76.0 → 3.77.0) |

### MD section outline (≥19 sections; enforced at T06)

1. Non-Materialization Disclaimer
2. Parent PR #242 Lineage
3. Parent PR #243 Lineage (Q5 Preserved)
4. Parent PR #245 Lineage (Q6 Discharged)
5. Parent PR #247 Lineage (Q6F → this proof)
6. Q6G-Only Scope
7. Glicko-2 Single-Candidate Justification (A5)
8. Algorithm Specification (event-by-event reference + batched-production shape; **only section permitted to reference Glicko-2 symbols mu / sigma / RD / phi / tau** per NIT-N1 / A20)
9. Forward-Only Update Semantics + Strict-`<` Filter Inheritance
10. Metric Definitions + Bootstrap Policy (A21)
11. Per-Path Metric Table (Rows 1 & 2)
12. Q6G Selected Policy Binding Row (Row 5)
13. Materialization Permission Statement
13a. Equivalence Proof Result (BLOCKER-1; A19; emits Spearman ρ, |Δ log-loss|, SE_event, pass/fail flags)
13b. Byte-Determinism Proof Result (Row 4 hash equality)
14. Non-Substitution Statement
15. Limitations (NIT-N4; toon_id region scope, cold-start gate, PHA decisive-only)
16. Falsifier Roll-Call
17. SHA Provenance (8 parent SHAs)
18. No Step 02_01_03 Closure / No Phase 03 Start
19. Citation Provenance (Glickman 1999 / 2012; Efron-Tibshirani 1993; Higham 2002)

### MD §10 sample table (NIT-N1; probability-only)

| pha_row_index | predicted_probability |
|---|---|
| 0 | 0.XXXXXX |
| 1 | 0.XXXXXX |
| 2 | 0.XXXXXX |
| 3 | 0.XXXXXX |
| 4 | 0.XXXXXX |

(5 rows; floats in [0, 1]; no other column; no raw rating-state value.)

### Forbidden files (zero-diff for both this Layer-1 PR and the future Layer-2 PR)

| Path / pattern | Reason |
|---|---|
| Any `*.parquet` under any `reports/artifacts/` path | No feature materialization in Q6G |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}` | No CROSS-02-01 audit until Layer-3 materialization |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` | No Step closure until Layer-3 materialization (or omit-and-unblock follow-up PR) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` | Derived from STEP_STATUS; no closure here |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` | Phase 03 stays not_started |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` | Per PR #242/#243/#245/#247 precedent |
| `reports/research_log.md` | No CROSS entry; sc2egset-internal |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | ROADMAP stub for 02_01_03 already exists (PR #239) |
| `reports/specs/02_*.md` | Spec edits CROSS-02-XX-only; Q6G does not amend specs |
| `data/db/schemas/views/*.yaml` | No cleaning-layer/view changes |
| `thesis/**`, `docs/**`, `.claude/**` | Out of scope |
| `data/**` | Out of scope |
| `src/rts_predict/games/aoe2/**`, `tests/rts_predict/games/aoe2/**` | Out of scope (AoE2) |
| `planning/current_plan*.md` in the FUTURE Layer-2 PR | Next planning round overwrites these |
| `sandbox/jupytext.toml` | Existing config; no edit |
| `src/rts_predict/games/sc2/datasets/sc2egset/survey_history_rating_algorithms.py` (PR #247 module) | Read-only import; no edit |
| Any TrueSkill engine code in Q6G | A5 + falsifier `q6g_no_trueskill_re_implementation` |

## Gate Condition

The Layer-2 PR (future) is complete only when ALL of the following observable conditions hold. These are the conditions the Layer-2 reviewer-adversarial verifies.

**(a) Artifact integrity:**
- a1. `02_01_03_q6g_rating_implementation_proof.csv` exists at the path in File Manifest #5; has exactly 39 data columns + 1 header (column count assertion via `head -1 <csv> | tr ',' '\n' | wc -l == 39`).
- a2. The CSV has exactly 5 data rows + 1 header.
- a3. `02_01_03_q6g_rating_implementation_proof.md` exists at the path in File Manifest #6; has ≥ 19 `## ` sections.
- a4. The MD §10 sample table has exactly 5 data rows, each with exactly 2 columns (`pha_row_index`, `predicted_probability`), each `predicted_probability` is a float in [0, 1] (NIT-N1 / A20).
- a5. The MD contains zero substring matches of `mu=`, `sigma=`, `RD=`, `phi=`, `tau=` OUTSIDE of §8 (NIT-N1 grep-check; A20).
- a6. CSV byte-stability: re-running the writer produces a bit-identical CSV.

**(b) Methodology integrity (BLOCKER-1):**
- b1. Row 3's `equivalence_proof_statistics` JSON is populated with `{"spearman_rho", "abs_delta_log_loss", "se_log_loss_event", "passes_spearman_bound", "passes_delta_log_loss_bound"}` — all 5 keys present with non-sentinel values.
- b2. Row 4's `byte_determinism_proof_statistics` JSON is populated with `{"run_a_sha256", "run_b_sha256", "hashes_equal"}` — all 3 keys present.
- b3. **If Row 5's `proof_verdict == "bind_now"`, then Row 3's `passes_spearman_bound == True` AND `passes_delta_log_loss_bound == True` AND Row 4's `hashes_equal == True`.** This is the BLOCKER-1 / A19 / NIT-N2 gate. Failure of this clause invalidates the entire Layer-2 PR; the auto-derived rule MUST emit `bind_now` only when all three conditions hold.
- b4. Falsifier `q6g_bind_now_emitted_without_equivalence_pass` (the BLOCKER-1 enforcement helper) does NOT fire on the auto-derived verdict.
- b5. PR #247's `_run_glicko2_survey` is **imported, not re-implemented**, for Row 1 (A18; verified by grep over the proof module).
- b6. Row 5's verdict is one of {`bind_now`, `recommendation_only_glicko2`, `defer_to_two_candidate_implementation_comparison`, `omit_reconstructed_rating_and_unblock_other_five`, `deferred_blocker`}. (The auto-derived rule emits only the first three; the others are reachable only via executor override with reviewer-adversarial sign-off.)

**(c) Schema integrity (NIT-N3):**
- c1. CSV column count == **39** in all of: module assertion (`assert len(Q6G_PROOF_SCHEMA) == 39`), CSV header, MD §11 column count statement, `TestModuleConstants` assertion. Reconciled in 4 places.
- c2. The 5 new NIT-N3 columns (`bootstrap_random_seed`, `rating_period_days`, `glicko2_iteration_tol`, `numpy_rng_bit_generator`, `python_floating_point_summation_order_policy`) are present and populated with the pinned values from A21 / A22 on every row.

**(d) Test integrity:**
- d1. `pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_proof_glicko2_implementation.py -v` reports ≥150 tests, all passing.
- d2. Branch coverage on `proof_glicko2_implementation` ≥ 95%.
- d3. `TestBlockerGuard_BindNowRequiresEquivalence` passes (verifies BLOCKER-1 enforcement).
- d4. `TestNIT_N1_MDSampleIsProbabilityOnly` passes.

**(e) Provenance integrity:**
- e1. All 8 parent SHAs match the pinned constants in the plan frontmatter.
- e2. CHANGELOG and pyproject reflect 3.76.0 → 3.77.0.
- e3. `planning/INDEX.md` archives PR #247 and registers the new Q6G active entry.

**(f) Non-batching / non-creep integrity:**
- f1. No `.parquet` written; no STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS mutation; no research_log entry; no ROADMAP edit; no spec edit; no leakage_audit file; no `data/db/schemas/views/*.yaml` mutation.
- f2. No TrueSkill engine code present in `proof_glicko2_implementation.py` (A5 / `q6g_no_trueskill_re_implementation`).

## Out of scope

The following are explicitly OUT OF SCOPE for both this Layer-1 plan PR and the future Layer-2 Q6G execution PR. Anything here is forbidden in Q6G even if discovered to be useful during execution; it must be deferred to a separate PR with its own planning round.

- **Phase 03 baselines / `create_temporal_split()` / cold-start gate G-CS-6.** Phase 03 stays `not_started` (PHASE_STATUS.yaml).
- **Layer-3 `reconstructed_rating` materialization.** Even if Q6G emits `bind_now`, materialization is a separate PR with its own CROSS-02-01 leakage audit.
- **TrueSkill re-implementation.** A5; the Q6H two-candidate comparison (if needed) is a separate PR.
- **`rating_period_days` sensitivity arm `{7, 30, 90}`.** A22; OQ6; deferred to a future Q6H or Layer-3-internal sensitivity step.
- **Hyperparameter tuning.** A9; literature defaults only.
- **BTL / Aligulac / Bradley-Terry / Neural-BTL.** Inherits PR #245 / PR #247 N-1 carry-forward rejection.
- **Raw MMR hybrid (`raw_mmr_where_present_plus_is_mmr_missing`).** Inherits PR #245 N-2 rejection.
- **Re-adjudication of Q5 / Q6F / Q1–Q4 / Q7 / Q8.** Q6G emits a Q6G verdict only; it does not retract or revisit any prior verdict.
- **Worldwide-identity migration.** NIT-N4 Limitations acknowledges toon_id region scope as accepted bias.
- **AoE2.** SC2EGSet-internal only.
- **Step 02_01_03 closure.** Reserved for the Layer-3 materialization PR (or named omit-and-unblock follow-up).
- **CROSS-02-01 audit file.** Reserved for Layer-3.
- **Any `.parquet` output.** A13.
- **External package additions (e.g., `trueskill`, `glicko2`, `openskill`).** Glicko-2 is implemented in-repo (T03); no PyPI dependency added.

### Falsifier index (BINDING; minimum set; the Layer-2 executor MUST register all of these in `FALSIFIER_PRIORITY_CHAIN`)

| Falsifier key | Failure mode it traps | Plan reference |
|---|---|---|
| `q6g_batched_event_ordering_equivalence_unproven` | Spearman ρ < 0.99 OR \|Δ log-loss\| > SE_event | A19 / BLOCKER-1 |
| `q6g_bind_now_emitted_without_equivalence_pass` | Row 5 verdict == `bind_now` while Row 3 fails any equivalence bound OR Row 4 fails determinism | BLOCKER-1 enforcement guard / T05 step 5 / Gate b3 |
| `q6g_raw_mu_or_sigma_persisted_in_md` | Any of `mu=`, `sigma=`, `RD=`, `phi=`, `tau=` appears in MD §10 or any non-§8 section | NIT-N1 / A20 |
| `q6g_decision_count_mismatch` | CSV decision count ≠ 5 | A11 |
| `q6g_decision_id_order_mismatch` | Decisions not in canonical A11 order | A11 |
| `q6g_q5_re_adjudication_drift` | Any Q5-verdict-bearing token appears in a Q6G verdict-bearing field | A2 |
| `q6g_q6f_re_adjudication_drift` | Any Q6F-verdict-bearing token appears in a Q6G verdict-bearing field | A3 |
| `q6g_no_trueskill_re_implementation` | TrueSkill symbols/code present in Q6G module | A5 |
| `q6g_rating_period_days_not_30` | RATING_PERIOD_DAYS != 30 | A22 |
| `q6g_bootstrap_seed_not_42` | BOOTSTRAP_RANDOM_SEED != 42 | A21 |
| `q6g_bootstrap_block_count_not_200` | BOOTSTRAP_BLOCK_COUNT != 200 | A21 |
| `q6g_bootstrap_method_not_deterministic_percentile` | BOOTSTRAP_METHOD != "deterministic_percentile" | A21 |
| `q6g_numpy_rng_not_pcg64` | NUMPY_RNG_BIT_GENERATOR != "PCG64" | A21 |
| `q6g_python_summation_policy_not_sorted_then_kahan` | PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY != "sorted_then_kahan" | A21 |
| `q6g_rating_trace_persistence_violation` | Any `.parquet`/`.json`/`.npz`/`.pkl` written outside CSV+MD pair | A17 |
| `q6g_materialization_creep` | Any row has non-empty `materialized_output_paths` | A13 |
| `q6g_status_drift` | Any STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS file modified | A14 |
| `q6g_research_log_drift` | Any research_log.md modified | A14 |
| `q6g_roadmap_drift` | ROADMAP.md modified | A14 |
| (8 parent-SHA-mismatch keys for PR #242/#243/#245/#247 CSV+MD) | Any pinned SHA does not match | A1 |

## Open questions

- **OQ1 — Final Q6G_selected_policy.** Default expected outcome is **`recommendation_only_glicko2`** per NIT-N2, UNLESS A19's equivalence criterion passes AND Row 4's determinism passes (then `bind_now` becomes reachable; the auto-derived rule emits it under those conditions). The Layer-2 executor's substantive examination of the Spearman ρ + |Δ log-loss| numbers decides; the auto-derived verdict is the planner's recommendation. Resolves by: Layer-2 executor + Layer-2 reviewer-adversarial Round 1.
- **OQ2 — Whether the executor overrides the auto-derived verdict.** The decision rule emits only one of {`bind_now`, `recommendation_only_glicko2`, `deferred_blocker`}. If the executor wants to emit `defer_to_two_candidate_implementation_comparison` or `omit_reconstructed_rating_and_unblock_other_five`, that requires substantive PR-description reasoning AND reviewer-adversarial Round 1 sign-off. Resolves by: Layer-2 executor + reviewer-adversarial.
- **OQ3 — Whether to add `scipy` as a dependency (for `scipy.stats.spearmanr`).** Check `pyproject.toml` at Layer-2 execution time; if `scipy` is already a transitive dependency of sklearn, no new add; otherwise the executor either adds `scipy` or hand-implements Spearman ρ via NumPy's rank API. Resolves by: Layer-2 executor at T05.
- **OQ4 — Whether the `equivalence_proof_statistics` JSON column needs structural validation (e.g., a Pydantic-style schema) or whether the dict-literal pattern in PR #247 is sufficient.** Default: dict-literal sufficient (matches PR #247). Resolves by: Layer-2 executor at T05.
- **OQ5 — Whether `TestKahanSummationOrder` should be a property-based test (Hypothesis) or a hand-curated fixture.** Default: hand-curated fixture matching PR #247's test style. Resolves by: Layer-2 executor at T08.
- **OQ6 — `rating_period_days` sensitivity arm `{7, 30, 90}`.** Per NIT-N5: cite Glickman 2012 §10 as the accepted default (30 days; matches the paper's worked example); the `{7, 30, 90}` sensitivity arm is OUT OF SCOPE for Q6G and is deferred to a future Q6H or Layer-3-internal sensitivity step. The planner explicitly recommends deferral. Resolves by: future Q6H or Layer-3 planning PR.

## Adversarial-Review Adjustments

### Round 1 (HOLD; addressed below verbatim)

Round 1 reviewer-adversarial returned **HOLD** on the prior draft with 1 BLOCKER (BLOCKER-1) + 6 NITs (NIT-N1 through NIT-N6). Round 1 of the 3-round Layer-1 cap is consumed.

### Round 2 amendment

This Round 2 amendment incorporates the BLOCKER and all 6 NITs as binding methodology (not as prose-only acknowledgements). Each amendment is traceable to a specific assumption, falsifier, OQ, or schema column. The traceability index:

| Round 1 finding | Where it is now binding in this plan | Falsifier or schema column |
|---|---|---|
| **BLOCKER-1** (event-vs-batched equivalence pre-required before `bind_now`) | A19 (new BINDING assumption); T03 (batched engine); T05 step 1 (equivalence computation); T05 step 4 (decision rule's `Equivalence pass` gate); T05 step 5 (BLOCKER-1 guard falsifier); Gate clause (b3) (`bind_now` permitted only if equivalence pass + determinism pass); MD §13a (Equivalence Proof Result section). Schema column 24 `equivalence_proof_statistics`. | `q6g_batched_event_ordering_equivalence_unproven`; `q6g_bind_now_emitted_without_equivalence_pass` |
| **NIT-N1** (MD §10 sample is probability-only, exactly 5 floats in [0, 1]) | A20 (new BINDING assumption); T06 step 4 (probability-only sample table emission); T06 step 5 (NIT-N1 writer-time grep-check); MD §10 section specification (under §File Manifest "MD section outline"); MD §8 is the only section permitted to reference Glicko-2 symbols (mu/sigma/RD/phi/tau); test `TestNIT_N1_MDSampleIsProbabilityOnly`; Gate clauses (a4) and (a5). | `q6g_raw_mu_or_sigma_persisted_in_md` |
| **NIT-N2** (`recommendation_only_glicko2` is realistic default expected outcome) | OQ1 (rewritten to make `recommendation_only_glicko2` the default expected outcome); T05 step 4 (decision rule's middle branch named `recommendation_only_glicko2` with explicit Q6F-CI-overlap reasoning quoted in the rule's rationale string); A12 row 2 (materialization permission matrix for `recommendation_only_glicko2`); Scope (outcome #3 in the bullet list). | (not a falsifier; a decision-rule branch) |
| **NIT-N3** (schema delta 34 → 39 with 5 new columns; reconciled everywhere) | A21 (the 5 new constants `BOOTSTRAP_METHOD`, `BOOTSTRAP_RANDOM_SEED`, `BOOTSTRAP_BLOCK_COUNT`, `NUMPY_RNG_BIT_GENERATOR`, `PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY` populate the 5 new schema columns); T01 step 8 (39-column schema enumerated; columns 35–39 are the new NIT-N3 columns); T08 `TestModuleConstants` (asserts schema length == 39 + each pinned constant); Gate clauses (c1) and (c2); File Manifest MD section outline §11 (will report `column count = 39`). Schema-parity-with-Q6F note: Q6F CSV = 44 cols (includes 14 metric/CI cols for 4 candidates); Q6G CSV = 39 cols (Q6G uses 2 different proof-class statistic columns `equivalence_proof_statistics` + `byte_determinism_proof_statistics` instead of the Q6F per-candidate AUC CI block); Q6G is NOT a subset of Q6F — it is the implementation-proof schema. | `q6g_rating_period_days_not_30`; `q6g_bootstrap_seed_not_42`; `q6g_bootstrap_block_count_not_200`; `q6g_bootstrap_method_not_deterministic_percentile`; `q6g_numpy_rng_not_pcg64`; `q6g_python_summation_policy_not_sorted_then_kahan` |
| **NIT-N4** (Limitations paragraph; toon_id region scope = accepted bias) | New `### Limitations` subsection inside §Assumptions & Unknowns (between Assumptions and Unknowns); MD §15 "Limitations" section (added to MD outline; mirrors the Limitations subsection verbatim). | (not a falsifier; a declared bias) |
| **NIT-N5** (rating-period sensitivity deferred; cite Glickman 2012 §10) | A22 (BINDING assumption: rating_period_days pinned at 30 per Glickman 2012 §10 worked example; `{7, 30, 90}` sensitivity arm out of scope, deferred); OQ6 (rewritten to record the planner's explicit recommendation to defer); §Out of scope (the rating_period_days sensitivity arm explicitly listed); schema column 36 `rating_period_days` (pinned 30); falsifier `q6g_rating_period_days_not_30`. | `q6g_rating_period_days_not_30` |
| **NIT-N6** (deterministic percentile bootstrap; seed 42; 200 blocks; PCG64; sorted-then-Kahan summation) | A21 (BINDING assumption: bootstrap_method_policy with 5 pinned constants); T04 step 2 (`_compute_deterministic_percentile_ci` implementation honours every constant); T03 step 7 (per-row summation uses `sorted_then_kahan`); T08 `TestDeterministicBootstrap`, `TestKahanSummationOrder`; schema columns 35 + 38 + 39; the literature citations `CITATION_EFRON_TIBSHIRANI_1993` + `CITATION_KAHAN_SUMMATION_HIGHAM_2002` added under External literature. Cross-referenced from A19: SE_log_loss_event used in the equivalence bound is derived from this exact bootstrap method, so the equivalence proof is reproducible. | `q6g_bootstrap_seed_not_42`; `q6g_bootstrap_block_count_not_200`; `q6g_bootstrap_method_not_deterministic_percentile`; `q6g_numpy_rng_not_pcg64`; `q6g_python_summation_policy_not_sorted_then_kahan` |

### Critique instruction (per planner output contract)

For Category A: adversarial critique is required before execution begins. Dispatch reviewer-adversarial for Round 2 review of this amended plan. Reviewer-adversarial Round 2 reads this entire document including the `### Round 2 amendment` traceability table above. The plan goes through 0–2 further rounds (cap = 3; Round 1 consumed; Round 2 consumed by upcoming dispatch; Round 3 available if Round 2 surfaces a new BLOCKER) before Layer-2 execution begins.

---

**End of Round 2 amended plan. Document length ≈ 720 lines (under the 800-line cap). All 10 named `##` sections present. All Round 1 findings (BLOCKER-1 + NIT-N1..N6) are incorporated as binding methodology with explicit traceability.**
