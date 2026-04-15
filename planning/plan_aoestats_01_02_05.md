---
category: A
branch: feat/aoestats-01-02-05-visualizations
date: 2026-04-14
planner_model: claude-opus-4-6
dataset: aoestats
phase: "01"
pipeline_section: "01_02 — Exploratory Data Analysis (Tukey-style)"
invariants_touched: [I6, I7, I9]
source_artifacts:
  - sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_04_univariate_census.py
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.json
  - src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/raw/matches_raw.yaml
  - src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/raw/players_raw.yaml
  - docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md
  - .claude/scientific-invariants.md
critique_required: true
research_log_ref: null
---

# Plan: aoestats 01_02_05 — Univariate Visualizations

## Scope

New step 01_02_05 for the aoestats dataset: a dedicated visualization notebook that produces all EDA plots based on the quantitative findings from 01_02_04 (and its pass-2 augmentation). Every plot cell is preceded by a pandas verification cell. The notebook reads from the JSON artifact and DuckDB directly — no analytical computation beyond what is needed for visualization. Thirteen visualization groups covering winner distribution, num_players distribution, categorical top-k, numeric distributions with dual-panel and sentinel handling, IQR outlier summary, NULL rate summary, and temporal match volume.

## Problem Statement

The 01_02_04 notebook currently mixes analytics (SQL queries, JSON artifact generation) with visualization (bar charts, histograms, boxplots, time series). After the pass-2 augmentation adds nine more analytical sections, the notebook becomes excessively long. Separating visualizations into a dedicated step provides:

1. Cleaner notebook structure: 01_02_04 is pure analytics; 01_02_05 is pure visualization.
2. Plot choices informed by 01_02_04 findings: dual-panel for duration (skewness=1032.64), sentinel exclusion for ELO, non-NULL-only for opening, variable bin widths for age uptimes.
3. Every plot has a verification cell.
4. Standalone PNG artifacts for thesis figures.

## Assumptions and Unknowns

- **Assumption:** 01_02_04 pass-2 has been executed and its JSON artifact contains all keys referenced in this plan (skew_kurtosis, opening_nonnull_distribution, outlier_counts, elo_sentinel_counts, etc.).
- **Assumption:** The notebook reads DuckDB in read-only mode for any data not already in the JSON artifact.
- **Assumption:** matplotlib is sufficient for all plots; no additional dependencies needed.
- **Unknown:** Whether thesis will ultimately use these PNG files or regenerate from code. Does not block execution — PNGs are artifacts regardless.

## Literature Context

EDA Manual Section 2.1: univariate analysis requires histograms, boxplots, and descriptive statistics. Section 3.4 recommends combining histograms with KDE for shape assessment.

Tukey 1977: "Exploratory data analysis is detective work... graphical detective work." Visualizations are not optional EDA decorations — they are the primary analytical instrument.

Anscombe's Quartet (1973): identical summary statistics, dramatically different visual patterns. This is why we produce plots even when we have full descriptive statistics.

Invariant #6: all SQL queries that produce plotted data must appear verbatim in the markdown artifact.

Invariant #7: no magic numbers. Every bin width, clip boundary, and annotation value in this plan is derived from the 01_02_04 census artifact with explicit derivation shown in `[I7: ...]` brackets.

## Execution Steps

### T01 — Add steps 01_02_04 and 01_02_05 to STEP_STATUS and ROADMAP

**Objective:** Register both the completed predecessor (01_02_04) and the new step (01_02_05) in the aoestats tracking files. Step 01_02_04 was executed but never formally registered; it must be registered before 01_02_05 can reference it as a predecessor.

**Instructions:**

1. In `src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml`, after the `01_02_03` entry, add:
   ```yaml
   "01_02_04":
     name: "Univariate Census"
     pipeline_section: "01_02"
     status: complete
     completed_at: "2026-04-14"
   "01_02_05":
     name: "Univariate Visualizations"
     pipeline_section: "01_02"
     status: not_started
   ```

2. In `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md`, after the step 01_02_03 YAML block, add step 01_02_04 and 01_02_05 blocks matching the YAML format used by existing steps. Include: step_number, name, description, phase, pipeline_section, manual_reference, dataset, question, method, predecessors, notebook_path, inputs, outputs, scientific_invariants_applied, gate.

