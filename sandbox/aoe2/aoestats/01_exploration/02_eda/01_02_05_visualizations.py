# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Step 01_02_05 -- Univariate Visualizations: aoestats
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_02 -- Exploratory Data Analysis (Tukey-style)
# **Dataset:** aoestats
# **Question:** What do the univariate distributions look like visually? Are there
# visual patterns not captured by summary statistics alone?
# **Invariants applied:** #6 (reproducibility -- SQL inlined in artifact),
# #7 (no magic numbers -- all values derived from census artifact at runtime),
# #9 (step scope: visualization only)
# **Predecessor:** 01_02_04 (Univariate Census) -- this notebook reads from its JSON artifact
# **Step scope:** visualization only -- no analytical computation beyond what is
# needed for plotting
# **Type:** Read-only -- no DuckDB writes, no new tables, no schema changes

# %% [markdown]
# ## Imports

# %%
import json
from pathlib import Path

import duckdb
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from rts_predict.games.aoe2.config import AOESTATS_DB_FILE
from rts_predict.common.notebook_utils import get_reports_dir, setup_notebook_logging

# %% [markdown]
# ## Setup

# %%
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
print(f"Plots dir: {plots_dir}")

# %%
sql_queries: dict[str, str] = {}

# %% [markdown]
# ## T03 — Winner Distribution Bar Chart

# %%
# Verification cell
winner_data = census["winner_distribution"]
winner_df = pd.DataFrame(winner_data)
print("Winner distribution data:")
print(winner_df.to_string(index=False))

# %%
n_players = census["players_null_census"]["total_rows"]
fig, ax = plt.subplots(figsize=(10, 6))
colors = {True: "green", False: "red"}
for _, row in winner_df.iterrows():
    bar = ax.bar(str(row["winner"]), row["cnt"], color=colors[row["winner"]])
    ax.text(
        bar[0].get_x() + bar[0].get_width() / 2,
        bar[0].get_height() + n_players * 0.002,
        f"{row['cnt']:,}\n({row['pct']:.1f}%)",
        ha="center",
        va="bottom",
        fontsize=11,
    )
ax.set_xlabel("Winner")
ax.set_ylabel("Count")
ax.set_title(f"Winner Distribution (players_raw, N={n_players:,})")
ax.set_ylim(0, max(winner_df["cnt"]) * 1.12)
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_winner_distribution.png", dpi=150)
plt.close()
print("Saved: 01_02_05_winner_distribution.png")

# %% [markdown]
# ## T04 — Num_players Distribution Bar Chart

# %%
# Verification cell
npl_data = census["num_players_distribution"]
npl_df = pd.DataFrame(npl_data)
print("num_players distribution:")
print(npl_df.to_string(index=False))

# %%
n_matches = census["matches_null_census"]["total_rows"]
fig, ax = plt.subplots(figsize=(10, 6))
for _, row in npl_df.iterrows():
    num = row["num_players"]
    color = "steelblue" if num % 2 == 0 else "gray"
    bar = ax.bar(str(num), row["distinct_match_count"], color=color)
    if row["distinct_match_count"] > 0:
        ax.text(
            bar[0].get_x() + bar[0].get_width() / 2,
            bar[0].get_height() + n_matches * 0.002,
            f"{row['distinct_match_count']:,}\n({row['pct']:.2f}%)",
            ha="center",
            va="bottom",
            fontsize=8,
        )
ax.set_xlabel("num_players")
ax.set_ylabel("Distinct Match Count")
ax.set_title(f"Match Size Distribution (matches_raw, N={n_matches:,})")
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="steelblue", label="Even (2, 4, 6, 8)"),
    Patch(facecolor="gray", label="Odd (1, 3, 5, 7)"),
]
ax.legend(handles=legend_elements, loc="upper right")
ax.set_ylim(0, max(npl_df["distinct_match_count"]) * 1.15)
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_num_players_distribution.png", dpi=150)
plt.close()
print("Saved: 01_02_05_num_players_distribution.png")

# %% [markdown]
# ## T05 — Map Top-20 and Civ Top-20 Horizontal Bar Charts

# %%
# Verification: map top-20
map_top20 = census["categorical_matches"]["map"]["top_values"][:20]
map_df = pd.DataFrame(map_top20)
map_cardinality = census["categorical_matches"]["map"]["cardinality"]
print(f"Map top-20 (cardinality={map_cardinality}):")
print(map_df.to_string(index=False))

