"""Tests for ``validate_registry_skeleton`` (V-1..V-6).

Covers the SC2EGSet Step 02_01_01 registry skeleton validation module. Uses
the actual tracker eligibility CSV shipped in the repo for V-2/V-4/V-5
checks and synthetic in-memory skeletons for V-1/V-3/V-6 failure cases.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest

from rts_predict.games.sc2.datasets.sc2egset.validate_registry_skeleton import (
    REQUIRED_COLUMNS,
    validate_registry_skeleton,
)

# Repo-relative path — resolve from this test file's location to avoid
# absolute paths and keep cross-machine portability.
TRACKER_CSV_PATH: Path = (
    Path(__file__).resolve().parents[6]
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


def _row(
    *,
    feature_family_id: str,
    prediction_setting: str,
    status: str,
    source_table_or_event_family: str = "matches_flat",
    temporal_anchor: str = "details_timeUTC",
    allowed_cutoff_rule: str = "match_time < target_time",
) -> dict[str, Any]:
    """Build a minimal valid skeleton row with sensible defaults."""
    return {
        "feature_family_id": feature_family_id,
        "dataset_tag": "sc2egset",
        "prediction_setting": prediction_setting,
        "source_table_or_event_family": source_table_or_event_family,
        "source_grain": "(filename, player_id_worldwide)",
        "model_input_grain": "(focal_match_id, focal_player)",
        "target_grain": "(focal_match_id, focal_player)",
        "temporal_anchor": temporal_anchor,
        "allowed_cutoff_rule": allowed_cutoff_rule,
        "candidate_leakage_modes": "none",
        "cold_start_handling": "G-CS-1",
        "status": status,
        "per_player_construction": "symmetric",
    }


@pytest.fixture()
def valid_skeleton() -> list[dict[str, Any]]:
    """A minimal but structurally complete skeleton covering all checks."""
    return [
        _row(
            feature_family_id="sc2egset.pre_game.focal_race_with_opponent_race_pair",
            prediction_setting="pre_game",
            status="allowed",
            source_table_or_event_family="replay_players_raw",
            temporal_anchor="details_timeUTC",
            allowed_cutoff_rule="snapshot_at_match_start",
        ),
        _row(
            feature_family_id="sc2egset.history_enriched_pre_game.focal_player_history",
            prediction_setting="history_enriched_pre_game",
            status="allowed",
            source_table_or_event_family="matches_flat",
            temporal_anchor="details_timeUTC",
            allowed_cutoff_rule="history_time < target_time",
        ),
        _row(
            feature_family_id="sc2egset.in_game_snapshot.count_units_built_by_cutoff_loop",
            prediction_setting="in_game_snapshot",
            status="allowed",
            source_table_or_event_family="tracker_events_raw.UnitBorn",
            temporal_anchor="event.loop",
            allowed_cutoff_rule="event.loop <= cutoff_loop",
        ),
        _row(
            feature_family_id="sc2egset.in_game_snapshot.slot_identity_consistency",
            prediction_setting="in_game_snapshot",
            status="sanity_gate_not_model_input",
            source_table_or_event_family="tracker_events_raw.PlayerSetup",
            temporal_anchor="event.loop",
            allowed_cutoff_rule="event.loop <= cutoff_loop",
        ),
        _row(
            feature_family_id="sc2egset.blocked_or_deferred.mind_control_event_count",
            prediction_setting="blocked_or_deferred",
            status="blocked_until_additional_validation",
            source_table_or_event_family="tracker_events_raw.UnitOwnerChange",
            temporal_anchor="event.loop",
            allowed_cutoff_rule="blocked",
        ),
        _row(
            feature_family_id="sc2egset.blocked_or_deferred.army_centroid_at_cutoff_snapshot",
            prediction_setting="blocked_or_deferred",
            status="blocked_until_additional_validation",
            source_table_or_event_family="tracker_events_raw.UnitPositions",
            temporal_anchor="event.loop",
            allowed_cutoff_rule="blocked",
        ),
        _row(
            feature_family_id="sc2egset.blocked_or_deferred.playerstats_cumulative_economy_fields",
            prediction_setting="blocked_or_deferred",
            status="blocked_until_additional_validation",
            source_table_or_event_family="tracker_events_raw.PlayerStats",
            temporal_anchor="event.loop",
            allowed_cutoff_rule="blocked",
        ),
    ]


# ---------------------------------------------------------------------------
# V-1 schema integrity
# ---------------------------------------------------------------------------


def test_tracker_csv_path_exists() -> None:
    """Sanity: the tracker CSV path resolves to an existing file."""
    assert TRACKER_CSV_PATH.exists(), (
        f"Tracker CSV not found at {TRACKER_CSV_PATH}. "
        "Update TRACKER_CSV_PATH if the artifact moved."
    )


def test_v1_valid_skeleton_passes(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    validate_registry_skeleton(valid_skeleton, TRACKER_CSV_PATH)


def test_v1_missing_column_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    del skel[0]["per_player_construction"]
    with pytest.raises(AssertionError, match="V-1.*missing required columns"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v1_extra_column_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    skel[0]["unexpected_extra_column"] = "boom"
    with pytest.raises(AssertionError, match="V-1.*forbidden extra columns"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v1_invalid_prediction_setting_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    skel[0]["prediction_setting"] = "post_game_god_mode"
    with pytest.raises(AssertionError, match="V-1.*invalid prediction_setting"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v1_invalid_status_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    skel[0]["status"] = "approved_by_committee"
    with pytest.raises(AssertionError, match="V-1.*invalid status"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v1_duplicate_feature_family_id_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    skel[1]["feature_family_id"] = skel[0]["feature_family_id"]
    with pytest.raises(AssertionError, match="V-1.*duplicate feature_family_id"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v1_wrong_dataset_tag_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    skel[0]["dataset_tag"] = "aoestats"
    with pytest.raises(AssertionError, match="V-1.*dataset_tag"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v1_empty_feature_family_id_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    skel[0]["feature_family_id"] = ""
    with pytest.raises(AssertionError, match="V-1.*null/empty feature_family_id"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v1_unprefixed_feature_family_id_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    skel[0]["feature_family_id"] = "pre_game.focal_race"  # missing 'sc2egset.' prefix
    with pytest.raises(AssertionError, match="V-1.*must start with 'sc2egset"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v1_required_columns_count() -> None:
    """Lock the schema width: any drift requires deliberate spec amendment."""
    assert len(REQUIRED_COLUMNS) == 13


# ---------------------------------------------------------------------------
# V-2 tracker eligibility split counts
# ---------------------------------------------------------------------------


def test_v2_csv_counts_correct(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    """V-2 passes against the actual tracker CSV shipped in the repo."""
    validate_registry_skeleton(valid_skeleton, TRACKER_CSV_PATH)


def test_v2_missing_csv_fails(
    valid_skeleton: list[dict[str, Any]], tmp_path: Path
) -> None:
    bogus = tmp_path / "does_not_exist.csv"
    with pytest.raises(AssertionError, match="V-2.*tracker CSV not found"):
        validate_registry_skeleton(valid_skeleton, bogus)


def test_v2_wrong_counts_fails(
    valid_skeleton: list[dict[str, Any]], tmp_path: Path
) -> None:
    """A doctored CSV with mismatched counts must be rejected."""
    bad_csv = tmp_path / "tracker.csv"
    header = (
        "feature_family,source_event_family,planned_for_phase02,"
        "status_pre_game,status_in_game_snapshot,status_post_game_or_blocked,"
        "eligibility_scope,blocking_reason_if_blocked,caveat,evidence_source,"
        "upstream_verdicts,notes_for_phase02"
    )
    # Only 1 row marked eligible_for_phase02_now (expected 5) -> must fail V-2.
    line = (
        "fake_family,UnitBorn,yes,not_applicable_to_pre_game,"
        "eligible_for_phase02_now,not_applicable,scope,,,evidence,V1,notes"
    )
    bad_csv.write_text(f"{header}\n{line}\n", encoding="utf-8")
    with pytest.raises(AssertionError, match="V-2.*count mismatch"):
        validate_registry_skeleton(valid_skeleton, bad_csv)


# ---------------------------------------------------------------------------
# V-3 blocked tracker families remain blocked
# ---------------------------------------------------------------------------


def test_v3_blocked_families_correct(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    """V-3 passes when the three blocked families carry the blocked status."""
    validate_registry_skeleton(valid_skeleton, TRACKER_CSV_PATH)


def test_v3_blocked_family_wrong_status_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    # Promote mind_control_event_count to "allowed" — must be rejected.
    for r in skel:
        if "mind_control_event_count" in r["feature_family_id"]:
            r["status"] = "allowed"
            break
    with pytest.raises(AssertionError, match="V-3.*expected"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v3_missing_blocked_family_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = [
        r
        for r in valid_skeleton
        if "army_centroid_at_cutoff_snapshot" not in r["feature_family_id"]
    ]
    with pytest.raises(AssertionError, match="V-3.*army_centroid_at_cutoff_snapshot"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


# ---------------------------------------------------------------------------
# V-4 slot_identity_consistency registry classification
# ---------------------------------------------------------------------------


def test_v4_slot_identity_correct(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    validate_registry_skeleton(valid_skeleton, TRACKER_CSV_PATH)


def test_v4_slot_identity_wrong_status_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    for r in skel:
        if "slot_identity_consistency" in r["feature_family_id"]:
            r["status"] = "allowed"
            break
    with pytest.raises(AssertionError, match="V-4.*sanity_gate_not_model_input"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v4_slot_identity_missing_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = [
        r
        for r in valid_skeleton
        if "slot_identity_consistency" not in r["feature_family_id"]
    ]
    with pytest.raises(AssertionError, match="V-4.*expected exactly 1"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v4_modified_csv_fails(
    valid_skeleton: list[dict[str, Any]], tmp_path: Path
) -> None:
    """If the CSV row for slot_identity_consistency is modified, V-4 fails."""
    bad_csv = tmp_path / "tracker.csv"
    header = (
        "feature_family,source_event_family,planned_for_phase02,"
        "status_pre_game,status_in_game_snapshot,status_post_game_or_blocked,"
        "eligibility_scope,blocking_reason_if_blocked,caveat,evidence_source,"
        "upstream_verdicts,notes_for_phase02"
    )
    # Build a CSV that satisfies V-2 counts (5/7/3) but mutates slot_identity
    # to a different status_in_game_snapshot value — V-4 must reject.
    rows = []
    # 5 eligible_for_phase02_now (one is slot_identity_consistency mutated)
    eligible_now_names = [
        "count_units_built_by_cutoff_loop",
        "count_units_killed_by_cutoff_loop",
        "morph_count_by_cutoff_loop",
        "building_construction_count_by_cutoff_loop",
        "slot_identity_consistency",
    ]
    for name in eligible_now_names:
        if name == "slot_identity_consistency":
            status = "eligible_with_caveat"  # mutated
        else:
            status = "eligible_for_phase02_now"
        rows.append(
            f"{name},PlayerSetup,yes,not_applicable_to_pre_game,"
            f"{status},not_applicable,s,,,e,V,n"
        )
    # 6 more eligible_with_caveat to total 7 (because slot mutation added one)
    for i in range(6):
        rows.append(
            f"caveat_family_{i},PlayerStats,yes,not_applicable_to_pre_game,"
            f"eligible_with_caveat,not_applicable,s,,,e,V,n"
        )
    # 3 blocked
    for name in (
        "mind_control_event_count",
        "army_centroid_at_cutoff_snapshot",
        "playerstats_cumulative_economy_fields",
    ):
        rows.append(
            f"{name},UnitOwnerChange,no,not_applicable_to_pre_game,"
            f"blocked_until_additional_validation,blocked_until_additional_validation,"
            f"blocked,,,e,V,n"
        )
    # Now we have 5 eligible_now + 1 mutated -> 4 eligible_now + 8 with_caveat
    # which fails V-2 first. To target V-4, keep counts at 5/7/3 by NOT mutating
    # the slot row and instead inject a duplicate slot row with wrong status.
    # Simpler approach: rebuild with exactly 5/7/3 where slot has wrong status.
    rows = []
    eligible_now_names = [
        "count_units_built_by_cutoff_loop",
        "count_units_killed_by_cutoff_loop",
        "morph_count_by_cutoff_loop",
        "building_construction_count_by_cutoff_loop",
        "slot_identity_consistency",  # will be marked eligible_with_caveat (wrong)
    ]
    for i, name in enumerate(eligible_now_names):
        if name == "slot_identity_consistency":
            # Move slot to with_caveat; balance by promoting one filler family
            # to eligible_now to keep counts at 5/7/3.
            rows.append(
                f"{name},PlayerSetup,yes,not_applicable_to_pre_game,"
                f"eligible_with_caveat,not_applicable,s,,,e,V,n"
            )
        else:
            rows.append(
                f"{name},UnitBorn,yes,not_applicable_to_pre_game,"
                f"eligible_for_phase02_now,not_applicable,s,,,e,V,n"
            )
    # Promote one filler to eligible_now to keep eligible_now count at 5.
    rows.append(
        "extra_eligible_now,PlayerStats,yes,not_applicable_to_pre_game,"
        "eligible_for_phase02_now,not_applicable,s,,,e,V,n"
    )
    # 6 eligible_with_caveat to total 7 (slot already counted as caveat).
    for i in range(6):
        rows.append(
            f"caveat_family_{i},PlayerStats,yes,not_applicable_to_pre_game,"
            f"eligible_with_caveat,not_applicable,s,,,e,V,n"
        )
    for name in (
        "mind_control_event_count",
        "army_centroid_at_cutoff_snapshot",
        "playerstats_cumulative_economy_fields",
    ):
        rows.append(
            f"{name},UnitOwnerChange,no,not_applicable_to_pre_game,"
            f"blocked_until_additional_validation,blocked_until_additional_validation,"
            f"blocked,,,e,V,n"
        )
    bad_csv.write_text(header + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
    with pytest.raises(AssertionError, match="V-4.*CSV must NOT be modified"):
        validate_registry_skeleton(valid_skeleton, bad_csv)


# ---------------------------------------------------------------------------
# V-5 zero tracker-derived rows in pre_game / history_enriched_pre_game
# ---------------------------------------------------------------------------


def test_v5_tracker_never_pre_game(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    validate_registry_skeleton(valid_skeleton, TRACKER_CSV_PATH)


def test_v5_tracker_in_pre_game_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    # Add a malformed row: tracker UnitBorn declared as pre_game.
    skel.append(
        _row(
            feature_family_id="sc2egset.pre_game.illegal_tracker_pre_game",
            prediction_setting="pre_game",
            status="allowed",
            source_table_or_event_family="tracker_events_raw.UnitBorn",
            temporal_anchor="details_timeUTC",
            allowed_cutoff_rule="snapshot_at_match_start",
        )
    )
    with pytest.raises(AssertionError, match="V-5.*tracker-derived"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v5_tracker_in_history_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    skel.append(
        _row(
            feature_family_id="sc2egset.history_enriched_pre_game.illegal_tracker_history",
            prediction_setting="history_enriched_pre_game",
            status="allowed",
            source_table_or_event_family="tracker_events_raw.PlayerStats",
            temporal_anchor="details_timeUTC",
            allowed_cutoff_rule="history_time < target_time",
        )
    )
    with pytest.raises(AssertionError, match="V-5.*tracker-derived"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v5_compound_event_family_match(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    """The compound CSV entry 'UnitInit / UnitDone' must match each component."""
    skel = copy.deepcopy(valid_skeleton)
    skel.append(
        _row(
            feature_family_id="sc2egset.pre_game.illegal_unit_done_pre_game",
            prediction_setting="pre_game",
            status="allowed",
            source_table_or_event_family="tracker_events_raw.UnitDone",
            temporal_anchor="details_timeUTC",
            allowed_cutoff_rule="snapshot_at_match_start",
        )
    )
    with pytest.raises(AssertionError, match="V-5.*tracker-derived"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


# ---------------------------------------------------------------------------
# V-6 history rows use strict < and details_timeUTC
# ---------------------------------------------------------------------------


def test_v6_history_strict_lt(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    validate_registry_skeleton(valid_skeleton, TRACKER_CSV_PATH)


def test_v6_history_lte_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    for r in skel:
        if r["prediction_setting"] == "history_enriched_pre_game":
            r["allowed_cutoff_rule"] = "history_time <= target_time"
            break
    with pytest.raises(AssertionError, match=r"V-6.*'<='"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v6_history_no_lt_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    for r in skel:
        if r["prediction_setting"] == "history_enriched_pre_game":
            r["allowed_cutoff_rule"] = "history_time before target_time"
            break
    with pytest.raises(AssertionError, match=r"V-6.*strict '<'"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v6_history_started_at_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    for r in skel:
        if r["prediction_setting"] == "history_enriched_pre_game":
            r["temporal_anchor"] = "started_at"
            break
    with pytest.raises(AssertionError, match="V-6.*temporal_anchor"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)


def test_v6_history_post_outcome_token_fails(
    valid_skeleton: list[dict[str, Any]],
) -> None:
    skel = copy.deepcopy(valid_skeleton)
    for r in skel:
        if r["prediction_setting"] == "history_enriched_pre_game":
            r["allowed_cutoff_rule"] = (
                "history_time < target_time AND match_result IS NOT NULL"
            )
            break
    with pytest.raises(AssertionError, match="V-6.*post-outcome"):
        validate_registry_skeleton(skel, TRACKER_CSV_PATH)
