"""
This validator audits predecessor artifact provenance only (V1). It does
NOT validate any temporal feature grid. Future temporal-discipline checks
(V3) must land in a separate validator module under a separate scaffold
rung.

Step 02_03_01 SCAFFOLD V1 validator (sc2egset).

Purpose: pre-flight validation of the 4 predecessor artifacts (PR #236
02_01_02 pre_game features, PR #259 02_01_03 history-enriched pre_game
features, PR #255 02_01_99 rating omit-closure decision, PR #270 02_02_01
symmetry/difference features) before any future temporal feature step
consumes them as inputs.

Validates:
  - V1.1: artifact existence at relative paths (Invariant I10).
  - V1.2: artifact byte-stability via SHA256 against pinned values.
  - V1.3: identity column presence (focal_match_id, focal_player,
          opponent_player) in Parquet artifacts.
  - V1.4: row-count equality (44418 rows expected) across all 4
          artifacts (cross-artifact row-count invariant).
  - V1.5: forbidden-emission guard: the future 02_03_01 outputs
          directory must NOT yet exist (this scaffold emits no
          temporal artifact).

Halt-priority order (first-failure-wins):
  H1 path-resolution (relative I10) → H2 artifact-exists → H3 SHA-match
  → H4 identity-columns → H5 row-count → H6 outputs-dir-absent.

Pure-function discipline: this module does NOT read column values from
any predecessor artifact; it reads only Parquet schema metadata and
file SHA256. No temporal feature computation, no window evaluation,
no decay logic, no cold-start threshold. All deferred per OQ-1/OQ-2/
OQ-3/OQ-4 of the PR #274 ROADMAP stub.

Lineage:
  - Layer-1 plan: PR #275 (merged at master e1701709).
  - ROADMAP stub: PR #274 (merged at master 6716aa17).
  - 4 parent artifacts: PR #236, #259, #255, #270.
  - Spec: CROSS-02-03-v1.0.1 (LOCKED 2026-05-06).

Invariants applied: I10 (relative-path provenance), I9 (research pipeline
discipline), I3 N/A (no feature computation), I5 N/A, I6 (verbatim SHA
constants), I7 (no magic numbers — SHA pins justified by empirical
derivation from merged parent artifacts), I8 (cross-game-portable
vocabulary; no SC2-specific names in function signatures).
"""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pyarrow.parquet as pq

# ---------------------------------------------------------------------------
# Predecessor artifact relative paths (Invariant I10 — repo-root-relative)
# ---------------------------------------------------------------------------

PARENT_02_01_02_PARQUET_RELPATH = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_02_pre_game_features.parquet"
)
PARENT_02_01_03_PARQUET_RELPATH = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_history_enriched_pre_game_features.parquet"
)
PARENT_02_01_99_CSV_RELPATH = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_99_rating_omit_closure.csv"
)
PARENT_02_02_01_PARQUET_RELPATH = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/02_symmetry_and_difference_features/"
    "02_02_01_symmetry_difference_features.parquet"
)

# Pinned SHA256 (verified 2026-05-30 against merged parent PR artifacts)
PARENT_02_01_02_PARQUET_SHA256 = (
    "24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39"
)
PARENT_02_01_03_PARQUET_SHA256 = (
    "053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071"
)
PARENT_02_01_99_CSV_SHA256 = (
    "831a622c6e0a98c9642e466d5c9dced0fb6b621a6d58e3008a1b0218dd03c370"
)
PARENT_02_02_01_PARQUET_SHA256 = (
    "c4b48601ee0ff800f4b823af270faf03571a637ce07c51a0ef6d072691896ff3"
)

# Identity columns (cross-game-portable vocabulary; not SC2-specific).
# These are the column names as materialised in the parent Parquet artifacts
# (PR #236, PR #259, PR #270): focal_match_id / focal_player / opponent_player.
IDENTITY_COLUMNS_PARQUET: tuple[str, ...] = (
    "focal_match_id",
    "focal_player",
    "opponent_player",
)
# 02_01_99 is a decision artifact; no identity columns required
IDENTITY_COLUMNS_CSV: tuple[str, ...] = ()

