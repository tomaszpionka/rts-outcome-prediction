---
task_id: "T02"
task_name: "Schema discovery — all 3 datasets (parameterized)"
agent: "executor"
model: "sonnet"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG02"
file_scope:
  - "sandbox/sc2/sc2egset/01_exploration/01_acquisition/"
  - "sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/"
  - "sandbox/aoe2/aoestats/01_exploration/01_acquisition/"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/"
  - "reports/research_log.md"
read_scope:
  - ".claude/scientific-invariants.md"
  - "docs/templates/research_log_entry_template.yaml"
  - "docs/templates/step_template.yaml"
  - "src/rts_predict/common/json_utils.py"
  - "src/rts_predict/common/parquet_utils.py"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
category: "A"
datasets:
  - id: sc2egset
    game: sc2
    notebook: sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_02_schema_discovery.py
    artifacts_dir: src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/
    research_log: src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
    roadmap: src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
    step_status: src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
    raw_dir: src/rts_predict/games/sc2/datasets/sc2egset/data/raw/
    prior_artifact: src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json
  - id: aoe2companion
    game: aoe2
    notebook: sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/01_01_02_schema_discovery.py
    artifacts_dir: src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/
    research_log: src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md
    roadmap: src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md
    step_status: src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml
    raw_dir: src/rts_predict/games/aoe2/datasets/aoe2companion/data/raw/
    prior_artifact: src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json
  - id: aoestats
    game: aoe2
    notebook: sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_02_schema_discovery.py
    artifacts_dir: src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/
    research_log: src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md
    roadmap: src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md
    step_status: src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml
    raw_dir: src/rts_predict/games/aoe2/datasets/aoestats/data/raw/
    prior_artifact: src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json
---

# Spec: Schema Discovery — All 3 Datasets (Parameterized)

## Objective

Create and execute schema discovery notebooks for all 3 datasets, produce
artifacts, write research log entries, update ROADMAPs with step
definitions, update STEP_STATUS, and write a CROSS entry.

## Instructions

Iterate the datasets table above. For each dataset, perform steps 1-8.
After all 3 complete, perform step 9 (CROSS entry).

### Per-dataset steps

**1. Add step definition to ROADMAP**

Read the dataset's ROADMAP file. Add the 01_01_02 step definition YAML
block after the existing 01_01_01 block. Read `docs/templates/step_template.yaml`
for the schema. The step definitions are provided in `planning/current_plan.md`
under "Step Definitions (for ROADMAPs)" — copy the appropriate block for
each dataset.

**2. Create the notebook**

Create a jupytext-paired `.py` notebook at the dataset's notebook path.
Structure:

- Cell 1: imports, config, paths (import from `rts_predict.common.json_utils`,
  `rts_predict.common.parquet_utils`, dataset config)
- Cell 2: load 01_01_01 artifact (the dataset's `prior_artifact` from the
  table above) to get file lists and directory structure
- Cell 3: sampling/census logic (deterministic file selection)
- Cell 4: schema discovery (per dataset method below)
- Cell 5: schema consistency check
- Cell 6: write JSON artifact to `{artifacts_dir}/01_01_02_schema_discovery.json`
- Cell 7: write Markdown artifact to `{artifacts_dir}/01_01_02_schema_discovery.md`

**3. Dataset-specific schema discovery method**

**sc2egset (JSON):**
- Select 1 file per directory (first alphabetically) for root schema
  via `discover_json_schema()` — 70 files total
- Select 3 files per directory for full keypath enumeration via
  `get_json_keypaths()` — 210 files total
- Compare root schemas across all 70 directories for consistency
- Report: root key catalog, keypath tree, observed types, consistency verdict
- No DuckDB type proposals

**aoe2companion (Parquet + CSV):**
- `matches/`: full census — `discover_parquet_schemas()` on all 2,073 files
  (metadata-only read, sub-second)
- `ratings/`: full census — `discover_csv_schema(sample_rows=50)` on all
  2,072 files (header + 50 rows each for type inference)
- Singletons: `discover_parquet_schema()` on `leaderboard.parquet` and
  `profile.parquet`
- Compare schemas within each subdirectory for consistency
- Report: column catalogs, Arrow/inferred types, consistency verdicts
- No DuckDB type proposals

