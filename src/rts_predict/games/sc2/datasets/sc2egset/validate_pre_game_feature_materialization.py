"""Validation module for SC2EGSet Step 02_01_02 pre-game tranche scaffold (scaffold-only).

This module validates the DESIGN CONTRACT for the 5 tranche-1 pre_game feature
families against the closed 02_01_01 registry CSV. It does NOT materialize
any feature value, does NOT run projection SQL against feature data, and does
NOT write any artifact. ``materialized_output_paths`` is always ``()``.

Binding sources:
    - Closed 02_01_01 registry CSV (authoritative catalog for tranche-1 scope).
    - CROSS-02-01-v1.0.1 §2.2 (POST-GAME token absence).
    - CROSS-02-02-v1.0.1 §6.1 line 228 (is_mmr_missing flag framing).
    - Invariant I3 (no tracker in pre_game tranche).
    - Invariant I5 (symmetric focal/opponent construction).
    - Invariant I7 (no magic numbers — module-level UPPER_SNAKE constants).

Falsifiers implemented (a fired falsifier sets halting_falsifier and passed=False):
    missing_families_in_tranche: one or more expected TRANCHE1_PRE_GAME_FAMILY_IDS
        absent from the registry.
    tranche_count_mismatch: loaded tranche row count != EXPECTED_TRANCHE1_COUNT
        (e.g. duplicate rows).
    extra_in_tranche: extra pre_game families in tranche beyond TRANCHE1_PRE_GAME_FAMILY_IDS.
    is_mmr_missing_not_flag: is_mmr_missing family absent or framed as skill scalar.
    tracker_in_pre_game: a tranche-1 family has a tracker source (Invariant I3).
    history_in_tranche: a history_enriched_pre_game family in tranche 1.
    in_game_in_tranche: an in_game_snapshot family in tranche 1.
    asymmetric: a tranche-1 family has per_player_construction != "symmetric".
    post_game_token: a POST_GAME token in a designed column name or source field.
    unexpected_source_table: a tranche-1 source table not in ALLOWED_PRE_GAME_SOURCE_TABLES.
    forbidden_skill_column: a designed column name is a forbidden skill scalar.
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

TRANCHE1_PRE_GAME_FAMILY_IDS: frozenset[str] = frozenset(
    {
        "sc2egset.pre_game.focal_race_with_opponent_race_pair",
        "sc2egset.pre_game.map_type_encoded",
        "sc2egset.pre_game.patch_version_encoded",
        "sc2egset.pre_game.matchup_encoded",
        "sc2egset.pre_game.is_mmr_missing_flag",
    }
)
EXPECTED_TRANCHE1_COUNT: int = 5
PRE_GAME_PREDICTION_SETTING: str = "pre_game"
SNAPSHOT_CUTOFF_RULE: str = "snapshot_at_match_start"
NO_LEAKAGE_MODE: str = "none"
PRE_GAME_COLD_START_GATE: str = "G-CS-1"
EXPECTED_PER_PLAYER_CONSTRUCTION: str = "symmetric"

# Source tables AUTHORITATIVE per the CLOSED 02_01_01 registry CSV.
ALLOWED_PRE_GAME_SOURCE_TABLES: frozenset[str] = frozenset(
    {
        "replay_players_raw",  # race-pair, matchup, mmr-missing
        "matches_flat",  # map_type, patch_version
    }
)

# is_mmr_missing is a MISSINGNESS/PROVENANCE flag, NOT a skill feature.
# (CROSS-02-02 §6.1 line 228: "Use the missingness flag, not the MMR scalar").
IS_MMR_MISSING_FAMILY_ID: str = "sc2egset.pre_game.is_mmr_missing_flag"

# Matching rule (see _is_forbidden_skill_column): a candidate name is lowercased
# and split on "_" into its underscore-delimited token set; it is ALLOWED if it
# is in APPROVED_MMR_MISSINGNESS_TOKENS, otherwise it is REJECTED iff any
# FORBIDDEN_SKILL_TOKENS member equals one of its tokens (boundary-aware token
# equality — NEVER substring containment, so "mu"/"sigma" reject only as
# standalone tokens, never inside words like "cumulative"/"summary").
APPROVED_MMR_MISSINGNESS_TOKENS: frozenset[str] = frozenset(
    {
        "is_mmr_missing",
        "is_mmr_missing_flag",
        "focal_is_mmr_missing",
        "opponent_is_mmr_missing",
    }
)
FORBIDDEN_SKILL_TOKENS: frozenset[str] = frozenset(
    {
        "mmr",
        "rating",
        "elo",
        "glicko",
        "skill",
        "mu",
        "sigma",
    }
)

TRUE_REGISTRY_CSV_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_01_feature_family_registry.csv"
)
STALE_REGISTRY_FILENAME_FRAGMENT: str = (
    "02_01_01_feature_family_registry_sc2egset.csv"
)
TRACKER_SOURCE_PREFIX: str = "tracker_events_raw"
HISTORY_PREDICTION_SETTING: str = "history_enriched_pre_game"
IN_GAME_PREDICTION_SETTING: str = "in_game_snapshot"
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
class PreGameTrancheRow:
    """Frozen view of a single tranche-1 registry row.

    Attributes:
        feature_family_id: The row's feature_family_id.
        prediction_setting: Must equal PRE_GAME_PREDICTION_SETTING.
        source_table_or_event_family: Must be in ALLOWED_PRE_GAME_SOURCE_TABLES.
        allowed_cutoff_rule: Must equal SNAPSHOT_CUTOFF_RULE.
        candidate_leakage_modes: Must equal NO_LEAKAGE_MODE.
        cold_start_handling: Must equal PRE_GAME_COLD_START_GATE.
        per_player_construction: Must equal EXPECTED_PER_PLAYER_CONSTRUCTION.
        status: Must equal "allowed".
    """

    feature_family_id: str
    prediction_setting: str
    source_table_or_event_family: str
    allowed_cutoff_rule: str
    candidate_leakage_modes: str
    cold_start_handling: str
    per_player_construction: str
    status: str


@dataclass(frozen=True)
class PreGameScaffoldValidationResult:
    """Aggregate result of the pre-game tranche scaffold validation.

    Attributes:
        passed: True iff no halting falsifier fired.
        tranche_family_ids: Tuple of family_ids loaded from the tranche.
        tranche_count: Count of tranche-1 rows loaded.
        missing_families_in_tranche: Expected tranche-1 family_ids that are
            absent from the loaded tranche (set difference
            ``TRANCHE1_PRE_GAME_FAMILY_IDS - set(tranche_family_ids)``).
            Sorted for determinism.
        extra_families_in_tranche: pre_game family_ids in registry but not in
            TRANCHE1_PRE_GAME_FAMILY_IDS.
        is_mmr_missing_classified_as_flag: True iff the is_mmr_missing family
            is present, framed as missingness/provenance, and no forbidden
            skill-scalar column name appears for it.
        tracker_in_pre_game: Tranche family_ids whose source starts with
            TRACKER_SOURCE_PREFIX.
        history_families_in_tranche: history_enriched_pre_game family_ids
            found among the tranche-1 family IDs in the full registry.
        in_game_families_in_tranche: in_game_snapshot family_ids found among
            the tranche-1 family IDs in the full registry.
        asymmetric_construction: Tranche family_ids with
            per_player_construction != "symmetric".
        post_game_token_hits: (family_id, token) pairs where a POST_GAME token
            appears as a boundary-aware token of a designed name, or as a
            substring of a registry source field for any tranche row.
        unexpected_source_tables: Tranche family_ids whose source table is not
            in ALLOWED_PRE_GAME_SOURCE_TABLES.
        materialized_output_paths: ALWAYS () — scaffold persists nothing.
        halting_falsifier: Label of the first falsifier that fired, or None.
    """

    passed: bool
    tranche_family_ids: tuple[str, ...]
    tranche_count: int
    missing_families_in_tranche: tuple[str, ...]
    extra_families_in_tranche: tuple[str, ...]
    is_mmr_missing_classified_as_flag: bool
    tracker_in_pre_game: tuple[str, ...]
    history_families_in_tranche: tuple[str, ...]
    in_game_families_in_tranche: tuple[str, ...]
    asymmetric_construction: tuple[str, ...]
    post_game_token_hits: tuple[tuple[str, str], ...]
    unexpected_source_tables: tuple[str, ...]
    materialized_output_paths: tuple[str, ...] = field(default_factory=tuple)
    halting_falsifier: str | None = None


# ---------------------------------------------------------------------------
# Public loader
# ---------------------------------------------------------------------------


def load_pre_game_tranche_rows(
    registry_csv_path: Path | str,
) -> list[PreGameTrancheRow]:
    """Load only the 5 tranche-1 pre_game rows from the registry CSV.

    Args:
        registry_csv_path: Path to 02_01_01_feature_family_registry.csv.

    Returns:
        List of PreGameTrancheRow, one per tranche-1 family.

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
        raise FileNotFoundError(
            f"Registry CSV not found at {path}"
        )
    rows: list[PreGameTrancheRow] = []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            fid = row.get("feature_family_id", "")
            if fid in TRANCHE1_PRE_GAME_FAMILY_IDS:
                rows.append(
                    PreGameTrancheRow(
                        feature_family_id=fid,
                        prediction_setting=row.get("prediction_setting", ""),
                        source_table_or_event_family=row.get(
                            "source_table_or_event_family", ""
                        ),
                        allowed_cutoff_rule=row.get("allowed_cutoff_rule", ""),
                        candidate_leakage_modes=row.get(
                            "candidate_leakage_modes", ""
                        ),
                        cold_start_handling=row.get("cold_start_handling", ""),
                        per_player_construction=row.get(
                            "per_player_construction", ""
                        ),
                        status=row.get("status", ""),
                    )
                )
    LOGGER.debug(
        "load_pre_game_tranche_rows: loaded %d tranche-1 rows from %s",
        len(rows),
        path,
    )
    return rows


