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
# # Step 01_05_07 -- Duration DGP Diagnostics (Q8)
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_05 -- Temporal & Panel EDA
# **Step:** 01_05_07
# **Dataset:** aoestats
# **spec:** reports/specs/01_05_preregistration.md@7e259dd8
#
# # Hypothesis: duration_seconds mean drifts < 5% between reference and any tested
# # quarter; corruption rate (is_duration_suspicious=TRUE) remains < 0.001% per quarter.
# # Falsifier: Any quarter shows corruption rate > 0.01% OR mean drift > 10% -- would
# # indicate a secular DGP shift worth flagging to Phase 02.

# %%
import json
from pathlib import Path

import numpy as np
import pandas as pd

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir

ARTIFACTS_DIR = get_reports_dir("aoe2", "aoestats") / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

db = get_notebook_db("aoe2", "aoestats")
print("Connected.")

# %%
# Per-quarter duration diagnostics (full data + corruption filter)
DGP_SQL = """
SELECT
  DATE_TRUNC('quarter', started_at) AS quarter_start,
  CAST(YEAR(started_at) AS VARCHAR) || '-Q' || CAST(QUARTER(started_at) AS VARCHAR) AS quarter_iso,
  COUNT(*) AS n_rows,
  AVG(duration_seconds) AS mean_duration,
  APPROX_QUANTILE(duration_seconds, 0.5) AS median_duration,
  APPROX_QUANTILE(duration_seconds, 0.05) AS p5_duration,
  APPROX_QUANTILE(duration_seconds, 0.95) AS p95_duration,
  APPROX_QUANTILE(duration_seconds, 0.75) - APPROX_QUANTILE(duration_seconds, 0.25) AS iqr_duration,
  STDDEV(duration_seconds) AS std_duration,
  COUNT(*) FILTER (WHERE duration_seconds > 86400) AS corrupt_count,
  COUNT(*) FILTER (WHERE duration_seconds > 86400) * 1.0 / COUNT(*) AS corrupt_rate
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-07-01'
  AND started_at < TIMESTAMP '2025-01-01'
  AND duration_seconds IS NOT NULL
GROUP BY 1, 2
ORDER BY 1
"""
print("Loading DGP diagnostics...")
df_dgp = db.fetch_df(DGP_SQL)
print(df_dgp.to_string())

# %%
# Reference period stats (2022-Q3/Q4 combined)
ref_mask = df_dgp["quarter_iso"].isin(["2022-Q3", "2022-Q4"])
df_ref_dgp = df_dgp[ref_mask]
mean_ref = float(df_ref_dgp["mean_duration"].mean())
std_ref = float(np.sqrt((df_ref_dgp["std_duration"] ** 2).mean()))
print(f"Reference mean duration: {mean_ref:.1f}s, std: {std_ref:.1f}s")

# %%
# Compute Cohen's d vs reference
tested_dgp = df_dgp[~ref_mask].copy()
tested_dgp["cohen_d_vs_ref"] = tested_dgp.apply(
    lambda row: (float(row["mean_duration"]) - mean_ref) / np.sqrt((float(row["std_duration"]) ** 2 + std_ref ** 2) / 2)
    if float(row["std_duration"]) > 0 else 0.0,
    axis=1,
)
tested_dgp["mean_drift_pct"] = (tested_dgp["mean_duration"] - mean_ref) / mean_ref * 100

# %%
# Falsifier check
max_corrupt_rate = float(tested_dgp["corrupt_rate"].max())
max_drift_pct = float(tested_dgp["mean_drift_pct"].abs().max())

if max_corrupt_rate > 0.0001:
    verdict = "FALSIFIED"
    print(f"FALSIFIED: max corrupt rate {max_corrupt_rate:.6f} > 0.01%")
elif max_drift_pct > 10.0:
    verdict = "FALSIFIED"
    print(f"FALSIFIED: max mean drift {max_drift_pct:.1f}% > 10%")
else:
    verdict = "PASSED"

print(f"Max corrupt rate: {max_corrupt_rate:.6f} ({max_corrupt_rate*100:.4f}%)")
print(f"Max mean drift: {max_drift_pct:.2f}%")
print(f"Q8 DGP hypothesis: {verdict}")

# %%
# Emit per-quarter CSVs
ref_df = df_ref_dgp.copy()
ref_df["cohen_d_vs_ref"] = 0.0
ref_df["mean_drift_pct"] = 0.0
ref_df["feature_name"] = "duration_seconds"
ref_df["notes"] = "POST_GAME_HISTORICAL (spec §10) -- reference period"
ref_csv = ARTIFACTS_DIR / "dgp_diagnostic_aoestats_2022-Q3Q4ref.csv"
ref_df.to_csv(ref_csv, index=False)

QUARTERS = [
    "2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4",
    "2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4",
]
for q_name in QUARTERS:
    q_df = tested_dgp[tested_dgp["quarter_iso"] == q_name].copy()
    q_df["feature_name"] = "duration_seconds"
    q_df["notes"] = "POST_GAME_HISTORICAL (spec §10)"
    fname = ARTIFACTS_DIR / f"dgp_diagnostic_aoestats_{q_name}.csv"
    q_df.to_csv(fname, index=False)

print("DGP diagnostic CSVs written.")

# %%
# Summary JSON
summary = {
    "step": "01_05_07",
    "spec": "reports/specs/01_05_preregistration.md@7e259dd8",
    "feature": "duration_seconds",
    "token": "POST_GAME_HISTORICAL",
    "reference_mean": round(mean_ref, 2),
    "reference_std": round(std_ref, 2),
    "max_corrupt_rate": round(max_corrupt_rate, 8),
    "max_mean_drift_pct": round(max_drift_pct, 2),
    "falsifier_verdict": verdict,
    "cohen_d_by_quarter": {
        row["quarter_iso"]: round(float(row["cohen_d_vs_ref"]), 4)
        for _, row in tested_dgp.iterrows()
    },
    "sql_queries": {"dgp_diagnostics": DGP_SQL.strip()},
}
with open(ARTIFACTS_DIR / "01_05_07_dgp_diagnostic_summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)

md_text = f"""# Duration DGP Diagnostics -- aoestats

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Step:** 01_05_07
**Token:** POST_GAME_HISTORICAL (excluded from PSI per I3)

## DGP Statistics

{df_dgp.to_markdown(index=False)}

## Falsifier verdict

**Q8 DGP hypothesis:** {verdict}
Max corrupt rate: {max_corrupt_rate:.6f} ({max_corrupt_rate*100:.4f}%)
Max mean drift: {max_drift_pct:.2f}%
"""
(ARTIFACTS_DIR / "01_05_07_dgp_diagnostic_summary.md").write_text(md_text)
print("Step 01_05_07 complete.")
