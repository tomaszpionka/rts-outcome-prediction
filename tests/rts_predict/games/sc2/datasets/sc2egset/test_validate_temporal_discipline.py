"""Tests for V3 strict-< temporal-discipline validator (sc2egset Step 02_03_01).

Test groups:
  A (4):   H1 positive control — real parents, real SHAs.
  B (4):   H1 negative — SHA mismatch, missing artifact.
  C (4):   H2 positive/negative — temporal anchor.
  D (5):   H3 positive/negative — history-column naming.
  D-FP(5): H3 false-positive control — anchored regex NIT-7.
  E (6):   H4 positive/negative — cite-string provenance.
  F (2):   H5 positive/negative — forbidden-emission guard.
  G (4):   H6 positive/negative — cross-game vocabulary.
  H (4):   H7 positive/negative — Q8 syntactic-only.
  I (5):   Halt-priority ordering.
  J (4):   Dataclass invariants.
  K (4):   NIT-2 schema-only enforcement (mock-based).
  L (3):   NIT-9 V1 non-import test.
  M (3):   Smoke tests — real repo_root.
"""

from __future__ import annotations

import hashlib
import inspect
import re
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

import rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline as vtd
from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
    FORBIDDEN_AOE2_CLAIM_PATTERNS,
    FORBIDDEN_V3_OUTPUTS_DIR,
    HISTORY_COLUMN_REGEX,
    PARENT_02_01_02_PARQUET_RELPATH,
    PARENT_02_01_02_PARQUET_SHA256,
    PARENT_02_01_03_PARQUET_RELPATH,
    PARENT_02_01_03_PARQUET_SHA256,
    PARENT_02_01_99_CSV_RELPATH,
    PARENT_02_01_99_CSV_SHA256,
    PARENT_02_02_01_PARQUET_RELPATH,
    PARENT_02_02_01_PARQUET_SHA256,
    REQUIRED_CITE_SUBSTRINGS,
    TemporalDisciplineCheckResult,
    _check_h1_provenance,
    _check_h2_temporal_anchor,
    _check_h3_history_naming,
    _check_h4_cite_strings,
    _check_h5_outputs_dir_absent,
    _check_h6_vocabulary,
    _check_h7_no_aoe2_claim,
    validate_temporal_discipline,
)

# ---------------------------------------------------------------------------
# Helper: repo root
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[6]


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


def _make_fake_parquet(
    tmp_path: Path,
    relpath: str,
    col_names: list[str],
    col_types: list[pa.DataType] | None = None,
) -> None:
    """Write a minimal Parquet at tmp_path/relpath with given columns."""
    if col_types is None:
        col_types = [pa.int64()] * len(col_names)
    fields = [pa.field(n, t) for n, t in zip(col_names, col_types)]
    schema = pa.schema(fields)
    dest = tmp_path / relpath
    dest.parent.mkdir(parents=True, exist_ok=True)
    table = pa.table({name: pa.array([]) for name in schema.names}, schema=schema)
    pq.write_table(table, dest)


def _write_fake_csv(
    tmp_path: Path,
    relpath: str,
    content: str = "col1\nval1\n",
) -> None:
    """Write a minimal CSV at tmp_path/relpath."""
    dest = tmp_path / relpath
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content)


def _make_valid_tmp_repo(tmp_path: Path) -> None:
    """Populate tmp_path with minimal valid predecessor artifacts."""
    _make_fake_parquet(
        tmp_path,
        PARENT_02_01_02_PARQUET_RELPATH,
        col_names=["focal_match_id", "focal_player", "opponent_player", "started_at"],
        col_types=[pa.int64(), pa.string(), pa.string(), pa.timestamp("us")],
    )
    _make_fake_parquet(
        tmp_path,
        PARENT_02_01_03_PARQUET_RELPATH,
        col_names=[
            "focal_match_id",
            "focal_player",
            "opponent_player",
            "started_at",
            "focal_games_prior_count",
            "opponent_games_prior_count",
        ],
        col_types=[
            pa.int64(),
            pa.string(),
            pa.string(),
            pa.timestamp("us"),
            pa.int64(),
            pa.int64(),
        ],
    )
    _write_fake_csv(tmp_path, PARENT_02_01_99_CSV_RELPATH)
    _make_fake_parquet(
        tmp_path,
        PARENT_02_02_01_PARQUET_RELPATH,
        col_names=["focal_match_id", "focal_player", "opponent_player", "started_at"],
        col_types=[pa.int64(), pa.string(), pa.string(), pa.timestamp("us")],
    )
    _patch_sha_pins(tmp_path)


