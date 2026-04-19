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
# # 01_05_05 ICC Variance Decomposition — aoe2companion
# spec: reports/specs/01_05_preregistration.md@7e259dd8
#
# **Spec §§:** §7 (reference window), §8 (variance decomposition — random-intercept LMM on player_id).
#
# **Scope (post-hang recovery):** Operates on the spec §7 reference window
# (2022-08-29 .. 2022-12-31) only, NOT the full analysis window. The earlier
# attempt at this notebook tried to fit `statsmodels.mixedlm` on ~7M rows ×
# ~20k groups over the full 2.5-year analysis window and hung indefinitely.
# Root cause: mixedlm cost is ~O(G × iter); ≥20k groups is intractable under
# default settings.
#
# **Sample-size strategy.**
# - Persist sample profile IDs at {5k, 10k, 20k} for reproducibility.
# - Fit LMM at 5k (primary) and 10k (sensitivity).
# - Skip LMM at 20k (cost-prohibitive); compute ANOVA ICC instead.
# - ANOVA ICC computed at all three sizes via the pandas-groupby fast path
#   (`compute_icc_anova_fast` in the dataset analysis module).
#
# **Method (spec §8):** Random-intercept LMM `won ~ 1 + (1 | player_id)` via
# `statsmodels.mixedlm`, REML, LBFGS (max_iter=50). Delta-method 95% CI per
# Gelman & Hill 2007 §12.5.
#
# **Secondary (critique B-01 carry-over):** ANOVA-based ICC per Wu/Crespi/Wong
# 2012 CCT 33(5):869-880 — observed-scale, robust under LMM non-convergence.
#
# **Hypothesis:** ICC_lpm in [0.05, 0.20], consistent with meaningful but not
# dominant between-player variance under competitive matchmaking.
# **Falsifier:** ICC_lpm < 0.02 or > 0.50.

# %% [markdown]
# ## Imports

# %%
import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir
from rts_predict.games.aoe2.datasets.aoe2companion.analysis.variance_decomposition import (
    RANDOM_SEED,
    compute_icc_anova_fast,
    compute_icc_lmm,
    fit_random_intercept_lmm,
    stratified_reservoir_sample,
)

ARTIFACTS = get_reports_dir("aoe2", "aoe2companion") / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

REF_START = "2022-08-29"
REF_END_EXCLUSIVE = "2023-01-01"  # §9 Query 3 assertion uses ref_end = 2022-12-31 (date-inclusive == timestamp < 2023-01-01)
MIN_OBS_PER_PLAYER = 10  # spec §8
SAMPLE_SIZES = [5_000, 10_000, 20_000]
LMM_SAMPLE_SIZES = [5_000, 10_000]  # Skip LMM at 20k — mixedlm cost-prohibitive

print("Artifacts dir:", ARTIFACTS)

# Spec §9 Query 3 assertion (reference-window window constants match spec §7)
assert datetime.fromisoformat(REF_START) == datetime(2022, 8, 29), f"Bad ref_start: {REF_START}"
assert datetime.fromisoformat(REF_END_EXCLUSIVE) == datetime(2023, 1, 1), f"Bad ref_end_exclusive: {REF_END_EXCLUSIVE}"
print("Reference window bounds match spec §7.")

# %% [markdown]
# ## Step 1: Load reference-window cohort (spec §7)
# ~4M rows, ~114k unique players — manageable in RAM.

# %%
COHORT_SQL = f"""
WITH eligible AS (
  SELECT player_id, COUNT(*) AS n_matches_in_ref
  FROM matches_history_minimal
  WHERE started_at >= TIMESTAMP '{REF_START}'
    AND started_at <  TIMESTAMP '{REF_END_EXCLUSIVE}'
  GROUP BY player_id
  HAVING COUNT(*) >= {MIN_OBS_PER_PLAYER}
)
SELECT
  mhm.player_id,
  mhm.faction,
  CAST(mhm.won AS INTEGER) AS won,
  e.n_matches_in_ref
FROM matches_history_minimal mhm
JOIN eligible e USING (player_id)
WHERE mhm.started_at >= TIMESTAMP '{REF_START}'
  AND mhm.started_at <  TIMESTAMP '{REF_END_EXCLUSIVE}'
"""

db = get_notebook_db("aoe2", "aoe2companion", read_only=True)
print("Loading reference-window cohort...")
df_full = db.con.execute(COHORT_SQL).df()
print(f"Loaded {len(df_full):,} rows, {df_full['player_id'].nunique():,} unique players")
print(f"won mean: {df_full['won'].mean():.4f}")
db.close()

# %% [markdown]
# ## Step 2: Stratified sampling at each size (persist IDs per critique M-06)

# %%
np.random.seed(RANDOM_SEED)
sample_frames: dict[int, pd.DataFrame] = {}

