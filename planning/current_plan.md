---
plan_role: planner-science
plan_model: claude-opus-4-7[1m]
plan_date: 2026-05-26
date: 2026-05-26
plan_layer: 1 (planning-only; 2-file diff) — Round 2 amendment + Round-2-mechanical-fix
chosen_outcome: A
branch: feat/sc2egset-02-01-03-q6h-rating-path-decision
future_layer2_version_bump: 3.77.0 -> 3.78.0
planning_pr_version_bump: none (planning-only; matches PR #240 / #244 / #246 / #248 precedent)
this_planning_pr_category: A
category: A
parent_planning_pr: 248 (merged 2026-05-26; Q6G Layer-1 plan)
parent_execution_pr: 249 (merged 2026-05-26; Q6G Layer-2 execution; recommendation_only_glicko2)
parent_q6f_pr: 247 (merged; Q6F narrow_with_evidence; BINDING)
parent_q6_pr: 245 (merged; Q6 deferred_blocker; discharged by Q6F)
parent_q5_pr: 243 (merged; Q5 sensitivity_indicator_co_registration; BINDING)
parent_q1_q4_q7_q8_pr: 242 (merged; RATIFIED)
base_ref: d9276194a1684542a04494ec02df44a5a3f2338e
phase_status_at_plan_time: Phase 02 in_progress; Phase 03 not_started
step_status_at_plan_time: 02_01_02 complete; 02_01_03 in_progress (Q6G recommendation_only_glicko2 -> Q6H final rating-path decision)
non_batching_compliance: this Layer-1 plan does not author any Q6H decision module, validator, notebook, artifact, status YAML, or research_log; the Layer-2 PR is a separate dispatch
adversarial_round_cap: 3 (symmetric per feedback_adversarial_cap_execution.md); Round 1 consumed (HOLD); Round 2 consumed (HOLD-WITH-MECHANICAL-FIX, R2.6 textual correction applied by parent without consuming Round 3); Round 3 remaining
---

# Plan: SC2EGSet Step 02_01_03 — Q6H final rating-path decision (Round 2 amendment + mechanical fix)

## Scope

This is the **Layer-1 planning-only PR** for the FINAL rating-path adjudication
artifact (Q6H) for SC2EGSet Step 02_01_03 after PR #249 (Q6G) merged on
2026-05-26 at master `d9276194a1684542a04494ec02df44a5a3f2338e` with
`Q6G_selected_policy = recommendation_only_glicko2`.

Q6H closes the rating-path question for `reconstructed_rating` (CROSS-02-02
§6.2 L241). It is the **terminal rating-path adjudication artifact** for
Step 02_01_03. After Q6H is merged, **no further Q6X (Q6I, Q6J, …) PRs are
authorised**; the downstream PR is either (i) a Layer-3 materialization PR for
the 5 non-rating history-enriched families (if Q6H = `omit_reconstructed_rating_and_unblock_other_five`),
or (ii) a Layer-3 materialization PR for all 6 families including
`reconstructed_rating` from the event-by-event Glicko-2 path (if Q6H =
`bind_event_by_event_glicko2`), or (iii) a step closure with
`reconstructed_rating` shelved (if Q6H = `recommendation_only_event_by_event_glicko2`
or `deferred_blocker`).

The Layer-2 execution PR (named in the §"File Manifest" Future-Layer-2 block)
will emit ONE adjudication artifact pair (CSV + MD) over four candidate Q6H
verdicts plus one emergent `Q6H_selected_policy` row. The Layer-2 PR is NOT
authored by this plan; it is a separate dispatch.

This planning PR records:

- **2 files only:** `planning/current_plan.md` (this content; Round 2
  amendment + mechanical fix) + `planning/current_plan.critique.md`
  (reviewer-adversarial Round 1 + Round 2 stub).
- **NO version bump** in this PR (matches PR #240 / PR #244 / PR #246 /
  PR #248 planning-only precedent).
- **NO Q6H module / test / notebook / artifact / status YAML / research_log /
  ROADMAP edit / spec edit / Parquet output / Step 02_01_03 closure / Phase 03
  start.**

Branch: `feat/sc2egset-02-01-03-q6h-rating-path-decision`.

## Problem Statement

Q6G's batched-vs-event Glicko-2 equivalence proof **FAILED both bounds** on
the sc2egset PHA corpus: Spearman ρ = 0.2292 (≪ 0.99 threshold) and
|Δ log-loss| = 0.07928 (≫ 1·SE = 0.00219). The byte-determinism proof
**PASSED** (run-A SHA-256 = run-B SHA-256 =
`71e5411024c01eb40018a5c7d0959db8162074e57e99bb5b8532cde247e75d8b`). Under the
Q6G auto-derived decision rule (`equivalence fail → recommendation_only_glicko2`
as NIT-N2 default; `determinism fail → deferred_blocker`), the emergent
verdict was `Q6G_selected_policy = recommendation_only_glicko2`. The
event-by-event reference (Row 1) reproduced PR #247 §11's Glicko-2 metrics to
within `1e-4` (log_loss = 0.625522, brier = 0.217711, calibration_error =
0.034911), establishing it as the validated reference; the rating-period
batched Glicko-2 form is therefore falsified for production materialization
on this corpus.

PR #249 thus left two open propositions:

1. The **batched** Glicko-2 form is non-viable on this corpus (rating_period_days = 30
   is long relative to most toons' time span — median 0.88 d per PR #249 §15 —
   so the batched path's per-row predictions degenerate to the initial-state
   0.5 prediction for ~68% of rows).
2. The **event-by-event** form remains methodologically defensible — it
   reproduced PR #247 §11's metrics — but PR #249 did NOT discharge its
   materialization permission. The permission stays
   `recommendation_only_glicko2_event_by_event_validated_batched_path_unproven_or_unequivalent`.

Q6H must therefore close the rating-path question **without binding the
batched path**. Per the Q6H auto-derived rule defined below, Q6H's canonical
default-expected outcome is `omit_reconstructed_rating_and_unblock_other_five`
under the `THESIS_PRAGMATISM = TRUE` gate (R2.2 admissibility pins). The
Layer-2 executor may override via the documented Branch-(i) substantive-anchor
mechanism, but no further Q6X PRs are authorised after Q6H regardless of
verdict.

### Why outcomes B–G are rejected

- **B — direct Layer-3 materialization (skip Q6H).** REJECTED: PR #249 left
  the materialization permission at `recommendation_only_*`, not `bind_now`.
  Jumping directly to materialization would silently encode an unbinding
  decision as if it were bound; this violates `data-analysis-lineage.md`
  "Artifact discipline".
- **C — direct event-by-event Glicko-2 materialization implementation-proof
  execution without planning.** REJECTED under plan → review → execute
  discipline. No artifact currently permits this skip.
- **D — omit `reconstructed_rating` and directly plan materialization of
  other five families without Q6H adjudication.** REJECTED: the omission
  decision itself must be adjudicated first (the alternative is a silent
  Q6 closure, which falsifier `q6h_silent_q6_closure_on_omit_branch` is
  designed to prevent).
- **E — Phase 03 baseline planning.** REJECTED: Phase 03 stays `not_started`
  per PHASE_STATUS.yaml; CLAUDE.md "NEVER begin a new phase until all prior
  phase artifacts exist on disk".
- **F — hygiene-only PR first.** REJECTED: no concrete repo defect blocks
  Q6H planning. The PR #249-vs-active-line cosmetic staleness in
  `planning/INDEX.md` is not a blocker (the next Layer-2 PR archives it as
  part of the standard release tail).
- **G — hold.** REJECTED: the 6 PRs of Q6 momentum (#244 → #249) make the
  rating-path closure the next-required step; holding would forfeit
  deliverability.

## Assumptions & Unknowns

### Assumptions (BINDING for the future Layer-2 execution PR)

The assumptions below are BINDING. The Layer-2 executor must honour them
verbatim; deviation requires a fresh planning round.

1. **A1 — Parent provenance (10 pinned SHAs).** The Layer-2 module must
   hard-code these as constants:
   - `parent_pr242_csv_sha256 = "f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b"`
   - `parent_pr242_md_sha256  = "fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d"`
   - `parent_pr243_csv_sha256 = "29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424"`
   - `parent_pr243_md_sha256  = "026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719"`
   - `parent_pr245_csv_sha256 = "703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0"`
   - `parent_pr245_md_sha256  = "7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419"`
   - `parent_pr247_csv_sha256 = "249e5591c6505b748fe3d371284a72d8f4620f57dbe9628c908ec2fbf097c8ed"`
   - `parent_pr247_md_sha256  = "4b49bee405bf87d4b8920b188e2c38d185ecc077b532d64a8bdd5a90cdf143f2"`
   - `parent_pr249_csv_sha256 = "1d9ee22e0523e640181fa0a7a7d2680467a267eefa376fec903f58094118b82f"`
   - `parent_pr249_md_sha256  = "8beed3ba6491afb6ba72ee2718b1364c9a2577b26c82237b735d219ccfdc0ea1"`

2. **A2 — Q5 BINDING.** `Q5_selected_policy = sensitivity_indicator_co_registration`,
   verdict `narrow_with_evidence`. Q6H does NOT re-adjudicate Q5. Falsifier
   `q6h_q5_re_adjudication_drift` enforces.

3. **A3 — Q6F BINDING.** `Q6F_selected_policy = narrow_with_evidence`;
   `materialization_permission = recommendation_only_blocked_pending_implementation_proof_pr`.
   The Q6H artifact does NOT re-adjudicate Q6F. Falsifier `q6h_q6f_re_adjudication_drift`.

4. **A4 — Q6G BINDING.** `Q6G_selected_policy = recommendation_only_glicko2`;
   batched-vs-event equivalence FAILED; byte-determinism PASSED. Q6H does NOT
   re-adjudicate Q6G. Falsifier `q6h_q6g_re_adjudication_drift`.

5. **A5 — No TrueSkill re-implementation, no batched Glicko-2 re-attempt.**
   Falsifiers `q6h_no_trueskill_re_implementation` and
   `q6h_no_batched_glicko2_re_implementation` enforce.

6. **A6 — Forward-only inherited.** PR #242 Q3 BIND_NOW
   `STRICT_LT_HISTORY_FILTER = "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"`
   is inherited by reference. Q6H does NOT execute history queries; the
   filter is a constraint communicated to the future materialization PR.

7. **A7 — Event-by-event engine import-by-name only.** If Branch (i)
   `bind_event_by_event_glicko2` is emitted, the future Layer-3
   materialization PR imports PR #247's `_run_glicko2_survey` engine by
   name (it is re-exported via PR #249's
   `proof_glicko2_implementation._run_glicko2_event_by_event_reference`).
   Q6H itself does NOT execute the engine. Falsifier
   `q6h_event_by_event_engine_not_imported_from_pr247` fires on
   re-implementation.

8. **A8 — 5-family post-omit set.** If Branch (iii)
   `omit_reconstructed_rating_and_unblock_other_five` is emitted, the
   permitted-for-materialization set is **CROSS-02-02 §6.2 minus L241
   `reconstructed_rating`** — i.e., the L238-240 + L242-243 rows of
   `reports/specs/02_02_feature_engineering_plan.md`:
   - L238 `focal_player_history`
   - L239 `opponent_player_history`
   - L240 `matchup_history_aggregate`
   - L242 `cross_region_fragmentation_handling`
   - L243 `in_game_history_aggregate`

   This is the R2.1 resolution: the 5-family set is `§6.2 minus L241`.
   Verbatim citation of `lines 238-243` is forbidden because that range
   includes L241 (which is precisely the family being excluded).

9. **A9 — `THESIS_PRAGMATISM` admissibility (R2.2; three pins).** The
   `THESIS_PRAGMATISM` boolean gate that controls Branch (iii) admissibility
   is constrained as follows to prevent magic-gate degeneration under
   Invariant I7:

   - **(a) Admissibility criterion.** `THESIS_PRAGMATISM` may be set to
     TRUE **only if BOTH**:
     - A substantive reasoning paragraph of **≥ 6 sentences** is present in
       the Layer-2 MD §15 ("Thesis-pragmatism rationale"), and that
       paragraph cites PR #249 §15 **finding-by-finding** (minimum 3
       explicit `PR #249 §X.Y` cross-references); AND
     - The Layer-2 PR carries an explicit reviewer-adversarial sign-off
       recording that the substantive paragraph was reviewed against the
       Branch-(iii) precondition and found sufficient.
   - **(b) Canonical default-derivation path.** At Layer-2 dispatch time,
     the default value is:
     `THESIS_PRAGMATISM = TRUE` iff
       - parent PR #249 chose `recommendation_only_glicko2` (verified at
         PR #249 CSV Row 5 `proof_verdict` cell; PR #249 SHA
         `1d9ee22e...` confirms), AND
       - no execution evidence has been gathered between PR #249 merge
         time and Q6H Layer-2 execution time (i.e., no new separating
         anchor produced; no new bootstrap CI re-run that materially
         shifts the Q6G finding).
     Otherwise `THESIS_PRAGMATISM = FALSE`.
   - **(c) Override falsifier.** Any Layer-2 emission of
     `THESIS_PRAGMATISM = FALSE` that is **not** accompanied by the
     substantive reasoning paragraph above OR any emission of `TRUE`
     without the §15 substantive paragraph triggers falsifier
     `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15`.

10. **A10 — 38-column schema (R2.3 resolution).** The Q6H CSV uses exactly
    **38** columns. Column 38 is `materialized_output_paths` (split from
    legacy `notes` per R2.3 so materialization paths are reviewer-grep-able
    without parsing prose). The column count is pinned in **4 reviewer-
    runnable places**: (i) module constant
    `assert len(Q6H_DECISION_SCHEMA) == 38`; (ii) test
    `TestModuleConstants::test_schema_count_equals_38`; (iii) Gate clause
    (c1) `csv.reader` parses exactly 38 fields; (iv) MD §11 column-count
    assertion sentence. Falsifier `q6h_schema_column_count_equals_38`
    enforces.

11. **A11 — 5 decision rows (canonical order).** Q6H emits exactly 5 rows
    in this order: (1) `Q6H_A_bind_event_by_event_glicko2`,
    (2) `Q6H_B_recommendation_only_event_by_event_glicko2`,
    (3) `Q6H_C_omit_reconstructed_rating_and_unblock_other_five`,
    (4) `Q6H_D_deferred_blocker`, (5) `Q6H_selected_policy` (BINDING;
    emergent). Falsifiers `q6h_decision_count_mismatch` and
    `q6h_decision_id_order_mismatch` enforce.

12. **A12 — Decision rule order-of-operations (R2.5 resolution).**
    Evidentiary branches are evaluated **before** the pragmatism branch.
    See §"Decision rule" below for the deterministic (i)→(v) order with
    methodological justification. Falsifier
    `q6h_decision_rule_order_not_evidentiary_first` enforces.

13. **A13 — `materialized_output_paths` MUST be empty on every row.** Q6H
    is an adjudication-class artifact. Falsifier `q6h_materialization_creep`.

14. **A14 — No status YAML / research_log / ROADMAP / spec mutation.**
    Per PR #242 / #243 / #245 / #247 / #249 non-closure precedent. Closure
    of Step 02_01_03 is reserved for the Layer-3 materialization PR (or
    the omit-closure follow-up).

15. **A15 — Test target.** ≥ 250 tests; ≥ 95% branch coverage on the
    Q6H decision module (matches PR #249 Layer-2 floor of 275 tests /
    95.04%).

16. **A16 — Read-only.** Q6H opens DuckDB read-only; writes only the CSV+MD
    pair plus `pytest tmp_path` fixtures.

### Unknowns (DEFERRED with explicit gating)

- **U1 — Final Q6H selected_policy.** Per the canonical default-derivation
  path (A9(b)), the auto-derived default is Branch (iii)
  `omit_reconstructed_rating_and_unblock_other_five`. The Layer-2
  executor's evaluation of Branches (i) and (ii) decides whether the
  default is reached; the auto-derived verdict is the planner's
  recommendation.
- **U2 — Whether a NEW separating anchor exists for Branch (i).** None
  is anticipated under PR #249's CI overlap finding (Q6F §11 Glicko-2
  log-loss CI [0.6216, 0.6302] vs TrueSkill [0.6246, 0.6342], overlap
  ≈ 0.9% of mid-range). The Layer-2 executor may explore Brier / ECE /
  calibration-slope anchors but the plan does NOT pre-authorise a new
  bootstrap.