# %%
map_df_sorted = map_df.sort_values("pct", ascending=True)
fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(map_df_sorted["map"], map_df_sorted["pct"], color="steelblue")
for bar, (_, row) in zip(bars, map_df_sorted.iterrows()):
    ax.text(
        bar.get_width() + 0.1,
        bar.get_y() + bar.get_height() / 2,
        f"{row['pct']:.2f}%",
        va="center",
        fontsize=8,
    )
ax.set_xlabel("Percentage (%)")
ax.set_title(f"Top-20 Maps (matches_raw, cardinality={map_cardinality})")
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_map_top20.png", dpi=150)
plt.close()
print("Saved: 01_02_05_map_top20.png")

# %%
# Verification: civ top-20
civ_top20 = census["categorical_players"]["civ"]["top_values"][:20]
civ_df = pd.DataFrame(civ_top20)
civ_cardinality = census["categorical_players"]["civ"]["cardinality"]
print(f"Civ top-20 (cardinality={civ_cardinality}):")
print(civ_df.to_string(index=False))

# %%
civ_df_sorted = civ_df.sort_values("pct", ascending=True)
fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(civ_df_sorted["civ"], civ_df_sorted["pct"], color="darkorange")
for bar, (_, row) in zip(bars, civ_df_sorted.iterrows()):
    ax.text(
        bar.get_width() + 0.05,
        bar.get_y() + bar.get_height() / 2,
        f"{row['pct']:.2f}%",
        va="center",
        fontsize=8,
    )
ax.set_xlabel("Percentage (%)")
ax.set_title(f"Top-20 Civilizations (players_raw, cardinality={civ_cardinality})")
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_civ_top20.png", dpi=150)
plt.close()
print("Saved: 01_02_05_civ_top20.png")

# %% [markdown]
# ## T06 — Leaderboard Distribution Bar Chart

# %%
# Verification cell
lb_data = census["categorical_matches"]["leaderboard"]["top_values"]
lb_df = pd.DataFrame(lb_data)
print("Leaderboard distribution:")
print(lb_df.to_string(index=False))

# %%
lb_df_sorted = lb_df.sort_values("pct", ascending=True)
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(lb_df_sorted["leaderboard"], lb_df_sorted["pct"], color="teal")
for bar, (_, row) in zip(bars, lb_df_sorted.iterrows()):
    ax.text(
        bar.get_width() + 0.1,
        bar.get_y() + bar.get_height() / 2,
        f"{row['cnt']:,} ({row['pct']:.2f}%)",
        va="center",
        fontsize=10,
    )
ax.set_xlabel("Percentage (%)")
ax.set_title(f"Leaderboard Distribution (matches_raw, N={n_matches:,})")
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_leaderboard_distribution.png", dpi=150)
plt.close()
print("Saved: 01_02_05_leaderboard_distribution.png")

# %% [markdown]
# ## T07 — Duration Histogram (Dual-Panel)
#
# Extreme skewness (1032.64) and max/median ratio ~2129x make a single panel uninformative.
# [I7: skewness=1032.64 from census["skew_kurtosis_matches"][0]; max/median = 5,574,815s / 2619.7s ~ 2129x]

# %%
# SQL queries for duration histograms
sql_queries["hist_duration_body"] = """SELECT FLOOR(duration / 1e9 / 60) AS minute_bin, COUNT(*) AS cnt
FROM matches_raw
WHERE duration IS NOT NULL AND duration / 1e9 / 60 <= 120
GROUP BY minute_bin
ORDER BY minute_bin"""

sql_queries["hist_duration_full_log"] = """SELECT FLOOR(duration / 1e9 / 600) * 10 AS ten_min_bin, COUNT(*) AS cnt
FROM matches_raw
WHERE duration IS NOT NULL
GROUP BY ten_min_bin
ORDER BY ten_min_bin"""

# %%
# Verification: left panel data
dur_body_df = con.sql(sql_queries["hist_duration_body"]).df()
print("Duration body (1-min bins, clipped at 120 min) - first/last 5 rows:")
print(dur_body_df.head(5).to_string(index=False))
print("...")
print(dur_body_df.tail(5).to_string(index=False))
print(f"Total bins: {len(dur_body_df)}")

# %%
# Verification: right panel data
dur_full_df = con.sql(sql_queries["hist_duration_full_log"]).df()
print("Duration full range (10-min bins) - first/last 5 rows:")
print(dur_full_df.head(5).to_string(index=False))
print("...")
print(dur_full_df.tail(5).to_string(index=False))
print(f"Total bins: {len(dur_full_df)}")

