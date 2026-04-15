# Adversarial Critique — plan_aoe2companion_01_02_04_pass3.md

**Plan:** planning/plan_aoe2companion_01_02_04_pass3.md
**Phase:** 01 / Step 01_02_04 (Pass 3)
**Date:** 2026-04-15
**Reviewer model:** claude-opus-4-6

---

## VERDICT: APPROVED WITH CONDITIONS

Two conditions must be addressed before execution begins (C1, C2 below).

---

## Critical Issues (must fix before execution)

### C1 — Freedman-Diaconis produces meaningless or division-by-zero results for low-cardinality integer columns

**Affects:** T01

The plan applies Freedman-Diaconis (FD) histograms uniformly to all 24 numeric columns. Several are low-cardinality integers where FD is inappropriate:

- `matches_raw.color` — likely 1–8 (player color slots)
- `matches_raw.slot` — likely 1–8
- `matches_raw.team` — likely 1–4
- `matches_raw.internalLeaderboardId` — small set of distinct IDs
- `ratings_raw.leaderboard_id` — notebook profiles this as categorical in Section H.1b (line 1032)
- `ratings_raw.season` — small set of integer season numbers
- `leaderboards_raw.season` — same
- `leaderboards_raw.rankLevel` — likely a small enum

**Division-by-zero failure path in the nice-number rounding block (plan lines 164–174):**

When FD yields `bin_width_raw = 0.3`:
- `magnitude = 10^floor(log10(0.3)) = 10^(-1) = 0.1`
- `normalized = 0.3 / 0.1 = 3.0` → `nice = 2`
- `bin_width = int(2 * 0.1) = int(0.2) = 0`

The guard at line 161 (`if bin_width_raw <= 0`) does NOT catch this. The subsequent `FLOOR(col / 0) * 0` in DuckDB causes division by zero. The guard at line 176 (`if bin_width < 1 and col_range >= 1`) catches some cases but not when `int()` truncation produces exactly 0 before the guard runs.

**Fix required:** Add a cardinality pre-check: if `COUNT(DISTINCT col) <= 20`, emit a frequency table (`SELECT col, COUNT(*) GROUP BY col ORDER BY col`) instead of a histogram. This is scientifically correct for discrete variables. Add `"frequency_table"` as a valid `bin_method`. Also add `if bin_width == 0: bin_width = 1` after line 174 as a safety guard.

**Evidence:** Notebook lines 426–429 include `slot`, `color`, `team` in `matches_numeric_cols`. Line 1032 treats `leaderboard_id` as categorical.

---

### C2 — T02 does not store SQL strings in result dicts; T03 emits unresolved template placeholders

**Affects:** T02, T03

T01 correctly stores `"sql": hist_sql.strip()` in each histogram result, enabling T03 to emit verbatim SQL. T02 does NOT store SQL strings in `lb_highcard_results` or `pr_highcard_results`. T03's H.1c and H.2c artifact sections emit literal `'{col}'` and `"{col}"` template placeholders rather than verbatim executed SQL — violating Invariant #6.

**Fix required:** In T02's loop, store the SQL string in the result dict:
```python
row_dict = row.to_dict()
row_dict["sql"] = sql.strip()
pr_highcard_results.append(row_dict)
```
Then in T03, emit actual per-column SQL from results instead of the template.

---

## Minor Issues (should fix)

### M1 — T01 issues 24 redundant COUNT queries against 277M+ row tables

Plan lines 141–143 run `SELECT COUNT("{col}") FROM {table} WHERE "{col}" IS NOT NULL` for every numeric column. This data is already in `null_census_matches` (line 87), `lb_summarize`, and ratings_raw SUMMARIZE outputs. Re-querying over 277M+ rows (matches_raw) and ~460M rows (ratings_raw) wastes time and risks exceeding the 1800s gate condition. Extract `n_nonnull` from existing null census dataframes instead.

### M2 — Sturges fallback does not guard against col_range < 1 when col_range > 0

When IQR=0 and col_range < 1 (e.g., 0.5), Sturges gives `bin_width_raw ≈ 0.018`. After nice-number rounding: `bin_width = 0.02` (float). The guard at line 176 (`if bin_width < 1 and col_range >= 1`) does NOT trigger because `col_range = 0.5 < 1`. Fix: add `elif bin_width < 1: bin_width = col_range` (one bin for the sub-unit range).

### M3 — `leaderboard_id` and `season` in ratings_raw are categoricals receiving histograms

`ratings_raw.leaderboard_id` is already profiled categorically in Section H.1b. A FD histogram is scientifically redundant. Addressed by C1's cardinality pre-check but worth explicit noting.

### M4 — No explicit note on removing old hardcoded histogram cells

The plan says to insert new histogram code at Section F.4 but does not explicitly instruct the executor to remove the old hardcoded cells at lines 665–729 (containing `rating_hist_df`, `ratingdiff_hist_df` variable names). Without full removal, two histogram implementations coexist.

---

## Confirmed Correct

1. **Variable names exist in notebook.** `matches_numeric_stats` (line 432), `ratings_numeric_stats` (line 466), `lb_numeric_stats` (line 501) — confirmed present.

2. **Column count 24 = 9 + 5 + 10 is accurate.** Verified against schema YAMLs and notebook column lists.
   - matches_raw: `rating, ratingDiff, population, slot, color, team, speedFactor, treatyLength, internalLeaderboardId` — 9
   - ratings_raw: `rating, games, rating_diff, leaderboard_id, season` — 5
   - leaderboards_raw: `rank, rating, wins, losses, games, streak, drops, rankCountry, season, rankLevel` — 10

3. **Section F.4 location.** Notebook line 665: `# ### F.4 Histograms and boxplots`. Confirmed.

4. **Section J location.** Notebook line 1439: `# ## J. Write artifacts`. Confirmed.

5. **No existing `histogram_data` key in `findings`.** All 34 `findings[` assignments confirmed by grep — no collision risk.

6. **The 5 VARCHAR columns for T02 are correct.** `profiles_raw`: `name`, `steamId`, `avatarhash`. `leaderboards_raw`: `name`, `steamId`. None currently profiled. Correct.

7. **No temporal leakage concerns.** Phase 01 EDA profiling; no feature construction.

8. **PII-adjacent fields handled appropriately.** Cardinality + NULL count only for `name`, `steamId`, `avatarhash` — no Top-K value dumps.

---

## Gate Condition Assessment

The gate condition is mostly mechanically verifiable but needs two updates:

**Gap 1:** Add `"frequency_table"` as valid `bin_method` once C1's cardinality pre-check is implemented. Update to: "each entry has `bin_method` in {freedman_diaconis, sturges, frequency_table, skipped_zero_range, skipped_no_data}."

**Gap 2:** Add: "old hardcoded histogram cells at lines 665–729 (containing `rating_hist_df`, `ratingdiff_hist_df` variable names) must not exist in the notebook."

All other gate conditions are mechanically testable.
