---
category: A
branch: feat/sc2egset-02-01-02-roadmap-stub
base_ref: e96374fef43ce06d03098d9bea8296b4ff74a409
date: 2026-05-22
planner_model: claude-opus-4-7[1m]
dataset: sc2egset
phase: "02"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
invariants_touched: [3, 5, 6, 7, 8, 9, 10]
critique_required_before_execution: true
critique_reviewer: reviewer-adversarial (deferred to Layer-2 / scaffold turn per reviewer-deep gate)
gate_reviewer: reviewer-deep (Layer-1 draft-PR gate)
source_artifacts:
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.md
  - reports/specs/02_00_feature_input_contract.md
  - reports/specs/02_01_leakage_audit_protocol.md
  - reports/specs/02_02_feature_engineering_plan.md
  - reports/specs/02_03_temporal_feature_audit_protocol.md
  - .claude/rules/data-analysis-lineage.md
  - .claude/scientific-invariants.md
  - .claude/ml-protocol.md
  - docs/TAXONOMY.md
  - docs/PHASES.md
  - docs/templates/step_template.yaml
---

# Plan: SC2EGSet Step 02_01_02 — ROADMAP-only successor stub (first pre_game materialization design)

## Scope

This is a **ROADMAP-only** Category A planning unit. It describes a FUTURE
execution PR that inserts ONE new Step definition — `02_01_02` — into the
sc2egset ROADMAP under the existing Pipeline Section `02_01` (Pre-Game vs
In-Game Boundary), declaring the first feature-family **materialization** Step
as the successor to the now-closed catalog-only Step `02_01_01`. The future
execution PR delivers ONLY the ROADMAP stub plus the mechanical release tail
(INDEX archival, CHANGELOG, version bump) and the two planning files. It
materializes NO feature value, creates NO notebook, generates NO artifact, and
flips NO status YAML. This conforms to `.claude/rules/data-analysis-lineage.md`
§"Non-batching rule for empirical work" sequence — *step 1 (ROADMAP stub only)*.

This plan is delivered in two distinct layers:

- **LAYER 1 — the draft planning PR materialized THIS turn (after the
  reviewer-deep gate):** commits ONLY `planning/current_plan.md` and
  `planning/current_plan.critique.md`. No other file is touched.
- **LAYER 2 — the FUTURE ROADMAP-only execution PR this plan describes:** a
  separate, explicitly-approved turn edits EXACTLY these 6 files and nothing
  else: the sc2egset `ROADMAP.md`, `planning/INDEX.md`, `planning/current_plan.md`,
  `planning/current_plan.critique.md`, `CHANGELOG.md`, `pyproject.toml`.

## Problem Statement

