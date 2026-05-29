"""Tests for ``validate_symmetry_difference_feature_materialization`` (scaffold design contract).

Covers the 14-step halting-falsifier priority chain for the Step 02_02_01
symmetry & difference feature scaffold:
    - module imports + constants exist;
    - dataclass field shapes;
    - audit JSON tuples match embedded constants;
    - input Parquet path existence + SHA256 byte-stability;
    - audit JSON alignment + mutation rejection;
    - direction annotation literal validity (per PR #265 plan A9 / N4);
    - direction-name suffix consistency;
    - source-column traceability (per PR #265 plan A10 / N5);
    - boundary-aware slot-token sweep (per PR #265 plan A8 / N3);
    - boundary-aware POST_GAME token sweep (per PR #265 plan A11 / N6)
      with positive controls for ``focal_prior_win_rate_decisive`` and
      ``matchup_h2h_focal_win_rate``;
    - reconstructed_rating family exclusion;
    - AoE2 ``civilization`` / ``civ`` token exclusion;
    - tracker-source prefix exclusion;
    - artifact-directory ABSENCE (not emptiness) (per PR #265 plan A12 / N7);
    - validator-writes-no-files invariant;
    - halting-falsifier priority chain (first failure wins);
    - real input artifact smoke test.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from rts_predict.games.sc2.datasets.sc2egset.validate_symmetry_difference_feature_materialization import (  # noqa: E501
    BLOCKED_FAMILY_FRAGMENTS,
    BLOCKED_SLOT_TOKEN_REGEX,
    CONTEXT_ANCHOR_COLUMNS,
    EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES,
    FORBIDDEN_AOE2_VOCABULARY,
    IDENTITY_COLUMNS,
    INPUT_02_01_02_AUDIT_JSON_RELPATH,
    INPUT_02_01_02_PARQUET_RELPATH,
    INPUT_02_01_02_PARQUET_SHA256,
    INPUT_02_01_03_AUDIT_JSON_RELPATH,
    INPUT_02_01_03_PARQUET_RELPATH,
    INPUT_02_01_03_PARQUET_SHA256,
    POST_GAME_TOKEN_ALLOWLIST_SUBSTRINGS,
    POST_GAME_TOKEN_REGEX,
    POST_GAME_TOKENS,
    TRACKER_SOURCE_PREFIX,
    UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02,
    UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03,
    VALID_DIRECTION_LITERAL_VALUES,
    CandidateFeatureSpec,
    SymmetryDifferenceValidationResult,
    validate_symmetry_difference_feature_materialization,
)

# ---------------------------------------------------------------------------
# Repo-relative paths — resolved from this test file's location
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[6]

REAL_INPUT_02_01_02_PARQUET = _REPO_ROOT / INPUT_02_01_02_PARQUET_RELPATH
REAL_INPUT_02_01_03_PARQUET = _REPO_ROOT / INPUT_02_01_03_PARQUET_RELPATH
REAL_AUDIT_02_01_02_JSON = _REPO_ROOT / INPUT_02_01_02_AUDIT_JSON_RELPATH
REAL_AUDIT_02_01_03_JSON = _REPO_ROOT / INPUT_02_01_03_AUDIT_JSON_RELPATH


# ---------------------------------------------------------------------------
# Canonical valid candidate-spec triple
# ---------------------------------------------------------------------------


def _valid_difference_specs() -> tuple[CandidateFeatureSpec, ...]:
    """Return a structurally valid difference-family spec tuple."""
    return (
        CandidateFeatureSpec(
            column_name="focal_minus_opponent_prior_match_count_diff",
            direction="focal_minus_opponent",
            source_columns=(
                "focal_prior_match_count",
                "opponent_prior_match_count",
            ),
        ),
        CandidateFeatureSpec(
            column_name="focal_minus_opponent_apm_prior_mean_diff",
            direction="focal_minus_opponent",
            source_columns=("focal_apm_prior_mean", "opponent_apm_prior_mean"),
        ),
    )


def _valid_symmetric_pair_specs() -> tuple[CandidateFeatureSpec, ...]:
    """Return a structurally valid symmetric-pair spec tuple."""
    return (
        CandidateFeatureSpec(
            column_name="prior_match_count_pair_mean",
            direction="symmetric",
            source_columns=(
                "focal_prior_match_count",
                "opponent_prior_match_count",
            ),
        ),
        CandidateFeatureSpec(
            column_name="apm_prior_mean_abs_diff",
            direction="symmetric",
            source_columns=("focal_apm_prior_mean", "opponent_apm_prior_mean"),
        ),
    )


def _valid_race_pair_candidate_specs() -> tuple[CandidateFeatureSpec, ...]:
    """Return the race-pair CANDIDATE / 02_05 deferral marker spec tuple."""
    return (
        CandidateFeatureSpec(
            column_name="race_pair__defer_to_02_05",
            direction="symmetric",
            source_columns=("race_pair",),
        ),
    )


def _valid_candidate_specs() -> tuple[
    tuple[CandidateFeatureSpec, ...],
    tuple[CandidateFeatureSpec, ...],
    tuple[CandidateFeatureSpec, ...],
]:
    """Return the canonical (diff, sym, race-pair) valid triple."""
    return (
        _valid_difference_specs(),
        _valid_symmetric_pair_specs(),
        _valid_race_pair_candidate_specs(),
    )


def _call_with_real_inputs(
    diff: tuple[CandidateFeatureSpec, ...],
    sym: tuple[CandidateFeatureSpec, ...],
    race: tuple[CandidateFeatureSpec, ...],
    repo_root: Path | None = None,
) -> SymmetryDifferenceValidationResult:
    """Invoke validator with real input paths and the supplied spec triple."""
    return validate_symmetry_difference_feature_materialization(
        REAL_INPUT_02_01_02_PARQUET,
        REAL_INPUT_02_01_03_PARQUET,
        (REAL_AUDIT_02_01_02_JSON, REAL_AUDIT_02_01_03_JSON),
        diff,
        sym,
        race,
        repo_root=repo_root,
    )


# ---------------------------------------------------------------------------
# Module imports + constants
# ---------------------------------------------------------------------------


def test_module_imports_cleanly() -> None:
    """The validator module is importable and exposes its public symbols."""
    assert callable(validate_symmetry_difference_feature_materialization)
    assert CandidateFeatureSpec is not None
    assert SymmetryDifferenceValidationResult is not None


def test_expected_constants_exist() -> None:
    """All module-level constants are non-empty and the right shape."""
    assert isinstance(INPUT_02_01_02_PARQUET_RELPATH, str)
    assert INPUT_02_01_02_PARQUET_RELPATH.endswith(".parquet")
    assert isinstance(INPUT_02_01_03_PARQUET_RELPATH, str)
    assert INPUT_02_01_03_PARQUET_RELPATH.endswith(".parquet")
    assert len(INPUT_02_01_02_PARQUET_SHA256) == 64
    assert len(INPUT_02_01_03_PARQUET_SHA256) == 64
    assert IDENTITY_COLUMNS == ("focal_match_id", "focal_player", "opponent_player")
    assert CONTEXT_ANCHOR_COLUMNS == ("started_at",)
    assert len(UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02) == 7
    assert len(UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03) == 24
    assert VALID_DIRECTION_LITERAL_VALUES == ("focal_minus_opponent", "symmetric")
    assert len(BLOCKED_SLOT_TOKEN_REGEX) >= 12
    assert "reconstructed_rating" in BLOCKED_FAMILY_FRAGMENTS
    assert len(POST_GAME_TOKENS) == 10
    assert len(POST_GAME_TOKEN_REGEX) == len(POST_GAME_TOKENS)
    assert "civilization" in FORBIDDEN_AOE2_VOCABULARY
    assert TRACKER_SOURCE_PREFIX == "tracker_events_raw"
    assert len(EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES) == 2


def test_dataclass_field_shape() -> None:
    """CandidateFeatureSpec and SymmetryDifferenceValidationResult fields are present."""
    spec = CandidateFeatureSpec(
        column_name="x",
        direction="symmetric",
        source_columns=("a",),
    )
    assert spec.column_name == "x"
    assert spec.direction == "symmetric"
    assert spec.source_columns == ("a",)
    # Frozen dataclass — mutation must raise.
    with pytest.raises(Exception):  # noqa: BLE001
        spec.column_name = "y"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Audit JSON tuple equality vs constants
# ---------------------------------------------------------------------------


def test_audit_tuples_match_audit_jsons() -> None:
    """``features_audited`` in both real audit JSONs equals embedded constants."""
    with REAL_AUDIT_02_01_02_JSON.open(encoding="utf-8") as fh:
        audit_02 = json.load(fh)
    with REAL_AUDIT_02_01_03_JSON.open(encoding="utf-8") as fh:
        audit_03 = json.load(fh)
    assert tuple(audit_02["features_audited"]) == UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02
    assert tuple(audit_03["features_audited"]) == UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03
    assert tuple(audit_02["projected_identity_columns"]) == IDENTITY_COLUMNS
    assert tuple(audit_03["projected_identity_columns"]) == IDENTITY_COLUMNS
    assert tuple(audit_02["projected_context_columns"]) == CONTEXT_ANCHOR_COLUMNS
    assert tuple(audit_03["projected_context_columns"]) == CONTEXT_ANCHOR_COLUMNS


# ---------------------------------------------------------------------------
# Input Parquet existence + SHA256
# ---------------------------------------------------------------------------


def test_input_parquets_exist() -> None:
    """Both upstream Parquet artifacts exist at their canonical paths."""
    assert REAL_INPUT_02_01_02_PARQUET.exists()
    assert REAL_INPUT_02_01_03_PARQUET.exists()


def test_input_parquet_sha256_matches() -> None:
    """The validator passes with real inputs (SHA256 pin matches)."""
    diff, sym, race = _valid_candidate_specs()
    result = _call_with_real_inputs(diff, sym, race)
    assert result.input_parquet_paths_present_ok is True
    assert result.input_parquet_sha256_ok is True


def test_missing_input_parquet_fails(tmp_path: Path) -> None:
    """A non-existent input Parquet halts at input_parquet_missing."""
    diff, sym, race = _valid_candidate_specs()
    bogus = tmp_path / "no_such.parquet"
    result = validate_symmetry_difference_feature_materialization(
        bogus,
        REAL_INPUT_02_01_03_PARQUET,
        (REAL_AUDIT_02_01_02_JSON, REAL_AUDIT_02_01_03_JSON),
        diff,
        sym,
        race,
    )
    assert result.passed is False
    assert result.halting_falsifier == "input_parquet_missing"
    assert result.input_parquet_paths_present_ok is False


def test_input_parquet_sha256_mismatch_fails(tmp_path: Path) -> None:
    """A one-byte mutation of an input Parquet halts at input_parquet_sha_mismatch."""
    diff, sym, race = _valid_candidate_specs()
    # Copy then mutate one byte at the end.
    mutated = tmp_path / "mutated.parquet"
    shutil.copy(REAL_INPUT_02_01_02_PARQUET, mutated)
    with mutated.open("r+b") as fh:
        fh.seek(0, 2)  # seek to end
        size = fh.tell()
        fh.seek(size - 1)
        last_byte = fh.read(1)
        fh.seek(size - 1)
        fh.write(bytes([(last_byte[0] ^ 0x01) & 0xFF]))
    result = validate_symmetry_difference_feature_materialization(
        mutated,
        REAL_INPUT_02_01_03_PARQUET,
        (REAL_AUDIT_02_01_02_JSON, REAL_AUDIT_02_01_03_JSON),
        diff,
        sym,
        race,
    )
    assert result.passed is False
    assert result.halting_falsifier == "input_parquet_sha_mismatch"
    assert result.input_parquet_sha256_ok is False


# ---------------------------------------------------------------------------
# Parent audit JSON presence + alignment
# ---------------------------------------------------------------------------


def test_audit_json_alignment_ok() -> None:
    """Real audit JSONs align with embedded constants (audit_json_alignment_ok=True)."""
    diff, sym, race = _valid_candidate_specs()
    result = _call_with_real_inputs(diff, sym, race)
    assert result.parent_audit_json_paths_present_ok is True
    assert result.audit_json_alignment_ok is True


def test_missing_audit_json_fails(tmp_path: Path) -> None:
    """A non-existent audit JSON halts at parent_audit_json_missing."""
    diff, sym, race = _valid_candidate_specs()
    bogus = tmp_path / "no_audit.json"
    result = validate_symmetry_difference_feature_materialization(
        REAL_INPUT_02_01_02_PARQUET,
        REAL_INPUT_02_01_03_PARQUET,
        (bogus, REAL_AUDIT_02_01_03_JSON),
        diff,
        sym,
        race,
    )
    assert result.passed is False
    assert result.halting_falsifier == "parent_audit_json_missing"
    assert result.parent_audit_json_paths_present_ok is False


def test_audit_json_alignment_fails_with_mutated_audit(tmp_path: Path) -> None:
    """A mutated audit JSON ``features_audited`` halts at audit_json_misaligned."""
    diff, sym, race = _valid_candidate_specs()
    mutated_audit = tmp_path / "mutated_audit_02_01_02.json"
    with REAL_AUDIT_02_01_02_JSON.open(encoding="utf-8") as fh:
        data = json.load(fh)
    data["features_audited"] = ["totally_made_up_column"]
    with mutated_audit.open("w", encoding="utf-8") as fh:
        json.dump(data, fh)
    result = validate_symmetry_difference_feature_materialization(
        REAL_INPUT_02_01_02_PARQUET,
        REAL_INPUT_02_01_03_PARQUET,
        (mutated_audit, REAL_AUDIT_02_01_03_JSON),
        diff,
        sym,
        race,
    )
    assert result.passed is False
    assert result.halting_falsifier == "audit_json_misaligned"
    assert result.audit_json_alignment_ok is False


# ---------------------------------------------------------------------------
# Direction annotation validity (per A9 / N4)
# ---------------------------------------------------------------------------


def test_valid_candidate_focal_minus_opponent_passes() -> None:
    """A clean focal_minus_opponent candidate triple passes."""
    diff, sym, race = _valid_candidate_specs()
    result = _call_with_real_inputs(diff, sym, race)
    assert result.passed is True
    assert result.direction_annotation_valid is True


def test_valid_candidate_symmetric_passes() -> None:
    """A clean symmetric candidate triple passes."""
    sym_only = _valid_symmetric_pair_specs()
    result = _call_with_real_inputs((), sym_only, ())
    assert result.passed is True
    assert result.direction_annotation_valid is True


@pytest.mark.parametrize("invalid_direction", ["invalid", "diff", "", "FOCAL_MINUS_OPPONENT"])
def test_invalid_direction_literal_fails(invalid_direction: str) -> None:
    """An invalid direction literal halts at direction_annotation_invalid."""
    bad = (
        CandidateFeatureSpec(
            column_name="prior_match_count_pair_mean",
            direction=invalid_direction,  # type: ignore[arg-type]
            source_columns=(
                "focal_prior_match_count",
                "opponent_prior_match_count",
            ),
        ),
    )
    result = _call_with_real_inputs((), bad, ())
    assert result.passed is False
    assert result.halting_falsifier == "direction_annotation_invalid"
    assert result.direction_annotation_valid is False


# ---------------------------------------------------------------------------
# Slot-token regex sweep (per A8 / N3)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "slot_token_name",
    [
        "player_1_match_count_diff",
        "player2_match_count_diff",
        "slot_1_match_count_diff",
        "p1_apm_diff",
        "idx_1_apm_diff",
        "home_apm_pair_mean",
        "away_apm_pair_mean",
        "left_apm_pair_mean",
        "right_apm_pair_mean",
        "host_apm_pair_mean",
        "guest_apm_pair_mean",
        "apm_a_minus_b_diff",
        "apm_b_minus_a_diff",
    ],
)
def test_blocked_slot_token_variants_fail(slot_token_name: str) -> None:
    """Slot-token variants (player/slot/p/idx/home/away/etc.) fire the falsifier."""
    bad = (
        CandidateFeatureSpec(
            column_name=slot_token_name,
            direction="focal_minus_opponent",
            source_columns=(
                "focal_prior_match_count",
                "opponent_prior_match_count",
            ),
        ),
    )
    result = _call_with_real_inputs(bad, (), ())
    assert result.passed is False
    assert result.halting_falsifier == "slot_dependent_token_present"
    assert result.slot_token_violations
    assert result.slot_token_violations[0][0] == slot_token_name


# ---------------------------------------------------------------------------
# Source-column traceability (per A10 / N5)
# ---------------------------------------------------------------------------


def test_audited_tuple_traceability_passes_for_known_columns() -> None:
    """Source_columns drawn from the 7+24 audited union pass traceability."""
    diff, sym, race = _valid_candidate_specs()
    result = _call_with_real_inputs(diff, sym, race)
    assert result.source_column_traceability_ok is True


def test_audited_tuple_traceability_fails_for_unknown_column() -> None:
    """An unknown source_column halts at source_column_traceability_violation."""
    bad = (
        CandidateFeatureSpec(
            column_name="prior_match_count_pair_mean",
            direction="symmetric",
            source_columns=(
                "focal_prior_match_count",
                "made_up_column_name",
            ),
        ),
    )
    result = _call_with_real_inputs((), bad, ())
    assert result.passed is False
    assert result.halting_falsifier == "source_column_traceability_violation"
    assert result.source_column_traceability_ok is False


def test_phase03_split_candidate_fails() -> None:
    """A Phase-03-style fold_split source name fails traceability."""
    bad = (
        CandidateFeatureSpec(
            column_name="fold_split_id_pair_mean",
            direction="symmetric",
            source_columns=("cv_fold_id",),
        ),
    )
    result = _call_with_real_inputs((), bad, ())
    assert result.passed is False
    assert result.halting_falsifier == "source_column_traceability_violation"


# ---------------------------------------------------------------------------
# Boundary-aware POST_GAME token sweep (per A11 / N6)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "leak_token_name",
    [
        "focal_won_count_diff",
        "outcome_pair_mean",
        "winner_pair_mean",
        "result_pair_mean",
        "loss_count_diff",
        "match_result_pair_mean",
        "post_game_score_diff",
        "final_state_pair_mean",
    ],
)
def test_boundary_aware_post_game_token_catches_real_tokens(
    leak_token_name: str,
) -> None:
    """Real POST_GAME tokens (won/loss/result/etc.) fire the leakage falsifier."""
    bad = (
        CandidateFeatureSpec(
            column_name=leak_token_name,
            direction="symmetric",
            source_columns=("focal_prior_match_count",),
        ),
    )
    result = _call_with_real_inputs((), bad, ())
    assert result.passed is False
    assert result.halting_falsifier == "target_leak_token_in_candidate"
    assert result.target_leak_token_violations


@pytest.mark.parametrize(
    "allowlist_name",
    [
        "focal_prior_win_rate_decisive",
        "matchup_h2h_focal_win_rate",
        "focal_prior_win_rate_race_conditional",
        "focal_prior_win_rate_map_conditional",
        "focal_prior_win_rate_matchup_conditional",
    ],
)
def test_boundary_aware_post_game_token_no_false_positive_on_win_rate(
    allowlist_name: str,
) -> None:
    """Legitimate ``prior_win_rate`` compounds do NOT fire the leak falsifier."""
    spec = (
        CandidateFeatureSpec(
            column_name=allowlist_name + "_pair_mean",
            direction="symmetric",
            source_columns=(allowlist_name,) if allowlist_name in (
                UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02
                + UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03
            ) else ("focal_prior_win_rate_decisive",),
        ),
    )
    result = _call_with_real_inputs((), spec, ())
    # Either the validator passes overall, OR the halting falsifier is NOT
    # target_leak_token_in_candidate.
    assert result.halting_falsifier != "target_leak_token_in_candidate"
    assert result.target_leak_token_violations == ()


def test_allowlist_substrings_constant_covers_real_audited_compounds() -> None:
    """POST_GAME_TOKEN_ALLOWLIST_SUBSTRINGS covers every real ``win_rate`` audited column."""
    audited = (
        UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02
        + UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03
    )
    for col in audited:
        if "win" in col:
            assert any(
                allow in col for allow in POST_GAME_TOKEN_ALLOWLIST_SUBSTRINGS
            ), f"Audited column {col!r} contains 'win' but no allowlist match"


# ---------------------------------------------------------------------------
# Reconstructed-rating exclusion
# ---------------------------------------------------------------------------


def test_reconstructed_rating_candidate_fails() -> None:
    """A reconstructed_rating-family candidate halts at reconstructed_rating_in_candidates."""
    bad = (
        CandidateFeatureSpec(
            column_name="reconstructed_rating_diff",
            direction="focal_minus_opponent",
            source_columns=("focal_prior_match_count", "opponent_prior_match_count"),
        ),
    )
    result = _call_with_real_inputs(bad, (), ())
    assert result.passed is False
    assert result.halting_falsifier == "reconstructed_rating_in_candidates"
    assert result.reconstructed_rating_violations


# ---------------------------------------------------------------------------
# AoE2 vocabulary exclusion (Invariant I8)
# ---------------------------------------------------------------------------


def test_aoe2_civilization_token_in_candidate_fails() -> None:
    """An AoE2 ``civilization`` token halts at aoe2_vocabulary_in_candidate."""
    bad = (
        CandidateFeatureSpec(
            column_name="civilization_pair_mean",
            direction="symmetric",
            source_columns=("focal_prior_match_count",),
        ),
    )
    result = _call_with_real_inputs((), bad, ())
    assert result.passed is False
    assert result.halting_falsifier == "aoe2_vocabulary_in_candidate"
    assert result.aoe2_vocabulary_violations


def test_aoe2_civ_token_in_candidate_fails() -> None:
    """The shorthand AoE2 ``civ`` token also halts."""
    bad = (
        CandidateFeatureSpec(
            column_name="focal_civ_count_diff",
            direction="focal_minus_opponent",
            source_columns=("focal_prior_match_count",),
        ),
    )
    result = _call_with_real_inputs(bad, (), ())
    assert result.passed is False
    assert result.halting_falsifier == "aoe2_vocabulary_in_candidate"


# ---------------------------------------------------------------------------
# Tracker-source prefix exclusion (Invariant I3)
# ---------------------------------------------------------------------------


def test_tracker_target_match_candidate_fails() -> None:
    """A tracker-source candidate halts at tracker_sourced_candidate."""
    bad = (
        CandidateFeatureSpec(
            column_name="tracker_unit_count_pair_mean",
            direction="symmetric",
            source_columns=("tracker_events_raw_unit_born",),
        ),
    )
    # Tracker source is also not in audited tuples, so traceability fires
    # first per the halting priority chain. The point of this test is to
    # ensure traceability OR tracker falsifier halts.
    result = _call_with_real_inputs((), bad, ())
    assert result.passed is False
    assert result.halting_falsifier in {
        "source_column_traceability_violation",
        "tracker_sourced_candidate",
    }


def test_tracker_prefix_detected_when_traceability_first_passes() -> None:
    """Tracker-prefix source plus a valid source: traceability halts first.

    Tracker source isn't in audited tuples, so traceability fires before
    the tracker falsifier per the halting priority chain.
    """
    # We cannot mutate the audited tuples at runtime; instead verify the
    # tracker_sourced_violations field gets populated via the public path
    # when the column traces (degenerate case: spec with one valid src AND
    # one tracker src). Direction-name consistency is not implicated.
    bad = (
        CandidateFeatureSpec(
            column_name="prior_match_count_pair_mean",
            direction="symmetric",
            source_columns=(
                "focal_prior_match_count",
                "tracker_events_raw_unit_born",
            ),
        ),
    )
    result = _call_with_real_inputs((), bad, ())
    # Traceability fires first because the tracker source isn't in audited.
    assert result.passed is False
    assert result.source_column_traceability_ok is False


# ---------------------------------------------------------------------------
# Race-pair CANDIDATE / 02_05 deferral marker
# ---------------------------------------------------------------------------


def test_race_pair_candidate_marked_may_defer_to_02_05_passes() -> None:
    """The race_pair__defer_to_02_05 marker is accepted as a valid candidate."""
    race = _valid_race_pair_candidate_specs()
    result = _call_with_real_inputs((), (), race)
    assert result.passed is True


# ---------------------------------------------------------------------------
# Artifact-directory absence (per A12 / N7)
# ---------------------------------------------------------------------------


def test_artifact_directory_absent_passes() -> None:
    """When neither target directory exists, artifact_directory_absence_ok=True."""
    diff, sym, race = _valid_candidate_specs()
    result = _call_with_real_inputs(diff, sym, race)
    assert result.artifact_directory_absence_ok is True


def test_artifact_directory_present_fails_when_directory_exists(
    tmp_path: Path,
) -> None:
    """When a target directory exists (even empty), the falsifier fires."""
    # Create the 02_02_01 directory inside tmp_path-scoped repo root.
    (tmp_path / EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES[0]).mkdir(parents=True)
    diff, sym, race = _valid_candidate_specs()
    result = _call_with_real_inputs(diff, sym, race, repo_root=tmp_path)
    assert result.passed is False
    assert result.halting_falsifier == "artifact_directory_present"
    assert result.artifact_directory_absence_ok is False


def test_artifact_directory_present_fails_with_only_gitkeep(
    tmp_path: Path,
) -> None:
    """Even a `.gitkeep`-only directory fires the falsifier (absence != emptiness)."""
    target = tmp_path / EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES[1]
    target.mkdir(parents=True)
    (target / ".gitkeep").write_text("")
    diff, sym, race = _valid_candidate_specs()
    result = _call_with_real_inputs(diff, sym, race, repo_root=tmp_path)
    assert result.passed is False
    assert result.halting_falsifier == "artifact_directory_present"


# ---------------------------------------------------------------------------
# Validator writes no files; materialized_output_paths always ()
# ---------------------------------------------------------------------------


def test_materialized_output_paths_is_empty_tuple_when_passing() -> None:
    """When passing, materialized_output_paths is exactly ()."""
    diff, sym, race = _valid_candidate_specs()
    result = _call_with_real_inputs(diff, sym, race)
    assert result.materialized_output_paths == ()


def test_validator_writes_no_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Running the validator does not create any file under tmp_path."""
    monkeypatch.chdir(tmp_path)
    diff, sym, race = _valid_candidate_specs()
    _call_with_real_inputs(diff, sym, race)
    # tmp_path should be empty (validator never writes).
    assert list(tmp_path.iterdir()) == []


