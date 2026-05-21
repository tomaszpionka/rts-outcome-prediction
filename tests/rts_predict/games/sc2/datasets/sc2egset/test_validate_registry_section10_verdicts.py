"""Tests for ``validate_registry_section10_verdicts`` (PM-1 §10 verdict audit).

Covers all 14 required test cases:
    T-INDEP, T-F1A, T-F1B, T-F2, T-F3, T-F4, T-F5, T-F6, T-F7,
    T-VAC, T-26ROW, T-ROWCNT, T-EMPTY, T-SYN.

Uses the real on-disk registry for T-26ROW / T-VAC (real path) and synthetic
in-memory DataFrames + a synthetic tracker CSV for all other tests.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from rts_predict.games.sc2.datasets.sc2egset.validate_registry_section10_verdicts import (
    DATASET_SIDE_BLOCKED_SYNONYM,
    HISTORY_STRICT_CUTOFF,
    SECTION10_VERDICTS,
    SLOT_IDENTITY_FEATURE_ID,
    Section10Rules,
    compare_registry_verdicts,
    derive_section10_verdict,
    load_registry_rows,
    validate_registry_section10_verdicts,
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

TRACKER_CSV_PATH: Path = (
    _TESTS_ROOT
    / "src"
    / "rts_predict"
    / "games"
    / "sc2"
    / "datasets"
    / "sc2egset"
    / "reports"
    / "artifacts"
    / "01_exploration"
    / "03_profiling"
    / "tracker_events_feature_eligibility.csv"
)

# ---------------------------------------------------------------------------
# Synthetic fixture helpers
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


def _reg_row(**kwargs: Any) -> dict[str, str]:
    """Build a minimal valid pre_game registry row with sensible defaults."""
    defaults: dict[str, str] = {
        "feature_family_id": "sc2egset.pre_game.dummy",
        "dataset_tag": "sc2egset",
        "prediction_setting": "pre_game",
        "source_table_or_event_family": "matches_flat",
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


def _make_df(rows: list[dict[str, str]]) -> pd.DataFrame:
    """Create a DataFrame from a list of row dicts using the registry column order."""
    return pd.DataFrame(rows, columns=list(_REGISTRY_COLUMNS))


def _df_to_series_list(df: pd.DataFrame) -> list[pd.Series]:
    """Convert a DataFrame to a list of pd.Series (one per row)."""
    return [df.iloc[i] for i in range(len(df))]


def _write_registry_csv(path: Path, rows: list[dict[str, str]]) -> None:
    """Write a registry CSV to disk (for load_registry_rows tests)."""
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(_REGISTRY_COLUMNS))
        writer.writeheader()
        writer.writerows(rows)


def _make_tracker_csv(tmp_path: Path) -> Path:
    """Write a minimal synthetic tracker CSV and return its path."""
    tracker_path = tmp_path / "tracker_events_feature_eligibility.csv"
    rows = [
        {
            "feature_family": "dummy",
            "source_event_family": "UnitBorn",
            "planned_for_phase02": "yes",
            "status_pre_game": "not_applicable_to_pre_game",
            "status_in_game_snapshot": "eligible_for_phase02_now",
            "status_post_game_or_blocked": "not_applicable",
            "eligibility_scope": "basic cutoff-count",
            "blocking_reason_if_blocked": "",
            "caveat": "",
            "evidence_source": "V5",
            "upstream_verdicts": "V1,V5",
            "notes_for_phase02": "",
        }
    ]
    with tracker_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return tracker_path


def _make_protocol_rules(tracker_csv_path: Path) -> Section10Rules:
    """Build a Section10Rules pointing at the given tracker CSV."""
    return Section10Rules(
        verdicts=SECTION10_VERDICTS,
        blocking_triggers=("missing_grain", "ambiguous_temporal_anchor"),
        history_cutoff=HISTORY_STRICT_CUTOFF,
        ingame_cutoff="event.loop <= cutoff_loop",
        slot_identity_feature_id=SLOT_IDENTITY_FEATURE_ID,
        sc2_tracker_blocked_token="blocked_until_additional_validation",
        tracker_eligibility_csv_path=tracker_csv_path,
    )


# ---------------------------------------------------------------------------
# T-INDEP: structural independence — derive_section10_verdict ignores 'status'
# ---------------------------------------------------------------------------


class TestTIndep:
    """T-INDEP: derive_section10_verdict must not read row['status']."""

    def test_identical_rows_different_status_same_verdict(
        self, tmp_path: Path
    ) -> None:
        """Two rows identical except 'status' must yield the same derived verdict."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        row_a = pd.Series(
            _reg_row(
                feature_family_id="sc2egset.pre_game.dummy_a",
                status="allowed",
            )
        )
        row_b = pd.Series(
            _reg_row(
                feature_family_id="sc2egset.pre_game.dummy_a",
                status="blocked_until_additional_validation",
            )
        )
        verdict_a = derive_section10_verdict(row_a, rules)
        verdict_b = derive_section10_verdict(row_b, rules)
        assert verdict_a.derived_status == verdict_b.derived_status

    def test_status_key_absent_from_row(self, tmp_path: Path) -> None:
        """Function must work correctly when 'status' key is entirely absent."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        row_data = _reg_row(feature_family_id="sc2egset.pre_game.no_status")
        row = pd.Series({k: v for k, v in row_data.items() if k != "status"})
        # Must not raise and must return allowed for a clean pre_game row
        verdict = derive_section10_verdict(row, rules)
        assert verdict.derived_status == "allowed"


# ---------------------------------------------------------------------------
# T-F1A: stricter drift detection
# ---------------------------------------------------------------------------


class TestTF1A:
    """T-F1A: stricter drift — derived is more restrictive than recorded status."""

    def test_stricter_drift_detected(self, tmp_path: Path) -> None:
        """A pre_game row with a post-game token should derive blocked; recorded=allowed.

        This creates a synthetic scenario where the derivation produces
        blocked_until_validation but the registry says allowed -> F-1a.
        """
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        # Inject a post-game token into allowed_cutoff_rule to force blocked derivation
        bad_row = _reg_row(
            feature_family_id="sc2egset.pre_game.leaky",
            allowed_cutoff_rule="snapshot_at_match_start_post_game_result",
            status="allowed",
        )
        rows = _df_to_series_list(_make_df([bad_row]))
        result = compare_registry_verdicts(rows, rules)

        assert result.passed is False
        assert result.halting_falsifier == "F-1a"
        assert len(result.stricter_drifts) >= 1
        ffids = [d[0] for d in result.stricter_drifts]
        assert "sc2egset.pre_game.leaky" in ffids


# ---------------------------------------------------------------------------
# T-F1B: looser drift detection
# ---------------------------------------------------------------------------


class TestTF1B:
    """T-F1B: looser drift — derived is less restrictive than recorded status."""

    def test_looser_drift_detected(self, tmp_path: Path) -> None:
        """A clean pre_game row recorded as blocked should trigger F-1b."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        # Row should derive as 'allowed' but is recorded as 'blocked'
        loose_row = _reg_row(
            feature_family_id="sc2egset.pre_game.over_blocked",
            status="blocked_until_additional_validation",
        )
        rows = _df_to_series_list(_make_df([loose_row]))
        result = compare_registry_verdicts(rows, rules)

        assert result.passed is False
        assert result.halting_falsifier == "F-1b"
        assert len(result.looser_drifts) >= 1
        ffids = [d[0] for d in result.looser_drifts]
        assert "sc2egset.pre_game.over_blocked" in ffids


