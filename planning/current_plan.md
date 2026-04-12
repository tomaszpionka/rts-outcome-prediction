---
category: "A"
branch: "feat/phase01-schema-discovery"
date: "2026-04-12"
planner_model: "claude-opus-4-6"
dataset: "sc2egset, aoe2companion, aoestats"
phase: "01"
pipeline_section: "01_01"
invariants_touched:
  - 6
  - 7
  - 9
source_artifacts:
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
---

# Category A Plan: Phase 01 Step 01_01_02 — Schema Discovery

**Phase/Step:** Phase 01, Pipeline Section 01_01, Step 01_01_02
**Datasets:** sc2egset, aoe2companion, aoestats

## Scope

Create utility code for Parquet/CSV schema reading, then run schema
discovery notebooks for all 3 datasets. Each notebook samples files across
the temporal range, reads headers/schemas/metadata (without loading row
data), and produces artifacts documenting column names, types, nesting
structure, and cross-file consistency. Update ROADMAPs with step
definitions, write research log entries, and produce a CROSS entry.

## Problem Statement

Step 01_01_01 established what files exist on disk. Before any DuckDB
ingestion can be designed, we need to know what those files contain
structurally — column names, data types, nesting depth (JSON), and whether
the schema is consistent across files. This is the minimum information
needed to write DDL and ingestion scripts.

Per Invariant #9, this step reads structure, not content. It cannot report
row counts, value distributions, or semantic interpretations.

## Assumptions & Unknowns

- `discover_json_schema()` and `get_json_keypaths()` already exist in
  `rts_predict.common.json_utils` and are tested.
- `pyarrow.parquet.read_schema()` reads Parquet metadata without loading
  row data — zero-row operation, very fast.
- sc2egset JSON files are ~3MB each. Loading 210 files for keypath
  enumeration = ~630MB sequential reads. Feasible on 36GB M4 Max.
- SC2 replay format may have evolved across 2016-2024 (protocol versions).
  Schema discovery should detect this but not resolve it (resolution is
  01_04 cleaning).
- CSV type inference from 10 rows may misidentify types. This is a known
  limitation, documented in the report.

## Literature Context

The Manual 01_DATA_EXPLORATION, Section 1 explicitly lists "schema
information (column names, types, constraints, relationships)" as a
component of the source inventory. This step fulfills that requirement.

## Open Questions

1. Should `_download_manifest.json` files in aoe2companion and aoestats
   root directories get their own schema section? They are acquisition
   metadata, not game data. Decision: include them — Invariant #9 says
   we should not assume content without reading it.
2. If sc2egset shows era-dependent schema variation, should the notebook
   escalate to a full census for variant keys? Decision: yes, as a
   conditional extension documented in the notebook.

## Research Question

*"What is the internal structure of each file type in this dataset: what
fields/columns exist, what are their data types, how deep is the nesting
(JSON), and is this structure consistent across files?"*

## Scope Boundary (Invariant #9)

**01_01_02 CAN conclude** (observable from headers/schemas):
- Column names and physical data types (Arrow types for Parquet, Python
  types for JSON, inferred types for CSV)
- Nesting depth and nested key names (JSON)
- Whether all files of the same type share the same schema
- Nullability from schema metadata (Parquet) or key presence frequency (JSON)

**01_01_02 CANNOT conclude** (requires querying row content):
- Row counts
- Value distributions, histograms, summary statistics
- Missing value rates at the row level
- Semantic interpretation of columns (e.g., "this column is a player ID")
- Whether dates in filenames match dates in content
- Data quality or deduplication
- DuckDB type mappings (deferred to ingestion design step — depends on
  value range and cardinality knowledge not yet established)

**Note on sample values:** The `discover_json_schema()` function captures
up to 3 sample values per key for type-inference validation. These are
included in the artifact for auditability but the step's conclusions do
NOT reference them semantically. Seeing a value like "Serral" in a string
column does not allow this step to conclude "this column contains player
nicknames" — that is semantic interpretation belonging to 01_02 EDA.

