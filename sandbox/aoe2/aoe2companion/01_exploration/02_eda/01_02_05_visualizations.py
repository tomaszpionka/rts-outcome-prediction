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
# # Step 01_02_05 -- Univariate Census Visualizations: aoe2companion
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_02 -- EDA
# **Dataset:** aoe2companion
# **Question:** What do the univariate distributions from 01_02_04 look like visually?
# **Invariants applied:** #6 (reproducibility -- SQL inlined in artifact),
# #7 (no magic numbers), #9 (step scope: visualization only)
# **Step scope:** visualization -- reads 01_02_04 JSON artifact and DuckDB (read-only)
# **Type:** Read-only -- no DuckDB writes, no new tables, no schema changes

# %% [markdown]
# ## 0. Imports and DB connection

# %%
import json
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rts_predict.common.notebook_utils import (
    get_notebook_db,
    get_reports_dir,
    setup_notebook_logging,
)

logger = setup_notebook_logging()
matplotlib.use("Agg")
plt.style.use("seaborn-v0_8-whitegrid")

# %%
db = get_notebook_db("aoe2", "aoe2companion")
con = db.con
print("Connected to aoe2companion DuckDB (read-only)")

# %%
reports_dir = get_reports_dir("aoe2", "aoe2companion")
artifacts_dir = reports_dir / "artifacts" / "01_exploration" / "02_eda"
artifacts_dir.mkdir(parents=True, exist_ok=True)
plots_dir = artifacts_dir / "plots"
plots_dir.mkdir(parents=True, exist_ok=True)
print(f"Artifacts dir: {artifacts_dir}")
print(f"Plots dir: {plots_dir}")

# %%
census_json_path = artifacts_dir / "01_02_04_univariate_census.json"
with open(census_json_path) as f:
    census = json.load(f)
print(f"Loaded 01_02_04 artifact: {len(census)} keys")
print(f"Keys: {sorted(census.keys())}")

# %% [markdown]
# ## T02 -- Plot 1: won distribution bar chart

# %%
won_dist = pd.DataFrame(census["won_distribution"])
print("=== won_dist (feeds bar chart) ===")
print(won_dist.to_string(index=False))

# %%
fig, ax = plt.subplots(figsize=(8, 6))
color_map = {True: '#2ecc71', False: '#e74c3c', None: '#95a5a6'}
labels = []
counts = []
colors = []
for row in census["won_distribution"]:
    label = str(row["won"]) if row["won"] is not None else "NULL"
    labels.append(label)
    counts.append(row["cnt"])
    colors.append(color_map[row["won"]])
bars = ax.bar(labels, counts, color=colors, edgecolor='black', linewidth=0.5)
for bar, cnt, row in zip(bars, counts, census['won_distribution']):
    ax.annotate(
        f"{cnt:,}\n({row['pct']:.2f}%)",
        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
        xytext=(0, 5),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=10,
    )
ax.set_xlabel("won value")
ax.set_ylabel("Row count")
ax.set_title("matches_raw: won Value Distribution")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_won_distribution.png", dpi=150)
plt.close()
print("Saved: 01_02_05_won_distribution.png")

# %% [markdown]
# ## T03 -- Plot 2: Intra-match consistency stacked bar

# %%
# CRITICAL: won_consistency_2row is a single-element list containing ONE dict
# with category names as keys. Do NOT use pd.DataFrame and then access ['category'].
raw = census["won_consistency_2row"][0]
total = raw["total_2row_matches"]
categories = [
    "consistent_complement", "both_true", "both_false",
    "both_null", "one_true_one_null", "one_false_one_null",
]
consistency = pd.DataFrame([
    {"category": cat, "count": raw[cat]} for cat in categories
])
consistency['pct'] = 100.0 * consistency['count'] / total
print("=== won_consistency_2row (feeds stacked bar) ===")
print(f"total_2row_matches: {total:,}")
print(consistency.to_string(index=False))

