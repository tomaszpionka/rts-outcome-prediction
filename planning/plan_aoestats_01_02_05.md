---
category: A
branch: feat/census-pass3
date: 2026-04-15
planner_model: claude-opus-4-6
dataset: aoestats
phase: "01"
pipeline_section: "01_02 — Exploratory Data Analysis (Tukey-style)"
invariants_touched: [I3, I6, I7, I9]
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

# Plan: aoestats 01_02_05 — Univariate Visualizations (revision 2)

Revision of the original plan incorporating all BLOCKER and WARNING fixes from
the adversarial pre-execution audit dated 2026-04-15.

## Part A — ROADMAP Patch Specification

All changes target the Step 01_02_05 YAML block in
`src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md`
(lines ~340-397 of current file).

### A.1 — `description` field

Replace the current description with:

```
"Produce all EDA plots based on quantitative findings from Step 01_02_04. Fourteen visualization groups covering target distribution, match size, categorical top-k, duration dual-panel, ELO panels (sentinel-excluded), old_rating, match_rating_diff (LEAKAGE UNRESOLVED annotation mandatory), age uptime histograms (IN-GAME annotation mandatory), opening non-NULL (IN-GAME annotation mandatory), IQR outlier summary, NULL rate summary, and monthly match volume. Dead constant fields not visualized: game_type (cardinality=1), game_speed (cardinality=1), starting_age (cardinality=2 but 99.99%+ 'dark' with only 19 exception rows — effectively dead). Every plot of a post-game or in-game column carries a visible temporal classification annotation per Invariant #3. All SQL queries stored in sql_queries dict and written to markdown artifact per Invariant #6."
```

### A.2 — `outputs` field

Replace `data_artifacts` list. All PNGs use `plots/` subdirectory:

```yaml
outputs:
  data_artifacts:
    - "artifacts/01_exploration/02_eda/plots/01_02_05_winner_distribution.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_num_players_distribution.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_map_top20.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_civ_top20.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_leaderboard_distribution.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_duration_histogram.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_elo_distributions.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_old_rating_histogram.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_match_rating_diff_histogram.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_age_uptime_histograms.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_opening_nonnull.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_iqr_outlier_summary.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_null_rate_bar.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_monthly_match_count.png"
  report: "artifacts/01_exploration/02_eda/01_02_05_visualizations.md"
```

### A.3 — `scientific_invariants_applied` field

Replace with (adds I3):

```yaml
scientific_invariants_applied:
  - number: "3"
    how_upheld: "Every plot of a post-game or in-game column carries a visible temporal classification annotation. match_rating_diff annotated 'LEAKAGE STATUS UNRESOLVED — do not use as feature until verified' per research log 01_02_04 deferred decision. opening and age uptimes annotated 'IN-GAME — not available at prediction time'. duration annotated 'POST-GAME — observed only after match ends'."
  - number: "6"
    how_upheld: "All SQL queries that produce plotted data stored in sql_queries dict and appear verbatim in the markdown artifact."
  - number: "7"
    how_upheld: "All bin widths, clip boundaries, and annotation values derived from census artifact at runtime — no hardcoded numbers."
  - number: "9"
    how_upheld: "Read-only step — visualization only; no analytical computation beyond what is needed for plotting."
```

### A.4 — `gate` field

Replace with:

```yaml
gate:
  artifact_check: "All 14 PNG files under artifacts/01_exploration/02_eda/plots/ and 01_02_05_visualizations.md exist and are non-empty."
  continue_predicate: "All 14 PNG files exist under plots/ subdirectory. Markdown artifact contains plot index table and all SQL queries. match_rating_diff plot carries LEAKAGE UNRESOLVED annotation. opening and age uptime plots carry IN-GAME annotation. duration plot carries POST-GAME annotation. Notebook executes end-to-end without errors."
  halt_predicate: "Any PNG file is missing, or any temporal classification annotation is absent on in-game/post-game/unresolved columns, or notebook execution fails."
```

### A.5 — No other fields change

`step_number`, `name`, `phase`, `pipeline_section`, `manual_reference`,
`dataset`, `question`, `method`, `stratification`, `predecessors`,
`notebook_path`, `inputs`, `reproducibility`, `thesis_mapping`,
`research_log_entry` remain as-is.


## Part B — Notebook Task List

