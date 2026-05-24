"""Tests for the SC2EGSet history-enriched pre_game adjudicator.

Covers module-shape invariants, per-Q decision content, every falsifier in
``FALSIFIER_PRIORITY_CHAIN``, the B-X1 forbidden-token scope+exempt split, the
B-X2 canonical strict-< discipline, deterministic CSV schema, halt-before-
artifact behavior, no-status-yaml/no-feature-materialization guarantees, and
real-input smoke tests gated by ``@pytest.mark.skipif``.
"""

from __future__ import annotations

import csv
import inspect
import re
from dataclasses import fields, replace
from pathlib import Path
from typing import Any

import pytest

from rts_predict.games.sc2.datasets.sc2egset import (
    adjudicate_history_enriched_pre_game_source_layer as adj_mod,
)
from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import (  # noqa: E501
    ADJUDICATION_CSV_REL,
    ADJUDICATION_MD_REL,
    EXPECTED_PR241_VALIDATOR_SHA256,
    FALSIFIER_PRIORITY_CHAIN,
    HELPER_TO_FALSIFIER_KEY,
    IN_GAME_HISTORICAL_COLUMNS_IN_SCOPE_PIPE,
    POST_GAME_TOKEN_EXEMPT_FIELDS,
    POST_GAME_TOKEN_SCOPED_FIELDS,
    POST_GAME_TOKENS,
    PR241_VALIDATOR_MODULE_PATH,
    PROVENANCE_SHA_FIELDS,
    Q_DECISION_IDS,
    STRICT_LT_FILTER_ROADMAP_RAW,
    STRICT_LT_HISTORY_FILTER,
    HistoryEnrichedAdjudicationDecision,
    _build_decisions,
    _check_decision_count,
    _check_forbidden_post_game_feature_tokens,
    _check_in_game_historical_strict_lt,
    _check_materialization_creep,
    _check_no_not_found_sha_fields,
    _check_pr241_sha256_match,
    _check_q1_single_row_per_n5,
    _check_q1_source_layer_evidence_consistent,
    _check_q2_target_anchor_type_match,
    _check_q3_history_time_column_dtype,
    _check_q3_monotonicity_smoke,
    _check_q4_cold_start_gates_complete,
    _check_q4_no_leakage_in_cold_start,
    _check_q5_cross_region_three_options_enumerated,
    _check_q6_rating_default_deferred,
    _check_q6_rating_forward_only,
    _check_q7_in_game_historical_columns_in_scope,
    _check_q7_no_target_match_tracker,
    _check_q8_mhm_documented,
    _check_strict_lt_filter_divergence,
    _check_universal_no_tracker_source,
    _sha256_file,
    adjudicate_history_enriched_pre_game_source_layer,
)

# ---------------------------------------------------------------------------
# Repo-relative paths
# ---------------------------------------------------------------------------

_TESTS_ROOT = Path(__file__).resolve().parents[6]

REGISTRY_CSV_PATH: Path = (
    _TESTS_ROOT
    / "src"
    / "rts_predict"
    / "games"
    / "sc2"
    / "datasets"
    / "sc2egset"
    / "reports"
    / "artifacts"
    / "02_feature_engineering"
    / "01_pre_game_vs_in_game_boundary"
    / "02_01_01_feature_family_registry.csv"
)
PR234_BINDING_CSV_PATH: Path = (
    _TESTS_ROOT
    / "src"
    / "rts_predict"
    / "games"
    / "sc2"
    / "datasets"
    / "sc2egset"
    / "reports"
    / "artifacts"
    / "02_feature_engineering"
    / "01_pre_game_vs_in_game_boundary"
    / "02_01_02_source_anchor_race_adjudication.csv"
)
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
PR241_VALIDATOR_PATH: Path = _TESTS_ROOT / PR241_VALIDATOR_MODULE_PATH


VALID_SHA: str = EXPECTED_PR241_VALIDATOR_SHA256
ALT_VALID_SHA: str = "a" * 64

# ---------------------------------------------------------------------------
# Common synthetic-decision builder
# ---------------------------------------------------------------------------

_COMMON_PROVENANCE: dict[str, str] = {
    "audit_pr": "PR #242",
    "provenance_git_sha": "0" * 40,
    "pr241_scaffold_validator_module_sha256": VALID_SHA,
    "roadmap_sha256": ALT_VALID_SHA,
    "registry_csv_sha256": ALT_VALID_SHA,
    "matches_history_minimal_yaml_sha256": ALT_VALID_SHA,
    "cross_02_00_spec_sha256": ALT_VALID_SHA,
    "cross_02_01_spec_sha256": ALT_VALID_SHA,
    "cross_02_02_spec_sha256": ALT_VALID_SHA,
    "cross_02_03_spec_sha256": ALT_VALID_SHA,
    "materialized_output_paths": "",
}


@pytest.fixture()
def passing_decisions() -> tuple[HistoryEnrichedAdjudicationDecision, ...]:
    """Build the canonical 8-decision tuple via the module's own builder."""
    return _build_decisions(
        audit_pr="PR #242",
        provenance_git_sha="0" * 40,
        pr241_sha256=VALID_SHA,
        roadmap_sha256=ALT_VALID_SHA,
        registry_csv_sha256=ALT_VALID_SHA,
        matches_history_minimal_yaml_sha256=ALT_VALID_SHA,
        cross_02_00_spec_sha256=ALT_VALID_SHA,
        cross_02_01_spec_sha256=ALT_VALID_SHA,
        cross_02_02_spec_sha256=ALT_VALID_SHA,
        cross_02_03_spec_sha256=ALT_VALID_SHA,
    )


def _replace_row(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
    target_id: str,
    **kwargs: Any,
) -> tuple[HistoryEnrichedAdjudicationDecision, ...]:
    """Return a new tuple with the named decision row replaced by ``replace(d, **kwargs)``."""
    out: list[HistoryEnrichedAdjudicationDecision] = []
    for d in decisions:
        if d.decision_id == target_id:
            out.append(replace(d, **kwargs))
        else:
            out.append(d)
    return tuple(out)


def _by_id(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
    decision_id: str,
) -> HistoryEnrichedAdjudicationDecision:
    for d in decisions:
        if d.decision_id == decision_id:
            return d
    raise AssertionError(f"decision_id {decision_id!r} not found")


# ---------------------------------------------------------------------------
# Module-shape tests
# ---------------------------------------------------------------------------


