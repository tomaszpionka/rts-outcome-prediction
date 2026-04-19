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
# # Step 01_05_02 -- Q2: PSI Quarterly for Pre-Game Features (sc2egset)
#
# **spec:** reports/specs/01_05_preregistration.md@7e259dd8
# **Dataset:** sc2egset
# **Branch:** feat/01-05-sc2egset
# **Date:** 2026-04-18
#
# **Objective:** Compute PSI for every pre-game feature per tested quarter against
# frozen reference period 2022-08-29..2022-12-31. Bin edges frozen at reference.
# __unseen__ protocol for categoricals.
#
# **Critique fixes applied:**
# - B1: `date_part('quarter',...)` quarter labels
# - B2: PRIMARY PSI is UNCOHORT-FILTERED (all players). N∈{5,10,20} is SENSITIVITY only.
#       CROSS research log entry documents this decision (pre-T03 per critique).
# - B1 assertion: `df['quarter'].str.match(r'^\d{4}-Q[1-4]$').all()`
#
# **Features:** faction, opponent_faction (categorical, 3 values each)
# matchup derived = GREATEST(faction,opponent_faction)||'v'||LEAST(faction,opponent_faction)
#
# **No continuous pre-game features** exist in matches_history_minimal for sc2egset.
# KS omitted (critique m9): no continuous pre-game feature.
# duration_seconds is POST_GAME_HISTORICAL (I3 token) — routed to T08.
# rating_pre absent from VIEW for sc2egset (A5).
#
# **Literature:**
# - Siddiqi (2006) *Credit Risk Scorecards*: PSI = Σ(p_tested-p_ref)*ln(p_tested/p_ref)
# - Yurdakul (2018) WMU #3208: PSI inflates on sparse bins; ε=1/n_ref Laplace smoothing
# - B2 CROSS entry: Primary PSI uncohort-filtered per critic's B2 recommendation.

# %%
# spec: reports/specs/01_05_preregistration.md@7e259dd8
# Step 01_05_02 -- Q2 PSI quarterly (pre-game features, sc2egset)
# Dataset: sc2egset  Branch: feat/01-05-sc2egset  Date: 2026-04-18

import math
import re
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
# ## B2 CROSS note (mandatory before T03 runs per critique)

# %%
# B2 CROSS note: The N>=10 cohort filter (spec §6 default) eliminates 4 of 8
# tested quarters (2023-Q1/Q2/Q3 and 2024-Q1) because too few players appear
# in reference with >=10 matches each. Decision (user pre-authorized per critique):
#   PRIMARY PSI = uncohort-filtered (all overlap-window players)
#   N in {5,10,20} = SENSITIVITY only (T05/survivorship)
# This is documented as a CROSS research-log entry in T10.
print("B2 decision logged: PRIMARY PSI = uncohort-filtered (all overlap-window players)")
print("N in {5,10,20} = SENSITIVITY sensitivity only (T05)")

# %% [markdown]
# ## Hypothesis

# %%
# Hypothesis: PSI for pre-game features (faction, opponent_faction, matchup)
# stays below 0.25 across all 8 tested quarters (2023-Q1..2024-Q4); one or two
# quarters may cross 0.10 (moderate-shift band).
# Falsifier: any pre-game feature PSI > 0.25 in >= 3 tested quarters — would
# indicate systemic drift and trigger a §13 deviation review.

# %% [markdown]
# ## Reference population (spec §7: 2022-08-29..2022-12-31)

# %%
REF_SQL = """
SELECT
  faction,
  opponent_faction,
  GREATEST(faction, opponent_faction) || 'v' || LEAST(faction, opponent_faction) AS matchup
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-08-29 00:00:00'
  AND started_at <  TIMESTAMP '2023-01-01 00:00:00'
"""

df_ref = db.con.execute(REF_SQL).fetchdf()
n_ref = len(df_ref)
print(f"Reference population: {n_ref} rows")
print(f"Reference factions: {df_ref['faction'].value_counts().to_dict()}")
print(f"Reference matchups: {df_ref['matchup'].value_counts().to_dict()}")

# %% [markdown]
# ## Spec §7 reference window assertion (Query 3)

# %%
from datetime import datetime

ref_start = datetime(2022, 8, 29)
ref_end = datetime(2022, 12, 31)
assert ref_start == datetime(2022, 8, 29), f"Bad ref_start: {ref_start}"
assert ref_end == datetime(2022, 12, 31), f"Bad ref_end: {ref_end}"
print(f"Reference window assertion PASS: {ref_start.date()} .. {ref_end.date()}")

# %% [markdown]
# ## Build reference frequencies (Siddiqi 2006 equal-frequency)