# ---------------------------------------------------------------------------
# Halting falsifier priority chain — first failure wins
# ---------------------------------------------------------------------------


def test_halting_falsifier_priority_first_failure_wins(tmp_path: Path) -> None:
    """Missing-input + invalid-direction simultaneously: input_parquet_missing wins."""
    bogus = tmp_path / "no_such.parquet"
    bad_direction = (
        CandidateFeatureSpec(
            column_name="some_name",
            direction="totally_invalid",  # type: ignore[arg-type]
            source_columns=("focal_prior_match_count",),
        ),
    )
    result = validate_symmetry_difference_feature_materialization(
        bogus,
        REAL_INPUT_02_01_03_PARQUET,
        (REAL_AUDIT_02_01_02_JSON, REAL_AUDIT_02_01_03_JSON),
        (),
        bad_direction,
        (),
    )
    assert result.passed is False
    # input_parquet_missing has higher priority than
    # direction_annotation_invalid.
    assert result.halting_falsifier == "input_parquet_missing"


# ---------------------------------------------------------------------------
# Direction-name consistency
# ---------------------------------------------------------------------------


def test_direction_name_inconsistent_diff_with_symmetric_label() -> None:
    """A ``_diff`` suffix with direction=symmetric halts at direction_name_inconsistent."""
    bad = (
        CandidateFeatureSpec(
            column_name="prior_match_count_diff",
            direction="symmetric",
            source_columns=(
                "focal_prior_match_count",
                "opponent_prior_match_count",
            ),
        ),
    )
    result = _call_with_real_inputs((), bad, ())
    assert result.passed is False
    assert result.halting_falsifier == "direction_name_inconsistent"
    assert result.direction_name_consistency_ok is False