for n_players in SAMPLE_SIZES:
    df_s = stratified_reservoir_sample(
        df_full, "player_id", n_players, stratify_by="n_matches_in_ref", seed=RANDOM_SEED
    )
    actual_n = df_s["player_id"].nunique()
    sample_frames[n_players] = df_s

    ids_df = pd.DataFrame({"player_id": df_s["player_id"].unique()})
    ids_path = ARTIFACTS / f"icc_sample_profileIds_{n_players // 1000}k.csv"
    ids_df.to_csv(ids_path, index=False)
    print(f"  n_requested={n_players:,} actual_unique={actual_n:,} rows={len(df_s):,} → {ids_path.name}")

# %% [markdown]
# ## Step 3: Primary LMM at 5k (spec §8)
# Random-intercept LMM via statsmodels.mixedlm; delta-method 95% CI.

# %%
primary_n = 5_000
df_primary = sample_frames[primary_n]
print(f"Fitting primary LMM at n={primary_n:,} (rows={len(df_primary):,})...")

try:
    lmm_result = fit_random_intercept_lmm(df_primary, "won", "player_id", max_iter=50)
    icc_lpm, icc_ci_low, icc_ci_high = compute_icc_lmm(lmm_result)
    lpm_converged = bool(lmm_result.converged)
    tau2_lpm = float(lmm_result.cov_re.iloc[0, 0])
    sigma2_lpm = float(lmm_result.scale)
    lpm_error = None
    print(f"LMM: ICC={icc_lpm:.6f} [{icc_ci_low:.6f}, {icc_ci_high:.6f}] converged={lpm_converged}")
    print(f"  tau2={tau2_lpm:.6f}  sigma2={sigma2_lpm:.6f}")
except Exception as exc:
    lmm_result = None
    icc_lpm = icc_ci_low = icc_ci_high = float("nan")
    tau2_lpm = sigma2_lpm = float("nan")
    lpm_converged = False
    lpm_error = str(exc)
    print(f"LMM failed: {exc}")

# %% [markdown]
# ## Step 4: ANOVA ICC at every sample size (fast path, observed-scale)

# %%
anova_by_size: dict[int, float] = {}
for n_players, df_s in sample_frames.items():
    icc_a = compute_icc_anova_fast(df_s, "won", "player_id")
    anova_by_size[n_players] = icc_a
    print(f"  ANOVA ICC @ n={n_players:,}: {icc_a:.6f}")

icc_anova_primary = anova_by_size[primary_n]

# %% [markdown]
# ## Step 5: LMM sensitivity at 10k (skip 20k — mixedlm cost-prohibitive)

# %%
sensitivity: dict[int, dict] = {}
for n_players in LMM_SAMPLE_SIZES:
    if n_players == primary_n:
        sensitivity[n_players] = {
            "icc_lmm": round(icc_lpm, 6) if not np.isnan(icc_lpm) else None,
            "converged": lpm_converged,
            "note": "primary",
        }
        continue
    df_s = sample_frames[n_players]
    print(f"Fitting sensitivity LMM at n={n_players:,} (rows={len(df_s):,})...")
    try:
        r_s = fit_random_intercept_lmm(df_s, "won", "player_id", max_iter=50)
        icc_s, _, _ = compute_icc_lmm(r_s)
        sensitivity[n_players] = {
            "icc_lmm": round(float(icc_s), 6),
            "converged": bool(r_s.converged),
        }
        print(f"  ICC_lmm={icc_s:.6f} converged={r_s.converged}")
    except Exception as exc:
        sensitivity[n_players] = {"icc_lmm": None, "converged": False, "error": str(exc)}
        print(f"  Failed: {exc}")

sensitivity[20_000] = {
    "icc_lmm": None,
    "converged": False,
    "note": "skipped — mixedlm cost-prohibitive at 20k groups; ANOVA ICC reported instead",
    "icc_anova_at_size": round(float(anova_by_size[20_000]), 6),
}

# %% [markdown]
# ## Step 6: Verdict

# %%
obs_per_player = df_primary.groupby("player_id")["won"].count()
if not np.isnan(icc_lpm) and 0.05 <= icc_lpm <= 0.20:
    verdict = "confirmed"
elif np.isnan(icc_lpm):
    # Fall through to ANOVA if LMM failed
    if 0.05 <= icc_anova_primary <= 0.20:
        verdict = "confirmed_via_anova_fallback"
    else:
        verdict = f"inconclusive: LMM failed, ANOVA={icc_anova_primary:.6f}"
else:
    verdict = f"falsified: ICC_lpm={icc_lpm:.6f} outside [0.05, 0.20]"
print(f"\nVerdict: {verdict}")

# %% [markdown]
# ## Step 7: Emit artifacts (JSON + MD)

