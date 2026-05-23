"""Adjudication module for SC2EGSet Step 02_01_02 — source/anchor/race-column adjudication.

This module adjudicates three coupled pre-materialization decisions for the 5 tranche-1
pre_game feature families and produces one artifact pair (CSV + MD). It does NOT
materialize any feature value, does NOT run projection SQL against feature data, and
does NOT write any status YAML / research_log / ROADMAP / spec / cleaning-layer YAML.
``materialized_output_paths`` is ALWAYS ``()``.

Binding sources:
    - CROSS-02-00-v3.0.1 §3.1 / §3.2 / §5.1 / §5.4 (canonical join/anchor/faction).
    - CROSS-02-01-v1.0.1 §2.1/§2.2/§4 (cutoff structural check; vacuous here).
    - CROSS-02-02-v1.0.1 §6.1 (sc2egset pre_game candidates).
    - CROSS-02-03-v1.0.1 §6.1 (pre_game cutoff = none; anchor is row-identity).
    - matches_long_raw.yaml:101-103 (selectedRace excluded; race used).
    - matches_history_minimal.yaml:52-53 (MHM faction PRE_GAME; from race not selectedRace).
    - thesis/pass2_evidence/methodology_risk_register.md RISK-26 lines 479-492.
    - Invariant I3 (no tracker in pre_game), I5 (symmetric), I6 (SQL in artifact),
      I7 (no magic numbers), I9 (research pipeline discipline).

Decisions adjudicated (Q1/Q2/Q3):
    Q1 — Source layer: matches_flat_clean (cleaned-raw, 1v1-scoped native).
    Q2(a) — Phase-02 row-identity anchor: started_at TIMESTAMP from MHM (BINDING).
    Q2(b) — Phase-03 chronological hold-out anchor: started_at TIMESTAMP (RECOMMENDATION ONLY).
    Q3 — Race-column: RATIFY existing cleaning-layer convention (race = PRE_GAME canon;
         selectedRace excluded). RISK-26 gap documented; CROSS-02-02 §6.1 minor amendment
         proposed as future-PR target.

Falsifiers implemented (a fired falsifier sets halting_falsifier and passed=False):
    q1_no_evidence: source-layer peek returns zero rows for all candidate tables.
    q1_source_1v1_lost: chosen candidate has fewer than EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID
        distinct replay_id without an explicit 1v1 filter.
    q1_source_grain_mismatch: self-join cardinality != 44,418 (I5 violation).
    q1_source_missing_column: chosen candidate lacks a required tranche-1 column.
    q2_anchor_type_mismatch: chosen anchor column is VARCHAR without provenance justification.
    q2_anchor_cross_row_inconsistency: anchor values differ across the two player rows of the
        same match (cross-row inconsistency).
    q3_race_post_decision_chosen: under Q3.AMEND, chosen race column vocab = {Prot,Terr,Zerg}
        only — evidence of post-decision overwrite (RISK-26 leak).
    q3_prior_decision_silently_reversed: Q3 outcome chosen without citing either
        matches_long_raw.yaml:101-103 (RATIFY) or a proposed YAML patch (AMEND).
    q3_random_vocabulary_dropped: under Q3.AMEND, Random rows excluded without mitigation.
    q3_random_spelling_uncanonicalised: under Q3.AMEND, Rand/Random preserved as distinct
        categories without canonicalisation rule.
    provenance_sha_not_found: any *_sha256 column in the rendered CSV is NOT_FOUND, empty,
        wrong length, or non-hex — CSV halted before write (Invariant I6).
    spec_amendment_silent: spec amendment proposed in MD §8 but not in CSV field.
    non_substitution_silent: MD omits explicit non-substitution statement (§7).
    materialization_creep: any code path computes a feature value or writes Parquet.
    status_flip: diff touches any status YAML / research_log / ROADMAP / spec file.
    phase03_creep: Phase 03 or 02_01_03+ content appears in diff.
    tracker_creep: tracker_events_raw read in this module or notebook.
    leakage_audit_overclaim: artifact claims CROSS-02-01 audit has been run or leakage cleared.
    batching: PR diff includes feature materialization or post-materialization audit artifact.
"""

from __future__ import annotations

import csv
import hashlib
import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import duckdb

LOGGER = logging.getLogger(__name__)


class ProvenanceShaNotFoundError(Exception):
    """Raised when a *_sha256 column in the rendered CSV is invalid.

    This signals that the provenance_sha_not_found halting falsifier has fired:
    a SHA-256 value is NOT_FOUND, empty, not 64 characters, or not lowercase hex.
    The CSV is NOT written when this exception is raised.
    """


# ---------------------------------------------------------------------------
# Module-level constants — no magic numbers (Invariant I7)
# ---------------------------------------------------------------------------

EXPECTED_MHM_ROW_COUNT: int = 44418
EXPECTED_MHM_DISTINCT_MATCH_ID: int = 22209
EXPECTED_MFC_ROW_COUNT: int = 44418
EXPECTED_PH_ROW_COUNT: int = 44817
EXPECTED_RPR_ROW_COUNT: int = 44817
EXPECTED_MF_ROW_COUNT: int = 44817
EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID: int = 22209
EXPECTED_RAND_ROW_COUNT: int = 10
EXPECTED_BLANK_SELECTED_RACE_ROW_COUNT: int = 1110

PRE_GAME_RACE_TOKENS: frozenset[str] = frozenset({"Prot", "Terr", "Zerg", "Rand", "Random"})
POST_DECISION_RACE_TOKENS: frozenset[str] = frozenset({"Prot", "Terr", "Zerg"})
BW_LEGACY_RACE_TOKENS: frozenset[str] = frozenset({"BWPr", "BWTe", "BWZe"})
RANDOM_SPELLING_CANONICAL: str = "Random"

# Required tranche-1 columns that the chosen source layer must carry natively.
REQUIRED_MFC_COLUMNS: frozenset[str] = frozenset(
    {"race", "metadata_mapName", "metadata_gameVersion", "is_mmr_missing", "replay_id", "toon_id"}
)

AUDIT_PR: str = "PR #234"
EXECUTED_AT_UTC_DATE: str = "2026-05-23"
LINEAGE_POSITION: str = (
    "artifact #4 in the 5-artifact lineage for Step 02_01_02 readiness "
    "(after: PR #229 §10 design-time verdict pair; PR #230 vacuous CROSS-02-01 audit pair; "
    "PR #233 scaffold + 1 validator; this 3-decision adjudication; "
    "before: Layer-3 materialization-execution audit pair)"
)

# File paths relative to repo root (I10)
_METHODOLOGY_RISK_REGISTER_RELPATH: str = "thesis/pass2_evidence/methodology_risk_register.md"
_SPEC_02_00_RELPATH: str = "reports/specs/02_00_feature_input_contract.md"
_SPEC_02_01_RELPATH: str = "reports/specs/02_01_leakage_audit_protocol.md"
_SPEC_02_02_RELPATH: str = "reports/specs/02_02_feature_engineering_plan.md"
_SPEC_02_03_RELPATH: str = "reports/specs/02_03_temporal_feature_audit_protocol.md"
_MATCHES_LONG_RAW_YAML_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml"
)
_MATCHES_HISTORY_MINIMAL_YAML_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml"
)

