---
task_id: "T01"
task_name: "Create parquet_utils + tests"
agent: "executor"
model: "sonnet"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG01"
file_scope:
  - "src/rts_predict/common/parquet_utils.py"
  - "tests/rts_predict/common/test_parquet_utils.py"
read_scope:
  - "src/rts_predict/common/json_utils.py"
category: "A"
---

# Spec: Create parquet_utils + tests

## Objective

Create Parquet and CSV schema discovery utility functions with tests.
These will be used by the 01_01_02 notebooks to read schema metadata
from Parquet files and CSV headers across all 3 datasets.

## Instructions

1. Create `src/rts_predict/common/parquet_utils.py` with:

   - `discover_parquet_schema(file_path: Path) -> dict` — calls
     `pyarrow.parquet.read_schema()`, returns dict with:
     - `columns`: list of `{"name": str, "arrow_type": str, "nullable": bool}`
     - `total_columns`: int
     - No DuckDB type proposals (deferred to ingestion design)

   - `discover_parquet_schemas(file_paths: list[Path]) -> dict` — runs
     `discover_parquet_schema()` on each file, compares schemas, returns:
     - `schemas`: list of per-file schemas
     - `all_files_same_schema`: bool
     - `variant_columns`: list (only populated if schemas differ)
     - `files_checked`: int

   - `discover_csv_schema(file_path: Path, sample_rows: int = 50) -> dict`
     — reads header + N rows via `pd.read_csv(nrows=sample_rows)`, returns:
     - `columns`: list of `{"name": str, "inferred_type": str, "nullable": bool}`
     - `total_columns`: int
     - `sample_rows_read`: int
     - No DuckDB type proposals

2. Read `src/rts_predict/common/json_utils.py` for style reference
   (similar wrapper pattern around discovery functions).

3. Write tests in `tests/rts_predict/common/test_parquet_utils.py`:
   - Create small synthetic Parquet file in conftest/fixture (3-4 columns,
     a few rows, mixed types including nullable)
   - Test `discover_parquet_schema()` returns correct column names and
     Arrow types
   - Test `discover_parquet_schemas()` with matching schemas (same file
     twice) → `all_files_same_schema: True`
   - Test `discover_parquet_schemas()` with mismatching schemas (different
     synthetic files) → `all_files_same_schema: False`, `variant_columns`
     populated
   - Create small synthetic CSV in fixture
   - Test `discover_csv_schema()` returns correct column names and
     inferred types
   - Test `sample_rows=50` parameter is respected

4. Run: `source .venv/bin/activate && poetry run pytest tests/rts_predict/common/test_parquet_utils.py -v`
5. Run: `source .venv/bin/activate && poetry run ruff check src/rts_predict/common/parquet_utils.py`
6. Run: `source .venv/bin/activate && poetry run mypy src/rts_predict/common/parquet_utils.py`

## Verification

- Tests pass
- Ruff clean
- Mypy clean
- `discover_parquet_schema()` returns column names + Arrow types (no DuckDB)
- `discover_parquet_schemas()` handles both matching and mismatching cases
- `discover_csv_schema()` returns column names + inferred types
- `sample_rows` parameter works correctly

## Context

- Style reference: `src/rts_predict/common/json_utils.py` (similar
  `discover_json_schema()` wrapper pattern)
- These functions are used by T02 notebooks for full-census schema
  discovery across Parquet and CSV files
- No DuckDB type proposals — that decision is deferred to a later
  ingestion design step per Invariant #9 scope discipline