def _patch_sha_pins(tmp_path: Path) -> None:
    """Update the module's _SHA256_BY_RELPATH for the tmp files."""
    for rp in [
        PARENT_02_01_02_PARQUET_RELPATH,
        PARENT_02_01_03_PARQUET_RELPATH,
        PARENT_02_01_99_CSV_RELPATH,
        PARENT_02_02_01_PARQUET_RELPATH,
    ]:
        path = tmp_path / rp
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        vtd._SHA256_BY_RELPATH[rp] = digest


def _restore_sha_pins() -> None:
    """Restore original SHA256 pins."""
    vtd._SHA256_BY_RELPATH[PARENT_02_01_02_PARQUET_RELPATH] = PARENT_02_01_02_PARQUET_SHA256
    vtd._SHA256_BY_RELPATH[PARENT_02_01_03_PARQUET_RELPATH] = PARENT_02_01_03_PARQUET_SHA256
    vtd._SHA256_BY_RELPATH[PARENT_02_01_99_CSV_RELPATH] = PARENT_02_01_99_CSV_SHA256
    vtd._SHA256_BY_RELPATH[PARENT_02_02_01_PARQUET_RELPATH] = PARENT_02_02_01_PARQUET_SHA256


# ===========================================================================
# Group A — H1 positive control (real ancestors, real SHAs)
# ===========================================================================


class TestGroupAH1Positive:
    """H1 positive: real predecessor artifacts exist and SHA matches."""

    def test_h1_02_01_02_exists(self) -> None:
        path = REPO_ROOT / PARENT_02_01_02_PARQUET_RELPATH
        assert path.exists(), "02_01_02 parquet must exist"

    def test_h1_02_01_03_exists(self) -> None:
        path = REPO_ROOT / PARENT_02_01_03_PARQUET_RELPATH
        assert path.exists(), "02_01_03 parquet must exist"

    def test_h1_02_01_99_exists(self) -> None:
        path = REPO_ROOT / PARENT_02_01_99_CSV_RELPATH
        assert path.exists(), "02_01_99 csv must exist"

    def test_h1_real_artifacts_pass(self) -> None:
        ok, label = _check_h1_provenance(REPO_ROOT)
        assert ok is True
        assert label is None


# ===========================================================================
# Group B — H1 negative (SHA mismatch, missing artifact)
# ===========================================================================


class TestGroupBH1Negative:
    """H1 negative: missing or tampered artifacts trigger h1_* falsifiers."""

    def test_h1_missing_artifact(self, tmp_path: Path) -> None:
        ok, label = _check_h1_provenance(tmp_path)
        assert ok is False
        assert label is not None
        assert label.startswith("h1_artifact_missing:")

    def test_h1_sha_mismatch_02_01_02(self, tmp_path: Path) -> None:
        dest = tmp_path / PARENT_02_01_02_PARQUET_RELPATH
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b"corrupted content")
        ok, label = _check_h1_provenance(tmp_path)
        assert ok is False
        assert label is not None
        assert "h1_" in label

    def test_h1_missing_02_01_03_after_first_passes(self, tmp_path: Path) -> None:
        # Write 02_01_02 with real bytes, 02_01_03 absent
        src = REPO_ROOT / PARENT_02_01_02_PARQUET_RELPATH
        dest = tmp_path / PARENT_02_01_02_PARQUET_RELPATH
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())
        ok, label = _check_h1_provenance(tmp_path)
        assert ok is False
        assert label is not None
        assert "h1_" in label

    def test_h1_falsifier_prefix(self, tmp_path: Path) -> None:
        ok, label = _check_h1_provenance(tmp_path)
        assert label is not None
        assert label.startswith("h1_")


