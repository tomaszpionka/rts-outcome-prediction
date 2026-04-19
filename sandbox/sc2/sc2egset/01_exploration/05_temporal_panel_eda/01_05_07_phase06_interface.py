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
# # Step 01_05_07 -- Phase 06 Interface CSV (sc2egset)
#
# **spec:** reports/specs/01_05_preregistration.md@7e259dd8
# **Dataset:** sc2egset
# **Branch:** feat/01-05-sc2egset
# **Date:** 2026-04-18
#
# **Objective:** Consolidate T03/T06/T08 outputs into the spec §12 flat schema.
# One row per (dataset × quarter × feature × metric).
#
# **M3 note:** Spec §1 9-col contract differs from actual VIEW schema.
# Per user pre-authorized decision: documented in INVARIANTS §5 as I8 partial.
# Phase 06 UNION joins on metric_name only (cross-dataset alignment).
# feature_name values match actual VIEW schema (faction/opponent_faction/duration_seconds).
#
# **M7:** [POP:tournament] tag in notes column for all rows.

# %%
# spec: reports/specs/01_05_preregistration.md@7e259dd8
# Step 01_05_07 -- Phase 06 interface CSV (sc2egset)
# Dataset: sc2egset  Branch: feat/01-05-sc2egset  Date: 2026-04-18

import json
from pathlib import Path

import numpy as np
import pandas as pd

from rts_predict.common.notebook_utils import get_reports_dir

# %%
reports_dir = get_reports_dir("sc2", "sc2egset")
artifact_dir = reports_dir / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
artifact_dir.mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ## Hypothesis

# %%
# Hypothesis: A union of T03 PSI rows, T06 ICC rows, and T08 DGP d rows
# conforms to spec §12 with 0 schema violations.
# Falsifier: any row with NaN in non-nullable columns, bad dtype, or unknown metric_name.

# %% [markdown]
# ## Load source CSVs

# %%
df_psi = pd.read_csv(artifact_dir / "psi_sc2egset.csv")
df_icc = pd.read_csv(artifact_dir / "variance_icc_sc2egset.csv")
df_dgp = pd.read_csv(artifact_dir / "dgp_diagnostic_sc2egset.csv")

print(f"PSI rows: {len(df_psi)}")
print(f"ICC rows: {len(df_icc)}")
print(f"DGP rows: {len(df_dgp)}")

# %% [markdown]
# ## Build Phase 06 interface (spec §12 schema)

# %%
# Spec §12 schema:
# dataset_tag, quarter, feature_name, metric_name, metric_value,
# reference_window_id, cohort_threshold, sample_size, notes

REQUIRED_COLS = [
    "dataset_tag", "quarter", "feature_name", "metric_name", "metric_value",
    "reference_window_id", "cohort_threshold", "sample_size", "notes",
]

VALID_METRIC_NAMES = {"psi", "cohen_h", "cohen_d", "ks_stat", "icc",
                      "icc_lpm_observed_scale", "icc_anova_observed_scale",
                      "icc_glmm_latent_scale"}

rows_ph06 = []

# --- PSI rows (T03) ---
for _, r in df_psi.iterrows():
    notes = str(r.get("notes", "")) if pd.notna(r.get("notes")) else ""
    if "[POP:tournament]" not in notes:
        notes = notes + ";[POP:tournament]" if notes else "[POP:tournament]"
    rows_ph06.append({
        "dataset_tag": "sc2egset",
        "quarter": r["quarter"],
        "feature_name": r["feature_name"],
        "metric_name": "psi",
        "metric_value": round(float(r["psi_value"]), 4) if pd.notna(r["psi_value"]) else None,
        "reference_window_id": "2022-Q3Q4",
        "cohort_threshold": None,  # PRIMARY = uncohort-filtered (B2 fix)
        "sample_size": int(r["n_tested"]),
        "notes": notes,
    })