PR #230 (merged 2026-05-22 at master `0c45c490`) closed Step `02_01_01` at the
**catalog-only registry layer** via a zero-materialization CROSS-02-01-v1.0.1
leakage-audit artifact pair. STEP_STATUS records `02_01_01: complete`,
PIPELINE_SECTION_STATUS records `02_01: complete`, PHASE_STATUS records Phase
`02: in_progress`. PR #231 (this branch's predecessor on the same release line)
reconciled the thesis notebook-regeneration manifest with that closure (OQ4).
No open follow-up now blocks designing the successor Step (PR #230 research_log:
"the gate for a future planner-science session to design `02_01_02` is now
open").

The closed `02_01_01` record DEFERS the actual feature-column materialization —
and the discharge of CROSS-02-03 dimensions D2, D3, D4-in_game, D5-in_game,
D6-full, D8 — to a future materialization Step it names verbatim as
"`02_01_02`" (registry MD commitment-path column; ROADMAP `continue_predicate`
clause 2). No `02_01_02` Step is defined anywhere in the ROADMAP today
(`02_01_02` appears only as forward-reference prose, never as a `step_number:`).
Per `docs/TAXONOMY.md` (Steps are sequential within a Pipeline Section) and
`docs/PHASES.md` (section `02_01` = manual §2, the pre-game/in-game boundary),
the correct next atomic unit is a ROADMAP stub for Step `02_01_02` under section
`02_01`. Per `.claude/rules/data-analysis-lineage.md`, that stub must be its own
PR — it must NOT be batched with the notebook scaffold, artifact, or status
updates that follow.

## Assumptions & unknowns

- **Assumption:** The PR #230 closure of `02_01_01` is byte-stable on master
  and this plan does not re-touch it. STEP_STATUS `02_01_01: complete` landed in
  PR #230; the registry/audit/§10 artifacts are CLOSED inputs to be cited, never
  modified.
- **Assumption:** Adding a ROADMAP Step stub that lacks a STEP_STATUS row does
  NOT change any derived status file. Section `02_01` stays `complete` after the
  ROADMAP-only PR (no STEP_STATUS row is added). The intended YAML re-derivation
  of `02_01 → in_progress` happens later, only when the SEPARATE execution of
  `02_01_02` lands a STEP_STATUS row — exactly as pre-disclosed in the PR #230
  CHANGELOG "status reopen disclosure". This is intended behaviour, not
  revisionism, and is out of scope for the ROADMAP-only PR.
- **Assumption:** The registry CSV's 5 `pre_game` rows
  (`status=allowed`, `cold_start_handling=G-CS-1`, `candidate_leakage_modes=none`,
  `allowed_cutoff_rule=snapshot_at_match_start`) are the correct minimal first
  materialization tranche. Justified in "Materialization scope" below from the
  CSV contents + Invariants #3/#8 + ml-protocol's three leakage failure modes.
- **Assumption (version):** Category A is feat-family. Per
  `.claude/rules/git-workflow.md` "minor for feat/refactor/docs", the bump is
  MINOR: `3.66.0 → 3.67.0`. (Although the deliverable is documentation-shaped, a
  ROADMAP Step definition is Phase-work category A on a `feat/` branch; minor is
  the conservative, policy-consistent choice and matches every prior
  `02_01_*` ROADMAP/closure PR on this line.)
- **Unknown (resolved by stub text, not by execution):** the numeric
  cutoff_loop value, window lengths, encoder choices, and any cold-start
  pseudocount for LATER tranches. These are deferred to the respective
  materialization Steps and are NOT pinned in this stub (Invariant #7). The
  ROADMAP stub declares them as gate categories only.
- **Unknown (resolved by reviewer-adversarial):** whether the stub's
  materialization-scope choice (5 pre_game families) survives adversarial
  methodology review before the FUTURE scaffold PR. The stub records the
  decision; it does not pre-empt the critique.

## Literature context

This unit is a ROADMAP stub (a planning/declaration artifact), not an empirical
experiment, so it introduces no new literature claim. The governing repo
conventions and methodology sources are: `.claude/scientific-invariants.md`
Invariants #3 (strict `match_time < T`; de Prado 2018 Ch.7 and Arlot & Celisse
2010 are the cited normalization-leakage precedents), #5 (symmetric player
treatment), #7 (no magic numbers — empirical or cited justification required),
#8 (shared cross-game pre-game feature categories; within-game comparison per
Demsar 2006 / Benavoli et al. 2017 / Garcia & Herrera 2008), #9 (research
pipeline discipline), #10 (relative-path provenance); `.claude/ml-protocol.md`
(the three leakage failure modes to test explicitly); the four LOCKED Phase-02
specs (CROSS-02-00-v3.0.1 input contract, CROSS-02-01-v1.0.1 leakage-audit
protocol, CROSS-02-02-v1.0.1 feature plan §6, CROSS-02-03-v1.0.1 temporal-audit
protocol §3/§4 D1–D15/§10); and `.claude/rules/data-analysis-lineage.md`
(non-batching sequence, feature-engineering discipline, temporal-leakage
discipline, SC2 tracker-event discipline). [OPINION] The minimal-first-tranche
choice is a design judgement grounded in the CSV's own per-row leakage-mode and
cold-start columns, not in an external benchmark.

## Execution Steps

> All tasks below are for the FUTURE execution PR, on branch
> `feat/sc2egset-02-01-02-roadmap-stub`, after this plan is approved on the draft
> PR and an explicit execution turn begins. The ROADMAP-only PR creates NO
> notebook, NO artifact, and flips NO status YAML.

### T01 — Insert the Step `02_01_02` YAML stub into the sc2egset ROADMAP