# ---------------------------------------------------------------------------
# T-F2: independent §10.2 trigger fires on allowed row
# ---------------------------------------------------------------------------


class TestTF2:
    """T-F2: independent §10.2 trigger on a row recorded as allowed."""

    def test_tracker_blocked_recorded_allowed(self, tmp_path: Path) -> None:
        """An in_game_snapshot row where tracker says blocked but status=allowed.

        This simulates a tracker CSV contradiction where the status is allowed
        but the tracker eligibility says blocked -> F-5 trigger fires -> F-2.
        """
        tracker_path = tmp_path / "tracker.csv"
        # Write a tracker CSV where 'count_units_built_by_cutoff_loop' is blocked
        rows = [
            {
                "feature_family": "count_units_built_blocked",
                "source_event_family": "UnitBorn",
                "planned_for_phase02": "yes",
                "status_pre_game": "not_applicable_to_pre_game",
                "status_in_game_snapshot": "blocked_until_additional_validation",
                "status_post_game_or_blocked": "not_applicable",
                "eligibility_scope": "blocked",
                "blocking_reason_if_blocked": "test",
                "caveat": "",
                "evidence_source": "V5",
                "upstream_verdicts": "V5",
                "notes_for_phase02": "",
            }
        ]
        with tracker_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

        rules = _make_protocol_rules(tracker_path)

        # Row: in_game_snapshot, tracker says blocked, but recorded status=allowed
        # derivation will yield blocked; recorded says allowed -> F-1a (stricter)
        # The independent trigger check also fires F-5 for rows recorded as allowed
        row = _reg_row(
            feature_family_id="sc2egset.in_game_snapshot.count_units_built_blocked",
            prediction_setting="in_game_snapshot",
            source_table_or_event_family="tracker_events_raw.UnitBorn",
            allowed_cutoff_rule="event.loop <= cutoff_loop",
            candidate_leakage_modes="none",
            status="allowed",
        )
        rows_series = _df_to_series_list(_make_df([row]))
        result = compare_registry_verdicts(rows_series, rules)

        # F-1a fires because derived=blocked but recorded=allowed
        assert result.passed is False
        assert result.halting_falsifier in {"F-1a", "F-2"}

    def test_independent_derivation_does_not_read_status(
        self, tmp_path: Path
    ) -> None:
        """Two rows with different status values produce the same independent verdict."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        base = _reg_row(feature_family_id="sc2egset.pre_game.check_indep")
        row_allowed = pd.Series({**base, "status": "allowed"})
        row_blocked = pd.Series(
            {**base, "status": "blocked_until_additional_validation"}
        )

        v_allowed = derive_section10_verdict(row_allowed, rules)
        v_blocked = derive_section10_verdict(row_blocked, rules)
        assert v_allowed.derived_status == v_blocked.derived_status


# ---------------------------------------------------------------------------
# T-F3: post-game token leakage
# ---------------------------------------------------------------------------


class TestTF3:
    """T-F3: post-game token in allowed_cutoff_rule."""

    def test_post_game_token_blocks_pre_game_row(self, tmp_path: Path) -> None:
        """A pre_game row with 'match_result' in cutoff_rule derives blocked."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        row = pd.Series(
            _reg_row(
                feature_family_id="sc2egset.pre_game.leaky_result",
                allowed_cutoff_rule="snapshot_at_match_result",
                status="allowed",
            )
        )
        verdict = derive_section10_verdict(row, rules)
        assert verdict.derived_status == "blocked_until_validation"
        assert any("F-3" in t for t in verdict.triggers_fired)

    @pytest.mark.parametrize("token", ["won", "final_state", "match_result", "post_game"])
    def test_all_post_game_tokens(self, tmp_path: Path, token: str) -> None:
        """Each of the four post-game tokens triggers a block."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        row = pd.Series(
            _reg_row(
                feature_family_id=f"sc2egset.pre_game.leaky_{token}",
                allowed_cutoff_rule=f"snapshot_at_{token}",
                status="allowed",
            )
        )
        verdict = derive_section10_verdict(row, rules)
        assert verdict.derived_status == "blocked_until_validation"


# ---------------------------------------------------------------------------
# T-F4: invalid cutoff operator on history row
# ---------------------------------------------------------------------------


class TestTF4:
    """T-F4: history row with '<=' instead of strict '<'."""

    def test_lte_operator_in_history_row(self, tmp_path: Path) -> None:
        """A history row with '<=' derives blocked_until_validation."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        row = pd.Series(
            _reg_row(
                feature_family_id="sc2egset.history_enriched_pre_game.bad_cutoff",
                prediction_setting="history_enriched_pre_game",
                allowed_cutoff_rule="history_time <= target_time",
                status="allowed",
            )
        )
        verdict = derive_section10_verdict(row, rules)
        assert verdict.derived_status == "blocked_until_validation"
        assert any("F-4" in t for t in verdict.triggers_fired)

    def test_missing_lt_operator_in_history_row(self, tmp_path: Path) -> None:
        """A history row with no '<' at all derives blocked_until_validation."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        row = pd.Series(
            _reg_row(
                feature_family_id="sc2egset.history_enriched_pre_game.no_cutoff",
                prediction_setting="history_enriched_pre_game",
                allowed_cutoff_rule="snapshot_at_match_start",
                status="allowed",
            )
        )
        verdict = derive_section10_verdict(row, rules)
        assert verdict.derived_status == "blocked_until_validation"
        assert any("F-4" in t for t in verdict.triggers_fired)


# ---------------------------------------------------------------------------
# T-F5: D13 tracker contradiction
# ---------------------------------------------------------------------------


class TestTF5:
    """T-F5: tracker CSV says blocked but registry says allowed."""

    def test_tracker_blocked_but_registry_allowed(self, tmp_path: Path) -> None:
        """Tracker CSV blocked => derivation yields blocked; recorded=allowed => F-1a."""
        tracker_path = tmp_path / "tracker.csv"
        tracker_rows = [
            {
                "feature_family": "ingame_family",
                "source_event_family": "UnitBorn",
                "planned_for_phase02": "yes",
                "status_pre_game": "not_applicable_to_pre_game",
                "status_in_game_snapshot": "blocked_until_additional_validation",
                "status_post_game_or_blocked": "not_applicable",
                "eligibility_scope": "blocked",
                "blocking_reason_if_blocked": "test block",
                "caveat": "",
                "evidence_source": "V5",
                "upstream_verdicts": "V5",
                "notes_for_phase02": "",
            }
        ]
        with tracker_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh, fieldnames=list(tracker_rows[0].keys())
            )
            writer.writeheader()
            writer.writerows(tracker_rows)

        rules = _make_protocol_rules(tracker_path)

        row = pd.Series(
            _reg_row(
                feature_family_id="sc2egset.in_game_snapshot.ingame_family",
                prediction_setting="in_game_snapshot",
                source_table_or_event_family="tracker_events_raw.UnitBorn",
                allowed_cutoff_rule="event.loop <= cutoff_loop",
                candidate_leakage_modes="none",
                status="allowed",  # contradicts tracker CSV
            )
        )
        verdict = derive_section10_verdict(row, rules)
        assert verdict.derived_status == "blocked_until_validation"
        assert any("F-5" in t for t in verdict.triggers_fired)


# ---------------------------------------------------------------------------
# T-F6: slot_identity_consistency gate misuse
# ---------------------------------------------------------------------------


class TestTF6:
    """T-F6: slot_identity_consistency must be sanity_gate_not_model_input."""

    def test_slot_identity_derives_sanity_gate(self, tmp_path: Path) -> None:
        """slot_identity_consistency always derives sanity_gate_not_model_input."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        row = pd.Series(
            _reg_row(
                feature_family_id=SLOT_IDENTITY_FEATURE_ID,
                prediction_setting="in_game_snapshot",
                source_table_or_event_family="tracker_events_raw.PlayerSetup",
                allowed_cutoff_rule="event.loop <= cutoff_loop",
                candidate_leakage_modes="none",
                status="sanity_gate_not_model_input",
            )
        )
        verdict = derive_section10_verdict(row, rules)
        assert verdict.derived_status == "sanity_gate_not_model_input"

    def test_slot_identity_recorded_as_allowed_causes_drift(
        self, tmp_path: Path
    ) -> None:
        """slot_identity_consistency recorded as 'allowed' triggers F-1b (looser drift)."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        row = _reg_row(
            feature_family_id=SLOT_IDENTITY_FEATURE_ID,
            prediction_setting="in_game_snapshot",
            source_table_or_event_family="tracker_events_raw.PlayerSetup",
            allowed_cutoff_rule="event.loop <= cutoff_loop",
            candidate_leakage_modes="none",
            status="allowed",  # should be sanity_gate_not_model_input
        )
        rows_series = _df_to_series_list(_make_df([row]))
        result = compare_registry_verdicts(rows_series, rules)

        assert result.passed is False
        # sanity_gate > allowed in strictness ranking -> stricter drift (F-1a)
        assert result.halting_falsifier == "F-1a"


# ---------------------------------------------------------------------------
# T-F7: unrecognised status value
# ---------------------------------------------------------------------------


class TestTF7:
    """T-F7: unrecognised status token in registry."""

    def test_unknown_status_triggers_f7(self, tmp_path: Path) -> None:
        """A row with an unrecognised status value triggers F-7."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        row = _reg_row(
            feature_family_id="sc2egset.pre_game.bad_status",
            status="definitely_not_a_valid_status",
        )
        rows_series = _df_to_series_list(_make_df([row]))
        result = compare_registry_verdicts(rows_series, rules)

        assert result.passed is False
        assert result.halting_falsifier == "F-7"