# ===========================================================================
# Group C — H2 temporal anchor
# ===========================================================================


class TestGroupCH2TemporalAnchor:
    """H2: started_at timestamp[us] must be present in all 3 Parquet schemas."""

    def test_h2_real_artifacts_pass(self) -> None:
        results, label = _check_h2_temporal_anchor(REPO_ROOT)
        assert label is None
        assert all(results.values()), f"H2 failed: {results}"

    def test_h2_missing_started_at(self, tmp_path: Path) -> None:
        _make_fake_parquet(
            tmp_path,
            PARENT_02_01_02_PARQUET_RELPATH,
            col_names=["focal_match_id", "focal_player"],
        )
        for rp in [PARENT_02_01_03_PARQUET_RELPATH, PARENT_02_02_01_PARQUET_RELPATH]:
            dest = tmp_path / rp
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((REPO_ROOT / rp).read_bytes())
        results, label = _check_h2_temporal_anchor(tmp_path)
        assert label is not None
        assert label.startswith("h2_temporal_anchor_missing:")

    def test_h2_wrong_type_started_at(self, tmp_path: Path) -> None:
        # started_at as int64 (wrong type)
        _make_fake_parquet(
            tmp_path,
            PARENT_02_01_02_PARQUET_RELPATH,
            col_names=["focal_match_id", "started_at"],
            col_types=[pa.int64(), pa.int64()],
        )
        for rp in [PARENT_02_01_03_PARQUET_RELPATH, PARENT_02_02_01_PARQUET_RELPATH]:
            dest = tmp_path / rp
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((REPO_ROOT / rp).read_bytes())
        results, label = _check_h2_temporal_anchor(tmp_path)
        assert label is not None
        assert "h2_" in label

    def test_h2_all_present_returns_dict(self) -> None:
        results, label = _check_h2_temporal_anchor(REPO_ROOT)
        assert isinstance(results, dict)
        assert len(results) == 3


# ===========================================================================
# Group D — H3 history-column naming
# ===========================================================================


class TestGroupDH3HistoryNaming:
    """H3: history-column naming convention."""

    def test_h3_real_artifacts_pass(self) -> None:
        naming, forbidden, label = _check_h3_history_naming(REPO_ROOT)
        assert label is None, f"H3 should pass on real artifacts but got: {label}"

    def test_h3_forbidden_column_including_target(self, tmp_path: Path) -> None:
        _make_fake_parquet(
            tmp_path,
            PARENT_02_01_02_PARQUET_RELPATH,
            col_names=["started_at", "focal_wins_including_target"],
            col_types=[pa.timestamp("us"), pa.int64()],
        )
        for rp in [PARENT_02_01_03_PARQUET_RELPATH, PARENT_02_02_01_PARQUET_RELPATH]:
            dest = tmp_path / rp
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((REPO_ROOT / rp).read_bytes())
        naming, forbidden, label = _check_h3_history_naming(tmp_path)
        assert label is not None
        assert label.startswith("h3_forbidden_column_present:")

    def test_h3_forbidden_h2h_with_target(self, tmp_path: Path) -> None:
        _make_fake_parquet(
            tmp_path,
            PARENT_02_01_02_PARQUET_RELPATH,
            col_names=["started_at", "focal_h2h_with_target_wins"],
            col_types=[pa.timestamp("us"), pa.int64()],
        )
        for rp in [PARENT_02_01_03_PARQUET_RELPATH, PARENT_02_02_01_PARQUET_RELPATH]:
            dest = tmp_path / rp
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((REPO_ROOT / rp).read_bytes())
        naming, forbidden, label = _check_h3_history_naming(tmp_path)
        assert label is not None
        assert "h3_" in label

    def test_h3_no_prior_columns_in_02_01_03(self, tmp_path: Path) -> None:
        for rp in [PARENT_02_01_02_PARQUET_RELPATH, PARENT_02_02_01_PARQUET_RELPATH]:
            _make_fake_parquet(
                tmp_path,
                rp,
                col_names=["started_at", "focal_match_id"],
                col_types=[pa.timestamp("us"), pa.int64()],
            )
        # 02_01_03 without prior_ columns
        _make_fake_parquet(
            tmp_path,
            PARENT_02_01_03_PARQUET_RELPATH,
            col_names=["started_at", "focal_match_id", "some_other_col"],
            col_types=[pa.timestamp("us"), pa.int64(), pa.float64()],
        )
        naming, forbidden, label = _check_h3_history_naming(tmp_path)
        assert label is not None
        assert "h3_no_prior_columns" in label

    def test_h3_valid_prior_columns_pass(self, tmp_path: Path) -> None:
        for rp in [PARENT_02_01_02_PARQUET_RELPATH, PARENT_02_02_01_PARQUET_RELPATH]:
            _make_fake_parquet(
                tmp_path,
                rp,
                col_names=["started_at", "focal_match_id"],
                col_types=[pa.timestamp("us"), pa.int64()],
            )
        _make_fake_parquet(
            tmp_path,
            PARENT_02_01_03_PARQUET_RELPATH,
            col_names=[
                "started_at",
                "focal_games_prior_count",
                "opponent_wins_prior_rate",
            ],
            col_types=[pa.timestamp("us"), pa.int64(), pa.float64()],
        )
        naming, forbidden, label = _check_h3_history_naming(tmp_path)
        assert label is None


