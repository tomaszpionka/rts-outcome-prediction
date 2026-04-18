---
category: A
date: 2026-04-18
branch: feat/01-04-02-duration-augmentation
phase: "01"
pipeline_section: "01_04"
step: "01_04_02"
step_addendum: "duration_augmentation"
datasets: [sc2egset, aoestats, aoe2companion]
game: mixed
title: "01_04_02 augmentation: duration_seconds + outlier flags across all 3 clean views"
manual_reference: "docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md §4"
invariants_touched: [I3, I6, I7, I8, I9]
predecessors: ["01_04_02 (all 3 datasets)", "01_04_03 (PR #154 — empirical source of 142/28/342 outlier counts)"]
plans_merged_from:
  - sc2egset planner (agent a2b10149974082e8b)
  - aoestats planner (agent ac64671d97763af4a)
  - aoe2companion planner (agent a670303270ebb13be, ad58c14b6d27691ae)
---

# 01_04_02 augmentation: duration_seconds + outlier flags

## Problem Statement

User directive post-PR #154: move duration derivation + outlier flagging **upstream** into the 01_04_02 CLEAN views. Centralizes duration provenance at cleaning stage so all downstream consumers (including future refactored `matches_history_minimal` pass-through) inherit `is_duration_suspicious` / `is_duration_negative` flags without re-deriving. Addresses the 56 aoestats outliers + 142 aoec outliers + 358 aoec clock-skew rows surfaced in 01_04_03.

## Scope

Extend all 3 datasets' clean views via `CREATE OR REPLACE VIEW` (or TABLE where DuckDB 1.5.1 forces it):

| dataset | input view | input cols | output cols | added cols |
|---|---|---|---|---|
| sc2egset | `matches_flat_clean` | 28 | 30 | `duration_seconds`, `is_duration_suspicious` |
| aoestats | `matches_1v1_clean` | 20 | 22 | `duration_seconds`, `is_duration_suspicious` |
| aoe2companion | `matches_1v1_clean` | 48 | 51 | `duration_seconds`, `is_duration_suspicious`, `is_duration_negative` |

All 3 add `duration_seconds` BIGINT (POST_GAME_HISTORICAL) + `is_duration_suspicious` BOOLEAN (`duration_seconds > 86400`). Only aoec adds `is_duration_negative` BOOLEAN (`duration_seconds < 0`) — sc2egset and aoestats native units cannot go negative.

## Literature Context

Cleaning-stage only:
- Manual `01_DATA_EXPLORATION_MANUAL.md` §4.2 (non-destructive cleaning) + §4.4 (post-cleaning validation)
- van Buuren (2018) + sklearn MissingIndicator precedent — flag-not-drop for informative failure modes
- Tukey (1977) EDA — 86,400s as sanity bound, not distributional cutpoint
- 01_04_02 precedent: `rating_was_null` BOOLEAN flag in aoec (DS-AOEC-04) — direct methodological template