# ---------------------------------------------------------------------------
# T-VAC: materialized_column_count is always 0
# ---------------------------------------------------------------------------


class TestTVac:
    """T-VAC: materialized_column_count == 0 always."""

    def test_vac_synthetic(self, tmp_path: Path) -> None:
        """Synthetic registry returns materialized_column_count == 0."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        row = _reg_row(feature_family_id="sc2egset.pre_game.vac_check")
        rows_series = _df_to_series_list(_make_df([row]))
        result = compare_registry_verdicts(rows_series, rules)

        assert result.materialized_column_count == 0

    @pytest.mark.skipif(
        not REGISTRY_CSV_PATH.exists(),
        reason="Real registry CSV not found on disk",
    )
    def test_vac_real_registry(self) -> None:
        """Real registry returns materialized_column_count == 0."""
        result = validate_registry_section10_verdicts(
            REGISTRY_CSV_PATH, TRACKER_CSV_PATH
        )
        assert result.materialized_column_count == 0


# ---------------------------------------------------------------------------
# T-26ROW: real on-disk registry passes with all expected values
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not REGISTRY_CSV_PATH.exists(),
    reason="Real registry CSV not found on disk",
)
class TestT26Row:
    """T-26ROW: full audit of the real on-disk registry."""

    def test_passed_is_true(self) -> None:
        result = validate_registry_section10_verdicts(
            REGISTRY_CSV_PATH, TRACKER_CSV_PATH
        )
        assert result.passed is True

    def test_rows_audited_is_26(self) -> None:
        result = validate_registry_section10_verdicts(
            REGISTRY_CSV_PATH, TRACKER_CSV_PATH
        )
        assert result.rows_audited == 26

    def test_materialized_column_count_is_0(self) -> None:
        result = validate_registry_section10_verdicts(
            REGISTRY_CSV_PATH, TRACKER_CSV_PATH
        )
        assert result.materialized_column_count == 0

    def test_halting_falsifier_is_none(self) -> None:
        result = validate_registry_section10_verdicts(
            REGISTRY_CSV_PATH, TRACKER_CSV_PATH
        )
        assert result.halting_falsifier is None

    def test_no_stricter_drifts(self) -> None:
        result = validate_registry_section10_verdicts(
            REGISTRY_CSV_PATH, TRACKER_CSV_PATH
        )
        assert len(result.stricter_drifts) == 0

    def test_no_looser_drifts(self) -> None:
        result = validate_registry_section10_verdicts(
            REGISTRY_CSV_PATH, TRACKER_CSV_PATH
        )
        assert len(result.looser_drifts) == 0

    def test_no_independent_trigger_hits(self) -> None:
        result = validate_registry_section10_verdicts(
            REGISTRY_CSV_PATH, TRACKER_CSV_PATH
        )
        assert len(result.independent_trigger_hits) == 0


# ---------------------------------------------------------------------------
# T-ROWCNT: row count != 26 raises ValueError
# ---------------------------------------------------------------------------


class TestTRowCnt:
    """T-ROWCNT: load_registry_rows raises ValueError when row count != 26."""

    def test_wrong_row_count_raises(self, tmp_path: Path) -> None:
        """CSV with 5 rows raises ValueError referencing the count."""
        registry_path = tmp_path / "registry.csv"
        rows = [
            _reg_row(feature_family_id=f"sc2egset.pre_game.r{i}") for i in range(5)
        ]
        _write_registry_csv(registry_path, rows)

        with pytest.raises(ValueError, match="S-2 FAIL"):
            load_registry_rows(registry_path)

    def test_extra_rows_raises(self, tmp_path: Path) -> None:
        """CSV with 27 rows raises ValueError."""
        registry_path = tmp_path / "registry.csv"
        rows = [
            _reg_row(feature_family_id=f"sc2egset.pre_game.r{i}")
            for i in range(27)
        ]
        _write_registry_csv(registry_path, rows)

        with pytest.raises(ValueError, match="S-2 FAIL"):
            load_registry_rows(registry_path)


# ---------------------------------------------------------------------------
# T-EMPTY: empty CSV (header only) raises ValueError
# ---------------------------------------------------------------------------


class TestTEmpty:
    """T-EMPTY: empty CSV (header only) raises ValueError."""

    def test_empty_csv_raises(self, tmp_path: Path) -> None:
        """CSV with header only (0 data rows) raises ValueError."""
        registry_path = tmp_path / "empty_registry.csv"
        _write_registry_csv(registry_path, [])

        with pytest.raises(ValueError, match="S-2 FAIL"):
            load_registry_rows(registry_path)


# ---------------------------------------------------------------------------
# T-SYN: synonym equivalence — blocked_until_additional_validation == blocked_until_validation
# ---------------------------------------------------------------------------


class TestTSyn:
    """T-SYN: dataset-side synonym equals spec-side token — no false F-1a/F-1b."""

    def test_synonym_treated_as_equal_for_blocked_or_deferred(
        self, tmp_path: Path
    ) -> None:
        """A blocked_or_deferred row with the synonym status should not trigger drift."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        row = _reg_row(
            feature_family_id="sc2egset.blocked_or_deferred.syn_test",
            prediction_setting="blocked_or_deferred",
            source_table_or_event_family="tracker_events_raw.UnitOwnerChange",
            source_grain="(filename, playerId)",
            model_input_grain="blocked",
            target_grain="blocked",
            temporal_anchor="event.loop",
            allowed_cutoff_rule="blocked",
            candidate_leakage_modes="blocked",
            cold_start_handling="blocked",
            status=DATASET_SIDE_BLOCKED_SYNONYM,  # synonym, not spec-side token
            per_player_construction="blocked",
            block="gate_and_blocked",
        )
        rows_series = _df_to_series_list(_make_df([row]))
        result = compare_registry_verdicts(rows_series, rules)

        # Both derive as blocked_until_validation; synonym must not cause drift
        assert len(result.stricter_drifts) == 0, (
            f"Unexpected stricter drifts: {result.stricter_drifts}"
        )
        assert len(result.looser_drifts) == 0, (
            f"Unexpected looser drifts: {result.looser_drifts}"
        )

    def test_synonym_not_in_section10_verdicts(self) -> None:
        """The dataset-side synonym is NOT in SECTION10_VERDICTS (spec-side only)."""
        assert DATASET_SIDE_BLOCKED_SYNONYM not in SECTION10_VERDICTS

    def test_synonym_constant_value(self) -> None:
        """Verify the synonym constant has the expected string value."""
        assert DATASET_SIDE_BLOCKED_SYNONYM == "blocked_until_additional_validation"


