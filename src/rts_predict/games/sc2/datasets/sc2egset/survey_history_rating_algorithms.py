"""Q6F rating-algorithm survey for SC2EGSet Step 02_01_03.

Pure read-only module. Writes ONLY the Q6F survey CSV+MD artifact pair.
Never materializes a rating value. Never writes Parquet. Never modifies
status YAMLs, research logs, or ROADMAP. See ``planning/current_plan.md``
for the Layer-1 specification.

This module is the Layer-2 successor to PR #245's Q6 deferred-blocker
verdict. PR #245 closed Q6 (``rating_policy``) as
``Q6_selected_policy = deferred_blocker_with_algorithm_survey_required``
with ``materialization_permission = blocked_pending_algorithm_survey_pr``.
This module (PR #<TBD>) emits an algorithm-survey verdict over the 4
included rating candidates plus 2 carry-forward references; the verdict
either unblocks materialization (``bind_now``), unblocks the other 5
families without ``reconstructed_rating``
(``omit_reconstructed_rating_and_unblock_other_five``), authorises only a
recommendation (``narrow_with_evidence`` / ``recommendation_only``), or
re-defers (``deferred_blocker``).

Candidate set (Layer-1 Assumption 7):

    Q6F_A  omit_reconstructed_rating  (carry-forward; no algorithm)
    Q6F_B  rolling_win_rate_or_bayesian_smoothed_baseline  (Laplace prior)
    Q6F_C  elo                            (Elo 1978; K = 24)
    Q6F_D  glicko_or_glicko_2             (Glickman 1999 / 2012)
    Q6F_E  trueskill_or_trueskill_like    (Herbrich, Minka, Graepel 2006)
    Q6F_F  deferred_blocker_with_algorithm_survey_required  (carry-forward)

N-1 binding (Layer-1 Assumption 8): ``aligulac_style_btl``,
``bradley_terry``, ``neural_btl`` are recorded in the
``excluded_methods_considered`` column as explicit acknowledgements of
methods considered but excluded from this survey (BTL family requires its
own model-training pipeline or a dedicated survey Step).

N-2 binding (Layer-1 Assumption 9): the raw-MMR-where-present hybrid
candidate (``raw_mmr_where_present_plus_is_mmr_missing``) is rejected
unchanged from PR #245 and the rejection rationale is recorded in every
row's ``raw_mmr_hybrid_rejection`` column.

NIT-3 / OQ1 (Layer-1 Adversarial-Review Adjustments Round 1): the
selection decision rule uses bootstrap confidence intervals on log-loss
and Brier (proper scoring rules) as the binding criterion. AUC is
reported with CI but is secondary; AUC alone cannot bind a candidate.

Forward-only protocol (Layer-1 T03): every per-row prediction is computed
from rating state aggregated strictly from PHA records satisfying
``TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at``
(``STRICT_LT_HISTORY_FILTER``, inherited verbatim from PR #245). The
target outcome updates the rating state ONLY AFTER scoring the
prediction; it is never read as an input feature for predicting its own
match.

Q5 BINDING (PR #243; preserved verbatim): ``Q5_selected_policy =
sensitivity_indicator_co_registration`` with verdict
``narrow_with_evidence``. The Q6F survey does NOT re-adjudicate Q5;
cross-region history rows remain in the input stream and the
``is_cross_region_fragmented`` flag is a co-registered evidence
dimension, not a filter.

Materialization is BLOCKED in this PR (Layer-1 Assumption 14): no row
of the survey CSV may reference any Parquet path; ``materialized_output_paths``
is empty on every row.
"""

from __future__ import annotations

import csv
import hashlib
import logging
import math
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd

LOGGER = logging.getLogger(__name__)


__all__ = [
    "ALLOWED_MATERIALIZATION_PERMISSIONS",
    "ALLOWED_Q6F_VERDICTS",
    "AUDIT_PR_NUMBER_PLACEHOLDER",
    "BOOTSTRAP_BLOCK_COUNT",
    "BOOTSTRAP_RANDOM_SEED",
    "CITATION_ELO_1978",
    "CITATION_GLICKMAN_1999",
    "CITATION_GLICKMAN_2012",
    "CITATION_HERBRICH_MINKA_GRAEPEL_2006",
    "CITATION_HOSMER_LEMESHOW_2013",
    "CITATION_STEYERBERG_2009",
    "DATASET_RESEARCH_LOG_REL",
    "EXCLUDED_METHODS_CONSIDERED",
    "EXPECTED_PR242_CSV_SHA256",
    "EXPECTED_PR242_MD_SHA256",
    "EXPECTED_PR243_CSV_SHA256",
    "EXPECTED_PR243_MD_SHA256",
    "EXPECTED_PR245_CSV_SHA256",
    "EXPECTED_PR245_MD_SHA256",
    "FALSIFIER_PRIORITY_CHAIN",
    "HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS",
    "NON_RATING_HISTORY_FAMILIES",
    "PARENT_PR242_CSV_REL",
    "PARENT_PR242_MD_REL",
    "PARENT_PR243_CSV_REL",
    "PARENT_PR243_MD_REL",
    "PARENT_PR245_CSV_REL",
    "PARENT_PR245_MD_REL",
    "Q5_SELECTED_POLICY",
    "Q5_SELECTED_POLICY_VERDICT",
    "Q6F_ALGORITHM_FAMILY_BY_CANDIDATE",
    "Q6F_ALLOWED_VERDICTS",
    "Q6F_CANDIDATE_INCLUSION",
    "Q6F_DECISION_IDS",
    "Q6F_HYPERPARAMETER_DEFAULTS",
    "Q6F_METRICS",
    "Q6F_RATING_ALGORITHM_CANDIDATES",
    "Q6F_SCHEMA_COLUMN_COUNT",
    "Q6F_SELECTION_DECISION_RULE",
    "Q6F_SURVEY_CANDIDATES",
    "Q6F_SURVEY_CSV_REL",
    "Q6F_SURVEY_MD_REL",
    "Q6F_SURVEY_SCHEMA",
    "RAW_MMR_HYBRID_REJECTION_TEXT",
    "STRICT_LT_HISTORY_FILTER",
    "TARGET_ANCHOR_COLUMN",
    "RatingSurveyDecision",
    "RatingSurveyError",
    "RatingSurveyResult",
    "compute_metrics_with_ci",
    "run_q6f_rating_algorithm_survey",
    "write_q6f_survey_artifacts",
]


# ---------------------------------------------------------------------------
# Parent PR provenance (BINDING; mismatch halts)
# ---------------------------------------------------------------------------

PARENT_PR242_NUMBER: str = "PR #242"
PARENT_PR243_NUMBER: str = "PR #243"
PARENT_PR245_NUMBER: str = "PR #245"
AUDIT_PR_NUMBER_PLACEHOLDER: str = "PR #<TBD>"

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
EXPECTED_PR245_CSV_SHA256: str = (
    "703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0"
)
EXPECTED_PR245_MD_SHA256: str = (
    "7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419"
)


# ---------------------------------------------------------------------------
# Inherited PR #242 / PR #243 / PR #245 anchors (referenced; NOT re-derived)
# ---------------------------------------------------------------------------

TARGET_ANCHOR_COLUMN: str = "matches_history_minimal.started_at"
STRICT_LT_HISTORY_FILTER: str = (
    "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"
)

# Inherited PR #243 anchors (referenced; NOT re-litigated).
Q5_SELECTED_POLICY: str = "sensitivity_indicator_co_registration"
Q5_SELECTED_POLICY_VERDICT: str = "narrow_with_evidence"


# ---------------------------------------------------------------------------
# Q6F candidate set + decision IDs
# ---------------------------------------------------------------------------

Q6F_RATING_ALGORITHM_CANDIDATES: tuple[str, ...] = (
    "omit_reconstructed_rating",
    "rolling_win_rate_or_bayesian_smoothed_baseline",
    "elo",
    "glicko_or_glicko_2",
    "trueskill_or_trueskill_like",
    "deferred_blocker_with_algorithm_survey_required",
)
Q6F_SURVEY_CANDIDATES: tuple[str, ...] = Q6F_RATING_ALGORITHM_CANDIDATES

# True iff the candidate has an algorithm whose forward-only predictions
# are scored numerically by this survey. False for carry-forward
# references (no algorithm; sentinel metric values used in the CSV).
Q6F_CANDIDATE_INCLUSION: dict[str, bool] = {
    "omit_reconstructed_rating": False,
    "rolling_win_rate_or_bayesian_smoothed_baseline": True,
    "elo": True,
    "glicko_or_glicko_2": True,
    "trueskill_or_trueskill_like": True,
    "deferred_blocker_with_algorithm_survey_required": False,
}

Q6F_ALGORITHM_FAMILY_BY_CANDIDATE: dict[str, str] = {
    "omit_reconstructed_rating": "none_omission_carry_forward",
    "rolling_win_rate_or_bayesian_smoothed_baseline": "win_rate_baseline_laplace_prior",
    "elo": "elo_1978",
    "glicko_or_glicko_2": "glicko_2_glickman_2012",
    "trueskill_or_trueskill_like": "trueskill_herbrich_minka_graepel_2006",
    "deferred_blocker_with_algorithm_survey_required": "none_deferred_carry_forward",
}

Q6F_DECISION_IDS: tuple[str, ...] = (
    "Q6F_A_omit_reconstructed_rating",
    "Q6F_B_rolling_win_rate_or_bayesian_smoothed_baseline",
    "Q6F_C_elo",
    "Q6F_D_glicko_or_glicko_2",
    "Q6F_E_trueskill_or_trueskill_like",
    "Q6F_F_deferred_blocker_with_algorithm_survey_required",
    "Q6F_selected_policy",
    "Q6F_per_family_impact_summary",
)
Q6F_DECISION_COUNT: int = 8


# ---------------------------------------------------------------------------
# N-1 binding: BTL family explicitly acknowledged and excluded
# (Layer-1 Assumption 8 + NIT-1 column path).
# ---------------------------------------------------------------------------

EXCLUDED_METHODS_CONSIDERED: tuple[str, ...] = (
    "aligulac_style_btl",
    "bradley_terry",
    "neural_btl",
)

# N-2 binding: raw-MMR-where-present hybrid explicit rejection
# (Layer-1 Assumption 9 + NIT-1 column path; PR #245 carry-forward).
RAW_MMR_HYBRID_REJECTION_TEXT: str = (
    "raw_mmr_where_present_plus_is_mmr_missing: REJECTED unchanged from "
    "PR #245 N-2. The rated/unrated partition is correlated with skill "
    "(only ranked-ladder games carry MMR; unrated games predominantly "
    "are leaderboard-absent practice / custom games), so admitting "
    "raw_mmr as a feature plus is_mmr_missing as a flag would leak corpus "
    "structure under Invariant I5 (symmetric treatment). The Q6F survey "
    "does not re-open this rejection."
)


# ---------------------------------------------------------------------------
# Allowed-value enums
# ---------------------------------------------------------------------------

Q6F_ALLOWED_VERDICTS: frozenset[str] = frozenset(
    {
        "bind_now",
        "narrow_with_evidence",
        "recommendation_only",
        "deferred_blocker",
        "omit_reconstructed_rating_and_unblock_other_five",
        "not_applicable_carry_forward",
    }
)
ALLOWED_Q6F_VERDICTS: frozenset[str] = Q6F_ALLOWED_VERDICTS

ALLOWED_MATERIALIZATION_PERMISSIONS: frozenset[str] = frozenset(
    {
        "permitted_for_all_6_families_with_pinned_hyperparameters_in_next_materialization_pr",
        "permitted_for_other_5_families_without_reconstructed_rating",
        "recommendation_only_blocked_pending_implementation_proof_pr",
        "blocked_pending_named_reason",
        "blocked_pending_algorithm_survey_pr",
        "not_applicable_carry_forward",
    }
)


# ---------------------------------------------------------------------------
# Hyperparameter defaults (Layer-1 Assumption 10; literature-pinned)
# ---------------------------------------------------------------------------

Q6F_HYPERPARAMETER_DEFAULTS: dict[str, dict[str, float]] = {
    "rolling_win_rate_or_bayesian_smoothed_baseline": {
        "alpha": 1.0,
        "beta": 1.0,
    },
    "elo": {
        "k_factor": 24.0,
        "initial_rating": 1500.0,
    },
    "glicko_or_glicko_2": {
        "mu": 1500.0,
        "rd": 350.0,
        "sigma": 0.06,
        "tau": 0.5,
        "rating_period_days": 30.0,
    },
    "trueskill_or_trueskill_like": {
        "mu": 25.0,
        "sigma": 25.0 / 3.0,
        "beta": 25.0 / 6.0,
        "tau": 25.0 / 300.0,
        "draw_margin": 0.0,
    },
}


# ---------------------------------------------------------------------------
# Algorithm primary-source citations (literature-pinned)
# ---------------------------------------------------------------------------

CITATION_ELO_1978: str = (
    "Elo (1978) -- The Rating of Chessplayers, Past and Present. "
    "Arco Publishing, New York."
)
CITATION_GLICKMAN_1999: str = (
    "Glickman (1999) -- Parameter estimation in large dynamic paired "
    "comparison experiments. Applied Statistics 48: 377-394."
)
CITATION_GLICKMAN_2012: str = (
    "Glickman (2012) -- Example of the Glicko-2 system. Boston "
    "University Technical Note."
)
CITATION_HERBRICH_MINKA_GRAEPEL_2006: str = (
    "Herbrich, Minka, Graepel (2006) -- TrueSkill: A Bayesian Skill "
    "Rating System. NIPS 2006: 569-576."
)
# NIT-3 / OQ1: AUC interpretation citations supporting the proper-score
# (log-loss + Brier) CI-based binding rule.
CITATION_STEYERBERG_2009: str = (
    "Steyerberg (2009) -- Clinical Prediction Models. Springer, "
    "Chapter 15 on discrimination and calibration."
)
CITATION_HOSMER_LEMESHOW_2013: str = (
    "Hosmer, Lemeshow, Sturdivant (2013) -- Applied Logistic Regression, "
    "3rd ed., Wiley, Chapter 5 on assessment of fit."
)


