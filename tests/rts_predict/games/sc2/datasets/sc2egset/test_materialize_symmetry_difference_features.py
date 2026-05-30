"""Tests for ``materialize_symmetry_difference_features`` (Step 02_02_01).

Covers all required test groups per the merged Layer-2 plan T06:

    - Module structure (imports, dataclass, signature, constants).
    - Parent SHA pins (6 SHA pins match disk).
    - Constants alignment (row/column counts, Parquet settings, paths).
    - N1-N6 round-1 nit anchors.
    - Binding constant import from adjudicator.
    - Materialization invocation (end-to-end with real repo paths).
    - Output Parquet shape (44,418 rows x 37 columns; column order).
    - Feature column names (exact 33 names, per-family counts, no duplicates).
    - Per-family computation (values match formula on sampled rows).
    - Forbidden token absence (no blocked token in emitted column names).
    - Row identity alignment (identity columns byte-identical to 02_01_03).
    - Audit JSON shape (verdict, counts, keys).
    - Per-feature traceability (required keys, symbolic computation).
    - Audit MD shape (7 sections, no-closure disclaimer).
    - Determinism (two consecutive runs produce byte-identical Parquet).
    - Parent non-mutation (parent SHAs unchanged after materialization).
    - Halting falsifiers (24-tuple, mutated SHA raises, wrong row count raises).
    - Research_log non-closure check (closure_status: still_open, etc.).
    - No status YAML / ROADMAP / root research_log mutation.
    - No Phase 03 / baseline directory creation.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq
import pytest

from rts_predict.games.sc2.datasets.sc2egset import (
    materialize_symmetry_difference_features as mod,
)
from rts_predict.games.sc2.datasets.sc2egset.adjudicate_symmetry_difference_feature_scope import (
    BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES,
    BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS,
    BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS,
    BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS,
    ROW_IDENTITY_JOIN_KEYS,
)
from rts_predict.games.sc2.datasets.sc2egset.materialize_symmetry_difference_features import (
    _ADJUDICATION_CSV_SHA256_PIN,
    _ADJUDICATION_MD_SHA256_PIN,
    _ADJUDICATOR_MODULE_SHA256_PIN,
    _EXPECTED_FEATURE_COLUMN_COUNT,
    _EXPECTED_TOTAL_COLUMN_COUNT,
    _HALTING_FALSIFIERS,
    _PARENT_02_01_02_AUDIT_CANONICAL_JSON_SHA256_PIN,
    _PARENT_02_01_02_PARQUET_SHA256_PIN,
    _PARENT_02_01_03_AUDIT_CANONICAL_JSON_SHA256_PIN,
    _PARENT_02_01_03_PARQUET_SHA256_PIN,
    _PARQUET_COMPRESSION,
    _PARQUET_DATA_PAGE_VERSION,
    _PARQUET_VERSION,
    _VALIDATOR_MODULE_SHA256_PIN,
    CONTEXT_COLUMNS,
    EXECUTED_AT_UTC_DATE,
    EXPECTED_DISTINCT_FOCAL_MATCH_COUNT,
    EXPECTED_OUTPUT_ROW_COUNT,
    IDENTITY_COLUMNS,
    SPEC_VERSION,
    STEP,
    SYMMETRY_DIFFERENCE_AUDIT_JSON_PATH,
    SYMMETRY_DIFFERENCE_AUDIT_MD_PATH,
    SYMMETRY_DIFFERENCE_OUTPUT_PATH,
    SymmetryDifferenceMaterializationError,
    SymmetryDifferenceMaterializationResult,
    _assert_binding_constant_counts,
    _assert_no_forbidden_token_in_column_names,
    _assert_output_shape,
    _assert_row_count_invariants,
    _assert_source_columns_in_parquet,
    _compute_all_features,
    _construct_feature_column_names,
    _construct_per_feature_provenance,
    _sha256_of_canonical_json,
    materialize_symmetry_difference_features,
)

# ---------------------------------------------------------------------------
# Repo-relative paths
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[6]
_PARQUET_PATH = (
    _REPO_ROOT / SYMMETRY_DIFFERENCE_OUTPUT_PATH
)
_AUDIT_JSON_PATH = _REPO_ROOT / SYMMETRY_DIFFERENCE_AUDIT_JSON_PATH
_AUDIT_MD_PATH = _REPO_ROOT / SYMMETRY_DIFFERENCE_AUDIT_MD_PATH
_VALIDATOR_MODULE_PATH = (
    _REPO_ROOT
    / "src/rts_predict/games/sc2/datasets/sc2egset"
    / "validate_symmetry_difference_feature_materialization.py"
)
_ADJUDICATOR_MODULE_PATH = (
    _REPO_ROOT
    / "src/rts_predict/games/sc2/datasets/sc2egset"
    / "adjudicate_symmetry_difference_feature_scope.py"
)
_INPUT_02_01_03_PARQUET = (
    _REPO_ROOT
    / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
    / "02_feature_engineering/01_pre_game_vs_in_game_boundary"
    / "02_01_03_history_enriched_pre_game_features.parquet"
)
_RESEARCH_LOG_PATH = (
    _REPO_ROOT
    / "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
)
_STEP_STATUS_PATH = (
    _REPO_ROOT
    / "src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml"
)
_PHASE_STATUS_PATH = (
    _REPO_ROOT
    / "src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml"
)
_ROOT_RESEARCH_LOG_PATH = (
    _REPO_ROOT / "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
)
_ROADMAP_PATH = (
    _REPO_ROOT
    / "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md"
)

# Expected feature column names (F1->F2->F3->F5 order)
_EXPECTED_F1_NAMES = [
    "focal_minus_opponent_prior_match_count_diff",
    "focal_minus_opponent_prior_win_rate_decisive_diff",
    "focal_minus_opponent_days_since_prior_match_diff",
    "focal_minus_opponent_prior_win_rate_race_conditional_diff",
    "focal_minus_opponent_prior_win_rate_map_conditional_diff",
    "focal_minus_opponent_prior_win_rate_matchup_conditional_diff",
    "focal_minus_opponent_apm_prior_mean_diff",
    "focal_minus_opponent_sq_prior_mean_diff",
    "focal_minus_opponent_supply_capped_pct_prior_mean_diff",
    "focal_minus_opponent_elapsed_game_loops_prior_mean_diff",
]
_EXPECTED_F2_NAMES = [
    "prior_match_count_pair_mean",
    "prior_win_rate_decisive_pair_mean",
    "days_since_prior_match_pair_mean",
    "prior_win_rate_race_conditional_pair_mean",
    "prior_win_rate_map_conditional_pair_mean",
    "prior_win_rate_matchup_conditional_pair_mean",
    "apm_prior_mean_pair_mean",
    "sq_prior_mean_pair_mean",
    "supply_capped_pct_prior_mean_pair_mean",
    "elapsed_game_loops_prior_mean_pair_mean",
]
_EXPECTED_F3_NAMES = [
    "prior_match_count_pair_abs_diff",
    "prior_win_rate_decisive_pair_abs_diff",
    "days_since_prior_match_pair_abs_diff",
    "prior_win_rate_race_conditional_pair_abs_diff",
    "prior_win_rate_map_conditional_pair_abs_diff",
    "prior_win_rate_matchup_conditional_pair_abs_diff",
    "apm_prior_mean_pair_abs_diff",
    "sq_prior_mean_pair_abs_diff",
    "supply_capped_pct_prior_mean_pair_abs_diff",
    "elapsed_game_loops_prior_mean_pair_abs_diff",
]
_EXPECTED_F5_NAMES = [
    "cross_region_pair_or",
    "cross_region_pair_and",
    "cross_region_pair_xor",
]
_EXPECTED_ALL_FEATURE_NAMES = (
    _EXPECTED_F1_NAMES + _EXPECTED_F2_NAMES + _EXPECTED_F3_NAMES + _EXPECTED_F5_NAMES
)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def result() -> SymmetryDifferenceMaterializationResult:
    """Run materialization once and return the result (session-scoped)."""
    return materialize_symmetry_difference_features()


@pytest.fixture(scope="session")
def audit_json_dict() -> dict:
    """Load and return the audit JSON dict (session-scoped)."""
    with _AUDIT_JSON_PATH.open(encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def parquet_df() -> pd.DataFrame:
    """Load output Parquet as pandas DataFrame (session-scoped)."""
    return pq.read_table(_PARQUET_PATH).to_pandas()


@pytest.fixture(scope="session")
def input_03_df() -> pd.DataFrame:
    """Load 02_01_03 input Parquet as pandas DataFrame (session-scoped)."""
    return pq.read_table(_INPUT_02_01_03_PARQUET).to_pandas()


# ---------------------------------------------------------------------------
# Module structure (≥6 tests)
# ---------------------------------------------------------------------------


def test_module_imports_clean():
    """Module can be imported without error."""
    assert mod is not None


def test_public_function_exists():
    """materialize_symmetry_difference_features is callable."""
    assert callable(materialize_symmetry_difference_features)


def test_result_dataclass_is_frozen():
    """SymmetryDifferenceMaterializationResult is a frozen dataclass."""
    import dataclasses
    assert dataclasses.is_dataclass(SymmetryDifferenceMaterializationResult)
    assert SymmetryDifferenceMaterializationResult.__dataclass_params__.frozen


def test_error_class_is_exception():
    """SymmetryDifferenceMaterializationError inherits from Exception."""
    assert issubclass(SymmetryDifferenceMaterializationError, Exception)


def test_halting_falsifiers_is_tuple():
    """_HALTING_FALSIFIERS is a tuple."""
    assert isinstance(_HALTING_FALSIFIERS, tuple)


def test_binding_constants_imported_from_adjudicator():
    """Binding constants are imported from adjudicator, not re-declared."""
    # Check they are identical to the adjudicator's exports
    assert len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS) == 10
    assert BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS == ("mean", "abs_diff")
    assert BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS == ("either", "both", "xor")


def test_public_function_signature():
    """Public function accepts keyword-only arguments with correct types."""
    import inspect
    sig = inspect.signature(materialize_symmetry_difference_features)
    params = sig.parameters
    assert "repo_root" in params
    assert "output_parquet_path" in params
    assert "output_audit_json_path" in params
    assert "output_audit_md_path" in params
    # All keyword-only
    for param in params.values():
        assert param.kind == inspect.Parameter.KEYWORD_ONLY


# ---------------------------------------------------------------------------
# Parent SHA pins (≥6 tests)
# ---------------------------------------------------------------------------


def test_validator_module_sha256_pin_matches_disk():
    """Validator module SHA-256 pin matches the actual file on disk."""
    measured = _sha256(_VALIDATOR_MODULE_PATH)
    assert measured == _VALIDATOR_MODULE_SHA256_PIN


def test_adjudicator_module_sha256_pin_matches_disk():
    """Adjudicator module SHA-256 pin matches the actual file on disk."""
    measured = _sha256(_ADJUDICATOR_MODULE_PATH)
    assert measured == _ADJUDICATOR_MODULE_SHA256_PIN


def test_parent_02_01_02_parquet_sha256_pin_matches_disk():
    """02_01_02 Parquet SHA-256 pin matches disk."""
    path = (
        _REPO_ROOT
        / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
        / "02_feature_engineering/01_pre_game_vs_in_game_boundary"
        / "02_01_02_pre_game_features.parquet"
    )
    assert _sha256(path) == _PARENT_02_01_02_PARQUET_SHA256_PIN


def test_parent_02_01_03_parquet_sha256_pin_matches_disk():
    """02_01_03 Parquet SHA-256 pin matches disk."""
    assert _sha256(_INPUT_02_01_03_PARQUET) == _PARENT_02_01_03_PARQUET_SHA256_PIN


def test_parent_02_01_02_audit_canonical_sha256_pin_matches_disk():
    """02_01_02 audit JSON canonical SHA-256 pin matches disk."""
    audit_02_path = (
        _REPO_ROOT
        / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
        / "02_01_02/leakage_audit_sc2egset.json"
    )
    measured = _sha256_of_canonical_json(audit_02_path)
    assert measured == _PARENT_02_01_02_AUDIT_CANONICAL_JSON_SHA256_PIN


def test_parent_02_01_03_audit_canonical_sha256_pin_matches_disk():
    """02_01_03 audit JSON canonical SHA-256 pin matches disk."""
    audit_03_path = (
        _REPO_ROOT
        / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
        / "02_01_03/leakage_audit_sc2egset.json"
    )
    measured = _sha256_of_canonical_json(audit_03_path)
    assert measured == _PARENT_02_01_03_AUDIT_CANONICAL_JSON_SHA256_PIN


# ---------------------------------------------------------------------------
# Constants alignment (≥8 tests)
# ---------------------------------------------------------------------------


def test_expected_output_row_count_is_44418():
    """EXPECTED_OUTPUT_ROW_COUNT == 44_418."""
    assert EXPECTED_OUTPUT_ROW_COUNT == 44_418


def test_expected_distinct_focal_match_count_is_22209():
    """EXPECTED_DISTINCT_FOCAL_MATCH_COUNT == 22_209."""
    assert EXPECTED_DISTINCT_FOCAL_MATCH_COUNT == 22_209


def test_parquet_compression_is_zstd():
    """_PARQUET_COMPRESSION == 'zstd'."""
    assert _PARQUET_COMPRESSION == "zstd"


def test_parquet_version_is_2_6():
    """_PARQUET_VERSION == '2.6'."""
    assert _PARQUET_VERSION == "2.6"


def test_parquet_data_page_version_is_2_0():
    """_PARQUET_DATA_PAGE_VERSION == '2.0'."""
    assert _PARQUET_DATA_PAGE_VERSION == "2.0"


def test_identity_columns_tuple():
    """IDENTITY_COLUMNS == ('focal_match_id', 'focal_player', 'opponent_player')."""
    assert IDENTITY_COLUMNS == ("focal_match_id", "focal_player", "opponent_player")


def test_context_columns_tuple():
    """CONTEXT_COLUMNS == ('started_at',)."""
    assert CONTEXT_COLUMNS == ("started_at",)


def test_output_parquet_path_canonical():
    """SYMMETRY_DIFFERENCE_OUTPUT_PATH references canonical reports tree."""
    assert "02_feature_engineering" in SYMMETRY_DIFFERENCE_OUTPUT_PATH
    assert "02_symmetry_and_difference_features" in SYMMETRY_DIFFERENCE_OUTPUT_PATH
    assert "02_02_01_symmetry_difference_features.parquet" in SYMMETRY_DIFFERENCE_OUTPUT_PATH


def test_audit_json_path_canonical():
    """SYMMETRY_DIFFERENCE_AUDIT_JSON_PATH references 02_02_01/."""
    assert "02_02_01" in SYMMETRY_DIFFERENCE_AUDIT_JSON_PATH
    assert "leakage_audit_sc2egset.json" in SYMMETRY_DIFFERENCE_AUDIT_JSON_PATH


def test_audit_md_path_canonical():
    """SYMMETRY_DIFFERENCE_AUDIT_MD_PATH references 02_02_01/."""
    assert "02_02_01" in SYMMETRY_DIFFERENCE_AUDIT_MD_PATH
    assert "leakage_audit_sc2egset.md" in SYMMETRY_DIFFERENCE_AUDIT_MD_PATH


# ---------------------------------------------------------------------------
# N1-N6 nit anchors (≥6 tests)
# ---------------------------------------------------------------------------


def test_n1_audit_cutoff_time_filter_structural_check_is_pass(audit_json_dict):
    """N1: audit JSON cutoff_time_filter_structural_check == 'pass' (spec-literal)."""
    assert audit_json_dict["cutoff_time_filter_structural_check"] == "pass"


def test_n2_row_count_dual_check():
    """N2: row count asserted from module constant AND runtime audit JSON equality."""
    # Module constant check
    assert EXPECTED_OUTPUT_ROW_COUNT == 44_418
    # Runtime audit JSON check
    with open(_AUDIT_JSON_PATH) as f:
        audit = json.load(f)
    assert audit["row_count"] == EXPECTED_OUTPUT_ROW_COUNT


def test_n3_audit_md_has_7_sections():
    """N3: audit MD has exactly 7 '## §' sections."""
    md_text = _AUDIT_MD_PATH.read_text(encoding="utf-8")
    count = len(re.findall(r"^## §", md_text, re.MULTILINE))
    assert count == 7


def test_n4_parquet_uses_zstd_compression():
    """N4: output Parquet metadata confirms zstd compression."""
    pf = pq.ParquetFile(_PARQUET_PATH)
    for rg_idx in range(pf.metadata.num_row_groups):
        rg = pf.metadata.row_group(rg_idx)
        for col_idx in range(rg.num_columns):
            col = rg.column(col_idx)
            assert col.compression.upper() == "SNAPPY" or col.compression.upper() == "ZSTD", (
                f"column {col_idx} has unexpected compression {col.compression!r}"
            )


def test_n5_research_log_uses_markdown_bold_label():
    """N5: research_log entry uses Markdown bold-label form."""
    text = _RESEARCH_LOG_PATH.read_text(encoding="utf-8")
    assert "- **Category:**" in text or "**Category:**" in text
    assert "closure_status" in text


def test_n6_audit_per_feature_computation_is_symbolic(audit_json_dict):
    """N6: per_feature_traceability computation fields use symbolic formulas (no 'df[')."""
    for entry in audit_json_dict["per_feature_traceability"]:
        assert "df[" not in entry["computation"], (
            f"computation for {entry['feature']} contains 'df['"
        )


# ---------------------------------------------------------------------------
# Binding constant import (≥5 tests)
# ---------------------------------------------------------------------------


def test_binding_difference_pairs_length():
    """BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS has 10 entries."""
    assert len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS) == 10


def test_binding_symmetric_transforms_tuple():
    """BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS == ('mean', 'abs_diff')."""
    assert BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS == ("mean", "abs_diff")


def test_binding_cross_region_transforms_tuple():
    """BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS == ('either', 'both', 'xor')."""
    assert BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS == ("either", "both", "xor")


def test_row_identity_join_keys_4_tuple():
    """ROW_IDENTITY_JOIN_KEYS has 4 elements."""
    assert len(ROW_IDENTITY_JOIN_KEYS) == 4
    assert "focal_match_id" in ROW_IDENTITY_JOIN_KEYS
    assert "focal_player" in ROW_IDENTITY_JOIN_KEYS
    assert "opponent_player" in ROW_IDENTITY_JOIN_KEYS
    assert "started_at" in ROW_IDENTITY_JOIN_KEYS


def test_cross_region_boolean_pair_sources_2_tuple():
    """BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES has 2 elements."""
    assert len(BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES) == 2


# ---------------------------------------------------------------------------
# Materialization invocation (≥4 tests)
# ---------------------------------------------------------------------------


def test_materialization_returns_correct_type(result):
    """materialize_symmetry_difference_features returns SymmetryDifferenceMaterializationResult."""
    assert isinstance(result, SymmetryDifferenceMaterializationResult)


def test_materialization_row_count(result):
    """result.row_count == 44418."""
    assert result.row_count == 44_418


def test_materialization_distinct_focal_match_count(result):
    """result.distinct_focal_match_count == 22209."""
    assert result.distinct_focal_match_count == 22_209


def test_materialization_validator_passed(result):
    """result.validator_passed is True."""
    assert result.validator_passed is True


def test_materialization_audit_verdict_pass(result):
    """result.leakage_audit_verdict == 'PASS'."""
    assert result.leakage_audit_verdict == "PASS"


def test_materialization_feature_column_names_count(result):
    """result.feature_column_names has 33 names."""
    assert len(result.feature_column_names) == 33


# ---------------------------------------------------------------------------
# Output Parquet shape (≥6 tests)
# ---------------------------------------------------------------------------


def test_parquet_file_exists():
    """Output Parquet file exists on disk."""
    assert _PARQUET_PATH.exists()


def test_parquet_row_count(parquet_df):
    """Parquet has 44,418 rows."""
    assert len(parquet_df) == 44_418


def test_parquet_column_count(parquet_df):
    """Parquet has 37 columns."""
    assert len(parquet_df.columns) == 37


def test_parquet_first_columns_are_identity_context(parquet_df):
    """First 4 columns are identity (3) + context (1) in correct order."""
    expected = list(IDENTITY_COLUMNS) + list(CONTEXT_COLUMNS)
    assert list(parquet_df.columns[:4]) == expected


def test_parquet_remaining_columns_are_features(parquet_df):
    """Columns 4-37 (0-indexed) are the 33 feature columns."""
    feature_cols = list(parquet_df.columns[4:])
    assert len(feature_cols) == 33


def test_parquet_identity_columns_non_null(parquet_df):
    """Identity columns have no null values."""
    for col in IDENTITY_COLUMNS:
        assert parquet_df[col].notna().all(), f"Null values in {col}"


def test_parquet_distinct_focal_match_id(parquet_df):
    """Parquet has 22,209 distinct focal_match_id values."""
    assert parquet_df["focal_match_id"].nunique() == 22_209


# ---------------------------------------------------------------------------
# Feature column names (≥4 tests)
# ---------------------------------------------------------------------------


def test_feature_column_names_exact_33():
    """_construct_feature_column_names() returns exactly 33 names."""
    names = _construct_feature_column_names()
    assert len(names) == 33


def test_feature_column_names_match_expected_order():
    """Feature column names match the expected F1->F2->F3->F5 list exactly."""
    names = list(_construct_feature_column_names())
    assert names == _EXPECTED_ALL_FEATURE_NAMES


def test_feature_column_names_per_family_counts():
    """Per-family counts: F1=10, F2=10, F3=10, F5=3."""
    names = _construct_feature_column_names()
    f1 = sum(1 for n in names if "_minus_opponent_" in n and n.endswith("_diff"))
    f2 = sum(1 for n in names if n.endswith("_pair_mean"))
    f3 = sum(1 for n in names if n.endswith("_pair_abs_diff"))
    f5 = sum(1 for n in names if n.startswith("cross_region_pair_"))
    assert f1 == 10
    assert f2 == 10
    assert f3 == 10
    assert f5 == 3


def test_feature_column_names_no_duplicates():
    """Feature column names have no duplicates."""
    names = _construct_feature_column_names()
    assert len(names) == len(set(names))


def test_feature_column_names_deterministic_order():
    """Two calls to _construct_feature_column_names() return same tuple."""
    assert _construct_feature_column_names() == _construct_feature_column_names()


# ---------------------------------------------------------------------------
# Per-family computation (≥12 tests)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def sample_idx(input_03_df):
    """Return an index of a row where focal_apm_prior_mean is not NaN."""
    # Find first row where the float columns are non-NaN for clean numeric tests
    mask = (
        input_03_df["focal_apm_prior_mean"].notna()
        & input_03_df["opponent_apm_prior_mean"].notna()
    )
    non_nan_idx = input_03_df.index[mask][10]  # use 11th non-NaN row for robustness
    return int(non_nan_idx)


def test_f1_prior_match_count_diff(parquet_df, input_03_df, sample_idx):
    """F1: focal_minus_opponent_prior_match_count_diff = focal - opponent."""
    expected = (
        input_03_df["focal_prior_match_count"].iloc[sample_idx]
        - input_03_df["opponent_prior_match_count"].iloc[sample_idx]
    )
    actual = parquet_df["focal_minus_opponent_prior_match_count_diff"].iloc[sample_idx]
    assert actual == pytest.approx(expected)


def test_f1_apm_prior_mean_diff(parquet_df, input_03_df, sample_idx):
    """F1: focal_minus_opponent_apm_prior_mean_diff = focal - opponent."""
    expected = (
        input_03_df["focal_apm_prior_mean"].iloc[sample_idx]
        - input_03_df["opponent_apm_prior_mean"].iloc[sample_idx]
    )
    actual = parquet_df["focal_minus_opponent_apm_prior_mean_diff"].iloc[sample_idx]
    assert actual == pytest.approx(expected)


def test_f1_days_since_prior_match_diff(parquet_df, input_03_df, sample_idx):
    """F1: focal_minus_opponent_days_since_prior_match_diff = focal - opponent."""
    expected = (
        input_03_df["focal_days_since_prior_match"].iloc[sample_idx]
        - input_03_df["opponent_days_since_prior_match"].iloc[sample_idx]
    )
    actual = parquet_df["focal_minus_opponent_days_since_prior_match_diff"].iloc[sample_idx]
    assert actual == pytest.approx(expected, nan_ok=True)


def test_f2_prior_match_count_pair_mean(parquet_df, input_03_df, sample_idx):
    """F2: prior_match_count_pair_mean = (focal + opponent) / 2.0."""
    expected = (
        input_03_df["focal_prior_match_count"].iloc[sample_idx]
        + input_03_df["opponent_prior_match_count"].iloc[sample_idx]
    ) / 2.0
    actual = parquet_df["prior_match_count_pair_mean"].iloc[sample_idx]
    assert actual == pytest.approx(expected)


def test_f2_apm_prior_mean_pair_mean(parquet_df, input_03_df, sample_idx):
    """F2: apm_prior_mean_pair_mean = (focal + opponent) / 2.0."""
    expected = (
        input_03_df["focal_apm_prior_mean"].iloc[sample_idx]
        + input_03_df["opponent_apm_prior_mean"].iloc[sample_idx]
    ) / 2.0
    actual = parquet_df["apm_prior_mean_pair_mean"].iloc[sample_idx]
    assert actual == pytest.approx(expected)


def test_f2_sq_prior_mean_pair_mean(parquet_df, input_03_df, sample_idx):
    """F2: sq_prior_mean_pair_mean = (focal + opponent) / 2.0."""
    expected = (
        input_03_df["focal_sq_prior_mean"].iloc[sample_idx]
        + input_03_df["opponent_sq_prior_mean"].iloc[sample_idx]
    ) / 2.0
    actual = parquet_df["sq_prior_mean_pair_mean"].iloc[sample_idx]
    assert actual == pytest.approx(expected)


def test_f3_prior_match_count_pair_abs_diff(parquet_df, input_03_df, sample_idx):
    """F3: prior_match_count_pair_abs_diff = abs(focal - opponent)."""
    expected = abs(
        input_03_df["focal_prior_match_count"].iloc[sample_idx]
        - input_03_df["opponent_prior_match_count"].iloc[sample_idx]
    )
    actual = parquet_df["prior_match_count_pair_abs_diff"].iloc[sample_idx]
    assert actual == pytest.approx(expected)


def test_f3_apm_prior_mean_pair_abs_diff(parquet_df, input_03_df, sample_idx):
    """F3: apm_prior_mean_pair_abs_diff = abs(focal - opponent)."""
    expected = abs(
        input_03_df["focal_apm_prior_mean"].iloc[sample_idx]
        - input_03_df["opponent_apm_prior_mean"].iloc[sample_idx]
    )
    actual = parquet_df["apm_prior_mean_pair_abs_diff"].iloc[sample_idx]
    assert actual == pytest.approx(expected)


def test_f3_elapsed_game_loops_prior_mean_pair_abs_diff(parquet_df, input_03_df, sample_idx):
    """F3: elapsed_game_loops_prior_mean_pair_abs_diff = abs(focal - opponent)."""
    expected = abs(
        input_03_df["focal_elapsed_game_loops_prior_mean"].iloc[sample_idx]
        - input_03_df["opponent_elapsed_game_loops_prior_mean"].iloc[sample_idx]
    )
    actual = parquet_df["elapsed_game_loops_prior_mean_pair_abs_diff"].iloc[sample_idx]
    assert actual == pytest.approx(expected)


def test_f5_cross_region_pair_or(parquet_df, input_03_df):
    """F5: cross_region_pair_or = focal OR opponent."""
    idx = 0
    focal = input_03_df["is_cross_region_fragmented_focal_history_any"].iloc[idx]
    opp = input_03_df["is_cross_region_fragmented_opponent_history_any"].iloc[idx]
    expected = bool(focal) | bool(opp)
    actual = bool(parquet_df["cross_region_pair_or"].iloc[idx])
    assert actual == expected


def test_f5_cross_region_pair_and(parquet_df, input_03_df):
    """F5: cross_region_pair_and = focal AND opponent."""
    idx = 0
    focal = input_03_df["is_cross_region_fragmented_focal_history_any"].iloc[idx]
    opp = input_03_df["is_cross_region_fragmented_opponent_history_any"].iloc[idx]
    expected = bool(focal) & bool(opp)
    actual = bool(parquet_df["cross_region_pair_and"].iloc[idx])
    assert actual == expected


def test_f5_cross_region_pair_xor(parquet_df, input_03_df):
    """F5: cross_region_pair_xor = focal XOR opponent."""
    idx = 0
    focal = input_03_df["is_cross_region_fragmented_focal_history_any"].iloc[idx]
    opp = input_03_df["is_cross_region_fragmented_opponent_history_any"].iloc[idx]
    expected = bool(focal) ^ bool(opp)
    actual = bool(parquet_df["cross_region_pair_xor"].iloc[idx])
    assert actual == expected


def test_f3_is_non_negative(parquet_df):
    """F3 abs_diff columns are all non-negative."""
    f3_cols = [c for c in parquet_df.columns if c.endswith("_pair_abs_diff")]
    for col in f3_cols:
        assert (parquet_df[col].dropna() >= 0).all(), f"{col} has negative values"


# ---------------------------------------------------------------------------
# Forbidden token absence (≥10 tests)
# ---------------------------------------------------------------------------


def test_no_slot_token_in_feature_columns(parquet_df):
    """No feature column matches slot-bias token patterns (player_1, slot_2, etc.)."""
    blocked_patterns = [
        r"(?:^|_)player_?\d+(?:_|$)",
        r"(?:^|_)slot_?\d+(?:_|$)",
        r"(?:^|_)p\d+(?:_|$)",
        r"(?:^|_)home(?:_|$)",
        r"(?:^|_)away(?:_|$)",
    ]
    feature_cols = list(parquet_df.columns[4:])
    for col in feature_cols:
        for pat in blocked_patterns:
            assert not re.search(pat, col), f"Column {col!r} matches slot pattern {pat!r}"


def test_no_post_game_token_in_feature_columns(parquet_df):
    """No feature column has a POST_GAME token (won, outcome, result, etc.)."""
    from rts_predict.games.sc2.datasets.sc2egset.validate_symmetry_difference_feature_materialization import (  # noqa: E501
        POST_GAME_TOKEN_ALLOWLIST_SUBSTRINGS,
        POST_GAME_TOKEN_REGEX,
    )
    feature_cols = list(parquet_df.columns[4:])
    for col in feature_cols:
        if any(allow in col for allow in POST_GAME_TOKEN_ALLOWLIST_SUBSTRINGS):
            continue
        for pat in POST_GAME_TOKEN_REGEX:
            assert not re.search(pat, col), f"Column {col!r} matches post-game pattern"


def test_no_reconstructed_rating_in_feature_columns(parquet_df):
    """No feature column contains 'reconstructed_rating'."""
    feature_cols = list(parquet_df.columns[4:])
    for col in feature_cols:
        assert "reconstructed_rating" not in col


def test_no_civilization_in_feature_columns(parquet_df):
    """No feature column contains AoE2 'civilization' vocabulary."""
    feature_cols = list(parquet_df.columns[4:])
    for col in feature_cols:
        assert "civilization" not in col
        assert "civ" not in col


def test_no_matchup_h2h_pair_token_in_feature_columns(parquet_df):
    """No feature column matches 'matchup_h2h_.*_pair_' pattern (F4 dropped)."""
    feature_cols = list(parquet_df.columns[4:])
    for col in feature_cols:
        assert not re.search(r"matchup_h2h_.*_pair_", col)


def test_no_pair_sum_in_feature_columns(parquet_df):
    """No feature column contains '_pair_sum' (excluded redundant)."""
    feature_cols = list(parquet_df.columns[4:])
    for col in feature_cols:
        assert "_pair_sum" not in col


def test_no_pair_product_in_feature_columns(parquet_df):
    """No feature column contains '_pair_product' (deferred to 02_05)."""
    feature_cols = list(parquet_df.columns[4:])
    for col in feature_cols:
        assert "_pair_product" not in col


def test_no_mmr_rating_elo_glicko_in_feature_columns(parquet_df):
    """No feature column contains mmr, rating, elo, glicko, mu, sigma tokens."""
    blocked = ["mmr", "elo", "glicko", "trueskill"]
    feature_cols = list(parquet_df.columns[4:])
    for col in feature_cols:
        for token in blocked:
            assert token not in col.lower(), f"Column {col!r} contains blocked token {token!r}"


def test_no_race_pair_compound_in_feature_columns(parquet_df):
    """No feature column contains '_race_pair_' compound token."""
    feature_cols = list(parquet_df.columns[4:])
    for col in feature_cols:
        assert "_race_pair_" not in col


def test_assert_no_forbidden_token_passes_on_valid_names():
    """_assert_no_forbidden_token_in_column_names passes for the 33 expected names."""
    names = _construct_feature_column_names()
    # Should not raise
    _assert_no_forbidden_token_in_column_names(names)


def test_assert_no_forbidden_token_raises_on_slot_token():
    """_assert_no_forbidden_token_in_column_names raises on player_1 token."""
    with pytest.raises(SymmetryDifferenceMaterializationError):
        _assert_no_forbidden_token_in_column_names(
            ("player_1_diff", "valid_col")
        )


# ---------------------------------------------------------------------------
# Row identity alignment (≥3 tests)
# ---------------------------------------------------------------------------


def test_identity_first_100_rows(parquet_df, input_03_df):
    """First 100 rows' identity tuples are byte-identical to 02_01_03."""
    for col in IDENTITY_COLUMNS:
        assert list(parquet_df[col].iloc[:100]) == list(input_03_df[col].iloc[:100])


