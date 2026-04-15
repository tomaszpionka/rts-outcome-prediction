---
category: A
branch: feat/census-pass3
date: 2026-04-15
planner_model: claude-opus-4-6
dataset: aoe2companion
phase: "01"
pipeline_section: "01_02 -- Exploratory Data Analysis"
invariants_touched: [3, 6, 7, 8, 9]
source_artifacts:
  - sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_05_visualizations.py
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.json
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.md
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md
  - sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_05_visualizations.py
  - .claude/scientific-invariants.md
  - docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md
critique_required: true
research_log_ref: src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md#2026-04-15-01-02-05-viz-revision
---

# Plan: aoe2companion 01_02_05 -- Univariate Census Visualizations (revision)

## Scope

Revision of the existing Step 01_02_05 notebook and ROADMAP entry for the aoe2companion dataset.
The existing 13-plot notebook executed successfully and all PNGs exist on disk, but a
pre-execution adversarial audit identified 3 BLOCKERs and 3 WARNINGs. This plan
adds 2 new plots (match duration histogram, NULL co-occurrence timeline), modifies
2 existing plots (ratingDiff with leakage annotation, completeness matrix with
harmonized thresholds), modifies 1 existing plot (won distribution to Win/Loss
2-bar + NULL annotation), updates the ROADMAP entry, and regenerates the markdown artifact.
Final plot count: 16.

Phase 01, Pipeline Section 01_02 (EDA), Step 01_02_05 (revision).

## Problem Statement

Three BLOCKERs prevent thesis-grade cross-dataset comparability:

1. **No match duration histogram.** aoestats and sc2egset both have dual-panel duration
   histograms. The census JSON has `match_duration_stats` (median=1,678s, p95=3,789s,
   max=3.28M s) and `duration_excluded_rows` (2,941 non-positive). Without a comparable
   plot, Chapter 4 cannot compare match duration distributions across all three datasets.

2. **PNG output paths in ROADMAP.** The ROADMAP `outputs` list says `artifacts/01_exploration/02_eda/plots/01_02_05_*.png`
   but does not enumerate filenames. Must list all 16.

3. **`ratingDiff` plotted without temporal classification annotation.** `ratingDiff` is
   classified `post_game` in the JSON `post_game_fields` key. Invariant #3 requires
   visible annotation. Examiner question: "Is this feature available at prediction time?"
   Answer must be visible on the plot.

Three WARNINGs require resolution:

4. NULL co-occurrence clusters (A: 8 boolean cols, 426K rows; B: fullTechTree+population,
   431K rows) not visualized. At minimum, a monthly timeline tests the API schema change
   hypothesis.

5. NULL severity color thresholds diverge from aoestats: aoestats uses green=0%,
   gold=>0 and <5%, orange=5-50%, red>=50%. aoe2companion uses green=<1%, orange=1-10%,
   red=>10%. Must harmonize to 4-tier aoestats scheme.

6. `won` bar chart shows NULL as third bar. For thesis comparability with aoestats
   (boolean 2-bar), restructure to Win/Loss 2-bar with NULL annotated separately.

## Assumptions & unknowns

- **Assumption:** The existing 01_02_05 notebook executed successfully and all 13 PNGs
  are on disk. This revision modifies the notebook in-place.
- **Assumption:** The JSON artifact `match_duration_stats`, `duration_excluded_rows`,
  `matches_raw_null_cooccurrence`, and `post_game_fields` keys contain the data needed.
  Verified: all four keys present in artifact.
- **Unknown:** Whether the monthly NULL co-occurrence timeline shows a clear temporal
  cutoff (supporting the API schema change hypothesis) or a diffuse pattern. Resolves
  by: execution (DuckDB query + plot).

## Literature context

EDA Manual Section 3.4 recommends dual-panel histograms for heavily skewed distributions:
body view (linear scale, clipped at a quantile) to show the main mass, and full-range
(log-y) to show the tail. This is the design used by aoestats (body clipped at 120 min,
full-range log-y) and sc2egset.

Tukey (1977) on temporal stability of missingness patterns: NULL co-occurrence clusters
should be plotted over time to distinguish schema changes (step function) from gradual
data quality degradation (trend).

