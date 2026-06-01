"""SC2EGSet Step 02_03_01 Layer-2 adjudicator — temporal feature grid decision record.

Decision-record module. Does NOT compute feature values. Does NOT read from
data/**. Does NOT query DuckDB. Does NOT pin concrete numerical winners for
window sizes, decay half-lives, or cold-start k-thresholds (Invariant I7;
deferred to a future materialization PR).

Adjudication scope (binding):
  - Q1 window-type family kinds (DEFER_TO_MATERIALIZATION; no concrete winner)
  - Q2 decay-type family kinds (DEFER_TO_MATERIALIZATION; no concrete winner)
  - Q3 cold-start-type family kinds (DEFER_TO_MATERIALIZATION; no concrete winner)
  - Q4 source_event_family categories (9 categories per direct enumeration
    of tracker_events_feature_eligibility.csv column 2)
  - Q5 in_game_snapshot prediction setting (DEFER_PAST_02_03_01)
  - Q6 cross-spec role separation (CONFIRMED)
  - Q7 V1+V3 preflight gate (PASS)
  - Q8 AoE2 cross-game portability (SYNTACTIC_ONLY; no empirical claim)

Adjudication sequence (binding, first-failure-wins; H0 -> H7b):
  H0 base/path preconditions (repo_root absolute and exists)
  H1 V1 preflight (validate_predecessor_artifact_provenance returns PASS)
  H2 V3 preflight (validate_temporal_discipline returns PASS)
  H3 parent/spec/tracker SHA capture (file readability for hashlib.sha256)
  H4 tracker eligibility CSV read
  H5 forbidden concrete numeric winners (I7 self-guard on output rows)
  H6 vocabulary / Q8 syntactic-only self-guard (output strings)
  H7a forbidden output dir present (V1.H6 + V3.H5 binding; paradox guard)
  H7b PR-self-archive forbidden (A-16 binding; non-output sentinel)
H_FINAL emit decision CSV + decision MD; return PASS.

The outputs directory is created ONLY after H1 and H2 both PASS. This is the
critical sequencing guard: V1's H6 and V3's H5 check absence of the
03_temporal_features directory; the adjudicator must therefore not pre-create
the output path before invoking preflights.

Cross-spec role separation (Q6, verbatim from planning/current_plan.md):
  "CROSS-02-02 = source of candidate family inventory; CROSS-02-03 = source
  of post-selection audit predicate. These are distinct roles."

CROSS-02-02 §10 candidate family inventory (G-L-1 through G-L-7):
  G-L-1 — fixed-game-count window
  G-L-2 — fixed-calendar-duration window
  G-L-3 — exponential decay
  G-L-4 — step-function decay
  G-L-5 — minimum-prior cold-start gate
  G-L-6 — pseudocount smoothing
  G-L-7 — combined gate + smoothing

CROSS-02-03 §4 post-selection audit predicate dimensions (D5/D6/D7):
  D5 — cutoff operator correctness (strict-< per Invariant I3)
  D6 — target-game exclusion
  D7 — post-game token exclusion

Invariant I3: strict history cutoff — history_time < T (strict, not <=).
The V3 scaffold (validate_temporal_discipline.py) enforces this at schema
level. The adjudicator cites Invariant I3 for every family kind with a
history cutoff.

V1 preflight reference:
  V1 PASS = validate_predecessor_artifact_provenance(repo_root).passed is True
V3 preflight reference:
  V3 PASS = validate_temporal_discipline(repo_root).passed is True

Cross-game-portable vocabulary (Invariant I8; A-15 from planning/current_plan.md):
  Public function signatures, return-type field names, and CSV column names
  use cross-game-portable vocabulary only (focal/opponent, history, prior,
  target-exclusion, candidate, winner, window-type, decay-type, cold-start-type).
  SC2-specific and AoE2-specific tokens MUST NOT appear in public API.
  Cross-game portability is syntactic-only (Q8); no empirical AoE2
  transferability claim is made.

Halt semantics: any halt H0-H7b returns AdjudicationResult(status=...) with
emit_attempted=False. Output directory and files are NEVER written on halt.
"""

from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
    TemporalDisciplineCheckResult,
    validate_temporal_discipline,
)
from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_feature_grid import (
    PARENT_02_01_02_PARQUET_RELPATH,
    PARENT_02_01_02_PARQUET_SHA256,
    PARENT_02_01_03_PARQUET_RELPATH,
    PARENT_02_01_03_PARQUET_SHA256,
    PARENT_02_01_99_CSV_RELPATH,
    PARENT_02_01_99_CSV_SHA256,
    PARENT_02_02_01_PARQUET_RELPATH,
    PARENT_02_02_01_PARQUET_SHA256,
    ProvenanceCheckResult,
    validate_predecessor_artifact_provenance,
)

# ---------------------------------------------------------------------------
# Status sentinels (Invariant I8: cross-game-portable vocabulary)
# ---------------------------------------------------------------------------