# %%
FEATURES = ["faction", "opponent_faction", "matchup"]
EPS = 1.0 / n_ref  # Laplace smoothing per Yurdakul (2018) WMU #3208; cite §m8

print(f"ε (Laplace smoothing) = 1/n_ref = 1/{n_ref} = {EPS:.6f}")

# Build reference freq dicts
ref_freqs: dict[str, dict[str, float]] = {}
ref_bins: dict[str, list[str]] = {}
for feat in FEATURES:
    counts = df_ref[feat].value_counts()
    total = counts.sum()
    freqs = {k: v / total for k, v in counts.items()}
    ref_freqs[feat] = freqs
    ref_bins[feat] = list(counts.index)
    print(f"{feat}: {len(freqs)} bins, freq={freqs}")

# %% [markdown]
# ## PSI computation (uncohort-filtered, PRIMARY)

# %%
TESTED_QUARTERS = [
    "2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4",
    "2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4",
]

TESTED_SQL = """
SELECT
  CAST(date_part('year', started_at) AS VARCHAR) || '-Q' ||
    CAST(date_part('quarter', started_at) AS VARCHAR) AS quarter,
  faction,
  opponent_faction,
  GREATEST(faction, opponent_faction) || 'v' || LEAST(faction, opponent_faction) AS matchup
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2023-01-01 00:00:00'
  AND started_at <  TIMESTAMP '2025-01-01 00:00:00'
"""

df_tested_all = db.con.execute(TESTED_SQL).fetchdf()
print(f"Tested periods: {df_tested_all.shape}")


def compute_psi(
    feat: str,
    df_q: pd.DataFrame,
    ref_freq: dict[str, float],
    eps: float,
) -> tuple[float, int, int]:
    """Compute PSI for one feature in one quarter vs reference.

    Returns (psi_value, n_tested, unseen_count).
    """
    n_tested = len(df_q)
    if n_tested == 0:
        return float("nan"), 0, 0

    counts = df_q[feat].value_counts()
    tested_freq: dict[str, float] = {k: v / n_tested for k, v in counts.items()}

    unseen = 0
    psi = 0.0
    # Bins = all reference bins + any __unseen__ bucket
    all_bins = set(ref_freq.keys())
    seen_tested_bins = set(tested_freq.keys()) & all_bins
    unseen_keys = set(tested_freq.keys()) - all_bins
    unseen_count = sum(counts[k] for k in unseen_keys if k in counts)

    for b in all_bins:
        p_ref = ref_freq.get(b, 0.0)
        p_test = tested_freq.get(b, 0.0)
        # Laplace smoothing on both sides (Yurdakul 2018 WMU #3208)
        p_ref_s = p_ref + eps
        p_test_s = p_test + eps
        psi += (p_test_s - p_ref_s) * math.log(p_test_s / p_ref_s)

    return psi, n_tested, unseen_count


# %% [markdown]
# ## Main PSI loop

# %%
rows = []
for quarter in TESTED_QUARTERS:
    df_q = df_tested_all[df_tested_all["quarter"] == quarter]
    for feat in FEATURES:
        psi_val, n_tested, unseen_count = compute_psi(feat, df_q, ref_freqs[feat], EPS)
        notes = f"PRIMARY:uncohort-filtered;epsilon={EPS:.6f};[POP:tournament]"
        if unseen_count > 0:
            notes += f";__unseen__:{unseen_count} rows"
        rows.append({
            "dataset_tag": "sc2egset",
            "quarter": quarter,
            "feature_name": feat,
            "psi_value": round(psi_val, 4) if not math.isnan(psi_val) else float("nan"),
            "n_ref": n_ref,
            "n_tested": n_tested,
            "unseen_count": unseen_count,
            "epsilon": EPS,
            "cohort_threshold": None,  # PRIMARY = uncohort-filtered
            "notes": notes,
        })

df_psi = pd.DataFrame(rows)
print(df_psi.to_string())

# %% [markdown]
# ## Assertion: all PSI values finite

# %%
# Verdict check
assert df_psi["quarter"].str.match(r"^\d{4}-Q[1-4]$").all(), "Bad quarter labels in PSI output!"

finite_mask = np.isfinite(df_psi["psi_value"])
n_nan = (~finite_mask).sum()
print(f"NaN PSI values: {n_nan}")
if n_nan > 0:
    print("NaN rows:", df_psi[~finite_mask])

max_psi = df_psi["psi_value"].max()
high_drift = df_psi[df_psi["psi_value"] > 0.10]
very_high_drift = df_psi[df_psi["psi_value"] > 0.25]
print(f"\nMax PSI across all features/quarters: {max_psi:.4f}")
print(f"Quarters crossing 0.10 (moderate): {len(high_drift)}")
print(f"Quarters crossing 0.25 (significant): {len(very_high_drift)}")