# %%
# Derive annotation values from census
dur_stats = census["numeric_stats_matches"][0]
assert dur_stats["label"] == "duration_sec", f"Expected duration_sec, got {dur_stats['label']}"
median_min = dur_stats["median_val"] / 60  # [I7: median = 2619.7/60 = 43.66 min]
p95_min = dur_stats["p95"] / 60  # [I7: p95 = 4714.1/60 = 78.57 min]
skewness_val = census["skew_kurtosis_matches"][0]["skewness"]  # [I7: 1032.64]
print(f"Median: {median_min:.1f} min, P95: {p95_min:.1f} min, Skewness: {skewness_val}")

fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(16, 5))

# Left panel: 1-minute bins, linear y, clipped at 120 min
ax_left.bar(dur_body_df["minute_bin"], dur_body_df["cnt"], width=1.0, color="steelblue", edgecolor="none")
ax_left.axvline(median_min, color="red", linestyle="--", linewidth=1.5, label=f"Median = {median_min:.1f} min")
ax_left.axvline(p95_min, color="orange", linestyle="--", linewidth=1.5, label=f"P95 = {p95_min:.1f} min")
ax_left.set_xlabel("Duration (minutes)")
ax_left.set_ylabel("Count")
ax_left.set_title("Duration (body, <= 120 min)")
ax_left.legend()

# Right panel: 10-minute bins, log y-scale
ax_right.bar(dur_full_df["ten_min_bin"], dur_full_df["cnt"], width=10.0, color="steelblue", edgecolor="none")
ax_right.set_yscale("log")
ax_right.set_xlabel("Duration (minutes)")
ax_right.set_ylabel("Count (log scale)")
ax_right.set_title("Duration (full range, log scale)")
ax_right.text(
    0.95, 0.95,
    f"Skewness = {skewness_val:.2f}\nirl_duration has identical distribution",
    transform=ax_right.transAxes,
    ha="right", va="top", fontsize=9,
    bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8),
)

plt.suptitle("Duration Distribution (matches_raw)", y=1.01)
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_duration_histogram.png", dpi=150)
plt.close()
print("Saved: 01_02_05_duration_histogram.png")

# %% [markdown]
# ## T08 — ELO Distribution Panels (1x3, Sentinel Excluded)
#
# Sentinel values (-1.0) excluded from team_0/1_elo.
# [I7: sentinel counts from census["elo_sentinel_counts"]: team_0=34, team_1=39; 34/30690651 = 0.00011%]

# %%
sql_queries["hist_avg_elo"] = """SELECT FLOOR(avg_elo / 25) * 25 AS bin, COUNT(*) AS cnt
FROM matches_raw
GROUP BY bin ORDER BY bin"""
# [I7: actual max = 2976.5 from census; 2976.5/25 = ~119 bins]

sql_queries["hist_team_0_elo"] = """SELECT FLOOR(team_0_elo / 25) * 25 AS bin, COUNT(*) AS cnt
FROM matches_raw
WHERE team_0_elo >= 0
GROUP BY bin ORDER BY bin"""
# [I7: actual max = 3038 from census; 3038/25 = ~122 bins]

sql_queries["hist_team_1_elo"] = """SELECT FLOOR(team_1_elo / 25) * 25 AS bin, COUNT(*) AS cnt
FROM matches_raw
WHERE team_1_elo >= 0
GROUP BY bin ORDER BY bin"""
# [I7: actual max = 3045 from census; 3045/25 = ~122 bins]

# %%
# Verification: first 5 bins of each ELO column
avg_elo_df = con.sql(sql_queries["hist_avg_elo"]).df()
team0_elo_df = con.sql(sql_queries["hist_team_0_elo"]).df()
team1_elo_df = con.sql(sql_queries["hist_team_1_elo"]).df()

print("avg_elo first 5 bins:")
print(avg_elo_df.head(5).to_string(index=False))
print("\nteam_0_elo first 5 bins (sentinel excluded):")
print(team0_elo_df.head(5).to_string(index=False))
print("\nteam_1_elo first 5 bins (sentinel excluded):")
print(team1_elo_df.head(5).to_string(index=False))

# %%
sentinel_0 = census["elo_sentinel_counts"]["team_0_elo_negative"]
sentinel_1 = census["elo_sentinel_counts"]["team_1_elo_negative"]

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# avg_elo
axes[0].bar(avg_elo_df["bin"], avg_elo_df["cnt"], width=25, color="steelblue", edgecolor="none")
axes[0].set_xlabel("avg_elo")
axes[0].set_ylabel("Count")
axes[0].set_title("avg_elo Distribution")

