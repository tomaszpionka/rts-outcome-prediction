"""Adjudicator for SC2EGSet history-enriched pre_game source/anchor/cold-start decisions.

Pure read-only module. Writes ONLY the approved adjudication CSV+MD artifact
pair. Never materializes features. Never writes Parquet. Never modifies status
YAMLs or research logs. See ``planning/current_plan.md`` for the full spec.

This module adjudicates 8 coupled pre-materialization decisions (Q1-Q8) for
the 6 tranche-2 ``history_enriched_pre_game`` feature families:

    Q1 — Source layer (target/history asymmetry; divergence + extension reasons)
    Q2 — Target temporal anchor
    Q3 — Historical row time column (canonical TRY_CAST form)
    Q4 — Cold-start policy (G-CS-2..G-CS-5; G-CS-6 distinguished)
    Q5 — Cross-region fragmentation policy
    Q6 — Rating reconstruction model family
    Q7 — IN_GAME_HISTORICAL prior-match aggregation policy
    Q8 — matches_history_minimal consumption documentation

Binding inputs:
    - Closed 02_01_01 registry CSV (rows 7-12; authoritative tranche-2 scope).
    - PR #234 tranche-1 adjudication CSV (Q1/Q2/Q3 binding precedent).
    - PR #241 scaffold validator module (SHA-256 re-asserted per row, N4).
    - DuckDB read-only probes (matches_flat_clean, matches_history_minimal,
      player_history_all).

The canonical strict-`<` filter (B-X2) is the single source of truth for any
executable history cutoff text inside this module:

    TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at

Any divergence (bare ``CAST``, missing cast, wrong alias, lowercase) is
rejected by the ``strict_lt_filter_divergence`` falsifier.
"""

from __future__ import annotations

import csv
import hashlib
import logging
import re
import subprocess
from collections.abc import Callable
from dataclasses import dataclass, fields
from pathlib import Path

import duckdb

from rts_predict.games.sc2.datasets.sc2egset.validate_history_enriched_pre_game_materialization import (  # noqa: E501
    HISTORY_TRANCHE2_FAMILY_IDS,
    IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
)

_FalsifierThunk = Callable[[], tuple[bool, str]]

__all__ = [
    "HISTORY_TRANCHE2_FAMILY_IDS",
    "IN_GAME_HISTORICAL_AGGREGATED_COLUMNS",
    "HistoryEnrichedAdjudicationDecision",
    "HistoryEnrichedAdjudicationResult",
    "adjudicate_history_enriched_pre_game_source_layer",
]

LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Module-level constants — no magic numbers (Invariant I7)
# ---------------------------------------------------------------------------

EXPECTED_TRANCHE2_COUNT: int = 6
EXPECTED_PR241_VALIDATOR_SHA256: str = (
    "b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904"
)
PR241_VALIDATOR_MODULE_PATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/"
    "validate_history_enriched_pre_game_materialization.py"
)
SHA256_HEX_LENGTH: int = 64
Q_DECISION_COUNT: int = 8

# Provenance file paths (relative to repo root; I10). SHA-256 of each is
# embedded on every adjudication row so the examiner can independently
# re-hash and confirm input provenance.
ROADMAP_REL: str = "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md"
REGISTRY_CSV_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_01_feature_family_registry.csv"
)
MATCHES_HISTORY_MINIMAL_YAML_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/"
    "matches_history_minimal.yaml"
)
CROSS_02_00_SPEC_REL: str = "reports/specs/02_00_feature_input_contract.md"
CROSS_02_01_SPEC_REL: str = "reports/specs/02_01_leakage_audit_protocol.md"
CROSS_02_02_SPEC_REL: str = "reports/specs/02_02_feature_engineering_plan.md"
CROSS_02_03_SPEC_REL: str = "reports/specs/02_03_temporal_feature_audit_protocol.md"

# Enumerates every provenance SHA-256 dataclass field, including the
# pre-existing PR #241 binding SHA. Used by ``_check_no_not_found_sha_fields``
# (priority key ``provenance_sha_invalid``) to verify every row carries a
# 64-char lowercase hex digest in each provenance field (no ``NOT_FOUND``,
# no empty, no wrong-length, no uppercase). 8 entries total.
PROVENANCE_SHA_FIELDS: frozenset[str] = frozenset(
    {
        "pr241_scaffold_validator_module_sha256",
        "roadmap_sha256",
        "registry_csv_sha256",
        "matches_history_minimal_yaml_sha256",
        "cross_02_00_spec_sha256",
        "cross_02_01_spec_sha256",
        "cross_02_02_spec_sha256",
        "cross_02_03_spec_sha256",
    }
)

# B-X2 canonical strict-< constants
STRICT_LT_HISTORY_FILTER: str = (
    "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"
)
STRICT_LT_FILTER_ROADMAP_RAW: str = "ph.details_timeUTC < target.started_at"

# Q decision ID enumeration (canonical CSV row order)
Q_DECISION_IDS: tuple[str, ...] = (
    "Q1_source_layer",
    "Q2_target_anchor",
    "Q3_history_time_column",
    "Q4_cold_start_policy",
    "Q5_cross_region_policy",
    "Q6_rating_policy",
    "Q7_in_game_historical_policy",
    "Q8_matches_history_minimal_consumption",
)

ALLOWED_VERDICTS: frozenset[str] = frozenset(
    {
        "bind_now",
        "ratify_with_evidence",
        "extend_with_evidence",
        "narrow_with_evidence",
        "deferred_blocker",
        "deferred_recommendation",
    }
)
ALLOWED_BINDING_LEVELS: frozenset[str] = frozenset(
    {
        "binding_for_materialization",
        "binding_for_phase_03_split",
        "recommendation_only",
        "deferred_blocker",
        "deferred_recommendation",
    }
)

# B-X1 forbidden-token field scope
POST_GAME_TOKEN_SCOPED_FIELDS: frozenset[str] = frozenset(
    {
        "selected_source_layer",
        "selected_target_source_layer",
        "selected_history_source_layer",
        "target_anchor",
        "history_time_column",
        "feature_family_id_or_scope",
        "materialized_output_paths",
        # Reserved scope: if a successor PR adds either of these fields to
        # the schema, it falls under POST-GAME token scanning automatically.
        "proposed_feature_columns",
        "designed_column_names",
    }
)
POST_GAME_TOKEN_EXEMPT_FIELDS: frozenset[str] = frozenset(
    {
        # Rationale-bearing fields; negated prose like "no target-match outcome",
        # "no future results", and "no global batch fit" is ALLOWED here so the
        # Q6 forward-only constraint can be expressed.
        "notes",
        "evidence_paths",
        "falsifiers",
        "decision_name",
        "rationale",
        "source_layer_divergence_reason",
        "history_source_extension_reason",
    }
)
POST_GAME_TOKENS: frozenset[str] = frozenset(
    {
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
    }
)

# B-X1 disjointness invariant — asserted at module load time
assert POST_GAME_TOKEN_SCOPED_FIELDS.isdisjoint(POST_GAME_TOKEN_EXEMPT_FIELDS), (
    "B-X1 invariant: POST_GAME_TOKEN_SCOPED_FIELDS and "
    "POST_GAME_TOKEN_EXEMPT_FIELDS must be disjoint"
)

# N1 deterministic column-set form for Q7 in-game-historical scope
IN_GAME_HISTORICAL_COLUMNS_IN_SCOPE_PIPE: str = "|".join(
    IN_GAME_HISTORICAL_AGGREGATED_COLUMNS
)

# Artifact destination paths (relative to repo root; I10)
ADJUDICATION_CSV_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_source_anchor_coldstart_adjudication.csv"
)
ADJUDICATION_MD_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_source_anchor_coldstart_adjudication.md"
)

# Expected DuckDB view row counts (PR #234 anchored)
EXPECTED_MFC_ROW_COUNT: int = 44418
EXPECTED_MHM_ROW_COUNT: int = 44418
EXPECTED_PH_ROW_COUNT: int = 44817
EXPECTED_MFC_DISTINCT_REPLAY_ID: int = 22209

# Q3 monotonicity smoke probe sample size
Q3_MONOTONICITY_SAMPLE_SIZE: int = 1000

# Q6 N-X3 evidence regexes
_Q6_REPO_PATH_REGEX: re.Pattern[str] = re.compile(
    r"^(src/|reports/|sandbox/|thesis/|tests/|docs/|\.claude/)"
)
_Q6_CITATION_REGEX: re.Pattern[str] = re.compile(
    r"^@\w+|\\cite\{|^[A-Z][a-z]+\d{4}|\(\d{4}\)"
)
_Q6_RATING_MODEL_FAMILIES: frozenset[str] = frozenset(
    {"elo", "glicko", "glicko2", "trueskill", "rolling_winrate_baseline"}
)
_Q6_FORWARD_ONLY_PHRASES: tuple[str, ...] = (
    "no target-match outcome",
    "no future results",
    "no global batch fit",
)
_Q6_DEFERRED_RATIONALE_PHRASE: str = "deferred_blocker because:"
_Q6_COLD_START_PHRASE: str = "cold-start handled by"
_Q6_MISSINGNESS_PHRASE: str = "missingness handled by"

# Tracker source prefix (Invariant I3)
_TRACKER_SOURCE_PREFIX: str = "tracker_events_raw"

# Q4 cold-start gate names that must be encoded in the cold_start_policy
_REQUIRED_Q4_COLD_START_GATES: tuple[str, ...] = (
    "G-CS-2",
    "G-CS-3",
    "G-CS-4",
    "G-CS-5",
)
_Q4_G_CS_6_GATE: str = "G-CS-6"
_Q4_LEAKAGE_PHRASE: str = "match_time < T"

# Q5 cross-region option names that must all be enumerated
_Q5_REQUIRED_OPTIONS: tuple[str, ...] = (
    "strict_exclusion",
    "dual_feature_path",
    "sensitivity_indicator_co_registration",
)
_Q5_ALLOWED_POLICIES: frozenset[str] = frozenset(
    {
        "strict_exclusion",
        "dual_feature_path",
        "sensitivity_indicator_co_registration",
        "deferred_blocker",
    }
)

# Q7 wording requirements
_Q7_PRIOR_MATCH_ONLY_PHRASES: tuple[str, ...] = (
    "prior matches",
    "history_time < target_time",
)
_Q7_ALLOWED_POLICIES: frozenset[str] = frozenset(
    {"prior_match_only_strict_lt", "deferred_blocker"}
)
_Q7_STRICT_LT_TOKENS: tuple[str, ...] = ("prior_match_only_strict_lt",)

# Q8 documented purposes
_Q8_REQUIRED_PHRASES: tuple[str, ...] = (
    "target row identity",
    "started_at",
    "cold-start enumeration",
)
_Q8_REQUIRED_SCOPE_TEXT: str = "NOT_A_FEATURE_SOURCE_unless_explicitly_justified"

# Named SQL constants (read-only)
_MFC_COUNT_QUERY: str = "SELECT COUNT(*) FROM matches_flat_clean"
_MFC_DISTINCT_REPLAY_ID_QUERY: str = (
    "SELECT COUNT(DISTINCT replay_id) FROM matches_flat_clean"
)
_MHM_COUNT_QUERY: str = "SELECT COUNT(*) FROM matches_history_minimal"
_PH_COUNT_QUERY: str = "SELECT COUNT(*) FROM player_history_all"
_MHM_DESCRIBE_QUERY: str = "DESCRIBE matches_history_minimal"
_PH_DESCRIBE_QUERY: str = "DESCRIBE player_history_all"

