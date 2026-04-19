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
# # Step 01_05_06 -- Q8: DGP Diagnostics -- duration_seconds (sc2egset)
#
# **spec:** reports/specs/01_05_preregistration.md@7e259dd8
# **Dataset:** sc2egset
# **Branch:** feat/01-05-sc2egset
# **Date:** 2026-04-18
#
# **Objective:** Per-quarter summary statistics + Cohen's d vs reference for
# duration_seconds. POST_GAME diagnostic only (not a pre-game feature).
#
# **Critique M9 fix:** JOIN matches_flat_clean to compute per-quarter
# AVG(is_duration_suspicious) instead of reporting NULL.
#
# **Literature:**
# - Cohen (1988) §2.2: d = (mean_q - mean_ref) / pooled_sd

# %%
# spec: reports/specs/01_05_preregistration.md@7e259dd8
# Step 01_05_06 -- Q8 DGP diagnostics duration_seconds (sc2egset)
# Dataset: sc2egset  Branch: feat/01-05-sc2egset  Date: 2026-04-18

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir

matplotlib.use("Agg")

# %%
db = get_notebook_db("sc2", "sc2egset", read_only=True)
reports_dir = get_reports_dir("sc2", "sc2egset")
artifact_dir = reports_dir / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
plots_dir = artifact_dir / "plots"
plots_dir.mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ## Hypothesis

# %%
# Hypothesis: duration_seconds mean/median drifts by < 5% across the 8 tested
# quarters vs reference (tournament formats stable).
# Falsifier: any tested-quarter Cohen's d > 0.2 (small effect threshold)
# would be notable and needs calling out.

# %% [markdown]
# ## Per-quarter duration statistics (M9 fix: join matches_flat_clean)

# %%
DGP_SQL = """
-- M9 fix: JOIN matches_flat_clean to get is_duration_suspicious
WITH tagged AS (
  SELECT
    CASE
      WHEN m.started_at BETWEEN TIMESTAMP '2022-08-29' AND TIMESTAMP '2022-12-31'
           THEN 'reference'
      ELSE CAST(date_part('year', m.started_at) AS VARCHAR) || '-Q' ||
             CAST(date_part('quarter', m.started_at) AS VARCHAR)
    END AS period_tag,
    m.duration_seconds,
    mfc.is_duration_suspicious
  FROM matches_history_minimal m
  JOIN matches_flat_clean mfc ON substr(m.match_id, 11) = mfc.replay_id
  WHERE m.started_at >= TIMESTAMP '2022-08-29'
    AND m.started_at <  TIMESTAMP '2025-01-01'
)
SELECT
  period_tag,
  AVG(duration_seconds)                              AS mean_dur,
  MEDIAN(duration_seconds)                           AS median_dur,
  QUANTILE_CONT(duration_seconds, 0.05)              AS p5_dur,
  QUANTILE_CONT(duration_seconds, 0.95)              AS p95_dur,
  QUANTILE_CONT(duration_seconds, 0.75) -
    QUANTILE_CONT(duration_seconds, 0.25)            AS iqr_dur,
  STDDEV_SAMP(duration_seconds)                      AS sd_dur,
  COUNT(*)                                           AS n,
  AVG(CAST(is_duration_suspicious AS DOUBLE))        AS suspicious_rate
FROM tagged
GROUP BY period_tag
ORDER BY period_tag
"""

df_dgp = db.con.execute(DGP_SQL).fetchdf()
print("DGP statistics by period:")
print(df_dgp.to_string())

# %% [markdown]
# ## Cohen's d computation

# %%
# Reference stats
ref_row = df_dgp[df_dgp["period_tag"] == "reference"].iloc[0]
mean_ref = ref_row["mean_dur"]
sd_ref = ref_row["sd_dur"]
n_ref = ref_row["n"]

print(f"Reference: mean={mean_ref:.1f}s, sd={sd_ref:.1f}s, n={n_ref}")

# Tested quarters
df_tested = df_dgp[df_dgp["period_tag"] != "reference"].copy()

# Validate B1: all period tags in tested are YYYY-QN format
import re
pattern = r"^\d{4}-Q[1-4]$"
assert df_tested["period_tag"].str.match(pattern).all(), "Bad period tags in DGP output!"
print("B1 assertion PASS: tested period tags match YYYY-Q[1-4] pattern")


def cohen_d(mean1: float, sd1: float, n1: int, mean2: float, sd2: float, n2: int) -> float:
    """Pooled Cohen's d between two groups."""
    pooled_sd = ((n1 - 1) * sd1 ** 2 + (n2 - 1) * sd2 ** 2) / (n1 + n2 - 2)
    pooled_sd = pooled_sd ** 0.5
    if pooled_sd == 0:
        return float("nan")
    return (mean1 - mean2) / pooled_sd


cohens_d_vals = []
for _, row in df_tested.iterrows():
    d = cohen_d(row["mean_dur"], row["sd_dur"], int(row["n"]),
                mean_ref, sd_ref, int(n_ref))
    cohens_d_vals.append(d)

df_tested = df_tested.copy()
df_tested["cohen_d"] = cohens_d_vals
print("\nCohen's d per tested quarter:")
print(df_tested[["period_tag", "mean_dur", "cohen_d"]].to_string())

# %% [markdown]
# ## Verdict

# %%
max_abs_d = df_tested["cohen_d"].abs().max()
n_notable = (df_tested["cohen_d"].abs() > 0.2).sum()
mean_drift_pct = abs((df_tested["mean_dur"] - mean_ref) / mean_ref).max() * 100

print(f"\nMax |Cohen's d|: {max_abs_d:.4f}")
print(f"Quarters with |d| > 0.2: {n_notable}")
print(f"Max mean drift from reference: {mean_drift_pct:.1f}%")

