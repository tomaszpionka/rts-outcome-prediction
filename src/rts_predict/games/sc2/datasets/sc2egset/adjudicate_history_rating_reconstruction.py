"""Q6 rating-reconstruction successor adjudicator for SC2EGSet Step 02_01_03.

Pure read-only module. Writes ONLY the Q6 successor adjudication CSV+MD
artifact pair. Never materializes a rating value. Never writes Parquet.
Never modifies status YAMLs or research logs. See
``planning/current_plan.md`` for the full Layer-1 spec.

This module is the Layer-2 successor to PR #242's parent adjudication.
PR #242 closed Q6 (``rating_policy``) as ``verdict=deferred_blocker``.
PR #243 resolved Q5 (``cross_region_fragmentation_handling``) with
``Q5_selected_policy=sensitivity_indicator_co_registration``. This module
(future PR #N) upgrades Q6 only; Q5 is NOT re-adjudicated.

The 6 candidate rating policies (closed enumerated set per planning
Assumption 11):

    Q6A  omit_reconstructed_rating
    Q6B  rolling_win_rate_or_bayesian_smoothed_baseline
    Q6C  elo                            (Elo 1978)
    Q6D  glicko_or_glicko_2             (Glickman 1999 / 2012)
    Q6E  trueskill_or_trueskill_like    (Herbrich, Minka, Graepel 2006)
    Q6F  deferred_blocker_with_algorithm_survey_required

N-1 binding: methods listed in dataset research_log lines 733-734 and 961
(aligulac_style_btl, bradley_terry, neural_btl) are recorded in the
``excluded_methods_considered`` field — NOT extended into the candidate
set (planning binding nit (b)).

N-2 binding: the "use raw MMR for the 16.05% rated subset + cold-start
the rest" hybrid is recorded in the ``raw_mmr_hybrid_rejection`` field
with an explicit rejection rationale (planning binding nit).

N-3 binding: PHA per-player history-depth probe uses ``GROUP BY toon_id``
because ``player_history_all`` does NOT carry a ``player_id_worldwide``
column on this dataset (verified at module-author time by DESCRIBE
player_history_all). The ``toon_id`` form is the canonical PHA grouping
key for sc2egset; ``player_id_worldwide`` is constructed only at the MHM
join layer (``'sc2egset::' || mfc.replay_id`` per PR #242 Q2 binding).
The probe's docstring records this resolution explicitly.

N-4 binding: probes use ORDER BY before LIMIT or omit LIMIT entirely
(byte-determinism guarantee preserved at zero probe cost).

N-9 (soft): the POST-GAME token set is re-used from PR #242's parent
adjudicator via direct import (``POST_GAME_TOKENS``,
``POST_GAME_TOKEN_SCOPED_FIELDS``, ``POST_GAME_TOKEN_EXEMPT_FIELDS``).

Selected verdict (per planning T05 "default recommendation if you cannot
conclusively bind a winner"): ``Q6F_deferred_with_algorithm_survey``
with ``verdict='deferred_blocker'`` and
``materialization_permission='blocked_pending_algorithm_survey_pr'``.
This preserves Invariant I7 (no magic-number K, prior, RD, sigma, tau,
rating_period) — comparative back-testing AUC / log-loss evidence does
not exist in any prior artifact and would require its own algorithm
survey Step. See planning OQ2.

Materialization is BLOCKED in this PR and in every downstream
consequence of this PR. The Q6_selected_policy row's
``materialization_permission`` field encodes this verbatim.
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import re
import subprocess
from collections.abc import Callable
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

import duckdb

from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import (  # noqa: E501
    EXPECTED_PR241_VALIDATOR_SHA256,
    POST_GAME_TOKENS,
)

_FalsifierThunk = Callable[[], tuple[bool, str]]

LOGGER = logging.getLogger(__name__)

__all__ = [
    "ALLOWED_COMPLEXITY_DEPLOYABILITY",
    "ALLOWED_LEAKAGE_RISK",
    "ALLOWED_MATERIALIZATION_PERMISSION",
    "ALLOWED_Q6_BINDING_LEVELS",
    "ALLOWED_Q6_VERDICTS",
    "ALLOWED_RATING_EVIDENCE_LEVELS",
    "CITATION_ELO_1978",
    "CITATION_GLICKMAN_1999",
    "CITATION_GLICKMAN_2012",
    "CITATION_HERBRICH_MINKA_GRAEPEL_2006",
    "EXCLUDED_METHODS_CONSIDERED",
    "EXPECTED_CROSS_02_02_SPEC_SHA256",
    "EXPECTED_DATASET_RESEARCH_LOG_SHA256",
    "EXPECTED_FEATURE_FAMILY_REGISTRY_CSV_SHA256",
    "EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256",
    "EXPECTED_MATCHES_HISTORY_MINIMAL_YAML_SHA256",
    "EXPECTED_MFC_DISTINCT_REPLAY_ID_COUNT",
    "EXPECTED_MFC_ROW_COUNT",
    "EXPECTED_MHM_ROW_COUNT",
    "EXPECTED_MMR_MISSING_DENSITY_MFC_PCT",
    "EXPECTED_MMR_MISSING_DENSITY_PHA_PCT",
    "EXPECTED_PHA_ROW_COUNT",
    "EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256",
    "EXPECTED_PR241_VALIDATOR_SHA256",
    "EXPECTED_PR242_CSV_SHA256",
    "EXPECTED_PR242_MD_SHA256",
    "EXPECTED_PR243_CSV_SHA256",
    "EXPECTED_PR243_MD_SHA256",
    "FALSIFIER_PRIORITY_CHAIN",
    "HELPER_TO_FALSIFIER_KEY",
    "HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS",
    "NON_RATING_HISTORY_FAMILIES",
    "Q5_SELECTED_POLICY",
    "Q5_SELECTED_POLICY_VERDICT",
    "Q6_ADJUDICATION_SCHEMA",
    "Q6_DECISION_IDS",
    "Q6_RATING_POLICY_CANDIDATES",
    "RATING_RECONSTRUCTION_ADJUDICATION_CSV_REL",
    "RATING_RECONSTRUCTION_ADJUDICATION_MD_REL",
    "RAW_MMR_HYBRID_REJECTION_TOKEN",
    "RatingReconstructionAdjudicationDecision",
    "RatingReconstructionAdjudicationError",
    "RatingReconstructionAdjudicationResult",
    "STRICT_LT_HISTORY_FILTER",
    "TARGET_ANCHOR_COLUMN",
    "TARGET_SOURCE_TABLE",
    "HISTORY_SOURCE_TABLE",
    "HISTORY_TIME_COLUMN",
    "run_rating_reconstruction_adjudication",
]


# ---------------------------------------------------------------------------
# Predecessor PR provenance + parent SHAs (BINDING; mismatch halts)
# ---------------------------------------------------------------------------

PARENT_PR242_NUMBER: str = "PR #242"
PARENT_PR243_NUMBER: str = "PR #243"

EXPECTED_PR242_CSV_SHA256: str = (
    "f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b"
)
EXPECTED_PR242_MD_SHA256: str = (
    "fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d"
)
EXPECTED_PR243_CSV_SHA256: str = (
    "29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424"
)
EXPECTED_PR243_MD_SHA256: str = (
    "026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719"
)

# Source-file SHAs — pinned at module-author time on master HEAD 0e3cf938.
# Any drift in the upstream files halts the entrypoint before write.
EXPECTED_CROSS_02_02_SPEC_SHA256: str = (
    "86af792370272e611f048aae0c48c9cc595eb4b44c1db38c0bb4ecea0ff1b289"
)
EXPECTED_FEATURE_FAMILY_REGISTRY_CSV_SHA256: str = (
    "320b8b018982f12539a34512421f1b34359bb825f0d1410687492dfe5c6fed1f"
)
EXPECTED_DATASET_RESEARCH_LOG_SHA256: str = (
    "3290607dad93f9907818f6c0fe61200fcbaa0d9891d3dfbec677996cb58fb1c7"
)
EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256: str = (
    "7962dd910e0b72419e35a9895689cd4ae6a51c2be0bc6e5e0fe4a0ceb8f207d0"
)
EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256: str = (
    "9f76c1912624535b7b7ac0d2fb767fd4b9791a1d808bf73f747416d557d6cb1f"
)
EXPECTED_MATCHES_HISTORY_MINIMAL_YAML_SHA256: str = (
    "4c700e1b1584186542d6c1c43f847c03ee8664ced948534143e605a05ae7e67f"
)


# ---------------------------------------------------------------------------
# Inherited PR #242 anchors (referenced; NOT re-derived)
# ---------------------------------------------------------------------------

TARGET_SOURCE_TABLE: str = "matches_flat_clean"
HISTORY_SOURCE_TABLE: str = "player_history_all"
TARGET_ANCHOR_COLUMN: str = "matches_history_minimal.started_at"
HISTORY_TIME_COLUMN: str = "player_history_all.details_timeUTC"
STRICT_LT_HISTORY_FILTER: str = (
    "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"
)
EXPECTED_MFC_ROW_COUNT: int = 44418
EXPECTED_MHM_ROW_COUNT: int = 44418
EXPECTED_PHA_ROW_COUNT: int = 44817
EXPECTED_MFC_DISTINCT_REPLAY_ID_COUNT: int = 22209
EXPECTED_MMR_MISSING_DENSITY_MFC_PCT: float = 83.95
EXPECTED_MMR_MISSING_DENSITY_PHA_PCT: float = 83.65

# Inherited PR #243 anchors (referenced; NOT re-litigated)
Q5_SELECTED_POLICY: str = "sensitivity_indicator_co_registration"
Q5_SELECTED_POLICY_VERDICT: str = "narrow_with_evidence"


# ---------------------------------------------------------------------------
# Q6 decision IDs and rating-policy candidate set
# ---------------------------------------------------------------------------

Q6_DECISION_IDS: tuple[str, ...] = (
    "Q6A_omit_reconstructed_rating",
    "Q6B_rolling_win_rate_or_bayesian_smoothed_baseline",
    "Q6C_elo",
    "Q6D_glicko_or_glicko_2",
    "Q6E_trueskill_or_trueskill_like",
    "Q6F_deferred_with_algorithm_survey",
    "Q6_selected_policy",
    "Q6_per_family_impact_summary",
)
Q6_DECISION_COUNT: int = 8

Q6_RATING_POLICY_CANDIDATES: tuple[str, ...] = (
    "omit_reconstructed_rating",
    "rolling_win_rate_or_bayesian_smoothed_baseline",
    "elo",
    "glicko_or_glicko_2",
    "trueskill_or_trueskill_like",
    "deferred_blocker_with_algorithm_survey_required",
)
Q6_RATING_POLICY_CANDIDATE_COUNT: int = 6

# N-1 binding: methods acknowledged from dataset research_log lines 733-734
# and 961 as part of the substrate's intended backtesting universe but
# EXCLUDED from the Q6 candidate set per planning binding nit (b). The
# rejection rationale lives in MD §5 and the per-row notes.
EXCLUDED_METHODS_CONSIDERED: tuple[str, ...] = (
    "aligulac_style_btl",
    "bradley_terry",
    "neural_btl",
)

# N-2 binding: raw-MMR-where-present hybrid candidate explicit rejection
# token. Cited verbatim in the Q6_selected_policy row's
# raw_mmr_hybrid_rejection field.
RAW_MMR_HYBRID_REJECTION_TOKEN: str = (
    "raw_mmr_where_present_plus_is_mmr_missing"
)


# ---------------------------------------------------------------------------
# Allowed-value enums
# ---------------------------------------------------------------------------

ALLOWED_Q6_VERDICTS: frozenset[str] = frozenset(
    {
        "bind_now",
        "ratify_with_evidence",
        "extend_with_evidence",
        "narrow_with_evidence",
        "recommendation_only",
        "deferred_recommendation",
        "deferred_blocker",
    }
)

ALLOWED_Q6_BINDING_LEVELS: frozenset[str] = frozenset(
    {
        "binding_for_materialization",
        "recommendation_only",
        "deferred_blocker",
    }
)

ALLOWED_RATING_EVIDENCE_LEVELS: frozenset[str] = frozenset(
    {
        "in_repo_only",
        "in_repo_plus_citation",
        "deferred",
    }
)

ALLOWED_COMPLEXITY_DEPLOYABILITY: frozenset[str] = frozenset(
    {"low", "medium", "high", "not_applicable"}
)

ALLOWED_LEAKAGE_RISK: frozenset[str] = frozenset(
    {
        "low_if_forward_only_enforced",
        "medium_if_forward_only_enforced",
        "high_if_global_fit_used",
        "not_applicable",
    }
)

ALLOWED_MATERIALIZATION_PERMISSION: frozenset[str] = frozenset(
    {
        "permitted_for_other_5_families_without_reconstructed_rating",
        "permitted_for_all_6_families_with_pinned_hyperparameters_pr",
        "blocked_pending_algorithm_survey_pr",
        "not_applicable",
    }
)


# ---------------------------------------------------------------------------
# Algorithm primary-source citations (author/year strings; N-X3 gate)
# ---------------------------------------------------------------------------

CITATION_ELO_1978: str = (
    "Elo (1978) -- The Rating of Chessplayers, Past and Present"
)
CITATION_GLICKMAN_1999: str = (
    "Glickman (1999) -- Parameter estimation in large dynamic paired "
    "comparison experiments"
)
CITATION_GLICKMAN_2012: str = (
    "Glickman (2012) -- The Glicko-2 system for rating players"
)
CITATION_HERBRICH_MINKA_GRAEPEL_2006: str = (
    "Herbrich, Minka, Graepel (2006) -- TrueSkill: A Bayesian Skill "
    "Rating System"
)

# Per-candidate citation requirements (non-omit non-deferred policies).
CANDIDATE_REQUIRED_CITATIONS: dict[str, tuple[str, ...]] = {
    "elo": (CITATION_ELO_1978,),
    "glicko_or_glicko_2": (
        CITATION_GLICKMAN_1999,
        CITATION_GLICKMAN_2012,
    ),
    "trueskill_or_trueskill_like": (CITATION_HERBRICH_MINKA_GRAEPEL_2006,),
}


# ---------------------------------------------------------------------------
# History-enriched pre_game family IDs (FIXED; for per_family_impact_summary)
# ---------------------------------------------------------------------------

HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS: tuple[str, ...] = (
    "focal_player_history",
    "opponent_player_history",
    "matchup_history_aggregate",
    "reconstructed_rating",
    "in_game_history_aggregate",
    "cross_region_fragmentation_handling",
)

NON_RATING_HISTORY_FAMILIES: tuple[str, ...] = tuple(
    f for f in HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS if f != "reconstructed_rating"
)


# ---------------------------------------------------------------------------
# Artifact-pair paths (relative; I10)
# ---------------------------------------------------------------------------

RATING_RECONSTRUCTION_ADJUDICATION_CSV_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_rating_reconstruction_adjudication.csv"
)
RATING_RECONSTRUCTION_ADJUDICATION_MD_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_rating_reconstruction_adjudication.md"
)

# Parent + source-file paths (relative).
PARENT_PR242_CSV_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_source_anchor_coldstart_adjudication.csv"
)
PARENT_PR242_MD_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_source_anchor_coldstart_adjudication.md"
)
PARENT_PR243_CSV_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_cross_region_adjudication.csv"
)
PARENT_PR243_MD_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_cross_region_adjudication.md"
)
PR241_VALIDATOR_MODULE_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/"
    "validate_history_enriched_pre_game_materialization.py"
)
CROSS_02_02_SPEC_REL: str = "reports/specs/02_02_feature_engineering_plan.md"
FEATURE_FAMILY_REGISTRY_CSV_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_01_feature_family_registry.csv"
)
DATASET_RESEARCH_LOG_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
)
PLAYER_HISTORY_ALL_YAML_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/"
    "player_history_all.yaml"
)
MATCHES_FLAT_CLEAN_YAML_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/"
    "matches_flat_clean.yaml"
)
MATCHES_HISTORY_MINIMAL_YAML_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/"
    "matches_history_minimal.yaml"
)


# ---------------------------------------------------------------------------
# SQL probes (read-only; evidence-availability ONLY; never rating runs)
#
# N-5 design note: every probe is a single-table COUNT FILTER over PHA or
# MFC (no JOIN), so PR #243's LEFT-JOIN-NULL trap is structurally
# inapplicable here.
#
# N-4 binding: full-table scans (no LIMIT) preserve byte-determinism at
# zero cost (44,817 rows is trivially cheap).
# ---------------------------------------------------------------------------

# Probe 1: PHA result distribution (full table; no LIMIT per N-4).
PROBE_PHA_RESULT_DISTRIBUTION_QUERY: str = """
SELECT result, COUNT(*) AS n
FROM player_history_all
GROUP BY result
ORDER BY n DESC, result
""".strip()

# Probe 2: PHA details_timeUTC TRY_CAST null-rate (full table; no LIMIT).
PROBE_PHA_DETAILS_TIMEUTC_TRY_CAST_NULL_RATE_QUERY: str = """
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE TRY_CAST(details_timeUTC AS TIMESTAMP) IS NULL)
        AS null_after_cast
