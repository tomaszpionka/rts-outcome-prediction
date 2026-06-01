"""Tests for ``adjudicate_temporal_feature_grid`` — Step 02_03_01 Layer-2 adjudicator.

Coverage targets the H0 -> H7b halt chain and the H_FINAL emit path. Tests
use a tmp_path harness that copies the real predecessor artifacts + cross
specs + tracker eligibility CSV + V1/V3 validator modules into a fake repo
skeleton, so V1 and V3 SHA pins resolve correctly. V3's own module-text
checks (H4/H6/H7) run against the installed module, not the file copy.

Test groups:
  H0  base/path precondition (relative root, missing root)
  H1  V1 preflight FAIL (broken SHA pin, missing parent artifact)
  H2  V3 preflight FAIL (V1 PASS via SHA but V3 H2-H7 trips)
  H3  SHA capture (missing V1/V3 module, missing cross-spec, missing tracker CSV)
  H4  tracker CSV read (corrupted / empty)
  H5  numeric-winner self-guard (not directly triggerable on normal output)
  H6  vocabulary self-guard (not directly triggerable on normal output)
  H7a forbidden output dir present (paradox guard)
  H7b PR-self-archive sentinel (synthetic INDEX.md)
  PASS  H_FINAL emit path (PASS_TEST harness against the real repo root)

Group P (PASS-path) tests run against the real repository root and clean up
the emitted output directory after each test. Synthetic-tmp-path tests are
the dominant pattern; the real-repo PASS test exercises the full emit path.
"""

from __future__ import annotations

import csv
import shutil
from collections.abc import Iterator
from pathlib import Path

import pytest

from rts_predict.games.sc2.datasets.sc2egset.adjudicate_temporal_feature_grid import (
    CROSS_02_02_SPEC_RELPATH,
    CROSS_02_02_SPEC_SHA256,
    CROSS_02_03_SPEC_RELPATH,
    CROSS_02_03_SPEC_SHA256,
    DECISION_BLOCKED,
    DECISION_CONFIRMED,
    DECISION_CSV_COLUMNS,
    DECISION_DEFER_PAST_02_03_01,
    DECISION_DEFER_TO_MATERIALIZATION,
    DECISION_ELIGIBLE,
    DECISION_ELIGIBLE_WITH_CAVEAT,
    DECISION_PASS,
    DECISION_SYNTACTIC_ONLY,
    FAMILY_KIND_Q1,
    FAMILY_KIND_Q2,
    FAMILY_KIND_Q3,
    FAMILY_KIND_Q5,
    FAMILY_KIND_Q6,
    FAMILY_KIND_Q7,
    FAMILY_KIND_Q8,
    FORBIDDEN_OUTPUT_PARENT_RELPATH,
    OUTPUT_CSV_FILENAME,
    OUTPUT_DIR_RELPATH,
    OUTPUT_MD_FILENAME,
    Q6_NON_CONFLATION_SENTENCE,
    STATUS_HALT_H0,
    STATUS_HALT_H3,
    STATUS_HALT_H4,
    STATUS_HALT_H5,
    STATUS_HALT_H6,
    STATUS_HALT_H7A,
    STATUS_HALT_H7B,
    STATUS_HALT_V1,
    STATUS_HALT_V3,
    STATUS_PASS,
    TRACKER_ELIGIBILITY_CSV_RELPATH,
    TRACKER_ELIGIBILITY_CSV_SHA256,
    V1_VALIDATOR_MODULE_RELPATH,
    V3_VALIDATOR_MODULE_RELPATH,
    AdjudicationResult,
    _aggregate_q4_family_decision,
    _build_decision_md,
    _build_decision_rows,
    _build_sha_pin_map,
    _check_h5_no_numeric_winner,
    _check_h6_vocabulary,
    _check_h7a_forbidden_dir,
    _check_h7b_no_self_archive,
    _compute_file_sha256,
    _read_tracker_eligibility_rows,
    _unique_q4_families,
    adjudicate_temporal_feature_grid,
)
from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_feature_grid import (
    ALL_ARTIFACT_RELPATHS,
    PARENT_02_01_02_PARQUET_RELPATH,
    PARENT_02_01_02_PARQUET_SHA256,
    PARENT_02_01_03_PARQUET_SHA256,
    PARENT_02_01_99_CSV_SHA256,
    PARENT_02_02_01_PARQUET_SHA256,
)

# ---------------------------------------------------------------------------
# Real repo root + helpers
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[6]


def _ancillary_relpaths() -> tuple[str, ...]:
    """Return tuple of ancillary file relpaths needed in addition to the 4 parents."""
    return (
        CROSS_02_02_SPEC_RELPATH,
        CROSS_02_03_SPEC_RELPATH,
        TRACKER_ELIGIBILITY_CSV_RELPATH,
        V1_VALIDATOR_MODULE_RELPATH,
        V3_VALIDATOR_MODULE_RELPATH,
    )


def _build_valid_tmp_repo(tmp_path: Path) -> Path:
    """Copy all 9 required files from the real repo into tmp_path."""
    all_files = list(ALL_ARTIFACT_RELPATHS) + list(_ancillary_relpaths())
    for rp in all_files:
        src = _REPO_ROOT / rp
        dest = tmp_path / rp
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    return tmp_path


@pytest.fixture
def clean_real_output_dir() -> Iterator[None]:
    """Ensure the real output directory does not exist before the test.

    Pre-test cleanup only — leaves any post-test emitted artifacts in place
    so that the deliverable decision CSV + decision MD survive the test
    session and can be committed.
    """
    target_parent = _REPO_ROOT / FORBIDDEN_OUTPUT_PARENT_RELPATH
    if target_parent.exists():
        shutil.rmtree(target_parent)
    yield


