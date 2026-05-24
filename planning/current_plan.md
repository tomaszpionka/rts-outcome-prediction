---
category: A
branch: feat/sc2egset-02-01-03-history-scaffold
title: "SC2EGSet Step 02_01_03 — notebook scaffold + ONE validation module (history-enriched pre_game tranche)"
phase: "02 — Feature Engineering"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
step_number: "02_01_03"
dataset: "sc2egset"
source_artifacts:
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md lines 2274-2523 (Step 02_01_03 yaml block; merged PR #239 at master f378f6f4ac37783e08dfcbe922d0c60b522a272a)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv rows 7-12 (the 6 history_enriched_pre_game families)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv rows 7-12 (per-family §10 verdicts)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/validate_pre_game_feature_materialization.py (644 LOC tranche-1 precedent to mirror)"
  - "sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.py (347 LOC scaffold precedent to mirror)"
  - "tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_pre_game_feature_materialization.py (31 test functions, 16 classes, precedent)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv (PR #234 tranche-1 adjudication output; format precedent for the deferred tranche-2 adjudication)"
  - "reports/specs/02_00_feature_input_contract.md §3.3 strict-< rule, §5.4 SC2 IN_GAME_HISTORICAL telemetry-scope decision"
  - "reports/specs/02_01_leakage_audit_protocol.md §2.1/§2.2/§2.3/§2.4"
  - "reports/specs/02_02_feature_engineering_plan.md §6.2 (6 history families row 5 cross_region; row 6 in_game_history_aggregate IN_GAME_HISTORICAL retention)"
  - "reports/specs/02_03_temporal_feature_audit_protocol.md §6.2 history_enriched_pre_game prediction-setting rules; D1-D15"
  - ".claude/scientific-invariants.md (I3 temporal+normalization; I5 symmetry; I6 SQL provenance; I7 no magic numbers; I8 cross-game)"
  - ".claude/ml-protocol.md (three leakage failure modes)"
  - ".claude/rules/data-analysis-lineage.md (non-batching rule; halt-before-artifact)"
invariants_touched: [I3, I5, I6, I7, I8, I9, I10]
version_bump_planned: "3.71.0 → 3.72.0 (minor; feat-family; applies to the future Layer-2 execution PR only — Layer-1 planning PR is version-neutral)"
critique_required: true
critique_path: "planning/current_plan.critique.md"
base_ref: f378f6f4ac37783e08dfcbe922d0c60b522a272a
date: 2026-05-24
planner_model: claude-opus-4-7[1m]
non_batching_sequence_position: "Step 2 of 9 (scaffold + ONE validation module) — follows merged ROADMAP-only stub (PR #239); precedes future tranche-2 source/anchor/cold-start adjudication, materialization-execution plan, materialization-execution, audit, and closure."
gate_reviewer: "reviewer-adversarial (Category A pre-execution gate)"
planning_pr: "PR #240"
planning_pr_scope: "Layer-1 (2 files only) — planning/current_plan.md + planning/current_plan.critique.md. NO scaffold, NO validator, NO test, NO source/notebook/artifact, NO pyproject bump, NO CHANGELOG entry, NO planning/INDEX.md archive, NO status YAML flip, NO research_log entry."
future_execution_pr_scope: "Layer-2 (9 files: 7 deliverable + 2 inherited planning) — sandbox/.../02_01_03_history_enriched_pre_game_feature_materialization.{py,ipynb} (scaffold pair) + src/.../validate_history_enriched_pre_game_materialization.py + tests/.../test_validate_history_enriched_pre_game_materialization.py + planning/INDEX.md (archive PR #239 → promote Layer-2) + CHANGELOG.md (new [3.72.0] block) + pyproject.toml (3.71.0 → 3.72.0) + planning/current_plan.md (persisted from Layer-1) + planning/current_plan.critique.md (persisted from Layer-1). NO materialization, NO artifact, NO status YAML flip, NO research_log, NO Phase 03, NO Step 02_01_04, NO baseline modeling."
---

## Scope

This is a **Layer-1 planning PR**. It commits ONLY two files:

- `planning/current_plan.md` (this document)
- `planning/current_plan.critique.md` (produced by reviewer-adversarial in a separate dispatch)

This plan describes the future **Layer-2 execution PR** on branch
`feat/sc2egset-02-01-03-history-scaffold`. The Layer-2 execution PR will
have a **9-file final tracked diff**: **7 execution files** (a jupytext-paired
scaffold notebook .py + .ipynb, a validation module under `src/rts_predict/`,
a mirrored test file, and three repo-housekeeping updates `planning/INDEX.md` +
`CHANGELOG.md` + `pyproject.toml`) **plus the 2 inherited planning files**
(`planning/current_plan.md` + `planning/current_plan.critique.md` carried
forward from this Layer-1 PR). The Layer-2 PR
performs the non-batching sequence step 2 ("Notebook scaffold + one
validation module") for SC2EGSet Step 02_01_03 (history-enriched pre_game
tranche; 6 families).

The Layer-2 execution PR is explicitly **scaffold-only**. It does NOT
materialize any feature value, does NOT execute projection SQL against the
DuckDB, does NOT write any artifact under
`reports/artifacts/02_01_03/`, does NOT update `STEP_STATUS.yaml` /
`PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml`, does NOT append a
`research_log.md` entry, does NOT close Step 02_01_03, does NOT begin Step
02_01_04 (the in_game_snapshot tranche), does NOT begin Phase 03, does NOT
patch any cleaning-layer YAML, does NOT patch any spec, and does NOT
re-execute the §10 verdict audit or the CROSS-02-01 leakage audit.

The 11+ design decisions that the scaffold + validator MUST encode (and
the falsifiers that enforce each) are enumerated in the **Execution Steps**
section. The decisions explicitly **deferred** to future PRs (cross-region
adjudication policy, rating reconstruction model choice, materialization
SQL, post-materialization CROSS-02-01 audit, closure) are enumerated in
**Open Questions**.

## Problem Statement

The merged PR #239 inserted the Step 02_01_03 ROADMAP-stub block (lines
2274-2523 of `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`)
under Pipeline Section 02_01. The block declares the 6 allowed
`history_enriched_pre_game` family rows from the closed 02_01_01 registry
CSV, the strict `ph.details_timeUTC < target.started_at` history filter, the
G-CS-2..6 cold-start gates, the G-L-1/3/4/7 halt predicates, the
`continue_predicate` requiring a re-executed §10 audit (or a non-vacuous
justification for skipping it), and the cross-region adjudication
**explicitly deferred** to a tranche-2 source/anchor/cold-start adjudication
PR analogous to PR #234.

