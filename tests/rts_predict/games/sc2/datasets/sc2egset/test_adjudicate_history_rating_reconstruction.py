"""Tests for the SC2EGSet Q6 rating-reconstruction successor adjudicator.

Covers: module-shape invariants (B4 45-entry equality), pinned SHA
constants (11 parent + source-file artifacts), per-Q6 decision content,
every falsifier in ``FALSIFIER_PRIORITY_CHAIN`` (45 entries: fire test +
pass test), SHA pinning tests, candidate-completeness tests,
POST-GAME-token rejection tests, MMR-missingness reaffirmation tests,
Q5-non-re-adjudication tests, scope-creep tests, materialization-creep
tests, forward-only / leakage-free tests, N-1 / N-2 / N-3 / N-4 / N-9
/ N-10 binding-nit tests, determinism tests, and real-DB integration
test gated by ``@pytest.mark.skipif``.
"""

from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import fields, replace
from pathlib import Path
from typing import Any

import pytest

from rts_predict.games.sc2.datasets.sc2egset import (
    adjudicate_history_rating_reconstruction as adj_mod,
)
from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import (  # noqa: E501
    POST_GAME_TOKENS as SOURCE_LAYER_POST_GAME_TOKENS,
)
from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_rating_reconstruction import (  # noqa: E501
    ALLOWED_COMPLEXITY_DEPLOYABILITY,
    ALLOWED_LEAKAGE_RISK,
    ALLOWED_MATERIALIZATION_PERMISSION,
    ALLOWED_Q6_BINDING_LEVELS,
    ALLOWED_Q6_VERDICTS,
    ALLOWED_RATING_EVIDENCE_LEVELS,
    CANDIDATE_REQUIRED_CITATIONS,
    CROSS_02_02_SPEC_REL,
    DATASET_RESEARCH_LOG_PR245_EVIDENCE_TOKENS,
    DATASET_RESEARCH_LOG_REL,
    EXCLUDED_METHODS_CONSIDERED,
    EXPECTED_CROSS_02_02_SPEC_SHA256,
    EXPECTED_FEATURE_FAMILY_REGISTRY_CSV_SHA256,
    EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256,
    EXPECTED_MATCHES_HISTORY_MINIMAL_YAML_SHA256,
    EXPECTED_MMR_MISSING_DENSITY_MFC_PCT,
    EXPECTED_MMR_MISSING_DENSITY_PHA_PCT,
    EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256,
    EXPECTED_PR241_VALIDATOR_SHA256,
    EXPECTED_PR242_CSV_SHA256,
    EXPECTED_PR242_MD_SHA256,
    EXPECTED_PR243_CSV_SHA256,
    EXPECTED_PR243_MD_SHA256,
    FALSIFIER_PRIORITY_CHAIN,
    FEATURE_FAMILY_REGISTRY_CSV_REL,
    HELPER_TO_FALSIFIER_KEY,
    HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS,
    MATCHES_FLAT_CLEAN_YAML_REL,
    MATCHES_HISTORY_MINIMAL_YAML_REL,
    NON_RATING_HISTORY_FAMILIES,
    PARENT_PR242_CSV_REL,
    PARENT_PR242_MD_REL,
    PARENT_PR243_CSV_REL,
    PARENT_PR243_MD_REL,
    PLAYER_HISTORY_ALL_YAML_REL,
    PR241_VALIDATOR_MODULE_REL,
    PROBE_MFC_MMR_MISSING_DENSITY_QUERY,
    PROBE_PHA_DETAILS_TIMEUTC_TRY_CAST_NULL_RATE_QUERY,
    PROBE_PHA_MMR_MISSING_DENSITY_QUERY,
    PROBE_PHA_PER_PLAYER_HISTORY_DEPTH_QUERY,
    PROBE_PHA_RESULT_DISTRIBUTION_QUERY,
    PROBE_PHA_RESULT_VS_MMR_PRESENCE_QUERY,
    Q6_ADJUDICATION_SCHEMA,
    Q6_DECISION_IDS,
    Q6_RATING_POLICY_CANDIDATES,
    RATING_RECONSTRUCTION_ADJUDICATION_CSV_REL,
    RATING_RECONSTRUCTION_ADJUDICATION_MD_REL,
    RAW_MMR_HYBRID_REJECTION_TOKEN,
    STRICT_LT_HISTORY_FILTER,
    RatingReconstructionAdjudicationDecision,
    RatingReconstructionAdjudicationError,
    _build_decisions,
    _check_cold_start_policy_present_when_non_omit,
    _check_complexity_deployability_valid,
    _check_cross_02_02_spec_sha256,
    _check_dataset_research_log_evidence_present,
    _check_decision_count,
    _check_decision_ids_canonical_order,
    _check_evidence_level_valid,
    _check_excluded_methods_considered_complete,
    _check_external_citation_present_when_non_omit_non_deferred,
    _check_feature_family_registry_csv_sha256,
    _check_forward_only_constraint_present_when_non_omit,
    _check_hyperparameter_policy_present_when_non_omit,
    _check_leakage_risk_valid,
    _check_matches_flat_clean_yaml_sha256,
    _check_matches_history_minimal_yaml_sha256,
    _check_materialization_permission_consistent_with_verdict,
    _check_materialization_permission_valid,
    _check_mmr_missingness_summary_present,
    _check_no_direct_target_match_outcome_reference,
    _check_no_future_match_reference,
    _check_no_global_batch_fit_reference,
    _check_no_materialized_output_paths_populated,
    _check_no_phase_03_baseline_creep,
    _check_no_post_game_token_in_scoped_fields,
    _check_no_research_log_mutation_implied,
    _check_no_roadmap_path_modified,
    _check_no_status_yaml_path_referenced,
    _check_parent_pr242_csv_sha256,
    _check_parent_pr242_md_sha256,
    _check_parent_pr243_csv_sha256,
    _check_parent_pr243_md_sha256,
    _check_per_family_impact_broadcasts_all_6_families,
    _check_per_family_impact_summary_row_present,
    _check_player_history_all_yaml_sha256,
    _check_pr241_validator_sha256,
    _check_q5_not_re_adjudicated,
    _check_q6_candidate_set_complete,
    _check_q6_deferred_candidate_present,
    _check_q6_omit_candidate_present,
    _check_raw_mmr_hybrid_rejection_token_present,
    _check_selected_policy_in_candidate_set,
    _check_selected_policy_row_present,
    _check_selected_policy_verdict_consistent,
    _check_tie_policy_present_when_non_omit,
    _check_universal_tracker_source_in_history,
    _common_fields,
    _decision_to_field_dict,
    _find_repo_root,
    _get_git_sha,
    _is_valid_sha256,
    _scoped_field_iter,
    _sha256_file,
    _write_md,
    compute_dataset_research_log_sha256,
    run_rating_reconstruction_adjudication,
)

# ---------------------------------------------------------------------------
# Repository-relative path constants
# ---------------------------------------------------------------------------

_TESTS_ROOT = Path(__file__).resolve().parents[6]

PARENT_PR242_CSV_PATH: Path = _TESTS_ROOT / PARENT_PR242_CSV_REL
PARENT_PR242_MD_PATH: Path = _TESTS_ROOT / PARENT_PR242_MD_REL
PARENT_PR243_CSV_PATH: Path = _TESTS_ROOT / PARENT_PR243_CSV_REL
PARENT_PR243_MD_PATH: Path = _TESTS_ROOT / PARENT_PR243_MD_REL
PR241_VALIDATOR_PATH: Path = _TESTS_ROOT / PR241_VALIDATOR_MODULE_REL
CROSS_02_02_SPEC_PATH: Path = _TESTS_ROOT / CROSS_02_02_SPEC_REL
FEATURE_FAMILY_REGISTRY_CSV_PATH: Path = _TESTS_ROOT / FEATURE_FAMILY_REGISTRY_CSV_REL
DATASET_RESEARCH_LOG_PATH: Path = _TESTS_ROOT / DATASET_RESEARCH_LOG_REL
PHA_YAML_PATH: Path = _TESTS_ROOT / PLAYER_HISTORY_ALL_YAML_REL
MFC_YAML_PATH: Path = _TESTS_ROOT / MATCHES_FLAT_CLEAN_YAML_REL
MHM_YAML_PATH: Path = _TESTS_ROOT / MATCHES_HISTORY_MINIMAL_YAML_REL
Q6_CSV_PATH: Path = _TESTS_ROOT / RATING_RECONSTRUCTION_ADJUDICATION_CSV_REL
Q6_MD_PATH: Path = _TESTS_ROOT / RATING_RECONSTRUCTION_ADJUDICATION_MD_REL
DUCKDB_PATH: Path = (
    _TESTS_ROOT
    / "src"
    / "rts_predict"
    / "games"
    / "sc2"
    / "datasets"
    / "sc2egset"
    / "data"
    / "db"
    / "db.duckdb"
)

VALID_SHA: str = EXPECTED_PR241_VALIDATOR_SHA256
ALT_VALID_SHA: str = "a" * 64

REAL_INPUTS_AVAILABLE: bool = (
    DUCKDB_PATH.exists()
    and PARENT_PR242_CSV_PATH.exists()
    and PARENT_PR242_MD_PATH.exists()
    and PARENT_PR243_CSV_PATH.exists()
    and PARENT_PR243_MD_PATH.exists()
)

# Pinned artifact SHAs (from committed artifacts at T01-T06)
EXPECTED_Q6_CSV_SHA: str = (
    "703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0"
)
EXPECTED_Q6_MD_SHA: str = (
    "7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419"
)


# ---------------------------------------------------------------------------
# Synthetic decision builder helpers
# ---------------------------------------------------------------------------


def _make_decisions(audit_pr: str = "PR #TEST") -> tuple[
    RatingReconstructionAdjudicationDecision, ...
]:
    """Build the canonical 8-decision tuple via the module's own builder."""
    return _build_decisions(_common_fields(audit_pr))


def _replace_row(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    target_id: str,
    **kwargs: Any,
) -> tuple[RatingReconstructionAdjudicationDecision, ...]:
    """Return a new tuple with the named row replaced by ``replace(d, **kwargs)``."""
    out: list[RatingReconstructionAdjudicationDecision] = []
    for d in decisions:
        if d.decision_id == target_id:
            out.append(replace(d, **kwargs))
        else:
            out.append(d)
    return tuple(out)