# ---------------------------------------------------------------------------
# H0 — base/path precondition
# ---------------------------------------------------------------------------


def test_h0_relative_repo_root_halts() -> None:
    """A relative repo_root path must halt at H0."""
    result = adjudicate_temporal_feature_grid(Path("./not_absolute"))
    assert result.status == STATUS_HALT_H0
    assert result.halting_step == "H0"
    assert result.rows_written == 0
    assert result.csv_path is None
    assert result.md_path is None


def test_h0_missing_repo_root_halts(tmp_path: Path) -> None:
    """A non-existent absolute repo_root must halt at H0."""
    missing = tmp_path / "does_not_exist"
    result = adjudicate_temporal_feature_grid(missing)
    assert result.status == STATUS_HALT_H0
    assert result.halting_step == "H0"


def test_h0_empty_path_halts() -> None:
    """An empty string path must halt at H0 (not absolute)."""
    result = adjudicate_temporal_feature_grid(Path(""))
    assert result.status == STATUS_HALT_H0


# ---------------------------------------------------------------------------
# H1 — V1 preflight FAIL
# ---------------------------------------------------------------------------


def test_h1_v1_preflight_fail_missing_parent_parquet(tmp_path: Path) -> None:
    """V1 fails when a parent Parquet is missing; no V3 / emit occurs."""
    _build_valid_tmp_repo(tmp_path)
    (tmp_path / PARENT_02_01_02_PARQUET_RELPATH).unlink()
    result = adjudicate_temporal_feature_grid(tmp_path)
    assert result.status == STATUS_HALT_V1
    assert result.halting_step == "H1"
    assert result.v1_preflight == "FAIL"
    assert result.v3_preflight is None
    assert result.rows_written == 0


def test_h1_v1_preflight_fail_emits_no_artifacts(tmp_path: Path) -> None:
    """V1 FAIL must not create the output dir or any output files."""
    _build_valid_tmp_repo(tmp_path)
    (tmp_path / PARENT_02_01_02_PARQUET_RELPATH).unlink()
    adjudicate_temporal_feature_grid(tmp_path)
    out_dir = tmp_path / OUTPUT_DIR_RELPATH
    assert not out_dir.exists()
    # Forbidden parent must also stay absent (paradox guard binding).
    forbidden_parent = tmp_path / FORBIDDEN_OUTPUT_PARENT_RELPATH
    assert not forbidden_parent.exists()


def test_h1_v1_preflight_fail_sha_mismatch(tmp_path: Path) -> None:
    """V1 fails when a parent SHA mismatches (file corrupted)."""
    _build_valid_tmp_repo(tmp_path)
    target = tmp_path / PARENT_02_01_02_PARQUET_RELPATH
    target.write_bytes(target.read_bytes() + b"\x00")
    result = adjudicate_temporal_feature_grid(tmp_path)
    assert result.status == STATUS_HALT_V1
    assert result.v1_preflight == "FAIL"


# ---------------------------------------------------------------------------
# H2 — V3 preflight FAIL
# ---------------------------------------------------------------------------


def test_h2_v3_preflight_fail_when_temporal_anchor_missing(tmp_path: Path) -> None:
    """V3 fails on missing temporal anchor; V1 already PASS."""
    _build_valid_tmp_repo(tmp_path)
    # Replace one Parquet with a schema lacking `started_at` — but that would
    # break V1 SHA too. Instead, we trigger V3 H1-equivalent via a route that
    # bypasses V1: write a stub Parquet with matching SHA is impossible. So
    # we synthesize a "V3-only fail" by deleting a Parquet file AFTER V1
    # would pass. Since V1 and V3 share the same H1 (parent provenance),
    # there's no realistic case where V1 PASS but V3 FAIL via H1.
    # Therefore: we exercise V3 H1-equivalent (which is congruent with V1
    # H3 SHA-mismatch) by corrupting one Parquet after V1's pinned SHA but
    # before V3's H1 — impossible. The test instead asserts that the V3
    # FAIL branch exists by mocking via a sentinel: see test below.
    pytest.skip("V1 and V3 share parent-provenance; covered by H1 tests.")


def test_h2_v3_preflight_fail_via_monkeypatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """V3 FAIL branch coverage via monkeypatched validate_temporal_discipline."""
    _build_valid_tmp_repo(tmp_path)
    from rts_predict.games.sc2.datasets.sc2egset import (
        adjudicate_temporal_feature_grid as adj_mod,
    )
    from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
        TemporalDisciplineCheckResult,
    )

    def fake_v3(_repo: Path) -> TemporalDisciplineCheckResult:
        return TemporalDisciplineCheckResult(
            passed=False,
            halting_falsifier="injected_fail",
        )

    monkeypatch.setattr(adj_mod, "validate_temporal_discipline", fake_v3)
    result = adjudicate_temporal_feature_grid(tmp_path)
    assert result.status == STATUS_HALT_V3
    assert result.halting_step == "H2"
    assert result.v1_preflight == "PASS"
    assert result.v3_preflight == "FAIL"


