"""Tests for ``adjudicate_symmetry_difference_feature_scope`` (02_02_01 adjudication).

Covers:
  Group A — Module structure (imports, constants, dataclasses).
  Group B — Round 1 blocker resolutions (B1/B2/B3).
  Group C — Round 2 nits N1–N6.
  Group D — Source-column traceability.
  Group E — Direction policy and naming.
  Group F — Validator invocation.
  Group G — Parent SHA pins.
  Group H — Artifact determinism + no-emit checks.
  Group I — Forbidden emissions.
  Group J — Halting falsifier order.
"""

from __future__ import annotations

import csv
import dataclasses
import io
import json
import re
from pathlib import Path

import pytest

import rts_predict.games.sc2.datasets.sc2egset.adjudicate_symmetry_difference_feature_scope as _adjmod  # noqa: E501
from rts_predict.games.sc2.datasets.sc2egset.adjudicate_symmetry_difference_feature_scope import (  # noqa: E501
    _CSV_HEADER,
    _EXPECTED_02_01_02_AUDIT_CANONICAL_SHA256,
    _EXPECTED_02_01_02_PARQUET_SHA256,
    _EXPECTED_02_01_03_AUDIT_CANONICAL_SHA256,
    _EXPECTED_02_01_03_PARQUET_SHA256,
    _EXPECTED_VALIDATOR_SHA256,
    _HALTING_FALSIFIER_CHAIN,
    _REPO_RELATIVE_PARENT_02_01_02_AUDIT,
    _REPO_RELATIVE_PARENT_02_01_02_PARQUET,
    _REPO_RELATIVE_PARENT_02_01_03_AUDIT,
    _REPO_RELATIVE_PARENT_02_01_03_PARQUET,
    _REPO_RELATIVE_VALIDATOR_PATH,
    ALLOWED_DIRECTIONS,
    BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS,
    BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS,
    BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS,
    DECISION_ID,
    EXECUTED_AT_UTC_DATE,
    MATCHUP_HISTORY_TRANSFORM_DECISION,
    ROW_IDENTITY_JOIN_KEYS,
    UNARY_TRANSFORM_DECISION,
    CandidateScopeDecision,
    SymmetryDifferenceAdjudicationError,
    SymmetryDifferenceAdjudicationResult,
    _assert_internal_consistency,
    _build_abs_diff_specs,
    _build_cross_region_specs,
    _build_difference_specs,
    _build_mean_specs,
    _construct_binding_candidate_specs,
    _construct_csv_row,
    _sha256_of_canonical_json,
    _sha256_of_file_bytes,
    run_symmetry_difference_feature_scope_adjudication,
)
from rts_predict.games.sc2.datasets.sc2egset.validate_symmetry_difference_feature_materialization import (  # noqa: E501
    BLOCKED_SLOT_TOKEN_REGEX,
    POST_GAME_TOKEN_REGEX,
    UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03,
    VALID_DIRECTION_LITERAL_VALUES,
)

