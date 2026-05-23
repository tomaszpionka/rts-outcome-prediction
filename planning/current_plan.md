---
category: A
branch: feat/sc2egset-02-01-02-source-anchor-race-adjudication
base_ref: a4cc290f29c16378022915b51d2ae0fa52d602e8
date: 2026-05-23
planner_model: claude-opus-4-7[1m]
dataset: sc2egset
phase: "02"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
step: "02_01_02 (adjudication preparation; precedes the eventual scaffold-execution-plus-materialization PRs)"
non_batching_sequence_position: "adjudication sub-step inserted between sequence step 2 (PR #233, scaffold + 1 validator on master) and sequence step 3 (validator execution + materialization-execution plan). Does NOT advance the 9-step sequence on its own; it precludes a coupled-decision batching defect in step 3."
critique_required_before_execution: true
critique_reviewer: reviewer-adversarial
gate_reviewer: "reviewer-adversarial (Category A pre-execution gate)"
chat_second_pass_required_before_materialization: true
planning_pr: "PR #<TBD — filled in literally by the parent after gh pr create>"
source_artifacts:
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json
  - sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.py
  - src/rts_predict/games/sc2/datasets/sc2egset/validate_pre_game_feature_materialization.py
  - tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_pre_game_feature_materialization.py
  - src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml
  - reports/specs/02_00_feature_input_contract.md  (CROSS-02-00-v3.0.1)
  - reports/specs/02_01_leakage_audit_protocol.md  (CROSS-02-01-v1.0.1)
  - reports/specs/02_02_feature_engineering_plan.md  (CROSS-02-02-v1.0.1)
  - reports/specs/02_03_temporal_feature_audit_protocol.md  (CROSS-02-03-v1.0.1)
  - thesis/pass2_evidence/methodology_risk_register.md  (RISK-20 line 375; RISK-24 line 445; RISK-26 line 479)
  - .claude/scientific-invariants.md
  - .claude/ml-protocol.md
  - .claude/rules/data-analysis-lineage.md
  - .claude/rules/sql-data.md
  - .claude/rules/python-code.md
---

# Plan — SC2EGSet Step 02_01_02 source/anchor/race-column adjudication (Category A)

## Scope

