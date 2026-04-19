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
# # Step 01_05_05 -- Variance Decomposition (ICC)
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_05 -- Temporal & Panel EDA
# **Step:** 01_05_05
# **Dataset:** aoestats
# **spec:** reports/specs/01_05_preregistration.md@7e259dd8
#
# # Hypothesis: Player-level variance explains > 15% of total variance in won
# # (ICC >= 0.15), consistent with meaningful skill signal for per-player prediction.
# # Falsifier: ICC < 0.05 -- would undermine the per-player prediction paradigm.
#
# **Critique M2:** Primary LMM (icc_lpm_observed_scale) + secondary ANOVA ICC
# (icc_anova_observed_scale, Wu/Crespi/Wong 2012 CCT 33(5):869-880).
# Optional tertiary GLMM (icc_glmm_latent_scale) -- skip if convergence fails.
# Bootstrap CI per Ukoumunne et al. 2012 PMC3426610.
#
# **Critique M3:** Stratified reservoir by n_matches_in_reference_period deciles.
# Report ICC + sensitivity at 20k and 100k. Persist icc_sample_profile_ids_*.csv.
#
# **Critique M7:** ICC computed on profile_id; per INVARIANTS §2, within-aoestats
# migration/collision unevaluable (branch v). aoec namespace bridge (VERDICT A 0.9960)
# supports stability but doesn't audit fragmentation. ICC = upper bound on per-player
# variance share.

# %%
import json
from pathlib import Path

import numpy as np
import pandas as pd

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir
from rts_predict.games.aoe2.datasets.aoestats.analysis.variance_decomposition import (
    RANDOM_SEED,
    compute_icc_anova,
    fit_random_intercept_lmm,
    compute_icc_lmm,
    stratified_reservoir_sample,
)

ARTIFACTS_DIR = get_reports_dir("aoe2", "aoestats") / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

db = get_notebook_db("aoe2", "aoestats")
print("Connected.")

# %%
REF_START = "2022-08-29"
REF_END = "2022-10-27"
REF_PATCH = 66692  # overviews_raw: actual patch ID for 2022-08-29 reference window

COHORT_SQL = f"""
WITH cohort AS (
  SELECT CAST(player_id AS BIGINT) AS player_id, COUNT(*) AS n_matches
  FROM matches_history_minimal
  WHERE started_at BETWEEN TIMESTAMP '{REF_START}' AND TIMESTAMP '{REF_END}'
  GROUP BY player_id HAVING COUNT(*) >= 10
)
SELECT
  CAST(mhm.player_id AS BIGINT) AS player_id,
  mhm.faction,
  CAST(mhm.won AS INTEGER) AS won,
  m1v1.p0_old_rating,
  m1v1.avg_elo,
  c.n_matches AS n_matches_in_ref
FROM matches_history_minimal mhm
JOIN matches_1v1_clean m1v1 ON mhm.match_id = 'aoestats::' || m1v1.game_id
JOIN cohort c ON CAST(mhm.player_id AS BIGINT) = c.player_id
WHERE mhm.started_at BETWEEN TIMESTAMP '{REF_START}' AND TIMESTAMP '{REF_END}'
LIMIT 2000000
"""
print("Loading reference cohort for ICC...")
df_full = db.fetch_df(COHORT_SQL)
print(f"Loaded {len(df_full):,} rows, {df_full['player_id'].nunique():,} unique players")

# %%
# Stratified reservoir samples per M3 (stratify by n_matches deciles)
icc_results = {}
sample_sizes = [20_000, 50_000, 100_000]