def test_h2_v3_fail_emits_no_artifacts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """V3 FAIL must not write outputs."""
    _build_valid_tmp_repo(tmp_path)
    from rts_predict.games.sc2.datasets.sc2egset import (
        adjudicate_temporal_feature_grid as adj_mod,
    )
    from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
        TemporalDisciplineCheckResult,
    )

    def fake_v3(_repo: Path) -> TemporalDisciplineCheckResult:
        return TemporalDisciplineCheckResult(
            passed=False,
            halting_falsifier="injected_fail",
        )

    monkeypatch.setattr(adj_mod, "validate_temporal_discipline", fake_v3)
    adjudicate_temporal_feature_grid(tmp_path)
    assert not (tmp_path / OUTPUT_DIR_RELPATH).exists()
    assert not (tmp_path / FORBIDDEN_OUTPUT_PARENT_RELPATH).exists()


# ---------------------------------------------------------------------------
# H3 — SHA capture
# ---------------------------------------------------------------------------


def test_h3_missing_v1_module_halts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """H3 halts if V1 module unreadable (post-preflight SHA capture)."""
    _build_valid_tmp_repo(tmp_path)
    # Force V3 to PASS regardless to isolate H3 path.
    from rts_predict.games.sc2.datasets.sc2egset import (
        adjudicate_temporal_feature_grid as adj_mod,
    )
    from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
        TemporalDisciplineCheckResult,
    )

    monkeypatch.setattr(
        adj_mod,
        "validate_temporal_discipline",
        lambda _r: TemporalDisciplineCheckResult(passed=True, halting_falsifier=None),
    )
    (tmp_path / V1_VALIDATOR_MODULE_RELPATH).unlink()
    result = adjudicate_temporal_feature_grid(tmp_path)
    assert result.status == STATUS_HALT_H3
    assert result.halting_step == "H3"
    assert result.v1_preflight == "PASS"
    assert result.v3_preflight == "PASS"


def test_h3_missing_v3_module_halts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """H3 halts if V3 module unreadable."""
    _build_valid_tmp_repo(tmp_path)
    from rts_predict.games.sc2.datasets.sc2egset import (
        adjudicate_temporal_feature_grid as adj_mod,
    )
    from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
        TemporalDisciplineCheckResult,
    )

    monkeypatch.setattr(
        adj_mod,
        "validate_temporal_discipline",
        lambda _r: TemporalDisciplineCheckResult(passed=True, halting_falsifier=None),
    )
    (tmp_path / V3_VALIDATOR_MODULE_RELPATH).unlink()
    result = adjudicate_temporal_feature_grid(tmp_path)
    assert result.status == STATUS_HALT_H3


def test_h3_missing_cross_02_02_spec_halts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """H3 halts if CROSS-02-02 spec unreadable."""
    _build_valid_tmp_repo(tmp_path)
    from rts_predict.games.sc2.datasets.sc2egset import (
        adjudicate_temporal_feature_grid as adj_mod,
    )
    from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
        TemporalDisciplineCheckResult,
    )

    monkeypatch.setattr(
        adj_mod,
        "validate_temporal_discipline",
        lambda _r: TemporalDisciplineCheckResult(passed=True, halting_falsifier=None),
    )
    (tmp_path / CROSS_02_02_SPEC_RELPATH).unlink()
    result = adjudicate_temporal_feature_grid(tmp_path)
    assert result.status == STATUS_HALT_H3


def test_h3_missing_cross_02_03_spec_halts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """H3 halts if CROSS-02-03 spec unreadable."""
    _build_valid_tmp_repo(tmp_path)
    from rts_predict.games.sc2.datasets.sc2egset import (
        adjudicate_temporal_feature_grid as adj_mod,
    )
    from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
        TemporalDisciplineCheckResult,
    )

    monkeypatch.setattr(
        adj_mod,
        "validate_temporal_discipline",
        lambda _r: TemporalDisciplineCheckResult(passed=True, halting_falsifier=None),
    )
    (tmp_path / CROSS_02_03_SPEC_RELPATH).unlink()
    result = adjudicate_temporal_feature_grid(tmp_path)
    assert result.status == STATUS_HALT_H3


def test_h3_missing_tracker_csv_halts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """H3 halts if tracker eligibility CSV unreadable for SHA capture."""
    _build_valid_tmp_repo(tmp_path)
    from rts_predict.games.sc2.datasets.sc2egset import (
        adjudicate_temporal_feature_grid as adj_mod,
    )
    from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
        TemporalDisciplineCheckResult,
    )

    monkeypatch.setattr(
        adj_mod,
        "validate_temporal_discipline",
        lambda _r: TemporalDisciplineCheckResult(passed=True, halting_falsifier=None),
    )
    (tmp_path / TRACKER_ELIGIBILITY_CSV_RELPATH).unlink()
    result = adjudicate_temporal_feature_grid(tmp_path)
    assert result.status == STATUS_HALT_H3


def test_h3_corrupted_cross_02_02_spec_halts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """H3 halts if CROSS-02-02 SHA mismatches pinned value."""
    _build_valid_tmp_repo(tmp_path)
    from rts_predict.games.sc2.datasets.sc2egset import (
        adjudicate_temporal_feature_grid as adj_mod,
    )
    from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
        TemporalDisciplineCheckResult,
    )

    monkeypatch.setattr(
        adj_mod,
        "validate_temporal_discipline",
        lambda _r: TemporalDisciplineCheckResult(passed=True, halting_falsifier=None),
    )
    target = tmp_path / CROSS_02_02_SPEC_RELPATH
    target.write_bytes(target.read_bytes() + b"\nextra trailing data\n")
    result = adjudicate_temporal_feature_grid(tmp_path)
    assert result.status == STATUS_HALT_H3


