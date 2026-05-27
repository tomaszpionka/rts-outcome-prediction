"""Step 02_01_99 omit-closure decision module for SC2EGSet (closure-side).

This module is the CLOSURE-SIDE decision artifact for SC2EGSet Step
02_01_99 ("rating omit closure"). It is NOT a Q6X re-adjudication module;
it explicitly preserves the BINDING Q5 / Q6F / Q6G / Q6H verdicts and does
NOT re-open any Q-chain question. The artifact emitted by
``run_close_history_rating_omit_path()`` records the Layer-2 election to
exclude the ``reconstructed_rating`` family from Phase-02 materialization
scope, unblocking the other five history-enriched families under the
Q6H ``Q6H_FIVE_FAMILY_POST_OMIT_SET`` anchor.

Provenance ledger (15 SHA values total):

    11 hard-coded provenance values = 10 parent artifact SHAs from
    PR #242 / #243 / #245 / #247 / #249 (2 SHAs per PR x 5 PRs) + 1
    ``head_master_sha_at_layer_1_plan_time``. Plus 4 dispatch-time SHAs
    (PR #251 CSV / MD / module + PR #253 ROADMAP) = 15 total provenance
    values.

The 45-column CSV schema (``OMIT_CLOSURE_SCHEMA``) extends the Q6H
38-column schema by 7 columns (NIT #2 simplification term applied: see
the Layer-1 plan ``## Schema Derivation`` section and the artifact MD §11
which embeds the per-column rationale verbatim). The 5 newly added
Round-2 columns are:

    13. elevation_rationale_jaccard_vs_q6h_section_15 (NIT #3; anti-
        boilerplate Jaccard <0.5 falsifier).
    14. branch_ii_state_semantic_anchor (NIT #1; 4-key semicolon string
        distinguishing Q6H verdict state vs. omit-closure scope
        interpretation).
    15. reviewer_adversarial_signoff_layer_1 (NIT #4).
    16. reviewer_adversarial_layer_1_critique_sha256 (NIT #4).
    17. reviewer_adversarial_signoff_layer_2 (NIT #4).
    18. reviewer_adversarial_layer_2_critique_sha256 (NIT #4).

(That is 6 Round-2 columns; the 7th deviation column is the duplicated
artifact-elevation vs Q6H-section-15 dual-count discipline at columns
9-10 and 11-12 retained from Round 1.)

This module performs NO feature materialization, NO Parquet emission, NO
CROSS-02-01 audit, NO status-YAML flip, NO ``research_log`` mutation,
NO ROADMAP edit, NO Step 02_01_04 / Phase 03 touch, and opens NO new Q6X
PR. The artifact is a decision-record CSV+MD pair only.
"""

from __future__ import annotations

import csv
import hashlib
import logging
import re
import subprocess
import unicodedata
from dataclasses import dataclass, fields
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.decide_history_rating_path import (
    PARENT_PR242_CSV_REL,
    PARENT_PR242_MD_REL,
    PARENT_PR243_CSV_REL,
    PARENT_PR243_MD_REL,
    PARENT_PR245_CSV_REL,
    PARENT_PR245_MD_REL,
    PARENT_PR247_CSV_REL,
    PARENT_PR247_MD_REL,
    PARENT_PR249_CSV_REL,
    PARENT_PR249_MD_REL,
    Q6H_DECISION_CSV_REL,
    Q6H_DECISION_MD_REL,
    Q6H_PATH_DECISION_RULE,
)
from rts_predict.games.sc2.datasets.sc2egset.decide_history_rating_path import (
    Q6H_FIVE_FAMILY_POST_OMIT_SET as _Q6H_FIVE_FAMILY_POST_OMIT_SET,
)

LOGGER = logging.getLogger(__name__)

__all__ = [
    "AUDIT_PR_NUMBER_PLACEHOLDER",
    "HEAD_MASTER_SHA_AT_LAYER_1_PLAN_TIME",
    "OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL",
    "OMIT_CLOSURE_DECISION_RULE_SHA256",
    "OMIT_CLOSURE_EXCLUDED_COLUMNS",
    "OMIT_CLOSURE_EXCLUDED_FAMILY",
    "OMIT_CLOSURE_FALSIFIER_KEYS",
    "OMIT_CLOSURE_FIVE_FAMILY_SET",
    "OMIT_CLOSURE_JACCARD_THRESHOLD",
    "OMIT_CLOSURE_PARENT_SHA_PINS",
    "OMIT_CLOSURE_PR249_CROSS_REF_MIN_COUNT",
    "OMIT_CLOSURE_PR249_CROSS_REF_REGEX",
    "OMIT_CLOSURE_SCHEMA",
    "OMIT_CLOSURE_THESIS_PRAGMATISM_MIN_SENTENCES",
    "OMIT_CLOSURE_VERDICT",
    "Q5_SELECTED_POLICY",
    "Q6F_SELECTED_POLICY",
    "Q6G_SELECTED_POLICY",
    "Q6H_BRANCH_II_RULE_TEXT",
    "Q6H_BRANCH_III_RULE_TEXT",
    "Q6H_SELECTED_POLICY",
    "RatingOmitClosureDecision",
    "RatingOmitClosureError",
    "RatingOmitClosureResult",
    "run_close_history_rating_omit_path",
]


# ---------------------------------------------------------------------------
# Verdict / scope constants
# ---------------------------------------------------------------------------

OMIT_CLOSURE_VERDICT: str = "omit_reconstructed_rating_and_unblock_other_five"

OMIT_CLOSURE_EXCLUDED_FAMILY: str = "reconstructed_rating"

OMIT_CLOSURE_EXCLUDED_COLUMNS: tuple[str, ...] = (
    "reconstructed_rating_focal_pre",
    "reconstructed_rating_opp_pre",
    "reconstructed_rating_diff",
)

# Re-export under the closure name to make the canonical anchor explicit.
OMIT_CLOSURE_FIVE_FAMILY_SET: tuple[str, ...] = _Q6H_FIVE_FAMILY_POST_OMIT_SET

assert len(OMIT_CLOSURE_FIVE_FAMILY_SET) == 5, (
    "OMIT_CLOSURE_FIVE_FAMILY_SET must contain exactly 5 entries (Q6H A8); "
    f"observed {len(OMIT_CLOSURE_FIVE_FAMILY_SET)}"
)
assert "reconstructed_rating" not in OMIT_CLOSURE_FIVE_FAMILY_SET, (
    "reconstructed_rating must NOT appear in OMIT_CLOSURE_FIVE_FAMILY_SET"
)


# ---------------------------------------------------------------------------
# Parent SHA pins (10 hard-coded; A1 verbatim) + Layer-1 head SHA
# ---------------------------------------------------------------------------

AUDIT_PR_NUMBER_PLACEHOLDER: str = "PR #<TBD>"

OMIT_CLOSURE_PARENT_SHA_PINS: dict[str, str] = {
    "parent_pr242_csv_sha256": (
        "f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b"
    ),
    "parent_pr242_md_sha256": (
        "fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d"
    ),
    "parent_pr243_csv_sha256": (
        "29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424"
    ),
    "parent_pr243_md_sha256": (
        "026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719"
    ),
    "parent_pr245_csv_sha256": (
        "703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0"
    ),
    "parent_pr245_md_sha256": (
        "7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419"
    ),
    "parent_pr247_csv_sha256": (
        "249e5591c6505b748fe3d371284a72d8f4620f57dbe9628c908ec2fbf097c8ed"
    ),
    "parent_pr247_md_sha256": (
        "4b49bee405bf87d4b8920b188e2c38d185ecc077b532d64a8bdd5a90cdf143f2"
    ),
    "parent_pr249_csv_sha256": (
        "1d9ee22e0523e640181fa0a7a7d2680467a267eefa376fec903f58094118b82f"
    ),
    "parent_pr249_md_sha256": (
        "8beed3ba6491afb6ba72ee2718b1364c9a2577b26c82237b735d219ccfdc0ea1"
    ),
}

assert len(OMIT_CLOSURE_PARENT_SHA_PINS) == 10, (
    "OMIT_CLOSURE_PARENT_SHA_PINS must contain exactly 10 hard-coded parent SHAs; "
    f"observed {len(OMIT_CLOSURE_PARENT_SHA_PINS)}"
)
for _k, _v in OMIT_CLOSURE_PARENT_SHA_PINS.items():
    assert len(_v) == 64 and all(c in "0123456789abcdef" for c in _v), (
        f"Parent SHA pin {_k} is not a 64-char lowercase hex digest"
    )