## Sampling Strategy

**Census where cheap, stratified sample where expensive.**

`pyarrow.parquet.read_schema()` reads only footer metadata — sub-second
for thousands of files. CSV `pd.read_csv(nrows=50)` reads header + 50 rows
— fast enough for a full sweep. JSON parsing is expensive (~3MB per file).
Census is used for Parquet and CSV; stratified sampling for JSON only.

| Dataset | File type | Strategy | Count | Rationale |
|---------|-----------|----------|-------|-----------|
| sc2egset | JSON root schema | Stratified sample | 70 (1 per dir) | ~3MB/file, I/O cost justifies sampling |
| sc2egset | JSON keypaths | Stratified sample | 210 (3 per dir) | Full traversal, higher cost per file |
| aoe2companion | Parquet (matches) | Full census | 2,073 | Metadata-only read, sub-second |
| aoe2companion | CSV (ratings) | Full census, 50 rows | 2,072 | Header + 50 rows per file for type inference |
| aoe2companion | Parquet (singletons) | Census | 2 files | Only 1 file each |
| aoestats | Parquet (matches) | Full census | 172 | Metadata-only read |
| aoestats | Parquet (players) | Full census | 171 | Metadata-only read |
| aoestats | JSON (overview) | Census (1 file) | Only 1 file |

File selection is deterministic (first N alphabetically per directory, or
evenly spaced by date index) for reproducibility.

## Artifact Specification

Each dataset produces two artifacts:

**JSON:** `artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.json`
- Sampling metadata (strategy, counts, selection method)
- Per-file-type schema: column name, physical type (Arrow for Parquet,
  Python for JSON, inferred for CSV), nullable, frequency (JSON),
  sample values (up to 3, for type validation only)
- Nesting depth and keypath tree (JSON only)
- Schema consistency verdict per subdirectory
- No DuckDB type proposals (deferred to ingestion design)

**Markdown:** `artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md`
- Sampling methodology summary
- Per-file-type schema tables (column name | physical type | nullable)
- Schema consistency verdict
- Structural observations only (no content-level interpretation)

---

## Execution Steps

### T01 — Create Parquet/CSV schema utility code + tests

**Objective:** Add `discover_parquet_schema()` and `discover_csv_schema()`
functions with tests.

**Instructions:**
1. Create `src/rts_predict/common/parquet_utils.py` with:
   - `discover_parquet_schema(file_path) -> dict` — calls
     `pyarrow.parquet.read_schema()`, returns column names, Arrow types,
     nullable flags (no DuckDB type proposals — deferred to ingestion)
   - `discover_parquet_schemas(file_paths) -> dict` — runs on multiple
     files, compares schemas, returns consistency verdict + any variant
     columns
   - `discover_csv_schema(file_path, sample_rows=50) -> dict` — reads
     header + N rows, infers types via pandas, returns column names and
     inferred types (no DuckDB type proposals)
2. Write tests in `tests/rts_predict/common/test_parquet_utils.py`:
   - Test with a small synthetic Parquet file (created in conftest)
   - Test schema consistency check with matching and mismatching schemas
   - Test CSV schema inference with a small synthetic CSV
   - Test `sample_rows=50` parameter
4. Run `source .venv/bin/activate && poetry run pytest tests/rts_predict/common/test_parquet_utils.py -v`
5. Run `source .venv/bin/activate && poetry run ruff check src/rts_predict/common/parquet_utils.py`
6. Run `source .venv/bin/activate && poetry run mypy src/rts_predict/common/parquet_utils.py`

**Verification:**
- Tests pass
- Ruff clean
- Mypy clean
- `discover_parquet_schema()` returns column names + Arrow types + DuckDB proposals
- `discover_csv_schema()` returns column names + inferred types

