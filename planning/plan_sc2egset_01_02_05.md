---
category: A
branch: feat/census-pass3
date: 2026-04-15
planner_model: claude-opus-4-6
dataset: sc2egset
phase: "01"
pipeline_section: "01_02 -- Exploratory Data Analysis (Tukey-style)"
step_ref: "01_02_05"
invariants_touched:
  - 3
  - 6
  - 7
  - 9
source_artifacts:
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.json
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.md
  - sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.py
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/01_02_05_visualizations.md
  - .claude/scientific-invariants.md
  - docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md
critique_required: true
research_log_ref: null
---

# Plan: sc2egset 01_02_05 -- Univariate EDA Visualizations (Pass 3 — Post-Audit Revision)

## Scope

Revised plan for Step 01_02_05 for the sc2egset dataset. This plan addresses
all BLOCKERs and WARNINGs identified by the pre-execution adversarial audit.
The step was previously executed (status: complete, 2026-04-14) but produced
artifacts that fail the audit gate. This plan specifies: (A) a full ROADMAP
entry to replace the skeleton stub, and (B) a revised notebook task list that
adds the missing map distribution chart, adds temporal classification
annotations to 4 in-game column plots, replaces the unjustified 40-minute
duration clip with a data-derived p95 threshold, and restructures the result
distribution chart for thesis comparability.

Phase 01, Pipeline Section 01_02, Step 01_02_05.

## Problem Statement

The existing 01_02_05 notebook produced 12 plots and a markdown artifact. An
adversarial audit identified three BLOCKERs: (1) the ROADMAP entry is a
skeleton stub missing `inputs`, `outputs`, `gate`, `scientific_invariants_applied`,
`thesis_mapping`, and `research_log_entry` fields; (2) four plots of in-game
columns (APM, SQ, supplyCappedPercent, elapsed_game_loops) carry no temporal
classification annotation per Invariant #3; (3) no map distribution bar chart
exists, breaking cross-dataset comparability with aoestats and aoe2companion
which both have map top-k charts. Additionally, four warnings require
resolution: the 40-minute duration clip lacks data justification (I7), the
relationship between 01_02_04 and 01_02_05 plot sets is undocumented, the
result bar chart structure does not match the thesis comparability standard,
and the zero-rate visualization could use severity color thresholds.

## Assumptions & unknowns

- **Assumption:** The existing notebook at
  `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.py` is the
  baseline. This plan modifies it in place rather than creating a new notebook.
- **Assumption:** The 01_02_04 JSON artifact `categorical_profiles.map_name`
  contains the top-20 map names with counts (confirmed: 20 entries present).
  Total map_name cardinality is 188.
- **Unknown:** Whether the existing 11 01_02_04-prefixed PNGs should be deleted
  or retained as historical artifacts. This plan specifies they are retained
  (supplements, not supersedes) and the ROADMAP documents both sets.

## Literature context

EDA Manual Section 2.1 specifies univariate visualizations as the first EDA
layer. Invariant #3 mandates temporal discipline — any visualization of a
column classified as `in_game` in the field_classification must carry a visible
annotation so the reader knows it is not available at prediction time.
Invariant #7 prohibits unjustified thresholds.

SC2 game loop to real-time conversion: 22.4 loops/second at "Faster" game
speed (the only speed present in sc2egset, confirmed by
`game_speed_assertion: "PASSED -- all Faster"` in the 01_02_04 JSON artifact).
This constant originates from the SC2 engine specification and is used in the
01_02_04 artifact's own `duration_stats` computation.

Duration clip threshold derivation (replaces unjustified 40 min):
- `duration_stats.p95` = 30,270.1 game loops (from 01_02_04 JSON artifact)
- 30,270.1 / 22.4 = 1,351.3 seconds = 22.52 minutes
- Clip at p95 = 1,352 seconds (rounded up). This shows 95% of games in the
  detailed panel and annotates the excluded 5% tail.