**Verification:**
- STEP_STATUS.yaml contains 01_02_04 with `status: complete, completed_at: "2026-04-14"`
- STEP_STATUS.yaml contains 01_02_05 with `status: not_started`
- ROADMAP.md contains step 01_02_04 and 01_02_05 blocks

**File scope:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml`

---

### T02 — Create notebook skeleton with imports and setup

**Objective:** Create the 01_02_05 notebook with standard header, imports, DuckDB connection, JSON artifact loading, artifact directory setup, and the `sql_queries` accumulator dict.

**Instructions:**

1. Create `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py` with the jupytext header (matching existing notebooks in the same directory — `percent` format, `.venv` kernelspec).

2. Include the following cells in order:
   - Markdown header cell documenting Phase, Pipeline Section, Dataset, Question, Invariants applied (#6 reproducibility, #7 no magic numbers, #9 step scope), Predecessor (01_02_04), Step scope (visualization only), Type (read-only)
   - Imports cell:
     ```python
     import json
     from pathlib import Path

     import duckdb
     import matplotlib
     import matplotlib.pyplot as plt
     import numpy as np
     import pandas as pd

     from rts_predict.games.aoe2.config import AOESTATS_DB_FILE
     from rts_predict.common.notebook_utils import get_reports_dir, setup_notebook_logging
     ```
   - Setup cell:
     ```python
     matplotlib.rcParams["figure.dpi"] = 150
     con = duckdb.connect(str(AOESTATS_DB_FILE), read_only=True)
     reports_dir = get_reports_dir("aoe2", "aoestats")
     artifacts_dir = reports_dir / "artifacts" / "01_exploration" / "02_eda"
     census_path = artifacts_dir / "01_02_04_univariate_census.json"
     with open(census_path) as f:
         census = json.load(f)
     print(f"Census loaded: {len(census)} top-level keys")
     print(f"Keys: {sorted(census.keys())}")
     ```
   - SQL queries accumulator cell:
     ```python
     sql_queries: dict[str, str] = {}
     ```

**Verification:**
- File exists and has valid jupytext header
- Imports include json, duckdb, matplotlib, pandas, numpy
- Census JSON loaded into `census` variable
- `sql_queries` dict initialized

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T03 — Winner distribution bar chart

**Objective:** Plot 1. Bar chart of winner distribution (TRUE/FALSE) counts from players_raw.

**Instructions:**

1. Verification cell:
   ```python
   winner_data = census["winner_distribution"]
   winner_df = pd.DataFrame(winner_data)
   print("Winner distribution data:")
   print(winner_df.to_string(index=False))
   ```

2. Plot cell: vertical bar chart, `figsize=(10, 6)`. Color: TRUE=green, FALSE=red. Each bar annotated with count and pct. Title: "Winner Distribution (players_raw, N=107,627,584)". Derive N from `census["players_null_census"]["total_rows"]`, not hardcoded.

3. Save as `artifacts_dir / "01_02_05_winner_distribution.png"` at dpi=150.

4. Call `plt.close()` immediately after `plt.savefig(...)`.

**Verification:**
- PNG file `01_02_05_winner_distribution.png` exists and is non-empty
- Verification print cell precedes plot cell

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T04 — Num_players distribution bar chart

**Objective:** Plot 2. Vertical bar chart of match size distribution (1-8 players), highlighting even-count game dominance.

**Instructions:**

1. Verification cell:
   ```python
   npl_data = census["num_players_distribution"]
   npl_df = pd.DataFrame(npl_data)
   print("num_players distribution:")
   print(npl_df.to_string(index=False))
   ```

2. Plot cell: vertical bar chart, `figsize=(10, 6)`.
   - X-axis = num_players (1-8)
   - Each bar annotated with count and pct (derive from `npl_df["distinct_match_count"]` and `npl_df["pct"]`)
   - Color: even values (2, 4, 6, 8) = blue; odd values (1, 3, 5, 7) = gray
   - This highlights even-count game dominance: `[I7: 2p=60.56%, 4p=16.48%, 6p=8.92%, 8p=14.04% from census]`
   - Title: "Match Size Distribution (matches_raw, N=30,690,651)" — derive N from `census["matches_null_census"]["total_rows"]`

3. Save as `artifacts_dir / "01_02_05_num_players_distribution.png"` at dpi=150.

4. Call `plt.close()` immediately after `plt.savefig(...)`.

**Verification:**
- PNG file `01_02_05_num_players_distribution.png` exists and is non-empty
- Even-player bars are blue, odd-player bars are gray

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T05 — Map top-20 and Civ top-20 horizontal bar charts

**Objective:** Plots 3-4. Horizontal bar charts for top-20 maps and top-20 civilizations.

**Instructions:**

1. For map top-20:
   - Verification cell: load `census["categorical_matches"]["map"]["top_values"][:20]`, build DataFrame, print.
   - Plot: horizontal bar (barh), `figsize=(10, 8)`, sorted descending, annotated with pct. Title includes cardinality from `census["categorical_matches"]["map"]["cardinality"]`.
   - Save as `artifacts_dir / "01_02_05_map_top20.png"`.
   - Call `plt.close()`.

2. For civ top-20:
   - Verification cell: load `census["categorical_players"]["civ"]["top_values"][:20]`, build DataFrame, print.
   - Plot: horizontal bar (barh), `figsize=(10, 8)`, sorted descending, annotated with pct. Title includes cardinality from `census["categorical_players"]["civ"]["cardinality"]`.
   - Save as `artifacts_dir / "01_02_05_civ_top20.png"`.
   - Call `plt.close()`.

**Verification:**
- `01_02_05_map_top20.png` and `01_02_05_civ_top20.png` exist

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T06 — Leaderboard distribution bar chart

**Objective:** Plot 5. Horizontal bar chart of leaderboard distribution (4 values only).

**Instructions:**

1. Verification cell: load `census["categorical_matches"]["leaderboard"]["top_values"]`, build DataFrame, print.

2. Plot: horizontal bar (barh), `figsize=(10, 6)`. Each bar annotated with count and pct. Title: "Leaderboard Distribution (matches_raw, N=30,690,651)".

3. Save as `artifacts_dir / "01_02_05_leaderboard_distribution.png"`.

4. Call `plt.close()`.

**Verification:**
- `01_02_05_leaderboard_distribution.png` exists

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T07 — Duration histogram (dual-panel)

**Objective:** Plot 6. Dual-panel duration histogram. The extreme skewness (1032.64) and max/median ratio of ~2129x make a single panel at any scale uninformative. `[I7: skewness=1032.64 from census["skew_kurtosis_matches"][0]; max/median = 5,574,815s / 2619.7s ~ 2129x]`

**Instructions:**

1. Left panel SQL (body view, 1-minute bins, clipped at 120 min):
   ```sql
   SELECT FLOOR(duration / 1e9 / 60) AS minute_bin, COUNT(*) AS cnt
   FROM matches_raw
   WHERE duration IS NOT NULL AND duration / 1e9 / 60 <= 120
   GROUP BY minute_bin
   ORDER BY minute_bin
   ```
   Store in `sql_queries["hist_duration_body"]`.

2. Right panel SQL (full range, 10-minute bins, log y-scale):
   ```sql
   SELECT FLOOR(duration / 1e9 / 600) * 10 AS ten_min_bin, COUNT(*) AS cnt
   FROM matches_raw
   WHERE duration IS NOT NULL
   GROUP BY ten_min_bin
   ORDER BY ten_min_bin
   ```
   Store in `sql_queries["hist_duration_full_log"]`.

3. Verification cells: print first/last 5 bins for each query.

4. Plot: `figsize=(16, 5)`, 1x2 subplots.
   - **Left panel:** 1-minute bin bars, linear y-scale. Title: "Duration (body, <= 120 min)".
     Annotate: median = 43.7 min (vertical dashed line), p95 = 78.6 min (vertical dashed line).
     `[I7: median = census["numeric_stats_matches"][0]["median_val"] / 60 = 2619.7/60 = 43.66 min; p95 = census["numeric_stats_matches"][0]["p95"] / 60 = 4714.1/60 = 78.57 min]`
     Derive these values from the census artifact at runtime, not hardcoded.
   - **Right panel:** 10-minute bin bars, log y-scale. Title: "Duration (full range, log scale)".
     Annotate: "Skewness = 1032.64" and "irl_duration has identical distribution" as text.
     Derive skewness from `census["skew_kurtosis_matches"][0]["skewness"]`.

5. Save as `artifacts_dir / "01_02_05_duration_histogram.png"`.

6. Call `plt.close()`.

**Verification:**
- `01_02_05_duration_histogram.png` exists with two panels
- Left panel has linear y, right panel has log y
- Median and p95 dashed lines visible on left panel

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T08 — ELO distribution panels (1x3, sentinel excluded)

**Objective:** Plot 7. Three ELO histograms (avg_elo, team_0_elo, team_1_elo) in a single row. Sentinel values (-1.0) are excluded from team_0/1_elo bins because sentinel counts are negligible (34 and 39 out of 30.7M). `[I7: sentinel counts from census["elo_sentinel_counts"]: team_0=34, team_1=39; 34/30690651 = 0.00011%]`

**Instructions:**

1. For each ELO column, execute a binned histogram query with bin width 25 and sentinel exclusion for team_0/1_elo:
   - `avg_elo`:
     ```sql
     SELECT FLOOR(avg_elo / 25) * 25 AS bin, COUNT(*) AS cnt
     FROM matches_raw
     GROUP BY bin ORDER BY bin
     ```
     `[I7: actual max = 2976.5 from census; 2976.5/25 = ~119 bins]`
   - `team_0_elo`:
     ```sql
     SELECT FLOOR(team_0_elo / 25) * 25 AS bin, COUNT(*) AS cnt
     FROM matches_raw
     WHERE team_0_elo >= 0
     GROUP BY bin ORDER BY bin
     ```
     `[I7: actual max = 3038 from census; 3038/25 = ~122 bins]`
   - `team_1_elo`:
     ```sql
     SELECT FLOOR(team_1_elo / 25) * 25 AS bin, COUNT(*) AS cnt
     FROM matches_raw
     WHERE team_1_elo >= 0
     GROUP BY bin ORDER BY bin
     ```
     `[I7: actual max = 3045 from census; 3045/25 = ~122 bins]`

   Store all three in `sql_queries` dict with descriptive keys.

2. Verification cell: print first 5 bins of each.

3. Plot: 1x3 subplot grid, `figsize=(18, 5)`.
   - Each subplot: histogram bars, same x-axis range for comparability.
   - On team_0_elo and team_1_elo panels, annotate sentinel count: derive from `census["elo_sentinel_counts"]["team_0_elo_negative"]` and `census["elo_sentinel_counts"]["team_1_elo_negative"]` — do NOT hardcode 34/39.
   - Annotation text: "N={count} sentinel (-1.0) excluded".

4. Save as `artifacts_dir / "01_02_05_elo_distributions.png"`.

5. Call `plt.close()`.

**Verification:**
- `01_02_05_elo_distributions.png` exists with 1x3 grid
- Sentinel annotation present on team_0/1_elo panels
- No bar at x=-1.0 on team_0/1_elo panels

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T09 — old_rating histogram and match_rating_diff histogram (two separate plots)

**Objective:** Plots 8-9. Separate histograms for old_rating and match_rating_diff from players_raw. Split into two plots because these variables have fundamentally different shapes and scales.

**Instructions:**

1. **old_rating histogram:**
   - SQL query with bin width 25:
     ```sql
     SELECT FLOOR(old_rating / 25) * 25 AS bin, COUNT(*) AS cnt
     FROM players_raw
     GROUP BY bin ORDER BY bin
     ```
     `[I7: range 0-3045 from census; 3045/25 = ~122 bins]`
     Store in `sql_queries["hist_old_rating"]`.
   - Verification cell: print first 5 bins.
   - Plot: single histogram, `figsize=(10, 6)`.
     Annotate: median=1066, p05=665, p95=1580 (vertical dashed lines).
     `[I7: all values from census["numeric_stats_players"][0] where label="old_rating"]`
     Derive at runtime from census, not hardcoded.
   - Save as `artifacts_dir / "01_02_05_old_rating_histogram.png"`.
   - Call `plt.close()`.

2. **match_rating_diff histogram:**
   - SQL query with bin width 5, clipped view to [-200, +200]:
     ```sql
     SELECT FLOOR(match_rating_diff / 5) * 5 AS bin, COUNT(*) AS cnt
     FROM players_raw
     WHERE match_rating_diff IS NOT NULL
       AND match_rating_diff BETWEEN -200 AND 200
     GROUP BY bin ORDER BY bin
     ```
     `[I7: p05=-59, p95=+59 from census; clip to [-200, +200] to show leptokurtic shape while covering main body; full range is [-2185, +2185]]`
     Store in `sql_queries["hist_match_rating_diff"]`.
   - Verification cell: print first/last 5 bins.
   - Plot: single histogram, `figsize=(10, 6)`.
     Annotate:
     - Kurtosis=65.68 as text (derive from `census["skew_kurtosis_players"]` where label="match_rating_diff")
     - IQR fences at -68 and +68 as vertical dashed lines (derive from `census["outlier_counts_players"]` where label="match_rating_diff", fields `lower_fence` and `upper_fence`)
     - Text note: "Full range: [-2185, +2185]" (derive from census min/max)
   - Save as `artifacts_dir / "01_02_05_match_rating_diff_histogram.png"`.
   - Call `plt.close()`.

**Verification:**
- `01_02_05_old_rating_histogram.png` exists with annotated percentiles
- `01_02_05_match_rating_diff_histogram.png` exists with kurtosis annotation and IQR fences
- No values outside [-200, +200] visible in match_rating_diff plot

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T10 — Age uptime histograms (variable bin widths)

**Objective:** Plot 10. Three-panel age uptime distributions (feudal, castle, imperial) with variable bin widths calibrated to each age's effective range, producing ~42-43 bins per panel.

**Instructions:**

1. For each age, query non-NULL histogram bins with age-specific bin width:
   - **feudal_age_uptime:** bin width 10s
     ```sql
     SELECT FLOOR(feudal_age_uptime / 10) * 10 AS bin, COUNT(*) AS cnt
     FROM players_raw
     WHERE feudal_age_uptime IS NOT NULL
     GROUP BY bin ORDER BY bin
     ```
     `[I7: p05=535.1, p95=962.6 from census; effective body ~427s; 427/10 = 43 bins]`
     Store in `sql_queries["hist_feudal_age_uptime"]`.
   - **castle_age_uptime:** bin width 20s
     ```sql
     SELECT FLOOR(castle_age_uptime / 20) * 20 AS bin, COUNT(*) AS cnt
     FROM players_raw
     WHERE castle_age_uptime IS NOT NULL
     GROUP BY bin ORDER BY bin
     ```
     `[I7: p05=889.1, p95=1752.1 from census; effective body ~863s; 863/20 = 43 bins]`
     Store in `sql_queries["hist_castle_age_uptime"]`.
   - **imperial_age_uptime:** bin width 30s
     ```sql
     SELECT FLOOR(imperial_age_uptime / 30) * 30 AS bin, COUNT(*) AS cnt
     FROM players_raw
     WHERE imperial_age_uptime IS NOT NULL
     GROUP BY bin ORDER BY bin
     ```
     `[I7: p05=1681.1, p95=2933.0 from census; effective body ~1252s; 1252/30 = 42 bins]`
     Store in `sql_queries["hist_imperial_age_uptime"]`.

2. Verification cells: print first 5 bins of each.

3. Plot: 1x3 subplot, `figsize=(18, 5)`. Each subplot annotated with:
   - N (non-null count): derive from `census["numeric_stats_players"]` where label matches, field `n_nonnull`
   - null_pct: derive from `census["players_null_census"]["columns"]` where column matches
   - median: derive from census numeric stats
   - skewness: derive from `census["skew_kurtosis_players"]` where label matches
   All values derived from artifact at runtime — NOT hardcoded.

4. Save as `artifacts_dir / "01_02_05_age_uptime_histograms.png"`.

5. Call `plt.close()`.

**Verification:**
- `01_02_05_age_uptime_histograms.png` exists with 1x3 grid
- Each panel shows only non-NULL data
- Annotations show correct N, null_pct, median, skewness from census

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T11 — Opening non-NULL distribution bar chart

**Objective:** Plot 11. Bar chart of opening strategies among non-NULL rows only. This avoids the dominant NaN bar (86.05% NULL) that pollutes the existing top-k.

**Instructions:**

1. **Prerequisite gate** — verify the pass-2 key exists before using it:
   ```python
   assert "opening_nonnull_distribution" in census, (
       "BLOCKER: 'opening_nonnull_distribution' not found in census. "
       "Execute plan_aoestats_01_02_04_pass2 (T08) before running T11."
   )
   ```

2. Verification cell:
   ```python
   opening_dist = census["opening_nonnull_distribution"]
   opening_df = pd.DataFrame(opening_dist["values"])
   total_nonnull = opening_dist["total_nonnull"]
   print(f"Opening non-NULL distribution: N={total_nonnull:,}")
   print(opening_df.to_string(index=False))
   ```

3. Plot: horizontal bar (barh), `figsize=(10, 6)`. Title annotates total non-NULL count and 86% NULL note: "Opening Strategy (non-NULL only, N=15,011,294; 86.05% NULL excluded)" — derive N and null_pct from census.

4. Save as `artifacts_dir / "01_02_05_opening_nonnull.png"`.

5. Call `plt.close()`.

**Verification:**
- `01_02_05_opening_nonnull.png` exists
- No NaN/NULL bar in the chart
- Title contains non-NULL count

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T12 — IQR outlier summary bar chart

**Objective:** Plot 12. Horizontal bar chart showing outlier_pct per column, color-coded by table, high-NULL columns annotated.

**Instructions:**

1. Verification cell: build a DataFrame from `census["outlier_counts_matches"]` and `census["outlier_counts_players"]`. Add a `table` column ("matches_raw" or "players_raw"). Sort by outlier_pct ascending. Print.

2. Plot: horizontal bar (barh), `figsize=(12, 7)`. Blue for matches_raw, orange for players_raw.
   Mark "*high NULL" annotation on feudal/castle/imperial_age_uptime columns (red text).
   Add legend for table color.

3. Save as `artifacts_dir / "01_02_05_iqr_outlier_summary.png"`.

4. Call `plt.close()`.

**Verification:**
- `01_02_05_iqr_outlier_summary.png` exists
- Bars color-coded by table with legend

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T13 — NULL rate bar chart for all 32 columns

**Objective:** Plot 13. Horizontal bar chart sorted by null_pct descending, color-coded by severity.

**Instructions:**

1. Verification cell: build a DataFrame from `census["matches_null_census"]["columns"]` (prefixed "m.") and `census["players_null_census"]["columns"]` (prefixed "p."). Sort by null_pct descending. Print.

2. Plot: horizontal bar (barh), `figsize=(12, 8)`. Color per severity function:
   - >= 50% null: red
   - 5-50% null: orange
   - > 0 and < 5%: yellow
   - 0%: green
   Legend for severity buckets.

3. Save as `artifacts_dir / "01_02_05_null_rate_bar.png"`.

4. Call `plt.close()`.

**Verification:**
- `01_02_05_null_rate_bar.png` exists with 32 bars (18 matches + 14 players)
- High-NULL columns colored red

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T14 — Monthly match count time series

**Objective:** Plot 14 (but saved as the last content plot). Line plot of match volume over time with mean annotation.

**Instructions:**

1. Query:
   ```sql
   SELECT DATE_TRUNC('month', started_timestamp) AS month, COUNT(*) AS match_count
   FROM matches_raw WHERE started_timestamp IS NOT NULL
   GROUP BY month ORDER BY month
   ```
   Store in `sql_queries["monthly_match_counts"]`.

2. Verification cell: print all months. Assert row count matches census:
   ```python
   monthly_df = con.sql(sql_queries["monthly_match_counts"]).df()
   assert len(monthly_df) == census["temporal_range"]["distinct_months"], (
       f"Expected {census['temporal_range']['distinct_months']} months, got {len(monthly_df)}"
   )
   print(monthly_df.to_string())
   ```

3. Plot: `figsize=(14, 6)`, line plot with `marker="o"`. Mean dashed line annotated. X labels rotated 45 degrees.

4. Save as `artifacts_dir / "01_02_05_monthly_match_count.png"`.

5. Call `plt.close()`.

**Verification:**
- `01_02_05_monthly_match_count.png` exists
- 42 data points (matching `census["temporal_range"]["distinct_months"]`)

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T15 — Artifact writing, connection close, and notebook execution

**Objective:** Write the visualizations.md index artifact (plot index table + all SQL queries per Invariant #6), close the connection, and execute the full notebook with extended timeout.

**Instructions:**

1. Build markdown artifact with: header, plot index table (13 rows for 13 PNG files), SQL queries section (all entries from `sql_queries` dict as fenced code blocks). The `sql_queries` dict has been populated by T07, T08, T09, T10, T14 throughout the notebook.

2. Write to `artifacts_dir / "01_02_05_visualizations.md"`.

3. Close connection: `con.close()`.

4. Execute notebook with extended timeout (aoestats has 30M matches + 107M players rows; 45GB DB memory footprint):
   ```bash
   source .venv/bin/activate && poetry run jupytext --execute sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py --to notebook --output sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.ipynb --ExecutePreprocessor.timeout=1800
   ```

5. Verify all 13 PNG files exist in the artifacts directory:
   ```
   01_02_05_winner_distribution.png
   01_02_05_num_players_distribution.png
   01_02_05_map_top20.png
   01_02_05_civ_top20.png
   01_02_05_leaderboard_distribution.png
   01_02_05_duration_histogram.png
   01_02_05_elo_distributions.png
   01_02_05_old_rating_histogram.png
   01_02_05_match_rating_diff_histogram.png
   01_02_05_age_uptime_histograms.png
   01_02_05_opening_nonnull.png
   01_02_05_iqr_outlier_summary.png
   01_02_05_null_rate_bar.png
   ```
   Plus 1 time series:
   ```
   01_02_05_monthly_match_count.png
   ```
   Total: 13 PNG files (the monthly match count is an additional content plot but 13 distinct PNG artifacts above cover the univariate census visualization scope; the monthly match count is the 14th if we count it separately but it is plot 14 in the notebook yielding a total of 14 PNG files).

   **Correction:** The total is **14 PNG files** (13 univariate + 1 temporal). Enumerate all:
   1. `01_02_05_winner_distribution.png`
   2. `01_02_05_num_players_distribution.png`
   3. `01_02_05_map_top20.png`
   4. `01_02_05_civ_top20.png`
   5. `01_02_05_leaderboard_distribution.png`
   6. `01_02_05_duration_histogram.png`
   7. `01_02_05_elo_distributions.png`
   8. `01_02_05_old_rating_histogram.png`
   9. `01_02_05_match_rating_diff_histogram.png`
   10. `01_02_05_age_uptime_histograms.png`
   11. `01_02_05_opening_nonnull.png`
   12. `01_02_05_iqr_outlier_summary.png`
   13. `01_02_05_null_rate_bar.png`
   14. `01_02_05_monthly_match_count.png`

6. Update STEP_STATUS.yaml: change 01_02_05 status from `not_started` to `complete`, add `completed_at: <date>`.

**Verification:**
- All 14 PNG files exist and are non-empty
- `01_02_05_visualizations.md` exists with plot index table and all SQL queries
- Both .py and .ipynb are committed and in sync
- Notebook executes without errors

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.ipynb`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_visualizations.md`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_*.png` (14 files)
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml`

## File Manifest

| File | Action |
|------|--------|
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` | Update |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml` | Update |
| `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.ipynb` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_visualizations.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_winner_distribution.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_num_players_distribution.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_map_top20.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_civ_top20.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_leaderboard_distribution.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_duration_histogram.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_elo_distributions.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_old_rating_histogram.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_match_rating_diff_histogram.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_age_uptime_histograms.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_opening_nonnull.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_iqr_outlier_summary.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_null_rate_bar.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_monthly_match_count.png` | Create |

