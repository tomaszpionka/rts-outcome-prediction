"""Tests for ``validate_pre_game_feature_materialization`` (scaffold design contract).

Covers all required test cases for the pre-game tranche-1 scaffold validation:
    - 5-family tranche membership (exactly the 5 ids).
    - Extra pre_game family rejected.
    - is_mmr_missing_flag provenance/missingness (not skill) — happy path.
    - _is_forbidden_skill_column PASS (allowed missingness flags).
    - _is_forbidden_skill_column FAIL (forbidden skill/rating/MMR-scalar).
    - _is_forbidden_skill_column no false positives (cumulative/summary/skillset_id/elong).
    - Stale _sc2egset registry filename raises.
    - Tracker-derived source in tranche rejected.
    - history_enriched_pre_game family in tranche rejected.
    - in_game_snapshot family in tranche rejected.
    - Asymmetric per_player_construction rejected.
    - POST-GAME token in designed names rejected.
    - materialized_output_paths always ().
    - PR #230 leakage JSON vacuity unchanged (features_audited == []).
    - Real registry CSV smoke test (skipif if absent).

Uses ``tmp_path`` synthetic CSVs for all falsifier tests. Uses module-level
constants for the standard DESIGNED_COLUMN_NAMES tuple.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import pytest

from rts_predict.games.sc2.datasets.sc2egset.validate_pre_game_feature_materialization import (
    EXPECTED_TRANCHE1_COUNT,
    STALE_REGISTRY_FILENAME_FRAGMENT,
    TRANCHE1_PRE_GAME_FAMILY_IDS,
    PreGameTrancheRow,
    _check_is_mmr_missing_is_flag_not_skill,
    _check_no_post_game_tokens,
    _is_forbidden_skill_column,
    load_pre_game_tranche_rows,
    validate_pre_game_feature_materialization,
)

# ---------------------------------------------------------------------------
# Repo-relative paths — resolved from this test file's location
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

LEAKAGE_AUDIT_JSON_PATH: Path = (
    _TESTS_ROOT
    / "src"
    / "rts_predict"
    / "games"
    / "sc2"
    / "datasets"
    / "sc2egset"
    / "reports"
    / "artifacts"
    / "02_01_01"
    / "leakage_audit_sc2egset.json"
)

# ---------------------------------------------------------------------------
# Standard designed column names (the 9 tranche-1 planned columns)
# ---------------------------------------------------------------------------

DESIGNED_COLUMN_NAMES: tuple[str, ...] = (
    "focal_race",
    "opponent_race",
    "race_pair",
    "focal_matchup",
    "opponent_matchup",
    "map_type",
    "patch_version",
    "focal_is_mmr_missing",
    "opponent_is_mmr_missing",
)

# ---------------------------------------------------------------------------
# Synthetic CSV helpers
# ---------------------------------------------------------------------------

_REGISTRY_COLUMNS = (
    "feature_family_id",
    "dataset_tag",
    "prediction_setting",
    "source_table_or_event_family",
    "source_grain",
    "model_input_grain",
    "target_grain",
    "temporal_anchor",
    "allowed_cutoff_rule",
    "candidate_leakage_modes",
    "cold_start_handling",
    "status",
    "per_player_construction",
    "block",
)


def _tranche_row(**kwargs: Any) -> dict[str, str]:
    """Build a minimal valid tranche-1 pre_game registry row."""
    defaults: dict[str, str] = {
        "feature_family_id": "sc2egset.pre_game.focal_race_with_opponent_race_pair",
        "dataset_tag": "sc2egset",
        "prediction_setting": "pre_game",
        "source_table_or_event_family": "replay_players_raw",
        "source_grain": "(filename, player_id_worldwide)",
        "model_input_grain": "(focal_match_id, focal_player)",
        "target_grain": "(focal_match_id, focal_player)",
        "temporal_anchor": "details_timeUTC",
        "allowed_cutoff_rule": "snapshot_at_match_start",
        "candidate_leakage_modes": "none",
        "cold_start_handling": "G-CS-1",
        "status": "allowed",
        "per_player_construction": "symmetric",
        "block": "pre_game",
    }
    defaults.update(kwargs)
    return defaults


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    """Write a registry CSV to disk."""
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(_REGISTRY_COLUMNS))
        writer.writeheader()
        writer.writerows(rows)


def _all_five_tranche_rows() -> list[dict[str, str]]:
    """Build the 5 standard tranche-1 rows."""
    return [
        _tranche_row(feature_family_id="sc2egset.pre_game.focal_race_with_opponent_race_pair",
                     source_table_or_event_family="replay_players_raw"),
        _tranche_row(feature_family_id="sc2egset.pre_game.map_type_encoded",
                     source_table_or_event_family="matches_flat"),
        _tranche_row(feature_family_id="sc2egset.pre_game.patch_version_encoded",
                     source_table_or_event_family="matches_flat"),
        _tranche_row(feature_family_id="sc2egset.pre_game.matchup_encoded",
                     source_table_or_event_family="replay_players_raw"),
        _tranche_row(feature_family_id="sc2egset.pre_game.is_mmr_missing_flag",
                     source_table_or_event_family="replay_players_raw"),
    ]


# ---------------------------------------------------------------------------
# Test 1: Exact 5-family tranche membership
# ---------------------------------------------------------------------------


class TestExactTrancheMembership:
    """Exactly 5 tranche-1 families are loaded from a synthetic CSV."""

    def test_five_family_ids_loaded(self, tmp_path: Path) -> None:
        """All 5 TRANCHE1_PRE_GAME_FAMILY_IDS are loaded; no extras."""
        csv_path = tmp_path / "registry.csv"
        _write_csv(csv_path, _all_five_tranche_rows())

        result = validate_pre_game_feature_materialization(
            csv_path, DESIGNED_COLUMN_NAMES
        )

        assert result.tranche_count == EXPECTED_TRANCHE1_COUNT
        assert set(result.tranche_family_ids) == TRANCHE1_PRE_GAME_FAMILY_IDS
        assert result.extra_families_in_tranche == ()

    def test_passed_is_true_with_five_rows(self, tmp_path: Path) -> None:
        """Validation passes with exactly the 5 tranche-1 rows."""
        csv_path = tmp_path / "registry.csv"
        _write_csv(csv_path, _all_five_tranche_rows())

        result = validate_pre_game_feature_materialization(
            csv_path, DESIGNED_COLUMN_NAMES
        )

        assert result.passed is True
        assert result.halting_falsifier is None


# ---------------------------------------------------------------------------
# Test 2: Extra pre_game family rejected
# ---------------------------------------------------------------------------


class TestExtraPreGameFamilyRejected:
    """An extra pre_game family not in TRANCHE1_PRE_GAME_FAMILY_IDS fires extra_in_tranche."""

    def test_extra_family_fires_falsifier(self, tmp_path: Path) -> None:
        """Adding a 6th pre_game row outside the tranche causes failure."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_five_tranche_rows() + [
            _tranche_row(
                feature_family_id="sc2egset.pre_game.unknown_extra_family",
                source_table_or_event_family="matches_flat",
            )
        ]
        _write_csv(csv_path, rows)

        result = validate_pre_game_feature_materialization(
            csv_path, DESIGNED_COLUMN_NAMES
        )

        assert result.passed is False
        assert result.halting_falsifier == "extra_in_tranche"
        assert "sc2egset.pre_game.unknown_extra_family" in result.extra_families_in_tranche