# team_0_elo
axes[1].bar(team0_elo_df["bin"], team0_elo_df["cnt"], width=25, color="darkorange", edgecolor="none")
axes[1].set_xlabel("team_0_elo")
axes[1].set_ylabel("Count")
axes[1].set_title("team_0_elo Distribution")
axes[1].text(
    0.95, 0.95,
    f"N={sentinel_0} sentinel (-1.0) excluded",
    transform=axes[1].transAxes,
    ha="right", va="top", fontsize=9,
    bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8),
)

# team_1_elo
axes[2].bar(team1_elo_df["bin"], team1_elo_df["cnt"], width=25, color="green", edgecolor="none")
axes[2].set_xlabel("team_1_elo")
axes[2].set_ylabel("Count")
axes[2].set_title("team_1_elo Distribution")
axes[2].text(
    0.95, 0.95,
    f"N={sentinel_1} sentinel (-1.0) excluded",
    transform=axes[2].transAxes,
    ha="right", va="top", fontsize=9,
    bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8),
)

plt.suptitle("ELO Distributions (matches_raw)", y=1.01)
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_elo_distributions.png", dpi=150)
plt.close()
print("Saved: 01_02_05_elo_distributions.png")

# %% [markdown]
# ## T09 — old_rating Histogram and match_rating_diff Histogram

# %%
sql_queries["hist_old_rating"] = """SELECT FLOOR(old_rating / 25) * 25 AS bin, COUNT(*) AS cnt
FROM players_raw
GROUP BY bin ORDER BY bin"""
# [I7: range 0-3045 from census; 3045/25 = ~122 bins]

# %%
# Verification: old_rating first 5 bins
old_rating_df = con.sql(sql_queries["hist_old_rating"]).df()
print("old_rating first 5 bins:")
print(old_rating_df.head(5).to_string(index=False))
print(f"Total bins: {len(old_rating_df)}")

# %%
# Derive annotation values from census
old_rating_stats = next(s for s in census["numeric_stats_players"] if s["label"] == "old_rating")
or_median = old_rating_stats["median_val"]  # [I7: 1066]
or_p05 = old_rating_stats["p05"]  # [I7: 665]
or_p95 = old_rating_stats["p95"]  # [I7: 1580]
print(f"old_rating: median={or_median}, p05={or_p05}, p95={or_p95}")

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(old_rating_df["bin"], old_rating_df["cnt"], width=25, color="steelblue", edgecolor="none")
ax.axvline(or_median, color="red", linestyle="--", linewidth=1.5, label=f"Median = {or_median:.0f}")
ax.axvline(or_p05, color="orange", linestyle="--", linewidth=1.5, label=f"P05 = {or_p05:.0f}")
ax.axvline(or_p95, color="purple", linestyle="--", linewidth=1.5, label=f"P95 = {or_p95:.0f}")
ax.set_xlabel("old_rating")
ax.set_ylabel("Count")
ax.set_title("old_rating Distribution (players_raw)")
ax.legend()
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_old_rating_histogram.png", dpi=150)
plt.close()
print("Saved: 01_02_05_old_rating_histogram.png")

# %%
sql_queries["hist_match_rating_diff"] = """SELECT FLOOR(match_rating_diff / 5) * 5 AS bin, COUNT(*) AS cnt
FROM players_raw
WHERE match_rating_diff IS NOT NULL
  AND match_rating_diff BETWEEN -200 AND 200
GROUP BY bin ORDER BY bin"""
# [I7: p05=-59, p95=+59 from census; clip to [-200, +200] to show leptokurtic shape while covering main body; full range is [-2185, +2185]]

# %%
# Verification: match_rating_diff first/last 5 bins
mrd_df = con.sql(sql_queries["hist_match_rating_diff"]).df()
print("match_rating_diff first 5 bins (clipped to [-200, +200]):")
print(mrd_df.head(5).to_string(index=False))
print("...")
print(mrd_df.tail(5).to_string(index=False))
print(f"Total bins: {len(mrd_df)}")