## Gate Condition

- All 14 PNG files exist and are non-empty
- `01_02_05_visualizations.md` exists with complete plot index and all SQL queries (Invariant #6)
- ROADMAP.md contains step 01_02_04 and 01_02_05 definitions
- STEP_STATUS.yaml contains step 01_02_04 with status complete
- STEP_STATUS.yaml contains step 01_02_05 with status complete after execution
- Notebook executes end-to-end without errors (with `--ExecutePreprocessor.timeout=1800`)
- Every plot cell has an immediately preceding print/display verification cell
- Every plot cell calls `plt.close()` after `plt.savefig(...)`
- Every SQL query that produces plotted data is stored in `sql_queries` dict and appears in the markdown artifact
- Both .py and .ipynb files committed and in sync

## Out of Scope

- **Bivariate and multivariate plots:** deferred to 01_02_06 or later
- **Research log entries:** deferred until notebooks polished
- **Field classification updates:** deferred, no source documentation
- **Thesis-quality figure formatting:** current plots are EDA-grade
- **KDE overlays:** deferred to 01_03

## Open Questions

- Whether the 01_02_04 pass-2 JSON artifact will contain `opening_nonnull_distribution` at execution time — T11 reads this key. Resolves by: executing pass-2 plan first.

## Deferred Debt

| Item | Target Step | Rationale |
|------|-------------|-----------|
| Bivariate plots (winner by civ, winner by map) | 01_02_06+ | Bivariate analysis belongs to next EDA layer |
| KDE overlays | 01_03 | More informative for group comparisons |
| Thesis-quality figure formatting | Thesis writing phase | EDA plots are exploratory; final figures regenerated |

---

For Category A, adversarial critique is required before execution. Dispatch reviewer-adversarial to produce `planning/current_plan.critique.md`.