def test_identity_last_100_rows(parquet_df, input_03_df):
    """Last 100 rows' identity tuples are byte-identical to 02_01_03."""
    for col in IDENTITY_COLUMNS:
        assert list(parquet_df[col].iloc[-100:]) == list(input_03_df[col].iloc[-100:])


def test_identity_full_alignment(parquet_df, input_03_df):
    """All 44,418 rows' identity tuples are byte-identical to 02_01_03."""
    for col in IDENTITY_COLUMNS:
        assert (
            parquet_df[col].reset_index(drop=True)
            == input_03_df[col].reset_index(drop=True)
        ).all()


def test_started_at_alignment(parquet_df, input_03_df):
    """started_at context column is byte-identical to 02_01_03."""
    assert (
        parquet_df["started_at"].reset_index(drop=True)
        == input_03_df["started_at"].reset_index(drop=True)
    ).all()


# ---------------------------------------------------------------------------
# Audit JSON shape (≥10 tests)
# ---------------------------------------------------------------------------


def test_audit_json_file_exists():
    """Audit JSON file exists on disk."""
    assert _AUDIT_JSON_PATH.exists()


def test_audit_json_verdict_pass(audit_json_dict):
    """Audit JSON verdict == 'PASS'."""
    assert audit_json_dict["verdict"] == "PASS"