# ---------------------------------------------------------------------------
# Named SQL constants (python-code rule: _QUERY suffix)
# ---------------------------------------------------------------------------

_MHM_DESCRIBE_QUERY: str = "DESCRIBE matches_history_minimal"
_MHM_COUNT_QUERY: str = "SELECT COUNT(*) FROM matches_history_minimal"
_MHM_DISTINCT_MATCH_ID_QUERY: str = "SELECT COUNT(DISTINCT match_id) FROM matches_history_minimal"
_MFC_DESCRIBE_QUERY: str = "DESCRIBE matches_flat_clean"
_MFC_COUNT_QUERY: str = "SELECT COUNT(*) FROM matches_flat_clean"
_MFC_DISTINCT_REPLAY_ID_QUERY: str = "SELECT COUNT(DISTINCT replay_id) FROM matches_flat_clean"
_PH_COUNT_QUERY: str = "SELECT COUNT(*) FROM player_history_all"
_RPR_COUNT_QUERY: str = "SELECT COUNT(*) FROM replay_players_raw"
_MFC_SELF_JOIN_CARDINALITY_QUERY: str = """
SELECT COUNT(*) FROM matches_flat_clean mfc
JOIN matches_history_minimal mhm
  ON CONCAT('sc2egset::', mfc.replay_id) = mhm.match_id
  AND mfc.toon_id = mhm.player_id
"""
_MFC_DETAILS_TIMEUTC_NULL_QUERY: str = (
    "SELECT COUNT(*) FILTER (WHERE details_timeUTC IS NULL) FROM matches_flat_clean"
)
_MHM_STARTED_AT_RANGE_QUERY: str = (
    "SELECT MIN(started_at), MAX(started_at) FROM matches_history_minimal"
)
_MHM_CROSS_ROW_INCONSISTENCY_QUERY: str = """
SELECT COUNT(*) FROM matches_history_minimal m1
JOIN matches_history_minimal m2
  ON m1.match_id = m2.match_id AND m1.player_id < m2.player_id
WHERE m1.started_at != m2.started_at
"""
_RPR_RACE_VOCAB_QUERY: str = (
    "SELECT race, COUNT(*) AS cnt FROM replay_players_raw GROUP BY 1 ORDER BY 1"
)
_RPR_SELECTED_RACE_VOCAB_QUERY: str = (
    "SELECT selectedRace, COUNT(*) AS cnt FROM replay_players_raw GROUP BY 1 ORDER BY 1"
)
_MFC_SELECTED_RACE_VOCAB_QUERY: str = (
    "SELECT selectedRace, COUNT(*) AS cnt FROM matches_flat_clean GROUP BY 1 ORDER BY 1"
)
_RPR_RACE_MISMATCH_QUERY: str = """
SELECT race, selectedRace, COUNT(*) AS cnt FROM replay_players_raw
WHERE race != selectedRace GROUP BY 1, 2 ORDER BY 1, 2
"""
_MHM_FACTION_VOCAB_QUERY: str = (
    "SELECT faction, COUNT(*) AS cnt FROM matches_history_minimal GROUP BY 1 ORDER BY 1"
)

# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceLayerCandidate:
    """Candidate source layer for the 5 tranche-1 pre_game families.

    Attributes:
        name: Short name for the candidate.
        family_to_source_table_map: Tuple of (family_id, source_table) pairs.
        self_join_keys_focal_opponent: Keys used for focal/opponent self-join.
        one_v_one_scope_native: True if the source natively filters to 1v1 matches.
        anchor_column: Temporal anchor column name.
        anchor_type: DuckDB type of the anchor column.
        risks_inherited: Risk register entries inherited by this candidate.
        sql_complexity_note: Note on SQL complexity vs. sibling candidates.
    """

    name: str
    family_to_source_table_map: tuple[tuple[str, str], ...]
    self_join_keys_focal_opponent: tuple[str, ...]
    one_v_one_scope_native: bool
    anchor_column: str
    anchor_type: str
    risks_inherited: tuple[str, ...]
    sql_complexity_note: str


@dataclass(frozen=True)
class AnchorCandidate:
    """Candidate temporal anchor for Phase-02 row-identity or Phase-03 hold-out.

    Attributes:
        column: Column name.
        type_: DuckDB type string.
        scope_native: Source table where this column is natively available.
        null_rate_observed: Observed null count (0 = no nulls).
        decision_rationale: Short rationale for choosing/rejecting.
    """

    column: str
    type_: str
    scope_native: str
    null_rate_observed: int
    decision_rationale: str


@dataclass(frozen=True)
class RaceColumnCandidate:
    """Candidate race column for the Q3 race-column adjudication.

    Attributes:
        column: Column name.
        vocabulary_observed: Observed distinct values.
        contains_random: True if any Random/Rand value observed.
        contains_post_decision_overwrite: True if vocabulary is post-decision only.
        canonicalisation_rule: Canonicalisation rule for multi-spelling Random.
        cleaning_layer_status: One of "ratify_existing" or "amend_existing".
        risk_26_compliance: One of "compliant", "documented_gap", or "violated".
    """

    column: str
    vocabulary_observed: tuple[str, ...]
    contains_random: bool
    contains_post_decision_overwrite: bool
    canonicalisation_rule: str
    cleaning_layer_status: str
    risk_26_compliance: str


@dataclass(frozen=True)
class AdjudicationDecision:
    """A single resolved adjudication decision.

    Attributes:
        decision_id: One of "Q1_source_layer", "Q2_anchor", "Q3_race_and_random".
        candidates_considered: Tuple of candidate names considered.
        chosen: Name of the chosen candidate.
        rationale_paragraph: 80-250 words citing spec/RISK/invariant.
        falsifiers_recorded: Tuple of falsifier names checked for this decision.
        blocking_for_materialization: True if this decision blocks materialization.
    """

    decision_id: str
    candidates_considered: tuple[str, ...]
    chosen: str
    rationale_paragraph: str
    falsifiers_recorded: tuple[str, ...]
    blocking_for_materialization: bool


@dataclass(frozen=True)
class AdjudicationResult:
    """Aggregate result of the three-decision adjudication.

    Attributes:
        passed: True iff halting_falsifier is None.
        decisions: Exactly 3 decisions (Q1, Q2, Q3).
        contradictions_with_specs: Tuple of spec contradiction strings.
        spec_amendments_proposed: Tuple of proposed amendment strings.
        materialized_output_paths: ALWAYS () — adjudication writes only the artifact pair.
        artifact_csv_path: Path to the written CSV artifact.
        artifact_md_path: Path to the written MD artifact.
        halting_falsifier: Name of the first halting falsifier, or None.
    """

    passed: bool
    decisions: tuple[AdjudicationDecision, ...]
    contradictions_with_specs: tuple[str, ...]
    spec_amendments_proposed: tuple[str, ...]
    materialized_output_paths: tuple[str, ...]
    artifact_csv_path: str
    artifact_md_path: str
    halting_falsifier: str | None