# ---------------------------------------------------------------------------
# Test 3: is_mmr_missing_flag provenance/missingness, not skill
# ---------------------------------------------------------------------------


class TestIsMmrMissingFlagProvenance:
    """is_mmr_missing family is classified as a missingness/provenance flag."""

    def test_happy_path_returns_true(self, tmp_path: Path) -> None:
        """Standard 5-family registry with standard designed columns passes."""
        csv_path = tmp_path / "registry.csv"
        _write_csv(csv_path, _all_five_tranche_rows())

        result = validate_pre_game_feature_materialization(
            csv_path, DESIGNED_COLUMN_NAMES
        )

        assert result.is_mmr_missing_classified_as_flag is True
        assert result.passed is True


# ---------------------------------------------------------------------------
# Tests 4 & 5: _is_forbidden_skill_column PASS and FAIL
# ---------------------------------------------------------------------------


class TestIsForbiddenSkillColumnAllowlist:
    """Allowlist-first: approved missingness flag names are not forbidden."""

    @pytest.mark.parametrize(
        "col_name",
        [
            "is_mmr_missing",
            "is_mmr_missing_flag",
            "focal_is_mmr_missing",
            "opponent_is_mmr_missing",
        ],
    )
    def test_approved_flag_names_return_false(self, col_name: str) -> None:
        """Approved missingness flag names return False (allowed)."""
        assert _is_forbidden_skill_column(col_name) is False