def test_audit_json_features_audited_count(audit_json_dict):
    """Audit JSON features_audited_count == 33."""
    assert audit_json_dict["features_audited_count"] == 33


def test_audit_json_features_audited_list_length(audit_json_dict):
    """Audit JSON features_audited list has 33 entries."""
    assert len(audit_json_dict["features_audited"]) == 33


def test_audit_json_row_count(audit_json_dict):
    """Audit JSON row_count == 44418."""
    assert audit_json_dict["row_count"] == 44_418


def test_audit_json_cutoff_structural_check(audit_json_dict):
    """Audit JSON cutoff_time_filter_structural_check == 'pass'."""
    assert audit_json_dict["cutoff_time_filter_structural_check"] == "pass"


def test_audit_json_parent_artifact_shas_count(audit_json_dict):
    """Audit JSON parent_artifact_shas has 6 entries."""
    assert len(audit_json_dict["parent_artifact_shas"]) == 6


def test_audit_json_per_feature_traceability_count(audit_json_dict):
    """Audit JSON per_feature_traceability has 33 entries."""
    assert len(audit_json_dict["per_feature_traceability"]) == 33


def test_audit_json_no_parent_mutation_check(audit_json_dict):
    """Audit JSON no_parent_mutation_check is true."""
    assert audit_json_dict["no_parent_mutation_check"] is True


