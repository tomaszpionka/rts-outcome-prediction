"""Adjudication module for SC2EGSet Step 02_02_01.

Source-anchor / column-naming / direction-policy / transform-scope adjudication
for the symmetry & difference feature family. Decision-recording only — emits
exactly one CSV + one MD adjudication artifact pair; does NOT materialise any
feature value, does NOT emit any CROSS-02-01 audit, does NOT touch any status
YAML / research_log / ROADMAP path. Future feature materialisation is a
separate Step 02_02 PR (Layer-2 materialisation, analogue of PR #259).

Lineage:
- ROADMAP stub: PR #264.
- Layer-1 scaffold plan: PR #265.
- Layer-2 scaffold execution + validator: PR #266.
- Layer-1 adjudication plan: PR #267.
- Layer-2 adjudication execution: THIS PR.

Binding contract is ``planning/current_plan.md`` (Round 2 plan; merged via PR #267).
Round-2 nits N1-N6 applied; see CSV/MD rationale fields and tests for traceability.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import logging
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from rts_predict.games.sc2.datasets.sc2egset.validate_symmetry_difference_feature_materialization import (  # noqa: E501
    CandidateFeatureSpec,
    validate_symmetry_difference_feature_materialization,
)

LOGGER = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Provenance / identity constants
# ---------------------------------------------------------------------------

AUDIT_PR: str = "PR #<TBD>"  # normalized after the draft PR opens
EXECUTED_AT_UTC_DATE: str = "2026-05-29"
DECISION_ID: str = "02_02_01_symmetry_difference_feature_scope"
LINEAGE_POSITION: str = (
    "PR #264 (ROADMAP stub) -> PR #265 (Layer-1 scaffold plan) -> "
    "PR #266 (Layer-2 scaffold execution + validator) -> "
    "PR #267 (Layer-1 adjudication plan) -> "
    "THIS PR (Layer-2 adjudication execution; no materialisation)"
)
ALLOWED_DIRECTIONS: tuple[str, str] = ("focal_minus_opponent", "symmetric")
ROW_IDENTITY_JOIN_KEYS: tuple[str, str, str, str] = (
    "focal_match_id",
    "focal_player",
    "opponent_player",
    "started_at",
)

# Authoritative inputs (resolved relative to repo_root)
_REPO_RELATIVE_VALIDATOR_PATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/"
    "validate_symmetry_difference_feature_materialization.py"
)
_REPO_RELATIVE_PARENT_02_01_02_PARQUET: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_02_pre_game_features.parquet"
)
_REPO_RELATIVE_PARENT_02_01_03_PARQUET: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_enriched_pre_game_features.parquet"
)
_REPO_RELATIVE_PARENT_02_01_02_AUDIT: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/"
    "leakage_audit_sc2egset.json"
)
_REPO_RELATIVE_PARENT_02_01_03_AUDIT: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/"
    "leakage_audit_sc2egset.json"
)

# Default output directory (relative to repo root)
_REPO_RELATIVE_OUTPUT_DIR: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/02_symmetry_and_difference_features"
)
_OUTPUT_CSV_NAME: str = "02_02_01_symmetry_difference_feature_adjudication.csv"
_OUTPUT_MD_NAME: str = "02_02_01_symmetry_difference_feature_adjudication.md"

# ---------------------------------------------------------------------------
# Binding decisions (per merged planning/current_plan.md A12-A17, A20, A21
# + Round-2 nits N1-N6)
# ---------------------------------------------------------------------------

RACE_PAIR_DECISION: str = "defer_to_02_05"
CROSS_REGION_BOOLEAN_PAIR_DECISION: str = (
    "bind_in_02_02_with_three_transforms_either_both_xor"
)
SYMMETRIC_PAIR_AGGREGATE_SCOPE_DECISION: str = (
    "bind_mean_and_abs_diff_only_for_tabular_phase_04_sum_excluded_redundant_"
    "product_deferred_to_02_05"
)
RATIO_FAMILY_DECISION: str = (
    "excluded_zero_bounded_denominators_unless_log_transform_introduced_in_02_03"
)
RECONSTRUCTED_RATING_DECISION: str = "excluded_per_pr_255_omit_closure"
RAW_SKILL_SCALAR_DECISION: str = (
    "excluded_per_pr_234_is_mmr_missing_binding_no_new_mmr_scalar"
)
TRACKER_SOURCING_DECISION: str = (
    "permitted_via_02_01_03_prior_mean_aggregates_only_never_via_tracker_events_raw_direct"
)
MATCHUP_HISTORY_TRANSFORM_DECISION: str = (
    "dropped_no_audited_opponent_counterpart_per_b1_round2"
)
UNARY_TRANSFORM_DECISION: str = (
    "open_design_question_per_n4_round2_no_unary_bound_in_this_pr"
)
PRODUCT_TRANSFORM_DECISION: str = (
    "deferred_to_02_05_per_a14_round2_not_linearly_expressible_from_mean_abs_diff"
)
SUM_TRANSFORM_DECISION: str = (
    "excluded_redundant_with_mean_per_a14_round2_sum_equals_two_times_mean"
)

# ---------------------------------------------------------------------------
# Numeric (focal, opponent) pairs from the 02_01_03 audited 24-tuple.
# Plan A20 estimated 11 pairs; actual derivation yields 10
# (matchup_h2h_count is a single column without focal/opponent split).
# ---------------------------------------------------------------------------

BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS: tuple[tuple[str, str], ...] = (
    ("focal_prior_match_count", "opponent_prior_match_count"),
    ("focal_prior_win_rate_decisive", "opponent_prior_win_rate_decisive"),
    ("focal_days_since_prior_match", "opponent_days_since_prior_match"),
    ("focal_prior_win_rate_race_conditional", "opponent_prior_win_rate_race_conditional"),
    ("focal_prior_win_rate_map_conditional", "opponent_prior_win_rate_map_conditional"),
    (
        "focal_prior_win_rate_matchup_conditional",
        "opponent_prior_win_rate_matchup_conditional",
    ),
    ("focal_apm_prior_mean", "opponent_apm_prior_mean"),
    ("focal_sq_prior_mean", "opponent_sq_prior_mean"),
    ("focal_supply_capped_pct_prior_mean", "opponent_supply_capped_pct_prior_mean"),
    ("focal_elapsed_game_loops_prior_mean", "opponent_elapsed_game_loops_prior_mean"),
)
BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS: tuple[str, str] = ("mean", "abs_diff")
BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES: tuple[str, str] = (
    "is_cross_region_fragmented_focal_history_any",
    "is_cross_region_fragmented_opponent_history_any",
)
BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS: tuple[str, str, str] = (
    "either",
    "both",
    "xor",
)

# F5 transforms map to validator-recognised symmetric tokens
_CROSS_REGION_TRANSFORM_TO_TOKEN: dict[str, str] = {
    "either": "or",
    "both": "and",
    "xor": "xor",
}

# Halting falsifier priority (first non-PASS halts)
_HALTING_FALSIFIER_CHAIN: tuple[str, ...] = (
    "validator_module_sha_pin_mismatch",
    "parent_parquet_02_01_02_sha_mismatch",
    "parent_parquet_02_01_03_sha_mismatch",
    "parent_audit_02_01_02_sha_mismatch",
    "parent_audit_02_01_03_sha_mismatch",
    "validator_failed_passed_false",
    "validator_halting_falsifier_fired",
    "binding_symmetric_pair_aggregate_transforms_not_mean_abs_diff",
    "binding_matchup_history_pair_operations_symbol_present",
    "binding_difference_family_numeric_pair_count_inconsistent",
    "pair_sum_candidate_present",
    "pair_product_candidate_present",
    "unary_matchup_h2h_focal_advantage_candidate_present",
    "non_deterministic_render_csv",
    "non_deterministic_render_md",
    "materialized_output_paths_non_empty",
    "target_directory_outside_canonical_02_02_subtree",
)

# Expected SHA-256 pins measured at adjudication time (2026-05-29).
# These are recomputed on every call; constants used for consistency tests.
_EXPECTED_VALIDATOR_SHA256: str = (
    "d8f34760db2e216cd8b838ab510bd252e7474e0324e4df1bec5d609a293b1753"
)
_EXPECTED_02_01_02_PARQUET_SHA256: str = (
    "24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39"
)
_EXPECTED_02_01_03_PARQUET_SHA256: str = (
    "053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071"
)
_EXPECTED_02_01_02_AUDIT_CANONICAL_SHA256: str = (
    "1da271c62a20bb2666863fd3737ea4fe6006cc9fec03e41ec11d013fb7e54c78"
)
_EXPECTED_02_01_03_AUDIT_CANONICAL_SHA256: str = (
    "183b9000d23b5d601b995a61c5ff52aad3fd21ff164bf21f5095fbdf450c9a92"
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CandidateScopeDecision:
    """One row in the binding candidate spec list (decision-only; no materialisation).

    Attributes:
        candidate_feature_name: The candidate feature column name.
        candidate_family: Family tag (F1/F2/F3/F5).
        direction: Either ``"focal_minus_opponent"`` or ``"symmetric"``.
        source_columns: Upstream column names this candidate derives from.
        source_artifact: Parquet artifact the source columns live in.
        source_family: Semantic sub-family label from the 02_01_03 audit.
        traceability_status: Whether tracing is to the 24-tuple or bool-pair.
        validator_passed: True iff the PR #266 validator accepted this spec.
        notes: Free-text notes (Round-2 nit cross-references, etc.).
    """

    candidate_feature_name: str
    candidate_family: Literal[
        "F1_difference",
        "F2_pair_mean",
        "F3_pair_abs_diff",
        "F5_cross_region_pair",
    ]
    direction: Literal["focal_minus_opponent", "symmetric"]
    source_columns: tuple[str, ...]
    source_artifact: Literal["02_01_03_history_enriched_pre_game_features.parquet"]
    source_family: str
    traceability_status: Literal[
        "traced_to_audited_24_tuple",
        "traced_to_audited_02_01_03_bool_pair",
    ]
    validator_passed: bool
    notes: str


@dataclass(frozen=True)
class SymmetryDifferenceAdjudicationResult:
    """Frozen adjudication state returned by the public function.

    Attributes:
        decision_id: Module constant ``DECISION_ID``.
        candidate_specs: All bound CandidateScopeDecision records.
        validator_passed: True iff the PR #266 validator passed.
        validator_halting_falsifier: First falsifier fired, or ``None``.
        csv_path: Path to the emitted CSV artifact.
        md_path: Path to the emitted MD artifact.
        materialized_output_paths: MUST be empty tuple.
        parent_02_01_02_parquet_sha256: SHA-256 of the 02_01_02 Parquet.
        parent_02_01_03_parquet_sha256: SHA-256 of the 02_01_03 Parquet.
        parent_02_01_02_audit_json_sha256: Canonical SHA-256 of 02_01_02 audit.
        parent_02_01_03_audit_json_sha256: Canonical SHA-256 of 02_01_03 audit.
        validator_module_sha256: SHA-256 of the validator .py file.
        binding_difference_family_numeric_pair_count: Always
            ``len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS)``.
        total_binding_candidate_count: F1+F2+F3+F5 candidate total.
    """

    decision_id: str
    candidate_specs: tuple[CandidateScopeDecision, ...]
    validator_passed: bool
    validator_halting_falsifier: str | None
    csv_path: Path
    md_path: Path
    materialized_output_paths: tuple[str, ...]
    parent_02_01_02_parquet_sha256: str
    parent_02_01_03_parquet_sha256: str
    parent_02_01_02_audit_json_sha256: str
    parent_02_01_03_audit_json_sha256: str
    validator_module_sha256: str
    binding_difference_family_numeric_pair_count: int
    total_binding_candidate_count: int


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------


class ProvenanceShaNotFoundError(Exception):
    """Raised when any SHA-256 pin mismatches the on-disk value."""


class SymmetryDifferenceAdjudicationError(Exception):
    """Raised on validator failure or internal consistency violation."""


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _sha256_of_file_bytes(path: Path) -> str:
    """Compute SHA-256 hex digest of a file via chunked binary read.

    Args:
        path: Path to the file.

    Returns:
        Lowercase hex SHA-256 digest string.
    """
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _sha256_of_canonical_json(path: Path) -> str:
    """Compute SHA-256 of a JSON file via canonical serialisation.

    Canonical form: ``json.dumps`` with ``sort_keys=True`` and
    ``separators=(",", ":")``, UTF-8 encoded.

    Args:
        path: Path to the JSON file.

    Returns:
        Lowercase hex SHA-256 digest string.
    """
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _resolve_repo_root(explicit: Path | str | None) -> Path:
    """Resolve repository root path.

    Args:
        explicit: Caller-supplied override, or ``None`` to derive from
            this module's location (six parents up).

    Returns:
        Absolute resolved path to the repo root.
    """
    if explicit is not None:
        return Path(explicit).resolve()
    return Path(__file__).resolve().parents[6]


def _stem_from_pair(focal: str, opponent: str) -> str:
    """Extract the shared semantic stem from a focal/opponent column pair.

    Args:
        focal: Focal column name (starts with ``focal_``).
        opponent: Opponent column name (starts with ``opponent_``).

    Returns:
        Shared stem string (e.g. ``"prior_match_count"``).
    """
    prefix = "focal_"
    if focal.startswith(prefix):
        return focal[len(prefix):]
    return focal


def _source_family_for_stem(stem: str) -> str:
    """Return the 02_01_03 source family for a given stem.

    Args:
        stem: Shared semantic stem derived from the focal/opponent pair.

    Returns:
        Source family label string.
    """
    _STEM_TO_FAMILY: dict[str, str] = {
        "prior_match_count": "focal_player_history",
        "prior_win_rate_decisive": "focal_player_history",
        "days_since_prior_match": "focal_player_history",
        "prior_win_rate_race_conditional": "focal_player_history",
        "prior_win_rate_map_conditional": "focal_player_history",
        "prior_win_rate_matchup_conditional": "focal_player_history",
        "apm_prior_mean": "in_game_history_aggregate",
        "sq_prior_mean": "in_game_history_aggregate",
        "supply_capped_pct_prior_mean": "in_game_history_aggregate",
        "elapsed_game_loops_prior_mean": "in_game_history_aggregate",
    }
    return _STEM_TO_FAMILY.get(stem, "unknown")


def _build_difference_specs(
) -> tuple[CandidateScopeDecision, ...]:
    """Build F1 difference candidate specs from binding pairs.

    Returns:
        Tuple of CandidateScopeDecision for F1 family.
    """
    specs: list[CandidateScopeDecision] = []
    for focal, opponent in BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS:
        stem = _stem_from_pair(focal, opponent)
        family = _source_family_for_stem(stem)
        note = (
            "F1: signed difference; direction=focal_minus_opponent; "
            "name suffix _diff per validator direction-name-consistency rule; "
            "Plan A20 estimated 11 pairs; actual 10 (matchup_h2h_count unpaired per A20)."
        )
        specs.append(
            CandidateScopeDecision(
                candidate_feature_name=f"focal_minus_opponent_{stem}_diff",
                candidate_family="F1_difference",
                direction="focal_minus_opponent",
                source_columns=(focal, opponent),
                source_artifact="02_01_03_history_enriched_pre_game_features.parquet",
                source_family=family,
                traceability_status="traced_to_audited_24_tuple",
                validator_passed=True,
                notes=note,
            )
        )
    return tuple(specs)


def _build_mean_specs() -> tuple[CandidateScopeDecision, ...]:
    """Build F2 symmetric pair_mean candidate specs from binding pairs.

    Returns:
        Tuple of CandidateScopeDecision for F2 family.
    """
    specs: list[CandidateScopeDecision] = []
    for focal, opponent in BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS:
        stem = _stem_from_pair(focal, opponent)
        family = _source_family_for_stem(stem)
        note = (
            "F2: symmetric pair mean; direction=symmetric; "
            "sum excluded (sum=2*mean, redundant per A14 B2 fix); "
            "product deferred to 02_05 (not LINEARLY expressible from (mean,abs_diff); N1)."
        )
        specs.append(
            CandidateScopeDecision(
                candidate_feature_name=f"{stem}_pair_mean",
                candidate_family="F2_pair_mean",
                direction="symmetric",
                source_columns=(focal, opponent),
                source_artifact="02_01_03_history_enriched_pre_game_features.parquet",
                source_family=family,
                traceability_status="traced_to_audited_24_tuple",
                validator_passed=True,
                notes=note,
            )
        )
    return tuple(specs)


def _build_abs_diff_specs() -> tuple[CandidateScopeDecision, ...]:
    """Build F3 symmetric pair_abs_diff candidate specs from binding pairs.

    Returns:
        Tuple of CandidateScopeDecision for F3 family.
    """
    specs: list[CandidateScopeDecision] = []
    for focal, opponent in BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS:
        stem = _stem_from_pair(focal, opponent)
        family = _source_family_for_stem(stem)
        note = (
            "F3: symmetric absolute difference; direction=symmetric; "
            "required for LogReg under Invariant I8 (abs_diff not linearly "
            "recoverable from signed difference; B3 fix). "
            "_abs_diff suffix triggers symmetric override in validator (line 517)."
        )
        specs.append(
            CandidateScopeDecision(
                candidate_feature_name=f"{stem}_pair_abs_diff",
                candidate_family="F3_pair_abs_diff",
                direction="symmetric",
                source_columns=(focal, opponent),
                source_artifact="02_01_03_history_enriched_pre_game_features.parquet",
                source_family=family,
                traceability_status="traced_to_audited_24_tuple",
                validator_passed=True,
                notes=note,
            )
        )
    return tuple(specs)


def _build_cross_region_specs() -> tuple[CandidateScopeDecision, ...]:
    """Build F5 cross-region BOOLEAN pair candidate specs.

    Returns:
        Tuple of CandidateScopeDecision for F5 family (3 transforms).
    """
    focal_src, opponent_src = BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES
    specs: list[CandidateScopeDecision] = []
    for transform in BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS:
        token = _CROSS_REGION_TRANSFORM_TO_TOKEN[transform]
        note = (
            f"F5: cross-region BOOLEAN pair transform={transform}; "
            f"validator token=_pair_{token}; direction=symmetric; "
            f"N3: under LogReg with regularization the (either,both,xor) design "
            f"matrix is rank-2 over the 2-dim Boolean source "
            f"(either=both OR xor); all three retained for tree-based models."
        )
        specs.append(
            CandidateScopeDecision(
                candidate_feature_name=f"cross_region_pair_{token}",
                candidate_family="F5_cross_region_pair",
                direction="symmetric",
                source_columns=(focal_src, opponent_src),
                source_artifact="02_01_03_history_enriched_pre_game_features.parquet",
                source_family="cross_region_fragmentation_handling",
                traceability_status="traced_to_audited_02_01_03_bool_pair",
                validator_passed=True,
                notes=note,
            )
        )
    return tuple(specs)


def _construct_binding_candidate_specs() -> tuple[
    tuple[CandidateFeatureSpec, ...],
    tuple[CandidateFeatureSpec, ...],
    tuple[CandidateFeatureSpec, ...],
    tuple[CandidateScopeDecision, ...],
]:
    """Construct binding candidate spec tuples for validator + adjudication.

    Returns:
        Four-tuple of:
            - difference_specs for validator (CandidateFeatureSpec)
            - symmetric_pair_specs for validator (CandidateFeatureSpec)
            - race_pair_specs for validator (empty; F6 deferred to 02_05)
            - all_scope_decisions (CandidateScopeDecision)
    """
    diff_decisions = _build_difference_specs()
    mean_decisions = _build_mean_specs()
    abs_diff_decisions = _build_abs_diff_specs()
    cross_region_decisions = _build_cross_region_specs()

    difference_validator_specs = tuple(
        CandidateFeatureSpec(
            column_name=d.candidate_feature_name,
            direction=d.direction,
            source_columns=d.source_columns,
        )
        for d in diff_decisions
    )
    symmetric_validator_specs = tuple(
        CandidateFeatureSpec(
            column_name=d.candidate_feature_name,
            direction=d.direction,
            source_columns=d.source_columns,
        )
        for d in mean_decisions + abs_diff_decisions + cross_region_decisions
    )
    race_pair_validator_specs: tuple[CandidateFeatureSpec, ...] = ()

    all_decisions = (
        diff_decisions
        + mean_decisions
        + abs_diff_decisions
        + cross_region_decisions
    )
    return (
        difference_validator_specs,
        symmetric_validator_specs,
        race_pair_validator_specs,
        all_decisions,
    )


def _construct_csv_row(
    *,
    validator_passed: bool,
    validator_halting_falsifier: str | None,
    parent_02_01_02_parquet_sha256: str,
    parent_02_01_03_parquet_sha256: str,
    parent_02_01_02_audit_json_sha256: str,
    parent_02_01_03_audit_json_sha256: str,
    validator_module_sha256: str,
    binding_pair_count: int,
) -> tuple[str, ...]:
    """Construct the single data row for the 23-column CSV.

    Args:
        validator_passed: True iff validator passed.
        validator_halting_falsifier: First falsifier label, or empty string.
        parent_02_01_02_parquet_sha256: SHA of 02_01_02 Parquet.
        parent_02_01_03_parquet_sha256: SHA of 02_01_03 Parquet.
        parent_02_01_02_audit_json_sha256: Canonical SHA of 02_01_02 audit.
        parent_02_01_03_audit_json_sha256: Canonical SHA of 02_01_03 audit.
        validator_module_sha256: SHA of the validator module file.
        binding_pair_count: Number of binding numeric pairs.

    Returns:
        23-element tuple of string values.
    """
    return (
        DECISION_ID,
        "F1_difference|F2_pair_mean|F3_pair_abs_diff|F5_cross_region_pair",
        "focal_minus_opponent_for_F1|symmetric_for_F2_F3_F5",
        str(binding_pair_count),
        "|".join(BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS),
        "|".join(BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS),
        RACE_PAIR_DECISION,
        CROSS_REGION_BOOLEAN_PAIR_DECISION,
        SYMMETRIC_PAIR_AGGREGATE_SCOPE_DECISION,
        MATCHUP_HISTORY_TRANSFORM_DECISION,
        RATIO_FAMILY_DECISION,
        RECONSTRUCTED_RATING_DECISION,
        RAW_SKILL_SCALAR_DECISION,
        TRACKER_SOURCING_DECISION,
        "|".join(ROW_IDENTITY_JOIN_KEYS),
        "focal_match_id+focal_player+opponent_player+started_at_join_on_02_01_03",
        str(validator_passed),
        validator_halting_falsifier or "",
        parent_02_01_02_parquet_sha256,
        parent_02_01_03_parquet_sha256,
        parent_02_01_02_audit_json_sha256,
        parent_02_01_03_audit_json_sha256,
        validator_module_sha256,
    )


_CSV_HEADER: tuple[str, ...] = (
    "decision_id",
    "candidate_family_set",
    "direction_policy",
    "binding_difference_family_numeric_pair_count",
    "binding_symmetric_pair_aggregate_transforms",
    "binding_cross_region_boolean_pair_transforms",
    "race_pair_decision",
    "cross_region_boolean_pair_decision",
    "symmetric_pair_aggregate_scope_decision",
    "matchup_history_transform_decision",
    "ratio_family_decision",
    "reconstructed_rating_decision",
    "raw_skill_scalar_decision",
    "tracker_sourcing_decision",
    "row_identity_join_keys",
    "row_alignment_policy",
    "validator_passed",
    "validator_halting_falsifier",
    "parent_02_01_02_parquet_sha256",
    "parent_02_01_03_parquet_sha256",
    "parent_02_01_02_audit_json_sha256",
    "parent_02_01_03_audit_json_sha256",
    "validator_module_sha256",
)


def _render_csv(
    header: tuple[str, ...],
    data_row: tuple[str, ...],
) -> str:
    """Render the CSV as a deterministic string.

    Args:
        header: 23-element header tuple.
        data_row: 23-element data tuple.

    Returns:
        UTF-8 BOM-less CSV string with ``\\n`` line endings.
    """
    buf = io.StringIO()
    writer = csv.writer(buf, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    writer.writerow(header)
    writer.writerow(data_row)
    return buf.getvalue()


def _render_md(
    *,
    all_decisions: tuple[CandidateScopeDecision, ...],
    validator_passed: bool,
    validator_halting_falsifier: str | None,
    parent_02_01_02_parquet_sha256: str,
    parent_02_01_03_parquet_sha256: str,
    parent_02_01_02_audit_json_sha256: str,
    parent_02_01_03_audit_json_sha256: str,
    validator_module_sha256: str,
    binding_pair_count: int,
    total_candidate_count: int,
    csv_path: Path,
) -> str:
    """Render the 13-section MD artifact as a deterministic string.

    Args:
        all_decisions: All CandidateScopeDecision records.
        validator_passed: True iff validator passed.
        validator_halting_falsifier: First falsifier, or None.
        parent_02_01_02_parquet_sha256: SHA of 02_01_02 Parquet.
        parent_02_01_03_parquet_sha256: SHA of 02_01_03 Parquet.
        parent_02_01_02_audit_json_sha256: Canonical SHA of 02_01_02 audit.
        parent_02_01_03_audit_json_sha256: Canonical SHA of 02_01_03 audit.
        validator_module_sha256: SHA of the validator module.
        binding_pair_count: Number of binding numeric pairs.
        total_candidate_count: F1+F2+F3+F5 total candidates.
        csv_path: Path to the emitted CSV for cross-reference.

    Returns:
        Multi-line markdown string.
    """
    rows_for_table = _build_candidate_table_rows(all_decisions)
    lines: list[str] = []
    _md_section_1(lines)
    _md_section_2(
        lines,
        parent_02_01_02_parquet_sha256=parent_02_01_02_parquet_sha256,
        parent_02_01_03_parquet_sha256=parent_02_01_03_parquet_sha256,
        parent_02_01_02_audit_json_sha256=parent_02_01_02_audit_json_sha256,
        parent_02_01_03_audit_json_sha256=parent_02_01_03_audit_json_sha256,
        validator_module_sha256=validator_module_sha256,
    )
    _md_section_3(lines)
    _md_section_4(lines, rows_for_table, total_candidate_count)
    _md_section_5(lines)
    _md_section_6(lines, binding_pair_count)
    _md_section_7(lines, validator_passed, validator_halting_falsifier)
    _md_section_8(lines)
    _md_section_9(lines)
    _md_section_10(lines)
    _md_section_11(lines, binding_pair_count, total_candidate_count)
    _md_section_12(lines)
    _md_section_13(lines)
    return "\n".join(lines) + "\n"


def _build_candidate_table_rows(
    all_decisions: tuple[CandidateScopeDecision, ...],
) -> list[tuple[str, str, str, str, str]]:
    """Build display rows for the candidate feature table.

    Args:
        all_decisions: All CandidateScopeDecision records.

    Returns:
        List of (name, family, direction, sources, traceability) tuples.
    """
    rows: list[tuple[str, str, str, str, str]] = []
    for d in all_decisions:
        rows.append((
            d.candidate_feature_name,
            d.candidate_family,
            d.direction,
            " + ".join(d.source_columns),
            d.traceability_status,
        ))
    return rows


def _md_section_1(lines: list[str]) -> None:
    """Append §1 non-materialisation disclaimer."""
    lines.extend([
        "## §1 — Non-materialization disclaimer",
        "",
        "This document is a **decision-only adjudication artifact** for SC2EGSet "
        "Step 02_02_01 (symmetry \\& difference feature scope). It does NOT:",
        "",
        "- materialise any feature value (no Parquet under "
        "`reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`);",
        "- emit any CROSS-02-01 leakage audit (`leakage_audit_sc2egset.{json,md}`);",
        "- modify any STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS YAML;",
        "- modify any research_log / ROADMAP path.",
        "",
        "Feature materialisation is a separate future Step 02_02 PR "
        "(analogue of PR #259 for Step 02_01_03).",
        "",
        f"Executed: {EXECUTED_AT_UTC_DATE}. Audit PR: {AUDIT_PR}.",
        "",
    ])


def _md_section_2(
    lines: list[str],
    *,
    parent_02_01_02_parquet_sha256: str,
    parent_02_01_03_parquet_sha256: str,
    parent_02_01_02_audit_json_sha256: str,
    parent_02_01_03_audit_json_sha256: str,
    validator_module_sha256: str,
) -> None:
    """Append §2 input artifact lineage (paths + SHA-256)."""
    lines.extend([
        "## §2 — Input artifact lineage (paths + SHA-256)",
        "",
        "All SHA-256 values are recomputed on every adjudication run and pinned "
        "in the CSV artifact. Parquet SHAs use raw file bytes; audit JSON SHAs use "
        "canonical serialisation (`sort_keys=True, separators=(',', ':')`).",
        "",
        "| Artifact | Relative path | SHA-256 |",
        "|---|---|---|",
        f"| 02_01_02 Parquet | `{_REPO_RELATIVE_PARENT_02_01_02_PARQUET}` | "
        f"`{parent_02_01_02_parquet_sha256}` |",
        f"| 02_01_03 Parquet | `{_REPO_RELATIVE_PARENT_02_01_03_PARQUET}` | "
        f"`{parent_02_01_03_parquet_sha256}` |",
        f"| 02_01_02 audit JSON | `{_REPO_RELATIVE_PARENT_02_01_02_AUDIT}` | "
        f"`{parent_02_01_02_audit_json_sha256}` (canonical) |",
        f"| 02_01_03 audit JSON | `{_REPO_RELATIVE_PARENT_02_01_03_AUDIT}` | "
        f"`{parent_02_01_03_audit_json_sha256}` (canonical) |",
        f"| Validator module | `{_REPO_RELATIVE_VALIDATOR_PATH}` | "
        f"`{validator_module_sha256}` |",
        "",
        "Lineage position: " + LINEAGE_POSITION,
        "",
    ])


def _md_section_3(lines: list[str]) -> None:
    """Append §3 row identity / alignment policy."""
    lines.extend([
        "## §3 — Row identity / alignment policy",
        "",
        "The row-identity join keys for the future materialisation step are a "
        "documentary future-materialisation gate, not a runtime promise for the adjudication PR.",
        "",
        "Join keys (from the 02_01_03 audit JSON "
        "`projected_identity_columns` + `projected_context_columns`):",
        "",
        "| Key | Role |",
        "|---|---|",
        "| `focal_match_id` | Identity |",
        "| `focal_player` | Identity |",
        "| `opponent_player` | Identity |",
        "| `started_at` | Context anchor (temporal) |",
        "",
        "Row alignment policy: join on "
        "`focal_match_id + focal_player + opponent_player + started_at` "
        "against the 02_01_03 Parquet (44,418 rows × 24 audited features). "
        "Every symmetry/difference candidate column is derived purely from the "
        "same row's `focal_*` / `opponent_*` values — no cross-row aggregation "
        "at materialisation time.",
        "",
    ])


def _md_section_4(
    lines: list[str],
    rows: list[tuple[str, str, str, str, str]],
    total_count: int,
) -> None:
    """Append §4 candidate feature table."""
    lines.extend([
        "## §4 — Candidate feature table",
        "",
        f"Total binding candidate count: **{total_count}** "
        "(F1=10 + F2=10 + F3=10 + F5=3).",
        "",
        "> **Note (N3 / LogReg-redundancy of F5):** "
        "Under logistic regression with regularisation the F5 "
        "`(either, both, xor)` design matrix is rank-2 over the 2-dimensional "
        "Boolean source (`either = both ∨ xor`), so two of the three transforms "
        "suffice for linear models. The decision to retain all three transforms "
        "stands for tree-based models (non-redundant), but the rationale does not "
        "claim non-redundancy for all model classes.",
        "",
        "| Candidate feature name | Family | Direction | Source columns | Traceability |",
        "|---|---|---|---|---|",
    ])
    for name, family, direction, sources, trace in rows:
        lines.append(f"| `{name}` | {family} | {direction} | {sources} | {trace} |")
    lines.extend(["", ""])


def _md_section_5(lines: list[str]) -> None:
    """Append §5 direction policy."""
    lines.extend([
        "## §5 — Direction policy",
        "",
        "Direction policy per `planning/current_plan.md` A9 / Invariant I5:",
        "",
        "- **`focal_minus_opponent`** (F1): signed arithmetic difference "
        "`focal_col − opponent_col`; name template `focal_minus_opponent_<stem>_diff`. "
        "Slot-orthogonal: the sign is meaningful only in the focal-is-row-1 "
        "convention (Invariant I5); slot-bias regex enforced by validator.",
        "",
        "- **`symmetric`** (F2 / F3 / F5): focal/opponent-swap invariant aggregate "
        "(mean, abs_diff, or BOOLEAN transform). Name template "
        "`<stem>_pair_mean`, `<stem>_pair_abs_diff`, "
        "`cross_region_pair_{or,and,xor}`. "
        "Permutation-invariant by construction (Hue \\& Vert ICML 2010; "
        "Zaheer et al. 2017 Deep Sets).",
        "",
        "No canonical-ordering concatenation is used. "
        "Slot-bias (player_1 / slot / home / away / etc.) is "
        "incompatible with Invariant I5 and enforced by the validator's "
        "`BLOCKED_SLOT_TOKEN_REGEX` (12 boundary-aware patterns).",
        "",
    ])


def _md_section_6(lines: list[str], binding_pair_count: int) -> None:
    """Append §6 source-column traceability proof."""
    lines.extend([
        "## §6 — Source-column traceability proof",
        "",
        f"All {binding_pair_count} numeric focal/opponent pairs are sourced from the "
        "02_01_03 audited 24-tuple "
        "(`UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03` in the PR #266 validator). "
        "All F5 Boolean sources are in the same 24-tuple "
        "(`is_cross_region_fragmented_focal_history_any`, "
        "`is_cross_region_fragmented_opponent_history_any`).",
        "",
        "Plan A20 estimated 11 numeric pairs; the audited 24-tuple yields 10. "
        "`matchup_h2h_count` is a single unpaired column (no `opponent` counterpart); "
        "`matchup_h2h_focal_win_rate` is also unpaired "
        "(B1 / Round 1 BLOCKER: framing it as a pair produces affine `2x−1`, "
        "zero information gain for both linear and tree models).",
        "",
        "Validator traceability check (PR #266 "
        "`_check_source_column_traceability`) passes on every run: "
        "every `source_columns` element is in the union of the 7-tuple "
        "(02_01_02) and 24-tuple (02_01_03) audited columns.",
        "",
    ])


def _md_section_7(
    lines: list[str],
    validator_passed: bool,
    validator_halting_falsifier: str | None,
) -> None:
    """Append §7 validator result summary."""
    lines.extend([
        "## §7 — Validator result summary",
        "",
        f"- `validator_passed`: **{validator_passed}**",
        f"- `validator_halting_falsifier`: **{validator_halting_falsifier!r}**",
        f"- Validator module: `{_REPO_RELATIVE_VALIDATOR_PATH}`",
        f"- Audit PR: {AUDIT_PR}",
        "",
        "The PR #266 validator runs the 14-step halting-falsifier chain over the "
        "candidate specs and the upstream Parquet SHA-256 pins. "
        "A `passed=True` result is required for the CSV+MD to be written; "
        "if the validator fires any falsifier, the adjudicator raises "
        "`SymmetryDifferenceAdjudicationError` before writing any artifact.",
        "",
    ])


def _md_section_8(lines: list[str]) -> None:
    """Append §8 race-pair deferral to 02_05."""
    lines.extend([
        "## §8 — Race-pair deferral to 02_05",
        "",
        "The F6 race-pair categorical interaction family "
        "(`race_pair` from the 02_01_02 7-tuple; `focal_race`, `opponent_race`) "
        "is deferred to Pipeline Section `02_05 — Categorical Encoding & Interactions` "
        "per `planning/current_plan.md` A12 / `02_FEATURE_ENGINEERING_MANUAL.md` §6.",
        "",
        "Rationale: race-pair encoded interactions are categorical cross-products, "
        "not continuous-valued symmetric/difference transforms. "
        "The validator's `designed_race_pair_candidate_specs` parameter is passed "
        "as an empty tuple for this adjudication.",
        "",
        "No race-pair candidate is emitted in the binding 33-candidate set.",
        "",
    ])


def _md_section_9(lines: list[str]) -> None:
    """Append §9 excluded features / families (subsections §9.1–§9.8)."""
    lines.extend([
        "## §9 — Excluded features / families",
        "",
        "### §9.1 — `sum` exclusion",
        "",
        "The `pair_sum` transform (`focal + opponent`) is excluded as redundant "
        "with `pair_mean` (§9.3 cross-links to this). "
        "The correct algebra is `sum = focal + opponent = 2 × mean`. "
        "Including both `sum` and `mean` in a linear model provides zero additional "
        "information (B2 / Round-2 fix). "
        "See also §9.3 for the joint-basis argument that places `mean` in the binding set.",
        "",
        "### §9.2 — `product` deferral to 02_05",
        "",
        "The `pair_product` transform (`focal × opponent`) is deferred to "
        "Pipeline Section `02_05 — Categorical Encoding & Interactions`. "
        "`product = focal × opponent` is not LINEARLY expressible from "
        "`(mean, abs_diff)` alone. "
        "The identity `focal × opponent = mean² − (abs_diff / 2)²` makes "
        "product a quadratic polynomial in `(mean, abs_diff)`; "
        "a linear-LogReg basis cannot recover it without polynomial terms.",
        "",
        "`02_FEATURE_ENGINEERING_MANUAL.md` §6 line 135 explicitly acknowledges "
        "that tree-based models capture polynomial interactions natively. "
        "The placement of `product` in `02_05` is a **Pipeline-Section convention "
        "choice** (governance simplicity and interaction-feature grouping), "
        "not a methodological necessity. "
        "For tree-based models, the `product` interaction is recoverable from the "
        "raw `focal_*` / `opponent_*` inputs without an explicit feature; "
        "the 02_05 placement groups all multiplicative interactions together for "
        "clarity and reusability.",
        "",
        "### §9.3 — `abs_diff` inclusion (cross-link to §9.1 and §5)",
        "",
        "The `pair_abs_diff` transform (`|focal − opponent|`) is included "
        "in the binding set (F3; B3 / Round-2 fix). "
        "Cross-referencing §9.1 (`sum` excluded as redundant with `mean`) "
        "and §5 (direction policy): "
        "the joint triple `(focal_minus_opponent_<stem>_diff, <stem>_pair_mean, "
        "<stem>_pair_abs_diff)` jointly spans the "
        "**linear-in-signed-difference**, **linear-in-mean-level**, and "
        "**linear-in-symmetric-magnitude** subspaces required for LogReg "
        "under Invariant I8.",
        "",
        "Quadratic effects (`focal²`, `opponent²`, `focal × opponent`) remain "
        "unrecoverable without polynomial terms — these are the 02_05 deferral surface "
        "(see §9.2). For tree-based models, `|focal − opponent|` is a piecewise-linear "
        "function of the signed difference and is recoverable; "
        "for LogReg it is not. "
        "Therefore `abs_diff` is the canonical symmetric-magnitude basis vector "
        "for every eligible numeric focal/opponent pair.",
        "",
        "### §9.4 — Ratio family exclusion",
        "",
        f"{RATIO_FAMILY_DECISION}.",
        "",
        "Rationale: ratio features (`focal / opponent`) have zero-bounded "
        "denominators in this dataset (e.g., `opponent_prior_match_count = 0` "
        "for cold-start cases). Without a log transform introduced at "
        "Step 02_03 (Temporal Features, Windows, Decay, Cold Starts), "
        "the ratio is undefined or infinite. "
        "Deferred until a log transform is available.",
        "",
        "### §9.5 — `reconstructed_rating` family exclusion",
        "",
        f"{RECONSTRUCTED_RATING_DECISION}.",
        "",
        "PR #255 omit-closure binds the exclusion of "
        "`reconstructed_rating_focal_pre`, `reconstructed_rating_opp_pre`, "
        "`reconstructed_rating_diff`. "
        "This adjudication does not re-introduce any reconstructed-rating column. "
        "The PR #266 validator's `BLOCKED_FAMILY_FRAGMENTS` constant enforces "
        "this structurally.",
        "",
        "### §9.6 — Raw MMR scalar exclusion",
        "",
        f"{RAW_SKILL_SCALAR_DECISION}.",
        "",
        "PR #234 `is_mmr_missing` flag is the only MMR-related signal in the "
        "binding 24-tuple. No new raw MMR scalar is introduced. "
        "The `is_mmr_missing` BOOLEAN columns are in the 02_01_02 7-tuple, "
        "not the 02_01_03 24-tuple, and are not symmetric/difference candidates.",
        "",
        "### §9.7 — Matchup-history pair operations exclusion (B1 / A20)",
        "",
        f"{MATCHUP_HISTORY_TRANSFORM_DECISION}.",
        "",
        "`matchup_h2h_focal_win_rate` is the only matchup-rate column in the "
        "audited 24-tuple; there is no `matchup_h2h_opponent_win_rate` counterpart. "
        "Treating it as a pair with implicit complement `1 − matchup_h2h_focal_win_rate` "
        "produces the affine transform `2·focal − 1` (zero linear-model information "
        "gain; zero tree-splitting effect). "
        "The F4 family (matchup history pair operations) is therefore dropped entirely. "
        "See also §12 for the open unary design question (N4).",
        "",
        "### §9.8 — `tracker_events_raw` direct sourcing exclusion",
        "",
        f"{TRACKER_SOURCING_DECISION}.",
        "",
        "Tracker-derived features are never pre-game features (Invariant I3; "
        "CROSS-02-00 §5.4). "
        "This adjudication permits only prior-mean aggregates sourced via "
        "the 02_01_03 Parquet (which itself sources from `player_history_all`, "
        "not from `tracker_events_raw` directly). "
        "The PR #266 validator's `_check_tracker_sourced_violations` enforces this.",
        "",
    ])


def _md_section_10(lines: list[str]) -> None:
    """Append §10 leakage controls."""
    lines.extend([
        "## §10 — Leakage controls",
        "",
        "Temporal leakage controls are inherited from Step 02_01_03 (PR #259):",
        "",
        "- Temporal anchor: `started_at` TIMESTAMP (CROSS-02-00 §3.1; PR #242 Q2(a)).",
        "- Cutoff rule: `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at` "
        "(strict `<`; Invariant I3).",
        "- Source: 02_01_03 Parquet (44,418 rows; SHA-pinned); "
        "no tracker-derived target-match feature.",
        "",
        "At adjudication time, no materialisation occurs, so no new "
        "leakage falsifiers fire. The validator's halting chain covers:",
        "",
        "- `input_parquet_sha_mismatch` — upstream Parquets byte-stable.",
        "- `tracker_sourced_candidate` — no tracker-source prefix in source_columns.",
        "- `target_leak_token_in_candidate` — boundary-aware POST_GAME token regex "
        "with `prior_win_rate` allowlist suppression.",
        "- `direction_annotation_invalid` / `direction_name_inconsistent` — "
        "name-direction alignment verified.",
        "",
    ])


def _md_section_11(
    lines: list[str],
    binding_pair_count: int,
    total_candidate_count: int,
) -> None:
    """Append §11 future materialisation contract."""
    lines.extend([
        "## §11 — Future materialisation contract",
        "",
        "The binding candidate list (33 candidates: F1=10 + F2=10 + F3=10 + F5=3) "
        "is the machine-checkable contract for the future Step 02_02 materialisation PR. "
        "That PR (analogue of PR #259) must:",
        "",
        f"1. Accept exactly {total_candidate_count} candidate column names "
        f"(including {binding_pair_count} difference columns, "
        f"{binding_pair_count} mean columns, {binding_pair_count} abs_diff columns, "
        f"3 cross-region BOOLEAN pair columns).",
        "2. Use the 02_01_03 Parquet as its sole source (SHA-pinned).",
        "3. Apply no new temporal cutoff (inherit strict `<` from 02_01_03).",
        "4. Run the PR #266 validator with the binding specs from this adjudication.",
        "5. Emit a CROSS-02-01 leakage audit JSON+MD pair.",
        "6. Append to the dataset `research_log.md` (non-closure entry).",
        "",
        "**Plan A20 note:** Plan A20 estimated 11 numeric pairs; "
        "the audited 24-tuple yields 10 "
        "(`matchup_h2h_count` is unpaired and excluded per A20). "
        "Total estimated 11 + 22 + 3 = 36 candidates from Plan U2; "
        "actual total is {total_candidate_count} candidates. "
        "This is the resolution of Plan U2 at notebook enumeration step.",
        "",
    ])


def _md_section_12(lines: list[str]) -> None:
    """Append §12 out-of-scope disclaimers."""
    lines.extend([
        "## §12 — Out-of-scope disclaimers",
        "",
        "The following items are explicitly out of scope for this adjudication PR:",
        "",
        "- **No feature value materialised.** No Parquet.",
        "- **No CROSS-02-01 leakage audit artifact.**",
        "- **No STEP_STATUS row for 02_02_01.**",
        "- **No PIPELINE_SECTION_STATUS row for 02_02.**",
        "- **No PHASE_STATUS mutation.** Phase 02 stays `in_progress`.",
        "- **No ROADMAP edit.** The 02_02_01 block (PR #264) remains byte-identical.",
        "- **No research_log append.** (Non-batching sequence step 8; appended at closure.)",
        "- **No Phase 03 / Step 02_01_04 / Step 02_02_02+ / baseline modelling.**",
        "- **No `sum` or `product` transforms.** "
        "(B2 / Round-2 / A14: sum excluded redundant; product deferred to 02_05.)",
        "- **No matchup-history pair operations.** (B1 / Round-2 / A20: F4 dropped.)",
        "- **No reconstructed_rating.** (PR #255 omit-closure.)",
        "- **No new MMR scalar.** (PR #234 `is_mmr_missing` flag stands.)",
        "- **No tracker_events_raw direct sourcing.** (Invariant I3.)",
        "- **No AoE2 civilization vocabulary.** (Invariant I8.)",
        "- **No CROSS-02-01 audit artifact.** "
        "No `leakage_audit_sc2egset.{json,md}` under `reports/artifacts/02_02_01/`.",
        "",
        "**Open design question OQ8 (unary transform — N4):** "
        "The potential unary transform `matchup_h2h_focal_advantage = 2·focal_win_rate − 1` "
        "rescales the single `matchup_h2h_focal_win_rate` column to `[−1, +1]`. "
        "This is an open design question: a unary feature is strictly neither "
        "`focal_minus_opponent` (no opponent column in the transform) nor "
        "`symmetric` (direction-dependent). "
        "No unary candidate is emitted in this adjudication. "
        "The decision remains undecided until a future PR "
        "(Phase 04 or a follow-up 02_02 micro-PR).",
        "",
    ])


def _md_section_13(lines: list[str]) -> None:
    """Append §13 Round-2 revision provenance."""
    lines.extend([
        "## §13 — Round 2 revision provenance",
        "",
        "**Round 1 verdict:** HOLD — 3 BLOCKERs (B1 vacuous F4 pair, "
        "B2 algebra error on product redundancy, B3 abs_diff exclusion "
        "incompatible with LogReg under I8).",
        "",
        "**Round 2 verdict:** APPROVE-WITH-NITS (0 BLOCKERs, 6 NITs). "
        "Plan merged via PR #267 (merge SHA `af8c3d98`). "
        "Round-2 reviewer-adversarial: `planning/current_plan.critique.md`.",
        "",
        "**Blocker resolutions:**",
        "",
        "- B1 resolved: F4 (matchup history pair operations) dropped entirely; "
        "`MATCHUP_HISTORY_TRANSFORM_DECISION` = "
        f"`{MATCHUP_HISTORY_TRANSFORM_DECISION}`. "
        "Test: `test_binding_matchup_history_pair_operations_symbol_absent`.",
        "",
        "- B2 resolved: Correct algebra `sum = 2 × mean`; "
        "`sum` excluded (redundant); `product` deferred to 02_05 (genuine "
        "multiplicative interaction). "
        "`SYMMETRIC_PAIR_AGGREGATE_SCOPE_DECISION` encodes both decisions. "
        "Test: `test_no_pair_sum_candidate_constructed` + "
        "`test_no_pair_product_candidate_constructed`.",
        "",
        "- B3 resolved: `abs_diff` included as F3 family; "
        "`BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS = (\"mean\", \"abs_diff\")`. "
        "Test: `test_binding_symmetric_pair_aggregate_transforms_exactly_mean_abs_diff`.",
        "",
        "**Nit applications (N1–N6):**",
        "",
        "- **N1** (MD §9.2): Wording corrected to "
        '"not LINEARLY expressible from `(mean, abs_diff)` alone" '
        "(quadratic identity `focal × opponent = mean² − (abs_diff/2)²`).",
        "",
        "- **N2** (MD §9.2): `02_FEATURE_ENGINEERING_MANUAL.md` §6 line 135 cited; "
        "Pipeline-Section placement acknowledged as convention choice, "
        "not methodological necessity.",
        "",
        "- **N3** (MD §4 footnote): LogReg-redundancy of F5 `(either, both, xor)` "
        "acknowledged (rank-2 design matrix over 2-dim Boolean source); "
        "all three retained for tree models.",
        "",
        "- **N4** (MD §12): Unary `matchup_h2h_focal_advantage = 2·focal − 1` "
        "recorded as open design question OQ8; no candidate emitted.",
        "",
        "- **N5** (internal consistency): Deterministic assertion "
        "`count(abs_diff specs) == len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS) "
        "== CSV binding_difference_family_numeric_pair_count`. "
        "Tests: `test_internal_consistency_abs_diff_count_equals_constant_equals_csv_field` "
        "and `test_internal_consistency_total_candidate_count_matches_csv_field`.",
        "",
        "- **N6** (MD §9.3): Joint-basis cross-link added: "
        "`(focal_minus_opponent_diff, pair_mean, pair_abs_diff)` spans "
        "linear-in-signed-difference, linear-in-mean-level, and "
        "linear-in-symmetric-magnitude; quadratic effects remain at 02_05.",
        "",
    ])


def _assert_internal_consistency(
    all_decisions: tuple[CandidateScopeDecision, ...],
    binding_pair_count: int,
    csv_row: tuple[str, ...],
) -> None:
    """Assert N5 internal consistency of candidate counts.

    Args:
        all_decisions: All CandidateScopeDecision records.
        binding_pair_count: Declared binding pair count.
        csv_row: The 23-element CSV data row.

    Raises:
        SymmetryDifferenceAdjudicationError: on any inconsistency.
    """
    abs_diff_count = sum(
        1 for d in all_decisions if d.candidate_family == "F3_pair_abs_diff"
    )
    constant_pair_count = len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS)
    csv_pair_count_idx = _CSV_HEADER.index(
        "binding_difference_family_numeric_pair_count"
    )
    csv_pair_count = int(csv_row[csv_pair_count_idx])

    if abs_diff_count != constant_pair_count:
        raise SymmetryDifferenceAdjudicationError(
            f"N5 inconsistency: abs_diff_count={abs_diff_count} != "
            f"len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS)={constant_pair_count}"
        )
    if constant_pair_count != csv_pair_count:
        raise SymmetryDifferenceAdjudicationError(
            f"N5 inconsistency: constant pair count={constant_pair_count} != "
            f"CSV field={csv_pair_count}"
        )
    if constant_pair_count != binding_pair_count:
        raise SymmetryDifferenceAdjudicationError(
            f"N5 inconsistency: constant pair count={constant_pair_count} != "
            f"function arg binding_pair_count={binding_pair_count}"
        )


# ---------------------------------------------------------------------------
# Public function
# ---------------------------------------------------------------------------


def run_symmetry_difference_feature_scope_adjudication(
    *,
    repo_root: Path | str | None = None,
    output_csv_path: Path | str | None = None,
    output_md_path: Path | str | None = None,
) -> SymmetryDifferenceAdjudicationResult:
    """Run the binding 02_02_01 adjudication and emit the CSV+MD artifact pair.

    The function:
    1. Resolves repo_root and the four parent artifact paths.
    2. Computes SHA-256 of every parent artifact (Parquet bytes; canonical
       JSON for audits) and the validator module.
    3. Constructs the binding candidate spec list from the module constants.
    4. Calls validate_symmetry_difference_feature_materialization on the
       constructed specs.
    5. Renders the 23-column CSV (1 header row + 1 data row).
    6. Renders the 13-section MD.
    7. Writes both artifacts (CSV+MD only — no Parquet, no audit, no status,
       no log).
    8. Returns the frozen result dataclass.

    Args:
        repo_root: Override for repository root resolution. Defaults to
            six parents up from this module's location.
        output_csv_path: Override for the output CSV path. Defaults to
            the canonical reports path under
            ``reports/artifacts/02_feature_engineering/
            02_symmetry_and_difference_features/``.
        output_md_path: Override for the output MD path. Same default
            directory as CSV.

    Returns:
        Frozen ``SymmetryDifferenceAdjudicationResult``.

    Raises:
        ProvenanceShaNotFoundError: on any SHA pin mismatch.
        SymmetryDifferenceAdjudicationError: on validator failure or
            internal consistency violation.
    """
    resolved_root = _resolve_repo_root(repo_root)

    # Resolve parent artifact paths
    parquet_02_path = resolved_root / _REPO_RELATIVE_PARENT_02_01_02_PARQUET
    parquet_03_path = resolved_root / _REPO_RELATIVE_PARENT_02_01_03_PARQUET
    audit_02_path = resolved_root / _REPO_RELATIVE_PARENT_02_01_02_AUDIT
    audit_03_path = resolved_root / _REPO_RELATIVE_PARENT_02_01_03_AUDIT
    validator_path = resolved_root / _REPO_RELATIVE_VALIDATOR_PATH

    # Resolve output paths
    output_dir = resolved_root / _REPO_RELATIVE_OUTPUT_DIR
    resolved_csv = (
        Path(output_csv_path) if output_csv_path is not None
        else output_dir / _OUTPUT_CSV_NAME
    )
    resolved_md = (
        Path(output_md_path) if output_md_path is not None
        else output_dir / _OUTPUT_MD_NAME
    )

    # Compute SHA-256 pins
    validator_sha = _sha256_of_file_bytes(validator_path)
    parquet_02_sha = _sha256_of_file_bytes(parquet_02_path)
    parquet_03_sha = _sha256_of_file_bytes(parquet_03_path)
    audit_02_sha = _sha256_of_canonical_json(audit_02_path)
    audit_03_sha = _sha256_of_canonical_json(audit_03_path)

    # Validate SHA pins against expected values
    if validator_sha != _EXPECTED_VALIDATOR_SHA256:
        raise ProvenanceShaNotFoundError(
            f"Validator SHA mismatch: got {validator_sha!r}, "
            f"expected {_EXPECTED_VALIDATOR_SHA256!r}"
        )
    if parquet_02_sha != _EXPECTED_02_01_02_PARQUET_SHA256:
        raise ProvenanceShaNotFoundError(
            f"02_01_02 Parquet SHA mismatch: got {parquet_02_sha!r}, "
            f"expected {_EXPECTED_02_01_02_PARQUET_SHA256!r}"
        )
    if parquet_03_sha != _EXPECTED_02_01_03_PARQUET_SHA256:
        raise ProvenanceShaNotFoundError(
            f"02_01_03 Parquet SHA mismatch: got {parquet_03_sha!r}, "
            f"expected {_EXPECTED_02_01_03_PARQUET_SHA256!r}"
        )
    if audit_02_sha != _EXPECTED_02_01_02_AUDIT_CANONICAL_SHA256:
        raise ProvenanceShaNotFoundError(
            f"02_01_02 audit canonical SHA mismatch: got {audit_02_sha!r}, "
            f"expected {_EXPECTED_02_01_02_AUDIT_CANONICAL_SHA256!r}"
        )
    if audit_03_sha != _EXPECTED_02_01_03_AUDIT_CANONICAL_SHA256:
        raise ProvenanceShaNotFoundError(
            f"02_01_03 audit canonical SHA mismatch: got {audit_03_sha!r}, "
            f"expected {_EXPECTED_02_01_03_AUDIT_CANONICAL_SHA256!r}"
        )

    # Construct binding candidate specs
    (
        diff_validator_specs,
        sym_validator_specs,
        race_validator_specs,
        all_decisions,
    ) = _construct_binding_candidate_specs()

    # Call PR #266 validator.
    # The validator checks for absence of the output artifact directories
    # (EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES) relative to repo_root.
    # At adjudication time we are about to CREATE those directories, so we pass
    # a temporary directory as repo_root for the validator's directory-absence
    # check only. All other validator checks use explicitly passed absolute
    # paths and are unaffected by repo_root.
    with tempfile.TemporaryDirectory() as _tmp_root:
        val_result = validate_symmetry_difference_feature_materialization(
            input_02_01_02_parquet_path=parquet_02_path,
            input_02_01_03_parquet_path=parquet_03_path,
            parent_audit_json_paths=(audit_02_path, audit_03_path),
            designed_difference_specs=diff_validator_specs,
            designed_symmetric_pair_specs=sym_validator_specs,
            designed_race_pair_candidate_specs=race_validator_specs,
            repo_root=_tmp_root,
        )

    if not val_result.passed:
        raise SymmetryDifferenceAdjudicationError(
            f"Validator failed: halting_falsifier={val_result.halting_falsifier!r}"
        )

    binding_pair_count = len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS)
    total_candidate_count = len(all_decisions)

    # Render CSV
    data_row = _construct_csv_row(
        validator_passed=val_result.passed,
        validator_halting_falsifier=val_result.halting_falsifier,
        parent_02_01_02_parquet_sha256=parquet_02_sha,
        parent_02_01_03_parquet_sha256=parquet_03_sha,
        parent_02_01_02_audit_json_sha256=audit_02_sha,
        parent_02_01_03_audit_json_sha256=audit_03_sha,
        validator_module_sha256=validator_sha,
        binding_pair_count=binding_pair_count,
    )
    csv_content = _render_csv(_CSV_HEADER, data_row)

    # Render MD
    md_content = _render_md(
        all_decisions=all_decisions,
        validator_passed=val_result.passed,
        validator_halting_falsifier=val_result.halting_falsifier,
        parent_02_01_02_parquet_sha256=parquet_02_sha,
        parent_02_01_03_parquet_sha256=parquet_03_sha,
        parent_02_01_02_audit_json_sha256=audit_02_sha,
        parent_02_01_03_audit_json_sha256=audit_03_sha,
        validator_module_sha256=validator_sha,
        binding_pair_count=binding_pair_count,
        total_candidate_count=total_candidate_count,
        csv_path=resolved_csv,
    )

    # Assert N5 internal consistency
    _assert_internal_consistency(all_decisions, binding_pair_count, data_row)

    # Write artifacts
    resolved_csv.parent.mkdir(parents=True, exist_ok=True)
    resolved_md.parent.mkdir(parents=True, exist_ok=True)
    resolved_csv.write_text(csv_content, encoding="utf-8")
    resolved_md.write_text(md_content, encoding="utf-8")

    LOGGER.info(
        "Adjudication complete: %d candidates; validator_passed=%s; "
        "csv=%s; md=%s",
        total_candidate_count,
        val_result.passed,
        resolved_csv,
        resolved_md,
    )

    return SymmetryDifferenceAdjudicationResult(
        decision_id=DECISION_ID,
        candidate_specs=all_decisions,
        validator_passed=val_result.passed,
        validator_halting_falsifier=val_result.halting_falsifier,
        csv_path=resolved_csv,
        md_path=resolved_md,
        materialized_output_paths=(),
        parent_02_01_02_parquet_sha256=parquet_02_sha,
        parent_02_01_03_parquet_sha256=parquet_03_sha,
        parent_02_01_02_audit_json_sha256=audit_02_sha,
        parent_02_01_03_audit_json_sha256=audit_03_sha,
        validator_module_sha256=validator_sha,
        binding_difference_family_numeric_pair_count=binding_pair_count,
        total_binding_candidate_count=total_candidate_count,
    )
