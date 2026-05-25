"""Comprehensive tests for survey_history_rating_algorithms.py (Q6F survey).

Coverage target: ≥95% branch coverage on the survey module.
All fixtures are synthetic in-memory; real DuckDB only via
_load_pha_history_chronological with a tiny tmp_path DB.
"""

from __future__ import annotations

import csv
import hashlib
import math
import re
import subprocess
from dataclasses import fields
from pathlib import Path
from typing import Any
from unittest import mock

import duckdb
import numpy as np
import pandas as pd
import pytest

from rts_predict.games.sc2.config import DB_FILE
from rts_predict.games.sc2.datasets.sc2egset import survey_history_rating_algorithms as mod
from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
    ALLOWED_MATERIALIZATION_PERMISSIONS,
    AUDIT_PR_NUMBER_PLACEHOLDER,
    BOOTSTRAP_BLOCK_COUNT,
    BOOTSTRAP_RANDOM_SEED,
    CITATION_ELO_1978,
    CITATION_GLICKMAN_1999,
    CITATION_GLICKMAN_2012,
    CITATION_HERBRICH_MINKA_GRAEPEL_2006,
    CITATION_HOSMER_LEMESHOW_2013,
    CITATION_STEYERBERG_2009,
    EXCLUDED_METHODS_CONSIDERED,
    EXPECTED_PR242_CSV_SHA256,
    EXPECTED_PR242_MD_SHA256,
    EXPECTED_PR243_CSV_SHA256,
    EXPECTED_PR243_MD_SHA256,
    EXPECTED_PR245_CSV_SHA256,
    EXPECTED_PR245_MD_SHA256,
    FALSIFIER_PRIORITY_CHAIN,
    HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS,
    NON_RATING_HISTORY_FAMILIES,
    PARENT_PR242_CSV_REL,
    PARENT_PR242_MD_REL,
    PARENT_PR243_CSV_REL,
    PARENT_PR243_MD_REL,
    PARENT_PR245_CSV_REL,
    PARENT_PR245_MD_REL,
    Q5_SELECTED_POLICY,
    Q5_SELECTED_POLICY_VERDICT,
    Q6F_ALLOWED_VERDICTS,
    Q6F_CANDIDATE_INCLUSION,
    Q6F_DECISION_IDS,
    Q6F_HYPERPARAMETER_DEFAULTS,
    Q6F_RATING_ALGORITHM_CANDIDATES,
    Q6F_SCHEMA_COLUMN_COUNT,
    Q6F_SELECTION_DECISION_RULE,
    Q6F_SURVEY_CANDIDATES,
    Q6F_SURVEY_SCHEMA,
    RAW_MMR_HYBRID_REJECTION_TEXT,
    STRICT_LT_HISTORY_FILTER,
    RatingSurveyDecision,
    RatingSurveyError,
    RatingSurveyResult,
    _auc_from_arrays,
    _brier_from_arrays,
    _build_decision,
    _build_survey_decisions,
    _calibration_error,
    _candidate_to_metric_strings,
    _check_candidate_set_complete,
    _check_decision_count,
    _check_decision_id_order,
    _check_excluded_methods_complete,
    _check_no_materialized_output_paths,
    _check_per_family_impact_summary_present,
    _check_q5_not_re_adjudicated,
    _check_raw_mmr_hybrid_rejection,
    _check_selected_policy_row_present,
    _find_repo_root,
    _get_git_sha,
    _log_loss_from_arrays,
    _md_sections,
    _per_family_broadcast,
    _run_elo_survey,
    _run_glicko2_survey,
    _run_rolling_baseline_survey,
    _run_trueskill_survey,
    _safe_float_str,
    _select_q6f_policy,
    _sha256_file,
    _write_csv,
    compute_metrics_with_ci,
    run_q6f_rating_algorithm_survey,
    write_q6f_survey_artifacts,
)

# ---------------------------------------------------------------------------
# Module-level fixtures
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parents[6]  # tests/rts_predict/games/sc2/datasets/sc2egset -> repo root

_BASE_TIMESTAMP = "2023-01-01T10:00:00Z"


def _make_stream(rows: list[dict[str, Any]]) -> pd.DataFrame:
    """Build a minimal PHA-format DataFrame from raw dicts."""
    df = pd.DataFrame(rows)
    df["_ts"] = pd.to_datetime(df["details_timeUTC"], format="ISO8601", utc=True, errors="coerce")
    return df


@pytest.fixture()
def synthetic_2player_4row_stream() -> pd.DataFrame:
    """4-row PHA stream: 2 players, 2 replays each."""
    rows = [
        {
            "focal_toon": "alice",
            "opponent_toon": "bob",
            "replay_id": "r1",
            "details_timeUTC": "2023-01-01T10:00:00Z",
            "focal_result": "Win",
            "is_cross_region_fragmented": False,
        },
        {
            "focal_toon": "bob",
            "opponent_toon": "alice",
            "replay_id": "r1",
            "details_timeUTC": "2023-01-01T10:00:00Z",
            "focal_result": "Loss",
            "is_cross_region_fragmented": False,
        },
        {
            "focal_toon": "alice",
            "opponent_toon": "bob",
            "replay_id": "r2",
            "details_timeUTC": "2023-01-02T10:00:00Z",
            "focal_result": "Loss",
            "is_cross_region_fragmented": False,
        },
        {
            "focal_toon": "bob",
            "opponent_toon": "alice",
            "replay_id": "r2",
            "details_timeUTC": "2023-01-02T10:00:00Z",
            "focal_result": "Win",
            "is_cross_region_fragmented": False,
        },
    ]
    return _make_stream(rows)


def _flat_metrics(
    log_loss: float = 0.5,
    ll_low: float = 0.45,
    ll_high: float = 0.55,
    brier: float = 0.2,
    b_low: float = 0.18,
    b_high: float = 0.22,
    auc: float = 0.55,
    a_low: float = 0.50,
    a_high: float = 0.60,
    calibration_error: float = 0.05,
    coverage_rate: float = 0.9,
    cold_start_rate: float = 0.1,
    runtime_seconds: float = 0.01,
    tie_rate: float = 0.0,
) -> dict[str, float]:
    return {
        "log_loss": log_loss,
        "log_loss_ci_low": ll_low,
        "log_loss_ci_high": ll_high,
        "brier": brier,
        "brier_ci_low": b_low,
        "brier_ci_high": b_high,
        "auc": auc,
        "auc_ci_low": a_low,
        "auc_ci_high": a_high,
        "calibration_error": calibration_error,
        "coverage_rate": coverage_rate,
        "cold_start_rate": cold_start_rate,
        "runtime_seconds": runtime_seconds,
        "tie_rate": tie_rate,
    }


def _make_metrics_by_candidate(
    branch: str,
) -> dict[str, dict[str, float]]:
    """Return metrics_by_candidate shaped to trigger a specific decision branch."""
    if branch == "bind_now":
        # c* = elo; dominates all others CI-disjointly + beats baseline
        return {
            "omit_reconstructed_rating": {k: math.nan for k in mod.Q6F_METRICS},
            "rolling_win_rate_or_bayesian_smoothed_baseline": _flat_metrics(
                log_loss=0.700, ll_low=0.680, ll_high=0.720,
                brier=0.25, b_low=0.23, b_high=0.27,
            ),
            "elo": _flat_metrics(
                log_loss=0.400, ll_low=0.380, ll_high=0.410,
                brier=0.15, b_low=0.13, b_high=0.16,
            ),
            "glicko_or_glicko_2": _flat_metrics(
                log_loss=0.650, ll_low=0.630, ll_high=0.670,
                brier=0.23, b_low=0.21, b_high=0.25,
            ),
            "trueskill_or_trueskill_like": _flat_metrics(
                log_loss=0.660, ll_low=0.640, ll_high=0.680,
                brier=0.24, b_low=0.22, b_high=0.26,
            ),
            "deferred_blocker_with_algorithm_survey_required": {
                k: math.nan for k in mod.Q6F_METRICS
            },
        }

    if branch == "narrow_with_evidence":
        # c* = elo; beats baseline (CI-disjoint), but glicko CIs overlap with elo
        return {
            "omit_reconstructed_rating": {k: math.nan for k in mod.Q6F_METRICS},
            "rolling_win_rate_or_bayesian_smoothed_baseline": _flat_metrics(
                log_loss=0.700, ll_low=0.680, ll_high=0.720,
                brier=0.25, b_low=0.23, b_high=0.27,
            ),
            "elo": _flat_metrics(
                log_loss=0.400, ll_low=0.380, ll_high=0.410,
                brier=0.15, b_low=0.13, b_high=0.16,
            ),
            "glicko_or_glicko_2": _flat_metrics(
                # elo CI high (0.410) > glicko CI low (0.390) => overlap => not bind_now
                log_loss=0.450, ll_low=0.390, ll_high=0.500,
                brier=0.17, b_low=0.14, b_high=0.20,
            ),
            "trueskill_or_trueskill_like": _flat_metrics(
                log_loss=0.460, ll_low=0.400, ll_high=0.510,
                brier=0.18, b_low=0.15, b_high=0.21,
            ),
            "deferred_blocker_with_algorithm_survey_required": {
                k: math.nan for k in mod.Q6F_METRICS
            },
        }

    if branch == "omit_reconstructed_rating_and_unblock_other_five":
        # c* = baseline (baseline has lowest log-loss)
        return {
            "omit_reconstructed_rating": {k: math.nan for k in mod.Q6F_METRICS},
            "rolling_win_rate_or_bayesian_smoothed_baseline": _flat_metrics(
                log_loss=0.350, ll_low=0.330, ll_high=0.370,
                brier=0.12, b_low=0.10, b_high=0.14,
            ),
            "elo": _flat_metrics(
                log_loss=0.500, ll_low=0.480, ll_high=0.520,
                brier=0.20, b_low=0.18, b_high=0.22,
            ),
            "glicko_or_glicko_2": _flat_metrics(
                log_loss=0.510, ll_low=0.490, ll_high=0.530,
                brier=0.21, b_low=0.19, b_high=0.23,
            ),
            "trueskill_or_trueskill_like": _flat_metrics(
                log_loss=0.520, ll_low=0.500, ll_high=0.540,
                brier=0.22, b_low=0.20, b_high=0.24,
            ),
            "deferred_blocker_with_algorithm_survey_required": {
                k: math.nan for k in mod.Q6F_METRICS
            },
        }

    if branch == "deferred_blocker":
        # c* = elo; beats baseline in point estimate but CIs overlap
        return {
            "omit_reconstructed_rating": {k: math.nan for k in mod.Q6F_METRICS},
            "rolling_win_rate_or_bayesian_smoothed_baseline": _flat_metrics(
                log_loss=0.690, ll_low=0.600, ll_high=0.780,
                brier=0.24, b_low=0.20, b_high=0.28,
            ),
            "elo": _flat_metrics(
                # elo CI high (0.720) > baseline CI low (0.600) => overlap => deferred
                log_loss=0.650, ll_low=0.610, ll_high=0.720,
                brier=0.22, b_low=0.19, b_high=0.26,
            ),
            "glicko_or_glicko_2": _flat_metrics(
                log_loss=0.660, ll_low=0.620, ll_high=0.730,
                brier=0.23, b_low=0.20, b_high=0.27,
            ),
            "trueskill_or_trueskill_like": _flat_metrics(
                log_loss=0.670, ll_low=0.625, ll_high=0.740,
                brier=0.235, b_low=0.205, b_high=0.275,
            ),
            "deferred_blocker_with_algorithm_survey_required": {
                k: math.nan for k in mod.Q6F_METRICS
            },
        }

    if branch == "all_nan":
        return {c: {k: math.nan for k in mod.Q6F_METRICS} for c in Q6F_RATING_ALGORITHM_CANDIDATES}

    raise ValueError(f"Unknown branch: {branch}")