# %%
# Derive annotation values from census
mrd_skew = next(s for s in census["skew_kurtosis_players"] if s["label"] == "match_rating_diff")
mrd_kurtosis = mrd_skew["kurtosis"]  # [I7: 65.6753]
mrd_outlier = next(o for o in census["outlier_counts_players"] if o["label"] == "match_rating_diff")
mrd_lower_fence = mrd_outlier["lower_fence"]  # [I7: -68]
mrd_upper_fence = mrd_outlier["upper_fence"]  # [I7: +68]
mrd_stats = next(s for s in census["numeric_stats_players"] if s["label"] == "match_rating_diff")
mrd_min = mrd_stats["min_val"]  # [I7: -2185]
mrd_max = mrd_stats["max_val"]  # [I7: +2185]
print(f"kurtosis={mrd_kurtosis}, lower_fence={mrd_lower_fence}, upper_fence={mrd_upper_fence}, min={mrd_min}, max={mrd_max}")

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(mrd_df["bin"], mrd_df["cnt"], width=5, color="steelblue", edgecolor="none")
ax.axvline(mrd_lower_fence, color="orange", linestyle="--", linewidth=1.5, label=f"IQR lower fence = {mrd_lower_fence:.0f}")
ax.axvline(mrd_upper_fence, color="orange", linestyle="--", linewidth=1.5, label=f"IQR upper fence = {mrd_upper_fence:.0f}")
ax.text(
    0.95, 0.95,
    f"Kurtosis = {mrd_kurtosis:.2f}\nFull range: [{mrd_min:.0f}, +{mrd_max:.0f}]",
    transform=ax.transAxes,
    ha="right", va="top", fontsize=9,
    bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8),
)
ax.set_xlabel("match_rating_diff")
ax.set_ylabel("Count")
ax.set_title("match_rating_diff Distribution (players_raw, clipped to [-200, +200])")
ax.set_xlim(-200, 200)
ax.legend()
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_match_rating_diff_histogram.png", dpi=150)
plt.close()
print("Saved: 01_02_05_match_rating_diff_histogram.png")

# %% [markdown]
# ## T10 — Age Uptime Histograms (Variable Bin Widths)
#
# Variable bin widths calibrated to each age's effective range, producing ~42-43 bins per panel.

# %%
sql_queries["hist_feudal_age_uptime"] = """SELECT FLOOR(feudal_age_uptime / 10) * 10 AS bin, COUNT(*) AS cnt
FROM players_raw
WHERE feudal_age_uptime IS NOT NULL
GROUP BY bin ORDER BY bin"""
# [I7: p05=535.1, p95=962.6 from census; effective body ~427s; 427/10 = 43 bins]

sql_queries["hist_castle_age_uptime"] = """SELECT FLOOR(castle_age_uptime / 20) * 20 AS bin, COUNT(*) AS cnt
FROM players_raw
WHERE castle_age_uptime IS NOT NULL
GROUP BY bin ORDER BY bin"""
# [I7: p05=889.1, p95=1752.1 from census; effective body ~863s; 863/20 = 43 bins]

sql_queries["hist_imperial_age_uptime"] = """SELECT FLOOR(imperial_age_uptime / 30) * 30 AS bin, COUNT(*) AS cnt
FROM players_raw
WHERE imperial_age_uptime IS NOT NULL
GROUP BY bin ORDER BY bin"""
# [I7: p05=1681.1, p95=2933.0 from census; effective body ~1252s; 1252/30 = 42 bins]

# %%
# Verification: first 5 bins of each age uptime
feudal_df = con.sql(sql_queries["hist_feudal_age_uptime"]).df()
castle_df = con.sql(sql_queries["hist_castle_age_uptime"]).df()
imperial_df = con.sql(sql_queries["hist_imperial_age_uptime"]).df()

print("feudal_age_uptime first 5 bins:")
print(feudal_df.head(5).to_string(index=False))
print("\ncastle_age_uptime first 5 bins:")
print(castle_df.head(5).to_string(index=False))
print("\nimperial_age_uptime first 5 bins:")
print(imperial_df.head(5).to_string(index=False))

# %%
# Derive annotation values from census for each age uptime
def get_player_stats(label: str) -> dict:
    return next(s for s in census["numeric_stats_players"] if s["label"] == label)

def get_player_null_pct(col: str) -> float:
    return next(c for c in census["players_null_census"]["columns"] if c["column"] == col)["null_pct"]

def get_skew(label: str) -> float:
    return next(s for s in census["skew_kurtosis_players"] if s["label"] == label)["skewness"]

feudal_stats = get_player_stats("feudal_age_uptime")
castle_stats = get_player_stats("castle_age_uptime")
imperial_stats = get_player_stats("imperial_age_uptime")