FROM player_history_all
""".strip()

# Probe 3: MMR-missingness reaffirmation against MFC.
PROBE_MFC_MMR_MISSING_DENSITY_QUERY: str = """
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE is_mmr_missing = TRUE) AS mmr_missing
FROM matches_flat_clean
""".strip()

# Probe 4: MMR-missingness reaffirmation against PHA.
PROBE_PHA_MMR_MISSING_DENSITY_QUERY: str = """
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE is_mmr_missing = TRUE) AS mmr_missing
FROM player_history_all
""".strip()

# Probe 5: PHA per-player history depth distribution (cold-start prevalence
# evidence). GROUPED BY toon_id (N-3 sanity-check resolution): the schema
# of player_history_all in sc2egset does NOT include a
# `player_id_worldwide` column (verified by DESCRIBE at module-author
# time). The canonical PHA grouping key for sc2egset is `toon_id`;
# `player_id_worldwide` is constructed only at the MHM join layer
# (`'sc2egset::' || mfc.replay_id` per PR #242 Q2 BIND_NOW). PR #243
# used `toon_id` for the same reason in its retention probes.
PROBE_PHA_PER_PLAYER_HISTORY_DEPTH_QUERY: str = """
SELECT cnt_bucket, COUNT(*) AS n_players
FROM (
    SELECT CASE
        WHEN n = 1 THEN '1'
        WHEN n BETWEEN 2 AND 4 THEN '2-4'
        WHEN n BETWEEN 5 AND 9 THEN '5-9'
        WHEN n BETWEEN 10 AND 24 THEN '10-24'
        ELSE '25+'
    END AS cnt_bucket
    FROM (
        SELECT toon_id, COUNT(*) AS n
        FROM player_history_all
        GROUP BY toon_id
    ) per_player
) bucketed
GROUP BY cnt_bucket
ORDER BY cnt_bucket
""".strip()

# Probe 6: result x MMR-presence cross-tab.
PROBE_PHA_RESULT_VS_MMR_PRESENCE_QUERY: str = """
SELECT
    CASE WHEN is_mmr_missing = TRUE THEN 'unrated' ELSE 'rated' END
        AS rating_regime,
    result,
    COUNT(*) AS n
FROM player_history_all
GROUP BY 1, 2
ORDER BY 1, 2
""".strip()


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------


class RatingReconstructionAdjudicationError(RuntimeError):
    """Raised when the entrypoint halts on a fired falsifier (advisory).

    The default entrypoint returns a Result with ``passed=False`` and
    ``halting_falsifier`` set; this exception is provided for callers
    that prefer exception-driven control flow.

    Attributes:
        falsifier_key: The first fired falsifier key (priority order).
        message: Human-readable observed-vs-expected message.
    """

    def __init__(self, falsifier_key: str, message: str) -> None:
        self.falsifier_key = falsifier_key
        self.message = message
        super().__init__(f"Falsifier {falsifier_key!r} fired: {message}")


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RatingReconstructionAdjudicationDecision:
    """A single resolved Q6 successor-adjudication row.

    The CSV column order is exactly this dataclass's field order
    (33 columns total; see ``Q6_ADJUDICATION_SCHEMA``).

    Attributes:
        decision_id: One of ``Q6_DECISION_IDS``.
        parent_decision_id: Always ``"Q6_rating_policy"``.
        decision_name: Short human-readable name.
        verdict: One of ``ALLOWED_Q6_VERDICTS``.
        binding_level: One of ``ALLOWED_Q6_BINDING_LEVELS``.
        scope: Family scope literal.
        candidate_policy: One of ``Q6_RATING_POLICY_CANDIDATES`` (or
            empty for derived rows).
        selected_policy: Populated only on the ``Q6_selected_policy`` row
            (and mirrored on the per-family summary row).
        rejected_options: JSON list string of the unselected candidates
            (with per-candidate brief rejection reason) on the
            ``Q6_selected_policy`` row; empty on candidate rows.
        excluded_methods_considered: JSON list string of N-1 methods
            considered but explicitly excluded from the candidate set.
        raw_mmr_hybrid_rejection: N-2 binding string referencing the
            ``raw_mmr_where_present_plus_is_mmr_missing`` rejection
            rationale.
        rating_model_family: Algorithm-family identifier.
        rating_forward_only_constraints: Verbatim forward-only update
            wording (must reference STRICT_LT_HISTORY_FILTER for
            non-omit candidates).
        rating_cold_start_policy: G-CS-4 satisfaction wording per
            candidate.
        rating_tie_policy: Tie/draw handling wording per candidate.
        rating_hyperparameter_policy: Hyperparameter deferral wording.
        rating_evidence_level: One of ``ALLOWED_RATING_EVIDENCE_LEVELS``.
        mmr_missingness_summary: References the 83.95% / 83.65% figures.
        feature_availability_summary: Description of which families
            remain materializable (JSON dict for the summary row).
        complexity_deployability_score: One of
            ``ALLOWED_COMPLEXITY_DEPLOYABILITY``.
        leakage_risk_score: One of ``ALLOWED_LEAKAGE_RISK``.
        materialization_permission: One of
            ``ALLOWED_MATERIALIZATION_PERMISSION``.
        evidence_paths: Newline-joined repo paths + citations (>=1 for
            non-omit candidates).
        falsifiers: Newline-joined ``key:status`` pairs.
        audit_pr: Layer-2 PR number placeholder ("PR #N" until merge).
        parent_pr242_csv_sha256: Pinned PR #242 CSV SHA-256.
        parent_pr242_md_sha256: Pinned PR #242 MD SHA-256.
        parent_pr243_csv_sha256: Pinned PR #243 CSV SHA-256.
        parent_pr243_md_sha256: Pinned PR #243 MD SHA-256.
        materialized_output_paths: ALWAYS empty (no materialization).
        notes: Free-text rationale; exempt from POST-GAME token scan.
    """

    decision_id: str
    parent_decision_id: str
    decision_name: str
    verdict: str
    binding_level: str
    scope: str
    candidate_policy: str
    selected_policy: str
    rejected_options: str
    excluded_methods_considered: str
    raw_mmr_hybrid_rejection: str
    rating_model_family: str
    rating_forward_only_constraints: str
    rating_cold_start_policy: str
    rating_tie_policy: str
    rating_hyperparameter_policy: str
    rating_evidence_level: str
    mmr_missingness_summary: str
    feature_availability_summary: str
    complexity_deployability_score: str
    leakage_risk_score: str
    materialization_permission: str
    evidence_paths: str
    falsifiers: str
    audit_pr: str
    parent_pr242_csv_sha256: str
    parent_pr242_md_sha256: str
    parent_pr243_csv_sha256: str
    parent_pr243_md_sha256: str
    materialized_output_paths: str
    notes: str


@dataclass(frozen=True)
class RatingReconstructionAdjudicationResult:
    """Aggregate result of the Q6 successor adjudication.

    Attributes:
        decisions: Exactly 8 rows in ``Q6_DECISION_IDS`` order.
        csv_path: Filesystem path where the CSV was (or would be) written.
        md_path: Filesystem path where the MD was (or would be) written.
        provenance_git_sha: HEAD git SHA at run time.
        probes: Probe outputs as a JSON-serializable dict (or empty dict
            if probes were skipped).
        falsifiers_fired: Tuple of every fired falsifier key (priority
            order).
        halting_falsifier: First falsifier key that fired (or None).
        passed: True iff ``halting_falsifier is None``.
    """

    decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    csv_path: str
    md_path: str
    provenance_git_sha: str
    probes: dict[str, Any]
    falsifiers_fired: tuple[str, ...]
    halting_falsifier: str | None
    passed: bool


# ---------------------------------------------------------------------------
# CSV schema (canonical column order — must match dataclass field order)
# ---------------------------------------------------------------------------

Q6_ADJUDICATION_SCHEMA: tuple[str, ...] = tuple(
    f.name for f in fields(RatingReconstructionAdjudicationDecision)
)
Q6_ADJUDICATION_SCHEMA_COLUMN_COUNT: int = len(Q6_ADJUDICATION_SCHEMA)


# ---------------------------------------------------------------------------
# Helper-to-falsifier-key mapping (45 entries; B4 invariant)
# ---------------------------------------------------------------------------

HELPER_TO_FALSIFIER_KEY: dict[str, str] = {
    # Parent + source-file SHA pins (10 entries)
    "_check_parent_pr242_csv_sha256": "parent_pr242_csv_sha256_mismatch",
    "_check_parent_pr242_md_sha256": "parent_pr242_md_sha256_mismatch",
    "_check_parent_pr243_csv_sha256": "parent_pr243_csv_sha256_mismatch",
    "_check_parent_pr243_md_sha256": "parent_pr243_md_sha256_mismatch",
    "_check_pr241_validator_sha256": "pr241_sha256_mismatch",
    "_check_cross_02_02_spec_sha256": "cross_02_02_spec_sha256_mismatch",
    "_check_feature_family_registry_csv_sha256": (
        "feature_family_registry_csv_sha256_mismatch"
    ),
    "_check_dataset_research_log_sha256": (
        "dataset_research_log_sha256_mismatch"
    ),
    "_check_player_history_all_yaml_sha256": (
        "player_history_all_yaml_sha256_mismatch"
    ),
    "_check_matches_flat_clean_yaml_sha256": (
        "matches_flat_clean_yaml_sha256_mismatch"
    ),
    "_check_matches_history_minimal_yaml_sha256": (
        "matches_history_minimal_yaml_sha256_mismatch"
    ),
    # Candidate-set completeness (4 entries)
    "_check_q6_candidate_set_complete": "q6_candidate_set_incomplete",
    "_check_q6_omit_candidate_present": "q6_omit_candidate_missing",
    "_check_q6_deferred_candidate_present": (
        "q6_deferred_blocker_candidate_missing"
    ),
    "_check_decision_count": "decision_count_mismatch",
    # Decision-row ordering (1)
    "_check_decision_ids_canonical_order": "decision_id_order_mismatch",
    # Token-scan rejections (5)
    "_check_no_post_game_token_in_scoped_fields": (
        "q6_post_game_token_in_scoped_field"
    ),
    "_check_no_direct_target_match_outcome_reference": (
        "q6_direct_target_match_outcome_referenced"
    ),
    "_check_no_future_match_reference": "q6_future_match_leakage_referenced",
    "_check_no_global_batch_fit_reference": "q6_global_batch_fit_referenced",
    "_check_no_phase_03_baseline_creep": "q6_phase_03_baseline_creep",
    # Per-candidate methodology fields (4)
    "_check_forward_only_constraint_present_when_non_omit": (
        "q6_forward_only_constraint_missing_for_non_omit_candidate"
    ),
    "_check_cold_start_policy_present_when_non_omit": (
        "q6_cold_start_policy_missing_for_non_omit_candidate"
    ),
    "_check_tie_policy_present_when_non_omit": (
        "q6_tie_policy_missing_for_non_omit_candidate"
    ),
    "_check_hyperparameter_policy_present_when_non_omit": (
        "q6_hyperparameter_policy_missing_for_non_omit_candidate"
    ),
    # Enum validity (4)
    "_check_evidence_level_valid": "q6_evidence_level_field_invalid",
    "_check_complexity_deployability_valid": (
        "q6_complexity_deployability_invalid"
    ),
    "_check_leakage_risk_valid": "q6_leakage_risk_invalid",
    "_check_materialization_permission_valid": (
        "q6_materialization_permission_invalid"
    ),
    # External-citation discipline (1)
    "_check_external_citation_present_when_non_omit_non_deferred": (
        "q6_external_citation_missing_when_non_omit_selected"
    ),
    # MMR-missingness summary present (1)
    "_check_mmr_missingness_summary_present": (
        "q6_mmr_missingness_summary_missing"
    ),
    # Materialization-permission/verdict consistency (1)
    "_check_materialization_permission_consistent_with_verdict": (
        "q6_materialization_permission_drift"
    ),
    # Q5 non-re-adjudication (1)
    "_check_q5_not_re_adjudicated": "q6_q5_re_adjudication_drift",
    # Scope-creep guards (3)
    "_check_no_status_yaml_path_referenced": "q6_status_yaml_drift",
    "_check_no_research_log_mutation_implied": "q6_research_log_drift",
    "_check_no_roadmap_path_modified": "q6_roadmap_drift",
    # Materialization creep + universal scanner (2)
    "_check_no_materialized_output_paths_populated": "q6_materialization_creep",
    "_check_universal_tracker_source_in_history": (
        "universal_tracker_source_in_history"
    ),
    # Per-row presence (4)
    "_check_per_family_impact_summary_row_present": (
        "q6_per_family_impact_summary_missing"
    ),
    "_check_selected_policy_row_present": "q6_selected_policy_row_missing",
    "_check_selected_policy_in_candidate_set": (
        "q6_selected_policy_not_in_candidate_set"
    ),
    "_check_selected_policy_verdict_consistent": (
        "q6_selected_policy_verdict_invalid"
    ),
    "_check_per_family_impact_broadcasts_all_6_families": (
        "q6_per_family_impact_broadcast_incomplete"
    ),
    # N-1 + N-2 binding helpers (2)
    "_check_excluded_methods_considered_complete": (
        "q6_excluded_methods_considered_incomplete"
    ),
    "_check_raw_mmr_hybrid_rejection_token_present": (
        "q6_raw_mmr_hybrid_rejection_token_missing"
    ),
}


FALSIFIER_PRIORITY_CHAIN: tuple[str, ...] = (
    # SHA pins first (drift on any pinned file halts before any other check).
    "parent_pr242_csv_sha256_mismatch",
    "parent_pr242_md_sha256_mismatch",
    "parent_pr243_csv_sha256_mismatch",
    "parent_pr243_md_sha256_mismatch",
    "pr241_sha256_mismatch",
    "cross_02_02_spec_sha256_mismatch",
    "feature_family_registry_csv_sha256_mismatch",
    "dataset_research_log_sha256_mismatch",
    "player_history_all_yaml_sha256_mismatch",
    "matches_flat_clean_yaml_sha256_mismatch",
    "matches_history_minimal_yaml_sha256_mismatch",
    # Candidate-set + decision-row structural checks.
    "q6_candidate_set_incomplete",
    "q6_omit_candidate_missing",
    "q6_deferred_blocker_candidate_missing",
    "decision_count_mismatch",
    "decision_id_order_mismatch",
    # Token-scan rejections.
    "q6_post_game_token_in_scoped_field",
    "q6_direct_target_match_outcome_referenced",
    "q6_future_match_leakage_referenced",
    "q6_global_batch_fit_referenced",
    "q6_phase_03_baseline_creep",
    # Per-candidate methodology fields.
    "q6_forward_only_constraint_missing_for_non_omit_candidate",
    "q6_cold_start_policy_missing_for_non_omit_candidate",
    "q6_tie_policy_missing_for_non_omit_candidate",
    "q6_hyperparameter_policy_missing_for_non_omit_candidate",
    # Enum validity.
    "q6_evidence_level_field_invalid",
    "q6_complexity_deployability_invalid",
    "q6_leakage_risk_invalid",
    "q6_materialization_permission_invalid",
    # External-citation + MMR + permission/verdict consistency.
    "q6_external_citation_missing_when_non_omit_selected",
    "q6_mmr_missingness_summary_missing",
    "q6_materialization_permission_drift",
    # Q5 + scope-creep guards.
    "q6_q5_re_adjudication_drift",
    "q6_status_yaml_drift",
    "q6_research_log_drift",
    "q6_roadmap_drift",
    "q6_materialization_creep",
    "universal_tracker_source_in_history",
    # Per-row presence checks.
    "q6_per_family_impact_summary_missing",
    "q6_selected_policy_row_missing",
    "q6_selected_policy_not_in_candidate_set",
    "q6_selected_policy_verdict_invalid",
    "q6_per_family_impact_broadcast_incomplete",
    # N-1 + N-2.
    "q6_excluded_methods_considered_incomplete",
    "q6_raw_mmr_hybrid_rejection_token_missing",
)


# ---------------------------------------------------------------------------
# Module-import mechanical verification (B4 invariant)
# ---------------------------------------------------------------------------

assert len(HELPER_TO_FALSIFIER_KEY) == len(FALSIFIER_PRIORITY_CHAIN), (
    "B4 invariant: HELPER_TO_FALSIFIER_KEY and FALSIFIER_PRIORITY_CHAIN "
    "lengths differ"
)
assert len(set(FALSIFIER_PRIORITY_CHAIN)) == len(FALSIFIER_PRIORITY_CHAIN), (
    "B4 invariant: FALSIFIER_PRIORITY_CHAIN contains duplicate keys"
)
assert set(FALSIFIER_PRIORITY_CHAIN) == set(HELPER_TO_FALSIFIER_KEY.values()), (
    "B4 invariant: orphan or missing entries between HELPER_TO_FALSIFIER_KEY "
    "and FALSIFIER_PRIORITY_CHAIN"
)
assert len(Q6_RATING_POLICY_CANDIDATES) == Q6_RATING_POLICY_CANDIDATE_COUNT, (
    "Q6 candidate-set length invariant violated"
)
assert len(Q6_DECISION_IDS) == Q6_DECISION_COUNT, (
    "Q6 decision-id length invariant violated"
)
assert len(HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS) == 6, (
    "history_enriched_pre_game family-id length invariant violated"
)
assert len(NON_RATING_HISTORY_FAMILIES) == 5, (
    "non-rating family-id length invariant violated"
)
assert Q6_ADJUDICATION_SCHEMA_COLUMN_COUNT == 31, (
    "Q6_ADJUDICATION_SCHEMA column-count invariant violated (expected 31)"
)


# ---------------------------------------------------------------------------
# Utility helpers
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
    """Return current HEAD git SHA or ``'UNKNOWN'`` if git is unavailable.

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
        Directory containing ``pyproject.toml``.

    Raises:
        FileNotFoundError: If no ``pyproject.toml`` is found.
    """
    candidate = start.resolve()
    while candidate != candidate.parent:
        if (candidate / "pyproject.toml").exists():
            return candidate
        candidate = candidate.parent
    raise FileNotFoundError(
        f"No pyproject.toml found walking up from {start}"
    )


def _decision_to_field_dict(
    d: RatingReconstructionAdjudicationDecision,
) -> dict[str, str]:
    """Return a string-valued dict of the decision's fields.

    Args:
        d: A decision dataclass instance.

    Returns:
        Mapping of field name to stringified value.
    """
    return {f.name: str(getattr(d, f.name)) for f in fields(d)}


def _get_decision(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    decision_id: str,
) -> RatingReconstructionAdjudicationDecision | None:
    """Return the decision with the given ID, or None.

    Args:
        decisions: All 8 decisions.
        decision_id: One of ``Q6_DECISION_IDS``.

    Returns:
        The decision dataclass, or None if absent.
    """
    for d in decisions:
        if d.decision_id == decision_id:
            return d
    return None


_HEX64_REGEX: re.Pattern[str] = re.compile(r"^[0-9a-f]{64}$")


def _is_valid_sha256(s: str) -> bool:
    """Return True iff ``s`` is a 64-char lowercase hex string.

    Args:
        s: Candidate digest.

    Returns:
        True iff matches ``^[0-9a-f]{64}$``.
    """
    return bool(_HEX64_REGEX.fullmatch(s))


# ---------------------------------------------------------------------------
# Read-only DuckDB probes
# ---------------------------------------------------------------------------


def _probe_pha_result_distribution(
    con: duckdb.DuckDBPyConnection,
) -> list[tuple[str, int]]:
    """Probe 1: PHA result distribution (full table).

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        List of ``(result, n)`` rows.
    """
    rows = con.execute(PROBE_PHA_RESULT_DISTRIBUTION_QUERY).fetchall()
    return [(str(r[0]) if r[0] is not None else "", int(r[1])) for r in rows]


def _probe_pha_details_timeutc_null_rate(
    con: duckdb.DuckDBPyConnection,
) -> tuple[int, int]:
    """Probe 2: PHA details_timeUTC TRY_CAST null rate.

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        ``(total, null_after_cast)``.
    """
    row = con.execute(
        PROBE_PHA_DETAILS_TIMEUTC_TRY_CAST_NULL_RATE_QUERY
    ).fetchone()
    if row is None:
        return (0, 0)
    return (int(row[0] or 0), int(row[1] or 0))


def _probe_mfc_mmr_missing_density(
    con: duckdb.DuckDBPyConnection,
) -> tuple[int, int]:
    """Probe 3: MMR-missingness reaffirmation against MFC.

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        ``(total, mmr_missing)``.
    """
    row = con.execute(PROBE_MFC_MMR_MISSING_DENSITY_QUERY).fetchone()
    if row is None:
        return (0, 0)
    return (int(row[0] or 0), int(row[1] or 0))


def _probe_pha_mmr_missing_density(
    con: duckdb.DuckDBPyConnection,
) -> tuple[int, int]:
    """Probe 4: MMR-missingness reaffirmation against PHA.

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        ``(total, mmr_missing)``.
    """
    row = con.execute(PROBE_PHA_MMR_MISSING_DENSITY_QUERY).fetchone()
    if row is None:
        return (0, 0)
    return (int(row[0] or 0), int(row[1] or 0))


def _probe_pha_per_player_history_depth(
    con: duckdb.DuckDBPyConnection,
) -> list[tuple[str, int]]:
    """Probe 5: PHA per-player history-depth distribution.

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        List of ``(cnt_bucket, n_players)`` rows.
    """
    rows = con.execute(PROBE_PHA_PER_PLAYER_HISTORY_DEPTH_QUERY).fetchall()
    return [(str(r[0]), int(r[1])) for r in rows]


def _probe_pha_result_vs_mmr_presence(
    con: duckdb.DuckDBPyConnection,
) -> list[tuple[str, str, int]]:
    """Probe 6: result x MMR-presence cross-tab.

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        List of ``(rating_regime, result, n)`` rows.
    """
    rows = con.execute(PROBE_PHA_RESULT_VS_MMR_PRESENCE_QUERY).fetchall()
    return [
        (str(r[0]), str(r[1]) if r[1] is not None else "", int(r[2]))
        for r in rows
    ]


# ---------------------------------------------------------------------------
# Falsifier helpers — SHA pins (11)
# ---------------------------------------------------------------------------


def _check_sha_pin(
    path: Path,
    expected_sha: str,
    label: str,
) -> tuple[bool, str]:
    """Verify a pinned file SHA-256 matches the expected constant.

    Args:
        path: Path to the file to hash.
        expected_sha: Pinned expected 64-char hex digest.
        label: Short label (used in the error message).

    Returns:
        ``(did_fire, message)``.
    """
    observed = _sha256_file(path)
    if observed != expected_sha or not _is_valid_sha256(observed):
        return True, (
            f"{label} SHA-256 mismatch: observed={observed!r} "
            f"expected={expected_sha!r}"
        )
    return False, ""


def _check_parent_pr242_csv_sha256(path: Path) -> tuple[bool, str]:
    """PR #242 parent CSV SHA pin."""
    return _check_sha_pin(path, EXPECTED_PR242_CSV_SHA256, "PR #242 CSV")