**Objective:** Add exactly one new `step_number: "02_01_02"` Step definition to
`ROADMAP.md`, immediately AFTER the closed `02_01_01` YAML block (after ROADMAP
line ~2097, before the `---` and the `## Phase 03 — Splitting & Baselines
(placeholder)` heading at ~line 2101), inside Pipeline Section `02_01`. The stub
declares the first feature-family **materialization** Step (5 pre_game families)
with full temporal/leakage/cold-start/SQL design, recorded as a declaration only
— NO feature value is materialized in this PR.

**Instructions:**
1. Locate the closing ` ``` ` of the `02_01_01` YAML block (ROADMAP ≈ line 2097)
   and the `---` separator beneath it (≈ line 2099). Insert a new `###` heading
   `### Step 02_01_02 — First pre_game feature-family materialization (sc2egset)`
   followed by a fenced ` ```yaml ` block, BEFORE the `---` that precedes
   `## Phase 03`.
2. Populate the YAML block with the EXACT stub content given in the "ROADMAP
   stub content" subsection below (matching the `02_01_01` field order and the
   `docs/templates/step_template.yaml` schema). Do not invent fields not in the
   template.
3. Do NOT edit the closed `02_01_01` block, its outputs, its gate, or any other
   ROADMAP text. Do NOT edit the Phase 03+ placeholders.
4. **(reviewer-deep N1)** In the new stub's `inputs.prior_artifacts`, cite the
   registry by its TRUE on-disk name `02_01_01_feature_family_registry.csv` (no
   `_sc2egset` suffix). Do NOT propagate the closed `02_01_01` block's stale
   `..._registry_sc2egset.csv` output path (which does not exist on disk). Do NOT
   fix that stale string inside the closed block — that would violate gate (a).

**Verification:**
- `grep -c 'step_number: "02_01_02"' src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` returns exactly 1.
- The new block contains the literal substring `NO feature value is materialized in this ROADMAP-stub PR`.
- The new block's `predecessors` field lists `02_01_01`.
- `source .venv/bin/activate && poetry run python -c "import yaml; [yaml.safe_load(b.split('```')[0]) for b in open('src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md').read().split('```yaml')[1:]]"` parses every YAML block without error.
- `git diff` for ROADMAP.md shows ONLY an insertion (no deletions, no edits to the `02_01_01` block).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.md`

---

### T02 — Archive PR #231 and set the new Active line in planning/INDEX.md

**Objective:** Move the current Active line (the PR #231 manifest-reconciliation
plan) into the Archive table as a new top row with its merge SHA, and set the
new Active line to this branch.

**Instructions:**
1. In `planning/INDEX.md`, move the existing `## Active plan` bullet
   (`docs/thesis-pass2-020101-manifest-closure-reconciliation … (PR #231)`)
   into the Archive table as a NEW top row, Category F, columns:
   `| docs/thesis-pass2-020101-manifest-closure-reconciliation | 2026-05-22 | F | <existing description, drop the "(PR #231, draft)" qualifier> | current_plan.md | #231 (merged 2026-05-22 at master e96374fe) |`.
   Use the literal merge date and SHA known at execution time; if PR #231 is not
   yet merged at execution, HALT (see Gate Condition). (Merged 2026-05-22 at
   `e96374fef43ce06d03098d9bea8296b4ff74a409`.)
2. Set the new `## Active plan` bullet to:
   `feat/sc2egset-02-01-02-roadmap-stub (2026-05-22) — Category A: ROADMAP-only stub defining Step 02_01_02 under Pipeline Section 02_01 (first pre_game feature-family materialization design; 5 allowed pre_game families; full temporal/leakage/cold-start/SQL design recorded as declaration only). NO feature value materialized, NO notebook, NO artifact, NO status YAML flip, NO Phase 03 work. Version bump 3.66.0 → 3.67.0 (PR #<this PR>, draft).`

**Verification:**
- `planning/INDEX.md` Archive table contains exactly one row whose Merged-PR cell starts `#231`.
- The sole `## Active plan` bullet names `feat/sc2egset-02-01-02-roadmap-stub`.
- No `(PR #231, draft)` qualifier remains anywhere in the file.

**File scope:**
- `planning/INDEX.md`

**Read scope:**
- (none — sibling task outputs not required)

---

### T03 — Release tail: pyproject version bump + CHANGELOG move