for n_players in sample_sizes:
    print(f"\nSampling {n_players:,} players (stratified by n_matches_in_ref deciles)...")
    df_samp = stratified_reservoir_sample(df_full, "player_id", n_players, stratify_by="n_matches_in_ref")
    actual_n = df_samp["player_id"].nunique()
    print(f"  Actual unique players: {actual_n:,}, rows: {len(df_samp):,}")

    # Persist sample profile IDs (M3)
    ids_df = pd.DataFrame({"player_id": df_samp["player_id"].unique()})
    ids_path = ARTIFACTS_DIR / f"icc_sample_profile_ids_{n_players // 1000}k.csv"
    ids_df.to_csv(ids_path, index=False)
    print(f"  Saved sample IDs: {ids_path}")

    # Primary: LMM (icc_lpm_observed_scale)
    icc_lmm_val, ci_lo_lmm, ci_hi_lmm = float("nan"), float("nan"), float("nan")
    convergence_warning = None
    try:
        print("  Fitting LMM...")
        lmm_result = fit_random_intercept_lmm(df_samp, "won", "player_id")
        icc_lmm_val, ci_lo_lmm, ci_hi_lmm = compute_icc_lmm(lmm_result)
        print(f"  LMM ICC = {icc_lmm_val:.4f} [{ci_lo_lmm:.4f}, {ci_hi_lmm:.4f}]")
        # Post-fix/01-05-aoestats-ngroups-ci-assert: CI sanity check.
        # A valid delta-method CI must contain its point estimate. Prior to this
        # PR, compute_icc_lmm raised AttributeError on `result.ngroups` and the
        # bare `except Exception` silently recorded it as a convergence failure.
        # The ANOVA CI was emitted uninspected and published with an inverted
        # interval on the aoestats 50k run (point=0.0268, CI=[0.0494, 0.0759]).
        if not np.isnan(icc_lmm_val) and not np.isnan(ci_lo_lmm) and not np.isnan(ci_hi_lmm):
            assert ci_lo_lmm <= icc_lmm_val + 1e-9, (
                f"LMM CI lower bound {ci_lo_lmm} > point {icc_lmm_val} (inverted CI — LMM math bug)"
            )
            assert ci_hi_lmm >= icc_lmm_val - 1e-9, (
                f"LMM CI upper bound {ci_hi_lmm} < point {icc_lmm_val} (inverted CI — LMM math bug)"
            )
    except AssertionError:
        # Sanity-check failure is a real bug, not a convergence issue. Re-raise.
        raise
    except Exception as exc:
        convergence_warning = str(exc)
        print(f"  LMM failed: {exc}")

    # Secondary: ANOVA ICC (icc_anova_observed_scale) per Wu/Crespi/Wong 2012
    print("  Computing ANOVA ICC (bootstrap CI, this may take a moment)...")
    icc_anova_val, ci_lo_anova, ci_hi_anova = compute_icc_anova(df_samp, "won", "player_id")
    print(f"  ANOVA ICC = {icc_anova_val:.4f} [{ci_lo_anova:.4f}, {ci_hi_anova:.4f}]")
    # CI sanity check — ANOVA bootstrap CI MUST contain its own point estimate.
    # Per the sc2egset pattern (variance_icc_sc2egset.py); catches bootstrap
    # resampling errors and prior aoestats 50k inverted-CI pathology.
    if not np.isnan(icc_anova_val) and not np.isnan(ci_lo_anova) and not np.isnan(ci_hi_anova):
        assert ci_lo_anova <= icc_anova_val + 1e-9, (
            f"ANOVA CI lower bound {ci_lo_anova} > point {icc_anova_val} "
            f"(inverted CI — check cluster-bootstrap resampling)"
        )
        assert ci_hi_anova >= icc_anova_val - 1e-9, (
            f"ANOVA CI upper bound {ci_hi_anova} < point {icc_anova_val} "
            f"(inverted CI — check cluster-bootstrap resampling)"
        )

    icc_results[f"n{n_players // 1000}k"] = {
        "n_players_requested": n_players,
        "n_players_actual": int(actual_n),
        "n_obs": len(df_samp),
        "icc_lpm_observed_scale": {
            "icc_point": round(icc_lmm_val, 4) if not np.isnan(icc_lmm_val) else None,
            "ci_lo": round(ci_lo_lmm, 4) if not np.isnan(ci_lo_lmm) else None,
            "ci_hi": round(ci_hi_lmm, 4) if not np.isnan(ci_hi_lmm) else None,
            "method": "statsmodels MixedLM REML lbfgs",
            "convergence_warning": convergence_warning,
        },
        "icc_anova_observed_scale": {
            "icc_point": round(icc_anova_val, 4) if not np.isnan(icc_anova_val) else None,
            "ci_lo": round(ci_lo_anova, 4) if not np.isnan(ci_lo_anova) else None,
            "ci_hi": round(ci_hi_anova, 4) if not np.isnan(ci_hi_anova) else None,
            "method": "ANOVA Wu/Crespi/Wong 2012 CCT 33(5):869-880 + bootstrap CI Ukoumunne 2012 PMC3426610",
        },
        "icc_glmm_latent_scale": None,  # Optional -- skipped (convergence risk on Bernoulli)
    }