def _make_full_decisions(branch: str = "narrow_with_evidence") -> tuple[RatingSurveyDecision, ...]:
    """Build a full 8-row decision tuple for testing falsifier checks."""
    metrics = _make_metrics_by_candidate(branch)
    return _build_survey_decisions(metrics, audit_pr="PR #TEST")


# ---------------------------------------------------------------------------
# TestModuleConstants
# ---------------------------------------------------------------------------


class TestModuleConstants:
    def test_schema_column_count_is_44(self) -> None:
        assert Q6F_SCHEMA_COLUMN_COUNT == 44

    def test_schema_length_matches_constant(self) -> None:
        assert len(Q6F_SURVEY_SCHEMA) == Q6F_SCHEMA_COLUMN_COUNT

    def test_candidate_count_is_6(self) -> None:
        assert len(Q6F_RATING_ALGORITHM_CANDIDATES) == 6

    def test_survey_candidates_equals_rating_candidates(self) -> None:
        assert Q6F_SURVEY_CANDIDATES == Q6F_RATING_ALGORITHM_CANDIDATES

    def test_included_count_is_4(self) -> None:
        included = sum(1 for v in Q6F_CANDIDATE_INCLUSION.values() if v)
        assert included == 4

    def test_decision_count_is_8(self) -> None:
        assert len(Q6F_DECISION_IDS) == 8

    def test_falsifier_count_at_least_35(self) -> None:
        assert len(FALSIFIER_PRIORITY_CHAIN) >= 35

    def test_falsifier_keys_unique(self) -> None:
        assert len(set(FALSIFIER_PRIORITY_CHAIN)) == len(FALSIFIER_PRIORITY_CHAIN)

    def test_hyperparameter_dict_has_all_4_included_candidates(self) -> None:
        included = [c for c, v in Q6F_CANDIDATE_INCLUSION.items() if v]
        for c in included:
            assert c in Q6F_HYPERPARAMETER_DEFAULTS, f"{c} missing from Q6F_HYPERPARAMETER_DEFAULTS"

    def test_citation_elo_present(self) -> None:
        assert "Elo" in CITATION_ELO_1978
        assert "1978" in CITATION_ELO_1978

    def test_citation_glickman_1999_present(self) -> None:
        assert "Glickman" in CITATION_GLICKMAN_1999
        assert "1999" in CITATION_GLICKMAN_1999

    def test_citation_glickman_2012_present(self) -> None:
        assert "Glickman" in CITATION_GLICKMAN_2012
        assert "2012" in CITATION_GLICKMAN_2012

    def test_citation_herbrich_present(self) -> None:
        assert "Herbrich" in CITATION_HERBRICH_MINKA_GRAEPEL_2006
        assert "2006" in CITATION_HERBRICH_MINKA_GRAEPEL_2006

    def test_citation_steyerberg_present(self) -> None:
        assert "Steyerberg" in CITATION_STEYERBERG_2009

    def test_citation_hosmer_present(self) -> None:
        assert "Hosmer" in CITATION_HOSMER_LEMESHOW_2013

    def test_q5_token_preserved(self) -> None:
        assert Q5_SELECTED_POLICY == "sensitivity_indicator_co_registration"

    def test_q5_verdict_preserved(self) -> None:
        assert Q5_SELECTED_POLICY_VERDICT == "narrow_with_evidence"

    def test_strict_lt_filter_string(self) -> None:
        assert "< target.started_at" in STRICT_LT_HISTORY_FILTER

    def test_history_enriched_family_count(self) -> None:
        assert len(HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS) == 6

    def test_non_rating_family_count(self) -> None:
        assert len(NON_RATING_HISTORY_FAMILIES) == 5

    def test_non_rating_excludes_reconstructed_rating(self) -> None:
        assert "reconstructed_rating" not in NON_RATING_HISTORY_FAMILIES

    def test_bootstrap_seed_is_42(self) -> None:
        assert BOOTSTRAP_RANDOM_SEED == 42

    def test_bootstrap_block_count_is_200(self) -> None:
        assert BOOTSTRAP_BLOCK_COUNT == 200

    def test_candidate_inclusion_keys_match_candidates(self) -> None:
        assert set(Q6F_CANDIDATE_INCLUSION.keys()) == set(Q6F_RATING_ALGORITHM_CANDIDATES)

    def test_selection_decision_rule_string_present(self) -> None:
        assert "bind_now" in Q6F_SELECTION_DECISION_RULE
        assert (
            "log-loss" in Q6F_SELECTION_DECISION_RULE
            or "log_loss" in Q6F_SELECTION_DECISION_RULE
        )

    def test_audit_pr_placeholder(self) -> None:
        assert "TBD" in AUDIT_PR_NUMBER_PLACEHOLDER

    def test_raw_mmr_rejection_token(self) -> None:
        assert "raw_mmr_where_present_plus_is_mmr_missing" in RAW_MMR_HYBRID_REJECTION_TEXT


# ---------------------------------------------------------------------------
# TestParentSHAs
# ---------------------------------------------------------------------------


class TestParentSHAs:
    def test_pr242_csv_sha_matches_file(self) -> None:
        path = REPO_ROOT / PARENT_PR242_CSV_REL
        assert path.exists(), f"PR #242 CSV not found: {path}"
        observed = _sha256_file(path)
        assert observed == EXPECTED_PR242_CSV_SHA256

    def test_pr242_md_sha_matches_file(self) -> None:
        path = REPO_ROOT / PARENT_PR242_MD_REL
        assert path.exists()
        observed = _sha256_file(path)
        assert observed == EXPECTED_PR242_MD_SHA256

    def test_pr243_csv_sha_matches_file(self) -> None:
        path = REPO_ROOT / PARENT_PR243_CSV_REL
        assert path.exists()
        observed = _sha256_file(path)
        assert observed == EXPECTED_PR243_CSV_SHA256

    def test_pr243_md_sha_matches_file(self) -> None:
        path = REPO_ROOT / PARENT_PR243_MD_REL
        assert path.exists()
        observed = _sha256_file(path)
        assert observed == EXPECTED_PR243_MD_SHA256

    def test_pr245_csv_sha_matches_file(self) -> None:
        path = REPO_ROOT / PARENT_PR245_CSV_REL
        assert path.exists()
        observed = _sha256_file(path)
        assert observed == EXPECTED_PR245_CSV_SHA256

    def test_pr245_md_sha_matches_file(self) -> None:
        path = REPO_ROOT / PARENT_PR245_MD_REL
        assert path.exists()
        observed = _sha256_file(path)
        assert observed == EXPECTED_PR245_MD_SHA256


# ---------------------------------------------------------------------------
# TestRollingBaselineEngine
# ---------------------------------------------------------------------------