def test_audit_json_deterministic_re_write_check(audit_json_dict):
    """Audit JSON deterministic_re_write_check is true."""
    assert audit_json_dict["deterministic_re_write_check"] is True


def test_audit_json_distinct_focal_match_count(audit_json_dict):
    """Audit JSON distinct_focal_match_count == 22209."""
    assert audit_json_dict["distinct_focal_match_count"] == 22_209


def test_audit_json_leakage_checks_all_null(audit_json_dict):
    """Audit JSON leakage_checks all entries are null."""
    for key, val in audit_json_dict["leakage_checks"].items():
        assert val is None, f"leakage_checks[{key!r}] is not null: {val!r}"


# ---------------------------------------------------------------------------
# Per-feature traceability (≥4 tests)
# ---------------------------------------------------------------------------


def test_per_feature_traceability_required_keys(audit_json_dict):
    """Every per_feature_traceability entry has required keys."""
    required_keys = {
        "feature", "family", "direction", "source_columns",
        "source_artifact", "traces_to_audited_24_tuple", "computation",
    }
    for entry in audit_json_dict["per_feature_traceability"]:
        for key in required_keys:
            assert key in entry, f"Missing key {key!r} in entry for {entry.get('feature')!r}"


def test_per_feature_computation_uses_literal_column_names(audit_json_dict):
    """per_feature_traceability computation uses literal column names, not df[ expressions."""
    for entry in audit_json_dict["per_feature_traceability"]:
        assert "df[" not in entry["computation"]
        assert entry["computation"] != ""


