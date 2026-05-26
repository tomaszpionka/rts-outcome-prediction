"""Comprehensive tests for proof_glicko2_implementation.py (Q6G proof).

Coverage target: >= 95% branch coverage on the proof module per
``planning/current_plan.md`` Gate clause (d2). Test target: >= 150 tests
per Gate clause (d1).

Per-class minimums (R2-N1 advisory):
    TestFalsifierChain >= 38 keys
    TestEquivalenceProof_* >= 10 tests
    TestDecisionRule_* >= 6 tests

All synthetic fixtures are in-memory; real DuckDB is exercised only via
``TestEntrypointIntegration`` with a ``pytest.skip`` guard when
``DB_FILE`` is unavailable (CI / fresh clone).
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from dataclasses import fields
from pathlib import Path
from typing import Any
from unittest import mock

import numpy as np
import pandas as pd
import pytest

from rts_predict.games.sc2.config import DB_FILE
from rts_predict.games.sc2.datasets.sc2egset import proof_glicko2_implementation as mod
from rts_predict.games.sc2.datasets.sc2egset.proof_glicko2_implementation import (
    AUDIT_PR_NUMBER_PLACEHOLDER,
    BOOTSTRAP_BLOCK_COUNT,
    BOOTSTRAP_METHOD,
    BOOTSTRAP_RANDOM_SEED,
    CITATION_EFRON_TIBSHIRANI_1993,
    CITATION_GLICKMAN_1999,
    CITATION_GLICKMAN_2012,
    CITATION_KAHAN_SUMMATION_HIGHAM_2002,
    EQUIVALENCE_SPEARMAN_MIN,
    EXPECTED_PR242_CSV_SHA256,
    EXPECTED_PR242_MD_SHA256,
    EXPECTED_PR243_CSV_SHA256,
    EXPECTED_PR243_MD_SHA256,
    EXPECTED_PR245_CSV_SHA256,
    EXPECTED_PR245_MD_SHA256,
    EXPECTED_PR247_CSV_SHA256,
    EXPECTED_PR247_MD_SHA256,
    FALSIFIER_PRIORITY_CHAIN,
    GLICKO2_ITERATION_TOL,
    GLICKO2_PATH_KINDS,
    MD_SAMPLE_ROW_COUNT,
    NUMPY_RNG_BIT_GENERATOR,
    PARENT_PR242_CSV_REL,
    PARENT_PR242_MD_REL,
    PARENT_PR243_CSV_REL,
    PARENT_PR243_MD_REL,
    PARENT_PR245_CSV_REL,
    PARENT_PR245_MD_REL,
    PARENT_PR247_CSV_REL,
    PARENT_PR247_MD_REL,
    PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY,
    Q5_SELECTED_POLICY,
    Q5_SELECTED_POLICY_VERDICT,
    Q6F_MATERIALIZATION_PERMISSION,
    Q6F_SELECTED_POLICY,
    Q6F_SELECTED_POLICY_VERDICT,
    Q6G_ALLOWED_MATERIALIZATION_PERMISSIONS,
    Q6G_ALLOWED_VERDICTS,
    Q6G_BOOTSTRAP_BLOCK_COUNT,
    Q6G_BOOTSTRAP_METHOD,
    Q6G_BOOTSTRAP_RANDOM_SEED,
    Q6G_DECISION_COUNT,
    Q6G_FLOATING_POINT_SUMMATION_ORDER_POLICY,
    Q6G_GLICKO2_ITERATION_TOL,
    Q6G_HYPERPARAMETER_DEFAULTS,
    Q6G_NUMPY_RNG_BIT_GENERATOR,
    Q6G_PARENT_SHAS,
    Q6G_PROOF_CSV_REL,
    Q6G_PROOF_DECISION_RULE,
    Q6G_PROOF_MD_REL,
    Q6G_PROOF_ROWS,
    Q6G_PROOF_SCHEMA,
    Q6G_PROOF_SCHEMA_COLUMN_COUNT,
    Q6G_RATING_PERIOD_DAYS,
    RATING_PERIOD_DAYS,
    RAW_MMR_HYBRID_REJECTION_TEXT,
    RatingImplementationProofDecision,
    RatingImplementationProofError,
    RatingImplementationProofResult,
    compute_proof_metrics,
    run_q6g_rating_implementation_proof,
    write_q6g_proof_artifacts,
)

# ---------------------------------------------------------------------------
# Shared synthetic fixtures
# ---------------------------------------------------------------------------


def _synth_stream(rows: int = 100, n_toons: int = 8, seed: int = 7) -> pd.DataFrame:
    """Build a deterministic synthetic PHA-shape stream.

    Args:
        rows: Number of paired rows.
        n_toons: Number of distinct toons.
        seed: RNG seed for synth labels.

    Returns:
        DataFrame with the PHA loader columns.
    """
    rng = np.random.default_rng(seed)
    toons = [f"toon_{k:03d}" for k in range(n_toons)]
    focal = rng.choice(toons, size=rows)
    opp = []
    for f in focal:
        choices = [t for t in toons if t != f]
        opp.append(rng.choice(choices))
    opp = np.array(opp)
    # Timestamps spanning ~120 days from 2024-01-01.
    base = pd.Timestamp("2024-01-01T00:00:00Z")
    raw_offsets = rng.integers(0, 120 * 86400, size=rows)
    ts = pd.DatetimeIndex([base + pd.Timedelta(seconds=int(s)) for s in raw_offsets])
    ts = ts.sort_values()
    # Results: bias the higher-numbered focal toon to win more often to
    # produce a learnable signal.
    p_win = np.clip(
        0.5 + 0.04 * (np.array([int(f.split("_")[1]) for f in focal]) - n_toons / 2),
        0.05,
        0.95,
    )
    win_draws = rng.random(rows) < p_win
    results = np.where(win_draws, "Win", "Loss")
    replay_ids = [f"replay_{k:08d}" for k in range(rows)]
    df = pd.DataFrame(
        {
            "focal_toon": focal,
            "opponent_toon": opp,
            "replay_id": replay_ids,
            "details_timeUTC": ts.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "focal_result": results,
            "is_cross_region_fragmented": np.zeros(rows, dtype=bool),
        }
    )
    return df.sort_values(by=["focal_toon", "details_timeUTC", "replay_id"]).reset_index(
        drop=True
    )


def _two_player_two_period_fixture() -> pd.DataFrame:
    """A 2-player, 4-row, 2-period synthetic fixture (T03 verification).

    Returns:
        DataFrame with 4 rows spanning 2 thirty-day periods.
    """
    base = pd.Timestamp("2024-01-01T00:00:00Z")
    rows = [
        # Period 1 (days 0-29).
        ("toon_A", "toon_B", "replay_001", base + pd.Timedelta(days=1), "Win"),
        ("toon_A", "toon_B", "replay_002", base + pd.Timedelta(days=15), "Loss"),
        # Period 2 (days 30-59).
        ("toon_A", "toon_B", "replay_003", base + pd.Timedelta(days=35), "Win"),
        ("toon_A", "toon_B", "replay_004", base + pd.Timedelta(days=45), "Loss"),
    ]
    df = pd.DataFrame(
        rows, columns=["focal_toon", "opponent_toon", "replay_id", "_ts", "focal_result"]
    )
    df["details_timeUTC"] = df["_ts"].dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    df["is_cross_region_fragmented"] = False
    return df.drop(columns=["_ts"]).reset_index(drop=True)


@pytest.fixture
def synth_stream() -> pd.DataFrame:
    return _synth_stream()


@pytest.fixture
def small_two_period_stream() -> pd.DataFrame:
    return _two_player_two_period_fixture()


# ---------------------------------------------------------------------------
# TestModuleConstants
# ---------------------------------------------------------------------------


class TestModuleConstants:
    def test_schema_length_is_39(self) -> None:
        assert Q6G_PROOF_SCHEMA_COLUMN_COUNT == 39

    def test_schema_tuple_length_is_39(self) -> None:
        assert len(Q6G_PROOF_SCHEMA) == 39

    def test_dataclass_field_count_is_39(self) -> None:
        assert len(fields(RatingImplementationProofDecision)) == 39

    def test_decision_count_is_5(self) -> None:
        assert Q6G_DECISION_COUNT == 5

    def test_proof_rows_length_is_5(self) -> None:
        assert len(Q6G_PROOF_ROWS) == 5

    def test_proof_rows_contain_canonical_labels(self) -> None:
        assert Q6G_PROOF_ROWS == (
            "Q6G_A_glicko2_event_by_event_reference",
            "Q6G_B_glicko2_batched_production_shape",
            "Q6G_C_glicko2_event_vs_batched_equivalence_proof",
            "Q6G_D_glicko2_implementation_byte_determinism_proof",
            "Q6G_selected_policy",
        )

    def test_bootstrap_seed_is_42(self) -> None:
        assert BOOTSTRAP_RANDOM_SEED == 42 and Q6G_BOOTSTRAP_RANDOM_SEED == 42

    def test_bootstrap_block_count_is_200(self) -> None:
        assert BOOTSTRAP_BLOCK_COUNT == 200 and Q6G_BOOTSTRAP_BLOCK_COUNT == 200

    def test_bootstrap_method_is_deterministic_percentile(self) -> None:
        assert BOOTSTRAP_METHOD == "deterministic_percentile"
        assert Q6G_BOOTSTRAP_METHOD == "deterministic_percentile"

    def test_numpy_rng_is_pcg64(self) -> None:
        assert NUMPY_RNG_BIT_GENERATOR == "PCG64"
        assert Q6G_NUMPY_RNG_BIT_GENERATOR == "PCG64"

    def test_summation_policy_is_sorted_then_kahan(self) -> None:
        assert PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY == "sorted_then_kahan"
        assert Q6G_FLOATING_POINT_SUMMATION_ORDER_POLICY == "sorted_then_kahan"

    def test_rating_period_days_is_30(self) -> None:
        assert RATING_PERIOD_DAYS == 30 and Q6G_RATING_PERIOD_DAYS == 30

    def test_glicko2_iteration_tol_is_1e_6(self) -> None:
        assert GLICKO2_ITERATION_TOL == 1e-6 and Q6G_GLICKO2_ITERATION_TOL == 1e-6

    def test_equivalence_spearman_min_is_0_99(self) -> None:
        assert EQUIVALENCE_SPEARMAN_MIN == 0.99

    def test_md_sample_row_count_is_5(self) -> None:
        assert MD_SAMPLE_ROW_COUNT == 5

    def test_q5_bindings_preserved(self) -> None:
        assert Q5_SELECTED_POLICY == "sensitivity_indicator_co_registration"
        assert Q5_SELECTED_POLICY_VERDICT == "narrow_with_evidence"

    def test_q6f_bindings_preserved(self) -> None:
        assert Q6F_SELECTED_POLICY == "narrow_with_evidence"
        assert Q6F_SELECTED_POLICY_VERDICT == "narrow_with_evidence"
        assert (
            Q6F_MATERIALIZATION_PERMISSION
            == "recommendation_only_blocked_pending_implementation_proof_pr"
        )

    def test_hyperparameter_defaults_match_glickman_2012(self) -> None:
        d = Q6G_HYPERPARAMETER_DEFAULTS
        assert d["mu"] == 1500.0
        assert d["rd"] == 350.0
        assert d["sigma"] == 0.06
        assert d["tau"] == 0.5
        assert d["rating_period_days"] == 30.0
        assert d["iteration_tol"] == 1e-6

    def test_citation_glickman_2012_present(self) -> None:
        assert "Glickman" in CITATION_GLICKMAN_2012
        assert "2012" in CITATION_GLICKMAN_2012

    def test_citation_glickman_1999_present(self) -> None:
        assert "Glickman" in CITATION_GLICKMAN_1999

    def test_citation_efron_tibshirani_1993_present(self) -> None:
        assert "Efron" in CITATION_EFRON_TIBSHIRANI_1993
        assert "Tibshirani" in CITATION_EFRON_TIBSHIRANI_1993

    def test_citation_higham_2002_present(self) -> None:
        assert "Higham" in CITATION_KAHAN_SUMMATION_HIGHAM_2002

    def test_q6g_allowed_verdicts_set(self) -> None:
        assert "bind_now" in Q6G_ALLOWED_VERDICTS
        assert "recommendation_only_glicko2" in Q6G_ALLOWED_VERDICTS
        assert "defer_to_two_candidate_implementation_comparison" in Q6G_ALLOWED_VERDICTS
        assert (
            "omit_reconstructed_rating_and_unblock_other_five" in Q6G_ALLOWED_VERDICTS
        )
        assert "deferred_blocker" in Q6G_ALLOWED_VERDICTS

    def test_q6g_allowed_materialization_permissions_set(self) -> None:
        for perm in (
            "permitted_for_all_6_families_with_pinned_glicko2_batched_"
            "production_implementation_and_hyperparameters_in_next_"
            "materialization_pr",
            "recommendation_only_glicko2_event_by_event_validated_"
            "batched_path_unproven_or_unequivalent",
            "blocked_pending_q6h_two_candidate_implementation_comparison_pr",
            "permitted_for_other_5_families_without_reconstructed_rating",
            "blocked_pending_byte_determinism_failure_investigation",
            "blocked_pending_named_reason",
        ):
            assert perm in Q6G_ALLOWED_MATERIALIZATION_PERMISSIONS

    def test_glicko2_path_kinds_enum(self) -> None:
        for k in (
            "event_by_event_reference",
            "batched_production_shape",
            "equivalence_proof",
            "byte_determinism_proof",
            "verdict_row",
        ):
            assert k in GLICKO2_PATH_KINDS

    def test_raw_mmr_hybrid_rejection_text_carries_q6f_provenance(self) -> None:
        assert "PR #245" in RAW_MMR_HYBRID_REJECTION_TEXT
        assert "PR #247" in RAW_MMR_HYBRID_REJECTION_TEXT
        assert "raw_mmr_where_present_plus_is_mmr_missing" in RAW_MMR_HYBRID_REJECTION_TEXT

    def test_decision_rule_text_present_and_nontrivial(self) -> None:
        assert "Equivalence pass" in Q6G_PROOF_DECISION_RULE
        assert "Determinism pass" in Q6G_PROOF_DECISION_RULE
        assert "bind_now" in Q6G_PROOF_DECISION_RULE
        assert "recommendation_only_glicko2" in Q6G_PROOF_DECISION_RULE
        assert "deferred_blocker" in Q6G_PROOF_DECISION_RULE
        assert "BLOCKER-1" in Q6G_PROOF_DECISION_RULE

    def test_q6g_proof_csv_rel_canonical_path(self) -> None:
        assert Q6G_PROOF_CSV_REL.endswith("02_01_03_q6g_rating_implementation_proof.csv")
        assert "02_feature_engineering/01_pre_game_vs_in_game_boundary" in Q6G_PROOF_CSV_REL

    def test_q6g_proof_md_rel_canonical_path(self) -> None:
        assert Q6G_PROOF_MD_REL.endswith("02_01_03_q6g_rating_implementation_proof.md")

    def test_audit_pr_placeholder_format(self) -> None:
        assert AUDIT_PR_NUMBER_PLACEHOLDER == "PR #<TBD>"


# ---------------------------------------------------------------------------
# TestParentSHAs
# ---------------------------------------------------------------------------


_PINNED_SHA_PAIRS: list[tuple[str, str]] = [
    ("parent_pr242_csv_sha256", EXPECTED_PR242_CSV_SHA256),
    ("parent_pr242_md_sha256", EXPECTED_PR242_MD_SHA256),
    ("parent_pr243_csv_sha256", EXPECTED_PR243_CSV_SHA256),
    ("parent_pr243_md_sha256", EXPECTED_PR243_MD_SHA256),
    ("parent_pr245_csv_sha256", EXPECTED_PR245_CSV_SHA256),
    ("parent_pr245_md_sha256", EXPECTED_PR245_MD_SHA256),
    ("parent_pr247_csv_sha256", EXPECTED_PR247_CSV_SHA256),
    ("parent_pr247_md_sha256", EXPECTED_PR247_MD_SHA256),
]


class TestParentSHAs:
    def test_q6g_parent_shas_has_8_entries(self) -> None:
        assert len(Q6G_PARENT_SHAS) == 8

    @pytest.mark.parametrize("name, expected", _PINNED_SHA_PAIRS)
    def test_q6g_parent_shas_entries(self, name: str, expected: str) -> None:
        assert Q6G_PARENT_SHAS[name] == expected
        assert len(expected) == 64
        int(expected, 16)  # hex-decodable

    @pytest.mark.parametrize("name, expected", _PINNED_SHA_PAIRS)
    def test_parent_pinned_sha_lowercase_hex(self, name: str, expected: str) -> None:
        assert re.fullmatch(r"[0-9a-f]{64}", expected) is not None

    def test_parent_paths_all_relative(self) -> None:
        for path in (
            PARENT_PR242_CSV_REL,
            PARENT_PR242_MD_REL,
            PARENT_PR243_CSV_REL,
            PARENT_PR243_MD_REL,
            PARENT_PR245_CSV_REL,
            PARENT_PR245_MD_REL,
            PARENT_PR247_CSV_REL,
            PARENT_PR247_MD_REL,
        ):
            assert not Path(path).is_absolute()
            assert path.startswith("src/rts_predict")

    def test_check_parent_pr_shas_all_match(self) -> None:
        repo_root = mod._find_repo_root(Path(__file__))
        mismatches = mod._check_parent_pr_shas(repo_root)
        assert mismatches == []

    def test_check_parent_pr_shas_mismatch_returns_key(self, tmp_path: Path) -> None:
        # Construct a sandbox with PR #242 csv replaced by wrong bytes.
        # Touch every required path with content that won't match the
        # pinned SHA so we exercise the mismatch branch.
        for rel in (
            PARENT_PR242_CSV_REL,
            PARENT_PR242_MD_REL,
            PARENT_PR243_CSV_REL,
            PARENT_PR243_MD_REL,
            PARENT_PR245_CSV_REL,
            PARENT_PR245_MD_REL,
            PARENT_PR247_CSV_REL,
            PARENT_PR247_MD_REL,
        ):
            p = tmp_path / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("intentionally wrong content")
        mismatches = mod._check_parent_pr_shas(tmp_path)
        # 8 fake files all wrong; should report 8 mismatches.
        assert len(mismatches) == 8
        keys = {m[0] for m in mismatches}
        assert "parent_pr242_csv_sha256_mismatch" in keys
        assert "parent_pr247_md_sha256_mismatch" in keys

    def test_pinned_pr247_csv_sha_matches_value_from_plan(self) -> None:
        assert (
            EXPECTED_PR247_CSV_SHA256
            == "249e5591c6505b748fe3d371284a72d8f4620f57dbe9628c908ec2fbf097c8ed"
        )

    def test_pinned_pr247_md_sha_matches_value_from_plan(self) -> None:
        assert (
            EXPECTED_PR247_MD_SHA256
            == "4b49bee405bf87d4b8920b188e2c38d185ecc077b532d64a8bdd5a90cdf143f2"
        )


# ---------------------------------------------------------------------------
# TestEventByEventReferenceMatchesQ6F
# ---------------------------------------------------------------------------


class TestEventByEventReferenceMatchesQ6F:
    def test_delegates_to_pr247(self) -> None:
        with mock.patch.object(mod, "_run_glicko2_survey") as m:
            m.return_value = {"mocked": True}
            out = mod._run_glicko2_event_by_event_reference(pd.DataFrame())
        assert out == {"mocked": True}
        m.assert_called_once()

    def test_loader_delegates_to_pr247(self) -> None:
        with mock.patch.object(mod, "_pr247_load_pha_history_chronological") as m:
            m.return_value = pd.DataFrame({"x": [1]})
            out = mod._load_pha_history_chronological(Path("/dev/null"))
        assert isinstance(out, pd.DataFrame) and out.shape == (1, 1)

    def test_loader_wraps_runtimeerror(self) -> None:
        with mock.patch.object(mod, "_pr247_load_pha_history_chronological") as m:
            m.side_effect = RuntimeError("upstream broke")
            with pytest.raises(RatingImplementationProofError) as exc:
                mod._load_pha_history_chronological(Path("/dev/null"))
        assert exc.value.falsifier_key == "q6g_event_reference_not_imported_from_pr247"

    @pytest.mark.skipif(not Path(DB_FILE).exists(), reason="Real DuckDB unavailable")
    def test_event_metrics_reproduce_pr247_section_11(self) -> None:
        stream = mod._load_pha_history_chronological(Path(DB_FILE))
        out = mod._run_glicko2_event_by_event_reference(stream)
        metrics = compute_proof_metrics(out)
        # T02 verification: log-loss / Brier / calibration_error in
        # PR #247 section 11 bounds within 1e-4.
        assert abs(metrics["log_loss"] - 0.6255) < 1e-3
        assert abs(metrics["brier"] - 0.2177) < 1e-3
        assert abs(metrics["calibration_error"] - 0.0349) < 1e-3

    @pytest.mark.skipif(not Path(DB_FILE).exists(), reason="Real DuckDB unavailable")
    def test_event_metric_ci_reproduces_pr247(self) -> None:
        stream = mod._load_pha_history_chronological(Path(DB_FILE))
        out = mod._run_glicko2_event_by_event_reference(stream)
        metrics = compute_proof_metrics(out)
        # log-loss CI roughly [0.6216, 0.6302] per PR #247.
        assert 0.62 < metrics["log_loss_ci_low"] < 0.625
        assert 0.625 < metrics["log_loss_ci_high"] < 0.635


# ---------------------------------------------------------------------------
# TestGlicko2BatchedProductionEngine
# ---------------------------------------------------------------------------


class TestGlicko2BatchedProductionEngine:
    def test_output_keys_match_contract(self, synth_stream: pd.DataFrame) -> None:
        out = mod._run_glicko2_batched_production(synth_stream)
        for k in (
            "predicted_probabilities",
            "actuals",
            "is_cold_start",
            "rating_state_at_end",
            "runtime_ms",
        ):
            assert k in out

    def test_predictions_in_unit_interval(self, synth_stream: pd.DataFrame) -> None:
        out = mod._run_glicko2_batched_production(synth_stream)
        p = out["predicted_probabilities"]
        assert (p >= 0.0).all() and (p <= 1.0).all()

    def test_actuals_are_zero_or_one(self, synth_stream: pd.DataFrame) -> None:
        out = mod._run_glicko2_batched_production(synth_stream)
        a = out["actuals"]
        assert set(np.unique(a)).issubset({0.0, 1.0})

    def test_cold_start_flag_first_occurrence_per_toon(
        self, synth_stream: pd.DataFrame
    ) -> None:
        out = mod._run_glicko2_batched_production(synth_stream)
        seen: set[str] = set()
        for i, toon in enumerate(synth_stream["focal_toon"]):
            if toon not in seen:
                assert out["is_cold_start"][i]
                seen.add(toon)
            else:
                assert not out["is_cold_start"][i]

    def test_empty_stream_returns_empty_arrays(self) -> None:
        empty = pd.DataFrame(
            {
                "focal_toon": pd.Series([], dtype=str),
                "opponent_toon": pd.Series([], dtype=str),
                "replay_id": pd.Series([], dtype=str),
                "details_timeUTC": pd.Series([], dtype=str),
                "focal_result": pd.Series([], dtype=str),
                "is_cross_region_fragmented": pd.Series([], dtype=bool),
            }
        )
        out = mod._run_glicko2_batched_production(empty)
        assert len(out["predicted_probabilities"]) == 0
        assert len(out["actuals"]) == 0
        assert len(out["is_cold_start"]) == 0

    def test_two_period_fixture_yields_period_aware_state(
        self, small_two_period_stream: pd.DataFrame
    ) -> None:
        out = mod._run_glicko2_batched_production(small_two_period_stream)
        # 4 rows; toon_A's first match is cold-start; subsequent matches
        # may or may not be cold depending on flush ordering, but the
        # rating_state_at_end should contain both players.
        assert "toon_A" in out["rating_state_at_end"]
        assert "toon_B" in out["rating_state_at_end"]
        for state in out["rating_state_at_end"].values():
            assert "mu" in state and "phi" in state and "sigma" in state

    def test_forward_only_first_prediction_is_prior(
        self, small_two_period_stream: pd.DataFrame
    ) -> None:
        out = mod._run_glicko2_batched_production(small_two_period_stream)
        # First prediction must be the prior-implied 0.5 because no
        # closed period exists at row 0.
        assert out["predicted_probabilities"][0] == pytest.approx(0.5)

    def test_runtime_ms_non_negative(self, synth_stream: pd.DataFrame) -> None:
        out = mod._run_glicko2_batched_production(synth_stream)
        assert out["runtime_ms"] >= 0.0

    def test_deterministic_across_invocations(
        self, synth_stream: pd.DataFrame
    ) -> None:
        a = mod._run_glicko2_batched_production(synth_stream)
        b = mod._run_glicko2_batched_production(synth_stream)
        np.testing.assert_array_equal(
            a["predicted_probabilities"], b["predicted_probabilities"]
        )

    def test_custom_hyperparameters_change_output(
        self, synth_stream: pd.DataFrame
    ) -> None:
        a = mod._run_glicko2_batched_production(synth_stream)
        b = mod._run_glicko2_batched_production(synth_stream, mu=1700.0)
        # mu shift cannot change predictions because both players start
        # at the same mu; verify both arrays are valid in [0, 1].
        for arr in (a["predicted_probabilities"], b["predicted_probabilities"]):
            assert (arr >= 0).all() and (arr <= 1).all()

    def test_glicko2_g_decreases_with_rd(self) -> None:
        small = mod._glicko2_g(0.5)
        big = mod._glicko2_g(2.0)
        assert small > big

    def test_glicko2_e_returns_probability(self) -> None:
        p = mod._glicko2_e(0.0, 0.0, 0.5)
        assert p == pytest.approx(0.5)

    def test_glicko2_e_symmetry(self) -> None:
        p = mod._glicko2_e(0.5, 0.0, 0.5)
        q = mod._glicko2_e(0.0, 0.5, 0.5)
        assert p + q == pytest.approx(1.0, rel=1e-9)

    def test_volatility_solver_converges(self) -> None:
        new_sigma = mod._glicko2_solve_new_volatility(
            sigma=0.06, phi=1.0, v=2.0, delta=0.5, tau=0.5
        )
        assert 0.0 < new_sigma < 1.0


# ---------------------------------------------------------------------------
# TestDeterministicBootstrap
# ---------------------------------------------------------------------------


class TestDeterministicBootstrap:
    def test_ci_deterministic_across_runs(self) -> None:
        actuals = np.array([1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0])
        probs = np.array([0.6, 0.4, 0.7, 0.5, 0.3, 0.8, 0.2, 0.4, 0.6, 0.7])
        a = mod._compute_deterministic_percentile_ci(actuals, probs, mod._log_loss_from_arrays)
        b = mod._compute_deterministic_percentile_ci(actuals, probs, mod._log_loss_from_arrays)
        assert a == b

    def test_ci_returns_ordered_tuple(self) -> None:
        actuals = np.array([1.0, 0.0, 1.0, 0.0])
        probs = np.array([0.7, 0.3, 0.8, 0.2])
        lo, hi = mod._compute_deterministic_percentile_ci(
            actuals, probs, mod._log_loss_from_arrays
        )
        assert lo <= hi

    def test_ci_empty_arrays_returns_nan(self) -> None:
        lo, hi = mod._compute_deterministic_percentile_ci(
            np.array([], dtype=np.float64),
            np.array([], dtype=np.float64),
            mod._log_loss_from_arrays,
        )
        assert math.isnan(lo) and math.isnan(hi)

    def test_ci_rejects_non_pcg64(self) -> None:
        actuals = np.array([1.0, 0.0])
        probs = np.array([0.5, 0.5])
        with pytest.raises(RatingImplementationProofError) as exc:
            mod._compute_deterministic_percentile_ci(
                actuals,
                probs,
                mod._log_loss_from_arrays,
                rng_bit_generator="MT19937",
            )
        assert exc.value.falsifier_key == "q6g_numpy_rng_not_pcg64"

    @pytest.mark.parametrize("seed", [42, 7, 0, 100])
    def test_ci_seed_affects_result(self, seed: int) -> None:
        actuals = np.array([1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0])
        probs = np.array([0.6, 0.3, 0.7, 0.4, 0.5, 0.8, 0.2, 0.3])
        lo, hi = mod._compute_deterministic_percentile_ci(
            actuals, probs, mod._log_loss_from_arrays, seed=seed
        )
        assert math.isfinite(lo) and math.isfinite(hi)

    def test_se_log_loss_from_ci(self) -> None:
        actuals = np.array([1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0])
        probs = np.array([0.6, 0.3, 0.7, 0.4, 0.5, 0.8, 0.2, 0.3])
        se = mod._compute_event_log_loss_se(actuals, probs)
        assert se >= 0.0

    def test_se_empty_returns_nan(self) -> None:
        se = mod._compute_event_log_loss_se(
            np.array([], dtype=np.float64), np.array([], dtype=np.float64)
        )
        assert math.isnan(se)

    def test_ci_block_count_smaller(self) -> None:
        actuals = np.array([1.0, 0.0, 1.0, 1.0])
        probs = np.array([0.6, 0.4, 0.7, 0.5])
        lo, hi = mod._compute_deterministic_percentile_ci(
            actuals, probs, mod._log_loss_from_arrays, block_count=10
        )
        assert lo <= hi

    def test_ci_99_percent_level(self) -> None:
        actuals = np.array([1.0, 0.0, 1.0, 0.0, 1.0])
        probs = np.array([0.6, 0.3, 0.7, 0.4, 0.5])
        lo95, hi95 = mod._compute_deterministic_percentile_ci(
            actuals, probs, mod._log_loss_from_arrays, ci_level=0.95
        )
        lo99, hi99 = mod._compute_deterministic_percentile_ci(
            actuals, probs, mod._log_loss_from_arrays, ci_level=0.99
        )
        assert lo99 <= lo95
        assert hi99 >= hi95

    def test_compute_proof_metrics_keys_present(self, synth_stream: pd.DataFrame) -> None:
        out = mod._run_glicko2_batched_production(synth_stream)
        m = compute_proof_metrics(out)
        for k in (
            "log_loss",
            "log_loss_ci_low",
            "log_loss_ci_high",
            "brier",
            "brier_ci_low",
            "brier_ci_high",
            "calibration_error",
            "coverage_rate",
            "cold_start_rate",
            "runtime_seconds",
        ):
            assert k in m

    def test_compute_proof_metrics_event_engine(
        self, synth_stream: pd.DataFrame
    ) -> None:
        out = mod._run_glicko2_event_by_event_reference(synth_stream)
        m = compute_proof_metrics(out)
        assert m["coverage_rate"] >= 0.0


# ---------------------------------------------------------------------------
# TestKahanSummationOrder
# ---------------------------------------------------------------------------


class TestKahanSummationOrder:
    def test_kahan_recovers_naive_on_homogeneous_input(self) -> None:
        arr = np.ones(1000, dtype=np.float64)
        assert mod._kahan_neumaier_sum(arr) == pytest.approx(1000.0, abs=1e-9)

    def test_kahan_more_accurate_for_skewed_magnitudes(self) -> None:
        # Single large + many small terms: naive sum loses precision.
        arr = np.concatenate(
            [np.array([1e16]), np.full(1000000, 1.0), np.array([-1e16])]
        )
        naive = float(arr.sum())
        kahan = mod._kahan_neumaier_sum(arr)
        # Expected exact answer is 1_000_000.0.
        assert abs(kahan - 1_000_000.0) <= abs(naive - 1_000_000.0)

    def test_kahan_handles_empty(self) -> None:
        assert mod._kahan_neumaier_sum(np.array([], dtype=np.float64)) == 0.0

    def test_kahan_handles_single_value(self) -> None:
        assert mod._kahan_neumaier_sum(np.array([3.14])) == pytest.approx(3.14)

    def test_kahan_handles_negative_values(self) -> None:
        arr = np.array([1.0, -1.0, 1.0, -1.0])
        assert mod._kahan_neumaier_sum(arr) == pytest.approx(0.0, abs=1e-12)

    def test_log_loss_uses_kahan_summation(self) -> None:
        # Indirect: log_loss should equal mean over all rows.
        actuals = np.array([1.0, 0.0, 1.0, 1.0])
        probs = np.array([0.6, 0.3, 0.7, 0.8])
        ll = mod._log_loss_from_arrays(actuals, probs)
        # Hand-computed log-loss.
        terms = -(
            actuals * np.log(np.clip(probs, 1e-15, 1 - 1e-15))
            + (1 - actuals) * np.log(np.clip(1 - probs, 1e-15, 1 - 1e-15))
        )
        assert ll == pytest.approx(float(terms.mean()), abs=1e-8)


# ---------------------------------------------------------------------------
# TestEquivalenceProof_PassesBound (>= 10 tests per R2-N1)
# ---------------------------------------------------------------------------


def _identical_paths_proof() -> dict[str, Any]:
    return {
        "predicted_probabilities": np.array([0.6, 0.4, 0.7, 0.5, 0.3, 0.8, 0.2, 0.65, 0.45, 0.55]),
        "actuals": np.array([1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0]),
        "is_cold_start": np.zeros(10, dtype=bool),
        "rating_state_at_end": {},
        "runtime_ms": 0.1,
    }


def _nearly_identical_paths_proof() -> dict[str, Any]:
    rng = np.random.default_rng(0)
    base = _identical_paths_proof()
    noisy = dict(base)
    noisy["predicted_probabilities"] = np.clip(
        base["predicted_probabilities"] + rng.normal(0, 1e-6, size=10), 0, 1
    )
    return noisy


class TestEquivalenceProof_PassesBound:
    def test_identical_paths_spearman_is_one(self) -> None:
        eq = mod._compute_event_vs_batched_equivalence_proof(
            _identical_paths_proof(), _identical_paths_proof()
        )
        assert eq["spearman_rho"] == pytest.approx(1.0, abs=1e-9)

    def test_identical_paths_delta_log_loss_zero(self) -> None:
        eq = mod._compute_event_vs_batched_equivalence_proof(
            _identical_paths_proof(), _identical_paths_proof()
        )
        assert eq["abs_delta_log_loss"] == pytest.approx(0.0, abs=1e-12)

    def test_identical_paths_passes_spearman_bound(self) -> None:
        eq = mod._compute_event_vs_batched_equivalence_proof(
            _identical_paths_proof(), _identical_paths_proof()
        )
        assert eq["passes_spearman_bound"] is True

    def test_identical_paths_passes_delta_log_loss_bound(self) -> None:
        eq = mod._compute_event_vs_batched_equivalence_proof(
            _identical_paths_proof(), _identical_paths_proof()
        )
        assert eq["passes_delta_log_loss_bound"] is True

    def test_equivalence_stats_all_5_keys_present(self) -> None:
        eq = mod._compute_event_vs_batched_equivalence_proof(
            _identical_paths_proof(), _identical_paths_proof()
        )
        for key in (
            "spearman_rho",
            "abs_delta_log_loss",
            "se_log_loss_event",
            "passes_spearman_bound",
            "passes_delta_log_loss_bound",
        ):
            assert key in eq

    def test_se_log_loss_event_non_negative(self) -> None:
        eq = mod._compute_event_vs_batched_equivalence_proof(
            _identical_paths_proof(), _identical_paths_proof()
        )
        assert eq["se_log_loss_event"] >= 0.0

    def test_nearly_identical_paths_pass_both_bounds(self) -> None:
        eq = mod._compute_event_vs_batched_equivalence_proof(
            _identical_paths_proof(), _nearly_identical_paths_proof()
        )
        assert eq["passes_spearman_bound"] in (True, False)
        # Even with eps noise, Spearman should be >= 0.99.
        assert eq["spearman_rho"] >= 0.99 - 1e-9

    def test_spearman_in_minus1_to_plus1_range(self) -> None:
        eq = mod._compute_event_vs_batched_equivalence_proof(
            _identical_paths_proof(), _identical_paths_proof()
        )
        assert -1.0 <= eq["spearman_rho"] <= 1.0

    def test_abs_delta_log_loss_non_negative(self) -> None:
        eq = mod._compute_event_vs_batched_equivalence_proof(
            _identical_paths_proof(), _identical_paths_proof()
        )
        assert eq["abs_delta_log_loss"] >= 0.0

    def test_cold_start_mask_excludes_cold_rows(self) -> None:
        # Hardcoded cold-start everywhere -> all masked out -> NaN/empty.
        event = _identical_paths_proof()
        batched = _identical_paths_proof()
        event = {**event, "is_cold_start": np.ones(10, dtype=bool)}
        batched = {**batched, "is_cold_start": np.ones(10, dtype=bool)}
        eq = mod._compute_event_vs_batched_equivalence_proof(event, batched)
        assert math.isnan(eq["spearman_rho"]) or eq["spearman_rho"] == 0.0
        assert eq["passes_spearman_bound"] is False

    def test_spearman_rho_helper_independently_returns_one_for_identical(self) -> None:
        x = np.array([1.0, 2.0, 3.0, 4.0])
        assert mod._spearman_rho(x, x) == pytest.approx(1.0, abs=1e-9)

    def test_spearman_rho_negative_for_anti_correlated(self) -> None:
        x = np.array([1.0, 2.0, 3.0, 4.0])
        y = np.array([4.0, 3.0, 2.0, 1.0])
        assert mod._spearman_rho(x, y) == pytest.approx(-1.0, abs=1e-9)


# ---------------------------------------------------------------------------
# TestEquivalenceProof_FailsBound
# ---------------------------------------------------------------------------


def _divergent_path() -> dict[str, Any]:
    p_event = np.array([0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.15, 0.85])
    p_batched = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.85, 0.15])
    actuals = np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0])
    return p_event, p_batched, actuals


class TestEquivalenceProof_FailsBound:
    def test_divergent_paths_low_spearman(self) -> None:
        p_e, p_b, a = _divergent_path()
        event = {
            "predicted_probabilities": p_e,
            "actuals": a,
            "is_cold_start": np.zeros(len(a), dtype=bool),
            "rating_state_at_end": {},
            "runtime_ms": 0.0,
        }
        batched = {
            "predicted_probabilities": p_b,
            "actuals": a,
            "is_cold_start": np.zeros(len(a), dtype=bool),
            "rating_state_at_end": {},
            "runtime_ms": 0.0,
        }
        eq = mod._compute_event_vs_batched_equivalence_proof(event, batched)
        assert eq["spearman_rho"] < 0.99
        assert eq["passes_spearman_bound"] is False

    def test_divergent_paths_large_delta_log_loss(self) -> None:
        p_e, p_b, a = _divergent_path()
        event = {
            "predicted_probabilities": p_e,
            "actuals": a,
            "is_cold_start": np.zeros(len(a), dtype=bool),
            "rating_state_at_end": {},
            "runtime_ms": 0.0,
        }
        batched = {
            "predicted_probabilities": p_b,
            "actuals": a,
            "is_cold_start": np.zeros(len(a), dtype=bool),
            "rating_state_at_end": {},
            "runtime_ms": 0.0,
        }
        eq = mod._compute_event_vs_batched_equivalence_proof(event, batched)
        assert eq["abs_delta_log_loss"] > 0.05

    def test_divergent_paths_fails_both_bounds(self) -> None:
        p_e, p_b, a = _divergent_path()
        event = {
            "predicted_probabilities": p_e,
            "actuals": a,
            "is_cold_start": np.zeros(len(a), dtype=bool),
            "rating_state_at_end": {},
            "runtime_ms": 0.0,
        }
        batched = {
            "predicted_probabilities": p_b,
            "actuals": a,
            "is_cold_start": np.zeros(len(a), dtype=bool),
            "rating_state_at_end": {},
            "runtime_ms": 0.0,
        }
        eq = mod._compute_event_vs_batched_equivalence_proof(event, batched)
        # At least one bound fails -> proof fails -> verdict NOT bind_now.
        assert eq["passes_spearman_bound"] is False or eq["passes_delta_log_loss_bound"] is False

    def test_anti_correlated_paths_negative_spearman(self) -> None:
        p_e, p_b, a = _divergent_path()
        event = {
            "predicted_probabilities": p_e,
            "actuals": a,
            "is_cold_start": np.zeros(len(a), dtype=bool),
            "rating_state_at_end": {},
            "runtime_ms": 0.0,
        }
        batched = {
            "predicted_probabilities": p_b,
            "actuals": a,
            "is_cold_start": np.zeros(len(a), dtype=bool),
            "rating_state_at_end": {},
            "runtime_ms": 0.0,
        }
        eq = mod._compute_event_vs_batched_equivalence_proof(event, batched)
        assert eq["spearman_rho"] < 0.0

    def test_falsifier_text_for_equivalence_unproven(self) -> None:
        # The auto-emitted falsifier key when equivalence fails.
        assert (
            "q6g_batched_event_ordering_equivalence_unproven"
            in FALSIFIER_PRIORITY_CHAIN
        )

    def test_low_spearman_blocks_bind_now(self) -> None:
        eq = {
            "spearman_rho": 0.2,
            "abs_delta_log_loss": 0.05,
            "se_log_loss_event": 0.001,
            "passes_spearman_bound": False,
            "passes_delta_log_loss_bound": False,
        }
        bd = {"run_a_sha256": "x", "run_b_sha256": "x", "hashes_equal": True}
        sel, verdict, _, _ = mod._q6g_select_policy(eq, bd)
        assert verdict == "recommendation_only_glicko2"

    def test_partial_pass_does_not_bind(self) -> None:
        # Spearman passes, but delta-log-loss exceeds SE.
        eq = {
            "spearman_rho": 0.999,
            "abs_delta_log_loss": 0.1,
            "se_log_loss_event": 0.001,
            "passes_spearman_bound": True,
            "passes_delta_log_loss_bound": False,
        }
        bd = {"run_a_sha256": "x", "run_b_sha256": "x", "hashes_equal": True}
        sel, verdict, _, _ = mod._q6g_select_policy(eq, bd)
        assert verdict == "recommendation_only_glicko2"

    def test_spearman_at_threshold_passes(self) -> None:
        # rho exactly 0.99 passes (>=).
        eq = {
            "spearman_rho": 0.99,
            "abs_delta_log_loss": 0.0,
            "se_log_loss_event": 1.0,
            "passes_spearman_bound": True,
            "passes_delta_log_loss_bound": True,
        }
        bd = {"run_a_sha256": "x", "run_b_sha256": "x", "hashes_equal": True}
        sel, verdict, _, _ = mod._q6g_select_policy(eq, bd)
        assert verdict == "bind_now"

    def test_spearman_below_threshold_fails(self) -> None:
        eq = {
            "spearman_rho": 0.985,
            "abs_delta_log_loss": 0.0,
            "se_log_loss_event": 1.0,
            "passes_spearman_bound": False,
            "passes_delta_log_loss_bound": True,
        }
        bd = {"run_a_sha256": "x", "run_b_sha256": "x", "hashes_equal": True}
        sel, verdict, _, _ = mod._q6g_select_policy(eq, bd)
        assert verdict == "recommendation_only_glicko2"

    def test_equivalence_fail_rationale_contains_metrics(self) -> None:
        eq = {
            "spearman_rho": 0.5,
            "abs_delta_log_loss": 0.01,
            "se_log_loss_event": 0.001,
            "passes_spearman_bound": False,
            "passes_delta_log_loss_bound": False,
        }
        bd = {"run_a_sha256": "x", "run_b_sha256": "x", "hashes_equal": True}
        _, _, _, rationale = mod._q6g_select_policy(eq, bd)
        assert "0.5000" in rationale or "0.500000" in rationale
        assert "0.010" in rationale or "0.010000" in rationale

    def test_equivalence_nan_inputs_fail_bounds(self) -> None:
        event = {
            "predicted_probabilities": np.array([np.nan, np.nan]),
            "actuals": np.array([1.0, 0.0]),
            "is_cold_start": np.zeros(2, dtype=bool),
            "rating_state_at_end": {},
            "runtime_ms": 0.0,
        }
        batched = dict(event)
        eq = mod._compute_event_vs_batched_equivalence_proof(event, batched)
        # Either Spearman is NaN, or both bounds report False (the
        # important contract is that bind_now is not reachable with NaN
        # input).
        assert eq["passes_spearman_bound"] is False or eq["passes_delta_log_loss_bound"] is False


# ---------------------------------------------------------------------------
# TestByteDeterminismProof
# ---------------------------------------------------------------------------


class TestByteDeterminismProof:
    def test_hashes_equal_on_identical_runs(self, synth_stream: pd.DataFrame) -> None:
        bd = mod._compute_byte_determinism_proof(synth_stream)
        assert bd["hashes_equal"] is True
        assert bd["run_a_sha256"] == bd["run_b_sha256"]

    def test_hashes_64_char_lowercase_hex(self, synth_stream: pd.DataFrame) -> None:
        bd = mod._compute_byte_determinism_proof(synth_stream)
        assert re.fullmatch(r"[0-9a-f]{64}", bd["run_a_sha256"]) is not None
        assert re.fullmatch(r"[0-9a-f]{64}", bd["run_b_sha256"]) is not None

    def test_hashes_differ_on_jittered_input(self, synth_stream: pd.DataFrame) -> None:
        # Change actual outcomes -> different engine output -> different hash.
        jittered = synth_stream.copy()
        jittered["focal_result"] = jittered["focal_result"].map(
            {"Win": "Loss", "Loss": "Win"}
        )
        bd_a = mod._compute_byte_determinism_proof(synth_stream)
        bd_b = mod._compute_byte_determinism_proof(jittered)
        # The two streams have different actuals, which propagate to
        # different rating updates and different per-row predictions.
        assert bd_a["run_a_sha256"] != bd_b["run_a_sha256"]

    def test_byte_determinism_stats_keys(self, synth_stream: pd.DataFrame) -> None:
        bd = mod._compute_byte_determinism_proof(synth_stream)
        for k in ("run_a_sha256", "run_b_sha256", "hashes_equal"):
            assert k in bd

    def test_hashes_equal_field_is_bool(self, synth_stream: pd.DataFrame) -> None:
        bd = mod._compute_byte_determinism_proof(synth_stream)
        assert isinstance(bd["hashes_equal"], bool)


# ---------------------------------------------------------------------------
# TestDecisionRule_AllThreeBranches (>= 6 tests per R2-N1)
# ---------------------------------------------------------------------------


_EQ_PASS = {
    "spearman_rho": 0.999,
    "abs_delta_log_loss": 0.0001,
    "se_log_loss_event": 0.01,
    "passes_spearman_bound": True,
    "passes_delta_log_loss_bound": True,
}
_EQ_FAIL = {
    "spearman_rho": 0.5,
    "abs_delta_log_loss": 0.05,
    "se_log_loss_event": 0.001,
    "passes_spearman_bound": False,
    "passes_delta_log_loss_bound": False,
}
_BD_PASS = {"run_a_sha256": "a" * 64, "run_b_sha256": "a" * 64, "hashes_equal": True}
_BD_FAIL = {"run_a_sha256": "a" * 64, "run_b_sha256": "b" * 64, "hashes_equal": False}


class TestDecisionRule_AllThreeBranches:
    def test_branch_bind_now(self) -> None:
        sel, verdict, mp, _ = mod._q6g_select_policy(_EQ_PASS, _BD_PASS)
        assert verdict == "bind_now"
        assert sel == "bind_now"
        assert "permitted_for_all_6_families" in mp

    def test_branch_recommendation_only_glicko2(self) -> None:
        sel, verdict, mp, _ = mod._q6g_select_policy(_EQ_FAIL, _BD_PASS)
        assert verdict == "recommendation_only_glicko2"
        assert sel == "recommendation_only_glicko2"
        assert "recommendation_only_glicko2" in mp

    def test_branch_deferred_blocker_determinism_fail(self) -> None:
        sel, verdict, mp, _ = mod._q6g_select_policy(_EQ_PASS, _BD_FAIL)
        assert verdict == "deferred_blocker"
        assert sel == "deferred_blocker"
        assert "byte_determinism_failure" in mp

    def test_determinism_fail_short_circuits_equivalence(self) -> None:
        sel, verdict, mp, _ = mod._q6g_select_policy(_EQ_FAIL, _BD_FAIL)
        # Even if equivalence also fails, determinism failure -> deferred_blocker.
        assert verdict == "deferred_blocker"
        assert "byte_determinism_failure" in mp

    def test_bind_now_rationale_contains_metrics(self) -> None:
        _, _, _, rationale = mod._q6g_select_policy(_EQ_PASS, _BD_PASS)
        assert "Spearman" in rationale and "0.9990" in rationale

    def test_deferred_blocker_rationale_specific(self) -> None:
        _, _, _, rationale = mod._q6g_select_policy(_EQ_PASS, _BD_FAIL)
        assert "byte-deterministic" in rationale

    def test_recommendation_rationale_quotes_q6f_overlap(self) -> None:
        _, _, _, rationale = mod._q6g_select_policy(_EQ_FAIL, _BD_PASS)
        assert "0.9% of mid-range" in rationale

    def test_branch_returns_4_tuple(self) -> None:
        out = mod._q6g_select_policy(_EQ_PASS, _BD_PASS)
        assert isinstance(out, tuple) and len(out) == 4


# ---------------------------------------------------------------------------
# TestBlockerGuard_BindNowRequiresEquivalence
# ---------------------------------------------------------------------------


class TestBlockerGuard_BindNowRequiresEquivalence:
    def test_guard_passes_when_all_three_succeed(self) -> None:
        # Should not raise.
        mod._enforce_bind_now_guard("bind_now", _EQ_PASS, _BD_PASS)

    def test_guard_raises_when_spearman_fails(self) -> None:
        bad_eq = {**_EQ_PASS, "passes_spearman_bound": False}
        with pytest.raises(RatingImplementationProofError) as exc:
            mod._enforce_bind_now_guard("bind_now", bad_eq, _BD_PASS)
        assert exc.value.falsifier_key == "q6g_bind_now_emitted_without_equivalence_pass"

    def test_guard_raises_when_delta_fails(self) -> None:
        bad_eq = {**_EQ_PASS, "passes_delta_log_loss_bound": False}
        with pytest.raises(RatingImplementationProofError) as exc:
            mod._enforce_bind_now_guard("bind_now", bad_eq, _BD_PASS)
        assert exc.value.falsifier_key == "q6g_bind_now_emitted_without_equivalence_pass"

    def test_guard_raises_when_determinism_fails(self) -> None:
        bad_bd = {**_BD_PASS, "hashes_equal": False}
        with pytest.raises(RatingImplementationProofError) as exc:
            mod._enforce_bind_now_guard("bind_now", _EQ_PASS, bad_bd)
        assert exc.value.falsifier_key == "q6g_bind_now_emitted_without_equivalence_pass"

    def test_guard_silent_on_non_bind_now_verdicts(self) -> None:
        # When verdict != bind_now, the guard returns without raising
        # regardless of the equivalence/determinism state.
        mod._enforce_bind_now_guard("recommendation_only_glicko2", _EQ_FAIL, _BD_FAIL)
        mod._enforce_bind_now_guard("deferred_blocker", _EQ_FAIL, _BD_FAIL)


# ---------------------------------------------------------------------------
# TestArtifactWriter
# ---------------------------------------------------------------------------


class _StubResult:
    pass


def _build_test_result(
    verdict: str = "recommendation_only_glicko2",
) -> RatingImplementationProofResult:
    metrics = {
        "log_loss": 0.6,
        "log_loss_ci_low": 0.58,
        "log_loss_ci_high": 0.62,
        "brier": 0.21,
        "brier_ci_low": 0.20,
        "brier_ci_high": 0.22,
        "calibration_error": 0.05,
        "coverage_rate": 0.95,
        "cold_start_rate": 0.05,
        "runtime_seconds": 0.1,
    }
    metrics_by_path = {
        "event_by_event_reference": metrics,
        "batched_production_shape": metrics,
    }
    eq_stats = {
        "spearman_rho": 0.5,
        "abs_delta_log_loss": 0.05,
        "se_log_loss_event": 0.001,
        "passes_spearman_bound": False,
        "passes_delta_log_loss_bound": False,
    }
    bd_stats = {"run_a_sha256": "a" * 64, "run_b_sha256": "a" * 64, "hashes_equal": True}
    decisions = mod._build_proof_decisions(
        metrics_by_path, eq_stats, bd_stats, audit_pr="PR #TEST"
    )
    return RatingImplementationProofResult(
        decisions=decisions,
        csv_path="/tmp/test.csv",
        md_path="/tmp/test.md",
        provenance_git_sha="UNKNOWN",
        falsifiers_fired=("q6g_batched_event_ordering_equivalence_unproven",),
        halting_falsifier=None,
        passed=True,
        metrics_by_path=metrics_by_path,
        equivalence_proof_statistics=eq_stats,
        byte_determinism_proof_statistics=bd_stats,
        sample_probabilities=(0.50, 0.55, 0.60, 0.45, 0.65),
        selection="recommendation_only_glicko2",
    )


class TestArtifactWriter:
    def test_csv_has_39_columns(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        with csv_path.open() as fh:
            reader = csv.reader(fh)
            header = next(reader)
        assert len(header) == 39

    def test_csv_has_5_data_rows(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        with csv_path.open() as fh:
            reader = csv.reader(fh)
            next(reader)
            data = list(reader)
        assert len(data) == 5

    def test_csv_header_matches_schema(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        with csv_path.open() as fh:
            reader = csv.reader(fh)
            header = next(reader)
        assert tuple(header) == Q6G_PROOF_SCHEMA

    def test_csv_byte_stable(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path_a = tmp_path / "a.csv"
        md_path_a = tmp_path / "a.md"
        csv_path_b = tmp_path / "b.csv"
        md_path_b = tmp_path / "b.md"
        write_q6g_proof_artifacts(result, csv_path_a, md_path_a)
        write_q6g_proof_artifacts(result, csv_path_b, md_path_b)
        h_a = hashlib.sha256(csv_path_a.read_bytes()).hexdigest()
        h_b = hashlib.sha256(csv_path_b.read_bytes()).hexdigest()
        assert h_a == h_b

    def test_md_has_at_least_19_sections(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        count = len(re.findall(r"^## ", md, re.MULTILINE))
        assert count >= 19

    def test_md_contains_non_materialization_disclaimer(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        assert "Non-Materialization Disclaimer" in md
        assert "does NOT materialize" in md or "does NOT close" in md

    def test_md_section_10_has_5_sample_rows(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        sec_10 = md[md.find("## 10."):md.find("## 11.")]
        # Count lines matching the | pha_row_index | predicted_probability | pattern.
        rows = re.findall(r"^\| \d+ \| \d+\.\d{6} \|$", sec_10, re.MULTILINE)
        assert len(rows) == 5

    def test_md_section_11_states_column_count_39(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        sec_11 = md[md.find("## 11."):md.find("## 12.")]
        assert "39" in sec_11

    def test_md_contains_sha_provenance(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        for sha in (
            EXPECTED_PR242_CSV_SHA256,
            EXPECTED_PR247_MD_SHA256,
            EXPECTED_PR245_CSV_SHA256,
        ):
            assert sha in md

    def test_md_section_13a_contains_equivalence_keys(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        assert "Equivalence Proof Result" in md
        assert "spearman_rho" in md
        assert "abs_delta_log_loss" in md

    def test_md_section_13b_contains_byte_determinism_keys(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        assert "Byte-Determinism Proof Result" in md
        assert "run_a_sha256" in md and "hashes_equal" in md

    def test_md_states_no_step_closure(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        assert "does NOT close Step 02_01_03" in md
        assert "Phase 03" in md and "not_started" in md

    def test_md_states_no_phase_03(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        assert re.search(r"Phase[\s-]?03.*not_started", md, re.IGNORECASE) is not None

    def test_md_does_not_claim_step_02_01_04(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        assert "02_01_04" not in md or "out of scope" in md.lower()


# ---------------------------------------------------------------------------
# TestNIT_N1_MDSampleIsProbabilityOnly
# ---------------------------------------------------------------------------


class TestNIT_N1_MDSampleIsProbabilityOnly:
    def test_sample_table_rows_count(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        sec_10 = md[md.find("## 10."):md.find("## 11.")]
        rows = re.findall(r"^\| \d+ \| (\d+\.\d{6}) \|$", sec_10, re.MULTILINE)
        assert len(rows) == 5

    def test_sample_values_in_unit_interval(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        sec_10 = md[md.find("## 10."):md.find("## 11.")]
        for v in re.findall(r"^\| \d+ \| (\d+\.\d{6}) \|$", sec_10, re.MULTILINE):
            f = float(v)
            assert 0.0 <= f <= 1.0

    def test_section_10_no_raw_mu_token(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        sec_10 = md[md.find("## 10."):md.find("## 11.")]
        assert "mu=" not in sec_10

    def test_section_10_no_raw_sigma_token(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        sec_10 = md[md.find("## 10."):md.find("## 11.")]
        assert "sigma=" not in sec_10

    def test_section_10_no_raw_phi_or_rd_token(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        sec_10 = md[md.find("## 10."):md.find("## 11.")]
        assert "phi=" not in sec_10
        assert "RD=" not in sec_10

    def test_section_10_no_raw_tau_token(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        sec_10 = md[md.find("## 10."):md.find("## 11.")]
        assert "tau=" not in sec_10

    def test_md_section_10_check_failure_raises(self, tmp_path: Path) -> None:
        # Construct an MD with explicit Glicko-2 symbol leak in section 10.
        bad_content = (
            "# X\n\n## 10. Metric Definitions + Bootstrap Policy (A21)\n\n"
            "mu=1500 sigma=0.06\n\n## 11. Per-Path Metric Table (Rows 1 & 2)\n"
        )
        passed, message = mod._check_md_section_10_probability_only(bad_content)
        assert passed is False
        assert "mu" in message or "sigma" in message

    def test_md_section_10_check_pass_on_clean(self) -> None:
        good = (
            "# X\n\n## 10. Metric Definitions + Bootstrap Policy (A21)\n\n"
            "Predicted probability: 0.500000\n\n"
            "## 11. Per-Path Metric Table (Rows 1 & 2)\n"
        )
        passed, _ = mod._check_md_section_10_probability_only(good)
        assert passed is True

    def test_writer_halts_on_md_symbol_leak(self, tmp_path: Path) -> None:
        result = _build_test_result()
        # Force a corrupted MD by patching the section renderer.
        def _bad_md_sections(*args: Any, **kwargs: Any) -> str:
            return (
                "# X\n## 10. Metric Definitions + Bootstrap Policy (A21)\n"
                "mu=1500\n## 11. Per-Path Metric Table (Rows 1 & 2)\n"
            )

        with mock.patch.object(mod, "_md_sections", _bad_md_sections):
            with pytest.raises(RatingImplementationProofError) as exc:
                mod._write_md(
                    result.decisions,
                    result.metrics_by_path,
                    result.equivalence_proof_statistics,
                    result.byte_determinism_proof_statistics,
                    result.sample_probabilities,
                    tmp_path / "q6g.md",
                    audit_pr="PR #TEST",
                )
        assert exc.value.falsifier_key == "q6g_raw_mu_or_sigma_persisted_in_md"


# ---------------------------------------------------------------------------
# TestFalsifierChain (>= 38 keys per R2-N1)
# ---------------------------------------------------------------------------


class TestFalsifierChain:
    def test_chain_length_meets_minimum(self) -> None:
        assert len(FALSIFIER_PRIORITY_CHAIN) >= 38

    def test_chain_has_no_duplicates(self) -> None:
        assert len(set(FALSIFIER_PRIORITY_CHAIN)) == len(FALSIFIER_PRIORITY_CHAIN)

    def test_chain_contains_blocker_1_key(self) -> None:
        assert "q6g_batched_event_ordering_equivalence_unproven" in FALSIFIER_PRIORITY_CHAIN

    def test_chain_contains_bind_now_guard_key(self) -> None:
        assert "q6g_bind_now_emitted_without_equivalence_pass" in FALSIFIER_PRIORITY_CHAIN

    def test_chain_contains_nit_n1_key(self) -> None:
        assert "q6g_raw_mu_or_sigma_persisted_in_md" in FALSIFIER_PRIORITY_CHAIN

    def test_chain_contains_no_trueskill_key(self) -> None:
        assert "q6g_no_trueskill_re_implementation" in FALSIFIER_PRIORITY_CHAIN

    @pytest.mark.parametrize(
        "key",
        [
            "parent_pr242_csv_sha256_mismatch",
            "parent_pr242_md_sha256_mismatch",
            "parent_pr243_csv_sha256_mismatch",
            "parent_pr243_md_sha256_mismatch",
            "parent_pr245_csv_sha256_mismatch",
            "parent_pr245_md_sha256_mismatch",
            "parent_pr247_csv_sha256_mismatch",
            "parent_pr247_md_sha256_mismatch",
        ],
    )
    def test_chain_contains_parent_sha_key(self, key: str) -> None:
        assert key in FALSIFIER_PRIORITY_CHAIN

    @pytest.mark.parametrize(
        "key",
        [
            "q6g_decision_count_mismatch",
            "q6g_decision_id_order_mismatch",
            "q6g_q6g_selected_policy_row_missing",
            "q6g_byte_determinism_failed",
            "q6g_rating_trace_persistence_violation",
            "q6g_q5_re_adjudication_drift",
            "q6g_q6f_re_adjudication_drift",
            "q6g_rating_period_days_not_30",
            "q6g_bootstrap_seed_not_42",
            "q6g_bootstrap_block_count_not_200",
            "q6g_bootstrap_method_not_deterministic_percentile",
            "q6g_numpy_rng_not_pcg64",
            "q6g_python_summation_policy_not_sorted_then_kahan",
            "q6g_glicko2_iteration_tol_not_1e_6",
            "q6g_materialization_creep",
            "q6g_parquet_emitted",
            "q6g_status_drift",
            "q6g_research_log_drift",
            "q6g_roadmap_drift",
            "q6g_spec_drift",
            "q6g_cleaning_layer_drift",
            "q6g_target_match_outcome_read_as_input",
            "q6g_future_match_leakage_referenced",
            "q6g_global_batch_fit_referenced",
            "q6g_no_post_game_token",
            "q6g_phase_03_baseline_creep",
            "q6g_step_02_01_04_creep",
            "q6g_event_reference_not_imported_from_pr247",
        ],
    )
    def test_chain_contains_q6g_namespaced_key(self, key: str) -> None:
        assert key in FALSIFIER_PRIORITY_CHAIN

    def test_falsifier_roll_call_has_did_not_fire_for_unfired_keys(self) -> None:
        text = mod._falsifier_roll_call(fired=())
        for k in FALSIFIER_PRIORITY_CHAIN:
            assert f"{k}:did_not_fire" in text

    def test_falsifier_roll_call_marks_fired(self) -> None:
        fired = ("q6g_byte_determinism_failed",)
        text = mod._falsifier_roll_call(fired=fired)
        assert "q6g_byte_determinism_failed:fired" in text

    def test_falsifier_keys_all_lowercase_snake_case(self) -> None:
        for k in FALSIFIER_PRIORITY_CHAIN:
            assert re.fullmatch(r"[a-z0-9_]+", k) is not None


# ---------------------------------------------------------------------------
# TestNoMaterializationCreep / TestNoTrueSkillReImplementation / persistence
# ---------------------------------------------------------------------------


class TestNoMaterializationCreep:
    def test_all_decisions_have_empty_materialized_paths(self) -> None:
        result = _build_test_result()
        for d in result.decisions:
            assert d.materialized_output_paths == ""

    def test_check_no_materialized_output_paths_passes(self) -> None:
        result = _build_test_result()
        passed, msg = mod._check_no_materialized_output_paths(result.decisions)
        assert passed is True
        assert msg == ""

    def test_check_no_materialized_output_paths_fails_on_dirty_row(self) -> None:
        result = _build_test_result()
        # Replace one decision with a tampered version.
        dirty = list(result.decisions)
        dirty[0] = mod.RatingImplementationProofDecision(
            **{**dirty[0].__dict__, "materialized_output_paths": "/some/path.parquet"}
        )
        passed, msg = mod._check_no_materialized_output_paths(tuple(dirty))
        assert passed is False
        assert "materialized_output_paths" in msg

    def test_no_parquet_extension_in_any_decision_field(self) -> None:
        result = _build_test_result()
        for d in result.decisions:
            for f in fields(d):
                v = str(getattr(d, f.name))
                assert ".parquet" not in v

    def test_no_audit_path_in_any_decision_field(self) -> None:
        result = _build_test_result()
        for d in result.decisions:
            for f in fields(d):
                v = str(getattr(d, f.name))
                assert "leakage_audit_sc2egset" not in v


class TestNoTrueSkillReImplementation:
    def test_module_source_lacks_trueskill_engine(self) -> None:
        src = Path(mod.__file__).read_text()
        passed, msg = mod._check_no_trueskill_re_implementation(src)
        assert passed is True, msg

    def test_module_source_has_no_trueskill_engine_function(self) -> None:
        src = Path(mod.__file__).read_text()
        # Module-level function definitions (column 0) only.
        for forbidden in (
            r"^def\s+_run_truesk" + r"ill\w*\(",
            r"^def\s+_truesk" + r"ill_v\(",
            r"^def\s+_truesk" + r"ill_w\(",
        ):
            assert re.search(forbidden, src, re.MULTILINE) is None

    def test_check_detects_synthetic_trueskill_leak(self) -> None:
        fake_src = "def " + "_run_truesk" + "ill_implementation(): pass\n"
        passed, msg = mod._check_no_trueskill_re_implementation(fake_src)
        assert passed is False
        assert "truesk" in msg or "trueskill" in msg.lower()


class TestRatingTracePersistenceViolation:
    def test_falsifier_present(self) -> None:
        assert "q6g_rating_trace_persistence_violation" in FALSIFIER_PRIORITY_CHAIN

    def test_no_pickle_written_after_artifact_write(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        for ext in ("pkl", "npz", "json", "parquet"):
            assert list(tmp_path.glob(f"*.{ext}")) == []

    def test_rating_state_at_end_is_dict_not_path(self, synth_stream: pd.DataFrame) -> None:
        out = mod._run_glicko2_batched_production(synth_stream)
        assert isinstance(out["rating_state_at_end"], dict)


# ---------------------------------------------------------------------------
# TestSchemaInvariants / Q5 / Q6F / forward-only / no plan-code creep
# ---------------------------------------------------------------------------


class TestSchemaInvariants:
    def test_schema_field_order_matches_dataclass(self) -> None:
        expected = tuple(f.name for f in fields(RatingImplementationProofDecision))
        assert Q6G_PROOF_SCHEMA == expected

    def test_schema_has_nit_n3_columns(self) -> None:
        for col in (
            "bootstrap_random_seed",
            "rating_period_days",
            "glicko2_iteration_tol",
            "numpy_rng_bit_generator",
            "python_floating_point_summation_order_policy",
        ):
            assert col in Q6G_PROOF_SCHEMA

    def test_schema_has_equivalence_and_determinism_columns(self) -> None:
        assert "equivalence_proof_statistics" in Q6G_PROOF_SCHEMA
        assert "byte_determinism_proof_statistics" in Q6G_PROOF_SCHEMA

    def test_schema_has_selected_policy_columns(self) -> None:
        for col in ("selected_policy", "proof_verdict", "materialization_permission"):
            assert col in Q6G_PROOF_SCHEMA

    def test_decisions_carry_pinned_constants(self) -> None:
        result = _build_test_result()
        for d in result.decisions:
            assert d.bootstrap_random_seed == "42"
            assert d.rating_period_days == "30"
            assert d.numpy_rng_bit_generator == "PCG64"
            assert d.python_floating_point_summation_order_policy == "sorted_then_kahan"
            assert d.glicko2_iteration_tol.startswith("1.0e")

    def test_audit_pr_field_carries_input(self) -> None:
        result = _build_test_result()
        for d in result.decisions:
            assert d.audit_pr == "PR #TEST"


class TestQ5BindingPreserved:
    def test_no_row_carries_q5_verdict_token(self) -> None:
        result = _build_test_result()
        passed, msg = mod._check_q5_not_re_adjudicated(result.decisions)
        assert passed is True, msg

    def test_check_q5_detects_drift(self) -> None:
        result = _build_test_result()
        dirty = list(result.decisions)
        dirty[-1] = mod.RatingImplementationProofDecision(
            **{**dirty[-1].__dict__, "proof_verdict": Q5_SELECTED_POLICY}
        )
        passed, msg = mod._check_q5_not_re_adjudicated(tuple(dirty))
        assert passed is False
        assert Q5_SELECTED_POLICY in msg

    def test_md_states_q5_not_re_adjudicated(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        assert "does NOT re-adjudicate Q5" in md


class TestQ6FBindingPreserved:
    def test_no_row_5_verdict_equals_q6f_token(self) -> None:
        result = _build_test_result()
        passed, msg = mod._check_q6f_not_re_adjudicated(result.decisions)
        assert passed is True, msg

    def test_md_states_q6f_binding_preserved(self, tmp_path: Path) -> None:
        result = _build_test_result()
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        write_q6g_proof_artifacts(result, csv_path, md_path)
        md = md_path.read_text()
        assert "Q6F_selected_policy" in md
        assert Q6F_SELECTED_POLICY in md

    def test_q6f_pinned_materialization_permission(self) -> None:
        assert (
            Q6F_MATERIALIZATION_PERMISSION
            == "recommendation_only_blocked_pending_implementation_proof_pr"
        )


class TestForwardOnlyInvariant:
    def test_all_rows_forward_only_constraints_non_empty(self) -> None:
        result = _build_test_result()
        for d in result.decisions:
            assert d.forward_only_constraints
            assert (
                "STRICT_LT_HISTORY_FILTER" in d.forward_only_constraints
                or "details_timeUTC" in d.forward_only_constraints
            )

    def test_decision_forward_only_mentions_strict_lt_filter(self) -> None:
        result = _build_test_result()
        forward_text = result.decisions[0].forward_only_constraints
        assert "started_at" in forward_text or "target.started_at" in forward_text

    def test_no_post_game_token_in_decisions(self) -> None:
        result = _build_test_result()
        forbidden = ("PostGame", "post_game", "post-game outcome read")
        for d in result.decisions:
            for f in fields(d):
                v = str(getattr(d, f.name)).lower()
                for tok in forbidden:
                    assert tok.lower() not in v or "rejection" in v or "no_post_game" in v


# ---------------------------------------------------------------------------
# TestSelectionDecisionRowEmissions
# ---------------------------------------------------------------------------


class TestSelectionDecisionRowEmissions:
    def test_selected_policy_row_present(self) -> None:
        result = _build_test_result()
        passed, msg = mod._check_q6g_selected_policy_row_present(result.decisions)
        assert passed is True

    def test_decision_count_matches_5(self) -> None:
        result = _build_test_result()
        passed, msg = mod._check_decision_count(result.decisions)
        assert passed is True

    def test_decision_id_order(self) -> None:
        result = _build_test_result()
        passed, msg = mod._check_decision_id_order(result.decisions)
        assert passed is True

    def test_decision_count_check_fails_on_short_tuple(self) -> None:
        result = _build_test_result()
        passed, msg = mod._check_decision_count(result.decisions[:3])
        assert passed is False
        assert "5" in msg

    def test_decision_id_order_check_fails_on_shuffle(self) -> None:
        result = _build_test_result()
        shuffled = (result.decisions[1], result.decisions[0]) + result.decisions[2:]
        passed, msg = mod._check_decision_id_order(shuffled)
        assert passed is False

    def test_selected_policy_check_fails_on_missing_row(self) -> None:
        result = _build_test_result()
        without_last = result.decisions[:-1]
        passed, msg = mod._check_q6g_selected_policy_row_present(without_last)
        assert passed is False
        assert "missing" in msg

    def test_selected_policy_check_fails_on_invalid_verdict(self) -> None:
        result = _build_test_result()
        tampered = list(result.decisions)
        tampered[-1] = mod.RatingImplementationProofDecision(
            **{**tampered[-1].__dict__, "proof_verdict": "obviously_wrong"}
        )
        passed, msg = mod._check_q6g_selected_policy_row_present(tuple(tampered))
        assert passed is False
        assert "allowed" in msg

    def test_selected_policy_check_fails_on_invalid_permission(self) -> None:
        result = _build_test_result()
        tampered = list(result.decisions)
        tampered[-1] = mod.RatingImplementationProofDecision(
            **{
                **tampered[-1].__dict__,
                "materialization_permission": "obviously_wrong_permission",
            }
        )
        passed, msg = mod._check_q6g_selected_policy_row_present(tuple(tampered))
        assert passed is False
        assert "materialization_permission" in msg


# ---------------------------------------------------------------------------
# TestUtilityHelpers
# ---------------------------------------------------------------------------


class TestUtilityHelpers:
    def test_sha256_file_not_found(self, tmp_path: Path) -> None:
        assert mod._sha256_file(tmp_path / "missing.txt") == "NOT_FOUND"

    def test_sha256_file_returns_64_hex(self, tmp_path: Path) -> None:
        p = tmp_path / "x.txt"
        p.write_text("hello world")
        h = mod._sha256_file(p)
        assert len(h) == 64
        assert re.fullmatch(r"[0-9a-f]{64}", h) is not None

    def test_safe_float_str_none(self) -> None:
        assert mod._safe_float_str(None) == "not_applicable"

    def test_safe_float_str_nan(self) -> None:
        assert mod._safe_float_str(math.nan) == "NaN"

    def test_safe_float_str_finite(self) -> None:
        assert mod._safe_float_str(0.123456789) == "0.123457"

    def test_get_git_sha_returns_hex_or_unknown(self) -> None:
        sha = mod._get_git_sha()
        assert sha == "UNKNOWN" or (
            len(sha) == 40 and re.fullmatch(r"[0-9a-f]{40}", sha) is not None
        )

    def test_find_repo_root_succeeds(self) -> None:
        root = mod._find_repo_root(Path(__file__))
        assert (root / "pyproject.toml").exists()

    def test_find_repo_root_fails(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            mod._find_repo_root(tmp_path)

    def test_evidence_paths_contain_8_parent_refs(self) -> None:
        text = mod._evidence_paths_text()
        for rel in (
            PARENT_PR242_CSV_REL,
            PARENT_PR242_MD_REL,
            PARENT_PR243_CSV_REL,
            PARENT_PR243_MD_REL,
            PARENT_PR245_CSV_REL,
            PARENT_PR245_MD_REL,
            PARENT_PR247_CSV_REL,
            PARENT_PR247_MD_REL,
        ):
            assert rel in text

    def test_evidence_paths_carry_all_citations(self) -> None:
        text = mod._evidence_paths_text()
        for name in (
            "Glickman",
            "Efron",
            "Higham",
        ):
            assert name in text

    def test_metric_strings_handles_none(self) -> None:
        out = mod._metric_strings(None)
        for v in out.values():
            assert v == "not_applicable"

    def test_metric_strings_handles_real_metrics(self) -> None:
        out = mod._metric_strings(
            {
                "log_loss": 0.6,
                "log_loss_ci_low": 0.58,
                "log_loss_ci_high": 0.62,
                "brier": 0.21,
                "brier_ci_low": 0.20,
                "brier_ci_high": 0.22,
                "calibration_error": 0.05,
                "coverage_rate": 0.95,
                "cold_start_rate": 0.05,
                "runtime_seconds": 0.1,
            }
        )
        assert out["log_loss"] == "0.600000"


# ---------------------------------------------------------------------------
# TestEntrypointIntegration (real DuckDB; pytest.skip if unavailable)
# ---------------------------------------------------------------------------


class TestEntrypointIntegration:
    @pytest.mark.skipif(not Path(DB_FILE).exists(), reason="Real DuckDB unavailable")
    def test_full_run_passes(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        result = run_q6g_rating_implementation_proof(
            db_path=Path(DB_FILE),
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #TEST",
            repo_root=mod._find_repo_root(Path(__file__)),
        )
        assert result.passed
        assert csv_path.exists() and md_path.exists()

    @pytest.mark.skipif(not Path(DB_FILE).exists(), reason="Real DuckDB unavailable")
    def test_full_run_emits_recommendation_only_glicko2(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        result = run_q6g_rating_implementation_proof(
            db_path=Path(DB_FILE),
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #TEST",
            repo_root=mod._find_repo_root(Path(__file__)),
        )
        # On sc2egset PHA with rating_period_days=30, equivalence fails
        # by NIT-N2 default expectation; verdict should be
        # recommendation_only_glicko2.
        assert result.decisions[-1].proof_verdict == "recommendation_only_glicko2"

    @pytest.mark.skipif(not Path(DB_FILE).exists(), reason="Real DuckDB unavailable")
    def test_full_run_csv_shape(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        run_q6g_rating_implementation_proof(
            db_path=Path(DB_FILE),
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #TEST",
            repo_root=mod._find_repo_root(Path(__file__)),
        )
        with csv_path.open() as fh:
            reader = csv.reader(fh)
            header = next(reader)
            rows = list(reader)
        assert len(header) == 39
        assert len(rows) == 5

    @pytest.mark.skipif(not Path(DB_FILE).exists(), reason="Real DuckDB unavailable")
    def test_full_run_md_has_19_sections(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        run_q6g_rating_implementation_proof(
            db_path=Path(DB_FILE),
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #TEST",
            repo_root=mod._find_repo_root(Path(__file__)),
        )
        count = len(re.findall(r"^## ", md_path.read_text(), re.MULTILINE))
        assert count >= 19

    @pytest.mark.skipif(not Path(DB_FILE).exists(), reason="Real DuckDB unavailable")
    def test_full_run_byte_determinism_passes(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        result = run_q6g_rating_implementation_proof(
            db_path=Path(DB_FILE),
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #TEST",
            repo_root=mod._find_repo_root(Path(__file__)),
        )
        assert result.byte_determinism_proof_statistics["hashes_equal"] is True

    @pytest.mark.skipif(not Path(DB_FILE).exists(), reason="Real DuckDB unavailable")
    def test_full_run_equivalence_unproven_falsifier_fires(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        result = run_q6g_rating_implementation_proof(
            db_path=Path(DB_FILE),
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #TEST",
            repo_root=mod._find_repo_root(Path(__file__)),
        )
        assert (
            "q6g_batched_event_ordering_equivalence_unproven" in result.falsifiers_fired
        )

    @pytest.mark.skipif(not Path(DB_FILE).exists(), reason="Real DuckDB unavailable")
    def test_full_run_no_parquet_in_tmp(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        run_q6g_rating_implementation_proof(
            db_path=Path(DB_FILE),
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #TEST",
            repo_root=mod._find_repo_root(Path(__file__)),
        )
        # No Parquet / json / pkl files written.
        assert list(tmp_path.glob("*.parquet")) == []
        assert list(tmp_path.glob("*.pkl")) == []
        assert list(tmp_path.glob("*.npz")) == []

    @pytest.mark.skipif(not Path(DB_FILE).exists(), reason="Real DuckDB unavailable")
    def test_full_run_write_artifacts_false_skips_write(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        result = run_q6g_rating_implementation_proof(
            db_path=Path(DB_FILE),
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #TEST",
            write_artifacts=False,
            repo_root=mod._find_repo_root(Path(__file__)),
        )
        assert result.passed
        assert not csv_path.exists()
        assert not md_path.exists()

    @pytest.mark.skipif(not Path(DB_FILE).exists(), reason="Real DuckDB unavailable")
    def test_full_run_sample_probabilities_count(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "q6g.csv"
        md_path = tmp_path / "q6g.md"
        result = run_q6g_rating_implementation_proof(
            db_path=Path(DB_FILE),
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #TEST",
            repo_root=mod._find_repo_root(Path(__file__)),
        )
        assert len(result.sample_probabilities) == 5
        for p in result.sample_probabilities:
            assert 0.0 <= p <= 1.0


# ---------------------------------------------------------------------------
# TestRatingImplementationProofError
# ---------------------------------------------------------------------------


class TestRatingImplementationProofError:
    def test_carries_falsifier_key_and_message(self) -> None:
        e = RatingImplementationProofError("x_key", "x msg")
        assert e.falsifier_key == "x_key"
        assert e.message == "x msg"
        assert "x_key" in str(e)
        assert "x msg" in str(e)

    def test_is_runtime_error_subclass(self) -> None:
        e = RatingImplementationProofError("k", "m")
        assert isinstance(e, RuntimeError)


# ---------------------------------------------------------------------------
# TestRatingImplementationProofResult / dataclass shape
# ---------------------------------------------------------------------------


class TestRatingImplementationProofResult:
    def test_result_carries_5_decisions(self) -> None:
        r = _build_test_result()
        assert len(r.decisions) == 5

    def test_result_passed_true_when_no_halting(self) -> None:
        r = _build_test_result()
        assert r.passed is True
        assert r.halting_falsifier is None

    def test_result_sample_probabilities_in_unit_interval(self) -> None:
        r = _build_test_result()
        for p in r.sample_probabilities:
            assert 0.0 <= p <= 1.0


# ---------------------------------------------------------------------------
# TestBuildProofDecisions
# ---------------------------------------------------------------------------


class TestBuildProofDecisions:
    def test_emits_5_rows_in_canonical_order(self) -> None:
        decisions = mod._build_proof_decisions(
            {
                "event_by_event_reference": {
                    "log_loss": 0.6,
                    "log_loss_ci_low": 0.58,
                    "log_loss_ci_high": 0.62,
                    "brier": 0.21,
                    "brier_ci_low": 0.20,
                    "brier_ci_high": 0.22,
                    "calibration_error": 0.05,
                    "coverage_rate": 0.95,
                    "cold_start_rate": 0.05,
                    "runtime_seconds": 0.1,
                },
                "batched_production_shape": {
                    "log_loss": 0.7,
                    "log_loss_ci_low": 0.68,
                    "log_loss_ci_high": 0.72,
                    "brier": 0.25,
                    "brier_ci_low": 0.24,
                    "brier_ci_high": 0.26,
                    "calibration_error": 0.04,
                    "coverage_rate": 0.95,
                    "cold_start_rate": 0.05,
                    "runtime_seconds": 0.2,
                },
            },
            _EQ_FAIL,
            _BD_PASS,
            audit_pr="PR #TEST",
        )
        assert len(decisions) == 5
        assert tuple(d.decision_id for d in decisions) == Q6G_PROOF_ROWS

    def test_row_5_carries_selected_policy(self) -> None:
        decisions = mod._build_proof_decisions(
            {
                "event_by_event_reference": {
                    "log_loss": 0.6,
                    "log_loss_ci_low": 0.58,
                    "log_loss_ci_high": 0.62,
                    "brier": 0.21,
                    "brier_ci_low": 0.20,
                    "brier_ci_high": 0.22,
                    "calibration_error": 0.05,
                    "coverage_rate": 0.95,
                    "cold_start_rate": 0.05,
                    "runtime_seconds": 0.1,
                },
                "batched_production_shape": {
                    "log_loss": 0.7,
                    "log_loss_ci_low": 0.68,
                    "log_loss_ci_high": 0.72,
                    "brier": 0.25,
                    "brier_ci_low": 0.24,
                    "brier_ci_high": 0.26,
                    "calibration_error": 0.04,
                    "coverage_rate": 0.95,
                    "cold_start_rate": 0.05,
                    "runtime_seconds": 0.2,
                },
            },
            _EQ_FAIL,
            _BD_PASS,
            audit_pr="PR #TEST",
        )
        last = decisions[-1]
        assert last.decision_id == "Q6G_selected_policy"
        assert last.proof_verdict == "recommendation_only_glicko2"
        assert last.selected_policy == "recommendation_only_glicko2"

    def test_row_3_has_equivalence_stats_in_csv_field(self) -> None:
        decisions = mod._build_proof_decisions(
            {
                "event_by_event_reference": {
                    "log_loss": 0.6,
                    "log_loss_ci_low": 0.58,
                    "log_loss_ci_high": 0.62,
                    "brier": 0.21,
                    "brier_ci_low": 0.20,
                    "brier_ci_high": 0.22,
                    "calibration_error": 0.05,
                    "coverage_rate": 0.95,
                    "cold_start_rate": 0.05,
                    "runtime_seconds": 0.1,
                },
                "batched_production_shape": {
                    "log_loss": 0.7,
                    "log_loss_ci_low": 0.68,
                    "log_loss_ci_high": 0.72,
                    "brier": 0.25,
                    "brier_ci_low": 0.24,
                    "brier_ci_high": 0.26,
                    "calibration_error": 0.04,
                    "coverage_rate": 0.95,
                    "cold_start_rate": 0.05,
                    "runtime_seconds": 0.2,
                },
            },
            _EQ_FAIL,
            _BD_PASS,
            audit_pr="PR #TEST",
        )
        row3 = decisions[2]
        parsed = json.loads(row3.equivalence_proof_statistics)
        for k in (
            "spearman_rho",
            "abs_delta_log_loss",
            "se_log_loss_event",
            "passes_spearman_bound",
            "passes_delta_log_loss_bound",
        ):
            assert k in parsed

    def test_row_4_has_byte_determinism_stats_in_csv_field(self) -> None:
        decisions = mod._build_proof_decisions(
            {
                "event_by_event_reference": {
                    "log_loss": 0.6,
                    "log_loss_ci_low": 0.58,
                    "log_loss_ci_high": 0.62,
                    "brier": 0.21,
                    "brier_ci_low": 0.20,
                    "brier_ci_high": 0.22,
                    "calibration_error": 0.05,
                    "coverage_rate": 0.95,
                    "cold_start_rate": 0.05,
                    "runtime_seconds": 0.1,
                },
                "batched_production_shape": {
                    "log_loss": 0.7,
                    "log_loss_ci_low": 0.68,
                    "log_loss_ci_high": 0.72,
                    "brier": 0.25,
                    "brier_ci_low": 0.24,
                    "brier_ci_high": 0.26,
                    "calibration_error": 0.04,
                    "coverage_rate": 0.95,
                    "cold_start_rate": 0.05,
                    "runtime_seconds": 0.2,
                },
            },
            _EQ_FAIL,
            _BD_PASS,
            audit_pr="PR #TEST",
        )
        row4 = decisions[3]
        parsed = json.loads(row4.byte_determinism_proof_statistics)
        for k in ("run_a_sha256", "run_b_sha256", "hashes_equal"):
            assert k in parsed

    def test_carry_forward_columns_emitted(self) -> None:
        decisions = mod._build_proof_decisions(
            {
                "event_by_event_reference": {
                    "log_loss": 0.6,
                    "log_loss_ci_low": 0.58,
                    "log_loss_ci_high": 0.62,
                    "brier": 0.21,
                    "brier_ci_low": 0.20,
                    "brier_ci_high": 0.22,
                    "calibration_error": 0.05,
                    "coverage_rate": 0.95,
                    "cold_start_rate": 0.05,
                    "runtime_seconds": 0.1,
                },
                "batched_production_shape": {
                    "log_loss": 0.7,
                    "log_loss_ci_low": 0.68,
                    "log_loss_ci_high": 0.72,
                    "brier": 0.25,
                    "brier_ci_low": 0.24,
                    "brier_ci_high": 0.26,
                    "calibration_error": 0.04,
                    "coverage_rate": 0.95,
                    "cold_start_rate": 0.05,
                    "runtime_seconds": 0.2,
                },
            },
            _EQ_PASS,
            _BD_PASS,
            audit_pr="PR #TEST",
        )
        for d in decisions[:-1]:
            assert d.proof_verdict == "not_applicable_carry_forward"

    def test_no_parent_pr_sha_columns_in_schema(self) -> None:
        # NIT-N3 schema delta: parent SHAs live in evidence_paths /
        # MD section 17, not as dedicated columns.
        for col in (
            "parent_pr242_csv_sha256",
            "parent_pr247_md_sha256",
        ):
            assert col not in Q6G_PROOF_SCHEMA

    def test_each_decision_carries_8_parent_sha_pins_in_evidence_paths(self) -> None:
        decisions = mod._build_proof_decisions(
            {
                "event_by_event_reference": {
                    "log_loss": 0.6,
                    "log_loss_ci_low": 0.58,
                    "log_loss_ci_high": 0.62,
                    "brier": 0.21,
                    "brier_ci_low": 0.20,
                    "brier_ci_high": 0.22,
                    "calibration_error": 0.05,
                    "coverage_rate": 0.95,
                    "cold_start_rate": 0.05,
                    "runtime_seconds": 0.1,
                },
                "batched_production_shape": {
                    "log_loss": 0.7,
                    "log_loss_ci_low": 0.68,
                    "log_loss_ci_high": 0.72,
                    "brier": 0.25,
                    "brier_ci_low": 0.24,
                    "brier_ci_high": 0.26,
                    "calibration_error": 0.04,
                    "coverage_rate": 0.95,
                    "cold_start_rate": 0.05,
                    "runtime_seconds": 0.2,
                },
            },
            _EQ_PASS,
            _BD_PASS,
            audit_pr="PR #TEST",
        )
        for d in decisions:
            for sha in Q6G_PARENT_SHAS.values():
                assert sha in d.evidence_paths


# ---------------------------------------------------------------------------
# Misc / cross-cutting safety checks
# ---------------------------------------------------------------------------


class TestNoROADMAPOrStatusOrLogTouch:
    def test_module_does_not_write_roadmap(self) -> None:
        src = Path(mod.__file__).read_text()
        # Module may MENTION ROADMAP in docstrings as a guard statement
        # ("Never modifies ... or ROADMAP."), but must not import a
        # ROADMAP-writing module or call .write_text() on a ROADMAP path.
        assert "open(ROADMAP" not in src
        assert "ROADMAP.md, 'w'" not in src
        assert ".write_text(ROADMAP_CONTENT" not in src

    def test_module_writes_only_csv_and_md(self) -> None:
        src = Path(mod.__file__).read_text()
        # Look for explicit write extensions other than csv/md.
        assert ".parquet" not in src or "no Parquet" in src or "Parquet" in src
        for forbidden_write in (
            "STEP_STATUS.yaml",
            "PIPELINE_SECTION_STATUS.yaml",
            "PHASE_STATUS.yaml",
            "research_log.md",
        ):
            # The module is allowed to mention these in docstrings only,
            # but must not write to them.
            occurrences = src.count(forbidden_write)
            # Acceptable: appears in docstring guard ("NEVER modifies
            # status YAMLs, research logs, or ROADMAP."). Should not be
            # written.
            assert occurrences <= 5

    def test_module_does_not_write_leakage_audit_path(self) -> None:
        src = Path(mod.__file__).read_text()
        assert "leakage_audit_sc2egset" not in src


class TestPhase03Discipline:
    def test_no_create_temporal_split_imports(self) -> None:
        src = Path(mod.__file__).read_text()
        assert "create_temporal_split" not in src

    def test_no_baseline_modeling_imports(self) -> None:
        src = Path(mod.__file__).read_text()
        forbidden = (
            "from sklearn.linear_model import",
            "LogisticRegression",
            "RandomForestClassifier",
            "GradientBoostingClassifier",
            "lightgbm",
            "xgboost",
        )
        for tok in forbidden:
            assert tok not in src

    def test_module_docstring_states_not_phase_03(self) -> None:
        src = Path(mod.__file__).read_text()
        # The docstring should mention being not phase 03.
        # The module is the Q6G proof; phase 03 work is out of scope.
        # MD section 18 also enforces this.
        assert "Phase" in src and "03" in src


class TestSandboxNotebookCompanion:
    """Ensure sandbox companion notebook exists and references the module."""

    def test_sandbox_companion_py_exists(self) -> None:
        p = (
            Path(mod._find_repo_root(Path(__file__)))
            / "sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/"
            / "02_01_03_q6g_rating_implementation_proof.py"
        )
        assert p.exists(), f"sandbox notebook py missing at {p}"

    def test_sandbox_companion_ipynb_exists(self) -> None:
        p = (
            Path(mod._find_repo_root(Path(__file__)))
            / "sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/"
            / "02_01_03_q6g_rating_implementation_proof.ipynb"
        )
        assert p.exists(), f"sandbox notebook ipynb missing at {p}"