**File scope:**
- `src/rts_predict/common/parquet_utils.py` (create)
- `tests/rts_predict/common/test_parquet_utils.py` (create)

**Read scope:**
- `src/rts_predict/common/json_utils.py` (for style reference)

---

### T02 — Run schema discovery for all 3 datasets + write research logs

**Objective:** Create and execute 3 schema discovery notebooks, produce
artifacts, write research log entries and CROSS entry. Update ROADMAPs
with step definitions.

This is a parameterized task — one set of instructions, iterated per
dataset.

**Datasets:**

```yaml
datasets:
  - id: sc2egset
    game: sc2
    notebook: sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_02_schema_discovery.py
    artifacts_dir: src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/
    research_log: src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
    roadmap: src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
    raw_dir: src/rts_predict/games/sc2/datasets/sc2egset/data/raw/
    prior_artifact: src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json
    file_types: "JSON (.SC2Replay.json)"
    method: |
      1. Read 01_01_01 artifact to get directory list
      2. Select 1 file per dir (first alphabetically) for root schema via discover_json_schema()
      3. Select 3 files per dir for keypaths via get_json_keypaths()
      4. Compare root schemas across all 70 dirs for consistency
      5. Report: root key catalog, keypath tree, types, consistency verdict (no DuckDB types)
    sample: "70 root (1/dir), 210 keypaths (3/dir) — stratified, JSON I/O cost justifies sampling"

  - id: aoe2companion
    game: aoe2
    notebook: sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/01_01_02_schema_discovery.py
    artifacts_dir: src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/
    research_log: src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md
    roadmap: src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md
    raw_dir: src/rts_predict/games/aoe2/datasets/aoe2companion/data/raw/
    prior_artifact: src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json
    file_types: "Parquet (matches, leaderboards, profiles) + CSV (ratings)"
    method: |
      1. Read 01_01_01 artifact to get file lists per subdir
      2. Parquet (matches): full census — discover_parquet_schemas() on all 2,073 files
      3. CSV (ratings): full census — discover_csv_schema(sample_rows=50) on all 2,072 files
      4. Singletons: read_schema() on leaderboard.parquet, profile.parquet
      5. Compare schemas within each subdir for consistency
      6. Report: column catalogs, Arrow/inferred types, consistency verdicts (no DuckDB types)
    sample: "Full census for Parquet (metadata-only) and CSV (header + 50 rows)"

  - id: aoestats
    game: aoe2
    notebook: sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_02_schema_discovery.py
    artifacts_dir: src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/
    research_log: src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md
    roadmap: src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md
    raw_dir: src/rts_predict/games/aoe2/datasets/aoestats/data/raw/
    prior_artifact: src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json
    file_types: "Parquet (matches, players) + JSON (overview)"
    method: |
      1. Read 01_01_01 artifact to get file lists per subdir
      2. Parquet: full census — discover_parquet_schemas() on all 172 matches + 171 players files
      3. JSON: discover_json_schema() on overview.json (census, 1 file)
      4. Cross-compare matches and players column names for structural overlap (raw string comparison)
      5. Compare schemas within each subdir for consistency
      6. Report: column catalogs, Arrow types, consistency verdicts, column name overlap (no DuckDB types)
    sample: "Full census for Parquet (metadata-only), census for JSON"
```

**Instructions (per dataset):**

1. Read the dataset's ROADMAP. Add the 01_01_02 step definition YAML block
   after the existing 01_01_01 block. Use the step definitions from this
   plan (see Step Definitions section below).
2. Create the notebook (jupytext-paired `.py`). Structure:
   - Cell 1: imports, config, paths
   - Cell 2: load 01_01_01 artifact to get file lists
   - Cell 3: sampling logic (deterministic file selection)
   - Cell 4: schema discovery (per dataset method above)
   - Cell 5: schema consistency check
   - Cell 6: write JSON artifact
   - Cell 7: write Markdown artifact
