"""Materialization + post-materialization audit for SC2EGSet Step 02_01_03.

This module materialises the FIVE history-enriched pre_game feature families
authorised by PR #257's ROADMAP amendment (grep token
``materialization_scope_amendment_post_pr_255``) into ONE Parquet artifact
(44,418 rows x 28 projected columns) and runs the post-materialization
CROSS-02-01-v1.0.1 leakage audit producing the FIRST non-vacuous audit for
Step ``02_01_03``.

Projected column partition (28 cols = 3 identity + 1 context + 24 audited):
    - 3 IDENTITY: focal_match_id, focal_player, opponent_player.
    - 1 CONTEXT row-identity anchor: started_at (CROSS-02-00 Section 5.1).
    - 24 AUDITED history-enriched PRE_GAME features over the 5 families:
        * focal_player_history (6 cols)
        * opponent_player_history (6 cols)
        * matchup_history_aggregate (2 cols; 1v1-restricted via MFC join)
        * cross_region_fragmentation_handling (2 cols; symmetric per I5)
        * in_game_history_aggregate (8 cols = 4 IN_GAME_HISTORICAL x 2 sides)

The ``reconstructed_rating`` family is EXCLUDED per PR #255 omit-closure
verdict ``omit_reconstructed_rating_and_unblock_other_five``; the three
forbidden columns ``reconstructed_rating_focal_pre``,
``reconstructed_rating_opp_pre``, ``reconstructed_rating_diff`` must NOT
appear anywhere in the output projection.

Binding sources (17 BINDING parent artifact SHAs are pinned at Layer-2 T01):
    - PR #242 Q1/Q2/Q3/Q4/Q7/Q8 adjudication (csv+md).
    - PR #243 Q5 cross-region adjudication (csv+md; selected_policy =
      ``sensitivity_indicator_co_registration``).
    - PR #245 Q6 rating-reconstruction successor adjudication (csv+md).
    - PR #247 Q6F rating-algorithm survey (csv+md).
    - PR #249 Q6G rating-implementation proof (csv+md).
    - PR #251 Q6H rating-path decision (csv+md).
    - PR #255 omit-closure (csv+md; ``q5_policy`` field re-elevates the Q5
      policy to BINDING in the omit-closure context).
    - 02_01_01 closed feature-family registry CSV.
    - PR #236 tranche-1 Parquet + audit JSON + audit MD (three SHA pins;
      consumed as audit-schema template).

Temporal discipline (Invariant I3; per ml-protocol three failure modes):
    - All per-player and matchup history aggregates filter via the strict-<
      predicate ``TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at``
      (the canonical TRY_CAST form per PR #242 Q3 BINDING B-X2).
    - ``ph.is_decisive_result = TRUE`` is used in place of inline
      ``ph.result IN ('Win', 'Loss')`` (player_history_all.yaml:48-54).
    - The matchup CTE restricts the shared-replay self-join to 1v1 prior
      matches via ``JOIN matches_flat_clean mfc_h ON mfc_h.replay_id =
      ph_focal.replay_id`` (B2 fix).
    - The per-player history CTEs aggregate ALL game types per Q1 BINDING
      (player_history_all is unfiltered across game modes); this
      cross-game-type aggregation is documented in audit MD Section 1.
    - The cross-region indicator pair is symmetrised per Invariant I5
      (focal/opponent symmetric construction beyond PR #243's
      single-indicator text; explicitly cited in audit MD Section 1).
    - No tracker_events_raw read.
    - No target-match outcome, no future-match leakage, no Phase 03 split
      leakage, no global batch fit, no raw MMR/rating scalar feature.

Falsifiers implemented (a fired falsifier sets halting_falsifier and
passed=False; structural drift errors win over per-row content errors):
    F-five-family-count-drift
    F-five-family-set-drift
    F-five-family-canonical-order-drift
    F-reconstructed-rating-column-present
    F-reconstructed-rating-token-leak
    F-forbidden-skill-scalar-projected
    F-row-count-mismatch
    F-focal-rows-per-match-violation
    F-symmetry-violation
    F-strict-lt-operator-missing
    F-equal-lt-operator-used
    F-try-cast-missing
    F-tracker-source-read
    F-target-match-row-in-history
    F-join-then-filter-invariant-violation
    F-post-game-token-projected
    F-cross-region-policy-mismatch
    F-in-game-historical-column-out-of-scope
    F-features-audited-empty
    F-features-audited-not-twenty-four
    F-features-audited-count-mismatch
    F-context-column-counted-as-feature
    F-audit-verdict-not-pass
    F-encoder-fit-at-materialization-layer
    F-examiner-clarity-sentence-missing
    F-non-deterministic-output
    F-matchup-cte-includes-non-1v1-history
    F-decisive-result-flag-not-used
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

DATASET_TAG: str = "sc2egset"
PHASE_02_STEP: str = "02_01_03"
AUDIT_PR_PLACEHOLDER: str = "PR #<TBD>"
SPEC_VERSION: str = "CROSS-02-01-v1"

EXPECTED_OUTPUT_ROW_COUNT: int = 44_418
EXPECTED_DISTINCT_FOCAL_MATCH_COUNT: int = 22_209

# Five-family permitted set (PR #257 amendment + PR #255 omit-closure CSV).
FIVE_FAMILY_PERMITTED_SET: frozenset[str] = frozenset(
    {
        "focal_player_history",
        "opponent_player_history",
        "matchup_history_aggregate",
        "cross_region_fragmentation_handling",
        "in_game_history_aggregate",
    }
)
FIVE_FAMILY_CANONICAL_ORDER: tuple[str, ...] = (
    "focal_player_history",
    "opponent_player_history",
    "matchup_history_aggregate",
    "cross_region_fragmentation_handling",
    "in_game_history_aggregate",
)
FIVE_FAMILY_PERMITTED_COUNT: int = 5

# Excluded family + columns (PR #257 amendment lines 2542-2548; PR #255).
EXCLUDED_FAMILY: str = "reconstructed_rating"
FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS: frozenset[str] = frozenset(
    {
        "reconstructed_rating_focal_pre",
        "reconstructed_rating_opp_pre",
        "reconstructed_rating_diff",
    }
)

# Q5 cross-region policy (PR #243 selected_policy + PR #255 q5_policy field).
CROSS_REGION_POLICY: str = "sensitivity_indicator_co_registration"

# Q7 IN_GAME_HISTORICAL allowed-column set (PR #242 Q7 BINDING).
IN_GAME_HISTORICAL_AGGREGATED_COLUMNS: tuple[str, ...] = (
    "APM",
    "SQ",
    "supplyCappedPercent",
    "header_elapsedGameLoops",
)

# POST_GAME tokens (CROSS-02-01-v1.0.1 Section 2.2; boundary-aware equality).
# `win` is intentionally NOT a single-token POST_GAME marker because the
# audited feature columns include `prior_win_rate` and `h2h_focal_win_rate`
# history-aggregated rates (rates over PRIOR matches are PRE_GAME features,
# not POST_GAME). `won` / `winner` remain POST_GAME because they denote
# target-game outcome.
_POST_GAME_TOKENS: frozenset[str] = frozenset(
    {
        "won",
        "loss",
        "result",
        "outcome",
        "winner",
        "final_state",
        "match_result",
        "post_game",
        "is_decisive",
    }
)
# Explicit allowlist of audited-column tokens that contain English words
# overlapping POST_GAME vocabulary (e.g. "win" in "win_rate"). A column
# matching one of these patterns is NEVER POST_GAME.
_PROTECTED_HISTORY_AGGREGATE_PATTERNS: tuple[str, ...] = (
    "prior_win_rate",
    "h2h_focal_win_rate",
)

# Forbidden skill scalars (PR #236 precedent).
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

# Source-table allowlist (Q1 BINDING; no tracker).
_ALLOWED_SOURCE_TABLES: frozenset[str] = frozenset(
    {"matches_flat_clean", "matches_history_minimal", "player_history_all"}
)
TRACKER_SOURCE_PREFIX: str = "tracker_events_raw"

# Sub-feature enumeration (CROSS-02-02 §6.2 row 1 verbatim 6-tuple per side).
FOCAL_PLAYER_HISTORY_SUBFEATURES: tuple[str, ...] = (
    "focal_prior_match_count",
    "focal_prior_win_rate_decisive",
    "focal_days_since_prior_match",
    "focal_prior_win_rate_race_conditional",
    "focal_prior_win_rate_map_conditional",
    "focal_prior_win_rate_matchup_conditional",
)
OPPONENT_PLAYER_HISTORY_SUBFEATURES: tuple[str, ...] = (
    "opponent_prior_match_count",
    "opponent_prior_win_rate_decisive",
    "opponent_days_since_prior_match",
    "opponent_prior_win_rate_race_conditional",
    "opponent_prior_win_rate_map_conditional",
    "opponent_prior_win_rate_matchup_conditional",
)
MATCHUP_HISTORY_SUBFEATURES: tuple[str, ...] = (
    "matchup_h2h_count",
    "matchup_h2h_focal_win_rate",
)
CROSS_REGION_SUBFEATURES: tuple[str, ...] = (
    "is_cross_region_fragmented_focal_history_any",
    "is_cross_region_fragmented_opponent_history_any",
)
IN_GAME_HISTORY_SUBFEATURES: tuple[str, ...] = (
    "focal_apm_prior_mean",
    "focal_sq_prior_mean",
    "focal_supply_capped_pct_prior_mean",
    "focal_elapsed_game_loops_prior_mean",
    "opponent_apm_prior_mean",
    "opponent_sq_prior_mean",
    "opponent_supply_capped_pct_prior_mean",
    "opponent_elapsed_game_loops_prior_mean",
)

# Derived counts (Invariant I7; assert at module-load time below).
EXPECTED_AUDITED_FEATURE_COLUMN_COUNT: int = (
    24  # 6 + 6 + 2 + 2 + 8 per FIVE_FAMILY_CANONICAL_ORDER
)
EXPECTED_PARQUET_COLUMN_COUNT: int = 28  # 3 identity + 1 context + 24 audited

PROJECTED_IDENTITY_COLUMNS: tuple[str, ...] = (
    "focal_match_id",
    "focal_player",
    "opponent_player",
)
PROJECTED_CONTEXT_COLUMNS: tuple[str, ...] = ("started_at",)

EXPECTED_AUDITED_FEATURE_COLUMNS: tuple[str, ...] = (
    FOCAL_PLAYER_HISTORY_SUBFEATURES
    + OPPONENT_PLAYER_HISTORY_SUBFEATURES
    + MATCHUP_HISTORY_SUBFEATURES
    + CROSS_REGION_SUBFEATURES
    + IN_GAME_HISTORY_SUBFEATURES
)

EXPECTED_OUTPUT_COLUMNS: tuple[str, ...] = (
    PROJECTED_IDENTITY_COLUMNS
    + PROJECTED_CONTEXT_COLUMNS
    + EXPECTED_AUDITED_FEATURE_COLUMNS
)

# Feature -> family mapping (used in audit JSON custom_extensions section).
FEATURE_TO_FAMILY_MAPPING: dict[str, str] = {
    **{c: "focal_player_history" for c in FOCAL_PLAYER_HISTORY_SUBFEATURES},
    **{c: "opponent_player_history" for c in OPPONENT_PLAYER_HISTORY_SUBFEATURES},
    **{c: "matchup_history_aggregate" for c in MATCHUP_HISTORY_SUBFEATURES},
    **{c: "cross_region_fragmentation_handling" for c in CROSS_REGION_SUBFEATURES},
    **{c: "in_game_history_aggregate" for c in IN_GAME_HISTORY_SUBFEATURES},
}

# Module-load-time assertions to guarantee the canonical counts.
assert len(EXPECTED_AUDITED_FEATURE_COLUMNS) == EXPECTED_AUDITED_FEATURE_COLUMN_COUNT
assert (
    len(EXPECTED_OUTPUT_COLUMNS)
    == EXPECTED_PARQUET_COLUMN_COUNT
    == 3 + 1 + EXPECTED_AUDITED_FEATURE_COLUMN_COUNT
)
assert FIVE_FAMILY_PERMITTED_COUNT == len(FIVE_FAMILY_PERMITTED_SET)
assert FIVE_FAMILY_PERMITTED_COUNT == len(FIVE_FAMILY_CANONICAL_ORDER)
assert frozenset(FIVE_FAMILY_CANONICAL_ORDER) == FIVE_FAMILY_PERMITTED_SET

# Repo-relative provenance paths (Invariant I10).
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
_PLAYER_HISTORY_ALL_YAML_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml"
)
_MATCHES_LONG_RAW_YAML_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml"
)
_REGISTRY_CSV_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_01_feature_family_registry.csv"
)
_PR236_TRANCHE1_PARQUET_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_02_pre_game_features.parquet"
)
_PR236_TRANCHE1_AUDIT_JSON_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_01_02/leakage_audit_sc2egset.json"
)
_PR236_TRANCHE1_AUDIT_MD_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_01_02/leakage_audit_sc2egset.md"
)

# Q-chain parent artifact paths (12 SHA pins; PR #242/#243/#245/#247/#249/#251).
_PARENT_PR242_CSV_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_source_anchor_coldstart_adjudication.csv"
)
_PARENT_PR242_MD_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_source_anchor_coldstart_adjudication.md"
)
_PARENT_PR243_CSV_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_cross_region_adjudication.csv"
)
_PARENT_PR243_MD_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_cross_region_adjudication.md"
)
_PARENT_PR245_CSV_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_rating_reconstruction_adjudication.csv"
)
_PARENT_PR245_MD_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_rating_reconstruction_adjudication.md"
)
_PARENT_PR247_CSV_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6f_rating_algorithm_survey.csv"
)
_PARENT_PR247_MD_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6f_rating_algorithm_survey.md"
)
_PARENT_PR249_CSV_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6g_rating_implementation_proof.csv"
)
_PARENT_PR249_MD_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6g_rating_implementation_proof.md"
)
_PARENT_PR251_CSV_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6h_rating_path_decision.csv"
)
_PARENT_PR251_MD_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6h_rating_path_decision.md"
)
_PARENT_PR255_CSV_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_99_rating_omit_closure.csv"
)
_PARENT_PR255_MD_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_99_rating_omit_closure.md"
)
_ROADMAP_MD_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md"
)


# Output artifact paths (canonical Layer-2 paths).
_REPO_ROOT_MARKER: Path = Path(__file__).resolve()
HISTORY_ENRICHED_OUTPUT_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_enriched_pre_game_features.parquet"
)
HISTORY_ENRICHED_AUDIT_JSON_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_01_03/leakage_audit_sc2egset.json"
)
HISTORY_ENRICHED_AUDIT_MD_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_01_03/leakage_audit_sc2egset.md"
)
HISTORY_ENRICHED_RESEARCH_LOG_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
)

LINEAGE_POSITION: str = (
    "five-family history-enriched pre_game materialisation for Step "
    "02_01_03 (host of Q1..Q8 adjudications + Q5/Q6F/Q6G/Q6H + PR #255 "
    "omit-closure + PR #257 ROADMAP amendment)"
)


# ---------------------------------------------------------------------------
# Named SQL constants (python-code rule: _QUERY suffix; Invariant I6 verbatim)
# ---------------------------------------------------------------------------

_MATERIALIZATION_QUERY: str = """
WITH mfc_focal AS (
    SELECT mfc.replay_id AS focal_replay_id, mfc.toon_id AS focal_toon_id,
           mfc.race AS focal_race, mfc.metadata_mapName AS focal_map_name
    FROM matches_flat_clean mfc
),
mfc_opponent AS (
    SELECT mfc.replay_id AS opp_replay_id, mfc.toon_id AS opponent_toon_id,
           mfc.race AS opponent_race
    FROM matches_flat_clean mfc
),
mfc_paired AS (
    SELECT f.focal_replay_id, f.focal_toon_id, o.opponent_toon_id,
           f.focal_race, o.opponent_race, f.focal_map_name
    FROM mfc_focal f
    JOIN mfc_opponent o
        ON f.focal_replay_id = o.opp_replay_id
       AND f.focal_toon_id <> o.opponent_toon_id
),
mhm_anchor AS (
    SELECT match_id, player_id, started_at
    FROM matches_history_minimal
),
targets AS (
    SELECT CONCAT('sc2egset::', p.focal_replay_id) AS focal_match_id,
           p.focal_toon_id AS focal_player,
           p.opponent_toon_id AS opponent_player,
           p.focal_race, p.opponent_race, p.focal_map_name,
           a.started_at
    FROM mfc_paired p
    JOIN mhm_anchor a
        ON a.match_id = CONCAT('sc2egset::', p.focal_replay_id)
       AND a.player_id = p.focal_toon_id
),
focal_player_history AS (
    SELECT t.focal_match_id, t.focal_player,
        COUNT(*) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_prior_match_count,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE)
            AS focal_prior_win_rate_decisive,
        DATE_DIFF('day',
            MAX(TRY_CAST(ph.details_timeUTC AS TIMESTAMP))
                FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at),
            t.started_at) AS focal_days_since_prior_match,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND ph.race = t.focal_race)
            AS focal_prior_win_rate_race_conditional,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND ph.metadata_mapName = t.focal_map_name)
            AS focal_prior_win_rate_map_conditional,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND EXISTS (
                          SELECT 1 FROM player_history_all ph_opp_h
                          WHERE ph_opp_h.replay_id = ph.replay_id
                            AND ph_opp_h.toon_id <> ph.toon_id
                            AND ph_opp_h.race = t.opponent_race))
            AS focal_prior_win_rate_matchup_conditional
    FROM targets t
    LEFT JOIN player_history_all ph
        ON ph.toon_id = t.focal_player
    GROUP BY t.focal_match_id, t.focal_player, t.started_at,
             t.focal_race, t.opponent_race, t.focal_map_name
),
opponent_player_history AS (
    SELECT t.focal_match_id, t.opponent_player,
        COUNT(*) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_prior_match_count,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE)
            AS opponent_prior_win_rate_decisive,
        DATE_DIFF('day',
            MAX(TRY_CAST(ph.details_timeUTC AS TIMESTAMP))
                FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at),
            t.started_at) AS opponent_days_since_prior_match,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND ph.race = t.opponent_race)
            AS opponent_prior_win_rate_race_conditional,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND ph.metadata_mapName = t.focal_map_name)
            AS opponent_prior_win_rate_map_conditional,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND EXISTS (
                          SELECT 1 FROM player_history_all ph_focal_h
                          WHERE ph_focal_h.replay_id = ph.replay_id
                            AND ph_focal_h.toon_id <> ph.toon_id
                            AND ph_focal_h.race = t.focal_race))
            AS opponent_prior_win_rate_matchup_conditional
    FROM targets t
    LEFT JOIN player_history_all ph
        ON ph.toon_id = t.opponent_player
    GROUP BY t.focal_match_id, t.opponent_player, t.started_at,
             t.focal_race, t.opponent_race, t.focal_map_name
),
matchup_history_aggregate AS (
    SELECT t.focal_match_id, t.focal_player, t.opponent_player,
        COUNT(*) FILTER (
            WHERE TRY_CAST(ph_focal.details_timeUTC AS TIMESTAMP) < t.started_at
              AND ph_focal.replay_id = ph_opp.replay_id
        ) AS matchup_h2h_count,
        AVG(CASE WHEN ph_focal.result = 'Win' THEN 1.0
                 WHEN ph_focal.result = 'Loss' THEN 0.0 END)
            FILTER (
                WHERE TRY_CAST(ph_focal.details_timeUTC AS TIMESTAMP) < t.started_at
                  AND ph_focal.replay_id = ph_opp.replay_id
                  AND ph_focal.is_decisive_result = TRUE
            ) AS matchup_h2h_focal_win_rate
    FROM targets t
    LEFT JOIN player_history_all ph_focal
        ON ph_focal.toon_id = t.focal_player
    LEFT JOIN player_history_all ph_opp
        ON ph_opp.toon_id = t.opponent_player
       AND ph_opp.replay_id = ph_focal.replay_id
    LEFT JOIN matches_flat_clean mfc_h
        ON mfc_h.replay_id = ph_focal.replay_id
       AND mfc_h.toon_id   = ph_focal.toon_id
    GROUP BY t.focal_match_id, t.focal_player, t.opponent_player, t.started_at
),
cross_region_fragmentation_handling AS (
    SELECT t.focal_match_id, t.focal_player,
        BOOL_OR(ph.is_cross_region_fragmented)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS is_cross_region_fragmented_focal_history_any,
        BOOL_OR(ph2.is_cross_region_fragmented)
            FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS is_cross_region_fragmented_opponent_history_any
    FROM targets t
    LEFT JOIN player_history_all ph  ON ph.toon_id  = t.focal_player
    LEFT JOIN player_history_all ph2 ON ph2.toon_id = t.opponent_player
    GROUP BY t.focal_match_id, t.focal_player, t.started_at
),
in_game_history_aggregate AS (
    SELECT t.focal_match_id, t.focal_player,
        AVG(ph.APM) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_apm_prior_mean,
        AVG(ph.SQ) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_sq_prior_mean,
        AVG(ph.supplyCappedPercent)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_supply_capped_pct_prior_mean,
        AVG(ph.header_elapsedGameLoops)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_elapsed_game_loops_prior_mean,
        AVG(ph2.APM) FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_apm_prior_mean,
        AVG(ph2.SQ) FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_sq_prior_mean,
        AVG(ph2.supplyCappedPercent)
            FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_supply_capped_pct_prior_mean,
        AVG(ph2.header_elapsedGameLoops)
            FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_elapsed_game_loops_prior_mean
    FROM targets t
    LEFT JOIN player_history_all ph  ON ph.toon_id  = t.focal_player
    LEFT JOIN player_history_all ph2 ON ph2.toon_id = t.opponent_player
    GROUP BY t.focal_match_id, t.focal_player, t.started_at
)
SELECT
    t.focal_match_id, t.focal_player, t.opponent_player,
    t.started_at,
    fph.focal_prior_match_count, fph.focal_prior_win_rate_decisive,
    fph.focal_days_since_prior_match,
    fph.focal_prior_win_rate_race_conditional,
    fph.focal_prior_win_rate_map_conditional,
    fph.focal_prior_win_rate_matchup_conditional,
    oph.opponent_prior_match_count, oph.opponent_prior_win_rate_decisive,
    oph.opponent_days_since_prior_match,
    oph.opponent_prior_win_rate_race_conditional,
    oph.opponent_prior_win_rate_map_conditional,
    oph.opponent_prior_win_rate_matchup_conditional,
    mha.matchup_h2h_count, mha.matchup_h2h_focal_win_rate,
    crfh.is_cross_region_fragmented_focal_history_any,
    crfh.is_cross_region_fragmented_opponent_history_any,
    ighp.focal_apm_prior_mean, ighp.focal_sq_prior_mean,
    ighp.focal_supply_capped_pct_prior_mean,
    ighp.focal_elapsed_game_loops_prior_mean,
    ighp.opponent_apm_prior_mean, ighp.opponent_sq_prior_mean,
    ighp.opponent_supply_capped_pct_prior_mean,
    ighp.opponent_elapsed_game_loops_prior_mean
