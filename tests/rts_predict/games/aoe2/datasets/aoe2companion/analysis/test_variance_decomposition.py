"""Tests for aoe2companion variance decomposition / ICC helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd

from rts_predict.games.aoe2.datasets.aoe2companion.analysis.variance_decomposition import (
    compute_icc_anova,
    compute_icc_anova_fast,
    compute_icc_lmm,
    fit_random_intercept_lmm,
    stratified_reservoir_sample,
)


class TestComputeIccAnovaFast:
    def test_perfect_within_group_consistency(self) -> None:
        groups = ["A"] * 50 + ["B"] * 50
        values = [1.0] * 50 + [0.0] * 50
        df = pd.DataFrame({"player_id": groups, "won": values})
        icc = compute_icc_anova_fast(df, "won", "player_id")
        assert 0 <= icc <= 1
        assert icc > 0.9  # nearly all variance is between groups

    def test_no_between_group_variance(self) -> None:
        groups = ["A"] * 50 + ["B"] * 50
        values = [0.5, 0.5] * 50
        df = pd.DataFrame({"player_id": groups, "won": values})
        icc = compute_icc_anova_fast(df, "won", "player_id")
        assert icc <= 0.05  # no between-group structure

    def test_single_group_returns_nan(self) -> None:
        df = pd.DataFrame({"player_id": ["A"] * 10, "won": [0.5] * 10})
        icc = compute_icc_anova_fast(df, "won", "player_id")
        assert np.isnan(icc)

    def test_empty_dataframe_returns_nan(self) -> None:
        df = pd.DataFrame({"player_id": [], "won": []})
        icc = compute_icc_anova_fast(df, "won", "player_id")
        assert np.isnan(icc)

    def test_icc_in_unit_interval_random_binary(self) -> None:
        rng = np.random.default_rng(0)
        n_groups = 50
        groups = np.repeat(np.arange(n_groups), 10)
        values = rng.integers(0, 2, size=n_groups * 10).astype(float)
        df = pd.DataFrame({"player_id": groups, "won": values})
        icc = compute_icc_anova_fast(df, "won", "player_id")
        assert 0 <= icc <= 1


class TestComputeIccAnovaTopLevel:
    def test_no_bootstrap_returns_nan_ci(self) -> None:
        df = pd.DataFrame({
            "player_id": np.repeat([1, 2, 3, 4], 5),
            "won": [1.0, 1.0, 0.0, 0.0] * 5,
        })
        icc, ci_lo, ci_hi = compute_icc_anova(df, "won", "player_id", n_bootstrap=0)
        assert not np.isnan(icc)
        assert np.isnan(ci_lo)
        assert np.isnan(ci_hi)

    def test_bootstrap_returns_finite_ci_when_requested(self) -> None:
        rng = np.random.default_rng(0)
        groups = np.repeat(np.arange(20), 10)
        values = rng.integers(0, 2, size=200).astype(float)
        df = pd.DataFrame({"player_id": groups, "won": values})
        icc, ci_lo, ci_hi = compute_icc_anova(df, "won", "player_id", n_bootstrap=50)
        assert not np.isnan(icc)
        assert np.isfinite(ci_lo)
        assert np.isfinite(ci_hi)
        assert ci_lo <= icc + 1e-9
        assert ci_hi >= icc - 1e-9


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

    def test_stratified_sample_covers_all_deciles(self) -> None:
        rng = np.random.default_rng(0)
        n_groups = 200
        rows_per_group = rng.integers(1, 20, size=n_groups)
        group_ids = np.concatenate([np.full(r, i) for i, r in enumerate(rows_per_group)])
        df = pd.DataFrame({
            "player_id": group_ids,
            "won": rng.integers(0, 2, size=len(group_ids)).astype(float),
            "n_matches_in_ref": np.concatenate([np.full(r, r) for r in rows_per_group]),
        })
        sampled = stratified_reservoir_sample(
            df, "player_id", n_players=50, stratify_by="n_matches_in_ref"
        )
        assert sampled["player_id"].nunique() <= 50
        assert sampled["player_id"].nunique() >= 10

    def test_reproducible_with_seed(self) -> None:
        df = pd.DataFrame({
            "player_id": np.repeat(np.arange(100), 3),
            "won": [0.0, 1.0] * 150,
        })
        s1 = stratified_reservoir_sample(df, "player_id", n_players=20, seed=123)
        s2 = stratified_reservoir_sample(df, "player_id", n_players=20, seed=123)
        assert set(s1["player_id"].unique()) == set(s2["player_id"].unique())

    def test_stratify_single_n_matches_value_falls_through(self) -> None:
        # All players have the same n_matches → n_unique < 2 → uniform fallback.
        df = pd.DataFrame({
            "player_id": np.repeat(np.arange(20), 5),
            "won": [0.0, 1.0] * 50,
            "n_matches_in_ref": [5] * 100,
        })
        sampled = stratified_reservoir_sample(
            df, "player_id", n_players=10, stratify_by="n_matches_in_ref"
        )
        assert sampled["player_id"].nunique() == 10

    def test_stratify_topup_branch(self) -> None:
        # Configure n_players so per_decile × deciles < n_players → top-up branch
        # at lines 302-305 is exercised.
        rng = np.random.default_rng(7)
        n_groups = 100
        rows_per_group = rng.integers(5, 30, size=n_groups)
        group_ids = np.concatenate([np.full(r, i) for i, r in enumerate(rows_per_group)])
        df = pd.DataFrame({
            "player_id": group_ids,
            "won": rng.integers(0, 2, size=len(group_ids)).astype(float),
            "n_matches_in_ref": np.concatenate([np.full(r, r) for r in rows_per_group]),
        })
        # Request 55 players from 100 — top-up is required because
        # per_decile = 55 // 10 = 5, so 10 × 5 = 50 covered; 5 more via top-up.
        sampled = stratified_reservoir_sample(
            df, "player_id", n_players=55, stratify_by="n_matches_in_ref", seed=1
        )
        assert 50 <= sampled["player_id"].nunique() <= 55


class TestBootstrapCIFallback:
    def test_zero_bootstrap_returns_point_only(self) -> None:
        df = pd.DataFrame({
            "player_id": np.repeat([1, 2, 3, 4], 5),
            "won": [1.0, 1.0, 0.0, 0.0] * 5,
        })
        icc, lo, hi = compute_icc_anova(df, "won", "player_id", n_bootstrap=0)
        assert not np.isnan(icc) and np.isnan(lo) and np.isnan(hi)

    def test_bootstrap_too_few_successful_returns_nan_ci(self) -> None:
        # Single-group degenerate case: every bootstrap fails the < 2 groups
        # check inside compute_icc_anova_fast → CI fallback at line 244.
        df = pd.DataFrame({"player_id": [1] * 10, "won": [0.5] * 10})
        icc, lo, hi = compute_icc_anova(df, "won", "player_id", n_bootstrap=20)
        assert np.isnan(icc) and np.isnan(lo) and np.isnan(hi)


class TestFitRandomInterceptLMM:
    def test_fit_returns_result_with_expected_attrs(self) -> None:
        rng = np.random.default_rng(0)
        n_groups = 30
        df = pd.DataFrame({
            "won": rng.integers(0, 2, n_groups * 10).astype(float),
            "player_id": np.repeat(np.arange(n_groups), 10),
        })
        result = fit_random_intercept_lmm(df, "won", "player_id", max_iter=50)
        assert hasattr(result, "cov_re")
        assert hasattr(result, "scale")
        assert result.model.n_groups == n_groups
        assert result.nobs == n_groups * 10


class TestComputeIccLMM:
    def test_icc_in_unit_interval_from_real_fit(self) -> None:
        rng = np.random.default_rng(0)
        # Synthetic data with mild between-group structure
        n_groups = 40
        group_means = rng.normal(0.5, 0.1, size=n_groups)
        rows = []
        for g, mu in enumerate(group_means):
            for _ in range(10):
                rows.append((g, float(rng.binomial(1, np.clip(mu, 0.01, 0.99)))))
        df = pd.DataFrame(rows, columns=["player_id", "won"])
        result = fit_random_intercept_lmm(df, "won", "player_id", max_iter=50)
        icc, ci_lo, ci_hi = compute_icc_lmm(result)
        assert 0 <= icc <= 1
        assert 0 <= ci_lo <= icc + 1e-9
        assert icc - 1e-9 <= ci_hi <= 1

    def test_icc_zero_total_variance_returns_nan(self) -> None:
        class FakeResult:
            class model:  # noqa: D106 — stub
                n_groups = 10
            cov_re = pd.DataFrame([[0.0]])
            scale = 0.0
            nobs = 100

        icc, ci_lo, ci_hi = compute_icc_lmm(FakeResult())
        assert np.isnan(icc) and np.isnan(ci_lo) and np.isnan(ci_hi)
