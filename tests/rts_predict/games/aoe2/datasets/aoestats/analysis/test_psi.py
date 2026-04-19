"""Tests for aoestats PSI analysis module.

Covers: empty DF, single row, NaN handling, unseen categorical,
        B2 critique ValueError on boolean feature,
        type routing for all feature types.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from rts_predict.games.aoe2.datasets.aoestats.analysis.psi import (
    apply_frozen_categories,
    apply_frozen_edges,
    cohen_h,
    compute_decile_edges,
    compute_feature_psi,
    compute_psi_binary,
    compute_psi_categorical,
    compute_psi_continuous,
    freeze_categorical_reference,
    get_feature_type,
    psi,
)


class TestGetFeatureType:
    def test_continuous_features(self) -> None:
        assert get_feature_type("p0_old_rating") == "continuous"
        assert get_feature_type("avg_elo") == "continuous"

    def test_binary_features(self) -> None:
        assert get_feature_type("mirror") == "binary"
        assert get_feature_type("p0_is_unrated") == "binary"

    def test_categorical_features(self) -> None:
        assert get_feature_type("faction") == "categorical"
        assert get_feature_type("map") == "categorical"

    def test_unknown_feature_raises(self) -> None:
        with pytest.raises(KeyError):
            get_feature_type("unknown_column")


class TestComputeDecileEdges:
    def test_returns_edges_for_large_series(self) -> None:
        values = pd.Series(np.random.default_rng(0).normal(1000, 100, 1000))
        edges = compute_decile_edges(values)
        assert len(edges) >= 2
        assert edges[0] <= edges[-1]

    def test_raises_on_boolean_series(self) -> None:
        # Boolean has only 2 unique values — should raise B2 ValueError
        values = pd.Series([True, False, True, False, True] * 100)
        with pytest.raises(ValueError, match="unique values <="):
            compute_decile_edges(values, n_bins=10)

    def test_raises_on_degenerate_constant(self) -> None:
        values = pd.Series([1.0] * 100)
        with pytest.raises(ValueError):
            compute_decile_edges(values)

    def test_handles_nan_by_ignoring(self) -> None:
        values = pd.Series([float("nan")] * 5 + list(range(100)))
        edges = compute_decile_edges(values)
        assert len(edges) >= 2


class TestApplyFrozenEdges:
    def test_values_within_range(self) -> None:
        edges = np.array([0.0, 1.0, 2.0, 3.0])
        values = pd.Series([0.5, 1.5, 2.5])
        result = apply_frozen_edges(values, edges)
        assert result.tolist() == [0, 1, 2]

    def test_values_clipped_outside_range(self) -> None:
        edges = np.array([1.0, 2.0, 3.0])
        values = pd.Series([0.0, 100.0])  # outside [1, 3]
        result = apply_frozen_edges(values, edges)
        # Both should map to a valid bin (clipped)
        assert all(0 <= v < len(edges) - 1 for v in result)


class TestFreezeCategoricalReference:
    def test_returns_sorted_unique(self) -> None:
        values = pd.Series(["b", "a", "c", "a", "b"])
        cats = freeze_categorical_reference(values)
        assert cats == ["a", "b", "c"]

    def test_ignores_nan(self) -> None:
        values = pd.Series(["a", None, "b"])
        cats = freeze_categorical_reference(values)
        assert "nan" not in cats
        assert len(cats) == 2


class TestApplyFrozenCategories:
    def test_known_values_pass_through(self) -> None:
        cats = ["a", "b", "c"]
        values = pd.Series(["a", "b", "c"])
        result = apply_frozen_categories(values, cats)
        assert result.tolist() == ["a", "b", "c"]

    def test_unseen_mapped_to_sentinel(self) -> None:
        cats = ["a", "b"]
        values = pd.Series(["a", "z", "x"])
        result = apply_frozen_categories(values, cats)
        assert result.tolist() == ["a", "__unseen__", "__unseen__"]


class TestPsi:
    def test_identical_distributions_returns_zero(self) -> None:
        hist = np.array([10, 20, 30, 40])
        result = psi(hist, hist)
        assert abs(result) < 1e-6

    def test_empty_reference_returns_nan(self) -> None:
        result = psi(np.array([0, 0, 0]), np.array([1, 2, 3]))
        assert np.isnan(result)

    def test_empty_tested_returns_nan(self) -> None:
        result = psi(np.array([1, 2, 3]), np.array([0, 0, 0]))
        assert np.isnan(result)

    def test_psi_non_negative(self) -> None:
        rng = np.random.default_rng(42)
        ref = rng.integers(1, 100, 10)
        test = rng.integers(1, 100, 10)
        result = psi(ref, test)
        assert result >= 0 or np.isnan(result)


class TestCohenH:
    def test_identical_proportions_returns_zero(self) -> None:
        assert abs(cohen_h(0.5, 0.5)) < 1e-10

    def test_non_negative(self) -> None:
        result = cohen_h(0.3, 0.7)
        assert result >= 0

    def test_symmetric(self) -> None:
        assert abs(cohen_h(0.3, 0.7) - cohen_h(0.7, 0.3)) < 1e-10


class TestComputePsiBinary:
    def test_returns_cohen_h_metric(self) -> None:
        ref = pd.Series([0, 1, 0, 1, 0] * 100)
        test = pd.Series([0, 0, 0, 1, 0] * 100)
        result = compute_psi_binary(ref, test, "mirror")
        assert result["metric_name"] == "cohen_h"
        assert isinstance(result["psi_value"], float)

    def test_empty_series_returns_nan(self) -> None:
        empty: pd.Series = pd.Series([], dtype=float)
        result = compute_psi_binary(empty, empty, "mirror")
        assert np.isnan(result["psi_value"])


class TestComputePsiCategorical:
    def test_counts_unseen_bin(self) -> None:
        ref = pd.Series(["a", "b", "c"] * 100)
        test = pd.Series(["a", "b", "d"] * 100)  # "d" is unseen
        result = compute_psi_categorical(ref, test, "faction")
        assert result["unseen_bin_count"] > 0
        assert result["metric_name"] == "psi"

    def test_identical_distribution_near_zero(self) -> None:
        ref = pd.Series(["a", "b", "c"] * 100)
        result = compute_psi_categorical(ref, ref.copy(), "faction")
        assert abs(result["psi_value"]) < 0.01


class TestComputePsiContinuous:
    def test_identical_distribution_near_zero(self) -> None:
        rng = np.random.default_rng(0)
        values = pd.Series(rng.normal(1000, 100, 1000))
        result = compute_psi_continuous(values, values.copy(), "avg_elo")
        assert result["metric_name"] == "psi"
        assert abs(result["psi_value"]) < 0.05

    def test_fallback_for_binary_input(self) -> None:
        # Boolean column should fall back to categorical
        ref = pd.Series([0, 1] * 500)
        test = pd.Series([0, 0] * 500)
        result = compute_psi_continuous(ref, test, "p0_is_unrated")
        # Should not crash; falls back gracefully
        assert "psi_value" in result


class TestComputeFeaturePsi:
    def test_routes_continuous(self) -> None:
        rng = np.random.default_rng(1)
        ref = pd.Series(rng.normal(1500, 200, 1000))
        test = pd.Series(rng.normal(1600, 200, 1000))
        result = compute_feature_psi(ref, test, "avg_elo")
        assert result["metric_name"] == "psi"

    def test_routes_binary(self) -> None:
        ref = pd.Series([True, False] * 500)
        test = pd.Series([True, True] * 500)
        result = compute_feature_psi(ref, test, "mirror")
        assert result["metric_name"] == "cohen_h"

    def test_routes_categorical(self) -> None:
        ref = pd.Series(["Franks", "Britons", "Chinese"] * 100)
        test = pd.Series(["Franks", "Britons", "Vikings"] * 100)
        result = compute_feature_psi(ref, test, "faction")
        assert result["metric_name"] == "psi"

    def test_unknown_feature_raises(self) -> None:
        with pytest.raises(KeyError):
            compute_feature_psi(pd.Series([1, 2]), pd.Series([1, 2]), "bad_col")