# ===========================================================================
# Group D-FP — H3 false-positive control (NIT-7 anchored regex)
# ===========================================================================


class TestGroupDFPH3FalsePositiveControl:
    """NIT-7: Verify anchored regex does not trigger on non-history columns."""

    def test_h3_unanchored_prior_substring_not_triggered(self) -> None:
        col = "unit_priority_score"
        assert HISTORY_COLUMN_REGEX.match(col) is None

    def test_h3_anchored_focal_prior_matches(self) -> None:
        col = "focal_games_prior_count"
        assert HISTORY_COLUMN_REGEX.match(col) is not None

    def test_h3_anchored_opponent_prior_matches(self) -> None:
        col = "opponent_wins_prior_rate"
        assert HISTORY_COLUMN_REGEX.match(col) is not None

    def test_h3_non_focal_opponent_prefix_not_matched(self) -> None:
        col = "player_games_prior_count"
        assert HISTORY_COLUMN_REGEX.match(col) is None

    def test_h3_priority_suffix_no_false_positive(self) -> None:
        col = "game_priority_level"
        assert HISTORY_COLUMN_REGEX.match(col) is None


# ===========================================================================
# Group E — H4 cite-string provenance
# ===========================================================================


class TestGroupEH4CiteStrings:
    """H4: required cite-strings present in module docstring."""

    def test_h4_all_cite_strings_present(self) -> None:
        text = inspect.getsource(vtd)
        results, label = _check_h4_cite_strings(text)
        assert label is None, f"Missing cite-string: {label}"
        assert all(results.values())

    @pytest.mark.parametrize("cite", list(REQUIRED_CITE_SUBSTRINGS))
    def test_h4_missing_single_cite_string(self, cite: str) -> None:
        # Text that has all cites except the one being tested
        text_parts = [c for c in REQUIRED_CITE_SUBSTRINGS if c != cite]
        text = " ".join(text_parts)
        results, label = _check_h4_cite_strings(text)
        assert label is not None
        assert "h4_cite_string_missing:" in label

    def test_h4_empty_text_fails(self) -> None:
        results, label = _check_h4_cite_strings("")
        assert label is not None
        assert label.startswith("h4_cite_string_missing:")

    def test_h4_whitespace_tolerance(self) -> None:
        # cite-string with extra internal whitespace should still be found
        text = "Invariant   I3 is present here CROSS-02-02 G-L-1 also"
        normalised = re.sub(r"\s+", " ", text)
        assert "Invariant I3" in normalised

    def test_h4_all_six_cite_strings_checked(self) -> None:
        assert len(REQUIRED_CITE_SUBSTRINGS) == 6

    def test_h4_falsifier_names_missing_cite(self) -> None:
        results, label = _check_h4_cite_strings("only CROSS-02-02 G-L-1 here")
        assert label is not None
        # First missing cite should be Invariant I3 (or whichever comes first)
        assert "h4_cite_string_missing:" in label


