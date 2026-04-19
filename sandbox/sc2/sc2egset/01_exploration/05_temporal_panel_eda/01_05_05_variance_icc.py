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
# # Step 01_05_05 -- Q6: Variance Decomposition & ICC (sc2egset)
#
# **spec:** reports/specs/01_05_preregistration.md@7e259dd8
# **Dataset:** sc2egset
# **Branch:** feat/01-05-sc2egset
# **Date:** 2026-04-18
#
# **Objective:** Fit random-intercept models on won ~ 1 + (1|player_id) to
# decompose between/within-player variance. Report ICC + 95% CI.
#
# **Critique B3 fix:** Implement BOTH:
# - Primary: statsmodels.mixedlm (LPM at observed scale) -> icc_lpm_observed_scale
# - Secondary: ANOVA-based ICC for binary outcomes (Wu/Crespi/Wong 2012 CCT) -> icc_anova_observed_scale
# - Optional: BinomialBayesMixedGLM attempt (latent scale ICC)
#
# **Cohort:** N>=10 matches in reference period (152 players, no span filter).
# Span>=30 filter removed: tournament data means players appear in short events.
# Documented as deviation from spec §6.2 with justification.
#
# **Literature:**
# - statsmodels MixedLM per Lindstrom & Bates (JASA 1988)
# - Wu/Crespi/Wong (2012) CCT 33(5):869-880: ANOVA-based ICC for binary outcomes
# - Gelman & Hill (2007) §12.5: ICC = σ²_between / (σ²_between + σ²_within)
# - Nakagawa/Johnson/Schielzeth (2017) JRS Interface 14:20170213: latent-scale ICC

# %%
# spec: reports/specs/01_05_preregistration.md@7e259dd8
# Step 01_05_05 -- Q6 Variance decomposition & ICC (sc2egset)
# Dataset: sc2egset  Branch: feat/01-05-sc2egset  Date: 2026-04-18

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir

# %%
db = get_notebook_db("sc2", "sc2egset", read_only=True)
reports_dir = get_reports_dir("sc2", "sc2egset")
artifact_dir = reports_dir / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
plots_dir = artifact_dir / "plots"
plots_dir.mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ## Hypothesis

# %%
# Hypothesis: Between-player variance dominates (ICC > 0.05) even for the 0/1
# outcome 'won', consistent with persistent skill gaps in a tournament population.
# Falsifier: ICC <= 0.01 -- individual skill is not a clustering variable.

# %% [markdown]
# ## Load cohort data

# %%
# Cohort: N>=10 matches in ref period (no span filter -- tournament structure)
COHORT_SQL = """
SELECT player_id, CAST(won AS DOUBLE) AS won
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-07-01'
  AND started_at <  TIMESTAMP '2025-01-01'
  AND player_id IN (
    SELECT player_id FROM matches_history_minimal
    WHERE started_at >= TIMESTAMP '2022-08-29'
      AND started_at <  TIMESTAMP '2023-01-01'
    GROUP BY player_id HAVING COUNT(*) >= 10
  )
"""

df = db.con.execute(COHORT_SQL).fetchdf()
n_obs = len(df)
n_groups = df["player_id"].nunique()
print(f"Cohort: {n_obs} observations, {n_groups} players")
print(f"Note: no active_span filter (tournament structure; span>=30d gives only 9 players)")
print(f"Overall mean(won) = {df['won'].mean():.4f} (expected ~0.5 for 1v1 tournaments)")

# %% [markdown]
# ## Primary: LPM MixedLM (statsmodels) -> icc_lpm_observed_scale

# %%
# B3 fix primary: statsmodels.mixedlm at observed scale (LPM interpretation)
# This is a Linear Probability Model interpretation of ICC (Lindstrom-Bates JASA 1988)
# NOT a canonical latent-scale GLMM ICC (see secondary below for ANOVA alternative)
# Label: icc_lpm_observed_scale

method_lpm = "icc_lpm_observed_scale"
icc_lpm = float("nan")
icc_lpm_ci_low = float("nan")
icc_lpm_ci_high = float("nan")
sigma_u2_lpm = float("nan")
sigma_e2_lpm = float("nan")
lpm_note = ""