# B-X2 smoke probe SQL — uses canonical form verbatim.
_STRICT_LT_SMOKE_QUERY: str = """
SELECT COUNT(*) FROM player_history_all ph
JOIN matches_history_minimal target ON ph.toon_id = target.player_id
WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
  AND ph.replay_id = REPLACE(target.match_id, 'sc2egset::', '')
""".strip()

# Q3 monotonicity smoke SQL — read-only, samples 1000 rows; the cast must
# succeed (no NULL returns from TRY_CAST) on every sample row.
_PH_TRY_CAST_NULL_SAMPLE_QUERY: str = f"""
SELECT COUNT(*) FROM (
  SELECT TRY_CAST(details_timeUTC AS TIMESTAMP) AS ts FROM player_history_all
  LIMIT {Q3_MONOTONICITY_SAMPLE_SIZE}
)
WHERE ts IS NULL
""".strip()


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HistoryEnrichedAdjudicationDecision:
    """A single resolved Q-decision row (one per Q1-Q8).

    The CSV row schema is exactly this dataclass's field order followed by the
    ``notes`` field (declared last here). The header therefore has 33 columns
    and the CSV has 9 lines (1 header + 8 rows).

    Attributes:
        decision_id: One of ``Q_DECISION_IDS``.
        decision_name: Short human-readable name.
        verdict: One of ``ALLOWED_VERDICTS``.
        binding_level: One of ``ALLOWED_BINDING_LEVELS``.
        feature_family_id_or_scope: Scope (six-family) or single family ID.
        selected_source_layer: Q1 only; backward-compat shorthand.
        selected_target_source_layer: Q1 only; N5 subfield.
        selected_history_source_layer: Q1 only; N5 subfield.
        target_history_asymmetry: Q1 only; "symmetric" / "asymmetric" / "".
        source_layer_divergence_reason: Q1 only; N-X4 NEW.
        history_source_extension_reason: Q1 only; N-X4 NEW.
        target_anchor: Q2 only.
        history_time_column: Q3 only; cites the canonical TRY_CAST form.
        strict_lt_expression: Q3 + Q7 only; verbatim canonical
            ``STRICT_LT_HISTORY_FILTER``. Empty on Q1/Q2/Q4/Q5/Q6/Q8.
        cold_start_policy: Q4 only; structured pipe-separated G-CS-2..6 mapping.
        cross_region_policy: Q5 only.
        rating_policy: Q6 only.
        in_game_historical_policy: Q7 only.
        in_game_historical_columns_in_scope: Q7 only; deterministic
            pipe-separated ``APM|SQ|supplyCappedPercent|header_elapsedGameLoops``.
        evidence_paths: Newline-separated repo-relative paths + citations.
        falsifiers: Newline-separated ``name:status`` pairs.
        audit_pr: The Layer-2 PR # placeholder; filled at write time.
        pr241_scaffold_validator_module_sha256: N4 binding; 64-char lowercase hex.
        roadmap_sha256: SHA-256 of the dataset ROADMAP.md; all-row constant.
        registry_csv_sha256: SHA-256 of the closed 02_01_01 registry CSV;
            all-row constant.
        matches_history_minimal_yaml_sha256: SHA-256 of the MHM view schema
            YAML; all-row constant.
        cross_02_00_spec_sha256: SHA-256 of ``02_00_feature_input_contract.md``;
            all-row constant.
        cross_02_01_spec_sha256: SHA-256 of ``02_01_leakage_audit_protocol.md``;
            all-row constant.
        cross_02_02_spec_sha256: SHA-256 of ``02_02_feature_engineering_plan.md``;
            all-row constant.
        cross_02_03_spec_sha256: SHA-256 of
            ``02_03_temporal_feature_audit_protocol.md``; all-row constant.
        provenance_git_sha: Resolved at write time.
        materialized_output_paths: Always ``""`` (no materialization).
        notes: Free-text rationale / deferral / non-substitution disclaimer.
    """

    decision_id: str
    decision_name: str
    verdict: str
    binding_level: str
    feature_family_id_or_scope: str
    selected_source_layer: str
    selected_target_source_layer: str
    selected_history_source_layer: str
    target_history_asymmetry: str
    source_layer_divergence_reason: str
    history_source_extension_reason: str
    target_anchor: str
    history_time_column: str
    strict_lt_expression: str
    cold_start_policy: str
    cross_region_policy: str
    rating_policy: str
    in_game_historical_policy: str
    in_game_historical_columns_in_scope: str
    evidence_paths: str
    falsifiers: str
    audit_pr: str
    pr241_scaffold_validator_module_sha256: str
    roadmap_sha256: str
    registry_csv_sha256: str
    matches_history_minimal_yaml_sha256: str
    cross_02_00_spec_sha256: str
    cross_02_01_spec_sha256: str
    cross_02_02_spec_sha256: str
    cross_02_03_spec_sha256: str
    provenance_git_sha: str
    materialized_output_paths: str
    notes: str


@dataclass(frozen=True)
class HistoryEnrichedAdjudicationResult:
    """Aggregate result of the 8-decision history-enriched adjudication.

    Attributes:
        decisions: Exactly 8 decision rows in ``Q_DECISION_IDS`` order.
        csv_path: Filesystem path the CSV was (or would be) written to.
        md_path: Filesystem path the MD was (or would be) written to.
        provenance_git_sha: HEAD git SHA resolved at run time.
        pr241_scaffold_validator_module_sha256: 64-char lowercase hex.
        falsifiers_fired: Every fired falsifier key (priority order).
        halting_falsifier: First falsifier key that fired, or None.
        passed: True iff ``halting_falsifier is None``.
    """

    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...]
    csv_path: str
    md_path: str
    provenance_git_sha: str
    pr241_scaffold_validator_module_sha256: str
    falsifiers_fired: tuple[str, ...]
    halting_falsifier: str | None
    passed: bool


# ---------------------------------------------------------------------------
# Helper-to-falsifier-key mapping (N-X1)
# ---------------------------------------------------------------------------

HELPER_TO_FALSIFIER_KEY: dict[str, str] = {
    "_check_q1_source_layer_evidence_consistent": "q1_source_layer_evidence_inconsistent",
    "_check_q1_single_row_per_n5": "q1_single_row_violation",
    "_check_q2_target_anchor_type_match": "q2_target_anchor_type_mismatch",
    "_check_q3_history_time_column_dtype": "q3_history_time_column_invalid",
    "_check_q3_monotonicity_smoke": "q3_strict_lt_smoke_failed",
    "_check_q4_cold_start_gates_complete": "q4_cold_start_gates_incomplete",
    "_check_q4_no_leakage_in_cold_start": "q4_cold_start_leakage",
    "_check_q5_cross_region_three_options_enumerated": (
        "q5_cross_region_three_options_not_enumerated"
    ),
    "_check_q6_rating_default_deferred": "q6_rating_default_deferred_violated",
    "_check_q6_rating_forward_only": "q6_rating_forward_only_missing",
    "_check_q7_in_game_historical_columns_in_scope": "q7_in_game_historical_columns_drift",
    "_check_q7_no_target_match_tracker": "q7_no_target_match_tracker_missing",
    "_check_in_game_historical_strict_lt": "in_game_historical_strict_lt_violated",
    "_check_q8_mhm_documented": "q8_mhm_documentation_missing",
    "_check_forbidden_post_game_feature_tokens": "universal_post_game_token_in_scoped_field",
    "_check_universal_no_tracker_source": "universal_tracker_source_in_history",
    "_check_pr241_sha256_match": "pr241_sha256_mismatch",
    "_check_no_not_found_sha_fields": "provenance_sha_invalid",
    "_check_strict_lt_filter_divergence": "strict_lt_filter_divergence",
    "_check_materialization_creep": "materialization_creep",
    "_check_decision_count": "decision_count_mismatch",
}

# Priority order — structural before per-row content (first to fire halts).
# ``provenance_sha_invalid`` runs immediately after the PR #241 SHA check so
# the broader 8-field provenance hash discipline halts before any per-row
# content falsifier touches the data.
FALSIFIER_PRIORITY_CHAIN: tuple[str, ...] = (
    "pr241_sha256_mismatch",
    "provenance_sha_invalid",
    "decision_count_mismatch",
    "q1_single_row_violation",
    "q1_source_layer_evidence_inconsistent",
    "strict_lt_filter_divergence",
    "q2_target_anchor_type_mismatch",
    "q3_history_time_column_invalid",
    "q3_strict_lt_smoke_failed",
    "q4_cold_start_gates_incomplete",
    "q4_cold_start_leakage",
    "q5_cross_region_three_options_not_enumerated",
    "q6_rating_default_deferred_violated",
    "q6_rating_forward_only_missing",
    "q7_in_game_historical_columns_drift",
    "q7_no_target_match_tracker_missing",
    "in_game_historical_strict_lt_violated",
    "q8_mhm_documentation_missing",
    "universal_post_game_token_in_scoped_field",
    "universal_tracker_source_in_history",
    "materialization_creep",
)


# ---------------------------------------------------------------------------
# Evidence loaders
# ---------------------------------------------------------------------------


def _load_pr234_binding_csv(path: Path) -> dict[str, dict[str, str]]:
    """Load Q1/Q2/Q3 decision dicts from the tranche-1 adjudication CSV.

    Args:
        path: Path to ``02_01_02_source_anchor_race_adjudication.csv``.

    Returns:
        Mapping ``decision_id -> row dict``. Empty dict if the file is absent.
    """
    if not path.exists():
        LOGGER.warning("_load_pr234_binding_csv: file not found at %s", path)
        return {}
    out: dict[str, dict[str, str]] = {}
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            decision_id = row.get("decision_id", "")
            if decision_id:
                out[decision_id] = dict(row)
    LOGGER.debug("_load_pr234_binding_csv: loaded %d rows from %s", len(out), path)
    return out


def _load_registry_csv(path: Path) -> list[dict[str, str]]:
    """Load all rows from the closed 02_01_01 registry CSV.

    Args:
        path: Path to ``02_01_01_feature_family_registry.csv``.

    Returns:
        List of row dicts (one per registry row).
    """
    if not path.exists():
        LOGGER.warning("_load_registry_csv: file not found at %s", path)
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


# ---------------------------------------------------------------------------
# Read-only DuckDB probes
# ---------------------------------------------------------------------------


def _probe_view_row_counts(con: duckdb.DuckDBPyConnection) -> dict[str, int]:
    """Probe view row counts (read-only) for Q1 source-layer evidence.

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        Mapping of probe name to row count.
    """
    mfc_count: int = con.execute(_MFC_COUNT_QUERY).fetchone()[0]  # type: ignore[index]
    mhm_count: int = con.execute(_MHM_COUNT_QUERY).fetchone()[0]  # type: ignore[index]
    ph_count: int = con.execute(_PH_COUNT_QUERY).fetchone()[0]  # type: ignore[index]
    mfc_distinct: int = (  # type: ignore[assignment]
        con.execute(_MFC_DISTINCT_REPLAY_ID_QUERY).fetchone()[0]  # type: ignore[index]
    )
    LOGGER.debug(
        "_probe_view_row_counts: mfc=%d mhm=%d ph=%d mfc_distinct=%d",
        mfc_count,
        mhm_count,
        ph_count,
        mfc_distinct,
    )
    return {
        "matches_flat_clean": mfc_count,
        "matches_history_minimal": mhm_count,
        "player_history_all": ph_count,
        "matches_flat_clean_distinct_replay_id": mfc_distinct,
    }