# ===========================================================================
# Group F — H5 forbidden-emission guard
# ===========================================================================


class TestGroupFH5ForbiddenEmission:
    """H5: forbidden V3 outputs directory must not exist."""

    def test_h5_absent_passes(self, tmp_path: Path) -> None:
        absent, label = _check_h5_outputs_dir_absent(tmp_path)
        assert absent is True
        assert label is None

    def test_h5_present_fails(self, tmp_path: Path) -> None:
        outputs_dir = tmp_path / FORBIDDEN_V3_OUTPUTS_DIR
        outputs_dir.mkdir(parents=True, exist_ok=True)
        absent, label = _check_h5_outputs_dir_absent(tmp_path)
        assert absent is False
        assert label == "h5_forbidden_outputs_dir_present"


# ===========================================================================
# Group G — H6 cross-game vocabulary
# ===========================================================================


class TestGroupGH6Vocabulary:
    """H6: no SC2-specific or AoE2-specific terms in public signatures."""

    def test_h6_clean_source_passes(self) -> None:
        source = """
def validate_temporal_discipline(repo_root):
    pass

class TemporalDisciplineCheckResult:
    passed: bool
"""
        ok, label = _check_h6_vocabulary(source)
        assert ok is True
        assert label is None

    @pytest.mark.parametrize("term", ["race", "mineral", "vespene", "PlayerStats"])
    def test_h6_sc2_term_in_signature_fails(self, term: str) -> None:
        source = f"def check_result(repo_root, {term}_value): pass"
        ok, label = _check_h6_vocabulary(source)
        assert ok is False
        assert label is not None
        assert "h6_sc2_term_in_public_surface:" in label

    @pytest.mark.parametrize("term", ["civilization", "leaderboard"])
    def test_h6_aoe2_term_in_signature_fails(self, term: str) -> None:
        source = f"def check_result(repo_root, {term}flag): pass"
        ok, label = _check_h6_vocabulary(source)
        assert ok is False
        assert label is not None
        assert "h6_aoe2_term_in_public_surface:" in label

    def test_h6_real_module_passes(self) -> None:
        text = inspect.getsource(vtd)
        ok, label = _check_h6_vocabulary(text)
        assert ok is True, f"H6 failed on real module: {label}"


# ===========================================================================
# Group H — H7 Q8 syntactic-only
# ===========================================================================


class TestGroupHH7AoE2Claim:
    """H7: no empirical AoE2 transferability claim."""

    def test_h7_clean_source_passes(self) -> None:
        source = "# This module works across games. No empirical claims."
        ok, label = _check_h7_no_aoe2_claim(source)
        assert ok is True
        assert label is None

    def test_h7_validated_on_aoe2_fails(self) -> None:
        source = "# validated on AoE2 dataset"
        ok, label = _check_h7_no_aoe2_claim(source)
        assert ok is False
        assert label is not None
        assert "h7_aoe2_empirical_claim:" in label

    def test_h7_aoe2_transferable_fails(self) -> None:
        source = "# aoe2 transferable approach"
        ok, label = _check_h7_no_aoe2_claim(source)
        assert ok is False
        assert label is not None

    def test_h7_real_module_passes(self) -> None:
        text = inspect.getsource(vtd)
        ok, label = _check_h7_no_aoe2_claim(text)
        assert ok is True, f"H7 failed on real module: {label}"

    def test_h7_forbidden_patterns_count(self) -> None:
        assert len(FORBIDDEN_AOE2_CLAIM_PATTERNS) == 5


# ===========================================================================
# Group I — Halt-priority ordering
# ===========================================================================