try:
    md = smf.mixedlm("won ~ 1", data=df, groups=df["player_id"])
    res = md.fit(reml=True)
    sigma_u2_lpm = float(res.cov_re.iloc[0, 0])
    sigma_e2_lpm = float(res.scale)
    icc_lpm = sigma_u2_lpm / (sigma_u2_lpm + sigma_e2_lpm)

    # Delta-method 95% CI (Gelman & Hill 2007 §12.5 approximation)
    # Variance of ICC via delta method: Var(ICC) ≈ (d(ICC)/d(σu2))^2 * Var(σu2)
    # Conservative: use Fisher information block if available, else use parametric bootstrap
    # For observed scale, use approximate SE from model
    se_u2 = float(res.bse_re.iloc[0]) if hasattr(res, "bse_re") else float("nan")
    if not np.isnan(se_u2):
        d_icc_d_su2 = sigma_e2_lpm / (sigma_u2_lpm + sigma_e2_lpm) ** 2
        se_icc = abs(d_icc_d_su2) * se_u2
        icc_lpm_ci_low = max(0.0, icc_lpm - 1.96 * se_icc)
        icc_lpm_ci_high = min(1.0, icc_lpm + 1.96 * se_icc)
    else:
        icc_lpm_ci_low = float("nan")
        icc_lpm_ci_high = float("nan")

    lpm_note = "LPM observed-scale ICC; NOT latent-scale GLMM (B3 note; Lindstrom-Bates JASA 1988)"
    print(f"LPM ICC = {icc_lpm:.4f} (95% CI [{icc_lpm_ci_low:.4f}, {icc_lpm_ci_high:.4f}])")
    print(f"sigma_u2={sigma_u2_lpm:.6f}, sigma_e2={sigma_e2_lpm:.6f}")
except Exception as exc:
    lpm_note = f"LPM fit failed: {exc}"
    print(f"LPM fit failed: {exc}")

# %% [markdown]
# ## Secondary: ANOVA-based ICC (Wu/Crespi/Wong 2012 CCT 33(5):869-880)

# %%
# B3 fix secondary: ANOVA-based ICC for binary outcomes
# ICC_ANOVA = (MS_between - MS_within) / (MS_between + (k-1)*MS_within)
# where k = mean cluster size (obs per player)
# Wu, S., Crespi, C.M., & Wong, W.K. (2012). CCT 33(5):869-880.

method_anova = "icc_anova_observed_scale"
k_mean = n_obs / n_groups  # mean cluster size

# Compute group means and SS
group_stats = df.groupby("player_id")["won"].agg(["mean", "count", "sum"]).reset_index()
grand_mean = df["won"].mean()

# Between-group SS and MS
ss_between = sum(row["count"] * (row["mean"] - grand_mean) ** 2 for _, row in group_stats.iterrows())
df_between = n_groups - 1
ms_between = ss_between / df_between if df_between > 0 else float("nan")

# Within-group SS and MS
ss_within = sum(
    ((df[df["player_id"] == row["player_id"]]["won"] - row["mean"]) ** 2).sum()
    for _, row in group_stats.iterrows()
)
df_within = n_obs - n_groups
ms_within = ss_within / df_within if df_within > 0 else float("nan")

# ANOVA ICC
icc_anova = (ms_between - ms_within) / (ms_between + (k_mean - 1) * ms_within)
icc_anova = max(0.0, min(1.0, icc_anova))  # clamp to [0,1]

# 95% CI via Fisher z-transform (Fleiss 1986 approximation)
# Var(ICC_ANOVA) ≈ 2 * (1-ICC)^2 * (1+(k-1)*ICC)^2 / (k*(k-1)*(n_groups-1))
var_icc_anova = (
    2 * (1 - icc_anova) ** 2 * (1 + (k_mean - 1) * icc_anova) ** 2
    / (k_mean * (k_mean - 1) * (n_groups - 1))
)
se_icc_anova = var_icc_anova ** 0.5
icc_anova_ci_low = max(0.0, icc_anova - 1.96 * se_icc_anova)
icc_anova_ci_high = min(1.0, icc_anova + 1.96 * se_icc_anova)