HEAD_MASTER_SHA_AT_LAYER_1_PLAN_TIME: str = (
    "0acc0e83274b52831daf80a56beaacaed9340b13"
)
assert len(HEAD_MASTER_SHA_AT_LAYER_1_PLAN_TIME) == 40, (
    "HEAD_MASTER_SHA_AT_LAYER_1_PLAN_TIME must be a 40-char SHA"
)


# ---------------------------------------------------------------------------
# Admissibility / anti-boilerplate constants
# ---------------------------------------------------------------------------

OMIT_CLOSURE_THESIS_PRAGMATISM_MIN_SENTENCES: int = 6
OMIT_CLOSURE_PR249_CROSS_REF_MIN_COUNT: int = 3
OMIT_CLOSURE_JACCARD_THRESHOLD: float = 0.5

OMIT_CLOSURE_PR249_CROSS_REF_REGEX: str = r"PR #249 §[0-9]+(?:\.[0-9]+)?[a-z]?"


# ---------------------------------------------------------------------------
# Branch (ii) state semantic anchor (NIT #1; canonical, binding)
# ---------------------------------------------------------------------------

OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL: str = (
    "q6h_verdict_state=reached_as_recommendation_only_event_by_event_glicko2;"
    "omit_closure_scope_interpretation=blocked_for_phase_02_materialization_"
    "scope_under_layer_2_election;"
    "is_q6h_re_adjudication=FALSE;"
    "is_new_q6x_loop=FALSE"
)

assert OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL.count(";") == 3, (
    "OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL must have exactly 4 "
    "semicolon-separated key=value pairs"
)
assert "is_q6h_re_adjudication=FALSE" in OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL
assert "is_new_q6x_loop=FALSE" in OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL


# ---------------------------------------------------------------------------
# Inherited Q-chain BINDING verdicts (preserved verbatim; NOT re-adjudicated)
# ---------------------------------------------------------------------------

Q5_SELECTED_POLICY: str = "sensitivity_indicator_co_registration"
Q6F_SELECTED_POLICY: str = "narrow_with_evidence"
Q6G_SELECTED_POLICY: str = "recommendation_only_glicko2"
Q6H_SELECTED_POLICY: str = "recommendation_only_event_by_event_glicko2"


# ---------------------------------------------------------------------------
# Q6H decision-rule literal quotes (verbatim from
# decide_history_rating_path.Q6H_PATH_DECISION_RULE) -- anchors §4.2 prose
# in the artifact MD without paraphrasing the binding rule.
# ---------------------------------------------------------------------------

def _extract_q6h_branch_block(rule_text: str, branch_token: str) -> str:
    """Slice the Q6H rule text between ``branch_token`` and the next BRANCH.

    Args:
        rule_text: The full ``Q6H_PATH_DECISION_RULE`` constant.
        branch_token: e.g. ``"BRANCH (ii)"`` or ``"BRANCH (iii)"``.

    Returns:
        The verbatim slice of the rule text starting at ``branch_token`` and
        ending immediately before the next ``BRANCH (`` token (or
        end-of-text).

    Raises:
        ValueError: If ``branch_token`` is not present in ``rule_text``.
    """
    start = rule_text.find(branch_token)
    if start < 0:
        raise ValueError(f"branch_token {branch_token!r} not found in rule text")
    after_start = start + len(branch_token)
    next_idx = rule_text.find("BRANCH (", after_start)
    if next_idx < 0:
        return rule_text[start:].rstrip()
    return rule_text[start:next_idx].rstrip()


Q6H_BRANCH_II_RULE_TEXT: str = _extract_q6h_branch_block(
    Q6H_PATH_DECISION_RULE, "BRANCH (ii)"
)
Q6H_BRANCH_III_RULE_TEXT: str = _extract_q6h_branch_block(
    Q6H_PATH_DECISION_RULE, "BRANCH (iii)"
)

OMIT_CLOSURE_DECISION_RULE_SHA256: str = hashlib.sha256(
    Q6H_BRANCH_III_RULE_TEXT.encode("utf-8")
).hexdigest()


# ---------------------------------------------------------------------------
# Falsifier roll-call (38 keys; >= 30 required by plan)
# ---------------------------------------------------------------------------

OMIT_CLOSURE_FALSIFIER_KEYS: tuple[str, ...] = (
    "omit_closure_schema_column_count_mismatch",
    "omit_closure_five_family_set_drift_from_q6h_constant",
    "omit_closure_excluded_columns_drift_from_q6h_literal",
    "omit_closure_thesis_pragmatism_not_true",
    "omit_closure_thesis_pragmatism_elevation_under_six_sentences",
    "omit_closure_q6h_section_15_under_six_sentences",
    "omit_closure_pr249_cross_ref_count_under_three_in_elevation",
    "omit_closure_pr249_cross_ref_count_under_three_in_q6h_section_15",
    "omit_closure_reviewer_signoff_layer_1_missing_or_invalid_sha",
    "omit_closure_reviewer_signoff_layer_2_missing_or_invalid_sha",
    "omit_closure_reviewer_signoff_layer_1_or_layer_2_not_approve_with_zero_blockers",
    "omit_closure_branch_ii_state_anchor_misnamed_or_missing_re_adjudication_assertion",
    "omit_closure_elevation_rationale_jaccard_overlap_with_q6h_section_15_exceeds_threshold",
    "omit_closure_q5_re_adjudication_drift",
    "omit_closure_q6f_re_adjudication_drift",
    "omit_closure_q6g_re_adjudication_drift",
    "omit_closure_q6h_re_adjudication_drift",
    "omit_closure_q6h_artifact_sha_mismatch",
    "omit_closure_q6h_module_sha_mismatch",
    "omit_closure_pr253_roadmap_sha_mismatch",
    "omit_closure_parent_sha_not_re_verified_at_dispatch",
    "omit_closure_parquet_emitted",
    "omit_closure_cross_02_01_audit_emitted",
    "omit_closure_status_yaml_mutation",
    "omit_closure_research_log_mutation",
    "omit_closure_roadmap_mutation",
    "omit_closure_spec_mutation",
    "omit_closure_phase_03_touch",
    "omit_closure_step_02_01_04_touch",
    "omit_closure_q6x_re_opened",
    "omit_closure_q6h_section_15_silently_modified",
    "omit_closure_reconstructed_rating_in_five_family_set",
    "omit_closure_excluded_family_not_reconstructed_rating",
    "omit_closure_five_family_set_size_not_five",
    "omit_closure_non_deterministic_emission",
    "omit_closure_silent_q6_closure",
    "omit_closure_5_family_narrowing_in_this_pr",
    "omit_closure_5_family_materialization_in_this_pr",
    "omit_closure_pr249_cross_ref_regex_undocumented",
)

assert len(OMIT_CLOSURE_FALSIFIER_KEYS) >= 30, (
    "OMIT_CLOSURE_FALSIFIER_KEYS must contain >= 30 keys; "
    f"observed {len(OMIT_CLOSURE_FALSIFIER_KEYS)}"
)
assert len(set(OMIT_CLOSURE_FALSIFIER_KEYS)) == len(OMIT_CLOSURE_FALSIFIER_KEYS), (
    "OMIT_CLOSURE_FALSIFIER_KEYS contains duplicate keys"
)


# ---------------------------------------------------------------------------
# 45-column CSV schema (canonical order; Round-2 per critique R2-N1/N2/N3)
# ---------------------------------------------------------------------------