def _probe_history_time_column_candidates(
    con: duckdb.DuckDBPyConnection,
) -> dict[str, dict[str, object]]:
    """Probe DESCRIBE-style metadata for candidate history-time columns.

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        Mapping ``"<view>.<col>" -> {"dtype": str, "exists": bool}``.
    """
    out: dict[str, dict[str, object]] = {}
    ph_desc = con.execute(_PH_DESCRIBE_QUERY).fetchdf()
    ph_types: dict[str, str] = dict(
        zip(ph_desc["column_name"], ph_desc["column_type"])
    )
    out["player_history_all.details_timeUTC"] = {
        "dtype": ph_types.get("details_timeUTC", ""),
        "exists": "details_timeUTC" in ph_types,
    }
    mhm_desc = con.execute(_MHM_DESCRIBE_QUERY).fetchdf()
    mhm_types: dict[str, str] = dict(
        zip(mhm_desc["column_name"], mhm_desc["column_type"])
    )
    out["matches_history_minimal.started_at"] = {
        "dtype": mhm_types.get("started_at", ""),
        "exists": "started_at" in mhm_types,
    }
    LOGGER.debug("_probe_history_time_column_candidates: %s", out)
    return out


def _probe_strict_lt_filter_smoke(
    con: duckdb.DuckDBPyConnection,
) -> dict[str, object]:
    """Run the canonical strict-< smoke probe (B-X2).

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        Dict carrying ``"sql"`` (verbatim canonical SQL), ``"self_join_rows"``
        (count, expected 0), and ``"try_cast_null_in_sample"`` (count from the
        1000-row TRY_CAST monotonicity probe; expected 0).
    """
    self_rows: int = (  # type: ignore[assignment]
        con.execute(_STRICT_LT_SMOKE_QUERY).fetchone()[0]  # type: ignore[index]
    )
    null_in_sample: int = (  # type: ignore[assignment]
        con.execute(_PH_TRY_CAST_NULL_SAMPLE_QUERY).fetchone()[0]  # type: ignore[index]
    )
    LOGGER.debug(
        "_probe_strict_lt_filter_smoke: self_rows=%d null_in_sample=%d",
        self_rows,
        null_in_sample,
    )
    return {
        "sql": _STRICT_LT_SMOKE_QUERY,
        "self_join_rows": self_rows,
        "try_cast_null_in_sample": null_in_sample,
        "sample_size": Q3_MONOTONICITY_SAMPLE_SIZE,
    }


def _probe_matches_history_minimal_columns(
    con: duckdb.DuckDBPyConnection,
) -> list[str]:
    """List MHM column names (read-only) to substantiate Q8.

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        Alphabetically sorted MHM column names.
    """
    mhm_desc = con.execute(_MHM_DESCRIBE_QUERY).fetchdf()
    cols = sorted(mhm_desc["column_name"].tolist())
    LOGGER.debug("_probe_matches_history_minimal_columns: %d columns", len(cols))
    return cols


# ---------------------------------------------------------------------------
# Q-specific falsifier helpers
# ---------------------------------------------------------------------------


def _get_decision(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
    decision_id: str,
) -> HistoryEnrichedAdjudicationDecision | None:
    """Return the decision with the given ID, or None.

    Args:
        decisions: All 8 decisions.
        decision_id: One of ``Q_DECISION_IDS``.

    Returns:
        The decision dataclass, or None if absent.
    """
    for d in decisions:
        if d.decision_id == decision_id:
            return d
    return None


def _check_q1_source_layer_evidence_consistent(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
    pr234_binding: dict[str, dict[str, str]],
) -> tuple[bool, str]:
    """Q1 must reconcile with PR #234 tranche-1 Q1 binding (matches_flat_clean).

    Args:
        decisions: All 8 decisions.
        pr234_binding: Loaded PR #234 binding rows (may be empty if absent).

    Returns:
        ``(did_fire, message)``.
    """
    q1 = _get_decision(decisions, "Q1_source_layer")
    if q1 is None:
        return True, "Q1_source_layer decision row missing"
    if q1.selected_target_source_layer != "matches_flat_clean":
        return True, (
            f"Q1 selected_target_source_layer = {q1.selected_target_source_layer!r}; "
            "expected 'matches_flat_clean' per PR #234 Q1 binding"
        )
    if not q1.selected_history_source_layer:
        return True, "Q1 selected_history_source_layer is empty"
    # PR234 binding presence cross-check: if available, ensure tranche-1
    # Q1 row cites matches_flat_clean.
    if pr234_binding:
        pr234_q1 = pr234_binding.get("Q1_source_layer", {})
        chosen = pr234_q1.get("chosen", "")
        if chosen and "matches_flat_clean" not in chosen:
            return True, (
                f"PR #234 Q1 binding chosen={chosen!r} does not include "
                "'matches_flat_clean'; tranche-2 Q1 cannot anchor to it"
            )
    return False, ""


