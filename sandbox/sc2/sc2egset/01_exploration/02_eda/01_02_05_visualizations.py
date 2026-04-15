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
# # Step 01_02_05 -- Univariate EDA Visualizations
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_02 -- EDA (Tukey-style)
# **Dataset:** sc2egset
# **Question:** What do the distributions from 01_02_04 look like visually,
# and do the visual patterns confirm or challenge the statistical summaries?
# **Invariants applied:** #6 (reproducibility -- queries inlined),
# #7 (no magic numbers), #9 (step scope: visualization of 01_02_04 findings)
# **Predecessor:** 01_02_04 (univariate census -- JSON artifact required)
# **Step scope:** visualize
# **Type:** Read-only -- no DuckDB writes

# %%
import json
from pathlib import Path

import duckdb
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from rts_predict.common.notebook_utils import get_reports_dir, setup_notebook_logging
from rts_predict.games.sc2.config import DB_FILE

matplotlib.use("Agg")
logger = setup_notebook_logging()
logger.info("DB_FILE: %s", DB_FILE)

# %%
con = duckdb.connect(str(DB_FILE), read_only=True)
print(f"Connected (read-only): {DB_FILE}")

# %%
census_json_path = (
    get_reports_dir("sc2", "sc2egset")
    / "artifacts" / "01_exploration" / "02_eda"
    / "01_02_04_univariate_census.json"
)
with open(census_json_path) as f:
    census = json.load(f)
print(f"Loaded 01_02_04 artifact: {len(census)} keys")

# %%
REQUIRED_KEYS = [
    "result_distribution",
    "categorical_profiles",
    "monthly_counts",
    "mmr_zero_interpretation",
    "isInClan_distribution",
    "clanTag_top20",
]
missing = [k for k in REQUIRED_KEYS if k not in census]
assert not missing, (
    f"BLOCKER: 01_02_04 artifact incomplete. Missing keys: {missing}. "
    "Execute plan_sc2egset_01_02_04_pass2 before running this notebook."
)
print(f"Prerequisite check PASSED. All {len(REQUIRED_KEYS)} required keys present.")

# %%
artifacts_dir = (
    get_reports_dir("sc2", "sc2egset")
    / "artifacts" / "01_exploration" / "02_eda"
)
plots_dir = artifacts_dir / "plots"
plots_dir.mkdir(parents=True, exist_ok=True)
print(f"Artifacts dir: {artifacts_dir}")
print(f"Plots dir: {plots_dir}")

# %% [markdown]
# ## Plot 1: Result Distribution

# %%
result_dist = pd.DataFrame(census["result_distribution"])
print("=== Result distribution data for plot ===")
print(result_dist.to_string(index=False))

# %%
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(result_dist["result"], result_dist["cnt"], color="steelblue")
for bar, cnt in zip(bars, result_dist["cnt"]):
    ax.annotate(
        f"{cnt:,}",
        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
        xytext=(0, 4),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=10,
    )
ax.set_xlabel("Result")
ax.set_ylabel("Count")
ax.set_title("Result Distribution (replay_players_raw)")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_result_bar.png", dpi=120)
plt.close()
print(f"Saved: {plots_dir / '01_02_05_result_bar.png'}")

# %% [markdown]
# ## Plot 2: Categorical Distributions

# %%
cat_race = pd.DataFrame(census["categorical_profiles"]["race"])
print("=== race data for plot ===")
print(cat_race.to_string(index=False))

# %%
cat_league = pd.DataFrame(census["categorical_profiles"]["highestLeague"])
print("=== highestLeague data for plot ===")
print(cat_league.to_string(index=False))

# %%
cat_region = pd.DataFrame(census["categorical_profiles"]["region"])
print("=== region data for plot ===")
print(cat_region.to_string(index=False))