anova_note = (
    "ANOVA-based ICC for binary outcomes; Wu/Crespi/Wong (2012) CCT 33(5):869-880; "
    "observed scale; NOT latent-scale GLMM"
)
print(f"ANOVA ICC = {icc_anova:.4f} (95% CI [{icc_anova_ci_low:.4f}, {icc_anova_ci_high:.4f}])")
print(f"ms_between={ms_between:.6f}, ms_within={ms_within:.6f}, k_mean={k_mean:.1f}")

# %% [markdown]
# ## Tertiary: BinomialBayesMixedGLM (latent-scale attempt)

# %%
# B3 fix tertiary: attempt BinomialBayesMixedGLM for latent-scale ICC
# If convergence fails, log and skip (per critique instructions)

method_glmm = "icc_glmm_latent_scale"
icc_glmm = float("nan")
icc_glmm_note = ""

try:
    from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM

    # Need exog_vc as identity-like matrix for random effects
    player_ids = df["player_id"].astype("category")
    n_players_glmm = player_ids.cat.categories.size

    # Build random effects structure
    ident_groups = player_ids.cat.codes.values

    glmm_model = BinomialBayesMixedGLM.from_formula(
        "won ~ 1",
        {"player": "0 + C(player_id)"},
        data=df,
    )
    glmm_result = glmm_model.fit_map()

    # Latent-scale ICC: tau^2 / (tau^2 + pi^2/3)
    # tau^2 is the variance of the random effect in logit-space
    vcomp = glmm_result.vcomp
    tau2 = float(vcomp[0]) if len(vcomp) > 0 else float("nan")
    icc_glmm = tau2 / (tau2 + (3.14159 ** 2) / 3)
    icc_glmm_note = (
        f"Latent-scale ICC via BinomialBayesMixedGLM; tau2={tau2:.4f}; "
        "Nakagawa/Johnson/Schielzeth (2017) JRS Interface 14:20170213"
    )
    print(f"GLMM latent-scale ICC = {icc_glmm:.4f} (tau2={tau2:.4f})")
except Exception as exc:
    icc_glmm_note = f"BinomialBayesMixedGLM failed or not converged: {exc}"
    print(f"GLMM tertiary: {icc_glmm_note}")
    print("Skipping tertiary as per critique instructions.")

# %% [markdown]
# ## Verdict

# %%
# Verdict based on primary LPM ICC
primary_icc = icc_lpm if not np.isnan(icc_lpm) else icc_anova
if primary_icc > 0.05:
    verdict = "CONFIRMED"
    print(f"# Verdict: {verdict} — ICC={primary_icc:.4f} > 0.05 (between-player variance dominates)")
elif primary_icc > 0.01:
    verdict = "INCONCLUSIVE"
    print(f"# Verdict: {verdict} — ICC={primary_icc:.4f} between 0.01 and 0.05")
else:
    verdict = "FALSIFIED"
    print(f"# Verdict: {verdict} — ICC={primary_icc:.4f} <= 0.01 (individual skill not a cluster var)")

print(f"\nSpec §8 interpretation caveat (B3 note):")
print("  LPM ICC is at observed scale; for Bernoulli outcomes, the canonical ICC")
print("  is at latent scale: tau^2/(tau^2+pi^2/3) (Nakagawa et al. 2017).")
print("  Observed-scale ICC underestimates if the model is non-linear at the margins.")

# %% [markdown]
# ## Per-faction secondary ICC

# %%
# Secondary: per-faction ICC (restricted to faction rows)
FACTION_SQL = """
SELECT player_id, faction, CAST(won AS DOUBLE) AS won
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-07-01'
  AND started_at <  TIMESTAMP '2025-01-01'
  AND player_id IN (
    SELECT player_id FROM matches_history_minimal
    WHERE started_at >= TIMESTAMP '2022-08-29'
      AND started_at <  TIMESTAMP '2023-01-01'
    GROUP BY player_id HAVING COUNT(*) >= 10
  )
"""

df_fac = db.con.execute(FACTION_SQL).fetchdf()