# %%
# Compute inconsistency annotation dynamically -- do NOT hardcode any percentage
inconsistent_count = raw["both_true"] + raw["both_false"]
inconsistent_pct = 100.0 * inconsistent_count / total
annotation = (
    f"~{inconsistent_pct:.2f}% of 2-player matches have both_true or both_false "
    f"won labels (empirical noise floor on prediction target accuracy).\n"
    f"Note: this counts only both_true+both_false; other inconsistent categories "
    f"(one_true_one_null, etc.) are shown but not counted here."
)
color_map_consistency = {
    "consistent_complement": "#2ecc71",
    "both_true": "#e67e22",
    "both_false": "#e67e22",
    "both_null": "#95a5a6",
    "one_true_one_null": "#f1c40f",
    "one_false_one_null": "#f1c40f",
}
fig, ax = plt.subplots(figsize=(14, 4))
left = 0.0
for _, row in consistency.iterrows():
    cat = row['category']
    pct = row['pct']
    ax.barh(0, pct, left=left, color=color_map_consistency[cat], label=cat,
            edgecolor='white', linewidth=0.5)
    if pct > 1.0:
        ax.text(
            left + pct / 2, 0, f'{pct:.1f}%',
            ha='center', va='center', fontsize=8, fontweight='bold', color='black'
        )
    left += pct
ax.set_xlim(0, 100)
ax.set_yticks([])
ax.set_xlabel("Percentage of 2-player matches")
ax.set_title("matches_raw: Intra-Match won Consistency (2-player matches)")
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=3, fontsize=9)
ax.text(
    0.01, -0.35, annotation,
    transform=ax.transAxes, fontsize=8, va='top',
    style='italic', color='#555555'
)
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_won_consistency.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: 01_02_05_won_consistency.png")

# %% [markdown]
# ## T04 -- Plots 3-5: Leaderboard, Civ top-30, Map top-30 horizontal bars

# %%
# I7: All 30 entries from the categorical_profiles artifact are plotted
# (no arbitrary cutoff). For civ, rank 30 (slavs) still represents 1.68%
# of rows. For map, rank 30 (rm_baltic) represents 0.42%.
# The artifact's LIMIT 30 in the source SQL is the data boundary here.
leaderboard_data = pd.DataFrame(census["categorical_profiles"]["leaderboard"])
print("=== leaderboard (feeds bar chart) ===")
print(leaderboard_data.to_string(index=False))

# %%
leaderboard_data_sorted = leaderboard_data.sort_values('cnt', ascending=True)
fig, ax = plt.subplots(figsize=(10, max(4, len(leaderboard_data_sorted) * 0.4)))
bars = ax.barh(leaderboard_data_sorted['value'], leaderboard_data_sorted['cnt'],
               color='#3498db', edgecolor='black', linewidth=0.3)
for bar, cnt in zip(bars, leaderboard_data_sorted['cnt']):
    ax.text(
        bar.get_width() + bar.get_width() * 0.01, bar.get_y() + bar.get_height() / 2,
        f'{cnt:,}', va='center', ha='left', fontsize=9
    )
ax.set_xlabel("Row count")
ax.set_title("matches_raw: leaderboard Distribution")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_leaderboard_distribution.png", dpi=150)
plt.close()
print("Saved: 01_02_05_leaderboard_distribution.png")

# %%
civ_data = pd.DataFrame(census["categorical_profiles"]["civ"])
print(f"=== civ top-{len(civ_data)} (feeds bar chart) ===")
print(civ_data.to_string(index=False))

# %%
civ_data_sorted = civ_data.sort_values('cnt', ascending=True)
fig, ax = plt.subplots(figsize=(10, max(6, len(civ_data_sorted) * 0.35)))
bars = ax.barh(civ_data_sorted['value'], civ_data_sorted['cnt'],
               color='#9b59b6', edgecolor='black', linewidth=0.3)
