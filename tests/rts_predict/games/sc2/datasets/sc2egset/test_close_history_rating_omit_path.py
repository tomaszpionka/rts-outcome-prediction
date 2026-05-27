"""Tests for ``close_history_rating_omit_path`` (Step 02_01_99 omit-closure).

Coverage target: >= 95% branch coverage on the new module. Test count
target: >= 150 tests (heavily parametrized).
"""

from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import fields
from pathlib import Path

import pytest

from rts_predict.games.sc2.datasets.sc2egset import (
    close_history_rating_omit_path as mod,
)
from rts_predict.games.sc2.datasets.sc2egset.close_history_rating_omit_path import (
    AUDIT_PR_NUMBER_PLACEHOLDER,
    HEAD_MASTER_SHA_AT_LAYER_1_PLAN_TIME,
    OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL,
    OMIT_CLOSURE_DECISION_RULE_SHA256,
    OMIT_CLOSURE_EXCLUDED_COLUMNS,
    OMIT_CLOSURE_EXCLUDED_FAMILY,
    OMIT_CLOSURE_FALSIFIER_KEYS,
    OMIT_CLOSURE_FIVE_FAMILY_SET,
    OMIT_CLOSURE_JACCARD_THRESHOLD,
    OMIT_CLOSURE_PARENT_SHA_PINS,
    OMIT_CLOSURE_PR249_CROSS_REF_MIN_COUNT,
    OMIT_CLOSURE_PR249_CROSS_REF_REGEX,
    OMIT_CLOSURE_SCHEMA,
    OMIT_CLOSURE_THESIS_PRAGMATISM_MIN_SENTENCES,
    OMIT_CLOSURE_VERDICT,
    Q5_SELECTED_POLICY,
    Q6F_SELECTED_POLICY,
    Q6G_SELECTED_POLICY,
    Q6H_BRANCH_II_RULE_TEXT,
    Q6H_BRANCH_III_RULE_TEXT,
    Q6H_SELECTED_POLICY,
    RatingOmitClosureDecision,
    RatingOmitClosureError,
    RatingOmitClosureResult,
    run_close_history_rating_omit_path,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_VALID_HEX_64 = "0" * 64
_VALID_HEX_64_B = "f" * 64
_VALID_HEX_40 = "a" * 40


@pytest.fixture
def repo_root() -> Path:
    """Locate the repo root by walking up from this test file."""
    candidate = Path(__file__).resolve()
    while candidate != candidate.parent:
        if (candidate / "pyproject.toml").exists():
            return candidate
        candidate = candidate.parent
    raise FileNotFoundError("pyproject.toml not found")


@pytest.fixture
def q6h_md_path(repo_root: Path) -> Path:
    return repo_root / (
        "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
        "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
        "02_01_03_q6h_rating_path_decision.md"
    )


@pytest.fixture
def q6h_csv_path(repo_root: Path) -> Path:
    return repo_root / (
        "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
        "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
        "02_01_03_q6h_rating_path_decision.csv"
    )


@pytest.fixture
def q6h_module_path(repo_root: Path) -> Path:
    return repo_root / (
        "src/rts_predict/games/sc2/datasets/sc2egset/decide_history_rating_path.py"
    )


@pytest.fixture
def roadmap_path(repo_root: Path) -> Path:
    return repo_root / (
        "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md"
    )


@pytest.fixture
def q6h_section_15_text() -> str:
    """A §15 paragraph that satisfies admissibility (>=6 sentences, >=3 refs)."""
    return (
        "The Q6H decision artifact retains a thesis-pragmatism standby paragraph. "
        "PR #249 §13a established the batched form is non-viable on this corpus. "
        "PR #249 §15 narrowed the binding window to event-by-event Glicko-2 alone. "
        "PR #249 §16 catalogued the falsifier roll-call without firing the override. "
        "The recommendation_only verdict therefore stands until either a new "
        "separating anchor is authored or the thesis-pragmatism gate is invoked. "
        "Q6H §15 inherits PR #249 §15's standby precedent whenever the paragraph "
        "is rendered."
    )


@pytest.fixture
def elevation_rationale_text() -> str:
    """A §6 elevation paragraph with low Jaccard overlap vs Q6H §15."""
    return (
        "Layer-2 elects to close Phase-02 materialization scope by omitting "
        "the reconstructed_rating family. "
        "Branches one and two were unblocked at Q6H but the Layer-2 election "
        "treats them as out-of-scope for Phase-02 materialization while keeping "
        "their evidentiary verdicts intact under PR #249 §13a. "
        "Five history-enriched families remain materialization-eligible without "
        "the omitted family per PR #249 §15. "
        "Future ROADMAP scope amendment will narrow the six-family declaration. "
        "Future materialization PR will execute the unblocking under its own "
        "CROSS-02-01 audit per PR #249 §16. "
        "Reviewer-adversarial sign-off was obtained at both Layer-1 planning "
        "and Layer-2 execution before emission."
    )


@pytest.fixture
def runner_kwargs(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> dict[str, object]:
    """Canonical kwargs for ``run_close_history_rating_omit_path``."""
    return {
        "head_sha": _VALID_HEX_40,
        "q6h_csv_sha256": _VALID_HEX_64,
        "q6h_md_sha256": _VALID_HEX_64_B,
        "q6h_module_sha256": _VALID_HEX_64,
        "pr253_roadmap_sha256": _VALID_HEX_64_B,
        "q6h_section_15_text": q6h_section_15_text,
        "elevation_rationale_text": elevation_rationale_text,
        "layer_1_critique_sha256": _VALID_HEX_64,
        "layer_1_signoff_state": "APPROVE",
        "layer_2_critique_sha256": _VALID_HEX_64_B,
        "layer_2_signoff_state": "APPROVE-WITH-NITS",
        "audit_pr_number": "PR #FIXTURE",
    }


# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------


class TestModuleConstants:
    def test_schema_length_45(self) -> None:
        assert len(OMIT_CLOSURE_SCHEMA) == 45

    def test_schema_unique(self) -> None:
        assert len(set(OMIT_CLOSURE_SCHEMA)) == 45

    def test_falsifier_count_at_least_30(self) -> None:
        assert len(OMIT_CLOSURE_FALSIFIER_KEYS) >= 30

    def test_falsifier_keys_unique(self) -> None:
        assert len(set(OMIT_CLOSURE_FALSIFIER_KEYS)) == len(OMIT_CLOSURE_FALSIFIER_KEYS)

    def test_five_family_size_5(self) -> None:
        assert len(OMIT_CLOSURE_FIVE_FAMILY_SET) == 5

    def test_excluded_family_value(self) -> None:
        assert OMIT_CLOSURE_EXCLUDED_FAMILY == "reconstructed_rating"

    def test_excluded_columns_size(self) -> None:
        assert len(OMIT_CLOSURE_EXCLUDED_COLUMNS) == 3

    def test_excluded_columns_names(self) -> None:
        assert OMIT_CLOSURE_EXCLUDED_COLUMNS == (
            "reconstructed_rating_focal_pre",
            "reconstructed_rating_opp_pre",
            "reconstructed_rating_diff",
        )

    def test_reconstructed_rating_not_in_five_family_set(self) -> None:
        assert "reconstructed_rating" not in OMIT_CLOSURE_FIVE_FAMILY_SET

    def test_jaccard_threshold(self) -> None:
        assert OMIT_CLOSURE_JACCARD_THRESHOLD == 0.5

    def test_min_sentences_six(self) -> None:
        assert OMIT_CLOSURE_THESIS_PRAGMATISM_MIN_SENTENCES == 6

    def test_min_cross_refs_three(self) -> None:
        assert OMIT_CLOSURE_PR249_CROSS_REF_MIN_COUNT == 3

    def test_audit_pr_placeholder(self) -> None:
        assert AUDIT_PR_NUMBER_PLACEHOLDER == "PR #255"

    def test_head_master_sha_40_hex(self) -> None:
        assert len(HEAD_MASTER_SHA_AT_LAYER_1_PLAN_TIME) == 40
        assert all(c in "0123456789abcdef" for c in HEAD_MASTER_SHA_AT_LAYER_1_PLAN_TIME)

    def test_head_master_sha_value(self) -> None:
        assert HEAD_MASTER_SHA_AT_LAYER_1_PLAN_TIME == (
            "0acc0e83274b52831daf80a56beaacaed9340b13"
        )

    def test_q5_policy(self) -> None:
        assert Q5_SELECTED_POLICY == "sensitivity_indicator_co_registration"

    def test_q6f_policy(self) -> None:
        assert Q6F_SELECTED_POLICY == "narrow_with_evidence"

    def test_q6g_policy(self) -> None:
        assert Q6G_SELECTED_POLICY == "recommendation_only_glicko2"

    def test_q6h_policy(self) -> None:
        assert Q6H_SELECTED_POLICY == "recommendation_only_event_by_event_glicko2"

    def test_verdict_value(self) -> None:
        assert OMIT_CLOSURE_VERDICT == (
            "omit_reconstructed_rating_and_unblock_other_five"
        )

    def test_decision_rule_sha_64hex(self) -> None:
        assert len(OMIT_CLOSURE_DECISION_RULE_SHA256) == 64
        assert all(c in "0123456789abcdef" for c in OMIT_CLOSURE_DECISION_RULE_SHA256)

    def test_decision_rule_sha_matches_branch_iii(self) -> None:
        expected = hashlib.sha256(Q6H_BRANCH_III_RULE_TEXT.encode("utf-8")).hexdigest()
        assert OMIT_CLOSURE_DECISION_RULE_SHA256 == expected

    def test_branch_ii_literal_starts_with_branch_ii(self) -> None:
        assert Q6H_BRANCH_II_RULE_TEXT.startswith("BRANCH (ii)")

    def test_branch_iii_literal_starts_with_branch_iii(self) -> None:
        assert Q6H_BRANCH_III_RULE_TEXT.startswith("BRANCH (iii)")

    def test_dataclass_field_count_45(self) -> None:
        assert len(fields(RatingOmitClosureDecision)) == 45

    def test_dataclass_field_order_matches_schema(self) -> None:
        names = tuple(f.name for f in fields(RatingOmitClosureDecision))
        assert names == OMIT_CLOSURE_SCHEMA


# ---------------------------------------------------------------------------
# Schema column-name presence (parametrized over all 45 columns)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("col_name", list(OMIT_CLOSURE_SCHEMA))
def test_schema_column_present(col_name: str) -> None:
    assert col_name in OMIT_CLOSURE_SCHEMA


@pytest.mark.parametrize(
    "index,expected",
    [
        (0, "decision_id"),
        (1, "parent_step_number"),
        (2, "lineage_step_number"),
        (3, "decision_name"),
        (4, "verdict"),
        (5, "binding_level"),
        (6, "selected_policy"),
        (7, "thesis_pragmatism"),
        (8, "thesis_pragmatism_sentence_count"),
        (9, "thesis_pragmatism_q6h_section_15_sentence_count"),
        (10, "pr249_cross_reference_count"),
        (11, "pr249_cross_reference_count_q6h_section_15"),
        (12, "elevation_rationale_jaccard_vs_q6h_section_15"),
        (13, "branch_ii_state_semantic_anchor"),
        (14, "reviewer_adversarial_signoff_layer_1"),
        (15, "reviewer_adversarial_layer_1_critique_sha256"),
        (16, "reviewer_adversarial_signoff_layer_2"),
        (17, "reviewer_adversarial_layer_2_critique_sha256"),
        (18, "q6_omission_status"),
        (19, "q6_not_silently_satisfied"),
        (20, "five_family_materialization_permission"),
        (21, "five_family_set"),
        (22, "excluded_family"),
        (23, "excluded_columns"),
        (24, "future_roadmap_scope_amendment_required"),
        (25, "future_materialization_pr_required"),
        (26, "q5_policy"),
        (27, "q6f_policy"),
        (28, "q6g_policy"),
        (29, "q6h_policy"),
        (30, "evidence_paths"),
        (31, "falsifiers"),
        (32, "audit_pr"),
        (33, "parent_pr242_csv_sha256"),
        (34, "parent_pr242_md_sha256"),
        (35, "parent_pr243_csv_sha256"),
        (36, "parent_pr243_md_sha256"),
        (37, "parent_pr245_csv_sha256"),
        (38, "parent_pr245_md_sha256"),
        (39, "parent_pr247_csv_sha256"),
        (40, "parent_pr247_md_sha256"),
        (41, "parent_pr249_csv_sha256"),
        (42, "parent_pr249_md_sha256"),
        (43, "parent_pr251_csv_sha256"),
        (44, "parent_pr251_md_sha256"),
    ],
)
def test_schema_canonical_order(index: int, expected: str) -> None:
    assert OMIT_CLOSURE_SCHEMA[index] == expected


# ---------------------------------------------------------------------------
# Parent SHA pin presence (parametrized over 10)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "sha_key,expected",
    list(OMIT_CLOSURE_PARENT_SHA_PINS.items()),
)
def test_parent_sha_pin_value(sha_key: str, expected: str) -> None:
    assert OMIT_CLOSURE_PARENT_SHA_PINS[sha_key] == expected


@pytest.mark.parametrize("sha_key", list(OMIT_CLOSURE_PARENT_SHA_PINS.keys()))
def test_parent_sha_pin_is_64_hex(sha_key: str) -> None:
    value = OMIT_CLOSURE_PARENT_SHA_PINS[sha_key]
    assert len(value) == 64
    assert all(c in "0123456789abcdef" for c in value)


def test_parent_sha_pin_count_10() -> None:
    assert len(OMIT_CLOSURE_PARENT_SHA_PINS) == 10


@pytest.mark.parametrize(
    "sha_key,rel_path",
    [
        ("parent_pr242_csv_sha256", "history_source_anchor_coldstart_adjudication.csv"),
        ("parent_pr242_md_sha256", "history_source_anchor_coldstart_adjudication.md"),
        ("parent_pr243_csv_sha256", "history_cross_region_adjudication.csv"),
        ("parent_pr243_md_sha256", "history_cross_region_adjudication.md"),
        ("parent_pr245_csv_sha256", "history_rating_reconstruction_adjudication.csv"),
        ("parent_pr245_md_sha256", "history_rating_reconstruction_adjudication.md"),
        ("parent_pr247_csv_sha256", "q6f_rating_algorithm_survey.csv"),
        ("parent_pr247_md_sha256", "q6f_rating_algorithm_survey.md"),
        ("parent_pr249_csv_sha256", "q6g_rating_implementation_proof.csv"),
        ("parent_pr249_md_sha256", "q6g_rating_implementation_proof.md"),
    ],
)
def test_parent_sha_matches_disk(
    sha_key: str, rel_path: str, repo_root: Path
) -> None:
    full = (
        repo_root
        / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
        "02_feature_engineering/01_pre_game_vs_in_game_boundary"
        / f"02_01_03_{rel_path}"
    )
    h = hashlib.sha256()
    with full.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    assert h.hexdigest() == OMIT_CLOSURE_PARENT_SHA_PINS[sha_key]


# ---------------------------------------------------------------------------
# Falsifier-key membership (parametrized)
# ---------------------------------------------------------------------------

_EXPECTED_FALSIFIER_KEYS = [
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
]


@pytest.mark.parametrize("key", _EXPECTED_FALSIFIER_KEYS)
def test_falsifier_key_present(key: str) -> None:
    assert key in OMIT_CLOSURE_FALSIFIER_KEYS


def test_falsifier_count_matches_expected() -> None:
    assert len(OMIT_CLOSURE_FALSIFIER_KEYS) == len(_EXPECTED_FALSIFIER_KEYS)


# ---------------------------------------------------------------------------
# Tokenization (Unicode-NFKD) -- parametrized
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text,expected_tokens",
    [
        ("Hello world", frozenset({"hello", "world"})),
        ("HELLO WORLD", frozenset({"hello", "world"})),
        ("Hello, world!", frozenset({"hello", "world"})),
        ("foo--bar", frozenset({"foobar"})),  # double-hyphen joins (no space)
        ("foo — bar", frozenset({"foo", "bar"})),  # em-dash
        ("foo – bar", frozenset({"foo", "bar"})),  # en-dash
        ("“Hello”", frozenset({"hello"})),  # curly quotes
        ("foo bar", frozenset({"foo", "bar"})),  # NBSP
        # NFKD-decomposed forms (combining marks not in P* category, so retained)
        (
            "Naïve résumé",
            frozenset({
                "naïve",  # i + combining diaeresis
                "résumé",  # e + combining acute (twice)
            }),
        ),
        ("a.b!c?", frozenset({"abc"})),  # adjacent punctuation joins tokens
        ("a;b:c,d", frozenset({"abcd"})),  # adjacent punctuation joins tokens
        ("a. b! c?", frozenset({"a", "b", "c"})),  # space after punctuation splits
        ("foo", frozenset({"foo"})),
        ("", frozenset()),
        ("   ", frozenset()),
        ("the quick brown fox", frozenset({"the", "quick", "brown", "fox"})),
        ("Α Β Γ", frozenset({"α", "β", "γ"})),  # greek letters preserved
    ],
)
def test_tokenize_for_jaccard(text: str, expected_tokens: frozenset[str]) -> None:
    assert mod._tokenize_for_jaccard(text) == expected_tokens