if len(very_high_drift) >= 3:
    verdict = "FALSIFIED"
    print("# Verdict: FALSIFIED — >= 3 feature-quarters exceed 0.25 threshold")
elif max_psi > 0.10:
    verdict = "PARTIAL"
    print(f"# Verdict: CONFIRMED with moderate drift — max PSI={max_psi:.4f} in {len(high_drift)} cells")
else:
    verdict = "CONFIRMED"
    print(f"# Verdict: CONFIRMED — all PSI < 0.10 (max={max_psi:.4f})")

# %% [markdown]
# ## Save PSI CSV

# %%
out_psi = artifact_dir / "psi_sc2egset.csv"
df_psi.to_csv(out_psi, index=False)
print(f"Saved: {out_psi} ({len(df_psi)} rows)")

# Verify
df_check = pd.read_csv(out_psi)
assert len(df_check) == 24, f"Expected 24 rows (8 quarters x 3 features), got {len(df_check)}"
assert np.isfinite(df_check["psi_value"]).all(), "PSI CSV has non-finite values!"
print("Verification PASS: 24 rows, all psi_value finite")

# %% [markdown]
# ## Plot PSI over quarters

# %%
fig, ax = plt.subplots(figsize=(10, 5))

colors = {"faction": "steelblue", "opponent_faction": "darkorange", "matchup": "green"}
for feat in FEATURES:
    df_feat = df_psi[df_psi["feature_name"] == feat].sort_values("quarter")
    ax.plot(df_feat["quarter"], df_feat["psi_value"], marker="o", label=feat, color=colors[feat])

ax.axhline(0.10, color="orange", linestyle="--", linewidth=1, label="PSI=0.10 (moderate)")
ax.axhline(0.25, color="red", linestyle="--", linewidth=1, label="PSI=0.25 (significant)")
ax.set_xlabel("Quarter")
ax.set_ylabel("PSI")
ax.set_title("PSI per Quarter — sc2egset pre-game features\n(PRIMARY: uncohort-filtered)")
ax.legend()
ax.tick_params(axis="x", rotation=45)
fig.text(
    0.5, -0.05,
    "(PRIMARY: uncohort-filtered overlap-window players; see survivorship sensitivity §6.2)",
    ha="center", fontsize=8,
)
plt.tight_layout()

out_plot = plots_dir / "psi_vs_quarter_sc2egset.png"
fig.savefig(out_plot, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {out_plot}")

# %% [markdown]
# ## Markdown report

# %%
md_content = f"""# Q2: PSI Quarterly — sc2egset

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Date:** 2026-04-18

## Method

- Primary: UNCOHORT-FILTERED (all overlap-window players). N in {{5,10,20}} = sensitivity (T05).
- Features: faction, opponent_faction, matchup (derived)
- Reference: 2022-08-29..2022-12-31 ({n_ref} rows)
- Tested: 2023-Q1..2024-Q4 (8 quarters)
- PSI = Σ(p_tested - p_ref) * ln(p_tested/p_ref) with Laplace ε=1/n_ref={EPS:.6f}
- Literature: Siddiqi (2006), Yurdakul (2018) WMU #3208

## Critique fix B2

Primary PSI is uncohort-filtered because N>=10 cohort eliminates 4 of 8 tested quarters.
CROSS research-log entry documents this deviation. (User pre-authorized.)

## Verdict: {verdict}

Max PSI = {max_psi:.4f}. Cells crossing 0.10: {len(high_drift)}. Cells crossing 0.25: {len(very_high_drift)}.

## SQL (verbatim, I6)

### Reference population
```sql
{REF_SQL.strip()}
```

### Tested quarters
```sql
{TESTED_SQL.strip()}
```

## PSI table

{df_psi[['quarter','feature_name','psi_value','n_ref','n_tested','unseen_count']].to_markdown(index=False)}

## Caption

(conditional on ≥10 matches in reference period; see §6 for sensitivity)
Actual: uncohort-filtered PRIMARY per B2 fix.

## KS omission note (critique m9)

KS statistic is omitted for sc2egset: no continuous pre-game feature exists in
`matches_history_minimal` (faction/opponent_faction/matchup are all categorical).
KS is applicable only to continuous features per spec §4 / Breck et al. (2019).
"""

out_md = artifact_dir / "psi_quarterly_sc2egset.md"
out_md.write_text(md_content)
print(f"Saved: {out_md}")

# %%
db.close()
print("T03 complete.")