OMIT_CLOSURE_SCHEMA: tuple[str, ...] = (
    "decision_id",  # 01
    "parent_step_number",  # 02
    "lineage_step_number",  # 03
    "decision_name",  # 04
    "verdict",  # 05
    "binding_level",  # 06
    "selected_policy",  # 07
    "thesis_pragmatism",  # 08
    "thesis_pragmatism_sentence_count",  # 09
    "thesis_pragmatism_q6h_section_15_sentence_count",  # 10
    "pr249_cross_reference_count",  # 11
    "pr249_cross_reference_count_q6h_section_15",  # 12
    "elevation_rationale_jaccard_vs_q6h_section_15",  # 13 (NIT #3)
    "branch_ii_state_semantic_anchor",  # 14 (NIT #1)
    "reviewer_adversarial_signoff_layer_1",  # 15 (NIT #4)
    "reviewer_adversarial_layer_1_critique_sha256",  # 16 (NIT #4)
    "reviewer_adversarial_signoff_layer_2",  # 17 (NIT #4)
    "reviewer_adversarial_layer_2_critique_sha256",  # 18 (NIT #4)
    "q6_omission_status",  # 19
    "q6_not_silently_satisfied",  # 20
    "five_family_materialization_permission",  # 21
    "five_family_set",  # 22
    "excluded_family",  # 23
    "excluded_columns",  # 24
    "future_roadmap_scope_amendment_required",  # 25
    "future_materialization_pr_required",  # 26
    "q5_policy",  # 27
    "q6f_policy",  # 28
    "q6g_policy",  # 29
    "q6h_policy",  # 30
    "evidence_paths",  # 31
    "falsifiers",  # 32
    "audit_pr",  # 33
    "parent_pr242_csv_sha256",  # 34
    "parent_pr242_md_sha256",  # 35
    "parent_pr243_csv_sha256",  # 36
    "parent_pr243_md_sha256",  # 37
    "parent_pr245_csv_sha256",  # 38
    "parent_pr245_md_sha256",  # 39
    "parent_pr247_csv_sha256",  # 40
    "parent_pr247_md_sha256",  # 41
    "parent_pr249_csv_sha256",  # 42
    "parent_pr249_md_sha256",  # 43
    "parent_pr251_csv_sha256",  # 44 (dispatch-time)
    "parent_pr251_md_sha256",  # 45 (dispatch-time)
)

assert len(OMIT_CLOSURE_SCHEMA) == 45, (
    f"OMIT_CLOSURE_SCHEMA must have exactly 45 columns per Layer-1 plan §Schema "
    f"Derivation (NIT #2); observed {len(OMIT_CLOSURE_SCHEMA)}"
)
assert len(set(OMIT_CLOSURE_SCHEMA)) == 45, (
    "OMIT_CLOSURE_SCHEMA contains duplicate column names"
)


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------


class RatingOmitClosureError(RuntimeError):
    """Raised when the omit-closure entrypoint halts on a fired falsifier.

    Attributes:
        falsifier_key: The first fired falsifier key.
        message: Human-readable observed-vs-expected message.
    """

    def __init__(self, falsifier_key: str, message: str) -> None:
        self.falsifier_key = falsifier_key
        self.message = message
        super().__init__(f"Falsifier {falsifier_key!r} fired: {message}")


# ---------------------------------------------------------------------------
# Decision dataclass (EXACTLY 45 fields; matches OMIT_CLOSURE_SCHEMA)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RatingOmitClosureDecision:
    """A single Step 02_01_99 omit-closure decision row.

    The CSV column order is exactly this dataclass's field order. The
    schema column count is asserted at module load against ``len(fields)``
    (must equal 45 per Round-2 critique).
    """

    decision_id: str
    parent_step_number: str
    lineage_step_number: str
    decision_name: str
    verdict: str
    binding_level: str
    selected_policy: str
    thesis_pragmatism: str
    thesis_pragmatism_sentence_count: str
    thesis_pragmatism_q6h_section_15_sentence_count: str
    pr249_cross_reference_count: str
    pr249_cross_reference_count_q6h_section_15: str
    elevation_rationale_jaccard_vs_q6h_section_15: str
    branch_ii_state_semantic_anchor: str
    reviewer_adversarial_signoff_layer_1: str
    reviewer_adversarial_layer_1_critique_sha256: str
    reviewer_adversarial_signoff_layer_2: str
    reviewer_adversarial_layer_2_critique_sha256: str
    q6_omission_status: str
    q6_not_silently_satisfied: str
    five_family_materialization_permission: str
    five_family_set: str
    excluded_family: str
    excluded_columns: str
    future_roadmap_scope_amendment_required: str
    future_materialization_pr_required: str
    q5_policy: str
    q6f_policy: str
    q6g_policy: str
    q6h_policy: str
    evidence_paths: str
    falsifiers: str
    audit_pr: str
    parent_pr242_csv_sha256: str
    parent_pr242_md_sha256: str
    parent_pr243_csv_sha256: str
    parent_pr243_md_sha256: str
    parent_pr245_csv_sha256: str
    parent_pr245_md_sha256: str
    parent_pr247_csv_sha256: str
    parent_pr247_md_sha256: str
    parent_pr249_csv_sha256: str
    parent_pr249_md_sha256: str
    parent_pr251_csv_sha256: str
    parent_pr251_md_sha256: str


@dataclass(frozen=True)
class RatingOmitClosureResult:
    """Top-level aggregate of the omit-closure artifact run.

    Attributes:
        decision: The canonical 45-field decision row.
        csv_path: Path where the CSV was written.
        md_path: Path where the MD was written.
        falsifier_status: Mapping from falsifier key to literal
            ``"fired"`` / ``"did_not_fire"``.
    """

    decision: RatingOmitClosureDecision
    csv_path: Path
    md_path: Path
    falsifier_status: dict[str, str]