for bar, cnt in zip(bars, civ_data_sorted['cnt']):
    ax.text(
        bar.get_width() + bar.get_width() * 0.01, bar.get_y() + bar.get_height() / 2,
        f'{cnt:,}', va='center', ha='left', fontsize=7
    )
ax.set_xlabel("Row count")
ax.set_title(f"matches_raw: civ Top {len(civ_data_sorted)} Distribution")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_civ_top30.png", dpi=150)
plt.close()
print("Saved: 01_02_05_civ_top30.png")

# %%
map_data = pd.DataFrame(census["categorical_profiles"]["map"])
print(f"=== map top-{len(map_data)} (feeds bar chart) ===")
print(map_data.to_string(index=False))

# %%
map_data_sorted = map_data.sort_values('cnt', ascending=True)
fig, ax = plt.subplots(figsize=(10, max(6, len(map_data_sorted) * 0.35)))
bars = ax.barh(map_data_sorted['value'], map_data_sorted['cnt'],
               color='#1abc9c', edgecolor='black', linewidth=0.3)
for bar, cnt in zip(bars, map_data_sorted['cnt']):
    ax.text(
        bar.get_width() + bar.get_width() * 0.01, bar.get_y() + bar.get_height() / 2,
        f'{cnt:,}', va='center', ha='left', fontsize=7
    )
ax.set_xlabel("Row count")
ax.set_title(f"matches_raw: map Top {len(map_data_sorted)} Distribution")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_map_top30.png", dpi=150)
plt.close()
print("Saved: 01_02_05_map_top30.png")

# %% [markdown]
# ## T05 -- Plots 6-7: rating and ratingDiff histograms

# %%
# I7: rating range -1 to 5001 (~5002 range); 5002/100 = ~50 bins --
# adequate resolution for skewness=0.57
rating_hist_df = con.execute('''
    SELECT (FLOOR(rating / 100) * 100)::INTEGER AS bin, COUNT(*) AS cnt
    FROM matches_raw WHERE rating IS NOT NULL
    GROUP BY bin ORDER BY bin
''').df()
print("=== rating histogram bins (feeds histogram plot) ===")
print(rating_hist_df.to_string(index=False))

# %%
# Load skewness/kurtosis from census artifact for 'rating'
sk_df = pd.DataFrame(census["matches_raw_skew_kurtosis"])
rating_sk = sk_df[sk_df['column_name'] == 'rating'].iloc[0]
rating_skewness = rating_sk['skewness']
rating_kurtosis = rating_sk['kurtosis']
# Get null stats
null_df = pd.DataFrame(census["matches_raw_null_census"])
rating_null = null_df[null_df['column_name'] == 'rating'].iloc[0]
total_rows = census["matches_raw_total_rows"]
non_null_count = total_rows - int(rating_null['null_count'])
null_pct = rating_null['null_pct']
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(rating_hist_df['bin'], rating_hist_df['cnt'], width=90,
       color='#3498db', edgecolor='black', linewidth=0.2, alpha=0.85)
ax.set_xlabel("rating (bin width=100)")
ax.set_ylabel("Row count")
ax.set_title(
    f'matches_raw.rating '
    f'(N={non_null_count:,} non-NULL of {total_rows:,} total, '
    f'{null_pct:.2f}% NULL; skew={rating_skewness:.4f}, kurt={rating_kurtosis:.4f})'
)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_rating_histogram.png", dpi=150)
plt.close()
print("Saved: 01_02_05_rating_histogram.png")

# %%
# I7: ratingDiff range -174 to +319 (~493 range); 493/10 = ~49 bins
ratingdiff_hist_df = con.execute('''
    SELECT (FLOOR("ratingDiff" / 10) * 10)::INTEGER AS bin, COUNT(*) AS cnt
    FROM matches_raw WHERE "ratingDiff" IS NOT NULL
    GROUP BY bin ORDER BY bin
''').df()
print("=== ratingDiff histogram bins (feeds histogram plot) ===")
print(ratingdiff_hist_df.to_string(index=False))