**Objective:** Bump the single version source and roll `[Unreleased]` into a new
versioned CHANGELOG block.

**Instructions:**
1. `pyproject.toml`: change `version = "3.66.0"` → `version = "3.67.0"` (minor;
   feat-family per git-workflow). Edit the version line ONLY.
2. `CHANGELOG.md`: move the (currently empty) `[Unreleased]` content under a new
   `## [3.67.0] — 2026-05-22 (PR #<this PR>: feat/sc2egset-02-01-02-roadmap-stub)`
   block with a `### Added` entry: "ROADMAP Step `02_01_02` stub (sc2egset,
   Pipeline Section 02_01) — first pre_game feature-family materialization
   design (5 allowed pre_game families); declaration only, NO materialization."
   and a `### Notes` entry restating: no notebook, no artifact, no status YAML
   flip, no Phase 03 work; section `02_01` remains `complete` (no STEP_STATUS row
   added by this PR; the YAML-derived re-derivation to `in_progress` occurs only
   when `02_01_02` executes — see reviewer-deep N2). Re-empty `[Unreleased]` with
   the four standard sub-headers. Preserve `[3.66.0]` and all older blocks.

**Verification:**
- `grep -c '^version = "3.67.0"' pyproject.toml` returns 1.
- `CHANGELOG.md` contains `## [3.67.0]` and an empty `[Unreleased]`; `[3.66.0]`
  is preserved verbatim.

**File scope:**
- `pyproject.toml`
- `CHANGELOG.md`

**Read scope:**
- (none)

---

### T04 — Final scope verification (HALT on any failure)

**Objective:** Prove the ROADMAP-only PR touched exactly the 6 permitted files
and nothing forbidden.

**Instructions:**
1. Confirm the final tracked diff against master is EXACTLY 6 files (2 planning
   files already on the branch from the Layer-1 materialization + the 4 execution
   files): `git diff --name-only master..HEAD | sort` returns:
   ```
   CHANGELOG.md
   planning/INDEX.md
   planning/current_plan.critique.md
   planning/current_plan.md
   pyproject.toml
   src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
   ```
2. Confirm NO status YAML, artifact, notebook, validator, test, spec, INVARIANTS,
   research_log, or thesis chapter is in the diff (grep the name-only list).

**Verification:**
- `git diff --name-only master..HEAD | wc -l` returns 6.
- `git diff --name-only master..HEAD | grep -E 'STEP_STATUS|PIPELINE_SECTION_STATUS|PHASE_STATUS|/artifacts/|/sandbox/|research_log|thesis/|INVARIANTS|validate_|/specs/|tests/'` returns nothing (exit 1).

**File scope:**
- (verification only — writes nothing)

**Read scope:**
- (none)

---

#### ROADMAP stub content (the EXACT YAML the future PR inserts in T01)