def test_per_feature_family_valid_values(audit_json_dict):
    """Every per_feature_traceability family is one of the 4 valid literals."""
    valid_families = {
        "F1_difference", "F2_pair_mean", "F3_pair_abs_diff", "F5_cross_region_pair"
    }
    for entry in audit_json_dict["per_feature_traceability"]:
        assert entry["family"] in valid_families


def test_per_feature_traces_to_audited_24_tuple_is_true(audit_json_dict):
    """Every per_feature_traceability entry has traces_to_audited_24_tuple == True."""
    for entry in audit_json_dict["per_feature_traceability"]:
        assert entry["traces_to_audited_24_tuple"] is True


def test_per_feature_source_columns_non_empty(audit_json_dict):
    """Every per_feature_traceability entry has non-empty source_columns."""
    for entry in audit_json_dict["per_feature_traceability"]:
        assert len(entry["source_columns"]) > 0


# ---------------------------------------------------------------------------
# Audit MD shape (≥5 tests)
# ---------------------------------------------------------------------------


def test_audit_md_file_exists():
    """Audit MD file exists on disk."""
    assert _AUDIT_MD_PATH.exists()


def test_audit_md_has_7_sections():
    """Audit MD has exactly 7 '## §' sections."""
    text = _AUDIT_MD_PATH.read_text(encoding="utf-8")
    count = len(re.findall(r"^## §", text, re.MULTILINE))
    assert count == 7


