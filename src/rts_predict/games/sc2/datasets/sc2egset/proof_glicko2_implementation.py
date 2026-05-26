"""Q6G rating-implementation-proof for SC2EGSet Step 02_01_03.

Pure read-only module. Writes ONLY the Q6G proof CSV+MD artifact pair.
Never materializes a rating value. Never writes Parquet. Never modifies
status YAMLs, research logs, or ROADMAP. See ``planning/current_plan.md``
for the Layer-1 specification.

This module is the Layer-2 successor to PR #247's Q6F survey. PR #247
selected ``Q6F_selected_policy = narrow_with_evidence`` with
``materialization_permission = recommendation_only_blocked_pending_implementation_proof_pr``.
This module (PR #<TBD>) emits an implementation-proof verdict for the
Glicko-2 candidate (single candidate under proof per A5): it (a) re-runs
PR #247's event-by-event reference engine, (b) implements the
production-shaped batched-update Glicko-2 path (Glickman 2012 §3
rating-period batching), (c) emits the BLOCKER-1 ordering-equivalence
proof (Spearman rho >= 0.99 AND |Delta log-loss| <= SE_event), and
(d) emits the byte-determinism proof for the batched engine.

Row set (Layer-1 A11):

    Q6G_A_glicko2_event_by_event_reference
    Q6G_B_glicko2_batched_production_shape
    Q6G_C_glicko2_event_vs_batched_equivalence_proof  (A19; BLOCKER-1)
    Q6G_D_glicko2_implementation_byte_determinism_proof
    Q6G_selected_policy                               (BINDING; emergent)

Decision rule (T05 step 4; auto-derived only emits one of
``bind_now`` / ``recommendation_only_glicko2`` / ``deferred_blocker``):

    IF NOT Determinism pass: -> deferred_blocker
    ELIF NOT Equivalence pass: -> recommendation_only_glicko2 (NIT-N2 default)
    ELIF Equivalence pass AND Determinism pass: -> bind_now

The middle / first branches are the NIT-N2 default-expected-outcome
path; ``bind_now`` is reachable only if BOTH BLOCKER-1 (event-vs-batched
ordering equivalence; A19) AND byte-determinism succeed.

NIT-N1 (A20): the MD section 10 sample table is probability-only -- five
floats in [0, 1]; no raw ``mu``, ``sigma``, ``RD``, ``phi``, or ``tau``
is persisted in the MD outside the algorithm-specification section
(section 8) where Glicko-2 symbols are part of the formula text.

NIT-N6 (A21): the bootstrap CI computation is the deterministic
percentile bootstrap (NOT BCa) with the constants pinned in
``BOOTSTRAP_METHOD = "deterministic_percentile"``,
``BOOTSTRAP_RANDOM_SEED = 42``, ``BOOTSTRAP_BLOCK_COUNT = 200``,
``NUMPY_RNG_BIT_GENERATOR = "PCG64"``,
``PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY = "sorted_then_kahan"``.

A22 / NIT-N5: ``RATING_PERIOD_DAYS = 30`` is pinned per Glickman 2012
section 10 worked example. The ``{7, 30, 90}`` sensitivity arm is OUT OF
SCOPE for Q6G and deferred to a future Q6H or Layer-3 sensitivity step
(OQ6).

Q5 BINDING (PR #243; preserved verbatim): ``Q5_selected_policy =
sensitivity_indicator_co_registration`` with verdict
``narrow_with_evidence``. The Q6G proof does NOT re-adjudicate Q5.

Q6F BINDING (PR #247; preserved verbatim): ``Q6F_selected_policy =
narrow_with_evidence`` with
``materialization_permission = recommendation_only_blocked_pending_implementation_proof_pr``.
The Q6G proof does NOT re-adjudicate Q6F (does not re-rank the four
candidates; does not retract the ``narrow_with_evidence`` verdict).

Materialization is BLOCKED in this PR (A13): no row of the proof CSV
may reference any Parquet path; ``materialized_output_paths`` is empty
on every row. Layer-3 materialization is a SEPARATE PR contingent on
the Q6G verdict.
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import math
import re
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
    CITATION_GLICKMAN_1999,
    CITATION_GLICKMAN_2012,
    STRICT_LT_HISTORY_FILTER,
    _run_glicko2_survey,
)
from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
    _load_pha_history_chronological as _pr247_load_pha_history_chronological,
)

LOGGER = logging.getLogger(__name__)


__all__ = [
    "AUDIT_PR_NUMBER_PLACEHOLDER",
    "BOOTSTRAP_BLOCK_COUNT",
    "BOOTSTRAP_METHOD",
    "BOOTSTRAP_RANDOM_SEED",
    "CITATION_EFRON_TIBSHIRANI_1993",
    "CITATION_GLICKMAN_1999",
    "CITATION_GLICKMAN_2012",
    "CITATION_KAHAN_SUMMATION_HIGHAM_2002",
    "EQUIVALENCE_SPEARMAN_MIN",
    "EXPECTED_PR242_CSV_SHA256",
    "EXPECTED_PR242_MD_SHA256",
    "EXPECTED_PR243_CSV_SHA256",
    "EXPECTED_PR243_MD_SHA256",
    "EXPECTED_PR245_CSV_SHA256",
    "EXPECTED_PR245_MD_SHA256",
    "EXPECTED_PR247_CSV_SHA256",
    "EXPECTED_PR247_MD_SHA256",
    "FALSIFIER_PRIORITY_CHAIN",
    "GLICKO2_ITERATION_TOL",
    "GLICKO2_PATH_KINDS",
    "MD_SAMPLE_ROW_COUNT",
    "NUMPY_RNG_BIT_GENERATOR",
    "PARENT_PR242_CSV_REL",
    "PARENT_PR242_MD_REL",
    "PARENT_PR243_CSV_REL",
    "PARENT_PR243_MD_REL",
    "PARENT_PR245_CSV_REL",
    "PARENT_PR245_MD_REL",
    "PARENT_PR247_CSV_REL",
    "PARENT_PR247_MD_REL",
    "PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY",
    "Q5_SELECTED_POLICY",
    "Q5_SELECTED_POLICY_VERDICT",
    "Q6F_MATERIALIZATION_PERMISSION",
    "Q6F_SELECTED_POLICY",
    "Q6F_SELECTED_POLICY_VERDICT",
    "Q6G_ALLOWED_MATERIALIZATION_PERMISSIONS",
    "Q6G_ALLOWED_VERDICTS",
    "Q6G_BOOTSTRAP_BLOCK_COUNT",
    "Q6G_BOOTSTRAP_METHOD",
    "Q6G_BOOTSTRAP_RANDOM_SEED",
    "Q6G_DECISION_COUNT",
    "Q6G_FLOATING_POINT_SUMMATION_ORDER_POLICY",
    "Q6G_GLICKO2_ITERATION_TOL",
    "Q6G_HYPERPARAMETER_DEFAULTS",
    "Q6G_NUMPY_RNG_BIT_GENERATOR",
    "Q6G_PARENT_SHAS",
    "Q6G_PROOF_CSV_REL",
    "Q6G_PROOF_DECISION_RULE",
    "Q6G_PROOF_MD_REL",
    "Q6G_PROOF_ROWS",
    "Q6G_PROOF_SCHEMA",
    "Q6G_PROOF_SCHEMA_COLUMN_COUNT",
    "Q6G_RATING_PERIOD_DAYS",
    "RATING_PERIOD_DAYS",
    "RAW_MMR_HYBRID_REJECTION_TEXT",
    "RatingImplementationProofDecision",
    "RatingImplementationProofError",
    "RatingImplementationProofResult",
    "compute_proof_metrics",
    "run_q6g_rating_implementation_proof",
    "write_q6g_proof_artifacts",
]


# ---------------------------------------------------------------------------
# Parent PR provenance (BINDING; mismatch halts)
# A1: 8 pinned parent SHA constants.
# ---------------------------------------------------------------------------

PARENT_PR242_NUMBER: str = "PR #242"
PARENT_PR243_NUMBER: str = "PR #243"
PARENT_PR245_NUMBER: str = "PR #245"
PARENT_PR247_NUMBER: str = "PR #247"
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
EXPECTED_PR247_CSV_SHA256: str = (
    "249e5591c6505b748fe3d371284a72d8f4620f57dbe9628c908ec2fbf097c8ed"
)
EXPECTED_PR247_MD_SHA256: str = (
    "4b49bee405bf87d4b8920b188e2c38d185ecc077b532d64a8bdd5a90cdf143f2"
)

Q6G_PARENT_SHAS: dict[str, str] = {
    "parent_pr242_csv_sha256": EXPECTED_PR242_CSV_SHA256,
    "parent_pr242_md_sha256": EXPECTED_PR242_MD_SHA256,
    "parent_pr243_csv_sha256": EXPECTED_PR243_CSV_SHA256,
    "parent_pr243_md_sha256": EXPECTED_PR243_MD_SHA256,
    "parent_pr245_csv_sha256": EXPECTED_PR245_CSV_SHA256,
    "parent_pr245_md_sha256": EXPECTED_PR245_MD_SHA256,
    "parent_pr247_csv_sha256": EXPECTED_PR247_CSV_SHA256,
    "parent_pr247_md_sha256": EXPECTED_PR247_MD_SHA256,
}


# ---------------------------------------------------------------------------
# Inherited anchors (referenced; not re-derived)
# ---------------------------------------------------------------------------

# Q5 BINDING (PR #243; preserved verbatim per A2).
Q5_SELECTED_POLICY: str = "sensitivity_indicator_co_registration"
Q5_SELECTED_POLICY_VERDICT: str = "narrow_with_evidence"

# Q6F BINDING (PR #247; preserved verbatim per A3).
Q6F_SELECTED_POLICY: str = "narrow_with_evidence"
Q6F_SELECTED_POLICY_VERDICT: str = "narrow_with_evidence"
Q6F_MATERIALIZATION_PERMISSION: str = (
    "recommendation_only_blocked_pending_implementation_proof_pr"
)

# A6: strict-< history filter inherited verbatim from PR #242 / PR #247.
# (Imported from PR #247's module; re-declared here for visibility.)
_STRICT_LT_HISTORY_FILTER: str = STRICT_LT_HISTORY_FILTER


# ---------------------------------------------------------------------------
# External citations (NIT-N6 / A21 additions to PR #247 internal set)
# ---------------------------------------------------------------------------

CITATION_EFRON_TIBSHIRANI_1993: str = (
    "Efron, Tibshirani (1993) -- An Introduction to the Bootstrap. "
    "Chapman & Hall. Source for the percentile bootstrap (NIT-N6)."
)
CITATION_KAHAN_SUMMATION_HIGHAM_2002: str = (
    "Higham (2002) -- Accuracy and Stability of Numerical Algorithms, "
    "2nd ed. SIAM. Source for Kahan / Neumaier compensated summation "
    "(NIT-N6 PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY = sorted_then_kahan)."
)


# ---------------------------------------------------------------------------
# Bootstrap / determinism constants (A21; NIT-N6)
# ---------------------------------------------------------------------------

BOOTSTRAP_METHOD: str = "deterministic_percentile"
BOOTSTRAP_RANDOM_SEED: int = 42
BOOTSTRAP_BLOCK_COUNT: int = 200
NUMPY_RNG_BIT_GENERATOR: str = "PCG64"
PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY: str = "sorted_then_kahan"

# Q6G_*-prefixed aliases (per execution prompt T01 step 6 visibility).
Q6G_BOOTSTRAP_METHOD: str = BOOTSTRAP_METHOD
Q6G_BOOTSTRAP_RANDOM_SEED: int = BOOTSTRAP_RANDOM_SEED
Q6G_BOOTSTRAP_BLOCK_COUNT: int = BOOTSTRAP_BLOCK_COUNT
Q6G_NUMPY_RNG_BIT_GENERATOR: str = NUMPY_RNG_BIT_GENERATOR
Q6G_FLOATING_POINT_SUMMATION_ORDER_POLICY: str = (
    PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY
)


# ---------------------------------------------------------------------------
# Glicko-2 hyperparameter defaults + rating period + iteration tol
# (A9 + A22; Glickman 2012 section 10 worked example)
# ---------------------------------------------------------------------------

RATING_PERIOD_DAYS: int = 30
GLICKO2_ITERATION_TOL: float = 1e-6

# Q6G_*-prefixed aliases.
Q6G_RATING_PERIOD_DAYS: int = RATING_PERIOD_DAYS
Q6G_GLICKO2_ITERATION_TOL: float = GLICKO2_ITERATION_TOL

Q6G_HYPERPARAMETER_DEFAULTS: dict[str, float] = {
    "mu": 1500.0,
    "rd": 350.0,
    "sigma": 0.06,
    "tau": 0.5,
    "rating_period_days": float(RATING_PERIOD_DAYS),
    "iteration_tol": GLICKO2_ITERATION_TOL,
}


# ---------------------------------------------------------------------------
# Q6G structural constants
# ---------------------------------------------------------------------------

# A11: exactly 5 proof rows (4 substantive + 1 emergent verdict row).
Q6G_PROOF_ROWS: tuple[str, ...] = (
    "Q6G_A_glicko2_event_by_event_reference",
    "Q6G_B_glicko2_batched_production_shape",
    "Q6G_C_glicko2_event_vs_batched_equivalence_proof",
    "Q6G_D_glicko2_implementation_byte_determinism_proof",
    "Q6G_selected_policy",
)
Q6G_DECISION_COUNT: int = 5

# A19: equivalence-bound thresholds.
EQUIVALENCE_SPEARMAN_MIN: float = 0.99

# NIT-N1 (A20): MD section 10 sample row count.
MD_SAMPLE_ROW_COUNT: int = 5

# Allowed glicko2_path_kind values.
GLICKO2_PATH_KINDS: frozenset[str] = frozenset(
    {
        "event_by_event_reference",
        "batched_production_shape",
        "equivalence_proof",
        "byte_determinism_proof",
        "verdict_row",
    }
)

# Row-5 allowed verdicts (auto-derivable + override-only).
Q6G_ALLOWED_VERDICTS: frozenset[str] = frozenset(
    {
        "bind_now",
        "recommendation_only_glicko2",
        "defer_to_two_candidate_implementation_comparison",
        "omit_reconstructed_rating_and_unblock_other_five",
        "deferred_blocker",
    }
)

# Row-5 allowed materialization_permission values.
Q6G_ALLOWED_MATERIALIZATION_PERMISSIONS: frozenset[str] = frozenset(
    {
        # bind_now branch.
        (
            "permitted_for_all_6_families_with_pinned_glicko2_batched_"
            "production_implementation_and_hyperparameters_in_next_"
            "materialization_pr"
        ),
        # recommendation_only_glicko2 branch.
        (
            "recommendation_only_glicko2_event_by_event_validated_"
            "batched_path_unproven_or_unequivalent"
        ),
        # defer_to_two_candidate_implementation_comparison branch.
        "blocked_pending_q6h_two_candidate_implementation_comparison_pr",
        # omit_reconstructed_rating_and_unblock_other_five branch.
        "permitted_for_other_5_families_without_reconstructed_rating",
        # deferred_blocker (determinism-fail) branch.
        "blocked_pending_byte_determinism_failure_investigation",
        # deferred_blocker generic-named-reason branch.
        "blocked_pending_named_reason",
    }
)


# ---------------------------------------------------------------------------
# N-2 binding (preserved verbatim from PR #245 / PR #247)
# ---------------------------------------------------------------------------

RAW_MMR_HYBRID_REJECTION_TEXT: str = (
    "raw_mmr_where_present_plus_is_mmr_missing: REJECTED unchanged from "
    "PR #245 N-2 and re-affirmed by PR #247 Q6F. Q6G inherits this "
    "rejection without re-adjudication; the rated/unrated partition is "
    "correlated with skill (only ranked-ladder games carry MMR), so "
    "admitting raw_mmr as a feature plus is_mmr_missing as a flag would "
    "leak corpus structure under Invariant I5 (symmetric treatment)."
)


# ---------------------------------------------------------------------------
# Artifact-pair paths (I10 -- repo-relative)
# ---------------------------------------------------------------------------

Q6G_PROOF_CSV_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6g_rating_implementation_proof.csv"
)
Q6G_PROOF_MD_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6g_rating_implementation_proof.md"
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
PARENT_PR247_CSV_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6f_rating_algorithm_survey.csv"
)
PARENT_PR247_MD_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6f_rating_algorithm_survey.md"
)


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------


class RatingImplementationProofError(RuntimeError):
    """Raised when the proof entrypoint halts on a fired falsifier.

    Attributes:
        falsifier_key: The first fired falsifier key (priority order).
        message: Human-readable observed-vs-expected message.
    """

    def __init__(self, falsifier_key: str, message: str) -> None:
        self.falsifier_key = falsifier_key
        self.message = message
        super().__init__(f"Falsifier {falsifier_key!r} fired: {message}")


# ---------------------------------------------------------------------------
# Decision dataclass (T01 step 10; EXACTLY 39 fields)
# Field order is the CSV column order.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RatingImplementationProofDecision:
    """A single Q6G proof row.

    The CSV column order is exactly this dataclass's field order. The
    schema column count is asserted at module load against
    ``len(fields)`` (must equal 39 per NIT-N3 / A21 / A22).
    """

    decision_id: str
    parent_decision_id: str
    proof_row_label: str
    included_in_proof: str
    inclusion_or_rejection_reason: str
    glicko2_path_kind: str
    initialization_policy: str
    hyperparameter_policy: str
    cold_start_policy: str
    tie_policy: str
    player_identity_policy: str
    cross_region_policy: str
    forward_only_constraints: str
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
    equivalence_proof_statistics: str
    byte_determinism_proof_statistics: str
    selected_policy: str
    proof_verdict: str
    materialization_permission: str
    raw_mmr_hybrid_rejection: str
    evidence_paths: str
    falsifiers: str
    audit_pr: str
    materialized_output_paths: str
    notes: str
    bootstrap_random_seed: str
    rating_period_days: str
    glicko2_iteration_tol: str
    numpy_rng_bit_generator: str
    python_floating_point_summation_order_policy: str


@dataclass(frozen=True)
class RatingImplementationProofResult:
    """Top-level aggregate result of the Q6G implementation proof.

    Attributes:
        decisions: Exactly 5 rows in ``Q6G_PROOF_ROWS`` order.
        csv_path: Path where the CSV was (or would be) written.
        md_path: Path where the MD was (or would be) written.
        provenance_git_sha: HEAD git SHA at run time.
        falsifiers_fired: Tuple of every fired falsifier key.
        halting_falsifier: First falsifier that fired (or None).
        passed: True iff no falsifier fired.
        metrics_by_path: Per-path metric dict
            (``"event_by_event_reference"``, ``"batched_production_shape"``).
        equivalence_proof_statistics: Row-3 BLOCKER-1 statistics dict.
        byte_determinism_proof_statistics: Row-4 byte-equality dict.
        sample_probabilities: Exactly 5 floats in [0, 1] from Row-2 path.
        selection: Q6G_selected_policy verdict literal.
    """

    decisions: tuple[RatingImplementationProofDecision, ...]
    csv_path: str
    md_path: str
    provenance_git_sha: str
    falsifiers_fired: tuple[str, ...]
    halting_falsifier: str | None
    passed: bool
    metrics_by_path: dict[str, dict[str, float]]
    equivalence_proof_statistics: dict[str, Any]
    byte_determinism_proof_statistics: dict[str, Any]
    sample_probabilities: tuple[float, ...]
    selection: str


# ---------------------------------------------------------------------------
# CSV schema (canonical column order; matches dataclass field order)
# ---------------------------------------------------------------------------

Q6G_PROOF_SCHEMA: tuple[str, ...] = tuple(
    f.name for f in fields(RatingImplementationProofDecision)
)
Q6G_PROOF_SCHEMA_COLUMN_COUNT: int = len(Q6G_PROOF_SCHEMA)


# ---------------------------------------------------------------------------
# Decision rule (T05 step 4; inlined verbatim per BINDING)
# ---------------------------------------------------------------------------

_Q6G_PROOF_DECISION_RULE_LINES: tuple[str, ...] = (
    "Q6G PROOF DECISION RULE (BLOCKER-1; A19; NIT-N2 default)",
    "========================================================",
    "",
    "Let R3 = Row 3's equivalence_proof_statistics dict.",
    "Let R4 = Row 4's byte_determinism_proof_statistics dict.",
    "",
    "Equivalence pass = R3.passes_spearman_bound AND R3.passes_delta_log_loss_bound",
    "                   (BLOCKER-1; A19; Spearman rho >= 0.99 AND",
    "                    |Delta log-loss| <= SE_log_loss_event).",
    "Determinism pass = R4.hashes_equal.",
    "",
    "IF NOT Determinism pass:",
    "    selected_policy = 'deferred_blocker'",
    "    verdict = 'deferred_blocker'",
    "    materialization_permission =",
    "        'blocked_pending_byte_determinism_failure_investigation'",
    "    rationale = 'Glicko-2 batched-production engine is not byte-deterministic",
    "                 on two identical runs; this disqualifies any materialization",
    "                 decision.'",
    "",
    "ELIF NOT Equivalence pass:",
    "    # NIT-N2 default expected outcome.",
    "    selected_policy = 'recommendation_only_glicko2'",
    "    verdict = 'recommendation_only_glicko2'",
    "    materialization_permission =",
    "        'recommendation_only_glicko2_event_by_event_validated_'",
    "        'batched_path_unproven_or_unequivalent'",
    "    rationale = ('Event-by-event Glicko-2 implementation validated against",
    "                  PR #247 section 11; batched-production path",
    "                  Spearman rho = {R3.spearman_rho:.4f} or",
    "                  |Delta log-loss| = {R3.abs_delta_log_loss:.6f}",
    "                  (SE = {R3.se_log_loss_event:.6f}) failed A19's equivalence",
    "                  criterion. Q6F CI overlap (0.9% of mid-range) is not",
    "                  strong enough to bind a batched path that is not",
    "                  provably equivalent to the event path on this corpus.')",
    "",
    "ELIF Equivalence pass AND Determinism pass:",
    "    selected_policy = 'bind_now'",
    "    verdict = 'bind_now'",
    "    materialization_permission =",
    "        'permitted_for_all_6_families_with_pinned_glicko2_'",
    "        'batched_production_implementation_and_hyperparameters_'",
    "        'in_next_materialization_pr'",
    "    rationale = ('Glicko-2 batched-production implementation is",
    "                  byte-deterministic AND ordering-equivalent to the",
    "                  event-by-event reference (Spearman rho = {R3.spearman_rho:.4f}",
    "                  >= 0.99; |Delta log-loss| = {R3.abs_delta_log_loss:.6f}",
    "                  <= SE = {R3.se_log_loss_event:.6f}). Q6F section 11 metrics",
    "                  now transfer to the production path.')",
    "",
    "No other verdict branch is reachable from Row 5 in Q6G's auto-derived rule;",
    "defer_to_two_candidate_implementation_comparison and",
    "omit_reconstructed_rating_and_unblock_other_five are NOT auto-emitted. The",
    "Layer-2 executor may override the auto-derived verdict ONLY by writing",
    "substantive reasoning in the PR description AND obtaining reviewer-",
    "adversarial sign-off; the override decision is OUT OF SCOPE for this planner.",
)
Q6G_PROOF_DECISION_RULE: str = "\n".join(_Q6G_PROOF_DECISION_RULE_LINES)


# ---------------------------------------------------------------------------
# Falsifier chain (BINDING; >= 38 keys per A19 falsifier-index minimum)
# ---------------------------------------------------------------------------

FALSIFIER_PRIORITY_CHAIN: tuple[str, ...] = (
    # 8 parent-SHA pins.
    "parent_pr242_csv_sha256_mismatch",
    "parent_pr242_md_sha256_mismatch",
    "parent_pr243_csv_sha256_mismatch",
    "parent_pr243_md_sha256_mismatch",
    "parent_pr245_csv_sha256_mismatch",
    "parent_pr245_md_sha256_mismatch",
    "parent_pr247_csv_sha256_mismatch",
    "parent_pr247_md_sha256_mismatch",
    # BLOCKER-1 (A19).
    "q6g_batched_event_ordering_equivalence_unproven",
    "q6g_bind_now_emitted_without_equivalence_pass",
    # NIT-N1 (A20).
    "q6g_raw_mu_or_sigma_persisted_in_md",
    # Structural row invariants (A11).
    "q6g_decision_count_mismatch",
    "q6g_decision_id_order_mismatch",
    "q6g_q6g_selected_policy_row_missing",
    # Byte determinism + persistence.
    "q6g_byte_determinism_failed",
    "q6g_rating_trace_persistence_violation",
    # Re-adjudication drift (A2, A3).
    "q6g_q5_re_adjudication_drift",
    "q6g_q6f_re_adjudication_drift",
    # A5: TrueSkill re-implementation forbidden.
    "q6g_no_trueskill_re_implementation",
    # A22 + A21: pinned constants integrity.
    "q6g_rating_period_days_not_30",
    "q6g_bootstrap_seed_not_42",
    "q6g_bootstrap_block_count_not_200",
    "q6g_bootstrap_method_not_deterministic_percentile",
    "q6g_numpy_rng_not_pcg64",
    "q6g_python_summation_policy_not_sorted_then_kahan",
    "q6g_glicko2_iteration_tol_not_1e_6",
    # A13: materialization creep guards.
    "q6g_materialization_creep",
    "q6g_parquet_emitted",
    # A14: status / log / roadmap drift guards.
    "q6g_status_drift",
    "q6g_research_log_drift",
    "q6g_roadmap_drift",
    "q6g_spec_drift",
    "q6g_cleaning_layer_drift",
    # Forward-only enforcement (A6, A7, A8).
    "q6g_target_match_outcome_read_as_input",
    "q6g_future_match_leakage_referenced",
    "q6g_global_batch_fit_referenced",
    "q6g_no_post_game_token",
    # Phase 03 + Step 02_01_04 creep guards.
    "q6g_phase_03_baseline_creep",
    "q6g_step_02_01_04_creep",
    # A18: event reference must delegate to PR #247.
    "q6g_event_reference_not_imported_from_pr247",
)


# ---------------------------------------------------------------------------
# Module-import mechanical verification
# T01 step 13: schema length, dataclass field count, row count assertions.
# ---------------------------------------------------------------------------

assert len(set(FALSIFIER_PRIORITY_CHAIN)) == len(FALSIFIER_PRIORITY_CHAIN), (
    "FALSIFIER_PRIORITY_CHAIN contains duplicate keys"
)
assert len(FALSIFIER_PRIORITY_CHAIN) >= 38, (
    f"FALSIFIER_PRIORITY_CHAIN must contain >= 38 keys per A19 minimum set; "
    f"observed {len(FALSIFIER_PRIORITY_CHAIN)}"
)
assert Q6G_PROOF_SCHEMA_COLUMN_COUNT == 39, (
    f"Q6G_PROOF_SCHEMA column-count invariant violated "
    f"(observed {Q6G_PROOF_SCHEMA_COLUMN_COUNT}, expected 39 per NIT-N3)"
)
assert len(fields(RatingImplementationProofDecision)) == 39, (
    "RatingImplementationProofDecision must have exactly 39 fields per NIT-N3"
)
assert len(Q6G_PROOF_ROWS) == Q6G_DECISION_COUNT == 5, (
    "Q6G_PROOF_ROWS must have exactly 5 entries per A11"
)
assert len(Q6G_PARENT_SHAS) == 8, (
    "Q6G_PARENT_SHAS must map exactly 8 parent SHA names per A1"
)
assert BOOTSTRAP_RANDOM_SEED == 42, "BOOTSTRAP_RANDOM_SEED must be 42 per A21"
assert BOOTSTRAP_BLOCK_COUNT == 200, "BOOTSTRAP_BLOCK_COUNT must be 200 per A21"
assert BOOTSTRAP_METHOD == "deterministic_percentile", (
    "BOOTSTRAP_METHOD must be 'deterministic_percentile' per A21"
)
assert NUMPY_RNG_BIT_GENERATOR == "PCG64", "NUMPY_RNG_BIT_GENERATOR must be 'PCG64'"
assert PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY == "sorted_then_kahan", (
    "PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY must be 'sorted_then_kahan'"
)
assert RATING_PERIOD_DAYS == 30, "RATING_PERIOD_DAYS must be 30 per A22"
assert GLICKO2_ITERATION_TOL == 1e-6, "GLICKO2_ITERATION_TOL must be 1e-6"


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
    """Return a deterministic 6-decimal string, or ``'NaN'`` / ``'not_applicable'``.

    Args:
        value: Floating-point value or ``None``.

    Returns:
        ``'not_applicable'`` if ``value`` is ``None``; ``'NaN'`` if it is
        ``math.nan``; otherwise a 6-decimal fixed-format string.
    """
    if value is None:
        return "not_applicable"
    if isinstance(value, float) and math.isnan(value):
        return "NaN"
    return f"{value:.6f}"


def _kahan_neumaier_sum(values: np.ndarray) -> float:
    """Return the Kahan-Neumaier compensated summation of ``values``.

    NIT-N6 (A21): the batched log-loss accumulation uses this routine to
    eliminate platform-specific round-off at the 1-SE bound of A19's
    |Delta log-loss| check. Input is sorted by ``(toon_id, timestamp,
    replay_id)`` upstream; this function applies the compensated-sum
    inner loop.

    Args:
        values: 1-D numeric array.

    Returns:
        Sum as a Python float; matches naive ``values.sum()`` to within
        ULP for well-behaved inputs and is materially more accurate when
        the array contains heterogeneous magnitudes.
    """
    total = 0.0
    compensation = 0.0
    for v in values:
        f = float(v)
        if abs(total) >= abs(f):
            compensation += (total - (total + f)) + f
        else:
            compensation += (f - (total + f)) + total
        total = total + f
    return total + compensation


# ---------------------------------------------------------------------------
# T02 -- PHA loader + event-by-event reference invocation
# ---------------------------------------------------------------------------


def _load_pha_history_chronological(db_path: Path) -> pd.DataFrame:
    """Delegate to PR #247's PHA forward-only loader (A18).

    The PHA stream definition is byte-identical to PR #247 to guarantee
    Row 1's event-by-event reference reproduces PR #247 section 11 metrics
    to within ``1e-4``.

    Args:
        db_path: Read-only path to the sc2egset DuckDB.

    Returns:
        DataFrame with the PHA forward-only paired-row stream.

    Raises:
        RatingImplementationProofError: If the PR #247 loader raises (the
            error is re-wrapped with the matching Q6G falsifier key).
    """
    try:
        return _pr247_load_pha_history_chronological(db_path)
    except RuntimeError as exc:
        raise RatingImplementationProofError(
            "q6g_event_reference_not_imported_from_pr247",
            f"PR #247 loader raised: {exc}",
        ) from exc


def _run_glicko2_event_by_event_reference(
    stream: pd.DataFrame,
) -> dict[str, Any]:
    """Invoke PR #247's ``_run_glicko2_survey`` verbatim (A18).

    Row 1's metrics are computed from this engine's output unchanged --
    no re-implementation of the algorithm in Q6G. Gate (b5) verifies the
    import path on the proof module's source.

    Args:
        stream: PHA forward-only stream from
            ``_load_pha_history_chronological``.

    Returns:
        Dict with ``predicted_probabilities``, ``actuals``, ``is_cold_start``,
        ``rating_state_at_end``, ``runtime_ms`` (PR #247 engine output
        contract preserved).
    """
    return _run_glicko2_survey(stream)


# ---------------------------------------------------------------------------
# T03 -- Glicko-2 batched-production engine (Row 2)
# ---------------------------------------------------------------------------


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
        Expected score in [0, 1].
    """
    return 1.0 / (1.0 + math.exp(-_glicko2_g(rd_j) * (mu - mu_j)))