Category A — Phase work, planning-only adjudication unit. Phase 02 → Pipeline Section 02_01 → Step `02_01_02` (pre-execution adjudication). Branch `feat/sc2egset-02-01-02-source-anchor-race-adjudication` from master @ `a4cc290f29c16378022915b51d2ae0fa52d602e8` (pyproject 3.68.0; PR #233 merged).

**Layer-1 diff for THIS planning PR = exactly 2 files:** `planning/current_plan.md` and `planning/current_plan.critique.md`. NO `current_plan.critique_resolution.md` is produced in Layer 1; the reviewer-adversarial pre-execution gate emits the critique only.

The plan body that follows describes the **future** Layer-2 adjudication-execution PR that this planning unit authorises (i.e., the next planner-science → reviewer-adversarial → executor cycle's `current_plan.md` payload), specifying exactly which three coupled decisions that future PR will resolve and what artifacts it will produce.

**Materialization caveats (Layer-1).** The Layer-1 tracked diff is exactly 2 files. The parent (orchestrator) is responsible for clearing any stale `planning/current_plan.md`, `planning/current_plan.critique.md`, and `planning/current_plan.critique_resolution.md` before `Write`. The Layer-1 PR itself does not author a critique-resolution artifact (no critique-resolution file is part of the Layer-1 diff).

The plan is deliberately NOT a materialization-execution plan; it is a "decide the inputs to the materialization-execution plan" plan. Materialization-execution planning is the **next** planner-science session after this one, gated on the three decisions resolving.

**Out of scope here (deferred to later sessions):**
- Materializing any of the 5 (or 9 designed) pre_game feature columns.
- Running the CROSS-02-01-v1.0.1 post-materialization audit / emitting a non-vacuous `02_01_02/leakage_audit_sc2egset.{json,md}`.
- The 6 `history_enriched_pre_game` and 11 `in_game_snapshot` families (02_01_03+).
- Any `STEP_STATUS` / `PIPELINE_SECTION_STATUS` / `PHASE_STATUS` flip; any `research_log` entry; any ROADMAP body edit; any spec amendment.
- Phase 03 (and 02_02..02_08); any thesis chapter prose; any AoE2 work.

## Problem Statement

PR #233 (merged at `a4cc290f`) scaffolded the 02_01_02 notebook + one structural validator and explicitly recorded a 3-way unresolved divergence as "**ONE coupled view-vs-raw decision** resolved at the future second-pass, NOT here" (`current_plan.md:107-109`). The reviewer-adversarial pre-execution critique at `current_plan.critique.md:122-130` confirmed: "**§4.1** is the most material divergence … the genuinely leakage-sensitive resolution is correctly deferred to the materialization PR plus its non-discharged Chat second-pass."

**Cleaning-layer project decision already on disk.** The schema YAMLs document the project's prior convention precisely:

- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml:101-103` (verbatim):
  > `- name: selectedRace`
  > `  reason: "Pre-game menu selection (includes 'Random'); race (actual played race) used instead."`

  i.e., `selectedRace` is **explicitly dropped** from the cleaned long-format view, and `race` is the surviving analytical race column.

- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml:52-53` (verbatim):
  > `  notes: PRE_GAME. Raw vocabulary (race actually played, not selectedRace which includes 'Random').`

  i.e., MHM `faction` is **classified PRE_GAME** in the cleaning layer, with `race` (not `selectedRace`) as its upstream source. This settles the U4/OQ1 provenance question of the original plan **without** a notebook probe — the YAML is authoritative.

**Empirical row counts (read-only DuckDB peek performed in the prior planning session).**

- `replay_players_raw.race` vocabulary: {Prot, Terr, Zerg} + 3 BW-legacy stems only. No `Rand` / `Random`.
- `replay_players_raw.selectedRace` vocabulary: includes **10 `Rand` rows + 1,110 blank rows (cleaned-view-normalized to `Random`) + Prot/Terr/Zerg**. The cleaned views show the canonicalised `Random` value after the `01_04_02` normalization step.
- `matches_history_minimal.faction` on-disk vocabulary: {Prot, Terr, Zerg} only — consistent with the MHM YAML's stated derivation from `race`.

**Reconciliation with RISK-26.** RISK-26 (`thesis/pass2_evidence/methodology_risk_register.md:489`) records: "the focal race feature for Random-pickers is `Random` at game-start time — NOT the eventual race the player commits to once the game begins." Read literally, RISK-26 says the only true pre-game race column is `selectedRace`. The cleaning layer made a different decision (race = PRE_GAME analytical convention; selectedRace = dropped). These two positions are not strictly contradictory — they cover different concerns (RISK-26 is about leakage semantics; the cleaning layer made an analytical-vocabulary stability choice that implicitly accepts the post-decision overwrite for Random-pickers as the canonical race). But they ARE in tension on a thesis-defensible methodology question that has not been adjudicated in writing anywhere in the repo.

**The three coupled unresolved decisions for the future Layer-2 adjudication-execution PR are:**

1. **Source-layer decision (Q1)** — raw-flat (`replay_players_raw`+`matches_flat`), cleaned-raw (`matches_flat_clean`, which is 1v1-scoped at the raw layer), view-layer (`matches_history_minimal`+`player_history_all`), or a hybrid (MHM for symmetric 1v1 pair + PH for map/patch/MMR-missing).
2. **Temporal anchor decision (Q2)** — split into two sub-decisions: (a) **Phase-02 row-identity timestamp choice** (raw VARCHAR `details_timeUTC` vs harmonized TIMESTAMP `started_at`), which is largely settled by the source-layer choice in Q1; (b) **Phase-03 chronological-hold-out anchor type RECOMMENDATION ONLY** — the binding decision is made in Phase 03 planning, not here. CROSS-02-03 §6.1 lines 235-242 confirms: a `pre_game` family "reads only static pre-match attributes of game T plus historical aggregates over games strictly prior to T" — for the 5 tranche-1 static game-T attributes, NO `<` filter applies and the anchor is a row-identity timestamp, not a window bound.
3. **Race-column decision (Q3) — cleaning-layer project decision vs RISK-26 reconciliation.** Two candidate outcomes, both LIVE; neither is pre-decided in this planning PR:
   - **Outcome Q3.RATIFY:** ratify the existing cleaning-layer convention (`race` = PRE_GAME analytical canon per `matches_long_raw.yaml:101-103` and `matches_history_minimal.yaml:52-53`; `selectedRace` excluded from cleaned views). Costs: tranche-1 inherits the post-decision overwrite for the 1,120 Random player-rows; downstream encoders see a 3-value race vocabulary; the gap between RISK-26 text and the cleaning convention is documented in the artifact MD but not patched.
   - **Outcome Q3.AMEND:** amend the cleaning-layer convention to honour RISK-26 literally. Costs: spec patches required to `matches_long_raw.yaml:101-103` (restore `selectedRace`), `matches_history_minimal.yaml:52-53` (re-source `faction` from `selectedRace`), and CROSS-02-02 §6.1 (clarify that the 4th `Random` value is actually carried in the MHM `faction` vocabulary); downstream consumers re-encode; canonicalisation rule for `Rand`/`Random` 2-spelling must be added.

   The Layer-2 adjudication artifact MUST present both outcomes as live options and adjudicate between them with explicit evidence and rationale; it MUST NOT pre-decide here.

**Narrowed novelty claim.** PR #233's plan at `planning/current_plan.md:374-376` already records that "Random is a 4th pre-game race; the eventually-played race is post-decision and is NOT used — RISK-26." This adjudication PR's contribution is therefore NOT "Random handling newly discovered" but rather:

- **(a)** elevating the decision to a thesis-citable adjudication artifact (3-decision CSV + 8-section MD, deterministic and citable);
- **(b)** settling column-name + canonicalisation-rule + row-retention dimensions that PR #233 left unspecified;
- **(c)** reconciling the cleaning-layer documented decision (`race` = PRE_GAME, `selectedRace` dropped) with RISK-26's "selectedRace is the only true pre-game race" — choosing between Q3.RATIFY and Q3.AMEND in writing with full rationale.

If a future materialization-execution PR tries to fold Q1+Q2+Q3 into one planning unit, it batches three thesis-citable methodology adjudications into one reviewer-adversarial cycle, falling exactly into the failure mode `.claude/rules/data-analysis-lineage.md` "Non-batching rule for empirical work" was written to prevent. This adjudication-planning unit splits the three decisions out into a dedicated planner-science → reviewer-adversarial → executor cycle whose **only** on-disk deliverable is a 3-decision adjudication artifact pair (CSV + MD) bound to repo evidence, so the next (materialization-execution) planning round inherits a single resolved input contract.

## Assumptions & Unknowns

- **Assumption (scope discipline).** This Layer-1 planning PR has a 2-file diff (`planning/current_plan.md`, `planning/current_plan.critique.md`) and authorises a SEPARATE FUTURE Layer-2 adjudication-execution PR whose diff is also small and bounded — see File Manifest. Materialization is **not** authorised by this plan and remains gated behind a still-later Layer-3 materialization-execution planner-science PR.
- **Assumption (predecessors closed).** Step `02_01_01` is closed per `STEP_STATUS.yaml:199`; the catalog registry CSV is the authoritative tranche-1 family-id catalog. The 5 tranche-1 family ids are stable; this plan does NOT propose changing them or their pre_game classification.
- **Assumption (cutoff semantics).** Per CROSS-02-03-v1.0.1 §6.1 (verbatim: a `pre_game` family "reads only static pre-match attributes of game T plus historical aggregates over games strictly prior to T") and CROSS-02-02-v1.0.1 §6.1 cutoff cell "none (game-T attribute)", `snapshot_at_match_start` is a static game-T attribute cutoff — **no `history_time < target_time` strict-`<` filter is required for the 5 tranche-1 families**. The Phase-02 anchor is a row-identity timestamp, not a window bound. Leak-freedom rests on the triad: (i) only game-T pre-game columns are read, (ii) POST-GAME token absence (CROSS-02-01-v1.0.1 §2.2), (iii) non-tracker source (Invariant I3). This adjudication does NOT change that — it picks columns that satisfy (i)–(iii).
- **Assumption (encoders specified, not fit).** Encoder design (race-pair, matchup, map, patch) is specified in the future materialization-execution PR and any future fit is **train-fold-only** (Invariant I3 normalization leakage); no encoder is fit by THIS adjudication PR or by the future Layer-2 adjudication-execution PR (because no feature is materialized).
- **Assumption (version bumps).** This Layer-1 planning PR does NOT bump `pyproject.toml`; the future Layer-2 adjudication-execution PR is `feat` minor `3.68.0 → 3.69.0` because it adds a new artifact pair under `reports/artifacts/` and a new validator module + test — to be confirmed in the adjudication-execution plan by quoting the git-workflow rule explicitly.

### Unknowns

- **U1. Source-layer choice.** Raw-flat / cleaned-raw / view / hybrid — none picked here; the Layer-2 adjudication-execution PR will document a single decision in the adjudication MD with evidence.
- **U2. Anchor choice (Phase-02 row-identity).** `details_timeUTC` (raw VARCHAR) vs `started_at` (harmonized TIMESTAMP) — none picked here; same artifact, same PR. Largely settled by U1 (the source-layer choice fixes which anchor is natively available).
- **U3. Race-column choice + Random handling — ratify-vs-amend.** The Layer-2 adjudication-execution PR will pick between Q3.RATIFY (keep the cleaning-layer convention; document the RISK-26 gap) and Q3.AMEND (patch the cleaning-layer YAMLs + CROSS-02-02 §6.1 to honour RISK-26 literally). If Q3.AMEND is chosen, the canonicalisation rule for the 2-spelling `Rand`/`Random` vocabulary and the 1,120-row sample handling (retain as 4th category, retain as 5th, exclude with documented bias, encode as sentinel-plus-flag) must also be decided in the same artifact. The Layer-2 artifact does NOT itself apply any spec patches; it PROPOSES them as a future PR target.

### Documented (no longer UNKNOWN)

- **U4 (DOCUMENTED, NOT BLOCKING).** MHM `faction` derives from `race` per `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml:52-53` (verbatim): "PRE_GAME. Raw vocabulary (race actually played, not selectedRace which includes 'Random')." The YAML is authoritative. The Layer-2 artifact MD §8 records: CROSS-02-02 §6.1's "Random is a fourth declared race at pre-game" wording is technically true at the pre-game level (Random IS a 4th declared race in `selectedRace`), but the MHM `faction` column does NOT carry the 4th value because the cleaning convention follows `race`. The artifact MD §8 proposes a CROSS-02-02 §6.1 minor amendment as a future-PR target ("MHM `faction` derives from `race` and so excludes Random from its vocabulary; the 4th value `Random` lives only in `selectedRace` in `replay_players_raw`"). The MHM-view-definition `duckdb_views()` probe is no longer needed; the YAML is the source of truth.

- **DEFERRED until after the adjudication artifact lands.** The exact projection SQL, the focal/opponent self-join keys, the encoder vocabularies, the I3 leakage-falsifier SQL for the future post-materialization CROSS-02-01 audit, the model-input grain (whether it stays `(focal_match_id, focal_player)` once the source-layer pick is made) — all gated on the adjudication artifact.

## Literature Context

This unit is a planning-only adjudication preparation; it introduces no empirical or literature claim and asserts no new finding. Governing repo sources cited verbatim or by anchor:

- **Invariants.** `.claude/scientific-invariants.md` I3 (no feature at game T from time T or later), I5 (symmetric player treatment), I6 (report-with-code), I7 (no magic numbers), I8 (shared cross-game pre-game categories must be defined at a level of abstraction that applies to both games), I9 (research pipeline discipline; a step references only its own artifacts plus completed predecessors' artifacts plus external source documentation), I10 (relative-path provenance).
- **Locked Phase-02 specs.**
  - CROSS-02-00-v3.0.1 §3.1 (canonical join + anchor on MHM = `player_id` + `started_at`); §3.2 (per-dataset raw anchor = `details_timeUTC` for sc2egset); §5.1 (MHM `faction` classification = PRE_GAME); §5.4 (PH `race` classification = PRE_GAME; PH `is_mmr_missing` classification = PRE_GAME).
  - CROSS-02-01-v1.0.1 §2.1 (cutoff structural check), §2.2 (POST-GAME token absence), §2.3 (normalization fit-scope), §3 (artifact schema), §4 (execution timing: AFTER materialization; vacuously satisfied here), §5 (gate condition).
  - CROSS-02-02-v1.0.1 §6.1 (sc2egset pre_game candidates: race / opp_race / matchup / map / patch / is_mmr_missing as missingness flag; Random is a 4th declared race; MMR scalar is forbidden because 83.95% missing).
  - CROSS-02-03-v1.0.1 §6.1 (pre_game cutoff = "none (game-T attribute)"; no `<` filter applies to the 5 tranche-1 static game-T attributes).
- **Cleaning-layer schema YAMLs (authoritative for cleaned-view column provenance).**
  - `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml:101-103` (selectedRace excluded; race used).
  - `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml:52-53` (MHM `faction` PRE_GAME; derived from `race` not `selectedRace`).
- **Methodology risk register.** RISK-20 line 375 (cross-region fragmentation; not the tranche-1 driver but adjacent), RISK-24 line 445 (focal/opponent slot asymmetry across dataset table shapes; relevant for U1 because the source-layer choice fixes the self-join shape), RISK-26 line 479-492 (Random race semantics for pre-game features; the operative reason for the Q3.AMEND outcome candidate).
- **Lineage rule.** `.claude/rules/data-analysis-lineage.md` "Non-batching rule for empirical work" (sequence 1–9; halt before artifact generation if assumption unreviewed / falsifier fails / source semantics unclear); "Feature-engineering discipline" (every feature family must declare dataset / source table / prediction setting / feature table grain / temporal anchor / allowed cutoff rule / leakage falsifier / cold-start behavior / lineage artifact); "Stop conditions" (specifically: source semantics are unclear → halt).
- **SQL/data and Python code rules** (loaded in-session by sql-data and python-code system reminders). Notable bindings: replay_id canonical join key (`regexp_extract(filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1) AS replay_id`); `matches_flat` is two-rows-per-game → always `COUNT(DISTINCT replay_id)`; SQL queries appear verbatim in MD artifact (I6); module-level UPPER_SNAKE constants; named SQL constants with `_QUERY` suffix.

[OPINION] The choice to insert an adjudication-planning unit between PR #233's scaffold and the eventual materialization-execution PR is grounded in the non-batching rule + the Q3.RATIFY-vs-Q3.AMEND ratify-vs-amend tension surfaced once `matches_long_raw.yaml:101-103` and `matches_history_minimal.yaml:52-53` are read alongside RISK-26.

## Execution Steps

> **All tasks below are for the FUTURE Layer-2 adjudication-execution PR**, on the same branch (`feat/sc2egset-02-01-02-source-anchor-race-adjudication`), after this plan is approved on the draft planning PR and an explicit execution turn begins. The Layer-2 PR creates ONE artifact pair under `reports/artifacts/`, persists ZERO feature values, runs ZERO projection SQL against feature data, and writes ZERO status YAML / research_log / ROADMAP / spec / chapter changes.
>
> The plan body MUST distinguish:
> - **This turn's diff (Layer 1):** exactly 2 files — `planning/current_plan.md` + `planning/current_plan.critique.md`.
> - **Future adjudication-execution PR diff (Layer 2):** the manifest in §File Manifest below — 9 files, explicitly free of materialization.
> - **Future materialization-execution PR (Layer 3, NOT this plan):** a separate planner-science round after the adjudication artifact lands.

### T01 — Read & verify the four locked specs + two YAML schemas against on-disk DuckDB

Sandbox notebook path (jupytext-paired) `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.py` (NEW; `.ipynb` paired). Cells: banner ("Source / anchor / race-column adjudication preparation — NON-MATERIALIZATION; persists ONE adjudication artifact pair only; touches NO feature data") → context (the 4 specs, the 2 cleaning-layer YAML schemas, the registry CSV, the PR #229 §10 verdict CSV, the PR #230 vacuous leakage JSON, the methodology risk register entries, this plan path) → 3-decision question table (Q1 source-layer, Q2 anchor split into Phase-02 + Phase-03 RECOMMENDATION, Q3 ratify-vs-amend) → per-decision "read repo evidence + run column-existence read-only DuckDB peek" subsection → per-decision adjudication paragraph (with falsifier list) → write the artifact pair (T04) → closing "no feature value materialized, no status flipped" cell.

Constraints (sandbox/README.md + python-code rule): no `def`/`class`/lambda in cells; cells ≤ 50 lines; `print()` for exploration, logger for diagnostics; no plan codes (T01/Q1) in cell text — use descriptive prose (e.g., "Decision Q1 — source-layer adjudication" is fine because Q1 is part of the artifact's CSV `decision_id` and so is descriptive, not a plan code); seed 42 referenced but unused. DuckDB read-only patterns only: `SELECT … LIMIT 5`, `DESCRIBE`, `SELECT COUNT(DISTINCT …)`, `SELECT col, COUNT(*) GROUP BY 1`. **FORBIDDEN:** `CREATE`, `INSERT`, `COPY`, `to_parquet`, `write_*`, `df.to_csv`, any aggregate over more than 50 GROUP BY groups (no scan of full data).

Per-decision peek queries — declared in the notebook by name and embedded in the artifact MD verbatim (I6):

- **Q1 source-layer.** `DESCRIBE matches_history_minimal`; `DESCRIBE player_history_all`; `DESCRIBE matches_flat`; `DESCRIBE matches_flat_clean`; `DESCRIBE replay_players_raw`; row counts (`SELECT COUNT(*) FROM <each>`); distinct-key counts (`SELECT COUNT(DISTINCT match_id) FROM matches_history_minimal`, `SELECT COUNT(DISTINCT replay_id) FROM matches_flat_clean`); the join-cardinality sanity (`SELECT COUNT(*) FROM matches_flat_clean mfc JOIN matches_history_minimal mhm ON CONCAT('sc2egset::', mfc.replay_id) = mhm.match_id AND mfc.toon_id = mhm.player_id` must equal 44,418).
- **Q2 anchor.** Type checks via DESCRIBE (`details_timeUTC VARCHAR` vs `started_at TIMESTAMP`); null-rate checks (`SELECT COUNT(*) FILTER (WHERE details_timeUTC IS NULL) FROM matches_flat_clean` — verified 0 in this session); ordering-stability check (`SELECT MIN(started_at), MAX(started_at) FROM matches_history_minimal`); cross-row-equality within a match (`SELECT COUNT(*) FROM matches_history_minimal m1 JOIN matches_history_minimal m2 ON m1.match_id=m2.match_id AND m1.player_id<m2.player_id WHERE m1.started_at != m2.started_at` — must equal 0).
- **Q3 race-column + Random.** `SELECT race, COUNT(*) FROM replay_players_raw GROUP BY 1` (confirmed Prot/Terr/Zerg+3 BW; no Rand); `SELECT selectedRace, COUNT(*) FROM replay_players_raw GROUP BY 1` (confirmed includes `Rand`=10, blank=1,110); the cleaned-view normalisation check (`SELECT selectedRace, COUNT(*) FROM matches_flat_clean GROUP BY 1` to verify the blank rows surface as the canonical `Random` token); `SELECT race, selectedRace, COUNT(*) FROM replay_players_raw WHERE race != selectedRace GROUP BY 1,2` (confirms which Random-pickers eventually played which race); same trio against `matches_flat_clean`, `player_history_all`, `matches_history_minimal`. **Note:** the MHM `faction` provenance is DOCUMENTED by `matches_history_minimal.yaml:52-53` (race actually played, not selectedRace) — no `duckdb_views()` probe is required; the YAML is authoritative.

**Stop condition.** If T01 peek surfaces a fact that materially contradicts any locked spec OR the two cleaning-layer YAML schemas (e.g., MHM `faction` distribution unexpectedly includes a `Random` value, which would contradict the MHM YAML's stated derivation), HALT before artifact write, record the contradiction in the artifact MD as a finding requiring a CROSS-02-00 §7 minor spec amendment OR a cleaning-layer YAML correction, set the artifact JSON `decisions_recorded` field to `partial`, and route the issue to a separate planner-science round.

### T02 — Author the adjudication module

Module path: `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_pre_game_source_layer.py` (NEW). Conventions match the existing validator modules (`validate_pre_game_feature_materialization.py`, `validate_registry_section10_verdicts.py`): `from __future__ import annotations`; `logging.getLogger(__name__)`; no `print`; frozen dataclasses; ONE public `adjudicate_pre_game_source_layer` entrypoint; private `_check_*` and `_render_*` helpers; module-level UPPER_SNAKE constants (I7); named SQL constants with `_QUERY` suffix per python-code rule.

Module-level constants (illustrative; the final constant list is fixed in the Layer-2 adjudication-execution PR, not here):

- `EXPECTED_MHM_ROW_COUNT: int = 44418`
- `EXPECTED_MHM_DISTINCT_MATCH_ID: int = 22209`
- `EXPECTED_MFC_ROW_COUNT: int = 44418`
- `EXPECTED_PH_ROW_COUNT: int = 44817`
- `EXPECTED_RPR_ROW_COUNT: int = 44817`
- `EXPECTED_MF_ROW_COUNT: int = 44817`
- `EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID: int = 22209`
- `PRE_GAME_RACE_TOKENS: frozenset[str] = frozenset({"Prot", "Terr", "Zerg", "Rand", "Random"})`
- `POST_DECISION_RACE_TOKENS: frozenset[str] = frozenset({"Prot", "Terr", "Zerg"})` (the eventually-played race vocabulary, used to detect a `race`-vs-`selectedRace` mis-pick under Q3.AMEND)
- `BW_LEGACY_RACE_TOKENS: frozenset[str] = frozenset({"BWPr", "BWTe", "BWZe"})` (1 row each in raw; verify whether MFC drops them)
- `RANDOM_SPELLING_CANONICAL: str = "Random"` (default canonicalisation under Q3.AMEND only; the cleaned-view normalisation step already produces this token)
- `EXPECTED_RAND_ROW_COUNT: int = 10`
- `EXPECTED_BLANK_SELECTED_RACE_ROW_COUNT: int = 1110`
- `_MHM_DESCRIBE_QUERY: str = "DESCRIBE matches_history_minimal"`
- … one named `_<probe>_QUERY` per peek listed in T01. **NOTE:** `_MHM_VIEW_DEFINITION_QUERY` is NOT a constant — the MHM YAML at `matches_history_minimal.yaml:52-53` is the authoritative source for `faction` provenance, so no `duckdb_views()` probe is performed.

Frozen dataclasses (illustrative API):

```python
@dataclass(frozen=True)
class SourceLayerCandidate:
    name: str
    family_to_source_table_map: tuple[tuple[str, str], ...]
    self_join_keys_focal_opponent: tuple[str, ...]
    one_v_one_scope_native: bool
    anchor_column: str
    anchor_type: str
    risks_inherited: tuple[str, ...]
    sql_complexity_note: str

@dataclass(frozen=True)
class AnchorCandidate:
    column: str
    type_: str
    scope_native: str
    null_rate_observed: int
    decision_rationale: str

@dataclass(frozen=True)
class RaceColumnCandidate:
    column: str
    vocabulary_observed: tuple[str, ...]
    contains_random: bool
    contains_post_decision_overwrite: bool
    canonicalisation_rule: str
    cleaning_layer_status: str   # "ratify_existing" | "amend_existing"
    risk_26_compliance: str      # "compliant" | "documented_gap" | "violated"

@dataclass(frozen=True)
class AdjudicationDecision:
    decision_id: str             # "Q1_source_layer" | "Q2_anchor" | "Q3_race_and_random"
    candidates_considered: tuple[str, ...]
    chosen: str
    rationale_paragraph: str     # 80–250 words, cites spec/RISK/invariant
    falsifiers_recorded: tuple[str, ...]
    blocking_for_materialization: bool

@dataclass(frozen=True)
class AdjudicationResult:
    passed: bool
    decisions: tuple[AdjudicationDecision, ...]   # exactly 3
    contradictions_with_specs: tuple[str, ...]
    spec_amendments_proposed: tuple[str, ...]     # e.g. "CROSS-02-02 §6.1 minor: faction excludes Random"
    materialized_output_paths: tuple[str, ...]    # ALWAYS () — adjudication persists ONLY the artifact pair
    artifact_csv_path: str
    artifact_md_path: str
    halting_falsifier: str | None
```

Signatures (unchanged from prior plan; reproduced for completeness):

```python
def adjudicate_pre_game_source_layer(
    duckdb_path: Path | str,
    registry_csv_path: Path | str,
    output_artifact_dir: Path | str,
) -> AdjudicationResult: ...
def _run_source_layer_peeks(con: duckdb.DuckDBPyConnection) -> dict[str, Any]: ...
def _run_anchor_peeks(con: duckdb.DuckDBPyConnection) -> dict[str, Any]: ...
def _run_race_and_random_peeks(con: duckdb.DuckDBPyConnection) -> dict[str, Any]: ...
def _adjudicate_source_layer(peeks: dict[str, Any]) -> AdjudicationDecision: ...
def _adjudicate_anchor(peeks: dict[str, Any]) -> AdjudicationDecision: ...
def _adjudicate_race_and_random(peeks: dict[str, Any]) -> AdjudicationDecision: ...
def _render_artifact_csv(result: AdjudicationResult, out_path: Path) -> None: ...
def _render_artifact_md(result: AdjudicationResult, out_path: Path) -> None: ...
```

### T03 — One test file

`tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_pre_game_source_layer.py` (mirrored tree per python-code rule). Coverage:

1. Frozen-dataclass shape: 3 decisions exactly; each decision has a non-empty rationale_paragraph ≥ 80 chars; `materialized_output_paths == ()` always.
2. Falsifier `q1_no_evidence`: synthetic DuckDB with empty MHM/PH raises the q1_no_evidence halting falsifier.
3. Falsifier `q2_anchor_type_mismatch`: synthetic MHM with `started_at VARCHAR` (instead of TIMESTAMP) flags `anchor_type_mismatch`.
4. Falsifier `q3_race_post_decision_chosen` (Q3.AMEND-path test): a candidate that picks `race` not `selectedRace` under an Amend outcome triggers `race_post_decision_chosen`.
5. Falsifier `q3_prior_decision_silently_reversed` (Q3.RATIFY-vs-AMEND silent-reversal test): the artifact picks an outcome (RATIFY or AMEND) but does NOT explicitly cite either `matches_long_raw.yaml:101-103` (ratify path) OR a proposed YAML patch (amend path) in its rationale — i.e., the prior cleaning-layer decision is silently overturned or silently kept without acknowledgement.
6. Falsifier `q3_random_vocabulary_dropped`: under Q3.AMEND, a candidate that excludes both `Rand` and `Random` from the projected vocabulary triggers `random_vocabulary_dropped` (RISK-26 violation).
7. Falsifier `q1_source_layer_loses_1v1_scope`: a candidate that picks raw `matches_flat` without an explicit 1v1 filter triggers `one_v_one_scope_lost`.
8. Stale registry path raises (mirrors the existing scaffold validator test pattern).
9. Real-DB smoke test (`pytest.mark.skipif` if DB absent): runs `adjudicate_pre_game_source_layer` and asserts `result.passed is True`, `len(result.decisions) == 3`, `result.materialized_output_paths == ()`, and the artifact files exist at the canonical paths after the call.
10. **MHM-`faction`-Random absence smoke test**: assert MHM `faction` vocabulary observed by the peek equals `{"Prot", "Terr", "Zerg"}` AND the adjudication artifact MD §8 records this as consistent with `matches_history_minimal.yaml:52-53` AND proposes a CROSS-02-02 §6.1 minor amendment (`spec_amendments_proposed` non-empty for this row); test does NOT treat the 3-value observation as a halting contradiction.

Tests must pass coverage ≥ 95% (`fail_under=95`); mirror tree per python-code rule.

### T04 — Artifact pair (the ONLY on-disk output of the Layer-2 PR)

Path (CSV): `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv`
Path (MD): `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.md`

**Note:** path uses the existing `02_feature_engineering/01_pre_game_vs_in_game_boundary/` directory (consistent with the §10 verdict CSV/MD that PR #229 created in the same directory); NOT the `reports/artifacts/02_01_02/` directory which the CROSS-02-01-v1.0.1 §3 schema reserves for the **post-materialization leakage audit JSON+MD** (which this PR does NOT produce — that artifact remains FUTURE and lands only when the materialization-execution PR runs).

CSV schema (deterministic order; 3 rows = 3 decisions): `decision_id, decision_name, candidates_considered (semicolon-separated), chosen, rationale_excerpt_300char, falsifiers_recorded (semicolon-separated), blocking_for_materialization, spec_contradictions (semicolon-separated; empty when none), spec_amendments_proposed (semicolon-separated; empty when none), provenance_git_sha, provenance_executed_at_utc_date, audit_pr, validator_module, validator_module_sha256, duckdb_path, duckdb_path_sha256, registry_csv_sha256, methodology_risk_register_sha256, spec_02_00_sha256, spec_02_01_sha256, spec_02_02_sha256, spec_02_03_sha256, matches_long_raw_yaml_sha256, matches_history_minimal_yaml_sha256`. The CSV is byte-deterministic across reruns on the same UTC date with the same `git_sha` + tool versions (PR #229 precedent).

MD companion sections (numbered, mandatory):

1. **Top non-overclaim disclaimer** (4 lines max): "This artifact is an adjudication of three coupled pre-materialization questions for sc2egset Step 02_01_02. It does NOT materialize any feature value, does NOT run the CROSS-02-01-v1.0.1 post-materialization leakage audit, and does NOT close Step 02_01_02. The CROSS-02-01 audit remains FUTURE and remains vacuously satisfied by PR #230 until a materialization PR lands."

2. **Q1 source-layer.** Verbatim SQL of each peek + result (I6). Candidates considered (4): raw-flat, cleaned-raw (`matches_flat_clean`), view-layer (MHM+PH), hybrid (MHM-for-pair + `matches_flat_clean`-for-static). The chosen candidate is named explicitly. Rationale paragraph cites: CROSS-02-00 §3.1 / §3.2 / §5.4; Invariant I5 (the self-join shape must be identical for both slots); RISK-24 (focal/opponent slot asymmetry).

3. **Q2 anchor — two sub-decisions.**
   - **Q2(a) Phase-02 row-identity timestamp choice.** Verbatim SQL of each peek + result. Candidates considered: raw VARCHAR `details_timeUTC`, harmonized TIMESTAMP `started_at`, hybrid (use `started_at` as the row-identity column; retain `details_timeUTC` as a provenance column never used in filters). Largely settled by Q1 (the source-layer choice fixes which anchor is natively available). The chosen candidate is named explicitly. Rationale cites CROSS-02-00 §3.1 (canonical cross-dataset dtype TIMESTAMP) and §3.3 (UTC session discipline). **Per CROSS-02-03 §6.1, no `<` filter applies to the 5 tranche-1 static game-T attributes; the anchor here is a row-identity timestamp, not a window bound.**
   - **Q2(b) Phase-03 chronological-hold-out anchor type — RECOMMENDATION ONLY.** The Layer-2 artifact records a RECOMMENDATION for the Phase 03 chronological hold-out anchor (likely `started_at TIMESTAMP` for ordering) but explicitly states that the binding decision is made in Phase 03 planning, NOT in this Layer-2 artifact. The recommendation is a downstream-coupling note, not a Phase-02 deliverable.

4. **Q3 race-column + Random — cleaning-layer ratify-vs-amend.** Verbatim SQL of each peek + result. Two outcome candidates, both LIVE:

   - **Q3.RATIFY (candidate A):** retain the cleaning-layer convention. Rationale: `matches_long_raw.yaml:101-103` and `matches_history_minimal.yaml:52-53` document the existing decision (race = PRE_GAME analytical canon; selectedRace dropped). Implications: tranche-1 inherits the post-decision overwrite for the 1,120 Random player-rows; downstream encoders see a 3-value race vocabulary; the gap between RISK-26 text and the cleaning convention is documented in the artifact MD §8 but not patched.
   - **Q3.AMEND (candidate B):** patch the cleaning-layer YAMLs + CROSS-02-02 §6.1 to honour RISK-26 literally. Spec patches required: (i) `matches_long_raw.yaml:101-103` removes the `selectedRace` exclusion; (ii) `matches_history_minimal.yaml:52-53` re-sources `faction` from `selectedRace`; (iii) CROSS-02-02 §6.1 clarifies that the 4th `Random` value is now carried in the MHM `faction` vocabulary. Sub-decision for Random vocabulary handling (4 candidates): (a) retain as 4th category `Random` (canonicalise `Rand`→`Random`; the verbose `Random` spelling dominates 1,110:10 and matches the cleaned-view normalisation); (b) retain as 5th category (preserve `Rand`/`Random` separately); (c) exclude with documented bias (drop 1,120 player-rows ≈ 555 matches); (d) encode as sentinel and add a `selected_random_flag` flag column.

   The chosen outcome (A or B) is named explicitly with rationale ≥ 250 words. The artifact MD does NOT itself apply any spec patches even under Q3.AMEND; it PROPOSES them as a future-PR target (recorded in `spec_amendments_proposed`).

5. **Falsifier roll-call.** Every falsifier from §Falsifiers below is listed by name with verdict "did not fire" or "FIRED → halt" (if any FIRED, the Layer-2 PR HALTS at T04 and does NOT write the artifact CSV — see Stop Conditions).

6. **Inputs to the FUTURE materialization-execution planner-science round.** The 3 decisions, restated as frozen inputs:
   - Source layer = `<chosen>`; family→table map = `<map>`; self-join keys = `<keys>`.
   - Anchor = `<chosen>`; type = `<TIMESTAMP|VARCHAR>`; use as window-bound = `false` (static game-T attribute per CROSS-02-03 §6.1); use as row-identity = `true`. Phase-03 RECOMMENDATION = `<chosen>` (NON-BINDING).
   - Race column = `<chosen under Q3.RATIFY or Q3.AMEND>`; Random handling = `<chosen>`; canonicalisation rule = `<chosen>`; row-retention impact = `<n>` rows retained, `<n>` rows excluded (if exclusion chosen); RISK-26 compliance = `<compliant|documented_gap>`.
   - **`lineage_position` (per N6 carry-forward):** "artifact #4 in the 5-artifact lineage for Step 02_01_02 readiness (after: PR #229 §10 design-time verdict pair; PR #230 vacuous CROSS-02-01 audit pair; PR #233 scaffold + 1 validator; this 3-decision adjudication; before: Layer-3 materialization-execution audit pair)."

7. **Explicit non-substitution statement.** This artifact does NOT replace, weaken, or amend: (a) PR #229 §10 design-time verdict-audit pair; (b) PR #230 CROSS-02-01 vacuous leakage-audit pair; (c) the FUTURE post-materialization CROSS-02-01 audit (which does not yet exist and is not produced here). The CROSS-02-01-v1.0.1 post-materialization leakage audit and the mandatory Claude/ChatGPT second-pass leakage review remain FUTURE.

8. **Spec amendments proposed (NOT applied here).** Under Q3.RATIFY: the artifact records that CROSS-02-02 §6.1's "Random is a fourth declared race at pre-game" wording is technically true at the pre-game level (in `selectedRace`) but the MHM `faction` column does NOT carry the 4th value because the cleaning convention follows `race` per `matches_history_minimal.yaml:52-53`. A CROSS-02-02 §6.1 minor amendment is proposed as a future-PR target (text: "MHM `faction` derives from `race` and so excludes Random from its vocabulary; the 4th value `Random` lives only in `selectedRace` in `replay_players_raw`"). Under Q3.AMEND: the artifact records the three patches enumerated in §4 (Q3.AMEND candidate). In both outcomes, the patches are PROPOSED only — not applied in this PR.

### T05 — Release tail + scope verification (Layer-2)

- `pyproject.toml` 3.68.0 → 3.69.0 (minor; Category A feat-style adjudication artifact addition; consistent with git-workflow rule "minor for feat" applied to the addition of a new on-disk artifact pair). Quote git-workflow rule explicitly in the Layer-2 plan when bumping.
- `CHANGELOG.md` `[Unreleased]` → `[3.69.0] — <YYYY-MM-DD> (PR #<N>: feat/sc2egset-02-01-02-source-anchor-race-adjudication)` with Added: validator + tests + notebook scaffold + artifact pair; Notes: zero-materialization, no status flip, leakage audit remains future/vacuous.
- `planning/INDEX.md`: archive-line update for PR #233; new Active line for this PR.
- Final scope check: tracked diff = exactly the 9 files in the Layer-2 manifest below; no extra file; no `data_artifacts` Parquet; no status YAML; no research_log; no ROADMAP body edit; no spec amendment (proposed amendments are recorded in the artifact MD only).

### Falsifiers (validator + reviewer enforce; any fired falsifier HALTS the Layer-2 PR)

- **F-Q1-source-1v1-lost.** A candidate source layer drops below `EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID` (22,209) without explicit 1v1 filter.
- **F-Q1-source-grain-mismatch.** A candidate source layer fails the self-join-cardinality check (`COUNT(*)` after self-join != 44,418 = 2 × 22,209), violating Invariant I5.
- **F-Q1-source-missing-column.** A candidate source layer does not carry one of the required columns natively AND the candidate does not specify a single explicit JOIN to a sibling table that does.
- **F-Q2-anchor-type-mismatch.** The chosen Phase-02 row-identity anchor is VARCHAR and the artifact provides no provenance-only justification for retaining VARCHAR (Q2(a) sub-decision).
- **F-Q2-anchor-cross-row-inconsistency.** Anchor values differ across the two player rows of the same match (`m1.started_at != m2.started_at` for any match_id) — should be 0.
- **F-Q3-race-post-decision-chosen.** Under Q3.AMEND, the chosen race column has vocabulary `{Prot, Terr, Zerg}` only — direct evidence the column is post-decision (RISK-26 leak).
- **F-Q3-prior-decision-silently-reversed.** The artifact picks Q3.RATIFY or Q3.AMEND but does NOT explicitly cite the prior cleaning-layer decision (`matches_long_raw.yaml:101-103` for RATIFY; or a proposed YAML patch text for AMEND) in its rationale — i.e., the prior decision is silently overturned or silently kept without acknowledgement.
- **F-Q3-random-vocabulary-dropped.** Under Q3.AMEND, the chosen race-projection projects {Prot, Terr, Zerg} only and explicitly drops the 1,120 Random player-rows without choice (d) sentinel-flag mitigation OR choice (c) explicit-exclusion documented bias.
- **F-Q3-random-spelling-uncanonicalised.** Under Q3.AMEND, the chosen projection preserves both `Rand` and `Random` as distinct categories without a canonicalisation rule (causes a 2-spelling vocabulary that downstream encoders will inflate).
- **F-spec-amendment-silent.** A spec amendment is proposed in the artifact MD §8 prose but is NOT recorded in the CSV `spec_amendments_proposed` field.
- **F-non-substitution-silent.** The artifact MD omits the explicit non-substitution statement (§7).
- **F-materialization-creep.** Any code path computes a feature value; `materialized_output_paths != ()`; or any Parquet/feature-table file is written to disk.
- **F-status-flip.** The diff touches any `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` / `research_log.md` / `ROADMAP.md` / any `reports/specs/*` file / any `data/db/schemas/views/*.yaml` file.
- **F-phase03-creep.** Any Phase 03 (or 02_01_03+) file or content appears in the diff. (The Q2(b) Phase-03 RECOMMENDATION lives INSIDE the Layer-2 artifact MD only; it does not write a Phase-03 file.)
- **F-tracker-creep.** Any read of `tracker_events_raw` appears in the adjudication validator module or notebook (Invariant I3; the 5 tranche-1 families are non-tracker by registry classification).
- **F-leakage-audit-overclaim.** Any text in the artifact, validator, test, notebook, research_log (FUTURE), changelog claims that the CROSS-02-01 post-materialization audit has been run, has cleared leakage, or that Step 02_01_02 is closed.
- **F-batching.** The PR diff includes a notebook that materializes a feature value OR includes the post-materialization audit artifact pair OR includes a status YAML flip — i.e., batches sequence steps 3..9 with this adjudication.

### T06 — Mandatory ChatGPT second-pass leakage review (FUTURE; not discharged here)

The Layer-2 adjudication-execution PR's reviewer-adversarial pre-execution gate is REQUIRED but does NOT discharge the still-future mandatory Claude/ChatGPT second-pass leakage review over the eventual projection SQL. **This Layer-1 planning PR satisfies NEITHER gate.** State explicitly in the adjudication MD §7 closing note: "The CROSS-02-01-v1.0.1 post-materialization leakage audit and the mandatory Claude/ChatGPT second-pass leakage review remain FUTURE. They are distinct gates and are not discharged by this artifact."

## File Manifest

| File | Action | Layer |
|------|--------|-------|
| `planning/current_plan.md` | Create (this plan) | 1 (this turn — 2-file diff) |
| `planning/current_plan.critique.md` | Create (reviewer-adversarial pre-execution gate output) | 1 (this turn) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.py` | Create (jupytext py:percent notebook source) | 2 (future adjudication-execution PR) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.ipynb` | Create (jupytext-paired notebook) | 2 (future) |
| `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_pre_game_source_layer.py` | Create (validator + adjudicator module) | 2 (future) |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_pre_game_source_layer.py` | Create (mirrored-tree test file) | 2 (future) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv` | Create (3-row deterministic CSV) | 2 (future) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.md` | Create (8-section MD with verbatim peek SQL) | 2 (future) |
| `planning/INDEX.md` | Update (archive PR #233; new Active line) | 2 (future) |
| `CHANGELOG.md` | Update (`[Unreleased]` → `[3.69.0]`) | 2 (future) |
| `pyproject.toml` | Update (3.68.0 → 3.69.0) | 2 (future) |

**Layer-1 tracked diff = 2 files (exactly).** **Layer-2 tracked diff = 9 files added on top of Layer 1 (11 total on branch).** NO `data_artifacts` Parquet, NO `02_01_02/leakage_audit_sc2egset.{json,md}`, NO `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml`, NO `research_log.md`, NO `ROADMAP.md`, NO `reports/specs/*` patch, NO cleaning-layer YAML patch.

## Gate Condition

The Layer-2 adjudication-execution PR is mergeable iff ALL of:

1. `adjudicate_pre_game_source_layer(duckdb_path, registry_csv_path, output_artifact_dir)` returns `result.passed=True` (`halting_falsifier is None`); exactly 3 decisions are present; each decision is non-empty with rationale_paragraph ≥ 80 chars; `materialized_output_paths == ()`.
2. `pytest tests/ -v` green (test count includes the new test file); coverage ≥ 95% (`fail_under=95`); ruff + mypy clean (pre-commit hooks).
3. jupytext `.py` / `.ipynb` pair in sync (jupytext pre-commit hook); BOTH staged.
4. The final tracked diff matches Layer-2 manifest EXACTLY (9 files added in Layer 2 on top of the 2 in Layer 1 = 11 files total on the branch). No artifact under `reports/artifacts/02_01_02/`. No `data_artifacts` Parquet. No status YAML / research_log / ROADMAP / spec / cleaning-layer YAML edit.
5. `02_01_01/leakage_audit_sc2egset.json` still has `features_audited == []` (vacuity preserved); no `02_01_02/leakage_audit_*.json` file exists.
6. PR #229 §10 verdict-audit CSV+MD untouched; PR #230 leakage JSON+MD untouched; registry CSV+MD untouched.
7. The reviewer-adversarial critique gate is satisfied (recorded in `planning/current_plan.critique.md` for Layer 1; for Layer 2, the same critique pre-execution gate runs again on the executed plan).
8. The artifact MD §8 "Spec amendments proposed" is either "None" or each listed amendment has a proposed CROSS-02-00 §7 (or cleaning-layer YAML) routing (no silent amendments).
9. The artifact MD §7 contains the verbatim "does NOT replace … does NOT clear leakage … remains FUTURE" non-substitution statement.
10. The artifact MD §3 (Q2) explicitly distinguishes Q2(a) Phase-02 row-identity (BINDING) from Q2(b) Phase-03 chronological hold-out anchor (RECOMMENDATION ONLY, non-binding).
11. The artifact MD §4 (Q3) explicitly presents both Q3.RATIFY and Q3.AMEND outcomes and names which was chosen with rationale ≥ 250 words.
12. The artifact MD §6 contains the `lineage_position` field (artifact #4 in the 5-artifact lineage).

## Open Questions

- **OQ1 (DOCUMENTED, NOT BLOCKING).** MHM `faction` derives from `race` per the MHM YAML at `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml:52` (verbatim: "PRE_GAME. Raw vocabulary (race actually played, not selectedRace which includes 'Random')"). The Layer-2 artifact MD §8 records that CROSS-02-02 §6.1's "Random is a fourth declared race" wording is technically true at the pre-game level (in `selectedRace`) but the MHM `faction` column does NOT carry the 4th value because the cleaning convention follows `race`. The artifact MD §8 proposes a CROSS-02-02 §6.1 minor amendment as a future-PR target (text: "MHM `faction` derives from `race` and so excludes Random from its vocabulary; the 4th value `Random` lives only in `selectedRace` in `replay_players_raw`").
- **OQ2 (DEFERRED to a future planner-science round, never to this PR).** Materialization-execution planning. Inputs are the 3 decisions from the adjudication artifact. The materialization-execution PR is gated on the adjudication artifact existing on disk and the mandatory Claude/ChatGPT second-pass leakage review over the chosen projection SQL.
- **OQ3 (DEFERRED).** The 6 `history_enriched_pre_game` families (02_01_03+) inherit the source-layer and anchor decisions from this artifact. The Random-handling decision does NOT propagate to history families because RISK-26 is a pre-game-only concern.
- **OQ4 (the reviewer-adversarial PR #233 nit 1 carried over).** Risk-register path: the future Layer-2 notebook + adjudicator module must cite RISK-20/24/26 by the `thesis/pass2_evidence/methodology_risk_register.md` path, not the dataset-level `risk_register_sc2egset.csv` which uses the SC-R scheme.
- **OQ5 (post-PR-#233 surprising-finding routing).** The `Rand`/`Random` 2-spelling vocabulary surfaced in this session was not previously documented in any per-dataset INVARIANTS.md, dataset risk register, or research_log entry. The Layer-2 artifact MD §8 must propose either a new sc2egset INVARIANTS.md row OR a CROSS-02-00 §5.4 patch amendment to record the on-disk vocabulary fact (`Rand`=10 + blank=1,110 in `selectedRace`; cleaned-view-normalised to `Random` after 01_04_02). The amendment is NOT made in this PR; only proposed in the artifact.

## Out of Scope

- Materializing any of the 5 tranche-1 (or 9 designed) pre_game feature columns.
- Producing the post-materialization CROSS-02-01-v1.0.1 audit artifact pair at `reports/artifacts/02_01_02/`.
- The 6 `history_enriched_pre_game` and 11 `in_game_snapshot` families.
- Any `STEP_STATUS` / `PIPELINE_SECTION_STATUS` / `PHASE_STATUS` flip.
- Any `research_log` entry (dataset-level or root CROSS-).
- Any ROADMAP body edit.
- Any `reports/specs/*` amendment (spec amendments are PROPOSED in the artifact MD only; they are applied in a separate Category A or E PR).
- Any cleaning-layer YAML edit (`matches_long_raw.yaml`, `matches_history_minimal.yaml`; if Q3.AMEND is chosen, the YAML patches are PROPOSED only).
- Phase 03 and any 02_02..02_08 work.
- Any thesis chapter prose / bib / appendix / docs / .claude / AoE2 edit.

## Evidence-distinctness ledger (must remain true post-PR)

- **PR #229 §10 design-time verdict audit pair:** per-family DESIGN-TIME verdicts (26 rows); NOT a leakage clearance.
- **PR #230 CROSS-02-01 vacuous audit pair:** `features_audited=[]`; PASS-by-vacuity; NOT a substitute for the future post-materialization audit.
- **PR #233 scaffold + 1 validator:** notebook scaffold + one structural validator; persists NOTHING; not a leakage clearance.
- **THIS PR's eventual Layer-2 adjudication artifact pair:** a 3-decision adjudication recording the source-layer / anchor / race-column-plus-Random-handling (ratify-vs-amend) choices and any spec amendments PROPOSED; persists ONE artifact pair; NOT a leakage clearance; NOT a materialization; does NOT close Step 02_01_02. **`lineage_position` = artifact #4 of 5.**
- **Future Layer-3 materialization-execution PR (not authorised by this plan):** materializes the 5 (or 9 designed) feature columns, runs the post-materialization CROSS-02-01 audit, emits `02_01_02/leakage_audit_sc2egset.{json,md}` with `features_audited != []`, flips the status YAMLs and writes the dataset research_log entry. Distinct from this PR; not produced here. **`lineage_position` = artifact #5 of 5.**

All five evidence types are DISTINCT; this PR adds the 4th (adjudication artifact) without overclaiming any of the others' coverage.

---

## Self-check — assumptions I most want the lightweight reviewer-adversarial pass to challenge

In rough order of brittleness (trimmed to 3, post-revision):

1. **The Q3 ratify-vs-amend framing.** I've now reframed Q3 as a live binary outcome (RATIFY vs AMEND) rather than a one-sided "AMEND-is-correct" framing. The strongest pushback: "you've turned an empirical column-pick decision into a politics-of-cleaning-layer decision; the cleaning-layer convention is settled and a single adjudication artifact MD section should not re-open it." My defense: RISK-26 is on disk in the methodology risk register and IS load-bearing for the thesis — leaving it un-reconciled with the cleaning-layer convention is exactly the kind of unrecorded methodology choice that adversarial examination at thesis defense will flag. The artifact MD makes the choice explicit in writing either way, which is the minimal defensibility bar.

2. **The Q2(b) Phase-03 RECOMMENDATION embedded in a Phase-02 artifact.** The reviewer may push back that even a non-binding recommendation about a Phase-03 anchor type pollutes the Phase-02 artifact scope. My defense: the recommendation is a one-paragraph note that documents the downstream coupling without committing Phase 03, satisfying both Q2(b)'s "must record" requirement and the F-phase03-creep falsifier's "no Phase 03 file" requirement. If reviewer disagrees, the simplest fix is to omit Q2(b) and let Phase 03 planning discover the coupling from Q2(a) + Q1 alone.

3. **The Random-vocabulary canonicalisation choice (`Rand`→`Random` under Q3.AMEND).** I'm defaulting to choice (a) (canonicalise to `Random`) with a verbose-spelling-dominates argument (1,110 vs 10) + cleaned-view-normalisation alignment. The lightweight reviewer-adversarial pass should challenge whether 10 rows is enough to canonicalise away vs whether the spelling difference encodes upstream-replay-version provenance. The Layer-2 T01 peek includes a temporal-stratification check to test whether the 2-spelling split is correlated with `details_timeUTC` cohort, but the answer to that check is not pre-known.

## Pipeline-section-status drift question

**`PIPELINE_SECTION_STATUS_02_01 = complete` is correct (NOT a drift defect).** Evidence (unchanged from original plan; reproduced for executor reference):

- `STEP_STATUS.yaml:1-12` header: "PIPELINE_SECTION_STATUS.yaml is derived from this file: Pipeline section is complete when ALL its steps are complete. Pipeline section is in_progress when ANY step is in_progress or complete. Pipeline section is not_started when NO step has started."
- `STEP_STATUS.yaml:196-200` shows the only `02_01_*` entry: `"02_01_01": name: "Feature-family registry skeleton" pipeline_section: "02_01" status: complete`. No `02_01_02` row.
- Per the header rule, with `02_01_01` the sole listed step in section `02_01` and it being `complete`, **ALL its steps are complete**, so `PIPELINE_SECTION_STATUS_02_01 = complete` is mechanically derived correctly.
- Pre-disclosed in PR #230's CHANGELOG `[3.65.0] Notes` and re-acknowledged in PR #232's `[3.67.0] Notes`. Outcome C is not warranted.

This adjudication PR continues the precedent: it does NOT add `02_01_02` to `STEP_STATUS` (since the materialization-execution PR is where the step's first non-vacuous artifact lands), so `02_01 = complete` remains correct after this PR too.

---

## Critique gate (Category A)

This is a Category A plan; per `.claude/rules/data-analysis-lineage.md` "Agent and model routing discipline" and per CLAUDE.md "Categories A/F require reviewer-adversarial pre-execution critique," **adversarial critique is required before any execution begins.**

This is a focused-revision turn over an already-APPROVED-WITH-NITS (zero blockers) original plan. A **lightweight `@reviewer-adversarial` pass** will run over the revised framing only (not a full re-gate). If it returns APPROVE / APPROVE-WITH-NITS with zero blockers, the parent materializes Layer-1 (2 files only: `planning/current_plan.md` + `planning/current_plan.critique.md`). The parent (orchestrator) is responsible for clearing any stale `planning/current_plan.md`, `planning/current_plan.critique.md`, and `planning/current_plan.critique_resolution.md` before `Write`. The Layer-1 PR itself does not author a critique-resolution artifact.

Do NOT produce the critique yourself in this turn — `@reviewer-adversarial` produces it as a separate artifact at `planning/current_plan.critique.md`. After the Layer-1 PR is open in draft, the parent records its PR number literally in the YAML frontmatter (`planning_pr`) and in the prose where `PR #233` appears (currently the active branch's draft PR per the recent commit history), updating any successor PR references if the active branch is re-targeted.
