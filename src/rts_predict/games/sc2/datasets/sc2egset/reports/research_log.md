# Research Log — SC2 / sc2egset

Thesis: "A comparative analysis of methods for predicting game results
in real-time strategy games, based on the examples of StarCraft II and
Age of Empires II."

SC2 / sc2egset findings. Reverse chronological.

---

## 2026-04-13 — [Phase 01 / Step 01_02_01] DuckDB ingestion investigation for sc2egset

**Category:** A (science)
**Dataset:** sc2egset
**Step scope:** query
**Artifacts produced:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_eda/01_02_01_duckdb_ingestion.json`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_eda/01_02_01_duckdb_ingestion.md`

### What

Tested DuckDB `read_json_auto` on 7 sample .SC2Replay.json files spanning the per-directory average file-size distribution (2.1 MB to 143.1 MB). Measured event array storage requirements across all 7 samples. Tested batch ingestion on one full tournament directory (64 files). Performed a full census of all 70 map_foreign_to_english_mapping.json files. Produced a design artifact with proposed table split strategy and recommended DDL for future ingestion.

### Why

Step 01_02_01 assesses DuckDB ingestion feasibility before committing to a full 22,390-file load. Per Invariant #6, all measurements are reproducible. Per Invariant #9, conclusions are limited to ingestion behavior (types, storage, parse success) -- no semantic analysis.

### How (reproducibility)

```python
from rts_predict.games.sc2.datasets.sc2egset.pre_ingestion import (
    select_sample_files, test_read_json_auto_single,
    measure_event_arrays, test_batch_ingestion,
    census_mapping_files, test_mapping_read_json_auto,
)
# Sample selection: 1 from smallest-avg dir, 1 from largest-avg dir,
# largest individual file, 3 from middle dirs
samples = select_sample_files(inventory, REPLAYS_SOURCE_DIR)
# read_json_auto per file
results = [test_read_json_auto_single(con, s) for s in samples]
# Event arrays
ea = [measure_event_arrays(s) for s in samples]
# Batch test on 2018_Cheeseadelphia_8 (64 files)
batch = test_batch_ingestion(con, batch_dir)
# Mapping census: all 70 files
census = census_mapping_files(REPLAYS_SOURCE_DIR)
```

Full derivation: `sandbox/sc2/sc2egset/01_exploration/01_eda/01_02_01_duckdb_ingestion.ipynb`

### Findings

- read_json_auto succeeds on all 7 sample files (100% parse success)
- All 11 root keys become columns; column count = 11 per file
- ToonPlayerDescMap: single-file parse creates STRUCT with per-file player-ID keys (non-unionable). With union_by_name=true (batch), correctly promoted to MAP(VARCHAR, STRUCT(...))
- Event array storage estimates (mean across 7 files, extrapolated to 22,390):
  - gameEvents: 326.8 GB
  - trackerEvents: 40.7 GB
  - messageEvents: 0.1 GB
  - Total: 367.6 GB
- Batch ingestion: 64 files in 1.66 seconds, 24 GB memory limit not exceeded
- Mapping file census: 70 files found, all identical (dict with 1,488 keys, foreign map name -> English name), combined 4.1 MB
- DuckDB parses mapping files as MAP(VARCHAR, VARCHAR)

### Decisions taken

- Proposed split-table strategy: separate metadata and event tables to avoid 370 GB single-table. Event array ingestion deferred.
- Mapping files: since all 70 are identical, a single file suffices for the lookup table.

### Decisions deferred

- Full 22,390-file ingestion: deferred pending decision on whether event arrays are needed for the prediction task.
- Whether to normalize overview.json list-valued columns deferred to EDA.

### Thesis mapping

- Chapter 4 -- Data and Methodology > 4.1.1 SC2EGSet: DuckDB ingestion strategy, JSON complexity, storage estimates.

### Open questions / follow-ups

