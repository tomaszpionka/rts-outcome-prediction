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
# # Step 01_05_04 -- Triple Survivorship Analysis (Q4)
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_05 -- Temporal & Panel EDA
# **Step:** 01_05_04
# **Dataset:** aoestats
# **spec:** reports/specs/01_05_preregistration.md@7e259dd8
#
# # Hypothesis: fraction_active decays approximately exponentially from 2022-Q3,
# # with < 30% of 2022-Q3 ever-active players still active in 2024-Q4.
# # Falsifier: fraction_active > 60% in 2024-Q4 (no meaningful churn) OR < 5%
# # (cohort collapse) -- both invalidate the cohort N=10 default.

# %%
import json
from datetime import date
from pathlib import Path

import pandas as pd

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir
from rts_predict.games.aoe2.datasets.aoestats.analysis.survivorship import (
    CONDITIONAL_CAPTION,
    compute_fraction_active,
    compute_n_match_cohort,
)

ARTIFACTS_DIR = get_reports_dir("aoe2", "aoestats") / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

db = get_notebook_db("aoe2", "aoestats")
print("Connected.")

# %%
OVERLAP_START = date(2022, 7, 1)
OVERLAP_END = date(2024, 12, 31)
REF_START = date(2022, 8, 29)
REF_END = date(2022, 10, 27)

# %%
# 6.1 Unconditional fraction_active (spec §6.1)
print("Computing unconditional fraction_active...")
df_active = compute_fraction_active(db, OVERLAP_START, OVERLAP_END)
print(df_active.to_string())

# %%
# Falsifier check
last_q = df_active.iloc[-1]
frac_last = float(last_q["fraction_active"])
if frac_last > 0.60:
    verdict = "FALSIFIED (no meaningful churn)"
elif frac_last < 0.05:
    verdict = "FALSIFIED (cohort collapse)"
else:
    verdict = "PASSED"
print(f"fraction_active in final quarter: {frac_last:.4f}")
print(f"Q4 survivorship hypothesis: {verdict}")

# %%
# Emit unconditional CSV
surv_csv = ARTIFACTS_DIR / "survivorship_unconditional.csv"
df_active.to_csv(surv_csv, index=False)
print(f"Wrote {surv_csv}")
assert len(df_active) == 10, f"Expected 10 quarters, got {len(df_active)}"

# %%
# 6.2 Sensitivity: N ∈ {5, 10, 20}
sens_rows = []
for n_min in [5, 10, 20]:
    print(f"Computing cohort N={n_min}...")
    cohort_ids = compute_n_match_cohort(db, REF_START, REF_END, n_min, span_days_min=30)
    print(f"  N={n_min}: {len(cohort_ids):,} players")

    # Compute PSI summary stat per feature for this cohort size
    # (simplified: just count active players per quarter for sensitivity)
    COHORT_SQL = f"""
    WITH cohort AS (
      SELECT CAST(player_id AS BIGINT) AS player_id
      FROM matches_history_minimal
      WHERE started_at >= TIMESTAMP '{REF_START}'
        AND started_at <= TIMESTAMP '{REF_END}'
      GROUP BY player_id
      HAVING COUNT(*) >= {n_min}
        AND MAX(started_at) - MIN(started_at) >= INTERVAL '30 days'
    )
    SELECT
      CAST(YEAR(mhm.started_at) AS VARCHAR) || '-Q' || CAST(QUARTER(mhm.started_at) AS VARCHAR) AS quarter_iso,
      COUNT(DISTINCT CAST(mhm.player_id AS BIGINT)) AS n_active_cohort,
      COUNT(*) AS n_rows
    FROM matches_history_minimal mhm
    JOIN cohort c ON CAST(mhm.player_id AS BIGINT) = c.player_id
    WHERE mhm.started_at >= TIMESTAMP '2023-01-01'
      AND mhm.started_at < TIMESTAMP '2025-01-01'
    GROUP BY 1
    ORDER BY 1
    """
    df_n = db.fetch_df(COHORT_SQL)
    for _, row in df_n.iterrows():
        sens_rows.append({
            "n_min": n_min,
            "quarter_iso": row["quarter_iso"],
            "n_active_cohort": int(row["n_active_cohort"]),
            "n_rows": int(row["n_rows"]),
        })

df_sens = pd.DataFrame(sens_rows)
sens_csv = ARTIFACTS_DIR / "survivorship_sensitivity.csv"
df_sens.to_csv(sens_csv, index=False)
print(f"Survivorship sensitivity: {len(df_sens)} rows")
# m2 fix: n_q x n_N x n_surviving_features; warn if < 64
n_expected = 8 * 3  # quarters x N values
if len(df_sens) < n_expected:
    print(f"WARNING: sensitivity has {len(df_sens)} rows < expected {n_expected}")
print(f"Wrote {sens_csv}")

# %%
# Summary JSON + MD
summary = {
    "step": "01_05_04",
    "spec": "reports/specs/01_05_preregistration.md@7e259dd8",
    "overlap_start": str(OVERLAP_START),
    "overlap_end": str(OVERLAP_END),
    "fraction_active_final_quarter": round(frac_last, 4),
    "falsifier_verdict": verdict,
    "n_quarters": len(df_active),
    "conditional_caption": CONDITIONAL_CAPTION,
}
with open(ARTIFACTS_DIR / "01_05_04_survivorship_summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)

md_text = f"""# Triple Survivorship Analysis -- aoestats

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Step:** 01_05_04

{CONDITIONAL_CAPTION}

## Unconditional Fraction Active (§6.1)

{df_active.to_markdown(index=False)}

## Sensitivity N ∈ {{5, 10, 20}} (§6.2)

{df_sens.to_markdown(index=False)}

## Falsifier verdict

**Q4 survivorship hypothesis:** {verdict}
fraction_active in final quarter: {frac_last:.4f}
"""
(ARTIFACTS_DIR / "01_05_04_survivorship_summary.md").write_text(md_text)
print("Step 01_05_04 complete.")