Invariant #3 (temporal discipline) requires that any column classified as `post_game`
or `in_game` carry a visible annotation when plotted, so that thesis readers and examiners
can immediately identify which features would constitute temporal leakage if used for
prediction.

Invariant #8 (cross-game comparability) requires the same core plot types across all
three datasets: target distribution, map top-k, match duration histogram, rating histogram.

## Execution Steps

### T01 -- Patch ROADMAP.md Step 01_02_05 entry

**Objective:** Update the ROADMAP entry to reflect the revised plot count (16), the
`plots/` subdirectory in all output paths, the harmonized gate condition, and
the I3 annotation requirement.

**Instructions:**

1. In `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md`, locate
   the `### Step 01_02_05` YAML block.

2. Change `description` field: replace "13 visualization plots" with "16 visualization plots".

3. Change `method` field: append to the existing method text: ", match duration dual-panel histogram, NULL co-occurrence monthly timeline, post-game temporal classification annotation on ratingDiff (Invariant #3)."

4. Replace the `outputs` block with the full 16-file enumerated list:
   ```yaml
   outputs:
     plots:
       - "artifacts/01_exploration/02_eda/plots/01_02_05_won_distribution.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_won_consistency.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_leaderboard_distribution.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_civ_top30.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_map_top30.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_rating_histogram.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_ratingDiff_histogram.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_leaderboards_boxplots.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_completeness_matrix.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_profiles_null_rates.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_lb_leaderboard_distribution.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_boolean_stacked.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_monthly_volume.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_duration_histogram.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_null_cooccurrence_timeline.png"
       - "artifacts/01_exploration/02_eda/plots/01_02_05_null_cooccurrence_heatmap.png"
     report: "artifacts/01_exploration/02_eda/01_02_05_visualizations.md"
   ```

5. Replace the `gate` block:
   ```yaml
   gate:
     artifact_check: "All 16 PNG files exist under artifacts/01_exploration/02_eda/plots/. 01_02_05_visualizations.md exists with SQL queries (Invariant #6)."
     continue_predicate: "Notebook executes end-to-end without errors. All 16 PNGs present. Markdown artifact references all 16 PNGs."
     halt_predicate: "Any plot fails to render or DuckDB query errors."
   ```

6. Replace the `scientific_invariants_applied` block:
   ```yaml
   scientific_invariants_applied:
     - number: "3"
       how_upheld: "ratingDiff histogram carries visible 'POST-GAME -- not available at prediction time' annotation. All plots of post-game columns carry temporal classification label."
     - number: "6"
       how_upheld: "All DuckDB SQL queries reproduced verbatim in the markdown artifact."
     - number: "7"
       how_upheld: "Bin widths, color thresholds, and cutoffs justified inline with I7 comments."
     - number: "8"
       how_upheld: "Cross-dataset comparability: target distribution, map top-k, match duration histogram, rating histogram all present -- matching aoestats and sc2egset."
     - number: "9"
       how_upheld: "Visualization-only step -- reads 01_02_04 JSON artifact and DuckDB read-only."
   ```

**Verification:**
- ROADMAP entry shows 16 plots, `plots/` subdirectory paths, I3 in invariants list.