3. Run fresh-kernel execution:
   `source .venv/bin/activate && poetry run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 <notebook_path>.ipynb`
4. Sync jupytext:
   `source .venv/bin/activate && poetry run jupytext --sync <notebook_path>.ipynb`
5. Read produced artifacts (JSON + MD).
6. Write research log entry using `docs/templates/research_log_entry_template.yaml`:
   - Set `step_scope: content`
   - Report: column counts, type distributions, nesting depth, consistency
     verdict, sample values
   - Per Invariant #9: no row counts, no value distributions, no semantic
     interpretation beyond what column names literally say
7. After all 3 datasets complete: write CROSS entry in
   `reports/research_log.md` constrained to structural observations only:
   - File format per dataset (JSON / Parquet / CSV)
   - Column count per file type
   - Nesting depth per file type (0 for flat Parquet/CSV, N for JSON)
   - Column name overlap across datasets as raw string comparison
   - Do NOT include semantic interpretation ("both contain match data")
   - Do NOT include ingestion design ("sc2egset needs flattening")
8. Update each dataset's `STEP_STATUS.yaml` to mark 01_01_02 as complete.

**Verification (per dataset):**
- Artifacts exist: `01_01_02_schema_discovery.json` and `.md`
- `.ipynb` / `.py` pair synced
- Research log entry has `step_scope: content`
- Research log entry contains no row counts, value distributions, or
  semantic interpretations
- ROADMAP has 01_01_02 step definition
- STEP_STATUS.yaml updated

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_02_schema_discovery.ipynb`
- `sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_02_schema_discovery.py`
- `sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/01_01_02_schema_discovery.ipynb`
- `sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/01_01_02_schema_discovery.py`
- `sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_02_schema_discovery.ipynb`
- `sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_02_schema_discovery.py`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/`
- `reports/research_log.md`

**Read scope:**
- `.claude/scientific-invariants.md`
- `docs/templates/research_log_entry_template.yaml`
- `docs/templates/step_template.yaml`
- `src/rts_predict/common/json_utils.py`
- `src/rts_predict/common/parquet_utils.py` (from T01)
- Each dataset's 01_01_01 artifact (listed in datasets table above)

---

## Step Definitions (for ROADMAPs)

### sc2egset

```yaml
step_number: "01_01_02"
name: "Schema Discovery"
description: "Sample sc2egset JSON files across all 70 directories. Discover root-level keys, nested keypaths, data types, and schema consistency across eras."
phase: "01 — Data Exploration"
pipeline_section: "01_01 — Data Acquisition & Source Inventory"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 1"
dataset: "sc2egset"
question: "What is the internal structure of the SC2EGSet JSON files, and is this structure consistent across all 70 directories?"
method: "Select 1 file from each of the 70 _data/ subdirectories (first alphabetically) for root-level schema via discover_json_schema(). Select 3 files from each directory for full keypath enumeration via get_json_keypaths(). Compare schemas across directories to detect era-dependent variation. Report root-level key catalog, full keypath tree, observed types, and consistency verdict. No DuckDB type proposals (deferred to ingestion design)."
stratification: "By directory (all 70 represented; temporal range 2016-2024)."
predecessors:
  - "01_01_01"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_02_schema_discovery.py"
inputs:
  duckdb_tables: "none — reads raw JSON files directly"
  prior_artifacts:
    - "artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
  external_references:
    - ".claude/scientific-invariants.md"
    - "docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md, Section 1"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.json"
  report: "artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md"
reproducibility: "All schema profiles produced by discover_json_schema() and get_json_keypaths() from rts_predict.common.json_utils. File selection is deterministic (first N alphabetically per directory). Code and output in the paired notebook per Invariant #6."
scientific_invariants_applied:
  - number: "6"
    how_upheld: "Schema profiles produced by code in the notebook, saved alongside the report."
  - number: "7"
    how_upheld: "Sample size (1 per directory for root schema, 3 for keypaths) justified by temporal stratification in the report."
  - number: "9"
    how_upheld: "Conclusions limited to structural observations. No row counts, value distributions, or semantic interpretation."
gate:
  artifact_check: "artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.json and .md exist and are non-empty."
  continue_predicate: "Schema artifacts exist and report a consistency verdict for all 70 directories."
  halt_predicate: "More than 30% of sampled files fail to parse."
thesis_mapping:
  - "Chapter 4 — Data and Methodology > 4.1.1 SC2EGSet (StarCraft II)"
research_log_entry: "Required on completion."
```

