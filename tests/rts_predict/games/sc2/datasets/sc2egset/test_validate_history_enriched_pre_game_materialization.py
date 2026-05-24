"""Tests for ``validate_history_enriched_pre_game_materialization`` (scaffold design contract).

Covers the falsifier-priority chain for the 6 tranche-2 history-enriched
pre_game families:
    - 6-family tranche membership (exactly the 6 ids).
    - Missing family rejected.
    - Extra history family beyond the tranche rejected.
    - Pre_game / in_game / blocked family aliasing of a tranche-2 id rejected.
    - Wrong prediction_setting / wrong temporal_anchor rejected.
    - Non-strict cutoff rule rejected (`<=`, `==`, `>=`, empty, wrong literal).
    - Tracker-derived source in a history family rejected (Invariant I3).
    - Asymmetric per_player_construction rejected (Invariant I5).
    - POST-GAME token in designed names rejected (CROSS-02-01 §2.2).
    - Cross-region caveat missing or wrong status rejected.
    - Illegal IN_GAME_HISTORICAL aggregation column rejected (CROSS-02-00 §5.4).
    - Cold-start gate outside {G-CS-2..G-CS-5} rejected.
    - Status outside {allowed, allowed_with_caveat} rejected.
    - materialized_output_paths always ().
    - Stale registry filename raises ValueError.
    - Real registry CSV smoke test (skipif if absent).
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import pytest

from rts_predict.games.sc2.datasets.sc2egset.validate_history_enriched_pre_game_materialization import (  # noqa: E501
    CROSS_REGION_FAMILY_ID,
    EXPECTED_TRANCHE2_COUNT,
    HISTORY_TRANCHE2_FAMILY_IDS,
    IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
    STALE_REGISTRY_FILENAME_FRAGMENT,
    HistoryEnrichedPreGameTrancheRow,
    _check_no_post_game_tokens,
    load_history_enriched_pre_game_tranche_rows,
    validate_history_enriched_pre_game_materialization,
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

# ---------------------------------------------------------------------------
# Standard designed column names (11 tranche-2 representative names)
# ---------------------------------------------------------------------------

DESIGNED_COLUMN_NAMES: tuple[str, ...] = (
    "focal_prior_match_count",
    "opponent_prior_match_count",
    "focal_prior_win_rate",
    "opponent_prior_win_rate",
    "matchup_h2h_count",
    "matchup_h2h_focal_win_rate",
    "focal_reconstructed_rating",
    "opponent_reconstructed_rating",
    "is_cross_region_fragmented",
    "focal_apm_prior_mean",
    "opponent_apm_prior_mean",
)

DESIGNED_IN_GAME_HISTORICAL_COLUMNS: tuple[str, ...] = (
    "APM",
    "SQ",
    "supplyCappedPercent",
    "header_elapsedGameLoops",
)

# Note: the default DESIGNED_COLUMN_NAMES tuple includes column names that
# would trigger the post_game_token check (e.g. "focal_prior_win_rate"
# contains the token "win"; "matchup_h2h_focal_win_rate" contains "win";
# "is_cross_region_fragmented" — fine). For synthetic-CSV tests we use a
# clean tuple that exercises the non-post-game-token path.
CLEAN_DESIGNED_COLUMN_NAMES: tuple[str, ...] = (
    "focal_prior_match_count",
    "opponent_prior_match_count",
    "matchup_h2h_count",
    "focal_reconstructed_rating",
    "opponent_reconstructed_rating",
    "is_cross_region_fragmented",
    "focal_apm_prior_mean",
    "opponent_apm_prior_mean",
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


def _history_tranche_row(**kwargs: Any) -> dict[str, str]:
    """Build a minimal valid tranche-2 history-enriched pre_game registry row.

    Defaults match the on-disk 02_01_01 registry CSV defaults for the history
    tranche: prediction_setting=history_enriched_pre_game,
    source_table_or_event_family=matches_flat, temporal_anchor=details_timeUTC,
    allowed_cutoff_rule=history_time < target_time, candidate_leakage_modes=
    rolling_includes_target_game, cold_start_handling=G-CS-2,
    status=allowed, per_player_construction=symmetric.
    """
    defaults: dict[str, str] = {
        "feature_family_id": (
            "sc2egset.history_enriched_pre_game.focal_player_history"
        ),
        "dataset_tag": "sc2egset",
        "prediction_setting": "history_enriched_pre_game",
        "source_table_or_event_family": "matches_flat",
        "source_grain": "(filename, player_id_worldwide)",
        "model_input_grain": "(focal_match_id, focal_player)",
        "target_grain": "(focal_match_id, focal_player)",
        "temporal_anchor": "details_timeUTC",
        "allowed_cutoff_rule": "history_time < target_time",
        "candidate_leakage_modes": "rolling_includes_target_game",
        "cold_start_handling": "G-CS-2",
        "status": "allowed",
        "per_player_construction": "symmetric",
        "block": "history_enriched_pre_game",
    }
    defaults.update(kwargs)
    return defaults


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    """Write a registry CSV to disk."""
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(_REGISTRY_COLUMNS))
        writer.writeheader()
        writer.writerows(rows)


def _all_six_tranche_rows() -> list[dict[str, str]]:
    """Build the 6 standard tranche-2 history rows (matching on-disk registry)."""
    return [
        _history_tranche_row(
            feature_family_id="sc2egset.history_enriched_pre_game.focal_player_history",
            candidate_leakage_modes="rolling_includes_target_game",
            cold_start_handling="G-CS-2",
        ),
        _history_tranche_row(
            feature_family_id="sc2egset.history_enriched_pre_game.opponent_player_history",
            candidate_leakage_modes="rolling_includes_target_game",
            cold_start_handling="G-CS-2",
        ),
        _history_tranche_row(
            feature_family_id="sc2egset.history_enriched_pre_game.matchup_history_aggregate",
            source_grain="(filename, player_id_worldwide, opponent_player_id_worldwide)",
            candidate_leakage_modes="h2h_includes_target_game",
            cold_start_handling="G-CS-3",
        ),
        _history_tranche_row(
            feature_family_id="sc2egset.history_enriched_pre_game.reconstructed_rating",
            candidate_leakage_modes="rating_uses_target_game_outcome",
            cold_start_handling="G-CS-4",
        ),
        _history_tranche_row(
            feature_family_id=CROSS_REGION_FAMILY_ID,
            candidate_leakage_modes="cross_region_history_drop",
            cold_start_handling="G-CS-5",
            status="allowed_with_caveat",
        ),
        _history_tranche_row(
            feature_family_id="sc2egset.history_enriched_pre_game.in_game_history_aggregate",
            candidate_leakage_modes="rolling_includes_target_game",
            cold_start_handling="G-CS-2",
        ),
    ]


# ---------------------------------------------------------------------------
# Test 1: Exact 6-family tranche membership
# ---------------------------------------------------------------------------


class TestExactTrancheMembership:
    """Exactly 6 tranche-2 families are loaded from a synthetic CSV."""

    def test_six_family_ids_loaded(self, tmp_path: Path) -> None:
        """All 6 HISTORY_TRANCHE2_FAMILY_IDS are loaded; no extras, no missing."""
        csv_path = tmp_path / "registry.csv"
        _write_csv(csv_path, _all_six_tranche_rows())

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.tranche_count == EXPECTED_TRANCHE2_COUNT
        assert set(result.tranche_family_ids) == HISTORY_TRANCHE2_FAMILY_IDS
        assert result.missing_families_in_tranche == ()
        assert result.extra_history_in_tranche == ()

    def test_passed_is_true_with_six_rows(self, tmp_path: Path) -> None:
        """Validation passes with exactly the 6 tranche-2 rows."""
        csv_path = tmp_path / "registry.csv"
        _write_csv(csv_path, _all_six_tranche_rows())

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is True
        assert result.halting_falsifier is None
        assert result.cross_region_caveat_ok is True


# ---------------------------------------------------------------------------
# Test 2: Missing family fires missing_families_in_tranche
# ---------------------------------------------------------------------------


class TestMissingFamilyInTranche:
    """Removing one of the 6 expected families fires missing_families_in_tranche."""

    @pytest.mark.parametrize(
        "missing_fid",
        [
            "sc2egset.history_enriched_pre_game.focal_player_history",
            "sc2egset.history_enriched_pre_game.opponent_player_history",
            "sc2egset.history_enriched_pre_game.matchup_history_aggregate",
            "sc2egset.history_enriched_pre_game.reconstructed_rating",
            "sc2egset.history_enriched_pre_game.in_game_history_aggregate",
        ],
    )
    def test_missing_family_fires_falsifier(
        self, tmp_path: Path, missing_fid: str
    ) -> None:
        """Removing any expected family (other than cross_region) halts validation."""
        csv_path = tmp_path / "registry.csv"
        rows = [
            r for r in _all_six_tranche_rows() if r["feature_family_id"] != missing_fid
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "missing_families_in_tranche"
        assert missing_fid in result.missing_families_in_tranche


# ---------------------------------------------------------------------------
# Test 3: Extra history family rejected
# ---------------------------------------------------------------------------


class TestExtraHistoryInTranche:
    """A 7th history family outside the tranche fires extra_history_in_tranche."""

    def test_extra_history_family_fires_falsifier(self, tmp_path: Path) -> None:
        """Adding a 7th history row outside the tranche causes failure."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows() + [
            _history_tranche_row(
                feature_family_id="sc2egset.history_enriched_pre_game.extra_unknown",
            )
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "extra_history_in_tranche"
        assert (
            "sc2egset.history_enriched_pre_game.extra_unknown"
            in result.extra_history_in_tranche
        )