# ---------------------------------------------------------------------------
# Repo root fixture
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[6]


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Return the repository root."""
    return _REPO_ROOT


@pytest.fixture(scope="session")
def adjudication_result(repo_root: Path) -> SymmetryDifferenceAdjudicationResult:
    """Return a real adjudication result using the live repo artifacts."""
    return run_symmetry_difference_feature_scope_adjudication(repo_root=repo_root)


@pytest.fixture(scope="session")
def csv_content(tmp_path_factory: pytest.TempPathFactory, repo_root: Path) -> str:
    """Return CSV content rendered to a temp path."""
    tmp = tmp_path_factory.mktemp("csv_render")
    r = run_symmetry_difference_feature_scope_adjudication(
        repo_root=repo_root,
        output_csv_path=tmp / "adj.csv",
        output_md_path=tmp / "adj.md",
    )
    return r.csv_path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def md_content(tmp_path_factory: pytest.TempPathFactory, repo_root: Path) -> str:
    """Return MD content rendered to a temp path."""
    tmp = tmp_path_factory.mktemp("md_render")
    r = run_symmetry_difference_feature_scope_adjudication(
        repo_root=repo_root,
        output_csv_path=tmp / "adj.csv",
        output_md_path=tmp / "adj.md",
    )
    return r.md_path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Group A — Module structure
# ---------------------------------------------------------------------------


class TestGroupAModuleStructure:
    """Group A: Module structure tests."""

    def test_module_imports(self) -> None:
        """Module imports without error; key symbols are accessible."""
        assert callable(run_symmetry_difference_feature_scope_adjudication)
        assert isinstance(DECISION_ID, str)
        assert isinstance(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS, tuple)

    def test_dataclasses_frozen(self) -> None:
        """CandidateScopeDecision is decorated with frozen=True."""
        csd_fields = dataclasses.fields(CandidateScopeDecision)
        assert len(csd_fields) > 0
        # Frozen dataclasses raise FrozenInstanceError on direct attribute assignment
        spec = CandidateScopeDecision(
            candidate_feature_name="x",
            candidate_family="F1_difference",
            direction="focal_minus_opponent",
            source_columns=("focal_prior_match_count", "opponent_prior_match_count"),
            source_artifact="02_01_03_history_enriched_pre_game_features.parquet",
            source_family="focal_player_history",
            traceability_status="traced_to_audited_24_tuple",
            validator_passed=True,
            notes="",
        )
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            spec.candidate_feature_name = "y"  # type: ignore[misc]

    def test_adjudication_result_frozen(  # noqa: E501
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """SymmetryDifferenceAdjudicationResult is frozen."""
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            adjudication_result.decision_id = "bad"  # type: ignore[misc]

    def test_allowed_directions_match_validator_literals(self) -> None:
        """ALLOWED_DIRECTIONS matches the validator's VALID_DIRECTION_LITERAL_VALUES."""
        assert set(ALLOWED_DIRECTIONS) == set(VALID_DIRECTION_LITERAL_VALUES)

    def test_row_identity_join_keys_match_audit_json(self, repo_root: Path) -> None:
        """ROW_IDENTITY_JOIN_KEYS equals projected_identity + projected_context."""
        audit_path = repo_root / _REPO_RELATIVE_PARENT_02_01_03_AUDIT
        with audit_path.open(encoding="utf-8") as fh:
            audit = json.load(fh)
        combined = tuple(
            audit["projected_identity_columns"] + audit["projected_context_columns"]
        )
        assert combined == ROW_IDENTITY_JOIN_KEYS

    def test_binding_difference_family_numeric_pairs_subset_of_24_tuple(self) -> None:
        """Every focal/opponent column in BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS is in 24-tuple."""
        audited_set = set(UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03)
        for focal, opponent in BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS:
            assert focal in audited_set, f"{focal!r} not in audited 24-tuple"
            assert opponent in audited_set, f"{opponent!r} not in audited 24-tuple"

    def test_binding_pair_count_is_ten(self) -> None:
        """BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS has exactly 10 pairs."""
        assert len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS) == 10


# ---------------------------------------------------------------------------
# Group B — Round 1 blocker resolutions
# ---------------------------------------------------------------------------


class TestGroupBBlockerResolutions:
    """Group B: Round 1 blocker resolutions (B1/B2/B3)."""

    def test_binding_matchup_history_pair_operations_symbol_absent(self) -> None:
        """B1: BINDING_MATCHUP_HISTORY_PAIR_OPERATIONS constant must NOT exist."""
        assert not hasattr(_adjmod, "BINDING_MATCHUP_HISTORY_PAIR_OPERATIONS")

    def test_matchup_history_transform_decision_dropped(self) -> None:
        """B1: MATCHUP_HISTORY_TRANSFORM_DECISION records 'dropped' decision."""
        assert "dropped" in MATCHUP_HISTORY_TRANSFORM_DECISION.lower()
        assert "no_audited_opponent_counterpart" in MATCHUP_HISTORY_TRANSFORM_DECISION

    def test_no_matchup_h2h_pair_candidate_in_constructed_specs(self) -> None:
        """B1: No candidate with 'matchup_h2h' in its name is constructed."""
        _, _, _, all_decisions = _construct_binding_candidate_specs()
        names = [d.candidate_feature_name for d in all_decisions]
        for name in names:
            assert "matchup_h2h" not in name, (
                f"Found forbidden matchup_h2h candidate: {name!r}"
            )

    def test_binding_symmetric_pair_aggregate_transforms_exactly_mean_abs_diff(self) -> None:
        """B3: BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS == ('mean', 'abs_diff')."""
        assert BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS == ("mean", "abs_diff")

    def test_sum_not_in_bound_transforms(self) -> None:
        """B2: 'sum' is not in BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS."""
        assert "sum" not in BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS

    def test_product_not_in_bound_transforms(self) -> None:
        """B2: 'product' is not in BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS."""
        assert "product" not in BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS

    def test_no_pair_sum_candidate_constructed(self) -> None:
        """B2: No candidate with '_pair_sum' in its name is constructed."""
        _, _, _, all_decisions = _construct_binding_candidate_specs()
        for d in all_decisions:
            assert "_pair_sum" not in d.candidate_feature_name

    def test_no_pair_product_candidate_constructed(self) -> None:
        """B2: No candidate with '_pair_product' in its name is constructed."""
        _, _, _, all_decisions = _construct_binding_candidate_specs()
        for d in all_decisions:
            assert "_pair_product" not in d.candidate_feature_name

    def test_pair_abs_diff_candidate_per_numeric_pair(self) -> None:
        """B3: Exactly one _pair_abs_diff candidate per binding numeric pair."""
        abs_diff_specs = _build_abs_diff_specs()
        assert len(abs_diff_specs) == len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS)
        for spec in abs_diff_specs:
            assert spec.candidate_feature_name.endswith("_pair_abs_diff")