**File scope:**
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md`

---

### T02 -- Modify won distribution to 2-bar + NULL annotation (BLOCKER #6 / WARNING #6)

**Objective:** Restructure the won bar chart from 3-bar (True/False/NULL) to 2-bar
(Win/Loss) with NULL count annotated separately, matching aoestats boolean 2-bar design
for thesis comparability.

**Instructions:**

1. In the existing T02 plot cell (line ~80 onward), replace the current 3-bar
   implementation with:
   - Extract only the True and False rows from `census["won_distribution"]`.
   - Plot 2 vertical bars: "Win" (green #2ecc71) and "Loss" (red #e74c3c).
   - Annotate each bar with count and percentage as before.
   - Add a text annotation below the chart or in subtitle:
     `f"NULL (target unknown): {null_cnt:,} rows ({null_pct:.2f}%) -- excluded from bars"`
     where `null_cnt` and `null_pct` come from the NULL entry in `won_distribution`.

2. Keep the filename `01_02_05_won_distribution.png` unchanged (same path).

**Verification:**
- Plot shows exactly 2 bars (Win, Loss). NULL count visible as text annotation, not as a bar.

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T03 -- Add ratingDiff leakage annotation (BLOCKER #3)

**Objective:** Add a visible "POST-GAME -- not available at prediction time" annotation
to the ratingDiff histogram, satisfying Invariant #3.

**Instructions:**

1. In the existing T05 ratingDiff plot cell (line ~304 onward), after setting the title,
   add a subtitle or prominent text annotation:
   ```python
   ax.text(
       0.5, 0.97,
       "POST-GAME -- not available at prediction time (Invariant #3)",
       transform=ax.transAxes, ha="center", va="top",
       fontsize=10, fontweight="bold", color="#c0392b",
       bbox=dict(boxstyle="round,pad=0.3", facecolor="#fadbd8", edgecolor="#c0392b", alpha=0.9)
   )
   ```

2. The title remains as-is (N=..., skew=..., kurt=...). The leakage label is a separate
   annotation positioned at the top center of the plot area.

3. Keep the filename `01_02_05_ratingDiff_histogram.png` unchanged.

**Verification:**
- ratingDiff histogram visually displays the "POST-GAME" annotation in red.

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T04 -- Harmonize completeness matrix color thresholds (WARNING #5)

**Objective:** Change the NULL severity color scheme from 3-tier (green <1%, orange
1-10%, red >10%) to 4-tier matching aoestats: green=0%, gold=>0 and <5%, orange=5-50%,
red>=50%.

**Instructions:**

1. In the existing T07 cell (line ~430 onward), replace the color assignment logic with:
   ```python
   # I7: Thresholds harmonized with aoestats (4-tier severity, Invariant #8 cross-game
   # comparability). green=0% NULL, gold=>0% and <5% NULL, orange=5-50% NULL, red>=50% NULL.
   # aoestats uses identical bands: sandbox/aoe2/aoestats/.../01_02_05_visualizations.py L690-698.
   def null_color(pct: float) -> str:
       if pct >= 50:
           return "#e74c3c"    # red: >= 50%
       elif pct >= 5:
           return "#f39c12"    # orange: 5-50%
       elif pct > 0:
           return "#f1c40f"    # gold: > 0% and < 5%
       else:
           return "#2ecc71"    # green: 0%
   colors = [null_color(pct) for pct in null_df_sorted["null_pct"]]
   ```

2. Update the reference lines: replace the 1% and 10% vertical lines with 5% and 50%
   lines, and add a legend with all 4 tiers:
   ```python
   ax.axvline(x=5, color="gray", linestyle="--", alpha=0.5)
   ax.axvline(x=50, color="gray", linestyle=":", alpha=0.5)
   from matplotlib.patches import Patch as MPatch
   legend_elements = [
       MPatch(facecolor="#e74c3c", label=">= 50% NULL"),
       MPatch(facecolor="#f39c12", label="5-50% NULL"),
       MPatch(facecolor="#f1c40f", label="> 0% and < 5% NULL"),
       MPatch(facecolor="#2ecc71", label="0% NULL"),
   ]
   ax.legend(handles=legend_elements, loc="lower right")
   ```

3. Update the I7 comment to reference the harmonization rationale.

4. Keep the filename `01_02_05_completeness_matrix.png` unchanged.

**Verification:**
- Completeness matrix shows 4 color tiers with 5%/50% reference lines.
- Color scheme matches aoestats `null_color()` function.

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T05 -- Add match duration dual-panel histogram (BLOCKER #1)

**Objective:** Add a new dual-panel match duration histogram to achieve cross-dataset
comparability with aoestats and sc2egset. Design: left panel shows body (linear scale,
clipped at p95), right panel shows full range (log-y scale).

**Instructions:**

1. Insert a new section after T11 (monthly volume, line ~600) and before T12 (markdown
   artifact), with markdown header:
   ```
   ## T05-new -- Plot 14: Match Duration Dual-Panel Histogram
   ```

2. DuckDB queries for bin data. Two queries:

   **Left panel (body, clipped at p95=3789s ~ 63 min):**
   ```sql
   SELECT FLOOR(EXTRACT(EPOCH FROM (finished - started)) / 60) AS minute_bin,
          COUNT(*) AS cnt
   FROM matches_raw
   WHERE finished > started
     AND EXTRACT(EPOCH FROM (finished - started)) <= 3789
   GROUP BY minute_bin
   ORDER BY minute_bin
   ```
   I7 justification: `p95=3789s from census["match_duration_stats"][0]["p95_secs"]; clipped at p95 to show body distribution. 1-minute bins: range 0-63 min = 63 bins.`

   **Right panel (full range, log-y, 10-minute bins):**
   ```sql
   SELECT FLOOR(EXTRACT(EPOCH FROM (finished - started)) / 600) * 10 AS ten_min_bin,
          COUNT(*) AS cnt
   FROM matches_raw
   WHERE finished > started
   GROUP BY ten_min_bin
   ORDER BY ten_min_bin
   ```
   I7 justification: `Full range 1s to 3.28M s. 10-minute bins for the full range to keep bin count manageable.`

3. Verification cells: print both DataFrames (head+tail).

4. Load annotation values from census JSON:
   ```python
   dur_stats = census["match_duration_stats"][0]
   median_min = dur_stats["median_duration_secs"] / 60
   p95_min = dur_stats["p95_secs"] / 60
   excluded = census["duration_excluded_rows"][0]
   non_positive = excluded["non_positive_duration_count"]
   max_secs = dur_stats["max_duration_secs"]
   ```

5. Two-panel plot:
   ```python
   fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(14, 6))
   ```
   - **Left panel:** bar chart with 1-minute bins, linear y-axis.
     - Red dashed vertical line at median (28.0 min).
     - Orange dashed vertical line at p95 (63.2 min).
     - Title: "Duration (body, <= p95)"
   - **Right panel:** bar chart with 10-minute bins, log y-axis (`ax_right.set_yscale("log")`).
     - Annotation text box:
       `f"max = {max_secs:,.0f}s ({max_secs/86400:.0f} days)\n{non_positive:,} rows excluded (finished <= started)"`
     - Title: "Duration (full range, log scale)"
   - Suptitle: "Match Duration Distribution (matches_raw)"

6. Save as `plots_dir / "01_02_05_duration_histogram.png"`.

7. Add both SQL queries to the `sql_queries` dict for the markdown artifact.

**Verification:**
- `01_02_05_duration_histogram.png` exists with 2 panels.
- Left panel clipped at p95, right panel shows full range on log scale.

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T06 -- Add NULL co-occurrence visualization (WARNING #4)

**Objective:** Add visualizations of the NULL co-occurrence clusters. A monthly timeline
plot tests the "API schema change" hypothesis by showing whether Cluster A/B NULLs
appear as a temporal step function. A small heatmap shows the cross-cluster overlap.

**Instructions:**

1. Insert a new section after T05-new, with markdown header:
   ```
   ## T06-new -- Plots 15-16: NULL Co-occurrence Timeline and Heatmap
   ```

2. **Plot 15: Monthly NULL cluster timeline.** DuckDB query:
   ```sql
   SELECT DATE_TRUNC('month', started) AS month,
          COUNT(*) FILTER (WHERE "allowCheats" IS NULL
              AND "lockSpeed" IS NULL AND "lockTeams" IS NULL
              AND "recordGame" IS NULL AND "sharedExploration" IS NULL
              AND "teamPositions" IS NULL AND "teamTogether" IS NULL
              AND "turboMode" IS NULL) AS cluster_a_null,
          COUNT(*) FILTER (WHERE "fullTechTree" IS NULL
              AND population IS NULL) AS cluster_b_null,
          COUNT(*) AS total_rows
   FROM matches_raw
   WHERE started IS NOT NULL
   GROUP BY month
   ORDER BY month
   ```

3. Verification cell: print DataFrame head+tail.

4. Compute rates:
   ```python
   cooc_df["cluster_a_pct"] = 100.0 * cooc_df["cluster_a_null"] / cooc_df["total_rows"]
   cooc_df["cluster_b_pct"] = 100.0 * cooc_df["cluster_b_null"] / cooc_df["total_rows"]
   ```

5. Line chart with two lines (Cluster A %, Cluster B %) over time.
   Title: "NULL Co-occurrence Cluster Frequency by Month (matches_raw)"
   Subtitle: "Tests API schema change hypothesis -- step function = schema addition"
   If the pattern shows a clear temporal cutoff, annotate with the approximate date.
   Save as `plots_dir / "01_02_05_null_cooccurrence_timeline.png"`.

6. **Plot 16: Cross-cluster overlap heatmap.** Using the data from
   `census["matches_raw_null_cooccurrence"]["cross_cluster_overlap"][0]`:
   - 2x2 matrix: rows = Cluster A (NULL / non-NULL), cols = Cluster B (NULL / non-NULL)
   - Values from the artifact:
     - both_clusters_null = 428,321
     - cluster_a_only_null = 17
     - cluster_b_only_null = 3,173
     - neither = total_rows - (428321 + 17 + 3173) (compute from matches_raw_total_rows)
   - Use `matplotlib.pyplot.imshow` or `sns.heatmap` equivalent with annotated counts.
   Title: "NULL Co-occurrence: Cluster A vs Cluster B"
   Save as `plots_dir / "01_02_05_null_cooccurrence_heatmap.png"`.

7. Add a deferred-debt markdown cell:
   ```python
   # DEFERRED: Full N-column co-occurrence heatmap (55x55) deferred to 01_03 (systematic profiling).
   # Justification: the 2-cluster structure identified in 01_02_04 is adequately visualized
   # by the timeline + 2x2 overlap. A 55x55 heatmap would add visual noise without new insight
   # at this univariate step.
   ```

8. Add the monthly query to `sql_queries` dict.

**Verification:**
- `01_02_05_null_cooccurrence_timeline.png` exists (line chart).
- `01_02_05_null_cooccurrence_heatmap.png` exists (2x2 matrix).

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_05_visualizations.py`

