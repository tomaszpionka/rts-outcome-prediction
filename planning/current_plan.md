---
plan_role: planner-science (Round 2)
plan_model: claude-opus-4-7[1m]
plan_round: 2
round_1_verdict: APPROVE-WITH-NITS
round_1_nits_count: 4
round_1_nits_resolved_in_round_2: [NIT-1, NIT-2, NIT-3, NIT-4]
schema_column_count: 45
plan_date: 2026-05-27
plan_layer: 1
chosen_outcome: A
category: A
branch: feat/sc2egset-02-01-99-rating-omit-closure-artifact
base_ref: a9cf552f346d8402fa4856fbee51fa34b0b0cefe
date: 2026-05-27
planner_model: claude-opus-4-7[1m]
dataset: sc2egset
phase: "02"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
step: "02_01_99 (Layer-1 plan for omit-closure decision artifact execution; Round 2 baking in all 4 Round-1 nits)"
non_batching_sequence_position: "Step 1 of 9 for the omit-closure ARTIFACT lineage segment within Step 02_01_99 (ROADMAP stub itself was already merged as PR #253; this Layer-1 PR plans the future Layer-2 artifact execution PR — a metadata-only adjudication artifact analogous to Q-chain PR #250 (Layer-1 plan) → PR #251 (Layer-2 artifact)). The future Layer-2 PR consolidates non-batching steps 2-7 into one execution because the decision is metadata-only: no DuckDB read, no feature column, no Parquet, no audit — only a CSV/MD pair recording the elevation."
critique_required: true
critique_required_before_execution: true
critique_reviewer: reviewer-adversarial
gate_reviewer: "reviewer-adversarial (Category A pre-execution gate)"
adversarial_round_cap: "3 rounds total (planning-side) per feedback_adversarial_cap_execution.md."
adversarial_cap_symmetry: "Same 3-round cap applies to execution-side review per feedback_adversarial_cap_execution.md."
parent_planning_pr: "PR #252 (02_01_99 ROADMAP-stub Layer-1; merged at master 703747f2)"
parent_execution_pr: "PR #253 (02_01_99 ROADMAP-stub Layer-2; merged at master a9cf552f)"
planning_pr: "PR #<TBD-this-Layer-1>"
planning_pr_version_bump: "none (Layer-1 planning-only; 2 files)"
planning_pr_scope: "Layer-1 (2 files only) — planning/current_plan.md + planning/current_plan.critique.md. NO ROADMAP edit, NO pyproject bump, NO CHANGELOG entry, NO planning/INDEX.md archive, NO status YAML flip, NO research_log entry, NO artifact, NO source/test/notebook touch, NO Q6H artifact mutation, NO Step 02_01_03 6-family declaration mutation."
future_layer2_pr: "PR #<TBD-Layer-2-artifact>"
future_layer2_version_bump: "3.79.0 → 3.80.0 (minor; feat-family per .claude/rules/git-workflow.md; precedent: PR #251 Q6H Layer-2 bumped 3.77.0 → 3.78.0)"
future_layer2_file_count: 9
future_layer2_pr_scope: "Layer-2 artifact-execution (9 files) — close_history_rating_omit_path.py + test_close_history_rating_omit_path.py + jupytext .py/.ipynb pair + omit-closure CSV + omit-closure MD + planning/INDEX.md (archive Layer-1, promote Layer-2) + CHANGELOG.md (new [3.80.0]) + pyproject.toml (3.79.0 → 3.80.0). NO Parquet, NO CROSS-02-01 audit, NO STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS flip, NO research_log entry (per Q-chain precedent #242/#243/#245/#247/#249/#251), NO ROADMAP edit (PR #253 stub is sufficient), NO Step 02_01_03 6-family declaration mutation, NO 5-family ROADMAP narrowing (separate downstream PR), NO feature materialization."
phase_status_at_plan_time: "Phase 02 in_progress (Pipeline Section 02_01 derived-complete because 02_01_01 + 02_01_02 are the only two STEP_STATUS entries; STEP_STATUS does not yet include 02_01_03 or 02_01_99); Phase 03 not_started"
step_status_at_plan_time: "02_01_01 complete; 02_01_02 complete; 02_01_03 NOT in STEP_STATUS (ROADMAP-only declared since PR #239; no closure entry); 02_01_99 NOT in STEP_STATUS (ROADMAP-only declared by PR #253; no closure entry). The artifact-execution PR planned here does NOT flip either step to a status; closure is a separate downstream PR."
non_batching_compliance: "Strictly compliant with .claude/rules/data-analysis-lineage.md §Non-batching rule. The Step 02_01_99 ROADMAP stub (sequence step 1) was completed by PR #253. This Layer-1 PR begins a NEW non-batching sequence for the artifact execution: position 1 (Layer-1 plan, this PR), position 2 (Layer-2 artifact PR, consolidates non-batching steps 2-7 because the decision is metadata-only — no DuckDB query, no validation module beyond falsifier suite, no scaffold beyond the decision module + mirrored test + jupytext notebook pair). Q-chain precedent: PR #250 → PR #251 followed the identical compressed pattern (Layer-1 plan → Layer-2 artifact in 9 files). Sequence steps 8 (research_log / STEP_STATUS) and 9 (reviewer-deep) are deferred to SEPARATE successor PRs."
source_artifacts:
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
  - planning/current_plan.md
  - planning/current_plan.critique.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.md
  - src/rts_predict/games/sc2/datasets/sc2egset/decide_history_rating_path.py
  - tests/rts_predict/games/sc2/datasets/sc2egset/test_decide_history_rating_path.py
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.md
  - src/rts_predict/games/sc2/datasets/sc2egset/proof_glicko2_implementation.py
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv
  - reports/specs/02_00_feature_input_contract.md
  - reports/specs/02_01_leakage_audit_protocol.md
  - reports/specs/02_02_feature_engineering_plan.md
  - reports/specs/02_03_temporal_feature_audit_protocol.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
  - .claude/scientific-invariants.md
  - .claude/ml-protocol.md
  - .claude/rules/data-analysis-lineage.md
  - .claude/rules/git-workflow.md
  - docs/PHASES.md
  - docs/TAXONOMY.md
  - docs/templates/planner_output_contract.md
  - docs/templates/plan_template.md
  - docs/templates/step_template.yaml
  - pyproject.toml
  - CHANGELOG.md
  - planning/INDEX.md
invariants_touched:
  - "I3 (temporal discipline — the future omit-closure artifact does NOT compute features; temporal discipline applies only to the downstream 5-family materialization PR, but the artifact MUST state that the 5-family unblock decision presupposes strict history_time < target_time for any future materialization)"
  - "I6 (SQL provenance — the future omit-closure artifact MD must embed verbatim queries / sentence-counts / cross-reference-counts with their derivation methods for any count it reports about Q6H §15)"
  - "I7 (no magic numbers / no magic gates — Branch (iii) preconditions are evidentiary admissibility criteria; the substantive paragraph + reviewer sign-off pins prevent boolean-driven closure; the ≥6-sentence and ≥3-cross-reference thresholds are inherited from Q6H §15 and traced to their derivation, not invented here)"
  - "I9 (research pipeline discipline — Step 02_01_99 conclusions derive only from its own future artifacts and from completed predecessor steps' artifacts)"
  - "I10 (raw data provenance / relative-path convention — the future omit-closure artifact uses relative paths in all SHA pins and prior_artifacts references)"
research_log_ref: null
---

# Plan: SC2EGSet Step 02_01_99 — Rating Omit-Closure Decision Artifact (Layer-1, Round 2)

This is **Round 2** of the Layer-1 plan. Round 1 reached **APPROVE-WITH-NITS** (0 blockers, 4 non-blocking nits) from reviewer-adversarial. The user has elected to bake ALL 4 nits into Round 2 BEFORE Layer-1 materialization (rather than deferring to Layer-2 dispatch). Outcome A is preserved. Round 2 changes are summarised in `## Adversarial-Review Adjustments (Round 1 → Round 2)`.

## Scope