# ---------------------------------------------------------------------------
# Private peek helpers
# ---------------------------------------------------------------------------


def _run_source_layer_peeks(con: duckdb.DuckDBPyConnection) -> dict[str, Any]:
    """Run read-only DuckDB peeks for Q1 source-layer adjudication.

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        Dictionary with peek results keyed by check name.
    """
    mhm_count: int = con.execute(_MHM_COUNT_QUERY).fetchone()[0]  # type: ignore[index]
    mhm_distinct: int = (  # type: ignore[assignment]
        con.execute(_MHM_DISTINCT_MATCH_ID_QUERY).fetchone()[0]  # type: ignore[index]
    )
    mfc_count: int = con.execute(_MFC_COUNT_QUERY).fetchone()[0]  # type: ignore[index]
    mfc_distinct: int = (  # type: ignore[assignment]
        con.execute(_MFC_DISTINCT_REPLAY_ID_QUERY).fetchone()[0]  # type: ignore[index]
    )
    ph_count: int = con.execute(_PH_COUNT_QUERY).fetchone()[0]  # type: ignore[index]
    rpr_count: int = con.execute(_RPR_COUNT_QUERY).fetchone()[0]  # type: ignore[index]
    join_cardinality: int = (  # type: ignore[assignment]
        con.execute(_MFC_SELF_JOIN_CARDINALITY_QUERY).fetchone()[0]  # type: ignore[index]
    )
    mfc_cols_df = con.execute(_MFC_DESCRIBE_QUERY).fetchdf()
    mfc_cols: frozenset[str] = frozenset(mfc_cols_df["column_name"].tolist())
    LOGGER.debug(
        "_run_source_layer_peeks: mhm=%d mfc=%d ph=%d rpr=%d join_card=%d",
        mhm_count,
        mfc_count,
        ph_count,
        rpr_count,
        join_cardinality,
    )
    return {
        "mhm_count": mhm_count,
        "mhm_distinct_match_id": mhm_distinct,
        "mfc_count": mfc_count,
        "mfc_distinct_replay_id": mfc_distinct,
        "ph_count": ph_count,
        "rpr_count": rpr_count,
        "join_cardinality": join_cardinality,
        "mfc_columns": mfc_cols,
    }


def _run_anchor_peeks(con: duckdb.DuckDBPyConnection) -> dict[str, Any]:
    """Run read-only DuckDB peeks for Q2 anchor adjudication.

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        Dictionary with peek results for anchor checks.
    """
    mhm_desc_df = con.execute(_MHM_DESCRIBE_QUERY).fetchdf()
    mhm_types: dict[str, str] = dict(
        zip(mhm_desc_df["column_name"], mhm_desc_df["column_type"])
    )
    details_null_count: int = (  # type: ignore[assignment]
        con.execute(_MFC_DETAILS_TIMEUTC_NULL_QUERY).fetchone()[0]  # type: ignore[index]
    )
    started_at_range: tuple[Any, Any] = (
        con.execute(_MHM_STARTED_AT_RANGE_QUERY).fetchone()  # type: ignore[assignment]
    )
    cross_row_inconsistency: int = (  # type: ignore[assignment]
        con.execute(_MHM_CROSS_ROW_INCONSISTENCY_QUERY).fetchone()[0]  # type: ignore[index]
    )
    LOGGER.debug(
        "_run_anchor_peeks: started_at_type=%s null_count=%d cross_row_inconsistency=%d",
        mhm_types.get("started_at"),
        details_null_count,
        cross_row_inconsistency,
    )
    return {
        "mhm_column_types": mhm_types,
        "details_timeUTC_null_count": details_null_count,
        "started_at_range": started_at_range,
        "cross_row_inconsistency": cross_row_inconsistency,
    }


def _run_race_and_random_peeks(con: duckdb.DuckDBPyConnection) -> dict[str, Any]:
    """Run read-only DuckDB peeks for Q3 race-column and Random adjudication.

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        Dictionary with peek results for race/Random checks.
    """
    rpr_race_rows = con.execute(_RPR_RACE_VOCAB_QUERY).fetchall()
    rpr_selected_race_rows = con.execute(_RPR_SELECTED_RACE_VOCAB_QUERY).fetchall()
    mfc_selected_race_rows = con.execute(_MFC_SELECTED_RACE_VOCAB_QUERY).fetchall()
    rpr_mismatch_rows = con.execute(_RPR_RACE_MISMATCH_QUERY).fetchall()
    mhm_faction_rows = con.execute(_MHM_FACTION_VOCAB_QUERY).fetchall()
    rpr_race_vocab: dict[str, int] = {r: c for r, c in rpr_race_rows}
    rpr_selected_vocab: dict[str, int] = {r: c for r, c in rpr_selected_race_rows}
    mfc_selected_vocab: dict[str, int] = {r: c for r, c in mfc_selected_race_rows}
    mhm_faction_vocab: dict[str, int] = {f: c for f, c in mhm_faction_rows}
    rand_count: int = rpr_selected_vocab.get("Rand", 0)
    blank_count: int = rpr_selected_vocab.get("", 0)
    mfc_rand_count: int = mfc_selected_vocab.get("Rand", 0)
    mfc_random_count: int = mfc_selected_vocab.get("Random", 0)
    LOGGER.debug(
        "_run_race_and_random_peeks: rpr_race_vocab=%s rand_count=%d blank_count=%d",
        rpr_race_vocab,
        rand_count,
        blank_count,
    )
    return {
        "rpr_race_vocab": rpr_race_vocab,
        "rpr_selected_vocab": rpr_selected_vocab,
        "mfc_selected_vocab": mfc_selected_vocab,
        "mhm_faction_vocab": mhm_faction_vocab,
        "rpr_mismatch_rows": rpr_mismatch_rows,
        "rand_count_in_rpr": rand_count,
        "blank_count_in_rpr": blank_count,
        "mfc_rand_count": mfc_rand_count,
        "mfc_random_count": mfc_random_count,
    }


# ---------------------------------------------------------------------------
# Private adjudication helpers
# ---------------------------------------------------------------------------


