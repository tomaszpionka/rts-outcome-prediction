---
title: "SC2EGSet Step 02_03_01 ADJUDICATION (Layer-1 planning PR; Q1-Q8 binding decisions for temporal-window/decay/cold-start grid)"
category: A
branch: feat/sc2egset-02-03-01-temporal-adjudication-plan
base_ref: master
base_sha: 846a8ece127dd9b4c119f226008969019d7ddd8e
predecessor_pr: 278
predecessor_pr_merge_sha: 846a8ece127dd9b4c119f226008969019d7ddd8e
predecessor_pr_layer: V3-scaffold
dataset: sc2egset
phase: "02"
pipeline_section: "02_03 — Temporal Features, Windows, Decay, Cold Starts"
invariants_touched: [I3, I5, I6, I7, I8, I9, I10]
draft_pr_files:
  - planning/current_plan.md
  - planning/current_plan.critique.md
future_execution_files:
  - src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_temporal_feature_grid.py
  - tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_temporal_feature_grid.py
  - sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_adjudication.py
  - sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_adjudication.ipynb
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/02_03_01_temporal_feature_grid_adjudication.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/02_03_01_temporal_feature_grid_adjudication.md
  - pyproject.toml
  - CHANGELOG.md
  - planning/INDEX.md
future_execution_file_count: 9
future_execution_pyproject_bump: "3.89.0 -> 3.90.0"
critique_required: true
research_log_ref: null
date: 2026-05-31
v1_predecessor_pr: 276
v1_predecessor_sha: 37c3a8855af038bd1bd4eefbdbd03497da323d47
v3_predecessor_pr: 278
v3_predecessor_sha: 846a8ece127dd9b4c119f226008969019d7ddd8e
scaffold_rungs_satisfied: [V1, V3]
adjudication_direct_rejected: true
reviewer_adversarial_round1: PROCEDURAL-HOLD
reviewer_adversarial_blockers: 0
reviewer_adversarial_nits: 4
nits_applied: [N-1, N-2, N-3, N-4]
carry_forwards_from_pr277: [A-15, H6, H7]
branch_model_clarification: "Layer-2 lands on NEW branch feat/sc2egset-02-03-01-temporal-adjudication-execution"
amendment_pr: "chore/sc2egset-02-03-01-adjudication-plan-provenance-amendment"
amendment_base_sha: "5764d524a5aa02a3e242485cd949873725b806c5"
amendment_fixes_applied: [Fix-1, Fix-2, Fix-3, Fix-4, Fix-5, Fix-6, NIT-A1, NIT-A2, NIT-A3, NIT-A4, NIT-A5, NIT-A6]
amendment_round1_verdict: "HOLD-PROCEDURAL; 0 substantive BLOCKERs; 6 NIT-A fixes applied inline"
---

## Scope

Author the Layer-1 planning artefact for the future Layer-2 **ADJUDICATION execution PR** for Step `02_03_01` — temporal-window / decay / cold-start grid adjudication. Both scaffold rungs have merged:

- **V1 scaffold** (PR #276, merged at master `37c3a8855af038bd1bd4eefbdbd03497da323d47`): SHA-pin predecessor artifact provenance validator.
- **V3 scaffold** (PR #278, merged at master `846a8ece127dd9b4c119f226008969019d7ddd8e`): strict-`<` temporal-discipline validator (`validate_temporal_discipline.py`).

The ROADMAP `continue_predicate` cascade now permits adjudication: both scaffold rungs are complete, and no further scaffold rung is required before adjudication.

**This Layer-1 planning PR** writes exactly two files:
1. `planning/current_plan.md` (this document).
2. `planning/current_plan.critique.md` (reviewer-adversarial Round 1 output — scaffold for Round 2).

**Adjudication-direct REJECTED.** The adjudication PR must NOT bypass V1 + V3 preflight gates at Layer-2 execution time. Even though both scaffold modules exist in the codebase, the Layer-2 adjudication execution PR must invoke V1 (`validate_temporal_feature_grid.py`) and V3 (`validate_temporal_discipline.py`) as preflight gates before the adjudicator logic executes. Both must return `PASS` before the grid adjudication proceeds.

**Out of scope (adjudication design surface — declared here, enforced by Layer-2 falsifiers):**

- Pinning concrete numerical winners for Q1 (temporal window sizes), Q2 (decay half-life values), or Q3 (cold-start k-thresholds) — Layer-1 describes family KINDS; Layer-2 (materialization PR) pins numerical WINNERS per Invariant I7.
- Any feature materialization (no Parquet outputs, no DuckDB writes).
- Any artifact emission to `reports/artifacts/02_feature_engineering/03_temporal_features/**`.
- Any ROADMAP / STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS / dataset research_log / root research_log edits.
- Phase 03 activation or baseline modeling.
- Any empirical AoE2 transferability claim.
- Any tracker_events family activation beyond what is already declared eligible in `tracker_events_feature_eligibility.csv`.
- Any in-game snapshot feature engineering (deferred past `02_03_01` adjudication scope boundary; see Q5).

## Problem Statement

Step `02_03_01` is the first temporal-features step in Pipeline Section `02_03`. The V1 and V3 scaffold rungs established:

- V1 (`validate_temporal_feature_grid.py`): the predecessor artifact provenance validator that audits SHA-pin existence, identity columns, and row counts of the four predecessor Parquet/CSV artifacts.
- V3 (`validate_temporal_discipline.py`): the strict-`<` temporal-discipline validator that audits schema-level naming convention, temporal-anchor presence (`started_at: timestamp[us]`), and cite-string provenance (6 verbatim cite-strings from CROSS-02-03-v1.0.1 §1.2 D1-D6).

With both scaffold rungs in place, the adjudication step selects the candidate temporal window families, decay families, and cold-start families for the `02_03_01` feature grid. The adjudication module (`adjudicate_temporal_feature_grid.py`) is a decision-record module: it does not compute feature values. It records:

1. Which temporal window types (family kinds) are included, excluded, or deferred.
2. Which decay types (family kinds) are included, excluded, or deferred.
3. Which cold-start types (family kinds) are included, excluded, or deferred.
4. Which tracker_events families are in-scope for `02_03_01` (constrained by `tracker_events_feature_eligibility.csv`).
5. Whether in-game snapshot features are within `02_03_01` scope or deferred to a later step.
6. That CROSS-02-02 and CROSS-02-03 roles are non-conflated (family inventory vs post-selection audit predicate).
7. That V1 + V3 preflight gates passed before adjudication proceeded.
8. That cross-game portability is syntactic-only (no empirical AoE2 transferability claim).

The adjudication module emits a structured decision CSV (`02_03_01_temporal_feature_grid_adjudication.csv`) and a decision Markdown report (`02_03_01_temporal_feature_grid_adjudication.md`) to `reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/`. These are the first materialised artifacts for Pipeline Section `02_03`.

## Literature Context

The three LOCKED cross-dataset specs governing Pipeline Section `02_03` are:

- **CROSS-02-00-v3.0.1** (LOCKED 2026-04-26; `reports/specs/02_00_feature_input_contract.md`): feature input contract; per-dataset I3 anchors; column-level classification.
- **CROSS-02-02-v1.0.1** (LOCKED 2026-05-06; `reports/specs/02_02_feature_engineering_plan.md`): cross-dataset feature engineering plan; lists candidate temporal window / decay / cold-start family kinds (§6, §9); leakage check table G-L-1 through G-L-7 (§10).
- **CROSS-02-03-v1.0.1** (LOCKED 2026-05-06; `reports/specs/02_03_temporal_feature_audit_protocol.md`): design-time temporal feature audit protocol; audit dimensions D1–D15 (§4); per-dataset temporal anchor table (§5); prediction-setting rules (§6); SC2 tracker constraints (§7).

**CROSS-02-02 §10 (G-L-1 through G-L-7) supplies the candidate family inventory.** G-L-1 through G-L-7 are the seven leakage-check rows that enumerate the leakage-relevant family dimensions. The adjudicator cites these rows verbatim as its inventory source. CROSS-02-02 is the source of candidate family KINDS; it is not the post-selection audit predicate.

**CROSS-02-03 §4 (D5, D6, D7) supplies the post-selection audit predicate.** Dimensions D5 (cutoff operator correctness), D6 (target-game exclusion), and D7 (post-game token exclusion) are the three design-time audit dimensions that the adjudicator must cite when recording its selection rationale. CROSS-02-03 is the source of audit predicates; it is not the family inventory.

**CROSS-02-02 = source of candidate family inventory; CROSS-02-03 = source of post-selection audit predicate. These are distinct roles.**

**Invariant I3 (Invariant I3: strict history cutoff).** The project-wide temporal discipline invariant mandates `history_time < T` strictly (not `<=`) for all history features targeting game T. The V3 scaffold (`validate_temporal_discipline.py`) enforces this at schema level. The adjudicator must cite Invariant I3 in its decision record for every family kind that has a history cutoff.

**Q8 cross-game portability.** The adjudicator module is scoped to SC2EGSet decision records only. Cross-game portability of the adjudicator design pattern is restricted to a syntactic-only observation: where the adjudicator uses candidate-agnostic vocabulary (focal/opponent, history, prior, target-exclusion, candidate, winner, window-type, decay-type, cold-start-type) rather than game-specific names, the design pattern is portable. No empirical AoE2 transferability claim is made; that determination is deferred to a future AoE2-specific Phase 02 step. This is verifiable by grep falsifiers H6 (cross-game-portable vocabulary) and H7 (Q8 syntactic-only guard) at Layer-2 execution.

**Version bump precedent.** PR #278 (`3.88.0 → 3.89.0`, minor feat-class scaffold) and PR #276 (`3.87.0 → 3.88.0`, minor feat-class scaffold) confirm the feat-class minor-bump rule for scaffold rungs. The adjudication execution PR is also feat-class (first artifact-producing step in `02_03`); target bump: `3.89.0 → 3.90.0` (minor per `.claude/rules/git-workflow.md` feat-class rule).

**Per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical work"**: scaffold declares scope and delivers one validation module per pass. The adjudication PR delivers the adjudicator module (one module) + decision artifacts; it does NOT deliver feature materialisation or model training.

## Assumptions & Unknowns

**A-1. Both scaffold rung SHAs confirmed.** V1 (PR #276) merged at master `37c3a8855af038bd1bd4eefbdbd03497da323d47`. V3 (PR #278) merged at master `846a8ece127dd9b4c119f226008969019d7ddd8e`. Layer-2 T01 must verify both SHAs before construction.

**A-2. V1 and V3 module byte-stability.** Both `validate_temporal_feature_grid.py` (V1) and `validate_temporal_discipline.py` (V3) are byte-stable between Layer-1 merge and Layer-2 merge. The adjudicator must NOT modify either module (per V1 docstring separation clause and V3 design contract). Layer-2 T01 must verify both module SHAs are unchanged before constructing the adjudicator.

**A-3. pyproject version baseline.** `pyproject.toml` declares `version = "3.89.0"` (post-PR #278). Layer-2 target bump: `3.89.0 → 3.90.0` (minor per `.claude/rules/git-workflow.md` feat-class rule; mirrors PR #278 `3.88.0 → 3.89.0` and PR #276 `3.87.0 → 3.88.0`).

**A-4. Adjudicator module scope (decision record; no feature computation).** The adjudicator module shipped in the Layer-2 execution PR:

- Invokes V1 preflight via `validate_predecessor_artifact_provenance(repo_root)` (from `rts_predict.games.sc2.datasets.sc2egset.validate_temporal_feature_grid`, returning `ProvenanceCheckResult`) and V3 preflight via `validate_temporal_discipline(repo_root)` (from `rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline`, returning `TemporalDisciplineCheckResult`) before any adjudication logic. Both must return `PASS`; on failure, the adjudicator halts with a structured error.
- Records family-kind decisions (window-type, decay-type, cold-start-type) for the SC2EGSet `02_03_01` feature grid.
- Emits a structured decision CSV and a decision Markdown report to `reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/`.
- Does NOT compute any feature values. Does NOT query DuckDB. Does NOT read from `data/**`.
- Does NOT pin concrete numerical winners (no integer literals for game counts, day counts, half-life values, or k-thresholds in module logic per Invariant I7).
- Returns a typed result object (dataclass or NamedTuple) with `v1_preflight`, `v3_preflight`, `window_families`, `decay_families`, `cold_start_families`, `tracker_families_included`, `in_game_deferred`, `cross_spec_citations` fields.
- Uses cross-game-portable vocabulary only in public function signatures and return-type fields.

**A-5. V1 and V3 preflight gates are REQUIRED at execution.** The adjudicator must run V1 (`validate_predecessor_artifact_provenance(repo_root)`) and V3 (`validate_temporal_discipline(repo_root)`) as preflight checks before adjudication logic begins. A V1 PASS + V3 PASS result is required. If either fails, the adjudicator returns a halting result without emitting artifacts. This is the structural operationalisation of Q7 binding.

**A-6. tracker_events_feature_eligibility.csv constrains Q4 scope.** The file at `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv` is the authoritative constraint on which tracker_events families may be included in `02_03_01`. The adjudicator reads this CSV to enumerate eligible families; it does not override or extend eligibility decisions.

**A-7. PIPELINE_SECTION_STATUS NOT touched.** No `02_03` row added or modified by the adjudication PR. The first-step-closure rule applies; `02_03` row is added only when the full section closes.

**A-8. STEP_STATUS NOT touched.** No `02_03_01` row added by the adjudication PR. The `02_03_01` row is added only when the step closes (after materialization + leakage audit + U2.B closure PR).

**A-9. PHASE_STATUS.yaml NOT touched.** Phase 02 stays `in_progress`; Phase 03 stays `not_started`. No PHASE_STATUS row added or modified by the Layer-2 adjudication execution PR. Phase 02 closure (and Phase 03 readiness) require future U2.B-style closure PR(s) downstream of adjudication + materialization rungs.

**A-10. planning/INDEX.md edits.** Three coupled edits at Layer-2:

1. **Active line rewrite.** Replace the current Active line (describing the V3 scaffold Layer-2 PR #278) with the new Active line for the adjudication execution PR on `feat/sc2egset-02-03-01-temporal-adjudication-execution`. Required content: adjudication scope; "no ROADMAP / status YAML / research_log / Phase 03"; version bump `3.89.0 → 3.90.0`; future PR number placeholder `PR #<TBD>`.
2. **Archive PR #278.** Insert a new row in the archive table for PR #278 (Layer-2 V3 scaffold for `02_03_01`; merge SHA `846a8ece`; date 2026-05-31; Category A).
3. **Archive this Layer-1 planning PR.** Insert a new row for this Layer-1 adjudication planning PR at its own merge SHA (set after this PR merges). Per A-16, the Layer-2 PR itself MUST NOT be archived by its own planning/INDEX.md edit (honest-lineage rule).

**A-11. CHANGELOG block.** New `## [3.90.0] — <date> (PR #<TBD>: feat/sc2egset-02-03-01-temporal-adjudication-execution)` block inserted above the existing `## [3.89.0]` block. Block must contain `### Added` bullet for the adjudicator module + decision artifacts and `### Notes` bullets (`**No feature materialization.**`, `**No STEP_STATUS row.**`, `**No PIPELINE_SECTION_STATUS row.**`, `**No PHASE_STATUS mutation.**`, `**No research_log entry.**`, `**No ROADMAP edit.**`, `**No Phase 03.**`, `**No baseline modeling.**`, `**No concrete numerical window sizes, decay half-lives, or cold-start k-thresholds pinned.**`).

**A-12. Decision artifacts grain and path.** The adjudicator emits exactly two artifacts to `reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/`:

- `02_03_01_temporal_feature_grid_adjudication.csv` — structured decision table; minimum 16 columns. Required base columns (7, unchanged): `family_kind`, `decision` (included/excluded/deferred), `rationale_g_l_ref`, `rationale_d_ref`, `invariant_i3_cited`, `v1_preflight`, `v3_preflight`. Required provenance/SHA columns (9, NEW): `parent_02_01_02_parquet_sha256`, `parent_02_01_03_parquet_sha256`, `parent_02_01_99_csv_sha256`, `parent_02_02_01_parquet_sha256`, `v1_validator_module_sha256`, `v3_validator_module_sha256`, `cross_02_02_spec_sha256`, `cross_02_03_spec_sha256`, `tracker_eligibility_csv_sha256`.

  SHA-pin column values (hex literals embedded in EVERY row by the adjudicator):
  - `parent_02_01_02_parquet_sha256` = `24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39`
  - `parent_02_01_03_parquet_sha256` = `053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071`
  - `parent_02_01_99_csv_sha256` = `831a622c6e0a98c9642e466d5c9dced0fb6b621a6d58e3008a1b0218dd03c370`
  - `parent_02_02_01_parquet_sha256` = `c4b48601ee0ff800f4b823af270faf03571a637ce07c51a0ef6d072691896ff3`
  - `v1_validator_module_sha256` = computed by adjudicator at execution time via `hashlib.sha256` on `validate_temporal_feature_grid.py` bytes; embedded in every row (NIT-A1: precise label `v1_validator_module_sha256`)
  - `v3_validator_module_sha256` = computed by adjudicator at execution time via `hashlib.sha256` on `validate_temporal_discipline.py` bytes; embedded in every row (NIT-A1: precise label `v3_validator_module_sha256`)
  - `cross_02_02_spec_sha256` = `86af792370272e611f048aae0c48c9cc595eb4b44c1db38c0bb4ecea0ff1b289`
  - `cross_02_03_spec_sha256` = `59e3227307c51ad09fb12b485caec36aa54413d175cb46acc382c06fbb8ac546`
  - `tracker_eligibility_csv_sha256` = `11bd4b9ef7c80657a027db3831313c1d74c39b85834c25ecdfa78506e8ad8d22`

  The adjudicator computes the V1 and V3 module SHA256 values at execution time via `hashlib.sha256` and embeds them in EVERY row of the decision CSV, providing byte-stable, auditable evidence of the exact validator module versions used during adjudication.

- `02_03_01_temporal_feature_grid_adjudication.md` — decision Markdown report; 14 sections including §6 (15-family cross-reference table: one row per row in `tracker_events_feature_eligibility.csv`); includes verbatim citations of CROSS-02-02 §10 G-L-1 through G-L-7, CROSS-02-03 §4 D5/D6/D7, and Invariant I3.

**A-13. No coverage gate impact for Layer-1.** Pre-commit hooks (`ruff` + `mypy`) run on `.py` file changes. The Layer-2 adjudication PR adds `.py` files; pytest coverage must be ≥ 35 tests and ≥ 95% branch coverage on the adjudicator module. The Layer-1 planning PR (this PR) touches zero `.py` files; no pytest run required.

**A-14. tracker_events_feature_eligibility.csv byte-stability.** The file at `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv` is byte-stable between Layer-1 merge and Layer-2 merge. If the file mutates, the Layer-2 PR halts before push.

**A-15 (cross-game-portable vocabulary; carried verbatim from PR #277 plan).** The Layer-2 adjudicator module's PUBLIC function signatures + return-type dataclass field names + CSV column names use cross-game-portable vocabulary ONLY (focal/opponent, history, prior, target-exclusion, candidate, winner, window-type, decay-type, cold-start-type). SC2-specific tokens (race, tracker_events, PlayerStats, mineral, vespene, toon_id, apm, sq) and AoE2-specific tokens (civilization, civ, profile_id, leaderboard) MUST NOT appear in public API. SC2-specific tokens MAY appear in MD prose as instance-specific references with verbatim "SC2-specific:" prefix per PR #275 N4 convention. No empirical AoE2 transferability claim is made; deferred to future AoE2-specific Phase 02 step.

**A-16 (PR-self-archive forbidden; PR #278 Round 2 carry-forward).** The Layer-2 adjudication execution PR's `planning/INDEX.md` edit must NOT include an archive row for itself. The Layer-2 PR archives ONLY: (a) PR #278 (V3 scaffold) at merge SHA `846a8ece127dd9b4c119f226008969019d7ddd8e`, AND (b) this Layer-1 adjudication planning PR at its own merge SHA (set after THIS PR merges). The Layer-2 PR's OWN archive row is added by a SUBSEQUENT PR per honest-lineage rule from PR #278 Round 2 BLOCKER remediation. No future-PR-self-archive row permitted in any `planning/INDEX.md` edit; this is a project-wide invariant established by PR #278 force-rewrite.

**Unknowns** (resolved at Layer-2 T01, not at Layer-1):

- **U-1.** The exact date of the Layer-2 adjudication execution PR merge (enters CHANGELOG date header and planning/INDEX archive row).
- **U-2.** Exact prose for the decision CSV rationale cells (bound by CROSS-02-02 §10 G-L-* and CROSS-02-03 §4 D5/D6/D7; exact prose drafted at Layer-2 T01).
- **U-3.** Exact tracker_events family inclusion list (read from `tracker_events_feature_eligibility.csv` at Layer-2 T01; not to be pre-resolved here).
- **U-4.** Whether in-game snapshot features are deferred entirely past `02_03_01` or deferred to a sub-step within `02_03_01`. Boundary resolved at Layer-2 T01 per Q5 direction (default: deferred past `02_03_01`).

## Execution Steps

The future Layer-2 adjudication execution PR executes the following tasks based off `master@846a8ece127dd9b4c119f226008969019d7ddd8e`. Each task is a delegated executor step.

**T01 — Verify base state (Sonnet executor).**

- Verify `git rev-parse master == 846a8ece127dd9b4c119f226008969019d7ddd8e`.
- Verify `pyproject.toml` `version = "3.89.0"`.
- Verify STEP_STATUS has `02_02_01: complete` row; `02_03_01` row is absent (not yet closed).
- Verify PIPELINE_SECTION_STATUS has `02_02: complete` row; `02_03` row is absent.
- Verify PHASE_STATUS Phase 02 `in_progress` / Phase 03 `not_started`.
- Verify ROADMAP.md has `02_03_01` block.
- Verify `validate_temporal_feature_grid.py` (V1) exists at canonical path.
- Verify `validate_temporal_discipline.py` (V3) exists at canonical path.
- Verify `adjudicate_temporal_feature_grid.py` does NOT yet exist (adjudicator creates it fresh).
- Verify `tracker_events_feature_eligibility.csv` exists at canonical path.
- Record V1 module SHA and V3 module SHA (for byte-stability check in T02).

Stop condition: any precondition fails → HALT, escalate to user.

Allowed files: NONE for write — Read-only verification only.

Required validation report: short summary echoing the 11 verifications including V1 SHA and V3 SHA recorded.

**T02 — Create adjudicator module (Opus executor; V1+V3 preflight integration + decision record).**

Allowed files:
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_temporal_feature_grid.py`.

Forbidden files: ALL others. Explicitly forbidden: `validate_temporal_feature_grid.py` (V1; must remain byte-stable) and `validate_temporal_discipline.py` (V3; must remain byte-stable).

**Note: T02 requires Opus execution.** The adjudicator integrates V1 and V3 preflight gate semantics, binds CROSS-02-02 §10 G-L-1 through G-L-7 verbatim, and cites CROSS-02-03 §4 D5/D6/D7 as post-selection audit predicates. This integration requires subtle reasoning about spec roles (CROSS-02-02 = inventory; CROSS-02-03 = audit predicate) and cross-game vocabulary discipline. Sonnet executor is insufficient for T02; Opus execution is required.

Create the adjudicator decision-record module. Module must:

- Invoke V1 preflight (`from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_feature_grid import validate_predecessor_artifact_provenance, ProvenanceCheckResult` → call `validate_predecessor_artifact_provenance(repo_root)`) and V3 preflight (`from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import validate_temporal_discipline, TemporalDisciplineCheckResult` → call `validate_temporal_discipline(repo_root)`) as first operations.
- Halt (structured error result) if either preflight returns non-PASS.
- Record family-kind decisions for window-type, decay-type, and cold-start-type families; no concrete numerical winners.
- Cite CROSS-02-02 §10 G-L-1 through G-L-7 verbatim in module docstring as the family-inventory source.
- Cite CROSS-02-03 §4 D5, D6, D7 verbatim in module docstring as the post-selection audit predicates.
- Cite Invariant I3 verbatim in module docstring.
- Use cross-game-portable vocabulary only in public function signatures, return-type dataclass fields, and CSV column names (per A-15).
- Emit decision CSV and decision MD to `reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/` (create directory if absent).
- Return a typed result object with `v1_preflight`, `v3_preflight`, `window_families`, `decay_families`, `cold_start_families`, `tracker_families_included`, `in_game_deferred`, `cross_spec_citations` fields.

**Adjudication sequence (binding, first-failure-halt):**

```
1. invoke V1 preflight (validate_predecessor_artifact_provenance(repo_root))
2. invoke V3 preflight (validate_temporal_discipline(repo_root))
3. check both v1.passed AND v3.passed; if either False, halt with AdjudicationResult(passed=False, halt_at=H1_or_H2)
4. capture all 9 SHA-pin values (4 parent artifacts + V1 module + V3 module + 2 CROSS specs + tracker CSV)
5. create outputs directory (.../03_temporal_features/02_03_01/) ONLY after preflight PASS
6. emit decision CSV (16-column schema, 9 rows for Q4 source_event_family categories + Q1-Q3+Q5-Q8 rows)
7. emit decision MD (14 sections including §6 15-family tracker cross-reference)
8. return AdjudicationResult; no further writes (no research_log, no status YAML, no spec edits)
```

The outputs directory (step 5) MUST NOT be created if either preflight fails (ordering hazard guard). Post-emission closure (step 8): after returning `AdjudicationResult`, the adjudicator performs no further writes. No research_log entry, no STEP_STATUS row, no spec edits.

Stop condition: module modifies V1 or V3 → HALT; module pins concrete numerical grid values → HALT; module uses forbidden vocabulary in public API → HALT; outputs directory created before preflight PASS → HALT.

Required validation report: `grep -n 'V1 PASS' src/.../adjudicate_temporal_feature_grid.py` returns ≥1; `grep -n 'V3 PASS' src/.../adjudicate_temporal_feature_grid.py` returns ≥1; `grep -n 'G-L-1' src/.../adjudicate_temporal_feature_grid.py` returns ≥1; `grep -n 'D5' src/.../adjudicate_temporal_feature_grid.py` returns ≥1; `grep -n 'Invariant I3' src/.../adjudicate_temporal_feature_grid.py` returns ≥1.

**T03 — Create mirrored test module (Sonnet executor).**

Allowed files:
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_temporal_feature_grid.py`.

Forbidden files: ALL others. Explicitly forbidden: V1 and V3 test modules (must remain byte-stable).

Create the mirrored test module. Tests must:

- Cover ≥ 35 tests with ≥ 95% branch coverage on `adjudicate_temporal_feature_grid.py`.
- Include V1 preflight PASS / FAIL controls.
- Include V3 preflight PASS / FAIL controls.
- Include a test asserting that halting on V1 failure returns no emitted artifacts.
- Include a test asserting that halting on V3 failure returns no emitted artifacts.
- Include a test asserting the decision CSV column names use cross-game-portable vocabulary only (H6 structural enforcement at test layer).
- Include a test asserting no concrete numerical grid values appear in decision CSV rows.
- Include tests for each declared family-kind decision (window-type, decay-type, cold-start-type included/excluded/deferred variants).
- Use `pytest.mark.parametrize` for boundary sweep tests.

Stop condition: any file outside allowed list touched; coverage below 95% → HALT.

Required validation report: `poetry run pytest tests/.../test_adjudicate_temporal_feature_grid.py -v --cov=rts_predict --cov-report=term-missing` passes with ≥ 35 tests, ≥ 95% branch coverage.

**T04 — Create jupytext-paired notebook scaffold (Sonnet executor).**

Allowed files:
- `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_adjudication.py`
- `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_adjudication.ipynb`

Forbidden files: ALL others.

Create the jupytext `py:percent` scaffold notebook. Notebook must:

- Follow sandbox/README.md hard rules: no inline definitions, 50-line cell cap, read-only DuckDB, jupytext percent-format.
- Declare hypothesis + falsifier + sanity-check up front in Markdown cells.
- Invoke the adjudicator (T02) and assert the result is a PASS result with `v1_preflight='PASS'` and `v3_preflight='PASS'`.
- Confirm the decision CSV and decision MD are emitted to the correct path.
- Use `print()` for exploration output (not `logger`).
- NOT contain any `def`, `class`, or `lambda` in cells.

Stop condition: notebook defines functions in cells; notebook claims empirical AoE2 transferability → HALT.

Required validation report: `jupytext --to notebook` produces a valid `.ipynb`; `nbconvert --execute` passes with no errors.

**T05 — Bump pyproject.toml (Sonnet executor).**

Allowed files:
- `pyproject.toml`.

Edit: `version = "3.89.0"` → `version = "3.90.0"` (line 3; minor per feat-class rule).

Stop condition: any unintended file change → HALT.

Required validation report: `git diff pyproject.toml` shows only the version line change.

**T06 — Add CHANGELOG.md [3.90.0] block (Sonnet executor).**

Allowed files:
- `CHANGELOG.md`.

Insert `## [3.90.0] — <date> (PR #<TBD>: feat/sc2egset-02-03-01-temporal-adjudication-execution)` block between the existing `[Unreleased]` section and the existing `## [3.89.0]` block. Block content per A-11.

Stop condition: any unintended file change → HALT.

Required validation report: `git diff CHANGELOG.md` shows the new `[3.90.0]` block inserted above `[3.89.0]`; the `[Unreleased]` section and `[3.89.0]` block are byte-unchanged.

**T07 — Update planning/INDEX.md (Sonnet executor).**

Allowed files:
- `planning/INDEX.md`.

Three coupled edits per A-10:

1. Replace the current Active line with the new Active line for the Layer-2 adjudication execution PR.
2. Insert a new archive row for PR #278 (V3 scaffold; merge SHA `846a8ece`).
3. Insert a new archive row for this Layer-1 adjudication planning PR (merge SHA set after this PR merges; to be resolved at Layer-2 T07 from `gh pr view <N> --json mergeCommit`).

Per A-16: do NOT insert an archive row for the Layer-2 execution PR itself.

Stop condition: any unintended file change → HALT; archive row for Layer-2 PR itself present → HALT.

Required validation report: `git diff planning/INDEX.md` shows the three intended edits and nothing else; `grep -n '846a8ece' planning/INDEX.md` returns the PR #278 archive row.

**T08 — Local checks and wrap-up (Sonnet executor).**

Required checks:

- `git diff --stat master..HEAD` shows exactly 9 files in the manifest (see §File Manifest).
- `grep -nE '^## ' planning/current_plan.md | wc -l` returns 8.
- No forbidden vocabulary in adjudicator or test: H6 falsifier returns zero matches in public function signatures and return-type fields.
- H7 falsifier returns zero matches in adjudicator source, test, notebook, and decision MD.
- Coverage: `poetry run pytest tests/.../test_adjudicate_temporal_feature_grid.py --cov=rts_predict --cov-report=term-missing` → ≥ 35 tests, ≥ 95% branch coverage.
- No status YAML diff: `git diff --stat master..HEAD -- '**/STEP_STATUS.yaml' '**/PIPELINE_SECTION_STATUS.yaml' '**/PHASE_STATUS.yaml'` returns empty.
- No research_log diff: `git diff --stat master..HEAD -- '**/research_log.md'` returns empty.
- No ROADMAP diff: `git diff --stat master..HEAD -- 'src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md'` returns empty.
- V1 byte-stability: `git diff --stat master..HEAD -- 'src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_feature_grid.py'` returns empty.
- V3 byte-stability: `git diff --stat master..HEAD -- 'src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_discipline.py'` returns empty.
- No A-16 violation: `grep -n 'feat/sc2egset-02-03-01-temporal-adjudication-execution' planning/INDEX.md | grep -v 'Active'` — the only match for the Layer-2 execution branch name should be in the Active line, not in an archive row for itself.
- V1 PASS + V3 PASS grep: `grep -cF 'V1 PASS' src/.../adjudicate_temporal_feature_grid.py` ≥ 1 AND `grep -cF 'V3 PASS' src/.../adjudicate_temporal_feature_grid.py` ≥ 1.

Stop condition: any check fails → HALT.

Required validation report: short summary echoing all checks; ready for commit/PR.

## File Manifest

This Layer-1 planning PR diff = exactly 2 files:
- `planning/current_plan.md` (this file)
- `planning/current_plan.critique.md` (reviewer-adversarial Round 1 scaffold)

**Branch model for Layer-2 adjudication execution PR (binding):**

Layer-2 adjudication execution PR will land on a NEW branch (NOT the same branch as this Layer-1 planning PR), mirroring the V3 scaffold branch-model precedent from PR #275 → PR #276 and PR #277 → PR #278. Under this NEW-branch model, the 2 planning files (`planning/current_plan.md` + `planning/current_plan.critique.md`) are NOT re-included in the Layer-2 diff because they will already have merged to master when this Layer-1 PR merges. Therefore Layer-2 diff = exactly 9 files (9-file diff: the 6 execution-class files + pyproject + CHANGELOG + INDEX). This differs from PR #234/#242's 11-file same-branch-reuse model where planning files are re-committed in the Layer-2 diff.

Layer-2 branch name (proposed): `feat/sc2egset-02-03-01-temporal-adjudication-execution` (sibling to this Layer-1 branch; distinct from V3 scaffold branches).

The future Layer-2 adjudication execution PR diff = exactly 9 files:

| File | Action | Notes |
|---|---|---|
| `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_temporal_feature_grid.py` | Create | Adjudicator decision-record module. V1 + V3 preflight integration. Family-kind decisions (window-type, decay-type, cold-start-type). CROSS-02-02 §10 G-L-1 through G-L-7 verbatim cited. CROSS-02-03 §4 D5/D6/D7 verbatim cited. Invariant I3 verbatim cited. Cross-game-portable vocabulary only in public API. No concrete numerical winners. |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_temporal_feature_grid.py` | Create | Mirrored test module. ≥ 35 tests, ≥ 95% branch coverage. V1/V3 preflight PASS/FAIL controls. Vocabulary guard test (H6 structural). No-numerical-winners test. |
| `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_adjudication.py` | Create | Jupytext `py:percent` scaffold. Hypothesis + falsifier declaration cells. Adjudicator invocation. Preflight PASS assertion. Decision CSV path confirmation. |
| `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_adjudication.ipynb` | Create | Paired `.ipynb`. Outputs cleared before commit. Executes end-to-end via nbconvert with no errors. |
| `reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/02_03_01_temporal_feature_grid_adjudication.csv` | Create | Decision CSV. Grain: one row per family-kind decision (9 rows for Q4 source_event_family categories: PlayerSetup, PlayerStats, UnitBorn, UnitDied, UnitInit/UnitDone, UnitOwnerChange, UnitPositions, UnitTypeChange, Upgrade; plus Q1-Q3 + Q5-Q8 rows). Minimum 16 columns: 7 base (`family_kind`, `decision`, `rationale_g_l_ref`, `rationale_d_ref`, `invariant_i3_cited`, `v1_preflight`, `v3_preflight`) + 9 SHA-pin provenance columns (`parent_02_01_02_parquet_sha256`, `parent_02_01_03_parquet_sha256`, `parent_02_01_99_csv_sha256`, `parent_02_02_01_parquet_sha256`, `v1_validator_module_sha256`, `v3_validator_module_sha256`, `cross_02_02_spec_sha256`, `cross_02_03_spec_sha256`, `tracker_eligibility_csv_sha256`). No concrete numerical winners in rows. |
| `reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/02_03_01_temporal_feature_grid_adjudication.md` | Create | Decision Markdown report. 14 sections including §6 (15-family tracker cross-reference table, one row per tracker_events_feature_eligibility.csv row). Verbatim CROSS-02-02 §10 G-L-1 through G-L-7 citations. Verbatim CROSS-02-03 §4 D5/D6/D7 citations. Invariant I3 citation. V1 + V3 preflight PASS records. |
| `pyproject.toml` | Update | Version `3.89.0 → 3.90.0` (minor; feat-class adjudication precedent). |
| `CHANGELOG.md` | Update | Insert `## [3.90.0]` block between `[Unreleased]` and `[3.89.0]`. |
| `planning/INDEX.md` | Update | Active line rewrite + archive PR #278 row + archive this Layer-1 PR row. Per A-16: NO self-archive row for the Layer-2 execution PR. |

**Files that MUST remain byte-unchanged in Layer-2 (binding negative-space contract):**
- src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
- src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
- src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml
- src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml
- src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
- reports/research_log.md
- src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_feature_grid.py (V1; byte-stable per A-2)
- src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_discipline.py (V3; byte-stable per A-2)
- src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv
- reports/specs/02_00_feature_input_contract.md
- reports/specs/02_01_leakage_audit_protocol.md
- reports/specs/02_02_feature_engineering_plan.md
- reports/specs/02_03_temporal_feature_audit_protocol.md (CROSS-02-03 LOCKED 2026-05-06)
- docs/**
- .claude/**
- data/**
- src/rts_predict/games/aoe2/**
- thesis/**

## Gate Condition

The Layer-1 planning PR (this PR) is acceptable for merge when all of the following hold:

**G1.** `git diff --name-only HEAD` (relative to master) shows EXACTLY:
- `planning/current_plan.md`
- `planning/current_plan.critique.md`

**G2.** 8 required H2 headings literal match: `grep -cE '^## (Scope|Execution Steps|File Manifest|Problem Statement|Assumptions & Unknowns|Literature Context|Gate Condition|Open Questions)$' planning/current_plan.md` must equal 8.

**G3.** Both scaffold rungs cited: `grep -F '846a8ece' planning/current_plan.md` returns ≥ 1 match (V3 SHA) AND `grep -F '37c3a8855' planning/current_plan.md` returns ≥ 1 match (V1 SHA).

**G4.** Q7 V1 + V3 preflight binding: `grep -F 'V1 PASS' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'V3 PASS' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'preflight' planning/current_plan.md` returns ≥ 1 match.

**G5.** Adjudication-direct rejected: `grep -F 'Adjudication-direct REJECTED' planning/current_plan.md` returns ≥ 1 match.

**G6.** CROSS-02-02 vs CROSS-02-03 non-conflation: `grep -F 'CROSS-02-02 = source of candidate family inventory; CROSS-02-03 = source of post-selection audit predicate. These are distinct roles.' planning/current_plan.md` returns ≥ 1 match.

**G7.** Invariant I3 cited: `grep -F 'Invariant I3' planning/current_plan.md` returns ≥ 1 match.

**G8.** I7 no-magic-numbers (Layer-1 plan-layer): `grep -nE '\b(7|10|14|20|30|60|90|180)\s*(games?|days?|d|matches?)\b|half[_-]life\s*=|k\s*=\s*[0-9]+' planning/current_plan.md` returns zero matches OUTSIDE §Open Questions and §Out-of-scope.

**G9.** A-15 vocabulary: `grep -F 'A-15' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'cross-game-portable vocabulary' planning/current_plan.md` returns ≥ 1 match.

**G10.** A-16 PR-self-archive forbidden: `grep -F 'A-16' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'PR-self-archive forbidden' planning/current_plan.md` returns ≥ 1 match AND `grep -F '846a8ece127dd9b4c119f226008969019d7ddd8e' planning/current_plan.md` returns ≥ 1 match.

**G11.** Round 2 re-gate trigger: `grep -F 'Round 2' planning/current_plan.md` returns ≥ 1 match.

**G12 (Fix 5 + NIT-A5 — sequence + closure):** `grep -F 'invoke V1 preflight' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'invoke V3 preflight' planning/current_plan.md` returns ≥ 1 match AND `grep -F 'return AdjudicationResult; no further writes' planning/current_plan.md` returns ≥ 1 match.

**G13 (Fix 1 + NIT-A1 — 16-column CSV schema):** `grep -F 'parent_02_01_02_parquet_sha256' planning/current_plan.md` returns ≥ 1 AND `grep -F 'v1_validator_module_sha256' planning/current_plan.md` returns ≥ 1 AND `grep -F 'v3_validator_module_sha256' planning/current_plan.md` returns ≥ 1 AND `grep -F 'cross_02_02_spec_sha256' planning/current_plan.md` returns ≥ 1 AND `grep -F 'tracker_eligibility_csv_sha256' planning/current_plan.md` returns ≥ 1.

**G14 (Fix 2 + NIT-A2 — 9-category Q4 grain):** `grep -F '9 distinct source_event_family categories per direct enumeration' planning/current_plan.md` returns ≥ 1 AND each of the 9 categories (PlayerSetup, PlayerStats, UnitBorn, UnitDied, UnitInit/UnitDone, UnitOwnerChange, UnitPositions, UnitTypeChange, Upgrade) returns ≥ 1 match.

**G15 (Fix 3 + NIT-A3 — actual repo symbols):** All shorthand module-level invocations replaced with actual repo symbols (`validate_predecessor_artifact_provenance(repo_root)` for V1 and `validate_temporal_discipline(repo_root)` for V3). `grep -F 'validate_predecessor_artifact_provenance(repo_root' planning/current_plan.md` returns ≥ 1 AND `grep -F 'validate_temporal_discipline(repo_root' planning/current_plan.md` returns ≥ 1.

**G16 (Fix 4 + NIT-A4 — 9-step halt chain):** `grep -F 'H7a' planning/current_plan.md` returns ≥ 1 AND `grep -F 'H7b' planning/current_plan.md` returns ≥ 1 AND each of H0, H1, H2, H3, H4, H5, H6 present.

**G17 (Fix 6 + NIT-A6 — .ipynb in H7 grep):** `grep -F '02_03_01_adjudication.ipynb' planning/current_plan.md` returns ≥ 1.

**Layer-2 plan-text grep falsifier predicates (binding):**

The future Layer-2 adjudication execution PR's `planning/current_plan.md` (Layer-2 plan) MUST satisfy the following grep predicates as a structural requirement of Q7 binding:

- `grep -F 'V1 PASS' planning/current_plan.md` — must return ≥1 match (Q7 preflight requirement).
- `grep -F 'V3 PASS' planning/current_plan.md` — must return ≥1 match (Q7 preflight requirement).
- `grep -F 'G-L-1' planning/current_plan.md` AND `grep -F 'G-L-2' planning/current_plan.md` AND `grep -F 'G-L-3' planning/current_plan.md` AND `grep -F 'G-L-4' planning/current_plan.md` AND `grep -F 'G-L-5' planning/current_plan.md` AND `grep -F 'G-L-6' planning/current_plan.md` AND `grep -F 'G-L-7' planning/current_plan.md` — each must return ≥1 match (CROSS-02-02 §10 verbatim cited).
- `grep -F 'D5' planning/current_plan.md` AND `grep -F 'D6' planning/current_plan.md` AND `grep -F 'D7' planning/current_plan.md` — each must return ≥1 match (CROSS-02-03 §4 verbatim cited).
- `grep -F 'Invariant I3' planning/current_plan.md` — must return ≥1 match.
- `grep -F 'preflight' planning/current_plan.md` — must return ≥1 match (V1+V3 as preflight gates).

Failure of any predicate = Q7 binding is paper-only (narrative-only); halt Layer-2 dispatch and re-author Q7.

**Layer-1 plan-layer I7 enforcement (no concrete numerical winners):**

The Layer-1 plan MUST NOT pin concrete numerical winners. Per Invariant I7 (no magic numbers without empirical-derivation or cited literature precedent), Q1-Q3 enumerate family kinds (window-type, decay-type, cold-start-type); winner selection (concrete N games, M days, τ half-life, K threshold, m pseudocount) is DEFERRED to the future materialization PR.

Grep falsifier predicate (Layer-1 plan-layer):

`grep -nE '\b(7|10|14|20|30|60|90|180)\s*(games?|days?|d|matches?)\b|half[_-]life\s*=|k\s*=\s*[0-9]+' planning/current_plan.md`

— must return zero matches OUTSIDE the §Open Questions section and §Out-of-scope subsection. Matches inside these sections (as illustrative examples of what NOT to commit) are permitted.

Layer-1 describes family KINDS. Layer-2 (materialization PR) pins numerical WINNERS.

**Layer-2 falsifier predicates carried from PR #277 plan (binding):**

- **H6 (cross-game-portable vocabulary; from V3 plan):** `grep -niE 'race|tracker_events|PlayerStats|mineral|vespene|toon_id|apm_focal|apm_opp|sq_focal|sq_opp|civilization|civ_|profile_id|leaderboard' src/.../adjudicate_temporal_feature_grid.py tests/.../test_adjudicate_temporal_feature_grid.py` — every match (if any) must be in forbidden-list constants (analogous to V3's `FORBIDDEN_SC2_TERMS` / `FORBIDDEN_AOE2_TERMS`) or in MD prose with verbatim "SC2-specific:" prefix. Public function signatures + return-type dataclass field names + CSV column names MUST return zero matches.

- **H7 (Q8 syntactic-only guard; from V3 plan; NIT-A6: extended to include .ipynb):**

  H7 grep target list (extended to include paired notebook):
  - `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_temporal_feature_grid.py`
  - `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_temporal_feature_grid.py`
  - `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_adjudication.py`
  - `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_adjudication.ipynb`   (NIT-A6: NEW)
  - `reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/02_03_01_temporal_feature_grid_adjudication.md`

  `grep -niE 'aoe2.*transferab|transferab.*aoe2|validated on aoe2|aoe2.*verified|cross-game validated'` across all 5 targets — must return ZERO matches. No empirical AoE2 transferability claim permitted in adjudicator source, test, notebook (.py and .ipynb), or decision MD. AoE2 transferability deferred to future AoE2-specific Phase 02 step (syntactic-only structural reusability is acceptable but cannot be empirically claimed).

**Adjudicator halt-priority chain (9 steps, first-failure-wins; binding for Layer-2 T02):**

The adjudicator module must check the following conditions in strict order, halting at the first failure and returning an `AdjudicationResult` with `passed=False` and the failing halt identifier:

```
H0 base/path preconditions (repo_root valid; relative paths per Invariant I10)
H1 V1 preflight failure (validate_predecessor_artifact_provenance returns passed=False)
H2 V3 preflight failure (validate_temporal_discipline returns passed=False)
H3 parent/spec/tracker SHA capture failure (file unreadable for hashlib.sha256)
H4 tracker eligibility CSV read failure
H5 forbidden concrete numeric winners / I7 violation in decision CSV
H6 Q8 syntactic-only / vocabulary failure (H6 grep + H7 grep)
H7a forbidden output dir present (paradox guard; V1.H6 + V3.H5 binding)
H7b PR-self-archive forbidden (A-16 binding; no self-row in planning/INDEX.md)
```

**Additional Layer-2 halt conditions:**

**LG1.** `git diff --stat master..HEAD` shows exactly 9 files matching the §File Manifest.

**LG2.** `poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_temporal_feature_grid.py --cov=rts_predict --cov-report=term-missing` passes with ≥ 35 tests, ≥ 95% branch coverage.

**LG3.** `grep -cF 'V1 PASS' src/.../adjudicate_temporal_feature_grid.py` ≥ 1 AND `grep -cF 'V3 PASS' src/.../adjudicate_temporal_feature_grid.py` ≥ 1.

**LG4.** `grep -cE '^## \[3\.90\.0\]' CHANGELOG.md` returns 1.

**LG5.** `grep 'version' pyproject.toml | head -1` returns `version = "3.90.0"`.

**LG6.** `git diff --stat master..HEAD -- '**/STEP_STATUS.yaml' '**/PIPELINE_SECTION_STATUS.yaml' '**/PHASE_STATUS.yaml' '**/research_log.md' 'src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md' 'reports/research_log.md' 'src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/**' 'src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_feature_grid.py' 'src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_discipline.py'` returns empty.

**LG7.** H6 + H7 falsifiers pass on adjudicator and test files (cross-game-portable vocabulary; no AoE2 empirical claim).

**LG8.** A-16 check: `grep -n 'feat/sc2egset-02-03-01-temporal-adjudication-execution' planning/INDEX.md | grep -v 'Active'` — zero archive rows match the Layer-2 execution branch name (no self-archive).

**Round 2 trigger:** If the materialized Layer-1 plan fails any of G1-G11 or the H6/H7 grep falsifiers, escalate to reviewer-adversarial Round 2. 3-round cap per `feedback_adversarial_cap_execution.md`.

## Open Questions

**Q1 — Temporal window type selection (family kinds; DEFERRED — Layer-1 enumerates kinds, not winners).** CROSS-02-02 §6 lists temporal window candidate families for SC2EGSet: fixed-game-count windows, fixed-calendar-duration windows, and exponential-decay windows. The adjudication step enumerates which kinds are included in the `02_03_01` feature grid candidate set. Concrete winner selection (specific game counts, specific day counts, specific half-life values) is DEFERRED to the future materialization PR per Invariant I7. Plan default: enumerate window-type KINDS in decision CSV; mark concrete values as DEFERRED.

**Q2 — Decay type selection (family kinds; DEFERRED — Layer-1 enumerates kinds, not winners).** CROSS-02-02 §6 lists exponential decay and step-function decay as candidate families. The adjudicator records which decay kinds are in scope. Concrete τ half-life values or step sizes are NOT pinned at adjudication; they are DEFERRED to materialization per Invariant I7. Plan default: enumerate decay-type KINDS; mark numerical values as DEFERRED.

**Q3 — Cold-start k-threshold selection (family kinds; DEFERRED — Layer-1 enumerates kinds, not winners).** CROSS-02-02 §9 defines cold-start handling gates. The adjudicator records which cold-start kind is selected (minimum-prior gate vs pseudocount smoothing vs both). Concrete k-threshold values and pseudocount magnitudes are NOT pinned at adjudication; DEFERRED to materialization per Invariant I7. Plan default: enumerate cold-start-type KIND; mark numerical values as DEFERRED.

**Q4 — tracker_events family scope.** `tracker_events_feature_eligibility.csv` constrains which tracker families are eligible for `02_03_01`. The adjudicator reads this CSV and includes only rows marked `eligible_for_phase02_now` or `eligible_with_caveat` (with caveat honoured). Blocked families remain excluded. Plan default: adjudicator enumerates eligible tracker families from the CSV; no manual override of eligibility decisions.

9 distinct source_event_family categories per direct enumeration of tracker_events_feature_eligibility.csv column 2: PlayerSetup, PlayerStats, UnitBorn, UnitDied, UnitInit/UnitDone, UnitOwnerChange, UnitPositions, UnitTypeChange, Upgrade.

The decision CSV body contains 9 rows for the Q4 source_event_family categories (one row per category), plus rows for Q1-Q3 and Q5-Q8 decisions. The decision Markdown report §6 contains a 15-family cross-reference table (one row per row in `tracker_events_feature_eligibility.csv`, cross-referencing each eligibility CSV row to the adjudicator's decision). No manual override of eligibility decisions.

**Q5 — In-game snapshot scope.** CROSS-02-03 §6.3 defines the `in_game_snapshot` prediction setting. Whether `02_03_01` includes in-game snapshot families or defers them entirely to a later step is a boundary question. Plan default: in-game snapshot families are DEFERRED past `02_03_01` (the `02_03_01` adjudication step covers `pre_game` and `history_enriched_pre_game` prediction settings only). In-game snapshot adjudication proceeds in a later step. This boundary is recorded in the decision CSV with `decision=deferred` and `rationale_d_ref=D5/D6/D7 (deferred pending in-game loop cutoff architecture)`.

**Q6 — CROSS-02-02 vs CROSS-02-03 non-conflation (binding resolved at Layer-1).** The adjudicator cites CROSS-02-02 §10 G-L-1 through G-L-7 as the candidate FAMILY INVENTORY source and CROSS-02-03 §4 D5/D6/D7 as the POST-SELECTION AUDIT PREDICATE source. These roles MUST NOT be conflated. The adjudicator module docstring must include the verbatim clause: "CROSS-02-02 = source of candidate family inventory; CROSS-02-03 = source of post-selection audit predicate. These are distinct roles."

**Q7 — V1 + V3 preflight as gate (binding resolved at Layer-1).** The adjudicator module MUST invoke V1 preflight (`validate_predecessor_artifact_provenance(repo_root)`, imported from `rts_predict.games.sc2.datasets.sc2egset.validate_temporal_feature_grid`) and V3 preflight (`validate_temporal_discipline(repo_root)`, imported from `rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline`) as the FIRST two operations before any adjudication logic. Both must return PASS (`ProvenanceCheckResult.passed == True` and `TemporalDisciplineCheckResult.passed == True`). On failure, the adjudicator returns a halting result with the failing preflight identifier. This is the structural operationalisation of the ROADMAP `continue_predicate` cascade at execution time. The Layer-2 plan body must contain `V1 PASS` and `V3 PASS` grep anchors per the binding Layer-2 plan-text grep falsifier predicates in §Gate Condition.

Adjudicator main entrypoint: `validate_temporal_feature_grid_adjudication(repo_root: Path) -> AdjudicationResult`

**Q8 — Cross-game portability (syntactic-only; binding resolved at Layer-1).** The adjudicator design pattern is syntactically portable (uses cross-game-portable vocabulary in public API). No empirical AoE2 transferability claim is made or permitted. The adjudicator module, test, notebook, and decision MD must not contain any string matching `aoe2.*transferab`, `transferab.*aoe2`, `validated on aoe2`, `aoe2.*verified`, or `cross-game validated` (H7 falsifier). AoE2 transferability is deferred to a future AoE2-specific Phase 02 step.

## Reviewer-adversarial Round 1 verdict (Layer-1 materialisation)

Round 1 verdict: **PROCEDURAL HOLD — substantive 0 blockers, 4 NITs applied inline (PR #279 merge).** All 4 NITs (N-1 through N-4) applied inline. Carry-forwards from PR #277 plan (A-15, H6, H7) applied verbatim. Branch-model clarification applied inline.

**Amendment (this PR — chore/sc2egset-02-03-01-adjudication-plan-provenance-amendment):** Round 1 reviewer-adversarial returned HOLD-PROCEDURAL with 0 substantive BLOCKERs + 6 NIT-A1..A6 fixes (CSV provenance BLOCKER + 3 NITs + 2 NOTEs). All 12 fixes (6 planner + 6 NIT-A) applied inline in this amendment. Round 2 will run against materialized text.

| # | Severity | Concern | Fix applied in plan body |
|---|---|---|---|
| **N-1** | NIT | Q7 verbatim grep predicates absent from §Gate Condition | §Gate Condition now includes "Layer-2 plan-text grep falsifier predicates (binding)" subsection with concrete grep predicates for V1 PASS, V3 PASS, G-L-1 through G-L-7, D5/D6/D7, Invariant I3, and preflight. Failure of any predicate = Q7 binding is paper-only; halt Layer-2 dispatch. |
| **N-2** | NIT | Q6 CROSS-02-02 vs CROSS-02-03 non-conflation clause absent | §Open Questions Q6, §Literature Context, and §Problem Statement all include verbatim clause: "CROSS-02-02 = source of candidate family inventory; CROSS-02-03 = source of post-selection audit predicate. These are distinct roles." §Gate Condition G6 binds this as a grep predicate. |
| **N-3** | NIT | I7 plan-layer enforcement (no magic numbers) absent from §Gate Condition | §Gate Condition now includes "Layer-1 plan-layer I7 enforcement (no concrete numerical winners)" subsection with grep falsifier predicate. Q1-Q3 explicitly enumerate family kinds, not winners. The grep falsifier is also applied as G8. |
| **N-4** | NIT | PR-self-archive forbidden (A-16; PR #278 Round 2 carry-forward) absent | §Assumptions & Unknowns now includes A-16 verbatim binding. §File Manifest T07 annotation forbids Layer-2 self-archive. §Gate Condition G10 binds A-16 presence as a grep predicate. |
| **NIT-A1** | NIT | CSV columns 8-16 (SHA-pin provenance) absent from A-12; labels `v1_validator_module_sha256` / `v3_validator_module_sha256` unspecified | A-12 expanded from 7 to 16+ columns. 9 SHA-pin columns added with precise labels (`v1_validator_module_sha256`, `v3_validator_module_sha256`) and hex-literal values for the 7 fixed-artifact SHAs. V1/V3 module SHAs computed at execution time via `hashlib.sha256`. File Manifest CSV row updated. G13 gate predicate added. |
| **NIT-A2** | NIT | Q4 grain unspecified: "9 categories" asserted but no literal list | Q4 Open Question now contains literal sorted list of 9 source_event_family categories per direct enumeration of tracker_events_feature_eligibility.csv column 2. MD §6 cross-reference now stated as 15-family (one row per CSV row). G14 gate predicate added. |
| **NIT-A3** | NIT | Shorthand invocations used in T02, Q7, A-4, A-5 — actual repo symbols absent | ALL shorthand invocations replaced with actual repo symbols: `validate_predecessor_artifact_provenance(repo_root)` (V1) and `validate_temporal_discipline(repo_root)` (V3). Adjudicator main entrypoint declared: `validate_temporal_feature_grid_adjudication(repo_root: Path) -> AdjudicationResult`. G15 gate predicate added. |
| **NIT-A4** | NIT | Halt-priority chain unenumerated; H7a/H7b split absent | 9-step halt-priority chain (H0-H7b) added to §Gate Condition with first-failure-wins semantics. H7a (paradox guard) and H7b (PR-self-archive) split explicitly. G16 gate predicate added. |
| **NIT-A5** | NIT | Ordering hazard unguarded (outputs dir before preflight) + post-emission closure absent | Adjudication sequence (8 steps) added to T02 Execution Steps. Outputs directory creation (step 5) explicitly gated on preflight PASS. Post-emission closure: "return AdjudicationResult; no further writes". G12 gate predicate added. |
| **NIT-A6** | NIT | H7 grep target list omits `.ipynb` paired notebook | H7 target list extended to 5 files, explicitly including `02_03_01_adjudication.ipynb`. G17 gate predicate added. |