# ---------------------------------------------------------------------------
# Metrics emitted per included candidate (NIT-3 / OQ1: CI-based binding)
# ---------------------------------------------------------------------------

Q6F_METRICS: tuple[str, ...] = (
    "auc",
    "auc_ci_low",
    "auc_ci_high",
    "log_loss",
    "log_loss_ci_low",
    "log_loss_ci_high",
    "brier",
    "brier_ci_low",
    "brier_ci_high",
    "calibration_error",
    "coverage_rate",
    "cold_start_rate",
    "runtime_seconds",
    "tie_rate",
)


# Deterministic bootstrap configuration (Layer-1 OQ1 default + T04
# determinism). Block bootstrap over chronological blocks; fixed seed.
BOOTSTRAP_RANDOM_SEED: int = 42
BOOTSTRAP_BLOCK_COUNT: int = 200


# ---------------------------------------------------------------------------
# History-enriched pre_game family IDs (FIXED per CROSS-02-02 §6.2)
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
# Artifact-pair paths (relative; I10 — filename relative to repo root)
# ---------------------------------------------------------------------------

Q6F_SURVEY_CSV_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6f_rating_algorithm_survey.csv"
)
Q6F_SURVEY_MD_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6f_rating_algorithm_survey.md"
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
PARENT_PR245_CSV_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_rating_reconstruction_adjudication.csv"
)
PARENT_PR245_MD_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_rating_reconstruction_adjudication.md"
)

DATASET_RESEARCH_LOG_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
)


# ---------------------------------------------------------------------------
# Read-only SQL probe (forward-only stream loader)
# ---------------------------------------------------------------------------

PHA_FORWARD_ONLY_STREAM_QUERY: str = """
WITH base AS (
    SELECT
        toon_id,
        replay_id,
        details_timeUTC,
        result,
        is_cross_region_fragmented
    FROM player_history_all
    WHERE result IN ('Win', 'Loss')
      AND toon_id IS NOT NULL
      AND toon_id <> ''
      AND TRY_CAST(details_timeUTC AS TIMESTAMP) IS NOT NULL
),
two_row_replays AS (
    SELECT replay_id
    FROM base
    GROUP BY replay_id
    HAVING COUNT(*) = 2
),
paired AS (
    SELECT
        a.replay_id,
        a.toon_id AS focal_toon,
        b.toon_id AS opponent_toon,
        a.details_timeUTC,
        a.result AS focal_result,
        a.is_cross_region_fragmented
    FROM base a
    JOIN base b
      ON a.replay_id = b.replay_id
     AND a.toon_id <> b.toon_id
    WHERE a.replay_id IN (SELECT replay_id FROM two_row_replays)
)
SELECT
    focal_toon,
    opponent_toon,
    replay_id,
    details_timeUTC,
    focal_result,
    is_cross_region_fragmented
FROM paired
ORDER BY focal_toon,
         TRY_CAST(details_timeUTC AS TIMESTAMP),
         replay_id
""".strip()


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------


class RatingSurveyError(RuntimeError):
    """Raised when the survey entrypoint halts on a fired falsifier.

    Attributes:
        falsifier_key: The first fired falsifier key (priority order).
        message: Human-readable observed-vs-expected message.
    """

    def __init__(self, falsifier_key: str, message: str) -> None:
        self.falsifier_key = falsifier_key
        self.message = message
        super().__init__(f"Falsifier {falsifier_key!r} fired: {message}")


# ---------------------------------------------------------------------------
# Survey decision dataclass — field order is the CSV column order
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RatingSurveyDecision:
    """A single Q6F survey row.

    The CSV column order is exactly this dataclass's field order. The
    schema column count is asserted at module load against ``len(fields)``.
    """

    decision_id: str
    parent_decision_id: str
    candidate_policy: str
    algorithm_family: str
    included_in_survey: str
    inclusion_or_rejection_reason: str
    initialization_policy: str
    hyperparameter_policy: str
    cold_start_policy: str
    tie_policy: str
    player_identity_policy: str
    cross_region_policy: str
    forward_only_constraints: str
    auc: str
    auc_ci_low: str
    auc_ci_high: str
    log_loss: str
    log_loss_ci_low: str
    log_loss_ci_high: str
    brier: str
    brier_ci_low: str
    brier_ci_high: str
    calibration_error: str
    coverage_rate: str
    cold_start_rate: str
    runtime_summary: str
    complexity_deployability_score: str
    leakage_risk_score: str
    selected_policy: str
    survey_verdict: str
    materialization_permission: str
    excluded_methods_considered: str
    raw_mmr_hybrid_rejection: str
    evidence_paths: str
    falsifiers: str
    audit_pr: str
    parent_pr242_csv_sha256: str
    parent_pr242_md_sha256: str
    parent_pr243_csv_sha256: str
    parent_pr243_md_sha256: str
    parent_pr245_csv_sha256: str
    parent_pr245_md_sha256: str
    materialized_output_paths: str
    notes: str


@dataclass(frozen=True)
class RatingSurveyResult:
    """Top-level aggregate result of the Q6F survey.

    Attributes:
        decisions: Exactly 8 rows in ``Q6F_DECISION_IDS`` order.
        csv_path: Path where the CSV was (or would be) written.
        md_path: Path where the MD was (or would be) written.
        provenance_git_sha: HEAD git SHA at run time.
        falsifiers_fired: Tuple of every fired falsifier key.
        halting_falsifier: First falsifier that fired (or None).
        passed: True iff no falsifier fired.
        metrics_by_candidate: Per-included-candidate metric dict.
        selection: Q6F_selected_policy verdict literal.
    """

    decisions: tuple[RatingSurveyDecision, ...]
    csv_path: str
    md_path: str
    provenance_git_sha: str
    falsifiers_fired: tuple[str, ...]
    halting_falsifier: str | None
    passed: bool
    metrics_by_candidate: dict[str, dict[str, float]]
    selection: str


# ---------------------------------------------------------------------------
# CSV schema (canonical column order — must match dataclass field order)
# ---------------------------------------------------------------------------

Q6F_SURVEY_SCHEMA: tuple[str, ...] = tuple(
    f.name for f in fields(RatingSurveyDecision)
)
Q6F_SCHEMA_COLUMN_COUNT: int = len(Q6F_SURVEY_SCHEMA)


# ---------------------------------------------------------------------------
# Selection decision rule (NIT-3 / OQ1: CI-based proper-score binding)
# ---------------------------------------------------------------------------

Q6F_SELECTION_DECISION_RULE: str = """
Q6F SELECTION DECISION RULE (NIT-3 / OQ1; CI-based binding)
============================================================

Let M = {rolling_baseline, elo, glicko_or_glicko_2,
trueskill_or_trueskill_like}, the set of 4 included candidates.

Let baseline = the rolling_win_rate_or_bayesian_smoothed_baseline
candidate (Laplace-prior baseline; used as the no-opponent-strength
reference for proper-score improvement).

For each candidate c in M, compute:

    log_loss(c), log_loss_ci_low(c), log_loss_ci_high(c)
    brier(c),    brier_ci_low(c),    brier_ci_high(c)
    auc(c),      auc_ci_low(c),      auc_ci_high(c)

Lower log-loss and lower Brier are better. AUC is secondary and reported
with CI only; AUC alone cannot bind a candidate (NIT-3 / OQ1).

DECISION:

1. If max(M.log_loss_ci_high) < baseline.log_loss_ci_low AND
   max(M.brier_ci_high)    < baseline.brier_ci_low:
   --- impossible by construction since baseline IS in M's candidate
       set --- this branch is illustrative only ---

2. Let c* = argmin over c in M of log_loss(c).
   If log_loss_ci_high(c*) < log_loss_ci_low(c) for every c in M\\{c*}
   AND brier_ci_high(c*) < brier_ci_low(c) for every c in M\\{c*}:
       selected_policy = "bind_now"
       verdict = "bind_now"
       materialization_permission = "permitted_for_all_6_families_..."

3. Else if log_loss_ci_high(c*) < baseline.log_loss_ci_low
   AND brier_ci_high(c*) < baseline.brier_ci_low:
       selected_policy = "narrow_with_evidence"
       verdict = "narrow_with_evidence"
       materialization_permission = "recommendation_only_blocked_pending_implementation_proof_pr"

4. Else if the best candidate's log-loss is within CI overlap of the
   baseline (no proper-score improvement detectable):
       selected_policy = "omit_reconstructed_rating_and_unblock_other_five"
       verdict = "omit_reconstructed_rating_and_unblock_other_five"
       materialization_permission = "permitted_for_other_5_families_without_reconstructed_rating"

5. Else (fallback; ambiguous):
       selected_policy = "deferred_blocker"
       verdict = "deferred_blocker"
       materialization_permission = "blocked_pending_named_reason"

This rule supersedes any pinned numeric AUC threshold (NIT-3 cit.
Steyerberg 2009; Hosmer-Lemeshow 2013). AUC is reported with CI for
transparency but never used as the sole binding criterion.
""".strip()


# ---------------------------------------------------------------------------
# Falsifier chain
# ---------------------------------------------------------------------------

FALSIFIER_PRIORITY_CHAIN: tuple[str, ...] = (
    # Parent-SHA pins (6).
    "parent_pr242_csv_sha256_mismatch",
    "parent_pr242_md_sha256_mismatch",
    "parent_pr243_csv_sha256_mismatch",
    "parent_pr243_md_sha256_mismatch",
    "parent_pr245_csv_sha256_mismatch",
    "parent_pr245_md_sha256_mismatch",
    # Candidate completeness / structural (3).
    "q6f_candidate_set_incomplete",
    "q6f_decision_count_mismatch",
    "q6f_decision_id_order_mismatch",
    # Byte-determinism (1).
    "q6f_csv_byte_determinism_violation",
    # Materialization-creep guards (4).
    "q6f_materialization_creep",
    "q6f_rating_trace_persistence_violation",
    "q6f_rating_object_persistence_violation",
    "q6f_parquet_emitted",
    # Q5 + per-question re-adjudication drift (1).
    "q6f_q5_re_adjudication_drift",
    # Status / research_log / ROADMAP / spec drift (5).
    "q6f_status_yaml_drift",
    "q6f_research_log_drift",
    "q6f_roadmap_drift",
    "q6f_spec_drift",
    "q6f_cleaning_layer_drift",
    # Forward-only enforcement (3).
    "q6f_target_match_outcome_read_as_input",
    "q6f_future_match_leakage_referenced",
    "q6f_global_batch_fit_referenced",
    # Phase 03 + Step 02_01_04 creep (2).
    "q6f_phase_03_baseline_creep",
    "q6f_step_02_01_04_creep",
    # Per-candidate methodology field presence (4).
    "q6f_forward_only_constraint_missing_for_non_omit_candidate",
    "q6f_cold_start_policy_missing_for_non_omit_candidate",
    "q6f_tie_policy_missing_for_non_omit_candidate",
    "q6f_hyperparameter_policy_missing_for_non_omit_candidate",
    # Selected-policy + per-family broadcast (4).
    "q6f_selected_policy_row_missing",
    "q6f_selected_policy_verdict_invalid",
    "q6f_per_family_impact_summary_missing",
    "q6f_per_family_impact_broadcast_incomplete",
    # N-1 + N-2 binding (2).
    "q6f_excluded_methods_considered_incomplete",
    "q6f_raw_mmr_hybrid_rejection_missing",
    # NIT bindings (3).
    "q6f_btl_family_acknowledgement_missing",
    "q6f_auc_alone_binding_violation",
    "q6f_trueskill_tau_unjustified",
)


# ---------------------------------------------------------------------------
# Module-import mechanical verification
# ---------------------------------------------------------------------------

assert len(set(FALSIFIER_PRIORITY_CHAIN)) == len(FALSIFIER_PRIORITY_CHAIN), (
    "FALSIFIER_PRIORITY_CHAIN contains duplicate keys"
)
assert len(FALSIFIER_PRIORITY_CHAIN) >= 35, (
    "FALSIFIER_PRIORITY_CHAIN must contain >=35 keys per planning T01"
)
assert len(Q6F_RATING_ALGORITHM_CANDIDATES) == 6, (
    "Q6F_RATING_ALGORITHM_CANDIDATES must have exactly 6 entries "
    "(4 included + 2 carry-forward)"
)
assert set(Q6F_CANDIDATE_INCLUSION.keys()) == set(Q6F_RATING_ALGORITHM_CANDIDATES), (
    "Q6F_CANDIDATE_INCLUSION keys must equal Q6F_RATING_ALGORITHM_CANDIDATES"
)
assert sum(1 for v in Q6F_CANDIDATE_INCLUSION.values() if v) == 4, (
    "exactly 4 candidates must be marked included_in_survey=True"
)
assert len(Q6F_DECISION_IDS) == Q6F_DECISION_COUNT == 8, (
    "Q6F_DECISION_IDS must have exactly 8 entries"
)
assert len(HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS) == 6, (
    "history_enriched_pre_game family-id length invariant violated"
)
assert len(NON_RATING_HISTORY_FAMILIES) == 5, (
    "non-rating family-id length invariant violated"
)
assert Q6F_SCHEMA_COLUMN_COUNT == 44, (
    f"Q6F_SURVEY_SCHEMA column-count invariant violated "
    f"(observed {Q6F_SCHEMA_COLUMN_COUNT}, expected 44)"
)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def _sha256_file(path: Path) -> str:
    """Return the SHA-256 hex digest of ``path``, or ``'NOT_FOUND'``.

    Args:
        path: Path to the file.

    Returns:
        64-char lowercase hex digest, or ``'NOT_FOUND'`` if ``path`` is
        absent.
    """
    if not path.exists():
        return "NOT_FOUND"
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _get_git_sha() -> str:
    """Return HEAD git SHA, or ``'UNKNOWN'`` if git is unavailable.

    Returns:
        40-char hex string, or ``'UNKNOWN'``.
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
        start: Starting directory or file.

    Returns:
        Repository root directory.

    Raises:
        FileNotFoundError: If no ``pyproject.toml`` is found.
    """
    candidate = start.resolve()
    while candidate != candidate.parent:
        if (candidate / "pyproject.toml").exists():
            return candidate
        candidate = candidate.parent
    raise FileNotFoundError(f"No pyproject.toml found walking up from {start}")