### aoe2companion

```yaml
step_number: "01_01_02"
name: "Schema Discovery"
description: "Read Parquet metadata and CSV headers from aoe2companion raw files. Discover column schemas for matches, ratings, leaderboards, and profiles. Check schema consistency across the temporal range."
phase: "01 — Data Exploration"
pipeline_section: "01_01 — Data Acquisition & Source Inventory"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 1"
dataset: "aoe2companion"
question: "What columns exist in each file type, what are their data types, and is the schema consistent across the temporal range?"
method: "Full census: pyarrow.parquet.read_schema() on all 2,073 files in matches/ (metadata-only, sub-second). Full census: pd.read_csv(nrows=50) on all 2,072 files in ratings/ (header + 50 rows for type inference). Read schema from singleton leaderboard.parquet and profile.parquet. Compare schemas within each subdirectory for consistency. Report column catalogs, Arrow/inferred types, and consistency verdicts. No DuckDB type proposals."
stratification: "By subdirectory. Full census within each — no sampling needed for Parquet metadata or CSV headers."
predecessors:
  - "01_01_01"
notebook_path: "sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/01_01_02_schema_discovery.py"
inputs:
  duckdb_tables: "none — reads raw file metadata directly"
  prior_artifacts:
    - "artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
  external_references:
    - ".claude/scientific-invariants.md"
    - "docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md, Section 1"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.json"
  report: "artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md"
reproducibility: "Parquet schemas via pyarrow.parquet.read_schema() (full census on all files). CSV schemas via pd.read_csv(nrows=50) (full census, 50 rows per file for type inference — sufficient to detect type variation without full content read). Code and output in the paired notebook per Invariant #6."
scientific_invariants_applied:
  - number: "6"
    how_upheld: "Schema profiles produced by code in the notebook, saved alongside the report."
  - number: "7"
    how_upheld: "Full census for Parquet (metadata-only, zero cost) and CSV (header + 50 rows). Census eliminates sample-size justification requirement."
  - number: "9"
    how_upheld: "Conclusions limited to column-level structural observations. No row counts or value distributions. No DuckDB type proposals."
gate:
  artifact_check: "artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.json and .md exist and are non-empty."
  continue_predicate: "Schema artifacts exist and report a consistency verdict for all subdirectories."
  halt_predicate: "Any Parquet file fails to open."
thesis_mapping:
  - "Chapter 4 — Data and Methodology > 4.1.2 AoE2 Match Data"
research_log_entry: "Required on completion."
```

### aoestats