# --- ICC rows (T06) ---
# ICC rows use 'quarter' = None (applies to entire overlap window, not per-quarter)
# Map to a special quarter value per spec: use 'overlap_window'
for _, r in df_icc.iterrows():
    metric = str(r["metric_name"])
    icc_val = r["icc"]
    notes = str(r.get("notes", "")) if pd.notna(r.get("notes")) else ""
    if "[POP:tournament]" not in notes:
        notes = notes + ";[POP:tournament]" if notes else "[POP:tournament]"
    rows_ph06.append({
        "dataset_tag": "sc2egset",
        "quarter": "overlap_window",  # ICC is computed across full overlap window
        "feature_name": "won",
        "metric_name": metric,  # M3: use actual metric_name from T06
        "metric_value": round(float(icc_val), 4) if pd.notna(icc_val) else None,
        "reference_window_id": "2022-Q3Q4",
        "cohort_threshold": int(r["cohort_threshold"]) if pd.notna(r.get("cohort_threshold")) else None,
        "sample_size": int(r["n_obs"]),
        "notes": notes,
    })

# --- DGP Cohen's d rows (T08, only cohen_d metric in Phase 06) ---
df_dgp_d = df_dgp[df_dgp["metric_name"] == "cohen_d"]
for _, r in df_dgp_d.iterrows():
    notes = str(r.get("notes", "")) if pd.notna(r.get("notes")) else ""
    if "[POP:tournament]" not in notes:
        notes = notes + ";[POP:tournament]" if notes else "[POP:tournament]"
    rows_ph06.append({
        "dataset_tag": "sc2egset",
        "quarter": r["period_tag"],
        "feature_name": "duration_seconds",
        "metric_name": "cohen_d",
        "metric_value": round(float(r["metric_value"]), 4) if pd.notna(r["metric_value"]) else None,
        "reference_window_id": "2022-Q3Q4",
        "cohort_threshold": None,
        "sample_size": int(r["n"]),
        "notes": notes + ";[SC2EGSET-POST-GAME]" if "[SC2EGSET-POST-GAME]" not in notes else notes,
    })

df_ph06 = pd.DataFrame(rows_ph06, columns=REQUIRED_COLS)
df_ph06["metric_value"] = df_ph06["metric_value"].round(4)

print(f"\nPhase 06 interface: {len(df_ph06)} rows")
print(df_ph06.dtypes)
print(f"\nMetric names: {df_ph06['metric_name'].unique().tolist()}")
print(f"Features: {df_ph06['feature_name'].unique().tolist()}")

# %% [markdown]
# ## Validation

# %%
# Schema validation
assert set(df_ph06.columns) == set(REQUIRED_COLS), \
    f"Schema mismatch: {set(df_ph06.columns) ^ set(REQUIRED_COLS)}"
assert df_ph06["dataset_tag"].eq("sc2egset").all(), "dataset_tag != sc2egset"
assert df_ph06.shape[0] > 0, "Empty Phase 06 interface"

# Check non-nullable columns
for col in ["dataset_tag", "quarter", "feature_name", "metric_name"]:
    assert df_ph06[col].notna().all(), f"NaN in non-nullable column: {col}"

# metric_name must be in extended set (M3 note: ICC has dataset-specific metric names)
valid_metrics = {"psi", "cohen_h", "cohen_d", "ks_stat", "icc",
                 "icc_lpm_observed_scale", "icc_anova_observed_scale",
                 "icc_glmm_latent_scale"}
invalid_metrics = set(df_ph06["metric_name"]) - valid_metrics
assert len(invalid_metrics) == 0, f"Invalid metric_names: {invalid_metrics}"

print("Schema validation PASS")
print(f"Row count: {len(df_ph06)}")

# Verdict
verdict = "CONFIRMED"
print(f"# Verdict: {verdict} — {len(df_ph06)} rows, schema valid, 0 violations")

# %% [markdown]
# ## Save artifacts

# %%
out_ph06 = artifact_dir / "phase06_interface_sc2egset.csv"
# NaN handling: store as SQL NULL (blank CSV cell)
df_ph06.to_csv(out_ph06, index=False, na_rep="")
print(f"Saved: {out_ph06}")