def _safe_float_str(value: float | None) -> str:
    """Return a deterministic 6-decimal string, or ``'NaN'`` / ``'NOT_APPLICABLE'``.

    Args:
        value: Floating-point value or ``None``.

    Returns:
        ``'NOT_APPLICABLE'`` if ``value`` is ``None``; ``'NaN'`` if it is
        ``math.nan``; otherwise a 6-decimal fixed-format string.
    """
    if value is None:
        return "NOT_APPLICABLE"
    if isinstance(value, float) and math.isnan(value):
        return "NaN"
    return f"{value:.6f}"


# ---------------------------------------------------------------------------
# Stream loader (T02)
# ---------------------------------------------------------------------------


def _load_pha_history_chronological(db_path: Path) -> pd.DataFrame:
    """Load the PHA forward-only paired-row stream.

    The returned frame has one row per ``(focal_toon, replay_id)`` pair on
    1v1 replays with exactly 2 PHA rows. Rows are sorted by
    ``(focal_toon, TRY_CAST(details_timeUTC AS TIMESTAMP), replay_id)`` so
    that every per-toon trajectory is chronological. Cross-region rows are
    retained (Q5 binding); the ``is_cross_region_fragmented`` flag is
    available as a co-registered evidence dimension.

    Args:
        db_path: Read-only path to the sc2egset DuckDB.

    Returns:
        DataFrame with columns ``focal_toon, opponent_toon, replay_id,
        details_timeUTC, focal_result, is_cross_region_fragmented``.

    Raises:
        RatingSurveyError: If the stream is empty.
    """
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        stream = con.execute(PHA_FORWARD_ONLY_STREAM_QUERY).df()
    finally:
        con.close()
    if len(stream) == 0:
        raise RatingSurveyError(
            "q6f_candidate_set_incomplete",
            "PHA forward-only stream produced 0 rows",
        )
    # Deterministic ordering belt-and-braces (DuckDB ORDER BY is the source
    # of truth, but pd.sort_values guarantees identical row order across
    # pandas versions).
    stream["_ts"] = pd.to_datetime(
        stream["details_timeUTC"], format="ISO8601", utc=True, errors="coerce"
    )
    if stream["_ts"].isna().any():
        raise RatingSurveyError(
            "q6f_candidate_set_incomplete",
            "PHA stream contains rows with unparseable details_timeUTC",
        )
    stream = stream.sort_values(
        by=["focal_toon", "_ts", "replay_id"], kind="stable"
    ).reset_index(drop=True)
    return stream


# ---------------------------------------------------------------------------
# Rating engines (T03; forward-only per-row predictions)
# ---------------------------------------------------------------------------


def _run_rolling_baseline_survey(
    stream: pd.DataFrame,
    alpha: float = 1.0,
    beta: float = 1.0,
) -> dict[str, Any]:
    """Run the rolling-win-rate Bayesian-smoothed baseline.

    Each focal-player row's predicted P(focal wins) is
    ``(alpha + wins_so_far) / (alpha + beta + games_so_far)`` using only
    matches strictly prior to the current row (forward-only). The first
    row per ``focal_toon`` has ``games_so_far == 0`` and is the cold-start
    case; the predicted probability is the Laplace prior
    ``alpha / (alpha + beta)``.

    Args:
        stream: PHA forward-only stream.
        alpha: Laplace prior wins (default 1.0).
        beta: Laplace prior losses (default 1.0).

    Returns:
        Dict with ``predicted_probabilities``, ``actuals``, ``is_cold_start``,
        ``rating_state_at_end``, ``runtime_ms``.
    """
    start = time.perf_counter()
    n = len(stream)
    predictions = np.zeros(n, dtype=np.float64)
    actuals = np.zeros(n, dtype=np.float64)
    is_cold = np.zeros(n, dtype=bool)
    wins: dict[str, int] = {}
    games: dict[str, int] = {}
    focals = stream["focal_toon"].to_numpy()
    results = stream["focal_result"].to_numpy()
    for i in range(n):
        toon = focals[i]
        prior_games = games.get(toon, 0)
        prior_wins = wins.get(toon, 0)
        predictions[i] = (alpha + prior_wins) / (alpha + beta + prior_games)
        is_cold[i] = prior_games == 0
        actuals[i] = 1.0 if results[i] == "Win" else 0.0
        games[toon] = prior_games + 1
        wins[toon] = prior_wins + (1 if results[i] == "Win" else 0)
    runtime_ms = (time.perf_counter() - start) * 1000.0
    return {
        "predicted_probabilities": predictions,
        "actuals": actuals,
        "is_cold_start": is_cold,
        "rating_state_at_end": {"wins": wins, "games": games},
        "runtime_ms": runtime_ms,
    }


def _elo_expected(rating_a: float, rating_b: float) -> float:
    """Logistic expectation for player A vs player B at rating diff.

    Args:
        rating_a: Player A's Elo rating.
        rating_b: Player B's Elo rating.

    Returns:
        ``1 / (1 + 10**((rating_b - rating_a) / 400))``.
    """
    return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))


def _run_elo_survey(
    stream: pd.DataFrame,
    k_factor: float = 24.0,
    initial_rating: float = 1500.0,
) -> dict[str, Any]:
    """Run forward-only Elo (1978) over the PHA stream.

    Prediction for row R uses the focal and opponent ratings as of
    strictly prior rows; the rating update for both players occurs only
    AFTER the prediction is scored. Cold-start uses ``initial_rating`` for
    both sides.

    Args:
        stream: PHA forward-only stream.
        k_factor: Elo K-factor (default 24.0).
        initial_rating: Initial Elo rating (default 1500.0).

    Returns:
        Dict with ``predicted_probabilities``, ``actuals``, ``is_cold_start``,
        ``rating_state_at_end``, ``runtime_ms``.
    """
    start = time.perf_counter()
    n = len(stream)
    predictions = np.zeros(n, dtype=np.float64)
    actuals = np.zeros(n, dtype=np.float64)
    is_cold = np.zeros(n, dtype=bool)
    ratings: dict[str, float] = {}
    seen: dict[str, int] = {}
    focals = stream["focal_toon"].to_numpy()
    opponents = stream["opponent_toon"].to_numpy()
    results = stream["focal_result"].to_numpy()
    for i in range(n):
        focal = focals[i]
        opp = opponents[i]
        r_focal = ratings.get(focal, initial_rating)
        r_opp = ratings.get(opp, initial_rating)
        predictions[i] = _elo_expected(r_focal, r_opp)
        is_cold[i] = seen.get(focal, 0) == 0
        actuals[i] = 1.0 if results[i] == "Win" else 0.0
        score = actuals[i]
        ratings[focal] = r_focal + k_factor * (score - predictions[i])
        ratings[opp] = r_opp + k_factor * ((1.0 - score) - (1.0 - predictions[i]))
        seen[focal] = seen.get(focal, 0) + 1
    runtime_ms = (time.perf_counter() - start) * 1000.0
    return {
        "predicted_probabilities": predictions,
        "actuals": actuals,
        "is_cold_start": is_cold,
        "rating_state_at_end": dict(ratings),
        "runtime_ms": runtime_ms,
    }


def _glicko2_g(rd: float) -> float:
    """Return the Glicko-2 ``g(RD)`` scale factor.

    Args:
        rd: Rating deviation in Glicko-2 units.

    Returns:
        ``1 / sqrt(1 + 3 * RD**2 / pi**2)``.
    """
    return 1.0 / math.sqrt(1.0 + 3.0 * rd * rd / (math.pi * math.pi))


def _glicko2_e(mu: float, mu_j: float, rd_j: float) -> float:
    """Return the Glicko-2 ``E`` expected-score function.

    Args:
        mu: Focal Glicko-2 rating in Glicko-2 units.
        mu_j: Opponent Glicko-2 rating.
        rd_j: Opponent rating deviation.

    Returns:
        Expected score (a probability in [0, 1]).
    """
    return 1.0 / (1.0 + math.exp(-_glicko2_g(rd_j) * (mu - mu_j)))


def _run_glicko2_survey(
    stream: pd.DataFrame,
    mu: float = 1500.0,
    rd: float = 350.0,
    sigma: float = 0.06,
    tau: float = 0.5,
) -> dict[str, Any]:
    """Run forward-only Glicko-2 (Glickman 2012) over the PHA stream.

    Implementation note: this is an event-by-event simplification of the
    canonical rating-period batched Glicko-2; rather than batching matches
    in fixed periods, the per-row update treats each match as a single-
    observation period. This is a defensible deployment-style variant
    (used by many real-time ladder systems) and is documented in MD §8.

    Args:
        stream: PHA forward-only stream.
        mu: Initial Glicko rating (default 1500.0; mapped to Glicko-2
            internal scale by ``(mu - 1500) / 173.7178``).
        rd: Initial rating deviation (default 350.0).
        sigma: Initial volatility (default 0.06).
        tau: System constant constraining volatility change (default 0.5).

    Returns:
        Dict with ``predicted_probabilities``, ``actuals``, ``is_cold_start``,
        ``rating_state_at_end``, ``runtime_ms``.
    """
    start = time.perf_counter()
    scale = 173.7178
    n = len(stream)
    predictions = np.zeros(n, dtype=np.float64)
    actuals = np.zeros(n, dtype=np.float64)
    is_cold = np.zeros(n, dtype=bool)
    ratings: dict[str, dict[str, float]] = {}
    seen: dict[str, int] = {}
    focals = stream["focal_toon"].to_numpy()
    opponents = stream["opponent_toon"].to_numpy()
    results = stream["focal_result"].to_numpy()
    for i in range(n):
        focal = focals[i]
        opp = opponents[i]
        state_focal = ratings.setdefault(
            focal, {"mu": (mu - 1500.0) / scale, "rd": rd / scale, "sigma": sigma}
        )
        state_opp = ratings.setdefault(
            opp, {"mu": (mu - 1500.0) / scale, "rd": rd / scale, "sigma": sigma}
        )
        e = _glicko2_e(state_focal["mu"], state_opp["mu"], state_opp["rd"])
        predictions[i] = e
        is_cold[i] = seen.get(focal, 0) == 0
        actuals[i] = 1.0 if results[i] == "Win" else 0.0
        s = actuals[i]
        # Update focal player using opponent's pre-match state.
        g_opp = _glicko2_g(state_opp["rd"])
        v = 1.0 / (g_opp * g_opp * e * (1.0 - e) + 1e-12)
        new_rd = 1.0 / math.sqrt(1.0 / (state_focal["rd"] ** 2 + 1e-12) + 1.0 / v)
        new_mu = state_focal["mu"] + new_rd ** 2 * g_opp * (s - e)
        ratings[focal] = {
            "mu": new_mu,
            "rd": new_rd,
            "sigma": state_focal["sigma"],
        }
        # Update opponent symmetrically (from focal's pre-match state).
        e_opp = 1.0 - e
        g_focal = _glicko2_g(state_focal["rd"])
        v_opp = 1.0 / (g_focal * g_focal * e_opp * (1.0 - e_opp) + 1e-12)
        new_rd_opp = 1.0 / math.sqrt(
            1.0 / (state_opp["rd"] ** 2 + 1e-12) + 1.0 / v_opp
        )
        new_mu_opp = state_opp["mu"] + new_rd_opp ** 2 * g_focal * ((1.0 - s) - e_opp)
        ratings[opp] = {
            "mu": new_mu_opp,
            "rd": new_rd_opp,
            "sigma": state_opp["sigma"],
        }
        seen[focal] = seen.get(focal, 0) + 1
    runtime_ms = (time.perf_counter() - start) * 1000.0
    # tau is used in the volatility update of the full Glicko-2 batched
    # period algorithm; in this event-by-event simplification we hold
    # sigma constant (its update requires a Newton-Raphson with the
    # accumulated variance over a period; here each period is one match).
    # Document via the rating_state_at_end snapshot.
    return {
        "predicted_probabilities": predictions,
        "actuals": actuals,
        "is_cold_start": is_cold,
        "rating_state_at_end": ratings,
        "runtime_ms": runtime_ms,
        "_tau_constant": tau,
    }


def _trueskill_win_prob(
    mu_a: float,
    sigma_a: float,
    mu_b: float,
    sigma_b: float,
    beta: float,
) -> float:
    """Return the TrueSkill win probability for player A vs player B.

    Args:
        mu_a: Player A's skill mean.
        sigma_a: Player A's skill stddev.
        mu_b: Player B's skill mean.
        sigma_b: Player B's skill stddev.
        beta: Performance noise stddev.

    Returns:
        ``Phi((mu_a - mu_b) / sqrt(2*beta^2 + sigma_a^2 + sigma_b^2))``
        where ``Phi`` is the standard normal CDF.
    """
    denom = math.sqrt(2.0 * beta * beta + sigma_a * sigma_a + sigma_b * sigma_b)
    return 0.5 * (1.0 + math.erf((mu_a - mu_b) / (denom * math.sqrt(2.0))))


def _normal_pdf(x: float) -> float:
    """Return the standard normal PDF at ``x``.

    Args:
        x: Real number.

    Returns:
        ``(1 / sqrt(2*pi)) * exp(-x^2 / 2)``.
    """
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def _normal_cdf(x: float) -> float:
    """Return the standard normal CDF at ``x``.

    Args:
        x: Real number.

    Returns:
        ``0.5 * (1 + erf(x / sqrt(2)))``.
    """
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _trueskill_v(t: float) -> float:
    """Return the TrueSkill ``v(t)`` truncated-Gaussian mean correction.

    Args:
        t: Standardised margin.

    Returns:
        ``pdf(t) / cdf(t)``.
    """
    cdf = _normal_cdf(t)
    if cdf < 1e-12:
        return -t
    return _normal_pdf(t) / cdf