# %%
ratingdiff_sk = sk_df[sk_df['column_name'] == 'ratingDiff'].iloc[0]
ratingdiff_skewness = ratingdiff_sk['skewness']
ratingdiff_kurtosis = ratingdiff_sk['kurtosis']
ratingdiff_null = null_df[null_df['column_name'] == 'ratingDiff'].iloc[0]
ratingdiff_non_null = total_rows - int(ratingdiff_null['null_count'])
ratingdiff_null_pct = ratingdiff_null['null_pct']
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(ratingdiff_hist_df['bin'], ratingdiff_hist_df['cnt'], width=9,
       color='#e74c3c', edgecolor='black', linewidth=0.2, alpha=0.85)
ax.set_xlabel("ratingDiff (bin width=10)")
ax.set_ylabel("Row count")
ax.set_title(
    f'matches_raw.ratingDiff '
    f'(N={ratingdiff_non_null:,} non-NULL of {total_rows:,} total, '
    f'{ratingdiff_null_pct:.2f}% NULL; skew={ratingdiff_skewness:.4f}, '
    f'kurt={ratingdiff_kurtosis:.4f})'
)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_ratingDiff_histogram.png", dpi=150)
plt.close()
print("Saved: 01_02_05_ratingDiff_histogram.png")

# %% [markdown]
# ## T06 -- Plot 8: leaderboards_raw numeric boxplots (two-panel)

# %%
lb_stats_df = pd.DataFrame(census["leaderboards_raw_numeric_stats"])
print("=== leaderboards_raw_numeric_stats (feeds boxplots) ===")
print(lb_stats_df.to_string(index=False))
lb_zero_df = pd.DataFrame(census["leaderboards_raw_zero_counts"])
print("\n=== leaderboards_raw_zero_counts ===")
print(lb_zero_df.to_string(index=False))
lb_sk_df = pd.DataFrame(census["leaderboards_raw_skew_kurtosis"])
print("\n=== leaderboards_raw_skew_kurtosis ===")
print(lb_sk_df.to_string(index=False))

# %%
# I7: season excluded (constant=-1, stddev=0, no information content).
# rankLevel excluded (constant=1, skewness=-273,614,308.64 is a numerical
# artifact of zero variance, not a meaningful distribution shape).
exclude_cols = {"season", "rankLevel"}
panel_a_cols = ["rank", "rating"]
panel_b_cols = ["wins", "losses", "games", "streak", "drops", "rankCountry"]


def build_bxp_stats(row):
    """Build bxp stats dict from a row of leaderboards_raw_numeric_stats."""
    return {
        "med": float(row["median_val"]),  # median_val is the field name, NOT p50
        "q1": float(row["p25"]),
        "q3": float(row["p75"]),
        "whislo": float(row["p05"]),
        "whishi": float(row["p95"]),
        "fliers": [],
        "label": row["column_name"],
    }


def get_zero_count(col):
    """Look up zero count for a column."""
    rows = lb_zero_df[lb_zero_df['column_name'] == col]
    if rows.empty:
        return 0
    return int(rows.iloc[0]['zero_count'])


def get_skewness(col):
    """Look up skewness for a column."""
    rows = lb_sk_df[lb_sk_df['column_name'] == col]
    if rows.empty:
        return float("nan")
    return float(rows.iloc[0]['skewness'])


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
# Panel A: rating-scale columns
panel_a_data = lb_stats_df[lb_stats_df['column_name'].isin(panel_a_cols)]
bxp_a = [build_bxp_stats(r) for _, r in panel_a_data.iterrows()]
ax1.bxp(bxp_a, showfliers=False, patch_artist=True,
        boxprops=dict(facecolor='#3498db', alpha=0.7))
ax1.set_title('leaderboards_raw: Rating-Scale Columns\n(p05/p25/median/p75/p95)')
ax1.set_ylabel("Value")
for i, col in enumerate(panel_a_cols):
    z = get_zero_count(col)
    s = get_skewness(col)
    ax1.annotate(
        f'zeros={z:,}\nskew={s:.2f}',
        xy=(i + 1, ax1.get_ylim()[0]),
        ha='center', fontsize=7, color='#333333'
    )