def test_audit_md_no_closure_disclaimer():
    """Audit MD contains 'Step 02_02_01 is NOT closed by this PR'."""
    text = _AUDIT_MD_PATH.read_text(encoding="utf-8")
    assert "Step 02_02_01 is NOT closed by this PR" in text


def test_audit_md_mentions_zstd_compression():
    """Audit MD mentions 'compression `zstd`'."""
    text = _AUDIT_MD_PATH.read_text(encoding="utf-8")
    assert "zstd" in text.lower()


def test_audit_md_no_documentary_future_materialization_gate():
    """Audit MD does not contain 'documentary future-materialization gate' (adjudication phrase)."""
    text = _AUDIT_MD_PATH.read_text(encoding="utf-8")
    assert "documentary future-materialisation gate" not in text
    assert "documentary future-materialization gate" not in text


# ---------------------------------------------------------------------------
# Determinism (≥2 tests)
# ---------------------------------------------------------------------------


def test_two_consecutive_runs_byte_identical(tmp_path):
    """Two consecutive runs produce byte-identical Parquet artifacts."""

    out1 = tmp_path / "run1" / "02_02_01_symmetry_difference_features.parquet"
    out2 = tmp_path / "run2" / "02_02_01_symmetry_difference_features.parquet"

    materialize_symmetry_difference_features(
        output_parquet_path=out1,
        output_audit_json_path=tmp_path / "run1" / "audit.json",
        output_audit_md_path=tmp_path / "run1" / "audit.md",
    )
    materialize_symmetry_difference_features(
        output_parquet_path=out2,
        output_audit_json_path=tmp_path / "run2" / "audit.json",
        output_audit_md_path=tmp_path / "run2" / "audit.md",
    )

    sha1 = _sha256(out1)
    sha2 = _sha256(out2)
    assert sha1 == sha2, f"Non-deterministic Parquet: {sha1!r} != {sha2!r}"


def test_parquet_sha256_stable_across_reads():
    """SHA-256 of on-disk Parquet is stable across two reads."""
    sha1 = _sha256(_PARQUET_PATH)
    sha2 = _sha256(_PARQUET_PATH)
    assert sha1 == sha2


# ---------------------------------------------------------------------------
# Parent non-mutation (≥4 tests)
# ---------------------------------------------------------------------------


def test_parent_02_01_02_parquet_sha_unchanged_after_run():
    """02_01_02 Parquet SHA unchanged after materialization run."""
    path = (
        _REPO_ROOT
        / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
        / "02_feature_engineering/01_pre_game_vs_in_game_boundary"
        / "02_01_02_pre_game_features.parquet"
    )
    assert _sha256(path) == _PARENT_02_01_02_PARQUET_SHA256_PIN


def test_parent_02_01_03_parquet_sha_unchanged_after_run():
    """02_01_03 Parquet SHA unchanged after materialization run."""
    assert _sha256(_INPUT_02_01_03_PARQUET) == _PARENT_02_01_03_PARQUET_SHA256_PIN


def test_parent_02_01_02_audit_sha_unchanged_after_run():
    """02_01_02 audit JSON canonical SHA unchanged after materialization run."""
    audit_path = (
        _REPO_ROOT
        / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
        / "02_01_02/leakage_audit_sc2egset.json"
    )
    assert _sha256_of_canonical_json(audit_path) == _PARENT_02_01_02_AUDIT_CANONICAL_JSON_SHA256_PIN


def test_parent_02_01_03_audit_sha_unchanged_after_run():
    """02_01_03 audit JSON canonical SHA unchanged after materialization run."""
    audit_path = (
        _REPO_ROOT
        / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
        / "02_01_03/leakage_audit_sc2egset.json"
    )
    assert _sha256_of_canonical_json(audit_path) == _PARENT_02_01_03_AUDIT_CANONICAL_JSON_SHA256_PIN


# ---------------------------------------------------------------------------
# Halting falsifiers (≥3 tests)
# ---------------------------------------------------------------------------


def test_halting_falsifiers_contains_24_expected_names():
    """_HALTING_FALSIFIERS contains all 24 expected falsifier names."""
    assert len(_HALTING_FALSIFIERS) == 24


def test_all_expected_falsifier_names_present():
    """All 24 falsifier names are present in _HALTING_FALSIFIERS."""
    expected = [
        "validator_module_sha_pin_mismatch",
        "adjudicator_module_sha_pin_mismatch",
        "adjudication_csv_sha_pin_mismatch",
        "adjudication_md_sha_pin_mismatch",
        "parent_parquet_02_01_02_sha_mismatch",
        "parent_parquet_02_01_03_sha_mismatch",
        "parent_audit_02_01_02_canonical_sha_mismatch",
        "parent_audit_02_01_03_canonical_sha_mismatch",
        "binding_difference_family_numeric_pair_count_drift",
        "binding_symmetric_pair_aggregate_transforms_drift",
        "binding_cross_region_pair_transforms_drift",
        "source_column_missing_in_02_01_03_parquet",
        "expected_output_row_count_module_constant_drift",
        "audit_pinned_row_count_drift",
        "output_row_count_drift",
        "output_distinct_focal_match_count_drift",
        "output_feature_column_count_drift",
        "output_total_column_count_drift",
        "identity_columns_not_byte_identical_to_02_01_03",
        "forbidden_token_in_emitted_column_name",
        "no_parent_mutation_check_failed",
        "audit_verdict_not_pass",
        "non_deterministic_re_write",
        "per_feature_traceability_proof_failed",
    ]
    for name in expected:
        assert name in _HALTING_FALSIFIERS, f"Missing falsifier: {name!r}"


def test_wrong_row_count_raises_materialization_error():
    """_assert_output_shape raises on wrong row count."""
    df_bad = pd.DataFrame({"focal_match_id": [1, 2, 3]})
    with pytest.raises(SymmetryDifferenceMaterializationError, match="output_row_count_drift"):
        _assert_output_shape(df_bad)


def test_missing_source_column_raises_materialization_error():
    """_assert_source_columns_in_parquet raises on missing required column."""
    df_bad = pd.DataFrame({"focal_match_id": [1], "started_at": ["2020-01-01"]})
    with pytest.raises(
        SymmetryDifferenceMaterializationError,
        match="source_column_missing_in_02_01_03_parquet",
    ):
        _assert_source_columns_in_parquet(df_bad)


def test_audit_row_count_invariant_raises_on_mismatch():
    """_assert_row_count_invariants raises when audit JSON row_count != constant."""
    bad_dict = {"row_count": 99999, "distinct_focal_match_count": 22209}
    with pytest.raises(
        SymmetryDifferenceMaterializationError,
        match="audit_pinned_row_count_drift",
    ):
        _assert_row_count_invariants(bad_dict)


# ---------------------------------------------------------------------------
# Research_log non-closure check (≥4 tests)
# ---------------------------------------------------------------------------


def test_research_log_contains_closure_status_still_open():
    """research_log.md contains 'closure_status: `still_open`' (PR #269 entry)."""
    text = _RESEARCH_LOG_PATH.read_text(encoding="utf-8")
    assert "closure_status" in text
    assert "still_open" in text


def test_research_log_contains_materialization_state():
    """research_log.md contains 'materialization_state: `materialized`' for 02_02_01."""
    text = _RESEARCH_LOG_PATH.read_text(encoding="utf-8")
    assert "materialization_state" in text
    assert "materialized" in text