class TestIsForbiddenSkillColumnForbidden:
    """Forbidden skill/rating/MMR-scalar column names return True."""

    @pytest.mark.parametrize(
        "col_name",
        [
            "mmr",
            "focal_mmr",
            "opponent_mmr",
            "mmr_value",
            "rating",
            "elo",
            "glicko",
            "skill",
            "mu",
            "sigma",
        ],
    )
    def test_forbidden_skill_names_return_true(self, col_name: str) -> None:
        """Forbidden skill/rating/MMR-scalar names return True (rejected)."""
        assert _is_forbidden_skill_column(col_name) is True


# ---------------------------------------------------------------------------
# Test 6: No false positives for _is_forbidden_skill_column
# ---------------------------------------------------------------------------


class TestIsForbiddenSkillColumnNoFalsePositives:
    """Innocent names containing forbidden token letters inside larger tokens are allowed."""

    @pytest.mark.parametrize(
        "col_name",
        [
            "cumulative",   # contains "mu" as a substring, not a token
            "summary",      # contains "mu" as a substring, not a token
            "skillset_id",  # contains "skill" but as "skillset", not token "skill"
            "elong",        # contains "elo" as a substring, not a token
        ],
    )
    def test_no_false_positive(self, col_name: str) -> None:
        """Innocent names do not trigger the forbidden-skill check."""
        assert _is_forbidden_skill_column(col_name) is False


# ---------------------------------------------------------------------------
# Test 7: Stale _sc2egset registry filename raises
# ---------------------------------------------------------------------------


class TestStaleRegistryFilenameRaises:
    """load_pre_game_tranche_rows raises ValueError for the stale filename."""

    def test_stale_path_raises_value_error(self, tmp_path: Path) -> None:
        """A path containing the stale fragment raises ValueError."""
        stale_path = tmp_path / "02_01_01_feature_family_registry_sc2egset.csv"
        assert STALE_REGISTRY_FILENAME_FRAGMENT in str(stale_path)

        with pytest.raises(ValueError, match="Stale registry path"):
            load_pre_game_tranche_rows(stale_path)


# ---------------------------------------------------------------------------
# Test 8: No tracker-derived family in pre_game tranche
# ---------------------------------------------------------------------------