# %%
json_out = {
    "spec": "reports/specs/01_05_preregistration.md@7e259dd8",
    "reference_window": {"start": REF_START, "end_exclusive": REF_END_EXCLUSIVE},
    "min_obs_per_player": MIN_OBS_PER_PLAYER,
    "primary_sample_size": primary_n,

    # Primary (LMM on 5k sample)
    "icc_lpm_observed_scale": round(float(icc_lpm), 6) if not np.isnan(icc_lpm) else None,
    "icc_lpm_ci_low": round(float(icc_ci_low), 6) if not np.isnan(icc_ci_low) else None,
    "icc_lpm_ci_high": round(float(icc_ci_high), 6) if not np.isnan(icc_ci_high) else None,
    "tau2_lpm": round(float(tau2_lpm), 6) if not np.isnan(tau2_lpm) else None,
    "sigma2_lpm": round(float(sigma2_lpm), 6) if not np.isnan(sigma2_lpm) else None,
    "lpm_converged": lpm_converged,
    "lpm_error": lpm_error,

    # Secondary (ANOVA at primary size)
    "icc_anova_observed_scale": round(float(icc_anova_primary), 6),
    "icc_anova_by_sample_size": {str(n): round(float(v), 6) for n, v in anova_by_size.items()},

    # GLMM not run — spec §8 only requires LMM; skip per cost/convergence tradeoff
    "icc_glmm_latent_scale": None,

    # Cohort stats
    "n_players_primary": int(df_primary["player_id"].nunique()),
    "n_obs_primary": int(len(df_primary)),
    "n_obs_per_player_median": round(float(obs_per_player.median()), 1),
    "n_obs_per_player_mean": round(float(obs_per_player.mean()), 1),
    "n_eligible_players_total": int(df_full["player_id"].nunique()),

    "sensitivity": {f"n_{k}": v for k, v in sensitivity.items()},
    "sample_files": {
        f"{n // 1000}k": str(ARTIFACTS / f"icc_sample_profileIds_{n // 1000}k.csv")
        for n in SAMPLE_SIZES
    },
    "sql": {"cohort_query": COHORT_SQL},
    "verdict": verdict,
    "produced_at": datetime.now().isoformat(),
    "methodology_note": (
        "LMM fit on 5k stratified sample (primary) + 10k (sensitivity). 20k skipped: "
        "statsmodels.mixedlm cost ~O(G × iter) makes ≥20k groups intractable at aoec scale. "
        "ANOVA ICC (pandas-groupby fast path) computed at all three sample sizes as robust "
        "secondary (observed-scale, per Wu/Crespi/Wong 2012)."
    ),
}

json_path = ARTIFACTS / "01_05_05_icc.json"
json_path.write_text(json.dumps(json_out, indent=2, default=str))
print(f"Wrote: {json_path}")

md_content = f"""# 01_05_05 ICC Variance Decomposition — aoe2companion

spec: reports/specs/01_05_preregistration.md@7e259dd8

## Method

Random-intercept LMM `won ~ 1 + (1 | player_id)` via `statsmodels.mixedlm`,
REML, LBFGS (max_iter=50). Delta-method 95% CI per Gelman & Hill 2007 §12.5.
Secondary: ANOVA-based ICC per Wu/Crespi/Wong 2012 (observed-scale).

Reference window: {REF_START} to {REF_END_EXCLUSIVE} (exclusive), min {MIN_OBS_PER_PLAYER} matches/player.
Primary sample size: {primary_n:,} (stratified by n_matches_in_ref deciles, seed={RANDOM_SEED}).

## Scope notes (post-hang recovery)

- Previous run attempted LMM on ~7M rows × ~20k groups over the full analysis
  window and hung indefinitely. This rewrite restricts to the spec §7
  reference window and caps LMM at 10k groups.
- ANOVA ICC is computed via a pandas-groupby fast path at all sample sizes.
- GLMM (latent-scale) skipped: spec §8 only binds the LMM method; GLMM is
  optional and was a convergence risk in the previous run.

## Results (primary: 5k stratified sample)

| Metric | Value | Notes |
|---|---|---|
| `icc_lpm_observed_scale` | {icc_lpm:.6f} | LMM; converged={lpm_converged} |
| `icc_lpm_ci_low` | {icc_ci_low:.6f} | Delta-method 95% CI lower |
| `icc_lpm_ci_high` | {icc_ci_high:.6f} | Delta-method 95% CI upper |
| `icc_anova_observed_scale` | {icc_anova_primary:.6f} | ANOVA @ 5k (Wu/Crespi/Wong 2012) |
| `n_players_primary` | {int(df_primary['player_id'].nunique()):,} | |
| `n_obs_primary` | {int(len(df_primary)):,} | |
| `obs_per_player_median` | {round(float(obs_per_player.median()), 1)} | |
| `n_eligible_players_total` | {int(df_full['player_id'].nunique()):,} | population |

## ANOVA ICC by sample size

| n_players | ICC_anova |
|---|---|
"""
for n, v in anova_by_size.items():
    md_content += f"| {n:,} | {v:.6f} |\n"

md_content += f"""
## Verdict

**{verdict}**

## SQL (cohort load)

```sql
{COHORT_SQL.strip()}
```

## Literature

- Gelman & Hill (2007) *Data Analysis Using Regression and Multilevel/Hierarchical Models*, §12.5 — delta-method CI for ICC.
- Wu, Crespi, Wong (2012) CCT 33(5):869-880 — ANOVA ICC for clustered binary outcomes.
- Ukoumunne et al. (2012) PMC3426610 — cluster bootstrap CI (not used here; opt-in in helper).
"""

md_path = ARTIFACTS / "01_05_05_icc.md"
md_path.write_text(md_content)
print(f"Wrote: {md_path}")
print("Done.")