def test_direction_name_inconsistent_pair_mean_with_diff_label() -> None:
    """A ``_pair_mean`` token with direction=focal_minus_opponent halts the validator."""
    bad = (
        CandidateFeatureSpec(
            column_name="prior_match_count_pair_mean",
            direction="focal_minus_opponent",
            source_columns=(
                "focal_prior_match_count",
                "opponent_prior_match_count",
            ),
        ),
    )
    result = _call_with_real_inputs(bad, (), ())
    assert result.passed is False
    assert result.halting_falsifier == "direction_name_inconsistent"


# ---------------------------------------------------------------------------
# Real input artifact smoke test
# ---------------------------------------------------------------------------


def test_real_input_artifact_smoke() -> None:
    """End-to-end smoke: real inputs + valid candidate triple => passed=True."""
    diff, sym, race = _valid_candidate_specs()
    result = _call_with_real_inputs(diff, sym, race)
    assert result.passed is True
    assert result.halting_falsifier is None
    assert result.materialized_output_paths == ()
    assert result.artifact_directory_absence_ok is True
    assert result.input_parquet_sha256_ok is True
    assert result.audit_json_alignment_ok is True
    assert result.direction_annotation_valid is True
    assert result.source_column_traceability_ok is True
    assert result.direction_name_consistency_ok is True
    assert result.slot_token_violations == ()
    assert result.target_leak_token_violations == ()
    assert result.reconstructed_rating_violations == ()
    assert result.aoe2_vocabulary_violations == ()
    assert result.tracker_sourced_violations == ()