class TestNoTrackerInPreGameTranche:
    """A tranche-1 family with tracker source fires tracker_in_pre_game."""

    def test_tracker_source_fires_falsifier(self, tmp_path: Path) -> None:
        """One tranche row with tracker_events_raw source causes failure."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_five_tranche_rows()
        # Override the is_mmr_missing row's source to a tracker family
        rows = [
            r if r["feature_family_id"] != "sc2egset.pre_game.is_mmr_missing_flag"
            else _tranche_row(
                feature_family_id="sc2egset.pre_game.is_mmr_missing_flag",
                source_table_or_event_family="tracker_events_raw",
            )
            for r in rows
        ]
        _write_csv(csv_path, rows)

        result = validate_pre_game_feature_materialization(
            csv_path, DESIGNED_COLUMN_NAMES
        )

        assert result.passed is False
        assert result.halting_falsifier == "tracker_in_pre_game"
        assert "sc2egset.pre_game.is_mmr_missing_flag" in result.tracker_in_pre_game


# ---------------------------------------------------------------------------
# Test 9: No history_enriched_pre_game family in tranche 1
# ---------------------------------------------------------------------------


class TestNoHistoryInTranche:
    """A history family aliasing a tranche-1 id fires history_in_tranche."""

    def test_history_row_with_tranche_id_fires_falsifier(
        self, tmp_path: Path
    ) -> None:
        """A registry row with a tranche-1 family_id but history prediction_setting fails."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_five_tranche_rows() + [
            _tranche_row(
                feature_family_id="sc2egset.pre_game.map_type_encoded",
                prediction_setting="history_enriched_pre_game",
                allowed_cutoff_rule="history_time < target_time",
                cold_start_handling="G-CS-2",
            )
        ]
        _write_csv(csv_path, rows)

        result = validate_pre_game_feature_materialization(
            csv_path, DESIGNED_COLUMN_NAMES
        )

        assert result.passed is False
        assert result.halting_falsifier == "history_in_tranche"
        assert "sc2egset.pre_game.map_type_encoded" in result.history_families_in_tranche


# ---------------------------------------------------------------------------
# Test 10: No in_game_snapshot family in tranche 1
# ---------------------------------------------------------------------------


class TestNoInGameInTranche:
    """An in_game family aliasing a tranche-1 id fires in_game_in_tranche."""

    def test_in_game_row_with_tranche_id_fires_falsifier(
        self, tmp_path: Path
    ) -> None:
        """A registry row with a tranche-1 family_id but in_game prediction_setting fails."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_five_tranche_rows() + [
            _tranche_row(
                feature_family_id="sc2egset.pre_game.patch_version_encoded",
                prediction_setting="in_game_snapshot",
                allowed_cutoff_rule="event.loop <= cutoff_loop",
            )
        ]
        _write_csv(csv_path, rows)

        result = validate_pre_game_feature_materialization(
            csv_path, DESIGNED_COLUMN_NAMES
        )

        assert result.passed is False
        assert result.halting_falsifier == "in_game_in_tranche"
        assert "sc2egset.pre_game.patch_version_encoded" in result.in_game_families_in_tranche


# ---------------------------------------------------------------------------
# Test 11: Focal/opponent symmetry
# ---------------------------------------------------------------------------


class TestFocalOpponentSymmetry:
    """A tranche row with asymmetric construction fires the asymmetric falsifier."""

    def test_asymmetric_fires_falsifier(self, tmp_path: Path) -> None:
        """Setting one row's per_player_construction to 'asymmetric' causes failure."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_five_tranche_rows()
        rows = [
            r if r["feature_family_id"] != "sc2egset.pre_game.matchup_encoded"
            else _tranche_row(
                feature_family_id="sc2egset.pre_game.matchup_encoded",
                source_table_or_event_family="replay_players_raw",
                per_player_construction="asymmetric",
            )
            for r in rows
        ]
        _write_csv(csv_path, rows)

        result = validate_pre_game_feature_materialization(
            csv_path, DESIGNED_COLUMN_NAMES
        )

        assert result.passed is False
        assert result.halting_falsifier == "asymmetric"
        assert "sc2egset.pre_game.matchup_encoded" in result.asymmetric_construction


# ---------------------------------------------------------------------------
# Test 12: No POST-GAME token in designed names or source fields
# ---------------------------------------------------------------------------


