"""Population Stability Index (PSI) helpers for aoestats temporal EDA.

spec: reports/specs/01_05_preregistration.md@7e259dd8

Implements spec §4 equal-frequency PSI with frozen reference edges.
Feature-type routing per critique fix B2:
  - Continuous (p0_old_rating, p1_old_rating, focal_old_rating, avg_elo):
    decile PSI (Siddiqi 2006)
  - Binary (mirror, p0_is_unrated, p1_is_unrated): exact-value frequency
    histogram + Cohen's h (Cohen 1988)
  - High-cardinality categorical (faction, opponent_faction, map):
    categorical-frequency with __unseen__ bin

References:
    Siddiqi (2006) Credit Risk Scorecards.
    Breck et al. (2019) TFDV. MLSys.
    Cohen (1988) Statistical Power Analysis for the Behavioral Sciences.
"""

from __future__ import annotations

import logging
from typing import Literal

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Threshold justification: Siddiqi (2006) Table 3-1
PSI_WARNING_THRESHOLD: float = 0.10
PSI_ALERT_THRESHOLD: float = 0.25
PSI_EPS: float = 1e-10  # floor per Breck et al. (2019)
N_BINS: int = 10  # spec §4 equal-frequency deciles

FeatureType = Literal["continuous", "binary", "categorical"]

# Feature type registry per spec §1 / critique B2
FEATURE_TYPE_MAP: dict[str, FeatureType] = {
    "p0_old_rating": "continuous",
    "p1_old_rating": "continuous",
    "focal_old_rating": "continuous",
    "avg_elo": "continuous",
    "mirror": "binary",
    "p0_is_unrated": "binary",
    "p1_is_unrated": "binary",
    "faction": "categorical",
    "opponent_faction": "categorical",
    "map": "categorical",
    "map_name": "categorical",
    "patch": "categorical",
}


def get_feature_type(feature_name: str) -> FeatureType:
    """Return the feature type for routing PSI computation.

    Args:
        feature_name: Column name from the PSI feature set.

    Returns:
        One of 'continuous', 'binary', 'categorical'.

    Raises:
        KeyError: If feature_name is not in the registry.
    """
    if feature_name not in FEATURE_TYPE_MAP:
        raise KeyError(
            f"Unknown feature {feature_name!r}. Add it to FEATURE_TYPE_MAP."
        )
    return FEATURE_TYPE_MAP[feature_name]


def compute_decile_edges(values: pd.Series, n_bins: int = N_BINS) -> np.ndarray:
    """Compute equal-frequency decile bin edges from reference values.

    Args:
        values: 1-D Series of numeric reference values (no NaN expected).
        n_bins: Number of bins (default 10 per spec §4).

    Returns:
        Array of (n_bins + 1) unique edge values.

    Raises:
        ValueError: If the number of unique values is <= n_bins (degenerate
            histogram; use exact-value routing instead). Per critique B2.
    """
    clean = values.dropna()
    n_unique = int(clean.nunique())
    if n_unique <= n_bins:
        raise ValueError(
            f"compute_decile_edges: only {n_unique} unique values <= n_bins={n_bins}. "
            "Use exact-value frequency histogram for this feature (critique B2)."
        )
    quantiles = np.linspace(0, 1, n_bins + 1)
    edges = np.quantile(clean.to_numpy(dtype=float), quantiles)
    # Ensure strict monotonicity by deduplicating edges
    unique_edges = np.unique(edges)
    if len(unique_edges) < 2:
        raise ValueError(
            f"compute_decile_edges: all {n_bins + 1} quantiles collapsed to one value. "
            "Feature has no variance."
        )
    return unique_edges


def freeze_categorical_reference(values: pd.Series) -> list[str]:
    """Return sorted unique values in the reference period.

    Args:
        values: Categorical column from reference period.

    Returns:
        Sorted list of unique string values (without NaN).
    """
    return sorted(str(v) for v in values.dropna().unique())


