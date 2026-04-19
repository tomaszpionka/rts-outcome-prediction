"""Variance decomposition and ICC helpers for aoe2companion temporal EDA.

spec: reports/specs/01_05_preregistration.md@7e259dd8

Implements spec §8 between/within variance decomposition via:
  Primary: statsmodels MixedLM random-intercept LMM (icc_lpm_observed_scale)
  Secondary: ANOVA-based ICC per Wu/Crespi/Wong 2012 CCT 33(5):869-880
             (icc_anova_observed_scale)

This module is a port of ``rts_predict.games.aoe2.datasets.aoestats.analysis.
variance_decomposition`` with adaptations for aoe2companion scale
(~54k eligible players vs. ~750 in aoestats' single-patch reference window).

Adaptations relative to the aoestats module:

- ``compute_icc_anova_fast``: pandas-groupby vectorization replacing the
  aoestats per-group Python loop. Total O(n log n) via groupby reductions
  instead of O(n × G), which is required at aoe2companion volume.
- ``fit_random_intercept_lmm`` accepts ``max_iter`` to bound LBFGS iterations.
- Bootstrap CI disabled by default (``n_bootstrap=0``); spec §8 mandates the
  delta-method CI on the LMM, not on the ANOVA — bootstrap is retained as an
  opt-in diagnostic only.

References:
    Gelman & Hill 2007 §12.5 (delta-method ICC).
    Nakagawa/Johnson/Schielzeth 2017 royalsocietypublishing.org/doi/10.1098/rsif.2017.0213
    Ukoumunne et al. 2012 PMC3426610 (bootstrap CI).
    Wu/Crespi/Wong 2012 CCT 33(5):869-880 (ANOVA ICC).
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import norm

logger = logging.getLogger(__name__)

RANDOM_SEED: int = 42
N_BOOTSTRAP: int = 200


def fit_random_intercept_lmm(
    df: pd.DataFrame,
    target: str,
    group: str,
    max_iter: int = 50,
) -> Any:
    """Fit a random-intercept LMM via statsmodels MixedLM.

    Formula: target ~ 1 + (1 | group)

    Args:
        df: DataFrame with target and group columns.
        target: Outcome column name.
        group: Grouping column name (random effect).
        max_iter: Max LBFGS iterations. statsmodels' default (200) is too
            slow above ~5k groups; 50 is a pragmatic ceiling.

    Returns:
        Fitted MixedLMResults object (statsmodels).

    Raises:
        ImportError: If statsmodels is not installed.
    """
    try:
        import statsmodels.formula.api as smf
    except ImportError as exc:  # pragma: no cover — statsmodels is a hard project dep
        raise ImportError("statsmodels required for LMM ICC") from exc

    model = smf.mixedlm(f"{target} ~ 1", data=df, groups=df[group])
    return model.fit(method="lbfgs", reml=True, maxiter=max_iter)


def compute_icc_lmm(
    result: Any,
    ci_level: float = 0.95,
) -> tuple[float, float, float]:
    """Compute ICC from MixedLMResults via delta method.

    ICC = sigma2_u / (sigma2_u + sigma2_e)

    Delta method CI: Gelman & Hill 2007 §12.5 via Taylor expansion of ICC in
    (sigma2_u, sigma2_e). Variance of REML estimators approximated by standard
    large-sample expressions 2*sigma2_u^2/G and 2*sigma2_e^2/(N-G) (Searle,
    Casella, McCulloch 2006 §6.5).

    Args:
        result: Fitted MixedLMResults object.
        ci_level: Confidence level (default 0.95).

    Returns:
        Tuple (icc_point, ci_lo, ci_hi). Returns all NaN if total variance <= 0.
    """
    sigma2_u = float(result.cov_re.iloc[0, 0])
    sigma2_e = float(result.scale)
    total = sigma2_u + sigma2_e

    if total <= 0:
        return (float("nan"), float("nan"), float("nan"))

    icc = sigma2_u / total

    # statsmodels MixedLMResults exposes n_groups on ``.model`` (not on the
    # result object itself — a common trip-up).
    model = result.model
    n_groups = int(getattr(model, "n_groups", len(getattr(model, "group_labels", []))))
    n_obs = int(result.nobs)

    se_u = float(np.sqrt(max(sigma2_u ** 2 * 2 / max(n_groups, 1), 0)))
    se_e = float(np.sqrt(max(sigma2_e ** 2 * 2 / max(n_obs - n_groups, 1), 0)))

    grad_u = sigma2_e / (total ** 2)
    grad_e = -sigma2_u / (total ** 2)
    se_icc = float(np.sqrt((grad_u * se_u) ** 2 + (grad_e * se_e) ** 2))

    z = float(norm.ppf(1 - (1 - ci_level) / 2))
    ci_lo = float(np.clip(icc - z * se_icc, 0, 1))
    ci_hi = float(np.clip(icc + z * se_icc, 0, 1))

    return (icc, ci_lo, ci_hi)


def compute_icc_anova_fast(
    df: pd.DataFrame,
    target: str,
    group: str,
) -> float:
    """ANOVA ICC point estimate using pandas groupby (vectorized).

    ICC_ANOVA = (MSB - MSW) / (MSB + (k - 1) * MSW)
    where k = mean group size (Wu/Crespi/Wong 2012).

    Total O(n log n) via one groupby.agg() reduction. Suitable for > 10k
    groups where the aoestats-style per-group Python loop is intractable.

    Args:
        df: DataFrame.
        target: Outcome column name.
        group: Group column name.

    Returns:
        ICC scalar clipped to [0, 1], or NaN if < 2 groups or NaN target.
    """
    values = df[target].to_numpy(dtype=float)
    if len(values) == 0:
        return float("nan")
    grand_mean = float(np.nanmean(values))

    agg = df.groupby(group)[target].agg(["count", "mean", "var"]).reset_index()
    agg = agg.rename(columns={"count": "n_i", "mean": "mean_i", "var": "var_i"})
    agg["var_i"] = agg["var_i"].fillna(0.0)

    n_groups = len(agg)
    if n_groups < 2:
        return float("nan")
    n_total = int(agg["n_i"].sum())

    ssb = float((agg["n_i"] * (agg["mean_i"] - grand_mean) ** 2).sum())
    ssw = float(((agg["n_i"] - 1) * agg["var_i"]).sum())

    msb = ssb / max(n_groups - 1, 1)
    msw = ssw / max(n_total - n_groups, 1)
    k_bar = float(agg["n_i"].mean())
    denom = msb + (k_bar - 1) * msw
    if denom <= 0:
        return 0.0
    return float(np.clip((msb - msw) / denom, 0, 1))


def compute_icc_anova(
    df: pd.DataFrame,
    target: str,
    group: str,
    n_bootstrap: int = 0,
) -> tuple[float, float, float]:
    """ANOVA ICC point estimate with optional bootstrap CI.

    Args:
        df: DataFrame with target and group columns.
        target: Outcome column name.
        group: Grouping column name.
        n_bootstrap: Bootstrap iterations. 0 (default) skips bootstrap and
            returns NaN CI — spec §8 only requires delta-method CI on the LMM.

    Returns:
        Tuple (icc_point, ci_lo, ci_hi).
    """
    icc = compute_icc_anova_fast(df, target, group)
    if np.isnan(icc) or n_bootstrap <= 0:
        return (icc, float("nan"), float("nan"))

    ci_lo, ci_hi = _bootstrap_icc_anova_ci(df, target, group, n_bootstrap=n_bootstrap)
    return (icc, ci_lo, ci_hi)


def _bootstrap_icc_anova_ci(
    df: pd.DataFrame,
    target: str,
    group: str,
    n_bootstrap: int = N_BOOTSTRAP,
    ci_level: float = 0.95,
) -> tuple[float, float]:
    """Cluster bootstrap CI for ANOVA ICC (Ukoumunne et al. 2012 PMC3426610).

    Resamples groups with replacement; each resample gets a fresh group id so
    duplicated groups count as distinct clusters (the correct cluster
    bootstrap).

    Args:
        df: Data frame.
        target: Outcome column.
        group: Group column.
        n_bootstrap: Bootstrap iterations.
        ci_level: Confidence level.

    Returns:
        Tuple (ci_lo, ci_hi). Both NaN if fewer than 10 iterations converge.
    """
    rng = np.random.default_rng(RANDOM_SEED)
    grouped = {g: sub.reset_index(drop=True) for g, sub in df.groupby(group)}
    group_ids = list(grouped.keys())
    icc_boot: list[float] = []

    for _ in range(n_bootstrap):
        sampled_groups = rng.choice(group_ids, size=len(group_ids), replace=True)
        parts: list[pd.DataFrame] = []
        tags: list[int] = []
        for i, g in enumerate(sampled_groups):
            sub = grouped[g]
            parts.append(sub)
            tags.extend([i] * len(sub))
        if not parts:
            continue
        boot_df = pd.concat(parts, ignore_index=True).copy()
        boot_df[group] = np.asarray(tags)
        icc_b = compute_icc_anova_fast(boot_df, target, group)
        if not np.isnan(icc_b):
            icc_boot.append(icc_b)

    if len(icc_boot) < 10:
        return (float("nan"), float("nan"))

    alpha = (1 - ci_level) / 2
    ci_lo = float(np.percentile(icc_boot, 100 * alpha))
    ci_hi = float(np.percentile(icc_boot, 100 * (1 - alpha)))
    return (ci_lo, ci_hi)


def stratified_reservoir_sample(
    df: pd.DataFrame,
    group: str,
    n_players: int,
    stratify_by: str | None = None,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """Sample ``n_players`` unique groups, optionally stratified by a column.

    Per critique M3: stratify by n_matches deciles, not uniform.

    Args:
        df: Full DataFrame.
        group: Column identifying each player/group.
        n_players: Target number of unique groups to sample.
        stratify_by: Column to stratify by (decile-binned). If None, uniform.
        seed: Random seed (default RANDOM_SEED).

    Returns:
        Filtered DataFrame containing only sampled groups.
    """
    rng = np.random.default_rng(seed)
    group_df = df.groupby(group).size().reset_index(name="n_matches")

    if stratify_by is not None and stratify_by in df.columns:
        strat_col = df.groupby(group)[stratify_by].sum().reset_index()
        group_df = group_df.merge(strat_col, on=group, how="left")
        n_unique = group_df["n_matches"].nunique()
        sampled_ids: list[Any]
        if n_unique < 2:
            all_ids = group_df[group].tolist()
            k = min(n_players, len(all_ids))
            sampled_ids = rng.choice(all_ids, size=k, replace=False).tolist()
        else:
            group_df["decile"] = pd.qcut(
                group_df["n_matches"],
                q=min(10, n_unique),
                labels=False,
                duplicates="drop",
            )
            sampled_ids = []
            deciles = group_df["decile"].dropna().unique()
            if len(deciles) == 0:
                deciles = [0]
                group_df["decile"] = 0
            per_decile = max(1, n_players // len(deciles))
            for d in deciles:
                candidates = group_df[group_df["decile"] == d][group].tolist()
                k = min(per_decile, len(candidates))
                sampled_ids.extend(rng.choice(candidates, size=k, replace=False).tolist())
            remaining = [g for g in group_df[group].tolist() if g not in sampled_ids]
            need = n_players - len(sampled_ids)
            if need > 0 and remaining:
                extra = rng.choice(remaining, size=min(need, len(remaining)), replace=False)
                sampled_ids.extend(extra.tolist())
            sampled_ids = sampled_ids[:n_players]
    else:
        all_ids = group_df[group].tolist()
        k = min(n_players, len(all_ids))
        sampled_ids = rng.choice(all_ids, size=k, replace=False).tolist()

    return df[df[group].isin(sampled_ids)].copy()