### Notebook path

`sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

### Artifact output directory

`reports_dir / "artifacts" / "01_exploration" / "02_eda" / "plots"` — create
this `plots/` subdirectory in setup. The markdown artifact goes to the parent
(`artifacts/01_exploration/02_eda/01_02_05_visualizations.md`).

---

### T01 — ROADMAP patch

**Objective:** Apply all Part A changes to the ROADMAP.md Step 01_02_05 entry.

**Instructions:**

1. Open `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md`.
2. Locate the Step 01_02_05 YAML block.
3. Apply changes A.1 through A.4 exactly as specified in Part A above.
4. Confirm no other steps are modified.

**Verification:**
- ROADMAP.md Step 01_02_05 `description` mentions starting_age as effectively dead
- ROADMAP.md Step 01_02_05 `outputs` list all 14 PNGs under `plots/` subdir
- ROADMAP.md Step 01_02_05 `scientific_invariants_applied` includes I3 with match_rating_diff leakage note
- ROADMAP.md Step 01_02_05 `gate` references temporal classification annotations

**File scope:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md`

---

### T02 — Create notebook skeleton with imports and setup

**Objective:** Create the 01_02_05 notebook with standard header, imports,
DuckDB connection, JSON artifact loading, `plots/` directory creation, and the
`sql_queries` accumulator dict.

**Instructions:**

1. Create `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`
   with the jupytext header (`percent` format, `.venv` kernelspec) matching
   existing notebooks in the same directory.

2. Markdown header cell:
   - Step: 01_02_05 — Univariate Visualizations
   - Phase: 01 — Data Exploration
   - Pipeline Section: 01_02 — EDA (Tukey-style)
   - Dataset: aoestats
   - Predecessor: 01_02_04 (Univariate Census)
   - Invariants: #3 (temporal classification annotations), #6 (SQL reproducibility), #7 (no magic numbers), #9 (read-only scope)
   - Step scope: visualization only — read-only DB access, no analytical computation

3. Imports cell:
   ```python
   import json
   from pathlib import Path

   import duckdb
   import matplotlib
   import matplotlib.pyplot as plt
   import numpy as np
   import pandas as pd

   from rts_predict.games.aoe2.config import AOESTATS_DB_FILE
   from rts_predict.common.notebook_utils import get_reports_dir
   ```

4. Setup cell:
   ```python
   matplotlib.rcParams["figure.dpi"] = 150
   con = duckdb.connect(str(AOESTATS_DB_FILE), read_only=True)
   reports_dir = get_reports_dir("aoe2", "aoestats")
   artifacts_dir = reports_dir / "artifacts" / "01_exploration" / "02_eda"
   plots_dir = artifacts_dir / "plots"
   plots_dir.mkdir(parents=True, exist_ok=True)
   census_path = artifacts_dir / "01_02_04_univariate_census.json"
   with open(census_path) as f:
       census = json.load(f)
   print(f"Census loaded: {len(census)} top-level keys")
   print(f"Keys: {sorted(census.keys())}")
   ```

5. SQL queries accumulator cell:
   ```python
   sql_queries: dict[str, str] = {}
   ```

**Verification:**
- File exists with valid jupytext header
- `plots_dir` variable points to `artifacts/01_exploration/02_eda/plots/`
- Census JSON loaded into `census` variable
- `sql_queries` dict initialized

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T03 — Winner distribution bar chart

**Objective:** Target variable distribution plot. Must be visually comparable
across all three datasets (sc2egset, aoe2companion, aoestats). Show Win/Loss
as 2 bars with total N annotated. This addresses WARNING #6 (thesis
comparability) and cross-dataset constraint #7a.

**Instructions:**

1. Verification cell:
   ```python
   winner_data = census["winner_distribution"]
   winner_df = pd.DataFrame(winner_data)
   total_n = census["players_null_census"]["total_rows"]
   print(f"Winner distribution (N={total_n:,}):")
   print(winner_df.to_string(index=False))
   ```

2. Plot cell: vertical bar chart, `figsize=(10, 6)`.
   - 2 bars: Win (winner=True) and Loss (winner=False).
   - Colors: Win=steelblue, Loss=salmon.
   - Each bar annotated with count and pct.
   - Title: `f"Target Variable: Winner Distribution (players_raw, N={total_n:,})"`.
   - Derive N from `census["players_null_census"]["total_rows"]`, not hardcoded.