def _load_full_registry(
    registry_csv_path: Path,
) -> list[dict[str, str]]:
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


def _is_forbidden_skill_column(name: str) -> bool:
    """Return True iff name is a forbidden skill/rating/MMR-scalar column.

    Allowlist-first, boundary-aware token-equality check.

    Algorithm:
        1. Lowercase the name.
        2. If lowercased name is in APPROVED_MMR_MISSINGNESS_TOKENS -> False
           (approved missingness flag; allowed even though it contains "mmr").
        3. Split on "_" into underscore-delimited tokens.
        4. Return True iff any FORBIDDEN_SKILL_TOKENS member EQUALS one of
           those tokens (token equality, NEVER substring containment).

    Allows: focal_is_mmr_missing, opponent_is_mmr_missing, is_mmr_missing,
        is_mmr_missing_flag, cumulative, summary, skillset_id, elong.
    Rejects: mmr, focal_mmr, opponent_mmr, mmr_value, rating, elo, glicko,
        skill, mu, sigma.

    Args:
        name: A candidate column name string.

    Returns:
        True if the column is a forbidden skill scalar; False if allowed.
    """
    lowered = name.lower()
    if lowered in APPROVED_MMR_MISSINGNESS_TOKENS:
        return False
    tokens = set(lowered.split("_"))
    return bool(tokens & FORBIDDEN_SKILL_TOKENS)