```yaml
step_number: "01_01_02"
name: "Schema Discovery"
description: "Read Parquet metadata from aoestats matches and players files. Read overview.json structure. Check schema consistency across the temporal range and compare matches/players schemas for structural overlap."
phase: "01 — Data Exploration"
pipeline_section: "01_01 — Data Acquisition & Source Inventory"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 1"
dataset: "aoestats"
question: "What columns exist in each file type, what are their data types, is the schema consistent across the temporal range, and do matches and players share structurally overlapping columns?"
method: "Full census: pyarrow.parquet.read_schema() on all 172 matches + 171 players files (metadata-only). discover_json_schema() on overview.json (1 file). Compare schemas within each subdirectory for consistency. Cross-compare matches and players column names for structural overlap (raw string comparison). Report column catalogs, Arrow types, consistency verdicts, and column name overlap. No DuckDB type proposals."
stratification: "By subdirectory. Full census within each."
predecessors:
  - "01_01_01"
notebook_path: "sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_02_schema_discovery.py"
inputs:
  duckdb_tables: "none — reads raw file metadata directly"
  prior_artifacts:
    - "artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
  external_references:
    - ".claude/scientific-invariants.md"
    - "docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md, Section 1"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.json"
  report: "artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md"
reproducibility: "Parquet schemas via pyarrow.parquet.read_schema() (full census on all files). JSON schema via discover_json_schema() (census, 1 file). Code and output in the paired notebook per Invariant #6."
scientific_invariants_applied:
  - number: "6"
    how_upheld: "Schema profiles produced by code in the notebook, saved alongside the report."
  - number: "7"
    how_upheld: "Full census for Parquet (metadata-only, zero cost) and JSON (1 file). Census eliminates sample-size justification requirement."
  - number: "9"
    how_upheld: "Conclusions limited to column-level structural observations. Cross-subdirectory comparison is structural (column name overlap as raw string comparison), not content-level. No DuckDB type proposals."
gate:
  artifact_check: "artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.json and .md exist and are non-empty."
  continue_predicate: "Schema artifacts exist and report a consistency verdict for all subdirectories."
  halt_predicate: "Any Parquet file fails to open."
thesis_mapping:
  - "Chapter 4 — Data and Methodology > 4.1.2 AoE2 Match Data"
research_log_entry: "Required on completion."
```

---

## File Manifest

| File | Action | Task |
|------|--------|------|
| `src/rts_predict/common/parquet_utils.py` | Create | T01 |
| `tests/rts_predict/common/test_parquet_utils.py` | Create | T01 |
| `sandbox/.../sc2egset/.../01_01_02_schema_discovery.{ipynb,py}` | Create + execute | T02 |
| `sandbox/.../aoe2companion/.../01_01_02_schema_discovery.{ipynb,py}` | Create + execute | T02 |
| `sandbox/.../aoestats/.../01_01_02_schema_discovery.{ipynb,py}` | Create + execute | T02 |
| `src/.../sc2egset/reports/artifacts/.../01_01_02_schema_discovery.{json,md}` | Generate | T02 |
| `src/.../aoe2companion/reports/artifacts/.../01_01_02_schema_discovery.{json,md}` | Generate | T02 |
| `src/.../aoestats/reports/artifacts/.../01_01_02_schema_discovery.{json,md}` | Generate | T02 |
| `src/.../sc2egset/reports/ROADMAP.md` | Add step definition | T02 |
| `src/.../aoe2companion/reports/ROADMAP.md` | Add step definition | T02 |
| `src/.../aoestats/reports/ROADMAP.md` | Add step definition | T02 |
| `src/.../sc2egset/reports/research_log.md` | Add entry | T02 |
| `src/.../aoe2companion/reports/research_log.md` | Add entry | T02 |
| `src/.../aoestats/reports/research_log.md` | Add entry | T02 |
| `src/.../sc2egset/reports/STEP_STATUS.yaml` | Mark 01_01_02 complete | T02 |
| `src/.../aoe2companion/reports/STEP_STATUS.yaml` | Mark 01_01_02 complete | T02 |
| `src/.../aoestats/reports/STEP_STATUS.yaml` | Mark 01_01_02 complete | T02 |
| `reports/research_log.md` | Add CROSS entry | T02 |

## Gate Condition

- `parquet_utils.py` exists with `discover_parquet_schema()` and
  `discover_csv_schema()` functions
- Tests pass: `pytest tests/rts_predict/common/test_parquet_utils.py -v`
- Ruff and mypy clean on `parquet_utils.py`
- 6 artifact files exist (JSON + MD per dataset) with current timestamps
- 3 notebooks executed fresh-kernel without error
- `.ipynb` / `.py` pairs synced for all 3 notebooks
- 3 per-dataset research log entries have `step_scope: content`
- 3 per-dataset research log entries contain no row counts, value
  distributions, or semantic interpretations
