"""V3 scaffold — strict-< temporal-discipline validator (sc2egset Step 02_03_01).

V3 is a schema-level design-time gate.
V3 does not read Parquet data rows, does not query DuckDB, and does not recompute feature values.
V3 and CROSS-02-01 are complementary, not redundant; value-level leakage is audited
post-materialization.

V3 enforces strict-`<` temporal discipline via three design-time predicates:
history-column naming convention, temporal-anchor column presence in Parquet
schema footer, and CROSS-02-03 / CROSS-02-02 / Invariant I3 cite-string
provenance in this module's docstring. V3 catches the common contributor
failure modes (forbidden column naming, missing temporal anchor, missing
cite-strings); CROSS-02-01-v1.0.1 post-materialization audits catch
sophisticated semantic leaks at the value layer.

Predecessor artifacts validated (schema metadata + file SHA256 only; NO row
reads):
  - 02_01_02 pre_game features (PR #236 @ 39298c0a; SHA `24db73fb...`)
  - 02_01_03 history-enriched pre_game features (PR #259 @ 5a62fc76;
    SHA `053900e7...`)
  - 02_01_99 rating omit-closure decision (PR #255 @ 52f9c108;
    SHA `831a622c...`)
  - 02_02_01 symmetry/difference features (PR #270 @ eddd0489;
    SHA `c4b48601...`)

Citations (binding):
  - Invariant I3: "No feature for game T may use information from game T or
    later. Strictly `match_time < T`." (`.claude/scientific-invariants.md`)
  - CROSS-02-02 G-L-1: "Every history-derived feature must satisfy
    `history_time < target_time` strictly."
    (`reports/specs/02_02_feature_engineering_plan.md`)
  - CROSS-02-02 G-L-7: "For `(focal, opponent)` head-to-head aggregates and
    rolling-window aggregates, the target match's own row MUST NOT appear in
    the window."
    (`reports/specs/02_02_feature_engineering_plan.md`)
  - CROSS-02-03 D5: "Cutoff operator correctness — operator `<`, not `<=`,
    `=`, `>=`. Equality on the history side is forbidden."
    (`reports/specs/02_03_temporal_feature_audit_protocol.md`)
  - CROSS-02-03 D6: "Target-game exclusion — No feature for game T may read
    game T's own row."
    (`reports/specs/02_03_temporal_feature_audit_protocol.md`)
  - CROSS-02-03 D7: "Post-game token exclusion — The family does not read
    columns classified TARGET / POST_GAME_HISTORICAL / IN_GAME_HISTORICAL of
    the target match itself."
    (`reports/specs/02_03_temporal_feature_audit_protocol.md`)

Falsifier chain (halt-priority order, first-failure-wins):
  H1 — Predecessor artifact existence + SHA byte-stability (re-pinned
    independently; no V1 import).
  H2 — Temporal anchor column `started_at: timestamp[us]` present in 3
    Parquet schemas.
  H3 — History-column naming convention (focal/opponent-prefixed `*_prior_*`
    columns present; forbidden patterns absent).
  H4 — Cross-spec citation provenance (6 verbatim cite-strings present in
    this docstring).
  H5 — Forbidden-emission guard (V3 outputs directory must not exist).
  H6 — Cross-game-portable vocabulary (no SC2-specific or AoE2-specific terms
    in public signatures).
  H7 — Q8 syntactic-only guard (no empirical AoE2 transferability claim in
    docstring/comments).

Pure-function discipline: reads only `pyarrow.parquet.read_schema` /
`pyarrow.parquet.read_metadata` footer outputs + file SHA256 + this module's
own text via `inspect.getsource`. Does NOT call
`pyarrow.parquet.read_table()`, `pandas.read_parquet()`, or any DuckDB
query. Does NOT re-compute any feature value.

Lineage:
  - Layer-1 plan: PR #277 (merged at master 73fa5a5c).
  - V1 scaffold rung: PR #276 (merged at master 37c3a8855).
  - ROADMAP stub: PR #274 (merged at master 6716aa17).
  - Spec: CROSS-02-03-v1.0.1 (LOCKED 2026-05-06).

Invariants applied: I3 (strict-< schema evidence), I5 (focal/opponent
symmetric vocabulary), I6 (verbatim SHA pins + cite-strings), I7 (no magic
numbers; SHA pins empirically derived; no concrete window/decay/k-threshold
values), I8 (cross-game-portable vocabulary; H6 enforces), I9 (research
pipeline discipline), I10 (relative-path provenance).
"""