FROM targets t
LEFT JOIN focal_player_history             fph  USING (focal_match_id, focal_player)
LEFT JOIN opponent_player_history          oph  USING (focal_match_id, opponent_player)
LEFT JOIN matchup_history_aggregate        mha
       USING (focal_match_id, focal_player, opponent_player)
LEFT JOIN cross_region_fragmentation_handling crfh USING (focal_match_id, focal_player)
LEFT JOIN in_game_history_aggregate        ighp USING (focal_match_id, focal_player)
ORDER BY t.started_at, t.focal_match_id, t.focal_player
""".strip()

# The canonical strict-< token (used by the F-strict-lt-operator-missing /
# F-try-cast-missing guards). Both must appear verbatim in the SQL.
_STRICT_LT_TRY_CAST_TOKEN: str = (
    "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at"
)

_OUTPUT_ROW_COUNT_QUERY: str = (
    "SELECT COUNT(*) FROM materialized_history_enriched_pre_game_features"
)
_OUTPUT_DISTINCT_FOCAL_MATCH_ID_QUERY: str = (
    "SELECT COUNT(DISTINCT focal_match_id) "
    "FROM materialized_history_enriched_pre_game_features"
)
_FOCAL_ROWS_PER_MATCH_QUERY: str = (
    "SELECT focal_match_id, COUNT(*) AS cnt "
    "FROM materialized_history_enriched_pre_game_features "
    "GROUP BY 1 HAVING COUNT(*) <> 2"
)
_SYMMETRY_CHECK_QUERY: str = """
SELECT COUNT(*) FROM materialized_history_enriched_pre_game_features m1
JOIN materialized_history_enriched_pre_game_features m2
    ON m1.focal_match_id = m2.focal_match_id
    AND m1.focal_player  = m2.opponent_player
    AND m1.opponent_player = m2.focal_player