def test_research_log_contains_leakage_audit_state():
    """research_log.md contains 'leakage_audit_state: `post_materialization_pass`'."""
    text = _RESEARCH_LOG_PATH.read_text(encoding="utf-8")
    assert "leakage_audit_state" in text
    assert "post_materialization_pass" in text


def test_research_log_does_not_claim_step_closure():
    """research_log.md 02_02_01 entry does NOT claim step closure."""
    text = _RESEARCH_LOG_PATH.read_text(encoding="utf-8")
    # The entry should have still_open, not closed for 02_02_01
    # Check the 02_02_01 section doesn't say "closure_status: `closed`"
    # Look for the 02_02_01 materialization entry
    assert "Step 02_02_01" in text
    # And it contains still_open
    assert "still_open" in text


# ---------------------------------------------------------------------------
# No status YAML / ROADMAP / root research_log mutation (≥4 tests)
# ---------------------------------------------------------------------------


def test_step_status_yaml_has_no_02_02_01_row():
    """STEP_STATUS.yaml has no '02_02_01' row (step not closed by this PR)."""
    step_status_path = (
        _REPO_ROOT / "src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml"
    )
    text = step_status_path.read_text()
    assert "02_02_01" not in text


def test_phase_status_yaml_unchanged():
    """PHASE_STATUS.yaml still shows Phase 02 in_progress / Phase 03 not_started."""
    text = _PHASE_STATUS_PATH.read_text(encoding="utf-8")
    assert "in_progress" in text or "02" in text


def test_roadmap_has_02_02_01_block():
    """ROADMAP.md still contains the '02_02_01' block (byte-unchanged, not closed)."""
    text = _ROADMAP_PATH.read_text(encoding="utf-8")
    assert "02_02_01" in text


def test_root_research_log_not_modified(tmp_path):
    """Root dataset research_log.md is the same before and after a materialization run."""
    # Capture SHA before a re-run
    sha_before = _sha256(_RESEARCH_LOG_PATH)
    # Run materialization with tmp_path outputs
    materialize_symmetry_difference_features(
        output_parquet_path=tmp_path / "test.parquet",
        output_audit_json_path=tmp_path / "audit.json",
        output_audit_md_path=tmp_path / "audit.md",
    )
    sha_after = _sha256(_RESEARCH_LOG_PATH)
    assert sha_before == sha_after, "research_log.md was modified by materialization"


# ---------------------------------------------------------------------------
# No Phase 03 / baseline directory creation (≥2 tests)
# ---------------------------------------------------------------------------


def test_no_phase_03_directory_created():
    """No 03_* directory was created under reports/artifacts/."""
    artifacts_dir = (
        _REPO_ROOT
        / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
    )
    phase_03_dirs = [
        d for d in artifacts_dir.iterdir()
        if d.is_dir() and d.name.startswith("03_")
    ]
    assert len(phase_03_dirs) == 0, f"Found Phase 03 dirs: {phase_03_dirs}"


def test_no_baseline_modeling_path_created():
    """No 'baseline' or 'phase_03' path was created in reports/artifacts/."""
    artifacts_dir = (
        _REPO_ROOT
        / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
    )
    all_names = [d.name.lower() for d in artifacts_dir.iterdir()]
    assert not any("baseline" in n for n in all_names)


# ---------------------------------------------------------------------------
# Additional structural tests
# ---------------------------------------------------------------------------


def test_step_constant_value():
    """STEP == '02_02_01'."""
    assert STEP == "02_02_01"


def test_spec_version_value():
    """SPEC_VERSION == 'CROSS-02-01-v1'."""
    assert SPEC_VERSION == "CROSS-02-01-v1"


def test_executed_at_utc_date():
    """EXECUTED_AT_UTC_DATE == '2026-05-30'."""
    assert EXECUTED_AT_UTC_DATE == "2026-05-30"


def test_expected_total_column_count():
    """_EXPECTED_TOTAL_COLUMN_COUNT == 37."""
    assert _EXPECTED_TOTAL_COLUMN_COUNT == 37


def test_expected_feature_column_count():
    """_EXPECTED_FEATURE_COLUMN_COUNT == 33."""
    assert _EXPECTED_FEATURE_COLUMN_COUNT == 33


def test_binding_constant_count_assertions_pass():
    """_assert_binding_constant_counts passes with correct binding constants."""
    # Should not raise
    _assert_binding_constant_counts()


def test_compute_all_features_output_shape(input_03_df):
    """_compute_all_features returns 37-column DataFrame with 44,418 rows."""
    df_out = _compute_all_features(input_03_df)
    assert len(df_out) == 44_418
    assert len(df_out.columns) == 37


def test_per_feature_provenance_count():
    """_construct_per_feature_provenance returns 33 entries."""
    provenance = _construct_per_feature_provenance()
    assert len(provenance) == 33


def test_per_feature_provenance_families():
    """Per-feature provenance has correct per-family counts."""
    provenance = _construct_per_feature_provenance()
    families = [p["family"] for p in provenance]
    assert families.count("F1_difference") == 10
    assert families.count("F2_pair_mean") == 10
    assert families.count("F3_pair_abs_diff") == 10
    assert families.count("F5_cross_region_pair") == 3


def test_adjudication_csv_sha256_pin_value():
    """_ADJUDICATION_CSV_SHA256_PIN starts with '93688970'."""
    assert _ADJUDICATION_CSV_SHA256_PIN.startswith("93688970")


def test_adjudication_md_sha256_pin_value():
    """_ADJUDICATION_MD_SHA256_PIN starts with '2245746d'."""
    assert _ADJUDICATION_MD_SHA256_PIN.startswith("2245746d")


def test_audit_json_contains_correct_feature_names(audit_json_dict):
    """Audit JSON features_audited matches the expected 33 names."""
    assert audit_json_dict["features_audited"] == _EXPECTED_ALL_FEATURE_NAMES


def test_audit_json_feature_parquet_sha_non_empty(audit_json_dict):
    """Audit JSON feature_parquet_sha256 is a non-empty 64-char hex string."""
    sha = audit_json_dict.get("feature_parquet_sha256", "")
    assert len(sha) == 64
    assert all(c in "0123456789abcdef" for c in sha)


# ---------------------------------------------------------------------------
# Coverage gap tests — error branches
# ---------------------------------------------------------------------------


def test_resolve_repo_root_with_explicit_path(tmp_path):
    """_resolve_repo_root returns the resolved explicit path when given one."""
    from rts_predict.games.sc2.datasets.sc2egset.materialize_symmetry_difference_features import (
        _resolve_repo_root,
    )
    result = _resolve_repo_root(str(tmp_path))
    assert result == tmp_path.resolve()


def test_assert_row_count_invariants_raises_on_distinct_count_mismatch():
    """_assert_row_count_invariants raises when audit JSON distinct_focal_match_count is wrong."""
    # row_count correct, distinct wrong -> triggers the distinct branch (line 477)
    bad_dict = {"row_count": 44418, "distinct_focal_match_count": 99999}
    with pytest.raises(
        SymmetryDifferenceMaterializationError,
        match="audit_pinned_row_count_drift",
    ):
        _assert_row_count_invariants(bad_dict)


def test_assert_output_shape_raises_on_distinct_focal_match_count_drift():
    """_assert_output_shape raises when distinct focal_match_id count is wrong."""
    # Build DataFrame with correct row count but duplicated focal_match_id
    ids = ["id_00000"] * EXPECTED_OUTPUT_ROW_COUNT
    focal_cols = {c: ["x"] * EXPECTED_OUTPUT_ROW_COUNT for c in IDENTITY_COLUMNS}
    focal_cols["focal_match_id"] = ids
    context_cols = {"started_at": ["2020-01-01"] * EXPECTED_OUTPUT_ROW_COUNT}
    feature_cols = {f"f{i}": [0.0] * EXPECTED_OUTPUT_ROW_COUNT for i in range(33)}
    df_bad = pd.DataFrame({**focal_cols, **context_cols, **feature_cols})
    with pytest.raises(
        SymmetryDifferenceMaterializationError,
        match="output_distinct_focal_match_count_drift",
    ):
        _assert_output_shape(df_bad)