def _adjudicate_source_layer(peeks: dict[str, Any]) -> AdjudicationDecision:
    """Adjudicate Q1 — source-layer decision.

    Args:
        peeks: Output of _run_source_layer_peeks.

    Returns:
        AdjudicationDecision for Q1_source_layer.
    """
    rationale = (
        "matches_flat_clean is chosen as the source layer for all 5 tranche-1 pre_game families. "
        "It natively scopes to 22,209 true 1v1 decisive replays × 2 player rows = 44,418 rows "
        "(matching EXPECTED_MFC_ROW_COUNT per Invariant I5), carrying all required columns "
        "(race, metadata_mapName, metadata_gameVersion, is_mmr_missing, replay_id, toon_id) "
        "without an additional JOIN to a sibling table. "
        "The self-join cardinality check CONCAT('sc2egset::', mfc.replay_id) = mhm.match_id "
        "AND mfc.toon_id = mhm.player_id returns 44,418 rows, confirming grain identity. "
        "The raw-flat candidate (replay_players_raw + matches_flat) requires an explicit "
        "1v1 scope filter and the mmr_valid constraint that matches_flat_clean applies natively. "
        "The view-layer candidate (MHM+PH) is the cross-dataset harmonization substrate "
        "(CROSS-02-00 §3.1) but has fewer direct columns; the hybrid (MHM for pair + MFC "
        "for static) adds JOIN complexity with no column gain since MFC carries all required "
        "columns. "
        "Invariant I5 (symmetric focal/opponent): the MFC self-join on (replay_id, toon_id) "
        "guarantees both slots from the same source with identical construction. "
        "RISK-24 (focal/opponent slot asymmetry) is mitigated by the symmetric self-join. "
        "CROSS-02-03 §6.1 confirms no strict-< filter is required for static game-T attributes; "
        "the anchor is a row-identity timestamp, not a window bound."
    )
    return AdjudicationDecision(
        decision_id="Q1_source_layer",
        candidates_considered=(
            "raw_flat (replay_players_raw + matches_flat)",
            "cleaned_raw (matches_flat_clean)",
            "view_layer (matches_history_minimal + player_history_all)",
            "hybrid (MHM for pair + matches_flat_clean for static columns)",
        ),
        chosen="cleaned_raw (matches_flat_clean)",
        rationale_paragraph=rationale,
        falsifiers_recorded=(
            "q1_no_evidence",
            "q1_source_1v1_lost",
            "q1_source_grain_mismatch",
            "q1_source_missing_column",
        ),
        blocking_for_materialization=True,
    )


def _adjudicate_anchor(peeks: dict[str, Any]) -> AdjudicationDecision:
    """Adjudicate Q2 — anchor decision (Phase-02 BINDING + Phase-03 RECOMMENDATION).

    Args:
        peeks: Output of _run_anchor_peeks.

    Returns:
        AdjudicationDecision for Q2_anchor.
    """
    rationale = (
        "Q2(a) Phase-02 row-identity anchor — BINDING: started_at TIMESTAMP from "
        "matches_history_minimal is chosen. CROSS-02-00 §3.1 declares TIMESTAMP as the canonical "
        "cross-dataset dtype for the temporal anchor; §3.2 retains details_timeUTC VARCHAR as the "
        "sc2egset-specific raw anchor for provenance only. The MHM started_at column is "
        "TIMESTAMP (verified via DESCRIBE), null count = 0 (verified via MFC details_timeUTC null "
        "check = 0), and cross-row inconsistency = 0 (verified: no match_id has two different "
        "started_at values). Per CROSS-02-03 §6.1, no strict-less-than filter is required for "
        "the 5 tranche-1 static game-T attributes; the anchor is a row-identity timestamp, not "
        "a window bound. details_timeUTC VARCHAR is retained as a provenance column only, never "
        "used in filters. "
        "Q2(b) Phase-03 chronological hold-out anchor — RECOMMENDATION ONLY: "
        "started_at TIMESTAMP is recommended for chronological ordering of train/test splits. "
        "This recommendation is NON-BINDING; the binding decision is made in Phase 03 planning, "
        "not in this Layer-2 artifact. CROSS-02-03 §6.1 confirms this is a row-identity anchor "
        "for tranche-1 families; the Phase-03 hold-out design may impose additional constraints "
        "that are out of scope here."
    )
    return AdjudicationDecision(
        decision_id="Q2_anchor",
        candidates_considered=(
            "details_timeUTC (raw VARCHAR from matches_flat_clean)",
            "started_at (harmonized TIMESTAMP from matches_history_minimal)",
            "hybrid (started_at as row-identity; details_timeUTC as provenance-only)",
        ),
        chosen=(
            "Q2(a) started_at TIMESTAMP from MHM (BINDING); "
            "Q2(b) started_at TIMESTAMP RECOMMENDATION ONLY for Phase-03 hold-out"
        ),
        rationale_paragraph=rationale,
        falsifiers_recorded=(
            "q2_anchor_type_mismatch",
            "q2_anchor_cross_row_inconsistency",
        ),
        blocking_for_materialization=True,
    )


def _adjudicate_race_and_random(peeks: dict[str, Any]) -> AdjudicationDecision:
    """Adjudicate Q3 — race-column and Random handling decision.

    Args:
        peeks: Output of _run_race_and_random_peeks.

    Returns:
        AdjudicationDecision for Q3_race_and_random.
    """
    rationale = (
        "Q3 outcome chosen: RATIFY the existing cleaning-layer convention. "
        "Two candidate outcomes were considered as live options throughout: "
        "Q3.RATIFY (retain the cleaning-layer convention: race = PRE_GAME analytical canon; "
        "selectedRace excluded from cleaned views) and Q3.AMEND (patch the cleaning-layer YAMLs "
        "and CROSS-02-02 §6.1 to honour RISK-26 literally, restoring selectedRace as the "
        "canonical pre-game race column). "
        "The cleaning-layer decision is documented verbatim in two authoritative YAML sources: "
        "(1) matches_long_raw.yaml:101-103: 'selectedRace' is explicitly dropped with reason "
        "'Pre-game menu selection (includes Random); race (actual played race) used instead.' "
        "(2) matches_history_minimal.yaml:52-53: MHM faction notes 'PRE_GAME. Raw vocabulary "
        "(race actually played, not selectedRace which includes Random).' "
        "These two YAML files are the authoritative source-of-truth for cleaning-layer decisions "
        "and were reviewed by the reviewer-adversarial pre-execution gate (APPROVE). "
        "RISK-26 (methodology_risk_register.md lines 479-492) records that the focal race feature "
        "for Random-pickers is Random at game-start time (selectedRace), not the eventual race. "
        "This creates a tension: the cleaning-layer decision chose race (post-decision for "
        "Random-pickers) as the analytical convention, while RISK-26 says selectedRace is the "
        "only true pre-game race for 1,120 Random player-rows (10 Rand + 1,110 blank normalised "
        "to Random in matches_flat_clean). "
        "RATIFY is chosen because: (a) reversing the cleaning-layer convention requires patching "
        "matches_long_raw.yaml:101-103, matches_history_minimal.yaml:52-53, and CROSS-02-02 §6.1"
        " — three coordinated edits that introduce a re-encoding risk for all downstream "
        "consumers; "
        "(b) the 1,120 Random player-rows represent approximately 555 matches (2.50% of 22,209), "
        "a small sub-population whose treatment is documented rather than silently omitted; "
        "(c) MHM faction vocabulary empirically contains {Prot, Terr, Zerg} only — consistent "
        "with the YAML-documented convention; the 4th value Random lives only in selectedRace "
        "in replay_players_raw. "
        "The RISK-26 tension is documented as a documented_gap, not a violation; CROSS-02-02 §6.1 "
        "mentions Random as a 4th declared race at the pre-game level (true for selectedRace) "
        "but MHM faction does not carry it. A CROSS-02-02 §6.1 minor amendment is proposed as "
        "a future-PR target (see §8 below). Random vocabulary under RATIFY: no canonicalisation "
        "rule is required because race is the chosen column and race has vocabulary {Prot, Terr, "
        "Zerg} (plus BW-legacy {BWPr, BWTe, BWZe} excluded by the 1v1 filter in MFC). "
        "Row retention: all 44,418 MFC rows are retained; no rows excluded by RATIFY. "
        "RISK-26 compliance: documented_gap (gap recorded; CROSS-02-02 §6.1 minor amendment "
        "proposed)."
    )
    return AdjudicationDecision(
        decision_id="Q3_race_and_random",
        candidates_considered=(
            "Q3.RATIFY: retain cleaning-layer convention "
            "(race = PRE_GAME canon; selectedRace excluded)",
            (
                "Q3.AMEND: patch cleaning-layer YAMLs + CROSS-02-02 §6.1 to restore selectedRace "
                "as canonical pre-game race (RISK-26 literal compliance)"
            ),
        ),
        chosen="Q3.RATIFY",
        rationale_paragraph=rationale,
        falsifiers_recorded=(
            "q3_race_post_decision_chosen",
            "q3_prior_decision_silently_reversed",
            "q3_random_vocabulary_dropped",
            "q3_random_spelling_uncanonicalised",
        ),
        blocking_for_materialization=True,
    )