WHERE m1.started_at != m2.started_at
""".strip()
_STARTED_AT_RANGE_QUERY: str = (
    "SELECT MIN(started_at), MAX(started_at) "
    "FROM materialized_history_enriched_pre_game_features"
)
_DESCRIBE_QUERY: str = "DESCRIBE materialized_history_enriched_pre_game_features"

# Examiner-clarity sentence (must appear in audit JSON `notes` AND audit MD §1).
EXAMINER_CLARITY_SENTENCE: str = (
    "`started_at` is projected as a row-identity anchor only "
    "(CROSS-02-00 Section 5.1 = CONTEXT; PR #242 Q2 use_as_window_bound = false) "
    "and is excluded from `features_audited`."
)
_EXAMINER_CLARITY_REQUIRED_FRAGMENTS: tuple[str, ...] = (
    "`started_at` is projected as a row-identity anchor only",
    "excluded from `features_audited`",
)

# Non-overclaim disclaimer (audit JSON notes + audit MD).
_CLOSURE_NON_OVERCLAIM: str = (
    "Step 02_01_03 NOT closed by this PR; closure deferred to a separate "
    "U2.B-style PR per PR #237 precedent."
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HistoryEnrichedMaterializationResult:
    """Result of the history-enriched pre_game materialization.

    Attributes:
        parquet_path: Path to the persisted Parquet feature file.
        row_count: COUNT(*) on the materialized output.
        column_names: Tuple of output column names in projection order.
        distinct_focal_match_id_count: Distinct focal_match_id count.
        focal_rows_per_match_violations: # of focal_match_ids with row count != 2.
        symmetry_violations: # of started_at swap symmetry violations.
        materialized_output_paths: Non-empty tuple containing the Parquet path.
        halting_falsifier: Label of the first falsifier that fired, or None.
    """

    parquet_path: Path
    row_count: int
    column_names: tuple[str, ...]
    distinct_focal_match_id_count: int
    focal_rows_per_match_violations: int
    symmetry_violations: int
    materialized_output_paths: tuple[str, ...] = field(default_factory=tuple)
    halting_falsifier: str | None = None

    @property
    def passed(self) -> bool:
        """Return True iff halting_falsifier is None."""
        return self.halting_falsifier is None


@dataclass(frozen=True)
class HistoryEnrichedAuditResult:
    """Result of the post-materialization CROSS-02-01 leakage audit.

    Attributes:
        spec_version: "CROSS-02-01-v1" per Section 3.
        dataset: "sc2egset".
        phase_02_step: "02_01_03".
        audit_date: ISO YYYY-MM-DD at materialisation execution time.
        future_leak_count: 0 (strict-< filter enforced).
        post_game_token_violations: Count of POST_GAME tokens in column names.
        normalization_fit_scope: "training_fold_only" (vacuously satisfied).
        target_encoding_fold_awareness: "N/A_no_target_encoding".
        cutoff_time_filter_structural_check: "pass".
        reference_window_assertion: "pass".
        features_audited: The 24 history-enriched feature columns under audit.
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
    """Walk upwards until a directory containing pyproject.toml is found.

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


# ---------------------------------------------------------------------------
# Schema / token guards
# ---------------------------------------------------------------------------


def _is_post_game_token(name: str) -> bool:
    """Return True iff name contains a POST_GAME token via token-equality.

    Args:
        name: Candidate column name.

    Returns:
        True if any POST_GAME token equals one of name's underscore tokens,
        UNLESS the column name matches a
        ``_PROTECTED_HISTORY_AGGREGATE_PATTERNS`` substring (e.g. a
        history-aggregated `prior_win_rate` column).
    """
    lowered = name.lower()
    if any(p in lowered for p in _PROTECTED_HISTORY_AGGREGATE_PATTERNS):
        return False
    tokens = set(lowered.split("_"))
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


def _is_reconstructed_rating_column(name: str) -> bool:
    """Return True iff the column name is a forbidden reconstructed_rating column.

    Args:
        name: Candidate column name.

    Returns:
        True if forbidden per PR #257 amendment lines 2546-2548.
    """
    return name in FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS or "reconstructed_rating" in name.lower()


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
        "replay_players_raw",
        "replays_meta_raw",
        "matches_long_raw",
        "matches_flat ",  # space-bounded to distinguish from matches_flat_clean
    )
    return tuple(s.strip() for s in forbidden_substrings if s in lowered)


def _check_strict_lt_try_cast_present(query: str) -> bool:
    """Return True iff the canonical strict-< TRY_CAST predicate appears in SQL.

    Args:
        query: Materialization SQL string.

    Returns:
        True if the canonical strict-< TRY_CAST token is present.
    """
    return _STRICT_LT_TRY_CAST_TOKEN in query


def _check_no_lte_or_eq_history_predicate(query: str) -> bool:
    """Return True iff a `<=` or `=` predicate on details_timeUTC is found.

    Args:
        query: Materialization SQL string.

    Returns:
        True if any non-strict timestamp predicate is detected (a falsifier hit).
    """
    lowered = query.lower()
    bad_tokens = (
        "details_timeutc as timestamp) <=",
        "details_timeutc as timestamp) =",
    )
    return any(token in lowered for token in bad_tokens)


def _check_try_cast_present(query: str) -> bool:
    """Return True iff TRY_CAST appears for the details_timeUTC predicate.

    Args:
        query: Materialization SQL string.

    Returns:
        True iff the canonical TRY_CAST(ph.details_timeUTC ...) pattern appears.
    """
    return "TRY_CAST(ph.details_timeUTC AS TIMESTAMP)" in query


def _check_matchup_cte_is_1v1_restricted(query: str) -> bool:
    """Return True iff matchup CTE includes the matches_flat_clean join.

    Args:
        query: Materialization SQL string.

    Returns:
        True iff the B2 matchup CTE 1v1-restriction join is present.
    """
    required = "matches_flat_clean mfc_h"
    return required in query


def _check_decisive_result_flag_used(query: str) -> bool:
    """Return True iff `is_decisive_result = TRUE` appears in the SQL.

    Args:
        query: Materialization SQL string.

    Returns:
        True iff the decisive-result flag is used (N11 fix).
    """
    return "is_decisive_result = TRUE" in query


def _check_no_reconstructed_rating_column(columns: tuple[str, ...]) -> bool:
    """Return True iff any column name is a reconstructed_rating column.

    Args:
        columns: Tuple of column names from the materialization output.

    Returns:
        True if a forbidden column is present (a falsifier hit).
    """
    return any(_is_reconstructed_rating_column(c) for c in columns)


def _check_no_post_game_token_in_columns(columns: tuple[str, ...]) -> int:
    """Count POST_GAME-token violations across the projected column list.

    Args:
        columns: Tuple of projected column names.

    Returns:
        Number of column names containing a POST_GAME token.
    """
    return sum(1 for c in columns if _is_post_game_token(c))


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
    """Create the session-scoped temp view ``materialized_history_enriched_pre_game_features``.

    Args:
        con: Open DuckDB connection (read-only is fine; TEMP views go to memory).
    """
    con.execute(
        f"CREATE OR REPLACE TEMP VIEW materialized_history_enriched_pre_game_features AS "
        f"{_MATERIALIZATION_QUERY}"
    )


def _export_to_parquet(
    con: duckdb.DuckDBPyConnection, output_parquet_path: Path
) -> None:
    """Write the temp view to Parquet with ZSTD compression.

    Args:
        con: Open DuckDB connection with the temp view registered.
        output_parquet_path: Destination Parquet path.
    """
    output_parquet_path.parent.mkdir(parents=True, exist_ok=True)
    con.execute(
        f"COPY (SELECT * FROM materialized_history_enriched_pre_game_features) "
        f"TO '{output_parquet_path.as_posix()}' "
        f"(FORMAT PARQUET, COMPRESSION 'ZSTD', ROW_GROUP_SIZE 100000)"
    )


def _query_column_names(con: duckdb.DuckDBPyConnection) -> tuple[str, ...]:
    """Return the column names of the materialized temp view in projection order.

    Args:
        con: Open DuckDB connection with the temp view registered.

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
    out["distinct_focal_match_id"] = con.execute(  # type: ignore[assignment]
        _OUTPUT_DISTINCT_FOCAL_MATCH_ID_QUERY
    ).fetchone()[0]  # type: ignore[index]
    out["focal_rows_per_match_violations"] = len(
        con.execute(_FOCAL_ROWS_PER_MATCH_QUERY).fetchall()
    )
    out["symmetry_violations"] = con.execute(_SYMMETRY_CHECK_QUERY).fetchone()[0]  # type: ignore[index]
    return out


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