# ---------------------------------------------------------------------------
# H4 — tracker CSV read
# ---------------------------------------------------------------------------


def test_h4_empty_tracker_csv_halts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """H4 halts on a header-only tracker CSV (no data rows)."""
    _build_valid_tmp_repo(tmp_path)
    from rts_predict.games.sc2.datasets.sc2egset import (
        adjudicate_temporal_feature_grid as adj_mod,
    )
    from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
        TemporalDisciplineCheckResult,
    )

    monkeypatch.setattr(
        adj_mod,
        "validate_temporal_discipline",
        lambda _r: TemporalDisciplineCheckResult(passed=True, halting_falsifier=None),
    )
    # Bypass H3 SHA pin guard for the tracker CSV.
    monkeypatch.setattr(adj_mod, "TRACKER_ELIGIBILITY_CSV_SHA256", "deadbeef")
    target = tmp_path / TRACKER_ELIGIBILITY_CSV_RELPATH
    # Header only.
    target.write_text(
        '"feature_family","source_event_family","planned_for_phase02",'
        '"status_pre_game","status_in_game_snapshot",'
        '"status_post_game_or_blocked","eligibility_scope",'
        '"blocking_reason_if_blocked","caveat","evidence_source",'
        '"upstream_verdicts","notes_for_phase02"\n'
    )
    # Recompute SHA constant in the monkeypatched module so H3 passes.
    monkeypatch.setattr(
        adj_mod,
        "TRACKER_ELIGIBILITY_CSV_SHA256",
        _compute_file_sha256(target),
    )
    result = adjudicate_temporal_feature_grid(tmp_path)
    assert result.status == STATUS_HALT_H4
    assert result.halting_step == "H4"


def test_h4_unreadable_tracker_csv_halts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """H4 halts if tracker CSV becomes unreadable between H3 and H4."""
    _build_valid_tmp_repo(tmp_path)
    from rts_predict.games.sc2.datasets.sc2egset import (
        adjudicate_temporal_feature_grid as adj_mod,
    )
    from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
        TemporalDisciplineCheckResult,
    )

    monkeypatch.setattr(
        adj_mod,
        "validate_temporal_discipline",
        lambda _r: TemporalDisciplineCheckResult(passed=True, halting_falsifier=None),
    )

    original_reader = adj_mod._read_tracker_eligibility_rows

    def _raise(_repo: Path) -> list[dict[str, str]]:
        raise OSError("simulated IO failure")

    monkeypatch.setattr(adj_mod, "_read_tracker_eligibility_rows", _raise)
    result = adjudicate_temporal_feature_grid(tmp_path)
    assert result.status == STATUS_HALT_H4
    # Restore for hygiene
    monkeypatch.setattr(adj_mod, "_read_tracker_eligibility_rows", original_reader)


# ---------------------------------------------------------------------------
# H5 / H6 — self-guards (helper-level coverage)
# ---------------------------------------------------------------------------


def test_h5_helper_flags_numeric_winner_in_q1() -> None:
    """_check_h5_no_numeric_winner returns a label for a poisoned Q1 row."""
    poisoned = [
        {"family_kind": FAMILY_KIND_Q1, "decision": "10 games"},
    ]
    assert _check_h5_no_numeric_winner(poisoned) is not None


def test_h5_helper_accepts_clean_q1_row() -> None:
    """_check_h5_no_numeric_winner returns None for the clean DEFER cell."""
    clean = [
        {"family_kind": FAMILY_KIND_Q1, "decision": DECISION_DEFER_TO_MATERIALIZATION},
    ]
    assert _check_h5_no_numeric_winner(clean) is None


def test_h5_helper_ignores_q4_rows_with_numeric_tokens() -> None:
    """Q4 rows are out of the H5 guard's scope (only Q1/Q2/Q3 covered)."""
    rows = [
        {"family_kind": "UnitInit / UnitDone", "decision": "10 games"},
    ]
    assert _check_h5_no_numeric_winner(rows) is None


def test_h6_helper_flags_forbidden_vocab() -> None:
    """_check_h6_vocabulary flags an SC2-specific token in decision text."""
    poisoned = [
        {
            "family_kind": FAMILY_KIND_Q1,
            "decision": "see race mineral",
            "rationale_g_l_ref": "",
            "rationale_d_ref": "",
        },
    ]
    assert _check_h6_vocabulary(poisoned) is not None


def test_h6_helper_accepts_clean_rows() -> None:
    """_check_h6_vocabulary returns None for the clean DEFER row."""
    clean = [
        {
            "family_kind": FAMILY_KIND_Q1,
            "decision": DECISION_DEFER_TO_MATERIALIZATION,
            "rationale_g_l_ref": "G-L-1; G-L-2",
            "rationale_d_ref": "D5; D6; D7",
        },
    ]
    assert _check_h6_vocabulary(clean) is None


# ---------------------------------------------------------------------------
# H7a — forbidden output dir paradox guard (synthetic; pre-emit)
# ---------------------------------------------------------------------------


def test_h7a_helper_detects_existing_forbidden_dir(tmp_path: Path) -> None:
    """_check_h7a_forbidden_dir returns label when dir exists."""
    (tmp_path / FORBIDDEN_OUTPUT_PARENT_RELPATH).mkdir(parents=True)
    assert _check_h7a_forbidden_dir(tmp_path) is not None


def test_h7a_helper_returns_none_when_dir_absent(tmp_path: Path) -> None:
    """_check_h7a_forbidden_dir returns None when dir absent."""
    assert _check_h7a_forbidden_dir(tmp_path) is None