# Schema JSON
schema_doc = {
    "schema_version": "1.0",
    "spec_ref": "reports/specs/01_05_preregistration.md@7e259dd8 §12",
    "dataset": "sc2egset",
    "columns": [
        {"name": "dataset_tag", "type": "VARCHAR", "nullable": False,
         "description": "Dataset identifier"},
        {"name": "quarter", "type": "VARCHAR", "nullable": False,
         "description": "Quarter label YYYY-QN or 'overlap_window' for ICC rows"},
        {"name": "feature_name", "type": "VARCHAR", "nullable": False,
         "description": "Feature or target column name"},
        {"name": "metric_name", "type": "VARCHAR", "nullable": False,
         "description": "Metric: psi, cohen_d, icc_lpm_observed_scale, icc_anova_observed_scale, icc_glmm_latent_scale"},
        {"name": "metric_value", "type": "DOUBLE", "nullable": True,
         "description": "Metric value (NULL if not applicable)"},
        {"name": "reference_window_id", "type": "VARCHAR", "nullable": True,
         "description": "Reference period label: '2022-Q3Q4'"},
        {"name": "cohort_threshold", "type": "INTEGER", "nullable": True,
         "description": "Min matches in reference for cohort inclusion (NULL = uncohort-filtered)"},
        {"name": "sample_size", "type": "INTEGER", "nullable": True,
         "description": "N rows in tested period for this row"},
        {"name": "notes", "type": "VARCHAR", "nullable": True,
         "description": "Free-text notes: [SMALL-COHORT], [POP:tournament], [SC2EGSET-POST-GAME], etc."},
    ],
    "m3_note": (
        "Spec §1 9-col contract differs from actual VIEW schema. "
        "Per INVARIANTS §5 I8 partial: feature_name values match actual VIEW schema "
        "(faction/opponent_faction/duration_seconds). Phase 06 UNION joins on metric_name only."
    ),
    "b2_note": "PRIMARY PSI = uncohort-filtered (cohort_threshold=NULL for PSI rows). B2 critique fix.",
    "b3_note": (
        "ICC has 3 metric_name values: icc_lpm_observed_scale (primary), "
        "icc_anova_observed_scale (secondary), icc_glmm_latent_scale (tertiary, may be NULL)."
    ),
}

out_schema = artifact_dir / "phase06_interface_sc2egset.schema.json"
with open(out_schema, "w") as f:
    json.dump(schema_doc, f, indent=2)
print(f"Saved: {out_schema}")

# Verify
df_check = pd.read_csv(out_ph06)
assert list(df_check.columns) == REQUIRED_COLS, f"Column order mismatch: {list(df_check.columns)}"
assert df_check["dataset_tag"].eq("sc2egset").all()
print("Verification PASS")

# %% [markdown]
# ## Markdown report

# %%
md_content = f"""# Phase 06 Interface CSV — sc2egset

**spec:** reports/specs/01_05_preregistration.md@7e259dd8 §12
**Date:** 2026-04-18

## Summary

- Total rows: {len(df_ph06)}
- PSI rows: {len(df_psi)} (T03; uncohort-filtered per B2 fix)
- ICC rows: {len(df_icc)} (T06; 3 metric_names per B3 fix)
- Cohen's d DGP rows: {len(df_dgp_d)} (T08; POST_GAME)

## M3 note

Spec §1 9-col contract differs from actual VIEW schema for sc2egset.
Per INVARIANTS §5 I8 partial: feature_name values match actual VIEW schema.
Phase 06 UNION joins on metric_name only (cross-dataset alignment).

## M7 note

All rows tagged [POP:tournament]: sc2egset is tournament-scraped.

## Schema (9 columns per spec §12)

| Column | Type | Nullable | Notes |
|---|---|---|---|
| dataset_tag | VARCHAR | No | 'sc2egset' constant |
| quarter | VARCHAR | No | YYYY-QN or 'overlap_window' |
| feature_name | VARCHAR | No | Actual VIEW column name |
| metric_name | VARCHAR | No | psi/cohen_d/icc_* |
| metric_value | DOUBLE | Yes | NULL = not applicable |
| reference_window_id | VARCHAR | Yes | '2022-Q3Q4' |
| cohort_threshold | INTEGER | Yes | NULL = uncohort-filtered |
| sample_size | INTEGER | Yes | N rows in tested period |
| notes | VARCHAR | Yes | Free-text tags |

## Sample rows

{df_ph06.head(10).to_markdown(index=False)}
"""

out_md = artifact_dir / "phase06_interface_sc2egset.md"
out_md.write_text(md_content)
print(f"Saved: {out_md}")

print("\nT09 complete.")
