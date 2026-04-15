# Step 01_02_05 — Univariate Visualizations: aoestats

**Phase:** 01 — Data Exploration
**Pipeline Section:** 01_02 — Exploratory Data Analysis (Tukey-style)
**Dataset:** aoestats
**Invariants applied:** #6 (SQL reproducibility), #7 (no magic numbers), #9 (step scope)
**Predecessor artifact:** `01_02_04_univariate_census.json`

## Plot Index

| # | File | Description |
|---|------|-------------|
| 1 | `01_02_05_winner_distribution.png` | Winner distribution bar chart (players_raw) |
| 2 | `01_02_05_num_players_distribution.png` | Match size distribution bar chart (matches_raw) |
| 3 | `01_02_05_map_top20.png` | Top-20 maps horizontal bar chart (matches_raw) |
| 4 | `01_02_05_civ_top20.png` | Top-20 civilizations horizontal bar chart (players_raw) |
| 5 | `01_02_05_leaderboard_distribution.png` | Leaderboard distribution bar chart (matches_raw) |
| 6 | `01_02_05_duration_histogram.png` | Duration dual-panel histogram: body (linear) + full range (log) |
| 7 | `01_02_05_elo_distributions.png` | ELO distributions 1x3 panel (sentinel -1.0 excluded) |
| 8 | `01_02_05_old_rating_histogram.png` | old_rating histogram with p05/median/p95 annotations |
| 9 | `01_02_05_match_rating_diff_histogram.png` | match_rating_diff histogram (clipped [-200,+200], kurtosis + IQR fences) |
| 10 | `01_02_05_age_uptime_histograms.png` | Age uptime 1x3 panel: feudal/castle/imperial (non-NULL, variable bin widths) |
| 11 | `01_02_05_opening_nonnull.png` | Opening strategy distribution (non-NULL only) |
| 12 | `01_02_05_iqr_outlier_summary.png` | IQR outlier summary bar chart (color-coded by table) |
| 13 | `01_02_05_null_rate_bar.png` | NULL rate bar chart for all 32 columns (severity color-coded) |
| 14 | `01_02_05_monthly_match_count.png` | Monthly match volume time series (matches_raw) |

## SQL Queries (Invariant #6)

All SQL queries that produce plotted data appear verbatim below.

### `hist_duration_body`

```sql
SELECT FLOOR(duration / 1e9 / 60) AS minute_bin, COUNT(*) AS cnt
FROM matches_raw
WHERE duration IS NOT NULL AND duration / 1e9 / 60 <= 120
GROUP BY minute_bin
ORDER BY minute_bin
```

### `hist_duration_full_log`

```sql
SELECT FLOOR(duration / 1e9 / 600) * 10 AS ten_min_bin, COUNT(*) AS cnt
FROM matches_raw
WHERE duration IS NOT NULL
GROUP BY ten_min_bin
ORDER BY ten_min_bin
```

### `hist_avg_elo`

```sql
SELECT FLOOR(avg_elo / 25) * 25 AS bin, COUNT(*) AS cnt
FROM matches_raw
GROUP BY bin ORDER BY bin
```

### `hist_team_0_elo`

```sql
SELECT FLOOR(team_0_elo / 25) * 25 AS bin, COUNT(*) AS cnt
FROM matches_raw
WHERE team_0_elo >= 0
GROUP BY bin ORDER BY bin
```

### `hist_team_1_elo`

```sql
SELECT FLOOR(team_1_elo / 25) * 25 AS bin, COUNT(*) AS cnt
FROM matches_raw
WHERE team_1_elo >= 0
GROUP BY bin ORDER BY bin
```

### `hist_old_rating`

```sql
SELECT FLOOR(old_rating / 25) * 25 AS bin, COUNT(*) AS cnt
FROM players_raw
GROUP BY bin ORDER BY bin
```

### `hist_match_rating_diff`

```sql
SELECT FLOOR(match_rating_diff / 5) * 5 AS bin, COUNT(*) AS cnt
FROM players_raw
WHERE match_rating_diff IS NOT NULL
  AND match_rating_diff BETWEEN -200 AND 200
GROUP BY bin ORDER BY bin
```

### `hist_feudal_age_uptime`

```sql
SELECT FLOOR(feudal_age_uptime / 10) * 10 AS bin, COUNT(*) AS cnt
FROM players_raw
WHERE feudal_age_uptime IS NOT NULL
GROUP BY bin ORDER BY bin
```

### `hist_castle_age_uptime`

```sql
SELECT FLOOR(castle_age_uptime / 20) * 20 AS bin, COUNT(*) AS cnt
FROM players_raw
WHERE castle_age_uptime IS NOT NULL
GROUP BY bin ORDER BY bin
```

### `hist_imperial_age_uptime`

```sql
SELECT FLOOR(imperial_age_uptime / 30) * 30 AS bin, COUNT(*) AS cnt
FROM players_raw
WHERE imperial_age_uptime IS NOT NULL
GROUP BY bin ORDER BY bin
```

### `monthly_match_counts`

```sql
SELECT DATE_TRUNC('month', started_timestamp) AS month, COUNT(*) AS match_count
FROM matches_raw WHERE started_timestamp IS NOT NULL
GROUP BY month ORDER BY month
```