if max_abs_d <= 0.2:
    verdict = "CONFIRMED"
    print(f"# Verdict: {verdict} — max |d|={max_abs_d:.4f} <= 0.2, duration stable")
else:
    verdict = "FALSIFIED"
    print(f"# Verdict: {verdict} — max |d|={max_abs_d:.4f} > 0.2, notable drift detected")

# %% [markdown]
# ## Build phase06-compatible long format CSV

# %%
# Spec §12 compatible: one row per (period_tag × metric)
dgp_rows = []
metrics_map = {
    "mean_dur": "mean",
    "median_dur": "median",
    "p5_dur": "p5",
    "p95_dur": "p95",
    "iqr_dur": "iqr",
    "sd_dur": "sd",
    "suspicious_rate": "suspicious_rate",
}

for _, row in df_dgp.iterrows():
    period = row["period_tag"]
    for col, metric in metrics_map.items():
        dgp_rows.append({
            "dataset_tag": "sc2egset",
            "period_tag": period,
            "feature_name": "duration_seconds",
            "metric_name": metric,
            "metric_value": round(float(row[col]), 4) if not np.isnan(float(row[col])) else None,
            "n": int(row["n"]),
            "notes": "[SC2EGSET-POST-GAME];[POP:tournament]",
        })

# Add Cohen's d for tested quarters
for _, row in df_tested.iterrows():
    dgp_rows.append({
        "dataset_tag": "sc2egset",
        "period_tag": row["period_tag"],
        "feature_name": "duration_seconds",
        "metric_name": "cohen_d",
        "metric_value": round(float(row["cohen_d"]), 4) if not np.isnan(float(row["cohen_d"])) else None,
        "n": int(row["n"]),
        "notes": f"cohen_d vs reference;[SC2EGSET-POST-GAME];[POP:tournament]",
    })

df_dgp_long = pd.DataFrame(dgp_rows)
print(f"DGP long format: {len(df_dgp_long)} rows")

# Verify finite values
n_nans = df_dgp_long["metric_value"].isna().sum()
print(f"Rows with NULL metric_value: {n_nans}")

# %% [markdown]
# ## Save artifacts

# %%
out_dgp = artifact_dir / "dgp_diagnostic_sc2egset.csv"
df_dgp_long.to_csv(out_dgp, index=False)
print(f"Saved: {out_dgp}")

# Verify prefix (no pre-game PSI file named dgp_diagnostic_)
assert out_dgp.name.startswith("dgp_diagnostic_"), "DGP file name prefix check failed"
assert (artifact_dir / "psi_sc2egset.csv").exists(), "PSI file exists (sanity check)"
psi_files_named_dgp = list(artifact_dir.glob("dgp_diagnostic_*psi*.csv"))
assert len(psi_files_named_dgp) == 0, "PSI file incorrectly named with dgp_diagnostic_ prefix"
print("Prefix check PASS")

# %% [markdown]
# ## Duration trend plot

# %%
df_plot = df_dgp.copy()
# Sort: reference first, then quarters
df_plot_sorted = pd.concat([
    df_plot[df_plot["period_tag"] == "reference"],
    df_plot[df_plot["period_tag"] != "reference"].sort_values("period_tag"),
])

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df_plot_sorted["period_tag"], df_plot_sorted["mean_dur"],
        marker="o", label="mean_dur", color="steelblue")
ax.plot(df_plot_sorted["period_tag"], df_plot_sorted["median_dur"],
        marker="s", linestyle="--", label="median_dur", color="darkorange")
ax.set_xlabel("Period")
ax.set_ylabel("Duration (seconds)")
ax.set_title("duration_seconds trend — sc2egset\n(POST_GAME_HISTORICAL; not a pre-game feature)")
ax.legend()
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()

out_plot = plots_dir / "dgp_diagnostic_duration_trend.png"
fig.savefig(out_plot, dpi=150)
plt.close(fig)
print(f"Saved: {out_plot}")

# %% [markdown]
# ## Markdown report

# %%
md_content = f"""# Q8: DGP Diagnostics — duration_seconds (sc2egset)

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Date:** 2026-04-18

## Method

- POST_GAME_HISTORICAL diagnostic only (duration_seconds excluded from pre-game PSI per I3)
- Reference: 2022-08-29..2022-12-31
- Tested: 2023-Q1..2024-Q4 (8 quarters)
- M9 fix: JOIN matches_flat_clean for is_duration_suspicious per-quarter rate
- Cohen (1988) §2.2: d = (mean_q - mean_ref) / pooled_sd

## SQL (verbatim, I6)

```sql
{DGP_SQL.strip()}
```

## Per-period statistics

{df_dgp.to_markdown(index=False)}

## Cohen's d per tested quarter

{df_tested[['period_tag','mean_dur','sd_dur','n','cohen_d']].to_markdown(index=False)}

## Verdict: {verdict}

Max |Cohen's d| = {max_abs_d:.4f}. Quarters with |d| > 0.2: {n_notable}.
Max mean drift from reference: {mean_drift_pct:.1f}%.

## is_duration_suspicious (M9 fix)

Per-quarter suspicious_rate computed via JOIN matches_flat_clean.
Average suspicious_rate across overlap window: {df_dgp[df_dgp['period_tag'] != 'reference']['suspicious_rate'].mean():.4f}
(0.0 = no suspicious durations; matches 01_04_03 ADDENDUM finding of zero outliers).
"""

out_md = artifact_dir / "dgp_diagnostic_sc2egset.md"
out_md.write_text(md_content)
print(f"Saved: {out_md}")

# %%
db.close()
print("T08 complete.")