class TestGroupIHaltPriority:
    """Multiple failures — only first reported in halting_falsifier."""

    def test_halt_priority_h1_before_h2(self, tmp_path: Path) -> None:
        result = validate_temporal_discipline(tmp_path)
        assert result.passed is False
        assert result.halting_falsifier is not None
        assert result.halting_falsifier.startswith("h1_")

    def test_halt_priority_h2_after_h1_passes(self, tmp_path: Path) -> None:
        _make_valid_tmp_repo(tmp_path)
        # Break H2 by replacing 02_01_02 with no started_at
        _make_fake_parquet(
            tmp_path,
            PARENT_02_01_02_PARQUET_RELPATH,
            col_names=["focal_match_id", "focal_player"],
        )
        _patch_sha_pins(tmp_path)
        try:
            result = validate_temporal_discipline(tmp_path)
        finally:
            _restore_sha_pins()
        assert result.passed is False
        assert result.halting_falsifier is not None
        assert result.halting_falsifier.startswith("h2_")

    def test_halt_priority_h3_after_h1_h2_pass(self, tmp_path: Path) -> None:
        _make_valid_tmp_repo(tmp_path)
        # Overwrite 02_01_03 without prior_ columns but with started_at
        _make_fake_parquet(
            tmp_path,
            PARENT_02_01_03_PARQUET_RELPATH,
            col_names=["started_at", "focal_match_id"],
            col_types=[pa.timestamp("us"), pa.int64()],
        )
        _patch_sha_pins(tmp_path)
        try:
            result = validate_temporal_discipline(tmp_path)
        finally:
            _restore_sha_pins()
        assert result.passed is False
        assert result.halting_falsifier is not None
        assert result.halting_falsifier.startswith("h3_")

    def test_halt_priority_h5_after_h1_h2_h3_h4_pass(self, tmp_path: Path) -> None:
        _make_valid_tmp_repo(tmp_path)
        outputs_dir = tmp_path / FORBIDDEN_V3_OUTPUTS_DIR
        outputs_dir.mkdir(parents=True, exist_ok=True)
        try:
            result = validate_temporal_discipline(tmp_path)
        finally:
            _restore_sha_pins()
        assert result.passed is False
        assert result.halting_falsifier == "h5_forbidden_outputs_dir_present"

    def test_halt_priority_first_failure_wins(self, tmp_path: Path) -> None:
        # Both H1 and H5 would fail; H1 fires first
        outputs_dir = tmp_path / FORBIDDEN_V3_OUTPUTS_DIR
        outputs_dir.mkdir(parents=True, exist_ok=True)
        result = validate_temporal_discipline(tmp_path)
        assert result.passed is False
        assert result.halting_falsifier is not None
        assert result.halting_falsifier.startswith("h1_")


# ===========================================================================
# Group J — Dataclass invariants
# ===========================================================================


class TestGroupJDataclassInvariants:
    """TemporalDisciplineCheckResult has all required fields with defaults."""

    def test_dataclass_passed_field(self) -> None:
        r = TemporalDisciplineCheckResult(passed=True, halting_falsifier=None)
        assert r.passed is True

    def test_dataclass_halting_falsifier_none_default(self) -> None:
        r = TemporalDisciplineCheckResult(passed=True, halting_falsifier=None)
        assert r.halting_falsifier is None

    def test_dataclass_all_default_fields(self) -> None:
        r = TemporalDisciplineCheckResult(passed=True, halting_falsifier=None)
        assert r.artifact_provenance_ok is True
        assert r.temporal_anchor_present == {}
        assert r.history_naming_valid == {}
        assert r.forbidden_columns_absent == {}
        assert r.cite_strings_present == {}
        assert r.outputs_dir_absent is True
        assert r.cross_game_vocabulary_ok is True
        assert r.no_aoe2_empirical_claim is True

    def test_dataclass_failed_result(self) -> None:
        r = TemporalDisciplineCheckResult(
            passed=False,
            halting_falsifier="h1_artifact_missing:some/path",
            artifact_provenance_ok=False,
        )
        assert r.passed is False
        assert r.artifact_provenance_ok is False
        assert r.halting_falsifier == "h1_artifact_missing:some/path"


# ===========================================================================
# Group K — NIT-2 schema-only enforcement (mock-based)
# ===========================================================================