class TestNoPostGameToken:
    """A POST-GAME token in a designed column name fires the post_game_token falsifier."""

    def test_post_game_token_in_designed_name_fires_falsifier(
        self, tmp_path: Path
    ) -> None:
        """A designed column name containing 'won' causes failure."""
        csv_path = tmp_path / "registry.csv"
        _write_csv(csv_path, _all_five_tranche_rows())

        # Inject a POST-GAME column name into the designed tuple
        bad_designed = DESIGNED_COLUMN_NAMES + ("focal_won",)

        result = validate_pre_game_feature_materialization(
            csv_path, bad_designed
        )

        assert result.passed is False
        assert result.halting_falsifier == "post_game_token"
        assert any(token == "won" for _, token in result.post_game_token_hits)


# ---------------------------------------------------------------------------
# Test 13: materialized_output_paths always ()
# ---------------------------------------------------------------------------


class TestMaterializedOutputPaths:
    """materialized_output_paths is always () regardless of validation outcome."""

    def test_empty_on_passing_result(self, tmp_path: Path) -> None:
        """Passing result has empty materialized_output_paths."""
        csv_path = tmp_path / "registry.csv"
        _write_csv(csv_path, _all_five_tranche_rows())

        result = validate_pre_game_feature_materialization(
            csv_path, DESIGNED_COLUMN_NAMES
        )

        assert result.materialized_output_paths == ()

    def test_empty_on_failing_result(self, tmp_path: Path) -> None:
        """Failing result also has empty materialized_output_paths."""
        csv_path = tmp_path / "registry.csv"
        # Add an extra family to trigger failure
        rows = _all_five_tranche_rows() + [
            _tranche_row(feature_family_id="sc2egset.pre_game.extra")
        ]
        _write_csv(csv_path, rows)

        result = validate_pre_game_feature_materialization(
            csv_path, DESIGNED_COLUMN_NAMES
        )

        assert result.passed is False
        assert result.materialized_output_paths == ()


# ---------------------------------------------------------------------------
# Test 14: PR #230 leakage JSON vacuity unchanged
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not LEAKAGE_AUDIT_JSON_PATH.exists(),
    reason="PR #230 leakage audit JSON not found on disk",
)
class TestLeakageAuditVacuity:
    """The PR #230 leakage_audit_sc2egset.json remains vacuous (features_audited == [])."""

    def test_features_audited_is_empty(self) -> None:
        """The leakage audit file's features_audited list is still empty."""
        with LEAKAGE_AUDIT_JSON_PATH.open(encoding="utf-8") as fh:
            data = json.load(fh)
        assert data["features_audited"] == [], (
            f"Expected features_audited == [] but got: {data['features_audited']}"
        )

    def test_verdict_is_pass(self) -> None:
        """The leakage audit verdict is still PASS."""
        with LEAKAGE_AUDIT_JSON_PATH.open(encoding="utf-8") as fh:
            data = json.load(fh)
        assert data["verdict"] == "PASS"


# ---------------------------------------------------------------------------
# Test 15: Real registry CSV smoke test
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not REGISTRY_CSV_PATH.exists(),
    reason="Real registry CSV not found on disk",
)
class TestRealRegistryCsvSmoke:
    """Full validation against the real on-disk 02_01_01 registry CSV."""

    def test_passed_is_true(self) -> None:
        """Real registry validates to passed=True."""
        result = validate_pre_game_feature_materialization(
            REGISTRY_CSV_PATH, DESIGNED_COLUMN_NAMES
        )
        assert result.passed is True

    def test_tranche_count_is_five(self) -> None:
        """Real registry has exactly 5 tranche-1 rows."""
        result = validate_pre_game_feature_materialization(
            REGISTRY_CSV_PATH, DESIGNED_COLUMN_NAMES
        )
        assert result.tranche_count == 5

    def test_materialized_output_paths_empty(self) -> None:
        """Real registry result has empty materialized_output_paths."""
        result = validate_pre_game_feature_materialization(
            REGISTRY_CSV_PATH, DESIGNED_COLUMN_NAMES
        )
        assert result.materialized_output_paths == ()

    def test_halting_falsifier_is_none(self) -> None:
        """Real registry has no halting falsifier."""
        result = validate_pre_game_feature_materialization(
            REGISTRY_CSV_PATH, DESIGNED_COLUMN_NAMES
        )
        assert result.halting_falsifier is None