The next step in the non-batching sequence (`.claude/rules/data-analysis-lineage.md`
sequence step 2) is "Notebook scaffold + one validation module". The 02_01_02
precedent is unambiguous: PR #233 produced a 347-LOC jupytext-paired scaffold
notebook plus a 644-LOC validator module with 11 falsifier helpers, and the
mirrored test file with 31 test functions across 16 classes — all before
PR #234 produced the source/anchor/race adjudication artifact.

The Layer-2 execution PR must mirror that precedent for tranche-2, with
six tranche-specific design constraints layered on:

1. The tranche is 6 families, not 5; the validator's
   `EXPECTED_TRANCHE_COUNT` is 6.
2. `prediction_setting` must be `history_enriched_pre_game`, not `pre_game`.
3. `allowed_cutoff_rule` must be `history_time < target_time`, not
   `snapshot_at_match_start`; the validator must reject `<=`.
4. `cold_start_handling` is family-specific (G-CS-2, G-CS-3, G-CS-4, G-CS-5,
   G-CS-6) per registry row, not a single uniform value.
5. The `cross_region_fragmentation_handling` row has `status =
   allowed_with_caveat` and `candidate_leakage_modes =
   cross_region_history_drop`; the validator must accept this row's
   special status and recognize that the policy choice
   (strict-exclusion / dual-path / sensitivity-indicator) is **deferred**
   to a future adjudication PR (the validator must NOT pin a policy
   numeric choice).
6. The `in_game_history_aggregate` row aggregates IN_GAME_HISTORICAL
   columns (APM / SQ / supplyCappedPercent / header_elapsedGameLoops)
   over PRIOR matches per CROSS-02-00 §5.4; these columns are retained
   in scope for history-aggregation use while remaining forbidden as
   direct game-T pre-game features. The validator must encode this
   distinction.

A seventh tranche-specific constraint emerged from PR #239's final-gate
review: the ROADMAP's `inputs.duckdb_tables` list contains
`matches_history_minimal` but the body `method` references only
`matches_flat_clean` + `player_history_all`. The Layer-2 scaffold must
**document** what `matches_history_minimal` is consumed for (most likely
cold-start enumeration G-CS-2/3/4/5: enumerating the set of
(focal_player, target.started_at) pairs over which prior-history is
counted). The validator must enforce that this documentation exists in
the scaffold notebook prose.

This Layer-1 PR commits the plan. The Layer-2 PR will implement it. No
data is touched at this layer; no DuckDB query runs; no Parquet is
written.

## Assumptions & Unknowns

### Assumptions (BINDING for the Layer-2 PR)

A1. The merged 02_01_01 registry CSV at
    `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv`
    is the **authoritative catalog** for tranche-2 scope. The validator
    binds to this path and rejects any stale path containing the deprecated
    `02_01_01_feature_family_registry_sc2egset.csv` fragment (mirroring
    the `STALE_REGISTRY_FILENAME_FRAGMENT` precedent in the tranche-1
    validator).

A2. The 6 `history_enriched_pre_game` family IDs from registry rows 7-12 are
    (verbatim):
    - `sc2egset.history_enriched_pre_game.focal_player_history`
    - `sc2egset.history_enriched_pre_game.opponent_player_history`
    - `sc2egset.history_enriched_pre_game.matchup_history_aggregate`
    - `sc2egset.history_enriched_pre_game.reconstructed_rating`
    - `sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling`
    - `sc2egset.history_enriched_pre_game.in_game_history_aggregate`
    These are frozen as `HISTORY_TRANCHE2_FAMILY_IDS: frozenset[str]`.

A3. The expected per-row registry values (frozen as module-level constants
    per Invariant I7):
    - `prediction_setting == "history_enriched_pre_game"` for all 6 rows.
    - `source_table_or_event_family == "matches_flat"` for all 6 rows
      (verified verbatim in the registry CSV; this is the registry-recorded
      source, which may be view-vs-raw refined in the future tranche-2
      adjudication PR — the validator binds to the registry as authoritative).
    - `temporal_anchor == "details_timeUTC"` for all 6 rows.
    - `allowed_cutoff_rule == "history_time < target_time"` for all 6 rows.
    - `per_player_construction == "symmetric"` for all 6 rows.
    - `dataset_tag == "sc2egset"` for all 6 rows.
    - `status == "allowed"` for 5 rows; `status == "allowed_with_caveat"`
      for `cross_region_fragmentation_handling` only.
    - `cold_start_handling` is one of {G-CS-2, G-CS-3, G-CS-4, G-CS-5}
      per the registry (note: G-CS-6 is NOT present in tranche-2 rows
      per the registry CSV; G-CS-6 appears only in in_game_caveat rows).

A4. The scaffold notebook is jupytext py:percent + ipynb pair, written under
    `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/`,
    with no `def` / `class` / lambda in cells (all logic imported from the
    validator module per `feedback_notebook_print_vs_logger.md` and
    `feedback_no_plan_codes_in_docs.md`).

A5. The validator module path is
    `src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py`
    (mirroring the tranche-1 file name pattern). It exposes the dataclasses
    and functions enumerated in **Validator design**.

A6. The mirrored test file path is
    `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py`
    per the project test mirror convention in `.claude/rules/python-code.md`.

A7. The Layer-2 execution PR's coverage gate is ≥95% per the tranche-1
    precedent (which achieved equivalent coverage via 31 test functions).

A8. The PR #239 final-gate nit about `matches_history_minimal` consumption
    is interpreted as a **scaffold-prose** requirement (the notebook must
    have a markdown cell explaining what MHM is consumed for); the
    validator enforces this by reading the registry CSV row source
    binding only. A scaffold-prose validator (e.g., a markdown linter) is
    out of scope for tranche-2; the requirement is enforced via plan
    Verification rather than via a runtime check.

### Unknowns (DEFERRED — not blocking this scaffold)

U1. **Cross-region fragmentation policy choice.** The registry's
    `cross_region_fragmentation_handling` row carries
    `status = allowed_with_caveat` and
    `candidate_leakage_modes = cross_region_history_drop`. CROSS-02-02 §6.2
    row 5 enumerates three operationalisation options: (a) strict-exclusion,
    (b) dual-feature-path, (c) sensitivity-indicator co-registration. The
    choice is empirically conditional (retention measurement) and is
    DEFERRED to the tranche-2 source/anchor/cold-start adjudication PR
    (analogous to PR #234). The Layer-2 scaffold validator must **NOT pin
    a choice**; it must verify that the registry row carries the
    `allowed_with_caveat` status and that no policy choice is encoded in
    the scaffold notebook prose.

U2. **Rating reconstruction model choice.** The `reconstructed_rating`
    row's cold-start handling is G-CS-4 (no global rating fit; forward-in-
    time reconstruction from prior decisive results only). The choice of
    Glicko-2 vs Elo vs alternatives is DEFERRED to the materialization
    PR (Layer-3+). The scaffold must record G-CS-4 as a declared
    cold-start gate without pinning the algorithm.