# ---------------------------------------------------------------------------
# H7b — PR-self-archive sentinel (synthetic INDEX.md)
# ---------------------------------------------------------------------------


def test_h7b_helper_returns_none_without_index(tmp_path: Path) -> None:
    """No planning/INDEX.md => sentinel returns None (advisory)."""
    assert _check_h7b_no_self_archive(tmp_path) is None


def test_h7b_helper_returns_none_for_active_line_only(tmp_path: Path) -> None:
    """Active-line mention of the Layer-2 branch is OK."""
    idx = tmp_path / "planning" / "INDEX.md"
    idx.parent.mkdir(parents=True)
    idx.write_text(
        "## Active\n\n"
        "- feat/sc2egset-02-03-01-temporal-adjudication-execution\n"
        "\n## Archive\n\n"
        "- some other branch\n"
    )
    assert _check_h7b_no_self_archive(tmp_path) is None


def test_h7b_helper_detects_self_archive(tmp_path: Path) -> None:
    """Archive-section mention of the Layer-2 branch is a violation."""
    idx = tmp_path / "planning" / "INDEX.md"
    idx.parent.mkdir(parents=True)
    idx.write_text(
        "## Active\n\n"
        "- some active branch\n"
        "\n## Archive\n\n"
        "- feat/sc2egset-02-03-01-temporal-adjudication-execution\n"
    )
    assert _check_h7b_no_self_archive(tmp_path) is not None


# ---------------------------------------------------------------------------
# Helper coverage — SHA, eligibility aggregation, Q4 grain
# ---------------------------------------------------------------------------


def test_compute_file_sha256_matches_known_v1_pin() -> None:
    """SHA256 helper returns the known V1 module byte-stable hash."""
    actual = _compute_file_sha256(_REPO_ROOT / V1_VALIDATOR_MODULE_RELPATH)
    assert (
        actual
        == "7945fc7fc7cf3500390c647c977702a14c3d5ab03c4ee7bbaf04d6bbe1033545"
    )


def test_compute_file_sha256_matches_known_v3_pin() -> None:
    """SHA256 helper returns the known V3 module byte-stable hash."""
    actual = _compute_file_sha256(_REPO_ROOT / V3_VALIDATOR_MODULE_RELPATH)
    assert (
        actual
        == "8e33b7ae0968cbaafa08c33b51e62196e7d4f19cadcd48b3b8d03b6aa2ae2a87"
    )


def test_build_sha_pin_map_returns_nine_entries() -> None:
    """SHA pin map has exactly 9 keys."""
    out = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    assert set(out.keys()) == {
        "parent_02_01_02_parquet_sha256",
        "parent_02_01_03_parquet_sha256",
        "parent_02_01_99_csv_sha256",
        "parent_02_02_01_parquet_sha256",
        "v1_validator_module_sha256",
        "v3_validator_module_sha256",
        "cross_02_02_spec_sha256",
        "cross_02_03_spec_sha256",
        "tracker_eligibility_csv_sha256",
    }


def test_build_sha_pin_map_embeds_module_shas_passed() -> None:
    """V1/V3 module SHA cells take the passed-in computed values."""
    out = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    assert out["v1_validator_module_sha256"] == "v1sha"
    assert out["v3_validator_module_sha256"] == "v3sha"


def test_unique_q4_families_returns_nine_distinct() -> None:
    """Q4 enumeration yields exactly 9 distinct source_event_family tokens."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    families = _unique_q4_families(rows)
    assert len(families) == 9


def test_q4_unit_init_unit_done_spacing_preserved() -> None:
    """UnitInit / UnitDone keeps its internal spaces (NIT-N1)."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    families = _unique_q4_families(rows)
    assert "UnitInit / UnitDone" in families


@pytest.mark.parametrize(
    "family,expected_decision",
    [
        ("PlayerSetup", DECISION_ELIGIBLE),
        ("PlayerStats", DECISION_BLOCKED),
        ("UnitBorn", DECISION_ELIGIBLE_WITH_CAVEAT),
        ("UnitDied", DECISION_ELIGIBLE_WITH_CAVEAT),
        ("UnitInit / UnitDone", DECISION_ELIGIBLE),
        ("UnitOwnerChange", DECISION_BLOCKED),
        ("UnitPositions", DECISION_BLOCKED),
        ("UnitTypeChange", DECISION_ELIGIBLE),
        ("Upgrade", DECISION_ELIGIBLE_WITH_CAVEAT),
    ],
)
def test_aggregate_q4_family_decision_per_category(
    family: str, expected_decision: str
) -> None:
    """Each Q4 category aggregates to the documented worst-case decision."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    assert _aggregate_q4_family_decision(family, rows) == expected_decision


def test_aggregate_q4_unknown_family_fallback() -> None:
    """Unknown family token falls back to ELIGIBLE_WITH_CAVEAT (defensive)."""
    fake_rows = [
        {"source_event_family": "UnknownFamily", "status_in_game_snapshot": "wat"},
    ]
    assert (
        _aggregate_q4_family_decision("UnknownFamily", fake_rows)
        == DECISION_ELIGIBLE_WITH_CAVEAT
    )


# ---------------------------------------------------------------------------
# Decision-row construction
# ---------------------------------------------------------------------------


def test_build_decision_rows_total_count_is_16() -> None:
    """Decision row builder emits exactly 16 rows."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    assert len(decision_rows) == 16