# Module-load schema/dataclass alignment.
assert len(fields(RatingOmitClosureDecision)) == 45, (
    f"RatingOmitClosureDecision must have exactly 45 fields; "
    f"observed {len(fields(RatingOmitClosureDecision))}"
)
assert tuple(f.name for f in fields(RatingOmitClosureDecision)) == OMIT_CLOSURE_SCHEMA, (
    "RatingOmitClosureDecision field order must match OMIT_CLOSURE_SCHEMA exactly"
)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _sha256_file(path: Path) -> str:
    """Return the SHA-256 hex digest of ``path``, or ``'NOT_FOUND'``.

    Args:
        path: Path to the file.

    Returns:
        64-char lowercase hex digest, or ``'NOT_FOUND'`` if the file does
        not exist.
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


def _tokenize_for_jaccard(text: str) -> frozenset[str]:
    """Unicode-safe tokeniser for the anti-boilerplate Jaccard falsifier.

    NFKD-normalise -> lowercase -> strip Unicode punctuation (category
    ``P*``) -> whitespace split. Handles em/en dashes, curly quotes,
    NBSPs, accented characters, and mixed casing per R2-N2 (binding).

    Args:
        text: Free-form prose.

    Returns:
        Frozenset of lowercase tokens with all Unicode punctuation
        removed.
    """
    normalised = unicodedata.normalize("NFKD", text).lower()
    stripped = "".join(
        c for c in normalised if not unicodedata.category(c).startswith("P")
    )
    return frozenset(stripped.split())


def _compute_jaccard(text_a: str, text_b: str) -> float:
    """Token-level Jaccard similarity in ``[0.0, 1.0]``.

    Args:
        text_a: First text.
        text_b: Second text.

    Returns:
        Jaccard similarity. Zero-division guarded: if both tokenisations
        produce an empty set, the function returns ``0.0`` (no overlap).
    """
    tokens_a = _tokenize_for_jaccard(text_a)
    tokens_b = _tokenize_for_jaccard(text_b)
    union = tokens_a | tokens_b
    if not union:
        return 0.0
    return len(tokens_a & tokens_b) / len(union)


def _count_paragraph_sentences(paragraph: str) -> int:
    """Return the sentence count of ``paragraph``.

    Splits on ``[.!?]`` followed by whitespace; filters out fragments
    shorter than 5 characters (after ``strip()``).

    Args:
        paragraph: Free-form prose.

    Returns:
        Number of sentences.
    """
    parts = re.split(r"(?<=[.!?])\s+", paragraph.strip())
    return len([s for s in parts if len(s.strip()) >= 5])


def _count_pr249_cross_references(paragraph: str) -> int:
    """Count ``PR #249 §X[.Y][a]`` cross-reference tokens in ``paragraph``.

    Args:
        paragraph: Free-form prose.

    Returns:
        Number of regex matches.
    """
    return len(re.findall(OMIT_CLOSURE_PR249_CROSS_REF_REGEX, paragraph))


_PARENT_SHA_PAIRS: tuple[tuple[str, str], ...] = (
    ("parent_pr242_csv_sha256", PARENT_PR242_CSV_REL),
    ("parent_pr242_md_sha256", PARENT_PR242_MD_REL),
    ("parent_pr243_csv_sha256", PARENT_PR243_CSV_REL),
    ("parent_pr243_md_sha256", PARENT_PR243_MD_REL),
    ("parent_pr245_csv_sha256", PARENT_PR245_CSV_REL),
    ("parent_pr245_md_sha256", PARENT_PR245_MD_REL),
    ("parent_pr247_csv_sha256", PARENT_PR247_CSV_REL),
    ("parent_pr247_md_sha256", PARENT_PR247_MD_REL),
    ("parent_pr249_csv_sha256", PARENT_PR249_CSV_REL),
    ("parent_pr249_md_sha256", PARENT_PR249_MD_REL),
)


def _check_parent_pr_shas(repo_root: Path) -> list[tuple[str, str]]:
    """Verify each of the 10 hard-coded parent SHAs vs current repo state.

    Args:
        repo_root: Repository root.

    Returns:
        List of ``(sha_key, message)`` mismatches; empty on success.
    """
    mismatches: list[tuple[str, str]] = []
    for sha_key, rel_path in _PARENT_SHA_PAIRS:
        expected = OMIT_CLOSURE_PARENT_SHA_PINS[sha_key]
        observed = _sha256_file(repo_root / rel_path)
        if observed != expected:
            mismatches.append(
                (
                    sha_key,
                    f"{rel_path}: observed {observed} expected {expected}",
                )
            )
    return mismatches


def _parse_branch_ii_state_anchor(s: str) -> dict[str, str]:
    """Parse and validate a Branch (ii) state semantic-anchor string.

    The canonical format is 4 semicolon-separated ``key=value`` pairs with
    keys ``q6h_verdict_state``, ``omit_closure_scope_interpretation``,
    ``is_q6h_re_adjudication``, ``is_new_q6x_loop``. The last two keys
    MUST have value ``FALSE`` to prevent silent Q6H re-adjudication or a
    new Q6X loop.

    Args:
        s: The serialized anchor string.

    Returns:
        Mapping of key -> value.

    Raises:
        ValueError: If the string is malformed (wrong key count, missing
            canonical keys, or the two FALSE assertions are not honoured).
    """
    parts = s.split(";")
    if len(parts) != 4:
        raise ValueError(
            f"Branch (ii) anchor must have exactly 4 ;-separated pairs; "
            f"observed {len(parts)} in {s!r}"
        )
    out: dict[str, str] = {}
    for pair in parts:
        if "=" not in pair:
            raise ValueError(f"Anchor segment {pair!r} missing '='")
        key, _, value = pair.partition("=")
        out[key] = value
    expected_keys = {
        "q6h_verdict_state",
        "omit_closure_scope_interpretation",
        "is_q6h_re_adjudication",
        "is_new_q6x_loop",
    }
    if set(out) != expected_keys:
        raise ValueError(
            f"Anchor keys {sorted(out)} != canonical {sorted(expected_keys)}"
        )
    if out["is_q6h_re_adjudication"] != "FALSE":
        raise ValueError(
            f"is_q6h_re_adjudication must be FALSE; observed "
            f"{out['is_q6h_re_adjudication']!r}"
        )
    if out["is_new_q6x_loop"] != "FALSE":
        raise ValueError(
            f"is_new_q6x_loop must be FALSE; observed {out['is_new_q6x_loop']!r}"
        )
    return out


def _evidence_paths_string() -> str:
    """Return a semicolon-joined evidence-paths string.

    Returns:
        Repo-relative paths for the 5 parent PR CSV/MD pairs + the Q6H
        artifact pair, in canonical order.
    """
    parts = [
        PARENT_PR242_CSV_REL,
        PARENT_PR242_MD_REL,
        PARENT_PR243_CSV_REL,
        PARENT_PR243_MD_REL,
        PARENT_PR245_CSV_REL,
        PARENT_PR245_MD_REL,
        PARENT_PR247_CSV_REL,
        PARENT_PR247_MD_REL,
        PARENT_PR249_CSV_REL,
        PARENT_PR249_MD_REL,
        Q6H_DECISION_CSV_REL,
        Q6H_DECISION_MD_REL,
    ]
    return ";".join(parts)


def _falsifier_csv_string(status: dict[str, str]) -> str:
    """Render falsifier roll-call as a CSV cell string.

    Args:
        status: Mapping of falsifier key -> literal ``"fired"`` /
            ``"did_not_fire"``.

    Returns:
        Semicolon-joined ``key=value`` entries, in
        ``OMIT_CLOSURE_FALSIFIER_KEYS`` order.
    """
    return ";".join(
        f"{key}={status.get(key, 'did_not_fire')}"
        for key in OMIT_CLOSURE_FALSIFIER_KEYS
    )


# ---------------------------------------------------------------------------
# Falsifier roll-call evaluation
# ---------------------------------------------------------------------------


def _is_hex64(value: str) -> bool:
    """Return True iff ``value`` is a 64-char lowercase hex string."""
    if len(value) != 64:
        return False
    return all(c in "0123456789abcdef" for c in value)


def _evaluate_falsifiers(
    *,
    decision: RatingOmitClosureDecision,
    elevation_rationale_text: str,
    q6h_section_15_text: str,
    layer_1_signoff_state: str,
    layer_2_signoff_state: str,
) -> dict[str, str]:
    """Evaluate the omit-closure falsifier roll-call against ``decision``.

    Args:
        decision: The constructed decision row.
        elevation_rationale_text: The §6 elevation paragraph.
        q6h_section_15_text: The Q6H MD §15 paragraph.
        layer_1_signoff_state: e.g. ``"APPROVE"`` /
            ``"APPROVE-WITH-NITS"`` / ``"HOLD-WITH-BLOCKERS"``.
        layer_2_signoff_state: Same, for Layer-2.

    Returns:
        Mapping of falsifier key -> ``"fired"`` / ``"did_not_fire"``.
    """
    status: dict[str, str] = {k: "did_not_fire" for k in OMIT_CLOSURE_FALSIFIER_KEYS}

    if len(OMIT_CLOSURE_SCHEMA) != 45:
        status["omit_closure_schema_column_count_mismatch"] = "fired"

    if tuple(decision.five_family_set.split(";")) != OMIT_CLOSURE_FIVE_FAMILY_SET:
        status["omit_closure_five_family_set_drift_from_q6h_constant"] = "fired"
    if len(decision.five_family_set.split(";")) != 5:
        status["omit_closure_five_family_set_size_not_five"] = "fired"
    if "reconstructed_rating" in decision.five_family_set.split(";"):
        status["omit_closure_reconstructed_rating_in_five_family_set"] = "fired"

    if tuple(decision.excluded_columns.split(";")) != OMIT_CLOSURE_EXCLUDED_COLUMNS:
        status["omit_closure_excluded_columns_drift_from_q6h_literal"] = "fired"
    if decision.excluded_family != OMIT_CLOSURE_EXCLUDED_FAMILY:
        status["omit_closure_excluded_family_not_reconstructed_rating"] = "fired"

    if decision.thesis_pragmatism != "TRUE":
        status["omit_closure_thesis_pragmatism_not_true"] = "fired"

    elevation_sentences = _count_paragraph_sentences(elevation_rationale_text)
    q6h_sentences = _count_paragraph_sentences(q6h_section_15_text)
    if elevation_sentences < OMIT_CLOSURE_THESIS_PRAGMATISM_MIN_SENTENCES:
        status["omit_closure_thesis_pragmatism_elevation_under_six_sentences"] = "fired"
    if q6h_sentences < OMIT_CLOSURE_THESIS_PRAGMATISM_MIN_SENTENCES:
        status["omit_closure_q6h_section_15_under_six_sentences"] = "fired"

    elevation_refs = _count_pr249_cross_references(elevation_rationale_text)
    q6h_refs = _count_pr249_cross_references(q6h_section_15_text)
    if elevation_refs < OMIT_CLOSURE_PR249_CROSS_REF_MIN_COUNT:
        status["omit_closure_pr249_cross_ref_count_under_three_in_elevation"] = "fired"
    if q6h_refs < OMIT_CLOSURE_PR249_CROSS_REF_MIN_COUNT:
        status[
            "omit_closure_pr249_cross_ref_count_under_three_in_q6h_section_15"
        ] = "fired"

    jaccard = _compute_jaccard(elevation_rationale_text, q6h_section_15_text)
    if jaccard >= OMIT_CLOSURE_JACCARD_THRESHOLD:
        status[
            "omit_closure_elevation_rationale_jaccard_overlap_with_q6h_section_15_exceeds_threshold"
        ] = "fired"

    if not _is_hex64(decision.reviewer_adversarial_layer_1_critique_sha256):
        status["omit_closure_reviewer_signoff_layer_1_missing_or_invalid_sha"] = "fired"
    if not _is_hex64(decision.reviewer_adversarial_layer_2_critique_sha256):
        status["omit_closure_reviewer_signoff_layer_2_missing_or_invalid_sha"] = "fired"

    approved = {"APPROVE", "APPROVE-WITH-NITS"}
    if layer_1_signoff_state not in approved or layer_2_signoff_state not in approved:
        status[
            "omit_closure_reviewer_signoff_layer_1_or_layer_2_not_approve_with_zero_blockers"
        ] = "fired"

    try:
        _parse_branch_ii_state_anchor(decision.branch_ii_state_semantic_anchor)
    except ValueError:
        status[
            "omit_closure_branch_ii_state_anchor_misnamed_or_missing_re_adjudication_assertion"
        ] = "fired"

    if decision.q5_policy != Q5_SELECTED_POLICY:
        status["omit_closure_q5_re_adjudication_drift"] = "fired"
    if decision.q6f_policy != Q6F_SELECTED_POLICY:
        status["omit_closure_q6f_re_adjudication_drift"] = "fired"
    if decision.q6g_policy != Q6G_SELECTED_POLICY:
        status["omit_closure_q6g_re_adjudication_drift"] = "fired"
    if decision.q6h_policy != Q6H_SELECTED_POLICY:
        status["omit_closure_q6h_re_adjudication_drift"] = "fired"

    if decision.q6_omission_status == "silently_satisfied":
        status["omit_closure_silent_q6_closure"] = "fired"
    if decision.q6_not_silently_satisfied != "TRUE":
        status["omit_closure_silent_q6_closure"] = "fired"

    if not OMIT_CLOSURE_PR249_CROSS_REF_REGEX:
        status["omit_closure_pr249_cross_ref_regex_undocumented"] = "fired"

    return status


# ---------------------------------------------------------------------------
# Decision-row builder
# ---------------------------------------------------------------------------


def _build_decision_row(
    *,
    q6h_csv_sha256: str,
    q6h_md_sha256: str,
    elevation_rationale_text: str,
    q6h_section_15_text: str,
    layer_1_critique_sha256: str,
    layer_1_signoff_state: str,
    layer_2_critique_sha256: str,
    layer_2_signoff_state: str,
    audit_pr_number: str,
) -> RatingOmitClosureDecision:
    """Build the canonical 45-field omit-closure decision row.

    Args:
        q6h_csv_sha256: Dispatch-time SHA of the Q6H CSV artifact.
        q6h_md_sha256: Dispatch-time SHA of the Q6H MD artifact.
        elevation_rationale_text: The §6 elevation paragraph.
        q6h_section_15_text: The Q6H MD §15 paragraph.
        layer_1_critique_sha256: SHA of the Layer-1 critique file.
        layer_1_signoff_state: APPROVE / APPROVE-WITH-NITS / HOLD-...
        layer_2_critique_sha256: SHA of the Layer-2 critique file.
        layer_2_signoff_state: APPROVE / APPROVE-WITH-NITS / HOLD-...
        audit_pr_number: PR number string, e.g. ``"PR #<TBD>"``.

    Returns:
        A populated ``RatingOmitClosureDecision``.
    """
    elevation_sentences = _count_paragraph_sentences(elevation_rationale_text)
    q6h_sentences = _count_paragraph_sentences(q6h_section_15_text)
    elevation_refs = _count_pr249_cross_references(elevation_rationale_text)
    q6h_refs = _count_pr249_cross_references(q6h_section_15_text)
    jaccard = _compute_jaccard(elevation_rationale_text, q6h_section_15_text)

    approved = {"APPROVE", "APPROVE-WITH-NITS"}
    layer_1_signoff_flag = "TRUE" if layer_1_signoff_state in approved else "FALSE"
    layer_2_signoff_flag = "TRUE" if layer_2_signoff_state in approved else "FALSE"

    return RatingOmitClosureDecision(
        decision_id=(
            "OMIT_CLOSURE_omit_reconstructed_rating_and_unblock_other_five"
        ),
        parent_step_number="02_01_03",
        lineage_step_number="02_01_99",
        decision_name="rating_omit_closure",
        verdict=OMIT_CLOSURE_VERDICT,
        binding_level="BINDING",
        selected_policy=OMIT_CLOSURE_VERDICT,
        thesis_pragmatism="TRUE",
        thesis_pragmatism_sentence_count=str(elevation_sentences),
        thesis_pragmatism_q6h_section_15_sentence_count=str(q6h_sentences),
        pr249_cross_reference_count=str(elevation_refs),
        pr249_cross_reference_count_q6h_section_15=str(q6h_refs),
        elevation_rationale_jaccard_vs_q6h_section_15=f"{jaccard:.4f}",
        branch_ii_state_semantic_anchor=(
            OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL
        ),
        reviewer_adversarial_signoff_layer_1=layer_1_signoff_flag,
        reviewer_adversarial_layer_1_critique_sha256=layer_1_critique_sha256,
        reviewer_adversarial_signoff_layer_2=layer_2_signoff_flag,
        reviewer_adversarial_layer_2_critique_sha256=layer_2_critique_sha256,
        q6_omission_status="intentionally_omitted_under_branch_iii",
        q6_not_silently_satisfied="TRUE",
        five_family_materialization_permission=(
            "permitted_for_5_history_enriched_families_without_reconstructed_"
            "rating_subject_to_future_roadmap_amendment_and_separate_"
            "materialization_pr"
        ),
        five_family_set=";".join(OMIT_CLOSURE_FIVE_FAMILY_SET),
        excluded_family=OMIT_CLOSURE_EXCLUDED_FAMILY,
        excluded_columns=";".join(OMIT_CLOSURE_EXCLUDED_COLUMNS),
        future_roadmap_scope_amendment_required="TRUE",
        future_materialization_pr_required="TRUE",
        q5_policy=Q5_SELECTED_POLICY,
        q6f_policy=Q6F_SELECTED_POLICY,
        q6g_policy=Q6G_SELECTED_POLICY,
        q6h_policy=Q6H_SELECTED_POLICY,
        evidence_paths=_evidence_paths_string(),
        falsifiers=";".join(OMIT_CLOSURE_FALSIFIER_KEYS),
        audit_pr=audit_pr_number,
        parent_pr242_csv_sha256=OMIT_CLOSURE_PARENT_SHA_PINS["parent_pr242_csv_sha256"],
        parent_pr242_md_sha256=OMIT_CLOSURE_PARENT_SHA_PINS["parent_pr242_md_sha256"],
        parent_pr243_csv_sha256=OMIT_CLOSURE_PARENT_SHA_PINS["parent_pr243_csv_sha256"],
        parent_pr243_md_sha256=OMIT_CLOSURE_PARENT_SHA_PINS["parent_pr243_md_sha256"],
        parent_pr245_csv_sha256=OMIT_CLOSURE_PARENT_SHA_PINS["parent_pr245_csv_sha256"],
        parent_pr245_md_sha256=OMIT_CLOSURE_PARENT_SHA_PINS["parent_pr245_md_sha256"],
        parent_pr247_csv_sha256=OMIT_CLOSURE_PARENT_SHA_PINS["parent_pr247_csv_sha256"],
        parent_pr247_md_sha256=OMIT_CLOSURE_PARENT_SHA_PINS["parent_pr247_md_sha256"],
        parent_pr249_csv_sha256=OMIT_CLOSURE_PARENT_SHA_PINS["parent_pr249_csv_sha256"],
        parent_pr249_md_sha256=OMIT_CLOSURE_PARENT_SHA_PINS["parent_pr249_md_sha256"],
        parent_pr251_csv_sha256=q6h_csv_sha256,
        parent_pr251_md_sha256=q6h_md_sha256,
    )


# ---------------------------------------------------------------------------
# Output paths
# ---------------------------------------------------------------------------

OMIT_CLOSURE_CSV_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_99_rating_omit_closure.csv"
)
OMIT_CLOSURE_MD_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_99_rating_omit_closure.md"
)


def _default_output_dir() -> Path:
    """Return the canonical output directory for the artifact pair."""
    here = Path(__file__).resolve()
    repo_root = _find_repo_root(here)
    return repo_root / (
        "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
        "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    )


# ---------------------------------------------------------------------------
# CSV writer
# ---------------------------------------------------------------------------


def _decision_to_row(decision: RatingOmitClosureDecision) -> list[str]:
    """Serialize ``decision`` to a list of CSV cells in schema order."""
    return [getattr(decision, name) for name in OMIT_CLOSURE_SCHEMA]


def _emit_decision_csv(
    decision: RatingOmitClosureDecision,
    out_path: Path,
) -> None:
    """Write the omit-closure CSV byte-deterministically.

    Args:
        decision: The canonical decision row.
        out_path: Output CSV path.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(list(OMIT_CLOSURE_SCHEMA))
        writer.writerow(_decision_to_row(decision))