---

### T07 -- Update markdown artifact and re-execute notebook

**Objective:** Regenerate the markdown summary artifact to include all 16 plots and
the new SQL queries. Re-execute the notebook end-to-end.

**Instructions:**

1. In the T12 cell, update the `plots_info` list to include 16 entries (add entries
   for duration_histogram, null_cooccurrence_timeline, null_cooccurrence_heatmap).

2. Update the `sql_queries` dict to include the new queries:
   - `hist_duration_body` (T05 left panel query)
   - `hist_duration_full_log` (T05 right panel query)
   - `null_cooccurrence_monthly` (T06 timeline query)

3. Update the verification loop to check for 16 PNG files.

4. Update the final print statement to report "All 16 plots present".

5. Re-execute the notebook:
   ```bash
   source .venv/bin/activate && poetry run jupytext --execute sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_05_visualizations.py --to notebook --output sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_05_visualizations.ipynb --ExecutePreprocessor.timeout=1800
   ```

6. Verify all 16 PNGs exist on disk.

**Verification:**
- `01_02_05_visualizations.md` lists all 16 PNGs with captions.
- `01_02_05_visualizations.md` includes SQL queries for duration histograms, NULL co-occurrence timeline, rating histogram, ratingDiff histogram, and monthly volume.
- All 16 PNG files exist under `reports/artifacts/01_exploration/02_eda/plots/`.
- Notebook `.ipynb` regenerated.

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_05_visualizations.py`
- `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_05_visualizations.ipynb`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/01_02_05_visualizations.md`