- Derivation: "p95 of elapsed_game_loops from 01_02_04 census artifact,
  converted at 22.4 loops/second (SC2 Faster speed)."

Bin count: 50 bins. Justification: Sturges rule yields
ceil(1 + log2(44817)) = 16 bins minimum for replay_players_raw,
ceil(1 + log2(22390)) = 15 bins minimum for replays_meta_raw. 50 bins provides
approximately 3x finer resolution for shape assessment in first-pass
exploratory histograms, per Tukey (1977) recommendation for visual consistency
across a single exploratory notebook. This is the project-wide first-pass EDA
resolution standard applied consistently across all three datasets.

---

## Part A — ROADMAP Patch Specification

The following is the complete ROADMAP entry for Step 01_02_05, replacing the
existing skeleton stub in its entirety. The executor must replace the entire
`### Step 01_02_05` section (from `### Step 01_02_05` through the closing
triple-backtick of the YAML block) with this content.

```yaml
step_number: "01_02_05"
name: "Univariate EDA Visualizations"
description: "Dedicated visualization notebook for all univariate distributions profiled in 01_02_04. Thirteen visualization groups covering target variable, categorical distributions, numeric distributions with split views, temporal coverage, map popularity, and MMR zero-spike cross-tabulation. Every in-game column plot carries a temporal classification annotation per Invariant #3. Supplements (does not supersede) the 11 exploratory PNGs produced by 01_02_04."
phase: "01 — Data Exploration"
pipeline_section: "01_02 — Exploratory Data Analysis (Tukey-style)"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Sections 2.1, 3.4"
dataset: "sc2egset"
question: "What do the distributions from 01_02_04 look like visually, and do the visual patterns confirm or challenge the statistical summaries?"
method: "Matplotlib visualizations driven by 01_02_04 JSON artifact and DuckDB queries. Bar charts for categorical variables. Dual-panel histograms for skewed distributions and sentinel exclusions. Temporal classification annotations on all in-game column plots (APM, SQ, supplyCappedPercent, elapsed_game_loops). All values derived from census artifact at runtime — no hardcoded numbers."
stratification: "By column type (categorical, numeric, temporal) and by table (replay_players_raw, replays_meta_raw via struct_flat)."
predecessors:
  - "01_02_04"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.py"
inputs:
  duckdb_tables:
    - "replay_players_raw"
    - "replays_meta_raw"
  prior_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_04_univariate_census.json"
  external_references:
    - ".claude/scientific-invariants.md"
    - "docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md, Sections 2.1, 3.4"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/02_eda/plots/01_02_05_result_bar.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_categorical_bars.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_selectedrace_bar.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_mmr_split.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_apm_hist.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_sq_split.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_supplycapped_hist.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_duration_hist.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_mmr_zero_interpretation.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_temporal_coverage.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_isinclan_bar.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_clantag_top20.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_map_top20.png"
  report: "artifacts/01_exploration/02_eda/01_02_05_visualizations.md"
  supplements_not_supersedes: "The 11 PNGs prefixed 01_02_04_* in the same plots/ directory were produced by the 01_02_04 notebook as inline exploratory plots. They are retained as historical artifacts. 01_02_05 produces the thesis-grade visualization set (13 PNGs) with verification cells, temporal annotations, and data-derived thresholds."
reproducibility: "Code and output in the paired notebook."
scientific_invariants_applied:
  - number: "3"
    how_upheld: "All four in-game columns (APM, SQ, supplyCappedPercent, elapsed_game_loops) carry a visible annotation: 'IN-GAME — not available at prediction time (Inv. #3)'. This ensures the reader knows these distributions describe post-game metrics, not pre-game features."
  - number: "6"
    how_upheld: "All DuckDB SQL queries that produce plotted data are stored in a sql_queries dict and appear verbatim in the markdown artifact."
  - number: "7"
    how_upheld: "Bin count justified via Sturges rule (16 min) with 50 for shape resolution per Tukey (1977). Duration clip at p95 (1,352 sec / 22.5 min) derived from 01_02_04 census artifact duration_stats.p95 = 30,270.1 loops / 22.4 loops/sec."
  - number: "9"
    how_upheld: "Read-only step — visualization only. No new analytical computation beyond what is needed for plotting. All underlying statistics come from 01_02_04 artifacts."
gate:
  artifact_check: "All 13 PNG files exist under artifacts/01_exploration/02_eda/plots/ (01_02_05_*.png). 01_02_05_visualizations.md exists and is non-empty."
  continue_predicate: "All 13 PNG files exist. Markdown artifact contains plot index table and all SQL queries. Notebook executes end-to-end without errors. All 4 in-game column plots carry temporal classification annotations."
  halt_predicate: "Any PNG file is missing, or any in-game column plot lacks a temporal classification annotation, or notebook execution fails."
thesis_mapping:
  - "Chapter 4 — Data and Methodology > 4.1.1 SC2EGSet (StarCraft II)"
  - "Chapter 4 — Data and Methodology > 4.2.1 Pre-game vs in-game field classification"
research_log_entry: "Required on completion."
```