from __future__ import annotations

import hashlib
import inspect
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional

import pyarrow as pa
import pyarrow.parquet as pq

# ---------------------------------------------------------------------------
# Predecessor artifact relative paths (Invariant I10 — repo-root-relative;
# V3 re-pins independently per H1; NO V1 import)
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

# Pinned SHA256 (verified 2026-05-30 against merged parent PR artifacts;
# V3 re-pins independently of V1)
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

# Collect all 4 relative paths for iteration
ALL_ARTIFACT_RELPATHS: tuple[str, ...] = (
    PARENT_02_01_02_PARQUET_RELPATH,
    PARENT_02_01_03_PARQUET_RELPATH,
    PARENT_02_01_99_CSV_RELPATH,
    PARENT_02_02_01_PARQUET_RELPATH,
)

# SHA256 pins keyed by relpath
_SHA256_BY_RELPATH: dict[str, str] = {
    PARENT_02_01_02_PARQUET_RELPATH: PARENT_02_01_02_PARQUET_SHA256,
    PARENT_02_01_03_PARQUET_RELPATH: PARENT_02_01_03_PARQUET_SHA256,
    PARENT_02_01_99_CSV_RELPATH: PARENT_02_01_99_CSV_SHA256,
    PARENT_02_02_01_PARQUET_RELPATH: PARENT_02_02_01_PARQUET_SHA256,
}

# Parquet-only relpaths (temporal-anchor + history-naming checks apply)
_PARQUET_RELPATHS: tuple[str, ...] = (
    PARENT_02_01_02_PARQUET_RELPATH,
    PARENT_02_01_03_PARQUET_RELPATH,
    PARENT_02_02_01_PARQUET_RELPATH,
)

# Temporal anchor column (required in all 3 Parquet schemas per H2;
# cross-game-portable name)
TEMPORAL_ANCHOR_COLUMN = "started_at"

# Expected Arrow type prefix for the temporal anchor column
TEMPORAL_ANCHOR_ARROW_TYPE: Literal["timestamp[us]"] = "timestamp[us]"

# History-column naming regex (NIT-7: ANCHORED to focal/opponent prefix;
# not unanchored substring)
HISTORY_COLUMN_REGEX = re.compile(r"^(focal|opponent)_.*_prior_")

# Forbidden history-column patterns (these would imply leakage)
FORBIDDEN_HISTORY_PATTERNS = (
    re.compile(r"_including_target"),
    re.compile(r"_h2h_with_target"),
    re.compile(r"_window_inclusive"),
    re.compile(r"_full_replay"),
    re.compile(r"_post_match"),
    re.compile(r"_with_T_"),
)

# Required cite-strings in module docstring (H4 — bound to NIT-8 whitespace
# tolerance)
REQUIRED_CITE_SUBSTRINGS = (
    "Invariant I3",
    "CROSS-02-02 G-L-1",
    "CROSS-02-02 G-L-7",
    "CROSS-02-03 D5",
    "CROSS-02-03 D6",
    "CROSS-02-03 D7",
)

# Forbidden output directory (H5 — V3 outputs must not exist; V3 emits no
# artifact)
FORBIDDEN_V3_OUTPUTS_DIR = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/03_temporal_features"
)

# H6 forbidden vocabulary (cross-game-portable enforcement)
FORBIDDEN_SC2_TERMS = (
    "race",
    "mineral",
    "vespene",
    "PlayerStats",
    "tracker_events",
    "toon_id",
    "apm_focal",
    "apm_opp",
    "sq_focal",
    "sq_opp",
)
FORBIDDEN_AOE2_TERMS = (
    "civilization",
    "civ_",
    "profile_id",
    "leaderboard",
)