def apply_frozen_edges(values: pd.Series, edges: np.ndarray) -> pd.Series:
    """Bin tested values into reference decile bins.

    Values outside [min_edge, max_edge] are assigned to the nearest terminal
    bin (left-clip to bin 0, right-clip to bin n_bins-1).

    Args:
        values: 1-D Series of numeric tested values.
        edges: Edge array from compute_decile_edges().

    Returns:
        Integer-coded bin Series (0-indexed).
    """
    clipped = values.clip(lower=float(edges[0]), upper=float(edges[-1]))
    binned = pd.cut(clipped, bins=edges, labels=False, include_lowest=True)
    return binned.fillna(0).astype(int)


def apply_frozen_categories(values: pd.Series, categories: list[str]) -> pd.Series:
    """Map tested values to reference categories; unseen values -> '__unseen__'.

    Args:
        values: Categorical column from tested period.
        categories: Reference category list from freeze_categorical_reference().

    Returns:
        String Series with '__unseen__' for out-of-vocabulary values.
    """
    cat_set = set(categories)
    return values.map(lambda v: str(v) if str(v) in cat_set else "__unseen__")


def psi(
    ref_hist: np.ndarray,
    tested_hist: np.ndarray,
    eps: float = PSI_EPS,
) -> float:
    """Compute PSI per Siddiqi (2006).

    PSI = sum((p_tested - p_ref) * log(p_tested / p_ref))

    Args:
        ref_hist: Reference bin counts (unnormalised).
        tested_hist: Tested bin counts (unnormalised).
        eps: Floor applied to both distributions before log. Default per
            Breck et al. (2019).

    Returns:
        PSI scalar (non-negative).
    """
    ref_total = float(ref_hist.sum())
    tested_total = float(tested_hist.sum())
    if ref_total == 0 or tested_total == 0:
        logger.warning("psi: empty histogram — returning NaN")
        return float("nan")
    ref_p = np.maximum(ref_hist.astype(float) / ref_total, eps)
    tested_p = np.maximum(tested_hist.astype(float) / tested_total, eps)
    return float(np.sum((tested_p - ref_p) * np.log(tested_p / ref_p)))


def cohen_h(p1: float, p2: float) -> float:
    """Compute Cohen's h effect size for two proportions.

    h = 2 * arcsin(sqrt(p1)) - 2 * arcsin(sqrt(p2))

    Args:
        p1: Proportion in first group (tested).
        p2: Proportion in second group (reference).

    Returns:
        Absolute Cohen's h value.

    References:
        Cohen (1988) §6.2.
    """
    return float(abs(2 * np.arcsin(np.sqrt(p1)) - 2 * np.arcsin(np.sqrt(p2))))


def compute_psi_continuous(
    ref_values: pd.Series,
    test_values: pd.Series,
    feature_name: str,
) -> dict[str, object]:
    """Compute PSI for a continuous feature using frozen decile edges.

    Args:
        ref_values: Reference period values.
        test_values: Tested quarter values.
        feature_name: Column name (for logging).

    Returns:
        Dict with keys: psi_value, reference_bin_count, tested_bin_count,
        unseen_bin_count, notes, metric_name.
    """
    ref_clean = ref_values.dropna()
    test_clean = test_values.dropna()
    try:
        edges = compute_decile_edges(ref_clean)
    except ValueError as exc:
        logger.warning("Feature %s: %s — fallback to categorical", feature_name, exc)
        return compute_psi_categorical(ref_clean.astype(str), test_clean.astype(str), feature_name)

    ref_binned = apply_frozen_edges(ref_clean, edges)
    test_binned = apply_frozen_edges(test_clean, edges)

    n_bins = len(edges) - 1
    ref_hist = np.bincount(ref_binned, minlength=n_bins)
    test_hist = np.bincount(test_binned, minlength=n_bins)

    psi_value = psi(ref_hist, test_hist)
    return {
        "psi_value": psi_value,
        "reference_bin_count": int(len(ref_clean)),
        "tested_bin_count": int(len(test_clean)),
        "unseen_bin_count": 0,
        "notes": f"continuous decile PSI n_bins={n_bins}",
        "metric_name": "psi",
    }


