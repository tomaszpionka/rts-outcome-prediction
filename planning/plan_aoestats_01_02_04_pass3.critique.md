# Adversarial Critique — plan_aoestats_01_02_04_pass3.md

**Plan:** planning/plan_aoestats_01_02_04_pass3.md
**Phase:** 01 / Step 01_02_04 (Pass 3)
**Date:** 2026-04-15
**Reviewer model:** claude-opus-4-6

---

## VERDICT: APPROVED WITH CONDITIONS

No blocking correctness errors. Four minor issues must be addressed to avoid silent failures and coverage gaps.

---

## Critical Issues (must fix before execution)

None identified.

---

## Minor Issues (should fix)

### M1 — COUNT(DISTINCT col) on STRUCT-array columns will error in DuckDB

**Affects:** T01 cardinality cell

The plan runs `COUNT(DISTINCT {col})` for all 9 `overviews_raw` columns. Five (`civs`, `openings`, `patches`, `groupings`, `changelog`) are `STRUCT(...)[]` types per `overviews_raw.yaml`. DuckDB has known issues with DISTINCT on LIST/nested STRUCT types. With N=1, cardinality is trivially 1 for all columns, but the query may still fail at plan time.

**Fix required:** Skip `COUNT(DISTINCT)` for the 5 complex-typed columns. Hardcode `cardinality = 1` with a note: "All columns have cardinality 1 (trivially — single-row table). STRUCT-array column cardinality set to 1 without DISTINCT query due to DuckDB limitation with nested types." Or wrap the loop in try/except with fallback to 1 for complex types.

### M2 — Histogram plot replacement scope underspecified in T02

**Affects:** T02

The plan says "Replace `HIST_DEFS_MATCHES` definition (line 702)" and "Update histogram plot grid" but does not specify the exact line range for the plot replacement. The existing plot code at lines 734–744 uses hardcoded `plt.subplots(1, 3)` and `zip(axes, hist_data.items())`. Both must be replaced when HIST_DEFS_MATCHES expands from 3 to 7 entries.

**Fix required:** Specify explicitly: "Replace lines 702–706 (HIST_DEFS_MATCHES definition) AND replace lines 734–744 (matches histogram plot) with the dynamic grid code." Without this, an executor could update HIST_DEFS_MATCHES but leave the old plot code, causing a runtime error.

### M3 — overviews_raw columns omitted from field_classification

**Affects:** T01 (implicitly)

The existing `field_classification` dict at notebook line 1268 covers matches_raw and players_raw. The plan adds overviews_raw to the census but does not add its columns. Per Invariant #3, temporal awareness is required:

- `total_match_count` — post-game aggregate (reflects all games at scrape time)
- `civs`, `openings`, `patches`, `groupings` — reference data (pre-game available)
- `last_updated` — provenance metadata
- `changelog`, `tournament_stages` — reference/metadata
- `filename` — provenance (path to source JSON file)

**Fix required:** Either add overviews_raw entries to `field_classification` in Section K, or add `findings["overviews_field_classification_note"]` explicitly documenting the classification decision and deferral. Do not leave this gap silent.

### M4 — Markdown artifact insertion point for overviews_raw subsection is ambiguous

**Affects:** T05

The plan says "Add overviews_raw subsection in Key Findings after num_players block." The num_players block ends at line 1396. The next substantive line (~1398) is `md_path = artifacts_dir / ...` which writes the file. Inserting after `md_path` means the content will not appear in the artifact.

**Fix required:** Specify: "Insert BEFORE the `md_path = ...` line that writes the markdown file (~line 1398)."

---

## Confirmed Correct

1. **DuckDB `LEN()` on LIST columns works.** DuckDB List Functions documentation confirms `len()` aliases `length()` on LIST types. `STRUCT(...)[]` is LIST-of-STRUCT in DuckDB's type system. Plan's caution is appropriate but LEN() will work.

2. **overviews_raw column enumeration is exact.** `overviews_raw.yaml` confirms exactly 9 columns: `last_updated` (VARCHAR), `total_match_count` (BIGINT), `civs` (STRUCT[]), `openings` (STRUCT[]), `patches` (STRUCT[]), `groupings` (STRUCT[]), `changelog` (STRUCT[]), `tournament_stages` (VARCHAR[]), `filename` (VARCHAR). Row count = 1. Plan matches YAML exactly.

3. **`HIST_DEFS_MATCHES` at line 702.** Confirmed: 3 entries — `duration_sec` (60), `irl_duration_sec` (60), `avg_elo` (50). Plan description accurate.

4. **`HIST_DEFS_PLAYERS` at line 747.** Confirmed: 6 entries in format `(table, column, label, bin_width)`. Matches plan expectations exactly.

5. **`sql_queries` dict exists.** Confirmed at notebook line 61: `sql_queries: dict = {}`. Used throughout for artifact SQL storage — consistent with plan's T01 usage.

6. **`findings["num_players_distribution"]` at line 327.** Confirmed. Next markdown cell at line 329. Plan T04 insertion point is valid.

7. **Markdown header string.** Confirmed at line 1362: `"**Tables:** matches_raw (18 cols), players_raw (14 cols)"` — exact match with plan's replace target.

8. **Gate condition column count 13 is correct.** `MATCHES_NUMERIC_DEFS` has 7 entries (lines 513–521). `HIST_DEFS_PLAYERS` has 6 entries (lines 747–753). 7 + 6 = 13.

9. **bin_width=1 for discrete codes is appropriate.** `FLOOR(col / 1) * 1` returns original value — this is a frequency distribution over distinct values. Correct for `raw_match_type` (code) and `patch` (version identifier).

10. **No temporal leakage from overviews_raw census.** Descriptive profiling, not feature construction.

---

## Gate Condition Assessment

Mostly sufficient but two gaps:

**Gap 1:** Does not verify matches histogram plot code (lines 734–744) was updated to dynamic grid. The "executes without errors" clause covers this at runtime but an explicit check is stronger: "matches histogram plot uses `plt.subplots(n_rows_plot, n_cols_plot)` with dynamically computed `n_rows_plot`, not hardcoded `plt.subplots(1, 3)`."

**Gap 2:** Does not verify `field_classification` includes overviews_raw columns (or has an explicit deferral note in `findings`). Add: "`findings['overviews_field_classification_note']` is present OR `overviews_raw` is a key in `field_classification`."