# %%
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, col, df in zip(
    axes,
    ["race", "highestLeague", "region"],
    [cat_race, cat_league, cat_region],
):
    df_sorted = df.sort_values("cnt", ascending=True)
    bars = ax.barh(df_sorted[col], df_sorted["cnt"], color="steelblue")
    for bar, cnt in zip(bars, df_sorted["cnt"]):
        ax.annotate(
            f"{cnt:,}",
            xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
            xytext=(4, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=8,
        )
    ax.set_title(col)
    ax.set_xlabel("Count")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.suptitle("Categorical Distributions (replay_players_raw)", fontsize=13)
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_categorical_bars.png", dpi=120)
plt.close()
print(f"Saved: {plots_dir / '01_02_05_categorical_bars.png'}")

# %% [markdown]
# ## Plot 3: selectedRace Distribution

# %%
sel_race_data = pd.DataFrame(census["categorical_profiles"]["selectedRace"])
print("=== selectedRace data for plot ===")
print(sel_race_data.to_string(index=False))

# %%
sel_race_sorted = sel_race_data.sort_values("cnt", ascending=True)
colors = [
    "tomato" if r == "" else "steelblue"
    for r in sel_race_sorted["selectedRace"]
]
labels = [r if r != "" else "(empty string)" for r in sel_race_sorted["selectedRace"]]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(labels, sel_race_sorted["cnt"], color=colors)
for bar, cnt in zip(bars, sel_race_sorted["cnt"]):
    ax.annotate(
        f"{cnt:,}",
        xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
        xytext=(4, 0),
        textcoords="offset points",
        ha="left",
        va="center",
        fontsize=9,
    )
ax.set_xlabel("Count")
ax.set_title("selectedRace Distribution (replay_players_raw)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
print("Compare with race: 1,110 empty strings (2.48%), 10 Rand picks (0.02%)")
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_selectedrace_bar.png", dpi=120)
plt.close()
print(f"Saved: {plots_dir / '01_02_05_selectedrace_bar.png'}")

# %% [markdown]
# ## Plot 4: MMR Distribution (Split View)

# %%
mmr_data = con.execute(
    "SELECT MMR FROM replay_players_raw WHERE MMR IS NOT NULL"
).df()
print(f"=== Full MMR data for plot ({len(mmr_data):,} rows) ===")
print(mmr_data["MMR"].describe().to_string())

# %%
n_zero = (mmr_data["MMR"] == 0).sum()
n_negative = (mmr_data["MMR"] < 0).sum()
n_positive = (mmr_data["MMR"] > 0).sum()
print(f"MMR=0: {n_zero:,}, MMR<0: {n_negative:,}, MMR>0: {n_positive:,}")
mmr_annotation = (
    f"N={n_zero + n_negative:,} rows with MMR<=0 excluded"
    f" (incl. {n_negative:,} negative-MMR)"
)
print(f"Annotation: {mmr_annotation}")

# %%
mmr_positive = mmr_data[mmr_data["MMR"] > 0]
print(f"=== MMR > 0 data for plot ({len(mmr_positive):,} rows) ===")
print(mmr_positive["MMR"].describe().to_string())

# %%
fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(14, 5))

# I7: Sturges rule: ceil(1+log2(44817))=16 bins minimum; 50 bins provides
# finer resolution for shape assessment per Tukey (1977) visual consistency
# recommendation for exploratory work
ax_a.hist(mmr_data["MMR"], bins=50, color="steelblue", edgecolor="white")
ax_a.set_title("MMR (all rows)")
ax_a.set_xlabel("MMR")
ax_a.set_ylabel("Count")
ax_a.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))

# I7: same justification as subplot (a)
ax_b.hist(mmr_positive["MMR"], bins=50, color="steelblue", edgecolor="white")
ax_b.set_title("MMR (excluding zero)")
ax_b.set_xlabel("MMR")
ax_b.set_ylabel("Count")
ax_b.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax_b.annotate(
    mmr_annotation,
    xy=(0.97, 0.97),
    xycoords="axes fraction",
    ha="right",
    va="top",
    fontsize=8,
    bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow"),
)

plt.suptitle("MMR Distribution (replay_players_raw)", fontsize=13)
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_mmr_split.png", dpi=120)
plt.close()
print(f"Saved: {plots_dir / '01_02_05_mmr_split.png'}")

# %% [markdown]
# ## Plot 5: APM Distribution

# %%
apm_data = con.execute(
    "SELECT APM FROM replay_players_raw WHERE APM IS NOT NULL"
).df()
print(f"=== APM data for plot ({len(apm_data):,} rows) ===")
print(apm_data["APM"].describe().to_string())

# %%
apm_median = apm_data["APM"].median()
apm_max = apm_data["APM"].max()