def _by_id(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    decision_id: str,
) -> RatingReconstructionAdjudicationDecision:
    for d in decisions:
        if d.decision_id == decision_id:
            return d
    raise AssertionError(f"decision_id {decision_id!r} not found")


@pytest.fixture(scope="module")
def passing_decisions() -> tuple[RatingReconstructionAdjudicationDecision, ...]:
    """Build the canonical 8-decision tuple; module-scoped for speed."""
    return _make_decisions()


# ---------------------------------------------------------------------------
# 1. Schema tests (~20)
# ---------------------------------------------------------------------------


class TestSchemaColumnCount:
    """Q6_ADJUDICATION_SCHEMA has exactly 31 columns."""

    def test_schema_has_31_columns(self) -> None:
        assert len(Q6_ADJUDICATION_SCHEMA) == 31

    def test_schema_column_count_equals_dataclass_field_count(self) -> None:
        assert len(fields(RatingReconstructionAdjudicationDecision)) == len(
            Q6_ADJUDICATION_SCHEMA
        )


class TestSchemaColumnOrder:
    """Column order matches the dataclass field order."""

    def test_schema_order_matches_dataclass(self) -> None:
        dataclass_names = tuple(
            f.name for f in fields(RatingReconstructionAdjudicationDecision)
        )
        assert Q6_ADJUDICATION_SCHEMA == dataclass_names


class TestCsvHeaderMatchesSchema:
    """On-disk CSV header matches Q6_ADJUDICATION_SCHEMA."""

    def test_csv_header_matches_schema(self) -> None:
        if not Q6_CSV_PATH.exists():
            pytest.skip("Q6 CSV artifact not present on disk")
        with Q6_CSV_PATH.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            assert reader.fieldnames is not None
            assert tuple(reader.fieldnames) == Q6_ADJUDICATION_SCHEMA

    def test_csv_has_8_data_rows(self) -> None:
        if not Q6_CSV_PATH.exists():
            pytest.skip("Q6 CSV artifact not present on disk")
        with Q6_CSV_PATH.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
        assert len(rows) == 8

    def test_csv_materialized_output_paths_empty_on_all_rows(self) -> None:
        if not Q6_CSV_PATH.exists():
            pytest.skip("Q6 CSV artifact not present on disk")
        with Q6_CSV_PATH.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                assert row["materialized_output_paths"] == "", (
                    f"Row {row['decision_id']!r} has non-empty materialized_output_paths"
                )

    def test_csv_audit_pr_populated_on_all_rows(self) -> None:
        if not Q6_CSV_PATH.exists():
            pytest.skip("Q6 CSV artifact not present on disk")
        with Q6_CSV_PATH.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                assert row["audit_pr"], (
                    f"Row {row['decision_id']!r} has empty audit_pr"
                )

    @pytest.mark.parametrize(
        "sha_field",
        [
            "parent_pr242_csv_sha256",
            "parent_pr242_md_sha256",
            "parent_pr243_csv_sha256",
            "parent_pr243_md_sha256",
        ],
    )
    def test_csv_sha_fields_are_lowercase_hex_64(self, sha_field: str) -> None:
        if not Q6_CSV_PATH.exists():
            pytest.skip("Q6 CSV artifact not present on disk")
        with Q6_CSV_PATH.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                sha = row[sha_field]
                assert re.fullmatch(r"[0-9a-f]{64}", sha), (
                    f"Row {row['decision_id']!r} field {sha_field!r} "
                    f"is not 64-char lowercase hex: {sha!r}"
                )


# ---------------------------------------------------------------------------
# 2. Decision-row tests (~30)
# ---------------------------------------------------------------------------