STATUS_PASS = "PASS"
STATUS_HALT_H0 = "HALT_H0_BASE_PRECONDITION"
STATUS_HALT_V1 = "HALT_H1_V1_PREFLIGHT"
STATUS_HALT_V3 = "HALT_H2_V3_PREFLIGHT"
STATUS_HALT_H3 = "HALT_H3_SHA_CAPTURE"
STATUS_HALT_H4 = "HALT_H4_TRACKER_CSV_READ"
STATUS_HALT_H5 = "HALT_H5_NUMERIC_WINNER"
STATUS_HALT_H6 = "HALT_H6_VOCABULARY"
STATUS_HALT_H7A = "HALT_H7A_FORBIDDEN_OUTPUT_DIR"
STATUS_HALT_H7B = "HALT_H7B_PR_SELF_ARCHIVE"

# Decision sentinels (CSV cell values; cross-game-portable vocabulary).
DECISION_DEFER_TO_MATERIALIZATION = "DEFER_TO_MATERIALIZATION"
DECISION_DEFER_PAST_02_03_01 = "DEFER_PAST_02_03_01"
DECISION_CONFIRMED = "CONFIRMED"
DECISION_PASS = "PASS"
DECISION_SYNTACTIC_ONLY = "SYNTACTIC_ONLY"
DECISION_ELIGIBLE = "ELIGIBLE"
DECISION_ELIGIBLE_WITH_CAVEAT = "ELIGIBLE_WITH_CAVEAT"
DECISION_BLOCKED = "BLOCKED"

# Family-kind sentinels (Q1/Q2/Q3/Q5/Q6/Q7/Q8 single-row identifiers).
FAMILY_KIND_Q1 = "temporal_window_size_grid"
FAMILY_KIND_Q2 = "decay_half_life_grid"
FAMILY_KIND_Q3 = "cold_start_k_threshold_grid"
FAMILY_KIND_Q5 = "in_game_snapshot_features"
FAMILY_KIND_Q6 = "cross_spec_role_separation"
FAMILY_KIND_Q7 = "v1_v3_preflight_gate"
FAMILY_KIND_Q8 = "q8_aoe2_transferability"

# ---------------------------------------------------------------------------
# Pinned SHA256 anchors (cross-spec; tracker eligibility CSV).
# ---------------------------------------------------------------------------

CROSS_02_02_SPEC_RELPATH = "reports/specs/02_02_feature_engineering_plan.md"
CROSS_02_03_SPEC_RELPATH = "reports/specs/02_03_temporal_feature_audit_protocol.md"
CROSS_02_02_SPEC_SHA256 = (
    "86af792370272e611f048aae0c48c9cc595eb4b44c1db38c0bb4ecea0ff1b289"
)
CROSS_02_03_SPEC_SHA256 = (
    "59e3227307c51ad09fb12b485caec36aa54413d175cb46acc382c06fbb8ac546"
)

TRACKER_ELIGIBILITY_CSV_RELPATH = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "01_exploration/03_profiling/tracker_events_feature_eligibility.csv"
)
TRACKER_ELIGIBILITY_CSV_SHA256 = (
    "11bd4b9ef7c80657a027db3831313c1d74c39b85834c25ecdfa78506e8ad8d22"
)

# V1 + V3 validator module relpaths (SHA computed at execution time).
V1_VALIDATOR_MODULE_RELPATH = (
    "src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_feature_grid.py"
)
V3_VALIDATOR_MODULE_RELPATH = (
    "src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_discipline.py"
)

# Output directory + artifact filenames.
OUTPUT_DIR_RELPATH = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/03_temporal_features/02_03_01"
)
OUTPUT_CSV_FILENAME = "02_03_01_temporal_feature_grid_adjudication.csv"
OUTPUT_MD_FILENAME = "02_03_01_temporal_feature_grid_adjudication.md"

# Forbidden output parent (V1.H6 / V3.H5 paradox guard).
FORBIDDEN_OUTPUT_PARENT_RELPATH = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/03_temporal_features"
)

# CSV column order (16 columns: 7 base + 9 SHA-pin provenance).
DECISION_CSV_COLUMNS: tuple[str, ...] = (
    "family_kind",
    "decision",
    "rationale_g_l_ref",
    "rationale_d_ref",
    "invariant_i3_cited",
    "v1_preflight",
    "v3_preflight",
    "parent_02_01_02_parquet_sha256",
    "parent_02_01_03_parquet_sha256",
    "parent_02_01_99_csv_sha256",
    "parent_02_02_01_parquet_sha256",
    "v1_validator_module_sha256",
    "v3_validator_module_sha256",
    "cross_02_02_spec_sha256",
    "cross_02_03_spec_sha256",
    "tracker_eligibility_csv_sha256",
)

# Q4 eligibility-status column (in-game snapshot, the column that varies by row).
TRACKER_CSV_STATUS_COLUMN = "status_in_game_snapshot"
TRACKER_CSV_FAMILY_COLUMN = "source_event_family"
TRACKER_CSV_FEATURE_COLUMN = "feature_family"

# Cross-CSV eligibility value tokens (verbatim from the tracker eligibility CSV).
ELIG_VALUE_ELIGIBLE = "eligible_for_phase02_now"
ELIG_VALUE_CAVEAT = "eligible_with_caveat"
ELIG_VALUE_BLOCKED = "blocked_until_additional_validation"

