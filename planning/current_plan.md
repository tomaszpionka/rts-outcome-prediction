---
category: A
branch: feat/sc2egset-02-01-03-history-source-anchor-coldstart-adjudication
title: "SC2EGSet Step 02_01_03 — source/anchor/cold-start adjudication (Layer-1 planning PR)"
phase: "02 — Feature Engineering"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
step_number: "02_01_03"
dataset: "sc2egset"
predecessors:
  - "02_01_02 (closed; PR #237 formal closure on master a16d78c2)"
  - "PR #241 — Step 02_01_03 scaffold + ONE validator (merged on master 3c6709bf; validator SHA-256 b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904)"
base_ref: 3c6709bfc21baba893d34a3b87c308d7f8ba787e
date: 2026-05-24
planner_model: claude-opus-4-7[1m]
critique_required: true
critique_path: "planning/current_plan.critique.md"
gate_reviewer: "reviewer-adversarial (Category A pre-execution gate; round 3 — round 2 returned HOLD with 2 NEW blockers B-X1 + B-X2 and 4 nits N-X1..N-X4 introduced by the round-2 revision itself; this is the LAST round in the 3-round adversarial cap)"
planning_pr_scope: "Layer-1 (exactly 2 files) — planning/current_plan.md + planning/current_plan.critique.md. NO adjudication CSV/MD, NO source module, NO test, NO notebook edits, NO feature materialization, NO ROADMAP edits, NO status YAML edits, NO research_log entry, NO CHANGELOG/pyproject/INDEX edits in this Layer-1 PR (those land in the future Layer-2 PR), NO spec or cleaning-layer YAML edits, NO thesis/docs/.claude/data/notebooks/AoE2 edits, NO Step 02_01_04 start, NO Phase 03 start, NO baseline modeling."
future_execution_pr_scope: |
  Future Layer-2 adjudication execution PR = 11 final tracked files:
    9 deliverable/execution files:
      1. sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.py
      2. sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.ipynb
      3. src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py
      4. tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_enriched_pre_game_source_layer.py
      5. src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
      6. src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md
      7. planning/INDEX.md
      8. CHANGELOG.md
      9. pyproject.toml
    + 2 inherited planning files already in the branch:
      10. planning/current_plan.md
      11. planning/current_plan.critique.md
version_bump_planned: "Layer-1 PR — version-neutral (planning-only; no code). Future Layer-2 adjudication PR planned bump: minor 3.72.0 → 3.73.0 (feat-family per .claude/rules/git-workflow.md — adds a new adjudication module + adjudication artifact pair; no materialized feature data)."
invariants_touched: [I3, I5, I6, I7, I8, I9, I10]
source_artifacts:
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md lines 2274-2523 (Step 02_01_03 block; merged PR #239 at master f378f6f4)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv rows 7-12 (the 6 history_enriched_pre_game families; SHA-256 320b8b018982f12539a34512421f1b34359bb825f0d1410687492dfe5c6fed1f)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv (per-family §10 verdicts; rows 7-12 cover tranche-2)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv (PR #234 tranche-1 adjudication; format precedent)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.md (PR #234 tranche-1 adjudication MD; format precedent)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet (probe metadata only — never re-materialized)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json (PR #236 tranche-1 non-vacuous audit; lineage anchor)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py (PR #241 scaffold validator; SHA-256 b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904 — N4 provenance anchor)"
  - "tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py (PR #241 mirrored tests; precedent for adjudicator tests)"
  - "sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py (PR #241 scaffold notebook; never re-edited)"
  - "reports/specs/02_00_feature_input_contract.md §3.3 strict-< rule, §5.1 sc2egset MHM columns, §5.4 SC2 IN_GAME_HISTORICAL telemetry-scope decision (Concern 8 / T15 record), §2.1 sc2egset row-grain note (player_history_all = all game types; no 1v1 filter)"
  - "reports/specs/02_01_leakage_audit_protocol.md §2.1/§2.2/§2.3/§2.4"
  - "reports/specs/02_02_feature_engineering_plan.md §6.2 (6 history families; row 1 focal_player_history sources from player_history_all; row 5 cross_region; row 6 in_game_history_aggregate IN_GAME_HISTORICAL retention), §9 (G-CS-2 through G-CS-6), §10 (G-L-1/3/4/7)"
  - "reports/specs/02_03_temporal_feature_audit_protocol.md §6.2 history_enriched_pre_game prediction-setting rules, §10 D1-D15 verdicts"
  - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml (provenance.scope = 'All replays (no 1v1/decisive filter)' — confirms history side is multi-game-type)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml (canonical schema metadata; 7 observed length variants 22-28 chars in upstream VARCHAR; TRY_CAST recommended for chronological fidelity)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/06_decision_gates/risk_register_sc2egset.md (RISK-20 cross-region fragmentation, W=30 FAIL verdict)"
  - ".claude/scientific-invariants.md (I3 temporal+normalization; I5 symmetry; I6 SQL provenance; I7 no magic numbers; I8 cross-game; I9 step-derived conclusions; I10 relative-path)"
  - ".claude/ml-protocol.md (three leakage failure modes — rolling, h2h, co-occurring matches)"
  - ".claude/rules/data-analysis-lineage.md (non-batching rule; halt-before-artifact; required structure for every empirical analysis)"
  - ".claude/rules/git-workflow.md"
  - ".claude/rules/python-code.md"
  - ".claude/rules/sql-data.md (replay_id canonical; matches_flat 2-rows-per-game; view-vs-raw discipline)"
  - "docs/TAXONOMY.md"
  - "docs/PHASES.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml (no 02_01_03 row yet)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml (02_01 = complete)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml (Phase 02 = in_progress; Phase 03 = not_started)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md (no 02_01_03 entry yet)"
  - "CHANGELOG.md (current [3.72.0] block describes PR #241 scaffold)"
  - "pyproject.toml (current version = 3.72.0)"
non_batching_sequence_position: "Step 3 of 9 (source/anchor/cold-start adjudication) — follows merged PR #239 ROADMAP-stub + PR #240 Layer-1 scaffold plan + PR #241 Layer-2 scaffold execution. Precedes future materialization-execution plan (step 4), materialization-execution (step 5), CROSS-02-01 post-materialization audit (step 6), §10 verdict re-run or justification (step 7), research_log/STEP_STATUS/manifest closure (step 8), reviewer-deep final gate (step 9)."
deep_research_disclaimer: "External ChatGPT deep-research relevant to SC2_Datasets ToonPlayerDescMap semantics (APM, SQ, supplyCappedPercent, race, selectedRace, MMR, result) is SUPPORTING SEMANTIC CAUTION only. Repo artifacts remain source of truth. result is post-outcome → forbidden as feature. APM/SQ/supplyCappedPercent only as prior-match historical aggregates (CROSS-02-00 §5.4). Target-match tracker/game-event consumption remains in-game and is forbidden for this step."
---

## Scope

This is a **Layer-1 planning PR**. It commits ONLY two files:

- `planning/current_plan.md` (this document)
- `planning/current_plan.critique.md` (produced by reviewer-adversarial in a separate dispatch)

This plan describes the **future Layer-2 adjudication execution PR** on branch
`feat/sc2egset-02-01-03-history-source-anchor-coldstart-adjudication`. The
future Layer-2 PR has an **11-file final tracked diff** — **9 deliverable/execution
files** (notebook pair `.py` + `.ipynb`, adjudicator source module, mirrored test
file, adjudication CSV + MD artifact pair, `planning/INDEX.md`, `CHANGELOG.md`,
`pyproject.toml`) **plus the 2 inherited planning files**
(`planning/current_plan.md` + `planning/current_plan.critique.md` carried
forward from this Layer-1 PR). The notebook `.py` and `.ipynb` count as **two
distinct deliverables** per the PR #234 precedent (B1 contract).

The future Layer-2 PR performs the non-batching sequence step 3 ("the
tranche-2 source/anchor/cold-start adjudication artifact pair"). It is the
tranche-2 analogue of PR #234 (which produced tranche-1's
`02_01_02_source_anchor_race_adjudication.{csv,md}` covering Q1 source layer
/ Q2 anchor / Q3 race column for the 5 pre_game families).

The Layer-2 PR is explicitly **adjudication-only**. It records 8 coupled
pre-materialization decisions (Q1-Q8) for the 6 `history_enriched_pre_game`
families and emits one CSV + one MD artifact pair. It does NOT materialize
any feature value, does NOT write any Parquet, does NOT run the
CROSS-02-01-v1.0.1 post-materialization leakage audit, does NOT touch any
status YAML, does NOT append a `research_log.md` entry, does NOT close Step
02_01_03, does NOT begin Step 02_01_04, does NOT begin Phase 03, does NOT
re-execute the CROSS-02-03 §10 verdict audit, does NOT edit any spec or
cleaning-layer YAML, does NOT edit the ROADMAP, does NOT re-edit the
PR #241 scaffold notebook or validator module (both inputs are
byte-unchanged anchors with SHA-256 provenance recorded).

The 8 Q-decisions, their candidates, falsifiers, evidence paths, and the
adjudication CSV/MD schemas are fully specified in the Execution Steps and
File Manifest sections below.

## Problem Statement

PR #241 (merged on master `3c6709bf`) persisted the Step 02_01_03 scaffold
notebook pair plus a 687-LOC validator module with 16 falsifiers, mirrored
test file (≥30 tests; 98% coverage), and the registry-bound design contract
for the 6 `history_enriched_pre_game` families. The validator binds to the
closed 02_01_01 registry CSV as authoritative; it does NOT pin any
source-layer, anchor, cold-start, cross-region, rating, or
IN_GAME_HISTORICAL-aggregation choice.

The next step in the non-batching sequence (`.claude/rules/data-analysis-lineage.md`
sequence step 3) is the **source/anchor/cold-start adjudication artifact**.
The PR #234 precedent (tranche-1) is unambiguous: 3 decisions (Q1 source
layer, Q2 anchor, Q3 race) were adjudicated in a single CSV + MD pair after
the scaffold validator landed and before the materialization-execution plan
was authored. Tranche-2 mirrors the same pattern with **8 decisions** instead
of 3 — the larger surface reflects the 6-family scope, the strict-`<` history
cutoff, the cold-start gate set, the cross-region fragmentation policy
deferral, the rating-reconstruction algorithm deferral, and the
IN_GAME_HISTORICAL prior-match aggregation discipline.

The 8 questions are coupled. Q1 (source layer) constrains which columns are
available; Q2 (target anchor) and Q3 (historical row time) determine the
strict-`<` filter expression; Q4 (cold-start policy) and Q5 (cross-region
policy) gate the support set for prior-history counts; Q6 (rating
reconstruction model family) determines what `reconstructed_rating` outputs
look like at materialization time; Q7 (IN_GAME_HISTORICAL prior-match
aggregation) determines what `in_game_history_aggregate` outputs look like;
Q8 (`matches_history_minimal` consumption) is the PR #239 ROADMAP-nit
documentation requirement promoted to a binding adjudication row.