```yaml
step_number: "02_01_02"
name: "First pre_game feature-family materialization (sc2egset)"
description: >-
  First MATERIALIZATION step of Pipeline Section 02_01: materialize the 5
  pre_game feature families declared allowed in the Step 02_01_01 registry
  (focal_race_with_opponent_race_pair, map_type_encoded, patch_version_encoded,
  matchup_encoded, is_mmr_missing_flag) into a per-(focal_match_id, focal_player)
  feature table, then re-run the CROSS-02-01-v1.0.1 post-materialization
  leakage audit on the resulting non-empty features_audited set. Scope is the
  minimal lowest-risk tranche: every selected family has status=allowed,
  candidate_leakage_modes=none, cold_start_handling=G-CS-1, and
  allowed_cutoff_rule=snapshot_at_match_start in
  02_01_01_feature_family_registry.csv. The 6 history_enriched_pre_game families
  (cold-start gates G-CS-2..G-CS-5; rolling/h2h/rating leakage modes) and the 11
  in_game_snapshot families (tracker-event-bound, event.loop <= cutoff_loop
  caveats) are DEFERRED to successor Steps 02_01_03+ so that distinct
  leakage-falsifier regimes are not batched into one notebook (per
  .claude/rules/data-analysis-lineage.md "Feature-engineering discipline"). NO
  feature value is materialized in this ROADMAP-stub PR — this entry only
  declares the future step per .claude/rules/data-analysis-lineage.md
  "Non-batching rule for empirical work" sequence step 1; the notebook scaffold,
  one validation module, materialization, and the post-materialization audit are
  produced by SEPARATE FUTURE PRs (sequence steps 2-9).
phase: "02 -- Feature Engineering"
pipeline_section: "02_01 -- Pre-Game vs In-Game Boundary"
manual_reference: "02_FEATURE_ENGINEERING_MANUAL.md, Section 2"
dataset: "sc2egset"
question: >-
  Can the 5 allowed pre_game feature families from the Step 02_01_01 registry be
  materialized into a per-(focal_match_id, focal_player) feature table whose
  every column passes the CROSS-02-01-v1.0.1 post-materialization leakage audit
  with a NON-vacuous (non-empty features_audited) PASS verdict, under strict
  snapshot-at-match-start cutoff and symmetric focal/opponent construction?
method: >-
  For each of the 5 pre_game families, write a DuckDB projection over
  replay_players_raw / matches_flat keyed on (filename, player_id_worldwide)
  producing focal_* and opponent_* columns symmetrically (Invariant I5). The
  cutoff is snapshot_at_match_start: every column is read from the target game's
  own pre-game metadata (race, map, patch, matchup, MMR-missing flag) — these are
  known-at-match-start fields, NOT history aggregates and NOT tracker-derived, so
  no history_time < target_time window applies and no post-game token may appear.
  Then run the CROSS-02-01-v1.0.1 audit (02_01_leakage_audit_protocol.md section
  2.1 cutoff structural check, 2.2 POST-GAME token absence, 2.3 normalization
  fit-scope) over the materialized columns; emit a NON-vacuous
  leakage_audit_sc2egset.{json,md} with features_audited = the 5 (or expanded
  focal_*/opponent_*) materialized column names. All non-trivial logic lives in
  src/rts_predict/ and is imported by the notebook. THIS PR delivers only the
  ROADMAP stub (sequence step 1); materialization is a separate future PR.
stratification: >-
  Per family: dataset_tag = sc2egset; prediction_setting = pre_game. SC2 races
  (Prot / Terr / Zerg / Rand) are stratification axes for the race-pair and
  matchup families (RISK-26 Random-race semantics cited); map_type and
  patch_version partition the encoded categoricals. Corpus-wide single-number
  aggregates are not an acceptable sole output.
predecessors: "02_01_01"
notebook_path: >-
  sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.py
inputs:
  duckdb_tables:
    - "matches_flat"
    - "replay_players_raw"
    - "matches_history_minimal"
  schema_yamls:
    - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml"
  prior_artifacts:
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json"
  external_references:
    - "reports/specs/02_00_feature_input_contract.md (CROSS-02-00-v3.0.1)"
    - "reports/specs/02_01_leakage_audit_protocol.md (CROSS-02-01-v1.0.1) sections 2.1/2.2/2.3, 4 (materialization)"
    - "reports/specs/02_02_feature_engineering_plan.md (CROSS-02-02-v1.0.1) section 6, section 9 (G-CS-1)"
    - "reports/specs/02_03_temporal_feature_audit_protocol.md (CROSS-02-03-v1.0.1) section 4 D2/D3/D4/D5/D6/D8, section 10"
    - ".claude/rules/data-analysis-lineage.md"
    - ".claude/ml-protocol.md (three leakage failure modes)"
    - ".claude/scientific-invariants.md (I3, I5, I6, I7, I8, I9, I10)"
outputs:
  data_artifacts:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_matrix.parquet"
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json"
  report:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.md"
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.md"
reproducibility: >-
  Every materialized column traces to a registry row in
  02_01_01_feature_family_registry.csv; every projection SQL is embedded verbatim
  in the report MD alongside its result (Invariant I6). No magic numbers
  (Invariant I7): pre_game families carry cold_start_handling G-CS-1 (no
  pseudocount / threshold / smoothing constant); encoder vocabularies are
  fit on training folds only (no cross-fold or cross-dataset fit). Seed 42
  convention; deterministic export; relative-path provenance (Invariant I10).
scientific_invariants_applied:
  - number: "3"
    how_upheld: >-
      Every pre_game column is read at snapshot_at_match_start from the target
      game's own pre-game metadata; no history window and no tracker-derived
      value is used, so no information from game T or later enters. The
      post-materialization CROSS-02-01-v1.0.1 section 2.2 POST-GAME token absence
      check is run on the materialized set and must report 0 violations.
  - number: "5"
    how_upheld: >-
      The same projection produces focal_* and opponent_* columns symmetrically;
      no player slot is privileged. RISK-24 data-dependent slot-assignment
      falsifier is enumerated in the materialization notebook.
  - number: "6"
    how_upheld: >-
      Every reported count/distribution in the report MD is accompanied by its
      verbatim DuckDB SQL; no value is paraphrased.
  - number: "7"
    how_upheld: >-
      No magic numbers — pre_game families are G-CS-1 (no cold-start constant);
      any later numeric (cutoff_loop, window length) belongs to deferred
      in_game / history tranches, not this Step.
  - number: "8"
    how_upheld: >-
      The 5 pre_game families are exactly the shared cross-game pre-game
      categories (faction matchup, map) named in Invariant I8; encoders carry the
      dataset_tag = 'sc2egset' partition note and are not fit cross-dataset,
      preserving cross-game comparability for the AoE2 datasets.
  - number: "9"
    how_upheld: >-
      The Step reads only Phase 01 outputs and the CLOSED Step 02_01_01 catalog
      artifacts (all lower-numbered, on disk); it makes no source-stratified
      evaluation claim and builds no model.
  - number: "10"
    how_upheld: >-
      The materialized feature table and its provenance use the relative-path
      convention; no absolute path is written to any artifact.
gate:
  artifact_check: >-
    NOT APPLICABLE TO THIS ROADMAP-STUB PR. The artifact_check fires only after
    the future scaffold-and-materialization PR materializes the feature table +
    the NON-vacuous CROSS-02-01-v1.0.1 audit pair; at that point the predicate is
    "the planned Parquet feature matrix, the audit JSON, and both report MDs
    exist at the declared paths and are non-empty, and the audit JSON has
    features_audited != [] with verdict = PASS."
  continue_predicate: >-
    A future PR may begin Step 02_01_03 (the next 02_01 materialization step —
    history_enriched_pre_game tranche) only after this Step 02_01_02 has reached
    its artifact-check at a future PR, the CROSS-02-01-v1.0.1 post-materialization
    audit has returned a NON-vacuous PASS (future_leak_count = 0,
    post_game_token_violations = 0 over a non-empty features_audited), and a
    per-family CROSS-02-03-v1.0.1 section 10 verdict consistent with the
    materialized columns is recorded. The §10 design-time verdict audit (PR #229)
    is a distinct artifact and does NOT substitute for this post-materialization
    CROSS-02-01 audit (PR #230 evidence remains distinct from PR #229 evidence).
  halt_predicate: >-
    Halt before generating any feature artifact if any of the following hold
    (per .claude/rules/data-analysis-lineage.md "Stop conditions"):
      - any materialized pre_game column reads a value that is not knowable at
        snapshot_at_match_start (Invariant I3 violation);
      - the CROSS-02-01-v1.0.1 section 2.2 POST-GAME token absence check reports
        any violation on the materialized set;
      - any family outside the 5 allowed pre_game rows is materialized in this
        Step (scope creep into the deferred history / in_game tranches);
      - the focal_* / opponent_* construction is asymmetric (Invariant I5);
      - any encoder is fit on validation/test folds or cross-dataset
        (normalization leakage, Invariant I3);
      - the future notebook scaffold attempts to batch ROADMAP + notebook +
        artifact + next step in one execution (non-batching rule).
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > 4.5 Feature engineering plan (sc2egset pre_game materialization)"
research_log_entry: >-
  NOT REQUIRED FOR THIS ROADMAP-STUB PR per .claude/rules/data-analysis-lineage.md
  "Non-batching rule" sequence (step 1 — ROADMAP stub only — produces no
  research_log entry). Required on the future scaffold-and-materialization PR per
  the standard step-completion protocol; entry goes into
  src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md.
```