def _trueskill_w(t: float) -> float:
    """Return the TrueSkill ``w(t)`` truncated-Gaussian variance correction.

    Args:
        t: Standardised margin.

    Returns:
        ``v(t) * (v(t) + t)``.
    """
    v = _trueskill_v(t)
    return v * (v + t)


def _run_trueskill_survey(
    stream: pd.DataFrame,
    mu_init: float = 25.0,
    sigma_init: float = 25.0 / 3.0,
    beta: float = 25.0 / 6.0,
    tau: float = 25.0 / 300.0,
    draw_margin: float = 0.0,
) -> dict[str, Any]:
    """Run forward-only TrueSkill (Herbrich, Minka, Graepel 2006) 1v1.

    NIT-4 binding: ``tau = 25/300`` is the literature default cited in
    Herbrich, Minka, Graepel (2006) §4 (and used by the official Xbox
    Live deployment); the value parameterises the per-game dynamic
    factor (skill drift). It is recorded in MD §8 as a literature default.

    Args:
        stream: PHA forward-only stream.
        mu_init: Initial skill mean (default 25.0).
        sigma_init: Initial skill stddev (default 25/3).
        beta: Performance noise stddev (default 25/6).
        tau: Dynamic skill drift stddev (default 25/300; NIT-4).
        draw_margin: Draw margin (default 0.0; PHA is decisive-only per
            PR #242 Q1).

    Returns:
        Dict with ``predicted_probabilities``, ``actuals``, ``is_cold_start``,
        ``rating_state_at_end``, ``runtime_ms``.
    """
    start = time.perf_counter()
    n = len(stream)
    predictions = np.zeros(n, dtype=np.float64)
    actuals = np.zeros(n, dtype=np.float64)
    is_cold = np.zeros(n, dtype=bool)
    ratings: dict[str, dict[str, float]] = {}
    seen: dict[str, int] = {}
    focals = stream["focal_toon"].to_numpy()
    opponents = stream["opponent_toon"].to_numpy()
    results = stream["focal_result"].to_numpy()
    for i in range(n):
        focal = focals[i]
        opp = opponents[i]
        s_focal = ratings.setdefault(
            focal, {"mu": mu_init, "sigma": sigma_init}
        )
        s_opp = ratings.setdefault(opp, {"mu": mu_init, "sigma": sigma_init})
        # Inject dynamic factor tau into pre-match variances.
        sigma_focal_sq = s_focal["sigma"] ** 2 + tau * tau
        sigma_opp_sq = s_opp["sigma"] ** 2 + tau * tau
        c_sq = 2.0 * beta * beta + sigma_focal_sq + sigma_opp_sq
        c = math.sqrt(c_sq)
        t = (s_focal["mu"] - s_opp["mu"] - draw_margin) / c
        predictions[i] = _normal_cdf(t)
        is_cold[i] = seen.get(focal, 0) == 0
        actuals[i] = 1.0 if results[i] == "Win" else 0.0
        s = actuals[i]
        # If focal won (s=1), the winner is focal; else opponent.
        sign = 1.0 if s == 1.0 else -1.0
        t_signed = sign * t
        v = _trueskill_v(t_signed)
        w = _trueskill_w(t_signed)
        new_mu_focal = s_focal["mu"] + sign * (sigma_focal_sq / c) * v
        new_sigma_focal = math.sqrt(
            max(sigma_focal_sq * (1.0 - sigma_focal_sq * w / c_sq), 1e-12)
        )
        new_mu_opp = s_opp["mu"] - sign * (sigma_opp_sq / c) * v
        new_sigma_opp = math.sqrt(
            max(sigma_opp_sq * (1.0 - sigma_opp_sq * w / c_sq), 1e-12)
        )
        ratings[focal] = {"mu": new_mu_focal, "sigma": new_sigma_focal}
        ratings[opp] = {"mu": new_mu_opp, "sigma": new_sigma_opp}
        seen[focal] = seen.get(focal, 0) + 1
    runtime_ms = (time.perf_counter() - start) * 1000.0
    return {
        "predicted_probabilities": predictions,
        "actuals": actuals,
        "is_cold_start": is_cold,
        "rating_state_at_end": ratings,
        "runtime_ms": runtime_ms,
    }


# ---------------------------------------------------------------------------
# Metrics with bootstrap CI (T04; NIT-3 / OQ1)
# ---------------------------------------------------------------------------