U3. **View-vs-raw source layer.** The registry CSV lists `matches_flat`
    as the source. Per the tranche-1 PR #234 precedent, the cleaned-raw
    layer (`matches_flat_clean`) may be the operative materialization
    source rather than `matches_flat`. The ROADMAP `inputs.duckdb_tables`
    lists `matches_flat_clean`, `matches_history_minimal`, and
    `player_history_all`. This is a known source-vs-registry divergence
    that the scaffold must **document** (mirroring the 02_01_02 scaffold
    cell at lines 96-115) but NOT resolve. Resolution is deferred to
    the tranche-2 adjudication PR.

U4. **Materialization SQL.** The exact projection SQL for each of the 6
    families is DEFERRED to the materialization PR (Layer-3+). The
    scaffold may record a high-level pattern (self-join
    `matches_flat_clean` to `player_history_all` on
    `(player_id_worldwide)` with strict `ph.details_timeUTC <
    target.started_at` filter; produce focal_* and opponent_* symmetric
    columns) without binding to a final SQL.

U5. **Post-materialization CROSS-02-01 audit.** The non-vacuous audit
    that returns `features_audited != []` over the 6 history families is
    DEFERRED to the materialization PR; the scaffold validator must NOT
    write any `leakage_audit_sc2egset.json` artifact.

U6. **Step closure.** The U2.B-style closure PR (adding `02_01_03:
    complete` to `STEP_STATUS.yaml` and the closure entry to the dataset
    `research_log.md`) is DEFERRED to a separate post-materialization
    closure PR per the PR #237 tranche-1 closure precedent.

## Literature Context

This is a methodology-scaffolding planning PR; the literature context is
the project's own normative documents (cited verbatim in the
`source_artifacts` frontmatter) and the cross-spec invariants in
`.claude/scientific-invariants.md`. No external academic citation is
load-bearing for the scaffold; literature derivations (cold-start
empirical thresholds K; smoothing pseudocount m; Bayesian prior strength
α; rating-reconstruction hyperparameters) are explicitly DEFERRED to the
materialization PR per Invariant I7.

For the rating reconstruction family (`reconstructed_rating`, G-CS-4),
the candidate algorithms cited at design time are: Elo (Elo 1978),
Glicko (Glickman 1999), Glicko-2 (Glickman 2012), TrueSkill (Herbrich,
Minka, Graepel 2006/2007). The choice between these is U2 — DEFERRED.
The relevant entries already exist in `thesis/references.bib`:
`Elo1978`, `Glickman1999`, `Glickman2012`, `Herbrich2006`.

For the cross-region fragmentation handling family (RISK-20), the project's
own evidence is `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/methodology_risk_register.md`
RISK-20 and the Phase 01 W=30 FAIL verdict cited in CROSS-02-02 §6.2 row 5.
No external citation is required at the scaffold layer.

The non-batching protocol cited is `.claude/rules/data-analysis-lineage.md`
"Non-batching rule for empirical work" (sequence step 2). The
falsifier-discipline protocol cited is "Required structure for every
empirical analysis" in the same rule (every empirical analysis declares
assumption, measurement claim, sanity check, falsifier, expected
artifact, lineage source, downstream decision).

## Execution Steps

Each task below describes work to be performed by the Layer-2 executor.
T01 through T08 produce the **7 Layer-2 execution files**; together with the
**2 inherited planning files** (`planning/current_plan.md` +
`planning/current_plan.critique.md` carried forward from this Layer-1 PR), the
future Layer-2 PR has a **9-file tracked diff**. T09 is the Layer-2 final-gate
dispatch. **None of T01-T09 executes at this Layer-1 PR.** This Layer-1 PR
only commits the plan + critique (2 files).

### T01 — Validator dataclasses and constants

**Objective:** Define the module-level constants and frozen dataclasses
for the history-enriched pre_game tranche-2 scaffold validator. No magic
numbers (Invariant I7); all expected values from the registry are
UPPER_SNAKE_CASE constants.

**Instructions:**
1. Create `src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py`.
2. Declare `HISTORY_TRANCHE2_FAMILY_IDS: frozenset[str]` containing exactly
   the 6 family IDs listed in Assumption A2.
3. Declare `EXPECTED_TRANCHE2_COUNT: int = 6`.
4. Declare `HISTORY_PREDICTION_SETTING: str = "history_enriched_pre_game"`.
5. Declare `EXPECTED_TEMPORAL_ANCHOR: str = "details_timeUTC"`.
6. Declare `EXPECTED_ALLOWED_CUTOFF_RULE: str = "history_time < target_time"`.
7. Declare `EXPECTED_PER_PLAYER_CONSTRUCTION: str = "symmetric"`.
8. Declare `ALLOWED_HISTORY_COLD_START_GATES: frozenset[str] = frozenset({"G-CS-2", "G-CS-3", "G-CS-4", "G-CS-5"})`.
9. Declare `ALLOWED_HISTORY_STATUSES: frozenset[str] = frozenset({"allowed", "allowed_with_caveat"})`.
10. Declare `CROSS_REGION_FAMILY_ID: str = "sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling"` and `CROSS_REGION_EXPECTED_STATUS: str = "allowed_with_caveat"`.
11. Declare `IN_GAME_HISTORY_AGG_FAMILY_ID: str = "sc2egset.history_enriched_pre_game.in_game_history_aggregate"` and the `IN_GAME_HISTORICAL` column names retained in scope per CROSS-02-00 §5.4: `IN_GAME_HISTORICAL_AGGREGATED_COLUMNS: tuple[str, ...] = ("APM", "SQ", "supplyCappedPercent", "header_elapsedGameLoops")`.
12. Declare `FORBIDDEN_CUTOFF_OPERATORS: tuple[str, ...] = ("<=", "==", ">=")` (the strict-< operator is the only admissible one for history; `<=` is the most common slip).
13. Declare `TRACKER_SOURCE_PREFIX: str = "tracker_events_raw"`, `PRE_GAME_PREDICTION_SETTING: str = "pre_game"`, `IN_GAME_PREDICTION_SETTING: str = "in_game_snapshot"`, `BLOCKED_PREDICTION_SETTING: str = "blocked_or_deferred"`.
14. Declare `TRUE_REGISTRY_CSV_RELPATH: str` (path of the closed 02_01_01 registry CSV) and `STALE_REGISTRY_FILENAME_FRAGMENT: str = "02_01_01_feature_family_registry_sc2egset.csv"` (mirroring the tranche-1 stale-path falsifier).
15. Declare `POST_GAME_TOKENS: tuple[str, ...]` mirroring tranche-1 (`"won"`, `"win"`, `"loss"`, `"result"`, `"final_state"`, `"match_result"`, `"post_game"`, `"outcome"`, `"winner"`, `"is_decisive"`).
16. Declare the `HistoryEnrichedPreGameTrancheRow` frozen dataclass with fields: `feature_family_id`, `prediction_setting`, `source_table_or_event_family`, `temporal_anchor`, `allowed_cutoff_rule`, `candidate_leakage_modes`, `cold_start_handling`, `status`, `per_player_construction`.
17. Declare the `HistoryEnrichedScaffoldValidationResult` frozen dataclass with all 13 result fields enumerated in **Validator design** below, including `materialized_output_paths: tuple[str, ...] = field(default_factory=tuple)` defaulting to `()`.