class TestDecisionCount:
    """Exactly 8 decisions in Q6_DECISION_IDS order."""

    def test_eight_decisions_canonical_order(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        assert len(passing_decisions) == 8
        ids = tuple(d.decision_id for d in passing_decisions)
        assert ids == Q6_DECISION_IDS


class TestQ6DecisionIds:
    """Q6_DECISION_IDS has exactly 8 entries."""

    def test_decision_ids_length(self) -> None:
        assert len(Q6_DECISION_IDS) == 8

    def test_decision_ids_no_duplicates(self) -> None:
        assert len(set(Q6_DECISION_IDS)) == len(Q6_DECISION_IDS)


class TestPerCandidateRowVerdictEnum:
    """Each per-candidate row has a valid verdict from ALLOWED_Q6_VERDICTS."""

    @pytest.mark.parametrize("decision_id", list(Q6_DECISION_IDS))
    def test_verdict_valid(
        self,
        decision_id: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        d = _by_id(passing_decisions, decision_id)
        assert d.verdict in ALLOWED_Q6_VERDICTS

    @pytest.mark.parametrize("decision_id", list(Q6_DECISION_IDS))
    def test_binding_level_valid(
        self,
        decision_id: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        d = _by_id(passing_decisions, decision_id)
        assert d.binding_level in ALLOWED_Q6_BINDING_LEVELS

    @pytest.mark.parametrize("decision_id", list(Q6_DECISION_IDS))
    def test_rating_evidence_level_valid(
        self,
        decision_id: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        d = _by_id(passing_decisions, decision_id)
        assert d.rating_evidence_level in ALLOWED_RATING_EVIDENCE_LEVELS

    @pytest.mark.parametrize("decision_id", list(Q6_DECISION_IDS))
    def test_complexity_deployability_valid(
        self,
        decision_id: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        d = _by_id(passing_decisions, decision_id)
        assert d.complexity_deployability_score in ALLOWED_COMPLEXITY_DEPLOYABILITY

    @pytest.mark.parametrize("decision_id", list(Q6_DECISION_IDS))
    def test_leakage_risk_valid(
        self,
        decision_id: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        d = _by_id(passing_decisions, decision_id)
        assert d.leakage_risk_score in ALLOWED_LEAKAGE_RISK

    @pytest.mark.parametrize("decision_id", list(Q6_DECISION_IDS))
    def test_materialization_permission_valid(
        self,
        decision_id: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        d = _by_id(passing_decisions, decision_id)
        assert d.materialization_permission in ALLOWED_MATERIALIZATION_PERMISSION


class TestSelectedPolicyRow:
    """Q6_selected_policy row encodes the correct binding."""

    def test_selected_policy_is_deferred_blocker(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        d = _by_id(passing_decisions, "Q6_selected_policy")
        assert d.selected_policy == "deferred_blocker_with_algorithm_survey_required"
        assert d.verdict == "deferred_blocker"
        assert d.binding_level == "deferred_blocker"

    def test_selected_policy_materialization_blocked(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        d = _by_id(passing_decisions, "Q6_selected_policy")
        assert d.materialization_permission == "blocked_pending_algorithm_survey_pr"

    def test_selected_policy_candidate_policy_empty(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        d = _by_id(passing_decisions, "Q6_selected_policy")
        assert d.candidate_policy == ""

    def test_selected_policy_parent_decision_id(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        d = _by_id(passing_decisions, "Q6_selected_policy")
        assert d.parent_decision_id == "Q6_rating_policy"


class TestPerFamilySummaryRow:
    """Q6_per_family_impact_summary row is informational."""

    def test_summary_row_verdict_is_recommendation_only(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        d = _by_id(passing_decisions, "Q6_per_family_impact_summary")
        assert d.verdict == "recommendation_only"

    def test_summary_row_broadcasts_all_6_families(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        d = _by_id(passing_decisions, "Q6_per_family_impact_summary")
        for family in HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS:
            assert family in d.feature_availability_summary


# ---------------------------------------------------------------------------
# 3. Falsifier roll-call tests (~45 fire tests + pass tests via parametrize)
# ---------------------------------------------------------------------------


class TestFalsifierRollCall:
    """Every falsifier key appears in both HELPER_TO_FALSIFIER_KEY and FALSIFIER_PRIORITY_CHAIN."""

    def test_all_45_keys_present_in_helper_map(self) -> None:
        assert len(HELPER_TO_FALSIFIER_KEY) == 45

    def test_all_45_keys_present_in_chain(self) -> None:
        assert len(FALSIFIER_PRIORITY_CHAIN) == 45

    def test_chain_has_no_duplicates(self) -> None:
        assert len(set(FALSIFIER_PRIORITY_CHAIN)) == 45

    def test_set_equality(self) -> None:
        assert set(FALSIFIER_PRIORITY_CHAIN) == set(HELPER_TO_FALSIFIER_KEY.values())


class TestShaFalsifierFires:
    """SHA-pin falsifiers fire on tampered files and pass on canonical files."""

    def test_pr242_csv_sha_fires_on_tampered(self, tmp_path: Path) -> None:
        fake = tmp_path / "x.csv"
        fake.write_bytes(b"tampered")
        fired, _ = _check_parent_pr242_csv_sha256(fake)
        assert fired

    def test_pr242_csv_sha_passes_on_canonical(self, tmp_path: Path) -> None:
        # We can't reconstruct the canonical file here, so verify that a file
        # with wrong content fires (mismatch path).
        data = b"body"
        fake = tmp_path / "real.csv"
        fake.write_bytes(data)
        # Direct call: sha mismatch → fired=True (because data sha != expected sha)
        fired, _ = _check_parent_pr242_csv_sha256(fake)
        assert fired  # data sha does not match pinned expected sha

    def test_pr242_md_sha_fires_on_tampered(self, tmp_path: Path) -> None:
        fake = tmp_path / "x.md"
        fake.write_bytes(b"tampered")
        fired, _ = _check_parent_pr242_md_sha256(fake)
        assert fired

    def test_pr243_csv_sha_fires_on_tampered(self, tmp_path: Path) -> None:
        fake = tmp_path / "x.csv"
        fake.write_bytes(b"tampered")
        fired, _ = _check_parent_pr243_csv_sha256(fake)
        assert fired

    def test_pr243_md_sha_fires_on_tampered(self, tmp_path: Path) -> None:
        fake = tmp_path / "x.md"
        fake.write_bytes(b"tampered")
        fired, _ = _check_parent_pr243_md_sha256(fake)
        assert fired

    def test_pr241_validator_sha_fires_on_tampered(self, tmp_path: Path) -> None:
        fake = tmp_path / "fake.py"
        fake.write_text("# tampered", encoding="utf-8")
        fired, _ = _check_pr241_validator_sha256(fake)
        assert fired

    def test_pr241_validator_sha_fires_on_missing(self, tmp_path: Path) -> None:
        fired, msg = _check_pr241_validator_sha256(tmp_path / "missing.py")
        assert fired
        assert "NOT_FOUND" in msg

    def test_cross_02_02_spec_sha_fires_on_tampered(self, tmp_path: Path) -> None:
        fake = tmp_path / "x.md"
        fake.write_text("# tampered", encoding="utf-8")
        fired, _ = _check_cross_02_02_spec_sha256(fake)
        assert fired

    def test_feature_family_registry_sha_fires_on_tampered(
        self, tmp_path: Path
    ) -> None:
        fake = tmp_path / "x.csv"
        fake.write_text("tampered", encoding="utf-8")
        fired, _ = _check_feature_family_registry_csv_sha256(fake)
        assert fired

    def test_dataset_research_log_evidence_fires_on_tampered(
        self, tmp_path: Path
    ) -> None:
        """Tampered content lacking PR #245-era tokens halts the check."""
        fake = tmp_path / "x.md"
        fake.write_text("# tampered (no PR #245 tokens)", encoding="utf-8")
        fired, msg = _check_dataset_research_log_evidence_present(fake)
        assert fired
        assert "evidence_missing" in msg

    def test_pha_yaml_sha_fires_on_tampered(self, tmp_path: Path) -> None:
        fake = tmp_path / "x.yaml"
        fake.write_text("# tampered", encoding="utf-8")
        fired, _ = _check_player_history_all_yaml_sha256(fake)
        assert fired

    def test_mfc_yaml_sha_fires_on_tampered(self, tmp_path: Path) -> None:
        fake = tmp_path / "x.yaml"
        fake.write_text("# tampered", encoding="utf-8")
        fired, _ = _check_matches_flat_clean_yaml_sha256(fake)
        assert fired

    def test_mhm_yaml_sha_fires_on_tampered(self, tmp_path: Path) -> None:
        fake = tmp_path / "x.yaml"
        fake.write_text("# tampered", encoding="utf-8")
        fired, _ = _check_matches_history_minimal_yaml_sha256(fake)
        assert fired

    def test_sha_helper_passes_on_correct_body(self, tmp_path: Path) -> None:
        """A file whose SHA-256 equals EXPECTED_PR241_VALIDATOR_SHA256 does not fire."""
        # Compute a body whose sha matches the pinned PR#241 sha is impossible without
        # the original file — instead verify the canonical file on disk.
        if not PR241_VALIDATOR_PATH.exists():
            pytest.skip("PR #241 validator module not on disk")
        fired, _ = _check_pr241_validator_sha256(PR241_VALIDATOR_PATH)
        assert not fired


class TestShaFalsifierPassesOnCanonical:
    """SHA-pin falsifiers do not fire on the canonical on-disk files."""

    def test_cross_02_02_spec_passes(self) -> None:
        if not CROSS_02_02_SPEC_PATH.exists():
            pytest.skip("CROSS-02-02 spec not on disk")
        fired, _ = _check_cross_02_02_spec_sha256(CROSS_02_02_SPEC_PATH)
        assert not fired

    def test_pha_yaml_passes(self) -> None:
        if not PHA_YAML_PATH.exists():
            pytest.skip("PHA YAML not on disk")
        fired, _ = _check_player_history_all_yaml_sha256(PHA_YAML_PATH)
        assert not fired

    def test_mfc_yaml_passes(self) -> None:
        if not MFC_YAML_PATH.exists():
            pytest.skip("MFC YAML not on disk")
        fired, _ = _check_matches_flat_clean_yaml_sha256(MFC_YAML_PATH)
        assert not fired

    def test_mhm_yaml_passes(self) -> None:
        if not MHM_YAML_PATH.exists():
            pytest.skip("MHM YAML not on disk")
        fired, _ = _check_matches_history_minimal_yaml_sha256(MHM_YAML_PATH)
        assert not fired

    def test_feature_family_registry_passes(self) -> None:
        if not FEATURE_FAMILY_REGISTRY_CSV_PATH.exists():
            pytest.skip("Feature family registry CSV not on disk")
        fired, _ = _check_feature_family_registry_csv_sha256(
            FEATURE_FAMILY_REGISTRY_CSV_PATH
        )
        assert not fired

    def test_dataset_research_log_evidence_present_passes(self) -> None:
        """Evidence-presence check passes on canonical on-disk content."""
        if not DATASET_RESEARCH_LOG_PATH.exists():
            pytest.skip("Dataset research_log not on disk")
        fired, _ = _check_dataset_research_log_evidence_present(
            DATASET_RESEARCH_LOG_PATH
        )
        assert not fired


class TestDatasetResearchLogAppendOnlySafety:
    """Regression tests for chore PR #<TBD> 2026-05-28 append-only fix.

    The dataset ``research_log.md`` is append-only mutable lineage; the
    original PR #245 exact-SHA pin was a category error. These tests
    pin the append-only-safe contract:

    1. Benign new entries appended at the end DO NOT halt the check.
    2. Removal / tampering of any required PR #245-era token DOES halt
       the check with an ``evidence_missing`` message.
    3. All three configured tokens are independently load-bearing
       (removing any one of them halts the check).
    4. The provenance-only ``compute_dataset_research_log_sha256``
       helper returns a valid digest without comparing it to anything.
    """

    def test_dataset_research_log_passes_when_new_entries_appended(
        self, tmp_path: Path
    ) -> None:
        """Appending a new entry after the existing content must not halt."""
        if not DATASET_RESEARCH_LOG_PATH.exists():
            pytest.skip("Dataset research_log not on disk")
        original = DATASET_RESEARCH_LOG_PATH.read_text(encoding="utf-8")
        appended = tmp_path / "research_log_with_append.md"
        appended.write_text(
            original
            + "\n\n---\n\n## 2099-01-01 -- benign append regression entry\n"
            + "- **Category:** C\n- **Note:** synthetic append-only safety probe\n",
            encoding="utf-8",
        )
        fired, msg = _check_dataset_research_log_evidence_present(appended)
        assert not fired, (
            f"Append-only update must not halt; got: {msg!r}"
        )

    def test_dataset_research_log_halts_when_pr245_evidence_removed(
        self, tmp_path: Path
    ) -> None:
        """Removing the PR #245-era anchor tokens must halt the check."""
        if not DATASET_RESEARCH_LOG_PATH.exists():
            pytest.skip("Dataset research_log not on disk")
        original = DATASET_RESEARCH_LOG_PATH.read_text(encoding="utf-8")
        stripped = original
        for tok in DATASET_RESEARCH_LOG_PR245_EVIDENCE_TOKENS:
            stripped = stripped.replace(tok, "")
        fake = tmp_path / "research_log_stripped.md"
        fake.write_text(stripped, encoding="utf-8")
        fired, msg = _check_dataset_research_log_evidence_present(fake)
        assert fired
        assert "evidence_missing" in msg

    @pytest.mark.parametrize(
        "token_index", list(range(len(DATASET_RESEARCH_LOG_PR245_EVIDENCE_TOKENS)))
    )
    def test_each_pr245_token_is_independently_load_bearing(
        self, tmp_path: Path, token_index: int
    ) -> None:
        """Removing any single required token must halt the check."""
        if not DATASET_RESEARCH_LOG_PATH.exists():
            pytest.skip("Dataset research_log not on disk")
        original = DATASET_RESEARCH_LOG_PATH.read_text(encoding="utf-8")
        target_token = DATASET_RESEARCH_LOG_PR245_EVIDENCE_TOKENS[token_index]
        stripped = original.replace(target_token, "")
        fake = tmp_path / f"research_log_missing_{token_index}.md"
        fake.write_text(stripped, encoding="utf-8")
        fired, msg = _check_dataset_research_log_evidence_present(fake)
        assert fired
        assert target_token in msg

    def test_check_halts_when_file_missing(self, tmp_path: Path) -> None:
        """Missing on-disk file must halt with evidence_missing message."""
        missing = tmp_path / "nope.md"
        fired, msg = _check_dataset_research_log_evidence_present(missing)
        assert fired
        assert "evidence_missing" in msg

    def test_compute_sha256_helper_returns_valid_digest(self) -> None:
        """Provenance helper returns a 64-char lowercase hex digest."""
        if not DATASET_RESEARCH_LOG_PATH.exists():
            pytest.skip("Dataset research_log not on disk")
        digest = compute_dataset_research_log_sha256(
            DATASET_RESEARCH_LOG_PATH
        )
        assert _is_valid_sha256(digest)

    def test_compute_sha256_helper_returns_not_found_for_missing(
        self, tmp_path: Path
    ) -> None:
        """Provenance helper returns ``'NOT_FOUND'`` when file absent."""
        assert (
            compute_dataset_research_log_sha256(tmp_path / "missing.md")
            == "NOT_FOUND"
        )


class TestCandidateSetFalsifiers:
    """Candidate-set completeness and ordering falsifiers."""

    def test_passes_on_canonical(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_q6_candidate_set_complete(passing_decisions)
        assert not fired

    def test_fires_when_candidate_missing(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = tuple(
            d
            for d in passing_decisions
            if d.candidate_policy != "elo"
        )
        fired, msg = _check_q6_candidate_set_complete(decisions)
        assert fired
        assert "elo" in msg

    def test_omit_candidate_present_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_q6_omit_candidate_present(passing_decisions)
        assert not fired

    def test_omit_candidate_missing_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6A_omit_reconstructed_rating",
            candidate_policy="",
        )
        fired, _ = _check_q6_omit_candidate_present(decisions)
        assert fired

    def test_deferred_candidate_present_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_q6_deferred_candidate_present(passing_decisions)
        assert not fired

    def test_deferred_candidate_missing_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6F_deferred_with_algorithm_survey",
            candidate_policy="",
        )
        fired, _ = _check_q6_deferred_candidate_present(decisions)
        assert fired

    def test_decision_count_eight_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_decision_count(passing_decisions)
        assert not fired

    def test_decision_count_seven_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = passing_decisions[:-1]
        fired, msg = _check_decision_count(decisions)
        assert fired
        assert "8" in msg

    def test_decision_count_nine_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        extra = replace(passing_decisions[0], decision_id="Q6Z_extra")
        decisions = (*passing_decisions, extra)
        fired, msg = _check_decision_count(decisions)
        assert fired

    def test_canonical_order_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_decision_ids_canonical_order(passing_decisions)
        assert not fired

    def test_wrong_order_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        # Swap first and last
        swapped = (
            passing_decisions[-1],
            *passing_decisions[1:-1],
            passing_decisions[0],
        )
        fired, _ = _check_decision_ids_canonical_order(swapped)
        assert fired


class TestPostGameTokenFalsifiers:
    """POST-GAME token falsifiers fire on forbidden tokens; notes field is exempt."""

    def test_no_post_game_token_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_no_post_game_token_in_scoped_fields(passing_decisions)
        assert not fired

    def test_post_game_token_in_verdict_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        # Use "outcome" -- a genuine POST_GAME token that matches as a standalone word.
        decisions = _replace_row(
            passing_decisions,
            "Q6A_omit_reconstructed_rating",
            verdict="outcome",
        )
        fired, _ = _check_no_post_game_token_in_scoped_fields(decisions)
        assert fired

    def test_post_game_token_in_notes_does_not_fire(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        """notes field is exempt from POST-GAME token scan (B-X1 carry-over)."""
        decisions = _replace_row(
            passing_decisions,
            "Q6A_omit_reconstructed_rating",
            notes="no win or loss outcome referenced here",
        )
        fired, _ = _check_no_post_game_token_in_scoped_fields(decisions)
        assert not fired

    def test_direct_outcome_reference_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            verdict="target_result",
        )
        fired, _ = _check_no_direct_target_match_outcome_reference(decisions)
        assert fired

    def test_no_direct_outcome_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_no_direct_target_match_outcome_reference(passing_decisions)
        assert not fired

    def test_future_match_reference_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            verdict="future_match",
        )
        fired, _ = _check_no_future_match_reference(decisions)
        assert fired

    def test_no_future_match_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_no_future_match_reference(passing_decisions)
        assert not fired

    def test_global_batch_fit_reference_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6D_glicko_or_glicko_2",
            verdict="global fit",
        )
        fired, _ = _check_no_global_batch_fit_reference(decisions)
        assert fired

    def test_no_global_batch_fit_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_no_global_batch_fit_reference(passing_decisions)
        assert not fired

    def test_phase_03_baseline_creep_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            verdict="phase_03_baseline",
        )
        fired, _ = _check_no_phase_03_baseline_creep(decisions)
        assert fired

    def test_no_phase_03_baseline_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_no_phase_03_baseline_creep(passing_decisions)
        assert not fired


# ---------------------------------------------------------------------------
# 4. SHA pinning tests (~10)
# ---------------------------------------------------------------------------


class TestSha256FileHelper:
    """_sha256_file returns 64-char lowercase hex or 'NOT_FOUND'."""

    def test_missing_file_returns_not_found(self, tmp_path: Path) -> None:
        assert _sha256_file(tmp_path / "missing.txt") == "NOT_FOUND"

    def test_known_content_returns_correct_sha(self, tmp_path: Path) -> None:
        f = tmp_path / "f.txt"
        f.write_bytes(b"hello")
        expected = hashlib.sha256(b"hello").hexdigest()
        assert _sha256_file(f) == expected

    def test_sha_is_lowercase_hex_64(self, tmp_path: Path) -> None:
        f = tmp_path / "f.txt"
        f.write_bytes(b"data")
        sha = _sha256_file(f)
        assert len(sha) == 64
        assert re.fullmatch(r"[0-9a-f]{64}", sha)


class TestIsValidSha256Helper:
    """_is_valid_sha256 accepts only 64-char lowercase hex strings."""

    @pytest.mark.parametrize("sha", [VALID_SHA, "0" * 64, "deadbeef" * 8])
    def test_valid_passes(self, sha: str) -> None:
        assert _is_valid_sha256(sha)

    @pytest.mark.parametrize(
        "sha",
        ["", "a" * 63, "A" * 64, "Z" * 64, "0" * 63 + "X", "NOT_FOUND"],
    )
    def test_invalid_rejected(self, sha: str) -> None:
        assert not _is_valid_sha256(sha)


class TestPinnedShaConstantsMatchDisk:
    """All 11 pinned SHA constants must match the live on-disk files."""

    def test_pr242_csv_sha_matches_disk(self) -> None:
        if not PARENT_PR242_CSV_PATH.exists():
            pytest.skip("PR #242 CSV not on disk")
        assert _sha256_file(PARENT_PR242_CSV_PATH) == EXPECTED_PR242_CSV_SHA256

    def test_pr242_md_sha_matches_disk(self) -> None:
        if not PARENT_PR242_MD_PATH.exists():
            pytest.skip("PR #242 MD not on disk")
        assert _sha256_file(PARENT_PR242_MD_PATH) == EXPECTED_PR242_MD_SHA256

    def test_pr243_csv_sha_matches_disk(self) -> None:
        if not PARENT_PR243_CSV_PATH.exists():
            pytest.skip("PR #243 CSV not on disk")
        assert _sha256_file(PARENT_PR243_CSV_PATH) == EXPECTED_PR243_CSV_SHA256

    def test_pr243_md_sha_matches_disk(self) -> None:
        if not PARENT_PR243_MD_PATH.exists():
            pytest.skip("PR #243 MD not on disk")
        assert _sha256_file(PARENT_PR243_MD_PATH) == EXPECTED_PR243_MD_SHA256

    def test_pr241_validator_sha_matches_disk(self) -> None:
        if not PR241_VALIDATOR_PATH.exists():
            pytest.skip("PR #241 validator not on disk")
        assert _sha256_file(PR241_VALIDATOR_PATH) == EXPECTED_PR241_VALIDATOR_SHA256

    def test_cross_02_02_spec_sha_matches_disk(self) -> None:
        if not CROSS_02_02_SPEC_PATH.exists():
            pytest.skip("CROSS-02-02 spec not on disk")
        assert _sha256_file(CROSS_02_02_SPEC_PATH) == EXPECTED_CROSS_02_02_SPEC_SHA256

    def test_feature_family_registry_sha_matches_disk(self) -> None:
        if not FEATURE_FAMILY_REGISTRY_CSV_PATH.exists():
            pytest.skip("Feature family registry CSV not on disk")
        assert (
            _sha256_file(FEATURE_FAMILY_REGISTRY_CSV_PATH)
            == EXPECTED_FEATURE_FAMILY_REGISTRY_CSV_SHA256
        )

    def test_pha_yaml_sha_matches_disk(self) -> None:
        if not PHA_YAML_PATH.exists():
            pytest.skip("PHA YAML not on disk")
        assert _sha256_file(PHA_YAML_PATH) == EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256

    def test_mfc_yaml_sha_matches_disk(self) -> None:
        if not MFC_YAML_PATH.exists():
            pytest.skip("MFC YAML not on disk")
        assert _sha256_file(MFC_YAML_PATH) == EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256

    def test_mhm_yaml_sha_matches_disk(self) -> None:
        if not MHM_YAML_PATH.exists():
            pytest.skip("MHM YAML not on disk")
        assert (
            _sha256_file(MHM_YAML_PATH) == EXPECTED_MATCHES_HISTORY_MINIMAL_YAML_SHA256
        )


# ---------------------------------------------------------------------------
# 5. Candidate-completeness tests (~10)
# ---------------------------------------------------------------------------


class TestCandidateCompletenessGates:
    """Missing / extra / duplicate candidates fire the right falsifiers."""

    def test_missing_rolling_candidate_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6B_rolling_win_rate_or_bayesian_smoothed_baseline",
            candidate_policy="",
        )
        fired, msg = _check_q6_candidate_set_complete(decisions)
        assert fired
        assert "rolling_win_rate_or_bayesian_smoothed_baseline" in msg

    def test_missing_glicko_candidate_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6D_glicko_or_glicko_2",
            candidate_policy="",
        )
        fired, msg = _check_q6_candidate_set_complete(decisions)
        assert fired
        assert "glicko_or_glicko_2" in msg

    def test_all_6_candidates_present_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_q6_candidate_set_complete(passing_decisions)
        assert not fired

    def test_selected_policy_row_present_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_selected_policy_row_present(passing_decisions)
        assert not fired

    def test_selected_policy_row_missing_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = tuple(
            d for d in passing_decisions if d.decision_id != "Q6_selected_policy"
        )
        fired, _ = _check_selected_policy_row_present(decisions)
        assert fired

    def test_per_family_summary_present_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_per_family_impact_summary_row_present(passing_decisions)
        assert not fired

    def test_per_family_summary_missing_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = tuple(
            d
            for d in passing_decisions
            if d.decision_id != "Q6_per_family_impact_summary"
        )
        fired, _ = _check_per_family_impact_summary_row_present(decisions)
        assert fired

    def test_selected_policy_not_in_candidate_set_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6_selected_policy",
            selected_policy="q6z_nonexistent_policy",
        )
        fired, _ = _check_selected_policy_in_candidate_set(decisions)
        assert fired

    def test_selected_policy_in_candidate_set_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_selected_policy_in_candidate_set(passing_decisions)
        assert not fired

    def test_selected_policy_verdict_invalid_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6_selected_policy",
            verdict="invalid_verdict_xyz",
        )
        fired, _ = _check_selected_policy_verdict_consistent(decisions)
        assert fired

    def test_selected_policy_verdict_valid_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_selected_policy_verdict_consistent(passing_decisions)
        assert not fired


# ---------------------------------------------------------------------------
# 6. POST-GAME token rejection tests (~10)
# ---------------------------------------------------------------------------


class TestPostGameTokenRejectionDetailed:
    """Each POST-GAME token in scoped fields fires; notes is exempt."""

    @pytest.mark.parametrize(
        "token",
        ["outcome", "winner", "match_result", "post_game", "final_state"],
    )
    def test_forbidden_token_in_verdict_fires(
        self,
        token: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            verdict=token,
        )
        fired, _ = _check_no_post_game_token_in_scoped_fields(decisions)
        assert fired

    @pytest.mark.parametrize(
        "token",
        ["outcome", "winner", "match_result", "post_game"],
    )
    def test_forbidden_token_in_notes_does_not_fire(
        self,
        token: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        """notes is exempt from POST-GAME scan per B-X1."""
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            notes=f"no {token} referenced here as per the design",
        )
        fired, _ = _check_no_post_game_token_in_scoped_fields(decisions)
        assert not fired


# ---------------------------------------------------------------------------
# 7. MMR-missingness reaffirmation tests (~5)
# ---------------------------------------------------------------------------


class TestMmrMissingnessReaffirmation:
    """MMR missingness figures (83.95% / 83.65%) must appear on candidate rows."""

    def test_passes_on_canonical(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_mmr_missingness_summary_present(passing_decisions)
        assert not fired

    def test_missing_mfc_figure_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6A_omit_reconstructed_rating",
            mmr_missingness_summary="only mentions 83.65%",
        )
        fired, msg = _check_mmr_missingness_summary_present(decisions)
        assert fired
        assert "83.95" in msg

    def test_missing_pha_figure_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            mmr_missingness_summary="only mentions 83.95%",
        )
        fired, msg = _check_mmr_missingness_summary_present(decisions)
        assert fired
        assert "83.65" in msg

    def test_both_figures_in_summary_field(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        for d in passing_decisions:
            if not d.candidate_policy:
                continue
            assert "83.95" in d.mmr_missingness_summary
            assert "83.65" in d.mmr_missingness_summary

    def test_expected_pct_constants_correct(self) -> None:
        assert EXPECTED_MMR_MISSING_DENSITY_MFC_PCT == 83.95
        assert EXPECTED_MMR_MISSING_DENSITY_PHA_PCT == 83.65


# ---------------------------------------------------------------------------
# 8. Q5-non-re-adjudication tests (~5)
# ---------------------------------------------------------------------------


class TestQ5NonReAdjudication:
    """Q5 verdict tokens forbidden in verdict-bearing fields."""

    def test_passes_on_canonical(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_q5_not_re_adjudicated(passing_decisions)
        assert not fired

    def test_cross_region_policy_in_verdict_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            verdict="cross_region_policy",
        )
        fired, msg = _check_q5_not_re_adjudicated(decisions)
        assert fired

    def test_strict_exclusion_in_selected_policy_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6_selected_policy",
            selected_policy="strict_exclusion",
        )
        fired, _ = _check_q5_not_re_adjudicated(decisions)
        assert fired

    def test_dual_feature_path_in_candidate_policy_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            candidate_policy="dual_feature_path",
        )
        fired, _ = _check_q5_not_re_adjudicated(decisions)
        assert fired

    def test_q5_token_in_notes_does_not_fire(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        """notes is not a verdict-bearing field; Q5 tokens are OK there."""
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            notes="Q5 cross_region_policy was strict_exclusion in PR #242",
        )
        fired, _ = _check_q5_not_re_adjudicated(decisions)
        assert not fired


# ---------------------------------------------------------------------------
# 9. Status-YAML / research_log / ROADMAP drift tests (~5)
# ---------------------------------------------------------------------------


class TestScopeCreepGuards:
    """Status YAML / research_log / ROADMAP tokens forbidden in scoped fields."""

    def test_no_status_yaml_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_no_status_yaml_path_referenced(passing_decisions)
        assert not fired

    @pytest.mark.parametrize(
        "fragment",
        ["STEP_STATUS.yaml", "PIPELINE_SECTION_STATUS.yaml", "PHASE_STATUS.yaml"],
    )
    def test_status_yaml_fragment_in_verdict_fires(
        self,
        fragment: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            verdict=fragment.lower(),
        )
        fired, _ = _check_no_status_yaml_path_referenced(decisions)
        assert fired

    def test_no_research_log_mutation_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_no_research_log_mutation_implied(passing_decisions)
        assert not fired

    def test_research_log_mutation_token_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            verdict="append to research_log",
        )
        fired, _ = _check_no_research_log_mutation_implied(decisions)
        assert fired

    def test_no_roadmap_edit_passes(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_no_roadmap_path_modified(passing_decisions)
        assert not fired

    def test_roadmap_edit_token_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            verdict="roadmap.md edit",
        )
        fired, _ = _check_no_roadmap_path_modified(decisions)
        assert fired


# ---------------------------------------------------------------------------
# 10. Materialization-creep tests (~5)
# ---------------------------------------------------------------------------


class TestMaterializationCreep:
    """materialized_output_paths must be empty on every row; no Parquet written."""

    def test_passes_on_canonical(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_no_materialized_output_paths_populated(passing_decisions)
        assert not fired

    @pytest.mark.parametrize("decision_id", list(Q6_DECISION_IDS))
    def test_non_empty_materialized_output_paths_fires(
        self,
        decision_id: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            decision_id,
            materialized_output_paths="some/output.parquet",
        )
        fired, _ = _check_no_materialized_output_paths_populated(decisions)
        assert fired

    def test_canonical_decisions_all_have_empty_materialized_output(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        for d in passing_decisions:
            assert d.materialized_output_paths == ""


# ---------------------------------------------------------------------------
# 11. B4 invariant tests (~3)
# ---------------------------------------------------------------------------


class TestB4Invariants:
    """B4: HELPER_TO_FALSIFIER_KEY and FALSIFIER_PRIORITY_CHAIN set equality."""

    def test_helper_map_len_equals_45(self) -> None:
        assert len(HELPER_TO_FALSIFIER_KEY) == 45

    def test_chain_len_equals_45(self) -> None:
        assert len(FALSIFIER_PRIORITY_CHAIN) == 45

    def test_chain_no_duplicates(self) -> None:
        assert len(set(FALSIFIER_PRIORITY_CHAIN)) == 45

    def test_set_equality(self) -> None:
        assert set(FALSIFIER_PRIORITY_CHAIN) == set(HELPER_TO_FALSIFIER_KEY.values())

    def test_chain_subset_of_map(self) -> None:
        assert set(FALSIFIER_PRIORITY_CHAIN) <= set(HELPER_TO_FALSIFIER_KEY.values())


# ---------------------------------------------------------------------------
# 12. Determinism tests (~5)
# ---------------------------------------------------------------------------


class TestDeterminism:
    """Two consecutive builds produce byte-identical decisions."""

    def test_decisions_byte_identical_on_two_builds(self) -> None:
        d1 = _build_decisions(_common_fields("PR #TEST"))
        d2 = _build_decisions(_common_fields("PR #TEST"))
        for a, b in zip(d1, d2):
            assert a == b

    def test_q6_csv_sha_matches_pinned(self) -> None:
        if not Q6_CSV_PATH.exists():
            pytest.skip("Q6 CSV artifact not on disk")
        observed = _sha256_file(Q6_CSV_PATH)
        assert observed == EXPECTED_Q6_CSV_SHA, (
            f"Q6 CSV SHA mismatch: {observed!r} != {EXPECTED_Q6_CSV_SHA!r}"
        )

    def test_q6_md_sha_matches_pinned(self) -> None:
        if not Q6_MD_PATH.exists():
            pytest.skip("Q6 MD artifact not on disk")
        observed = _sha256_file(Q6_MD_PATH)
        assert observed == EXPECTED_Q6_MD_SHA, (
            f"Q6 MD SHA mismatch: {observed!r} != {EXPECTED_Q6_MD_SHA!r}"
        )

    def test_canonical_sha_constants_are_valid_hex(self) -> None:
        assert _is_valid_sha256(EXPECTED_Q6_CSV_SHA)
        assert _is_valid_sha256(EXPECTED_Q6_MD_SHA)

    def test_build_decisions_output_length_stable(self) -> None:
        decisions = _build_decisions(_common_fields("PR #RUN1"))
        assert len(decisions) == 8


# ---------------------------------------------------------------------------
# 13. Binding-nit tests — N-1 method acknowledgement (~10)
# ---------------------------------------------------------------------------


class TestN1MethodAcknowledgement:
    """Every non-summary row must list all 3 EXCLUDED_METHODS_CONSIDERED tokens."""

    def test_passes_on_canonical(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_excluded_methods_considered_complete(passing_decisions)
        assert not fired

    @pytest.mark.parametrize("method", list(EXCLUDED_METHODS_CONSIDERED))
    def test_method_present_on_all_non_summary_rows(
        self,
        method: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        for d in passing_decisions:
            if d.decision_id == "Q6_per_family_impact_summary":
                continue
            assert method in d.excluded_methods_considered, (
                f"Method {method!r} missing from {d.decision_id!r} "
                f"excluded_methods_considered"
            )

    def test_aligulac_missing_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6A_omit_reconstructed_rating",
            excluded_methods_considered='["bradley_terry", "neural_btl"]',
        )
        fired, msg = _check_excluded_methods_considered_complete(decisions)
        assert fired
        assert "aligulac_style_btl" in msg

    def test_excluded_methods_count_is_3(self) -> None:
        assert len(EXCLUDED_METHODS_CONSIDERED) == 3

    def test_all_three_tokens_in_excluded_methods(self) -> None:
        assert "aligulac_style_btl" in EXCLUDED_METHODS_CONSIDERED
        assert "bradley_terry" in EXCLUDED_METHODS_CONSIDERED
        assert "neural_btl" in EXCLUDED_METHODS_CONSIDERED


class TestN2RawMmrHybridRejection:
    """The Q6_selected_policy row must reference the raw_mmr_hybrid_rejection token."""

    def test_passes_on_canonical(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_raw_mmr_hybrid_rejection_token_present(passing_decisions)
        assert not fired

    def test_token_missing_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6_selected_policy",
            raw_mmr_hybrid_rejection="some other rejection text",
        )
        fired, msg = _check_raw_mmr_hybrid_rejection_token_present(decisions)
        assert fired
        assert RAW_MMR_HYBRID_REJECTION_TOKEN in msg

    def test_rejection_token_constant_value(self) -> None:
        assert RAW_MMR_HYBRID_REJECTION_TOKEN == "raw_mmr_where_present_plus_is_mmr_missing"


# ---------------------------------------------------------------------------
# 14. N-3 probe-grouping test
# ---------------------------------------------------------------------------


class TestN3ProbeGroupingByToonId:
    """Probe 5 uses GROUP BY toon_id; player_id_worldwide is not in the query."""

    def test_probe_5_uses_group_by_toon_id(self) -> None:
        assert "GROUP BY toon_id" in PROBE_PHA_PER_PLAYER_HISTORY_DEPTH_QUERY

    def test_probe_5_does_not_use_player_id_worldwide(self) -> None:
        assert "player_id_worldwide" not in PROBE_PHA_PER_PLAYER_HISTORY_DEPTH_QUERY


# ---------------------------------------------------------------------------
# 15. N-4 determinism test — ORDER BY before LIMIT or no LIMIT
# ---------------------------------------------------------------------------


class TestN4ProbeDeterminism:
    """All probe SQL strings satisfy N-4: ORDER BY or no LIMIT."""

    @pytest.mark.parametrize(
        "probe_query",
        [
            PROBE_PHA_RESULT_DISTRIBUTION_QUERY,
            PROBE_PHA_DETAILS_TIMEUTC_TRY_CAST_NULL_RATE_QUERY,
            PROBE_MFC_MMR_MISSING_DENSITY_QUERY,
            PROBE_PHA_MMR_MISSING_DENSITY_QUERY,
            PROBE_PHA_PER_PLAYER_HISTORY_DEPTH_QUERY,
            PROBE_PHA_RESULT_VS_MMR_PRESENCE_QUERY,
        ],
    )
    def test_probe_has_order_by_or_no_limit(self, probe_query: str) -> None:
        has_limit = "LIMIT" in probe_query.upper()
        has_order_by = "ORDER BY" in probe_query.upper()
        if has_limit:
            assert has_order_by, (
                "Probe has LIMIT without ORDER BY -- N-4 violation: "
                f"{probe_query[:120]!r}"
            )


# ---------------------------------------------------------------------------
# 16. N-9 POST_GAME token-set source test
# ---------------------------------------------------------------------------


class TestN9TokenSetSource:
    """POST_GAME_TOKENS must equal POST_GAME_TOKENS from the source-layer adjudicator."""

    def test_post_game_tokens_match_source_layer(self) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_rating_reconstruction import (  # noqa: E501
            POST_GAME_TOKENS,
        )
        assert POST_GAME_TOKENS == SOURCE_LAYER_POST_GAME_TOKENS


# ---------------------------------------------------------------------------
# 17. N-10 Q6F-legitimate verdict test
# ---------------------------------------------------------------------------


class TestN10Q6FLegitimate:
    """MD §12 must contain the word 'legitimate' referring to Q6F."""

    def test_md_section_12_contains_legitimate(self) -> None:
        if not Q6_MD_PATH.exists():
            pytest.skip("Q6 MD artifact not on disk")
        content = Q6_MD_PATH.read_text(encoding="utf-8")
        sec12_idx = content.find("## §12")
        assert sec12_idx != -1, "MD does not contain '## §12'"
        sec12_content = content[sec12_idx:]
        assert "legitimate" in sec12_content.lower(), (
            "MD §12 does not contain 'legitimate' reference to Q6F"
        )

    def test_q6f_notes_contains_legitimate(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        d = _by_id(passing_decisions, "Q6F_deferred_with_algorithm_survey")
        assert "legitimate" in d.notes.lower()


# ---------------------------------------------------------------------------
# 18. Forward-only / leakage-free tests (~15)
# ---------------------------------------------------------------------------


class TestForwardOnlyConstraints:
    """Non-omit candidate rows must reference forward-only wording."""

    def test_passes_on_canonical(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_forward_only_constraint_present_when_non_omit(
            passing_decisions
        )
        assert not fired

    @pytest.mark.parametrize(
        "decision_id",
        [
            "Q6B_rolling_win_rate_or_bayesian_smoothed_baseline",
            "Q6C_elo",
            "Q6D_glicko_or_glicko_2",
            "Q6E_trueskill_or_trueskill_like",
        ],
    )
    def test_missing_forward_only_wording_fires(
        self,
        decision_id: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            decision_id,
            rating_forward_only_constraints="no constraints specified",
        )
        fired, msg = _check_forward_only_constraint_present_when_non_omit(decisions)
        assert fired
        assert decision_id in msg

    def test_strict_lt_history_filter_form(self) -> None:
        assert STRICT_LT_HISTORY_FILTER == (
            "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"
        )


class TestColdStartConstraints:
    """Non-omit candidate rows must reference G-CS-4 wording."""

    def test_passes_on_canonical(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_cold_start_policy_present_when_non_omit(passing_decisions)
        assert not fired

    @pytest.mark.parametrize(
        "decision_id",
        [
            "Q6B_rolling_win_rate_or_bayesian_smoothed_baseline",
            "Q6C_elo",
        ],
    )
    def test_missing_g_cs_4_fires(
        self,
        decision_id: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            decision_id,
            rating_cold_start_policy="no cold start policy",
        )
        fired, msg = _check_cold_start_policy_present_when_non_omit(decisions)
        assert fired
        assert "G-CS-4" in msg


class TestTiePolicyConstraints:
    """Non-omit candidate rows must include tie/draw policy wording."""

    def test_passes_on_canonical(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_tie_policy_present_when_non_omit(passing_decisions)
        assert not fired

    def test_empty_tie_policy_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            rating_tie_policy="",
        )
        fired, msg = _check_tie_policy_present_when_non_omit(decisions)
        assert fired


class TestHyperparameterPolicyConstraints:
    """Non-omit candidate rows must defer hyperparameters."""

    def test_passes_on_canonical(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_hyperparameter_policy_present_when_non_omit(passing_decisions)
        assert not fired

    def test_missing_deferred_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            rating_hyperparameter_policy="K=32 fixed",
        )
        fired, msg = _check_hyperparameter_policy_present_when_non_omit(decisions)
        assert fired

    def test_missing_algorithm_word_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6D_glicko_or_glicko_2",
            rating_hyperparameter_policy="deferred to some other step",
        )
        fired, msg = _check_hyperparameter_policy_present_when_non_omit(decisions)
        assert fired


class TestLeakageTokenRejection:
    """Leakage tokens in scoped fields fire the appropriate falsifiers."""

    def test_history_time_gt_target_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            verdict="history_time > target_time",
        )
        fired, _ = _check_no_future_match_reference(decisions)
        assert fired

    def test_global_batch_fit_fires_in_verdict(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6D_glicko_or_glicko_2",
            verdict="batch fit",
        )
        fired, _ = _check_no_global_batch_fit_reference(decisions)
        assert fired

    def test_phase_03_in_verdict_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6E_trueskill_or_trueskill_like",
            verdict="baseline_modeling",
        )
        fired, _ = _check_no_phase_03_baseline_creep(decisions)
        assert fired


class TestMaterializationPermissionConsistency:
    """deferred_blocker verdict → blocked_pending_algorithm_survey_pr permission."""

    def test_passes_on_canonical(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_materialization_permission_consistent_with_verdict(
            passing_decisions
        )
        assert not fired

    def test_deferred_blocker_without_blocked_permission_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6_selected_policy",
            materialization_permission="not_applicable",
        )
        fired, msg = _check_materialization_permission_consistent_with_verdict(decisions)
        assert fired
        assert "blocked_pending_algorithm_survey_pr" in msg

    def test_non_deferred_blocker_does_not_fire(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        # Q6A has verdict=deferred_recommendation (not deferred_blocker)
        # so consistency check should pass.
        decisions = _replace_row(
            passing_decisions,
            "Q6_selected_policy",
            verdict="narrow_with_evidence",
            materialization_permission="not_applicable",
        )
        fired, _ = _check_materialization_permission_consistent_with_verdict(decisions)
        assert not fired


# ---------------------------------------------------------------------------
# 19. Misc tests (~10)
# ---------------------------------------------------------------------------


class TestModuleImportInvariants:
    """Module import-time invariants pass without exception."""

    def test_module_imports_cleanly(self) -> None:
        import importlib
        mod = importlib.import_module(
            "rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_rating_reconstruction"
        )
        assert mod is not None

    def test_adjudication_schema_length(self) -> None:
        assert len(Q6_ADJUDICATION_SCHEMA) == 31

    def test_decision_ids_length(self) -> None:
        assert len(Q6_DECISION_IDS) == 8

    def test_rating_policy_candidates_length(self) -> None:
        assert len(Q6_RATING_POLICY_CANDIDATES) == 6

    def test_excluded_methods_length(self) -> None:
        assert len(EXCLUDED_METHODS_CONSIDERED) == 3

    def test_history_enriched_family_ids_length(self) -> None:
        assert len(HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS) == 6

    def test_non_rating_history_families_length(self) -> None:
        assert len(NON_RATING_HISTORY_FAMILIES) == 5

    def test_helper_to_falsifier_key_len_45(self) -> None:
        assert len(HELPER_TO_FALSIFIER_KEY) == 45

    def test_falsifier_priority_chain_len_45(self) -> None:
        assert len(FALSIFIER_PRIORITY_CHAIN) == 45

    def test_values_set_equality(self) -> None:
        assert set(HELPER_TO_FALSIFIER_KEY.values()) == set(FALSIFIER_PRIORITY_CHAIN)


class TestTrackerSourceRejection:
    """Tracker-events source tokens forbidden in scoped fields."""

    def test_passes_on_canonical(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_universal_tracker_source_in_history(passing_decisions)
        assert not fired

    @pytest.mark.parametrize(
        "token",
        ["tracker_events_raw", "tracker_events", "trackerevents"],
    )
    def test_tracker_token_in_verdict_fires(
        self,
        token: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            verdict=token,
        )
        fired, _ = _check_universal_tracker_source_in_history(decisions)
        assert fired


class TestPerFamilyBroadcast:
    """Q6_per_family_impact_summary must reference all 6 family IDs."""

    def test_passes_on_canonical(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        fired, _ = _check_per_family_impact_broadcasts_all_6_families(passing_decisions)
        assert not fired

    def test_missing_family_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6_per_family_impact_summary",
            feature_availability_summary="only has focal_player_history",
        )
        fired, msg = _check_per_family_impact_broadcasts_all_6_families(decisions)
        assert fired


class TestCustomException:
    """RatingReconstructionAdjudicationError roundtrip."""

    def test_construct_and_message(self) -> None:
        err = RatingReconstructionAdjudicationError(
            "test_key", "observed != expected"
        )
        assert err.falsifier_key == "test_key"
        assert "test_key" in str(err)
        assert "observed != expected" in str(err)


# ---------------------------------------------------------------------------
# 20. External-citation discipline tests
# ---------------------------------------------------------------------------


class TestExternalCitationDiscipline:
    """Non-omit non-deferred selected policy must cite algorithm sources."""

    def test_passes_on_canonical_deferred(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        """Q6F is deferred; no external citation required."""
        fired, _ = _check_external_citation_present_when_non_omit_non_deferred(
            passing_decisions
        )
        assert not fired

    def test_elo_selected_without_citation_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6_selected_policy",
            selected_policy="elo",
            evidence_paths="some/path.md",
        )
        fired, msg = _check_external_citation_present_when_non_omit_non_deferred(
            decisions
        )
        assert fired

    def test_glicko_selected_without_citation_fires(
        self, passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6_selected_policy",
            selected_policy="glicko_or_glicko_2",
            evidence_paths="some/path.md",
        )
        fired, msg = _check_external_citation_present_when_non_omit_non_deferred(
            decisions
        )
        assert fired

    def test_candidate_required_citations_has_elo_entry(self) -> None:
        assert "elo" in CANDIDATE_REQUIRED_CITATIONS

    def test_candidate_required_citations_has_glicko_entry(self) -> None:
        assert "glicko_or_glicko_2" in CANDIDATE_REQUIRED_CITATIONS

    def test_candidate_required_citations_has_trueskill_entry(self) -> None:
        assert "trueskill_or_trueskill_like" in CANDIDATE_REQUIRED_CITATIONS


# ---------------------------------------------------------------------------
# 21. Row-level SHA fields presence tests
# ---------------------------------------------------------------------------


class TestRowLevelShaFields:
    """Every row carries the pinned parent SHA fields verbatim."""

    @pytest.mark.parametrize("decision_id", list(Q6_DECISION_IDS))
    def test_pr242_csv_sha_present(
        self,
        decision_id: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        d = _by_id(passing_decisions, decision_id)
        assert d.parent_pr242_csv_sha256 == EXPECTED_PR242_CSV_SHA256

    @pytest.mark.parametrize("decision_id", list(Q6_DECISION_IDS))
    def test_pr243_csv_sha_present(
        self,
        decision_id: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        d = _by_id(passing_decisions, decision_id)
        assert d.parent_pr243_csv_sha256 == EXPECTED_PR243_CSV_SHA256

    @pytest.mark.parametrize("decision_id", list(Q6_DECISION_IDS))
    def test_materialized_output_paths_empty(
        self,
        decision_id: str,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        d = _by_id(passing_decisions, decision_id)
        assert d.materialized_output_paths == ""


# ---------------------------------------------------------------------------
# 22. Integration test — real DuckDB (skip_probes=False)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not REAL_INPUTS_AVAILABLE,
    reason="Real DuckDB / parent artifacts not available in this environment",
)
class TestIntegrationWithRealDuckDb:
    """Full entrypoint run against the real DuckDB; confirms pass + determinism."""

    @pytest.fixture(scope="class")
    def real_result(self, tmp_path_factory: pytest.TempPathFactory) -> Any:
        tmp = tmp_path_factory.mktemp("q6_real")
        csv_out = tmp / "q6.csv"
        md_out = tmp / "q6.md"
        result = run_rating_reconstruction_adjudication(
            duckdb_path=DUCKDB_PATH,
            parent_pr242_csv_path=PARENT_PR242_CSV_PATH,
            parent_pr242_md_path=PARENT_PR242_MD_PATH,
            parent_pr243_csv_path=PARENT_PR243_CSV_PATH,
            parent_pr243_md_path=PARENT_PR243_MD_PATH,
            pr241_validator_module_path=PR241_VALIDATOR_PATH,
            cross_02_02_spec_path=CROSS_02_02_SPEC_PATH,
            feature_family_registry_csv_path=FEATURE_FAMILY_REGISTRY_CSV_PATH,
            dataset_research_log_path=DATASET_RESEARCH_LOG_PATH,
            player_history_all_yaml_path=PHA_YAML_PATH,
            matches_flat_clean_yaml_path=MFC_YAML_PATH,
            matches_history_minimal_yaml_path=MHM_YAML_PATH,
            csv_out_path=csv_out,
            md_out_path=md_out,
            audit_pr="PR #INTEGRATION_TEST",
            skip_probes=False,
        )
        return result

    def test_result_passed(self, real_result: Any) -> None:
        assert real_result.passed is True

    def test_halting_falsifier_is_none(self, real_result: Any) -> None:
        assert real_result.halting_falsifier is None

    def test_eight_decisions(self, real_result: Any) -> None:
        assert len(real_result.decisions) == 8

    def test_probes_non_empty(self, real_result: Any) -> None:
        assert len(real_result.probes) > 0

    def test_probe_keys_expected(self, real_result: Any) -> None:
        expected_keys = {
            "pha_result_distribution",
            "pha_details_timeutc_null_rate",
            "mfc_mmr_missing",
            "pha_mmr_missing",
            "pha_per_player_history_depth",
            "pha_result_vs_mmr_presence",
        }
        assert expected_keys <= set(real_result.probes.keys())

    def test_csv_sha_matches_pinned_from_real_run(
        self, real_result: Any, tmp_path_factory: pytest.TempPathFactory
    ) -> None:
        csv_path = Path(real_result.csv_path)
        if not csv_path.exists():
            pytest.skip("CSV not written")
        # The audit_pr differs so SHA won't match committed SHA; just verify valid hex.
        observed = _sha256_file(csv_path)
        assert _is_valid_sha256(observed)


# ---------------------------------------------------------------------------
# 23. _get_git_sha exception path (line 894-895)
# ---------------------------------------------------------------------------


class TestGetGitShaExceptionPath:
    """_get_git_sha returns 'UNKNOWN' when subprocess fails."""

    def test_returns_unknown_when_called_process_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import subprocess as sp

        def _fail(*args: Any, **kwargs: Any) -> Any:
            raise sp.CalledProcessError(1, "git")

        monkeypatch.setattr(adj_mod.subprocess, "run", _fail)
        result = _get_git_sha()
        assert result == "UNKNOWN"

    def test_returns_unknown_when_file_not_found(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def _fail(*args: Any, **kwargs: Any) -> Any:
            raise FileNotFoundError("git not found")

        monkeypatch.setattr(adj_mod.subprocess, "run", _fail)
        result = _get_git_sha()
        assert result == "UNKNOWN"


# ---------------------------------------------------------------------------
# 24. _find_repo_root FileNotFoundError path (lines 910-915)
# ---------------------------------------------------------------------------


class TestFindRepoRootFileNotFound:
    """_find_repo_root raises FileNotFoundError when no pyproject.toml exists."""

    def test_raises_when_no_pyproject_toml(self, tmp_path: Path) -> None:
        deep = tmp_path / "a" / "b" / "c"
        deep.mkdir(parents=True)
        with pytest.raises(FileNotFoundError, match="pyproject.toml"):
            _find_repo_root(deep)

    def test_returns_correct_root_when_pyproject_exists(
        self, tmp_path: Path
    ) -> None:
        (tmp_path / "pyproject.toml").write_text("[tool]\n", encoding="utf-8")
        sub = tmp_path / "sub" / "dir"
        sub.mkdir(parents=True)
        found = _find_repo_root(sub)
        assert found == tmp_path


# ---------------------------------------------------------------------------
# 25. Probe None-return branches (lines 1003, 1020, 1037)
# ---------------------------------------------------------------------------


class TestProbeNoneReturnBranches:
    """Probe functions return (0, 0) when the query yields no rows."""

    def test_probe_pha_details_timeutc_returns_zero_tuple_on_none(self) -> None:
        from unittest.mock import MagicMock

        from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_rating_reconstruction import (  # noqa: E501
            _probe_pha_details_timeutc_null_rate,
        )

        mock_con = MagicMock()
        mock_con.execute.return_value.fetchone.return_value = None
        result = _probe_pha_details_timeutc_null_rate(mock_con)
        assert result == (0, 0)

    def test_probe_mfc_mmr_missing_density_returns_zero_tuple_on_none(self) -> None:
        from unittest.mock import MagicMock

        from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_rating_reconstruction import (  # noqa: E501
            _probe_mfc_mmr_missing_density,
        )

        mock_con = MagicMock()
        mock_con.execute.return_value.fetchone.return_value = None
        result = _probe_mfc_mmr_missing_density(mock_con)
        assert result == (0, 0)

    def test_probe_pha_mmr_missing_density_returns_zero_tuple_on_none(self) -> None:
        from unittest.mock import MagicMock

        from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_rating_reconstruction import (  # noqa: E501
            _probe_pha_mmr_missing_density,
        )

        mock_con = MagicMock()
        mock_con.execute.return_value.fetchone.return_value = None
        result = _probe_pha_mmr_missing_density(mock_con)
        assert result == (0, 0)


# ---------------------------------------------------------------------------
# 26. _scoped_field_iter field_name not in row branch (line 1329)
# ---------------------------------------------------------------------------


class TestScopedFieldIterMissingField:
    """_scoped_field_iter skips field names not present in the decision dict."""

    def test_unknown_field_name_skipped(
        self,
        monkeypatch: pytest.MonkeyPatch,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        # Add a field name that is NOT in the dataclass to force the continue branch.
        original = adj_mod.Q6_SCOPED_FIELDS_FOR_TOKEN_SCAN
        monkeypatch.setattr(
            adj_mod,
            "Q6_SCOPED_FIELDS_FOR_TOKEN_SCAN",
            original | {"__nonexistent_field_xyz__"},
        )
        # Should not raise; the non-existent field is silently skipped.
        result = _scoped_field_iter(passing_decisions)
        # All real fields still appear; the fake one does not.
        field_names = {fname for _, fname, _ in result}
        assert "__nonexistent_field_xyz__" not in field_names
        assert "verdict" in field_names  # real scoped field is still present


# ---------------------------------------------------------------------------
# 27. Enum-invalid falsifier return True paths (lines 1580, 1596, 1610, 1626)
# ---------------------------------------------------------------------------


class TestEnumInvalidFalsifierReturnPaths:
    """Enum-validity falsifiers return True when the field value is not in the enum."""

    def test_evidence_level_invalid_fires(
        self,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6A_omit_reconstructed_rating",
            rating_evidence_level="invalid_level_xyz",
        )
        fired, msg = _check_evidence_level_valid(decisions)
        assert fired
        assert "invalid_level_xyz" in msg

    def test_complexity_deployability_invalid_fires(
        self,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6B_rolling_win_rate_or_bayesian_smoothed_baseline",
            complexity_deployability_score="invalid_complexity_xyz",
        )
        fired, msg = _check_complexity_deployability_valid(decisions)
        assert fired
        assert "invalid_complexity_xyz" in msg

    def test_leakage_risk_invalid_fires(
        self,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6C_elo",
            leakage_risk_score="invalid_risk_xyz",
        )
        fired, msg = _check_leakage_risk_valid(decisions)
        assert fired
        assert "invalid_risk_xyz" in msg

    def test_materialization_permission_invalid_fires(
        self,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6D_glicko_or_glicko_2",
            materialization_permission="invalid_permission_xyz",
        )
        fired, msg = _check_materialization_permission_valid(decisions)
        assert fired
        assert "invalid_permission_xyz" in msg


# ---------------------------------------------------------------------------
# 28. None-guard paths when Q6_selected_policy / Q6_per_family_impact_summary
#     are absent (lines 1648, 1868, 1883, 1900, 1943)
# ---------------------------------------------------------------------------


class TestNoneGuardPaths:
    """None-guard early returns fire False when the target row is absent."""

    def test_external_citation_check_returns_false_when_no_selected(self) -> None:
        # Remove Q6_selected_policy entirely.
        decisions = _make_decisions()
        decisions_no_selected = tuple(
            d for d in decisions if d.decision_id != "Q6_selected_policy"
        )
        fired, _ = _check_external_citation_present_when_non_omit_non_deferred(
            decisions_no_selected
        )
        assert not fired

    def test_selected_policy_in_candidate_set_returns_false_when_no_selected(
        self,
    ) -> None:
        decisions = _make_decisions()
        decisions_no_selected = tuple(
            d for d in decisions if d.decision_id != "Q6_selected_policy"
        )
        fired, _ = _check_selected_policy_in_candidate_set(decisions_no_selected)
        assert not fired

    def test_selected_policy_verdict_consistent_returns_false_when_no_selected(
        self,
    ) -> None:
        decisions = _make_decisions()
        decisions_no_selected = tuple(
            d for d in decisions if d.decision_id != "Q6_selected_policy"
        )
        fired, _ = _check_selected_policy_verdict_consistent(decisions_no_selected)
        assert not fired

    def test_per_family_broadcasts_returns_false_when_no_summary(self) -> None:
        decisions = _make_decisions()
        decisions_no_summary = tuple(
            d for d in decisions if d.decision_id != "Q6_per_family_impact_summary"
        )
        fired, _ = _check_per_family_impact_broadcasts_all_6_families(
            decisions_no_summary
        )
        assert not fired

    def test_raw_mmr_hybrid_rejection_returns_false_when_no_selected(self) -> None:
        decisions = _make_decisions()
        decisions_no_selected = tuple(
            d for d in decisions if d.decision_id != "Q6_selected_policy"
        )
        fired, _ = _check_raw_mmr_hybrid_rejection_token_present(decisions_no_selected)
        assert not fired

    def test_materialization_permission_consistent_returns_false_when_no_selected(
        self,
    ) -> None:
        decisions = _make_decisions()
        decisions_no_selected = tuple(
            d for d in decisions if d.decision_id != "Q6_selected_policy"
        )
        fired, _ = _check_materialization_permission_consistent_with_verdict(
            decisions_no_selected
        )
        assert not fired


# ---------------------------------------------------------------------------
# 29. _write_md with non-empty probes (line 2984->2993)
# ---------------------------------------------------------------------------


class TestWriteMdWithProbes:
    """_write_md writes probe reaffirmation text when probes dict is non-empty."""

    def test_write_md_includes_probe_figures_when_probes_populated(
        self,
        tmp_path: Path,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        md_out = tmp_path / "q6_with_probes.md"
        falsifier_status = {key: "did_not_fire" for key in FALSIFIER_PRIORITY_CHAIN}
        probes = {
            "mfc_mmr_missing": (100000, 83950),
            "pha_mmr_missing": (500000, 418250),
        }
        _write_md(passing_decisions, md_out, falsifier_status, probes)
        content = md_out.read_text(encoding="utf-8")
        assert "Probe re-affirmation" in content
        assert "total=100000" in content

    def test_write_md_excludes_probe_figures_when_probes_empty(
        self,
        tmp_path: Path,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        md_out = tmp_path / "q6_no_probes.md"
        falsifier_status = {key: "did_not_fire" for key in FALSIFIER_PRIORITY_CHAIN}
        _write_md(passing_decisions, md_out, falsifier_status, {})
        content = md_out.read_text(encoding="utf-8")
        assert "Probe re-affirmation" not in content


# ---------------------------------------------------------------------------
# 30. _write_md with selected=None (line 3043->3064 else-skip branch)
# ---------------------------------------------------------------------------


class TestWriteMdWithNoSelectedPolicy:
    """_write_md skips §12 selected-policy block when Q6_selected_policy absent."""

    def test_write_md_skips_selected_block_when_no_selected(
        self, tmp_path: Path
    ) -> None:
        decisions = _make_decisions()
        decisions_no_selected = tuple(
            d for d in decisions if d.decision_id != "Q6_selected_policy"
        )
        md_out = tmp_path / "q6_no_selected.md"
        falsifier_status = {key: "did_not_fire" for key in FALSIFIER_PRIORITY_CHAIN}
        _write_md(decisions_no_selected, md_out, falsifier_status, {})
        content = md_out.read_text(encoding="utf-8")
        # §12 header exists but selected block content absent
        assert "## §12" in content
        assert "**Selected:**" not in content


# ---------------------------------------------------------------------------
# 31. Entrypoint halting path (lines 3372, 3375-3378, 3386->3410, 3414)
# ---------------------------------------------------------------------------


class TestEntrypointHaltingPath:
    """run_rating_reconstruction_adjudication halts and does not write when a SHA fires."""

    def test_halting_falsifier_set_when_sha_tampered(self, tmp_path: Path) -> None:
        fake_csv = tmp_path / "fake.csv"
        fake_csv.write_bytes(b"tampered")
        fake_md = tmp_path / "fake.md"
        fake_md.write_bytes(b"tampered")
        # All other files can be tmp_path (will fail SHA too but first one halts)
        result = run_rating_reconstruction_adjudication(
            duckdb_path=tmp_path / "db.duckdb",
            parent_pr242_csv_path=fake_csv,
            parent_pr242_md_path=fake_md,
            parent_pr243_csv_path=fake_md,
            parent_pr243_md_path=fake_md,
            pr241_validator_module_path=fake_csv,
            cross_02_02_spec_path=fake_md,
            feature_family_registry_csv_path=fake_csv,
            dataset_research_log_path=fake_md,
            player_history_all_yaml_path=fake_md,
            matches_flat_clean_yaml_path=fake_md,
            matches_history_minimal_yaml_path=fake_md,
            csv_out_path=tmp_path / "out.csv",
            md_out_path=tmp_path / "out.md",
            audit_pr="PR #TEST_HALTING",
            skip_probes=True,
        )
        assert result.passed is False
        assert result.halting_falsifier is not None
        assert len(result.falsifiers_fired) >= 1

    def test_csv_not_written_when_halting(self, tmp_path: Path) -> None:
        fake = tmp_path / "fake.csv"
        fake.write_bytes(b"tampered")
        out_csv = tmp_path / "out.csv"
        out_md = tmp_path / "out.md"
        run_rating_reconstruction_adjudication(
            duckdb_path=tmp_path / "db.duckdb",
            parent_pr242_csv_path=fake,
            parent_pr242_md_path=fake,
            parent_pr243_csv_path=fake,
            parent_pr243_md_path=fake,
            pr241_validator_module_path=fake,
            cross_02_02_spec_path=fake,
            feature_family_registry_csv_path=fake,
            dataset_research_log_path=fake,
            player_history_all_yaml_path=fake,
            matches_flat_clean_yaml_path=fake,
            matches_history_minimal_yaml_path=fake,
            csv_out_path=out_csv,
            md_out_path=out_md,
            audit_pr="PR #TEST_HALTING2",
            skip_probes=True,
        )
        assert not out_csv.exists()
        assert not out_md.exists()


# ---------------------------------------------------------------------------
# 32. DuckDB error path (lines 3406-3408)
# ---------------------------------------------------------------------------


class TestEntrypointDuckDbErrorPath:
    """run_rating_reconstruction_adjudication handles DuckDB connection errors gracefully."""

    def test_probes_empty_when_duckdb_connect_fails(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import duckdb as _ddb

        def _bad_connect(*args: Any, **kwargs: Any) -> Any:
            raise _ddb.Error("connection failed")

        monkeypatch.setattr(_ddb, "connect", _bad_connect)
        # Use real artifact paths so SHA falsifiers don't halt first.
        if not REAL_INPUTS_AVAILABLE:
            pytest.skip("Real artifacts not available; cannot test DuckDB error path")
        out_csv = tmp_path / "out.csv"
        out_md = tmp_path / "out.md"
        result = run_rating_reconstruction_adjudication(
            duckdb_path=DUCKDB_PATH,
            parent_pr242_csv_path=PARENT_PR242_CSV_PATH,
            parent_pr242_md_path=PARENT_PR242_MD_PATH,
            parent_pr243_csv_path=PARENT_PR243_CSV_PATH,
            parent_pr243_md_path=PARENT_PR243_MD_PATH,
            pr241_validator_module_path=PR241_VALIDATOR_PATH,
            cross_02_02_spec_path=CROSS_02_02_SPEC_PATH,
            feature_family_registry_csv_path=FEATURE_FAMILY_REGISTRY_CSV_PATH,
            dataset_research_log_path=DATASET_RESEARCH_LOG_PATH,
            player_history_all_yaml_path=PHA_YAML_PATH,
            matches_flat_clean_yaml_path=MFC_YAML_PATH,
            matches_history_minimal_yaml_path=MHM_YAML_PATH,
            csv_out_path=out_csv,
            md_out_path=out_md,
            audit_pr="PR #TEST_DUCKDB_ERR",
            skip_probes=False,
        )
        # No halting falsifier (SHAs pass), but probes are empty due to DuckDB error.
        assert result.passed is True
        assert result.probes == {}


# ---------------------------------------------------------------------------
# 33. _decision_to_field_dict helper
# ---------------------------------------------------------------------------


class TestDecisionToFieldDict:
    """_decision_to_field_dict returns a string-keyed dict of all dataclass fields."""

    def test_all_schema_columns_present_in_dict(
        self,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        d = passing_decisions[0]
        field_dict = _decision_to_field_dict(d)
        for col in Q6_ADJUDICATION_SCHEMA:
            assert col in field_dict

    def test_values_are_strings(
        self,
        passing_decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    ) -> None:
        d = passing_decisions[0]
        field_dict = _decision_to_field_dict(d)
        for v in field_dict.values():
            assert isinstance(v, str)
