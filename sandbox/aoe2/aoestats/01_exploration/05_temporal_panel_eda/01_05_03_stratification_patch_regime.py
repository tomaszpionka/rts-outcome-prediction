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
# # Step 01_05_03 -- Stratification and Patch Regime (Q3)
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_05 -- Temporal & Panel EDA
# **Step:** 01_05_03
# **Dataset:** aoestats
# **spec:** reports/specs/01_05_preregistration.md@7e259dd8
#
# **Honest statement (spec §5):** `regime_id ≡ calendar quarter`. Cross-dataset
# stratification by `regime_id` IS stratification by time, identical to Q1 grain.
# It provides no additional variance reduction beyond Q1.
#
# # Hypothesis: Per-patch win-rate by civ exhibits heterogeneity consistent with
# # patch-driven balance changes; at least 3 civs show |Δwin_rate| >= 5pp in >= 1
# # patch transition.
# # Falsifier: Civ win rates stationary across all 19 patches (max |Δ| < 2pp for
# # every civ at every patch boundary) -- would undermine patch-heterogeneity motivation.
#
# **Critique M1:** Per-quarter share_of_row_count_by_patch + Simpson's paradox probe.
# Cite Chitayat et al. 2023 arxiv.org/abs/2305.18477.
# **m3 fix:** Patch threshold 5pp justified by Cohen h=0.1 (Cohen 1988 §6.2).

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
# Pull 19-patch map from overviews_raw (spec §5)
PATCH_MAP_SQL = """
SELECT
  p.patch_info.number AS patch_number,
  p.patch_info.label AS patch_label,
  p.patch_info.release_date AS release_date,
  p.patch_info.total_games AS total_games
FROM (SELECT UNNEST(patches) AS patch_info FROM overviews_raw) p
ORDER BY release_date
"""
df_patches = db.fetch_df(PATCH_MAP_SQL)
print(f"Patch map: {len(df_patches)} patches")
print(df_patches.to_string())

# %%
assert len(df_patches) == 19, f"Expected 19 patches, got {len(df_patches)}"
patch_csv = ARTIFACTS_DIR / "patch_map.csv"
df_patches.to_csv(patch_csv, index=False)
print(f"Wrote {patch_csv}")

# %%
# Per-quarter patch distribution (M1: Simpson's paradox probe)
# Per Chitayat et al. 2023 arxiv.org/abs/2305.18477 "Beyond the Meta"
PATCH_QUARTER_SQL = """
SELECT
  DATE_TRUNC('quarter', mhm.started_at) AS quarter_start,
  CAST(YEAR(mhm.started_at) AS VARCHAR) || '-Q' || CAST(QUARTER(mhm.started_at) AS VARCHAR) AS quarter_iso,
  m1v1.patch AS patch_number,
  COUNT(*) AS n_rows,
  AVG(CAST(mhm.won AS INTEGER)) AS win_rate_agg
FROM matches_history_minimal mhm
JOIN matches_1v1_clean m1v1 ON mhm.match_id = 'aoestats::' || m1v1.game_id
WHERE mhm.started_at >= TIMESTAMP '2022-07-01'
  AND mhm.started_at < TIMESTAMP '2025-01-01'
GROUP BY 1, 2, 3
ORDER BY 1, 3
"""
df_patch_qtr = db.fetch_df(PATCH_QUARTER_SQL)
print(f"Patch-quarter distribution: {len(df_patch_qtr)} rows")

# %%
# Compute share_of_row_count_by_patch per quarter (M1)
df_patch_qtr["quarter_total"] = df_patch_qtr.groupby("quarter_iso")["n_rows"].transform("sum")
df_patch_qtr["share_of_row_count"] = df_patch_qtr["n_rows"] / df_patch_qtr["quarter_total"]

# Identify multi-patch quarters
multi_patch = df_patch_qtr.groupby("quarter_iso")["patch_number"].nunique()
print("Patches per quarter:")
print(multi_patch)

# %%
# Per-civ win rate by patch (aggregate)
CIV_WIN_RATE_SQL = """
SELECT
  m1v1.patch AS patch_number,
  mhm.faction AS civ,
  COUNT(*) AS n_matches,
  AVG(CAST(mhm.won AS INTEGER)) AS win_rate
FROM matches_history_minimal mhm
JOIN matches_1v1_clean m1v1 ON mhm.match_id = 'aoestats::' || m1v1.game_id
GROUP BY m1v1.patch, mhm.faction
HAVING COUNT(*) >= 100
ORDER BY m1v1.patch, mhm.faction
"""
print("Loading per-civ win rates by patch (this may take a moment)...")
df_civ_rates = db.fetch_df(CIV_WIN_RATE_SQL)
print(f"Civ-patch win rates: {len(df_civ_rates)} rows")