# Panel B: activity-count columns with symlog y-axis
panel_b_data = lb_stats_df[lb_stats_df['column_name'].isin(panel_b_cols)]
bxp_b = [build_bxp_stats(r) for _, r in panel_b_data.iterrows()]
ax2.bxp(bxp_b, showfliers=False, patch_artist=True,
        boxprops=dict(facecolor='#e67e22', alpha=0.7))
ax2.set_yscale("symlog")
ax2.set_title('leaderboards_raw: Activity-Count Columns\n(symlog scale, p05/p25/median/p75/p95)')
ax2.set_ylabel("Value (symlog)")
for i, col in enumerate(panel_b_cols):
    z = get_zero_count(col)
    s = get_skewness(col)
    ax2.annotate(
        f'zeros={z:,}\nskew={s:.2f}',
        xy=(i + 1, ax2.get_ylim()[0]),
        ha='center', fontsize=7, color='#333333'
    )
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_leaderboards_boxplots.png", dpi=150)
plt.close()
print("Saved: 01_02_05_leaderboards_boxplots.png")

# %% [markdown]
# ## T07 -- Plot 9: Completeness matrix (NULL rate bar chart for 55 matches_raw columns)

# %%
# Horizontal bar chart used instead of heatmap: with 55 columns and a single
# NULL-rate dimension (no row-level structure), a heatmap adds no information
# over a bar chart. The bar chart provides higher information density per
# EDA Manual Section 7 (anti cherry-picking).
null_df_plot = pd.DataFrame(census["matches_raw_null_census"])
print(f"=== matches_raw NULL rates ({len(null_df_plot)} columns) ===")
print(null_df_plot.sort_values('null_pct', ascending=False).to_string(index=False))

# %%
null_df_sorted = null_df_plot.sort_values('null_pct', ascending=True)
# I7: <1% green (MCAR-safe per EDA Manual Section 4.5); 1-10% orange (moderate;
# warrants investigation); >10% red (severe; feature flagged for cleaning phase)
colors = []
for pct in null_df_sorted['null_pct']:
    if pct < 1:
        colors.append('#2ecc71')   # green: < 1%
    elif pct < 10:
        colors.append('#f39c12')   # orange: 1-10%
    else:
        colors.append('#e74c3c')   # red: > 10%
fig, ax = plt.subplots(figsize=(12, 16))
ax.barh(null_df_sorted['column_name'], null_df_sorted['null_pct'], color=colors)
ax.set_xlabel("NULL %")
ax.set_title("matches_raw: Column NULL Rates (55 columns)")
ax.axvline(x=1, color='gray', linestyle='--', alpha=0.5, label='1%')
ax.axvline(x=10, color='gray', linestyle=':', alpha=0.5, label='10%')
ax.legend()
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_completeness_matrix.png", dpi=150)
plt.close()
print("Saved: 01_02_05_completeness_matrix.png")

# %% [markdown]
# ## T08 -- Plot 10: profiles_raw NULL rates

# %%
profiles_null_df = pd.DataFrame(census["profiles_raw_null_census"])
print(f"=== profiles_raw NULL rates ({len(profiles_null_df)} columns) ===")
print(profiles_null_df.sort_values('null_pct', ascending=False).to_string(index=False))

# %%
profiles_null_sorted = profiles_null_df.sort_values('null_pct', ascending=True)
profile_colors = []
for pct in profiles_null_sorted['null_pct']:
    if pct >= 100:
        profile_colors.append('#e74c3c')   # red: dead column
    else:
        profile_colors.append('#3498db')   # blue: live column