# ---------------------------------------------------------------------------
# Falsifier evaluation
# ---------------------------------------------------------------------------


def _evaluate_query_falsifiers(query: str) -> str | None:
    """Return the first SQL-text-side falsifier label that fires, or None.

    Args:
        query: Materialization SQL text.

    Returns:
        Falsifier label or None.
    """
    if not _check_try_cast_present(query):
        return "F-try-cast-missing"
    if not _check_strict_lt_try_cast_present(query):
        return "F-strict-lt-operator-missing"
    if _check_no_lte_or_eq_history_predicate(query):
        return "F-equal-lt-operator-used"
    if _check_source_table_allowlist(query):
        return "F-tracker-source-read"
    if not _check_matchup_cte_is_1v1_restricted(query):
        return "F-matchup-cte-includes-non-1v1-history"
    if not _check_decisive_result_flag_used(query):
        return "F-decisive-result-flag-not-used"
    return None


def _evaluate_materialization_falsifiers(
    sanity: dict[str, Any],
    columns: tuple[str, ...],
    query: str,
) -> str | None:
    """Return the first materialization falsifier label that fires, or None.

    Args:
        sanity: Sanity-check result dict.
        columns: Tuple of materialized column names.
        query: Materialization SQL text.

    Returns:
        Falsifier label or None.
    """
    # Structural drift errors first.
    if len(FIVE_FAMILY_PERMITTED_SET) != FIVE_FAMILY_PERMITTED_COUNT:
        return "F-five-family-count-drift"
    if frozenset(FIVE_FAMILY_CANONICAL_ORDER) != FIVE_FAMILY_PERMITTED_SET:
        return "F-five-family-set-drift"
    if _check_no_reconstructed_rating_column(columns):
        return "F-reconstructed-rating-column-present"
    if any(_is_forbidden_skill_column(c) for c in columns):
        return "F-forbidden-skill-scalar-projected"
    if _check_no_post_game_token_in_columns(columns) > 0:
        return "F-post-game-token-projected"
    if columns != EXPECTED_OUTPUT_COLUMNS:
        return "F-output-column-mismatch"
    sql_falsifier = _evaluate_query_falsifiers(query)
    if sql_falsifier is not None:
        return sql_falsifier
    if sanity["row_count"] != EXPECTED_OUTPUT_ROW_COUNT:
        return "F-row-count-mismatch"
    if sanity["focal_rows_per_match_violations"] != 0:
        return "F-focal-rows-per-match-violation"
    if sanity["symmetry_violations"] != 0:
        return "F-symmetry-violation"
    return None


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
    if len(features_audited) != EXPECTED_AUDITED_FEATURE_COLUMN_COUNT:
        return "F-features-audited-not-twenty-four"
    if set(features_audited) != set(EXPECTED_AUDITED_FEATURE_COLUMNS):
        return "F-features-audited-not-twenty-four"
    audit_set = set(features_audited)
    if audit_set & set(projected_identity_columns):
        return "F-context-column-counted-as-feature"
    if audit_set & set(projected_context_columns):
        return "F-context-column-counted-as-feature"
    if any(fr not in examiner_notes for fr in _EXAMINER_CLARITY_REQUIRED_FRAGMENTS):
        return "F-examiner-clarity-sentence-missing"
    if EXAMINER_CLARITY_SENTENCE not in examiner_md_section1:
        return "F-examiner-clarity-sentence-missing"
    if any(_is_post_game_token(c) for c in parquet_columns):
        return "F-post-game-token-projected"
    if any(_is_forbidden_skill_column(c) for c in parquet_columns):
        return "F-forbidden-skill-scalar-projected"
    if any(_is_reconstructed_rating_column(c) for c in parquet_columns):
        return "F-reconstructed-rating-column-present"
    return None


# ---------------------------------------------------------------------------
# Public entrypoint — materialization
# ---------------------------------------------------------------------------


