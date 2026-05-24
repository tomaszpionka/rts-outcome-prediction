---
category: A
branch: feat/sc2egset-02-01-03-roadmap-stub
base_ref: a16d78c25f16aaf8fad4f2c362445212aac1a16b
date: 2026-05-24
planner_model: claude-opus-4-7[1m]
dataset: sc2egset
phase: "02"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
step: "02_01_03 (Layer-1 ROADMAP-only stub design)"
non_batching_sequence_position: "Step 1 of 9 (ROADMAP stub only) — first planning unit for Pipeline Section 02_01 tranche-2 (history_enriched_pre_game)."
critique_required_before_execution: true
critique_reviewer: reviewer-adversarial
gate_reviewer: "reviewer-adversarial (Category A pre-execution gate)"
planning_pr: "PR #238"
planning_pr_scope: "Layer-1 (2 files only) — planning/current_plan.md + planning/current_plan.critique.md. NO ROADMAP edit, NO pyproject bump, NO CHANGELOG entry, NO planning/INDEX.md archive, NO status YAML flip, NO research_log entry, NO artifact, NO source/test/notebook touch."
future_execution_pr_scope: "Layer-2 (6 files) — ROADMAP.md (insert Step 02_01_03 block) + pyproject.toml (3.70.1 → 3.71.0) + CHANGELOG.md (new [3.71.0] block) + planning/INDEX.md (archive PR #237 → promote feat/sc2egset-02-01-03-roadmap-stub) + planning/current_plan.md (persisted from this Layer-1) + planning/current_plan.critique.md (persisted from this Layer-1)."
future_execution_pr_version_bump: "3.70.1 → 3.71.0 (minor; feat-family per .claude/rules/git-workflow.md)"
source_artifacts:
  # PR #236 + PR #237 closure evidence (predecessor lineage)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.md
  # Closed Step 02_01_01 catalog (the 22-family registry; defines the 6 tranche-2 history families)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json
  # Specs (provenance bond targets)
  - reports/specs/02_00_feature_input_contract.md  # CROSS-02-00-v3.0.1 §3.3 strict-< rule, §5.4 SC2 column classification
  - reports/specs/02_01_leakage_audit_protocol.md  # CROSS-02-01-v1.0.1 §2.1/§2.2/§2.3/§2.4
  - reports/specs/02_02_feature_engineering_plan.md  # CROSS-02-02-v1.0.1 §6.2 (6 history families), §9 (G-CS-*), §10 (G-L-*)
  - reports/specs/02_03_temporal_feature_audit_protocol.md  # CROSS-02-03-v1.0.1 §6.2 history rules, §5.1 strict-<
  # Closure-relevant status YAMLs (READ; byte-unchanged in the Layer-2 PR)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml
  # Dataset ROADMAP (the future Layer-2 PR inserts Step 02_01_03 between lines 2272 and 2274)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
  # Dataset research log (READ only; no entry added by Layer-2 ROADMAP-stub PR per non-batching rule sequence step 1)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
  # Rules / invariants / protocols
  - .claude/scientific-invariants.md
  - .claude/ml-protocol.md
  - .claude/rules/data-analysis-lineage.md
  - .claude/rules/git-workflow.md
  - docs/PHASES.md
  - docs/TAXONOMY.md
---

# SC2EGSet Step 02_01_03 — ROADMAP-only stub (Layer-1 planning)

## Branch

`feat/sc2egset-02-01-03-roadmap-stub`

## Category

A — Phase 02 ROADMAP authoring. The **future Layer-2 execution PR** creates a new ROADMAP yaml block (a new executable plan unit declaring Step `02_01_03`) and bumps the minor version per `.claude/rules/git-workflow.md` (minor for `feat`). The **present Layer-1 planning PR** contains only `planning/current_plan.md` + `planning/current_plan.critique.md`; no ROADMAP edit, no version bump, no CHANGELOG, no INDEX archive, and no status flip in this Layer-1.

## Version Bump

Layer-1 (this PR): none. Layer-2 (future execution PR): `3.70.1 → 3.71.0` in `pyproject.toml`, minor bump per `.claude/rules/git-workflow.md` (feat-family branch prefix). Precedent: PR #232 (the analogous ROADMAP-stub for Step `02_01_02`) bumped `3.66.0 → 3.67.0` with branch `feat/sc2egset-02-01-02-roadmap-stub`. Layer-1 planning PRs in this repo have historically also bundled minor bumps (PR #235 bumped `3.68.0 → 3.69.0` for plan + critique only); the present Layer-1 deviates from that precedent **only** because the bounded autonomous prompt that authored this plan caps the Layer-1 diff at exactly two files (`planning/current_plan.md` + `planning/current_plan.critique.md`). The version/CHANGELOG/INDEX tail is consequently deferred to the Layer-2 execution PR. This deviation is intentional and disclosed in the Layer-1 PR body.

## Scope

The **future Layer-2 execution PR** inserts ONE new ROADMAP yaml block — Step `02_01_03` — under Pipeline Section `02_01 — Pre-Game vs In-Game Boundary` in `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`, immediately after the closed `02_01_02` block (line 2272). The new block declares the design of the next Step `02_01_03 — History-enriched pre_game feature-family materialization (sc2egset)` — covering the 6 `history_enriched_pre_game` families from the closed Step 02_01_01 registry. It is ROADMAP-only: no notebook scaffold, no validator, no module, no test, no materialization, no feature value, no audit artifact, no status YAML flip, no research_log entry, no spec amendment, no cleaning-layer YAML edit, no INVARIANTS.md edit, no root `reports/research_log.md` edit. Phase 03 work is NOT started.

**The 6 history_enriched_pre_game families** (verbatim from `02_01_01_feature_family_registry.csv` rows 7–12; all carry `derived_section10_verdict ∈ {allowed, allowed_with_caveat}` per `02_01_01_section10_verdict_audit.csv` rows 7–12):