# Row-count invariant (Parquet artifacts at 44418 — single match-pair grain)
# The 02_01_99 CSV is a single-row decision artifact; not subject to this invariant.
EXPECTED_ROW_COUNT_PARQUET = 44418

# Forbidden output directory (forbidden-emission guard for 02_03_01 scaffold)
FORBIDDEN_02_03_01_OUTPUTS_DIR = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/03_temporal_features"
)

# Collect all 4 relative paths for iteration
ALL_ARTIFACT_RELPATHS: tuple[str, ...] = (
    PARENT_02_01_02_PARQUET_RELPATH,
    PARENT_02_01_03_PARQUET_RELPATH,
    PARENT_02_01_99_CSV_RELPATH,
    PARENT_02_02_01_PARQUET_RELPATH,
)

# SHA256 pins keyed by relpath suffix (last path component)
_SHA256_BY_RELPATH: dict[str, str] = {
    PARENT_02_01_02_PARQUET_RELPATH: PARENT_02_01_02_PARQUET_SHA256,
    PARENT_02_01_03_PARQUET_RELPATH: PARENT_02_01_03_PARQUET_SHA256,
    PARENT_02_01_99_CSV_RELPATH: PARENT_02_01_99_CSV_SHA256,
    PARENT_02_02_01_PARQUET_RELPATH: PARENT_02_02_01_PARQUET_SHA256,
}

# Parquet-only relpaths (identity-column + row-count checks apply)
_PARQUET_RELPATHS: tuple[str, ...] = (
    PARENT_02_01_02_PARQUET_RELPATH,
    PARENT_02_01_03_PARQUET_RELPATH,
    PARENT_02_02_01_PARQUET_RELPATH,
)


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------


@dataclass
class ProvenanceCheckResult:
    """Aggregate result of the V1 predecessor artifact provenance validator.

    Attributes:
        passed: True iff no halting falsifier fired.
        halting_falsifier: Label of the first falsifier that fired, or None.
        parent_paths_checked: Tuple of relative paths that were checked.
        sha_matches: Mapping from relpath to bool (True = SHA matched).
        identity_columns_ok: Mapping from Parquet relpath to bool.
        row_counts: Mapping from relpath to measured row count.
        outputs_dir_absent: True iff the forbidden 02_03_01 outputs dir
            does not exist.
    """

    passed: bool
    halting_falsifier: Optional[str]
    parent_paths_checked: tuple[str, ...]
    sha_matches: dict[str, bool] = field(default_factory=dict)
    identity_columns_ok: dict[str, bool] = field(default_factory=dict)
    row_counts: dict[str, int] = field(default_factory=dict)
    outputs_dir_absent: bool = True


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _check_relative_paths(relpaths: tuple[str, ...]) -> Optional[str]:
    """Return a halting falsifier label if any relpath is absolute or contains '..'.

    Args:
        relpaths: Tuple of relative path strings to validate.

    Returns:
        Falsifier label string if a violation is found, else None.
    """
    for rp in relpaths:
        p = Path(rp)
        if p.is_absolute():
            return f"absolute_path_violation:{rp}"
        if ".." in p.parts:
            return f"dotdot_path_violation:{rp}"
    return None


def compute_sha256(path: Path) -> str:
    """Compute SHA256 hex digest of a file via chunked binary read.

    Args:
        path: Absolute path to the file.

    Returns:
        Lowercase hex SHA256 digest string.
    """
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _check_artifact_exists(repo_root: Path, relpath: str) -> bool:
    """Return True iff the artifact exists at repo_root / relpath.

    Args:
        repo_root: Resolved absolute repo root path.
        relpath: Relative path string from repo root.

    Returns:
        True iff the resolved path exists on disk.
    """
    return (repo_root / relpath).exists()


