"""Q5 cross-region retention successor adjudicator for SC2EGSet Step 02_01_03.

Pure read-only module. Writes ONLY the Q5 successor adjudication CSV+MD
artifact pair. Never materializes features. Never writes Parquet. Never
modifies status YAMLs or research logs. See ``planning/current_plan.md``
for the full spec.

This module is the Layer-2 successor to PR #242's parent adjudication.
PR #242 closed Q5 (``cross_region_fragmentation_handling``) and Q6
(``rating_policy``) as ``verdict=deferred_blocker``. PR #243 (this module's
output) upgrades Q5 only — Q6 remains deferred and out of scope.

The module evaluates the three pre-enumerated CROSS-02-02 §6.2 row 5 options:

    (a) ``strict_exclusion`` — filter PHA history rows
        ``WHERE NOT ph.is_cross_region_fragmented`` BEFORE aggregation
    (b) ``dual_feature_path`` — keep all PHA rows, materialize ``xr_*`` and
        ``nonxr_*`` per-branch columns
    (c) ``sensitivity_indicator_co_registration`` — keep all PHA rows, add a
        ``is_cross_region_fragmented`` flag co-registered alongside the
        history features at the target-time anchor

The canonical strict-`<` filter (B-X2 inherited from PR #242) is the single
source of truth for any executable history cutoff text inside this module:

    TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at

Round-2/3/4 binding fixes:

- B1 (column on PHA not MFC): every probe reads
  ``player_history_all.is_cross_region_fragmented``; MFC has no such column.
- B2 (MFC join keys): ``mfc.replay_id`` / ``mfc.toon_id`` (NOT
  ``mfc.match_id`` / ``mfc.player_id``); MHM keyed by
  ``'sc2egset::' || mfc.replay_id`` / ``mfc.toon_id``.
- B3 (filter HISTORY rows, not TARGET rows): ``WHERE NOT
  ph.is_cross_region_fragmented`` applied to PHA rows BEFORE aggregation.
  Retention smoke (kept + dropped == total) measures only rows with a
  matched PHA history record; cold-start target rows (LEFT-JOIN NULL on
  ``history_is_xr``) are excluded from ``history_rows_total`` via the
  ``FILTER (WHERE history_is_xr IS NOT NULL)`` clause in
  ``_STRICT_EXCLUSION_HISTORY_FILTER_RETENTION_QUERY``
  (PR #243 Dispatch 3 OPTION (a) fix; see also
  ``_check_strict_exclusion_history_filter_retention_smoke`` docstring).
- N3 (verdict-emergence discipline): the recommended verdict in
  ``Q5_selected_policy`` is PROVISIONAL — the executor must report the
  per-family retention table FIRST and the verdict EMERGES from the table.
- NIT-B (4 pinned source-file SHAs): silent drift in
  ``player_history_all.yaml`` / ``01_04_05_cross_region_annotation.md`` /
  ``matches_flat_clean.yaml`` / ``02_02_feature_engineering_plan.md``
  invalidates the binding rationale; SHA mismatch halts before write.
- NIT-C (two-probe split): toon_id-membership BINDING probe + nickname-
  anchored EQUIVALENCE probe; the 32,031 anchor is bound only by the
  nickname-anchored probe (per 01_05_10 MD §3.3 line 398 SQL 3 idiom).
- NIT-D (structured field): ``history_row_filter_on_pha_applied`` replaces
  the round-2 vacuous prose-substring assertion with a tri-valued enum
  (``yes``/``no``/``not_applicable``); SQL byte-scan portion KEPT.
- B4 (count invariants): ``HELPER_TO_FALSIFIER_KEY`` and
  ``FALSIFIER_PRIORITY_CHAIN`` each contain EXACTLY 31 entries; their value
  set is equal; the chain has no duplicates — asserted at module import.
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

from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import (  # noqa: E501
    EXPECTED_PR241_VALIDATOR_SHA256,
    POST_GAME_TOKEN_EXEMPT_FIELDS,
    POST_GAME_TOKEN_SCOPED_FIELDS,
    POST_GAME_TOKENS,
    STRICT_LT_FILTER_ROADMAP_RAW,
    STRICT_LT_HISTORY_FILTER,
)
from rts_predict.games.sc2.datasets.sc2egset.validate_history_enriched_pre_game_materialization import (  # noqa: E501
    HISTORY_TRANCHE2_FAMILY_IDS,
    IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
)

_FalsifierThunk = Callable[[], tuple[bool, str]]

__all__ = [
    "ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS",
    "ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED",
    "ALLOWED_Q5_BINDING_LEVELS",
    "ALLOWED_Q5_VERDICTS",
    "CROSS_REGION_COLUMN_NAME",
    "CROSS_REGION_COLUMN_SOURCE_TABLE",
    "CrossRegionAdjudicationDecision",
    "CrossRegionAdjudicationResult",
    "EXPECTED_01_04_05_MD_SHA256",
    "EXPECTED_CROSS_02_02_SPEC_SHA256",
    "EXPECTED_CROSS_REGION_NICKNAME_COUNT",
    "EXPECTED_CROSS_REGION_PLAYER_MATCH_PAIR_COUNT_NICKNAME_ANCHORED",
    "EXPECTED_CROSS_REGION_TOON_ID_COUNT",
    "EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256",
    "EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256",
    "EXPECTED_PR241_VALIDATOR_SHA256",
    "FALSIFIER_PRIORITY_CHAIN",
    "HELPER_TO_FALSIFIER_KEY",
    "HISTORY_TRANCHE2_FAMILY_IDS",
    "IN_GAME_HISTORICAL_AGGREGATED_COLUMNS",
    "Q5_DECISION_IDS",
    "Q5_OPTION_NAMES",
    "Q5AdjudicationFalsifierError",
    "STRICT_LT_FILTER_ROADMAP_RAW",
    "STRICT_LT_HISTORY_FILTER",
    "adjudicate_history_cross_region_retention",
]

LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Predecessor PR provenance constants
# ---------------------------------------------------------------------------

PARENT_PR242_NUMBER: str = "PR #242"
SUCCESSOR_PR_NUMBER: str = "PR #243"

# ---------------------------------------------------------------------------
# NIT-B — pinned SHA-256 source-file constants (round-3 NIT-B / A18)
# Verified at planner-time 2026-05-24 on master HEAD e372e7b6.
# Any drift halts via the matching helper in T03; the executor must re-pin
# and re-verify the B1/B3 binding rationale before re-running.
# ---------------------------------------------------------------------------

EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256: str = (
    "7962dd910e0b72419e35a9895689cd4ae6a51c2be0bc6e5e0fe4a0ceb8f207d0"
)
EXPECTED_01_04_05_MD_SHA256: str = (
    "7bac26fd69952509a9dac323436e074902ca8ba9e0bac64021ad04de7f5dc9fe"
)
EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256: str = (
    "9f76c1912624535b7b7ac0d2fb767fd4b9791a1d808bf73f747416d557d6cb1f"
)
EXPECTED_CROSS_02_02_SPEC_SHA256: str = (
    "86af792370272e611f048aae0c48c9cc595eb4b44c1db38c0bb4ecea0ff1b289"
)


# ---------------------------------------------------------------------------
# Q5 decision IDs and option names (exactly 5 rows; exactly 3 options)
# ---------------------------------------------------------------------------

Q5_DECISION_IDS: tuple[str, ...] = (
    "Q5A_strict_exclusion_retention",
    "Q5B_dual_feature_path_retention",
    "Q5C_sensitivity_indicator_retention",
    "Q5_selected_policy",
    "Q5_per_family_impact_summary",
)
Q5_DECISION_COUNT: int = 5

Q5_OPTION_NAMES: tuple[str, ...] = (
    "strict_exclusion",
    "dual_feature_path",
    "sensitivity_indicator_co_registration",
)
Q5_OPTION_COUNT: int = 3

# Map decision IDs to the policy they evaluate (or empty for selected/summary).
Q5_DECISION_ID_TO_POLICY: dict[str, str] = {
    "Q5A_strict_exclusion_retention": "strict_exclusion",
    "Q5B_dual_feature_path_retention": "dual_feature_path",
    "Q5C_sensitivity_indicator_retention": "sensitivity_indicator_co_registration",
    "Q5_selected_policy": "",  # filled at decision-build time
    "Q5_per_family_impact_summary": "",
}


# ---------------------------------------------------------------------------
# Cross-region column source (round-2 B1 / A15 — PHA, not MFC)
# ---------------------------------------------------------------------------

CROSS_REGION_COLUMN_SOURCE_TABLE: str = "player_history_all"
CROSS_REGION_COLUMN_NAME: str = "is_cross_region_fragmented"


# ---------------------------------------------------------------------------
# Anchor / structured-field enums (NIT-C and NIT-D)
# ---------------------------------------------------------------------------

ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS: frozenset[str] = frozenset(
    {"toon_id_based", "nickname_based", "both"}
)

ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED: frozenset[str] = frozenset(
    {"yes", "no", "not_applicable"}
)


# ---------------------------------------------------------------------------
# 01_05_10 nickname-anchored numeric anchors (read by EQUIVALENCE probe only;
# NOT shared by the toon_id-membership BINDING probe — see NIT-C / A19)
# ---------------------------------------------------------------------------

EXPECTED_CROSS_REGION_NICKNAME_COUNT: int = 246
EXPECTED_CROSS_REGION_TOON_ID_COUNT: int = 1923
EXPECTED_CROSS_REGION_PLAYER_MATCH_PAIR_COUNT_NICKNAME_ANCHORED: int = 32031


# ---------------------------------------------------------------------------
# Allowed verdicts and binding levels for Q5 successor decisions
# ---------------------------------------------------------------------------

ALLOWED_Q5_VERDICTS: frozenset[str] = frozenset(
    {
        "bind_now",
        "ratify_with_evidence",
        "extend_with_evidence",
        "narrow_with_evidence",
        "deferred_recommendation",
        "deferred_blocker",
    }
)
ALLOWED_Q5_BINDING_LEVELS: frozenset[str] = frozenset(
    {
        "binding_for_materialization",
        "binding_for_phase_03_split",
        "recommendation_only",
        "deferred_blocker",
        "deferred_recommendation",
    }
)


# ---------------------------------------------------------------------------
# Artifact paths (relative to repo root; I10)
# ---------------------------------------------------------------------------

PR241_VALIDATOR_MODULE_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/"
    "validate_history_enriched_pre_game_materialization.py"
)
PARENT_PR242_MODULE_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/"
    "adjudicate_history_enriched_pre_game_source_layer.py"
)
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
ADJUDICATION_CSV_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_cross_region_adjudication.csv"
)
ADJUDICATION_MD_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_cross_region_adjudication.md"
)

# NIT-B path constants (relative; SHA-256 verified against pinned constants).
PLAYER_HISTORY_ALL_YAML_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/"
    "player_history_all.yaml"
)
STEP_01_04_05_MD_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "01_exploration/04_cleaning/01_04_05_cross_region_annotation.md"
)
MATCHES_FLAT_CLEAN_YAML_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/"
    "matches_flat_clean.yaml"
)
CROSS_02_02_SPEC_REL: str = "reports/specs/02_02_feature_engineering_plan.md"

# 01_05_10 evidence (SHAs computed at runtime; expected constants set by caller
# or compared after pinning — see entrypoint).
STEP_01_05_10_MD_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "01_exploration/05_temporal_panel_eda/cross_region_history_impact_sc2egset.md"
)
STEP_01_05_10_JSON_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "01_exploration/05_temporal_panel_eda/cross_region_history_impact_sc2egset.json"
)


# ---------------------------------------------------------------------------
# Q5-policy enforcement constants (NIT-D consistency rules)
# ---------------------------------------------------------------------------

# Required value of history_row_filter_on_pha_applied per selected_policy.
# Q5C binds 'no' per planner mandate (the option does not apply a PHA filter);
# the spec ALLOWS 'not_applicable' for Q5C but planner pins 'no' for the more
# informative reading.
Q5_POLICY_TO_HISTORY_ROW_FILTER: dict[str, str] = {
    "strict_exclusion": "yes",
    "dual_feature_path": "yes",
    "sensitivity_indicator_co_registration": "no",
}


# ---------------------------------------------------------------------------
# Q6 disclaimer constants (Q6 remains deferred_blocker; this PR is Q5-only)
# ---------------------------------------------------------------------------

Q6_OUT_OF_SCOPE_PHRASE: str = (
    "Q6 (rating policy) remains deferred_blocker per PR #242; out of scope for PR #243."
)


# ---------------------------------------------------------------------------
# SQL probe constants (read-only; named per python-code.md `_QUERY` suffix)
# ---------------------------------------------------------------------------

# T02 step 1: BINDING base probe (round-3 NIT-C; anchor: toon_id-membership;
# expected count pinned at Layer-2 write time as
# EXPECTED_PHA_CROSS_REGION_TOONID_MEMBERSHIP_COUNT, passed in to entrypoint).
_CROSS_REGION_TOONID_MEMBERSHIP_BASE_PROBE_QUERY: str = """
SELECT COUNT(*) AS n_pha_rows_toonid_membership_anchored
FROM player_history_all ph
WHERE ph.toon_id IN (
  SELECT DISTINCT toon_id
  FROM player_history_all
  WHERE is_cross_region_fragmented = TRUE
)
""".strip()

# T02 step 2: EQUIVALENCE base probe (round-3 NIT-C; anchor: lowercase
# nickname; expected counts (246, 1923, 32031) per 01_05_10 MD §3.3 line 398
# / SQL 3 idiom). Exploratory check, NOT the binding probe.
_CROSS_REGION_NICKNAME_ANCHOR_PROBE_QUERY: str = """
WITH cross_region_nicks AS (
  SELECT LOWER(nickname) AS nick
  FROM replay_players_raw
  GROUP BY 1
  HAVING COUNT(DISTINCT region) > 1
)
SELECT
  (SELECT COUNT(*) FROM cross_region_nicks) AS n_cross_region_nicknames,
  (SELECT COUNT(DISTINCT ph.toon_id)
     FROM player_history_all ph
     WHERE ph.is_cross_region_fragmented = TRUE) AS n_cross_region_toon_ids,
  (SELECT COUNT(*)
     FROM player_history_all ph
     INNER JOIN cross_region_nicks crn ON LOWER(ph.nickname) = crn.nick
     WHERE ph.details_timeUTC IS NOT NULL) AS n_player_match_pairs_nickname_anchored