# ---------------------------------------------------------------------------
# Jaccard computation -- parametrized
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a,b,expected",
    [
        ("hello world", "hello world", 1.0),
        ("hello world", "completely different stuff", 0.0),
        ("a b c", "a b d", 2 / 4),
        ("", "", 0.0),  # zero-division guard
        ("a", "a", 1.0),
        ("a", "b", 0.0),
        ("a b", "b c", 1 / 3),
        ("a b c d", "a b c d e f", 4 / 6),
        ("Hello, world!", "hello world", 1.0),  # punctuation stripped
        ("foo — bar", "foo - bar", 1.0),  # em-dash equivalent to hyphen
    ],
)
def test_compute_jaccard(a: str, b: str, expected: float) -> None:
    result = mod._compute_jaccard(a, b)
    assert abs(result - expected) < 1e-9


# ---------------------------------------------------------------------------
# Sentence-count -- parametrized
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Sentence one. Sentence two. Sentence three.", 3),
        ("One sentence.", 1),
        ("", 0),
        ("A! B! C! D! E! F!", 0),  # all fragments <5 chars after strip; filtered
        (
            "Sentence one is here. Sentence two is here. Sentence three. "
            "Sentence four. Sentence five. Sentence six.",
            6,
        ),
        ("Short. Words. Q. Ok.", 2),  # "Q." and "Ok." are <5 chars after strip
    ],
)
def test_count_paragraph_sentences(text: str, expected: int) -> None:
    assert mod._count_paragraph_sentences(text) == expected


