---
category: A
branch: feat/aoe2companion-won-investigation
date: 2026-04-14
planner_model: claude-sonnet-4-6
dataset: aoe2companion
phase: "01"
pipeline_section: "01_02 EDA"
invariants_touched: [6, 9]
source_artifacts:
  - sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.py
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.json
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md
---

# Plan: Won column NULL root-cause investigation (aoe2companion 01_02_01)

## Scope

Extend the existing step 01_02_01 notebook
(`sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.py`)
with a new diagnostic section that identifies why 12.99M rows (4.69%) have `won=NULL`
after DuckDB reads the full matches Parquet corpus with `union_by_name=true`. This is
a Phase 01 / Step 01_02_01 amendment, not a new step. The investigation runs entirely
in-memory using `duckdb.connect(":memory:")`.

## Problem Statement

The 01_02_01 artifact records 12,985,561 NULL values in the `won` column out of
277,099,059 total rows. The `won` column is the prediction target for this thesis.
Understanding whether these NULLs are genuine (the source data never recorded a winner)
or artificial (caused by DuckDB type promotion when `union_by_name=true` coerces
heterogeneous Parquet column types) is critical before any cleaning decisions are made
in later steps.

Two hypotheses require testing: (H1) the `won` column was encoded with different Parquet
types across files over the data collection period (e.g., INT64 in early files, BOOLEAN
in later files), and DuckDB's union-by-name type promotion silently converts non-boolean
values to NULL; (H2) the NULLs are genuine — the source data contains NULL `won` values
within individual files, independent of type promotion. These hypotheses are not mutually
exclusive.

## Literature Context

DuckDB's `union_by_name` option resolves schema conflicts by promoting columns
to a common supertype. The Parquet format allows the same logical column to have
different physical types across files (e.g., INT32, INT64, BOOLEAN). When DuckDB
promotes INT64 to BOOLEAN, values other than 0 and 1 may become NULL rather than
raising an error. This is standard Parquet reader behaviour but is not prominently
documented as a data loss risk.

The 01_01_02 schema discovery step confirmed 54 consistent column names across
all 2,073 match files but did not inspect per-column Parquet physical types —
it checked column name consistency only. The current investigation fills that gap
for the `won` column specifically.

## Assumptions & Unknowns

- **Assumption:** The `won` column exists in all 2,073 match Parquet files (01_01_02
  found 54 consistent columns across all files).
- **Assumption:** DuckDB's `parquet_schema()` function can read individual file metadata
  without loading row data.
- **Unknown:** Whether `won` has a uniform Parquet physical/logical type across all 2,073
  files. Resolved by Q1.
- **Unknown:** Whether files with non-BOOLEAN `won` types produce NULLs under
  `union_by_name=true` promotion. Resolved by Q3.
- **Unknown:** Whether genuine NULL `won` values exist within individual files independent
  of type promotion. Resolved by Q2 and Q4.

---

## Execution Steps

## T01 — Extend 01_02_01 with won NULL root-cause investigation

**Objective:** Add a new section 8 ("Won column: root-cause investigation") to the
existing 01_02_01 notebook. This section runs four diagnostic queries (Q1–Q4) that
together determine whether `won` NULLs originate from Parquet schema heterogeneity and
DuckDB type promotion, from genuine source NULLs, or from both. Extend the existing JSON
artifact with a `won_null_root_cause` key containing all query results.

**Instructions:**

1. Open `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.py`.

2. Rename the existing section 8 ("Findings and ingestion strategy recommendation") to
   section 9. Rename the "Write artifact" section to section 10.

3. Insert the following new section 8 after the existing section 7e. All code in this
   section uses a fresh `duckdb.connect(":memory:")` connection (`con8`). The matches
   glob is `str(AOE2COMPANION_RAW_DIR / "matches" / "*.parquet")`.

4. **Section 8 header cell** (markdown):
   ```
   ## 8. Won column: root-cause investigation

   The prediction target `won` has 12.99M NULLs (4.69%). This section
   diagnoses whether these NULLs originate from Parquet schema heterogeneity
   (DuckDB type promotion under `union_by_name=true`) or from genuine NULL
   values in the source files.

   Two hypotheses:
   - **H1 (schema evolution):** `won` was stored as different Parquet types
     across files (e.g., INT64 in early files, BOOLEAN in later files).
     DuckDB type promotion silently converts non-boolean values to NULL.
   - **H2 (genuine NULLs):** Source files contain NULL `won` values
     independent of type promotion.
   ```

