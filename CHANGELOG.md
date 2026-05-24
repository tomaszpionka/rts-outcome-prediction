# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Conventional Commits](https://www.conventionalcommits.org/).

Each feature branch merges as a semver bump. The `[Unreleased]` section
tracks only changes on the current working branch that have not yet been
merged to `master`.

## [Unreleased]

### Added

### Changed

### Fixed

### Removed

## [3.74.0] — 2026-05-24 (PR #243: feat/sc2egset-02-01-03-history-cross-region-adjudication)

### Added

- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` — Q5-only cross-region retention-measurement successor adjudicator module for SC2EGSet Step 02_01_03. Two frozen dataclasses (`CrossRegionAdjudicationDecision` 30 fields × 5 rows; `CrossRegionAdjudicationResult`); module-level UPPER_SNAKE constants (Invariant I7) including `Q5_DECISION_IDS` (canonical 5-row ordered tuple: Q5A/Q5B/Q5C/Q5_selected_policy/Q5_per_family_impact_summary), `Q5_OPTION_NAMES` (3 CROSS-02-02 §6.2 row-5 options: `strict_exclusion`/`dual_feature_path`/`sensitivity_indicator_co_registration`), `CROSS_REGION_COLUMN_SOURCE_TABLE = "player_history_all"` + `CROSS_REGION_COLUMN_NAME = "is_cross_region_fragmented"` (B1: the cross-region column lives on PHA, not MFC), `ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS` (NIT-C enum: `toon_id_based`/`nickname_based`/`both`), `ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED` (NIT-D structured tri-valued enum: `yes`/`no`/`not_applicable`), `EXPECTED_CROSS_REGION_NICKNAME_COUNT = 246` + `EXPECTED_CROSS_REGION_TOON_ID_COUNT = 1923` + `EXPECTED_CROSS_REGION_PLAYER_MATCH_PAIR_COUNT_NICKNAME_ANCHORED = 32031` (01_05_10 nickname-anchored numeric anchors used by EQUIVALENCE probe only; not shared with the toon_id-membership BINDING probe per NIT-C); 4 pinned NIT-B SHA constants for `player_history_all.yaml` / `01_04_05_cross_region_annotation.md` / `matches_flat_clean.yaml` / `02_02_feature_engineering_plan.md` (silent drift halts before write); `EXPECTED_PR241_VALIDATOR_SHA256` re-asserted on every row (NIT-B binding); `HELPER_TO_FALSIFIER_KEY` and `FALSIFIER_PRIORITY_CHAIN` both contain exactly 31 entries with set-equality and no chain duplicates (B4 count invariants asserted at module import); public entrypoint `adjudicate_history_cross_region_retention(duckdb_path, parent_pr242_csv_path, parent_pr242_md_path, step_01_05_10_md_path, step_01_05_10_json_path, csv_path, md_path, audit_pr, audit_date, ...)`; read-only DuckDB probes (`_probe_cross_region_toonid_membership_count` for the BINDING toon_id-membership probe distinct from `_probe_cross_region_nickname_anchor_counts` for the EQUIVALENCE nickname-anchored probe per NIT-C; `_probe_strict_exclusion_retention`, `_probe_dual_feature_path_branches`, `_probe_sensitivity_indicator`, `_probe_family_level_impact`); structured `history_row_filter_on_pha_applied` field replaces the round-2 vacuous prose-substring assertion with the tri-valued enum (NIT-D; SQL byte-scan portion KEPT). B1/B2/B3 invariants preserved from PR #242 R1: B1 every probe reads `player_history_all.is_cross_region_fragmented` (MFC has no such column); B2 MFC join keys are `mfc.replay_id` / `mfc.toon_id` (NOT `mfc.match_id` / `mfc.player_id`); B3 `WHERE NOT ph.is_cross_region_fragmented` applied to PHA rows BEFORE aggregation. PR #243 Dispatch 3 OPTION (a) fix: the strict-exclusion retention probe's `history_rows_total` is now computed as `COUNT(*) FILTER (WHERE history_is_xr IS NOT NULL)` so cold-start target rows (LEFT-JOIN NULL on `history_is_xr`) are excluded from the kept+dropped==total invariant; the smoke falsifier measures retention strictly over rows with a matched PHA history record. `materialized_output_paths` is `""` on every row by construction. Halt-before-artifact discipline: no CSV / MD written when any falsifier fires.
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_cross_region_retention.py` — 194-test mirrored-tree test file covering every falsifier in the 31-entry `FALSIFIER_PRIORITY_CHAIN`, the NIT-C two-probe split (BINDING vs EQUIVALENCE), the NIT-D structured-field enum guard, the NIT-B four-SHA pinned anchor set, byte-determinism modulo provenance, halt-before-artifact discipline, and a real-DuckDB `skipif` smoke. Coverage ≥95% on the adjudicator module (≥95% gate per `pyproject.toml`).
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.py` and paired `.ipynb` — jupytext py:percent Q5 successor ADJUDICATION-only notebook. No `def` / `class` / `lambda` in cells; all logic imported from the Q5 adjudicator module. Per-Q5 hypothesis + falsifier markdown cells (Q5A strict_exclusion / Q5B dual_feature_path / Q5C sensitivity_indicator_co_registration / Q5_selected_policy with verdict-emergence discipline / Q5_per_family_impact_summary with NIT-D `not_applicable` tri-value). Single adjudication-call cell invokes the entrypoint against the real DuckDB + PR #242 parent CSV/MD + 01_05_10 evidence MD/JSON and asserts `passed`, `len(decisions) == 5`, `halting_falsifier is None`, plus per-decision NIT-B SHA binding. Closing cell preserves Q6 deferral and materialization-blocked statement.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.csv` — 30-column Q5 successor adjudication CSV (5 rows + 1 header; one row per `Q5_DECISION_IDS`). Q5A = `narrow_with_evidence` (cross_region_policy `strict_exclusion`; `history_row_filter_on_pha_applied = yes`; PHA history retention `kept=258,849 / total=1,576,919` measured strictly over rows with a matched history record). Q5B = `narrow_with_evidence` (cross_region_policy `dual_feature_path`; `history_row_filter_on_pha_applied = yes`). Q5C = `narrow_with_evidence` (cross_region_policy `sensitivity_indicator_co_registration`; `history_row_filter_on_pha_applied = no`; per-target boolean-OR flag distribution non-degenerate; anchored at `target.started_at`). Q5_selected_policy = `narrow_with_evidence` selecting `sensitivity_indicator_co_registration` (verdict EMERGES from the per-family retention table per A14; the selected option preserves the full PHA history population while co-registering the cross-region signal at target time). Q5_per_family_impact_summary = informational row aggregating strict-exclusion impact across the 6 tranche-2 family IDs; `history_row_filter_on_pha_applied = not_applicable` (NIT-D tri-valued enum). `materialized_output_paths` is `""` on every row; `audit_pr = "PR #243"` on every row; all 10 SHA-256 fields are 64-char lowercase hex.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.md` — multi-section Q5 successor adjudication MD (§1 non-materialization disclaimer · §2 parent PR #242 lineage · §3 Q5-only scope (Q6 out of scope) · §4 per-option decision table · §5 per-family retention table (BINDING evidence) · §6 SQL probe outputs verbatim per Invariant I6 (§6.1 BINDING toon_id-membership · §6.2 EQUIVALENCE nickname-anchored · §6.3 strict-exclusion retention · §6.4 dual-feature-path branch · §6.5 sensitivity-indicator · §6.6 family-level impact) · §7 toon_id-vs-nickname anchor semantics (NIT-C) · §8 target-filter vs history-filter distinction (B3) · §9 structured field explanation (NIT-D) · §10 materialization-blocked-until-Q6-resolved · §11 no-Q6-decision-here · §12 no-Step-closure-claim / no-Phase-03-start · §13 per-decision sections · §14 falsifier roll-call iterating `HELPER_TO_FALSIFIER_KEY.values()` · §15 SHA provenance).

### Changed

- `planning/INDEX.md` — archived PR #242 (master `e372e7b6`); promoted `feat/sc2egset-02-01-03-history-cross-region-adjudication` to the Active line as this Q5 successor adjudication execution PR.
- `pyproject.toml` — bumped `version = "3.73.0"` → `"3.74.0"` (minor; feat-family per `.claude/rules/git-workflow.md`).

### Notes

- **Scope: 9 execution files + 2 inherited planning files = 11 total branch content.** This PR's tracked diff is exactly the 9 execution files listed under Added/Changed; the 2 planning files (`planning/current_plan.md` + `planning/current_plan.critique.md`) are inherited from the Layer-1 planning sequence and are byte-unchanged on this branch.
- **Q5-only successor adjudication PR.** NO feature value is materialised. NO Parquet artifact is written under `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`. NO leakage-audit JSON / MD is written under `reports/artifacts/02_01_03/`. NO `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, or `PHASE_STATUS.yaml` flip. NO `research_log.md` entry (dataset or root). NO ROADMAP body edit (the 02_01_03 stub block from PR #239 is byte-unchanged). NO spec amendment. NO cleaning-layer YAML edit. NO Step `02_01_04`. NO Phase 03 work. NO baseline modelling.
- **Q6 rating reconstruction REMAINS `deferred_blocker` — OUT OF SCOPE for this PR.** Tracked as OQ1 in `planning/current_plan.md` for a future Q6 successor adjudication PR with rating-family empirical evaluation evidence satisfying the N-X3 strengthened gate. MATERIALIZATION REMAINS BLOCKED until BOTH Q5 AND Q6 are upgraded.
- **Version bump rationale.** Accepted from Layer-1 plan: minor bump (`3.73.0 → 3.74.0`) because this PR adds a new feat-family artifact pair and a new feat-family module (the Q5 successor adjudicator) per `.claude/rules/git-workflow.md`.
- **`HELPER_TO_FALSIFIER_KEY` and `FALSIFIER_PRIORITY_CHAIN` both 31 entries (set-equal per R4 B4 fix).** Both constants contain exactly 31 entries; the chain has no duplicates; the chain value-set equals the mapping value-set. The invariants are asserted at module import (`assert len(HELPER_TO_FALSIFIER_KEY) == 31`; `assert len(FALSIFIER_PRIORITY_CHAIN) == 31`; `assert len(set(FALSIFIER_PRIORITY_CHAIN)) == 31`; `assert set(FALSIFIER_PRIORITY_CHAIN) == set(HELPER_TO_FALSIFIER_KEY.values())`) and re-tested in `TestModuleImportInvariants`.

## [3.73.0] — 2026-05-24 (PR #242: feat/sc2egset-02-01-03-history-source-anchor-coldstart-adjudication)

### Added

- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` — adjudicator module for SC2EGSet Step 02_01_03 source/anchor/cold-start (history-enriched pre_game tranche; 6 families). Two frozen dataclasses (`HistoryEnrichedAdjudicationDecision` 33 fields × 8 rows; `HistoryEnrichedAdjudicationResult`); module-level UPPER_SNAKE constants (Invariant I7) including `EXPECTED_PR241_VALIDATOR_SHA256` (N4 binding to the PR #241 validator module), `STRICT_LT_HISTORY_FILTER` (B-X2 canonical `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at`), `STRICT_LT_FILTER_ROADMAP_RAW` (provenance-only raw form), `POST_GAME_TOKEN_SCOPED_FIELDS` (B-X1 the 3 scoped fields), `POST_GAME_TOKEN_EXEMPT_FIELDS` (B-X1 the 7 prose/evidence fields exempt; disjoint by module-load assertion), `IN_GAME_HISTORICAL_AGGREGATED_COLUMNS` (N1 deterministic 4-tuple), `HELPER_TO_FALSIFIER_KEY` (N-X1 mapping; exactly 20 entries; all values appear in the priority chain), `FALSIFIER_PRIORITY_CHAIN` (21-falsifier ordering); public entrypoint `adjudicate_history_enriched_pre_game_source_layer(duckdb_path, registry_csv_path, pr234_binding_csv_path, csv_path, md_path, audit_pr, audit_date)`; read-only DuckDB probes (`matches_flat_clean`, `matches_history_minimal`, `player_history_all`, strict-`<` smoke, TRY_CAST NULL-rate sample); 8-field provenance SHA-256 set re-hashed per run (ROADMAP, registry CSV, MHM YAML, CROSS-02-00/01/02/03 specs, PR #241 validator). `materialized_output_paths` is `""` on every row by construction. Halt-before-artifact discipline: no CSV / MD written when any falsifier fires.
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_enriched_pre_game_source_layer.py` — 159-test mirrored-tree test file covering all 21 falsifiers plus B-X1 scoped + exempt fields, B-X2 canonical-form cross-site, N-X1 helper-to-falsifier-key mapping completeness, N-X2 Q1 evidence, N-X3 Q6 evidence-sufficiency branches, N-X4 Q1 subfield disambiguation, byte-determinism modulo provenance, halt-before-artifact, real-registry + real-DuckDB `skipif` smokes. Coverage 98.48% on the adjudicator module (≥95% gate).
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.py` and paired `.ipynb` — jupytext py:percent ADJUDICATION-only notebook. No `def` / `class` / `lambda` in cells; all logic imported from the adjudicator module. Per-Q hypothesis + falsifier markdown cells (Q1 with N-X4 subfield disambiguation; Q3 + Q7 with B-X2 canonical TRY_CAST form). Single adjudication-call cell invokes the entrypoint against the real DuckDB + closed 02_01_01 registry + PR #234 binding CSV and asserts `passed`, `len(decisions) == 8`, `halting_falsifier is None`.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv` — 33-column adjudication CSV (8 rows + 1 header; one row per Q1-Q8). Q1 = `extend_with_evidence` (asymmetric: target=`matches_flat_clean`, history=`player_history_all`; 5 verbatim spec quotes recorded in `notes`). Q2 = `ratify_with_evidence` (`matches_history_minimal.started_at TIMESTAMP`). Q3 = `bind_now` (canonical TRY_CAST form). Q4 = `extend_with_evidence` (G-CS-2..5 bound; G-CS-6 distinguished as materialization-time gate). Q5 = `deferred_blocker` (3 options enumerated). Q6 = `deferred_blocker` (per N3 + N-X3 strengthened gate; ~83.95% MMR-missing density). Q7 = `bind_now` (`APM | SQ | supplyCappedPercent | header_elapsedGameLoops`). Q8 = `ratify_with_evidence` (NOT_A_FEATURE_SOURCE). `materialized_output_paths` is `""` on every row.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md` — multi-section adjudication MD (§1 non-overclaim disclaimer · §2-§9 per-Q decisions with verbatim SQL per Invariant I6 · §10 falsifier roll-call iterating `HELPER_TO_FALSIFIER_KEY.values()` · §11 lineage position · §12 explicit non-substitution statement · §13 materialization-blocked-until-deferred-resolved · §14 no-Step-closure-claim).

### Changed

- `planning/INDEX.md` — archived PR #241 (master `3c6709bf`); promoted `feat/sc2egset-02-01-03-history-source-anchor-coldstart-adjudication` to the Active line as this adjudication execution PR.
- `pyproject.toml` — bumped `version = "3.72.0"` → `"3.73.0"` (minor; feat-family per `.claude/rules/git-workflow.md`).

### Notes

- **Scope: 9 execution files + 2 inherited planning files = 11 total branch content.** This PR's tracked diff is exactly the 9 execution files listed under Added/Changed; the 2 planning files (`planning/current_plan.md` + `planning/current_plan.critique.md`) are inherited from the Layer-1 planning sequence and are byte-unchanged on this branch.
- **Adjudication-only PR.** NO feature value is materialised. NO Parquet artifact is written under `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`. NO leakage-audit JSON / MD is written under `reports/artifacts/02_01_03/`. NO `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, or `PHASE_STATUS.yaml` flip. NO `research_log.md` entry (dataset or root). NO ROADMAP body edit (the 02_01_03 stub block from PR #239 is byte-unchanged). NO spec amendment. NO cleaning-layer YAML edit. NO Step `02_01_04`. NO Phase 03 work. NO baseline modelling.
- **Q5 cross-region fragmentation remains DEFERRED.** The Q5 row is bound as `deferred_blocker` (not `bind_now`). The three CROSS-02-02 §6.2 row 5 options (strict_exclusion, dual_feature_path, sensitivity_indicator_co_registration) are all enumerated in the CSV row's `cross_region_policy` field per the `q5_cross_region_three_options_not_enumerated` falsifier, but no option is selected. MATERIALIZATION REMAINS BLOCKED until Q5 is upgraded to `bind_now` in a successor adjudication PR with retention-impact measurement evidence.
- **Q6 rating reconstruction model family remains DEFERRED.** The Q6 row is bound as `deferred_blocker` per the N3 default. The N-X3 strengthened evidence gate is satisfied: `evidence_paths` is non-empty (3 repo paths + 4 citations: Elo 1978, Glickman 1999, Glickman 2012, Herbrich/Minka/Graepel 2006); `notes` contains the substring `deferred_blocker because:` and the three forward-only phrases (`no target-match outcome`, `no future results`, `no global batch fit`) plus `cold-start handled by` and `missingness handled by`. MATERIALIZATION REMAINS BLOCKED until Q6 is upgraded to `bind_now` in a successor adjudication PR with rating-family empirical evaluation evidence.
- **Status YAMLs byte-unchanged.** No `02_01_03` row is added to `STEP_STATUS.yaml` at adjudication time (per PR #234 precedent for the 02_01_02 adjudication). Pipeline Section `02_01` remains `complete`; Phase `02` remains `in_progress`; Phase `03` remains `not_started`.
- **PR #241 SHA-256 binding (N4).** Every CSV row carries `pr241_scaffold_validator_module_sha256 = b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904` as the constant-bound SHA of the PR #241 validator module. Mismatch halts via `pr241_sha256_mismatch`.
- **B-X1 forbidden POST-GAME token scope** — scanning is limited to `selected_source_layer`, `feature_family_id_or_scope`, `materialized_output_paths`. Prose / evidence / falsifier-name fields (`notes`, `evidence_paths`, `falsifiers`, `decision_name`, `rationale`, `source_layer_divergence_reason`, `history_source_extension_reason`) are exempt — negated rationale (e.g. `no target-match outcome`) is allowed in `notes`. The disjointness invariant is asserted at module load.
- **B-X2 canonical strict-`<` form** — the canonical filter expression `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at` is the single source of truth for any executable strict-`<` site inside the module (Q3 `history_time_column`, Q7 `strict_lt_expression`, T02 smoke probe SQL). The ROADMAP §02_01_03 raw form `ph.details_timeUTC < target.started_at` is recorded as `STRICT_LT_FILTER_ROADMAP_RAW` for provenance only and is rejected at any executable site by `strict_lt_filter_divergence`.

## [3.72.0] — 2026-05-24 (PR #241: feat/sc2egset-02-01-03-history-scaffold)

### Added

- `src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py` — scaffold-only validator module for SC2EGSet Step 02_01_03 (history-enriched pre_game tranche; 6 families). Two frozen dataclasses (`HistoryEnrichedPreGameTrancheRow`, `HistoryEnrichedScaffoldValidationResult`); module-level UPPER_SNAKE constants (Invariant I7) including `HISTORY_TRANCHE2_FAMILY_IDS` (frozenset of the 6 family IDs), `EXPECTED_TRANCHE2_COUNT = 6`, `ALLOWED_HISTORY_COLD_START_GATES = {G-CS-2, G-CS-3, G-CS-4, G-CS-5}` (registry-bound; G-CS-6 is the materialization-time fold-aware fit gate per CROSS-02-02 §9 and is intentionally excluded), `IN_GAME_HISTORICAL_AGGREGATED_COLUMNS = (APM, SQ, supplyCappedPercent, header_elapsedGameLoops)` (CROSS-02-00 §5.4 Concern 8 / T15 record), `STALE_REGISTRY_FILENAME_FRAGMENT` (mirrors tranche-1 stale-filename guard); public loader `load_history_enriched_pre_game_tranche_rows` and public entrypoint `validate_history_enriched_pre_game_materialization(registry_csv_path, designed_column_names, designed_in_game_historical_columns)`; 11 private `_check_*` helpers; 16-falsifier priority chain (`missing_families_in_tranche` → `extra_history_in_tranche` → `pre_game_in_history_tranche` → `in_game_in_history_tranche` → `blocked_in_history_tranche` → `tranche_count_mismatch` → `wrong_prediction_setting` → `wrong_temporal_anchor` → `cutoff_not_strict` → `tracker_source_in_history` → `asymmetric_construction` → `post_game_token` → `cross_region_caveat_missing` → `in_game_historical_column_out_of_scope` → `cold_start_gate_invalid` → `status_not_admissible`); `materialized_output_paths` always `()`.
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py` — 39-test mirrored-tree test file covering all 16 falsifiers across 20 test classes. Synthetic `tmp_path` CSV fixtures (`_history_tranche_row` builder, `_all_six_tranche_rows` helper); deterministic cross-region priority pair (removal fires priority-1 `missing_families_in_tranche`; status-flip fires priority-13 `cross_region_caveat_missing`); real-registry `skipif` smoke (7 assertions: passed, count=6, no halting falsifier, missing=(), materialized_output_paths=(), cross_region status, frozenset match). Coverage 98% on the validator module (≥95% gate).
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py` and paired `.ipynb` — jupytext py:percent SCAFFOLD-only notebook (14 cells: title, no-materialization banner, imports, design table, context/input artifacts, MHM consumption documentation, view-vs-raw deferral, three-concept distinction (CROSS-02-00 §5.4 + CROSS-02-02 §6.2), projection design (SPECIFIED, NOT EXECUTED), cross-region adjudication DEFERRED (with §10 verdict-audit re-run vs justification deferral sentence), rating reconstruction model choice DEFERRED, validator-call cell, closing). No `def` / `class` / lambda in cells; all logic imported from the validator module.

### Changed

- `planning/INDEX.md` — archived PR #239 (master `f378f6f4`) and PR #240 (master `33e3c681`); promoted `feat/sc2egset-02-01-03-history-scaffold` to the Active line as this scaffold execution PR.
- `pyproject.toml` — bumped `version = "3.71.0"` → `"3.72.0"` (minor; feat-family per `.claude/rules/git-workflow.md`).

### Notes

- **Scope: 7 execution files + 2 inherited planning files = 9 total branch content.** This PR's tracked diff is exactly the 7 execution files listed under Added/Changed; the 2 planning files (`planning/current_plan.md` + `planning/current_plan.critique.md`) are inherited from the Layer-1 planning PR #240 and are byte-unchanged on this branch.
- **Scaffold-only PR.** NO feature value is materialised. NO Parquet/CSV/JSON/MD artifact is written. NO `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, or `PHASE_STATUS.yaml` flip. NO `research_log.md` entry (dataset or root). NO ROADMAP body edit (the 02_01_03 stub block from PR #239 is byte-unchanged). NO spec amendment. NO cleaning-layer YAML edit. NO Phase 03 work. NO Step 02_01_04 work. NO baseline modeling. The tranche-2 source/anchor/cold-start adjudication, materialization-execution plan, materialization-execution, post-materialization audit, and closure are produced by SEPARATE FUTURE PRs per `.claude/rules/data-analysis-lineage.md` "Non-batching rule for empirical work" sequence steps 3-9.
- **Status YAMLs byte-unchanged.** No `02_01_03` row is added to `STEP_STATUS.yaml` at scaffold time (per PR #233 precedent for the 02_01_02 scaffold). Pipeline Section `02_01` remains `complete`; Phase `02` remains `in_progress`; Phase `03` remains `not_started`.
- **Cross-region adjudication DEFERRED.** The validator accepts the registry's `cross_region_fragmentation_handling` row with `status=allowed_with_caveat` and does NOT pin a policy choice between (a) strict-exclusion, (b) dual-feature-path, or (c) sensitivity-indicator co-registration. The choice is empirically conditional (retention measurement) and is DEFERRED to the future tranche-2 source/anchor/cold-start adjudication PR (the tranche-2 analogue of PR #234 for tranche-1).
- **Rating reconstruction model choice DEFERRED.** Glicko-2 vs Elo vs TrueSkill vs Glicko is DEFERRED to the materialization PR; the scaffold records only `G-CS-4` as the declared cold-start gate.
- **View-vs-raw source layer DEFERRED.** The registry CSV records `matches_flat` (raw layer); the ROADMAP `inputs.duckdb_tables` lists `matches_flat_clean` (1v1-scoped view used by tranche-1 per PR #234 Q1). This is a known divergence DEFERRED to the future tranche-2 adjudication PR; the scaffold validator binds to the registry as authoritative.

## [3.71.0] — 2026-05-24 (PR #239: feat/sc2egset-02-01-03-roadmap-stub)

### Added

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` — inserted Step `02_01_03` yaml block (History-enriched pre_game feature-family materialization (sc2egset)) under Pipeline Section `02_01 — Pre-Game vs In-Game Boundary`, immediately after the closed Step `02_01_02` block. The block declares the 6 `history_enriched_pre_game` families: `focal_player_history`, `opponent_player_history`, `matchup_history_aggregate`, `reconstructed_rating`, `cross_region_fragmentation_handling` (the only `allowed_with_caveat` row; leakage mode `cross_region_history_drop`; RISK-20), `in_game_history_aggregate` (note: `history_enriched_pre_game` prediction setting, NOT `in_game_snapshot`; aggregates IN_GAME_HISTORICAL columns over PRIOR matches per CROSS-02-02 §6.2 row 6).
- Strict history cutoff `ph.details_timeUTC < target.started_at` recorded in the block's `method` and `gate.halt_predicate` fields, with explicit enumeration of CROSS-02-02 §10 leakage gates G-L-1 (no `<=`), G-L-3 (no target-match final state), G-L-4 (no rating-uses-game-T-outcome), G-L-7 (no rolling/h2h includes target). Cold-start gates G-CS-2 through G-CS-6 listed for tranche-2 cold-start handling.
- Future post-materialization audit obligation: `gate.continue_predicate` requires a NON-vacuous CROSS-02-01-v1.0.1 PASS (`future_leak_count = 0`, `post_game_token_violations = 0` over a non-empty `features_audited` covering all 6 history families' materialized columns) plus a re-executed §10 audit over the 6 history rows (distinct from PR #229's design-time audit) — OR a non-vacuous justification for not re-running, recorded in the future materialization PR's `research_log` entry.
- `predecessors: "02_01_02"` only (string scalar; `02_01_01` is a transitive predecessor and is NOT listed as a direct predecessor per the reviewer-adversarial N4 resolution).

### Notes

- **ROADMAP-only PR.** NO feature value is materialized. NO notebook scaffold, NO validator, NO source/test/module, NO Parquet/CSV artifact, NO materialization, NO post-materialization audit, NO status YAML flip, NO `research_log` entry, NO `INVARIANTS.md` edit, NO spec amendment, NO cleaning-layer YAML edit, NO Phase 03 work, NO baseline modeling. The notebook scaffold + one validation module, tranche-2 source/anchor/cold-start adjudication, materialization-execution plan, materialization-execution, and closure are produced by SEPARATE FUTURE PRs per `.claude/rules/data-analysis-lineage.md` "Non-batching rule for empirical work" sequence steps 2-9.
- **Status YAMLs byte-unchanged.** `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml` are not updated. No `02_01_03` row is added to `STEP_STATUS.yaml` at ROADMAP-stub time (per PR #232 precedent for `02_01_02`'s ROADMAP-stub); the row will be added at the future closure PR for Step `02_01_03`. Pipeline Section `02_01` therefore remains `complete` per the YAML-derivation rule (all currently-tracked steps `02_01_01` and `02_01_02` are complete). Phase `02` remains `in_progress`; Phase `03` remains `not_started`.
- **Six reviewer-adversarial nits from PR #238 incorporated into the inserted block.** N1 G-L-3 explicit; N2 IN_GAME_HISTORICAL retention note for `in_game_history_aggregate`; N3 lineage-position framing (artifact #1 of N for Step 02_01_03 readiness); N4 `predecessors: "02_01_02"` string scalar; N5 cross-region adjudication gating in `halt_predicate`; N6 §10 audit re-run gating in `continue_predicate`.
- **Layer-2 of the 02_01_03 planning sequence.** PR #238 merged the Layer-1 plan + critique. This Layer-2 PR inserts the ROADMAP block + version/CHANGELOG/INDEX tail. No follow-up PR is opened in this run; the future scaffold/validator/materialization/audit PRs are deferred to separate explicit prompts.
- **No baseline modeling.** Phase 03 work (Splitting & Baselines) is barred per `PHASE_STATUS.yaml` Phase 03 `not_started`; only 1 of 8 Phase-02 pipeline sections is `complete` per `PIPELINE_SECTION_STATUS.yaml`.

## [3.70.1] — 2026-05-24 (PR #237: chore/sc2egset-02-01-02-formal-closure)

### Changed

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` — added `"02_01_02"` row (`name: "First pre_game feature-family materialization (sc2egset)"`, `pipeline_section: "02_01"`, `status: complete`, `completed_at: "2026-05-23"`) immediately after the existing `02_01_01` row. `completed_at` uses the PR #236 audit-evidence date (not the closure-PR open/merge date) per the `STEP_STATUS.yaml` evidence-date convention.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` — appended a reverse-chronological closure entry above the PR #236 entry, recording `closure_status: closed`, `materialization_state: materialized`, `leakage_audit_state: post_materialization_pass`, `status_yaml_state: complete`, `features_audited_count: 7`, `row_count: 44418`, the Parquet + audit artifact paths from PR #236, and the explicit non-closure of Step 02_01_03 + Phase 03. The PR #236 baseline entry (`closure_status: still_open`) is preserved byte-unchanged as historical evidence.
- `planning/INDEX.md` — archived PR #236 with master merge commit `39298c0a`; promoted `chore/sc2egset-02-01-02-formal-closure` to the Active line.

### Notes

- **Formal closure of Step 02_01_02 only.** PR #237 creates **NO new on-disk artifact** (no Parquet, no audit JSON/MD, no notebook, no module, no test, no spec, no cleaning-layer YAML edit, no ROADMAP body edit, no `INVARIANTS.md` edit, no root `reports/research_log.md` edit). PR #236 remains the materialization/audit evidence PR; PR #237 only records that Step 02_01_02 is now `complete` in the status chain.
- **NO Parquet or audit regeneration.** `02_01_02_pre_game_features.parquet`, `02_01_02/leakage_audit_sc2egset.json`, and `02_01_02/leakage_audit_sc2egset.md` are byte-unchanged from PR #236.
- **NO source / test / notebook / module edit.** `materialize_pre_game_features.py`, `test_materialize_pre_game_features.py`, the sandbox notebook pair, and every other source / test / module under `src/rts_predict/**.py` and `tests/**.py` are byte-unchanged.
- **NO ROADMAP / spec / cleaning-layer YAML / `INVARIANTS.md` patch.**
- **NO root `reports/research_log.md` edit.**
- **NO Step 02_01_03 work** and **NO Phase 03 work** is started or implied by this PR.
- **`PIPELINE_SECTION_STATUS.yaml` byte-unchanged.** `02_01` remains `complete` per the YAML header rule "Pipeline section is complete when ALL its steps are complete." Both `02_01_01` and `02_01_02` are now `complete`; ALL steps in `02_01` are complete; the derivation rule yields `complete`. **Reconciliation with PR #236 audit JSON `notes` re-derivation language.** The PR #236 audit JSON `notes` field on master reads: "PIPELINE_SECTION_STATUS 02_01 = complete remains derived from STEP_STATUS until a future PR adds 02_01_02 to STEP_STATUS, at which point YAML-derivation re-derives 02_01 = in_progress (intended behaviour, pre-disclosed in PR #230 CHANGELOG Notes)." That sentence was conditioned on the successor landing with status `in_progress` (the typical scaffold-style path). This closure lands the successor directly with status `complete`, so the more-specific "ALL steps complete" clause of the derivation rule dominates and re-derivation yields `complete`. PR #232 and PR #234 plan bodies anticipated this exact case ("if the successor lands with status `complete` directly, the section stays `complete`"). The PR #236 audit JSON is NOT amended by this PR; the reconciliation is recorded here in this CHANGELOG `[3.70.1]` Notes block as the authoritative location.
- **`PHASE_STATUS.yaml` byte-unchanged.** Phase 02 remains `in_progress` (only `02_01` is complete among 8 canonical pipeline sections per `docs/PHASES.md`); Phase 03 remains `not_started`.
- **Branch prefix `chore/` + patch version bump.** PR #230 used `feat/` + minor (3.64.0 → 3.65.0) because it created 2 new audit artifacts; the present closure creates no new on-disk artifact, so `chore/` + patch (`3.70.0 → 3.70.1`) is the consistent choice per `.claude/rules/git-workflow.md` ("minor for feat/refactor/docs, patch for fix/test/chore").
- PR #229 §10 verdict-audit pair, PR #230 vacuous catalog audit pair, PR #233 scaffold validator + tests, PR #234 source/anchor/race adjudication CSV+MD, PR #235 Layer-1 plan, and PR #236 materialization Parquet + audit JSON+MD remain byte-unchanged at their distinct paths.

## [3.70.0] — 2026-05-23 (PR #236: feat/sc2egset-02-01-02-pre-game-materialization-execution)

### Added

- `src/rts_predict/games/sc2/datasets/sc2egset/materialize_pre_game_features.py` — materialization + post-materialization audit module; frozen `MaterializationResult` + `AuditResult` dataclasses; module-level UPPER_SNAKE constants (Invariant I7); named SQL constants with `_QUERY` suffix (`_MATERIALIZATION_QUERY` reproduces the full projection — Invariant I6); public entrypoints `materialize_pre_game_features(duckdb_path, output_parquet_path, registry_csv_path)` and `run_post_materialization_audit(parquet_path, audit_json_path, audit_md_path, duckdb_path, audit_date, dataset, phase_02_step, audit_pr)`; 22 falsifiers implemented (incl. F-row-count-mismatch, F-symmetry-violation, F-race-vocabulary-drift, F-is-mmr-missing-distribution-drift, F-selectedRace-projected, F-post-game-token-projected, F-scalar-mmr-projected, F-tracker-source-read, F-history-window-leakage, F-features-audited-empty, F-features-audited-not-7, F-context-column-counted-as-feature, F-examiner-clarity-sentence-missing); examiner-clarity sentence embedded verbatim in BOTH the audit JSON `notes` and the audit MD §1.
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_pre_game_features.py` — 45-test mirrored-tree test file; synthetic `tmp_path` DuckDB fixtures (10-replay generator with configurable race vocab, MMR-missing flag, map name, patch); real-DB `skipif` smoke (row count, MMR distribution, audit JSON schema, examiner-clarity sentence presence, PR #234 binding hash check, PR #230 byte-preservation, reproducibility across runs); direct `_evaluate_materialization_falsifiers` / `_evaluate_audit_falsifiers` coverage on every halting label; ≥95% coverage.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet` — 44,418 rows × 11 projected cols (3 IDENTITY: `focal_match_id`, `focal_player`, `opponent_player`; 1 CONTEXT row-identity anchor: `started_at`; 7 audited PRE_GAME features: `focal_race`, `opponent_race`, `race_pair`, `map_type`, `patch_version`, `focal_is_mmr_missing`, `opponent_is_mmr_missing`); ZSTD compression; 100,000-row groups.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json` — first non-vacuous CROSS-02-01-v1.0.1 §3 audit JSON for Step 02_01_02; `features_audited` = exactly the 7 PRE_GAME feature columns; `projected_context_columns = ["started_at"]`; `projected_identity_columns = ["focal_match_id", "focal_player", "opponent_player"]`; `verdict = PASS`; full SHA-256 provenance bonds (PR #234 binding CSV+MD, registry CSV, 4 CROSS-02-NN specs, 3 cleaning-layer YAMLs, methodology risk register, materialization module, materialized Parquet).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.md` — 8-section MD companion; verbatim `_MATERIALIZATION_QUERY` per Invariant I6; verbatim `matches_flat_clean.yaml:178-189` provenance block + registry-cell upstream-source → MFC cleaned-view binding paragraph; examiner-clarity sentence verbatim in §1; non-overclaim disclaimer; non-substitution + lineage statement.

### Changed

- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.py` + `.ipynb` — jupytext py:percent banner promoted from "SCAFFOLD + ONE VALIDATION MODULE" to "MATERIALIZATION + POST-MAT AUDIT (non-batching sequence steps 6-8 of 9)"; PR #233 scaffold cells preserved for lineage; new cells appended for imports (with `SET TimeZone = 'UTC'` per CROSS-02-00 §3.3, applied by the module on the DuckDB session), PR #234 frozen-inputs context, materialization call with assertions on row count / column order / halting falsifier, audit call with assertions on `verdict = PASS` / 7-tuple `features_audited` / role-partition disjointness; closing cell rewritten to record what was persisted (Parquet + non-vacuous audit JSON+MD) and what was NOT done (status YAML flips deferred to U2.B closure PR).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` — append-only entry at top recording materialization-execution PR #236: `closure_status: still_open`, `leakage_audit_state: post_materialization_pass`, `features_audited_count: 7`, `row_count: 44418`, explicit "Step 02_01_02 NOT closed by this PR" statement, status YAML flips deferred to U2.B closure PR, Phase 03 not started.
- `planning/INDEX.md` — archive PR #235 (merged 2026-05-23 at master `3b4340cb`) with the materialization-execution Layer-1 plan summary; promote PR #236 active line for this execution PR.

### Notes

- No status YAML flip: `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml` byte-unchanged. Step 02_01_02 closure is deferred to a separate U2.B closure PR per the merged Layer-1 plan (`planning/current_plan.md` §Open Questions OQ1 / §File Manifest closure-PR row).
- No ROADMAP edit (the 02_01_02 stub block from PR #232 is untouched).
- No spec amendment (CROSS-02-02 §6.1 minor amendment proposed in PR #234 §8 remains future-PR target).
- No cleaning-layer YAML patch (`matches_flat_clean.yaml`, `matches_history_minimal.yaml`, `matches_long_raw.yaml` byte-unchanged).
- No Phase 03 or 02_01_03+ work.
- PR #230 audit JSON at `02_01_01/leakage_audit_sc2egset.json` is byte-unchanged (vacuous `features_audited == []` historical record preserved at its distinct path).
- PR #234 adjudication artifacts at `02_01_02_source_anchor_race_adjudication.{csv,md}` are byte-unchanged.
- PR #233 scaffold validator + tests are byte-unchanged.
- ChatGPT second-pass leakage review (GPT-5.2 Thinking, 2026-05-23) returned APPROVE on the exact `_MATERIALIZATION_QUERY`; verdict quoted verbatim in `planning/current_plan.md` §Open Questions with ISO date.
- Q1 source layer = `matches_flat_clean`; Q2(a) Phase-02 row-identity = `started_at TIMESTAMP` (`use_as_window_bound = false`); Q3 = RATIFY (`race`, not `selectedRace`).
- Version bump 3.69.0 → 3.70.0 per git-workflow rule (minor for `feat`; new on-disk feature Parquet + audit JSON+MD + module + 45 tests + research_log entry).

## [3.69.0] — 2026-05-23 (PR #234: feat/sc2egset-02-01-02-source-anchor-race-adjudication)

### Added

- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.py` + `.ipynb` — jupytext py:percent adjudication notebook (Layer-2 execution); cells: banner (NON-MATERIALIZATION; ONE artifact pair; no status/research_log/ROADMAP/spec/YAML/Phase-03 changes) → imports → context (specs, cleaning-layer YAMLs, registry CSV, PR #229 §10 verdict CSV, PR #230 vacuous leakage JSON, RISK-26 register) → 3-decision question table → run `adjudicate_pre_game_source_layer(...)` → print `result.passed`, count of decisions, artifact paths, halting falsifier → closing non-substitution + future-gate statement. No `def`/`class`/lambda in cells; no DuckDB `CREATE`/`INSERT`/`COPY`/`to_parquet`.
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_pre_game_source_layer.py` — adjudication module; frozen dataclasses `SourceLayerCandidate`, `AnchorCandidate`, `RaceColumnCandidate`, `AdjudicationDecision`, `AdjudicationResult`; module-level UPPER_SNAKE constants (Invariant I7); named SQL constants with `_QUERY` suffix; public entrypoint `adjudicate_pre_game_source_layer(duckdb_path, registry_csv_path, output_artifact_dir)`; private helpers `_run_source_layer_peeks`, `_run_anchor_peeks`, `_run_race_and_random_peeks`, `_adjudicate_source_layer`, `_adjudicate_anchor`, `_adjudicate_race_and_random`, `_render_artifact_csv`, `_render_artifact_md`; 18 falsifiers implemented; `materialized_output_paths` always `()`.
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_pre_game_source_layer.py` — test file; synthetic `tmp_path` DuckDB fixtures + real-DB `skipif` smoke; 33 tests covering: 3-decision shape, rationale ≥ 80 chars, `materialized_output_paths==()`, `q1_no_evidence`, `q2_anchor_type_mismatch`, `q3_prior_decision_silently_reversed`, `q3_random_vocabulary_dropped`, `q1_source_1v1_lost`, stale-path, real-DB smoke (5 assertions), MHM-faction-Random absence (3 assertions), private-helper coverage (7 tests).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv` — 3-row deterministic adjudication CSV; 24 columns including all required provenance hashes (validator module, DuckDB, registry CSV, methodology risk register, four CROSS-02-NN specs, two cleaning-layer YAMLs); `audit_pr=PR #234`.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.md` — 8-section MD companion; verbatim peek SQL per Invariant I6; Q3.RATIFY and Q3.AMEND both presented; chosen outcome Q3.RATIFY with rationale ≥ 250 words; falsifier roll-call (18 falsifiers); `lineage_position` = artifact #4 in 5-artifact lineage; explicit non-substitution statement; spec-amendments-proposed (NOT applied).

### Notes

- No feature materialization: NO feature value computed or written; NO Parquet/CSV feature table; NO `reports/artifacts/02_01_02/leakage_audit_*` file.
- No status YAML flip: STEP_STATUS, PIPELINE_SECTION_STATUS, PHASE_STATUS byte-unchanged.
- No `research_log` entry written.
- No ROADMAP edit.
- No spec or cleaning-layer YAML patch (`matches_long_raw.yaml`, `matches_history_minimal.yaml`); amendments proposed in artifact MD §8 only.
- No Phase 03 or 02_01_03+ work.
- PR #230 `leakage_audit_sc2egset.json` unchanged (`features_audited==[]`; vacuity holds).
- Post-materialization CROSS-02-01 audit and mandatory Claude/ChatGPT second-pass leakage review remain FUTURE. Distinct gates; not discharged by this artifact.
- Q1 source layer = `matches_flat_clean` (cleaned-raw, 1v1-scoped native; 22,209 × 2 = 44,418).
- Q2(a) Phase-02 row-identity = `started_at` TIMESTAMP from MHM (canonical per CROSS-02-00 §3.1); `details_timeUTC` retained as provenance only. Q2(b) Phase-03 hold-out = `started_at` TIMESTAMP RECOMMENDATION ONLY; Phase 03 planning binds.
- Q3 = RATIFY cleaning-layer convention (`race` = PRE_GAME per `matches_long_raw.yaml:101-103` and `matches_history_minimal.yaml:52-53`; `selectedRace` excluded). RISK-26 gap = documented_gap; CROSS-02-02 §6.1 minor amendment proposed as future-PR target. Not applied.
- Version bump 3.68.0 → 3.69.0 per git-workflow rule (minor for feat; new on-disk artifact pair + validator module + tests added).

## [3.68.0] — 2026-05-23 (PR #233: feat/sc2egset-02-01-02-pre-game-materialization-scaffold)

### Added

- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.py` + `.ipynb` — jupytext py:percent notebook scaffold (non-batching sequence step 2 of 9); banner declares SCAFFOLD + ONE VALIDATION MODULE; cells: banner → imports → context/inputs → 5-family tranche design table → projection design markdown (snapshot_at_match_start cutoff; no history `<` filter; symmetric focal/opponent self-join; is_mmr_missing framed as missingness/provenance, not skill) → designed column-names tuple → run validator → closing "nothing persisted / no status flipped" cell. No `def`/`class`/lambda in cells; no DuckDB `CREATE`/`INSERT`/`COPY`/`to_parquet`.
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_pre_game_feature_materialization.py` — validation module; `PreGameTrancheRow` + `PreGameScaffoldValidationResult` frozen dataclasses; public entrypoint `validate_pre_game_feature_materialization(registry_csv_path, designed_column_names)`; allowlist-first + boundary-aware token-equality `_is_forbidden_skill_column` (ChatGPT second-pass correction — approved `is_mmr_missing` flag names pass while scalar MMR/rating/skill columns are rejected); checks: 5-family tranche membership, no-tracker, no-history-in-tranche, no-in-game-in-tranche, symmetry, no-POST-GAME-token, approved-source-table, is-flag-not-skill, forbidden-skill-column; `materialized_output_paths` always `()`; writes nothing.
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_pre_game_feature_materialization.py` — test file; synthetic `tmp_path` CSVs + real-CSV `skipif` smoke; covers: 5-family membership, extra-family rejection, is_mmr_missing flag framing, allowlist PASS / scalar-MMR/rating/skill FAIL / no-false-positive edge cases (cumulative/summary/skillset_id/elong), stale `_sc2egset` path rejected, tracker/history/in-game rejection, asymmetric rejection, POST-GAME-token rejection, `materialized_output_paths==()`, PR #230 leakage JSON vacuity unchanged, real-registry smoke.

### Notes

- No materialization: NO feature value computed or written; NO Parquet/CSV/JSON/MD artifact.
- No status YAML flip: STEP_STATUS, PIPELINE_SECTION_STATUS, PHASE_STATUS byte-unchanged.
- No `research_log` entry written.
- No ROADMAP edit.
- No Phase 03 work.
- PR #230 `leakage_audit_sc2egset.json` unchanged (`features_audited==[]`); vacuity holds.
- ChatGPT second-pass MMR-missingness allowlist + boundary-aware token-equality correction included: `APPROVED_MMR_MISSINGNESS_TOKENS` = `{is_mmr_missing, is_mmr_missing_flag, focal_is_mmr_missing, opponent_is_mmr_missing}` (closed allowlist); `_is_forbidden_skill_column` uses token equality, never substring.
- `is_mmr_missing_flag` stays tranche 1 as a pre-game missingness/provenance flag — NOT a skill feature; scalar MMR/rating proxies remain forbidden/deferred.
- The mandatory Claude/ChatGPT second-pass leakage review over focal/opponent projection SQL remains REQUIRED before any future materialization PR.

## [3.67.0] — 2026-05-22 (PR #232: feat/sc2egset-02-01-02-roadmap-stub)

### Added

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` — inserted the Step `02_01_02` ROADMAP stub (first `pre_game` feature-family materialization design) under Pipeline Section `02_01`: declares materialization of the 5 allowed `pre_game` registry families only (`focal_race_with_opponent_race_pair`, `map_type_encoded`, `patch_version_encoded`, `matchup_encoded`, `is_mmr_missing_flag`); `predecessors: "02_01_01"`; full temporal/leakage/cold-start/SQL design recorded as a declaration only. Insertion-only; the closed `02_01_01` block and the Phase 03 placeholder are byte-unchanged.

### Notes

- ROADMAP-only PR: NO notebook scaffolded, NO artifact generated, NO feature value materialized, NO status YAML flip, NO `research_log.md` entry, NO Phase 03 work.
- `is_mmr_missing_flag` is kept in tranche 1 as a pre-game missingness/provenance flag (NOT a skill feature); the 6 `history_enriched_pre_game` and 11 `in_game_snapshot` families are deferred to Steps `02_01_03+`.
- Pipeline Section `02_01` remains `complete` because this ROADMAP-only PR adds NO `STEP_STATUS` row. The YAML-derived re-derivation of `02_01 → in_progress` occurs only when `02_01_02` later executes and lands a `STEP_STATUS` row (intended behaviour, pre-disclosed in the PR #230 status-reopen note).
- PR #229 §10 design-time verdict-audit evidence and PR #230 / future post-materialization CROSS-02-01 evidence are kept distinct.

## [3.66.0] — 2026-05-22 (PR #231: docs/thesis-pass2-020101-manifest-closure-reconciliation)

### Changed

- `thesis/pass2_evidence/notebook_regeneration_manifest.md` — OQ4 reconciliation with the PR #230 catalog-only closure of SC2EGSet Step 02_01_01: added the new `catalog_only_closed_zero_materialization` status token; re-tokenized the `02_01_01_feature_family_registry_skeleton.py` row off the now-false `partial_coverage_v9_baseline` (the row no longer says "no Step closure"); added 2 Phase-02 rows (the PR #229 §10 verdict-audit notebook and the PR #230 hand-written CROSS-02-01 artifact pair), all 3 carrying the new token; updated the Summary "Last updated" + Change note + footnote (footnote accounting, not a new column); `confirmed_intact` total unchanged.
- `planning/INDEX.md` — archived PR #230 (merged 2026-05-22 at master `0c45c490`); new Active line for `docs/thesis-pass2-020101-manifest-closure-reconciliation` (PR #231).

### Notes

- **Thesis-lineage bookkeeping only.** No status YAML, artifact, notebook, source, test, dataset/root `research_log`, or thesis chapter changed. PR #230's closure is preserved untouched: Step 02_01_01 closed at the catalog-only registry layer; Phase 02 `in_progress`; Step 02_01_02 NOT started; Phase 03 NOT started.
- The new token asserts catalog-layer closure ONLY; a future post-materialization CROSS-02-01 audit remains REQUIRED before any empirical leakage-clearance claim.

## [3.65.0] — 2026-05-21 (PR #230: feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit)

### Added

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json` (NEW; CROSS-02-01-v1.0.1 zero-materialization closure stub for the catalog-only registry layer; verdict=PASS justified on §5(a) vacuity + §3/§5(c) artifact-presence at the spec-named path; features_audited=[]).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.md` (NEW; companion MD with the 8 prescribed sections: (1) top non-overclaim disclaimer, (2) §3 spec citation verbatim, (3) §5(a) vacuity argument, (4) §3/§5(c) artifact-presence argument, (5) explicit non-substitution statement, (6) verdict justification, (7) OQ1-RESOLVED cross-reference, and (8) the standalone "Audit queries: none — vacuously satisfied" section).
- New `research_log.md` entry in `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (Step 02_01_01 closure; `closure_status: closed`; `leakage_audit_state: zero_materialization_pass`; PR #230).

### Changed

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` — added `"02_01_01": complete`.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` — added `"02_01": complete` (phase: "02", name: "Pre-Game vs In-Game Boundary").
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` — Phase 02 `not_started` → `in_progress`.
- `planning/INDEX.md` — PR #229 archived (merged 2026-05-21 at master `a14dc547`); new Active plan line for `feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit`.
- `pyproject.toml` — version 3.64.0 → 3.65.0.

### Notes

- **This PR closes Step 02_01_01 at the catalog-only registry layer.** Closure is justified on the zero-materialization CROSS-02-01 leakage-audit artifact pair (verdict=PASS) at the spec-named path plus the §5(a) vacuity argument on the empty materialized set. No feature column is materialized by this PR.
- **Status-reopen disclosure.** PIPELINE_SECTION_STATUS `02_01 = complete` is YAML-derived from STEP_STATUS per the file header rule "Pipeline section is complete when ALL its steps are complete." If a future PR adds a successor step (e.g., `02_01_02`) to STEP_STATUS with status `in_progress`, the derivation chain will re-derive `02_01 = in_progress`. This is intended YAML-derivation behaviour, not silent revisionism. No regression is implied by a future `02_01 = in_progress` value.
- **Non-substitution disclaimers.** The new artifact pair does NOT substitute for the PR #229 §10 verdict-audit CSV+MD pair (which audits CROSS-02-03 §10 design-time per-family verdicts for all 26 catalog rows). The new artifact pair does NOT substitute for a future post-materialization CROSS-02-01 audit that any later 02_01 materialization step will require. The new artifact pair does NOT make Step 02_01_01 a materialization step; Step 02_01_01 remains catalog-only.
- **OQ1 RESOLVED pre-execution.** The JSON field `normalization_fit_scope = "training_fold_only"` is the spec-permitted PASS value (alternative beta), vacuously satisfied on empty `features_audited` at the catalog-only layer (no normalizer was fit). Treatment is symmetric to `target_encoding_fold_awareness` (`N/A_no_target_encoding` — spec-permitted) and `cutoff_time_filter_structural_check` / `reference_window_assertion` (`pass` vacuously).
- **No notebook is created.** Step 02_01_01 closure at the catalog-only layer requires no notebook; emitting one would falsify the lineage.
- **No source code, no validator, no spec, no ROADMAP body, no registry CSV/MD, no Phase 01 artifact, no INVARIANTS.md, no root research_log, no thesis chapter is touched.** This is a closure PR, not a feature PR.

## [3.64.0] — 2026-05-21 (PR #229: feat/sc2egset-02-01-01-section10-audit-persistence)

### Added

- New artifact `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv` — 23-column persistence of the PM-1 §10 verdict audit (26 rows, deterministic, SHA-256 provenance, `audit_executed_at_utc_date` not runtime timestamp, `audit_pr=PR #229` literal).
- New artifact `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.md` — companion summary with verbatim ROADMAP `continue_predicate` three-clause analysis, falsifier roll-call (F-1, F-1a, F-1b, F-2..F-7, PERSIST — all "did not fire"), non-closure disclaimer at §1.
- New `research_log.md` entry in `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (Phase 02 / Step 02_01_01; `closure_status: still_open`; `evidence_persistence_state: section10_verdict_audit_persisted_step_open`).

### Changed

- Notebook `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.{py,ipynb}` — one artifact-write cell added + one banner markdown edit.
- `planning/INDEX.md` — PR #228 archived (merged 2026-05-21 at master `5c7ef380`); new Active plan line for `feat/sc2egset-02-01-01-section10-audit-persistence` (PR #229).
- `planning/current_plan.md` + `planning/current_plan.critique.md` — already committed in PR #229 (commits `fb4bef79` + `119686d0`).

### Notes

- **This PR persists evidence but does NOT close Step `02_01_01`.**
- No materialized-column audit is applicable at the catalog-only registry layer (materialized_column_count=0); this becomes non-vacuous once Step 02_01_02 materializes the first feature column per 02_01_leakage_audit_protocol.md §4 lines 117–121.
- Validator (`validate_registry_section10_verdicts.py`), validator tests, registry CSV/MD, status YAMLs (`STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`), `ROADMAP.md`, `INVARIANTS.md`, locked specs, and root `reports/research_log.md` are UNCHANGED.
- Phase 02 remains `not_started` per `PHASE_STATUS.yaml`. Step `02_01_02` is NOT authorized. Phase 03 is NOT started.

## [3.63.0] — 2026-05-21 (PR #228: feat/sc2egset-02-01-01-section10-verdict-audit)

### Added

- `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py`: PM-1 §10 verdict-audit validator for the SC2EGSet feature-family registry (26 rows). Implements bidirectional §10 verdict equality (`F-1` overall; `F-1a` stricter drift halts; `F-1b` looser drift halts), an independent §10.2 blocking-trigger checklist evaluated WITHOUT reading the registry `status` column (mechanical `row.drop` independence guard), and dataset/spec synonym mapping `blocked_until_additional_validation` ↔ `blocked_until_validation`.
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.{py,ipynb}`: jupytext-paired PM-1 audit notebook scaffold; calls the validator and asserts the gate (`passed=True`, `rows_audited=26`, `materialized_column_count=0`); banner declares "design-time §10 verdict audit, NOT materialization; does NOT close Step 02_01_01".
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_section10_verdicts.py`: tests covering T-INDEP independence, T-F1A/T-F1B drift halts, T-F2 independent §10.2 trigger, T-F3..T-F7 falsifiers, T-VAC vacuous clause-2, T-26ROW real registry pass, T-ROWCNT/T-EMPTY/T-SYN.
- `planning/current_plan.md`: durable approved Category-A plan (20 sections).
- `planning/current_plan.critique.md`: reviewer-adversarial Round-1 (APPROVE-WITH-CONDITIONS, 2026-05-20) + bounded conditions-satisfied check (APPROVE, 2026-05-21).

### Notes

- This PR is a clause-3 increment of Step 02_01_01; clause-2's materialized-column set is EMPTY for the catalog-layer registry (vacuously satisfied per `02_01_leakage_audit_protocol.md:117-121` materialization definition).
- This PR explicitly does **NOT** close Step `02_01_01` and does **NOT** update `STEP_STATUS.yaml`, `PHASE_STATUS.yaml`, `ROADMAP.md`, `research_log.md`, or any `reports/artifacts/**` file.

### Changed

*(none)*

### Fixed

*(none)*

### Removed

*(none)*

## [3.62.0] — 2026-05-19 (PR #227: docs/thesis-appendix-key-canonicalization)

### Added

### Changed

- Appendix-only bib-key canonicalization in two `thesis/reviews_and_others/` files (`thesis/references.bib` and `thesis/chapters/**` are byte-unchanged):
  - `Baek2022` → `BaekKim2022`: key-token-only swap in embedded `@article{…}` block and all inline/ref-list loci (B1 + C3: block differs from references.bib in field order and whitespace; only the key token changed, no field reorder or whitespace re-alignment).
  - `Porcpine2020` → `Porcpine2020EloAoE`: key-token-only swap in embedded `@misc{…}` block and all inline/ref-list loci (C3: reading (b), key-swap only; no note/url/howpublished additions).
  - `Herbrich2007` → `Herbrich2006`: key-token-only swap in embedded `@inproceedings{…}` block and all inline/ref-list loci (key/style only; `year = {2007}` deliberately retained and NOT asserted to be erroneous — NeurIPS 2006 proceedings; 2007 publication is a venue-year/publication-year distinction, consistent with the canonical entry). Herbrich key normalized to the canonical alias Herbrich2006 for cross-document key consistency; the embedded year = {2007} is retained deliberately and is NOT asserted to be erroneous (NeurIPS 2006 proceedings; 2007 publication is a venue-year/publication-year distinction, consistent with the canonical entry).

### Fixed

- `Glickman2025` appendix embedded block 2nd-author given-name typo: `Jones, Alexander C.` → `Jones, Albyn C.` (one token; key/title/journal/year byte-unchanged; references-list `A.C.` abbreviation left unchanged).
- `BT2025Survey` appendix repaired at all three loci (C1; key UNCHANGED; NOT imported into references.bib): embedded block `author` corrected to `Fang, Shuxing and Han, Ruijian and Luo, Yuanhang and Xu, Yiming` and `year` corrected to `{2026}` (vs arXiv:2601.14727); inline prose year `2025` → `2026`; references-list author `Li, Y. et al. (2025)` → `Fang, S., Han, R., Luo, Y., & Xu, Y. (2026)`; title/arXiv id/URL unchanged.

### Removed

## [3.61.0] — 2026-05-19 (PR #226: docs/thesis-bialecki2023-author-correction)

### Added

### Changed

### Fixed

- `Bialecki2023` authors 3–4 corrected post-merge: `Dobrowolski, Piotr` / `Białecki, Paweł` → `Dobrowolski, Paweł` / `Białecki, Piotr`, per concordant Crossref (`10.1038/s41597-023-02510-7`) and arXiv (`2207.03428`). **This supersedes the now-falsified `[3.60.0]` statement** "Bialecki2023 official author list already matches the bib" — the `[3.60.0]` Fixed entry was wrong because the #225 audit and the inheriting reviewer-adversarial pass verified only at surname+initial granularity (`Piotr` and `Paweł` both collapse to "P." under initial-only matching, so the given-name swap was invisible). Five load-bearing false statements in `thesis/pass2_evidence/bibliography_cleanup_report.md` corrected in place (lineage preserved; none deleted).

### Removed

## [3.60.0] — 2026-05-18 (PR #225: docs/thesis-bibliography-canonicalization)

### Added

- Added `thesis/pass2_evidence/bibliography_cleanup_report.md`: a full per-key audit of `thesis/references.bib` + the 5 scoped sources — 14-column master table (119 rows), live Crossref/publisher/official verification with per-field diffs + confidence, four user-named-pair true-state analysis, alias-remap list, manual-decision list, bib↔markdown drift list, schema-change specifics, a "stale prior-audit statements superseded" section, a candidate appendix-follow-up-PR list, and a data-analysis-lineage header. Audit-only; no chapter or appendix edit.

### Changed

- `thesis/references.bib` canonicalized (bib-only; keys preserved except the one deleted duplicate): `Elo1978` `@article`→`@book` (Arco Publishing, New York; canonical two-word title "The Rating of Chess Players, Past and Present"); `Buro2003` `@article`→`@inproceedings` (booktitle IJCAI-18th; existing pages 1534--1535 + url preserved); `Dimitriadis2024` corrected to the published "triptych" version after the record-identity collision was closed at ≥80 (same work; DOI added; *Int. J. Forecasting* 40(3):1101–1122; 4th author Vogel appended; key + title unchanged, no new key, no work substitution).

### Fixed

- Retired the byte-identical, uncited duplicate `@article{Wu2017,…}` (canonical `Wu2017MSC` retained; deletion gated on a re-confirmed zero `[Wu2017]` citation grep — every `[Wu2017]` mention is documentary inside the new audit report only; `@` entry count 107→106). `Bialecki2023` and `Glickman1995` were verified and intentionally left byte-unchanged (Bialecki2023 official author list already matches the bib; Glickman1995 `@unpublished`→`@article` is an editorial manual-decision documented in the report, not auto-applied). bib↔markdown alias/key drift (`Baek2022`/`Porcpine2020`/`Herbrich2007` — key/style only; `Herbrich2007` year 2007 is bibliographically defensible, NOT a year error) and the `Glickman2025` appendix second-author typo are catalogued for a separate, separately-approved follow-up PR; `thesis/chapters/**` and `thesis/reviews_and_others/**` are read-only this PR. reviewer-deep PASS at plan (T01: PASS-WITH-NITS) and final (T03: APPROVE); reviewer-adversarial escalation trigger not met (not invoked).

### Removed

## [3.59.0] — 2026-05-18 (PR #224: docs/thesis-ch1-ch4-supervisor-handoff-package)

### Added

- Added `thesis/pass2_evidence/ch1_ch4_supervisor_handoff_package.md`: the capstone supervisor handoff package for thesis Chapters 1–4, consolidating the merged citation-audit chain (PR #220 audit → #221 M-1 → #222 M-2 → #223 M-3, all on master). Fixed 8-section structure: executive decision (`ready_to_send_with_disclaimer`; supersedes the pre-#221 audit §10 "hold Chapter 2" framing — with M-1 merged all four chapters are sendable together), what to send (the four chapter files), what NOT to send (Chapters 5–7 are BLOCKED/skeleton — no Phase 03+ model results), the M-1/M-2/M-3 closure table, a by-category retained-flag inventory (76 Pass-2 flags + 18 Chapter-4 annotations; 41 ok-to-send-with-flag / 9 manual-full-text-required / 14 future-phase-dependent), a user-approved verbatim Polish supervisor cover note (makes no completed-experiment claim), optional-only traceability attachments, and post-handoff workstreams.
- Documentation-relay only: no new methodology, no chapter prose edit, no `thesis/references.bib` edit, no `[REVIEW]` flag removed, no clean/stripped chapter copy, no PDF/DOCX export. reviewer-deep PASS at plan (T01) and final (T03); reviewer-adversarial escalation trigger not met (not invoked). The PR is held unmerged pending explicit user approval to send.

### Changed

### Fixed

### Removed

## [3.58.0] — 2026-05-18 (PR #223: docs/thesis-aoestats-rowcount-scope-caveat)

### Added

### Changed

### Fixed

- Resolved Chapters 1–4 citation-audit must-fix **M-3 / TQ-05** (finding C-10): clarified the aoestats interface-CSV row-count and `[POP:]`-scope framing in `thesis/chapters/04_data_and_methodology.md` §4.1.4 (line 212 only). Row-count corrected to `137 wierszy łącznie: 1 nagłówek + 136 wierszy danych`.
- On-disk-true correction of the audit's own stale prescription: the audit/brief framing ("aoestats `[POP:]` *not tag-carried* / *0 of 137 tags*") was verified STALE/FALSE post-F6 — `phase06_interface_aoestats.csv` carries `[POP:ranked_ladder]` in all 136 data rows (+30 `[PRE-canonical_slot]`). The corrected sentence states the artifact carries the provisional `[POP:ranked_ladder]` token, operationally superseded in the thesis prose by the disciplined `[POP:1v1_random_map]` / Tier-4 queue-opacity framing (grounded in cleaning rule R02 `leaderboard='random_map'` + input contract `02_00`); no false "0 tags" claim, no Phase 02/06 closure claim, no new theory claim. The stale pre-F6 text in `thesis/pass2_evidence/**` and the WRITING_STATUS §4.1.4 prefix is left as historical audit evidence (out of scope; superseded by an additive WRITING_STATUS line).
- §4.4.6 line 428 (`136 wierszy danych`) byte-unchanged; sc2egset `35/35` + aoe2companion `74/74` clauses + dataset-conditional claim preserved; line-212 `[REVIEW]` flag retained (not closed); no `references.bib` / `REVIEW_QUEUE.md` change. reviewer-deep PASS at plan (T01: PASS-WITH-NITS, grep-battery nits fixed) and final (T03: APPROVE); reviewer-adversarial escalation trigger not met (not invoked). With M-1 (PR #221) and M-2 (PR #222) merged, M-3 closure brings Chapters 1–4 to `ready_to_send_with_disclaimer` for supervisor handoff (subject to retained review flags).

### Removed

## [3.57.0] — 2026-05-18 (PR #222: docs/thesis-ch1-footer-bib-consolidation)

### Added

- Promoted seven Chapter-1 `## References`-footer-only sources into the central `thesis/references.bib` with web-verified metadata (append-only; 100 → 107 `@` entries): `Shin1993` (*The Economic Journal* 103(420):1141–1153), `Forrest2005` (*Int. J. Forecasting* 21(3):551–564, DOI 10.1016/j.ijforecast.2005.03.003), `Levitt2004` (*The Economic Journal* 114(495):223–246, DOI 10.1111/j.1468-0297.2004.00207.x), `Mangat2024` (*Journal of Gambling Studies* 40(2):893–914, DOI 10.1007/s10899-023-10256-5), `Formosa2022` (*Proc. ACM HCI* 6(CHI PLAY) Art. 399, DOI 10.1145/3549490), `Novak2025` (*Frontiers in Sports and Active Living* 7:1636823, DOI 10.3389/fspor.2025.1636823), `Balduzzi2018` (NeurIPS 2018, arXiv:1806.02643).

### Changed

### Fixed

- Resolved Chapters 1–4 citation-audit must-fix **M-2** (findings C-06 / D1-NOTE / §7.1 R-1): the Chapter-1 central-bibliography gap is closed; every `[Key]` cited in Chapter 1 now resolves in `references.bib` (0 unresolved, was 6).
- Corrected the Chapter-1 `## References` footer Mangat2024 metadata in `thesis/chapters/01_introduction.md` (line 85 only): `Journal of Gambling Studies, 40(1), 145-165` → `40(2), 893-914` to match the verified canonical record (Springer/PubMed PMID 37740076, DOI 10.1007/s10899-023-10256-5) and the new bib entry. Chapter-1 prose body unchanged; the line-11 betting-market transferability `[REVIEW]` hedge and the line-85 metadata flag are retained (NOT closed by this metadata consolidation — no new theory claim). `Novak2025` first author corrected to `Pál` (web-verified, Frontiers); `Shin1993`/`Forrest2005` inherited reviewer-deep PR #220 audit §7.1 verified starting points. reviewer-deep PASS at plan (T01) and final (T03); reviewer-adversarial escalation trigger not met (not invoked).

### Removed

## [3.56.0] — 2026-05-18 (PR #221: docs/thesis-esportsbench-version-harmonization)

### Added

### Changed

### Fixed

- Harmonised the EsportsBench version/cutoff parenthetical in Chapter 2 §2.5.5 (`thesis/chapters/02_theoretical_background.md:179`): `(wersja HuggingFace v8.0, cutoff 2025-12-31)` → `(wersja HuggingFace v9.0, cutoff 2026-03-31, dostęp 2026-04-26)`, character-identical to the already-correct Chapter 3 §3.2.4 (`03_related_work.md:77`) and §3.5. Resolves Chapters 1–4 citation-audit must-fix **M-1** / finding C-01 (cross-chapter EsportsBench self-contradiction on the SC2 Aligulac 411 030-match / ~80% Glicko comparator); Chapter 2 supervisor-readiness `not_ready` → `ready_to_send_with_disclaimer`. No new EsportsBench claim, no `thesis/references.bib` change, no Chapter 3 edit; one additive dated provenance line in `thesis/WRITING_STATUS.md` §2.5. reviewer-deep PASS at plan (T01) and final (T03); reviewer-adversarial escalation trigger not met (not invoked).

### Removed

## [3.55.0] — 2026-05-17 (PR #220: docs/thesis-ch1-ch4-citation-literature-audit)

### Added

- Added `thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md`: an audit-only Category F evidence document verifying thesis Chapters 1–4 for citation-key existence/metadata, claim-source support, REVIEW-flag triage, and internal artifact-path support before supervisor handoff.
- Audit verdict `supervisor_handoff_recommendation = send_after_must_fixes`: 3 must-fix (M-1 EsportsBench §2.5.5 version harmonisation; M-2 Chapter-1 footer → `references.bib` consolidation; M-3 TQ-05 aoestats 136-vs-137 row count), 41 ok-to-send-with-flag, 9 manual-full-text-required, 14 future-phase-dependent; per-chapter readiness matrix, Polish supervisor cover note, and four proposed follow-up PRs.
- Audit reuses prior `pass2_evidence/` verification rather than re-deriving it; honors the reviewer-deep T01 chapter-prose freshness carve-out (EsportsBench three-locus partition; TQ-04 §3.2.4 sub-claim recorded `prior_pass2_locus_description_stale`); records a §7.1 residual for the four W-routed Ch1 econ-metadata loci deferred to PR-2 (Shin1993/Forrest2005 metadata independently web-verified at T03).
- This PR is audit-only: no chapter prose, no `references.bib`, no citation add/remove, no flag closure, no dataset artifacts, no notebook execution.
- Gating: reviewer-deep plan review (T01: BLOCKER → fixed `b569f7cb` → PASS-WITH-NITS) and reviewer-deep final audit review (T03: APPROVE WITH CONDITIONS; both conditions applied `3df0fdc8`); reviewer-adversarial escalation trigger not met (not invoked).

### Changed

### Fixed

### Removed

## [3.54.0] — 2026-05-17 (PR #219: thesis/phase02-registry-methodology-section-4-5)

### Added

- Added new Chapter 4 section `§4.5 Rejestr rodzin cech Phase 02 — prowizoryczny artefakt walidowany do V-9` in `thesis/chapters/04_data_and_methodology.md` (TQ-03 from PR #217 audit §12).
- §4.5 explains the SC2EGSet provisional feature-family registry artifacts emitted by PR #216: `02_01_01_feature_family_registry.csv` and `02_01_01_feature_family_registry.md`.
- §4.5 defines the registry as a Step artifact and thesis methodology construct, not a new `docs/TAXONOMY.md` unit.
- §4.5 records that the registry has 26 data rows and 14 columns: 13 required registry columns plus appended `block`.
- §4.5 states that the registry contains feature-family declarations, not feature values; it is not a final feature catalog and not a model-ready feature matrix.
- §4.5 preserves `validated_through = V-9` and `partial_coverage_v9_baseline` verbatim.
- §4.5 explains deferred CROSS-02-03 design-time dimensions D2, D3, D4-in_game, D5-in_game, D6-full, D8, D9, D10-sub-2, D12, D14, and D15, with D15 framed as artifact-lineage readiness / methodology discipline (not N/A).
- §4.5 states that CROSS-02-01-v1.0.1 post-materialization leakage audit remains mandatory for any materialized feature column.
- §4.5 states that Step 02_01_01, Pipeline Section 02_01, and Phase 02 remain open / not complete; no status YAML is flipped by this PR.
- §4.5 states that AoE2 Phase 02 has ROADMAP stubs only and no comparable registry artifact yet; the prose preserves cross-game asymmetry without parity framing.
- `thesis/WRITING_STATUS.md` Chapter 4 row added for §4.5; line 75 (PR #218 GATE-14A6) unchanged.
- `thesis/chapters/REVIEW_QUEUE.md` carries Pending row routing the new §4.5 prose through reviewer-deep + reviewer-adversarial gates.
- Reviewer-deep T03 returned PASS-WITH-FIXES (zero blockers); reviewer-adversarial T04 returned APPROVE (zero blockers, zero required fixes).

### Changed

### Fixed

- Corrected `thesis/chapters/04_data_and_methodology.md` §4.5 post-table wording so D15 is no longer grouped with N/A / AoE2-side deferred dimensions; D15 is now explicitly framed as artifact-lineage readiness confirmed by lineage chain (T03b FIX-1 discharging the T03 reviewer-deep MUST-FIX-BEFORE-T04).
- Corrected `thesis/WRITING_STATUS.md` §4.5 row length figure from false-low `~7.3k znaków polskich` to actual `~11.4k znaków polskich prose-only / ~14.7k total including table and HTML provenance comments` (T03b FIX-3).

### Removed

## [3.53.0] — 2026-05-17 (PR #218: thesis/sc2-tracker-eligibility-section-4-3)

### Added

- New Chapter 4 subsection `§4.3.3 Walidacja semantyczna strumienia tracker_events_raw (Step 01_03_05; GATE-14A6 — narrowed)` in `thesis/chapters/04_data_and_methodology.md` (TQ-02 from PR #217 audit §12).
- Repaired stale §4.3.2 paragraph (TQ-01): Step 01_03_05 is complete as of 2026-05-05; GATE-14A6 outcome is `narrowed`, not `closed`; tracker-derived features remain never pre-game (Invariant I3 / Amendment 2).
- Renumbered AoE2-specific feature subsection from §4.3.3 to §4.3.4; updated §4.1.3 cross-reference to point to both new §4.3.3 and renumbered §4.3.4.
- `thesis/WRITING_STATUS.md` Chapter 4 rows updated to reflect Step 01_03_05 completion; line 75 GATE-14A6 wording repaired to keep §4.4 FINAL status gated by Phase 02 materialization + CROSS-02-01-v1.0.1 (does NOT imply §4.4 is unblocked).
- `thesis/chapters/REVIEW_QUEUE.md` carries Pending row routing the new prose through reviewer-deep + reviewer-adversarial gates.
- Explicit non-claims preserved: no Phase 02 closure, no Step 02_01_01 closure, no final feature catalog, no leakage-free materialized features, no model-ready feature matrix, no model results, no tabular-vs-GNN conclusion.

### Changed

### Fixed

### Removed

## [3.52.2] — 2026-05-17 (PR #217 amendment: thesis/phase01-phase02-writing-readiness-audit)

### Added

- Existing-draft conformance audit appended to `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` as §10 (six-category conformance comparison of existing draft chapter prose against post-PR #216 repository evidence), §11 (Draft correction backlog), and §12 (Writing agent task queue). Category E docs-only extension; no thesis chapter prose modified.

### Changed

### Fixed

### Removed

## [3.52.1] — 2026-05-17 (PR #217: docs/thesis-phase01-phase02-writing-readiness-audit)

### Added

- Phase 01/02 writing readiness audit at `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` (Category E docs-only; cross-dataset; maps existing Phase 01/02 evidence to thesis sections; enumerates forbidden claims and a drafting queue).

### Changed

### Fixed

### Removed

## [3.52.0] — 2026-05-16 (PR #216: phase02/sc2egset-registry-artifact-provisional-v9)

### Added

- SC2EGSet Step 02_01_01 provisional feature-family registry artifact emitted under `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
- Registry CSV: 26 data rows, 14 columns (13 REQUIRED_COLUMNS + `block` metadata column), validated through V-9. Closure of Step 02_01_01 is NOT claimed; STEP_STATUS.yaml is untouched.
- Registry MD companion: provisional disclaimer, per-dimension deferred-coverage table (D2/D3/D4-in_game/D5-in_game/D6-full/D8/D9/D10-sub-2/D12/D14/D15), non-supersession of CROSS-02-01-v1.0.1 post-materialization audit gate, and partial closure framing. Artifact status token: `partial_coverage_v9_baseline`.
- Notebook execution generates both artifacts deterministically; provenance includes repo-relative artifact paths, `executed_at` UTC date, `git_sha` (execution HEAD), `python_version`, and `poetry_version`.
- No feature values, no scaler fit, no model training, no final feature catalog claim in this release segment.
- CROSS-02-01-v1.0.1 post-materialization audit gate remains mandatory for any future feature column the registry triggers materialization of.
- Lineage log/manifest updates (`research_log.md` + `notebook_regeneration_manifest.md` with `partial_coverage_v9_baseline` token) are handled in the following T09 checkpoint of PR #216.

### Changed

### Fixed

### Removed

## [3.51.0] — 2026-05-10 (PR #215: phase02/sc2egset-feature-registry-v9-symmetry)

### Added

- V-9 per-player construction / focal-opponent symmetry validation (spec-D10 sub-clause 1; Invariant I5). Controlled vocabulary `{"symmetric"}` for model-input and sanity-gate rows; carve-out sentinel `"blocked"` under the V-7 conjunction (`prediction_setting == "blocked_or_deferred"` AND `status == "blocked_until_additional_validation"`). Fixture lift on three blocked rows (`mind_control_event_count`, `army_centroid_at_cutoff_snapshot`, `playerstats_cumulative_economy_fields`). D10 sub-clause 2 (aoestats `canonical_slot` p0/p1 projection) recorded N/A for sc2egset and deferred to a future aoestats-side V-N.

## [3.50.0] — 2026-05-09 (PR #214: phase02/sc2egset-feature-registry-v8-source-grain-well-formedness)

### Added

- V-8 source-grain structural well-formedness and provenance-key consistency validation: every row's `source_grain` matches the parenthesised tuple form `(filename[, key1[, key2]])`; tracker-event rows draw extra keys from `{playerId, controlPlayerId, killerPlayerId, owner_via_unitborn_lineage}`; non-tracker rows draw extra keys from `{player_id_worldwide, opponent_player_id_worldwide}` or use the bare `(filename)` form for match-level rows.
- Tuple-style `source_grain` syntax and known provenance-key checks (regex shape + set-membership against the documented vocabularies).
- Separate tracker provenance-key validation from non-tracker source-grain validation (partition on `source_table_or_event_family.startswith("tracker_events_raw")`).
- Blocked rows (`prediction_setting == "blocked_or_deferred"` AND `status == "blocked_until_additional_validation"`) use real provenance-grain tuples, not a `"blocked"` sentinel — sentinels exist on `cold_start_handling`, `model_input_grain`, `target_grain`, `temporal_anchor`, `allowed_cutoff_rule`, `candidate_leakage_modes`, but NOT on `source_grain`.
- Notebook scaffold narrative + executed-output banner updated to `validate_registry_skeleton: ALL PASS (V-1 through V-8)`.
- 8 new V-8 tests (happy path, regex-malformed × 3, unknown tracker key, unknown non-tracker key, non-string source_grain, blocked-row source_grain still validates). Targeted-file test count: 56 (48 pre-existing + 8 new).
- V-8 is NOT CROSS-02-03-v1.0.1 §4.1 D10 (focal/opponent symmetry — Invariant I5); D10 is deferred to a future V-9 against the `per_player_construction` column. Notebook narrative explicitly disambiguates V-8 from spec-D10.
- Non-batching discipline: this PR remains within lineage sequence step 6 ("next validation module") per `.claude/rules/data-analysis-lineage.md`. No report artifacts, no `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` / `research_log.md` / `notebook_regeneration_manifest.md` updates; Step 02_01_01 remains not closed.

### Changed

### Fixed

### Removed

## [3.49.0] — 2026-05-09 (PR #213: phase02/sc2egset-feature-registry-v1-strict-and-v7-cold-start)

### Added

- V-1 strict `feature_family_id` segment alignment: every row must follow `sc2egset.<prediction_setting>.<family>` and the second dot-segment must equal `prediction_setting` verbatim (closes PR #212 reviewer-deep follow-up #1).
- V-7 `cold_start_handling` vocabulary/sentinel validation: active/candidate rows use `G-CS-1..G-CS-6` (CROSS-02-02-v1.0.1 §9.1); `blocked_or_deferred` rows whose `status == "blocked_until_additional_validation"` use the literal `"blocked"` sentinel; numeric tokens forbidden everywhere (Invariant I7).
- New tests for V-1 strict and V-7 (happy and failure paths). Total targeted-file test count: 48 (30 pre-existing + 18 new).
- Notebook scaffold narrative + executed-output banner updated to `ALL PASS (V-1 through V-7)`.
- Non-batching discipline: this PR remains within lineage sequence step 6 ("next validation module") per `.claude/rules/data-analysis-lineage.md`. No report artifacts, no `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` / `research_log.md` / `notebook_regeneration_manifest.md` updates; Step 02_01_01 remains not closed.

### Changed

### Fixed

### Removed

## [3.48.0] — 2026-05-08 (PR #212: phase02/sc2egset-feature-registry-scaffold)

### Added

- SC2EGSet Phase 02 feature-family registry scaffold notebook pair (`sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.{py,ipynb}`): 26-row in-memory registry skeleton (5 `pre_game` + 6 `history_enriched_pre_game` + 4 `in_game_snapshot` eligible_for_phase02_now + 7 `in_game_snapshot` eligible_with_caveat + 1 sanity_gate + 3 blocked), with cell outputs confirming "ALL PASS (V-1 through V-6)".
- Validation module `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py` exposing `validate_registry_skeleton(skeleton, tracker_csv_path) -> None` with assertions V-1 through V-6: schema integrity, tracker eligibility split counts, blocked tracker families remain blocked, `slot_identity_consistency` registry reclassification, zero tracker-derived rows in `pre_game`/`history_enriched_pre_game`, and history strict-`<` with `details_timeUTC` provenance.
- 30 unit tests for the validation module covering V-1 through V-6 plus helper edge cases (`tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`).
- Implements lineage sequence step 2 (scaffold + one validation module) per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical work". No feature values computed, no report artifacts produced, no STEP_STATUS.yaml / PIPELINE_SECTION_STATUS.yaml / PHASE_STATUS.yaml edits, no research_log.md entries, and no notebook_regeneration_manifest.md entries in this PR (all deferred to a subsequent artifacts/log/status/manifest PR after reviewed execution).

### Changed

### Fixed

### Removed

## [3.47.0] — 2026-05-07 (PR #211: phase02/roadmap-stubs-feature-registry)

### Added

- SC2EGSet ROADMAP stub added for Step 02_01_01 feature-family registry.
- aoestats ROADMAP stub added for Step 02_01_01 feature-family registry.
- aoe2companion ROADMAP stub added for Step 02_01_01 feature-family registry.
- ROADMAP-stub only: no notebooks created, no feature generation, no generated artifacts, no raw data edits, no status YAML edits, no research_log edits, no thesis edits.
- CROSS-02-00-v3.0.1, CROSS-02-01-v1.0.1, CROSS-02-02-v1.0.1, CROSS-02-03-v1.0.1 preserved as locked inputs.
- SC2 tracker features constrained by tracker_events_feature_eligibility.csv.
- aoestats Tier 4 semantic opacity preserved.
- aoe2companion mixed-mode ID 6 + ID 18 preserved.

## [3.46.0] — 2026-05-06 (PR #210: docs/phase02-contracts-lock-and-planning-cleanup)

### Changed

- CROSS-02-02-v1.0.1 and CROSS-02-03-v1.0.1 locked (DRAFT → LOCKED) on master after PR #209 merged at `ef3fc627be1793c135711b8bc3715ecda7490cf7` (2026-05-05T21:00:02Z). Both specs flipped via their own §14 / §13 patch lanes (v1 → v1.0.1). `spec_id` literals preserved; no table cell values changed; no audit dimension D1–D15 semantics changed. Validator and `02_04_cross_spec_consistency_report.{json,md}` unchanged.
- Sibling cross-dataset Phase 02 contract triplet now fully LOCKED: `CROSS-02-00-v3.0.1`, `CROSS-02-01-v1.0.1`, `CROSS-02-02-v1.0.1`, `CROSS-02-03-v1.0.1`.
- `planning/current_plan.md` reset to `<!-- No active plan -->` placeholder per `planning/README.md` §Purge protocol.
- `planning/INDEX.md` reset to no-active-plan template (agent routing table preserved).
- `planning/README.md` amended (Option A) — §Contents lifecycle table extended with new row for `current_plan.critique_resolution.md` (Ephemeral; critique-resolution companion); §Purge protocol step 2 made explicit on symmetric deletion alongside `current_plan.critique.md`.

### Removed

- `planning/current_plan.critique.md` (per §Purge protocol step 2; merged-PR-#209-local artifact).
- `planning/current_plan.critique_resolution.md` (per amended §Purge protocol step 2; merged-PR-#209-local artifact).

### Added

- `reports/research_log.md` — new `[CROSS] 2026-05-06 — Post-PR-#209 cleanup and Phase 02 contract lock` entry summarizing T01 (spec lock), T02 (planning purge), and the T00b repository hygiene audit (no `thesis/pass2_evidence/` deletions; no `thesis/reviews_and_others/` deletions; no file moves; 5 follow-up candidates flagged for future PRs).

### Unchanged in this PR

- No dataset ROADMAPs, notebooks, generated dataset artifacts, raw data, `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` files, thesis chapters, `thesis/pass2_evidence/` files, or `thesis/reviews_and_others/` files were modified. `reports/specs/02_00_feature_input_contract.md`, `reports/specs/02_01_leakage_audit_protocol.md`, `reports/specs/02_04_cross_spec_consistency_report.{json,md}`, and `scripts/validate_phase02_readiness_contracts.py` are unchanged.

## [3.45.0] — 2026-05-05 (PR #209: phase02/feature-engineering-readiness)

### Added

- Phase 02 feature-engineering readiness contracts (PR #209, `phase02/feature-engineering-readiness`). Documentation/specification-only readiness work preparing Phase 02 entry across sc2egset, aoestats, and aoe2companion. **No feature generation, notebooks, generated dataset artifacts, dataset ROADMAPs, status YAMLs, or thesis chapters were modified.**
  - `planning/current_plan.md` + `planning/current_plan.critique.md` + `planning/current_plan.critique_resolution.md` + `planning/INDEX.md` — active Phase 02 plan, plan-stage reviewer-deep PASS-WITH-NOTES (0 unresolved BLOCKERs), and T05A planning amendment converting T05 from a read-only transcript pass to a reproducible deterministic Python validator with JSON + Markdown report deliverables.
  - `thesis/pass2_evidence/phase01_closeout_summary.md` (T01) — Phase 01 → Phase 02 entry-condition gate document for all three datasets; not thesis chapter prose; mandatory phrases `GATE-14A6 outcome: narrowed`, `full tracker scope is not closed`, `aoestats Tier 4`, `aoe2companion mixed-mode`, `tracker-derived features are never pre-game` validated.
  - `.claude/rules/data-analysis-lineage.md` (T02) — anti-GIGO workflow rule enforcing ROADMAP / notebook / artifact non-batching; assumption / sanity-check / falsifier review before any artifact generation; tracker-CSV constraint; AoE2 source-label discipline; agent-and-model routing guidance.
  - `reports/specs/02_02_feature_engineering_plan.md` (T03) — CROSS-02-02-v1 (DRAFT / PR-local until reviewed); Phase 02 feature-engineering plan specifying prediction settings (`pre_game`, `history_enriched_pre_game`, `in_game_snapshot`), feature table grains, per-dataset minimal feature families, leakage checks, cold-start gates, AoE2 source-specific labels, SC2 tracker eligibility constraints, and proposed Phase 02 ROADMAP steps (proposals only; does not supersede locked CROSS-02-00-v3.0.1 or CROSS-02-01-v1.0.1).
  - `reports/specs/02_03_temporal_feature_audit_protocol.md` (T04) — CROSS-02-03-v1 (DRAFT / PR-local until reviewed); design-time temporal feature audit protocol with 15 audit dimensions D1–D15, explicit pass conditions and failure routes, and declared (not yet generated) future audit artifact schema.
  - `scripts/validate_phase02_readiness_contracts.py` + `reports/specs/02_04_cross_spec_consistency_report.json` + `reports/specs/02_04_cross_spec_consistency_report.md` (T05A/T05B1/T05B2) — reproducible deterministic cross-spec consistency validator and its generated reports; verdict `PASS` across all 9 checked dimensions; 0 blockers.
  - `reports/research_log.md` — new [CROSS] 2026-05-05 entry recording PR #209 scope, committed deliverables, consistency verdict, and Phase 02 constraints.

### Changed

### Fixed

### Removed

## [3.44.0] — 2026-05-05 (PR #208: phase01/sc2egset-tracker-events-semantic-validation)

### Added

- New SC2EGSet Phase 01 Step 01_03_05 — Tracker Events Semantic Validation. Closes the GATE-14A6 hard gate from `thesis/pass2_evidence/phase02_readiness_hardening.md` §14A.6 + RISK-21 by validating `tracker_events_raw` (62,003,411 rows) semantics across 8 modules (V1 loop / time semantics, V2 player-id mapping, V3 PlayerStats field semantics, V4 event coverage and key-set stability, V5 unit lifecycle ordering, V6 coordinate semantics, V7 leakage boundary, V8 final feature-family eligibility aggregation). Notebook pair `sandbox/sc2/sc2egset/01_exploration/03_profiling/01_03_05_tracker_events_semantic_validation.{py,ipynb}`. Three artifacts under `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/`: `01_03_05_tracker_events_semantic_validation.json` (V1..V8 verdicts + 25 named SQL queries; 167 KB), `01_03_05_tracker_events_semantic_validation.md` (10 KB), `tracker_events_feature_eligibility.csv` (15 rows; per-prediction-setting columns per Amendment 2; 7.6 KB).
- GATE-14A6 outcome: `gate_14a6_decision = narrowed`; `initial_phase02_subset_ready = true`; two distinct predicates exposed (`planned_subset_ready_predicate_satisfied = true` for the 12 planned-yes rows; `full_tracker_scope_closed_predicate_satisfied = false` because 3 candidate families remain blocked). Tracker-derived features remain NEVER pre-game (Amendment 2 / Invariant I3); cutoff rule is `event.loop <= cutoff_loop` (game loops; seconds conversion `cutoff_loop / 22.4` is contextual only, V1 caveat).
- 12 planned Phase 02 tracker feature families ready under each row's `eligibility_scope`: 5 `eligible_for_phase02_now` (UnitBorn / UnitInit / UnitDone / UnitDied / UnitTypeChange basic cutoff counts, PlayerSetup slot consistency, UnitInit+UnitDone construction count) + 7 `eligible_with_caveat` (4 PlayerStats snapshot families, censored time-to-first-expansion, UnitDied victim attribution via UnitBorn lineage, Upgrade occurrence-count). 3 blocked families with explicit reasons: PlayerStats cumulative-economy fields (Q3 strict — s2protocol does not confirm cumulative semantics for `*Lost` / `*Killed` / `*FriendlyFire` / `*Used` keys), UnitOwnerChange dynamic ownership (V4 `sparse_event_family_not_broadly_available`), UnitPositions coordinate features (V6 unpacking + Amendment 5 source-confirmation gap).
- Step 01_03_05 ROADMAP entry, research_log entry (2026-05-05), STEP_STATUS row (`01_03_05`: complete, completed_at "2026-05-05"). PIPELINE_SECTION_STATUS / PHASE_STATUS already at derived values (01_03=complete, Phase 01=complete) so the chain remains consistent.

### Changed

- `thesis/pass2_evidence/notebook_regeneration_manifest.md` — new sc2egset Step 01_03_05 row (confirmed_intact; never flagged_stale) + detail record with full GATE-14A6 outcome + summary counts updated (sc2egset confirmed_intact 32 → 33; Total 85 → 86).
- `thesis/pass2_evidence/phase02_readiness_hardening.md` — appended POST-VALIDATION subsection under §14A.6 recording GATE-14A6 = narrowed, both predicates, what Phase 02 may use (12 of 15 rows), 3 blocked families with reasons, recommended thesis framing for §4.3 / §4.4, future validation route. Original §14A.6 historical/gated text preserved unchanged. "SC2 tracker_events validation status" flipped from NOT executed to Executed (PR #208, 2026-05-05). "Remaining risks" pointer table extended with current-state column.
- `thesis/pass2_evidence/methodology_risk_register.md` — RISK-21 transitioned from OPEN to **MITIGATED-NARROWED** via a new `Status (PR #208 T12, 2026-05-05)` row at the top of the RISK-21 table; risk is NOT marked fully resolved (3 blocked families remain OPEN with explicit reasons + FoodUsed/FoodMade scaling caveat). Updated Evidence source / Mitigation applied / Residual uncertainty / Wording recommendation / Future validation route / Downstream task responsible.

## [3.43.1] — 2026-04-21 (PR #TBD: chore/cross-research-log-refresh)

### Changed

- chore(research_log): refresh top-level `reports/research_log.md` CROSS index + add 5 CROSS entries backfilling this session's cross-dataset work. Index-table last-entry dates updated: sc2egset `2026-04-19 (01_06)` → `2026-04-21 (01_04_05 cross-region fragmentation annotation; WP-7)`; aoestats `2026-04-20 (BACKLOG F1 + W4)` → `2026-04-21 (01_04_07 old_rating CONDITIONAL_PRE_GAME annotation; WP-6)`; aoe2companion unchanged (`2026-04-19 (01_06)`; no aoe2companion work in-session). 5 new CROSS entries prepended (reverse-chronological): WP-7 spec 02_00 v2→v3 amendment + sc2egset 01_04_05 cross-region annotation; WP-6 spec 02_00 v1→v2 amendment + aoestats 01_04_07 CONDITIONAL_PRE_GAME annotation; WP-2 PR #199 cross-dataset leakage-audit protocol spec CROSS-02-01-v1 + Phase 01 audit summary artifact; WP-1 PR #198 cross-dataset Phase 01 → Phase 02 input contract spec CROSS-02-00-v1; PR #197 Phase 01 audit cleanup (7 NOTE-level findings across 3 datasets). Per-dataset research_logs were already up-to-date (top entries: aoestats 01_04_07; sc2egset 01_04_05; aoe2companion 01_06 unchanged).

## [3.43.0] — 2026-04-21 (PR #TBD: feat/sc2egset-cross-region-annotation)

### Added

- New Phase 01 step 01_04_05 — sc2egset cross-region fragmentation annotation. `player_history_all` VIEW amended via DDL to add `is_cross_region_fragmented` BOOLEAN column (row count preserved at 44,817; source `matches_flat mf`). Notebook + MD + JSON artifacts. Flag TRUE for cross-region toon_ids (toons whose LOWER(nickname) appears in 2+ regions — 1,923 toons from 246 nicknames per INVARIANTS.md §2). Applies WP-3 FAIL finding as Phase 01 cleaning annotation per user directive 2026-04-21.

### Changed

- `INVARIANTS.md §2` — "Tolerance and accepted bias" paragraph extended with Phase 01 operationalization sentence citing `is_cross_region_fragmented` column + 01_04_05 artifact + blanket-flag conservatism argument (handle-length breakdown: lt_5=636, 5_to_7=831, ge_8=456 per distinct toon_id).
- `player_history_all.yaml` — `schema_version` descriptive string introduced per canonical_slot + WP-6 precedent: `'38-col (AMENDMENT: is_cross_region_fragmented added 2026-04-21 per 01_04_05)'`. New column entry for `is_cross_region_fragmented` appended.
- `reports/specs/02_00_feature_input_contract.md` — CROSS-02-00-v2 → CROSS-02-00-v3 per §7 change protocol: §2.1 column count corrected post-amendment to 38 (reconciles both WP-7 addition AND pre-existing spec-vs-yaml drift of 36 → 37 → 38); §5.4 adds `is_cross_region_fragmented` BOOLEAN/CONTEXT column row; §7 amendment log entry added.
- `sc2egset/reports/ROADMAP.md` — step 01_04_05 entry added with completed_at, artifacts, key findings, and gate condition.

## [3.42.0] — 2026-04-21 (PR #TBD: feat/aoestats-old-rating-conditional-classification)

### Added

- New Phase 01 step 01_04_07 — aoestats `old_rating` CONDITIONAL_PRE_GAME annotation. `player_history_all` VIEW amended via DDL to add `time_since_prior_match_days` DOUBLE column (row count preserved at 107,626,399). Notebook + MD + JSON artifacts with data-driven threshold selection (N*=7 days chosen empirically from candidates {1, 2, 3, 7}) + 4×4 leaderboard × time-gap stratification (SCOPE = `random_map_only`, chosen empirically: `team_random_map`, `co_random_map`, `co_team_random_map` fail <7d gate). Applies WP-4 FAIL finding as Phase 01 cleaning annotation per user directive 2026-04-21.

### Changed

- `INVARIANTS.md §3` — `old_rating` demoted from PRE-GAME (WP-4 FAIL) to CONDITIONAL_PRE_GAME with empirically-selected N*=7 + SCOPE=random_map_only + explicit NULL-first-match handling (NULL → PRE-GAME, no prior-match cross-session risk). Threshold selection table (N ∈ {1,2,3,7}) + 4×4 leaderboard × time-gap stratification + scope argument all documented in INVARIANTS.md §3.
- `player_history_all.yaml` — `schema_version` field introduced per canonical_slot descriptive-string precedent: `'15-col (AMENDMENT: time_since_prior_match_days added 2026-04-21 per 01_04_07)'`. New column entry for `time_since_prior_match_days`.
- `reports/specs/02_00_feature_input_contract.md` — amended CROSS-02-00-v1 → CROSS-02-00-v2 per §7 change protocol: §2.2 column count 14 → 15; schema_version string introduced; §5.5 adds `time_since_prior_match_days` CONTEXT column row; `old_rating` reclassified PRE_GAME → CONDITIONAL_PRE_GAME; §7 amendment log entry added.
- `aoestats/reports/ROADMAP.md` — step 01_04_07 entry added with current-state `player_history_all` reference as 15-col post-amendment.

## [3.41.2] — 2026-04-21 (PR #TBD: chore/aoestats-43-day-gap-provenance)

### Fixed

- chore(aoestats): Phase 01 audit NOTE 2 closure — "43-day post-patch gap figure no artifact provenance" corrected via follow-up verification 2026-04-21. Provenance located at `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md:29,38` (reports the 43-day + 8-day + 8-day matches/ gaps and the additional 8-day players/ gap) + `sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_01_file_inventory.py` (filename-scanning derivation). Together the `.md` + `.py` pair constitute I9-compliant provenance. `phase01_audit_summary_2026-04-21.md` aoestats NOTE 2 closure-table row updated: OPEN-SCHEDULED → CLOSED with citation. Also cascade-closes the stale aoestats WARNING 2 closure-table row (actually closed by PR #201 / WP-4; audit-summary table row not refreshed at that time — fixed here as a one-line cascade hygiene edit). `INVARIANTS.md §3 Temporal invariants` adds an "Inter-file temporal gaps" bullet at line 75 enumerating all 7 gaps with anchor paths to both the `.md` output and `.py` derivation. Thesis §4.1.2 interpretive claim (post-patch API-schema correlation) retains its existing in-place [REVIEW] flag — Pass-2 Chat workflow territory, not in scope here. **All 5 WPs (WP-1 PR #198, WP-2 PR #199, WP-3 PR #200, WP-4 PR #201, WP-5 this PR) closing the 2026-04-21 Phase 01 audit findings are now complete.**

## [3.41.1] — 2026-04-21 (PR #TBD: fix/aoestats-old-rating-pregame-closure)

### Fixed

- aoestats `old_rating` PRE-GAME classification empirical closure via Step 01_04_06: leaderboard-partitioned consecutive-match temporal consistency test (LAG window `PARTITION BY (profile_id_i64, leaderboard) ORDER BY (started_timestamp, game_id)`; primary scope `random_map`; per-leaderboard + per-time-gap-bucket stratification). CAST discipline per DS-AOESTATS-IDENTITY-04 (`profile_id` DOUBLE → BIGINT). Threshold argument per DS-AOESTATS-02 tolerance (0.95 primary; 50-unit magnitude; 0.90 stratum). Verdict: FAIL (primary agreement=0.9210, max_disagreement=1,118 units; multiple leaderboard and time-gap strata below 0.90). Three follow-up candidates recorded in INVARIANTS.md §3. `INVARIANTS.md §3` "deferred to Phase 02" flag replaced with full empirical finding. Closes aoestats WARNING 2 from `phase01_audit_summary_2026-04-21.md §3`.

## [3.41.0] — 2026-04-21 (PR #TBD: feat/sc2egset-cross-region-history-impact)

### Added

- New Phase 01 step 01_05_10 — sc2egset cross-region history-fragmentation impact; notebook `01_05_10_cross_region_history_impact` (`.py` + `.ipynb`) + MD + JSON artifacts at `reports/artifacts/01_exploration/05_temporal_panel_eda/`. Closes sc2egset WARNING 3. Per-(player, match) rolling-window undercount at window=30 (primary) + sensitivity {5, 10, 100} + MMR-fragmentation Spearman ρ with bootstrap 95% CI (n=1000) + rare-handle subsample control (length ≥ 8). 3-threshold gate: median_rolling30 ≤ 1 AND p95_rolling30 ≤ 5 AND |bootstrap_CI_upper(ρ)| < 0.2. Verdict: FAIL (16.0/29.0/0.2913). Cat D mitigation scope enumerated in artifact §6.

### Changed

- `INVARIANTS.md §2` extended with quantitative Phase 02 rolling-feature impact statement from 01_05_10 measurements: median=16.0, p95=29.0, ρ CI=[-0.009, 0.291], rare-handle subsample comparison, FAIL verdict citation.
- `research_log.md` new 01_05_10 entry (2026-04-21) with full sub-sections per per-dataset-log protocol.

## [3.40.0] — 2026-04-21 (PR #TBD: docs/phase02-leakage-audit-protocol)

### Added

- Phase 01 audit summary artifact at `reports/artifacts/01_exploration/06_decision_gates/phase01_audit_summary_2026-04-21.md` — on-disk traceability for the 2026-04-21 reviewer-adversarial Phase 01 sign-off sweep (3 datasets, verdicts READY_WITH_CAVEATS, zero BLOCKERs; 5 WARNINGs + 9 NOTEs enumerated with closure map). Referenced by WP-2/WP-3/WP-4/WP-5 for I9 traceability.
- Cross-dataset Phase 02 pre-training leakage-audit protocol at `reports/specs/02_01_leakage_audit_protocol.md` (version CROSS-02-01-v1, LOCKED 2026-04-21). Sibling spec to WP-1's `reports/specs/02_00_feature_input_contract.md` (CROSS-02-00-v1). Closes sc2egset WARNING 2 from the 2026-04-21 Phase 01 sign-off audits (now traceable via `phase01_audit_summary_2026-04-21.md §2`). Binds Pipeline Section 02_01 as a hard exit gate; v1 enforcement is convention-based (reviewer-adversarial mandatory review gate); automated tooling enforcement is scheduled as the top-priority §7 future-amendment target. Audits four dimensions: (1) cutoff-time structural check (strict `<` operator, per-dataset anchor column), (2) POST-GAME token absence from feature lineage, (3) normalization fit-scope (training folds only), (4) reference-window assertion (reused from Phase 01). Prescribes JSON + sibling Markdown audit artifact schema. Protocol is reused (not re-gated) by 02_03 and 02_06.

### Changed

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` Phase 02 placeholder — appended mandatory-entry requirement paragraph citing `reports/specs/02_01_leakage_audit_protocol.md` (CROSS-02-01-v1) as hard gate for Pipeline Section 02_01 exit.
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` Phase 02 placeholder — same mandatory-entry requirement paragraph as sc2egset (identical wording, no dataset-specific variance).
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` Phase 02 placeholder — same mandatory-entry requirement paragraph as sc2egset.

## [3.39.0] — 2026-04-21 (PR #TBD: docs/phase02-interface-contract)

### Added

- Cross-dataset Phase 02 feature-engineering input contract at `reports/specs/02_00_feature_input_contract.md` (version CROSS-02-00-v1, LOCKED). Closes sc2egset WARNING 1, aoestats NOTE 3, sc2egset NOTE 4 from the 2026-04-21 Phase 01 sign-off audits. Spec covers: per-dataset canonical input VIEWs + row grain; join keys + I3 temporal anchor (with explicit per-dataset `player_history_all` column enumeration: sc2egset `details_timeUTC` VARCHAR / aoestats `started_timestamp` TIMESTAMPTZ / aoe2companion `started` TIMESTAMP); cross-game categorical encoding protocol (I8 compliance, general rule + instances: faction/race/civ, map, leaderboard); column-level classification summary (§5 tables for 6 VIEW × dataset combinations); Phase 02 Pipeline Section cross-reference (02_01–02_08).

### Changed

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/06_decision_gates/modeling_readiness_sc2egset.md` §5 — added backlink to `reports/specs/02_00_feature_input_contract.md §2` (CROSS-02-00-v1, LOCKED 2026-04-21) as the Phase 02 input binding.
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/06_decision_gates/modeling_readiness_aoestats.md` §5 — added backlink to `reports/specs/02_00_feature_input_contract.md §2` (CROSS-02-00-v1, LOCKED 2026-04-21) as the Phase 02 input binding.
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/06_decision_gates/modeling_readiness_aoe2companion.md` §5 — added backlink to `reports/specs/02_00_feature_input_contract.md §2` (CROSS-02-00-v1, LOCKED 2026-04-21) as the Phase 02 input binding.
- `reports/artifacts/01_exploration/06_decision_gates/cross_dataset_phase01_rollup.md` §5 — added Phase 02 input binding paragraph citing `reports/specs/02_00_feature_input_contract.md` (CROSS-02-00-v1).
- `reports/artifacts/01_exploration/06_decision_gates/cross_dataset_phase01_rollup.md` §1 + §5 — aoestats GO-NARROW refreshed to GO-FULL (per-slot features invariant-safe after canonical_slot amendment landed 2026-04-20 per PR #185 / BACKLOG F1+W4); stale READY_CONDITIONAL verdict updated to READY_WITH_DECLARED_RESIDUALS.

## [3.38.1] — 2026-04-21 (PR #TBD: chore/phase01-audit-cleanup)

### Fixed

- chore(phase01): Pass-01 audit cleanup PR — address all 7 NOTE-level findings surfaced by the reviewer-adversarial Phase 01 sign-off audits (sc2egset, aoestats, aoe2companion) run 2026-04-21. All findings are documentation staleness / artifact provenance gaps; zero methodology errors. Dataset PHASE_STATUS unchanged (all three remain `Phase 01 = complete`).
- **Top-level `reports/research_log.md`** — index table deduplicated (was 5 rows for 3 datasets with stale dates; now 1 row per dataset with accurate last-entry dates: sc2egset 2026-04-19/01_06, aoestats 2026-04-20/BACKLOG F1+W4 canonical_slot, aoe2companion 2026-04-19/01_06). Source: sc2egset audit NOTE 5.
- **`aoe2companion/reports/research_log.md:124`** — LPM ICC values corrected `0.000485 → 0.000491` (5k) and `0.002501 → 0.002505` (10k) to match canonical artifact `01_05_05_icc.json:18,39`. Source: aoe2companion audit NOTE 1 (thesis-citation trap prevention for §4.4.5).
- **`aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_05_icc.json:50-52`** — `sample_files` block paths relativized from machine-local absolute (`/Users/tomaszpionka/...`) to repo-root-relative (`src/rts_predict/...`); added `path_convention` marker citing I10 analogue. Source: aoe2companion audit NOTE 4 (reproducibility gap).
- **`aoe2companion/reports/artifacts/01_exploration/06_decision_gates/risk_register_aoe2companion.md`** — new entry **AC-R06 [LOW] — CROSS_DATASET_ICC_SPEC_ASYMMETRY** documenting the aoec-specific spec v1.0.2 procedural divergences (5k LMM sample-size cap + GLMM omission) and citing the `cross_dataset_phase01_rollup.md §4 item 2` ANOVA-primary harmonization as the formal closure of the I8 AT RISK flag. Severity distribution header updated (LOW: 2 → 3). Source: aoe2companion audit NOTE 2.
- **`aoe2companion/reports/ROADMAP.md:12-19`** + **`aoe2companion/reports/artifacts/01_exploration/06_decision_gates/modeling_readiness_aoe2companion.md:78`** — `cross_dataset_phase01_rollup.md` path citation clarified with explicit `repo-root` qualifier (cross-dataset artifact lives at `<repo>/reports/...`, not at `<dataset>/reports/...`). Source: aoe2companion audit NOTE 3.
- **`aoestats/reports/artifacts/01_exploration/06_decision_gates/data_quality_report_aoestats.md:52`** — `matches_history_minimal` column count corrected `9 → 10 (post-canonical_slot amendment 2026-04-20 per PR #185 / BACKLOG F1+W4; aoestats locally extends the cross-dataset 9-col contract)`. Source: aoestats audit WARNING 1 (consumer-facing schema confusion prevention).
- **`aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_06_temporal_leakage_audit_v1.md` §Q7.4** — new AMENDMENT block documenting the BACKLOG F6 back-tagging fix (2026-04-19: 30 per-slot rows back-tagged `[PRE-canonical_slot]`) and the PR #185 canonical_slot-column landing (2026-04-20: `canonical_slot present: False → True`; `[PRE-canonical_slot]` flag protocol ACTIVE → HISTORICAL per spec §9). Q7.4 FAILED line retained as historical pre-backfill record; overall audit verdict `PASS` unchanged. Source: aoestats audit NOTE 5.
- **Remaining Phase-01-audit follow-ups (NOT in scope of this PR)** — sc2egset WARNINGs 1/2/3 (Phase 02 interface contract; mandated Phase 02 leakage-audit protocol; cross-region fragmentation quantification) and aoestats WARNING 2 + NOTEs 3/4 (old_rating PRE-GAME deferral closure; player_history_all interface docs; 43-day post-patch gap provenance) all deferred to Phase 02 kickoff planning (planner-science next session). NOTE 4 on sc2egset (cross-game faction encoding) also deferred to Phase 02 planning.

## [3.38.0] — 2026-04-21 (PR #TBD: docs/thesis-pass2-status-refresh-and-local-closures)

### Changed

- docs(thesis): Pass-2 Code-track wrap-up — `thesis/reviews_and_others/pass2_status.md` fully refreshed after stale drift since PR #191 (was "3.34.0 / 5 PRs merged / 3 remaining"; now "3.38.0 / 8 audit PRs + 1 handoff + 1 refresh / all scheduled Code PRs complete"). Extended with F-finding closure matrix, remaining-work categorization (Category 1 PDF-read / Category 2 external-search / Category 3 locally-closed), updated flag inventory, 3 new gotchas (#9 stale-handoff risk; #10 HuggingFace README ≠ data; #11 rapid re-verification beats audit-trust), extended version trajectory through 3.38.0, and Claude Chat Pass-2 handoff protocol.
- docs(thesis): F6.6 EsportsBench v7.0/v8.0 reconciliation CLOSED locally — web-verification 2026-04-21 via HuggingFace commit history (dataset `EsportsBench/EsportsBench`, commit `0482ab5` dated 2026-01-25, message "update to 8.0", 20 parquet files updated, size 351.6 MB → 357.6 MB) confirmed v8.0 with cutoff 2025-12-31 IS released, not planned. `02_theoretical_background.md:179` (§2.5.5) and `03_related_work.md:77` (§3.2.4) parentheticals both simplified from "(publicznie dostępna wersja HuggingFace v7.0, cutoff 2025-09-30; planowana wersja v8.0 ma cutoff 2025-12-31)" to "(wersja HuggingFace v8.0, cutoff 2025-12-31)"; both F6.6 [REVIEW] flags removed. §3.5 Luka 3 wording ("v8.0 (2025-12-31)") already aligned. Net prose flag delta: −2 occurrences.
- docs(thesis): F6.8 SBGames Proceedings ISSN CLOSED locally — web-verification 2026-04-21 via ISSN.org portal (https://portal.issn.org/resource/ISSN/2179-2259) confirmed ISSN 2179-2259 = SBGames Proceedings (Confirmed record; Online medium; Brazil; last modified 2024-10-08; independently corroborated by SBGames 2013 paper front matter). `% [REVIEW: F6.8]` BibTeX comment at `references.bib:500` removed; `issn = {2179-2259}` field retained unchanged.
- docs(thesis): `REVIEW_QUEUE.md` and `WRITING_STATUS.md` §2.5 / §3.2 / §3.3 rows gain 2026-04-21 dated closure notes documenting the F6.6 and F6.8 local closures with source URLs and HF commit anchors.
- Post-refresh flag inventory: `thesis/chapters/*.md` carries 65 flag-matching lines (was 66; Δ −1 line, −2 flag occurrences). All remaining flags are Claude Chat Pass-2 items (Category 1 PDF-read: F5.6 Demšar, F6.4 Vinyals, F6.7 Yang, F6.2 Elbert, Minami verification; Category 2 external-search: F6.1 four seed authors, F6.5 patch-notes citation, F6.9 Xie Medium post).

## [3.37.0] — 2026-04-20 (PR #TBD: docs/thesis-pass2-tg6b-bib-hygiene-minor-prose)

### Changed

- docs(thesis): Pass-2 PR-6b — F6.4 §2.2.4 line 43 Vinyals2017 added as secondary peer-reviewed anchor alongside Liquipedia_GameSpeed at the 22,4 game loops/sec locus (Mode A reversal of original substitution — Liquipedia retained as PRIMARY verified grey-literature anchor); existing chapter-02 line-49 [REVIEW] flag preserved UNCHANGED (net 0 at that locus). F6.5 §2.2.4 — Patch 2.0.8 release date deferred to Pass-2 per Mode A option (c); line 45 kept unchanged (no inline date parenthetical); new standalone [REVIEW: F6.5 Pass-2 audit] flag appended to the §2.2.4 paragraph noting [BlizzardS2Protocol] README covers protocol version 2.0.8 but not patch release date. F6.6 §2.5.5 + §3.2.4 EsportsBench versioning — both loci add parenthetical "(publicznie dostępna wersja HuggingFace v7.0, cutoff 2025-09-30; planowana v8.0 cutoff 2025-12-31)" with two new [REVIEW: F6.6 Pass-2] flags reconciling v8.0/2025-12-31 (§3.5 Luka 3 current) vs v7.0/2025-09-30 (HuggingFace verified state per WebFetch 2026-04-20). F6.7 §3.3.1 Yang 2017 — qualitative "9:1 split is random-not-temporal" clarification appended with one new [REVIEW: F6.7 Pass-2 audit] flag; numeric reclassification (58,69% = Kinkade reimplementation vs own LR 60,07%) deferred to REVIEW_QUEUE §3.3 per F6.1 precedent (WebSearch 2026-04-20 did NOT surface 60,07%). F6.8 Silva2018LoL bib — pages = {639--642} + issn = {2179-2259} fields added at references.bib lines 500–506; % [REVIEW: F6.8] comment placed OUTSIDE the @inproceedings{} block per Mode A NOTE (parser-safe placement). F6.9 §3.4.4 Xie2020MediumAoE R²-vs-accuracy hypothesis flag — one sentence appended with [REVIEW: F6.9 Pass-2 verify] flag. F6.10 bib: Porcpine2020EloAoE at references.bib line 95–102 — url fixed (dead `/aoe2/elo.html` HTTP 404 → live `/aoe2_comparisons/elo/`), howpublished extended with GitHub Pages root + code-repo URL, note extended to document r=0,96 bin-aggregation inflation. F6.10-prose §3.4.4 line 163 — one sentence clarifying r=0,96 is on bin-aggregated win-percentages per rating-difference bin, not raw binary signal (no [REVIEW] flag — derivable from Porcpine analysis itself).
- F6.11 skipped (already resolved in TG4/PR #190); F6.12 deferred (blockquote convention; tooling regression risk).
- Net new [REVIEW] flags in prose: 5 (F6.5 §2.2.4 defer patch-notes date; F6.6 ×2 §2.5.5+§3.2.4 EsportsBench versioning; F6.7 §3.3.1 Yang random-not-temporal; F6.9 §3.4.4 Xie R²-vs-accuracy); F6.4 preserves existing line-49 flag (net 0 at that locus); F6.10 prose carries no [REVIEW] flag. REVIEW_QUEUE §3.3 row gains one additional deferral entry (F6.7 60,07%/Kinkade reclassification). Zero new bib entries; two existing entries edited (Silva2018LoL adds pages+ISSN with %-comment outside block; Porcpine2020EloAoE url/howpublished/note updated).

## [3.36.0] — 2026-04-20 (PR #TBD: docs/thesis-pass2-tg6a-luka-prophylactic-strengthening)

### Changed

- docs(thesis): Pass-2 PR-6a — F6.1 §3.5 Luka 1 strengthened with verified Minami2024 citation (single witness per reference-class filter) + [NEEDS CITATION] flag for 4 unverified seed authors (Brookhouse & Buckley; Caldeira; Alhumaid & Tur; Ferraz); F6.2 §3.5 Luka 2 Elbert2025EC/SHAP conditional disambiguation with §4.4 forward-reference; F6.3 §3.5 Luka 4 short restatement (GarciaMendez2025 referenced as terminology example only); one new bib entry (Minami2024).

## [3.35.0] — 2026-04-20 (PR #TBD: docs/thesis-pass2-tg5b-circular-spec-thorrez-proxy)

### Changed

- docs(thesis): Pass-2 PR-5b — F5.4 §4.1.3 reference-window defence anchored to [Nakagawa2017, Gelman2007, Ukoumunne2003, WuCrespiWong2012] with orthogonal-axes reframe (bias vs precision) and patch-66692-uniqueness external anchor; F4.5 §2.2.3 Thorrez2024 Glicko-2 80.13% academic-proxy insertion with preserved calibration-vs-accuracy distinction; REVIEW_QUEUE + WRITING_STATUS entries; no bib changes.

## [3.34.0] — 2026-04-20 (PR #TBD: docs/thesis-pass2-tg5a-internal-consistency-chore)

### Added

- `thesis/reviews_and_others/pass2_dispatch.md` — Pass-2 dispatch audit (446 lines) saved for durable recovery. Recovered from compacted transcript `36812a12` line 6 (34,795 chars). The audit spawned TG1–TG6; TG1–TG4 previously merged but the audit itself lived only in external Claude Chat + transcript. Saving to repo so remaining TG5 + TG6 scope survives future compactions.
- `planning/current_plan.md` — Category F TG5-PR-5a plan (3 /critic iterations with combined 27 revisions applied + Mode A pre-execution audit with 2 BLOCKER + 4 WARN findings all resolved via structural plan revision + Mode C draft review APPROVE).
- `planning/current_plan.critique.md` — Mode A findings (2 BLOCKERs on unverified Demšar §3.1.3 attribution + 4 WARNs + 4 NOTEs); BLOCKERs resolved by restructuring F5.6 to flag-planting only (no citation swap).

### Changed

- Pass-2 TG5-PR-5a internal-consistency chore: 5 audit findings addressed — F5.1 (§1.1 flag-count drift), F5.2 (THESIS_STRUCTURE Ch1 footer), F5.3 (Aligulac 80% calibration-not-accuracy reframing), F5.5 (Elbert2025EC §3.4 placement decision), F5.6 (Demšar §3.1.3 location uncertainty — flag-planting only, no citation swap).
- **F5.1:** `thesis/chapters/REVIEW_QUEUE.md` §1.1 `Flag count` cell corrected from `0` to `2 physical [REVIEW] tags covering 3 audit-named concerns`; `thesis/WRITING_STATUS.md` §1.1 Notes cell refreshed with corresponding enumeration (GarciaMendez2025 at line 11; Shin1993/Forrest2005/Mangat2024 bundle at line 13; bibliography-footer flags at lines 81, 83).
- **F5.2:** `thesis/THESIS_STRUCTURE.md:67` Chapter 1 "Fed by" footer softened to acknowledge §4.1.3–§4.1.4 cross-corpus framing as motivational feed (prior wording under-claimed "No roadmap phase directly"; over-claim of "Tabela 4.4b, §4.1.3" anchor avoided per Mode A W1).
- **F5.3:** `thesis/chapters/02_theoretical_background.md:39` (§2.2.3) prose rewritten to distinguish calibration (Aligulac FAQ ~80%) from classification accuracy; existing §2.5.5 line 183 [REVIEW] flag reworded to align. Thorrez2024 comparator insertion at §2.2.3 **intentionally deferred to PR-5b** (chore-scope discipline); PR-5b scope expanded to include F4.5 Aligulac reframing alongside F5.4.
- **F5.5:** `thesis/chapters/03_related_work.md` §3.4.3 — single-sentence placement-decision inserted grounding Elbert2025EC in AoE2 game identity (not RTS genre); §3.4 organizing principle documented as game-based, not team-size-based.
- **F5.6 (flag-planting only):** `thesis/chapters/04_data_and_methodology.md` lines 213 (§4.1.4), 375 + 377 (§4.4.4) and `thesis/chapters/02_theoretical_background.md` line 211 (§2.6.3) each receive a canonical `[REVIEW: F5.6 Pass-2 audit H3 claims N≥10 threshold is in Demšar 2006 §3.1.3, not §3.2; manual verification against readable PDF required — Pass 2 closes this flag.]` annotation. **§3.2 citations retained at all four loci.** The §3.2 → §3.1.3 swap deferred to a post-Pass-2 PR pending readable Demšar 2006 PDF (Mode A B1/B2 resolution — swap on unverified audit assertion would replace one unverified citation with another). Line 373 of `04_data_and_methodology.md` already reads `§3.1.3` from TG1 and remained untouched.
- **T06 metadata cascade:** `WRITING_STATUS.md` and `REVIEW_QUEUE.md` section-row annotations refreshed for §1.1, §2.2, §2.5, §2.6, §3.4, §4.1.4, §4.4.4.

### Fixed

- F6.11 (Elbert `Stein, Nora` → `Nikolai`; `Schenk, Amadeus` → `Alicia`) confirmed already-landed in TG4 (PR #190); dropped from future PR-6b scope.
- Pre-existing internal drift between WRITING_STATUS §1.1 "0 flags" cell and actual 3 in-prose concerns (audit H1 closure).

## [3.33.0] — 2026-04-20 (PR #190: docs/thesis-pass2-tg4-bibliography-findings)

### Changed

- Pass-2 TG4 bibliography audit: 11 originally-named references verified + 1 latent bug surfaced during /critic (Lin Shih "Yi-Wei" → "Yu-Wei" typo). 12 edits total to `thesis/references.bib`.
- **Author-name corrections:** Thorrez2024 (Lucas → Clayton); Hodge2021 (fabricated Sherkat coauthors → canonical 6-author IEEE Xplore list); BaekKim2022 (Jihun/Jinyoung → Insung/Seoung Bum); Aligulac (Kim Espen → Fonn Eivind with community contributors); Elbert2025EC (Schenk Amadeus → Alicia; Stein Nora → Nikolai); Lin2024NCT (Shih Yi-Wei → Yu-Wei).
- **Metadata completeness:** Glickman2001 DOI added; Lin2024NCT arXiv URL added; Hodge2021 volume/issue/pages added; Thorrez2024 HuggingFace URL + title-variance note added.
- **Duplicate elimination:** Tarassoli2024 phantom entry deleted (same paper as Khan2024SCPhi2, arXiv:2409.18989); Khan2024SCPhi2 pages 2444–2462 → 2338–2352 per MDPI canonical.
- **Verified correct (no edit):** CetinTas2023; Bunker2024 (DOI correct, vol/issue/pages deferred to Pass 2 per SAGE online-first ambiguity).
- **Chapter prose propagation:** `01_introduction.md` — `[Baek2022]` bibkey harmonized to `[BaekKim2022]` at three sites (lines 13, 25, 69); References block initials "Baek, J., & Kim, S." → "Baek, I., & Kim, S. B." `03_related_work.md:69` — resolved Tarassoli2024 `[REVIEW:]` flag removed. `THESIS_STRUCTURE.md:148` — "Tarassoli et al. (2024)" → "Khan & Sukthankar (2024)".
- WRITING_STATUS.md: §1.1, §1.3, §2.5, §3.2 rows gain PR-TG4 notes.
- REVIEW_QUEUE.md: Tarassoli2024 reconciliation resolved; new Pass 2 chore documents triple-divergent Thorrez first-name across repo (references.bib "Clayton" canonical; scratchpad `reviews_and_others/related_work_rating_systems.md:393` carries "Calvin"; previously "Lucas" in pre-TG4 bib).

### Added

- `GarciaMendez2025` bibkey inserted into global `thesis/references.bib` (previously cited by bibkey at `01_introduction.md:11` but absent from global bib, breaking BibTeX resolution per `.claude/rules/thesis-writing.md` cross-chapter bibkey convention).
- `planning/current_plan.md` — Category F TG4 plan (1 /critic iteration with 13 revisions + Mode A pre-execution audit with 6 additional revisions + Mode C draft review PASS).
- `planning/current_plan.critique.md` — Mode A findings (BLOCKER B1 on Baek occurrence count undercount + 3 WARNINGs + 3 NOTEs); all resolved before execution.

### Removed

- `Tarassoli2024` bibkey deleted from `thesis/references.bib` (phantom entry — fabricated attribution of the SC-Phi2 paper; Khan & Sukthankar 2024 is the canonical author pair).

## [3.32.0] — 2026-04-20 (PR #189: docs/thesis-pass2-tg3-luka3-narrowing)

### Changed

- Pass-2 TG3 Luka 3 narrowing against Thorrez 2024 EsportsBench across
  thesis §3.5, §3.2.4, §1.3, §2.5.5. Three-part edit.
- **§3.5 Luka 3 rewrite** (`03_related_work.md:187`) — hedge-only
  novelty claim ("pierwsza znana nam") replaced with argued four-
  constraint conjunction: (a) ML-classifier family vs paired-comparison
  rating systems; (b) paired-game cross-comparison with AoE2-absence
  anchor verified against EsportsBench v8.0 (2025-12-31); (c)
  calibration-diagnostics absence-from-README (HuggingFace + GitHub);
  (d) 1v1 scope. Lin2024NCT/Elbert2025EC/CetinTas2023 disqualifications
  retained.
- **§3.2.4 EsportsBench characterization** (`03_related_work.md:77`) —
  supplementary sentence identifying EsportsBench as paired-comparison
  rating-systems benchmark with per-game fit; SC1+SC2+WC3 named as RTS
  representation, AoE2 absence explicit.
- **§1.3 RQ1 hypothesis** (`01_introduction.md:31`) — surgical deletion
  of miscited `[Thorrez2024]` from GBDT-dominance claim. Hodge2021 +
  Tang2025 retained as correctly-supporting citations. Narrowed-
  induction consequence (Dota-2-only base + margin caveat) documented
  in WRITING_STATUS §1.3 note; broader cross-esport GBDT-dominance
  citation extension deferred to Pass 2.
- **§2.5.5 hybrid-strategy citations** (`02_theoretical_background.md`)
  — line 181: `[Hodge2021, Thorrez2024]` → `[Hodge2021]` (EsportsBench
  does not benchmark hybrid rating+GBDT pipelines). Line 177: claim
  tightened from "rankingi... używane... jako cechy wejściowe w ML
  pipelines" to "benchmarkuje paired-comparison rating systems (m.in.
  Elo, Glicko, Glicko-2, TrueSkill) na danych esportowych"; Thorrez2024
  citation retained with corrected scope.
- ISO YYYY-MM-DD dates throughout; em-dash "—" for ranges. Unified
  rating-family enumeration "m.in. Elo, Glicko, Glicko-2, TrueSkill"
  across §3.2.4, §2.5.5:177, §3.5.
- WRITING_STATUS.md: §1.3, §2.5, §3.2, §3.5 rows gain dated PR-TG3
  notes; §1.3 note records narrowed-induction mitigation.
- REVIEW_QUEUE.md: §1.3 row (line 22) question (2) resolved in-place;
  §3.5 row (line 40) RQ3 novelty hedge resolved.

### Added

- `planning/current_plan.md` — Category F TG3 plan (1 /critic iteration
  with 10 revisions + Mode A pre-execution audit with 3 revisions +
  Mode C draft review with 2 prose fixes applied).
- `planning/current_plan.critique.md` — Mode A findings (BLOCKER B-1
  on EsportsBench advertised-metric overclaim + MAJOR W-1 narrowed-
  induction mitigation + MAJOR W-2 asymmetric rating-family
  enumeration); all resolved before execution.
- Reduced-scope `[REVIEW:]` flag at §3.5:187 covering two residual
  uncertainties: EsportsBench v9.0+ future-release monitoring
  (post-2025-12-31 AoE2 addition or ML-classifier benchmark
  introduction) AND preprint Table 2 calibration-metrics manual
  verification.

## [3.31.0] — 2026-04-20 (PR #188: docs/thesis-pass2-tg2-factual-contradictions)

### Changed

- Pass-2 TG2 factual-contradictions correction across thesis §1.1, §1.2,
  §1.3, §1.4, §2.2.2, §2.3.2, §2.5.4, §3.1.2, §3.2.2 (nine sites across
  three chapters) + `references.bib`.
- SC2EGSet date range "2016–2022" → "2016–2024" at §2.2.2:33 and
  §3.2.2:55 (matching §4.1.1.1, Tabela 4.4a, and the 01_02_04 univariate
  census Section F endpoints 2016-01-07 — 2024-12-01). §2.2.2 was
  pre-flagged as MIGRATION CANDIDATE in `sec_4_1_crosswalk.md:14`;
  §3.2.2 caught via independent grep.
- `references.bib:791` AoE2DE note field: "The Mountain Royals (2024)"
  → "The Mountain Royals (2023)" (single-token edit; verified release
  2023-10-31 via Wikipedia, Steam, Neowin, ageofempires.com).
- AoE2 civilization count "45" → "50" across nine sites, anchored to
  the aoestats empirical observation in window 2022-08-28 — 2026-02-07
  (`aoestats/INVARIANTS.md:10`). Cascading arithmetic: 990 → 1 225
  unordered non-mirror; 1035 → 1 275 ordered at §2.3.2:69.
- §2.3.2:67 `[REVIEW:]` flag lifecycle: the original civ-count question
  is resolved; a reduced-scope flag is planted covering DLC-chronology
  completeness (Three Kingdoms 2025-05-06, Chronicles: Alexander the
  Great 2025-10-14, Last Chieftains 2026-02-17). Full-roster cardinality
  audit deferred to a dedicated Pass-2 edit with fresh source
  verification.
- Tabela 4.4a forward-references added at §1.4:45, §2.2.2:33, §2.3.2:67,
  §3.2.2:55 for window/date-range anchoring consistency.
- ISO YYYY-MM-DD date format used throughout; em-dash "—" for window
  ranges (matching Tabela 4.4a character convention).
- WRITING_STATUS.md: §1.1, §1.2, §1.4, §2.2, §2.3, §3.2 rows gain dated
  PR-TG2 notes.
- REVIEW_QUEUE.md: §1.4 row in-place closure of question (2) civ count;
  question (1) mgz parser remains Pending. §2.2 + §2.3 rows gain
  PR-TG2 revision notes.

### Added

- `planning/current_plan.md` — Category F TG2 plan after 3 iterations
  of /critic (~27 revisions applied) and a reviewer-adversarial Mode A
  pre-execution audit (A1 BLOCKER + A2/A3 MAJORs + A4 MINOR, all
  resolved).
- `planning/current_plan.critique.md` — Mode A findings that caught the
  factually-wrong "53 total, 3 Chronicles excluded" parenthetical
  (Chronicles shipped in two parts for 6 civs; Three Kingdoms and
  Last Chieftains also omitted from the DLC chronology). BLOCKER
  resolved by dropping the parenthetical and deferring full-roster
  audit.
- Reduced-scope `[REVIEW:]` flag at §2.3.2:67 for DLC-chronology
  completeness (Three Kingdoms 2025-05-06, Chronicles: Alexander the
  Great 2025-10-14, Last Chieftains 2026-02-17).

## [3.30.0] — 2026-04-20 (PR #187: docs/thesis-pass2-tg1-methodological-drift)

### Changed

- Pass-2 TG1 methodological drift correction across thesis §1.2, §2.6,
  §4.4.4. Un-commits the Dimitriadis triptych and the within-game
  statistical comparison protocol (Friedman + Wilcoxon-Holm + Bayesian
  signed-rank). Preserves Option B end-state: ECE + reliability diagrams
  + Murphy decomposition designated as the operational aggregate-level
  diagnostic; triptych framed as one candidate extension. §4.4.4 now
  enumerates three genuinely distinct inferential families (rank-based
  frequentist with gating variants, Bayesian, resampling) rather than
  committing to a single protocol.
- ROPE width and Holm α both deferred to §4.4.2 methodology finalization
  (invariant #7 full compliance restored — previously only ROPE was
  flagged).
- §4.1.4 line 213 carries explicit within-game/cross-game scoping
  qualifier; Demšar §3.1.3 (N ≥ 5 blocks, within-game) and §3.2 (N ≥ 10
  datasets, cross-game) thresholds distinguished rather than conflated.
- WRITING_STATUS.md: §2.6 and §4.4.4 rows transitioned DRAFTED → REVISED;
  §1.2 and §4.1.4 rows annotated with PR-TG1 notes.
- REVIEW_QUEUE.md: new §1.2 ¶1 Pending row; PR-TG1 revision notes
  appended to §2.6 and §4.4.4 rows; §4.4.4 flag count 2 → 3.

### Added

- planning/current_plan.md — Category F plan produced through 3
  iterations of /critic (22+ revisions) and a reviewer-adversarial
  Mode A pre-execution audit (A1–A6 findings folded in).
- planning/current_plan.critique.md — Mode A findings documenting
  the pre-execution methodology audit that produced the A1–A6
  revisions.
- 2 new [REVIEW:] flags: §2.6.3 Demšar §3.1.3 citation section
  verification (WebFetch could not confirm section anchor from PDF);
  §4.4.4 Pass-2 TG1 candidate-framing acceptability for examiner
  review.

## [3.29.1] — 2026-04-20 (PR #186: chore/purge-planning-pr-185)

### Removed

- `planning/current_plan.md` reset to `<!-- No active plan -->` and
  `planning/current_plan.critique.md` deleted. Post-merge purge for
  the aoestats `canonical_slot` (BACKLOG F1 + W4) workstream
  completed in PR #185.

## [3.29.0] — 2026-04-20 (PR #185: feat/aoestats-canonical-slot)

### Added

- aoestats `canonical_slot VARCHAR` column in `matches_history_minimal` (hash-on-match_id; skill-orthogonal by construction). Resolves BACKLOG F1. Artifact: `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_03b_canonical_slot_amendment.{json,md}`.

### Changed

- INVARIANTS.md §5 I5 row: PARTIAL → HOLDS (W4 operational content).
- `reports/specs/01_05_preregistration.md` bumped v1.0.5 → v1.1.0 (§14 amendment log; aoestats `matches_history_minimal` 9 → 10 columns; cross-dataset UNION ALL contract projects 9 shared columns only).
- `modeling_readiness_aoestats.md` verdict: READY_CONDITIONAL → READY_WITH_DECLARED_RESIDUALS. Phase 02 scope: GO-NARROW → GO-FULL.
- `risk_register_aoestats.csv` AO-R01 mitigation_status: OPEN → RESOLVED.

### Fixed

- `[PRE-canonical_slot]` flag protocol transitioned ACTIVE → HISTORICAL (operational closure of §4.4.6 flag; substantive thesis rewrite deferred to Pass-2 per REVIEW_QUEUE).

### Removed

- `planning/BACKLOG.md` F1 entry (resolved).

## [3.28.1] — 2026-04-19 (PR #184: chore/purge-planning-pr-183)

### Removed

- `planning/current_plan.md` reset to `<!-- No active plan -->` and
  `planning/current_plan.critique.md` deleted. Post-merge purge for
  the Phase 01 Decision Gates (01_06) workstream completed in PR #183.

### Changed

- CHANGELOG `[3.28.0]` header: `PR #TBD` → `PR #183` backfill.

## [3.28.0] — 2026-04-19 (PR #183: feat/phase01-decision-gates-01-06)

### Added

- Pipeline Section 01_06 (Decision Gates) across all three datasets: sc2egset, aoestats, aoe2companion.
  Four deliverables per dataset (data dictionary, data quality report, risk register, modeling readiness
  decision) plus cross-dataset rollup at `reports/artifacts/01_exploration/06_decision_gates/cross_dataset_phase01_rollup.md`.
- 12 sandbox `06_decision_gates/` notebooks (4 per dataset × 3) + 1 retroactive `01_05_09_gate_memo.py` for aoe2companion; 18 per-dataset artifact files under `06_decision_gates/` (6 per dataset × 3: `data_dictionary.{csv,md}`, `data_quality_report.md`, `risk_register.{csv,md}`, `modeling_readiness.md`) + 1 cross-dataset rollup + 1 retroactive aoe2companion `01_05_09_gate_memo.md` + 1 sc2egset git-mv rename (`decision_gate_sc2egset.md` → `01_05_09_gate_memo.md` for naming parity with aoestats).
- Retroactive `01_05_09_gate_memo.md` for aoe2companion (fills symmetry gap with sc2egset and aoestats).
- Spec v1.0 locked at `reports/specs/01_06_readiness_criteria.md` (four-tier verdict taxonomy,
  six role-assignment dimensions D1–D6).

### Changed

- Phase 01 status → COMPLETE for sc2egset, aoestats, aoe2companion (PHASE_STATUS.yaml × 3).
- PIPELINE_SECTION_STATUS 01_06 → complete; 01_05 aoe2companion → complete (T07 checkpoint 1 restore).
- STEP_STATUS.yaml: 01_06_01..04 + 01_05_09 flipped to complete across all three datasets.
- ROADMAP.md Role blocks updated from TBD to dimension-specific assignments (D1–D6) for sc2egset,
  aoestats, and aoe2companion.
- `planning/BACKLOG.md` F1 entry updated with F1+W4 coupling note (01_06 flip-predicate registration).
- `thesis/WRITING_STATUS.md` §4.1 / §4.1.3 / §4.1.4 rows enriched with 01_06 gate-closure notes;
  header updated.
- Three per-dataset research logs + project-level CROSS entry added.

### Removed

- `.github/tmp/01_05/` directory and its 6 orphan plan files (T13 cleanup).

## [3.27.1] — 2026-04-19 (PR #TBD: chore/purge-planning-pr-181)

### Removed

- `planning/current_plan.md` reset to `<!-- No active plan -->` and
  `planning/current_plan.critique.md` deleted. Post-merge purge for
  the F3 thesis-§4.2.2 / aoe2companion-rate-reconcile workstream
  completed in PR #181.

### Changed

- CHANGELOG `[3.27.0]` header: `PR #TBD` → `PR #181` backfill.

## [3.27.0] — 2026-04-19 (PR #181: docs/thesis-4.2.2-identity-meta-rule)

### Changed

- **Thesis §4.2.2 "Rozpoznanie tożsamości gracza" revised to reflect
  I2 extended 5-branch procedure.** Closes BACKLOG F3. Paragraphs 2–4
  rewritten as 5 paragraphs implementing the operational procedure from
  `.claude/scientific-invariants.md:31–127`: (a) Formal operationalisation
  bridging classical Fellegi–Sunter record-linkage [FellegiSunter1969,
  Christen2012DataMatching] → *a priori* schema selection via 5-branch
  procedure; (b) sc2egset Branch (iii) `player_id_worldwide` worked
  example (`migration_rate ≈ 12%` + `collision_rate = 30.6%` cited from
  sc2egset `INVARIANTS.md:50–51`; "deferred to a future manual-curation
  upgrade path" framing); (c) aoe2companion Branch (i) `profileId` worked
  example (`migration_rate = 2.57%` + `collision_rate = 3.55%` post
  rm_1v1-scope reconciliation, 2026-04-19); (d) aoestats Branch (v)
  structurally-forced declaration + cross-dataset namespace bridge to
  aoec (VERDICT A, 0.9960 agreement); (e) Branch (ii) framework-
  completeness note (handle-only platforms like chess.com named as
  indicative class, not worked example). Paragraph 1 preserved;
  paragraph 5 retained + cross-ref sentence appended; Forward reference
  structural role preserved with revised flag wording.
- **Tabela 4.5 row `Plan Phase 02 (I2)` renamed to `Klucz kanoniczny
  (I2 §2)`** with per-corpus declared-branch values from each dataset's
  `INVARIANTS.md §2`: sc2egset `player_id_worldwide` (branch (iii);
  ~12% cross-region accepted bias); aoestats `profile_id` (branch (v),
  structurally-forced — no visible handle); aoe2companion `profileId`
  (branch (i); rename-stable).
- `thesis/WRITING_STATUS.md` §4.2.2 status flipped `DRAFTED` → `REVISED`.
- `thesis/chapters/REVIEW_QUEUE.md` §4.2.2 Notes cell extended with F3
  revision summary; post-rewrite line anchors recorded for all 4
  REVIEW flags (lines 235 / 243 / 263 / 265 post-rewrite).

### Fixed

- **aoe2companion identity-rate artifacts reconciled to rm_1v1 scope.**
  `INVARIANTS.md §2` SQL snippets (rename / collision rates) were missing
  the rm_1v1 scope filter (`internalLeaderboardId IN (6, 18)
  AND profileId != -1 AND name IS NOT NULL`) that the primary artifact
  `01_04_04_identity_resolution.md` applies, producing a three-way
  artifact disagreement on the collision rate (INVARIANTS.md 3.7% vs
  primary artifact 3.55% vs unfiltered DuckDB re-run 3.49%). Both SQL
  snippets now carry the scope filter; published rates updated to
  `migration_rate = 2.57%` and `collision_rate = 3.55%` (23,221
  collision names / 654,841 total) consistent with the 01_04_04
  primary artifact snapshot. Scope-note paragraph added. Invariant-
  compliance table line 98 updated. New 2026-04-19 session entry in
  aoe2companion `research_log.md` documents root cause, verification
  against current DuckDB, and reconciliation policy (historical
  research_log entries preserved; primary artifact's executive-summary
  prose kept intact with inline addendum note explaining the
  reconciliation). Precursor fix enabling `[3.27.0]` thesis §4.2.2
  citation of the aoe2companion `collision_rate` figure.

### Removed

- BACKLOG F3 entry (executed in this PR).

## [3.26.3] — 2026-04-19 (PR #180: fix/aoestats-phase06-pop-tag-backfill)

### Changed

- **aoestats Phase 06 CSV `notes` column now carries scoping tags.**
  Closes BACKLOG F6. `[POP:ranked_ladder]` on all 136 data rows
  (parity with sc2egset `[POP:tournament]` 35/35 and aoe2companion
  `[POP:ranked_ladder]` 74/74); `[PRE-canonical_slot]` on 30 rows
  (`p0_is_unrated` + `p1_is_unrated` × 15 quarters each: 8 primary
  + 7 counterfactual-reference). Classification rationale: only
  features literally indexing `team=0` / `team=1` carry the per-slot
  flag; aggregate / UNION-ALL-symmetric / match-level features do
  not. Zero metric-value regression; ICC ANOVA
  cohort_threshold=10 (0.0268 / 0.0148 / 0.0387) and PSI 2023-Q1
  focal_old_rating (0.037) unchanged. Spec §12 v1.0.5 11-column
  schema preserved.
- Notebook `01_05_08_phase06_interface.py` refactored with
  `PER_SLOT_FEATURES` constant + `_tag_prefix()` helper + idempotency
  assertion block.
- Thesis §4.1.4 + §4.4.6 — two `[REVIEW: post-F6 stale]` flags
  planted at grep-verifiable claims ("nie niesie jawnego tagu",
  "zwraca 0 dopasowań") that become false post-merge. Full prose
  rewrite deferred to Pass-2.

### Removed

- `pre_canonical_slot_flag_active` side-channel read of
  `01_05_06_temporal_leakage_audit_v1.json` in the Phase 06 notebook
  — superseded by explicit `PER_SLOT_FEATURES` constant.
- BACKLOG F6 entry (executed in this PR).

## [3.26.2] — 2026-04-19 (PR #179: chore/cleanup-stale-artifacts-defend-sequence-followup)

### Removed

- `NIGHT_SUMMARY_2026-04-17.md` — 2-day-old autonomous-session report;
  all referenced work has since merged via PRs #150-#177.
- `temp/` directory (5 files, 2 219 lines): `critique_3_4_3_5_r1.md`,
  `plan_01_05_sc2egset.md`, `plan_3_4_3_5_v1.md`, `plan_3_4_3_5_v2.md`,
  `session_report_2026-04-18.md`. All superseded by merged work in the
  `03_related_work.md` §3.4/§3.5 drafts, the Phase 01 §01_05 artifacts,
  and the DEFEND-IN-THESIS 3-PR sequence. Git history preserves content.
- `planning/dags/` (DAG.yaml + README.md) and `planning/specs/`
  (README.md only) — closes BACKLOG F5. DAG/spec pattern was
  decommissioned per memory `feedback_decommission_dag.md`; executors
  read `planning/current_plan.md` directly.

### Changed

- `planning/BACKLOG.md`: removed F2 (01_05 Temporal & Panel EDA —
  complete across all three datasets via PRs #162–#177 series);
  removed F5 (executed in this PR); F3 unblocking note added
  (previously blocked on F2, now actionable).
- `ARCHITECTURE.md` tier 9b: updated to reflect current planning-artifact
  structure (`current_plan.md` + `current_plan.critique.md` only; no
  DAG/spec derivations).

## [3.26.1] — 2026-04-19 (PR #TBD: chore/purge-planning-pr-177-defend-sequence-complete)

### Removed

- `planning/current_plan.md` reset to `<!-- No active plan -->` and
  `planning/current_plan.critique.md` deleted. Final post-merge purge
  for the DEFEND-IN-THESIS 3-PR sequence (PR #175, PR #176, PR #177).

### Changed

- CHANGELOG `[3.26.0]` header: `PR #TBD` → `PR #177` backfill.
- `planning/CHAPTER_4_DEFEND_IN_THESIS.md` residual #5 checkbox:
  `PR #TBD` → `PR #177` backfill.
- **DEFEND-IN-THESIS sequence complete**: all 6 residuals
  (#1 reference-window, #2 [POP:] scope, #3 observed-scale ICC,
  #4 744-player cohort, #5 [PRE-canonical_slot] flag, #6 N=2
  cross-game test limit) addressed across PR #175 (§4.1.3 +
  §4.1.4 + §4.1.2.1), PR #176 (§4.4.4 + §4.4.5 + Tabela 4.7), and
  PR #177 (§4.4.6 + §4.1.2.1 footnote). Pass-2 Claude Chat session
  pending for ~17 accumulated [REVIEW]/[UNVERIFIED] flags plus
  deferred MINORs.

## [3.26.0] — 2026-04-19 (PR #177: docs/thesis-ch4-canonical-slot-flag)

### Changed

- **Chapter 4 §4.4.6 + §4.1.2.1 footnote — DEFEND-IN-THESIS residual
  #5 `[PRE-canonical_slot]` flag.** Final PR in the DEFEND-IN-THESIS
  sequence; closes the 6-of-6 residual cycle.
  1. NEW §4.4.6 Flaga `[PRE-canonical_slot]` dla aoestats per-slot
     analyz. Three paragraphs: Geneza (W3 ARTEFACT_EDGE commit
     `ab23ab1d`; 80,3% higher-ELO → team=1; spec §1 line 71 + §11);
     Zakres per-slot vs aggregate (M1 fix — raw `matches_1v1_clean`
     per-slot `p0_civ` + `p1_civ`; aggregates arise post-Phase-02
     UNION-ALL; niezmiennik I5 cited correctly as symmetric player
     treatment); Zastosowania i plan zamknięcia (BACKLOG F1 Phase
     02 unblocker; F6 artifact-vs-spec divergence tracker; flag
     honest-matched as methodological convention not CSV metadata).
  2. §4.1.2.1 inline footnote at "team=1 wygrywa 52,27%" sentence.
- `planning/BACKLOG.md` F1 Predecessors bullet extended with PR-3
  thesis-side provenance reference.
- 3 [REVIEW] flags planted for Pass-2 resolution.
- **All 6 DEFEND-IN-THESIS residuals now addressed** across PR-1
  (#175, §4.1.3 + §4.1.2.1 + §4.1.4) + PR-2 (#176, §4.4.4 + §4.4.5)
  + PR-3 (§4.4.6 + §4.1.2.1 footnote).
- Two adversarial review rounds consumed (plan-side R1 verdict
  REVISE non-blocking — 2 MAJORs + 3 MINORs inline; execution-side
  R2 verdict PASS — 0 BLOCKERs + 0 MAJORs + 3 MINORs Pass-2/F6
  deferred).

## [3.25.0] — 2026-04-19 (PR #176: docs/thesis-ch4-stat-methodology-residuals)

### Changed

- **Chapter 4 §4.4 DEFEND-IN-THESIS residuals #3 + #6** addressed as
  Polish prose. Closes the stat-methodology cluster from
  `planning/CHAPTER_4_DEFEND_IN_THESIS.md`:
  1. §4.4.4 Evaluation metrics DRAFTABLE → DRAFTED. Four subsections
     (Metryki podstawowe, dyskryminacyjne, stratyfikowane, within-game
     / cross-game). Residual #6 (N=2 cross-game statistical-test
     inapplicability) absorbed at the cross-game paragraph, citing
     [Demsar2006] §3.2 with N ≥ 10 corollary framing. [#6]
  2. NEW §4.4.5 Wybór estymatora ICC (Residual #3). Defends
     observed-scale ANOVA ICC as cross-dataset-comparable headline;
     latent-scale argument via [Nakagawa2017] §2.2 + Browne 2005 as
     directional lower-bound, no plug-in formula. Closes PR-1's
     §4.1.2.1 + §4.1.4 forward-refs. [#3]
- **Tabela 4.7** — headline ICC reconciliation, three datasets,
  six columns (Korpus / ICC / 95% CI / N (graczy) / N (obs.) /
  Metoda CI). Cites spec v1.0.4 §14(b) (ANOVA-primary declaration).
- **5 new bibtex entries** (Nakagawa2017, Chung2013, Ukoumunne2003,
  WuCrespiWong2012, Gelman2007) — all verified via WebSearch.
- **7 [REVIEW] / [UNVERIFIED] flags** planted for Pass-2 resolution.
- **Two adversarial review rounds** consumed (plan-side verdict
  REVISE — 1 BLOCKER formula error, 4 MAJORs, 7 MINORs all
  addressed inline; execution-side verdict PASS — 0 BLOCKERs, 1
  MAJOR fixed inline, 5 MINORs 2 fixed inline + 3 deferred to
  Pass-2).

## [3.24.0] — 2026-04-19 (PR #175: docs/thesis-ch4-corpus-framing-residuals)

### Changed

- **Chapter 4 §4.1 DEFEND-IN-THESIS residuals #1, #2, #4** addressed as
  Polish prose. Closes the corpus-framing cluster from
  `planning/CHAPTER_4_DEFEND_IN_THESIS.md`:
  1. §4.1.3 tail paragraph defending the reference-window asymmetry
     (sc2egset + aoe2companion 4-month per spec §7; aoestats 9-week
     patch-anchored per spec §7 + §11 W3 ARTEFACT_EDGE). [#1]
  2. §4.1.2.1 paragraph on the aoestats 744-player cohort ceiling at
     N=10 default (sensitivity table 4 325 / 744 / 3 across N=5 / N=10 /
     N=20 verified against `01_05_05_icc_results.json`), attributed to
     spec §11 single-patch constraint, with M1 defensive sentence
     guarding the §4.1.2.1-read-in-isolation vulnerability. [#4]
  3. NEW §4.1.4 subsection scoping every cross-corpus claim as
     dataset-conditional per invariant #8. Honest-matched to artifact
     state (sc2egset + aoe2companion carry jawny `[POP:]` tag; aoestats
     scope implicit via spec §0 + cleaning rule R02). [#2]
- `planning/BACKLOG.md` F6 — new Category-D entry for aoestats CSV
  `[POP:]` + `[PRE-canonical_slot]` tag backfill (pre-empts PR-3
  BLOCKER for `[PRE-canonical_slot]`).
- Five [REVIEW] flags planted for Pass-2 resolution; no new bibtex
  entries (Demsar2006 reused from §2.6).
- Two adversarial review rounds consumed (plan-side verdict REVISE
  → execution-side verdict PASS with 1 MAJOR char overage accepted
  + 2 MINORs fixed inline + 1 MINOR deferred to Pass-2).

## [3.23.1] — 2026-04-19 (PR #174: chore/purge-planning-pr-173)

### Removed

- `planning/current_plan.md` contents (replaced with `<!-- No active plan -->`)
  and `planning/current_plan.critique.md` (deleted). Both were stale artifacts
  of the `feat/01-05-aoestats` plan cycle (merged via PR #171; purge deferred
  across PRs #172 and #173). Per `planning/README.md` post-merge purge
  protocol; `planning/INDEX.md` was already at template state.

## [3.23.0] — 2026-04-19 (PR #172: fix/01-05-phase06-schema-harmonization)

### Changed

- **Spec `CROSS-01-05-v1` bumped to v1.0.5: Phase 06 interface schema
  harmonization.** Closes DEFEND-IN-THESIS #3a + #3b from the 2026-04-19
  pre-01_06 adversarial review. Three changes to §12:

  1. **Two new columns**: `metric_ci_low DOUBLE NULL` and `metric_ci_high
     DOUBLE NULL`. CI bounds for a metric now live on the same row in these
     columns. Previously `aoe2companion` emitted CI bounds as separate rows
     with `metric_name=icc_lpm_ci_low`/`icc_lpm_ci_high` — those names are no
     longer in the closed enumeration and would be dropped by a
     schema-validating consumer.
  2. **Closed `metric_name` enumeration**: `{psi, cohen_h, cohen_d, ks_stat,
     icc_lpm_observed_scale, icc_anova_observed_scale, icc_glmm_latent_scale}`.
     Consumers MUST reject out-of-enumeration values (assertion in all three
     dataset notebooks).
  3. **`cohort_threshold=0` sentinel** for uncohort-filtered primary
     analyses. Previously sc2egset emitted NULL here (ambiguous between
     B2-uncohort and missing metadata). NULL is now reserved for metadata
     gaps and blocks Phase 06 ingest.

  All three datasets' Phase 06 interface CSVs now have **11 columns** and
  join cleanly on `(dataset_tag, quarter, feature_name, metric_name)` with
  uniform CI semantics.

- **sc2egset `01_05_07_phase06_interface.py`**: `cohort_threshold=0` on PSI
  and DGP rows (was NULL); ICC rows populate `metric_ci_low`/`metric_ci_high`
  from `variance_icc_sc2egset.csv`; closed-enum validator added; schema
  JSON bumped to `schema_version: "1.0.5"` with new column descriptions.
- **aoe2companion `01_05_07_phase06_interface.py`**: stopped emitting
  `icc_lpm_ci_low`/`icc_lpm_ci_high` as separate rows; inlined CI bounds
  into `metric_ci_low`/`metric_ci_high` columns on the primary row. Total
  ICC rows reduced from 4 to 3 (one per estimator); grand-total row count
  76 → 74. Closed-enum validator added.
- **aoestats `01_05_08_phase06_interface.py`**: populated CI columns for
  each of the 6 per-cohort-threshold ICC rows (post-v1.0.4) from the
  cluster-bootstrap CI (ANOVA) / delta-method CI (LMM); schema validator
  bumped to 11 columns; closed-enum assertion added.

## [3.22.0] — 2026-04-19 (PR #TBD: fix/01-05-aoestats-icc-cohort-axis)

### Changed

- **aoestats 01_05_05 ICC — sensitivity axis realigned to spec §6.2 cohort
  thresholds.** Prior notebook used `sample_sizes = [20_000, 50_000, 100_000]`
  via stratified reservoir sampling. aoestats's single-patch reference window
  has only ~744 eligible players at N=10, so all three "sample sizes"
  degenerated to the full population — producing three identical ICC rows
  labeled as sensitivity. 2026-04-19 pre-01_06 adversarial review flagged
  this as DEFEND-IN-THESIS #2 (axis confusion between §6.2 cohort-threshold
  and variance-decomposition sample-group size).

  v1.0.4 (this PR): the sensitivity axis is spec §6.2 cohort match-count
  thresholds `N ∈ {5, 10, 20}` (the same `N` spec §6 uses for survivorship).
  Each threshold produces a distinct cohort of players with ≥N prior
  matches in the reference window. Primary headline is ANOVA @ N=10 (spec
  §6.3 default + v1.0.4 §14(b) cross-dataset ANOVA convention).

  Post-fix sensitivity table (genuinely informative):
  - N=5: 4,325 players, ANOVA `0.0251 [0.0183, 0.0324]`, LMM `0.0248 [0.0237, 0.0259]`
  - **N=10 (primary): 744 players, ANOVA `0.0268 [0.0148, 0.0387]`, LMM `0.0259 [0.0232, 0.0286]`**
  - N=20: 3 players, ANOVA `0.0176 [0, 0.0226]`, LMM `0.0172 [0, 0.0449]`

  Verdict unchanged: **FALSIFIED** (primary ANOVA 0.0268 below the
  pre-registered [0.05, 0.20] hypothesis range). LMM and ANOVA now agree
  to within 0.001 at each threshold; both CIs contain their point estimates
  (sanity asserts pass from PR #167).

  **N=20 scope note for Chapter 4:** only 3 players have ≥20 matches in
  the patch-66692 reference window (9 weeks). This is a reference-window
  artifact, not a dataset limitation — the single-patch §11 W3 binding
  imposes the 9-week window, which limits how restrictive a cohort
  threshold can be. Chapter 4 notes this as a scope-limitation footnote.

  JSON schema change: `icc_by_sample_size` (old) renamed to
  `icc_by_cohort_threshold`. Per-block key renamed from `n{K}k` to
  `n_min{N}`. Legacy key name tolerated by the Phase 06 interface notebook
  for transitional backwards compatibility.

- **aoestats Phase 06 interface CSV** now emits 6 ICC rows (3 cohort
  thresholds × 2 estimators) instead of 3 (one per sample size, mixing
  estimators). Each row carries the correct `cohort_threshold` value
  (5, 10, or 20) instead of a blanket 10. `metric_name` values are now
  the specific estimator names (`icc_anova_observed_scale`,
  `icc_lpm_observed_scale`) instead of the generic `icc`.

### Removed

- Stale cohort artifact files `icc_sample_profile_ids_{20k,50k,100k}.csv`
  (superseded by `icc_cohort_profile_ids_n{5,10,20}.csv` — one ID list
  per cohort threshold).

## [3.21.5] — 2026-04-19 (PR #TBD: fix/01-05-spec-v1-0-4-icc-anova-primary)

### Changed

- **Spec `CROSS-01-05-v1` bumped to v1.0.4.** Extends the v1.0.2 §14(b)
  ANOVA-primary ICC headline convention from `aoe2companion` to `sc2egset`
  and `aoestats`. All three datasets' Phase 06 interface CSV headline ICC
  rows now use `metric_name = icc_anova_observed_scale`. Per-dataset CSVs
  continue to carry LMM and GLMM estimates as diagnostics.

  Cross-game ICC headlines under v1.0.4:
  - sc2egset: `0.0463` (ANOVA)
  - aoe2companion: `0.003013` (ANOVA, bootstrap CI `[0.001724, 0.004202]`)
  - aoestats: `0.0268` (ANOVA, bootstrap CI `[0.0145, 0.0407]`)

  All three directly comparable: observed-scale ANOVA ICCs on the same
  outcome (`won`) under the same estimator (Wu/Crespi/Wong 2012 CCT
  33(5):869-880). Closes DEFEND-IN-THESIS #1 from the 2026-04-19
  pre-01_06 adversarial review.

  Zero code / artifact changes. All three datasets' notebooks already
  emit both LMM and ANOVA ICC values; only the headline reporting
  convention changes. sc2egset LMM (`0.0456`) and ANOVA (`0.0463`)
  agree within 1.5% — no directional change to any finding.

  Rationale (full detail in spec §14 and `reports/research_log.md`
  2026-04-19 CROSS entry): REML LMM on Bernoulli outcomes near the
  τ²-boundary shrinks toward zero (Chung et al. 2013 Psychometrika
  78(4):685-709). This applies symmetrically to any Bernoulli outcome
  on any cohort, making the v1.0.2 aoec-local choice the correct
  cross-dataset convention.

## [3.21.1] — 2026-04-19 (PR #TBD: fix/01-05-sc2egset-leakage-substantive)

### Fixed

- **sc2egset leakage-audit Q1 redesign (v2, post-PR #164 adversarial review).**
  The PR #164 cleanup removed a dead-code `QUERY1_REF_SQL` tautology but the
  surviving "real" check `QUERY1_MEANING_SQL` was itself structurally
  tautological: the outer `WHERE started_at BETWEEN REF_START AND REF_END`
  made the inner `COUNT(*) FILTER (WHERE started_at < REF_START OR
  started_at >= REF_END)` always 0 by construction. Same defect affected
  the Q1c tested-period check. The `assert future_leak_count == 0` gate
  was therefore decorative.

  Replaced with three substantive sub-checks ported from the aoec pattern
  (`sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_08_leakage_audit.py`):
  - **Q1a (ref-range integrity):** DB `MIN/MAX(started_at)` in the spec §7
    reference window lies within declared bounds, `count > 0`. Catches DB
    timezone bugs and filter-predicate regressions.
  - **Q1b (quarter-label consistency):** for each tested quarter, the
    `MIN/MAX(started_at)` of rows labeled that quarter lies within the
    ISO-calendar bounds of that quarter. Catches off-by-one in the
    `CONCAT(EXTRACT..., CEIL(EXTRACT.../3.0))` quarter-label SQL.
  - **Q1c (PSI source-string substring check):** the PSI notebook source
    (`01_05_02_psi_quarterly.py`) literally contains the spec §7 date
    substrings `2022-08-29` and `2023-01-01`. Catches silent
    reference-window drift between `01_05_02` and this audit.

  Each sub-check has its own `PASS/FAIL` flag and its own `assert`. The
  composite `future_leak_count` int is retained for JSON back-compat.
  Closes I3 VIOLATED on sc2egset per the 2026-04-19 pre-01_06 adversarial
  review. Does not change the `Q7 PASS` verdict.
## [3.21.2] — 2026-04-19 (PR #TBD: fix/01-05-aoestats-ngroups-ci-assert)

### Fixed

- **aoestats `compute_icc_lmm` `.ngroups` attribute bug** at
  `src/rts_predict/games/aoe2/datasets/aoestats/analysis/variance_decomposition.py:92-93`.
  The function referenced `result.ngroups`, which does not exist on
  statsmodels `MixedLMResults`. The correct accessor is `result.model.n_groups`
  (the aoec port was already correct). Pre-fix, every LMM delta-method CI
  call raised `AttributeError`, which `01_05_05_variance_decomposition_icc.py`'s
  bare `except Exception` silently recorded as `convergence_warning`. The
  "LMM failed to converge" claim in the aoestats research log was a
  misdiagnosis. Flagged by the 2026-04-19 pre-01_06 adversarial review.
- **aoestats ANOVA cluster-bootstrap CI was inverted** (lower bound > point
  estimate) due to a cluster-bootstrap resampling bug at
  `variance_decomposition.py:213-241`. When a group was sampled with
  replacement multiple times, the bootstrap concatenated its rows but reused
  the *original* group id, so `_icc_anova_point`'s pandas-groupby collapsed
  the duplicated clusters back into one — inflating `k_bar` while holding
  `n_groups` constant, biasing SSB upward, producing CIs that did not contain
  their point estimate. Pre-fix aoestats 50k run: `point=0.0268`,
  "CI"=[0.0494, 0.0759]. Post-fix: `[0.0145, 0.0407]` (contains point).
  Fix ports the aoec cluster-bootstrap pattern: each resampled group is
  re-tagged with a fresh unique id so duplicates count as distinct clusters
  (Ukoumunne et al. 2012 PMC3426610).
- **CI sanity asserts added** to `01_05_05_variance_decomposition_icc.py` —
  `assert ci_lo ≤ point ≤ ci_hi` on both LMM and ANOVA results, matching the
  sc2egset pattern. Catches any future re-occurrence of the inverted-CI
  pathology.
- **Dead ternary** `primary_icc = icc_anova if not np.isnan(icc_lmm) else
  icc_anova` (both branches returned ANOVA) rewritten as
  `primary_icc = icc_lmm if not np.isnan(icc_lmm) else icc_anova`. Spec §8
  literal binding for aoestats (v1.0.1) prefers LMM as primary.

### Changed

- **aoestats ICC verdict retained: FALSIFIED.** With the bug fixed:
  LMM ICC = 0.0259 [0.0232, 0.0286]; ANOVA ICC = 0.0268 [0.0145, 0.0407].
  Both well below the pre-registered hypothesis range [0.05, 0.20]. The
  direction of the conclusion is unchanged; the evidentiary chain is now
  sound — LMM and ANOVA agree to within 0.001 on the point estimate, and
  both CIs contain their respective points.
## [3.21.3] — 2026-04-19 (PR #TBD: fix/01-05-aoestats-leakage-substantive)

### Fixed

- **aoestats leakage-audit Q7.1 gate redesign (v3).** Pre-this-PR (v2, from
  PR #165) the gate compared a PSI-JSON `reference_window.start/.end` against
  Python constants `REF_START/REF_END`. Both sides were written by the
  SAME file (`01_05_02_psi_pre_game_features.py`) using the SAME hard-coded
  constants: a silent widening of the PSI SQL filter would not be caught.
  v3 replaces with two substantive sub-checks:
  - **Q7.1a (DB ref-range integrity):** `MIN/MAX(started_at)` of rows within
    the declared spec §7 reference window lies strictly within those bounds;
    row count > 0. Catches DB timezone bugs and filter-predicate regressions.
  - **Q7.1b (PSI source substring):** `01_05_02_psi_pre_game_features.py`
    source literally contains the spec §7 date substrings `2022-08-29` and
    `2022-10-27`. Catches silent SQL-filter drift between the PSI notebook
    and this audit.

  Each sub-check has its own PASS/FAIL flag and independent `assert`. The
  composite `future_leak_count` int is retained for JSON back-compat.
  Post-fix run: `Q7.1a min=2022-08-29 00:04:05, max=2022-10-26 23:52:02,
  count=70,934 → PASS`; `Q7.1b missing=none → PASS`. Closes I3 PARTIAL
  status on aoestats per the 2026-04-19 pre-01_06 adversarial review.
  Does not change the `Q7 PASS` verdict.
## [3.21.4] — 2026-04-19 (PR #TBD: fix/01-05-aoestats-spec-patch-amendment)

### Changed

- **Spec `CROSS-01-05-v1` bumped to v1.0.3.** `reports/specs/01_05_preregistration.md`
  gains a §14 v1.0.3 amendment correcting the aoestats reference-window patch
  ID from `125283` to `66692`. Empirical verification against `matches_raw`
  (2026-04-19) established that patch `125283` covers `2024-10-15 .. 2025-04-11`
  (over 2 years AFTER the declared reference window `[2022-08-29, 2022-10-27]`)
  while patch `66692` is the only patch present during the reference window
  (241,981 matches total, 123,367 in the window). The original v1.0 spec cited
  `125283` as a pre-empirical-validation error; the aoestats notebook's
  `REF_PATCH = 66692` constant was always scientifically correct.

  Spec edits (3 textual, zero parameter changes):
  - §7 table row: `patch 125283` → `patch 66692`.
  - §7 aoestats-rationale paragraph: `patch 125283` → `patch 66692`.
  - §11 patch-anchored reference justification: `patch 125283` → `patch 66692`.
  - §12 Phase 06 interface `reference_window_id` example: `2022-Q3-patch125283`
    → `2022-Q3-patch66692` (the CSV artifact already emitted the correct value).

  Closes the last BLOCKER from the 2026-04-19 pre-01_06 adversarial review
  (I9 VIOLATION: spec drift without §14 amendment).

### Fixed

- **Stale `patch 125283` references cleaned up** in:
  - `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_02_psi_pre_game_features.py` (line 40 critique-fix comment + line 67 `REF_PATCH` constant comment + line 390 MD emission)
  - `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_08_phase06_interface.py` (docstring hypothesis line 27)
  - `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_09_gate_memo.py` (two occurrences)
  - `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_summary.md` (header)
  - `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_09_gate_memo.md` (two occurrences)

  Data-file references to `125283` (e.g., `patch_map.csv`, `patch_civ_win_rates.csv`, `01_05_03_patch_regime_summary.md`) retained — `125283` is a valid later-period patch appearing in the `matches_raw` corpus; those files correctly document its empirical existence.

## [3.20.0] — 2026-04-19 (PR #TBD: feat/01-05-sc2egset)

### Added

- **01_05 Temporal & Panel EDA — sc2egset:** 8 content notebooks + 1 scaffold under
  `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/`. Notebooks implement Q1
  quarterly grain, Q2 PSI (uncohort-filtered per B2 critique fix), Q3 tournament_era
  secondary regime (hand-mapped 70-dir lookup per M2), Q4 triple survivorship, Q6 ICC
  (LPM + ANOVA + GLMM attempt per B3), Q7 leakage audit (PASS), Q8 DGP diagnostics
  (M9 fix: join matches_flat_clean for is_duration_suspicious), Q9 Phase 06 interface
  CSV (35 rows, 9 columns, schema-valid). All artifacts under
  `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/`.
- **statsmodels** dependency added to `pyproject.toml` (v0.14.6) for mixedlm ICC fitting.
- **tournament_tier_lookup.csv** (70 rows hand-mapped via Liquipedia tier heuristics).
- **INVARIANTS.md §4** populated with 8 01_05 empirical findings (I6: each cites SQL).
- **INVARIANTS.md §5** updated with I8 partial (Spec §1 schema divergence) and M7
  tournament scope note (Heckman 1979 selection bias framework).
- **STEP_STATUS.yaml** updated with 8 new 01_05 step entries (all `status: complete`).
- **PIPELINE_SECTION_STATUS.yaml** 01_05 → `status: complete`.
- **ROADMAP.md** 01_05 step blocks appended (step names + gates, no scientific claims).
- **research_log.md** 2026-04-18 01_05 entry + [CROSS] B2 PSI cohort decision.
- **reports/research_log.md** [CROSS] entries for B2 decision + pointer update.
- **decision_gate_sc2egset.md** with Q1..Q9 execution table and gate verdict.

### Changed

### Fixed

### Removed

## [3.19.1] — 2026-04-19 (PR #TBD: fix/01-05-aoec-adversarial-followup)

### Changed

- **Spec `CROSS-01-05-v1` bumped to v1.0.2.** `reports/specs/01_05_preregistration.md`
  gains a §14 v1.0.2 amendment documenting three aoe2companion-specific
  §8 adaptations (others datasets unaffected): (a) LMM sample-size cap for
  aoec 54k-player scale, (b) ANOVA promoted from secondary to robust primary
  estimator, (c) GLMM explicitly skipped with Phase 02+ deferral. Per spec
  §13 deviation procedure — closes adversarial-review BLOCKER 1 on PR #162.
- **`01_05_05_icc.py` — ANOVA promoted to primary.** `compute_icc_anova` with
  200-sample cluster bootstrap CI is now the headline estimator. LMM remains
  as a labeled diagnostic with explicit disclosure of the observed-scale LPM
  caveat and invalid delta-method CI on Bernoulli + unbalanced-`n_i` design
  (Chung et al. 2013, Psychometrika 78(4):685-709). JSON schema: `icc_anova_*`
  primary, `icc_lpm_ci_*_invalid_asymptotic` rename for the diagnostic CI.
- **Verdict restated.** Hypothesis [0.05, 0.20] remains **falsified**, now on
  the ANOVA point estimate 0.003013 with bootstrap CI [0.001724, 0.004202]
  — more than 10× below the lower hypothesis bound. Direction unchanged;
  evidentiary chain now defensible.

### Fixed

- **Leakage audit Check 1 redesigned.** `01_05_08_leakage_audit.py` Check 1a/1b
  had WHERE clauses of the form `(A ∧ B) ∧ (¬A ∨ ¬B)` — logically
  unsatisfiable, returned 0 regardless of data. Replaced with three
  substantive sub-checks: (1a) reference-cohort `MIN`/`MAX(started_at)`
  lie within declared spec §7 bounds with non-empty cohort; (1b) each
  tested quarter's row range lies within its ISO-calendar quarter; (1c)
  `01_05_02_psi_shift.json` `sql_queries` literally contains the spec §7
  timestamp bounds. Closes adversarial-review BLOCKER 2 on PR #162.
- **Headline ICC number reconciled.** Single atomic notebook run produced
  canonical values in JSON and `01_05_05_icc.md`; research_log entry
  rewritten to match JSON byte-for-byte. 10k LMM sensitivity
  `converged=True` now consistent across all artifacts (previous PR #162
  research_log prose "converged=False with boundary warnings" was
  incorrect — boundary warnings fire but do not set `converged=False`).
  Closes adversarial-review BLOCKER 3 on PR #162.

## [3.19.0] — 2026-04-19 (PR #TBD: feat/01-05-aoe2companion)

### Added

- **aoe2companion 01_05 Temporal & Panel EDA** — completes the 8-notebook
  pipeline section under spec `CROSS-01-05-v1` v1.0.1 (commit `7e259dd8`).
  Recovers from an earlier hang in 01_05_05 (`statsmodels.mixedlm` called on
  ~7.4 M rows × ~20 k groups over the full analysis window — intractable).
  Recovery rewrite scopes the ICC fit to the spec §7 reference window
  (2022-08-29..2022-12-31) and caps LMM at 10 k groups. ANOVA ICC via a new
  pandas-groupby fast path (`compute_icc_anova_fast`) at all three sample
  sizes {5 k, 10 k, 20 k}. All 8 notebooks execute end-to-end; artifacts in
  `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/`.
  Scientific outcome: `ICC_lpm=0.000487`, `ICC_anova=0.003013` — the
  hypothesis range [0.05, 0.20] is **falsified**, consistent with calibrated
  matchmaking equalizing `won` to ~0.5 across players. The per-player skill
  signal lives in `rating_pre`, not `won`.
- **aoe2companion variance_decomposition module** at
  `src/rts_predict/games/aoe2/datasets/aoe2companion/analysis/variance_decomposition.py`
  with LMM + ANOVA ICC helpers, `stratified_reservoir_sample`, and a
  pandas-groupby fast path. 11 unit tests in
  `tests/rts_predict/games/aoe2/datasets/aoe2companion/analysis/`.

### Changed

- **pyproject.toml**: added `statsmodels >=0.14,<1` as a project dependency
  (required by 01_05_05 LMM ICC).

### Fixed

- **01_05_08 leakage audit**: replaced `Path(__file__).parent` (undefined
  under a Jupyter kernel) with a `get_reports_dir`-rooted fallback so the
  notebook executes both as a plain-python script and via
  `jupytext --execute`.
- **compute_icc_lmm attribute bug**: the aoestats version of this helper
  references `result.ngroups`, which does not exist on statsmodels 0.14
  `MixedLMResults`. The aoe2companion port uses `result.model.n_groups`.

### Removed
## [3.21.0] — 2026-04-19 (PR #TBD: feat/01-05-aoestats)

### Added

- **aoestats Pipeline Section 01_05 Temporal & Panel EDA** (9 steps; spec v1.0.1 SHA 7e259dd8). All 3 BLOCKER and 8 MAJOR critique fixes applied. Key results: PSI PASSED (rating drift >= 0.10 PSI in 6/8 quarters), ICC FALSIFIED (ANOVA ICC 50k = 0.0268 in early crawler period), leakage audit PASS, Phase 06 interface emitted (134 rows, 9 columns, reference_window_id = "2022-Q3-patch66692"). BACKLOG F1 documented: canonical_slot column absent, Phase 02 unblocker required.
- **Analysis modules** for aoestats PSI, survivorship, and variance decomposition: `src/rts_predict/games/aoe2/datasets/aoestats/analysis/{psi,survivorship,variance_decomposition}.py`. Feature-type routing (B2 fix), stratified reservoir sampling (M3 fix), ANOVA ICC with bootstrap CI (M2 fix). 53 unit tests all passing.

## [3.18.0] — 2026-04-18 (PR #TBD: feat/pre-01-05-cleanup)

### Added

- **Identity-resolution meta-rule (Invariant I2 extension)** with 4-step decision procedure + 5 precedence branches (i–v). Reconciles 3 locally-defensible but inconsistent per-dataset identity strategies (sc2egset → branch (iii); aoe2companion → (i); aoestats → (v) structurally-forced). No universal Christen-2012 5% threshold; each dataset declares tolerance empirically in its `INVARIANTS.md` §2.
- **Per-dataset `INVARIANTS.md` scaffolds** for sc2egset, aoe2companion, aoestats per `scientific-invariants.md` L206–207. §1 Data-source, §2 Identity, §3 Temporal seeded from prior 01_04 research_log entries. §4 Empirical findings is a prose stub populated by 01_05 / Phase 02. §5 cross-reference lists only VIOLATED/PARTIAL exceptions.
- **aoestats 01_04_05 — Team-Slot Asymmetry Diagnosis (I5)**. Diagnostic battery of 5 SQL queries + Cochran–Mantel–Haenszel stratified by civ-pair × quarter (13,509 strata) produces verdict **ARTEFACT_EDGE**: upstream API assigns team=1 to the higher-ELO player in 80.3% of games (mean ELO diff +11.9), masking as a 52.27% team=1 win rate. Not a game-mechanical effect; canonical_slot column required before Phase 02 feature engineering.
- **Cross-dataset 01_05 pre-registration spec** at `reports/specs/01_05_preregistration.md` (spec_id `CROSS-01-05-v1`, v1.0.1). Locks 9 parameter groups (Q1–Q9) binding sc2egset / aoe2companion / aoestats 01_05 to identical protocol for Phase 06 Cross-Domain Transfer compatibility. Key decisions: overlap window 2022-Q3→2024-Q4; ADF/KPSS forbidden cross-dataset (effect sizes + PSI only); reference period non-overlapping with tested; `regime_id ≡ calendar quarter` (honest acknowledgment); triple survivorship analysis; POST_GAME diagnostics in dedicated §10; aoestats leakage audit incorporates W3 verdict.
- **Pre-commit spec-binding hook** `scripts/check_01_05_binding.py` (~134 LOC). Scans `sandbox/*/01_exploration/05_temporal_panel_eda/*.py` for `# spec: reports/specs/01_05_preregistration.md@<SHA>` docstring binding; validates SHA via `git cat-file -e`. No-op during Phase 01_04. Both `--check` (staged) and `--all` (CI) modes.

### Fixed

- **Post-PR #158 hygiene** (merged in PR #159): dedup duplicate `01_04_04b` block in sc2egset `STEP_STATUS.yaml`; relocate misplaced `01_04_04b` step YAML in sc2egset `ROADMAP.md` from Phase 07 back under Phase 01 / Pipeline Section 01_04; purge merged-PR planning artifacts per `planning/README.md`.
- **aoe2companion 01_04_04 CI-drift reconciliation (Invariant I6)**. Narrative cited `p̂=0.8818, CI=[0.8671, 0.8964]`; artifact JSON cited `p̂=0.8782, CI=[0.8634, 0.8931]`. Root cause: DuckDB `REPEATABLE(seed)` reservoir sampling is deterministic only for fixed input row-order; `matches_raw` was rebuilt between narrative and artifact runs (DB mtime preceded artifact mtime by ~1h24m). Both triples preserved forensically via strikethrough + footnote at 3 aoec sites + 1 root CROSS site. Permanent reproducibility caveat added to aoec `INVARIANTS.md` §3. Christen VERDICT A is preserved under either triple.

## [3.17.0] — 2026-04-18 (PR #TBD: feat/01-04-04-sc2egset-worldwide-identity)

### Added
- **sc2egset 01_04_04b — `player_identity_worldwide` VIEW (decomposition-based)**.
  Follow-up to PR #157 identity-resolution step. Exposes the full Battle.net
  `R-S2-G-P` qualifier of each toon_id as `player_id_worldwide`, with
  segments parsed into queryable integer columns (region_code, realm_code,
  profile_id) + human-readable labels. 7 cols, 2,494 rows. Non-destructive
  (I9).
- **Empirical resolution of 01_04_04 open questions:**
  - `userID` cardinality=16 = local Battle.net profile slot indices stored
    in SC2 replay header (NOT a player identifier)
  - 2 empty-toon_id outlier rows characterized as observer-profile ghost
    entries from two distinct tournaments (IEM Katowice 2017, HomeStory Cup
    XIX 2019) ~850 days apart — not systematic; isolated parsing anomalies
  - 273 toon_ids have multiple nicknames across the 2016–2024 span
    (clan-tag changes, e.g., Serral as `<mYi>Serral` / `<ENCE>Serral` /
    `<BASKGG>Serral`); VIEW uses ROW_NUMBER() to pick most-frequent
    nickname per toon_id
- Schema YAML with 7 cols + I2/I6/I7/I9/I10 invariants + explicit
  region-scoping limitation note (multi-region human = multiple
  player_id_worldwide; upgrade path documented via future manual
  tournament-roster curation if ever warranted).
- Validation JSON with 8 SQL queries verbatim + 6 literature URLs +
  outlier investigation block.

### Changed
- sc2egset `STEP_STATUS.yaml` adds `01_04_04b: complete`.
- sc2egset `PIPELINE_SECTION_STATUS.yaml` 01_04 flip complete → in_progress
  → complete (roundtrip).
- sc2egset `ROADMAP.md` appends 01_04_04b sub-step block.
- sc2egset `research_log.md` prepends 01_04_04b entry.

### Fixed
- R1 drafted 5-signal Fellegi-Sunter behavioral classifier (APM-JSD / race /
  clanTag / MMR / temporal) — rejected for scope drift into
  behavioral-fingerprinting when the structural question was simpler.
- R2 drafted external-bridge catalog (Liquipedia / Aligulac / sc2pulse /
  Blizzard OAuth) — rejected by web-verified adversarial: no external
  source exposes (nickname → region-scoped profile-id) at bulk scale.
- R3 drafted sha256 composite stub — rejected for redundant encoding (toon_id
  already contains the region+realm segments being re-hashed).
- R4 (shipped): decomposition VIEW, the simplest honest answer.

### Removed

## [3.16.0] — 2026-04-18 (PR #TBD: feat/01-04-04-identity-resolution)

### Added
- **01_04_04 Identity Resolution — 3-dataset exploratory step** completing the
  Phase 01 identity-characterization gap. No DDL; pure census + decision-ledger
  artifacts routing 15 DS-*-IDENTITY-* decisions (5 per dataset) to Phase 02.
- **Cross-dataset VERDICT A (strong)**: aoestats `profile_id` and aoec `profileId`
  share the same integer namespace (aoe2insights.com API). Both sides' 95% CIs
  exclude 0.5 by wide margin (aoec [0.867, 0.896], aoestats [0.992, 0.999] with
  95.3% rating-agreement on matched pairs). Implication: aoe2companion `name`
  column can supply I2 canonical nicknames to aoestats via profileId JOIN —
  resolves aoestats structural nickname gap (no native nickname column).
- **sc2egset identity census**: 0 cross-region toon_ids (Battle.net scoping
  confirmed), 30.6% within-region LOWER(nickname) collision rate (6× Christen
  2012 threshold — nickname-alone unsafe), Fellegi-Sunter temporal classes
  A=294 (multi-account candidates), B=15,474 (disjoint), C=317 (degenerate),
  userID cardinality 16 confirmed as slot index.
- **aoestats civ-fingerprint JSD**: within-profile p50=0.1262 vs cross-profile
  p50=0.3606 — 2.9× gap confirms civ-preference temporal stability as a
  behavioral identity surrogate (Hahn et al. 2020 adjacent-literature
  anchor, hedged in MD). 489 (game_id, profile_id) duplicates match 01_03_03
  anchor exactly. `-1` sentinel hypothesis empirically refuted for aoestats.
  replay_summary_raw confirmed Python-dict parseable (feasibility only).
- **aoe2companion identity census**: 277M match-player rows, 2.66M distinct
  profileIds, 12.97M sentinel=-1 (4.7%). Rename history 2.06% renamers (2
  names); 3.7% name-collision rate; 80.8% country-stable; 0.035% multi-country.
  Join integrity: matches_raw ⊇ profiles_raw (0 orphans); rm_1v1 ratings
  coverage 38.4%.
- 3 new sandbox notebooks (jupytext-paired .py + .ipynb); 6 new artifact
  files (JSON + MD per dataset); 5 supplementary artifacts for sc2egset (2
  CSVs + 3 PNGs).
- 15 `DS-{SC2,AOESTATS,AOEC}-IDENTITY-01..05` decisions routed to Phase 02
  planner as grounding for canonical-identity-VIEW design.
- `reports/research_log.md` CROSS entry reconciling the 3-dataset findings
  and declaring VERDICT A.

### Changed
- All 3 datasets' ROADMAP blocks append 01_04_04 step definition.
- STEP_STATUS.yaml 01_04_04 → complete across all 3 datasets.
- PIPELINE_SECTION_STATUS.yaml 01_04 flip: complete → in_progress → complete
  (addendum roundtrip per 01_04_02/03 precedent).
- Research logs prepended with 01_04_04 per-dataset narrative entries.
- Minor auto-drift: sc2egset schema YAMLs + 01_04_02/03 artifacts have
  research_log.md line-number citation updates (333 → 424) from log growth;
  cosmetic, not substantive.

### Fixed
- Single pre-execution adversarial round (APPROVE_WITH_WARNINGS; 5 WARNINGs
  embedded in executor briefs): ladder-filter symmetry for cross-dataset
  preview, decision-count standardization (≥5 per dataset), CI-aware verdict
  HALT rubric, civ-JSD adjacent-literature hedge, I7 threshold provenance for
  every numeric threshold (5% / 0.10/0.30/0.50 / 1% / 50-ELO / 60s / 2.26).

### Removed

## [3.15.0] — 2026-04-18 (PR #TBD: feat/01-04-02-duration-augmentation)

### Added
- **01_04_02 augmentation across 3 datasets: `duration_seconds` + outlier flags at cleaning stage.**
  Moves duration derivation upstream from 01_04_03 minimal history view. Centralizes outlier
  flagging + POST_GAME_HISTORICAL token at the canonical clean-view layer so all downstream
  consumers inherit the signal uniformly.
- **sc2egset `matches_flat_clean`**: 28 → 30 cols. Adds `duration_seconds BIGINT` +
  `is_duration_suspicious BOOLEAN`. Source: `player_history_all.header_elapsedGameLoops / 22.4`
  via aggregated LEFT JOIN. 0 suspicious rows (no outliers).
- **aoestats `matches_1v1_clean`**: 20 → 22 cols. Adds same 2 cols. Source:
  `matches_raw.duration / 1_000_000_000` (Arrow duration[ns] → BIGINT nanoseconds).
  28 suspicious matches confirmed (matches 01_04_03 empirical 56 player-rows ÷ 2).
- **aoe2companion `matches_1v1_clean`**: 48 → 51 cols. Adds 3 cols including
  `is_duration_negative BOOLEAN` (strict `< 0`) for 342 clock-skew rows. Source:
  `EXTRACT(EPOCH FROM (matches_raw.finished - matches_raw.started))`. 142 suspicious
  + 342 negative + 16 zero-duration (documented as known state for Phase 02).
- Parallel 3-planner + 3-executor dispatch pattern: combined plan integration + single
  adversarial round per user directive. New jupytext notebooks for sc2egset + aoec
  (separate from original 01_04_02 notebooks); aoestats amends existing notebook.

### Changed
- Schema YAMLs for all 3 datasets' clean views now carry `schema_version` line and
  POST_GAME_HISTORICAL invariant extensions (I3 + I7 provenance).
- All 3 datasets' ROADMAP blocks have 01_04_02 addendum sections documenting duration
  provenance + expected outlier counts.
- All 3 datasets' research_log files have ADDENDUM entries prepended (reverse-chronological).

### Fixed
- Threshold 86,400s (24h) applied canonically across 3 datasets for I8 cross-dataset
  comparability (was implicit in 01_04_03 Gate +5b; now explicit cleaning contract).

### Removed

## [3.14.0] — 2026-04-18 (PR #TBD: feat/01-04-03-aoe2-minimal-history)

### Added
- **Phase 01 Step 01_04_03 — aoe2 datasets + sc2egset 9-col extension.** Completes
  the 3/3 dataset cross-dataset harmonization substrate for Phase 02+ rating-system
  backtesting. Originally scoped as aoe2-only; extended mid-PR per user directive
  to bump ALL 3 datasets' `matches_history_minimal` from 8 → 9 cols by adding
  `duration_seconds` BIGINT (POST_GAME_HISTORICAL). sc2egset's 8-col view from
  PR #152 is updated in-place; aoestats + aoe2companion new at 9 cols.
- **`duration_seconds` column (9-col extension — all 3 datasets):**
  - sc2egset: `CAST(ANY_VALUE(header_elapsedGameLoops) / 22.4 AS BIGINT)` via JOIN
    to aggregated `player_history_all`. 22.4 = SC2 "Faster" game-speed loops/sec,
    empirical via `details.gameSpeed` cardinality=1 (W02). Max 6,073s; no outliers.
  - aoestats: `CAST(r.duration / 1_000_000_000 AS BIGINT)` via JOIN to `matches_raw`.
    Raw `duration` is Arrow `duration[ns]` → BIGINT nanoseconds per DuckDB 1.5.1
    (`pre_ingestion.py:271`). 56 outliers (28 corrupted matches) reported.
  - aoe2companion: `CAST(EXTRACT(EPOCH FROM (r.finished - r.started)) AS BIGINT)`
    in `_mhm_base` staging. 142 wall-clock outliers + 358 clock-skew rows reported.
- **Gate +5 split** (R1 post-exec fix): +5a HALTING canary (`max ≤ 1_000_000_000`
  catches nanosecond-unit regression) + +5b REPORT-ONLY (outlier count, no halt).
  Enables data-quality outliers to pass through visibly without masking unit bugs.
- **Gate +6** (aoec-specific HALTING): `finished` NULL fraction ≤ 1%.
- **aoestats `matches_history_minimal` VIEW** — 8-col × 35,629,894 rows (= 2 ×
  17,814,947 matches). UNION ALL pivot from 1-row-per-match (p0/p1 cols) to
  2-rows-per-match. `started_at` via `CAST(started_timestamp AT TIME ZONE 'UTC'
  AS TIMESTAMP)` (TIMESTAMPTZ → canonical TIMESTAMP). Slot-bias gate:
  `AVG(won::INT) = 0.5` exactly (UNION erases upstream team1_wins ≈ 52.27% slot
  asymmetry at output level). 13/13 gates PASS.
- **aoe2companion `matches_history_minimal` TABLE** — 8-col × 61,062,392 rows
  (= 2 × 30,531,196 matches). Self-join on matchId (sc2egset pattern). `started_at`
  pass-through (already TIMESTAMP). Numeric-tail regex `[0-9]+` prefix gate with
  round-trip cast (matchId is INTEGER; variable decimal width). 12/12 gates PASS.
  **DuckDB 1.5.1 workaround**: TABLE (not VIEW) due to self-join-on-VIEW-with-
  window-function InternalException; 3-step materialization via staging tables.
  Documented in schema YAML `object_type_note`.
- Schema YAMLs for both datasets' `matches_history_minimal` with per-dataset
  polymorphic faction warning (aoestats ~50 civ names; aoec ~56 civ names).
- 2 jupytext-paired notebooks (19 cells aoestats, 18 cells aoec) + 4 artifacts
  (JSON + MD each). All SQL literals verbatim in validation JSON `sql_queries`
  (I6). DESCRIBE snapshot captured (R2-WARNING-3 fix inherited from sc2egset).

### Changed
- Both aoe2 datasets' `STEP_STATUS.yaml`: 01_04_03 added and closed to complete.
- Both aoe2 datasets' `PIPELINE_SECTION_STATUS.yaml`: 01_04 flipped in_progress →
  complete (net zero relative to pre-PR state).
- Both `ROADMAP.md`: 01_04_03 step block inserted after 01_04_02.
- Both `research_log.md`: 01_04_03 entry prepended.

### Fixed
- (User-directed single adversarial round per "less ceremony" directive; 0
  BLOCKERs surfaced pre-execution. 3 WARNINGs were documentation gaps caught
  by execution-time gates — all 25 gates PASSED.)

### Removed

## [3.13.0] — 2026-04-18 (PR #152: feat/01-04-03-sc2egset-minimal-history)

### Added
- **New Phase 01 step 01_04_03** — `matches_history_minimal` VIEW for sc2egset
  (pattern-establisher). 8-column player-row-grain projection of
  `matches_flat_clean` (2 rows × 22,209 matches = 44,418 rows). Canonical
  TIMESTAMP temporal dtype via `TRY_CAST(details_timeUTC AS TIMESTAMP)`;
  per-dataset-polymorphic faction vocabulary (`Prot`/`Terr`/`Zerg` 4-char
  stems for sc2egset; aoestats + aoe2companion sibling PRs will ship civ
  names). Cross-dataset-harmonized substrate for Phase 02+ rating-system
  backtesting (Elo, Glicko, Glicko-2, TrueSkill, Aligulac, Bradley–Terry,
  Neural BTL).
- Schema YAML `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml`
  with explicit I3/I5-analog/I6/I7/I8/I9 invariants block, per-dataset
  polymorphic faction warning, concrete `nullable` booleans from DuckDB
  DESCRIBE (R2-WARNING-3 fix).
- Jupytext-paired notebook `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_03_minimal_history_view.{py,ipynb}`
  (18 cells).
- Validation JSON + MD artifacts in `reports/artifacts/01_exploration/04_cleaning/`
  carrying all 8 SQL literals verbatim (I6) and DESCRIBE snapshot.
- ROADMAP.md step block for 01_04_03.
- research_log.md narrative entry for 01_04_03 (Category A) with full gate
  table, cross-dataset contract documentation, and aoestats sibling-PR
  column mapping.
- Planning critique chain `planning/current_plan.critique.{md,v2.md,v3.md}`
  documenting the 3-round pre-execution adversarial cycle (5 BLOCKERs / 7
  WARNINGs → APPROVE_WITH_WARNINGS) plus post-execution R1 APPROVE.

### Changed
- STEP_STATUS.yaml: 01_04_03 added; 01_04_02 still complete.
- PIPELINE_SECTION_STATUS.yaml: 01_04 transitioned in_progress → complete
  (net zero; intermediate in_progress state preserves derivation-chain
  consistency during execution per R1-WARNING-3 fix).

### Fixed
- (Plan-stage adversarial closed 5 pre-execution BLOCKERs; see commit
  message for details.)

### Removed

## [3.12.0] — 2026-04-17 (PR #148: docs/thesis-4.1-data-chapter)

### Added
- **Thesis §4.1 Data chapter fully drafted** in Polish (46.7k chars across §4.1.1 SC2EGSet
  + §4.1.2 AoE2 datasets + §4.1.3 Cross-dataset asymmetry), relocating the corpus
  statistics that Sprint 7 retrospective adversarial had cut from §2.2.5 / §2.3.4
  to their methodologically correct home. All numerical claims traced to Phase 01
  artifacts via a durable 145-line crosswalk (`temp/plan_4.1_crosswalk.md`).
- §4.1.1 SC2EGSet description (~18.5k chars, 5 subsections) covering Bialecki2023
  citation + Zenodo provenance, 22,390 replays / 22,209 true 1v1 decisive corpus
  scale, tournament date range (2016-2022), 28-col matches_flat_clean schema, 3
  event streams (tracker 62M + game 608M + message 52K events), 83.95% MMR=0
  sentinel rate, 51.96% side=0 asymmetry, and narrow-population limitations.
  Includes Tabela 4.1 (CONSORT flow).
- §4.1.2 AoE2 datasets description (~22.5k chars) with §4.1.2.0 dual-corpus framing
  (triple-methodological-validation rationale), §4.1.2.1 aoestats (~10k chars; 17.8M
  matches, 52.27% team=1 asymmetry, schema-evolution columns post-2024-03 patch),
  §4.1.2.2 aoe2companion (~9k chars; 30.5M matches / 61M player-rows, 47.18%
  team=1 asymmetry, BIGINT profile_id), plus §4.1.2 closing forward-ref paragraph.
  Includes Tabela 4.2 (aoestats CONSORT) and Tabela 4.3 (aoec CONSORT).
- §4.1.3 Cross-dataset asymmetry section (~5.7k chars) hosting canonical Tabela 4.4a
  (Skala i akwizycja — 7 rows × 3 corpora) and Tabela 4.4b (Asymetria analityczna —
  13 rows × 3 corpora). Tables are rows-as-dimensions per Q5 LOCKED decision.
- 3 new bibtex entries: `Rubin1976` (Biometrika 63:3 MCAR/MAR/MNAR taxonomy),
  `vanBuuren2018` (Flexible Imputation 2nd ed.), `SchaferGraham2002` (Psychological
  Methods 7:2 MCAR boundary thresholds). Total bibtex: 84 → 87 entries.
- `temp/plan_4.1_crosswalk.md` — durable 145-line artifact-to-claim crosswalk with
  8-column schema (prose_form + artifact_form + normalized_value + path + anchor +
  datatype + hedging_needed + consuming_subsection).

### Changed
- `thesis/WRITING_STATUS.md` — §4.1.1, §4.1.2, §4.1.3 all moved from `BLOCKED`
  (per prior Phase 01 §01_08 / AoE2-roadmap preconditions) to `DRAFTED` (user
  explicitly overrode prior BLOCKED status because Phase 01 §01_04 is mature for
  all 3 datasets). Remaining-BLOCKED count reduced from 11 to 9 sections.
- `thesis/chapters/REVIEW_QUEUE.md` — 3 new Pending entries (§4.1.1 5 [REVIEW]
  flags; §4.1.2 4 [REVIEW] flags; §4.1.3 1 [REVIEW] flag; 8 total Pass-2 queue
  items for this batch).

### Fixed
- **Adversarial cycle discipline:** per user standing directive "after every review,
  run planner-science, apply fixes, then once again adversarial review and so on",
  this PR went through **6 total adversarial rounds** (3 plan-side + 3 execution-side):
  - Plan round 1 verdict REQUIRE_REVISION (3 BLOCKERs + 10 WARNINGs)
  - Plan round 2 verdict APPROVE_WITH_MINOR_FIXES (4 mechanical)
  - Plan round 3 verdict APPROVE_FOR_EXECUTION
  - Execution round 1 verdict REQUIRE_REVISION (4 BLOCKERs)
  - Execution round 2 verdict APPROVE_WITH_MINOR_FIXES (1 residual)
  - Execution round 3 verdict APPROVE_FOR_COMMIT
- Round-1 execution caught fabricated "16,05% rated" + "99,97% rated" numbers not
  present in artifacts — replaced with sentinel rates (83,95% MMR=0; 0,0007% avg_elo=0).
- Round-1 execution caught "n/d" cell in Tabela 4.4b contradicting prose; replaced
  with 47,18%/52,82% aoec asymmetry citation.
- Round-2 execution caught residual "max ~24,85 mln" speculation in Tabela 4.4b;
  cell simplified to "`profile_id` (BIGINT)" matching Pass-2 deferral in prose.

### Removed
- None in this PR.

## [3.11.0] — 2026-04-17 (PR #146: feat/01-04-02-aoe2companion)

### Added
- **aoec 01_04_02 data cleaning execution** (third + final dataset in three-PR
  Option A sequence; sc2egset PR #142 + aoestats PR #144 already merged). Acts on
  all 8 user-locked DS-AOEC cleaning resolutions from the 01_04_01 missingness
  audit. CONSORT: `matches_1v1_clean` 54→48 cols (drop 7: server, scenario,
  modDataset, password, antiquityMode, mod, status; add 1: `rating_was_null`
  BOOLEAN missingness flag); `player_history_all` 20→19 cols (drop status). Row
  counts unchanged (61,062,392 / 264,132,745). All 23 assertion-battery checks
  pass.
- New artifacts: `01_04_02_data_cleaning_execution.{py,ipynb}` (jupytext-paired,
  ~1815 lines), `01_04_02_post_cleaning_validation.{json,md}` with CONSORT block
  + decisions registry + assertion results, NEW `matches_1v1_clean.yaml` schema
  (48 cols + invariants + 9-entry excluded_columns enumeration + provenance.notes
  marker), UPDATED `player_history_all.yaml` (19 cols, status removed).
- **CROSS PR I8 schema YAML notes vocabulary harmonization** (resolves a
  cross-dataset asymmetry deferred from PRs #142, #144, and the aoec 01_04_02
  commit). All 6 view schema YAMLs across the 3 datasets now use prose-format
  per-column `notes:` and carry a 6-entry `provenance_categories` invariant
  enumeration sourced verbatim from `sc2egset/player_history_all.yaml`.
- **Thesis Chapter 1**: §1.3 Pytania badawcze (4 RQs operationalized, ~5.0k
  chars Polish) and §1.4 Zakres i ograniczenia (~4.6k chars Polish) drafted.
- **Thesis Chapter 2 (FULLY DRAFTED)**: §2.1 Gry strategiczne czasu rzeczywistego
  (~12.0k chars), §2.2 StarCraft II (~12.5k post-adversarial), §2.3 Age of
  Empires II (~9.5k post-adversarial), §2.4 Maszynowe metody klasyfikacji
  binarnej (~14.7k), §2.5 Player skill rating systems (~20.9k; Gate 0.5
  PASS_FOR_PRODUCTION_SCALING), §2.6 Metryki ewaluacyjne i porównanie statystyczne
  (~12.8k) — all in Polish academic register.
- **Thesis Chapter 3**: §3.1 Predykcja w sportach tradycyjnych (~7.8k chars),
  §3.2 StarCraft prediction literature (~14.8k), §3.3 MOBA + pozostałe gatunki
  esportowe (~11.4k) drafted in Polish.
- 60 new bibtex entries in `thesis/references.bib` (was 13 → 84) covering RTS/SC2/
  AoE2/MOBA/CS:GO prediction literature, rating systems (Elo, Glicko/Glicko-2,
  TrueSkill, Aligulac, BTL theoretical foundations), classical ML (Hastie ESL,
  Friedman GBM, XGBoost, LightGBM, Goodfellow DL, etc.), statistical comparison
  (Demšar, Wilcoxon, Holm, García & Herrera, Benavoli, Nadeau-Bengio, Dietterich,
  Bouckaert, etc.), and traditional sports prediction (Dixon-Coles, Constantinou,
  Bunker tennis ML).
- `NIGHT_SUMMARY_2026-04-17.md` (autonomous-mode session summary committed for
  morning user review).

### Changed
- `STEP_STATUS.yaml` for aoe2companion: 01_04_02 → complete.
- `PIPELINE_SECTION_STATUS.yaml` for aoe2companion: 01_04 → complete (closes
  Pipeline Section per derivation rule; `PHASE_STATUS.yaml` unchanged — Phase 01
  stays in_progress because 01_05 + 01_06 remain not_started for all 3 datasets).
- `ROADMAP.md` for aoe2companion: new `### Step 01_04_02` block appended.
- `research_log.md` for aoe2companion: 2026-04-17 [01_04_02] entry with CONSORT
  table + 8 DS resolutions + Reconciliation notes (country rate 13.37% → 2.25%
  authoritative; difficulty correctly RETAIN_AS_IS not constant).
- 8 thesis sections moved from `DRAFTABLE` (or `BLOCKED` for §2.3) to `DRAFTED`
  in `thesis/WRITING_STATUS.md`. 10 sections enqueued in
  `thesis/chapters/REVIEW_QUEUE.md` for Pass 2 (Claude Chat) review with 30
  outstanding `[REVIEW]` flags catalogued.

### Fixed
- Buro2003 bibtex URL corrected (`IJCAI03.pdf` → `RTS-ijcai03.pdf`) — caught by
  retrospective adversarial review of Sprint 7.
- Post-adversarial scope-discipline revision of §2.1 + §2.2 + §2.3 (commit
  `1492d90`): §2.2.5 "Korpus SC2EGSet — krótkie umiejscowienie" subsection
  deleted (data-chapter content); §2.3.4 trimmed from 3.7k → 500 chars (corpus
  numerics deferred to §4.1.2 staging); §2.3.3 first paragraph rewritten (player
  roster + commentator list + Red Bull Wololo Londinium tournament narrative
  removed); K-factor paragraph collapsed to forward-reference to §2.5.4.

### Removed
- Two DuckDB workarounds applied in `01_04_02_data_cleaning_execution.py` (both
  documented in DDL comment headers): multi-column `SUM(CASE WHEN ...)`
  aggregation on the `matches_1v1_clean` view replaced with individual per-column
  `COUNT(*) WHERE col IS NULL` queries (mathematically equivalent); `SELECT *
  EXCLUDE (rn)` in subqueries replaced with explicit column enumeration.

## [3.10.3] — 2026-04-17 (PR #TBD: fix/01-04-null-audit)

### Added
- Consolidated 01_04_01 missingness audit across all 3 datasets (sc2egset, aoestats,
  aoe2companion) with two coordinated census passes (SQL NULL + sentinel) plus runtime
  constants detection feeding a 17-column missingness ledger per VIEW.
- New artifact files per dataset: `01_04_01_missingness_ledger.csv` and
  `01_04_01_missingness_ledger.json` (full-coverage Option B — every VIEW column
  gets a row; zero-missingness rows tagged RETAIN_AS_IS / mechanism=N/A;
  constants tagged DROP_COLUMN / mechanism=N/A; identity columns routed via B5
  branch with n_distinct=null per W6 budget skip).
- 5-value recommendation enum (DROP_COLUMN, FLAG_FOR_IMPUTATION, RETAIN_AS_IS,
  EXCLUDE_TARGET_NULL_ROWS, CONVERT_SENTINEL_TO_NULL) with 4-tier override priority
  (identity → constants → F1 zero-missingness → spec/fallback → target post-step).
- `is_primary_feature` and `carries_semantic_content` boolean columns surfaced
  to ledger CSV/JSON for downstream Phase 02 consumption (W8).
- Per-dataset `decisions_surfaced` blocks in ROADMAP.md and artifact JSON/MD
  surfacing open questions for 01_04_02+ (DS-SC2-01..10, DS-AOESTATS-01..08,
  DS-AOEC-01..08). B6 deferral: CONVERT_SENTINEL_TO_NULL recommendations are
  marked non-binding for sentinel-with-semantic-content cases — downstream
  chooses without prejudice from the audit.
- Methodology citations block in each dataset's ROADMAP entry (Rubin 1976,
  Little & Rubin 2019, van Buuren 2018, Sambasivan 2021, Schafer & Graham 2002,
  Davis 2024, sklearn v1.8 MissingIndicator, CRISP-DM, Manual 01 §3 + §4).

### Changed
- All 3 datasets now use uniform DB connection convention `con = db.con` then
  `con.execute(...)` (W4):
  - sc2egset: 58 existing `con.con.execute(...)` calls converted to
    `con.execute(...)` via two-step rename (`con = get_notebook_db(...)` →
    `db = get_notebook_db(...)` + `con = db.con`).
  - aoestats: `con = db._con` (private attribute) → `con = db.con` (public
    @property); existing `con.execute(...)` call sites unchanged.
  - aoe2companion: already conformant.
- ROADMAP.md 01_04_01 step blocks replaced per dataset with new YAML covering
  `methodology_citations`, `decisions_surfaced`, `outputs.data_artifacts`
  (including new ledger files), and updated gate condition.
- Description-only cleanup of plan-code annotations (`R02`/`R04`/`R05`/`R07`/
  `W03`/`W04`) from
  `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml`
  per `feedback_no_plan_codes_in_docs` (N1; no DDL/type/nullability changes).

### Fixed
- F1: aoestats `_consolidate_ledger` no longer carries stale spec justification
  text when runtime n_total_missing=0; mechanism overridden to N/A and
  recommendation to RETAIN_AS_IS regardless of spec contents.
- F2: aoestats removed legacy `col != "winner"` exception that hardcoded
  winner→MAR even when winner had 0 NULLs.
- B5: identity-column branch added FIRST in `_consolidate_ledger` if/elif chain
  to avoid pandas dtype-dependent NA propagation when `n_distinct=None` (W6 skip).
- W3 (post-execution): aoec `_IDENTITY_COLS_M1` extended to include `profileId`
  to dodge DuckDB COUNT(DISTINCT) artifact returning 0 on window-function VIEW.

### Removed
- N/A (audit is additive on existing artifacts; no VIEW DDL changes; no schema
  YAML semantic changes; no STEP_STATUS bumps).

### Added (NOTE-3 + W2 refactor)
- `src/rts_predict/common/missingness_audit.py` — shared missingness-audit
  helpers extracted from 3 inline notebook definitions (`_build_sentinel_predicate`,
  `_sentinel_census`, `_detect_constants`, `_recommend`, `_consolidate_ledger`);
  new `build_audit_views_block` helper for canonical `views.<view_name>:` JSON shape;
  100% unit-test coverage at `tests/rts_predict/common/test_missingness_audit.py`.

### Changed (NOTE-3 + W2 refactor)
- All 3 cleaning notebooks (`01_04_01_data_cleaning.py`) now import helpers from
  `rts_predict.common.missingness_audit` instead of defining them inline. Inline
  `missingness_audit.views` JSON block standardized to canonical
  `views.<view_name>: {total_rows, columns_audited, ledger}` shape across all 3
  datasets (W2 fix); aoec `_recommend` body upgraded from contracted to canonical
  (recommendation codes unchanged, free-text `recommendation_justification` for
  affected rows now carries the full B6 deferral sentence and expanded §3.1
  references). **aoec inline `missingness_audit.<view>.n_cols` field renamed to
  `views.<view>.columns_audited` as part of W2 canonicalization** (per WARNING-2
  critique fix — explicit because downstream consumers referencing `n_cols` would
  otherwise break silently). aoestats `missingness_audit.ledger_<view_name>` flat
  keys replaced by canonical `views.<view_name>:` shape (W2 fix; no data change).

## [3.10.2] — 2026-04-16 (PR #TBD: fix/01-04-aoestats-ingame-cols)

### Fixed
- aoestats `matches_1v1_clean`: removed 8 IN-GAME columns (`p0_opening`, `p1_opening`,
  `p0_feudal_age_uptime`, `p1_feudal_age_uptime`, `p0_castle_age_uptime`, `p1_castle_age_uptime`,
  `p0_imperial_age_uptime`, `p1_imperial_age_uptime`) that were classified IN-GAME in 01_03_01
  profiling but included in the prediction target VIEW without I3 assertion coverage.
  Extended `forbidden` set and added combined `information_schema` assertion covering both
  POST-GAME and IN-GAME I3 violations.
- Added slot-assignment asymmetry warning comment to aoestats `matches_1v1_clean` VIEW DDL
  (team=1 wins ~52.27%; Phase 02 must randomise p0/p1 slot before using as focal/opponent pairs).

## [3.10.1] — 2026-04-16 (PR #TBD: fix/01-04-i3-violations)

### Fixed
- B1: aoe2companion `matches_1v1_clean` — removed `d.finished` and `d.ratingDiff` (POST-GAME I3 violations).
  Extended V2 leakage check to cover `matches_1v1_clean` (previously only `player_history_all`).
- B2: aoestats `matches_1v1_clean` — removed `m.duration`, `m.irl_duration`,
  `p0_match_rating_diff`, `p1_match_rating_diff` (POST-GAME I3 violations).
  aoestats `player_history_all` — removed `p.match_rating_diff` (POST-GAME I3 violation).
  Added `match_rating_diff` to `forbidden_hist` and explicit `information_schema` assertion.
- B3: research_log.md — corrected aoe2companion 01_04_00 entry: 1v1-scoped side=0 has 29,921,254 rows
  (win_pct 47.18%), side=1 has 29,920,914 rows (win_pct 52.81%); prior entry incorrectly stated
  "only side=1 rows appear".
- W1: sc2egset `player_history_all` — removed duplicate `max_players_check` alias of `gd_maxPlayers`.
- W2: aoestats `player_history_all.yaml` — removed `match_rating_diff` column entry; updated I3 invariant.
- W3: Added explicit `information_schema.columns` assertions for POST-GAME absence in `matches_1v1_clean`
  (all three datasets).

### Removed
- aoestats `player_history_all.yaml`: `match_rating_diff` column (POST-GAME I3 violation, now excluded from VIEW).
- sc2egset `player_history_all.yaml`: `max_players_check` column (duplicate of `gd_maxPlayers`).

## [3.10.0] — 2026-04-16 (PR #TBD: feat/data-cleaning-01-04)

### Added
- Step 01_04_00 — Source Normalisation to Canonical Long Skeleton (all three datasets):
  `matches_long_raw` VIEW per dataset, 10-column unified schema, one row per player per match.
  Includes I5 symmetry audit; documents ~5pp slot asymmetry in both AoE2 datasets.
- Step 01_04_01 — Data Cleaning (all three datasets):
  `matches_1v1_clean` and `player_history_all` VIEWs per dataset.
  Prediction-scope vs feature-scope separation: 1v1 target scope in `matches_1v1_clean`,
  full-game-history feature source in `player_history_all`.
- Schema YAMLs for all new VIEWs (`matches_long_raw.yaml`, `player_history_all.yaml`).
- Planning artifacts, critiques, and research log entries for 01_04_00 and 01_04_01.
- `temp/follow_up_01_04.md` documenting open I3 violations to fix in next session.

## [3.9.1] — 2026-04-16 (PR #TBD: chore/sc2egset-schema-descriptions)

### Changed
- All schema YAML column descriptions populated across all three datasets:
  sc2egset (41 cols from s2protocol), aoe2companion (92 cols from API research),
  aoestats (38 cols manually). Zero "TODO: fill" entries remain.
  Descriptions are semantic only — no profiling statistics (I7 compliant).

## [3.9.0] — 2026-04-16 (PR #TBD: feat/sc2egset-01-03-04-event-profiling)

### Added
- **01_03_04 Event Table Profiling** for sc2egset — deep profiling of tracker_events_raw
  (62M rows, 10 types, PlayerStats every 160 loops, 232 unit types), game_events_raw
  (608M rows, 23 types, CameraUpdate 63.67%), message_events_raw (52K rows, LOW_UTILITY)
- event_data JSON schema samples for 7 event types (5 tracker, 2 game)
- [CROSS] research log entry for in-game data asymmetry (I8)

## [3.8.1] — 2026-04-16 (PR #TBD: fix/stale-research-log-refs)

### Fixed
- aoe2companion research log: 6 stale "rating AMBIGUOUS / deferred to 01_04" references
  updated with strikethrough and cross-reference to 01_03_03 PRE-GAME resolution

## [3.8.0] — 2026-04-16 (PR #TBD: feat/table-utility-assessment)

### Added
- **01_03_02 True 1v1 Match Identification** for all three datasets — structural
  player-count verification vs label-based filtering, true 1v1 population sizing
- **01_03_03 Table Utility Assessment** for all three datasets — empirical
  investigation of which raw tables serve the prediction pipeline vs stale snapshots
- Cross-dataset summary table in all three research logs

### Changed
- aoe2companion `matches_raw.rating` reclassified from AMBIGUOUS to **PRE-GAME**
  (99.8% exact match with ratings_raw pre-match entries). This resolves the single
  most important open question from 01_02_04.
- aoe2companion `ratings_raw` downgraded to CONDITIONALLY USABLE — leaderboard_id=6
  (rm_1v1) has zero rows; pre-game rating for rm_1v1 must come from matches_raw.rating

### Fixed
- aoestats 01_03_02 match type breakdown PNG moved to plots/ subdirectory

## [3.7.3] — 2026-04-16 (PR #TBD: fix/aoe2-01-03-01-profile-gaps)

### Fixed
- aoestats 01_03_01 I3 table: 30 → 32 rows (dict key collision on filename/game_id)
- aoe2companion 01_03_01: temporal coverage added (2020-07 to 2026-04, 70 months)
- aoe2companion 01_03_01: near-constant stratified into 11 genuinely uninformative +
  39 low-cardinality categorical (TARGET rule keeps `won` in categorical)
- aoe2companion 01_03_01: cross_table_notes for 7 dead profiles_raw columns
- sc2egset KDE omission justification restored in notebook source (PR2 overwrite)
- aoe2companion research log: 6 remaining rating "Phase 02" references → 01_04
- All 01_03_01 PNGs moved to `plots/` subdirectory (matches 02_eda convention)

## [3.7.2] — 2026-04-16 (PR #TBD: fix/sc2egset-01-03-01-profile-gaps)

### Fixed
- sc2egset 01_03_01 sentinel summary expanded from 2 to 7 patterns (APM=0, MMR<0,
  map_size=0, handicap=0, selectedRace="") with runtime SQL counts (I7)
- sc2egset 01_03_01 temporal coverage added (2016-01 to 2024-12, 76 months, 32 gaps)
- sc2egset 01_03_01 startLocX/startLocY type and range verification added
- sc2egset stale elapsed_game_loops reclassification claim fixed in notebook source

## [3.7.1] — 2026-04-16 (PR #TBD: fix/retroactive-tracking-and-logs)

### Fixed
- PIPELINE_SECTION_STATUS.yaml stale for all 3 datasets (01_02 and 01_03 now `complete`)
- aoe2companion research log 01_03_01 duplicate contradiction (was "No duplicates",
  profile JSON shows 3.6M groups); added metric reconciliation note
- aoestats `mirror` removed from safe pre-game features (reclassified POST-GAME in 01_03_01)
- aoe2companion rating deferral destination standardized to 01_04 (was inconsistently "Phase 02")
- sc2egset isInClan open question cross-referenced with 01_02_06 chi-square result
- KDE omission documented with Tukey (1977) justification in all 3 dataset profile MDs

## [3.7.0] — 2026-04-16 (PR #129: feat/census-pass3)

### Added
- **01_02_05 Univariate Visualizations** for all three datasets (aoe2companion 17 plots,
  aoestats 15 plots, sc2egset 14 plots) — dedicated visualization notebooks reading from
  01_02_04 census JSON artifacts
- **01_02_06 Bivariate EDA** for all three datasets — conditional distributions by outcome,
  Mann-Whitney U tests with rank-biserial effect sizes, Spearman correlation matrices,
  leakage verification (aoestats match_rating_diff confirmed PRE-GAME)
- **01_02_07 Multivariate EDA** for all three datasets — cluster-ordered Spearman heatmaps,
  PCA scree/biplot where viable (aoestats 5 pre-game numerics), degenerate-case fallbacks
  (aoe2companion 0 viable pre-game numerics, sc2egset 1 pre-game numeric)
- **01_03_01 Systematic Data Profiling** for all three datasets — column-level profiling,
  dataset-level profiling, critical detection (dead/constant/near-constant), QQ plots,
  ECDFs, I3 temporal classification for all columns, sentinel analysis
- Retroactive fixes plan (`planning/fixes_and_next_steps.md`) with adversarial-reviewed
  PR1/PR2/PR3 plans for tracking, research log, and notebook corrections
- `temp/01_02_roadmap_finalization.md` — working document for 01_02 pipeline section closure

### Changed
- ROADMAP.md updated for all three datasets with 01_02_05 through 01_03_01 step definitions
- STEP_STATUS.yaml updated for all three datasets (01_02_05 through 01_03_01 complete)
- 01_02_04 census notebooks updated with pass-3 improvements (sc2egset field classification
  corrections, additional census sections)
- 01_02_05 visualization notebooks revised per adversarial critique findings
- Existing 01_02_04 plot artifacts moved to `plots/` subdirectory for consistency

### Fixed
- sc2egset `elapsed_game_loops` I3 classification corrected from IN-GAME to POST-GAME
- aoe2companion 01_02_05 won_consistency data extraction bug (single-element list structure)
- aoestats duration unit handling (BIGINT nanoseconds → seconds conversion)
- Various plot designs revised per adversarial critique (bin widths, sentinel handling,
  dual-panel layouts, I7 compliance)

## [3.6.2] — 2026-04-14 (PR #TBD: chore/raw-schema-docs)

### Added
- `docs/templates/duckdb_schema_template.yaml` — canonical template for `*_raw` schema YAMLs;
  enforces `describe_artifact` cross-reference, verbatim DESCRIBE types, and column-count gate condition
- `01_02_03_raw_schema_describe` notebooks for sc2egset, aoe2companion, aoestats — run DESCRIBE on
  every `*_raw` table/view and save results to artifacts
- 13 `*_raw` schema YAML files across all three datasets, sourced verbatim from 01_02_03 DESCRIBE artifacts:
  sc2egset (6), aoe2companion (4), aoestats (3)

## [3.6.1] — 2026-04-14 (PR #TBD: chore/sandbox-logging-timestamp)

### Added
- `notebook_utils.py`: `setup_notebook_logging()` — centralised logging setup;
  configures root logger at INFO with `HH:MM:SS` timestamp format, returns a
  named `logging.Logger`; collapses two-line boilerplate to one call in all notebooks
- `test_notebook_utils.py`: tests for `setup_notebook_logging()` (default name,
  custom name, root-logger level, idempotency)
- `aoe2companion/01_02_01`: section 8 (Q1–Q4) won=NULL root-cause investigation —
  `parquet_schema()` type scan across all 2,073 files, per-type value census without
  type promotion, type-promotion NULL injection test, per-file NULL distribution;
  extends artifact with `won_null_root_cause` key (H1 rejected: single BOOLEAN type;
  H2 supported: 12,985,561 genuine NULLs spanning full 5.7-year corpus history)
- `sc2egset/research_log.md`: 01_02_02 DuckDB ingestion findings entry
- `aoe2companion/research_log.md`: won-NULL root-cause findings entry; corrected
  01_02_01 entry (was describing full ingestion; artifact shows pre-ingestion
  investigation)

### Changed
- All 12 sandbox notebooks (`sc2egset`, `aoe2companion`, `aoestats`): two-line
  `logging.basicConfig` + `logging.getLogger` boilerplate replaced with single
  `setup_notebook_logging()` call; all notebook output now shows `HH:MM:SS` timestamps
- All three 01_02_01 notebooks: artifact writing restored (code had been lost when
  notebooks were reworked from full-ingestion to pre-ingestion format)
- `docs/templates/notebook_template.yaml`: updated logging setup section

### Fixed
- `test_notebook_utils.py`: removed unused `import logging` inside
  `test_setup_notebook_logging_default_name` that caused ruff E401 failure

## [3.6.0] — 2026-04-14 (PR #TBD: feat/sc2egset-event-views)

### Added
- `sc2egset/ingestion.py`: `load_event_views` — registers event Parquet
  subdirectories (`gameEvents/`, `trackerEvents/`, `messageEvents/`) as
  DuckDB views (`game_events_raw`, `tracker_events_raw`, `message_events_raw`);
  views not tables so no data is duplicated; `EVENT_SUBDIR_TO_VIEW` exported
  for use in notebooks and tests
- Notebook `01_02_02`: Sections 6–7 — event view registration and health checks
  (NULL rates, filename coverage vs `replays_meta_raw`, top-10 `evtTypeName`
  distribution per view, all SQL inlined for Invariant I6)
- Artifact `01_02_02_duckdb_ingestion.json/.md` now includes
  `event_extraction_counts`, `event_views_created`, and `event_views_health`

### Changed
- Notebook `01_02_02`: Section 5 comment updated to reflect production status
  (no longer "optional/deferred"); Section 6 renamed to Section 8

## [3.5.1] — 2026-04-13 (PR #TBD: fix/sc2egset-single-pass-event-extraction)

### Changed
- `sc2egset/ingestion.py`: refactored `extract_events_to_parquet` to single-pass
  (read each JSON file once, route events to all three type accumulators per batch)
  reducing I/O by ~3× on the full 22,390-file corpus

## [3.5.0] — 2026-04-14 (PR #TBD: chore/aoe2companion-ingestion-fix)

### Changed
- `aoe2companion/ingestion.py`: renamed all tables from `raw_*` to `*_raw` suffix
  (`matches_raw`, `ratings_raw`, `leaderboards_raw`, `profiles_raw`) and functions
  from `load_raw_*` to `load_*_raw`, consistent with Invariant I10
- Added `binary_as_string=true` to all three Parquet reads (required for
  unannotated BYTE_ARRAY columns confirmed in Step 01_02_01)
- Fixed notebook `01_02_02`: DtypeDecision corrected to `explicit` strategy,
  NULL queries fixed (`matchId` not `match_id`), artifact now inlines SQL (I6),
  adds `won` NULL count and I10 filename assertions
- Added `HH:MM:SS` timestamp to `logging.basicConfig` across all 12 sandbox notebooks

### Changed

### Fixed

### Removed

## [3.4.0] — 2026-04-13 (PR #TBD: feat/sc2-phase01-duckdb-ingestion)

### Added
- Phase 01 / Step 01_02_02: DuckDB ingestion for sc2egset — three-stream strategy
  materialising `replays_meta_raw` (22,390 rows), `replay_players_raw` (44,817 rows),
  and `map_aliases_raw` (104,160 rows) in `data/db/db.duckdb`
- Invariant I10 in `.claude/scientific-invariants.md`: every `*_raw` table and Parquet
  event file must carry a `filename` column relative to `raw_dir`; absolute paths and
  bare basenames both forbidden
- `ingestion.py`: `load_replays_meta_raw`, `load_replay_players_raw`,
  `load_map_aliases_raw`, `load_all_raw_tables`, `extract_events_to_parquet`
  with per-tournament batch loading for replays_meta to avoid OOM
- All three dataset ROADMAPs updated to `*_raw` suffix naming convention (I10)
- Draft of thesis Chapter 1 Introduction (Polish)

## [3.3.0] — 2026-04-13 (PR #TBD: chore/dag-decommission-and-cleanup)

### Changed
- Decommissioned DAG + spec materialization infrastructure; executors now read
  `planning/current_plan.md` directly — no `DAG.yaml`, no `spec_NN_*.md` files
- Removed `/dag` and `/materialize_plan` slash commands
- Removed `docs/templates/dag_template.yaml`, `dag_status_template.yaml`, `spec_template.md`
- Simplified `planning/README.md`, `planning/INDEX.md` to reflect two-artifact lifecycle
- Updated all planner and executor agent definitions to remove DAG/spec requirements
- Removed DAG/Job/Task Group/Task/parallel strategy terms from `docs/TAXONOMY.md`
- Simplified `planner_output_contract.md` and `plan_template.md` (no Suggested Execution Graph)

### Removed
- `planning/specs/spec_*.md` pattern — specs no longer produced or consumed
- `planning/dags/DAG.yaml` as an execution artifact (stubbed to `# No active DAG`)

## [3.2.1] — 2026-04-12 (PR #TBD: chore/dag-token-economy)

### Changed
- DAG intermediate review gates are now optional (omitted by default);
  `final_review` is the standard quality gate
- DAG task schema: added `model` field (haiku/sonnet/opus) for per-task
  model dispatch; orchestrator passes to Agent tool when present
- Spec template: added `model` and `datasets` optional frontmatter fields
- Plan template: added Spec Design Rules section (self-contained specs,
  consolidation by read_scope, parameterized dataset tables, no model
  mixing, 15-file cap)
- `/materialize_plan` command: self-contained spec enforcement and
  consolidation rules
- `/dag` command: conditional review gate dispatch, model override dispatch
- CLAUDE.md dispatch rules: conditional review gates, final reviewer
  by category (reviewer-adversarial for Cat A/F, reviewer for Cat B/C/D/E)
- TAXONOMY.md: Task Group definition updated (review gates MAY run if
  configured); Task definition updated (model field)
- Agent manual: review gates opt-in, model assignment guidance
- Test DAGs: review gates removed, model fields added

## [3.2.0] — 2026-04-12 (PR #117: feat/rerun-01-01-01)

### Added
- Scientific Invariant #9 (research pipeline discipline) codified in
  `.claude/scientific-invariants.md`: step conclusions may only reference
  own-step artifacts, prior completed-step artifacts, and external source docs
- `docs/templates/dataset_reports_readme_template.yaml` — new template for
  dataset reports READMEs with per-section Source annotations and Invariant #9
  compliance notes
- `docs/templates/research_log_entry_template.yaml` — extended with `step_scope`
  field and Invariant #9 annotation on the `findings` section
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/README.md` — new reports
  README populated from 01_01_01 artifacts

### Changed
- Step 01_01_01 file inventory notebooks re-run (fresh kernel) for sc2egset,
  aoe2companion, and aoestats; JSON and Markdown artifacts regenerated
- ROADMAs and reports/READMEs for all three datasets populated with artifact-
  derived counts; research logs stripped of context leaks and rewritten per
  Invariant #9 (filesystem-scoped findings only)
- Root `reports/research_log.md` CROSS entry for 01_01_01 updated
- SC2-specific "tournament" vocabulary replaced with neutral cross-game terms
  across all shared methodology files (`.claude/scientific-invariants.md`,
  `.claude/ml-protocol.md`, `executor.md`, `reviewer-adversarial.md`); split
  strategy renamed to "per-player chronological hold-out" with per-dataset
  hold-out unit deferred to each dataset's ROADMAP.md Phase 03
- sc2egset 01_01_01 notebook: JSON artifact keys renamed
  (`num_tournament_dirs` → `num_top_level_dirs`,
  `tournaments_missing_data_dir` → `dirs_missing_data_subdir`,
  `tournaments` → `top_level_dirs`); all "tournament" prose, comments, variable
  names, and artifact output replaced with neutral structural terms
- Agent files updated to reference 9 invariants (was 8); `reviewer-adversarial`
  output template extended with Invariant #9 compliance row
- `.claude/settings.json` raw/ deny rule tightened from `data/raw/**` to
  `data/raw/**/!(README.md)` to allow README writes while protecting data files

### Fixed
- sc2egset research log: semantic label violations ("tournament", "replay" as
  content-level descriptors) replaced with filesystem-neutral phrasing
- aoestats research log: "weekly" cadence label removed; "documented in ROADMAP"
  cross-reference removed (beyond filesystem step scope)
- aoestats `reports/README.md`: missing-file provenance note restored with
  explicit `_download_manifest.json` source annotation per Invariant #9

## [3.1.3] — 2026-04-12 (PR #116: chore/thesis-prep)

### Changed
- `writer-thesis` agent: added WebFetch/WebSearch tools, Polish language
  instruction, `.claude/author-style-brief-pl.md` in Read First, argumentative
  prose rules ("every method choice must present alternatives considered")
- `reviewer-adversarial` agent: added voice audit for Category F against
  Polish style brief, style brief added to Required Reading
- `planner-science` agent: added Category F spec requirements (must-justify,
  must-cite, must-contrast lists per section)
- `reviewer-deep` agent: added cross-chapter voice consistency check against
  Polish style brief for Category F
- `thesis/WRITING_STATUS.md`: 16 sections moved from SKELETON to DRAFTABLE
  (13 fully draftable literature-based + 3 with revision notes)

## [3.1.2] — 2026-04-12 (PR #115: chore/agent-efficiency)

### Added
- `scripts/hooks/check_status_chain.py` — pre-commit hook validating Tier 7
  consistency (STEP_STATUS → PIPELINE_SECTION_STATUS → PHASE_STATUS); uses
  contradiction-only logic to avoid false positives on partially-filled status files
- `scripts/hooks/check_rule_triggers.py` — pre-commit hook validating that all
  `.claude/rules/` path globs match at least one real file; catches silent rule
  death after path restructures; `EXPECTED_EMPTY` set for forward-declared globs
- Both hooks registered in `.pre-commit-config.yaml`

### Changed
- `CLAUDE.md` — session-start reads now category-gated: Cat A/D-data/F reads
  PHASE_STATUS + SI; Cat B/C/E skips (rules auto-load on file touch)
- `CLAUDE.md` — context injection protocol added to dispatch rules: every
  subagent prompt must include `Category/Branch/Dataset/Phase` header so agents
  skip redundant independent reads of PHASE_STATUS and ROADMAP
- `CLAUDE.md` — final review routing by category: reviewer-adversarial for Cat A,
  reviewer-deep for Cat B/D, reviewer (Sonnet) for Cat C/E
- `reviewer-deep.md` — Required reading is now category-gated: 5 always-reads for
  all categories; 6 additional science reads only for Cat A/D-data/F; saves ~18s
  startup latency per Cat B/C review
- Package structure: `src/rts_predict/<game>/data/<dataset>/` and
  `src/rts_predict/<game>/reports/<dataset>/` replaced by
  `src/rts_predict/games/<game>/datasets/<dataset>/{data,reports}` (PR #114)
- All imports updated (68 statements across ~18 files) to new `rts_predict.games.*`
  namespace (PR #114)
- Both `config.py` files rewritten with new `__file__`-relative path derivation
  (PR #114)
- `.gitignore`, `.claude/settings.json`, 6 shell scripts, 3 sandbox notebooks,
  ~42 documentation files updated for new path layout (PR #114)

### Fixed
- `executor.md` — PHASE_STATUS path and config.py path updated to new
  `games/<game>/datasets/<dataset>/` layout (missed by T08 in PR #114)
- `reviewer-deep.md` — 3 stale paths updated (PHASE_STATUS, data layout,
  thesis artifact reports); missed by T08 in PR #114
- `sql-data.md` — trigger glob deepened from `src/rts_predict/*/data/**/*.py`
  to `src/rts_predict/games/*/datasets/*/data/**/*.py`; rule was silently
  dead post-restructure

### Removed
- Colocated test directories inside `src/` (were empty): `src/rts_predict/sc2/data/tests/`,
  `src/rts_predict/aoe2/data/aoestats/tests/`, `src/rts_predict/common/tests/`
  (PR #114)

## [3.1.1] — 2026-04-12 (PR #113: chore/token-economy-indexing)

### Added

- 9 directory `README.md` files (routing documents for key subdirectories)
- `docs/INDEX.md` — centralized directory map and routing hub
- `scripts/hooks/check_planning_drift.py` — pre-commit hook for planning artifact validation
- `tests/infrastructure/test_check_planning_drift.py` — 23 initial tests + 4 follow-up (`test_main_integration_clean`, `test_main_integration_errors`, `test_absolute_spec_file_path`, `test_legacy_heuristic_false_positive`)

### Changed

- `CLAUDE.md` trimmed (~16 lines removed, dispatch rules preserved)
- `ARCHITECTURE.md` trimmed (~18 lines, pointers replace duplication)
- `.claude/agents/executor.md` trimmed (~40 lines, data layout + notebook workflow replaced with pointers)
- `src/rts_predict/aoe2/README.md` — added 4 per-dataset report/artifact path constants
- `docs/TAXONOMY.md` — added Strategy A/B parallel execution definitions; `docs/agents/AGENT_MANUAL.md` and `planning/README.md` updated with formal terms

### Fixed

- `scripts/hooks/check_planning_drift.py` — absolute `spec_file` path handling in orphan detection

### Removed

- `docs/ml_experiment_phases/PHASES.md` (derivative of canonical `docs/PHASES.md`)
- `docs/ml_experiment_phases/PIPELINE_SECTIONS.md` (derivative)
- `scripts/hooks/check_phases_drift.py` (no longer needed)

## [3.1.0] — 2026-04-12 (PR #111: chore/research-log-split)

### Added
- 3 per-dataset `research_log.md` files (sc2egset, aoe2companion, aoestats) with migrated Step 01_01_01 findings

### Changed
- `reports/research_log.md` rewritten as index + CROSS entries
- ~25 files updated to reference per-dataset logs instead of unified log

## [3.0.5] — 2026-04-12 (PR #110: chore/plan-template-rewrite)

### Added
- `.claude/commands/dag.md` — `/dag` skill for executing DAGs with codified dispatch protocol (pointer prompts, per-job orchestration, review gates)
- `tests/dags/` — smoke test fixtures for DAG execution (single-job and multi-job canary tests with documented results)
- `CLAUDE.md` — Critical Rule: orchestrator must not read specs/plan when dispatching executors during DAG execution
- `CLAUDE.md` — Dispatch rules section documenting executor, review gate, and final review dispatch conventions
- `docs/templates/dag_template.yaml` — documented multi-agent support (non-executor agents valid in `agent:` field)

### Changed
- `docs/templates/plan_template.md` — rewritten with DAG-compatible, per-task structure covering Categories A–F, gate conditions, and agent assignments
- `docs/templates/plan_critique_template.md` — rewritten to cover all 8 scientific invariants, citation requirements, temporal discipline checks, and to be produced by reviewer-adversarial
- `docs/templates/planner_output_contract.md` — rewritten as agent-agnostic, plan-only output contract with Category A–F sections; all critiques now routed to reviewer-adversarial
- `planning/README.md` — updated to include critique step in the plan lifecycle and purge rule for `current_plan.critique.md`
- `.claude/agents/planner-science.md` — updated to reference `planner_output_contract.md` and flag critique requirement
- `.claude/agents/planner.md` — updated to reference `planner_output_contract.md` and critique-flagging rules for Category B/D
- `.claude/commands/materialize_plan.md` — updated to enforce critique pre-flight check for Category A and F plans
- `.claude/agents/executor.md` — updated "Read first" section with explicit spec-first dispatch protocol (echo task_id, file_scope, verification count before execution)

## [3.0.4] — 2026-04-11 (PR #109: chore/session-audit-dashboard)

### Added
- `scripts/session_audit.py` — on-demand session audit dashboard (token usage, PR efficiency, subagent analysis)
- `.claude/commands/materialize_plan.md` — `/materialize_plan` slash command enforcing the materialization flow
- `scripts/hooks/check_phases_drift.py` — pre-commit hook that detects drift between `docs/PHASES.md` and `docs/ml_experiment_phases/PHASES.md` by comparing phase number + name pairs; fires only when either file is staged
- `.pre-commit-config.yaml`: `phases-drift` hook entry wired to `check_phases_drift.py`

### Changed
- `scripts/hooks/log-subagent.sh`: audit log moved to `~/Projects/tp-claude-logs/agent-audit.log`, ephemeral state to `/tmp/tp-claude-logs/`, added `project=` field
- `scripts/hooks/log-bash.sh`: audit log moved from `~/.claude/bash-audit.log` to `~/Projects/tp-claude-logs/bash-audit.log`, added `project=` field
- `scripts/hooks/README.md`: updated all path references and format examples
- `docs/templates/dag_template.yaml`: renamed `spec_ref` to `plan_ref`, clarified `spec_file` comment
- `planning/README.md`: expanded materialization to 5 sub-steps (purge → specs → DAG → INDEX → commit)
- `planning/specs/README.md`: added 4 rules (start at 01, purge before create, one per task, derived not invented)
- `.claude/agents/planner.md` and `planner-science.md`: DAG requirement now includes `spec_file` paths
- `CLAUDE.md`: inlined 5-step materialization sequence
- `docs/templates/research_log_template.yaml`: normalized `ordering:` field to `value:` + `required:` pattern; updated `markdown_rendering` to point to `docs/research/RESEARCH_LOG_ENTRY.md`
- `planning/current_plan.md`: added `scripts/hooks/log-subagent.sh` to T10 file_scope (was modified in execution but missing from plan manifest)
- `CHANGELOG.md` [3.0.3]: added `.gitignore` removal to `### Removed` (was undocumented)
- `src/rts_predict/aoe2/reports/ROADMAP.md`: removed bullet #3 (Pre-Phase-01 DuckDB row count claim) from Dataset Strategy planning indicators
- `src/rts_predict/aoe2/reports/aoe2companion/ROADMAP.md`: replaced Source data section — removed provenance callout, DuckDB row count table, snapshot table warning, and sparse rating regime note; replaced with file-inventory-derived table (Step 01_01_01) and forward reference to schema discovery steps
- `src/rts_predict/aoe2/reports/aoestats/ROADMAP.md`: replaced Source data section — removed provenance callout, DuckDB row count table, and schema drift section; replaced with file-inventory-derived table and forward reference to schema discovery steps
- `src/rts_predict/aoe2/reports/aoe2companion/README.md`: removed pre-phase provenance note, T_ingestion row count section, snapshot table section, sparse rating regime section, and dtype strategy section (all DuckDB-derived); acquisition date preserved under Acquisition
- `src/rts_predict/aoe2/reports/aoestats/README.md`: removed pre-phase provenance note, T_ingestion row count section, and schema drift section (all DuckDB-derived); acquisition date preserved under Acquisition

### Fixed

### Removed
- `session_audit.md` (replaced by `scripts/session_audit.py`)
- 10 orphaned spec files from PR #108 (`planning/specs/spec_01` through `spec_10`)
- `reports/RESEARCH_LOG_TEMPLATE.md` — superseded by `docs/research/RESEARCH_LOG_ENTRY.md` (added in 3.0.3)

## [3.0.3] — 2026-04-11 (PR #108: chore/template-hierarchy)

### Added
- `docs/templates/phase_template.yaml` — ROADMAP authoring template for Phase blocks
- `docs/templates/pipeline_section_template.yaml` — ROADMAP authoring template for Pipeline Section blocks
- `docs/templates/dataset_roadmap_template.yaml` — ROADMAP document structure template
- `docs/templates/research_log_template.yaml` — research log document structure template (updated to match new hierarchy)
- `docs/templates/phase_status_template.yaml` — schema for PHASE_STATUS.yaml files
- `docs/templates/pipeline_section_status_template.yaml` — schema for PIPELINE_SECTION_STATUS.yaml files
- `docs/templates/step_status_template.yaml` — schema for STEP_STATUS.yaml files
- PIPELINE_SECTION_STATUS.yaml for all 3 datasets (sc2egset, aoe2companion, aoestats)
- `docs/ml_experiment_phases/PHASES.md`, `PIPELINE_SECTIONS.md`, `STEPS.md` — canonical reference docs for the three-tier tracking hierarchy
- `docs/research/RESEARCH_LOG.md`, `RESEARCH_LOG_ENTRY.md`, `ROADMAP.md` — reference docs for research log and roadmap conventions
- Materialization gate in plan/execute workflow: DAG.yaml + spec files required before execution begins
- DAG.yaml and 10 spec files in `planning/` for this branch

### Changed
- AoE2 game-level ROADMAP: retracted premature PRIMARY/SUPPLEMENTARY role assignments, replaced with provisional language pending Phase 01 Decision Gates
- AoE2 dataset ROADMAPs (aoe2companion, aoestats): removed premature role banners, set roles to TO BE DETERMINED, restored full Phase 01-07 scope
- STEP_STATUS.yaml: added `game` and `pipeline_section` fields (all 3 datasets); updated derivation comments to three-tier chain
- PHASE_STATUS.yaml: added derivation chain comments (all 3 datasets)
- CLAUDE.md: added materialization gate to Plan/Execute workflow; added PIPELINE_SECTION_STATUS.yaml to Key File Locations
- `planning/README.md`: added materialization gate to lifecycle section
- `.claude/agents/executor.md`: updated spec-first read order for dispatched agents
- `scripts/hooks/log-subagent.sh`: added model mappings for reviewer-deep, reviewer-adversarial, and writer-thesis agents

### Fixed

### Removed
- `.gitignore`: removed `.github/tmp/` staging-area override rules (`!.github/tmp/`, `.github/tmp/*`, `!.github/tmp/.gitkeep`); the directory's `.gitkeep` remains tracked and ephemeral files (`pr.txt`, `commit.txt`) are cleaned up by the workflow immediately after use

### Follow-up
- DAG review gates: the execution graph specified 3 separate reviewer agents for TG02/TG03/TG04 but the orchestrator combined them into a single reviewer invocation. The TG05 intermediate review gate was also elided in favor of a direct `reviewer-deep` final pass. Both deviations preserved dependency ordering. Follow-up: consider whether `planning/dags/DAG.yaml` should support a `combinable: true` flag on adjacent review gates to make this consolidation explicit rather than ad-hoc.

## [3.0.2] — 2026-04-11 (PR #107: chore/dag-orchestration-infrastructure)

### Added
- `planning/` directory — unified orchestration root for plan/execute workflow
- `planning/INDEX.md` — agent routing table (token-efficient entry point)
- `planning/README.md` — lifecycle, purge protocol, source-of-truth rules
- `planning/dags/README.md` — DAG format documentation, commit strategy, review gates
- `docs/templates/dag_template.yaml` — YAML schema for execution DAGs
- `docs/templates/dag_status_template.yaml` — lightweight execution state tracker
- `docs/templates/spec_template.md` — YAML-frontmatter + markdown for task specs
- `scripts/hooks/guard-master-branch.sh` — prevents Write/Edit on master branch
- DAG, Job, Task Group, Task — operational terms in `docs/TAXONOMY.md`
- DAG Orchestration section in `docs/agents/AGENT_MANUAL.md`
- Tier 8b (planning artifacts) in `ARCHITECTURE.md` source-of-truth hierarchy

### Changed
- `_current_plan.md` → `planning/current_plan.md` (path migration across 13 files)
- `specs/` → `planning/specs/` (directory restructure)
- `.claude/settings.json` — added branch guard hook to PreToolUse
- Planners now required to include "Suggested Execution Graph" in every plan
- Executor "Read first" updated for spec-file vs full-plan dispatch
- Disambiguated casual "task" usage in agent descriptions (now a formal term)

## [3.0.1] — 2026-04-11 (PR #106: chore/hooks-and-permissions)

### Added
- `scripts/hooks/log-bash.sh` — PreToolUse hook that appends every Bash invocation to `~/.claude/bash-audit.log` for full audit trail across all agents and sub-agents
- `scripts/hooks/README.md` — documents all four hooks with useful query commands for each log

### Changed
- `.claude/settings.json` — replaced ~50 per-command `Bash(cmd:*)` allow entries (several broken due to wrong `:` separator) with a single `Bash(*)` wildcard; same consolidation for `Write(*)`/`Edit(*)`; deny list unchanged; added `PreToolUse` Bash hook entry

## [3.0.0] — 2026-04-11 (PR #105: chore/pre-01_01_02-housekeeping)

### Added
- `docs/templates/research_log_entry_template.yaml`: canonical YAML template
  for research log entries (required/optional sections, Invariant #6 compliance)
- `STEP_STATUS.yaml` for all 3 datasets: step-level execution tracking
  (01_01_01 marked complete); PHASE_STATUS.yaml now derived from step status
- Provenance markers on AoE2 ROADMAP source_data sections and reports/ README
  files (pre-phase-system content clearly labelled as unverified)
- raw/README.md files populated with 01_01_01 artifact data (dotfile exclusion)

### Changed
- `.claude/ml-protocol.md`: hardcoded research log fields replaced with
  template reference
- `CLAUDE.md`: STEP_STATUS.yaml added to session-start reads and key files
- `docs/templates/raw_data_readme_template.yaml`: total_files exclusion
  policy changed from ".gitkeep only" to "all dotfiles"
- `ARCHITECTURE.md`: data/ package description updated for Phase 01 state
- `src/rts_predict/sc2/cli.py`: removed init/audit/explore subcommands
  (depended on deleted legacy code); kept export-schemas and db commands
- `src/rts_predict/sc2/config.py`: quarantine marker added to ML constants
- `.claude/rules/sql-data.md`: premature "Validated in Phase 01" claim fixed

### Removed
- **BREAKING:** `src/rts_predict/sc2/data/README.md` — 238 lines of pre-Phase
  Stage 1-5 pipeline documentation (context leak for schema discovery)
- **BREAKING:** `src/rts_predict/aoe2/data/README.md` — superseded acquisition
  plan using banned "Phase 0" terminology
- **BREAKING:** `src/rts_predict/sc2/data/{schemas,ingestion,exploration,audit}.py`
  — pre-Phase legacy code assuming unvalidated raw file schemas (~3,500 lines)
- **BREAKING:** `src/rts_predict/sc2/data/sc2egset/db/schemas/*.yaml` — 7 pre-Phase
  DuckDB DESCRIBE exports (will be regenerated by Phase 01 schema discovery)
- **BREAKING:** `src/rts_predict/aoe2/data/{aoe2companion,aoestats}/audit.py`
  — pre-Phase "Phase 0" schema profiling (~900 lines)
- `src/rts_predict/sc2/data/samples/` — sample replay files and processing script
- `stress_test.md`, `what_can_be_pre_commit_hooks.md`, `coverage.txt` — stale artifacts
- Dead `pyproject.toml` references to deleted files (mirror_drift exempt_sources,
  coverage omit _legacy)

## [2.0.0] — 2026-04-11 (PR #104: chore/architecture-audit-fixes)

### Added
- `.claude/scientific-invariants.md` Invariant #3: normalization leakage guard (de Prado 2018, Arlot & Celisse 2010) — scalers must fit on training data only
- Invariant #8: two-level statistical comparison framework — within-game (Friedman, N_folds >= 5) vs cross-game (per-game rankings + bootstrapped CIs + 5x2 cv F-test for N=2 games)
- AoE2 dataset strategy: aoe2companion = PRIMARY, aoestats = SUPPLEMENTARY VALIDATION — documented in game ROADMAP, per-dataset ROADMAPs, and research_log
- `docs/templates/notebook_template.yaml`: `{phase_slug}` and `{section_slug}` placeholders for TAXONOMY-compliant artifact paths
- `thesis/THESIS_STRUCTURE.md`: provisional markers on Chapters 5-7
- `docs/templates/raw_data_readme_template.yaml`: Section Z skip-gate header for agents

### Changed
- **BREAKING:** Artifact directory convention aligned to TAXONOMY.md — `artifacts/01_01/` → `artifacts/01_exploration/01_acquisition/` across all 3 datasets (sc2egset, aoe2companion, aoestats)
- Thesis chapter numbering fixed: "Chapter 3 — Data & Methodology" → "Chapter 4 — Data and Methodology" in ROADMAPs, notebooks, research_log, raw_data_readme_template
- Evaluation metrics hierarchy: Brier score (Murphy decomposition) promoted to primary metric in THESIS_STRUCTURE.md §4.4.4
- `CONTRACT.md`: Invariant #10 → #8 (renumbering drift fix)
- `.claude/ml-protocol.md`: activation gate lowered from Phase 04 to Phase 02; research log field names reconciled with actual usage; stale archive references updated
- `.claude/agents/planner-science.md`: ml-protocol reference updated to Phase 02
- `docs/thesis/THESIS_WRITING_MANUAL.md`: Friedman N=2 caveat added, two-level comparison framework
- `CLAUDE.md`: converted duplicated sections to pointers → ARCHITECTURE.md (153 → 108 lines); restored after-phase-gate and after-Category-F tracking instructions
- `docs/TAXONOMY.md`: reference-only usage note added
- ROADMAP placeholder sections (Phases 02-07): Pipeline Section lists replaced with one-line pointers to `docs/PHASES.md` (3 ROADMAPs)
- `thesis/WRITING_STATUS.md`: compressed BLOCKED entries into summary lines (115 → 95 lines)
- `pyproject.toml`: removed dead ruff/mirror_drift references to deleted archive paths

### Removed
- `reports/archive/` — stale pre-phase-migration research log archives
- `src/rts_predict/sc2/reports/sc2egset/archive/` — all superseded exploration artifacts
- `src/rts_predict/aoe2/reports/aoe2companion/archive/` — all superseded exploration artifacts
- `src/rts_predict/aoe2/reports/aoestats/archive/` — all superseded exploration artifacts

## [1.2.14] — 2026-04-11 (PR #103: chore/pre-commit-followup)

### Changed
- `.claude/settings.json`: add `Bash(pre-commit *)` to allow list so subagents can run pre-commit commands without triggering permission prompts (followup to #102)
- `.gitignore`: add `!/_current_review.md` and `!/_phases_review.md` as tracked exceptions

### Removed
- `source_audit.md`: stale planning artefact, superseded by phase work
- `web_enable_plan.md`: stale planning artefact, superseded by phase work

## [1.2.13] — 2026-04-11 (PR #102: chore/pre-commit-hooks)

### Added
- `.pre-commit-config.yaml`: ruff-check hook (`astral-sh/ruff-pre-commit` v0.9.10, `--no-fix`) and mypy local hook (`poetry run mypy src/rts_predict/`, `pass_filenames: false`) alongside the existing jupytext sync hook
- `what_can_be_pre_commit_hooks.md`: engineering audit that motivated this change

### Changed
- `pyproject.toml`: `[tool.ruff] extend-exclude` now skips `archive/` and `sandbox/` (E402/E501 are structural in jupytext percent-format notebooks); `[tool.mirror_drift] exempt_sources` now includes the two archive `.py` files to suppress false-positive orphan detection
- `.claude/settings.json`: added `Write/Edit` allow for `.pre-commit-config.yaml`; added `Bash(git commit*--no-verify*)` to deny list to prevent hook bypass
- `.claude/rules/python-code.md`, `.claude/agents/executor.md`, `.claude/rules/git-workflow.md`, `CLAUDE.md`: updated to reflect that ruff and mypy are now hook-enforced on every commit — no longer manual post-change gates

## [1.2.12] — 2026-04-11 (PR #101: chore/fix-source-activation-permissions)

### Changed
- `.claude/settings.json`: consolidated 11 fragmented `source .venv/bin/activate` Bash allow-patterns into a single catch-all `Bash(source .venv/bin/activate:*)`, covering all command variants (timed runs, piped output, non-poetry chains)

## [1.2.11] — 2026-04-11 (PR #100: chore/web-access-science-agents)

### Added
- `.claude/agents/reviewer-adversarial.md`: `WebFetch`, `WebSearch` added to tools; new `## Web access — when and how to use it` guidance section specifying allowed use cases and preferred sources (NeurIPS/ICML/AAAI/IJCAI, arXiv, JMLR, canonical textbooks)
- `.claude/agents/planner-science.md`: `WebFetch`, `WebSearch` added to tools
- `.claude/agents/reviewer-deep.md`: `WebFetch`, `WebSearch` added to tools
- `.claude/settings.json`: `WebFetch`, `WebSearch` added to `permissions.allow` (auto-approve without per-call prompt)

## [1.2.10] — 2026-04-11 (PR #99: chore/unsupervised-permissions-overhaul)

### Changed
- `.claude/settings.json`: replaced space-wildcard `poetry *` allow entry with 11 colon-delimited per-tool entries (ruff, mypy, pytest, jupyter, jupytext, diff-cover, sc2, python); added `git add:*`, `git commit:*`, `git rebase:*`, `gh pr:*`, `gh issue:*`, `.venv/bin/python:*`, `rm .github/tmp/*` to allow; narrowed `rm *` deny to `rm -r*`, `git rebase*` to `git rebase -i*`; removed `git commit*` from deny; removed `/tmp/**` Read/Write/Edit deny entries
- `.claude/settings.local.json`: pruned 107 accumulated one-off allow entries down to 11 (removed dead entries, absolute-path violations, double-slash bugs, `xargs rm` loophole, bare python3/pip entries, and everything now covered by settings.json)
- `CLAUDE.md`: updated Permissions section to reflect autonomous `git add`/`git commit`/`git rebase`; relaxed PHASE_STATUS.yaml rule to Category A/F only; added venv Python permission rule
- `.claude/agents/writer-thesis.md`: added `disallowedTools: Write(reports/**), Edit(reports/**)` to enforce "Do not modify reports/" programmatically

### Removed
- `Bash(python3 -m pytest*)` allow entry (contradicted "NEVER bare python3" rule)

## [1.2.9] — 2026-04-11 (PR #98: chore/inventory-enhancements-filename-patterns)

### Added
- `src/rts_predict/common/filename_patterns.py`: new module with `normalize_filename_to_pattern()` (replaces ISO dates → `{date}`, hex hashes ≥ 16 chars → `{hash}`, standalone numeric tokens → `{N}`) and `summarize_filename_patterns()` (returns `{pattern: count}` dict sorted by count descending)
- `tests/rts_predict/common/test_filename_patterns.py`: 10 tests covering both functions, 100% line coverage

### Changed
- `sandbox/sc2/sc2egset/01_01_01_file_inventory.{py,ipynb}`: added `summarize_filename_patterns` import and two new cells — whole-tree pattern summary (re-scans `_data/` two-level structure to collect all replay `FileEntry` objects) and markdown interpretation; JSON artifact now includes `filename_patterns` dict and `total_files_scanned` int; MD artifact now includes a "Filename patterns" table section
- `sandbox/aoe2/aoe2companion/01_01_01_file_inventory.{py,ipynb}`: same whole-tree pattern summary cells added; JSON and MD artifacts updated accordingly
- `sandbox/aoe2/aoestats/01_01_01_file_inventory.{py,ipynb}`: same whole-tree pattern summary cells added; JSON and MD artifacts updated accordingly

## [1.2.8] — 2026-04-10 (PR #97: chore/notebook-template-conformance-01_01_01)

### Changed
- `sandbox/sc2/sc2egset/01_01_01_file_inventory.{py,ipynb}`: restructured to conform with `docs/templates/notebook_template.yaml` v2 — added 3 missing frontmatter fields (Invariants applied, ROADMAP reference, Commit), consolidated datetime imports into cell_02, added markdown interpretation cells after every analysis code cell, replaced bare `## Verification` with structured `## Conclusion` (Artifacts produced, Thesis mapping, Follow-ups); analysis logic preserved verbatim
- `sandbox/aoe2/aoe2companion/01_01_01_file_inventory.{py,ipynb}`: same template conformance pass — additionally consolidated datetime import from mid-notebook into cell_02
- `sandbox/aoe2/aoestats/01_01_01_file_inventory.{py,ipynb}`: same template conformance pass — additionally consolidated datetime import from mid-notebook into cell_02

## [1.2.7] — 2026-04-10 (PR #96: chore/notebook-template-v2)

### Added
- Notebook template v2 at `docs/templates/notebook_template.yaml` — canonical schema for sandbox notebooks with parameterized placeholders, phase-conditional sections, and temporal leakage verification requirements

## [1.2.6] — 2026-04-10 (PR #95: chore/raw-readme-conformance)

### Changed
- `src/rts_predict/sc2/data/sc2egset/raw/README.md`: rewritten to conform to `raw_data_readme_template.yaml` (YAML front-matter + Markdown body); all artifact-derived numeric fields marked PENDING until corrected 01_01_01 artifacts are available
- `src/rts_predict/aoe2/data/aoe2companion/raw/README.md`: rewritten to conform to `raw_data_readme_template.yaml`; all artifact-derived numeric fields marked PENDING
- `src/rts_predict/aoe2/data/aoestats/raw/README.md`: rewritten to conform to `raw_data_readme_template.yaml`; all artifact-derived numeric fields marked PENDING

## [1.2.5] — 2026-04-10 (PR #94: chore/fix-agent-definitions)

### Changed
- `planner-science` agent: fixed invariant count (10 → 8), added AoE2 data layout, added `ml-protocol.md` to read-first list, added multi-dataset coordination guidance
- `executor` agent: expanded Category A temporal discipline rules (strict `< T`, three leakage failure modes, test requirement, Opus self-flag), fixed notebook workflow step 1 template reference, added Category F HALT-on-unsupported-claims guardrail, added AoE2 data layout and missing SC2 staging/tmp paths

## [1.2.4] — 2026-04-10 (PR #93: chore/raw-data-readme-template)

### Added
- `docs/templates/raw_data_readme_template.yaml`: standardized YAML schema for `raw/README.md` files across all game*dataset combinations, with sections A–H (Identity, Provenance, Content/Layout, Temporal Coverage, Acquisition Filtering, Verification, Immutability, Known Limitations) plus illustrative SC2 and AoE2 examples

## [1.2.3] — 2026-04-10 (PR #92: chore/adversarial-review-agent)

### Added
- `reviewer-adversarial` agent for scientific methodology challenge and thesis defensibility review
- `docs/agents/AGENT_MANUAL.md`: added `reviewer-adversarial`, `reviewer-deep`, and `writer-thesis` subsections, Workflow F (Methodology Challenge), Quick Reference rows, and Decision Flowchart updates

### Changed
- Renamed `.claude/agents/reviewier-deep.md` → `reviewer-deep.md` (typo fix)
- `.claude/agents/reviewer-deep.md`: added scope boundary section clarifying split with `reviewer-adversarial`; fixed "10 invariants" → "8 invariants"; fixed `AGENT_MANUAL.md` path to `docs/agents/AGENT_MANUAL.md`
- `CLAUDE.md`: agent table expanded from 5 to 8 agents
- `docs/agents/AGENT_MANUAL.md`: subtitle, agent count, color table, and cost table updated to reflect 8 agents

## [1.2.2] — 2026-04-10 (PR #91: chore/update-agent-docs-and-rules)

### Added
- `.claude/commands/pr.md`: `/pr` slash command skill for full PR wrap-up workflow
- `specs/README.md` + `specs/spec_*.md`: parallel spec execution framework
- `CLAUDE.md`: Parallel Executor Orchestration section (Strategy A shared-branch, Strategy B worktree)
- `docs/agents/AGENT_MANUAL.md`: Workflow E (parallel spec execution), Branch Guard hook docs, Custom Skills (`/pr`) section

### Changed
- All `poetry run` invocations prefixed with `source .venv/bin/activate &&` across CLAUDE.md, README.md, `.claude/agents/executor.md`, `.claude/agents/reviewer.md`, `.claude/rules/git-workflow.md`, `.claude/rules/python-code.md`, and `scripts/hooks/lint-on-edit.sh` for cross-machine reproducibility
- `.claude/settings.json`: added `Bash(source .venv/bin/activate && poetry *)` to the allow-list
- `README.md`: Quick Start commands updated; Prior Work section updated to reference per-dataset archive directories
- `.claude/rules/git-workflow.md`: clarified commit message workflow (Write tool to `.github/tmp/commit.txt`); added absolute-path note for ephemeral files

### Removed
- `temp/commit_msg.txt`, `temp/pr.txt`: ephemeral files cleaned up

## [1.2.1] — 2026-04-10 (PR #90: chore/phase01-status-update)

### Changed
- PHASE_STATUS.yaml: Phase 01 status updated to `in_progress` for sc2egset, aoe2companion, and aoestats
- `_current_plan.md` updated for traceability

## [1.2.0] — 2026-04-09 (PR #89: feat/phase01-step-01-01-01-file-inventory)

### Added
- Step 01_01_01 file inventory notebooks for sc2egset, aoe2companion, and aoestats
- File inventory artifacts (JSON + Markdown) for all 3 datasets
- Step 01_01_01 definitions in all 3 dataset ROADMAPs
- Research log entry for Step 01_01_01

## [1.1.0] — 2026-04-09 (PR #88: feat/phase01-discovery-library)

### Added
- `src/rts_predict/common/inventory.py`: `InventoryResult`, `SubdirSummary`, `FileEntry` dataclasses and `inventory_directory()` function for filesystem inventory
- `src/rts_predict/common/json_utils.py`: `KeyProfile` dataclass and `discover_json_schema()` function for root-level JSON schema discovery across multiple files
- `src/rts_predict/aoe2/config.py`: `AOESTATS_RAW_OVERVIEW_DIR` constant for overview file storage
- `src/rts_predict/aoe2/data/aoestats/acquisition.py`: `download_overview()` function for idempotent overview JSON acquisition
- `tests/rts_predict/common/test_inventory.py`: full test coverage for inventory module
- `tests/rts_predict/common/test_json_utils.py`: full test coverage for json_utils module (new and existing functions)
- `tests/rts_predict/aoe2/data/aoestats/test_acquisition.py`: tests for `download_overview()`

## [1.0.1] — 2026-04-09 (PR #87: chore/roadmap-phase01-skeleton-reset)

### Changed
- 3 dataset ROADMAPs: Phase 01 reset from detailed Steps to generic Pipeline Section skeleton; detailed versions archived with `_2026-04-09_detailed_phase01` suffix
- `thesis/WRITING_STATUS.md`: 2 stale `DRAFTABLE` statuses reset to `BLOCKED`; Phase 01 progress claim removed from header; game loop derivation note corrected

## [1.0.0] — 2026-04-09 (PRs #71–#85: chore/phase-migration)

Phase migration release. The project transitioned from an 11-phase scheme
(0–10) to a 7-phase scheme (01–07) defined in `docs/PHASES.md`. All prior
work remains accessible in per-dataset `archive/` directories.

This release consolidates the work delivered across PRs #70–#85 (versions
0.28.0–0.29.15) plus the foundational `docs/PHASES.md` and `docs/TAXONOMY.md`
documents that landed before the migration started.

### Added
- `docs/PHASES.md` — canonical 7-phase list (Phase 01–07); single source of
  truth for which Phases exist and what Pipeline Sections each contains
- `docs/TAXONOMY.md` — project-wide terminology taxonomy (Phase / Pipeline
  Section / Step hierarchy, directory layout rules, operational terms)
- `docs/templates/step_template.yaml` — science-oriented YAML Step definition
  schema (20+ fields: identity, hierarchy context, scientific purpose,
  predecessors, inputs/outputs, reproducibility, gate decomposition, thesis
  mapping, research_log_entry)
- `src/rts_predict/aoe2/reports/aoe2companion/README.md` — permanent API
  acquisition provenance record
- `src/rts_predict/aoe2/reports/aoestats/README.md` — permanent API
  acquisition provenance record (including known missing file and schema drift)
- `src/rts_predict/aoe2/reports/aoe2companion/ROADMAP.md` — dataset ROADMAP
  for aoe2companion; Phase 01 decomposed into 6 Pipeline Sections with 11 Steps
- `src/rts_predict/aoe2/reports/aoestats/ROADMAP.md` — dataset ROADMAP for
  aoestats; Phase 01 decomposed into 6 Pipeline Sections with 9 Steps
- `src/rts_predict/sc2/reports/sc2egset/PHASE_STATUS.yaml` — dataset-level
  phase status file with 7-phase schema (01–07), all `not_started`
- `src/rts_predict/aoe2/reports/aoe2companion/PHASE_STATUS.yaml` — dataset-level
  phase status file, same schema
- `src/rts_predict/aoe2/reports/aoestats/PHASE_STATUS.yaml` — dataset-level
  phase status file, same schema

### Changed
- Phase scheme migrated from 0–10 to 01–07 per `docs/PHASES.md` and
  `docs/TAXONOMY.md`; all operational files updated to new scheme
- `PHASE_STATUS.yaml` relocated from game-level to dataset-level
  (`reports/<dataset>/PHASE_STATUS.yaml`)
- All Claude operational files audited and updated: `.claude/dev-constraints.md`,
  `.claude/ml-protocol.md`, `.claude/rules/sql-data.md`,
  `.claude/rules/thesis-writing.md`, `.claude/scientific-invariants.md`,
  `CLAUDE.md`, `docs/INDEX.md`, all agent files under `.claude/agents/`
- `ARCHITECTURE.md`: inserted `docs/PHASES.md` as new tier 4 in Source-of-Truth
  Hierarchy; renumbered tiers 5–8; game package contract table updated to
  dataset-level `PHASE_STATUS.yaml`; "Adding a new game" Step 2 updated
- `README.md`: replaced stale `SC2_THESIS_ROADMAP.md` references with
  `docs/PHASES.md` pointer; Project State sentence updated to Phase 01 naming
- `docs/TAXONOMY.md`: Phase naming clarifications and `docs/PHASES.md`
  cross-references added
- `docs/agents/AGENT_MANUAL.md`: Workflow A updated for sandbox execution;
  `PHASE_STATUS` path pattern updated to dataset-level; added schema reading
  section (carried forward from v0.24.0)
- Game-level ROADMAPs rewritten as thin navigation pointers:
  `src/rts_predict/sc2/reports/ROADMAP.md` and
  `src/rts_predict/aoe2/reports/ROADMAP.md`
- `src/rts_predict/sc2/reports/sc2egset/ROADMAP.md`: complete rewrite from
  old Phase 0–10 scheme to new Phase 01–07 structure with 18 Steps in Phase 01
- `sandbox/README.md`: updated directory structure to nested Phase/PipelineSection/Step
  layout per `docs/TAXONOMY.md`; naming convention updated to three-level
  `{PHASE}_{SECTION}_{STEP}` scheme
- `sandbox/notebook_config.toml`: removed stale phase references
- `reports/RESEARCH_LOG_TEMPLATE.md`: step numbering format updated from
  `[PHASE X / Step X.Y]` to `[Phase XX / Step XX_YY_ZZ]`
- `reports/research_log.md`: reset to fresh log with migration header note
- Thesis structure files: `thesis/THESIS_STRUCTURE.md` and
  `thesis/WRITING_STATUS.md` updated to new Phase 01–07 numbering; chapter
  skeleton comments updated across chapters 02, 04, 05

### Removed
- `src/rts_predict/sc2/PHASE_STATUS.yaml` — replaced by dataset-level file
- `src/rts_predict/aoe2/PHASE_STATUS.yaml` — replaced by per-dataset files
- Old 11-phase scheme references throughout all operational and documentation
  files

### Archived
- All sc2egset Phase 0/1 artifacts, notebooks, and plans →
  `src/rts_predict/sc2/reports/sc2egset/archive/`
- All aoe2companion Phase 0 artifacts →
  `src/rts_predict/aoe2/reports/aoe2companion/archive/`
- All aoestats Phase 0 artifacts →
  `src/rts_predict/aoe2/reports/aoestats/archive/`
- `reports/research_log.md` (full pre-migration log) →
  `reports/archive/research_log_pre_phase_migration.md`

## [0.29.15] — 2026-04-09 (PR #85: chore/thesis-phase-refs)

### Changed
- `thesis/THESIS_STRUCTURE.md`: Phase-to-chapter mapping table rewritten from old 11-phase to new 7-phase (Phase 01–07) scheme; all scattered "Phase N" references updated; pointer to `docs/PHASES.md` added
- `thesis/WRITING_STATUS.md`: "Feeds from" column updated throughout to use new Phase 01–07 numbering; last-updated date refreshed
- `thesis/chapters/02_theoretical_background.md`: skeleton comment updated from "Phase 1" to "Phase 01 (Data Exploration)"
- `thesis/chapters/04_data_and_methodology.md`: all skeleton BLOCKED/DRAFTABLE comments updated to new Phase numbering with Pipeline Section references
- `thesis/chapters/05_experiments_and_results.md`: all skeleton BLOCKED comments updated to new Phase numbering

## [0.29.14] — 2026-04-09 (PR #84: chore/arch-game-contract-phase-refs)

### Changed
- `ARCHITECTURE.md`: game package contract table updated — `PHASE_STATUS.yaml` row moved from game-level to dataset-level (`reports/<dataset>/PHASE_STATUS.yaml`, Required column changed to "Per dataset")
- `ARCHITECTURE.md`: "Adding a new game" Step 2 updated to reference dataset-level `reports/<dataset>/PHASE_STATUS.yaml` with pointer to `docs/PHASES.md` schema
- `ARCHITECTURE.md`: SOT Hierarchy tier 5 (game-level ROADMAP) description updated — no longer claims to own canonical Phase numbering; now described as a navigation document pointing to `docs/PHASES.md`
- `ARCHITECTURE.md`: Progress tracking paragraph updated — "per game" changed to "per dataset"; sentence clarified to reference the active dataset's PHASE_STATUS.yaml

## [0.29.13] — 2026-04-09 (PR #83: chore/aoestats-roadmap)

### Added
- `src/rts_predict/aoe2/reports/aoestats/ROADMAP.md`: new dataset ROADMAP for aoestats; Phase 01 fully decomposed into 6 Pipeline Sections (01_01–01_06) with 9 Steps tailored to aoestats' data structure (2 raw tables: raw_matches and raw_players); known missing file `2025-11-16_2025-11-22_players.parquet` documented in header, Step 01_01_01, and cleaning rule inventory; schema drift (raw_match_type DOUBLE→BIGINT, five raw_players columns) documented in header with canonical resolved types verified in profiling steps; Phases 02-07 listed as placeholders; all notebook paths use nested layout under `sandbox/aoe2/aoestats/01_exploration/`; library function names verified against `ingestion.py`

## [0.29.12] — 2026-04-09 (PR #82: chore/aoe2companion-roadmap)

### Added
- `src/rts_predict/aoe2/reports/aoe2companion/ROADMAP.md`: new dataset ROADMAP for aoe2companion; Phase 01 fully decomposed into 6 Pipeline Sections (01_01–01_06) with 11 Steps tailored to aoe2companion's data structure (4 raw tables, no replay JSON parsing, no in-game event extraction); Phases 02-07 listed as placeholders; snapshot-table warning, sparse-regime boundary (2025-06-26), and acquisition provenance reference to README.md included; all notebook paths use nested layout; library function names verified against `ingestion.py`

## [0.29.11] — 2026-04-09 (PR #81: chore/sc2egset-roadmap-rewrite)

### Changed
- `src/rts_predict/sc2/reports/sc2egset/ROADMAP.md`: complete rewrite from old Phase 0-10 scheme to new Phase 01-07 structure; Phase 01 fully decomposed into 6 Pipeline Sections (01_01–01_06) with 18 Steps; Phases 02-07 listed as placeholders with Pipeline Section names from `docs/PHASES.md`; all notebook paths use nested layout per TAXONOMY.md; all library function references verified against actual code

## [0.29.10] — 2026-04-09 (PR #80: chore/game-roadmaps-phase-migration)

### Changed
- `src/rts_predict/sc2/reports/ROADMAP.md`: rewritten as thin navigation pointer; removed phase shells and planning content; lists sc2egset dataset with links to its ROADMAP and PHASE_STATUS.yaml
- `src/rts_predict/aoe2/reports/ROADMAP.md`: rewritten as thin navigation pointer; removed placeholder planning content; lists aoe2companion and aoestats datasets with links to their ROADMAPs and PHASE_STATUS.yaml files

## [0.29.9] — 2026-04-09 (PR #79: chore/phase-status-redesign)

### Added
- `src/rts_predict/sc2/reports/sc2egset/PHASE_STATUS.yaml`: new dataset-level phase status file with 7-phase schema (01–07), all `not_started`
- `src/rts_predict/aoe2/reports/aoe2companion/PHASE_STATUS.yaml`: new dataset-level phase status file, same schema
- `src/rts_predict/aoe2/reports/aoestats/PHASE_STATUS.yaml`: new dataset-level phase status file, same schema

### Removed
- `src/rts_predict/sc2/PHASE_STATUS.yaml`: replaced by dataset-level file; used wrong granularity (game-level) and old 11-phase numbering (0–10)
- `src/rts_predict/aoe2/PHASE_STATUS.yaml`: replaced by per-dataset files; same issues

## [0.29.8] — 2026-04-09 (PR #78: chore/research-log-archive-fresh-start)

### Changed
- `reports/RESEARCH_LOG_TEMPLATE.md`: updated step numbering format from `[PHASE X / Step X.Y]` to `[Phase XX / Step XX_YY_ZZ]` per docs/PHASES.md
- `reports/research_log.md`: reset to fresh log with migration header note; all new entries use the new step format

### Fixed
- `CHANGELOG.md`: corrected PR number placeholders (`PR #N` → `PR #77` for 0.29.7, `PR #11` → `PR #78` for 0.29.8)
- `CLAUDE.md`: updated sandbox naming convention from `{PHASE:02d}_{STEP}` to three-level `{PHASE}_{PIPELINE_SECTION}_{STEP}` matching sandbox/README.md
- `CLAUDE.md`: fixed stale agent manual path `docs/AGENT_MANUAL.md` → `docs/agents/AGENT_MANUAL.md`

### Removed
- `reports/research_log.md` (old log): archived to `reports/archive/research_log_pre_phase_migration.md`
- `reports/_archive/` directory: consolidated into `reports/archive/`; `research_log_pre_notebook_sandbox.md` moved to `reports/archive/`

## [0.29.7] — 2026-04-09 (PR #77: chore/sandbox-phase-refs)

### Changed
- `sandbox/README.md`: updated directory structure to show nested Phase/PipelineSection/Step layout per `docs/TAXONOMY.md`; updated naming convention from flat `{PHASE}_{STEP}` to three-level `{PHASE}_{SECTION}_{STEP}`; replaced old phase references ("Phases 0–2", "Phase 1", "Step 1.1", "Step 1.8") with new scheme; corrected jupytext.toml path to `sandbox/jupytext.toml`
- `sandbox/notebook_config.toml`: removed stale `_current_plan.md B.9.16` and `Step 1.6` references

## [0.29.6] — 2026-04-09 (PR #76: chore/archive-aoestats-phase-migration)

### Changed
- `src/rts_predict/aoe2/reports/aoestats/archive/`: consolidated all pre-migration aoestats artifacts — moved `INVARIANTS.md` and all 8 Phase 0 artifacts (`00_01` through `00_07`) into `archive/`; created `archive/_README.md` describing archive contents
- `src/rts_predict/aoe2/reports/aoestats/README.md`: added permanent provenance record preserving acquisition facts (download date 2026-04-06, 172 non-zero weeks, 30,690,651 raw_matches rows, schema drift details, known download failure for `2025-11-16_2025-11-22_players.parquet`)

## [0.29.5] — 2026-04-09 (PR #75: chore/archive-aoe2companion-phase-migration)

### Changed
- `src/rts_predict/aoe2/reports/aoe2companion/archive/`: consolidated all pre-migration aoe2companion artifacts — moved `INVARIANTS.md`, `aoe2companion_download_report.md`, and all 10 Phase 0 artifacts (`00_01` through `00_08`) into `archive/`; created `archive/_README.md` describing archive contents
- `src/rts_predict/aoe2/reports/aoe2companion/README.md`: added permanent provenance record preserving acquisition facts (download date 2026-04-06, 4,147 files, 277,099,059 raw_matches rows, snapshot timestamps, sparse rating regime boundary 2025-06-26, dtype strategy, reconciliation strength)

## [0.29.4] — 2026-04-09 (PR #74: chore/archive-sc2egset-phase-migration)

### Changed
- `src/rts_predict/sc2/reports/sc2egset/archive/`: consolidated all pre-migration sc2egset artifacts — moved `INVARIANTS.md`, `SUPERSEDED.md`, `artifacts/00_99_post_rebuild_verification.md`, sandbox notebooks (`01_08_game_settings_audit`, `00_99_post_rebuild_verification`), `sandbox/sc2/sc2egset/plans/`, and `_archive_2026-04_pre_notebook_reset/` into a single `archive/` directory; created `archive/_README.md` describing the archive contents
- `sandbox/sc2/sc2egset/`: removed pre-migration notebooks and plans; added `.gitkeep` to preserve directory for future Phase 01 work

## [0.29.3] — 2026-04-09 (PR #73: chore/claude-agents-phase-refs)

### Changed
- `.claude/agents/executor.md`, `.claude/agents/planner-science.md`, `.claude/agents/reviewer.md`, `.claude/agents/reviewier-deep.md`, `docs/agents/AGENT_MANUAL.md`: replaced old-scheme phase references with canonical new-scheme refs and updated `PHASE_STATUS` path pattern to dataset-level

## [0.29.2] — 2026-04-09 (PR #72: chore/sot-hierarchy-phase-refs)

### Added
- `docs/templates/step_template.yaml`: full science-oriented YAML step schema (20+ fields) covering identity, hierarchy context, scientific purpose, predecessors, inputs/outputs, reproducibility, scientific invariants applied, gate decomposition (artifact_check, continue_predicate, halt_predicate), thesis mapping, and research_log_entry

### Changed
- `ARCHITECTURE.md`: inserted `docs/PHASES.md` as new tier 4 in Source-of-Truth Hierarchy; renumbered old tiers 4–7 to 5–8; updated internal cross-references; removed old-scheme phase number ranges from package layout and game contract tables
- `README.md`: replaced stale `SC2_THESIS_ROADMAP.md` references with `docs/PHASES.md` pointer; updated Project State sentence to Phase 01 naming scheme
- `docs/TAXONOMY.md`: added Phase naming clarifications and `docs/PHASES.md` cross-reference updates

## [0.29.1] — 2026-04-09 (PR #71: chore/claude-ops-phase-refs-core)

### Changed
- `.claude/dev-constraints.md`, `.claude/ml-protocol.md`, `.claude/rules/sql-data.md`, `.claude/rules/thesis-writing.md`, `.claude/scientific-invariants.md`, `CLAUDE.md`, `docs/INDEX.md`: replaced hardcoded old-scheme phase identifiers (Phases 0–11) with canonical new-scheme refs (Phase 01–07) and `docs/PHASES.md` pointers

## [0.29.0] — 2026-04-09 (PR #70: docs/project-taxonomy-draft)

### Changed
- `docs/TAXONOMY.md`: added `docs/PHASES.md` cross-reference and Phase naming clarifications

## [0.28.0] — 2026-04-09 (PR #69: docs/canonical-phase-list)

### Added
- `docs/PHASES.md`: canonical Phase list — single source of truth for which Phases exist and what Pipeline Sections each contains; defines the 7-Phase ML experiment lifecycle (01 Data Exploration through 07 Thesis Writing Wrap-up), Phase scope rule, Pipeline Section derivation rule with per-Phase tables and exclusion rationale, Phase 07 gate-marker semantics, and maintenance rules

## [0.27.0] — 2026-04-09 (PR #68: docs/architecture-source-of-truth)

### Added
- `ARCHITECTURE.md`: preamble pointer to `docs/TAXONOMY.md` as the vocabulary source of truth
- `ARCHITECTURE.md`: new "Source-of-Truth Hierarchy" section — 7-tier precedence ladder with propagation rule and out-of-scope note
- `ARCHITECTURE.md`: `docs/TAXONOMY.md` row added to the cross-cutting files table

## [0.26.0] — 2026-04-09 (PR #67: docs/project-taxonomy)

### Added
- `docs/TAXONOMY.md`: project-wide terminology taxonomy — single source of truth for Phase / Pipeline Section / Step hierarchy, directory layout rules, operational terms (Spec, PR, Category, Session), and the list of terms explicitly not used

## [0.25.0] — 2026-04-09 (PR #66: plan/phase1-sc2-taxonomy)

### Added
- `sandbox/sc2/sc2egset/plans/01_00_phase1_taxonomy_and_first_chunk_plan.md`: Phase 1 planning document with JSON field taxonomy (~200 leaf fields), per-table shape assessment, 10 cross-table integrity concerns, 16 candidate steps in 3 sub-phases, and first-chunk recommendation (steps 01_01–01_05)

## [0.24.1] — 2026-04-09 (PR #64: chore/phase1-sc2-archive-pre-reset)

### Added
- `src/rts_predict/sc2/reports/sc2egset/_archive_2026-04_pre_notebook_reset/_README.md`: tombstone explaining why artifacts were archived, what was excluded, and how to recover
- `src/rts_predict/sc2/reports/sc2egset/_archive_2026-04_pre_notebook_reset/01_00_phase1_audit_inventory.csv`: full inventory of 36 archived artifacts with kind, step ID, size, mtime, deleted-symbol references, and disposition
- Stage 3a entry in `reports/research_log.md`

### Changed
- 36 numbered Phase 0/1 artifacts moved via `git mv` from `sc2/reports/sc2egset/artifacts/` to `_archive_2026-04_pre_notebook_reset/` — preserved for historical reference, not current use

## [0.24.0] — 2026-04-08 (PR #63: feat/schema-export-utility)

### Added
- `src/rts_predict/common/schema_export.py`: generic DuckDB schema export utility producing per-table YAML files + `_index.yaml`, with comment/notes preservation across re-runs
- `poetry run sc2 export-schemas --db <db> --out <dir>`: CLI command for schema export
- `tests/rts_predict/common/test_schema_export.py`: 10 tests covering file count, structure, comment preservation, warning on dropped columns, and edge cases
- `tests/rts_predict/common/conftest.py`: `two_table_db` fixture for schema export tests
- Schema YAML files for all 6 sc2egset tables with hand-filled column comments and table-level notes: `src/rts_predict/sc2/data/sc2egset/db/schemas/`
- "Reading database schemas" section in `docs/agents/AGENT_MANUAL.md`
- `pyyaml` production dependency, `types-pyyaml` dev dependency
- Stage 2 entry in `reports/research_log.md`

### Changed
- `raw_map_alias_files` table: added `PRIMARY KEY (tournament_dir)` — constraint enforced by DuckDB v1.5.1
- DB rebuilt after PK addition; verified raw=22,390, raw_map_alias_files=70 (no drift)

### Fixed

### Removed

## [0.23.0] — 2026-04-08 (PR #62: feat/phase0-map-alias-ingestion)

### Added
- `ingest_map_alias_files(con, raw_dir, *, mapping_filename)` in `ingestion.py`: row-per-file ingestion with SHA1 checksum, raw JSON stored verbatim, new `raw_map_alias_files` table schema (tournament_dir, file_path, byte_sha1, n_bytes, raw_json, ingested_at)
- `_RAW_MAP_ALIAS_CREATE_QUERY` constant with the new 6-column schema
- `in_memory_duckdb` fixture in `tests/rts_predict/sc2/data/conftest.py`
- Verification notebook `sandbox/sc2/sc2egset/00_99_post_rebuild_verification.{py,ipynb}`
- Report artifact `src/rts_predict/sc2/reports/sc2egset/artifacts/00_99_post_rebuild_verification.md`
- Stage 1 entry in `reports/research_log.md`

### Changed
- `cli.py`: `init_database()` now calls `ingest_map_alias_files(con, REPLAYS_SOURCE_DIR)` — produces two raw tables only (`raw`, `raw_map_alias_files`)
- `ingestion.py`: module docstring updated to reflect row-per-file design
- `src/rts_predict/sc2/data/README.md`: updated pipeline usage and removed stale Stage 3/4 view docs
- `src/rts_predict/sc2/reports/sc2egset/ROADMAP.md`: Step 0.9 updated; Phase 1 inputs list updated

### Removed
- `load_map_translations()` from `ingestion.py` — replaced by `ingest_map_alias_files`
- `map_translation` table (was created inline by `load_map_translations`)
- `create_ml_views()` and `_MATCHES_VIEW_QUERY` from `processing.py`
- `validate_map_translation_coverage()` from `audit.py`
- All corresponding test classes: `TestCreateMlViews` (test_processing.py); old `TestIngestMapAliasFiles` (replaced with 3 new tests)
- `map_translation` fixture from `raw_table_con` in `tests/rts_predict/sc2/data/conftest.py`

## [0.22.4] — 2026-04-08 (PR #61: chore/sandbox-and-artifacts-guidance)

### Added
- `CLAUDE.md`: new "Phase Work Execution (Sandbox Notebooks)" section documenting that all Category A code runs in `sandbox/<game>/<dataset>/` jupytext pairs and artifacts go to `reports/<dataset>/artifacts/`
- `ARCHITECTURE.md`: `sandbox/` added to repo layout tree and cross-cutting files table
- `.claude/dev-constraints.md`: new "Phase Work Execution" section
- `.claude/agents/executor.md`: new notebook workflow item requiring artifacts to target `artifacts/` subdir
- `.claude/agents/reviewer.md`: new "Artifact path check" item in notebook review checklist
- `.claude/agents/reviewier-deep.md`: new "Artifact output path" blocker-level check
- `.claude/agents/planner-science.md`: Category A plans must now specify sandbox notebook path and artifact target
- `docs/agents/AGENT_MANUAL.md`: Workflow A now describes sandbox execution and artifact path convention

### Changed
- `sandbox/README.md`: fixed "Report artifacts" paragraph — path now correctly points to `reports/<dataset>/artifacts/` (was incorrectly pointing to the report root)

## [0.22.3] — 2026-04-08 (PR #60: chore/artifacts-subdir-migration)

### Changed
- All machine-generated step artifact files (`XX_XX_*` prefix, any extension) moved from `reports/<dataset>/` into `reports/<dataset>/artifacts/` subdirectories (54 files across sc2egset, aoe2companion, aoestats)
- Added `DATASET_ARTIFACTS_DIR`, `AOE2COMPANION_ARTIFACTS_DIR`, `AOESTATS_ARTIFACTS_DIR` config constants; updated all writer functions in `audit.py` and `exploration.py` to use them
- Updated 4 test files, ROADMAP.md, SUPERSEDED.md, INVARIANTS.md, ARCHITECTURE.md, research logs, and sandbox notebook to reference new artifact paths

## [0.22.2] — 2026-04-08 (PR #59: chore/test-mirror-migration)

### Added
- `scripts/check_mirror_drift.py` — guardrail script enforcing `src/` ↔ `tests/` mirror
- `tests/infrastructure/test_mirror_drift.py` — tests for the drift checker
- `branch = true` in `[tool.coverage.run]` for branch coverage
- `diff-cover` dev dependency for PR diff-coverage checks

### Changed
- Test layout: migrated from co-located `src/rts_predict/**/tests/` to mirrored `tests/rts_predict/` tree
- `pyproject.toml`: `testpaths` now `["tests"]` only; added `--import-mode=importlib`
- All agent and documentation references updated to new test layout

## [0.22.1] — 2026-04-08 (PR #58: chore/notebook-sandbox)

### Added
- `sandbox/` directory structure for Jupyter notebook exploration (gitignored working artifacts)
- `sandbox/jupytext.toml` — jupytext pairing config (percent format, metadata filter)
- `sandbox/notebook_config.toml` — notebook workflow constraints (50-line cell cap, read-only DB policy)
- `src/rts_predict/common/notebook_utils.py` — `get_notebook_db()` and `get_reports_dir()` helpers for sandbox notebooks
- `.pre-commit-config.yaml` — jupytext sync hook wired into pre-commit
- `sandbox/sc2/sc2egset/01_08_game_settings_audit.ipynb` — proof-of-concept notebook reproducing Step 1.8 game settings audit
- `src/rts_predict/sc2/reports/sc2egset/SUPERSEDED.md` — documents which report artifacts are superseded by notebooks

### Changed
- `reports/research_log.md` — archived old log, created fresh with two new entries (Category A Step 1.8 audit + Category C sandbox chore)
- `.claude/agents/` executor and reviewer agents updated with notebook workflow rules

## [0.22.0] — 2026-04-08 (PR #57: feat/sc2-phase1-step1.9)

### Added
- `run_tpdm_field_inventory`, `run_tpdm_key_set_constancy`, `run_toplevel_field_inventory` functions in `src/rts_predict/sc2/data/exploration.py` (Step 1.9A/B/C)
- Step `"1.9"` registered in `run_phase_1_exploration` orchestrator (also supports sub-step IDs `"1.9A"`, `"1.9B"`, `"1.9C"`)
- Three CSV artifacts in `src/rts_predict/sc2/reports/sc2egset/`: `01_09_tpdm_field_inventory.csv` (20 TPDM keys), `01_09_tpdm_key_set_constancy.csv` (1 variant, 100% coverage), `01_09_toplevel_field_inventory.csv` (18 column/key pairs incl. nested `initData.gameDescription`)
- 19 new tests for Step 1.9 in `src/rts_predict/sc2/data/tests/test_exploration.py`

### Changed

### Fixed

### Removed

## [0.21.0] — 2026-04-07 (PR #56: feat/sc2-phase1-step1.8)

### Added
- `src/rts_predict/sc2/reports/sc2egset/artifacts/01_08_game_settings_audit.md` — full game settings and replay field completeness audit for SC2EGSet (22,390 replays, 70 tournaments): game speed, handicap, error flags, game mode flags, random race, map/lobby metadata, and version consistency sub-steps with embedded SQL and findings
- `src/rts_predict/sc2/reports/sc2egset/artifacts/01_08_error_flags_audit.csv` — parse error flag scan results (zero errors found across all replays)

### Changed
- `src/rts_predict/sc2/reports/sc2egset/ROADMAP.md` — Step 1.8 marked complete, cleaning rules C-D1 and C-E1 added to Phase 6 backlog
- `reports/research_log.md` — Phase 1 Step 1.8 entry added with key findings and artifact references

## [0.20.7] — 2026-04-07 (PR #55: feat/aoe2-phase0-ingestion)

### Added
- `src/rts_predict/aoe2/data/aoe2companion/audit.py` — Phase 0 audit functions for aoe2companion dataset (source audit, schema profiling for matches/ratings/singletons, smoke test, reconciliation, Phase 0 summary)
- `src/rts_predict/aoe2/data/aoe2companion/ingestion.py` — full CTAS ingestion for all four aoe2companion raw tables
- `src/rts_predict/aoe2/data/aoe2companion/types.py` — shared type aliases for aoe2companion audit return values
- `src/rts_predict/aoe2/data/aoestats/audit.py` — Phase 0 audit functions for aoestats dataset (source audit, match/player schema profiling with per-sample row counts, smoke test, reconciliation)
- `src/rts_predict/aoe2/data/aoestats/ingestion.py` — full CTAS ingestion for aoestats raw tables
- `src/rts_predict/aoe2/reports/aoe2companion/` — 8 Phase 0 report artifacts: source audit, 3 schema profiles, dtype decision, smoke test, ingestion log, reconciliation, Phase 0 summary, and INVARIANTS.md
- `src/rts_predict/aoe2/reports/aoestats/` — 7 Phase 0 report artifacts: source audit, match/player schema profiles (with per-sample row counts), smoke test, ingestion log, reconciliation, Phase 0 summary, and INVARIANTS.md

### Changed
- `src/rts_predict/aoe2/PHASE_STATUS.yaml` — Phase 0 marked `status: complete`, `gate_date: "2026-04-07"` for both aoe2companion and aoestats datasets
- `reports/research_log.md` — aoe2companion Phase 0 entry (Steps 0.1–0.8) added in reverse-chronological order alongside existing aoestats entry

## [0.20.6] — 2026-04-07 (PR #54: chore/phase1-roadmap-augmentation)

### Changed
- `src/rts_predict/sc2/reports/sc2egset/ROADMAP.md` — Steps 1.9–1.16 inserted after Step 1.8 covering schema profiling, temporal analysis, leakage audit, data quality reporting, risk register, modeling readiness decision, and documentation consolidation; Phase 1 gate replaced with four §6.1 thesis deliverables (data dictionary, data quality report, risk register, modeling readiness decision)
- `src/rts_predict/sc2/PHASE_STATUS.yaml` — Phase 1 `notes:` field updated to reflect new gate structure and pending steps 1.9–1.16

## [0.20.5] — 2026-04-07 (PR #53: chore/research-log-template-content)

### Added
- `reports/RESEARCH_LOG_TEMPLATE.md` — canonical template for Category A and F research log entries, with mandatory fields (date, phase, step, actions, findings, next steps)

### Changed
- `reports/research_log.md` — Steps 1.6 and 1.7 rewritten into new template format; header note added pointing to `RESEARCH_LOG_TEMPLATE.md`

## [0.20.4] — 2026-04-07 (PR #52: chore/research-log-template)

### Added
- `reports/RESEARCH_LOG_TEMPLATE.md` — canonical template for research log entries, establishing structured format with mandatory fields (date, phase, step, actions, findings, next steps)

### Changed
- `reports/research_log.md` — Steps 1.6 and 1.7 rewritten into new template format; header note added pointing to `RESEARCH_LOG_TEMPLATE.md`

## [0.20.3] — 2026-04-07 (PR #51: chore/sc2-reports-roadmap-placeholder)

### Changed
- `src/rts_predict/sc2/reports/ROADMAP.md` — replaced speculative Phase 3–10 content with a short placeholder; Phase ≥2 content is not authored until all SC2 datasets complete their Phase 1 epistemic-readiness gate; planned phase shells (names only) and authoring trigger documented

## [0.20.2] — 2026-04-07 (PR #50: chore/dataset-agnostic-invariants)

### Changed
- `.claude/scientific-invariants.md` — stripped all SC2EGSet-specific empirical findings (APM, MMR, 22.4 game-loop constant); remaining 8 invariants are fully dataset-agnostic and game-agnostic; added explicit header declaring scope and 5 pointers to `docs/INDEX.md` and `docs/ml_experiment_lifecycle/06_CROSS_DOMAIN_TRANSFER_MANUAL.md`; added "Per-dataset findings" section directing readers to per-dataset INVARIANTS files
- `.claude/agents/planner-science.md` — "Read first" list now uses dataset-agnostic paths (universal invariants → INDEX.md → active PHASE_STATUS → active ROADMAP → active INVARIANTS → research log); role description updated to reference `docs/INDEX.md` instead of SC2 roadmap
- `.claude/rules/thesis-writing.md` — replaced hardcoded SC2 "Phase-to-Section Mapping" table with a pointer to `docs/INDEX.md` and each ROADMAP.md's per-step "Thesis mapping" field as the single source of truth
- `CLAUDE.md` — added "Per-dataset invariants" row to Key File Locations table

### Added
- `src/rts_predict/sc2/reports/sc2egset/INVARIANTS.md` — new file holding SC2EGSet-specific empirical findings moved from `scientific-invariants.md`: 22.4 game-loop derivation with sources, APM usability from 2017 onward, MMR 83.6%-zero finding; each finding cites `01_04_apm_mmr_audit.md`

## [0.20.1] — 2026-04-06 (PR #49: fix/aoe2-acquisition-fixes)

### Added
- `src/rts_predict/aoe2/data/aoe2companion/acquisition.py` — download module for aoe2companion CDN: parses `api_dump_list.json`, filters to 4,147 targets (match parquets, leaderboard, profile, rating CSVs), size-based idempotency, atomic temp-file-then-rename downloads, JSON download log
- `src/rts_predict/aoe2/data/aoestats/acquisition.py` — download module for aoestats.io: parses `db_dump_list.json`, skips zero-match weeks (172 active weekly dumps → 344 files), MD5-based idempotency, deferred by default (requires `--force`), JSON download log
- `download` CLI subcommand in `aoe2/cli.py` with `source` positional arg (`aoe2companion`/`aoestats`), `--dry-run`, `--force`, `--log-interval` flags
- `src/rts_predict/aoe2/data/aoe2companion/__init__.py` and `aoestats/__init__.py` — make dataset dirs importable Python packages
- Co-located tests: `data/aoe2companion/tests/test_acquisition.py` (24 tests) and `data/aoestats/tests/test_acquisition.py` (20 tests), plus per-dataset `conftest.py` fixtures; CLI tests extended in `aoe2/tests/test_cli.py` (+7 tests)
- `src/rts_predict/aoe2/reports/aoe2companion/aoe2companion_download_report.md` — download run report: failure analysis, size-check fix rationale, retry results, final inventory
- `.gitkeep` files tracked in `raw/` subdirs and `api/` dirs for both datasets

### Fixed
- `aoe2companion/acquisition.py` — `_HTTP_HEADERS` User-Agent header added to bypass Cloudflare 403 blocking on CDN requests
- `aoe2companion/acquisition.py` — size check relaxed: accepts files where `actual >= expected` (CDN updates); `leaderboard`/`profile` categories bypass size check entirely (`expected_size=None`) since these are live files updated independently of the manifest
- `aoestats/acquisition.py` — same `_HTTP_HEADERS` User-Agent fix
- `aoestats/acquisition.py` — `_write_download_log` writes to `AOESTATS_RAW_DIR` (was `AOESTATS_DIR`)
- `aoe2companion/acquisition.py` — `_write_download_log` writes to `AOE2COMPANION_RAW_DIR` (was `AOE2COMPANION_DIR`)
- `.gitignore` — `raw/` subdirs: subdirectories un-ignored so `.gitkeep` negation works; `api/` dirs: all contents ignored except `.gitkeep`

## [0.20.0] — 2026-04-06 (PR #48: docs/manual-index-and-path-fixes)

### Added

- `docs/INDEX.md` — authoritative entry point for all project documentation, maps ML experiment lifecycle phases (0–11) to methodology manuals 01–06

### Changed

- `docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md` — replaced stale 12-point lifecycle listing with concise paragraph pointing to `docs/INDEX.md`
- `.claude/thesis-formatting-rules.yaml`, `thesis/WRITING_STATUS.md`, `README.md` — fixed stale `docs/PJAIT_THESIS_REQUIREMENTS.md` → `docs/thesis/PJAIT_THESIS_REQUIREMENTS.md`
- `CLAUDE.md` — added `Methodology manuals index` row to Key File Locations table
- `ARCHITECTURE.md` — added `Methodology manuals` row to Cross-cutting files table

## [0.18.4] — 2026-04-06 (PR #45: chore/per-dataset-reports)

### Added
- `src/rts_predict/sc2/reports/sc2egset/ROADMAP.md` — dataset-level roadmap (Phases 0–2) split from the former monolithic `SC2_THESIS_ROADMAP.md`
- `src/rts_predict/sc2/reports/ROADMAP.md` — game-level roadmap (Phases 3–10)
- `src/rts_predict/aoe2/reports/ROADMAP.md` — AoE2 game-level placeholder roadmap
- `src/rts_predict/aoe2/reports/aoe2companion/.gitkeep` and `aoestats/.gitkeep` — dataset report subdirectories
- `DATASET_REPORTS_DIR` constant in `sc2/config.py` pointing to `reports/sc2egset/`
- `AOE2COMPANION_REPORTS_DIR` and `AOESTATS_REPORTS_DIR` constants in `aoe2/config.py`

### Changed
- `audit.py` — artifact output defaults changed from `REPORTS_DIR` to `DATASET_REPORTS_DIR` (Phase 0 artifacts now written to `reports/sc2egset/`)
- `exploration.py` — same: Phase 1 artifacts now written to `reports/sc2egset/`
- `test_audit.py` and `test_exploration.py` — updated to monkeypatch `DATASET_REPORTS_DIR` instead of `REPORTS_DIR`
- `sc2/PHASE_STATUS.yaml` — replaced `roadmap:` with `dataset_roadmap:`, `game_roadmap:`, and `current_dataset:` fields
- `aoe2/PHASE_STATUS.yaml` — replaced `roadmap:` with split fields; `current_dataset: null`
- `ARCHITECTURE.md` — game package contract table updated for per-dataset report structure; "Adding a new game" steps renumbered
- `CLAUDE.md` — roadmap key file location split into `SC2 dataset roadmap` and `SC2 game roadmap`
- `.claude/agents/planner-science.md` — Read first section updated to per-file roadmap paths
- `thesis/THESIS_STRUCTURE.md` — roadmap reference updated to new split paths

### Removed
- `src/rts_predict/sc2/reports/SC2_THESIS_ROADMAP.md` — split into `sc2egset/ROADMAP.md` (Phases 0–2) and `ROADMAP.md` (Phases 3–10)
- `src/rts_predict/aoe2/reports/AOE2_THESIS_ROADMAP.md` — replaced by `ROADMAP.md` placeholder

## [0.18.3] — 2026-04-06 (PR #44: chore/per-dataset-reports)

### Added
- `src/rts_predict/sc2/data/tests/test_audit.py` — 9 new tests covering `run_full_path_a_ingestion`, `run_path_b_extraction`, and the `validate_path_a_b_join` audit-file cross-reference branch; `audit.py` now at 100% coverage

### Changed
- Migrated SC2 Phase 0–1 report artifacts into `src/rts_predict/sc2/reports/sc2egset/` per-dataset subdirectory (25 files moved via `git mv`)

## [0.18.2] — 2026-04-06 (PR #43: refactor/sc2-use-db-client)

### Added
- `src/rts_predict/common/tests/` — co-located test package for `common/` modules (`test_db.py`, `test_db_cli.py`), reaching 100% coverage on `db.py` and `db_cli.py`
- `src/rts_predict/sc2/tests/test_cli.py` — comprehensive CLI tests covering init, explore, audit, and no-command paths
- New tests across `data/tests/` to cover `audit.py` orchestrator, `exploration.py` helpers, `ingestion.py` exception paths, and `processing.py` DataFrame function
- `.claude/rules/git-workflow.md` — PR creation flow now includes mandatory coverage gate (≥95%, enforced via `fail_under = 95` in `pyproject.toml`)

### Changed
- `sc2/cli.py` — removed `_connect_db()` helper; all DB connections now use `DuckDBClient` context manager from `common/db.py`
- Root `tests/test_common_db.py` and `tests/test_common_db_cli.py` moved to co-located `common/tests/` (mirrors `sc2/` pattern)
- `pyproject.toml` — `[tool.coverage.report]`: added `fail_under = 95` threshold; added `exclude_lines` for `TYPE_CHECKING`, `__main__`, and `pragma: no cover` blocks

### Fixed

### Removed
- `_connect_db()` from `sc2/cli.py` (replaced by `DuckDBClient` context manager)
- `tests/test_common_db.py` and `tests/test_common_db_cli.py` at repo root (moved to co-located packages)

## [0.18.1] — 2026-04-06 (PR #42: chore/changelog-audit)

### Changed
- `CHANGELOG.md` — retroactive audit: 14 stale pending-PR headers replaced with actual PR numbers (#16–#29), `[0.18.0]` cut from `[Unreleased]` for PRs #39/#40/#41, PR #32 retroactive entry added inside `[0.16.2]`, `[0.7.0]` branch prefix corrected (`docs/` → `fix/`)
- `.claude/rules/git-workflow.md` — PR creation flow updated to write body to `.github/tmp/pr.txt` and use `gh pr create --body-file` instead of inline heredoc

## [0.18.0] — 2026-04-06 (PR #39: docs/thesis-formatting-rules, PR #40: docs/pjait-references, PR #41: chore/hook-logging)

### Added
- `.claude/thesis-formatting-rules.yaml` — machine-readable PJAIT formatting thresholds and rules extracted from `PJAIT_THESIS_REQUIREMENTS.md` §1
- `docs/PJAIT_THESIS_REQUIREMENTS.md` tracked in git; authoritative source for formatting and defense requirements
- `README.md` PJAIT institution name, degree, and key document references
- `thesis/WRITING_STATUS.md` formatting targets reference box
- `thesis/THESIS_STRUCTURE.md` PJAIT institution line

### Changed
- `scripts/hooks/log-subagent.sh` — robust per-field jq parsing (fixes field-shift anomaly), model name lookup from agent_type, token aggregation from transcript JSONL on SubagentStop, SessionOpen/SessionClose wrapper lines per session
- `.claude/rules/thesis-writing.md` — added cross-reference to formatting rules YAML
- `.claude/scientific-invariants.md` invariant #10: Nemenyi → Wilcoxon/Holm + Bayesian signed-rank
- `thesis/THESIS_STRUCTURE.md` §2.6 and §5.3.1: same Nemenyi → Wilcoxon/Holm + Bayesian update
- `thesis/chapters/02_theoretical_background.md`, `04_data_and_methodology.md`, `05_experiments_and_results.md`: skeleton comments updated

### Fixed

### Removed
- `docs/THESIS_REQUIREMENTS.md` — empty placeholder, superseded by `PJAIT_THESIS_REQUIREMENTS.md` at repo root

## [0.17.0] — 2026-04-06 (PR #38: docs/manual-patch)

### Added

- `THESIS_WRITING_MANUAL.md` §3.2: expanded statistical testing guidance explaining Nemenyi pool-dependence flaw, recommending Wilcoxon+Holm as frequentist best practice and Bayesian signed-rank (via `baycomp`) as complementary analysis
- `THESIS_WRITING_MANUAL.md` §8: new GenAI Transparency and Attribution section covering disclosure requirements, citation formats, Polish university context, and practical recommendations
- `THESIS_WRITING_MANUAL.md` References: 10 new reference link definitions (Benavoli 2016/2017, García & Herrera 2008, García 2010, baycomp, Corani 2017, KU Leuven GenAI, APA ChatGPT, Elsevier AI, UW AI guidelines)
- `DATA_EXPLORATION_MANUAL.md` §7: eighth pitfall "Not documenting AI-assisted exploration" with KU Leuven GenAI framework citation
- `DATA_EXPLORATION_MANUAL.md` References: `[kuleuven-genai]` reference link definition
- `FEATURE_ENGINEERING_MANUAL.md` §10: new "AI-assisted feature engineering disclosure" subsection on documenting AI tool usage and feature origin traceability
- `FEATURE_ENGINEERING_MANUAL.md` §7: new "A note on Bayesian model comparison and feature importance" subsection recommending `baycomp` for feature ablation evaluation
- `FEATURE_ENGINEERING_MANUAL.md` References: 4 new reference link definitions (Benavoli 2017, baycomp, KU Leuven GenAI, APA ChatGPT)

### Fixed

- `THESIS_WRITING_MANUAL.md` §9: replaced stale "Friedman + Nemenyi" bullet with updated "Friedman + Wilcoxon/Holm for multi-method comparison, with Bayesian signed-rank as complement"

## [0.16.6] — 2026-04-06 (PR #37: chore/aoe2-cli-shared-db)

### Added

- `DatasetConfig` frozen dataclass and `DuckDBClient` context manager in `common/db.py` — game-agnostic DuckDB connection with configurable resource pragmas
- Shared `add_db_subparser` / `handle_db_command` helpers in `common/db_cli.py`
- `sc2 db query <sql> [--format csv|json|table]` — ad-hoc DuckDB queries
- `sc2 db tables` / `sc2 db schema <table>` subcommands
- `aoe2` CLI entrypoint with same `db` subcommand group supporting `--dataset aoe2companion|aoestats`
- `DATASETS` / `DEFAULT_DATASET` registry added to both `sc2/config.py` and `aoe2/config.py`
- 20 new tests (9 + 6 + 3 + 2)

### Changed

- `common/CONTRACT.md` updated to include DB infrastructure as in-scope
- **Follow-up required:** `refactor/sc2-use-db-client` — migrate `_connect_db()` callers in `sc2/cli.py` to use `DuckDBClient` directly (deferred to keep this chore focused)

### Fixed

### Removed

## [0.16.5] — 2026-04-05 (PR #36: chore/init-aoe2-structure)

### Added

- AoE2 package directory tree under `src/rts_predict/aoe2/` mirroring the SC2 layout: `data/`, `data/tests/`, `reports/`, `tests/`, and per-source subdirs (`aoe2companion/`, `aoestats/`) each with `raw/`, `db/`, and `tmp/` directories
- `config.py` for the AoE2 package with path constants for both data sources (`AOE2COMPANION_*` and `AOESTATS_*`)
- `data/README.md` documenting the full data acquisition plan: source overview, per-source download tables (file patterns, counts, sizes, target directories), URL patterns, deferred/skip rationale, and download script requirements
- Per-source `raw/README.md` files describing subdir layout and data provenance for `aoe2companion/raw/` and `aoestats/raw/`
- `data/__init__.py`, `data/tests/__init__.py`, `tests/__init__.py` to make new subdirectories proper Python packages
- `AOE2_THESIS_ROADMAP.md` placeholder in `reports/` noting roadmap will be authored after SC2 pipeline reaches Phase 3
- Updated `PHASE_STATUS.yaml` `roadmap` field to reference `reports/AOE2_THESIS_ROADMAP.md`

### Changed

### Fixed

### Removed

- `src/rts_predict/aoe2/.gitkeep` placeholder (superseded by real content)

## [0.16.4] — 2026-04-05 (PR #35: chore/agent-observability)

### Added

- SubagentStart/Stop hooks (`scripts/hooks/log-subagent.sh`) logging agent events
  to `/tmp/rts-agent-log.txt` with session ID, agent ID, type, and transcript path
- `scripts/debug/find-session.sh` — finds session directories and correlates
  subagent transcript paths
- `color` and `permissionMode` fields in all 5 agent frontmatter files
- New Bash allow patterns in `settings.json`: `python3 -c *`, `echo *`, `date *`,
  `jq *`, `du *`, `sort *`, `python3 -m pytest*`

### Changed

- `scripts/debug/find-session.sh` updated to search `<session_id>/subagents/`
  for agent transcripts (correct Claude Code layout)
- `scripts/hooks/log-subagent.sh` hardened: single jq call, `// "unknown"`
  fallbacks on all fields
- `docs/AGENT_MANUAL.md` Troubleshooting section expanded with transcript paths,
  lint latency note, and write-guard CWD caveat

## [0.16.3] — 2026-04-05 (PR #34: chore/agent-infrastructure)

### Added

- 5-agent Claude Code architecture: `planner-science` (Opus), `planner` (Sonnet), `executor` (Sonnet), `reviewer` (Sonnet), `lookup` (Haiku) in `.claude/agents/`
- Project settings (`.claude/settings.json`) with permission allow/deny rules and hook configuration
- PostToolUse hook (`scripts/hooks/lint-on-edit.sh`) — auto-runs ruff on edited `.py` files
- PreToolUse hook (`scripts/hooks/guard-write-path.sh`) — write-path guardrail (repo=allow, home=ask, outside=block)
- Agent manual (`docs/AGENT_MANUAL.md`) with decision flowchart, workflows, and permission model docs
- Planning Protocol section in CLAUDE.md (read-only session enforcement, step-scoped execution)
- Agent Architecture reference table in CLAUDE.md

### Changed

### Fixed

### Removed

## [0.16.2] — 2026-04-05 (PR #33: chore/report-step-prefix)

### Changed

- Renamed all Phase 0 and Phase 1 report files to include step numbers: `{PHASE:02d}_{STEP:02d}_{name}.{ext}` (e.g. `00_source_audit.json` → `00_01_source_audit.json`, `01_apm_mmr_audit.md` → `01_04_apm_mmr_audit.md`)
- Updated `audit.py`, `exploration.py`, `test_exploration.py`, `SC2_THESIS_ROADMAP.md`, `research_log.md` to reference the new filenames

> **Note (retroactive — PR #32: chore/sc2egset-scripts, merged between #31 and #33):**
> This PR had no CHANGELOG entry at merge time. Changes: moved SC2EGSet data
> scripts from `src/rts_predict/sc2/data/` into `scripts/sc2egset/`; added
> `scripts/sc2egset/README.md`; enhanced `validate_map_names.sh` (66-line
> rewrite); renamed all scripts to drop the `sc2_` prefix.

## [0.16.1] — 2026-04-05 (PR #31: chore/consolidate-data-dirs)

### Added
- Dataset-scoped data directory scaffold: `data/sc2egset/{raw,staging,db,tmp}/`
- `_connect_db()` helper in `cli.py` with `mkdir` safety net for DB parent dirs
- `DUCKDB_TEMP_DIR.mkdir()` safety net in `ingestion.py` before DuckDB SET queries
- README.md files in `sc2egset/raw/` and `sc2egset/staging/` describing directory contents

### Changed
- All data paths in `config.py` routed through new `DATASET_DIR` constant (no more `~/duckdb_work/` or `~/Downloads/` hardcoded paths)
- `.gitignore` rewritten with dataset-aware patterns (`**/data/*/...`) for raw, staging, db, tmp
- `IN_GAME_MANIFEST_PATH` relocated from game root to `DATASET_DIR/staging/`
- Documentation updated: `dev-constraints.md`, `ARCHITECTURE.md`, `data/README.md`, `CLAUDE.md`

### Removed
- `IN_GAME_DB_PATH` constant (dead code, never imported)
- Hardcoded external paths (`~/duckdb_work/`, `~/Downloads/SC2_Replays/`) from config and docs

## [0.16.0] — 2026-04-04 (PR #30: refactor/mypy-and-test-cleanup)

### Added
- `tests/test_mps.py` rewritten as proper pytest: 5 test functions with `@pytest.mark.mps`, `skipif` guard, and session cleanup fixture (replaces standalone script)
- `mps` pytest marker registered in `pyproject.toml`

### Changed
- Fixed 37 mypy type errors across 8 files: `fetchone()` None guards on all DuckDB queries, `Generator` return types on yielding fixtures, explicit `rows` annotation in conftest

### Removed
- `tests/helpers.py` — unused `make_matches_df()` / `make_series_df()` (never imported)

## [0.15.1] — 2026-04-04 (PR #29: chore/archive-cleanup)

### Removed
- 16 archive files (run logs 01-09, ROADMAP_v1, methodology_v1, data_analysis_notes, gnn_collapse_log, sanity_validation, research_log, gnn_space_map) replaced by single `ARCHIVE_SUMMARY.md`

## [0.15.0] — 2026-04-04 (PR #28: docs/claude-config-restructure)

### Changed
- `CLAUDE.md` rewritten to 80 lines (from 277) — project identity, critical rules, and session workflow only; all detailed guidance moved to path-scoped rules
- `.claude/project-architecture.md` → `.claude/dev-constraints.md` — stripped ARCHITECTURE.md duplication, kept only non-obvious constraints (module ordering, legacy warnings, platform notes, external data paths)
- `.claude/ml-protocol.md` — added phase-activation guard (Phase 9+)
- `ARCHITECTURE.md` — updated 3 references from deleted files to new `.claude/rules/thesis-writing.md`

### Added
- `.claude/rules/python-code.md` — merged coding-standards + testing-standards + python-workflow (loads on `**/*.py` touch)
- `.claude/rules/thesis-writing.md` — merged thesis-writing + chat-handoff (loads on `thesis/**/*` touch)
- `.claude/rules/sql-data.md` — extracted SQL/data constraints from project-architecture (loads on `*/data/**/*.py` touch)
- `.claude/rules/git-workflow.md` — moved from `.claude/git-workflow.md` with PR template instructions preserved (loads on CHANGELOG/pyproject touch)

### Removed
- `.claude/coding-standards.md` — absorbed into `rules/python-code.md`
- `.claude/testing-standards.md` — absorbed into `rules/python-code.md`
- `.claude/python-workflow.md` — absorbed into `rules/python-code.md`
- `.claude/thesis-writing.md` — absorbed into `rules/thesis-writing.md`
- `.claude/chat-handoff.md` — absorbed into `rules/thesis-writing.md`
- `.claude/git-workflow.md` — absorbed into `rules/git-workflow.md`
- `.claude/aoe2-plan.md` — placeholder content, no longer needed
- `.claude/project-architecture.md` — replaced by `dev-constraints.md`

**Impact:** Always-loaded context reduced from 1,416 → 287 lines (−80%), 63,658 → 14,364 chars (−77%), 11 → 4 files (−64%). All content preserved in on-demand path-scoped rules.

## [0.14.3] — 2026-04-04 (PR #27: chore/slim-pr-template)

### Changed
- `.github/pull_request_template.md` — stripped to three sections (Summary, optional Motivation, Test plan) and Claude Code footer; removed type/scope checkboxes, changes table, ML experiment, data integrity and documentation checklists, and commit messages block
- `.claude/git-workflow.md` Step 7 — PR body guidance now explicitly references the template structure and provides a `gh pr create` heredoc example

## [0.14.2] — 2026-04-04 (PR #26: chore/sc2-data-compression-scripts)

### Added
- `src/rts_predict/sc2/data/sc2_rezip_data.sh` — re-zips each `*_data/` tournament
  directory back into a `*_data.zip` archive. Idempotent: skips tournaments where the
  zip already exists. Critical for local storage: 22 390 individual JSON files (~209 GB
  uncompressed) cause sustained Spotlight indexing and Defender real-time scanning on
  every file access, generating unnecessary IO load. Re-zipping compresses to ~12 GB
  and makes archives opaque to indexers. If data is ever moved to object storage
  (S3/GCS) this step is unnecessary as cloud storage is not subject to local IO overhead.
- `src/rts_predict/sc2/data/sc2_remove_data_dirs.sh` — removes `*_data/` source
  directories after re-zipping. Three guards required before any delete: (1) matching
  `.zip` exists, (2) zip is non-zero bytes, (3) real JSON file count in zip (excluding
  `._*` ditto resource-fork stubs) equals count in directory. Must be run after
  `sc2_rezip_data.sh` reports zero failures.
- `src/rts_predict/sc2/data/sc2_validate_map_name_mappings.sh` — validates that
  `map_foreign_to_english_mapping.json` is byte-identical across all tournament
  directories.

## [0.14.1] — 2026-04-04 (PR #25: chore/repo-reorganization)

> Note: Entries before v0.14.0 reference the old `sc2ml` package name and
> root-level `reports/` paths. See the repo reorganization in v0.14.0.

### Added
- **Step 2.5**: `src/rts_predict/sc2/PHASE_STATUS.yaml` — machine-readable SC2 phase progress
- **Step 2.5**: `src/rts_predict/aoe2/PHASE_STATUS.yaml` — AoE2 placeholder
- **Step 2.6**: `src/rts_predict/common/CONTRACT.md` — shared vs game-specific boundary rules
- **Step 2.6**: `src/rts_predict/common/__init__.py`, `src/rts_predict/aoe2/__init__.py` — placeholder modules
- **Step 2.7**: `thesis/chapters/REVIEW_QUEUE.md` — Pass 1 → Pass 2 thesis handoff tracker
- **Step 2.7**: `.claude/chat-handoff.md` — Claude Code → Claude Chat handoff protocol

### Changed
- **Step 1**: Moved Python package `src/sc2ml/` → `src/rts_predict/sc2/` via `git mv` (history preserved)
- **Step 1**: Moved `src/aoe2/` → `src/rts_predict/aoe2/` via `git mv`
- **Step 1**: Created `src/rts_predict/__init__.py` (namespace package docstring; `__version__` lives in `pyproject.toml` only per step 9 fixup)
- **Step 1**: Created `src/rts_predict/common/` placeholder directory
- **Step 2**: Moved SC2 phase artifacts (`reports/00_*`, `reports/01_*`, `sanity_validation.md`, `archive/`) → `src/rts_predict/sc2/reports/` via `git mv`
- **Step 2**: Renamed `SC2ML_THESIS_ROADMAP.md` → `SC2_THESIS_ROADMAP.md` during move
- **Step 2**: `reports/` now contains only cross-cutting `research_log.md`
- **Step 3**: Gitignored runtime artifacts (model `.joblib`/`.pt` files, logs, manifest) manually migrated from root `models/`, `logs/` → `src/rts_predict/sc2/models/`, `src/rts_predict/sc2/logs/`
- **Step 4**: Centralized `GAME_DIR`, `ROOT_DIR`, `REPORTS_DIR` in `config.py`; removed duplicate `REPORTS_DIR` definitions from `audit.py` and `exploration.py`
- **Step 5**: Renamed all `sc2ml` imports to `rts_predict.sc2` across all Python source and test files
- **Step 6**: `pyproject.toml` — package renamed to `rts_predict`, CLI entry point renamed from `sc2ml` to `sc2`, coverage source updated to `src/rts_predict`, version bumped to `0.14.0`
- **Step 7**: `.gitignore` — artifact patterns updated to game-scoped `src/rts_predict/*/` wildcards
- **Step 8**: All `.claude/*.md` documentation — paths, commands, and references updated to `rts_predict` namespace
- **Step 9**: `CLAUDE.md` — major rewrite; all paths, commands, layout, and progress tracking updated
- **Step 10**: `README.md` — commands, roadmap reference, `ARCHITECTURE.md` mention
- **Step 11**: `CHANGELOG.md` — this entry
- **Step 12**: `reports/research_log.md` — reorganization entry, `[SC2]` tags, path updates
- **Step 13**: `thesis/THESIS_STRUCTURE.md` — `SC2ML` → `SC2`, `reports/` path references updated
- **Step 14**: Removed empty legacy root directories `src/sc2ml/` and `src/aoe2/` (emptied by `git mv` in Step 1)
- **Step 15**: `poetry.lock` regenerated after package rename; `poetry install` verified clean install
- **Step 16**: `ARCHITECTURE.md` — new repo-root document describing package layout, game contract, version management, and thesis writing workflow
- **Step 17**: `test_ingestion.py` — replaced backslash line continuation in `with` statements with parenthesized form

## [0.13.3] — 2026-04-04 (PR #24: chore/rename-repo-rts-outcome-prediction)

### Changed
- Renamed repository from `sc2-ml` to `rts-outcome-prediction` for game-agnostic naming

## [0.13.2] — 2026-04-04 (PR #23: chore/remove-pre-roadmap-legacy-code)

### Removed
- Deleted `src/sc2ml/features/`, `src/sc2ml/gnn/`, `src/sc2ml/models/`, `src/sc2ml/analysis/` — pre-roadmap feature engineering, GNN, classical ML, and analysis modules (recoverable via git history; tagged `pre-roadmap-cleanup`)
- Deleted `tests/integration/` — integration tests for the removed modules
- Deleted `src/sc2ml/data/cv.py`, `src/sc2ml/validation.py`, and their associated test/helper files
- Deleted stale `src/sc2ml/logs/sc2_pipeline.log` and `processing_manifest.json`

### Changed
- `src/sc2ml/cli.py`: stripped to Phase 0–1 subcommands only (`init`, `audit`, `explore`); removed `run`, `ablation`, `tune`, `evaluate`, `sanity` subcommands and all associated pipeline functions
- `src/sc2ml/data/processing.py`: removed `create_temporal_split`, `validate_temporal_split`, `validate_data_split_sql` and their SQL constants
- `src/sc2ml/data/ingestion.py`: removed deprecated `slim_down_sc2_with_manifest`
- `src/sc2ml/config.py`: removed orphaned constants (`MANIFEST_PATH`, `TRAIN_RATIO`, `VAL_RATIO`, `TEST_RATIO`, `VETERAN_MIN_GAMES`, `PATCH_MIN_MATCHES`, `EXPANDING_CV_N_SPLITS`, `EXPANDING_CV_MIN_TRAIN_FRAC`)

## [0.13.1] — 2026-04-04 (PR #22: chore/housekeeping-workflow-and-roadmap)

### Changed
- **Workflow guard**: skip pytest/ruff/mypy on commits with no `.py` files staged
- **mypy scope**: broadened from `src/sc2ml/` to `src/` to cover future packages
- **Roadmap Phase 0**: restored full plan content (context, known issues, steps 0.1–0.9, artifacts, gate) above the "Status: complete" line
- **Roadmap Phase 1**: expanded context paragraph (references Phase 0 findings, adds `game_events_raw` and `match_player_map` as inputs); step 1.1 split into sub-sections A and B

### Added
- `src/aoe2/.gitkeep` — placeholder directory reserves the package slot for future AoE2 integration

## [0.13.0] — 2026-04-04 (PR #21: feature/phase-1-corpus-inventory)

### Added
- **Phase 1 corpus exploration** (`src/sc2ml/data/exploration.py`): 7-step exploration
  pipeline (Steps 1.1–1.7) producing 16 report artifacts — corpus summary, parse quality,
  duration distribution with plots, APM/MMR audit, patch landscape, event type inventory,
  and PlayerStats sampling regularity check
- **Exploration tests** (`src/sc2ml/data/tests/test_exploration.py`): 23 tests with
  synthetic DuckDB fixtures covering all steps and orchestrator (98% coverage)
- **CLI `explore` subcommand**: `sc2ml explore [--steps 1.1 1.3]` for selective step execution
- **tabulate dependency**: Required for DataFrame-to-markdown in report generation

### Changed

### Fixed

### Removed

## [0.12.0] — 2026-04-03 (PR #20: docs/thesis-infrastructure-invariants-v2)

### Added
- **Thesis directory structure** (`thesis/`): chapter skeletons (01–07), `THESIS_STRUCTURE.md` (section-to-phase mapping, ~300 lines), `WRITING_STATUS.md` (per-section status tracker), `references.bib` (~20 BibTeX entries), `figures/` and `tables/` directories
- **Thesis writing workflow** (`.claude/thesis-writing.md`): two-pass review process, critical review checklist (6 mandatory checks), inline flag system (`[REVIEW:]`, `[NEEDS CITATION]`, etc.), section-to-phase drafting schedule
- **Category F — Thesis writing** in `CLAUDE.md`: new work category with planning template, trigger words, progress tracking integration
- **Scientific invariants 7–10** (`.claude/scientific-invariants.md`): data field status with empirical backing (APM 97.5% usable 2017+, MMR 83.6% unusable), magic number ban, cross-game comparability protocol
- **SC2 game loop timing reference** (`reports/SC2ML_THESIS_ROADMAP.md`): 22.4 loops/sec derivation with landmarks table, citations (Blizzard s2client-proto, Vinyals et al. 2017)
- **Data utility script** (`src/sc2ml/data/sc2_nested_zip_remove.sh`): removes nested `_data.zip` files from SC2 replay directories
- **Reports archive stub** (`reports/archive/research_log.md`)

### Changed
- **Scientific invariants restructured** (`.claude/scientific-invariants.md`): reorganized from 6 to 10 numbered invariants with thematic sections (identity, temporal, symmetric, domain, data fields, reproducibility, cross-game)
- **Roadmap v2** (`reports/SC2ML_THESIS_ROADMAP.md`): Phase 0 marked complete with empirical gate results (22,390 replays, 62M tracker rows, 609M game event rows, 188 maps); Phase 1 expanded with empirical duration distribution emphasis and new steps (1.5 version landscape, 1.6 tracker event inventory); all phases now include explicit thesis section mapping
- **CLAUDE.md**: added Category F workflow, thesis writing trigger words, post-phase-gate thesis check in progress tracking, thesis writing references in project status

## [0.11.0] — 2026-04-03 (PR #19: docs/invariant-6-research-log)

### Added
- **Scientific invariant #6** (`.claude/scientific-invariants.md`): all analytical results must be reported alongside the literal SQL/Python code that produced them
- Phase 0 audit artifacts (Steps 0.1–0.9): all 8 report files in `reports/00_*`

### Changed
- **Research log Phase 0 entry rewritten** (`reports/research_log.md`): every finding now includes the exact SQL query or Python code per invariant #6; APM/MMR analysis expanded with per-year and per-league breakdown tables; map count corrected from 189 → 188
- `ingestion.py` glob patterns unified to `*.SC2Replay.json` (was `*/data/*.SC2Replay.json` in `audit_raw_data_availability`, `slim_down_sc2_with_manifest`, `_collect_pending_files`)

## [0.10.0] — 2026-04-03 (PR #18: feat/phase-0-ingestion-audit)

### Added
- **Phase 0 ingestion audit module** (`src/sc2ml/data/audit.py`): 9 audit functions mapping to roadmap steps 0.1–0.9 — source file audit, tournament name validation, replay_id spec, Path A smoke test (in-memory DuckDB), full Path A ingestion, Path B extraction, Path A↔B join validation, map translation coverage
- **`raw_enriched` view** in `processing.py`: adds `tournament_dir` and `replay_id` computed columns to `raw` table via `CREATE OR REPLACE VIEW`; `flat_players` now reads from `raw_enriched` instead of `raw`
- **`create_raw_enriched_view()`** function in `processing.py`, called during `init_database` pipeline
- **`audit` CLI subcommand**: `poetry run python -m sc2ml.cli audit [--steps 0.1 0.2 ...]` runs Phase 0 audit steps against real data
- **`run_phase_0_audit()` orchestrator** accepting optional step list for selective execution
- 14 new tests: `test_audit.py` (10 tests covering all public audit functions), `TestCreateRawEnrichedView` in `test_processing.py` (4 tests)

### Changed
- `_FLAT_PLAYERS_VIEW_QUERY` now reads from `raw_enriched` instead of `raw`; `tournament_name` derived from `tournament_dir` column instead of inline `split_part()`
- `init_database()` in `cli.py` now calls `create_raw_enriched_view(con)` between `move_data_to_duck_db` and `load_map_translations`
- `conftest.py` synthetic filenames updated to use 32-char hex prefixes (`SYNTHETIC_REPLAY_IDS`) matching real replay naming; APM/MMR set to 0 (dead fields)
- Integration test fixtures and sanity validation fixtures updated to call `create_raw_enriched_view` before `create_ml_views`

## [0.9.0] — 2026-04-03 (PR #17: refactor/data-schemas-sql-extraction)

### Changed
- **`schemas.py` extracted** (`src/sc2ml/data/schemas.py`): `PLAYER_STATS_FIELD_MAP`, `TRACKER_SCHEMA`, `GAME_EVENT_SCHEMA`, `METADATA_SCHEMA` moved out of `ingestion.py`; re-exported from `ingestion` for backward compatibility
- **SQL queries extracted in `processing.py`**: all inline SQL moved to module-level `_QUERY` constants (`FLAT_PLAYERS_VIEW_QUERY`, `MATCHES_FLAT_VIEW_QUERY`, `MATCHES_WITH_SPLIT_QUERY`, `MATCHES_WITHOUT_SPLIT_QUERY`, `YEAR_DISTRIBUTION_QUERY`, `CHRONOLOGICAL_SPLIT_QUERY`, `SERIES_ASSIGNMENT_QUERY`, `SERIES_OTHER_PERSPECTIVE_QUERY`, `TOURNAMENT_GROUPING_QUERY`, `MATCH_SPLIT_CREATE_QUERY`, `SPLIT_STATS_QUERY`, `SPLIT_BOUNDARIES_QUERY`, `TOURNAMENT_CONTAINMENT_QUERY`, `SERIES_INTEGRITY_QUERY`, `YEAR_DIST_PER_SPLIT_QUERY`); parameterized f-string in `get_matches_dataframe` converted to `?` binding
- **SQL queries extracted in `ingestion.py`**: `DUCKDB_SET_QUERIES`, `RAW_TABLE_CREATE_QUERY`, `TRACKER_EVENTS_TABLE_QUERY`, `PLAYER_STATS_VIEW_QUERY`, `GAME_EVENTS_TABLE_QUERY`, `MATCH_PLAYER_MAP_TABLE_QUERY` extracted to module-level constants; `PLAYER_STATS_VIEW_QUERY` built once at module level via `_build_player_stats_view_query()`
- **`slim_down_sc2_with_manifest` deprecated** in `ingestion.py` and `samples/process_sample.py`: `DeprecationWarning` added, docstrings updated with `.. deprecated::` directive pointing to `run_in_game_extraction()`
- **`cv.py` docstrings** converted from NumPy style to Google style per coding standards
- **`data/__init__.py`**: `schemas` added to submodules docstring

## [0.8.0] — 2026-04-03 (PR #16: chore/consolidate-base)

### Added
- **Evaluation infrastructure** (`models/evaluation.py`): `compute_metrics` (accuracy, AUC-ROC, Brier, log loss), `bootstrap_ci` (95% CI via 1000 bootstrap iterations), `calibration_curve_data`, `mcnemar_test` (exact binomial + chi-squared), `delong_test` (fast DeLong AUC comparison), `evaluate_model` (full eval with CIs + per-matchup + veterans), `compare_models` (pairwise statistical tests), `run_permutation_importance`
- **Baseline classifiers** (`models/baselines.py`): `MajorityClassBaseline`, `EloOnlyBaseline`, `EloLRBaseline` — all with `predict_proba` for probability-based metrics
- **Feature ablation runner** (`evaluation.py:run_feature_ablation`): trains LightGBM per group subset (A, A+B, ..., A+B+C+D+E), reports marginal lift per step
- **Expanding-window temporal CV** (`data/cv.py`): `ExpandingWindowCV` with series-aware boundary snapping, sklearn `BaseCrossValidator` compatible
- **Optuna tuning** (`models/tuning.py`): `tune_lgbm_optuna`, `tune_xgb_optuna` (Bayesian optimization, 200 trials), `tune_lr_grid` (grid search over C + penalty)
- **SHAP analysis** (`analysis/shap_analysis.py`): `compute_shap_values` (TreeExplainer/LinearExplainer), `plot_shap_beeswarm`, `plot_shap_per_matchup` (6 matchup types), `shap_feature_importance_table`
- **Error analysis** (`analysis/error_analysis.py`): `classify_error_subgroups` (mirrors, upsets, close Elo, short/long games), `error_subgroup_report`
- **Patch drift experiment** (`evaluation.py:run_patch_drift_experiment`): train on old patches, test on new, per-patch accuracy breakdown
- **Reporting** (`models/reporting.py`): `ExperimentReport` with `.to_json()` and `.to_markdown()` for thesis-ready reports
- **CLI subcommands**: `sc2ml ablation`, `sc2ml tune`, `sc2ml evaluate`
- `matchup_type` column preserved through feature engineering for per-matchup analysis
- `p1_race`/`p2_race` added to `_METADATA_COLUMNS` for safe ablation without Group C
- Config constants: `BOOTSTRAP_N_ITER`, `BOOTSTRAP_CI_LEVEL`, `CALIBRATION_N_BINS`, `RESULTS_DIR`, `EXPANDING_CV_N_SPLITS`, `EXPANDING_CV_MIN_TRAIN_FRAC`, `OPTUNA_N_TRIALS_LGBM`, `OPTUNA_N_TRIALS_XGB`, `LR_GRID_C`, `LR_GRID_PENALTY`
- `@pytest.mark.slow` marker registered in `pyproject.toml`
- `optuna` and `shap` dependencies
- 75 new tests: `test_evaluation.py` (22), `test_baselines.py` (18), `test_cv.py` (13), `test_ablation.py` (6), `test_analysis/test_error_analysis.py` (9), `test_analysis/test_shap_analysis.py` (7)
- **Phase 0 sanity validation** (`validation.py`): 28 automated checks across 5 sections — DuckDB view sanity (§3.1), temporal split integrity (§3.2), feature distribution checks (§3.3), leakage & baseline smoke tests (§3.4), known issues verification (§3.5)
- `SanityCheck`/`SanityReport` result containers with `.summary` property
- `run_full_sanity()` aggregator running all Phase 0 checks
- `sc2ml sanity` CLI subcommand for real-data validation (writes `reports/sanity_validation.md`)
- `@pytest.mark.sanity` marker registered in `pyproject.toml`
- 29 new tests in `test_sanity_validation.py` (25 passing, 4 skipped on synthetic data)
- **Scientific invariants** (`.claude/scientific-invariants.md`): thesis methodology constraints read-before-any-work
- **Thesis roadmap** (`reports/SC2ML_THESIS_ROADMAP.md`): authoritative phase-by-phase execution plan
- **Co-located tests**: all package tests moved next to source (`src/sc2ml/*/tests/`)
- `tests/integration/` directory for cross-package integration tests
- Data samples: `SC2EGSet_datasheet.pdf`, `README.md`, shell extraction scripts

### Changed
- `train_and_evaluate_models()` now returns `(dict[str, Pipeline], list[ModelResults])` instead of just pipelines
- `classical.py` refactored: model definitions extracted to `_build_model_pipelines()`, evaluation delegated to `evaluation.py`
- `.claude/` configuration files rewritten: `project-architecture.md`, `ml-protocol.md`, `testing-standards.md`, `git-workflow.md`, `coding-standards.md`
- `CLAUDE.md` restructured with scientific invariants mandate, progress tracking, end-of-session checklist
- `README.md` rewritten with project overview and documentation index

### Removed
- Duplicate root-level tests (`tests/test_*.py`) — replaced by co-located versions under `src/`
- Superseded reports: `reports/ROADMAP.md`, `reports/methodology.md`, `reports/test_plan.md`
- Root-level test helpers (`tests/helpers_*.py`)

### Known Issues
- 16 test errors + 1 failure in `test_processing.py` temporal split tests — fixture missing `flat_players` table; will be rewritten in Phase 0
- 1 GNN prediction quality test failure — expected, GNN is deprioritized
- 41 mypy errors — pre-existing `fetchone()` return type issues in DuckDB code

## [0.7.0] — 2026-04-03 (PR #15: fix/data-pipeline-integrity)

### Documentation Refactoring
- **Unified documentation structure**: eliminated redundancy across 12+ markdown files. One authoritative source per topic.
- Moved `src/sc2ml/methodology.md` → `reports/methodology.md` (thesis specification doesn't belong in Python source tree)
- Moved `test_plan.md` → `reports/test_plan.md` (planning doc, not a root-level file)
- Archived `src/sc2ml/data/plan.md` → `reports/archive/data_analysis_notes.md` (superseded by methodology.md)
- Deleted `src/sc2ml/action_plan.md` — execution checklist folded into ROADMAP.md
- **ROADMAP.md** is now the single progress tracker: added Phase 0→1 execution checklist with exact CLI commands, §3.6 test coverage tracking, fixed cross-references
- **`.claude/project-architecture.md`** rewritten: fixed 6+ factual errors (deleted modules referenced as current, wrong feature count 45→66, outdated tuning description, GNN not marked as deprioritized)
- **CLAUDE.md** updated: added mandatory "Progress Tracking" section, added `reports/methodology.md`, `reports/ROADMAP.md`, `reports/test_plan.md` to guidelines table, added git-workflow reference to end-of-session checklist
- **README.md** replaced: was empty, now has project overview with documentation index

### Critical Bug Fixes (discovered during Phase 0 sanity validation)

#### Elo System — All Ratings Were 1500.0 (Complete Failure)
- **Root cause:** `group_a_elo.py` used a two-pass algorithm where Phase 1 recorded every player's Elo *before* Phase 2 updated anything. Result: all pre-match Elo values were the initialization constant (1500.0), producing zero variance and a useless Elo baseline (48.8% accuracy — worse than random).
- **Fix:** Merged into a single chronological pass — snapshot pre-match Elo, then update immediately, processing each unique match_id once via dedup guard. Elo now actually reflects player skill trajectories.
- **Impact:** All Elo-derived features (`p1_pre_match_elo`, `p2_pre_match_elo`, `elo_diff`, `expected_win_prob`) were non-functional across all prior pipeline runs. Historical run results in `reports/archive/` were achieved *without any Elo signal*.

#### H2H Feature Self-Leakage
- **Root cause:** `_compute_h2h()` in `group_d_form.py` used `expanding_sum` grouped by a canonical player pair key. In the dual-perspective layout (2 rows per match), the second row's expanding window included the first row's target value — which is the same match's result from the other perspective.
- **Fix:** H2H features now computed on deduplicated matches (one row per match_id) using a canonical-perspective target, then mapped back to both rows. Canonical ordering via `p1_name < p2_name`.
- **Impact:** `h2h_p1_winrate_smooth` had 0.62 correlation with target (detected by sanity check §3.4). This would have inflated model accuracy via leakage.

#### Temporal Split — Tournament Boundary Violations
- **Root cause:** `create_temporal_split()` split at series-level boundaries, but multiple tournaments can overlap chronologically (e.g., IEM Katowice 2024 qualifiers ran Dec 2023–Feb 2024, overlapping with ESL Winter Finals Dec 15–18). Result: 3 tournaments were split across train/val or val/test, creating temporal leakage and violating the principle that tournament context should not leak between splits.
- **Fix:** Split now operates at **tournament-level boundaries**. All matches from the same tournament (identified by source directory name during ingestion) are guaranteed to be in the same split. Series containment follows automatically since all series are within a tournament.
- **Impact:** Train/Val and Val/Test boundaries now have clean gaps (23 days and 3.5 months respectively). Previously had overlaps of 10 minutes and 2 months.
- **Observations from real data:** 66 tournaments spanning 2016–2024, 22,390 replays ingested (up from 22,103). Final split: train=17,991 (80.4%), val=3,520 (15.7%), test=858 (3.8%).

#### Data Quality — Team Games and Brood War Replays
- **Root cause:** `flat_players` view included non-1v1 matches (team games with 4-9 players) and Brood War exhibition replays (races: BWPr, BWTe, BWZe). These produced matches with !=2 rows, corrupting the dual-perspective assumption.
- **Fix:** Added two filters to `flat_players` view: (1) exclude BW races (`race NOT LIKE 'BW%'`), (2) restrict to 1v1 matches via subquery (`HAVING COUNT(*) = 2` on Win/Loss players per match). Affected: 13 team game replays (HSC XVI, TSL5, EWC) + 1 BW exhibition match.

### Other Changes
- Removed `series_length_so_far` feature — perfectly correlated with `series_game_number` (literally `game_number - 1`), provided zero additional information
- `validate_temporal_split()` now checks tournament containment in addition to series containment
- LightGBM sanity checks run in subprocess isolation when PyTorch is loaded (avoids dual-OpenMP segfault on macOS)
- `check_elo_baseline` threshold relaxed for small synthetic datasets (10 test rows with random data can't reliably beat 50%)
- Synthetic test fixtures updated to use chronological tournament assignment (20 tournaments, 5 matches each) instead of random assignment, required by tournament-level splitting

### Phase 0 Sanity Results (first run on real data — 16/25 passed)
Initial sanity run identified all the bugs above. Key observations:
- **22,390 replays** ingested across 66 tournaments (2016-2024)
- **1,044 unique players** in the dataset
- Target balance: ~50% (confirmed by dual-perspective layout)
- Historical features have no NaN (cold-start handling works)
- No series spans multiple splits
- Race dummies are int (not bool) — previously flagged issue was already fixed
- Expanding-window aggregates correctly exclude current match
- Feature count: 75 columns from 5 groups (slightly above the 66 expected — needs audit)
- **Next session:** proper source data analysis before running experiments

## [0.6.0] — 2026-04-02 (PR #7: test/gnn-diagnostics)

### Added
- **GNN diagnostic test suite** (`tests/test_gnn_diagnostics.py`): 14 tests across 6 groups confirming GATv2 majority-class collapse root causes — no `pos_weight` in BCE loss, edge feature scaler leak (fit on full dataset), hard 0.5 threshold
- `@pytest.mark.gnn` marker registered in `pyproject.toml` (skip with `-m "not gnn"`)
- `setup_logging()` now called in `run_pipeline()` for reliable file logging when invoked outside `main()`

## [0.5.0] — 2026-04-02 (PR #6: fix/pipeline-coherence)

### Added
- `init_database()` function and CLI `init` subcommand for one-step database setup from raw replays
- CLI argparse with `init [--force]` and `run` subcommands (backward-compatible: bare invocation still runs pipeline)
- `game_version` column in `flat_players` and `matches_flat` SQL views (from `metadata.gameVersion`)
- 12 integration smoke tests (`tests/test_integration.py`) verifying the full chain: ingestion → processing → features → model training
- Race normalization and game version parsing tests in data and feature test suites

### Fixed
- **Race name mismatch**: SQL view now normalizes abbreviated race names (`Terr`→`Terran`, `Prot`→`Protoss`) so one-hot columns match GNN visualizer and test expectations
- **Validation set discarded**: `train_and_evaluate_models()` now accepts optional `X_val`/`y_val`; XGBoost and LightGBM use it for early stopping; val accuracy reported for all models
- **Patch version always zero on real data**: Group E now uses `game_version` (`"3.1.1.39948"`) for `patch_version_numeric` instead of plain `data_build` (`"39948"`)
- **Compat fallback crash**: `cli.py` fallback path now drops string columns via `select_dtypes(include='number')` before passing to sklearn
- **t-SNE `n_iter` deprecation**: Updated to `max_iter` for scikit-learn 1.6+

### Changed
- `cli.py` refactored: pipeline logic extracted to `run_pipeline()`, `init_database()` added, imports now include ingestion/processing functions

## [0.4.0] — 2026-04-01 (PR #5: refactor/feature-groups-ablation)

### Added
- **Feature groups A–E** implementing methodology Section 3.1 for incremental ablation:
  - Group A (`group_a_elo.py`): Dynamic K-factor Elo ratings (refactored from `elo.py`)
  - Group B (`group_b_historical.py`): Historical aggregates + new variance features (`hist_std_apm`, `hist_std_sq`)
  - Group C (`group_c_matchup.py`): Race encoding, spawn distance, map area + new map×race interaction winrate
  - Group D (`group_d_form.py`): **New** — win/loss streaks, EMA stats, activity windows (7d/30d), head-to-head records
  - Group E (`group_e_context.py`): **New** — patch version numeric, tournament match position, series game number
- `build_features(df, groups=FeatureGroup.C)` API for composable group selection and ablation
- `split_for_ml()` consuming the series-aware 80/15/5 split from `data/processing.py`
- `FeatureGroup` enum and `get_groups()` for ablation protocol (methodology Section 7.1)
- Feature group registry (`registry.py`) with lazy-loaded compute functions
- Backward-compatible wrappers in `compat.py` (`perform_feature_engineering`, `temporal_train_test_split`)
- Config constants: `EMA_ALPHA`, `ACTIVITY_WINDOW_SHORT`, `ACTIVITY_WINDOW_LONG`, `H2H_BAYESIAN_C`
- 73 new tests in `tests/test_features/` covering all groups, common primitives, registry, ablation, and compat
- `tests/helpers.py`: `make_series_df()` for Group E testing; deterministic win streaks for Player_0
- `tests/helpers_classical.py`: isolated worker for classical model reproducibility (no torch import)
- `pytest-cov` and `coverage` dev dependencies
- **Path B in-game event extraction pipeline** in `ingestion.py`: `audit_raw_data_availability()`, `extract_raw_events_from_file()`, `save_raw_events_to_parquet()`, `run_in_game_extraction()`, DuckDB loaders with `player_stats` view and `match_player_map` table
- `PLAYER_STATS_FIELD_MAP` — 39 `scoreValue*` → snake_case field mappings for tracker events
- Temporal split management in `processing.py`: `assign_series_ids()`, `create_temporal_split()`, `validate_temporal_split()`
- `player_id` column added to `flat_players` and `matches_flat` SQL views
- `get_matches_dataframe()` now accepts optional `split` parameter for filtered queries
- Config constants: `IN_GAME_DB_PATH`, `IN_GAME_PARQUET_DIR`, `IN_GAME_MANIFEST_PATH`, `IN_GAME_WORKERS`, `IN_GAME_BATCH_SIZE`, `TRAIN_RATIO`, `VAL_RATIO`, `TEST_RATIO`, `SERIES_GAP_SECONDS`
- `pyarrow` dependency for Parquet-based event storage
- 42 new tests in `src/sc2ml/data/tests/` covering ingestion and processing pipelines
- Data pipeline documentation: `src/sc2ml/data/README.md`, methodology notes

### Changed
- `cli.py` now uses `build_features()` + `split_for_ml()` instead of monolithic `perform_feature_engineering()` + `temporal_train_test_split()`
- `temporal_train_test_split()` now emits `DeprecationWarning` (use `split_for_ml()` instead)
- Test imports updated: `from sc2ml.features import ...` replaces `from sc2ml.features.engineering import ...`
- `slim_down_sc2_with_manifest()` now defaults to `dry_run=True` for safety

### Fixed
- **Dual-OpenMP segfault on macOS (LightGBM + PyTorch)**: LightGBM ships Homebrew `libomp.dylib`, PyTorch bundles its own `libomp.dylib`. Loading both in the same process causes a segfault at shutdown during OpenMP thread pool teardown. Fix: classical model reproducibility tests now run in a `multiprocessing.spawn` child process via `helpers_classical.py` (which never imports torch), fully isolating the two runtimes. GNN test adds `gc.collect()` + `torch.mps.empty_cache()` cleanup per `test_mps.py` pattern.

### Removed
- `features/elo.py` and `features/engineering.py` (replaced by group modules + compat wrappers)

## [0.3.0] — 2026-03-31 (PR #4: refactor/break-down-claude-md)

### Added
- `.claude/` sub-files: `python-workflow.md`, `testing-standards.md`, `coding-standards.md`, `git-workflow.md`, `ml-protocol.md`, `project-architecture.md`

## [0.2.0] — 2026-03-30 (PR #3: refactor/package-structure)

### Changed
- **Reorganized into `src/sc2ml/` package** with four subpackages: `data/`, `features/`, `models/`, `gnn/` — proper Python src layout replacing flat root-level modules
- Renamed modules to avoid namespace redundancy (e.g. `data_ingestion.py` → `sc2ml.data.ingestion`)
- Updated `pyproject.toml` to src layout (`packages = [{include = "sc2ml", from = "src"}]`)
- Replaced hardcoded `ROOT_PROJECTS_DIR` path with `Path(__file__)` derivation in `config.py`
- Moved logging setup from module-level side effect to `setup_logging()` function in `cli.py`
- Fixed duplicate `perform_feature_engineering()` call in pipeline orchestrator
- Replaced string type annotations with proper `TYPE_CHECKING` imports in GNN modules
- Archived legacy run reports (`01_run.md`–`09_run.md`) to `reports/archive/`
- Translated all Polish comments and log strings to English across all 13 Python modules
- Added type hints to all function signatures (parameters and return types) in all modules
- Extracted 60+ magic numbers into named constants in `config.py`

### Added
- `src/sc2ml/__init__.py` with package version `0.2.0`
- `[project.scripts]` entry point: `sc2ml = "sc2ml.cli:main"`
- `tests/conftest.py` for pytest configuration
- `tests/helpers.py` for shared test utilities (replaces `tests/fixtures.py`)
- `[tool.pytest.ini_options]` in `pyproject.toml`
- `pyproject.toml` with Poetry dependency management
- `config.py` with all centralized constants
- `tests/` directory with test suite (data validation, feature engineering, graph construction, model reproducibility)
- CLAUDE.md, CHANGELOG.md, and research log

### Removed
- Root-level `__init__.py` (incorrect — root is not a package)
- `tests/fixtures.py` (absorbed into `tests/helpers.py`)
- `sys.path.insert()` hack from all test files
- Unused imports in `cli.py` (data ingestion functions not called in current pipeline)
- Dead commented-out legacy `main()` function block (~100 lines)

### Fixed
- Test fixture now drops non-numeric columns (e.g. `data_build`) before passing to sklearn
- Ruff import sorting and unused import warnings resolved across all modules

## [0.1.0] — 2026-03-30 (Baseline)

### Added
- SC2 data ingestion pipeline with manifest tracking (`data_ingestion.py`)
- DuckDB-based data processing with SQL views (`data_processing.py`)
- Feature engineering with 45+ features and Bayesian smoothing (`ml_pipeline.py`)
- Custom ELO rating system with dynamic K-factor (`elo_system.py`)
- Classical ML baselines: Logistic Regression, Random Forest, Gradient Boosting, XGBoost, LightGBM (`model_training.py`)
- Random Forest hyperparameter tuning via RandomizedSearchCV (`hyperparameter_tuning.py`)
- GATv2-based Graph Neural Network for edge classification (`gnn_model.py`, `gnn_pipeline.py`, `gnn_trainer.py`)
- Node2Vec embedding pipeline (`node2vec_embedder.py`)
- t-SNE visualization of GNN embeddings (`gnn_visualizer.py`)
- Pipeline orchestrator with configurable model selection (`main.py`)
- Execution reports documenting 9 pipeline runs (`reports/`)