- **U3 — Whether reviewer-adversarial Round 2 (Layer-2) accepts the
  THESIS_PRAGMATISM substantive paragraph.** The Layer-2 dispatch is
  the venue.

### Limitations (carried forward from Q6G NIT-N4)

- **toon_id is region-scoped** per Invariant #2 branch (iii). Rating
  fragmentation across region-migrating players is an accepted Q6H bias.
  A future worldwide-identity PR (out of scope here) would address it
  separately. This limitation must be re-stated verbatim in MD §13.
- **Cold-start gate (G-CS-4).** Q6H inherits PR #247 / PR #249's
  cold-start mask. The first PHA row for any toon_id contributes nothing
  to metric computation but is counted in `cold_start_rate`.
- **PHA decisive-only.** Per PR #242 Q1, PHA carries decisive results
  only.

## Literature Context

### Internal (BINDING; read before authoring Layer-2 module)

- `reports/specs/02_02_feature_engineering_plan.md` §6.2 row 4 line 241
  (`reconstructed_rating` spec-favoured framing). The 5-family post-omit
  set is L238-240 + L242-243.
- PR #247 (Q6F) §11 verbatim per-candidate metric table and §12 decision
  rule. CI overlap between Glicko-2 [0.6216, 0.6302] and TrueSkill
  [0.6246, 0.6342] is the structural cause of `narrow_with_evidence`.