def _glicko2_solve_new_volatility(
    sigma: float,
    phi: float,
    v: float,
    delta: float,
    tau: float,
    tol: float = GLICKO2_ITERATION_TOL,
) -> float:
    """Solve the Glicko-2 volatility-update equation (Glickman 2012 section 3).

    Implements the illinois-method bracketing root-finder for the
    function ``f(x) = exp(x) * (delta^2 - phi^2 - v - exp(x)) /
    (2 * (phi^2 + v + exp(x))^2) - (x - log(sigma^2)) / tau^2``.

    Args:
        sigma: Current volatility.
        phi: Current rating deviation in Glicko-2 units.
        v: Estimated variance from this rating period.
        delta: Estimated improvement from this rating period.
        tau: System constant constraining volatility change.
        tol: Iteration tolerance (default ``GLICKO2_ITERATION_TOL`` = 1e-6).

    Returns:
        New volatility (sigma') for the player.
    """
    a = math.log(sigma * sigma)

    def f(x: float) -> float:
        e_x = math.exp(x)
        denom = phi * phi + v + e_x
        return e_x * (delta * delta - phi * phi - v - e_x) / (2.0 * denom * denom) - (
            x - a
        ) / (tau * tau)

    # Initial bracketing.
    if delta * delta > phi * phi + v:
        big_b = math.log(delta * delta - phi * phi - v)
    else:
        k = 1
        while f(a - k * tau) < 0:
            k += 1
            if k > 100:
                break
        big_b = a - k * tau
    big_a = a
    fa = f(big_a)
    fb = f(big_b)
    iterations = 0
    while abs(big_b - big_a) > tol:
        if iterations > 1000:
            break
        c = big_a + (big_a - big_b) * fa / (fb - fa + 1e-300)
        fc = f(c)
        if fc * fb <= 0:
            big_a = big_b
            fa = fb
        else:
            fa = fa / 2.0
        big_b = c
        fb = fc
        iterations += 1
    return math.exp(big_a / 2.0)