The 8 decisions must be adjudicated together (not sequentially across 8 PRs)
because they share evidence (the same DuckDB tables, the same registry CSV,
the same PR #234 binding), and a wrong Q1 choice would invalidate Q2-Q8
evidence. A single adjudication pass with explicit falsifiers per decision
is the methodologically correct atomic unit for this Layer-2 PR.

This Layer-1 PR commits the plan. The Layer-2 PR will implement it. No data
is touched at this layer; no DuckDB query runs; no Parquet is written.

## Assumptions & Unknowns

### Assumptions (BINDING for the Layer-2 PR)

A1. **PR #241 scaffold byte-unchanged.** The validator module
   `src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py`
   (SHA-256 `b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904`)
   is the authoritative scaffold contract. The Layer-2 PR does NOT edit it.
   The 64-char SHA-256 is re-asserted in every adjudication CSV row as
   `pr241_scaffold_validator_module_sha256` (N4).

A2. **Registry CSV is authoritative for tranche-2 scope.** The 6 family IDs
   are the rows 7-12 of `02_01_01_feature_family_registry.csv` (SHA-256
   `320b8b018982f12539a34512421f1b34359bb825f0d1410687492dfe5c6fed1f`):
   - `sc2egset.history_enriched_pre_game.focal_player_history`
   - `sc2egset.history_enriched_pre_game.opponent_player_history`
   - `sc2egset.history_enriched_pre_game.matchup_history_aggregate`
   - `sc2egset.history_enriched_pre_game.reconstructed_rating`
   - `sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling`
   - `sc2egset.history_enriched_pre_game.in_game_history_aggregate`

A3. **Tranche-1 evidence binding (PR #234).** The PR #234 Q1=MFC,
   Q2(a)=`started_at TIMESTAMP` BINDING, Q3=RATIFY decisions are anchored
   inputs. The tranche-2 adjudication may RATIFY, EXTEND, or NARROW these
   choices for the history tranche, but must explicitly cite the
   tranche-1 evidence path (`02_01_02_source_anchor_race_adjudication.csv`
   row by `decision_id`) before deviating.

A4. **Notebook pair = 2 deliverables.** Per PR #234 (which shipped
   `02_01_02_source_anchor_race_adjudication.py` + `.ipynb` as 2 of its
   deliverables), the Layer-2 PR's notebook pair counts as **two distinct
   deliverables** in the 11-file diff. This is the B1 contract. Every
   manifest count uses "11 = 9 deliverable + 2 inherited planning" verbatim.

A5. **Adjudicator module path.**
   `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py`
   (mirroring tranche-1's `adjudicate_pre_game_source_layer.py` filename
   pattern). Public entrypoint
   `adjudicate_history_enriched_pre_game_source_layer(...) ->
   HistoryEnrichedAdjudicationResult` writes CSV + MD via two helpers
   (`_write_csv`, `_write_md`); never writes Parquet.

A6. **Mirrored test path.**
   `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_enriched_pre_game_source_layer.py`
   per project test mirror convention.

A7. **Coverage gate.** ≥95% line coverage on the adjudicator module
   (matching the tranche-1 + PR #241 precedent).

A8. **Notebook discipline.** Jupytext `py:percent` `.py` canonical + paired
   `.ipynb` (outputs cleared); no `def` / `class` / `lambda` in cells; all
   logic imported from the adjudicator module; `print()` only for read-only
   exploration; `logging.getLogger(__name__)` for diagnostics. Per
   `feedback_notebook_iterative_testing.md`, every notebook cell declares
   its hypothesis + falsifier inline before executing.

A9. **CSV/MD provenance.** The CSV columns include `provenance_git_sha`
   (resolved at write time) plus N4 `pr241_scaffold_validator_module_sha256`
   plus `provenance_sha256` fields for every critical input (registry CSV,
   PR #234 binding CSV+MD, methodology risk register, 4 CROSS-02-NN specs,
   3 cleaning-layer YAMLs, DuckDB path). The MD reproduces every cited SQL
   query and its result verbatim (Invariant I6).

A10. **Q-decisions must answer "RATIFY / EXTEND / NARROW / DEFER" per
   decision.** The 8 Q-decisions never silently pin a numeric threshold,
   smoothing pseudocount, Bayesian prior, or rating-model hyperparameter
   (Invariant I7). Where a choice cannot be bound at this layer (Q6 rating
   algorithm), the verdict is `deferred_blocker` per N3 — explicit, not
   silent. Where a choice can be bound (Q1 source layer), the verdict is
   `bind_now` / `extend_with_evidence` with evidence-backed rationale.

A11. **Strict-< filter has one canonical form (B-X2).** The single canonical
   expression for the strict-`<` history filter EVERYWHERE in the
   adjudicator module, smoke probes, evidence bindings, and tests is:
   ```
   TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
   ```
   `TRY_CAST` (not bare `CAST`) is chosen to handle the 7 observed length
   variants 22-28 chars in upstream VARCHAR per
   `matches_history_minimal.yaml`. Any divergence (bare `CAST`, missing
   cast, wrong alias) is rejected by a dedicated falsifier
   `strict_lt_filter_divergence`. Where the ROADMAP raw text contains
   `ph.details_timeUTC < target.started_at` (lex-only form), this plan
   explicitly labels that text as "ROADMAP §02_01_03 raw form (normalized
   by this adjudication plan to the canonical TRY_CAST form for
   chronological fidelity per `matches_history_minimal.yaml`)" and does
   NOT propagate the bare form into any executable site.

### Unknowns (DEFERRED with explicit gating)

U1. **Materialization SQL.** The exact projection SQL for each of the 6
   families is DEFERRED to the future materialization PR (Layer-3+). The
   adjudication CSV records the BINDING source-table choice, anchor, and
   strict-`<` filter; the SQL skeleton is recorded only as a pseudocode
   pattern in the MD §rationale.

U2. **Cold-start numeric thresholds (K, m, α).** Per Invariant I7, every
   threshold must be empirically derived on training folds OR cited from
   literature. Both options are DEFERRED to the materialization PR. The
   adjudication CSV records cold-start POLICY (`fold_aware_fit` /
   `literature_constant` / `deferred_blocker`) without pinning a numeric.

U3. **Q6 rating reconstruction model family.** Per N3, the default verdict
   is `deferred_blocker` unless the future Layer-2 PR's read-only evidence
   gathering produces enough repo/primary-source binding to commit to a
   model family (Elo / Glicko / Glicko-2 / TrueSkill / rolling baseline).
   The ~83.95% MMR-missing density (verified in the dataset research log:
   "is_mmr_missing distribution = (False=7128, True=37290) = 83.95% TRUE")
   makes algorithm choice first-order; no premature pin. **N-X3
   strengthened gate:** when verdict is `deferred_blocker`, evidence_paths
   must be non-empty AND notes must contain explicit deferred-blocker
   rationale ("deferred_blocker because: ..."). When verdict is a model
   family, evidence_paths must contain at least 1 repo path AND at least
   1 primary-source citation (newline-separated; falsifier splits and
   counts), notes must contain forward-only wording, and notes must
   contain explicit cold-start / missingness handling wording.

U4. **Post-materialization CROSS-02-01 audit.** The non-vacuous audit JSON+MD
   covering the 6 history families' materialized columns is DEFERRED to the
   future materialization PR. This adjudication PR writes ZERO entries
   under `reports/artifacts/02_01_03/`.

U5. **§10 verdict-audit re-run vs justification.** The ROADMAP
   `continue_predicate` (lines 2464+) requires either a re-executed §10
   audit over the 6 history rows OR a non-vacuous justification recorded
   in the materialization PR's `research_log` entry. This adjudication PR
   does NOT discharge that obligation; it RECORDS the choice as one
   adjudication row (within Q4 cold-start subfields) for the materialization
   planner to consume.

U6. **Step closure.** The U2.B-style closure PR (adding `02_01_03: complete`
   to `STEP_STATUS.yaml` and the closure entry to dataset `research_log.md`)
   is DEFERRED to a separate post-materialization closure PR per the PR #237
   tranche-1 closure precedent.

U7. **AoE2 cross-game decisions.** This is a sc2egset-scoped tranche-2
   adjudication. CROSS-02-00 cross-game decisions (faction polymorphism,
   per-dataset encoders) are RATIFIED-by-citation only; no new cross-game
   commitment is made.

## Literature Context

This is a methodology-scaffolding adjudication PR; the literature context
is the project's own normative documents (cited verbatim in the
`source_artifacts` frontmatter) plus the cross-spec invariants in
`.claude/scientific-invariants.md`. No external academic citation is
load-bearing for the **adjudication verdict**; literature derivations
(cold-start empirical thresholds K, smoothing pseudocount m, Bayesian
prior strength α, rating-reconstruction hyperparameters) are explicitly
DEFERRED to the materialization PR per Invariant I7.

For the rating reconstruction family (`reconstructed_rating`, G-CS-4), the
candidate algorithms cited at design time are: Elo (Elo 1978), Glicko
(Glickman 1999), Glicko-2 (Glickman 2012), TrueSkill (Herbrich, Minka,
Graepel 2006/2007). The choice between these is **Q6 — default verdict
`deferred_blocker` per N3 (strengthened per N-X3)**. The relevant entries
already exist in `thesis/references.bib`: `Elo1978`, `Glickman1999`,
`Glickman2012`, `Herbrich2006`. These citations are NOT bound at this
layer; the adjudication CSV records `rating_policy = deferred_blocker`
(or the evidence-bound alternative the future Layer-2 PR substantiates
under the strengthened N-X3 evidence gate).

For the cross-region fragmentation handling family (RISK-20), the project's
own evidence is `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/06_decision_gates/risk_register_sc2egset.md`
RISK-20 (cross-region fragmentation; cited at ROADMAP line 2386) plus the
Phase 01 W=30 FAIL verdict cited in CROSS-02-02 §6.2 row 5. No external
citation is required.

The non-batching protocol cited is `.claude/rules/data-analysis-lineage.md`
"Non-batching rule for empirical work" (sequence step 3). The
falsifier-discipline protocol cited is "Required structure for every
empirical analysis" in the same rule (every empirical analysis declares
assumption, measurement claim, sanity check, falsifier, expected artifact,
lineage source, downstream decision).

External ChatGPT deep-research relevant to SC2_Datasets ToonPlayerDescMap
semantics (APM, SQ, supplyCappedPercent, race, selectedRace, MMR, result)
is **supporting semantic caution** only. Repo artifacts remain source of
truth. The semantic notes are recorded in the MD §evidence section as
"external semantic support" without elevating them to binding sources.

## Execution Steps

Each task below describes work to be performed by the Layer-2 executor.
T01-T08 produce the **9 deliverable/execution files**; together with the
**2 inherited planning files** (`planning/current_plan.md` +
`planning/current_plan.critique.md` carried forward from this Layer-1 PR),
the future Layer-2 PR has an **11-file tracked diff**. T09 is the
Layer-2 final-gate dispatch. **None of T01-T09 executes at this Layer-1
PR.** This Layer-1 PR only commits the plan + critique (2 files).

### T01 — Adjudicator module: dataclasses, constants, schema constants

**Objective:** Define module-level constants, the
`HistoryEnrichedAdjudicationResult` frozen dataclass, and the
`HistoryEnrichedAdjudicationDecision` frozen dataclass for one Q-row.
No magic numbers (Invariant I7).

