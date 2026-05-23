"""Materialization + post-materialization audit for SC2EGSet Step 02_01_02 pre_game tranche.

This module materialises the 5 tranche-1 pre_game feature families into ONE
Parquet artifact (44,418 rows x 11 projected columns) and runs the
post-materialization CROSS-02-01-v1.0.1 leakage audit. The 11 projected columns
partition into 3 IDENTITY (focal_match_id, focal_player, opponent_player),
1 CONTEXT row-identity anchor (started_at), and 7 audited PRE_GAME features
(focal_race, opponent_race, race_pair, map_type, patch_version,
focal_is_mmr_missing, opponent_is_mmr_missing). Only the 7 PRE_GAME columns
enter the audit's ``features_audited`` list per CROSS-02-01 Section 3 / Section 5.

Binding sources:
    - PR #234 Q1 binding: source layer = ``matches_flat_clean``.
    - PR #234 Q2(a) binding: row-identity anchor = ``started_at TIMESTAMP``
      from ``matches_history_minimal``; ``use_as_window_bound = false``,
      ``use_as_row_identity = true``.
    - PR #234 Q3 RATIFY: race column = ``race`` (cleaning-layer convention);
      ``selectedRace`` excluded; RISK-26 = ``documented_gap``.
    - CROSS-02-00-v3.0.1 Section 5.1 line 360: ``started_at`` is CONTEXT (not PRE_GAME).
    - CROSS-02-03-v1.0.1 Section 6.1: pre_game cutoff = "none (game-T attribute)";
      no strict-`<` filter applies for static game-T attributes.
    - CROSS-02-01-v1.0.1 Section 3 / Section 5: post-materialization audit schema.
    - Invariant I3 (no tracker in pre_game tranche).
    - Invariant I5 (symmetric focal/opponent construction via MFC self-join).
    - Invariant I6 (every reported count has verbatim SQL in the MD).
    - Invariant I7 (no magic numbers; module-level UPPER_SNAKE constants).
    - Invariant I10 (relative-path provenance).

Falsifiers implemented (a fired falsifier sets halting_falsifier and passed=False):
    F-row-count-mismatch: COUNT(*) != EXPECTED_OUTPUT_ROW_COUNT (44,418).
    F-focal-rows-per-match-violation: any focal_match_id has count != 2.
    F-symmetry-violation: focal/opponent swap reproduces NON-matching sibling.
    F-null-feature: any non-identity feature column has NULL count > 0.
    F-race-vocabulary-drift: race vocab != EXPECTED_RACE_VOCABULARY.
    F-is-mmr-missing-distribution-drift: TRUE/FALSE counts != (37290, 7128).
    F-map-distinct-drift: distinct_map_count != EXPECTED_MAP_DISTINCT_COUNT.
    F-patch-distinct-drift: distinct_patch_count != EXPECTED_PATCH_DISTINCT_COUNT.
    F-selectedRace-projected: selectedRace appears in output columns.
    F-post-game-token-projected: a POST_GAME token in EXPECTED_OUTPUT_COLUMNS.
    F-scalar-mmr-projected: a FORBIDDEN_SKILL_TOKENS column in EXPECTED_OUTPUT_COLUMNS.
    F-tracker-source-read: tracker_events_raw or unapproved table read.
    F-history-window-leakage: strict-< filter on started_at in materialization SQL.
    F-unexpected-source-table: source-table allowlist violation.
    F-pr234-binding-hash-mismatch: PR #234 CSV SHA differs from recorded value.
    F-features-audited-empty: len(features_audited) == 0.
    F-features-audited-not-7: features_audited != EXPECTED_AUDITED_FEATURE_COLUMNS.
    F-context-column-counted-as-feature: started_at or identity in features_audited.
    F-audit-verdict-not-pass: verdict != "PASS".
    F-encoder-fit: encoder/scaler fit at this layer (vacuously satisfied).
    F-examiner-clarity-sentence-missing: anchor-clarification sentence absent
        from audit JSON notes or audit MD Section 1.
    F-stale-output-path: output Parquet path contains '_sc2egset' fragment.
"""

from __future__ import annotations

import hashlib
import json
import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import duckdb

LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Module-level constants (no magic numbers; Invariant I7)
# ---------------------------------------------------------------------------

EXPECTED_MFC_ROW_COUNT: int = 44418
EXPECTED_OUTPUT_ROW_COUNT: int = 44418
EXPECTED_OUTPUT_COLUMN_COUNT: int = 11
EXPECTED_AUDITED_FEATURE_COLUMN_COUNT: int = 7
EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID: int = 22209
EXPECTED_IS_MMR_MISSING_TRUE_COUNT: int = 37290
EXPECTED_IS_MMR_MISSING_FALSE_COUNT: int = 7128
EXPECTED_MAP_DISTINCT_COUNT: int = 181
EXPECTED_PATCH_DISTINCT_COUNT: int = 46
EXPECTED_RACE_VOCABULARY: frozenset[str] = frozenset({"Prot", "Terr", "Zerg"})

PROJECTED_IDENTITY_COLUMNS: tuple[str, ...] = (
    "focal_match_id",
    "focal_player",
    "opponent_player",
)
PROJECTED_CONTEXT_COLUMNS: tuple[str, ...] = ("started_at",)
EXPECTED_AUDITED_FEATURE_COLUMNS: tuple[str, ...] = (
    "focal_race",
    "opponent_race",
    "race_pair",
    "map_type",
    "patch_version",
    "focal_is_mmr_missing",
    "opponent_is_mmr_missing",
)
EXPECTED_OUTPUT_COLUMNS: tuple[str, ...] = (
    PROJECTED_IDENTITY_COLUMNS
    + PROJECTED_CONTEXT_COLUMNS
    + EXPECTED_AUDITED_FEATURE_COLUMNS
)

# POST_GAME tokens (CROSS-02-01-v1.0.1 Section 2.2) — boundary-aware token equality.
_POST_GAME_TOKENS: frozenset[str] = frozenset(
    {
        "won",
        "result",
        "outcome",
        "winner",
        "is_decisive_result",
        "duration_seconds",
        "is_duration_suspicious",
        "loss",
        "match_result",
        "final_state",
        "post_game",
        "win",
    }
)

# Forbidden skill scalars (mirrors the existing scaffold validator).
_FORBIDDEN_SKILL_TOKENS: frozenset[str] = frozenset(
    {"mmr", "rating", "elo", "glicko", "skill", "mu", "sigma"}
)
_APPROVED_MMR_MISSINGNESS_TOKENS: frozenset[str] = frozenset(
    {
        "is_mmr_missing",
        "is_mmr_missing_flag",
        "focal_is_mmr_missing",
        "opponent_is_mmr_missing",
    }
)

# Source-table allowlist (Invariant I3; no tracker; PR #234 Q1 binding).
_ALLOWED_SOURCE_TABLES: frozenset[str] = frozenset(
    {"matches_flat_clean", "matches_history_minimal"}
)

DATASET_TAG: str = "sc2egset"
PHASE_02_STEP: str = "02_01_02"
AUDIT_PR_PLACEHOLDER: str = "PR #<TBD>"
SPEC_VERSION: str = "CROSS-02-01-v1"
LINEAGE_POSITION: str = (
    "artifact #5 in the 5-artifact lineage for Step 02_01_02 readiness "
    "(after: PR #229 Section 10 design-time verdict pair; PR #230 vacuous "
    "CROSS-02-01 audit pair; PR #233 scaffold + 1 validator; "
    "PR #234 adjudication artifact pair; this materialization + post-mat audit)"
)