1. `sc2egset.history_enriched_pre_game.focal_player_history` — rolling/expanding aggregates over `player_history_all` for focal `toon_id`. Cold-start gate G-CS-2. Leakage mode: `rolling_includes_target_game`. §10 verdict: **allowed**.
2. `sc2egset.history_enriched_pre_game.opponent_player_history` — symmetric mirror for opponent `toon_id`. Cold-start gate G-CS-2. Leakage mode: `rolling_includes_target_game`. §10 verdict: **allowed**.
3. `sc2egset.history_enriched_pre_game.matchup_history_aggregate` — head-to-head + matchup-conditional history aggregates over `(focal_toon, opponent_toon)`. Cold-start gate G-CS-3. Leakage mode: `h2h_includes_target_game`. §10 verdict: **allowed**.
4. `sc2egset.history_enriched_pre_game.reconstructed_rating` — Glicko-2 or analogous rating reconstructed forward in time from prior decisive results. Cold-start gate G-CS-4. Leakage mode: `rating_uses_target_game_outcome`. §10 verdict: **allowed**.
5. `sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling` — `is_cross_region_fragmented` sensitivity-aware handling per RISK-20. Cold-start gate G-CS-5. Leakage mode: `cross_region_history_drop`. §10 verdict: **allowed_with_caveat**.
6. `sc2egset.history_enriched_pre_game.in_game_history_aggregate` — rolling APM / SQ / supplyCappedPercent / header_elapsedGameLoops aggregates over **prior** matches (NOT the target match). Cold-start gate G-CS-2. Leakage mode: `rolling_includes_target_game`. §10 verdict: **allowed**. **Lexical-confusion note:** this is `history_enriched_pre_game`, not `in_game_snapshot`; the columns are `IN_GAME_HISTORICAL` per CROSS-02-00 §5.4 and are **retained in scope** for history-aggregation use while remaining forbidden as direct game-T pre-game features. The Layer-2 ROADMAP block must include this CROSS-02-02 §6.2 row-6 note verbatim (reviewer-adversarial N2).