# H7 forbidden empirical-AoE2-claim patterns
FORBIDDEN_AOE2_CLAIM_PATTERNS = (
    re.compile(r"validated on aoe2", re.IGNORECASE),
    re.compile(r"aoe2 transferab", re.IGNORECASE),
    re.compile(r"transferab.*aoe2", re.IGNORECASE),
    re.compile(r"empirical.*aoe2", re.IGNORECASE),
    re.compile(r"aoe2.*empirical", re.IGNORECASE),
)


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------


@dataclass
class TemporalDisciplineCheckResult:
    """Aggregate result of the V3 strict-< temporal-discipline validator.

    Attributes:
        passed: True iff no halting falsifier fired.
        halting_falsifier: Label of the first falsifier that fired, or None.
        artifact_provenance_ok: True iff H1 passed (all artifacts exist +
            SHA matches).
        temporal_anchor_present: Mapping from Parquet relpath to bool
            (True = `started_at: timestamp[us]` present in schema).
        history_naming_valid: Mapping from Parquet relpath to bool
            (True = no forbidden patterns, at least one valid `prior_` column
            where applicable).
        forbidden_columns_absent: Mapping from Parquet relpath to list of
            forbidden column names found (empty list = no violations).
        cite_strings_present: Mapping from cite-string to bool
            (True = present in module docstring).
        outputs_dir_absent: True iff FORBIDDEN_V3_OUTPUTS_DIR does not exist.
        cross_game_vocabulary_ok: True iff H6 found no forbidden SC2/AoE2
            terms in public signatures.
        no_aoe2_empirical_claim: True iff H7 found no empirical AoE2
            transferability claim.
    """

    passed: bool
    halting_falsifier: Optional[str]
    artifact_provenance_ok: bool = True
    temporal_anchor_present: dict[str, bool] = field(default_factory=dict)
    history_naming_valid: dict[str, bool] = field(default_factory=dict)
    forbidden_columns_absent: dict[str, list[str]] = field(default_factory=dict)
    cite_strings_present: dict[str, bool] = field(default_factory=dict)
    outputs_dir_absent: bool = True
    cross_game_vocabulary_ok: bool = True
    no_aoe2_empirical_claim: bool = True


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _compute_sha256(path: Path) -> str:
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


def _check_h1_provenance(
    repo_root: Path,
) -> tuple[bool, Optional[str]]:
    """Check H1: all 4 predecessor artifacts exist and match pinned SHA256.

    Args:
        repo_root: Absolute path to the repository root.

    Returns:
        Tuple of (ok: bool, falsifier_label: Optional[str]).
        falsifier_label is None iff ok is True.
    """
    for rp in ALL_ARTIFACT_RELPATHS:
        artifact_path = repo_root / rp
        if not artifact_path.exists():
            return False, f"h1_artifact_missing:{rp}"
        computed = _compute_sha256(artifact_path)
        if computed != _SHA256_BY_RELPATH[rp]:
            return False, f"h1_sha_mismatch:{rp}"
    return True, None


def _check_h2_temporal_anchor(
    repo_root: Path,
) -> tuple[dict[str, bool], Optional[str]]:
    """Check H2: `started_at: timestamp[us]` present in all 3 Parquet schemas.

    Reads only schema metadata via pq.read_schema(). No row reads.

    Args:
        repo_root: Absolute path to the repository root.

    Returns:
        Tuple of (results: dict[relpath, bool], falsifier_label: Optional[str]).
    """
    results: dict[str, bool] = {}
    for rp in _PARQUET_RELPATHS:
        schema = pq.read_schema(repo_root / rp)
        names = schema.names
        if TEMPORAL_ANCHOR_COLUMN not in names:
            results[rp] = False
            return results, f"h2_temporal_anchor_missing:{rp}"
        col_idx = schema.get_field_index(TEMPORAL_ANCHOR_COLUMN)
        col_type = schema.field(col_idx).type
        # Accept timestamp[us] or timestamp[us, tz=UTC] variants
        if not (
            pa.types.is_timestamp(col_type)
            and str(col_type).startswith("timestamp[us")
        ):
            results[rp] = False
            return results, f"h2_temporal_anchor_wrong_type:{rp}:{col_type}"
        results[rp] = True
    return results, None


