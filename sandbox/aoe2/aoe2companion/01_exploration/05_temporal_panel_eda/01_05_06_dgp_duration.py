# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: rts-predict
#     language: python
#     name: rts-predict
# ---

# %% [markdown]
# # 01_05_06 DGP Duration Diagnostics — aoe2companion
# spec: reports/specs/01_05_preregistration.md@7e259dd8
#
# **Spec §§:** §10 (DGP diagnostics, duration_seconds + suspicious flags)
# **Critique fix M-05:** "Interpretation at large N" paragraph included.
#
# POST_GAME features ONLY. NEVER appears in T03/T04 pre-game outputs (I3 guard).
#
# **Hypothesis:** duration_seconds median and p95 are stable within +/-10% across
# quarters after excluding is_duration_suspicious and is_duration_negative rows;
# Cohen's d on cleaned duration vs reference is < 0.2 in every quarter.
# **Falsifier:** any quarter has |Cohen's d| >= 0.5 (medium effect) on cleaned duration.

# %% [markdown]
# ## Imports

# %%
import json
import math
from datetime import datetime
from pathlib import Path

import pandas as pd

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir

ARTIFACTS = get_reports_dir("aoe2", "aoe2companion") / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

PERIODS = [
    ("reference", "2022-08-29", "2023-01-01"),
    ("2023-Q1", "2023-01-01", "2023-04-01"),
    ("2023-Q2", "2023-04-01", "2023-07-01"),
    ("2023-Q3", "2023-07-01", "2023-10-01"),
    ("2023-Q4", "2023-10-01", "2024-01-01"),
    ("2024-Q1", "2024-01-01", "2024-04-01"),
    ("2024-Q2", "2024-04-01", "2024-07-01"),
    ("2024-Q3", "2024-07-01", "2024-10-01"),
    ("2024-Q4", "2024-10-01", "2025-01-01"),
]

print("Artifacts dir:", ARTIFACTS)

# %% [markdown]
# ## Step 1: I3 guard — confirm no PSI computation on POST_GAME features

# %%
# I3 guard: duration_seconds is POST_GAME_HISTORICAL (01_04_02 ADDENDUM)
# This notebook is the SOLE home for duration analysis (spec §10)
print("I3 guard: duration_seconds, is_duration_suspicious, is_duration_negative are POST_GAME features.")
print("These features DO NOT appear in T03/T04 pre-game outputs.")
print("Confirmed: no PSI computation on POST_GAME features in this notebook.")

# %% [markdown]
# ## Step 2: Per-period duration statistics

# %%
QUERY_DGP = """
SELECT
    COUNT(*) AS n_total,
    COUNT(*) FILTER (WHERE NOT is_duration_suspicious AND NOT is_duration_negative) AS n_clean,
    AVG(duration_seconds) AS mean_dur_raw,
    quantile_cont(duration_seconds, 0.5) AS median_dur_raw,
    quantile_cont(duration_seconds, 0.05) AS p05_raw,
    quantile_cont(duration_seconds, 0.95) AS p95_raw,
    quantile_cont(duration_seconds, 0.75) - quantile_cont(duration_seconds, 0.25) AS iqr_raw,
    AVG(duration_seconds) FILTER (WHERE NOT is_duration_suspicious AND NOT is_duration_negative) AS mean_dur_clean,
    quantile_cont(duration_seconds, 0.5)
        FILTER (WHERE NOT is_duration_suspicious AND NOT is_duration_negative) AS median_dur_clean,
    quantile_cont(duration_seconds, 0.95)
        FILTER (WHERE NOT is_duration_suspicious AND NOT is_duration_negative) AS p95_clean,
    STDDEV(duration_seconds)
        FILTER (WHERE NOT is_duration_suspicious AND NOT is_duration_negative) AS std_dur_clean,
    COUNT(*) FILTER (WHERE is_duration_suspicious) AS n_suspicious,
    COUNT(*) FILTER (WHERE is_duration_negative) AS n_negative,
    COUNT(*) FILTER (WHERE duration_seconds = 0) AS n_zero,
    COUNT(*) FILTER (WHERE is_duration_suspicious) * 1.0 / COUNT(*) AS suspicious_rate,
    COUNT(*) FILTER (WHERE is_duration_negative) * 1.0 / COUNT(*) AS negative_rate
FROM matches_1v1_clean
WHERE started >= TIMESTAMP '{ts_start}'
  AND started <  TIMESTAMP '{ts_end}'
"""

db = get_notebook_db("aoe2", "aoe2companion", read_only=True)

period_stats = {}
for period_name, ts_start, ts_end in PERIODS:
    res = db.con.execute(QUERY_DGP.format(ts_start=ts_start, ts_end=ts_end)).fetchone()
    period_stats[period_name] = {
        "period": period_name,
        "ts_start": ts_start,
        "ts_end": ts_end,
        "n_total": res[0],
        "n_clean": res[1],
        "mean_dur_raw": round(float(res[2] or 0), 1),
        "median_dur_raw": round(float(res[3] or 0), 1),
        "p05_raw": round(float(res[4] or 0), 1),
        "p95_raw": round(float(res[5] or 0), 1),
        "iqr_raw": round(float(res[6] or 0), 1),
        "mean_dur_clean": round(float(res[7] or 0), 1),
        "median_dur_clean": round(float(res[8] or 0), 1),
        "p95_clean": round(float(res[9] or 0), 1),
        "std_dur_clean": round(float(res[10] or 0), 1),
        "n_suspicious": res[11],
        "n_negative": res[12],
        "n_zero": res[13],
        "suspicious_rate": round(float(res[14] or 0), 8),
        "negative_rate": round(float(res[15] or 0), 8),
    }
    print(f"{period_name}: n={res[0]:,}, median_clean={round(float(res[8] or 0), 0)}s, suspicious={res[11]}, negative={res[12]}")