feudal_null_pct = get_player_null_pct("feudal_age_uptime")
castle_null_pct = get_player_null_pct("castle_age_uptime")
imperial_null_pct = get_player_null_pct("imperial_age_uptime")

feudal_skew = get_skew("feudal_age_uptime")
castle_skew = get_skew("castle_age_uptime")
imperial_skew = get_skew("imperial_age_uptime")

print(f"feudal: N={feudal_stats['n_nonnull']:.0f}, null_pct={feudal_null_pct:.1f}%, median={feudal_stats['median_val']:.1f}, skew={feudal_skew:.2f}")
print(f"castle: N={castle_stats['n_nonnull']:.0f}, null_pct={castle_null_pct:.1f}%, median={castle_stats['median_val']:.1f}, skew={castle_skew:.2f}")
print(f"imperial: N={imperial_stats['n_nonnull']:.0f}, null_pct={imperial_null_pct:.1f}%, median={imperial_stats['median_val']:.1f}, skew={imperial_skew:.2f}")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

age_configs = [
    ("feudal_age_uptime", feudal_df, feudal_stats, feudal_null_pct, feudal_skew, 10, "steelblue"),
    ("castle_age_uptime", castle_df, castle_stats, castle_null_pct, castle_skew, 20, "darkorange"),
    ("imperial_age_uptime", imperial_df, imperial_stats, imperial_null_pct, imperial_skew, 30, "green"),
]

for ax, (label, df, stats, null_pct, skew, bw, color) in zip(axes, age_configs):
    ax.bar(df["bin"], df["cnt"], width=bw, color=color, edgecolor="none")
    ax.axvline(stats["median_val"], color="red", linestyle="--", linewidth=1.5)
    ax.set_xlabel(f"{label} (seconds)")
    ax.set_ylabel("Count")
    ax.set_title(label.replace("_", " ").title())
    ax.text(
        0.97, 0.97,
        f"N={stats['n_nonnull']:.0f}\nnull_pct={null_pct:.1f}%\nmedian={stats['median_val']:.0f}s\nskew={skew:.2f}",
        transform=ax.transAxes,
        ha="right", va="top", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8),
    )

plt.suptitle("Age Uptime Distributions (players_raw, non-NULL only)", y=1.01)
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_age_uptime_histograms.png", dpi=150)
plt.close()
print("Saved: 01_02_05_age_uptime_histograms.png")

# %% [markdown]
# ## T11 — Opening Non-NULL Distribution Bar Chart

# %%
# Prerequisite gate
assert "opening_nonnull_distribution" in census, (
    "BLOCKER: 'opening_nonnull_distribution' not found in census. "
    "Execute plan_aoestats_01_02_04_pass2 (T08) before running T11."
)

# %%
# Verification cell
opening_dist = census["opening_nonnull_distribution"]
opening_df = pd.DataFrame(opening_dist["values"])
total_nonnull = opening_dist["total_nonnull"]
print(f"Opening non-NULL distribution: N={total_nonnull:,}")
print(opening_df.to_string(index=False))

# %%
# Derive null_pct from census
opening_null_pct = next(
    c for c in census["players_null_census"]["columns"] if c["column"] == "opening"
)["null_pct"]
print(f"opening null_pct: {opening_null_pct:.2f}%")

opening_df_sorted = opening_df.sort_values("pct_of_nonnull", ascending=True)
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(opening_df_sorted["opening"], opening_df_sorted["pct_of_nonnull"], color="mediumseagreen")
for bar, (_, row) in zip(bars, opening_df_sorted.iterrows()):
    ax.text(
        bar.get_width() + 0.2,
        bar.get_y() + bar.get_height() / 2,
        f"{row['pct_of_nonnull']:.2f}%",
        va="center",
        fontsize=9,
    )
ax.set_xlabel("% of non-NULL rows")
ax.set_title(
    f"Opening Strategy (non-NULL only, N={total_nonnull:,}; {opening_null_pct:.2f}% NULL excluded)"
)
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_opening_nonnull.png", dpi=150)
plt.close()
print("Saved: 01_02_05_opening_nonnull.png")

# %% [markdown]
# ## T12 — IQR Outlier Summary Bar Chart

# %%
# Verification cell
outlier_matches = pd.DataFrame(census["outlier_counts_matches"])
outlier_matches["table"] = "matches_raw"
outlier_players = pd.DataFrame(census["outlier_counts_players"])
outlier_players["table"] = "players_raw"
outlier_all = pd.concat([outlier_matches, outlier_players], ignore_index=True)
outlier_all_sorted = outlier_all.sort_values("outlier_pct", ascending=True)
print("IQR outlier summary:")
print(outlier_all_sorted[["label", "table", "outlier_pct", "outlier_total"]].to_string(index=False))