fig, ax = plt.subplots(figsize=(10, 6))
# I7: Sturges rule: ceil(1+log2(44817))=16 bins minimum; 50 bins provides
# finer resolution for shape assessment per Tukey (1977) visual consistency
# recommendation for exploratory work
ax.hist(apm_data["APM"], bins=50, color="steelblue", edgecolor="white")
ax.axvline(apm_median, color="darkorange", linestyle="--", linewidth=1.5,
           label=f"Median={apm_median:.0f}")
ax.annotate(
    f"Max APM={apm_max:,.0f}",
    xy=(0.97, 0.97),
    xycoords="axes fraction",
    ha="right",
    va="top",
    fontsize=9,
    bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow"),
)
ax.set_xlabel("APM")
ax.set_ylabel("Count")
ax.set_title("APM Distribution (replay_players_raw)")
ax.legend()
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_apm_hist.png", dpi=120)
plt.close()
print(f"Saved: {plots_dir / '01_02_05_apm_hist.png'}")

# %% [markdown]
# ## Plot 6: SQ Distribution (Split View)

# %%
sq_data = con.execute(
    "SELECT SQ FROM replay_players_raw WHERE SQ IS NOT NULL"
).df()
print(f"=== Full SQ data for plot ({len(sq_data):,} rows) ===")
print(sq_data["SQ"].describe().to_string())

# %%
sq_clean = sq_data[sq_data["SQ"] != -2147483648]
print(f"=== SQ excluding sentinel ({len(sq_clean):,} rows) ===")
print(sq_clean["SQ"].describe().to_string())

# %%
fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(14, 5))

# I7: Sturges rule: ceil(1+log2(44817))=16 bins minimum; 50 bins provides
# finer resolution for shape assessment per Tukey (1977) visual consistency
# recommendation for exploratory work
ax_a.hist(sq_data["SQ"], bins=50, color="steelblue", edgecolor="white")
ax_a.set_title("SQ (all rows, sentinel visible)")
ax_a.set_xlabel("SQ")
ax_a.set_ylabel("Count")
ax_a.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))

# I7: same justification as subplot (a)
ax_b.hist(sq_clean["SQ"], bins=50, color="steelblue", edgecolor="white")
ax_b.set_title("SQ (sentinel excluded, range -51 to 187)")
ax_b.set_xlabel("SQ")
ax_b.set_ylabel("Count")
ax_b.annotate(
    "2 sentinel rows excluded (INT32_MIN = -2,147,483,648)",
    xy=(0.97, 0.97),
    xycoords="axes fraction",
    ha="right",
    va="top",
    fontsize=8,
    bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow"),
)

plt.suptitle("SQ Distribution (replay_players_raw)", fontsize=13)
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_sq_split.png", dpi=120)
plt.close()
print(f"Saved: {plots_dir / '01_02_05_sq_split.png'}")

# %% [markdown]
# ## Plot 7: supplyCappedPercent Distribution

# %%
sc_data = con.execute(
    "SELECT supplyCappedPercent"
    " FROM replay_players_raw"
    " WHERE supplyCappedPercent IS NOT NULL"
).df()
print(f"=== supplyCappedPercent data ({len(sc_data):,} rows) ===")
print(sc_data["supplyCappedPercent"].describe().to_string())

# %%
sc_median = sc_data["supplyCappedPercent"].median()

fig, ax = plt.subplots(figsize=(10, 6))
# I7: Sturges rule: ceil(1+log2(44817))=16 bins minimum; 50 bins provides
# finer resolution for shape assessment per Tukey (1977) visual consistency
# recommendation for exploratory work
ax.hist(sc_data["supplyCappedPercent"], bins=50, color="steelblue", edgecolor="white")
ax.axvline(sc_median, color="darkorange", linestyle="--", linewidth=1.5,
           label=f"Median={sc_median:.1f}")
ax.set_xlabel("supplyCappedPercent")
ax.set_ylabel("Count")
ax.set_title("supplyCappedPercent Distribution (replay_players_raw)")
ax.legend()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_supplycapped_hist.png", dpi=120)
plt.close()
print(f"Saved: {plots_dir / '01_02_05_supplycapped_hist.png'}")

# %% [markdown]
# ## Plot 8: Game Duration (elapsed_game_loops)

