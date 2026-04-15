# Adversarial Critique — plan_sc2egset_01_02_05.md

**Verdict: REVISE BEFORE EXECUTION**

Plan reviewed against: OLD plan from 19:46 (before planner comprehensive revision).
Note: planner revision (from completion at 20:30) addresses B1 (selectedRace added), B2 (Inv#6 SQL
section added to T14), W1 (SQ range corrected), W5 (max APM hardcode removed), W6 (handicap documented
in out-of-scope), W-elapsed_game_loops added as T09.
Remaining open issues noted below.

---

## BLOCKER — Already addressed by planner revision

### B1: False claim "selectedRace is not a column in replay_players_raw schema"
Column confirmed at `replay_players_raw.yaml` line 47. 8 categories including 1,110 empty strings and
10 Rand picks. Must be visualized.
**Planner fix:** Added as T04 — selectedRace horizontal bar chart.

### B2: Invariant #6 violation — SQL queries not in summary artifact
Plan T12 had no SQL section; plot captions only.
**Planner fix:** T14 now requires a "SQL Queries" section with all DuckDB queries verbatim.

### B3: bins=50 magic number (Invariant #7) — PARTIALLY ADDRESSED
Plan says "50 bins used throughout as consistent first-pass EDA resolution" (circular reasoning).
**Planner rationale:** "50 bins is the project-wide first-pass EDA resolution (Invariant #7: justified as consistent resolution across all histograms in this notebook, following Tukey's emphasis on visual consistency)."
This is still circular. True compliance requires Sturges/FD derivation or a cited literature precedent.
**Status:** WARNING-level — defensible in practice but not fully Invariant #7 compliant.

---

## BLOCKER — Added by planner (was missing from old plan)

### elapsed_game_loops not visualized (EDA Manual §7: incomplete coverage)
Column exists in replays_meta_raw, skewness=2.03. DuckDB connection available.
**Planner fix:** Added as T09 — dual-panel duration histogram.

---

## REMAINING OPEN ISSUES (not addressed by planner revision)

### W1 (Remaining): bins=50 circular justification
bins=50 says "consistent across notebook" but doesn't derive from data. Acceptable pragmatically
but Invariant #7 requires: derive from data OR cite precedent.
**Suggested fix:** Add to T05/T06/etc.: "[I7: Sturges rule: ceil(1+log2(44817))=16 bins minimum;
50 bins provides finer resolution for shape assessment per Tukey (1977) visual consistency
recommendation]"

### W2: Negative MMR values (min=-36400) not addressed
MMR filter `MMR > 0` in T05 subplot (b) excludes BOTH zeros AND negative values. The annotation
"N=37,489 MMR=0 (83.6%) excluded" is wrong — it undercounts excluded rows.
**Examiner question:** "How many negative-MMR rows exist and what do they mean?"
**Suggested fix:** In T05 verification, compute:
```python
n_zero = (mmr_data["MMR"] == 0).sum()
n_negative = (mmr_data["MMR"] < 0).sum()
n_positive = (mmr_data["MMR"] > 0).sum()
print(f"MMR=0: {n_zero}, MMR<0: {n_negative}, MMR>0: {n_positive}")
```
And update annotation accordingly: "N={n_zero+n_negative} rows with MMR<=0 excluded (includes
{n_negative} negative MMR)".

### W3: Prerequisite gate checks 3 of 7+ consumed JSON keys
Gate checks only mmr_zero_interpretation, isInClan_distribution, clanTag_top20.
Notebook also reads: result_distribution, categorical_profiles, monthly_counts.
**Suggested fix:** Expand gate to check all consumed keys:
```python
REQUIRED_KEYS = [
    "result_distribution", "categorical_profiles", "monthly_counts",
    "mmr_zero_interpretation", "isInClan_distribution", "clanTag_top20",
]
```

### W4: categorical_profiles column name heterogeneity
Each profile's DataFrame has different label column names ("race", "highestLeague", "region").
A generic loop assuming a common column name will KeyError.
**Suggested fix:** In T03, reference the column named `col` explicitly for each plot.

### N2: Temporal line plot string x-axis hides month gaps
`monthly_counts` has gaps (e.g., 2016-04 through 2016-06 missing). String x-axis makes adjacent
months equidistant, hiding gaps. Use `pd.to_datetime()` for proper temporal axis.
**Suggested fix:** Parse month strings: `monthly_df["month"] = pd.to_datetime(monthly_df["month"])`
then use `fig.autofmt_xdate()`.

---

## Key statistics verified from JSON artifact

- MMR: min=-36400, 83.6% zeros (N=37,489 MMR=0 from artifact, but N_negative unknown — compute dynamically)
- SQ: min=-51, max=187 (NOT 0-187 as old plan claimed), 2 sentinel rows at -2,147,483,648
- APM: skewness=-0.20 (near-symmetric), 1,132 zeros (2.5%)
- supplyCappedPercent: skewness=2.25, p95=16 (95% of data in [0,16])
- selectedRace: 8 categories: Terran, Zerg, Protoss, Random, "" (1110), Rand (10), BWTe, BWZe, BWPr