class TestModuleConstants:
    """Module-level constants must satisfy their declared shapes."""

    def test_q_decision_ids_length_is_eight(self) -> None:
        assert len(Q_DECISION_IDS) == 8

    def test_expected_pr241_sha_is_lowercase_hex_64(self) -> None:
        assert len(EXPECTED_PR241_VALIDATOR_SHA256) == 64
        assert re.fullmatch(r"[0-9a-f]{64}", EXPECTED_PR241_VALIDATOR_SHA256)
        assert EXPECTED_PR241_VALIDATOR_SHA256 == (
            "b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904"
        )

    def test_strict_lt_history_filter_form(self) -> None:
        assert STRICT_LT_HISTORY_FILTER.startswith("TRY_CAST")
        assert STRICT_LT_HISTORY_FILTER == (
            "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"
        )

    def test_strict_lt_filter_roadmap_raw_form(self) -> None:
        assert STRICT_LT_FILTER_ROADMAP_RAW == (
            "ph.details_timeUTC < target.started_at"
        )

    def test_helper_to_falsifier_key_length_is_21(self) -> None:
        assert len(HELPER_TO_FALSIFIER_KEY) == 21

    def test_falsifier_priority_chain_length_is_21(self) -> None:
        assert len(FALSIFIER_PRIORITY_CHAIN) == 21

    def test_helper_map_values_match_priority_chain(self) -> None:
        assert set(HELPER_TO_FALSIFIER_KEY.values()) == set(FALSIFIER_PRIORITY_CHAIN)

    def test_provenance_sha_fields_length_is_8(self) -> None:
        assert len(PROVENANCE_SHA_FIELDS) == 8


class TestForbiddenTokensExemptFieldsList:
    """B-X1 scope and exempt sets must be disjoint and have the documented contents."""

    def test_scoped_and_exempt_are_disjoint(self) -> None:
        assert POST_GAME_TOKEN_SCOPED_FIELDS.isdisjoint(POST_GAME_TOKEN_EXEMPT_FIELDS)

    @pytest.mark.parametrize(
        "field_name",
        [
            "notes",
            "evidence_paths",
            "falsifiers",
            "decision_name",
            "source_layer_divergence_reason",
            "history_source_extension_reason",
        ],
    )
    def test_field_is_exempt(self, field_name: str) -> None:
        assert field_name in POST_GAME_TOKEN_EXEMPT_FIELDS

    @pytest.mark.parametrize(
        "field_name",
        [
            "selected_source_layer",
            "target_anchor",
            "feature_family_id_or_scope",
            "materialized_output_paths",
        ],
    )
    def test_field_is_scoped(self, field_name: str) -> None:
        assert field_name in POST_GAME_TOKEN_SCOPED_FIELDS


class TestDataclassFieldCount:
    """The dataclass must declare exactly 33 fields."""

    def test_thirty_three_fields(self) -> None:
        assert len(fields(HistoryEnrichedAdjudicationDecision)) == 33


# ---------------------------------------------------------------------------
# Per-Q decision-row tests (synthetic happy-path uses _build_decisions)
# ---------------------------------------------------------------------------


