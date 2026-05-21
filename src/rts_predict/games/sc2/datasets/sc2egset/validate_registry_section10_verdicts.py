"""Validation module for SC2EGSet Step 02_01_01 §10 verdict audit (PM-1).

This module implements the CROSS-02-03-v1.0.1 §10 design-time verdict audit
for all 26 feature-family rows in the SC2EGSet registry CSV. It derives the
expected §10 verdict for each row INDEPENDENTLY from the protocol rules and
row evidence, then compares each derived verdict to the registry's recorded
``status`` column, detecting bidirectional drift (F-1a stricter, F-1b looser).

Binding specs:
    - CROSS-02-03-v1.0.1 §10 (four verdicts, §10.1 taxonomy, §10.2 triggers,
      §10.3 tracker special case)
    - CROSS-02-01-v1.0.1 §4 (Materialization definition — lines 117-121)
    - CROSS-02-00-v3.0.1 §3.3 (strict ``<`` for history rows)

Falsifiers implemented (F-1a > F-1b > F-2 > F-3 > F-4 > F-5 > F-6 > F-7):
    F-1a: derived verdict strictly more restrictive than recorded status (HALT).
    F-1b: derived verdict strictly less restrictive than recorded status (HALT).
    F-2: independent §10.2 trigger fires on row recorded as allowed/caveat (HALT).
    F-3: post-game token in allowed_cutoff_rule (HALT).
    F-4: invalid cutoff operator on history row (HALT).
    F-5: D13 tracker contradiction — tracker CSV says blocked but registry says allowed (HALT).
    F-6: slot_identity_consistency not classified sanity_gate_not_model_input (HALT).
    F-7: unrecognised status value (HALT).

Materialized column count is always 0: this is a design-time audit; no feature
columns have been persisted to DuckDB/Parquet at this step
(CROSS-02-01-v1.0.1 §4 Materialization definition).
"""

from __future__ import annotations

import csv
import logging
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Top-level constants — no magic numbers (Invariant I7)
# ---------------------------------------------------------------------------

EXPECTED_ROW_COUNT: int = 26

SECTION10_VERDICTS: frozenset[str] = frozenset(
    {
        "allowed",
        "allowed_with_caveat",
        "blocked_until_validation",
        "sanity_gate_not_model_input",
    }
)

# Dataset-side synonym for spec-side "blocked_until_validation".
# The registry uses the longer form for all currently-blocked rows.
DATASET_SIDE_BLOCKED_SYNONYM: str = "blocked_until_additional_validation"

# All valid status tokens recognised by the comparator (spec-side + synonym).
_ALL_VALID_STATUSES: frozenset[str] = SECTION10_VERDICTS | {
    DATASET_SIDE_BLOCKED_SYNONYM
}

# CROSS-02-00-v3.0.1 §3.3 — strict '<' for history rows.
HISTORY_STRICT_CUTOFF: str = "history_time < target_time"

# In-game snapshot cutoff (CROSS-02-03-v1.0.1 §4 D6).
INGAME_CUTOFF: str = "event.loop <= cutoff_loop"

# Slot identity feature is a sanity gate, not a model input.
SLOT_IDENTITY_FEATURE_ID: str = (
    "sc2egset.in_game_snapshot.slot_identity_consistency"
)

# Tracker eligibility token that blocks a family (D13).
_TRACKER_BLOCKED_TOKEN: str = "blocked_until_additional_validation"

# Tokens in allowed_cutoff_rule that reference post-outcome state (F-3).
_POST_GAME_TOKENS: tuple[str, ...] = (
    "won",
    "final_state",
    "match_result",
    "post_game",
)

# Strictness ordering for drift detection (lower = more permissive).
_VERDICT_RANK: dict[str, int] = {
    "allowed": 0,
    "allowed_with_caveat": 1,
    "sanity_gate_not_model_input": 2,
    "blocked_until_validation": 3,
    # synonym maps to same rank as spec-side token
    DATASET_SIDE_BLOCKED_SYNONYM: 3,
}