## Materialization scope (RECORDED in the stub; NOT executed)

**Decision: option (b) — a minimal first subset.** Step `02_01_02` is scoped to
materialize the **5 `pre_game` families ONLY**
(`focal_race_with_opponent_race_pair`, `map_type_encoded`,
`patch_version_encoded`, `matchup_encoded`, `is_mmr_missing_flag`), all with
`status=allowed`, `cold_start_handling=G-CS-1` (no cold-start dependency),
`temporal_anchor=details_timeUTC`, `allowed_cutoff_rule=snapshot_at_match_start`,
`candidate_leakage_modes=none` in the registry CSV.

Justification (from the registry CSV + invariants + ml-protocol):

- The 5 `pre_game` rows are the only families with `candidate_leakage_modes=none`
  AND `cold_start_handling=G-CS-1` AND `allowed_cutoff_rule=snapshot_at_match_start`
  — the cleanest possible first materialization (no rolling window, no history
  join, no tracker interpretation, no fixed-point/loop-scaling caveat).
- NOT option (a) "all allowed/with-caveat families": that pulls in the 6
  `history_enriched_pre_game` families (whose `candidate_leakage_modes` are
  exactly the three failure modes ml-protocol.md flags —
  `rolling_includes_target_game`, `h2h_includes_target_game`,
  `rating_uses_target_game_outcome` — and which need fold-aware cold-start gates
  G-CS-2..G-CS-5) and the 11 `in_game_snapshot` families (tracker-bound,
  `event.loop <= cutoff_loop`). Materializing all in one Step batches distinct
  leakage-falsifier regimes into one notebook — forbidden by the non-batching
  rule and "Feature-engineering discipline" — and bloats the CROSS-02-01
  `features_audited` set, undermining auditability. Invariant #3 and the three
  leakage failure modes are far easier to falsify on a `pre_game`-only tranche.