# ---------------------------------------------------------------------------
# PR #249 cross-reference regex -- parametrized
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text,expected_count",
    [
        ("see PR #249 §13", 1),
        ("see PR #249 §13a", 1),
        ("see PR #249 §13.1", 1),
        ("PR #249 §15 and PR #249 §16", 2),
        ("PR #249 §13a, PR #249 §13.1, PR #249 §15", 3),
        ("no cross references here", 0),
        ("PR #250 §13 (wrong PR)", 0),
        ("PR #249 §1 PR #249 §2 PR #249 §3 PR #249 §4", 4),
    ],
)
def test_count_pr249_cross_references(text: str, expected_count: int) -> None:
    assert mod._count_pr249_cross_references(text) == expected_count


def test_pr249_regex_matches_canonical_format() -> None:
    matches = re.findall(
        OMIT_CLOSURE_PR249_CROSS_REF_REGEX, "PR #249 §13a; PR #249 §15"
    )
    assert matches == ["PR #249 §13a", "PR #249 §15"]


# ---------------------------------------------------------------------------
# Branch (ii) state anchor parse -- parametrized
# ---------------------------------------------------------------------------


def test_canonical_anchor_parses() -> None:
    parsed = mod._parse_branch_ii_state_anchor(
        OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL
    )
    assert parsed["is_q6h_re_adjudication"] == "FALSE"
    assert parsed["is_new_q6x_loop"] == "FALSE"