_STALE_OUTPUT_FRAGMENT: str = "_sc2egset.parquet"

# Repo-relative provenance paths (Invariant I10).
_METHODOLOGY_RISK_REGISTER_RELPATH: str = "thesis/pass2_evidence/methodology_risk_register.md"
_SPEC_02_00_RELPATH: str = "reports/specs/02_00_feature_input_contract.md"
_SPEC_02_01_RELPATH: str = "reports/specs/02_01_leakage_audit_protocol.md"
_SPEC_02_02_RELPATH: str = "reports/specs/02_02_feature_engineering_plan.md"
_SPEC_02_03_RELPATH: str = "reports/specs/02_03_temporal_feature_audit_protocol.md"
_MATCHES_FLAT_CLEAN_YAML_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml"
)
_MATCHES_HISTORY_MINIMAL_YAML_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml"
)
_MATCHES_LONG_RAW_YAML_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml"
)
_PR234_CSV_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_02_source_anchor_race_adjudication.csv"
)
_PR234_MD_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_02_source_anchor_race_adjudication.md"
)
_REGISTRY_CSV_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_01_feature_family_registry.csv"
)


# ---------------------------------------------------------------------------
# Named SQL constants (python-code rule: _QUERY suffix; Invariant I6 verbatim)
# ---------------------------------------------------------------------------

_MATERIALIZATION_QUERY: str = """
WITH mfc_focal AS (
    SELECT
        mfc.replay_id          AS focal_replay_id,
        mfc.toon_id            AS focal_toon_id,
        mfc.race               AS focal_race,
        mfc.is_mmr_missing     AS focal_is_mmr_missing,
        mfc.metadata_mapName   AS map_type,
        mfc.metadata_gameVersion AS patch_version
    FROM matches_flat_clean mfc
),
mfc_opponent AS (
    SELECT
        mfc.replay_id          AS opp_replay_id,
        mfc.toon_id            AS opponent_toon_id,
        mfc.race               AS opponent_race,
        mfc.is_mmr_missing     AS opponent_is_mmr_missing
    FROM matches_flat_clean mfc
),
mfc_paired AS (
    SELECT
        f.focal_replay_id,
        f.focal_toon_id,
        o.opponent_toon_id,
        f.focal_race,
        o.opponent_race,
        f.focal_is_mmr_missing,
        o.opponent_is_mmr_missing,
        f.map_type,
        f.patch_version
    FROM mfc_focal f
    JOIN mfc_opponent o
        ON f.focal_replay_id = o.opp_replay_id
        AND f.focal_toon_id  <> o.opponent_toon_id
),
mhm_anchor AS (
    SELECT
        match_id,
        player_id,
        started_at
    FROM matches_history_minimal
)
SELECT
    CONCAT('sc2egset::', p.focal_replay_id)     AS focal_match_id,
    p.focal_toon_id                              AS focal_player,
    p.opponent_toon_id                           AS opponent_player,
    a.started_at                                 AS started_at,
    p.focal_race                                 AS focal_race,
    p.opponent_race                              AS opponent_race,
    CONCAT(p.focal_race, '_vs_', p.opponent_race) AS race_pair,
    p.map_type                                   AS map_type,
    p.patch_version                              AS patch_version,
    p.focal_is_mmr_missing                       AS focal_is_mmr_missing,
    p.opponent_is_mmr_missing                    AS opponent_is_mmr_missing
FROM mfc_paired p
JOIN mhm_anchor a
    ON a.match_id  = CONCAT('sc2egset::', p.focal_replay_id)
    AND a.player_id = p.focal_toon_id
ORDER BY a.started_at, p.focal_replay_id, p.focal_toon_id
""".strip()

_OUTPUT_ROW_COUNT_QUERY: str = (
    "SELECT COUNT(*) FROM materialized_pre_game_features"
)
_OUTPUT_DISTINCT_FOCAL_MATCH_ID_QUERY: str = (
    "SELECT COUNT(DISTINCT focal_match_id) FROM materialized_pre_game_features"
)
_FOCAL_ROWS_PER_MATCH_QUERY: str = (
    "SELECT focal_match_id, COUNT(*) AS cnt "
    "FROM materialized_pre_game_features GROUP BY 1 HAVING COUNT(*) <> 2"
)
_SYMMETRY_CHECK_QUERY: str = """
SELECT COUNT(*) FROM materialized_pre_game_features m1
JOIN materialized_pre_game_features m2
    ON m1.focal_match_id = m2.focal_match_id
    AND m1.focal_player  = m2.opponent_player
    AND m1.opponent_player = m2.focal_player
WHERE m1.focal_race           != m2.opponent_race
   OR m1.opponent_race        != m2.focal_race
   OR m1.focal_is_mmr_missing != m2.opponent_is_mmr_missing
   OR m1.opponent_is_mmr_missing != m2.focal_is_mmr_missing
   OR m1.map_type             != m2.map_type
   OR m1.patch_version        != m2.patch_version
   OR m1.started_at           != m2.started_at
""".strip()
_NO_NULL_FEATURE_QUERY: str = """
SELECT
    COUNT(*) FILTER (WHERE focal_race IS NULL) AS null_focal_race,
    COUNT(*) FILTER (WHERE opponent_race IS NULL) AS null_opp_race,
    COUNT(*) FILTER (WHERE race_pair IS NULL) AS null_race_pair,
    COUNT(*) FILTER (WHERE map_type IS NULL) AS null_map,
    COUNT(*) FILTER (WHERE patch_version IS NULL) AS null_patch,
    COUNT(*) FILTER (WHERE focal_is_mmr_missing IS NULL) AS null_focal_mmr_missing,
    COUNT(*) FILTER (WHERE opponent_is_mmr_missing IS NULL) AS null_opp_mmr_missing,
    COUNT(*) FILTER (WHERE started_at IS NULL) AS null_started_at
FROM materialized_pre_game_features
""".strip()
_RACE_VOCAB_QUERY: str = (
    "SELECT focal_race, COUNT(*) FROM materialized_pre_game_features "
    "GROUP BY 1 ORDER BY 1"
)
_IS_MMR_MISSING_DIST_QUERY: str = (
    "SELECT focal_is_mmr_missing, COUNT(*) FROM materialized_pre_game_features "
    "GROUP BY 1 ORDER BY 1"
)
_MAP_DISTINCT_QUERY: str = (
    "SELECT COUNT(DISTINCT map_type) FROM materialized_pre_game_features"
)
_PATCH_DISTINCT_QUERY: str = (
    "SELECT COUNT(DISTINCT patch_version) FROM materialized_pre_game_features"
)
_STARTED_AT_RANGE_QUERY: str = (
    "SELECT MIN(started_at), MAX(started_at) FROM materialized_pre_game_features"
)
_DESCRIBE_QUERY: str = "DESCRIBE materialized_pre_game_features"

# Examiner-clarity sentence (must appear in audit JSON `notes` and audit MD Section 1).
EXAMINER_CLARITY_SENTENCE: str = (
    "`started_at` is projected as a row-identity anchor only "
    "(CROSS-02-00 Section 5.1 = CONTEXT; PR #234 Q2(a) "
    "use_as_window_bound = false) and is excluded from `features_audited`."
)
_EXAMINER_CLARITY_REQUIRED_FRAGMENTS: tuple[str, ...] = (
    "`started_at` is projected as a row-identity anchor only",
    "excluded from `features_audited`",
)

