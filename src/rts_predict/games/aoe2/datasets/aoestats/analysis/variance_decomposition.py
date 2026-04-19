"""Variance decomposition and ICC helpers for aoestats temporal EDA.

spec: reports/specs/01_05_preregistration.md@7e259dd8

Implements spec §8 between/within variance decomposition via:
  Primary: statsmodels MixedLM random-intercept LMM (icc_lpm_observed_scale)
  Secondary: ANOVA-based ICC per Wu/Crespi/Wong 2012 CCT 33(5):869-880
             (icc_anova_observed_scale)
  Optional tertiary: logistic GLMM latent-scale (icc_glmm_latent_scale)
  Bootstrap CI: Ukoumunne et al. 2012 PMC3426610

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

logger = logging.getLogger(__name__)

RANDOM_SEED: int = 42
N_BOOTSTRAP: int = 200  # Ukoumunne et al. recommend >= 200 for stable CI


def fit_random_intercept_lmm(
    df: pd.DataFrame,
    target: str,
    group: str,
) -> Any:
    """Fit a random-intercept LMM via statsmodels MixedLM.

    Formula: target ~ 1 + (1 | group)

    Args:
        df: DataFrame with target and group columns.
        target: Outcome column name.
        group: Grouping column name (random effect).

    Returns:
        Fitted MixedLMResults object (statsmodels).

    Raises:
        ImportError: If statsmodels is not installed.
    """
    try:
        import statsmodels.formula.api as smf
    except ImportError as exc:
        raise ImportError("statsmodels required for LMM ICC") from exc

    model = smf.mixedlm(f"{target} ~ 1", data=df, groups=df[group])
    result = model.fit(method="lbfgs", reml=True)
    return result


def compute_icc_lmm(
    result: Any,
    ci_level: float = 0.95,
) -> tuple[float, float, float]:
    """Compute ICC from MixedLMResults via delta method.

    ICC = sigma2_u / (sigma2_u + sigma2_e)

    Delta method CI: Gelman & Hill 2007 §12.5 via Taylor expansion.

    Args:
        result: Fitted MixedLMResults object.
        ci_level: Confidence level (default 0.95).

    Returns:
        Tuple (icc_point, ci_lo, ci_hi).
    """
    sigma2_u = float(result.cov_re.iloc[0, 0])
    sigma2_e = float(result.scale)
    total = sigma2_u + sigma2_e

    if total <= 0:
        return (float("nan"), float("nan"), float("nan"))

    icc = sigma2_u / total

    # Delta method variance approximation
    # d(ICC)/d(sigma2_u) = sigma2_e / total^2
    # d(ICC)/d(sigma2_e) = -sigma2_u / total^2
    #
    # NOTE: statsmodels MixedLMResults exposes n_groups on `.model`, not on the
    # result object. The attribute `result.ngroups` does NOT exist and raises
    # AttributeError. Pre-fix/01-05-aoestats-ngroups-ci-assert this function
    # referenced the non-existent attribute, causing all LMM delta-method CI
    # computations to crash via AttributeError — which the calling notebook's
    # bare `except Exception` block caught and mislabeled as "LMM convergence
    # failure." See the aoec port in
    # src/rts_predict/games/aoe2/datasets/aoe2companion/analysis/variance_decomposition.py
    # which uses the correct accessor.
    model = result.model
    n_groups = int(getattr(model, "n_groups", len(getattr(model, "group_labels", []))))
    n_obs = int(result.nobs)
    se_u = float(np.sqrt(max(sigma2_u ** 2 * 2 / max(n_groups, 1), 0)))
    se_e = float(np.sqrt(max(sigma2_e ** 2 * 2 / max(n_obs - n_groups, 1), 0)))

    grad_u = sigma2_e / (total ** 2)
    grad_e = -sigma2_u / (total ** 2)
    se_icc = float(np.sqrt((grad_u * se_u) ** 2 + (grad_e * se_e) ** 2))

    z = float(np.abs(np.percentile(np.random.default_rng(RANDOM_SEED).standard_normal(10_000),
                                    100 * (1 - (1 - ci_level) / 2))))
    ci_lo = float(np.clip(icc - z * se_icc, 0, 1))
    ci_hi = float(np.clip(icc + z * se_icc, 0, 1))

    return (icc, ci_lo, ci_hi)


def compute_icc_anova(
    df: pd.DataFrame,
    target: str,
    group: str,
) -> tuple[float, float, float]:
    """Compute ANOVA-based ICC per Wu/Crespi/Wong 2012 CCT 33(5):869-880.

    ICC_ANOVA = (MSB - MSW) / (MSB + (k-1) * MSW)
    where k = mean group size.

    Args:
        df: DataFrame with target and group columns.
        target: Outcome column name.
        group: Grouping column name.

    Returns:
        Tuple (icc_point, ci_lo, ci_hi) using bootstrap CI (Ukoumunne 2012).
    """
    groups = df[group].to_numpy()
    values = df[target].to_numpy(dtype=float)

    icc = _icc_anova_point(groups, values)
    if np.isnan(icc):
        return (float("nan"), float("nan"), float("nan"))

    # Bootstrap CI per Ukoumunne et al. 2012 PMC3426610
    ci_lo, ci_hi = _bootstrap_icc_anova_ci(df, target, group, n_bootstrap=N_BOOTSTRAP)
    return (icc, ci_lo, ci_hi)


def _icc_anova_point(
    groups: np.ndarray,
    values: np.ndarray,
) -> float:
    """Compute ANOVA ICC point estimate from raw arrays (no recursion).

    Args:
        groups: Group label array.
        values: Outcome value array.

    Returns:
        ICC scalar (clipped to [0, 1]).
    """
    grand_mean = float(np.nanmean(values))
    group_labels = np.unique(groups)
    n_groups = len(group_labels)
    if n_groups < 2:
        return float("nan")

    ssb = 0.0
    ssw = 0.0
    n_total = len(values)
    k_sizes = []
    for g in group_labels:
        mask = groups == g
        g_vals = values[mask]
        g_n = len(g_vals)
        g_mean = float(np.nanmean(g_vals))
        ssb += g_n * (g_mean - grand_mean) ** 2
        ssw += float(np.nansum((g_vals - g_mean) ** 2))
        k_sizes.append(g_n)

    msb = ssb / max(n_groups - 1, 1)
    msw = ssw / max(n_total - n_groups, 1)
    k_bar = float(np.mean(k_sizes))
    denom = msb + (k_bar - 1) * msw
    if denom <= 0:
        return 0.0
    return float(np.clip((msb - msw) / denom, 0, 1))


def _bootstrap_icc_anova_ci(
    df: pd.DataFrame,
    target: str,
    group: str,
    n_bootstrap: int = N_BOOTSTRAP,
    ci_level: float = 0.95,
) -> tuple[float, float]:
    """Bootstrap CI for ANOVA ICC.

    Resamples groups with replacement (cluster bootstrap).
    Per Ukoumunne et al. 2012 PMC3426610.

    Args:
        df: Data frame.
        target: Outcome column.
        group: Group column.
        n_bootstrap: Number of bootstrap iterations (default 200).
        ci_level: Confidence level.

    Returns:
        Tuple (ci_lo, ci_hi).
    """
    # Pre-fix/01-05-aoestats-ngroups-ci-assert: the bootstrap resampled with
    # replacement but reused the ORIGINAL group id in boot_g / boot_v. When a
    # group was sampled k times, the concatenated arrays held k*n_i rows all
    # tagged with the same group id, so `_icc_anova_point` groupby collapsed
    # them into ONE cluster of size k*n_i. This inflated k_bar while keeping
    # n_groups at its original value, biasing SSB upward and producing CIs
    # that did not contain the point estimate (aoestats 50k run: point=0.0268,
    # "CI"=[0.0494, 0.0759] — inverted). See the 2026-04-19 pre-01_06
    # adversarial review and the aoec port
    # src/rts_predict/games/aoe2/datasets/aoe2companion/analysis/
    # variance_decomposition.py which implements the correct cluster bootstrap
    # by re-tagging each resampled group with a fresh unique id.
    rng = np.random.default_rng(RANDOM_SEED)
    group_ids = df[group].unique()
    groups_arr = df[group].to_numpy()
    values_arr = df[target].to_numpy(dtype=float)
    # Pre-index each group's row positions once — O(N) — so the bootstrap
    # inner loop is O(sum of sampled group sizes) instead of O(n_groups * N).
    group_to_positions: dict[Any, np.ndarray] = {
        g: np.flatnonzero(groups_arr == g) for g in group_ids
    }
    icc_boot = []

    for _ in range(n_bootstrap):
        sampled_groups = rng.choice(group_ids, size=len(group_ids), replace=True)
        parts_v: list[np.ndarray] = []
        parts_tag: list[np.ndarray] = []
        for i, g in enumerate(sampled_groups):
            pos = group_to_positions[g]
            parts_v.append(values_arr[pos])
            # Correct cluster bootstrap: tag this resample with a fresh unique
            # id (i). A duplicated group (same `g`) now counts as two distinct
            # clusters in the ANOVA ICC formula, as the cluster bootstrap
            # requires (Ukoumunne et al. 2012 PMC3426610).
            parts_tag.append(np.full(len(pos), i, dtype=np.int64))
        if not parts_v:
            continue
        bv = np.concatenate(parts_v)
        bg = np.concatenate(parts_tag)
        icc_b = _icc_anova_point(bg, bv)
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
    """Sample n_players unique groups stratified by a column.

    Per critique M3: stratify reservoir by n_matches deciles, not uniform.

    Args:
        df: Full DataFrame.
        group: Column identifying each player/group.
        n_players: Target number of unique groups to sample.
        stratify_by: Column to stratify by (deciles). If None, uniform sample.
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
        group_df["decile"] = pd.qcut(
            group_df["n_matches"], q=min(10, n_unique), labels=False, duplicates="drop"
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
        # top-up or trim to n_players
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
