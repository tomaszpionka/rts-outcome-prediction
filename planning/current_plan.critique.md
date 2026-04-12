# Adversarial Critique — Plan: Schema Discovery 01_01_02

**Plan:** planning/current_plan.md
**Phase:** 01 / Step 01_01_02 (Schema Discovery)
**Date:** 2026-04-12
**Verdict:** REVISE BEFORE EXECUTION

---

## Lens assessments

- **Temporal discipline:** N/A — no features or predictions
- **Statistical methodology:** N/A — no statistical tests
- **Feature engineering:** N/A — no features constructed
- **Thesis defensibility:** ADEQUATE — two weaknesses below
- **Cross-game comparability:** AT RISK — CROSS entry scope ambiguity

## Findings

### 1. [WARNING] Invariant #9 boundary: sample_values expose content

The plan says "reads structure, not content." But `discover_json_schema()`
stores actual scalar values (strings, ints) in `sample_values`. If the
artifact stores `["Serral", "Maru", "Reynor"]`, any reader can interpret
the column semantically — exactly what the scope boundary forbids.

The `step_scope: content` definition does explicitly allow "sample rows,"
so this is not a violation. But the plan's own Scope Boundary section
says no "semantic interpretation of columns" — while sample values enable
exactly that.

**Resolution needed:** Acknowledge the tension explicitly. Document that
sample values are included for type-inference validation only, and the
step's conclusions do not reference them semantically.

### 2. [WARNING] Parquet schema should be census, not sample

`pyarrow.parquet.read_schema()` reads only footer metadata — no row data.
For aoe2companion (2073 files) and aoestats (172 files), reading ALL
schemas is a sub-second operation. Sampling 5 when a census is free
introduces an unnecessary methodological weakness.

An examiner can ask: "Why did you sample when a census was free?"

**Resolution needed:** Change Parquet subdirectories to full schema census.
Keep the temporal stratification narrative for the thesis but base it on
complete data.

### 3. [WARNING] T02 file scope exceeds ~15-file cap

T02 writes 22 files (6 notebooks, 6 artifacts, 3 ROADMAPs, 3 research
logs, 3 STEP_STATUS, 1 CROSS). The plan template says "Cap at ~15 files."

Natural split: T02a (notebooks + artifacts = 12 files), T02b (ROADMAPs +
research logs + STEP_STATUS + CROSS = 10 files).

**Resolution needed:** Either split or explicitly acknowledge the guideline
is exceeded with stated rationale.

### 4. [NOTE] DuckDB type proposals are partially outside scope

For Parquet: Arrow-to-DuckDB mapping is mechanical — defensible. For JSON:
the `_propose_duckdb_type()` heuristic always maps `int` to `BIGINT`
regardless of value range — a design decision, not a structural
observation. For CSV: `pd.read_csv(nrows=10)` infers types from actual
cell values — content-level reading.

**Recommendation:** Document that DuckDB type proposals are preliminary,
to be validated during ingestion. Also: justify `nrows=10` per Invariant
#7 (no magic numbers) or trace it to a source.

### 5. [NOTE] CROSS entry scope ambiguity

"Structural parallels" is ambiguous. Column name string equality is
structural. "Both datasets contain match-level records with player
identifiers" is semantic interpretation.

**Recommendation:** Constrain CROSS entry to: format enumeration, column
name overlap as raw string comparison, schema complexity comparison
(nesting depth, column count). Exclude ingestion design observations.

### 6. [NOTE] discover_parquet_schema() wrapper justification

The wrapper adds dict serialization, DuckDB proposal, and multi-file
consistency check. The consistency check is genuinely new; the rest is
thin. Justified by precedent (`json_utils.py`). Ensure tests cover both
matching and mismatching schema cases.

### 7. [NOTE] get_json_keypaths() performance

210 files x 3MB = 630MB sequential JSON parsing. Feasible but potentially
slow. The 600s notebook timeout should be sufficient but hasn't been
validated.

## Invariant compliance

| # | Status | Notes |
|---|--------|-------|
| 6 | RESPECTED | Code in notebooks, artifacts alongside reports |
| 7 | AT RISK | Parquet sample size unjustified (census is free); CSV nrows=10 not traced |
| 9 | AT RISK | sample_values tension; CSV row reading is content-level |

## Required revisions before materialization

1. **sample_values tension** (finding #1): Add one sentence to Scope
   Boundary acknowledging sample values are for type-inference validation
   only, not semantic interpretation.
2. **Parquet census** (finding #2): Change from 5-file sample to full
   schema census for Parquet subdirectories.
3. **T02 scope** (finding #3): Either split T02 or acknowledge the ~15-file
   guideline is exceeded with rationale.

## Recommended but not blocking

4. Document DuckDB type proposals as preliminary (finding #4).
5. Constrain CROSS entry to structural observations with examples (finding #5).
6. Justify CSV nrows=10 or trace to source (finding #4).