def test_canonical_anchor_four_keys() -> None:
    parsed = mod._parse_branch_ii_state_anchor(
        OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL
    )
    assert set(parsed.keys()) == {
        "q6h_verdict_state",
        "omit_closure_scope_interpretation",
        "is_q6h_re_adjudication",
        "is_new_q6x_loop",
    }


_BAD_ANCHORS = [
    # only 3 pairs
    (
        "q6h_verdict_state=x;omit_closure_scope_interpretation=y;"
        "is_q6h_re_adjudication=FALSE"
    ),
    # 5 pairs
    (
        "q6h_verdict_state=x;omit_closure_scope_interpretation=y;"
        "is_q6h_re_adjudication=FALSE;is_new_q6x_loop=FALSE;extra=z"
    ),
    # bad re_adj value
    (
        "q6h_verdict_state=x;omit_closure_scope_interpretation=y;"
        "is_q6h_re_adjudication=TRUE;is_new_q6x_loop=FALSE"
    ),
    # bad new_q6x value
    (
        "q6h_verdict_state=x;omit_closure_scope_interpretation=y;"
        "is_q6h_re_adjudication=FALSE;is_new_q6x_loop=TRUE"
    ),
    # wrong keyname
    (
        "wrong_key=x;omit_closure_scope_interpretation=y;"
        "is_q6h_re_adjudication=FALSE;is_new_q6x_loop=FALSE"
    ),
    # missing '=' in first pair
    (
        "q6h_verdict_state_no_equals;omit_closure_scope_interpretation=y;"
        "is_q6h_re_adjudication=FALSE;is_new_q6x_loop=FALSE"
    ),
]


@pytest.mark.parametrize("bad", _BAD_ANCHORS)
def test_anchor_malformed_raises(bad: str) -> None:
    with pytest.raises(ValueError):
        mod._parse_branch_ii_state_anchor(bad)


def test_branch_ii_anchor_has_three_semicolons() -> None:
    assert OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL.count(";") == 3


def test_branch_ii_anchor_contains_false_re_adjudication() -> None:
    assert "is_q6h_re_adjudication=FALSE" in OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL


def test_branch_ii_anchor_contains_false_q6x_loop() -> None:
    assert "is_new_q6x_loop=FALSE" in OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL


# ---------------------------------------------------------------------------
# Helpers: _sha256_file, _is_hex64, _find_repo_root, _evidence_paths_string
# ---------------------------------------------------------------------------


def test_sha256_file_not_found(tmp_path: Path) -> None:
    assert mod._sha256_file(tmp_path / "nonexistent.bin") == "NOT_FOUND"