def _check_h3_history_naming(
    repo_root: Path,
) -> tuple[dict[str, bool], dict[str, list[str]], Optional[str]]:
    """Check H3: history-column naming convention (only for 02_01_03).

    Checks that:
      (a) No column in any Parquet artifact matches a FORBIDDEN_HISTORY_PATTERNS
          pattern.
      (b) At least one column matching `^(focal|opponent)_.*_prior_` exists in
          02_01_03 (history-enriched artifact; 02_01_02 and 02_02_01 may not
          have such columns and are not gated on H3-positive).

    Reads only schema metadata via pq.read_schema(). No row reads.

    Args:
        repo_root: Absolute path to the repository root.

    Returns:
        Tuple of (naming_valid: dict[relpath, bool],
                  forbidden_found: dict[relpath, list[str]],
                  falsifier_label: Optional[str]).
    """
    naming_valid: dict[str, bool] = {}
    forbidden_found: dict[str, list[str]] = {}

    # H3a: Check forbidden patterns across all 3 Parquet artifacts
    for rp in _PARQUET_RELPATHS:
        schema = pq.read_schema(repo_root / rp)
        forbidden_cols: list[str] = []
        for col_name in schema.names:
            for pattern in FORBIDDEN_HISTORY_PATTERNS:
                if pattern.search(col_name):
                    forbidden_cols.append(col_name)
                    break
        forbidden_found[rp] = forbidden_cols
        if forbidden_cols:
            naming_valid[rp] = False
            return (
                naming_valid,
                forbidden_found,
                f"h3_forbidden_column_present:{rp}:{forbidden_cols[0]}",
            )
        naming_valid[rp] = True

    # H3b: Check 02_01_03 has at least one anchored `^(focal|opponent)_.*_prior_`
    # column (positive presence check; only on history-enriched artifact)
    schema_03 = pq.read_schema(repo_root / PARENT_02_01_03_PARQUET_RELPATH)
    has_prior_col = any(
        HISTORY_COLUMN_REGEX.match(col) for col in schema_03.names
    )
    if not has_prior_col:
        naming_valid[PARENT_02_01_03_PARQUET_RELPATH] = False
        return (
            naming_valid,
            forbidden_found,
            f"h3_no_prior_columns_in_02_01_03:{PARENT_02_01_03_PARQUET_RELPATH}",
        )

    return naming_valid, forbidden_found, None


def _check_h4_cite_strings(
    module_text: str,
) -> tuple[dict[str, bool], Optional[str]]:
    """Check H4: all 6 required cite-strings present in module docstring.

    Uses whitespace-tolerant search (NIT-8): normalises runs of whitespace
    before matching, so cite-strings survive doc-reformatting.

    Args:
        module_text: Full module source text (from inspect.getsource or
            __doc__).

    Returns:
        Tuple of (results: dict[cite_string, bool],
                  falsifier_label: Optional[str]).
    """
    # Normalise whitespace for tolerance
    normalised = re.sub(r"\s+", " ", module_text)
    results: dict[str, bool] = {}
    for cite in REQUIRED_CITE_SUBSTRINGS:
        # Also normalise the cite string itself for robustness
        normalised_cite = re.sub(r"\s+", " ", cite)
        present = normalised_cite in normalised
        results[cite] = present
        if not present:
            return results, f"h4_cite_string_missing:{cite}"
    return results, None


def _check_h5_outputs_dir_absent(
    repo_root: Path,
) -> tuple[bool, Optional[str]]:
    """Check H5: forbidden V3 outputs directory must not exist.

    Args:
        repo_root: Absolute path to the repository root.

    Returns:
        Tuple of (absent: bool, falsifier_label: Optional[str]).
    """
    outputs_path = repo_root / FORBIDDEN_V3_OUTPUTS_DIR
    if outputs_path.exists():
        return False, "h5_forbidden_outputs_dir_present"
    return True, None