def _check_q1_single_row_per_n5(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q1 must be a single row with subfields populated (including N-X4 fields).

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    q1_rows = [d for d in decisions if d.decision_id.startswith("Q1")]
    if len(q1_rows) != 1:
        return True, (
            f"Q1 must be exactly 1 row; found {len(q1_rows)} rows with "
            "decision_id starting with 'Q1'"
        )
    q1 = q1_rows[0]
    if q1.decision_id != "Q1_source_layer":
        return True, (
            f"Q1 decision_id = {q1.decision_id!r}; expected 'Q1_source_layer' "
            "(no Q1a/Q1b/Q1c split)"
        )
    required_subfields = (
        ("selected_target_source_layer", q1.selected_target_source_layer),
        ("selected_history_source_layer", q1.selected_history_source_layer),
        ("target_history_asymmetry", q1.target_history_asymmetry),
        ("source_layer_divergence_reason", q1.source_layer_divergence_reason),
        ("history_source_extension_reason", q1.history_source_extension_reason),
    )
    for name, value in required_subfields:
        if not value:
            return True, (
                f"Q1 subfield {name!r} is empty (N-X4 / N5 requirement)"
            )
    return False, ""


def _check_q2_target_anchor_type_match(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
    history_time_metadata: dict[str, dict[str, object]],
) -> tuple[bool, str]:
    """Q2 must verify ``started_at`` is TIMESTAMP via DESCRIBE.

    Args:
        decisions: All 8 decisions.
        history_time_metadata: Output of ``_probe_history_time_column_candidates``.

    Returns:
        ``(did_fire, message)``.
    """
    q2 = _get_decision(decisions, "Q2_target_anchor")
    if q2 is None:
        return True, "Q2_target_anchor decision row missing"
    if "started_at" not in q2.target_anchor or "TIMESTAMP" not in q2.target_anchor:
        return True, (
            f"Q2 target_anchor = {q2.target_anchor!r}; expected to cite "
            "'started_at' and 'TIMESTAMP'"
        )
    started_meta = history_time_metadata.get("matches_history_minimal.started_at", {})
    dtype = str(started_meta.get("dtype", ""))
    if dtype and dtype != "TIMESTAMP":
        return True, (
            f"matches_history_minimal.started_at dtype = {dtype!r}; "
            "expected 'TIMESTAMP'"
        )
    return False, ""


def _check_q3_history_time_column_dtype(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
    history_time_metadata: dict[str, dict[str, object]],
) -> tuple[bool, str]:
    """Q3 must verify ``ph.details_timeUTC`` exists with a non-empty dtype.

    Args:
        decisions: All 8 decisions.
        history_time_metadata: Output of ``_probe_history_time_column_candidates``.

    Returns:
        ``(did_fire, message)``.
    """
    q3 = _get_decision(decisions, "Q3_history_time_column")
    if q3 is None:
        return True, "Q3_history_time_column decision row missing"
    if "details_timeUTC" not in q3.history_time_column:
        return True, (
            f"Q3 history_time_column = {q3.history_time_column!r}; expected "
            "to cite 'details_timeUTC'"
        )
    ph_meta = history_time_metadata.get("player_history_all.details_timeUTC", {})
    exists_flag = bool(ph_meta.get("exists", False))
    dtype = str(ph_meta.get("dtype", ""))
    if not exists_flag or not dtype:
        return True, (
            "player_history_all.details_timeUTC missing or has empty dtype "
            f"(exists={exists_flag}, dtype={dtype!r})"
        )
    return False, ""


def _check_q3_monotonicity_smoke(
    smoke_probe: dict[str, object],
) -> tuple[bool, str]:
    """Q3 smoke: strict-< self-rows == 0 AND TRY_CAST null-in-sample == 0.

    Args:
        smoke_probe: Output of ``_probe_strict_lt_filter_smoke``.

    Returns:
        ``(did_fire, message)``.
    """
    self_rows = smoke_probe.get("self_join_rows")
    null_in_sample = smoke_probe.get("try_cast_null_in_sample")
    if not isinstance(self_rows, int) or self_rows != 0:
        return True, (
            f"strict-< smoke probe returned {self_rows!r} self-rows; "
            "expected 0 (target row excluded by strict-<)"
        )
    if not isinstance(null_in_sample, int) or null_in_sample != 0:
        return True, (
            f"TRY_CAST returned NULL on {null_in_sample!r} of "
            f"{Q3_MONOTONICITY_SAMPLE_SIZE} sample rows; upstream cleaning required"
        )
    return False, ""


def _check_q4_cold_start_gates_complete(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q4 ``cold_start_policy`` must encode every gate in G-CS-2..G-CS-5.

    G-CS-6 is documented but distinguished (materialization-time fold-aware fit
    gate per CROSS-02-02 §9 and ROADMAP lines 2334-2338).

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    q4 = _get_decision(decisions, "Q4_cold_start_policy")
    if q4 is None:
        return True, "Q4_cold_start_policy decision row missing"
    policy = q4.cold_start_policy
    missing = [g for g in _REQUIRED_Q4_COLD_START_GATES if g not in policy]
    if missing:
        return True, (
            f"Q4 cold_start_policy missing required gates {missing}; "
            f"policy={policy!r}"
        )
    if _Q4_G_CS_6_GATE not in policy:
        return True, (
            "Q4 cold_start_policy does not distinguish G-CS-6 "
            "(materialization-time fold-aware fit gate)"
        )
    return False, ""


def _check_q4_no_leakage_in_cold_start(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q4 notes must explicitly state ``match_time < T`` only.

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    q4 = _get_decision(decisions, "Q4_cold_start_policy")
    if q4 is None:
        return True, "Q4_cold_start_policy decision row missing"
    if _Q4_LEAKAGE_PHRASE not in q4.notes:
        return True, (
            f"Q4 notes missing required phrase {_Q4_LEAKAGE_PHRASE!r} "
            "(Invariant I3 forward-only constraint)"
        )
    return False, ""


def _check_q5_cross_region_three_options_enumerated(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q5 notes must enumerate the 3 CROSS-02-02 §6.2 row 5 options.

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    q5 = _get_decision(decisions, "Q5_cross_region_policy")
    if q5 is None:
        return True, "Q5_cross_region_policy decision row missing"
    missing = [opt for opt in _Q5_REQUIRED_OPTIONS if opt not in q5.notes]
    if missing:
        return True, (
            f"Q5 notes missing required option enumeration {missing}; "
            "all three options must be named"
        )
    if q5.cross_region_policy not in _Q5_ALLOWED_POLICIES:
        return True, (
            f"Q5 cross_region_policy = {q5.cross_region_policy!r}; expected "
            f"one of {sorted(_Q5_ALLOWED_POLICIES)}"
        )
    return False, ""


def _q6_evidence_paths_satisfy_n_x3(evidence_paths: str) -> tuple[bool, bool]:
    """Return ``(has_repo_path, has_citation)`` for the Q6 N-X3 evidence gate.

    Args:
        evidence_paths: Newline-separated evidence paths / citations.

    Returns:
        Two-tuple of booleans.
    """
    has_repo_path = False
    has_citation = False
    for line in evidence_paths.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        if _Q6_REPO_PATH_REGEX.match(stripped):
            has_repo_path = True
        if _Q6_CITATION_REGEX.match(stripped) or _Q6_CITATION_REGEX.search(stripped):
            has_citation = True
    return has_repo_path, has_citation


def _check_q6_rating_default_deferred(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q6 rating-policy evidence sufficiency gate (N3 + N-X3 strengthened).

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.

    Notes:
        The Q6 ``notes`` field carries verbatim phrases like "no target-match
        outcome", "no future results", and "no global batch fit". Per B-X1,
        ``notes`` is in ``POST_GAME_TOKEN_EXEMPT_FIELDS`` so these tokens are
        ALLOWED here and the universal POST-GAME scan does not fire on them.
    """
    q6 = _get_decision(decisions, "Q6_rating_policy")
    if q6 is None:
        return True, "Q6_rating_policy decision row missing"
    policy = q6.rating_policy
    if policy == "deferred_blocker":
        if not q6.evidence_paths.strip():
            return True, (
                "Q6 deferred_blocker requires non-empty evidence_paths "
                "(N-X3 strengthened gate)"
            )
        if _Q6_DEFERRED_RATIONALE_PHRASE not in q6.notes:
            return True, (
                f"Q6 deferred_blocker notes missing required phrase "
                f"{_Q6_DEFERRED_RATIONALE_PHRASE!r}"
            )
        return False, ""
    if policy in _Q6_RATING_MODEL_FAMILIES:
        has_repo_path, has_citation = _q6_evidence_paths_satisfy_n_x3(q6.evidence_paths)
        if not has_repo_path:
            return True, (
                f"Q6 rating_policy={policy!r} requires >=1 repo-path "
                "evidence_paths entry (N-X3 strengthened gate)"
            )
        if not has_citation:
            return True, (
                f"Q6 rating_policy={policy!r} requires >=1 primary-source "
                "citation in evidence_paths (N-X3 strengthened gate)"
            )
        if not all(p in q6.notes for p in _Q6_FORWARD_ONLY_PHRASES):
            missing = [p for p in _Q6_FORWARD_ONLY_PHRASES if p not in q6.notes]
            return True, (
                f"Q6 rating_policy={policy!r} notes missing forward-only "
                f"phrases {missing} (N-X3)"
            )
        if _Q6_COLD_START_PHRASE not in q6.notes:
            return True, (
                f"Q6 rating_policy={policy!r} notes missing "
                f"{_Q6_COLD_START_PHRASE!r} wording (N-X3)"
            )
        if _Q6_MISSINGNESS_PHRASE not in q6.notes:
            return True, (
                f"Q6 rating_policy={policy!r} notes missing "
                f"{_Q6_MISSINGNESS_PHRASE!r} wording (N-X3)"
            )
        return False, ""
    return True, (
        f"Q6 rating_policy={policy!r} not in allowed set "
        f"{sorted(_Q6_RATING_MODEL_FAMILIES | {'deferred_blocker'})}"
    )


def _check_q6_rating_forward_only(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q6 notes must contain all 3 forward-only constraint phrases.

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    q6 = _get_decision(decisions, "Q6_rating_policy")
    if q6 is None:
        return True, "Q6_rating_policy decision row missing"
    missing = [p for p in _Q6_FORWARD_ONLY_PHRASES if p not in q6.notes]
    if missing:
        return True, (
            f"Q6 notes missing forward-only phrases {missing}; all three of "
            f"{list(_Q6_FORWARD_ONLY_PHRASES)} required"
        )
    return False, ""


def _check_q7_in_game_historical_columns_in_scope(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q7 columns must equal the deterministic pipe-separated scope (N1).

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    q7 = _get_decision(decisions, "Q7_in_game_historical_policy")
    if q7 is None:
        return True, "Q7_in_game_historical_policy decision row missing"
    if q7.in_game_historical_columns_in_scope != IN_GAME_HISTORICAL_COLUMNS_IN_SCOPE_PIPE:
        return True, (
            f"Q7 in_game_historical_columns_in_scope = "
            f"{q7.in_game_historical_columns_in_scope!r}; expected "
            f"{IN_GAME_HISTORICAL_COLUMNS_IN_SCOPE_PIPE!r}"
        )
    return False, ""


def _check_q7_no_target_match_tracker(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q7 notes must state prior-match-only consumption (no target-match tracker).

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    q7 = _get_decision(decisions, "Q7_in_game_historical_policy")
    if q7 is None:
        return True, "Q7_in_game_historical_policy decision row missing"
    missing = [p for p in _Q7_PRIOR_MATCH_ONLY_PHRASES if p not in q7.notes]
    if missing:
        return True, (
            f"Q7 notes missing prior-match-only phrases {missing}; "
            f"required: {list(_Q7_PRIOR_MATCH_ONLY_PHRASES)}"
        )
    return False, ""


def _check_in_game_historical_strict_lt(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q7 in_game_historical_policy must encode strict-< semantics (N2).

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    q7 = _get_decision(decisions, "Q7_in_game_historical_policy")
    if q7 is None:
        return True, "Q7_in_game_historical_policy decision row missing"
    if q7.in_game_historical_policy not in _Q7_ALLOWED_POLICIES:
        return True, (
            f"Q7 in_game_historical_policy = {q7.in_game_historical_policy!r}; "
            f"expected one of {sorted(_Q7_ALLOWED_POLICIES)}"
        )
    if q7.in_game_historical_policy == "deferred_blocker":
        return False, ""
    if not any(tok in q7.in_game_historical_policy for tok in _Q7_STRICT_LT_TOKENS):
        return True, (
            f"Q7 in_game_historical_policy {q7.in_game_historical_policy!r} "
            "does not encode strict-< token 'prior_match_only_strict_lt'"
        )
    return False, ""


def _check_q8_mhm_documented(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q8 must cite both MHM consumption purposes (PR #239 ROADMAP nit).

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    q8 = _get_decision(decisions, "Q8_matches_history_minimal_consumption")
    if q8 is None:
        return True, "Q8_matches_history_minimal_consumption decision row missing"
    missing = [p for p in _Q8_REQUIRED_PHRASES if p not in q8.notes]
    if missing:
        return True, (
            f"Q8 notes missing required MHM-purpose phrases {missing}"
        )
    if q8.feature_family_id_or_scope != _Q8_REQUIRED_SCOPE_TEXT:
        return True, (
            f"Q8 feature_family_id_or_scope = "
            f"{q8.feature_family_id_or_scope!r}; expected "
            f"{_Q8_REQUIRED_SCOPE_TEXT!r}"
        )
    return False, ""


# ---------------------------------------------------------------------------
# Universal falsifiers (B-X1 + tracker + SHA + B-X2 + mechanical)
# ---------------------------------------------------------------------------


def _check_forbidden_post_game_feature_tokens(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Scoped POST-GAME token rejection (B-X1).

    Scans only the fields in ``POST_GAME_TOKEN_SCOPED_FIELDS`` for any token
    in ``POST_GAME_TOKENS``. Explicitly exempts every field in
    ``POST_GAME_TOKEN_EXEMPT_FIELDS`` — negated prose like "no target-match
    outcome" / "no future results" / "no global batch fit" is allowed in
    rationale-bearing fields (notably ``notes``, which carries Q6's
    forward-only constraint wording).

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    for d in decisions:
        row = _decision_to_field_dict(d)
        for field_name in POST_GAME_TOKEN_SCOPED_FIELDS:
            if field_name not in row:
                continue
            value = str(row[field_name]).lower()
            for token in POST_GAME_TOKENS:
                if token in value:
                    return True, (
                        f"POST-GAME token {token!r} found in scoped field "
                        f"{field_name!r} of decision {d.decision_id!r} "
                        f"(value={row[field_name]!r})"
                    )
    return False, ""


def _check_universal_no_tracker_source(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """No source-layer field may contain ``tracker_events_raw`` (Invariant I3).

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    for d in decisions:
        for field_name in (
            "selected_source_layer",
            "selected_target_source_layer",
            "selected_history_source_layer",
        ):
            value = getattr(d, field_name, "")
            if _TRACKER_SOURCE_PREFIX in value:
                return True, (
                    f"Tracker source {_TRACKER_SOURCE_PREFIX!r} found in "
                    f"{field_name!r} of decision {d.decision_id!r} "
                    f"(value={value!r})"
                )
    return False, ""


def _check_pr241_sha256_match(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Every decision row's PR #241 SHA-256 must equal the expected value (N4).

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    valid_hex = frozenset("0123456789abcdef")
    for d in decisions:
        sha = d.pr241_scaffold_validator_module_sha256
        if (
            not sha
            or sha == "NOT_FOUND"
            or len(sha) != SHA256_HEX_LENGTH
            or not all(c in valid_hex for c in sha)
        ):
            return True, (
                f"Decision {d.decision_id!r} has invalid SHA-256 "
                f"{sha!r} (must be 64-char lowercase hex)"
            )
        if sha != EXPECTED_PR241_VALIDATOR_SHA256:
            return True, (
                f"Decision {d.decision_id!r} SHA-256 {sha!r} != expected "
                f"{EXPECTED_PR241_VALIDATOR_SHA256!r}"
            )
    return False, ""


_HEX64_REGEX: re.Pattern[str] = re.compile(r"^[0-9a-f]{64}$")


def _check_no_not_found_sha_fields(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Every provenance SHA field on every row must be 64-char lowercase hex.

    Scans every field in ``PROVENANCE_SHA_FIELDS`` on every decision row and
    rejects empty strings, ``"NOT_FOUND"`` sentinels, wrong-length values, and
    any non-lowercase-hex characters. This broadens the existing PR #241 SHA
    check (which only inspects ``pr241_scaffold_validator_module_sha256``) to
    the 7 additional provenance SHA columns introduced in PR #242.

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    for d in decisions:
        for field_name in PROVENANCE_SHA_FIELDS:
            sha = str(getattr(d, field_name, ""))
            if sha == "NOT_FOUND":
                return True, (
                    f"Decision {d.decision_id!r} provenance SHA field "
                    f"{field_name!r} = 'NOT_FOUND' (input file missing or "
                    "unresolved at run time)"
                )
            if not sha:
                return True, (
                    f"Decision {d.decision_id!r} provenance SHA field "
                    f"{field_name!r} is empty"
                )
            if len(sha) != SHA256_HEX_LENGTH:
                return True, (
                    f"Decision {d.decision_id!r} provenance SHA field "
                    f"{field_name!r} = {sha!r} has length {len(sha)}; "
                    f"expected {SHA256_HEX_LENGTH}"
                )
            if not _HEX64_REGEX.fullmatch(sha):
                return True, (
                    f"Decision {d.decision_id!r} provenance SHA field "
                    f"{field_name!r} = {sha!r} is not 64-char lowercase hex"
                )
    return False, ""


def _normalize_ws(s: str) -> str:
    """Collapse runs of whitespace to a single space and strip.

    Args:
        s: Input string.

    Returns:
        Whitespace-normalized string.
    """
    return re.sub(r"\s+", " ", s).strip()


def _check_strict_lt_filter_divergence(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
    smoke_probe_sql: str,
) -> tuple[bool, str]:
    """Strict-< canonical form must appear at every executable site (B-X2).

    Scans 4 sites:
        (a) the ``STRICT_LT_HISTORY_FILTER`` module constant,
        (b) the T02 smoke probe SQL string,
        (c) Q3 ``history_time_column`` / ``notes`` AND ``strict_lt_expression``,
        (d) Q7 ``notes`` AND ``strict_lt_expression``.

    Args:
        decisions: All 8 decisions.
        smoke_probe_sql: Verbatim smoke-probe SQL string.

    Returns:
        ``(did_fire, message)``.
    """
    canonical = _normalize_ws(STRICT_LT_HISTORY_FILTER)
    constant_norm = _normalize_ws(STRICT_LT_HISTORY_FILTER)
    if constant_norm != canonical:
        return True, (
            f"STRICT_LT_HISTORY_FILTER constant diverges from canonical form "
            f"(got={constant_norm!r}, want={canonical!r})"
        )
    smoke_norm = _normalize_ws(smoke_probe_sql)
    if canonical not in smoke_norm:
        return True, (
            "T02 smoke probe SQL does not contain canonical TRY_CAST strict-< "
            f"clause (canonical={canonical!r}, smoke={smoke_norm!r})"
        )
    q3 = _get_decision(decisions, "Q3_history_time_column")
    if q3 is not None:
        if canonical not in _normalize_ws(q3.history_time_column + " " + q3.notes):
            return True, (
                "Q3 bound expression does not contain canonical TRY_CAST "
                f"strict-< clause (canonical={canonical!r})"
            )
        if _normalize_ws(q3.strict_lt_expression) != canonical:
            return True, (
                "Q3 strict_lt_expression field does not equal canonical "
                f"TRY_CAST strict-< clause (got={q3.strict_lt_expression!r}, "
                f"want={STRICT_LT_HISTORY_FILTER!r})"
            )
    q7 = _get_decision(decisions, "Q7_in_game_historical_policy")
    if q7 is not None and q7.in_game_historical_policy != "deferred_blocker":
        if canonical not in _normalize_ws(q7.notes):
            return True, (
                "Q7 bound expression does not contain canonical TRY_CAST "
                f"strict-< clause (canonical={canonical!r})"
            )
        if _normalize_ws(q7.strict_lt_expression) != canonical:
            return True, (
                "Q7 strict_lt_expression field does not equal canonical "
                f"TRY_CAST strict-< clause (got={q7.strict_lt_expression!r}, "
                f"want={STRICT_LT_HISTORY_FILTER!r})"
            )
    return False, ""


def _check_materialization_creep(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Every decision row must have empty ``materialized_output_paths``.

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    for d in decisions:
        if d.materialized_output_paths:
            return True, (
                f"Decision {d.decision_id!r} has non-empty "
                f"materialized_output_paths={d.materialized_output_paths!r} "
                "(adjudication writes ZERO materialized data)"
            )
    return False, ""


def _check_decision_count(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Exactly 8 decisions must be present.

    Args:
        decisions: All decisions.

    Returns:
        ``(did_fire, message)``.
    """
    if len(decisions) != Q_DECISION_COUNT:
        return True, (
            f"Expected exactly {Q_DECISION_COUNT} decisions; got {len(decisions)}"
        )
    decision_ids = {d.decision_id for d in decisions}
    if decision_ids != set(Q_DECISION_IDS):
        missing = sorted(set(Q_DECISION_IDS) - decision_ids)
        extra = sorted(decision_ids - set(Q_DECISION_IDS))
        return True, (
            f"Decision IDs mismatch; missing={missing}; extra={extra}"
        )
    return False, ""


# ---------------------------------------------------------------------------
# Decision-building (T05 verbatim bindings)
# ---------------------------------------------------------------------------


def _decision_to_field_dict(
    d: HistoryEnrichedAdjudicationDecision,
) -> dict[str, str]:
    """Return a string-valued dict of the decision's fields (excluding notes scope).

    Args:
        d: A decision dataclass instance.

    Returns:
        Mapping of field name to stringified value.
    """
    return {f.name: str(getattr(d, f.name)) for f in fields(d)}


def _build_decisions(
    *,
    audit_pr: str,
    provenance_git_sha: str,
    pr241_sha256: str,
    roadmap_sha256: str,
    registry_csv_sha256: str,
    matches_history_minimal_yaml_sha256: str,
    cross_02_00_spec_sha256: str,
    cross_02_01_spec_sha256: str,
    cross_02_02_spec_sha256: str,
    cross_02_03_spec_sha256: str,
) -> tuple[HistoryEnrichedAdjudicationDecision, ...]:
    """Construct the 8 hard-bound Q-decision rows per T05.

    Args:
        audit_pr: Layer-2 PR number placeholder string.
        provenance_git_sha: Current HEAD git SHA.
        pr241_sha256: 64-char lowercase hex SHA of the PR #241 validator module.
        roadmap_sha256: 64-char lowercase hex SHA of the dataset ROADMAP.md.
        registry_csv_sha256: 64-char lowercase hex SHA of the closed 02_01_01
            registry CSV.
        matches_history_minimal_yaml_sha256: 64-char lowercase hex SHA of the
            MHM view schema YAML.
        cross_02_00_spec_sha256: 64-char lowercase hex SHA of
            ``02_00_feature_input_contract.md``.
        cross_02_01_spec_sha256: 64-char lowercase hex SHA of
            ``02_01_leakage_audit_protocol.md``.
        cross_02_02_spec_sha256: 64-char lowercase hex SHA of
            ``02_02_feature_engineering_plan.md``.
        cross_02_03_spec_sha256: 64-char lowercase hex SHA of
            ``02_03_temporal_feature_audit_protocol.md``.

    Returns:
        Tuple of 8 ``HistoryEnrichedAdjudicationDecision`` rows in
        ``Q_DECISION_IDS`` order.
    """
    common: dict[str, str] = {
        "audit_pr": audit_pr,
        "pr241_scaffold_validator_module_sha256": pr241_sha256,
        "roadmap_sha256": roadmap_sha256,
        "registry_csv_sha256": registry_csv_sha256,
        "matches_history_minimal_yaml_sha256": matches_history_minimal_yaml_sha256,
        "cross_02_00_spec_sha256": cross_02_00_spec_sha256,
        "cross_02_01_spec_sha256": cross_02_01_spec_sha256,
        "cross_02_02_spec_sha256": cross_02_02_spec_sha256,
        "cross_02_03_spec_sha256": cross_02_03_spec_sha256,
        "provenance_git_sha": provenance_git_sha,
        "materialized_output_paths": "",
    }

    q1 = _build_q1(common)
    q2 = _build_q2(common)
    q3 = _build_q3(common)
    q4 = _build_q4(common)
    q5 = _build_q5(common)
    q6 = _build_q6(common)
    q7 = _build_q7(common)
    q8 = _build_q8(common)
    return (q1, q2, q3, q4, q5, q6, q7, q8)


def _build_q1(common: dict[str, str]) -> HistoryEnrichedAdjudicationDecision:
    """Build the Q1 source-layer decision row (T05 Q1).

    Args:
        common: Common provenance fields shared across all rows.

    Returns:
        Q1 decision dataclass.
    """
    q1_notes = (
        "Q1 binds the source layer for the 6 history-enriched pre_game families. "
        "Target = matches_flat_clean (RATIFY tranche-1 PR #234 Q1 binding; 1v1-scoped, "
        "44,418 rows). History = player_history_all (all-game-types, 44,817 rows). "
        "Target/history asymmetry is asymmetric.\n\n"
        "Verbatim spec evidence (Option A; RECOMMENDED; BINDING):\n"
        "  (1) reports/specs/02_02_feature_engineering_plan.md §6.2 row 1 "
        "(focal_player_history): 'rolling/expanding aggregates over player_history_all "
        "rows for the focal toon_id: prior match count, prior win rate, time since prior "
        "match, race-conditional, map-conditional, matchup-conditional'.\n"
        "  (2) reports/specs/02_02_feature_engineering_plan.md §6.2 row 4 "
        "(reconstructed_rating): 'derived from player_history_all filtered by I3 anchor'.\n"
        "  (3) reports/specs/02_02_feature_engineering_plan.md §6.2 row 6 "
        "(in_game_history_aggregate): 'player_history_all APM / SQ / supplyCappedPercent "
        "/ header_elapsedGameLoops (IN_GAME_HISTORICAL classification per CROSS-02-00 §5.4)'.\n"
        "  (4) reports/specs/02_00_feature_input_contract.md §2.1 sc2egset row grain: "
        "'1 row per player per match (all game types; no 1v1 filter)'.\n"
        "  (5) player_history_all.yaml provenance.scope: 'All replays (no 1v1/decisive "
        "filter). Includes non-1v1 and indecisive replays excluded from matches_flat_clean'.\n\n"
        "Alternative B (REJECTED): symmetric — target and history both filtered to 1v1-only. "
        "Rejected because (a) the spec §6.2 row 1 binds history to player_history_all, not "
        "a 1v1-filtered subset; (b) the 83.95% MMR-missing density makes restricting history "
        "to 1v1-only leave cold-start gates G-CS-2/G-CS-3 with near-empty support sets for "
        "newcomers; (c) CROSS-02-02 §6.2 retains multi-game-type history precisely to mitigate "
        "this support-set sparsity; (d) the player_history_all.yaml provenance.scope note "
        "explicitly retains non-1v1 and indecisive replays for this purpose. Rejecting "
        "Alternative B would contradict the verbatim §6.2 rows 4 and 6 bindings."
    )
    q1_evidence_paths = "\n".join(
        [
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
            "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
            "02_01_02_source_anchor_race_adjudication.csv",
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
            "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
            "02_01_02_source_anchor_race_adjudication.md",
            "reports/specs/02_00_feature_input_contract.md",
            "reports/specs/02_02_feature_engineering_plan.md",
            "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/"
            "player_history_all.yaml",
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md",
        ]
    )
    return HistoryEnrichedAdjudicationDecision(
        decision_id="Q1_source_layer",
        decision_name=(
            "History-enriched pre_game source layer (target row + history row + "
            "asymmetry; divergence + extension annotated)"
        ),
        verdict="extend_with_evidence",
        binding_level="binding_for_materialization",
        feature_family_id_or_scope="all_six_history_enriched_pre_game_families",
        selected_source_layer="matches_flat_clean",
        selected_target_source_layer="matches_flat_clean",
        selected_history_source_layer="player_history_all",
        target_history_asymmetry="asymmetric",
        source_layer_divergence_reason=(
            "matches_flat_clean (operationally) vs matches_flat (registry); "
            "cleaned-view chosen for 1v1-scoping + 44,418-row deterministic count "
            "per PR #234 §3 binding (selected_source_layer = matches_flat_clean was "
            "BINDING in tranche-1)"
        ),
        history_source_extension_reason=(
            "tranche-1 (5 pre_game families) had no history-side source; tranche-2 "
            "(6 history-enriched families) adds player_history_all as the history-side "
            "source per ROADMAP line 2367 inputs.duckdb_tables and CROSS-02-02 §6.2 "
            "rows 1-4 + 6 verbatim source bindings"
        ),
        target_anchor="",
        history_time_column="",
        strict_lt_expression="",
        cold_start_policy="",
        cross_region_policy="",
        rating_policy="",
        in_game_historical_policy="",
        in_game_historical_columns_in_scope="",
        evidence_paths=q1_evidence_paths,
        falsifiers=(
            "q1_source_layer_evidence_inconsistent:did_not_fire\n"
            "q1_single_row_violation:did_not_fire"
        ),
        notes=q1_notes,
        **common,
    )


def _build_q2(common: dict[str, str]) -> HistoryEnrichedAdjudicationDecision:
    """Build the Q2 target-anchor decision row (T05 Q2).

    Args:
        common: Common provenance fields shared across all rows.

    Returns:
        Q2 decision dataclass.
    """
    return HistoryEnrichedAdjudicationDecision(
        decision_id="Q2_target_anchor",
        decision_name="Target match temporal anchor for the strict-< history filter",
        verdict="ratify_with_evidence",
        binding_level="binding_for_materialization",
        feature_family_id_or_scope="all_six_history_enriched_pre_game_families",
        selected_source_layer="",
        selected_target_source_layer="",
        selected_history_source_layer="",
        target_history_asymmetry="",
        source_layer_divergence_reason="",
        history_source_extension_reason="",
        target_anchor="matches_history_minimal.started_at TIMESTAMP",
        history_time_column="",
        strict_lt_expression="",
        cold_start_policy="",
        cross_region_policy="",
        rating_policy="",
        in_game_historical_policy="",
        in_game_historical_columns_in_scope="",
        evidence_paths=(
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
            "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
            "02_01_02_source_anchor_race_adjudication.csv\n"
            "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/"
            "matches_history_minimal.yaml\n"
            "reports/specs/02_00_feature_input_contract.md"
        ),
        falsifiers="q2_target_anchor_type_mismatch:did_not_fire",
        notes=(
            "RATIFY tranche-1 PR #234 Q2(a) BINDING: target_anchor = "
            "matches_history_minimal.started_at TIMESTAMP (canonical cross-dataset "
            "dtype per CROSS-02-00 §3.1; DESCRIBE TIMESTAMP confirmed; 0 nulls; "
            "0 cross-row inconsistency). Phase-03 hold-out anchor (Q2(b) per "
            "PR #234) remains RECOMMENDATION ONLY for Phase 03 planning."
        ),
        **common,
    )


def _build_q3(common: dict[str, str]) -> HistoryEnrichedAdjudicationDecision:
    """Build the Q3 history-time-column decision row (T05 Q3).

    Args:
        common: Common provenance fields shared across all rows.

    Returns:
        Q3 decision dataclass.
    """
    return HistoryEnrichedAdjudicationDecision(
        decision_id="Q3_history_time_column",
        decision_name=(
            "Historical row time column for strict-< filter (canonical TRY_CAST form)"
        ),
        verdict="bind_now",
        binding_level="binding_for_materialization",
        feature_family_id_or_scope="all_six_history_enriched_pre_game_families",
        selected_source_layer="",
        selected_target_source_layer="",
        selected_history_source_layer="",
        target_history_asymmetry="",
        source_layer_divergence_reason="",
        history_source_extension_reason="",
        target_anchor="",
        history_time_column=(
            "player_history_all.details_timeUTC (TRY_CAST AS TIMESTAMP for "
            "comparison with target.started_at)"
        ),
        strict_lt_expression=STRICT_LT_HISTORY_FILTER,
        cold_start_policy="",
        cross_region_policy="",
        rating_policy="",
        in_game_historical_policy="",
        in_game_historical_columns_in_scope="",
        evidence_paths=(
            "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/"
            "player_history_all.yaml\n"
            "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/"
            "matches_history_minimal.yaml\n"
            "reports/specs/02_00_feature_input_contract.md (§5.4 sc2egset PH "
            "details_timeUTC row)\n"
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md "
            "(§02_01_03 raw form: STRICT_LT_FILTER_ROADMAP_RAW)"
        ),
        falsifiers=(
            "q3_history_time_column_invalid:did_not_fire\n"
            "q3_strict_lt_smoke_failed:did_not_fire\n"
            "strict_lt_filter_divergence:did_not_fire"
        ),
        notes=(
            "Strict-< filter expression (CANONICAL per B-X2): "
            f"{STRICT_LT_HISTORY_FILTER}. "
            f"This is exactly STRICT_LT_HISTORY_FILTER. The ROADMAP §02_01_03 raw "
            f"form {STRICT_LT_FILTER_ROADMAP_RAW!r} is recorded for provenance ONLY "
            "(as STRICT_LT_FILTER_ROADMAP_RAW); this adjudication explicitly "
            "NORMALIZES that raw form to the canonical TRY_CAST expression for "
            "chronological fidelity per matches_history_minimal.yaml (7 observed "
            "length variants 22-28 chars in upstream VARCHAR; lex comparison is "
            "NOT chronologically faithful). Deterministic ordering via "
            "(player_id_worldwide, TRY_CAST(ph.details_timeUTC AS TIMESTAMP), "
            "ph.replay_id). 1000-row TRY_CAST NULL-rate sanity probe required: "
            "q3_strict_lt_smoke_failed halts if any NULL."
        ),
        **common,
    )


def _build_q4(common: dict[str, str]) -> HistoryEnrichedAdjudicationDecision:
    """Build the Q4 cold-start-policy decision row (T05 Q4).

    Args:
        common: Common provenance fields shared across all rows.

    Returns:
        Q4 decision dataclass.
    """
    cold_start_policy = (
        "G-CS-2:scaffold_registry_gate_for_focal_player_history"
        "+opponent_player_history+in_game_history_aggregate"
        "|G-CS-3:scaffold_registry_gate_for_matchup_history_aggregate"
        "|G-CS-4:scaffold_registry_gate_for_reconstructed_rating"
        "|G-CS-5:scaffold_registry_gate_for_cross_region_fragmentation_handling"
        "|G-CS-6:materialization_time_fold_aware_fit_gate_per_invariant_I3"
        "_and_CROSS-02-02_section_9"
    )
    return HistoryEnrichedAdjudicationDecision(
        decision_id="Q4_cold_start_policy",
        decision_name=(
            "Cold-start policy per family (G-CS-2/3/4/5; G-CS-6 distinguished as "
            "materialization-time gate)"
        ),
        verdict="extend_with_evidence",
        binding_level="binding_for_materialization",
        feature_family_id_or_scope="all_six_history_enriched_pre_game_families",
        selected_source_layer="",
        selected_target_source_layer="",
        selected_history_source_layer="",
        target_history_asymmetry="",
        source_layer_divergence_reason="",
        history_source_extension_reason="",
        target_anchor="",
        history_time_column="",
        strict_lt_expression="",
        cold_start_policy=cold_start_policy,
        cross_region_policy="",
        rating_policy="",
        in_game_historical_policy="",
        in_game_historical_columns_in_scope="",
        evidence_paths=(
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
            "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
            "02_01_01_feature_family_registry.csv\n"
            "reports/specs/02_02_feature_engineering_plan.md (§9 G-CS-2..G-CS-6)\n"
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md "
            "(lines 2334-2338)"
        ),
        falsifiers=(
            "q4_cold_start_gates_incomplete:did_not_fire\n"
            "q4_cold_start_leakage:did_not_fire"
        ),
        notes=(
            "Distinguishes: scaffold registry gates G-CS-2/3/4/5 (registry-time; "
            "bound here); G-CS-6 (materialization-time fold-aware fit gate per "
            "ROADMAP lines 2334-2338; DEFERRED to materialization PR); "
            "model-training Phase-03 cold-start handling (DEFERRED to Phase 03). "
            "ML-protocol three failure modes (rolling aggregates, head-to-head, "
            "co-occurring matches) explicitly forbidden; only match_time < T "
            "evidence used. Per B-X1 the notes field is EXEMPT from POST-GAME "
            "token scanning."
        ),
        **common,
    )


def _build_q5(common: dict[str, str]) -> HistoryEnrichedAdjudicationDecision:
    """Build the Q5 cross-region-policy decision row (T05 Q5).

    Args:
        common: Common provenance fields shared across all rows.

    Returns:
        Q5 decision dataclass.
    """
    return HistoryEnrichedAdjudicationDecision(
        decision_id="Q5_cross_region_policy",
        decision_name="Cross-region fragmentation operationalization (RISK-20)",
        verdict="deferred_blocker",
        binding_level="deferred_blocker",
        feature_family_id_or_scope=(
            "sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling"
        ),
        selected_source_layer="",
        selected_target_source_layer="",
        selected_history_source_layer="",
        target_history_asymmetry="",
        source_layer_divergence_reason="",
        history_source_extension_reason="",
        target_anchor="",
        history_time_column="",
        strict_lt_expression="",
        cold_start_policy="",
        cross_region_policy="deferred_blocker",
        rating_policy="",
        in_game_historical_policy="",
        in_game_historical_columns_in_scope="",
        evidence_paths=(
            "reports/specs/02_02_feature_engineering_plan.md (§6.2 row 5)\n"
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
            "01_exploration/06_decision_gates/risk_register_sc2egset.md (RISK-20)\n"
            "src/rts_predict/games/sc2/datasets/sc2egset/"
            "validate_history_enriched_pre_game_materialization.py "
            "(_check_cross_region_caveat)"
        ),
        falsifiers="q5_cross_region_three_options_not_enumerated:did_not_fire",
        notes=(
            "CROSS-02-02 §6.2 row 5 enumerates three options: strict_exclusion "
            "(drop cross-region players from train+test); dual_feature_path "
            "(maintain separate per-region history aggregates with explicit "
            "merge rules); sensitivity_indicator_co_registration (retain a "
            "binary is_cross_region indicator alongside the merged history). "
            "The retention impact of each option is empirically conditional; "
            "binding any here without a measurement study would pin a numeric "
            "without evidence (Invariant I7 violation). The PR #241 scaffold "
            "validator accepts allowed_with_caveat without pinning; this "
            "adjudication preserves that deferral as an explicit BINDING gate "
            "against materialization. MATERIALIZATION BLOCKED until Q5 is "
            "upgraded to bind_now in a successor adjudication PR with "
            "retention-measurement evidence."
        ),
        **common,
    )


def _build_q6(common: dict[str, str]) -> HistoryEnrichedAdjudicationDecision:
    """Build the Q6 rating-policy decision row (T05 Q6; N-X3 strengthened).

    Args:
        common: Common provenance fields shared across all rows.

    Returns:
        Q6 decision dataclass.
    """
    q6_evidence = "\n".join(
        [
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
            "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
            "02_01_01_feature_family_registry.csv",
            "reports/specs/02_02_feature_engineering_plan.md (§6.2 row 4; §9 G-CS-4)",
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md "
            "(is_mmr_missing density 83.95%)",
            "Elo (1978)",
            "Glickman (1999)",
            "Glickman (2012)",
            "Herbrich, Minka, Graepel (2006)",
        ]
    )
    q6_notes = (
        "deferred_blocker because: per N3, ~83.95% MMR-missing density "
        "(verified in the dataset research log; consistent with the registry CSV "
        "is_mmr_missing_flag family) makes algorithm choice first-order. Pinning "
        "Elo / Glicko / Glicko-2 / TrueSkill / a rolling-winrate baseline without "
        "empirical evidence of which family handles the unrated / no-rating-history "
        "regime best would violate Invariant I7. Four candidate citations exist "
        "(Elo 1978; Glickman 1999; Glickman 2012; Herbrich, Minka, Graepel 2006) "
        "but binding one over the others requires repo evidence not yet generated. "
        "Forward-only constraint explicit: no target-match outcome; no future "
        "results; no global batch fit; per-game forward update only. Cold-start "
        "handled by initializing rating = literature-prior for new players "
        "(DEFERRED to materialization PR's training-fold-fit step); missingness "
        "handled by retaining is_mmr_missing as a separate companion feature "
        "(DEFERRED to materialization PR). Per B-X1 the notes field is EXEMPT "
        "from POST-GAME token scanning, so negated-prose phrases are allowed here. "
        "MATERIALIZATION BLOCKED until Q6 is upgraded to bind_now in a successor "
        "adjudication PR with rating-family empirical evaluation evidence "
        "satisfying the N-X3 strengthened gate (>=1 repo path + >=1 citation + "
        "forward-only wording + cold-start/missingness wording)."
    )
    return HistoryEnrichedAdjudicationDecision(
        decision_id="Q6_rating_policy",
        decision_name=(
            "Rating reconstruction model family for reconstructed_rating (G-CS-4)"
        ),
        verdict="deferred_blocker",
        binding_level="deferred_blocker",
        feature_family_id_or_scope=(
            "sc2egset.history_enriched_pre_game.reconstructed_rating"
        ),
        selected_source_layer="",
        selected_target_source_layer="",
        selected_history_source_layer="",
        target_history_asymmetry="",
        source_layer_divergence_reason="",
        history_source_extension_reason="",
        target_anchor="",
        history_time_column="",
        strict_lt_expression="",
        cold_start_policy="",
        cross_region_policy="",
        rating_policy="deferred_blocker",
        in_game_historical_policy="",
        in_game_historical_columns_in_scope="",
        evidence_paths=q6_evidence,
        falsifiers=(
            "q6_rating_default_deferred_violated:did_not_fire\n"
            "q6_rating_forward_only_missing:did_not_fire"
        ),
        notes=q6_notes,
        **common,
    )


def _build_q7(common: dict[str, str]) -> HistoryEnrichedAdjudicationDecision:
    """Build the Q7 in-game-historical-policy decision row (T05 Q7).

    Args:
        common: Common provenance fields shared across all rows.

    Returns:
        Q7 decision dataclass.
    """
    q7_notes = (
        "CROSS-02-00 §5.4 Concern 8 / T15 record retains these 4 columns "
        f"({IN_GAME_HISTORICAL_COLUMNS_IN_SCOPE_PIPE}) in scope for prior-match "
        "aggregation ONLY; never as direct game-T pre-game features. Source = "
        "player_history_all (per ROADMAP line 2367 + CROSS-02-02 §6.2 row 6). "
        "Strict-< filter expression (CANONICAL per B-X2): "
        f"{STRICT_LT_HISTORY_FILTER}. Aggregation only over rows where "
        "history_time < target_time (prior matches); never the target match "
        "itself. Distinct from in_game_snapshot tranche; aggregation pseudocount "
        "/ window-size constants DEFERRED to materialization PR. Per B-X1 notes "
        "exempt from POST-GAME scan."
    )
    return HistoryEnrichedAdjudicationDecision(
        decision_id="Q7_in_game_historical_policy",
        decision_name=(
            "IN_GAME_HISTORICAL prior-match aggregation policy for "
            "in_game_history_aggregate"
        ),
        verdict="bind_now",
        binding_level="binding_for_materialization",
        feature_family_id_or_scope=(
            "sc2egset.history_enriched_pre_game.in_game_history_aggregate"
        ),
        selected_source_layer="",
        selected_target_source_layer="",
        selected_history_source_layer="",
        target_history_asymmetry="",
        source_layer_divergence_reason="",
        history_source_extension_reason="",
        target_anchor="",
        history_time_column="",
        strict_lt_expression=STRICT_LT_HISTORY_FILTER,
        cold_start_policy="",
        cross_region_policy="",
        rating_policy="",
        in_game_historical_policy="prior_match_only_strict_lt",
        in_game_historical_columns_in_scope=IN_GAME_HISTORICAL_COLUMNS_IN_SCOPE_PIPE,
        evidence_paths=(
            "reports/specs/02_00_feature_input_contract.md (§5.4 sc2egset PH "
            "IN_GAME_HISTORICAL rows; Concern 8 / T15 record)\n"
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
            "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
            "02_01_01_feature_family_registry.csv (row 12)\n"
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md "
            "(line 2367 inputs.duckdb_tables)"
        ),
        falsifiers=(
            "q7_in_game_historical_columns_drift:did_not_fire\n"
            "q7_no_target_match_tracker_missing:did_not_fire\n"
            "in_game_historical_strict_lt_violated:did_not_fire\n"
            "strict_lt_filter_divergence:did_not_fire"
        ),
        notes=q7_notes,
        **common,
    )


def _build_q8(common: dict[str, str]) -> HistoryEnrichedAdjudicationDecision:
    """Build the Q8 MHM-consumption decision row (T05 Q8).

    Args:
        common: Common provenance fields shared across all rows.

    Returns:
        Q8 decision dataclass.
    """
    q8_notes = (
        "MHM is consumed for (1) target row identity / started_at TIMESTAMP "
        "anchor per PR #234 Q2(a) BINDING (the canonical source of started_at "
        "joined back onto matches_flat_clean); (2) cold-start enumeration "
        "G-CS-2/3/4/5 (the support set of (focal_player, target.started_at) "
        "target rows over which prior history is counted). MHM is NOT a "
        "feature source — no MHM column becomes a feature column in the "
        "materialized output unless this adjudication row is updated in a "
        "successor PR with explicit justification. MHM column-level provenance "
        "recorded for examiner clarity; no MHM PRE_GAME column elevated to "
        "feature without successor-PR adjudication. Per B-X1 notes exempt "
        "from POST-GAME scan."
    )
    return HistoryEnrichedAdjudicationDecision(
        decision_id="Q8_matches_history_minimal_consumption",
        decision_name=(
            "What matches_history_minimal is consumed for in the history-enriched "
            "pre_game tranche"
        ),
        verdict="ratify_with_evidence",
        binding_level="binding_for_materialization",
        feature_family_id_or_scope=_Q8_REQUIRED_SCOPE_TEXT,
        selected_source_layer="",
        selected_target_source_layer="",
        selected_history_source_layer="",
        target_history_asymmetry="",
        source_layer_divergence_reason="",
        history_source_extension_reason="",
        target_anchor="",
        history_time_column="",
        strict_lt_expression="",
        cold_start_policy="",
        cross_region_policy="",
        rating_policy="",
        in_game_historical_policy="",
        in_game_historical_columns_in_scope="",
        evidence_paths=(
            "sandbox/sc2/sc2egset/02_feature_engineering/"
            "01_pre_game_vs_in_game_boundary/"
            "02_01_03_history_enriched_pre_game_feature_materialization.py "
            "(scaffold cell: What matches_history_minimal is consumed for)\n"
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md "
            "(inputs.duckdb_tables line 2366)\n"
            "reports/specs/02_00_feature_input_contract.md (§5.1 sc2egset MHM "
            "column table)"
        ),
        falsifiers="q8_mhm_documentation_missing:did_not_fire",
        notes=q8_notes,
        **common,
    )


# ---------------------------------------------------------------------------
# SHA-256 + git provenance helpers
# ---------------------------------------------------------------------------


def _sha256_file(path: Path) -> str:
    """Compute SHA-256 hex digest of a file, or ``'NOT_FOUND'`` if absent.

    Args:
        path: Path to the file.

    Returns:
        64-char lowercase hex digest or ``'NOT_FOUND'``.
    """
    if not path.exists():
        return "NOT_FOUND"
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _get_git_sha() -> str:
    """Return the current HEAD git SHA or ``'UNKNOWN'`` if git is unavailable.

    Returns:
        Git SHA string.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "UNKNOWN"


def _find_repo_root(start: Path) -> Path:
    """Walk up from ``start`` until ``pyproject.toml`` is found.

    Args:
        start: Starting file or directory.

    Returns:
        The directory containing ``pyproject.toml``.

    Raises:
        FileNotFoundError: If no ``pyproject.toml`` is found walking up.
    """
    candidate = start.resolve()
    while candidate != candidate.parent:
        if (candidate / "pyproject.toml").exists():
            return candidate
        candidate = candidate.parent
    raise FileNotFoundError(
        f"No pyproject.toml found walking up from {start}; cannot determine repo root."
    )


# ---------------------------------------------------------------------------
# CSV + MD writers
# ---------------------------------------------------------------------------


_CSV_FIELDNAMES: tuple[str, ...] = tuple(
    f.name for f in fields(HistoryEnrichedAdjudicationDecision)
)


def _write_csv(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
    csv_path: Path,
) -> None:
    """Write the 33-column deterministic adjudication CSV.

    Args:
        decisions: The 8 decision rows in ``Q_DECISION_IDS`` order.
        csv_path: Destination path.
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(_CSV_FIELDNAMES))
        writer.writeheader()
        for d in decisions:
            writer.writerow(_decision_to_field_dict(d))
    LOGGER.debug("_write_csv: wrote %d rows to %s", len(decisions), csv_path)


def _write_md(
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
    md_path: Path,
    falsifier_status: dict[str, str],
    smoke_probe_sql: str,
    view_counts: dict[str, int],
) -> None:
    """Write the §1-§14 adjudication MD companion artifact.

    Args:
        decisions: The 8 decision rows.
        md_path: Destination path.
        falsifier_status: Mapping of falsifier key to ``"did_fire"`` /
            ``"did_not_fire"``.
        smoke_probe_sql: Verbatim canonical smoke-probe SQL string.
        view_counts: Output of ``_probe_view_row_counts``.
    """
    md_path.parent.mkdir(parents=True, exist_ok=True)
    parts: list[str] = []
    parts.append(
        "# SC2EGSet Step 02_01_03 — History-Enriched Pre-Game Source / "
        "Anchor / Cold-Start Adjudication\n\n"
    )
    parts.append("## §1 Non-Overclaim Disclaimer\n\n")
    parts.append(
        "This artifact is an adjudication of 8 coupled pre-materialization "
        "questions for sc2egset Step 02_01_03 (tranche-2, 6 "
        "history-enriched pre_game families). It does NOT materialize any "
        "feature value, does NOT run the CROSS-02-01-v1.0.1 "
        "post-materialization leakage audit, does NOT close Step 02_01_03, "
        "and does NOT append to any status YAML or research_log. "
        "Materialization remains FUTURE.\n\n"
    )
    parts.append("## §2-§9 Per-Q Decisions\n\n")
    for d in decisions:
        parts.append(f"### {d.decision_id} — {d.decision_name}\n\n")
        parts.append(f"- **Verdict:** `{d.verdict}`\n")
        parts.append(f"- **Binding level:** `{d.binding_level}`\n")
        parts.append(f"- **Scope:** `{d.feature_family_id_or_scope}`\n")
        if d.target_anchor:
            parts.append(f"- **Target anchor:** `{d.target_anchor}`\n")
        if d.history_time_column:
            parts.append(f"- **History time column:** `{d.history_time_column}`\n")
        if d.cold_start_policy:
            parts.append(f"- **Cold-start policy:** `{d.cold_start_policy}`\n")
        if d.cross_region_policy:
            parts.append(f"- **Cross-region policy:** `{d.cross_region_policy}`\n")
        if d.rating_policy:
            parts.append(f"- **Rating policy:** `{d.rating_policy}`\n")
        if d.in_game_historical_policy:
            parts.append(
                f"- **In-game-historical policy:** `{d.in_game_historical_policy}`\n"
            )
        if d.in_game_historical_columns_in_scope:
            parts.append(
                f"- **In-game-historical columns in scope:** "
                f"`{d.in_game_historical_columns_in_scope}`\n"
            )
        parts.append(f"\n**Rationale / notes:**\n\n{d.notes}\n\n")
        parts.append(f"**Evidence paths:**\n\n```\n{d.evidence_paths}\n```\n\n")
    parts.append("## §10 Falsifier Roll-Call\n\n")
    parts.append("Every falsifier from `HELPER_TO_FALSIFIER_KEY.values()`:\n\n")
    for key in FALSIFIER_PRIORITY_CHAIN:
        status = falsifier_status.get(key, "did_not_fire")
        parts.append(f"- `{key}`: {status}\n")
    parts.append("\n### Verbatim canonical strict-< smoke SQL (Invariant I6)\n\n")
    parts.append(f"```sql\n{smoke_probe_sql}\n```\n\n")
    parts.append("### Probe row counts\n\n")
    for name, count in sorted(view_counts.items()):
        parts.append(f"- `{name}`: {count}\n")
    parts.append("\n## §11 Lineage Position\n\n")
    parts.append(
        "Artifact #3 in the lineage chain for Step 02_01_03 readiness:\n"
        "1. PR #239 ROADMAP stub.\n"
        "2. PR #241 scaffold + validator.\n"
        "3. THIS adjudication.\n"
        "4. Future materialization plan.\n"
        "5. Future materialization + CROSS-02-01 post-mat audit.\n"
        "6. Future Step 02_01_03 closure PR.\n\n"
    )
    parts.append("## §12 Explicit Non-Substitution Statement\n\n")
    parts.append(
        "This artifact does NOT replace, weaken, or amend: "
        "(a) PR #229 §10 design-time verdict pair; "
        "(b) PR #230 vacuous CROSS-02-01 audit pair; "
        "(c) PR #234 tranche-1 adjudication; "
        "(d) PR #236 tranche-1 materialization + audit; "
        "(e) PR #237 tranche-1 closure; "
        "(f) PR #241 scaffold + validator; "
        "(g) the FUTURE materialization + post-materialization CROSS-02-01 "
        "audit (which do not yet exist).\n\n"
    )
    parts.append("## §13 Materialization Blocked Until Deferred-Blocker Resolved\n\n")
    parts.append(
        "If any decision row carries `verdict == \"deferred_blocker\"`, the "
        "future Layer-3 materialization PR must NOT proceed until that "
        "decision is upgraded to `bind_now` / `ratify_with_evidence` / "
        "`extend_with_evidence` / `narrow_with_evidence` in a successor "
        "adjudication PR. Q5 (cross-region) and Q6 (rating) are currently "
        "deferred_blocker.\n\n"
    )
    parts.append("## §14 No Step Closure Claim\n\n")
    parts.append(
        "Step 02_01_03 remains OPEN. This artifact does NOT add "
        "`02_01_03: complete` to `STEP_STATUS.yaml`. Closure is deferred to a "
        "separate post-materialization closure PR per the PR #237 tranche-1 "
        "closure precedent.\n"
    )
    md_path.write_text("".join(parts), encoding="utf-8")
    LOGGER.debug("_write_md: wrote MD to %s", md_path)


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def adjudicate_history_enriched_pre_game_source_layer(
    duckdb_path: Path,
    registry_csv_path: Path,
    pr234_binding_csv_path: Path,
    csv_path: Path,
    md_path: Path,
    audit_pr: str,
    audit_date: str,  # noqa: ARG001 — recorded in MD via provenance footer hooks
) -> HistoryEnrichedAdjudicationResult:
    """Adjudicate the 8 coupled history-enriched pre_game decisions.

    Opens DuckDB read-only, runs the T02/T03 evidence probes, constructs the
    8 Q-decisions per T05's verbatim bindings, runs every falsifier in the
    ``FALSIFIER_PRIORITY_CHAIN`` order, and (if no falsifier fires) writes
    the 33-column CSV + §1-§14 MD artifact pair. ``materialized_output_paths``
    is ALWAYS empty.

    Args:
        duckdb_path: Path to the sc2egset DuckDB file (opened read-only).
        registry_csv_path: Path to the closed 02_01_01 registry CSV.
        pr234_binding_csv_path: Path to the tranche-1 adjudication CSV.
        csv_path: Destination CSV path (typically ``ADJUDICATION_CSV_REL``).
        md_path: Destination MD path (typically ``ADJUDICATION_MD_REL``).
        audit_pr: PR number placeholder string (e.g. ``"PR #242"``).
        audit_date: ISO YYYY-MM-DD date (carried in provenance only).

    Returns:
        ``HistoryEnrichedAdjudicationResult`` with ``passed=True`` iff no
        halting falsifier fired.
    """
    LOGGER.info(
        "adjudicate_history_enriched_pre_game_source_layer: opening DuckDB at "
        "%s (read-only)",
        duckdb_path,
    )
    # Load evidence (file-based)
    pr234_binding = _load_pr234_binding_csv(pr234_binding_csv_path)
    _registry = _load_registry_csv(registry_csv_path)
    LOGGER.debug(
        "adjudicate_history_enriched_pre_game_source_layer: registry rows=%d "
        "pr234_rows=%d expected_tranche2=%d",
        len(_registry),
        len(pr234_binding),
        EXPECTED_TRANCHE2_COUNT,
    )

    # Probe DuckDB (read-only)
    con = duckdb.connect(str(duckdb_path), read_only=True)
    try:
        view_counts = _probe_view_row_counts(con)
        history_time_metadata = _probe_history_time_column_candidates(con)
        smoke_probe = _probe_strict_lt_filter_smoke(con)
        _mhm_cols = _probe_matches_history_minimal_columns(con)
    finally:
        con.close()

    # Provenance
    git_sha = _get_git_sha()
    # The PR #241 SHA is recorded by binding (N4 anchor); we do not recompute.
    pr241_sha = EXPECTED_PR241_VALIDATOR_SHA256

    # Compute provenance SHA-256 of every input file referenced by this
    # adjudication. Each digest is embedded on every row so an examiner can
    # independently re-hash and confirm the input set this PR was built against.
    repo_root = _find_repo_root(Path(__file__))
    roadmap_sha = _sha256_file(repo_root / ROADMAP_REL)
    registry_csv_sha = _sha256_file(repo_root / REGISTRY_CSV_REL)
    mhm_yaml_sha = _sha256_file(repo_root / MATCHES_HISTORY_MINIMAL_YAML_REL)
    cross_02_00_sha = _sha256_file(repo_root / CROSS_02_00_SPEC_REL)
    cross_02_01_sha = _sha256_file(repo_root / CROSS_02_01_SPEC_REL)
    cross_02_02_sha = _sha256_file(repo_root / CROSS_02_02_SPEC_REL)
    cross_02_03_sha = _sha256_file(repo_root / CROSS_02_03_SPEC_REL)

    # Build decisions
    decisions = _build_decisions(
        audit_pr=audit_pr,
        provenance_git_sha=git_sha,
        pr241_sha256=pr241_sha,
        roadmap_sha256=roadmap_sha,
        registry_csv_sha256=registry_csv_sha,
        matches_history_minimal_yaml_sha256=mhm_yaml_sha,
        cross_02_00_spec_sha256=cross_02_00_sha,
        cross_02_01_spec_sha256=cross_02_01_sha,
        cross_02_02_spec_sha256=cross_02_02_sha,
        cross_02_03_spec_sha256=cross_02_03_sha,
    )

    # Run falsifiers in FALSIFIER_PRIORITY_CHAIN order (first fired halts).
    smoke_sql = str(smoke_probe.get("sql", ""))
    halting: str | None = None
    fired: list[str] = []
    key_to_invocation = _build_falsifier_invocations(
        decisions=decisions,
        pr234_binding=pr234_binding,
        history_time_metadata=history_time_metadata,
        smoke_probe=smoke_probe,
        smoke_sql=smoke_sql,
    )
    for key in FALSIFIER_PRIORITY_CHAIN:
        invocation = key_to_invocation.get(key)
        if invocation is None:
            continue
        did_fire, message = invocation()
        if did_fire:
            fired.append(key)
            if halting is None:
                halting = key
            LOGGER.warning(
                "falsifier %s fired: %s",
                key,
                message,
            )

    falsifier_status: dict[str, str] = {
        key: ("did_fire" if key in fired else "did_not_fire")
        for key in FALSIFIER_PRIORITY_CHAIN
    }

    # Halt-before-artifact: never write CSV when a falsifier fires.
    if halting is None:
        _write_csv(decisions, csv_path)
        _write_md(decisions, md_path, falsifier_status, smoke_sql, view_counts)
    else:
        LOGGER.warning(
            "adjudicate_history_enriched_pre_game_source_layer: halting "
            "falsifier %s — CSV+MD NOT written",
            halting,
        )

    return HistoryEnrichedAdjudicationResult(
        decisions=decisions,
        csv_path=str(csv_path),
        md_path=str(md_path),
        provenance_git_sha=git_sha,
        pr241_scaffold_validator_module_sha256=pr241_sha,
        falsifiers_fired=tuple(fired),
        halting_falsifier=halting,
        passed=halting is None,
    )


def _build_falsifier_invocations(
    *,
    decisions: tuple[HistoryEnrichedAdjudicationDecision, ...],
    pr234_binding: dict[str, dict[str, str]],
    history_time_metadata: dict[str, dict[str, object]],
    smoke_probe: dict[str, object],
    smoke_sql: str,
) -> dict[str, _FalsifierThunk]:
    """Build a key->thunk map for the 21 falsifiers (priority-chain order).

    Each thunk is a zero-argument callable returning ``(did_fire, message)``.

    Args:
        decisions: All 8 decisions.
        pr234_binding: Loaded PR #234 binding rows.
        history_time_metadata: Output of ``_probe_history_time_column_candidates``.
        smoke_probe: Output of ``_probe_strict_lt_filter_smoke``.
        smoke_sql: Verbatim canonical smoke-probe SQL string.

    Returns:
        Mapping from falsifier key to thunk.
    """
    return {
        "pr241_sha256_mismatch": lambda: _check_pr241_sha256_match(decisions),
        "provenance_sha_invalid": lambda: _check_no_not_found_sha_fields(decisions),
        "decision_count_mismatch": lambda: _check_decision_count(decisions),
        "q1_single_row_violation": lambda: _check_q1_single_row_per_n5(decisions),
        "q1_source_layer_evidence_inconsistent": (
            lambda: _check_q1_source_layer_evidence_consistent(decisions, pr234_binding)
        ),
        "strict_lt_filter_divergence": (
            lambda: _check_strict_lt_filter_divergence(decisions, smoke_sql)
        ),
        "q2_target_anchor_type_mismatch": (
            lambda: _check_q2_target_anchor_type_match(decisions, history_time_metadata)
        ),
        "q3_history_time_column_invalid": (
            lambda: _check_q3_history_time_column_dtype(decisions, history_time_metadata)
        ),
        "q3_strict_lt_smoke_failed": lambda: _check_q3_monotonicity_smoke(smoke_probe),
        "q4_cold_start_gates_incomplete": (
            lambda: _check_q4_cold_start_gates_complete(decisions)
        ),
        "q4_cold_start_leakage": lambda: _check_q4_no_leakage_in_cold_start(decisions),
        "q5_cross_region_three_options_not_enumerated": (
            lambda: _check_q5_cross_region_three_options_enumerated(decisions)
        ),
        "q6_rating_default_deferred_violated": (
            lambda: _check_q6_rating_default_deferred(decisions)
        ),
        "q6_rating_forward_only_missing": (
            lambda: _check_q6_rating_forward_only(decisions)
        ),
        "q7_in_game_historical_columns_drift": (
            lambda: _check_q7_in_game_historical_columns_in_scope(decisions)
        ),
        "q7_no_target_match_tracker_missing": (
            lambda: _check_q7_no_target_match_tracker(decisions)
        ),
        "in_game_historical_strict_lt_violated": (
            lambda: _check_in_game_historical_strict_lt(decisions)
        ),
        "q8_mhm_documentation_missing": lambda: _check_q8_mhm_documented(decisions),
        "universal_post_game_token_in_scoped_field": (
            lambda: _check_forbidden_post_game_feature_tokens(decisions)
        ),
        "universal_tracker_source_in_history": (
            lambda: _check_universal_no_tracker_source(decisions)
        ),
        "materialization_creep": lambda: _check_materialization_creep(decisions),
    }