Downstream-consumer context (not this step's methodology): Phase 02 rating-system backtesting will consume these flags for outlier filtering + match-quality weighting.

## Assumptions & Unknowns

**Shared across all 3 datasets:**
- **A1:** 86,400s (24h) threshold is cross-dataset canonical sanity bound (I7 provenance: 01_04_03 Gate +5b precedent; ~25× p99). I8 demands identical threshold across all 3 datasets for UNION-compatible downstream filtering.
- **A2:** POST_GAME_HISTORICAL token is canonical first-word of `notes` for `duration_seconds` + derived flags (machine-grep for Phase 02 feature extractor auto-exclusion).
- **A3:** STEP_STATUS 01_04_02 stays `complete`; audit trail lives in ROADMAP `addendum:` block + schema YAML `schema_version` line + research_log ADDENDUM entry. No status flip (matches 01_04_03 addendum precedent).
- **A4:** `CREATE OR REPLACE VIEW` is used where DuckDB 1.5.1 allows; aoec empirically verified VIEW works for this pattern (no self-reference to clean view, unlike 01_04_03 self-join which forced TABLE workaround).

**Per-dataset:**
- **A-sc2:** 22.4 SC2 "Faster" loops/sec constant — I7 via `details.gameSpeed` cardinality=1 (W02 census, sc2egset research_log.md:333). Source via aggregated `player_history_all` JOIN (sc2egset's `matches_flat_clean` excludes `header_elapsedGameLoops`; only `player_history_all` retains it). Expected 0 suspicious rows (01_04_03 max 6073s).
- **A-aoestats:** `matches_raw.duration` is BIGINT NANOSECONDS (Arrow duration[ns] → BIGINT per DuckDB 1.5.1); divisor 1,000,000,000 cites `pre_ingestion.py:271`. Expected 28 suspicious matches TRUE (= 28 × 2 = 56 player-rows in 01_04_03; aoestats is 1-row-per-match so here 28).
- **A-aoec:** `matches_raw.finished` nullable in schema but empirically 0.0% NULL in 1v1 scope (01_04_03 Gate +6). `EXTRACT(EPOCH FROM finished - started)` standard DuckDB. Expected 142 suspicious + 342 strict-negative (Q2 resolved: strict `<0`, not non-positive — 16 zero-duration rows documented as known state, handled in Phase 02).

## Execution Steps

### T01 — Register addendum in all 3 ROADMAPs (parallel in-session; no executor dispatch)

For each dataset, append a markdown addendum section to the `### Step 01_04_02` block in `reports/ROADMAP.md`:
- Note new cols + dtypes + derivation formula
- I7 provenance
- Reference PR for this work
- Link to new validation JSON path

STEP_STATUS 01_04_02 stays `complete`. PIPELINE_SECTION_STATUS 01_04 stays `complete`. PHASE_STATUS unchanged.

### T02 — Execute per-dataset notebooks (3 parallel executors)

Each dataset's executor:
1. Amend existing 01_04_02 execution notebook OR create new augmentation notebook (executor chooses per DuckDB compatibility — aoec may need new notebook due to 1.5.1 JOIN bug on the VIEW).
2. Run new `CREATE OR REPLACE VIEW` DDL.
3. Validate against gate conditions (see per-dataset gate tables below).
4. Regenerate schema YAML (add new col entries + `schema_version: "XX-col (ADDENDUM: duration added 2026-04-18)"` line + I3/I7 invariant extensions).
5. Regenerate validation JSON + MD artifacts with duration stats + outlier samples.
6. Prepend ADDENDUM entry to `reports/research_log.md`.

Parallel dispatch: 3 executors, one per dataset. Non-overlapping files.

### T03 — Post-execution integration (parent)

After all 3 executors return:
1. Verify I9 empty diff on all 9 upstream YAMLs
2. Verify cross-dataset column parity (identical names + dtypes for `duration_seconds` + `is_duration_suspicious`)
3. Commit feat + chore(release) 3.15.0
4. Push + PR

### T04 — Adversarial review (single round per user directive)

Post-execution reviewer-adversarial on PR diff. If APPROVE / APPROVE_WITH_WARNINGS, merge; if REQUIRE_REVISION, fix + re-review.

## File Manifest

**Per-dataset (× 3):**
- `sandbox/<game>/<dataset>/01_exploration/04_cleaning/01_04_02_<notebook>.py` + `.ipynb` (modify or create new — executor choice)
- `src/rts_predict/games/<game>/datasets/<dataset>/data/db/schemas/views/<clean_view>.yaml` (add N cols + `schema_version` + invariants extensions)
- `src/rts_predict/games/<game>/datasets/<dataset>/reports/artifacts/01_exploration/04_cleaning/<new_artifact>.json` + `.md` (new or extended)
- `src/rts_predict/games/<game>/datasets/<dataset>/reports/ROADMAP.md` (addendum section)
- `src/rts_predict/games/<game>/datasets/<dataset>/reports/research_log.md` (ADDENDUM entry at top)

**Shared:**
- `pyproject.toml` (version 3.14.0 → 3.15.0)
- `CHANGELOG.md` ([3.15.0] entry)
- `planning/current_plan.md` (this plan)

**NOT touched (I9):**
- All 3 datasets' `matches_raw.yaml`, `matches_long_raw.yaml`, `player_history_all.yaml`, `matches_history_minimal.yaml`
- STEP_STATUS.yaml (all datasets)
- PIPELINE_SECTION_STATUS.yaml (all datasets)
- PHASE_STATUS.yaml (all datasets)

## Gate Condition

Per-dataset shared gates (all HALTING):

1. DESCRIBE returns expected col count (sc2: 30; aoestats: 22; aoec: 51)
2. Last 2-3 cols match spec: `duration_seconds BIGINT`, `is_duration_suspicious BOOLEAN`, [aoec only] `is_duration_negative BOOLEAN`
3. Row count unchanged (sc2: 44,418; aoestats: 17,814,947; aoec: 61,062,392)
4. `COUNT(*) FILTER (WHERE duration_seconds IS NULL) ≤ 1%` (expected 0 for sc2+aoestats; 0 for aoec)
5. `MAX(duration_seconds) ≤ 1_000_000_000` (unit regression canary)
6. I5-analog symmetry: 2-row mirror for sc2+aoec (new cols identical between rows); aoestats 1-row-per-match (no symmetry check)
7. Schema YAML has `schema_version: "...ADDENDUM 2026-04-18..."` + new col entries + I3 invariant mentions POST_GAME_HISTORICAL token
8. `git diff --stat` on 9 upstream YAMLs empty (I9)
9. Validation JSON: `all_assertions_pass: true` + all new SQL verbatim in `sql_queries`

Per-dataset specific gates:

| dataset | suspicious count expected | negative count expected |
|---|---|---|
| sc2egset | 0 (HALTING) | N/A |
| aoestats | 28 (HALTING, ±1 tolerance for race) | N/A |
| aoe2companion | 142 (HALTING) | 342 (HALTING, strict `<0`) |

## Open Questions

All resolved:

- **Q1** STEP_STATUS strategy → (a) in-place revision, stay `complete` (all 3 planners recommended; matches 01_04_03 addendum precedent)
- **Q2** aoec `is_duration_negative` semantics → (a) strict `< 0` (expected 342); 16 zero-duration rows documented as known state for Phase 02
- **Q3** threshold consistency → (a) identical 86,400s across all 3 datasets (I8 cross-dataset comparability)
- **Q4** aoec row-set equivalence check → 6-col EXCEPT smoke test sufficient (48-col EXCEPT NULL-semantics risk)

## Cross-sibling column contract (I8)

All 3 datasets MUST emit:
- `duration_seconds` BIGINT, classified POST_GAME_HISTORICAL in `notes` first token
- `is_duration_suspicious` BOOLEAN, threshold 86_400s

Only aoec additionally emits:
- `is_duration_negative` BOOLEAN, threshold strict `< 0`

Phase 02 rating-system backtest will filter on these flags uniformly (for aoec); sc2+aoestats always-FALSE `is_duration_negative` would be redundant.