def _check_sha256(repo_root: Path, relpath: str) -> bool:
    """Return True iff the artifact SHA256 matches the pinned value.

    Args:
        repo_root: Resolved absolute repo root path.
        relpath: Relative path string from repo root.

    Returns:
        True iff computed SHA256 equals the pinned value.
    """
    path = repo_root / relpath
    computed = compute_sha256(path)
    return computed == _SHA256_BY_RELPATH[relpath]


def _check_identity_columns(repo_root: Path, relpath: str) -> bool:
    """Return True iff the Parquet schema contains all required identity columns.

    Reads only schema metadata; does not read column values.

    Args:
        repo_root: Resolved absolute repo root path.
        relpath: Relative path string to a Parquet artifact.

    Returns:
        True iff all IDENTITY_COLUMNS_PARQUET are present in the schema.
    """
    schema = pq.read_schema(repo_root / relpath)
    names = set(schema.names)
    return all(col in names for col in IDENTITY_COLUMNS_PARQUET)


def _read_parquet_row_count(repo_root: Path, relpath: str) -> int:
    """Return the row count of a Parquet file via metadata only.

    Args:
        repo_root: Resolved absolute repo root path.
        relpath: Relative path string to a Parquet artifact.

    Returns:
        Integer row count.
    """
    meta = pq.read_metadata(repo_root / relpath)
    return meta.num_rows


def _read_csv_row_count(repo_root: Path, relpath: str) -> int:
    """Return the data row count of a CSV file (header row excluded).

    Args:
        repo_root: Resolved absolute repo root path.
        relpath: Relative path string to a CSV artifact.

    Returns:
        Integer row count (excluding header).
    """
    path = repo_root / relpath
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        rows = list(reader)
    # Subtract 1 for header row
    return max(0, len(rows) - 1)