# %%
duration_data = con.execute(
    "SELECT header.elapsedGameLoops AS elapsed_game_loops"
    " FROM replays_meta_raw"
    " WHERE header.elapsedGameLoops IS NOT NULL"
).df()
# Convert game loops to seconds: SC2 Faster speed = 22.4 loops/second
LOOPS_PER_SECOND = 22.4  # I7: SC2 engine constant for Faster speed
duration_data["duration_sec"] = (
    duration_data["elapsed_game_loops"] / LOOPS_PER_SECOND
)
print(f"=== Duration data ({len(duration_data):,} replays) ===")
print(duration_data["duration_sec"].describe().to_string())

# %%
CLIP_SECONDS = 2400  # I7: 40 minutes = standard "long game" boundary
n_over_40min = (duration_data["duration_sec"] > CLIP_SECONDS).sum()

fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(14, 5))

# I7: Sturges rule: ceil(1+log2(22390))=15 bins minimum; 50 bins provides
# finer resolution for shape assessment per Tukey (1977) visual consistency
# recommendation for exploratory work
ax_a.hist(duration_data["duration_sec"], bins=50, color="steelblue", edgecolor="white")
ax_a.set_title("Game Duration (full range)")
ax_a.set_xlabel("Duration (seconds)")
ax_a.set_ylabel("Count")
ax_a.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))

# I7: same justification as subplot (a)
clipped = duration_data[duration_data["duration_sec"] <= CLIP_SECONDS]
ax_b.hist(clipped["duration_sec"], bins=50, color="steelblue", edgecolor="white")
ax_b.set_title("Game Duration (clipped at 40 min)")
ax_b.set_xlabel("Duration (seconds)")
ax_b.set_ylabel("Count")
ax_b.annotate(
    f"N={n_over_40min:,} replays > 40 min (not shown)",
    xy=(0.95, 0.95),
    xycoords="axes fraction",
    ha="right",
    va="top",
    fontsize=9,
    bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow"),
)

plt.suptitle("Game Duration from elapsed_game_loops (replays_meta_raw)", fontsize=13)
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_duration_hist.png", dpi=120)
plt.close()
print(f"Saved: {plots_dir / '01_02_05_duration_hist.png'}")

# %% [markdown]
# ## Plot 9: MMR Zero-Spike by Result and by highestLeague

# %%
mmr_by_result = pd.DataFrame(
    census["mmr_zero_interpretation"]["by_result"]
)
print("=== MMR=0 by result ===")
print(mmr_by_result.to_string(index=False))

# %%
mmr_by_league = pd.DataFrame(
    census["mmr_zero_interpretation"]["by_highestLeague"]
)
print("=== MMR=0 by highestLeague ===")
print(mmr_by_league.to_string(index=False))

# %%
overall_mmr_zero_pct = 100.0 * sum(
    r["mmr_zero_cnt"]
    for r in census["mmr_zero_interpretation"]["by_result"]
) / sum(
    r["total_cnt"]
    for r in census["mmr_zero_interpretation"]["by_result"]
)
print(f"Overall MMR=0 rate: {overall_mmr_zero_pct:.2f}%")

fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(14, 5))

ax_a.bar(mmr_by_result["result"], mmr_by_result["mmr_zero_pct"], color="steelblue")
ax_a.axhline(overall_mmr_zero_pct, color="darkorange", linestyle="--",
             linewidth=1.5, label=f"Overall {overall_mmr_zero_pct:.1f}%")
ax_a.set_title("MMR=0 Rate by Result")
ax_a.set_xlabel("Result")
ax_a.set_ylabel("MMR=0 %")
ax_a.set_ylim(0, 100)
ax_a.legend(fontsize=8)

ax_b.bar(mmr_by_league["highestLeague"], mmr_by_league["mmr_zero_pct"],
         color="steelblue")
ax_b.axhline(overall_mmr_zero_pct, color="darkorange", linestyle="--",
             linewidth=1.5, label=f"Overall {overall_mmr_zero_pct:.1f}%")
ax_b.set_title("MMR=0 Rate by highestLeague")
ax_b.set_xlabel("highestLeague")
ax_b.set_ylabel("MMR=0 %")
ax_b.set_ylim(0, 100)
ax_b.legend(fontsize=8)
plt.setp(ax_b.get_xticklabels(), rotation=30, ha="right")

plt.suptitle("MMR Zero-Spike Cross-Tabulation (replay_players_raw)", fontsize=13)
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_mmr_zero_interpretation.png", dpi=120)
plt.close()
print(f"Saved: {plots_dir / '01_02_05_mmr_zero_interpretation.png'}")