This is a **Layer-1 planning-only PR** that authors the planning record for the **future Layer-2 omit-closure decision artifact execution PR**. The future Layer-2 PR (9 files; analogous to PR #251 Q6H Layer-2's 9-file diff) emits ONE artifact pair — `02_01_99_rating_omit_closure.{csv,md}` — recording Branch (iii) selection (`omit_reconstructed_rating_and_unblock_other_five`) under explicit Branch (iii) precondition satisfaction.

Round 2 makes the following explicit baked-in commitments that govern the future Layer-2 artifact:

1. The CSV schema is exactly **45 columns** (Round 1 had 42; Round 2 adds 3 via NITs #1, #3, #4 net +1).
2. The CSV records a new column `branch_ii_state_semantic_anchor` (NIT #1) that distinguishes Q6H Branch (ii) literal verdict state from omit-closure scope interpretation.
3. The CSV records a new column `elevation_rationale_jaccard_vs_q6h_section_15` (NIT #3) — float 4 decimal places.
4. The single Round-1 column `reviewer_adversarial_signoff_critique_sha256` is replaced by 4 columns covering Layer-1 and Layer-2 sign-off pairs (NIT #4).
5. The plan introduces `## Schema Derivation` between Future Artifact Contract and Future Tests Contract (NIT #2).
6. The plan introduces 4 new BINDING assumptions A26–A29 and 5 new falsifier keys.

The 2-file Layer-1 diff: `planning/current_plan.md` (this file) + `planning/current_plan.critique.md` (to be produced by reviewer-adversarial after this plan is committed). No code, no version bump, no CHANGELOG, no INDEX archive, no status YAML flip, no research_log entry, no spec edit, no ROADMAP edit, no source/test/notebook touch.

The future Layer-2 9-file diff:
1. New decision module `src/rts_predict/games/sc2/datasets/sc2egset/close_history_rating_omit_path.py`.
2. Mirrored test file `tests/rts_predict/games/sc2/datasets/sc2egset/test_close_history_rating_omit_path.py` (coverage target ≥95%).
3. Jupytext-paired notebook `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.py`.
4. Jupytext-paired notebook `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.ipynb`.
5. Decision CSV `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.csv` (**45 columns**).
6. Decision MD `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.md`.
7. `planning/INDEX.md` (archive this Layer-1 PR; promote Layer-2 PR).
8. `CHANGELOG.md` (new `[3.80.0]` section).
9. `pyproject.toml` (3.79.0 → 3.80.0).

Step 02_01_03 remains in_progress (no STEP_STATUS entry); Step 02_01_99 remains ROADMAP-only (no STEP_STATUS entry). Both step closures are downstream of this lineage segment.

Explicit "no execution" guarantees in this Layer-1 PR are preserved verbatim from Round 1: NO mutation of the Q6H artifact pair, NO mutation of the Q6H decision module, NO re-adjudication of Q5 / Q6F / Q6G / Q6H, NO ROADMAP edit, NO new Q6X PR, NO feature materialization / Parquet / CROSS-02-01 audit, NO 5-family ROADMAP narrowing, NO Step 02_01_03 closure, NO Phase 03 / Step 02_01_04 work, NO AoE2, NO thesis prose.

## Problem Statement

PR #253 (merged 2026-05-27 at master `a9cf552f`) inserted the Step `02_01_99` ROADMAP stub declaring the rating omit-closure follow-up lineage segment. The stub's `gate.artifact_check` (ROADMAP line 2668) explicitly states the gate fires "only after the future omit-closure artifact PR materializes the CSV + MD decision pair," and the `gate.continue_predicate` (line 2682) states "A future PR may begin the 5-family ROADMAP narrowing (amending Step 02_01_03's 6-family declaration to 5 families) only after the omit-closure artifact PR merges with a passing artifact_check." The omit-closure artifact PR is therefore the next atomic unit after PR #253.

The omit-closure decision is a **metadata-only adjudication**: it elevates `thesis_pragmatism` from the canonical-default FALSE to TRUE under explicit reviewer-adversarial sign-off (now split into Layer-1 and Layer-2 pins per NIT #4), re-verifies that Q6H §15 already contains ≥6 substantive sentences and ≥3 `PR #249 §X.Y` cross-references, records Branches (i) and (ii) as blocked-by-Layer-2-election with a verbatim semantic-anchor string (NIT #1), enforces an anti-boilerplate Jaccard token-overlap falsifier against Q6H §15 (NIT #3), and emits a CSV row with `verdict = omit_reconstructed_rating_and_unblock_other_five` plus the canonical 5-family permitted set verbatim from `Q6H_FIVE_FAMILY_POST_OMIT_SET`.

The Branch (iii) preconditions (Q6H `decide_history_rating_path.py` lines 457–481, embedded in the Q6H MD §7 decision rule):

1. Branches (i) AND (ii) are both blocked.
2. `thesis_pragmatism == TRUE` (canonical default is FALSE per A9(b); must be deliberately elevated).
3. `substantive_paragraph_ok == TRUE` (Q6H §15 sentence count ≥6 AND `PR #249 §X.Y` cross-reference count ≥3).
4. `reviewer_signoff == TRUE` (explicit reviewer-adversarial sign-off in `planning/current_plan.critique.md`).

Round 2 adds a fifth observable check (anti-boilerplate Jaccard): the elevation rationale's token-level Jaccard similarity with the Q6H §15 paragraph MUST be `< 0.5`, ensuring the rationale is substantively independent of the Q6H §15 evidence it cites.

The future Layer-2 artifact PR's job is to: (a) record all 4 preconditions plus the Jaccard observable as row fields with falsifier-grade names; (b) emit a decision CSV (schema specified in §Future Artifact Contract below; exactly **45 columns**) with one canonical decision row; (c) emit a decision MD with the required structure including §4.2 Q6H decision-rule literal quotes and §19.1 / §19.2 Layer-1 and Layer-2 sign-off subsections; (d) authorise downstream 5-family ROADMAP narrowing (a SEPARATE later PR after this artifact merges); (e) preserve all four Q-chain BINDING parent verdicts (Q5 / Q6F / Q6G / Q6H) byte-unchanged via SHA pins.

The two-path admission from Q6H §17 ("Layer-3 materialization or omit-closure follow-up") is preserved: this artifact selects the omit-closure path; the materialization path remains a SEPARATE downstream PR.

## Literature Context

### Internal authority (repo-internal artifacts and rules)

- **PR #253 ROADMAP stub** (`src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` lines 2527–2740) — declares Step `02_01_99` and binds the future omit-closure artifact's gate predicates.
- **PR #251 Q6H decision MD §17 (Non-Substitution Statement)** — verbatim authority basis: "Step 02_01_03 closure is deferred to a future PR (Layer-3 materialization or omit-closure follow-up)."
- **PR #251 Q6H decision MD §15 (Thesis-Pragmatism Rationale standby paragraph)** — the substantive paragraph invoked under Branch (iii). The omit-closure artifact does NOT rewrite or extend it; it re-counts it and (Round 2) computes a Jaccard distance against the new elevation rationale.
- **PR #251 Q6H decision module `Q6H_PATH_DECISION_RULE` Branch (ii) literal at lines 442–448** — verbatim Branch (ii) reasoning text (recommendation_only_event_by_event_glicko2). Quoted in artifact MD §4.2 (per NIT #1).
- **PR #251 Q6H decision module `Q6H_PATH_DECISION_RULE` Branch (iii) literal at lines 457–481** — verbatim cited as the source of the 4 Branch (iii) preconditions and the verdict literal `omit_reconstructed_rating_and_unblock_other_five`. Quoted in artifact MD §4.2 (per NIT #1).
- **PR #251 Q6H decision module `Q6H_FIVE_FAMILY_POST_OMIT_SET` constant** (`decide_history_rating_path.py` line 224) — the canonical 5-family set.
- **PR #251 Q6H decision module override falsifier** `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15`.
- **PR #249 Q6G implementation-proof MD §15 (rating-period limitations)** — evidence anchor for the Branch (iii) thesis-pragmatism elevation rationale.
- **PR #249 Q6G implementation-proof MD §13a (equivalence proof: Spearman rho = 0.2292; |Delta log-loss| = 0.07928)** — the evidentiary basis for Branch (ii) recommendation_only.
- **PR #247 Q6F survey MD §11 (Glicko-2 vs TrueSkill CI overlap ~0.9%)**.
- **PR #243 Q5 cross-region adjudication** (`Q5_selected_policy = sensitivity_indicator_co_registration`; BINDING).
- **PR #242 Step 02_01_03 source/anchor/cold-start adjudication**.
- **`.claude/rules/data-analysis-lineage.md` §"Non-batching rule"** and §"Stop conditions".
- **`.claude/scientific-invariants.md`** §I3, §I6, §I7, §I9, §I10.
- **`docs/TAXONOMY.md`** Step schema.
- **`docs/PHASES.md`** canonical Phase list.

### Precedent compressed Layer-1 → Layer-2 ladder (Q-chain pattern this plan mirrors)

- PR #244 → PR #245 (Q6).
- PR #246 → PR #247 (Q6F).
- PR #248 → PR #249 (Q6G).
- PR #250 → PR #251 (Q6H).
- PR #252 → PR #253 (02_01_99 ROADMAP-stub).
- **THIS PR (Round 2) → future Layer-2 artifact PR** (02_01_99 omit-closure decision): 2-file plan → 9-file artifact PR.

### External literature (not load-bearing for this Layer-1 plan)

- **Glickman (2012)** — cited transitively via PR #249 §15.
- **Steyerberg (2009), Hosmer-Lemeshow (2013)** — cited transitively via PR #247.

### Anti-boilerplate measurement literature (NIT #3)

- **Jaccard (1901)** — set-overlap coefficient. Token-level Jaccard `|intersect| / |union|` is the standard text-overlap measure for short paragraphs; threshold `>= 0.5` indicates substantial token overlap. The Round 2 threshold is `< 0.5` (rationale must be substantively independent of the Q6H §15 paragraph it cites). Reviewer-adversarial calibration: thresholds 0.3–0.5 are commonly used for plagiarism/paraphrase detection; 0.5 is the conservative ceiling.

## Assumptions & Unknowns

### Binding assumptions (A1–A29)

A1–A25 are preserved verbatim from Round 1. A23 is **revised** to reflect the dual sign-off structure (NIT #4). A26–A29 are **new** Round 2 BINDING assumptions.

- **A1 (BINDING) — Parent SHA pins (15 keys, pinned at Layer-1 plan time; re-verified at Layer-2 dispatch time):**
  - `parent_pr242_csv_sha256`: `f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b`
  - `parent_pr242_md_sha256`: `fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d`
  - `parent_pr243_csv_sha256`: `29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424`
  - `parent_pr243_md_sha256`: `026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719`
  - `parent_pr245_csv_sha256`: `703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0`
  - `parent_pr245_md_sha256`: `7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419`
  - `parent_pr247_csv_sha256`: `249e5591c6505b748fe3d371284a72d8f4620f57dbe9628c908ec2fbf097c8ed`
  - `parent_pr247_md_sha256`: `4b49bee405bf87d4b8920b188e2c38d185ecc077b532d64a8bdd5a90cdf143f2`
  - `parent_pr249_csv_sha256`: `1d9ee22e0523e640181fa0a7a7d2680467a267eefa376fec903f58094118b82f`
  - `parent_pr249_md_sha256`: `8beed3ba6491afb6ba72ee2718b1364c9a2577b26c82237b735d219ccfdc0ea1`
  - `parent_pr251_csv_sha256` (Q6H CSV) — computed at Layer-2 dispatch via `sha256sum`.
  - `parent_pr251_md_sha256` (Q6H MD) — computed at Layer-2 dispatch via `sha256sum`.
  - `parent_pr251_module_sha256` (Q6H `decide_history_rating_path.py`) — computed at Layer-2 dispatch via `sha256sum`.
  - `parent_pr253_roadmap_sha256` (PR #253 merged ROADMAP) — computed at Layer-2 dispatch via `sha256sum`.
  - `head_master_sha_at_layer_1_plan_time`: `a9cf552f346d8402fa4856fbee51fa34b0b0cefe`
- **A2 (BINDING) — Q6H lineage preservation:** The Q6H artifact pair and the Q6H decision module are READ-ONLY parent provenance for Step 02_01_99 closure-side work.
- **A3 (BINDING) — No in-place Q6H artifact mutation.**
- **A4 (BINDING) — Branch (iii) precondition enumeration (4 pins) — each is an observable CSV row field.**
- **A5 (BINDING) — 5-family set canonical reference:** Members of `Q6H_FIVE_FAMILY_POST_OMIT_SET`: `focal_player_history`, `opponent_player_history`, `matchup_history_aggregate`, `cross_region_fragmentation_handling`, `in_game_history_aggregate`. Excluded sixth family: `reconstructed_rating`. Excluded columns: `reconstructed_rating_focal_pre`, `reconstructed_rating_opp_pre`, `reconstructed_rating_diff`.
- **A6 (BINDING) — No spec mutation.**
- **A7 (BINDING) — No status YAML mutation.**
- **A8 (BINDING) — No research_log entry.**
- **A9 (BINDING) — Future Layer-2 version bump:** `3.79.0 → 3.80.0`.
- **A10 (BINDING) — No Q6X PR; closure-side module name `close_history_rating_omit_path.py`.**
- **A11 (BINDING) — Step token `02_01_99`.**
- **A12 (BINDING) — No materialization, no Parquet, no CROSS-02-01 audit.**
- **A13 (BINDING) — Decision-rule order-of-operations preserved.**
- **A14 (BINDING) — Adversarial round cap: 3 rounds total on the planning side.**
- **A15 (BINDING) — Adversarial cap symmetry: same 3-round cap on execution-side.**
- **A16 (BINDING) — No ROADMAP narrowing in this lineage segment.**
- **A17 (BINDING) — Plan word budget: 1100–1400 lines (Round 2 expanded from Round 1's 939 by new sections + dual sign-off + Jaccard observables + NIT #1 semantic anchor + per-column Schema Derivation).**
- **A18 (BINDING) — Required `##` sections.** Scope, Problem Statement, Literature Context, Assumptions & Unknowns, Execution Steps, File Manifest, Gate Condition, Open Questions, plus additional preserved sections plus Round-2 new sections (`## Schema Derivation`, `## Adversarial-Review Adjustments (Round 1 → Round 2)`).
- **A19 (BINDING) — Compressed Layer-2 scope (9 files).**
- **A20 (BINDING) — Q6H §17 verbatim citation.**
- **A21 (BINDING) — Q6H §15 invocation, not rewriting.**
- **A22 (BINDING) — `thesis_pragmatism_elevation_rationale` column content discipline.** ≥3 specific `PR #249 §X.Y` cross-references AND ≥6 substantive sentences in artifact MD §6. Round 2: ALSO Jaccard `< 0.5` against Q6H §15 (anti-copy-paste).
- **A23 (BINDING, Round-2 revised) — Reviewer-adversarial sign-off recording (DUAL STRUCTURE per NIT #4):**
  - **Layer-1 sign-off:** Recorded in two places: (i) in the `planning/current_plan.critique.md` of THIS Layer-1 PR (planning-side critique location); (ii) in the artifact MD's §19.1 "Reviewer-Adversarial Layer-1 Sign-Off" section as a SHA pin to that critique file.
    - The Layer-1 SHA `reviewer_adversarial_layer_1_critique_sha256` = `sha256sum planning/current_plan.critique.md` is computed at the **artifact PR's execution start (Layer-2 T01)** because the Layer-1 critique is finalized at Layer-1 PR merge time, which precedes Layer-2 dispatch. The Layer-1 PR merge SHA must already exist; the SHA pin is over the merged-state byte content.
  - **Layer-2 sign-off:** Recorded in two places: (i) in the `planning/current_plan.critique.md` of the future Layer-2 PR (the artifact PR's own critique); (ii) in the artifact MD's §19.2 "Reviewer-Adversarial Layer-2 Sign-Off" section as a SHA pin to that critique file.
    - The Layer-2 SHA `reviewer_adversarial_layer_2_critique_sha256` = `sha256sum planning/current_plan.critique.md` is computed at the artifact PR's **commit time (Layer-2 T09 after reviewer-adversarial sign-off)**.
  - Both sign-offs MUST be APPROVE or APPROVE-WITH-NITS with 0 blockers; the booleans `reviewer_adversarial_signoff_layer_1` and `reviewer_adversarial_signoff_layer_2` are TRUE iff the corresponding critique recorded an admissible verdict.
  - The Round-1 single column `reviewer_adversarial_signoff_critique_sha256` is replaced by 4 columns; the net schema delta is +2.
- **A24 (BINDING) — Q6H §15 cross-reference enumeration discipline:** regex `r'PR #249 §[0-9]+(?:[.][0-9]+)?[a-z]?'`.
- **A25 (BINDING) — Q6G/Q6F evidence anchor citation discipline.**
- **A26 (BINDING, NEW Round 2 per NIT #1) — Branch (ii) state semantic anchor recording:** A new CSV column `branch_ii_state_semantic_anchor` (string) records a semicolon-separated 4-key declaration distinguishing:
  - (a) Q6H Branch (ii) literal verdict state (verdict was actually REACHED, not blocked; verdict = `recommendation_only_event_by_event_glicko2`);
  - (b) omit-closure scope interpretation (Branch (ii) is BLOCKED for the current Phase-02 materialization scope, under the Layer-2 election authorised by this artifact's own scope; the block is a SCOPE statement, not a verdict statement);
  - (c) explicit assertion that this anchor is NOT Q6H re-adjudication;
  - (d) explicit assertion that this anchor does NOT open a new Q6X loop.

  The canonical column value format is exactly:
  ```
  q6h_verdict_state=reached_as_recommendation_only_event_by_event_glicko2;omit_closure_scope_interpretation=blocked_for_phase_02_materialization_scope_under_layer_2_election;is_q6h_re_adjudication=FALSE;is_new_q6x_loop=FALSE
  ```
  The artifact MD §4.2 quotes the Q6H decision-rule literal lines 442–448 (Branch (ii) reasoning) AND 457–481 (Branch (iii) preconditions) to source-anchor the distinction. Falsifier `omit_closure_branch_ii_state_anchor_misnamed_or_missing_re_adjudication_assertion` enforces.

- **A27 (BINDING, NEW Round 2 per NIT #4) — Layer-1 SHA timing:** The Layer-1 critique SHA `reviewer_adversarial_layer_1_critique_sha256` is computed at the **Layer-2 T01** execution-start step (after the Layer-1 PR has merged and reviewer-adversarial Round 1 verdict is finalized). The SHA is over the merged-state byte content of `planning/current_plan.critique.md` from the Layer-1 PR.

  Operational rule: at Layer-2 T01, after `git fetch origin master`, verify that the Layer-1 critique file's verdict is APPROVE or APPROVE-WITH-NITS with 0 blockers; compute `sha256sum planning/current_plan.critique.md` against the merged Layer-1 byte state; pin into the artifact CSV row.

  Falsifier `omit_closure_reviewer_signoff_layer_1_missing_or_invalid_sha` enforces.

- **A28 (BINDING, NEW Round 2 per NIT #4) — Layer-2 SHA timing:** The Layer-2 critique SHA `reviewer_adversarial_layer_2_critique_sha256` is computed at the **Layer-2 T09** step (after reviewer-adversarial Round 1 has signed off on the Layer-2 PR's diff).

  Operational rule: after reviewer-adversarial completes its Round-1 (or Round-2 / Round-3 within the 3-round cap) verdict on the Layer-2 PR, ensure the verdict is APPROVE or APPROVE-WITH-NITS with 0 blockers; compute `sha256sum planning/current_plan.critique.md` against the Layer-2 critique file's current state; pin into the artifact CSV row before the artifact CSV is written.

  Practical sequencing: the artifact CSV is written by `run_close_history_rating_omit_path()` which is invoked from the sandbox notebook at T04 (before T09). To satisfy A28 timing, the notebook reads the critique file at invocation time. If T09 modifies the critique file (e.g., reviewer-adversarial signs off in a separate commit), the artifact CSV+MD MUST be regenerated after T09 sign-off and the regenerated SHA pinned. Falsifier `omit_closure_reviewer_signoff_layer_2_missing_or_invalid_sha` enforces.

  This creates a sequencing nuance: if reviewer-adversarial requires changes to the Layer-2 PR diff (Round 1 nits or blockers), the artifact CSV+MD must be regenerated AFTER the changes are committed AND after the final reviewer-adversarial sign-off SHA stabilises. This is precedented in Q-chain Layer-2 PRs (the sandbox notebook is rerun in T09 if reviewer-adversarial requests changes).

- **A29 (BINDING, NEW Round 2 per NIT #3) — Anti-boilerplate Jaccard discipline:** The token-level Jaccard similarity between the artifact MD §6 elevation rationale text and the Q6H MD §15 standby paragraph text MUST be `< 0.5` (token-level Jaccard). The threshold is enforced both:
  - As a CSV column `elevation_rationale_jaccard_vs_q6h_section_15` (float, 4 decimal places — `:.4f` format).
  - As a falsifier `omit_closure_elevation_rationale_jaccard_overlap_with_q6h_section_15_exceeds_threshold` that fires iff `jaccard >= 0.5`.

  **Mechanics (verbatim binding):** tokenize both texts by whitespace; lowercase every token; strip punctuation using `str.translate(str.maketrans("", "", string.punctuation))`; build two token sets `set_a` and `set_b`; compute `jaccard = len(set_a & set_b) / len(set_a | set_b)` (guard against zero-division: if `len(set_a | set_b) == 0` return `1.0` and let the falsifier fire — that indicates degenerate input); fire IF `jaccard >= 0.5`.

  **Rationale for threshold `>= 0.5`:** Token-level Jaccard ≥0.5 indicates the elevation rationale shares more than half of unique tokens with Q6H §15 (after lowercase + punctuation strip), which means the rationale is largely a paraphrase or copy-paste of the §15 paragraph rather than an independent substantive argument. The reviewer-adversarial review at T09 is the substantive guardrail; the Jaccard threshold is the structural guardrail.

  **Implementation:** functions `_tokenize_for_jaccard(text: str) -> set[str]` and `_compute_jaccard(set_a: set[str], set_b: set[str]) -> float` in `close_history_rating_omit_path.py` (T02). Test `test_omit_closure_elevation_rationale_jaccard_lt_threshold` in T03. Pre-emit verification in T04 (sandbox notebook reads §6 text and Q6H §15 text, computes Jaccard, asserts `< 0.5`, then calls `run_close_history_rating_omit_path()`).

### Unknowns (U1–U7) — preserved from Round 1; no new Round-2 unknowns

- **U1:** Final regex for `PR #249 §X.Y` cross-reference enumeration.
- **U2:** `nltk.sent_tokenize` vs regex fallback.
- **U3:** Single-row CSV.
- **U4:** Dual-count discipline.
- **U5:** Decision module function signature.
- **U6 (resolved 2026-05-27):** Branch slug `feat/sc2egset-02-01-99-rating-omit-closure-artifact`.
- **U7:** CSV `excluded_columns` semicolon-separation.

### Acknowledged limitations (L1–L5) — preserved verbatim from Round 1

- **L1:** Omit-closure does NOT resolve the Phase-03 rating decision.
- **L2:** This plan does NOT bind a Step 02_01_03 closure date or a Step 02_01_99 closure date.
- **L3:** The future omit-closure artifact does NOT execute any DuckDB query.
- **L4:** The `thesis_pragmatism` elevation is methodologically subjective. Round 2: the new Jaccard threshold (A29) plus the existing dual-count discipline (A22) plus the dual-sign-off discipline (A23) all constrain the judgment.
- **L5:** The 5-family unblock is for the future materialization PR's scope; NOT retroactive to Step 02_01_03's existing ROADMAP block.

## Future Artifact Contract

### Future artifact requirements (per the upstream prompt; verified; Round-2 update)

1. Sets `thesis_pragmatism = TRUE` in the CSV row.
2. MD has ≥6 substantive sentences in its thesis-pragmatism elevation section.
3. MD has ≥3 `PR #249 §X.Y` cross-references in the elevation section.
4. Records reviewer-adversarial sign-off as TWO SHA pins (Layer-1 and Layer-2; NIT #4).
5. CSV verdict row selects `omit_reconstructed_rating_and_unblock_other_five`.
6. Explicitly states Q6 is intentionally omitted/excluded.
7. Lists exactly the five-family permitted set.
8. Lists excluded family `reconstructed_rating`.
9. Lists excluded column names verbatim from Q6H Branch (iii) literal.
10. States NO feature materialization occurs.
11. States future ROADMAP scope-amendment PR + future 5-family materialization PR are SEPARATE downstream units.
12. Preserves Q5/Q6F/Q6G/Q6H parent verdicts byte-unchanged via SHA pins.
13. Preserves Step 02_01_03's existing 6-family ROADMAP declaration.
14. Does NOT open another Q6X loop.
15. **(NEW, NIT #1)** Records `branch_ii_state_semantic_anchor` distinguishing Q6H verdict state from omit-closure scope interpretation.
16. **(NEW, NIT #3)** Records Jaccard similarity `< 0.5` between elevation rationale and Q6H §15.
17. **(NEW, NIT #4)** Records dual Layer-1 + Layer-2 reviewer sign-off.

### Future artifact CSV schema (exactly 45 columns)

The future omit-closure CSV MUST contain exactly **45 columns** in the canonical order below. Each row is a single canonical decision row. The exact column count is asserted at module load via `assert len(OMIT_CLOSURE_SCHEMA) == 45`; deviation triggers `omit_closure_schema_column_count_mismatch` falsifier.

```
01. decision_id                                          # "OMIT_CLOSURE_omit_reconstructed_rating_and_unblock_other_five"
02. parent_step_number                                   # "02_01_03"
03. lineage_step_number                                  # "02_01_99"
04. decision_name                                        # "rating_omit_closure"
05. verdict                                              # "omit_reconstructed_rating_and_unblock_other_five"
06. binding_level                                        # "BINDING"
07. selected_policy                                      # "omit_reconstructed_rating_and_unblock_other_five"
08. thesis_pragmatism                                    # "TRUE"
09. thesis_pragmatism_sentence_count                     # >= 6 (artifact's elevation section)
10. thesis_pragmatism_q6h_section_15_sentence_count      # >= 6 (Q6H §15 re-counted)
11. pr249_cross_reference_count                          # >= 3 (artifact's elevation section)
12. pr249_cross_reference_count_q6h_section_15           # >= 3 (Q6H §15 re-counted)
13. elevation_rationale_jaccard_vs_q6h_section_15        # float, 4 decimal places; < 0.5  (NEW NIT #3)
14. branch_ii_state_semantic_anchor                      # 4-key semicolon string (NEW NIT #1)
15. reviewer_adversarial_signoff_layer_1                 # "TRUE" iff Layer-1 critique APPROVE/APPROVE-WITH-NITS with 0 blockers (NEW NIT #4)
16. reviewer_adversarial_layer_1_critique_sha256         # 64-char hex; pinned at Layer-2 T01 (NEW NIT #4)
17. reviewer_adversarial_signoff_layer_2                 # "TRUE" iff Layer-2 critique APPROVE/APPROVE-WITH-NITS with 0 blockers (NEW NIT #4)
18. reviewer_adversarial_layer_2_critique_sha256         # 64-char hex; pinned at Layer-2 T09 (NEW NIT #4)
19. q6_omission_status                                   # "intentionally_omitted_under_branch_iii"
20. q6_not_silently_satisfied                            # "TRUE"
21. five_family_materialization_permission               # permitted-string-with-conditions
22. five_family_set                                      # semicolon-separated 5 names
23. excluded_family                                      # "reconstructed_rating"
24. excluded_columns                                     # semicolon-separated 3 names
25. future_roadmap_scope_amendment_required              # "TRUE"
26. future_materialization_pr_required                   # "TRUE"
27. q5_policy                                            # "sensitivity_indicator_co_registration"
28. q6f_policy                                           # "narrow_with_evidence"
29. q6g_policy                                           # "recommendation_only_glicko2"
30. q6h_policy                                           # "recommendation_only_event_by_event_glicko2"
31. evidence_paths                                       # semicolon-separated relative paths
32. falsifiers                                           # semicolon-separated falsifier-key list
33. audit_pr                                             # "PR #<TBD>"
34. parent_pr242_csv_sha256                              # from A1
35. parent_pr242_md_sha256                               # from A1
36. parent_pr243_csv_sha256                              # from A1
37. parent_pr243_md_sha256                               # from A1
38. parent_pr245_csv_sha256                              # from A1
39. parent_pr245_md_sha256                               # from A1
40. parent_pr247_csv_sha256                              # from A1
41. parent_pr247_md_sha256                               # from A1
42. parent_pr249_csv_sha256                              # from A1
43. parent_pr249_md_sha256                               # from A1
44. parent_pr251_csv_sha256                              # from A1 (Q6H CSV; computed at Layer-2 dispatch)
45. parent_pr251_md_sha256                               # from A1 (Q6H MD; computed at Layer-2 dispatch)
```

**Column count: 45.** Deviations from Round 1 (42 columns): +1 column `elevation_rationale_jaccard_vs_q6h_section_15` (NIT #3); +1 column `branch_ii_state_semantic_anchor` (NIT #1); +2 columns net for the sign-off split (1 → 4; NIT #4). Removed: `reviewer_adversarial_signoff`, `reviewer_adversarial_signoff_critique_sha256`. The 4 dispatch-time SHA columns retained from Round 1 (`parent_pr251_*_sha256`, `parent_pr251_module_sha256`, `parent_pr253_roadmap_sha256`) are NOT all in the schema in Round 2; the schema retains only the 12 SHA columns shown above (10 hard-coded + 2 dispatch-time Q6H). The Q6H module SHA and PR #253 ROADMAP SHA continue to be pinned in module constants (not the CSV row) per A1 and the module's `OMIT_CLOSURE_PARENT_SHA_PINS` dict; the artifact MD §20 also records them. This is a Round-1 → Round-2 simplification documented in §Schema Derivation column 16.

All `*_sha256` fields are deterministic 64-char lowercase hex; no `NOT_FOUND` allowed.

### Future artifact MD structure (sections updated for NIT #1 and NIT #4)

The future omit-closure MD has the following sections in order:

1. **§1 Summary** — non-materialization disclaimer; Q6H §17 verbatim citation.
2. **§2 Parent Lineage** — PR #243, PR #245, PR #247, PR #249, PR #251, PR #253; lists all 15 SHA pins.
3. **§3 Scope and Explicit Exclusions.**
4. **§4 Branch (iii) Precondition Re-Verification.**
   - **§4.1 Four-precondition observable evidence.**
   - **§4.2 (NEW per NIT #1) Q6H decision-rule literal quotes** — verbatim citation of `decide_history_rating_path.py` lines 442–448 (Branch (ii) reasoning text) AND lines 457–481 (Branch (iii) precondition logic). Used to source-anchor the `branch_ii_state_semantic_anchor` column. Includes an explicit subsection narrative: "This subsection quotes the Q6H decision-rule literal verbatim. The omit-closure artifact does NOT re-adjudicate Q6H. The Branch (ii) verdict was REACHED (not blocked) by Q6H; the omit-closure artifact records that Branch (ii) is blocked-for-Phase-02-materialization-scope under the Layer-2 election, which is a SCOPE statement, not a verdict statement. This is NOT a new Q6X loop."
5. **§5 Q6H §15 Re-Count Methodology.**
6. **§6 Thesis-Pragmatism Elevation Rationale (Layer-2 election; ≥6 sentences; ≥3 `PR #249 §X.Y` cross-references; Jaccard < 0.5 vs Q6H §15).**
7. **§7 Q5/Q6F/Q6G/Q6H Parent Verdict Preservation.**
8. **§8 The 5-Family Permitted Set.**
9. **§9 Excluded Family and Excluded Columns.**
10. **§10 Q6 Intentionally Omitted (Not Silently Satisfied).**
11. **§11 Schema Column Count Assertion (Round-2 per NIT #2) — embeds the per-column Schema Derivation rationale verbatim from the plan's `## Schema Derivation` section.** Each of the 7 columns added beyond the Q6H 38-column schema MUST have ≥1 substantive sentence of derivation prose. Asserts `len(OMIT_CLOSURE_SCHEMA) == 45`.
12. **§12 Falsifier Roll-Call.**
13. **§13 Future ROADMAP Scope Amendment Requirement.**
14. **§14 Future Materialization Requirement.**
15. **§15 Explicit Non-Substitution Statement.**
16. **§16 No Step Closure Claim.**
17. **§17 No Phase 03 Claim.**
18. **§18 No Feature Materialization Claim.**
19. **§19 Reviewer-Adversarial Sign-Off Section.**
    - **§19.1 Reviewer-Adversarial Layer-1 Sign-Off** (NEW Round-2 per NIT #4): SHA pin to Layer-1 `planning/current_plan.critique.md`; verbatim Layer-1 sign-off quote; reviewer agent identity (`reviewer-adversarial`); verdict (APPROVE or APPROVE-WITH-NITS with 0 blockers); date pinned at Layer-2 T01.
    - **§19.2 Reviewer-Adversarial Layer-2 Sign-Off** (NEW Round-2 per NIT #4): SHA pin to Layer-2 `planning/current_plan.critique.md`; verbatim Layer-2 sign-off quote; reviewer agent identity; verdict; date pinned at Layer-2 T09.
20. **§20 Provenance (15 SHA Pins + Master HEAD SHA).**
21. **§21 Final Verdict.**

## Schema Derivation

This Round-2 section (NEW per NIT #2) reproduces the per-column derivation rationale for each of the 7 columns that deviate from the Q6H 38-column schema. The artifact MD §11 quotes this section verbatim.

The Q6H artifact (PR #251) used a 38-column schema. The Round-2 omit-closure artifact uses a 45-column schema. The 7 deviations:

**Deviation 1 — `elevation_rationale_jaccard_vs_q6h_section_15` (column 13; NIT #3; float, `:.4f`).** Reviewer-adversarial Round-1 concern: the dual-count discipline (sentence count ≥6 + cross-reference count ≥3) can be satisfied by a boilerplate paraphrase of the Q6H §15 paragraph. Round-2 mitigation: a token-level Jaccard similarity measure against Q6H §15 with threshold `< 0.5` enforces that the elevation rationale shares less than half of its unique tokens (after lowercase + punctuation strip) with the §15 paragraph. The column makes the Jaccard observable inspectable post-emission; the corresponding falsifier `omit_closure_elevation_rationale_jaccard_overlap_with_q6h_section_15_exceeds_threshold` makes it test-grade. Lineage need: the elevation rationale's substantive independence from Q6H §15 is the methodological backbone of Branch (iii); without this falsifier, reviewer-adversarial T09 sign-off carries the entire substantive burden, leaving no structural guardrail. Threshold derivation: Jaccard ≥0.5 is the conservative ceiling for "paraphrase-likely" overlap in short paragraphs; threshold can be tightened post-Round-2 in a downstream PR if the §6 text proves to consistently score `<< 0.5`.

**Deviation 2 — `branch_ii_state_semantic_anchor` (column 14; NIT #1; string, semicolon-separated 4-key format).** Reviewer-adversarial Round-1 concern: re-labeling Q6H Branch (ii) as "blocked-by-Layer-2-election" risks subtle re-adjudication of Q6H's actual verdict (which was REACHED, not blocked). Round-2 mitigation: a structured 4-key string explicitly distinguishes (a) Q6H literal verdict state, (b) omit-closure scope interpretation, (c) absence of Q6H re-adjudication, (d) absence of new Q6X loop. The column value format is binding: `q6h_verdict_state=reached_as_recommendation_only_event_by_event_glicko2;omit_closure_scope_interpretation=blocked_for_phase_02_materialization_scope_under_layer_2_election;is_q6h_re_adjudication=FALSE;is_new_q6x_loop=FALSE`. Lineage need: the OQ7 wording bridge (from PR #252 critique R2-N1) is preserved in plain-text form in Round 1 (§Assumptions A4(a) and the Open Question OQ7), but Round-1 did not surface the distinction as a falsifier-checkable row field. Reviewer concern: greps for "Branch (ii) blocked" must reach a row showing both the verdict state and the scope interpretation, not implicit prose. The column makes the distinction grep-able. Falsifier `omit_closure_branch_ii_state_anchor_misnamed_or_missing_re_adjudication_assertion` enforces.

**Deviation 3 — `reviewer_adversarial_signoff_layer_1` (column 15; NIT #4; boolean string `TRUE` / `FALSE`).** Reviewer-adversarial Round-1 concern: a single sign-off SHA conflates the Layer-1 planning critique (which authorises the Layer-2 execution) with the Layer-2 execution critique (which audits the emitted artifact). Round-2 mitigation: the boolean is TRUE iff the Layer-1 critique recorded APPROVE or APPROVE-WITH-NITS with 0 blockers. Lineage need: making Layer-1 sign-off auditable independently of Layer-2 sign-off lets the artifact's reader verify "the planning critique was admissible" without re-reading the entire critique file. Falsifier `omit_closure_reviewer_signoff_layer_1_or_layer_2_not_approve_with_zero_blockers` enforces.

**Deviation 4 — `reviewer_adversarial_layer_1_critique_sha256` (column 16; NIT #4; SHA pin).** Reviewer-adversarial Round-1 concern: the original single SHA column did not specify whether the Layer-1 or Layer-2 critique was pinned. Round-2 mitigation: the SHA is computed at Layer-2 T01 against the Layer-1 PR's merged-state byte content. Lineage need: pinning the Layer-1 critique SHA at Layer-2 T01 establishes a deterministic provenance chain from Layer-1 PR merge → Layer-2 dispatch. Falsifier `omit_closure_reviewer_signoff_layer_1_missing_or_invalid_sha` enforces. The schema simplification (Round-1's `parent_pr251_module_sha256` and `parent_pr253_roadmap_sha256` removed from the CSV row to preserve the 45-column budget) is documented here: those two SHAs are pinned in the module constant `OMIT_CLOSURE_PARENT_SHA_PINS` and recorded in MD §20, not in the CSV row. This preserves the auditable provenance without bloating the CSV.

**Deviation 5 — `reviewer_adversarial_signoff_layer_2` (column 17; NIT #4; boolean string `TRUE` / `FALSE`).** Same logic as Deviation 3 applied to Layer-2. Reviewer concern: the Layer-2 sign-off is the execution-side audit; making it a separate boolean lets downstream readers verify "the execution critique was admissible" independently. Lineage need: dual-boolean structure mirrors the dual-critique structure (Layer-1 planning critique + Layer-2 execution critique). Falsifier `omit_closure_reviewer_signoff_layer_1_or_layer_2_not_approve_with_zero_blockers` (shared with Deviation 3) enforces both booleans.

**Deviation 6 — `reviewer_adversarial_layer_2_critique_sha256` (column 18; NIT #4; SHA pin).** Reviewer-adversarial Round-1 concern: same as Deviation 4 for Layer-2. Round-2 mitigation: the SHA is computed at Layer-2 T09 against the Layer-2 critique file's post-sign-off byte state. Lineage need: pinning the Layer-2 critique SHA at T09 establishes a deterministic provenance chain from reviewer-adversarial Layer-2 sign-off → final artifact CSV emission. Practical sequencing note: if T09 modifies the critique file (e.g., Round-2 sign-off), the artifact CSV+MD MUST be regenerated; this is precedented in Q-chain artifact PRs (the notebook is rerun if reviewer-adversarial requests changes). Falsifier `omit_closure_reviewer_signoff_layer_2_missing_or_invalid_sha` enforces.

**Deviation 7 — Duplication of artifact-elevation count vs Q6H-section-15 re-count (columns 9–10 sentence counts + columns 11–12 cross-reference counts).** This deviation was present in Round 1 (columns 9, 10, 11, 12) and is retained in Round 2 unchanged. Reviewer-adversarial Round-1 acknowledged this as a methodologically correct dual-count discipline (the elevation §6 has its own independent count; Q6H §15 has its independent count; the dual-count makes the discipline grep-able and prevents copy-paste). Lineage need: the dual-count enforces that the elevation rationale is independent of Q6H §15's evidence count.

The 38-column Q6H schema is preserved as a sub-schema (the omit-closure schema is a strict superset by these 7 deviations; no Q6H column is removed). The 45-column count is asserted at module load.

## Future Tests Contract

The future Layer-2 PR's `tests/rts_predict/games/sc2/datasets/sc2egset/test_close_history_rating_omit_path.py` MUST cover at minimum the following test categories. Coverage target ≥95%.

- **Parent SHA verification:** Tests for each of the 15 SHA pins.
- **Parent PR #253 ROADMAP SHA verification.**
- **Schema column count: assert `len(OMIT_CLOSURE_SCHEMA) == 45`.** (Round-2 update from 42 → 45.)
- **Every planned decision row present.**
- **No `NOT_FOUND` SHA fields.**
- **No materialized output path.**
- **No feature materialization artifact.**
- **No CROSS-02-01 audit.**
- **No status YAML change.**
- **No `research_log` change.**
- **No ROADMAP change.**
- **No Q5/Q6F/Q6G/Q6H re-adjudication drift.**
- **`thesis_pragmatism = TRUE`.**
- **Thesis-pragmatism elevation sentence count ≥6.**
- **Q6H §15 re-count sentence count ≥6.**
- **PR #249 cross-reference count ≥3 (artifact §6).**
- **PR #249 cross-reference count ≥3 (Q6H §15 re-count).**
- **(NEW Round-2 per NIT #3) `test_omit_closure_elevation_rationale_jaccard_lt_threshold`:** Tokenize artifact MD §6 and Q6H §15; compute Jaccard; assert `< 0.5`. Implements the falsifier as a test.
- **(NEW Round-2 per NIT #1) `test_omit_closure_branch_ii_state_anchor_format`:** Parse the `branch_ii_state_semantic_anchor` column; assert it contains exactly 4 semicolon-separated key=value pairs with the canonical key names from A26; assert `is_q6h_re_adjudication=FALSE` and `is_new_q6x_loop=FALSE`.
- **(NEW Round-2 per NIT #4) `test_reviewer_adversarial_signoff_layer_1_recorded`:** Assert `reviewer_adversarial_signoff_layer_1 = "TRUE"` AND `reviewer_adversarial_layer_1_critique_sha256` is 64-char hex.
- **(NEW Round-2 per NIT #4) `test_reviewer_adversarial_signoff_layer_2_recorded`:** Assert `reviewer_adversarial_signoff_layer_2 = "TRUE"` AND `reviewer_adversarial_layer_2_critique_sha256` is 64-char hex.
- **(NEW Round-2 per NIT #4) `test_reviewer_signoff_both_layers_zero_blockers`:** Assert both Layer-1 and Layer-2 critique verdicts are APPROVE or APPROVE-WITH-NITS with 0 blockers (loaded from the critique files).
- **`omit_reconstructed_rating_and_unblock_other_five` selected.**
- **`reconstructed_rating` excluded.**
- **Exact five-family set present.**
- **Excluded columns present.**
- **Q6 not silently satisfied.**
- **No Phase 03 / baseline modeling creep.**
- **No Step 02_01_04 creep.**
- **Byte determinism modulo allowed provenance fields.**
- **No new Q6X PR.**
- **Override falsifier Q6H §15 preservation.**

Approximate test count: **55–85 tests** (Round-1 estimate 50–80 + the 5 new Round-2 tests).


## Branch & Versioning

### Branch slug (this Layer-1 PR)

```
feat/sc2egset-02-01-99-rating-omit-closure-artifact
```

**Rationale:** Per A11 / U6 / OQ6, the canonical token `02_01_99` is taxonomy-conformant and matches the on-disk ROADMAP `step_number`.

### Branch slug (future Layer-2 PR)

The future Layer-2 artifact PR uses the SAME branch slug as this Layer-1 PR.

### Version bumps

- **This Layer-1 PR:** No version bump (planning-only; 2 files).
- **Future Layer-2 PR:** `3.79.0 → 3.80.0` (minor; feat-family).

## Hard Stops

This Layer-1 PR's diff is restricted to 2 files: `planning/current_plan.md` + `planning/current_plan.critique.md`. ALL of the following are forbidden in this Layer-1 PR; the future Layer-2 PR ALSO enforces these (except where explicitly noted as part of the Layer-2 file manifest):

- Do NOT execute the omit-closure artifact in this Layer-1 PR.
- Do NOT create omit-closure CSV/MD artifacts in this Layer-1 PR.
- Do NOT create / edit source modules, tests, or notebooks in this Layer-1 PR.
- Do NOT edit ROADMAP in this Layer-1 PR (and the future Layer-2 artifact PR also does NOT edit ROADMAP).
- Do NOT materialize features in this Layer-1 PR or in the future Layer-2 artifact PR.
- Do NOT create feature artifacts or Parquet outputs in either PR.
- Do NOT create CROSS-02-01 audit artifacts in either PR.
- Do NOT update status YAMLs in either PR.
- Do NOT update dataset or root `research_log.md` in either PR.
- Do NOT edit `CHANGELOG.md`, `pyproject.toml`, or `planning/INDEX.md` in THIS Layer-1 PR.
- Do NOT edit specs, cleaning-layer YAMLs, thesis files, docs, `.claude`, data, notebooks, or AoE2 paths in either PR.
- Do NOT start Step `02_01_04` in either PR.
- Do NOT start Phase 03 in either PR.
- Do NOT run baseline modeling in either PR.
- Do NOT open another Q6X PR in either PR.
- Do NOT merge this Layer-1 PR until reviewer-adversarial Round 2 verdict is APPROVE or APPROVE-WITH-NITS with zero blockers.
- Do NOT mark the draft PR ready until user explicitly approves.
- Do NOT rewrite, paraphrase, extend, or degrade the Q6H §15 standby paragraph in either PR.
- Do NOT mutate `decide_history_rating_path.py` in either PR.
- Do NOT mutate the Q6H artifact pair in either PR.
- Do NOT mutate any other Q-chain artifact in either PR.

## Execution Steps

The Execution Steps below describe the FUTURE Layer-2 omit-closure artifact execution PR. This Layer-1 planning PR itself has NO execution steps in the operational sense.

### T01 — Create execution branch and verify pre-execution state (Round-2 updated for NIT #4 Layer-1 SHA timing)

**Objective:** Branch off master HEAD pinned at the Layer-1 merge SHA; verify that this Layer-1 plan has merged and that reviewer-adversarial Round 2 (planning-side) verdict is APPROVE or APPROVE-WITH-NITS with 0 blockers; pin the 15 parent SHAs; compute and pin the Layer-1 critique SHA per A27.

**Instructions:**
1. Run `git fetch origin master` and verify HEAD SHA is the Layer-1 merge commit. Pin the actual SHA in the PR description.
2. Create new branch `feat/sc2egset-02-01-99-rating-omit-closure-artifact` off the Layer-1 merge SHA.
3. Verify `pyproject.toml` version reads `3.79.0`.
4. Verify `planning/current_plan.md` is this Layer-1 plan content (verbatim).
5. Verify `planning/current_plan.critique.md` contains the reviewer-adversarial Round 2 verdict (APPROVE or APPROVE-WITH-NITS, 0 blockers). If HOLD-WITH-BLOCKERS, HALT and re-plan.
6. **(NEW Round-2 per A27/NIT #4) Compute Layer-1 critique SHA:** at execution start, after `git fetch origin master`, compute `reviewer_adversarial_layer_1_critique_sha256 = $(sha256sum planning/current_plan.critique.md | awk '{print $1}')` against the merged Layer-1 PR byte state. Verify the file's Round 2 (or final round) verdict is APPROVE or APPROVE-WITH-NITS with 0 blockers; record the verdict text alongside the SHA for use in T04 (notebook elevation rationale) and T03 (test fixtures). Stash the SHA in `.github/tmp/omit_closure_evidence.txt` for T02/T03/T04 reference (this scratch file is NOT committed).
7. Compute and pin the 4 dispatch-time SHAs at execution start:
   - `parent_pr251_csv_sha256 = $(sha256sum src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.csv | awk '{print $1}')`
   - `parent_pr251_md_sha256 = $(sha256sum src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.md | awk '{print $1}')`
   - `parent_pr251_module_sha256 = $(sha256sum src/rts_predict/games/sc2/datasets/sc2egset/decide_history_rating_path.py | awk '{print $1}')`
   - `parent_pr253_roadmap_sha256 = $(sha256sum src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md | awk '{print $1}')`
8. Verify the 11 pinned parent SHAs (PR #242/#243/#245/#247/#249) match A1 verbatim.
9. Re-read Q6H MD §15 verbatim; derive the cross-reference regex; record the regex in `.github/tmp/omit_closure_evidence.txt` scratch file alongside the Layer-1 critique SHA from step 6.
10. (NEW Round-2 per NIT #1) Re-read `decide_history_rating_path.py` lines 442–448 (Branch (ii) reasoning) and lines 457–481 (Branch (iii) preconditions); copy verbatim into `.github/tmp/omit_closure_evidence.txt` for use in T02 (module constants) and T04 (notebook §4.2 generation).

**Verification:**
- `git branch --show-current` outputs `feat/sc2egset-02-01-99-rating-omit-closure-artifact`.
- `pyproject.toml` version is `3.79.0`.
- All 15 SHA pins are 64-char lowercase hex.
- `planning/current_plan.critique.md` Round 2 verdict is APPROVE or APPROVE-WITH-NITS, 0 blockers.
- The Layer-1 critique SHA `reviewer_adversarial_layer_1_critique_sha256` is computed and recorded in `.github/tmp/omit_closure_evidence.txt`.

**File scope:** None (no file writes in T01).

**Routing:** Sonnet executor sufficient.

---

### T02 — Author `close_history_rating_omit_path.py` decision module (Round-2 updated for NITs #1, #3, #4)

**Objective:** Create the closure-side decision module that emits the omit-closure CSV + MD artifact pair, with a deterministic **45-column** schema, a falsifier roll-call, and a `run_close_history_rating_omit_path()` entry point.

**Instructions:**
1. Create `src/rts_predict/games/sc2/datasets/sc2egset/close_history_rating_omit_path.py`.
2. Module docstring: declare the module is a CLOSURE-SIDE decision module (NOT a Q6X adjudication module).
3. Module constants:
   - `OMIT_CLOSURE_SCHEMA: tuple[str, ...]` — exactly **45 column names** in the canonical order from §Future Artifact Contract. Assert `len(OMIT_CLOSURE_SCHEMA) == 45`. (Round-2 update from 42 → 45.)
   - `OMIT_CLOSURE_FIVE_FAMILY_SET: tuple[str, ...]` — imported verbatim from `decide_history_rating_path.Q6H_FIVE_FAMILY_POST_OMIT_SET`.
   - `OMIT_CLOSURE_EXCLUDED_COLUMNS: tuple[str, ...]` = `("reconstructed_rating_focal_pre", "reconstructed_rating_opp_pre", "reconstructed_rating_diff")`.
   - `OMIT_CLOSURE_PARENT_SHA_PINS: dict[str, str]` — the 11 hard-coded parent SHAs from A1.
   - `OMIT_CLOSURE_PR249_CROSS_REF_REGEX: str` = `r'PR #249 §[0-9]+(?:[.][0-9]+)?[a-z]?'`.
   - **(NEW Round-2 per NIT #1)** `OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_TEMPLATE: str` = `"q6h_verdict_state=reached_as_recommendation_only_event_by_event_glicko2;omit_closure_scope_interpretation=blocked_for_phase_02_materialization_scope_under_layer_2_election;is_q6h_re_adjudication=FALSE;is_new_q6x_loop=FALSE"`. Module asserts this template has exactly 4 semicolon-separated key=value pairs.
   - **(NEW Round-2 per NIT #3)** `OMIT_CLOSURE_JACCARD_THRESHOLD: float` = `0.5` (Jaccard `>= 0.5` triggers falsifier).
   - **(NEW Round-2 per NIT #1)** `OMIT_CLOSURE_Q6H_BRANCH_II_LITERAL_LINES: tuple[int, int]` = `(442, 448)` and `OMIT_CLOSURE_Q6H_BRANCH_III_LITERAL_LINES: tuple[int, int]` = `(457, 481)` (for §4.2 quote anchoring).
   - `OMIT_CLOSURE_FALSIFIER_KEYS: tuple[str, ...]` — Round-1 keys plus the 5 new Round-2 keys (see §Falsifier Roll-Call below).
4. Functions:
   - `def _count_sentences(text: str) -> int` — Q6H §15 sentence counter (nltk preferred, regex fallback).
   - `def _count_pr249_cross_references(text: str) -> int` — applies the regex.
   - **(NEW Round-2 per NIT #3)** `def _tokenize_for_jaccard(text: str) -> set[str]`:
     ```python
     import string
     def _tokenize_for_jaccard(text: str) -> set[str]:
         lowered = text.lower()
         stripped = lowered.translate(str.maketrans("", "", string.punctuation))
         tokens = stripped.split()
         return set(tokens)
     ```
   - **(NEW Round-2 per NIT #3)** `def _compute_jaccard(set_a: set[str], set_b: set[str]) -> float`:
     ```python
     def _compute_jaccard(set_a: set[str], set_b: set[str]) -> float:
         if len(set_a | set_b) == 0:
             return 1.0
         return len(set_a & set_b) / len(set_a | set_b)
     ```
   - **(NEW Round-2 per NIT #1)** `def _build_branch_ii_state_anchor() -> str` — returns the template constant (no parameterization; the value is canonical and binding).
   - `def _emit_decision_csv(row: dict[str, str], out_path: Path) -> None` — deterministic CSV writer; the Jaccard float is formatted with `f"{value:.4f}"`.
   - `def _emit_decision_md(rationale: str, q6h_section_15: str, sha_pins: dict[str, str], out_path: Path) -> None` — deterministic MD writer; §4.2 inserts verbatim quotes of `decide_history_rating_path.py` lines 442–448 AND 457–481 (read at notebook time); §19 splits into §19.1 Layer-1 + §19.2 Layer-2 subsections.
   - `def run_close_history_rating_omit_path(output_dir: Path | None = None, *, head_sha: str, parent_sha_pins: dict[str, str], q6h_section_15_text: str, layer1_signoff_sha: str, layer2_signoff_sha: str, elevation_rationale_text: str, q6h_branch_ii_literal: str, q6h_branch_iii_literal: str) -> dict[str, Any]` — main entry point (Round-2: 9 keyword args, +3 over Round-1 — `layer1_signoff_sha`, `q6h_branch_ii_literal`, `q6h_branch_iii_literal`).
5. Falsifier roll-call now includes the 5 new keys (Round-2):
   - `omit_closure_branch_ii_state_anchor_misnamed_or_missing_re_adjudication_assertion` (NEW NIT #1)
   - `omit_closure_reviewer_signoff_layer_1_missing_or_invalid_sha` (NEW NIT #4)
   - `omit_closure_reviewer_signoff_layer_2_missing_or_invalid_sha` (NEW NIT #4)
   - `omit_closure_reviewer_signoff_layer_1_or_layer_2_not_approve_with_zero_blockers` (NEW NIT #4)
   - `omit_closure_elevation_rationale_jaccard_overlap_with_q6h_section_15_exceeds_threshold` (NEW NIT #3)
   - Round-1 keys preserved: `omit_closure_schema_column_count_mismatch`, `omit_closure_five_family_set_drift_from_q6h_constant`, `omit_closure_excluded_columns_drift_from_q6h_literal`, `omit_closure_thesis_pragmatism_not_true`, `omit_closure_thesis_pragmatism_elevation_under_six_sentences`, `omit_closure_q6h_section_15_under_six_sentences`, `omit_closure_pr249_cross_ref_count_under_three_in_elevation`, `omit_closure_pr249_cross_ref_count_under_three_in_q6h_section_15`, `omit_closure_q5_re_adjudication_drift`, `omit_closure_q6f_re_adjudication_drift`, `omit_closure_q6g_re_adjudication_drift`, `omit_closure_q6h_re_adjudication_drift`, `omit_closure_q6h_artifact_sha_mismatch`, `omit_closure_q6h_module_sha_mismatch`, `omit_closure_pr253_roadmap_sha_mismatch`, `omit_closure_parquet_emitted`, `omit_closure_cross_02_01_audit_emitted`, `omit_closure_status_yaml_mutation`, `omit_closure_research_log_mutation`, `omit_closure_roadmap_mutation`, `omit_closure_spec_mutation`, `omit_closure_phase_03_touch`, `omit_closure_step_02_01_04_touch`, `omit_closure_q6x_re_opened`, `omit_closure_q6h_section_15_silently_modified`, `omit_closure_reconstructed_rating_in_five_family_set`, `omit_closure_excluded_family_not_reconstructed_rating`, `omit_closure_five_family_set_size_not_five`, `omit_closure_non_deterministic_emission`, `omit_closure_silent_q6_closure`, `omit_closure_5_family_narrowing_in_this_pr`, `omit_closure_5_family_materialization_in_this_pr`, `omit_closure_parent_sha_not_re_verified_at_dispatch`, `omit_closure_pr249_cross_ref_regex_undocumented`.
6. Type-hint everything; pass `mypy --strict`.
7. Format with `ruff`.

**Verification:**
- `python -c "from rts_predict.games.sc2.datasets.sc2egset.close_history_rating_omit_path import OMIT_CLOSURE_SCHEMA; assert len(OMIT_CLOSURE_SCHEMA) == 45"` passes.
- `python -c "from rts_predict.games.sc2.datasets.sc2egset.close_history_rating_omit_path import OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_TEMPLATE as T; assert T.count(';') == 3 and 'is_q6h_re_adjudication=FALSE' in T and 'is_new_q6x_loop=FALSE' in T"` passes.
- `python -c "from rts_predict.games.sc2.datasets.sc2egset.close_history_rating_omit_path import _tokenize_for_jaccard, _compute_jaccard; a = _tokenize_for_jaccard('Hello world!'); b = _tokenize_for_jaccard('hello universe'); j = _compute_jaccard(a, b); assert 0.0 <= j <= 1.0"` passes.
- `ruff check src/rts_predict/games/sc2/datasets/sc2egset/close_history_rating_omit_path.py` passes.
- `mypy --strict src/rts_predict/games/sc2/datasets/sc2egset/close_history_rating_omit_path.py` passes.

**Routing:** Opus execution required.

---

### T03 — Author mirrored test file `test_close_history_rating_omit_path.py` (Round-2 updated)

**Objective:** Create the mirrored test file. Round-2 updates: `test_omit_closure_schema_column_count` asserts `== 45`; 5 new tests added (one per new falsifier key).

**Instructions:**
1. Create `tests/rts_predict/games/sc2/datasets/sc2egset/test_close_history_rating_omit_path.py`.
2. Implement test categories from §Future Tests Contract. Estimated 55–85 tests.
3. Add the 5 new Round-2 tests:
   - `test_omit_closure_elevation_rationale_jaccard_lt_threshold` (NIT #3): tokenize artifact MD §6 and Q6H §15; compute Jaccard; assert `< 0.5`.
   - `test_omit_closure_branch_ii_state_anchor_format` (NIT #1): parse the column; assert 4 key=value pairs in canonical order with `is_q6h_re_adjudication=FALSE` and `is_new_q6x_loop=FALSE`.
   - `test_reviewer_adversarial_signoff_layer_1_recorded` (NIT #4): assert boolean TRUE and SHA 64-char hex.
   - `test_reviewer_adversarial_signoff_layer_2_recorded` (NIT #4): assert boolean TRUE and SHA 64-char hex.
   - `test_reviewer_signoff_both_layers_zero_blockers` (NIT #4): load critique files; assert both have APPROVE or APPROVE-WITH-NITS with 0 blockers.
4. Use pytest fixtures for 15 SHA pins.
5. Use `tmp_path` fixture for testing `run_close_history_rating_omit_path()`.
6. Type-hint everything; pass `mypy --strict`.

**Verification:**
- `poetry run pytest tests/.../test_close_history_rating_omit_path.py -v` passes 100%.
- `poetry run pytest ... --cov=rts_predict.games.sc2.datasets.sc2egset.close_history_rating_omit_path --cov-report=term-missing` shows ≥95% branch coverage.

**Routing:** Sonnet executor sufficient if T02 module signature is fixed.

---

### T04 — Author sandbox jupytext notebook pair (Round-2 updated for NITs #1, #3, #4)

**Objective:** Create the jupytext-paired notebook. Round-2 updates: the notebook reads Q6H decision-rule literal lines 442–448 and 457–481 for §4.2 (NIT #1); reads BOTH Layer-1 (this PR) and Layer-2 critique files for sign-off SHAs (NIT #4); computes Jaccard before calling `run_close_history_rating_omit_path()` and asserts `< 0.5` (NIT #3).

**Instructions:**
1. Create `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.py`.
2. Notebook cells (in order):
   - `# %% [markdown]`: title + non-batching disclaimer + Q6H §17 verbatim citation + Step 02_01_99 omit-closure scope statement.
   - `# %%`: imports.
   - `# %%`: read Q6H MD §15 verbatim into `q6h_section_15_text`.
   - **(NEW Round-2 per NIT #1)** `# %%`: read `decide_history_rating_path.py` lines 442–448 verbatim into `q6h_branch_ii_literal`; read lines 457–481 verbatim into `q6h_branch_iii_literal`.
   - **(NEW Round-2 per NIT #4)** `# %%`: read the Layer-1 PR's merged-state `planning/current_plan.critique.md` (via `git show <layer_1_merge_sha>:planning/current_plan.critique.md` or directly from the merged byte state) and compute `layer1_signoff_sha = sha256sum(...)`. Verify Round 2 verdict (or final-round verdict) is APPROVE or APPROVE-WITH-NITS with 0 blockers.
   - `# %%`: read this Layer-2 PR's `planning/current_plan.critique.md` and compute `layer2_signoff_sha = sha256sum(critique_path)`.
   - `# %%`: read the head commit SHA.
   - `# %%`: define `elevation_rationale_text` — a Python triple-quoted string with ≥6 sentences and ≥3 cross-references. **(NEW Round-2 per NIT #3) BEFORE calling `run_close_history_rating_omit_path()`, compute Jaccard:**
     ```python
     from rts_predict.games.sc2.datasets.sc2egset.close_history_rating_omit_path import _tokenize_for_jaccard, _compute_jaccard, OMIT_CLOSURE_JACCARD_THRESHOLD
     set_a = _tokenize_for_jaccard(elevation_rationale_text)
     set_b = _tokenize_for_jaccard(q6h_section_15_text)
     jaccard = _compute_jaccard(set_a, set_b)
     assert jaccard < OMIT_CLOSURE_JACCARD_THRESHOLD, f"Jaccard {jaccard:.4f} >= 0.5; rationale is too similar to Q6H §15"
     print(f"Anti-boilerplate check OK: jaccard = {jaccard:.4f} < {OMIT_CLOSURE_JACCARD_THRESHOLD}")
     ```
     If the assertion fires, HALT and revise `elevation_rationale_text` (the rationale is too similar to Q6H §15). Do NOT proceed to artifact emission.
   - `# %%`: build `parent_sha_pins` dict combining 11 hard-coded + 4 dispatch-time SHAs.
   - `# %%`: call `result = run_close_history_rating_omit_path(output_dir=..., head_sha=head_sha, parent_sha_pins=parent_sha_pins, q6h_section_15_text=q6h_section_15_text, layer1_signoff_sha=layer1_signoff_sha, layer2_signoff_sha=layer2_signoff_sha, elevation_rationale_text=elevation_rationale_text, q6h_branch_ii_literal=q6h_branch_ii_literal, q6h_branch_iii_literal=q6h_branch_iii_literal)`.
   - `# %%`: print the falsifier roll-call.
   - `# %%`: print the canonical decision row.
3. Run `jupytext --to ipynb` to generate `.ipynb`; clear outputs.
4. Run the `.py` notebook source as a script to materialize the CSV + MD pair.

**Verification:**
- Notebook outputs include `Anti-boilerplate check OK: jaccard = <value> < 0.5`.
- All 4 artifact files exist (`.py` notebook, `.ipynb` notebook, `.csv`, `.md`).

**Routing:** Opus execution required.

---

### T05 — Verify falsifier roll-call PASS-ALL (Round-2 unchanged from Round 1)

**Objective:** Run the falsifier roll-call against the emitted artifact pair and confirm all falsifiers report `did_not_fire`.

**Instructions:**
1. Run `poetry run pytest tests/.../test_close_history_rating_omit_path.py -v --cov=... --cov-report=term-missing | tee coverage.txt`.
2. Inspect; confirm branch coverage ≥95%; fill gaps.
3. Re-read the emitted artifact MD §12; confirm every falsifier key reports `did_not_fire`.
4. Confirm the artifact CSV's `falsifiers` column lists every key.
5. Delete `coverage.txt`.

**Verification:**
- Test suite passes 100%.
- Coverage ≥95%.
- Artifact MD §12 has ≥35 falsifier rows (30 Round-1 + 5 Round-2), all `did_not_fire`.

**Routing:** Sonnet executor sufficient.

---

### T06 — Append CHANGELOG entry (Round-2 minor update)

**Objective:** Add `[3.80.0]` section.

**Instructions:**
1. Insert `## [3.80.0] — 2026-05-<DD> (PR #<PR_NUMBER>: feat/sc2egset-02-01-99-rating-omit-closure-artifact)` section above `[3.79.0]`.
2. Group changes by `Added` and `Changed`. The Added list MUST include: the 45-column omit-closure CSV/MD pair; the `branch_ii_state_semantic_anchor` semantic-anchor column (Round-2 NIT #1); the dual Layer-1+Layer-2 reviewer sign-off columns (Round-2 NIT #4); the Jaccard anti-boilerplate falsifier (Round-2 NIT #3).
3. Provenance / lineage block: list the 15 SHA pins.
4. Notes block: verbatim "Omit-closure artifact only. NO Parquet, NO CROSS-02-01 audit, NO status YAML flip, NO research_log entry, NO ROADMAP edit, NO Step 02_01_03 closure, NO 5-family ROADMAP narrowing, NO 5-family materialization, NO Step 02_01_04 / Phase 03 work."
5. Move `[Unreleased]` content into `[3.80.0]`.

**Routing:** Sonnet executor sufficient.

---

### T07 — Bump version in `pyproject.toml`

Edit line 3 from `version = "3.79.0"` to `version = "3.80.0"`. Sonnet sufficient.

---

### T08 — Update `planning/INDEX.md`

Archive this Layer-1 PR + the Layer-2 PR; replace active line. Sonnet sufficient.

---

### T09 — Reviewer-adversarial Round 1 (execution-side gate; Round-2 updated for NIT #4 Layer-2 SHA timing)

**Objective:** Dispatch reviewer-adversarial to verify the artifact contents conform to §Future Artifact Contract; verify no out-of-scope file edits; verify the elevation rationale is substantive (not boilerplate); verify ALL hard stops are upheld; verify the falsifier roll-call PASS-ALL. **(Round-2 per A28/NIT #4) After sign-off, compute and pin the Layer-2 critique SHA.**

**Instructions:**
1. Parent session dispatches `reviewer-adversarial` agent with `planning/current_plan.md` path + `planning/current_plan.critique.md` path + `base_ref` (= Layer-1 merge SHA) + diff scope.
2. Reviewer-adversarial verdict goes into `planning/current_plan.critique.md` Round-1 execution-side section.
3. If verdict is APPROVE or APPROVE-WITH-NITS with 0 blockers: proceed to step 4.
4. **(NEW Round-2 per A28/NIT #4) Compute the Layer-2 critique SHA:** after the reviewer-adversarial verdict text is finalized AND committed (or recorded) in `planning/current_plan.critique.md`, compute `reviewer_adversarial_layer_2_critique_sha256 = $(sha256sum planning/current_plan.critique.md | awk '{print $1}')`.
5. **(NEW Round-2) Verify SHA stability via re-emission:** the artifact CSV+MD must record this SHA. Because the sandbox notebook at T04 was executed BEFORE T09 completed, the emitted CSV+MD reference an earlier Layer-2 SHA value (one from a not-yet-signed critique). Therefore, RE-RUN the sandbox notebook at T04 with the new `layer2_signoff_sha`; verify the regenerated CSV+MD have the updated SHA in columns 17–18 and in §19.2; re-run the test suite (T05) to confirm all falsifiers continue to `did_not_fire`. Commit the regenerated CSV+MD with a single commit message "Regenerate artifact after reviewer-adversarial Layer-2 sign-off SHA pin."
6. If verdict is HOLD-WITH-BLOCKERS: HALT; address blockers; re-dispatch reviewer-adversarial Round 2 (per the 3-round cap from `feedback_adversarial_cap_execution.md`). For each subsequent round, the Layer-2 critique SHA evolves; re-run T04 + T05 after the final-round sign-off.
7. **(Practical stop condition)** If after 3 rounds reviewer-adversarial still requires changes, HALT this Layer-2 PR; user decides whether to escalate or re-plan from Layer-1.

**Verification:**
- `planning/current_plan.critique.md` execution-side Round 1 (or 2 or 3) verdict is APPROVE or APPROVE-WITH-NITS with 0 blockers.
- Artifact CSV columns 17–18 and MD §19.2 reflect the final-round critique SHA.
- All falsifiers `did_not_fire` post-regeneration.

**Routing:** Opus (reviewer-adversarial); Opus for T04 re-run (notebook).

---

### T10 — Commit and create PR

**Objective:** Commit the 9-file diff; create a draft PR; do NOT mark ready; do NOT merge.

**Instructions:**
1. `git add` the 9 files explicitly.
2. Write commit message to `.github/tmp/commit.txt` (per `feedback_git_commit_format.md`).
3. `git commit -F .github/tmp/commit.txt`.
4. Write PR body to `.github/tmp/pr.txt` (per `feedback_pr_body_file.md`).
5. `gh pr create --draft --title "feat(sc2egset): Step 02_01_99 rating omit-closure decision artifact (45-column dual-signoff schema)" --body-file .github/tmp/pr.txt`.
6. Delete `.github/tmp/pr.txt` and `.github/tmp/commit.txt`.
7. Return the PR URL to the user.

**Routing:** Sonnet executor sufficient.

## File Manifest

The future Layer-2 PR's 9-file diff:

| File | Action |
|------|--------|
| `src/rts_predict/games/sc2/datasets/sc2egset/close_history_rating_omit_path.py` | Create |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_close_history_rating_omit_path.py` | Create |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.py` | Create |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.ipynb` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.csv` | Create (**45 columns**) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.md` | Create |
| `planning/INDEX.md` | Update |
| `CHANGELOG.md` | Update |
| `pyproject.toml` | Update |

This Layer-1 PR's 2-file diff:

| File | Action |
|------|--------|
| `planning/current_plan.md` | Create / Rewrite (Round 2) |
| `planning/current_plan.critique.md` | Create / Rewrite (Round 2) |

## Lineage & SHA Provenance

The future Layer-2 artifact's `OMIT_CLOSURE_PARENT_SHA_PINS` dict combines:

- **11 hard-coded SHA pins:**
  - `parent_pr242_csv_sha256`, `parent_pr242_md_sha256`
  - `parent_pr243_csv_sha256`, `parent_pr243_md_sha256`
  - `parent_pr245_csv_sha256`, `parent_pr245_md_sha256`
  - `parent_pr247_csv_sha256`, `parent_pr247_md_sha256`
  - `parent_pr249_csv_sha256`, `parent_pr249_md_sha256`
  - (10 SHA-pinned files = 5 PRs × 2 files; plus the 1 head_master SHA = 11 keys in the hard-coded set)

- **4 dispatch-time SHA pins (Round-2 unchanged):**
  - `parent_pr251_csv_sha256` (Q6H CSV)
  - `parent_pr251_md_sha256` (Q6H MD)
  - `parent_pr251_module_sha256` (`decide_history_rating_path.py`)
  - `parent_pr253_roadmap_sha256` (PR #253 merged ROADMAP)

- **NEW Round-2 — 2 sign-off SHA pins (per NIT #4):**
  - `reviewer_adversarial_layer_1_critique_sha256` (computed at Layer-2 T01; A27)
  - `reviewer_adversarial_layer_2_critique_sha256` (computed at Layer-2 T09; A28)

- **1 master HEAD SHA pin** (recorded at Layer-2 execution start): `head_master_sha_at_layer_2_dispatch_time`.

Total provenance SHA pins recorded by the artifact = 15 (file-byte) + 2 (sign-off) = 17 distinct SHA values. Of these, only the CSV columns surface 12 (10 hard-coded file SHAs + 2 dispatch-time Q6H SHAs) plus the 2 sign-off SHAs = **14 SHA columns** in the **45-column** CSV schema; the remaining 3 SHAs (PR #251 module, PR #253 ROADMAP, master HEAD) are recorded in the module constant `OMIT_CLOSURE_PARENT_SHA_PINS` and in MD §20. This Round-2 simplification preserves auditable provenance without bloating the CSV row.

All deterministic 64-char lowercase hex. No `NOT_FOUND` allowed. Falsifier `omit_closure_parent_sha_not_re_verified_at_dispatch` enforces dispatch-time re-verification.

## Reviewer-Adversarial Charter

Reviewer-adversarial Round 2 (planning-side; this Layer-1 PR; planner-side round counter) MUST verify:

1. **All 4 Round-1 nits are correctly baked into Round 2.** The plan must include §Schema Derivation (NIT #2); §Adversarial-Review Adjustments (Round 1 → Round 2); A26–A29; the 5 new falsifier keys; the 4-column sign-off split; the Jaccard column; the semantic-anchor column.
2. **Schema count is exactly 45 in every location where a count appears.** No leftover 42/43/44 except in Round-1-history narrative.
3. **Outcome A is preserved.** Branch (iii) selection; `omit_reconstructed_rating_and_unblock_other_five`; NO Q6X loop.
4. **Compressed Layer-2 9-file scope is justified.** Metadata-only adjudication; no DuckDB read.
5. **Module name `close_history_rating_omit_path.py` is correctly closure-side.**
6. **The 5-family set is canonical from `Q6H_FIVE_FAMILY_POST_OMIT_SET`.**
7. **The future artifact does NOT silently elevate Branch (iii).** Reviewer must verify the Round-2 Jaccard threshold + dual-count discipline + dual-signoff discipline.
8. **OQ7 wording bridge handled via `branch_ii_state_semantic_anchor` column (NIT #1).**
9. **The future artifact does NOT authorise 5-family materialization.**
10. **Q5/Q6F/Q6G/Q6H BINDING verdicts preserved.**
11. **No materialization, no Q6X re-opening, Phase 03 / Step 02_01_04 barred.**
12. **Version bump 3.79.0 → 3.80.0 is SemVer-correct.**
13. **Branch slug `feat/sc2egset-02-01-99-rating-omit-closure-artifact`.**
14. **The Future Tests Contract is implementable.** Estimated 55–85 tests; coverage ≥95% achievable.
15. **No batching of ROADMAP + notebook + artifact + next Step.**
16. **(NEW Round-2) NIT #1 resolution is correctly placed.** Verify column 14 `branch_ii_state_semantic_anchor` exists; verify A26 specifies the canonical 4-key format; verify §4.2 quotes Q6H decision-rule lines 442–448 + 457–481.
17. **(NEW Round-2) NIT #2 resolution is correctly placed.** Verify `## Schema Derivation` section exists between §Future Artifact Contract and §Future Tests Contract; verify ≥1 substantive sentence per deviation (7 deviations).
18. **(NEW Round-2) NIT #3 resolution is correctly placed.** Verify column 13 `elevation_rationale_jaccard_vs_q6h_section_15` (float, `:.4f`); verify A29 specifies the binding mechanics; verify the falsifier key exists; verify T02 has the `_tokenize_for_jaccard` and `_compute_jaccard` functions; verify T03 has `test_omit_closure_elevation_rationale_jaccard_lt_threshold`; verify T04 has pre-emit Jaccard verification.
19. **(NEW Round-2) NIT #4 resolution is correctly placed.** Verify the 4-column dual sign-off split (columns 15–18); verify A23 revised + A27 + A28 added; verify T01 has Layer-1 SHA pinning instruction; verify T09 has Layer-2 SHA pinning instruction and regeneration sequencing; verify §19.1 + §19.2 in artifact MD.

## Gate Condition

This Layer-1 PR's gate (Round 2; observable conditions that confirm the plan is complete):

- `planning/current_plan.md` exists with this verbatim content; conforms to `docs/templates/plan_template.md`; passes the pre-commit `feedback_plan_required_sections.md` hook.
- `planning/current_plan.critique.md` exists with reviewer-adversarial Round 2 verdict APPROVE or APPROVE-WITH-NITS, 0 blockers.
- The PR diff is exactly 2 files.
- No file outside `planning/` is touched.
- No version bump.
- All 4 Round-1 nits are baked in (NIT-1, NIT-2, NIT-3, NIT-4).
- The plan body states schema count = **45** in every binding location.

The future Layer-2 PR's gate (Round-2 updated; observable conditions; verified by reviewer-adversarial at Layer-2 T09):

- The 9-file diff matches the File Manifest exactly.
- `pyproject.toml` version is `3.80.0`.
- `CHANGELOG.md` has a new `[3.80.0]` section; `[Unreleased]` is empty.
- `planning/INDEX.md` archives both Layer-1 and Layer-2 PRs.
- `close_history_rating_omit_path.py` exists with `OMIT_CLOSURE_SCHEMA` of length **45**, `OMIT_CLOSURE_FIVE_FAMILY_SET` of length 5, ≥35-falsifier roll-call (30 Round-1 + 5 Round-2).
- `test_close_history_rating_omit_path.py` passes 100% with ≥95% branch coverage.
- The sandbox notebook pair exists with outputs cleared.
- The omit-closure CSV exists with **45** columns and 1 canonical decision row.
- The omit-closure MD exists with all sections from §Future Artifact Contract incl. §4.2 (Q6H literal quotes) and §19.1 + §19.2 (dual sign-off).
- `decision_row.verdict == "omit_reconstructed_rating_and_unblock_other_five"`.
- `decision_row.thesis_pragmatism == "TRUE"`.
- `decision_row.thesis_pragmatism_sentence_count >= 6`.
- `decision_row.thesis_pragmatism_q6h_section_15_sentence_count >= 6`.
- `decision_row.pr249_cross_reference_count >= 3`.
- `decision_row.pr249_cross_reference_count_q6h_section_15 >= 3`.
- **(NEW Round-2)** `decision_row.elevation_rationale_jaccard_vs_q6h_section_15 < 0.5` (4 decimal places).
- **(NEW Round-2)** `decision_row.branch_ii_state_semantic_anchor` matches the canonical 4-key format from A26.
- **(NEW Round-2)** `decision_row.reviewer_adversarial_signoff_layer_1 == "TRUE"`.
- **(NEW Round-2)** `decision_row.reviewer_adversarial_layer_1_critique_sha256` is 64-char hex.
- **(NEW Round-2)** `decision_row.reviewer_adversarial_signoff_layer_2 == "TRUE"`.
- **(NEW Round-2)** `decision_row.reviewer_adversarial_layer_2_critique_sha256` is 64-char hex.
- `decision_row.q6_omission_status == "intentionally_omitted_under_branch_iii"`.
- `decision_row.q6_not_silently_satisfied == "TRUE"`.
- `decision_row.five_family_set` equals `Q6H_FIVE_FAMILY_POST_OMIT_SET`.
- `decision_row.excluded_family == "reconstructed_rating"`.
- `decision_row.excluded_columns` equals the 3 Q6H literal columns.
- All 12 file-byte SHA columns + 2 sign-off SHA columns are 64-char hex (= 14 SHA columns).
- All ≥35 falsifiers in `OMIT_CLOSURE_FALSIFIER_KEYS` report `did_not_fire`.
- Status YAMLs / research_log / ROADMAP / Q6H artifact pair / `decide_history_rating_path.py` byte-state unchanged from their respective parent merges.
- No Parquet, no CROSS-02-01 audit.
- The Layer-2 PR is created in DRAFT state.

## Out of Scope

(Preserved from Round 1.)

- Step 02_01_03 closure — separate downstream PR.
- Step 02_01_99 closure — separate downstream PR.
- 5-family ROADMAP narrowing — separate downstream PR.
- 5-family materialization Parquet emission — separate downstream PR.
- CROSS-02-01-v1.0.1 post-materialization leakage audit — downstream.
- Step 02_01_04 (in_game_snapshot tranche).
- Phase 03 baseline modeling.
- AoE2 work.
- Thesis chapter prose.
- Spec amendments.
- Cleaning-layer YAML edits.
- New Q6X PRs.
- New rating engine implementations.
- Worldwide-identity migration for `toon_id`.
- Sensitivity sweeps over `rating_period_days`.
- TrueSkill re-implementation.

## Open Questions

(Preserved Round-1 OQ1–OQ7 + 1 noted Round-2 sequencing question OQ8.)

- **OQ1:** Final regex for `PR #249 §X.Y` cross-reference enumeration. Resolves at Layer-2 T02.
- **OQ2:** Sentence tokenizer choice. Resolves at Layer-2 T02.
- **OQ3:** Whether `thesis_pragmatism_elevation_rationale` text is stored in the CSV as a single multi-line cell, in MD §6 only, or both. Resolves at Layer-2 T02. Recommended: MD §6 only.
- **OQ4:** Whether the future 5-family ROADMAP-amendment PR edits Step 02_01_03's existing block or adds a new "Step 02_01_03c" block. Resolves at that PR's own Layer-1 plan time.
- **OQ5:** Whether `q6h_section_15_text` is hard-coded or read dynamically. Resolves at Layer-2 T04. Recommended: dynamic read.
- **OQ6 (resolved 2026-05-27):** Branch slug = `feat/sc2egset-02-01-99-rating-omit-closure-artifact`.
- **OQ7 (resolved 2026-05-27; baked into Round 2 via NIT #1):** Branch (ii) state semantic-anchor wording. Resolved: `branch_ii_state_semantic_anchor` CSV column with the canonical 4-key format from A26; §4.2 in artifact MD quotes Q6H decision-rule literal lines 442–448 + 457–481.
- **OQ8 (NEW Round-2 sequencing nuance):** The Layer-2 sign-off SHA pinning at T09 requires the artifact CSV+MD to be regenerated AFTER the reviewer-adversarial verdict is committed. The notebook re-run in T09 is sequential to reviewer-adversarial verdict commit. If reviewer-adversarial requires Round 2 changes to the Layer-2 PR, the regeneration repeats. Resolves at Layer-2 T09 (operational): the executor re-runs the sandbox notebook with the updated Layer-2 SHA after each round of reviewer-adversarial sign-off; the final regeneration's CSV+MD are committed.

## Rejected Alternatives

(Preserved from Round 1.)

- **B — direct omit-closure artifact execution (no separate Layer-1 plan):** Rejected per non-batching rule.
- **C — ROADMAP scope-amendment planning PR first:** Rejected per PR #253 ROADMAP block continue_predicate.
- **D — five-family materialization planning PR first:** Rejected per PR #253 ROADMAP halt.
- **E — another Q6X PR:** Rejected per PR #251 CHANGELOG and PR #253 ROADMAP halt clause.
- **F — Phase 03 baseline planning:** Rejected per `PHASE_STATUS.yaml` and Phase 02 gate.
- **G — formal blocked-state note:** Rejected (Q6H §17 admits omit-closure as one of two paths).
- **H — hold (predicate inconsistency):** Rejected (repo predicates consistent).

Round-2 also implicitly rejects:

- **I — defer the 4 nits to Layer-2 dispatch:** Rejected. The user explicitly elected to bake the nits into Round 2 to make the Layer-1 plan stand on its own without Layer-2 amendments.
- **J — tighter Jaccard threshold (e.g., 0.3):** Rejected for Round 2. Threshold 0.5 is the conservative ceiling for paraphrase-likely overlap; tightening could be revisited in a downstream PR if Layer-2 evidence shows §6 reliably scores `<< 0.5`.
- **K — merge sign-off SHA into a single dual-purpose column:** Rejected. The user explicitly required the 4-column split (booleans + SHAs) for inspectability.

## Planner-side Self-Critique

(Self-identified weaknesses for reviewer-adversarial to probe.)

- **S-1 — Is the omit-closure artifact truly the next atomic unit after PR #253?** Counter: Q-chain precedent compresses non-batching steps 2–7 for metadata-only adjudications; reviewer-adversarial-approved each time.
- **S-2 — Does the Layer-2 PR risk silent Branch (iii) selection if the elevation rationale is thin?** Counter (Round-2 strengthened): the Jaccard `< 0.5` falsifier (A29) plus the dual-count discipline (A22) plus the dual-signoff discipline (A23/A27/A28) provide three independent structural guardrails on top of the reviewer-adversarial substantive guardrail. Boilerplate that passes sentence count would still fail at least one of Jaccard / cross-reference count / reviewer review.
- **S-3 — Does the OQ7 reframing risk subtle Q6H re-adjudication?** Counter (Round-2 strengthened via NIT #1): the `branch_ii_state_semantic_anchor` column makes the distinction grep-able with a canonical 4-key format including explicit `is_q6h_re_adjudication=FALSE` and `is_new_q6x_loop=FALSE` assertions; §4.2 quotes Q6H decision-rule literal lines 442–448 + 457–481 verbatim. The reviewer can grep for "is_q6h_re_adjudication=FALSE" to confirm.
- **S-4 — Is module name `close_history_rating_omit_path.py` correctly non-Q6X-coded?** Counter: prefix `close_*` is the standard library naming convention for closure-side operations.
- **S-5 — Is the 5-family set complete and correct?** Counter: imported verbatim; assert `len == 5` + `"reconstructed_rating" not in`.
- **S-6 — Does the future artifact correctly state that a SEPARATE ROADMAP scope-amendment PR and a SEPARATE materialization-plan PR are downstream?** Counter: artifact MD §13 + §14 + CSV columns `future_roadmap_scope_amendment_required` + `future_materialization_pr_required`.
- **S-7 — Is the version bump 3.79.0 → 3.80.0 correct?** Counter: feat-family (new module, artifact, test, notebook).
- **S-8 — Branch-slug choice rationale.** Counter: canonical `02-01-99` form per `docs/TAXONOMY.md`.
- **S-9 (NEW Round-2 per NIT #1) — Could the `branch_ii_state_semantic_anchor` column inadvertently look like a Q6H re-adjudication assertion?** A reviewer may argue that a string column claiming "blocked_for_phase_02_materialization_scope_under_layer_2_election" makes a scope-claim that effectively re-interprets Q6H's verdict. Counter-argument: the column value explicitly asserts `is_q6h_re_adjudication=FALSE` and `is_new_q6x_loop=FALSE` in its own canonical format, and §4.2 quotes the Q6H decision-rule literal verbatim. The column is a SCOPE statement (about how the omit-closure artifact interprets the Q6H Branch (ii) verdict for the Phase-02 materialization scope), not a verdict statement. The falsifier `omit_closure_branch_ii_state_anchor_misnamed_or_missing_re_adjudication_assertion` enforces format compliance. Reviewer-adversarial in Round 2 should grep the column value byte-for-byte against A26.
- **S-10 (NEW Round-2 per NIT #4) — Is the dual sign-off discipline operationally feasible given the sequencing constraint that T09 modifies the critique file?** A reviewer may argue that pinning a Layer-2 SHA at T09 creates a chicken-and-egg problem: the artifact CSV must reference a SHA over a file that is being modified during the artifact's audit. Counter-argument: the T09 instructions (Round-2 updated) explicitly mandate notebook re-run after each reviewer-adversarial round; the regenerated CSV+MD reference the latest critique SHA; this is precedented (Q-chain Layer-2 PRs do the same when reviewer-adversarial requests changes). The 3-round cap on reviewer-adversarial bounds the maximum number of regenerations to 3. OQ8 acknowledges the operational nuance.
- **S-11 (NEW Round-2 per NIT #3) — Is the Jaccard threshold 0.5 the right choice?** A reviewer may argue that 0.5 is too lenient (could allow substantial paraphrase) or too strict (could fire on genuinely independent rationales that happen to use technical jargon shared with Q6H §15 like "Glicko-2" and "rating_period_days"). Counter-argument: at the token level after lowercase + punctuation strip, technical jargon contributes ~5-15 unique tokens to a multi-sentence rationale; even if all are shared, the per-token overlap for a 50-100-unique-token rationale would be <= 0.3 at most. The 0.5 threshold is a safety net against copy-paste (which would yield Jaccard ≥0.8). Round-2 also leaves J in the rejected-alternatives list (tightening to 0.3) for a possible downstream PR if empirical evidence justifies it. The threshold is documented in A29 and §Schema Derivation Deviation 1.

## Adversarial-Review Adjustments (Round 1 → Round 2)

Round 1 of this Layer-1 plan was reviewed by reviewer-adversarial on 2026-05-27 and received the verdict **APPROVE-WITH-NITS** (0 blockers, 4 non-blocking nits). The user elected to bake all 4 nits into Round 2 BEFORE Layer-1 materialization, rather than deferring them to Layer-2 dispatch. This section is a Round-2-only record of the changes.

### Round 1 baseline

- Schema column count: 42.
- Falsifier roll-call: 30 keys.
- Reviewer sign-off: 1 column (`reviewer_adversarial_signoff_critique_sha256`); 1 boolean (`reviewer_adversarial_signoff`).
- Branch (ii) state: handled via prose in §4 + A4 + OQ7; no falsifier-checkable row field.
- Boilerplate prevention: only sentence count + cross-reference count thresholds; no token-overlap measure.
- Schema derivation: no per-column derivation paragraph.

### Round 2 deltas

- **NIT #1 baked in** (`branch_ii_state_semantic_anchor` column + A26 + §4.2 Q6H literal quote + falsifier `omit_closure_branch_ii_state_anchor_misnamed_or_missing_re_adjudication_assertion`).
- **NIT #2 baked in** (`## Schema Derivation` section + per-column derivation paragraphs reproduced in MD §11).
- **NIT #3 baked in** (`elevation_rationale_jaccard_vs_q6h_section_15` column + A29 + Jaccard functions in T02 + Jaccard test in T03 + pre-emit Jaccard verification in T04 + falsifier `omit_closure_elevation_rationale_jaccard_overlap_with_q6h_section_15_exceeds_threshold`).
- **NIT #4 baked in** (4-column dual sign-off split: `reviewer_adversarial_signoff_layer_1`, `reviewer_adversarial_layer_1_critique_sha256`, `reviewer_adversarial_signoff_layer_2`, `reviewer_adversarial_layer_2_critique_sha256` + A23 revised + A27 + A28 + T01 Layer-1 SHA pinning + T09 Layer-2 SHA pinning with regeneration sequencing + §19.1 + §19.2 + 3 new falsifiers: `omit_closure_reviewer_signoff_layer_1_missing_or_invalid_sha`, `omit_closure_reviewer_signoff_layer_2_missing_or_invalid_sha`, `omit_closure_reviewer_signoff_layer_1_or_layer_2_not_approve_with_zero_blockers`).

### Schema column count progression

- Round 1: 42 columns.
- Round 2: 42 + 1 (NIT #1) + 2 (NIT #4 net: 2 → 4) + 1 (NIT #3) = **45 columns**.

### Falsifier roll-call progression

- Round 1: 30 keys.
- Round 2: 30 + 5 (NIT #1: 1; NIT #3: 1; NIT #4: 3) = **35 keys**.

### New BINDING assumptions (Round 2)

- A26: Branch (ii) state semantic anchor recording (NIT #1).
- A27: Layer-1 SHA timing (NIT #4).
- A28: Layer-2 SHA timing (NIT #4).
- A29: Anti-boilerplate Jaccard discipline (NIT #3).

### New self-critique items (Round 2)

- S-9: Risk of misreading `branch_ii_state_semantic_anchor` as Q6H re-adjudication.
- S-10: Sequencing feasibility of dual sign-off SHA pinning.
- S-11: Jaccard threshold calibration.

### Preserved methodology

Outcome A; NO ROADMAP edit in Layer-1 PR; NO artifact/module/test/notebook/materialization in Layer-1 PR; NO Q6X loop; Q5/Q6F/Q6G/Q6H parent decisions preserved; future Layer-2 artifact selects `omit_reconstructed_rating_and_unblock_other_five` only after Branch (iii) preconditions are met (now augmented by the Jaccard observable and the dual sign-off); Q6 intentionally omitted, not silently satisfied; Phase 03 barred.

### Outcome justification

Round 1 received APPROVE-WITH-NITS (0 blockers). All 4 nits are non-blocking — i.e., they could have been deferred to Layer-2 dispatch without altering Outcome A. The user elected to bake them in for Round 2 because:

1. **Stronger structural guardrails** — Round 2 adds three new falsifier keys (NIT #4) and one new Jaccard falsifier (NIT #3) and one semantic-anchor falsifier (NIT #1). These augment the Round-1 30-key roll-call to a Round-2 35-key roll-call, making the Layer-2 artifact more resilient to subtle drift.
2. **Better grep-ability** — the Round-2 `branch_ii_state_semantic_anchor` column makes the OQ7 distinction grep-able with a canonical 4-key format, instead of requiring readers to parse §4 prose.
3. **Dual sign-off audit trail** — splitting the single SHA into Layer-1 + Layer-2 pairs creates a clear chronological audit trail from planning critique (Layer-1) to execution critique (Layer-2). Each is independently inspectable.
4. **Schema rationale transparency** — `## Schema Derivation` makes each non-Q6H column traceable to its reviewer concern, preventing future drift in the schema rationale.
5. **Layer-1 stand-alone strength** — baking the nits into Round 2 makes the Layer-1 plan stand on its own without Layer-2 amendments; reviewer-adversarial Round-2 (planning-side) can verify the plan against all 45 columns + 35 falsifiers in one pass.

Outcome A is unchanged.

---

## Critique instruction for parent session

For Category A, adversarial critique is required before execution begins. Dispatch `reviewer-adversarial` to produce `planning/current_plan.critique.md` Round-2 verdict (APPROVE / APPROVE-WITH-NITS / HOLD-WITH-BLOCKERS), axis-by-axis assessment, and Round-2 blockers/nits/notes. The 3-round adversarial cap applies (planning-side); Rounds 2 (this round) and Round 3 (if needed) are reserved for the 4 baked-in nits and any newly-discovered issues.

The execution-side reviewer-adversarial gate (Layer-2 PR T09) inherits a fresh 3-round adversarial cap per `feedback_adversarial_cap_execution.md` (symmetric to planning-side).