---

## File Manifest

| File | Action |
|------|--------|
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` | Update |
| `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_05_visualizations.py` | Rewrite |
| `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_05_visualizations.ipynb` | Rewrite |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/01_02_05_visualizations.md` | Rewrite |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/plots/01_02_05_won_distribution.png` | Rewrite |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/plots/01_02_05_ratingDiff_histogram.png` | Rewrite |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/plots/01_02_05_completeness_matrix.png` | Rewrite |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/plots/01_02_05_duration_histogram.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/plots/01_02_05_null_cooccurrence_timeline.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/plots/01_02_05_null_cooccurrence_heatmap.png` | Create |

## Gate Condition

- [ ] All 16 PNG files exist under `reports/artifacts/01_exploration/02_eda/plots/`:
  1. `01_02_05_won_distribution.png` (2-bar Win/Loss + NULL annotation)
  2. `01_02_05_won_consistency.png` (unchanged)
  3. `01_02_05_leaderboard_distribution.png` (unchanged)
  4. `01_02_05_civ_top30.png` (unchanged)
  5. `01_02_05_map_top30.png` (unchanged)
  6. `01_02_05_rating_histogram.png` (unchanged)
  7. `01_02_05_ratingDiff_histogram.png` (with POST-GAME leakage annotation)
  8. `01_02_05_leaderboards_boxplots.png` (unchanged)
  9. `01_02_05_completeness_matrix.png` (4-tier colors harmonized with aoestats)
  10. `01_02_05_profiles_null_rates.png` (unchanged)
  11. `01_02_05_lb_leaderboard_distribution.png` (unchanged)
  12. `01_02_05_boolean_stacked.png` (unchanged)
  13. `01_02_05_monthly_volume.png` (unchanged)
  14. `01_02_05_duration_histogram.png` (NEW: dual-panel)
  15. `01_02_05_null_cooccurrence_timeline.png` (NEW: monthly line chart)
  16. `01_02_05_null_cooccurrence_heatmap.png` (NEW: 2x2 overlap matrix)