- The 367.6 GB event array estimate is based on JSON byte size; DuckDB columnar compression may reduce this substantially. Actual compressed size unknown without test ingestion.
- ToonPlayerDescMap MAP(VARCHAR, STRUCT) type works with union_by_name=true but may have performance implications at 22,390 rows -- untested at scale.

---

## 2026-04-12 — [Phase 01 / Step 01_01_02] Schema discovery of sc2egset JSON files

**Category:** A (science)
**Dataset:** sc2egset
**Step scope:** content
**Artifacts produced:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.json`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md`

### What

Selected 1 file per `_data/` directory (first alphabetically) for root-level schema profiling via `discover_json_schema()` — 70 files total across all 70 directories. Selected 3 files per directory for full keypath enumeration via `get_json_keypaths()` — 210 files total. Compared root-level key sets across all 70 directories for schema consistency. Results written to JSON and Markdown artifacts.

### Why

Step 01_01_02 establishes the structural profile of the raw JSON files before any DuckDB ingestion can be designed. Per Invariant #9, this step is limited to structure (column names, types, nesting depth, consistency) — not row counts, distributions, or semantic interpretation. Sampling strategy is justified by I/O cost: each file is ~3MB; census of 22,390 files would require ~65GB of sequential reads and is not warranted at this stage.

### How (reproducibility)

```python
from rts_predict.common.json_utils import discover_json_schema, get_json_keypaths

# Root schema: 1 file per directory (first alphabetically)
root_schema_files = [sorted(data_dir.iterdir())[0] for data_dir in all_data_dirs]
key_profiles = discover_json_schema(root_schema_files, max_sample_values=3)

# Keypath enumeration: 3 files per directory (first 3 alphabetically)
keypath_files = [f for data_dir in all_data_dirs for f in sorted(data_dir.iterdir())[:3]]
all_keypaths: set[str] = set()
for fp in keypath_files:
    all_keypaths.update(get_json_keypaths(fp))

# Consistency check: compare key sets across all 70 directories
per_dir_key_sets = {dir_name: set(json.load(open(fp)).keys()) for dir_name, fp in ...}
variant_dirs = [d for d, ks in per_dir_key_sets.items() if ks != reference_keys]
```

Full derivation: `sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_02_schema_discovery.ipynb`

### Findings

- Root-level key count: 11 keys
- Root-level key names: `ToonPlayerDescMap`, `details`, `gameEvents`, `gameEventsErr`, `header`, `initData`, `messageEvents`, `messageEventsErr`, `metadata`, `trackerEvents`, `trackerEvtsErr`
- All 11 root-level keys are present in all 70 sampled files (frequency 70/70): 0 nullable root keys
- Root-level types: all 11 keys are either `dict`, `list`, or `bool`
- Maximum nesting depth: 5 levels
- Unique keypaths discovered: 7,350 (from 210 files across all 70 directories)
- Schema consistency across all 70 directories: True — all 70 directories share identical root-level key sets
- Files sampled for root schema: 70 (1 per directory)
- Files sampled for keypaths: 210 (3 per directory)
- Parse errors: 0

### Decisions taken

- None — observation only.

### Decisions deferred

- DuckDB type proposals for each JSON key deferred to ingestion design step (requires value range and cardinality knowledge not yet established).
- Whether era-dependent variation exists at deeper nesting levels (not detectable from root-key consistency check alone) deferred to Step 01_03 (systematic profiling).
- The 7,350 unique keypaths indicate substantial nesting; which keypaths are relevant for the prediction task requires content-level profiling (01_02/01_03).

### Thesis mapping

- Chapter 4 — Data and Methodology > 4.1.1 SC2EGSet (StarCraft II): JSON file structure, nesting depth, and schema consistency.

### Open questions / follow-ups

- The 5-level nesting depth and 7,350 keypaths suggest a complex schema. Whether all keypaths are populated across all files (vs. sparse optional fields) cannot be determined without querying row content (Step 01_03).
- The `gameEventsErr`, `messageEventsErr`, and `trackerEvtsErr` boolean keys (keys with `Err` suffix) have type `bool`; their values cannot be established at this step.