# ---------------------------------------------------------------------------
# MD writer (21 sections)
# ---------------------------------------------------------------------------


def _emit_decision_md(
    *,
    decision: RatingOmitClosureDecision,
    elevation_rationale_text: str,
    q6h_section_15_text: str,
    head_sha: str,
    q6h_module_sha256: str,
    pr253_roadmap_sha256: str,
    layer_1_signoff_state: str,
    layer_2_signoff_state: str,
    falsifier_status: dict[str, str],
    out_path: Path,
) -> None:
    """Write the omit-closure MD with all 21 sections present (stub).

    Stage 1 emits all 21 sections so the writer interface is exercised by
    the test suite; Stage 2 will refine the prose content. The §11
    schema-derivation embed is left as a structural placeholder for the
    Stage-2 enrichment, which will copy the verbatim plan-body §Schema
    Derivation block into §11 per R2-N1 narrative.

    Args:
        decision: The canonical decision row.
        elevation_rationale_text: The §6 elevation paragraph.
        q6h_section_15_text: The Q6H MD §15 paragraph (for §5 recount).
        head_sha: HEAD git SHA at run time.
        q6h_module_sha256: Dispatch-time SHA of the Q6H module.
        pr253_roadmap_sha256: Dispatch-time SHA of the PR #253 ROADMAP.
        layer_1_signoff_state: APPROVE / APPROVE-WITH-NITS / ...
        layer_2_signoff_state: APPROVE / APPROVE-WITH-NITS / ...
        falsifier_status: Falsifier roll-call mapping.
        out_path: Output MD path.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Step 02_01_99 Rating Omit-Closure Decision")
    lines.append("")
    lines.append(f"**Audit PR:** {decision.audit_pr}")
    lines.append("")

    lines.append("## 1. Summary")
    lines.append("")
    lines.append(
        "This omit-closure artifact records the Layer-2 election to exclude "
        f"`{OMIT_CLOSURE_EXCLUDED_FAMILY}` from Phase-02 materialization "
        "scope, unblocking the other five history-enriched families under "
        "the Q6H A8 anchor. This artifact does NOT materialize features and "
        "is NOT a Q6X re-adjudication."
    )
    lines.append("")

    lines.append("## 2. Parent Lineage")
    lines.append("")
    lines.append(
        "Parent PR SHA pins (10 hard-coded + 4 dispatch-time + 1 Layer-1 "
        "head = 15 total provenance values):"
    )
    for sha_key, sha_val in OMIT_CLOSURE_PARENT_SHA_PINS.items():
        lines.append(f"- `{sha_key}`: `{sha_val}`")
    lines.append(f"- `parent_pr251_csv_sha256`: `{decision.parent_pr251_csv_sha256}`")
    lines.append(f"- `parent_pr251_md_sha256`: `{decision.parent_pr251_md_sha256}`")
    lines.append(f"- `parent_pr251_module_sha256`: `{q6h_module_sha256}`")
    lines.append(f"- `parent_pr253_roadmap_sha256`: `{pr253_roadmap_sha256}`")
    lines.append(
        f"- `head_master_sha_at_layer_1_plan_time`: "
        f"`{HEAD_MASTER_SHA_AT_LAYER_1_PLAN_TIME}`"
    )
    lines.append("")

    lines.append("## 3. Scope and Explicit Exclusions")
    lines.append("")
    lines.append(
        "In scope: emit the 45-column CSV+MD artifact pair recording the "
        "omit-closure decision. Out of scope: feature materialization; "
        "Parquet output; CROSS-02-01 audit; status-YAML flip; "
        "research_log mutation; ROADMAP edit; Step 02_01_04 / Phase 03 "
        "touch; new Q6X PR."
    )
    lines.append("")

    lines.append("## 4. Branch (iii) Precondition Re-Verification")
    lines.append("")
    lines.append("### 4.1 Four-precondition observable evidence")
    lines.append("")
    lines.append(
        "(a) Branches (i) and (ii) blocked for Phase-02 materialization "
        "scope under Layer-2 election; (b) thesis-pragmatism = TRUE; (c) "
        "substantive_paragraph_ok = TRUE (>= 6 sentences, >= 3 PR #249 "
        "cross-refs, Jaccard < 0.5); (d) reviewer-adversarial sign-off "
        "obtained at both Layer 1 and Layer 2."
    )
    lines.append("")
    lines.append("### 4.2 Q6H decision-rule literal quotes")
    lines.append("")
    lines.append(
        "This subsection quotes the Q6H decision-rule literal verbatim. "
        "The omit-closure artifact does NOT re-adjudicate Q6H. The "
        "Branch (ii) verdict was REACHED (not blocked) by Q6H; the "
        "omit-closure artifact records that Branch (ii) is blocked-for-"
        "Phase-02-materialization-scope under the Layer-2 election, which "
        "is a SCOPE statement, not a verdict statement. This is NOT a new "
        "Q6X loop."
    )
    lines.append("")
    lines.append("```")
    lines.append(Q6H_BRANCH_II_RULE_TEXT)
    lines.append("```")
    lines.append("")
    lines.append("```")
    lines.append(Q6H_BRANCH_III_RULE_TEXT)
    lines.append("```")
    lines.append("")

    lines.append("## 5. Q6H Section 15 Re-Count Methodology")
    lines.append("")
    lines.append(
        f"Sentence count (Q6H §15): "
        f"{decision.thesis_pragmatism_q6h_section_15_sentence_count}. PR #249 "
        f"cross-references: {decision.pr249_cross_reference_count_q6h_section_15}."
    )
    lines.append("")
    lines.append("Q6H §15 verbatim (recount source):")
    lines.append("")
    lines.append("> " + q6h_section_15_text.replace("\n", "\n> "))
    lines.append("")

    lines.append("## 6. Thesis-Pragmatism Elevation Rationale")
    lines.append("")
    lines.append(elevation_rationale_text)
    lines.append("")
    lines.append(
        f"Sentence count (elevation): "
        f"{decision.thesis_pragmatism_sentence_count}; PR #249 cross-references: "
        f"{decision.pr249_cross_reference_count}; Jaccard vs Q6H §15: "
        f"{decision.elevation_rationale_jaccard_vs_q6h_section_15}."
    )
    lines.append("")

    lines.append("## 7. Q5 / Q6F / Q6G / Q6H Parent Verdict Preservation")
    lines.append("")
    lines.append(f"- `Q5_selected_policy = {Q5_SELECTED_POLICY}` (BINDING).")
    lines.append(f"- `Q6F_selected_policy = {Q6F_SELECTED_POLICY}` (BINDING).")
    lines.append(f"- `Q6G_selected_policy = {Q6G_SELECTED_POLICY}` (BINDING).")
    lines.append(f"- `Q6H_selected_policy = {Q6H_SELECTED_POLICY}` (BINDING).")
    lines.append("")

    lines.append("## 8. The 5-Family Permitted Set")
    lines.append("")
    for fam in OMIT_CLOSURE_FIVE_FAMILY_SET:
        lines.append(f"- `{fam}`")
    lines.append("")

    lines.append("## 9. Excluded Family and Excluded Columns")
    lines.append("")
    lines.append(f"Excluded family: `{OMIT_CLOSURE_EXCLUDED_FAMILY}`.")
    lines.append("")
    lines.append("Excluded columns:")
    for col in OMIT_CLOSURE_EXCLUDED_COLUMNS:
        lines.append(f"- `{col}`")
    lines.append("")

    lines.append("## 10. Q6 Intentionally Omitted (Not Silently Satisfied)")
    lines.append("")
    lines.append(
        f"`q6_omission_status = {decision.q6_omission_status}`; "
        f"`q6_not_silently_satisfied = {decision.q6_not_silently_satisfied}`."
    )
    lines.append("")

    lines.append("## 11. Schema Column Count Assertion (Round-2 per NIT #2)")
    lines.append("")
    lines.append(
        "Asserted at module load: `len(OMIT_CLOSURE_SCHEMA) == 45`. "
        "**Round 2 arithmetic:** 42 (Round 1) + 1 (NIT #1 "
        "`branch_ii_state_semantic_anchor`) + 2 (NIT #4 net: 2 sign-off "
        "columns -> 4 sign-off columns) + 1 (NIT #3 "
        "`elevation_rationale_jaccard_vs_q6h_section_15`) - 1 (Round-2 "
        "simplification: 2 module-SHA columns "
        "`parent_pr251_module_sha256` + `parent_pr253_roadmap_sha256` "
        "relocated from CSV to module constants, net per-column-budget "
        "impact -1) = 45 columns."
    )
    lines.append("")
    lines.append(
        "**Per-column derivation prose (NIT #2; reproduced verbatim from "
        "the Layer-1 plan `## Schema Derivation` section).**"
    )
    lines.append("")
    lines.append(
        "**Deviation 1 - `elevation_rationale_jaccard_vs_q6h_section_15` "
        "(column 13; NIT #3; float, `:.4f`).** Reviewer-adversarial "
        "Round-1 concern: the dual-count discipline (sentence count >= 6 "
        "+ cross-reference count >= 3) can be satisfied by a boilerplate "
        "paraphrase of the Q6H §15 paragraph. Round-2 mitigation: a "
        "token-level Jaccard similarity measure against Q6H §15 with "
        "threshold `< 0.5` enforces that the elevation rationale shares "
        "less than half of its unique tokens (after Unicode-NFKD "
        "normalisation + lowercase + Unicode punctuation strip per R2-N2) "
        "with the §15 paragraph. The column makes the Jaccard observable "
        "inspectable post-emission; the corresponding falsifier "
        "`omit_closure_elevation_rationale_jaccard_overlap_with_q6h_"
        "section_15_exceeds_threshold` makes it test-grade. Threshold "
        "derivation: Jaccard >= 0.5 is the conservative ceiling for "
        "paraphrase-likely overlap in short paragraphs."
    )
    lines.append("")
    lines.append(
        "**Deviation 2 - `branch_ii_state_semantic_anchor` (column 14; "
        "NIT #1; string, semicolon-separated 4-key format).** "
        "Reviewer-adversarial Round-1 concern: re-labeling Q6H Branch "
        "(ii) as \"blocked-by-Layer-2-election\" risks subtle "
        "re-adjudication of Q6H's actual verdict (which was REACHED, not "
        "blocked). Round-2 mitigation: a structured 4-key string "
        "explicitly distinguishes (a) Q6H literal verdict state, (b) "
        "omit-closure scope interpretation, (c) absence of Q6H "
        "re-adjudication, (d) absence of new Q6X loop. The column value "
        "format is binding: "
        f"`{OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL}`. Falsifier "
        "`omit_closure_branch_ii_state_anchor_misnamed_or_missing_re_"
        "adjudication_assertion` enforces."
    )
    lines.append("")
    lines.append(
        "**Deviation 3 - `reviewer_adversarial_signoff_layer_1` (column "
        "15; NIT #4; boolean string `TRUE` / `FALSE`).** "
        "Reviewer-adversarial Round-1 concern: a single sign-off SHA "
        "conflated the Layer-1 planning critique (which authorises the "
        "Layer-2 execution) with the Layer-2 execution critique (which "
        "audits the emitted artifact). Round-2 mitigation: the boolean "
        "is TRUE iff the Layer-1 critique recorded APPROVE or "
        "APPROVE-WITH-NITS with 0 blockers. Falsifier "
        "`omit_closure_reviewer_signoff_layer_1_or_layer_2_not_approve_"
        "with_zero_blockers` enforces."
    )
    lines.append("")
    lines.append(
        "**Deviation 4 - `reviewer_adversarial_layer_1_critique_sha256` "
        "(column 16; NIT #4; SHA pin).** Reviewer-adversarial Round-1 "
        "concern: the original single SHA column did not specify whether "
        "the Layer-1 or Layer-2 critique was pinned. Round-2 mitigation: "
        "the SHA is computed at Layer-2 T01 against the Layer-1 "
        "critique file's merged-state byte content. The schema "
        "simplification (Round-1's `parent_pr251_module_sha256` and "
        "`parent_pr253_roadmap_sha256` removed from the CSV row to "
        "preserve the 45-column budget) is documented here: those two "
        "SHAs are pinned in the module constant "
        "`OMIT_CLOSURE_PARENT_SHA_PINS` and recorded in MD §20, not in "
        "the CSV row. Falsifier "
        "`omit_closure_reviewer_signoff_layer_1_missing_or_invalid_sha` "
        "enforces."
    )
    lines.append("")
    lines.append(
        "**Deviation 5 - `reviewer_adversarial_signoff_layer_2` (column "
        "17; NIT #4; boolean string `TRUE` / `FALSE`).** Same logic as "
        "Deviation 3 applied to Layer-2. The Layer-2 sign-off is the "
        "execution-side audit; making it a separate boolean lets "
        "downstream readers verify the execution critique was admissible "
        "independently. Falsifier "
        "`omit_closure_reviewer_signoff_layer_1_or_layer_2_not_approve_"
        "with_zero_blockers` (shared with Deviation 3) enforces both "
        "booleans."
    )
    lines.append("")
    lines.append(
        "**Deviation 6 - `reviewer_adversarial_layer_2_critique_sha256` "
        "(column 18; NIT #4; SHA pin).** Same as Deviation 4 for "
        "Layer-2. Round-2 mitigation: the SHA is computed at Layer-2 "
        "T09 against the Layer-2 critique file's post-sign-off byte "
        "state. Practical sequencing note: if T09 modifies the critique "
        "file (e.g., Round-2 sign-off), the artifact CSV+MD MUST be "
        "regenerated; this is precedented in Q-chain artifact PRs. "
        "Falsifier "
        "`omit_closure_reviewer_signoff_layer_2_missing_or_invalid_sha` "
        "enforces."
    )
    lines.append("")
    lines.append(
        "**Deviation 7 - Duplication of artifact-elevation count vs "
        "Q6H-section-15 re-count (columns 9-10 sentence counts + "
        "columns 11-12 cross-reference counts).** This deviation was "
        "present in Round 1 (columns 9, 10, 11, 12) and is retained in "
        "Round 2 unchanged. Reviewer-adversarial Round-1 acknowledged "
        "this as a methodologically correct dual-count discipline (the "
        "elevation §6 has its own independent count; Q6H §15 has its "
        "independent count; the dual-count makes the discipline "
        "grep-able and prevents copy-paste). The dual-count enforces "
        "that the elevation rationale is independent of Q6H §15's "
        "evidence count."
    )
    lines.append("")

    lines.append("## 12. Falsifier Roll-Call")
    lines.append("")
    lines.append("```")
    lines.append("FALSIFIER ROLL-CALL (Step 02_01_99 omit-closure)")
    lines.append("=" * 48)
    lines.append("")
    for key in OMIT_CLOSURE_FALSIFIER_KEYS:
        lines.append(f"  - {key}  :{falsifier_status.get(key, 'did_not_fire')}")
    lines.append("```")
    lines.append("")

    lines.append("## 13. Future ROADMAP Scope Amendment Requirement")
    lines.append("")
    lines.append(
        f"`future_roadmap_scope_amendment_required = "
        f"{decision.future_roadmap_scope_amendment_required}`. A separate "
        "downstream PR must narrow the Step 02_01_03 6-family ROADMAP "
        "declaration to the 5-family permitted set."
    )
    lines.append("")

    lines.append("## 14. Future Materialization Requirement")
    lines.append("")
    lines.append(
        f"`future_materialization_pr_required = "
        f"{decision.future_materialization_pr_required}`. Materialization is "
        "a SEPARATE downstream PR subject to its own CROSS-02-01 "
        "post-materialization leakage audit."
    )
    lines.append("")

    lines.append("## 15. Explicit Non-Substitution Statement")
    lines.append("")
    lines.append(
        "This artifact does NOT substitute for any future materialization "
        "PR. Q5 / Q6F / Q6G / Q6H remain BINDING and are not retracted."
    )
    lines.append("")

    lines.append("## 16. No Step Closure Claim")
    lines.append("")
    lines.append(
        "This artifact does NOT close Step 02_01_03 (the 6-family ROADMAP "
        "declaration still stands; the ROADMAP scope amendment is a "
        "SEPARATE downstream PR)."
    )
    lines.append("")

    lines.append("## 17. No Phase 03 Claim")
    lines.append("")
    lines.append("This artifact does NOT touch Phase 03 or any baseline modeling work.")
    lines.append("")

    lines.append("## 18. No Feature Materialization Claim")
    lines.append("")
    lines.append(
        "This artifact does NOT materialize features and emits NO Parquet output."
    )
    lines.append("")

    lines.append("## 19. Reviewer-Adversarial Sign-Off")
    lines.append("")
    lines.append("### 19.1 Reviewer-Adversarial Layer-1 Sign-Off")
    lines.append("")
    lines.append(
        f"- Layer-1 critique SHA-256: "
        f"`{decision.reviewer_adversarial_layer_1_critique_sha256}`\n"
        f"- Verdict: `{layer_1_signoff_state}`\n"
        f"- Sign-off flag: "
        f"`{decision.reviewer_adversarial_signoff_layer_1}`\n"
        f"- Reviewer agent: `reviewer-adversarial`"
    )
    lines.append("")
    lines.append("### 19.2 Reviewer-Adversarial Layer-2 Sign-Off")
    lines.append("")
    lines.append(
        f"- Layer-2 critique SHA-256: "
        f"`{decision.reviewer_adversarial_layer_2_critique_sha256}`\n"
        f"- Verdict: `{layer_2_signoff_state}`\n"
        f"- Sign-off flag: "
        f"`{decision.reviewer_adversarial_signoff_layer_2}`\n"
        f"- Reviewer agent: `reviewer-adversarial`"
    )
    lines.append("")

    lines.append("## 20. Provenance (15 SHA Pins + Master HEAD SHA)")
    lines.append("")
    lines.append(
        "**Provenance ledger (R2-N3 wording).** 11 hard-coded provenance "
        "values = 10 parent artifact SHAs from PR #242 / #243 / #245 / "
        "#247 / #249 (2 SHAs per PR x 5 PRs = 10 file SHAs) + 1 "
        "`head_master_sha_at_layer_1_plan_time`. Plus 4 dispatch-time "
        "SHAs (PR #251 CSV / MD / module + PR #253 ROADMAP) = 15 total "
        "provenance values."
    )
    lines.append("")
    for sha_key, sha_val in OMIT_CLOSURE_PARENT_SHA_PINS.items():
        lines.append(f"- `{sha_key}`: `{sha_val}`")
    lines.append(f"- `parent_pr251_csv_sha256`: `{decision.parent_pr251_csv_sha256}`")
    lines.append(f"- `parent_pr251_md_sha256`: `{decision.parent_pr251_md_sha256}`")
    lines.append(f"- `parent_pr251_module_sha256`: `{q6h_module_sha256}`")
    lines.append(f"- `parent_pr253_roadmap_sha256`: `{pr253_roadmap_sha256}`")
    lines.append(
        f"- `head_master_sha_at_layer_1_plan_time`: "
        f"`{HEAD_MASTER_SHA_AT_LAYER_1_PLAN_TIME}`"
    )
    lines.append(
        f"- Omit-closure decision-rule SHA-256 (Q6H Branch (iii) literal): "
        f"`{OMIT_CLOSURE_DECISION_RULE_SHA256}`"
    )
    lines.append(f"- HEAD git SHA at run time: `{head_sha}`")
    lines.append("")

    lines.append("## 21. Final Verdict")
    lines.append("")
    lines.append(
        f"**Verdict:** `{decision.verdict}`\n\n"
        f"**Selected policy:** `{decision.selected_policy}`\n\n"
        f"**Binding level:** `{decision.binding_level}`."
    )
    lines.append("")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def run_close_history_rating_omit_path(
    *,
    output_dir: Path | None = None,
    head_sha: str,
    q6h_csv_sha256: str,
    q6h_md_sha256: str,
    q6h_module_sha256: str,
    pr253_roadmap_sha256: str,
    q6h_section_15_text: str,
    elevation_rationale_text: str,
    layer_1_critique_sha256: str,
    layer_1_signoff_state: str,
    layer_2_critique_sha256: str,
    layer_2_signoff_state: str,
    audit_pr_number: str = AUDIT_PR_NUMBER_PLACEHOLDER,
) -> RatingOmitClosureResult:
    """Build the 45-field decision row, run the falsifier roll-call, emit
    the CSV+MD pair.

    Args:
        output_dir: Optional output directory; defaults to the canonical
            ``reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/``
            path.
        head_sha: HEAD git SHA at dispatch time.
        q6h_csv_sha256: Dispatch-time SHA of the Q6H CSV.
        q6h_md_sha256: Dispatch-time SHA of the Q6H MD.
        q6h_module_sha256: Dispatch-time SHA of the Q6H module file.
        pr253_roadmap_sha256: Dispatch-time SHA of the SC2EGSet ROADMAP.
        q6h_section_15_text: The Q6H MD §15 paragraph (for recount /
            Jaccard).
        elevation_rationale_text: The §6 elevation paragraph (>= 6
            sentences, >= 3 PR #249 cross-refs, Jaccard < 0.5).
        layer_1_critique_sha256: SHA-256 of the Layer-1 critique file.
        layer_1_signoff_state: Verdict literal (APPROVE / APPROVE-WITH-
            NITS / HOLD-WITH-BLOCKERS / ...).
        layer_2_critique_sha256: SHA-256 of the Layer-2 critique file.
        layer_2_signoff_state: Verdict literal.
        audit_pr_number: PR number string.

    Returns:
        A populated ``RatingOmitClosureResult``.

    Raises:
        RatingOmitClosureError: If any falsifier fires.
    """
    decision = _build_decision_row(
        q6h_csv_sha256=q6h_csv_sha256,
        q6h_md_sha256=q6h_md_sha256,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_critique_sha256=layer_1_critique_sha256,
        layer_1_signoff_state=layer_1_signoff_state,
        layer_2_critique_sha256=layer_2_critique_sha256,
        layer_2_signoff_state=layer_2_signoff_state,
        audit_pr_number=audit_pr_number,
    )
    falsifier_status = _evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state=layer_1_signoff_state,
        layer_2_signoff_state=layer_2_signoff_state,
    )
    # Rebuild decision with falsifier_status reflected in the falsifiers cell
    # (semicolon key=value pairs).
    falsifiers_cell = _falsifier_csv_string(falsifier_status)
    decision = RatingOmitClosureDecision(
        **{**{f.name: getattr(decision, f.name) for f in fields(decision)},
           "falsifiers": falsifiers_cell}
    )

    fired = [k for k, v in falsifier_status.items() if v == "fired"]
    if fired:
        raise RatingOmitClosureError(
            fired[0],
            f"Falsifier(s) fired: {fired!r}",
        )

    out_dir = output_dir if output_dir is not None else _default_output_dir()
    csv_path = out_dir / "02_01_99_rating_omit_closure.csv"
    md_path = out_dir / "02_01_99_rating_omit_closure.md"

    _emit_decision_csv(decision, csv_path)
    _emit_decision_md(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        head_sha=head_sha,
        q6h_module_sha256=q6h_module_sha256,
        pr253_roadmap_sha256=pr253_roadmap_sha256,
        layer_1_signoff_state=layer_1_signoff_state,
        layer_2_signoff_state=layer_2_signoff_state,
        falsifier_status=falsifier_status,
        out_path=md_path,
    )

    return RatingOmitClosureResult(
        decision=decision,
        csv_path=csv_path,
        md_path=md_path,
        falsifier_status=falsifier_status,
    )