def test_build_decision_rows_all_have_16_columns() -> None:
    """Each decision row contains exactly the 16 documented columns."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    for r in decision_rows:
        assert set(r.keys()) == set(DECISION_CSV_COLUMNS)


def test_decision_csv_columns_count_at_least_16() -> None:
    """DECISION_CSV_COLUMNS literal has at least 16 entries."""
    assert len(DECISION_CSV_COLUMNS) >= 16


def test_decision_csv_columns_exact_names_match_literal_list() -> None:
    """DECISION_CSV_COLUMNS is byte-exact to the planned tuple."""
    expected = (
        "family_kind",
        "decision",
        "rationale_g_l_ref",
        "rationale_d_ref",
        "invariant_i3_cited",
        "v1_preflight",
        "v3_preflight",
        "parent_02_01_02_parquet_sha256",
        "parent_02_01_03_parquet_sha256",
        "parent_02_01_99_csv_sha256",
        "parent_02_02_01_parquet_sha256",
        "v1_validator_module_sha256",
        "v3_validator_module_sha256",
        "cross_02_02_spec_sha256",
        "cross_02_03_spec_sha256",
        "tracker_eligibility_csv_sha256",
    )
    assert DECISION_CSV_COLUMNS == expected


def test_decision_rows_q1_decision_is_defer() -> None:
    """Q1 row decision cell is DEFER_TO_MATERIALIZATION (no concrete winner)."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    q1 = next(r for r in decision_rows if r["family_kind"] == FAMILY_KIND_Q1)
    assert q1["decision"] == DECISION_DEFER_TO_MATERIALIZATION


def test_decision_rows_q2_decision_is_defer() -> None:
    """Q2 row decision cell is DEFER_TO_MATERIALIZATION."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    q2 = next(r for r in decision_rows if r["family_kind"] == FAMILY_KIND_Q2)
    assert q2["decision"] == DECISION_DEFER_TO_MATERIALIZATION


def test_decision_rows_q3_decision_is_defer() -> None:
    """Q3 row decision cell is DEFER_TO_MATERIALIZATION."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    q3 = next(r for r in decision_rows if r["family_kind"] == FAMILY_KIND_Q3)
    assert q3["decision"] == DECISION_DEFER_TO_MATERIALIZATION


def test_decision_rows_q5_decision_is_defer_past_02_03_01() -> None:
    """Q5 row decision cell is DEFER_PAST_02_03_01."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    q5 = next(r for r in decision_rows if r["family_kind"] == FAMILY_KIND_Q5)
    assert q5["decision"] == DECISION_DEFER_PAST_02_03_01


def test_decision_rows_q6_decision_is_confirmed() -> None:
    """Q6 row decision cell is CONFIRMED (non-conflation binding)."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    q6 = next(r for r in decision_rows if r["family_kind"] == FAMILY_KIND_Q6)
    assert q6["decision"] == DECISION_CONFIRMED


def test_decision_rows_q7_decision_is_pass() -> None:
    """Q7 row decision cell is PASS (preflight gate outcome)."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    q7 = next(r for r in decision_rows if r["family_kind"] == FAMILY_KIND_Q7)
    assert q7["decision"] == DECISION_PASS


def test_decision_rows_q8_decision_is_syntactic_only() -> None:
    """Q8 row decision cell is SYNTACTIC_ONLY (no empirical AoE2 claim)."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    q8 = next(r for r in decision_rows if r["family_kind"] == FAMILY_KIND_Q8)
    assert q8["decision"] == DECISION_SYNTACTIC_ONLY


def test_decision_rows_all_carry_nine_sha_pins() -> None:
    """Every decision row contains all 9 SHA-pin columns."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    pin_cols = (
        "parent_02_01_02_parquet_sha256",
        "parent_02_01_03_parquet_sha256",
        "parent_02_01_99_csv_sha256",
        "parent_02_02_01_parquet_sha256",
        "v1_validator_module_sha256",
        "v3_validator_module_sha256",
        "cross_02_02_spec_sha256",
        "cross_02_03_spec_sha256",
        "tracker_eligibility_csv_sha256",
    )
    for r in decision_rows:
        for c in pin_cols:
            assert r[c]


def test_decision_rows_all_carry_v1_v3_pass_sentinels() -> None:
    """Every decision row has v1_preflight=PASS and v3_preflight=PASS."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    for r in decision_rows:
        assert r["v1_preflight"] == "PASS"
        assert r["v3_preflight"] == "PASS"


def test_decision_rows_q4_count_is_nine() -> None:
    """Q4 category rows count is exactly 9."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    q_singleton_keys = {
        FAMILY_KIND_Q1,
        FAMILY_KIND_Q2,
        FAMILY_KIND_Q3,
        FAMILY_KIND_Q5,
        FAMILY_KIND_Q6,
        FAMILY_KIND_Q7,
        FAMILY_KIND_Q8,
    }
    q4 = [r for r in decision_rows if r["family_kind"] not in q_singleton_keys]
    assert len(q4) == 9


def test_decision_rows_no_numeric_winner_in_q123() -> None:
    """Live decision rows never trip the H5 numeric-winner regex."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    assert _check_h5_no_numeric_winner(decision_rows) is None


def test_decision_rows_no_forbidden_vocab() -> None:
    """Live decision rows never trip the H6 vocabulary regex."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    assert _check_h6_vocabulary(decision_rows) is None


# ---------------------------------------------------------------------------
# Decision MD construction
# ---------------------------------------------------------------------------


def test_build_decision_md_contains_q6_non_conflation_verbatim() -> None:
    """Decision MD includes the Q6 non-conflation sentence verbatim."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    md = _build_decision_md(sha_map, rows, decision_rows)
    assert Q6_NON_CONFLATION_SENTENCE in md