- [ ] `01_02_05_visualizations.md` exists, references all 16 PNGs, includes SQL queries for all DuckDB-sourced plots.
- [ ] `ratingDiff` histogram visually displays "POST-GAME -- not available at prediction time" annotation.
- [ ] `won` distribution shows exactly 2 bars (Win, Loss) with NULL annotated as text.
- [ ] Completeness matrix uses 4-tier color scheme: green/gold/orange/red with 5%/50% thresholds.
- [ ] ROADMAP.md Step 01_02_05 entry updated with 16 plots, `plots/` paths, I3/I6/I7/I8/I9 invariants.
- [ ] Cross-dataset comparability: target distribution (check), map top-k (check), match duration histogram (check), rating histogram (check) -- all 4 core plots present.
- [ ] Notebook executes end-to-end without errors (timeout=1800s).
- [ ] No DuckDB writes (read-only notebook).

## Out of scope

- Quantitative analytics (all in 01_02_04 -- visualization only here).
- Bivariate or multivariate plots (Pipeline Section 01_03+).
- Research log entry (post-execution responsibility).
- Full 55x55 NULL co-occurrence heatmap (deferred to 01_03 systematic profiling).
- Per-leaderboard stratification of any plots (deferred to bivariate analysis 01_03+).
- STEP_STATUS.yaml re-update (already marked complete; revision does not change status).
- Matching the exact aoestats duration clip point (aoestats clips at 120 min because its
  p95 is different; aoe2companion clips at p95=63 min per its own distribution).

## Open questions

- Whether the NULL co-occurrence timeline shows a sharp step function (confirming API
  schema change) or a gradual pattern. Resolves by: execution of T06 DuckDB query.
- Whether the max duration outlier (3.28M s = 38 days) should be annotated on the
  right panel or is sufficiently visible on log scale. Resolves by: visual inspection
  at execution time; include annotation text box regardless.

## Deferred Debt

| Item | Target Step | Rationale |
|------|-------------|-----------|
| Full 55x55 NULL co-occurrence heatmap | 01_03 | Two-cluster structure adequately shown by timeline + 2x2; full matrix adds noise at univariate step |
| Per-leaderboard boxplot stratification | 01_03+ | Requires leaderboard_id as grouping variable (bivariate) |
| Temporal classification annotations on `rating` (ambiguous) | Phase 02 | Rating classified as ambiguous_pre_or_post; annotation deferred until row-level co-occurrence check resolves the ambiguity |
| KDE / QQ plots | 01_03+ | More informative when comparing groups |

---

**Critique gate:** For Category A, adversarial critique is required before execution.
Dispatch reviewer-adversarial to produce `planning/plan_aoe2companion_01_02_05.critique.md`.