### Cross-dataset comparability check (constraint #8)

After this plan, all three datasets will have:
- (a) Target distribution plot: `01_02_05_result_bar.png` (sc2egset), `01_02_05_winner_distribution.png` (aoestats), `01_02_05_won_distribution.png` (aoe2companion). PRESENT.
- (b) Map top-k bar chart: `01_02_05_map_top20.png` (sc2egset, NEW), `01_02_05_map_top20.png` (aoestats), `01_02_05_map_top_k.png` (aoe2companion). PRESENT.
- (c) Match duration histogram: `01_02_05_duration_hist.png` (sc2egset), `01_02_05_duration_histogram.png` (aoestats), varies (aoe2companion — no duration column; confirmed out of scope). PRESENT for datasets that have duration.
- (d) Rating/MMR histogram: `01_02_05_mmr_split.png` (sc2egset), `01_02_05_elo_distributions.png` (aoestats), `01_02_05_rating_histogram.png` (aoe2companion). PRESENT.

---

## Part B — Notebook Task List

### Relationship to existing plan tasks

The existing plan (plan_sc2egset_01_02_05.md) has T01-T15. The existing notebook
has been executed and produced 12 plots. This pass 3 revision modifies the
existing notebook rather than recreating it. Tasks below specify only the
**changes** needed. Tasks that require no changes are not listed.

**Unchanged tasks** (no modifications needed):
- T01 (skeleton/load), T03 (categorical bars), T04 (selectedRace),
  T05 (MMR split), T10 (MMR zero-spike), T11 (temporal coverage),
  T12 (isInClan), T13 (clanTag top-20).

**Modified tasks** (listed below):
- T02 (result bar) — restructured for thesis comparability
- T06 (APM) — add temporal classification annotation
- T07 (SQ split) — add temporal classification annotation
- T08 (supplyCappedPercent) — add temporal classification annotation
- T09 (duration) — add temporal annotation + replace 40-min clip with p95 threshold
- T14 (markdown artifact) — update to 13 plots, add map query
- T15 (ROADMAP/STEP_STATUS) — full ROADMAP entry replacement

**New tasks:**
- T16 (map top-20 bar chart) — new plot

---

### T02 — Result distribution bar chart (REVISED)

**Objective:** Revise the result bar chart so that Win and Loss are the two
primary bars (the binary prediction classes), with Undecided (24) and Tie (2)
annotated separately as a text note rather than as full-height bars. This makes
the chart visually comparable across all three datasets.

**Instructions:**
1. Replace the existing T02 plot cell in the notebook.
2. Read data from `census["result_distribution"]`.
3. Create a figure with figsize=(10, 6).
4. Plot only Win and Loss as two vertical bars.
5. Add count annotations on each bar.
6. Add a text annotation in the upper-right corner of the plot:
   `f"Excluded from binary target: Undecided ({n_undecided}), Tie ({n_tie})"`
   where `n_undecided` and `n_tie` are dynamically derived from the JSON data.