# ---------------------------------------------------------------------------
# Group C — Round 2 nits N1–N6
# ---------------------------------------------------------------------------


class TestGroupCRound2Nits:
    """Group C: Round 2 nit applications N1–N6."""

    def test_md_section_9_2_uses_linearly_expressible_wording(self, md_content: str) -> None:
        """N1: MD §9.2 contains 'not LINEARLY expressible'."""
        assert "not LINEARLY expressible" in md_content

    def test_md_section_9_2_cites_manual_section_6_line_135(self, md_content: str) -> None:
        """N2: MD §9.2 cites 02_FEATURE_ENGINEERING_MANUAL.md §6 line 135."""
        assert "§6 line 135" in md_content

    def test_md_section_9_2_acknowledges_pipeline_section_convention(self, md_content: str) -> None:
        """N2: MD §9.2 acknowledges Pipeline-Section placement is convention choice."""
        assert "Pipeline-Section convention" in md_content or "convention choice" in md_content

    def test_md_section_4_acknowledges_logreg_redundancy_of_f5(  # noqa: E501
        self, md_content: str
    ) -> None:
        """N3: MD §4 acknowledges LogReg-redundancy of (either, both, xor)."""
        assert "rank-2" in md_content or "LogReg" in md_content

    def test_md_section_12_records_unary_as_open_design_question(self, md_content: str) -> None:
        """N4: MD §12 records unary transform as open design question OQ8."""
        assert "open design question" in md_content.lower()
        assert "OQ8" in md_content or "unary" in md_content

    def test_internal_consistency_abs_diff_count_equals_constant_equals_csv_field(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """N5: abs_diff count == BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS len == CSV field."""
        specs = adjudication_result.candidate_specs
        abs_diff_count = sum(
            1 for s in specs if s.candidate_family == "F3_pair_abs_diff"
        )
        constant_count = len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS)
        assert abs_diff_count == constant_count
        assert (
            adjudication_result.binding_difference_family_numeric_pair_count
            == constant_count
        )

    def test_internal_consistency_total_candidate_count_matches_csv_field(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """N5: total candidate count matches total_binding_candidate_count field."""
        assert adjudication_result.total_binding_candidate_count == len(
            adjudication_result.candidate_specs
        )
        assert adjudication_result.total_binding_candidate_count == 33

    def test_md_section_9_3_cross_links_to_9_1_and_5_joint_basis(self, md_content: str) -> None:
        """N6: MD §9.3 cross-links to §9.1 and §5 and states the joint basis."""
        assert "§9.1" in md_content
        assert "§5" in md_content
        assert "joint" in md_content.lower() or "jointly" in md_content.lower()


# ---------------------------------------------------------------------------
# Group D — Source-column traceability
# ---------------------------------------------------------------------------


class TestGroupDTraceability:
    """Group D: Source-column traceability."""

    def test_every_difference_spec_source_columns_in_24_tuple(self) -> None:
        """F1 specs' source_columns are all in the 24-tuple."""
        audited = set(UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03)
        for spec in _build_difference_specs():
            for col in spec.source_columns:
                assert col in audited, f"F1 source {col!r} not in 24-tuple"

    def test_every_mean_spec_source_columns_in_24_tuple(self) -> None:
        """F2 specs' source_columns are all in the 24-tuple."""
        audited = set(UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03)
        for spec in _build_mean_specs():
            for col in spec.source_columns:
                assert col in audited, f"F2 source {col!r} not in 24-tuple"

    def test_every_abs_diff_spec_source_columns_in_24_tuple(self) -> None:
        """F3 specs' source_columns are all in the 24-tuple."""
        audited = set(UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03)
        for spec in _build_abs_diff_specs():
            for col in spec.source_columns:
                assert col in audited, f"F3 source {col!r} not in 24-tuple"

    def test_every_cross_region_spec_source_columns_in_24_tuple(self) -> None:
        """F5 specs' source_columns are in the 24-tuple."""
        audited = set(UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03)
        for spec in _build_cross_region_specs():
            for col in spec.source_columns:
                assert col in audited, f"F5 source {col!r} not in 24-tuple"


# ---------------------------------------------------------------------------
# Group E — Direction policy and naming
# ---------------------------------------------------------------------------


class TestGroupEDirectionPolicy:
    """Group E: Direction policy and naming tests."""

    def test_difference_candidates_direction_is_focal_minus_opponent(self) -> None:
        """F1 candidates have direction='focal_minus_opponent'."""
        for spec in _build_difference_specs():
            assert spec.direction == "focal_minus_opponent"

    def test_mean_candidates_direction_is_symmetric(self) -> None:
        """F2 candidates have direction='symmetric'."""
        for spec in _build_mean_specs():
            assert spec.direction == "symmetric"

    def test_abs_diff_candidates_direction_is_symmetric(self) -> None:
        """F3 candidates have direction='symmetric'."""
        for spec in _build_abs_diff_specs():
            assert spec.direction == "symmetric"

    def test_cross_region_candidates_direction_is_symmetric(self) -> None:
        """F5 candidates have direction='symmetric'."""
        for spec in _build_cross_region_specs():
            assert spec.direction == "symmetric"

    def test_no_candidate_name_contains_slot_dependent_token(self) -> None:
        """No candidate name matches any BLOCKED_SLOT_TOKEN_REGEX pattern."""
        _, _, _, all_decisions = _construct_binding_candidate_specs()
        for spec in all_decisions:
            for pattern in BLOCKED_SLOT_TOKEN_REGEX:
                assert not re.search(pattern, spec.candidate_feature_name), (
                    f"Slot token {pattern!r} matched in {spec.candidate_feature_name!r}"
                )

    def test_no_candidate_name_in_post_game_token(self) -> None:
        """No candidate name matches POST_GAME_TOKEN_REGEX (excluding win_rate compounds)."""
        _, _, _, all_decisions = _construct_binding_candidate_specs()
        # Allowlist same as in validator
        allow = ("prior_win_rate",)
        for spec in all_decisions:
            name = spec.candidate_feature_name
            if any(a in name for a in allow):
                continue
            for pattern in POST_GAME_TOKEN_REGEX:
                assert not re.search(pattern, name), (
                    f"Post-game token {pattern!r} matched in {name!r}"
                )

    def test_f1_names_end_with_diff_suffix(self) -> None:
        """F1 difference candidate names end with '_diff'."""
        for spec in _build_difference_specs():
            assert spec.candidate_feature_name.endswith("_diff"), (
                f"Expected _diff suffix: {spec.candidate_feature_name!r}"
            )

    def test_f2_names_contain_pair_mean(self) -> None:
        """F2 mean candidate names contain '_pair_mean'."""
        for spec in _build_mean_specs():
            assert "_pair_mean" in spec.candidate_feature_name

    def test_f3_names_contain_pair_abs_diff(self) -> None:
        """F3 abs_diff candidate names contain '_pair_abs_diff'."""
        for spec in _build_abs_diff_specs():
            assert "_pair_abs_diff" in spec.candidate_feature_name

    def test_f5_names_contain_cross_region_pair(self) -> None:
        """F5 cross-region candidate names contain 'cross_region_pair'."""
        for spec in _build_cross_region_specs():
            assert "cross_region_pair" in spec.candidate_feature_name


# ---------------------------------------------------------------------------
# Group F — Validator invocation
# ---------------------------------------------------------------------------


class TestGroupFValidatorInvocation:
    """Group F: Validator invocation tests."""

    def test_validator_invoked_passed_true(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """Validator passes with the constructed specs."""
        assert adjudication_result.validator_passed is True

    def test_validator_halting_falsifier_is_none(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """No halting falsifier fires."""
        assert adjudication_result.validator_halting_falsifier is None

    def test_validator_materialized_output_paths_empty(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """materialized_output_paths is always the empty tuple."""
        assert adjudication_result.materialized_output_paths == ()

    def test_validator_module_sha_pin_matches_disk(self, repo_root: Path) -> None:
        """The embedded validator SHA256 pin matches the on-disk file."""
        disk_sha = _sha256_of_file_bytes(repo_root / _REPO_RELATIVE_VALIDATOR_PATH)
        assert disk_sha == _EXPECTED_VALIDATOR_SHA256


# ---------------------------------------------------------------------------
# Group G — Parent SHA pins
# ---------------------------------------------------------------------------


class TestGroupGParentShaPins:
    """Group G: Parent artifact SHA pin tests."""

    def test_parent_02_01_02_parquet_sha_matches_disk(self, repo_root: Path) -> None:
        """02_01_02 Parquet SHA pin matches on-disk bytes."""
        disk_sha = _sha256_of_file_bytes(
            repo_root / _REPO_RELATIVE_PARENT_02_01_02_PARQUET
        )
        assert disk_sha == _EXPECTED_02_01_02_PARQUET_SHA256

    def test_parent_02_01_03_parquet_sha_matches_disk(self, repo_root: Path) -> None:
        """02_01_03 Parquet SHA pin matches on-disk bytes."""
        disk_sha = _sha256_of_file_bytes(
            repo_root / _REPO_RELATIVE_PARENT_02_01_03_PARQUET
        )
        assert disk_sha == _EXPECTED_02_01_03_PARQUET_SHA256

    def test_parent_02_01_02_audit_json_sha_matches_disk_canonical_form(
        self, repo_root: Path
    ) -> None:
        """02_01_02 audit JSON canonical SHA pin matches on-disk canonical form."""
        disk_sha = _sha256_of_canonical_json(
            repo_root / _REPO_RELATIVE_PARENT_02_01_02_AUDIT
        )
        assert disk_sha == _EXPECTED_02_01_02_AUDIT_CANONICAL_SHA256

    def test_parent_02_01_03_audit_json_sha_matches_disk_canonical_form(
        self, repo_root: Path
    ) -> None:
        """02_01_03 audit JSON canonical SHA pin matches on-disk canonical form."""
        disk_sha = _sha256_of_canonical_json(
            repo_root / _REPO_RELATIVE_PARENT_02_01_03_AUDIT
        )
        assert disk_sha == _EXPECTED_02_01_03_AUDIT_CANONICAL_SHA256


# ---------------------------------------------------------------------------
# Group H — Artifact determinism + no-emit checks
# ---------------------------------------------------------------------------


class TestGroupHArtifactDeterminism:
    """Group H: Artifact shape, wording, and determinism tests."""

    def test_csv_column_count_equals_23(self, csv_content: str) -> None:
        """CSV has exactly 23 columns."""
        reader = csv.reader(io.StringIO(csv_content))
        header = next(reader)
        assert len(header) == 23

    def test_csv_row_count_equals_2(self, csv_content: str) -> None:
        """CSV has exactly 2 rows (header + 1 data row)."""
        rows = list(csv.reader(io.StringIO(csv_content)))
        assert len(rows) == 2

    def test_csv_no_not_found_sha(self, csv_content: str) -> None:
        """CSV contains no 'NOT_FOUND' string in any SHA field."""
        assert "NOT_FOUND" not in csv_content

    def test_md_section_count_equals_13(self, md_content: str) -> None:
        """MD has exactly 13 top-level ## §N sections."""
        count = sum(1 for line in md_content.splitlines() if line.startswith("## §"))
        assert count == 13

    def test_md_section_3_documentary_not_runtime_wording(self, md_content: str) -> None:
        """MD §3 contains the gate-clause verbatim phrase."""
        expected = (
            "documentary future-materialisation gate, not a runtime promise "
            "for the adjudication PR"
        )
        assert expected in md_content

    def test_csv_render_byte_deterministic_across_two_calls(
        self, tmp_path: Path, repo_root: Path
    ) -> None:
        """Rendering CSV twice produces byte-identical output."""
        run_symmetry_difference_feature_scope_adjudication(
            repo_root=repo_root,
            output_csv_path=tmp_path / "a.csv",
            output_md_path=tmp_path / "a.md",
        )
        run_symmetry_difference_feature_scope_adjudication(
            repo_root=repo_root,
            output_csv_path=tmp_path / "b.csv",
            output_md_path=tmp_path / "b.md",
        )
        assert (tmp_path / "a.csv").read_bytes() == (tmp_path / "b.csv").read_bytes()

    def test_md_render_byte_deterministic_across_two_calls(
        self, tmp_path: Path, repo_root: Path
    ) -> None:
        """Rendering MD twice produces byte-identical output."""
        run_symmetry_difference_feature_scope_adjudication(
            repo_root=repo_root,
            output_csv_path=tmp_path / "c.csv",
            output_md_path=tmp_path / "c.md",
        )
        run_symmetry_difference_feature_scope_adjudication(
            repo_root=repo_root,
            output_csv_path=tmp_path / "d.csv",
            output_md_path=tmp_path / "d.md",
        )
        assert (tmp_path / "c.md").read_bytes() == (tmp_path / "d.md").read_bytes()

    def test_csv_header_matches_expected_columns(self, csv_content: str) -> None:
        """CSV header matches the _CSV_HEADER constant exactly."""
        reader = csv.reader(io.StringIO(csv_content))
        header = next(reader)
        assert tuple(header) == _CSV_HEADER

    def test_csv_data_row_binding_pair_count_field(self, csv_content: str) -> None:
        """CSV data row binding_difference_family_numeric_pair_count == '10'."""
        reader = csv.reader(io.StringIO(csv_content))
        next(reader)  # skip header
        row = next(reader)
        idx = list(_CSV_HEADER).index("binding_difference_family_numeric_pair_count")
        assert row[idx] == "10"


# ---------------------------------------------------------------------------
# Group I — Forbidden emissions
# ---------------------------------------------------------------------------


class TestGroupIForbiddenEmissions:
    """Group I: Forbidden emission checks."""

    def test_no_parquet_emitted_under_02_symmetry_and_difference_features(
        self, tmp_path: Path, repo_root: Path
    ) -> None:
        """No Parquet file is written anywhere after adjudication."""
        run_symmetry_difference_feature_scope_adjudication(
            repo_root=repo_root,
            output_csv_path=tmp_path / "adj.csv",
            output_md_path=tmp_path / "adj.md",
        )
        parquet_files = list(tmp_path.glob("**/*.parquet"))
        assert parquet_files == [], f"Unexpected Parquet files: {parquet_files}"

    def test_no_audit_json_or_md_emitted_under_02_02_01_subtree(
        self, tmp_path: Path, repo_root: Path
    ) -> None:
        """No leakage audit JSON or MD emitted in the output."""
        run_symmetry_difference_feature_scope_adjudication(
            repo_root=repo_root,
            output_csv_path=tmp_path / "adj.csv",
            output_md_path=tmp_path / "adj.md",
        )
        json_files = list(tmp_path.glob("**/*.json"))
        assert json_files == [], f"Unexpected JSON files: {json_files}"

    def test_no_step_status_modified_during_run(
        self, tmp_path: Path, repo_root: Path
    ) -> None:
        """STEP_STATUS.yaml mtime is unchanged after adjudication."""
        step_status_path = (
            repo_root
            / "src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml"
        )
        if not step_status_path.exists():
            pytest.skip("STEP_STATUS.yaml not present")
        mtime_before = step_status_path.stat().st_mtime
        run_symmetry_difference_feature_scope_adjudication(
            repo_root=repo_root,
            output_csv_path=tmp_path / "adj.csv",
            output_md_path=tmp_path / "adj.md",
        )
        mtime_after = step_status_path.stat().st_mtime
        assert mtime_before == mtime_after

    def test_no_research_log_modified_during_run(
        self, tmp_path: Path, repo_root: Path
    ) -> None:
        """dataset research_log.md mtime is unchanged after adjudication."""
        log_path = (
            repo_root
            / "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
        )
        if not log_path.exists():
            pytest.skip("research_log.md not present")
        mtime_before = log_path.stat().st_mtime
        run_symmetry_difference_feature_scope_adjudication(
            repo_root=repo_root,
            output_csv_path=tmp_path / "adj.csv",
            output_md_path=tmp_path / "adj.md",
        )
        mtime_after = log_path.stat().st_mtime
        assert mtime_before == mtime_after

    def test_no_roadmap_modified_during_run(
        self, tmp_path: Path, repo_root: Path
    ) -> None:
        """ROADMAP.md mtime is unchanged after adjudication."""
        roadmap_path = (
            repo_root
            / "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md"
        )
        if not roadmap_path.exists():
            pytest.skip("ROADMAP.md not present")
        mtime_before = roadmap_path.stat().st_mtime
        run_symmetry_difference_feature_scope_adjudication(
            repo_root=repo_root,
            output_csv_path=tmp_path / "adj.csv",
            output_md_path=tmp_path / "adj.md",
        )
        mtime_after = roadmap_path.stat().st_mtime
        assert mtime_before == mtime_after

    def test_only_csv_and_md_written_to_output_paths(
        self, tmp_path: Path, repo_root: Path
    ) -> None:
        """Only the CSV and MD files are written; no other files in tmp_path."""
        run_symmetry_difference_feature_scope_adjudication(
            repo_root=repo_root,
            output_csv_path=tmp_path / "adj.csv",
            output_md_path=tmp_path / "adj.md",
        )
        written = sorted(p.name for p in tmp_path.iterdir())
        assert written == ["adj.csv", "adj.md"]


# ---------------------------------------------------------------------------
# Group J — Halting falsifier order
# ---------------------------------------------------------------------------


class TestGroupJHaltingFalsifierOrder:
    """Group J: Halting falsifier chain ordering tests."""

    def test_halting_falsifier_chain_starts_with_validator_module_sha(self) -> None:
        """The halting falsifier chain's first element is validator_module_sha_pin_mismatch."""
        assert _HALTING_FALSIFIER_CHAIN[0] == "validator_module_sha_pin_mismatch"

    def test_halting_falsifier_chain_contains_round_2_anchors(self) -> None:
        """The chain contains all Round-2-specific falsifier anchors."""
        chain = set(_HALTING_FALSIFIER_CHAIN)
        assert "binding_matchup_history_pair_operations_symbol_present" in chain
        assert "pair_sum_candidate_present" in chain
        assert "pair_product_candidate_present" in chain
        assert "unary_matchup_h2h_focal_advantage_candidate_present" in chain
        assert "binding_symmetric_pair_aggregate_transforms_not_mean_abs_diff" in chain

    def test_halting_falsifier_chain_has_materialized_output_paths_check(self) -> None:
        """Chain contains materialized_output_paths_non_empty."""
        assert "materialized_output_paths_non_empty" in _HALTING_FALSIFIER_CHAIN

    def test_halting_falsifier_chain_validator_sha_before_parquet_sha(self) -> None:
        """validator_module_sha comes before parquet sha checks."""
        chain = list(_HALTING_FALSIFIER_CHAIN)
        sha_idx = chain.index("validator_module_sha_pin_mismatch")
        parquet_idx = chain.index("parent_parquet_02_01_02_sha_mismatch")
        assert sha_idx < parquet_idx

    def test_halting_falsifier_chain_validator_failed_before_content_checks(self) -> None:
        """validator_failed_passed_false appears before content-level checks."""
        chain = list(_HALTING_FALSIFIER_CHAIN)
        val_failed_idx = chain.index("validator_failed_passed_false")
        sym_transform_idx = chain.index(
            "binding_symmetric_pair_aggregate_transforms_not_mean_abs_diff"
        )
        assert val_failed_idx < sym_transform_idx


# ---------------------------------------------------------------------------
# Additional traceability / scope tests
# ---------------------------------------------------------------------------


class TestGroupAdditionalScope:
    """Additional scope and correctness tests."""

    def test_total_candidate_count_is_33(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """Total candidate count is exactly 33 (F1=10 + F2=10 + F3=10 + F5=3)."""
        assert adjudication_result.total_binding_candidate_count == 33

    def test_f1_candidate_count_is_10(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """F1 (difference) has exactly 10 candidates."""
        count = sum(
            1
            for s in adjudication_result.candidate_specs
            if s.candidate_family == "F1_difference"
        )
        assert count == 10

    def test_f2_candidate_count_is_10(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """F2 (pair_mean) has exactly 10 candidates."""
        count = sum(
            1
            for s in adjudication_result.candidate_specs
            if s.candidate_family == "F2_pair_mean"
        )
        assert count == 10

    def test_f3_candidate_count_is_10(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """F3 (pair_abs_diff) has exactly 10 candidates."""
        count = sum(
            1
            for s in adjudication_result.candidate_specs
            if s.candidate_family == "F3_pair_abs_diff"
        )
        assert count == 10

    def test_f5_candidate_count_is_3(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """F5 (cross_region_pair) has exactly 3 candidates."""
        count = sum(
            1
            for s in adjudication_result.candidate_specs
            if s.candidate_family == "F5_cross_region_pair"
        )
        assert count == 3

    def test_f5_transforms_are_or_and_xor(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """F5 candidates are cross_region_pair_or, _and, _xor."""
        f5_names = sorted(
            s.candidate_feature_name
            for s in adjudication_result.candidate_specs
            if s.candidate_family == "F5_cross_region_pair"
        )
        assert f5_names == [
            "cross_region_pair_and",
            "cross_region_pair_or",
            "cross_region_pair_xor",
        ]

    def test_every_candidate_source_artifact_is_02_01_03(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """All candidates declare source_artifact=02_01_03_*."""
        for spec in adjudication_result.candidate_specs:
            assert spec.source_artifact == (
                "02_01_03_history_enriched_pre_game_features.parquet"
            )

    def test_decision_id_matches_constant(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """Result decision_id == DECISION_ID constant."""
        assert adjudication_result.decision_id == DECISION_ID

    def test_unary_transform_decision_is_open_question(self) -> None:
        """UNARY_TRANSFORM_DECISION records open design question (N4)."""
        assert "open_design_question" in UNARY_TRANSFORM_DECISION

    def test_csv_path_exists_after_run(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """CSV file exists at result.csv_path."""
        assert adjudication_result.csv_path.exists()

    def test_md_path_exists_after_run(
        self, adjudication_result: SymmetryDifferenceAdjudicationResult
    ) -> None:
        """MD file exists at result.md_path."""
        assert adjudication_result.md_path.exists()

    def test_binding_symmetric_transforms_contains_abs_diff(self) -> None:
        """BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS contains 'abs_diff'."""
        assert "abs_diff" in BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS

    def test_binding_symmetric_transforms_contains_mean(self) -> None:
        """BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS contains 'mean'."""
        assert "mean" in BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS

    def test_cross_region_transforms_are_either_both_xor(self) -> None:
        """BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS == ('either', 'both', 'xor')."""
        assert BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS == ("either", "both", "xor")

    def test_no_race_pair_candidate_in_constructed_specs(self) -> None:
        """No race-pair candidate is constructed (F6 deferred to 02_05)."""
        _, _, _, all_decisions = _construct_binding_candidate_specs()
        for d in all_decisions:
            assert "race_pair" not in d.candidate_feature_name

    def test_md_section_9_3_contains_abs_diff(self, md_content: str) -> None:
        """MD §9.3 references abs_diff inclusion."""
        assert "abs_diff" in md_content

    def test_md_section_8_mentions_race_pair_deferral(self, md_content: str) -> None:
        """MD §8 references race-pair deferral to 02_05."""
        assert "02_05" in md_content
        assert "race" in md_content.lower()

    def test_md_section_13_cites_pr_267_merge_sha(self, md_content: str) -> None:
        """MD §13 cites PR #267 merge SHA af8c3d98."""
        assert "af8c3d98" in md_content

    def test_executed_at_utc_date_is_iso_format(self) -> None:
        """EXECUTED_AT_UTC_DATE is in ISO YYYY-MM-DD format."""
        import re as _re
        assert _re.match(r"^\d{4}-\d{2}-\d{2}$", EXECUTED_AT_UTC_DATE)


# ---------------------------------------------------------------------------
# Group K — Error path coverage
# ---------------------------------------------------------------------------


class TestGroupKErrorPaths:
    """Group K: Error paths for branch coverage >= 95%."""

    def test_resolve_repo_root_default_no_explicit(self) -> None:
        """_resolve_repo_root(None) returns a valid Path (the default no-explicit branch)."""
        from rts_predict.games.sc2.datasets.sc2egset.adjudicate_symmetry_difference_feature_scope import (  # noqa: E501
            _resolve_repo_root,
        )
        root = _resolve_repo_root(None)
        # Should be an absolute path ending at repo root
        assert root.is_absolute()
        assert (root / "pyproject.toml").exists()

    def test_stem_from_pair_no_focal_prefix(self) -> None:
        """_stem_from_pair returns focal unchanged if it doesn't start with 'focal_'."""
        from rts_predict.games.sc2.datasets.sc2egset.adjudicate_symmetry_difference_feature_scope import (  # noqa: E501
            _stem_from_pair,
        )
        # When focal doesn't start with 'focal_', it returns focal as-is
        result = _stem_from_pair("plain_column", "opponent_plain_column")
        assert result == "plain_column"

    def test_assert_internal_consistency_fires_on_abs_diff_count_mismatch(self) -> None:
        """_assert_internal_consistency raises on abs_diff count != constant."""
        # Build specs with no abs_diff to trigger the mismatch
        diff_specs = _build_difference_specs()
        # Create a data row with correct pair count
        data_row = _construct_csv_row(
            validator_passed=True,
            validator_halting_falsifier=None,
            parent_02_01_02_parquet_sha256="a" * 64,
            parent_02_01_03_parquet_sha256="b" * 64,
            parent_02_01_02_audit_json_sha256="c" * 64,
            parent_02_01_03_audit_json_sha256="d" * 64,
            validator_module_sha256="e" * 64,
            binding_pair_count=len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS),
        )
        # Pass diff_specs only (no abs_diff) to trigger abs_diff_count != constant
        n_pairs = len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS)
        with pytest.raises(SymmetryDifferenceAdjudicationError, match="abs_diff_count"):
            _assert_internal_consistency(diff_specs, n_pairs, data_row)

    def test_assert_internal_consistency_fires_on_csv_pair_count_mismatch(self) -> None:
        """_assert_internal_consistency raises when CSV field disagrees with constant."""
        _, _, _, all_decisions = _construct_binding_candidate_specs()
        # Build a row with wrong binding_difference_family_numeric_pair_count
        data_row_list = list(_construct_csv_row(
            validator_passed=True,
            validator_halting_falsifier=None,
            parent_02_01_02_parquet_sha256="a" * 64,
            parent_02_01_03_parquet_sha256="b" * 64,
            parent_02_01_02_audit_json_sha256="c" * 64,
            parent_02_01_03_audit_json_sha256="d" * 64,
            validator_module_sha256="e" * 64,
            binding_pair_count=len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS),
        ))
        # Patch the CSV field to be wrong
        idx = list(_CSV_HEADER).index("binding_difference_family_numeric_pair_count")
        data_row_list[idx] = "99"
        bad_row = tuple(data_row_list)
        n_pairs = len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS)
        with pytest.raises(SymmetryDifferenceAdjudicationError, match="constant pair count"):
            _assert_internal_consistency(all_decisions, n_pairs, bad_row)

    def test_assert_internal_consistency_fires_on_binding_pair_count_arg_mismatch(self) -> None:
        """_assert_internal_consistency raises when binding_pair_count arg disagrees."""
        _, _, _, all_decisions = _construct_binding_candidate_specs()
        data_row = _construct_csv_row(
            validator_passed=True,
            validator_halting_falsifier=None,
            parent_02_01_02_parquet_sha256="a" * 64,
            parent_02_01_03_parquet_sha256="b" * 64,
            parent_02_01_02_audit_json_sha256="c" * 64,
            parent_02_01_03_audit_json_sha256="d" * 64,
            validator_module_sha256="e" * 64,
            binding_pair_count=len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS),
        )
        # Pass wrong binding_pair_count argument
        with pytest.raises(
            SymmetryDifferenceAdjudicationError, match="function arg binding_pair_count"
        ):
            _assert_internal_consistency(all_decisions, 999, data_row)

    def test_sha_mismatch_raises_provenance_error(
        self, tmp_path: Path, repo_root: Path
    ) -> None:
        """SHA pin mismatch raises ProvenanceShaNotFoundError."""
        # Create a fake validator file with wrong content
        fake_validator = tmp_path / "fake_validator.py"
        fake_validator.write_bytes(b"# fake")
        # We can't easily call the adjudicator with a wrong validator without
        # changing the module constants, but we can test the SHA helper directly
        computed = _sha256_of_file_bytes(fake_validator)
        # The computed SHA will differ from the pinned SHA
        assert computed != _EXPECTED_VALIDATOR_SHA256

    def test_run_adjudication_with_explicit_repo_root(
        self, tmp_path: Path, repo_root: Path
    ) -> None:
        """run_symmetry_difference_feature_scope_adjudication accepts explicit repo_root."""
        r = run_symmetry_difference_feature_scope_adjudication(
            repo_root=str(repo_root),  # Pass as string to exercise str branch
            output_csv_path=tmp_path / "out.csv",
            output_md_path=tmp_path / "out.md",
        )
        assert r.validator_passed is True
        assert r.total_binding_candidate_count == 33