# ---------------------------------------------------------------------------
# Test 4: Pre-game alias of a tranche-2 id rejected
# ---------------------------------------------------------------------------


class TestPreGameAliasInTrancheRejected:
    """A pre_game row using a tranche-2 family_id fires pre_game_in_history_tranche."""

    def test_pre_game_alias_fires_falsifier(self, tmp_path: Path) -> None:
        """A pre_game row aliasing a tranche-2 id causes failure."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows() + [
            _history_tranche_row(
                feature_family_id="sc2egset.history_enriched_pre_game.focal_player_history",
                prediction_setting="pre_game",
                allowed_cutoff_rule="snapshot_at_match_start",
                cold_start_handling="G-CS-1",
            )
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "pre_game_in_history_tranche"
        assert (
            "sc2egset.history_enriched_pre_game.focal_player_history"
            in result.pre_game_aliases_in_tranche
        )


# ---------------------------------------------------------------------------
# Test 5: In-game snapshot alias of a tranche-2 id rejected
# ---------------------------------------------------------------------------


class TestInGameSnapshotAliasInTrancheRejected:
    """An in_game_snapshot row using a tranche-2 family_id fires in_game_in_history_tranche."""

    def test_in_game_alias_fires_falsifier(self, tmp_path: Path) -> None:
        """An in_game_snapshot row aliasing a tranche-2 id causes failure."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows() + [
            _history_tranche_row(
                feature_family_id="sc2egset.history_enriched_pre_game.opponent_player_history",
                prediction_setting="in_game_snapshot",
                allowed_cutoff_rule="event.loop <= cutoff_loop",
            )
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "in_game_in_history_tranche"
        assert (
            "sc2egset.history_enriched_pre_game.opponent_player_history"
            in result.in_game_aliases_in_tranche
        )