# %% [markdown]
# ## Plot 10: Temporal Coverage

# %%
monthly = pd.DataFrame(census["monthly_counts"])
print(f"=== Monthly counts ({len(monthly)} months) ===")
print(monthly.to_string(index=False))

# %%
monthly["month"] = pd.to_datetime(monthly["month"])

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly["month"], monthly["cnt"], marker="o", linewidth=1.5,
        markersize=4, color="steelblue")

low_months = monthly[monthly["cnt"] < 50]
for _, row in low_months.iterrows():
    ax.annotate(
        f"{int(row['cnt'])}",
        xy=(row["month"], row["cnt"]),
        xytext=(0, 8),
        textcoords="offset points",
        ha="center",
        fontsize=7,
        color="tomato",
    )

ax.set_xlabel("Month")
ax.set_ylabel("Replay Count")
ax.set_title("Temporal Coverage — Monthly Replay Counts (replays_meta_raw)")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_temporal_coverage.png", dpi=120)
plt.close()
print(f"Saved: {plots_dir / '01_02_05_temporal_coverage.png'}")

# %% [markdown]
# ## Plot 11: isInClan Distribution

# %%
clan_dist = pd.DataFrame(census["isInClan_distribution"])
print("=== isInClan distribution ===")
print(clan_dist.to_string(index=False))

# %%
total_clan = clan_dist["cnt"].sum()

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(
    [str(v) for v in clan_dist["isInClan"]],
    clan_dist["cnt"],
    color="steelblue",
)
for bar, row in zip(bars, clan_dist.itertuples()):
    pct = 100.0 * row.cnt / total_clan
    ax.annotate(
        f"{row.cnt:,}\n({pct:.1f}%)",
        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
        xytext=(0, 4),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=10,
    )
ax.set_xlabel("isInClan")
ax.set_ylabel("Count")
ax.set_title("isInClan Distribution (replay_players_raw)")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_isinclan_bar.png", dpi=120)
plt.close()
print(f"Saved: {plots_dir / '01_02_05_isinclan_bar.png'}")

# %% [markdown]
# ## Plot 12: clanTag Top-20

# %%
clan_top20 = pd.DataFrame(census["clanTag_top20"])
print("=== clanTag top-20 ===")
print(clan_top20.to_string(index=False))

# %%
clan_sorted = clan_top20.sort_values("cnt", ascending=True)

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(clan_sorted["clanTag"], clan_sorted["cnt"], color="steelblue")
for bar, cnt in zip(bars, clan_sorted["cnt"]):
    ax.annotate(
        f"{cnt:,}",
        xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
        xytext=(4, 0),
        textcoords="offset points",
        ha="left",
        va="center",
        fontsize=8,
    )
ax.set_xlabel("Count")
ax.set_title("Top-20 clanTag by Frequency (replay_players_raw)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
plt.savefig(plots_dir / "01_02_05_clantag_top20.png", dpi=120)
plt.close()
print(f"Saved: {plots_dir / '01_02_05_clantag_top20.png'}")

# %% [markdown]
# ## Summary and Markdown Artifact

# %%
# Verify all 12 plot files exist
expected_plots = [
    "01_02_05_result_bar.png",
    "01_02_05_categorical_bars.png",
    "01_02_05_selectedrace_bar.png",
    "01_02_05_mmr_split.png",
    "01_02_05_apm_hist.png",
    "01_02_05_sq_split.png",
    "01_02_05_supplycapped_hist.png",
    "01_02_05_duration_hist.png",
    "01_02_05_mmr_zero_interpretation.png",
    "01_02_05_temporal_coverage.png",
    "01_02_05_isinclan_bar.png",
    "01_02_05_clantag_top20.png",
]
missing_plots = [p for p in expected_plots if not (plots_dir / p).exists()]
assert not missing_plots, f"Missing plots: {missing_plots}"
print(f"All {len(expected_plots)} plot files verified present.")

# %%
md_content = f"""# Step 01_02_05 -- Univariate EDA Visualizations

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
"""

md_path = artifacts_dir / "01_02_05_visualizations.md"
with open(md_path, "w") as f:
    f.write(md_content)
print(f"Written markdown artifact: {md_path}")

# %%
con.close()
print("DuckDB connection closed.")
print(f"Step 01_02_05 complete. {len(expected_plots)} plots + 1 markdown artifact produced.")