7. Title: "Result Distribution (Binary Prediction Target)".
8. Save as `plots_dir / "01_02_05_result_bar.png"` (same filename, overwrite).
9. `plt.close()` after save.

**Verification:**
- Plot shows exactly 2 bars (Win, Loss).
- Text annotation shows Undecided and Tie counts.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T06 — APM distribution histogram (REVISED — add temporal annotation)

**Objective:** Add an in-game temporal classification annotation to the APM
histogram per Invariant #3 and audit BLOCKER #2.

**Instructions:**
1. In the existing T06 plot cell, add the following annotation after plotting:
   ```python
   ax.annotate(
       "IN-GAME — not available at prediction time (Inv. #3)",
       xy=(0.5, 1.02), xycoords="axes fraction",
       ha="center", va="bottom", fontsize=9, fontstyle="italic",
       color="red",
   )
   ```
2. The annotation must appear ABOVE the title so it is immediately visible.
   Alternatively, place it in the upper-left corner inside the plot area with a
   colored background box:
   ```python
   ax.annotate(
       "IN-GAME — not available\nat prediction time (Inv. #3)",
       xy=(0.02, 0.98), xycoords="axes fraction",
       ha="left", va="top", fontsize=8, fontstyle="italic",
       color="darkred",
       bbox=dict(boxstyle="round,pad=0.3", fc="#ffe0e0", ec="red", alpha=0.9),
   )
   ```
   The executor may choose either placement; the critical requirement is that
   the annotation is visible and contains the text "IN-GAME" and "not available
   at prediction time".
3. Save as `plots_dir / "01_02_05_apm_hist.png"` (overwrite).
4. `plt.close()` after save.

**Verification:**
- Plot contains visible red-styled annotation with "IN-GAME" text.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T07 — SQ distribution split view (REVISED — add temporal annotation)

**Objective:** Add an in-game temporal classification annotation to both SQ
subplots per Invariant #3.

**Instructions:**
1. In the existing T07 plot cell, add the same style of annotation as T06 to
   the figure-level (not per-subplot). Use `fig.text()` or annotate on subplot (b):
   ```python
   fig.text(
       0.5, 0.01,
       "IN-GAME — not available at prediction time (Inv. #3)",
       ha="center", va="bottom", fontsize=9, fontstyle="italic",
       color="darkred",
   )
   ```
   Or add to each subplot individually using the same `ax.annotate` pattern
   from T06. The critical requirement is visibility.
2. Save as `plots_dir / "01_02_05_sq_split.png"` (overwrite).
3. `plt.close()` after save.

**Verification:**
- Both subplots (or the figure as a whole) carry visible "IN-GAME" annotation.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T08 — supplyCappedPercent histogram (REVISED — add temporal annotation)

**Objective:** Add an in-game temporal classification annotation to the
supplyCappedPercent histogram per Invariant #3.

**Instructions:**
1. Same annotation pattern as T06. Add to the existing plot cell:
   ```python
   ax.annotate(
       "IN-GAME — not available\nat prediction time (Inv. #3)",
       xy=(0.02, 0.98), xycoords="axes fraction",
       ha="left", va="top", fontsize=8, fontstyle="italic",
       color="darkred",
       bbox=dict(boxstyle="round,pad=0.3", fc="#ffe0e0", ec="red", alpha=0.9),
   )
   ```
2. Save as `plots_dir / "01_02_05_supplycapped_hist.png"` (overwrite).
3. `plt.close()` after save.

**Verification:**
- Plot contains visible "IN-GAME" annotation.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T09 — Duration histogram (REVISED — temporal annotation + data-derived clip)

**Objective:** (a) Replace the unjustified 40-minute clip with a data-derived
p95 threshold, and (b) add a temporal classification annotation labeling
elapsed_game_loops as an in-game/game-level descriptor.

**Instructions:**