---

## 2026-04-12 — [Phase 01 / Step 01_01_01] File inventory of sc2egset raw directory

**Category:** A (science)
**Dataset:** sc2egset
**Step scope:** filesystem
**Artifacts produced:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md`

### What

Ran `inventory_directory()` on the sc2egset `raw/` directory to count all files
and subdirectories at two levels: the top-level directories (level 1)
and each directory's `_data/` subdirectory (level 2). Filename patterns were
summarised across both levels using `summarize_filename_patterns()`. Results
were written to a JSON artifact and a Markdown report in the artifacts directory.

### Why

Phase 01, Step 01_01_01 requires establishing the authoritative file counts and
directory structure of the raw data before any content-level work. Per Invariant
#9, all downstream steps must reference this artifact for source file counts.
Per Invariant #6, the code that produced every count is traceable via the paired
notebook (`01_01_01_file_inventory.ipynb`).

### How (reproducibility)

```python
from rts_predict.common.inventory import inventory_directory
from rts_predict.common.filename_patterns import summarize_filename_patterns

# Level 1: top-level directories
meta_result = inventory_directory(RAW_DIR)

# Level 2: each directory's _data/ subdir
for sd in meta_result.subdirs:
    data_dir = RAW_DIR / sd.name / (sd.name + "_data")
    replay_inv = inventory_directory(data_dir)

# Filename patterns across both levels
patterns = summarize_filename_patterns(all_files)
```

Full code: `sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb`

### Findings

- Raw directory layout: `raw/DIR/DIR_data/*.SC2Replay.json` (two levels)
- 70 top-level directories under `raw/`
- 3 files at `raw/` root: `README.md`, `README.sc2egset.md`, `SC2EGSet_datasheet.pdf`
- 431 metadata files distributed across top-level directories (`.zip`, `.log`, `.json` patterns)
- Each top-level directory contains one `map_foreign_to_english_mapping.json` (70 total)
- 22,390 files with extension `.json` and pattern `{hash}.SC2Replay.json` inside `_data/` subdirectories
- Total size of `_data/` files: 214,060.62 MB (~209 GiB)
- Files per `_data/` subdirectory: min 30, max 1,296, median 260.5
- 0 top-level directories with a missing `_data/` subdirectory
- Filename-derived date range: directory names span `2016_*` through `2024_*`
- 8 `.DS_Store` files present in the tree
- Total files scanned across both levels: 22,821
- All `_data/` files carry the `.json` extension; no other extension observed in `_data/` subdirectories

### Decisions taken

- None — observation only.

### Decisions deferred

- Whether any of the 70 top-level directories should be excluded from analysis
  (e.g., due to size, date coverage, or file count): deferred to Step 01_04_xx
  (data cleaning / filtering decisions require content-level profiling first).
- The `.DS_Store` files (8) and root-level housekeeping files are noted but
  no action is needed until ingestion is designed (Phase 01 content steps).

### Thesis mapping

- Chapter 4 — Data and Methodology > 4.1.1 SC2EGSet (StarCraft II): source
  file counts, directory layout, and date range derived from directory names.

### Open questions / follow-ups

- The `{hash}.SC2Replay.json` filename pattern does not embed dates; dates are
  encoded only in top-level directory names, not individual filenames. Whether
  individual files carry internal timestamps must be established at Step 01_01_02
  (content/schema profiling).
- The per-directory file count range (30 to 1,296) is wide; whether top-level directories with fewer files (e.g., those with < 50) represent complete acquisitions or partial extractions cannot be determined from filenames alone.
- The `processed_failed.log` files present in every top-level directory indicate
  a processing step was run during dataset creation; the contents of these logs
  are unknown at this step and may surface exclusion-worthy files at Step 01_01_02.

---