**Instructions:**
1. Create `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py`.
2. Declare module-level constants matching the registry-bound set in PR #241:
   - `HISTORY_TRANCHE2_FAMILY_IDS: frozenset[str]` (re-imported from the
     PR #241 validator module — single source of truth).
   - `EXPECTED_TRANCHE2_COUNT: int = 6`.
   - `IN_GAME_HISTORICAL_AGGREGATED_COLUMNS: tuple[str, ...]` (re-imported
     from PR #241 validator module).
   - `PR241_VALIDATOR_MODULE_PATH: str` (relative path to validator).
   - `EXPECTED_PR241_VALIDATOR_SHA256: str = "b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904"` (N4 binding).
   - **B-X2 canonical strict-`<` constant:**
     `STRICT_LT_HISTORY_FILTER: str = "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"`
     (TRY_CAST — not bare CAST — matches `matches_history_minimal.yaml`
     guidance handling 7 observed length variants 22-28 chars in upstream
     VARCHAR; alias `target` is canonical, NOT `mhm`).
   - `STRICT_LT_FILTER_ROADMAP_RAW: str = "ph.details_timeUTC < target.started_at"`
     (the raw lex-only form quoted from ROADMAP §02_01_03 — recorded
     for provenance ONLY; never used as an executable expression;
     `strict_lt_filter_divergence` falsifier asserts no executable site
     adopts this bare form).
   - `Q_DECISION_IDS: tuple[str, ...] = ("Q1_source_layer", "Q2_target_anchor", "Q3_history_time_column", "Q4_cold_start_policy", "Q5_cross_region_policy", "Q6_rating_policy", "Q7_in_game_historical_policy", "Q8_matches_history_minimal_consumption")`.
   - `ALLOWED_VERDICTS: frozenset[str] = frozenset({"bind_now", "ratify_with_evidence", "extend_with_evidence", "narrow_with_evidence", "deferred_blocker", "deferred_recommendation"})`.
   - `ALLOWED_BINDING_LEVELS: frozenset[str] = frozenset({"binding_for_materialization", "binding_for_phase_03_split", "recommendation_only", "deferred_blocker", "deferred_recommendation"})`.
   - **B-X1 forbidden-token field scope constants:**
     `POST_GAME_TOKEN_SCOPED_FIELDS: tuple[str, ...] = ("selected_source_layer", "selected_target_source_layer", "selected_history_source_layer", "target_anchor", "history_time_column", "feature_family_id_or_scope", "materialized_output_paths", "proposed_feature_columns", "designed_column_names")`
     (note: `proposed_feature_columns` and `designed_column_names` are
     reserved scope — if a successor PR adds either of these fields to
     the schema, it falls under POST-GAME token scanning automatically).
     `POST_GAME_TOKEN_EXEMPT_FIELDS: tuple[str, ...] = ("notes", "evidence_paths", "falsifiers", "decision_name", "rationale", "source_layer_divergence_reason", "history_source_extension_reason")`
     (rationale-bearing fields are EXEMPT — negated prose like "no
     target-match outcome; no future results; no global batch fit" is
     ALLOWED here).
   - `POST_GAME_TOKENS: frozenset[str] = frozenset({"won", "win", "loss", "result", "final_state", "match_result", "post_game", "outcome", "winner", "is_decisive"})` (mirrors PR #241 validator).
   - `ADJUDICATION_CSV_REL: str = "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv"`.
   - `ADJUDICATION_MD_REL: str = "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md"`.
3. Declare `HistoryEnrichedAdjudicationDecision` frozen dataclass with the
   **26-field schema** (N-X4 adds 2 subfields; the future Layer-2 CSV row
   schema is exactly this dataclass's `astuple()` ordering, with the
   `notes` field as the 27th field carrying free-text rationale — the
   header therefore has 27 columns, `wc -l` on the CSV is `9` = 1 header
   + 8 rows):
   - `decision_id: str` (one of Q_DECISION_IDS)
   - `decision_name: str`
   - `verdict: str` (one of ALLOWED_VERDICTS)
   - `binding_level: str` (one of ALLOWED_BINDING_LEVELS)
   - `feature_family_id_or_scope: str` (six-family scope or single-family id)
   - `selected_source_layer: str` (Q1 only; "" for others) — kept as a
     row-level shorthand for backward-compat with PR #234 schema; the
     authoritative target/history fields are below
   - `selected_target_source_layer: str` (N5 subfield)
   - `selected_history_source_layer: str` (N5 subfield)
   - `target_history_asymmetry: str` (N5 subfield; "symmetric" / "asymmetric" / "")
   - **`source_layer_divergence_reason: str` (N-X4 NEW; Q1 only; "" otherwise)**
     — captures operational divergence between registry-recorded source
     (`matches_flat`) and operationally-used source (`matches_flat_clean`).
   - **`history_source_extension_reason: str` (N-X4 NEW; Q1 only; "" otherwise)**
     — captures the tranche-1 → tranche-2 extension (adding
     `player_history_all` as the history-side source).
   - `target_anchor: str` (Q2 only; "" for others)
   - `history_time_column: str` (Q3 only; "" for others — value cites
     the canonical TRY_CAST expression per B-X2)
   - `cold_start_policy: str` (Q4 only; structured `G-CS-2:..|G-CS-3:..|G-CS-4:..|G-CS-5:..|G-CS-6:..`)
   - `cross_region_policy: str` (Q5 only; one of "strict_exclusion" / "dual_feature_path" / "sensitivity_indicator_co_registration" / "deferred_blocker")
   - `rating_policy: str` (Q6 only; one of "elo" / "glicko" / "glicko2" / "trueskill" / "rolling_winrate_baseline" / "deferred_blocker")
   - `in_game_historical_policy: str` (Q7 only; one of "prior_match_only_strict_lt" / "deferred_blocker")
   - `in_game_historical_columns_in_scope: str` (N1; Q7 only; deterministic pipe-separated `APM|SQ|supplyCappedPercent|header_elapsedGameLoops`)
   - `evidence_paths: str` (newline-separated repo-relative paths)
   - `falsifiers: str` (newline-separated `name:status` pairs)
   - `audit_pr: str` (the future Layer-2 PR # placeholder, filled at write time)
   - `pr241_scaffold_validator_module_sha256: str` (N4; 64-char lowercase hex)
   - `provenance_git_sha: str` (resolved at write time)
   - `materialized_output_paths: str` (always `""` — adjudication writes ZERO materialized data)
   - `notes: str` (free-text deferral rationale / non-substitution disclaimer reference)
4. Declare `HistoryEnrichedAdjudicationResult` frozen dataclass containing:
   - `decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]` (exactly 8 entries; one per Q-decision)
   - `csv_path: str`
   - `md_path: str`
   - `provenance_git_sha: str`
   - `pr241_scaffold_validator_module_sha256: str`
   - `falsifiers_fired: tuple[str, ...]` (every fired falsifier)
   - `halting_falsifier: str | None`
   - `passed: bool`
5. Type hints on every signature; Google-style docstrings on every public
   surface; constants in UPPER_SNAKE_CASE.

**Verification:**
- `source .venv/bin/activate && poetry run python -c "from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import Q_DECISION_IDS, EXPECTED_PR241_VALIDATOR_SHA256, STRICT_LT_HISTORY_FILTER, POST_GAME_TOKEN_SCOPED_FIELDS, POST_GAME_TOKEN_EXEMPT_FIELDS; assert len(Q_DECISION_IDS) == 8 and len(EXPECTED_PR241_VALIDATOR_SHA256) == 64 and 'TRY_CAST' in STRICT_LT_HISTORY_FILTER and 'target.started_at' in STRICT_LT_HISTORY_FILTER and 'notes' in POST_GAME_TOKEN_EXEMPT_FIELDS and 'evidence_paths' in POST_GAME_TOKEN_EXEMPT_FIELDS"` returns exit 0.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py` (PR #241; constants re-imported)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv` (PR #234 format precedent)
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml` (B-X2 canonical form provenance)

### T02 — Adjudicator module: evidence-loading helpers + per-Q falsifiers (Q1, Q2, Q3, Q8)

**Objective:** Implement read-only DuckDB / Parquet / CSV probes for Q1
(source layer), Q2 (target anchor), Q3 (history time column), Q8
(`matches_history_minimal` consumption). Each probe returns a typed
evidence record; no writes. Per-Q falsifiers attach to each probe.

**Instructions:**
1. Implement `_load_pr234_binding_csv(path: Path) -> dict[str, dict[str, str]]` returning Q1/Q2/Q3 decision dicts from the tranche-1 adjudication CSV.
2. Implement `_load_registry_csv(path: Path) -> list[dict[str, str]]` loading the closed 02_01_01 registry.
3. Implement `_probe_view_row_counts(con: duckdb.DuckDBPyConnection) -> dict[str, int]` running:
   - `SELECT COUNT(*) FROM matches_flat_clean` (expect 44418).
   - `SELECT COUNT(*) FROM matches_history_minimal` (expect 44418).
   - `SELECT COUNT(*) FROM player_history_all` (expect 44817).
   - `SELECT COUNT(DISTINCT replay_id) FROM matches_flat_clean` (expect 22209).
   Mirror the tranche-1 PR #234 probe pattern verbatim.
4. Implement `_probe_history_time_column_candidates(con) -> dict[str, dict[str, object]]` returning DESCRIBE-style metadata for `player_history_all.details_timeUTC`, `matches_history_minimal.started_at`, and any candidate history-time column. Record dtype and null count for each.
5. **B-X2 canonical smoke probe.** Implement `_probe_strict_lt_filter_smoke(con) -> dict[str, int]` running a small read-only smoke pair to demonstrate the strict-`<` semantics yields 0 self-rows. SQL string is built as a single string constant and MUST use the canonical form (B-X2) verbatim — `target` alias (not `mhm`) and `TRY_CAST`. The text the falsifier `strict_lt_filter_divergence` checks against the canonical constant `STRICT_LT_HISTORY_FILTER`:
   ```sql
   SELECT COUNT(*) FROM player_history_all ph
   JOIN matches_history_minimal target ON ph.toon_id = target.player_id
   WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
     AND ph.replay_id = REPLACE(target.match_id, 'sc2egset::', '')
   ```
   Expected: 0 (the only row where `ph.details_timeUTC = target.started_at`
   is the target row itself, excluded by strict-`<`). The probe stores
   the SQL string verbatim in its returned dict for cross-site falsifier
   inspection.
6. Implement `_probe_matches_history_minimal_columns(con) -> list[str]` listing MHM columns to substantiate Q8 (the consumption documentation).
7. Implement per-Q falsifier helpers, each returning `(bool_did_fire, message)`:
   - `_check_q1_source_layer_evidence_consistent(pr234_binding, registry, view_counts) -> tuple[bool, str]` — Q1 evidence must reconcile with PR #234 Q1 binding (MFC); if registry source is `matches_flat` but PR #234 binding is `matches_flat_clean`, record the divergence and verdict `extend_with_evidence` (cleaned-raw is operationally chosen; raw is registry-recorded). The divergence rationale is recorded in `source_layer_divergence_reason` (N-X4).
   - `_check_q2_target_anchor_type_match(pr234_binding, view_metadata) -> tuple[bool, str]` — Q2 must verify `started_at` TIMESTAMP type via DESCRIBE.
   - `_check_q3_history_time_column_dtype(history_time_metadata) -> tuple[bool, str]` — Q3 must verify `ph.details_timeUTC` exists with non-null dtype; record VARCHAR-to-TIMESTAMP TRY_CAST assumption (B-X2 canonical).
   - `_check_q3_monotonicity_smoke(con) -> tuple[bool, str]` — Q3 must verify the cast `TRY_CAST(ph.details_timeUTC AS TIMESTAMP)` succeeds on a 1000-row sample (read-only), AND the count of TRY_CAST failures (NULL returns) is 0 on that sample. If TRY_CAST returns NULL on any sample row, the falsifier fires and the bound expression must be revised (e.g., upstream cleaning step required) before proceeding.
   - `_check_in_game_historical_strict_lt(rows) -> tuple[bool, str]` — **N2 falsifier; Q7-specific**. Verifies that the `in_game_history_aggregate` decision row's `cold_start_policy` and `in_game_historical_policy` together encode strict-`<` semantics for IN_GAME_HISTORICAL prior-match aggregation (NOT a runtime SQL check; a row-text check on the adjudication decision). Distinct from any generic `_check_strict_lt_policy`.
   - `_check_q8_mhm_documented(mhm_cols, decision_row) -> tuple[bool, str]` — Q8 must verify the adjudication row's `notes` field cites both `matches_history_minimal` purposes per the PR #239 ROADMAP nit (cold-start enumeration + row-identity anchor) and that `feature_family_id_or_scope` says "NOT a feature source unless explicitly justified".

**Verification:**
- `source .venv/bin/activate && poetry run ruff check src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` exit 0.
- `source .venv/bin/activate && poetry run mypy src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` exit 0.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` (updated)

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb` (read-only via `duckdb.connect(read_only=True)`)
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml`

### T03 — Adjudicator module: per-Q falsifiers (Q4, Q5, Q6, Q7), POST-GAME rejection, tracker rejection, strict-< canonical-form falsifier

**Objective:** Implement falsifiers for cold-start (Q4), cross-region (Q5),
rating (Q6 with N-X3-strengthened evidence gate), IN_GAME_HISTORICAL (Q7),
plus universal leakage falsifiers (B-X1-scoped forbidden-token rejection,
tracker source rejection, and the B-X2 canonical-form `strict_lt_filter_divergence`
falsifier).

**Instructions:**
1. Implement `_check_q4_cold_start_gates_complete(decision_row, registry_rows) -> tuple[bool, str]` — Q4's `cold_start_policy` field must encode a policy for every gate in {G-CS-2, G-CS-3, G-CS-4, G-CS-5}; G-CS-6 (the materialization-time fold-aware fit gate per ROADMAP lines 2334-2338) is documented but explicitly distinguished from registry-time gates (PR #241 validator N2 precedent).
2. Implement `_check_q4_no_leakage_in_cold_start(decision_row) -> tuple[bool, str]` — Q4 must explicitly state that the cold-start support set uses ONLY `match_time < T` evidence per Invariant I3 (`.claude/ml-protocol.md` rolling-aggregate failure mode 1).
3. Implement `_check_q5_cross_region_three_options_enumerated(decision_row) -> tuple[bool, str]` — Q5 must enumerate the three CROSS-02-02 §6.2 row 5 options (strict-exclusion / dual-feature-path / sensitivity-indicator-co-registration) and either select one (verdict `bind_now`) with retention-measurement evidence or defer (verdict `deferred_blocker`) with rationale.
4. **N-X3 strengthened.** Implement `_check_q6_rating_default_deferred(decision_row) -> tuple[bool, str]` — **N3 + N-X3 falsifier**. Q6 evidence sufficiency gate:
   - If `rating_policy == "deferred_blocker"`: PASSES iff `evidence_paths != ""` AND notes contain explicit deferred-blocker rationale matching the substring `"deferred_blocker because:"` (case-sensitive token-search).
   - If `rating_policy IN {"elo", "glicko", "glicko2", "trueskill", "rolling_winrate_baseline"}`: HALTS unless ALL of:
     (a) `evidence_paths` contains at least 1 line whose value matches `^(src/|reports/|sandbox/|thesis/|tests/|docs/|\.claude/)` (a repo path) AND at least 1 line whose value matches `^@\w+|\\cite\{|^[A-Z][a-z]+\d{4}` or contains parenthetical year (e.g., `Glickman (2012)`) signaling a primary-source citation; the falsifier splits `evidence_paths` on newline and counts.
     (b) Notes contain explicit forward-only constraint wording per `_check_q6_rating_forward_only` companion check (`"no target-match outcome"`, `"no future results"`, `"no global batch fit"`).
     (c) Notes contain explicit cold-start / missingness handling wording (e.g., the substring `"cold-start handled by"` AND `"missingness handled by"`).
   - The plan's overall recommendation (T05 Q6) stays `deferred_blocker` for this Layer-2 PR.
5. Implement `_check_q6_rating_forward_only(decision_row) -> tuple[bool, str]` — Q6 must explicitly forbid future results / target-match outcome / global batch fit. The falsifier rejects the row if the rationale `notes` field omits the forward-only constraint (substring match of all three required phrases: `"no target-match outcome"`, `"no future results"`, `"no global batch fit"`). Per B-X1 exempt-fields rule, these negated-prose tokens are ALLOWED in `notes` (the rationale-bearing field is exempt from the universal POST-GAME token scan).
6. Implement `_check_q7_in_game_historical_columns_in_scope(decision_row) -> tuple[bool, str]` — **N1 falsifier**. Q7's `in_game_historical_columns_in_scope` field must equal the deterministic pipe-separated `APM|SQ|supplyCappedPercent|header_elapsedGameLoops`. The falsifier rejects on any drift (alphabetical reorder counts as drift unless the policy is updated to declare alphabetical canonical order).
7. Implement `_check_q7_no_target_match_tracker(decision_row) -> tuple[bool, str]` — Q7 must explicitly state that IN_GAME_HISTORICAL columns are consumed ONLY from prior matches (`history_time < target_time`), never from the target match. The falsifier rejects on missing or contradicting wording.
8. **B-X1: renamed + scoped forbidden-token falsifier.** Implement `_check_forbidden_post_game_feature_tokens(decisions) -> tuple[bool, str]` — renamed from `_check_universal_no_post_game_token`. Scans only the fields in `POST_GAME_TOKEN_SCOPED_FIELDS` for any token in `POST_GAME_TOKENS`. EXPLICITLY exempts every field in `POST_GAME_TOKEN_EXEMPT_FIELDS` — `notes`, `evidence_paths`, `falsifiers`, `decision_name`, `rationale`, `source_layer_divergence_reason`, `history_source_extension_reason`. Negated prose (`"no target-match outcome"`, `"no future results"`, `"no global batch fit"`, `"forbid result"`, `"reject winner field"`) is ALLOWED in any exempt field. The falsifier message names the offending field and token when it fires.
9. Implement `_check_universal_no_tracker_source(decisions) -> tuple[bool, str]` — universal falsifier rejecting any `selected_source_layer`, `selected_target_source_layer`, or `selected_history_source_layer` containing `tracker_events_raw` (Invariant I3; Amendment 2 of PR #208).
10. Implement `_check_pr241_sha256_match(decision_rows) -> tuple[bool, str]` — **N4 falsifier**. Every decision row's `pr241_scaffold_validator_module_sha256` must equal `EXPECTED_PR241_VALIDATOR_SHA256` (64-char lowercase hex `b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904`). Reject `NOT_FOUND` / empty / wrong-length / wrong-case / mismatched values.
11. Implement `_check_q1_single_row_per_n5(decisions) -> tuple[bool, str]` — **N5 falsifier**. Q1 must be exactly ONE row with subfields `selected_target_source_layer`, `selected_history_source_layer`, `target_history_asymmetry`, `source_layer_divergence_reason`, `history_source_extension_reason` populated (the last two are N-X4 additions). Reject any split into Q1a / Q1b / Q1c.
12. **B-X2 new falsifier.** Implement `_check_strict_lt_filter_divergence(decisions, smoke_probe_sql, q3_bound_expression, q7_bound_expression) -> tuple[bool, str]` — fires if ANY of these three sites — (a) the `STRICT_LT_HISTORY_FILTER` constant, (b) the T02 step 5 smoke probe SQL string, (c) the T05 Q3/Q7 bound expression strings — deviates from the canonical form
   ```
   TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
   ```
   modulo allowed whitespace (the falsifier normalizes runs of whitespace
   to a single space before comparison). Specifically rejects:
   - bare `CAST` (without `TRY_`)
   - missing cast altogether (lex-only `ph.details_timeUTC < target.started_at`)
   - wrong alias (e.g., `mhm.started_at` instead of `target.started_at`)
   - capitalization variants (e.g., `try_cast`)
   When firing, the message names the offending site and quotes the divergent text.

### T03b — HELPER_TO_FALSIFIER_KEY mapping table (N-X1)

**Objective:** Declare an explicit literal mapping from helper-function names
to the falsifier keys they report, so the priority chain and tests can refer
to a single source of truth.

**Instructions:** Declare a module-level `HELPER_TO_FALSIFIER_KEY: dict[str, str]` constant with the following literal contents (asserted by `TestHelperToFalsifierKeyMappingIsComplete`):

| Helper function | Falsifier key |
|---|---|
| `_check_q1_source_layer_evidence_consistent` | `q1_source_layer_evidence_inconsistent` |
| `_check_q1_single_row_per_n5` | `q1_single_row_violation` |
| `_check_q2_target_anchor_type_match` | `q2_target_anchor_type_mismatch` |
| `_check_q3_history_time_column_dtype` | `q3_history_time_column_invalid` |
| `_check_q3_monotonicity_smoke` | `q3_strict_lt_smoke_failed` |
| `_check_q4_cold_start_gates_complete` | `q4_cold_start_gates_incomplete` |
| `_check_q4_no_leakage_in_cold_start` | `q4_cold_start_leakage` |
| `_check_q5_cross_region_three_options_enumerated` | `q5_cross_region_three_options_not_enumerated` |
| `_check_q6_rating_default_deferred` | `q6_rating_default_deferred_violated` |
| `_check_q6_rating_forward_only` | `q6_rating_forward_only_missing` |
| `_check_q7_in_game_historical_columns_in_scope` | `q7_in_game_historical_columns_drift` |
| `_check_q7_no_target_match_tracker` | `q7_no_target_match_tracker_missing` |
| `_check_in_game_historical_strict_lt` | `in_game_historical_strict_lt_violated` |
| `_check_q8_mhm_documented` | `q8_mhm_documentation_missing` |
| `_check_forbidden_post_game_feature_tokens` | `universal_post_game_token_in_scoped_field` |
| `_check_universal_no_tracker_source` | `universal_tracker_source_in_history` |
| `_check_pr241_sha256_match` | `pr241_sha256_mismatch` |
| `_check_strict_lt_filter_divergence` | `strict_lt_filter_divergence` |
| `_check_materialization_creep` | `materialization_creep` |
| `_check_decision_count` | `decision_count_mismatch` |

**Verification:**
- `source .venv/bin/activate && poetry run python -c "from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import HELPER_TO_FALSIFIER_KEY; assert len(HELPER_TO_FALSIFIER_KEY) == 20 and HELPER_TO_FALSIFIER_KEY['_check_strict_lt_filter_divergence'] == 'strict_lt_filter_divergence' and HELPER_TO_FALSIFIER_KEY['_check_forbidden_post_game_feature_tokens'] == 'universal_post_game_token_in_scoped_field'"` exit 0.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` (updated)

### T04 — Adjudicator module: writers (CSV + MD); public entrypoint; falsifier priority

**Objective:** Implement `_write_csv`, `_write_md`, and the public entrypoint
`adjudicate_history_enriched_pre_game_source_layer(...)`. Falsifier priority
ordering is explicit and structural-before-content. Bytes-deterministic output
modulo allowed provenance fields.

**Instructions:**
1. Implement `_write_csv(decisions, csv_path) -> None` writing the 8 rows in `Q_DECISION_IDS` order with the **27-column** schema from T01 step 3 (26 dataclass fields + `notes` = 27). CSV must use `\n` line endings and ASCII (UTF-8 NFC) with no BOM; rows sorted by `decision_id` (which equals `Q_DECISION_IDS` order). Field order matches the dataclass field declaration order (deterministic).
2. Implement `_write_md(decisions, md_path, evidence_blob) -> None` writing the MD with sections:
   - `§1 Non-Overclaim Disclaimer` (verbatim non-materialization disclaimer).
   - `§2 — §9` — one section per Q-decision (Q1 through Q8) with verdict / binding_level / rationale / SQL evidence (verbatim from `evidence_blob` per Invariant I6). All strict-`<` SQL quoted in MD uses the canonical B-X2 TRY_CAST form.
   - `§10 Falsifier Roll-Call` (every falsifier listed with `did_fire` / `did_not_fire` status; mirror PR #234 §5 precedent; entries iterate `HELPER_TO_FALSIFIER_KEY.values()` for completeness).
   - `§11 Lineage Position` (artifact #N in the lineage chain for Step 02_01_03 readiness, with explicit PR # placeholders).
   - `§12 Explicit Non-Substitution Statement` — does NOT replace PR #229 §10 audit, PR #230 vacuous CROSS-02-01 audit, PR #234 tranche-1 adjudication, PR #236 tranche-1 materialization+audit, PR #237 tranche-1 closure, PR #241 scaffold + validator, nor the FUTURE materialization + post-materialization CROSS-02-01 audit (which do not yet exist).
   - `§13 Materialization Blocked Until Deferred-Blocker Resolved` — explicit statement: if any decision row carries `verdict == "deferred_blocker"`, the future Layer-3 materialization PR must NOT proceed until that decision is upgraded to `bind_now` / `ratify_with_evidence` / `extend_with_evidence` / `narrow_with_evidence` in a successor adjudication PR.
   - `§14 No Step Closure Claim` — explicit statement that Step 02_01_03 remains OPEN; this PR does NOT add `02_01_03: complete` to `STEP_STATUS.yaml`.
3. Implement `adjudicate_history_enriched_pre_game_source_layer(duckdb_path, registry_csv_path, pr234_binding_csv_path, csv_path, md_path, audit_pr, audit_date) -> HistoryEnrichedAdjudicationResult`:
   - Open DuckDB read-only.
   - Run T02 + T03 evidence probes.
   - Construct 8 `HistoryEnrichedAdjudicationDecision` instances based on probe outcomes plus the adjudication policy spelled out in this plan's §"Required adjudication-decision rows (Q1-Q8)" mirror in T05 below.
   - Run every falsifier in priority order (structural before per-row; see below).
   - If any falsifier fires, set `halting_falsifier` and abort BEFORE writing CSV/MD (halt-before-artifact per `.claude/rules/data-analysis-lineage.md`).
   - Otherwise write CSV + MD, populate `HistoryEnrichedAdjudicationResult`, return.
4. **Falsifier priority chain (structural before content; first to fire halts).** All entries reference the `HELPER_TO_FALSIFIER_KEY` mapping (N-X1):
   - `pr241_sha256_mismatch` (N4) — every decision row must carry the correct SHA-256.
   - `decision_count_mismatch` — exactly 8 decisions, no more no fewer.
   - `q1_single_row_violation` (N5) — Q1 must be one row with subfields (including the 2 N-X4 subfields).
   - `q1_source_layer_evidence_inconsistent` — Q1 must reconcile with PR #234 binding.
   - **`strict_lt_filter_divergence` (B-X2 NEW)** — constant + T02 smoke SQL + T05 Q3/Q7 bound expressions must all use the canonical TRY_CAST form. Runs structurally BEFORE Q2/Q3 type checks because divergence here invalidates downstream Q3/Q7 evidence.
   - `q2_target_anchor_type_mismatch` — Q2 must verify `started_at` TIMESTAMP type.
   - `q3_history_time_column_invalid` — Q3 must verify `ph.details_timeUTC` dtype.
   - `q3_strict_lt_smoke_failed` — Q3 smoke must show strict-`<` semantics yields 0 self-rows AND TRY_CAST returns 0 NULLs on 1000-row sample.
   - `q4_cold_start_gates_incomplete` — Q4 must cover G-CS-2..5 (G-CS-6 distinguished).
   - `q4_cold_start_leakage` — Q4 must explicitly state `match_time < T` only.
   - `q5_cross_region_three_options_not_enumerated` — Q5 must enumerate 3 options.
   - `q6_rating_default_deferred_violated` (N3 + N-X3) — Q6 verdict default `deferred_blocker` unless evidence-bound per strengthened gate.
   - `q6_rating_forward_only_missing` — Q6 must forbid future / target-match / global batch fit.
   - `q7_in_game_historical_columns_drift` (N1) — Q7 columns must equal `APM|SQ|supplyCappedPercent|header_elapsedGameLoops`.
   - `q7_no_target_match_tracker_missing` — Q7 must forbid target-match tracker consumption.
   - `in_game_historical_strict_lt_violated` (N2) — Q7-specific strict-`<` falsifier (NOT generic `_check_strict_lt_policy`).
   - `q8_mhm_documentation_missing` — Q8 must document both MHM purposes per PR #239 nit.
   - **`universal_post_game_token_in_scoped_field` (B-X1 RENAMED + SCOPED)** — no decision-row scoped field contains a POST-GAME token; rationale-bearing exempt fields explicitly allowed to carry negated prose.
   - `universal_tracker_source_in_history` — no `selected_source_layer` / `selected_target_source_layer` / `selected_history_source_layer` contains `tracker_events_raw`.
   - `materialization_creep` — no decision row has `materialized_output_paths != ""`.
5. Use `LOGGER = logging.getLogger(__name__)`; emit one DEBUG line per probe.

**Verification:**
- `source .venv/bin/activate && poetry run ruff check src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` exit 0.
- `source .venv/bin/activate && poetry run mypy src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` exit 0.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` (updated)

**Read scope:**
- (no new file reads)

### T05 — Adjudicator module: bind the 8 Q-decisions per this plan

**Objective:** Hard-bind the 8 Q-decision content (verdicts, binding levels,
rationales, evidence paths, falsifier roll-call) inside the adjudicator
module so the Layer-2 executor produces a deterministic CSV+MD pair when the
falsifier chain passes. The decisions are RECOMMENDED below; the Layer-2
executor MUST audit them against fresh DuckDB / Parquet / spec evidence
before binding and revise any decision whose falsifier fires.

**Instructions:**

For each Q-decision below, the Layer-2 executor MUST:
(a) load probe evidence (T02);
(b) run per-Q falsifiers (T03 + T03b mapping);
(c) bind the verdict only if falsifiers do not fire;
(d) on any falsifier hit, halt and revise the decision per the
    fix-forward rule.

**Q1 — Source layer (one row per N5; N-X4 subfields populated).**

- `decision_id = "Q1_source_layer"`.
- `decision_name = "History-enriched pre_game source layer (target row + history row + asymmetry; divergence + extension annotated)"`.
- `feature_family_id_or_scope = "all_six_history_enriched_pre_game_families"`.
- Recommended `verdict = "extend_with_evidence"`; `binding_level = "binding_for_materialization"`.
- `selected_target_source_layer` = `"matches_flat_clean"` (RATIFY tranche-1 PR #234 Q1 binding; cleaned-raw, 1v1-scoped, 44,418 rows).
- `selected_history_source_layer` = `"player_history_all"` (per ROADMAP line 2367 `inputs.duckdb_tables`; row count 44,817 per PR #234 probe §2; per CROSS-02-02 §6.2 rows 1-4 + 6 all explicitly source from `player_history_all`).
- **`target_history_asymmetry = "asymmetric"`** with `binding_level = "binding_for_materialization"`.

  **N-X2 Option A (RECOMMENDED, BINDING) — verbatim spec evidence below.**

  - **Verbatim spec passage 1** (`reports/specs/02_02_feature_engineering_plan.md` §6.2 row 1, `focal_player_history`):
    > "rolling/expanding aggregates over `player_history_all` rows for the focal `toon_id`: prior match count, prior win rate, time since prior match, race-conditional win rate, map-conditional win rate, matchup-conditional win rate"
  - **Verbatim spec passage 2** (`reports/specs/02_02_feature_engineering_plan.md` §6.2 row 4, `reconstructed_rating`):
    > "derived from `player_history_all.result` filtered by I3 anchor"
  - **Verbatim spec passage 3** (`reports/specs/02_02_feature_engineering_plan.md` §6.2 row 6, `in_game_history_aggregate`):
    > "`player_history_all.APM` / `SQ` / `supplyCappedPercent` / `header_elapsedGameLoops` (IN_GAME_HISTORICAL classification per CROSS-02-00 §5.4)"
  - **Verbatim spec passage 4** (`reports/specs/02_00_feature_input_contract.md` §2.1 sc2egset row 2):
    > Row grain | 1 row per player per match (all game types; no 1v1 filter)
  - **Verbatim view-schema passage** (`src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml` `provenance.scope`):
    > "All replays (no 1v1/decisive filter). Includes non-1v1 and indecisive replays excluded from matches_flat_clean."

  - **Alternative A (RECOMMENDED, BINDING):** asymmetric — target = `matches_flat_clean` (1v1-scoped, 44,418 rows; cleaning per PR #234 §3), history = `player_history_all` (all-game-types; 44,817 rows; per CROSS-02-02 §6.2 rows 1-4 + 6 all source from `player_history_all`; per CROSS-02-00 §2.1 the row grain note "1 row per player per match (all game types; no 1v1 filter)" makes the all-game-types property authoritative). **Rationale (quoted spec):** every history-side row of §6.2 binds to `player_history_all`; the row-grain note is explicit; the view-schema scope note is explicit.

  - **Alternative B (REJECTED):** symmetric — target and history both filtered to 1v1-only (e.g., both via `matches_flat_clean` or both via a hypothetical `player_history_1v1_only` view). **Rationale why rejected (evidence-cited):** the spec §6.2 row 1 binds history to `player_history_all`, not a 1v1-filtered subset; restricting history to 1v1-only would truncate the player's prior-skill signal in the regime where MMR-missing density is 83.95%, leaving cold-start gates G-CS-2/G-CS-3 with near-empty support sets for newcomers; CROSS-02-02 §6.2 retains multi-game-type history precisely to mitigate this support-set sparsity, and the `player_history_all.yaml` `provenance.scope` note explicitly retains non-1v1 and indecisive replays for this purpose. Rejecting Alternative B would also contradict the verbatim CROSS-02-02 §6.2 rows 4 and 6 (`reconstructed_rating` and `in_game_history_aggregate` both source from `player_history_all`).

- `source_layer_divergence_reason` (N-X4) = `"matches_flat_clean (operationally) vs matches_flat (registry); cleaned-view chosen for 1v1-scoping + 44,418-row deterministic count per PR #234 §3 binding (selected_source_layer = matches_flat_clean was BINDING in tranche-1)"`.
- `history_source_extension_reason` (N-X4) = `"tranche-1 (5 pre_game families) had no history-side source; tranche-2 (6 history-enriched families) adds player_history_all as the history-side source per ROADMAP line 2367 inputs.duckdb_tables and CROSS-02-02 §6.2 rows 1-4 + 6 verbatim source bindings"`.
- The Q1 `verdict = "extend_with_evidence"` now unambiguously refers to the **history-side extension** (adding `player_history_all`); the source-layer divergence (registry-recorded `matches_flat` vs operationally-used `matches_flat_clean`) is documented separately in `source_layer_divergence_reason` as RATIFY-with-divergence-noted (N-X4 disambiguation).
- Evidence paths: PR #234 binding CSV + MD; CROSS-02-00 §2.1; CROSS-02-02 §6.2 rows 1, 4, 6; ROADMAP lines 2363-2367; `player_history_all.yaml` `provenance.scope`.
- Falsifiers: `q1_source_layer_evidence_inconsistent`, `q1_single_row_violation` (N5).
- Notes: cites PR #234 evidence; explicit asymmetry rationale per Option A verbatim quotes above; mentions Alternative B and its rejection. **Per B-X1 the notes field is EXEMPT** from POST-GAME token scanning, so the phrase "indecisive replays" quoted from the schema is allowed here.

**Q2 — Target temporal anchor.**

- `decision_id = "Q2_target_anchor"`.
- `decision_name = "Target match temporal anchor for the strict-< history filter"`.
- `feature_family_id_or_scope = "all_six_history_enriched_pre_game_families"`.
- Recommended `verdict = "ratify_with_evidence"`; `binding_level = "binding_for_materialization"`.
- `target_anchor = "matches_history_minimal.started_at TIMESTAMP"` (RATIFY tranche-1 PR #234 Q2(a) BINDING; per CROSS-02-00 §3.1 canonical cross-dataset dtype).
- Evidence: PR #234 §3 SQL probe results (DESCRIBE TIMESTAMP type, 0 nulls, 0 cross-row inconsistency).
- Falsifiers: `q2_target_anchor_type_mismatch`.
- Notes: ratifies tranche-1 Phase-02 row-identity anchor; Phase-03 hold-out anchor (Q2(b) per PR #234) remains RECOMMENDATION ONLY.

**Q3 — Historical row time column (B-X2 canonical form binding).**

- `decision_id = "Q3_history_time_column"`.
- `decision_name = "Historical row time column for strict-< filter (canonical TRY_CAST form)"`.
- `feature_family_id_or_scope = "all_six_history_enriched_pre_game_families"`.
- Recommended `verdict = "bind_now"`; `binding_level = "binding_for_materialization"`.
- `history_time_column = "player_history_all.details_timeUTC (TRY_CAST AS TIMESTAMP for comparison with target.started_at)"`.
- **Strict-`<` filter expression (CANONICAL per B-X2):**
  ```
  TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
  ```
  This is exactly `STRICT_LT_HISTORY_FILTER`. The ROADMAP §02_01_03 raw form
  `ph.details_timeUTC < target.started_at` is recorded for provenance ONLY
  (as `STRICT_LT_FILTER_ROADMAP_RAW`); this plan explicitly NORMALIZES that
  raw form to the canonical TRY_CAST expression for chronological fidelity
  per `matches_history_minimal.yaml` (which notes 7 observed length variants
  22-28 chars in upstream VARCHAR; lex comparison is NOT chronologically
  faithful). Any executable site adopting the bare form is rejected by
  `strict_lt_filter_divergence`.
- Evidence: T02 step 5 strict-`<` smoke probe (expect 0 self-rows; canonical SQL); spec §5.4 sc2egset PH `details_timeUTC` row (CONTEXT, VARCHAR, "I3 anchor"); `matches_history_minimal.yaml` schema metadata note on TRY_CAST.
- Falsifiers: `q3_history_time_column_invalid`, `q3_strict_lt_smoke_failed`, `strict_lt_filter_divergence` (B-X2 NEW).
- Notes: VARCHAR-to-TIMESTAMP TRY_CAST assumption recorded; deterministic ordering via `(player_id_worldwide, TRY_CAST(ph.details_timeUTC AS TIMESTAMP), ph.replay_id)`; 1000-row TRY_CAST NULL-rate sanity probe required (`q3_strict_lt_smoke_failed` halts if any NULL).

**Q4 — Cold-start policy.**

- `decision_id = "Q4_cold_start_policy"`.
- `decision_name = "Cold-start policy per family (G-CS-2/3/4/5; G-CS-6 distinguished as materialization-time gate)"`.
- `feature_family_id_or_scope = "all_six_history_enriched_pre_game_families"` with per-family annotation in `cold_start_policy`.
- Recommended `verdict = "extend_with_evidence"`; `binding_level = "binding_for_materialization"`.
- `cold_start_policy = "G-CS-2:scaffold_registry_gate_for_focal_player_history+opponent_player_history+in_game_history_aggregate|G-CS-3:scaffold_registry_gate_for_matchup_history_aggregate|G-CS-4:scaffold_registry_gate_for_reconstructed_rating|G-CS-5:scaffold_registry_gate_for_cross_region_fragmentation_handling|G-CS-6:materialization_time_fold_aware_fit_gate_per_invariant_I3_and_CROSS-02-02_section_9"`.
- Distinguish: scaffold registry gates G-CS-2/3/4/5 (registry-time; bound here); G-CS-6 (materialization-time fold-aware fit gate per ROADMAP lines 2334-2338; DEFERRED to materialization PR); model-training Phase-03 cold-start handling (DEFERRED to Phase 03 planning).
- Evidence: registry CSV rows 7-12; CROSS-02-02 §9 G-CS-2..6; ROADMAP lines 2334-2338.
- Falsifiers: `q4_cold_start_gates_incomplete`, `q4_cold_start_leakage`.
- Notes: ML-protocol three failure modes (rolling, h2h, co-occurring matches) explicitly forbidden; only `match_time < T` evidence used. Per B-X1 notes field exempt from POST-GAME scan.

**Q5 — Cross-region fragmentation policy.**

- `decision_id = "Q5_cross_region_policy"`.
- `decision_name = "Cross-region fragmentation operationalization (RISK-20)"`.
- `feature_family_id_or_scope = "sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling"`.
- Recommended `verdict = "deferred_blocker"`; `binding_level = "deferred_blocker"`.
- `cross_region_policy = "deferred_blocker"`.
- Rationale: CROSS-02-02 §6.2 row 5 enumerates three options (strict-exclusion / dual-feature-path / sensitivity-indicator-co-registration). The retention impact of each option is empirically conditional (a separate measurement study is required) and binding here without that measurement would pin a numeric without evidence (Invariant I7 violation). The PR #241 scaffold validator correctly accepts the `allowed_with_caveat` status without pinning; the adjudication preserves that deferral as an explicit BINDING gate against materialization.
- Evidence: CROSS-02-02 §6.2 row 5; `risk_register_sc2egset.md` RISK-20; PR #241 validator `_check_cross_region_caveat`.
- Falsifiers: `q5_cross_region_three_options_not_enumerated`.
- Notes: MATERIALIZATION BLOCKED until Q5 upgraded to `bind_now` in a successor adjudication PR with retention-measurement evidence.

**Q6 — Rating reconstruction model family (per N3 default `deferred_blocker`; N-X3 strengthened evidence gate).**

- `decision_id = "Q6_rating_policy"`.
- `decision_name = "Rating reconstruction model family for reconstructed_rating (G-CS-4)"`.
- `feature_family_id_or_scope = "sc2egset.history_enriched_pre_game.reconstructed_rating"`.
- Recommended `verdict = "deferred_blocker"`; `binding_level = "deferred_blocker"`.
- `rating_policy = "deferred_blocker"`.
- `evidence_paths` MUST be non-empty even when `deferred_blocker` is chosen (N-X3 strengthened gate); recommended `evidence_paths` value:
  ```
  src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  reports/specs/02_02_feature_engineering_plan.md (§6.2 row 4; §9 G-CS-4)
  src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md (is_mmr_missing density 83.95%)
  Elo (1978)
  Glickman (1999)
  Glickman (2012)
  Herbrich, Minka, Graepel (2006)
  ```
  (3 repo paths + 4 primary-source citations; satisfies N-X3 minimum "at least 1 repo + at least 1 citation" easily).
- Rationale (`notes`): **MUST contain the substring `"deferred_blocker because:"`** (N-X3 strengthened). Recommended notes verbatim:
  > "deferred_blocker because: per N3, ~83.95% MMR-missing density (verified in the dataset research log; consistent with the registry CSV `is_mmr_missing_flag` family) makes algorithm choice first-order. Pinning Elo / Glicko / Glicko-2 / TrueSkill / a rolling-winrate baseline without empirical evidence of which family handles the unrated / no-rating-history regime best would violate Invariant I7. Four candidate citations exist (Elo 1978; Glickman 1999; Glickman 2012; Herbrich, Minka, Graepel 2006) but binding one over the others requires repo evidence not yet generated. Forward-only constraint explicit: no target-match outcome; no future results; no global batch fit; per-game forward update only. Cold-start handled by initializing rating = literature-prior for new players (DEFERRED to materialization PR's training-fold-fit step); missingness handled by retaining `is_mmr_missing` as a separate companion feature (DEFERRED to materialization PR)."
  Notes contain (a) explicit "deferred_blocker because:" rationale, (b) the three forward-only phrases, (c) "cold-start handled by" + "missingness handled by" phrasing. Per B-X1 the `notes` field is EXEMPT from POST-GAME token scanning, so negated-prose terms ("no target-match outcome", "no future results", "no global batch fit") are ALLOWED here.
- Evidence: registry CSV row 10; ROADMAP lines 2334-2338 G-CS-4; CROSS-02-02 §6.2 row 4; `thesis/references.bib` citations.
- Falsifiers: `q6_rating_default_deferred_violated` (N3 + N-X3), `q6_rating_forward_only_missing`.
- Notes: MATERIALIZATION BLOCKED until Q6 upgraded to `bind_now` in a successor adjudication PR with rating-family empirical evaluation evidence satisfying the N-X3 strengthened gate (≥1 repo path + ≥1 citation + forward-only wording + cold-start/missingness wording).

**Q7 — IN_GAME_HISTORICAL prior-match aggregation (per N1 + N2; canonical strict-< per B-X2).**

- `decision_id = "Q7_in_game_historical_policy"`.
- `decision_name = "IN_GAME_HISTORICAL prior-match aggregation policy for in_game_history_aggregate"`.
- `feature_family_id_or_scope = "sc2egset.history_enriched_pre_game.in_game_history_aggregate"`.
- Recommended `verdict = "bind_now"`; `binding_level = "binding_for_materialization"`.
- `in_game_historical_policy = "prior_match_only_strict_lt"`.
- `in_game_historical_columns_in_scope = "APM|SQ|supplyCappedPercent|header_elapsedGameLoops"` (N1 deterministic).
- **Strict-`<` filter (CANONICAL per B-X2):** same as Q3 — `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at`.
- Rationale: CROSS-02-00 §5.4 Concern 8 / T15 record retains these 4 columns in scope for prior-match aggregation ONLY; never as direct game-T pre-game features. Forbid target-match tracker / target-match game-state consumption (those are `in_game_snapshot`, deferred to Step 02_01_04). The source is `player_history_all` (per ROADMAP line 2367 + CROSS-02-02 §6.2 row 6).
- Evidence: spec §5.4 sc2egset PH IN_GAME_HISTORICAL rows; CROSS-02-00 §5.4 Concern 8 / T15 record; registry CSV row 12.
- Falsifiers: `q7_in_game_historical_columns_drift` (N1), `q7_no_target_match_tracker_missing`, `in_game_historical_strict_lt_violated` (N2 — Q7-specific, not generic), `strict_lt_filter_divergence` (B-X2 — applies to Q7's bound expression).
- Notes: distinct from `in_game_snapshot` tranche; aggregation pseudocount / window-size constants DEFERRED to materialization PR. Per B-X1 notes exempt from POST-GAME scan.

**Q8 — `matches_history_minimal` consumption (PR #239 ROADMAP-nit promoted to adjudication row).**

- `decision_id = "Q8_matches_history_minimal_consumption"`.
- `decision_name = "What matches_history_minimal is consumed for in the history-enriched pre_game tranche"`.
- `feature_family_id_or_scope = "NOT_A_FEATURE_SOURCE_unless_explicitly_justified"`.
- Recommended `verdict = "ratify_with_evidence"`; `binding_level = "binding_for_materialization"`.
- Rationale: MHM is consumed for (1) target row identity / `started_at` TIMESTAMP anchor per PR #234 Q2(a) BINDING (the canonical source of `started_at` joined back onto MFC); (2) cold-start enumeration G-CS-2/3/4/5 (the support set of `(focal_player, target.started_at)` target rows over which prior history is counted). MHM is NOT a feature source — no MHM column becomes a feature column in the materialized output unless this adjudication row is updated in a successor PR with explicit justification.
- Evidence: PR #241 scaffold notebook cell "What matches_history_minimal is consumed for"; ROADMAP `inputs.duckdb_tables` line 2366; spec §5.1 sc2egset MHM column table.
- Falsifiers: `q8_mhm_documentation_missing`.
- Notes: MHM column-level provenance recorded for examiner clarity; no MHM PRE_GAME column elevated to feature without successor-PR adjudication. Per B-X1 notes exempt from POST-GAME scan.

**Verification:**
- `source .venv/bin/activate && poetry run ruff check src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` exit 0.
- `source .venv/bin/activate && poetry run mypy src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` exit 0.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` (updated)

**Read scope:**
- (no new file reads)

### T06 — Test file: synthetic fixtures + test classes covering every Q + every falsifier + B-X1/B-X2/N-X1/N-X2/N-X3/N-X4

**Objective:** Create the mirrored test file with synthetic CSV/Parquet
fixtures and ≥40 tests across ≥30 test classes (one class per Q-decision
plus one per falsifier plus dedicated classes for B-X1 scope, B-X2
canonical-form cross-site, N-X1 mapping completeness, N-X2 Q1 evidence,
N-X3 Q6 evidence-sufficiency branches, N-X4 Q1 subfield disambiguation).
Coverage ≥95% on the adjudicator module.

**Instructions:**
1. Create `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_enriched_pre_game_source_layer.py`.
2. Resolve `_TESTS_ROOT = Path(__file__).resolve().parents[6]` (mirror tranche-1 pattern).
3. Declare paths: real registry CSV; real PR #234 binding CSV; real DuckDB; expected SHA-256 constant; canonical strict-`<` expression constant.
4. Implement test classes (one per falsifier + Q + revision-finding class):
   - `TestExactEightDecisionsPresent` — happy path: all 8 Q-decisions returned.
   - `TestPr241Sha256Match` (N4) — fixture row with wrong / NOT_FOUND / 63-char SHA → halting `pr241_sha256_mismatch`.
   - `TestQ1SingleRowPerN5` (N5) — fixture splitting Q1 into Q1a/Q1b → halting `q1_single_row_violation`.
   - `TestQ1SourceLayerEvidenceConsistent` — fixture with Q1 selected source = `replay_players_raw` → halting `q1_source_layer_evidence_inconsistent`.
   - **`TestQ1SubfieldDisambiguation` (N-X4 NEW)** — assert Q1 row carries:
     - `selected_target_source_layer == "matches_flat_clean"`
     - `selected_history_source_layer == "player_history_all"`
     - `target_history_asymmetry == "asymmetric"`
     - `source_layer_divergence_reason` non-empty and contains `"matches_flat_clean (operationally) vs matches_flat (registry)"`
     - `history_source_extension_reason` non-empty and contains `"player_history_all"` and `"tranche-2"`
     Fixture omitting either N-X4 subfield → halting `q1_single_row_violation`.
   - `TestQ2TargetAnchorTypeMatch` — fixture asserting non-TIMESTAMP anchor → halting `q2_target_anchor_type_mismatch`.
   - `TestQ3HistoryTimeColumnInvalid` — fixture with missing PH `details_timeUTC` → halting `q3_history_time_column_invalid`.
   - `TestQ3StrictLtSmokeFailed` — fixture mocking probe to return `>0` self-rows OR TRY_CAST NULL on sample → halting `q3_strict_lt_smoke_failed`.
   - `TestQ4ColdStartGatesIncomplete` — fixture missing G-CS-3 in Q4 cold_start_policy → halting `q4_cold_start_gates_incomplete`.
   - `TestQ4ColdStartLeakage` — fixture Q4 notes omits `match_time < T` wording → halting `q4_cold_start_leakage`.
   - `TestQ5CrossRegionThreeOptions` — fixture Q5 enumerates only 2 options → halting `q5_cross_region_three_options_not_enumerated`.
   - **`TestQ6RatingEvidenceSufficiency` (N3 + N-X3 NEW; rename of `TestQ6RatingDefaultDeferred`)** — 4 fixture branches:
     - **deferred-pass:** `rating_policy="deferred_blocker"`, `evidence_paths` non-empty (3 repo paths + 4 citations), notes contain `"deferred_blocker because:"` → PASSES.
     - **deferred-fail-no-rationale:** `rating_policy="deferred_blocker"`, `evidence_paths` non-empty, but notes lack `"deferred_blocker because:"` → HALTING `q6_rating_default_deferred_violated`.
     - **bind-pass-with-full-evidence:** `rating_policy="glicko2"`, `evidence_paths` contains 2 repo paths + 1 citation, notes contain forward-only phrases AND `"cold-start handled by"` AND `"missingness handled by"` → PASSES.
     - **bind-fail-with-only-1-repo-path:** `rating_policy="glicko2"`, `evidence_paths` contains 1 repo path and 0 citations → HALTING `q6_rating_default_deferred_violated`.
   - `TestQ6RatingForwardOnlyMissing` — fixture Q6 notes omits any of the three forward-only phrases → halting `q6_rating_forward_only_missing`.
   - `TestQ7InGameHistoricalColumnsDrift` (N1) — fixture Q7 columns = `APM|SQ` → halting `q7_in_game_historical_columns_drift`. Companion: with full 4 columns → passes.
   - `TestQ7NoTargetMatchTrackerMissing` — fixture Q7 notes omits prior-match-only wording → halting `q7_no_target_match_tracker_missing`.
   - `TestQ7InGameHistoricalStrictLt` (N2) — fixture Q7 `cold_start_policy` / `in_game_historical_policy` omitting strict-`<` → halting `in_game_historical_strict_lt_violated`. Distinct from any generic `_check_strict_lt_policy`.
   - `TestQ8MhmDocumentationMissing` — fixture Q8 missing both purposes → halting `q8_mhm_documentation_missing`.
   - **`TestUniversalPostGameToken` (B-X1 RE-SCOPED)** — re-scope to `POST_GAME_TOKEN_SCOPED_FIELDS`; parametrized over the 10 tokens. For each (token, scoped_field) pair: injecting the token into `selected_source_layer` / `feature_family_id_or_scope` / `materialized_output_paths` (in turn) → halting `universal_post_game_token_in_scoped_field`. Assert explicit "exempt fields" list assertion: the test asserts `POST_GAME_TOKEN_EXEMPT_FIELDS == ("notes", "evidence_paths", "falsifiers", "decision_name", "rationale", "source_layer_divergence_reason", "history_source_extension_reason")`.
   - **`TestNegativeRationaleAllowedInNotes` (B-X1 NEW POSITIVE COMPANION)** — fixture: Q6 notes contains the exact wording `"no target-match outcome; no future results; no global batch fit"`; assert the adjudication PASSES (does NOT halt). Additionally fixtures inject `"forbid result"` and `"reject winner field"` into notes → PASSES. Independent fixture: inject `"deferred_blocker because: avoid winner-side leakage"` into Q6 notes → PASSES (negated rationale in exempt field).
   - **`TestForbiddenTokensExemptFieldsList` (B-X1 NEW)** — assert that every field name in `POST_GAME_TOKEN_EXEMPT_FIELDS` is a valid dataclass field (`assert name in {f.name for f in fields(HistoryEnrichedAdjudicationDecision)}`) AND no field name appears in both `POST_GAME_TOKEN_SCOPED_FIELDS` and `POST_GAME_TOKEN_EXEMPT_FIELDS` (disjoint sets).
   - `TestUniversalTrackerSourceInHistory` — fixture Q1 `selected_history_source_layer = tracker_events_raw.PlayerStats` → halting `universal_tracker_source_in_history`.
   - **`TestStrictLtFilterCanonicalAcrossSites` (B-X2 NEW)** — assert the `STRICT_LT_HISTORY_FILTER` constant, the T02 smoke probe SQL string, and the Q3 + Q7 bound `history_time_column` / strict-`<` expression strings ALL use the canonical TRY_CAST form (specifically: contain `"TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"` modulo whitespace). Parametrized over 4 divergence cases (each MUST halt `strict_lt_filter_divergence`):
     - constant changed to `"CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"` (bare CAST)
     - constant changed to `"ph.details_timeUTC < target.started_at"` (no cast)
     - constant changed to `"TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < mhm.started_at"` (wrong alias)
     - constant changed to `"try_cast(ph.details_timeUTC as timestamp) < target.started_at"` (lowercase)
   - **`TestRoadmapRawFormNotPropagated` (B-X2 NEW)** — assert `STRICT_LT_FILTER_ROADMAP_RAW` exists, has value `"ph.details_timeUTC < target.started_at"`, and is NOT used anywhere in the T02 smoke SQL or T05 Q3/Q7 bound expressions (greps the module source for the bare form and asserts it appears only inside the `STRICT_LT_FILTER_ROADMAP_RAW` constant declaration and inside the matching falsifier-message format string).
   - `TestMaterializationCreepRejected` — fixture any row with `materialized_output_paths != ""` → halting `materialization_creep`.
   - `TestNoFilesWrittenOnHaltingFalsifier` — assert no CSV/MD written when a falsifier fires (halt-before-artifact).
   - `TestDeterministicCsvSchema` — assert the **27-column** CSV header is byte-identical across two runs.
   - `TestCsvFieldsPopulated` — assert `in_game_historical_columns_in_scope` populated on Q7 (not empty); assert `pr241_scaffold_validator_module_sha256` populated and 64-char lowercase hex on every row; assert `source_layer_divergence_reason` + `history_source_extension_reason` populated on Q1 and empty on Q2-Q8.
   - `TestNoArtifactPathDrift` — assert CSV and MD paths exactly match `ADJUDICATION_CSV_REL` and `ADJUDICATION_MD_REL` constants.
   - `TestNoMaterializedOutputPath` — assert every row's `materialized_output_paths == ""`.
   - `TestNoStatusYamlChange` — assert no `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` write attempted (`monkeypatch.setattr` on `Path.write_text` to record writes; assert none target status paths).
   - `TestNoFeatureMaterialization` — assert no Parquet written under `reports/artifacts/02_01_03/`.
   - `TestStrictLtPolicyRepresented` — assert Q3 + Q7 both encode strict-`<` semantics using canonical TRY_CAST form.
   - **`TestDirectTargetMatchOutcomeRejected` (B-X1 RE-SCOPED)** — fixture injects forbidden tokens (`"target_match_outcome"`, `"winner"`, `"is_decisive"`) into `selected_source_layer` / `feature_family_id_or_scope` / `materialized_output_paths` (NOT into notes). Halting `universal_post_game_token_in_scoped_field`. Companion: same tokens in `notes` → PASSES.
   - `TestTrackerTargetMatchInGameRejected` — fixture Q7 `selected_source_layer` contains `tracker_events_raw` → halting on `universal_tracker_source_in_history`.
   - `TestCrossRegionDeferredOrSelectedPolicyRepresented` — assert Q5 verdict is one of the 4 allowed values (3 options + deferred_blocker).
   - `TestRatingPolicyRepresentedAndLeakageGuarded` — assert Q6 verdict is one of {elo, glicko, glicko2, trueskill, rolling_winrate_baseline, deferred_blocker} AND (per N-X3) notes forbid future / target / global-batch AND notes contain cold-start + missingness wording when verdict is a model family.
   - `TestMhmConsumptionDocumented` — assert Q8 notes cite both MHM purposes (anchor + cold-start enumeration).
   - **`TestHelperToFalsifierKeyMappingIsComplete` (N-X1 NEW)** — assert `HELPER_TO_FALSIFIER_KEY` contains exactly 20 entries; every key is a real callable in the adjudicator module; every value is a unique string; the mapping is exactly equal to the literal table in T03b (loaded from a frozen reference dict declared inside the test).
   - **`TestPriorityChainReferencesMapping` (N-X1 NEW)** — assert every falsifier name in the T04 falsifier priority chain (read by parsing the constant or list-of-names in the module) appears in `HELPER_TO_FALSIFIER_KEY.values()`.
   - `TestRealRegistryCsvSmoke` (`@pytest.mark.skipif(not REGISTRY_CSV_PATH.exists(), ...)`) — assert real-registry happy path: 8 decisions, 0 halting falsifiers, CSV+MD written to `tmp_path` (NOT the real artifact path).
   - `TestRealDuckDbReadOnlySmoke` (`@pytest.mark.skipif(not DUCKDB_PATH.exists(), ...)`) — assert read-only DuckDB probe succeeds (T02 step 3 view row counts match expected).
   - `TestByteDeterminismModuloProvenance` — assert two runs of the writer produce byte-identical CSV+MD except for `provenance_git_sha` and `audit_pr` fields (and any timestamp fields). Tests the determinism gate.
5. Synthetic-CSV / synthetic-DuckDB fixtures use `tmp_path`; real-DB tests use `skipif`.
6. Target ≥40 tests, ≥30 test classes. Coverage ≥95% on the adjudicator module per Invariant convention.

**Verification:**
- `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_enriched_pre_game_source_layer.py -v` ≥40 passed, 0 failed.
- `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_enriched_pre_game_source_layer.py --cov=rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer --cov-report=term-missing` ≥95% line coverage.

**File scope:**
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_enriched_pre_game_source_layer.py`

**Read scope:**
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py` (PR #241 test precedent)
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` (target module)

### T07 — Adjudication notebook pair (jupytext .py + .ipynb)

**Objective:** Create the jupytext-paired adjudication notebook under the
sandbox tree. No `def` / `class` / lambda in cells. All logic imported from
the adjudicator module. Each cell declares hypothesis + falsifier inline per
`feedback_notebook_iterative_testing.md`.

**Instructions:**
1. Create `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.py` with `formats: ipynb,py:percent` header (mirror PR #234 notebook pair).
2. Add cells:
   - Title cell: `# Step 02_01_03 — History-enriched source/anchor/cold-start ADJUDICATION: sc2egset`.
   - Lineage cell: artifact #3 of N for Step 02_01_03 readiness (PR #239 stub → PR #240 scaffold plan → PR #241 scaffold + validator → THIS adjudication → future materialization plan → materialization + post-mat audit → closure).
   - Non-materialization banner (verbatim from PR #234 §1 disclaimer + this plan's §Scope).
   - Imports cell: `from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import adjudicate_history_enriched_pre_game_source_layer, EXPECTED_PR241_VALIDATOR_SHA256, IN_GAME_HISTORICAL_AGGREGATED_COLUMNS, STRICT_LT_HISTORY_FILTER, POST_GAME_TOKEN_SCOPED_FIELDS, POST_GAME_TOKEN_EXEMPT_FIELDS, HELPER_TO_FALSIFIER_KEY`.
   - Per-Q markdown + execution cells (one per Q1-Q8): each cell starts with `# Hypothesis: <one sentence>` and `# Falsifier: <name>` per `feedback_notebook_iterative_testing.md`. Q1 cell explicitly documents the N-X4 subfield disambiguation (target/history asymmetry + divergence reason + extension reason). Q3 + Q7 cells explicitly show the canonical TRY_CAST form (B-X2).
   - Adjudication-call cell: invokes `adjudicate_history_enriched_pre_game_source_layer(...)` with real DuckDB + registry CSV + PR #234 binding CSV; asserts `result.passed is True`, `len(result.decisions) == 8`, `result.halting_falsifier is None`.
   - Closing cell: artifact #3 of N persisted; NO materialization; NO status flip; NO research_log entry; explicit list of deferred items (Q5 cross-region, Q6 rating, materialization SQL, post-mat audit, closure).
3. Generate paired `.ipynb` via `source .venv/bin/activate && poetry run jupytext --sync <path>.py`.
4. Clear all outputs in `.ipynb` before staging.

**Verification:**
- `source .venv/bin/activate && poetry run jupytext --check-metadata <path>.py` succeeds.
- `git diff --stat` shows both `.py` and `.ipynb` present.
- Manually inspect `.ipynb` cells: all outputs empty.

**File scope:**
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.py`
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.ipynb`

**Read scope:**
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.py` (PR #234 adjudication-notebook precedent).
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` (the module being driven).

### T08 — Execute the notebook → emit the adjudication CSV+MD; housekeeping (INDEX, CHANGELOG, pyproject)

**Objective:** Run the adjudication notebook against the real DuckDB +
registry CSV + PR #234 binding CSV; emit the **27-column** CSV + multi-section
MD at the declared paths; update `planning/INDEX.md`, `CHANGELOG.md`, and
`pyproject.toml`.

**Instructions:**
1. Activate venv: `source .venv/bin/activate`.
2. Execute the notebook to write
   `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv`
   and `.md`. Halt if any falsifier fires (the notebook's assertion cell
   will raise).
3. Update `planning/INDEX.md`: archive whichever Active row precedes this
   PR (currently PR #241); promote
   `feat/sc2egset-02-01-03-history-source-anchor-coldstart-adjudication` to
   Active.
4. Update `CHANGELOG.md`: move `[Unreleased]` into a new
   `[3.73.0] — <date> (PR #<number>: feat/sc2egset-02-01-03-history-source-anchor-coldstart-adjudication)`
   section with Added entries for adjudicator module, mirrored tests,
   adjudication CSV+MD pair, notebook pair; Changed entries for INDEX +
   pyproject.
5. Bump `pyproject.toml` `version = "3.72.0"` → `"3.73.0"` (minor; feat-family
   per `.claude/rules/git-workflow.md`).
6. Spot-check: `ls reports/artifacts/02_01_03/ 2>/dev/null` returns nothing
   (no leakage audit dir created); `ls reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/` shows the new adjudication CSV + MD only.

**Verification:**
- `source .venv/bin/activate && poetry version` reports `3.73.0`.
- Adjudication CSV exists at the declared path; has 8 data rows + 1 header row (`wc -l` returns `9`); 27 columns; SHA-256 stable across runs (modulo provenance fields).
- Adjudication MD exists at the declared path with §1–§14 sections.
- `git diff --stat` shows exactly the 9 deliverable execution files (the 2 inherited planning files are unchanged on the branch).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md`
- `planning/INDEX.md`
- `CHANGELOG.md`
- `pyproject.toml`

**Read scope:**
- (no new file reads beyond T07)

### T09 — Pre-commit + final-gate routing for the Layer-2 PR

**Objective:** Confirm ruff, mypy, pytest, coverage pass; dispatch reviewer
agents per `.claude/rules/data-analysis-lineage.md`.

**Instructions:**
1. Run `source .venv/bin/activate && poetry run ruff check src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_enriched_pre_game_source_layer.py`.
2. Run `source .venv/bin/activate && poetry run mypy src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py`.
3. Run `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_enriched_pre_game_source_layer.py -v --cov=rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer --cov-report=term-missing` ≥95% coverage.
4. Run `source .venv/bin/activate && poetry run pre-commit run --files <staged-files>`.
5. Layer-2 commit message: `feat(sc2egset): Step 02_01_03 source/anchor/cold-start adjudication`.
6. On Layer-2 PR open, dispatch `@reviewer-deep` for structural correctness, spec compliance, invariant tracing.
7. Because this Layer-2 PR is **methodology-sensitive** (rating-algorithm deferral, cross-region policy deferral, IN_GAME_HISTORICAL aggregation discipline, B-X1 forbidden-token scope, B-X2 canonical strict-`<` form), ALSO dispatch `@reviewer-adversarial` for the methodology defensibility gate per `.claude/rules/data-analysis-lineage.md` ("before Phase 03+ methodology-sensitive work" — applies to Phase-02 adjudication that locks downstream materialization policy).
8. Final gate verdict from BOTH reviewers must be APPROVE (with or without nits) before merge.
9. User explicitly approves merge in chat.

**Verification:**
- ruff + mypy + pytest exit 0.
- Coverage ≥95%.
- Reviewer-deep report exists on the PR with APPROVE verdict.
- Reviewer-adversarial report exists on the PR with APPROVE (or APPROVE-WITH-NITS) verdict.
- User has explicitly approved the merge in chat.

**File scope:** (none — runs commands and routes reviewers)

## File Manifest

### This Layer-1 planning PR (exactly 2 files)
- `planning/current_plan.md` (created — this document)
- `planning/current_plan.critique.md` (created by reviewer-adversarial in a separate dispatch)

### Future Layer-2 adjudication execution PR = 11 final tracked files

**9 deliverable/execution files:**
1. `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.py` (created by T07)
2. `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.ipynb` (created by T07)
3. `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py` (created by T01-T05)
4. `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_enriched_pre_game_source_layer.py` (created by T06)
5. `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv` (created by T08; 27 columns; 8 rows + 1 header)
6. `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md` (created by T08; §1-§14)
7. `planning/INDEX.md` (updated by T08)
8. `CHANGELOG.md` (updated by T08)
9. `pyproject.toml` (updated by T08)

**+ 2 inherited planning files already in the branch (byte-unchanged on Layer-2):**
10. `planning/current_plan.md` (inherited from this Layer-1 PR)
11. `planning/current_plan.critique.md` (inherited from this Layer-1 PR)

The notebook pair `.py` + `.ipynb` (deliverables #1 and #2) counts as **two
distinct deliverables** per the PR #234 precedent. The total is exactly
**11 = 9 + 2**.

### Files explicitly NOT touched at either layer
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` (no `02_01_03: complete` added; closure deferred per U6).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` (frozen).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` (frozen; Phase 02 = in_progress, Phase 03 = not_started).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (frozen; 02_01_03 block at lines 2274-2523 unchanged).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` (frozen).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (frozen; closure PR will append).
- `reports/research_log.md` (frozen; no CROSS entry needed).
- Any file under `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/` (no leakage audit; no Parquet).
- Any Parquet under `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/` (only the existing `02_01_02_pre_game_features.parquet` remains; no `02_01_03_*.parquet`).
- Any file under `reports/specs/` (no spec patch).
- Any cleaning-layer YAML.
- Any file under `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/`.
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py` (PR #241 byte-unchanged; SHA re-asserted).
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py` (PR #241 byte-unchanged).
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.{py,ipynb}` (PR #241 byte-unchanged).
- Any file under `src/rts_predict/games/aoe2/`.
- Any file under `thesis/`.
- Any file under `docs/` or `.claude/`.
- Any file under `data/` (raw / staging / db).

## Gate Condition

The future Layer-2 adjudication execution PR passes its final gate iff ALL
of the following hold:

1. **Exact file scope.** `git diff --name-only master..HEAD` shows exactly
   the **11 tracked files** (9 deliverable + 2 inherited planning). No
   extras. Notebook pair `.py` + `.ipynb` counts as two distinct files.

2. **Adjudicator runs on real DuckDB + registry + PR #234 binding.**
   ```
   source .venv/bin/activate && poetry run python -c "from pathlib import Path; from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import adjudicate_history_enriched_pre_game_source_layer; r = adjudicate_history_enriched_pre_game_source_layer(duckdb_path=Path('src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb'), registry_csv_path=Path('src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv'), pr234_binding_csv_path=Path('src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv'), csv_path=Path('src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv'), md_path=Path('src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md'), audit_pr='PR #<number>', audit_date='2026-05-24'); assert r.passed and len(r.decisions) == 8 and r.halting_falsifier is None"
   ```
   returns exit 0.

3. **Adjudication CSV present.** `wc -l <csv>` returns `9` (1 header + 8 rows). Every row carries the **27 columns** (26 dataclass fields + `notes`); `in_game_historical_columns_in_scope` is populated on Q7 exactly as `APM|SQ|supplyCappedPercent|header_elapsedGameLoops`; `pr241_scaffold_validator_module_sha256` is `b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904` on every row; `source_layer_divergence_reason` (N-X4) populated on Q1 and empty on Q2-Q8; `history_source_extension_reason` (N-X4) populated on Q1 and empty on Q2-Q8; no row has `NOT_FOUND` in any SHA field; no row has a non-empty `materialized_output_paths`; **the strict-`<` expression text in `history_time_column` on Q3 contains the canonical `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at` (B-X2); no scoped field on any row contains any POST-GAME token (B-X1)**.

4. **Adjudication MD present.** §1–§14 all present including: §1 non-overclaim disclaimer; §2-§9 Q1-Q8 decisions with verbatim SQL (Invariant I6) — all strict-`<` SQL uses canonical TRY_CAST form (B-X2); §10 falsifier roll-call iterating `HELPER_TO_FALSIFIER_KEY.values()`; §11 lineage; §12 explicit non-substitution; §13 materialization-blocked-until-deferred-resolved; §14 no-Step-closure-claim.

5. **Tests pass with coverage.** `pytest -v` ≥40 passed, 0 failed; coverage ≥95% on adjudicator module. `TestStrictLtFilterCanonicalAcrossSites` (B-X2), `TestRoadmapRawFormNotPropagated` (B-X2), `TestUniversalPostGameToken` re-scoped (B-X1), `TestNegativeRationaleAllowedInNotes` (B-X1), `TestForbiddenTokensExemptFieldsList` (B-X1), `TestHelperToFalsifierKeyMappingIsComplete` (N-X1), `TestPriorityChainReferencesMapping` (N-X1), `TestQ1SubfieldDisambiguation` (N-X4), `TestQ6RatingEvidenceSufficiency` (N3 + N-X3) all PASS.

6. **Lint and type checks clean.** `ruff check` and `mypy` exit 0.

7. **No notebook outputs committed.** Every cell output in the `.ipynb` is empty.

8. **No status YAML / research_log / spec / cleaning-layer / ROADMAP change.** `git diff master..HEAD -- src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md reports/research_log.md reports/specs/ src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/` reports nothing.

9. **No materialization or audit dir.** `ls src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/ 2>/dev/null` returns "No such file or directory"; no Parquet under `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_*.parquet`.

10. **PR #241 byte-unchanged.** `git diff master..HEAD -- src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_history_enriched_pre_game_materialization.py sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.ipynb` reports nothing.

11. **Reviewer-deep APPROVE.** Report on PR with verdict APPROVE (with or without nits).

12. **Reviewer-adversarial APPROVE (methodology-sensitive Phase-02 adjudication; mandatory per T09 step 7).** Report on PR with verdict APPROVE (with or without nits).

13. **No merge without user approval.** User explicitly approves merge in chat after reading both reviewer reports.

If any of conditions 1-13 fail, the PR is BLOCKED. Fix-forward is the rule
(per `.claude/rules/data-analysis-lineage.md` — do not amend; create a NEW
commit).

## Out of scope

- Materialization SQL execution (DuckDB queries that project the 6 history
  families into a Parquet table). DEFERRED to a future Layer-3
  materialization-execution plan + materialization-execution PR pair.
- Parquet feature artifact (`02_01_03_history_enriched_pre_game_features.parquet`). DEFERRED.
- Non-vacuous CROSS-02-01-v1.0.1 leakage audit JSON/MD over the 6 history
  families' materialized columns. DEFERRED.
- Re-executed CROSS-02-03-v1.0.1 §10 verdict audit over rows 7-12. DEFERRED
  per ROADMAP `continue_predicate`.
- Cross-region fragmentation policy numeric choice (Q5). EXPLICITLY DEFERRED
  to a successor adjudication PR with retention-measurement evidence.
- Rating reconstruction algorithm choice (Q6). EXPLICITLY DEFERRED to a
  successor adjudication PR with rating-family empirical evaluation
  evidence satisfying N-X3 strengthened gate (≥1 repo + ≥1 citation +
  forward-only + cold-start + missingness wording).
- Empirical derivation of cold-start constants (K, m, α). DEFERRED to the
  materialization PR (must be fit on training folds only per G-CS-6 /
  Invariant I3 normalization discipline).
- Phase 03 splitting + baselines (Phase 02 has 7 remaining Pipeline
  Sections out of 8; Phase 03 gate not met).
- Step 02_01_04 (in_game_snapshot tranche).
- Closure of Step 02_01_03 in `STEP_STATUS.yaml`. DEFERRED to a separate
  closure PR per the PR #237 tranche-1 closure precedent.
- Append to dataset `research_log.md`. DEFERRED to the closure PR.
- AoE2 work.
- Any cleaning-layer YAML patch.
- Any spec patch (CROSS-02-00, CROSS-02-01, CROSS-02-02, CROSS-02-03).
- Any thesis chapter prose.
- Any `.claude/` or `docs/` edit.
- Any data file edit (raw / staging / db).
- Re-edit of PR #241 scaffold notebook or validator module (byte-unchanged
  anchors; SHA-256 re-asserted as N4 binding).
- ROADMAP body edit (frozen at PR #239's merged block lines 2274-2523).
- Ready-for-review on the Layer-2 PR draft; the user explicitly approves the
  merge in chat after reading reviewer reports.

## Open Questions

These questions are for the reviewer-adversarial round-3 pass on this
Layer-1 planning PR. They are NOT blockers for the Layer-2 execution PR;
the adjudicator's 20-falsifier priority chain (per N-X1 mapping table) is
non-vacuous regardless of the answers.

1. **Q5 retention measurement now vs deferred.** Recommendation here is
   `deferred_blocker` because retention measurement (how many `(focal, opp)`
   pairs are dropped under each of the 3 options) is itself an empirical
   measurement study not yet executed. Alternative: include a Q5 retention
   measurement probe in T02 (e.g., compute the row-count delta for each of
   the 3 options) and use the result to bind. Recommendation: keep deferred
   — pre-empting the measurement here violates the non-batching rule
   (sequence step 3 is adjudication, not Step 02_01_06-style empirical
   measurement).

2. **Q6 rating-family empirical evaluation now vs deferred.** Recommendation
   here is `deferred_blocker` per N3 + N-X3. Alternative: run a small
   offline rating-family comparison study at this adjudication layer (Elo
   vs Glicko-2 vs rolling-winrate baseline on a tiny holdout).
   Recommendation: keep deferred — comparison study is Phase-03 work and
   would violate non-batching.

3. **Should Q5 and Q6 share a single `deferred_blocker_with_retention_evidence`
   verdict / `deferred_blocker_with_rating_evidence` verdict, or stay with
   the simple `deferred_blocker`?** Recommendation: simple `deferred_blocker`
   for both; rationale text in `notes` distinguishes them; binding evidence
   is recorded at the successor-PR binding time, not embedded in the
   current verdict label.

4. **N-X3 evidence-count thresholds (1 repo + 1 citation).** The strengthened
   gate requires at least 1 repo path AND at least 1 primary-source
   citation when verdict is a model family. Should the threshold be ≥3 repo
   + ≥1 citation? Recommendation: keep the minimum at 1+1 — the successor
   PR's own reviewer-adversarial pass will gate evidence depth; pre-pinning
   a higher count without precedent violates Invariant I7 (no magic
   numbers). The pattern-match regexes for "repo path" and "citation" are
   themselves caveat-free conservative defaults.

5. **Q8 `feature_family_id_or_scope` text.** This plan uses
   `"NOT_A_FEATURE_SOURCE_unless_explicitly_justified"`. Alternative: leave
   as `""` with the notes field bearing the qualification. Recommendation:
   keep explicit `NOT_A_FEATURE_SOURCE_*` token in scope field — examiner-
   clarity benefit; matches the PR #234 §6 row binding-style. Note B-X1
   scope is field-aware; the `feature_family_id_or_scope` field is SCOPED
   (not exempt), so the falsifier scans it — but `NOT_A_FEATURE_SOURCE`
   itself is not a POST-GAME token, so no false positive.

6. **B-X1 reserve-fields rule.** `POST_GAME_TOKEN_SCOPED_FIELDS` includes
   the two reserve names `proposed_feature_columns` and `designed_column_names`
   even though they aren't in the current 26-field dataclass. Alternative:
   add them only when a successor PR introduces them. Recommendation: keep
   reserved (cost-free defensive declaration; ensures any successor PR
   adding either field falls under POST-GAME scanning automatically without
   silent regression). T06 `TestForbiddenTokensExemptFieldsList` documents
   the reserve-name design and ensures no overlap with the exempt set.

7. **B-X2 whitespace-normalization rule for `strict_lt_filter_divergence`.**
   The falsifier normalizes runs of whitespace to a single space before
   comparison. Alternative: byte-exact comparison. Recommendation: keep
   whitespace-normalized — SQL string formatting (e.g., line breaks in
   multi-line strings, indentation) should not trigger false positives;
   the canonical form's semantic content is what matters. The four
   parametrized divergence cases in `TestStrictLtFilterCanonicalAcrossSites`
   all fail BECAUSE of semantic divergence (wrong CAST kind, missing CAST,
   wrong alias, capitalization), not whitespace.

8. **Reviewer-adversarial mandatory or conditional for the Layer-2 PR.** T09
   step 7 makes it MANDATORY because the PR locks downstream materialization
   policy. Alternative: keep conditional per the PR #241 scaffold pattern.
   Recommendation: mandatory — adjudication binds rating + cross-region
   policy choices that materialization will rely on; adversarial methodology
   review is needed pre-materialization.

9. **Real-DB read-only probe scope.** T02 probes 4 row counts + 1 strict-`<`
   smoke (canonical TRY_CAST form per B-X2) + DESCRIBE on 2 anchor candidates
   + MHM column list + 1000-row TRY_CAST NULL-rate sample. Alternative:
   expand to include `_probe_cross_region_retention_pilot` for Q5
   evidence-gathering. Recommendation: keep minimal — expanding scope risks
   premature Q5 binding (see OQ1).

10. **N-X2 Option A vs Option B chosen as A.** The planner's defensible
    call: Option A (asymmetric, `binding_for_materialization`) is
    selected because CROSS-02-02 §6.2 rows 1, 4, 6 ALL source verbatim from
    `player_history_all`; CROSS-02-00 §2.1 row-grain note ("all game types;
    no 1v1 filter") is verbatim; `player_history_all.yaml`
    `provenance.scope` explicitly retains non-1v1 + indecisive replays;
    the WP-3 cross-region retention argument cited in `player_history_all.yaml`
    is supporting evidence. Alternative B (symmetric 1v1-only) would
    contradict three independent verbatim spec passages and reduce the
    cold-start support set under exactly the conditions G-CS-2/3 are
    designed to mitigate. Reviewer-adversarial may rebut by quoting an
    overriding verbatim spec passage; absent such, Option A binds.

## Self-check against B-X1, B-X2, N-X1, N-X2, N-X3, N-X4 + preserved B1 + N1-N5

**B-X1 — POST_GAME-token falsifier must not self-trip on required negative Q6 rationale.**
APPLIED. T01 step 2 declares `POST_GAME_TOKEN_SCOPED_FIELDS` (9 fields:
`selected_source_layer`, `selected_target_source_layer`,
`selected_history_source_layer`, `target_anchor`, `history_time_column`,
`feature_family_id_or_scope`, `materialized_output_paths`, plus reserved
`proposed_feature_columns`, `designed_column_names`) and
`POST_GAME_TOKEN_EXEMPT_FIELDS` (7 fields: `notes`, `evidence_paths`,
`falsifiers`, `decision_name`, `rationale`, `source_layer_divergence_reason`,
`history_source_extension_reason`). T03 step 8 RENAMES
`_check_universal_no_post_game_token` to
`_check_forbidden_post_game_feature_tokens`, scoped to only the scoped
fields, with rationale fields EXPLICITLY exempted. T04 priority chain
entry 18 uses the new name + key `universal_post_game_token_in_scoped_field`.
T06 `TestUniversalPostGameToken` re-scoped (parametrized over 10 tokens ×
3 scoped fields = halting in each); `TestNegativeRationaleAllowedInNotes`
NEW positive companion (negated wording in `notes` passes; "deferred_blocker
because: avoid winner-side leakage" passes; "forbid result" + "reject
winner field" pass); `TestForbiddenTokensExemptFieldsList` NEW asserts
exempt fields are valid dataclass field names and scoped+exempt sets are
disjoint; `TestDirectTargetMatchOutcomeRejected` re-scoped (forbidden
tokens in scoped fields halt; same tokens in notes pass). T05 Q1-Q8 notes
sections explicitly state "Per B-X1 notes exempt from POST-GAME scan"
where negated prose is used. Q6 notes verbatim contains "no target-match
outcome; no future results; no global batch fit; per-game forward update
only" without tripping the falsifier.

**B-X2 — one canonical strict-`<` expression everywhere.**
APPLIED. T01 step 2 `STRICT_LT_HISTORY_FILTER = "TRY_CAST(ph.details_timeUTC
AS TIMESTAMP) < target.started_at"` (TRY_CAST, not bare CAST; `target`
alias, not `mhm`; matches `matches_history_minimal.yaml` guidance). T01
step 2 also declares `STRICT_LT_FILTER_ROADMAP_RAW =
"ph.details_timeUTC < target.started_at"` for ROADMAP provenance ONLY
(non-executable). T02 step 5 smoke probe SQL rewritten:
```sql
SELECT COUNT(*) FROM player_history_all ph
JOIN matches_history_minimal target ON ph.toon_id = target.player_id
WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
  AND ph.replay_id = REPLACE(target.match_id, 'sc2egset::', '')
```
uses canonical form + `target` alias. T05 Q3 `history_time_column =
"player_history_all.details_timeUTC (TRY_CAST AS TIMESTAMP for comparison
with target.started_at)"`; strict-`<` expression = canonical constant. T05
Q7 strict-`<` filter = canonical form. T03 step 12 adds NEW falsifier
`_check_strict_lt_filter_divergence` (mapped to key `strict_lt_filter_divergence`
per T03b N-X1 mapping); rejects bare CAST, no cast, wrong alias,
capitalization variants. T04 priority chain inserts
`strict_lt_filter_divergence` after `q1_source_layer_evidence_inconsistent`
and BEFORE Q2/Q3 type checks (structural-before-content). T06
`TestStrictLtFilterCanonicalAcrossSites` (B-X2) parametrized over 4
divergence cases asserts halt; `TestRoadmapRawFormNotPropagated` (B-X2)
asserts ROADMAP raw form appears only in the named constant + falsifier
message. Where the plan quotes the ROADMAP raw text, it is explicitly
labeled as "ROADMAP §02_01_03 raw form (normalized by this adjudication
plan to the canonical TRY_CAST form for chronological fidelity per
`matches_history_minimal.yaml`)" (A11 assumption + T01 step 2
`STRICT_LT_FILTER_ROADMAP_RAW` doc + T05 Q3 binding section).

**N-X1 — helper/falsifier-key mapping table.**
APPLIED. T03b declares the full `HELPER_TO_FALSIFIER_KEY` literal mapping
table with all 20 entries (mirrors the table in the round-3 dispatch
prompt). T04 falsifier priority chain (item 4 and downstream) references
the mapping; T04 step 2 §10 falsifier roll-call iterates
`HELPER_TO_FALSIFIER_KEY.values()`; T06 `TestHelperToFalsifierKeyMappingIsComplete`
asserts the table has exactly 20 entries, all keys are real callables in
the module, all values are unique; `TestPriorityChainReferencesMapping`
asserts every priority-chain entry appears in `HELPER_TO_FALSIFIER_KEY.values()`.

**N-X2 — Q1 `target_history_asymmetry` over-binding without evidence.**
APPLIED. **Option A chosen (RECOMMENDED, BINDING)** with `binding_level =
"binding_for_materialization"`. T05 Q1 binding section quotes 5 verbatim
spec/schema passages:
- CROSS-02-02 §6.2 row 1 (`focal_player_history` sources from `player_history_all`)
- CROSS-02-02 §6.2 row 4 (`reconstructed_rating` derived from `player_history_all.result`)
- CROSS-02-02 §6.2 row 6 (`in_game_history_aggregate` from `player_history_all.APM/SQ/supplyCappedPercent/header_elapsedGameLoops`)
- CROSS-02-00 §2.1 sc2egset row 2 (Row grain = "1 row per player per match (all game types; no 1v1 filter)")
- `player_history_all.yaml` `provenance.scope` ("All replays (no 1v1/decisive filter). Includes non-1v1 and indecisive replays excluded from matches_flat_clean.")
Alternative A (RECOMMENDED) and Alternative B (REJECTED) both
explicitly enumerated with evidence-cited rationale. Rejection of
Alternative B explicitly cites cold-start support-set sparsity argument
under 83.95% MMR-missing density regime. Option B fallback (demoting to
`recommendation_only` / `deferred_blocker`) NOT triggered — verbatim spec
evidence is sufficient.

**N-X3 — N3 rating-evidence falsifier strength.**
APPLIED. T03 step 4 strengthens `_check_q6_rating_default_deferred`:
- `deferred_blocker` branch: PASSES iff `evidence_paths != ""` AND notes
  contain `"deferred_blocker because:"`.
- model-family branch: HALTS unless (a) `evidence_paths` contains ≥1 repo
  path AND ≥1 primary-source citation (newline-split count), (b) notes
  contain all three forward-only phrases, (c) notes contain `"cold-start
  handled by"` AND `"missingness handled by"`.
T05 Q6 binding includes recommended `evidence_paths` (3 repo paths + 4
primary-source citations) and verbatim recommended `notes` containing
"deferred_blocker because:", the three forward-only phrases, and the
"cold-start handled by" + "missingness handled by" wording. T06
`TestQ6RatingEvidenceSufficiency` (rename of `TestQ6RatingDefaultDeferred`)
exercises all 4 fixture branches: deferred-pass, deferred-fail-no-rationale,
bind-pass-with-full-evidence, bind-fail-with-only-1-repo-path. The plan's
overall recommendation: Q6 default = `deferred_blocker`.

**N-X4 — Q1 EXTEND disambiguation.**
APPLIED. T01 step 3 adds 2 NEW subfields to the dataclass
(`source_layer_divergence_reason: str`, `history_source_extension_reason:
str`); both Q1-only ("" otherwise). T05 Q1 binding populates both
verbatim:
- `source_layer_divergence_reason = "matches_flat_clean (operationally) vs matches_flat (registry); cleaned-view chosen for 1v1-scoping + 44,418-row deterministic count per PR #234 §3 binding (selected_source_layer = matches_flat_clean was BINDING in tranche-1)"`
- `history_source_extension_reason = "tranche-1 (5 pre_game families) had no history-side source; tranche-2 (6 history-enriched families) adds player_history_all as the history-side source per ROADMAP line 2367 inputs.duckdb_tables and CROSS-02-02 §6.2 rows 1-4 + 6 verbatim source bindings"`.
Q1 `verdict = "extend_with_evidence"` explicitly refers to the
history-side extension; source-layer divergence is documented separately
in its own subfield (RATIFY-with-divergence-noted). Dataclass field count
grows from 24 → 26; total CSV columns = 27 (with `notes`). §Gate
Condition condition 3 updated: 27 columns; `source_layer_divergence_reason`
populated on Q1 + empty on Q2-Q8; `history_source_extension_reason`
populated on Q1 + empty on Q2-Q8. T06 `TestQ1SubfieldDisambiguation` (N-X4
NEW) asserts both new subfields populated on Q1 with the recommended
content; fixture omitting either → halting `q1_single_row_violation`.
T08 instructions reflect 27-column CSV; `wc -l` still `9`.

**B1 — 11-file = 9 deliverable + 2 inherited planning contract (PRESERVED).**
PRESERVED. Frontmatter `future_execution_pr_scope` literal block unchanged
(11 entries). §Scope: "11-file final tracked diff — 9 deliverable
files… plus the 2 inherited planning files." §File Manifest: explicit
"9 deliverable/execution files" enumeration (#1-#9) + "2 inherited planning
files" (#10-#11) + closing sentence "Total is exactly 11 = 9 + 2." §Gate
Condition condition 1: "exactly the 11 tracked files (9 deliverable + 2
inherited planning). Notebook pair `.py` + `.ipynb` counts as two distinct
files." No occurrence anywhere in the plan of "10 files", "8 deliverable",
or "notebook pair counts as one file".

**N1 — CSV field `in_game_historical_columns_in_scope` (PRESERVED).**
PRESERVED. T01 step 3 declares the field in the 26+1-column schema (same
schema as round 2, plus 2 N-X4 subfields). T03 step 6 declares the
`_check_q7_in_game_historical_columns_in_scope` falsifier (key
`q7_in_game_historical_columns_drift` per N-X1 mapping). T05 Q7 binds the
exact pipe-separated value `APM|SQ|supplyCappedPercent|header_elapsedGameLoops`.
T06 declares `TestQ7InGameHistoricalColumnsDrift` test class. §Gate
Condition condition 3 asserts the populated value on Q7 verbatim.

**N2 — Q7-specific `_check_in_game_historical_strict_lt` falsifier (PRESERVED).**
PRESERVED. T02 step 7 lists the helper signature with explicit "Distinct
from any generic `_check_strict_lt_policy`" language. T04 falsifier
priority chain item 16 names `in_game_historical_strict_lt_violated`
(per N-X1 mapping) with the parenthetical "Q7-specific strict-`<`
falsifier (NOT generic `_check_strict_lt_policy`)". T06 test class
`TestQ7InGameHistoricalStrictLt` (N2) explicitly notes the distinction.

**N3 — Q6 rating recommendation `deferred_blocker` default (PRESERVED + STRENGTHENED per N-X3).**
PRESERVED + STRENGTHENED. T03 step 4 declares the strengthened
`_check_q6_rating_default_deferred` (N3 + N-X3) falsifier with both
branches. T05 Q6 binds `rating_policy = "deferred_blocker"` with
83.95%-MMR-missing-density rationale + the N-X3-required wording; no
premature pin of Elo / Glicko / Glicko-2 / TrueSkill / rolling baseline.
§Assumptions A10 states explicit RATIFY/EXTEND/NARROW/DEFER discipline.
§Unknowns U3 reproduces the N3 + N-X3 rationale verbatim. §Literature
Context states the four citations exist but are NOT bound at this layer.
T06 `TestQ6RatingEvidenceSufficiency` (N3 + N-X3) tests all 4 branches.

**N4 — `pr241_scaffold_validator_module_sha256` field (PRESERVED).**
PRESERVED. T01 step 3 declares the field in the 26+1-column schema with "(N4;
64-char lowercase hex)" annotation. T01 step 2 declares
`EXPECTED_PR241_VALIDATOR_SHA256 = "b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904"`
(the actual 64-char hex computed via `shasum -a 256` on the PR #241
validator). T03 step 10 declares the `_check_pr241_sha256_match` (N4)
falsifier rejecting `NOT_FOUND` / empty / wrong-length / wrong-case /
mismatched values. §Gate Condition condition 3 asserts populated on every
row, exact value match, no `NOT_FOUND`. T06 `TestPr241Sha256Match` (N4)
test class.

**N5 — Q1 single row with subfields (not split into Q1a/Q1b) (PRESERVED + EXTENDED per N-X4).**
PRESERVED + EXTENDED. T01 step 3 declares the three original N5 subfields
(`selected_target_source_layer`, `selected_history_source_layer`,
`target_history_asymmetry`) PLUS the two N-X4 subfields
(`source_layer_divergence_reason`, `history_source_extension_reason`) — all
on a single Q1 row. T03 step 11 declares the `_check_q1_single_row_per_n5`
(N5) falsifier explicitly rejecting any split into Q1a/Q1b/Q1c AND requiring
the N-X4 subfields populated. T05 Q1 binds all five subfields in one row
with explicit "(one row per N5; N-X4 subfields populated)" header. T06
`TestQ1SingleRowPerN5` (N5) + `TestQ1SubfieldDisambiguation` (N-X4) test
classes.

**Frontmatter, all 8 required `##` sections, and the bonus `## Out of scope`
+ `## Self-check` sections (PRESERVED).**
PRESERVED. Frontmatter has `category: A`, branch, base_ref, dataset,
predecessors, etc. (with `gate_reviewer` updated to round-3 framing). All
8 required `##` sections present in order: `## Scope`, `## Problem Statement`,
`## Assumptions & Unknowns`, `## Literature Context`, `## Execution Steps`,
`## File Manifest`, `## Gate Condition`, `## Open Questions`. Bonus
`## Out of scope` + `## Self-check` sections present.

---

**For Category A, adversarial critique is required before execution.
Dispatch reviewer-adversarial round 3 to produce
`planning/current_plan.critique.md`. The Layer-1 PR opens only after
reviewer-adversarial round 3 returns zero blockers (per the user
instruction in this prompt: "The parent will materialize it to disk only
if reviewer-adversarial round 3 returns zero blockers"). This is the LAST
round in the 3-round adversarial cap.**