3. Save to `plots_dir / "01_02_05_winner_distribution.png"` at dpi=150.
4. `plt.close()`.

**Verification:**
- PNG exists and is non-empty
- Chart shows exactly 2 bars (Win, Loss) with total N in title

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T04 — Num_players distribution bar chart

**Objective:** Match size distribution. Cross-dataset constraint #7 does not
require this for all datasets, but it documents the 1v1 majority share.

**Instructions:**

1. Verification cell: load `census["num_players_distribution"]`, build DataFrame, print.

2. Plot: vertical bar chart, `figsize=(10, 6)`.
   - X-axis = num_players (1-8).
   - Each bar annotated with count and pct.
   - Color: even values (2, 4, 6, 8) = steelblue; odd values (1, 3, 5, 7) = lightgray.
   - Title: `f"Match Size Distribution (matches_raw, N={matches_total:,})"` where
     `matches_total = census["matches_null_census"]["total_rows"]`.

3. Save to `plots_dir / "01_02_05_num_players_distribution.png"` at dpi=150.
4. `plt.close()`.

**Verification:**
- PNG exists with 8 bars

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T05 — Map top-20 and Civ top-20 horizontal bar charts

**Objective:** Two categorical top-k bar charts. Map top-20 is a cross-dataset
mandatory plot (constraint #7b).

**Instructions:**

1. **Map top-20:**
   - Verification cell: load `census["categorical_matches"]["map"]["top_values"][:20]`, build DataFrame, print.
   - Plot: horizontal barh, `figsize=(10, 8)`, sorted descending (highest at top), annotated with pct.
   - Title includes cardinality: `f"Top 20 Maps (matches_raw, {cardinality} total, N={matches_total:,})"`.
   - Save to `plots_dir / "01_02_05_map_top20.png"`.
   - `plt.close()`.

2. **Civ top-20:**
   - Verification cell: load `census["categorical_players"]["civ"]["top_values"][:20]`, build DataFrame, print.
   - Plot: horizontal barh, `figsize=(10, 8)`, sorted descending, annotated with pct.
   - Title includes cardinality: `f"Top 20 Civilizations (players_raw, {cardinality} total, N={players_total:,})"`.
   - Save to `plots_dir / "01_02_05_civ_top20.png"`.
   - `plt.close()`.

**Verification:**
- Both PNGs exist

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T06 — Leaderboard distribution bar chart

**Objective:** Leaderboard type distribution (4 values).

**Instructions:**

1. Verification cell: load `census["categorical_matches"]["leaderboard"]["top_values"]`, build DataFrame, print.

2. Plot: horizontal barh, `figsize=(10, 6)`. Each bar annotated with count and pct.
   Title: `f"Leaderboard Distribution (matches_raw, N={matches_total:,})"`.

3. Save to `plots_dir / "01_02_05_leaderboard_distribution.png"`.
4. `plt.close()`.

**Verification:**
- PNG exists

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T07 — Duration histogram (dual-panel) — POST-GAME annotation

**Objective:** Duration distribution. This is a **post-game** column (game
duration is only known after the match ends). The plot must carry the
annotation: **"POST-GAME — observed only after match ends"** as a figure
suptitle. Cross-dataset constraint #7c (match duration histogram).

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

3. Verification cells: execute both, print first/last 5 bins.

4. Plot: `figsize=(16, 6)`, 1x2 subplots.
   - **fig.suptitle**: `"POST-GAME — observed only after match ends"`, fontsize=11, color="red", fontstyle="italic".
   - **Left panel:** 1-minute bin bars, linear y-scale.
     Title: "Duration (body, <= 120 min)".
     Vertical dashed lines: median and p95.
     Derive from census: `census["numeric_stats_matches"]` where label="duration_sec":
     median = `median_val / 60`, p95 = `p95 / 60`.
   - **Right panel:** 10-minute bin bars, log y-scale.
     Title: "Duration (full range, log scale)".
     Text annotation: skewness value from `census["skew_kurtosis_matches"]` where index 0 (duration_sec).

5. Save to `plots_dir / "01_02_05_duration_histogram.png"`.
6. `plt.close()`.

**Invariant notes:** I3 — duration is post-game, annotation required. I7 — all
bin widths and reference lines derived from census.

**Verification:**
- PNG exists with two panels
- Red POST-GAME suptitle is visible

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T08 — ELO distribution panels (1x3, sentinel excluded)

**Objective:** Three ELO histograms (avg_elo, team_0_elo, team_1_elo).
Cross-dataset constraint #7d (rating/ELO histogram). These are pre-game
columns — no temporal annotation needed.

**Instructions:**

1. For each ELO column, SQL query with bin width 25, sentinel exclusion for
   team_0/1_elo (WHERE >= 0):
   - `avg_elo`:
     ```sql
     SELECT FLOOR(avg_elo / 25) * 25 AS bin, COUNT(*) AS cnt
     FROM matches_raw
     GROUP BY bin ORDER BY bin
     ```
   - `team_0_elo`:
     ```sql
     SELECT FLOOR(team_0_elo / 25) * 25 AS bin, COUNT(*) AS cnt
     FROM matches_raw WHERE team_0_elo >= 0
     GROUP BY bin ORDER BY bin
     ```
   - `team_1_elo`:
     ```sql
     SELECT FLOOR(team_1_elo / 25) * 25 AS bin, COUNT(*) AS cnt
     FROM matches_raw WHERE team_1_elo >= 0
     GROUP BY bin ORDER BY bin
     ```
   Store all three in `sql_queries` with descriptive keys.

2. Verification cell: print first 5 bins of each.

3. Plot: 1x3 subplot, `figsize=(18, 5)`.
   - Same x-axis range across all three.
   - team_0_elo and team_1_elo panels: annotate sentinel count from
     `census["elo_sentinel_counts"]["team_0_elo_negative"]` and
     `census["elo_sentinel_counts"]["team_1_elo_negative"]`.
     Text: `f"N={count} sentinel (-1.0) excluded"`.

4. Save to `plots_dir / "01_02_05_elo_distributions.png"`.
5. `plt.close()`.

**Invariant notes:** I7 — sentinel counts from census, not hardcoded.

**Verification:**
- PNG exists with 1x3 grid
- Sentinel annotation present on team_0/1_elo panels

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T09 — old_rating histogram (pre-game)

**Objective:** Pre-game rating distribution. No temporal annotation needed —
old_rating is the pre-game rating column.

**Instructions:**

1. SQL query with bin width 25:
   ```sql
   SELECT FLOOR(old_rating / 25) * 25 AS bin, COUNT(*) AS cnt
   FROM players_raw
   GROUP BY bin ORDER BY bin
   ```
   Store in `sql_queries["hist_old_rating"]`.

2. Verification cell: print first 5 bins.

3. Plot: single histogram, `figsize=(10, 6)`.
   Vertical dashed lines: median, p05, p95. Derive from
   `census["numeric_stats_players"]` where label="old_rating".
   Title: `f"old_rating Distribution (players_raw, N={n:,})"`.

4. Save to `plots_dir / "01_02_05_old_rating_histogram.png"`.
5. `plt.close()`.

**Verification:**
- PNG exists with percentile annotations

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T10 — match_rating_diff histogram — LEAKAGE UNRESOLVED annotation

**Objective:** Histogram of match_rating_diff. This column's temporal
classification is **unresolved** — it could be (new_rating - old_rating) =
post-game leakage, or (player_elo - opponent_elo) = pre-game feature. The
verification query `SELECT COUNT(*) FROM players_raw WHERE ABS(match_rating_diff - (new_rating - old_rating)) < 0.01` is documented in research log 01_02_04
but has not yet been executed. The plot MUST carry the annotation:

**"LEAKAGE STATUS UNRESOLVED -- do not use as feature until verified (see research log 01_02_04)"**

This addresses BLOCKER #1 and BLOCKER #3.

**Instructions:**

1. SQL query with bin width 5, clipped to [-200, +200]:
   ```sql
   SELECT FLOOR(match_rating_diff / 5) * 5 AS bin, COUNT(*) AS cnt
   FROM players_raw
   WHERE match_rating_diff IS NOT NULL
     AND match_rating_diff BETWEEN -200 AND 200
   GROUP BY bin ORDER BY bin
   ```
   Store in `sql_queries["hist_match_rating_diff"]`.

2. Verification cell: print first/last 5 bins.

3. Plot: single histogram, `figsize=(10, 6)`.
   - **fig.suptitle**: `"LEAKAGE STATUS UNRESOLVED -- do not use as feature until verified"`, fontsize=11, color="red", fontstyle="italic".
   - Title: `f"match_rating_diff Distribution (clipped [-200, +200], N={n:,})"`.
   - Kurtosis annotation: derive from `census["skew_kurtosis_players"]` where label="match_rating_diff".
   - IQR fences as vertical dashed lines: derive from `census["outlier_counts_players"]` where label="match_rating_diff".
   - Text: `f"Full range: [{min_val}, {max_val}]"` from census numeric stats.

4. Save to `plots_dir / "01_02_05_match_rating_diff_histogram.png"`.
5. `plt.close()`.

**Invariant notes:** I3 — leakage unresolved, mandatory annotation. I7 — all
values from census.

**Verification:**
- PNG exists with red LEAKAGE UNRESOLVED suptitle
- Kurtosis and IQR fences visible

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T11 — Age uptime histograms (1x3) — IN-GAME annotation

**Objective:** Three-panel age uptime distributions. These are **in-game**
columns — they record timestamps during gameplay and are not available at
prediction time. The plot MUST carry the annotation:

**"IN-GAME -- not available at prediction time"**

This addresses BLOCKER #1.

**Instructions:**

1. For each age, SQL query with variable bin widths:
   - **feudal_age_uptime** (bin=10s):
     ```sql
     SELECT FLOOR(feudal_age_uptime / 10) * 10 AS bin, COUNT(*) AS cnt
     FROM players_raw WHERE feudal_age_uptime IS NOT NULL
     GROUP BY bin ORDER BY bin
     ```
     `[I7: p05=535.1, p95=962.6; body ~427s; 427/10 = 43 bins]`
   - **castle_age_uptime** (bin=20s):
     ```sql
     SELECT FLOOR(castle_age_uptime / 20) * 20 AS bin, COUNT(*) AS cnt
     FROM players_raw WHERE castle_age_uptime IS NOT NULL
     GROUP BY bin ORDER BY bin
     ```
     `[I7: p05=889.1, p95=1752.1; body ~863s; 863/20 = 43 bins]`
   - **imperial_age_uptime** (bin=30s):
     ```sql
     SELECT FLOOR(imperial_age_uptime / 30) * 30 AS bin, COUNT(*) AS cnt
     FROM players_raw WHERE imperial_age_uptime IS NOT NULL
     GROUP BY bin ORDER BY bin
     ```
     `[I7: p05=1681.1, p95=2933.0; body ~1252s; 1252/30 = 42 bins]`
   Store all three in `sql_queries`.

2. Verification cells: print first 5 bins of each.

3. Plot: 1x3 subplot, `figsize=(18, 6)`.
   - **fig.suptitle**: `"IN-GAME -- not available at prediction time"`, fontsize=11, color="red", fontstyle="italic".
   - Each subplot annotated with: N (non-null count), null_pct, median, skewness.
     All from census artifact at runtime.

4. Save to `plots_dir / "01_02_05_age_uptime_histograms.png"`.
5. `plt.close()`.

**Invariant notes:** I3 — in-game columns, annotation mandatory. I7 — bin
widths justified by p05/p95 ranges.

**Verification:**
- PNG exists with 1x3 grid
- Red IN-GAME suptitle visible

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T12 — Opening non-NULL distribution bar chart — IN-GAME annotation

**Objective:** Opening strategy distribution among non-NULL rows only (86.05%
NULL excluded). This is an **in-game** column. The plot MUST carry the
annotation:

**"IN-GAME -- not available at prediction time"**

This addresses BLOCKER #1.

**Instructions:**

1. Prerequisite gate:
   ```python
   assert "opening_nonnull_distribution" in census, (
       "BLOCKER: 'opening_nonnull_distribution' not in census."
   )
   ```

2. Verification cell: load `census["opening_nonnull_distribution"]`, build DataFrame, print.

3. Plot: horizontal barh, `figsize=(10, 6)`.
   - **fig.suptitle**: `"IN-GAME -- not available at prediction time"`, fontsize=11, color="red", fontstyle="italic".
   - Title: `f"Opening Strategy (non-NULL only, N={total_nonnull:,}; {null_pct}% NULL excluded)"`.
     Derive total_nonnull from `census["opening_nonnull_distribution"]["total_nonnull"]`.
     Derive null_pct from `census["players_null_census"]["columns"]` where column="opening".

4. Save to `plots_dir / "01_02_05_opening_nonnull.png"`.
5. `plt.close()`.

**Invariant notes:** I3 — in-game, annotation mandatory. I7 — N and null_pct
from census.

**Verification:**
- PNG exists with IN-GAME suptitle
- No NULL/NaN bar in chart

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T13 — IQR outlier summary bar chart

**Objective:** Horizontal bar chart of outlier_pct per numeric column, color-coded by table.

**Instructions:**

1. Verification cell: build DataFrame from `census["outlier_counts_matches"]`
   and `census["outlier_counts_players"]`. Add `table` column. Sort by
   outlier_pct ascending. Print.

2. Plot: horizontal barh, `figsize=(12, 7)`. Blue for matches_raw, orange for players_raw.
   Annotate "*high NULL" in red text on feudal/castle/imperial_age_uptime bars.
   Add legend for table color.

3. Save to `plots_dir / "01_02_05_iqr_outlier_summary.png"`.
4. `plt.close()`.

**Verification:**
- PNG exists with color-coded bars and legend

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T14 — NULL rate bar chart for all 32 columns

**Objective:** Horizontal bar chart sorted by null_pct descending, color-coded
by severity. Thresholds harmonized with aoe2companion per WARNING #4:
green=0%, yellow=>0 and <5%, orange=5-50%, red>=50%.

**Instructions:**

1. Verification cell: build DataFrame from
   `census["matches_null_census"]["columns"]` (prefix "m.") and
   `census["players_null_census"]["columns"]` (prefix "p."). Sort by null_pct
   descending. Print.

2. Plot: horizontal barh, `figsize=(12, 8)`. Color per severity:
   - 0%: green
   - >0% and <5%: yellow
   - 5% to <50%: orange
   - >=50%: red
   Add legend for severity buckets.

3. Save to `plots_dir / "01_02_05_null_rate_bar.png"`.
4. `plt.close()`.

**Invariant notes:** I7 — thresholds are the cross-dataset standard (also
used by aoe2companion), not arbitrary.

**Verification:**
- PNG exists with 32 bars (18 matches + 14 players)
- High-NULL columns (opening, feudal/castle/imperial_age_uptime) colored red

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T15 — Monthly match count time series

**Objective:** Line plot of match volume over time. No temporal annotation
needed — started_timestamp is a pre-game field.

**Instructions:**

1. SQL query:
   ```sql
   SELECT DATE_TRUNC('month', started_timestamp) AS month, COUNT(*) AS match_count
   FROM matches_raw WHERE started_timestamp IS NOT NULL
   GROUP BY month ORDER BY month
   ```
   Store in `sql_queries["monthly_match_counts"]`.

2. Verification cell: execute query, assert row count matches
   `census["temporal_range"]["distinct_months"]` (expected: 42):
   ```python
   monthly_df = con.sql(sql_queries["monthly_match_counts"]).df()
   assert len(monthly_df) == census["temporal_range"]["distinct_months"], (
       f"Expected {census['temporal_range']['distinct_months']} months, got {len(monthly_df)}"
   )
   print(monthly_df.to_string())
   ```

3. Plot: `figsize=(14, 6)`, line plot with `marker="o"`. Mean dashed horizontal
   line annotated. X labels rotated 45 degrees.
   Title: `f"Monthly Match Volume (matches_raw, N={matches_total:,})"`.

4. Save to `plots_dir / "01_02_05_monthly_match_count.png"`.
5. `plt.close()`.

**Verification:**
- PNG exists
- 42 data points (matching census temporal_range distinct_months)

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T16 — Artifact writing, connection close, STEP_STATUS update

**Objective:** Write the 01_02_05_visualizations.md artifact (plot index + all
SQL queries per Invariant #6), close DB connection, execute notebook, update
STEP_STATUS.

**Instructions:**

1. Build markdown artifact with:
   - Header (step, date, dataset)
   - Plot index table: 14 rows, columns: Plot #, Filename, Description,
     Temporal Annotation. The temporal annotation column must state one of:
     "PRE-GAME", "POST-GAME", "IN-GAME", "LEAKAGE UNRESOLVED", or "N/A" for
     each plot. Specifically:
     - winner_distribution: N/A (target variable)
     - num_players_distribution: PRE-GAME
     - map_top20: PRE-GAME
     - civ_top20: PRE-GAME
     - leaderboard_distribution: PRE-GAME
     - duration_histogram: POST-GAME
     - elo_distributions: PRE-GAME
     - old_rating_histogram: PRE-GAME
     - match_rating_diff_histogram: LEAKAGE UNRESOLVED
     - age_uptime_histograms: IN-GAME
     - opening_nonnull: IN-GAME
     - iqr_outlier_summary: N/A (meta-summary)
     - null_rate_bar: N/A (meta-summary)
     - monthly_match_count: PRE-GAME
   - SQL queries section: all entries from `sql_queries` dict as fenced code blocks.

2. Write to `artifacts_dir / "01_02_05_visualizations.md"`.

3. Close connection: `con.close()`.

4. Execute notebook:
   ```bash
   source .venv/bin/activate && poetry run jupytext --execute sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py --to notebook --output sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.ipynb --ExecutePreprocessor.timeout=1800
   ```

5. Verify all 14 PNGs exist in `plots/`:
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
   01_02_05_monthly_match_count.png
   ```

6. Update `src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml`:
   change 01_02_05 status from `not_started` to `complete`, add
   `completed_at: <date>`.

**Verification:**
- All 14 PNGs exist and are non-empty under `plots/`
- `01_02_05_visualizations.md` exists with plot index table (including temporal
  annotation column) and all SQL queries
- Notebook executes without errors

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py`
- `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.ipynb`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_visualizations.md`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml`


## Gate Condition Checklist

- [ ] All 14 PNG files exist under `artifacts/01_exploration/02_eda/plots/` and are non-empty
- [ ] `01_02_05_visualizations.md` exists with plot index table (includes temporal annotation column) and all SQL queries (Invariant #6)
- [ ] ROADMAP.md Step 01_02_05 updated with: `plots/` output paths, I3 in invariants, starting_age dead-column note, temporal annotation gate conditions
- [ ] STEP_STATUS.yaml shows 01_02_05 as `complete`
- [ ] `match_rating_diff_histogram.png` carries red "LEAKAGE STATUS UNRESOLVED" suptitle
- [ ] `duration_histogram.png` carries red "POST-GAME" suptitle
- [ ] `age_uptime_histograms.png` carries red "IN-GAME" suptitle
- [ ] `opening_nonnull.png` carries red "IN-GAME" suptitle
- [ ] Winner bar chart shows exactly 2 bars (Win/Loss) with total N in title
- [ ] NULL rate bar chart uses harmonized thresholds: green=0%, yellow=<5%, orange=5-50%, red>=50%
- [ ] Notebook executes end-to-end without errors


## File Manifest

| File | Action |
|------|--------|
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` | Update (Step 01_02_05 block only) |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml` | Update (01_02_05 status) |
| `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.ipynb` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_05_visualizations.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_winner_distribution.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_num_players_distribution.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_map_top20.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_civ_top20.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_leaderboard_distribution.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_duration_histogram.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_elo_distributions.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_old_rating_histogram.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_match_rating_diff_histogram.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_age_uptime_histograms.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_opening_nonnull.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_iqr_outlier_summary.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_null_rate_bar.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/plots/01_02_05_monthly_match_count.png` | Create |


## Out of Scope

- Executing the match_rating_diff leakage verification query. That is deferred to a targeted pre-Phase-02 step.
- Bivariate or multivariate visualizations (Phase 01_03+).
- Visualization of dead constant fields (game_type, game_speed, starting_age).
- Visualization of overviews_raw (reference metadata, not per-match).
- New analytical computation — this step is read-only visualization of 01_02_04 census results.


## Open Questions

- match_rating_diff leakage: remains the single highest-priority open question for this dataset. The verification query is documented in research log 01_02_04 and must be executed before Phase 02 feature engineering.
- Whether 1v1 restriction or full match-size inclusion is the modelling scope. Does not affect visualization.


## Critique Instruction

For Category A, adversarial critique is required before execution. Dispatch
reviewer-adversarial to produce `planning/current_plan.critique.md`.