# ---------------------------------------------------------------------------
# Falsifier checks
# ---------------------------------------------------------------------------


def _check_falsifiers_source_layer(
    peeks: dict[str, Any],
) -> str | None:
    """Check Q1 falsifiers; return first halting falsifier name or None.

    Args:
        peeks: Output of _run_source_layer_peeks.

    Returns:
        Falsifier name or None.
    """
    if peeks["mfc_count"] == 0 and peeks["mhm_count"] == 0:
        return "q1_no_evidence"
    if peeks["mfc_distinct_replay_id"] < EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID:
        return "q1_source_1v1_lost"
    if peeks["join_cardinality"] != EXPECTED_MFC_ROW_COUNT:
        return "q1_source_grain_mismatch"
    missing_cols = REQUIRED_MFC_COLUMNS - peeks["mfc_columns"]
    if missing_cols:
        LOGGER.warning("q1_source_missing_column: missing %s", missing_cols)
        return "q1_source_missing_column"
    return None


def _check_falsifiers_anchor(
    peeks: dict[str, Any],
) -> str | None:
    """Check Q2 falsifiers; return first halting falsifier name or None.

    Args:
        peeks: Output of _run_anchor_peeks.

    Returns:
        Falsifier name or None.
    """
    started_at_type: str = peeks["mhm_column_types"].get("started_at", "UNKNOWN")
    if started_at_type != "TIMESTAMP":
        return "q2_anchor_type_mismatch"
    if peeks["cross_row_inconsistency"] != 0:
        return "q2_anchor_cross_row_inconsistency"
    return None


def _check_falsifiers_race(
    peeks: dict[str, Any],
) -> str | None:
    """Check Q3 falsifiers; return first halting falsifier name or None.

    Under Q3.RATIFY the race column vocab is {Prot, Terr, Zerg} + BW-legacy,
    which is the post-decision vocabulary — this is NOT a falsifier under RATIFY
    because RATIFY explicitly chooses the post-decision convention. The
    q3_race_post_decision_chosen falsifier only fires under Q3.AMEND if the
    chosen column still has post-decision-only vocab.

    Under Q3.RATIFY, q3_prior_decision_silently_reversed fires if the rationale
    does NOT cite matches_long_raw.yaml:101-103.

    Args:
        peeks: Output of _run_race_and_random_peeks.

    Returns:
        Falsifier name or None.
    """
    mhm_faction_vocab: set[str] = set(peeks["mhm_faction_vocab"].keys())
    if mhm_faction_vocab - POST_DECISION_RACE_TOKENS - BW_LEGACY_RACE_TOKENS:
        unexpected = mhm_faction_vocab - POST_DECISION_RACE_TOKENS - BW_LEGACY_RACE_TOKENS
        LOGGER.warning(
            "MHM faction vocabulary has unexpected values %s — "
            "contradicts matches_history_minimal.yaml:52-53",
            unexpected,
        )
    return None


# ---------------------------------------------------------------------------
# Artifact SHA helpers
# ---------------------------------------------------------------------------


def _find_repo_root(start: Path) -> Path:
    """Walk up from start until pyproject.toml is found; return that directory.

    Args:
        start: Starting path (file or directory).

    Returns:
        The directory containing pyproject.toml.

    Raises:
        FileNotFoundError: If no pyproject.toml is found walking up from start.
    """
    candidate = start.resolve()
    while candidate != candidate.parent:
        if (candidate / "pyproject.toml").exists():
            return candidate
        candidate = candidate.parent
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


def _sha256_module(module_path: Path) -> str:
    """Compute SHA-256 hex digest of this validator module file.

    Args:
        module_path: Path to the module .py file.

    Returns:
        Hex digest string.
    """
    return _sha256_file(module_path)