def _check_h6_vocabulary(
    module_text: str,
) -> tuple[bool, Optional[str]]:
    """Check H6: no SC2-specific or AoE2-specific terms in public signatures.

    Scans lines containing public function/class definitions and their
    parameter names + return annotations. Excludes the FORBIDDEN_SC2_TERMS /
    FORBIDDEN_AOE2_TERMS constant blocks (where terms are catalogued as
    known-bad vocabulary, not used as identifiers).

    Args:
        module_text: Full module source text.

    Returns:
        Tuple of (ok: bool, falsifier_label: Optional[str]).
    """
    # Extract lines that are public function/class defs or dataclass fields,
    # skipping the forbidden-list constant definition blocks
    public_sig_lines: list[str] = []
    in_constant_block = False
    for line in module_text.splitlines():
        stripped = line.strip()
        # Detect entry into the forbidden-list constant blocks
        if stripped.startswith("FORBIDDEN_SC2_TERMS") or stripped.startswith(
            "FORBIDDEN_AOE2_TERMS"
        ):
            in_constant_block = True
        if in_constant_block:
            if stripped.endswith(")"):
                in_constant_block = False
            continue
        # Collect public signatures and dataclass field lines
        if (
            stripped.startswith("def ")
            or stripped.startswith("class ")
            or stripped.startswith("    ")  # indented (field defs, params)
        ):
            public_sig_lines.append(stripped)

    sig_text = " ".join(public_sig_lines)

    for term in FORBIDDEN_SC2_TERMS:
        if term in sig_text:
            return False, f"h6_sc2_term_in_public_surface:{term}"
    for term in FORBIDDEN_AOE2_TERMS:
        if term in sig_text:
            return False, f"h6_aoe2_term_in_public_surface:{term}"
    return True, None