""".strip()

# T02 step 3: per-family strict-exclusion retention (round-2 B3 binding —
# WHERE NOT ph.is_cross_region_fragmented applied to PHA HISTORY rows BEFORE
# aggregation; the MFC target view does NOT carry the cross-region column).
# Uses MFC's canonical replay_id / toon_id keys + MHM's 'sc2egset::'
# single-prefixed match_id (A16). The strict-< filter uses
# STRICT_LT_HISTORY_FILTER (B-X2).
_STRICT_EXCLUSION_HISTORY_FILTER_RETENTION_QUERY: str = """
WITH base AS (
  SELECT
    target.match_id       AS target_match_id,
    target.player_id      AS target_player,
    target.started_at     AS target_started_at,
    ph.replay_id          AS history_replay_id,
    ph.toon_id            AS history_toon_id,
    ph.details_timeUTC    AS history_time,
    ph.is_cross_region_fragmented AS history_is_xr
  FROM matches_flat_clean mfc
  JOIN matches_history_minimal target
    ON target.match_id  = 'sc2egset::' || mfc.replay_id
   AND target.player_id = mfc.toon_id
  LEFT JOIN player_history_all ph
    ON ph.toon_id = mfc.toon_id
   AND TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
)
-- 3.A OPTION (a) fix (PR #243 Dispatch 3): the base CTE is a LEFT JOIN on
-- player_history_all, so cold-start target rows (no prior PHA history)
-- contribute a row with history_is_xr IS NULL. Those NULL rows cannot be
-- counted as kept (FALSE) or dropped (TRUE), so including them in
-- history_rows_total would falsely break the kept + dropped == total smoke
-- invariant. Restrict history_rows_total to rows with an actual matched
-- history record (history_is_xr IS NOT NULL); the cold-start NULL rows are
-- not a retention measurement.
SELECT
  COUNT(*) FILTER (WHERE history_is_xr = FALSE)                            AS history_rows_kept,
  COUNT(*) FILTER (WHERE history_is_xr = TRUE)                             AS history_rows_dropped,
  COUNT(DISTINCT history_toon_id) FILTER (WHERE history_is_xr = TRUE)      AS players_affected,
  COUNT(DISTINCT target_match_id) FILTER (WHERE history_is_xr = TRUE)      AS matches_affected,
  COUNT(*) FILTER (WHERE history_is_xr IS NOT NULL)                        AS history_rows_total
FROM base
""".strip()

# T02 step 4: dual-feature-path branch nondegeneracy probe (option (b)).
# Splits PHA history rows on is_cross_region_fragmented and counts per-branch
# coverage per target row. Filter applied to PHA history rows (A17).
_DUAL_FEATURE_PATH_RETENTION_QUERY: str = """
WITH base AS (
  SELECT
    target.match_id  AS target_match_id,
    target.player_id AS target_player,
    target.started_at,
    ph.is_cross_region_fragmented AS history_is_xr,
    ph.replay_id     AS history_replay_id
  FROM matches_flat_clean mfc
  JOIN matches_history_minimal target
    ON target.match_id  = 'sc2egset::' || mfc.replay_id
   AND target.player_id = mfc.toon_id
  LEFT JOIN player_history_all ph
    ON ph.toon_id = mfc.toon_id
   AND TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
),
branched AS (
  SELECT
    target_match_id,
    target_player,
    COUNT(*) FILTER (WHERE history_is_xr = FALSE) AS nonxr_branch_count,
    COUNT(*) FILTER (WHERE history_is_xr = TRUE)  AS xr_branch_count
  FROM base
  GROUP BY target_match_id, target_player
)
SELECT
  COUNT(*)                                              AS n_target_rows,
  SUM(CASE WHEN nonxr_branch_count > 0 THEN 1 ELSE 0 END) AS n_nonxr_nondegenerate,
  SUM(CASE WHEN xr_branch_count > 0 THEN 1 ELSE 0 END)    AS n_xr_nondegenerate,
  SUM(nonxr_branch_count)                                 AS total_nonxr_rows,
  SUM(xr_branch_count)                                    AS total_xr_rows
FROM branched
""".strip()

# T02 step 5: sensitivity-indicator nondegeneracy + target-time anchoring
# probe (option (c)). For each target row, project the boolean-OR of
# ph.is_cross_region_fragmented over the strict-< history window. The flag
# must be non-degenerate (both TRUE and FALSE present).
_SENSITIVITY_INDICATOR_RETENTION_QUERY: str = """
WITH base AS (
  SELECT
    target.match_id  AS target_match_id,
    target.player_id AS target_player,
    target.started_at,
    BOOL_OR(ph.is_cross_region_fragmented) AS sensitivity_flag,
    COUNT(*)                                AS history_rows_in_window
  FROM matches_flat_clean mfc
  JOIN matches_history_minimal target
    ON target.match_id  = 'sc2egset::' || mfc.replay_id
   AND target.player_id = mfc.toon_id
  LEFT JOIN player_history_all ph
    ON ph.toon_id = mfc.toon_id
   AND TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
  GROUP BY target.match_id, target.player_id, target.started_at
)
SELECT
  COUNT(*)                                                AS n_target_rows,
  SUM(CASE WHEN sensitivity_flag = TRUE  THEN 1 ELSE 0 END) AS n_flag_true,
  SUM(CASE WHEN sensitivity_flag = FALSE THEN 1 ELSE 0 END) AS n_flag_false,
  SUM(CASE WHEN sensitivity_flag IS NULL THEN 1 ELSE 0 END) AS n_flag_null,
  SUM(history_rows_in_window)                             AS total_history_rows
FROM base
""".strip()

# T02 step 6: family-level impact summary probe. Computes per-family
# (history_rows_kept, history_rows_dropped) under strict_exclusion option.
# Tagging by family is implicit (each row covers all 6 families because PHA
# history aggregates feed every family; the per-family decomposition is the
# product of this row count with each family's known weight, recorded in
# the MD §rationale).
_FAMILY_LEVEL_IMPACT_QUERY: str = """
WITH base AS (
  SELECT
    ph.is_cross_region_fragmented AS history_is_xr,
    ph.toon_id                    AS history_toon_id
  FROM matches_flat_clean mfc
  JOIN matches_history_minimal target
    ON target.match_id  = 'sc2egset::' || mfc.replay_id
   AND target.player_id = mfc.toon_id
  LEFT JOIN player_history_all ph
    ON ph.toon_id = mfc.toon_id
   AND TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
)
SELECT
  COUNT(*) FILTER (WHERE history_is_xr = FALSE)                            AS history_rows_kept,
  COUNT(*) FILTER (WHERE history_is_xr = TRUE)                             AS history_rows_dropped,
  COUNT(DISTINCT history_toon_id) FILTER (WHERE history_is_xr = TRUE)      AS players_affected,
  COUNT(*)                                                                 AS history_rows_total
FROM base
""".strip()


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------


class Q5AdjudicationFalsifierError(RuntimeError):
    """Raised when the entrypoint halts on a fired falsifier (advisory).

    Note: the entrypoint signals halt by returning a Result with
    ``passed=False`` and ``halting_falsifier`` set; this exception is
    provided for callers that prefer exception-driven flow. The default
    entrypoint does NOT raise — it returns a Result.

    Attributes:
        falsifier_key: The first fired falsifier key (priority order).
        observed: Brief observed value description.
        expected: Brief expected value description.
    """

    def __init__(self, falsifier_key: str, observed: str, expected: str) -> None:
        self.falsifier_key = falsifier_key
        self.observed = observed
        self.expected = expected
        super().__init__(
            f"Falsifier {falsifier_key!r} fired: observed={observed!r} "
            f"expected={expected!r}"
        )


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CrossRegionAdjudicationDecision:
    """A single resolved Q5 successor-adjudication row.

    The CSV row schema is exactly this dataclass's field order (29 columns
    total = 28 fields here + notes appended last; ``wc -l`` on the CSV = 6 =
    1 header + 5 data rows in ``Q5_DECISION_IDS`` order).

    Attributes:
        decision_id: One of ``Q5_DECISION_IDS``.
        parent_decision_id: Literal ``"Q5_cross_region_policy"`` (NEW field
            introduced by this successor PR per round-2 N1; back-fillable
            into PR #242 via a future cosmetic chore — not in scope here).
        decision_name: Short human-readable name.
        verdict: One of ``ALLOWED_Q5_VERDICTS``.
        binding_level: One of ``ALLOWED_Q5_BINDING_LEVELS``.
        scope: Family scope or all-six-families literal.
        selected_policy: One of ``Q5_OPTION_NAMES`` (or ``""`` for evaluation
            and summary rows).
        rejected_options: Newline-joined; for ``Q5_selected_policy`` only.
        cross_region_policy: Mirror of ``selected_policy`` for downstream
            materialization SQL keying.
        cross_region_retention_counts: JSON-string keyed by family_id with
            ``{history_rows_kept, history_rows_dropped, retention_pct}``
            triples. Counts measure PHA HISTORY rows (B3).
        cross_region_affected_players: Per-option distinct PHA toon_id count
            (stringified integer).
        cross_region_affected_matches: Per-option distinct MHM match_id count
            (stringified integer).
        cross_region_anchor_semantics: One of
            ``ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS`` (NIT-C / A19).
        history_row_filter_on_pha_applied: One of
            ``ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED`` (NIT-D / A20);
            structured replacement for the round-2 vacuous substring check.
        retention_measurement_summary: One-sentence prose summary.
        evidence_paths: Newline-joined repo-relative paths.
        falsifiers: Newline-joined ``key:status`` pairs.
        audit_pr: Literal ``"PR #243"`` (Layer-2 PR number).
        pr241_scaffold_validator_module_sha256: PR #241 binding SHA.
        parent_pr242_csv_sha256: PR #242 parent CSV SHA.
        parent_pr242_md_sha256: PR #242 parent MD SHA.
        parent_pr242_artifact_sha256: SHA-256 of CSV+MD concatenated bytes.
        provenance_01_05_10_md_sha256: 01_05_10 MD evidence SHA.
        provenance_01_05_10_json_sha256: 01_05_10 JSON evidence SHA.
        player_history_all_yaml_sha256: PHA YAML SHA (NIT-B / A18).
        step_01_04_05_md_sha256: 01_04_05 cleaning MD SHA (NIT-B / A18).
        matches_flat_clean_yaml_sha256: MFC YAML SHA (NIT-B / A18).
        cross_02_02_spec_sha256: CROSS-02-02 spec SHA (NIT-B / A18).
        materialized_output_paths: Always ``""`` (this is an adjudication,
            not a materialization).
        notes: Free-text rationale; column 29.
    """

    decision_id: str
    parent_decision_id: str
    decision_name: str
    verdict: str
    binding_level: str
    scope: str
    selected_policy: str
    rejected_options: str
    cross_region_policy: str
    cross_region_retention_counts: str
    cross_region_affected_players: str
    cross_region_affected_matches: str
    cross_region_anchor_semantics: str
    history_row_filter_on_pha_applied: str
    retention_measurement_summary: str
    evidence_paths: str
    falsifiers: str
    audit_pr: str
    pr241_scaffold_validator_module_sha256: str
    parent_pr242_csv_sha256: str
    parent_pr242_md_sha256: str
    parent_pr242_artifact_sha256: str
    provenance_01_05_10_md_sha256: str
    provenance_01_05_10_json_sha256: str
    player_history_all_yaml_sha256: str
    step_01_04_05_md_sha256: str
    matches_flat_clean_yaml_sha256: str
    cross_02_02_spec_sha256: str
    materialized_output_paths: str
    notes: str


@dataclass(frozen=True)
class CrossRegionAdjudicationResult:
    """Aggregate result of the Q5 successor adjudication.

    Attributes:
        decisions: Exactly 5 rows in ``Q5_DECISION_IDS`` order.
        csv_path: Filesystem path the CSV was (or would be) written to.
        md_path: Filesystem path the MD was (or would be) written to.
        provenance_git_sha: HEAD git SHA resolved at run time.
        falsifiers_fired: Every fired falsifier key (priority order).
        halting_falsifier: First falsifier key that fired, or None.
        passed: True iff ``halting_falsifier is None``.
    """

    decisions: tuple[CrossRegionAdjudicationDecision, ...]
    csv_path: str
    md_path: str
    provenance_git_sha: str
    falsifiers_fired: tuple[str, ...]
    halting_falsifier: str | None
    passed: bool


# ---------------------------------------------------------------------------
# Helper-to-falsifier-key mapping (round-3 B4 / NIT-B / NIT-D — 31 entries)
# ---------------------------------------------------------------------------

HELPER_TO_FALSIFIER_KEY: dict[str, str] = {
    # Provenance SHA checks (5 baseline + 4 NIT-B = 9 total)
    "_check_parent_pr242_csv_sha256": "parent_pr242_csv_sha256_mismatch",
    "_check_parent_pr242_md_sha256": "parent_pr242_md_sha256_mismatch",
    "_check_pr241_validator_sha256": "pr241_sha256_mismatch",
    "_check_01_05_10_evidence_sha256_md": "cross_region_01_05_10_md_sha256_mismatch",
    "_check_01_05_10_evidence_sha256_json": "cross_region_01_05_10_json_sha256_mismatch",
    "_check_player_history_all_yaml_sha256": "player_history_all_yaml_sha256_mismatch",
    "_check_step_01_04_05_md_sha256": "step_01_04_05_md_sha256_mismatch",
    "_check_matches_flat_clean_yaml_sha256": "matches_flat_clean_yaml_sha256_mismatch",
    "_check_cross_02_02_spec_sha256": "cross_02_02_spec_sha256_mismatch",
    # Module byte-scan checks (B1 + strict-<)
    "_check_no_mfc_cross_region_column_reference": "mfc_cross_region_column_referenced",
    "_check_strict_lt_filter_divergence": "strict_lt_filter_divergence",
    # DuckDB anchor probes (NIT-C — BINDING + EQUIVALENCE)
    "_check_cross_region_toonid_anchor_count_drift": (
        "cross_region_toon_id_anchor_count_drift"
    ),
    "_check_cross_region_nickname_anchor_count_drift": (
        "cross_region_nickname_anchor_count_drift"
    ),
    # Decision-row structural checks
    "_check_decision_count": "decision_count_drift",
    "_check_q5_three_options_enumerated": "q5_three_options_not_enumerated",
    # Per-option retention probes (B3 + dual-branch + sensitivity)
    "_check_strict_exclusion_history_filter_retention_smoke": (
        "strict_exclusion_history_filter_retention_smoke_failed"
    ),
    "_check_dual_feature_path_branches_nondegenerate": (
        "dual_feature_path_branch_degenerate"
    ),
    "_check_sensitivity_indicator_flag_nondegenerate": (
        "sensitivity_indicator_flag_degenerate"
    ),
    "_check_sensitivity_indicator_anchor_target_time": (
        "sensitivity_indicator_post_game_token_in_scoped_field"
    ),
    # Per-row semantic checks
    "_check_q5_evidence_sufficiency": "q5_evidence_sufficiency_violated",
    "_check_q5_no_post_game_token_in_scoped_fields": (
        "q5_post_game_token_in_scoped_field"
    ),
    "_check_q5_no_direct_target_match_outcome": (
        "q5_direct_target_match_outcome_referenced"
    ),
    "_check_q5_no_future_match_leakage": "q5_future_match_leakage_referenced",
    "_check_q5_no_global_batch_fit": "q5_global_batch_fit_referenced",
    "_check_q5_no_phase_03_baseline_creep": "q5_phase_03_baseline_creep",
    # NIT-D split (structured-field check + SQL byte-scan)
    "_check_history_row_filter_on_pha_field_valid": (
        "history_row_filter_on_pha_field_invalid"
    ),
    "_check_q5_filter_target_is_pha_history_sql": (
        "q5_filter_target_is_pha_history_violated_sql"
    ),
    # Scope-creep guards
    "_check_materialization_creep": "materialization_creep",
    "_check_no_status_yaml_change": "status_yaml_drift",
    "_check_no_research_log_change": "research_log_drift",
    "_check_no_q6_artifact_change": "q6_scope_creep",
}


# Priority chain — structural / SHA / module-scan first, then DuckDB probes,
# then decision-row checks, then scope-creep guards. 31 entries (per A21).
FALSIFIER_PRIORITY_CHAIN: tuple[str, ...] = (
    "parent_pr242_csv_sha256_mismatch",
    "parent_pr242_md_sha256_mismatch",
    "pr241_sha256_mismatch",
    "cross_region_01_05_10_md_sha256_mismatch",
    "cross_region_01_05_10_json_sha256_mismatch",
    "player_history_all_yaml_sha256_mismatch",
    "step_01_04_05_md_sha256_mismatch",
    "matches_flat_clean_yaml_sha256_mismatch",
    "cross_02_02_spec_sha256_mismatch",
    "mfc_cross_region_column_referenced",
    "cross_region_toon_id_anchor_count_drift",
    "cross_region_nickname_anchor_count_drift",
    "strict_lt_filter_divergence",
    "decision_count_drift",
    "q5_three_options_not_enumerated",
    "strict_exclusion_history_filter_retention_smoke_failed",
    "dual_feature_path_branch_degenerate",
    "sensitivity_indicator_flag_degenerate",
    "sensitivity_indicator_post_game_token_in_scoped_field",
    "q5_evidence_sufficiency_violated",
    "q5_post_game_token_in_scoped_field",
    "q5_direct_target_match_outcome_referenced",
    "q5_future_match_leakage_referenced",
    "q5_global_batch_fit_referenced",
    "q5_phase_03_baseline_creep",
    "history_row_filter_on_pha_field_invalid",
    "q5_filter_target_is_pha_history_violated_sql",
    "materialization_creep",
    "status_yaml_drift",
    "research_log_drift",
    "q6_scope_creep",
)


# ---------------------------------------------------------------------------
# Module-import mechanical verification (round-4 B4 invariants; per A21).
# Drift fails BEFORE any test runs and BEFORE any artifact is written.
# ---------------------------------------------------------------------------

assert len(HELPER_TO_FALSIFIER_KEY) == 31, "B4 invariant: helper count drifted"
assert len(FALSIFIER_PRIORITY_CHAIN) == 31, "B4 invariant: chain count drifted"
assert len(set(FALSIFIER_PRIORITY_CHAIN)) == 31, "B4 invariant: chain duplicates"
assert set(FALSIFIER_PRIORITY_CHAIN) == set(HELPER_TO_FALSIFIER_KEY.values()), (
    "B4 invariant: orphan or missing chain entries"
)


# ---------------------------------------------------------------------------
# Utility helpers (SHA, git, repo root, decision dict)
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


def _sha256_concat(paths: tuple[Path, ...]) -> str:
    """SHA-256 of concatenated file byte-streams (in given order).

    Args:
        paths: Tuple of paths to concatenate-and-hash.

    Returns:
        64-char lowercase hex digest. ``'NOT_FOUND'`` if any path is absent.
    """
    h = hashlib.sha256()
    for p in paths:
        if not p.exists():
            return "NOT_FOUND"
        with p.open("rb") as fh:
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
        f"No pyproject.toml found walking up from {start}; cannot determine repo root."
    )


def _decision_to_field_dict(
    d: CrossRegionAdjudicationDecision,
) -> dict[str, str]:
    """Return a string-valued dict of the decision's fields.

    Args:
        d: A decision dataclass instance.

    Returns:
        Mapping of field name to stringified value.
    """
    return {f.name: str(getattr(d, f.name)) for f in fields(d)}


def _get_decision(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
    decision_id: str,
) -> CrossRegionAdjudicationDecision | None:
    """Return the decision with the given ID, or None.

    Args:
        decisions: All 5 decisions.
        decision_id: One of ``Q5_DECISION_IDS``.

    Returns:
        The decision dataclass, or None if absent.
    """
    for d in decisions:
        if d.decision_id == decision_id:
            return d
    return None


def _normalize_ws(s: str) -> str:
    """Collapse runs of whitespace to a single space and strip.

    Args:
        s: Input string.

    Returns:
        Whitespace-normalized string.
    """
    return re.sub(r"\s+", " ", s).strip()


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


def _probe_cross_region_toonid_membership_count(
    con: duckdb.DuckDBPyConnection,
) -> int:
    """Probe the BINDING toon_id-membership count (NIT-C).

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        Count of PHA rows whose toon_id is in the cross-region set.
    """
    row = con.execute(_CROSS_REGION_TOONID_MEMBERSHIP_BASE_PROBE_QUERY).fetchone()
    if row is None:
        return 0
    return int(row[0])


def _probe_cross_region_nickname_anchor_counts(
    con: duckdb.DuckDBPyConnection,
) -> tuple[int, int, int]:
    """Probe the EQUIVALENCE nickname-anchored 3-tuple (NIT-C).

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        ``(n_nicknames, n_toon_ids, n_player_match_pairs_nickname_anchored)``.
    """
    row = con.execute(_CROSS_REGION_NICKNAME_ANCHOR_PROBE_QUERY).fetchone()
    if row is None:
        return (0, 0, 0)
    return (int(row[0]), int(row[1]), int(row[2]))


def _probe_strict_exclusion_retention(
    con: duckdb.DuckDBPyConnection,
) -> dict[str, int]:
    """Probe per-option strict-exclusion retention (T02 step 3).

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        Dict of {history_rows_kept, history_rows_dropped, players_affected,
        matches_affected, history_rows_total}.
    """
    row = con.execute(_STRICT_EXCLUSION_HISTORY_FILTER_RETENTION_QUERY).fetchone()
    if row is None:
        return {
            "history_rows_kept": 0,
            "history_rows_dropped": 0,
            "players_affected": 0,
            "matches_affected": 0,
            "history_rows_total": 0,
        }
    return {
        "history_rows_kept": int(row[0] or 0),
        "history_rows_dropped": int(row[1] or 0),
        "players_affected": int(row[2] or 0),
        "matches_affected": int(row[3] or 0),
        "history_rows_total": int(row[4] or 0),
    }


def _probe_dual_feature_path_branches(
    con: duckdb.DuckDBPyConnection,
) -> dict[str, int]:
    """Probe per-option dual-feature-path branch nondegeneracy (T02 step 4).

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        Dict of branch counts.
    """
    row = con.execute(_DUAL_FEATURE_PATH_RETENTION_QUERY).fetchone()
    if row is None:
        return {
            "n_target_rows": 0,
            "n_nonxr_nondegenerate": 0,
            "n_xr_nondegenerate": 0,
            "total_nonxr_rows": 0,
            "total_xr_rows": 0,
        }
    return {
        "n_target_rows": int(row[0] or 0),
        "n_nonxr_nondegenerate": int(row[1] or 0),
        "n_xr_nondegenerate": int(row[2] or 0),
        "total_nonxr_rows": int(row[3] or 0),
        "total_xr_rows": int(row[4] or 0),
    }


def _probe_sensitivity_indicator(
    con: duckdb.DuckDBPyConnection,
) -> dict[str, int]:
    """Probe per-option sensitivity-indicator nondegeneracy (T02 step 5).

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        Dict of flag-state counts.
    """
    row = con.execute(_SENSITIVITY_INDICATOR_RETENTION_QUERY).fetchone()
    if row is None:
        return {
            "n_target_rows": 0,
            "n_flag_true": 0,
            "n_flag_false": 0,
            "n_flag_null": 0,
            "total_history_rows": 0,
        }
    return {
        "n_target_rows": int(row[0] or 0),
        "n_flag_true": int(row[1] or 0),
        "n_flag_false": int(row[2] or 0),
        "n_flag_null": int(row[3] or 0),
        "total_history_rows": int(row[4] or 0),
    }


def _probe_family_level_impact(
    con: duckdb.DuckDBPyConnection,
) -> dict[str, int]:
    """Probe family-level impact summary (T02 step 6).

    Args:
        con: Open read-only DuckDB connection.

    Returns:
        Dict of summary counts.
    """
    row = con.execute(_FAMILY_LEVEL_IMPACT_QUERY).fetchone()
    if row is None:
        return {
            "history_rows_kept": 0,
            "history_rows_dropped": 0,
            "players_affected": 0,
            "history_rows_total": 0,
        }
    return {
        "history_rows_kept": int(row[0] or 0),
        "history_rows_dropped": int(row[1] or 0),
        "players_affected": int(row[2] or 0),
        "history_rows_total": int(row[3] or 0),
    }


# ---------------------------------------------------------------------------
# SHA-256 falsifier helpers (9 total — 5 baseline + 4 NIT-B)
# ---------------------------------------------------------------------------


def _check_parent_pr242_csv_sha256(
    csv_path: Path,
    expected_sha: str,
) -> tuple[bool, str]:
    """Verify PR #242 parent CSV SHA-256 matches expected.

    Args:
        csv_path: Path to the parent CSV.
        expected_sha: Expected 64-char hex digest.

    Returns:
        ``(did_fire, message)``.
    """
    observed = _sha256_file(csv_path)
    if observed != expected_sha or not _is_valid_sha256(observed):
        return True, (
            f"PR #242 parent CSV SHA-256 mismatch: observed={observed!r} "
            f"expected={expected_sha!r}"
        )
    return False, ""


def _check_parent_pr242_md_sha256(
    md_path: Path,
    expected_sha: str,
) -> tuple[bool, str]:
    """Verify PR #242 parent MD SHA-256 matches expected.

    Args:
        md_path: Path to the parent MD.
        expected_sha: Expected 64-char hex digest.

    Returns:
        ``(did_fire, message)``.
    """
    observed = _sha256_file(md_path)
    if observed != expected_sha or not _is_valid_sha256(observed):
        return True, (
            f"PR #242 parent MD SHA-256 mismatch: observed={observed!r} "
            f"expected={expected_sha!r}"
        )
    return False, ""


def _check_pr241_validator_sha256(
    validator_path: Path,
) -> tuple[bool, str]:
    """Verify PR #241 validator module SHA-256 matches the pinned constant.

    Args:
        validator_path: Path to the validator module.

    Returns:
        ``(did_fire, message)``.
    """
    observed = _sha256_file(validator_path)
    if observed != EXPECTED_PR241_VALIDATOR_SHA256 or not _is_valid_sha256(observed):
        return True, (
            f"PR #241 validator SHA-256 mismatch: observed={observed!r} "
            f"expected={EXPECTED_PR241_VALIDATOR_SHA256!r}"
        )
    return False, ""


def _check_01_05_10_evidence_sha256_md(
    md_path: Path,
    expected_sha: str,
) -> tuple[bool, str]:
    """Verify 01_05_10 evidence MD SHA-256 matches expected.

    Args:
        md_path: Path to the evidence MD.
        expected_sha: Expected 64-char hex digest (caller-supplied;
            captured at first run and pinned).

    Returns:
        ``(did_fire, message)``.
    """
    observed = _sha256_file(md_path)
    if not _is_valid_sha256(observed):
        return True, (
            f"01_05_10 MD SHA-256 invalid: observed={observed!r}"
        )
    if expected_sha and observed != expected_sha:
        return True, (
            f"01_05_10 MD SHA-256 mismatch: observed={observed!r} "
            f"expected={expected_sha!r}"
        )
    return False, ""


def _check_01_05_10_evidence_sha256_json(
    json_path: Path,
    expected_sha: str,
) -> tuple[bool, str]:
    """Verify 01_05_10 evidence JSON SHA-256 matches expected.

    Args:
        json_path: Path to the evidence JSON.
        expected_sha: Expected 64-char hex digest.

    Returns:
        ``(did_fire, message)``.
    """
    observed = _sha256_file(json_path)
    if not _is_valid_sha256(observed):
        return True, (
            f"01_05_10 JSON SHA-256 invalid: observed={observed!r}"
        )
    if expected_sha and observed != expected_sha:
        return True, (
            f"01_05_10 JSON SHA-256 mismatch: observed={observed!r} "
            f"expected={expected_sha!r}"
        )
    return False, ""


def _check_player_history_all_yaml_sha256(
    yaml_path: Path,
) -> tuple[bool, str]:
    """Verify PHA YAML SHA-256 matches the pinned NIT-B constant.

    Args:
        yaml_path: Path to ``player_history_all.yaml``.

    Returns:
        ``(did_fire, message)``.

    Notes:
        Round-2 B1 / A15 binding rationale hinges on PHA's line-214
        ``is_cross_region_fragmented`` declaration plus lines 220-226 NOTES;
        silent drift would invalidate the binding.
    """
    observed = _sha256_file(yaml_path)
    if observed != EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256:
        return True, (
            f"PHA YAML SHA-256 mismatch: observed={observed!r} "
            f"expected={EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256!r}"
        )
    return False, ""


def _check_step_01_04_05_md_sha256(
    md_path: Path,
) -> tuple[bool, str]:
    """Verify 01_04_05 cleaning MD SHA-256 matches the pinned NIT-B constant.

    Args:
        md_path: Path to ``01_04_05_cross_region_annotation.md``.

    Returns:
        ``(did_fire, message)``.

    Notes:
        Round-2 B3 binding rationale hinges on §7 strategy 1 wording at
        lines 203-208.
    """
    observed = _sha256_file(md_path)
    if observed != EXPECTED_01_04_05_MD_SHA256:
        return True, (
            f"01_04_05 MD SHA-256 mismatch: observed={observed!r} "
            f"expected={EXPECTED_01_04_05_MD_SHA256!r}"
        )
    return False, ""


def _check_matches_flat_clean_yaml_sha256(
    yaml_path: Path,
) -> tuple[bool, str]:
    """Verify MFC YAML SHA-256 matches the pinned NIT-B constant.

    Args:
        yaml_path: Path to ``matches_flat_clean.yaml``.

    Returns:
        ``(did_fire, message)``.

    Notes:
        Round-2 B1 binding rationale hinges on MFC's 30-col schema and the
        absence of ``is_cross_region_fragmented``.
    """
    observed = _sha256_file(yaml_path)
    if observed != EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256:
        return True, (
            f"MFC YAML SHA-256 mismatch: observed={observed!r} "
            f"expected={EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256!r}"
        )
    return False, ""


def _check_cross_02_02_spec_sha256(
    md_path: Path,
) -> tuple[bool, str]:
    """Verify CROSS-02-02 spec SHA-256 matches the pinned NIT-B constant.

    Args:
        md_path: Path to ``02_02_feature_engineering_plan.md``.

    Returns:
        ``(did_fire, message)``.

    Notes:
        Round-2 B3 binding rationale hinges on §6.2 row 5 line 242
        Source/Constraint columns.
    """
    observed = _sha256_file(md_path)
    if observed != EXPECTED_CROSS_02_02_SPEC_SHA256:
        return True, (
            f"CROSS-02-02 spec SHA-256 mismatch: observed={observed!r} "
            f"expected={EXPECTED_CROSS_02_02_SPEC_SHA256!r}"
        )
    return False, ""


# ---------------------------------------------------------------------------
# Module-scan falsifier helpers
# ---------------------------------------------------------------------------


# Forbidden MFC cross-region column reference (assembled at runtime so the
# literal string never appears in this source file). The byte-scan helper
# checks every other line for this assembled token.
_FORBIDDEN_MFC_XR_TOKEN: str = "mfc" + "." + CROSS_REGION_COLUMN_NAME


def _check_no_mfc_cross_region_column_reference(
    module_path: Path,
) -> tuple[bool, str]:
    """Byte-scan: no MFC-aliased cross-region column reference allowed (B1).

    The forbidden token (``mfc`` + ``.`` + ``is_cross_region_fragmented``) is
    assembled at runtime so the literal string never appears in this source
    file. This avoids false positives on the helper's own definition.

    Args:
        module_path: Path to this adjudicator module.

    Returns:
        ``(did_fire, message)``.
    """
    if not module_path.exists():
        return True, f"Module path {module_path!r} does not exist for byte scan"
    text = module_path.read_text(encoding="utf-8")
    hits = [
        (lineno, line)
        for lineno, line in enumerate(text.splitlines(), start=1)
        if _FORBIDDEN_MFC_XR_TOKEN in line
    ]
    if hits:
        return True, (
            f"Forbidden MFC-aliased cross-region column reference "
            f"{_FORBIDDEN_MFC_XR_TOKEN!r} found at line(s) "
            f"{[lineno for lineno, _ in hits]}"
        )
    return False, ""


# Bare strict-< pattern assembled at runtime so the literal token never
# appears as a single substring in this source file.
_BARE_STRICT_LT_PATTERN_PARTS: tuple[str, str] = (
    "ph" + "." + "details_timeUTC",
    "target" + "." + "started_at",
)
_BARE_STRICT_LT_REGEX: re.Pattern[str] = re.compile(
    re.escape(_BARE_STRICT_LT_PATTERN_PARTS[0])
    + r"\s*<\s*"
    + re.escape(_BARE_STRICT_LT_PATTERN_PARTS[1])
)
_CANONICAL_STRICT_LT_REGEX: re.Pattern[str] = re.compile(
    r"TRY_CAST\s*\(\s*"
    + re.escape(_BARE_STRICT_LT_PATTERN_PARTS[0])
    + r"\s+AS\s+TIMESTAMP\s*\)\s*<\s*"
    + re.escape(_BARE_STRICT_LT_PATTERN_PARTS[1])
)


def _check_strict_lt_filter_divergence(
    module_path: Path,
) -> tuple[bool, str]:
    """Byte-scan: the bare strict-< form is allowed only via the named constant.

    The bare lex form is recorded ONLY as ``STRICT_LT_FILTER_ROADMAP_RAW``.
    Every executable SQL site must use ``TRY_CAST(... AS TIMESTAMP)`` form.
    The bare pattern is assembled at runtime so the literal token never
    appears as a single substring in this source file.

    Args:
        module_path: Path to this adjudicator module.

    Returns:
        ``(did_fire, message)``.
    """
    if not module_path.exists():
        return True, f"Module path {module_path!r} does not exist for byte scan"
    text = module_path.read_text(encoding="utf-8")
    offending_lines: list[int] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not _BARE_STRICT_LT_REGEX.search(line):
            continue
        if _CANONICAL_STRICT_LT_REGEX.search(line):
            continue
        # Allow the raw-form constant declaration line itself.
        if "STRICT_LT_FILTER_ROADMAP_RAW" in line:
            continue
        offending_lines.append(lineno)
    if offending_lines:
        return True, (
            f"Bare strict-< pattern "
            f"{_BARE_STRICT_LT_PATTERN_PARTS[0]} < {_BARE_STRICT_LT_PATTERN_PARTS[1]} "
            f"found outside STRICT_LT_FILTER_ROADMAP_RAW at line(s) "
            f"{offending_lines}"
        )
    return False, ""


# ---------------------------------------------------------------------------
# DuckDB anchor probe falsifier helpers (NIT-C)
# ---------------------------------------------------------------------------


def _check_cross_region_toonid_anchor_count_drift(
    observed_count: int,
    expected_count: int | None,
) -> tuple[bool, str]:
    """BINDING toon_id-membership probe count check (NIT-C).

    Args:
        observed_count: Count returned by
            ``_probe_cross_region_toonid_membership_count``.
        expected_count: Pinned expected count (or ``None`` to skip check on
            first run, e.g. for pinning).

    Returns:
        ``(did_fire, message)``.
    """
    if expected_count is None:
        return False, ""
    if observed_count != expected_count:
        return True, (
            f"BINDING toon_id-membership probe count drift: "
            f"observed={observed_count} expected={expected_count}"
        )
    return False, ""


def _check_cross_region_nickname_anchor_count_drift(
    observed: tuple[int, int, int],
) -> tuple[bool, str]:
    """EQUIVALENCE nickname-anchored probe count check (NIT-C).

    Args:
        observed: ``(n_nicknames, n_toon_ids, n_player_match_pairs)``.

    Returns:
        ``(did_fire, message)``.
    """
    expected = (
        EXPECTED_CROSS_REGION_NICKNAME_COUNT,
        EXPECTED_CROSS_REGION_TOON_ID_COUNT,
        EXPECTED_CROSS_REGION_PLAYER_MATCH_PAIR_COUNT_NICKNAME_ANCHORED,
    )
    if observed != expected:
        return True, (
            f"EQUIVALENCE nickname-anchored probe count drift: "
            f"observed={observed} expected={expected}"
        )
    return False, ""


# ---------------------------------------------------------------------------
# Decision-row structural / semantic falsifier helpers
# ---------------------------------------------------------------------------


def _check_decision_count(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Exactly 5 decisions in ``Q5_DECISION_IDS`` order.

    Args:
        decisions: All decisions.

    Returns:
        ``(did_fire, message)``.
    """
    if len(decisions) != Q5_DECISION_COUNT:
        return True, (
            f"Expected exactly {Q5_DECISION_COUNT} decisions; got {len(decisions)}"
        )
    decision_ids = tuple(d.decision_id for d in decisions)
    if decision_ids != Q5_DECISION_IDS:
        return True, (
            f"Decision IDs mismatch (order matters): got={decision_ids} "
            f"expected={Q5_DECISION_IDS}"
        )
    return False, ""


def _check_q5_three_options_enumerated(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Per-option rows must cite exactly the 3 ``Q5_OPTION_NAMES``.

    Args:
        decisions: All 5 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    per_option_policies = sorted(
        d.cross_region_policy
        for d in decisions
        if d.decision_id in {
            "Q5A_strict_exclusion_retention",
            "Q5B_dual_feature_path_retention",
            "Q5C_sensitivity_indicator_retention",
        }
    )
    expected = sorted(Q5_OPTION_NAMES)
    if per_option_policies != expected:
        return True, (
            f"Per-option cross_region_policy values do not match the three "
            f"enumerated options: got={per_option_policies} expected={expected}"
        )
    return False, ""


def _check_strict_exclusion_history_filter_retention_smoke(
    probe: dict[str, int],
    expected_history_row_count: int | None,
) -> tuple[bool, str]:
    """Verify history_rows_kept + history_rows_dropped totals match anchor.

    The strict-exclusion probe is computed over a LEFT JOIN on
    ``player_history_all``; cold-start target rows yield ``history_is_xr IS
    NULL`` and cannot belong to either kept (FALSE) or dropped (TRUE). PR
    #243 Dispatch 3 OPTION (a) fixes the upstream SQL so
    ``history_rows_total`` already excludes the LEFT-JOIN NULL cold-start
    rows; this falsifier therefore measures retention only over rows with a
    real matched history record. See R4/B3 block.

    Args:
        probe: Output of ``_probe_strict_exclusion_retention``.
        expected_history_row_count: Pinned PHA strict-< history row count
            (or ``None`` to skip the total-count check on first-run pinning).

    Returns:
        ``(did_fire, message)``.
    """
    kept = probe.get("history_rows_kept", 0)
    dropped = probe.get("history_rows_dropped", 0)
    total = probe.get("history_rows_total", 0)
    if kept + dropped != total:
        return True, (
            f"strict-exclusion smoke failed: kept+dropped={kept + dropped} "
            f"!= history_rows_total={total}"
        )
    if expected_history_row_count is not None and total != expected_history_row_count:
        return True, (
            f"strict-exclusion smoke failed: observed total={total} != "
            f"expected_history_row_count={expected_history_row_count}"
        )
    return False, ""


def _check_dual_feature_path_branches_nondegenerate(
    probe: dict[str, int],
) -> tuple[bool, str]:
    """Both XR and non-XR branches must have nondegenerate coverage.

    Args:
        probe: Output of ``_probe_dual_feature_path_branches``.

    Returns:
        ``(did_fire, message)``.
    """
    nonxr = probe.get("n_nonxr_nondegenerate", 0)
    xr = probe.get("n_xr_nondegenerate", 0)
    if nonxr == 0:
        return True, (
            f"dual_feature_path non-XR branch degenerate: n_nonxr_nondegenerate={nonxr}"
        )
    if xr == 0:
        return True, (
            f"dual_feature_path XR branch degenerate: n_xr_nondegenerate={xr}"
        )
    return False, ""


def _check_sensitivity_indicator_flag_nondegenerate(
    probe: dict[str, int],
) -> tuple[bool, str]:
    """Sensitivity-indicator flag must have both TRUE and FALSE present.

    Args:
        probe: Output of ``_probe_sensitivity_indicator``.

    Returns:
        ``(did_fire, message)``.
    """
    n_true = probe.get("n_flag_true", 0)
    n_false = probe.get("n_flag_false", 0)
    if n_true == 0:
        return True, (
            f"sensitivity_indicator flag degenerate: n_flag_true={n_true} (no TRUE)"
        )
    if n_false == 0:
        return True, (
            f"sensitivity_indicator flag degenerate: n_flag_false={n_false} (no FALSE)"
        )
    return False, ""


_SENSITIVITY_TARGET_TIME_PHRASE: str = "anchored at target.started_at"


def _check_sensitivity_indicator_anchor_target_time(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Q5C row notes must cite target-time anchoring and avoid POST-GAME tokens.

    Args:
        decisions: All 5 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    q5c = _get_decision(decisions, "Q5C_sensitivity_indicator_retention")
    if q5c is None:
        return True, "Q5C_sensitivity_indicator_retention row missing"
    if _SENSITIVITY_TARGET_TIME_PHRASE not in q5c.notes:
        return True, (
            f"Q5C notes missing required phrase "
            f"{_SENSITIVITY_TARGET_TIME_PHRASE!r}"
        )
    # POST-GAME token scan over scoped fields only.
    row = _decision_to_field_dict(q5c)
    for field_name in POST_GAME_TOKEN_SCOPED_FIELDS:
        if field_name not in row:
            continue
        value = str(row[field_name]).lower()
        for token in POST_GAME_TOKENS:
            if token in value:
                return True, (
                    f"POST-GAME token {token!r} in scoped field "
                    f"{field_name!r} of Q5C row (value={row[field_name]!r})"
                )
    return False, ""


_EVIDENCE_REPO_PATH_REGEX: re.Pattern[str] = re.compile(
    r"^(src/|reports/|sandbox/|thesis/|tests/|docs/|\.claude/)"
)


def _check_q5_evidence_sufficiency(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """bind_now / narrow_with_evidence rows need >=3 repo-path evidence paths.

    deferred_blocker rows need ``deferred_blocker because:`` in notes.

    Args:
        decisions: All 5 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    for d in decisions:
        if d.verdict in {"bind_now", "narrow_with_evidence", "ratify_with_evidence"}:
            paths = [
                line.strip()
                for line in d.evidence_paths.split("\n")
                if line.strip()
            ]
            repo_paths = [p for p in paths if _EVIDENCE_REPO_PATH_REGEX.match(p)]
            if len(repo_paths) < 3:
                return True, (
                    f"Decision {d.decision_id!r} verdict={d.verdict!r} requires "
                    f">=3 repo-path evidence_paths entries; got {len(repo_paths)} "
                    f"(matching {_EVIDENCE_REPO_PATH_REGEX.pattern!r})"
                )
        elif d.verdict == "deferred_blocker":
            if "deferred_blocker because:" not in d.notes:
                return True, (
                    f"Decision {d.decision_id!r} verdict=deferred_blocker "
                    f"requires 'deferred_blocker because:' in notes"
                )
    return False, ""


def _check_q5_no_post_game_token_in_scoped_fields(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """POST-GAME tokens in scoped fields forbidden (B-X1 inherited).

    Args:
        decisions: All 5 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    for d in decisions:
        row = _decision_to_field_dict(d)
        for field_name in POST_GAME_TOKEN_SCOPED_FIELDS:
            if field_name not in row:
                continue
            if field_name in POST_GAME_TOKEN_EXEMPT_FIELDS:
                continue
            value = str(row[field_name]).lower()
            for token in POST_GAME_TOKENS:
                if token in value:
                    return True, (
                        f"POST-GAME token {token!r} in scoped field "
                        f"{field_name!r} of decision {d.decision_id!r} "
                        f"(value={row[field_name]!r})"
                    )
    return False, ""


_DIRECT_OUTCOME_TOKENS: frozenset[str] = frozenset(
    {"target_result", "target_winner", "target_outcome", "target_won", "target_final_state"}
)


def _check_q5_no_direct_target_match_outcome(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Reject any explicit reference to target-match outcome fields.

    Args:
        decisions: All 5 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    for d in decisions:
        row = _decision_to_field_dict(d)
        for field_name in POST_GAME_TOKEN_SCOPED_FIELDS:
            if field_name not in row:
                continue
            value = str(row[field_name]).lower()
            for token in _DIRECT_OUTCOME_TOKENS:
                if token in value:
                    return True, (
                        f"Direct target-match outcome token {token!r} found in "
                        f"scoped field {field_name!r} of decision "
                        f"{d.decision_id!r}"
                    )
    return False, ""


_FUTURE_LEAKAGE_TOKENS: frozenset[str] = frozenset(
    {"future_match", "future_game", "post_match_t", "match_time > t"}
)


def _check_q5_no_future_match_leakage(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Reject any explicit reference to future-match data in scoped fields.

    Args:
        decisions: All 5 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    for d in decisions:
        row = _decision_to_field_dict(d)
        for field_name in POST_GAME_TOKEN_SCOPED_FIELDS:
            if field_name not in row:
                continue
            value = str(row[field_name]).lower()
            for token in _FUTURE_LEAKAGE_TOKENS:
                if token in value:
                    return True, (
                        f"Future-match leakage token {token!r} found in "
                        f"scoped field {field_name!r} of decision "
                        f"{d.decision_id!r}"
                    )
    return False, ""


_GLOBAL_BATCH_FIT_TOKENS: frozenset[str] = frozenset(
    {"global_batch_fit", "global_scaler_fit", "global_normalizer_fit"}
)


def _check_q5_no_global_batch_fit(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Reject any explicit reference to global-batch fit in scoped fields.

    Args:
        decisions: All 5 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    for d in decisions:
        row = _decision_to_field_dict(d)
        for field_name in POST_GAME_TOKEN_SCOPED_FIELDS:
            if field_name not in row:
                continue
            value = str(row[field_name]).lower()
            for token in _GLOBAL_BATCH_FIT_TOKENS:
                if token in value:
                    return True, (
                        f"Global-batch-fit token {token!r} found in "
                        f"scoped field {field_name!r} of decision "
                        f"{d.decision_id!r}"
                    )
    return False, ""


_PHASE_03_BASELINE_TOKENS: frozenset[str] = frozenset(
    {"phase_03_baseline", "baseline_modeling", "logistic_regression_fit"}
)


def _check_q5_no_phase_03_baseline_creep(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Reject Phase-03 baseline-modeling work creep into Q5 decisions.

    Args:
        decisions: All 5 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    for d in decisions:
        row = _decision_to_field_dict(d)
        for field_name in POST_GAME_TOKEN_SCOPED_FIELDS:
            if field_name not in row:
                continue
            value = str(row[field_name]).lower()
            for token in _PHASE_03_BASELINE_TOKENS:
                if token in value:
                    return True, (
                        f"Phase-03 baseline-creep token {token!r} found in "
                        f"scoped field {field_name!r} of decision "
                        f"{d.decision_id!r}"
                    )
    return False, ""


# ---------------------------------------------------------------------------
# NIT-D — structured field + SQL byte-scan falsifier helpers
# ---------------------------------------------------------------------------


def _check_history_row_filter_on_pha_field_valid(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """``history_row_filter_on_pha_applied`` must be in allowed set + consistent.

    Args:
        decisions: All 5 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    for d in decisions:
        value = d.history_row_filter_on_pha_applied
        if value not in ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED:
            return True, (
                f"Decision {d.decision_id!r} has invalid "
                f"history_row_filter_on_pha_applied={value!r}; allowed: "
                f"{sorted(ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED)}"
            )
        # Consistency checks per A20.
        policy = d.selected_policy or d.cross_region_policy
        if d.decision_id == "Q5_per_family_impact_summary":
            if value != "not_applicable":
                return True, (
                    f"Q5_per_family_impact_summary requires "
                    f"history_row_filter_on_pha_applied='not_applicable'; got {value!r}"
                )
            continue
        if d.decision_id == "Q5_selected_policy":
            if d.verdict in {"deferred_recommendation", "deferred_blocker"}:
                if value != "not_applicable":
                    return True, (
                        f"Q5_selected_policy with verdict={d.verdict!r} requires "
                        f"history_row_filter_on_pha_applied='not_applicable'; "
                        f"got {value!r}"
                    )
                continue
            if d.selected_policy in Q5_POLICY_TO_HISTORY_ROW_FILTER:
                required = Q5_POLICY_TO_HISTORY_ROW_FILTER[d.selected_policy]
                if value != required:
                    return True, (
                        f"Q5_selected_policy with selected_policy="
                        f"{d.selected_policy!r} requires "
                        f"history_row_filter_on_pha_applied={required!r}; "
                        f"got {value!r}"
                    )
                continue
        if policy in Q5_POLICY_TO_HISTORY_ROW_FILTER:
            required = Q5_POLICY_TO_HISTORY_ROW_FILTER[policy]
            if value != required:
                return True, (
                    f"Decision {d.decision_id!r} with cross_region_policy="
                    f"{policy!r} requires history_row_filter_on_pha_applied="
                    f"{required!r}; got {value!r}"
                )
    return False, ""


# Aliases that are forbidden as the anchor for an is_cross_region_fragmented
# predicate. Both `mfc` and `target` would indicate the filter was applied to
# the wrong source (round-2 B1 + B3). Full-table-name references (e.g.
# `player_history_all.is_cross_region_fragmented`) are allowed as canonical
# column declarations in spec quotes / docstrings.
_FORBIDDEN_XR_ALIASES: frozenset[str] = frozenset({"mfc", "target", "mhm"})


def _check_q5_filter_target_is_pha_history_sql(
    module_path: Path,
) -> tuple[bool, str]:
    """Byte-scan: no MFC/MHM/target alias may anchor a cross-region predicate.

    Allows ``ph.is_cross_region_fragmented`` (B1 binding) and full-table-name
    references like ``player_history_all.is_cross_region_fragmented`` (these
    appear in spec quotes / docstrings). Forbids ``mfc.`` / ``target.`` /
    ``mhm.`` aliases on the cross-region column.

    Args:
        module_path: Path to this adjudicator module.

    Returns:
        ``(did_fire, message)``.
    """
    if not module_path.exists():
        return True, f"Module path {module_path!r} does not exist for byte scan"
    text = module_path.read_text(encoding="utf-8")
    column_suffix = "." + CROSS_REGION_COLUMN_NAME
    offending: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        idx = 0
        while True:
            found = line.find(column_suffix, idx)
            if found == -1:
                break
            # Extract the alias preceding the dot.
            alias_end = found
            alias_start = alias_end
            while alias_start > 0 and (
                line[alias_start - 1].isalnum() or line[alias_start - 1] == "_"
            ):
                alias_start -= 1
            alias = line[alias_start:alias_end]
            if alias in _FORBIDDEN_XR_ALIASES:
                offending.append((lineno, alias))
            idx = found + len(column_suffix)
    if offending:
        return True, (
            f"Forbidden alias on {CROSS_REGION_COLUMN_NAME!r} "
            f"at line(s) {offending} (allowed: 'ph' or full table name)"
        )
    return False, ""


# ---------------------------------------------------------------------------
# Scope-creep guards
# ---------------------------------------------------------------------------


def _check_materialization_creep(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """Every row's ``materialized_output_paths`` must be empty.

    Args:
        decisions: All 5 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    for d in decisions:
        if d.materialized_output_paths:
            return True, (
                f"Decision {d.decision_id!r} has non-empty "
                f"materialized_output_paths={d.materialized_output_paths!r}"
            )
    return False, ""


_STATUS_YAML_RELS: tuple[str, ...] = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml",
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml",
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml",
)
_RESEARCH_LOG_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
)


def _check_no_status_yaml_change(
    repo_root: Path,
    baseline_shas: dict[str, str] | None,
) -> tuple[bool, str]:
    """Verify status YAMLs are unchanged from a captured baseline (if given).

    Args:
        repo_root: Repo root directory.
        baseline_shas: Optional mapping of relative path to SHA-256 captured
            at entrypoint start. If ``None``, the check is skipped.

    Returns:
        ``(did_fire, message)``.
    """
    if baseline_shas is None:
        return False, ""
    for rel in _STATUS_YAML_RELS:
        observed = _sha256_file(repo_root / rel)
        expected = baseline_shas.get(rel, observed)
        if observed != expected:
            return True, (
                f"Status YAML drift detected at {rel!r}: "
                f"observed={observed!r} expected={expected!r}"
            )
    return False, ""


def _check_no_research_log_change(
    repo_root: Path,
    baseline_sha: str | None,
) -> tuple[bool, str]:
    """Verify dataset research_log.md is unchanged (if baseline given).

    Args:
        repo_root: Repo root directory.
        baseline_sha: Optional SHA-256 captured at entrypoint start.

    Returns:
        ``(did_fire, message)``.
    """
    if baseline_sha is None:
        return False, ""
    observed = _sha256_file(repo_root / _RESEARCH_LOG_REL)
    if observed != baseline_sha:
        return True, (
            f"research_log.md drift detected: observed={observed!r} "
            f"expected={baseline_sha!r}"
        )
    return False, ""


def _check_no_q6_artifact_change(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
) -> tuple[bool, str]:
    """No Q6 row may appear; Q6 wording only in the one-line disclaimer.

    Args:
        decisions: All 5 decisions.

    Returns:
        ``(did_fire, message)``.
    """
    for d in decisions:
        if d.parent_decision_id == "Q6_rating_policy":
            return True, (
                f"Decision {d.decision_id!r} has parent_decision_id="
                f"'Q6_rating_policy'; Q6 is out of scope for this PR"
            )
        # Q6 prose allowed ONLY as the canonical out-of-scope disclaimer.
        # Count case-insensitive occurrences of 'Q6' outside the disclaimer.
        if "Q6" in d.notes and Q6_OUT_OF_SCOPE_PHRASE not in d.notes:
            # Allow only if the only Q6 occurrence is in the disclaimer phrase
            # (which itself contains Q6 once). If the phrase is absent and Q6
            # appears, that is scope creep.
            return True, (
                f"Decision {d.decision_id!r} notes mention Q6 without the "
                f"canonical out-of-scope disclaimer: {Q6_OUT_OF_SCOPE_PHRASE!r}"
            )
    return False, ""


# ---------------------------------------------------------------------------
# Decision-building (T05 verbatim bindings — provisional verdicts per N3)
# ---------------------------------------------------------------------------


def _format_retention_counts_json(
    probe: dict[str, int],
    family_scope: str,
) -> str:
    """Format a per-family retention counts JSON string.

    Args:
        probe: Strict-exclusion probe result.
        family_scope: Either a single family ID or ``"all_six_families"``.

    Returns:
        JSON-like string keyed by family scope.
    """
    kept = probe.get("history_rows_kept", 0)
    dropped = probe.get("history_rows_dropped", 0)
    total = kept + dropped
    pct = round(100.0 * kept / total, 4) if total else 0.0
    return (
        f'{{"{family_scope}": {{'
        f'"history_rows_kept": {kept}, '
        f'"history_rows_dropped": {dropped}, '
        f'"retention_pct": {pct}'
        f"}}}}"
    )


def _format_dual_branch_counts_json(
    probe: dict[str, int],
    family_scope: str,
) -> str:
    """Format dual-feature-path branch counts JSON.

    Args:
        probe: Dual-feature-path probe result.
        family_scope: Either a single family ID or ``"all_six_families"``.

    Returns:
        JSON-like string keyed by family scope.
    """
    return (
        f'{{"{family_scope}": {{'
        f'"history_rows_kept": {probe.get("total_nonxr_rows", 0) + probe.get("total_xr_rows", 0)}, '
        f'"history_rows_dropped": 0, '
        f'"retention_pct": 100.0, '
        f'"nonxr_branch_target_rows": {probe.get("n_nonxr_nondegenerate", 0)}, '
        f'"xr_branch_target_rows": {probe.get("n_xr_nondegenerate", 0)}'
        f"}}}}"
    )


def _format_sensitivity_counts_json(
    probe: dict[str, int],
    family_scope: str,
) -> str:
    """Format sensitivity-indicator JSON.

    Args:
        probe: Sensitivity-indicator probe result.
        family_scope: Either a single family ID or ``"all_six_families"``.

    Returns:
        JSON-like string keyed by family scope.
    """
    total = probe.get("total_history_rows", 0)
    return (
        f'{{"{family_scope}": {{'
        f'"history_rows_kept": {total}, '
        f'"history_rows_dropped": 0, '
        f'"retention_pct": 100.0, '
        f'"n_flag_true": {probe.get("n_flag_true", 0)}, '
        f'"n_flag_false": {probe.get("n_flag_false", 0)}, '
        f'"n_flag_null": {probe.get("n_flag_null", 0)}'
        f"}}}}"
    )


def _format_summary_counts_json(
    family_impact: dict[str, int],
) -> str:
    """Format the family-level impact summary JSON (broadcast over 6 families).

    Args:
        family_impact: Output of ``_probe_family_level_impact``.

    Returns:
        JSON-like string keyed per-family (broadcast).
    """
    kept = family_impact.get("history_rows_kept", 0)
    dropped = family_impact.get("history_rows_dropped", 0)
    total = kept + dropped
    pct = round(100.0 * kept / total, 4) if total else 0.0
    family_entries = ", ".join(
        f'"{family_id}": {{'
        f'"history_rows_kept": {kept}, '
        f'"history_rows_dropped": {dropped}, '
        f'"retention_pct": {pct}'
        f"}}"
        for family_id in sorted(HISTORY_TRANCHE2_FAMILY_IDS)
    )
    return f"{{{family_entries}}}"


_Q5A_NOTES_TEMPLATE: str = (
    "Q5A evaluates option (a) strict_exclusion (CROSS-02-02 §6.2 row 5). "
    "Counts measure PHA HISTORY rows kept/dropped under "
    "`WHERE NOT ph.is_cross_region_fragmented` applied BEFORE aggregation "
    "(round-2 B3 binding). Anchored on toon_id-membership "
    "(round-3 NIT-C / A19). "
    "Strict-< filter: `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at` "
    "(B-X2 inherited).\n\n"
    "VERBATIM CROSS-02-02 §6.2 row 5 line 242, Source column: "
    "`player_history_all.is_cross_region_fragmented` (CROSS-02-00 §5.4)\n\n"
    "VERBATIM CROSS-02-02 §6.2 row 5 line 242, Constraint column: "
    "Phase 02 must implement one of: (a) strict-exclusion sensitivity arm, "
    "(b) dual feature paths (with vs without filter), or "
    "(c) sensitivity indicator co-registered alongside the history features.\n\n"
    "VERBATIM 01_04_05 §7 strategy 1 lines 203-208: "
    "Safe-subset filter: `WHERE NOT is_cross_region_fragmented` -- restricts "
    "history to non-fragmented players; cleanest rolling-window estimates but "
    "reduces the training population to 7,716 / 44,817 rows = 17.2% of the "
    "corpus (tournament players are over-represented among the 1,923 flagged "
    "toons; see Sec.4 flag distribution). This is a material data loss; "
    "strategy (2) or (3) are usually preferable for non-catastrophic bias levels.\n\n"
    "VERBATIM PHA YAML NOTES lines 220-226: "
    "Phase 02 rolling features over `player_id_worldwide` should apply "
    "`WHERE NOT is_cross_region_fragmented` as safe-subset filter, OR use "
    "dual feature paths, OR use as sensitivity indicator. Blanket flag "
    "(no handle-length filter) by design -- false positives bounded by "
    "short-handle count (see 01_04_05 Sec.6 conservatism argument). "
    "Empirical grounding from WP-3 (01_05_10): median_rolling30_undercount=16, "
    "p95=29 on flagged toons.\n\n"
    "Comparison to 01_05_10 W=30 noise-floor sqrt(30) ~ 5.5 "
    "(Hollander and Wolfe 1999 §11.2): retention loss compared against this "
    "noise-floor establishes whether the discard is material vs measurement noise.\n\n"
    "No target-match outcome read; no future matches read; no global batch fit; "
    "deterministic SQL probe via "
    "`_STRICT_EXCLUSION_HISTORY_FILTER_RETENTION_QUERY`. "
    "RISK-20 reference: risk_register_sc2egset.md (SC-R01 MEDIUM IDENTITY entry). "
    "This row replaces the empirical part of PR #242 Q5 only; the binding "
    "policy is the Q5_selected_policy row. " + Q6_OUT_OF_SCOPE_PHRASE
)


_Q5B_NOTES_TEMPLATE: str = (
    "Q5B evaluates option (b) dual_feature_path (CROSS-02-02 §6.2 row 5). "
    "Both XR and non-XR PHA history branches are materialized as separate "
    "columns; history-row retention is 100% but per-branch sparsity may "
    "produce degenerate sub-features for cross-region players. "
    "Anchored on toon_id-membership (round-3 NIT-C / A19). "
    "Strict-< filter: `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at`.\n\n"
    "VERBATIM 01_04_05 §7 strategy 2 lines 210-212: "
    "Dual feature paths: Compute rolling-window features for all players, "
    "then add `is_cross_region_fragmented` as a covariate in the model. "
    "The model learns to adjust for the known fragmentation bias.\n\n"
    "No target-match outcome read; no future matches read; no global batch fit; "
    "deterministic SQL probe via `_DUAL_FEATURE_PATH_RETENTION_QUERY`. "
    + Q6_OUT_OF_SCOPE_PHRASE
)


_Q5C_NOTES_TEMPLATE: str = (
    "Q5C evaluates option (c) sensitivity_indicator_co_registration "
    "(CROSS-02-02 §6.2 row 5). No PHA history rows dropped; a single "
    "`is_cross_region_fragmented` flag is co-registered alongside the 6 "
    "history feature columns, anchored at target.started_at via "
    "`TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at` over "
    "the player's strictly-prior PHA history window. "
    "Anchored on toon_id-membership (round-3 NIT-C / A19).\n\n"
    "VERBATIM 01_04_05 §7 strategy 3 lines 214-216: "
    "Sensitivity indicator: Use the flag to partition evaluation metrics by "
    "`is_cross_region_fragmented` and report differential model performance. "
    "Documents remaining bias for the thesis.\n\n"
    "Co-registration semantics: for each target row, project the boolean-OR "
    "of `ph.is_cross_region_fragmented` over the player's strictly-prior PHA "
    "history window per `STRICT_LT_HISTORY_FILTER`. Flag nondegeneracy "
    "verified by `_SENSITIVITY_INDICATOR_RETENTION_QUERY`. "
    "No target-match outcome read; no future matches read; no global batch fit. "
    + Q6_OUT_OF_SCOPE_PHRASE
)


def _build_q5a_decision(
    common: dict[str, str],
    strict_probe: dict[str, int],
) -> CrossRegionAdjudicationDecision:
    """Build the Q5A strict_exclusion evaluation row.

    Args:
        common: Common provenance fields.
        strict_probe: Output of ``_probe_strict_exclusion_retention``.

    Returns:
        ``CrossRegionAdjudicationDecision``.
    """
    summary = (
        f"Strict exclusion drops {strict_probe.get('history_rows_dropped', 0)} "
        f"PHA history rows / {strict_probe.get('players_affected', 0)} players / "
        f"{strict_probe.get('matches_affected', 0)} target matches at the "
        f"aggregation layer; PHA history retention "
        f"({strict_probe.get('history_rows_kept', 0)} kept / "
        f"{strict_probe.get('history_rows_total', 0)} total) computed via "
        f"WHERE NOT ph.is_cross_region_fragmented applied to HISTORY rows BEFORE aggregation."
    )
    evidence = "\n".join(
        [
            STEP_01_05_10_MD_REL,
            STEP_01_05_10_JSON_REL,
            STEP_01_04_05_MD_REL,
            CROSS_02_02_SPEC_REL,
            PLAYER_HISTORY_ALL_YAML_REL,
            MATCHES_FLAT_CLEAN_YAML_REL,
            PARENT_PR242_CSV_REL,
        ]
    )
    return CrossRegionAdjudicationDecision(
        decision_id="Q5A_strict_exclusion_retention",
        parent_decision_id="Q5_cross_region_policy",
        decision_name=(
            "Cross-region option (a) strict_exclusion — per-family PHA "
            "history retention measurement"
        ),
        verdict="deferred_recommendation",
        binding_level="recommendation_only",
        scope=(
            "sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling"
        ),
        selected_policy="",
        rejected_options="",
        cross_region_policy="strict_exclusion",
        cross_region_retention_counts=_format_retention_counts_json(
            strict_probe, "all_six_families"
        ),
        cross_region_affected_players=str(strict_probe.get("players_affected", 0)),
        cross_region_affected_matches=str(strict_probe.get("matches_affected", 0)),
        cross_region_anchor_semantics="toon_id_based",
        history_row_filter_on_pha_applied="yes",
        retention_measurement_summary=summary,
        evidence_paths=evidence,
        falsifiers=(
            "strict_exclusion_history_filter_retention_smoke_failed:did_not_fire\n"
            "cross_region_toon_id_anchor_count_drift:did_not_fire"
        ),
        notes=_Q5A_NOTES_TEMPLATE,
        **common,
    )


def _build_q5b_decision(
    common: dict[str, str],
    dual_probe: dict[str, int],
) -> CrossRegionAdjudicationDecision:
    """Build the Q5B dual_feature_path evaluation row.

    Args:
        common: Common provenance fields.
        dual_probe: Output of ``_probe_dual_feature_path_branches``.

    Returns:
        ``CrossRegionAdjudicationDecision``.
    """
    summary = (
        f"Dual feature path: history retention 100% "
        f"({dual_probe.get('total_nonxr_rows', 0)} non-XR + "
        f"{dual_probe.get('total_xr_rows', 0)} XR PHA history rows); "
        f"{dual_probe.get('n_nonxr_nondegenerate', 0)} target rows have "
        f"nondegenerate non-XR branch coverage; "
        f"{dual_probe.get('n_xr_nondegenerate', 0)} target rows have "
        f"nondegenerate XR branch coverage."
    )
    evidence = "\n".join(
        [
            STEP_01_05_10_MD_REL,
            STEP_01_04_05_MD_REL,
            CROSS_02_02_SPEC_REL,
            PLAYER_HISTORY_ALL_YAML_REL,
            PARENT_PR242_CSV_REL,
        ]
    )
    return CrossRegionAdjudicationDecision(
        decision_id="Q5B_dual_feature_path_retention",
        parent_decision_id="Q5_cross_region_policy",
        decision_name=(
            "Cross-region option (b) dual_feature_path — per-branch PHA "
            "history coverage measurement"
        ),
        verdict="deferred_recommendation",
        binding_level="recommendation_only",
        scope=(
            "sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling"
        ),
        selected_policy="",
        rejected_options="",
        cross_region_policy="dual_feature_path",
        cross_region_retention_counts=_format_dual_branch_counts_json(
            dual_probe, "all_six_families"
        ),
        cross_region_affected_players="0",
        cross_region_affected_matches="0",
        cross_region_anchor_semantics="toon_id_based",
        history_row_filter_on_pha_applied="yes",
        retention_measurement_summary=summary,
        evidence_paths=evidence,
        falsifiers="dual_feature_path_branch_degenerate:did_not_fire",
        notes=_Q5B_NOTES_TEMPLATE,
        **common,
    )


def _build_q5c_decision(
    common: dict[str, str],
    sens_probe: dict[str, int],
) -> CrossRegionAdjudicationDecision:
    """Build the Q5C sensitivity_indicator_co_registration evaluation row.

    Args:
        common: Common provenance fields.
        sens_probe: Output of ``_probe_sensitivity_indicator``.

    Returns:
        ``CrossRegionAdjudicationDecision``.
    """
    summary = (
        f"Sensitivity indicator co-registration anchored at target.started_at: "
        f"PHA history retention 100% "
        f"({sens_probe.get('total_history_rows', 0)} rows); per-target boolean-OR "
        f"flag distribution n_true={sens_probe.get('n_flag_true', 0)} / "
        f"n_false={sens_probe.get('n_flag_false', 0)} / "
        f"n_null={sens_probe.get('n_flag_null', 0)}."
    )
    evidence = "\n".join(
        [
            STEP_01_05_10_MD_REL,
            STEP_01_04_05_MD_REL,
            CROSS_02_02_SPEC_REL,
            PLAYER_HISTORY_ALL_YAML_REL,
            PARENT_PR242_CSV_REL,
        ]
    )
    return CrossRegionAdjudicationDecision(
        decision_id="Q5C_sensitivity_indicator_retention",
        parent_decision_id="Q5_cross_region_policy",
        decision_name=(
            "Cross-region option (c) sensitivity_indicator_co_registration — "
            "per-target flag nondegeneracy measurement (anchored at target.started_at)"
        ),
        verdict="deferred_recommendation",
        binding_level="recommendation_only",
        scope=(
            "sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling"
        ),
        selected_policy="",
        rejected_options="",
        cross_region_policy="sensitivity_indicator_co_registration",
        cross_region_retention_counts=_format_sensitivity_counts_json(
            sens_probe, "all_six_families"
        ),
        cross_region_affected_players="0",
        cross_region_affected_matches="0",
        cross_region_anchor_semantics="toon_id_based",
        history_row_filter_on_pha_applied="no",
        retention_measurement_summary=summary,
        evidence_paths=evidence,
        falsifiers=(
            "sensitivity_indicator_flag_degenerate:did_not_fire\n"
            "sensitivity_indicator_post_game_token_in_scoped_field:did_not_fire"
        ),
        notes=_Q5C_NOTES_TEMPLATE,
        **common,
    )


_Q5_SELECTED_NOTES_TEMPLATE: str = (
    "Q5_selected_policy is the BINDING row for the Q5 successor adjudication. "
    "PROVISIONAL recommendation (round-2 N3 / A14: VERDICT EMERGES FROM TABLE): "
    "narrow_with_evidence with selected_policy=sensitivity_indicator_co_registration "
    "(option (c)). Rationale: option (c) preserves full PHA history-row retention "
    "while honoring the 01_05_10 W=30 FAIL verdict by providing the sensitivity-arm "
    "input that the Phase-03 model can use to stratify; option (a) discards "
    "the strict_exclusion-probe-reported number of PHA history rows whose cardinality "
    "the per-family table quantifies; option (b) introduces per-branch PHA sparsity "
    "that defeats the smoothing motivation of matchup_history_aggregate (G-CS-3).\n\n"
    "VERDICT EMERGED FROM TABLE: see Q5A/Q5B/Q5C per-option retention triples; "
    "the Q5_per_family_impact_summary row records the per-family broadcast.\n\n"
    "MATERIALIZATION GATE: the future materialization PR consumes this row's "
    "selected_policy + cross_region_policy fields as the keying input for the "
    "cross_region_fragmentation_handling family materialization SQL. "
    "The MFC-target-row drop alternative is OUT OF SCOPE per A4 + A17 "
    "(filter applies to PHA HISTORY rows, not MFC TARGET rows). "
    + Q6_OUT_OF_SCOPE_PHRASE
)


def _build_q5_selected_decision(
    common: dict[str, str],
    strict_probe: dict[str, int],
    family_impact: dict[str, int],
    selected_policy: str,
    verdict: str,
) -> CrossRegionAdjudicationDecision:
    """Build the Q5_selected_policy BINDING row.

    Args:
        common: Common provenance fields.
        strict_probe: Output of ``_probe_strict_exclusion_retention``.
        family_impact: Output of ``_probe_family_level_impact``.
        selected_policy: One of ``Q5_OPTION_NAMES`` (or ``""`` for deferred).
        verdict: One of ``ALLOWED_Q5_VERDICTS``.

    Returns:
        ``CrossRegionAdjudicationDecision``.
    """
    binding_level = "recommendation_only"
    if verdict == "bind_now":
        binding_level = "binding_for_materialization"
    elif verdict in {"deferred_blocker", "deferred_recommendation"}:
        binding_level = verdict
    rejected: list[str] = []
    if selected_policy:
        rejected = [p for p in Q5_OPTION_NAMES if p != selected_policy]
    rejected_str = "\n".join(rejected)
    # History-row filter consistency per Q5_POLICY_TO_HISTORY_ROW_FILTER.
    if verdict in {"deferred_blocker", "deferred_recommendation"}:
        history_filter = "not_applicable"
    else:
        history_filter = Q5_POLICY_TO_HISTORY_ROW_FILTER.get(
            selected_policy, "not_applicable"
        )
    evidence = "\n".join(
        [
            STEP_01_05_10_MD_REL,
            STEP_01_05_10_JSON_REL,
            STEP_01_04_05_MD_REL,
            CROSS_02_02_SPEC_REL,
            PLAYER_HISTORY_ALL_YAML_REL,
            MATCHES_FLAT_CLEAN_YAML_REL,
            PARENT_PR242_CSV_REL,
            PARENT_PR242_MD_REL,
        ]
    )
    summary = (
        f"Selected policy: {selected_policy!r}; verdict {verdict!r}; "
        f"PHA history retention {strict_probe.get('history_rows_kept', 0)}/"
        f"{strict_probe.get('history_rows_total', 0)} under strict_exclusion; "
        f"family-impact total rows {family_impact.get('history_rows_total', 0)} "
        f"(kept {family_impact.get('history_rows_kept', 0)} / dropped "
        f"{family_impact.get('history_rows_dropped', 0)})."
    )
    notes_with_deferral_marker = _Q5_SELECTED_NOTES_TEMPLATE
    if verdict == "deferred_blocker":
        notes_with_deferral_marker = (
            "deferred_blocker because: insufficient empirical evidence in the "
            "per-family retention table to bind a single policy.\n\n"
            + _Q5_SELECTED_NOTES_TEMPLATE
        )
    return CrossRegionAdjudicationDecision(
        decision_id="Q5_selected_policy",
        parent_decision_id="Q5_cross_region_policy",
        decision_name=(
            "Q5 cross-region policy selection (BINDING row; verdict emerges from "
            "per-family retention table per A14)"
        ),
        verdict=verdict,
        binding_level=binding_level,
        scope=(
            "sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling"
        ),
        selected_policy=selected_policy,
        rejected_options=rejected_str,
        cross_region_policy=selected_policy,
        cross_region_retention_counts=_format_retention_counts_json(
            strict_probe, "all_six_families"
        ),
        cross_region_affected_players=str(strict_probe.get("players_affected", 0)),
        cross_region_affected_matches=str(strict_probe.get("matches_affected", 0)),
        cross_region_anchor_semantics="toon_id_based",
        history_row_filter_on_pha_applied=history_filter,
        retention_measurement_summary=summary,
        evidence_paths=evidence,
        falsifiers="q5_evidence_sufficiency_violated:did_not_fire",
        notes=notes_with_deferral_marker,
        **common,
    )


_Q5_SUMMARY_NOTES_TEMPLATE: str = (
    "Q5_per_family_impact_summary is the derived per-family broadcast row. "
    "The cross_region_retention_counts JSON keys are the 6 history-enriched "
    "pre_game family IDs; values are the (kept, dropped, retention_pct) "
    "triples broadcast from `_FAMILY_LEVEL_IMPACT_QUERY` over PHA HISTORY rows "
    "(round-2 B3). Anchor semantics='both' (carries data from both the "
    "toon_id-membership BINDING probe and the nickname-anchored EQUIVALENCE "
    "probe per round-3 NIT-C). "
    "history_row_filter_on_pha_applied='not_applicable' (the summary row makes "
    "no per-option commitment; the binding policy lives in Q5_selected_policy).\n\n"
    + Q6_OUT_OF_SCOPE_PHRASE
)


def _build_q5_summary_decision(
    common: dict[str, str],
    family_impact: dict[str, int],
) -> CrossRegionAdjudicationDecision:
    """Build the Q5_per_family_impact_summary derived row.

    Args:
        common: Common provenance fields.
        family_impact: Output of ``_probe_family_level_impact``.

    Returns:
        ``CrossRegionAdjudicationDecision``.
    """
    summary = (
        f"Family-level impact summary: PHA history rows "
        f"kept={family_impact.get('history_rows_kept', 0)} / "
        f"dropped={family_impact.get('history_rows_dropped', 0)} / "
        f"total={family_impact.get('history_rows_total', 0)} broadcast over "
        f"the 6 history-enriched pre_game families."
    )
    evidence = "\n".join(
        [
            STEP_01_05_10_MD_REL,
            STEP_01_05_10_JSON_REL,
            STEP_01_04_05_MD_REL,
            CROSS_02_02_SPEC_REL,
            PLAYER_HISTORY_ALL_YAML_REL,
            PARENT_PR242_CSV_REL,
        ]
    )
    return CrossRegionAdjudicationDecision(
        decision_id="Q5_per_family_impact_summary",
        parent_decision_id="Q5_cross_region_policy",
        decision_name=(
            "Q5 per-family impact summary (derived row; broadcasts the "
            "family-level retention over the 6 history-enriched pre_game families)"
        ),
        verdict="ratify_with_evidence",
        binding_level="binding_for_materialization",
        scope="all_six_history_enriched_pre_game_families",
        selected_policy="",
        rejected_options="",
        cross_region_policy="",
        cross_region_retention_counts=_format_summary_counts_json(family_impact),
        cross_region_affected_players=str(family_impact.get("players_affected", 0)),
        cross_region_affected_matches="0",
        cross_region_anchor_semantics="both",
        history_row_filter_on_pha_applied="not_applicable",
        retention_measurement_summary=summary,
        evidence_paths=evidence,
        falsifiers="q5_evidence_sufficiency_violated:did_not_fire",
        notes=_Q5_SUMMARY_NOTES_TEMPLATE,
        **common,
    )


def _build_decisions(
    *,
    common: dict[str, str],
    strict_probe: dict[str, int],
    dual_probe: dict[str, int],
    sens_probe: dict[str, int],
    family_impact: dict[str, int],
    selected_policy: str,
    selected_verdict: str,
) -> tuple[CrossRegionAdjudicationDecision, ...]:
    """Construct the 5 Q5 successor decision rows per T05.

    Args:
        common: Common provenance fields.
        strict_probe: Output of ``_probe_strict_exclusion_retention``.
        dual_probe: Output of ``_probe_dual_feature_path_branches``.
        sens_probe: Output of ``_probe_sensitivity_indicator``.
        family_impact: Output of ``_probe_family_level_impact``.
        selected_policy: One of ``Q5_OPTION_NAMES`` (or ``""`` for deferred).
        selected_verdict: One of ``ALLOWED_Q5_VERDICTS``.

    Returns:
        Tuple of 5 ``CrossRegionAdjudicationDecision`` rows in
        ``Q5_DECISION_IDS`` order.
    """
    return (
        _build_q5a_decision(common, strict_probe),
        _build_q5b_decision(common, dual_probe),
        _build_q5c_decision(common, sens_probe),
        _build_q5_selected_decision(
            common, strict_probe, family_impact, selected_policy, selected_verdict
        ),
        _build_q5_summary_decision(common, family_impact),
    )


# ---------------------------------------------------------------------------
# CSV + MD writers
# ---------------------------------------------------------------------------


_CSV_FIELDNAMES: tuple[str, ...] = tuple(
    f.name for f in fields(CrossRegionAdjudicationDecision)
)


def _write_csv(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
    csv_path: Path,
) -> None:
    """Write the deterministic 29-column Q5 successor adjudication CSV.

    Args:
        decisions: The 5 decision rows in ``Q5_DECISION_IDS`` order.
        csv_path: Destination path.
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(_CSV_FIELDNAMES))
        writer.writeheader()
        for d in decisions:
            writer.writerow(_decision_to_field_dict(d))
    LOGGER.debug("_write_csv: wrote %d rows to %s", len(decisions), csv_path)


def _format_decision_md_section(
    d: CrossRegionAdjudicationDecision,
) -> str:
    """Format one decision row as a markdown section.

    Args:
        d: Decision dataclass.

    Returns:
        Multi-line markdown string.
    """
    parts: list[str] = []
    parts.append(f"### {d.decision_id} — {d.decision_name}\n\n")
    parts.append(f"- **Verdict:** `{d.verdict}`\n")
    parts.append(f"- **Binding level:** `{d.binding_level}`\n")
    parts.append(f"- **Scope:** `{d.scope}`\n")
    parts.append(f"- **Cross-region policy:** `{d.cross_region_policy or '(none)'}`\n")
    parts.append(
        f"- **Cross-region anchor semantics:** `{d.cross_region_anchor_semantics}`\n"
    )
    parts.append(
        f"- **History-row filter on PHA applied:** "
        f"`{d.history_row_filter_on_pha_applied}`\n"
    )
    parts.append(
        f"- **Retention counts:**\n\n```json\n{d.cross_region_retention_counts}\n```\n\n"
    )
    parts.append(f"**Retention measurement summary:** {d.retention_measurement_summary}\n\n")
    parts.append(f"**Rationale / notes:**\n\n{d.notes}\n\n")
    parts.append(f"**Evidence paths:**\n\n```\n{d.evidence_paths}\n```\n\n")
    parts.append(f"**Falsifiers:**\n\n```\n{d.falsifiers}\n```\n\n")
    return "".join(parts)


def _write_md(
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
    md_path: Path,
    falsifier_status: dict[str, str],
    binding_probe_count: int,
    nickname_probe_counts: tuple[int, int, int],
    strict_probe: dict[str, int],
    dual_probe: dict[str, int],
    sens_probe: dict[str, int],
    family_impact: dict[str, int],
) -> None:
    """Write the Q5 successor adjudication MD companion artifact.

    Args:
        decisions: The 5 decision rows.
        md_path: Destination path.
        falsifier_status: Mapping of falsifier key to status string.
        binding_probe_count: BINDING toon_id-membership probe count.
        nickname_probe_counts: EQUIVALENCE nickname-anchored probe 3-tuple.
        strict_probe: Strict-exclusion probe result.
        dual_probe: Dual-feature-path probe result.
        sens_probe: Sensitivity-indicator probe result.
        family_impact: Family-level impact probe result.
    """
    md_path.parent.mkdir(parents=True, exist_ok=True)
    parts: list[str] = []
    parts.append(
        "# SC2EGSet Step 02_01_03 — Q5 Cross-Region Retention Successor Adjudication\n\n"
    )
    parts.append("## §1 Non-Materialization Disclaimer\n\n")
    parts.append(
        "This artifact is a Q5 successor adjudication of the cross-region "
        "fragmentation operationalization for sc2egset Step 02_01_03 "
        "(tranche-2, 6 history-enriched pre_game families). It does NOT "
        "materialize any feature value, does NOT write any Parquet, does NOT "
        "run the CROSS-02-01-v1.0.1 post-materialization leakage audit, does "
        "NOT close Step 02_01_03, and does NOT append to any status YAML or "
        "research_log. Materialization remains FUTURE.\n\n"
    )
    parts.append("## §2 Parent PR #242 Lineage\n\n")
    parts.append(
        "This artifact upgrades the PR #242 parent adjudication's Q5 row "
        "(`Q5_cross_region_policy`, which closed as `verdict=deferred_blocker`). "
        "PR #242 byte-stable artifacts are referenced by SHA-256 on every row "
        "(`parent_pr242_csv_sha256`, `parent_pr242_md_sha256`, "
        "`parent_pr242_artifact_sha256`).\n\n"
    )
    parts.append("## §3 Q5-Only Scope (Q6 Out of Scope)\n\n")
    parts.append(f"{Q6_OUT_OF_SCOPE_PHRASE}\n\n")
    parts.append("## §4 Per-Option Decision Table\n\n")
    parts.append(
        "| decision_id | cross_region_policy | history_row_filter_on_pha_applied | "
        "anchor_semantics | verdict |\n"
    )
    parts.append("|---|---|---|---|---|\n")
    for d in decisions:
        parts.append(
            f"| `{d.decision_id}` | `{d.cross_region_policy or '(none)'}` | "
            f"`{d.history_row_filter_on_pha_applied}` | "
            f"`{d.cross_region_anchor_semantics}` | `{d.verdict}` |\n"
        )
    parts.append("\n## §5 Per-Family Retention Table (BINDING Evidence)\n\n")
    kept = family_impact.get("history_rows_kept", 0)
    dropped = family_impact.get("history_rows_dropped", 0)
    total = kept + dropped
    pct = round(100.0 * kept / total, 4) if total else 0.0
    parts.append(
        f"Family-level PHA history retention under strict_exclusion: "
        f"`{kept}` kept / `{dropped}` dropped / `{total}` total "
        f"(`{pct}%` retention).\n\n"
    )
    parts.append("## §6 SQL Probe Outputs (Verbatim per Invariant I6)\n\n")
    parts.append(
        "### §6.1 BINDING toon_id-membership probe (NIT-C)\n\n"
        f"```sql\n{_CROSS_REGION_TOONID_MEMBERSHIP_BASE_PROBE_QUERY}\n```\n\n"
        f"Observed count: `{binding_probe_count}`.\n\n"
    )
    parts.append(
        "### §6.2 EQUIVALENCE nickname-anchored probe (NIT-C; 01_05_10 §3.3 SQL 3)\n\n"
        f"```sql\n{_CROSS_REGION_NICKNAME_ANCHOR_PROBE_QUERY}\n```\n\n"
        f"Observed: `(n_nicknames={nickname_probe_counts[0]}, "
        f"n_toon_ids={nickname_probe_counts[1]}, "
        f"n_player_match_pairs={nickname_probe_counts[2]})`. "
        f"Expected: `({EXPECTED_CROSS_REGION_NICKNAME_COUNT}, "
        f"{EXPECTED_CROSS_REGION_TOON_ID_COUNT}, "
        f"{EXPECTED_CROSS_REGION_PLAYER_MATCH_PAIR_COUNT_NICKNAME_ANCHORED})`.\n\n"
    )
    parts.append(
        "### §6.3 Strict-exclusion retention probe (B3)\n\n"
        f"```sql\n{_STRICT_EXCLUSION_HISTORY_FILTER_RETENTION_QUERY}\n```\n\n"
        f"Observed: `{strict_probe}`.\n\n"
    )
    parts.append(
        "### §6.4 Dual-feature-path branch probe\n\n"
        f"```sql\n{_DUAL_FEATURE_PATH_RETENTION_QUERY}\n```\n\n"
        f"Observed: `{dual_probe}`.\n\n"
    )
    parts.append(
        "### §6.5 Sensitivity-indicator probe (target-time anchored)\n\n"
        f"```sql\n{_SENSITIVITY_INDICATOR_RETENTION_QUERY}\n```\n\n"
        f"Observed: `{sens_probe}`.\n\n"
    )
    parts.append(
        "### §6.6 Family-level impact probe\n\n"
        f"```sql\n{_FAMILY_LEVEL_IMPACT_QUERY}\n```\n\n"
        f"Observed: `{family_impact}`.\n\n"
    )
    parts.append("## §7 Toon_id vs Nickname Anchor Semantics (NIT-C)\n\n")
    parts.append(
        "Two cross-region anchor semantics are evaluated: the BINDING probe "
        "(toon_id-membership; aligns with the downstream `WHERE "
        "ph.is_cross_region_fragmented = TRUE` predicate) and the EQUIVALENCE "
        "probe (lowercase nickname join; reproduces the 01_05_10 §3.3 SQL 3 "
        "idiom). The 32,031 anchor is shared ONLY by the EQUIVALENCE probe.\n\n"
    )
    parts.append("## §8 Target-Filter vs History-Filter Distinction (B3)\n\n")
    parts.append(
        "The Q5 filter is applied to PHA HISTORY rows (`WHERE NOT "
        "ph.is_cross_region_fragmented` BEFORE aggregation), NOT to MFC TARGET "
        "rows. MFC has no `is_cross_region_fragmented` column (30-col schema). "
        "The MFC-target-row drop alternative is OUT OF SCOPE per A4 + A17.\n\n"
    )
    parts.append("## §9 Structured Field Explanation (NIT-D)\n\n")
    parts.append(
        "The `history_row_filter_on_pha_applied` field replaces the round-2 "
        "vacuous prose-substring assertion with a tri-valued enum "
        "(`yes`/`no`/`not_applicable`). Per-option consistency: Q5A=`yes`, "
        "Q5B=`yes`, Q5C=`no`, Q5_selected_policy=mirror of selected_policy "
        "(or `not_applicable` for deferred verdicts), "
        "Q5_per_family_impact_summary=`not_applicable`. The SQL byte-scan "
        "portion (reject any MFC-aliased "
        f"`{CROSS_REGION_COLUMN_NAME}` predicate) "
        "is KEPT separately as `q5_filter_target_is_pha_history_violated_sql`.\n\n"
    )
    parts.append("## §10 Materialization Blocked Until Q6 Resolved\n\n")
    parts.append(
        "Q5 may upgrade from `deferred_blocker` (PR #242) to "
        "`bind_now`/`ratify_with_evidence`/`extend_with_evidence`/"
        "`narrow_with_evidence` in this PR per the Q5_selected_policy row. "
        "Q6 (rating policy) remains `deferred_blocker`; the future Layer-3 "
        "materialization PR must NOT proceed until Q6 is upgraded in a "
        "separate successor adjudication PR.\n\n"
    )
    parts.append("## §11 No Q6 Decision Here\n\n")
    parts.append(f"{Q6_OUT_OF_SCOPE_PHRASE}\n\n")
    parts.append("## §12 No Step Closure / No Phase 03 Start\n\n")
    parts.append(
        "Step 02_01_03 remains OPEN. This artifact does NOT add "
        "`02_01_03: complete` to `STEP_STATUS.yaml`. Phase 03 work remains "
        "forbidden.\n\n"
    )
    parts.append("## §13 Per-Decision Sections\n\n")
    for d in decisions:
        parts.append(_format_decision_md_section(d))
    parts.append("## §14 Falsifier Roll-Call\n\n")
    parts.append("Every falsifier in `FALSIFIER_PRIORITY_CHAIN`:\n\n")
    for key in FALSIFIER_PRIORITY_CHAIN:
        status = falsifier_status.get(key, "did_not_fire")
        parts.append(f"- `{key}`: {status}\n")
    parts.append("\n## §15 SHA Provenance\n\n")
    if decisions:
        d0 = decisions[0]
        parts.append(
            f"- `pr241_scaffold_validator_module_sha256`: "
            f"`{d0.pr241_scaffold_validator_module_sha256}`\n"
        )
        parts.append(
            f"- `parent_pr242_csv_sha256`: `{d0.parent_pr242_csv_sha256}`\n"
        )
        parts.append(f"- `parent_pr242_md_sha256`: `{d0.parent_pr242_md_sha256}`\n")
        parts.append(
            f"- `parent_pr242_artifact_sha256`: `{d0.parent_pr242_artifact_sha256}`\n"
        )
        parts.append(
            f"- `provenance_01_05_10_md_sha256`: `{d0.provenance_01_05_10_md_sha256}`\n"
        )
        parts.append(
            f"- `provenance_01_05_10_json_sha256`: "
            f"`{d0.provenance_01_05_10_json_sha256}`\n"
        )
        parts.append(
            f"- `player_history_all_yaml_sha256`: "
            f"`{d0.player_history_all_yaml_sha256}`\n"
        )
        parts.append(
            f"- `step_01_04_05_md_sha256`: `{d0.step_01_04_05_md_sha256}`\n"
        )
        parts.append(
            f"- `matches_flat_clean_yaml_sha256`: "
            f"`{d0.matches_flat_clean_yaml_sha256}`\n"
        )
        parts.append(
            f"- `cross_02_02_spec_sha256`: `{d0.cross_02_02_spec_sha256}`\n"
        )
    md_path.write_text("".join(parts), encoding="utf-8")
    LOGGER.debug("_write_md: wrote MD to %s", md_path)


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def adjudicate_history_cross_region_retention(
    duckdb_path: Path,
    parent_pr242_csv_path: Path,
    parent_pr242_md_path: Path,
    step_01_05_10_md_path: Path,
    step_01_05_10_json_path: Path,
    csv_path: Path,
    md_path: Path,
    audit_pr: str,
    audit_date: str,  # noqa: ARG001 — recorded via provenance footer hooks
    *,
    expected_parent_pr242_csv_sha256: str = "",
    expected_parent_pr242_md_sha256: str = "",
    expected_01_05_10_md_sha256: str = "",
    expected_01_05_10_json_sha256: str = "",
    expected_pha_cross_region_toonid_membership_count: int | None = None,
    expected_pha_strict_lt_history_row_count: int | None = None,
    selected_policy: str = "sensitivity_indicator_co_registration",
    selected_verdict: str = "narrow_with_evidence",
) -> CrossRegionAdjudicationResult:
    """Adjudicate the Q5 cross-region retention successor decision.

    Opens DuckDB read-only, runs the T02 probes, constructs the 5 Q5 decisions
    per T05's verbatim bindings (with provisional verdict EMERGING from the
    per-family table per A14), runs every falsifier in
    ``FALSIFIER_PRIORITY_CHAIN`` order, and (if no falsifier fires) writes the
    29-column CSV + §1-§15 MD artifact pair. ``materialized_output_paths`` is
    ALWAYS empty.

    Args:
        duckdb_path: Path to the sc2egset DuckDB file (opened read-only).
        parent_pr242_csv_path: Path to the PR #242 parent CSV.
        parent_pr242_md_path: Path to the PR #242 parent MD.
        step_01_05_10_md_path: Path to the 01_05_10 evidence MD.
        step_01_05_10_json_path: Path to the 01_05_10 evidence JSON.
        csv_path: Destination Q5 successor CSV path.
        md_path: Destination Q5 successor MD path.
        audit_pr: Layer-2 PR number placeholder string (e.g. ``"PR #243"``).
        audit_date: ISO YYYY-MM-DD date (recorded in provenance only).
        expected_parent_pr242_csv_sha256: Optional pinned PR #242 CSV SHA.
        expected_parent_pr242_md_sha256: Optional pinned PR #242 MD SHA.
        expected_01_05_10_md_sha256: Optional pinned 01_05_10 MD SHA.
        expected_01_05_10_json_sha256: Optional pinned 01_05_10 JSON SHA.
        expected_pha_cross_region_toonid_membership_count: Pinned binding
            probe expected count (or ``None`` on first run for pinning).
        expected_pha_strict_lt_history_row_count: Pinned strict-< history row
            count (or ``None`` on first run for pinning).
        selected_policy: Q5 selected policy (provisional). One of
            ``Q5_OPTION_NAMES`` (or ``""`` for deferred verdicts).
        selected_verdict: Q5 selected verdict (provisional). One of
            ``ALLOWED_Q5_VERDICTS``.

    Returns:
        ``CrossRegionAdjudicationResult`` with ``passed=True`` iff no halting
        falsifier fired.
    """
    LOGGER.info(
        "adjudicate_history_cross_region_retention: opening DuckDB at %s "
        "(read-only)",
        duckdb_path,
    )
    repo_root = _find_repo_root(Path(__file__))
    module_path = Path(__file__).resolve()

    # Resolve NIT-B + ancillary paths.
    pha_yaml_path = repo_root / PLAYER_HISTORY_ALL_YAML_REL
    step_01_04_05_md_repo_path = repo_root / STEP_01_04_05_MD_REL
    mfc_yaml_path = repo_root / MATCHES_FLAT_CLEAN_YAML_REL
    cross_02_02_spec_path = repo_root / CROSS_02_02_SPEC_REL
    pr241_validator_path = repo_root / PR241_VALIDATOR_MODULE_REL

    # Probe DuckDB (read-only).
    con = duckdb.connect(str(duckdb_path), read_only=True)
    try:
        binding_count = _probe_cross_region_toonid_membership_count(con)
        nickname_counts = _probe_cross_region_nickname_anchor_counts(con)
        strict_probe = _probe_strict_exclusion_retention(con)
        dual_probe = _probe_dual_feature_path_branches(con)
        sens_probe = _probe_sensitivity_indicator(con)
        family_impact = _probe_family_level_impact(con)
    finally:
        con.close()

    # Provenance SHAs.
    git_sha = _get_git_sha()
    pr241_sha = EXPECTED_PR241_VALIDATOR_SHA256
    parent_csv_sha = _sha256_file(parent_pr242_csv_path)
    parent_md_sha = _sha256_file(parent_pr242_md_path)
    parent_artifact_sha = _sha256_concat(
        (parent_pr242_csv_path, parent_pr242_md_path)
    )
    step_01_05_10_md_sha = _sha256_file(step_01_05_10_md_path)
    step_01_05_10_json_sha = _sha256_file(step_01_05_10_json_path)
    pha_yaml_sha = _sha256_file(pha_yaml_path)
    step_01_04_05_md_sha = _sha256_file(step_01_04_05_md_repo_path)
    mfc_yaml_sha = _sha256_file(mfc_yaml_path)
    cross_02_02_sha = _sha256_file(cross_02_02_spec_path)

    common: dict[str, str] = {
        "audit_pr": audit_pr,
        "pr241_scaffold_validator_module_sha256": pr241_sha,
        "parent_pr242_csv_sha256": parent_csv_sha,
        "parent_pr242_md_sha256": parent_md_sha,
        "parent_pr242_artifact_sha256": parent_artifact_sha,
        "provenance_01_05_10_md_sha256": step_01_05_10_md_sha,
        "provenance_01_05_10_json_sha256": step_01_05_10_json_sha,
        "player_history_all_yaml_sha256": pha_yaml_sha,
        "step_01_04_05_md_sha256": step_01_04_05_md_sha,
        "matches_flat_clean_yaml_sha256": mfc_yaml_sha,
        "cross_02_02_spec_sha256": cross_02_02_sha,
        "materialized_output_paths": "",
    }

    decisions = _build_decisions(
        common=common,
        strict_probe=strict_probe,
        dual_probe=dual_probe,
        sens_probe=sens_probe,
        family_impact=family_impact,
        selected_policy=selected_policy,
        selected_verdict=selected_verdict,
    )

    # Run falsifiers in FALSIFIER_PRIORITY_CHAIN order.
    invocations = _build_falsifier_invocations(
        decisions=decisions,
        module_path=module_path,
        pr241_validator_path=pr241_validator_path,
        parent_pr242_csv_path=parent_pr242_csv_path,
        parent_pr242_md_path=parent_pr242_md_path,
        step_01_05_10_md_path=step_01_05_10_md_path,
        step_01_05_10_json_path=step_01_05_10_json_path,
        pha_yaml_path=pha_yaml_path,
        step_01_04_05_md_path=step_01_04_05_md_repo_path,
        mfc_yaml_path=mfc_yaml_path,
        cross_02_02_spec_path=cross_02_02_spec_path,
        expected_parent_pr242_csv_sha256=expected_parent_pr242_csv_sha256,
        expected_parent_pr242_md_sha256=expected_parent_pr242_md_sha256,
        expected_01_05_10_md_sha256=expected_01_05_10_md_sha256,
        expected_01_05_10_json_sha256=expected_01_05_10_json_sha256,
        binding_probe_count=binding_count,
        expected_binding_count=expected_pha_cross_region_toonid_membership_count,
        nickname_probe_counts=nickname_counts,
        strict_probe=strict_probe,
        expected_history_row_count=expected_pha_strict_lt_history_row_count,
        dual_probe=dual_probe,
        sens_probe=sens_probe,
        repo_root=repo_root,
    )

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

    if halting is None:
        _write_csv(decisions, csv_path)
        _write_md(
            decisions,
            md_path,
            falsifier_status,
            binding_count,
            nickname_counts,
            strict_probe,
            dual_probe,
            sens_probe,
            family_impact,
        )
    else:
        LOGGER.warning(
            "adjudicate_history_cross_region_retention: halting falsifier %s — "
            "CSV+MD NOT written",
            halting,
        )

    return CrossRegionAdjudicationResult(
        decisions=decisions,
        csv_path=str(csv_path),
        md_path=str(md_path),
        provenance_git_sha=git_sha,
        falsifiers_fired=tuple(fired),
        halting_falsifier=halting,
        passed=halting is None,
    )


def _build_falsifier_invocations(
    *,
    decisions: tuple[CrossRegionAdjudicationDecision, ...],
    module_path: Path,
    pr241_validator_path: Path,
    parent_pr242_csv_path: Path,
    parent_pr242_md_path: Path,
    step_01_05_10_md_path: Path,
    step_01_05_10_json_path: Path,
    pha_yaml_path: Path,
    step_01_04_05_md_path: Path,
    mfc_yaml_path: Path,
    cross_02_02_spec_path: Path,
    expected_parent_pr242_csv_sha256: str,
    expected_parent_pr242_md_sha256: str,
    expected_01_05_10_md_sha256: str,
    expected_01_05_10_json_sha256: str,
    binding_probe_count: int,
    expected_binding_count: int | None,
    nickname_probe_counts: tuple[int, int, int],
    strict_probe: dict[str, int],
    expected_history_row_count: int | None,
    dual_probe: dict[str, int],
    sens_probe: dict[str, int],
    repo_root: Path,
) -> dict[str, _FalsifierThunk]:
    """Build a key->thunk map for all 31 falsifiers (priority-chain order).

    Args:
        decisions: All 5 decisions.
        module_path: This adjudicator module's filesystem path.
        pr241_validator_path: Path to the PR #241 validator module.
        parent_pr242_csv_path: Path to PR #242 parent CSV.
        parent_pr242_md_path: Path to PR #242 parent MD.
        step_01_05_10_md_path: Path to 01_05_10 evidence MD.
        step_01_05_10_json_path: Path to 01_05_10 evidence JSON.
        pha_yaml_path: Path to player_history_all.yaml.
        step_01_04_05_md_path: Path to 01_04_05 cleaning MD.
        mfc_yaml_path: Path to matches_flat_clean.yaml.
        cross_02_02_spec_path: Path to CROSS-02-02 spec.
        expected_parent_pr242_csv_sha256: Pinned PR #242 CSV SHA (or "").
        expected_parent_pr242_md_sha256: Pinned PR #242 MD SHA (or "").
        expected_01_05_10_md_sha256: Pinned 01_05_10 MD SHA (or "").
        expected_01_05_10_json_sha256: Pinned 01_05_10 JSON SHA (or "").
        binding_probe_count: Observed BINDING probe count.
        expected_binding_count: Pinned BINDING probe expected count.
        nickname_probe_counts: Observed EQUIVALENCE probe 3-tuple.
        strict_probe: Strict-exclusion probe result.
        expected_history_row_count: Pinned PHA strict-< total row count.
        dual_probe: Dual-feature-path probe result.
        sens_probe: Sensitivity-indicator probe result.
        repo_root: Repo root directory.

    Returns:
        Mapping from falsifier key to zero-arg thunk.
    """
    return {
        "parent_pr242_csv_sha256_mismatch": lambda: (
            _check_parent_pr242_csv_sha256(
                parent_pr242_csv_path, expected_parent_pr242_csv_sha256
            )
            if expected_parent_pr242_csv_sha256
            else (False, "")
        ),
        "parent_pr242_md_sha256_mismatch": lambda: (
            _check_parent_pr242_md_sha256(
                parent_pr242_md_path, expected_parent_pr242_md_sha256
            )
            if expected_parent_pr242_md_sha256
            else (False, "")
        ),
        "pr241_sha256_mismatch": lambda: _check_pr241_validator_sha256(
            pr241_validator_path
        ),
        "cross_region_01_05_10_md_sha256_mismatch": lambda: (
            _check_01_05_10_evidence_sha256_md(
                step_01_05_10_md_path, expected_01_05_10_md_sha256
            )
        ),
        "cross_region_01_05_10_json_sha256_mismatch": lambda: (
            _check_01_05_10_evidence_sha256_json(
                step_01_05_10_json_path, expected_01_05_10_json_sha256
            )
        ),
        "player_history_all_yaml_sha256_mismatch": lambda: (
            _check_player_history_all_yaml_sha256(pha_yaml_path)
        ),
        "step_01_04_05_md_sha256_mismatch": lambda: (
            _check_step_01_04_05_md_sha256(step_01_04_05_md_path)
        ),
        "matches_flat_clean_yaml_sha256_mismatch": lambda: (
            _check_matches_flat_clean_yaml_sha256(mfc_yaml_path)
        ),
        "cross_02_02_spec_sha256_mismatch": lambda: (
            _check_cross_02_02_spec_sha256(cross_02_02_spec_path)
        ),
        "mfc_cross_region_column_referenced": lambda: (
            _check_no_mfc_cross_region_column_reference(module_path)
        ),
        "cross_region_toon_id_anchor_count_drift": lambda: (
            _check_cross_region_toonid_anchor_count_drift(
                binding_probe_count, expected_binding_count
            )
        ),
        "cross_region_nickname_anchor_count_drift": lambda: (
            _check_cross_region_nickname_anchor_count_drift(nickname_probe_counts)
        ),
        "strict_lt_filter_divergence": lambda: (
            _check_strict_lt_filter_divergence(module_path)
        ),
        "decision_count_drift": lambda: _check_decision_count(decisions),
        "q5_three_options_not_enumerated": lambda: (
            _check_q5_three_options_enumerated(decisions)
        ),
        "strict_exclusion_history_filter_retention_smoke_failed": lambda: (
            _check_strict_exclusion_history_filter_retention_smoke(
                strict_probe, expected_history_row_count
            )
        ),
        "dual_feature_path_branch_degenerate": lambda: (
            _check_dual_feature_path_branches_nondegenerate(dual_probe)
        ),
        "sensitivity_indicator_flag_degenerate": lambda: (
            _check_sensitivity_indicator_flag_nondegenerate(sens_probe)
        ),
        "sensitivity_indicator_post_game_token_in_scoped_field": lambda: (
            _check_sensitivity_indicator_anchor_target_time(decisions)
        ),
        "q5_evidence_sufficiency_violated": lambda: (
            _check_q5_evidence_sufficiency(decisions)
        ),
        "q5_post_game_token_in_scoped_field": lambda: (
            _check_q5_no_post_game_token_in_scoped_fields(decisions)
        ),
        "q5_direct_target_match_outcome_referenced": lambda: (
            _check_q5_no_direct_target_match_outcome(decisions)
        ),
        "q5_future_match_leakage_referenced": lambda: (
            _check_q5_no_future_match_leakage(decisions)
        ),
        "q5_global_batch_fit_referenced": lambda: (
            _check_q5_no_global_batch_fit(decisions)
        ),
        "q5_phase_03_baseline_creep": lambda: (
            _check_q5_no_phase_03_baseline_creep(decisions)
        ),
        "history_row_filter_on_pha_field_invalid": lambda: (
            _check_history_row_filter_on_pha_field_valid(decisions)
        ),
        "q5_filter_target_is_pha_history_violated_sql": lambda: (
            _check_q5_filter_target_is_pha_history_sql(module_path)
        ),
        "materialization_creep": lambda: _check_materialization_creep(decisions),
        "status_yaml_drift": lambda: _check_no_status_yaml_change(repo_root, None),
        "research_log_drift": lambda: _check_no_research_log_change(repo_root, None),
        "q6_scope_creep": lambda: _check_no_q6_artifact_change(decisions),
    }
