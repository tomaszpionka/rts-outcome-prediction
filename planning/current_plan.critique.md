---
reviewer: reviewer-adversarial
plan: planning/plan_01_02_03_struct_eda.md
date: 2026-04-14
verdict: APPROVE_WITH_CHANGES
---

# Adversarial Critique: plan_01_02_03_struct_eda.md

## Verdict
**APPROVE WITH REVISIONS** — The plan is scientifically sound in scope and structure, but contains one unsupported assumption (universal Faster game speed) that could silently corrupt duration calculations, omits a required ROADMAP entry, and has gate conditions too weak to catch STRUCT path failures.

---

## Critical Issues (must fix before execution)

### 1. Game-loop conversion assumes Faster speed without verification (plan Section E)

The plan states: "convert to real seconds (game loops / 22.4 at Faster speed)" and applies this in Section E (numeric descriptive statistics) **before** Section D has established whether `details.gameSpeed` is uniformly "Faster" across all 22,390 replays.

The 22.4 constant is correct for Faster speed (16 base loops/s × 5734/4096 multiplier = 22.4). But Section E applies it unconditionally without conditioning on the Section D census of `gameSpeed` values.

**Why it matters:** If any replays use Normal, Slow, or Slower speeds, the duration calculation will be wrong by up to 2.3x, silently corrupting descriptive statistics and any downstream cleaning thresholds.