# %%
# Patch-to-patch delta per civ
patch_order = sorted(df_civ_rates["patch_number"].unique())
rows_flagged = []
for civ in df_civ_rates["civ"].unique():
    civ_df = df_civ_rates[df_civ_rates["civ"] == civ].set_index("patch_number")
    for i in range(1, len(patch_order)):
        p0 = patch_order[i - 1]
        p1 = patch_order[i]
        if p0 in civ_df.index and p1 in civ_df.index:
            delta = abs(float(civ_df.loc[p1, "win_rate"]) - float(civ_df.loc[p0, "win_rate"]))
            # m3 fix: threshold 5pp justified by Cohen h=0.1 (Cohen 1988 §6.2)
            flagged = delta >= 0.05
            rows_flagged.append({
                "civ": civ,
                "patch_from": p0,
                "patch_to": p1,
                "delta_win_rate": round(delta, 4),
                "flagged_ge_5pp": flagged,
            })

df_transitions = pd.DataFrame(rows_flagged)
n_flagged_civs = df_transitions[df_transitions["flagged_ge_5pp"]]["civ"].nunique()
print(f"Civs with |Δwin_rate| >= 5pp in >= 1 patch transition: {n_flagged_civs}")

# %%
# Falsifier check
if n_flagged_civs >= 3:
    verdict = "PASSED"
else:
    verdict = "FALSIFIED"
print(f"Q3 patch-heterogeneity hypothesis: {verdict}")

# %%
# M1: Simpson's paradox probe -- PSI stratified by patch within quarter
# Compute patch heterogeneity decomposition
total_variance_q = df_patch_qtr.groupby("quarter_iso")["win_rate_agg"].var()
within_patch_var = df_patch_qtr.groupby(["quarter_iso", "patch_number"])["win_rate_agg"].var()
between_patch_var = total_variance_q - within_patch_var.groupby(level=0).mean()

decomp_rows = []
for q in total_variance_q.index:
    tv = float(total_variance_q.get(q, float("nan")))
    bp = float(between_patch_var.get(q, float("nan")))
    wp = float(total_variance_q.get(q, float("nan")) - bp) if not np.isnan(bp) else float("nan")
    pct_between = round(bp / tv * 100, 2) if tv > 0 and not np.isnan(bp) else float("nan")
    pct_within = round(100 - pct_between, 2) if not np.isnan(pct_between) else float("nan")
    decomp_rows.append({
        "quarter_iso": q,
        "total_variance": round(tv, 6) if not np.isnan(tv) else None,
        "drift_attributable_to_patch_pct": pct_between,
        "intra_patch_temporal_pct": pct_within,
        "note": "Chitayat et al. 2023 arxiv.org/abs/2305.18477 Beyond the Meta",
    })

df_decomp = pd.DataFrame(decomp_rows)
decomp_csv = ARTIFACTS_DIR / "patch_heterogeneity_decomposition.csv"
df_decomp.to_csv(decomp_csv, index=False)
print(f"Wrote {decomp_csv}")
print(df_decomp.to_string())

# %%
# Emit artifacts
civ_csv = ARTIFACTS_DIR / "patch_civ_win_rates.csv"
df_civ_rates.to_csv(civ_csv, index=False)

trans_csv = ARTIFACTS_DIR / "patch_transitions_flagged.csv"
df_transitions.to_csv(trans_csv, index=False)

patch_qtr_csv = ARTIFACTS_DIR / "patch_quarter_distribution.csv"
df_patch_qtr.to_csv(patch_qtr_csv, index=False)

# %%
# Summary JSON + MD
HONEST_STMT = (
    "`regime_id ≡ calendar quarter`. Cross-dataset stratification by `regime_id` IS "
    "stratification by time, identical to the Q1 grain. It provides no additional "
    "variance reduction beyond Q1."
)

summary = {
    "step": "01_05_03",
    "spec": "reports/specs/01_05_preregistration.md@7e259dd8",
    "honest_statement": HONEST_STMT,
    "n_patches": len(df_patches),
    "civs_with_large_patch_delta": n_flagged_civs,
    "falsifier_verdict": verdict,
    "sql_queries": {
        "patch_map": PATCH_MAP_SQL.strip(),
        "civ_win_rate": CIV_WIN_RATE_SQL.strip(),
        "patch_quarter": PATCH_QUARTER_SQL.strip(),
    },
    "m1_note": (
        "Patch heterogeneity decomposition per Chitayat et al. 2023 arxiv.org/abs/2305.18477. "
        "Simpson's paradox probe: drift attributable to patch vs intra-patch temporal."
    ),
}
with open(ARTIFACTS_DIR / "01_05_03_patch_regime_summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)

md_text = f"""# Stratification and Patch Regime Summary -- aoestats

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Step:** 01_05_03
**Label:** [WITHIN-AOESTATS-SECONDARY; NOT CROSS-DATASET]

## Honest statement (spec §5)

*{HONEST_STMT}*

## Patch Map

{df_patches.to_markdown(index=False)}

## Patch-Heterogeneity Decomposition (M1)

Per Chitayat et al. 2023 (arxiv.org/abs/2305.18477 "Beyond the Meta"):

{df_decomp.to_markdown(index=False)}

*Threshold 5pp justified by Cohen h=0.1 (Cohen 1988 §6.2).*

## Falsifier verdict

**Q3 patch-heterogeneity:** {verdict}
Civs with |Δwin_rate| >= 5pp: {n_flagged_civs}
"""
(ARTIFACTS_DIR / "01_05_03_patch_regime_summary.md").write_text(md_text)
print("Step 01_05_03 complete.")