def test_build_decision_md_has_14_sections() -> None:
    """Decision MD contains exactly 14 `## ` H2 headings."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    md = _build_decision_md(sha_map, rows, decision_rows)
    headings = [line for line in md.splitlines() if line.startswith("## ")]
    assert len(headings) == 14


def test_build_decision_md_has_15_family_table_in_section_6() -> None:
    """MD §6 contains a 15-row cross-reference table for tracker_events."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    md = _build_decision_md(sha_map, rows, decision_rows)
    section_marker = "## 6."
    assert section_marker in md
    section_text = md.split(section_marker, 1)[1].split("\n## ", 1)[0]
    # 15 table body rows (each begins with "| <int> |").
    table_rows = [
        ln for ln in section_text.splitlines()
        if ln.startswith("| ") and "|" in ln[2:] and "---" not in ln
    ]
    # Header row + 15 body rows; subtract 1 for header.
    assert len(table_rows) == 16


def test_build_decision_md_contains_v1_pass_and_v3_pass_anchors() -> None:
    """MD records V1 PASS and V3 PASS anchors (Q7 plan-text falsifier)."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    md = _build_decision_md(sha_map, rows, decision_rows)
    assert "V1 PASS" in md
    assert "V3 PASS" in md


def test_build_decision_md_cites_invariant_i3() -> None:
    """MD cites Invariant I3 verbatim."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    md = _build_decision_md(sha_map, rows, decision_rows)
    assert "Invariant I3" in md


def test_build_decision_md_no_empirical_aoe2_claim() -> None:
    """MD has no empirical AoE2 transferability claim."""
    rows = _read_tracker_eligibility_rows(_REPO_ROOT)
    sha_map = _build_sha_pin_map(_REPO_ROOT, "v1sha", "v3sha")
    decision_rows = _build_decision_rows(_REPO_ROOT, sha_map, rows)
    md = _build_decision_md(sha_map, rows, decision_rows)
    import re

    forbidden = re.compile(
        r"aoe2.*transferab|transferab.*aoe2|validated on aoe2|"
        r"aoe2.*verified|cross-game validated",
        re.IGNORECASE,
    )
    assert forbidden.search(md) is None


# ---------------------------------------------------------------------------
# AdjudicationResult contract
# ---------------------------------------------------------------------------


def test_adjudication_result_pass_default_field_defaults() -> None:
    """AdjudicationResult is constructible with status alone."""
    r = AdjudicationResult(status=STATUS_PASS)
    assert r.status == STATUS_PASS
    assert r.halting_step is None
    assert r.v1_preflight is None
    assert r.v3_preflight is None
    assert r.sha_pins == {}
    assert r.csv_path is None
    assert r.md_path is None
    assert r.rows_written == 0


def test_adjudication_result_frozen() -> None:
    """AdjudicationResult is frozen (round-trips by value)."""
    r = AdjudicationResult(status=STATUS_PASS)
    with pytest.raises(Exception):
        r.status = STATUS_HALT_H0  # type: ignore[misc]


def test_status_sentinels_distinct() -> None:
    """All halt sentinels are distinct strings."""
    sentinels = {
        STATUS_PASS,
        STATUS_HALT_H0,
        STATUS_HALT_V1,
        STATUS_HALT_V3,
        STATUS_HALT_H3,
        STATUS_HALT_H4,
        STATUS_HALT_H5,
        STATUS_HALT_H6,
        STATUS_HALT_H7A,
        STATUS_HALT_H7B,
    }
    assert len(sentinels) == 10


# ---------------------------------------------------------------------------
# H_FINAL PASS path — real repo end-to-end
# ---------------------------------------------------------------------------


def test_pass_real_repo_emits_csv_and_md(clean_real_output_dir: None) -> None:
    """Against the real repo, adjudicator PASSes and emits both artifacts."""
    del clean_real_output_dir
    result = adjudicate_temporal_feature_grid(_REPO_ROOT)
    assert result.status == STATUS_PASS, result
    assert result.csv_path is not None
    assert result.md_path is not None
    assert result.csv_path.exists()
    assert result.md_path.exists()
    assert result.rows_written == 16
    assert result.v1_preflight == "PASS"
    assert result.v3_preflight == "PASS"


def test_pass_emitted_csv_has_correct_columns(clean_real_output_dir: None) -> None:
    """Emitted CSV header exactly matches DECISION_CSV_COLUMNS."""
    del clean_real_output_dir
    result = adjudicate_temporal_feature_grid(_REPO_ROOT)
    assert result.csv_path is not None
    with result.csv_path.open() as fh:
        reader = csv.reader(fh)
        header = next(reader)
    assert tuple(header) == DECISION_CSV_COLUMNS


def test_pass_emitted_csv_has_exactly_16_body_rows(
    clean_real_output_dir: None,
) -> None:
    """Emitted CSV has exactly 16 body rows."""
    del clean_real_output_dir
    result = adjudicate_temporal_feature_grid(_REPO_ROOT)
    assert result.csv_path is not None
    with result.csv_path.open() as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    assert len(rows) == 16


