---
category: A
branch: "feat/phase01-duckdb-ingestion"
date: "2026-04-13"
planner_model: "claude-opus-4-6"
dataset: null  # multi-dataset: sc2egset, aoe2companion, aoestats
phase: "01"
pipeline_section: "01_02 — Exploratory Data Analysis (Tukey-style)"
step_refs: ["01_02_02"]
invariants_touched: [6, 7, 9]
critique_required: true
---

# Plan: Step 01_02_02 — DuckDB Ingestion (All Datasets)

## Scope

Step 01_02_02 materialises raw data into persistent DuckDB tables across
all three datasets using strategies determined by 01_02_01. For SC2, also
extracts event arrays to Parquet so the ~200 GB raw JSON can be re-zipped.

## Problem Statement

Each dataset has completed 01_02_01 pre-ingestion investigation. The raw
data exists on disk but is not yet in a queryable database. SC2 has deeply
nested JSON with ~368 GB of event arrays requiring a split strategy. AoE2
datasets need targeted ingestion with known type traps. This step creates
the bronze-layer tables that all subsequent Phase 01 profiling reads from.

## Assumptions & Unknowns

**Assumptions:**
- 01_02_01 notebooks will confirm strategies below when re-executed. If
  findings diverge, the plan must be revisited.
- Existing AoE2 pre_ingestion modules are structurally sound.
- SC2 event Parquet extraction is feasible within available SSD space.

**Unknowns:**
- Exact SC2 metadata STRUCT sub-field types (resolves: 01_02_01 §8a)
- Whether aoestats profile_id DOUBLE→BIGINT is lossy (resolves: 01_02_01 §7a)
- SC2 mapping file variation across 70 tournaments (resolves: 01_02_01 §7)
- ToonPlayerDescMap field stability across eras (resolves: 01_02_01 §8c)

## Literature Context