# ---------------------------------------------------------------------------
# Test 6: Blocked alias of a tranche-2 id rejected
# ---------------------------------------------------------------------------


class TestBlockedAliasInTrancheRejected:
    """A blocked_or_deferred row using a tranche-2 family_id fires blocked_in_history_tranche."""

    def test_blocked_alias_fires_falsifier(self, tmp_path: Path) -> None:
        """A blocked_or_deferred row aliasing a tranche-2 id causes failure."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows() + [
            _history_tranche_row(
                feature_family_id="sc2egset.history_enriched_pre_game.matchup_history_aggregate",
                prediction_setting="blocked_or_deferred",
                allowed_cutoff_rule="blocked",
                cold_start_handling="blocked",
                status="blocked_until_additional_validation",
            )
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "blocked_in_history_tranche"
        assert (
            "sc2egset.history_enriched_pre_game.matchup_history_aggregate"
            in result.blocked_aliases_in_tranche
        )


# ---------------------------------------------------------------------------
# Test 7: Wrong prediction_setting rejected
# ---------------------------------------------------------------------------


class TestWrongPredictionSettingRejected:
    """A tranche row with prediction_setting != history_enriched_pre_game halts.

    Note: this exercises the per-row content check (post structural/aliasing).
    To avoid hitting the pre_game/in_game/blocked aliasing falsifier first,
    we use a non-recognised prediction_setting label.
    """

    def test_wrong_prediction_setting_fires_falsifier(self, tmp_path: Path) -> None:
        """Flipping one row's prediction_setting to an unknown label fails."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows()
        rows = [
            r
            if r["feature_family_id"]
            != "sc2egset.history_enriched_pre_game.focal_player_history"
            else _history_tranche_row(
                feature_family_id="sc2egset.history_enriched_pre_game.focal_player_history",
                prediction_setting="unknown_setting_label",
            )
            for r in rows
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "wrong_prediction_setting"
        assert (
            "sc2egset.history_enriched_pre_game.focal_player_history"
            in result.wrong_prediction_setting_rows
        )


# ---------------------------------------------------------------------------
# Test 8: Wrong temporal_anchor rejected
# ---------------------------------------------------------------------------


class TestWrongTemporalAnchorRejected:
    """A tranche row with temporal_anchor != details_timeUTC halts validation."""

    def test_wrong_temporal_anchor_fires_falsifier(self, tmp_path: Path) -> None:
        """Flipping one row's temporal_anchor to 'started_at' causes failure."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows()
        rows = [
            r
            if r["feature_family_id"]
            != "sc2egset.history_enriched_pre_game.reconstructed_rating"
            else _history_tranche_row(
                feature_family_id="sc2egset.history_enriched_pre_game.reconstructed_rating",
                temporal_anchor="started_at",
                cold_start_handling="G-CS-4",
                candidate_leakage_modes="rating_uses_target_game_outcome",
            )
            for r in rows
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "wrong_temporal_anchor"


# ---------------------------------------------------------------------------
# Test 9: Non-strict cutoff rule rejected (parametrized)
# ---------------------------------------------------------------------------


class TestCutoffNotStrictRejected:
    """A cutoff rule other than 'history_time < target_time' halts validation."""

    @pytest.mark.parametrize(
        "bad_rule",
        [
            "history_time <= target_time",
            "history_time == target_time",
            "history_time >= target_time",
            "",
            "snapshot_at_match_start",
        ],
    )
    def test_non_strict_cutoff_fires_falsifier(
        self, tmp_path: Path, bad_rule: str
    ) -> None:
        """Setting a non-strict cutoff rule on one row halts validation."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows()
        rows = [
            r
            if r["feature_family_id"]
            != "sc2egset.history_enriched_pre_game.matchup_history_aggregate"
            else _history_tranche_row(
                feature_family_id="sc2egset.history_enriched_pre_game.matchup_history_aggregate",
                allowed_cutoff_rule=bad_rule,
                cold_start_handling="G-CS-3",
                candidate_leakage_modes="h2h_includes_target_game",
            )
            for r in rows
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "cutoff_not_strict"


# ---------------------------------------------------------------------------
# Test 10: Tracker source in history rejected (Invariant I3)
# ---------------------------------------------------------------------------


class TestTrackerSourceInHistoryRejected:
    """A tranche row with tracker_events_raw source fires tracker_source_in_history."""

    def test_tracker_source_fires_falsifier(self, tmp_path: Path) -> None:
        """One tranche row with tracker source causes failure."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows()
        rows = [
            r
            if r["feature_family_id"]
            != "sc2egset.history_enriched_pre_game.in_game_history_aggregate"
            else _history_tranche_row(
                feature_family_id="sc2egset.history_enriched_pre_game.in_game_history_aggregate",
                source_table_or_event_family="tracker_events_raw.PlayerStats",
            )
            for r in rows
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "tracker_source_in_history"
        assert (
            "sc2egset.history_enriched_pre_game.in_game_history_aggregate"
            in result.tracker_source_in_history
        )


# ---------------------------------------------------------------------------
# Test 11: Asymmetric construction rejected (Invariant I5)
# ---------------------------------------------------------------------------


class TestAsymmetricConstructionRejected:
    """A tranche row with asymmetric per_player_construction halts validation."""

    def test_asymmetric_fires_falsifier(self, tmp_path: Path) -> None:
        """Setting one row's per_player_construction to 'asymmetric' fails."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows()
        rows = [
            r
            if r["feature_family_id"]
            != "sc2egset.history_enriched_pre_game.opponent_player_history"
            else _history_tranche_row(
                feature_family_id="sc2egset.history_enriched_pre_game.opponent_player_history",
                per_player_construction="asymmetric",
            )
            for r in rows
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "asymmetric_construction"
        assert (
            "sc2egset.history_enriched_pre_game.opponent_player_history"
            in result.asymmetric_construction
        )


# ---------------------------------------------------------------------------
# Test 12: POST-GAME token in designed names rejected (CROSS-02-01 §2.2)
# ---------------------------------------------------------------------------


class TestPostGameTokenRejected:
    """A POST-GAME token in a designed column name fires post_game_token."""

    def test_post_game_token_in_designed_name_fires_falsifier(
        self, tmp_path: Path
    ) -> None:
        """A designed column name containing 'won' causes failure."""
        csv_path = tmp_path / "registry.csv"
        _write_csv(csv_path, _all_six_tranche_rows())

        bad_designed = CLEAN_DESIGNED_COLUMN_NAMES + ("focal_won",)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            bad_designed,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "post_game_token"
        assert any(token == "won" for _, token in result.post_game_token_hits)


# ---------------------------------------------------------------------------
# Test 13: Cross-region caveat missing (N3 — deterministic priority test)
# ---------------------------------------------------------------------------


class TestCrossRegionCaveatMissing:
    """Cross-region row absent OR status not 'allowed_with_caveat' halts validation.

    Two sub-cases enforce the priority chain:
    1. Row removed entirely: priority-1 'missing_families_in_tranche' fires first
       (deterministic — wins over priority-13 'cross_region_caveat_missing').
    2. Row kept but status flipped to 'allowed': the dedicated
       'cross_region_caveat_missing' falsifier fires.
    """

    def test_removed_row_fires_missing_families_first(self, tmp_path: Path) -> None:
        """Removing the cross_region row fires the priority-1 missing falsifier."""
        csv_path = tmp_path / "registry.csv"
        rows = [
            r
            for r in _all_six_tranche_rows()
            if r["feature_family_id"] != CROSS_REGION_FAMILY_ID
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        # Deterministic: priority-1 missing fires before priority-13 cross_region
        assert result.halting_falsifier == "missing_families_in_tranche"
        assert CROSS_REGION_FAMILY_ID in result.missing_families_in_tranche
        # Cross-region status check independently fails (row absent)
        assert result.cross_region_caveat_ok is False

    def test_status_flipped_to_allowed_fires_cross_region_caveat(
        self, tmp_path: Path
    ) -> None:
        """Keeping the row but flipping status to 'allowed' fires the dedicated falsifier."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows()
        rows = [
            r
            if r["feature_family_id"] != CROSS_REGION_FAMILY_ID
            else _history_tranche_row(
                feature_family_id=CROSS_REGION_FAMILY_ID,
                candidate_leakage_modes="cross_region_history_drop",
                cold_start_handling="G-CS-5",
                status="allowed",  # flipped from allowed_with_caveat
            )
            for r in rows
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "cross_region_caveat_missing"
        assert result.cross_region_caveat_ok is False


# ---------------------------------------------------------------------------
# Test 14: Illegal IN_GAME_HISTORICAL column rejected (CROSS-02-00 §5.4)
# ---------------------------------------------------------------------------


class TestInGameHistoricalOutOfScopeRejected:
    """A designed IN_GAME_HISTORICAL column outside §5.4 retained set halts validation."""

    def test_out_of_scope_column_fires_falsifier(self, tmp_path: Path) -> None:
        """Adding 'foo_random_metric' to the designed IN_GAME_HISTORICAL tuple fails."""
        csv_path = tmp_path / "registry.csv"
        _write_csv(csv_path, _all_six_tranche_rows())

        bad_in_game_historical = DESIGNED_IN_GAME_HISTORICAL_COLUMNS + (
            "foo_random_metric",
        )

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            bad_in_game_historical,
        )

        assert result.passed is False
        assert (
            result.halting_falsifier == "in_game_historical_column_out_of_scope"
        )
        assert "foo_random_metric" in result.in_game_historical_out_of_scope


# ---------------------------------------------------------------------------
# Test 15: Cold-start gate outside {G-CS-2..G-CS-5} rejected
# ---------------------------------------------------------------------------


class TestColdStartGateInvalidRejected:
    """A cold_start_handling not in {G-CS-2..G-CS-5} fires cold_start_gate_invalid."""

    def test_g_cs_1_rejected(self, tmp_path: Path) -> None:
        """G-CS-1 (the pre_game gate) is invalid for the history tranche."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows()
        rows = [
            r
            if r["feature_family_id"]
            != "sc2egset.history_enriched_pre_game.focal_player_history"
            else _history_tranche_row(
                feature_family_id="sc2egset.history_enriched_pre_game.focal_player_history",
                cold_start_handling="G-CS-1",
            )
            for r in rows
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "cold_start_gate_invalid"
        assert any(
            fid == "sc2egset.history_enriched_pre_game.focal_player_history"
            for fid, _ in result.cold_start_gate_violations
        )

    def test_g_cs_6_rejected(self, tmp_path: Path) -> None:
        """G-CS-6 (the materialization-time fold-aware fit gate) is invalid at registry."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows()
        rows = [
            r
            if r["feature_family_id"]
            != "sc2egset.history_enriched_pre_game.matchup_history_aggregate"
            else _history_tranche_row(
                feature_family_id="sc2egset.history_enriched_pre_game.matchup_history_aggregate",
                cold_start_handling="G-CS-6",
                candidate_leakage_modes="h2h_includes_target_game",
            )
            for r in rows
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "cold_start_gate_invalid"


# ---------------------------------------------------------------------------
# Test 16: Status not in {allowed, allowed_with_caveat} rejected
# ---------------------------------------------------------------------------


class TestStatusNotAdmissibleRejected:
    """A status outside {allowed, allowed_with_caveat} fires status_not_admissible."""

    def test_blocked_status_fires_falsifier(self, tmp_path: Path) -> None:
        """Flipping one row's status to 'blocked_until_validation' fails."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows()
        rows = [
            r
            if r["feature_family_id"]
            != "sc2egset.history_enriched_pre_game.in_game_history_aggregate"
            else _history_tranche_row(
                feature_family_id="sc2egset.history_enriched_pre_game.in_game_history_aggregate",
                status="blocked_until_validation",
            )
            for r in rows
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.halting_falsifier == "status_not_admissible"


# ---------------------------------------------------------------------------
# Test 17: Stale registry filename raises
# ---------------------------------------------------------------------------


class TestStaleRegistryFilenameRaises:
    """load_history_enriched_pre_game_tranche_rows raises for the stale filename."""

    def test_stale_path_raises_value_error(self, tmp_path: Path) -> None:
        """A path containing the stale fragment raises ValueError."""
        stale_path = tmp_path / "02_01_01_feature_family_registry_sc2egset.csv"
        assert STALE_REGISTRY_FILENAME_FRAGMENT in str(stale_path)

        with pytest.raises(ValueError, match="Stale registry path"):
            load_history_enriched_pre_game_tranche_rows(stale_path)


# ---------------------------------------------------------------------------
# Test 18: materialized_output_paths always ()
# ---------------------------------------------------------------------------


class TestMaterializedOutputPathsAlwaysEmpty:
    """materialized_output_paths is always () regardless of validation outcome."""

    def test_empty_on_passing_result(self, tmp_path: Path) -> None:
        """Passing result has empty materialized_output_paths."""
        csv_path = tmp_path / "registry.csv"
        _write_csv(csv_path, _all_six_tranche_rows())

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.materialized_output_paths == ()

    def test_empty_on_failing_result(self, tmp_path: Path) -> None:
        """Failing result also has empty materialized_output_paths."""
        csv_path = tmp_path / "registry.csv"
        rows = _all_six_tranche_rows() + [
            _history_tranche_row(
                feature_family_id="sc2egset.history_enriched_pre_game.extra"
            )
        ]
        _write_csv(csv_path, rows)

        result = validate_history_enriched_pre_game_materialization(
            csv_path,
            CLEAN_DESIGNED_COLUMN_NAMES,
            DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
        )

        assert result.passed is False
        assert result.materialized_output_paths == ()


# ---------------------------------------------------------------------------
# Test 19: Real registry CSV smoke test
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not REGISTRY_CSV_PATH.exists(),
    reason="Real registry CSV not found on disk",
)
class TestRealRegistryCsvSmoke:
    """Full validation against the real on-disk 02_01_01 registry CSV."""

    def test_passed_is_true_on_real_registry(self) -> None:
        """Real registry validates to passed=True with clean designed names."""
        result = validate_history_enriched_pre_game_materialization(
            REGISTRY_CSV_PATH,
            CLEAN_DESIGNED_COLUMN_NAMES,
            IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
        )
        assert result.passed is True

    def test_tranche_count_is_six(self) -> None:
        """Real registry has exactly 6 tranche-2 rows."""
        result = validate_history_enriched_pre_game_materialization(
            REGISTRY_CSV_PATH,
            CLEAN_DESIGNED_COLUMN_NAMES,
            IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
        )
        assert result.tranche_count == 6

    def test_halting_falsifier_is_none(self) -> None:
        """Real registry has no halting falsifier."""
        result = validate_history_enriched_pre_game_materialization(
            REGISTRY_CSV_PATH,
            CLEAN_DESIGNED_COLUMN_NAMES,
            IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
        )
        assert result.halting_falsifier is None

    def test_missing_families_empty(self) -> None:
        """Real registry has no missing expected tranche-2 families."""
        result = validate_history_enriched_pre_game_materialization(
            REGISTRY_CSV_PATH,
            CLEAN_DESIGNED_COLUMN_NAMES,
            IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
        )
        assert result.missing_families_in_tranche == ()

    def test_materialized_output_paths_empty(self) -> None:
        """Real registry result has empty materialized_output_paths."""
        result = validate_history_enriched_pre_game_materialization(
            REGISTRY_CSV_PATH,
            CLEAN_DESIGNED_COLUMN_NAMES,
            IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
        )
        assert result.materialized_output_paths == ()

    def test_cross_region_status_is_allowed_with_caveat(self) -> None:
        """Real registry's cross_region row has status='allowed_with_caveat'."""
        result = validate_history_enriched_pre_game_materialization(
            REGISTRY_CSV_PATH,
            CLEAN_DESIGNED_COLUMN_NAMES,
            IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
        )
        assert result.cross_region_caveat_ok is True

    def test_six_family_ids_match_expected_frozenset(self) -> None:
        """Real registry's 6 family IDs match HISTORY_TRANCHE2_FAMILY_IDS exactly."""
        result = validate_history_enriched_pre_game_materialization(
            REGISTRY_CSV_PATH,
            CLEAN_DESIGNED_COLUMN_NAMES,
            IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
        )
        assert set(result.tranche_family_ids) == HISTORY_TRANCHE2_FAMILY_IDS


# ---------------------------------------------------------------------------
# Test 20: Additional coverage
# ---------------------------------------------------------------------------


class TestAdditionalCoverage:
    """Coverage tests for uncovered branches and edge cases."""

    def test_load_history_tranche_rows_file_not_found(
        self, tmp_path: Path
    ) -> None:
        """load_history_enriched_pre_game_tranche_rows raises FileNotFoundError."""
        missing_path = tmp_path / "no_such_registry.csv"

        with pytest.raises(FileNotFoundError):
            load_history_enriched_pre_game_tranche_rows(missing_path)

    def test_post_game_token_in_source_field(self) -> None:
        """A POST_GAME token in a registry source field fires post_game_token."""
        row = HistoryEnrichedPreGameTrancheRow(
            feature_family_id="sc2egset.history_enriched_pre_game.focal_player_history",
            prediction_setting="history_enriched_pre_game",
            source_table_or_event_family="matches_flat_won_table",
            temporal_anchor="details_timeUTC",
            allowed_cutoff_rule="history_time < target_time",
            candidate_leakage_modes="rolling_includes_target_game",
            cold_start_handling="G-CS-2",
            status="allowed",
            per_player_construction="symmetric",
        )
        hits = _check_no_post_game_tokens([row], ())
        assert len(hits) > 0
        tokens = [token for _, token in hits]
        assert "won" in tokens