**Clip threshold derivation (Invariant #7):**
- Source: `census["duration_stats"]["p95"]` = 30,270.1 game loops.
- Conversion: 30,270.1 / 22.4 = 1,351.3 seconds.
- Clip value: `CLIP_SECONDS = census["duration_stats"]["p95"] / 22.4`
  (derive at runtime from the JSON, do NOT hardcode 1352).
- The `LOOPS_PER_SECOND = 22.4` constant is retained because it is the SC2
  engine constant for Faster speed, confirmed by `game_speed_assertion` in the
  artifact.

**Modifications to existing T09 cell:**
1. Replace `CLIP_SECONDS = 2400` with:
   ```python
   CLIP_SECONDS = census["duration_stats"]["p95"] / LOOPS_PER_SECOND
   clip_minutes = CLIP_SECONDS / 60
   print(f"Duration clip at p95: {CLIP_SECONDS:.1f}s ({clip_minutes:.1f} min)")
   ```
2. Update subplot (b) title from `"Game Duration (clipped at 40 min)"` to:
   ```python
   f"Game Duration (clipped at p95 = {clip_minutes:.0f} min)"
   ```
3. Update subplot (b) annotation from `"N={n} replays > 40 min"` to:
   ```python
   n_over_p95 = (duration_data["duration_sec"] > CLIP_SECONDS).sum()
   ax_b.annotate(
       f"N={n_over_p95:,} replays > p95 ({clip_minutes:.0f} min) not shown\n"
       f"[p95 derived from 01_02_04 census artifact]",
       xy=(0.95, 0.95), xycoords="axes fraction",
       ha="right", va="top", fontsize=8,
       bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow"),
   )
   ```
4. Add temporal classification annotation (as a figure-level or per-subplot
   annotation):
   ```python
   fig.text(
       0.5, 0.01,
       "IN-GAME (game-level descriptor) — duration known only after match ends (Inv. #3)",
       ha="center", va="bottom", fontsize=9, fontstyle="italic",
       color="darkred",
   )
   ```
5. Adjust `fig.subplots_adjust(bottom=...)` if needed to make room for the
   figure-level annotation.
6. Save as `plots_dir / "01_02_05_duration_hist.png"` (overwrite).
7. `plt.close()` after save.

**Verification:**
- Subplot (b) clips at approximately 22.5 min (not 40 min).
- Clip value is derived from `census["duration_stats"]["p95"]`, not hardcoded.
- Plot carries visible "IN-GAME" temporal annotation.
- Annotation references "p95 derived from 01_02_04 census artifact".

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T16 — Map top-20 horizontal bar chart (NEW)

**Objective:** Create a horizontal bar chart of the 20 most frequently played
maps, filling the cross-dataset comparability gap identified in BLOCKER #3.
Both aoestats and aoe2companion have equivalent charts.

**Instructions:**
1. Add a new markdown cell after T13 (clanTag): `## Plot 13: Map Top-20`.
2. Verification cell:
   ```python
   map_data = pd.DataFrame(census["categorical_profiles"]["map_name"])
   print(f"=== Map top-20 ({len(map_data)} entries, total cardinality=188) ===")
   print(map_data.to_string(index=False))
   ```
3. Plot cell: horizontal bar chart (barh), figsize=(12, 8).
   - Sort by count descending (largest at top).
   - Annotate bars with count values.
   - x-axis label: "Number of replays".
   - y-axis label: "Map name".
   - Title: "Map Distribution (Top 20 of 188 maps)".
   - Derive total replays for context annotation:
     ```python
     total_in_top20 = sum(r["cnt"] for r in census["categorical_profiles"]["map_name"])
     total_replays = census["duration_stats"]["min_val"]  # wrong, use below
     # Actually, derive total replays from the known count:
     total_replays = 22390  # But don't hardcode -- use:
     total_replays = census["null_census"]["replays_meta_raw_filename"]["total_rows"]
     pct_top20 = 100.0 * total_in_top20 / total_replays
     ```
     Add annotation: `f"Top 20 maps cover {pct_top20:.1f}% of {total_replays:,} replays"`.
4. The data source for this plot is the 01_02_04 JSON artifact
   `categorical_profiles.map_name` key, which contains the top-20 map names
   and their counts. The total cardinality (188) is from the
   `cardinality_data` key where `column == "map_name"`.
5. No DuckDB query is needed for this plot — all data comes from the JSON
   artifact.
6. Save as `plots_dir / "01_02_05_map_top20.png"`.
7. `plt.close()` after save.

**Verification:**
- Plot file exists at `plots_dir / "01_02_05_map_top20.png"`.
- 20 horizontal bars visible, sorted by count.
- Annotation shows coverage percentage.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.py`

**Invariant notes:**
- I7: No thresholds used — full top-20 from artifact.
- I9: No new computation — reads pre-existing artifact.
- I6: No DuckDB query used; data source is JSON artifact (noted in markdown artifact).

---

### T14 — Write summary markdown artifact (REVISED)

**Objective:** Update the markdown artifact to reflect 13 plots (was 12),
add the map top-20 entry, add the DuckDB query for map_name (none needed --
note JSON source), and document the 01_02_04 vs 01_02_05 plot relationship.

**Instructions:**
1. Update the plot index table from 12 to 13 rows. Add row 13:
   `| 13 | Map Distribution (Top 20) | 01_02_05_map_top20.png | Top 20 of 188 maps; covers approximately X% of replays. Map variety driven by seasonal ladder map pools. |`
2. Add a new section after the plot index table:

   ```markdown
   ## Relationship to 01_02_04 Plots

   The 11 PNGs prefixed `01_02_04_*` in the same `plots/` directory were
   produced by the 01_02_04 notebook as inline exploratory plots during the
   univariate census. They are retained as historical artifacts.

   01_02_05 produces the thesis-grade visualization set (13 PNGs) with:
   - Verification cells preceding every plot
   - Temporal classification annotations on all in-game columns (Inv. #3)
   - Data-derived thresholds (Inv. #7)
   - Cross-dataset comparability (map top-k chart)

   The 01_02_05 set is the authoritative reference for thesis figures.
   ```

3. Update the "SQL Queries" section. The map plot uses no SQL query — add a
   note: "T16 (map top-20): Data from 01_02_04 JSON artifact
   `categorical_profiles.map_name` — no DuckDB query."

4. Update the observation for plot 1 (result bar) to note the revised structure:
   "Win/Loss shown as binary target bars; Undecided (24) and Tie (2) annotated
   separately."

5. Update the observation for plot 8 (duration) to note the revised clip:
   "Clipped at p95 = ~22.5 min (derived from 01_02_04 census
   duration_stats.p95 = 30,270.1 loops / 22.4 loops/sec)."

6. Verify all 13 PNG files exist.
7. Write to `artifacts_dir / "01_02_05_visualizations.md"` (overwrite).
8. Close DuckDB connection.

**Verification:**
- Markdown artifact lists 13 plots.
- Contains "Relationship to 01_02_04 Plots" section.
- SQL Queries section present with note for T16.
- All 13 PNG files verified present.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.py`
- `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.ipynb`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/01_02_05_visualizations.md`

---

### T15 — Update ROADMAP.md (REVISED — full entry replacement)

**Objective:** Replace the skeleton stub in ROADMAP.md with the full entry from
Part A.

**Instructions:**
1. Open `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`.
2. Locate the section `### Step 01_02_05 -- Univariate EDA Visualizations`.
3. Replace the entire YAML block (from the opening triple-backtick through the
   closing triple-backtick) with the full YAML from Part A of this plan.
4. Preserve the `---` separator after the block.
5. Do NOT modify STEP_STATUS.yaml — the step status remains `complete` with
   the existing date; this revision updates artifact quality, not step status.
   After execution, STEP_STATUS completed_at should be updated to the new date.

**Verification:**
- ROADMAP.md Step 01_02_05 contains all fields: inputs, outputs, gate,
  scientific_invariants_applied, thesis_mapping, research_log_entry,
  supplements_not_supersedes.
- No skeleton stub fields remain.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`

---

## Gate Condition

All of the following must be true:

- [ ] 13 PNG files exist under `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/plots/`:
  1. `01_02_05_result_bar.png`
  2. `01_02_05_categorical_bars.png`
  3. `01_02_05_selectedrace_bar.png`
  4. `01_02_05_mmr_split.png`
  5. `01_02_05_apm_hist.png`
  6. `01_02_05_sq_split.png`
  7. `01_02_05_supplycapped_hist.png`
  8. `01_02_05_duration_hist.png`
  9. `01_02_05_mmr_zero_interpretation.png`
  10. `01_02_05_temporal_coverage.png`
  11. `01_02_05_isinclan_bar.png`
  12. `01_02_05_clantag_top20.png`
  13. `01_02_05_map_top20.png`
- [ ] Markdown artifact `01_02_05_visualizations.md` exists and lists all 13 plots.
- [ ] Markdown artifact contains "Relationship to 01_02_04 Plots" section.
- [ ] Markdown artifact contains SQL Queries section (Invariant #6).
- [ ] `01_02_05_apm_hist.png` contains visible "IN-GAME" temporal annotation.
- [ ] `01_02_05_sq_split.png` contains visible "IN-GAME" temporal annotation.
- [ ] `01_02_05_supplycapped_hist.png` contains visible "IN-GAME" temporal annotation.
- [ ] `01_02_05_duration_hist.png` contains visible "IN-GAME" temporal annotation.
- [ ] `01_02_05_duration_hist.png` subplot (b) clips at p95 (~22.5 min), not 40 min.
- [ ] `01_02_05_result_bar.png` shows Win/Loss as 2 bars with Undecided/Tie annotated.
- [ ] ROADMAP.md Step 01_02_05 contains full entry (not skeleton stub).
- [ ] STEP_STATUS.yaml `01_02_05.completed_at` updated to execution date.
- [ ] Notebook executes end-to-end without error.

## File Manifest

| File | Action |
|------|--------|
| `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.py` | Modify |
| `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.ipynb` | Modify (jupytext sync) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/01_02_05_visualizations.md` | Overwrite |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/plots/01_02_05_result_bar.png` | Overwrite |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/plots/01_02_05_apm_hist.png` | Overwrite |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/plots/01_02_05_sq_split.png` | Overwrite |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/plots/01_02_05_supplycapped_hist.png` | Overwrite |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/plots/01_02_05_duration_hist.png` | Overwrite |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/plots/01_02_05_map_top20.png` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | Modify |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` | Modify |

## Out of scope

- Deleting the 11 `01_02_04_*` PNGs (retained as historical artifacts).
- Zero-rate severity color thresholds (WARNING #7) — sc2egset has 0% NULLs,
  so there is no NULL rate plot. The zero-rate observation (MMR 83.6% zero,
  APM 2.5% zero) is documented in the JSON artifact and research log; a
  visualization of zero-rates is not warranted at this step because these
  are sentinel/missing-data patterns, not data quality severity indicators.
  Cross-dataset color thresholds will be applied if a unified data quality
  dashboard is produced in a later step.
- Bivariate and multivariate visualizations (future steps).
- Research log entry (written by executor after completion, not by this plan).
- Modifications to unchanged tasks (T01, T03, T04, T05, T10, T11, T12, T13).

## Open questions

- The T16 map chart uses the JSON artifact's top-20 list. If the thesis
  requires all 188 maps, a DuckDB query will be needed — but this is unlikely
  for a bar chart (top-k is standard).
- Whether the `supplements_not_supersedes` ROADMAP field becomes a
  project-wide convention. This is the first use of such a field.

---

**Critique gate:** For Category A, adversarial critique is required before
execution. Dispatch reviewer-adversarial to produce
`planning/current_plan.critique.md`.