# Leakage modes in history rows that are mitigated by the strict-'<' cutoff.
# Rows declaring only these modes + the correct cutoff rule are classified allowed.
_MITIGATED_HISTORY_LEAKAGE_MODES: frozenset[str] = frozenset(
    {
        "rolling_includes_target_game",
        "h2h_includes_target_game",
        "rating_uses_target_game_outcome",
        "none",
    }
)

# Leakage mode that signals a caveat (not a block) on history rows.
_HISTORY_CAVEAT_LEAKAGE_MODE: str = "cross_region_history_drop"

# Leakage modes on in_game_snapshot rows that signal caveat (not block).
_INGAME_CAVEAT_LEAKAGE_MODES: frozenset[str] = frozenset(
    {
        "snapshot_oscillation",
        "lps_caveat_on_5min",
        "fixed_point_scaling_unconfirmed",
        "full_replay_min_loop_blocked",
        "lineage_orphan_drop",
        "upgrade_count_field_unconfirmed",
    }
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Section10Rules:
    """Frozen view of the §10 protocol rules used in derivation.

    Attributes:
        verdicts: The four spec-side §10.1 verdicts.
        blocking_triggers: Human-readable §10.2 trigger labels.
        history_cutoff: Expected strict-'<' token for history rows.
        ingame_cutoff: Expected '<=' token for in-game rows.
        slot_identity_feature_id: The feature_family_id classified as
            sanity_gate_not_model_input.
        sc2_tracker_blocked_token: The tracker eligibility status that
            blocks a family (D13).
        tracker_eligibility_csv_path: Path to tracker_events_feature_eligibility.csv.
    """

    verdicts: frozenset[str]
    blocking_triggers: tuple[str, ...]
    history_cutoff: str
    ingame_cutoff: str
    slot_identity_feature_id: str
    sc2_tracker_blocked_token: str
    tracker_eligibility_csv_path: Path


@dataclass(frozen=True)
class Section10Verdict:
    """Per-row derived verdict and evidence trail.

    Attributes:
        feature_family_id: The row's feature_family_id.
        derived_status: One of SECTION10_VERDICTS (spec-side form, never synonym).
        triggers_fired: §10.2 trigger labels that fired during derivation.
        rule_path: Human-readable derivation path (for diagnostics).
    """

    feature_family_id: str
    derived_status: str
    triggers_fired: tuple[str, ...]
    rule_path: str


@dataclass(frozen=True)
class RegistryVerdictAuditResult:
    """Aggregate result of the full §10 verdict audit.

    Attributes:
        passed: True iff no halting falsifier fired and counts match expectations.
        rows_audited: Number of registry rows processed.
        halting_falsifier: Label of the first matched falsifier (F-1a priority),
            or None if no falsifier fired.
        stricter_drifts: Rows where derived verdict is stricter than recorded
            status. Each entry is (feature_family_id, derived, recorded).
        looser_drifts: Rows where derived verdict is looser than recorded status.
        independent_trigger_hits: Rows where an independent §10.2 trigger
            fired but recorded status is allowed/allowed_with_caveat.
            Each entry is (feature_family_id, trigger_name).
        materialized_column_count: Always 0 — design-time audit; no feature
            columns have been persisted to DuckDB/Parquet
            (CROSS-02-01-v1.0.1 §4 Materialization definition).
    """

    passed: bool
    rows_audited: int
    halting_falsifier: str | None
    stricter_drifts: tuple[tuple[str, str, str], ...]
    looser_drifts: tuple[tuple[str, str, str], ...]
    independent_trigger_hits: tuple[tuple[str, str], ...]
    materialized_column_count: int


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _load_tracker_map(tracker_csv_path: Path) -> dict[str, str]:
    """Load tracker eligibility CSV into a family -> status_in_game_snapshot map.

    Args:
        tracker_csv_path: Path to tracker_events_feature_eligibility.csv.

    Returns:
        Dict mapping feature_family name to status_in_game_snapshot value.

    Raises:
        FileNotFoundError: if the CSV does not exist.
    """
    if not tracker_csv_path.exists():
        raise FileNotFoundError(
            f"Tracker eligibility CSV not found at {tracker_csv_path}"
        )
    with tracker_csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return {
            row["feature_family"]: row["status_in_game_snapshot"]
            for row in reader
        }


def _normalise_status(status: str) -> str:
    """Normalise the dataset-side synonym to the spec-side token.

    Args:
        status: Raw status string from the registry row.

    Returns:
        Spec-side status string (synonym replaced with blocked_until_validation).
    """
    if status == DATASET_SIDE_BLOCKED_SYNONYM:
        return "blocked_until_validation"
    return status


def _derive_pre_game_verdict(
    row_evidence: pd.Series,
) -> Section10Verdict:
    """Derive verdict for a pre_game row.

    Pre-game rows carry static attributes that are fixed at match-start.
    No temporal cutoff is needed; no tracker event families are involved.
    The only blocking path is a §10.2 trigger (e.g., missing grain or
    post-outcome reference), which are checked by the caller.

    Args:
        row_evidence: pd.Series with registry columns, 'status' dropped.

    Returns:
        Section10Verdict with derived_status = 'allowed' (no triggers fire
        for well-formed pre_game rows in the registry).
    """
    ffid = str(row_evidence["feature_family_id"])
    # F-3 post-game token check
    cutoff_rule = str(row_evidence.get("allowed_cutoff_rule", "") or "")
    for token in _POST_GAME_TOKENS:
        if token in cutoff_rule.lower():
            return Section10Verdict(
                feature_family_id=ffid,
                derived_status="blocked_until_validation",
                triggers_fired=(f"F-3:post_game_token:{token}",),
                rule_path=f"pre_game -> F-3 post_game token '{token}' in cutoff_rule",
            )
    return Section10Verdict(
        feature_family_id=ffid,
        derived_status="allowed",
        triggers_fired=(),
        rule_path="pre_game -> no triggers -> allowed",
    )


def _derive_history_verdict(
    row_evidence: pd.Series,
) -> Section10Verdict:
    """Derive verdict for a history_enriched_pre_game row.

    History rows must declare strict '<' in allowed_cutoff_rule
    (CROSS-02-00-v3.0.1 §3.3). The candidate_leakage_modes field
    declares which leakage mode the family's strict-'<' cutoff mitigates.
    All modes in _MITIGATED_HISTORY_LEAKAGE_MODES are considered mitigated
    by the correct cutoff rule. The cross_region_history_drop mode is a
    declared caveat, yielding allowed_with_caveat.

    Args:
        row_evidence: pd.Series with registry columns, 'status' dropped.

    Returns:
        Section10Verdict with derived_status determined by cutoff + leakage analysis.
    """
    ffid = str(row_evidence["feature_family_id"])
    cutoff_rule = str(row_evidence.get("allowed_cutoff_rule", "") or "")
    leakage = str(row_evidence.get("candidate_leakage_modes", "") or "")

    # F-3: post-game token check
    for token in _POST_GAME_TOKENS:
        if token in cutoff_rule.lower():
            return Section10Verdict(
                feature_family_id=ffid,
                derived_status="blocked_until_validation",
                triggers_fired=(f"F-3:post_game_token:{token}",),
                rule_path=(
                    f"history_enriched_pre_game -> F-3 post_game token '{token}'"
                ),
            )

    # F-4: must contain strict '<' and NOT contain '<='
    if "<=" in cutoff_rule:
        return Section10Verdict(
            feature_family_id=ffid,
            derived_status="blocked_until_validation",
            triggers_fired=("F-4:invalid_cutoff_operator:<=",),
            rule_path="history_enriched_pre_game -> F-4 '<=' found in cutoff_rule",
        )
    if "<" not in cutoff_rule:
        return Section10Verdict(
            feature_family_id=ffid,
            derived_status="blocked_until_validation",
            triggers_fired=("F-4:missing_strict_lt",),
            rule_path="history_enriched_pre_game -> F-4 strict '<' missing",
        )

    # Caveat: cross_region_history_drop is a declared caveat, not a block
    if leakage == _HISTORY_CAVEAT_LEAKAGE_MODE:
        return Section10Verdict(
            feature_family_id=ffid,
            derived_status="allowed_with_caveat",
            triggers_fired=(),
            rule_path=(
                "history_enriched_pre_game -> strict '<' present -> "
                "leakage=cross_region_history_drop -> allowed_with_caveat"
            ),
        )

    # All other history leakage modes are mitigated by the strict-'<' cutoff
    return Section10Verdict(
        feature_family_id=ffid,
        derived_status="allowed",
        triggers_fired=(),
        rule_path=(
            f"history_enriched_pre_game -> strict '<' present -> "
            f"leakage={leakage!r} mitigated -> allowed"
        ),
    )


def _derive_ingame_verdict(
    row_evidence: pd.Series,
    tracker_map: dict[str, str],
    slot_identity_feature_id: str,
    tracker_blocked_token: str,
) -> Section10Verdict:
    """Derive verdict for an in_game_snapshot row.

    In-game rows are cross-checked against the tracker eligibility CSV (D13).
    The slot_identity_consistency family is always classified as
    sanity_gate_not_model_input (F-6 guard). Tracker-blocked families yield
    blocked_until_validation. Families with caveat modes or eligible_with_caveat
    tracker status yield allowed_with_caveat. Others yield allowed.

    Args:
        row_evidence: pd.Series with registry columns, 'status' dropped.
        tracker_map: feature_family -> status_in_game_snapshot from tracker CSV.
        slot_identity_feature_id: The feature_family_id for the sanity gate.
        tracker_blocked_token: The tracker status that blocks a family.

    Returns:
        Section10Verdict with derived_status.
    """
    ffid = str(row_evidence["feature_family_id"])
    leakage = str(row_evidence.get("candidate_leakage_modes", "") or "")

    # F-6: slot identity is always sanity_gate_not_model_input
    if ffid == slot_identity_feature_id:
        return Section10Verdict(
            feature_family_id=ffid,
            derived_status="sanity_gate_not_model_input",
            triggers_fired=(),
            rule_path=(
                "in_game_snapshot -> slot_identity_consistency"
                " -> sanity_gate_not_model_input"
            ),
        )

    # Extract family short name (last dot-segment) for tracker CSV lookup
    family_short = ffid.rsplit(".", 1)[-1] if "." in ffid else ffid

    # F-5 / D13: tracker CSV check
    tracker_status = tracker_map.get(family_short, "")
    if tracker_status == tracker_blocked_token:
        return Section10Verdict(
            feature_family_id=ffid,
            derived_status="blocked_until_validation",
            triggers_fired=(f"F-5:D13:tracker_blocked:{family_short}",),
            rule_path=(
                "in_game_snapshot -> tracker CSV says "
                "blocked_until_additional_validation -> blocked_until_validation"
            ),
        )

    # Caveat leakage modes or eligible_with_caveat tracker status
    if leakage in _INGAME_CAVEAT_LEAKAGE_MODES:
        return Section10Verdict(
            feature_family_id=ffid,
            derived_status="allowed_with_caveat",
            triggers_fired=(),
            rule_path=(
                f"in_game_snapshot -> caveat leakage mode '{leakage}' -> "
                f"allowed_with_caveat"
            ),
        )
    if tracker_status == "eligible_with_caveat":
        return Section10Verdict(
            feature_family_id=ffid,
            derived_status="allowed_with_caveat",
            triggers_fired=(),
            rule_path=(
                "in_game_snapshot -> tracker eligible_with_caveat -> "
                "allowed_with_caveat"
            ),
        )

    return Section10Verdict(
        feature_family_id=ffid,
        derived_status="allowed",
        triggers_fired=(),
        rule_path="in_game_snapshot -> no caveat/block -> allowed",
    )


def _evaluate_independent_triggers(
    row_evidence: pd.Series,
    tracker_map: dict[str, str],
    tracker_blocked_token: str,
    slot_identity_feature_id: str,
) -> list[str]:
    """Evaluate all §10.2 blocking triggers independently on a row.

    This function does NOT read 'status'. It returns the list of trigger
    labels that fire. Used for F-2 independent trigger evaluation.

    Args:
        row_evidence: pd.Series with registry columns, 'status' dropped.
        tracker_map: feature_family -> status_in_game_snapshot.
        tracker_blocked_token: The tracker status that triggers a block.
        slot_identity_feature_id: The sanity-gate feature_family_id.

    Returns:
        List of trigger label strings that fired.
    """
    triggers: list[str] = []
    ps = str(row_evidence.get("prediction_setting", "") or "")
    ffid = str(row_evidence["feature_family_id"])
    cutoff_rule = str(row_evidence.get("allowed_cutoff_rule", "") or "")
    leakage = str(row_evidence.get("candidate_leakage_modes", "") or "")

    # F-3: post-game tokens
    for token in _POST_GAME_TOKENS:
        if token in cutoff_rule.lower():
            triggers.append(f"F-3:post_game_token:{token}")

    # F-4: history row with invalid cutoff
    if ps == "history_enriched_pre_game":
        if "<=" in cutoff_rule:
            triggers.append("F-4:invalid_cutoff_operator:<=")
        elif "<" not in cutoff_rule:
            triggers.append("F-4:missing_strict_lt")

    # F-5: D13 tracker contradiction for in_game_snapshot
    if ps == "in_game_snapshot" and ffid != slot_identity_feature_id:
        family_short = ffid.rsplit(".", 1)[-1] if "." in ffid else ffid
        tracker_status = tracker_map.get(family_short, "")
        if tracker_status == tracker_blocked_token:
            triggers.append(f"F-5:D13:tracker_blocked:{family_short}")

    # F-6: slot identity gate misuse (any verdict other than sanity_gate)
    if ffid == slot_identity_feature_id:
        # trigger fires only if independent derivation would route to sanity_gate
        # and current status is NOT sanity_gate (checked by caller)
        triggers.append("F-6:slot_identity_gate")

    # Missing grain trigger
    if not str(row_evidence.get("source_grain", "") or "").strip():
        triggers.append("trigger:missing_source_grain")
    if not str(row_evidence.get("model_input_grain", "") or "").strip():
        triggers.append("trigger:missing_model_input_grain")

    # Missing prediction setting trigger
    if not ps.strip():
        triggers.append("trigger:missing_prediction_setting")

    # Missing temporal anchor trigger
    anchor = str(row_evidence.get("temporal_anchor", "") or "")
    if not anchor.strip():
        triggers.append("trigger:missing_temporal_anchor")

    # Tracker pre-game regression (§10.3)
    src = str(row_evidence.get("source_table_or_event_family", "") or "")
    if ps in {"pre_game", "history_enriched_pre_game"} and src.startswith(
        "tracker_events_raw"
    ):
        triggers.append("trigger:tracker_in_pre_game")

    # Leakage mode "blocked" on a non-blocked row
    if leakage == "blocked" and ps != "blocked_or_deferred":
        triggers.append("trigger:blocked_leakage_on_non_blocked_row")

    return triggers


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_registry_rows(registry_csv_path: Path) -> list[pd.Series]:
    """Load the 26-row registry CSV, enforcing S-1 / S-2 / S-3.

    Sanity checks inline:
        S-1: CSV exists on disk.
        S-2: Exactly 26 data rows (excluding header).
        S-3: All feature_family_id values are unique.

    Args:
        registry_csv_path: Path to 02_01_01_feature_family_registry.csv.

    Returns:
        List of pd.Series, one per data row (excluding header). Each Series
        index is the column names from the CSV header.

    Raises:
        FileNotFoundError: if CSV does not exist (S-1).
        ValueError: if row count != 26 (S-2) or duplicate feature_family_id (S-3).
    """
    if not registry_csv_path.exists():
        raise FileNotFoundError(
            f"S-1 FAIL: Registry CSV not found at {registry_csv_path}"
        )
    df = pd.read_csv(registry_csv_path, dtype=str, keep_default_na=False)
    row_count = len(df)
    if row_count != EXPECTED_ROW_COUNT:
        raise ValueError(
            f"S-2 FAIL: Expected {EXPECTED_ROW_COUNT} data rows, got {row_count}. "
            f"Path: {registry_csv_path}"
        )
    ids = df["feature_family_id"].tolist()
    seen: set[str] = set()
    for fid in ids:
        if fid in seen:
            raise ValueError(
                f"S-3 FAIL: Duplicate feature_family_id '{fid}' in registry."
            )
        seen.add(fid)
    logger.debug(
        "load_registry_rows: loaded %d rows from %s",
        row_count,
        registry_csv_path,
    )
    return [df.iloc[i] for i in range(len(df))]


def derive_section10_verdict(
    row: pd.Series,
    protocol_rules: Section10Rules,
) -> Section10Verdict:
    """Derive the §10 verdict for a single registry row from protocol rules + row evidence.

    The function does NOT read ``row['status']`` — the registry's recorded status is
    excluded from the derivation input set. To make accidental reads structurally
    impossible, the function projects the row to a view that explicitly drops the
    'status' column before any rule evaluation:

        row_evidence = row.drop(labels=[s for s in ('status',) if s in row.index])

    All rule evaluation operates exclusively on ``row_evidence``.

    Args:
        row: pd.Series with registry columns. Must contain 'prediction_setting',
            'allowed_cutoff_rule', 'candidate_leakage_modes', 'feature_family_id',
            'source_table_or_event_family'. Must NOT be read for 'status'.
        protocol_rules: Frozen §10 rule set, including tracker CSV path.

    Returns:
        Section10Verdict with the derived status and evidence trail.
    """
    # Structural independence guard (Mod nit #1): drop 'status' before evaluation.
    row_evidence = row.drop(labels=[s for s in ("status",) if s in row.index])

    tracker_map = _load_tracker_map(protocol_rules.tracker_eligibility_csv_path)
    ps = str(row_evidence.get("prediction_setting", "") or "")

    if ps == "pre_game":
        return _derive_pre_game_verdict(row_evidence)
    if ps == "history_enriched_pre_game":
        return _derive_history_verdict(row_evidence)
    if ps == "in_game_snapshot":
        return _derive_ingame_verdict(
            row_evidence,
            tracker_map,
            protocol_rules.slot_identity_feature_id,
            protocol_rules.sc2_tracker_blocked_token,
        )
    # blocked_or_deferred and anything unrecognised -> blocked_until_validation
    ffid = str(row_evidence.get("feature_family_id", "<unknown>"))
    return Section10Verdict(
        feature_family_id=ffid,
        derived_status="blocked_until_validation",
        triggers_fired=(),
        rule_path=f"prediction_setting={ps!r} -> blocked_until_validation",
    )


def compare_registry_verdicts(
    rows: list[pd.Series],
    protocol_rules: Section10Rules,
) -> RegistryVerdictAuditResult:
    """Compare independently derived §10 verdicts against registry recorded status.

    Step order (S-4 enforced):
    1. First pass: derive all row verdicts independently (no status reads).
    2. Second pass: compare each derived verdict to row['status'].
    3. Classify stricter drifts (F-1a) and looser drifts (F-1b).
    4. Run independent §10.2 trigger checklist on every row (F-2).
    5. Set halting_falsifier in priority: F-1a > F-1b > F-2 > F-3 > F-4 > F-5 > F-6 > F-7.
    6. Set materialized_column_count = 0 (S-5).
    7. Set passed = (no halting_falsifier AND drifts empty AND triggers empty AND rows == 26).

    Args:
        rows: List of pd.Series from load_registry_rows.
        protocol_rules: Frozen §10 rule set.

    Returns:
        RegistryVerdictAuditResult with full audit summary.
    """
    tracker_map = _load_tracker_map(protocol_rules.tracker_eligibility_csv_path)

    # --- Pass 1: derive all verdicts independently (S-4) ---
    derived: dict[str, Section10Verdict] = {}
    for row in rows:
        verdict = derive_section10_verdict(row, protocol_rules)
        derived[verdict.feature_family_id] = verdict

    # --- Pass 2: compare to recorded status ---
    stricter_drifts: list[tuple[str, str, str]] = []
    looser_drifts: list[tuple[str, str, str]] = []
    f7_hits: list[str] = []

    for row in rows:
        ffid = str(row.get("feature_family_id", "<unknown>"))
        recorded_raw = str(row.get("status", "") or "")

        # F-7: unrecognised status token
        if recorded_raw not in _ALL_VALID_STATUSES:
            f7_hits.append(ffid)
            continue

        recorded_norm = _normalise_status(recorded_raw)
        derived_status = derived[ffid].derived_status

        derived_rank = _VERDICT_RANK.get(derived_status, -1)
        recorded_rank = _VERDICT_RANK.get(recorded_norm, -1)

        if derived_rank > recorded_rank:
            stricter_drifts.append((ffid, derived_status, recorded_raw))
        elif derived_rank < recorded_rank:
            looser_drifts.append((ffid, derived_status, recorded_raw))

    # --- F-2: independent §10.2 trigger checklist (no status read) ---
    independent_trigger_hits: list[tuple[str, str]] = []
    for row in rows:
        ffid = str(row.get("feature_family_id", "<unknown>"))
        recorded_raw = str(row.get("status", "") or "")
        # Only flag rows classified as allowed/caveat that fire a trigger
        if recorded_raw in {
            "allowed",
            "allowed_with_caveat",
        }:
            row_evidence = row.drop(
                labels=[s for s in ("status",) if s in row.index]
            )
            hits = _evaluate_independent_triggers(
                row_evidence,
                tracker_map,
                protocol_rules.sc2_tracker_blocked_token,
                protocol_rules.slot_identity_feature_id,
            )
            # F-6 hit on slot_identity is expected (it derives sanity_gate);
            # only report if the recorded status is NOT sanity_gate_not_model_input.
            for h in hits:
                if h == "F-6:slot_identity_gate":
                    # slot_identity should not be allowed/caveat; it would be
                    # caught by F-1a/F-1b; don't double-count
                    continue
                independent_trigger_hits.append((ffid, h))

    # --- Determine halting falsifier (priority order) ---
    halting_falsifier: str | None = None
    if stricter_drifts:
        halting_falsifier = "F-1a"
    elif looser_drifts:
        halting_falsifier = "F-1b"
    elif independent_trigger_hits:
        halting_falsifier = "F-2"
    elif f7_hits:
        halting_falsifier = "F-7"

    # --- S-5: materialized_column_count is always 0 ---
    materialized_column_count: int = 0

    passed = (
        halting_falsifier is None
        and len(stricter_drifts) == 0
        and len(looser_drifts) == 0
        and len(independent_trigger_hits) == 0
        and len(rows) == EXPECTED_ROW_COUNT
    )

    logger.debug(
        "compare_registry_verdicts: rows=%d stricter=%d looser=%d "
        "triggers=%d f7=%d passed=%s",
        len(rows),
        len(stricter_drifts),
        len(looser_drifts),
        len(independent_trigger_hits),
        len(f7_hits),
        passed,
    )

    return RegistryVerdictAuditResult(
        passed=passed,
        rows_audited=len(rows),
        halting_falsifier=halting_falsifier,
        stricter_drifts=tuple(stricter_drifts),
        looser_drifts=tuple(looser_drifts),
        independent_trigger_hits=tuple(independent_trigger_hits),
        materialized_column_count=materialized_column_count,
    )


def validate_registry_section10_verdicts(
    registry_csv_path: Path,
    tracker_csv_path: Path,
) -> RegistryVerdictAuditResult:
    """Entry point: load registry rows and run the full §10 verdict audit.

    Args:
        registry_csv_path: Path to 02_01_01_feature_family_registry.csv.
        tracker_csv_path: Path to tracker_events_feature_eligibility.csv.

    Returns:
        RegistryVerdictAuditResult. Caller is responsible for asserting .passed.
    """
    protocol_rules = Section10Rules(
        verdicts=SECTION10_VERDICTS,
        blocking_triggers=(
            "missing_grain",
            "missing_prediction_setting",
            "ambiguous_temporal_anchor",
            "history_lacking_strict_lt",
            "tracker_absent_or_blocked",
            "aoe2_source_label_regression",
            "pseudocount_without_derivation",
            "feature_table_generation_attempted_before_audit",
        ),
        history_cutoff=HISTORY_STRICT_CUTOFF,
        ingame_cutoff=INGAME_CUTOFF,
        slot_identity_feature_id=SLOT_IDENTITY_FEATURE_ID,
        sc2_tracker_blocked_token=_TRACKER_BLOCKED_TOKEN,
        tracker_eligibility_csv_path=tracker_csv_path,
    )
    rows = load_registry_rows(registry_csv_path)
    return compare_registry_verdicts(rows, protocol_rules)