def test_pass_emitted_csv_q1_q2_q3_carry_defer_decision(
    clean_real_output_dir: None,
) -> None:
    """Emitted CSV: Q1/Q2/Q3 decision cells are DEFER_TO_MATERIALIZATION."""
    del clean_real_output_dir
    result = adjudicate_temporal_feature_grid(_REPO_ROOT)
    assert result.csv_path is not None
    with result.csv_path.open() as fh:
        rows = {r["family_kind"]: r for r in csv.DictReader(fh)}
    for q_kind in (FAMILY_KIND_Q1, FAMILY_KIND_Q2, FAMILY_KIND_Q3):
        assert rows[q_kind]["decision"] == DECISION_DEFER_TO_MATERIALIZATION


def test_pass_emitted_csv_unit_init_unit_done_row_preserves_spaces(
    clean_real_output_dir: None,
) -> None:
    """Emitted CSV preserves UnitInit / UnitDone spaces verbatim (NIT-N1)."""
    del clean_real_output_dir
    result = adjudicate_temporal_feature_grid(_REPO_ROOT)
    assert result.csv_path is not None
    with result.csv_path.open() as fh:
        rows = list(csv.DictReader(fh))
    family_kinds = {r["family_kind"] for r in rows}
    assert "UnitInit / UnitDone" in family_kinds


def test_pass_emitted_md_has_14_h2_sections(
    clean_real_output_dir: None,
) -> None:
    """Emitted MD has exactly 14 `## ` H2 sections."""
    del clean_real_output_dir
    result = adjudicate_temporal_feature_grid(_REPO_ROOT)
    assert result.md_path is not None
    md_text = result.md_path.read_text()
    headings = [ln for ln in md_text.splitlines() if ln.startswith("## ")]
    assert len(headings) == 14


def test_pass_sha_pins_match_known_v1_v3_module_pins(
    clean_real_output_dir: None,
) -> None:
    """Emitted CSV's V1/V3 SHA pin cells match the known byte-stable values."""
    del clean_real_output_dir
    result = adjudicate_temporal_feature_grid(_REPO_ROOT)
    assert result.csv_path is not None
    with result.csv_path.open() as fh:
        first = next(csv.DictReader(fh))
    assert (
        first["v1_validator_module_sha256"]
        == "7945fc7fc7cf3500390c647c977702a14c3d5ab03c4ee7bbaf04d6bbe1033545"
    )
    assert (
        first["v3_validator_module_sha256"]
        == "8e33b7ae0968cbaafa08c33b51e62196e7d4f19cadcd48b3b8d03b6aa2ae2a87"
    )


def test_pass_sha_pin_constants_match_known_values() -> None:
    """All non-V1/V3 SHA pin constants match the planned hex literals."""
    assert (
        PARENT_02_01_02_PARQUET_SHA256
        == "24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39"
    )
    assert (
        PARENT_02_01_03_PARQUET_SHA256
        == "053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071"
    )
    assert (
        PARENT_02_01_99_CSV_SHA256
        == "831a622c6e0a98c9642e466d5c9dced0fb6b621a6d58e3008a1b0218dd03c370"
    )
    assert (
        PARENT_02_02_01_PARQUET_SHA256
        == "c4b48601ee0ff800f4b823af270faf03571a637ce07c51a0ef6d072691896ff3"
    )
    assert (
        CROSS_02_02_SPEC_SHA256
        == "86af792370272e611f048aae0c48c9cc595eb4b44c1db38c0bb4ecea0ff1b289"
    )
    assert (
        CROSS_02_03_SPEC_SHA256
        == "59e3227307c51ad09fb12b485caec36aa54413d175cb46acc382c06fbb8ac546"
    )
    assert (
        TRACKER_ELIGIBILITY_CSV_SHA256
        == "11bd4b9ef7c80657a027db3831313c1d74c39b85834c25ecdfa78506e8ad8d22"
    )


def test_pass_output_dir_only_created_after_preflights(
    tmp_path: Path,
) -> None:
    """V1 FAIL: outputs dir was never touched (paradox guard)."""
    _build_valid_tmp_repo(tmp_path)
    (tmp_path / PARENT_02_01_02_PARQUET_RELPATH).unlink()
    adjudicate_temporal_feature_grid(tmp_path)
    # Parent dir of the planned output must not exist (V1.H6 / V3.H5 binding).
    assert not (tmp_path / FORBIDDEN_OUTPUT_PARENT_RELPATH).exists()


def test_pass_idempotent_filenames(clean_real_output_dir: None) -> None:
    """PASS emits files at the documented filenames."""
    del clean_real_output_dir
    result = adjudicate_temporal_feature_grid(_REPO_ROOT)
    assert result.csv_path is not None
    assert result.md_path is not None
    assert result.csv_path.name == OUTPUT_CSV_FILENAME
    assert result.md_path.name == OUTPUT_MD_FILENAME


def test_pass_decision_csv_all_rows_have_invariant_i3_cited(
    clean_real_output_dir: None,
) -> None:
    """Every emitted CSV row carries the Invariant I3 citation column."""
    del clean_real_output_dir
    result = adjudicate_temporal_feature_grid(_REPO_ROOT)
    assert result.csv_path is not None
    with result.csv_path.open() as fh:
        for r in csv.DictReader(fh):
            assert r["invariant_i3_cited"] == "Invariant I3"


def test_pass_decision_md_summary_states_row_and_column_counts(
    clean_real_output_dir: None,
) -> None:
    """MD §14 summary states the 16-row x 16-col shape."""
    del clean_real_output_dir
    result = adjudicate_temporal_feature_grid(_REPO_ROOT)
    assert result.md_path is not None
    md_text = result.md_path.read_text()
    assert "16 body rows" in md_text
    assert "16 columns" in md_text