# %%
high_null_cols = {"feudal_age_uptime", "castle_age_uptime", "imperial_age_uptime"}
colors_table = {"matches_raw": "steelblue", "players_raw": "darkorange"}
bar_colors = [colors_table[t] for t in outlier_all_sorted["table"]]

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(
    outlier_all_sorted["label"],
    outlier_all_sorted["outlier_pct"],
    color=bar_colors,
)

for bar, (_, row) in zip(bars, outlier_all_sorted.iterrows()):
    label_text = row["label"]
    if label_text in high_null_cols:
        ax.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"{row['outlier_pct']:.2f}% *high NULL",
            va="center",
            fontsize=8,
            color="red",
        )
    else:
        ax.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"{row['outlier_pct']:.2f}%",
            va="center",
            fontsize=8,
        )

from matplotlib.patches import Patch as MPatch
legend_elements = [
    MPatch(facecolor="steelblue", label="matches_raw"),
    MPatch(facecolor="darkorange", label="players_raw"),
]
ax.legend(handles=legend_elements, loc="lower right")
ax.set_xlabel("Outlier Percentage (IQR method, %)")
ax.set_title("IQR Outlier Summary (all numeric columns)")
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_iqr_outlier_summary.png", dpi=150)
plt.close()
print("Saved: 01_02_05_iqr_outlier_summary.png")

# %% [markdown]
# ## T13 — NULL Rate Bar Chart for All 32 Columns

# %%
# Verification cell
null_matches = pd.DataFrame(census["matches_null_census"]["columns"])
null_matches["col_label"] = "m." + null_matches["column"]
null_players = pd.DataFrame(census["players_null_census"]["columns"])
null_players["col_label"] = "p." + null_players["column"]
null_all = pd.concat(
    [null_matches[["col_label", "null_pct"]], null_players[["col_label", "null_pct"]]],
    ignore_index=True,
)
null_all_sorted = null_all.sort_values("null_pct", ascending=False)
print(f"NULL rate summary ({len(null_all_sorted)} columns):")
print(null_all_sorted.to_string(index=False))

# %%
def null_color(pct: float) -> str:
    if pct >= 50:
        return "red"
    elif pct >= 5:
        return "orange"
    elif pct > 0:
        return "gold"
    else:
        return "green"

bar_colors_null = [null_color(p) for p in null_all_sorted["null_pct"]]

fig, ax = plt.subplots(figsize=(12, 8))
ax.barh(null_all_sorted["col_label"], null_all_sorted["null_pct"], color=bar_colors_null)
ax.set_xlabel("NULL Rate (%)")
ax.set_title("NULL Rate: All 32 Columns (m.=matches_raw, p.=players_raw)")

from matplotlib.patches import Patch as MPatch2
legend_elements = [
    MPatch2(facecolor="red", label=">= 50% NULL"),
    MPatch2(facecolor="orange", label="5-50% NULL"),
    MPatch2(facecolor="gold", label="> 0% and < 5% NULL"),
    MPatch2(facecolor="green", label="0% NULL"),
]
ax.legend(handles=legend_elements, loc="lower right")
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_null_rate_bar.png", dpi=150)
plt.close()
print("Saved: 01_02_05_null_rate_bar.png")

# %% [markdown]
# ## T14 — Monthly Match Count Time Series

# %%
sql_queries["monthly_match_counts"] = """SELECT DATE_TRUNC('month', started_timestamp) AS month, COUNT(*) AS match_count
FROM matches_raw WHERE started_timestamp IS NOT NULL
GROUP BY month ORDER BY month"""

# %%
# Verification cell
monthly_df = con.sql(sql_queries["monthly_match_counts"]).df()
assert len(monthly_df) == census["temporal_range"]["distinct_months"], (
    f"Expected {census['temporal_range']['distinct_months']} months, got {len(monthly_df)}"
)
print(monthly_df.to_string())

# %%
mean_count = monthly_df["match_count"].mean()
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(monthly_df["month"], monthly_df["match_count"], marker="o", linewidth=1.5, markersize=4, color="steelblue")
ax.axhline(mean_count, color="red", linestyle="--", linewidth=1.5, label=f"Mean = {mean_count:,.0f}")
ax.set_xlabel("Month")
ax.set_ylabel("Match Count")
ax.set_title("Monthly Match Volume (matches_raw)")
ax.legend()
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_monthly_match_count.png", dpi=150)
plt.close()
print("Saved: 01_02_05_monthly_match_count.png")

