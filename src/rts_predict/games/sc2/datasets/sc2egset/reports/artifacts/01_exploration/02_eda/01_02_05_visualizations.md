# Step 01_02_05 -- Univariate EDA Visualizations

**Dataset:** sc2egset
**Phase:** 01 -- Data Exploration
**Pipeline Section:** 01_02 -- EDA (Tukey-style)
**Predecessor:** 01_02_04 (univariate census)
**Invariants applied:** #6 (SQL queries inlined), #7 (no magic numbers), #9 (step scope: visualize)

## Plots Produced

| # | Title | Filename | Observation |
|---|-------|----------|-------------|
| 1 | Result Distribution | 01_02_05_result_bar.png | Near-perfect 50/50 Win/Loss split (22,409 vs 22,382) with 7 Undecided and 2 Tie -- confirms clean binary outcome for modeling. |
| 2 | Categorical Distributions | 01_02_05_categorical_bars.png | Race is dominated by Prot/Zerg/Terr; highestLeague has 72% Unknown; region skews European (47%). |
| 3 | selectedRace Distribution | 01_02_05_selectedrace_bar.png | 8 categories including 1,110 empty strings (2.48%, highlighted red) and 10 Rand picks; anomalous entries absent from the race column. |
| 4 | MMR Distribution (Split View) | 01_02_05_mmr_split.png | Left panel dominated by zero-spike; right panel (MMR>0) reveals unimodal MMR distribution with long right tail toward Grandmaster ratings. |
| 5 | APM Distribution | 01_02_05_apm_hist.png | Near-symmetric distribution (skewness=-0.20) centered around median; extreme outlier visible at high APM values. |
| 6 | SQ Distribution (Split View) | 01_02_05_sq_split.png | Left panel shows INT32_MIN sentinel as isolated spike far below main mass; right panel (sentinel excluded) shows continuous distribution in -51 to 187 range. |
| 7 | supplyCappedPercent Distribution | 01_02_05_supplycapped_hist.png | Strong right-skew (skewness=2.25) with median near 0; 95th percentile at 16, confirming most players rarely hit supply cap. |
| 8 | Game Duration (elapsed_game_loops) | 01_02_05_duration_hist.png | Right-skewed duration; full-range panel compressed by extreme outliers; clipped panel at 40 min reveals main mass with long-game annotation. |
| 9 | MMR Zero-Spike by Result and highestLeague | 01_02_05_mmr_zero_interpretation.png | MMR=0 rate uniform across result categories (~83%) and across most league tiers, confirming zero is a missing-data sentinel not correlated with outcome. |
| 10 | Temporal Coverage | 01_02_05_temporal_coverage.png | Dataset spans 2016-2024 with visible gap in 2016-04 through 2016-06; monthly counts generally increase through mid-period before declining in later years. |
| 11 | isInClan Distribution | 01_02_05_isinclan_bar.png | 74% of players are not in a clan; 26% are clan members -- clan membership is a minority feature worth retaining for feature engineering. |
| 12 | clanTag Top-20 | 01_02_05_clantag_top20.png | Team liquid (αX) dominates clan tags; top-20 clans account for a substantial share of non-empty clan entries. |

## SQL Queries

All DuckDB SQL queries used in this notebook (Invariant #6: reproducibility):

**T05 (MMR):**
```sql
SELECT MMR FROM replay_players_raw WHERE MMR IS NOT NULL
```

**T06 (APM):**
```sql
SELECT APM FROM replay_players_raw WHERE APM IS NOT NULL
```

**T07 (SQ):**
```sql
SELECT SQ FROM replay_players_raw WHERE SQ IS NOT NULL
```

**T08 (supplyCappedPercent):**
```sql
SELECT supplyCappedPercent FROM replay_players_raw WHERE supplyCappedPercent IS NOT NULL
```

**T09 (duration):**
```sql
SELECT header.elapsedGameLoops AS elapsed_game_loops FROM replays_meta_raw WHERE header.elapsedGameLoops IS NOT NULL
```

## Data Sources

- `replay_players_raw` (DuckDB persistent table): player-level fields
- `replays_meta_raw` (DuckDB persistent table): replay-level metadata including elapsed_game_loops
- `01_02_04_univariate_census.json`: pre-computed distributions for result, categorical profiles, monthly counts, MMR zero-spike cross-tabulation, isInClan, and clanTag top-20
