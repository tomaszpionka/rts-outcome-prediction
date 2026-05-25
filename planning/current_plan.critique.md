---
reviewer_role: reviewer-adversarial
reviewer_model: claude-opus-4-7[1m]
reviewer_date: 2026-05-25
plan_base_ref: ee15d3625eee60688776219f533d4a5ceefb4b76
plan_file: planning/current_plan.md
chosen_outcome: A
branch: feat/sc2egset-02-01-03-q6f-rating-algorithm-survey
planning_pr_number: TBD
planning_pr_url: TBD
planning_pr_state: draft
verdict: APPROVE-WITH-NITS
blockers: 0
nits: 4
round: 1
round_cap: 3
future_layer2_pr_number: TBD
future_layer2_version_bump: 3.75.0 -> 3.76.0
parent_planning_pr: 244
parent_execution_pr: 245
parent_q5_pr: 243
parent_q1_q4_q7_q8_pr: 242
---

# Q6F plan adversarial review

## Metadata

- Plan: `planning/current_plan.md`
- Plan author: `@planner-science` (Opus 4.7, 1M context)
- Plan timestamp: 2026-05-25
- Reviewer: `@reviewer-adversarial`
- Review timestamp: 2026-05-25
- Round: 1 of 3 (adversarial cap; per `feedback_adversarial_cap_execution.md`)
- Chosen outcome under review: A — Q6F rating-algorithm survey planning PR
- Branch: `feat/sc2egset-02-01-03-q6f-rating-algorithm-survey`
- Layer: Layer-1 (planning-only; 2-file diff)
- Predecessors verified:
  - PR #242 (Q1-Q4, Q7, Q8 ratified)
  - PR #243 (Q5 resolved; `Q5_selected_policy = sensitivity_indicator_co_registration`, verdict `narrow_with_evidence`, BINDING)
  - PR #244 (Q6 Layer-1 plan; APPROVE-WITH-NITS Round 1)
  - PR #245 (Q6 Layer-2 execution; verdict `deferred_blocker`; materialization `blocked_pending_algorithm_survey_pr`; this Q6F survey is the named unblock)

## Verdict: APPROVE-WITH-NITS

The plan is materializable as a 2-file Layer-1 planning-only PR. The chosen outcome (A — Q6F rating-algorithm survey) is correctly motivated and uniquely justified. **0 blockers; 4 cosmetic nits** — all inlined into the plan's `## Adversarial-Review Adjustments (Round 1)` section as Layer-2 executor guidance. The most subtle scope risk (Q6F survey drifting into Phase 03 baseline modelling) is enforced by 4 independent falsifiers (`q6f_phase_03_baseline_creep`, `q6f_train_test_split_referenced`, `q6f_global_batch_fit_referenced`, `q6f_target_match_outcome_read_as_input`) plus the T03 prediction-before-update protocol.

## 11-point checklist

1. **Q6F-as-next-atomic-step — PASS.** Lines 73-79 reject outcomes B-F with cited reasons. B violates I7 (Q6 still `deferred_blocker_with_algorithm_survey_required`). C violates non-batching rule. D would train Phase 03 on a spec-disowned feature universe. E (hygiene-only) has no real blocker. F forfeits a known-required step. The "direct materialization with omit" alternative is correctly subsumed under Q6F itself as the `omit_reconstructed_rating_and_unblock_other_five` verdict branch (lines 42, 147-148, 282-286), so the omit path is reachable WITHIN Q6F without bypassing the survey. Airtight.

2. **Materialization barred — PASS.** Multiple layered enforcement: Assumption 14 (`materialized_output_paths` MUST be empty on every row); Assumption 18 (evaluation traces are EPHEMERAL — NOT persisted to Parquet, JSON, npz, pkl); falsifier `q6f_materialization_creep`; falsifier `q6f_rating_trace_persistence_violation`; falsifier `q6f_rating_object_persistence_violation`; Forbidden Files table bars any `*.parquet`. The evaluation-trace-vs-feature distinction is unambiguous at line 66 ("evaluation traces of forward-only rating predictions ... Q6F-internal artifacts ONLY"). Falsifier-enforced.