- NOT option (c) "scaffold only": `02_01_02` must be a *materialization* Step
  (it is the step the closed `02_01_01` record repeatedly defers materialization
  to). A pure scaffold re-creates the vacuous-audit situation of `02_01_01` and
  does not discharge the deferred dimensions. The point of the successor Step is
  to make `features_audited` NON-empty so the CROSS-02-01 audit becomes empirical
  rather than vacuous.
- Cross-game comparability (Invariant #8) favours starting pre_game: the shared
  cross-game pre-game categories (skill rating, win rate, activity, faction
  matchup, map) are exactly the `pre_game` / `history_enriched_pre_game`
  families. Starting with the SC2 `pre_game` tranche establishes the
  column-materialization + audit pattern that AoE2 datasets (no in-game state)
  can mirror, before SC2 diverges into its in-game-only families.

This decision is RECORDED in the stub's `description` / `method` /
`scientific_invariants_applied` fields. It is NOT executed. The
`history_enriched_pre_game` (6) and `in_game_snapshot` (11) tranches are deferred
to `02_01_03+` successor Steps; the stub records this so the section's remaining
materialization is sequenced, not abandoned.

## File Manifest

| File | Action |
|------|--------|
| `planning/current_plan.md` | Create (Layer 1, this turn) |
| `planning/current_plan.critique.md` | Create (Layer 1, this turn — reviewer-deep gate) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | Update (Layer 2 — insert Step 02_01_02 stub only) |
| `planning/INDEX.md` | Update (Layer 2 — archive PR #231, set new Active line) |
| `CHANGELOG.md` | Update (Layer 2 — `[Unreleased]` → `[3.67.0]`) |
| `pyproject.toml` | Update (Layer 2 — version line 3.66.0 → 3.67.0) |

## Gate Condition

The future ROADMAP-only execution PR is mergeable iff:
- (a) `ROADMAP.md` contains exactly one `step_number: "02_01_02"` block, inserted
  under Pipeline Section `02_01`, before the `## Phase 03` placeholder, with the
  exact stub content above; the closed `02_01_01` block is byte-unchanged.
- (b) Every YAML block in `ROADMAP.md` parses; the new block lists `predecessors:
  "02_01_01"` and contains the literal "NO feature value is materialized in this
  ROADMAP-stub PR".
- (c) The status triad (STEP_STATUS, PIPELINE_SECTION_STATUS, PHASE_STATUS) is
  byte-unchanged; section `02_01` remains `complete`; Phase `02` remains
  `in_progress`; Phase `03` remains `not_started`.
- (d) `planning/INDEX.md` archives PR #231 (with its real merge SHA, no "draft"
  qualifier) and sets the new Active line to this branch.
- (e) `pyproject.toml` = `3.67.0` with a matching `## [3.67.0]` CHANGELOG block
  and an empty `[Unreleased]`; `[3.66.0]` preserved.
- (f) `git diff --name-only master..HEAD | sort` is EXACTLY the 6 files in the
  File Manifest; NO artifact, notebook, validator, test, spec, INVARIANTS,
  research_log, or thesis chapter is in the diff.
- (g) The `@reviewer-adversarial` post-execution Cat A final gate returns APPROVE
  with zero blockers. PR #230's closure is preserved untouched throughout.

## Out of scope

- **All feature materialization.** No DuckDB VIEW/table, no Parquet, no encoder
  fit, no feature value is produced by the ROADMAP-only PR.
- **The `02_01_02` notebook scaffold + validation module.** That is the NEXT
  atomic unit (a separate scaffold PR, sequence step 2), requiring its own
  planner → reviewer-adversarial → executor cycle.
- **The post-materialization CROSS-02-01 audit re-run.** Designed (declared) in
  the stub; executed only by the future materialization PR.
- **Any status YAML flip.** No STEP_STATUS / PIPELINE_SECTION_STATUS /
  PHASE_STATUS edit. Section `02_01` intentionally stays `complete` (the
  YAML-derived re-derivation to `in_progress` happens later, on `02_01_02`
  execution, per the PR #230 status-reopen disclosure).
- **research_log.md (per-dataset OR root).** Step-1 ROADMAP stubs produce no
  research_log entry.
- **The history_enriched_pre_game (6) and in_game_snapshot (11) tranches.**
  Deferred to Steps `02_01_03+`; named in the stub so the section's remaining
  materialization is sequenced.
- **Editing the closed `02_01_01` ROADMAP block** (including its
  `02_01_01_feature_family_registry_sc2egset.csv` planned-output filename, which
  differs from the on-disk `02_01_01_feature_family_registry.csv`). That string
  lives inside a CLOSED Step's record; correcting it is a separate Category C/E
  hygiene unit, not part of this stub PR.
- **Phase 03+ work**; any model/split/baseline; any thesis prose; any
  bibliography/appendix; any edit to master; any merge.
- **Overclaiming leakage clearance.** The stub DESIGNS the first materialization
  and its audit; it does not assert leakage is empirically cleared. The PR #229
  §10 verdict-audit evidence and the PR #230 CROSS-02-01 leakage_audit evidence
  are kept DISTINCT in every reference.

## Open questions

- Does the materialization-scope choice (5 pre_game families as the minimal first
  tranche) survive adversarial methodology review? — resolves by:
  reviewer-adversarial critique on this plan, BEFORE the future scaffold PR
  (reviewer-deep deferred adversarial to the Layer-2 turn).
- Should `is_mmr_missing_flag` be materialized in the first tranche or deferred
  alongside the rating/history families (it is a pre_game flag but is adjacent to
  MMR semantics; MMR is ~83.95% missing per the Phase-01 missingness ledger)? —
  resolves by: reviewer-adversarial / user decision; the stub currently includes
  it because the registry classifies it `pre_game / allowed / G-CS-1 /
  candidate_leakage_modes=none`.
- Exact merge SHA + date of PR #231 for the INDEX archive row. — RESOLVED: PR
  #231 merged 2026-05-22 at `e96374fef43ce06d03098d9bea8296b4ff74a409`. (Executor
  re-confirms via `gh pr view 231` at execution time; HALT if not merged.)

---

**Critique gate (Category A):** A reviewer-deep gate on this plan returned
APPROVE-WITH-NITS with zero blockers and recommended DEFER-TO-LAYER-2 for
adversarial escalation (a recorded-but-not-executed scope decision in a stub does
not materially affect leakage semantics at the draft-planning stage; the future
scaffold/materialization PR gets its own Category A reviewer-adversarial gate
where the leakage computation actually lands). Therefore, before any Layer-2
EXECUTION turn begins, the parent session MUST dispatch `@reviewer-adversarial`
to produce the Category A pre-execution critique for the materialization-scope
decision (and refresh `planning/current_plan.critique.md` with it). The
reviewer-deep gate review is recorded in `planning/current_plan.critique.md` for
this Layer-1 draft PR.