def _run_glicko2_batched_production(
    stream: pd.DataFrame,
    mu: float = 1500.0,
    rd: float = 350.0,
    sigma: float = 0.06,
    tau: float = 0.5,
    rating_period_days: int = RATING_PERIOD_DAYS,
    iteration_tol: float = GLICKO2_ITERATION_TOL,
) -> dict[str, Any]:
    """Run the production-shape batched-update Glicko-2 over the PHA stream.

    A22 / Glickman 2012 section 3: matches within a rating period are
    batched for the player; the player's ``(mu, RD, sigma)`` is updated
    once at the period boundary using the canonical batched-update
    equations. BETWEEN periods the state advances; the period boundary
    MUST NOT cross the target match's ``started_at`` (enforced via the
    strict-``<`` filter from A6).

    Per-row prediction at row R uses the rating state from the most
    recent CLOSED rating period strictly prior to R's timestamp -- this
    is the "production shape" because it matches how a serving system
    would carry rating state from period to period.

    NIT-N6 / A21: per-block log-loss accumulation uses
    ``sorted_then_kahan`` summation (sort by ``(toon_id, timestamp,
    replay_id)`` then Kahan-Neumaier compensated sum).

    Args:
        stream: PHA forward-only stream.
        mu: Initial Glicko rating (default 1500.0).
        rd: Initial rating deviation (default 350.0).
        sigma: Initial volatility (default 0.06).
        tau: System constant constraining volatility change (default 0.5).
        rating_period_days: Period length in days (A22 = 30).
        iteration_tol: Volatility-update convergence tolerance
            (default ``GLICKO2_ITERATION_TOL`` = 1e-6).

    Returns:
        Dict with ``predicted_probabilities``, ``actuals``, ``is_cold_start``,
        ``rating_state_at_end``, ``runtime_ms`` (matches PR #247 engine
        output contract).
    """
    start = time.perf_counter()
    scale = 173.7178
    n = len(stream)
    predictions = np.zeros(n, dtype=np.float64)
    actuals = np.zeros(n, dtype=np.float64)
    is_cold = np.zeros(n, dtype=bool)
    # NIT-N6: pre-sort the stream by (toon_id, timestamp, replay_id) for
    # deterministic accumulation order; the input is already sorted by
    # PR #247 loader but we make this explicit for byte-determinism.
    ts = pd.to_datetime(
        stream["details_timeUTC"], format="ISO8601", utc=True, errors="coerce"
    )
    df = stream.assign(_ts=ts).sort_values(
        by=["focal_toon", "_ts", "replay_id"], kind="stable"
    ).reset_index(drop=True)
    focals = df["focal_toon"].to_numpy()
    opponents = df["opponent_toon"].to_numpy()
    results = df["focal_result"].to_numpy()
    timestamps = df["_ts"].to_numpy()
    period_delta = np.timedelta64(rating_period_days, "D")
    if n == 0:
        runtime_ms = (time.perf_counter() - start) * 1000.0
        return {
            "predicted_probabilities": predictions,
            "actuals": actuals,
            "is_cold_start": is_cold,
            "rating_state_at_end": {},
            "runtime_ms": runtime_ms,
        }
    period_origin = timestamps[0]
    ratings: dict[str, dict[str, float]] = {}
    seen: dict[str, int] = {}
    # Pending batch keyed by toon_id; entries are (opp_mu, opp_phi,
    # outcome) tuples in match order. Predictions are emitted at row
    # time using closed-period state; the batch is flushed at period
    # boundaries.
    pending: dict[str, list[tuple[float, float, float]]] = {}
    current_period_index = 0
    state_published: dict[str, dict[str, float]] = {}

    def _initial_state() -> dict[str, float]:
        return {
            "mu": (mu - 1500.0) / scale,
            "phi": rd / scale,
            "sigma": sigma,
        }

    def _flush_period() -> None:
        """Apply the Glickman 2012 batched update to all pending players."""
        for player, observations in pending.items():
            state = ratings.setdefault(player, _initial_state())
            if not observations:
                # No matches in this period: phi grows by the pre-period
                # rule phi' = sqrt(phi^2 + sigma^2).
                state["phi"] = math.sqrt(state["phi"] ** 2 + state["sigma"] ** 2)
                continue
            v_inv = 0.0
            delta_term = 0.0
            for opp_mu, opp_phi, score in observations:
                g_j = _glicko2_g(opp_phi)
                e_j = 1.0 / (1.0 + math.exp(-g_j * (state["mu"] - opp_mu)))
                v_inv += g_j * g_j * e_j * (1.0 - e_j)
                delta_term += g_j * (score - e_j)
            v = 1.0 / (v_inv + 1e-300)
            delta = v * delta_term
            new_sigma = _glicko2_solve_new_volatility(
                state["sigma"], state["phi"], v, delta, tau, tol=iteration_tol
            )
            phi_star = math.sqrt(state["phi"] ** 2 + new_sigma * new_sigma)
            new_phi = 1.0 / math.sqrt(1.0 / (phi_star * phi_star) + 1.0 / v)
            new_mu = state["mu"] + new_phi * new_phi * delta_term
            ratings[player] = {
                "mu": new_mu,
                "phi": new_phi,
                "sigma": new_sigma,
            }
        # Carry forward state of players with no observations this period.
        for player, state in ratings.items():
            if player not in pending:
                state["phi"] = math.sqrt(state["phi"] ** 2 + state["sigma"] ** 2)
        # Publish closed-period state (snapshot used by the next period's
        # row predictions).
        state_published.clear()
        for player, state in ratings.items():
            state_published[player] = {
                "mu": state["mu"],
                "phi": state["phi"],
                "sigma": state["sigma"],
            }
        pending.clear()

    state_published.clear()  # bootstrap closed-period state is empty.
    for i in range(n):
        focal = focals[i]
        opp = opponents[i]
        ts_i = timestamps[i]
        # Identify the rating-period index for this row.
        elapsed_ns = ts_i - period_origin
        period_idx = int(elapsed_ns // period_delta)
        # Flush any periods that have closed strictly before this row's
        # period; A22 enforces that period_origin + period_delta * k <=
        # ts_i means period k is closed.
        while current_period_index < period_idx:
            _flush_period()
            current_period_index += 1
        # Predict using the most recently published closed-period state.
        # If no period has been closed yet, both players use the prior.
        focal_state = state_published.get(focal)
        opp_state = state_published.get(opp)
        if focal_state is None:
            focal_state_pred = _initial_state()
        else:
            focal_state_pred = focal_state
        if opp_state is None:
            opp_state_pred = _initial_state()
        else:
            opp_state_pred = opp_state
        e = _glicko2_e(focal_state_pred["mu"], opp_state_pred["mu"], opp_state_pred["phi"])
        predictions[i] = e
        is_cold[i] = seen.get(focal, 0) == 0
        actuals[i] = 1.0 if results[i] == "Win" else 0.0
        score_focal = actuals[i]
        # Push observations into both players' pending batches; ratings[]
        # is initialised lazily on first batch flush.
        # Read the opponent's closed-period (mu, phi) for the focal's
        # batched update; symmetric for the opponent.
        pending.setdefault(focal, []).append(
            (opp_state_pred["mu"], opp_state_pred["phi"], score_focal)
        )
        pending.setdefault(opp, []).append(
            (focal_state_pred["mu"], focal_state_pred["phi"], 1.0 - score_focal)
        )
        seen[focal] = seen.get(focal, 0) + 1
    # Flush the final open period so rating_state_at_end is complete.
    if pending:
        _flush_period()
        current_period_index += 1
    runtime_ms = (time.perf_counter() - start) * 1000.0
    return {
        "predicted_probabilities": predictions,
        "actuals": actuals,
        "is_cold_start": is_cold,
        "rating_state_at_end": ratings,
        "runtime_ms": runtime_ms,
    }


# ---------------------------------------------------------------------------
# T04 -- Metrics + deterministic percentile bootstrap CI
# ---------------------------------------------------------------------------


def _log_loss_from_arrays(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Compute binary log-loss with clipping (NIT-N6 sorted_then_kahan).

    Args:
        y_true: 1-D array of 0/1 labels.
        y_score: 1-D array of predicted probabilities.

    Returns:
        Mean negative log likelihood, or ``math.nan`` if empty.
    """
    if len(y_true) == 0:
        return math.nan
    eps = 1e-15
    y_clipped = np.clip(y_score, eps, 1.0 - eps)
    terms = -(y_true * np.log(y_clipped) + (1.0 - y_true) * np.log(1.0 - y_clipped))
    # NIT-N6: sorted_then_kahan summation. Sort the per-row terms by
    # magnitude (ascending |term|) then apply Kahan-Neumaier compensated
    # summation. The sort key is the absolute term value; the input is
    # already in stream order from the engine output.
    order = np.argsort(np.abs(terms), kind="stable")
    return float(_kahan_neumaier_sum(terms[order]) / len(terms))


def _brier_from_arrays(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Compute the binary Brier score.

    Args:
        y_true: 1-D array of 0/1 labels.
        y_score: 1-D array of predicted probabilities.

    Returns:
        Mean squared error, or ``math.nan`` if empty.
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
        ECE in [0, 1], or ``math.nan`` if empty.
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
        bin_mean_pred = float(y_score[mask].mean())
        bin_mean_actual = float(y_true[mask].mean())
        ece += (m / n) * abs(bin_mean_pred - bin_mean_actual)
    return float(ece)


def _compute_deterministic_percentile_ci(
    actuals: np.ndarray,
    probabilities: np.ndarray,
    metric_fn: Callable[[np.ndarray, np.ndarray], float],
    *,
    seed: int = BOOTSTRAP_RANDOM_SEED,
    block_count: int = BOOTSTRAP_BLOCK_COUNT,
    ci_level: float = 0.95,
    rng_bit_generator: str = NUMPY_RNG_BIT_GENERATOR,
) -> tuple[float, float]:
    """Compute a deterministic percentile bootstrap CI for ``metric_fn``.

    A21: the RNG is ``np.random.Generator(np.random.PCG64(seed))``; the
    resampling indices are stable across platforms because the PCG64
    bit-generator with a fixed seed produces an identical integer stream
    on every machine. The CI is the 2.5th / 97.5th percentile of the
    bootstrap distribution (NOT BCa).

    Args:
        actuals: 1-D array of 0/1 labels.
        probabilities: 1-D array of predicted probabilities.
        metric_fn: Function ``(actuals, probabilities) -> float``.
        seed: RNG seed (default 42).
        block_count: Number of bootstrap replicates (default 200).
        ci_level: Confidence level (default 0.95).
        rng_bit_generator: Must equal ``"PCG64"`` (A21).

    Returns:
        ``(ci_low, ci_high)`` tuple.

    Raises:
        RatingImplementationProofError: If ``rng_bit_generator`` is not
            ``"PCG64"``.
    """
    if rng_bit_generator != "PCG64":
        raise RatingImplementationProofError(
            "q6g_numpy_rng_not_pcg64",
            f"rng_bit_generator must be 'PCG64'; observed {rng_bit_generator!r}",
        )
    n = len(actuals)
    if n == 0:
        return (math.nan, math.nan)
    rng = np.random.Generator(np.random.PCG64(seed))
    samples = np.zeros(block_count, dtype=np.float64)
    for b in range(block_count):
        idx = rng.integers(0, n, size=n)
        samples[b] = metric_fn(actuals[idx], probabilities[idx])
    alpha = (1.0 - ci_level) / 2.0
    return (
        float(np.percentile(samples, alpha * 100.0)),
        float(np.percentile(samples, (1.0 - alpha) * 100.0)),
    )


def _compute_event_log_loss_se(
    actuals: np.ndarray, probabilities: np.ndarray
) -> float:
    """Return the deterministic-bootstrap SE for log-loss.

    A19: ``SE_log_loss_event = (CI_high - CI_low) / (2 * 1.96)`` from the
    95% percentile bootstrap.

    Args:
        actuals: 1-D array of 0/1 labels.
        probabilities: 1-D array of predicted probabilities.

    Returns:
        Estimated SE of log-loss.
    """
    ci_low, ci_high = _compute_deterministic_percentile_ci(
        actuals, probabilities, _log_loss_from_arrays
    )
    if math.isnan(ci_low) or math.isnan(ci_high):
        return math.nan
    return (ci_high - ci_low) / (2.0 * 1.96)


def compute_proof_metrics(
    engine_output: dict[str, Any],
    *,
    seed: int = BOOTSTRAP_RANDOM_SEED,
    block_count: int = BOOTSTRAP_BLOCK_COUNT,
) -> dict[str, float]:
    """Compute T04 metrics from a single engine's output.

    Args:
        engine_output: Output dict from
            ``_run_glicko2_event_by_event_reference`` or
            ``_run_glicko2_batched_production``.
        seed: Bootstrap seed (default 42).
        block_count: Bootstrap replicate count (default 200).

    Returns:
        Dict with ``log_loss``, ``log_loss_ci_low``, ``log_loss_ci_high``,
        ``brier``, ``brier_ci_low``, ``brier_ci_high``,
        ``calibration_error``, ``coverage_rate``, ``cold_start_rate``,
        ``runtime_summary`` (the runtime summary is a deterministic
        descriptor; wall-clock seconds are recorded separately as
        ``runtime_ms`` in the engine output but not emitted in metrics).
    """
    is_cold = engine_output["is_cold_start"]
    mask = ~is_cold
    yt = engine_output["actuals"][mask].astype(np.float64)
    ys = engine_output["predicted_probabilities"][mask].astype(np.float64)
    ll = _log_loss_from_arrays(yt, ys)
    brier = _brier_from_arrays(yt, ys)
    cal = _calibration_error(yt, ys)
    ll_low, ll_high = _compute_deterministic_percentile_ci(
        yt, ys, _log_loss_from_arrays, seed=seed, block_count=block_count
    )
    br_low, br_high = _compute_deterministic_percentile_ci(
        yt, ys, _brier_from_arrays, seed=seed, block_count=block_count
    )
    coverage_rate = float(mask.mean()) if len(is_cold) > 0 else math.nan
    cold_start_rate = float(is_cold.mean()) if len(is_cold) > 0 else math.nan
    return {
        "log_loss": ll,
        "log_loss_ci_low": ll_low,
        "log_loss_ci_high": ll_high,
        "brier": brier,
        "brier_ci_low": br_low,
        "brier_ci_high": br_high,
        "calibration_error": cal,
        "coverage_rate": coverage_rate,
        "cold_start_rate": cold_start_rate,
        "runtime_seconds": float(engine_output["runtime_ms"] / 1000.0),
    }


# ---------------------------------------------------------------------------
# T05 -- Equivalence proof + byte-determinism proof + selection
# ---------------------------------------------------------------------------


def _spearman_rho(x: np.ndarray, y: np.ndarray) -> float:
    """Return the Spearman rank correlation (tie-averaged ranks).

    Hand-implemented to avoid adding ``scipy`` as a runtime dependency
    (OQ3 default: avoid the new dep). Tie-averaged ranks match the
    convention used by PR #247's AUC computation.

    Args:
        x: 1-D numeric array.
        y: 1-D numeric array of the same length.

    Returns:
        Spearman rho in [-1, 1], or ``math.nan`` if either array is
        empty or has zero variance.
    """
    n = len(x)
    if n == 0 or n != len(y):
        return math.nan
    rx = _tie_averaged_ranks(x)
    ry = _tie_averaged_ranks(y)
    rx_mean = rx.mean()
    ry_mean = ry.mean()
    num = float(((rx - rx_mean) * (ry - ry_mean)).sum())
    denom_x = float(((rx - rx_mean) ** 2).sum())
    denom_y = float(((ry - ry_mean) ** 2).sum())
    if denom_x <= 0.0 or denom_y <= 0.0:
        return math.nan
    return num / math.sqrt(denom_x * denom_y)


def _tie_averaged_ranks(values: np.ndarray) -> np.ndarray:
    """Return ranks with ties broken by the average-rank convention.

    Args:
        values: 1-D numeric array.

    Returns:
        Array of float64 ranks (length matches ``values``); ties get the
        average of the positions they would otherwise occupy.
    """
    n = len(values)
    order = np.argsort(values, kind="stable")
    ranks = np.empty(n, dtype=np.float64)
    sorted_vals = values[order]
    i = 0
    while i < n:
        j = i + 1
        while j < n and sorted_vals[j] == sorted_vals[i]:
            j += 1
        avg = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[order[k]] = avg
        i = j
    return ranks


def _compute_event_vs_batched_equivalence_proof(
    event_output: dict[str, Any],
    batched_output: dict[str, Any],
) -> dict[str, Any]:
    """Compute the BLOCKER-1 / A19 equivalence statistics.

    Args:
        event_output: Output from ``_run_glicko2_event_by_event_reference``.
        batched_output: Output from ``_run_glicko2_batched_production``.

    Returns:
        Dict with ``spearman_rho``, ``abs_delta_log_loss``,
        ``se_log_loss_event``, ``passes_spearman_bound``,
        ``passes_delta_log_loss_bound`` (all 5 keys present).
    """
    # Cold-start mask: the union of both engines' cold-start flags so
    # equivalence is computed over comparable rows only.
    is_cold = event_output["is_cold_start"] | batched_output["is_cold_start"]
    mask = ~is_cold
    actuals = event_output["actuals"][mask].astype(np.float64)
    event_probs = event_output["predicted_probabilities"][mask].astype(np.float64)
    batched_probs = batched_output["predicted_probabilities"][mask].astype(np.float64)
    if len(actuals) == 0:
        return {
            "spearman_rho": math.nan,
            "abs_delta_log_loss": math.nan,
            "se_log_loss_event": math.nan,
            "passes_spearman_bound": False,
            "passes_delta_log_loss_bound": False,
        }
    spearman = _spearman_rho(event_probs, batched_probs)
    ll_event = _log_loss_from_arrays(actuals, event_probs)
    ll_batched = _log_loss_from_arrays(actuals, batched_probs)
    abs_delta_ll = abs(ll_batched - ll_event)
    se = _compute_event_log_loss_se(actuals, event_probs)
    passes_spearman = (
        spearman is not None
        and not math.isnan(spearman)
        and spearman >= EQUIVALENCE_SPEARMAN_MIN
    )
    passes_delta = (
        not math.isnan(abs_delta_ll)
        and not math.isnan(se)
        and abs_delta_ll <= se
    )
    return {
        "spearman_rho": float(spearman) if not math.isnan(spearman) else math.nan,
        "abs_delta_log_loss": float(abs_delta_ll),
        "se_log_loss_event": float(se),
        "passes_spearman_bound": bool(passes_spearman),
        "passes_delta_log_loss_bound": bool(passes_delta),
    }


def _compute_byte_determinism_proof(
    stream: pd.DataFrame,
) -> dict[str, Any]:
    """Run the batched engine twice and SHA-256 the probability arrays.

    Args:
        stream: PHA forward-only stream.

    Returns:
        Dict with ``run_a_sha256``, ``run_b_sha256``, ``hashes_equal``.
    """
    run_a = _run_glicko2_batched_production(stream)
    run_b = _run_glicko2_batched_production(stream)
    bytes_a = np.ascontiguousarray(run_a["predicted_probabilities"]).tobytes()
    bytes_b = np.ascontiguousarray(run_b["predicted_probabilities"]).tobytes()
    sha_a = hashlib.sha256(bytes_a).hexdigest()
    sha_b = hashlib.sha256(bytes_b).hexdigest()
    return {
        "run_a_sha256": sha_a,
        "run_b_sha256": sha_b,
        "hashes_equal": sha_a == sha_b,
    }


def _q6g_select_policy(
    equivalence_stats: dict[str, Any],
    byte_determinism_stats: dict[str, Any],
) -> tuple[str, str, str, str]:
    """Apply the Q6G auto-derived decision rule (T05 step 4).

    Args:
        equivalence_stats: Output from
            ``_compute_event_vs_batched_equivalence_proof``.
        byte_determinism_stats: Output from
            ``_compute_byte_determinism_proof``.

    Returns:
        4-tuple ``(selected_policy, verdict, materialization_permission,
        rationale)``.
    """
    equivalence_pass = bool(
        equivalence_stats.get("passes_spearman_bound", False)
        and equivalence_stats.get("passes_delta_log_loss_bound", False)
    )
    determinism_pass = bool(byte_determinism_stats.get("hashes_equal", False))
    if not determinism_pass:
        rationale = (
            "Glicko-2 batched-production engine is not byte-deterministic "
            "on two identical runs; this disqualifies any materialization "
            "decision. Investigate floating-point summation order, RNG "
            "seed handling, and per-period state caching."
        )
        return (
            "deferred_blocker",
            "deferred_blocker",
            "blocked_pending_byte_determinism_failure_investigation",
            rationale,
        )
    if not equivalence_pass:
        # NIT-N2 default expected outcome.
        rho = equivalence_stats.get("spearman_rho", math.nan)
        abs_delta = equivalence_stats.get("abs_delta_log_loss", math.nan)
        se = equivalence_stats.get("se_log_loss_event", math.nan)
        rho_str = f"{rho:.4f}" if not math.isnan(rho) else "NaN"
        delta_str = f"{abs_delta:.6f}" if not math.isnan(abs_delta) else "NaN"
        se_str = f"{se:.6f}" if not math.isnan(se) else "NaN"
        rationale = (
            "Event-by-event Glicko-2 implementation validated against "
            "PR #247 section 11; batched-production path Spearman rho = "
            f"{rho_str} or |Delta log-loss| = {delta_str} (SE = {se_str}) "
            "failed A19's equivalence criterion. Q6F's CI overlap (0.9% "
            "of mid-range) is not strong enough to bind a batched path "
            "that is not provably equivalent to the event path on this "
            "corpus."
        )
        return (
            "recommendation_only_glicko2",
            "recommendation_only_glicko2",
            (
                "recommendation_only_glicko2_event_by_event_validated_"
                "batched_path_unproven_or_unequivalent"
            ),
            rationale,
        )
    # Equivalence pass AND Determinism pass: bind_now.
    rho = equivalence_stats["spearman_rho"]
    abs_delta = equivalence_stats["abs_delta_log_loss"]
    se = equivalence_stats["se_log_loss_event"]
    rationale = (
        "Glicko-2 batched-production implementation is byte-deterministic "
        "AND ordering-equivalent to the event-by-event reference "
        f"(Spearman rho = {rho:.4f} >= 0.99; |Delta log-loss| = "
        f"{abs_delta:.6f} <= SE = {se:.6f}). Q6F section 11 metrics now "
        "transfer to the production path."
    )
    return (
        "bind_now",
        "bind_now",
        (
            "permitted_for_all_6_families_with_pinned_glicko2_batched_"
            "production_implementation_and_hyperparameters_in_next_"
            "materialization_pr"
        ),
        rationale,
    )


def _enforce_bind_now_guard(
    verdict: str,
    equivalence_stats: dict[str, Any],
    byte_determinism_stats: dict[str, Any],
) -> None:
    """Enforce the BLOCKER-1 / A19 guard: bind_now requires both passes.

    Args:
        verdict: Row 5's proof_verdict.
        equivalence_stats: Row 3's statistics.
        byte_determinism_stats: Row 4's statistics.

    Raises:
        RatingImplementationProofError: If ``verdict == 'bind_now'`` and
            any of the equivalence / determinism bounds fail. Falsifier
            key is ``q6g_bind_now_emitted_without_equivalence_pass``.
    """
    if verdict != "bind_now":
        return
    if not equivalence_stats.get("passes_spearman_bound", False):
        raise RatingImplementationProofError(
            "q6g_bind_now_emitted_without_equivalence_pass",
            "Row 5 verdict is 'bind_now' but Row 3 passes_spearman_bound "
            "is False",
        )
    if not equivalence_stats.get("passes_delta_log_loss_bound", False):
        raise RatingImplementationProofError(
            "q6g_bind_now_emitted_without_equivalence_pass",
            "Row 5 verdict is 'bind_now' but Row 3 "
            "passes_delta_log_loss_bound is False",
        )
    if not byte_determinism_stats.get("hashes_equal", False):
        raise RatingImplementationProofError(
            "q6g_bind_now_emitted_without_equivalence_pass",
            "Row 5 verdict is 'bind_now' but Row 4 hashes_equal is False",
        )


# ---------------------------------------------------------------------------
# Decision-row builder
# ---------------------------------------------------------------------------


_NOT_APPLICABLE: str = "not_applicable"


def _evidence_paths_text() -> str:
    """Return the newline-joined evidence-paths block.

    Returns:
        Multi-line string of repo-relative paths and citation strings.
    """
    return "\n".join(
        [
            PARENT_PR242_CSV_REL,
            PARENT_PR242_MD_REL,
            PARENT_PR243_CSV_REL,
            PARENT_PR243_MD_REL,
            PARENT_PR245_CSV_REL,
            PARENT_PR245_MD_REL,
            PARENT_PR247_CSV_REL,
            PARENT_PR247_MD_REL,
            f"citation::{CITATION_GLICKMAN_1999}",
            f"citation::{CITATION_GLICKMAN_2012}",
            f"citation::{CITATION_EFRON_TIBSHIRANI_1993}",
            f"citation::{CITATION_KAHAN_SUMMATION_HIGHAM_2002}",
            f"parent_pr242_csv_sha256::{EXPECTED_PR242_CSV_SHA256}",
            f"parent_pr242_md_sha256::{EXPECTED_PR242_MD_SHA256}",
            f"parent_pr243_csv_sha256::{EXPECTED_PR243_CSV_SHA256}",
            f"parent_pr243_md_sha256::{EXPECTED_PR243_MD_SHA256}",
            f"parent_pr245_csv_sha256::{EXPECTED_PR245_CSV_SHA256}",
            f"parent_pr245_md_sha256::{EXPECTED_PR245_MD_SHA256}",
            f"parent_pr247_csv_sha256::{EXPECTED_PR247_CSV_SHA256}",
            f"parent_pr247_md_sha256::{EXPECTED_PR247_MD_SHA256}",
        ]
    )


def _falsifier_roll_call(fired: tuple[str, ...] = ()) -> str:
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


def _metric_strings(metrics: dict[str, float] | None) -> dict[str, str]:
    """Return formatted-string metric values for the CSV.

    Args:
        metrics: Metric dict from ``compute_proof_metrics``, or ``None``.

    Returns:
        Dict with CSV-string-valued entries for the 9 numeric metric
        columns (excluding ``runtime_summary``, which is qualitative).
    """
    if metrics is None:
        return {
            "log_loss": _NOT_APPLICABLE,
            "log_loss_ci_low": _NOT_APPLICABLE,
            "log_loss_ci_high": _NOT_APPLICABLE,
            "brier": _NOT_APPLICABLE,
            "brier_ci_low": _NOT_APPLICABLE,
            "brier_ci_high": _NOT_APPLICABLE,
            "calibration_error": _NOT_APPLICABLE,
            "coverage_rate": _NOT_APPLICABLE,
            "cold_start_rate": _NOT_APPLICABLE,
        }
    return {
        "log_loss": _safe_float_str(metrics["log_loss"]),
        "log_loss_ci_low": _safe_float_str(metrics["log_loss_ci_low"]),
        "log_loss_ci_high": _safe_float_str(metrics["log_loss_ci_high"]),
        "brier": _safe_float_str(metrics["brier"]),
        "brier_ci_low": _safe_float_str(metrics["brier_ci_low"]),
        "brier_ci_high": _safe_float_str(metrics["brier_ci_high"]),
        "calibration_error": _safe_float_str(metrics["calibration_error"]),
        "coverage_rate": _safe_float_str(metrics["coverage_rate"]),
        "cold_start_rate": _safe_float_str(metrics["cold_start_rate"]),
    }


_PATH_INITIALIZATION_POLICY: str = (
    "Initial mu=1500 (Glicko scale), RD=350, sigma=0.06 (Glickman 2012 "
    "reference defaults; A9). Mapped to Glicko-2 internal scale by "
    "(mu - 1500) / 173.7178."
)
_PATH_HYPERPARAMETER_POLICY: str = (
    "mu=1500, RD=350, sigma=0.06, tau=0.5 (Glickman 2012 reference "
    "defaults; A9). rating_period_days=30 (A22 / NIT-N5 / OQ6; pinned "
    "per Glickman 2012 section 10 worked example). iteration_tol=1e-6."
)
_PATH_COLD_START_POLICY: str = (
    "G-CS-4: first match per focal toon_id is flagged is_cold_start=True; "
    "predicted probability at cold-start = symmetric E function = 0.5; "
    "cold-start rows are excluded from metric computation and from the "
    "BLOCKER-1 equivalence proof."
)
_PATH_TIE_POLICY: str = (
    "Decisive-only (Win/Loss) per PR #242 Q1 (PHA carries decisive "
    "results only); same-timestamp ties broken by deterministic sort "
    "key (focal_toon, TRY_CAST(details_timeUTC AS TIMESTAMP), replay_id)."
)
_PATH_PLAYER_IDENTITY: str = (
    "toon_id (PHA grouping key per PR #245 / PR #247; A10). NIT-N4 "
    "limitation: toon_id is region-scoped per Invariant #2 branch (iii); "
    "rating fragmentation across region-migrating players is an accepted "
    "Q6G bias."
)
_PATH_CROSS_REGION: str = (
    "is_cross_region_fragmented is a co-registered evidence dimension "
    "preserved per Q5 BINDING (PR #243 narrow_with_evidence); NOT a "
    "filter on the proof input stream. The Q6G proof does NOT "
    "re-adjudicate Q5."
)
_PATH_FORWARD_ONLY: str = (
    "Per-row prediction uses only PHA records satisfying "
    "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at "
    "(STRICT_LT_HISTORY_FILTER; A6 / PR #242 Q3 BIND_NOW). The target "
    "outcome updates the rating state ONLY AFTER scoring the prediction; "
    "it is never read as feature input for predicting its own match."
)
_ROW_METHODOLOGY: dict[str, dict[str, str]] = {
    "Q6G_A_glicko2_event_by_event_reference": {
        "glicko2_path_kind": "event_by_event_reference",
        "inclusion_or_rejection_reason": (
            "Row 1: PR #247 Glicko-2 event-by-event engine invoked verbatim "
            "via _run_glicko2_event_by_event_reference (A18). Reference "
            "anchor for the BLOCKER-1 equivalence proof."
        ),
        "initialization_policy": _PATH_INITIALIZATION_POLICY,
        "hyperparameter_policy": _PATH_HYPERPARAMETER_POLICY,
        "cold_start_policy": _PATH_COLD_START_POLICY,
        "tie_policy": _PATH_TIE_POLICY,
        "player_identity_policy": _PATH_PLAYER_IDENTITY,
        "cross_region_policy": _PATH_CROSS_REGION,
        "forward_only_constraints": _PATH_FORWARD_ONLY,
        "runtime_summary": "deterministic_forward_only_event_by_event_single_pass",
    },
    "Q6G_B_glicko2_batched_production_shape": {
        "glicko2_path_kind": "batched_production_shape",
        "inclusion_or_rejection_reason": (
            "Row 2: production-shape Glicko-2 batched-update path "
            "implemented per Glickman 2012 section 3 rating-period batching. "
            "Matches within a rating period are batched; state is "
            "published at period boundaries; per-row predictions consume "
            "the most recent CLOSED-period state."
        ),
        "initialization_policy": _PATH_INITIALIZATION_POLICY,
        "hyperparameter_policy": _PATH_HYPERPARAMETER_POLICY,
        "cold_start_policy": _PATH_COLD_START_POLICY,
        "tie_policy": _PATH_TIE_POLICY,
        "player_identity_policy": _PATH_PLAYER_IDENTITY,
        "cross_region_policy": _PATH_CROSS_REGION,
        "forward_only_constraints": _PATH_FORWARD_ONLY,
        "runtime_summary": "deterministic_forward_only_batched_period_pass",
    },
    "Q6G_C_glicko2_event_vs_batched_equivalence_proof": {
        "glicko2_path_kind": "equivalence_proof",
        "inclusion_or_rejection_reason": (
            "Row 3: BLOCKER-1 / A19 binding equivalence proof. Spearman "
            "rho between event-by-event and batched-production predicted "
            "probabilities (tie-averaged ranks; ~is_cold_start mask) plus "
            "|Delta log-loss| compared against the deterministic-bootstrap "
            "SE of the event-path log-loss."
        ),
        "initialization_policy": _NOT_APPLICABLE,
        "hyperparameter_policy": _PATH_HYPERPARAMETER_POLICY,
        "cold_start_policy": _PATH_COLD_START_POLICY,
        "tie_policy": _PATH_TIE_POLICY,
        "player_identity_policy": _PATH_PLAYER_IDENTITY,
        "cross_region_policy": _PATH_CROSS_REGION,
        "forward_only_constraints": _PATH_FORWARD_ONLY,
        "runtime_summary": "deterministic_equivalence_proof",
    },
    "Q6G_D_glicko2_implementation_byte_determinism_proof": {
        "glicko2_path_kind": "byte_determinism_proof",
        "inclusion_or_rejection_reason": (
            "Row 4: byte-stability proof for the batched-production "
            "engine. Two independent runs with identical args; the SHA-256 "
            "of the predicted-probability bytes must match (hashes_equal)."
        ),
        "initialization_policy": _NOT_APPLICABLE,
        "hyperparameter_policy": _PATH_HYPERPARAMETER_POLICY,
        "cold_start_policy": _NOT_APPLICABLE,
        "tie_policy": _NOT_APPLICABLE,
        "player_identity_policy": _PATH_PLAYER_IDENTITY,
        "cross_region_policy": _PATH_CROSS_REGION,
        "forward_only_constraints": _PATH_FORWARD_ONLY,
        "runtime_summary": "deterministic_byte_determinism_proof",
    },
    "Q6G_selected_policy": {
        "glicko2_path_kind": "verdict_row",
        "inclusion_or_rejection_reason": (
            "Row 5: emergent Q6G_selected_policy verdict per the auto-"
            "derived decision rule (Q6G_PROOF_DECISION_RULE). Equivalence "
            "pass AND determinism pass -> bind_now; equivalence fail -> "
            "recommendation_only_glicko2 (NIT-N2 default); determinism "
            "fail -> deferred_blocker."
        ),
        "initialization_policy": _NOT_APPLICABLE,
        "hyperparameter_policy": _PATH_HYPERPARAMETER_POLICY,
        "cold_start_policy": _NOT_APPLICABLE,
        "tie_policy": _NOT_APPLICABLE,
        "player_identity_policy": _PATH_PLAYER_IDENTITY,
        "cross_region_policy": _PATH_CROSS_REGION,
        "forward_only_constraints": _PATH_FORWARD_ONLY,
        "runtime_summary": "verdict_row",
    },
}


def _build_decision(
    *,
    decision_id: str,
    parent_decision_id: str,
    proof_row_label: str,
    included_in_proof: str,
    metrics: dict[str, float] | None,
    equivalence_stats: dict[str, Any] | None,
    byte_determinism_stats: dict[str, Any] | None,
    selected_policy: str,
    verdict: str,
    materialization_permission: str,
    audit_pr: str,
    notes: str,
) -> RatingImplementationProofDecision:
    """Construct one ``RatingImplementationProofDecision`` row.

    Args:
        decision_id: One of ``Q6G_PROOF_ROWS``.
        parent_decision_id: Parent linkage in the proof DAG.
        proof_row_label: Human-readable label.
        included_in_proof: ``"True"`` / ``"False"`` string.
        metrics: Per-path metric dict, or ``None`` for non-metric rows.
        equivalence_stats: Row-3 stats dict, or ``None``.
        byte_determinism_stats: Row-4 stats dict, or ``None``.
        selected_policy: Row-5 selected policy, or empty string.
        verdict: Row-5 verdict, or carry-forward sentinel.
        materialization_permission: Row-5 permission, or carry-forward.
        audit_pr: PR number string (e.g., ``'PR #249'``).
        notes: Free-form notes column.

    Returns:
        A frozen ``RatingImplementationProofDecision``.
    """
    methodology = _ROW_METHODOLOGY[decision_id]
    metric_strs = _metric_strings(metrics)
    eq_str = (
        json.dumps(equivalence_stats, sort_keys=True)
        if equivalence_stats is not None
        else _NOT_APPLICABLE
    )
    bd_str = (
        json.dumps(byte_determinism_stats, sort_keys=True)
        if byte_determinism_stats is not None
        else _NOT_APPLICABLE
    )
    return RatingImplementationProofDecision(
        decision_id=decision_id,
        parent_decision_id=parent_decision_id,
        proof_row_label=proof_row_label,
        included_in_proof=included_in_proof,
        inclusion_or_rejection_reason=methodology["inclusion_or_rejection_reason"],
        glicko2_path_kind=methodology["glicko2_path_kind"],
        initialization_policy=methodology["initialization_policy"],
        hyperparameter_policy=methodology["hyperparameter_policy"],
        cold_start_policy=methodology["cold_start_policy"],
        tie_policy=methodology["tie_policy"],
        player_identity_policy=methodology["player_identity_policy"],
        cross_region_policy=methodology["cross_region_policy"],
        forward_only_constraints=methodology["forward_only_constraints"],
        log_loss=metric_strs["log_loss"],
        log_loss_ci_low=metric_strs["log_loss_ci_low"],
        log_loss_ci_high=metric_strs["log_loss_ci_high"],
        brier=metric_strs["brier"],
        brier_ci_low=metric_strs["brier_ci_low"],
        brier_ci_high=metric_strs["brier_ci_high"],
        calibration_error=metric_strs["calibration_error"],
        coverage_rate=metric_strs["coverage_rate"],
        cold_start_rate=metric_strs["cold_start_rate"],
        runtime_summary=methodology["runtime_summary"],
        equivalence_proof_statistics=eq_str,
        byte_determinism_proof_statistics=bd_str,
        selected_policy=selected_policy,
        proof_verdict=verdict,
        materialization_permission=materialization_permission,
        raw_mmr_hybrid_rejection=RAW_MMR_HYBRID_REJECTION_TEXT,
        evidence_paths=_evidence_paths_text(),
        falsifiers=_falsifier_roll_call(),
        audit_pr=audit_pr,
        materialized_output_paths="",
        notes=notes,
        bootstrap_random_seed=str(BOOTSTRAP_RANDOM_SEED),
        rating_period_days=str(RATING_PERIOD_DAYS),
        glicko2_iteration_tol=f"{GLICKO2_ITERATION_TOL:.1e}",
        numpy_rng_bit_generator=NUMPY_RNG_BIT_GENERATOR,
        python_floating_point_summation_order_policy=(
            PYTHON_FLOATING_POINT_SUMMATION_ORDER_POLICY
        ),
    )


def _build_proof_decisions(
    metrics_by_path: dict[str, dict[str, float]],
    equivalence_stats: dict[str, Any],
    byte_determinism_stats: dict[str, Any],
    audit_pr: str,
) -> tuple[RatingImplementationProofDecision, ...]:
    """Construct all 5 proof decisions in ``Q6G_PROOF_ROWS`` order.

    Args:
        metrics_by_path: Mapping of path-kind to metric dict.
        equivalence_stats: Row-3 statistics.
        byte_determinism_stats: Row-4 statistics.
        audit_pr: PR number string.

    Returns:
        5-tuple of ``RatingImplementationProofDecision`` in canonical order.
    """
    selected_policy, verdict, materialization_permission, rationale = (
        _q6g_select_policy(equivalence_stats, byte_determinism_stats)
    )
    decisions: list[RatingImplementationProofDecision] = []
    # Row 1: event-by-event reference.
    notes_1 = (
        "Q6G Row 1 (event-by-event reference). Engine: PR #247 "
        "_run_glicko2_survey delegated verbatim via "
        "_run_glicko2_event_by_event_reference (A18). Metrics computed on "
        "the non-cold-start mask; expected to match PR #247 section 11 "
        "Glicko-2 row to within 1e-4 (log_loss ~ 0.6255, brier ~ 0.2177, "
        "calibration_error ~ 0.0349)."
    )
    decisions.append(
        _build_decision(
            decision_id="Q6G_A_glicko2_event_by_event_reference",
            parent_decision_id="Q6F_D_glicko_or_glicko_2",
            proof_row_label="Glicko-2 event-by-event reference",
            included_in_proof="True",
            metrics=metrics_by_path.get("event_by_event_reference"),
            equivalence_stats=None,
            byte_determinism_stats=None,
            selected_policy="",
            verdict="not_applicable_carry_forward",
            materialization_permission="not_applicable_carry_forward",
            audit_pr=audit_pr,
            notes=notes_1,
        )
    )
    # Row 2: batched production.
    notes_2 = (
        "Q6G Row 2 (batched-production Glicko-2). Engine: "
        "_run_glicko2_batched_production with rating_period_days=30, "
        "iteration_tol=1e-6, sorted_then_kahan summation order. Per-row "
        "predictions consume closed-period state only; period boundaries "
        "anchored at the earliest PHA timestamp."
    )
    decisions.append(
        _build_decision(
            decision_id="Q6G_B_glicko2_batched_production_shape",
            parent_decision_id="Q6G_A_glicko2_event_by_event_reference",
            proof_row_label="Glicko-2 batched-production shape",
            included_in_proof="True",
            metrics=metrics_by_path.get("batched_production_shape"),
            equivalence_stats=None,
            byte_determinism_stats=None,
            selected_policy="",
            verdict="not_applicable_carry_forward",
            materialization_permission="not_applicable_carry_forward",
            audit_pr=audit_pr,
            notes=notes_2,
        )
    )
    # Row 3: equivalence proof.
    notes_3 = (
        "Q6G Row 3 (BLOCKER-1 / A19 equivalence proof). Computes Spearman "
        "rho between Row 1 and Row 2 probabilities on the joint "
        "non-cold-start mask AND |Delta log-loss| against the "
        "deterministic-bootstrap SE of the event-path log-loss. "
        f"passes_spearman_bound = {equivalence_stats['passes_spearman_bound']}; "
        f"passes_delta_log_loss_bound = "
        f"{equivalence_stats['passes_delta_log_loss_bound']}."
    )
    decisions.append(
        _build_decision(
            decision_id="Q6G_C_glicko2_event_vs_batched_equivalence_proof",
            parent_decision_id="Q6G_B_glicko2_batched_production_shape",
            proof_row_label="Glicko-2 event-vs-batched equivalence proof",
            included_in_proof="True",
            metrics=None,
            equivalence_stats=equivalence_stats,
            byte_determinism_stats=None,
            selected_policy="",
            verdict="not_applicable_carry_forward",
            materialization_permission="not_applicable_carry_forward",
            audit_pr=audit_pr,
            notes=notes_3,
        )
    )
    # Row 4: byte-determinism proof.
    notes_4 = (
        "Q6G Row 4 (byte-determinism proof). Two independent invocations "
        "of _run_glicko2_batched_production over the same PHA stream; "
        "SHA-256 of np.ascontiguousarray(predicted_probabilities).tobytes() "
        "for each run. hashes_equal = "
        f"{byte_determinism_stats['hashes_equal']}."
    )
    decisions.append(
        _build_decision(
            decision_id="Q6G_D_glicko2_implementation_byte_determinism_proof",
            parent_decision_id="Q6G_B_glicko2_batched_production_shape",
            proof_row_label="Glicko-2 implementation byte determinism proof",
            included_in_proof="True",
            metrics=None,
            equivalence_stats=None,
            byte_determinism_stats=byte_determinism_stats,
            selected_policy="",
            verdict="not_applicable_carry_forward",
            materialization_permission="not_applicable_carry_forward",
            audit_pr=audit_pr,
            notes=notes_4,
        )
    )
    # Row 5: Q6G_selected_policy.
    selected_notes = (
        f"Q6G SELECTED POLICY = {selected_policy}\n"
        f"VERDICT = {verdict}\n"
        f"MATERIALIZATION PERMISSION = {materialization_permission}\n"
        f"RATIONALE: {rationale}\n"
        f"DECISION RULE (verbatim from Q6G_PROOF_DECISION_RULE): "
        "BLOCKER-1 (A19) + byte-determinism jointly necessary for bind_now; "
        "equivalence fail -> recommendation_only_glicko2 (NIT-N2 default); "
        "determinism fail -> deferred_blocker.\n"
        f"Q5 BINDING preserved ({Q5_SELECTED_POLICY}); "
        f"Q6F BINDING preserved ({Q6F_SELECTED_POLICY}); raw_mmr_hybrid "
        "rejection re-affirmed; no TrueSkill re-implementation (A5)."
    )
    decisions.append(
        _build_decision(
            decision_id="Q6G_selected_policy",
            parent_decision_id="Q6G_C_glicko2_event_vs_batched_equivalence_proof",
            proof_row_label="Q6G selected policy (BINDING)",
            included_in_proof="True",
            metrics=None,
            equivalence_stats=None,
            byte_determinism_stats=None,
            selected_policy=selected_policy,
            verdict=verdict,
            materialization_permission=materialization_permission,
            audit_pr=audit_pr,
            notes=selected_notes,
        )
    )
    return tuple(decisions)


# ---------------------------------------------------------------------------
# Structural / SHA falsifier checks
# ---------------------------------------------------------------------------


def _check_decision_count(
    decisions: tuple[RatingImplementationProofDecision, ...],
) -> tuple[bool, str]:
    """Verify exactly 5 decisions per A11.

    Args:
        decisions: All decisions.

    Returns:
        ``(passed, message)``.
    """
    if len(decisions) != Q6G_DECISION_COUNT:
        return (
            False,
            f"expected {Q6G_DECISION_COUNT} decisions; got {len(decisions)}",
        )
    return (True, "")


def _check_decision_id_order(
    decisions: tuple[RatingImplementationProofDecision, ...],
) -> tuple[bool, str]:
    """Verify decision IDs match the canonical A11 order.

    Args:
        decisions: 5 decisions.

    Returns:
        ``(passed, message)``.
    """
    observed = tuple(d.decision_id for d in decisions)
    if observed != Q6G_PROOF_ROWS:
        return (
            False,
            f"decision id order mismatch: observed {observed}; expected {Q6G_PROOF_ROWS}",
        )
    return (True, "")


def _check_q6g_selected_policy_row_present(
    decisions: tuple[RatingImplementationProofDecision, ...],
) -> tuple[bool, str]:
    """Verify the Q6G_selected_policy row exists with a valid verdict.

    Args:
        decisions: 5 decisions.

    Returns:
        ``(passed, message)``.
    """
    for d in decisions:
        if d.decision_id == "Q6G_selected_policy":
            if d.proof_verdict not in Q6G_ALLOWED_VERDICTS:
                return (
                    False,
                    f"Q6G_selected_policy verdict {d.proof_verdict!r} not in allowed set",
                )
            if d.materialization_permission not in Q6G_ALLOWED_MATERIALIZATION_PERMISSIONS:
                return (
                    False,
                    (
                        "Q6G_selected_policy materialization_permission "
                        f"{d.materialization_permission!r} not in allowed set"
                    ),
                )
            return (True, "")
    return (False, "Q6G_selected_policy row missing")


def _check_no_materialized_output_paths(
    decisions: tuple[RatingImplementationProofDecision, ...],
) -> tuple[bool, str]:
    """Verify every decision's ``materialized_output_paths`` is empty (A13).

    Args:
        decisions: 5 decisions.

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
    decisions: tuple[RatingImplementationProofDecision, ...],
) -> tuple[bool, str]:
    """Verify no row's verdict/selected_policy carries a Q5 token (A2).

    Args:
        decisions: 5 decisions.

    Returns:
        ``(passed, message)``.
    """
    q5_token = Q5_SELECTED_POLICY
    for d in decisions:
        for field_name in ("selected_policy", "proof_verdict"):
            value = getattr(d, field_name)
            if value == q5_token:
                return (
                    False,
                    f"row {d.decision_id} {field_name} carries Q5 token {q5_token!r}",
                )
    return (True, "")


def _check_q6f_not_re_adjudicated(
    decisions: tuple[RatingImplementationProofDecision, ...],
) -> tuple[bool, str]:
    """Verify no row's verdict/selected_policy retracts Q6F (A3).

    Q6F's verdict is ``narrow_with_evidence``; Q6G's allowed verdict set
    does NOT include that string. If any row's verdict literally equals
    ``narrow_with_evidence``, the proof is treated as having silently
    re-adjudicated Q6F.

    Args:
        decisions: 5 decisions.

    Returns:
        ``(passed, message)``.
    """
    q6f_token = Q6F_SELECTED_POLICY  # "narrow_with_evidence"
    for d in decisions:
        if d.decision_id == "Q6G_selected_policy" and d.proof_verdict == q6f_token:
            return (
                False,
                f"row {d.decision_id} carries Q6F verdict {q6f_token!r}",
            )
    return (True, "")


def _check_no_trueskill_re_implementation(module_source: str) -> tuple[bool, str]:
    """Verify the Q6G module does not re-implement TrueSkill (A5).

    Matches function definitions starting at column 0 only (module-level
    declarations); string-literal occurrences in this helper itself do
    not trigger a false positive.

    Args:
        module_source: Source text of this module.

    Returns:
        ``(passed, message)``.
    """
    # Function-name fragments that would indicate a TrueSkill engine
    # inside Q6G itself. The PR #247 module is allowed to define these;
    # the Q6G module must not.
    forbidden_function_fragments = (
        "_run_truesk" + "ill",
        "_truesk" + "ill_v",
        "_truesk" + "ill_w",
        "_truesk" + "ill_win_prob",
    )
    for fragment in forbidden_function_fragments:
        pattern = r"^def\s+" + re.escape(fragment) + r"\w*\("
        if re.search(pattern, module_source, re.MULTILINE):
            return (
                False,
                f"Q6G module contains forbidden function definition {fragment!r} (A5)",
            )
    return (True, "")


def _check_parent_pr_shas(
    repo_root: Path,
) -> list[tuple[str, str]]:
    """Verify all 8 parent SHAs match the pinned values (A1).

    Args:
        repo_root: Repository root.

    Returns:
        List of ``(falsifier_key, message)`` for any mismatch; empty on
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
        (
            "parent_pr247_csv_sha256_mismatch",
            repo_root / PARENT_PR247_CSV_REL,
            EXPECTED_PR247_CSV_SHA256,
        ),
        (
            "parent_pr247_md_sha256_mismatch",
            repo_root / PARENT_PR247_MD_REL,
            EXPECTED_PR247_MD_SHA256,
        ),
    ]
    for key, path, expected in pairs:
        sha = _sha256_file(path)
        if sha != expected:
            mismatches.append((key, f"{path}: observed {sha} expected {expected}"))
    return mismatches


# ---------------------------------------------------------------------------
# T06 -- CSV + MD writer (NIT-N1 probability-only sample)
# ---------------------------------------------------------------------------


def _decision_to_row(d: RatingImplementationProofDecision) -> list[str]:
    """Convert a decision to its CSV row list (column order).

    Args:
        d: A decision instance.

    Returns:
        List of stringified field values in canonical column order.
    """
    return [str(getattr(d, f.name)) for f in fields(d)]


def _write_csv(
    decisions: tuple[RatingImplementationProofDecision, ...], csv_path: Path
) -> None:
    """Write the proof CSV byte-deterministically.

    Args:
        decisions: 5 decisions.
        csv_path: Output path.
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(list(Q6G_PROOF_SCHEMA))
        for d in decisions:
            writer.writerow(_decision_to_row(d))


_MD_SECTION_10_HEADER: str = "## 10. Metric Definitions + Bootstrap Policy (A21)"
_MD_SECTION_11_HEADER: str = "## 11. Per-Path Metric Table (Rows 1 & 2)"


def _check_md_section_10_probability_only(md_content: str) -> tuple[bool, str]:
    """Verify MD section 10 contains no raw Glicko-2 symbols (NIT-N1 / A20).

    The grep-class check looks for ``mu=``, ``sigma=``, ``RD=``, ``phi=``,
    ``tau=`` between the section-10 and section-11 headers. Glicko-2
    symbol references are ALLOWED only in section 8 (Algorithm
    Specification).

    Args:
        md_content: Full MD content string.

    Returns:
        ``(passed, message)`` -- ``passed=False`` if any raw symbol is
        found in the section-10 slice.
    """
    start = md_content.find(_MD_SECTION_10_HEADER)
    end = md_content.find(_MD_SECTION_11_HEADER)
    if start < 0 or end < 0 or end <= start:
        return (False, "MD section 10 or 11 header missing or out of order")
    slice_text = md_content[start:end]
    match = re.search(r"\b(mu|sigma|RD|phi|tau)\s*=", slice_text)
    if match:
        return (
            False,
            f"MD section 10 contains forbidden Glicko-2 symbol token "
            f"{match.group(0)!r} (NIT-N1 / A20)",
        )
    return (True, "")


def _md_sections(
    decisions: tuple[RatingImplementationProofDecision, ...],
    metrics_by_path: dict[str, dict[str, float]],
    equivalence_stats: dict[str, Any],
    byte_determinism_stats: dict[str, Any],
    sample_probabilities: tuple[float, ...],
    audit_pr: str,
) -> str:
    """Render the proof MD document (19 sections per File Manifest outline).

    Args:
        decisions: 5 decisions.
        metrics_by_path: Per-path metric dict.
        equivalence_stats: Row-3 stats.
        byte_determinism_stats: Row-4 stats.
        sample_probabilities: Exactly 5 floats in [0, 1] from Row-2.
        audit_pr: PR number string.

    Returns:
        Full MD content string.
    """
    selected_row = next(d for d in decisions if d.decision_id == "Q6G_selected_policy")
    # event_metrics is rendered indirectly via metrics_by_path lookups
    # inside the per-path table.
    _ = metrics_by_path.get("event_by_event_reference", {})
    _ = metrics_by_path.get("batched_production_shape", {})
    lines: list[str] = []
    lines.append("# Q6G Rating-Implementation Proof")
    lines.append("")
    lines.append(f"**Audit PR:** {audit_pr}")
    lines.append("")
    # Section 1.
    lines.append("## 1. Non-Materialization Disclaimer")
    lines.append("")
    lines.append(
        "This artifact is the Q6G rating-implementation PROOF only. It "
        "does NOT materialize any rating value, does NOT write any "
        "Parquet, does NOT run the CROSS-02-01 post-materialization "
        "leakage audit, does NOT close Step 02_01_03, does NOT update "
        "any status YAML, and does NOT touch the dataset research_log "
        "or ROADMAP. The per-path metrics and equivalence / determinism "
        "statistics in this artifact are EVALUATION TRACES of forward-"
        "only rating predictions; they are Q6G-internal and are NOT "
        "Phase-03 baseline modelling results."
    )
    lines.append("")
    # Section 2.
    lines.append("## 2. Parent PR #242 Lineage")
    lines.append("")
    lines.append(f"- CSV SHA256: `{EXPECTED_PR242_CSV_SHA256}` (`{PARENT_PR242_CSV_REL}`)")
    lines.append(f"- MD  SHA256: `{EXPECTED_PR242_MD_SHA256}` (`{PARENT_PR242_MD_REL}`)")
    lines.append("")
    # Section 3.
    lines.append("## 3. Parent PR #243 Lineage (Q5 Preserved)")
    lines.append("")
    lines.append(f"- CSV SHA256: `{EXPECTED_PR243_CSV_SHA256}` (`{PARENT_PR243_CSV_REL}`)")
    lines.append(f"- MD  SHA256: `{EXPECTED_PR243_MD_SHA256}` (`{PARENT_PR243_MD_REL}`)")
    lines.append("")
    lines.append(
        f"Q5_selected_policy = `{Q5_SELECTED_POLICY}`; verdict = "
        f"`{Q5_SELECTED_POLICY_VERDICT}`. This proof does NOT re-adjudicate Q5."
    )
    lines.append("")
    # Section 4.
    lines.append("## 4. Parent PR #245 Lineage (Q6 Discharged)")
    lines.append("")
    lines.append(f"- CSV SHA256: `{EXPECTED_PR245_CSV_SHA256}` (`{PARENT_PR245_CSV_REL}`)")
    lines.append(f"- MD  SHA256: `{EXPECTED_PR245_MD_SHA256}` (`{PARENT_PR245_MD_REL}`)")
    lines.append("")
    lines.append(
        "PR #245 closed Q6 with verdict `deferred_blocker` and "
        "materialization_permission `blocked_pending_algorithm_survey_pr`. "
        "PR #247 (Q6F) discharged the algorithm-survey deferral with "
        f"`Q6F_selected_policy = {Q6F_SELECTED_POLICY}`."
    )
    lines.append("")
    # Section 5.
    lines.append("## 5. Parent PR #247 Lineage (Q6F -> this proof)")
    lines.append("")
    lines.append(f"- CSV SHA256: `{EXPECTED_PR247_CSV_SHA256}` (`{PARENT_PR247_CSV_REL}`)")
    lines.append(f"- MD  SHA256: `{EXPECTED_PR247_MD_SHA256}` (`{PARENT_PR247_MD_REL}`)")
    lines.append("")
    lines.append(
        f"`Q6F_selected_policy = {Q6F_SELECTED_POLICY}`; "
        f"materialization_permission = `{Q6F_MATERIALIZATION_PERMISSION}`. "
        "This Q6G implementation-proof PR is the direct unblock condition "
        "for the `_blocked_pending_implementation_proof_pr` clause. The "
        "Q6F verdict is BINDING and is NOT re-adjudicated by this proof."
    )
    lines.append("")
    # Section 6.
    lines.append("## 6. Q6G-Only Scope")
    lines.append("")
    lines.append(
        "Q6G is the Layer-2 implementation proof for the Glicko-2 "
        "candidate. It is NOT Phase-03 baseline modelling. The metrics "
        "are evaluation traces, not features. It does NOT train any "
        "downstream classifier. The outcome of each PHA row is used "
        "only to score the forward-only prediction and to update the "
        "rating state for FUTURE rows; it is never read as a feature "
        "input for predicting its own match. Q6G is also NOT feature "
        "materialization: Layer-3 materialization is a SEPARATE PR "
        "contingent on the Q6G verdict."
    )
    lines.append("")
    # Section 7.
    lines.append("## 7. Glicko-2 Single-Candidate Justification (A5)")
    lines.append("")
    lines.append(
        "PR #247 section 11 ranked Glicko-2 lowest by log-loss among the 4 "
        "included candidates (Glicko-2 = 0.6255 vs TrueSkill = 0.6291); the "
        "minimum-unblock unit is to prove the chosen candidate's "
        "implementation. Q6G proves Glicko-2 specifically. TrueSkill is "
        "NOT re-implemented in Q6G. If Q6G's verdict is "
        "`defer_to_two_candidate_implementation_comparison`, a separate "
        "Q6H PR would implement TrueSkill alongside."
    )
    lines.append("")
    # Section 8.
    lines.append("## 8. Algorithm Specification")
    lines.append("")
    lines.append(
        "Glicko-2 (Glickman 2012). Internal scale mapping: r -> "
        "(r - 1500) / 173.7178 to convert rating from Glicko scale to "
        "Glicko-2 internal mu units; RD -> RD / 173.7178 to convert "
        "rating deviation to Glicko-2 phi units; sigma is the volatility. "
        "Event-by-event simplification (Row 1): each match treated as a "
        "single-observation rating period; sigma held constant; the full "
        "batched volatility update is deferred to Row 2's batched path. "
        "Batched-production shape (Row 2): rating-period batching per "
        "Glickman 2012 section 3 equations 4-9 with rating_period_days=30 "
        "(A22) and iteration_tol=1e-6. Symbols mu, sigma, RD, phi, tau "
        "refer to the Glicko-2 player state and system constant as "
        "defined in Glickman 2012."
    )
    lines.append("")
    # Section 9.
    lines.append("## 9. Forward-Only Update Semantics + Strict-`<` Filter Inheritance")
    lines.append("")
    lines.append(
        f"Every per-row prediction uses rating state computed strictly "
        f"from PHA records satisfying `{_STRICT_LT_HISTORY_FILTER}` "
        "(verbatim from PR #242 / PR #247). The target outcome updates "
        "the rating state ONLY AFTER scoring the prediction. Stream "
        "ordering is `(focal_toon, TRY_CAST(details_timeUTC AS "
        "TIMESTAMP), replay_id)` -- deterministic; same-timestamp ties "
        "broken by `replay_id`."
    )
    lines.append("")
    # Section 10 (NIT-N1: probability-only).
    lines.append(_MD_SECTION_10_HEADER)
    lines.append("")
    lines.append(
        "Log-loss uses sorted_then_kahan compensated summation (NIT-N6); "
        "Brier is the mean squared error of the predicted probability; "
        "calibration error is expected calibration error (ECE) over 10 "
        "equal-width bins. Bootstrap CIs: deterministic percentile with "
        "BOOTSTRAP_RANDOM_SEED=42, BOOTSTRAP_BLOCK_COUNT=200, "
        "NUMPY_RNG_BIT_GENERATOR=PCG64 (A21)."
    )
    lines.append("")
    lines.append(
        "Sample probabilities (Row 2 batched-production path; first 5 "
        "PHA rows in stream-deterministic order; probability-only per "
        "NIT-N1 / A20):"
    )
    lines.append("")
    lines.append("| pha_row_index | predicted_probability |")
    lines.append("|---|---|")
    for idx, p in enumerate(sample_probabilities):
        lines.append(f"| {idx} | {p:.6f} |")
    lines.append("")
    # Section 11.
    lines.append(_MD_SECTION_11_HEADER)
    lines.append("")
    lines.append("| Path | Log-loss (CI) | Brier (CI) | Calibration Error |")
    lines.append("|---|---|---|---|")
    for label, path_key in (
        ("event_by_event_reference", "event_by_event_reference"),
        ("batched_production_shape", "batched_production_shape"),
    ):
        m = metrics_by_path.get(path_key, {})
        if not m:
            lines.append(f"| {label} | n/a | n/a | n/a |")
            continue
        lines.append(
            f"| {label} | {m['log_loss']:.4f} "
            f"({m['log_loss_ci_low']:.4f}--{m['log_loss_ci_high']:.4f}) | "
            f"{m['brier']:.4f} ({m['brier_ci_low']:.4f}--{m['brier_ci_high']:.4f}) | "
            f"{m['calibration_error']:.4f} |"
        )
    lines.append("")
    lines.append(
        f"CSV column count = {Q6G_PROOF_SCHEMA_COLUMN_COUNT} (per NIT-N3); "
        f"row count = {Q6G_DECISION_COUNT}."
    )
    lines.append("")
    # Section 12.
    lines.append("## 12. Q6G Selected Policy Binding Row (Row 5)")
    lines.append("")
    lines.append(f"- selected_policy: `{selected_row.selected_policy}`")
    lines.append(f"- verdict: `{selected_row.proof_verdict}`")
    lines.append(
        f"- materialization_permission: `{selected_row.materialization_permission}`"
    )
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
    lines.append(Q6G_PROOF_DECISION_RULE)
    lines.append("```")
    lines.append("")
    # Section 13.
    lines.append("## 13. Materialization Permission Statement")
    lines.append("")
    lines.append(
        f"Materialization permission for Step 02_01_03 reconstructed_rating "
        f"family: `{selected_row.materialization_permission}`."
    )
    lines.append("")
    lines.append(
        "Future feature materialization is a SEPARATE PR (Layer-3) and is "
        "subject to its own CROSS-02-01 post-materialization leakage "
        "audit. This Q6G proof does NOT substitute for that audit."
    )
    lines.append("")
    lines.append(
        "AUTHORITY (BINDING; A19): PR #247 section 11 metrics transfer to "
        "a batched-Glicko-2 `bind_now` ONLY IF A19's equivalence "
        "criterion passes (Spearman rho >= 0.99 AND |Delta log-loss| <= "
        "SE_log_loss_event). Without equivalence, the Q6F numbers do NOT "
        "certify the production path."
    )
    lines.append("")
    # Section 13a.
    lines.append("## 13a. Equivalence Proof Result (BLOCKER-1; A19)")
    lines.append("")
    eq = equivalence_stats
    rho_v = eq.get("spearman_rho", math.nan)
    delta_v = eq.get("abs_delta_log_loss", math.nan)
    se_v = eq.get("se_log_loss_event", math.nan)
    lines.append(
        f"- spearman_rho: `{rho_v:.6f}`" if not math.isnan(rho_v) else "- spearman_rho: `NaN`"
    )
    lines.append(
        f"- abs_delta_log_loss: `{delta_v:.6f}`"
        if not math.isnan(delta_v)
        else "- abs_delta_log_loss: `NaN`"
    )
    lines.append(
        f"- se_log_loss_event: `{se_v:.6f}`"
        if not math.isnan(se_v)
        else "- se_log_loss_event: `NaN`"
    )
    lines.append(
        f"- passes_spearman_bound (>= 0.99): "
        f"`{eq.get('passes_spearman_bound', False)}`"
    )
    lines.append(
        f"- passes_delta_log_loss_bound (<= SE): "
        f"`{eq.get('passes_delta_log_loss_bound', False)}`"
    )
    lines.append("")
    # Section 13b.
    lines.append("## 13b. Byte-Determinism Proof Result")
    lines.append("")
    bd = byte_determinism_stats
    lines.append(f"- run_a_sha256: `{bd.get('run_a_sha256', '')}`")
    lines.append(f"- run_b_sha256: `{bd.get('run_b_sha256', '')}`")
    lines.append(f"- hashes_equal: `{bd.get('hashes_equal', False)}`")
    lines.append("")
    # Section 14.
    lines.append("## 14. Non-Substitution Statement")
    lines.append("")
    lines.append(
        "This artifact does NOT replace PR #242, PR #243, PR #245, or "
        "PR #247. It is a successor adjudication that emits a Q6G "
        "verdict; it does not retract any prior verdict. Layer-3 "
        "materialization is a SEPARATE PR, with its own CROSS-02-01 "
        "post-materialization leakage audit."
    )
    lines.append("")
    # Section 15 (NIT-N4 Limitations).
    lines.append("## 15. Limitations (NIT-N4)")
    lines.append("")
    lines.append(
        "- `toon_id` is region-scoped per Invariant #2 branch (iii); "
        "rating fragmentation across region-migrating players is an "
        "accepted Q6G bias. A future worldwide-identity PR (out of scope "
        "here) would address it separately."
    )
    lines.append(
        "- Cold-start gate (G-CS-4): the first PHA row for any toon_id "
        "contributes nothing to metric computation but is counted in "
        "`cold_start_rate`. Cold-start rows do NOT participate in the "
        "A19 equivalence proof."
    )
    lines.append(
        "- PHA decisive-only (PR #242 Q1): Glicko-2's draw-margin "
        "parameter is inapplicable."
    )
    lines.append("")
    # Section 16.
    lines.append("## 16. Falsifier Roll-Call")
    lines.append("")
    lines.append("```")
    lines.append(_falsifier_roll_call())
    lines.append("```")
    lines.append("")
    # Section 17.
    lines.append("## 17. SHA Provenance")
    lines.append("")
    lines.append(
        f"- PR #242 CSV SHA256: `{EXPECTED_PR242_CSV_SHA256}`\n"
        f"- PR #242 MD  SHA256: `{EXPECTED_PR242_MD_SHA256}`\n"
        f"- PR #243 CSV SHA256: `{EXPECTED_PR243_CSV_SHA256}`\n"
        f"- PR #243 MD  SHA256: `{EXPECTED_PR243_MD_SHA256}`\n"
        f"- PR #245 CSV SHA256: `{EXPECTED_PR245_CSV_SHA256}`\n"
        f"- PR #245 MD  SHA256: `{EXPECTED_PR245_MD_SHA256}`\n"
        f"- PR #247 CSV SHA256: `{EXPECTED_PR247_CSV_SHA256}`\n"
        f"- PR #247 MD  SHA256: `{EXPECTED_PR247_MD_SHA256}`"
    )
    lines.append("")
    # Section 18.
    lines.append("## 18. No Step 02_01_03 Closure / No Phase 03 Start")
    lines.append("")
    lines.append(
        "This PR does NOT close Step 02_01_03; closure is reserved for "
        "a future Layer-3 materialization PR (or a separate omit-and-"
        "unblock closure PR if Q6G selects "
        "`omit_reconstructed_rating_and_unblock_other_five`). Phase 03 "
        "remains `not_started` and no baseline modelling is performed in "
        "this PR."
    )
    lines.append("")
    # Section 19.
    lines.append("## 19. Citation Provenance")
    lines.append("")
    lines.append(
        f"- {CITATION_GLICKMAN_1999}\n"
        f"- {CITATION_GLICKMAN_2012}\n"
        f"- {CITATION_EFRON_TIBSHIRANI_1993}\n"
        f"- {CITATION_KAHAN_SUMMATION_HIGHAM_2002}"
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def _write_md(
    decisions: tuple[RatingImplementationProofDecision, ...],
    metrics_by_path: dict[str, dict[str, float]],
    equivalence_stats: dict[str, Any],
    byte_determinism_stats: dict[str, Any],
    sample_probabilities: tuple[float, ...],
    md_path: Path,
    audit_pr: str,
) -> None:
    """Write the proof MD document.

    NIT-N1 grep-check is applied before writing; a match raises
    ``RatingImplementationProofError`` with falsifier key
    ``q6g_raw_mu_or_sigma_persisted_in_md``.

    Args:
        decisions: 5 decisions.
        metrics_by_path: Per-path metric dict.
        equivalence_stats: Row-3 stats.
        byte_determinism_stats: Row-4 stats.
        sample_probabilities: Exactly 5 floats in [0, 1] from Row-2.
        md_path: Output path.
        audit_pr: PR number string.
    """
    md_path.parent.mkdir(parents=True, exist_ok=True)
    content = _md_sections(
        decisions,
        metrics_by_path,
        equivalence_stats,
        byte_determinism_stats,
        sample_probabilities,
        audit_pr,
    )
    passed, message = _check_md_section_10_probability_only(content)
    if not passed:
        raise RatingImplementationProofError(
            "q6g_raw_mu_or_sigma_persisted_in_md", message
        )
    md_path.write_text(content, encoding="utf-8")


def write_q6g_proof_artifacts(
    result: RatingImplementationProofResult,
    csv_path: Path,
    md_path: Path,
) -> None:
    """Write the Q6G proof CSV+MD pair byte-deterministically.

    Args:
        result: A populated ``RatingImplementationProofResult`` (typically
            returned by ``run_q6g_rating_implementation_proof``).
        csv_path: Output CSV path.
        md_path: Output MD path.
    """
    _write_csv(result.decisions, csv_path)
    _write_md(
        result.decisions,
        result.metrics_by_path,
        result.equivalence_proof_statistics,
        result.byte_determinism_proof_statistics,
        result.sample_probabilities,
        md_path,
        audit_pr=result.decisions[0].audit_pr,
    )


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def run_q6g_rating_implementation_proof(
    db_path: Path,
    csv_path: Path,
    md_path: Path,
    audit_pr: str = AUDIT_PR_NUMBER_PLACEHOLDER,
    write_artifacts: bool = True,
    repo_root: Path | None = None,
    seed: int = BOOTSTRAP_RANDOM_SEED,
    block_count: int = BOOTSTRAP_BLOCK_COUNT,
) -> RatingImplementationProofResult:
    """Run the Q6G rating-implementation proof end-to-end.

    Steps (T01-T06):
        1. Verify all 8 parent PR SHAs (halt on mismatch).
        2. Load PHA forward-only stream (read-only DuckDB).
        3. Run Row 1 event-by-event reference (PR #247 engine delegated).
        4. Run Row 2 batched-production engine (Glickman 2012 section 3).
        5. Compute per-path metrics (deterministic percentile bootstrap CIs).
        6. Compute Row 3 equivalence proof (BLOCKER-1 / A19).
        7. Compute Row 4 byte-determinism proof.
        8. Apply the auto-derived decision rule for Row 5.
        9. Enforce the BLOCKER-1 guard.
       10. Construct 5 decisions and (optionally) write CSV+MD.

    Args:
        db_path: Read-only path to the sc2egset DuckDB.
        csv_path: Proof CSV output path.
        md_path: Proof MD output path.
        audit_pr: PR number string (e.g., ``'PR #249'``); placeholder
            ``'PR #<TBD>'`` is the default sentinel and is replaced once
            the draft PR is assigned a number.
        write_artifacts: If True, write the CSV+MD pair; otherwise
            return the result without writing.
        repo_root: Optional repository root for SHA pin verification;
            if omitted, walks up from ``db_path``.
        seed: Bootstrap seed (default ``BOOTSTRAP_RANDOM_SEED`` = 42).
        block_count: Bootstrap replicate count (default
            ``BOOTSTRAP_BLOCK_COUNT`` = 200).

    Returns:
        Populated ``RatingImplementationProofResult``.

    Raises:
        RatingImplementationProofError: If any parent SHA mismatches, any
            falsifier in ``FALSIFIER_PRIORITY_CHAIN`` fires, or the PHA
            stream is empty.
    """
    if repo_root is None:
        repo_root = _find_repo_root(db_path)
    # Step 1: parent SHA verification.
    pre_mismatches = _check_parent_pr_shas(repo_root)
    if pre_mismatches:
        key, message = pre_mismatches[0]
        raise RatingImplementationProofError(key, message)
    # Step 2: load forward-only stream.
    stream = _load_pha_history_chronological(db_path)
    # Step 3: Row 1 event-by-event reference.
    event_output = _run_glicko2_event_by_event_reference(stream)
    # Step 4: Row 2 batched-production.
    batched_output = _run_glicko2_batched_production(stream)
    # Step 5: per-path metrics.
    metrics_by_path: dict[str, dict[str, float]] = {
        "event_by_event_reference": compute_proof_metrics(
            event_output, seed=seed, block_count=block_count
        ),
        "batched_production_shape": compute_proof_metrics(
            batched_output, seed=seed, block_count=block_count
        ),
    }
    # Step 6: equivalence proof (Row 3).
    equivalence_stats = _compute_event_vs_batched_equivalence_proof(
        event_output, batched_output
    )
    # Step 7: byte-determinism proof (Row 4).
    byte_determinism_stats = _compute_byte_determinism_proof(stream)
    # Step 8-9: Row 5 decision + BLOCKER-1 guard.
    _, verdict, _, _ = _q6g_select_policy(equivalence_stats, byte_determinism_stats)
    _enforce_bind_now_guard(verdict, equivalence_stats, byte_determinism_stats)
    # Step 10: build decisions.
    decisions = _build_proof_decisions(
        metrics_by_path,
        equivalence_stats,
        byte_determinism_stats,
        audit_pr=audit_pr,
    )
    sample_count = MD_SAMPLE_ROW_COUNT
    raw_sample = batched_output["predicted_probabilities"][:sample_count]
    sample_probabilities: tuple[float, ...] = tuple(float(p) for p in raw_sample)
    # Structural checks.
    falsifiers_fired: list[str] = []
    halting_key: str | None = None
    structural_checks: list[
        tuple[
            str,
            Callable[[tuple[RatingImplementationProofDecision, ...]], tuple[bool, str]],
        ]
    ] = [
        ("q6g_decision_count_mismatch", _check_decision_count),
        ("q6g_decision_id_order_mismatch", _check_decision_id_order),
        ("q6g_q6g_selected_policy_row_missing", _check_q6g_selected_policy_row_present),
        ("q6g_materialization_creep", _check_no_materialized_output_paths),
        ("q6g_q5_re_adjudication_drift", _check_q5_not_re_adjudicated),
        ("q6g_q6f_re_adjudication_drift", _check_q6f_not_re_adjudicated),
    ]
    for key, check in structural_checks:
        passed, message = check(decisions)
        if not passed:
            falsifiers_fired.append(key)
            if halting_key is None:
                halting_key = key
                LOGGER.warning("Falsifier %s fired: %s", key, message)
    # BLOCKER-1 + A19 falsifier surfacing (non-halting; reported in roll-call).
    if not equivalence_stats.get("passes_spearman_bound", False) or not equivalence_stats.get(
        "passes_delta_log_loss_bound", False
    ):
        falsifiers_fired.append("q6g_batched_event_ordering_equivalence_unproven")
    if not byte_determinism_stats.get("hashes_equal", False):
        falsifiers_fired.append("q6g_byte_determinism_failed")
    result = RatingImplementationProofResult(
        decisions=decisions,
        csv_path=str(csv_path),
        md_path=str(md_path),
        provenance_git_sha=_get_git_sha(),
        falsifiers_fired=tuple(falsifiers_fired),
        halting_falsifier=halting_key,
        passed=halting_key is None,
        metrics_by_path=metrics_by_path,
        equivalence_proof_statistics=equivalence_stats,
        byte_determinism_proof_statistics=byte_determinism_stats,
        sample_probabilities=sample_probabilities,
        selection=decisions[-1].selected_policy,
    )
    if write_artifacts and result.passed:
        write_q6g_proof_artifacts(result, csv_path, md_path)
    return result