def _check_tranche_membership(
    rows: list[PreGameTrancheRow],
    full_registry: list[dict[str, str]],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Check that the tranche contains exactly TRANCHE1_PRE_GAME_FAMILY_IDS.

    Args:
        rows: Loaded tranche-1 rows.
        full_registry: All rows from the registry CSV.

    Returns:
        (tranche_family_ids, missing_families_in_tranche, extra_pre_game_beyond_tranche)
        where missing_families_in_tranche is the set difference
        TRANCHE1_PRE_GAME_FAMILY_IDS - set(loaded ids), sorted for determinism,
        and extra_pre_game_beyond_tranche contains pre_game family_ids in the
        full registry that are NOT in TRANCHE1_PRE_GAME_FAMILY_IDS, sorted for
        determinism.
    """
    tranche_ids = tuple(r.feature_family_id for r in rows)
    missing: tuple[str, ...] = tuple(
        sorted(TRANCHE1_PRE_GAME_FAMILY_IDS - set(tranche_ids))
    )
    extra: list[str] = []
    for row in full_registry:
        fid = row.get("feature_family_id", "")
        ps = row.get("prediction_setting", "")
        if ps == PRE_GAME_PREDICTION_SETTING and fid not in TRANCHE1_PRE_GAME_FAMILY_IDS:
            extra.append(fid)
    return tranche_ids, missing, tuple(sorted(extra))


def _check_is_mmr_missing_is_flag_not_skill(
    rows: list[PreGameTrancheRow],
    designed_column_names: tuple[str, ...],
) -> bool:
    """Verify is_mmr_missing family is framed as missingness/provenance, not skill.

    Checks ALL of:
        (1) IS_MMR_MISSING_FAMILY_ID is present in the loaded rows.
        (2) Every designed flag column in APPROVED_MMR_MISSINGNESS_TOKENS that
            appears in designed_column_names satisfies
            _is_forbidden_skill_column(...) is False.
        (3) No designed column for any tranche-1 family is a forbidden
            skill scalar (_is_forbidden_skill_column True).
        (4) Provenance framing: the is_mmr_missing row has family_id ending
            in "is_mmr_missing_flag", prediction_setting=pre_game,
            candidate_leakage_modes=none.

    Args:
        rows: Loaded tranche-1 rows.
        designed_column_names: Planned focal/opponent column-name tuple.

    Returns:
        True iff all four checks pass.
    """
    fids = {r.feature_family_id for r in rows}
    if IS_MMR_MISSING_FAMILY_ID not in fids:
        return False

    # Check (2): approved flag names must pass the allowlist check
    for col in designed_column_names:
        lowered = col.lower()
        if lowered in APPROVED_MMR_MISSINGNESS_TOKENS:
            if _is_forbidden_skill_column(col):
                return False

    # Check (3): no designed column may be a forbidden skill scalar
    for col in designed_column_names:
        if _is_forbidden_skill_column(col):
            return False

    # Check (4): provenance framing on the registry row
    for row in rows:
        if row.feature_family_id == IS_MMR_MISSING_FAMILY_ID:
            if not row.feature_family_id.endswith("is_mmr_missing_flag"):
                return False
            if row.prediction_setting != PRE_GAME_PREDICTION_SETTING:
                return False
            if row.candidate_leakage_modes != NO_LEAKAGE_MODE:
                return False

    return True


def _check_no_tracker_in_pre_game(
    rows: list[PreGameTrancheRow],
) -> tuple[str, ...]:
    """Return tranche family_ids whose source starts with TRACKER_SOURCE_PREFIX.

    Args:
        rows: Loaded tranche-1 rows.

    Returns:
        Tuple of family_ids with a tracker source (should be empty for pre_game).
    """
    return tuple(
        r.feature_family_id
        for r in rows
        if r.source_table_or_event_family.startswith(TRACKER_SOURCE_PREFIX)
    )


def _check_no_deferred_settings_in_tranche(
    full_registry: list[dict[str, str]],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Check no history or in_game family_id aliases a tranche-1 family_id.

    For tranche-1 scope: checks that no row in the full registry carries a
    tranche-1 family_id with a history_enriched_pre_game or in_game_snapshot
    prediction_setting.

    Args:
        full_registry: All rows from the registry CSV.

    Returns:
        (history_ids_in_tranche, in_game_ids_in_tranche) — both should be ().
    """
    history_hits: list[str] = []
    in_game_hits: list[str] = []
    for row in full_registry:
        fid = row.get("feature_family_id", "")
        ps = row.get("prediction_setting", "")
        if fid in TRANCHE1_PRE_GAME_FAMILY_IDS:
            if ps == HISTORY_PREDICTION_SETTING:
                history_hits.append(fid)
            elif ps == IN_GAME_PREDICTION_SETTING:
                in_game_hits.append(fid)
    return tuple(history_hits), tuple(in_game_hits)


def _check_symmetry(
    rows: list[PreGameTrancheRow],
) -> tuple[str, ...]:
    """Return tranche family_ids with per_player_construction != "symmetric".

    Args:
        rows: Loaded tranche-1 rows.

    Returns:
        Tuple of family_ids with asymmetric construction (Invariant I5 violation).
    """
    return tuple(
        r.feature_family_id
        for r in rows
        if r.per_player_construction != EXPECTED_PER_PLAYER_CONSTRUCTION
    )


def _check_no_post_game_tokens(
    rows: list[PreGameTrancheRow],
    designed_column_names: tuple[str, ...],
) -> tuple[tuple[str, str], ...]:
    """Return (family_id, token) pairs where a POST_GAME token is detected.

    Detection applies boundary-aware token equality on designed column names
    and substring check on registry source fields.

    Args:
        rows: Loaded tranche-1 rows.
        designed_column_names: Planned column-name tuple.

    Returns:
        Tuple of (family_id, token) pairs — should be empty for a clean scaffold.
    """
    hits: list[tuple[str, str]] = []

    # Check designed column names with boundary-aware token equality
    for col in designed_column_names:
        col_tokens = set(col.lower().split("_"))
        for token in POST_GAME_TOKENS:
            if token in col_tokens:
                # Use a sentinel family_id for designed-name hits
                hits.append(("designed_columns", token))
                break

    # Check registry source fields with substring containment (registry-controlled)
    for row in rows:
        src = row.source_table_or_event_family.lower()
        for token in POST_GAME_TOKENS:
            if token in src:
                hits.append((row.feature_family_id, token))

    return tuple(hits)


def _check_source_tables(
    rows: list[PreGameTrancheRow],
) -> tuple[str, ...]:
    """Return tranche family_ids whose source table is not in ALLOWED_PRE_GAME_SOURCE_TABLES.

    Args:
        rows: Loaded tranche-1 rows.

    Returns:
        Tuple of family_ids with an unexpected source table.
    """
    return tuple(
        r.feature_family_id
        for r in rows
        if r.source_table_or_event_family not in ALLOWED_PRE_GAME_SOURCE_TABLES
    )


def _check_forbidden_skill_columns(
    designed_column_names: tuple[str, ...],
    rows: list[PreGameTrancheRow],
) -> tuple[str, ...]:
    """Return designed column names that are forbidden skill scalars.

    Applies _is_forbidden_skill_column to ALL designed column names (not
    only the MMR family ones). This implements the F-mmr-scalar falsifier.

    Args:
        designed_column_names: Planned column-name tuple.
        rows: Loaded tranche-1 rows (unused directly; kept for API symmetry).

    Returns:
        Tuple of forbidden column names found.
    """
    return tuple(
        col for col in designed_column_names if _is_forbidden_skill_column(col)
    )


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def validate_pre_game_feature_materialization(
    registry_csv_path: Path | str,
    designed_column_names: tuple[str, ...],
) -> PreGameScaffoldValidationResult:
    """Validate the scaffold design contract for the 5 tranche-1 pre_game families.

    Loads the closed 02_01_01 registry CSV, runs every ``_check_*`` helper,
    and returns a frozen result dataclass. Does NOT materialize any feature
    value, does NOT write any file, and sets ``materialized_output_paths``
    always to ``()``.

    ``designed_column_names`` is the notebook-supplied PLANNED focal_*/opponent_*
    column-name tuple used for POST_GAME token-absence and skill-scalar checks
    only. It is never read from a feature table — keeping the validator pure
    and the notebook artifact-free.

    Args:
        registry_csv_path: Path to 02_01_01_feature_family_registry.csv.
        designed_column_names: Planned column-name tuple for the tranche.

    Returns:
        PreGameScaffoldValidationResult with all check outputs populated.
        ``passed`` is True iff ``halting_falsifier is None``.
    """
    path = Path(registry_csv_path)
    rows = load_pre_game_tranche_rows(path)
    full_registry = _load_full_registry(path)

    tranche_ids, missing_families, extra_families = _check_tranche_membership(
        rows, full_registry
    )
    tranche_count = len(rows)
    is_flag = _check_is_mmr_missing_is_flag_not_skill(rows, designed_column_names)
    tracker_hits = _check_no_tracker_in_pre_game(rows)
    history_hits, in_game_hits = _check_no_deferred_settings_in_tranche(full_registry)
    asym_hits = _check_symmetry(rows)
    post_game_hits = _check_no_post_game_tokens(rows, designed_column_names)
    unexpected_src = _check_source_tables(rows)
    forbidden_cols = _check_forbidden_skill_columns(designed_column_names, rows)

    # Determine first halting falsifier in priority order.
    # missing_families_in_tranche is highest priority — an incomplete tranche
    # must be caught before any per-row checks are meaningful.
    # extra_in_tranche, history_in_tranche, and in_game_in_tranche fire before
    # tranche_count_mismatch so that the most descriptive structural falsifier
    # always wins.  tranche_count_mismatch is the defensive catch for pure
    # duplicate rows (missing, extra, history, and in_game all empty but
    # count != EXPECTED_TRANCHE1_COUNT).
    halting_falsifier: str | None = None
    if missing_families:
        halting_falsifier = "missing_families_in_tranche"
    elif extra_families:
        halting_falsifier = "extra_in_tranche"
    elif history_hits:
        halting_falsifier = "history_in_tranche"
    elif in_game_hits:
        halting_falsifier = "in_game_in_tranche"
    elif tranche_count != EXPECTED_TRANCHE1_COUNT:
        halting_falsifier = "tranche_count_mismatch"
    elif not is_flag:
        halting_falsifier = "is_mmr_missing_not_flag"
    elif tracker_hits:
        halting_falsifier = "tracker_in_pre_game"
    elif asym_hits:
        halting_falsifier = "asymmetric"
    elif post_game_hits:
        halting_falsifier = "post_game_token"
    elif unexpected_src:
        halting_falsifier = "unexpected_source_table"
    elif forbidden_cols:
        halting_falsifier = "forbidden_skill_column"

    passed = halting_falsifier is None

    LOGGER.debug(
        "validate_pre_game_feature_materialization: passed=%s tranche_count=%d "
        "halting_falsifier=%s",
        passed,
        tranche_count,
        halting_falsifier,
    )

    return PreGameScaffoldValidationResult(
        passed=passed,
        tranche_family_ids=tranche_ids,
        tranche_count=tranche_count,
        missing_families_in_tranche=missing_families,
        extra_families_in_tranche=extra_families,
        is_mmr_missing_classified_as_flag=is_flag,
        tracker_in_pre_game=tracker_hits,
        history_families_in_tranche=history_hits,
        in_game_families_in_tranche=in_game_hits,
        asymmetric_construction=asym_hits,
        post_game_token_hits=post_game_hits,
        unexpected_source_tables=unexpected_src,
        materialized_output_paths=(),
        halting_falsifier=halting_falsifier,
    )