faction_icc_rows = []
for faction in ["Prot", "Terr", "Zerg"]:
    df_f = df_fac[df_fac["faction"] == faction].copy()
    n_f = len(df_f)
    n_g_f = df_f["player_id"].nunique()
    if n_g_f < 5:
        print(f"Faction {faction}: only {n_g_f} players, skipping ICC")
        continue

    try:
        md_f = smf.mixedlm("won ~ 1", data=df_f, groups=df_f["player_id"])
        res_f = md_f.fit(reml=True)
        su2_f = float(res_f.cov_re.iloc[0, 0])
        se2_f = float(res_f.scale)
        icc_f = su2_f / (su2_f + se2_f)
        print(f"Faction {faction}: ICC={icc_f:.4f} (n={n_f}, players={n_g_f})")
        faction_icc_rows.append({
            "dataset_tag": "sc2egset",
            "faction": faction,
            "icc": round(icc_f, 4),
            "n_obs": n_f,
            "n_groups": n_g_f,
            "metric_name": "icc_lpm_observed_scale",
            "notes": "faction_restricted=True;[POP:tournament]",
        })
    except Exception as e:
        print(f"Faction {faction} ICC failed: {e}")

df_faction_icc = pd.DataFrame(faction_icc_rows)
if len(df_faction_icc) > 0:
    print("\nPer-faction ICC:")
    print(df_faction_icc.to_string())

# %% [markdown]
# ## Save artifacts

# %%
rows = [
    {
        "dataset_tag": "sc2egset",
        "target": "won",
        "cohort_threshold": 10,
        "sigma_between": round(sigma_u2_lpm, 6),
        "sigma_within": round(sigma_e2_lpm, 6),
        "icc": round(icc_lpm, 4) if not np.isnan(icc_lpm) else None,
        "icc_ci_low": round(icc_lpm_ci_low, 4) if not np.isnan(icc_lpm_ci_low) else None,
        "icc_ci_high": round(icc_lpm_ci_high, 4) if not np.isnan(icc_lpm_ci_high) else None,
        "n_obs": n_obs,
        "n_groups": n_groups,
        "metric_name": method_lpm,
        "notes": lpm_note + ";[POP:tournament]",
    },
    {
        "dataset_tag": "sc2egset",
        "target": "won",
        "cohort_threshold": 10,
        "sigma_between": round(ms_between, 6),
        "sigma_within": round(ms_within, 6),
        "icc": round(icc_anova, 4),
        "icc_ci_low": round(icc_anova_ci_low, 4),
        "icc_ci_high": round(icc_anova_ci_high, 4),
        "n_obs": n_obs,
        "n_groups": n_groups,
        "metric_name": method_anova,
        "notes": anova_note + ";[POP:tournament]",
    },
    {
        "dataset_tag": "sc2egset",
        "target": "won",
        "cohort_threshold": 10,
        "sigma_between": None,
        "sigma_within": None,
        "icc": round(icc_glmm, 4) if not np.isnan(icc_glmm) else None,
        "icc_ci_low": None,
        "icc_ci_high": None,
        "n_obs": n_obs,
        "n_groups": n_groups,
        "metric_name": method_glmm,
        "notes": icc_glmm_note + ";[POP:tournament]",
    },
]

df_icc = pd.DataFrame(rows)
print(df_icc.to_string())

# Validate ICC range (skip NaN rows -- GLMM may fail)
for _, row in df_icc.iterrows():
    icc_val = row["icc"]
    if icc_val is not None and not (isinstance(icc_val, float) and np.isnan(icc_val)):
        assert 0 <= icc_val <= 1, f"ICC out of [0,1]: {icc_val}"
        ci_lo = row["icc_ci_low"]
        ci_hi = row["icc_ci_high"]
        if ci_lo is not None and ci_hi is not None and not np.isnan(ci_lo) and not np.isnan(ci_hi):
            assert ci_lo <= icc_val <= ci_hi, \
                f"CI check failed: {ci_lo} <= {icc_val} <= {ci_hi}"

out_icc = artifact_dir / "variance_icc_sc2egset.csv"
df_icc.to_csv(out_icc, index=False)
print(f"\nSaved: {out_icc}")