- 3 ROADMAPs have 01_01_02 step definition YAML blocks
- 3 STEP_STATUS.yaml files show 01_01_02 as complete
- Root CROSS log has factual 01_01_02 summary
- Full test suite passes: `pytest tests/ -v --cov`

## Design Decisions

1. **2 consolidated specs, not 8.** T01 (utility code) and T02 (all 3
   notebooks + docs) — applying the spec consolidation rule. T02 uses a
   parameterized dataset table. T02 writes ~22 files, exceeding the ~15
   guideline. Accepted: the parameterized table keeps instructions
   unified, and splitting notebooks from docs would force a second
   executor to re-read all artifacts. The token savings outweigh the
   tracking complexity.

2. **No intermediate review gate.** Final `reviewer-adversarial` only,
   per the new DAG token economy policy.

3. **Census where cheap, stratified where expensive.** Parquet metadata
   reads and CSV header reads are sub-second — full census eliminates
   sampling defensibility concerns at zero cost. JSON parsing is ~3MB
   per file — stratified sampling justified by I/O cost.

4. **sc2egset samples 70+210 files.** Higher than AoE2 because the JSON
   format has no embedded schema metadata — we must read file content.
   The 70 directories serve as natural strata.

5. **No DuckDB type proposals.** Deferred to ingestion design step.
   DuckDB type choice depends on value range and cardinality — content-
   level knowledge this step does not have.

6. **Step definitions go in ROADMAPs during T02.** Not a separate task —
   the executor creating the notebook also has the context to write the
   step definition.

7. **Sample values included for auditability, not interpretation.** The
   `discover_json_schema()` function captures up to 3 sample values per
   key. These support type-inference validation. The step's conclusions
   do not reference them semantically.

---

## Suggested Execution Graph

```yaml
dag_id: "dag_schema_discovery"
plan_ref: "planning/current_plan.md"
category: "A"
branch: "feat/phase01-schema-discovery"
base_ref: "master"
default_isolation: "shared_branch"
phase_ref: "01"
pipeline_section_ref: "01_01"
step_refs:
  - "01_01_02"

jobs:
  - job_id: "J01"
    name: "Schema discovery — all datasets"
    task_groups:
      - group_id: "TG01"
        name: "Utility code"
        depends_on: []
        tasks:
          - task_id: "T01"
            name: "Create parquet_utils + tests"
            spec_file: "planning/specs/spec_01_parquet_utils.md"
            agent: "executor"
            model: "sonnet"
            parallel_safe: false
            file_scope:
              - "src/rts_predict/common/parquet_utils.py"
              - "tests/rts_predict/common/test_parquet_utils.py"
            read_scope:
              - "src/rts_predict/common/json_utils.py"
            depends_on: []

      - group_id: "TG02"
        name: "Notebooks + artifacts + docs (all 3 datasets)"
        depends_on: ["TG01"]
        tasks:
          - task_id: "T02"
            name: "Schema discovery — all 3 datasets (parameterized)"
            spec_file: "planning/specs/spec_02_schema_discovery.md"
            agent: "executor"
            model: "sonnet"
            parallel_safe: false
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
            depends_on: []

final_review:
  agent: "reviewer-adversarial"
  scope: "all"
  base_ref: "master"
  on_blocker: "halt"

failure_policy:
  on_failure: "halt"
```

## Dependency Graph

```
TG01: T01 (parquet_utils + tests)
  |
TG02: T02 (3 notebooks + artifacts + research logs + ROADMAPs + CROSS)
```

2 specs, 2 dispatches. The DAG applies all token economy improvements:
no intermediate review gates, model hints, consolidated parameterized spec.