def compute_psi_binary(
    ref_values: pd.Series,
    test_values: pd.Series,
    feature_name: str,
) -> dict[str, object]:
    """Compute Cohen's h for a binary feature (2-level boolean/int).

    Per critique B2: binary features use exact-value frequency histogram +
    Cohen's h. Not PSI (degenerate under N=10 equal-frequency).

    Args:
        ref_values: Reference period values (0/1 or bool).
        test_values: Tested quarter values.
        feature_name: Column name (for logging).

    Returns:
        Dict with keys: psi_value (=cohen_h), reference_bin_count,
        tested_bin_count, unseen_bin_count, notes, metric_name.
    """
    ref_clean = ref_values.dropna().astype(float)
    test_clean = test_values.dropna().astype(float)

    ref_rate = float(ref_clean.mean()) if len(ref_clean) > 0 else float("nan")
    test_rate = float(test_clean.mean()) if len(test_clean) > 0 else float("nan")

    if np.isnan(ref_rate) or np.isnan(test_rate):
        h = float("nan")
    else:
        h = cohen_h(test_rate, ref_rate)

    return {
        "psi_value": h,
        "reference_bin_count": int(len(ref_clean)),
        "tested_bin_count": int(len(test_clean)),
        "unseen_bin_count": 0,
        "notes": (
            f"binary exact-value Cohen h; ref_rate={ref_rate:.4f} "
            f"test_rate={test_rate:.4f} (spec §3 metric_name=cohen_h)"
        ),
        "metric_name": "cohen_h",
    }


def compute_psi_categorical(
    ref_values: pd.Series,
    test_values: pd.Series,
    feature_name: str,
) -> dict[str, object]:
    """Compute categorical PSI with __unseen__ bin.

    Args:
        ref_values: Reference period categorical values.
        test_values: Tested quarter categorical values.
        feature_name: Column name (for logging).

    Returns:
        Dict with keys: psi_value, reference_bin_count, tested_bin_count,
        unseen_bin_count, notes, metric_name.
    """
    categories = freeze_categorical_reference(ref_values)
    ref_mapped = apply_frozen_categories(ref_values.dropna().astype(str), categories)
    test_mapped = apply_frozen_categories(test_values.dropna().astype(str), categories)

    all_cats = categories + ["__unseen__"]
    ref_hist = np.array([int((ref_mapped == c).sum()) for c in all_cats])
    test_hist = np.array([int((test_mapped == c).sum()) for c in all_cats])

    unseen_count = int(test_hist[-1])
    psi_value = psi(ref_hist, test_hist)

    return {
        "psi_value": psi_value,
        "reference_bin_count": int(len(ref_mapped)),
        "tested_bin_count": int(len(test_mapped)),
        "unseen_bin_count": unseen_count,
        "notes": (
            f"categorical PSI with __unseen__ bin; "
            f"n_ref_cats={len(categories)}; unseen_tested={unseen_count}"
        ),
        "metric_name": "psi",
    }


def compute_feature_psi(
    ref_values: pd.Series,
    test_values: pd.Series,
    feature_name: str,
) -> dict[str, object]:
    """Route PSI computation by feature type.

    Per critique B2 routing:
    - continuous -> decile PSI
    - binary -> Cohen h
    - categorical -> categorical PSI with __unseen__

    Args:
        ref_values: Reference period Series.
        test_values: Tested quarter Series.
        feature_name: Feature name for type lookup.

    Returns:
        Result dict from the appropriate sub-function.

    Raises:
        KeyError: If feature_name not in registry.
    """
    ftype = get_feature_type(feature_name)
    if ftype == "continuous":
        return compute_psi_continuous(ref_values, test_values, feature_name)
    elif ftype == "binary":
        return compute_psi_binary(ref_values, test_values, feature_name)
    else:
        return compute_psi_categorical(ref_values, test_values, feature_name)