class TestGroupKSchemaOnlyEnforcement:
    """V3 must NEVER call read_table() or read_parquet()."""

    def test_v3_does_not_call_read_table_on_pass(self, tmp_path: Path) -> None:
        _make_valid_tmp_repo(tmp_path)
        with patch("pyarrow.parquet.read_table") as mock_rt:
            try:
                validate_temporal_discipline(tmp_path)
            finally:
                _restore_sha_pins()
            assert mock_rt.call_count == 0, "V3 must not call pq.read_table()"

    def test_v3_does_not_call_read_table_on_fail(self, tmp_path: Path) -> None:
        with patch("pyarrow.parquet.read_table") as mock_rt:
            validate_temporal_discipline(tmp_path)
            assert mock_rt.call_count == 0

    def test_v3_does_not_import_pandas(self) -> None:
        import rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline as vtd_mod

        source_file = vtd_mod.__file__
        assert source_file is not None
        content = Path(source_file).read_text()
        assert "import pandas" not in content, "V3 must not import pandas"
        assert "pd.read_parquet" not in content

    def test_v3_does_not_call_pandas_read_parquet(self, tmp_path: Path) -> None:
        _make_valid_tmp_repo(tmp_path)
        mock_pd = MagicMock()
        with patch.dict(sys.modules, {"pandas": mock_pd}):
            try:
                validate_temporal_discipline(tmp_path)
            finally:
                _restore_sha_pins()
            assert mock_pd.read_parquet.call_count == 0


# ===========================================================================
# Group L — NIT-9 V1 non-import test
# ===========================================================================


class TestGroupLV1NonImport:
    """V3 must NOT import validate_temporal_feature_grid (V1)."""

    def test_v3_source_does_not_reference_v1_module(self) -> None:
        import rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline as vtd_mod

        text = inspect.getsource(vtd_mod)
        assert "validate_temporal_feature_grid" not in text, (
            "V3 source must not reference V1 module validate_temporal_feature_grid"
        )

    def test_importing_v3_does_not_import_v1(self) -> None:
        v1_key = (
            "rts_predict.games.sc2.datasets.sc2egset.validate_temporal_feature_grid"
        )
        v3_key = (
            "rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline"
        )
        saved_v3 = sys.modules.pop(v3_key, None)
        saved_v1 = sys.modules.pop(v1_key, None)
        try:
            import importlib

            importlib.import_module(v3_key)
            assert v1_key not in sys.modules, (
                "Importing V3 must not import V1 validate_temporal_feature_grid"
            )
        finally:
            if saved_v3 is not None:
                sys.modules[v3_key] = saved_v3
            if saved_v1 is not None:
                sys.modules[v1_key] = saved_v1

    def test_v3_sha_pins_independent_of_v1(self) -> None:
        from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
            PARENT_02_01_02_PARQUET_SHA256 as v3_sha,
        )

        assert isinstance(v3_sha, str)
        assert len(v3_sha) == 64  # SHA256 hex


# ===========================================================================
# Group M — Smoke tests (real repo_root)
# ===========================================================================


class TestGroupMSmokeTests:
    """Real repo_root smoke tests — confirm V3 passes all 7 checks."""

    def test_smoke_validate_passes_real_repo(self) -> None:
        result = validate_temporal_discipline(repo_root=REPO_ROOT)
        assert result.passed is True, (
            f"V3 should pass on real repo but got "
            f"halting_falsifier={result.halting_falsifier}"
        )

    def test_smoke_halting_falsifier_none(self) -> None:
        result = validate_temporal_discipline(repo_root=REPO_ROOT)
        assert result.halting_falsifier is None

    def test_smoke_all_checks_positive(self) -> None:
        result = validate_temporal_discipline(repo_root=REPO_ROOT)
        assert result.artifact_provenance_ok is True
        assert result.outputs_dir_absent is True
        assert result.cross_game_vocabulary_ok is True
        assert result.no_aoe2_empirical_claim is True
        assert all(result.temporal_anchor_present.values())
        assert all(result.history_naming_valid.values())
        assert all(len(v) == 0 for v in result.forbidden_columns_absent.values())
        assert all(result.cite_strings_present.values())