3. **Survey vs Phase 03 baseline modelling — PASS.** Lines 67-69, 250, 266 distinguish: (a) no train/test split / temporal CV / k-fold (falsifier `q6f_train_test_split_referenced`); (b) no model object fit — rating engines are forward-only online updaters, not classifiers; (c) no global / batch fit (falsifier `q6f_global_batch_fit_referenced`); (d) target-game outcome read as evaluation target only (falsifier `q6f_target_match_outcome_read_as_input`); (e) explicit `q6f_phase_03_baseline_creep` falsifier with explanation that T04 metrics are NOT Phase-03 baselines. T03's forward-only protocol at line 244-248 is correctly described: "predicted probability ... using ONLY the rating state accumulated from rows with strictly-earlier ... timestamp ... after scoring row R, the rating state is updated using R's actual outcome (which becomes input to FUTURE rows' predictions but NEVER to R's own prediction)." Boundary clean.

4. **AUC / log-loss / Brier as evaluation targets only — PASS.** T03 line 247: "After scoring row R, the rating state is updated using R's actual outcome (which becomes input to FUTURE rows' predictions but NEVER to R's own prediction)." T04 line 266: "the rating INPUT for each prediction never sees the future actual." Two falsifiers enforce: `q6f_target_match_outcome_read_as_input` and `q6f_future_match_leakage_referenced`. Invariant I3 (`history_time < target_time`) is honoured via the inherited `STRICT_LT_HISTORY_FILTER` constant.

5. **Candidate completeness and fairness — PASS.** 4 included + 2 carry-forward (lines 105-114). Rolling-baseline justified as "rating proxy without opponent strength; baseline" (line 107) — legitimate floor; the survey would lack a "no opponent-strength" reference otherwise. Elo K=24 (midpoint between K=20 and K=32 with rationale). Glicko-2 defaults pinned per Glickman 2012. TrueSkill 1v1→Glicko-like degeneracy noted in Assumption 7 and tested in T08 `TestTrueSkillEngine`.

6. **BTL / Bradley-Terry / Neural BTL inclusion — PASS.** Assumption 8 carries forward PR #245 N-1 rejection with rationale: "BTL collapses to Elo-with-race-prior in 1v1; Neural BTL needs its own model-training pipeline." Rejection re-stated in every row's `excluded_methods_considered` column. Executor permitted to expand IFF substantive case + citations + fixtures. Defensible.

7. **Raw MMR hybrid rejection — PASS.** Assumption 9 carries PR #245 N-2 rationale. See NIT-1 (schema clarity).

8. **Q5 binding preserved — PASS.** Q5 cited as BINDING at line 95 with explicit re-affirmation protocol: cross-region history rows are NOT dropped from survey input; `is_cross_region_fragmented` is a co-registered evidence dimension. Falsifier `q6f_q5_re_adjudication_drift` halts entrypoint if any survey row carries Q5-verdict-bearing token in verdict-bearing field. MD §3 re-affirms.

9. **Schema sufficiency and determinism — PASS.** 36 columns (lines 405-444); all 6 SHA fields named with `_sha256` suffix; `materialized_output_paths` is column 34 and Assumption 14 plus falsifier `q6f_materialization_creep` enforces empty. Byte-stability via dual-write hash check (T06, T08). See NIT-2 (column-count consistency).

10. **No status / no research_log / no ROADMAP / no Phase 03 creep — PASS.** `## Out of scope` (lines 521-541) lists 14 forbidden mutations, each with named falsifier. Forbidden Files table bars STEP_STATUS, PIPELINE_SECTION_STATUS, PHASE_STATUS, research_log (dataset + reports), ROADMAP, CROSS-02-01 audit. Gate Condition #12 re-asserts.