fig, ax = plt.subplots(figsize=(10, max(5, len(profiles_null_sorted) * 0.4)))
bars = ax.barh(
    profiles_null_sorted['column_name'],
    profiles_null_sorted['null_pct'],
    color=profile_colors,
    edgecolor='black', linewidth=0.3
)
# Annotate dead bars
for bar, pct, col in zip(bars, profiles_null_sorted['null_pct'],
                         profiles_null_sorted['column_name']):
    if pct >= 100:
        ax.text(
            bar.get_width() / 2, bar.get_y() + bar.get_height() / 2,
            'DEAD', ha='center', va='center', fontsize=8,
            fontweight='bold', color='white'
        )
ax.set_xlabel("NULL %")
ax.set_title("profiles_raw: Column NULL Rates (red=DEAD, blue=live)")
ax.axvline(x=100, color='gray', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_profiles_null_rates.png", dpi=150)
plt.close()
print("Saved: 01_02_05_profiles_null_rates.png")
dead_cols = profiles_null_sorted[profiles_null_sorted['null_pct'] >= 100]['column_name'].tolist()
print(f"Dead columns ({len(dead_cols)}): {dead_cols}")

# %% [markdown]
# ## T09 -- Plot 11: leaderboards_raw.leaderboard top-k

# %%
lb_leaderboard = pd.DataFrame(census["leaderboards_raw_categorical"]["leaderboard"])
print(f"=== leaderboards_raw.leaderboard ({len(lb_leaderboard)} values) ===")
print(lb_leaderboard.to_string(index=False))

# %%
lb_leaderboard_sorted = lb_leaderboard.sort_values('cnt', ascending=True)
fig, ax = plt.subplots(figsize=(10, max(4, len(lb_leaderboard_sorted) * 0.45)))
bars = ax.barh(lb_leaderboard_sorted['value'], lb_leaderboard_sorted['cnt'],
               color='#2980b9', edgecolor='black', linewidth=0.3)
for bar, cnt in zip(bars, lb_leaderboard_sorted['cnt']):
    ax.text(
        bar.get_width() + bar.get_width() * 0.01, bar.get_y() + bar.get_height() / 2,
        f'{cnt:,}', va='center', ha='left', fontsize=9
    )
ax.set_xlabel("Row count")
ax.set_title("leaderboards_raw: leaderboard Distribution")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_lb_leaderboard_distribution.png", dpi=150)
plt.close()
print("Saved: 01_02_05_lb_leaderboard_distribution.png")

# %% [markdown]
# ## T10 -- Plot 12: Boolean columns stacked bar

# %%
bool_df = pd.DataFrame(census["boolean_census"])
print(f"=== boolean_census ({len(bool_df)} columns) ===")
print(bool_df.to_string(index=False))

# %%
total = census["matches_raw_total_rows"]
bool_df['true_pct'] = 100.0 * bool_df['true_count'] / total
bool_df['false_pct'] = 100.0 * bool_df['false_count'] / total
bool_df['null_pct_calc'] = 100.0 * bool_df['null_count'] / total
fig, ax = plt.subplots(figsize=(12, 8))
y = range(len(bool_df))
ax.barh(y, bool_df['true_pct'], color='#2ecc71', label='TRUE')
ax.barh(y, bool_df['false_pct'], left=bool_df['true_pct'],
        color='#e74c3c', label='FALSE')
ax.barh(y, bool_df['null_pct_calc'],
        left=bool_df['true_pct'] + bool_df['false_pct'],
        color='#95a5a6', label='NULL')
ax.set_yticks(list(y))
ax.set_yticklabels(bool_df['column_name'])
ax.set_xlabel("Percentage")
ax.set_title("Boolean Column Proportions -- matches_raw")
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_boolean_stacked.png", dpi=150)
plt.close()
print(f"Saved: 01_02_05_boolean_stacked.png ({len(bool_df)} boolean columns)")

# %% [markdown]
# ## T11 -- Plot 13: Monthly match volume line chart

# %%
monthly_df = con.execute('''
    SELECT
        DATE_TRUNC('month', started) AS month,
        COUNT(DISTINCT matchId) AS distinct_matches,
        COUNT(*) AS total_rows
    FROM matches_raw
    WHERE started IS NOT NULL
    GROUP BY month
    ORDER BY month
''').df()
print("=== monthly match volume (feeds line chart) ===")
print("Head:")
print(monthly_df.head(5).to_string(index=False))
print("Tail:")
print(monthly_df.tail(5).to_string(index=False))

# %%
ratings_start = census["temporal_range_ratings"][0]["earliest_rating"]
print(f"ratings_raw earliest_rating (reference line): {ratings_start}")
monthly_df['month'] = pd.to_datetime(monthly_df['month'])
ratings_start_dt = pd.to_datetime(ratings_start)
fig, ax1 = plt.subplots(figsize=(14, 6))
color_matches = '#2980b9'
color_rows = '#e74c3c'
ax1.plot(monthly_df['month'], monthly_df['distinct_matches'],
         color=color_matches, linewidth=1.5, label='distinct_matches')
ax1.set_xlabel("Month")
ax1.set_ylabel("Distinct Matches", color=color_matches)
ax1.tick_params(axis='y', labelcolor=color_matches)
ax2 = ax1.twinx()
ax2.plot(monthly_df['month'], monthly_df['total_rows'],
         color=color_rows, linewidth=1.5, linestyle='--', label='total_rows')
ax2.set_ylabel("Total Rows", color=color_rows)
ax2.tick_params(axis='y', labelcolor=color_rows)
ax1.axvline(x=ratings_start_dt, color='purple', linestyle=':', linewidth=1.5,
            label='ratings_raw start')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax1.set_title("Monthly Match Volume -- matches_raw")
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_monthly_volume.png", dpi=150)
plt.close()
print("Saved: 01_02_05_monthly_volume.png")
print(f"Time range: {monthly_df['month'].min()} to {monthly_df['month'].max()}")

# %% [markdown]
# ## T12 -- Write markdown summary artifact and close

# %%
sql_queries = {
    "rating_histogram": (
        "SELECT (FLOOR(rating / 100) * 100)::INTEGER AS bin, COUNT(*) AS cnt\n"
        "FROM matches_raw WHERE rating IS NOT NULL\n"
        "GROUP BY bin ORDER BY bin"
    ),
    "ratingDiff_histogram": (
        'SELECT (FLOOR(\"ratingDiff\" / 10) * 10)::INTEGER AS bin, COUNT(*) AS cnt\n'
        'FROM matches_raw WHERE \"ratingDiff\" IS NOT NULL\n'
        "GROUP BY bin ORDER BY bin"
    ),
    "monthly_volume": (
        "SELECT\n"
        "    DATE_TRUNC('month', started) AS month,\n"
        "    COUNT(DISTINCT matchId) AS distinct_matches,\n"
        "    COUNT(*) AS total_rows\n"
        "FROM matches_raw\n"
        "WHERE started IS NOT NULL\n"
        "GROUP BY month\n"
        "ORDER BY month"
    ),
}
plots_info = [
    ("01_02_05_won_distribution.png", "Plot 1: won Distribution Bar Chart",
     "Vertical bar chart showing TRUE/FALSE/NULL counts for matches_raw.won; "
     "reveals ~4.69% NULL rate on the prediction target."),
    ("01_02_05_won_consistency.png", "Plot 2: Intra-Match won Consistency Stacked Bar",
     f"Stacked bar showing intra-match consistency categories for 2-player matches; "
     f"~{inconsistent_pct:.2f}% of matches have both_true or both_false labels."),
    ("01_02_05_leaderboard_distribution.png", "Plot 3: matches_raw.leaderboard Distribution",
     "Horizontal bar chart of leaderboard values in matches_raw."),
    ("01_02_05_civ_top30.png", "Plot 4: matches_raw.civ Top 30",
     "Horizontal bar chart of top-30 civilization values in matches_raw."),
    ("01_02_05_map_top30.png", "Plot 5: matches_raw.map Top 30",
     "Horizontal bar chart of top-30 map values in matches_raw."),
    ("01_02_05_rating_histogram.png", "Plot 6: matches_raw.rating Histogram",
     "Histogram with bin_width=100 showing rating distribution; skew=0.5662, kurt=1.6157."),
    ("01_02_05_ratingDiff_histogram.png", "Plot 7: matches_raw.ratingDiff Histogram",
     "Histogram with bin_width=10 showing ratingDiff distribution; skew=0.1105, kurt=0.8900."),
    ("01_02_05_leaderboards_boxplots.png", "Plot 8: leaderboards_raw Numeric Boxplots (two-panel)",
     "Two-panel boxplots (rating-scale and activity-count with symlog scale); "
     "season and rankLevel excluded as constants."),
    ("01_02_05_completeness_matrix.png", "Plot 9: matches_raw Completeness Matrix (55 columns)",
     "Horizontal bar chart of NULL % for all 55 matches_raw columns, "
     "color-coded green/orange/red by severity."),
    ("01_02_05_profiles_null_rates.png", "Plot 10: profiles_raw NULL Rates",
     "Horizontal bar chart distinguishing 100% NULL (dead) columns from live columns in profiles_raw."),
    ("01_02_05_lb_leaderboard_distribution.png",
     "Plot 11: leaderboards_raw.leaderboard Distribution",
     "Horizontal bar chart of leaderboard type counts in leaderboards_raw."),
    ("01_02_05_boolean_stacked.png", "Plot 12: matches_raw Boolean Column Proportions",
     "Stacked bar chart showing TRUE/FALSE/NULL proportions for all 18 boolean columns."),
    ("01_02_05_monthly_volume.png", "Plot 13: Monthly Match Volume",
     "Dual-axis line chart of monthly distinct match count and total rows; "
     "vertical reference line marks ratings_raw start (2022-09-10)."),
]
md_lines = [
    "# Step 01_02_05 -- Univariate Census Visualizations: aoe2companion",
    "",
    "**Generated by:** `sandbox/aoe2/aoe2companion/01_exploration/02_eda/01_02_05_visualizations.py`",
    "**Source artifact:** `01_02_04_univariate_census.json`",
    "**Plots directory:** `artifacts/01_exploration/02_eda/plots/`",
    "",
    "## Plots",
    "",
]
for filename, title, caption in plots_info:
    md_lines.append(f"### {title}")
    md_lines.append("")
    md_lines.append(f"**File:** `plots/{filename}`")
    md_lines.append("")
    md_lines.append(f"**Caption:** {caption}")
    md_lines.append("")
md_lines += [
    "## SQL Queries (Invariant #6 -- Reproducibility)",
    "",
    "All DuckDB SQL queries used to produce plots in this notebook are listed verbatim below.",
    "Any plot produced from a DuckDB query can be reproduced by running the query against",
    "the persistent `aoe2companion` DuckDB.",
    "",
    "### rating histogram (Plot 6)",
    "",
    "```sql",
    sql_queries["rating_histogram"],
    "```",
    "",
    "### ratingDiff histogram (Plot 7)",
    "",
    "```sql",
    sql_queries["ratingDiff_histogram"],
    "```",
    "",
    "### monthly match volume (Plot 13)",
    "",
    "```sql",
    sql_queries["monthly_volume"],
    "```",
    "",
]
md_content = '\n'.join(md_lines)
md_path = artifacts_dir / "01_02_05_visualizations.md"
with open(md_path, 'w') as f:
    f.write(md_content)
print(f"Written: {md_path}")
print("\n=== Plot file verification ===")
all_ok = True
for filename, title, _ in plots_info:
    png_path = plots_dir / filename
    exists = png_path.exists()
    status = "OK" if exists else "MISSING"
    print(f"  {status}: {filename}")
    if not exists:
        all_ok = False
print(f"\nAll 13 plots present: {all_ok}")

# %%
con.close()
print("DB connection closed.")