class TestQ1SubfieldDisambiguation:
    """Q1 row carries both divergence and extension reason narratives."""

    def test_q1_n_x4_subfields_populated(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q1 = _by_id(passing_decisions, "Q1_source_layer")
        assert q1.source_layer_divergence_reason
        assert q1.history_source_extension_reason


class TestQ1SingleRowPerN5:
    """A 9-decision tuple with Q1 split into Q1a/Q1b halts on q1_single_row_violation."""

    def test_q1_split_fires_falsifier(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q1 = _by_id(passing_decisions, "Q1_source_layer")
        q1a = replace(q1, decision_id="Q1a_source_layer_target")
        q1b = replace(q1, decision_id="Q1b_source_layer_history")
        decisions = (q1a, q1b) + tuple(
            d for d in passing_decisions if d.decision_id != "Q1_source_layer"
        )
        assert len(decisions) == 9
        did_fire, msg = _check_q1_single_row_per_n5(decisions)
        assert did_fire
        assert "exactly 1 row" in msg


class TestQ2TargetAnchorPresent:
    """Q2 target_anchor references matches_history_minimal.started_at."""

    def test_q2_anchor_contains_started_at(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q2 = _by_id(passing_decisions, "Q2_target_anchor")
        assert "matches_history_minimal.started_at" in q2.target_anchor or (
            "started_at" in q2.target_anchor
        )
        # The build_q2 binding contains "matches_history_minimal.started_at TIMESTAMP"
        assert "matches_history_minimal.started_at" in q2.target_anchor


class TestQ3StrictLtExpressionPresent:
    """Q3 strict_lt_expression equals the canonical TRY_CAST filter."""

    def test_q3_strict_lt_matches_canonical(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q3 = _by_id(passing_decisions, "Q3_history_time_column")
        assert q3.strict_lt_expression == STRICT_LT_HISTORY_FILTER


class TestQ4ColdStartPolicyComplete:
    """Q4 cold_start_policy enumerates G-CS-2..G-CS-6."""

    @pytest.mark.parametrize("gate", ["G-CS-2", "G-CS-3", "G-CS-4", "G-CS-5", "G-CS-6"])
    def test_q4_policy_mentions_gate(
        self,
        passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
        gate: str,
    ) -> None:
        q4 = _by_id(passing_decisions, "Q4_cold_start_policy")
        assert gate in q4.cold_start_policy


class TestQ5CrossRegionDeferred:
    """Q5 row is deferred and notes enumerate all 3 options."""

    def test_q5_cross_region_policy_is_deferred(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q5 = _by_id(passing_decisions, "Q5_cross_region_policy")
        assert q5.cross_region_policy == "deferred_blocker"

    @pytest.mark.parametrize(
        "option",
        [
            "strict_exclusion",
            "dual_feature_path",
            "sensitivity_indicator_co_registration",
        ],
    )
    def test_q5_notes_enumerate_option(
        self,
        passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
        option: str,
    ) -> None:
        q5 = _by_id(passing_decisions, "Q5_cross_region_policy")
        assert option in q5.notes


class TestQ6RatingDeferred:
    """Q6 rating_policy is deferred and notes contain N-X3 rationale + forward-only."""

    def test_q6_rating_policy_is_deferred(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q6 = _by_id(passing_decisions, "Q6_rating_policy")
        assert q6.rating_policy == "deferred_blocker"

    @pytest.mark.parametrize(
        "phrase",
        [
            "deferred_blocker because:",
            "no target-match outcome",
            "no future results",
            "no global batch fit",
        ],
    )
    def test_q6_notes_contain_phrase(
        self,
        passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
        phrase: str,
    ) -> None:
        q6 = _by_id(passing_decisions, "Q6_rating_policy")
        assert phrase in q6.notes


class TestQ7InGameHistoricalColumnsInScope:
    """Q7 in_game_historical_columns_in_scope equals the canonical pipe-separated form."""

    def test_q7_columns_match_canonical(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q7 = _by_id(passing_decisions, "Q7_in_game_historical_policy")
        assert q7.in_game_historical_columns_in_scope == (
            "APM|SQ|supplyCappedPercent|header_elapsedGameLoops"
        )
        assert (
            q7.in_game_historical_columns_in_scope
            == IN_GAME_HISTORICAL_COLUMNS_IN_SCOPE_PIPE
        )


class TestQ7StrictLtExpressionPresent:
    """Q7 strict_lt_expression equals the canonical TRY_CAST filter."""

    def test_q7_strict_lt_matches_canonical(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q7 = _by_id(passing_decisions, "Q7_in_game_historical_policy")
        assert q7.strict_lt_expression == STRICT_LT_HISTORY_FILTER


class TestQ8MhmDocumentation:
    """Q8 carries the NOT_A_FEATURE_SOURCE scope and cites both MHM purposes."""

    def test_q8_scope_is_not_a_feature_source(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q8 = _by_id(passing_decisions, "Q8_matches_history_minimal_consumption")
        assert "NOT_A_FEATURE_SOURCE" in q8.feature_family_id_or_scope

    def test_q8_notes_cite_both_purposes(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q8 = _by_id(passing_decisions, "Q8_matches_history_minimal_consumption")
        assert "target row identity" in q8.notes
        assert "started_at" in q8.notes
        assert "cold-start enumeration" in q8.notes


# ---------------------------------------------------------------------------
# Per-falsifier tests
# ---------------------------------------------------------------------------


class TestPr241Sha256Match:
    """N4: PR #241 SHA mismatch halts on pr241_sha256_mismatch."""

    @pytest.mark.parametrize(
        "bad_sha",
        [
            "NOT_FOUND",
            "",
            "a" * 63,
            "A" * 64,
            "Z" * 64,
            "0" * 63 + "X",
            "deadbeef" * 8,  # valid hex but != EXPECTED
        ],
    )
    def test_invalid_sha_fires_falsifier(
        self,
        passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
        bad_sha: str,
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q1_source_layer",
            pr241_scaffold_validator_module_sha256=bad_sha,
        )
        did_fire, _msg = _check_pr241_sha256_match(decisions)
        assert did_fire

    def test_canonical_sha_passes(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        did_fire, _msg = _check_pr241_sha256_match(passing_decisions)
        assert not did_fire


class TestProvenanceShaInvalid:
    """Any provenance SHA field of 'NOT_FOUND' on any row halts on provenance_sha_invalid."""

    @pytest.mark.parametrize(
        "field_name",
        sorted(PROVENANCE_SHA_FIELDS - {"pr241_scaffold_validator_module_sha256"}),
    )
    def test_not_found_sha_fires(
        self,
        passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
        field_name: str,
    ) -> None:
        decisions = _replace_row(
            passing_decisions, "Q3_history_time_column", **{field_name: "NOT_FOUND"}
        )
        did_fire, msg = _check_no_not_found_sha_fields(decisions)
        assert did_fire
        assert field_name in msg

    def test_empty_sha_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions, "Q2_target_anchor", roadmap_sha256=""
        )
        did_fire, _msg = _check_no_not_found_sha_fields(decisions)
        assert did_fire

    def test_wrong_length_sha_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions, "Q2_target_anchor", roadmap_sha256="a" * 60
        )
        did_fire, _msg = _check_no_not_found_sha_fields(decisions)
        assert did_fire

    def test_uppercase_sha_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions, "Q2_target_anchor", roadmap_sha256="A" * 64
        )
        did_fire, _msg = _check_no_not_found_sha_fields(decisions)
        assert did_fire


class TestDecisionCountMismatch:
    """A 7-decision tuple halts on decision_count_mismatch."""

    def test_seven_decisions_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q8_id = "Q8_matches_history_minimal_consumption"
        decisions = tuple(d for d in passing_decisions if d.decision_id != q8_id)
        assert len(decisions) == 7
        did_fire, msg = _check_decision_count(decisions)
        assert did_fire
        assert "Expected exactly 8" in msg

    def test_eight_decisions_with_wrong_id_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        # Replace Q8 with a duplicate of Q1 so the count is 8 but IDs mismatch
        decisions = _replace_row(
            passing_decisions,
            "Q8_matches_history_minimal_consumption",
            decision_id="Q9_unexpected",
        )
        did_fire, msg = _check_decision_count(decisions)
        assert did_fire
        assert "Decision IDs mismatch" in msg


class TestQ1SourceLayerEvidenceConsistent:
    """Q1 target source layer mismatch with matches_flat_clean halts."""

    def test_wrong_target_source_layer_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q1_source_layer",
            selected_target_source_layer="matches_flat",
        )
        did_fire, msg = _check_q1_source_layer_evidence_consistent(decisions, {})
        assert did_fire
        assert "matches_flat_clean" in msg

    def test_pr234_binding_inconsistency_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        pr234 = {"Q1_source_layer": {"chosen": "some_other_table"}}
        did_fire, msg = _check_q1_source_layer_evidence_consistent(
            passing_decisions, pr234
        )
        assert did_fire
        assert "matches_flat_clean" in msg

    def test_passes_when_consistent(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        did_fire, _msg = _check_q1_source_layer_evidence_consistent(
            passing_decisions, {}
        )
        assert not did_fire


class TestQ2TargetAnchorTypeMismatch:
    """Q2 target_anchor lacking TIMESTAMP halts on q2_target_anchor_type_mismatch."""

    def test_missing_timestamp_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q2_target_anchor",
            target_anchor="matches_history_minimal.started_at",
        )
        meta = {"matches_history_minimal.started_at": {"dtype": "TIMESTAMP", "exists": True}}
        did_fire, _msg = _check_q2_target_anchor_type_match(decisions, meta)
        assert did_fire

    def test_dtype_mismatch_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        meta = {"matches_history_minimal.started_at": {"dtype": "VARCHAR", "exists": True}}
        did_fire, _msg = _check_q2_target_anchor_type_match(passing_decisions, meta)
        assert did_fire


class TestQ3HistoryTimeColumnInvalid:
    """Q3 history_time_column missing details_timeUTC halts."""

    def test_empty_history_time_column_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions, "Q3_history_time_column", history_time_column=""
        )
        meta = {"player_history_all.details_timeUTC": {"dtype": "VARCHAR", "exists": True}}
        did_fire, _msg = _check_q3_history_time_column_dtype(decisions, meta)
        assert did_fire

    def test_missing_metadata_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        meta = {"player_history_all.details_timeUTC": {"dtype": "", "exists": False}}
        did_fire, _msg = _check_q3_history_time_column_dtype(passing_decisions, meta)
        assert did_fire


class TestQ3StrictLtSmokeFailed:
    """Q3 smoke probe returning > 0 self-rows halts on q3_strict_lt_smoke_failed."""

    def test_nonzero_self_rows_fires(self) -> None:
        smoke = {"self_join_rows": 1, "try_cast_null_in_sample": 0}
        did_fire, msg = _check_q3_monotonicity_smoke(smoke)
        assert did_fire
        assert "self-rows" in msg

    def test_nonzero_try_cast_null_fires(self) -> None:
        smoke = {"self_join_rows": 0, "try_cast_null_in_sample": 5}
        did_fire, msg = _check_q3_monotonicity_smoke(smoke)
        assert did_fire
        assert "TRY_CAST" in msg

    def test_clean_smoke_passes(self) -> None:
        smoke = {"self_join_rows": 0, "try_cast_null_in_sample": 0}
        did_fire, _msg = _check_q3_monotonicity_smoke(smoke)
        assert not did_fire

    def test_non_integer_self_rows_fires(self) -> None:
        smoke = {"self_join_rows": None, "try_cast_null_in_sample": 0}
        did_fire, _msg = _check_q3_monotonicity_smoke(smoke)
        assert did_fire


class TestQ4ColdStartGatesIncomplete:
    """Q4 missing any of G-CS-2..6 halts on q4_cold_start_gates_incomplete."""

    def test_missing_g_cs_3_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q4 = _by_id(passing_decisions, "Q4_cold_start_policy")
        truncated = q4.cold_start_policy.replace("G-CS-3", "G-CS-9")
        decisions = _replace_row(
            passing_decisions, "Q4_cold_start_policy", cold_start_policy=truncated
        )
        did_fire, msg = _check_q4_cold_start_gates_complete(decisions)
        assert did_fire
        assert "G-CS-3" in msg

    def test_missing_g_cs_6_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q4 = _by_id(passing_decisions, "Q4_cold_start_policy")
        truncated = q4.cold_start_policy.replace("G-CS-6", "G-CS-X")
        decisions = _replace_row(
            passing_decisions, "Q4_cold_start_policy", cold_start_policy=truncated
        )
        did_fire, msg = _check_q4_cold_start_gates_complete(decisions)
        assert did_fire
        assert "G-CS-6" in msg


class TestQ4ColdStartLeakage:
    """Q4 notes omitting `match_time < T` halts on q4_cold_start_leakage."""

    def test_missing_leakage_phrase_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q4 = _by_id(passing_decisions, "Q4_cold_start_policy")
        bad_notes = q4.notes.replace("match_time < T", "match_time UNDEFINED")
        decisions = _replace_row(
            passing_decisions, "Q4_cold_start_policy", notes=bad_notes
        )
        did_fire, _msg = _check_q4_no_leakage_in_cold_start(decisions)
        assert did_fire


class TestQ5CrossRegionThreeOptions:
    """Q5 notes failing to enumerate all 3 options halts."""

    def test_only_two_options_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q5 = _by_id(passing_decisions, "Q5_cross_region_policy")
        bad_notes = q5.notes.replace(
            "sensitivity_indicator_co_registration", "REDACTED_OPTION"
        )
        decisions = _replace_row(
            passing_decisions, "Q5_cross_region_policy", notes=bad_notes
        )
        did_fire, _msg = _check_q5_cross_region_three_options_enumerated(decisions)
        assert did_fire

    def test_bad_policy_value_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q5_cross_region_policy",
            cross_region_policy="some_unknown_policy",
        )
        did_fire, _msg = _check_q5_cross_region_three_options_enumerated(decisions)
        assert did_fire


class TestQ6RatingEvidenceSufficiency:
    """Q6 N-X3 strengthened evidence sufficiency: 4 branches."""

    def test_deferred_pass(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        # The canonical Q6 from _build_q6 already meets the deferred-pass
        # contract (deferred_blocker + non-empty evidence + the
        # "deferred_blocker because:" phrase + the 3 forward-only phrases).
        did_fire, _msg = _check_q6_rating_default_deferred(passing_decisions)
        assert not did_fire

    def test_deferred_fail_no_rationale_phrase(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q6 = _by_id(passing_decisions, "Q6_rating_policy")
        bad_notes = q6.notes.replace("deferred_blocker because:", "deferred because:")
        decisions = _replace_row(passing_decisions, "Q6_rating_policy", notes=bad_notes)
        did_fire, msg = _check_q6_rating_default_deferred(decisions)
        assert did_fire
        assert "deferred_blocker because:" in msg

    def test_deferred_fail_empty_evidence(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions, "Q6_rating_policy", evidence_paths="   \n  "
        )
        did_fire, msg = _check_q6_rating_default_deferred(decisions)
        assert did_fire
        assert "evidence_paths" in msg

    def test_bind_pass_with_full_evidence(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        evidence = "\n".join(
            ["src/some/repo/path.py", "Glickman (1999)"]
        )
        # Build notes that include forward-only, cold-start, and missingness wording.
        notes = (
            "Forward-only constraint explicit: no target-match outcome; "
            "no future results; no global batch fit. "
            "cold-start handled by initializing rating = literature-prior; "
            "missingness handled by retaining is_mmr_missing companion."
        )
        decisions = _replace_row(
            passing_decisions,
            "Q6_rating_policy",
            rating_policy="glicko2",
            evidence_paths=evidence,
            notes=notes,
        )
        did_fire, msg = _check_q6_rating_default_deferred(decisions)
        assert not did_fire, msg

    def test_bind_fail_no_repo_path_only_citation(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6_rating_policy",
            rating_policy="glicko2",
            evidence_paths="Glickman (1999)",
            notes="forward-only stuff",
        )
        did_fire, msg = _check_q6_rating_default_deferred(decisions)
        assert did_fire
        assert "repo-path" in msg

    def test_bind_fail_missing_forward_only_phrase(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6_rating_policy",
            rating_policy="glicko2",
            evidence_paths="src/some/repo/path.py\nGlickman (1999)",
            notes="no target-match outcome only; other forward-only phrases missing",
        )
        did_fire, msg = _check_q6_rating_default_deferred(decisions)
        assert did_fire
        assert "forward-only" in msg

    def test_bind_fail_missing_cold_start_phrase(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6_rating_policy",
            rating_policy="glicko2",
            evidence_paths="src/some/repo/path.py\nGlickman (1999)",
            notes=(
                "no target-match outcome; no future results; no global batch fit. "
                "missingness handled by retaining is_mmr_missing."
            ),
        )
        did_fire, msg = _check_q6_rating_default_deferred(decisions)
        assert did_fire
        assert "cold-start handled by" in msg

    def test_bind_fail_missing_missingness_phrase(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6_rating_policy",
            rating_policy="glicko2",
            evidence_paths="src/some/repo/path.py\nGlickman (1999)",
            notes=(
                "no target-match outcome; no future results; no global batch fit. "
                "cold-start handled by literature-prior init."
            ),
        )
        did_fire, msg = _check_q6_rating_default_deferred(decisions)
        assert did_fire
        assert "missingness handled by" in msg

    def test_bind_fail_only_repo_path_no_citation(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q6_rating_policy",
            rating_policy="glicko2",
            evidence_paths="src/some/repo/path.py",
            notes="forward-only stuff but no citation",
        )
        did_fire, msg = _check_q6_rating_default_deferred(decisions)
        assert did_fire
        assert "citation" in msg

    def test_bind_fail_bad_policy_value(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions, "Q6_rating_policy", rating_policy="not_a_model"
        )
        did_fire, _msg = _check_q6_rating_default_deferred(decisions)
        assert did_fire


class TestQ6RatingForwardOnlyMissing:
    """Q6 notes missing any of the 3 forward-only phrases halts."""

    def test_missing_one_phrase_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q6 = _by_id(passing_decisions, "Q6_rating_policy")
        bad_notes = q6.notes.replace("no future results", "REDACTED_PHRASE")
        decisions = _replace_row(passing_decisions, "Q6_rating_policy", notes=bad_notes)
        did_fire, msg = _check_q6_rating_forward_only(decisions)
        assert did_fire
        assert "no future results" in msg


class TestQ7InGameHistoricalColumnsDrift:
    """Q7 columns differing from the canonical scope halts."""

    def test_truncated_columns_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q7_in_game_historical_policy",
            in_game_historical_columns_in_scope="APM|SQ",
        )
        did_fire, _msg = _check_q7_in_game_historical_columns_in_scope(decisions)
        assert did_fire


class TestQ7NoTargetMatchTrackerMissing:
    """Q7 notes omitting prior-match-only wording halts."""

    def test_missing_prior_matches_phrase_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q7 = _by_id(passing_decisions, "Q7_in_game_historical_policy")
        bad_notes = q7.notes.replace("prior matches", "all matches")
        bad_notes = bad_notes.replace("history_time < target_time", "ANY_TIME")
        decisions = _replace_row(
            passing_decisions, "Q7_in_game_historical_policy", notes=bad_notes
        )
        did_fire, _msg = _check_q7_no_target_match_tracker(decisions)
        assert did_fire


class TestInGameHistoricalStrictLt:
    """N2: Q7-specific strict-< token check (distinct from Q3 smoke and divergence)."""

    def test_unknown_policy_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q7_in_game_historical_policy",
            in_game_historical_policy="some_random_policy",
        )
        did_fire, _msg = _check_in_game_historical_strict_lt(decisions)
        assert did_fire

    def test_deferred_blocker_passes(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q7_in_game_historical_policy",
            in_game_historical_policy="deferred_blocker",
        )
        did_fire, _msg = _check_in_game_historical_strict_lt(decisions)
        assert not did_fire

    def test_helper_key_distinct_from_others(self) -> None:
        # Confirms this is a distinct entry in the helper map.
        assert (
            HELPER_TO_FALSIFIER_KEY["_check_in_game_historical_strict_lt"]
            == "in_game_historical_strict_lt_violated"
        )
        assert (
            HELPER_TO_FALSIFIER_KEY["_check_strict_lt_filter_divergence"]
            == "strict_lt_filter_divergence"
        )
        assert (
            HELPER_TO_FALSIFIER_KEY["_check_q3_monotonicity_smoke"]
            == "q3_strict_lt_smoke_failed"
        )


class TestQ8MhmDocumentationMissing:
    """Q8 notes omitting any required MHM-purpose phrase halts."""

    def test_missing_phrase_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        q8 = _by_id(passing_decisions, "Q8_matches_history_minimal_consumption")
        bad_notes = q8.notes.replace("cold-start enumeration", "REDACTED")
        decisions = _replace_row(
            passing_decisions,
            "Q8_matches_history_minimal_consumption",
            notes=bad_notes,
        )
        did_fire, _msg = _check_q8_mhm_documented(decisions)
        assert did_fire

    def test_wrong_scope_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q8_matches_history_minimal_consumption",
            feature_family_id_or_scope="something_else",
        )
        did_fire, _msg = _check_q8_mhm_documented(decisions)
        assert did_fire


class TestUniversalPostGameToken:
    """B-X1: POST-GAME tokens in SCOPED fields halt; tokens in EXEMPT fields do not."""

    @pytest.mark.parametrize("token", sorted(POST_GAME_TOKENS))
    def test_token_in_scoped_field_fires(
        self,
        passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
        token: str,
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q1_source_layer",
            selected_source_layer=f"some_{token}_table",
        )
        did_fire, msg = _check_forbidden_post_game_feature_tokens(decisions)
        assert did_fire
        assert token in msg


class TestNegativeRationaleAllowedInNotes:
    """B-X1 positive companion: forward-only phrases in notes (EXEMPT) must not halt."""

    def test_q6_forward_only_phrases_pass(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        # The canonical Q6 notes contain "no target-match outcome; no future
        # results; no global batch fit" verbatim. The token scan must not fire.
        did_fire, msg = _check_forbidden_post_game_feature_tokens(passing_decisions)
        assert not did_fire, msg
        q6 = _by_id(passing_decisions, "Q6_rating_policy")
        assert (
            "no target-match outcome" in q6.notes
            and "no future results" in q6.notes
            and "no global batch fit" in q6.notes
        )


class TestDirectTargetMatchOutcomeRejected:
    """B-X1 scoped: 'outcome' in a SCOPED field halts; same text in notes (exempt) passes."""

    def test_outcome_in_scoped_field_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q4_cold_start_policy",
            feature_family_id_or_scope="target_match_outcome",
        )
        did_fire, msg = _check_forbidden_post_game_feature_tokens(decisions)
        assert did_fire
        assert "outcome" in msg

    def test_outcome_in_notes_does_not_fire(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q4_cold_start_policy",
            notes=(
                "Three failure modes (target_match_outcome leakage): rolling "
                "aggregates, head-to-head, co-occurring matches. Only "
                "match_time < T evidence used."
            ),
        )
        did_fire, _msg = _check_forbidden_post_game_feature_tokens(decisions)
        assert not did_fire


class TestUniversalTrackerSourceInHistory:
    """Q1 selected_history_source_layer containing tracker_events_raw halts."""

    def test_tracker_in_history_layer_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q1_source_layer",
            selected_history_source_layer="tracker_events_raw.PlayerStats",
        )
        did_fire, msg = _check_universal_no_tracker_source(decisions)
        assert did_fire
        assert "tracker_events_raw" in msg


class TestMaterializationCreepRejected:
    """Any row with non-empty materialized_output_paths halts."""

    def test_nonempty_materialized_paths_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q2_target_anchor",
            materialized_output_paths="reports/some/output.parquet",
        )
        did_fire, _msg = _check_materialization_creep(decisions)
        assert did_fire

    def test_all_empty_passes(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        did_fire, _msg = _check_materialization_creep(passing_decisions)
        assert not did_fire


class TestStrictLtFilterCanonicalAcrossSites:
    """B-X2: Q3 strict_lt_expression must equal canonical; mutation halts."""

    def test_q3_bare_lex_form_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q3_history_time_column",
            strict_lt_expression=STRICT_LT_FILTER_ROADMAP_RAW,
        )
        did_fire, msg = _check_strict_lt_filter_divergence(
            decisions, _smoke_sql_with_canonical()
        )
        assert did_fire
        assert "strict_lt_expression" in msg or "canonical" in msg

    def test_canonical_q3_passes(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        did_fire, msg = _check_strict_lt_filter_divergence(
            passing_decisions, _smoke_sql_with_canonical()
        )
        assert not did_fire, msg

    def test_smoke_sql_missing_canonical_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        did_fire, msg = _check_strict_lt_filter_divergence(
            passing_decisions, "SELECT 1"
        )
        assert did_fire
        assert "smoke probe" in msg.lower()

    def test_q7_canonical_mutation_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions,
            "Q7_in_game_historical_policy",
            strict_lt_expression=STRICT_LT_FILTER_ROADMAP_RAW,
        )
        did_fire, _msg = _check_strict_lt_filter_divergence(
            decisions, _smoke_sql_with_canonical()
        )
        assert did_fire


def _smoke_sql_with_canonical() -> str:
    """Helper: a minimal smoke SQL string that contains the canonical filter."""
    return f"SELECT COUNT(*) FROM t WHERE {STRICT_LT_HISTORY_FILTER}"


class TestRoadmapRawFormNotPropagated:
    """B-X2: STRICT_LT_FILTER_ROADMAP_RAW only appears as a constant declaration / message."""

    def test_roadmap_raw_constant_value(self) -> None:
        assert STRICT_LT_FILTER_ROADMAP_RAW == "ph.details_timeUTC < target.started_at"

    def test_bare_form_does_not_appear_as_executable_expression(self) -> None:
        source = inspect.getsource(adj_mod)
        # Count plain occurrences of the bare lex form
        occurrences = source.count("ph.details_timeUTC < target.started_at")
        # The bare form may appear in: (a) the constant declaration on the
        # right-hand side of `STRICT_LT_FILTER_ROADMAP_RAW = ...`, (b) format
        # strings or doc/notes that interpolate the constant (the bare form
        # could be present in a Q3 notes "raw form" string), and (c) potentially
        # docstrings / comments. Verify each occurrence is preceded by either a
        # constant-declaration token or an interpolation token, NOT a bare
        # executable usage.
        assert occurrences >= 1  # at least the constant declaration
        # Pattern: bare form must NOT appear as the body of a SQL `WHERE`
        # clause (would indicate an executable site).
        executable_pattern = re.compile(
            r"WHERE\s+ph\.details_timeUTC\s*<\s*target\.started_at",
            re.IGNORECASE,
        )
        assert not executable_pattern.search(source), (
            "STRICT_LT_FILTER_ROADMAP_RAW bare form must not appear as a SQL "
            "WHERE clause body in the module source"
        )


# ---------------------------------------------------------------------------
# Determinism / artifact-shape / boundary tests
# ---------------------------------------------------------------------------


class TestDeterministicCsvSchema:
    """CSV header line is byte-identical across two writes; 33 columns."""

    def test_header_byte_identical_across_writes(
        self,
        tmp_path: Path,
        passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
    ) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import (  # noqa: E501
            _write_csv,
        )

        path_a = tmp_path / "a.csv"
        path_b = tmp_path / "b.csv"
        _write_csv(passing_decisions, path_a)
        _write_csv(passing_decisions, path_b)
        header_a = path_a.read_text(encoding="utf-8").splitlines()[0]
        header_b = path_b.read_text(encoding="utf-8").splitlines()[0]
        assert header_a == header_b
        assert len(header_a.split(",")) == 33


class TestByteDeterminismModuloProvenance:
    """Two writes with identical inputs produce byte-identical CSV (no varying fields)."""

    def test_two_writes_byte_identical(
        self,
        tmp_path: Path,
        passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
    ) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import (  # noqa: E501
            _write_csv,
        )

        path_a = tmp_path / "a.csv"
        path_b = tmp_path / "b.csv"
        _write_csv(passing_decisions, path_a)
        _write_csv(passing_decisions, path_b)
        assert path_a.read_bytes() == path_b.read_bytes()


class TestCsvHeaderColumnCount:
    """CSV header has exactly 33 comma-separated column names."""

    def test_thirty_three_columns_in_header(
        self,
        tmp_path: Path,
        passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
    ) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import (  # noqa: E501
            _write_csv,
        )

        path = tmp_path / "out.csv"
        _write_csv(passing_decisions, path)
        with path.open(encoding="utf-8") as fh:
            reader = csv.reader(fh)
            header = next(reader)
        assert len(header) == 33


class TestNoStatusYamlChange:
    """Entrypoint writes no STEP_STATUS / PHASE_STATUS / research_log / ROADMAP file."""

    @pytest.mark.skipif(
        not (DUCKDB_PATH.exists() and REGISTRY_CSV_PATH.exists()),
        reason="Real DuckDB or registry CSV not present",
    )
    def test_no_status_yaml_writes(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        recorded_writes: list[str] = []

        original_write_text = Path.write_text
        original_write_bytes = Path.write_bytes

        def _record_text(self: Path, *args: Any, **kwargs: Any) -> int:
            recorded_writes.append(str(self))
            return original_write_text(self, *args, **kwargs)

        def _record_bytes(self: Path, *args: Any, **kwargs: Any) -> int:
            recorded_writes.append(str(self))
            return original_write_bytes(self, *args, **kwargs)

        monkeypatch.setattr(Path, "write_text", _record_text)
        monkeypatch.setattr(Path, "write_bytes", _record_bytes)

        csv_path = tmp_path / "out.csv"
        md_path = tmp_path / "out.md"
        adjudicate_history_enriched_pre_game_source_layer(
            duckdb_path=DUCKDB_PATH,
            registry_csv_path=REGISTRY_CSV_PATH,
            pr234_binding_csv_path=PR234_BINDING_CSV_PATH,
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #242",
            audit_date="2026-05-24",
        )

        forbidden_fragments = (
            "STEP_STATUS.yaml",
            "PIPELINE_SECTION_STATUS.yaml",
            "PHASE_STATUS.yaml",
            "research_log.md",
            "ROADMAP.md",
        )
        for w in recorded_writes:
            for frag in forbidden_fragments:
                assert frag not in w, (
                    f"Entrypoint wrote to forbidden target {w!r} (contains {frag!r})"
                )


class TestNoFeatureMaterialization:
    """Entrypoint writes no `.parquet` and nothing under reports/artifacts/02_01_03/."""

    @pytest.mark.skipif(
        not (DUCKDB_PATH.exists() and REGISTRY_CSV_PATH.exists()),
        reason="Real DuckDB or registry CSV not present",
    )
    def test_no_parquet_or_02_01_03_dir_writes(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        recorded_writes: list[str] = []
        original_write_text = Path.write_text
        original_write_bytes = Path.write_bytes

        def _record_text(self: Path, *args: Any, **kwargs: Any) -> int:
            recorded_writes.append(str(self))
            return original_write_text(self, *args, **kwargs)

        def _record_bytes(self: Path, *args: Any, **kwargs: Any) -> int:
            recorded_writes.append(str(self))
            return original_write_bytes(self, *args, **kwargs)

        monkeypatch.setattr(Path, "write_text", _record_text)
        monkeypatch.setattr(Path, "write_bytes", _record_bytes)

        csv_path = tmp_path / "out.csv"
        md_path = tmp_path / "out.md"
        adjudicate_history_enriched_pre_game_source_layer(
            duckdb_path=DUCKDB_PATH,
            registry_csv_path=REGISTRY_CSV_PATH,
            pr234_binding_csv_path=PR234_BINDING_CSV_PATH,
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #242",
            audit_date="2026-05-24",
        )

        for w in recorded_writes:
            assert not w.endswith(".parquet"), f"Entrypoint wrote parquet: {w!r}"
            assert "reports/artifacts/02_01_03" not in w, (
                f"Entrypoint wrote inside 02_01_03 artifact dir: {w!r}"
            )


class TestNoFilesWrittenOnHaltingFalsifier:
    """When a falsifier halts, the CSV and MD must NOT be written (halt-before-artifact)."""

    @pytest.mark.skipif(
        not (DUCKDB_PATH.exists() and REGISTRY_CSV_PATH.exists()),
        reason="Real DuckDB or registry CSV not present",
    )
    def test_halt_inhibits_csv_md(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Force a halt by monkeypatching the materialization_creep helper to
        # always return (True, "forced"). The entrypoint resolves the thunk
        # via `_build_falsifier_invocations` which calls the module-level
        # helper by name, so this monkeypatch is picked up.
        monkeypatch.setattr(
            adj_mod,
            "_check_materialization_creep",
            lambda _decisions: (True, "forced halt for testing"),
        )
        csv_path = tmp_path / "out.csv"
        md_path = tmp_path / "out.md"
        result = adjudicate_history_enriched_pre_game_source_layer(
            duckdb_path=DUCKDB_PATH,
            registry_csv_path=REGISTRY_CSV_PATH,
            pr234_binding_csv_path=PR234_BINDING_CSV_PATH,
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #242",
            audit_date="2026-05-24",
        )
        assert result.passed is False
        assert result.halting_falsifier == "materialization_creep"
        assert not csv_path.exists()
        assert not md_path.exists()


class TestNoArtifactPathDrift:
    """Entrypoint writes CSV/MD only to the caller-supplied paths."""

    @pytest.mark.skipif(
        not (DUCKDB_PATH.exists() and REGISTRY_CSV_PATH.exists()),
        reason="Real DuckDB or registry CSV not present",
    )
    def test_writes_to_supplied_paths(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "subdir" / "custom_name.csv"
        md_path = tmp_path / "subdir" / "custom_name.md"
        result = adjudicate_history_enriched_pre_game_source_layer(
            duckdb_path=DUCKDB_PATH,
            registry_csv_path=REGISTRY_CSV_PATH,
            pr234_binding_csv_path=PR234_BINDING_CSV_PATH,
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #242",
            audit_date="2026-05-24",
        )
        if result.passed:
            assert csv_path.exists()
            assert md_path.exists()
            assert result.csv_path == str(csv_path)
            assert result.md_path == str(md_path)

    def test_module_path_constants_present(self) -> None:
        assert ADJUDICATION_CSV_REL.endswith(
            "02_01_03_history_source_anchor_coldstart_adjudication.csv"
        )
        assert ADJUDICATION_MD_REL.endswith(
            "02_01_03_history_source_anchor_coldstart_adjudication.md"
        )


# ---------------------------------------------------------------------------
# Real-DB / real-input smokes
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not (
        DUCKDB_PATH.exists()
        and REGISTRY_CSV_PATH.exists()
        and PR234_BINDING_CSV_PATH.exists()
    ),
    reason="Real DuckDB / registry / PR #234 binding not present",
)
class TestRealRegistryAndPr234BindingSmoke:
    """End-to-end smoke: run the entrypoint against the real inputs."""

    def test_real_run_passes(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "out.csv"
        md_path = tmp_path / "out.md"
        result = adjudicate_history_enriched_pre_game_source_layer(
            duckdb_path=DUCKDB_PATH,
            registry_csv_path=REGISTRY_CSV_PATH,
            pr234_binding_csv_path=PR234_BINDING_CSV_PATH,
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #242",
            audit_date="2026-05-24",
        )
        assert result.passed is True, (
            f"halting_falsifier={result.halting_falsifier!r} "
            f"fired={result.falsifiers_fired!r}"
        )
        assert len(result.decisions) == 8
        assert result.halting_falsifier is None
        assert set(d.decision_id for d in result.decisions) == set(Q_DECISION_IDS)

    def test_real_run_all_provenance_shas_valid(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "out.csv"
        md_path = tmp_path / "out.md"
        result = adjudicate_history_enriched_pre_game_source_layer(
            duckdb_path=DUCKDB_PATH,
            registry_csv_path=REGISTRY_CSV_PATH,
            pr234_binding_csv_path=PR234_BINDING_CSV_PATH,
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #242",
            audit_date="2026-05-24",
        )
        hex_re = re.compile(r"^[0-9a-f]{64}$")
        for d in result.decisions:
            for field_name in PROVENANCE_SHA_FIELDS:
                sha = getattr(d, field_name)
                assert hex_re.fullmatch(sha), (
                    f"{field_name} on {d.decision_id} = {sha!r} not 64-char lowercase hex"
                )

    def test_real_run_no_materialized_output_paths(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "out.csv"
        md_path = tmp_path / "out.md"
        result = adjudicate_history_enriched_pre_game_source_layer(
            duckdb_path=DUCKDB_PATH,
            registry_csv_path=REGISTRY_CSV_PATH,
            pr234_binding_csv_path=PR234_BINDING_CSV_PATH,
            csv_path=csv_path,
            md_path=md_path,
            audit_pr="PR #242",
            audit_date="2026-05-24",
        )
        for d in result.decisions:
            assert d.materialized_output_paths == ""


class TestHelperMissingDecisionBranches:
    """Each Q-specific helper must halt when its target row is absent."""

    @pytest.mark.parametrize(
        ("helper", "exclude_id"),
        [
            (
                _check_q1_source_layer_evidence_consistent,
                "Q1_source_layer",
            ),
            (_check_q1_single_row_per_n5, "Q1_source_layer"),
            (
                _check_q4_cold_start_gates_complete,
                "Q4_cold_start_policy",
            ),
            (_check_q4_no_leakage_in_cold_start, "Q4_cold_start_policy"),
            (
                _check_q5_cross_region_three_options_enumerated,
                "Q5_cross_region_policy",
            ),
            (_check_q6_rating_default_deferred, "Q6_rating_policy"),
            (_check_q6_rating_forward_only, "Q6_rating_policy"),
            (
                _check_q7_in_game_historical_columns_in_scope,
                "Q7_in_game_historical_policy",
            ),
            (
                _check_q7_no_target_match_tracker,
                "Q7_in_game_historical_policy",
            ),
            (
                _check_in_game_historical_strict_lt,
                "Q7_in_game_historical_policy",
            ),
            (
                _check_q8_mhm_documented,
                "Q8_matches_history_minimal_consumption",
            ),
        ],
    )
    def test_missing_target_decision_halts(
        self,
        passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
        helper: Any,
        exclude_id: str,
    ) -> None:
        decisions = tuple(d for d in passing_decisions if d.decision_id != exclude_id)
        # Helpers that take an extra arg need a no-op default.
        sig_param_count = helper.__code__.co_argcount
        if sig_param_count == 1:
            did_fire, _msg = helper(decisions)
        else:
            did_fire, _msg = helper(decisions, {})
        assert did_fire

    def test_q2_check_with_missing_q2(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = tuple(
            d for d in passing_decisions if d.decision_id != "Q2_target_anchor"
        )
        did_fire, msg = _check_q2_target_anchor_type_match(decisions, {})
        assert did_fire
        assert "Q2" in msg

    def test_q3_dtype_check_with_missing_q3(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = tuple(
            d for d in passing_decisions if d.decision_id != "Q3_history_time_column"
        )
        did_fire, msg = _check_q3_history_time_column_dtype(decisions, {})
        assert did_fire
        assert "Q3" in msg


class TestQ1SubfieldEmptyChecks:
    """Each of Q1's 5 required subfields must be non-empty (parametrized empty trigger)."""

    @pytest.mark.parametrize(
        "field_name",
        [
            "selected_target_source_layer",
            "selected_history_source_layer",
            "target_history_asymmetry",
            "source_layer_divergence_reason",
            "history_source_extension_reason",
        ],
    )
    def test_empty_subfield_fires(
        self,
        passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
        field_name: str,
    ) -> None:
        decisions = _replace_row(
            passing_decisions, "Q1_source_layer", **{field_name: ""}
        )
        did_fire, msg = _check_q1_single_row_per_n5(decisions)
        assert did_fire
        assert field_name in msg

    def test_wrong_q1_decision_id_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        # decision_id starts with "Q1" but is not exactly "Q1_source_layer"
        decisions = _replace_row(
            passing_decisions, "Q1_source_layer", decision_id="Q1a_source_layer"
        )
        did_fire, msg = _check_q1_single_row_per_n5(decisions)
        assert did_fire
        assert "Q1a_source_layer" in msg


class TestQ1EmptyHistoryLayer:
    """The Q1 evidence helper also halts if selected_history_source_layer is empty."""

    def test_empty_history_layer_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions, "Q1_source_layer", selected_history_source_layer=""
        )
        did_fire, msg = _check_q1_source_layer_evidence_consistent(decisions, {})
        assert did_fire
        assert "history" in msg.lower()


class TestStrictLtFilterMissingDecisions:
    """Strict-< divergence check operates only on present Q3/Q7 rows."""

    def test_smoke_sql_canonical_with_only_q3_q7_dropped(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        # Drop both Q3 and Q7 — the check skips them and should pass on the
        # remaining 6 rows.
        decisions = tuple(
            d
            for d in passing_decisions
            if d.decision_id not in {"Q3_history_time_column", "Q7_in_game_historical_policy"}
        )
        did_fire, msg = _check_strict_lt_filter_divergence(
            decisions, _smoke_sql_with_canonical()
        )
        assert not did_fire, msg

    def test_q3_notes_missing_canonical_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        # Mutate Q3 history_time_column and notes so the canonical does not appear
        decisions = _replace_row(
            passing_decisions,
            "Q3_history_time_column",
            history_time_column="something else",
            notes="no canonical here",
        )
        did_fire, msg = _check_strict_lt_filter_divergence(
            decisions, _smoke_sql_with_canonical()
        )
        assert did_fire
        assert "Q3" in msg

    def test_q7_notes_missing_canonical_fires(
        self, passing_decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    ) -> None:
        decisions = _replace_row(
            passing_decisions, "Q7_in_game_historical_policy", notes="no canonical"
        )
        did_fire, msg = _check_strict_lt_filter_divergence(
            decisions, _smoke_sql_with_canonical()
        )
        assert did_fire
        assert "Q7" in msg


class TestProvenanceHelpers:
    """SHA + git + repo-root helpers."""

    def test_sha256_file_missing_returns_not_found(self, tmp_path: Path) -> None:
        missing = tmp_path / "no_such_file.txt"
        assert _sha256_file(missing) == "NOT_FOUND"

    def test_sha256_file_present_returns_64_hex(self, tmp_path: Path) -> None:
        p = tmp_path / "f.txt"
        p.write_text("hello", encoding="utf-8")
        sha = _sha256_file(p)
        assert re.fullmatch(r"[0-9a-f]{64}", sha)

    def test_find_repo_root_raises_when_no_pyproject(
        self, tmp_path: Path
    ) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import (  # noqa: E501
            _find_repo_root,
        )

        # tmp_path is under /private/var on macOS and won't have a pyproject
        # walking up to /.
        with pytest.raises(FileNotFoundError):
            _find_repo_root(tmp_path)

    def test_get_git_sha_returns_string(self) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import (  # noqa: E501
            _get_git_sha,
        )

        sha = _get_git_sha()
        assert isinstance(sha, str)
        # 40-char hex or "UNKNOWN"
        assert sha == "UNKNOWN" or re.fullmatch(r"[0-9a-f]{40}", sha)


class TestLoaderMissingPaths:
    """The CSV loaders return empty containers when the path does not exist."""

    def test_load_pr234_binding_missing_returns_empty(self, tmp_path: Path) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import (  # noqa: E501
            _load_pr234_binding_csv,
        )

        out = _load_pr234_binding_csv(tmp_path / "missing.csv")
        assert out == {}

    def test_load_registry_missing_returns_empty(self, tmp_path: Path) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import (  # noqa: E501
            _load_registry_csv,
        )

        out = _load_registry_csv(tmp_path / "missing.csv")
        assert out == []


@pytest.mark.skipif(
    not PR241_VALIDATOR_PATH.exists(),
    reason="PR #241 validator module not present at expected path",
)
class TestPr241ValidatorSha256MatchesEmpirically:
    """The on-disk PR #241 validator module hashes to EXPECTED_PR241_VALIDATOR_SHA256."""

    def test_empirical_sha_matches_expected(self) -> None:
        empirical = _sha256_file(PR241_VALIDATOR_PATH)
        assert empirical == EXPECTED_PR241_VALIDATOR_SHA256, (
            f"On-disk PR #241 validator SHA-256 {empirical!r} != expected "
            f"{EXPECTED_PR241_VALIDATOR_SHA256!r}. The expected SHA constant "
            "in the adjudicator module must be updated (or the validator "
            "module was modified without updating the binding)."
        )