11. **Blockers — NONE.** All 11 checks pass.

## Additional adversarial probes

- **Plan-required `##` sections — PASS.** 10 sections present at lines 27, 52, 81, 168, 197, 362, 470, 503, 521, 543 (8 required + `## Out of scope` + `## Adversarial-Review Adjustments`).
- **Hyperparameter discipline — PASS.** Assumption 10 pins fixed literature defaults and explicitly bars tuned variants. OQ2 cleanly defers tuning to a hypothetical "Q6G" follow-up Step. Defensible.
- **Cold-start floor — PASS-WITH-CAVEAT.** OQ4 acknowledges `cold_start_rate ≥ ~50%` structurally; recommends reporting but not gating. No arbitrary threshold pinned, which is correct given I7.
- **Selected_policy AUC floor — NIT-3.** AUC_FLOOR=0.55 and AUC_BIND_THRESHOLD=0.60 pinned in T05 with rationales not cited to a primary source.
- **PR-number normalisation — PASS.** Standard PR #244/#245 precedent.
- **Branch naming — PASS.** `feat/sc2egset-02-01-03-q6f-rating-algorithm-survey` consistent with PR #242/#243/#245.
- **N-3 player_id_worldwide handling — PASS.** Assumption 11 acknowledges PHA has no `player_id_worldwide`; mandates `toon_id` as grouping key per PR #245 §9.
- **Critique stub format — PASS.** Matches PR #244/#245 precedent.

## Nits (non-blocking; all 4 inlined into plan)

### NIT-1 — Schema clarity for `raw_mmr_hybrid_rejection`

**Severity:** soft (Layer-2 executor SHOULD address).

**Evidence:** Assumption 9 (line 117) references a "`raw_mmr_hybrid_rejection` field" that does NOT appear in the canonical 36-column `Q6F_SURVEY_SCHEMA` (lines 408-444). The schema comment at line 446 says the N-2 rejection string is carried in the `notes` column (column 35). This is consistent (per-row N-2 rejection lives in `notes`), but Assumption 9's wording implies a dedicated field.

**Fix (inlined):** Layer-2 executor chooses one path: (a) add `raw_mmr_hybrid_rejection` as column 37 of `Q6F_SURVEY_SCHEMA`, mirroring PR #245's dedicated-column pattern exactly (preferred for PR #245 parity); or (b) reword Assumption 9 in the future MD §7 to say "the raw-MMR-hybrid rejection token is carried in the `notes` column per row" (less mirroring; valid). Document the choice in the Layer-2 PR body.

### NIT-2 — Trivial column-count consistency

**Severity:** trivial.

**Evidence:** `## Scope` line 36 says "≥36 columns" — should say "exactly 36 columns" to match the canonical schema declaration. One-word edit.

**Fix (inlined):** Layer-2 executor changes "≥36" → "exactly 36" (or "exactly 37" if NIT-1 path (a) is chosen).

### NIT-3 — AUC threshold rationale citation

**Severity:** soft (Layer-2 executor SHOULD address).

**Evidence:** T05's `AUC_FLOOR=0.55` and `AUC_BIND_THRESHOLD=0.60` are pinned with informal rationales ("5% above no-skill ... commonly used in calibration literature" and "defensible 'genuine forward-only skill signal' floor for ~22K decisive matches"). These are borderline Invariant I7 (no magic numbers — every threshold traced to data or citation). OQ1 surfaces this; OQ7 provides a tie-breaking fallback.

**Fix (inlined):** Layer-2 executor chooses one path: (a) cite a primary source for the floor (e.g., Steyerberg 2009 §5.4 on AUC interpretation; Hosmer-Lemeshow 2013 on weak-discrimination floors); or (b) compute bootstrap CIs on each candidate's AUC and use the lower-CI-bound > 0.5 test instead of pinning a numeric floor. The plan's default (keep pinned thresholds, surface follow-up PR if metrics are bunched) is defensible but not maximally rigorous.