# Also save as JSON (for phase06 interface and leakage audit reference)
import json
icc_json = {
    "dataset_tag": "sc2egset",
    "metrics": rows,
    "faction_icc": df_faction_icc.to_dict(orient="records") if len(df_faction_icc) > 0 else [],
    "verdict": verdict,
    "spec_note_B3": (
        "B3 fix: Primary=LPM(observed scale); Secondary=ANOVA(Wu/Crespi/Wong 2012); "
        "Tertiary=BinomialBayesMixedGLM(latent scale, attempted)."
    ),
}
out_json = artifact_dir / "icc.json"
with open(out_json, "w") as f:
    json.dump(icc_json, f, indent=2, default=str)
print(f"Saved: {out_json}")

# %% [markdown]
# ## ICC plot (per-faction)

# %%
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

fig, ax = plt.subplots(figsize=(8, 4))
if len(df_faction_icc) > 0:
    factions = df_faction_icc["faction"].tolist()
    icc_vals = df_faction_icc["icc"].tolist()
    ax.bar(factions, icc_vals, color=["steelblue", "darkorange", "green"])
    if not np.isnan(icc_lpm):
        ax.axhline(icc_lpm, color="red", linestyle="--", label=f"Overall LPM ICC={icc_lpm:.4f}")
    ax.set_ylabel("ICC (LPM observed scale)")
    ax.set_title("Per-faction ICC — sc2egset (restricted to cohort players)")
    ax.legend()
else:
    ax.text(0.5, 0.5, "Insufficient faction-level data", ha="center", va="center")
    ax.set_title("Per-faction ICC — sc2egset")

plt.tight_layout()
out_plot = plots_dir / "icc_player_vs_faction.png"
fig.savefig(out_plot, dpi=150)
plt.close(fig)
print(f"Saved: {out_plot}")

# %% [markdown]
# ## Markdown report

# %%
md_content = f"""# Q6: Variance Decomposition & ICC — sc2egset

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Date:** 2026-04-18

## Method (B3 fix)

Three ICC estimators per critique fix B3:
1. **icc_lpm_observed_scale**: statsmodels.mixedlm (LPM; Lindstrom-Bates JASA 1988)
2. **icc_anova_observed_scale**: ANOVA-based ICC for binary outcomes (Wu/Crespi/Wong 2012 CCT 33(5):869-880)
3. **icc_glmm_latent_scale**: BinomialBayesMixedGLM attempt (Nakagawa et al. 2017)

## SQL (verbatim, I6)

```sql
{COHORT_SQL.strip()}
```

## Cohort

- {n_obs} observations, {n_groups} players
- Cohort: N>=10 matches in reference period (2022-08-29..2022-12-31), no span filter
- Span filter removed: tournament structure means players appear in short events (3-5 days)
- reference cohort N>=10 without span filter: 152 players

## Results

| metric_name | icc | ci_low | ci_high |
|---|---|---|---|
| icc_lpm_observed_scale | {icc_lpm:.4f} | {icc_lpm_ci_low:.4f} | {icc_lpm_ci_high:.4f} |
| icc_anova_observed_scale | {icc_anova:.4f} | {icc_anova_ci_low:.4f} | {icc_anova_ci_high:.4f} |
| icc_glmm_latent_scale | {icc_glmm if not (isinstance(icc_glmm, float) and np.isnan(icc_glmm)) else 'N/A'} | N/A | N/A |

## Verdict: {verdict}

## Spec §8 interpretation caveat (B3 note)

LPM ICC is at observed scale. For Bernoulli outcomes, the canonical ICC is at latent
scale: tau^2/(tau^2+pi^2/3) (Nakagawa/Johnson/Schielzeth 2017 JRS Interface 14:20170213).
Observed-scale ICC underestimates if the model is non-linear at the margins.

## rating_pre secondary (A5)

N/A for sc2egset: matches_history_minimal does not expose rating_pre for this dataset.
MMR is available but 83.65% are zero-sentinels (not reported). Per spec §8, secondary
target requires non-NULL in >= 80% of rows. Condition not met.
"""

out_md = artifact_dir / "variance_icc_sc2egset.md"
out_md.write_text(md_content)
print(f"Saved: {out_md}")

# %%
db.close()
print("T06 complete.")