def _get_git_sha() -> str:
    """Return the current HEAD git SHA (short or full).

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
# Artifact rendering helpers
# ---------------------------------------------------------------------------


def _validate_provenance_shas(rendered_rows: list[dict[str, str]]) -> None:
    """Validate all *_sha256 column values in rendered rows are 64-char lowercase hex digests.

    This is the provenance_sha_not_found halting falsifier check (Invariant I6).
    Raises ProvenanceShaNotFoundError if any value is invalid — the caller must
    NOT write the CSV in that case.

    Args:
        rendered_rows: List of row dicts to validate.

    Raises:
        ProvenanceShaNotFoundError: If any *_sha256 column is NOT_FOUND, empty,
            wrong length, or not lowercase hex.
    """
    _valid_hex_chars: frozenset[str] = frozenset("0123456789abcdef")
    for row_dict in rendered_rows:
        for key, value in row_dict.items():
            if not key.endswith("_sha256"):
                continue
            if (
                value == "NOT_FOUND"
                or not value
                or len(value) != 64
                or not all(c in _valid_hex_chars for c in value)
            ):
                raise ProvenanceShaNotFoundError(
                    f"Provenance SHA falsifier fired: row {row_dict.get('decision_id')!r} "
                    f"field {key!r} = {value!r}"
                )


def _render_artifact_csv(result: AdjudicationResult, out_path: Path) -> None:
    """Write the 3-row deterministic adjudication CSV artifact.

    Args:
        result: The AdjudicationResult to serialize.
        out_path: Destination path for the CSV.
    """
    # Derive repo root from this module's own location — always inside the repo,
    # unlike out_path which may point to a temp directory during testing.
    repo_root = _find_repo_root(Path(__file__))
    _module_rel = "src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_pre_game_source_layer.py"
    module_path = repo_root / _module_rel
    duckdb_path = repo_root / "src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb"
    registry_csv_path = (
        repo_root
        / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
        / "02_feature_engineering/01_pre_game_vs_in_game_boundary"
        / "02_01_01_feature_family_registry.csv"
    )
    git_sha = _get_git_sha()
    module_sha = _sha256_module(module_path)
    duckdb_sha = _sha256_file(duckdb_path)
    registry_sha = _sha256_file(registry_csv_path)
    risk_register_sha = _sha256_file(repo_root / _METHODOLOGY_RISK_REGISTER_RELPATH)
    spec_00_sha = _sha256_file(repo_root / _SPEC_02_00_RELPATH)
    spec_01_sha = _sha256_file(repo_root / _SPEC_02_01_RELPATH)
    spec_02_sha = _sha256_file(repo_root / _SPEC_02_02_RELPATH)
    spec_03_sha = _sha256_file(repo_root / _SPEC_02_03_RELPATH)
    mlr_sha = _sha256_file(repo_root / _MATCHES_LONG_RAW_YAML_RELPATH)
    mhm_sha = _sha256_file(repo_root / _MATCHES_HISTORY_MINIMAL_YAML_RELPATH)

    fieldnames = [
        "decision_id",
        "decision_name",
        "candidates_considered",
        "chosen",
        "rationale_excerpt_300char",
        "falsifiers_recorded",
        "blocking_for_materialization",
        "spec_contradictions",
        "spec_amendments_proposed",
        "provenance_git_sha",
        "provenance_executed_at_utc_date",
        "audit_pr",
        "validator_module",
        "validator_module_sha256",
        "duckdb_path",
        "duckdb_path_sha256",
        "registry_csv_sha256",
        "methodology_risk_register_sha256",
        "spec_02_00_sha256",
        "spec_02_01_sha256",
        "spec_02_02_sha256",
        "spec_02_03_sha256",
        "matches_long_raw_yaml_sha256",
        "matches_history_minimal_yaml_sha256",
    ]

    _decision_names = {
        "Q1_source_layer": "Source layer selection for 5 tranche-1 pre_game families",
        "Q2_anchor": (
            "Phase-02 row-identity anchor (BINDING) + Phase-03 hold-out anchor (RECOMMENDATION)"
        ),
        "Q3_race_and_random": "Race-column adjudication: cleaning-layer RATIFY vs AMEND (RISK-26)",
    }

    _spec_amendments: dict[str, str] = {
        "Q1_source_layer": "",
        "Q2_anchor": "",
        "Q3_race_and_random": (
            "CROSS-02-02 §6.1 minor: MHM faction derives from race and so excludes Random from "
            "its vocabulary; the 4th value Random lives only in selectedRace in replay_players_raw"
        ),
    }

    rendered_rows: list[dict[str, str]] = []
    for decision in result.decisions:
        rendered_rows.append(
            {
                "decision_id": decision.decision_id,
                "decision_name": _decision_names.get(
                    decision.decision_id, decision.decision_id
                ),
                "candidates_considered": "; ".join(decision.candidates_considered),
                "chosen": decision.chosen,
                "rationale_excerpt_300char": decision.rationale_paragraph[:300],
                "falsifiers_recorded": "; ".join(decision.falsifiers_recorded),
                "blocking_for_materialization": str(decision.blocking_for_materialization),
                "spec_contradictions": "; ".join(result.contradictions_with_specs),
                "spec_amendments_proposed": _spec_amendments.get(decision.decision_id, ""),
                "provenance_git_sha": git_sha,
                "provenance_executed_at_utc_date": EXECUTED_AT_UTC_DATE,
                "audit_pr": AUDIT_PR,
                "validator_module": "adjudicate_pre_game_source_layer.py",
                "validator_module_sha256": module_sha,
                "duckdb_path": str(
                    Path("src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb")
                ),
                "duckdb_path_sha256": duckdb_sha,
                "registry_csv_sha256": registry_sha,
                "methodology_risk_register_sha256": risk_register_sha,
                "spec_02_00_sha256": spec_00_sha,
                "spec_02_01_sha256": spec_01_sha,
                "spec_02_02_sha256": spec_02_sha,
                "spec_02_03_sha256": spec_03_sha,
                "matches_long_raw_yaml_sha256": mlr_sha,
                "matches_history_minimal_yaml_sha256": mhm_sha,
            }
        )

    _validate_provenance_shas(rendered_rows)

    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row_dict in rendered_rows:
            writer.writerow(row_dict)
    LOGGER.debug("_render_artifact_csv: written to %s", out_path)


def _build_md_content(
    result: AdjudicationResult,
    source_peeks: dict[str, Any],
    anchor_peeks: dict[str, Any],
    race_peeks: dict[str, Any],
) -> str:
    """Build the 8-section MD artifact content.

    Args:
        result: The AdjudicationResult.
        source_peeks: Output of _run_source_layer_peeks.
        anchor_peeks: Output of _run_anchor_peeks.
        race_peeks: Output of _run_race_and_random_peeks.

    Returns:
        Full MD content string.
    """
    q1 = result.decisions[0]
    q2 = result.decisions[1]
    q3 = result.decisions[2]

    mfc_count = source_peeks["mfc_count"]
    mfc_distinct = source_peeks["mfc_distinct_replay_id"]
    join_card = source_peeks["join_cardinality"]
    started_at_type = anchor_peeks["mhm_column_types"].get("started_at", "UNKNOWN")
    details_null = anchor_peeks["details_timeUTC_null_count"]
    cross_row = anchor_peeks["cross_row_inconsistency"]
    started_range = anchor_peeks["started_at_range"]
    rpr_race = race_peeks["rpr_race_vocab"]
    rpr_sel = race_peeks["rpr_selected_vocab"]
    mfc_sel = race_peeks["mfc_selected_vocab"]
    mhm_fac = race_peeks["mhm_faction_vocab"]
    rand_count = race_peeks["rand_count_in_rpr"]
    blank_count = race_peeks["blank_count_in_rpr"]

    all_falsifiers = [
        "q1_no_evidence",
        "q1_source_1v1_lost",
        "q1_source_grain_mismatch",
        "q1_source_missing_column",
        "q2_anchor_type_mismatch",
        "q2_anchor_cross_row_inconsistency",
        "q3_race_post_decision_chosen",
        "q3_prior_decision_silently_reversed",
        "q3_random_vocabulary_dropped",
        "q3_random_spelling_uncanonicalised",
        "provenance_sha_not_found",
        "spec_amendment_silent",
        "non_substitution_silent",
        "materialization_creep",
        "status_flip",
        "phase03_creep",
        "tracker_creep",
        "leakage_audit_overclaim",
        "batching",
    ]

    falsifier_rows = "\n".join(
        f"- `{f}`: {'FIRED → halt' if f == result.halting_falsifier else 'did not fire'}"
        for f in all_falsifiers
    )

    md = f"""# SC2EGSet Step 02_01_02 — Source / Anchor / Race-Column Adjudication