### NIT-4 — TrueSkill `tau` justification

**Severity:** trivial.

**Evidence:** Assumption 10 sets TrueSkill `tau=25/300` without justification (the `draw_margin=0` rationale at "PHA is decisive-only per PR #242 Q1" IS justified). Trivial — Herbrich et al. 2006 defaults are standard.

**Fix (inlined):** Layer-2 executor adds inline citation to Herbrich-Minka-Graepel (2006) §4 for the default `tau` value, or documents the choice as "literature default."

## Non-issues considered and dismissed

- **Materialization gate framing.** 5-layer enforcement; clean.
- **Survey vs Phase 03 baseline.** 4 falsifiers + T03/T04 protocol enforce.
- **AUC/log-loss/Brier as evaluation targets only.** T03 "prediction-before-update" protocol explicit; 2 falsifiers enforce.
- **Q6F-as-next-atomic-step.** Outcomes B-F airtight rejection.
- **Candidate completeness.** 4 included + 2 carry-forward justified.
- **BTL / Bradley-Terry / Neural BTL inclusion.** Carry-forward as N-1 rejection from PR #245.
- **Raw MMR hybrid rejection.** Carry-forward as N-2 rejection from PR #245.
- **Q5 binding preserved.** Falsifier `q6f_q5_re_adjudication_drift` enforces.
- **Hyperparameter discipline.** Fixed-defaults-only declaration defensible.
- **Cold-start floor.** Reported but not gated; correct given I7.
- **No status / no research_log / no ROADMAP / no Phase 03 creep.** 14 forbidden mutations with named falsifiers.
- **N-3 player_id_worldwide handling.** Correctly carried forward as `toon_id` per PR #245 §9.

## Summary

| Dimension | Verdict |
|---|---|
| Outcome A defensibility | yes — uniquely motivated; B/C/D/E/F rejections cite verifiable evidence |
| Q6F-vs-Phase-03 boundary | clean — 4 falsifiers + T03/T04 prediction-before-update protocol |
| Candidate-set completeness | yes — 4 included + 2 carry-forward, justified |
| BTL / raw-MMR carry-forward | correct — PR #245 N-1 and N-2 rationale preserved |
| Q5 binding preservation | enforced via falsifier `q6f_q5_re_adjudication_drift` |
| Schema sufficiency | yes — 36 columns, SHA fields properly typed, materialization gated |
| Falsifier-set completeness | yes — 4 Phase-03-creep falsifiers + 2 leakage falsifiers + parent-SHA pinning |
| Materialization-gate framing | correct — 5-layer enforcement |
| Total blockers | 0 |
| Total nits | 4 (NIT-1 and NIT-3 SHOULD be addressed by Layer-2; NIT-2 and NIT-4 trivial) |
| Recommendation | materialize draft PR; Layer-2 dispatch in separate session after user review |

Round 1 of 3 adversarial cap consumed.

## Layer-2 dispatch reminder for the parent session

After this planning-only PR is reviewed and merged, the next session's executor:

- Reads `planning/current_plan.md` (this Q6F plan) directly.
- Addresses NIT-1 (schema/prose alignment for `raw_mmr_hybrid_rejection`) and NIT-3 (AUC threshold citation) per the plan's `## Adversarial-Review Adjustments (Round 1)` guidance.
- Treats NIT-2 and NIT-4 as cosmetic / trivial.
- Routes T03 + T05 (substantive rating-engine + verdict reasoning) to Opus; T01-T02 / T04 / T06-T09 may use Sonnet.
- Dispatches `@reviewer-adversarial` as the Layer-2 final gate; the adversarial 3-round cap resets for Layer-2 (per `feedback_adversarial_cap_execution.md` symmetric application).
- Does NOT begin Step 02_01_04 or Phase 03 work.
- Does NOT materialise the `reconstructed_rating` Parquet column (the Q6F survey produces a CSV/MD verdict, NOT a feature artifact).