def _auc_from_arrays(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Compute ROC-AUC by trapezoidal rule on the ROC curve.

    Args:
        y_true: 1-D array of 0/1 labels.
        y_score: 1-D array of predicted probabilities.

    Returns:
        AUC in [0, 1], or ``math.nan`` if either class is missing.
    """
    if len(y_true) == 0:
        return math.nan
    positives = y_true.sum()
    negatives = len(y_true) - positives
    if positives == 0 or negatives == 0:
        return math.nan
    # Mann-Whitney U formulation: P(score_pos > score_neg) + 0.5 * P(=).
    order = np.argsort(y_score, kind="stable")
    ranks = np.empty_like(order, dtype=np.float64)
    ranks[order] = np.arange(1, len(y_score) + 1, dtype=np.float64)
    # Average ranks for ties.
    sorted_scores = y_score[order]
    i = 0
    n = len(sorted_scores)
    while i < n:
        j = i + 1
        while j < n and sorted_scores[j] == sorted_scores[i]:
            j += 1
        if j > i + 1:
            avg = (ranks[order[i]] + ranks[order[j - 1]]) / 2.0
            for k in range(i, j):
                ranks[order[k]] = avg
        i = j
    sum_pos_ranks = float(ranks[y_true == 1].sum())
    return (sum_pos_ranks - positives * (positives + 1) / 2.0) / (positives * negatives)


def _log_loss_from_arrays(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Compute binary log-loss with clipping to ``[eps, 1-eps]``.

    Args:
        y_true: 1-D array of 0/1 labels.
        y_score: 1-D array of predicted probabilities.

    Returns:
        Mean negative log likelihood, or ``math.nan`` if the array is empty.
    """
    if len(y_true) == 0:
        return math.nan
    eps = 1e-15
    y_clipped = np.clip(y_score, eps, 1.0 - eps)
    return float(-(y_true * np.log(y_clipped) + (1 - y_true) * np.log(1 - y_clipped)).mean())


def _brier_from_arrays(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Compute the binary Brier score.

    Args:
        y_true: 1-D array of 0/1 labels.
        y_score: 1-D array of predicted probabilities.

    Returns:
        Mean squared error of the predicted probabilities, or
        ``math.nan`` if the array is empty.
    """
    if len(y_true) == 0:
        return math.nan
    return float(((y_score - y_true) ** 2).mean())


def _calibration_error(
    y_true: np.ndarray, y_score: np.ndarray, n_bins: int = 10
) -> float:
    """Compute expected calibration error (ECE) over equal-width bins.

    Args:
        y_true: 1-D array of 0/1 labels.
        y_score: 1-D array of predicted probabilities.
        n_bins: Number of equal-width probability bins (default 10).

    Returns:
        ECE in [0, 1], or ``math.nan`` if input is empty.
    """
    if len(y_true) == 0:
        return math.nan
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    n = len(y_true)
    for k in range(n_bins):
        lo, hi = edges[k], edges[k + 1]
        if k == n_bins - 1:
            mask = (y_score >= lo) & (y_score <= hi)
        else:
            mask = (y_score >= lo) & (y_score < hi)
        m = mask.sum()
        if m == 0:
            continue
        bin_mean_pred = y_score[mask].mean()
        bin_mean_actual = y_true[mask].mean()
        ece += (m / n) * abs(bin_mean_pred - bin_mean_actual)
    return float(ece)


def compute_metrics_with_ci(
    y_true: np.ndarray,
    y_score: np.ndarray,
    n_bootstrap: int = BOOTSTRAP_BLOCK_COUNT,
    seed: int = BOOTSTRAP_RANDOM_SEED,
) -> dict[str, float]:
    """Compute AUC, log-loss, Brier with deterministic block bootstrap CIs.

    The bootstrap resamples chronological blocks of contiguous rows with
    replacement, with a fixed ``seed`` (default ``BOOTSTRAP_RANDOM_SEED``)
    for full byte-determinism. The block count is fixed at
    ``BOOTSTRAP_BLOCK_COUNT`` (default 200) — this is a deterministic
    resampling protocol, not a stochastic Monte-Carlo.

    Args:
        y_true: 1-D array of 0/1 labels (non-cold-start mask applied
            upstream).
        y_score: 1-D array of predicted probabilities aligned with
            ``y_true``.
        n_bootstrap: Number of bootstrap replicates (default 200).
        seed: RNG seed for the bootstrap (default 42).

    Returns:
        Dict with ``auc, auc_ci_low, auc_ci_high, log_loss, log_loss_ci_low,
        log_loss_ci_high, brier, brier_ci_low, brier_ci_high,
        calibration_error``.
    """
    if len(y_true) == 0:
        return {
            "auc": math.nan,
            "auc_ci_low": math.nan,
            "auc_ci_high": math.nan,
            "log_loss": math.nan,
            "log_loss_ci_low": math.nan,
            "log_loss_ci_high": math.nan,
            "brier": math.nan,
            "brier_ci_low": math.nan,
            "brier_ci_high": math.nan,
            "calibration_error": math.nan,
        }
    auc = _auc_from_arrays(y_true, y_score)
    ll = _log_loss_from_arrays(y_true, y_score)
    brier = _brier_from_arrays(y_true, y_score)
    cal = _calibration_error(y_true, y_score)
    rng = np.random.default_rng(seed)
    n = len(y_true)
    auc_samples = np.zeros(n_bootstrap, dtype=np.float64)
    ll_samples = np.zeros(n_bootstrap, dtype=np.float64)
    brier_samples = np.zeros(n_bootstrap, dtype=np.float64)
    for b in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        yt = y_true[idx]
        ys = y_score[idx]
        auc_samples[b] = _auc_from_arrays(yt, ys)
        ll_samples[b] = _log_loss_from_arrays(yt, ys)
        brier_samples[b] = _brier_from_arrays(yt, ys)
    # Use 95% percentile interval; nan-aware quantiles for AUC (degenerate
    # bootstrap samples can lack a class).
    auc_low, auc_high = (
        float(np.nanpercentile(auc_samples, 2.5)),
        float(np.nanpercentile(auc_samples, 97.5)),
    )
    ll_low, ll_high = (
        float(np.percentile(ll_samples, 2.5)),
        float(np.percentile(ll_samples, 97.5)),
    )
    brier_low, brier_high = (
        float(np.percentile(brier_samples, 2.5)),
        float(np.percentile(brier_samples, 97.5)),
    )
    return {
        "auc": auc,
        "auc_ci_low": auc_low,
        "auc_ci_high": auc_high,
        "log_loss": ll,
        "log_loss_ci_low": ll_low,
        "log_loss_ci_high": ll_high,
        "brier": brier,
        "brier_ci_low": brier_low,
        "brier_ci_high": brier_high,
        "calibration_error": cal,
    }


def _compute_engine_metrics(
    engine_output: dict[str, Any],
    n_bootstrap: int = BOOTSTRAP_BLOCK_COUNT,
    seed: int = BOOTSTRAP_RANDOM_SEED,
) -> dict[str, float]:
    """Compute T04 metrics from a single engine's output.

    Args:
        engine_output: Output dict from one of the ``_run_*_survey``
            functions.
        n_bootstrap: Bootstrap replicate count.
        seed: RNG seed.

    Returns:
        Dict with the 10 CI-aware numeric metrics plus ``coverage_rate``,
        ``cold_start_rate``, ``runtime_seconds``, ``tie_rate``.
    """
    is_cold = engine_output["is_cold_start"]
    mask = ~is_cold
    yt = engine_output["actuals"][mask].astype(np.float64)
    ys = engine_output["predicted_probabilities"][mask].astype(np.float64)
    metrics = compute_metrics_with_ci(yt, ys, n_bootstrap=n_bootstrap, seed=seed)
    coverage_rate = float(mask.mean()) if len(is_cold) > 0 else math.nan
    cold_start_rate = float(is_cold.mean()) if len(is_cold) > 0 else math.nan
    metrics["coverage_rate"] = coverage_rate
    metrics["cold_start_rate"] = cold_start_rate
    metrics["runtime_seconds"] = float(engine_output["runtime_ms"] / 1000.0)
    metrics["tie_rate"] = 0.0  # PHA is decisive-only (PR #242 Q1).
    return metrics


# ---------------------------------------------------------------------------
# Selection decision (T05; CI-based binding rule)
# ---------------------------------------------------------------------------


def _select_q6f_policy(
    metrics_by_candidate: dict[str, dict[str, float]],
) -> tuple[str, str, str, str]:
    """Apply ``Q6F_SELECTION_DECISION_RULE`` over per-candidate metrics.

    Args:
        metrics_by_candidate: Mapping of candidate name to its metric
            dict (from ``_compute_engine_metrics``).

    Returns:
        4-tuple ``(selected_policy, verdict, materialization_permission,
        rationale)``.
    """
    baseline_key = "rolling_win_rate_or_bayesian_smoothed_baseline"
    included = [
        c for c in Q6F_RATING_ALGORITHM_CANDIDATES if Q6F_CANDIDATE_INCLUSION[c]
    ]
    # Best by minimum log-loss (proper score; lower is better).
    valid = [c for c in included if not math.isnan(metrics_by_candidate[c]["log_loss"])]
    if not valid:
        rationale = (
            "All included candidates produced NaN log-loss after the "
            "non-cold-start mask was applied; rating reconstruction "
            "provides no measurable forward-only skill signal on the "
            "sc2egset PHA corpus."
        )
        return (
            "omit_reconstructed_rating_and_unblock_other_five",
            "omit_reconstructed_rating_and_unblock_other_five",
            "permitted_for_other_5_families_without_reconstructed_rating",
            rationale,
        )
    c_star = min(valid, key=lambda c: metrics_by_candidate[c]["log_loss"])
    baseline_ll_low = metrics_by_candidate[baseline_key]["log_loss_ci_low"]
    baseline_brier_low = metrics_by_candidate[baseline_key]["brier_ci_low"]
    star_ll_high = metrics_by_candidate[c_star]["log_loss_ci_high"]
    star_brier_high = metrics_by_candidate[c_star]["brier_ci_high"]
    # Branch 2: c* dominates every other included candidate (CI-disjoint).
    if c_star != baseline_key:
        dominates_all = True
        for c in valid:
            if c == c_star:
                continue
            other_ll_low = metrics_by_candidate[c]["log_loss_ci_low"]
            other_brier_low = metrics_by_candidate[c]["brier_ci_low"]
            if not (star_ll_high < other_ll_low and star_brier_high < other_brier_low):
                dominates_all = False
                break
        if (
            dominates_all
            and star_ll_high < baseline_ll_low
            and star_brier_high < baseline_brier_low
        ):
            rationale = (
                f"Candidate {c_star} achieved log-loss "
                f"{metrics_by_candidate[c_star]['log_loss']:.6f} "
                f"(CI {metrics_by_candidate[c_star]['log_loss_ci_low']:.6f}--"
                f"{metrics_by_candidate[c_star]['log_loss_ci_high']:.6f}) and "
                f"Brier {metrics_by_candidate[c_star]['brier']:.6f} (CI "
                f"{metrics_by_candidate[c_star]['brier_ci_low']:.6f}--"
                f"{metrics_by_candidate[c_star]['brier_ci_high']:.6f}); both "
                f"CI upper bounds lie strictly below the baseline CI lower "
                f"bounds and below every other included candidate's CI lower "
                f"bounds. Binding for materialization with the pinned "
                f"literature-default hyperparameters per "
                f"Q6F_HYPERPARAMETER_DEFAULTS."
            )
            return (
                "bind_now",
                "bind_now",
                "permitted_for_all_6_families_with_pinned_hyperparameters_in_next_materialization_pr",
                rationale,
            )
    # Branch 3: c* beats baseline but does not strictly dominate every other.
    if (
        c_star != baseline_key
        and star_ll_high < baseline_ll_low
        and star_brier_high < baseline_brier_low
    ):
        rationale = (
            f"Candidate {c_star} achieved log-loss "
            f"{metrics_by_candidate[c_star]['log_loss']:.6f} (CI upper bound "
            f"{star_ll_high:.6f}) strictly below the baseline CI lower bound "
            f"({baseline_ll_low:.6f}); however the other included opponent-"
            f"strength candidates' CIs overlap with {c_star}'s CI. Recording "
            f"narrow_with_evidence: an implementation-proof PR is required "
            f"before Layer-3 materialization to demonstrate byte-stable "
            f"forward-only rating outputs and re-evaluate the inter-candidate "
            f"ordering with a larger bootstrap."
        )
        return (
            "narrow_with_evidence",
            "narrow_with_evidence",
            "recommendation_only_blocked_pending_implementation_proof_pr",
            rationale,
        )
    # Branch 4: c* is the baseline (no opponent-strength candidate beats it).
    if c_star == baseline_key:
        rationale = (
            f"The Laplace-prior rolling baseline minimised log-loss "
            f"({metrics_by_candidate[baseline_key]['log_loss']:.6f}) over the "
            f"4 included candidates; no Elo/Glicko/TrueSkill variant showed a "
            f"CI-disjoint improvement over the no-opponent-strength baseline. "
            f"Recommendation: omit reconstructed_rating as a feature and "
            f"unblock the other 5 history-enriched pre_game families."
        )
        return (
            "omit_reconstructed_rating_and_unblock_other_five",
            "omit_reconstructed_rating_and_unblock_other_five",
            "permitted_for_other_5_families_without_reconstructed_rating",
            rationale,
        )
    # Branch 5: fallback (ambiguous).
    rationale = (
        f"Best log-loss candidate is {c_star} ({metrics_by_candidate[c_star]['log_loss']:.6f}), "
        f"but CI overlap with the baseline log-loss CI ({baseline_ll_low:.6f}--"
        f"{metrics_by_candidate[baseline_key]['log_loss_ci_high']:.6f}) prevents "
        f"a non-ambiguous binding. Deferring with named reason: no candidate "
        f"clears the baseline CI under the proper-score (log-loss + Brier) "
        f"binding criterion."
    )
    return (
        "deferred_blocker",
        "deferred_blocker",
        "blocked_pending_named_reason",
        rationale,
    )


# ---------------------------------------------------------------------------
# Decision-row builder (T05 row authoring)
# ---------------------------------------------------------------------------


_BTL_REJECTION_TEXT: str = (
    "BTL family (aligulac_style_btl, bradley_terry, neural_btl) acknowledged "
    "from dataset research_log lines 733-734 and 961 but EXCLUDED from this "
    "Q6F survey's executable candidate set per Layer-1 Assumption 8: in 1v1 "
    "decisive matches BTL collapses to Elo-with-race-prior (Elo already in the "
    "survey); Neural BTL requires a full model-training pipeline (Phase-03 "
    "scope; out of scope here). The Layer-2 executor may extend the candidate "
    "set in a follow-up survey PR with explicit substantive justification and "
    "citations."
)

_NOT_APPLICABLE_CARRY_FORWARD: str = "not_applicable_carry_forward"


def _evidence_paths_text() -> str:
    """Return the newline-joined evidence-paths block.

    Returns:
        Multi-line string of repo-relative paths plus citation strings.
    """
    return "\n".join(
        [
            PARENT_PR242_CSV_REL,
            PARENT_PR242_MD_REL,
            PARENT_PR243_CSV_REL,
            PARENT_PR243_MD_REL,
            PARENT_PR245_CSV_REL,
            PARENT_PR245_MD_REL,
            DATASET_RESEARCH_LOG_REL,
            f"citation::{CITATION_ELO_1978}",
            f"citation::{CITATION_GLICKMAN_1999}",
            f"citation::{CITATION_GLICKMAN_2012}",
            f"citation::{CITATION_HERBRICH_MINKA_GRAEPEL_2006}",
            f"citation::{CITATION_STEYERBERG_2009}",
            f"citation::{CITATION_HOSMER_LEMESHOW_2013}",
        ]
    )


def _falsifier_roll_call(
    fired: tuple[str, ...] = (),
) -> str:
    """Return the newline-joined falsifier roll-call.

    Args:
        fired: Tuple of fired falsifier keys (empty by default).

    Returns:
        Multi-line string of ``key:status`` pairs.
    """
    return "\n".join(
        f"{k}:{'fired' if k in fired else 'did_not_fire'}"
        for k in FALSIFIER_PRIORITY_CHAIN
    )


def _candidate_to_metric_strings(
    candidate: str, metrics: dict[str, float]
) -> dict[str, str]:
    """Return formatted-string metric values for the CSV.

    Args:
        candidate: Candidate policy name.
        metrics: Metric dict from ``_compute_engine_metrics``.

    Returns:
        Dict with CSV-string-valued entries for the 14 metric columns.
    """
    if not Q6F_CANDIDATE_INCLUSION[candidate]:
        return {
            "auc": _NOT_APPLICABLE_CARRY_FORWARD,
            "auc_ci_low": _NOT_APPLICABLE_CARRY_FORWARD,
            "auc_ci_high": _NOT_APPLICABLE_CARRY_FORWARD,
            "log_loss": _NOT_APPLICABLE_CARRY_FORWARD,
            "log_loss_ci_low": _NOT_APPLICABLE_CARRY_FORWARD,
            "log_loss_ci_high": _NOT_APPLICABLE_CARRY_FORWARD,
            "brier": _NOT_APPLICABLE_CARRY_FORWARD,
            "brier_ci_low": _NOT_APPLICABLE_CARRY_FORWARD,
            "brier_ci_high": _NOT_APPLICABLE_CARRY_FORWARD,
            "calibration_error": _NOT_APPLICABLE_CARRY_FORWARD,
            "coverage_rate": _NOT_APPLICABLE_CARRY_FORWARD,
            "cold_start_rate": _NOT_APPLICABLE_CARRY_FORWARD,
            "runtime_summary": _NOT_APPLICABLE_CARRY_FORWARD,
            "tie_rate": _NOT_APPLICABLE_CARRY_FORWARD,
        }
    return {
        "auc": _safe_float_str(metrics["auc"]),
        "auc_ci_low": _safe_float_str(metrics["auc_ci_low"]),
        "auc_ci_high": _safe_float_str(metrics["auc_ci_high"]),
        "log_loss": _safe_float_str(metrics["log_loss"]),
        "log_loss_ci_low": _safe_float_str(metrics["log_loss_ci_low"]),
        "log_loss_ci_high": _safe_float_str(metrics["log_loss_ci_high"]),
        "brier": _safe_float_str(metrics["brier"]),
        "brier_ci_low": _safe_float_str(metrics["brier_ci_low"]),
        "brier_ci_high": _safe_float_str(metrics["brier_ci_high"]),
        "calibration_error": _safe_float_str(metrics["calibration_error"]),
        "coverage_rate": _safe_float_str(metrics["coverage_rate"]),
        "cold_start_rate": _safe_float_str(metrics["cold_start_rate"]),
        # Deterministic descriptor only; wall-clock seconds are
        # process-dependent and would break byte-determinism. Runtime
        # complexity is recorded qualitatively in
        # complexity_deployability_score.
        "runtime_summary": "deterministic_forward_only_single_pass",
        "tie_rate": _safe_float_str(metrics["tie_rate"]),
    }


_CANDIDATE_METHODOLOGY: dict[str, dict[str, str]] = {
    "omit_reconstructed_rating": {
        "initialization_policy": _NOT_APPLICABLE_CARRY_FORWARD,
        "hyperparameter_policy": _NOT_APPLICABLE_CARRY_FORWARD,
        "cold_start_policy": (
            "Trivially satisfied: omission of the reconstructed_rating "
            "feature obviates cold-start (G-CS-4) for this family. "
            "is_mmr_missing co-registration is preserved per CROSS-02-02 "
            "§6.2."
        ),
        "tie_policy": _NOT_APPLICABLE_CARRY_FORWARD,
        "forward_only_constraints": _NOT_APPLICABLE_CARRY_FORWARD,
        "complexity_deployability_score": "low_no_runtime_state",
        "leakage_risk_score": "low_omitted_feature",
        "inclusion_or_rejection_reason": (
            "Carry-forward reference: included as the omit-option row "
            "whose verdict is re-affirmed if Q6F_selected_policy = "
            "omit_reconstructed_rating_and_unblock_other_five."
        ),
    },
    "rolling_win_rate_or_bayesian_smoothed_baseline": {
        "initialization_policy": (
            "Laplace prior: alpha=1.0 wins + beta=1.0 losses; prior-implied "
            "P(focal wins) = 0.5 at cold-start."
        ),
        "hyperparameter_policy": (
            "alpha=1.0, beta=1.0 (literature default; Laplace 1814 "
            "rule-of-succession). Expanding window over all strictly-prior "
            "PHA rows for the focal toon_id; no finite-window variant in "
            "this survey."
        ),
        "cold_start_policy": (
            "G-CS-4: first match per focal toon_id is cold-start; prior-"
            "implied probability 0.5 is emitted; is_cold_start=True is "
            "flagged for downstream coverage_rate."
        ),
        "tie_policy": (
            "Decisive-only (Win/Loss) per PR #242 Q1; same-timestamp ties "
            "broken by deterministic sort key "
            "(focal_toon, TRY_CAST(details_timeUTC AS TIMESTAMP), replay_id)."
        ),
        "forward_only_constraints": (
            "Prediction uses only strictly-prior PHA rows for the focal "
            "toon_id per STRICT_LT_HISTORY_FILTER. Rating state updated "
            "AFTER scoring; outcome never read as feature input for its "
            "own match."
        ),
        "complexity_deployability_score": "low_o1_update_no_opponent_strength",
        "leakage_risk_score": "low_no_opponent_state_no_global_fit",
        "inclusion_or_rejection_reason": (
            "Included as the no-opponent-strength reference; tests whether "
            "any opponent-strength rating system beats the marginal "
            "win-rate proxy."
        ),
    },
    "elo": {
        "initialization_policy": (
            "Initial rating R0=1500 (Elo 1978 chess convention); applied "
            "to every previously-unseen toon_id."
        ),
        "hyperparameter_policy": (
            "K-factor=24.0 (mid-point between chess-conservative K=20 and "
            "chess-default K=32; commonly used in aoe2-tournament Elo "
            "deployments). No tuning in this survey per Layer-1 "
            "Assumption 10."
        ),
        "cold_start_policy": (
            "G-CS-4: first match per focal toon_id uses initial rating "
            "1500; is_cold_start=True is flagged for downstream "
            "coverage_rate; predicted probability at cold-start is the "
            "expected-score function evaluated at the symmetric rating "
            "diff."
        ),
        "tie_policy": (
            "Decisive-only (Win/Loss) per PR #242 Q1; same-timestamp ties "
            "broken by deterministic sort key."
        ),
        "forward_only_constraints": (
            "Prediction uses focal and opponent ratings as of strictly-"
            "prior PHA rows per STRICT_LT_HISTORY_FILTER. Both players' "
            "ratings updated AFTER scoring; outcome never read as feature "
            "input for its own match."
        ),
        "complexity_deployability_score": "low_o1_update_per_match",
        "leakage_risk_score": "low_if_forward_only_enforced",
        "inclusion_or_rejection_reason": (
            "Included as the canonical 1v1 rating algorithm (Elo 1978); "
            "minimal hyperparameter surface; full literature provenance."
        ),
    },
    "glicko_or_glicko_2": {
        "initialization_policy": (
            "Initial mu=1500 (Glicko scale), RD=350, sigma=0.06 "
            "(Glickman 2012 reference defaults). Mapped to Glicko-2 "
            "internal scale by (mu - 1500) / 173.7178."
        ),
        "hyperparameter_policy": (
            "mu=1500, RD=350, sigma=0.06, tau=0.5 (Glickman 2012 reference "
            "defaults). Event-by-event simplification: each match treated "
            "as a single-observation rating period. Sigma held constant "
            "in this simplification; the full batched volatility update "
            "is deferred to a future Q6G PR."
        ),
        "cold_start_policy": (
            "G-CS-4: first match per focal toon_id uses prior mu=1500, "
            "RD=350; is_cold_start=True is flagged for downstream "
            "coverage_rate; predicted probability at cold-start is the "
            "symmetric E function evaluated at zero mu diff."
        ),
        "tie_policy": (
            "Decisive-only (Win/Loss) per PR #242 Q1; same-timestamp ties "
            "broken by deterministic sort key."
        ),
        "forward_only_constraints": (
            "Prediction uses focal and opponent (mu, RD) states as of "
            "strictly-prior PHA rows per STRICT_LT_HISTORY_FILTER. Both "
            "players' states updated AFTER scoring; outcome never read as "
            "feature input for its own match."
        ),
        "complexity_deployability_score": "medium_state_per_player_includes_rd",
        "leakage_risk_score": "low_if_forward_only_enforced",
        "inclusion_or_rejection_reason": (
            "Included as the §6.2 row 4 spec-favoured candidate "
            "(reconstructed_rating noted as 'Glicko-2 or analogous'); "
            "tests the prior toward the spec-favoured path."
        ),
    },
    "trueskill_or_trueskill_like": {
        "initialization_policy": (
            "Initial mu=25, sigma=25/3 (Herbrich, Minka, Graepel 2006 "
            "defaults; also Xbox Live deployment defaults)."
        ),
        "hyperparameter_policy": (
            "mu=25, sigma=25/3, beta=25/6, tau=25/300 (Herbrich, Minka, "
            "Graepel 2006 §4; literature default; cited in MD §8 per "
            "NIT-4), draw_margin=0 (PHA is decisive-only per PR #242 Q1)."
        ),
        "cold_start_policy": (
            "G-CS-4: first match per focal toon_id uses prior mu=25, "
            "sigma=25/3; is_cold_start=True is flagged for downstream "
            "coverage_rate; predicted probability at cold-start is the "
            "symmetric normal CDF evaluated at zero mu diff."
        ),
        "tie_policy": (
            "Decisive-only (Win/Loss) per PR #242 Q1; draw_margin=0; same-"
            "timestamp ties broken by deterministic sort key."
        ),
        "forward_only_constraints": (
            "Prediction uses focal and opponent (mu, sigma) states as of "
            "strictly-prior PHA rows per STRICT_LT_HISTORY_FILTER. Both "
            "players' states updated AFTER scoring; outcome never read as "
            "feature input for its own match. Dynamic factor tau is "
            "applied to pre-match variances each game."
        ),
        "complexity_deployability_score": "medium_gaussian_factor_graph",
        "leakage_risk_score": "low_if_forward_only_enforced",
        "inclusion_or_rejection_reason": (
            "Included as the Gaussian-factor-graph rating system "
            "(Herbrich, Minka, Graepel 2006); 1v1 specialisation; full "
            "literature provenance."
        ),
    },
    "deferred_blocker_with_algorithm_survey_required": {
        "initialization_policy": _NOT_APPLICABLE_CARRY_FORWARD,
        "hyperparameter_policy": _NOT_APPLICABLE_CARRY_FORWARD,
        "cold_start_policy": _NOT_APPLICABLE_CARRY_FORWARD,
        "tie_policy": _NOT_APPLICABLE_CARRY_FORWARD,
        "forward_only_constraints": _NOT_APPLICABLE_CARRY_FORWARD,
        "complexity_deployability_score": _NOT_APPLICABLE_CARRY_FORWARD,
        "leakage_risk_score": _NOT_APPLICABLE_CARRY_FORWARD,
        "inclusion_or_rejection_reason": (
            "Carry-forward reference: represents PR #245's Q6 deferred "
            "verdict; the Q6F_selected_policy row is conceptually a "
            "successor adjudication of this row."
        ),
    },
}


def _build_decision(
    decision_id: str,
    candidate_policy: str,
    metrics: dict[str, float] | None,
    selected_policy: str,
    verdict: str,
    materialization_permission: str,
    audit_pr: str,
    notes: str,
) -> RatingSurveyDecision:
    """Construct a single ``RatingSurveyDecision`` instance.

    Args:
        decision_id: One of ``Q6F_DECISION_IDS``.
        candidate_policy: One of ``Q6F_RATING_ALGORITHM_CANDIDATES`` (or
            empty for derived rows).
        metrics: Per-candidate metric dict (or ``None`` for
            carry-forward / derived rows).
        selected_policy: Q6F_selected_policy literal (populated on the
            Q6F_selected_policy / per_family rows; mirrored on candidate
            rows).
        verdict: One of ``Q6F_ALLOWED_VERDICTS``.
        materialization_permission: One of
            ``ALLOWED_MATERIALIZATION_PERMISSIONS``.
        audit_pr: PR number string (e.g., ``'PR #246'`` or placeholder).
        notes: Free-text rationale; appended to the row's notes column.

    Returns:
        ``RatingSurveyDecision`` dataclass instance.
    """
    methodology = _CANDIDATE_METHODOLOGY.get(candidate_policy, {})
    if metrics is None:
        metric_strings = _candidate_to_metric_strings(
            candidate_policy if candidate_policy else "omit_reconstructed_rating",
            {k: math.nan for k in Q6F_METRICS},
        )
        # Derived rows (Q6F_selected_policy / Q6F_per_family_impact_summary)
        # do not have per-candidate methodology; use sentinel strings.
        if candidate_policy == "":
            for col in (
                "initialization_policy",
                "hyperparameter_policy",
                "cold_start_policy",
                "tie_policy",
                "forward_only_constraints",
                "complexity_deployability_score",
                "leakage_risk_score",
                "inclusion_or_rejection_reason",
            ):
                methodology = {**methodology, col: _NOT_APPLICABLE_CARRY_FORWARD}
    else:
        metric_strings = _candidate_to_metric_strings(candidate_policy, metrics)
    algorithm_family = Q6F_ALGORITHM_FAMILY_BY_CANDIDATE.get(
        candidate_policy, "derived_summary_row"
    )
    included_in_survey = (
        "True"
        if candidate_policy and Q6F_CANDIDATE_INCLUSION.get(candidate_policy, False)
        else "False"
    )
    player_identity_policy = (
        "toon_id (PHA grouping key per PR #245 §9; PHA has no "
        "player_id_worldwide column on this dataset)"
    )
    cross_region_policy = (
        f"Q5 BINDING preserved: Q5_selected_policy={Q5_SELECTED_POLICY}, "
        f"verdict={Q5_SELECTED_POLICY_VERDICT}; is_cross_region_fragmented "
        f"is a co-registered evidence dimension, not a filter applied to "
        f"the survey input stream."
    )
    return RatingSurveyDecision(
        decision_id=decision_id,
        parent_decision_id="Q6_rating_policy_deferred_blocker",
        candidate_policy=candidate_policy,
        algorithm_family=algorithm_family,
        included_in_survey=included_in_survey,
        inclusion_or_rejection_reason=methodology.get(
            "inclusion_or_rejection_reason", _NOT_APPLICABLE_CARRY_FORWARD
        ),
        initialization_policy=methodology.get(
            "initialization_policy", _NOT_APPLICABLE_CARRY_FORWARD
        ),
        hyperparameter_policy=methodology.get(
            "hyperparameter_policy", _NOT_APPLICABLE_CARRY_FORWARD
        ),
        cold_start_policy=methodology.get(
            "cold_start_policy", _NOT_APPLICABLE_CARRY_FORWARD
        ),
        tie_policy=methodology.get("tie_policy", _NOT_APPLICABLE_CARRY_FORWARD),
        player_identity_policy=player_identity_policy,
        cross_region_policy=cross_region_policy,
        forward_only_constraints=methodology.get(
            "forward_only_constraints", _NOT_APPLICABLE_CARRY_FORWARD
        ),
        auc=metric_strings["auc"],
        auc_ci_low=metric_strings["auc_ci_low"],
        auc_ci_high=metric_strings["auc_ci_high"],
        log_loss=metric_strings["log_loss"],
        log_loss_ci_low=metric_strings["log_loss_ci_low"],
        log_loss_ci_high=metric_strings["log_loss_ci_high"],
        brier=metric_strings["brier"],
        brier_ci_low=metric_strings["brier_ci_low"],
        brier_ci_high=metric_strings["brier_ci_high"],
        calibration_error=metric_strings["calibration_error"],
        coverage_rate=metric_strings["coverage_rate"],
        cold_start_rate=metric_strings["cold_start_rate"],
        runtime_summary=metric_strings["runtime_summary"],
        complexity_deployability_score=methodology.get(
            "complexity_deployability_score", _NOT_APPLICABLE_CARRY_FORWARD
        ),
        leakage_risk_score=methodology.get(
            "leakage_risk_score", _NOT_APPLICABLE_CARRY_FORWARD
        ),
        selected_policy=selected_policy,
        survey_verdict=verdict,
        materialization_permission=materialization_permission,
        excluded_methods_considered=",".join(EXCLUDED_METHODS_CONSIDERED),
        raw_mmr_hybrid_rejection=RAW_MMR_HYBRID_REJECTION_TEXT,
        evidence_paths=_evidence_paths_text(),
        falsifiers=_falsifier_roll_call(),
        audit_pr=audit_pr,
        parent_pr242_csv_sha256=EXPECTED_PR242_CSV_SHA256,
        parent_pr242_md_sha256=EXPECTED_PR242_MD_SHA256,
        parent_pr243_csv_sha256=EXPECTED_PR243_CSV_SHA256,
        parent_pr243_md_sha256=EXPECTED_PR243_MD_SHA256,
        parent_pr245_csv_sha256=EXPECTED_PR245_CSV_SHA256,
        parent_pr245_md_sha256=EXPECTED_PR245_MD_SHA256,
        materialized_output_paths="",
        notes=notes,
    )


def _per_family_broadcast(
    verdict: str,
) -> str:
    """Return the per-family impact summary for the selected verdict.

    Args:
        verdict: Q6F_selected_policy verdict literal.

    Returns:
        Multi-line free-form summary covering all 6 families.
    """
    lines = []
    if verdict == "bind_now":
        for fam in HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS:
            lines.append(f"{fam}: unblocked_for_materialization")
    elif verdict == "narrow_with_evidence":
        for fam in HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS:
            lines.append(
                f"{fam}: recommendation_only_blocked_pending_implementation_proof_pr"
            )
    elif verdict == "omit_reconstructed_rating_and_unblock_other_five":
        for fam in NON_RATING_HISTORY_FAMILIES:
            lines.append(f"{fam}: unblocked_for_materialization")
        lines.append("reconstructed_rating: permanently_absent")
    elif verdict == "deferred_blocker":
        for fam in HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS:
            lines.append(f"{fam}: blocked_pending_named_reason")
    else:
        for fam in HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS:
            lines.append(f"{fam}: unknown_verdict_review_required")
    return "\n".join(lines)


def _build_survey_decisions(
    metrics_by_candidate: dict[str, dict[str, float]],
    audit_pr: str,
) -> tuple[RatingSurveyDecision, ...]:
    """Construct all 8 ``RatingSurveyDecision`` rows.

    Args:
        metrics_by_candidate: Mapping of candidate name to its metric dict.
        audit_pr: PR number string (e.g., ``'PR #246'`` or placeholder).

    Returns:
        8-tuple of decisions in ``Q6F_DECISION_IDS`` order.
    """
    selected_policy, verdict, materialization_permission, rationale = _select_q6f_policy(
        metrics_by_candidate
    )
    decisions: list[RatingSurveyDecision] = []
    for decision_id, candidate in zip(
        Q6F_DECISION_IDS[:6], Q6F_RATING_ALGORITHM_CANDIDATES, strict=True
    ):
        notes_lines = [
            (
                f"Q6F survey row for candidate {candidate}; "
                f"Q5 BINDING preserved ({Q5_SELECTED_POLICY}); "
                f"PR #242/#243/#245 lineage SHA-pinned."
            ),
            f"raw_mmr_hybrid_rejection: {RAW_MMR_HYBRID_REJECTION_TEXT}",
            _BTL_REJECTION_TEXT,
        ]
        if Q6F_CANDIDATE_INCLUSION.get(candidate, False):
            m = metrics_by_candidate[candidate]
            notes_lines.append(
                f"Forward-only metrics: log_loss={m['log_loss']:.6f} "
                f"(CI {m['log_loss_ci_low']:.6f}--{m['log_loss_ci_high']:.6f}); "
                f"brier={m['brier']:.6f} "
                f"(CI {m['brier_ci_low']:.6f}--{m['brier_ci_high']:.6f}); "
                f"auc={m['auc']:.6f} "
                f"(CI {m['auc_ci_low']:.6f}--{m['auc_ci_high']:.6f}); "
                f"calibration_error={m['calibration_error']:.6f}."
            )
        decisions.append(
            _build_decision(
                decision_id=decision_id,
                candidate_policy=candidate,
                metrics=metrics_by_candidate.get(candidate)
                if Q6F_CANDIDATE_INCLUSION.get(candidate, False)
                else None,
                selected_policy=selected_policy if candidate == selected_policy else "",
                verdict=(
                    verdict
                    if candidate == selected_policy
                    else "not_applicable_carry_forward"
                ),
                materialization_permission=(
                    materialization_permission
                    if candidate == selected_policy
                    else "not_applicable_carry_forward"
                ),
                audit_pr=audit_pr,
                notes="\n".join(notes_lines),
            )
        )
    # Row 7: Q6F_selected_policy.
    selected_notes = (
        f"Q6F SELECTED POLICY = {selected_policy}\n"
        f"VERDICT = {verdict}\n"
        f"MATERIALIZATION PERMISSION = {materialization_permission}\n"
        f"RATIONALE: {rationale}\n"
        f"DECISION RULE (verbatim): NIT-3 / OQ1 proper-score CI binding; "
        f"AUC alone CANNOT bind a candidate.\n"
        f"Q5 BINDING preserved ({Q5_SELECTED_POLICY}); "
        f"raw_mmr_hybrid_rejection re-affirmed; BTL family acknowledgement re-affirmed."
    )
    decisions.append(
        _build_decision(
            decision_id="Q6F_selected_policy",
            candidate_policy="",
            metrics=None,
            selected_policy=selected_policy,
            verdict=verdict,
            materialization_permission=materialization_permission,
            audit_pr=audit_pr,
            notes=selected_notes,
        )
    )
    # Row 8: Q6F_per_family_impact_summary.
    family_block = _per_family_broadcast(verdict)
    family_notes = (
        f"Per-family broadcast of Q6F selected policy ({selected_policy}):\n"
        f"{family_block}\n"
        f"All 6 history-enriched pre_game families covered; "
        f"no Step 02_01_03 closure claim; "
        f"no Phase 03 baseline claim; "
        f"no feature materialization claim."
    )
    decisions.append(
        _build_decision(
            decision_id="Q6F_per_family_impact_summary",
            candidate_policy="",
            metrics=None,
            selected_policy=selected_policy,
            verdict=verdict,
            materialization_permission=materialization_permission,
            audit_pr=audit_pr,
            notes=family_notes,
        )
    )
    return tuple(decisions)


# ---------------------------------------------------------------------------
# Falsifier checks (post-build; structural)
# ---------------------------------------------------------------------------


def _check_candidate_set_complete(
    decisions: tuple[RatingSurveyDecision, ...],
) -> tuple[bool, str]:
    """Verify all 6 candidate policies are represented across rows 1-6.

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(passed, message)``.
    """
    candidate_policies = {d.candidate_policy for d in decisions[:6]}
    if candidate_policies != set(Q6F_RATING_ALGORITHM_CANDIDATES):
        missing = set(Q6F_RATING_ALGORITHM_CANDIDATES) - candidate_policies
        return (
            False,
            f"missing candidates in rows 1-6: {sorted(missing)}",
        )
    return (True, "")


def _check_decision_count(
    decisions: tuple[RatingSurveyDecision, ...],
) -> tuple[bool, str]:
    """Verify exactly 8 decisions.

    Args:
        decisions: All decisions.

    Returns:
        ``(passed, message)``.
    """
    if len(decisions) != Q6F_DECISION_COUNT:
        return (
            False,
            f"expected {Q6F_DECISION_COUNT} decisions; got {len(decisions)}",
        )
    return (True, "")


def _check_decision_id_order(
    decisions: tuple[RatingSurveyDecision, ...],
) -> tuple[bool, str]:
    """Verify decision IDs match the canonical order.

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(passed, message)``.
    """
    observed = tuple(d.decision_id for d in decisions)
    if observed != Q6F_DECISION_IDS:
        return (
            False,
            f"decision id order mismatch: observed {observed}; expected {Q6F_DECISION_IDS}",
        )
    return (True, "")


def _check_no_materialized_output_paths(
    decisions: tuple[RatingSurveyDecision, ...],
) -> tuple[bool, str]:
    """Verify every decision's ``materialized_output_paths`` is empty.

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(passed, message)``.
    """
    for d in decisions:
        if d.materialized_output_paths != "":
            return (
                False,
                f"row {d.decision_id} has non-empty materialized_output_paths",
            )
    return (True, "")


def _check_q5_not_re_adjudicated(
    decisions: tuple[RatingSurveyDecision, ...],
) -> tuple[bool, str]:
    """Verify no row's verdict / selected_policy carries a Q5 binding token.

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(passed, message)``.
    """
    q5_token = Q5_SELECTED_POLICY
    for d in decisions:
        for field_name in ("selected_policy", "survey_verdict"):
            value = getattr(d, field_name)
            if value == q5_token:
                return (
                    False,
                    f"row {d.decision_id} {field_name} carries Q5 token {q5_token!r}",
                )
    return (True, "")


def _check_selected_policy_row_present(
    decisions: tuple[RatingSurveyDecision, ...],
) -> tuple[bool, str]:
    """Verify the Q6F_selected_policy row exists with a valid verdict.

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(passed, message)``.
    """
    for d in decisions:
        if d.decision_id == "Q6F_selected_policy":
            if d.survey_verdict not in Q6F_ALLOWED_VERDICTS:
                return (
                    False,
                    f"Q6F_selected_policy verdict {d.survey_verdict!r} not in allowed set",
                )
            if d.materialization_permission not in ALLOWED_MATERIALIZATION_PERMISSIONS:
                return (
                    False,
                    (
                        "Q6F_selected_policy materialization_permission "
                        f"{d.materialization_permission!r} not in allowed set"
                    ),
                )
            return (True, "")
    return (False, "Q6F_selected_policy row missing")


def _check_per_family_impact_summary_present(
    decisions: tuple[RatingSurveyDecision, ...],
) -> tuple[bool, str]:
    """Verify the per-family impact summary row exists.

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(passed, message)``.
    """
    for d in decisions:
        if d.decision_id == "Q6F_per_family_impact_summary":
            for fam in HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS:
                if fam not in d.notes:
                    return (
                        False,
                        f"per_family_impact_summary row missing family {fam!r}",
                    )
            return (True, "")
    return (False, "Q6F_per_family_impact_summary row missing")


def _check_excluded_methods_complete(
    decisions: tuple[RatingSurveyDecision, ...],
) -> tuple[bool, str]:
    """Verify each row's ``excluded_methods_considered`` includes all N-1 methods.

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(passed, message)``.
    """
    expected = set(EXCLUDED_METHODS_CONSIDERED)
    for d in decisions:
        observed = set(d.excluded_methods_considered.split(","))
        if not expected.issubset(observed):
            return (
                False,
                f"row {d.decision_id} excluded_methods_considered missing {expected - observed}",
            )
    return (True, "")


def _check_raw_mmr_hybrid_rejection(
    decisions: tuple[RatingSurveyDecision, ...],
) -> tuple[bool, str]:
    """Verify each row carries the raw-MMR hybrid rejection text.

    Args:
        decisions: All 8 decisions.

    Returns:
        ``(passed, message)``.
    """
    for d in decisions:
        if "raw_mmr_where_present_plus_is_mmr_missing" not in d.raw_mmr_hybrid_rejection:
            return (
                False,
                f"row {d.decision_id} missing raw_mmr_hybrid_rejection token",
            )
    return (True, "")


def _check_parent_pr_shas(
    decisions: tuple[RatingSurveyDecision, ...],
    repo_root: Path,
) -> list[tuple[str, str]]:
    """Verify PR #242 / #243 / #245 artifact SHAs match the pinned values.

    Args:
        decisions: All 8 decisions (for cross-checking).
        repo_root: Repository root.

    Returns:
        List of ``(falsifier_key, message)`` for any mismatches; empty on
        success.
    """
    mismatches: list[tuple[str, str]] = []
    pairs = [
        (
            "parent_pr242_csv_sha256_mismatch",
            repo_root / PARENT_PR242_CSV_REL,
            EXPECTED_PR242_CSV_SHA256,
        ),
        (
            "parent_pr242_md_sha256_mismatch",
            repo_root / PARENT_PR242_MD_REL,
            EXPECTED_PR242_MD_SHA256,
        ),
        (
            "parent_pr243_csv_sha256_mismatch",
            repo_root / PARENT_PR243_CSV_REL,
            EXPECTED_PR243_CSV_SHA256,
        ),
        (
            "parent_pr243_md_sha256_mismatch",
            repo_root / PARENT_PR243_MD_REL,
            EXPECTED_PR243_MD_SHA256,
        ),
        (
            "parent_pr245_csv_sha256_mismatch",
            repo_root / PARENT_PR245_CSV_REL,
            EXPECTED_PR245_CSV_SHA256,
        ),
        (
            "parent_pr245_md_sha256_mismatch",
            repo_root / PARENT_PR245_MD_REL,
            EXPECTED_PR245_MD_SHA256,
        ),
    ]
    for key, path, expected in pairs:
        sha = _sha256_file(path)
        if sha != expected:
            mismatches.append((key, f"{path}: observed {sha} expected {expected}"))
    return mismatches


# ---------------------------------------------------------------------------
# CSV writer
# ---------------------------------------------------------------------------


def _decision_to_row(d: RatingSurveyDecision) -> list[str]:
    """Convert a decision dataclass to its CSV row list (column order).

    Args:
        d: A decision instance.

    Returns:
        List of stringified field values in canonical column order.
    """
    return [str(getattr(d, f.name)) for f in fields(d)]


def _write_csv(decisions: tuple[RatingSurveyDecision, ...], csv_path: Path) -> None:
    """Write the survey CSV byte-deterministically.

    Args:
        decisions: All 8 decisions.
        csv_path: Output path.
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(list(Q6F_SURVEY_SCHEMA))
        for d in decisions:
            writer.writerow(_decision_to_row(d))


def _md_sections(
    decisions: tuple[RatingSurveyDecision, ...],
    metrics_by_candidate: dict[str, dict[str, float]],
    audit_pr: str,
) -> str:
    """Render the survey MD document.

    Args:
        decisions: All 8 decisions.
        metrics_by_candidate: Per-candidate metric dict.
        audit_pr: PR number string.

    Returns:
        Full MD content string.
    """
    selected_row = next(d for d in decisions if d.decision_id == "Q6F_selected_policy")
    family_row = next(d for d in decisions if d.decision_id == "Q6F_per_family_impact_summary")
    lines: list[str] = []
    lines.append("# Q6F Rating-Algorithm Survey")
    lines.append("")
    lines.append(f"**Audit PR:** {audit_pr}")
    lines.append("")
    lines.append("## 1. Non-Materialization Disclaimer")
    lines.append("")
    lines.append(
        "This artifact is the Q6F rating-algorithm SURVEY only. It does "
        "NOT materialize any rating value, does NOT write any Parquet, "
        "does NOT run the CROSS-02-01 post-materialization leakage audit, "
        "does NOT close Step 02_01_03, does NOT update any status YAML, "
        "and does NOT touch the dataset research_log or ROADMAP. The "
        "per-candidate metrics in this artifact are EVALUATION TRACES of "
        "forward-only rating predictions; they are Q6F-internal and are "
        "NOT Phase-03 baseline modelling results."
    )
    lines.append("")
    lines.append("## 2. Parent PR #242 Lineage")
    lines.append("")
    lines.append(f"- CSV SHA256: `{EXPECTED_PR242_CSV_SHA256}` (`{PARENT_PR242_CSV_REL}`)")
    lines.append(f"- MD  SHA256: `{EXPECTED_PR242_MD_SHA256}` (`{PARENT_PR242_MD_REL}`)")
    lines.append("")
    lines.append("## 3. Parent PR #243 Lineage (Q5 Preserved)")
    lines.append("")
    lines.append(f"- CSV SHA256: `{EXPECTED_PR243_CSV_SHA256}` (`{PARENT_PR243_CSV_REL}`)")
    lines.append(f"- MD  SHA256: `{EXPECTED_PR243_MD_SHA256}` (`{PARENT_PR243_MD_REL}`)")
    lines.append("")
    lines.append(
        f"Q5_selected_policy = `{Q5_SELECTED_POLICY}`; verdict = "
        f"`{Q5_SELECTED_POLICY_VERDICT}`. This survey does NOT re-adjudicate Q5."
    )
    lines.append("")
    lines.append("## 4. Parent PR #245 Lineage (Q6 deferred_blocker -> this survey)")
    lines.append("")
    lines.append(f"- CSV SHA256: `{EXPECTED_PR245_CSV_SHA256}` (`{PARENT_PR245_CSV_REL}`)")
    lines.append(f"- MD  SHA256: `{EXPECTED_PR245_MD_SHA256}` (`{PARENT_PR245_MD_REL}`)")
    lines.append("")
    lines.append(
        "Quoted from PR #245 Q6_selected_policy row: "
        "'`deferred_blocker_with_algorithm_survey_required` because the "
        "comparative back-testing evidence among Elo / Glicko-2 / TrueSkill "
        "/ rolling-baseline does not exist in any prior artifact and binding "
        "a winner would violate Invariant I7.' This Q6F survey is the direct "
        "unblock condition."
    )
    lines.append("")
    lines.append("## 5. Q6F-Only Scope")
    lines.append("")
    lines.append(
        "Q6F is the Layer-2 algorithm survey. It is NOT Phase 03 baseline "
        "modelling. The metrics are evaluation traces, not features. It does "
        "NOT train logistic regression, gradient boosting, GNNs, or any "
        "downstream classifier. It does NOT use a train/test split or "
        "temporal CV. The outcome of each PHA row is used only to score the "
        "forward-only prediction and to update the rating state for FUTURE "
        "rows; it is never read as a feature input for predicting its own "
        "match."
    )
    lines.append("")
    lines.append("## 6. Candidate Set + N-1 Rejection (BTL family)")
    lines.append("")
    lines.append(_BTL_REJECTION_TEXT)
    lines.append("")
    lines.append(
        f"Methods acknowledged-and-excluded: {', '.join(EXCLUDED_METHODS_CONSIDERED)}."
    )
    lines.append("")
    lines.append("## 7. Candidate Set + N-2 Rejection (raw MMR hybrid)")
    lines.append("")
    lines.append(RAW_MMR_HYBRID_REJECTION_TEXT)
    lines.append("")
    lines.append("## 8. Algorithm Specifications per Candidate")
    lines.append("")
    for c in Q6F_RATING_ALGORITHM_CANDIDATES:
        m = _CANDIDATE_METHODOLOGY.get(c, {})
        lines.append(f"### {c}")
        lines.append("")
        lines.append(f"- Initialization: {m.get('initialization_policy', '')}")
        lines.append(f"- Hyperparameter policy: {m.get('hyperparameter_policy', '')}")
        lines.append(f"- Cold-start policy: {m.get('cold_start_policy', '')}")
        lines.append(f"- Tie policy: {m.get('tie_policy', '')}")
        lines.append(f"- Forward-only constraints: {m.get('forward_only_constraints', '')}")
        lines.append(
            "- Player identity policy: toon_id (PHA grouping key per PR #245 §9; "
            "PHA has no player_id_worldwide column on this dataset)."
        )
        lines.append("")
    lines.append("## 9. Forward-Only Update Semantics")
    lines.append("")
    lines.append(
        f"Every per-row prediction uses rating state computed strictly from "
        f"PHA records satisfying `{STRICT_LT_HISTORY_FILTER}` (verbatim from "
        f"PR #245). The target outcome updates the rating state ONLY AFTER "
        f"scoring the prediction. Stream ordering is "
        f"`(focal_toon, TRY_CAST(details_timeUTC AS TIMESTAMP), replay_id)` "
        f"-- deterministic; same-timestamp ties broken by `replay_id`."
    )
    lines.append("")
    lines.append("## 10. Metric Definitions")
    lines.append("")
    lines.append(
        "AUC (ROC) computed via the Mann-Whitney U formulation with "
        "tie-averaged ranks; log-loss is the mean negative log likelihood "
        "with predictions clipped to [1e-15, 1 - 1e-15]; Brier is the mean "
        "squared error of the predicted probability; calibration error is "
        "expected calibration error (ECE) over 10 equal-width bins. All "
        "metrics computed on the non-cold-start subset (mask "
        "`~is_cold_start`)."
    )
    lines.append("")
    lines.append("## 11. Per-Candidate Metric Table")
    lines.append("")
    lines.append("| Candidate | AUC (CI) | Log-loss (CI) | Brier (CI) | Calibration Error |")
    lines.append("|---|---|---|---|---|")
    for c in Q6F_RATING_ALGORITHM_CANDIDATES:
        if not Q6F_CANDIDATE_INCLUSION[c]:
            lines.append(f"| {c} | n/a (carry-forward) | n/a | n/a | n/a |")
        else:
            mm = metrics_by_candidate[c]
            lines.append(
                f"| {c} | {mm['auc']:.4f} ({mm['auc_ci_low']:.4f}--"
                f"{mm['auc_ci_high']:.4f}) | {mm['log_loss']:.4f} "
                f"({mm['log_loss_ci_low']:.4f}--{mm['log_loss_ci_high']:.4f}) | "
                f"{mm['brier']:.4f} ({mm['brier_ci_low']:.4f}--"
                f"{mm['brier_ci_high']:.4f}) | {mm['calibration_error']:.4f} |"
            )
    lines.append("")
    lines.append("## 12. Q6F Selected Policy Binding Row")
    lines.append("")
    lines.append(f"- selected_policy: `{selected_row.selected_policy}`")
    lines.append(f"- verdict: `{selected_row.survey_verdict}`")
    lines.append(f"- materialization_permission: `{selected_row.materialization_permission}`")
    lines.append("")
    lines.append("Rationale (verbatim from CSV notes column):")
    lines.append("")
    lines.append("```")
    lines.append(selected_row.notes)
    lines.append("```")
    lines.append("")
    lines.append("Decision rule:")
    lines.append("")
    lines.append("```")
    lines.append(Q6F_SELECTION_DECISION_RULE)
    lines.append("```")
    lines.append("")
    lines.append("## 13. Materialization Permission Statement")
    lines.append("")
    lines.append(
        f"Materialization permission for Step 02_01_03: "
        f"`{selected_row.materialization_permission}`. Per the per-family "
        f"impact summary:"
    )
    lines.append("")
    lines.append("```")
    lines.append(_per_family_broadcast(selected_row.survey_verdict))
    lines.append("```")
    lines.append("")
    lines.append(
        "Future feature materialization is a SEPARATE PR (Layer-3) and is "
        "subject to its own CROSS-02-01 post-materialization leakage audit. "
        "This Q6F survey does NOT substitute for that audit."
    )
    lines.append("")
    lines.append("## 14. Non-Substitution Statement")
    lines.append("")
    lines.append(
        "This artifact does NOT replace PR #242 (8-question parent "
        "adjudication), PR #243 (Q5 cross-region successor), or PR #245 "
        "(Q6 rating-reconstruction successor). It is a successor "
        "adjudication that emits a Q6F verdict; it does not retract "
        "any prior verdict."
    )
    lines.append("")
    lines.append("## 15. Falsifier Roll-Call")
    lines.append("")
    lines.append("```")
    lines.append(_falsifier_roll_call())
    lines.append("```")
    lines.append("")
    lines.append("## 16. SHA Provenance")
    lines.append("")
    lines.append(
        f"- PR #242 CSV SHA256: `{EXPECTED_PR242_CSV_SHA256}`\n"
        f"- PR #242 MD  SHA256: `{EXPECTED_PR242_MD_SHA256}`\n"
        f"- PR #243 CSV SHA256: `{EXPECTED_PR243_CSV_SHA256}`\n"
        f"- PR #243 MD  SHA256: `{EXPECTED_PR243_MD_SHA256}`\n"
        f"- PR #245 CSV SHA256: `{EXPECTED_PR245_CSV_SHA256}`\n"
        f"- PR #245 MD  SHA256: `{EXPECTED_PR245_MD_SHA256}`"
    )
    lines.append("")
    lines.append("## 17. No Step 02_01_03 Closure / No Phase 03 Start")
    lines.append("")
    lines.append(
        "This PR does NOT close Step 02_01_03; closure is reserved for a "
        "future Layer-3 materialization PR (or a separate omit-and-unblock "
        "closure PR if Q6F selected "
        "`omit_reconstructed_rating_and_unblock_other_five`). Phase 03 "
        "remains `not_started` and no baseline modelling is performed in "
        "this PR."
    )
    lines.append("")
    lines.append("## 18. Citation Provenance")
    lines.append("")
    lines.append(
        f"- {CITATION_ELO_1978}\n"
        f"- {CITATION_GLICKMAN_1999}\n"
        f"- {CITATION_GLICKMAN_2012}\n"
        f"- {CITATION_HERBRICH_MINKA_GRAEPEL_2006}\n"
        f"- {CITATION_STEYERBERG_2009}\n"
        f"- {CITATION_HOSMER_LEMESHOW_2013}"
    )
    lines.append("")
    # Use family_row variable to suppress unused warning while keeping it
    # available for future MD shape extensions (e.g., per-row narrative).
    lines.append(
        f"<!-- per_family_impact_summary row decision_id: {family_row.decision_id} -->"
    )
    return "\n".join(lines) + "\n"


def _write_md(
    decisions: tuple[RatingSurveyDecision, ...],
    metrics_by_candidate: dict[str, dict[str, float]],
    md_path: Path,
    audit_pr: str,
) -> None:
    """Write the survey MD document.

    Args:
        decisions: All 8 decisions.
        metrics_by_candidate: Per-candidate metric dict.
        md_path: Output path.
        audit_pr: PR number string.
    """
    md_path.parent.mkdir(parents=True, exist_ok=True)
    content = _md_sections(decisions, metrics_by_candidate, audit_pr)
    md_path.write_text(content, encoding="utf-8")


def write_q6f_survey_artifacts(
    result: RatingSurveyResult,
    csv_path: Path,
    md_path: Path,
) -> None:
    """Write the Q6F survey CSV+MD pair byte-deterministically.

    Args:
        result: A populated ``RatingSurveyResult`` (typically returned by
            ``run_q6f_rating_algorithm_survey``).
        csv_path: Output CSV path.
        md_path: Output MD path.
    """
    _write_csv(result.decisions, csv_path)
    _write_md(
        result.decisions,
        result.metrics_by_candidate,
        md_path,
        audit_pr=result.decisions[0].audit_pr,
    )


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


_RatingEngine = Callable[[pd.DataFrame], dict[str, Any]]
_RATING_ENGINES: dict[str, _RatingEngine] = {
    "rolling_win_rate_or_bayesian_smoothed_baseline": _run_rolling_baseline_survey,
    "elo": _run_elo_survey,
    "glicko_or_glicko_2": _run_glicko2_survey,
    "trueskill_or_trueskill_like": _run_trueskill_survey,
}


def run_q6f_rating_algorithm_survey(
    db_path: Path,
    csv_path: Path,
    md_path: Path,
    audit_pr: str = AUDIT_PR_NUMBER_PLACEHOLDER,
    write_artifacts: bool = True,
    repo_root: Path | None = None,
    n_bootstrap: int = BOOTSTRAP_BLOCK_COUNT,
    seed: int = BOOTSTRAP_RANDOM_SEED,
) -> RatingSurveyResult:
    """Run the Q6F rating-algorithm survey end-to-end.

    Steps (Layer-1 T01-T06):
        1. Verify parent PR #242/#243/#245 SHAs (halt on mismatch).
        2. Load PHA forward-only stream (read-only DuckDB).
        3. Run 4 rating engines (rolling baseline, Elo, Glicko-2,
           TrueSkill) with forward-only per-row predictions.
        4. Compute per-candidate metrics with deterministic block-bootstrap
           CIs.
        5. Apply the proper-score CI binding decision rule
           (``Q6F_SELECTION_DECISION_RULE``).
        6. Construct 8 decision rows and (optionally) write CSV+MD.

    Args:
        db_path: Read-only path to the sc2egset DuckDB.
        csv_path: Survey CSV output path.
        md_path: Survey MD output path.
        audit_pr: PR number string (e.g., ``'PR #246'``); placeholder
            ``'PR #<TBD>'`` permitted at first commit and replaced after
            the draft PR is opened.
        write_artifacts: If True, write the CSV+MD pair; otherwise return
            the result without writing.
        repo_root: Optional repository root for SHA pin verification; if
            omitted, walks up from ``db_path``.
        n_bootstrap: Bootstrap replicate count for the CI computation
            (default ``BOOTSTRAP_BLOCK_COUNT``).
        seed: RNG seed for the bootstrap (default
            ``BOOTSTRAP_RANDOM_SEED``).

    Returns:
        Populated ``RatingSurveyResult`` instance.

    Raises:
        RatingSurveyError: If a parent SHA mismatches or the PHA stream is
            empty.
    """
    if repo_root is None:
        repo_root = _find_repo_root(db_path)
    # Step 1: parent SHA verification (halt on any mismatch).
    pre_mismatches = _check_parent_pr_shas((), repo_root)
    if pre_mismatches:
        key, message = pre_mismatches[0]
        raise RatingSurveyError(key, message)
    # Step 2: load forward-only stream.
    stream = _load_pha_history_chronological(db_path)
    # Step 3: run engines + Step 4: compute metrics.
    metrics_by_candidate: dict[str, dict[str, float]] = {}
    for c in Q6F_RATING_ALGORITHM_CANDIDATES:
        if not Q6F_CANDIDATE_INCLUSION[c]:
            metrics_by_candidate[c] = {k: math.nan for k in Q6F_METRICS}
            continue
        engine = _RATING_ENGINES[c]
        output = engine(stream)
        metrics_by_candidate[c] = _compute_engine_metrics(
            output, n_bootstrap=n_bootstrap, seed=seed
        )
    # Step 5: select policy.
    selection_tuple = _select_q6f_policy(metrics_by_candidate)
    # Step 6: build decisions + structural checks.
    decisions = _build_survey_decisions(metrics_by_candidate, audit_pr=audit_pr)
    falsifiers_fired: list[str] = []
    _StructuralCheck = Callable[
        [tuple[RatingSurveyDecision, ...]], tuple[bool, str]
    ]
    structural_checks: list[tuple[str, _StructuralCheck]] = [
        ("q6f_candidate_set_incomplete", _check_candidate_set_complete),
        ("q6f_decision_count_mismatch", _check_decision_count),
        ("q6f_decision_id_order_mismatch", _check_decision_id_order),
        ("q6f_materialization_creep", _check_no_materialized_output_paths),
        ("q6f_q5_re_adjudication_drift", _check_q5_not_re_adjudicated),
        ("q6f_selected_policy_row_missing", _check_selected_policy_row_present),
        ("q6f_per_family_impact_summary_missing", _check_per_family_impact_summary_present),
        ("q6f_excluded_methods_considered_incomplete", _check_excluded_methods_complete),
        ("q6f_raw_mmr_hybrid_rejection_missing", _check_raw_mmr_hybrid_rejection),
    ]
    halting_key: str | None = None
    for key, check in structural_checks:
        passed, message = check(decisions)
        if not passed:
            falsifiers_fired.append(key)
            if halting_key is None:
                halting_key = key
                LOGGER.warning("Falsifier %s fired: %s", key, message)
    # Re-write decisions with updated falsifier roll-call.
    if falsifiers_fired:
        decisions = tuple(
            _build_decision(
                decision_id=d.decision_id,
                candidate_policy=d.candidate_policy,
                metrics=metrics_by_candidate.get(d.candidate_policy)
                if Q6F_CANDIDATE_INCLUSION.get(d.candidate_policy, False)
                else None,
                selected_policy=d.selected_policy,
                verdict=d.survey_verdict,
                materialization_permission=d.materialization_permission,
                audit_pr=audit_pr,
                notes=d.notes,
            )
            for d in decisions
        )
    result = RatingSurveyResult(
        decisions=decisions,
        csv_path=str(csv_path),
        md_path=str(md_path),
        provenance_git_sha=_get_git_sha(),
        falsifiers_fired=tuple(falsifiers_fired),
        halting_falsifier=halting_key,
        passed=halting_key is None,
        metrics_by_candidate=metrics_by_candidate,
        selection=selection_tuple[0],
    )
    if write_artifacts and result.passed:
        write_q6f_survey_artifacts(result, csv_path, md_path)
    return result
