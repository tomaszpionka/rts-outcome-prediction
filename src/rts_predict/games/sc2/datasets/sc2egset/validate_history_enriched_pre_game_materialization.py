"""Validation module for SC2EGSet Step 02_01_03 history-enriched pre_game tranche scaffold.

This module validates the DESIGN CONTRACT for the 6 tranche-2
``history_enriched_pre_game`` feature families against the closed 02_01_01
registry CSV. It does NOT materialize any feature value, does NOT run
projection SQL against feature data, and does NOT write any artifact.
``materialized_output_paths`` is always ``()``.

Binding sources:
    - Closed 02_01_01 registry CSV (authoritative catalog for tranche-2 scope).
    - ROADMAP Step 02_01_03 block (lines 2274-2523 of the dataset ROADMAP).
    - CROSS-02-00-v1.0.1 §3.3 (strict-< history cutoff) and §5.4 (SC2
      IN_GAME_HISTORICAL telemetry-scope retention).
    - CROSS-02-01-v1.0.1 §2.2 (POST-GAME token absence).
    - CROSS-02-02-v1.0.1 §6.2 (6 history families; row 5 cross_region;
      row 6 in_game_history_aggregate IN_GAME_HISTORICAL retention) and §9
      (cold-start gates G-CS-2..G-CS-6).
    - Invariant I3 (no tracker in history_enriched_pre_game tranche).
    - Invariant I5 (symmetric focal/opponent construction).
    - Invariant I7 (no magic numbers — module-level UPPER_SNAKE constants).

Falsifiers implemented (priority order; first to fire halts):
    missing_families_in_tranche, extra_history_in_tranche,
    pre_game_in_history_tranche, in_game_in_history_tranche,
    blocked_in_history_tranche, tranche_count_mismatch,
    wrong_prediction_setting, wrong_temporal_anchor, cutoff_not_strict,
    tracker_source_in_history, asymmetric_construction, post_game_token,
    cross_region_caveat_missing, in_game_historical_column_out_of_scope,
    cold_start_gate_invalid, status_not_admissible.
"""

from __future__ import annotations

import csv
import logging
from dataclasses import dataclass, field
from pathlib import Path

LOGGER = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level constants — no magic numbers (Invariant I7)
# ---------------------------------------------------------------------------

HISTORY_TRANCHE2_FAMILY_IDS: frozenset[str] = frozenset(
    {
        "sc2egset.history_enriched_pre_game.focal_player_history",
        "sc2egset.history_enriched_pre_game.opponent_player_history",
        "sc2egset.history_enriched_pre_game.matchup_history_aggregate",
        "sc2egset.history_enriched_pre_game.reconstructed_rating",
        "sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling",
        "sc2egset.history_enriched_pre_game.in_game_history_aggregate",
    }
)
EXPECTED_TRANCHE2_COUNT: int = 6
HISTORY_PREDICTION_SETTING: str = "history_enriched_pre_game"
EXPECTED_TEMPORAL_ANCHOR: str = "details_timeUTC"
EXPECTED_ALLOWED_CUTOFF_RULE: str = "history_time < target_time"
EXPECTED_PER_PLAYER_CONSTRUCTION: str = "symmetric"

# Registry-bound set; G-CS-6 is a materialization-time fold-aware fit gate per
# CROSS-02-02 §9 and ROADMAP lines 2334-2338, intentionally excluded here.
ALLOWED_HISTORY_COLD_START_GATES: frozenset[str] = frozenset(
    {"G-CS-2", "G-CS-3", "G-CS-4", "G-CS-5"}
)
ALLOWED_HISTORY_STATUSES: frozenset[str] = frozenset(
    {"allowed", "allowed_with_caveat"}
)

CROSS_REGION_FAMILY_ID: str = (
    "sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling"
)
CROSS_REGION_EXPECTED_STATUS: str = "allowed_with_caveat"