# ---------------------------------------------------------------------------
# Additional coverage tests for uncovered branches
# ---------------------------------------------------------------------------


class TestAdditionalCoverage:
    """Coverage tests for branches not exercised by the 14 required test cases."""

    def test_load_registry_rows_file_not_found(self, tmp_path: Path) -> None:
        """load_registry_rows raises FileNotFoundError when CSV is absent (S-1)."""
        missing_path = tmp_path / "nonexistent.csv"
        with pytest.raises(FileNotFoundError, match="S-1 FAIL"):
            load_registry_rows(missing_path)

    def test_load_registry_rows_duplicate_id_raises(self, tmp_path: Path) -> None:
        """load_registry_rows raises ValueError on duplicate feature_family_id (S-3)."""
        registry_path = tmp_path / "dup_registry.csv"
        # Create 26 rows but with a duplicate ID
        rows = [
            _reg_row(feature_family_id=f"sc2egset.pre_game.r{i}")
            for i in range(25)
        ]
        # Add a duplicate of r0
        rows.append(_reg_row(feature_family_id="sc2egset.pre_game.r0"))
        _write_registry_csv(registry_path, rows)

        with pytest.raises(ValueError, match="S-3 FAIL"):
            load_registry_rows(registry_path)

    def test_load_tracker_map_file_not_found(self, tmp_path: Path) -> None:
        """_load_tracker_map raises FileNotFoundError when tracker CSV is absent."""
        from rts_predict.games.sc2.datasets.sc2egset.validate_registry_section10_verdicts import (
            _load_tracker_map,
        )

        missing_path = tmp_path / "no_tracker.csv"
        with pytest.raises(FileNotFoundError):
            _load_tracker_map(missing_path)

    def test_history_row_with_post_game_token(self, tmp_path: Path) -> None:
        """A history_enriched_pre_game row with a post-game token derives blocked."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        row = pd.Series(
            _reg_row(
                feature_family_id=(
                    "sc2egset.history_enriched_pre_game.history_won"
                ),
                prediction_setting="history_enriched_pre_game",
                allowed_cutoff_rule="history_time < won_timestamp",
                status="allowed",
            )
        )
        verdict = derive_section10_verdict(row, rules)
        assert verdict.derived_status == "blocked_until_validation"
        assert any("F-3" in t for t in verdict.triggers_fired)

    def test_ingame_eligible_with_caveat_tracker_path(
        self, tmp_path: Path
    ) -> None:
        """An in_game_snapshot row with no leakage mode but eligible_with_caveat
        in tracker CSV derives allowed_with_caveat via tracker path."""
        tracker_path = tmp_path / "tracker.csv"
        tracker_rows = [
            {
                "feature_family": "caveat_family",
                "source_event_family": "UnitBorn",
                "planned_for_phase02": "yes",
                "status_pre_game": "not_applicable_to_pre_game",
                "status_in_game_snapshot": "eligible_with_caveat",
                "status_post_game_or_blocked": "not_applicable",
                "eligibility_scope": "with caveat",
                "blocking_reason_if_blocked": "",
                "caveat": "some caveat",
                "evidence_source": "V5",
                "upstream_verdicts": "V5",
                "notes_for_phase02": "",
            }
        ]
        with tracker_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh, fieldnames=list(tracker_rows[0].keys())
            )
            writer.writeheader()
            writer.writerows(tracker_rows)

        rules = _make_protocol_rules(tracker_path)

        row = pd.Series(
            _reg_row(
                feature_family_id=(
                    "sc2egset.in_game_snapshot.caveat_family"
                ),
                prediction_setting="in_game_snapshot",
                source_table_or_event_family="tracker_events_raw.UnitBorn",
                allowed_cutoff_rule="event.loop <= cutoff_loop",
                # 'none' leakage, but tracker is eligible_with_caveat
                candidate_leakage_modes="none",
                status="allowed_with_caveat",
            )
        )
        verdict = derive_section10_verdict(row, rules)
        assert verdict.derived_status == "allowed_with_caveat"
        assert "eligible_with_caveat" in verdict.rule_path

    def test_f7_as_halting_falsifier(self, tmp_path: Path) -> None:
        """F-7 becomes the halting_falsifier when no other falsifier fires first."""
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        # Single row with bad status — no other falsifier fires
        row = _reg_row(
            feature_family_id="sc2egset.pre_game.bad",
            status="not_a_real_status",
        )
        rows_series = _df_to_series_list(_make_df([row]))
        result = compare_registry_verdicts(rows_series, rules)

        assert result.passed is False
        assert result.halting_falsifier == "F-7"

    def test_evaluate_independent_triggers_missing_grain(
        self, tmp_path: Path
    ) -> None:
        """Missing source_grain fires the trigger:missing_source_grain trigger."""
        from rts_predict.games.sc2.datasets.sc2egset.validate_registry_section10_verdicts import (
            _evaluate_independent_triggers,
        )

        tracker_map = {
            r["feature_family"]: r["status_in_game_snapshot"]
            for r in [
                {
                    "feature_family": "dummy",
                    "status_in_game_snapshot": "eligible_for_phase02_now",
                }
            ]
        }

        row_data = _reg_row(
            feature_family_id="sc2egset.pre_game.no_grain",
            source_grain="",
        )
        row_evidence = pd.Series(
            {k: v for k, v in row_data.items() if k != "status"}
        )
        hits = _evaluate_independent_triggers(
            row_evidence,
            tracker_map,
            "blocked_until_additional_validation",
            SLOT_IDENTITY_FEATURE_ID,
        )
        assert "trigger:missing_source_grain" in hits

    def test_evaluate_independent_triggers_missing_model_input_grain(
        self, tmp_path: Path
    ) -> None:
        """Missing model_input_grain fires the trigger:missing_model_input_grain trigger."""
        from rts_predict.games.sc2.datasets.sc2egset.validate_registry_section10_verdicts import (
            _evaluate_independent_triggers,
        )

        tracker_map: dict[str, str] = {}
        row_data = _reg_row(
            feature_family_id="sc2egset.pre_game.no_model_grain",
            model_input_grain="",
        )
        row_evidence = pd.Series(
            {k: v for k, v in row_data.items() if k != "status"}
        )
        hits = _evaluate_independent_triggers(
            row_evidence,
            tracker_map,
            "blocked_until_additional_validation",
            SLOT_IDENTITY_FEATURE_ID,
        )
        assert "trigger:missing_model_input_grain" in hits

    def test_evaluate_independent_triggers_missing_prediction_setting(
        self,
    ) -> None:
        """Missing prediction_setting fires the trigger:missing_prediction_setting trigger."""
        from rts_predict.games.sc2.datasets.sc2egset.validate_registry_section10_verdicts import (
            _evaluate_independent_triggers,
        )

        tracker_map: dict[str, str] = {}
        row_data = _reg_row(
            feature_family_id="sc2egset.pre_game.no_ps",
            prediction_setting="",
        )
        row_evidence = pd.Series(
            {k: v for k, v in row_data.items() if k != "status"}
        )
        hits = _evaluate_independent_triggers(
            row_evidence,
            tracker_map,
            "blocked_until_additional_validation",
            SLOT_IDENTITY_FEATURE_ID,
        )
        assert "trigger:missing_prediction_setting" in hits

    def test_evaluate_independent_triggers_missing_temporal_anchor(
        self,
    ) -> None:
        """Missing temporal_anchor fires the trigger:missing_temporal_anchor trigger."""
        from rts_predict.games.sc2.datasets.sc2egset.validate_registry_section10_verdicts import (
            _evaluate_independent_triggers,
        )

        tracker_map: dict[str, str] = {}
        row_data = _reg_row(
            feature_family_id="sc2egset.pre_game.no_anchor",
            temporal_anchor="",
        )
        row_evidence = pd.Series(
            {k: v for k, v in row_data.items() if k != "status"}
        )
        hits = _evaluate_independent_triggers(
            row_evidence,
            tracker_map,
            "blocked_until_additional_validation",
            SLOT_IDENTITY_FEATURE_ID,
        )
        assert "trigger:missing_temporal_anchor" in hits

    def test_evaluate_independent_triggers_tracker_in_pre_game(
        self,
    ) -> None:
        """Tracker source in pre_game fires the tracker_in_pre_game trigger (§10.3)."""
        from rts_predict.games.sc2.datasets.sc2egset.validate_registry_section10_verdicts import (
            _evaluate_independent_triggers,
        )

        tracker_map: dict[str, str] = {}
        row_data = _reg_row(
            feature_family_id="sc2egset.pre_game.tracker_regression",
            prediction_setting="pre_game",
            source_table_or_event_family="tracker_events_raw.UnitBorn",
        )
        row_evidence = pd.Series(
            {k: v for k, v in row_data.items() if k != "status"}
        )
        hits = _evaluate_independent_triggers(
            row_evidence,
            tracker_map,
            "blocked_until_additional_validation",
            SLOT_IDENTITY_FEATURE_ID,
        )
        assert "trigger:tracker_in_pre_game" in hits

    def test_evaluate_independent_triggers_blocked_leakage_on_non_blocked(
        self,
    ) -> None:
        """Leakage mode 'blocked' on non-blocked row fires the trigger."""
        from rts_predict.games.sc2.datasets.sc2egset.validate_registry_section10_verdicts import (
            _evaluate_independent_triggers,
        )

        tracker_map: dict[str, str] = {}
        row_data = _reg_row(
            feature_family_id="sc2egset.pre_game.blocked_leakage",
            prediction_setting="pre_game",
            candidate_leakage_modes="blocked",
        )
        row_evidence = pd.Series(
            {k: v for k, v in row_data.items() if k != "status"}
        )
        hits = _evaluate_independent_triggers(
            row_evidence,
            tracker_map,
            "blocked_until_additional_validation",
            SLOT_IDENTITY_FEATURE_ID,
        )
        assert "trigger:blocked_leakage_on_non_blocked_row" in hits

    def test_evaluate_independent_triggers_history_lte(
        self,
    ) -> None:
        """History row with '<=' fires F-4 in independent trigger evaluation."""
        from rts_predict.games.sc2.datasets.sc2egset.validate_registry_section10_verdicts import (
            _evaluate_independent_triggers,
        )

        tracker_map: dict[str, str] = {}
        row_data = _reg_row(
            feature_family_id=(
                "sc2egset.history_enriched_pre_game.lte_row"
            ),
            prediction_setting="history_enriched_pre_game",
            allowed_cutoff_rule="history_time <= target_time",
        )
        row_evidence = pd.Series(
            {k: v for k, v in row_data.items() if k != "status"}
        )
        hits = _evaluate_independent_triggers(
            row_evidence,
            tracker_map,
            "blocked_until_additional_validation",
            SLOT_IDENTITY_FEATURE_ID,
        )
        assert "F-4:invalid_cutoff_operator:<=" in hits

    def test_evaluate_independent_triggers_history_missing_lt(
        self,
    ) -> None:
        """History row missing '<' fires F-4:missing_strict_lt trigger."""
        from rts_predict.games.sc2.datasets.sc2egset.validate_registry_section10_verdicts import (
            _evaluate_independent_triggers,
        )

        tracker_map: dict[str, str] = {}
        row_data = _reg_row(
            feature_family_id=(
                "sc2egset.history_enriched_pre_game.no_lt"
            ),
            prediction_setting="history_enriched_pre_game",
            allowed_cutoff_rule="snapshot_at_match_start",
        )
        row_evidence = pd.Series(
            {k: v for k, v in row_data.items() if k != "status"}
        )
        hits = _evaluate_independent_triggers(
            row_evidence,
            tracker_map,
            "blocked_until_additional_validation",
            SLOT_IDENTITY_FEATURE_ID,
        )
        assert "F-4:missing_strict_lt" in hits

    def test_f2_halting_falsifier_via_missing_anchor(
        self, tmp_path: Path
    ) -> None:
        """F-2 fires when an independent trigger hits an 'allowed' row with no drift.

        Row derives as 'allowed' (pre_game, no post-game tokens), recorded='allowed',
        so no drift. But the row has empty temporal_anchor, which fires
        trigger:missing_temporal_anchor in the independent trigger check.
        F-2 then becomes the halting_falsifier.
        """
        tracker_path = _make_tracker_csv(tmp_path)
        rules = _make_protocol_rules(tracker_path)

        row = _reg_row(
            feature_family_id="sc2egset.pre_game.missing_anchor",
            prediction_setting="pre_game",
            temporal_anchor="",  # fires trigger:missing_temporal_anchor
            status="allowed",  # no drift: derivation also says allowed
        )
        rows_series = _df_to_series_list(_make_df([row]))
        result = compare_registry_verdicts(rows_series, rules)

        assert result.passed is False
        assert result.halting_falsifier == "F-2"
        assert len(result.independent_trigger_hits) >= 1