# ---------------------------------------------------------------------------
# Additional: forbidden_skill_column falsifier via designed names
# ---------------------------------------------------------------------------


class TestAdditionalCoverage:
    """Coverage tests for uncovered branches in the validator module."""

    def test_load_pre_game_tranche_rows_file_not_found(
        self, tmp_path: Path
    ) -> None:
        """load_pre_game_tranche_rows raises FileNotFoundError for non-existent path."""
        missing_path = tmp_path / "no_such_registry.csv"

        with pytest.raises(FileNotFoundError):
            load_pre_game_tranche_rows(missing_path)

    def test_is_mmr_missing_family_absent_fires_is_mmr_missing_not_flag(
        self, tmp_path: Path
    ) -> None:
        """IS_MMR_MISSING_FAMILY_ID absent from tranche rows returns False."""
        # Build rows without the is_mmr_missing family
        csv_path = tmp_path / "registry.csv"
        rows_without_mmr = [
            _tranche_row(feature_family_id="sc2egset.pre_game.focal_race_with_opponent_race_pair",
                         source_table_or_event_family="replay_players_raw"),
            _tranche_row(feature_family_id="sc2egset.pre_game.map_type_encoded",
                         source_table_or_event_family="matches_flat"),
        ]
        _write_csv(csv_path, rows_without_mmr)

        loaded = load_pre_game_tranche_rows(csv_path)
        result = _check_is_mmr_missing_is_flag_not_skill(loaded, DESIGNED_COLUMN_NAMES)
        assert result is False

    def test_post_game_token_in_source_field(self, tmp_path: Path) -> None:
        """A POST_GAME token in a registry source field fires post_game_token falsifier."""
        row = PreGameTrancheRow(
            feature_family_id="sc2egset.pre_game.map_type_encoded",
            prediction_setting="pre_game",
            source_table_or_event_family="matches_flat_won_table",  # contains 'won'
            allowed_cutoff_rule="snapshot_at_match_start",
            candidate_leakage_modes="none",
            cold_start_handling="G-CS-1",
            per_player_construction="symmetric",
            status="allowed",
        )
        hits = _check_no_post_game_tokens([row], ())
        assert len(hits) > 0
        tokens = [token for _, token in hits]
        assert "won" in tokens

    def test_unexpected_source_table_fires_falsifier(self, tmp_path: Path) -> None:
        """An unexpected source table fires the unexpected_source_table falsifier."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_five_tranche_rows()
        rows = [
            r if r["feature_family_id"] != "sc2egset.pre_game.map_type_encoded"
            else _tranche_row(
                feature_family_id="sc2egset.pre_game.map_type_encoded",
                source_table_or_event_family="unknown_table_xyz",
            )
            for r in rows
        ]
        _write_csv(csv_path, rows)

        result = validate_pre_game_feature_materialization(
            csv_path, DESIGNED_COLUMN_NAMES
        )

        assert result.passed is False
        assert result.halting_falsifier == "unexpected_source_table"
        assert "sc2egset.pre_game.map_type_encoded" in result.unexpected_source_tables

    def test_forbidden_skill_column_standalone_falsifier(
        self, tmp_path: Path
    ) -> None:
        """A forbidden skill column triggers a failure (may appear as multiple falsifier labels)."""
        csv_path = tmp_path / "registry.csv"
        _write_csv(csv_path, _all_five_tranche_rows())

        # Use 'sigma' which is forbidden but is NOT in approved tokens
        # and is NOT a post-game token
        bad_designed = DESIGNED_COLUMN_NAMES + ("sigma",)

        result = validate_pre_game_feature_materialization(
            csv_path, bad_designed
        )

        assert result.passed is False
        # sigma is a forbidden skill token; it fires is_mmr_missing_not_flag
        # (check #3 in _check_is_mmr_missing_is_flag_not_skill) or
        # forbidden_skill_column in the final priority chain
        assert result.halting_falsifier in (
            "is_mmr_missing_not_flag",
            "forbidden_skill_column",
        )

    def test_provenance_framing_wrong_prediction_setting(
        self, tmp_path: Path
    ) -> None:
        """is_mmr_missing family with wrong prediction_setting fails provenance check."""
        bad_row = PreGameTrancheRow(
            feature_family_id="sc2egset.pre_game.is_mmr_missing_flag",
            prediction_setting="history_enriched_pre_game",  # wrong
            source_table_or_event_family="replay_players_raw",
            allowed_cutoff_rule="snapshot_at_match_start",
            candidate_leakage_modes="none",
            cold_start_handling="G-CS-1",
            per_player_construction="symmetric",
            status="allowed",
        )
        result = _check_is_mmr_missing_is_flag_not_skill([bad_row], DESIGNED_COLUMN_NAMES)
        assert result is False

    def test_provenance_framing_wrong_leakage_modes(self, tmp_path: Path) -> None:
        """is_mmr_missing family with wrong candidate_leakage_modes fails provenance check."""
        bad_row = PreGameTrancheRow(
            feature_family_id="sc2egset.pre_game.is_mmr_missing_flag",
            prediction_setting="pre_game",
            source_table_or_event_family="replay_players_raw",
            allowed_cutoff_rule="snapshot_at_match_start",
            candidate_leakage_modes="some_leakage_mode",  # wrong
            cold_start_handling="G-CS-1",
            per_player_construction="symmetric",
            status="allowed",
        )
        result = _check_is_mmr_missing_is_flag_not_skill([bad_row], DESIGNED_COLUMN_NAMES)
        assert result is False


class TestForbiddenSkillColumnFalsifier:
    """Forbidden skill/rating/MMR-scalar in designed names causes validation failure."""

    @pytest.mark.parametrize(
        "bad_col",
        ["focal_mmr", "opponent_mmr", "mmr_value", "rating", "elo", "skill"],
    )
    def test_forbidden_skill_column_causes_failure(
        self, tmp_path: Path, bad_col: str
    ) -> None:
        """A forbidden skill column in designed_column_names causes failure.

        When a forbidden skill column is added to designed_column_names,
        the validator fires a falsifier. Because _check_is_mmr_missing_is_flag_not_skill
        checks ALL designed columns for forbidden skill scalars (check #3),
        it fires 'is_mmr_missing_not_flag' before the standalone
        'forbidden_skill_column' check runs in the priority chain.
        Both represent the same underlying violation (forbidden skill scalar);
        either is an acceptable outcome.
        """
        csv_path = tmp_path / "registry.csv"
        _write_csv(csv_path, _all_five_tranche_rows())

        # Add a forbidden skill column to the designed tuple
        bad_designed = DESIGNED_COLUMN_NAMES + (bad_col,)

        result = validate_pre_game_feature_materialization(
            csv_path, bad_designed
        )

        assert result.passed is False
        # The forbidden skill column fires either is_mmr_missing_not_flag
        # (from _check_is_mmr_missing_is_flag_not_skill check #3) or
        # forbidden_skill_column (from _check_forbidden_skill_columns).
        # Both indicate a forbidden skill scalar is present.
        assert result.halting_falsifier in (
            "forbidden_skill_column",
            "is_mmr_missing_not_flag",
            "post_game_token",
        )