**Verification:**
- `source .venv/bin/activate && poetry run python -c "from rts_predict.games.sc2.datasets.sc2egset.validate_history_enriched_pre_game_materialization import HISTORY_TRANCHE2_FAMILY_IDS, EXPECTED_TRANCHE2_COUNT; assert len(HISTORY_TRANCHE2_FAMILY_IDS) == EXPECTED_TRANCHE2_COUNT == 6"` returns exit 0.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_pre_game_feature_materialization.py` (tranche-1 precedent)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv` (rows 7-12 verbatim source)

### T02 — Validator loader and helpers

**Objective:** Implement the public loader `load_history_enriched_pre_game_tranche_rows` and the private `_check_*` falsifier helpers. The validator never writes a file; it only reads the registry CSV.

**Instructions:**
1. Implement `load_history_enriched_pre_game_tranche_rows(registry_csv_path: Path | str) -> list[HistoryEnrichedPreGameTrancheRow]` mirroring the tranche-1 loader pattern: raise `ValueError` if the path contains `STALE_REGISTRY_FILENAME_FRAGMENT`; raise `FileNotFoundError` if missing; read with `csv.DictReader`; filter rows whose `feature_family_id ∈ HISTORY_TRANCHE2_FAMILY_IDS`; return frozen dataclass instances.
2. Implement `_load_full_registry(path: Path) -> list[dict[str, str]]` returning all registry rows as dicts.
3. Implement `_check_tranche_membership(rows, full_registry) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]` returning `(tranche_family_ids, missing_families_in_tranche, extra_history_families_beyond_tranche)`. The "extra" check scans the full registry for any row with `prediction_setting == HISTORY_PREDICTION_SETTING` whose `feature_family_id` is NOT in `HISTORY_TRANCHE2_FAMILY_IDS`.
4. Implement `_check_prediction_setting(rows) -> tuple[str, ...]` returning family_ids whose `prediction_setting != HISTORY_PREDICTION_SETTING`.
5. Implement `_check_cutoff_rule_is_strict(rows) -> tuple[tuple[str, str], ...]` returning `(family_id, allowed_cutoff_rule)` pairs whose `allowed_cutoff_rule != EXPECTED_ALLOWED_CUTOFF_RULE` OR contains any token in `FORBIDDEN_CUTOFF_OPERATORS` ("<=", "==", ">=").
6. Implement `_check_no_tracker_source(rows) -> tuple[str, ...]` returning family_ids whose `source_table_or_event_family` starts with `TRACKER_SOURCE_PREFIX` (Invariant I3; Amendment 2 of PR #208).
7. Implement `_check_no_pre_game_or_in_game_or_blocked_in_tranche(full_registry) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]` returning three tuples of family_ids: pre_game families that alias a tranche-2 id, in_game families that alias a tranche-2 id, blocked families that alias a tranche-2 id.
8. Implement `_check_symmetry(rows) -> tuple[str, ...]` returning family_ids whose `per_player_construction != EXPECTED_PER_PLAYER_CONSTRUCTION` (Invariant I5).
9. Implement `_check_no_post_game_tokens(rows, designed_column_names) -> tuple[tuple[str, str], ...]` mirroring the tranche-1 boundary-aware token equality on designed column names + substring check on registry source fields (CROSS-02-01 §2.2).
10. Implement `_check_temporal_anchor(rows) -> tuple[str, ...]` returning family_ids whose `temporal_anchor != EXPECTED_TEMPORAL_ANCHOR` (CROSS-02-00 §3.2).
11. Implement `_check_cross_region_caveat(rows) -> bool` returning True iff `CROSS_REGION_FAMILY_ID` is present in tranche rows AND that row's `status == CROSS_REGION_EXPECTED_STATUS` (`allowed_with_caveat`).
12. Implement `_check_in_game_history_aggregate_columns(rows, designed_in_game_historical_columns) -> tuple[str, ...]` returning the set difference `set(designed_in_game_historical_columns) - set(IN_GAME_HISTORICAL_AGGREGATED_COLUMNS)` — the scaffold notebook declares which IN_GAME_HISTORICAL columns it plans to aggregate over PRIOR matches for `in_game_history_aggregate`; the validator verifies this declared list is a subset of the CROSS-02-00 §5.4 retained set.
13. Implement `_check_cold_start_gates(rows) -> tuple[tuple[str, str], ...]` returning `(family_id, cold_start_handling)` pairs whose `cold_start_handling` is NOT in `ALLOWED_HISTORY_COLD_START_GATES`.
14. Implement `_check_status_admissibility(rows) -> tuple[tuple[str, str], ...]` returning `(family_id, status)` pairs whose `status` is NOT in `ALLOWED_HISTORY_STATUSES`.
15. All helpers must be pure (no side effects, no file writes). Type hints on every signature. Google-style docstrings. Maximum ~50 LOC per helper (per `.claude/rules/python-code.md`).

**Verification:**
- `source .venv/bin/activate && poetry run ruff check src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py` returns exit 0.
- `source .venv/bin/activate && poetry run mypy src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py` returns exit 0.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py` (updated)

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_pre_game_feature_materialization.py` (helper-shape precedent)

### T03 — Validator public entrypoint and falsifier priority

**Objective:** Implement `validate_history_enriched_pre_game_materialization(registry_csv_path, designed_column_names, designed_in_game_historical_columns) -> HistoryEnrichedScaffoldValidationResult` with explicit falsifier priority ordering and `materialized_output_paths = ()` always.

**Instructions:**
1. Add the public function signature with three parameters: `registry_csv_path: Path | str`, `designed_column_names: tuple[str, ...]`, `designed_in_game_historical_columns: tuple[str, ...]` (the third parameter is the notebook-declared list of IN_GAME_HISTORICAL columns the scaffold plans to aggregate; tranche-1 only needed two parameters).
2. Inside the function, call all 12 `_check_*` helpers from T02.
3. Resolve `halting_falsifier` in this priority order (highest first; most structural before more specific):
   - `missing_families_in_tranche` (any expected family absent)
   - `extra_history_in_tranche` (any history family in registry outside the tranche)
   - `pre_game_in_history_tranche` (a pre_game family aliases a tranche-2 id)
   - `in_game_in_history_tranche` (an in_game family aliases a tranche-2 id)
   - `blocked_in_history_tranche` (a blocked family aliases a tranche-2 id)
   - `tranche_count_mismatch` (defensive: count != 6 despite no membership errors)
   - `wrong_prediction_setting` (any tranche row's `prediction_setting != "history_enriched_pre_game"`)
   - `wrong_temporal_anchor` (any tranche row's `temporal_anchor != "details_timeUTC"`)
   - `cutoff_not_strict` (any tranche row's `allowed_cutoff_rule != "history_time < target_time"` or contains `<=` / `==` / `>=`)
   - `tracker_source_in_history` (any tranche row's source starts with `tracker_events_raw`)
   - `asymmetric_construction` (any tranche row's `per_player_construction != "symmetric"`)
   - `post_game_token` (any designed column name or registry source field contains a POST_GAME token)
   - `cross_region_caveat_missing` (cross-region row absent or its status is not `allowed_with_caveat`)
   - `in_game_historical_column_out_of_scope` (designed IN_GAME_HISTORICAL columns include a name outside CROSS-02-00 §5.4)
   - `cold_start_gate_invalid` (any tranche row's `cold_start_handling` not in {G-CS-2, G-CS-3, G-CS-4, G-CS-5})
   - `status_not_admissible` (any tranche row's `status` not in {allowed, allowed_with_caveat})
4. Set `passed = halting_falsifier is None`.
5. Return the dataclass with all 13 result fields populated.
6. Always set `materialized_output_paths=()`.
7. Use `LOGGER = logging.getLogger(__name__)`; emit one `LOGGER.debug` line summarising passed/tranche_count/halting_falsifier per the tranche-1 precedent.

**Verification:**
- `source .venv/bin/activate && poetry run python -c "from pathlib import Path; from rts_predict.games.sc2.datasets.sc2egset.validate_history_enriched_pre_game_materialization import validate_history_enriched_pre_game_materialization; r = validate_history_enriched_pre_game_materialization(Path('src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv'), (), ('APM','SQ','supplyCappedPercent','header_elapsedGameLoops')); assert r.passed is True and r.materialized_output_paths == () and len(r.tranche_family_ids) == 6"` returns exit 0.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py` (updated)

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv` (real CSV for smoke validation)

### T04 — Test file: synthetic CSV helpers and shared fixtures

**Objective:** Create the mirrored test file at the project test path with synthetic CSV helpers (`_history_tranche_row`, `_write_csv`, `_all_six_tranche_rows`) and shared module-level constants.

**Instructions:**
1. Create `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py`.
2. Resolve `_TESTS_ROOT = Path(__file__).resolve().parents[6]` (mirroring the tranche-1 test file).
3. Declare `REGISTRY_CSV_PATH` to the real on-disk 02_01_01 registry CSV (skipif if absent).
4. Declare `DESIGNED_COLUMN_NAMES: tuple[str, ...]` — a tranche-2 representative list, e.g.:
   `("focal_prior_match_count", "opponent_prior_match_count", "focal_prior_win_rate", "opponent_prior_win_rate", "matchup_h2h_count", "matchup_h2h_focal_win_rate", "focal_reconstructed_rating", "opponent_reconstructed_rating", "is_cross_region_fragmented", "focal_apm_prior_mean", "opponent_apm_prior_mean")`.
5. Declare `DESIGNED_IN_GAME_HISTORICAL_COLUMNS: tuple[str, ...] = ("APM", "SQ", "supplyCappedPercent", "header_elapsedGameLoops")` (matches CROSS-02-00 §5.4 retained set).
6. Implement `_history_tranche_row(**kwargs) -> dict[str, str]` building a minimal valid history-enriched pre_game registry row with all 14 registry columns; defaults match the registry (`prediction_setting=history_enriched_pre_game`, `source_table_or_event_family=matches_flat`, `temporal_anchor=details_timeUTC`, `allowed_cutoff_rule=history_time < target_time`, `per_player_construction=symmetric`, `status=allowed`, `block=history_enriched_pre_game`, `cold_start_handling=G-CS-2`).
7. Implement `_write_csv(path, rows)` mirroring tranche-1.
8. Implement `_all_six_tranche_rows()` returning the 6 family rows (the cross_region row carries `status=allowed_with_caveat`, `candidate_leakage_modes=cross_region_history_drop`, `cold_start_handling=G-CS-5`; the matchup_history_aggregate row carries `cold_start_handling=G-CS-3`; the reconstructed_rating row carries `cold_start_handling=G-CS-4`; the in_game_history_aggregate row carries `cold_start_handling=G-CS-2`; the two player_history rows carry `cold_start_handling=G-CS-2`).

**Verification:**
- `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py::TestExactTrancheMembership -v` returns at least one collected test (validates file imports cleanly).

**File scope:**
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py`

**Read scope:**
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_pre_game_feature_materialization.py` (synthetic CSV precedent)

### T05 — Test file: 13 falsifier test classes

**Objective:** Implement 13 test classes mirroring the falsifier priority chain from T03, with ≥1 test method per class. Target: ≥30 individual test functions, ≥95% line coverage of the validator module.

**Instructions:**

Implement the 13 test classes (one per falsifier in T03 priority order) plus the additional coverage tests:

1. `TestExactSixFamilyMembership` — synthetic CSV with all 6 rows → `passed=True`, `tranche_count=6`, `halting_falsifier=None`.
2. `TestMissingFamilyInTranche` — parametrized over each of the 6 family IDs; remove one → `halting_falsifier == "missing_families_in_tranche"`.
3. `TestExtraHistoryInTranche` — add a 7th history row outside the tranche → `halting_falsifier == "extra_history_in_tranche"`.
4. `TestPreGameAliasInTrancheRejected` — add a row with a tranche-2 family_id but `prediction_setting=pre_game` → `halting_falsifier == "pre_game_in_history_tranche"`.
5. `TestInGameAliasInTrancheRejected` — add a row with a tranche-2 family_id but `prediction_setting=in_game_snapshot` → `halting_falsifier == "in_game_in_history_tranche"`.
6. `TestBlockedAliasInTrancheRejected` — add a row with a tranche-2 family_id but `prediction_setting=blocked_or_deferred` → `halting_falsifier == "blocked_in_history_tranche"`.
7. `TestWrongPredictionSettingRejected` — flip one row's `prediction_setting` to `pre_game` → `halting_falsifier == "wrong_prediction_setting"`.
8. `TestWrongTemporalAnchorRejected` — flip one row's `temporal_anchor` to `started_at` → `halting_falsifier == "wrong_temporal_anchor"`.
9. `TestCutoffNotStrictRejected` — parametrized: cutoff rule = `history_time <= target_time`, `=`, `>=`, or empty string → `halting_falsifier == "cutoff_not_strict"`.
10. `TestTrackerSourceInHistoryRejected` — flip one row's source to `tracker_events_raw.PlayerStats` → `halting_falsifier == "tracker_source_in_history"`.
11. `TestAsymmetricConstructionRejected` — flip one row's `per_player_construction` to `asymmetric` → `halting_falsifier == "asymmetric_construction"`.
12. `TestPostGameTokenRejected` — add `"focal_won"` to designed columns → `halting_falsifier == "post_game_token"`.
13. `TestCrossRegionCaveatMissing` — remove the cross_region row → `halting_falsifier in ("missing_families_in_tranche", "cross_region_caveat_missing")` (whichever fires first by priority); separately: keep the row but flip `status` to `allowed` → `halting_falsifier == "cross_region_caveat_missing"`.
14. `TestInGameHistoricalOutOfScopeRejected` — pass `designed_in_game_historical_columns=("foo_random_metric",)` → `halting_falsifier == "in_game_historical_column_out_of_scope"`.
15. `TestColdStartGateInvalidRejected` — flip one row's `cold_start_handling` to `G-CS-1` (the pre_game gate, invalid for history) → `halting_falsifier == "cold_start_gate_invalid"`.
16. `TestStatusNotAdmissibleRejected` — flip one row's `status` to `blocked_until_validation` → `halting_falsifier == "status_not_admissible"`.
17. `TestStaleRegistryPathRaises` — pass a path containing `02_01_01_feature_family_registry_sc2egset.csv` → `pytest.raises(ValueError, match="Stale registry path")`.
18. `TestMaterializedOutputPathsAlwaysEmpty` — both passing and failing results return `materialized_output_paths == ()`.
19. `TestRealRegistryCsvSmoke` (with `@pytest.mark.skipif(not REGISTRY_CSV_PATH.exists(), ...)`):
    - `test_passed_is_true_on_real_registry`
    - `test_tranche_count_is_six`
    - `test_halting_falsifier_is_none`
    - `test_missing_families_empty`
    - `test_materialized_output_paths_empty`
    - `test_cross_region_status_is_allowed_with_caveat`
    - `test_six_family_ids_match_expected_frozenset`

20. `TestAdditionalCoverage` — `test_load_history_tranche_rows_file_not_found` (FileNotFoundError); `test_post_game_token_in_source_field` (registry source contains `won`).

**Verification:**
- `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py -v` reports ≥30 passed, 0 failed.
- `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py --cov=rts_predict.games.sc2.datasets.sc2egset.validate_history_enriched_pre_game_materialization --cov-report=term-missing` reports ≥95% coverage on the validator module.

**File scope:**
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py` (updated)

**Read scope:**
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_pre_game_feature_materialization.py` (test-shape precedent)

### T06 — Scaffold notebook: jupytext pair, prose cells, validator import

**Objective:** Create the jupytext-paired scaffold notebook (.py canonical + .ipynb pair) under the sandbox tree. No `def`/`class`/lambda in cells. All logic imported from T01-T03. Read-only `print()` summaries only.

**Instructions:**
1. Create `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py` with jupytext header `formats: ipynb,py:percent` (mirror the 02_01_02 scaffold header).
2. Add markdown title cell: `# Step 02_01_03 — History-enriched pre_game feature-family materialization SCAFFOLD: sc2egset`.
3. Add prose cells covering (each as its own `# %% [markdown]` block):
   - **Lineage position:** artifact #2 of N for Step 02_01_03 readiness; ROADMAP stub (PR #239) preceded.
   - **Six-family design table:** verbatim 6 rows from registry rows 7-12 with all columns; matches tranche-1 design-table precedent.
   - **Context and input artifacts:** binds to (a) closed 02_01_01 registry CSV; (b) PR #229 §10 design-time verdict-audit CSV; (c) PR #234 source/anchor/race adjudication CSV (tranche-1 reference); (d) the merged 02_01_02 materialized Parquet at `02_01_02_pre_game_features.parquet` — READ as upstream evidence only, NOT re-materialized.
   - **What `matches_history_minimal` is consumed for (PR #239 nit):** explicitly document — most likely cold-start enumeration G-CS-2/3/4/5 (enumerating the set of `(focal_player, target.started_at)` target rows over which prior history is counted) and/or the row-identity anchor `started_at` per PR #234 Q2(a). NOTE that resolution is deferred to the tranche-2 source/anchor/cold-start adjudication PR; the scaffold only records the consumption purpose.
   - **Three concepts distinguished (per CROSS-02-00 §5.4 + CROSS-02-02 §6.2):**
     1. `history_enriched_pre_game` over PRIOR matches (the 6 families in this tranche) — strict `<` cutoff.
     2. `in_game_snapshot` over target-match tracker/game events (DEFERRED to Step 02_01_04+) — `<=` cutoff.
     3. `IN_GAME_HISTORICAL` columns aggregated from PRIOR matches (used by `in_game_history_aggregate` family) — retained in scope per CROSS-02-00 §5.4 Concern 8 / T15 record.
   - **Projection design (SPECIFIED, NOT EXECUTED):** the future SQL pattern is a self-join `matches_flat_clean` (target row) to `player_history_all` (history rows) on `(player_id_worldwide)` with strict `ph.details_timeUTC < target.started_at`; produces focal_* and opponent_* symmetric columns; encoders/smoothing-priors SPECIFIED but NOT FIT (G-CS-6 fold-aware fit deferred to materialization). NO SQL is executed in this scaffold.
   - **Cross-region adjudication DEFERRED:** the policy choice (strict-exclusion / dual-path / sensitivity-indicator co-registration) is deferred to a future tranche-2 source/anchor/cold-start adjudication PR analogous to PR #234; the scaffold validator verifies only that the `cross_region_fragmentation_handling` row exists with `status=allowed_with_caveat`.
   - **Rating reconstruction model choice DEFERRED:** Glicko-2 vs Elo vs alternatives is deferred to the materialization PR; the scaffold records only G-CS-4 as the declared cold-start gate.
4. Add the import cell:
   ```python
   from pathlib import Path
   from rts_predict.games.sc2.datasets.sc2egset.validate_history_enriched_pre_game_materialization import (
       validate_history_enriched_pre_game_materialization,
       IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
   )
   ```
5. Add the data-cell:
   ```python
   DESIGNED_COLUMN_NAMES = (
       "focal_prior_match_count",
       "opponent_prior_match_count",
       "focal_prior_win_rate",
       "opponent_prior_win_rate",
       "matchup_h2h_count",
       "matchup_h2h_focal_win_rate",
       "focal_reconstructed_rating",
       "opponent_reconstructed_rating",
       "is_cross_region_fragmented",
       "focal_apm_prior_mean",
       "opponent_apm_prior_mean",
   )
   DESIGNED_IN_GAME_HISTORICAL_COLUMNS = IN_GAME_HISTORICAL_AGGREGATED_COLUMNS
   REGISTRY_CSV = Path(
       "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
       "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
       "02_01_01_feature_family_registry.csv"
   )
   ```
6. Add the validator-call cell:
   ```python
   result = validate_history_enriched_pre_game_materialization(
       REGISTRY_CSV, DESIGNED_COLUMN_NAMES, DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
   )
   print("passed:", result.passed)
   print("tranche_count:", result.tranche_count)
   print("tranche_family_ids:", result.tranche_family_ids)
   print("halting_falsifier:", result.halting_falsifier)
   print("materialized_output_paths:", result.materialized_output_paths)
   assert result.passed is True
   assert result.materialized_output_paths == ()
   assert result.halting_falsifier is None
   ```
7. Add a final markdown cell **"Closing — scaffold + ONE validator persisted; NO feature value materialized; NO artifact; NO status flip; NO research_log; lineage position artifact #2 of N for Step 02_01_03 readiness."**
8. After saving the .py, generate the paired .ipynb via `source .venv/bin/activate && poetry run jupytext --sync sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py`.
9. Clear all outputs in the .ipynb before staging (no notebook outputs committed; the .py is canonical).

**Verification:**
- `source .venv/bin/activate && poetry run jupytext --check-metadata sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py` succeeds.
- `git diff --stat` shows .py and .ipynb both present.
- Manually inspect the .ipynb cell outputs: ALL must be empty.

**File scope:**
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py`
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.ipynb`

**Read scope:**
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.py` (scaffold-cell precedent)
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py` (validator import surface produced by T01-T03)

### T07 — Repo housekeeping: INDEX archive, CHANGELOG, version bump

**Objective:** Update `planning/INDEX.md`, `CHANGELOG.md`, and `pyproject.toml` for the Layer-2 execution PR.

**Instructions:**
1. In `planning/INDEX.md`, move the current Active row (PR #239 if not already archived; or whichever planning PR is Active when this Layer-2 PR opens) to the Archive table, and add a new Active row for `feat/sc2egset-02-01-03-history-scaffold` describing this Layer-2 PR.
2. In `CHANGELOG.md`, move `[Unreleased]` content into a new versioned section `[3.72.0] — <date> (PR #<number>: feat/sc2egset-02-01-03-history-scaffold)` with `Added` entries for the validator module, the test file, and the scaffold notebook pair. Mirror the PR #233 changelog phrasing.
3. In `pyproject.toml`, bump `version = "3.71.0"` → `version = "3.72.0"` (minor; feat-family per `.claude/rules/git-workflow.md`).

**Verification:**
- `source .venv/bin/activate && poetry version` reports `3.72.0`.
- `git diff planning/INDEX.md` shows the active row replaced + an Archive row appended.
- `git diff CHANGELOG.md` shows a new `[3.72.0]` section, no `[Unreleased]` content.

**File scope:**
- `planning/INDEX.md`
- `CHANGELOG.md`
- `pyproject.toml`

### T08 — Pre-commit validation pass

**Objective:** Confirm ruff, mypy, and pytest pass cleanly on the entire Layer-2 diff before commit.

**Instructions:**
1. Run `source .venv/bin/activate && poetry run ruff check src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py`.
2. Run `source .venv/bin/activate && poetry run mypy src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py`.
3. Run `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py -v --cov=rts_predict.games.sc2.datasets.sc2egset.validate_history_enriched_pre_game_materialization --cov-report=term-missing`.
4. Run the pre-commit hook check: `source .venv/bin/activate && poetry run pre-commit run --files <staged-files>`.
5. If any check fails, fix and re-stage. Do NOT use `--no-verify`. Do NOT amend; create a NEW commit if a hook failure produces a delta.

**Verification:**
- All three commands return exit 0.
- Coverage ≥ 95% on the validator module.
- pytest reports ≥ 30 tests passed, 0 failed.
- The Layer-2 commit message follows the format `feat(sc2egset): Step 02_01_03 scaffold + validator (history-enriched pre_game)`.

**File scope:** (none — runs commands)

### T09 — Final-gate routing for the Layer-2 PR

**Objective:** Dispatch the appropriate reviewers per category routing.

**Instructions:**
1. On Layer-2 PR open, dispatch `@reviewer-deep` for structural correctness, spec compliance, and invariant tracing.
2. Per `.claude/rules/data-analysis-lineage.md` "Agent and model routing discipline" — if reviewer-deep raises any methodology BLOCKER, dispatch `@reviewer-adversarial` for the methodology defensibility check; otherwise reviewer-adversarial is optional for this scaffold-only PR (which materializes nothing and writes no artifact).
3. Final gate verdict from reviewer-deep must be APPROVE (with or without nits) before merge.
4. Do NOT merge in the execution prompt without explicit user decision; the user reviews the reviewer report and approves the merge.

**Verification:**
- Reviewer-deep report exists on the PR before merge.
- If methodology BLOCKER raised, reviewer-adversarial report exists too.
- User has explicitly approved the merge in chat.

**File scope:** (none — process step)

## File Manifest

### This Layer-1 planning PR (2 files)
- `planning/current_plan.md` (created — this document)
- `planning/current_plan.critique.md` (created by reviewer-adversarial in a separate dispatch)

### Future Layer-2 execution PR (7 execution files + 2 inherited planning = 9 total)
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py` (created by T06)
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.ipynb` (created by T06)
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py` (created by T01-T03)
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py` (created by T04-T05)
- `planning/INDEX.md` (updated by T07)
- `CHANGELOG.md` (updated by T07)
- `pyproject.toml` (updated by T07)
- `planning/current_plan.md` (inherited from this Layer-1 PR; rewritten only if the Layer-2 PR amends scope)
- `planning/current_plan.critique.md` (inherited from this Layer-1 PR)

### Files explicitly NOT touched at either layer
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` (no `02_01_03: complete` added; closure is a future PR)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` (frozen; 02_01 already complete)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` (frozen; Phase 02 = in_progress)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (frozen; 02_01_03 block at lines 2274-2523 is canonical)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` (frozen)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (frozen at this layer; closure PR will append)
- `reports/research_log.md` (frozen; no CROSS entry needed for scaffold)
- Any file under `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/` (no audit JSON/MD; no leakage_audit; no Parquet)
- Any file under `reports/specs/` (no spec patch)
- Any cleaning-layer YAML
- Any file under `src/rts_predict/games/aoe2/`

## Gate Condition

The Layer-2 execution PR passes the gate iff ALL of the following hold (verified by reviewer-deep + reviewer-adversarial if dispatched):

1. **Exact file scope.** `git diff --name-only master..HEAD` shows exactly the **7 execution files + 2 inherited planning files = 9 tracked files**. No extras.

2. **Validator passes on real registry.** A one-line bash command:
   ```
   source .venv/bin/activate && poetry run python -c "from pathlib import Path; from rts_predict.games.sc2.datasets.sc2egset.validate_history_enriched_pre_game_materialization import validate_history_enriched_pre_game_materialization, IN_GAME_HISTORICAL_AGGREGATED_COLUMNS; r = validate_history_enriched_pre_game_materialization(Path('src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv'), (), IN_GAME_HISTORICAL_AGGREGATED_COLUMNS); assert r.passed and r.tranche_count == 6 and r.materialized_output_paths == ()"
   ```
   returns exit 0.

3. **Tests pass with coverage.** `pytest -v` reports ≥30 tests passed, 0 failed; `--cov` reports ≥95% line coverage on the validator module.

4. **Lint and type checks clean.** `ruff check` exit 0; `mypy` exit 0 on the validator module.

5. **No notebook outputs committed.** Manual inspection: every cell output in the .ipynb is empty.

6. **No status YAML / research_log / artifact / spec / cleaning-layer YAML change.** `git diff master..HEAD -- src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md reports/research_log.md reports/specs/ src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/` reports nothing.

7. **No artifact write.** `ls src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/ 2>/dev/null` returns nothing or "No such file or directory"; the directory must not exist post-Layer-2.

8. **Reviewer-deep APPROVE.** A reviewer-deep report on the PR with verdict APPROVE (with or without nits).

9. **No merge without user approval.** The user explicitly approves the merge in chat after reading the reviewer report(s).

If any of conditions 1-9 fail, the PR is BLOCKED. Fix-forward is the rule (per `.claude/rules/data-analysis-lineage.md` — do not amend; create a NEW commit).

## Out of scope

- Materialization SQL execution (DuckDB queries against `matches_flat_clean`, `player_history_all`, `matches_history_minimal`). DEFERRED to a future materialization PR.
- Parquet feature artifact (`02_01_03_history_enriched_pre_game_features.parquet`). DEFERRED.
- Non-vacuous CROSS-02-01-v1.0.1 leakage audit JSON/MD over the 6 history families. DEFERRED.
- Re-executed CROSS-02-03-v1.0.1 §10 verdict audit over rows 7-12 (the `continue_predicate` in the ROADMAP allows either a re-run OR a non-vacuous justification; the decision is DEFERRED to the materialization PR).
- Cross-region fragmentation policy choice. DEFERRED to tranche-2 source/anchor/cold-start adjudication PR.
- Rating reconstruction algorithm choice (Glicko-2 / Elo / TrueSkill / alternative). DEFERRED to materialization PR.
- Empirical derivation of cold-start constants (K, m, α). DEFERRED to materialization PR (must be fit on training folds only per G-CS-6 / Invariant I3 normalization discipline).
- Phase 03 splitting + baselines.
- Step 02_01_04 (in_game_snapshot tranche).
- Closure of Step 02_01_03 in `STEP_STATUS.yaml`. DEFERRED to a separate closure PR.
- Append to dataset `research_log.md`. DEFERRED to closure PR.
- AoE2 work.
- Any cleaning-layer YAML patch.
- Any spec patch (CROSS-02-00, CROSS-02-01, CROSS-02-02, CROSS-02-03).

## Open Questions

These questions are for the reviewer-adversarial pass on this Layer-1 planning PR. They are NOT blockers for the Layer-2 execution PR; the validator's 13-falsifier design is sufficient regardless of the answers.

1. **`matches_history_minimal` consumption documentation form (scaffold prose vs runtime check).** Assumption A8 interprets the PR #239 nit as a scaffold-prose requirement enforced by reviewer reading rather than by a runtime falsifier. Should the validator have a runtime check that verifies a specific markdown-cell substring exists? Alternative: keep this purely procedural (reviewer-deep reads the cell and confirms). Recommendation: procedural — runtime markdown linting is over-scoped for tranche-2.

2. **Number of cold-start gates the validator should accept (G-CS-2..5 only, vs G-CS-2..6).** The registry CSV rows 7-12 carry cold-start gates G-CS-2, G-CS-3, G-CS-4, G-CS-5 (no G-CS-6 in tranche-2). However, CROSS-02-02 §9 enumerates G-CS-2 through G-CS-6 inclusive, and G-CS-6 is the fold-aware fit gate that applies at materialization time (not at registry time). Should `ALLOWED_HISTORY_COLD_START_GATES` be `{G-CS-2, G-CS-3, G-CS-4, G-CS-5}` (strict, matches the on-disk registry) or `{G-CS-2..G-CS-6}` (permissive, matches CROSS-02-02 §9)? Recommendation: strict {G-CS-2, G-CS-3, G-CS-4, G-CS-5} per T01 step 8 — this is registry-bound, and any future amendment to add G-CS-6 to a registry row would require a registry update first, which the validator would then need to be updated to accept.

3. **`IN_GAME_HISTORICAL_AGGREGATED_COLUMNS` exposed as a public constant vs validator-internal only.** T01 step 11 declares this as a module-level public constant so the scaffold notebook can import it (T06 step 5). Alternative: keep it private and have the notebook duplicate the tuple. Recommendation: public — single source of truth per Invariant I7.

4. **Test count target (≥30 vs higher).** Tranche-1 achieved 31 test functions across 16 classes; this plan's T05 specifies "≥30". Should the target be tighter (e.g., exactly 31 to match tranche-1) or looser (e.g., ≥25)? Recommendation: ≥30 with a stretch target of 35+ given tranche-2's larger falsifier count (13 vs tranche-1's 11).

5. **Reviewer routing — adversarial mandatory or optional.** T09 step 2 makes reviewer-adversarial conditional on reviewer-deep raising a methodology BLOCKER. Alternative: mandatory adversarial review for all Phase 02 scaffold PRs. Recommendation: conditional, per `.claude/rules/data-analysis-lineage.md` "Agent and model routing discipline" line 24 ("do not invoke reviewer-adversarial unless the plan is amended or reviewer-deep raises a BLOCKER requiring adversarial methodology review") — scaffold PRs materialize nothing.

---

**For Category A or F, adversarial critique is required before execution. Dispatch reviewer-adversarial to produce `planning/current_plan.critique.md`.**