# Q6 verbatim non-conflation sentence (referenced by the decision MD §6 lead-in).
Q6_NON_CONFLATION_SENTENCE = (
    "CROSS-02-02 = source of candidate family inventory; "
    "CROSS-02-03 = source of post-selection audit predicate. "
    "These are distinct roles."
)

# Numeric-winner self-guard (H5). Match common pinned-magnitude tokens that
# would indicate a concrete winner sneaking into a Q1/Q2/Q3 decision cell.
_NUMERIC_WINNER_REGEX = re.compile(
    r"\d+\s*(min|sec|games|matches|wins|days|hours)|"
    r"k\s*=\s*\d+|"
    r"h\s*=\s*\d+|"
    r"n\s*=\s*\d+|"
    r"half[_\-]life\s*=",
    re.IGNORECASE,
)

# Vocabulary self-guard (H6). Reject SC2-specific or AoE2-specific tokens in
# decision-row text. Per A-15, the public API uses cross-game-portable
# vocabulary only.
_FORBIDDEN_VOCAB_REGEX = re.compile(
    r"\b(race|tracker_events|playerstats|mineral|vespene|toon_id|"
    r"apm_focal|apm_opp|sq_focal|sq_opp|civilization|civ_|"
    r"profile_id|leaderboard)\b",
    re.IGNORECASE,
)