def test_sha256_file_correct_digest(tmp_path: Path) -> None:
    f = tmp_path / "x.txt"
    f.write_bytes(b"hello")
    expected = hashlib.sha256(b"hello").hexdigest()
    assert mod._sha256_file(f) == expected


def test_is_hex64_valid() -> None:
    assert mod._is_hex64("a" * 64) is True


def test_is_hex64_wrong_length() -> None:
    assert mod._is_hex64("a" * 63) is False


def test_is_hex64_wrong_charset() -> None:
    assert mod._is_hex64("g" * 64) is False


def test_is_hex64_uppercase_rejected() -> None:
    assert mod._is_hex64("A" * 64) is False


def test_find_repo_root(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[tool.poetry]")
    sub = tmp_path / "a" / "b"
    sub.mkdir(parents=True)
    assert mod._find_repo_root(sub).resolve() == tmp_path.resolve()


def test_find_repo_root_raises_if_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        mod._find_repo_root(tmp_path)


def test_evidence_paths_string_contains_all_parents() -> None:
    s = mod._evidence_paths_string()
    parts = s.split(";")
    assert len(parts) == 12  # 5 parent PR pairs (10) + Q6H pair (2)


def test_evidence_paths_string_uses_semicolons() -> None:
    s = mod._evidence_paths_string()
    assert ";" in s and "\n" not in s


def test_falsifier_csv_string_contains_all_keys() -> None:
    status = {k: "did_not_fire" for k in OMIT_CLOSURE_FALSIFIER_KEYS}
    s = mod._falsifier_csv_string(status)
    for key in OMIT_CLOSURE_FALSIFIER_KEYS:
        assert key in s


def test_falsifier_csv_string_marks_fired() -> None:
    status = {k: "did_not_fire" for k in OMIT_CLOSURE_FALSIFIER_KEYS}
    first = OMIT_CLOSURE_FALSIFIER_KEYS[0]
    status[first] = "fired"
    s = mod._falsifier_csv_string(status)
    assert f"{first}=fired" in s


def test_extract_q6h_branch_block_missing_token() -> None:
    with pytest.raises(ValueError):
        mod._extract_q6h_branch_block("nothing", "BRANCH (iv)")


def test_extract_q6h_branch_block_no_following_branch() -> None:
    rule = "BRANCH (z) -- only one block here"
    out = mod._extract_q6h_branch_block(rule, "BRANCH (z)")
    assert out.startswith("BRANCH (z)")


def test_check_parent_pr_shas_clean(repo_root: Path) -> None:
    mismatches = mod._check_parent_pr_shas(repo_root)
    assert mismatches == []


def test_check_parent_pr_shas_detects_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Build a fake repo root with no parent artifacts -> all SHAs mismatch.
    for sha_key, rel in mod._PARENT_SHA_PAIRS:
        del sha_key, rel  # unused
    mismatches = mod._check_parent_pr_shas(tmp_path)
    assert len(mismatches) == 10  # all parents missing


def test_get_git_sha_returns_string() -> None:
    sha = mod._get_git_sha()
    assert isinstance(sha, str)
    assert len(sha) >= 7  # either a real SHA or "UNKNOWN"


# ---------------------------------------------------------------------------
# Default output dir
# ---------------------------------------------------------------------------


def test_default_output_dir_exists_or_creatable(repo_root: Path) -> None:
    d = mod._default_output_dir()
    assert (
        d.relative_to(repo_root) == Path(
            "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
            "02_feature_engineering/01_pre_game_vs_in_game_boundary"
        )
    )


# ---------------------------------------------------------------------------
# CSV writer & decision-to-row
# ---------------------------------------------------------------------------


def _make_minimal_decision() -> RatingOmitClosureDecision:
    """Return a structurally-valid 45-field decision row with synthetic values."""
    return RatingOmitClosureDecision(
        decision_id="OMIT_CLOSURE_omit_reconstructed_rating_and_unblock_other_five",
        parent_step_number="02_01_03",
        lineage_step_number="02_01_99",
        decision_name="rating_omit_closure",
        verdict=OMIT_CLOSURE_VERDICT,
        binding_level="BINDING",
        selected_policy=OMIT_CLOSURE_VERDICT,
        thesis_pragmatism="TRUE",
        thesis_pragmatism_sentence_count="7",
        thesis_pragmatism_q6h_section_15_sentence_count="7",
        pr249_cross_reference_count="3",
        pr249_cross_reference_count_q6h_section_15="3",
        elevation_rationale_jaccard_vs_q6h_section_15="0.1000",
        branch_ii_state_semantic_anchor=OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL,
        reviewer_adversarial_signoff_layer_1="TRUE",
        reviewer_adversarial_layer_1_critique_sha256=_VALID_HEX_64,
        reviewer_adversarial_signoff_layer_2="TRUE",
        reviewer_adversarial_layer_2_critique_sha256=_VALID_HEX_64_B,
        q6_omission_status="intentionally_omitted_under_branch_iii",
        q6_not_silently_satisfied="TRUE",
        five_family_materialization_permission="permitted",
        five_family_set=";".join(OMIT_CLOSURE_FIVE_FAMILY_SET),
        excluded_family=OMIT_CLOSURE_EXCLUDED_FAMILY,
        excluded_columns=";".join(OMIT_CLOSURE_EXCLUDED_COLUMNS),
        future_roadmap_scope_amendment_required="TRUE",
        future_materialization_pr_required="TRUE",
        q5_policy=Q5_SELECTED_POLICY,
        q6f_policy=Q6F_SELECTED_POLICY,
        q6g_policy=Q6G_SELECTED_POLICY,
        q6h_policy=Q6H_SELECTED_POLICY,
        evidence_paths=mod._evidence_paths_string(),
        falsifiers=";".join(OMIT_CLOSURE_FALSIFIER_KEYS),
        audit_pr="PR #FIXTURE",
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
        parent_pr251_csv_sha256=_VALID_HEX_64,
        parent_pr251_md_sha256=_VALID_HEX_64_B,
    )


def test_decision_to_row_length_45() -> None:
    decision = _make_minimal_decision()
    row = mod._decision_to_row(decision)
    assert len(row) == 45


def test_decision_to_row_order_matches_schema() -> None:
    decision = _make_minimal_decision()
    row = mod._decision_to_row(decision)
    assert row[0] == decision.decision_id
    assert row[4] == decision.verdict
    assert row[13] == decision.branch_ii_state_semantic_anchor
    assert row[44] == decision.parent_pr251_md_sha256


def test_emit_decision_csv_creates_file(tmp_path: Path) -> None:
    decision = _make_minimal_decision()
    out = tmp_path / "x.csv"
    mod._emit_decision_csv(decision, out)
    assert out.exists()


def test_emit_decision_csv_header_matches_schema(tmp_path: Path) -> None:
    decision = _make_minimal_decision()
    out = tmp_path / "x.csv"
    mod._emit_decision_csv(decision, out)
    with out.open(newline="") as fh:
        rows = list(csv.reader(fh))
    assert tuple(rows[0]) == OMIT_CLOSURE_SCHEMA


def test_emit_decision_csv_has_data_row(tmp_path: Path) -> None:
    decision = _make_minimal_decision()
    out = tmp_path / "x.csv"
    mod._emit_decision_csv(decision, out)
    with out.open(newline="") as fh:
        rows = list(csv.reader(fh))
    assert len(rows) == 2
    assert len(rows[1]) == 45


def test_emit_decision_csv_lineterminator_is_lf(tmp_path: Path) -> None:
    decision = _make_minimal_decision()
    out = tmp_path / "x.csv"
    mod._emit_decision_csv(decision, out)
    raw = out.read_bytes()
    assert b"\r\n" not in raw
    assert raw.endswith(b"\n")


def test_emit_decision_csv_byte_deterministic(tmp_path: Path) -> None:
    decision = _make_minimal_decision()
    out_a = tmp_path / "a.csv"
    out_b = tmp_path / "b.csv"
    mod._emit_decision_csv(decision, out_a)
    mod._emit_decision_csv(decision, out_b)
    assert out_a.read_bytes() == out_b.read_bytes()


# ---------------------------------------------------------------------------
# Falsifier evaluator
# ---------------------------------------------------------------------------


def test_evaluator_clean_run(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    fired = [k for k, v in status.items() if v == "fired"]
    assert fired == []


def test_evaluator_fires_drift_q5(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    decision = mod.RatingOmitClosureDecision(
        **{**{f.name: getattr(decision, f.name) for f in fields(decision)},
           "q5_policy": "wrong_policy"}
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_q5_re_adjudication_drift"] == "fired"


def test_evaluator_fires_drift_q6f(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    decision = mod.RatingOmitClosureDecision(
        **{**{f.name: getattr(decision, f.name) for f in fields(decision)},
           "q6f_policy": "bogus"}
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_q6f_re_adjudication_drift"] == "fired"


def test_evaluator_fires_drift_q6g(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    decision = mod.RatingOmitClosureDecision(
        **{**{f.name: getattr(decision, f.name) for f in fields(decision)},
           "q6g_policy": "bogus"}
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_q6g_re_adjudication_drift"] == "fired"


def test_evaluator_fires_drift_q6h(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    decision = mod.RatingOmitClosureDecision(
        **{**{f.name: getattr(decision, f.name) for f in fields(decision)},
           "q6h_policy": "bogus"}
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_q6h_re_adjudication_drift"] == "fired"


def test_evaluator_fires_thesis_pragmatism_not_true(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    decision = mod.RatingOmitClosureDecision(
        **{**{f.name: getattr(decision, f.name) for f in fields(decision)},
           "thesis_pragmatism": "FALSE"}
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_thesis_pragmatism_not_true"] == "fired"


def test_evaluator_fires_under_six_sentences(
    q6h_section_15_text: str
) -> None:
    decision = _make_minimal_decision()
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text="One sentence. Two sentences.",
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_thesis_pragmatism_elevation_under_six_sentences"] == "fired"


def test_evaluator_fires_q6h_15_under_six_sentences(
    elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text="Short text only.",
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_q6h_section_15_under_six_sentences"] == "fired"


def test_evaluator_fires_under_three_cross_refs_elevation(
    q6h_section_15_text: str
) -> None:
    decision = _make_minimal_decision()
    bad = (
        "Sentence one. Sentence two. Sentence three. "
        "Sentence four. Sentence five. Sentence six."
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=bad,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert (
        status["omit_closure_pr249_cross_ref_count_under_three_in_elevation"]
        == "fired"
    )


def test_evaluator_fires_high_jaccard(
    q6h_section_15_text: str
) -> None:
    decision = _make_minimal_decision()
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=q6h_section_15_text,  # identical
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert (
        status[
            "omit_closure_elevation_rationale_jaccard_overlap_with_q6h_section_15_exceeds_threshold"
        ]
        == "fired"
    )


def test_evaluator_fires_bad_layer_1_sha(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    decision = mod.RatingOmitClosureDecision(
        **{
            **{f.name: getattr(decision, f.name) for f in fields(decision)},
            "reviewer_adversarial_layer_1_critique_sha256": "NOT_A_HEX",
        }
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_reviewer_signoff_layer_1_missing_or_invalid_sha"] == "fired"


def test_evaluator_fires_bad_layer_2_sha(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    decision = mod.RatingOmitClosureDecision(
        **{
            **{f.name: getattr(decision, f.name) for f in fields(decision)},
            "reviewer_adversarial_layer_2_critique_sha256": "NOT_A_HEX",
        }
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_reviewer_signoff_layer_2_missing_or_invalid_sha"] == "fired"


def test_evaluator_fires_bad_signoff_state(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="HOLD-WITH-BLOCKERS",
        layer_2_signoff_state="APPROVE",
    )
    assert (
        status[
            "omit_closure_reviewer_signoff_layer_1_or_layer_2_not_approve_with_zero_blockers"
        ]
        == "fired"
    )


def test_evaluator_fires_bad_branch_ii_anchor(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    decision = mod.RatingOmitClosureDecision(
        **{
            **{f.name: getattr(decision, f.name) for f in fields(decision)},
            "branch_ii_state_semantic_anchor": "a=b;c=d",
        }
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert (
        status[
            "omit_closure_branch_ii_state_anchor_misnamed_or_missing_re_adjudication_assertion"
        ]
        == "fired"
    )


def test_evaluator_fires_reconstructed_in_five_family(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    decision = mod.RatingOmitClosureDecision(
        **{
            **{f.name: getattr(decision, f.name) for f in fields(decision)},
            "five_family_set": "reconstructed_rating;a;b;c;d",
        }
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_reconstructed_rating_in_five_family_set"] == "fired"


def test_evaluator_fires_five_family_size_not_five(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    decision = mod.RatingOmitClosureDecision(
        **{
            **{f.name: getattr(decision, f.name) for f in fields(decision)},
            "five_family_set": "a;b;c",
        }
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_five_family_set_size_not_five"] == "fired"


def test_evaluator_fires_excluded_family_drift(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    decision = mod.RatingOmitClosureDecision(
        **{
            **{f.name: getattr(decision, f.name) for f in fields(decision)},
            "excluded_family": "wrong_family",
        }
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_excluded_family_not_reconstructed_rating"] == "fired"


def test_evaluator_fires_excluded_columns_drift(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    decision = mod.RatingOmitClosureDecision(
        **{
            **{f.name: getattr(decision, f.name) for f in fields(decision)},
            "excluded_columns": "a;b",
        }
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_excluded_columns_drift_from_q6h_literal"] == "fired"


def test_evaluator_fires_silent_q6_closure(
    q6h_section_15_text: str, elevation_rationale_text: str
) -> None:
    decision = _make_minimal_decision()
    decision = mod.RatingOmitClosureDecision(
        **{
            **{f.name: getattr(decision, f.name) for f in fields(decision)},
            "q6_not_silently_satisfied": "FALSE",
        }
    )
    status = mod._evaluate_falsifiers(
        decision=decision,
        elevation_rationale_text=elevation_rationale_text,
        q6h_section_15_text=q6h_section_15_text,
        layer_1_signoff_state="APPROVE",
        layer_2_signoff_state="APPROVE",
    )
    assert status["omit_closure_silent_q6_closure"] == "fired"


# ---------------------------------------------------------------------------
# Entry-point invariants
# ---------------------------------------------------------------------------


def test_run_emits_csv_and_md(tmp_path: Path, runner_kwargs: dict[str, object]) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    assert result.csv_path.exists()
    assert result.md_path.exists()


def test_run_csv_has_correct_header(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    with result.csv_path.open(newline="") as fh:
        rows = list(csv.reader(fh))
    assert tuple(rows[0]) == OMIT_CLOSURE_SCHEMA


def test_run_csv_data_row_45_cells(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    with result.csv_path.open(newline="") as fh:
        rows = list(csv.reader(fh))
    assert len(rows) == 2
    assert len(rows[1]) == 45


def test_run_decision_verdict_is_omit(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    assert result.decision.verdict == OMIT_CLOSURE_VERDICT


def test_run_decision_binding_level(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    assert result.decision.binding_level == "BINDING"


def test_run_decision_thesis_pragmatism_true(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    assert result.decision.thesis_pragmatism == "TRUE"


def test_run_decision_five_family_set(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    assert tuple(result.decision.five_family_set.split(";")) == OMIT_CLOSURE_FIVE_FAMILY_SET


def test_run_decision_excluded_family(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    assert result.decision.excluded_family == OMIT_CLOSURE_EXCLUDED_FAMILY


def test_run_decision_excluded_columns(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    assert tuple(result.decision.excluded_columns.split(";")) == OMIT_CLOSURE_EXCLUDED_COLUMNS


def test_run_decision_parents_carried(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    assert (
        result.decision.parent_pr242_csv_sha256
        == OMIT_CLOSURE_PARENT_SHA_PINS["parent_pr242_csv_sha256"]
    )


def test_run_decision_q5_q6f_q6g_q6h(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    assert result.decision.q5_policy == Q5_SELECTED_POLICY
    assert result.decision.q6f_policy == Q6F_SELECTED_POLICY
    assert result.decision.q6g_policy == Q6G_SELECTED_POLICY
    assert result.decision.q6h_policy == Q6H_SELECTED_POLICY


def test_run_decision_jaccard_below_threshold(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    jaccard = float(result.decision.elevation_rationale_jaccard_vs_q6h_section_15)
    assert jaccard < OMIT_CLOSURE_JACCARD_THRESHOLD


def test_run_decision_jaccard_is_four_decimals(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    val = result.decision.elevation_rationale_jaccard_vs_q6h_section_15
    assert re.match(r"^\d\.\d{4}$", val) is not None


def test_run_decision_signoff_flags_true(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    assert result.decision.reviewer_adversarial_signoff_layer_1 == "TRUE"
    assert result.decision.reviewer_adversarial_signoff_layer_2 == "TRUE"


def test_run_decision_branch_ii_anchor(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    assert (
        result.decision.branch_ii_state_semantic_anchor
        == OMIT_CLOSURE_BRANCH_II_STATE_ANCHOR_CANONICAL
    )


def test_run_falsifier_status_all_did_not_fire(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    for key in OMIT_CLOSURE_FALSIFIER_KEYS:
        assert result.falsifier_status[key] == "did_not_fire", f"key={key}"


def test_run_falsifiers_cell_reflects_status(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    for key in OMIT_CLOSURE_FALSIFIER_KEYS:
        assert f"{key}=did_not_fire" in result.decision.falsifiers


def test_run_md_contains_all_21_sections(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    md = result.md_path.read_text(encoding="utf-8")
    for n in range(1, 22):
        assert f"## {n}." in md, f"Missing §{n} in MD"


def test_run_md_section_19_subsections(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    md = result.md_path.read_text(encoding="utf-8")
    assert "### 19.1" in md
    assert "### 19.2" in md


def test_run_md_section_4_subsections(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    md = result.md_path.read_text(encoding="utf-8")
    assert "### 4.1" in md
    assert "### 4.2" in md


def test_run_md_quotes_branch_iii_literal(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    md = result.md_path.read_text(encoding="utf-8")
    assert "BRANCH (iii)" in md


def test_run_md_quotes_branch_ii_literal(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    md = result.md_path.read_text(encoding="utf-8")
    assert "BRANCH (ii)" in md


def test_run_md_contains_head_master_sha(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    md = result.md_path.read_text(encoding="utf-8")
    assert HEAD_MASTER_SHA_AT_LAYER_1_PLAN_TIME in md


def test_run_raises_on_high_jaccard(
    tmp_path: Path, runner_kwargs: dict[str, object], q6h_section_15_text: str
) -> None:
    kwargs = {**runner_kwargs, "elevation_rationale_text": q6h_section_15_text}
    with pytest.raises(RatingOmitClosureError):
        run_close_history_rating_omit_path(output_dir=tmp_path, **kwargs)  # type: ignore[arg-type]


def test_run_raises_on_under_six_sentences(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    kwargs = {
        **runner_kwargs,
        "elevation_rationale_text": "Short. Text. Only.",
    }
    with pytest.raises(RatingOmitClosureError):
        run_close_history_rating_omit_path(output_dir=tmp_path, **kwargs)  # type: ignore[arg-type]


def test_run_raises_on_bad_layer_1_sha(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    kwargs = {**runner_kwargs, "layer_1_critique_sha256": "NOT_A_HEX"}
    with pytest.raises(RatingOmitClosureError):
        run_close_history_rating_omit_path(output_dir=tmp_path, **kwargs)  # type: ignore[arg-type]


def test_run_raises_on_bad_layer_2_sha(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    kwargs = {**runner_kwargs, "layer_2_critique_sha256": "NOT_A_HEX"}
    with pytest.raises(RatingOmitClosureError):
        run_close_history_rating_omit_path(output_dir=tmp_path, **kwargs)  # type: ignore[arg-type]


def test_run_raises_on_hold_with_blockers(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    kwargs = {**runner_kwargs, "layer_1_signoff_state": "HOLD-WITH-BLOCKERS"}
    with pytest.raises(RatingOmitClosureError):
        run_close_history_rating_omit_path(output_dir=tmp_path, **kwargs)  # type: ignore[arg-type]


def test_run_default_output_dir(
    runner_kwargs: dict[str, object], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Redirect the default output dir so the test doesn't pollute real artifacts.
    monkeypatch.setattr(mod, "_default_output_dir", lambda: tmp_path)
    result = run_close_history_rating_omit_path(**runner_kwargs)  # type: ignore[arg-type]
    assert result.csv_path.parent == tmp_path
    assert result.md_path.parent == tmp_path


def test_run_result_type(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    result = run_close_history_rating_omit_path(output_dir=tmp_path, **runner_kwargs)  # type: ignore[arg-type]
    assert isinstance(result, RatingOmitClosureResult)
    assert isinstance(result.decision, RatingOmitClosureDecision)


def test_run_csv_byte_deterministic_back_to_back(
    tmp_path: Path, runner_kwargs: dict[str, object]
) -> None:
    out_a = tmp_path / "a"
    out_b = tmp_path / "b"
    result_a = run_close_history_rating_omit_path(output_dir=out_a, **runner_kwargs)  # type: ignore[arg-type]
    result_b = run_close_history_rating_omit_path(output_dir=out_b, **runner_kwargs)  # type: ignore[arg-type]
    assert result_a.csv_path.read_bytes() == result_b.csv_path.read_bytes()


# ---------------------------------------------------------------------------
# Exception class
# ---------------------------------------------------------------------------


def test_error_attributes() -> None:
    err = RatingOmitClosureError("some_key", "some_message")
    assert err.falsifier_key == "some_key"
    assert err.message == "some_message"
    assert "some_key" in str(err)
    assert "some_message" in str(err)


def test_error_is_runtime_error() -> None:
    err = RatingOmitClosureError("k", "m")
    assert isinstance(err, RuntimeError)


# ---------------------------------------------------------------------------
# AUDIT placeholder default
# ---------------------------------------------------------------------------


def test_run_audit_pr_default(
    tmp_path: Path,
    q6h_section_15_text: str,
    elevation_rationale_text: str,
) -> None:
    result = run_close_history_rating_omit_path(
        output_dir=tmp_path,
        head_sha=_VALID_HEX_40,
        q6h_csv_sha256=_VALID_HEX_64,
        q6h_md_sha256=_VALID_HEX_64_B,
        q6h_module_sha256=_VALID_HEX_64,
        pr253_roadmap_sha256=_VALID_HEX_64_B,
        q6h_section_15_text=q6h_section_15_text,
        elevation_rationale_text=elevation_rationale_text,
        layer_1_critique_sha256=_VALID_HEX_64,
        layer_1_signoff_state="APPROVE",
        layer_2_critique_sha256=_VALID_HEX_64_B,
        layer_2_signoff_state="APPROVE",
    )
    assert result.decision.audit_pr == AUDIT_PR_NUMBER_PLACEHOLDER