**Fix:** Add a sequencing dependency: the Section E duration conversion cell must first assert that all replays have `gameSpeed = 'Faster'` using the Section D census result, or branch to use per-replay speed. Add the Liquipedia multiplier citation rather than bare "22.4" (Invariant #7 — no magic numbers without citation).

### 2. Step 01_02_03 missing from ROADMAP

The ROADMAP defines only steps 01_01_01, 01_01_02, 01_02_01, 01_02_02. STEP_STATUS.yaml header states: "Derived from ROADMAP.md step definitions. If this file disagrees with the ROADMAP, this file is wrong."

T02 instructs the executor to add 01_02_03 to STEP_STATUS.yaml, but there is no instruction to add the step definition to the ROADMAP first.

**Fix:** Add a T00 pre-task (or prepend to T02) that adds the 01_02_03 step definition to ROADMAP.md using the same YAML schema as existing steps (step_number, name, description, phase, pipeline_section, predecessors, notebook_path, inputs, outputs, gate, thesis_mapping, research_log_entry). Add `ROADMAP.md` to T02's file scope.

---

## Moderate Issues (should fix)

### 3. Gate conditions cannot detect STRUCT path failures

Gate condition #3 requires valid JSON with NULL counts and descriptive statistics. But DuckDB returns NULL (not an error) when accessing a non-existent STRUCT field path. A notebook that runs on wrong STRUCT paths will produce all-NULL results — which is valid JSON and does "contain" statistics (all NULL/NaN). The gate passes.

**Fix:** Add explicit gate condition: "At least 3 extracted STRUCT fields must have non-NULL rate > 0%." Or add a sanity-check assertion cell after Section A: assert `COUNT(*) WHERE game_speed IS NOT NULL > 0`.

### 4. `timeUTC` full parsing risk (Section F)

The SC2EGSet `timeUTC` format is `2016-07-29T04:50:12.5655603Z` — 7-digit fractional seconds (.NET 100-nanosecond precision). DuckDB's `STRPTIME %f` handles only 6 digits; 7 digits may fail.

**Fix:** In Section F, use string-based MIN/MAX (ISO 8601 strings sort lexicographically) and `SUBSTR(details.timeUTC, 1, 7)` for month extraction — no STRPTIME needed. Reserve full timestamp parsing for 01_05 (Temporal & Panel EDA).

### 5. `header."version"` quoting inconsistency

SQL sketch correctly uses `header."version"` (quoted, since `version` is a DuckDB reserved keyword), but prose references use unquoted `header.version`. Unquoted form will fail with a parse error.

**Fix:** Standardize to `header."version"` throughout. Add a one-line note warning the executor that `version` must be quoted.

### 6. EDA Manual Section 3.1/3.2 coverage claims are overstated

The plan claims to cover Manual Sections 3.1 and 3.2, but omits required items:

- **Section 3.1** requires: zero count, skewness, kurtosis, outlier detection (IQR fences, z-scores), pattern/format frequency for strings, uniqueness ratio as per-column metric.
- **Section 3.2** requires: duplicate row count/percentage, feature completeness matrix, correlation matrices, memory footprint. These belong in 01_03 (Systematic Data Profiling).

**Fix:** Change the Scientific Rationale to say "partially covers Manual Sections 3.1 and 3.2 — univariate census layer; remaining profiling metrics (zero counts, skewness, kurtosis, IQR outlier detection, correlation matrices, duplicate detection) deferred to 01_03."

---

## Minor Issues (consider fixing)

### 7. Cross-check analyses technically bivariate

Section A proposes cross-checking `details.gameSpeed` vs `initData.gameDescription.gameSpeed`. This is technically bivariate. The plan defers all bivariate analysis but includes these.

**Fix:** Add a note to Out of Scope: "Data-quality cross-checks between duplicate fields are included as integrity checks, not exploratory bivariate EDA."

### 8. `gameOptions` sub-STRUCT fields not documented

`initData.gameDescription.gameOptions` contains fields (`competitive`, `observers`, `practice`, `randomRaces`) not extracted. `gameOptions.competitive` could be relevant for filtering non-competitive replays in 01_04.

**Fix:** Add a note to the research_log template that these fields exist and may be relevant for 01_04 cleaning filters.

### 9. Section D and E cell count risk

Sections D (10 categorical fields) and E (8+ numeric fields) may exceed the 50-line cell cap if implemented as per-column cells.

**Fix:** T01 instructions should explicitly state that Sections D and E use loop-based cells iterating over column lists — matching the pattern in 01_02_02's for-loop cells.

### 10. NULL census missing null percentage

Section B's NULL census SQL computes raw null counts but not null percentages. EDA Manual Section 3.1 requires "null/missing count **and percentage**."

**Fix:** Add `ROUND(100.0 * (COUNT(*) - COUNT(col)) / COUNT(*), 2)` columns, or compute in a follow-up cell.

---

## Confirmed Correct

1. **All STRUCT field paths are valid.** Every path in the SQL sketch was cross-referenced against the 01_02_02 ingestion artifact schema — all match (`details.gameSpeed`, `header.elapsedGameLoops`, `metadata.mapName`, `initData.gameDescription.mapSizeX`, etc.).

2. **The 25-column NULL census is complete and correct.** All 25 columns listed match the `replay_players_raw` schema from the ingestion artifact exactly.

3. **`result` column exists in `replay_players_raw`.** Confirmed from ingestion.py (`result VARCHAR`). Target variable analysis will work.

4. **22.4 loops/second constant is arithmetically correct for Faster speed.** 16 base × 5734/4096 = 22.4. The problem is unconditional application, not the constant itself.

5. **Invariant #6 compliance correctly planned.** T01 instruction 10 requires SQL queries verbatim in the markdown; gate condition 2 re-states it. Matches 01_02_02 pattern.

6. **Invariant #9 compliance correctly planned.** Conclusions limited to univariate distributions and NULL rates. No cleaning, no features, no identity resolution. Out of Scope section explicitly documents the boundaries.

7. **`SUBSTR(details.timeUTC, 1, 7)` for month extraction is robust.** Given confirmed ISO 8601 format, this produces correct `YYYY-MM` keys that sort lexicographically. MIN/MAX on raw VARCHAR is also correct.

8. **`get_notebook_db("sc2", "sc2egset")` read-only access is correct.** No DDL/DML needed; the step only queries existing tables.