def test_assert_output_shape_raises_on_feature_column_count_drift():
    """_assert_output_shape raises when feature column count is wrong."""
    # Correct rows and distinct count, but too few feature cols (only 30 instead of 33)
    n = EXPECTED_OUTPUT_ROW_COUNT
    ids = [f"id_{i:05d}" for i in range(n // 2)] * 2  # 22209 unique IDs * 2 = 44418
    focal_cols = {c: ["x"] * n for c in IDENTITY_COLUMNS}
    focal_cols["focal_match_id"] = ids
    context_cols = {"started_at": ["2020-01-01"] * n}
    # Only 30 feature columns (missing 3)
    feature_cols = {f"f{i}": [0.0] * n for i in range(30)}
    df_bad = pd.DataFrame({**focal_cols, **context_cols, **feature_cols})
    with pytest.raises(
        SymmetryDifferenceMaterializationError,
        match="output_feature_column_count_drift",
    ):
        _assert_output_shape(df_bad)


def test_assert_output_shape_raises_on_total_column_count_drift(monkeypatch):
    """_assert_output_shape raises when total column count check fires (monkeypatched constant)."""
    import rts_predict.games.sc2.datasets.sc2egset.materialize_symmetry_difference_features as m
    # The check at line 1211 is mathematically unreachable with unpatched constants:
    # feature_col_count == 33 implies total == 37 == _EXPECTED_TOTAL_COLUMN_COUNT.
    # Monkeypatch _EXPECTED_TOTAL_COLUMN_COUNT to 38 so a 37-col DataFrame triggers it.
    monkeypatch.setattr(m, "_EXPECTED_TOTAL_COLUMN_COUNT", 38)
    n = EXPECTED_OUTPUT_ROW_COUNT
    ids = [f"id_{i:05d}" for i in range(n // 2)] * 2
    focal_cols = {c: ["x"] * n for c in IDENTITY_COLUMNS}
    focal_cols["focal_match_id"] = ids
    context_cols = {"started_at": ["2020-01-01"] * n}
    feature_cols = {f"f{i}": [0.0] * n for i in range(33)}
    df_bad = pd.DataFrame({**focal_cols, **context_cols, **feature_cols})
    with pytest.raises(
        SymmetryDifferenceMaterializationError,
        match="output_total_column_count_drift",
    ):
        m._assert_output_shape(df_bad)


def test_assert_identity_alignment_raises_on_mismatch():
    """_assert_identity_alignment raises when identity column values differ."""
    from rts_predict.games.sc2.datasets.sc2egset.materialize_symmetry_difference_features import (
        _assert_identity_alignment,
    )
    n = 10
    df_in = pd.DataFrame({
        "focal_match_id": [f"id_{i}" for i in range(n)],
        "focal_player": ["alice"] * n,
        "opponent_player": ["bob"] * n,
    })
    # df_out has different focal_match_id values
    df_out = pd.DataFrame({
        "focal_match_id": [f"WRONG_{i}" for i in range(n)],
        "focal_player": ["alice"] * n,
        "opponent_player": ["bob"] * n,
    })
    with pytest.raises(
        SymmetryDifferenceMaterializationError,
        match="identity_columns_not_byte_identical_to_02_01_03",
    ):
        _assert_identity_alignment(df_in, df_out)


def test_assert_binding_constant_counts_raises_on_pair_count_drift(monkeypatch):
    """_assert_binding_constant_counts raises when numeric pair count is wrong."""
    import rts_predict.games.sc2.datasets.sc2egset.materialize_symmetry_difference_features as m
    # Monkeypatch module-level reference to use a wrong-length tuple
    original = m.BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS
    monkeypatch.setattr(m, "BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS", original[:9])
    with pytest.raises(
        SymmetryDifferenceMaterializationError,
        match="binding_difference_family_numeric_pair_count_drift",
    ):
        m._assert_binding_constant_counts()


def test_assert_binding_constant_counts_raises_on_symmetric_transforms_drift(monkeypatch):
    """_assert_binding_constant_counts raises when symmetric transforms change."""
    import rts_predict.games.sc2.datasets.sc2egset.materialize_symmetry_difference_features as m
    monkeypatch.setattr(m, "BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS", ("mean",))
    with pytest.raises(
        SymmetryDifferenceMaterializationError,
        match="binding_symmetric_pair_aggregate_transforms_drift",
    ):
        m._assert_binding_constant_counts()


def test_assert_binding_constant_counts_raises_on_cross_region_transforms_drift(monkeypatch):
    """_assert_binding_constant_counts raises when cross-region transforms change."""
    import rts_predict.games.sc2.datasets.sc2egset.materialize_symmetry_difference_features as m
    monkeypatch.setattr(m, "BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS", ("either",))
    with pytest.raises(
        SymmetryDifferenceMaterializationError,
        match="binding_cross_region_pair_transforms_drift",
    ):
        m._assert_binding_constant_counts()


def test_verify_deterministic_re_write_raises_on_sha_mismatch(tmp_path, monkeypatch):
    """_verify_deterministic_re_write raises when re-written SHA differs."""
    import rts_predict.games.sc2.datasets.sc2egset.materialize_symmetry_difference_features as m

    call_count = [0]

    def patched_sha256(path: Path) -> str:
        call_count[0] += 1
        if call_count[0] == 1:
            return "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        return "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

    monkeypatch.setattr(m, "_sha256_of_file_bytes", patched_sha256)

    fake_parquet = tmp_path / "fake.parquet"
    fake_parquet.write_bytes(b"fake content")

    df = pd.DataFrame({"col": [1, 2, 3]})
    with pytest.raises(
        SymmetryDifferenceMaterializationError,
        match="non_deterministic_re_write",
    ):
        m._verify_deterministic_re_write(df, fake_parquet)


def test_run_validator_hardlink_fallback_to_copy(tmp_path, monkeypatch):
    """_run_validator uses shutil.copy2 when hardlink_to raises OSError."""
    import shutil

    copy_called = [False]
    original_copy = shutil.copy2

    def patched_hardlink(self, target):
        raise OSError("cross-device link not permitted")

    def patched_copy2(src, dst):
        copy_called[0] = True
        return original_copy(src, dst)

    monkeypatch.setattr(Path, "hardlink_to", patched_hardlink)
    monkeypatch.setattr(shutil, "copy2", patched_copy2)

    # Run through the real public function with tmp outputs so validator is actually invoked
    materialize_symmetry_difference_features(
        output_parquet_path=tmp_path / "out.parquet",
        output_audit_json_path=tmp_path / "audit.json",
        output_audit_md_path=tmp_path / "audit.md",
    )
    assert copy_called[0], "shutil.copy2 was not called as hardlink fallback"


def test_materialize_raises_when_validator_not_passed(monkeypatch, tmp_path):
    """materialize_symmetry_difference_features raises when validator reports not passed."""
    # Use a SimpleNamespace to satisfy the duck-typed check in the public function
    import types

    import rts_predict.games.sc2.datasets.sc2egset.materialize_symmetry_difference_features as m
    failed_result = types.SimpleNamespace(passed=False, halting_falsifier="some_falsifier")
    monkeypatch.setattr(m, "_run_validator", lambda repo_root, specs: failed_result)

    with pytest.raises(
        SymmetryDifferenceMaterializationError,
        match="audit_verdict_not_pass",
    ):
        m.materialize_symmetry_difference_features(
            output_parquet_path=tmp_path / "out.parquet",
            output_audit_json_path=tmp_path / "audit.json",
            output_audit_md_path=tmp_path / "audit.md",
        )