The 5 closed `pre_game` families (already materialized by PR #236) and the 11 `in_game_snapshot` families plus 3 `blocked_until_additional_validation` families remain out of scope for Step `02_01_03`.

## Problem Statement

PR #237 closed Step `02_01_02` at the status-chain layer (`STEP_STATUS.yaml` records `"02_01_02": { status: complete, completed_at: "2026-05-23" }`; dataset `research_log.md` 2026-05-24 entry records `closure_status: closed`, `status_yaml_state: complete`, `leakage_audit_state: post_materialization_pass`, `features_audited_count: 7`, `row_count: 44418`). The ROADMAP `02_01_02` `continue_predicate` reads:

> A future PR may begin Step 02_01_03 (the next 02_01 materialization step — history_enriched_pre_game tranche) only after this Step 02_01_02 has reached its artifact-check at a future PR, the CROSS-02-01-v1.0.1 post-materialization audit has returned a NON-vacuous PASS (future_leak_count = 0, post_game_token_violations = 0 over a non-empty features_audited), and a per-family CROSS-02-03-v1.0.1 section 10 verdict consistent with the materialized columns is recorded.

Each of the three clauses is cleared on disk:

- **artifact_check**: `02_01_02_pre_game_features.parquet` (44,418 rows × 11 cols; 719,068 bytes) at the spec-named path.
- **non-vacuous audit**: `02_01_02/leakage_audit_sc2egset.json` `verdict = PASS`, `features_audited` length 7 (focal_race, opponent_race, race_pair, map_type, patch_version, focal_is_mmr_missing, opponent_is_mmr_missing), `audit_pr = "PR #236"`, `future_leak_count = 0`, `post_game_token_violations = 0`.
- **per-family §10 consistency**: PR #229 §10 verdict audit CSV records all 26 catalog rows; the 5 tranche-1 materialized columns are consistent with the design-time §10 verdicts (verified by PR #237 closure entry).

The continue_predicate therefore **permits** a future PR to begin Step `02_01_03`.

But the ROADMAP currently has **NO** concrete Step `02_01_03` block: `grep -n "step_number" ROADMAP.md` returns only `"02_01_01"` (line 1917) and `"02_01_02"` (line 2102); the next heading is `## Phase 03 — Splitting & Baselines (placeholder)` at line 2276 (placeholder with no concrete steps). Per `.claude/rules/data-analysis-lineage.md` "Non-batching rule for empirical work" sequence step 1, the next atomic Step must begin with a **ROADMAP stub only** — scaffold, validator, materialization, and audit must be on *separate* successor PRs. The next atomic unit is therefore a Step `02_01_03` ROADMAP-only stub.

**Why not Phase 03?** Per `docs/PHASES.md`, Phase 02 has 8 pipeline sections (`02_01` through `02_08`); only `02_01` is `complete` per `PIPELINE_SECTION_STATUS.yaml` (1 of 8). Per `PHASE_STATUS.yaml`, Phase 02 is `in_progress` and Phase 03 is `not_started`. No clause in the repository permits beginning Phase 03 baseline work before Phase 02 sections `02_02` through `02_08` are complete.

**Why ROADMAP-only and not scaffold-included?** The non-batching rule explicitly states: "Do not create a full empirical notebook in the same execution that creates the ROADMAP entry for that Step. The first notebook pass should be a scaffold plus one validation module only." Step `02_01_02` followed this rule across 6 successor PRs (#232 ROADMAP-stub → #233 scaffold+validator → #234 source/anchor adjudication → #235 Layer-1 materialization plan → #236 materialization-execution → #237 closure). Step `02_01_03` history features carry HIGHER leakage risk than `02_01_02` (history windows + Bayesian smoothing + rating reconstruction + cross-region drop), so the same multi-PR cadence is **required**, not optional.

**Why is the CROSS-02-02 §6.1 amendment NOT a tranche-2 blocker?** The §6.1 amendment (proposed in PR #234 §8) concerns pre_game `race` vs `selectedRace` vocabulary clarification only. It does NOT affect any tranche-2 history family — the matchup_history_aggregate vocabulary is the SC2 race vocabulary {Prot, Terr, Zerg} per the closed PR #234 Q3.RATIFY (Random handling preserved as documented_gap). The §6.1 amendment remains a separate future Category E spec-only PR target and does not block Step `02_01_03` ROADMAP-stub planning. Reviewer-adversarial confirmed this is deferrable.

## Future ROADMAP block (verbatim draft for the future Layer-2 execution PR)

The future Layer-2 execution PR inserts the following block immediately after line 2272 (the closing fence of the existing `02_01_02` block) and immediately before line 2274 (the `---` separator before `## Phase 03 — Splitting & Baselines (placeholder)`). No other line of ROADMAP.md is touched.

The block below is the EXACT text to insert. Outer fence is 4 backticks (`````) so the inner ROADMAP `yaml` fence remains intact:

`````markdown
### Step 02_01_03 — History-enriched pre_game feature-family materialization (sc2egset)

```yaml
step_number: "02_01_03"
name: "History-enriched pre_game feature-family materialization (sc2egset)"
description: >-
  Second MATERIALIZATION step of Pipeline Section 02_01: materialize the 6
  history_enriched_pre_game feature families declared allowed (or
  allowed_with_caveat for cross_region_fragmentation_handling) in the closed
  Step 02_01_01 registry — focal_player_history, opponent_player_history,
  matchup_history_aggregate, reconstructed_rating,
  cross_region_fragmentation_handling, in_game_history_aggregate. Then
  re-run the CROSS-02-01-v1.0.1 post-materialization leakage audit on the
  resulting non-empty features_audited set. Strict history cutoff:
  history_time < target_time (per CROSS-02-02 §6.2 row 1 strict-less-than;
  Invariant I3; CROSS-02-00-v3.0.1 §3.3; CROSS-02-03 §5.1). Per-dataset
  history anchor: ph.details_timeUTC < target.started_at. The 6th family
  in_game_history_aggregate aggregates IN_GAME_HISTORICAL columns
  (APM/SQ/supplyCappedPercent/header_elapsedGameLoops) over PRIOR matches;
  these columns are retained in scope per CROSS-02-02 §6.2 row 6 for
  history-aggregation use while remaining forbidden as direct game-T
  pre-game features. No tracker_events_raw source for any family (Invariant
  I3; Amendment 2 of PR #208). The 5 closed pre_game families materialized
  by PR #236 are READ as upstream evidence inputs but NOT re-materialized.
  The 11 in_game_snapshot families (tracker-event-bound) are DEFERRED to a
  successor Step 02_01_04+. Lineage position: ROADMAP stub is artifact #1
  of N for Step 02_01_03 readiness (subsequent artifacts: notebook scaffold
  + one validator, tranche-2 source/anchor/cold-start adjudication,
  materialization-execution plan, materialization-execution, closure).
  This is the SECOND materialization tranche of Pipeline Section 02_01;
  tranche 1 (PR #236) materialized 5 pre_game families; tranche 3 (future
  Step 02_01_04) will materialize in_game_snapshot families. NO feature
  value is materialized in this ROADMAP-stub PR — this entry only declares
  the future step per .claude/rules/data-analysis-lineage.md "Non-batching
  rule for empirical work" sequence step 1; the notebook scaffold, one
  validation module, source/anchor/cold-start adjudication, materialization,
  and the post-materialization audit are produced by SEPARATE FUTURE PRs
  (sequence steps 2-9).
phase: "02 — Feature Engineering"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
manual_reference: "02_FEATURE_ENGINEERING_MANUAL.md, Section 2"
dataset: "sc2egset"
question: >-
  Can the 6 allowed history_enriched_pre_game feature families from the
  closed Step 02_01_01 registry be materialized into a
  per-(focal_match_id, focal_player) feature table whose every column
  passes the CROSS-02-01-v1.0.1 post-materialization leakage audit with a
  NON-vacuous (non-empty features_audited) PASS verdict, under strict
  history_time < target_time cutoff (no <=, no closed-interval window, no
  target-match final state — covers G-L-1, G-L-3, G-L-4, G-L-7),
  symmetric focal/opponent construction (Invariant I5), and explicit
  cold-start handling per CROSS-02-02 §9 (G-CS-2 through G-CS-6)?
method: >-
  For each of the 6 history_enriched_pre_game families, write a DuckDB
  projection over matches_flat_clean joined to player_history_all keyed on
  (player_id_worldwide) and filtered by ph.details_timeUTC <
  target.started_at (STRICT inequality; Invariant I3; G-L-1 prohibits <=;
  G-L-3 prohibits target-match final state; G-L-7 prohibits rolling /
  h2h that include the target match). Produce focal_* and opponent_*
  columns symmetrically (Invariant I5). Cold-start handling per family:
  G-CS-2 (allow cold_start flag with declared threshold derivation) /
  G-CS-3 (empirical smoothing-prior derivation from training fold only) /
  G-CS-4 (no global rating fit; rating reconstructed forward in time from
  prior decisive results only) / G-CS-5 (per-source cold-start
  enumeration) / G-CS-6 (encoder + smoothing-prior fit on training folds
  only). All smoothing/threshold constants empirically derived from
  training folds only (Invariant I3 normalization discipline + G-CS-6) or
  cited from literature (Invariant I7). Run the CROSS-02-01-v1.0.1 audit
  (sections 2.1 cutoff structural check, 2.2 POST-GAME token absence, 2.3
  normalization fit-scope, 2.4 reference window) over the materialized
  columns; emit a NON-vacuous leakage_audit_sc2egset.{json,md} under
  reports/artifacts/02_01_03/ with features_audited = the full set of
  focal_* + opponent_* + matchup_* + rating_* + sensitivity column names.
  All non-trivial logic in src/rts_predict/. THIS PR delivers only the
  ROADMAP stub (sequence step 1); materialization is a separate future PR.
stratification: >-
  Per family: dataset_tag = sc2egset; prediction_setting =
  history_enriched_pre_game. SC2 races (Prot / Terr / Zerg) are
  stratification axes for matchup_history_aggregate (vocabulary {Prot,
  Terr, Zerg} per closed PR #234 Q3.RATIFY; Random handled per
  documented_gap noted in PR #234 §8). Cross-region fragmentation
  sensitivity arm is co-stratified (with vs without filter) per
  CROSS-02-02 §6.2 row 5 / RISK-20; the choice between (a)
  strict-exclusion, (b) dual-feature-path, (c) sensitivity-indicator
  co-registration is DEFERRED to the tranche-2 source/anchor/cold-start
  adjudication PR (analogous to PR #234 for tranche-1).
predecessors: "02_01_02"
notebook_path: >-
  sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py
inputs:
  duckdb_tables:
    - "matches_flat_clean"
    - "matches_history_minimal"
    - "player_history_all"
  schema_yamls:
    - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml"
    - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml"
  prior_artifacts:
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv"
  external_references:
    - "reports/specs/02_00_feature_input_contract.md (CROSS-02-00-v3.0.1) §3.3 strict-less-than rule, §5.4 SC2 column classification (IN_GAME_HISTORICAL distinct from IN_GAME)"
    - "reports/specs/02_01_leakage_audit_protocol.md (CROSS-02-01-v1.0.1) §2.1 / §2.2 / §2.3 / §2.4"
    - "reports/specs/02_02_feature_engineering_plan.md (CROSS-02-02-v1.0.1) §6.2 (6 history families; row 6 IN_GAME_HISTORICAL retention note), §9 (G-CS-2 / G-CS-3 / G-CS-4 / G-CS-5 / G-CS-6), §10 (G-L-1 / G-L-3 / G-L-4 / G-L-7)"
    - "reports/specs/02_03_temporal_feature_audit_protocol.md (CROSS-02-03-v1.0.1) §3 audit object, §4 D1-D15, §5.1 strict-less-than, §6.2 history_enriched_pre_game prediction-setting rules, §10 verdicts"
    - ".claude/rules/data-analysis-lineage.md (non-batching rule; halt-before-artifact)"
    - ".claude/ml-protocol.md (three leakage failure modes — rolling, h2h, co-occurring matches)"
    - ".claude/scientific-invariants.md (I3 temporal, I3 normalization, I5 symmetry, I6 SQL provenance, I7 no magic numbers, I8 cross-game, I9 step-derived conclusions, I10 relative-path)"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/methodology_risk_register.md (RISK-20 cross-region fragmentation; RISK-24 slot asymmetry; RISK-26 Random race semantics)"
outputs:
  data_artifacts:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_features.parquet"
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.json"
  report:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.md"
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.md"
reproducibility: >-
  Every materialized column traces to a registry row in
  02_01_01_feature_family_registry.csv (rows 7-12); every projection SQL
  with its strict-< history filter is embedded verbatim in the report MD
  alongside its result (Invariant I6). No magic numbers (Invariant I7):
  cold-start thresholds (K), smoothing pseudocounts (m), and Bayesian
  prior strengths (alpha) are either empirically derived from training
  folds only (G-CS-1 / G-CS-3) or cited from literature; the derivation
  procedure is recorded in the materialization PR's report MD. Encoder
  and smoothing-prior fit on training folds only (G-CS-6; CROSS-02-01
  §2.3). Glicko-2 rating reconstructed forward in time match-by-match —
  no global / batch fit. Seed 42 convention; deterministic export;
  relative-path provenance (Invariant I10).
scientific_invariants_applied:
  - number: "3"
    how_upheld: >-
      Every history-derived column applies STRICT ph.details_timeUTC <
      target.started_at; no closed-interval, no <=, no rolling window
      that includes the target match (G-L-1, G-L-3, G-L-7). Rating
      reconstruction is forward in time only — game T's outcome never
      enters game T's rating feature (CROSS-02-02 §10 G-L-4). All
      smoothing/scaling/imputation statistics are fit on training folds
      only (Invariant I3 normalization-leakage discipline; G-CS-6). No
      tracker-derived source (Invariant I3; Amendment 2 of PR #208).
  - number: "5"
    how_upheld: >-
      Every per-player family produces focal_* and opponent_* columns
      symmetrically via the same SQL pattern; no player slot is
      privileged. RISK-24 data-dependent slot-assignment falsifier
      enumerated in the materialization notebook.
  - number: "6"
    how_upheld: >-
      Every reported count/distribution in the report MD is accompanied
      by its verbatim DuckDB SQL with the strict-< filter; no value is
      paraphrased.
  - number: "7"
    how_upheld: >-
      No magic numbers. Cold-start threshold K, smoothing pseudocount m,
      Bayesian prior strength alpha, and rating-reconstruction
      hyperparameters are each either empirically derived from training
      folds (G-CS-1/G-CS-3/G-CS-6) or cited from literature with the
      citation embedded in the materialization PR's report MD.
  - number: "8"
    how_upheld: >-
      The 6 history families are the shared cross-game history
      categories (player_history, opponent_history, matchup_history,
      reconstructed rating) named in Invariant I8; encoders + smoothing
      priors carry dataset_tag = 'sc2egset' partition and are not fit
      cross-dataset.
  - number: "9"
    how_upheld: >-
      The Step reads only Phase 01 outputs and the CLOSED Steps 02_01_01
      + 02_01_02 artifacts (all lower-numbered, on disk); builds no
      model; makes no source-stratified evaluation claim.
  - number: "10"
    how_upheld: >-
      The materialized feature table and its provenance use the
      relative-path convention; no absolute path is written to any
      artifact.
gate:
  artifact_check: >-
    NOT APPLICABLE TO THIS ROADMAP-STUB PR. The artifact_check fires only
    after the future scaffold-and-materialization PR materializes the
    feature table + the NON-vacuous CROSS-02-01-v1.0.1 audit pair; at
    that point the predicate is "the planned Parquet feature matrix, the
    audit JSON, and both report MDs exist at the declared paths and are
    non-empty, the audit JSON has features_audited != [] with verdict =
    PASS, and every history column projected applied a strict-<
    ph.details_timeUTC < target.started_at filter verifiable in the
    materialization SQL."
  continue_predicate: >-
    A future PR may begin Step 02_01_04 (the next 02_01 materialization
    step — in_game_snapshot tranche) only after this Step 02_01_03 has
    reached its artifact-check at a future PR, the CROSS-02-01-v1.0.1
    post-materialization audit has returned a NON-vacuous PASS
    (future_leak_count = 0, post_game_token_violations = 0 over a
    non-empty features_audited covering all 6 history families'
    materialized columns), and a per-family CROSS-02-03-v1.0.1 §10
    verdict consistent with the materialized columns is recorded. The
    §10 design-time verdict audit (PR #229) is a distinct artifact and
    does NOT substitute for this post-materialization CROSS-02-01 audit;
    a re-executed §10 audit over the 6 history rows (distinct from the
    PR #229 design-time audit that covered the catalog at registry-
    creation time) is required before tranche-3 may begin, OR a
    non-vacuous justification for not re-running must be recorded in the
    materialization PR's research_log entry.
  halt_predicate: >-
    Halt before generating any feature artifact if any of the following
    hold (per .claude/rules/data-analysis-lineage.md "Stop conditions"):
      - any materialized history column uses <= or no time filter
        (G-L-1 violation; Invariant I3);
      - any rolling aggregate or head-to-head aggregate includes the
        target match's own row (G-L-7);
      - any history column uses the target match's final state
        (G-L-3 violation);
      - any rating uses game T's outcome (G-L-4);
      - any encoder, scaler, smoothing prior, or rating-reconstruction
        hyperparameter is fit on validation/test folds, on the full
        dataset, or cross-dataset (Invariant I3 normalization-leakage;
        G-CS-6);
      - any tracker_events_raw column is read for a history family
        (Invariant I3; Amendment 2 of PR #208);
      - any family outside the 6 history_enriched_pre_game rows is
        materialized in this Step (scope creep into the deferred
        in_game_snapshot tranche);
      - any cold-start row pins a numeric pseudocount, threshold, or
        smoothing constant without a fold-aware empirical derivation or
        literature citation (Invariant I7; G-CS-1);
      - the focal_* / opponent_* construction is asymmetric (Invariant
        I5; RISK-24);
      - the cross_region_fragmentation_handling sensitivity arm is
        materialized without prior tranche-2 source/anchor/cold-start
        adjudication selecting (a) strict-exclusion, (b) dual-path, or
        (c) sensitivity-indicator co-registration (CROSS-02-02 §6.2
        row 5; RISK-20);
      - the future notebook scaffold attempts to batch ROADMAP +
        notebook + artifact + next step in one execution (non-batching
        rule);
      - any future-Step pre-emption appears (e.g., 02_01_04 in_game
        material in the same PR).
thesis_mapping:
  - "Chapter 4 — Data and Methodology > §4.5 Feature engineering plan (sc2egset history_enriched_pre_game materialization)"
research_log_entry: >-
  NOT REQUIRED FOR THIS ROADMAP-STUB PR per
  .claude/rules/data-analysis-lineage.md "Non-batching rule" sequence
  (step 1 — ROADMAP stub only — produces no research_log entry).
  Required on the future scaffold-and-materialization PR per the
  standard step-completion protocol; entry goes into
  src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md.
```
`````

## Assumptions & Unknowns

Assumptions (verified on master at `a16d78c25f16aaf8fad4f2c362445212aac1a16b` by @lookup, 13/13 PASS):

1. PR #237 closure on disk: `STEP_STATUS.yaml` contains `"02_01_02": { status: complete, completed_at: "2026-05-23" }`.
2. PR #236 evidence: `02_01_02/leakage_audit_sc2egset.json` reports `verdict: PASS`, `features_audited` length 7, `audit_pr: "PR #236"`, `future_leak_count: 0`, `post_game_token_violations: 0`, `normalization_fit_scope: training_fold_only`.
3. Continue predicate cleared: all three ROADMAP `02_01_02` `continue_predicate` clauses (artifact_check, non-vacuous CROSS-02-01 audit, per-family §10 verdict) satisfied on disk.
4. ROADMAP currently has no `02_01_03` block: `grep -n "step_number"` returns only `02_01_01` (line 1917) and `02_01_02` (line 2102); next heading is `## Phase 03 — ...` at line 2276.
5. The 6 `history_enriched_pre_game` families enumerated above match `02_01_01_feature_family_registry.csv` rows 7–12 verbatim and all carry `derived_section10_verdict ∈ {allowed, allowed_with_caveat}` per `02_01_01_section10_verdict_audit.csv` rows 7–12.
6. Pipeline Section `02_01` will remain `complete` when this ROADMAP-stub PR lands (no STEP_STATUS row for `02_01_03` is added at Layer-2 ROADMAP-stub time — see Layer-2 Gate Condition; this mirrors the YAML-derivation behaviour disclosed in PR #230 / PR #232 / PR #237 status-derivation notes).

Unknowns (deferred to successor PRs; not blocking this Layer-1 planning PR or the Layer-2 ROADMAP-stub):

- The exact source binding for each of the 6 history families (tranche-1 used `matches_flat_clean` per PR #234 Q1 RATIFY; tranche-2 history families likely require a JOIN to `player_history_all`). Resolved in tranche-2 source/anchor adjudication PR.
- The exact cold-start threshold derivation procedure for G-CS-2 / G-CS-3 / G-CS-4 / G-CS-5. Resolved in tranche-2 cold-start adjudication PR.
- The cross-region fragmentation sensitivity arm choice (strict-exclusion vs dual-feature-path vs sensitivity-indicator co-registration per CROSS-02-02 §6.2 row 5). Resolved in tranche-2 source/anchor adjudication PR.
- The rating-reconstruction choice (Glicko-2 vs Elo vs alternatives). Resolved in tranche-2 design adjudication.

## Literature Context

Each history-feature design decision deferred to successor PRs must cite either empirical derivation from training-fold data or prior literature. For the ROADMAP-stub PR itself, the cited foundations are repository-internal:

- CROSS-02-02-v1.0.1 §6.2 (rolling/expanding history families, reconstructed rating, in_game_history_aggregate constraints; row 6 IN_GAME_HISTORICAL retention note).
- CROSS-02-02-v1.0.1 §9 (cold-start gates G-CS-1 through G-CS-6).
- CROSS-02-02-v1.0.1 §10 (leakage gates G-L-1, G-L-3, G-L-4, G-L-7).
- CROSS-02-03-v1.0.1 §6.2 (`history_enriched_pre_game` prediction-setting rules) and §5.1 (strict less-than rule).
- CROSS-02-00-v3.0.1 §3.3 (strict-less-than history cutoff); §5.4 (IN_GAME_HISTORICAL distinct from IN_GAME column classification).
- `.claude/scientific-invariants.md` I3 (temporal + normalization discipline), I5 (symmetric treatment), I6 (SQL provenance), I7 (no magic numbers), I8 (cross-game), I10 (relative paths).
- `.claude/ml-protocol.md` "three leakage failure modes": rolling aggregates that include game T; head-to-head that includes game T; co-occurring matches that include game T.
- PR #229 §10 design-time verdict audit (per-family allowed / allowed_with_caveat).
- PR #232 ROADMAP-stub template (the structural model this Step `02_01_03` ROADMAP-stub mirrors).
- de Prado 2018 Ch. 7 and Arlot & Celisse 2010 (cited in `.claude/scientific-invariants.md` §3 for normalization-leakage discipline that constrains rating / smoothing-prior fitting).

External literature citations (Glicko-2, Bayesian win-rate smoothing) are **deferred** to the materialization PR's design adjudication, not introduced in the ROADMAP stub.

## Execution Steps

### Layer-1 (THIS PR) — 2 mechanical operations

- **L1-T01** — Write `planning/current_plan.md` (this file) to the branch `feat/sc2egset-02-01-03-roadmap-stub` and commit. Falsifier `F-layer1-file-count` — diff must contain exactly 2 file paths.
- **L1-T02** — Write `planning/current_plan.critique.md` (reviewer-adversarial verdict body) to the same branch and commit (may be a single commit with L1-T01). Open draft PR. Normalize `planning_pr` placeholder in both files with the assigned PR number.

### Layer-2 (FUTURE PR) — 7 mechanical operations

The future Layer-2 execution PR performs exactly the following 7 file operations and no others:

- **L2-T01** — Insert the Step `02_01_03` block (from the "Future ROADMAP block" section above) into `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` between line 2272 (closing fence of `02_01_02` block) and line 2274 (`---` before Phase 03 placeholder). No other line of ROADMAP.md is edited. Falsifier `F-roadmap-line-count-delta-too-small` — the diff must be a pure insertion of ≥ 180 lines; no deletion; no edit to existing `02_01_01` or `02_01_02` blocks; no edit to Phase 03 placeholder.
- **L2-T02** — Bump version in `pyproject.toml`: `version = "3.70.1"` → `version = "3.71.0"`. Falsifier `F-version-bump-incorrect`.
- **L2-T03** — Update `CHANGELOG.md`. Move `[Unreleased]` content (empty) into a new `## [3.71.0] — 2026-05-DD (PR #NNN: feat/sc2egset-02-01-03-roadmap-stub)` block. Leave `[Unreleased]` empty with the four standard headers. The new block contains: `### Added`: bullet listing the inserted ROADMAP block. `### Notes`: bullets enforcing "ROADMAP-only; NO notebook, NO artifact, NO feature value, NO status YAML flip, NO research_log entry, NO Phase 03 work; the 6 history_enriched_pre_game and the 11 in_game_snapshot families are partitioned correctly per the registry; Pipeline Section `02_01` remains `complete` because this ROADMAP-only PR adds NO STEP_STATUS row (intended YAML-derivation behaviour, pre-disclosed in PR #230 / PR #232 / PR #237 status-derivation notes); PR #229 §10 evidence and PR #230 / PR #236 / PR #237 closure chain are kept distinct."
- **L2-T04** — Update `planning/INDEX.md`. Archive PR #237 with its master merge SHA `a16d78c2`; promote `feat/sc2egset-02-01-03-roadmap-stub` to the Active line. **Note**: The Layer-1 PR did NOT update INDEX.md per its 2-file scope cap; Layer-2 inherits the dual archive (PR #237 → archived, the Layer-1 planning PR → archived, the Layer-2 PR → Active).
- **L2-T05** — Persist `planning/current_plan.md` and `planning/current_plan.critique.md` as they exist on the Layer-1 branch (no Layer-2 rewrite). They are already committed on `feat/sc2egset-02-01-03-roadmap-stub` by the Layer-1 PR; Layer-2 inherits them.
- **L2-T06** — Run pre-commit hooks. `ruff` and `mypy` are skipped (no `.py` files in diff). The plan-section-name pre-commit hook (enforcing `## Scope`, `## Execution Steps`, `## File Manifest`, `## Problem Statement`, `## Assumptions & Unknowns`, `## Literature Context`, `## Gate Condition`, `## Open Questions`) runs against the persisted `planning/current_plan.md`. Falsifier `F-pre-commit-rejects-plan-section-names`.
- **L2-T07** — Open Layer-2 PR. Title: `feat(sc2egset): roadmap stub for Step 02_01_03 (history-enriched pre_game tranche)`. Body per `.github/pull_request_template.md`. Body explicitly declares: ROADMAP-only; NO notebook, NO artifact, NO feature value, NO status YAML flip, NO research_log, NO Phase 03 work.

The Layer-2 executor is `@executor` (Sonnet sufficient — mechanically specified; no scientific decision remains).

## File Manifest

### Layer-1 (THIS PR) — exactly 2 files

| # | Path | Operation |
|---|------|-----------|
| 1 | `planning/current_plan.md` | Overwrite with this plan body |
| 2 | `planning/current_plan.critique.md` | Overwrite with reviewer-adversarial critique |

### Layer-2 (FUTURE PR) — exactly 6 files (incl. 2 inherited from Layer-1)

| # | Path | Operation |
|---|------|-----------|
| 1 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | Insert Step `02_01_03` block (pure insertion between lines 2272 and 2274; no other line touched) |
| 2 | `pyproject.toml` | Bump `version = "3.70.1"` → `version = "3.71.0"` |
| 3 | `CHANGELOG.md` | Move `[Unreleased]` (empty) into new `[3.71.0]` block |
| 4 | `planning/INDEX.md` | Archive PR #237; archive the Layer-1 planning PR; promote `feat/sc2egset-02-01-03-roadmap-stub` Layer-2 to Active |
| 5 | `planning/current_plan.md` | Inherited from Layer-1; no Layer-2 rewrite |
| 6 | `planning/current_plan.critique.md` | Inherited from Layer-1; no Layer-2 rewrite |

### Files NOT touched (negation, verified by both Layer-1 and Layer-2)

- `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml` — no status flip; no STEP_STATUS row added for `02_01_03`.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` (if exists) — byte-unchanged.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` — no entry (non-batching rule sequence step 1 produces no research_log entry).
- `reports/research_log.md` (root) — byte-unchanged (single-dataset stub is not a cross-dataset decision).
- Any `reports/artifacts/**` file — byte-unchanged.
- Any `reports/specs/**` file (the CROSS-02-02 §6.1 minor amendment proposed in PR #234 §8 remains a future Category E spec-only PR target; this ROADMAP-stub PR does not apply it).
- Any cleaning-layer YAML (`matches_flat_clean.yaml`, `matches_history_minimal.yaml`, `matches_long_raw.yaml`) — byte-unchanged.
- Any source / test / notebook / module (`src/rts_predict/**.py`, `tests/**.py`, `sandbox/**.py`, `sandbox/**.ipynb`) — byte-unchanged. No `def`/`class`/lambda authored at this layer or the next.
- Any AoE2 file (`src/rts_predict/games/aoe2/**`) — byte-unchanged.
- Any thesis file (`thesis/**`) — byte-unchanged.
- Any `docs/**` or `.claude/**` file — byte-unchanged.

## Gate Condition

### Layer-1 (THIS PR) merge eligibility

The Layer-1 PR is merge-eligible if and only if all of the following hold:

- `git diff master --name-only` returns exactly 2 paths: `planning/current_plan.md` and `planning/current_plan.critique.md` (no more, no less).
- `planning/current_plan.md` contains all 8 required `##` sections (Scope, Execution Steps, File Manifest, Problem Statement, Assumptions & Unknowns, Literature Context, Gate Condition, Open Questions) per the project pre-commit hook (`feedback_plan_required_sections.md`).
- `planning/current_plan.critique.md` carries the reviewer-adversarial verdict `APPROVE-WITH-NITS` with zero blockers.
- `planning_pr` placeholders in both planning files are normalized to the literal assigned PR number after PR creation.
- PR is OPEN, DRAFT, and not merged.

### Layer-2 (FUTURE PR) merge eligibility

The Layer-2 PR is merge-eligible if and only if all of the following hold post-execution and pre-merge:

- `git diff master --name-only` returns exactly the 6 paths in the Layer-2 File Manifest (no more, no less).
- ROADMAP.md adds a single new `02_01_03` block between lines 2272 and 2274; no other ROADMAP line is changed.
- The inserted block declares `predecessors: "02_01_02"` (only — `02_01_01` is a transitive predecessor and must NOT appear) and `dataset: "sc2egset"` and lists the 6 `history_enriched_pre_game` families exactly (no `in_game_snapshot`, no `blocked_until_additional_validation`, no fewer than 6, no more than 6, no name drift from the registry CSV).
- The inserted block's `gate.continue_predicate` requires NON-vacuous CROSS-02-01 PASS over the materialized columns plus per-family §10 consistency before any `02_01_04` PR may begin; explicitly requires a re-executed §10 audit over the 6 history rows (distinct from PR #229) OR a non-vacuous justification for not re-running.
- The inserted block's `gate.halt_predicate` enumerates all four leakage gates from CROSS-02-02 §10 by name (G-L-1 strict-<, G-L-3 target-final-state, G-L-4 rating-outcome, G-L-7 rolling/h2h-target-inclusion), plus the three ml-protocol.md failure modes by semantic content (rolling, h2h, normalization fit-scope), plus the tracker-creep falsifier, the cross-region adjudication-prerequisite falsifier, the asymmetry falsifier (Invariant I5; RISK-24), the magic-number falsifier (Invariant I7; G-CS-1), and the non-batching falsifier.
- `pyproject.toml` version is `3.71.0`.
- `CHANGELOG.md` `[3.71.0]` block records the inserted block + the ROADMAP-only / no-artifact / no-status-flip / no-Phase-03 disclaimers + the YAML-derivation note that Pipeline Section `02_01` remains `complete`.
- `planning/INDEX.md` archives PR #237 + the Layer-1 planning PR and lists the new Layer-2 branch as Active.
- `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml` are byte-unchanged.
- `research_log.md` (dataset and root) are byte-unchanged.
- Pre-commit hooks pass.
- Reviewer-adversarial (Cat A final gate) APPROVE on the persisted ROADMAP diff + the planning artifacts.

## Open Questions

Reviewer-adversarial (claude-opus-4-7[1m], 2026-05-24) returned APPROVE-WITH-NITS with **zero blockers**. The six non-blocking nits are reproduced here as acceptance criteria for the Layer-2 ROADMAP block draft (not Layer-1 blockers):

- **N1 — G-L-3 explicit in halt_predicate.** The Future ROADMAP block above lists G-L-3 ("any history column uses the target match's final state") explicitly alongside G-L-1, G-L-4, G-L-7. Addressed in the Future ROADMAP block draft.
- **N2 — `in_game_history_aggregate` naming clarity.** The Future ROADMAP block `description` field includes the verbatim CROSS-02-02 §6.2 row-6 note that IN_GAME_HISTORICAL columns are retained in scope for history-aggregation use while remaining forbidden as direct game-T pre-game features. Addressed in the Future ROADMAP block draft.
- **N3 — Lineage-position framing for Step `02_01_03`.** The Future ROADMAP block `description` field includes the lineage-position comment ("artifact #1 of N for Step 02_01_03 readiness; subsequent artifacts: notebook scaffold + one validator, tranche-2 source/anchor/cold-start adjudication, materialization-execution plan, materialization-execution, closure"). Addressed in the Future ROADMAP block draft.
- **N4 — `predecessors: "02_01_02"` only.** The Future ROADMAP block `predecessors` field is `"02_01_02"` (string, not list); `02_01_01` is a transitive predecessor and is NOT listed. Addressed in the Future ROADMAP block draft. Layer-2 Gate Condition explicitly enforces this.
- **N5 — Cross-region fragmentation adjudication gating.** The Future ROADMAP block `gate.halt_predicate` includes the falsifier that `cross_region_fragmentation_handling` cannot be materialized without a prior tranche-2 source/anchor/cold-start adjudication selecting (a) strict-exclusion, (b) dual-path, or (c) sensitivity-indicator co-registration. The block `stratification` field also flags this deferral. Addressed in the Future ROADMAP block draft.
- **N6 — §10 audit re-run gating.** The Future ROADMAP block `gate.continue_predicate` explicitly requires "a re-executed §10 audit over the 6 history rows (distinct from the PR #229 design-time audit that covered the catalog at registry-creation time) is required before tranche-3 may begin, OR a non-vacuous justification for not re-running must be recorded in the materialization PR's research_log entry." Addressed in the Future ROADMAP block draft.

Additional non-blocker design questions (DEFERRED to successor PRs):

- **OQ-DEF-1 — Should `cross_region_fragmentation_handling` (allowed_with_caveat) be split into its own sub-Step `02_01_03a`?** Recommendation: keep all 6 families in one Step `02_01_03` for ROADMAP-stub-stage parsimony; defer the split decision to the tranche-2 source/anchor adjudication PR.
- **OQ-DEF-2 — Should the rating family (reconstructed Glicko-2; G-CS-4) be split out as the most methodologically complex family?** Recommendation: keep all 6 in one Step `02_01_03`; defer the split decision to the tranche-2 design adjudication.
- **OQ-DEF-3 — Should the Layer-1 planning PR also explicitly authorize the tranche-2 source/anchor/cold-start adjudication PR (analogous to PR #234 for tranche-1)?** Recommendation: DEFER. Each layer carries its own scientific scope; PR #234's three-question structure (Q1 source, Q2 anchor, Q3 race) does not map cleanly onto tranche-2's six families.

## Stop Conditions

Halt this planning PR (Layer-1) before execution if any of the following hold:

- The PR #236 audit JSON is empirically not `verdict = PASS` or `features_audited` length is not 7. **Verified PASS** as of `a16d78c2`.
- The dataset `research_log.md` most-recent entry does not have `closure_status: closed`. **Verified `closed`** as of 2026-05-24.
- The ROADMAP at `a16d78c2` already contains a Step `02_01_03` block. **Verified absent** as of `a16d78c2`.
- A pending CROSS-02-02 §6.1 amendment is required before tranche-2 planning can begin. **Verified deferrable** — §6.1 amendment concerns pre_game race vocabulary only; no tranche-2 history family is blocked.
- The PR #237 closure was reopened or contested before this planning PR executes. **Verified merged and unchallenged**.

## Critique gate notice

This is a Category A plan. Per `CLAUDE.md` "Plan / Execute Workflow":

1. The reviewer-adversarial verdict (APPROVE-WITH-NITS, zero blockers) is captured in `planning/current_plan.critique.md` on this branch.
2. After Layer-1 PR merge, a separate Layer-2 execution PR will be opened (executor: `@executor` on Sonnet, mechanically specified). The executor reads `planning/current_plan.md` and `planning/current_plan.critique.md` directly per the agent-routing protocol.
3. The Layer-2 PR is itself a Category A gate — a final reviewer-adversarial pass must verify the persisted ROADMAP block + version/CHANGELOG/INDEX tail before Layer-2 merge.
4. Per the 3-round adversarial cap (symmetric to execution-side review per `feedback_adversarial_cap_execution.md`), planning-side adversarial may go up to 3 rounds before halting for explicit user direction. This Layer-1 round completed in 1 pass.
