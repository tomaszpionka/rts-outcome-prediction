# Adversarial Critique — plan_aoe2companion_01_02_05.md

**Verdict: REVISE BEFORE EXECUTION**

Plan reviewed against: OLD plan from 19:46 (before planner comprehensive revision).
Note: planner revision (from completion at 20:30) addresses BLOCKER #1 (T03 data extraction bug).
Remaining open issues noted below.

---

## BLOCKER — Already addressed by planner revision

### B1: T03 won_consistency_2row data structure mismatch — guaranteed KeyError
Plan assumed JSON structure is category-value rows. Actual structure is ONE dict with category names as keys.
Old code: `consistency["category"].isin(["both_true", "both_false"])` — KeyError, column "category" does not exist.
**Planner fix:** `raw = census["won_consistency_2row"][0]; pd.DataFrame([{"category": cat, "count": raw[cat]} for cat in categories])`

### B2: T03 category list — total_2row_matches must not be plotted as a category
The old code would naively include total_2row_matches as a bar if it melted the entire dict.
**Planner fix:** Explicit categories list excludes total_2row_matches; other_inconsistent noted as 0.

---

## WARNING — Already addressed by planner revision

### W5: T06 season/rankLevel excluded without justification
**Planner fix:** Excluded with reasoning (season=constant=-1; rankLevel=pathological skewness=-273M).
**Planner fix:** Added two-panel grouping: Panel A (rank, rating) vs Panel B (wins/losses/games/streak/drops/rankCountry) with symlog y-scale.

### W9: T05 missing skewness annotation (Invariant #7 partial)
**Planner fix:** Annotate titles with skew/kurt from `census["matches_raw_skew_kurtosis"]`.

### W: Monthly volume line chart missing (deferred from 01_02_04, required by EDA Manual §3.2)
**Planner fix:** Added T11 (new): monthly match volume line chart with dual y-axis.

---

## REMAINING OPEN ISSUES (not addressed by planner revision)

### W1: T04 "top 20" cutoff is a magic number (Invariant #7)
The artifact contains 30 entries each for civ and map. Choosing top-20 has no documented derivation.
Examiner question: "Why 20 and not 30?" — No documented answer.
**Suggested fix:** Plot all 30 entries (match what the artifact contains), or add justification comment:
"Top-20 chosen because entries 21-30 each represent <0.5% of rows."

### W2: T05 bin widths (rating=100, ratingDiff=10) are magic numbers (Invariant #7)
Neither bin width is derived from data range, IQR, or a cited rule (Sturges/Freedman-Diaconis).
**Suggested fix:** Add I7 comments: "rating range 0-5001 / 100 = ~50 bins; ratingDiff range -174/+319 / 10 = ~50 bins"

### W3: T07 bar chart deviates from EDA Manual §3.2 "heatmap of missingness" — undocumented
The manual says "heatmap"; plan implements a bar chart. Deviation is defensible (single dimension for
55 columns) but must be documented.
**Suggested fix:** Add note in plan: "Bar chart used instead of heatmap per EDA Manual §3.2: for 55
columns with a single NULL-rate dimension, a bar chart provides higher information density than a
2D heatmap with a single row (which would be identical to a bar chart but harder to read)."

### W4: T07 color thresholds (1% and 10%) are magic numbers (Invariant #7)
**Suggested fix:** Add justification: "EDA Manual §4.5 suggests <5% as MCAR-safe threshold; 1%/10%/50%
are conventional EDA severity bands (minimal/moderate/severe missingness)."

### W6: T06 leaderboard aggregation not documented
Boxplots aggregate all leaderboard types. Examiner may ask why 1v1 and team rankings are mixed.
**Suggested fix:** Add note: "Global distributions shown across all leaderboard types; per-leaderboard
stratification deferred to bivariate analysis (01_03+) where leaderboard is the grouping variable."

---

## Key statistics verified from JSON artifact

- won: TRUE=47.62%, FALSE=47.69%, NULL=4.69% (near-perfect balance)
- won_consistency_2row: total_2row=40,062,975; both_true=2,499,163; both_false=1,899,564 (inconsistency ~10.98%)
- rating: skewness=0.5662, NULL=42.46%; ratingDiff: skewness=0.1105, NULL=42.46%
- profiles_raw: 7 dead columns (100% NULL), HyperLogLog phantom cardinalities 2-44
- leaderboards_raw: wins skewness=8.21, drops skewness=27.22, streak skewness=-10.85