- PR #247 (Q6F) module `_run_glicko2_survey` — Branch (i) materialization
  re-uses this engine verbatim.
- PR #249 (Q6G) §13a equivalence proof (Spearman ρ = 0.2292 < 0.99;
  |Δ log-loss| = 0.07928 > SE = 0.00219; both bounds FAILED).
- PR #249 §13b byte-determinism proof (PASS).
- PR #249 §15 limitations: `rating_period_days = 30` long vs median toon
  span 0.88 d.
- PR #245 Q6_selected_policy row's notes (the framing under which the
  entire algorithm-survey-then-implementation-proof chain ran).

### External (CITATION-ONLY; inherited from PR #247 / PR #249)

- **Glickman (2012)** — "Example of the Glicko-2 system" (Boston
  University technical note). Authoritative source for §3 rating-period
  batching and §10 worked example. Q6H does NOT re-implement Glicko-2.
- **Glickman (1999)** — Original Glicko reliability-deviation
  formulation.
- **Efron & Tibshirani (1993)** — Percentile bootstrap method
  (NIT-N6 from PR #248). Q6H does NOT re-bootstrap.
- **Higham (2002)** — Kahan / Neumaier compensated summation. Q6H does
  NOT re-sum.

### When WebFetch is permitted

- For Glickman 2012 §3 batched-update equations IF the Layer-2 executor
  needs to verify a paraphrase before quoting in MD §15. NOT for new
  metric computations.

## Execution Steps

The future Layer-2 execution PR runs T01–T08 in order under the
`data-analysis-lineage.md` non-batching rule.

### T01 — Proof module shell (constants + dataclasses + 38-column schema)

**Objective:** Stand up the Q6H decision module with constants, dataclasses,
and the 38-column schema. No engine logic; no I/O.

**Instructions:**

1. Create `src/rts_predict/games/sc2/datasets/sc2egset/decide_history_rating_path.py`
   mirroring PR #249's module structure.
2. Define `Q6H_DECISION_ROWS: tuple[str, ...]` with the 5 canonical row
   labels per A11.
3. Define `Q6H_PARENT_SHAS: dict[str, str]` with the 10 parent SHA pins
   per A1.
4. Define `Q6H_PATH_DECISION_RULE: str` (the binding constant; see
   §"Decision rule" below; embed verbatim).
5. Define `Q6H_FIVE_FAMILY_POST_OMIT_SET: tuple[str, ...]` with exactly 5
   names per A8.
6. Define `THESIS_PRAGMATISM_ADMISSIBILITY_MIN_SENTENCES: int = 6` and
   `THESIS_PRAGMATISM_ADMISSIBILITY_MIN_CROSS_REFERENCES: int = 3` per
   A9(a).
7. Define `Q6H_DECISION_SCHEMA: tuple[str, ...]` with **EXACTLY 38** column
   names per A10. The schema is:
   1. `decision_id`
   2. `parent_decision_id`
   3. `decision_name`
   4. `included_in_decision`
   5. `inclusion_or_rejection_reason`
   6. `rating_path_kind`
   7. `verdict`
   8. `binding_level`
   9. `decision_path`
   10. `selected_policy`
   11. `rating_policy_status`
   12. `event_by_event_policy`
   13. `batched_policy_status`
   14. `omit_reconstructed_rating_policy`
   15. `other_five_families_materialization_permission`
   16. `future_materialization_permission`
   17. `future_column_names`
   18. `excluded_column_names`
   19. `q5_cross_region_policy`
   20. `q6_status` (R2.N3; e.g., `discharged_by_omission_under_thesis_pragmatism`)
   21. `thesis_pragmatism_flag_value` (R2.2; ∈ {`TRUE`, `FALSE`, `null`})
   22. `thesis_pragmatism_substantive_paragraph_sentence_count` (R2.2; ≥ 6 iff row 3 emitted)
   23. `branch_evaluated` (R2.5; ∈ {`(i)`, `(ii)`, `(iii)`, `(iv)`, `(v)`})
   24. `forward_only_constraints`
   25. `leakage_guard`
   26. `deployability_rationale`
   27. `thesis_pragmatism_rationale`
   28. `evidence_paths`
   29. `falsifiers`
   30. `audit_pr`
   31. `parent_pr242_csv_sha256`
   32. `parent_pr243_csv_sha256`
   33. `parent_pr245_md_sha256`
   34. `parent_pr247_csv_sha256`
   35. `parent_pr247_md_sha256`
   36. `parent_pr249_csv_sha256`
   37. `notes` (free-form prose; R2.3 split)
   38. `materialized_output_paths` (empty on every row; A13; R2.3 split)
8. Define dataclass `RatingPathDecision` with **exactly 38 fields**
   matching `Q6H_DECISION_SCHEMA`.
9. Define dataclass `RatingPathDecisionResult` (top-level container;
   mirrors PR #249's `RatingImplementationProofResult`).
10. Define `FALSIFIER_PRIORITY_CHAIN: tuple[str, ...]` with ≥ 37 keys per
    §"Falsifier chain".
11. Module-load asserts: `assert len(Q6H_DECISION_SCHEMA) == 38`;
    `assert len(fields(RatingPathDecision)) == 38`;
    `assert len(Q6H_DECISION_ROWS) == 5`;
    `assert len(Q6H_PARENT_SHAS) == 10`;
    `assert len(Q6H_FIVE_FAMILY_POST_OMIT_SET) == 5`;
    `assert "reconstructed_rating" not in Q6H_FIVE_FAMILY_POST_OMIT_SET`.

**Verification:**

- `source .venv/bin/activate && poetry run python -c "import rts_predict.games.sc2.datasets.sc2egset.decide_history_rating_path"` returns 0.
- Module-load asserts pass.

**File scope:** `src/rts_predict/games/sc2/datasets/sc2egset/decide_history_rating_path.py`

**Routing:** Sonnet sufficient (mechanical scaffolding).

### T02 — Parent SHA verification + decision-row builder

**Objective:** Build the 5-row decision set by reading the 10 parent SHAs
from the master file system and asserting they match `Q6H_PARENT_SHAS`.

**Instructions:**

1. Define `_check_parent_pr_shas(repo_root: Path) -> list[tuple[str, str]]`
   mirroring PR #249's helper. Halt on first mismatch.
2. Define `_build_decision_row_a_bind_event_by_event_glicko2(...) -> RatingPathDecision`
   and analogous builders for rows B, C, D, and the emergent verdict row.
3. Each builder returns a dataclass instance with the row-specific cells
   populated; non-applicable cells = `"not_applicable_carry_forward"`.

**Verification:** parent SHAs verified for all 5 PR pairs; mismatch fires
the matching falsifier.

**File scope:** extends T01.

**Routing:** Sonnet sufficient.

### T03 — Decision rule enforcement + bind-now / pragmatism guards

**Objective:** Implement the deterministic decision rule (§"Decision rule")
including the order-of-operations guard (A12) and the `THESIS_PRAGMATISM`
override falsifier (A9(c)).

**Instructions:**

1. Define `_apply_q6h_decision_rule(executor_inputs: dict) -> tuple[str, str, str, str]`
   returning `(selected_policy, verdict, materialization_permission, rationale)`.
2. Walk the branches in order (i) → (v); take the first branch whose
   preconditions are met.
3. Implement the `THESIS_PRAGMATISM` admissibility guard: if Branch (iii)
   is emitted, verify the MD §15 sentence count ≥ 6 and cross-reference
   count ≥ 3 via a writer-time grep helper.
4. Implement the override falsifier: if Branch (iii) emitted without the
   §15 substantive paragraph, raise `RatingPathDecisionError` with
   `falsifier_key = "q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15"`.

**Verification:** parametric tests cover all 5 branches; the bind-now guard
test parallels PR #249's `TestBlockerGuard_BindNowRequiresEquivalence`.

**File scope:** extends T01–T02.

**Routing:** Opus REQUIRED. Substantive reasoning: (a) the
order-of-operations is the methodological backbone of the decision; (b)
the THESIS_PRAGMATISM override falsifier is the binding admissibility
mechanism; (c) the §15 sentence-count + cross-reference helper is
subtle (must NOT count code blocks or quoted PR #249 text as
substantive sentences).

### T04 — CSV + MD writer (NIT-N1-style probability-only sample inherited)

**Objective:** Write byte-deterministic 38-column CSV + ≥ 19-section MD.

**Instructions:**

1. Define `write_q6h_decision_artifacts(result: RatingPathDecisionResult, csv_path: Path, md_path: Path) -> None`.
2. CSV writer: byte-deterministic (sort decisions by `decision_id`;
   `lineterminator="\n"`; `quoting=csv.QUOTE_MINIMAL`; dialect mirrors
   PR #249).
3. MD writer: ≥ 19 sections mirroring PR #249's structure; explicit §15
   "Thesis-pragmatism rationale" + §16 "PR #247 docstring verbatim
   quotation" sections.
4. §15 grep-check at writer time: sentence count ≥ 6 (count via
   `re.split(r"(?<=[.!?])\s+", §15_content)`); cross-reference count ≥ 3
   (count via `re.findall(r"PR #249 §\d+", §15_content)`). Failure raises
   the override falsifier.
5. §16 verbatim quotation of PR #247 docstring lines 15–17, preserving
   double-backticks and the verbatim token
   `omit_reconstructed_rating_and_unblock_other_five`.

**Verification:**

- Byte-stability: run writer twice; assert outputs hash-identical.
- CSV column count == 38; CSV row count == 6 (1 header + 5 decisions).
- MD section count ≥ 19; §15 sentence ≥ 6; §15 cross-reference ≥ 3;
  §16 verbatim quote present.

**File scope:** extends T01–T03.

**Routing:** Sonnet sufficient (mechanical writer).

### T05 — Sandbox jupytext notebook pair

**Objective:** Author the jupytext-paired sandbox notebook.

**Instructions:**

1. Create `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.{py,ipynb}`.
2. No `def` / `class` / `lambda` in cells.
3. All logic imported from the decision module.
4. Outputs cleared before commit.
5. Cells exercise: (a) module import + constants; (b) parent SHA
   verification; (c) decision-row builders (rows 1–4); (d) emergent
   verdict (row 5); (e) artifact writer invocation.

**Verification:** `poetry run jupytext --execute sandbox/.../...py` exits 0.

**File scope:** sandbox pair.

**Routing:** Sonnet sufficient.

### T06 — Mirrored test file (≥ 250 tests; ≥ 95% branch coverage)

**Objective:** Implement the mirrored test suite covering every constant,
every decision row, the order-of-operations guard, the §15 admissibility
check, every falsifier — including the BLOCKER-1-style bind-now guard.

**Instructions:**

1. Create `tests/rts_predict/games/sc2/datasets/sc2egset/test_decide_history_rating_path.py`.
2. Test classes (mirror PR #249 structure):
   - `TestModuleConstants` — schema length == 38; row count == 5; 10
     parent SHAs.
   - `TestParentSHAs` — 10 SHAs verified; mismatch raises with correct
     falsifier key.
   - `TestDecisionRowBuilders` — each of 5 builders emits valid rows.
   - `TestDecisionRule_AllFiveBranches` — synthesise inputs covering
     branches (i) through (v); assert outcomes per A12.
   - `TestThesisPragmatismAdmissibility` — §15 sentence-count + cross-ref
     checks (R2.2 / R2.4).
   - `TestBlockerGuard_BranchIIIRequiresSubstantiveParagraph` —
     PR #249-style guard.
   - `TestArtifactWriter` — byte-stability; CSV column count == 38;
     MD section count ≥ 19.
   - `TestFalsifierChain` — for each key in `FALSIFIER_PRIORITY_CHAIN`
     (≥ 37 keys), construct a failing fixture and assert helper raises.
   - `TestNoMaterializationCreep` — `materialized_output_paths` empty on
     every row; no `.parquet` written under `tmp_path`.
   - `TestNo5FamilyDrift` — A8 5-family set excludes
     `reconstructed_rating`.
3. ≥ 250 tests; ≥ 95% branch coverage.

**Verification:** `poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_decide_history_rating_path.py -v --cov=rts_predict.games.sc2.datasets.sc2egset.decide_history_rating_path --cov-branch` passes.

**File scope:** `tests/rts_predict/games/sc2/datasets/sc2egset/test_decide_history_rating_path.py`.

**Routing:** Sonnet sufficient.

### T07 — Release tail

**Objective:** Bump version, append CHANGELOG, archive PR #249 and update
active line in `planning/INDEX.md`.

**Instructions:**

1. `pyproject.toml`: version `3.77.0 → 3.78.0`.
2. `CHANGELOG.md`: new `## [3.78.0] - YYYY-MM-DD (PR #N: feat/sc2egset-02-01-03-q6h-rating-path-decision)` block.
3. `planning/INDEX.md`: archive PR #249 at merge SHA `d9276194`; new
   Active entry for the Q6H PR.

**Verification:** pre-commit hooks pass; `git status` shows only expected
files.

**File scope:** `pyproject.toml`, `CHANGELOG.md`, `planning/INDEX.md`.

**Routing:** Sonnet sufficient.

### T08 — Draft PR + final adversarial gate

**Objective:** Create draft PR, run validation, dispatch reviewer-adversarial
final gate, mark ready if APPROVE.

**Instructions:**

1. Create draft PR with `PR #<TBD>` placeholders.
2. Normalize placeholders to assigned PR number in 9 files + PR body.
3. Run targeted test suite + full project suite + ruff + mypy + jupytext
   sync.
4. Dispatch `@reviewer-adversarial` (fresh 3-round cap per `feedback_adversarial_cap_execution.md`).
5. If APPROVE / APPROVE-WITH-NITS with zero blockers, `gh pr ready <N>`.
6. Do NOT merge.

## File Manifest

### This Layer-1 planning PR (EXACTLY 2 files)

| File | Action |
|------|--------|
| `planning/current_plan.md` | Create (this Round 2 amendment + R2.6 mechanical fix) |
| `planning/current_plan.critique.md` | Create (reviewer-adversarial Round 1 + Round 2 record) |

### Future Layer-2 execution PR (9 files; NOT created in this PR)

The Layer-2 PR is a SEPARATE dispatch on the same branch. Its 9-file
manifest is enumerated here for forward visibility ONLY.

| # | File | Action |
|---|------|--------|
| 1 | `src/rts_predict/games/sc2/datasets/sc2egset/decide_history_rating_path.py` | Create |
| 2 | `tests/rts_predict/games/sc2/datasets/sc2egset/test_decide_history_rating_path.py` | Create |
| 3 | `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.py` | Create |
| 4 | `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.ipynb` | Create |
| 5 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.csv` | Create (38 cols × 5 rows + 1 header) |
| 6 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.md` | Create (≥ 19 sections including §15 + §16) |
| 7 | `planning/INDEX.md` | Update (archive PR #249; set Q6H active) |
| 8 | `CHANGELOG.md` | Update (new `[3.78.0]` block) |
| 9 | `pyproject.toml` | Update (`3.77.0 → 3.78.0`) |

### Forbidden in this Layer-1 PR

Zero diff required for:

- Any `.py` module / test / notebook.
- Any artifact CSV / MD / Parquet / JSON.
- `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`.
- Dataset and root `research_log.md`.
- `ROADMAP.md`.
- `reports/specs/**`, `data/db/schemas/views/**`.
- `CHANGELOG.md`, `pyproject.toml`, `planning/INDEX.md` (this Layer-1 PR
  is planning-only; release tail is reserved for the Layer-2 PR).
- `reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}`.
- `*.parquet`.
- `thesis/**`, `docs/**`, `.claude/**`, `data/**`, `src/rts_predict/games/aoe2/**`.

## Decision rule (deterministic order-of-operations; A12; R2.5 resolution)

Define `Q6H_PATH_DECISION_RULE` as a BINDING multi-line string constant
embedded verbatim in the future Q6H module and quoted verbatim in the
future MD §"Decision rule".

**Methodological justification for evidentiary-first order:** evidentiary
obligations are evaluated **before** pragmatic gates. The thesis pipeline
prefers a substantively justified verdict (bind via fresh evidence, then
conservative recommendation) over a pragmatic omission. `THESIS_PRAGMATISM`
is a last-resort gate that may close the family **only when no evidentiary
branch is reachable**; evaluating it first would allow a boolean to
short-circuit substantive adjudication, violating Invariant I7 (no magic
gates).

```
Q6H FINAL RATING-PATH DECISION RULE (BINDING; A12; R2.5)
========================================================

Let parent_pr249_verdict      = PR #249 Row 5 selected_policy
                                = "recommendation_only_glicko2" (verified).
Let parent_pr249_equivalence  = PR #249 Row 3 equivalence_proof_statistics
                                (passes_spearman_bound = false;
                                 passes_delta_log_loss_bound = false).
Let parent_pr249_determinism  = PR #249 Row 4 byte_determinism_proof
                                (hashes_equal = true).
Let new_separating_anchor     = (Layer-2 executor input; default empty).
Let thesis_pragmatism         = bool per A9(b) canonical default-derivation.
Let substantive_paragraph_ok  = (MD §15 sentence count >= 6 AND
                                 cross-reference count >= 3).
Let reviewer_signoff          = (Layer-2 reviewer-adversarial sign-off
                                 on the §15 paragraph; default FALSE).

Branches are evaluated in order (i) -> (v); first satisfied branch wins.

BRANCH (i) -- bind_event_by_event_glicko2:
    IF new_separating_anchor produces non-overlapping bootstrap CI
       between Glicko-2 and TrueSkill on a pre-registered anchor
       (Brier / ECE / calibration-slope) AND the anchor was named in
       this Layer-1 plan:
           selected_policy = 'bind_event_by_event_glicko2'
           verdict = 'bind_event_by_event_glicko2'
           future_materialization_permission =
               'permitted_for_all_6_history_enriched_families_with_'
               'event_by_event_glicko2_engine_imported_from_pr247_'
               'subject_to_q5_binding_and_cross_02_01_post_audit'
           rationale = ('Event-by-event Glicko-2 is the deployment-
                         style variant (PR #247 docstring lines 15-17).
                         Batched form ruled out by PR #249 §13a.
                         New separating anchor: {anchor_name}.')
    ELSE fall through.

BRANCH (ii) -- recommendation_only_event_by_event_glicko2:
    IF parent_pr249_verdict == 'recommendation_only_glicko2'
       (no determinism regression; no falsifier trigger from PR #249
        re-load):
           selected_policy = 'recommendation_only_event_by_event_glicko2'
           verdict = 'recommendation_only_event_by_event_glicko2'
           materialization_permission =
               'recommendation_only_blocked_pending_phase_03_or_later_decision'
           named_next_proof = (Layer-2 executor picks one or more from:
               'online_update_determinism_over_third_run',
               'cold_start_gate_G_CS_4_sensitivity_sweep',
               'toon_id_region_scoped_identifier_policy_proof',
               '1_96_se_log_loss_ci_gap_to_rolling_baseline')
    ELSE fall through.

BRANCH (iii) -- omit_reconstructed_rating_and_unblock_other_five:
    IF branches (i) and (ii) are both blocked
       AND thesis_pragmatism == TRUE
       AND substantive_paragraph_ok == TRUE
       AND reviewer_signoff == TRUE:
           selected_policy = 'omit_reconstructed_rating_and_unblock_other_five'
           verdict = 'omit_reconstructed_rating_and_unblock_other_five'
           other_five_families_materialization_permission =
               'permitted_for_5_history_enriched_families_'
               'without_reconstructed_rating_'
               'subject_to_q5_binding_and_cross_02_01_post_audit'
           excluded_column_names = ['reconstructed_rating_focal_pre',
                                    'reconstructed_rating_opp_pre',
                                    'reconstructed_rating_diff']
           future_column_names = focal_player_history.*,
                                 opponent_player_history.*,
                                 matchup_history_aggregate.*,
                                 in_game_history_aggregate.*,
                                 cross_region_fragmentation_handling.is_cross_region
           q6_status = 'discharged_by_omission_under_thesis_pragmatism'
           rationale = (>= 6 sentences in MD §15 with >= 3 PR #249
                        cross-references; cites #247 -> #249 -> Q6H
                        regression explicitly per Round 1 N1.)
    ELSE fall through.

BRANCH (iv) -- defer_to_layer_3_phase_02_internal_decision:
    IF branches (i)-(iii) all blocked AND no fresh blocking finding:
           selected_policy = 'defer_to_layer_3_phase_02_internal_decision'
           verdict = 'defer_to_layer_3_phase_02_internal_decision'
           materialization_permission =
               'deferred_to_layer_3_phase_02_internal_step'
    ELSE fall through.

BRANCH (v) -- deferred_blocker:
    ELSE:
           selected_policy = 'deferred_blocker'
           verdict = 'deferred_blocker'
           materialization_permission = 'blocked_pending_named_reason'
           named_missing_evidence = >= 2 enumerated items.

NOTE: The canonical default-derivation (A9(b)) sets THESIS_PRAGMATISM
appropriately and Branch (ii) is the default reachable verdict from
PR #249 evidence (recommendation_only_event_by_event_glicko2). Branch
(iii) is reached ONLY if the Layer-2 executor explicitly records
substantive reasoning + obtains reviewer-adversarial sign-off. The
override decision is OUT OF SCOPE for this Layer-1 planner.
```

## Falsifier chain (≥ 37 keys; R2.4 resolution; 4 groups)

**Group 1 — Identity / parent-SHA / base-ref discipline (9 keys):**

```
q6h_base_ref_not_d9276194
q6h_parent_sha_pin_count_equals_10
parent_pr242_csv_sha256_mismatch
parent_pr242_md_sha256_mismatch
parent_pr243_csv_sha256_mismatch
parent_pr243_md_sha256_mismatch
parent_pr247_csv_sha256_mismatch
parent_pr247_md_sha256_mismatch
parent_pr249_csv_sha256_mismatch
parent_pr249_md_sha256_mismatch
```

(SHA pins #245 CSV/MD are tracked implicitly under `q6h_parent_sha_pin_count_equals_10`;
the 9 keys above plus the count-equality check cover all 10 pins. 9 keys + 1 count check = 10
distinct provenance assertions.)

**Group 2 — Decision-set / 5-family integrity (10 keys):**

```
q6h_decision_count_mismatch
q6h_decision_id_order_mismatch
q6h_q6h_selected_policy_row_missing
q6h_q5_re_adjudication_drift
q6h_q6f_re_adjudication_drift
q6h_q6g_re_adjudication_drift
q6h_omit_emitted_without_excluded_columns_listed
q6h_omit_emitted_without_five_families_listed
q6h_reconstructed_rating_appears_in_future_column_names_if_omit
q6h_reconstructed_rating_missing_from_excluded_columns_if_omit
```

**Group 3 — Decision-rule order-of-operations integrity (8 keys):**

```
q6h_decision_rule_order_not_evidentiary_first
q6h_bind_emitted_without_separating_anchor
q6h_recommendation_emitted_without_pr_249_evidence_stand
q6h_omit_emitted_without_branches_i_and_ii_blocked
q6h_omit_emitted_with_thesis_pragmatism_false
q6h_defer_layer_3_emitted_without_branches_i_ii_iii_blocked
q6h_deferred_blocker_emitted_without_blocking_artifact_citation
q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15
```

**Group 4 — Non-recurrence / non-creep boundary (10 keys):**

```
q6h_no_status_yaml_mutation
q6h_no_research_log_mutation
q6h_no_roadmap_mutation
q6h_no_spec_mutation
q6h_no_phase_03_touch
q6h_no_step_02_01_04_touch
q6h_no_trueskill_re_implementation
q6h_no_batched_glicko2_re_implementation
q6h_event_by_event_engine_not_imported_from_pr247
q6h_parquet_emitted
q6h_silent_q6_closure_on_omit_branch
q6h_materialization_creep
```

Total: 10 + 10 + 8 + 12 = **40** keys (≥ 37 minimum per A10; absorbs R2.4
additions `q6h_parquet_emitted` and `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15`).

Each falsifier appears (a) as a module-level constant in
`FALSIFIER_PRIORITY_CHAIN`, (b) in MD §"Falsifier roll-call" with
`:did_not_fire` annotation on the canonical run, (c) in at least one test
in T06 asserting the canonical run does not trigger it.

## Gate Condition

The Layer-2 PR (future) is complete only when ALL of the following hold.
These are the conditions the Layer-2 reviewer-adversarial verifies.

**(a) Artifact integrity:**

- a1. `02_01_03_q6h_rating_path_decision.csv` has exactly 38 columns
  (A10 / R2.3) and exactly 5 data rows + 1 header.
- a2. `02_01_03_q6h_rating_path_decision.md` has ≥ 19 `## ` sections
  including §15 ("Thesis-pragmatism rationale") and §16 ("PR #247
  docstring verbatim quotation").
- a3. CSV byte-stability: re-running the writer produces a bit-identical
  CSV.

**(b) Methodology integrity:**

- b1. Decision rule order-of-operations matches §"Decision rule" exactly;
  `decision_rule_order_hash` (the SHA-256 of `Q6H_PATH_DECISION_RULE`)
  matches the pinned Layer-1 SHA.
- b2. Q5, Q6F, Q6G are NOT re-adjudicated (Group 2 falsifiers do not fire).
- b3. If Row 5's verdict is `omit_reconstructed_rating_and_unblock_other_five`,
  Branch (iii) preconditions hold: branches (i) and (ii) blocked;
  `thesis_pragmatism_flag_value = TRUE`; §15 sentence count ≥ 6; §15
  cross-reference count ≥ 3; reviewer-adversarial sign-off recorded.
- b4. Falsifier `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15`
  does NOT fire.
- b5. PR #247 docstring lines 15–17 are verbatim-quoted in MD §16 with
  preserved double-backticks and the token
  `omit_reconstructed_rating_and_unblock_other_five`.

**(c) Schema integrity:**

- c1. CSV column count == 38 in all 4 of: module assertion, CSV header,
  MD §11 statement, `TestModuleConstants::test_schema_count_equals_38`.

**(d) Test integrity:**

- d1. `pytest tests/.../test_decide_history_rating_path.py -v` ≥ 250
  tests, all passing.
- d2. Branch coverage on `decide_history_rating_path` ≥ 95%.
- d3. `TestBlockerGuard_BranchIIIRequiresSubstantiveParagraph` passes
  (verifies R2.2 admissibility enforcement).
- d4. `TestNo5FamilyDrift` passes (A8 5-family set excludes
  `reconstructed_rating`).

**(e) Provenance integrity:**

- e1. All 10 parent SHAs match the pinned A1 constants.
- e2. CHANGELOG and `pyproject.toml` reflect `3.77.0 → 3.78.0`.
- e3. `planning/INDEX.md` archives PR #249 and registers the new Q6H
  active entry.

**(f) Non-batching / non-creep integrity:**

- f1. No `.parquet` written; no STEP_STATUS / PIPELINE_SECTION_STATUS /
  PHASE_STATUS mutation; no research_log entry; no ROADMAP edit; no
  spec edit; no leakage_audit file.
- f2. No TrueSkill or batched-Glicko-2 re-implementation in the Q6H
  module (Group 4 falsifiers).

## Open Questions

- **OQ1 — Final Q6H selected_policy.** Per the canonical default-derivation
  path (A9(b)), the auto-derived default is Branch (ii)
  `recommendation_only_event_by_event_glicko2` (PR #249 evidence stands;
  no new separating anchor authorized). Branch (iii)
  `omit_reconstructed_rating_and_unblock_other_five` is reachable ONLY
  if branches (i) and (ii) are explicitly blocked AND
  `THESIS_PRAGMATISM = TRUE` AND substantive paragraph + sign-off pass.
  Resolves: Layer-2 executor + Layer-2 reviewer-adversarial.
- **OQ2 — Whether the Layer-2 executor produces a new separating anchor**
  (Brier / ECE / calibration-slope) that would activate Branch (i).
  Default expectation: NO (no anchor authorized in this Layer-1 plan).
  Resolves: Layer-2 executor at T03.
- **OQ3 — Whether the §15 substantive paragraph qualifies under the R2.2
  three-pin admissibility.** Resolves: Layer-2 reviewer-adversarial.
- **OQ4 — Whether the Layer-3 materialization PR follows Q6H immediately
  or after a hygiene checkpoint.** Recommendation: brief hygiene checkpoint
  (full test suite, ruff, mypy on master after Q6H merge; verify
  falsifiers fire correctly).
- **OQ5 — Whether the Q6H decision module exports `Q6H_PATH_DECISION_RULE`
  as an importable constant consumed by the future Layer-3 module.**
  Recommendation: yes (mirrors how PR #247's `_run_glicko2_survey` is
  consumed by PR #249).
- **OQ6 — Whether an additional falsifier guards silent equivalence-
  criterion mutation across Q6G → Q6H.** Recommendation: out of scope
  for Q6H (PR #249 enforces it on its own module).

## Out of scope

- Phase 03 baselines / `create_temporal_split()` / cold-start gate G-CS-6.
- Layer-3 materialization (separate PR).
- Re-adjudication of Q1–Q5, Q6, Q6F, Q6G.
- New batched-Glicko-2 sensitivity arm or `{7, 30, 90}` rating-period
  sweep.
- TrueSkill re-implementation.
- BTL / Aligulac / Bradley-Terry / Neural-BTL re-consideration.
- Raw MMR hybrid re-consideration.
- New algorithm survey.
- Worldwide-identity migration.
- AoE2.
- Step 02_01_03 closure.
- CROSS-02-01 audit file.
- Any `.parquet` output.
- Spec edits.

## Adversarial-Review Adjustments

### Round 1 (HOLD; resolved below)

Round 1 reviewer-adversarial returned **HOLD** with 3 blockers (R2.1
5-family line-range; R2.2 `THESIS_PRAGMATISM` admissibility; R2.3 schema
column count) + 2 warnings (R2.4 invited falsifier additions; R2.5
decision-rule order-of-operations) + 3 notes (N1 §15 regression-reconciliation
sentence; N2 verbatim PR #247 docstring citation; N3 optional `q6_status`
token).

### Round 2 amendment

This Round 2 amendment resolves every Round 1 blocker, warning, and
note. Traceability:

| Round 1 ref | Resolution location in this plan | Pinning mechanism |
|-------------|----------------------------------|-------------------|
| **R2.1** (5-family / §6.2 line-range citation defect) | §Scope, A8, T01 step 5, §"Decision rule" Branch (iii), Schema columns 14–18, Gate (d4), Falsifier Group 2 keys 7–10 | Verbatim "§6.2 minus L241 reconstructed_rating; remaining set L238 + L239 + L240 + L242 + L243"; falsifier `q6h_reconstructed_rating_missing_from_excluded_columns_if_omit`. |
| **R2.2** (`THESIS_PRAGMATISM` admissibility / Invariant I9) | A9 (three pins (a)/(b)/(c)); §"Decision rule" Branch (iii); Schema columns 21–22; Group 3 falsifier; Gate (b3), (b4) | Three-pin: (a) admissibility criterion ≥ 6 sentences + ≥ 3 cross-references + reviewer-adversarial sign-off; (b) canonical default-derivation path; (c) override falsifier `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15`. |
| **R2.3** (Schema column count = 38) | A10, T01 step 7 (38-column schema enumerated), Gate (c1), Falsifier `q6h_schema_column_count_equals_38` (Group 4 implicit via module assert) | 4-place pin: module assertion, CSV header, MD §11 statement, `TestModuleConstants::test_schema_count_equals_38`. Column 38 `materialized_output_paths` split from column 37 `notes`. |
| **R2.4** (Invited falsifier additions) | Falsifier Group 3 (8th key) + Group 4 (10th key); chain count moves from ≥ 35 to ≥ 37 (actual: 40 keys) | `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15` (Group 3); `q6h_parquet_emitted` (Group 4). |
| **R2.5** (Decision-rule order-of-operations) | §"Decision rule" — explicit (i)→(v) ordering with methodological-justification paragraph; A12; Falsifier `q6h_decision_rule_order_not_evidentiary_first`; `decision_rule_order_hash` cell | Evidentiary branches (i) bind + (ii) recommendation evaluated **before** pragmatism branch (iii). Justified in §"Decision rule" preamble paragraph. |
| **N1** (§15 paragraph reconciling #247 → #249 → Q6H regression) | T04 step 4; T06 `TestThesisPragmatismAdmissibility`; Gate (b3) | §15 must include ≥ 6 sentences AND ≥ 3 explicit `PR #249 §X.Y` cross-references AND a sentence reconciling the #247 → #249 → Q6H sequence regression. |
| **N2** (Verbatim PR #247 docstring quotation) | T04 step 5; Gate (b5) | §16 verbatim-quotes PR #247 docstring lines 15–17 preserving double-backticks and the token `omit_reconstructed_rating_and_unblock_other_five`. |
| **N3** (Optional `q6_status` field token) | T01 step 7 (schema column 20); A8 / decision rule Branch (iii); falsifier `q6h_silent_q6_closure_on_omit_branch` | `q6_status = "discharged_by_omission_under_thesis_pragmatism"` for Branch (iii) emission. |

### Round-2-mechanical-fix (R2.6 — applied by parent without consuming Round 3)

**R2.6 — §"Problem Statement" Q6G metric inversion.** The Round 2
amendment as initially produced by planner-science misreported Q6G's
equivalence outcome as PASSED (Spearman ρ = 0.9931; |Δ log-loss| = 0.0028).
PR #249 master artifact actually has FAILED both bounds (Spearman ρ =
0.2292; |Δ log-loss| = 0.07928; passes_*_bound = false on both). The
verdict `recommendation_only_glicko2` was the NIT-N2 default expected
outcome under the auto-derived rule when equivalence FAILS and
byte-determinism PASSES — not the consequence of a passed equivalence
without a separating anchor.

Reviewer-adversarial Round 2 verdict was **HOLD-WITH-MECHANICAL-FIX**:
the textual error was the only Round 2 blocker (R2.6); the decision
rule, falsifier set, schema, and gate clauses were all derived from the
actual FAILED outcome and are therefore correct as written. The reviewer
authorised the parent to execute the textual correction directly without
dispatching planner-science Round 3 (the 3-round cap accounts only for
substantive methodology rounds; mechanical text correction does not
consume a round).

The §"Problem Statement" above has been corrected in this Round 2
amendment to reflect the actual PR #249 FAILED outcome with full citation
of the Row 3 / Row 5 evidence. No other plan-section content required
revision under R2.6.

### Critique instruction (per planner output contract)

For Category A: adversarial critique is required before execution begins.
Reviewer-adversarial Round 1 (HOLD with 3 blockers + 2 warnings + 3 notes)
+ Round 2 (HOLD-WITH-MECHANICAL-FIX on R2.6) are both consumed. After
this Round-2-mechanical-fix amendment is committed and the Layer-1 PR
merges, the Layer-2 execution PR receives a fresh 3-round adversarial
cap.

---

**End of Round 2 amended + mechanically-fixed plan. All Round 1 + Round 2
findings incorporated as binding methodology with explicit traceability.**