IN_GAME_HISTORY_AGG_FAMILY_ID: str = (
    "sc2egset.history_enriched_pre_game.in_game_history_aggregate"
)
IN_GAME_HISTORICAL_AGGREGATED_COLUMNS: tuple[str, ...] = (
    "APM",
    "SQ",
    "supplyCappedPercent",
    "header_elapsedGameLoops",
)

FORBIDDEN_CUTOFF_OPERATORS: tuple[str, ...] = ("<=", "==", ">=")
TRACKER_SOURCE_PREFIX: str = "tracker_events_raw"
PRE_GAME_PREDICTION_SETTING: str = "pre_game"
IN_GAME_PREDICTION_SETTING: str = "in_game_snapshot"
BLOCKED_PREDICTION_SETTING: str = "blocked_or_deferred"

TRUE_REGISTRY_CSV_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_01_feature_family_registry.csv"
)
STALE_REGISTRY_FILENAME_FRAGMENT: str = (
    "02_01_01_feature_family_registry_sc2egset.csv"
)

POST_GAME_TOKENS: tuple[str, ...] = (
    "won",
    "win",
    "loss",
    "result",
    "final_state",
    "match_result",
    "post_game",
    "outcome",
    "winner",
    "is_decisive",
)

# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HistoryEnrichedPreGameTrancheRow:
    """Frozen view of a single tranche-2 history-enriched pre_game registry row.

    Attributes:
        feature_family_id: The row's feature_family_id.
        prediction_setting: Must equal HISTORY_PREDICTION_SETTING.
        source_table_or_event_family: The registry-recorded source table.
        temporal_anchor: Must equal EXPECTED_TEMPORAL_ANCHOR.
        allowed_cutoff_rule: Must equal EXPECTED_ALLOWED_CUTOFF_RULE.
        candidate_leakage_modes: Registry-recorded candidate leakage modes.
        cold_start_handling: Must be in ALLOWED_HISTORY_COLD_START_GATES.
        status: Must be in ALLOWED_HISTORY_STATUSES.
        per_player_construction: Must equal EXPECTED_PER_PLAYER_CONSTRUCTION.
    """

    feature_family_id: str
    prediction_setting: str
    source_table_or_event_family: str
    temporal_anchor: str
    allowed_cutoff_rule: str
    candidate_leakage_modes: str
    cold_start_handling: str
    status: str
    per_player_construction: str