def _check_parent_pr242_md_sha256(path: Path) -> tuple[bool, str]:
    """PR #242 parent MD SHA pin."""
    return _check_sha_pin(path, EXPECTED_PR242_MD_SHA256, "PR #242 MD")


def _check_parent_pr243_csv_sha256(path: Path) -> tuple[bool, str]:
    """PR #243 parent CSV SHA pin."""
    return _check_sha_pin(path, EXPECTED_PR243_CSV_SHA256, "PR #243 CSV")


def _check_parent_pr243_md_sha256(path: Path) -> tuple[bool, str]:
    """PR #243 parent MD SHA pin."""
    return _check_sha_pin(path, EXPECTED_PR243_MD_SHA256, "PR #243 MD")


def _check_pr241_validator_sha256(path: Path) -> tuple[bool, str]:
    """PR #241 validator module SHA pin."""
    return _check_sha_pin(
        path, EXPECTED_PR241_VALIDATOR_SHA256, "PR #241 validator"
    )


def _check_cross_02_02_spec_sha256(path: Path) -> tuple[bool, str]:
    """CROSS-02-02 spec SHA pin."""
    return _check_sha_pin(
        path, EXPECTED_CROSS_02_02_SPEC_SHA256, "CROSS-02-02 spec"
    )


def _check_feature_family_registry_csv_sha256(
    path: Path,
) -> tuple[bool, str]:
    """02_01_01 feature-family registry CSV SHA pin."""
    return _check_sha_pin(
        path,
        EXPECTED_FEATURE_FAMILY_REGISTRY_CSV_SHA256,
        "feature_family_registry CSV",
    )


def _check_dataset_research_log_sha256(path: Path) -> tuple[bool, str]:
    """Dataset research_log.md SHA pin."""
    return _check_sha_pin(
        path, EXPECTED_DATASET_RESEARCH_LOG_SHA256, "dataset research_log"
    )


def _check_player_history_all_yaml_sha256(
    path: Path,
) -> tuple[bool, str]:
    """player_history_all.yaml SHA pin."""
    return _check_sha_pin(
        path, EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256, "PHA YAML"
    )


def _check_matches_flat_clean_yaml_sha256(
    path: Path,
) -> tuple[bool, str]:
    """matches_flat_clean.yaml SHA pin."""
    return _check_sha_pin(
        path, EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256, "MFC YAML"
    )


def _check_matches_history_minimal_yaml_sha256(
    path: Path,
) -> tuple[bool, str]:
    """matches_history_minimal.yaml SHA pin."""
    return _check_sha_pin(
        path,
        EXPECTED_MATCHES_HISTORY_MINIMAL_YAML_SHA256,
        "MHM YAML",
    )


# ---------------------------------------------------------------------------
# Falsifier helpers — candidate-set + structural (4)
# ---------------------------------------------------------------------------