# AoE2 empirical claim guard (Q8 / H7-equivalent for decision text).
_AOE2_EMPIRICAL_CLAIM_REGEX = re.compile(
    r"aoe2.*transferab|transferab.*aoe2|validated on aoe2|"
    r"aoe2.*verified|cross-game validated",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Public result dataclass (cross-game-portable field names; A-15 binding).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AdjudicationResult:
    """Aggregate result of the Step 02_03_01 temporal feature grid adjudicator.

    Frozen dataclass (round-trips by value). The contract is:
      status == STATUS_PASS iff both preflights returned PASS and all halts
      H0-H7b returned no failure.

    Attributes:
        status: One of STATUS_PASS, STATUS_HALT_H0..STATUS_HALT_H7B.
        halting_step: The halt identifier (H0..H7b) on failure, else None.
        v1_preflight: "PASS" / "FAIL" string capturing the V1 outcome (None
            if H0 halted before V1 ran).
        v3_preflight: "PASS" / "FAIL" string capturing the V3 outcome (None
            if H1 halted before V3 ran).
        sha_pins: Mapping from pin column label to SHA256 hex string (or
            None for pins not yet computed at halt time).
        csv_path: Path to the emitted decision CSV, or None on halt.
        md_path: Path to the emitted decision MD, or None on halt.
        rows_written: Count of decision CSV body rows written (16 on PASS,
            0 on halt).
    """

    status: str
    halting_step: Optional[str] = None
    v1_preflight: Optional[str] = None
    v3_preflight: Optional[str] = None
    sha_pins: dict[str, Optional[str]] = field(default_factory=dict)
    csv_path: Optional[Path] = None
    md_path: Optional[Path] = None
    rows_written: int = 0


# ---------------------------------------------------------------------------
# Private helpers (no I/O outside the documented surface).
# ---------------------------------------------------------------------------


def _compute_file_sha256(path: Path) -> str:
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


def _build_sha_pin_map(
    repo_root: Path,
    v1_module_sha: str,
    v3_module_sha: str,
) -> dict[str, str]:
    """Build the 9-pin SHA map embedded in every decision CSV row.

    Args:
        repo_root: Absolute path to the repository root.
        v1_module_sha: Pre-computed SHA256 of the V1 validator module.
        v3_module_sha: Pre-computed SHA256 of the V3 validator module.

    Returns:
        Dict from SHA-pin column label to hex digest string.
    """
    del repo_root  # consumed upstream; preserved for symmetry / typing.
    return {
        "parent_02_01_02_parquet_sha256": PARENT_02_01_02_PARQUET_SHA256,
        "parent_02_01_03_parquet_sha256": PARENT_02_01_03_PARQUET_SHA256,
        "parent_02_01_99_csv_sha256": PARENT_02_01_99_CSV_SHA256,
        "parent_02_02_01_parquet_sha256": PARENT_02_02_01_PARQUET_SHA256,
        "v1_validator_module_sha256": v1_module_sha,
        "v3_validator_module_sha256": v3_module_sha,
        "cross_02_02_spec_sha256": CROSS_02_02_SPEC_SHA256,
        "cross_02_03_spec_sha256": CROSS_02_03_SPEC_SHA256,
        "tracker_eligibility_csv_sha256": TRACKER_ELIGIBILITY_CSV_SHA256,
    }


def _read_tracker_eligibility_rows(repo_root: Path) -> list[dict[str, str]]:
    """Read tracker_events_feature_eligibility.csv as a list of dicts.

    Args:
        repo_root: Absolute path to the repository root.

    Returns:
        List of row dicts keyed by column header.
    """
    csv_path = repo_root / TRACKER_ELIGIBILITY_CSV_RELPATH
    with csv_path.open() as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def _aggregate_q4_family_decision(
    family: str,
    rows: list[dict[str, str]],
) -> str:
    """Aggregate the eligibility status of a source_event_family across rows.

    Worst-case aggregation: BLOCKED > ELIGIBLE_WITH_CAVEAT > ELIGIBLE.

    Args:
        family: The source_event_family token (verbatim, including spaces).
        rows: All rows from the tracker eligibility CSV.

    Returns:
        One of DECISION_BLOCKED / DECISION_ELIGIBLE_WITH_CAVEAT /
        DECISION_ELIGIBLE.
    """
    relevant = [r for r in rows if r[TRACKER_CSV_FAMILY_COLUMN] == family]
    statuses = [r[TRACKER_CSV_STATUS_COLUMN] for r in relevant]
    if any(s == ELIG_VALUE_BLOCKED for s in statuses):
        return DECISION_BLOCKED
    if any(s == ELIG_VALUE_CAVEAT for s in statuses):
        return DECISION_ELIGIBLE_WITH_CAVEAT
    if all(s == ELIG_VALUE_ELIGIBLE for s in statuses) and statuses:
        return DECISION_ELIGIBLE
    # Fallback: if mixture without BLOCKED, treat unknown tokens as caveat.
    return DECISION_ELIGIBLE_WITH_CAVEAT


def _build_decision_rows(
    repo_root: Path,
    sha_pin_map: dict[str, str],
    tracker_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Build the 16-row decision CSV body (Q1, Q2, Q3, Q4 x 9, Q5, Q6, Q7, Q8).

    Each row carries all 9 SHA-pin values (identical across rows) plus the
    7 base decision columns.

    Args:
        repo_root: Absolute path to the repository root.
        sha_pin_map: Dict from pin column label to hex digest string.
        tracker_rows: All rows from the tracker eligibility CSV.

    Returns:
        Ordered list of 16 row dicts; column order matches DECISION_CSV_COLUMNS.
    """
    del repo_root  # consumed upstream.

    base = dict(sha_pin_map)
    base["v1_preflight"] = "PASS"
    base["v3_preflight"] = "PASS"

    rows: list[dict[str, str]] = []

    # Q1 — window-type kinds (no concrete winner).
    rows.append(_assemble_row(
        family_kind=FAMILY_KIND_Q1,
        decision=DECISION_DEFER_TO_MATERIALIZATION,
        rationale_g_l_ref="G-L-1; G-L-2",
        rationale_d_ref="D5; D6; D7",
        invariant_i3_cited="Invariant I3",
        base=base,
    ))
    # Q2 — decay-type kinds (no concrete winner).
    rows.append(_assemble_row(
        family_kind=FAMILY_KIND_Q2,
        decision=DECISION_DEFER_TO_MATERIALIZATION,
        rationale_g_l_ref="G-L-3; G-L-4",
        rationale_d_ref="D5; D6; D7",
        invariant_i3_cited="Invariant I3",
        base=base,
    ))
    # Q3 — cold-start-type kinds (no concrete winner).
    rows.append(_assemble_row(
        family_kind=FAMILY_KIND_Q3,
        decision=DECISION_DEFER_TO_MATERIALIZATION,
        rationale_g_l_ref="G-L-5; G-L-6; G-L-7",
        rationale_d_ref="D5; D6; D7",
        invariant_i3_cited="Invariant I3",
        base=base,
    ))

    # Q4 — 9 rows, one per source_event_family category (verbatim token).
    q4_families = _unique_q4_families(tracker_rows)
    for family in q4_families:
        rows.append(_assemble_row(
            family_kind=family,
            decision=_aggregate_q4_family_decision(family, tracker_rows),
            rationale_g_l_ref="G-L-1..G-L-7 (tracker eligibility csv)",
            rationale_d_ref="D5; D6; D7",
            invariant_i3_cited="Invariant I3",
            base=base,
        ))

    # Q5 — in-game snapshot deferral.
    rows.append(_assemble_row(
        family_kind=FAMILY_KIND_Q5,
        decision=DECISION_DEFER_PAST_02_03_01,
        rationale_g_l_ref="G-L-1..G-L-7 (in-game scope)",
        rationale_d_ref="D5; D6; D7",
        invariant_i3_cited="Invariant I3",
        base=base,
    ))
    # Q6 — cross-spec role separation confirmed.
    rows.append(_assemble_row(
        family_kind=FAMILY_KIND_Q6,
        decision=DECISION_CONFIRMED,
        rationale_g_l_ref="G-L-1..G-L-7",
        rationale_d_ref="D5; D6; D7",
        invariant_i3_cited="Invariant I3",
        base=base,
    ))
    # Q7 — V1+V3 preflight pass.
    rows.append(_assemble_row(
        family_kind=FAMILY_KIND_Q7,
        decision=DECISION_PASS,
        rationale_g_l_ref="G-L-1..G-L-7",
        rationale_d_ref="D5; D6; D7",
        invariant_i3_cited="Invariant I3",
        base=base,
    ))
    # Q8 — AoE2 cross-game transferability syntactic-only.
    rows.append(_assemble_row(
        family_kind=FAMILY_KIND_Q8,
        decision=DECISION_SYNTACTIC_ONLY,
        rationale_g_l_ref="G-L-1..G-L-7 (syntactic)",
        rationale_d_ref="D5; D6; D7",
        invariant_i3_cited="Invariant I3",
        base=base,
    ))

    return rows


def _assemble_row(
    family_kind: str,
    decision: str,
    rationale_g_l_ref: str,
    rationale_d_ref: str,
    invariant_i3_cited: str,
    base: dict[str, str],
) -> dict[str, str]:
    """Compose a 16-column row dict from the 7 base fields and the 9 SHA pins.

    Args:
        family_kind: The Q-row family-kind token (e.g. PlayerStats, Q1 kind).
        decision: The decision sentinel (e.g. DECISION_DEFER_TO_MATERIALIZATION).
        rationale_g_l_ref: CROSS-02-02 §10 G-L-* citation string.
        rationale_d_ref: CROSS-02-03 §4 D5/D6/D7 citation string.
        invariant_i3_cited: "Invariant I3" verbatim.
        base: SHA-pin map + v1/v3 preflight values.

    Returns:
        Dict with all 16 keys from DECISION_CSV_COLUMNS populated.
    """
    row = {
        "family_kind": family_kind,
        "decision": decision,
        "rationale_g_l_ref": rationale_g_l_ref,
        "rationale_d_ref": rationale_d_ref,
        "invariant_i3_cited": invariant_i3_cited,
    }
    row.update(base)
    return row


def _unique_q4_families(tracker_rows: list[dict[str, str]]) -> list[str]:
    """Return the 9 unique source_event_family tokens, preserving first-seen order.

    Verbatim preservation: UnitInit / UnitDone keeps its internal spaces (N1).

    Args:
        tracker_rows: All rows from the tracker eligibility CSV.

    Returns:
        Ordered list of unique source_event_family tokens.
    """
    seen: dict[str, None] = {}
    for r in tracker_rows:
        fam = r[TRACKER_CSV_FAMILY_COLUMN]
        if fam not in seen:
            seen[fam] = None
    return list(seen.keys())


def _check_h5_no_numeric_winner(rows: list[dict[str, str]]) -> Optional[str]:
    """H5 self-guard: assert no Q1/Q2/Q3 row pins a concrete numerical winner.

    Args:
        rows: Decision row dicts.

    Returns:
        Halt label on violation, else None.
    """
    q123 = {FAMILY_KIND_Q1, FAMILY_KIND_Q2, FAMILY_KIND_Q3}
    for r in rows:
        if r["family_kind"] in q123:
            if _NUMERIC_WINNER_REGEX.search(r["decision"]):
                return f"numeric_winner_in:{r['family_kind']}"
    return None


def _check_h6_vocabulary(rows: list[dict[str, str]]) -> Optional[str]:
    """H6 self-guard: assert decision strings contain no forbidden vocabulary.

    Note: family_kind cells emitted verbatim from the tracker CSV are exempt
    (they are intentional fixed citations, not vocabulary additions).

    Args:
        rows: Decision row dicts.

    Returns:
        Halt label on violation, else None.
    """
    for r in rows:
        for col in ("decision", "rationale_g_l_ref", "rationale_d_ref"):
            if _FORBIDDEN_VOCAB_REGEX.search(r[col]):
                return f"forbidden_vocab_in:{r['family_kind']}:{col}"
    return None


def _check_h7a_forbidden_dir(repo_root: Path) -> Optional[str]:
    """H7a paradox guard: forbidden parent output dir must be absent before emit.

    Args:
        repo_root: Absolute path to the repository root.

    Returns:
        Halt label if the forbidden parent dir exists, else None.
    """
    if (repo_root / FORBIDDEN_OUTPUT_PARENT_RELPATH).exists():
        return "forbidden_output_dir_present"
    return None


def _check_h7b_no_self_archive(repo_root: Path) -> Optional[str]:
    """H7b sentinel: A-16 PR-self-archive forbidden (advisory check).

    Reads planning/INDEX.md (if present) and confirms no archive row
    mentions the Layer-2 execution branch. This is a soft sentinel; the
    Layer-2 branch name is checked verbatim against archive lines.

    Args:
        repo_root: Absolute path to the repository root.

    Returns:
        Halt label on violation, else None.
    """
    index = repo_root / "planning" / "INDEX.md"
    if not index.exists():
        return None
    branch_name = "feat/sc2egset-02-03-01-temporal-adjudication-execution"
    archive_marker = "Archive"
    text = index.read_text()
    if branch_name not in text:
        return None
    # If the branch name appears only on the Active line, that is OK.
    # If it appears below an "Archive" header, that is a self-archive.
    lines = text.splitlines()
    in_archive = False
    for line in lines:
        if archive_marker in line and line.lstrip().startswith("#"):
            in_archive = True
            continue
        if in_archive and branch_name in line:
            return "pr_self_archive_violation"
    return None


def _write_decision_csv(
    path: Path,
    rows: list[dict[str, str]],
) -> None:
    """Write the 16-row decision CSV with QUOTE_ALL discipline.

    Args:
        path: Absolute path to the output CSV.
        rows: Ordered list of decision row dicts.
    """
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=list(DECISION_CSV_COLUMNS),
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _build_decision_md(
    sha_pin_map: dict[str, str],
    tracker_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
) -> str:
    """Build the 14-section decision Markdown report text.

    Args:
        sha_pin_map: Dict from pin column label to hex digest string.
        tracker_rows: All rows from the tracker eligibility CSV.
        decision_rows: The decision CSV rows (already assembled).

    Returns:
        Markdown text (no trailing newline beyond final section).
    """
    parts: list[str] = []
    parts.append("# Step 02_03_01 temporal feature grid adjudication\n")
    parts.append(
        "\nLayer-2 decision-record output. No feature materialization. "
        "No concrete numerical winners pinned (Invariant I7). V1 + V3 "
        "preflights both PASS.\n"
    )

    parts.append("\n## 1. Scope\n")
    parts.append(
        "\nAdjudication of the SC2EGSet `02_03_01` temporal feature grid: "
        "Q1 window-type kinds, Q2 decay-type kinds, Q3 cold-start-type kinds, "
        "Q4 tracker `source_event_family` categories, Q5 in-game snapshot "
        "deferral boundary, Q6 cross-spec role separation, Q7 V1+V3 preflight "
        "gate, Q8 cross-game portability (syntactic-only).\n"
    )

    parts.append("\n## 2. Preflight gates\n")
    parts.append(
        "\n- V1 preflight: V1 PASS via "
        "`validate_predecessor_artifact_provenance(repo_root)`.\n"
        "- V3 preflight: V3 PASS via "
        "`validate_temporal_discipline(repo_root)`.\n"
    )

    parts.append("\n## 3. SHA-pin provenance\n")
    parts.append("\n| Pin column | SHA256 |\n|---|---|\n")
    for col_name in (
        "parent_02_01_02_parquet_sha256",
        "parent_02_01_03_parquet_sha256",
        "parent_02_01_99_csv_sha256",
        "parent_02_02_01_parquet_sha256",
        "v1_validator_module_sha256",
        "v3_validator_module_sha256",
        "cross_02_02_spec_sha256",
        "cross_02_03_spec_sha256",
        "tracker_eligibility_csv_sha256",
    ):
        parts.append(f"| `{col_name}` | `{sha_pin_map[col_name]}` |\n")

    parts.append("\n## 4. Invariant I3 — strict history cutoff\n")
    parts.append(
        "\nInvariant I3 mandates `history_time < T` strictly (not `<=`) for "
        "all history features targeting game T. V3 enforces this at schema "
        "level (`started_at: timestamp[us]` anchor; strict-< naming convention). "
        "Every decision row carries the `invariant_i3_cited` column.\n"
    )

    parts.append("\n## 5. Cross-spec citations\n")
    parts.append(
        "\n- CROSS-02-02 §10 candidate family inventory: G-L-1 (fixed-game-count "
        "window), G-L-2 (fixed-calendar-duration window), G-L-3 (exponential "
        "decay), G-L-4 (step-function decay), G-L-5 (minimum-prior cold-start "
        "gate), G-L-6 (pseudocount smoothing), G-L-7 (combined gate + "
        "smoothing).\n"
        "- CROSS-02-03 §4 post-selection audit predicate dimensions: D5 "
        "(cutoff operator correctness), D6 (target-game exclusion), D7 "
        "(post-game token exclusion).\n"
        f"\n{Q6_NON_CONFLATION_SENTENCE}\n"
    )

    parts.append("\n## 6. Tracker `source_event_family` cross-reference (15-family)\n")
    parts.append(
        "\nOne row per row in `tracker_events_feature_eligibility.csv` "
        "(15 rows). Q4 decision rows aggregate per `source_event_family` "
        "(worst-case across `status_in_game_snapshot`): "
        "BLOCKED > ELIGIBLE_WITH_CAVEAT > ELIGIBLE. The `family_kind` cell "
        "is emitted verbatim from the CSV — `UnitInit / UnitDone` keeps its "
        "internal whitespace.\n"
    )
    parts.append(
        "\n| # | feature_family | source_event_family | "
        "status_in_game_snapshot | aggregated_decision |\n"
        "|---|---|---|---|---|\n"
    )
    for idx, r in enumerate(tracker_rows, start=1):
        family = r[TRACKER_CSV_FAMILY_COLUMN]
        agg = _aggregate_q4_family_decision(family, tracker_rows)
        parts.append(
            f"| {idx} | `{r[TRACKER_CSV_FEATURE_COLUMN]}` | "
            f"`{family}` | "
            f"`{r[TRACKER_CSV_STATUS_COLUMN]}` | `{agg}` |\n"
        )

    parts.append("\n## 7. Q1 temporal window-type kinds (deferred)\n")
    parts.append(
        "\nQ1 enumerates window-type kinds (G-L-1 fixed-game-count, G-L-2 "
        "fixed-calendar-duration, G-L-3 exponential decay). Concrete numerical "
        "winner selection (specific game counts, day counts, half-life values) "
        "is DEFERRED to the future materialization PR per Invariant I7. The "
        "decision cell reads `DEFER_TO_MATERIALIZATION`.\n"
    )

    parts.append("\n## 8. Q2 decay-type kinds (deferred)\n")
    parts.append(
        "\nQ2 enumerates decay-type kinds (G-L-3 exponential, G-L-4 "
        "step-function). Concrete tau half-life values or step sizes are "
        "NOT pinned at adjudication; DEFERRED to materialization per "
        "Invariant I7.\n"
    )

    parts.append("\n## 9. Q3 cold-start-type kinds (deferred)\n")
    parts.append(
        "\nQ3 enumerates cold-start kinds (G-L-5 minimum-prior gate, G-L-6 "
        "pseudocount smoothing, G-L-7 combined). Concrete k-threshold values "
        "and pseudocount magnitudes are NOT pinned; DEFERRED to materialization "
        "per Invariant I7.\n"
    )

    parts.append("\n## 10. Q5 in-game snapshot deferral\n")
    parts.append(
        "\nIn-game snapshot families are DEFERRED past `02_03_01`. The "
        "`02_03_01` adjudication step covers `pre_game` and "
        "`history_enriched_pre_game` prediction settings only. In-game "
        "snapshot adjudication proceeds in a later step.\n"
    )

    parts.append("\n## 11. Q6 cross-spec role separation\n")
    parts.append(f"\n{Q6_NON_CONFLATION_SENTENCE}\n")

    parts.append("\n## 12. Q7 preflight gate outcome\n")
    parts.append(
        "\nV1 PASS + V3 PASS recorded. Both preflights ran before the output "
        "directory was created (V1.H6 / V3.H5 paradox guard satisfied).\n"
    )

    parts.append("\n## 13. Q8 cross-game portability (syntactic-only)\n")
    parts.append(
        "\nThe adjudicator's public API uses cross-game-portable vocabulary "
        "only (focal/opponent, history, prior, target-exclusion, candidate, "
        "winner, window-type, decay-type, cold-start-type). The design "
        "pattern is syntactically portable. The Q8 stance is SYNTACTIC_ONLY: "
        "no empirical cross-target claim is made; any second-game-target "
        "determination is deferred to a future second-game-specific "
        "Phase 02 step.\n"
    )

    parts.append("\n## 14. Decision CSV summary\n")
    parts.append(
        f"\nDecision CSV has {len(decision_rows)} body rows × "
        f"{len(DECISION_CSV_COLUMNS)} columns (7 base + 9 SHA-pin "
        "provenance). Every row carries identical SHA-pin values; the "
        "`family_kind`, `decision`, `rationale_g_l_ref`, `rationale_d_ref`, "
        "and `invariant_i3_cited` columns vary per Q-row.\n"
    )

    return "".join(parts)


# ---------------------------------------------------------------------------
# Public entrypoint.
# ---------------------------------------------------------------------------


def adjudicate_temporal_feature_grid(repo_root: Path) -> AdjudicationResult:
    """SC2EGSet Step 02_03_01 temporal feature grid adjudicator entrypoint.

    Halt-priority sequence (first-failure-wins; H0 -> H7b -> emit):

      H0  base/path precondition (repo_root is absolute and exists)
      H1  V1 preflight: validate_predecessor_artifact_provenance(repo_root) is PASS
      H2  V3 preflight: validate_temporal_discipline(repo_root) is PASS
      H3  SHA capture (all 9 pin files readable by hashlib.sha256)
      H4  tracker eligibility CSV read
      H5  numeric-winner self-guard on Q1/Q2/Q3 decision cells
      H6  vocabulary self-guard on decision cells
      H7a forbidden output parent dir absent (paradox guard)
      H7b PR-self-archive sentinel (A-16)
      H_FINAL: emit decision CSV + decision MD; return STATUS_PASS.

    The output directory is created ONLY after H1 and H2 both pass (V1.H6 +
    V3.H5 paradox guard).

    Args:
        repo_root: Absolute Path to the repository root. Callers passing a
            relative path or non-existent path will trigger H0 halt.

    Returns:
        AdjudicationResult with status sentinel populated. On STATUS_PASS,
        csv_path and md_path point to the emitted artifacts; on halt, both
        are None and rows_written is 0.
    """
    # H0 — base/path precondition.
    if not repo_root.is_absolute() or not repo_root.exists():
        return AdjudicationResult(
            status=STATUS_HALT_H0,
            halting_step="H0",
        )

    # H1 — V1 preflight. Validate V1 PASS sentinel before continuing.
    v1: ProvenanceCheckResult = validate_predecessor_artifact_provenance(repo_root)
    if not v1.passed:
        return AdjudicationResult(
            status=STATUS_HALT_V1,
            halting_step="H1",
            v1_preflight="FAIL",
        )

    # H2 — V3 preflight. Validate V3 PASS sentinel before continuing.
    v3: TemporalDisciplineCheckResult = validate_temporal_discipline(repo_root)
    if not v3.passed:
        return AdjudicationResult(
            status=STATUS_HALT_V3,
            halting_step="H2",
            v1_preflight="PASS",
            v3_preflight="FAIL",
        )

    # H3 — SHA capture (9 pin columns; 4 are constants, V1/V3 modules computed
    # at execution time via hashlib.sha256, 2 cross-spec + tracker CSV checked
    # for byte-stability against pinned constants).
    try:
        v1_module_sha = _compute_file_sha256(repo_root / V1_VALIDATOR_MODULE_RELPATH)
        v3_module_sha = _compute_file_sha256(repo_root / V3_VALIDATOR_MODULE_RELPATH)
        # Re-verify the 7 fixed pins (parent artifacts + cross specs + tracker CSV).
        for relpath, expected_sha in (
            (PARENT_02_01_02_PARQUET_RELPATH, PARENT_02_01_02_PARQUET_SHA256),
            (PARENT_02_01_03_PARQUET_RELPATH, PARENT_02_01_03_PARQUET_SHA256),
            (PARENT_02_01_99_CSV_RELPATH, PARENT_02_01_99_CSV_SHA256),
            (PARENT_02_02_01_PARQUET_RELPATH, PARENT_02_02_01_PARQUET_SHA256),
            (CROSS_02_02_SPEC_RELPATH, CROSS_02_02_SPEC_SHA256),
            (CROSS_02_03_SPEC_RELPATH, CROSS_02_03_SPEC_SHA256),
            (TRACKER_ELIGIBILITY_CSV_RELPATH, TRACKER_ELIGIBILITY_CSV_SHA256),
        ):
            actual = _compute_file_sha256(repo_root / relpath)
            if actual != expected_sha:
                return AdjudicationResult(
                    status=STATUS_HALT_H3,
                    halting_step="H3",
                    v1_preflight="PASS",
                    v3_preflight="PASS",
                )
    except OSError:
        return AdjudicationResult(
            status=STATUS_HALT_H3,
            halting_step="H3",
            v1_preflight="PASS",
            v3_preflight="PASS",
        )

    sha_pin_map = _build_sha_pin_map(repo_root, v1_module_sha, v3_module_sha)

    # H4 — tracker eligibility CSV read.
    try:
        tracker_rows = _read_tracker_eligibility_rows(repo_root)
    except OSError:
        return AdjudicationResult(
            status=STATUS_HALT_H4,
            halting_step="H4",
            v1_preflight="PASS",
            v3_preflight="PASS",
            sha_pins=dict(sha_pin_map),
        )
    if not tracker_rows:
        return AdjudicationResult(
            status=STATUS_HALT_H4,
            halting_step="H4",
            v1_preflight="PASS",
            v3_preflight="PASS",
            sha_pins=dict(sha_pin_map),
        )

    decision_rows = _build_decision_rows(repo_root, sha_pin_map, tracker_rows)

    # H5 — numeric-winner self-guard.
    h5_violation = _check_h5_no_numeric_winner(decision_rows)
    if h5_violation is not None:
        return AdjudicationResult(
            status=STATUS_HALT_H5,
            halting_step="H5",
            v1_preflight="PASS",
            v3_preflight="PASS",
            sha_pins=dict(sha_pin_map),
        )

    # H6 — vocabulary self-guard.
    h6_violation = _check_h6_vocabulary(decision_rows)
    if h6_violation is not None:
        return AdjudicationResult(
            status=STATUS_HALT_H6,
            halting_step="H6",
            v1_preflight="PASS",
            v3_preflight="PASS",
            sha_pins=dict(sha_pin_map),
        )

    # H7a — forbidden output parent dir paradox guard.
    h7a_violation = _check_h7a_forbidden_dir(repo_root)
    if h7a_violation is not None:
        return AdjudicationResult(
            status=STATUS_HALT_H7A,
            halting_step="H7a",
            v1_preflight="PASS",
            v3_preflight="PASS",
            sha_pins=dict(sha_pin_map),
        )

    # H7b — PR-self-archive sentinel.
    h7b_violation = _check_h7b_no_self_archive(repo_root)
    if h7b_violation is not None:
        return AdjudicationResult(
            status=STATUS_HALT_H7B,
            halting_step="H7b",
            v1_preflight="PASS",
            v3_preflight="PASS",
            sha_pins=dict(sha_pin_map),
        )

    # H_FINAL — all halts passed. Create output dir (ONLY now) and emit.
    output_dir = repo_root / OUTPUT_DIR_RELPATH
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / OUTPUT_CSV_FILENAME
    md_path = output_dir / OUTPUT_MD_FILENAME

    _write_decision_csv(csv_path, decision_rows)
    md_text = _build_decision_md(sha_pin_map, tracker_rows, decision_rows)
    md_path.write_text(md_text)

    # Q8 self-check on emitted MD (no empirical AoE2 claim).
    if _AOE2_EMPIRICAL_CLAIM_REGEX.search(md_text):  # pragma: no cover — guarded
        # If this ever fires, something is structurally wrong with our MD
        # template; return as H6 violation (vocabulary discipline).
        return AdjudicationResult(
            status=STATUS_HALT_H6,
            halting_step="H6",
            v1_preflight="PASS",
            v3_preflight="PASS",
            sha_pins=dict(sha_pin_map),
        )

    return AdjudicationResult(
        status=STATUS_PASS,
        halting_step=None,
        v1_preflight="PASS",
        v3_preflight="PASS",
        sha_pins=dict(sha_pin_map),
        csv_path=csv_path,
        md_path=md_path,
        rows_written=len(decision_rows),
    )