# %% [markdown]
# ## T15 — Write Markdown Artifact and Close Connection

# %%
# Build markdown artifact
plot_index_rows = [
    ("1", "01_02_05_winner_distribution.png", "Winner distribution bar chart (players_raw)"),
    ("2", "01_02_05_num_players_distribution.png", "Match size distribution bar chart (matches_raw)"),
    ("3", "01_02_05_map_top20.png", "Top-20 maps horizontal bar chart (matches_raw)"),
    ("4", "01_02_05_civ_top20.png", "Top-20 civilizations horizontal bar chart (players_raw)"),
    ("5", "01_02_05_leaderboard_distribution.png", "Leaderboard distribution bar chart (matches_raw)"),
    ("6", "01_02_05_duration_histogram.png", "Duration dual-panel histogram: body (linear) + full range (log)"),
    ("7", "01_02_05_elo_distributions.png", "ELO distributions 1x3 panel (sentinel -1.0 excluded)"),
    ("8", "01_02_05_old_rating_histogram.png", "old_rating histogram with p05/median/p95 annotations"),
    ("9", "01_02_05_match_rating_diff_histogram.png", "match_rating_diff histogram (clipped [-200,+200], kurtosis + IQR fences)"),
    ("10", "01_02_05_age_uptime_histograms.png", "Age uptime 1x3 panel: feudal/castle/imperial (non-NULL, variable bin widths)"),
    ("11", "01_02_05_opening_nonnull.png", "Opening strategy distribution (non-NULL only)"),
    ("12", "01_02_05_iqr_outlier_summary.png", "IQR outlier summary bar chart (color-coded by table)"),
    ("13", "01_02_05_null_rate_bar.png", "NULL rate bar chart for all 32 columns (severity color-coded)"),
    ("14", "01_02_05_monthly_match_count.png", "Monthly match volume time series (matches_raw)"),
]

table_rows = "\n".join(
    f"| {n} | `{fn}` | {desc} |"
    for n, fn, desc in plot_index_rows
)

sql_blocks = "\n\n".join(
    f"### `{key}`\n\n```sql\n{sql}\n```"
    for key, sql in sql_queries.items()
)

md_content = f"""# Step 01_02_05 — Univariate Visualizations: aoestats

**Phase:** 01 — Data Exploration
**Pipeline Section:** 01_02 — Exploratory Data Analysis (Tukey-style)
**Dataset:** aoestats
**Invariants applied:** #6 (SQL reproducibility), #7 (no magic numbers), #9 (step scope)
**Predecessor artifact:** `01_02_04_univariate_census.json`

## Plot Index

| # | File | Description |
|---|------|-------------|
{table_rows}

## SQL Queries (Invariant #6)

All SQL queries that produce plotted data appear verbatim below.

{sql_blocks}
"""

md_path = artifacts_dir / "01_02_05_visualizations.md"
with open(md_path, "w") as f:
    f.write(md_content)
print(f"Written markdown artifact: {md_path}")
print(f"sql_queries keys: {list(sql_queries.keys())}")

# %%
con.close()
print("DuckDB connection closed.")

# %%
# Final verification
import os
expected_pngs = [
    "01_02_05_winner_distribution.png",
    "01_02_05_num_players_distribution.png",
    "01_02_05_map_top20.png",
    "01_02_05_civ_top20.png",
    "01_02_05_leaderboard_distribution.png",
    "01_02_05_duration_histogram.png",
    "01_02_05_elo_distributions.png",
    "01_02_05_old_rating_histogram.png",
    "01_02_05_match_rating_diff_histogram.png",
    "01_02_05_age_uptime_histograms.png",
    "01_02_05_opening_nonnull.png",
    "01_02_05_iqr_outlier_summary.png",
    "01_02_05_null_rate_bar.png",
    "01_02_05_monthly_match_count.png",
]
missing = []
for fname in expected_pngs:
    p = plots_dir / fname
    if not p.exists() or p.stat().st_size == 0:
        missing.append(fname)
if missing:
    print(f"MISSING or empty: {missing}")
else:
    print(f"All {len(expected_pngs)} PNG files present and non-empty.")
print(f"Markdown artifact exists: {(artifacts_dir / '01_02_05_visualizations.md').exists()}")