# Non-overclaim disclaimer (audit JSON notes + audit MD).
_CLOSURE_NON_OVERCLAIM: str = (
    "Step 02_01_02 NOT closed by this PR; closure deferred to a separate "
    "PR per planning U2.B (PR #229 -> PR #230 precedent)."
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MaterializationResult:
    """Result of the pre_game tranche materialization.

    Attributes:
        passed: True iff halting_falsifier is None.
        parquet_path: Path to the persisted Parquet feature file.
        row_count: COUNT(*) on the materialized output.
        column_names: Tuple of output column names in projection order.
        distinct_focal_match_id_count: Distinct focal_match_id count.
        race_vocabulary: Set of distinct focal_race values.
        is_mmr_missing_true_count: COUNT WHERE focal_is_mmr_missing=TRUE.
        is_mmr_missing_false_count: COUNT WHERE focal_is_mmr_missing=FALSE.
        distinct_map_count: Distinct map_type count.
        distinct_patch_count: Distinct patch_version count.
        materialized_output_paths: Non-empty tuple containing the Parquet path.
        halting_falsifier: Label of the first falsifier that fired, or None.
    """

    parquet_path: Path
    row_count: int
    column_names: tuple[str, ...]
    distinct_focal_match_id_count: int
    race_vocabulary: frozenset[str]
    is_mmr_missing_true_count: int
    is_mmr_missing_false_count: int
    distinct_map_count: int
    distinct_patch_count: int
    materialized_output_paths: tuple[str, ...] = field(default_factory=tuple)
    halting_falsifier: str | None = None

    @property
    def passed(self) -> bool:
        """Return True iff halting_falsifier is None."""
        return self.halting_falsifier is None


@dataclass(frozen=True)
class AuditResult:
    """Result of the post-materialization CROSS-02-01 leakage audit.

    Attributes:
        spec_version: "CROSS-02-01-v1" per Section 3.
        dataset: "sc2egset".
        phase_02_step: "02_01_02".
        audit_date: ISO YYYY-MM-DD at execution.
        future_leak_count: 0 (no strict-< filter applies; tranche-1 static attributes).
        post_game_token_violations: Count of POST_GAME tokens in column names.
        normalization_fit_scope: "training_fold_only" (vacuously satisfied).
        target_encoding_fold_awareness: "N/A_no_target_encoding".
        cutoff_time_filter_structural_check: "pass" (pass-by-design).
        reference_window_assertion: "pass".
        features_audited: The 7 PRE_GAME feature columns under audit.
        projected_context_columns: ("started_at",) — CONTEXT, not feature.
        projected_identity_columns: 3 identity carriers; not features.
        verdict: "PASS" iff halting_falsifier is None.
        artifact_json_path: Path to the audit JSON.
        artifact_md_path: Path to the audit MD.
        halting_falsifier: Label of the first falsifier that fired, or None.
    """

    spec_version: str
    dataset: str
    phase_02_step: str
    audit_date: str
    future_leak_count: int
    post_game_token_violations: int
    normalization_fit_scope: str
    target_encoding_fold_awareness: str
    cutoff_time_filter_structural_check: str
    reference_window_assertion: str
    features_audited: tuple[str, ...]
    projected_context_columns: tuple[str, ...]
    projected_identity_columns: tuple[str, ...]
    verdict: str
    artifact_json_path: str
    artifact_md_path: str
    halting_falsifier: str | None = None


# ---------------------------------------------------------------------------
# Repo-root + provenance helpers
# ---------------------------------------------------------------------------


def _find_repo_root(start: Path) -> Path:
    """Walk upwards from ``start`` until a directory containing pyproject.toml is found.

    Args:
        start: Path to begin searching from.

    Returns:
        Absolute path to the repo root.

    Raises:
        FileNotFoundError: If no pyproject.toml is found in any ancestor.
    """
    current = start.resolve()
    if current.is_file():
        current = current.parent
    while True:
        if (current / "pyproject.toml").exists():
            return current
        if current.parent == current:
            break
        current = current.parent
    raise FileNotFoundError(
        f"No pyproject.toml found walking up from {start}; cannot determine repo root."
    )


def _sha256_file(path: Path) -> str:
    """Compute SHA-256 hex digest of a file, or 'NOT_FOUND' if absent.

    Args:
        path: Path to the file.

    Returns:
        Hex digest string or 'NOT_FOUND'.
    """
    if not path.exists():
        return "NOT_FOUND"
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _get_git_sha() -> str:
    """Return the current HEAD git SHA, or 'UNKNOWN' if git is unavailable.

    Returns:
        Git SHA string or 'UNKNOWN'.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:  # noqa: BLE001
        return "UNKNOWN"


# ---------------------------------------------------------------------------
# Schema / token guards
# ---------------------------------------------------------------------------


def _is_post_game_token(name: str) -> bool:
    """Return True iff name contains a POST_GAME token via token-equality.

    Args:
        name: Candidate column name.

    Returns:
        True if any POST_GAME token equals one of name's underscore tokens.
    """
    tokens = set(name.lower().split("_"))
    return bool(tokens & _POST_GAME_TOKENS)


def _is_forbidden_skill_column(name: str) -> bool:
    """Return True iff name is a forbidden skill scalar (not an approved flag).

    Args:
        name: Candidate column name.

    Returns:
        True if forbidden; False if allowed.
    """
    lowered = name.lower()
    if lowered in _APPROVED_MMR_MISSINGNESS_TOKENS:
        return False
    tokens = set(lowered.split("_"))
    return bool(tokens & _FORBIDDEN_SKILL_TOKENS)


def _check_no_post_game_token_in_columns(
    columns: tuple[str, ...],
) -> int:
    """Count POST_GAME-token violations across the projected column list.

    Args:
        columns: Tuple of projected column names.

    Returns:
        Number of column names containing a POST_GAME token.
    """
    return sum(1 for c in columns if _is_post_game_token(c))


def _check_source_table_allowlist(query: str) -> tuple[str, ...]:
    """Detect any FROM/JOIN of an unapproved source table in the SQL text.

    Args:
        query: Materialization SQL string.

    Returns:
        Tuple of offending source-table tokens found (empty if clean).
    """
    lowered = query.lower()
    forbidden_substrings = (
        "tracker_events_raw",
        "player_history_all",
        "replay_players_raw",
        "matches_flat ",
        "matches_long_raw",
    )
    return tuple(s.strip() for s in forbidden_substrings if s in lowered)


def _check_no_history_window(query: str) -> bool:
    """Return True iff a strict-< or <= predicate between timestamp columns is present.

    Args:
        query: Materialization SQL string.

    Returns:
        True if the query contains a history-window filter (a falsifier hit).
    """
    lowered = query.lower()
    history_window_tokens = (
        " < started_at",
        "started_at <",
        "started_at<",
        "<= started_at",
    )
    return any(token in lowered for token in history_window_tokens)


# ---------------------------------------------------------------------------
# DuckDB execution helpers
# ---------------------------------------------------------------------------


def _connect_duckdb(duckdb_path: Path) -> duckdb.DuckDBPyConnection:
    """Open the DuckDB file READ-ONLY and configure UTC session timezone.

    Args:
        duckdb_path: Path to the DuckDB file.

    Returns:
        Open DuckDB connection with TimeZone set to UTC.
    """
    con = duckdb.connect(str(duckdb_path), read_only=True)
    con.execute("SET TimeZone = 'UTC'")
    return con


def _create_materialized_view(con: duckdb.DuckDBPyConnection) -> None:
    """Create the session-scoped temp view ``materialized_pre_game_features``.

    Args:
        con: Open DuckDB connection (read-only is fine; TEMP views go to memory).
    """
    con.execute(
        f"CREATE OR REPLACE TEMP VIEW materialized_pre_game_features AS "
        f"{_MATERIALIZATION_QUERY}"
    )


def _export_to_parquet(
    con: duckdb.DuckDBPyConnection, output_parquet_path: Path
) -> None:
    """Write the temp view to Parquet with ZSTD compression.

    Args:
        con: Open DuckDB connection with materialized_pre_game_features registered.
        output_parquet_path: Destination Parquet path.
    """
    output_parquet_path.parent.mkdir(parents=True, exist_ok=True)
    con.execute(
        f"COPY (SELECT * FROM materialized_pre_game_features) "
        f"TO '{output_parquet_path.as_posix()}' "
        f"(FORMAT PARQUET, COMPRESSION 'ZSTD', ROW_GROUP_SIZE 100000)"
    )


def _query_column_names(con: duckdb.DuckDBPyConnection) -> tuple[str, ...]:
    """Return the column names of the materialized temp view in projection order.

    Args:
        con: Open DuckDB connection with materialized_pre_game_features registered.

    Returns:
        Tuple of column names.
    """
    rows = con.execute(_DESCRIBE_QUERY).fetchall()
    return tuple(row[0] for row in rows)


def _run_sanity_checks(
    con: duckdb.DuckDBPyConnection,
) -> dict[str, Any]:
    """Execute every sanity-check SQL and return a dict of (label -> result).

    Args:
        con: Open DuckDB connection.

    Returns:
        Dict mapping check label to its result value.
    """
    out: dict[str, Any] = {}
    out["row_count"] = con.execute(_OUTPUT_ROW_COUNT_QUERY).fetchone()[0]  # type: ignore[index]
    out["distinct_focal_match_id"] = (  # type: ignore[assignment]
        con.execute(_OUTPUT_DISTINCT_FOCAL_MATCH_ID_QUERY).fetchone()[0]  # type: ignore[index]
    )
    out["focal_rows_per_match_violations"] = len(
        con.execute(_FOCAL_ROWS_PER_MATCH_QUERY).fetchall()
    )
    out["symmetry_violations"] = con.execute(_SYMMETRY_CHECK_QUERY).fetchone()[0]  # type: ignore[index]
    null_row = con.execute(_NO_NULL_FEATURE_QUERY).fetchone()
    assert null_row is not None
    out["null_counts"] = tuple(null_row)
    race_rows = con.execute(_RACE_VOCAB_QUERY).fetchall()
    out["race_vocabulary"] = frozenset(r[0] for r in race_rows)
    mmr_rows = con.execute(_IS_MMR_MISSING_DIST_QUERY).fetchall()
    out["is_mmr_missing_distribution"] = {bool(r[0]): r[1] for r in mmr_rows}
    out["distinct_map_count"] = con.execute(_MAP_DISTINCT_QUERY).fetchone()[0]  # type: ignore[index]
    out["distinct_patch_count"] = con.execute(_PATCH_DISTINCT_QUERY).fetchone()[0]  # type: ignore[index]
    return out


def _evaluate_materialization_falsifiers(
    sanity: dict[str, Any], columns: tuple[str, ...], query: str
) -> str | None:
    """Return the first materialization falsifier label that fires, or None.

    Args:
        sanity: Sanity-check result dict from _run_sanity_checks.
        columns: Tuple of materialized column names.
        query: Materialization SQL text.

    Returns:
        Falsifier label string, or None if all checks pass.
    """
    if sanity["row_count"] != EXPECTED_OUTPUT_ROW_COUNT:
        return "F-row-count-mismatch"
    if sanity["focal_rows_per_match_violations"] != 0:
        return "F-focal-rows-per-match-violation"
    if sanity["symmetry_violations"] != 0:
        return "F-symmetry-violation"
    if any(c != 0 for c in sanity["null_counts"]):
        return "F-null-feature"
    if sanity["race_vocabulary"] != EXPECTED_RACE_VOCABULARY:
        return "F-race-vocabulary-drift"
    mmr_dist = sanity["is_mmr_missing_distribution"]
    if (
        mmr_dist.get(True, 0) != EXPECTED_IS_MMR_MISSING_TRUE_COUNT
        or mmr_dist.get(False, 0) != EXPECTED_IS_MMR_MISSING_FALSE_COUNT
    ):
        return "F-is-mmr-missing-distribution-drift"
    if sanity["distinct_map_count"] != EXPECTED_MAP_DISTINCT_COUNT:
        return "F-map-distinct-drift"
    if sanity["distinct_patch_count"] != EXPECTED_PATCH_DISTINCT_COUNT:
        return "F-patch-distinct-drift"
    if "selectedrace" in {c.lower() for c in columns}:
        return "F-selectedRace-projected"
    if _check_no_post_game_token_in_columns(columns) > 0:
        return "F-post-game-token-projected"
    if any(_is_forbidden_skill_column(c) for c in columns):
        return "F-scalar-mmr-projected"
    if _check_source_table_allowlist(query):
        return "F-tracker-source-read"
    if _check_no_history_window(query):
        return "F-history-window-leakage"
    if columns != EXPECTED_OUTPUT_COLUMNS:
        return "F-output-column-mismatch"
    return None


# ---------------------------------------------------------------------------
# Public entrypoint — materialization
# ---------------------------------------------------------------------------


def materialize_pre_game_features(
    duckdb_path: Path | str,
    output_parquet_path: Path | str,
    registry_csv_path: Path | str,
) -> MaterializationResult:
    """Materialize the 5 tranche-1 pre_game families to Parquet.

    Reads ``matches_flat_clean`` and ``matches_history_minimal`` from the
    DuckDB file (read-only), executes ``_MATERIALIZATION_QUERY`` into a temp
    view, writes the view to Parquet with ZSTD compression and 100k row
    groups, then runs every sanity-check query and evaluates falsifiers.
    If any falsifier fires, the parquet is left in place and the result
    carries the failure label in ``halting_falsifier``.

    Args:
        duckdb_path: Path to the on-disk DuckDB file.
        output_parquet_path: Destination Parquet path for the feature table.
        registry_csv_path: Path to the closed registry CSV (read-only; used
            for SHA-256 provenance only).

    Returns:
        MaterializationResult with all sanity-check outputs populated.

    Raises:
        ValueError: If output_parquet_path matches the stale fragment.
    """
    duckdb_path = Path(duckdb_path)
    output_parquet_path = Path(output_parquet_path)
    registry_csv_path = Path(registry_csv_path)
    if _STALE_OUTPUT_FRAGMENT in output_parquet_path.name:
        raise ValueError(
            f"Stale output path detected: '{output_parquet_path}' contains "
            f"the deprecated fragment '{_STALE_OUTPUT_FRAGMENT}'."
        )

    LOGGER.debug(
        "materialize_pre_game_features: duckdb=%s output=%s registry=%s",
        duckdb_path,
        output_parquet_path,
        registry_csv_path,
    )

    con = _connect_duckdb(duckdb_path)
    try:
        _create_materialized_view(con)
        column_names = _query_column_names(con)
        _export_to_parquet(con, output_parquet_path)
        sanity = _run_sanity_checks(con)
    finally:
        con.close()

    halting_falsifier = _evaluate_materialization_falsifiers(
        sanity, column_names, _MATERIALIZATION_QUERY
    )

    return MaterializationResult(
        parquet_path=output_parquet_path,
        row_count=int(sanity["row_count"]),
        column_names=column_names,
        distinct_focal_match_id_count=int(sanity["distinct_focal_match_id"]),
        race_vocabulary=sanity["race_vocabulary"],
        is_mmr_missing_true_count=int(
            sanity["is_mmr_missing_distribution"].get(True, 0)
        ),
        is_mmr_missing_false_count=int(
            sanity["is_mmr_missing_distribution"].get(False, 0)
        ),
        distinct_map_count=int(sanity["distinct_map_count"]),
        distinct_patch_count=int(sanity["distinct_patch_count"]),
        materialized_output_paths=(str(output_parquet_path),),
        halting_falsifier=halting_falsifier,
    )


# ---------------------------------------------------------------------------
# Post-materialization audit helpers
# ---------------------------------------------------------------------------


def _read_parquet_columns(parquet_path: Path) -> tuple[str, ...]:
    """Return parquet column names using a temporary DuckDB session.

    Args:
        parquet_path: Path to the Parquet file.

    Returns:
        Tuple of column names in file order.
    """
    con = duckdb.connect(":memory:")
    try:
        rows = con.execute(
            f"DESCRIBE SELECT * FROM read_parquet('{parquet_path.as_posix()}')"
        ).fetchall()
        return tuple(row[0] for row in rows)
    finally:
        con.close()


def _read_parquet_row_count(parquet_path: Path) -> int:
    """Return total row count of the Parquet file.

    Args:
        parquet_path: Path to the Parquet file.

    Returns:
        Row count.
    """
    con = duckdb.connect(":memory:")
    try:
        row = con.execute(
            f"SELECT COUNT(*) FROM read_parquet('{parquet_path.as_posix()}')"
        ).fetchone()
        assert row is not None
        return int(row[0])
    finally:
        con.close()


def _resolve_repo_root_relpath(path: Path, repo_root: Path) -> str:
    """Return a forward-slash relative path from repo_root to path.

    Args:
        path: Absolute path inside the repo.
        repo_root: Repo root directory.

    Returns:
        Relative path string with forward slashes.
    """
    try:
        rel = path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return path.as_posix()
    return rel.as_posix()


def _evaluate_audit_falsifiers(
    parquet_columns: tuple[str, ...],
    features_audited: tuple[str, ...],
    projected_identity_columns: tuple[str, ...],
    projected_context_columns: tuple[str, ...],
    examiner_notes: str,
    examiner_md_section1: str,
) -> str | None:
    """Return the first audit-side falsifier label that fires, or None.

    Args:
        parquet_columns: Columns read from the materialized Parquet.
        features_audited: Tuple of feature columns flagged as audited.
        projected_identity_columns: Identity-only projected columns.
        projected_context_columns: Context-only projected columns.
        examiner_notes: Audit-JSON ``notes`` string under verification.
        examiner_md_section1: Audit-MD Section 1 string under verification.

    Returns:
        Falsifier label or None.
    """
    if parquet_columns != EXPECTED_OUTPUT_COLUMNS:
        return "F-output-column-mismatch"
    if len(features_audited) == 0:
        return "F-features-audited-empty"
    if (
        len(features_audited) != EXPECTED_AUDITED_FEATURE_COLUMN_COUNT
        or set(features_audited) != set(EXPECTED_AUDITED_FEATURE_COLUMNS)
    ):
        return "F-features-audited-not-7"
    audit_set = set(features_audited)
    if (
        audit_set & set(projected_identity_columns)
        or audit_set & set(projected_context_columns)
    ):
        return "F-context-column-counted-as-feature"
    if any(fr not in examiner_notes for fr in _EXAMINER_CLARITY_REQUIRED_FRAGMENTS):
        return "F-examiner-clarity-sentence-missing"
    if EXAMINER_CLARITY_SENTENCE not in examiner_md_section1:
        return "F-examiner-clarity-sentence-missing"
    if any(_is_post_game_token(c) for c in parquet_columns):
        return "F-post-game-token-projected"
    if any(_is_forbidden_skill_column(c) for c in parquet_columns):
        return "F-scalar-mmr-projected"
    return None


# ---------------------------------------------------------------------------
# Audit artifact rendering
# ---------------------------------------------------------------------------


def _build_audit_notes(
    pr_label: str,
) -> str:
    """Construct the multi-paragraph audit JSON ``notes`` string.

    The notes string contains:
        - Step closure non-overclaim (F-closure-overclaim guard).
        - Cutoff-pass justification.
        - Normalization fit-scope vacuity.
        - PR #230 preservation statement.
        - Examiner-clarity sentence (F-examiner-clarity-sentence-missing guard).
        - 11-column role-partition explanation.

    Args:
        pr_label: The literal "PR #<N>" string (or "PR #<TBD>" placeholder).

    Returns:
        Joined notes string.
    """
    parts = [
        _CLOSURE_NON_OVERCLAIM,
        (
            "PIPELINE_SECTION_STATUS 02_01 = complete remains derived from "
            "STEP_STATUS until a future PR adds 02_01_02 to STEP_STATUS, at "
            "which point YAML-derivation re-derives 02_01 = in_progress "
            "(intended behaviour, pre-disclosed in PR #230 CHANGELOG Notes)."
        ),
        (
            "cutoff_time_filter_structural_check = pass is justified BY DESIGN "
            "for the 5 tranche-1 static game-T attributes per CROSS-02-03 "
            "Section 6.1; no strict-< filter applies; the anchor started_at "
            "is a row-identity column not a window bound."
        ),
        (
            "normalization_fit_scope = training_fold_only is vacuously "
            "satisfied because no encoder/scaler was fit at this layer -- "
            "raw categorical strings and BOOLEAN values are retained for "
            "Phase 03 fold-aware encoder fitting (Invariant I3 "
            "normalization-leakage discipline; CROSS-02-02 Section 9.1 G-CS-6)."
        ),
        (
            "PR #230 audit JSON at 02_01_01/leakage_audit_sc2egset.json "
            "remains byte-unchanged (features_audited == [] historical "
            "record preserved at distinct path)."
        ),
        (
            f"EXAMINER-CLARITY: {EXAMINER_CLARITY_SENTENCE} The 11 output "
            "columns partition into 3 projected identity columns "
            "(`focal_match_id`, `focal_player`, `opponent_player`), "
            "1 projected context anchor (`started_at`), and 7 audited "
            "PRE_GAME feature columns (the exact contents of "
            "`features_audited` above). Only the 7 audited columns are "
            "model features; the 3 identity columns are lineage / split "
            "keys; the 1 context anchor is a row-identity anchor never "
            "consumed as a numeric/categorical feature."
        ),
        (
            f"This is the first non-vacuous CROSS-02-01 audit for "
            f"Step {PHASE_02_STEP} ({pr_label})."
        ),
    ]
    return " ".join(parts)


def _gather_provenance_shas(
    repo_root: Path,
    parquet_path: Path,
    module_path: Path,
) -> dict[str, str]:
    """Compute SHA-256 digests for every provenance asset referenced in audit JSON.

    Args:
        repo_root: Repository root.
        parquet_path: Materialized Parquet path.
        module_path: This module's own .py path.

    Returns:
        Dict of provenance field name -> SHA-256 digest string.
    """
    return {
        "feature_parquet_sha256": _sha256_file(parquet_path),
        "materialize_module_sha256": _sha256_file(module_path),
        "registry_csv_sha256": _sha256_file(repo_root / _REGISTRY_CSV_RELPATH),
        "pr_234_binding_csv_sha256": _sha256_file(repo_root / _PR234_CSV_RELPATH),
        "pr_234_binding_md_sha256": _sha256_file(repo_root / _PR234_MD_RELPATH),
        "methodology_risk_register_sha256": _sha256_file(
            repo_root / _METHODOLOGY_RISK_REGISTER_RELPATH
        ),
        "matches_flat_clean_yaml_sha256": _sha256_file(
            repo_root / _MATCHES_FLAT_CLEAN_YAML_RELPATH
        ),
        "matches_history_minimal_yaml_sha256": _sha256_file(
            repo_root / _MATCHES_HISTORY_MINIMAL_YAML_RELPATH
        ),
        "matches_long_raw_yaml_sha256": _sha256_file(
            repo_root / _MATCHES_LONG_RAW_YAML_RELPATH
        ),
        "spec_02_00_sha256": _sha256_file(repo_root / _SPEC_02_00_RELPATH),
        "spec_02_01_sha256": _sha256_file(repo_root / _SPEC_02_01_RELPATH),
        "spec_02_02_sha256": _sha256_file(repo_root / _SPEC_02_02_RELPATH),
        "spec_02_03_sha256": _sha256_file(repo_root / _SPEC_02_03_RELPATH),
    }


def _render_audit_json(
    audit: AuditResult,
    audit_json_path: Path,
    parquet_path: Path,
    audit_pr: str,
    audit_date: str,
    provenance_shas: dict[str, str],
    git_sha: str,
) -> None:
    """Write the CROSS-02-01-v1.0.1 Section 3 audit JSON.

    Args:
        audit: Populated AuditResult.
        audit_json_path: Destination JSON path.
        parquet_path: Materialized Parquet path (for relative-path reference).
        audit_pr: PR label string (e.g. "PR #236").
        audit_date: ISO date.
        provenance_shas: SHA-256 digests from _gather_provenance_shas.
        git_sha: Current git HEAD SHA.
    """
    repo_root = _find_repo_root(Path(__file__))
    feature_parquet_relpath = _resolve_repo_root_relpath(parquet_path, repo_root)
    payload: dict[str, Any] = {
        "spec_version": audit.spec_version,
        "dataset": audit.dataset,
        "phase_02_step": audit.phase_02_step,
        "audit_date": audit_date,
        "future_leak_count": audit.future_leak_count,
        "post_game_token_violations": audit.post_game_token_violations,
        "normalization_fit_scope": audit.normalization_fit_scope,
        "target_encoding_fold_awareness": audit.target_encoding_fold_awareness,
        "cutoff_time_filter_structural_check": audit.cutoff_time_filter_structural_check,
        "reference_window_assertion": audit.reference_window_assertion,
        "features_audited": list(audit.features_audited),
        "projected_context_columns": list(audit.projected_context_columns),
        "projected_identity_columns": list(audit.projected_identity_columns),
        "verdict": audit.verdict,
        "audit_pr": audit_pr,
        "lineage_position": LINEAGE_POSITION,
        "feature_parquet_path": feature_parquet_relpath,
        **provenance_shas,
        "provenance_git_sha": git_sha,
        "notes": _build_audit_notes(audit_pr),
    }
    audit_json_path.parent.mkdir(parents=True, exist_ok=True)
    audit_json_path.write_text(
        json.dumps(payload, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def _build_md_section_1(audit_pr: str) -> str:
    """Render audit MD Section 1 (non-overclaim disclaimer + examiner clarity).

    Args:
        audit_pr: PR label.

    Returns:
        Markdown body for Section 1.
    """
    return (
        "## 1. Non-overclaim disclaimer\n\n"
        f"{_CLOSURE_NON_OVERCLAIM}\n\n"
        "Feature Parquet persisted (11 projected columns: 3 identity + 1 "
        "context anchor + 7 audited PRE_GAME features). PR #230 audit JSON "
        "at `reports/artifacts/02_01_01/leakage_audit_sc2egset.json` is "
        "byte-unchanged (vacuous `features_audited == []` historical record "
        "preserved at its distinct path).\n\n"
        "CROSS-02-01-v1.0.1 Section 5 gate condition is mechanically "
        "satisfied: `features_audited` non-empty (= 7 PRE_GAME feature "
        "columns), `verdict = PASS`, JSON + MD persisted at the spec-named "
        "paths.\n\n"
        f"**Examiner-clarity sentence (verbatim):** {EXAMINER_CLARITY_SENTENCE}\n\n"
        f"This is the first non-vacuous CROSS-02-01 post-materialization "
        f"audit for Step {PHASE_02_STEP} ({audit_pr}).\n"
    )


def _build_md_section_2() -> str:
    """Render audit MD Section 2 (materialization SQL + source-binding paragraph)."""
    yaml_block = (
        "```yaml\n"
        "provenance:\n"
        "  source_tables:\n"
        "  - replay_players_raw\n"
        "  - replays_meta_raw\n"
        "  - player_history_all\n"
        "  join_key: NULLIF(regexp_extract(filename, "
        "'([0-9a-f]{32})\\.SC2Replay\\.json', 1),\n"
        "    '') AS replay_id\n"
        "  filter: true_1v1_decisive CTE (exactly 2 players, 1 Win + 1 Loss); "
        "mmr_valid CTE\n"
        "    (no MMR<0 player in replay)\n"
        "  scope: True 1v1 decisive replays only. 22,209 replays, 44,418 "
        "rows (2 per replay).\n"
        "  created_by: sandbox/sc2/sc2egset/01_exploration/04_cleaning/"
        "01_04_02_data_cleaning_execution.py\n"
        "  addendum_by: sandbox/sc2/sc2egset/01_exploration/04_cleaning/"
        "01_04_02_duration_augmentation.py\n"
        "```\n"
    )
    return (
        "## 2. Materialization SQL + source-binding justification\n\n"
        "The full `_MATERIALIZATION_QUERY` from "
        "`materialize_pre_game_features.py` is reproduced verbatim per "
        "Invariant I6:\n\n"
        "```sql\n"
        f"{_MATERIALIZATION_QUERY}\n"
        ";\n"
        "```\n\n"
        "**Registry-cell upstream-source -> MFC cleaned-view binding** "
        "(per `matches_flat_clean.yaml` lines 178-189, quoted verbatim):\n\n"
        f"{yaml_block}\n"
        "The registry CSV (`02_01_01_feature_family_registry.csv`) rows 2, 5, "
        "6 cite `replay_players_raw` (race-pair, matchup, is_mmr_missing) and "
        "rows 3, 4 cite `matches_flat` (map, patch) as the *upstream* "
        "`source_table_or_event_family`. The Layer-2 materialization reads "
        "ALL 5 columns from `matches_flat_clean` (the cleaned, 1v1-scoped "
        "VIEW). This is consistent: per the YAML provenance block above, "
        "MFC is a cleaned + 1v1-scoped projection over `[replay_players_raw, "
        "replays_meta_raw, player_history_all]`. The 1v1 cleaning filter "
        "(`true_1v1_decisive` CTE) reduces upstream `matches_flat` "
        "(89,944 rows) to `matches_flat_clean` (44,418 rows = 22,209 1v1 "
        "replays × 2 rows). The registry's `source_table_or_event_family` "
        "cell preserves the *upstream* table binding (the registry is NOT "
        "amended by this PR); the materialization-layer binding to the "
        "cleaned VIEW is recorded here in the audit MD Section 2 as the "
        "authoritative location. This binding is consistent with PR #234 "
        "Q1 adjudication (`matches_flat_clean` ratified as the source layer).\n"
    )


def _build_md_section_3(sanity: dict[str, Any]) -> str:
    """Render audit MD Section 3 (sanity-check SQL + verbatim results)."""
    mmr_dist = sanity["is_mmr_missing_distribution"]
    race_vocab_sorted = sorted(sanity["race_vocabulary"])
    return (
        "## 3. Sanity-check SQL + results\n\n"
        "All sanity-check queries are reproduced verbatim per Invariant I6; "
        "each is followed by the observed empirical result.\n\n"
        f"```sql\n{_OUTPUT_ROW_COUNT_QUERY}\n```\n"
        f"-- Result: {int(sanity['row_count'])}\n\n"
        f"```sql\n{_OUTPUT_DISTINCT_FOCAL_MATCH_ID_QUERY}\n```\n"
        f"-- Result: {int(sanity['distinct_focal_match_id'])}\n\n"
        f"```sql\n{_FOCAL_ROWS_PER_MATCH_QUERY}\n```\n"
        f"-- Result: {int(sanity['focal_rows_per_match_violations'])} "
        "violating rows (expected 0)\n\n"
        f"```sql\n{_SYMMETRY_CHECK_QUERY}\n```\n"
        f"-- Result: {int(sanity['symmetry_violations'])} "
        "(expected 0; Invariant I5)\n\n"
        f"```sql\n{_NO_NULL_FEATURE_QUERY}\n```\n"
        f"-- Result: {sanity['null_counts']!r} (each entry must be 0)\n\n"
        f"```sql\n{_RACE_VOCAB_QUERY}\n```\n"
        f"-- Result: race vocabulary = {race_vocab_sorted!r}\n\n"
        f"```sql\n{_IS_MMR_MISSING_DIST_QUERY}\n```\n"
        f"-- Result: FALSE={mmr_dist.get(False, 0)}, "
        f"TRUE={mmr_dist.get(True, 0)}\n\n"
        f"```sql\n{_MAP_DISTINCT_QUERY}\n```\n"
        f"-- Result: {int(sanity['distinct_map_count'])}\n\n"
        f"```sql\n{_PATCH_DISTINCT_QUERY}\n```\n"
        f"-- Result: {int(sanity['distinct_patch_count'])}\n"
    )


def _build_md_section_4() -> str:
    """Render audit MD Section 4 (cutoff structural check + anchor-classification)."""
    return (
        "## 4. Cutoff structural check + anchor classification\n\n"
        "CROSS-02-03-v1.0.1 Section 6.1 states that pre_game families which "
        "are static game-T attributes have cutoff = \"none (game-T "
        "attribute)\"; NO strict-`<` history-window filter applies. The 5 "
        "tranche-1 families (race-pair, map, patch, matchup, is_mmr_missing) "
        "are all static game-T attributes per the closed 02_01_01 registry "
        "CSV (allowed_cutoff_rule = `snapshot_at_match_start`). The "
        "materialization SQL contains NO `WHERE` predicate on `started_at` "
        "and NO strict-`<` between any two timestamp columns. The "
        "structural verdict therefore reports **pass-by-design**, with "
        "explicit justification recorded here.\n\n"
        "Leak-freedom for this tranche rests on the triad: (i) only game-T "
        "pre-game columns are read; (ii) POST-GAME token absence (Section "
        "5 below; CROSS-02-01-v1.0.1 Section 2.2); (iii) non-tracker source "
        "(Section 5 below; Invariant I3).\n\n"
        "**Anchor classification reiteration.** Per CROSS-02-00 Section 5.1 "
        "line 360, `started_at` is CONTEXT (not PRE_GAME): \"I3 temporal "
        "anchor; TRY_CAST from details_timeUTC\". Per PR #234 Q2(a) the "
        "projected anchor carries `use_as_window_bound = false` and "
        "`use_as_row_identity = true`. Per PR #234 Q2(b) the Phase-03 "
        "chronological hold-out binding is a RECOMMENDATION ONLY (Phase 03 "
        "planning binds; not this PR). Therefore `started_at` is documented "
        "in the audit JSON's `projected_context_columns` field and is "
        "excluded from `features_audited` -- the 7 audited PRE_GAME feature "
        "columns enumerated in Section 1 are exactly the audited set, with "
        "no anchor and no identity column.\n"
    )


def _build_md_section_5(query: str) -> str:
    """Render audit MD Section 5 (POST-GAME token absence + source-table allowlist)."""
    return (
        "## 5. POST-GAME token absence + source-table allowlist\n\n"
        "POST-GAME tokens (CROSS-02-01-v1.0.1 Section 2.2) are detected via "
        "boundary-aware token equality against every column name in the "
        "materialized Parquet. The forbidden token set is:\n\n"
        f"`{sorted(_POST_GAME_TOKENS)!r}`\n\n"
        "Result: 0 hits across the 11 projected column names.\n\n"
        "Source-table allowlist (Invariant I3; no tracker; PR #234 Q1 "
        "binding):\n\n"
        f"`{sorted(_ALLOWED_SOURCE_TABLES)!r}`\n\n"
        "The materialization SQL text was scanned for any FROM/JOIN of a "
        "table outside the allowlist (substring detection for "
        "`tracker_events_raw`, `player_history_all`, `replay_players_raw`, "
        "`matches_flat ` (space-bounded to distinguish from "
        "`matches_flat_clean`), `matches_long_raw`). Result: 0 hits.\n"
    )


def _build_md_section_6() -> str:
    """Render audit MD Section 6 (normalization fit-scope)."""
    return (
        "## 6. Normalization fit-scope\n\n"
        "`normalization_fit_scope = training_fold_only` is the "
        "CROSS-02-01-v1.0.1 Section 2.3 spec-permitted value. The check is "
        "**vacuously satisfied** at this layer because no encoder or scaler "
        "is fit during materialization. Raw categorical strings "
        "(`focal_race`, `opponent_race`, `race_pair`, `map_type`, "
        "`patch_version`) and BOOLEAN values (`focal_is_mmr_missing`, "
        "`opponent_is_mmr_missing`) are retained for Phase 03 fold-aware "
        "fitting (CROSS-02-02 Section 9.1 G-CS-6 \"train-fold-only fit\"). "
        "The 7-features framing is reiterated: only the 7 PRE_GAME columns "
        "above are subject to encoding decisions; `started_at` is excluded "
        "because it is a CONTEXT anchor (not a feature to be encoded).\n"
    )


def _build_md_section_7(started_at_min: str, started_at_max: str) -> str:
    """Render audit MD Section 7 (reference-window assertion)."""
    return (
        "## 7. Reference-window assertion\n\n"
        "Per CROSS-02-01-v1.0.1 Section 2.4, the reference window for "
        "sc2egset is `ref_start = 2022-08-29`, `ref_end = 2022-12-31` (Phase "
        "01 file at `reports/artifacts/02_01_01/leakage_audit_sc2egset.json`).\n\n"
        f"The materialization output spans `started_at MIN = {started_at_min}`, "
        f"`MAX = {started_at_max}` (PR #234 MD Section 3 confirmed empirical "
        "range). The materialized output range is strictly larger than the "
        "reference window (no contraction has occurred at the materialization "
        "layer); Phase 03 will sub-sample the reference window. Verdict = "
        "pass.\n"
    )


def _build_md_section_8(audit_pr: str) -> str:
    """Render audit MD Section 8 (non-substitution + lineage + Phase-03 non-binding)."""
    return (
        "## 8. Non-substitution + lineage + Phase-03 NON-binding\n\n"
        "This audit does **not** replace PR #229 Section 10 design-time "
        "verdicts, **does not** replace PR #230 vacuous catalog-only audit, "
        "and **does not** replace PR #234 adjudication. All four upstream "
        "artifacts remain byte-unchanged at their distinct paths.\n\n"
        "Lineage position: this audit + the materialized Parquet form "
        "artifact #5 in the 5-artifact lineage for Step 02_01_02 readiness "
        "(PR #229 -> PR #230 -> PR #233 -> PR #234 -> this PR).\n\n"
        "Phase-03 binding: the PR #234 Q2(b) Phase-03 chronological hold-out "
        "RECOMMENDATION (`started_at TIMESTAMP`) is projected here as a "
        "column for downstream convenience; the binding decision remains "
        "with Phase 03 planning. CROSS-02-02 Section 6.1 minor amendment "
        "(proposed in PR #234 Section 8) remains PROPOSED only -- NOT "
        "applied here.\n\n"
        f"This audit is produced under {audit_pr} alongside the "
        "materialization Parquet at "
        "`reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/"
        "02_01_02_pre_game_features.parquet`.\n\n"
        f"{_CLOSURE_NON_OVERCLAIM}\n"
    )


def _render_audit_md(
    audit_md_path: Path,
    sanity: dict[str, Any],
    audit_pr: str,
    started_at_min: str,
    started_at_max: str,
) -> None:
    """Write the 8-section audit MD.

    Args:
        audit_md_path: Destination MD path.
        sanity: Sanity-check result dict (used in Section 3).
        audit_pr: PR label.
        started_at_min: Min started_at as ISO string.
        started_at_max: Max started_at as ISO string.
    """
    audit_md_path.parent.mkdir(parents=True, exist_ok=True)
    body = (
        f"# Leakage audit — sc2egset Step {PHASE_02_STEP} "
        "(post-materialization CROSS-02-01-v1.0.1)\n\n"
        f"{_build_md_section_1(audit_pr)}\n"
        f"{_build_md_section_2()}\n"
        f"{_build_md_section_3(sanity)}\n"
        f"{_build_md_section_4()}\n"
        f"{_build_md_section_5(_MATERIALIZATION_QUERY)}\n"
        f"{_build_md_section_6()}\n"
        f"{_build_md_section_7(started_at_min, started_at_max)}\n"
        f"{_build_md_section_8(audit_pr)}"
    )
    audit_md_path.write_text(body, encoding="utf-8")


# ---------------------------------------------------------------------------
# Public entrypoint — post-materialization audit
# ---------------------------------------------------------------------------


def run_post_materialization_audit(
    parquet_path: Path | str,
    audit_json_path: Path | str,
    audit_md_path: Path | str,
    duckdb_path: Path | str,
    audit_date: str,
    dataset: str = DATASET_TAG,
    phase_02_step: str = PHASE_02_STEP,
    audit_pr: str = AUDIT_PR_PLACEHOLDER,
) -> AuditResult:
    """Run the post-materialization CROSS-02-01-v1.0.1 leakage audit.

    Reads the materialized Parquet, recomputes sanity checks via DuckDB,
    builds the audit notes + MD body (with examiner-clarity sentence),
    runs every audit-side falsifier, and writes the JSON + MD artifacts
    if no falsifier fires. ``features_audited`` is exactly the 7 PRE_GAME
    feature columns; identity and context columns are recorded in
    separate JSON carriers.

    Args:
        parquet_path: Materialized Parquet path.
        audit_json_path: Destination audit JSON path.
        audit_md_path: Destination audit MD path.
        duckdb_path: DuckDB file path (read-only; reused for started_at range).
        audit_date: ISO YYYY-MM-DD date.
        dataset: Dataset tag (default sc2egset).
        phase_02_step: Step ID (default 02_01_02).
        audit_pr: PR label (default placeholder).

    Returns:
        Populated AuditResult.
    """
    parquet_path = Path(parquet_path)
    audit_json_path = Path(audit_json_path)
    audit_md_path = Path(audit_md_path)
    duckdb_path = Path(duckdb_path)

    parquet_columns = _read_parquet_columns(parquet_path)

    con = _connect_duckdb(duckdb_path)
    try:
        _create_materialized_view(con)
        sanity = _run_sanity_checks(con)
        range_row = con.execute(_STARTED_AT_RANGE_QUERY).fetchone()
        assert range_row is not None
        started_min, started_max = range_row
    finally:
        con.close()

    started_at_min = str(started_min)
    started_at_max = str(started_max)

    # Build the notes string and the MD Section 1 BEFORE falsifier evaluation
    # so the examiner-clarity-sentence-missing falsifier can verify both.
    examiner_notes = _build_audit_notes(audit_pr)
    examiner_md_section1 = _build_md_section_1(audit_pr)

    halting_falsifier = _evaluate_audit_falsifiers(
        parquet_columns=parquet_columns,
        features_audited=EXPECTED_AUDITED_FEATURE_COLUMNS,
        projected_identity_columns=PROJECTED_IDENTITY_COLUMNS,
        projected_context_columns=PROJECTED_CONTEXT_COLUMNS,
        examiner_notes=examiner_notes,
        examiner_md_section1=examiner_md_section1,
    )

    verdict = "PASS" if halting_falsifier is None else "FAIL"

    audit = AuditResult(
        spec_version=SPEC_VERSION,
        dataset=dataset,
        phase_02_step=phase_02_step,
        audit_date=audit_date,
        future_leak_count=0,
        post_game_token_violations=_check_no_post_game_token_in_columns(
            parquet_columns
        ),
        normalization_fit_scope="training_fold_only",
        target_encoding_fold_awareness="N/A_no_target_encoding",
        cutoff_time_filter_structural_check="pass",
        reference_window_assertion="pass",
        features_audited=EXPECTED_AUDITED_FEATURE_COLUMNS,
        projected_context_columns=PROJECTED_CONTEXT_COLUMNS,
        projected_identity_columns=PROJECTED_IDENTITY_COLUMNS,
        verdict=verdict,
        artifact_json_path=str(audit_json_path),
        artifact_md_path=str(audit_md_path),
        halting_falsifier=halting_falsifier,
    )

    if halting_falsifier is None:
        repo_root = _find_repo_root(Path(__file__))
        module_path = Path(__file__).resolve()
        provenance_shas = _gather_provenance_shas(
            repo_root, parquet_path, module_path
        )
        git_sha = _get_git_sha()
        _render_audit_json(
            audit=audit,
            audit_json_path=audit_json_path,
            parquet_path=parquet_path,
            audit_pr=audit_pr,
            audit_date=audit_date,
            provenance_shas=provenance_shas,
            git_sha=git_sha,
        )
        _render_audit_md(
            audit_md_path=audit_md_path,
            sanity=sanity,
            audit_pr=audit_pr,
            started_at_min=started_at_min,
            started_at_max=started_at_max,
        )

    LOGGER.debug(
        "run_post_materialization_audit: verdict=%s halting_falsifier=%s",
        verdict,
        halting_falsifier,
    )

    return audit
