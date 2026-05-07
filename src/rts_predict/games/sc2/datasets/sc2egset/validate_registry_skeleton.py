"""Validation module for SC2EGSet Step 02_01_01 feature-family registry skeleton.

This module implements the V-1..V-6 structural assertions for the planned
26-row registry skeleton declared in
``sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py``.

Binding specs:
    - CROSS-02-00-v3.0.1 §3.3 (strict ``<`` for history features)
    - CROSS-02-02-v1.0.1 §6 (SC2EGSet feature families) and §9 (cold-start gates)
    - CROSS-02-03-v1.0.1 §3 (audit-object 13-column schema), §4 (D1–D15),
      §5.1 (sc2egset ``temporal_anchor = details_timeUTC``; ``started_at``
      is the cross-dataset alias and is rejected for sc2egset rows)

Scope (six checks implemented here):
    V-1 Schema integrity: 13 required columns, controlled vocabularies for
        ``prediction_setting`` and ``status``, dataset-prefixed unique
        ``feature_family_id``, single-dataset ``dataset_tag``.
    V-2 Tracker eligibility split counts: ``eligible_for_phase02_now`` = 5,
        ``eligible_with_caveat`` = 7, ``blocked_until_additional_validation`` = 3.
    V-3 Blocked tracker families remain blocked in the skeleton.
    V-4 ``slot_identity_consistency`` is a registry-introduced
        ``sanity_gate_not_model_input`` classification — the tracker CSV
        itself is NOT modified.
    V-5 Zero tracker-derived rows in ``pre_game`` or
        ``history_enriched_pre_game``.
    V-6 ``history_enriched_pre_game`` rows use strict ``<`` and the
        sc2egset-specific ``details_timeUTC`` provenance anchor; the
        cross-dataset alias ``started_at`` is rejected.

Deferred to subsequent validation modules (NOT covered here):
    - Cold-start gate vocabulary check (gates G-CS-1..G-CS-6 only,
      no magic numbers per Invariant I7).
    - Per-player construction symmetry (Invariant I5).
    - Candidate-leakage-mode coverage against CROSS-02-01-v1.0.1.

The module exposes exactly one public function,
``validate_registry_skeleton``. It performs no file I/O other than reading
the tracker CSV from the supplied path. It does not call ``print``; the
notebook caller is responsible for surfacing PASS/FAIL output.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

REQUIRED_COLUMNS: tuple[str, ...] = (
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
)

ALLOWED_PREDICTION_SETTINGS: frozenset[str] = frozenset(
    {
        "pre_game",
        "history_enriched_pre_game",
        "in_game_snapshot",
        "blocked_or_deferred",
    }
)

ALLOWED_STATUSES: frozenset[str] = frozenset(
    {
        "allowed",
        "allowed_with_caveat",
        "sanity_gate_not_model_input",
        "blocked_until_additional_validation",
    }
)

EXPECTED_DATASET_TAG = "sc2egset"

EXPECTED_TRACKER_COUNTS: dict[str, int] = {
    "eligible_for_phase02_now": 5,
    "eligible_with_caveat": 7,
    "blocked_until_additional_validation": 3,
}

BLOCKED_TRACKER_FAMILIES: tuple[str, ...] = (
    "mind_control_event_count",
    "army_centroid_at_cutoff_snapshot",
    "playerstats_cumulative_economy_fields",
)

MODEL_INPUT_PREDICTION_SETTINGS: frozenset[str] = frozenset(
    {"pre_game", "history_enriched_pre_game", "in_game_snapshot"}
)

PRE_GAME_OR_HISTORY: frozenset[str] = frozenset(
    {"pre_game", "history_enriched_pre_game"}
)

# CROSS-02-03-v1.0.1 §5.1 — sc2egset uses details_timeUTC; started_at is the
# cross-dataset alias and is rejected for sc2egset history rows.
SC2EGSET_HISTORY_TEMPORAL_ANCHOR = "details_timeUTC"
REJECTED_HISTORY_TEMPORAL_ANCHOR = "started_at"

# Substrings that, if present in allowed_cutoff_rule, indicate post-outcome /
# target-game leakage references.
POST_OUTCOME_FORBIDDEN_TOKENS: tuple[str, ...] = (
    "won",
    "final_state",
    "match_result",
    "post_game",
)


def _read_tracker_rows(tracker_csv_path: Path | str) -> list[dict[str, str]]:
    """Read the tracker eligibility CSV into a list of row dicts.

    Args:
        tracker_csv_path: Path to ``tracker_events_feature_eligibility.csv``.

    Returns:
        Ordered list of row dicts as produced by ``csv.DictReader``.
    """
    path = Path(tracker_csv_path)
    assert path.exists(), f"V-2: tracker CSV not found at {path}"
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def _check_v1_schema_integrity(skeleton: list[dict[str, Any]]) -> None:
    """V-1: schema integrity, vocabularies, uniqueness, single-dataset tag."""
    assert isinstance(skeleton, list), "V-1: skeleton must be a list of dicts"
    assert len(skeleton) > 0, "V-1: skeleton is empty"

    required = set(REQUIRED_COLUMNS)
    seen_ids: set[str] = set()

    for idx, row in enumerate(skeleton):
        assert isinstance(row, dict), f"V-1: row {idx} is not a dict"

        row_keys = set(row.keys())
        missing = required - row_keys
        extra = row_keys - required
        assert not missing, (
            f"V-1: row {idx} ({row.get('feature_family_id', '<unknown>')}) "
            f"missing required columns: {sorted(missing)}"
        )
        assert not extra, (
            f"V-1: row {idx} ({row.get('feature_family_id', '<unknown>')}) "
            f"has forbidden extra columns (no materialized feature values "
            f"allowed): {sorted(extra)}"
        )
        assert len(row_keys) == len(REQUIRED_COLUMNS), (
            f"V-1: row {idx} has {len(row_keys)} columns; expected "
            f"exactly {len(REQUIRED_COLUMNS)}"
        )

        ffid = row["feature_family_id"]
        assert isinstance(ffid, str) and ffid, (
            f"V-1: row {idx} has null/empty feature_family_id"
        )
        assert ffid.startswith(f"{EXPECTED_DATASET_TAG}."), (
            f"V-1: feature_family_id '{ffid}' must start with "
            f"'{EXPECTED_DATASET_TAG}.' (dataset-prefixed per OQ1)"
        )
        assert ffid not in seen_ids, (
            f"V-1: duplicate feature_family_id '{ffid}' in skeleton"
        )
        seen_ids.add(ffid)

        ps = row["prediction_setting"]
        assert ps in ALLOWED_PREDICTION_SETTINGS, (
            f"V-1: row '{ffid}' has invalid prediction_setting '{ps}'; "
            f"allowed: {sorted(ALLOWED_PREDICTION_SETTINGS)}"
        )

        st = row["status"]
        assert st in ALLOWED_STATUSES, (
            f"V-1: row '{ffid}' has invalid status '{st}'; "
            f"allowed: {sorted(ALLOWED_STATUSES)}"
        )

        dt = row["dataset_tag"]
        assert dt == EXPECTED_DATASET_TAG, (
            f"V-1: row '{ffid}' has dataset_tag '{dt}'; expected "
            f"'{EXPECTED_DATASET_TAG}' (single-dataset skeleton)"
        )


def _check_v2_tracker_split_counts(tracker_rows: list[dict[str, str]]) -> None:
    """V-2: tracker CSV row counts by ``status_in_game_snapshot``."""
    actual_counts: dict[str, int] = {}
    for row in tracker_rows:
        key = row["status_in_game_snapshot"]
        actual_counts[key] = actual_counts.get(key, 0) + 1

    for expected_key, expected_value in EXPECTED_TRACKER_COUNTS.items():
        actual = actual_counts.get(expected_key, 0)
        assert actual == expected_value, (
            f"V-2: tracker CSV count mismatch for "
            f"status_in_game_snapshot='{expected_key}': "
            f"expected {expected_value}, got {actual}. "
            f"Full counts: {actual_counts}"
        )

    expected_total = sum(EXPECTED_TRACKER_COUNTS.values())
    actual_total = sum(actual_counts.values())
    assert actual_total == expected_total, (
        f"V-2: tracker CSV total row count {actual_total} "
        f"differs from expected {expected_total}; counts={actual_counts}"
    )


def _check_v3_blocked_families(skeleton: list[dict[str, Any]]) -> None:
    """V-3: the three blocked tracker families remain blocked in the skeleton."""
    for family_name in BLOCKED_TRACKER_FAMILIES:
        matches = [
            row
            for row in skeleton
            if family_name in row.get("feature_family_id", "")
        ]
        assert len(matches) >= 1, (
            f"V-3: expected at least one skeleton row for blocked family "
            f"'{family_name}'; found 0"
        )
        for row in matches:
            ffid = row["feature_family_id"]
            assert row["status"] == "blocked_until_additional_validation", (
                f"V-3: blocked family row '{ffid}' has status "
                f"'{row['status']}'; expected "
                f"'blocked_until_additional_validation'"
            )
            ps = row["prediction_setting"]
            if ps in MODEL_INPUT_PREDICTION_SETTINGS:
                # Combination of model-input prediction_setting with non-blocked
                # status is the failure mode V-3 guards against. Status is
                # already asserted blocked above; defensive check below.
                assert (
                    row["status"] == "blocked_until_additional_validation"
                ), (
                    f"V-3: blocked family row '{ffid}' has model-input "
                    f"prediction_setting '{ps}' but non-blocked status "
                    f"'{row['status']}'"
                )


def _check_v4_slot_identity_consistency(
    skeleton: list[dict[str, Any]], tracker_rows: list[dict[str, str]]
) -> None:
    """V-4: ``slot_identity_consistency`` is a registry-introduced gate.

    The tracker CSV marks ``slot_identity_consistency`` as
    ``eligible_for_phase02_now``. The registry reclassifies it to
    ``sanity_gate_not_model_input`` per the CSV ``notes_for_phase02`` field
    and PR #208 Phase 02 guidance. This is a registry-introduced
    classification — the CSV itself is NOT modified by this validation.
    """
    target = "slot_identity_consistency"
    matches = [
        row
        for row in skeleton
        if target in row.get("feature_family_id", "")
    ]
    assert len(matches) == 1, (
        f"V-4: expected exactly 1 skeleton row containing "
        f"'{target}'; found {len(matches)}"
    )
    row = matches[0]
    ffid = row["feature_family_id"]
    assert row["status"] == "sanity_gate_not_model_input", (
        f"V-4: slot_identity_consistency row '{ffid}' has status "
        f"'{row['status']}'; expected 'sanity_gate_not_model_input' "
        "(registry-introduced classification per PR #208 guidance)"
    )

    csv_matches = [
        r for r in tracker_rows if r["feature_family"] == target
    ]
    assert len(csv_matches) == 1, (
        f"V-4: expected exactly 1 tracker CSV row for "
        f"feature_family='{target}'; found {len(csv_matches)}"
    )
    csv_row = csv_matches[0]
    assert csv_row["status_in_game_snapshot"] == "eligible_for_phase02_now", (
        f"V-4: tracker CSV row for '{target}' has "
        f"status_in_game_snapshot='{csv_row['status_in_game_snapshot']}'; "
        "expected 'eligible_for_phase02_now' — the CSV must NOT be modified; "
        "the registry-layer reclassification is independent of CSV state"
    )


def _matches_tracker_event_family(
    source_table_or_event_family: str, tracker_event_families: set[str]
) -> bool:
    """Check if a skeleton source field references any tracker event family.

    The skeleton may store prefixed forms (e.g.
    ``tracker_events_raw.UnitBorn``) while the tracker CSV stores bare names
    (e.g. ``UnitBorn``). Compound CSV entries such as
    ``UnitInit / UnitDone`` are split on ``/`` and each component is
    compared individually. We use substring containment after normalizing
    whitespace so both naming forms match.
    """
    skel_norm = source_table_or_event_family.strip()
    if not skel_norm:
        return False
    for family in tracker_event_families:
        # Split compound entries like "UnitInit / UnitDone" into components.
        for component in family.split("/"):
            comp = component.strip()
            if not comp:
                continue
            if comp == skel_norm or comp in skel_norm:
                return True
    return False


def _check_v5_no_tracker_in_pre_game(
    skeleton: list[dict[str, Any]], tracker_rows: list[dict[str, str]]
) -> None:
    """V-5: zero tracker-derived rows in ``pre_game`` / ``history_enriched_pre_game``."""
    tracker_event_families: set[str] = {
        r["source_event_family"]
        for r in tracker_rows
        if r.get("source_event_family")
    }

    violations: list[str] = []
    for row in skeleton:
        ps = row["prediction_setting"]
        if ps not in PRE_GAME_OR_HISTORY:
            continue
        src = row.get("source_table_or_event_family", "") or ""
        if _matches_tracker_event_family(src, tracker_event_families):
            violations.append(
                f"feature_family_id='{row['feature_family_id']}' "
                f"prediction_setting='{ps}' "
                f"source_table_or_event_family='{src}'"
            )

    assert not violations, (
        "V-5: tracker-derived rows must NOT use prediction_setting in "
        "{pre_game, history_enriched_pre_game} (Invariant I3 / Amendment 2 "
        f"of PR #208). Violations: {violations}"
    )


def _check_v6_history_strict_lt(skeleton: list[dict[str, Any]]) -> None:
    """V-6: history rows use strict ``<`` and ``details_timeUTC`` provenance."""
    for row in skeleton:
        if row["prediction_setting"] != "history_enriched_pre_game":
            continue

        ffid = row["feature_family_id"]
        cutoff_rule = row["allowed_cutoff_rule"] or ""
        anchor = row["temporal_anchor"]

        assert "<" in cutoff_rule, (
            f"V-6: history row '{ffid}' allowed_cutoff_rule='{cutoff_rule}' "
            "must contain strict '<' operator (CROSS-02-00-v3.0.1 §3.3, "
            "Invariant I3)"
        )
        assert "<=" not in cutoff_rule, (
            f"V-6: history row '{ffid}' allowed_cutoff_rule='{cutoff_rule}' "
            "must NOT contain '<=' (strict inequality only — CROSS-02-00-v3.0.1 §3.3)"
        )

        assert anchor == SC2EGSET_HISTORY_TEMPORAL_ANCHOR, (
            f"V-6: history row '{ffid}' temporal_anchor='{anchor}'; "
            f"expected '{SC2EGSET_HISTORY_TEMPORAL_ANCHOR}' "
            "(CROSS-02-03-v1.0.1 §5.1 — sc2egset-specific provenance anchor)"
        )
        assert anchor != REJECTED_HISTORY_TEMPORAL_ANCHOR, (
            f"V-6: history row '{ffid}' temporal_anchor='{anchor}' "
            "is the cross-dataset alias and is rejected for sc2egset rows "
            "(CROSS-02-03-v1.0.1 §5.1)"
        )

        cutoff_lower = cutoff_rule.lower()
        for token in POST_OUTCOME_FORBIDDEN_TOKENS:
            assert token not in cutoff_lower, (
                f"V-6: history row '{ffid}' allowed_cutoff_rule="
                f"'{cutoff_rule}' references post-outcome token '{token}' "
                "(forbidden — Invariant I3)"
            )


def validate_registry_skeleton(
    skeleton: list[dict[str, Any]], tracker_csv_path: Path | str
) -> None:
    """Run V-1..V-6 structural assertions on the registry skeleton.

    Args:
        skeleton: List of row dicts; one dict per planned feature family.
            Every row must carry exactly the 13 columns enumerated in
            :data:`REQUIRED_COLUMNS`.
        tracker_csv_path: Path to
            ``tracker_events_feature_eligibility.csv`` (the binding
            eligibility evidence for SC2 in_game_snapshot families).

    Raises:
        AssertionError: with a descriptive message naming the failing
            check (V-1..V-6) and the offending row(s) on any structural
            violation.
    """
    _check_v1_schema_integrity(skeleton)
    tracker_rows = _read_tracker_rows(tracker_csv_path)
    _check_v2_tracker_split_counts(tracker_rows)
    _check_v3_blocked_families(skeleton)
    _check_v4_slot_identity_consistency(skeleton, tracker_rows)
    _check_v5_no_tracker_in_pre_game(skeleton, tracker_rows)
    _check_v6_history_strict_lt(skeleton)