def _check_q6_candidate_set_complete(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """All 6 candidate_policy values must appear on the per-candidate rows."""
    candidate_rows = [
        d.candidate_policy for d in decisions if d.candidate_policy
    ]
    missing = [
        p for p in Q6_RATING_POLICY_CANDIDATES if p not in candidate_rows
    ]
    if missing:
        return True, (
            f"Q6 candidate set incomplete; missing: {missing}"
        )
    return False, ""


def _check_q6_omit_candidate_present(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """The ``omit_reconstructed_rating`` candidate row must exist."""
    if not any(
        d.candidate_policy == "omit_reconstructed_rating" for d in decisions
    ):
        return True, "Q6A omit_reconstructed_rating candidate row missing"
    return False, ""


def _check_q6_deferred_candidate_present(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """The Q6F deferred-with-survey candidate row must exist."""
    if not any(
        d.candidate_policy
        == "deferred_blocker_with_algorithm_survey_required"
        for d in decisions
    ):
        return True, (
            "Q6F deferred_blocker_with_algorithm_survey_required candidate "
            "row missing"
        )
    return False, ""


def _check_decision_count(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Exactly 8 decisions in ``Q6_DECISION_IDS`` order."""
    if len(decisions) != Q6_DECISION_COUNT:
        return True, (
            f"Expected exactly {Q6_DECISION_COUNT} decisions; "
            f"got {len(decisions)}"
        )
    return False, ""


def _check_decision_ids_canonical_order(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Decision rows must appear in ``Q6_DECISION_IDS`` order."""
    observed = tuple(d.decision_id for d in decisions)
    if observed != Q6_DECISION_IDS:
        return True, (
            f"Decision-ID order mismatch: got={observed} "
            f"expected={Q6_DECISION_IDS}"
        )
    return False, ""


# ---------------------------------------------------------------------------
# Falsifier helpers — token scans (5)
#
# Scoped-field discipline (mirrors PR #243 / PR #242 design):
# - Q6_SCOPED_FIELDS is an inclusion allowlist of substantive Q6
#   methodology-claim fields. ``decision_id`` is STRUCTURAL (carries the
#   row's identity literal like 'Q6B_rolling_win_rate_...') and is NOT
#   scanned because it would self-collide with token substrings.
# - Rationale-bearing fields (notes, evidence_paths, falsifiers, etc.)
#   are EXEMPT per POST_GAME_TOKEN_EXEMPT_FIELDS from PR #242: negated
#   prose like "no global batch fit" is legitimate there.
# - rating_forward_only_constraints describes the leakage-PROTECTION
#   wording per candidate; it must reference STRICT_LT_HISTORY_FILTER
#   and "forward-only" so it ALSO needs exemption to permit negated
#   leakage-protection prose.
# ---------------------------------------------------------------------------


# Substantive Q6 methodology-claim fields (inclusion allowlist).
# Exclusions are intentional:
# - decision_id / parent_decision_id / decision_name / scope:
#   structural literals (decision_id 'Q6B_rolling_win_rate_...'
#   contains the literal 'win' and would self-collide).
# - rating_forward_only_constraints / rating_cold_start_policy /
#   rating_tie_policy / rating_hyperparameter_policy: rationale-bearing
#   leakage-protection prose; negated tokens like "no global batch fit"
#   are legitimate there. They are scanned separately by the dedicated
#   _check_forward_only_constraint_present_when_non_omit /
#   _check_cold_start_policy_present_when_non_omit /
#   _check_tie_policy_present_when_non_omit /
#   _check_hyperparameter_policy_present_when_non_omit helpers for
#   REQUIRED phrasing.
# - mmr_missingness_summary / feature_availability_summary: structured
#   factual claims with no rating-policy verdict semantics.
# - All SHA fields, audit_pr, materialized_output_paths: structural.
# - rejected_options / excluded_methods_considered /
#   raw_mmr_hybrid_rejection: rationale-bearing JSON/prose listing
#   methods that were considered; negated rejection prose is the whole
#   point.
Q6_SCOPED_FIELDS_FOR_TOKEN_SCAN: frozenset[str] = frozenset(
    {
        "verdict",
        "binding_level",
        "candidate_policy",
        "selected_policy",
        "rating_model_family",
        "rating_evidence_level",
        "complexity_deployability_score",
        "leakage_risk_score",
        "materialization_permission",
    }
)


def _scoped_field_iter(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> list[tuple[str, str, str]]:
    """Yield ``(decision_id, field_name, value_lower)`` for Q6 scoped fields.

    Args:
        decisions: All decisions.

    Returns:
        List of triples (decision_id, field_name, lowercased value)
        over Q6_SCOPED_FIELDS_FOR_TOKEN_SCAN only.
    """
    out: list[tuple[str, str, str]] = []
    for d in decisions:
        row = _decision_to_field_dict(d)
        for field_name in Q6_SCOPED_FIELDS_FOR_TOKEN_SCAN:
            if field_name not in row:
                continue
            out.append((d.decision_id, field_name, str(row[field_name]).lower()))
    return out


# Word-boundary regex per POST_GAME token. The Q6 candidate set
# legitimately contains the algorithm-name token "rolling_win_rate"
# (a Bayesian-smoothed forward-only winrate baseline). Plain substring
# matching would self-collide on the literal "win" inside that name.
# Word-boundary regex (``\b`` on each side) lets "rolling_win_rate"
# pass while still rejecting genuine post-game leakage tokens
# (e.g. "win" as a standalone word, "outcome" anywhere).
_POST_GAME_TOKEN_REGEXES: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (token, re.compile(r"\b" + re.escape(token) + r"\b"))
    for token in sorted(POST_GAME_TOKENS)
)


def _check_no_post_game_token_in_scoped_fields(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """POST-GAME tokens forbidden in Q6 scoped fields (B-X1 inherited).

    Uses the canonical POST_GAME_TOKENS set imported from PR #242 (N-9
    soft binding). Scans only Q6_SCOPED_FIELDS_FOR_TOKEN_SCAN (the
    substantive Q6 methodology-claim fields); rationale-bearing fields
    like ``notes`` / ``rating_forward_only_constraints`` are exempt so
    negated prose ("no global batch fit") is legitimate there.

    Matching uses word-boundary regex (``\\b<token>\\b``) so legitimate
    algorithm-name substrings (e.g., "win" inside "rolling_win_rate")
    do not self-collide; genuine standalone leakage tokens still halt.
    """
    for did, fname, value in _scoped_field_iter(decisions):
        for token, pattern in _POST_GAME_TOKEN_REGEXES:
            if pattern.search(value):
                return True, (
                    f"POST-GAME token {token!r} in Q6 scoped field "
                    f"{fname!r} of decision {did!r} "
                    f"(value snippet={value[:80]!r})"
                )
    return False, ""


_DIRECT_OUTCOME_TOKENS: frozenset[str] = frozenset(
    {
        "target_result",
        "target_winner",
        "target_outcome",
        "target_won",
        "target_final_state",
    }
)


def _check_no_direct_target_match_outcome_reference(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Reject direct target-match outcome references in scoped fields."""
    for did, fname, value in _scoped_field_iter(decisions):
        for token in _DIRECT_OUTCOME_TOKENS:
            if token in value:
                return True, (
                    f"Direct target-match outcome token {token!r} in "
                    f"field {fname!r} of decision {did!r}"
                )
    return False, ""


_FUTURE_LEAKAGE_TOKENS: frozenset[str] = frozenset(
    {
        "future_match",
        "future_game",
        "post_match_t",
        "match_time > t",
        "history_time > target_time",
    }
)


def _check_no_future_match_reference(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Reject future-match-leakage references in scoped fields."""
    for did, fname, value in _scoped_field_iter(decisions):
        for token in _FUTURE_LEAKAGE_TOKENS:
            if token in value:
                return True, (
                    f"Future-match leakage token {token!r} in field "
                    f"{fname!r} of decision {did!r}"
                )
    return False, ""


_GLOBAL_BATCH_FIT_TOKENS: frozenset[str] = frozenset(
    {
        "global_batch_fit",
        "global fit",
        "batch fit",
        "fit on full corpus",
        "global_scaler_fit",
        "global_normalizer_fit",
    }
)


def _check_no_global_batch_fit_reference(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Reject global-batch-fit references in scoped fields."""
    for did, fname, value in _scoped_field_iter(decisions):
        for token in _GLOBAL_BATCH_FIT_TOKENS:
            if token in value:
                return True, (
                    f"Global-batch-fit token {token!r} in field "
                    f"{fname!r} of decision {did!r}"
                )
    return False, ""


_PHASE_03_BASELINE_TOKENS: frozenset[str] = frozenset(
    {
        "phase_03_baseline",
        "baseline_modeling",
        "logistic_regression_fit",
    }
)


def _check_no_phase_03_baseline_creep(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Reject Phase-03 baseline-modeling work creep in scoped fields."""
    for did, fname, value in _scoped_field_iter(decisions):
        for token in _PHASE_03_BASELINE_TOKENS:
            if token in value:
                return True, (
                    f"Phase-03 baseline-creep token {token!r} in field "
                    f"{fname!r} of decision {did!r}"
                )
    return False, ""


# ---------------------------------------------------------------------------
# Falsifier helpers — per-candidate methodology wording (4)
# ---------------------------------------------------------------------------

_NON_OMIT_NON_DEFERRED_CANDIDATES: frozenset[str] = frozenset(
    {
        "rolling_win_rate_or_bayesian_smoothed_baseline",
        "elo",
        "glicko_or_glicko_2",
        "trueskill_or_trueskill_like",
    }
)


def _is_non_omit_candidate_row(
    d: RatingReconstructionAdjudicationDecision,
) -> bool:
    """Return True iff the row is a non-omit, non-deferred candidate row."""
    return d.candidate_policy in _NON_OMIT_NON_DEFERRED_CANDIDATES


def _check_forward_only_constraint_present_when_non_omit(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Non-omit candidate rows must reference forward-only wording.

    Required substring (case-insensitive): ``strict_lt_history_filter``
    or ``forward-only`` or ``forward only``.
    """
    required = ("strict_lt_history_filter", "forward-only", "forward only")
    for d in decisions:
        if not _is_non_omit_candidate_row(d):
            continue
        value = d.rating_forward_only_constraints.lower()
        if not any(tok in value for tok in required):
            return True, (
                f"Decision {d.decision_id!r} missing forward-only "
                f"wording in rating_forward_only_constraints "
                f"(value={d.rating_forward_only_constraints!r})"
            )
    return False, ""


def _check_cold_start_policy_present_when_non_omit(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Non-omit candidate rows must reference G-CS-4 wording."""
    for d in decisions:
        if not _is_non_omit_candidate_row(d):
            continue
        if "g-cs-4" not in d.rating_cold_start_policy.lower():
            return True, (
                f"Decision {d.decision_id!r} missing 'G-CS-4' in "
                f"rating_cold_start_policy "
                f"(value={d.rating_cold_start_policy!r})"
            )
    return False, ""


def _check_tie_policy_present_when_non_omit(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Non-omit candidate rows must include a tie/draw policy field.

    Acceptable wording includes ``decisive``, ``draw``, ``tie``.
    """
    keywords = ("decisive", "draw", "tie", "no draw", "no_draw")
    for d in decisions:
        if not _is_non_omit_candidate_row(d):
            continue
        value = d.rating_tie_policy.lower()
        if not any(k in value for k in keywords):
            return True, (
                f"Decision {d.decision_id!r} missing tie/draw wording in "
                f"rating_tie_policy (value={d.rating_tie_policy!r})"
            )
    return False, ""


def _check_hyperparameter_policy_present_when_non_omit(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Non-omit candidate rows must defer hyperparameters to a separate PR."""
    for d in decisions:
        if not _is_non_omit_candidate_row(d):
            continue
        value = d.rating_hyperparameter_policy.lower()
        if "deferred" not in value or "algorithm" not in value:
            return True, (
                f"Decision {d.decision_id!r} missing 'deferred to "
                f"algorithm-implementation-proof PR' wording in "
                f"rating_hyperparameter_policy "
                f"(value={d.rating_hyperparameter_policy!r})"
            )
    return False, ""


# ---------------------------------------------------------------------------
# Falsifier helpers — enum validity (4)
# ---------------------------------------------------------------------------


def _check_evidence_level_valid(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Every row's rating_evidence_level must be in the allowed enum."""
    for d in decisions:
        if d.rating_evidence_level not in ALLOWED_RATING_EVIDENCE_LEVELS:
            return True, (
                f"Decision {d.decision_id!r} has invalid "
                f"rating_evidence_level={d.rating_evidence_level!r}"
            )
    return False, ""


def _check_complexity_deployability_valid(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Every row's complexity_deployability_score must be in the enum."""
    for d in decisions:
        if (
            d.complexity_deployability_score
            not in ALLOWED_COMPLEXITY_DEPLOYABILITY
        ):
            return True, (
                f"Decision {d.decision_id!r} has invalid "
                f"complexity_deployability_score="
                f"{d.complexity_deployability_score!r}"
            )
    return False, ""


def _check_leakage_risk_valid(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Every row's leakage_risk_score must be in the enum."""
    for d in decisions:
        if d.leakage_risk_score not in ALLOWED_LEAKAGE_RISK:
            return True, (
                f"Decision {d.decision_id!r} has invalid "
                f"leakage_risk_score={d.leakage_risk_score!r}"
            )
    return False, ""


def _check_materialization_permission_valid(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Every row's materialization_permission must be in the enum."""
    for d in decisions:
        if (
            d.materialization_permission
            not in ALLOWED_MATERIALIZATION_PERMISSION
        ):
            return True, (
                f"Decision {d.decision_id!r} has invalid "
                f"materialization_permission="
                f"{d.materialization_permission!r}"
            )
    return False, ""


# ---------------------------------------------------------------------------
# Falsifier helpers — external citation + MMR + consistency (3)
# ---------------------------------------------------------------------------


def _check_external_citation_present_when_non_omit_non_deferred(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """If Q6_selected_policy binds a non-omit non-deferred candidate, the
    Q6_selected_policy row's evidence_paths must cite at least one of the
    required algorithm citations.
    """
    selected = _get_decision(decisions, "Q6_selected_policy")
    if selected is None:
        return False, ""
    policy = selected.selected_policy
    if policy not in CANDIDATE_REQUIRED_CITATIONS:
        # omit / rolling baseline / deferred — no external citation required.
        return False, ""
    required = CANDIDATE_REQUIRED_CITATIONS[policy]
    if not any(c in selected.evidence_paths for c in required):
        return True, (
            f"Q6_selected_policy binds {policy!r} but evidence_paths "
            f"contains none of the required citations {required}"
        )
    return False, ""


_MMR_PCT_FIGURES: tuple[str, str] = ("83.95", "83.65")


def _check_mmr_missingness_summary_present(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Every candidate row's mmr_missingness_summary must reference the
    83.95% (MFC) and 83.65% (PHA) figures.
    """
    for d in decisions:
        if not d.candidate_policy:
            # Selected / summary rows may carry shorter summaries.
            continue
        value = d.mmr_missingness_summary
        if not all(p in value for p in _MMR_PCT_FIGURES):
            return True, (
                f"Decision {d.decision_id!r} mmr_missingness_summary "
                f"missing one of {_MMR_PCT_FIGURES} (value={value!r})"
            )
    return False, ""


def _check_materialization_permission_consistent_with_verdict(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """materialization_permission must align with the row's verdict.

    Rule: a ``deferred_blocker`` verdict on the selected_policy row
    requires ``blocked_pending_algorithm_survey_pr`` materialization
    permission.
    """
    selected = _get_decision(decisions, "Q6_selected_policy")
    if selected is None:
        return False, ""
    if (
        selected.verdict == "deferred_blocker"
        and selected.materialization_permission
        != "blocked_pending_algorithm_survey_pr"
    ):
        return True, (
            f"Q6_selected_policy verdict='deferred_blocker' requires "
            f"materialization_permission="
            f"'blocked_pending_algorithm_survey_pr'; got "
            f"{selected.materialization_permission!r}"
        )
    return False, ""


# ---------------------------------------------------------------------------
# Falsifier helpers — Q5 non-re-adjudication + scope-creep + misc (8)
# ---------------------------------------------------------------------------

_Q5_DRIFT_TOKENS: frozenset[str] = frozenset(
    {
        "cross_region_policy",
        "strict_exclusion",
        "dual_feature_path",
    }
)


def _check_q5_not_re_adjudicated(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q5 binding must not be touched.

    Forbids any of the Q5 verdict-bearing tokens appearing in
    verdict-bearing fields (verdict, candidate_policy, selected_policy,
    rating_model_family). Permits the tokens to appear in notes for
    reference / non-re-adjudication context.
    """
    verdict_bearing_fields = {
        "verdict",
        "candidate_policy",
        "selected_policy",
        "rating_model_family",
    }
    for d in decisions:
        row = _decision_to_field_dict(d)
        for fname in verdict_bearing_fields:
            value = row.get(fname, "").lower()
            for token in _Q5_DRIFT_TOKENS:
                if token in value:
                    return True, (
                        f"Q5-drift token {token!r} in verdict-bearing "
                        f"field {fname!r} of decision {d.decision_id!r}"
                    )
    return False, ""


_STATUS_YAML_FRAGMENTS: tuple[str, ...] = (
    "STEP_STATUS.yaml",
    "PIPELINE_SECTION_STATUS.yaml",
    "PHASE_STATUS.yaml",
)


def _check_no_status_yaml_path_referenced(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """No status YAML path may appear in scoped fields (notes exempt)."""
    for did, fname, value in _scoped_field_iter(decisions):
        for fragment in _STATUS_YAML_FRAGMENTS:
            if fragment.lower() in value:
                return True, (
                    f"Status-YAML path fragment {fragment!r} in field "
                    f"{fname!r} of decision {did!r}"
                )
    return False, ""


def _check_no_research_log_mutation_implied(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Scoped fields must not imply a research_log append."""
    forbidden = ("append to research_log", "research_log.md append")
    for did, fname, value in _scoped_field_iter(decisions):
        for tok in forbidden:
            if tok in value:
                return True, (
                    f"Research-log mutation token {tok!r} in field "
                    f"{fname!r} of decision {did!r}"
                )
    return False, ""


def _check_no_roadmap_path_modified(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Scoped fields must not imply a ROADMAP.md edit."""
    forbidden = ("roadmap.md edit", "roadmap.md append", "modify roadmap")
    for did, fname, value in _scoped_field_iter(decisions):
        for tok in forbidden:
            if tok in value:
                return True, (
                    f"ROADMAP-edit token {tok!r} in field {fname!r} "
                    f"of decision {did!r}"
                )
    return False, ""


def _check_no_materialized_output_paths_populated(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Every row's materialized_output_paths must be empty."""
    for d in decisions:
        if d.materialized_output_paths:
            return True, (
                f"Decision {d.decision_id!r} has non-empty "
                f"materialized_output_paths="
                f"{d.materialized_output_paths!r}"
            )
    return False, ""


_TRACKER_SOURCE_TOKENS: frozenset[str] = frozenset(
    {
        "tracker_events_raw",
        "tracker_events",
        "trackerevents",
    }
)


def _check_universal_tracker_source_in_history(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Tracker-events source must not appear in any scoped field.

    SC2 tracker-derived features are never pre-game features per the
    data-analysis-lineage rule. The Q6 adjudication runs over PHA only.
    """
    for did, fname, value in _scoped_field_iter(decisions):
        for tok in _TRACKER_SOURCE_TOKENS:
            if tok in value:
                return True, (
                    f"Tracker-source token {tok!r} in field {fname!r} "
                    f"of decision {did!r}"
                )
    return False, ""


def _check_per_family_impact_summary_row_present(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """The Q6_per_family_impact_summary row must exist."""
    if _get_decision(decisions, "Q6_per_family_impact_summary") is None:
        return True, "Q6_per_family_impact_summary row missing"
    return False, ""


def _check_selected_policy_row_present(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """The Q6_selected_policy row must exist."""
    if _get_decision(decisions, "Q6_selected_policy") is None:
        return True, "Q6_selected_policy row missing"
    return False, ""


def _check_selected_policy_in_candidate_set(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q6_selected_policy.selected_policy must be in the candidate set."""
    selected = _get_decision(decisions, "Q6_selected_policy")
    if selected is None:
        return False, ""
    if selected.selected_policy not in Q6_RATING_POLICY_CANDIDATES:
        return True, (
            f"Q6_selected_policy.selected_policy="
            f"{selected.selected_policy!r} not in Q6_RATING_POLICY_CANDIDATES"
        )
    return False, ""


def _check_selected_policy_verdict_consistent(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q6_selected_policy.verdict must be in the allowed-verdict enum."""
    selected = _get_decision(decisions, "Q6_selected_policy")
    if selected is None:
        return False, ""
    if selected.verdict not in ALLOWED_Q6_VERDICTS:
        return True, (
            f"Q6_selected_policy.verdict={selected.verdict!r} not in "
            f"ALLOWED_Q6_VERDICTS"
        )
    return False, ""


def _check_per_family_impact_broadcasts_all_6_families(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q6_per_family_impact_summary.feature_availability_summary must
    reference all 6 history-enriched pre_game family IDs.
    """
    summary = _get_decision(decisions, "Q6_per_family_impact_summary")
    if summary is None:
        return False, ""
    text = summary.feature_availability_summary
    missing = [f for f in HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS if f not in text]
    if missing:
        return True, (
            f"Q6_per_family_impact_summary feature_availability_summary "
            f"missing family IDs: {missing}"
        )
    return False, ""


# ---------------------------------------------------------------------------
# Falsifier helpers — N-1 + N-2 binding (2)
# ---------------------------------------------------------------------------


def _check_excluded_methods_considered_complete(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Every per-candidate row + selected_policy row must list all 3
    EXCLUDED_METHODS_CONSIDERED entries in excluded_methods_considered.
    """
    for d in decisions:
        if d.decision_id == "Q6_per_family_impact_summary":
            continue
        text = d.excluded_methods_considered
        for method in EXCLUDED_METHODS_CONSIDERED:
            if method not in text:
                return True, (
                    f"Decision {d.decision_id!r} excluded_methods_considered "
                    f"missing {method!r} (value={text!r})"
                )
    return False, ""


def _check_raw_mmr_hybrid_rejection_token_present(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """The Q6_selected_policy row's raw_mmr_hybrid_rejection field must
    reference the ``raw_mmr_where_present_plus_is_mmr_missing`` token.
    """
    selected = _get_decision(decisions, "Q6_selected_policy")
    if selected is None:
        return False, ""
    if RAW_MMR_HYBRID_REJECTION_TOKEN not in selected.raw_mmr_hybrid_rejection:
        return True, (
            f"Q6_selected_policy.raw_mmr_hybrid_rejection missing token "
            f"{RAW_MMR_HYBRID_REJECTION_TOKEN!r} "
            f"(value={selected.raw_mmr_hybrid_rejection!r})"
        )
    return False, ""


# ---------------------------------------------------------------------------
# Decision-row constructors (T05 substantive content)
# ---------------------------------------------------------------------------


def _common_fields(
    audit_pr: str,
) -> dict[str, str]:
    """Return common provenance fields shared across all rows."""
    return {
        "audit_pr": audit_pr,
        "parent_pr242_csv_sha256": EXPECTED_PR242_CSV_SHA256,
        "parent_pr242_md_sha256": EXPECTED_PR242_MD_SHA256,
        "parent_pr243_csv_sha256": EXPECTED_PR243_CSV_SHA256,
        "parent_pr243_md_sha256": EXPECTED_PR243_MD_SHA256,
        "materialized_output_paths": "",
    }


_MMR_SUMMARY: str = (
    f"MMR missing in {EXPECTED_MMR_MISSING_DENSITY_MFC_PCT}% of "
    f"matches_flat_clean rows ({EXPECTED_MFC_ROW_COUNT} total) and "
    f"{EXPECTED_MMR_MISSING_DENSITY_PHA_PCT}% of player_history_all rows "
    f"({EXPECTED_PHA_ROW_COUNT} total); is_mmr_missing flag co-registered "
    f"per CROSS-02-02 §6.2 row 'is_mmr_missing (PRE_GAME flag)' line 228."
)

_FEATURE_AVAILABILITY_OMIT: str = (
    "5 of 6 history-enriched pre_game families remain available for "
    "materialization (focal_player_history, opponent_player_history, "
    "matchup_history_aggregate, in_game_history_aggregate, "
    "cross_region_fragmentation_handling); the reconstructed_rating slot "
    "is permanently empty."
)
_FEATURE_AVAILABILITY_ALL_SIX: str = (
    "All 6 history-enriched pre_game families remain available for "
    "materialization (focal_player_history, opponent_player_history, "
    "matchup_history_aggregate, reconstructed_rating, "
    "in_game_history_aggregate, cross_region_fragmentation_handling) "
    "once the algorithm-implementation-proof PR pins hyperparameters."
)
_FEATURE_AVAILABILITY_DEFERRED: str = (
    "5 of 6 history-enriched pre_game families (focal_player_history, "
    "opponent_player_history, matchup_history_aggregate, "
    "in_game_history_aggregate, cross_region_fragmentation_handling) are "
    "blocked pending the algorithm-survey PR; reconstructed_rating itself "
    "is blocked pending Q6 upgrade from this deferred verdict."
)

_EXCLUDED_METHODS_JSON: str = json.dumps(list(EXCLUDED_METHODS_CONSIDERED))

_EXCLUDED_METHODS_PROSE: str = (
    "Methods listed in dataset research_log lines 733-734 + 961 as part "
    "of the substrate's intended backtesting universe but EXCLUDED from "
    "the Q6 candidate set per planning binding nit (b): "
    f"{', '.join(EXCLUDED_METHODS_CONSIDERED)}. Rationale: BTL and "
    "race-conditioned BTL collapse to Elo-with-race-prior in 1v1 (the "
    "sc2egset PHA scope); Neural BTL requires its own training/eval "
    "pipeline that exceeds Q6 successor-adjudication scope and would be "
    "addressed under the algorithm-survey Step if Q6F is selected. "
    "JSON list (canonical form for excluded_methods_considered field): "
    f"{_EXCLUDED_METHODS_JSON}"
)

_RAW_MMR_HYBRID_REJECTION_PROSE: str = (
    "The hybrid candidate "
    f"{RAW_MMR_HYBRID_REJECTION_TOKEN!r} -- use raw MMR for the 16.05% "
    "rated subset and cold-start the unrated 83.95% -- is REJECTED. "
    "Rationale: violates Invariant I5 symmetric-treatment because "
    "rated-vs-unrated rows would be fed asymmetric features; the "
    "rated/unrated partition is correlated with skill (tournament "
    "players over-represented in the rated 16.05% per research_log "
    "lines 1576-1626); the partition-as-feature would leak corpus "
    "structure into the model. Use is_mmr_missing flag co-registration "
    "plus the Q6-selected reconstructed_rating (or omission) instead."
)


def _build_q6a_omit(common: dict[str, str]) -> RatingReconstructionAdjudicationDecision:
    """Q6A — omit_reconstructed_rating candidate row."""
    notes = (
        "Q6A evaluates option omit_reconstructed_rating. Omission is the "
        "strongest cold-start posture: no synthetic rating is fabricated "
        "for first-match rows; G-CS-4 is trivially satisfied because "
        "no rating value is produced; the is_mmr_missing flag "
        "(CROSS-02-02 §6.2 row 'is_mmr_missing (PRE_GAME flag)' line 228) "
        "remains the primary skill-signal proxy across the 83.95% MMR-"
        "missing density. Cost: loses cross-player skill comparability; "
        "rolling-winrate features (focal_player_history, "
        "opponent_player_history) cannot distinguish 50% winrate against "
        "weak opponents from 50% winrate against strong opponents. "
        "Materialization permission for the 5 non-rating families is "
        "PRESERVED. No target-match outcome read; no future matches "
        "read; no global batch fit (vacuously). " + _EXCLUDED_METHODS_PROSE
    )
    return RatingReconstructionAdjudicationDecision(
        decision_id="Q6A_omit_reconstructed_rating",
        parent_decision_id="Q6_rating_policy",
        decision_name=(
            "Rating policy option (A) omit_reconstructed_rating -- "
            "drop the reconstructed_rating family entirely"
        ),
        verdict="deferred_recommendation",
        binding_level="recommendation_only",
        scope="sc2egset.history_enriched_pre_game.reconstructed_rating",
        candidate_policy="omit_reconstructed_rating",
        selected_policy="",
        rejected_options="",
        excluded_methods_considered=_EXCLUDED_METHODS_JSON,
        raw_mmr_hybrid_rejection=(
            f"{RAW_MMR_HYBRID_REJECTION_TOKEN}: not-applicable for "
            "Q6A because omission obviates the hybrid question; see "
            "Q6_selected_policy row for the binding rejection."
        ),
        rating_model_family="none",
        rating_forward_only_constraints="not_applicable_omitted",
        rating_cold_start_policy=(
            "G-CS-4 trivially satisfied by omission plus is_mmr_missing flag"
        ),
        rating_tie_policy="not_applicable_omitted",
        rating_hyperparameter_policy="not_applicable_omitted",
        rating_evidence_level="in_repo_only",
        mmr_missingness_summary=_MMR_SUMMARY,
        feature_availability_summary=_FEATURE_AVAILABILITY_OMIT,
        complexity_deployability_score="low",
        leakage_risk_score="not_applicable",
        materialization_permission=(
            "permitted_for_other_5_families_without_reconstructed_rating"
        ),
        evidence_paths="\n".join(
            [
                CROSS_02_02_SPEC_REL,
                FEATURE_FAMILY_REGISTRY_CSV_REL,
                DATASET_RESEARCH_LOG_REL,
                PARENT_PR242_CSV_REL,
                PARENT_PR242_MD_REL,
            ]
        ),
        falsifiers="q6_post_game_token_in_scoped_field:did_not_fire",
        notes=notes,
        **common,
    )


def _build_q6b_rolling(common: dict[str, str]) -> RatingReconstructionAdjudicationDecision:
    """Q6B — rolling_win_rate_or_bayesian_smoothed_baseline candidate row."""
    notes = (
        "Q6B evaluates option rolling_win_rate_or_bayesian_smoothed_"
        "baseline. Bayesian-smoothed forward-only win rate as a rating "
        "proxy (no opponent strength; no draws). Baseline -- not a true "
        "rating: cannot distinguish a 50% winrate against weak opponents "
        "from a 50% winrate against strong opponents. Lowest leakage "
        "surface among non-omit candidates. Already implicit in "
        "CROSS-02-02 §6.2 row 1 (focal_player_history rolling features). "
        "Per-game forward update only; no global batch fit; no target-"
        "match outcome read. " + _EXCLUDED_METHODS_PROSE
    )
    return RatingReconstructionAdjudicationDecision(
        decision_id="Q6B_rolling_win_rate_or_bayesian_smoothed_baseline",
        parent_decision_id="Q6_rating_policy",
        decision_name=(
            "Rating policy option (B) rolling_win_rate_or_bayesian_"
            "smoothed_baseline -- forward-only Bayesian-smoothed winrate"
        ),
        verdict="deferred_recommendation",
        binding_level="recommendation_only",
        scope="sc2egset.history_enriched_pre_game.reconstructed_rating",
        candidate_policy="rolling_win_rate_or_bayesian_smoothed_baseline",
        selected_policy="",
        rejected_options="",
        excluded_methods_considered=_EXCLUDED_METHODS_JSON,
        raw_mmr_hybrid_rejection=(
            f"{RAW_MMR_HYBRID_REJECTION_TOKEN}: rejected; see "
            "Q6_selected_policy row for the binding rationale."
        ),
        rating_model_family="bayesian_smoothed_rolling_win_rate",
        rating_forward_only_constraints=(
            "STRICT_LT_HISTORY_FILTER per PR #242 Q3 BIND_NOW then "
            "running beta-binomial or empirical-bayes update; "
            "forward-only per-pair update chronologically ordered by "
            "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) with ph.replay_id "
            "tiebreaker."
        ),
        rating_cold_start_policy=(
            "G-CS-4 via global prior alpha=beta=1 (Laplace) with "
            "is_first_match flag co-registered."
        ),
        rating_tie_policy=(
            "not_applicable; PHA history already decisive per PR #242 Q1 "
            "history filter (no draw handling)."
        ),
        rating_hyperparameter_policy=(
            "alpha_prior, beta_prior, window_length deferred to algorithm "
            "implementation proof PR (OQ2)."
        ),
        rating_evidence_level="in_repo_only",
        mmr_missingness_summary=_MMR_SUMMARY,
        feature_availability_summary=_FEATURE_AVAILABILITY_ALL_SIX,
        complexity_deployability_score="low",
        leakage_risk_score="low_if_forward_only_enforced",
        materialization_permission=(
            "permitted_for_all_6_families_with_pinned_hyperparameters_pr"
        ),
        evidence_paths="\n".join(
            [
                CROSS_02_02_SPEC_REL,
                FEATURE_FAMILY_REGISTRY_CSV_REL,
                DATASET_RESEARCH_LOG_REL,
                PARENT_PR242_CSV_REL,
            ]
        ),
        falsifiers="q6_post_game_token_in_scoped_field:did_not_fire",
        notes=notes,
        **common,
    )


def _build_q6c_elo(common: dict[str, str]) -> RatingReconstructionAdjudicationDecision:
    """Q6C — elo candidate row."""
    notes = (
        "Q6C evaluates option elo (Elo 1978). Simplest principled rating; "
        "forward-only per-pair update; logistic expectation; constant K. "
        "Lacks inactivity decay (vs Glicko-RD) -- a player inactive for "
        "months retains their last rating. May be a poor fit for the "
        "dataset's tournament rhythm where players appear in bursts. "
        "No target-match outcome read; no future matches read; no global "
        "batch fit. " + _EXCLUDED_METHODS_PROSE
    )
    return RatingReconstructionAdjudicationDecision(
        decision_id="Q6C_elo",
        parent_decision_id="Q6_rating_policy",
        decision_name=(
            "Rating policy option (C) elo (Elo 1978) -- "
            "constant-K forward-only Elo update"
        ),
        verdict="deferred_recommendation",
        binding_level="recommendation_only",
        scope="sc2egset.history_enriched_pre_game.reconstructed_rating",
        candidate_policy="elo",
        selected_policy="",
        rejected_options="",
        excluded_methods_considered=_EXCLUDED_METHODS_JSON,
        raw_mmr_hybrid_rejection=(
            f"{RAW_MMR_HYBRID_REJECTION_TOKEN}: rejected; see "
            "Q6_selected_policy row for the binding rationale."
        ),
        rating_model_family="elo_per_toon_id_grouped",
        rating_forward_only_constraints=(
            "STRICT_LT_HISTORY_FILTER then per-pair forward update "
            "chronologically ordered by TRY_CAST(ph.details_timeUTC AS "
            "TIMESTAMP) with ph.replay_id tiebreaker; forward-only "
            "(no global batch fit)."
        ),
        rating_cold_start_policy=(
            "G-CS-4 via literature prior rating=1500 for first-match "
            "rows with is_first_match flag co-registered."
        ),
        rating_tie_policy=(
            "decisive only; PHA history already decisive per PR #242 Q1; "
            "no explicit draw handling."
        ),
        rating_hyperparameter_policy=(
            "K_factor and initial_rating deferred to algorithm "
            "implementation proof PR (OQ2)."
        ),
        rating_evidence_level="in_repo_plus_citation",
        mmr_missingness_summary=_MMR_SUMMARY,
        feature_availability_summary=_FEATURE_AVAILABILITY_ALL_SIX,
        complexity_deployability_score="low",
        leakage_risk_score="low_if_forward_only_enforced",
        materialization_permission=(
            "permitted_for_all_6_families_with_pinned_hyperparameters_pr"
        ),
        evidence_paths="\n".join(
            [
                CROSS_02_02_SPEC_REL,
                FEATURE_FAMILY_REGISTRY_CSV_REL,
                DATASET_RESEARCH_LOG_REL,
                PARENT_PR242_CSV_REL,
                CITATION_ELO_1978,
            ]
        ),
        falsifiers="q6_post_game_token_in_scoped_field:did_not_fire",
        notes=notes,
        **common,
    )


def _build_q6d_glicko(common: dict[str, str]) -> RatingReconstructionAdjudicationDecision:
    """Q6D — glicko_or_glicko_2 candidate row (spec-favoured path)."""
    notes = (
        "Q6D evaluates option glicko_or_glicko_2 (Glickman 1999, 2012). "
        "CROSS-02-02 §6.2 row 4 line 241 names 'Glicko-2 or analogous' "
        "first -- this is the spec-favoured path. Adds rating deviation "
        "(RD) that grows with inactivity -- matches the dataset's "
        "tournament rhythm where players appear in bursts. Glicko-2 "
        "additionally tracks rating volatility sigma. Rating-period "
        "batching is a within-period micro-leakage surface that must be "
        "carefully bounded; recorded honestly as medium leakage risk. "
        "No target-match outcome read; no future matches read; no global "
        "batch fit. " + _EXCLUDED_METHODS_PROSE
    )
    return RatingReconstructionAdjudicationDecision(
        decision_id="Q6D_glicko_or_glicko_2",
        parent_decision_id="Q6_rating_policy",
        decision_name=(
            "Rating policy option (D) glicko_or_glicko_2 "
            "(Glickman 1999, 2012) -- forward-only with RD inactivity decay"
        ),
        verdict="deferred_recommendation",
        binding_level="recommendation_only",
        scope="sc2egset.history_enriched_pre_game.reconstructed_rating",
        candidate_policy="glicko_or_glicko_2",
        selected_policy="",
        rejected_options="",
        excluded_methods_considered=_EXCLUDED_METHODS_JSON,
        raw_mmr_hybrid_rejection=(
            f"{RAW_MMR_HYBRID_REJECTION_TOKEN}: rejected; see "
            "Q6_selected_policy row for the binding rationale."
        ),
        rating_model_family="glicko_or_glicko_2_per_toon_id_grouped",
        rating_forward_only_constraints=(
            "STRICT_LT_HISTORY_FILTER then per-rating-period batched "
            "update internally; the rating period itself is a "
            "hyperparameter (deferred); forward-only (no global batch "
            "fit) across rating periods."
        ),
        rating_cold_start_policy=(
            "G-CS-4 via literature prior mu=1500, RD=350, sigma=0.06 "
            "for first-match rows with is_first_match flag co-registered "
            "(Glicko-2 defaults; final values deferred)."
        ),
        rating_tie_policy=(
            "decisive only; PHA history already decisive per PR #242 Q1; "
            "draw score 0.5 not used."
        ),
        rating_hyperparameter_policy=(
            "mu_prior, RD_prior, sigma_prior, tau, rating_period_days "
            "deferred to algorithm implementation proof PR (OQ2)."
        ),
        rating_evidence_level="in_repo_plus_citation",
        mmr_missingness_summary=_MMR_SUMMARY,
        feature_availability_summary=_FEATURE_AVAILABILITY_ALL_SIX,
        complexity_deployability_score="medium",
        leakage_risk_score="medium_if_forward_only_enforced",
        materialization_permission=(
            "permitted_for_all_6_families_with_pinned_hyperparameters_pr"
        ),
        evidence_paths="\n".join(
            [
                CROSS_02_02_SPEC_REL,
                FEATURE_FAMILY_REGISTRY_CSV_REL,
                DATASET_RESEARCH_LOG_REL,
                PARENT_PR242_CSV_REL,
                CITATION_GLICKMAN_1999,
                CITATION_GLICKMAN_2012,
            ]
        ),
        falsifiers="q6_post_game_token_in_scoped_field:did_not_fire",
        notes=notes,
        **common,
    )


def _build_q6e_trueskill(
    common: dict[str, str],
) -> RatingReconstructionAdjudicationDecision:
    """Q6E — trueskill_or_trueskill_like candidate row."""
    notes = (
        "Q6E evaluates option trueskill_or_trueskill_like "
        "(Herbrich, Minka, Graepel 2006). Gaussian skill prior; "
        "factor-graph message passing; handles multi-player FFA but "
        "degenerates to Elo-like for 1v1 -- the marginal expressiveness "
        "gain for sc2egset's 1v1-decisive PHA scope may not justify the "
        "Bayesian factor-graph implementation cost. Mature libraries "
        "exist (e.g., trueskill PyPI package) but the implementation "
        "complexity exceeds Glicko-2 for limited 1v1 payoff. No target-"
        "match outcome read; no future matches read; no global batch "
        "fit. " + _EXCLUDED_METHODS_PROSE
    )
    return RatingReconstructionAdjudicationDecision(
        decision_id="Q6E_trueskill_or_trueskill_like",
        parent_decision_id="Q6_rating_policy",
        decision_name=(
            "Rating policy option (E) trueskill_or_trueskill_like "
            "(Herbrich, Minka, Graepel 2006) -- forward-only Bayesian "
            "skill rating"
        ),
        verdict="deferred_recommendation",
        binding_level="recommendation_only",
        scope="sc2egset.history_enriched_pre_game.reconstructed_rating",
        candidate_policy="trueskill_or_trueskill_like",
        selected_policy="",
        rejected_options="",
        excluded_methods_considered=_EXCLUDED_METHODS_JSON,
        raw_mmr_hybrid_rejection=(
            f"{RAW_MMR_HYBRID_REJECTION_TOKEN}: rejected; see "
            "Q6_selected_policy row for the binding rationale."
        ),
        rating_model_family=(
            "trueskill_2006_1v1_subset_or_trueskill_through_time_per_"
            "toon_id_grouped"
        ),
        rating_forward_only_constraints=(
            "STRICT_LT_HISTORY_FILTER then per-rating-period forward "
            "Gaussian message-passing posterior update; forward-only "
            "(no global batch fit)."
        ),
        rating_cold_start_policy=(
            "G-CS-4 via literature prior mu=25, sigma=25/3 for first-"
            "match rows with is_first_match flag co-registered "
            "(TrueSkill defaults; final values deferred)."
        ),
        rating_tie_policy=(
            "decisive only; PHA history already decisive per PR #242 Q1; "
            "draw margin zero or minimal."
        ),
        rating_hyperparameter_policy=(
            "mu_prior, sigma_prior, beta, tau, draw_margin deferred to "
            "algorithm implementation proof PR (OQ2)."
        ),
        rating_evidence_level="in_repo_plus_citation",
        mmr_missingness_summary=_MMR_SUMMARY,
        feature_availability_summary=_FEATURE_AVAILABILITY_ALL_SIX,
        complexity_deployability_score="high",
        leakage_risk_score="medium_if_forward_only_enforced",
        materialization_permission=(
            "permitted_for_all_6_families_with_pinned_hyperparameters_pr"
        ),
        evidence_paths="\n".join(
            [
                CROSS_02_02_SPEC_REL,
                FEATURE_FAMILY_REGISTRY_CSV_REL,
                DATASET_RESEARCH_LOG_REL,
                PARENT_PR242_CSV_REL,
                CITATION_HERBRICH_MINKA_GRAEPEL_2006,
            ]
        ),
        falsifiers="q6_post_game_token_in_scoped_field:did_not_fire",
        notes=notes,
        **common,
    )


def _build_q6f_deferred(
    common: dict[str, str],
) -> RatingReconstructionAdjudicationDecision:
    """Q6F — deferred_blocker_with_algorithm_survey_required candidate row."""
    notes = (
        "Q6F evaluates option deferred_blocker_with_algorithm_survey_"
        "required. This is the 'punt with rigour' verdict: comparative "
        "empirical evidence (back-testing AUC / log-loss on the unrated "
        "regime) does NOT exist in any prior artifact and would require "
        "its own algorithm-survey Step. Selecting Q6F preserves "
        "Invariant I7 (no magic numbers for K, prior, RD, sigma, tau, "
        "rating_period) -- a legitimate Q6 verdict per planning N-10, "
        "NOT a planning failure. The survey would back-test all 4 "
        "non-trivial families (B/C/D/E) plus the excluded BTL family "
        "from a separate Step. Forward-only / cold-start / leakage "
        "constraints are binding in advance: any candidate evaluated "
        "by the survey must honour them. No target-match outcome read; "
        "no future matches read; no global batch fit. "
        + _EXCLUDED_METHODS_PROSE
    )
    return RatingReconstructionAdjudicationDecision(
        decision_id="Q6F_deferred_with_algorithm_survey",
        parent_decision_id="Q6_rating_policy",
        decision_name=(
            "Rating policy option (F) deferred_blocker_with_algorithm_"
            "survey_required -- 'punt with rigour' verdict per N-10"
        ),
        verdict="deferred_blocker",
        binding_level="deferred_blocker",
        scope="sc2egset.history_enriched_pre_game.reconstructed_rating",
        candidate_policy="deferred_blocker_with_algorithm_survey_required",
        selected_policy="",
        rejected_options="",
        excluded_methods_considered=_EXCLUDED_METHODS_JSON,
        raw_mmr_hybrid_rejection=(
            f"{RAW_MMR_HYBRID_REJECTION_TOKEN}: rejected; see "
            "Q6_selected_policy row for the binding rationale."
        ),
        rating_model_family="to_be_determined_after_algorithm_survey_step",
        rating_forward_only_constraints=(
            "binding in advance: STRICT_LT_HISTORY_FILTER; no global "
            "batch fit; no target-match outcome read; no future-match "
            "read; the algorithm-survey Step must honour these for "
            "every candidate evaluated. Forward-only."
        ),
        rating_cold_start_policy=(
            "G-CS-4 binding in advance for every candidate evaluated by "
            "the future algorithm-survey Step."
        ),
        rating_tie_policy=(
            "decisive only; PHA history already decisive per PR #242 Q1."
        ),
        rating_hyperparameter_policy=(
            "deferred pending algorithm-survey Step and a downstream "
            "algorithm-implementation-proof PR (OQ2)."
        ),
        rating_evidence_level="deferred",
        mmr_missingness_summary=_MMR_SUMMARY,
        feature_availability_summary=_FEATURE_AVAILABILITY_DEFERRED,
        complexity_deployability_score="not_applicable",
        leakage_risk_score="not_applicable",
        materialization_permission="blocked_pending_algorithm_survey_pr",
        evidence_paths="\n".join(
            [
                CROSS_02_02_SPEC_REL,
                FEATURE_FAMILY_REGISTRY_CSV_REL,
                DATASET_RESEARCH_LOG_REL,
                PARENT_PR242_CSV_REL,
                PARENT_PR242_MD_REL,
            ]
        ),
        falsifiers=(
            "q6_post_game_token_in_scoped_field:did_not_fire"
        ),
        notes=(
            "deferred_blocker because: comparative empirical evidence "
            "to bind a single rating-model family does not exist in any "
            "prior artifact and would require its own algorithm-survey "
            "Step. " + notes
        ),
        **common,
    )


def _build_q6_selected_policy(
    common: dict[str, str],
) -> RatingReconstructionAdjudicationDecision:
    """Q6_selected_policy — BINDING row.

    Selected verdict: Q6F (deferred-with-survey) per planning T05's
    "default recommendation if you cannot conclusively bind a winner."
    """
    rejected_list = [
        {
            "candidate": "omit_reconstructed_rating",
            "reason": (
                "rejected as the binding selection because permanent "
                "omission forecloses the rating signal in any future "
                "Step; the algorithm-survey Step may yet find that "
                "Glicko-2 or rolling-baseline materially helps. "
                "Recommended only as a contingency if the survey "
                "concludes no candidate clears the noise floor."
            ),
        },
        {
            "candidate": "rolling_win_rate_or_bayesian_smoothed_baseline",
            "reason": (
                "rejected as the binding selection because it is a "
                "baseline (no opponent strength) rather than a true "
                "rating; back-testing against opponent-strength-aware "
                "candidates (Elo / Glicko / TrueSkill) is required "
                "before binding."
            ),
        },
        {
            "candidate": "elo",
            "reason": (
                "rejected as the binding selection because Elo lacks "
                "inactivity decay (vs Glicko-RD) and the dataset's "
                "tournament rhythm penalises this; back-testing "
                "required to confirm or refute this prior."
            ),
        },
        {
            "candidate": "glicko_or_glicko_2",
            "reason": (
                "rejected as the binding selection NOT on methodology "
                "grounds (this is the §6.2 row 4 spec-favoured path) "
                "but on evidence grounds: no comparative back-testing "
                "AUC / log-loss exists in any prior artifact. "
                "Recommended favourite for the algorithm-survey Step."
            ),
        },
        {
            "candidate": "trueskill_or_trueskill_like",
            "reason": (
                "rejected as the binding selection because TrueSkill "
                "degenerates to Glicko-like for 1v1; marginal "
                "expressiveness gain may not justify the Bayesian "
                "factor-graph implementation cost."
            ),
        },
    ]
    rejected_options = json.dumps(rejected_list)
    notes = (
        "Q6_selected_policy is the BINDING row for the Q6 successor "
        "adjudication. Selected: Q6F_deferred_with_algorithm_survey "
        "(deferred_blocker_with_algorithm_survey_required). Rationale: "
        "comparative back-testing AUC / log-loss evidence among the 4 "
        "non-trivial candidates (B/C/D/E) does NOT exist in any prior "
        "artifact; binding a single family without this evidence would "
        "violate Invariant I7 ('no magic numbers' applied to model-"
        "family choice). Per planning N-10, selecting Q6F is a "
        "legitimate verdict, NOT a planning failure -- it preserves "
        "I7 and triggers a dedicated algorithm-survey Step that will "
        "back-test the candidates over the unrated regime. "
        "Materialization permission: blocked_pending_algorithm_survey_pr "
        "(the future Layer-3 materialization PR must NOT proceed until "
        "the algorithm-survey Step resolves the selection). "
        "Q5 binding from PR #243 (Q5_selected_policy="
        f"{Q5_SELECTED_POLICY}, verdict={Q5_SELECTED_POLICY_VERDICT}) "
        "is preserved verbatim and not re-adjudicated. "
        + _RAW_MMR_HYBRID_REJECTION_PROSE
        + " "
        + _EXCLUDED_METHODS_PROSE
    )
    return RatingReconstructionAdjudicationDecision(
        decision_id="Q6_selected_policy",
        parent_decision_id="Q6_rating_policy",
        decision_name=(
            "Q6 rating policy selection (BINDING row; verdict emerges "
            "from per-candidate evidence table)"
        ),
        verdict="deferred_blocker",
        binding_level="deferred_blocker",
        scope="sc2egset.history_enriched_pre_game.reconstructed_rating",
        candidate_policy="",
        selected_policy="deferred_blocker_with_algorithm_survey_required",
        rejected_options=rejected_options,
        excluded_methods_considered=_EXCLUDED_METHODS_JSON,
        raw_mmr_hybrid_rejection=_RAW_MMR_HYBRID_REJECTION_PROSE,
        rating_model_family="to_be_determined_after_algorithm_survey_step",
        rating_forward_only_constraints=(
            "binding in advance on every candidate the algorithm-survey "
            "Step evaluates: STRICT_LT_HISTORY_FILTER; no global batch "
            "fit; no target-match outcome read; no future-match read; "
            "forward-only per-pair update."
        ),
        rating_cold_start_policy=(
            "G-CS-4 binding in advance on every candidate evaluated."
        ),
        rating_tie_policy=(
            "decisive only; PHA history already decisive per PR #242 Q1."
        ),
        rating_hyperparameter_policy=(
            "deferred pending algorithm-survey Step and the downstream "
            "algorithm-implementation-proof PR (OQ2)."
        ),
        rating_evidence_level="deferred",
        mmr_missingness_summary=_MMR_SUMMARY,
        feature_availability_summary=_FEATURE_AVAILABILITY_DEFERRED,
        complexity_deployability_score="not_applicable",
        leakage_risk_score="not_applicable",
        materialization_permission="blocked_pending_algorithm_survey_pr",
        evidence_paths="\n".join(
            [
                CROSS_02_02_SPEC_REL,
                FEATURE_FAMILY_REGISTRY_CSV_REL,
                DATASET_RESEARCH_LOG_REL,
                PARENT_PR242_CSV_REL,
                PARENT_PR242_MD_REL,
                PARENT_PR243_CSV_REL,
                PARENT_PR243_MD_REL,
            ]
        ),
        falsifiers=(
            "q6_post_game_token_in_scoped_field:did_not_fire\n"
            "q6_q5_re_adjudication_drift:did_not_fire\n"
            "q6_materialization_creep:did_not_fire"
        ),
        notes=notes,
        **common,
    )


def _build_q6_per_family_summary(
    common: dict[str, str],
) -> RatingReconstructionAdjudicationDecision:
    """Q6_per_family_impact_summary — derived broadcast row."""
    family_impact = {
        f: {
            "affected_by_q6": "yes" if f == "reconstructed_rating" else "no",
            "materialization_status": (
                "blocked_pending_algorithm_survey_pr"
                if f == "reconstructed_rating"
                else "blocked_pending_algorithm_survey_pr_per_q6f_selected"
            ),
        }
        for f in HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS
    }
    feature_availability = json.dumps(family_impact)
    notes = (
        "Q6_per_family_impact_summary is the derived per-family broadcast "
        "row mirroring PR #243's Q5_per_family_impact_summary pattern. "
        "Q6 strictly affects only the reconstructed_rating family; the "
        "other 5 families' materialization is blocked downstream of the "
        "Q6F deferred verdict (the entire 6-family tranche is blocked "
        "pending the algorithm-survey PR because the planning Assumption "
        "11 binding bundles the 6 families). If a future plan elects to "
        "decouple the 5 non-rating families and materialize them under a "
        "scope-narrowing Step (per OQ1), this summary row's status "
        "values would change. " + Q5_NON_RE_ADJUDICATION_PHRASE
    )
    return RatingReconstructionAdjudicationDecision(
        decision_id="Q6_per_family_impact_summary",
        parent_decision_id="Q6_rating_policy",
        decision_name=(
            "Q6 per-family impact summary (derived row; broadcasts the "
            "Q6 selected_policy decision over the 6 history-enriched "
            "pre_game families)"
        ),
        verdict="recommendation_only",
        binding_level="recommendation_only",
        scope="all_six_history_enriched_pre_game_families",
        candidate_policy="",
        selected_policy="deferred_blocker_with_algorithm_survey_required",
        rejected_options="",
        excluded_methods_considered=_EXCLUDED_METHODS_JSON,
        raw_mmr_hybrid_rejection=(
            f"{RAW_MMR_HYBRID_REJECTION_TOKEN}: rejection inherited from "
            "Q6_selected_policy row."
        ),
        rating_model_family="not_applicable_per_family_summary_row",
        rating_forward_only_constraints=(
            "not_applicable_per_family_summary_row"
        ),
        rating_cold_start_policy="not_applicable_per_family_summary_row",
        rating_tie_policy="not_applicable_per_family_summary_row",
        rating_hyperparameter_policy="not_applicable_per_family_summary_row",
        rating_evidence_level="deferred",
        mmr_missingness_summary=_MMR_SUMMARY,
        feature_availability_summary=feature_availability,
        complexity_deployability_score="not_applicable",
        leakage_risk_score="not_applicable",
        materialization_permission="blocked_pending_algorithm_survey_pr",
        evidence_paths="\n".join(
            [
                CROSS_02_02_SPEC_REL,
                FEATURE_FAMILY_REGISTRY_CSV_REL,
                DATASET_RESEARCH_LOG_REL,
                PARENT_PR242_CSV_REL,
                PARENT_PR243_CSV_REL,
            ]
        ),
        falsifiers="q6_per_family_impact_broadcast_incomplete:did_not_fire",
        notes=notes,
        **common,
    )


Q5_NON_RE_ADJUDICATION_PHRASE: str = (
    "Q5 binding from PR #243 "
    f"(Q5_selected_policy={Q5_SELECTED_POLICY}, "
    f"verdict={Q5_SELECTED_POLICY_VERDICT}) is preserved verbatim and "
    "not re-adjudicated."
)


def _build_decisions(
    common: dict[str, str],
) -> tuple[RatingReconstructionAdjudicationDecision, ...]:
    """Build the 8 Q6 decision rows in canonical order."""
    return (
        _build_q6a_omit(common),
        _build_q6b_rolling(common),
        _build_q6c_elo(common),
        _build_q6d_glicko(common),
        _build_q6e_trueskill(common),
        _build_q6f_deferred(common),
        _build_q6_selected_policy(common),
        _build_q6_per_family_summary(common),
    )


# ---------------------------------------------------------------------------
# CSV + MD writers (byte-deterministic)
# ---------------------------------------------------------------------------


def _write_csv(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    csv_path: Path,
) -> None:
    """Write the deterministic Q6 successor adjudication CSV.

    Args:
        decisions: 8 decision rows in ``Q6_DECISION_IDS`` order.
        csv_path: Destination path.
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(Q6_ADJUDICATION_SCHEMA))
        writer.writeheader()
        for d in decisions:
            writer.writerow(_decision_to_field_dict(d))
    LOGGER.debug(
        "_write_csv: wrote %d rows to %s", len(decisions), csv_path
    )


def _md_decision_section(
    d: RatingReconstructionAdjudicationDecision,
) -> str:
    """Format one decision row as a markdown section."""
    parts: list[str] = []
    parts.append(f"### {d.decision_id} -- {d.decision_name}\n\n")
    parts.append(f"- **Verdict:** `{d.verdict}`\n")
    parts.append(f"- **Binding level:** `{d.binding_level}`\n")
    parts.append(f"- **Scope:** `{d.scope}`\n")
    parts.append(
        f"- **Candidate policy:** `{d.candidate_policy or '(derived row)'}`\n"
    )
    parts.append(
        f"- **Selected policy:** `{d.selected_policy or '(per-candidate row)'}`\n"
    )
    parts.append(
        f"- **Rating model family:** `{d.rating_model_family}`\n"
    )
    parts.append(
        f"- **Rating evidence level:** `{d.rating_evidence_level}`\n"
    )
    parts.append(
        f"- **Complexity / deployability:** `{d.complexity_deployability_score}`\n"
    )
    parts.append(f"- **Leakage risk:** `{d.leakage_risk_score}`\n")
    parts.append(
        f"- **Materialization permission:** `{d.materialization_permission}`\n\n"
    )
    parts.append(
        f"**Forward-only constraints:** {d.rating_forward_only_constraints}\n\n"
    )
    parts.append(
        f"**Cold-start policy (G-CS-4):** {d.rating_cold_start_policy}\n\n"
    )
    parts.append(f"**Tie policy:** {d.rating_tie_policy}\n\n")
    parts.append(
        f"**Hyperparameter policy:** {d.rating_hyperparameter_policy}\n\n"
    )
    parts.append(f"**MMR missingness summary:** {d.mmr_missingness_summary}\n\n")
    parts.append(
        f"**Feature availability summary:**\n\n"
        f"```json\n{d.feature_availability_summary}\n```\n\n"
    )
    parts.append(
        f"**Excluded methods considered (N-1):**\n\n"
        f"```json\n{d.excluded_methods_considered}\n```\n\n"
    )
    parts.append(
        f"**Raw-MMR-hybrid rejection (N-2):** {d.raw_mmr_hybrid_rejection}\n\n"
    )
    if d.rejected_options:
        parts.append(
            f"**Rejected options:**\n\n```json\n{d.rejected_options}\n```\n\n"
        )
    parts.append(f"**Rationale / notes:**\n\n{d.notes}\n\n")
    parts.append(f"**Evidence paths:**\n\n```\n{d.evidence_paths}\n```\n\n")
    parts.append(f"**Falsifiers (row-level):**\n\n```\n{d.falsifiers}\n```\n\n")
    return "".join(parts)


def _write_md(
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...],
    md_path: Path,
    falsifier_status: dict[str, str],
    probes: dict[str, Any],
) -> None:
    """Write the Q6 successor adjudication MD companion artifact.

    Args:
        decisions: 8 decision rows.
        md_path: Destination path.
        falsifier_status: Mapping of falsifier key to ``did_fire`` /
            ``did_not_fire``.
        probes: Probe outputs (may be empty if probes were skipped).
    """
    md_path.parent.mkdir(parents=True, exist_ok=True)
    parts: list[str] = []
    parts.append(
        "# SC2EGSet Step 02_01_03 -- Q6 Rating-Reconstruction Successor "
        "Adjudication\n\n"
    )

    parts.append("## §1 Non-Materialization Disclaimer\n\n")
    parts.append(
        "This artifact is a Q6 successor adjudication of the "
        "`reconstructed_rating` family's rating-policy choice for "
        "sc2egset Step 02_01_03. It does NOT materialize any rating "
        "value, does NOT write any Parquet, does NOT run the "
        "CROSS-02-01-v1.0.1 post-materialization leakage audit, does "
        "NOT close Step 02_01_03, and does NOT append to any status "
        "YAML or research_log. Materialization is BLOCKED pending the "
        "algorithm-survey PR named by the Q6_selected_policy row.\n\n"
    )

    parts.append("## §2 Parent PR #242 Lineage\n\n")
    parts.append(
        "This artifact upgrades the PR #242 parent adjudication's Q6 "
        "row (`Q6_rating_policy`, which closed as "
        "`verdict=deferred_blocker`). Verbatim Q6 rationale from PR "
        "#242 (`02_01_03_history_source_anchor_coldstart_adjudication"
        ".md` §Q6 row): "
        "'deferred_blocker because: per N3, ~83.95% MMR-missing "
        "density (verified in the dataset research log; consistent "
        "with the registry CSV is_mmr_missing_flag family) makes "
        "algorithm choice first-order. Pinning Elo / Glicko / Glicko-2 "
        "/ TrueSkill / a rolling-winrate baseline without empirical "
        "evidence of which family handles the unrated / no-rating-"
        "history regime best would violate Invariant I7. Four "
        "candidate citations exist (Elo 1978; Glickman 1999; Glickman "
        "2012; Herbrich, Minka, Graepel 2006) but binding one over the "
        "others requires repo evidence not yet generated.' "
        "PR #242 byte-stable artifacts are referenced by SHA-256 on "
        "every row (`parent_pr242_csv_sha256`, "
        "`parent_pr242_md_sha256`). Pinned SHAs:\n\n"
        f"- PR #242 CSV: `{EXPECTED_PR242_CSV_SHA256}`\n"
        f"- PR #242 MD: `{EXPECTED_PR242_MD_SHA256}`\n\n"
    )

    parts.append("## §3 Parent PR #243 Lineage (Q5 Preserved)\n\n")
    parts.append(
        "Q5 (`cross_region_fragmentation_handling`) was resolved by "
        f"PR #243 with `Q5_selected_policy={Q5_SELECTED_POLICY}`, "
        f"verdict `{Q5_SELECTED_POLICY_VERDICT}`. This artifact does "
        "NOT re-adjudicate Q5. The `q6_q5_re_adjudication_drift` "
        "falsifier halts the entrypoint before write if any row "
        "carries a Q5 verdict-bearing token in a verdict-bearing "
        "field. Pinned SHAs:\n\n"
        f"- PR #243 CSV: `{EXPECTED_PR243_CSV_SHA256}`\n"
        f"- PR #243 MD: `{EXPECTED_PR243_MD_SHA256}`\n\n"
    )

    parts.append("## §4 Q6-Only Scope Statement\n\n")
    parts.append(
        "Scope: select one of the 6 `Q6_RATING_POLICY_CANDIDATES` "
        "(or re-defer with rigour) for the `reconstructed_rating` "
        "family. Out of scope: any materialization, any algorithm "
        "benchmark, any race-conditioned BTL / Bradley-Terry / Neural "
        "BTL (recorded in §5 as 'excluded methods considered' per "
        "N-1), any raw-MMR-where-present hybrid (rejected in §5 per "
        "N-2), any Q5 re-adjudication, any Q1-Q4 / Q7 / Q8 re-"
        "adjudication, any Step 02_01_03 closure, any Step 02_01_04 "
        "start, any Phase 03 work, any cross-dataset (aoe2, aoestats, "
        "aoe2companion) work.\n\n"
    )

    parts.append("## §5 Per-Candidate Decision Table\n\n")
    parts.append(
        "| decision_id | candidate_policy | verdict | "
        "rating_evidence_level | complexity | leakage_risk | "
        "materialization_permission |\n"
    )
    parts.append("|---|---|---|---|---|---|---|\n")
    for d in decisions:
        if not d.candidate_policy:
            continue
        parts.append(
            f"| `{d.decision_id}` | `{d.candidate_policy}` | "
            f"`{d.verdict}` | `{d.rating_evidence_level}` | "
            f"`{d.complexity_deployability_score}` | "
            f"`{d.leakage_risk_score}` | "
            f"`{d.materialization_permission}` |\n"
        )
    parts.append("\n### §5.1 Excluded Methods Considered (N-1 binding)\n\n")
    parts.append(
        "Methods listed in the dataset's `research_log.md` (lines "
        "733-734 and 961) as part of the intended backtesting universe "
        "but EXPLICITLY EXCLUDED from the Q6 candidate set per planning "
        "binding nit (b):\n\n"
    )
    for m in EXCLUDED_METHODS_CONSIDERED:
        parts.append(f"- `{m}`\n")
    parts.append(
        "\n**Rationale.** BTL and race-conditioned BTL collapse to "
        "Elo-with-race-prior in 1v1 (the sc2egset PHA scope is 1v1-"
        "decisive). Neural BTL requires its own training/eval pipeline "
        "that exceeds Q6 successor-adjudication scope and would be "
        "addressed under the algorithm-survey Step if Q6F is selected. "
        "These methods are NOT extended into `Q6_RATING_POLICY_"
        "CANDIDATES`; they are recorded in every row's "
        "`excluded_methods_considered` field (JSON form) so the "
        "examination defense trail is preserved.\n\n"
    )
    parts.append(
        "### §5.2 Raw-MMR-where-present hybrid rejection (N-2 binding)\n\n"
    )
    parts.append(
        f"The hybrid candidate `{RAW_MMR_HYBRID_REJECTION_TOKEN}` "
        "(use raw MMR for the 16.05% rated subset; cold-start the "
        "remaining 83.95%) is REJECTED. Rationale: violates Invariant "
        "I5 symmetric-treatment because rated-vs-unrated rows would be "
        "fed asymmetric features; the rated/unrated partition is "
        "correlated with skill (tournament players over-represented in "
        "the rated 16.05% per research_log lines 1576-1626); the "
        "partition-as-feature would leak corpus structure into the "
        "model. The N-2 rejection token is carried verbatim in the "
        "`raw_mmr_hybrid_rejection` field of every row.\n\n"
    )
    parts.append(
        "### §5.3 Q6F is a Legitimate Verdict (N-10 binding)\n\n"
        "Selecting `Q6F_deferred_with_algorithm_survey` is a "
        "legitimate Q6 verdict, NOT a planning failure -- it preserves "
        "Invariant I7 ('no magic numbers') when comparative empirical "
        "evidence is genuinely insufficient. The Q6_selected_policy "
        "row binds Q6F per the planning T05 default recommendation "
        "(see §12 below).\n\n"
    )

    parts.append("## §6 Candidate Policy Comparison (4-axis)\n\n")
    parts.append(
        "| candidate | deployability | complexity | leakage_risk | "
        "evidence_level |\n"
    )
    parts.append("|---|---|---|---|---|\n")
    for d in decisions:
        if not d.candidate_policy:
            continue
        parts.append(
            f"| `{d.candidate_policy}` | "
            f"`{d.complexity_deployability_score}` | "
            f"`{d.complexity_deployability_score}` | "
            f"`{d.leakage_risk_score}` | "
            f"`{d.rating_evidence_level}` |\n"
        )
    parts.append("\n")

    parts.append("## §7 MMR-Missingness Reaffirmation\n\n")
    parts.append(
        f"MMR is missing in **{EXPECTED_MMR_MISSING_DENSITY_MFC_PCT}%** "
        f"of `matches_flat_clean` rows ({EXPECTED_MFC_ROW_COUNT} total) "
        f"and **{EXPECTED_MMR_MISSING_DENSITY_PHA_PCT}%** of "
        f"`player_history_all` rows ({EXPECTED_PHA_ROW_COUNT} total). "
        "Cited verbatim from the dataset `research_log.md` lines 106 + "
        "1135. This is not an outlier; it is structural (unrated "
        "professional corpus). The `is_mmr_missing` flag (CROSS-02-02 "
        "§6.2 row 'is_mmr_missing (PRE_GAME flag)' line 228) is the "
        "primary skill-signal proxy across the missing-MMR regime.\n\n"
    )
    if probes:
        mfc = probes.get("mfc_mmr_missing", (0, 0))
        pha = probes.get("pha_mmr_missing", (0, 0))
        parts.append(
            f"**Probe re-affirmation (this run):** MFC "
            f"total={mfc[0]} / missing={mfc[1]}; PHA total={pha[0]} "
            f"/ missing={pha[1]}.\n\n"
        )

    parts.append("## §8 Rating-Method Literature Context\n\n")
    parts.append(
        "Algorithm primary sources (citation-only; no implementation):\n\n"
    )
    parts.append(f"- {CITATION_ELO_1978}\n")
    parts.append(f"- {CITATION_GLICKMAN_1999}\n")
    parts.append(f"- {CITATION_GLICKMAN_2012}\n")
    parts.append(f"- {CITATION_HERBRICH_MINKA_GRAEPEL_2006}\n\n")

    parts.append("## §9 Forward-Only Update Semantics (per candidate)\n\n")
    parts.append(
        "Deterministic ordering (binding on every candidate the future "
        "algorithm-survey Step evaluates): `(toon_id, "
        "TRY_CAST(ph.details_timeUTC AS TIMESTAMP), ph.replay_id)`. "
        "The strict-`<` filter `STRICT_LT_HISTORY_FILTER` "
        f"(`{STRICT_LT_HISTORY_FILTER}`) per PR #242 Q3 BIND_NOW "
        "applies to every candidate. Note on the grouping key: "
        "`player_history_all` does NOT carry a `player_id_worldwide` "
        "column on this dataset (verified by DESCRIBE at module-author "
        "time); the canonical PHA grouping key for sc2egset is "
        "`toon_id`; `player_id_worldwide` is constructed only at the "
        "MHM join layer per PR #242 Q2 BIND_NOW.\n\n"
    )

    parts.append("## §10 Cold-Start Policy per Candidate (G-CS-4)\n\n")
    parts.append(
        "Every candidate honours G-CS-4 (`reports/specs/"
        "02_02_feature_engineering_plan.md` §9 line 422): the first-"
        "match row for any player must not be silently dropped; "
        "missingness encoded as a `is_first_match` flag, imputed value "
        "with explicit imputation rule, or separate cold-start branch. "
        "Q6A satisfies trivially (omission). Q6B-E use literature "
        "priors (rating=1500 / mu-RD-sigma defaults / mu=25-sigma=25/3) "
        "with `is_first_match` co-registered. Q6F binds G-CS-4 in "
        "advance on every candidate evaluated by the algorithm-survey "
        "Step.\n\n"
    )

    parts.append("## §11 Leakage Constraints per Candidate (G-L-4)\n\n")
    parts.append(
        "Every candidate honours G-L-4 (`reports/specs/"
        "02_02_feature_engineering_plan.md` §10 line 455): no `pre_game` "
        "or `history_enriched_pre_game` feature may read game T's post-"
        "game rating delta or rating-after value. No global / batch fit. "
        "No future-match read. No target-match outcome read. "
        "Forward-only per-pair update.\n\n"
    )

    parts.append("## §12 Q6 Selected Policy Binding Row\n\n")
    selected = _get_decision(decisions, "Q6_selected_policy")
    if selected is not None:
        parts.append(
            f"**Selected:** `{selected.selected_policy}`. "
            f"**Verdict:** `{selected.verdict}`. "
            f"**Materialization permission:** "
            f"`{selected.materialization_permission}`.\n\n"
            "Rationale (verbatim from the Q6_selected_policy row): "
            "comparative back-testing AUC / log-loss evidence among "
            "the 4 non-trivial candidates (B/C/D/E) does NOT exist in "
            "any prior artifact; binding a single family without this "
            "evidence would violate Invariant I7. Per planning N-10, "
            "this is a legitimate verdict, NOT a planning failure -- "
            "it preserves I7 and triggers a dedicated algorithm-survey "
            "Step that will back-test the candidates over the unrated "
            "regime.\n\n"
            "**Rejection rationale for the 5 unselected candidates** "
            "(JSON, also stored in the row's `rejected_options` "
            "field):\n\n"
            f"```json\n{selected.rejected_options}\n```\n\n"
        )

    parts.append("## §13 Materialization Permission Statement\n\n")
    parts.append(
        "Materialization for the `reconstructed_rating` family is "
        "BLOCKED pending the algorithm-survey PR. The future Layer-3 "
        "materialization PR for the 6 history-enriched pre_game "
        "families must NOT proceed until the algorithm-survey Step "
        "resolves the Q6F deferral with a binding selection. The "
        "per-family impact summary row encodes this constraint over "
        "all 6 families.\n\n"
    )

    parts.append("## §14 Non-Substitution Statement\n\n")
    parts.append(
        "This artifact does NOT replace PR #229, #230, #234, #236, "
        "#237, #239, #240, #241, #242, #243, or #244. It does NOT "
        "alter Q1-Q5 / Q7 / Q8 bindings from PR #242 / #243. It "
        "augments the PR #242 Q6 row only.\n\n"
    )

    parts.append("## §15 Falsifier Roll-Call\n\n")
    parts.append(
        "Every key from `FALSIFIER_PRIORITY_CHAIN` (status reported "
        "verbatim per PR #242 / #243 precedent):\n\n"
    )
    for key in FALSIFIER_PRIORITY_CHAIN:
        status = falsifier_status.get(key, "did_not_fire")
        parts.append(f"- `{key}`: {status}\n")
    parts.append("\n")

    parts.append("## §16 SHA Provenance\n\n")
    parts.append(
        f"- `parent_pr242_csv_sha256`: `{EXPECTED_PR242_CSV_SHA256}`\n"
        f"- `parent_pr242_md_sha256`: `{EXPECTED_PR242_MD_SHA256}`\n"
        f"- `parent_pr243_csv_sha256`: `{EXPECTED_PR243_CSV_SHA256}`\n"
        f"- `parent_pr243_md_sha256`: `{EXPECTED_PR243_MD_SHA256}`\n"
        f"- `pr241_scaffold_validator_module_sha256`: "
        f"`{EXPECTED_PR241_VALIDATOR_SHA256}`\n"
        f"- `cross_02_02_spec_sha256`: "
        f"`{EXPECTED_CROSS_02_02_SPEC_SHA256}`\n"
        f"- `feature_family_registry_csv_sha256`: "
        f"`{EXPECTED_FEATURE_FAMILY_REGISTRY_CSV_SHA256}`\n"
        f"- `dataset_research_log_sha256`: "
        f"`{EXPECTED_DATASET_RESEARCH_LOG_SHA256}`\n"
        f"- `player_history_all_yaml_sha256`: "
        f"`{EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256}`\n"
        f"- `matches_flat_clean_yaml_sha256`: "
        f"`{EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256}`\n"
        f"- `matches_history_minimal_yaml_sha256`: "
        f"`{EXPECTED_MATCHES_HISTORY_MINIMAL_YAML_SHA256}`\n\n"
    )

    parts.append("## §17 No Step 02_01_03 Closure / No Phase 03 Start\n\n")
    parts.append(
        "Step 02_01_03 remains OPEN. This artifact does NOT add "
        "`02_01_03: complete` to `STEP_STATUS.yaml`. Closure is "
        "deferred per the PR #237 tranche-1 closure precedent. Phase "
        "03 work remains forbidden (PHASE_STATUS.yaml shows Phase 03 "
        "= `not_started`; ml-protocol §4 superseded "
        "`create_temporal_split()` is barred from any thesis "
        "experiment).\n\n"
    )

    parts.append("## §18 Per-Decision Sections\n\n")
    for d in decisions:
        parts.append(_md_decision_section(d))

    md_path.write_text("".join(parts), encoding="utf-8")
    LOGGER.debug("_write_md: wrote MD to %s", md_path)


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def run_rating_reconstruction_adjudication(
    *,
    duckdb_path: Path,
    parent_pr242_csv_path: Path,
    parent_pr242_md_path: Path,
    parent_pr243_csv_path: Path,
    parent_pr243_md_path: Path,
    pr241_validator_module_path: Path,
    cross_02_02_spec_path: Path,
    feature_family_registry_csv_path: Path,
    dataset_research_log_path: Path,
    player_history_all_yaml_path: Path,
    matches_flat_clean_yaml_path: Path,
    matches_history_minimal_yaml_path: Path,
    csv_out_path: Path,
    md_out_path: Path,
    audit_pr: str,
    audit_date: str = "2026-05-25",  # noqa: ARG001 — provenance footer only
    skip_probes: bool = False,
) -> RatingReconstructionAdjudicationResult:
    """Run the Q6 rating-reconstruction successor adjudication.

    Verifies SHA pins on all 11 parent/source files, constructs the 8 Q6
    decision rows per T05, runs every falsifier in
    ``FALSIFIER_PRIORITY_CHAIN`` order, and (if no falsifier fires)
    writes the CSV + MD artifact pair byte-deterministically.

    Probes are optional sanity-evidence (read-only DuckDB); when
    ``skip_probes=True`` they are not run. Probes are never used as
    gating.

    Args:
        duckdb_path: Path to the sc2egset DuckDB file (opened read-only).
        parent_pr242_csv_path: Path to the PR #242 parent CSV.
        parent_pr242_md_path: Path to the PR #242 parent MD.
        parent_pr243_csv_path: Path to the PR #243 parent CSV.
        parent_pr243_md_path: Path to the PR #243 parent MD.
        pr241_validator_module_path: Path to the PR #241 validator module.
        cross_02_02_spec_path: Path to ``02_02_feature_engineering_plan.md``.
        feature_family_registry_csv_path: Path to the 02_01_01 registry CSV.
        dataset_research_log_path: Path to the dataset ``research_log.md``.
        player_history_all_yaml_path: Path to ``player_history_all.yaml``.
        matches_flat_clean_yaml_path: Path to ``matches_flat_clean.yaml``.
        matches_history_minimal_yaml_path: Path to
            ``matches_history_minimal.yaml``.
        csv_out_path: Destination Q6 CSV path.
        md_out_path: Destination Q6 MD path.
        audit_pr: Layer-2 PR number placeholder string (e.g., ``"PR #N"``).
        audit_date: ISO YYYY-MM-DD date (recorded in provenance only).
        skip_probes: If True, skip the read-only DuckDB probes entirely
            (tests use this to avoid DuckDB I/O).

    Returns:
        ``RatingReconstructionAdjudicationResult`` with ``passed=True``
        iff no halting falsifier fired.
    """
    LOGGER.info(
        "run_rating_reconstruction_adjudication: audit_pr=%s "
        "skip_probes=%s",
        audit_pr,
        skip_probes,
    )

    # Build the 8 decision rows.
    common = _common_fields(audit_pr)
    decisions = _build_decisions(common)

    # SHA pin checks (priority order).
    invocations: dict[str, _FalsifierThunk] = {
        "parent_pr242_csv_sha256_mismatch": lambda: _check_parent_pr242_csv_sha256(
            parent_pr242_csv_path
        ),
        "parent_pr242_md_sha256_mismatch": lambda: _check_parent_pr242_md_sha256(
            parent_pr242_md_path
        ),
        "parent_pr243_csv_sha256_mismatch": lambda: _check_parent_pr243_csv_sha256(
            parent_pr243_csv_path
        ),
        "parent_pr243_md_sha256_mismatch": lambda: _check_parent_pr243_md_sha256(
            parent_pr243_md_path
        ),
        "pr241_sha256_mismatch": lambda: _check_pr241_validator_sha256(
            pr241_validator_module_path
        ),
        "cross_02_02_spec_sha256_mismatch": lambda: _check_cross_02_02_spec_sha256(
            cross_02_02_spec_path
        ),
        "feature_family_registry_csv_sha256_mismatch": (
            lambda: _check_feature_family_registry_csv_sha256(
                feature_family_registry_csv_path
            )
        ),
        "dataset_research_log_sha256_mismatch": (
            lambda: _check_dataset_research_log_sha256(
                dataset_research_log_path
            )
        ),
        "player_history_all_yaml_sha256_mismatch": (
            lambda: _check_player_history_all_yaml_sha256(
                player_history_all_yaml_path
            )
        ),
        "matches_flat_clean_yaml_sha256_mismatch": (
            lambda: _check_matches_flat_clean_yaml_sha256(
                matches_flat_clean_yaml_path
            )
        ),
        "matches_history_minimal_yaml_sha256_mismatch": (
            lambda: _check_matches_history_minimal_yaml_sha256(
                matches_history_minimal_yaml_path
            )
        ),
        # Candidate-set + structural.
        "q6_candidate_set_incomplete": lambda: _check_q6_candidate_set_complete(
            decisions
        ),
        "q6_omit_candidate_missing": lambda: _check_q6_omit_candidate_present(
            decisions
        ),
        "q6_deferred_blocker_candidate_missing": (
            lambda: _check_q6_deferred_candidate_present(decisions)
        ),
        "decision_count_mismatch": lambda: _check_decision_count(decisions),
        "decision_id_order_mismatch": lambda: _check_decision_ids_canonical_order(
            decisions
        ),
        # Token scans.
        "q6_post_game_token_in_scoped_field": (
            lambda: _check_no_post_game_token_in_scoped_fields(decisions)
        ),
        "q6_direct_target_match_outcome_referenced": (
            lambda: _check_no_direct_target_match_outcome_reference(decisions)
        ),
        "q6_future_match_leakage_referenced": (
            lambda: _check_no_future_match_reference(decisions)
        ),
        "q6_global_batch_fit_referenced": (
            lambda: _check_no_global_batch_fit_reference(decisions)
        ),
        "q6_phase_03_baseline_creep": (
            lambda: _check_no_phase_03_baseline_creep(decisions)
        ),
        # Per-candidate wording.
        "q6_forward_only_constraint_missing_for_non_omit_candidate": (
            lambda: _check_forward_only_constraint_present_when_non_omit(
                decisions
            )
        ),
        "q6_cold_start_policy_missing_for_non_omit_candidate": (
            lambda: _check_cold_start_policy_present_when_non_omit(decisions)
        ),
        "q6_tie_policy_missing_for_non_omit_candidate": (
            lambda: _check_tie_policy_present_when_non_omit(decisions)
        ),
        "q6_hyperparameter_policy_missing_for_non_omit_candidate": (
            lambda: _check_hyperparameter_policy_present_when_non_omit(
                decisions
            )
        ),
        # Enums.
        "q6_evidence_level_field_invalid": lambda: _check_evidence_level_valid(
            decisions
        ),
        "q6_complexity_deployability_invalid": (
            lambda: _check_complexity_deployability_valid(decisions)
        ),
        "q6_leakage_risk_invalid": lambda: _check_leakage_risk_valid(decisions),
        "q6_materialization_permission_invalid": (
            lambda: _check_materialization_permission_valid(decisions)
        ),
        # Citations + MMR + consistency.
        "q6_external_citation_missing_when_non_omit_selected": (
            lambda: _check_external_citation_present_when_non_omit_non_deferred(
                decisions
            )
        ),
        "q6_mmr_missingness_summary_missing": (
            lambda: _check_mmr_missingness_summary_present(decisions)
        ),
        "q6_materialization_permission_drift": (
            lambda: _check_materialization_permission_consistent_with_verdict(
                decisions
            )
        ),
        # Q5 + scope.
        "q6_q5_re_adjudication_drift": lambda: _check_q5_not_re_adjudicated(
            decisions
        ),
        "q6_status_yaml_drift": lambda: _check_no_status_yaml_path_referenced(
            decisions
        ),
        "q6_research_log_drift": (
            lambda: _check_no_research_log_mutation_implied(decisions)
        ),
        "q6_roadmap_drift": lambda: _check_no_roadmap_path_modified(decisions),
        "q6_materialization_creep": (
            lambda: _check_no_materialized_output_paths_populated(decisions)
        ),
        "universal_tracker_source_in_history": (
            lambda: _check_universal_tracker_source_in_history(decisions)
        ),
        # Per-row presence.
        "q6_per_family_impact_summary_missing": (
            lambda: _check_per_family_impact_summary_row_present(decisions)
        ),
        "q6_selected_policy_row_missing": (
            lambda: _check_selected_policy_row_present(decisions)
        ),
        "q6_selected_policy_not_in_candidate_set": (
            lambda: _check_selected_policy_in_candidate_set(decisions)
        ),
        "q6_selected_policy_verdict_invalid": (
            lambda: _check_selected_policy_verdict_consistent(decisions)
        ),
        "q6_per_family_impact_broadcast_incomplete": (
            lambda: _check_per_family_impact_broadcasts_all_6_families(
                decisions
            )
        ),
        # N-1 + N-2.
        "q6_excluded_methods_considered_incomplete": (
            lambda: _check_excluded_methods_considered_complete(decisions)
        ),
        "q6_raw_mmr_hybrid_rejection_token_missing": (
            lambda: _check_raw_mmr_hybrid_rejection_token_present(decisions)
        ),
    }

    halting: str | None = None
    fired: list[str] = []
    for key in FALSIFIER_PRIORITY_CHAIN:
        thunk = invocations.get(key)
        if thunk is None:
            continue
        did_fire, message = thunk()
        if did_fire:
            fired.append(key)
            if halting is None:
                halting = key
            LOGGER.warning("falsifier %s fired: %s", key, message)

    falsifier_status: dict[str, str] = {
        key: ("did_fire" if key in fired else "did_not_fire")
        for key in FALSIFIER_PRIORITY_CHAIN
    }

    probes: dict[str, Any] = {}
    if not skip_probes and halting is None:
        try:
            con = duckdb.connect(str(duckdb_path), read_only=True)
            try:
                probes["pha_result_distribution"] = (
                    _probe_pha_result_distribution(con)
                )
                probes["pha_details_timeutc_null_rate"] = (
                    _probe_pha_details_timeutc_null_rate(con)
                )
                probes["mfc_mmr_missing"] = _probe_mfc_mmr_missing_density(con)
                probes["pha_mmr_missing"] = _probe_pha_mmr_missing_density(con)
                probes["pha_per_player_history_depth"] = (
                    _probe_pha_per_player_history_depth(con)
                )
                probes["pha_result_vs_mmr_presence"] = (
                    _probe_pha_result_vs_mmr_presence(con)
                )
            finally:
                con.close()
        except (duckdb.Error, OSError) as exc:
            LOGGER.warning("DuckDB probes skipped due to error: %s", exc)
            probes = {}

    if halting is None:
        _write_csv(decisions, csv_out_path)
        _write_md(decisions, md_out_path, falsifier_status, probes)
    else:
        LOGGER.warning(
            "run_rating_reconstruction_adjudication: halting falsifier %s "
            "-- CSV+MD NOT written",
            halting,
        )

    git_sha = _get_git_sha()
    return RatingReconstructionAdjudicationResult(
        decisions=decisions,
        csv_path=str(csv_out_path),
        md_path=str(md_out_path),
        provenance_git_sha=git_sha,
        probes=probes,
        falsifiers_fired=tuple(fired),
        halting_falsifier=halting,
        passed=halting is None,
    )