5. **Q1 cell** — Per-file `won` Parquet schema type

   Markdown header: `### 8a. Q1 — Per-file won Parquet schema type`

   Code cell:
   ```python
   con8 = duckdb.connect(":memory:")
   matches_glob = str(AOE2COMPANION_RAW_DIR / "matches" / "*.parquet")

   q1_result = con8.sql("""
       SELECT
           type AS parquet_type,
           COUNT(*) AS file_count,
           LIST(file_name ORDER BY file_name)[:3] AS example_files
       FROM parquet_schema('{glob}')
       WHERE name = 'won'
       GROUP BY type
       ORDER BY file_count DESC
   """.format(glob=matches_glob))
   q1_result.show()
   q1_df = q1_result.fetchdf()
   print(f"\nDistinct won types across {q1_df['file_count'].sum()} files: "
         f"{len(q1_df)} type(s)")
   ```

   **Purpose:** Reads Parquet metadata only (no row data). If `won` appears as multiple
   types (e.g., BOOLEAN in some files, INT64 in others), this directly confirms H1.

6. **Q2 cell** — Per-type-group `won` value census without type promotion

   Markdown header: `### 8b. Q2 — Per-type-group won value census (no type promotion)`

   Code cell:
   ```python
   # Get file groups by won type from Q1
   q2_groups = con8.sql("""
       SELECT
           type AS parquet_type,
           LIST(file_name ORDER BY file_name) AS files
       FROM parquet_schema('{glob}')
       WHERE name = 'won'
       GROUP BY type
   """.format(glob=matches_glob)).fetchall()

   for parquet_type, files in q2_groups:
       # Read all files in the type group — no sampling cap.
       # Each file is read without union_by_name so no type promotion occurs;
       # the GROUP BY aggregation is lightweight regardless of file count.
       file_list = ", ".join(f"'{f}'" for f in files)
       print(f"\n{'='*60}")
       print(f"  won type: {parquet_type} — {len(files)} files")
       print(f"{'='*60}")
       # Read WITHOUT union_by_name to avoid type promotion
       con8.sql("""
           SELECT
               typeof(won) AS runtime_type,
               won::VARCHAR AS won_value,
               COUNT(*) AS row_count
           FROM read_parquet(
               [{file_list}],
               binary_as_string=true
           )
           GROUP BY runtime_type, won_value
           ORDER BY row_count DESC
       """.format(file_list=file_list)).show()
   ```

   **Purpose:** For each distinct Parquet `won` type, reads a sample of files without
   `union_by_name` to see the actual values. Reveals whether files with non-BOOLEAN
   `won` types contain integers (1/0) or strings, and whether genuine NULLs exist
   within each type group.

7. **Q3 cell** — DuckDB type promotion NULL injection test

   Markdown header: `### 8c. Q3 — Type promotion NULL injection test`

   Code cell:
   ```python
   # If Q1 found multiple types, test promotion on a mixed sample
   if len(q1_df) > 1:
       # Pick up to 3 files from each type group
       mixed_files = []
       for parquet_type, files in q2_groups:
           mixed_files.extend(files[:3])
       mixed_file_list = ", ".join(f"'{f}'" for f in mixed_files)

       print("=== WITHOUT union_by_name (no promotion) ===")
       for f in mixed_files:
           result = con8.sql("""
               SELECT
                   '{fname}' AS file,
                   typeof(won) AS runtime_type,
                   COUNT(*) AS total,
                   COUNT(won) AS won_nn,
                   COUNT(*) - COUNT(won) AS won_null
               FROM read_parquet('{fpath}', binary_as_string=true)
           """.format(fname=f.split('/')[-1], fpath=f))
           result.show()

       print("\n=== WITH union_by_name (promotion active) ===")
       con8.sql("""
           SELECT
               filename.split('match-')[2][:10] AS file_date,
               typeof(won) AS promoted_type,
               COUNT(*) AS total,
               COUNT(won) AS won_nn,
               COUNT(*) - COUNT(won) AS won_null
           FROM read_parquet(
               [{file_list}],
               binary_as_string=true, filename=true, union_by_name=true
           )
           GROUP BY file_date, promoted_type
           ORDER BY file_date
       """.format(file_list=mixed_file_list)).show()
   else:
       print("Q1 found only one won type — type promotion is not the cause.")
       print("Skipping Q3 (no mixed-type promotion to test).")
   ```

   **Purpose:** Direct before/after comparison. If files with INT64 `won` have 0 NULLs
   when read individually but gain NULLs when read together via `union_by_name=true`,
   this conclusively proves H1.