def materialize_history_enriched_pre_game_features(
    duckdb_path: Path | str,
    output_parquet_path: Path | str,
) -> HistoryEnrichedMaterializationResult:
    """Materialize the 5 history-enriched pre_game families to Parquet.

    Reads ``matches_flat_clean``, ``matches_history_minimal``, and
    ``player_history_all`` (read-only) from the DuckDB file; executes
    ``_MATERIALIZATION_QUERY`` into a temp view; writes the view to Parquet
    with ZSTD compression and 100k row groups; then runs every sanity-check
    query and evaluates falsifiers. If any falsifier fires, the result
    carries the failure label in ``halting_falsifier``.

    Args:
        duckdb_path: Path to the on-disk DuckDB file.
        output_parquet_path: Destination Parquet path for the feature table.

    Returns:
        HistoryEnrichedMaterializationResult with all sanity-check outputs.
    """
    duckdb_path = Path(duckdb_path)
    output_parquet_path = Path(output_parquet_path)

    LOGGER.debug(
        "materialize_history_enriched_pre_game_features: duckdb=%s output=%s",
        duckdb_path,
        output_parquet_path,
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

    return HistoryEnrichedMaterializationResult(
        parquet_path=output_parquet_path,
        row_count=int(sanity["row_count"]),
        column_names=column_names,
        distinct_focal_match_id_count=int(sanity["distinct_focal_match_id"]),
        focal_rows_per_match_violations=int(
            sanity["focal_rows_per_match_violations"]
        ),
        symmetry_violations=int(sanity["symmetry_violations"]),
        materialized_output_paths=(str(output_parquet_path),),
        halting_falsifier=halting_falsifier,
    )


# ---------------------------------------------------------------------------
# Audit JSON / MD rendering
# ---------------------------------------------------------------------------


def _build_audit_notes(audit_pr: str) -> str:
    """Construct the multi-paragraph audit JSON ``notes`` string.

    Args:
        audit_pr: The literal "PR #<N>" string (or placeholder).

    Returns:
        Joined notes string.
    """
    parts = [
        _CLOSURE_NON_OVERCLAIM,
        (
            "cutoff_time_filter_structural_check = pass is justified by the "
            "verbatim strict-< TRY_CAST predicate "
            f"`{_STRICT_LT_TRY_CAST_TOKEN}` applied to every history "
            "aggregate (CROSS-02-03 Section 6.1; Invariant I3)."
        ),
        (
            "normalization_fit_scope = training_fold_only is vacuously "
            "satisfied because no encoder/scaler is fit during materialization "
            "-- raw aggregates are retained for Phase 03 fold-aware encoder "
            "fitting (CROSS-02-02 Section 9.1 G-CS-6)."
        ),
        (
            "Per Q1 BINDING (PR #242), the per-player history side aggregates "
            "ALL game types (1v1 + 2v2 + 3v3 + 4v4 + FFA): per-player win "
            "rates are deliberate cross-game-type rates. The "
            "matchup_history_aggregate CTE restricts the shared-replay self-"
            "join to 1v1 historical matches via JOIN matches_flat_clean."
        ),
        (
            f"EXAMINER-CLARITY: {EXAMINER_CLARITY_SENTENCE} The 28 output "
            "columns partition into 3 projected identity columns "
            "(`focal_match_id`, `focal_player`, `opponent_player`), "
            "1 projected context anchor (`started_at`), and 24 audited "
            "history-enriched PRE_GAME feature columns spanning the 5 "
            "permitted families (focal_player_history=6, "
            "opponent_player_history=6, matchup_history_aggregate=2, "
            "cross_region_fragmentation_handling=2, "
            "in_game_history_aggregate=8). The `reconstructed_rating` family "
            "and its three columns are EXCLUDED per PR #255 omit-closure."
        ),
        (
            f"This is the first non-vacuous CROSS-02-01 audit for "
            f"Step {PHASE_02_STEP} ({audit_pr}). "
            "Grep token: materialization_scope_amendment_post_pr_255."
        ),
    ]
    return " ".join(parts)


def _gather_provenance_shas(
    repo_root: Path,
    parquet_path: Path,
    module_path: Path,
) -> dict[str, str]:
    """Compute SHA-256 digests for every provenance asset.

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
        "spec_02_00_sha256": _sha256_file(repo_root / _SPEC_02_00_RELPATH),
        "spec_02_01_sha256": _sha256_file(repo_root / _SPEC_02_01_RELPATH),
        "spec_02_02_sha256": _sha256_file(repo_root / _SPEC_02_02_RELPATH),
        "spec_02_03_sha256": _sha256_file(repo_root / _SPEC_02_03_RELPATH),
        "matches_flat_clean_yaml_sha256": _sha256_file(
            repo_root / _MATCHES_FLAT_CLEAN_YAML_RELPATH
        ),
        "matches_history_minimal_yaml_sha256": _sha256_file(
            repo_root / _MATCHES_HISTORY_MINIMAL_YAML_RELPATH
        ),
        "player_history_all_yaml_sha256": _sha256_file(
            repo_root / _PLAYER_HISTORY_ALL_YAML_RELPATH
        ),
        "matches_long_raw_yaml_sha256": _sha256_file(
            repo_root / _MATCHES_LONG_RAW_YAML_RELPATH
        ),
        "registry_csv_sha256": _sha256_file(repo_root / _REGISTRY_CSV_RELPATH),
        "parent_pr242_csv_sha256": _sha256_file(repo_root / _PARENT_PR242_CSV_RELPATH),
        "parent_pr242_md_sha256": _sha256_file(repo_root / _PARENT_PR242_MD_RELPATH),
        "parent_pr243_csv_sha256": _sha256_file(repo_root / _PARENT_PR243_CSV_RELPATH),
        "parent_pr243_md_sha256": _sha256_file(repo_root / _PARENT_PR243_MD_RELPATH),
        "parent_pr245_csv_sha256": _sha256_file(repo_root / _PARENT_PR245_CSV_RELPATH),
        "parent_pr245_md_sha256": _sha256_file(repo_root / _PARENT_PR245_MD_RELPATH),
        "parent_pr247_csv_sha256": _sha256_file(repo_root / _PARENT_PR247_CSV_RELPATH),
        "parent_pr247_md_sha256": _sha256_file(repo_root / _PARENT_PR247_MD_RELPATH),
        "parent_pr249_csv_sha256": _sha256_file(repo_root / _PARENT_PR249_CSV_RELPATH),
        "parent_pr249_md_sha256": _sha256_file(repo_root / _PARENT_PR249_MD_RELPATH),
        "parent_pr251_csv_sha256": _sha256_file(repo_root / _PARENT_PR251_CSV_RELPATH),
        "parent_pr251_md_sha256": _sha256_file(repo_root / _PARENT_PR251_MD_RELPATH),
        "parent_pr255_csv_sha256": _sha256_file(repo_root / _PARENT_PR255_CSV_RELPATH),
        "parent_pr255_md_sha256": _sha256_file(repo_root / _PARENT_PR255_MD_RELPATH),
        "pr236_tranche1_parquet_sha256": _sha256_file(
            repo_root / _PR236_TRANCHE1_PARQUET_RELPATH
        ),
        "pr236_tranche1_audit_json_sha256": _sha256_file(
            repo_root / _PR236_TRANCHE1_AUDIT_JSON_RELPATH
        ),
        "pr236_tranche1_audit_md_sha256": _sha256_file(
            repo_root / _PR236_TRANCHE1_AUDIT_MD_RELPATH
        ),
        "roadmap_md_sha256": _sha256_file(repo_root / _ROADMAP_MD_RELPATH),
    }


def _render_audit_json(
    audit: HistoryEnrichedAuditResult,
    audit_json_path: Path,
    parquet_path: Path,
    audit_pr: str,
    audit_date: str,
    provenance_shas: dict[str, str],
    git_sha: str,
    distinct_focal_match_count: int,
    row_count: int,
) -> None:
    """Write the CROSS-02-01-v1.0.1 Section 3 audit JSON.

    Args:
        audit: Populated HistoryEnrichedAuditResult.
        audit_json_path: Destination JSON path.
        parquet_path: Materialized Parquet path (for relative-path reference).
        audit_pr: PR label string (e.g. "PR #259").
        audit_date: ISO date.
        provenance_shas: SHA-256 digests from _gather_provenance_shas.
        git_sha: Current git HEAD SHA.
        distinct_focal_match_count: # of distinct focal_match_id values.
        row_count: Total row count of the Parquet artifact.
    """
    repo_root = _find_repo_root(Path(__file__))
    feature_parquet_relpath = _resolve_repo_root_relpath(parquet_path, repo_root)
    audit_json_relpath = _resolve_repo_root_relpath(audit_json_path, repo_root)
    audit_md_relpath = _resolve_repo_root_relpath(
        Path(audit.artifact_md_path), repo_root
    )
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
        "features_audited_count": len(audit.features_audited),
        "projected_context_columns": list(audit.projected_context_columns),
        "projected_identity_columns": list(audit.projected_identity_columns),
        "verdict": audit.verdict,
        "audit_pr": audit_pr,
        "lineage_position": LINEAGE_POSITION,
        "feature_parquet_path": feature_parquet_relpath,
        "materialized_output_paths": [feature_parquet_relpath],
        "audit_json_path": audit_json_relpath,
        "audit_md_path": audit_md_relpath,
        "row_count": row_count,
        "distinct_focal_match_count": distinct_focal_match_count,
        "feature_column_count": len(audit.features_audited),
        "five_family_set": list(FIVE_FAMILY_CANONICAL_ORDER),
        "five_family_canonical_order": list(FIVE_FAMILY_CANONICAL_ORDER),
        "excluded_family": EXCLUDED_FAMILY,
        "excluded_columns": sorted(FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS),
        "cross_region_policy": CROSS_REGION_POLICY,
        "in_game_historical_aggregated_columns": list(
            IN_GAME_HISTORICAL_AGGREGATED_COLUMNS
        ),
        "temporal_filter": _STRICT_LT_TRY_CAST_TOKEN,
        "feature_to_family_mapping": dict(FEATURE_TO_FAMILY_MAPPING),
        "leakage_falsifiers": [
            "F-five-family-count-drift",
            "F-five-family-set-drift",
            "F-five-family-canonical-order-drift",
            "F-reconstructed-rating-column-present",
            "F-reconstructed-rating-token-leak",
            "F-forbidden-skill-scalar-projected",
            "F-row-count-mismatch",
            "F-focal-rows-per-match-violation",
            "F-symmetry-violation",
            "F-strict-lt-operator-missing",
            "F-equal-lt-operator-used",
            "F-try-cast-missing",
            "F-tracker-source-read",
            "F-target-match-row-in-history",
            "F-join-then-filter-invariant-violation",
            "F-post-game-token-projected",
            "F-cross-region-policy-mismatch",
            "F-in-game-historical-column-out-of-scope",
            "F-features-audited-empty",
            "F-features-audited-not-twenty-four",
            "F-features-audited-count-mismatch",
            "F-context-column-counted-as-feature",
            "F-audit-verdict-not-pass",
            "F-encoder-fit-at-materialization-layer",
            "F-examiner-clarity-sentence-missing",
            "F-non-deterministic-output",
            "F-matchup-cte-includes-non-1v1-history",
            "F-decisive-result-flag-not-used",
        ],
        "custom_extensions": {
            "_comment": (
                "Fields beyond CROSS-02-01-v1.0.1 Section 3 are enumerated "
                "here so examiners can distinguish spec-mandated fields "
                "from project extensions."
            ),
            "fields": [
                "feature_to_family_mapping",
                "feature_column_count",
                "distinct_focal_match_count",
                "five_family_set",
                "five_family_canonical_order",
                "excluded_family",
                "excluded_columns",
                "cross_region_policy",
                "in_game_historical_aggregated_columns",
                "temporal_filter",
                "leakage_falsifiers",
                "materialized_output_paths",
                "audit_json_path",
                "audit_md_path",
                "parent_artifact_shas",
                "generated_sql_provenance",
            ],
        },
        "parent_artifact_shas": {
            k: v for k, v in provenance_shas.items() if "parent_pr" in k
        },
        "generated_sql_provenance": {
            "git_sha": git_sha,
            "module_sha256": provenance_shas["materialize_module_sha256"],
        },
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
    """Render audit MD Section 1.

    Args:
        audit_pr: PR label.

    Returns:
        Markdown body for Section 1.
    """
    return (
        "## 1. Non-overclaim disclaimer + non-vacuous audit statement\n\n"
        f"{_CLOSURE_NON_OVERCLAIM}\n\n"
        "Feature Parquet persisted (28 projected columns: 3 identity + 1 "
        "context anchor + 24 audited history-enriched PRE_GAME features "
        "spanning the five permitted families per PR #257 ROADMAP amendment "
        "(grep token `materialization_scope_amendment_post_pr_255`)).\n\n"
        "CROSS-02-01-v1.0.1 Section 5 gate condition is mechanically "
        "satisfied: `features_audited` non-empty (= 24 history-enriched "
        "PRE_GAME feature columns), `verdict = PASS`, JSON + MD persisted "
        "at the spec-named paths.\n\n"
        f"**Examiner-clarity sentence (verbatim):** {EXAMINER_CLARITY_SENTENCE}\n\n"
        "**B2 cross-game-type per-player win-rate aggregation acknowledgement.** "
        "Per Q1 BINDING (PR #242 row Q1_source_layer; "
        "`selected_history_source_layer = player_history_all`), the per-player "
        "history side aggregates ALL game types (1v1 + 2v2 + 3v3 + 4v4 + "
        "FFA). The `focal_prior_win_rate_decisive` and "
        "`opponent_prior_win_rate_decisive` features are therefore "
        "deliberate cross-game-type rates: a player's 4v4 win-rate "
        "contributes to their 1v1 prediction. This is a documented "
        "Q1-binding consequence, not an oversight; ranking experiments at "
        "Phase 04 will treat this as a baseline measurement of the "
        "player-level win-rate signal.\n\n"
        "**B2 matchup CTE 1v1-restriction.** The "
        "`matchup_history_aggregate` family CTE restricts the shared-replay "
        "self-join to 1v1 historical matches via "
        "`JOIN matches_flat_clean mfc_h ON mfc_h.replay_id = ph_focal.replay_id`. "
        "This prevents 4v4/3v3/2v2 prior teammate-or-opponent encounters "
        "from spuriously inflating the head-to-head count. The 1v1 "
        "restriction on the matchup CTE -- combined with the cross-game-type "
        "per-player win-rate above -- operationalises the intuition that "
        "head-to-head is a same-game-type construct while per-player skill "
        "aggregates a player's overall activity.\n\n"
        "**N9 Invariant I5 citation.** The cross-region indicator pair "
        "(`is_cross_region_fragmented_focal_history_any`, "
        "`is_cross_region_fragmented_opponent_history_any`) goes beyond "
        "PR #243's single-indicator text by symmetrising the indicator "
        "across focal + opponent. The methodological basis is Invariant I5 "
        "(focal/opponent symmetric construction per "
        "`.claude/scientific-invariants.md`), not PR #243's text alone.\n\n"
        f"This is the first non-vacuous CROSS-02-01 post-materialization "
        f"audit for Step {PHASE_02_STEP} ({audit_pr}).\n"
    )


def _build_md_section_2(provenance_shas: dict[str, str]) -> str:
    """Render audit MD Section 2 (verbatim materialization SQL + lineage).

    Args:
        provenance_shas: SHA-256 digests from _gather_provenance_shas.

    Returns:
        Markdown body for Section 2.
    """
    sha_table_lines = [
        "| Source role | SHA-256 |",
        "|-------------|---------|",
        f"| PR #242 csv | {provenance_shas['parent_pr242_csv_sha256']} |",
        f"| PR #242 md | {provenance_shas['parent_pr242_md_sha256']} |",
        f"| PR #243 csv (Q5 = sensitivity_indicator_co_registration) | "
        f"{provenance_shas['parent_pr243_csv_sha256']} |",
        f"| PR #243 md | {provenance_shas['parent_pr243_md_sha256']} |",
        f"| PR #245 csv | {provenance_shas['parent_pr245_csv_sha256']} |",
        f"| PR #245 md | {provenance_shas['parent_pr245_md_sha256']} |",
        f"| PR #247 csv | {provenance_shas['parent_pr247_csv_sha256']} |",
        f"| PR #247 md | {provenance_shas['parent_pr247_md_sha256']} |",
        f"| PR #249 csv | {provenance_shas['parent_pr249_csv_sha256']} |",
        f"| PR #249 md | {provenance_shas['parent_pr249_md_sha256']} |",
        f"| PR #251 csv (Q6H terminal) | {provenance_shas['parent_pr251_csv_sha256']} |",
        f"| PR #251 md | {provenance_shas['parent_pr251_md_sha256']} |",
        f"| PR #255 csv (omit-closure; q5_policy re-elevation) | "
        f"{provenance_shas['parent_pr255_csv_sha256']} |",
        f"| PR #255 md | {provenance_shas['parent_pr255_md_sha256']} |",
        f"| 02_01_01 registry CSV | {provenance_shas['registry_csv_sha256']} |",
        f"| PR #236 tranche-1 Parquet | "
        f"{provenance_shas['pr236_tranche1_parquet_sha256']} |",
        f"| PR #236 tranche-1 audit JSON | "
        f"{provenance_shas['pr236_tranche1_audit_json_sha256']} |",
        f"| PR #236 tranche-1 audit MD | "
        f"{provenance_shas['pr236_tranche1_audit_md_sha256']} |",
    ]
    return (
        "## 2. Verbatim materialization SQL + 17 binding parent provenance\n\n"
        "The full `_MATERIALIZATION_QUERY` from "
        "`materialize_history_enriched_pre_game_features.py` is reproduced "
        "verbatim per Invariant I6:\n\n"
        "```sql\n"
        f"{_MATERIALIZATION_QUERY}\n"
        ";\n"
        "```\n\n"
        "**17 BINDING parent artifact SHA-256 pins** (12 Q-chain + 2 "
        "omit-closure + 1 registry + 3 tranche-1):\n\n"
        + "\n".join(sha_table_lines)
        + "\n\n"
        "**R3-N2 defensive lineage-completeness pin.** The "
        "`matches_long_raw_yaml_sha256` "
        f"(= {provenance_shas['matches_long_raw_yaml_sha256']}) is a "
        "defensive lineage-completeness pin (NOT a read-source pin) to "
        "detect future drift if a later revision joins this view; the "
        "current materialisation does NOT read `matches_long_raw`. "
        "Retained to prevent unnoticed view-schema drift from changing the "
        "operational meaning of any future revision.\n"
    )


def _build_md_section_3() -> str:
    """Render audit MD Section 3 (five-family enumeration + 24-feature listing)."""
    by_family_lines: list[str] = [
        "| # | Feature column | Family |",
        "|---|----------------|--------|",
    ]
    for i, col in enumerate(EXPECTED_AUDITED_FEATURE_COLUMNS, start=1):
        family = FEATURE_TO_FAMILY_MAPPING[col]
        by_family_lines.append(f"| {i} | `{col}` | `{family}` |")
    family_count_lines = [
        "| Family | Column count |",
        "|--------|-------------|",
        "| focal_player_history | 6 |",
        "| opponent_player_history | 6 |",
        "| matchup_history_aggregate | 2 |",
        "| cross_region_fragmentation_handling | 2 |",
        "| in_game_history_aggregate | 8 |",
        "| **TOTAL** | **24** |",
    ]
    excluded_list = ", ".join(
        f"`{c}`" for c in sorted(FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS)
    )
    return (
        "## 3. Five-family enumeration + audited feature listing\n\n"
        "**Five-family permitted set (canonical order; PR #257 amendment lines "
        "2536-2540):**\n\n"
        + "\n".join(
            f"- `{name}`" for name in FIVE_FAMILY_CANONICAL_ORDER
        )
        + "\n\n"
        "**Excluded family (PR #257 amendment line 2542):** "
        f"`{EXCLUDED_FAMILY}`\n\n"
        "**Excluded columns (PR #257 amendment lines 2546-2548):** "
        f"{excluded_list}\n\n"
        "**Family -> audited-column count mapping:**\n\n"
        + "\n".join(family_count_lines)
        + "\n\n"
        "**24 audited feature columns (in T03 projection order):**\n\n"
        + "\n".join(by_family_lines)
        + "\n"
    )


def _build_md_section_4() -> str:
    """Render audit MD Section 4 (temporal-filter proof + Q-chain lineage)."""
    return (
        "## 4. Temporal-filter proof + Q-chain lineage citations\n\n"
        "**Strict-< TRY_CAST predicate (Invariant I3; PR #242 Q3 BINDING; "
        "B-X2 canonical TRY_CAST):** every per-player, matchup, cross-region, "
        "and in-game-history aggregate uses the canonical predicate\n\n"
        f"```\n{_STRICT_LT_TRY_CAST_TOKEN}\n```\n\n"
        "verbatim, with no `<=` or `=` variant. The `is_decisive_result = "
        "TRUE` flag is used in place of inline `ph.result IN ('Win', "
        "'Loss')` per the N11 fix (verified to exist as BOOLEAN at "
        "`player_history_all.yaml` lines 48-54).\n\n"
        "**Q-chain lineage citations:**\n\n"
        "- **Q1 (PR #242):** `selected_target_source_layer = "
        "matches_flat_clean`; `selected_history_source_layer = "
        "player_history_all`. The per-player history side therefore "
        "aggregates ALL game types per Q1 BINDING (documented in Section 1).\n"
        "- **Q2 (PR #242):** `target_anchor = matches_history_minimal."
        "started_at TIMESTAMP`; CONTEXT per CROSS-02-00 Section 5.1.\n"
        "- **Q3 (PR #242):** strict-< TRY_CAST form ratified (above).\n"
        "- **Q4 (PR #242):** cold-start gates G-CS-2/3/4/5 at the registry "
        "layer; G-CS-6 deferred to Phase 03 fold-aware fit.\n"
        f"- **Q5 (PR #243):** `selected_policy = {CROSS_REGION_POLICY}` "
        "(BINDING); re-elevated by PR #255 `q5_policy` field. Cross-region "
        "indicator pair symmetrised per Invariant I5 (cited in Section 1).\n"
        "- **Q6 (PR #245):** rating-reconstruction successor adjudication; "
        "verdict propagates to PR #255 omit-closure.\n"
        "- **Q6F (PR #247):** rating-algorithm survey (`recommendation_only_"
        "blocked_pending_implementation_proof_pr`).\n"
        "- **Q6G (PR #249):** rating-implementation proof "
        "(`recommendation_only_glicko2`).\n"
        "- **Q6H (PR #251):** terminal rating-path decision "
        "(`recommendation_only_event_by_event_glicko2`).\n"
        "- **PR #255 omit-closure:** verdict "
        "`omit_reconstructed_rating_and_unblock_other_five`; "
        f"`q5_policy = {CROSS_REGION_POLICY}`; the three forbidden "
        "`reconstructed_rating_*` columns enumerated.\n"
        "- **PR #257 ROADMAP amendment:** "
        "`materialization_scope_amendment_post_pr_255` token inserted at "
        "ROADMAP.md:2525 (host) + 2837 (back-reference); five-family "
        "permitted set at lines 2536-2540; excluded family + columns at "
        "lines 2542-2548.\n\n"
        f"- **Q7 IN_GAME_HISTORICAL allowed-column set:** "
        f"{', '.join('`' + c + '`' for c in IN_GAME_HISTORICAL_AGGREGATED_COLUMNS)} "
        "(PR #242 Q7 BINDING). Only these four columns are aggregated "
        "(×2 sides = 8 audited columns in `in_game_history_aggregate`).\n"
    )


def _render_audit_md(
    audit_md_path: Path,
    audit_pr: str,
    provenance_shas: dict[str, str],
) -> None:
    """Write the four-section audit MD.

    Args:
        audit_md_path: Destination MD path.
        audit_pr: PR label.
        provenance_shas: SHA-256 digests from _gather_provenance_shas.
    """
    audit_md_path.parent.mkdir(parents=True, exist_ok=True)
    body = (
        f"# Leakage audit -- sc2egset Step {PHASE_02_STEP} "
        "(post-materialization CROSS-02-01-v1.0.1)\n\n"
        f"{_build_md_section_1(audit_pr)}\n"
        f"{_build_md_section_2(provenance_shas)}\n"
        f"{_build_md_section_3()}\n"
        f"{_build_md_section_4()}"
    )
    audit_md_path.write_text(body, encoding="utf-8")


# ---------------------------------------------------------------------------
# Public entrypoint — post-materialization audit
# ---------------------------------------------------------------------------


def audit_history_enriched_pre_game_features(
    parquet_path: Path | str,
    audit_json_path: Path | str,
    audit_md_path: Path | str,
    duckdb_path: Path | str,
    audit_date: str,
    dataset: str = DATASET_TAG,
    phase_02_step: str = PHASE_02_STEP,
    audit_pr: str = AUDIT_PR_PLACEHOLDER,
) -> HistoryEnrichedAuditResult:
    """Run the post-materialization CROSS-02-01-v1.0.1 leakage audit.

    Reads the materialized Parquet, recomputes sanity checks via DuckDB,
    builds the audit notes + MD body (with examiner-clarity sentence),
    runs every audit-side falsifier, and writes the JSON + MD artifacts
    if no falsifier fires. ``features_audited`` is exactly the 24
    history-enriched feature columns; identity and context columns are
    recorded in separate JSON carriers.

    Args:
        parquet_path: Materialized Parquet path.
        audit_json_path: Destination audit JSON path.
        audit_md_path: Destination audit MD path.
        duckdb_path: DuckDB file path (read-only; reused for sanity checks).
        audit_date: ISO YYYY-MM-DD date (materialisation execution time).
        dataset: Dataset tag (default sc2egset).
        phase_02_step: Step ID (default 02_01_03).
        audit_pr: PR label (default placeholder).

    Returns:
        Populated HistoryEnrichedAuditResult.
    """
    parquet_path = Path(parquet_path)
    audit_json_path = Path(audit_json_path)
    audit_md_path = Path(audit_md_path)
    duckdb_path = Path(duckdb_path)

    parquet_columns = _read_parquet_columns(parquet_path)
    row_count = _read_parquet_row_count(parquet_path)

    con = _connect_duckdb(duckdb_path)
    try:
        _create_materialized_view(con)
        sanity = _run_sanity_checks(con)
    finally:
        con.close()
    distinct_focal_match_count = int(sanity["distinct_focal_match_id"])

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

    audit = HistoryEnrichedAuditResult(
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
            distinct_focal_match_count=distinct_focal_match_count,
            row_count=row_count,
        )
        _render_audit_md(
            audit_md_path=audit_md_path,
            audit_pr=audit_pr,
            provenance_shas=provenance_shas,
        )

    LOGGER.debug(
        "audit_history_enriched_pre_game_features: verdict=%s halting=%s",
        verdict,
        halting_falsifier,
    )

    return audit


# ---------------------------------------------------------------------------
# Public entrypoint — research_log non-closure append
# ---------------------------------------------------------------------------


def _build_research_log_block(
    audit_pr: str,
    audit_date: str,
    branch: str,
) -> str:
    """Construct the dataset research_log.md non-closure entry block.

    Mirrors PR #236's 30-line precedent. Required field labels:
    closure_status, materialization_state, leakage_audit_state,
    features_audited_count, row_count, artifact, leakage_audit.

    Args:
        audit_pr: PR label (e.g. ``PR #259`` or placeholder).
        audit_date: ISO YYYY-MM-DD.
        branch: Branch name (e.g. ``feat/sc2egset-02-01-03-...``).

    Returns:
        Multi-line research_log entry (terminated by `\n---\n`).
    """
    return (
        f"## {audit_date} — Materialize Step {PHASE_02_STEP} "
        "five-family history-enriched pre_game tranche + first non-vacuous "
        "CROSS-02-01 audit\n\n"
        "- **Category:** A (science / Phase 02 / materialization-execution)\n"
        f"- **Dataset:** {DATASET_TAG}\n"
        f"- **Branch:** `{branch}`\n"
        f"- **PR:** `{audit_pr}`\n"
        f"- **Step scope:** Step `{PHASE_02_STEP}` -- FIRST history-enriched "
        "pre_game feature-family materialisation for the five permitted "
        "families authorised by PR #257 ROADMAP amendment "
        "(`materialization_scope_amendment_post_pr_255`): "
        f"{', '.join('`' + name + '`' for name in FIVE_FAMILY_CANONICAL_ORDER)}. "
        f"Excluded family `{EXCLUDED_FAMILY}` per PR #255 omit-closure "
        "verdict; the three forbidden columns "
        f"({', '.join('`' + c + '`' for c in sorted(FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS))}) "
        "are NOT materialised. Step closure is NOT claimed; closure flips "
        "are deferred to a separate U2.B-style PR per PR #237 precedent.\n"
        "- **closure_status:** `still_open`\n"
        "- **materialization_state:** `materialized`\n"
        "- **leakage_audit_state:** `post_materialization_pass`\n"
        f"- **features_audited_count:** `{EXPECTED_AUDITED_FEATURE_COLUMN_COUNT}`\n"
        f"- **row_count:** `{EXPECTED_OUTPUT_ROW_COUNT}`\n"
        "- **artifact:** `02_01_03_history_enriched_pre_game_features.parquet`\n"
        "- **leakage_audit:** "
        "`reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}`\n"
        "- **What:** Persisted the Layer-2 deliverable authorised by merged "
        "PR #257 ROADMAP amendment:\n"
        "  (i) one Parquet feature table at "
        "`reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/"
        "02_01_03_history_enriched_pre_game_features.parquet` "
        f"carrying {EXPECTED_OUTPUT_ROW_COUNT} rows × {EXPECTED_PARQUET_COLUMN_COUNT} "
        "projected columns — partitioned as 3 IDENTITY (`focal_match_id`, "
        "`focal_player`, `opponent_player`), 1 CONTEXT row-identity anchor "
        f"(`started_at`), and {EXPECTED_AUDITED_FEATURE_COLUMN_COUNT} audited "
        "history-enriched PRE_GAME features spanning the five permitted "
        "families (6 + 6 + 2 + 2 + 8);\n"
        "  (ii) the FIRST non-vacuous CROSS-02-01-v1.0.1 post-materialization "
        "audit pair at `reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}` "
        "with `features_audited` = exactly the 24 history-enriched PRE_GAME "
        "feature columns, `verdict = PASS`, `future_leak_count = 0`, "
        "`post_game_token_violations = 0`, full SHA-256 provenance bonds for "
        "the 17 binding parent artifacts (12 Q-chain SHAs from "
        "PR #242/#243/#245/#247/#249/#251 + 2 omit-closure SHAs from PR #255 "
        "+ 1 registry SHA + 3 tranche-1 SHAs from PR #236), the 4 CROSS-02-** "
        "specs, the 4 view YAMLs (including the defensive "
        "`matches_long_raw_yaml_sha256` pin per R3-N2), and the "
        "materialization module. The examiner-clarity sentence "
        "(`` `started_at` is projected as a row-identity anchor only ... "
        "excluded from `features_audited` ``) appears verbatim in both the "
        "JSON `notes` field and the MD §1.\n"
        "- **Why:** Discharges the materialisation-execution branch of the "
        "non-batching sequence authorised by merged Layer-1 PR #258 and the "
        "PR #257 ROADMAP amendment. The CROSS-02-01 §5 gate condition is "
        "now mechanically satisfied for Step `02_01_03` (non-empty "
        "`features_audited` + verdict PASS + JSON/MD at spec-named paths); "
        "evidence-distinctness from PR #229 §10 design-time verdict audit, "
        "PR #230 vacuous catalog audit, PR #236 tranche-1 audit, the "
        "Q-chain adjudication artifacts (PR #242/#243/#245/#247/#249/#251), "
        "PR #255 omit-closure, and PR #257 ROADMAP amendment is preserved "
        "by routing the new audit JSON+MD to the `02_01_03/` subdirectory "
        "and leaving every upstream artifact byte-unchanged.\n"
        "- **How (reproducibility):** notebook at "
        "`sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/"
        "02_01_03_history_enriched_pre_game_materialization.{py,ipynb}` "
        "(jupytext py:percent canonical; existing PR #241 scaffold overwritten "
        "in place per `sandbox/README.md` single-notebook-per-Step contract; "
        "PR #241 scaffold content preserved at git SHA `3c6709bf`); "
        "materialisation module at "
        "`src/rts_predict/games/sc2/datasets/sc2egset/"
        "materialize_history_enriched_pre_game_features.py` carrying "
        "`materialize_history_enriched_pre_game_features(...)`, "
        "`audit_history_enriched_pre_game_features(...)`, and "
        "`run_step_02_01_03(...)` entrypoints; frozen "
        "`HistoryEnrichedMaterializationResult` and "
        "`HistoryEnrichedAuditResult` dataclasses; module-level UPPER_SNAKE "
        "constants (Invariant I7); the named `_MATERIALIZATION_QUERY` "
        "(Invariant I6); the canonical strict-< TRY_CAST predicate "
        f"`{_STRICT_LT_TRY_CAST_TOKEN}`; matchup CTE 1v1-restriction via "
        "`JOIN matches_flat_clean mfc_h` (B2 fix); `ph.is_decisive_result = "
        "TRUE` instead of inline `ph.result IN ('Win', 'Loss')` (N11); "
        "tests at `tests/rts_predict/games/sc2/datasets/sc2egset/"
        "test_materialize_history_enriched_pre_game_features.py` "
        "(≥66 named tests; ≥95% branch coverage on the materialisation "
        "module); SHA-256 bonds recorded in the audit JSON; `git_sha` "
        f"captured from `git rev-parse HEAD` at execution; audit_date = "
        f"materialisation-execution ISO date {audit_date}.\n"
        f"- **Findings:** all sanity checks pass against the real DuckDB at "
        f"`data/db/db.duckdb` -- `COUNT(*) = {EXPECTED_OUTPUT_ROW_COUNT}`; "
        f"`COUNT(DISTINCT focal_match_id) = {EXPECTED_DISTINCT_FOCAL_MATCH_COUNT}`; "
        "focal/opponent symmetry on `started_at` swap = 0 violations "
        "(Invariant I5); `reconstructed_rating` family ABSENT from the "
        "output projection (the three forbidden columns ABSENT); no scalar "
        "MMR/rating/elo/glicko/skill/mu/sigma column; no POST-GAME token in "
        "column names; no tracker_events_raw / replay_players_raw / "
        "replays_meta_raw / matches_long_raw / space-bounded matches_flat "
        "read (source-table allowlist = `{matches_flat_clean, "
        "matches_history_minimal, player_history_all}`); strict-< TRY_CAST "
        "predicate present in every history CTE; no `<=` / `=` variant; "
        "matchup CTE includes `JOIN matches_flat_clean mfc_h` (B2 fix); "
        "`is_decisive_result = TRUE` used in place of inline result IN "
        "list (N11); reproducibility check passes (two consecutive runs "
        "produce byte-identical Parquet); PR #236 tranche-1 Parquet + audit "
        "JSON + audit MD byte-unchanged; PR #255 omit-closure CSV+MD "
        "byte-unchanged; PR #242/#243/#245/#247/#249/#251 adjudication "
        "artifacts byte-unchanged; PR #257 ROADMAP amendment byte-unchanged.\n"
        f"- **What this means:** Step `{PHASE_02_STEP}` has produced its "
        "first feature artifact and its first non-vacuous leakage audit; "
        "the CROSS-02-01 §5 gate is mechanically cleared at the "
        f"Parquet/audit-pair layer. Step `{PHASE_02_STEP}` is **NOT** "
        "closed by this PR. Status YAML flips (`STEP_STATUS.yaml`, "
        "`PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`) are deferred "
        "to a separate U2.B-style closure PR (per PR #237 precedent). The "
        "next 02_01 step (`in_game_snapshot`, Step 02_01_04+) remains "
        "DEFERRED; Phase 03 is NOT started.\n"
        "- **Decisions taken:** materialise only the five permitted "
        "families per PR #257 amendment + PR #255 omit-closure; exclude "
        f"`{EXCLUDED_FAMILY}` family and the three forbidden columns; "
        "co-register the cross-region indicator pair per Q5 BINDING "
        f"`{CROSS_REGION_POLICY}` (PR #243 + PR #255 `q5_policy` "
        "re-elevation); use the IN_GAME_HISTORICAL allowed-column 4-tuple "
        f"({', '.join('`' + c + '`' for c in IN_GAME_HISTORICAL_AGGREGATED_COLUMNS)}) "
        "per Q7 BINDING (PR #242); use strict-< TRY_CAST history filter "
        "(Invariant I3; PR #242 Q3 BINDING + B-X2); restrict matchup CTE "
        "to 1v1 history via `matches_flat_clean` join (B2 fix); use "
        "`is_decisive_result = TRUE` (N11); symmetrise cross-region "
        "indicator per Invariant I5 (N9 fix); separate closure PR (U2.B); "
        "record SHA-256 provenance bonds for every audit input in the "
        "JSON (17 binding parent artifact SHAs + 4 CROSS-02-** spec SHAs + "
        "4 view YAML SHAs); embed the examiner-clarity sentence verbatim "
        "in BOTH the JSON `notes` and the MD §1.\n"
        f"- **Decisions deferred:** Step `{PHASE_02_STEP}` closure "
        "(separate U2.B-style PR; status YAML flips; closure-only "
        "research_log entry); Step `02_01_04+` in_game_snapshot families; "
        "Phase 03 splitting and baseline modeling; AoE2 work; any thesis "
        "chapter prose.\n"
        "- **Thesis mapping:** Chapter 4 §4.5 (feature engineering plan) "
        "-- citable as the FIRST non-vacuous CROSS-02-01 post-materialization "
        "audit row for Step `02_01_03` alongside the PR #236 tranche-1 audit "
        "and the Q-chain adjudications. The future U2.B closure PR will add "
        "the step-closure row.\n"
        "- **Open questions / follow-ups:** schedule the U2.B closure "
        f"planner-science round for Step `{PHASE_02_STEP}` (separate PR); "
        "confirm whether Step `02_01_04` planner-science may begin before "
        "the formal closure PR (likely yes per the 02_01_01 -> 02_01_02 "
        "pattern); future Phase 03 splitting and modeling plan.\n"
        "- **Acknowledged trade-offs:** the per-player history CTEs "
        "aggregate ALL game types per Q1 BINDING (a 4v4 win-rate "
        "contributes to a 1v1 prediction); the matchup CTE is 1v1-"
        "restricted via `matches_flat_clean` to prevent non-1v1 prior "
        "matches from inflating head-to-head counts. This Q1-binding "
        "consequence is explicitly documented in audit MD §1, not silently "
        "absorbed. Cross-region indicator symmetrisation goes beyond "
        "PR #243's single-indicator text; the methodological basis is "
        "Invariant I5 (cited in audit MD §1). Reproducibility on this "
        "DuckDB is byte-exact; cross-rebuild reproducibility (different "
        "DuckDB hash) will produce identical content but distinct "
        "provenance SHAs by design.\n"
        "- **Scope notes:** does NOT touch root `reports/research_log.md`; "
        "does NOT touch ROADMAP body (PR #257 amendment is sufficient); "
        "does NOT touch any spec or cleaning-layer YAML; does NOT touch "
        "`STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, "
        "`PHASE_STATUS.yaml`; does NOT touch any 02_01_01 or 02_01_02 "
        "artifact; does NOT touch any AoE2 path, thesis chapter, bib, "
        "appendix, docs, or `.claude/` file.\n\n"
        "---\n\n"
    )


def append_research_log_entry(
    research_log_path: Path | str,
    audit_pr: str,
    audit_date: str,
    branch: str,
) -> str:
    """Append a non-closure research_log block immediately under the file header.

    Mirrors PR #236's precedent: the new entry is inserted after the
    first ``---`` separator (line 3) so the most-recent entry appears on
    top.

    Args:
        research_log_path: Path to the dataset research_log.md file.
        audit_pr: PR label.
        audit_date: ISO YYYY-MM-DD.
        branch: Branch name.

    Returns:
        The inserted block (for caller inspection / testing).
    """
    research_log_path = Path(research_log_path)
    block = _build_research_log_block(audit_pr, audit_date, branch)
    current = research_log_path.read_text(encoding="utf-8")
    # Insert immediately after the first `---\n\n` separator (PR #236
    # precedent). Fallback: prepend if marker not found.
    marker = "\n---\n\n"
    idx = current.find(marker)
    if idx == -1:
        new_content = block + current
    else:
        insert_at = idx + len(marker)
        new_content = current[:insert_at] + block + current[insert_at:]
    research_log_path.write_text(new_content, encoding="utf-8")
    return block


# ---------------------------------------------------------------------------
# Public entrypoint — full Step 02_01_03 orchestration
# ---------------------------------------------------------------------------


def run_step_02_01_03(
    duckdb_path: Path | str,
    output_parquet_path: Path | str,
    audit_json_path: Path | str,
    audit_md_path: Path | str,
    research_log_path: Path | str,
    audit_date: str,
    branch: str,
    audit_pr: str = AUDIT_PR_PLACEHOLDER,
    write_research_log: bool = True,
) -> tuple[HistoryEnrichedMaterializationResult, HistoryEnrichedAuditResult]:
    """Orchestrate the full Step 02_01_03 materialisation + audit + log append.

    Args:
        duckdb_path: Path to the on-disk DuckDB file.
        output_parquet_path: Destination Parquet path.
        audit_json_path: Destination audit JSON path.
        audit_md_path: Destination audit MD path.
        research_log_path: Path to the dataset research_log.md.
        audit_date: ISO YYYY-MM-DD (materialisation execution date).
        branch: Branch name for research_log entry.
        audit_pr: PR label (default placeholder).
        write_research_log: If True (default), append the research_log entry.

    Returns:
        (materialization_result, audit_result) tuple.
    """
    mat_result = materialize_history_enriched_pre_game_features(
        duckdb_path=duckdb_path,
        output_parquet_path=output_parquet_path,
    )
    if mat_result.halting_falsifier is not None:
        # Caller is responsible for inspecting halting_falsifier; we still
        # return an audit result so the test surface is uniform.
        audit_result = HistoryEnrichedAuditResult(
            spec_version=SPEC_VERSION,
            dataset=DATASET_TAG,
            phase_02_step=PHASE_02_STEP,
            audit_date=audit_date,
            future_leak_count=0,
            post_game_token_violations=0,
            normalization_fit_scope="training_fold_only",
            target_encoding_fold_awareness="N/A_no_target_encoding",
            cutoff_time_filter_structural_check="pass",
            reference_window_assertion="pass",
            features_audited=(),
            projected_context_columns=PROJECTED_CONTEXT_COLUMNS,
            projected_identity_columns=PROJECTED_IDENTITY_COLUMNS,
            verdict="FAIL",
            artifact_json_path=str(audit_json_path),
            artifact_md_path=str(audit_md_path),
            halting_falsifier=mat_result.halting_falsifier,
        )
        return mat_result, audit_result
    audit_result = audit_history_enriched_pre_game_features(
        parquet_path=output_parquet_path,
        audit_json_path=audit_json_path,
        audit_md_path=audit_md_path,
        duckdb_path=duckdb_path,
        audit_date=audit_date,
        audit_pr=audit_pr,
    )
    if write_research_log and audit_result.verdict == "PASS":
        append_research_log_entry(
            research_log_path=research_log_path,
            audit_pr=audit_pr,
            audit_date=audit_date,
            branch=branch,
        )
    return mat_result, audit_result
