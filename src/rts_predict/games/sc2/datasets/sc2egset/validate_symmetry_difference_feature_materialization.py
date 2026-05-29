"""Validation module for SC2EGSet Step 02_02_01 symmetry & difference scaffold.

Scaffold-only: validates the design contract for the symmetry & difference
feature family; does NOT materialise feature values.

This module is a PURE FUNCTION over candidate-feature design specs and the
schema metadata of two byte-stable upstream Parquet artifacts. It does NOT
open the Parquet files for value reads, does NOT materialise any feature,
and does NOT write any path under reports/artifacts/.

Layer-2 stage marker: scaffold (scaffold-only). The validator will be
re-used at materialisation; the docstring will be updated then.

Binding sources:
    - Step 02_01_02 leakage audit JSON (7-tuple ``features_audited``,
      ``projected_identity_columns``, ``projected_context_columns``).
    - Step 02_01_03 leakage audit JSON (24-tuple ``features_audited``,
      same identity/context projection).
    - PR #265 Layer-1 plan (this scaffold authorises CANDIDATE-only
      enumeration; binding decision deferred to future source-anchor
      adjudication PR analogous to PR #234).
    - ``02_FEATURE_ENGINEERING_MANUAL.md`` §3 (Bradley-Terry; difference
      features as default for pairwise prediction).
    - Invariant I3 (no tracker in pre-game features; strict-< temporal
      cutoff inherited from 02_01_03).
    - Invariant I5 (focal/opponent symmetry; slot-orthogonality of
      candidate differences).
    - Invariant I7 (no magic numbers — module-level UPPER_SNAKE constants).
    - Invariant I8 (cross-game hygiene — no AoE2 ``civilization`` token
      in SC2EGSet vocabulary).
    - Invariant I9 (prior-artifact dependency — SHA256 pins on inputs).
    - Invariant I10 (relative-path provenance — relpaths from repo root).

Falsifiers implemented (halting priority order; first to fire halts):
    input_parquet_missing, input_parquet_sha_mismatch,
    parent_audit_json_missing, audit_json_misaligned,
    artifact_directory_present, direction_annotation_invalid,
    source_column_traceability_violation,
    reconstructed_rating_in_candidates,
    slot_dependent_token_present, target_leak_token_in_candidate,
    aoe2_vocabulary_in_candidate, tracker_sourced_candidate,
    direction_name_inconsistent, materialization_output_path_present.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

LOGGER = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level constants — no magic numbers (Invariant I7)
# ---------------------------------------------------------------------------

INPUT_02_01_02_PARQUET_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_02_pre_game_features.parquet"
)
INPUT_02_01_03_PARQUET_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_enriched_pre_game_features.parquet"
)

# Measured 2026-05-29; bind Invariant I9 (prior-artifact dependency) and I10
# (relative-path provenance). The validator re-computes SHA256 on every call
# and halts on mismatch.
INPUT_02_01_02_PARQUET_SHA256: str = (
    "24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39"
)
INPUT_02_01_03_PARQUET_SHA256: str = (
    "053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071"
)

INPUT_02_01_02_AUDIT_JSON_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_01_02/leakage_audit_sc2egset.json"
)
INPUT_02_01_03_AUDIT_JSON_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_01_03/leakage_audit_sc2egset.json"
)
EXPECTED_PARENT_AUDIT_JSON_RELPATHS: tuple[str, str] = (
    INPUT_02_01_02_AUDIT_JSON_RELPATH,
    INPUT_02_01_03_AUDIT_JSON_RELPATH,
)

# Identity / context projection — read literally from both audit JSONs'
# ``projected_identity_columns`` / ``projected_context_columns``.
IDENTITY_COLUMNS: tuple[str, str, str] = (
    "focal_match_id",
    "focal_player",
    "opponent_player",
)
CONTEXT_ANCHOR_COLUMNS: tuple[str, ...] = ("started_at",)

# 02_01_02 ``features_audited`` 7-tuple — verbatim from audit JSON.
UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02: tuple[str, ...] = (
    "focal_race",
    "opponent_race",
    "race_pair",
    "map_type",
    "patch_version",
    "focal_is_mmr_missing",
    "opponent_is_mmr_missing",
)

# 02_01_03 ``features_audited`` 24-tuple — verbatim from audit JSON.
UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03: tuple[str, ...] = (
    "focal_prior_match_count",
    "focal_prior_win_rate_decisive",
    "focal_days_since_prior_match",
    "focal_prior_win_rate_race_conditional",
    "focal_prior_win_rate_map_conditional",
    "focal_prior_win_rate_matchup_conditional",
    "opponent_prior_match_count",
    "opponent_prior_win_rate_decisive",
    "opponent_days_since_prior_match",
    "opponent_prior_win_rate_race_conditional",
    "opponent_prior_win_rate_map_conditional",
    "opponent_prior_win_rate_matchup_conditional",
    "matchup_h2h_count",
    "matchup_h2h_focal_win_rate",
    "is_cross_region_fragmented_focal_history_any",
    "is_cross_region_fragmented_opponent_history_any",
    "focal_apm_prior_mean",
    "focal_sq_prior_mean",
    "focal_supply_capped_pct_prior_mean",
    "focal_elapsed_game_loops_prior_mean",
    "opponent_apm_prior_mean",
    "opponent_sq_prior_mean",
    "opponent_supply_capped_pct_prior_mean",
    "opponent_elapsed_game_loops_prior_mean",
)

# Direction annotation literal — only these two values are accepted
# (Invariant I5; PR #265 plan A9 / reviewer-adversarial N4).
VALID_DIRECTION_LITERAL_VALUES: tuple[str, str] = (
    "focal_minus_opponent",
    "symmetric",
)

# Slot-token regex set — boundary-aware; covers player/slot/p/idx/home/away/
# left/right/host/guest/a_minus_b/b_minus_a variants. Any candidate column
# name matching any pattern fires the slot_dependent_token_present
# falsifier (PR #265 plan A8 / reviewer-adversarial N3).
BLOCKED_SLOT_TOKEN_REGEX: tuple[str, ...] = (
    r"(?:^|_)player_?\d+(?:_|$)",
    r"(?:^|_)slot_?\d+(?:_|$)",
    r"(?:^|_)p\d+(?:_|$)",
    r"(?:^|_)idx_?\d+(?:_|$)",
    r"(?:^|_)home(?:_|$)",
    r"(?:^|_)away(?:_|$)",
    r"(?:^|_)left(?:_|$)",
    r"(?:^|_)right(?:_|$)",
    r"(?:^|_)host(?:_|$)",
    r"(?:^|_)guest(?:_|$)",
    r"(?:^|_)a_minus_b(?:_|$)",
    r"(?:^|_)b_minus_a(?:_|$)",
)

# PR #255 / PR #257 binding exclusion — the reconstructed_rating family is
# intentionally OMITTED from 02_01_03 materialisation; 02_02 must not
# silently re-introduce it (PR #265 plan A15).
BLOCKED_FAMILY_FRAGMENTS: tuple[str, ...] = (
    "reconstructed_rating",
    "reconstructed_rating_focal_pre",
    "reconstructed_rating_opp_pre",
    "reconstructed_rating_diff",
)

# POST-GAME tokens — copied verbatim from predecessor PR #241 validator
# (validate_history_enriched_pre_game_materialization.py lines 100-111).
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

# Boundary-aware POST-GAME token regex — replaces naive substring checks
# to avoid false-positives on legitimate ``win_rate`` compounds (PR #265
# plan A11 / reviewer-adversarial N6).
POST_GAME_TOKEN_REGEX: tuple[str, ...] = tuple(
    rf"(?:^|_){re.escape(token)}(?:_|$)" for token in POST_GAME_TOKENS
)

# Allowlist substrings — if a candidate column name contains any of these
# legitimate compounds, a boundary-aware POST_GAME token match is
# suppressed. These are PR #259-bound history-aggregate columns whose
# ``win`` is part of ``win_rate`` (Bradley-Terry-grounded prior signal),
# not a target-leak token.
POST_GAME_TOKEN_ALLOWLIST_SUBSTRINGS: tuple[str, ...] = (
    "prior_win_rate",
    "prior_win_rate_decisive",
    "prior_win_rate_race_conditional",
    "prior_win_rate_map_conditional",
    "prior_win_rate_matchup_conditional",
    "matchup_h2h_focal_win_rate",
)

# AoE2 vocabulary — boundary-aware enforcement (Invariant I8 cross-game
# hygiene). SC2EGSet uses ``race`` exclusively.
FORBIDDEN_AOE2_VOCABULARY: tuple[str, ...] = ("civilization", "civ")
FORBIDDEN_AOE2_VOCABULARY_REGEX: tuple[str, ...] = tuple(
    rf"(?:^|_){re.escape(token)}(?:_|$)"
    for token in FORBIDDEN_AOE2_VOCABULARY
)

# Tracker source prefix — tracker-derived target-match features are
# never pre-game features (Invariant I3; CROSS-02-00 §5.4).
TRACKER_SOURCE_PREFIX: str = "tracker_events_raw"

# Filesystem-absence check targets — neither directory may exist at
# scaffold stage (PR #265 plan A12 / reviewer-adversarial N7).
EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES: tuple[str, str] = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_02_01",
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/02_symmetry_and_difference_features",
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CandidateFeatureSpec:
    """Frozen design spec for one CANDIDATE symmetry/difference feature.

    Attributes:
        column_name: The candidate feature column name (notebook-declared).
        direction: Either ``"focal_minus_opponent"`` (signed difference) or
            ``"symmetric"`` (focal/opponent-swap invariant aggregate).
        source_columns: Tuple of upstream column names this candidate is
            derived from. Each element MUST appear in
            ``UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02`` or
            ``UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03``.
    """

    column_name: str
    direction: Literal["focal_minus_opponent", "symmetric"]
    source_columns: tuple[str, ...]


@dataclass(frozen=True)
class SymmetryDifferenceValidationResult:
    """Aggregate result of the symmetry/difference scaffold validation.

    Attributes:
        passed: True iff no halting falsifier fired.
        input_parquet_paths_present_ok: Both upstream Parquet paths exist.
        input_parquet_sha256_ok: Both Parquet SHA256 match the embedded pins.
        parent_audit_json_paths_present_ok: Both audit JSON paths exist.
        audit_json_alignment_ok: ``features_audited`` /
            ``projected_identity_columns`` / ``projected_context_columns``
            in each audit JSON equal the module-level constants.
        direction_annotation_valid: True iff every candidate's ``direction``
            is in ``VALID_DIRECTION_LITERAL_VALUES``.
        source_column_traceability_ok: True iff every candidate's
            ``source_columns`` element is in the union of audited tuples.
        direction_name_consistency_ok: True iff candidate column names
            ending in ``_diff`` / containing ``_minus_`` carry
            ``direction == "focal_minus_opponent"`` and names containing
            ``_pair_mean`` / ``_pair_sum`` / ``_pair_product`` /
            ``_abs_diff`` / ``_pair_xor`` / ``_pair_and`` / ``_pair_or``
            carry ``direction == "symmetric"``.
        slot_token_violations: ``(column_name, matched_pattern)`` pairs
            where a BLOCKED_SLOT_TOKEN_REGEX pattern matched.
        target_leak_token_violations: ``(column_name, matched_pattern)``
            pairs where a POST_GAME_TOKEN_REGEX pattern matched AND the
            column name does NOT contain a POST_GAME_TOKEN_ALLOWLIST
            substring.
        reconstructed_rating_violations: Candidate column names containing
            a BLOCKED_FAMILY_FRAGMENTS substring.
        aoe2_vocabulary_violations: ``(column_name, matched_pattern)``
            pairs where a FORBIDDEN_AOE2_VOCABULARY_REGEX matched.
        tracker_sourced_violations: Candidate column names whose
            ``source_columns`` contain an element starting with
            ``TRACKER_SOURCE_PREFIX``.
        artifact_directory_absence_ok: True iff neither directory in
            ``EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES`` exists.
        materialized_output_paths: ALWAYS ``()`` — scaffold persists nothing.
        halting_falsifier: Label of the first falsifier that fired, or
            ``None``.
    """

    passed: bool
    input_parquet_paths_present_ok: bool
    input_parquet_sha256_ok: bool
    parent_audit_json_paths_present_ok: bool
    audit_json_alignment_ok: bool
    direction_annotation_valid: bool
    source_column_traceability_ok: bool
    direction_name_consistency_ok: bool
    slot_token_violations: tuple[tuple[str, str], ...]
    target_leak_token_violations: tuple[tuple[str, str], ...]
    reconstructed_rating_violations: tuple[str, ...]
    aoe2_vocabulary_violations: tuple[tuple[str, str], ...]
    tracker_sourced_violations: tuple[str, ...]
    artifact_directory_absence_ok: bool
    materialized_output_paths: tuple[str, ...] = field(default_factory=tuple)
    halting_falsifier: str | None = None


# ---------------------------------------------------------------------------
# Private check helpers
# ---------------------------------------------------------------------------


def _resolve_repo_root(repo_root: Path | str | None) -> Path:
    """Resolve repo root: explicit override or upward walk from this module.

    Args:
        repo_root: Caller-supplied repo root, or ``None`` to derive from
            this module's location (six parents up).

    Returns:
        Absolute resolved path to the repo root.
    """
    if repo_root is not None:
        return Path(repo_root).resolve()
    return Path(__file__).resolve().parents[6]


def _sha256_of_file(path: Path) -> str:
    """Compute SHA256 hex digest of a file via chunked binary read.

    Args:
        path: Path to the file.

    Returns:
        Lowercase hex SHA256 digest string.
    """
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _check_input_parquet_paths_present(
    input_02_01_02_path: Path,
    input_02_01_03_path: Path,
) -> bool:
    """Verify both upstream Parquet paths exist (Invariant I9).

    Args:
        input_02_01_02_path: Resolved path to 02_01_02 Parquet.
        input_02_01_03_path: Resolved path to 02_01_03 Parquet.

    Returns:
        True iff both paths exist on disk.
    """
    return input_02_01_02_path.exists() and input_02_01_03_path.exists()


def _check_input_parquet_sha256(
    input_02_01_02_path: Path,
    input_02_01_03_path: Path,
) -> bool:
    """Verify SHA256 of both Parquets matches embedded pins (Invariant I9).

    Args:
        input_02_01_02_path: Resolved path to 02_01_02 Parquet.
        input_02_01_03_path: Resolved path to 02_01_03 Parquet.

    Returns:
        True iff both SHA256 digests match.
    """
    sha_02 = _sha256_of_file(input_02_01_02_path)
    sha_03 = _sha256_of_file(input_02_01_03_path)
    return (
        sha_02 == INPUT_02_01_02_PARQUET_SHA256
        and sha_03 == INPUT_02_01_03_PARQUET_SHA256
    )


def _check_parent_audit_jsons_present(
    audit_paths: tuple[Path, Path],
) -> bool:
    """Verify both parent audit JSON paths exist on disk.

    Args:
        audit_paths: Resolved paths to the two leakage audit JSON files.

    Returns:
        True iff both paths exist.
    """
    return all(p.exists() for p in audit_paths)


def _check_audit_json_alignment(
    audit_02_01_02_path: Path,
    audit_02_01_03_path: Path,
) -> bool:
    """Verify audit JSON content equals the embedded constants.

    Checks ``features_audited``, ``projected_identity_columns``, and
    ``projected_context_columns`` in each audit JSON.

    Args:
        audit_02_01_02_path: Resolved path to 02_01_02 audit JSON.
        audit_02_01_03_path: Resolved path to 02_01_03 audit JSON.

    Returns:
        True iff every projected list matches the embedded constants.
    """
    with audit_02_01_02_path.open(encoding="utf-8") as fh:
        audit_02 = json.load(fh)
    with audit_02_01_03_path.open(encoding="utf-8") as fh:
        audit_03 = json.load(fh)
    if tuple(audit_02.get("features_audited", [])) != UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02:
        return False
    if tuple(audit_03.get("features_audited", [])) != UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03:
        return False
    if tuple(audit_02.get("projected_identity_columns", [])) != IDENTITY_COLUMNS:
        return False
    if tuple(audit_03.get("projected_identity_columns", [])) != IDENTITY_COLUMNS:
        return False
    if tuple(audit_02.get("projected_context_columns", [])) != CONTEXT_ANCHOR_COLUMNS:
        return False
    if tuple(audit_03.get("projected_context_columns", [])) != CONTEXT_ANCHOR_COLUMNS:
        return False
    return True


def _check_direction_annotation_validity(
    specs: tuple[CandidateFeatureSpec, ...],
) -> bool:
    """Verify every candidate's ``direction`` is in the allowed Literal set.

    Args:
        specs: Tuple of all candidate specs (all three families flattened).

    Returns:
        True iff every spec's ``direction`` is in
        ``VALID_DIRECTION_LITERAL_VALUES``.
    """
    return all(spec.direction in VALID_DIRECTION_LITERAL_VALUES for spec in specs)


def _check_source_column_traceability(
    specs: tuple[CandidateFeatureSpec, ...],
) -> bool:
    """Verify every spec's ``source_columns`` trace to audited tuples.

    The audited set is the union of
    ``UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02`` and
    ``UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03``. Tracker-source
    prefixes are NOT in this set; they fail traceability AND fire the
    later tracker-source falsifier.

    Args:
        specs: Tuple of all candidate specs.

    Returns:
        True iff every spec's ``source_columns`` element is in the
        audited union.
    """
    audited = set(UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02) | set(
        UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03
    )
    for spec in specs:
        for src in spec.source_columns:
            if src not in audited:
                return False
    return True


def _check_direction_name_consistency(
    specs: tuple[CandidateFeatureSpec, ...],
) -> bool:
    """Verify candidate name suffixes match the declared direction.

    Names ending in ``_diff`` or containing ``_minus_`` must declare
    ``direction == "focal_minus_opponent"``. Names containing any of
    ``_pair_mean``, ``_pair_sum``, ``_pair_product``, ``_abs_diff``,
    ``_pair_xor``, ``_pair_and``, ``_pair_or`` must declare
    ``direction == "symmetric"``.

    Args:
        specs: Tuple of all candidate specs.

    Returns:
        True iff every spec's name and declared direction are consistent.
    """
    diff_tokens = ("_minus_",)
    diff_suffixes = ("_diff",)
    symmetric_tokens = (
        "_pair_mean",
        "_pair_sum",
        "_pair_product",
        "_abs_diff",
        "_pair_xor",
        "_pair_and",
        "_pair_or",
    )
    for spec in specs:
        name = spec.column_name
        has_diff = name.endswith(diff_suffixes) or any(tok in name for tok in diff_tokens)
        has_sym = any(tok in name for tok in symmetric_tokens)
        # ``_abs_diff`` ends with ``_diff`` but is symmetric — symmetric wins.
        if has_sym:
            if spec.direction != "symmetric":
                return False
            continue
        if has_diff and spec.direction != "focal_minus_opponent":
            return False
    return True


def _check_slot_token_violations(
    specs: tuple[CandidateFeatureSpec, ...],
) -> tuple[tuple[str, str], ...]:
    """Return ``(column_name, matched_pattern)`` for slot-token matches.

    Enforces Invariant I5 slot-orthogonality (PR #265 plan A8). Patterns
    are boundary-aware so ``focal_player`` / ``opponent_player`` (identity
    columns) are NOT in candidate column names anyway — but candidates
    must not introduce ``player_1``, ``slot_2``, ``home``, ``away``, etc.

    Args:
        specs: Tuple of all candidate specs.

    Returns:
        Tuple of ``(column_name, matched_pattern)`` pairs in violation.
    """
    hits: list[tuple[str, str]] = []
    for spec in specs:
        for pattern in BLOCKED_SLOT_TOKEN_REGEX:
            if re.search(pattern, spec.column_name):
                hits.append((spec.column_name, pattern))
    return tuple(hits)


def _check_target_leak_token_violations(
    specs: tuple[CandidateFeatureSpec, ...],
) -> tuple[tuple[str, str], ...]:
    """Return ``(column_name, matched_pattern)`` for boundary-aware POST_GAME hits.

    Two-step filter (PR #265 plan A11):
        1. For each POST_GAME_TOKEN_REGEX pattern, check
           ``re.search`` against the candidate's column name.
        2. If matched, suppress when the column name contains any
           POST_GAME_TOKEN_ALLOWLIST_SUBSTRINGS substring (legitimate
           ``prior_win_rate`` compounds).

    Args:
        specs: Tuple of all candidate specs.

    Returns:
        Tuple of ``(column_name, matched_pattern)`` pairs in violation
        (excluding allowlisted compounds).
    """
    hits: list[tuple[str, str]] = []
    for spec in specs:
        name = spec.column_name
        if any(allow in name for allow in POST_GAME_TOKEN_ALLOWLIST_SUBSTRINGS):
            continue
        for pattern in POST_GAME_TOKEN_REGEX:
            if re.search(pattern, name):
                hits.append((name, pattern))
    return tuple(hits)


def _check_reconstructed_rating_violations(
    specs: tuple[CandidateFeatureSpec, ...],
) -> tuple[str, ...]:
    """Return candidate column names containing a BLOCKED_FAMILY_FRAGMENTS substring.

    Enforces PR #255 / PR #257 binding exclusion of the
    ``reconstructed_rating`` family (PR #265 plan A15).

    Args:
        specs: Tuple of all candidate specs.

    Returns:
        Tuple of offending candidate column names.
    """
    hits: list[str] = []
    for spec in specs:
        for fragment in BLOCKED_FAMILY_FRAGMENTS:
            if fragment in spec.column_name:
                hits.append(spec.column_name)
                break
        # Also sweep source_columns for the same family fragments.
        for src in spec.source_columns:
            for fragment in BLOCKED_FAMILY_FRAGMENTS:
                if fragment in src:
                    hits.append(spec.column_name)
                    break
    return tuple(hits)


def _check_aoe2_vocabulary_violations(
    specs: tuple[CandidateFeatureSpec, ...],
) -> tuple[tuple[str, str], ...]:
    """Return ``(column_name, matched_pattern)`` for AoE2 vocabulary tokens.

    Enforces Invariant I8 cross-game hygiene: SC2EGSet uses ``race``
    exclusively; ``civilization`` / ``civ`` is an AoE2 token.

    Args:
        specs: Tuple of all candidate specs.

    Returns:
        Tuple of ``(column_name, matched_pattern)`` pairs in violation.
    """
    hits: list[tuple[str, str]] = []
    for spec in specs:
        for pattern in FORBIDDEN_AOE2_VOCABULARY_REGEX:
            if re.search(pattern, spec.column_name):
                hits.append((spec.column_name, pattern))
    return tuple(hits)


def _check_tracker_sourced_violations(
    specs: tuple[CandidateFeatureSpec, ...],
) -> tuple[str, ...]:
    """Return candidate names whose source_columns include a tracker prefix.

    Enforces Invariant I3 / CROSS-02-00 §5.4: tracker-derived target-match
    features are never pre-game features at this layer.

    Args:
        specs: Tuple of all candidate specs.

    Returns:
        Tuple of offending candidate column names.
    """
    hits: list[str] = []
    for spec in specs:
        for src in spec.source_columns:
            if src.startswith(TRACKER_SOURCE_PREFIX):
                hits.append(spec.column_name)
                break
    return tuple(hits)


def _check_artifact_directories_absent(
    repo_root: Path,
) -> bool:
    """Verify filesystem absence (not emptiness) of both target directories.

    Per PR #265 plan A12 / reviewer-adversarial N7: ``.gitkeep`` /
    ``.DS_Store`` would false-pass an emptiness check; absence is the only
    mechanically-defensible artifact-free promise at scaffold stage.

    Args:
        repo_root: Resolved repo root path.

    Returns:
        True iff neither directory in
        ``EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES`` exists.
    """
    for relpath in EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES:
        if (repo_root / relpath).exists():
            return False
    return True


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def validate_symmetry_difference_feature_materialization(
    input_02_01_02_parquet_path: Path | str,
    input_02_01_03_parquet_path: Path | str,
    parent_audit_json_paths: tuple[Path | str, Path | str],
    designed_difference_specs: tuple[CandidateFeatureSpec, ...],
    designed_symmetric_pair_specs: tuple[CandidateFeatureSpec, ...],
    designed_race_pair_candidate_specs: tuple[CandidateFeatureSpec, ...],
    repo_root: Path | str | None = None,
) -> SymmetryDifferenceValidationResult:
    """Validate the symmetry/difference scaffold design contract.

    Runs the 14-step halting falsifier chain over the byte-stable
    upstream Parquet artifacts (path existence + SHA256 pin) and the
    notebook-declared CANDIDATE column-name tuples. Does NOT open any
    Parquet for value reads, does NOT compute any aggregate, and does
    NOT write any path. ``materialized_output_paths`` is always ``()``.

    Args:
        input_02_01_02_parquet_path: Path to the 02_01_02 pre_game
            features Parquet (SHA-pinned).
        input_02_01_03_parquet_path: Path to the 02_01_03 history-
            enriched pre_game features Parquet (SHA-pinned).
        parent_audit_json_paths: ``(02_01_02 audit JSON, 02_01_03 audit
            JSON)`` tuple.
        designed_difference_specs: Tuple of CandidateFeatureSpec for the
            difference family (direction ``focal_minus_opponent``).
        designed_symmetric_pair_specs: Tuple of CandidateFeatureSpec for
            the symmetric-pair family (direction ``symmetric``).
        designed_race_pair_candidate_specs: Tuple of CandidateFeatureSpec
            for the race-pair CANDIDATE family (may defer to 02_05).
        repo_root: Override for repo-root resolution (defaults to upward
            walk from this module's location).

    Returns:
        ``SymmetryDifferenceValidationResult`` with all check outputs
        populated. ``passed`` is True iff ``halting_falsifier is None``.
    """
    repo_root_resolved = _resolve_repo_root(repo_root)

    input_02_path = Path(input_02_01_02_parquet_path)
    input_03_path = Path(input_02_01_03_parquet_path)
    audit_paths_resolved: tuple[Path, Path] = (
        Path(parent_audit_json_paths[0]),
        Path(parent_audit_json_paths[1]),
    )

    all_specs: tuple[CandidateFeatureSpec, ...] = (
        designed_difference_specs
        + designed_symmetric_pair_specs
        + designed_race_pair_candidate_specs
    )

    input_paths_present_ok = _check_input_parquet_paths_present(
        input_02_path, input_03_path
    )

    if input_paths_present_ok:
        input_sha256_ok = _check_input_parquet_sha256(input_02_path, input_03_path)
    else:
        input_sha256_ok = False

    parent_audit_present_ok = _check_parent_audit_jsons_present(audit_paths_resolved)

    if parent_audit_present_ok:
        audit_alignment_ok = _check_audit_json_alignment(
            audit_paths_resolved[0], audit_paths_resolved[1]
        )
    else:
        audit_alignment_ok = False

    artifact_absence_ok = _check_artifact_directories_absent(repo_root_resolved)

    direction_valid = _check_direction_annotation_validity(all_specs)
    traceability_ok = _check_source_column_traceability(all_specs)
    direction_name_ok = _check_direction_name_consistency(all_specs)

    slot_hits = _check_slot_token_violations(all_specs)
    leak_hits = _check_target_leak_token_violations(all_specs)
    recon_hits = _check_reconstructed_rating_violations(all_specs)
    aoe2_hits = _check_aoe2_vocabulary_violations(all_specs)
    tracker_hits = _check_tracker_sourced_violations(all_specs)

    # Halting falsifier priority chain — first failure wins. Structural
    # input failures (parquet/audit) precede content failures (candidates).
    halting_falsifier: str | None = None
    if not input_paths_present_ok:
        halting_falsifier = "input_parquet_missing"
    elif not input_sha256_ok:
        halting_falsifier = "input_parquet_sha_mismatch"
    elif not parent_audit_present_ok:
        halting_falsifier = "parent_audit_json_missing"
    elif not audit_alignment_ok:
        halting_falsifier = "audit_json_misaligned"
    elif not artifact_absence_ok:
        halting_falsifier = "artifact_directory_present"
    elif not direction_valid:
        halting_falsifier = "direction_annotation_invalid"
    elif not traceability_ok:
        halting_falsifier = "source_column_traceability_violation"
    elif recon_hits:
        halting_falsifier = "reconstructed_rating_in_candidates"
    elif slot_hits:
        halting_falsifier = "slot_dependent_token_present"
    elif leak_hits:
        halting_falsifier = "target_leak_token_in_candidate"
    elif aoe2_hits:
        halting_falsifier = "aoe2_vocabulary_in_candidate"
    elif tracker_hits:
        halting_falsifier = "tracker_sourced_candidate"
    elif not direction_name_ok:
        halting_falsifier = "direction_name_inconsistent"

    passed = halting_falsifier is None

    LOGGER.debug(
        "validate_symmetry_difference_feature_materialization: passed=%s "
        "halting_falsifier=%s candidate_count=%d",
        passed,
        halting_falsifier,
        len(all_specs),
    )

    return SymmetryDifferenceValidationResult(
        passed=passed,
        input_parquet_paths_present_ok=input_paths_present_ok,
        input_parquet_sha256_ok=input_sha256_ok,
        parent_audit_json_paths_present_ok=parent_audit_present_ok,
        audit_json_alignment_ok=audit_alignment_ok,
        direction_annotation_valid=direction_valid,
        source_column_traceability_ok=traceability_ok,
        direction_name_consistency_ok=direction_name_ok,
        slot_token_violations=slot_hits,
        target_leak_token_violations=leak_hits,
        reconstructed_rating_violations=recon_hits,
        aoe2_vocabulary_violations=aoe2_hits,
        tracker_sourced_violations=tracker_hits,
        artifact_directory_absence_ok=artifact_absence_ok,
        materialized_output_paths=(),
        halting_falsifier=halting_falsifier,
    )