8. **Q4 cell** — Per-file NULL distribution

   Markdown header: `### 8d. Q4 — Per-file won NULL distribution`

   Code cell:
   ```python
   q4_result = con8.sql("""
       SELECT
           filename.split('match-')[2][:10] AS file_date,
           COUNT(*) AS total_rows,
           COUNT(won) AS won_nn,
           COUNT(*) - COUNT(won) AS won_null,
           ROUND(100.0 * (COUNT(*) - COUNT(won)) / COUNT(*), 2) AS won_null_pct
       FROM read_parquet(
           '{glob}',
           binary_as_string=true, filename=true, union_by_name=true
       )
       GROUP BY file_date
       HAVING won_null > 0
       ORDER BY file_date
   """.format(glob=matches_glob))
   q4_result.show(max_rows=50)
   q4_df = q4_result.fetchdf()
   total_files = int(q1_df['file_count'].sum())
   print(f"\nFiles with won NULLs: {len(q4_df)} out of {total_files}")
   print(f"Files with zero NULLs: {total_files - len(q4_df)}")
   print(f"Total NULL rows across all files: {q4_df['won_null'].sum():,}")
   if len(q4_df) > 0:
       print(f"Date range of affected files: {q4_df['file_date'].min()} to "
             f"{q4_df['file_date'].max()}")
   ```

   **Purpose:** Identifies which files contribute NULLs. If NULLs concentrate in a
   specific time window this correlates with a schema change in the source API. Combined
   with Q1, this pinpoints whether the NULL-producing files are the same files with a
   non-BOOLEAN `won` type.

9. **Section 8 verdict cell** (markdown + code):

   Markdown header: `### 8e. Root-cause verdict`

   Code cell:
   ```python
   type_count = len(q1_df)
   types_found = q1_df['parquet_type'].tolist()
   type_file_counts = dict(zip(q1_df['parquet_type'], q1_df['file_count'].astype(int)))
   total_files = int(q1_df['file_count'].sum())
   files_with_nulls = len(q4_df)
   total_nulls = int(q4_df['won_null'].sum()) if len(q4_df) > 0 else 0

   # H1: schema heterogeneity (type promotion)
   verdict_parts = []
   if type_count > 1:
       verdict_parts.append(
           f"H1 SUPPORTED: won column has {type_count} distinct Parquet types "
           f"across files: {types_found}. Type promotion under union_by_name "
           f"may inject NULLs."
       )
   else:
       verdict_parts.append(
           f"H1 REJECTED: won column has a single Parquet type ({types_found[0]}) "
           f"across all files. Type promotion is not the cause of NULLs."
       )

   # H2: genuine NULLs in source files
   # Q2 census (won_value=None in native type) confirms genuine NULLs exist.
   # If H1 is rejected and NULLs are present, H2 is the only explanation.
   if total_nulls > 0 and type_count == 1:
       verdict_parts.append(
           f"H2 SUPPORTED: {total_nulls:,} genuine NULL won values exist in source "
           f"files (not caused by type promotion). Affected files: {files_with_nulls} "
           f"of {total_files}."
       )
   elif total_nulls > 0:
       verdict_parts.append(
           f"H2 PARTIALLY SUPPORTED: NULLs present; disentangle H1/H2 attribution "
           f"by comparing Q2 native-NULL counts vs Q4 post-promotion-NULL counts."
       )
   else:
       verdict_parts.append("H2 REJECTED: no NULL won values found in any file.")

   verdict_parts.append(
       f"Files with won NULLs: {files_with_nulls} of {total_files}. "
       f"Total NULLs: {total_nulls:,}."
   )

   won_root_cause = {
       "q1_parquet_types": type_file_counts,
       "q4_files_with_nulls": files_with_nulls,
       "q4_files_without_nulls": total_files - files_with_nulls,
       "q4_total_nulls": total_nulls,
       "q4_date_range": (
           [q4_df['file_date'].min(), q4_df['file_date'].max()]
           if len(q4_df) > 0 else []
       ),
       "verdict": verdict_parts,
   }

   for line in verdict_parts:
       print(line)
   ```