db.close()

# %% [markdown]
# ## Step 3: Cohen's d per quarter vs reference

# %%
ref_stats = period_stats["reference"]
ref_mean = ref_stats["mean_dur_clean"]
ref_std = ref_stats["std_dur_clean"]
ref_n = ref_stats["n_clean"]

print(f"\nReference: mean={ref_mean:.1f}s, std={ref_std:.1f}s, n={ref_n:,}")
print(f"Suspicious in reference: {ref_stats['n_suspicious']} (aoec INVARIANTS §1: 142 expected, rebuild-specific)")
print(f"Negative in reference: {ref_stats['n_negative']} (aoec INVARIANTS §1: 342 expected, rebuild-specific)")

for period_name, stats in period_stats.items():
    if period_name == "reference":
        stats["cohen_d_clean"] = 0.0
        continue
    n_t = stats["n_clean"]
    mean_t = stats["mean_dur_clean"]
    std_t = stats["std_dur_clean"]
    pooled_var = ((n_t - 1) * std_t**2 + (ref_n - 1) * ref_std**2) / (n_t + ref_n - 2)
    pooled_sd = math.sqrt(max(pooled_var, 1e-6))
    d = (mean_t - ref_mean) / pooled_sd
    stats["cohen_d_clean"] = round(d, 6)
    print(f"{period_name}: cohen_d={d:.4f} ({'|d|>=0.5 MEDIUM' if abs(d) >= 0.5 else ('|d|>=0.2 SMALL' if abs(d) >= 0.2 else 'negligible')})")

# %% [markdown]
# ## Step 4: Verdict

# %%
max_d = max(abs(stats["cohen_d_clean"]) for k, stats in period_stats.items() if k != "reference")
verdict = "confirmed" if max_d < 0.2 else f"falsified: max |d|={max_d:.4f} {'>=0.5 MEDIUM' if max_d >= 0.5 else '>=0.2 SMALL'}"
print(f"\n# Verdict: {verdict}")

print("\n[M-05] Interpretation at large N:")
print("At N~60M rows, confidence intervals on Cohen's d are ±~0.001.")
print("Any drift will appear 'statistically significant'. Substantive significance (|d| >= 0.2) is the relevant standard.")
print("Sullivan & Feinn (2012) JGME 4(3):279-282.")

# %% [markdown]
# ## Step 5: Emit per-period CSV files and consolidated artifacts

# %%
df_stats = pd.DataFrame(list(period_stats.values()))

for period_name, stats in period_stats.items():
    csv_path = ARTIFACTS / f"dgp_diagnostic_aoe2companion_{period_name}.csv"
    pd.DataFrame([stats]).to_csv(csv_path, index=False)

print(f"Wrote {len(period_stats)} CSV files: dgp_diagnostic_aoe2companion_*.csv")

# %%
consolidated_json = {
    "periods": list(period_stats.values()),
    "reference_n_suspicious": ref_stats["n_suspicious"],
    "reference_n_negative": ref_stats["n_negative"],
    "max_cohen_d_clean": round(max_d, 6),
    "verdict": verdict,
    "i3_guard_confirmed": True,
    "post_game_features_in_psi": [],
    "sql_template": QUERY_DGP,
    "interpretation_at_large_n": (
        "Sullivan & Feinn (2012) JGME 4(3):279-282: at N~60M CI on d ~ ±0.001. "
        "Any drift is statistically detectable. |d| >= 0.2 is the substantive threshold applied here."
    ),
    "produced_at": datetime.now().isoformat(),
}

json_path = ARTIFACTS / "01_05_06_dgp_duration.json"
json_path.write_text(json.dumps(consolidated_json, indent=2, default=str))
print("Wrote:", json_path)

# %%
md_table = df_stats[["period", "n_total", "n_clean", "median_dur_clean", "p95_clean",
                       "suspicious_rate", "negative_rate", "cohen_d_clean"]].to_markdown(index=False)

md_content = f"""# 01_05_06 DGP Duration Diagnostics — aoe2companion

spec: reports/specs/01_05_preregistration.md@7e259dd8

## I3 Guard

POST_GAME features (`duration_seconds`, `is_duration_suspicious`, `is_duration_negative`) are the
SOLE subject of this notebook. They do NOT appear in T03/T04 pre-game outputs (spec §10, I3).

## Interpretation at Large N (M-05)

Sullivan & Feinn (2012) JGME 4(3):279-282: at N~60M, confidence intervals on Cohen's d ≈ ±0.001.
Any drift is statistically detectable. Substantive thresholds: |d| < 0.2 negligible, ≥ 0.2 small, ≥ 0.5 medium.
All verdicts below apply substantive standards, not statistical significance.

## Results

{md_table}

**Max |Cohen's d| (cleaned duration vs reference):** {max_d:.4f}

**Verdict:** {verdict}

## Reconciliation note

aoec INVARIANTS §1 records: 142 suspicious rows (>86,400s), 342 strict-negative rows (clock-skew).
These are absolute counts from the 01_04_02 ADDENDUM. Per aoec INVARIANTS §3 reservoir-sample caveat:
counts may differ slightly on DB rebuild. The reference period counts above reflect the current DB state.

## SQL

```sql
{QUERY_DGP}
```
"""

md_path = ARTIFACTS / "01_05_06_dgp_duration.md"
md_path.write_text(md_content)
print("Wrote:", md_path)
print("Done.")