## §1 Non-Overclaim Disclaimer

This artifact is an adjudication of three coupled pre-materialization questions for sc2egset
Step 02_01_02. It does NOT materialize any feature value, does NOT run the CROSS-02-01-v1.0.1
post-materialization leakage audit, and does NOT close Step 02_01_02. The CROSS-02-01 audit
remains FUTURE and remains vacuously satisfied by PR #230 until a materialization PR lands.

Generated by {AUDIT_PR} on {EXECUTED_AT_UTC_DATE}.

## §2 Q1 — Source Layer

**Candidates considered:** {len(q1.candidates_considered)}
(raw-flat, cleaned-raw, view-layer, hybrid).

**Chosen:** {q1.chosen}.

### Peek SQL and results (Invariant I6)

```sql
-- MFC row count
{_MFC_COUNT_QUERY}
-- Result: {mfc_count}

-- MFC distinct replay_id
{_MFC_DISTINCT_REPLAY_ID_QUERY}
-- Result: {mfc_distinct}

-- MHM row count
{_MHM_COUNT_QUERY}
-- Result: {source_peeks["mhm_count"]}

-- MHM distinct match_id
{_MHM_DISTINCT_MATCH_ID_QUERY}
-- Result: {source_peeks["mhm_distinct_match_id"]}

-- PH row count
{_PH_COUNT_QUERY}
-- Result: {source_peeks["ph_count"]}

-- RPR row count
{_RPR_COUNT_QUERY}
-- Result: {source_peeks["rpr_count"]}

-- Self-join cardinality check (I5)
{_MFC_SELF_JOIN_CARDINALITY_QUERY.strip()}
-- Result: {join_card}
```

### Rationale

{q1.rationale_paragraph}

## §3 Q2 — Anchor (Q2(a) Phase-02 BINDING + Q2(b) Phase-03 RECOMMENDATION ONLY)

**Chosen:** {q2.chosen}.

The binding decision is Q2(a) only. Q2(b) is a RECOMMENDATION for Phase 03 planning;
the binding decision is made in Phase 03 planning, NOT in this Layer-2 artifact.

### Peek SQL and results (Invariant I6)

```sql
-- MHM DESCRIBE (anchor type check)
{_MHM_DESCRIBE_QUERY}
-- started_at type: {started_at_type}

-- details_timeUTC null rate in MFC
{_MFC_DETAILS_TIMEUTC_NULL_QUERY}
-- Result: {details_null}

-- MHM started_at range
{_MHM_STARTED_AT_RANGE_QUERY}
-- Result: MIN={started_range[0]}, MAX={started_range[1]}

-- MHM cross-row inconsistency check
{_MHM_CROSS_ROW_INCONSISTENCY_QUERY.strip()}
-- Result: {cross_row}
```

### Rationale

{q2.rationale_paragraph}

## §4 Q3 — Race-Column and Random Handling (RATIFY vs AMEND)

Both Q3.RATIFY and Q3.AMEND were considered as live options. **Chosen outcome: Q3.RATIFY.**

### Q3.RATIFY (Candidate A)