def _check_outputs_dir_absent(repo_root: Path) -> bool:
    """Return True iff the forbidden 02_03_01 outputs directory does not exist.

    Args:
        repo_root: Resolved absolute repo root path.

    Returns:
        True iff FORBIDDEN_02_03_01_OUTPUTS_DIR does not exist under repo_root.
    """
    return not (repo_root / FORBIDDEN_02_03_01_OUTPUTS_DIR).exists()


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def validate_predecessor_artifact_provenance(
    repo_root: Path,
) -> ProvenanceCheckResult:
    """V1 predecessor artifact provenance validator public entrypoint.

    Implements the halt-priority chain:
      H1 relative-path check (Invariant I10) →
      H2 artifact-exists check →
      H3 SHA256 match →
      H4 identity-column presence (Parquet only) →
      H5 row-count equality (Parquet only) →
      H6 outputs-dir-absent guard.

    Pure-function: reads only file bytes (SHA) and Parquet schema metadata.
    Writes nothing.

    Args:
        repo_root: Absolute Path to the repository root. Must be absolute;
            callers passing a relative path will trigger H1 falsifier.

    Returns:
        ProvenanceCheckResult with all check outputs populated.
        ``passed`` is True iff ``halting_falsifier is None``.
    """
    relpaths = ALL_ARTIFACT_RELPATHS
    halting_falsifier: Optional[str] = None
    sha_matches: dict[str, bool] = {}
    identity_columns_ok: dict[str, bool] = {}
    row_counts: dict[str, int] = {}
    outputs_dir_absent = True

    # H1 — relative-path discipline (Invariant I10)
    # repo_root itself must be absolute; relpaths must be relative.
    if not repo_root.is_absolute():
        return ProvenanceCheckResult(
            passed=False,
            halting_falsifier=f"absolute_path_violation:{repo_root}",
            parent_paths_checked=relpaths,
            sha_matches=sha_matches,
            identity_columns_ok=identity_columns_ok,
            row_counts=row_counts,
            outputs_dir_absent=outputs_dir_absent,
        )

    relative_path_violation = _check_relative_paths(relpaths)
    if relative_path_violation is not None:
        return ProvenanceCheckResult(
            passed=False,
            halting_falsifier=relative_path_violation,
            parent_paths_checked=relpaths,
            sha_matches=sha_matches,
            identity_columns_ok=identity_columns_ok,
            row_counts=row_counts,
            outputs_dir_absent=outputs_dir_absent,
        )

    # H2 — artifact exists
    for rp in relpaths:
        if not _check_artifact_exists(repo_root, rp):
            halting_falsifier = f"artifact_missing:{rp}"
            return ProvenanceCheckResult(
                passed=False,
                halting_falsifier=halting_falsifier,
                parent_paths_checked=relpaths,
                sha_matches=sha_matches,
                identity_columns_ok=identity_columns_ok,
                row_counts=row_counts,
                outputs_dir_absent=outputs_dir_absent,
            )

    # H3 — SHA256 match
    for rp in relpaths:
        matched = _check_sha256(repo_root, rp)
        sha_matches[rp] = matched
        if not matched:
            halting_falsifier = f"sha_mismatch:{rp}"
            return ProvenanceCheckResult(
                passed=False,
                halting_falsifier=halting_falsifier,
                parent_paths_checked=relpaths,
                sha_matches=sha_matches,
                identity_columns_ok=identity_columns_ok,
                row_counts=row_counts,
                outputs_dir_absent=outputs_dir_absent,
            )

    # H4 — identity columns (Parquet artifacts only)
    for rp in _PARQUET_RELPATHS:
        cols_ok = _check_identity_columns(repo_root, rp)
        identity_columns_ok[rp] = cols_ok
        if not cols_ok:
            schema = pq.read_schema(repo_root / rp)
            missing = [
                col for col in IDENTITY_COLUMNS_PARQUET if col not in set(schema.names)
            ]
            col_name = missing[0] if missing else "unknown"
            halting_falsifier = f"identity_column_missing:{col_name}"
            return ProvenanceCheckResult(
                passed=False,
                halting_falsifier=halting_falsifier,
                parent_paths_checked=relpaths,
                sha_matches=sha_matches,
                identity_columns_ok=identity_columns_ok,
                row_counts=row_counts,
                outputs_dir_absent=outputs_dir_absent,
            )

    # H5 — row-count equality (Parquet artifacts only; CSV exempt)
    for rp in _PARQUET_RELPATHS:
        rc = _read_parquet_row_count(repo_root, rp)
        row_counts[rp] = rc
        if rc != EXPECTED_ROW_COUNT_PARQUET:
            halting_falsifier = (
                f"row_count_mismatch:{rp}"
                f":expected={EXPECTED_ROW_COUNT_PARQUET}:actual={rc}"
            )
            return ProvenanceCheckResult(
                passed=False,
                halting_falsifier=halting_falsifier,
                parent_paths_checked=relpaths,
                sha_matches=sha_matches,
                identity_columns_ok=identity_columns_ok,
                row_counts=row_counts,
                outputs_dir_absent=outputs_dir_absent,
            )
    # Record CSV row count for completeness (not gated)
    csv_rc = _read_csv_row_count(repo_root, PARENT_02_01_99_CSV_RELPATH)
    row_counts[PARENT_02_01_99_CSV_RELPATH] = csv_rc

    # H6 — outputs directory absent
    outputs_dir_absent = _check_outputs_dir_absent(repo_root)
    if not outputs_dir_absent:
        halting_falsifier = "forbidden_outputs_dir_present"
        return ProvenanceCheckResult(
            passed=False,
            halting_falsifier=halting_falsifier,
            parent_paths_checked=relpaths,
            sha_matches=sha_matches,
            identity_columns_ok=identity_columns_ok,
            row_counts=row_counts,
            outputs_dir_absent=outputs_dir_absent,
        )

    return ProvenanceCheckResult(
        passed=True,
        halting_falsifier=None,
        parent_paths_checked=relpaths,
        sha_matches=sha_matches,
        identity_columns_ok=identity_columns_ok,
        row_counts=row_counts,
        outputs_dir_absent=outputs_dir_absent,
    )