No external literature applies. Governed by DuckDB 1.5.1 documentation
and project scientific invariants (#6, #7, #9).

## Prerequisites — 01_02_01 re-execution gate

**HARD GATE:** All three 01_02_01 notebooks must be re-executed with
recorded outputs before 01_02_02 can proceed. Re-execution is the user's
responsibility, not a task in this DAG.

---

## Per-Dataset Ingestion Strategy

### SC2EGSet — Three-stream extraction

**Stream 1 — Replay Scalars (`replays_meta`):** DuckDB table, one row per
replay (22,390 rows). Contains `details`, `header`, `initData`, `metadata`
as STRUCT columns, error booleans, and `ToonPlayerDescMap` stored as JSON
text blob (VARCHAR). `filename` for provenance. Event arrays EXCLUDED.

**Stream 2 — Players (`replay_players`):** DuckDB table normalised from
ToonPlayerDescMap. One row per (replay, player). `replay_id` derived from
`filename` column (same provenance column present in all tables). `toon_id`
(MAP key), plus all per-player fields. Temporal annotations in code comments:
- Pre-game: MMR, selectedRace, handicap, region, realm, highestLeague
- Post-game: result, APM, SQ, supplyCappedPercent
- Identity: nickname, playerID, userID, isInClan, clanTag, color_*, etc.

**Stream 3 — Events (Parquet):** Extract gameEvents, trackerEvents,
messageEvents to zstd-compressed Parquet partitioned by `evtTypeName`.
Each row includes `replay_id` and `loop` (game tick). NOT loaded into
DuckDB — preserved for potential Phase 02 use.
**Fallback:** If median storage estimate exceeds available SSD, extract
only trackerEvents. If even that is infeasible, defer entirely.

**Also:** `map_aliases` DuckDB table from all 70 tournament mapping files.
Files may vary across tournaments — ingest all with a `tournament` column
for provenance, then deduplicate or union as appropriate based on 01_02_01
census findings.

### AoE2Companion — Four tables

| Table | Source | Key notes |
|-------|--------|-----------|
| `matches_raw` | 2,073 daily Parquet | `binary_as_string=true`, `filename=true` |
| `ratings_raw` | 2,072 daily CSV | Explicit types (read_csv_auto fails at scale) |
| `leaderboards_raw` | Singleton Parquet | `binary_as_string=true` |
| `profiles_raw` | Singleton Parquet | `binary_as_string=true` |

### AoeStats — Three tables

| Table | Source | Key notes |
|-------|--------|-----------|
| `matches_raw` | 172 weekly Parquet | `union_by_name=true`, `filename=true` |
| `players_raw` | 171 weekly Parquet | `union_by_name=true`, `filename=true` |
| `overviews_raw` | Singleton JSON | `read_json_auto`, `filename=true` |

Pending: profile_id BIGINT cast (if lossless per 7a), duration as BIGINT ns.

---

## Execution Steps

### T01 — SC2EGSet ingestion module

Create `src/rts_predict/games/sc2/datasets/sc2egset/ingestion.py`:

- `load_replays_meta(con, raw_dir) -> int`
- `load_replay_players(con, raw_dir) -> int`
- `extract_events_to_parquet(raw_dir, output_dir) -> dict[str, int]`
- `load_map_aliases(con, raw_dir) -> int` — all 70 files with tournament provenance
- `load_all_raw_tables(con, raw_dir) -> dict[str, int]`

Agent: executor, model: opus
File scope: `src/rts_predict/games/sc2/datasets/sc2egset/ingestion.py`

### T02 — SC2EGSet ingestion tests

Create tests with synthetic JSON fixtures. Test table creation, column
presence, ToonPlayerDescMap VARCHAR type, replay_players normalisation,
Parquet event extraction, map_aliases with tournament column, idempotency.

Agent: executor, model: sonnet
Depends on: T01
File scope: `tests/rts_predict/games/sc2/datasets/sc2egset/test_ingestion.py`,
`tests/rts_predict/games/sc2/datasets/sc2egset/conftest.py`

### T03 — Ingestion notebooks (all 3 datasets)

Create `01_02_02_duckdb_ingestion.py` for each dataset:
- Import ingestion module, call loaders against persistent DuckDB
- Post-ingestion validation: DESCRIBE, row counts, NULL rates on key fields
- Write JSON + MD artifacts
- SC2: also call extract_events_to_parquet, report Parquet file sizes

Agent: executor, model: sonnet
File scope: `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_02_duckdb_ingestion.py`,
`sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_02_duckdb_ingestion.py`,
`sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_02_duckdb_ingestion.py`

### T04 — ROADMAP and status updates

Add Step 01_02_02 to each ROADMAP.md and STEP_STATUS.yaml (not_started).

Agent: executor, model: haiku
File scope: 3x ROADMAP.md, 3x STEP_STATUS.yaml

## Suggested Execution Graph

```yaml
dag_id: "dag_01_02_02_duckdb_ingestion"
plan_ref: "planning/current_plan.md"
category: "A"
branch: "feat/phase01-duckdb-ingestion"
base_ref: "master"

jobs:
  - job_id: "J01"
    task_groups:
      - group_id: "TG01"
        name: "SC2 ingestion module"
        tasks:
          - task_id: "T01"
            agent: "executor"
            model: "opus"
            spec_file: "planning/specs/spec_01_sc2_ingestion.md"
            parallel_safe: true

      - group_id: "TG02"
        name: "SC2 tests"
        depends_on: ["TG01"]
        tasks:
          - task_id: "T02"
            agent: "executor"
            model: "sonnet"
            spec_file: "planning/specs/spec_02_sc2_tests.md"
            parallel_safe: false

      - group_id: "TG03"
        name: "Notebooks and ROADMAP"
        depends_on: ["TG02"]
        tasks:
          - task_id: "T03"
            agent: "executor"
            model: "sonnet"
            spec_file: "planning/specs/spec_03_notebooks.md"
            parallel_safe: true
          - task_id: "T04"
            agent: "executor"
            model: "haiku"
            spec_file: "planning/specs/spec_04_roadmap_status.md"
            parallel_safe: true

final_review:
  agent: "reviewer-adversarial"
  scope: "all"
  base_ref: "master"
```

## File Manifest

| File | Action |
|------|--------|
| `src/rts_predict/games/sc2/datasets/sc2egset/ingestion.py` | Create |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_ingestion.py` | Create |
| `tests/rts_predict/games/sc2/datasets/sc2egset/conftest.py` | Update |
| `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_02_duckdb_ingestion.py` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_02_duckdb_ingestion.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_02_duckdb_ingestion.py` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | Update |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` | Update |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` | Update |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` | Update |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml` | Update |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml` | Update |

## Gate Condition

1. `pytest tests/ -v` passes, no failures
2. `ruff check src/ tests/` clean
3. `mypy src/rts_predict/` clean
4. SC2 `ingestion.py` exists with all 5 public functions
5. All three 01_02_02 notebooks exist as valid jupytext files
6. All three ROADMAP.md files contain Step 01_02_02
7. All three STEP_STATUS.yaml files list 01_02_02 as not_started

## Open Questions

- **Q1:** Does aoestats profile_id lose precision in DOUBLE→BIGINT cast?
  Resolves by 01_02_01 §7a. If lossy, keep DOUBLE.
- **Q2:** How do SC2 mapping files vary across tournaments? Resolves by
  01_02_01 §7. Ingestion loads all 70 with tournament provenance.
- **Q3:** Do ToonPlayerDescMap fields vary across eras (2016-2024)?
  Resolves by 01_02_01 §8c across multiple samples.

## Out of Scope

- Notebook execution against real data (user action)
- Schema evolution cleaning (Phase 01_04)
- Temporal field annotation enforcement (Phase 02)
- Deduplication (cleaning step)
- CLI integration
- Event analysis (Phase 02 decision)
- Legacy ingestion.py module reconciliation (separate chore)

## Thesis Mapping

- Chapter 4 — Data and Methodology > 4.1.1 SC2EGSet: three-stream ingestion,
  event Parquet extraction, ToonPlayerDescMap normalisation
- Chapter 4 — Data and Methodology > 4.1.2 AoE2 Match Data: binary column
  handling, CSV type strategy, variant column promotion