**aoestats (Parquet + JSON):**
- `matches/`: full census — `discover_parquet_schemas()` on all 172 files
- `players/`: full census — `discover_parquet_schemas()` on all 171 files
- `overview/`: `discover_json_schema()` on `overview.json` (1 file)
- Cross-compare matches and players column names for structural overlap
  (raw string comparison of column names only — not semantic interpretation)
- Compare schemas within each subdirectory for consistency
- Report: column catalogs, Arrow types, consistency verdicts, column name
  overlap
- No DuckDB type proposals

**4. Artifact JSON structure**

```json
{
  "step": "01_01_02",
  "dataset": "<name>",
  "sampling": {
    "strategy": "<census | systematic_temporal_stratified>",
    "total_files_in_dataset": "<N>",
    "files_checked": "<N>",
    "method": "<description>"
  },
  "file_types": [
    {
      "type": "<parquet | csv | json>",
      "subdirectory": "<name>",
      "files_in_subdirectory": "<N>",
      "files_checked": "<N>",
      "schema": {
        "columns": [
          {
            "name": "<column_name>",
            "physical_type": "<arrow_type | python_type | inferred_type>",
            "nullable": "<bool>",
            "frequency": "<N (JSON only)>",
            "total_samples": "<N (JSON only)>",
            "sample_values": ["<up to 3, for type validation only>"]
          }
        ],
        "total_columns": "<N>",
        "nesting_depth": "<N (JSON only)>",
        "keypaths": ["<dotted paths (JSON only)>"]
      },
      "consistency": {
        "all_files_same_schema": "<bool>",
        "variant_columns": ["<only if inconsistent>"]
      }
    }
  ]
}
```

**5. Execute notebook**

```bash
source .venv/bin/activate && poetry run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 <notebook_path>.ipynb
```

**6. Sync jupytext**

```bash
source .venv/bin/activate && poetry run jupytext --sync <notebook_path>.ipynb
```

**7. Write research log entry**

Use `docs/templates/research_log_entry_template.yaml`. Rules:
- Set `step_scope: content`
- Report: column counts, type summary, nesting depth, consistency verdict
- Per Invariant #9: no row counts, no value distributions, no semantic
  interpretation beyond what column names literally say
- Sample values are included in artifacts for type-inference validation
  only — do NOT reference them semantically in the research log
- No DuckDB type proposals

**8. Update STEP_STATUS.yaml**

Mark 01_01_02 as complete in the dataset's STEP_STATUS.yaml.

### After all 3 datasets complete

**9. Write CROSS entry**

Write a CROSS entry in `reports/research_log.md`. Constrained to structural
observations only:
- File format per dataset (JSON / Parquet / CSV)
- Column count per file type
- Nesting depth per file type (0 for flat Parquet/CSV, N for JSON)
- Column name overlap across datasets as raw string comparison

Do NOT include:
- Semantic interpretation ("both contain match data")
- Ingestion design observations ("sc2egset needs JSON flattening")

## Verification

Per dataset:
- Artifacts exist: `01_01_02_schema_discovery.json` and `.md`
- `.ipynb` / `.py` pair synced
- Research log entry has `step_scope: content`
- Research log entry contains no row counts, value distributions, semantic
  interpretations, or DuckDB type proposals
- ROADMAP has 01_01_02 step definition
- STEP_STATUS.yaml updated

Global:
- CROSS entry in `reports/research_log.md` contains only structural
  observations (format, column count, nesting depth, name overlap)
- No DuckDB type proposals in any artifact

## Context

- Invariant #9 (research pipeline discipline): conclusions derive from
  own artifacts and prior step artifacts only. Sample values are for
  type validation, not semantic interpretation.
- Invariant #6 (reproducibility): all schema profiles produced by code
  in the notebooks, saved alongside reports.
- Invariant #7 (no magic numbers): Parquet and CSV use full census
  (zero cost). JSON sampling justified by I/O cost (3MB/file).
  CSV reads 50 header rows — sufficient for type variation detection
  without full content read.
- Step definitions for all 3 ROADMAPs are in the plan under
  "Step Definitions (for ROADMAPs)".