@dataclass(frozen=True)
class HistoryEnrichedScaffoldValidationResult:
    """Aggregate result of the history-enriched pre_game scaffold validation.

    Attributes:
        passed: True iff no halting falsifier fired.
        tranche_family_ids: Tuple of family_ids loaded from the tranche.
        tranche_count: Count of tranche-2 rows loaded.
        missing_families_in_tranche: Expected tranche-2 family_ids absent
            from the loaded tranche, sorted for determinism.
        extra_history_in_tranche: history_enriched_pre_game family_ids in
            the full registry NOT in HISTORY_TRANCHE2_FAMILY_IDS.
        pre_game_aliases_in_tranche: pre_game family rows that alias a
            tranche-2 family_id.
        in_game_aliases_in_tranche: in_game_snapshot family rows that alias
            a tranche-2 family_id.
        blocked_aliases_in_tranche: blocked_or_deferred family rows that
            alias a tranche-2 family_id.
        wrong_prediction_setting_rows: Tranche rows whose prediction_setting
            != HISTORY_PREDICTION_SETTING.
        wrong_temporal_anchor_rows: Tranche rows whose temporal_anchor
            != EXPECTED_TEMPORAL_ANCHOR.
        cutoff_violations: (family_id, allowed_cutoff_rule) pairs whose rule
            is not strictly EXPECTED_ALLOWED_CUTOFF_RULE or contains a
            FORBIDDEN_CUTOFF_OPERATORS token.
        tracker_source_in_history: Tranche family_ids whose source starts
            with TRACKER_SOURCE_PREFIX.
        asymmetric_construction: Tranche family_ids with
            per_player_construction != "symmetric".
        post_game_token_hits: (family_id, token) pairs where a POST_GAME
            token appears as a boundary-aware token of a designed name, or
            as a substring of a registry source field.
        cross_region_caveat_ok: True iff the cross_region row is present
            in tranche rows AND its status == CROSS_REGION_EXPECTED_STATUS.
        in_game_historical_out_of_scope: Designed IN_GAME_HISTORICAL columns
            NOT in IN_GAME_HISTORICAL_AGGREGATED_COLUMNS.
        cold_start_gate_violations: (family_id, cold_start_handling) pairs
            whose handling is NOT in ALLOWED_HISTORY_COLD_START_GATES.
        status_violations: (family_id, status) pairs whose status is NOT in
            ALLOWED_HISTORY_STATUSES.
        materialized_output_paths: ALWAYS () — scaffold persists nothing.
        halting_falsifier: Label of the first falsifier that fired, or None.
    """

    passed: bool
    tranche_family_ids: tuple[str, ...]
    tranche_count: int
    missing_families_in_tranche: tuple[str, ...]
    extra_history_in_tranche: tuple[str, ...]
    pre_game_aliases_in_tranche: tuple[str, ...]
    in_game_aliases_in_tranche: tuple[str, ...]
    blocked_aliases_in_tranche: tuple[str, ...]
    wrong_prediction_setting_rows: tuple[str, ...]
    wrong_temporal_anchor_rows: tuple[str, ...]
    cutoff_violations: tuple[tuple[str, str], ...]
    tracker_source_in_history: tuple[str, ...]
    asymmetric_construction: tuple[str, ...]
    post_game_token_hits: tuple[tuple[str, str], ...]
    cross_region_caveat_ok: bool
    in_game_historical_out_of_scope: tuple[str, ...]
    cold_start_gate_violations: tuple[tuple[str, str], ...]
    status_violations: tuple[tuple[str, str], ...]
    materialized_output_paths: tuple[str, ...] = field(default_factory=tuple)
    halting_falsifier: str | None = None


# ---------------------------------------------------------------------------
# Public loader
# ---------------------------------------------------------------------------


def load_history_enriched_pre_game_tranche_rows(
    registry_csv_path: Path | str,
) -> list[HistoryEnrichedPreGameTrancheRow]:
    """Load only the 6 tranche-2 history-enriched pre_game rows from the registry CSV.

    Args:
        registry_csv_path: Path to 02_01_01_feature_family_registry.csv.

    Returns:
        List of HistoryEnrichedPreGameTrancheRow, one per tranche-2 family.

    Raises:
        ValueError: if the path contains STALE_REGISTRY_FILENAME_FRAGMENT.
        FileNotFoundError: if the CSV does not exist.
    """
    path = Path(registry_csv_path)
    if STALE_REGISTRY_FILENAME_FRAGMENT in str(path):
        raise ValueError(
            f"Stale registry path detected: '{path}' contains the deprecated "
            f"fragment '{STALE_REGISTRY_FILENAME_FRAGMENT}'. "
            f"Use the true path: '{TRUE_REGISTRY_CSV_RELPATH}'."
        )
    if not path.exists():
        raise FileNotFoundError(f"Registry CSV not found at {path}")
    rows: list[HistoryEnrichedPreGameTrancheRow] = []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            fid = row.get("feature_family_id", "")
            if fid in HISTORY_TRANCHE2_FAMILY_IDS:
                rows.append(
                    HistoryEnrichedPreGameTrancheRow(
                        feature_family_id=fid,
                        prediction_setting=row.get("prediction_setting", ""),
                        source_table_or_event_family=row.get(
                            "source_table_or_event_family", ""
                        ),
                        temporal_anchor=row.get("temporal_anchor", ""),
                        allowed_cutoff_rule=row.get(
                            "allowed_cutoff_rule", ""
                        ),
                        candidate_leakage_modes=row.get(
                            "candidate_leakage_modes", ""
                        ),
                        cold_start_handling=row.get(
                            "cold_start_handling", ""
                        ),
                        status=row.get("status", ""),
                        per_player_construction=row.get(
                            "per_player_construction", ""
                        ),
                    )
                )
    LOGGER.debug(
        "load_history_enriched_pre_game_tranche_rows: loaded %d tranche-2 rows from %s",
        len(rows),
        path,
    )
    return rows