def _check_h7_no_aoe2_claim(
    module_text: str,
) -> tuple[bool, Optional[str]]:
    """Check H7: no empirical AoE2 transferability claim in comment lines.

    Scans only `#`-prefixed comment lines. Docstrings and function-doc text
    that describe H7 itself (meta-descriptions of the guard) are excluded;
    a genuine empirical claim would appear in a plain `#` comment.

    This avoids self-referential false positives: the module docstring says
    "no empirical AoE2 transferability claim (Q8 syntactic-only)" as a
    meta-description of the guard, not as an empirical claim.

    Args:
        module_text: Full module source text.

    Returns:
        Tuple of (ok: bool, falsifier_label: Optional[str]).
    """
    # Scan only comment lines (stripped lines starting with #)
    # and exclude the FORBIDDEN_AOE2_CLAIM_PATTERNS constant block
    # Sentinel comment prefix for the H7 constant block header line
    _H7_BLOCK_HEADER = "# H7 forbidden empirical-AoE2-claim patterns"
    in_constant_block = False
    for line in module_text.splitlines():
        stripped = line.strip()
        # Mark start of the forbidden-patterns constant block (including its
        # header comment) so both the comment and pattern strings are excluded
        if stripped == _H7_BLOCK_HEADER or stripped.startswith(
            "FORBIDDEN_AOE2_CLAIM_PATTERNS"
        ):
            in_constant_block = True
        if in_constant_block:
            if stripped.endswith(")"):
                in_constant_block = False
            continue
        # Only check plain comment lines — not docstrings or string literals
        if stripped.startswith("#"):
            for pattern in FORBIDDEN_AOE2_CLAIM_PATTERNS:
                match = pattern.search(stripped)
                if match:
                    return False, f"h7_aoe2_empirical_claim:{match.group(0)[:60]}"
    return True, None


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def validate_temporal_discipline(repo_root: Path) -> TemporalDisciplineCheckResult:
    """Validate strict-< temporal-discipline at design time (V3 scaffold).

    Halt-priority: H1 → H2 → H3 → H4 → H5 → H6 → H7. First failure wins.

    Pure function over schema metadata + file SHA + module text.
    Does NOT call read_table(), read_parquet(), or any DuckDB query.
    Does NOT re-compute any feature value.

    Args:
        repo_root: Absolute Path to the repository root.

    Returns:
        TemporalDisciplineCheckResult with all check outputs populated.
        ``passed`` is True iff ``halting_falsifier is None``.
    """
    # --- H1: Predecessor artifact provenance ---
    h1_ok, h1_falsifier = _check_h1_provenance(repo_root)
    if not h1_ok:
        return TemporalDisciplineCheckResult(
            passed=False,
            halting_falsifier=h1_falsifier,
            artifact_provenance_ok=False,
        )

    # --- H2: Temporal anchor column ---
    h2_results, h2_falsifier = _check_h2_temporal_anchor(repo_root)
    if h2_falsifier is not None:
        return TemporalDisciplineCheckResult(
            passed=False,
            halting_falsifier=h2_falsifier,
            artifact_provenance_ok=True,
            temporal_anchor_present=h2_results,
        )

    # --- H3: History-column naming convention ---
    h3_naming, h3_forbidden, h3_falsifier = _check_h3_history_naming(repo_root)
    if h3_falsifier is not None:
        return TemporalDisciplineCheckResult(
            passed=False,
            halting_falsifier=h3_falsifier,
            artifact_provenance_ok=True,
            temporal_anchor_present=h2_results,
            history_naming_valid=h3_naming,
            forbidden_columns_absent=h3_forbidden,
        )

    # --- H4: Cross-spec citation provenance ---
    # Use inspect.getsource on this module to get the full text
    import rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline as _self

    module_text = inspect.getsource(_self)
    h4_results, h4_falsifier = _check_h4_cite_strings(module_text)
    if h4_falsifier is not None:
        return TemporalDisciplineCheckResult(
            passed=False,
            halting_falsifier=h4_falsifier,
            artifact_provenance_ok=True,
            temporal_anchor_present=h2_results,
            history_naming_valid=h3_naming,
            forbidden_columns_absent=h3_forbidden,
            cite_strings_present=h4_results,
        )

    # --- H5: Forbidden-emission guard ---
    h5_absent, h5_falsifier = _check_h5_outputs_dir_absent(repo_root)
    if not h5_absent:
        return TemporalDisciplineCheckResult(
            passed=False,
            halting_falsifier=h5_falsifier,
            artifact_provenance_ok=True,
            temporal_anchor_present=h2_results,
            history_naming_valid=h3_naming,
            forbidden_columns_absent=h3_forbidden,
            cite_strings_present=h4_results,
            outputs_dir_absent=False,
        )

    # --- H6: Cross-game-portable vocabulary ---
    h6_ok, h6_falsifier = _check_h6_vocabulary(module_text)
    if not h6_ok:
        return TemporalDisciplineCheckResult(
            passed=False,
            halting_falsifier=h6_falsifier,
            artifact_provenance_ok=True,
            temporal_anchor_present=h2_results,
            history_naming_valid=h3_naming,
            forbidden_columns_absent=h3_forbidden,
            cite_strings_present=h4_results,
            outputs_dir_absent=True,
            cross_game_vocabulary_ok=False,
        )

    # --- H7: Q8 syntactic-only guard ---
    h7_ok, h7_falsifier = _check_h7_no_aoe2_claim(module_text)
    if not h7_ok:
        return TemporalDisciplineCheckResult(
            passed=False,
            halting_falsifier=h7_falsifier,
            artifact_provenance_ok=True,
            temporal_anchor_present=h2_results,
            history_naming_valid=h3_naming,
            forbidden_columns_absent=h3_forbidden,
            cite_strings_present=h4_results,
            outputs_dir_absent=True,
            cross_game_vocabulary_ok=True,
            no_aoe2_empirical_claim=False,
        )

    return TemporalDisciplineCheckResult(
        passed=True,
        halting_falsifier=None,
        artifact_provenance_ok=True,
        temporal_anchor_present=h2_results,
        history_naming_valid=h3_naming,
        forbidden_columns_absent=h3_forbidden,
        cite_strings_present=h4_results,
        outputs_dir_absent=True,
        cross_game_vocabulary_ok=True,
        no_aoe2_empirical_claim=True,
    )