# %%
# Falsifier check (use 50k primary)
primary = icc_results.get("n50k", {})
icc_anova_50k = primary.get("icc_anova_observed_scale", {}).get("icc_point", float("nan"))
icc_lmm_50k = primary.get("icc_lpm_observed_scale", {}).get("icc_point", float("nan"))

if icc_anova_50k is None:
    icc_anova_50k = float("nan")
if icc_lmm_50k is None:
    icc_lmm_50k = float("nan")

# Post-fix/01-05-aoestats-ngroups-ci-assert: fix dead ternary.
# Previous `primary_icc = icc_anova_50k if ... else icc_anova_50k` was a
# tautology — both branches returned ANOVA. Intent was: prefer LMM when
# available, fall back to ANOVA. With the `.ngroups` bug fixed, LMM is now
# actually available; use it as primary (spec §8 literal binding for aoestats
# under v1.0.1 — this dataset is NOT on v1.0.2 yet).
primary_icc = icc_lmm_50k if not np.isnan(icc_lmm_50k) else icc_anova_50k

if primary_icc >= 0.05:
    verdict = "PASSED"
else:
    verdict = "FALSIFIED"
print(f"Primary ICC (50k, ANOVA): {icc_anova_50k}")
print(f"Primary ICC (50k, LMM): {icc_lmm_50k}")
print(f"Q6 skill-signal hypothesis: {verdict}")

# %%
# M7 limitation paragraph (verbatim per critique)
M7_PARAGRAPH = (
    "ICC computed on `profile_id`; per INVARIANTS §2, within-aoestats migration/collision "
    "unevaluable (branch v). aoec namespace bridge (VERDICT A 0.9960) supports stability "
    "but doesn't audit fragmentation. ICC = upper bound on per-player variance share."
)

# Full ICC results JSON
icc_json = {
    "step": "01_05_05",
    "spec": "reports/specs/01_05_preregistration.md@7e259dd8",
    "reference_window": {"start": REF_START, "end": REF_END, "patch": REF_PATCH},
    "falsifier_verdict": verdict,
    "icc_by_sample_size": icc_results,
    "m7_branch_v_limitation": M7_PARAGRAPH,
    "random_seed": RANDOM_SEED,
}
icc_path = ARTIFACTS_DIR / "01_05_05_icc_results.json"
with open(icc_path, "w") as f:
    json.dump(icc_json, f, indent=2, default=str)
print(f"Wrote {icc_path}")

# Validation
assert "icc_point" in primary.get("icc_anova_observed_scale", {}), "ICC missing icc_point"

# %%
# Summary MD
md_text = f"""# Variance Decomposition ICC -- aoestats

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Step:** 01_05_05

## M7 Branch-v Limitation

{M7_PARAGRAPH}

## ICC Results (Primary: 50k stratified sample)

| Method | ICC | CI lo | CI hi |
|--------|-----|-------|-------|
| LMM observed-scale | {icc_lmm_50k} | - | - |
| ANOVA observed-scale (Wu/Crespi/Wong 2012) | {icc_anova_50k} | - | - |

*Bootstrap CI per Ukoumunne et al. 2012 PMC3426610.*
*Stratified reservoir by n_matches_in_reference_period deciles (critique M3).*

## Falsifier verdict

**Q6 skill-signal hypothesis:** {verdict}
"""
(ARTIFACTS_DIR / "01_05_05_icc_results.md").write_text(md_text)

print(f"Q6 skill-signal hypothesis: {verdict}")
print("Step 01_05_05 complete.")