def _load_full_registry(registry_csv_path: Path) -> list[dict[str, str]]:
    """Load all rows from the registry CSV as plain dicts.

    Args:
        registry_csv_path: Path to the registry CSV.

    Returns:
        List of row dicts, one per data row.
    """
    with registry_csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


# ---------------------------------------------------------------------------
# Private check helpers
# ---------------------------------------------------------------------------


def _check_tranche_membership(
    rows: list[HistoryEnrichedPreGameTrancheRow],
    full_registry: list[dict[str, str]],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Check that the tranche contains exactly HISTORY_TRANCHE2_FAMILY_IDS.

    Args:
        rows: Loaded tranche-2 rows.
        full_registry: All rows from the registry CSV.

    Returns:
        (tranche_family_ids, missing_families_in_tranche, extra_history_beyond_tranche).
    """
    tranche_ids = tuple(r.feature_family_id for r in rows)
    missing: tuple[str, ...] = tuple(
        sorted(HISTORY_TRANCHE2_FAMILY_IDS - set(tranche_ids))
    )
    extra: list[str] = []
    for row in full_registry:
        fid = row.get("feature_family_id", "")
        ps = row.get("prediction_setting", "")
        if ps == HISTORY_PREDICTION_SETTING and fid not in HISTORY_TRANCHE2_FAMILY_IDS:
            extra.append(fid)
    return tranche_ids, missing, tuple(sorted(extra))


def _check_aliasing_in_tranche(
    full_registry: list[dict[str, str]],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Check no pre_game / in_game / blocked family aliases a tranche-2 family_id.

    Args:
        full_registry: All rows from the registry CSV.

    Returns:
        (pre_game_aliases, in_game_aliases, blocked_aliases) — should be all ().
    """
    pre_game_hits: list[str] = []
    in_game_hits: list[str] = []
    blocked_hits: list[str] = []
    for row in full_registry:
        fid = row.get("feature_family_id", "")
        ps = row.get("prediction_setting", "")
        if fid in HISTORY_TRANCHE2_FAMILY_IDS:
            if ps == PRE_GAME_PREDICTION_SETTING:
                pre_game_hits.append(fid)
            elif ps == IN_GAME_PREDICTION_SETTING:
                in_game_hits.append(fid)
            elif ps == BLOCKED_PREDICTION_SETTING:
                blocked_hits.append(fid)
    return tuple(pre_game_hits), tuple(in_game_hits), tuple(blocked_hits)


def _check_prediction_setting(
    rows: list[HistoryEnrichedPreGameTrancheRow],
) -> tuple[str, ...]:
    """Return tranche family_ids whose prediction_setting != HISTORY_PREDICTION_SETTING.

    Args:
        rows: Loaded tranche-2 rows.

    Returns:
        Tuple of family_ids with the wrong prediction_setting.
    """
    return tuple(
        r.feature_family_id
        for r in rows
        if r.prediction_setting != HISTORY_PREDICTION_SETTING
    )


def _check_temporal_anchor(
    rows: list[HistoryEnrichedPreGameTrancheRow],
) -> tuple[str, ...]:
    """Return tranche family_ids whose temporal_anchor != EXPECTED_TEMPORAL_ANCHOR.

    Args:
        rows: Loaded tranche-2 rows.

    Returns:
        Tuple of family_ids with the wrong temporal anchor (CROSS-02-00 §3.2).
    """
    return tuple(
        r.feature_family_id
        for r in rows
        if r.temporal_anchor != EXPECTED_TEMPORAL_ANCHOR
    )


def _check_cutoff_rule_is_strict(
    rows: list[HistoryEnrichedPreGameTrancheRow],
) -> tuple[tuple[str, str], ...]:
    """Return (family_id, allowed_cutoff_rule) pairs whose rule is not strict.

    A cutoff rule is rejected if it differs from EXPECTED_ALLOWED_CUTOFF_RULE
    or contains any FORBIDDEN_CUTOFF_OPERATORS token ("<=", "==", ">=").

    Args:
        rows: Loaded tranche-2 rows.

    Returns:
        Tuple of (family_id, allowed_cutoff_rule) pairs in violation.
    """
    hits: list[tuple[str, str]] = []
    for r in rows:
        rule = r.allowed_cutoff_rule
        if rule != EXPECTED_ALLOWED_CUTOFF_RULE:
            hits.append((r.feature_family_id, rule))
            continue
        for forbidden in FORBIDDEN_CUTOFF_OPERATORS:
            if forbidden in rule:
                hits.append((r.feature_family_id, rule))
                break
    return tuple(hits)


def _check_no_tracker_source(
    rows: list[HistoryEnrichedPreGameTrancheRow],
) -> tuple[str, ...]:
    """Return tranche family_ids whose source starts with TRACKER_SOURCE_PREFIX.

    Args:
        rows: Loaded tranche-2 rows.

    Returns:
        Tuple of family_ids with a tracker source (Invariant I3 violation).
    """
    return tuple(
        r.feature_family_id
        for r in rows
        if r.source_table_or_event_family.startswith(TRACKER_SOURCE_PREFIX)
    )


def _check_symmetry(
    rows: list[HistoryEnrichedPreGameTrancheRow],
) -> tuple[str, ...]:
    """Return tranche family_ids with per_player_construction != "symmetric".

    Args:
        rows: Loaded tranche-2 rows.

    Returns:
        Tuple of family_ids with asymmetric construction (Invariant I5 violation).
    """
    return tuple(
        r.feature_family_id
        for r in rows
        if r.per_player_construction != EXPECTED_PER_PLAYER_CONSTRUCTION
    )


def _check_no_post_game_tokens(
    rows: list[HistoryEnrichedPreGameTrancheRow],
    designed_column_names: tuple[str, ...],
) -> tuple[tuple[str, str], ...]:
    """Return (family_id, token) pairs where a POST_GAME token is detected.

    Detection applies boundary-aware token equality on designed column names
    and substring check on registry source fields.

    Args:
        rows: Loaded tranche-2 rows.
        designed_column_names: Planned focal/opponent column-name tuple.

    Returns:
        Tuple of (family_id, token) pairs — should be empty for a clean scaffold.
    """
    hits: list[tuple[str, str]] = []
    for col in designed_column_names:
        col_tokens = set(col.lower().split("_"))
        for token in POST_GAME_TOKENS:
            if token in col_tokens:
                hits.append(("designed_columns", token))
                break
    for row in rows:
        src = row.source_table_or_event_family.lower()
        for token in POST_GAME_TOKENS:
            if token in src:
                hits.append((row.feature_family_id, token))
    return tuple(hits)


def _check_cross_region_caveat(
    rows: list[HistoryEnrichedPreGameTrancheRow],
) -> bool:
    """Return True iff cross_region row is present AND status is allowed_with_caveat.

    Args:
        rows: Loaded tranche-2 rows.

    Returns:
        True iff CROSS_REGION_FAMILY_ID is present in the tranche AND that
        row's status equals CROSS_REGION_EXPECTED_STATUS.
    """
    for r in rows:
        if r.feature_family_id == CROSS_REGION_FAMILY_ID:
            return r.status == CROSS_REGION_EXPECTED_STATUS
    return False


def _check_in_game_history_aggregate_columns(
    designed_in_game_historical_columns: tuple[str, ...],
) -> tuple[str, ...]:
    """Return designed IN_GAME_HISTORICAL columns NOT in the retained scope.

    The retained scope per CROSS-02-00 §5.4 Concern 8 / T15 record is
    ``IN_GAME_HISTORICAL_AGGREGATED_COLUMNS``: APM, SQ, supplyCappedPercent,
    header_elapsedGameLoops. The validator returns the set difference.

    If CROSS-02-00 §5.4 is amended, update ``IN_GAME_HISTORICAL_AGGREGATED_COLUMNS``
    constant in lockstep before regenerating the scaffold.

    Args:
        designed_in_game_historical_columns: Notebook-declared columns the
            scaffold plans to aggregate over PRIOR matches for the
            ``in_game_history_aggregate`` family.

    Returns:
        Tuple of out-of-scope column names (sorted for determinism).
    """
    allowed = set(IN_GAME_HISTORICAL_AGGREGATED_COLUMNS)
    designed = set(designed_in_game_historical_columns)
    return tuple(sorted(designed - allowed))


def _check_cold_start_gates(
    rows: list[HistoryEnrichedPreGameTrancheRow],
) -> tuple[tuple[str, str], ...]:
    """Return (family_id, cold_start_handling) pairs outside the allowed set.

    Args:
        rows: Loaded tranche-2 rows.

    Returns:
        Tuple of (family_id, cold_start_handling) pairs whose handling is
        NOT in ALLOWED_HISTORY_COLD_START_GATES.
    """
    return tuple(
        (r.feature_family_id, r.cold_start_handling)
        for r in rows
        if r.cold_start_handling not in ALLOWED_HISTORY_COLD_START_GATES
    )


def _check_status_admissibility(
    rows: list[HistoryEnrichedPreGameTrancheRow],
) -> tuple[tuple[str, str], ...]:
    """Return (family_id, status) pairs whose status is not in the allowed set.

    Args:
        rows: Loaded tranche-2 rows.

    Returns:
        Tuple of (family_id, status) pairs whose status is NOT in
        ALLOWED_HISTORY_STATUSES.
    """
    return tuple(
        (r.feature_family_id, r.status)
        for r in rows
        if r.status not in ALLOWED_HISTORY_STATUSES
    )


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def validate_history_enriched_pre_game_materialization(
    registry_csv_path: Path | str,
    designed_column_names: tuple[str, ...],
    designed_in_game_historical_columns: tuple[str, ...],
) -> HistoryEnrichedScaffoldValidationResult:
    """Validate the scaffold design contract for the 6 tranche-2 history families.

    Loads the closed 02_01_01 registry CSV, runs every ``_check_*`` helper,
    and returns a frozen result dataclass. Does NOT materialize any feature
    value, does NOT write any file, and sets ``materialized_output_paths``
    always to ``()``.

    ``designed_column_names`` is the notebook-supplied PLANNED focal_*/opponent_*
    column-name tuple used for POST_GAME token-absence checks only.
    ``designed_in_game_historical_columns`` is the notebook-supplied list of
    IN_GAME_HISTORICAL columns that the scaffold plans to aggregate over PRIOR
    matches for the ``in_game_history_aggregate`` family (CROSS-02-00 §5.4).
    Neither parameter is read from a feature table — keeping the validator
    pure and the notebook artifact-free.

    Args:
        registry_csv_path: Path to 02_01_01_feature_family_registry.csv.
        designed_column_names: Planned column-name tuple for the tranche.
        designed_in_game_historical_columns: Planned IN_GAME_HISTORICAL
            columns to aggregate (must be subset of the §5.4 retained set).

    Returns:
        HistoryEnrichedScaffoldValidationResult with all check outputs
        populated. ``passed`` is True iff ``halting_falsifier is None``.
    """
    path = Path(registry_csv_path)
    rows = load_history_enriched_pre_game_tranche_rows(path)
    full_registry = _load_full_registry(path)

    tranche_ids, missing_families, extra_history = _check_tranche_membership(
        rows, full_registry
    )
    tranche_count = len(rows)
    pre_game_aliases, in_game_aliases, blocked_aliases = _check_aliasing_in_tranche(
        full_registry
    )
    wrong_ps = _check_prediction_setting(rows)
    wrong_anchor = _check_temporal_anchor(rows)
    cutoff_violations = _check_cutoff_rule_is_strict(rows)
    tracker_hits = _check_no_tracker_source(rows)
    asym_hits = _check_symmetry(rows)
    post_game_hits = _check_no_post_game_tokens(rows, designed_column_names)
    cross_region_ok = _check_cross_region_caveat(rows)
    in_game_hist_out = _check_in_game_history_aggregate_columns(
        designed_in_game_historical_columns
    )
    cold_start_violations = _check_cold_start_gates(rows)
    status_violations = _check_status_admissibility(rows)

    # Determine first halting falsifier in priority order. Structural
    # membership errors win over per-row content errors.
    halting_falsifier: str | None = None
    if missing_families:
        halting_falsifier = "missing_families_in_tranche"
    elif extra_history:
        halting_falsifier = "extra_history_in_tranche"
    elif pre_game_aliases:
        halting_falsifier = "pre_game_in_history_tranche"
    elif in_game_aliases:
        halting_falsifier = "in_game_in_history_tranche"
    elif blocked_aliases:
        halting_falsifier = "blocked_in_history_tranche"
    elif tranche_count != EXPECTED_TRANCHE2_COUNT:
        halting_falsifier = "tranche_count_mismatch"
    elif wrong_ps:
        halting_falsifier = "wrong_prediction_setting"
    elif wrong_anchor:
        halting_falsifier = "wrong_temporal_anchor"
    elif cutoff_violations:
        halting_falsifier = "cutoff_not_strict"
    elif tracker_hits:
        halting_falsifier = "tracker_source_in_history"
    elif asym_hits:
        halting_falsifier = "asymmetric_construction"
    elif post_game_hits:
        halting_falsifier = "post_game_token"
    elif not cross_region_ok:
        halting_falsifier = "cross_region_caveat_missing"
    elif in_game_hist_out:
        halting_falsifier = "in_game_historical_column_out_of_scope"
    elif cold_start_violations:
        halting_falsifier = "cold_start_gate_invalid"
    elif status_violations:
        halting_falsifier = "status_not_admissible"

    passed = halting_falsifier is None

    LOGGER.debug(
        "validate_history_enriched_pre_game_materialization: passed=%s "
        "tranche_count=%d halting_falsifier=%s",
        passed,
        tranche_count,
        halting_falsifier,
    )

    return HistoryEnrichedScaffoldValidationResult(
        passed=passed,
        tranche_family_ids=tranche_ids,
        tranche_count=tranche_count,
        missing_families_in_tranche=missing_families,
        extra_history_in_tranche=extra_history,
        pre_game_aliases_in_tranche=pre_game_aliases,
        in_game_aliases_in_tranche=in_game_aliases,
        blocked_aliases_in_tranche=blocked_aliases,
        wrong_prediction_setting_rows=wrong_ps,
        wrong_temporal_anchor_rows=wrong_anchor,
        cutoff_violations=cutoff_violations,
        tracker_source_in_history=tracker_hits,
        asymmetric_construction=asym_hits,
        post_game_token_hits=post_game_hits,
        cross_region_caveat_ok=cross_region_ok,
        in_game_historical_out_of_scope=in_game_hist_out,
        cold_start_gate_violations=cold_start_violations,
        status_violations=status_violations,
        materialized_output_paths=(),
        halting_falsifier=halting_falsifier,
    )