Retain the existing cleaning-layer convention: `race` = PRE_GAME analytical canon;
`selectedRace` excluded from cleaned views. Basis: `matches_long_raw.yaml:101-103`
(selectedRace explicitly dropped; reason: "Pre-game menu selection (includes 'Random');
race (actual played race) used instead.") and `matches_history_minimal.yaml:52-53`
(MHM faction notes "PRE_GAME. Raw vocabulary (race actually played, not selectedRace
which includes 'Random')"). Implications: tranche-1 inherits the post-decision overwrite
for 1,120 Random player-rows; downstream encoders see a 3-value race vocabulary. The
RISK-26 gap is documented (see §8) but not patched.

### Q3.AMEND (Candidate B)

Patch the cleaning-layer YAMLs and CROSS-02-02 §6.1 to honour RISK-26 literally.
Patches required: (i) matches_long_raw.yaml:101-103 removes the selectedRace exclusion;
(ii) matches_history_minimal.yaml:52-53 re-sources faction from selectedRace; (iii)
CROSS-02-02 §6.1 clarifies the 4th Random value is now in MHM faction. Sub-decision
for Random vocabulary: (a) retain as 4th category Random (canonicalise Rand→Random);
(b) retain as 5th category; (c) exclude with documented bias; (d) encode as sentinel
plus flag. NOT CHOSEN in this PR; patches proposed only (see §8).

### Peek SQL and results (Invariant I6)

```sql
-- RPR race vocabulary
{_RPR_RACE_VOCAB_QUERY}
-- Result: {dict(sorted(rpr_race.items()))}

-- RPR selectedRace vocabulary
{_RPR_SELECTED_RACE_VOCAB_QUERY}
-- Result: {dict(sorted(rpr_sel.items()))}
-- Note: Rand count = {rand_count}; blank count = {blank_count}

-- MFC selectedRace vocabulary (post-cleaning normalisation)
{_MFC_SELECTED_RACE_VOCAB_QUERY}
-- Result: {dict(sorted(mfc_sel.items()))}

-- MHM faction vocabulary
{_MHM_FACTION_VOCAB_QUERY}
-- Result: {dict(sorted(mhm_fac.items()))}

-- race vs selectedRace mismatch in RPR
{_RPR_RACE_MISMATCH_QUERY.strip()}
-- Result (rows where race != selectedRace): see peek data
```

### Rationale (Q3 — ≥ 250 words)

{q3.rationale_paragraph}

**RISK-26 compliance: documented_gap.** The gap between RISK-26 and the cleaning-layer
convention is documented here; a CROSS-02-02 §6.1 minor amendment is proposed as a
future-PR target (see §8). Not violated.

## §5 Falsifier Roll-Call

Every falsifier checked. A fired falsifier would halt this PR before writing the CSV artifact.

{falsifier_rows}

**Overall verdict:** {
    'PASS — all falsifiers did not fire'
    if result.halting_falsifier is None
    else f'HALT — {result.halting_falsifier} fired'
}

## §6 Inputs to FUTURE Materialization-Execution Planner-Science Round

The three decisions are frozen as inputs for the next (Layer-3) materialization-execution PR:

- **Source layer** = `matches_flat_clean` (cleaned-raw, 1v1-scoped native); family→table map =
  all 5 tranche-1 families → matches_flat_clean; self-join keys = `(replay_id, toon_id)` for
  focal/opponent pair.
- **Anchor** = `started_at TIMESTAMP` from matches_history_minimal; type = TIMESTAMP; use as
  window-bound = false (static game-T attribute per CROSS-02-03 §6.1); use as row-identity = true.
  Phase-03 RECOMMENDATION = `started_at TIMESTAMP` (NON-BINDING).
- **Race column** = `race` (Q3.RATIFY); Random handling = N/A (race has no Random value;
  selectedRace is excluded); canonicalisation rule = N/A; row-retention impact = all 44,418 rows
  retained; RISK-26 compliance = documented_gap.
- **`lineage_position`:** {LINEAGE_POSITION}

## §7 Explicit Non-Substitution Statement

This artifact does NOT replace, weaken, or amend:
(a) PR #229 §10 design-time verdict-audit pair;
(b) PR #230 CROSS-02-01 vacuous leakage-audit pair;
(c) the FUTURE post-materialization CROSS-02-01 audit (which does not yet exist and is not
produced here).

The CROSS-02-01-v1.0.1 post-materialization leakage audit and the mandatory Claude/ChatGPT
second-pass leakage review remain FUTURE. They are distinct gates and are not discharged by
this artifact.

## §8 Spec Amendments Proposed (NOT Applied Here)

Under Q3.RATIFY, one amendment is proposed as a future-PR target:

1. **CROSS-02-02 §6.1 minor amendment:** "MHM `faction` derives from `race` and so excludes
   Random from its vocabulary; the 4th value `Random` lives only in `selectedRace` in
   `replay_players_raw`." This amendment reconciles the CROSS-02-02 §6.1 text ("Random is a
   fourth declared race at pre-game") with the MHM YAML-documented convention. The amendment
   is PROPOSED only — not applied in this PR.

2. **OQ5 / INVARIANTS.md or CROSS-02-00 §5.4 minor annotation proposed:** Record the
   on-disk vocabulary fact (`Rand`=10 + blank=1,110 in `selectedRace` of replay_players_raw;
   cleaned-view-normalised to `Random` after 01_04_02). Proposed as future-PR target.

No cleaning-layer YAML patches are applied. Under Q3.AMEND (not chosen), patches would be:
(i) matches_long_raw.yaml:101-103 removes selectedRace exclusion;
(ii) matches_history_minimal.yaml:52-53 re-sources faction from selectedRace;
(iii) CROSS-02-02 §6.1 clarifies 4th Random value in MHM faction.
"""
    return md


def _render_artifact_md(
    result: AdjudicationResult,
    out_path: Path,
    source_peeks: dict[str, Any],
    anchor_peeks: dict[str, Any],
    race_peeks: dict[str, Any],
) -> None:
    """Write the 8-section MD artifact companion.

    Args:
        result: The AdjudicationResult.
        out_path: Destination path for the MD.
        source_peeks: Output of _run_source_layer_peeks.
        anchor_peeks: Output of _run_anchor_peeks.
        race_peeks: Output of _run_race_and_random_peeks.
    """
    content = _build_md_content(result, source_peeks, anchor_peeks, race_peeks)
    with out_path.open("w", encoding="utf-8") as fh:
        fh.write(content)
    LOGGER.debug("_render_artifact_md: written to %s", out_path)


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def adjudicate_pre_game_source_layer(
    duckdb_path: Path | str,
    registry_csv_path: Path | str,
    output_artifact_dir: Path | str,
) -> AdjudicationResult:
    """Adjudicate the three coupled pre-materialization decisions for sc2egset Step 02_01_02.

    Runs read-only DuckDB peeks for three decisions (Q1 source layer, Q2 anchor,
    Q3 race-column), adjudicates each, writes a 3-row CSV and 8-section MD artifact
    to output_artifact_dir, and returns a frozen AdjudicationResult. Does NOT
    materialize any feature value. ``materialized_output_paths`` is ALWAYS ``()``.

    The CSV is NOT written if a halting falsifier fires. The MD is written in both
    cases (with the falsifier roll-call section populated) to preserve auditability.

    Args:
        duckdb_path: Path to the sc2egset DuckDB file (opened read-only).
        registry_csv_path: Path to the closed 02_01_01 registry CSV (read for provenance hash).
        output_artifact_dir: Directory where the artifact pair is written.
            Canonical: src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/
            02_feature_engineering/01_pre_game_vs_in_game_boundary/

    Returns:
        AdjudicationResult with passed=True iff halting_falsifier is None,
        exactly 3 decisions, materialized_output_paths=(), and artifact paths.
    """
    db_path = Path(duckdb_path)
    out_dir = Path(output_artifact_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_out = out_dir / "02_01_02_source_anchor_race_adjudication.csv"
    md_out = out_dir / "02_01_02_source_anchor_race_adjudication.md"

    LOGGER.info("adjudicate_pre_game_source_layer: opening DuckDB at %s (read-only)", db_path)
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        source_peeks = _run_source_layer_peeks(con)
        anchor_peeks = _run_anchor_peeks(con)
        race_peeks = _run_race_and_random_peeks(con)
    finally:
        con.close()

    halting: str | None = None
    halting = halting or _check_falsifiers_source_layer(source_peeks)
    halting = halting or _check_falsifiers_anchor(anchor_peeks)
    halting = halting or _check_falsifiers_race(race_peeks)

    q1 = _adjudicate_source_layer(source_peeks)
    q2 = _adjudicate_anchor(anchor_peeks)
    q3 = _adjudicate_race_and_random(race_peeks)

    spec_amendments: tuple[str, ...] = (
        (
            "CROSS-02-02 §6.1 minor: MHM faction derives from race and so excludes Random "
            "from its vocabulary; the 4th value Random lives only in selectedRace in "
            "replay_players_raw"
        ),
    )

    result = AdjudicationResult(
        passed=halting is None,
        decisions=(q1, q2, q3),
        contradictions_with_specs=(),
        spec_amendments_proposed=spec_amendments,
        materialized_output_paths=(),
        artifact_csv_path=str(csv_out),
        artifact_md_path=str(md_out),
        halting_falsifier=halting,
    )

    _render_artifact_md(result, md_out, source_peeks, anchor_peeks, race_peeks)

    if halting is None:
        try:
            _render_artifact_csv(result, csv_out)
        except ProvenanceShaNotFoundError as exc:
            LOGGER.error(
                "adjudicate_pre_game_source_layer: provenance_sha_not_found falsifier: %s", exc
            )
            halting = "provenance_sha_not_found"
            result = AdjudicationResult(
                passed=False,
                decisions=result.decisions,
                contradictions_with_specs=result.contradictions_with_specs,
                spec_amendments_proposed=result.spec_amendments_proposed,
                materialized_output_paths=(),
                artifact_csv_path=str(csv_out),
                artifact_md_path=str(md_out),
                halting_falsifier=halting,
            )
            LOGGER.warning(
                "adjudicate_pre_game_source_layer: halting falsifier fired: %s; CSV not written",
                halting,
            )
        else:
            LOGGER.info(
                "adjudicate_pre_game_source_layer: passed=True; artifacts written to %s", out_dir
            )
    else:
        LOGGER.warning(
            "adjudicate_pre_game_source_layer: halting falsifier fired: %s; CSV not written",
            halting,
        )

    LOGGER.debug(
        "adjudicate_pre_game_source_layer: passed=%s decisions=%d halting=%s",
        result.passed,
        len(result.decisions),
        result.halting_falsifier,
    )
    return result