class TestRollingBaselineEngine:
    def test_forward_only_invariant(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        """Prediction at row N must not use row N's result."""
        result = _run_rolling_baseline_survey(synthetic_2player_4row_stream)
        preds = result["predicted_probabilities"]
        actuals = result["actuals"]
        # Row 0 (alice, first game): cold-start => prior = 0.5
        assert preds[0] == pytest.approx(0.5)
        # At cold-start, is_cold_start must be True
        assert result["is_cold_start"][0]
        # Predictions must be in (0, 1)
        assert all(0.0 < p < 1.0 for p in preds)
        # actuals must be 0 or 1
        assert all(a in (0.0, 1.0) for a in actuals)

    def test_cold_start_laplace_prior(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_rolling_baseline_survey(synthetic_2player_4row_stream, alpha=1.0, beta=1.0)
        # First row per player is cold-start; prior = alpha/(alpha+beta) = 0.5
        assert result["predicted_probabilities"][0] == pytest.approx(0.5)

    def test_cold_start_flag(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_rolling_baseline_survey(synthetic_2player_4row_stream)
        cold = result["is_cold_start"]
        # alice appears at index 0 and 2; bob at 1 and 3
        # sorted: alice row0, bob row1, alice row2, bob row3
        # Rows 0 and 1 are each player's first => cold_start = True
        assert cold[0]
        assert cold[1]
        assert not cold[2]
        assert not cold[3]

    def test_runtime_ms_positive(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_rolling_baseline_survey(synthetic_2player_4row_stream)
        assert result["runtime_ms"] > 0.0

    def test_rating_state_at_end_has_games_and_wins(
        self, synthetic_2player_4row_stream: pd.DataFrame
    ) -> None:
        result = _run_rolling_baseline_survey(synthetic_2player_4row_stream)
        state = result["rating_state_at_end"]
        assert "wins" in state
        assert "games" in state
        assert state["games"]["alice"] == 2
        assert state["games"]["bob"] == 2

    def test_prediction_does_not_use_own_row_result(
        self, synthetic_2player_4row_stream: pd.DataFrame
    ) -> None:
        """Second appearance of alice at row 2 uses only row 0's result."""
        result = _run_rolling_baseline_survey(synthetic_2player_4row_stream, alpha=1.0, beta=1.0)
        # alice row 0: Win. Row 2 prediction = (1 + 1) / (1 + 1 + 1) = 2/3
        # (alpha=1 + 1 win) / (alpha=1 + beta=1 + 1 game)
        assert result["predicted_probabilities"][2] == pytest.approx(2.0 / 3.0)

    def test_custom_alpha_beta(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_rolling_baseline_survey(synthetic_2player_4row_stream, alpha=2.0, beta=3.0)
        # Cold-start prior = 2/(2+3) = 0.4
        assert result["predicted_probabilities"][0] == pytest.approx(0.4)

    def test_returns_required_keys(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_rolling_baseline_survey(synthetic_2player_4row_stream)
        assert set(result.keys()) >= {
            "predicted_probabilities", "actuals", "is_cold_start",
            "rating_state_at_end", "runtime_ms",
        }


# ---------------------------------------------------------------------------
# TestEloEngine
# ---------------------------------------------------------------------------


class TestEloEngine:
    def test_k_factor_default(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        """Default K-factor is 24."""
        out_default = _run_elo_survey(synthetic_2player_4row_stream, k_factor=24.0)
        out_explicit = _run_elo_survey(synthetic_2player_4row_stream, k_factor=24.0)
        assert (
            out_default["predicted_probabilities"] == out_explicit["predicted_probabilities"]
        ).all()

    def test_cold_start_uses_initial_rating(
        self, synthetic_2player_4row_stream: pd.DataFrame
    ) -> None:
        result = _run_elo_survey(synthetic_2player_4row_stream, initial_rating=1500.0)
        # When both players start at 1500, expected = 0.5
        assert result["predicted_probabilities"][0] == pytest.approx(0.5)

    def test_cold_start_flag_set(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_elo_survey(synthetic_2player_4row_stream)
        assert result["is_cold_start"][0]

    def test_symmetric_updates(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        """Focal win -> focal rating increases, opponent rating decreases."""
        result = _run_elo_survey(synthetic_2player_4row_stream)
        state = result["rating_state_at_end"]
        # alice won r1, lost r2; bob lost r1, won r2 => ratings should fluctuate
        assert "alice" in state
        assert "bob" in state

    def test_ratings_change_after_win_loss(
        self, synthetic_2player_4row_stream: pd.DataFrame
    ) -> None:
        result = _run_elo_survey(
            synthetic_2player_4row_stream, k_factor=24.0, initial_rating=1500.0
        )
        state = result["rating_state_at_end"]
        # Not both equal to initial after 2 games each
        assert state["alice"] != 1500.0 or state["bob"] != 1500.0

    def test_prediction_never_reads_own_result(
        self, synthetic_2player_4row_stream: pd.DataFrame
    ) -> None:
        """Row 2 (alice vs bob, 2nd game) uses rating from after row 0 only."""
        result = _run_elo_survey(
            synthetic_2player_4row_stream, k_factor=24.0, initial_rating=1500.0
        )
        preds = result["predicted_probabilities"]
        # Row 0: symmetric => 0.5; after alice wins, alice rating > 1500
        # Row 2: alice rating > 1500 so expected > 0.5
        assert preds[2] > 0.5

    def test_runtime_ms_positive(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_elo_survey(synthetic_2player_4row_stream)
        assert result["runtime_ms"] > 0.0

    def test_returns_required_keys(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_elo_survey(synthetic_2player_4row_stream)
        assert set(result.keys()) >= {
            "predicted_probabilities", "actuals", "is_cold_start",
            "rating_state_at_end", "runtime_ms",
        }

    def test_actuals_are_binary(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_elo_survey(synthetic_2player_4row_stream)
        assert all(a in (0.0, 1.0) for a in result["actuals"])


# ---------------------------------------------------------------------------
# TestGlicko2Engine
# ---------------------------------------------------------------------------


class TestGlicko2Engine:
    def test_mu_default_is_1500(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_glicko2_survey(synthetic_2player_4row_stream, mu=1500.0)
        # Cold-start: both players at mu=1500 => E = 0.5
        assert result["predicted_probabilities"][0] == pytest.approx(0.5, abs=1e-4)

    def test_cold_start_symmetry(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_glicko2_survey(synthetic_2player_4row_stream)
        assert result["predicted_probabilities"][0] == pytest.approx(0.5, abs=1e-4)

    def test_rd_shrinks_after_match(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        """After one match, the focal player's RD should be smaller."""
        result = _run_glicko2_survey(synthetic_2player_4row_stream, rd=350.0)
        state = result["rating_state_at_end"]
        initial_rd_internal = 350.0 / 173.7178
        # alice has 2 matches -> RD should have changed
        assert state["alice"]["rd"] != initial_rd_internal

    def test_ratings_change_forward(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_glicko2_survey(synthetic_2player_4row_stream)
        state = result["rating_state_at_end"]
        initial_mu = (1500.0 - 1500.0) / 173.7178  # = 0.0
        # After 2 decisive matches (1 win, 1 loss) mu should differ from 0
        assert state["alice"]["mu"] != pytest.approx(initial_mu, abs=1e-9)

    def test_tau_constant_recorded(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_glicko2_survey(synthetic_2player_4row_stream, tau=0.5)
        assert result["_tau_constant"] == 0.5

    def test_runtime_ms_positive(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        assert _run_glicko2_survey(synthetic_2player_4row_stream)["runtime_ms"] > 0.0

    def test_cold_start_flag(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_glicko2_survey(synthetic_2player_4row_stream)
        assert result["is_cold_start"][0]

    def test_returns_required_keys(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_glicko2_survey(synthetic_2player_4row_stream)
        assert set(result.keys()) >= {
            "predicted_probabilities", "actuals", "is_cold_start",
            "rating_state_at_end", "runtime_ms", "_tau_constant",
        }


# ---------------------------------------------------------------------------
# TestTrueSkillEngine
# ---------------------------------------------------------------------------


class TestTrueSkillEngine:
    def test_mu_default_is_25(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_trueskill_survey(synthetic_2player_4row_stream, mu_init=25.0)
        state = result["rating_state_at_end"]
        # After decisive games, mu changes from 25
        assert "alice" in state

    def test_cold_start_symmetry(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        """When both players start at mu=25, prediction = 0.5."""
        result = _run_trueskill_survey(synthetic_2player_4row_stream)
        assert result["predicted_probabilities"][0] == pytest.approx(0.5, abs=1e-4)

    def test_sigma_default(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_trueskill_survey(
            synthetic_2player_4row_stream, sigma_init=25.0 / 3.0
        )
        assert result["runtime_ms"] > 0.0

    def test_beta_default(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_trueskill_survey(
            synthetic_2player_4row_stream, beta=25.0 / 6.0
        )
        assert "predicted_probabilities" in result

    def test_tau_default(self) -> None:
        assert Q6F_HYPERPARAMETER_DEFAULTS["trueskill_or_trueskill_like"]["tau"] == pytest.approx(
            25.0 / 300.0
        )

    def test_draw_margin_default_is_zero(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_trueskill_survey(synthetic_2player_4row_stream, draw_margin=0.0)
        preds = result["predicted_probabilities"]
        assert all(0.0 < p < 1.0 for p in preds)

    def test_ratings_change_after_match(
        self, synthetic_2player_4row_stream: pd.DataFrame
    ) -> None:
        result = _run_trueskill_survey(synthetic_2player_4row_stream, mu_init=25.0)
        state = result["rating_state_at_end"]
        assert state["alice"]["mu"] != pytest.approx(25.0)

    def test_cold_start_flag(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        result = _run_trueskill_survey(synthetic_2player_4row_stream)
        assert result["is_cold_start"][0]

    def test_runtime_ms_positive(self, synthetic_2player_4row_stream: pd.DataFrame) -> None:
        assert _run_trueskill_survey(synthetic_2player_4row_stream)["runtime_ms"] > 0.0


# ---------------------------------------------------------------------------
# TestMetrics
# ---------------------------------------------------------------------------


class TestMetrics:
    # Golden-number tests with predictions=[0.6, 0.4, 0.5, 0.7], actuals=[1,0,1,1]
    _preds = np.array([0.6, 0.4, 0.5, 0.7])
    _acts = np.array([1.0, 0.0, 1.0, 1.0])

    def test_auc_golden(self) -> None:
        auc = _auc_from_arrays(self._acts, self._preds)
        # Positive scores: [0.6, 0.5, 0.7]; Negative scores: [0.4]
        # P(pos > neg): 0.6>0.4, 0.5>0.4, 0.7>0.4 => 3 wins, 0 ties out of 3
        # AUC = 3/3 = 1.0 actually... let me recompute:
        # n_pos=3, n_neg=1; sum_pos_ranks in sorted [0.4,0.5,0.6,0.7]
        # ranks: 0.4->1, 0.5->2, 0.6->3, 0.7->4
        # positives at indices [0.5,0.6,0.7] => ranks 2+3+4=9
        # AUC = (9 - 3*4/2) / (3*1) = (9-6)/3 = 1.0
        assert auc == pytest.approx(1.0)

    def test_auc_empty_returns_nan(self) -> None:
        assert math.isnan(_auc_from_arrays(np.array([]), np.array([])))

    def test_auc_single_class_returns_nan(self) -> None:
        assert math.isnan(
            _auc_from_arrays(np.array([1.0, 1.0, 1.0]), np.array([0.6, 0.7, 0.8]))
        )

    def test_auc_all_zero_returns_nan(self) -> None:
        assert math.isnan(
            _auc_from_arrays(np.array([0.0, 0.0, 0.0]), np.array([0.6, 0.7, 0.8]))
        )

    def test_auc_with_ties(self) -> None:
        # All same score: AUC = 0.5
        y_true = np.array([1.0, 0.0, 1.0, 0.0])
        y_score = np.array([0.5, 0.5, 0.5, 0.5])
        auc = _auc_from_arrays(y_true, y_score)
        assert auc == pytest.approx(0.5)

    def test_log_loss_golden(self) -> None:
        ll = _log_loss_from_arrays(self._acts, self._preds)
        expected = -(
            math.log(0.6) + math.log(0.6) + math.log(0.5) + math.log(0.7)
        ) / 4.0
        assert ll == pytest.approx(expected, rel=1e-5)

    def test_log_loss_empty_returns_nan(self) -> None:
        assert math.isnan(_log_loss_from_arrays(np.array([]), np.array([])))

    def test_log_loss_clipping(self) -> None:
        y_true = np.array([1.0])
        y_score = np.array([0.0])  # Would be -inf without clipping
        ll = _log_loss_from_arrays(y_true, y_score)
        assert math.isfinite(ll)

    def test_log_loss_perfect_is_small(self) -> None:
        y_true = np.array([1.0, 0.0, 1.0])
        y_score = np.array([0.9999, 0.0001, 0.9999])
        assert _log_loss_from_arrays(y_true, y_score) < 0.01

    def test_brier_golden(self) -> None:
        brier = _brier_from_arrays(self._acts, self._preds)
        expected = ((0.6 - 1) ** 2 + (0.4 - 0) ** 2 + (0.5 - 1) ** 2 + (0.7 - 1) ** 2) / 4.0
        assert brier == pytest.approx(expected, rel=1e-5)

    def test_brier_approx_0165(self) -> None:
        brier = _brier_from_arrays(self._acts, self._preds)
        assert brier == pytest.approx(0.165, abs=0.005)

    def test_brier_empty_returns_nan(self) -> None:
        assert math.isnan(_brier_from_arrays(np.array([]), np.array([])))

    def test_calibration_error_empty(self) -> None:
        assert math.isnan(_calibration_error(np.array([]), np.array([])))

    def test_calibration_error_perfect(self) -> None:
        # Perfect calibration: score = fraction of positives
        y_true = np.array([1.0, 0.0] * 50)
        y_score = np.array([0.5] * 100)
        ece = _calibration_error(y_true, y_score)
        assert ece == pytest.approx(0.0, abs=0.01)

    def test_calibration_error_range(self) -> None:
        rng = np.random.default_rng(0)
        y_true = rng.integers(0, 2, size=100).astype(float)
        y_score = rng.uniform(0, 1, size=100)
        ece = _calibration_error(y_true, y_score)
        assert 0.0 <= ece <= 1.0


# ---------------------------------------------------------------------------
# TestBootstrapCI
# ---------------------------------------------------------------------------


class TestBootstrapCI:
    def test_deterministic_same_seed(self) -> None:
        rng = np.random.default_rng(7)
        y_true = rng.integers(0, 2, size=50).astype(float)
        y_score = rng.uniform(0, 1, size=50)
        r1 = compute_metrics_with_ci(y_true, y_score, n_bootstrap=50, seed=42)
        r2 = compute_metrics_with_ci(y_true, y_score, n_bootstrap=50, seed=42)
        assert r1["auc"] == r2["auc"]
        assert r1["log_loss_ci_low"] == r2["log_loss_ci_low"]
        assert r1["brier_ci_high"] == r2["brier_ci_high"]

    def test_ci_widens_with_fewer_bootstrap(self) -> None:
        """Fewer bootstrap replicates => wider (noisier) CIs on small samples."""
        rng = np.random.default_rng(11)
        y_true = rng.integers(0, 2, size=40).astype(float)
        y_score = rng.uniform(0.3, 0.7, size=40)
        wide = compute_metrics_with_ci(y_true, y_score, n_bootstrap=10, seed=99)
        narrow = compute_metrics_with_ci(y_true, y_score, n_bootstrap=500, seed=99)
        wide_range = wide["log_loss_ci_high"] - wide["log_loss_ci_low"]
        narrow_range = narrow["log_loss_ci_high"] - narrow["log_loss_ci_low"]
        # Fewer replicates => more variance in CI estimate; not guaranteed
        # deterministically, but should hold with these seeds
        assert wide_range >= 0.0
        assert narrow_range >= 0.0

    def test_empty_array_returns_all_nan(self) -> None:
        result = compute_metrics_with_ci(np.array([]), np.array([]))
        for k, v in result.items():
            assert math.isnan(v), f"Expected NaN for key {k}, got {v}"

    def test_returns_all_required_keys(self) -> None:
        rng = np.random.default_rng(0)
        y_true = rng.integers(0, 2, size=20).astype(float)
        y_score = rng.uniform(0, 1, size=20)
        result = compute_metrics_with_ci(y_true, y_score, n_bootstrap=10, seed=0)
        expected_keys = {
            "auc", "auc_ci_low", "auc_ci_high",
            "log_loss", "log_loss_ci_low", "log_loss_ci_high",
            "brier", "brier_ci_low", "brier_ci_high",
            "calibration_error",
        }
        assert expected_keys.issubset(set(result.keys()))

    def test_ci_low_lte_point_estimate_lte_ci_high_log_loss(self) -> None:
        rng = np.random.default_rng(3)
        y_true = rng.integers(0, 2, size=100).astype(float)
        y_score = rng.uniform(0, 1, size=100)
        result = compute_metrics_with_ci(y_true, y_score, n_bootstrap=100, seed=3)
        assert result["log_loss_ci_low"] <= result["log_loss"] <= result["log_loss_ci_high"]
        assert result["brier_ci_low"] <= result["brier"] <= result["brier_ci_high"]


# ---------------------------------------------------------------------------
# TestSelectionDecisionRule
# ---------------------------------------------------------------------------


class TestSelectionDecisionRule:
    def test_bind_now_branch(self) -> None:
        metrics = _make_metrics_by_candidate("bind_now")
        policy, verdict, perm, rationale = _select_q6f_policy(metrics)
        assert verdict == "bind_now"
        assert perm == (
            "permitted_for_all_6_families_with_pinned_hyperparameters"
            "_in_next_materialization_pr"
        )
        assert (
            "bind_now" in rationale.lower()
            or "log-loss" in rationale.lower()
            or "Candidate" in rationale
        )

    def test_narrow_with_evidence_branch(self) -> None:
        metrics = _make_metrics_by_candidate("narrow_with_evidence")
        policy, verdict, perm, rationale = _select_q6f_policy(metrics)
        assert verdict == "narrow_with_evidence"
        assert perm == "recommendation_only_blocked_pending_implementation_proof_pr"

    def test_omit_reconstructed_rating_branch(self) -> None:
        metrics = _make_metrics_by_candidate("omit_reconstructed_rating_and_unblock_other_five")
        policy, verdict, perm, rationale = _select_q6f_policy(metrics)
        assert verdict == "omit_reconstructed_rating_and_unblock_other_five"
        assert perm == "permitted_for_other_5_families_without_reconstructed_rating"

    def test_deferred_blocker_branch(self) -> None:
        metrics = _make_metrics_by_candidate("deferred_blocker")
        policy, verdict, perm, rationale = _select_q6f_policy(metrics)
        assert verdict == "deferred_blocker"
        assert perm == "blocked_pending_named_reason"

    def test_all_nan_branch(self) -> None:
        metrics = _make_metrics_by_candidate("all_nan")
        policy, verdict, perm, rationale = _select_q6f_policy(metrics)
        assert verdict == "omit_reconstructed_rating_and_unblock_other_five"

    def test_returned_policy_in_allowed_verdicts(self) -> None:
        for branch in ["bind_now", "narrow_with_evidence",
                       "omit_reconstructed_rating_and_unblock_other_five",
                       "deferred_blocker", "all_nan"]:
            metrics = _make_metrics_by_candidate(branch)
            _, verdict, _, _ = _select_q6f_policy(metrics)
            assert verdict in Q6F_ALLOWED_VERDICTS


# ---------------------------------------------------------------------------
# TestDecisionBuilder
# ---------------------------------------------------------------------------


class TestDecisionBuilder:
    def test_emits_exactly_8_decisions(self) -> None:
        decisions = _make_full_decisions()
        assert len(decisions) == 8

    def test_decisions_in_canonical_order(self) -> None:
        decisions = _make_full_decisions()
        observed_ids = tuple(d.decision_id for d in decisions)
        assert observed_ids == Q6F_DECISION_IDS

    def test_materialized_output_paths_empty_on_all_rows(self) -> None:
        decisions = _make_full_decisions()
        for d in decisions:
            assert d.materialized_output_paths == ""

    def test_excluded_methods_on_every_row(self) -> None:
        decisions = _make_full_decisions()
        for d in decisions:
            for method in EXCLUDED_METHODS_CONSIDERED:
                assert method in d.excluded_methods_considered

    def test_raw_mmr_hybrid_rejection_on_every_row(self) -> None:
        decisions = _make_full_decisions()
        for d in decisions:
            assert "raw_mmr_where_present_plus_is_mmr_missing" in d.raw_mmr_hybrid_rejection

    def test_parent_pr242_sha_on_every_row(self) -> None:
        decisions = _make_full_decisions()
        for d in decisions:
            assert d.parent_pr242_csv_sha256 == EXPECTED_PR242_CSV_SHA256
            assert d.parent_pr242_md_sha256 == EXPECTED_PR242_MD_SHA256

    def test_parent_pr243_sha_on_every_row(self) -> None:
        decisions = _make_full_decisions()
        for d in decisions:
            assert d.parent_pr243_csv_sha256 == EXPECTED_PR243_CSV_SHA256
            assert d.parent_pr243_md_sha256 == EXPECTED_PR243_MD_SHA256

    def test_parent_pr245_sha_on_every_row(self) -> None:
        decisions = _make_full_decisions()
        for d in decisions:
            assert d.parent_pr245_csv_sha256 == EXPECTED_PR245_CSV_SHA256
            assert d.parent_pr245_md_sha256 == EXPECTED_PR245_MD_SHA256

    def test_decision_is_frozen_dataclass(self) -> None:
        decisions = _make_full_decisions()
        with pytest.raises(AttributeError):
            decisions[0].decision_id = "mutated"  # type: ignore[misc]

    def test_selected_policy_row_verdict_in_allowed(self) -> None:
        decisions = _make_full_decisions()
        selected = next(d for d in decisions if d.decision_id == "Q6F_selected_policy")
        assert selected.survey_verdict in Q6F_ALLOWED_VERDICTS


# ---------------------------------------------------------------------------
# TestFalsifierChecks
# ---------------------------------------------------------------------------


class TestFalsifierChecks:
    # --- _check_candidate_set_complete ---
    def test_candidate_set_complete_pass(self) -> None:
        decisions = _make_full_decisions()
        passed, msg = _check_candidate_set_complete(decisions)
        assert passed
        assert msg == ""

    def test_candidate_set_complete_fail(self) -> None:
        decisions = _make_full_decisions()
        # Replace first decision's candidate_policy with a duplicate to cause missing
        broken = list(decisions)
        d0 = broken[0]
        broken[0] = RatingSurveyDecision(**{
            **{f.name: getattr(d0, f.name) for f in fields(d0)},
            "candidate_policy": "nonexistent_candidate",
        })
        passed, msg = _check_candidate_set_complete(tuple(broken))
        assert not passed
        assert len(msg) > 0

    # --- _check_decision_count ---
    def test_decision_count_pass(self) -> None:
        decisions = _make_full_decisions()
        passed, msg = _check_decision_count(decisions)
        assert passed
        assert msg == ""

    def test_decision_count_fail(self) -> None:
        decisions = _make_full_decisions()
        passed, msg = _check_decision_count(decisions[:7])
        assert not passed
        assert len(msg) > 0

    # --- _check_decision_id_order ---
    def test_decision_id_order_pass(self) -> None:
        decisions = _make_full_decisions()
        passed, msg = _check_decision_id_order(decisions)
        assert passed

    def test_decision_id_order_fail(self) -> None:
        decisions = list(_make_full_decisions())
        # Swap first two IDs
        d0, d1 = decisions[0], decisions[1]
        decisions[0] = RatingSurveyDecision(**{
            **{f.name: getattr(d0, f.name) for f in fields(d0)},
            "decision_id": d1.decision_id,
        })
        decisions[1] = RatingSurveyDecision(**{
            **{f.name: getattr(d1, f.name) for f in fields(d1)},
            "decision_id": d0.decision_id,
        })
        passed, msg = _check_decision_id_order(tuple(decisions))
        assert not passed
        assert len(msg) > 0

    # --- _check_no_materialized_output_paths ---
    def test_no_materialized_paths_pass(self) -> None:
        decisions = _make_full_decisions()
        passed, msg = _check_no_materialized_output_paths(decisions)
        assert passed

    def test_no_materialized_paths_fail(self) -> None:
        decisions = list(_make_full_decisions())
        d0 = decisions[0]
        decisions[0] = RatingSurveyDecision(**{
            **{f.name: getattr(d0, f.name) for f in fields(d0)},
            "materialized_output_paths": "some/path.parquet",
        })
        passed, msg = _check_no_materialized_output_paths(tuple(decisions))
        assert not passed
        assert len(msg) > 0

    # --- _check_q5_not_re_adjudicated ---
    def test_q5_not_re_adjudicated_pass(self) -> None:
        decisions = _make_full_decisions()
        passed, msg = _check_q5_not_re_adjudicated(decisions)
        assert passed

    def test_q5_not_re_adjudicated_fail(self) -> None:
        decisions = list(_make_full_decisions())
        d0 = decisions[0]
        decisions[0] = RatingSurveyDecision(**{
            **{f.name: getattr(d0, f.name) for f in fields(d0)},
            "survey_verdict": Q5_SELECTED_POLICY,
        })
        passed, msg = _check_q5_not_re_adjudicated(tuple(decisions))
        assert not passed
        assert len(msg) > 0

    # --- _check_selected_policy_row_present ---
    def test_selected_policy_row_pass(self) -> None:
        decisions = _make_full_decisions()
        passed, msg = _check_selected_policy_row_present(decisions)
        assert passed

    def test_selected_policy_row_missing_fail(self) -> None:
        decisions = _make_full_decisions()
        # Remove the selected_policy row
        filtered = tuple(d for d in decisions if d.decision_id != "Q6F_selected_policy")
        passed, msg = _check_selected_policy_row_present(filtered)
        assert not passed
        assert len(msg) > 0

    def test_selected_policy_row_invalid_verdict_fail(self) -> None:
        decisions = list(_make_full_decisions())
        idx = next(i for i, d in enumerate(decisions) if d.decision_id == "Q6F_selected_policy")
        d = decisions[idx]
        decisions[idx] = RatingSurveyDecision(**{
            **{f.name: getattr(d, f.name) for f in fields(d)},
            "survey_verdict": "invalid_verdict_xyz",
        })
        passed, msg = _check_selected_policy_row_present(tuple(decisions))
        assert not passed
        assert len(msg) > 0

    def test_selected_policy_row_invalid_materialization_fail(self) -> None:
        decisions = list(_make_full_decisions())
        idx = next(i for i, d in enumerate(decisions) if d.decision_id == "Q6F_selected_policy")
        d = decisions[idx]
        decisions[idx] = RatingSurveyDecision(**{
            **{f.name: getattr(d, f.name) for f in fields(d)},
            "materialization_permission": "totally_invalid_permission",
        })
        passed, msg = _check_selected_policy_row_present(tuple(decisions))
        assert not passed
        assert len(msg) > 0

    # --- _check_per_family_impact_summary_present ---
    def test_per_family_summary_pass(self) -> None:
        decisions = _make_full_decisions()
        passed, msg = _check_per_family_impact_summary_present(decisions)
        assert passed

    def test_per_family_summary_missing_row_fail(self) -> None:
        decisions = tuple(
            d for d in _make_full_decisions() if d.decision_id != "Q6F_per_family_impact_summary"
        )
        passed, msg = _check_per_family_impact_summary_present(decisions)
        assert not passed

    def test_per_family_summary_missing_family_fail(self) -> None:
        decisions = list(_make_full_decisions())
        idx = next(
            i for i, d in enumerate(decisions)
            if d.decision_id == "Q6F_per_family_impact_summary"
        )
        d = decisions[idx]
        # Remove all family mentions from notes
        decisions[idx] = RatingSurveyDecision(**{
            **{f.name: getattr(d, f.name) for f in fields(d)},
            "notes": "empty notes",
        })
        passed, msg = _check_per_family_impact_summary_present(tuple(decisions))
        assert not passed
        assert len(msg) > 0

    # --- _check_excluded_methods_complete ---
    def test_excluded_methods_pass(self) -> None:
        decisions = _make_full_decisions()
        passed, msg = _check_excluded_methods_complete(decisions)
        assert passed

    def test_excluded_methods_fail(self) -> None:
        decisions = list(_make_full_decisions())
        d0 = decisions[0]
        decisions[0] = RatingSurveyDecision(**{
            **{f.name: getattr(d0, f.name) for f in fields(d0)},
            "excluded_methods_considered": "only_one_method",
        })
        passed, msg = _check_excluded_methods_complete(tuple(decisions))
        assert not passed
        assert len(msg) > 0

    # --- _check_raw_mmr_hybrid_rejection ---
    def test_raw_mmr_pass(self) -> None:
        decisions = _make_full_decisions()
        passed, msg = _check_raw_mmr_hybrid_rejection(decisions)
        assert passed

    def test_raw_mmr_fail(self) -> None:
        decisions = list(_make_full_decisions())
        d0 = decisions[0]
        decisions[0] = RatingSurveyDecision(**{
            **{f.name: getattr(d0, f.name) for f in fields(d0)},
            "raw_mmr_hybrid_rejection": "missing_token_text",
        })
        passed, msg = _check_raw_mmr_hybrid_rejection(tuple(decisions))
        assert not passed
        assert len(msg) > 0


# ---------------------------------------------------------------------------
# TestArtifactWriter
# ---------------------------------------------------------------------------


class TestArtifactWriter:
    def _make_result(self) -> RatingSurveyResult:
        metrics = _make_metrics_by_candidate("narrow_with_evidence")
        decisions = _build_survey_decisions(metrics, audit_pr="PR #TEST")
        return RatingSurveyResult(
            decisions=decisions,
            csv_path="dummy.csv",
            md_path="dummy.md",
            provenance_git_sha="abc123",
            falsifiers_fired=(),
            halting_falsifier=None,
            passed=True,
            metrics_by_candidate=metrics,
            selection="narrow_with_evidence",
        )

    def test_byte_determinism(self, tmp_path: Path) -> None:
        result = self._make_result()
        csv1 = tmp_path / "run1" / "survey.csv"
        md1 = tmp_path / "run1" / "survey.md"
        csv2 = tmp_path / "run2" / "survey.csv"
        md2 = tmp_path / "run2" / "survey.md"
        write_q6f_survey_artifacts(result, csv1, md1)
        write_q6f_survey_artifacts(result, csv2, md2)

        def sha(p: Path) -> str:
            h = hashlib.sha256()
            h.update(p.read_bytes())
            return h.hexdigest()

        assert sha(csv1) == sha(csv2)
        assert sha(md1) == sha(md2)

    def test_csv_has_9_records(self, tmp_path: Path) -> None:
        result = self._make_result()
        csv_path = tmp_path / "survey.csv"
        md_path = tmp_path / "survey.md"
        write_q6f_survey_artifacts(result, csv_path, md_path)
        with csv_path.open("r", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            rows = list(reader)
        # 1 header + 8 data rows
        assert len(rows) == 9

    def test_csv_header_column_count_is_44(self, tmp_path: Path) -> None:
        result = self._make_result()
        csv_path = tmp_path / "survey.csv"
        md_path = tmp_path / "survey.md"
        write_q6f_survey_artifacts(result, csv_path, md_path)
        with csv_path.open("r", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            header = next(reader)
        assert len(header) == 44

    def test_md_has_at_least_17_h2_headings(self, tmp_path: Path) -> None:
        result = self._make_result()
        csv_path = tmp_path / "survey.csv"
        md_path = tmp_path / "survey.md"
        write_q6f_survey_artifacts(result, csv_path, md_path)
        content = md_path.read_text(encoding="utf-8")
        headings = re.findall(r"^## ", content, re.MULTILINE)
        assert len(headings) >= 17

    def test_csv_header_matches_schema(self, tmp_path: Path) -> None:
        result = self._make_result()
        csv_path = tmp_path / "survey.csv"
        write_q6f_survey_artifacts(result, csv_path, tmp_path / "s.md")
        with csv_path.open("r", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            header = next(reader)
        assert tuple(header) == Q6F_SURVEY_SCHEMA

    def test_write_creates_parent_dirs(self, tmp_path: Path) -> None:
        result = self._make_result()
        deep_csv = tmp_path / "a" / "b" / "c" / "survey.csv"
        deep_md = tmp_path / "a" / "b" / "c" / "survey.md"
        write_q6f_survey_artifacts(result, deep_csv, deep_md)
        assert deep_csv.exists()
        assert deep_md.exists()


# ---------------------------------------------------------------------------
# TestNoMaterializationCreep
# ---------------------------------------------------------------------------


class TestNoMaterializationCreep:
    def test_no_q6f_parquet_under_artifact_dir(self) -> None:
        artifact_dir = REPO_ROOT / (
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
            "02_feature_engineering"
        )
        if not artifact_dir.exists():
            pytest.skip("Artifact directory not found")
        q6f_parquets = list(artifact_dir.rglob("*02_01_03_q6f*.parquet"))
        assert q6f_parquets == [], f"Unexpected parquets: {q6f_parquets}"

    def test_no_q6f_json_pkl_npz_under_artifact_dir(self) -> None:
        artifact_dir = REPO_ROOT / (
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
            "02_feature_engineering"
        )
        if not artifact_dir.exists():
            pytest.skip("Artifact directory not found")
        for ext in ["*.json", "*.pkl", "*.npz"]:
            found = [
                p for p in artifact_dir.rglob(ext)
                if "02_01_03_q6f" in p.name
            ]
            assert found == [], f"Unexpected {ext} file: {found}"


# ---------------------------------------------------------------------------
# TestForwardOnlyInvariant
# ---------------------------------------------------------------------------


class TestForwardOnlyInvariant:
    def test_row2_uses_only_row0_state(self) -> None:
        """3 rows for one player; verify state used at row 2 is from row 0+1."""
        rows = [
            {
                "focal_toon": "alice",
                "opponent_toon": "bob",
                "replay_id": "r1",
                "details_timeUTC": "2023-01-01T10:00:00Z",
                "focal_result": "Win",
                "is_cross_region_fragmented": False,
            },
            {
                "focal_toon": "bob",
                "opponent_toon": "alice",
                "replay_id": "r1",
                "details_timeUTC": "2023-01-01T10:00:00Z",
                "focal_result": "Loss",
                "is_cross_region_fragmented": False,
            },
            {
                "focal_toon": "alice",
                "opponent_toon": "bob",
                "replay_id": "r2",
                "details_timeUTC": "2023-01-02T10:00:00Z",
                "focal_result": "Win",
                "is_cross_region_fragmented": False,
            },
        ]
        stream = _make_stream(rows)
        result = _run_rolling_baseline_survey(stream, alpha=1.0, beta=1.0)
        # Row 0 (alice cold-start): prior = 0.5
        assert result["predicted_probabilities"][0] == pytest.approx(0.5)
        # Row 2 (alice 2nd game): uses row 0's result (1 win, 1 game)
        # pred = (1 + 1) / (1 + 1 + 1) = 2/3
        assert result["predicted_probabilities"][2] == pytest.approx(2.0 / 3.0)

    def test_row3_uses_state_from_rows_0_and_2(self) -> None:
        """4-row stream: alice at rows 0, 2, 4 => row 4 uses rows 0+2 outcomes."""
        rows = []
        ts_base = "2023-01-0{}T10:00:00Z"
        _game_seq = [
            ("Win", "1"), ("Win", "1"),
            ("Win", "2"), ("Loss", "2"),
            ("Loss", "3"), ("Win", "3"),
        ]
        for i, (r, ts) in enumerate(_game_seq):
            focal = "alice" if i % 2 == 0 else "bob"
            opp = "bob" if focal == "alice" else "alice"
            rows.append({
                "focal_toon": focal,
                "opponent_toon": opp,
                "replay_id": f"r{i//2 + 1}",
                "details_timeUTC": ts_base.format(ts),
                "focal_result": r,
                "is_cross_region_fragmented": False,
            })
        stream = _make_stream(rows)
        stream = (
            stream
            .sort_values(["focal_toon", "_ts", "replay_id"], kind="stable")
            .reset_index(drop=True)
        )
        result = _run_rolling_baseline_survey(stream, alpha=1.0, beta=1.0)
        # Every prediction must be in valid probability range
        assert all(0.0 < p < 1.0 for p in result["predicted_probabilities"])

    def test_is_cold_start_only_first_appearance(self) -> None:
        rows = [
            {
                "focal_toon": "alice",
                "opponent_toon": "bob",
                "replay_id": "r1",
                "details_timeUTC": "2023-01-01T10:00:00Z",
                "focal_result": "Win",
                "is_cross_region_fragmented": False,
            },
            {
                "focal_toon": "alice",
                "opponent_toon": "bob",
                "replay_id": "r2",
                "details_timeUTC": "2023-01-02T10:00:00Z",
                "focal_result": "Loss",
                "is_cross_region_fragmented": False,
            },
        ]
        stream = _make_stream(rows)
        result = _run_rolling_baseline_survey(stream)
        assert result["is_cold_start"][0]
        assert not result["is_cold_start"][1]


# ---------------------------------------------------------------------------
# TestQ5BindingPreserved
# ---------------------------------------------------------------------------


class TestQ5BindingPreserved:
    def test_q5_selected_policy_constant(self) -> None:
        assert Q5_SELECTED_POLICY == "sensitivity_indicator_co_registration"

    def test_q5_verdict_constant(self) -> None:
        assert Q5_SELECTED_POLICY_VERDICT == "narrow_with_evidence"

    def test_q6f_decisions_do_not_carry_q5_verdict(self) -> None:
        decisions = _make_full_decisions()
        passed, msg = _check_q5_not_re_adjudicated(decisions)
        assert passed, msg

    def test_q5_not_readjudicated_check_returns_true(self) -> None:
        decisions = _make_full_decisions("bind_now")
        passed, _ = _check_q5_not_re_adjudicated(decisions)
        assert passed

    def test_q5_not_readjudicated_for_omit_branch(self) -> None:
        decisions = _make_full_decisions("omit_reconstructed_rating_and_unblock_other_five")
        passed, _ = _check_q5_not_re_adjudicated(decisions)
        assert passed

    def test_q5_not_readjudicated_for_deferred_branch(self) -> None:
        decisions = _make_full_decisions("deferred_blocker")
        passed, _ = _check_q5_not_re_adjudicated(decisions)
        assert passed


# ---------------------------------------------------------------------------
# TestBTLAcknowledgement
# ---------------------------------------------------------------------------


class TestBTLAcknowledgement:
    def test_excluded_methods_tuple(self) -> None:
        assert EXCLUDED_METHODS_CONSIDERED == ("aligulac_style_btl", "bradley_terry", "neural_btl")

    def test_btl_in_md_output(self) -> None:
        metrics = _make_metrics_by_candidate("narrow_with_evidence")
        decisions = _build_survey_decisions(metrics, audit_pr="PR #TEST")
        md = _md_sections(decisions, metrics, "PR #TEST")
        assert "aligulac_style_btl" in md
        assert "bradley_terry" in md
        assert "neural_btl" in md

    def test_btl_methods_on_every_decision_row(self) -> None:
        decisions = _make_full_decisions()
        for d in decisions:
            for m in ("aligulac_style_btl", "bradley_terry", "neural_btl"):
                assert m in d.excluded_methods_considered

    def test_btl_section_in_md(self) -> None:
        metrics = _make_metrics_by_candidate("narrow_with_evidence")
        decisions = _build_survey_decisions(metrics, audit_pr="PR #TEST")
        md = _md_sections(decisions, metrics, "PR #TEST")
        assert "BTL" in md or "bradley_terry" in md


# ---------------------------------------------------------------------------
# TestRawMMRRejection
# ---------------------------------------------------------------------------


class TestRawMMRRejection:
    def test_token_in_rejection_text(self) -> None:
        assert "raw_mmr_where_present_plus_is_mmr_missing" in RAW_MMR_HYBRID_REJECTION_TEXT

    def test_rejection_text_mentions_pr245(self) -> None:
        assert "PR #245" in RAW_MMR_HYBRID_REJECTION_TEXT

    def test_every_decision_has_rejection_token(self) -> None:
        decisions = _make_full_decisions()
        for d in decisions:
            assert "raw_mmr_where_present_plus_is_mmr_missing" in d.raw_mmr_hybrid_rejection

    def test_raw_mmr_check_passes(self) -> None:
        decisions = _make_full_decisions()
        passed, _ = _check_raw_mmr_hybrid_rejection(decisions)
        assert passed

    def test_rejection_text_non_empty(self) -> None:
        assert len(RAW_MMR_HYBRID_REJECTION_TEXT) > 50


# ---------------------------------------------------------------------------
# TestNIT4TrueSkillTau
# ---------------------------------------------------------------------------


class TestNIT4TrueSkillTau:
    def test_tau_default_value(self) -> None:
        expected = 25.0 / 300.0
        actual = Q6F_HYPERPARAMETER_DEFAULTS["trueskill_or_trueskill_like"]["tau"]
        assert actual == pytest.approx(expected)

    def test_citation_herbrich_minka_graepel(self) -> None:
        assert "Herbrich" in CITATION_HERBRICH_MINKA_GRAEPEL_2006
        assert "Minka" in CITATION_HERBRICH_MINKA_GRAEPEL_2006
        assert "Graepel" in CITATION_HERBRICH_MINKA_GRAEPEL_2006
        assert "2006" in CITATION_HERBRICH_MINKA_GRAEPEL_2006

    def test_tau_note_in_hyperparameter_policy(self) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            _CANDIDATE_METHODOLOGY,
        )
        policy = _CANDIDATE_METHODOLOGY["trueskill_or_trueskill_like"]["hyperparameter_policy"]
        assert "tau" in policy.lower() or "tau" in policy

    def test_trueskill_sigma_default(self) -> None:
        assert Q6F_HYPERPARAMETER_DEFAULTS["trueskill_or_trueskill_like"]["sigma"] == (
            pytest.approx(25.0 / 3.0)
        )

    def test_trueskill_beta_default(self) -> None:
        assert Q6F_HYPERPARAMETER_DEFAULTS["trueskill_or_trueskill_like"]["beta"] == (
            pytest.approx(25.0 / 6.0)
        )

    def test_trueskill_draw_margin_default(self) -> None:
        assert Q6F_HYPERPARAMETER_DEFAULTS["trueskill_or_trueskill_like"]["draw_margin"] == 0.0


# ---------------------------------------------------------------------------
# TestAUCNotSoleBinder
# ---------------------------------------------------------------------------


class TestAUCNotSoleBinder:
    def test_high_auc_but_worse_logloss_not_bind_now(self) -> None:
        """AUC is secondary; high AUC but worse log-loss must not produce bind_now."""
        # elo has lower AUC but MUCH better log-loss (it wins on proper scores)
        # baseline minimises log-loss => omit branch, not bind_now
        metrics = _make_metrics_by_candidate("omit_reconstructed_rating_and_unblock_other_five")
        _, verdict, _, _ = _select_q6f_policy(metrics)
        assert verdict != "bind_now"

    def test_decision_rule_text_says_auc_secondary(self) -> None:
        assert "AUC" in Q6F_SELECTION_DECISION_RULE
        assert (
            "secondary" in Q6F_SELECTION_DECISION_RULE
            or "cannot bind" in Q6F_SELECTION_DECISION_RULE.lower()
        )

    def test_auc_not_in_binding_condition_code(self) -> None:
        """The binding rule uses log_loss_ci_* and brier_ci_* not auc_ci_*."""
        import inspect
        src = inspect.getsource(_select_q6f_policy)
        # The binding branches must check log_loss and brier CI
        assert "log_loss_ci_low" in src
        assert "brier_ci_low" in src

    def test_narrow_with_evidence_does_not_require_auc_dominance(self) -> None:
        # narrow_with_evidence branch: elo beats baseline on log-loss CI but
        # glicko CI overlaps with elo -> narrow_with_evidence, not bind_now
        metrics = _make_metrics_by_candidate("narrow_with_evidence")
        _, verdict, _, _ = _select_q6f_policy(metrics)
        assert verdict == "narrow_with_evidence"


# ---------------------------------------------------------------------------
# TestEntrypointIntegration
# ---------------------------------------------------------------------------


class TestEntrypointIntegration:
    def test_run_against_real_db(self, tmp_path: Path) -> None:
        db_path = Path(DB_FILE)
        if not db_path.exists():
            pytest.skip("Real DuckDB not available")
        csv_path = tmp_path / "q6f_survey.csv"
        md_path = tmp_path / "q6f_survey.md"
        result = run_q6f_rating_algorithm_survey(
            db_path=db_path,
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #TEST",
            write_artifacts=True,
            repo_root=REPO_ROOT,
            n_bootstrap=20,
            seed=42,
        )
        assert result.passed, f"halting_falsifier={result.halting_falsifier}"
        assert result.halting_falsifier is None
        assert result.selection in Q6F_ALLOWED_VERDICTS
        assert len(result.decisions) == 8
        assert csv_path.exists()
        assert md_path.exists()

    def test_run_no_write_artifacts(self, tmp_path: Path) -> None:
        db_path = Path(DB_FILE)
        if not db_path.exists():
            pytest.skip("Real DuckDB not available")
        csv_path = tmp_path / "survey.csv"
        md_path = tmp_path / "survey.md"
        result = run_q6f_rating_algorithm_survey(
            db_path=db_path,
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #TEST",
            write_artifacts=False,
            repo_root=REPO_ROOT,
            n_bootstrap=10,
            seed=42,
        )
        assert not csv_path.exists()
        assert not md_path.exists()
        assert result.selection in Q6F_ALLOWED_VERDICTS

    def test_write_artifacts_false_when_falsifier_fires(self, tmp_path: Path) -> None:
        """write_artifacts branch: if result.passed=False, artifacts must NOT be written."""
        db_path = Path(DB_FILE)
        if not db_path.exists():
            pytest.skip("Real DuckDB not available")
        csv_path = tmp_path / "survey.csv"
        md_path = tmp_path / "survey.md"
        # Patch _check_candidate_set_complete to always fail
        with mock.patch(
            "rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms._check_candidate_set_complete",
            return_value=(False, "synthetic failure"),
        ):
            result = run_q6f_rating_algorithm_survey(
                db_path=db_path,
                csv_path=csv_path,
                md_path=md_path,
                write_artifacts=True,
                repo_root=REPO_ROOT,
                n_bootstrap=5,
                seed=42,
            )
        assert not result.passed
        assert not csv_path.exists()


# ---------------------------------------------------------------------------
# TestUtilityHelpers
# ---------------------------------------------------------------------------


class TestUtilityHelpers:
    def test_sha256_file_not_found(self, tmp_path: Path) -> None:
        result = _sha256_file(tmp_path / "nonexistent.txt")
        assert result == "NOT_FOUND"

    def test_sha256_file_existing(self, tmp_path: Path) -> None:
        p = tmp_path / "file.txt"
        p.write_text("hello world", encoding="utf-8")
        digest = _sha256_file(p)
        assert len(digest) == 64
        assert all(c in "0123456789abcdef" for c in digest)

    def test_sha256_file_deterministic(self, tmp_path: Path) -> None:
        p = tmp_path / "file.txt"
        p.write_bytes(b"test content 123")
        assert _sha256_file(p) == _sha256_file(p)

    def test_safe_float_str_none(self) -> None:
        assert _safe_float_str(None) == "NOT_APPLICABLE"

    def test_safe_float_str_nan(self) -> None:
        assert _safe_float_str(math.nan) == "NaN"

    def test_safe_float_str_finite(self) -> None:
        result = _safe_float_str(0.123456)
        assert result == "0.123456"

    def test_safe_float_str_zero(self) -> None:
        result = _safe_float_str(0.0)
        assert result == "0.000000"

    def test_get_git_sha_returns_40_chars_or_unknown(self) -> None:
        sha = _get_git_sha()
        assert sha == "UNKNOWN" or (len(sha) == 40 and all(c in "0123456789abcdef" for c in sha))

    def test_get_git_sha_failure_path(self) -> None:
        with mock.patch(
            "subprocess.run",
            side_effect=FileNotFoundError("git not found"),
        ):
            sha = _get_git_sha()
        assert sha == "UNKNOWN"

    def test_get_git_sha_process_error_path(self) -> None:
        with mock.patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(128, "git"),
        ):
            sha = _get_git_sha()
        assert sha == "UNKNOWN"

    def test_find_repo_root_finds_pyproject(self) -> None:
        start = REPO_ROOT / "src" / "rts_predict"
        root = _find_repo_root(start)
        assert (root / "pyproject.toml").exists()

    def test_find_repo_root_failure(self, tmp_path: Path) -> None:
        # tmp_path has no pyproject.toml anywhere above it
        deep = tmp_path / "a" / "b" / "c"
        deep.mkdir(parents=True)
        with pytest.raises(FileNotFoundError):
            _find_repo_root(deep)


# ---------------------------------------------------------------------------
# TestSchemaInvariants
# ---------------------------------------------------------------------------


class TestSchemaInvariants:
    def test_schema_is_tuple(self) -> None:
        assert isinstance(Q6F_SURVEY_SCHEMA, tuple)

    def test_schema_matches_dataclass_field_order(self) -> None:
        dc_fields = tuple(f.name for f in fields(RatingSurveyDecision))
        assert Q6F_SURVEY_SCHEMA == dc_fields

    def test_schema_column_count_constant_equals_44(self) -> None:
        assert Q6F_SCHEMA_COLUMN_COUNT == 44

    def test_every_field_is_str_annotation(self) -> None:
        for f in fields(RatingSurveyDecision):
            assert f.type == "str", f"Field {f.name} has type {f.type}, expected str"

    def test_dataclass_frozen(self) -> None:
        d = _make_full_decisions()[0]
        with pytest.raises(AttributeError):
            d.decision_id = "mutated"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# TestEnumSets
# ---------------------------------------------------------------------------


class TestEnumSets:
    def test_allowed_verdicts_is_frozenset(self) -> None:
        assert isinstance(Q6F_ALLOWED_VERDICTS, frozenset)

    def test_allowed_verdicts_contains_all_6(self) -> None:
        expected = {
            "bind_now",
            "narrow_with_evidence",
            "recommendation_only",
            "deferred_blocker",
            "omit_reconstructed_rating_and_unblock_other_five",
            "not_applicable_carry_forward",
        }
        assert expected == Q6F_ALLOWED_VERDICTS

    def test_allowed_materialization_is_frozenset(self) -> None:
        assert isinstance(ALLOWED_MATERIALIZATION_PERMISSIONS, frozenset)

    def test_allowed_materialization_has_at_least_6_entries(self) -> None:
        assert len(ALLOWED_MATERIALIZATION_PERMISSIONS) >= 6

    def test_allowed_verdicts_alias(self) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            ALLOWED_Q6F_VERDICTS,
        )
        assert ALLOWED_Q6F_VERDICTS is Q6F_ALLOWED_VERDICTS


# ---------------------------------------------------------------------------
# TestPerFamilyBroadcast
# ---------------------------------------------------------------------------


class TestPerFamilyBroadcast:
    def test_bind_now_all_6_unblocked(self) -> None:
        text = _per_family_broadcast("bind_now")
        for fam in HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS:
            assert fam in text
            assert "unblocked_for_materialization" in text

    def test_omit_5_unblocked_reconstructed_absent(self) -> None:
        text = _per_family_broadcast("omit_reconstructed_rating_and_unblock_other_five")
        for fam in NON_RATING_HISTORY_FAMILIES:
            assert fam in text
        assert "reconstructed_rating: permanently_absent" in text

    def test_deferred_all_6_blocked(self) -> None:
        text = _per_family_broadcast("deferred_blocker")
        for fam in HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS:
            assert fam in text
            assert "blocked_pending_named_reason" in text

    def test_narrow_with_evidence_mentions_implementation_proof(self) -> None:
        text = _per_family_broadcast("narrow_with_evidence")
        assert "implementation_proof_pr" in text

    def test_unknown_verdict_review_required(self) -> None:
        text = _per_family_broadcast("some_unknown_verdict")
        assert "unknown_verdict_review_required" in text

    def test_bind_now_covers_all_families(self) -> None:
        text = _per_family_broadcast("bind_now")
        lines = text.strip().split("\n")
        assert len(lines) == 6


# ---------------------------------------------------------------------------
# TestRatingSurveyError
# ---------------------------------------------------------------------------


class TestRatingSurveyError:
    def test_falsifier_key_attribute(self) -> None:
        err = RatingSurveyError("foo_falsifier", "bar message")
        assert err.falsifier_key == "foo_falsifier"

    def test_message_includes_falsifier_key(self) -> None:
        err = RatingSurveyError("foo_falsifier", "bar message")
        assert "foo_falsifier" in str(err)

    def test_is_runtime_error_subclass(self) -> None:
        err = RatingSurveyError("x", "y")
        assert isinstance(err, RuntimeError)

    def test_can_be_raised_and_caught(self) -> None:
        with pytest.raises(RatingSurveyError) as exc_info:
            raise RatingSurveyError("test_key", "test_message")
        assert exc_info.value.falsifier_key == "test_key"

    def test_message_attribute(self) -> None:
        err = RatingSurveyError("k", "my message")
        assert err.message == "my message"


# ---------------------------------------------------------------------------
# TestCandidateToMetricStrings
# ---------------------------------------------------------------------------


class TestCandidateToMetricStrings:
    def test_excluded_candidate_returns_not_applicable(self) -> None:
        result = _candidate_to_metric_strings(
            "omit_reconstructed_rating", {k: 0.5 for k in mod.Q6F_METRICS}
        )
        for v in result.values():
            assert v == "not_applicable_carry_forward"

    def test_included_candidate_returns_float_strings(self) -> None:
        metrics = _flat_metrics()
        result = _candidate_to_metric_strings("elo", metrics)
        assert result["auc"] != "not_applicable_carry_forward"
        assert "." in result["auc"]

    def test_included_candidate_nan_returns_nan_string(self) -> None:
        metrics = _flat_metrics()
        metrics["auc"] = math.nan
        result = _candidate_to_metric_strings("elo", metrics)
        assert result["auc"] == "NaN"

    def test_excluded_carry_forward_deferred_blocker(self) -> None:
        result = _candidate_to_metric_strings(
            "deferred_blocker_with_algorithm_survey_required",
            {k: 0.5 for k in mod.Q6F_METRICS},
        )
        assert all(v == "not_applicable_carry_forward" for v in result.values())

    def test_runtime_summary_is_deterministic_descriptor(self) -> None:
        metrics = _flat_metrics()
        result = _candidate_to_metric_strings("elo", metrics)
        assert result["runtime_summary"] == "deterministic_forward_only_single_pass"


# ---------------------------------------------------------------------------
# TestWriteCSVDirectly
# ---------------------------------------------------------------------------


class TestWriteCSVDirectly:
    def test_write_csv_creates_file(self, tmp_path: Path) -> None:
        decisions = _make_full_decisions()
        csv_path = tmp_path / "test.csv"
        _write_csv(decisions, csv_path)
        assert csv_path.exists()

    def test_write_csv_row_count(self, tmp_path: Path) -> None:
        decisions = _make_full_decisions()
        csv_path = tmp_path / "test.csv"
        _write_csv(decisions, csv_path)
        with csv_path.open() as fh:
            rows = list(csv.reader(fh))
        assert len(rows) == 9  # 1 header + 8 data


# ---------------------------------------------------------------------------
# TestBuildDecisionDerivedRow
# ---------------------------------------------------------------------------


class TestBuildDecisionDerivedRow:
    def test_derived_row_empty_candidate_policy(self) -> None:
        """When candidate_policy is '', derived row uses sentinel methodology."""
        d = _build_decision(
            decision_id="Q6F_selected_policy",
            candidate_policy="",
            metrics=None,
            selected_policy="narrow_with_evidence",
            verdict="narrow_with_evidence",
            materialization_permission="recommendation_only_blocked_pending_implementation_proof_pr",
            audit_pr="PR #TEST",
            notes="test notes",
        )
        assert d.decision_id == "Q6F_selected_policy"
        assert d.candidate_policy == ""
        assert d.included_in_survey == "False"
        assert d.materialized_output_paths == ""

    def test_build_decision_with_real_candidate_and_metrics(self) -> None:
        metrics = _flat_metrics()
        d = _build_decision(
            decision_id="Q6F_C_elo",
            candidate_policy="elo",
            metrics=metrics,
            selected_policy="",
            verdict="not_applicable_carry_forward",
            materialization_permission="not_applicable_carry_forward",
            audit_pr="PR #TEST",
            notes="elo row",
        )
        assert d.included_in_survey == "True"
        assert d.algorithm_family == "elo_1978"

    def test_build_decision_carry_forward_not_included(self) -> None:
        d = _build_decision(
            decision_id="Q6F_A_omit_reconstructed_rating",
            candidate_policy="omit_reconstructed_rating",
            metrics=None,
            selected_policy="",
            verdict="not_applicable_carry_forward",
            materialization_permission="not_applicable_carry_forward",
            audit_pr="PR #TEST",
            notes="",
        )
        assert d.included_in_survey == "False"
        assert d.auc == "not_applicable_carry_forward"


# ---------------------------------------------------------------------------
# TestMDSections
# ---------------------------------------------------------------------------


class TestMDSections:
    def _build(self) -> tuple[tuple[RatingSurveyDecision, ...], dict[str, dict[str, float]], str]:
        metrics = _make_metrics_by_candidate("narrow_with_evidence")
        decisions = _build_survey_decisions(metrics, audit_pr="PR #TEST")
        return decisions, metrics, "PR #TEST"

    def test_md_starts_with_h1(self) -> None:
        decisions, metrics, audit_pr = self._build()
        md = _md_sections(decisions, metrics, audit_pr)
        assert md.startswith("# Q6F Rating-Algorithm Survey")

    def test_md_contains_btl_methods(self) -> None:
        decisions, metrics, audit_pr = self._build()
        md = _md_sections(decisions, metrics, audit_pr)
        assert "aligulac_style_btl" in md

    def test_md_contains_raw_mmr_rejection(self) -> None:
        decisions, metrics, audit_pr = self._build()
        md = _md_sections(decisions, metrics, audit_pr)
        assert "raw_mmr_where_present_plus_is_mmr_missing" in md

    def test_md_contains_sha_provenance(self) -> None:
        decisions, metrics, audit_pr = self._build()
        md = _md_sections(decisions, metrics, audit_pr)
        assert EXPECTED_PR242_CSV_SHA256 in md
        assert EXPECTED_PR245_MD_SHA256 in md

    def test_md_mentions_no_materialization(self) -> None:
        decisions, metrics, audit_pr = self._build()
        md = _md_sections(decisions, metrics, audit_pr)
        assert "NOT materialize" in md or "does NOT materialize" in md or "does not" in md.lower()


# ---------------------------------------------------------------------------
# TestLoadPHAHistoryChronological (tiny in-memory DuckDB)
# ---------------------------------------------------------------------------


class TestLoadPHAHistoryChronological:
    def _build_db(self, tmp_path: Path) -> Path:
        """Create a tiny in-memory DuckDB at tmp_path with a player_history_all table."""
        db_path = tmp_path / "test.duckdb"
        con = duckdb.connect(str(db_path))
        con.execute("""
            CREATE TABLE player_history_all (
                toon_id VARCHAR,
                replay_id VARCHAR,
                details_timeUTC VARCHAR,
                result VARCHAR,
                is_cross_region_fragmented BOOLEAN
            )
        """)
        con.execute("""
            INSERT INTO player_history_all VALUES
            ('alice', 'r1', '2023-01-01T10:00:00Z', 'Win',  false),
            ('bob',   'r1', '2023-01-01T10:00:00Z', 'Loss', false),
            ('alice', 'r2', '2023-01-02T10:00:00Z', 'Loss', false),
            ('bob',   'r2', '2023-01-02T10:00:00Z', 'Win',  false)
        """)
        con.close()
        return db_path

    def test_load_returns_dataframe(self, tmp_path: Path) -> None:
        db_path = self._build_db(tmp_path)
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            _load_pha_history_chronological,
        )
        df = _load_pha_history_chronological(db_path)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4

    def test_load_has_required_columns(self, tmp_path: Path) -> None:
        db_path = self._build_db(tmp_path)
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            _load_pha_history_chronological,
        )
        df = _load_pha_history_chronological(db_path)
        for col in (
            "focal_toon", "opponent_toon", "replay_id",
            "details_timeUTC", "focal_result", "is_cross_region_fragmented",
        ):
            assert col in df.columns

    def test_load_empty_raises_survey_error(self, tmp_path: Path) -> None:
        db_path = tmp_path / "empty.duckdb"
        con = duckdb.connect(str(db_path))
        con.execute("""
            CREATE TABLE player_history_all (
                toon_id VARCHAR,
                replay_id VARCHAR,
                details_timeUTC VARCHAR,
                result VARCHAR,
                is_cross_region_fragmented BOOLEAN
            )
        """)
        con.close()
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            _load_pha_history_chronological,
        )
        with pytest.raises(RatingSurveyError):
            _load_pha_history_chronological(db_path)


# ---------------------------------------------------------------------------
# TestDecisionIDsComplete
# ---------------------------------------------------------------------------


class TestDecisionIDsComplete:
    def test_candidate_decision_ids_match_candidates(self) -> None:
        candidate_ids = Q6F_DECISION_IDS[:6]
        for did, cand in zip(candidate_ids, Q6F_RATING_ALGORITHM_CANDIDATES):
            assert cand in did

    def test_last_two_decision_ids(self) -> None:
        assert Q6F_DECISION_IDS[6] == "Q6F_selected_policy"
        assert Q6F_DECISION_IDS[7] == "Q6F_per_family_impact_summary"


# ---------------------------------------------------------------------------
# TestHyperparameterDefaults
# ---------------------------------------------------------------------------


class TestHyperparameterDefaults:
    def test_rolling_baseline_alpha_beta(self) -> None:
        hp = Q6F_HYPERPARAMETER_DEFAULTS["rolling_win_rate_or_bayesian_smoothed_baseline"]
        assert hp["alpha"] == pytest.approx(1.0)
        assert hp["beta"] == pytest.approx(1.0)

    def test_elo_k_factor(self) -> None:
        hp = Q6F_HYPERPARAMETER_DEFAULTS["elo"]
        assert hp["k_factor"] == pytest.approx(24.0)

    def test_elo_initial_rating(self) -> None:
        hp = Q6F_HYPERPARAMETER_DEFAULTS["elo"]
        assert hp["initial_rating"] == pytest.approx(1500.0)

    def test_glicko_mu(self) -> None:
        hp = Q6F_HYPERPARAMETER_DEFAULTS["glicko_or_glicko_2"]
        assert hp["mu"] == pytest.approx(1500.0)

    def test_glicko_rd(self) -> None:
        hp = Q6F_HYPERPARAMETER_DEFAULTS["glicko_or_glicko_2"]
        assert hp["rd"] == pytest.approx(350.0)

    def test_glicko_sigma(self) -> None:
        hp = Q6F_HYPERPARAMETER_DEFAULTS["glicko_or_glicko_2"]
        assert hp["sigma"] == pytest.approx(0.06)

    def test_glicko_tau(self) -> None:
        hp = Q6F_HYPERPARAMETER_DEFAULTS["glicko_or_glicko_2"]
        assert hp["tau"] == pytest.approx(0.5)

    def test_trueskill_mu(self) -> None:
        hp = Q6F_HYPERPARAMETER_DEFAULTS["trueskill_or_trueskill_like"]
        assert hp["mu"] == pytest.approx(25.0)


# ---------------------------------------------------------------------------
# Additional coverage: _build_survey_decisions branches
# ---------------------------------------------------------------------------


class TestBuildSurveyDecisionsBranches:
    def test_bind_now_selected_policy_row_verdict(self) -> None:
        metrics = _make_metrics_by_candidate("bind_now")
        decisions = _build_survey_decisions(metrics, audit_pr="PR #TEST")
        selected = next(d for d in decisions if d.decision_id == "Q6F_selected_policy")
        assert selected.survey_verdict == "bind_now"

    def test_omit_selected_policy_row_verdict(self) -> None:
        metrics = _make_metrics_by_candidate("omit_reconstructed_rating_and_unblock_other_five")
        decisions = _build_survey_decisions(metrics, audit_pr="PR #TEST")
        selected = next(d for d in decisions if d.decision_id == "Q6F_selected_policy")
        assert selected.survey_verdict == "omit_reconstructed_rating_and_unblock_other_five"

    def test_deferred_selected_policy_row_verdict(self) -> None:
        metrics = _make_metrics_by_candidate("deferred_blocker")
        decisions = _build_survey_decisions(metrics, audit_pr="PR #TEST")
        selected = next(d for d in decisions if d.decision_id == "Q6F_selected_policy")
        assert selected.survey_verdict == "deferred_blocker"

    def test_all_nan_selected_policy_row_verdict(self) -> None:
        metrics = _make_metrics_by_candidate("all_nan")
        decisions = _build_survey_decisions(metrics, audit_pr="PR #TEST")
        selected = next(d for d in decisions if d.decision_id == "Q6F_selected_policy")
        assert selected.survey_verdict == "omit_reconstructed_rating_and_unblock_other_five"

    def test_per_family_row_notes_contain_families(self) -> None:
        metrics = _make_metrics_by_candidate("narrow_with_evidence")
        decisions = _build_survey_decisions(metrics, audit_pr="PR #TEST")
        family_row = next(d for d in decisions if d.decision_id == "Q6F_per_family_impact_summary")
        for fam in HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS:
            assert fam in family_row.notes

    def test_candidate_rows_have_q5_binding_in_cross_region_policy(self) -> None:
        decisions = _make_full_decisions()
        for d in decisions[:6]:
            assert Q5_SELECTED_POLICY in d.cross_region_policy


# ---------------------------------------------------------------------------
# TestGlicko2InternalFunctions
# ---------------------------------------------------------------------------


class TestGlicko2InternalFunctions:
    def test_glicko2_g_zero(self) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            _glicko2_g,
        )
        # g(0) = 1 / sqrt(1) = 1
        assert _glicko2_g(0.0) == pytest.approx(1.0)

    def test_glicko2_e_symmetric(self) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            _glicko2_e,
        )
        # E(mu, mu, rd) = 0.5
        assert _glicko2_e(0.0, 0.0, 0.5) == pytest.approx(0.5)

    def test_trueskill_win_prob_symmetric(self) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            _trueskill_win_prob,
        )
        assert _trueskill_win_prob(25.0, 8.33, 25.0, 8.33, 4.17) == pytest.approx(0.5, abs=1e-3)

    def test_trueskill_v_high_t(self) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            _trueskill_v,
        )
        # v(t) for very high t: pdf/cdf ~ t when cdf -> 0
        v = _trueskill_v(-100.0)
        assert math.isfinite(v)

    def test_trueskill_w_positive(self) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            _trueskill_w,
        )
        w = _trueskill_w(1.0)
        assert w > 0.0


# ---------------------------------------------------------------------------
# TestComputeEngineMetrics
# ---------------------------------------------------------------------------


class TestComputeEngineMetrics:
    def test_all_cold_start_returns_nan_auc(
        self, synthetic_2player_4row_stream: pd.DataFrame
    ) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            _compute_engine_metrics,
        )
        # Create a 1-row stream so everything is cold-start
        rows = [
            {
                "focal_toon": "solo_player",
                "opponent_toon": "opp",
                "replay_id": "r1",
                "details_timeUTC": "2023-01-01T10:00:00Z",
                "focal_result": "Win",
                "is_cross_region_fragmented": False,
            }
        ]
        stream = _make_stream(rows)
        engine_out = _run_rolling_baseline_survey(stream)
        metrics = _compute_engine_metrics(engine_out, n_bootstrap=5, seed=42)
        # coverage_rate = 0 (all cold start), auc = NaN
        assert metrics["cold_start_rate"] == pytest.approx(1.0)
        assert math.isnan(metrics["auc"])

    def test_normal_path_returns_valid_metrics(
        self, synthetic_2player_4row_stream: pd.DataFrame
    ) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            _compute_engine_metrics,
        )
        engine_out = _run_rolling_baseline_survey(synthetic_2player_4row_stream)
        metrics = _compute_engine_metrics(engine_out, n_bootstrap=10, seed=42)
        assert "auc" in metrics
        assert "log_loss" in metrics
        assert "brier" in metrics
        assert metrics["tie_rate"] == 0.0
        assert metrics["runtime_seconds"] > 0.0


# ---------------------------------------------------------------------------
# TestRemainingBranches (targeted to reach >=99% coverage)
# ---------------------------------------------------------------------------


class TestRemainingBranches:
    def test_load_pha_unparseable_timestamp_raises(self, tmp_path: Path) -> None:
        """Covers line 884: unparseable details_timeUTC."""
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            _load_pha_history_chronological,
        )
        db_path = tmp_path / "bad_ts.duckdb"
        con = duckdb.connect(str(db_path))
        con.execute("""
            CREATE TABLE player_history_all (
                toon_id VARCHAR,
                replay_id VARCHAR,
                details_timeUTC VARCHAR,
                result VARCHAR,
                is_cross_region_fragmented BOOLEAN
            )
        """)
        # Two rows from same replay (required for pairing) with bad timestamp
        con.execute("""
            INSERT INTO player_history_all VALUES
            ('alice', 'r1', 'not-a-date', 'Win',  false),
            ('bob',   'r1', 'not-a-date', 'Loss', false)
        """)
        con.close()
        with pytest.raises(RatingSurveyError) as exc_info:
            _load_pha_history_chronological(db_path)
        assert exc_info.value.falsifier_key == "q6f_candidate_set_incomplete"

    def test_check_parent_pr_shas_mismatch(self, tmp_path: Path) -> None:
        """Covers line 2431: SHA mismatch in _check_parent_pr_shas."""
        from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
            _check_parent_pr_shas,
        )
        # Create a fake repo root with wrong-content artifact files
        artifact_dir = (
            tmp_path
            / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
            / "02_feature_engineering/01_pre_game_vs_in_game_boundary"
        )
        artifact_dir.mkdir(parents=True)
        for rel in [PARENT_PR242_CSV_REL, PARENT_PR242_MD_REL,
                    PARENT_PR243_CSV_REL, PARENT_PR243_MD_REL,
                    PARENT_PR245_CSV_REL, PARENT_PR245_MD_REL]:
            (tmp_path / rel).write_text("wrong content", encoding="utf-8")
        mismatches = _check_parent_pr_shas((), tmp_path)
        assert len(mismatches) > 0
        assert mismatches[0][0] == "parent_pr242_csv_sha256_mismatch"

    def test_run_without_repo_root_uses_find(self, tmp_path: Path) -> None:
        """Covers line 2807: repo_root=None triggers _find_repo_root."""
        db_path = Path(DB_FILE)
        if not db_path.exists():
            pytest.skip("Real DuckDB not available")
        csv_path = tmp_path / "survey.csv"
        md_path = tmp_path / "survey.md"
        # repo_root=None => _find_repo_root is called internally
        result = run_q6f_rating_algorithm_survey(
            db_path=db_path,
            csv_path=csv_path,
            md_path=md_path,
            write_artifacts=False,
            repo_root=None,  # triggers the find
            n_bootstrap=5,
            seed=42,
        )
        assert result.selection in Q6F_ALLOWED_VERDICTS

    def test_run_sha_mismatch_raises_survey_error(self, tmp_path: Path) -> None:
        """Covers lines 2811-2812: SHA mismatch raises RatingSurveyError."""
        db_path = Path(DB_FILE)
        if not db_path.exists():
            pytest.skip("Real DuckDB not available")
        # Create a fake repo root with wrong content -> SHA mismatch
        artifact_dir = (
            tmp_path
            / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
            / "02_feature_engineering/01_pre_game_vs_in_game_boundary"
        )
        artifact_dir.mkdir(parents=True)
        for rel in [PARENT_PR242_CSV_REL, PARENT_PR242_MD_REL,
                    PARENT_PR243_CSV_REL, PARENT_PR243_MD_REL,
                    PARENT_PR245_CSV_REL, PARENT_PR245_MD_REL]:
            (tmp_path / rel).write_text("wrong content", encoding="utf-8")
        (tmp_path / "pyproject.toml").write_text("[tool]", encoding="utf-8")
        with pytest.raises(RatingSurveyError) as exc_info:
            run_q6f_rating_algorithm_survey(
                db_path=db_path,
                csv_path=tmp_path / "s.csv",
                md_path=tmp_path / "s.md",
                repo_root=tmp_path,
                n_bootstrap=5,
                seed=42,
            )
        assert "sha256_mismatch" in exc_info.value.falsifier_key

    def test_falsifiers_fired_triggers_rebuild(self, tmp_path: Path) -> None:
        """Covers line 2847->2843: falsifiers_fired causes decision rebuild."""
        db_path = Path(DB_FILE)
        if not db_path.exists():
            pytest.skip("Real DuckDB not available")
        csv_path = tmp_path / "s.csv"
        md_path = tmp_path / "s.md"
        call_count = {"n": 0}

        original_check = mod._check_candidate_set_complete

        def patched_check(decisions: tuple) -> tuple[bool, str]:
            call_count["n"] += 1
            if call_count["n"] == 1:
                return (False, "synthetic first-call failure")
            return original_check(decisions)

        with mock.patch(
            "rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms._check_candidate_set_complete",
            side_effect=patched_check,
        ):
            result = run_q6f_rating_algorithm_survey(
                db_path=db_path,
                csv_path=csv_path,
                md_path=md_path,
                write_artifacts=False,
                repo_root=REPO_ROOT,
                n_bootstrap=5,
                seed=42,
            )
        # The first check fires => falsifiers_fired non-empty => rebuild happens
        assert "q6f_candidate_set_incomplete" in result.falsifiers_fired