10. **Close `con8`** at the end of section 8:
    ```python
    con8.close()
    ```

11. **Extend the artifact write cell** (in the existing "Write artifact" section,
    renumbered to section 10). Add the `won_null_root_cause` key to `artifact_data`
    before the JSON write call:
    ```python
    artifact_data["won_null_root_cause"] = won_root_cause
    ```
    Insert this line after the `artifact_data` dict is constructed and before
    `artifact_path.write_text(...)` is called. Also add a summary line to the MD report:
    ```python
    f"## Won NULL root cause\n",
    f"- H1 (schema heterogeneity): {'SUPPORTED' if type_count > 1 else 'REJECTED'}",
    f"- H2 (genuine NULLs): {'SUPPORTED' if total_nulls > 0 and type_count == 1 else 'see verdict'}",
    f"- Files with NULLs: {files_with_nulls} of {total_files}",
    f"- Total NULLs: {total_nulls:,}",
    ```

12. **Update the research log** at
    `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md`.
    Prepend an entry documenting the root-cause investigation findings: which hypothesis
    was supported/rejected, total NULLs, date range of affected files, and the artifact
    path. Use the same entry format as existing entries.

**Verification:**
- Notebook executes end-to-end without errors (run via jupytext or execute cells
  manually)
- Artifact JSON contains `won_null_root_cause` key with non-empty `q1_parquet_types`
  and `verdict`
- The `verdict` list has at least one entry disposing H1 (SUPPORTED or REJECTED)
- Research log has a new entry dated 2026-04-14 referencing step 01_02_01
- `ruff check` and `mypy` pass on touched `.py` files

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.py`
- `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.ipynb` (auto-synced)
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.json`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md`

**Read scope:**
- `src/rts_predict/games/aoe2/config.py` (for `AOE2COMPANION_RAW_DIR`)
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.json`

---

## File Manifest

| File | Action |
|------|--------|
| `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.py` | Update |
| `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.ipynb` | Update (jupytext sync) |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.json` | Update (add `won_null_root_cause` key) |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.md` | Update (add root-cause summary section) |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md` | Update (prepend entry) |

---

## Gate Condition

1. Notebook executes end-to-end without error
2. Artifact JSON contains `won_null_root_cause` with non-empty `q1_parquet_types` and
   `verdict`
3. At least one hypothesis (H1 or H2) has a definitive disposition (SUPPORTED or
   REJECTED) in `verdict`
4. Research log contains a new entry dated 2026-04-14 referencing step 01_02_01
5. No new helper functions were added to `pre_ingestion.py`
6. No new test files were created

---

## Out of Scope

- **Step 01_02_02 (DuckDB Ingestion):** Not touched. The investigation informs future
  cleaning decisions but does not implement them.
- **Helper functions in `pre_ingestion.py`:** Q1–Q4 are single-use diagnostic notebook
  code. No library code is created.
- **Unit tests:** These are exploratory EDA queries, not testable library functions.
- **Other columns:** Only `won` is investigated.
- **Cleaning decisions:** This step diagnoses the root cause. Decisions about how to
  handle NULLs (drop rows, filter by file date, explicit cast) are deferred to a future
  cleaning step.
- **STEP_STATUS.yaml / PHASE_STATUS.yaml:** Step 01_02_01 remains `complete`. This is
  an amendment to an already-complete step, not a status change.

---

## Open Questions

- If H1 is confirmed, can the NULLs be recovered by reading affected files with their
  native type and casting explicitly? — Resolves in a future 01_02_02 or cleaning step.
- If both H1 and H2 are confirmed, what fraction of NULLs is attributable to each cause?
  — Resolves by comparing Q2 (per-file native NULLs) against Q4 (post-promotion NULLs).
