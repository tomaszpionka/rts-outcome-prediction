"""Tests for aoestats variance decomposition / ICC module."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from rts_predict.games.aoe2.datasets.aoestats.analysis.variance_decomposition import (
    _bootstrap_icc_anova_ci,
    _icc_anova_point,
    compute_icc_anova,
    compute_icc_lmm,
    fit_random_intercept_lmm,
    stratified_reservoir_sample,
)


class TestComputeIccAnova:
    def test_perfect_within_group_consistency(self) -> None:
        # Each group has the same outcome value -> high ICC
        groups = ["A"] * 50 + ["B"] * 50
        values = [1.0] * 50 + [0.0] * 50
        df = pd.DataFrame({"player_id": groups, "won": values})
        icc, ci_lo, ci_hi = compute_icc_anova(df, "won", "player_id")
        assert 0 <= icc <= 1
        assert ci_lo <= icc <= ci_hi or np.isnan(ci_lo)

    def test_single_group_returns_nan(self) -> None:
        df = pd.DataFrame({"player_id": ["A"] * 10, "won": [0.5] * 10})
        icc, _, _ = compute_icc_anova(df, "won", "player_id")
        assert np.isnan(icc)

    def test_icc_in_unit_interval(self) -> None:
        rng = np.random.default_rng(0)
        n_groups = 50
        groups = np.repeat(np.arange(n_groups), 10)
        values = rng.integers(0, 2, size=n_groups * 10).astype(float)
        df = pd.DataFrame({"player_id": groups, "won": values})
        icc, ci_lo, ci_hi = compute_icc_anova(df, "won", "player_id")
        assert 0 <= icc <= 1
        assert ci_lo <= ci_hi


class TestFitRandomInterceptLmm:
    def test_requires_statsmodels(self) -> None:
        # Verify the function exists and has correct signature
        import inspect
        sig = inspect.signature(fit_random_intercept_lmm)
        assert "df" in sig.parameters
        assert "target" in sig.parameters
        assert "group" in sig.parameters

    def test_raises_import_error_if_statsmodels_missing(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import builtins
        real_import = builtins.__import__

        def mock_import(name: str, *args: object, **kwargs: object) -> object:
            if name == "statsmodels.formula.api":
                raise ImportError("mocked missing statsmodels")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)
        df = pd.DataFrame({"player_id": ["A"] * 5, "won": [1.0] * 5})
        with pytest.raises(ImportError, match="statsmodels required"):
            fit_random_intercept_lmm(df, "won", "player_id")


class TestComputeIccLmm:
    def test_returns_tuple_of_three_floats(self) -> None:
        from unittest.mock import MagicMock

        mock_result = MagicMock()
        mock_result.cov_re = pd.DataFrame([[0.1]], columns=[0])
        mock_result.scale = 0.25
        mock_result.ngroups = 100
        mock_result.nobs = 1000

        icc, ci_lo, ci_hi = compute_icc_lmm(mock_result)
        assert 0 <= icc <= 1
        assert 0 <= ci_lo <= icc
        assert icc <= ci_hi <= 1

    def test_zero_total_variance_returns_nan(self) -> None:
        from unittest.mock import MagicMock

        mock_result = MagicMock()
        mock_result.cov_re = pd.DataFrame([[0.0]], columns=[0])
        mock_result.scale = 0.0
        mock_result.ngroups = 100
        mock_result.nobs = 1000

        icc, ci_lo, ci_hi = compute_icc_lmm(mock_result)
        assert np.isnan(icc)
        assert np.isnan(ci_lo)
        assert np.isnan(ci_hi)


class TestIccAnovaPoint:
    def test_zero_denominator_returns_zero(self) -> None:
        # All groups have the same mean as the grand mean -> MSB = 0
        groups = np.array(["A", "A", "B", "B"])
        values = np.array([0.5, 0.5, 0.5, 0.5])
        result = _icc_anova_point(groups, values)
        assert result == 0.0

    def test_single_group_returns_nan(self) -> None:
        groups = np.array(["A", "A", "A"])
        values = np.array([1.0, 0.0, 1.0])
        result = _icc_anova_point(groups, values)
        assert np.isnan(result)

    def test_result_clipped_to_unit_interval(self) -> None:
        rng = np.random.default_rng(0)
        groups = np.array(["A"] * 10 + ["B"] * 10 + ["C"] * 10)
        values = rng.uniform(0, 1, 30)
        result = _icc_anova_point(groups, values)
        assert 0.0 <= result <= 1.0


class TestBootstrapIccAnovaCi:
    def test_returns_nan_tuple_when_too_few_bootstrap_icc(self) -> None:
        # Single group -> all bootstrap samples will yield NaN -> fewer than 10 valid
        df = pd.DataFrame({"player_id": ["A"] * 10, "won": [0.5] * 10})
        ci_lo, ci_hi = _bootstrap_icc_anova_ci(df, "won", "player_id", n_bootstrap=5)
        assert np.isnan(ci_lo)
        assert np.isnan(ci_hi)

    def test_ci_lo_le_ci_hi(self) -> None:
        rng = np.random.default_rng(0)
        n_groups = 20
        df = pd.DataFrame({
            "player_id": np.repeat(np.arange(n_groups), 10),
            "won": rng.integers(0, 2, n_groups * 10).astype(float),
        })
        ci_lo, ci_hi = _bootstrap_icc_anova_ci(df, "won", "player_id", n_bootstrap=50)
        assert ci_lo <= ci_hi


class TestStratifiedReservoirSample:
    def test_returns_at_most_n_players(self) -> None:
        rng = np.random.default_rng(42)
        n_groups = 200
        df = pd.DataFrame({
            "player_id": np.repeat(np.arange(n_groups), 5),
            "won": rng.integers(0, 2, n_groups * 5).astype(float),
        })
        sampled = stratified_reservoir_sample(df, "player_id", n_players=50)
        assert sampled["player_id"].nunique() <= 50

    def test_returns_all_if_fewer_than_n(self) -> None:
        df = pd.DataFrame({
            "player_id": [1, 1, 2, 2, 3, 3],
            "won": [1.0, 0.0, 1.0, 1.0, 0.0, 0.0],
        })
        sampled = stratified_reservoir_sample(df, "player_id", n_players=100)
        assert sampled["player_id"].nunique() == 3

    def test_stratify_by_column_works(self) -> None:
        rng = np.random.default_rng(0)
        n_groups = 100
        df = pd.DataFrame({
            "player_id": np.repeat(np.arange(n_groups), 10),
            "won": rng.integers(0, 2, n_groups * 10).astype(float),
            "n_matches_in_ref": np.repeat(rng.integers(5, 50, n_groups), 10),
        })
        sampled = stratified_reservoir_sample(
            df, "player_id", n_players=30, stratify_by="n_matches_in_ref"
        )
        assert sampled["player_id"].nunique() <= 30

    def test_uniform_sample_when_no_stratify_by(self) -> None:
        rng = np.random.default_rng(0)
        n_groups = 50
        df = pd.DataFrame({
            "player_id": np.repeat(np.arange(n_groups), 5),
            "won": rng.integers(0, 2, n_groups * 5).astype(float),
        })
        sampled = stratified_reservoir_sample(df, "player_id", n_players=20, stratify_by=None)
        assert sampled["player_id"].nunique() <= 20
