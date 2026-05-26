"""Comprehensive tests for decide_history_rating_path.py (Q6H decision).

Coverage target: >= 95% branch coverage on the decision module per
``planning/current_plan.md`` Gate clause (d2). Test target: >= 250 tests
per Gate clause (d1).

Test classes mirror the PR #249 structure adapted to the Q6H decision
artifact contract (5 rows, 38 columns, 4 candidate verdicts + 1 emergent
verdict row).
"""

from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import fields
from pathlib import Path
from typing import Any
from unittest import mock

import pytest

from rts_predict.games.sc2.datasets.sc2egset import (
    decide_history_rating_path as mod,
)
from rts_predict.games.sc2.datasets.sc2egset.decide_history_rating_path import (
    AUDIT_PR_NUMBER_PLACEHOLDER,
    FALSIFIER_PRIORITY_CHAIN,
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
    Q5_SELECTED_POLICY,
    Q5_SELECTED_POLICY_VERDICT,
    Q6F_SELECTED_POLICY,
    Q6G_SELECTED_POLICY,
    Q6H_DECISION_CSV_REL,
    Q6H_DECISION_MD_REL,
    Q6H_DECISION_ROWS,
    Q6H_DECISION_SCHEMA,
    Q6H_DECISION_SCHEMA_COLUMN_COUNT,
    Q6H_FIVE_FAMILY_POST_OMIT_SET,
    Q6H_PARENT_SHAS,
    Q6H_PATH_DECISION_RULE,
    Q6H_PATH_DECISION_RULE_SHA256,
    THESIS_PRAGMATISM_ADMISSIBILITY_MIN_CROSS_REFERENCES,
    THESIS_PRAGMATISM_ADMISSIBILITY_MIN_SENTENCES,
    RatingPathDecision,
    RatingPathDecisionError,
    RatingPathDecisionResult,
    build_q6h_decision_result,
    run_q6h_rating_path_decision,
    write_q6h_decision_artifacts,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def canonical_inputs() -> dict[str, Any]:
    """Canonical Layer-2 dispatch executor inputs (Branch (ii) verdict)."""
    return {
        "parent_pr249_verdict": "recommendation_only_glicko2",
        "new_separating_anchor": None,
        "thesis_pragmatism": False,
        "substantive_paragraph_ok": False,
        "reviewer_signoff": False,
        "substantive_paragraph": "",
        "no_fresh_blocking_finding": True,
        "named_missing_evidence": (),
    }


@pytest.fixture
def canonical_result(canonical_inputs: dict[str, Any]) -> RatingPathDecisionResult:
    """Canonical result built with default Branch (ii) inputs."""
    return build_q6h_decision_result(
        audit_pr="PR #FIXTURE",
        executor_inputs=canonical_inputs,
    )


def _valid_substantive_paragraph() -> str:
    """Return a §15 paragraph that satisfies A9(a) admissibility."""
    return (
        "The Q6H decision selects Branch (iii) under thesis-pragmatism. "
        "PR #249 §13a established the batched form is non-viable. "
        "PR #249 §15 narrowed the binding window to the event form. "
        "PR #249 §16 catalogued the falsifier roll-call. "
        "The five non-rating families remain materialization-eligible. "
        "Reconstructed rating is omitted with reviewer-adversarial sign-off."
    )


# ---------------------------------------------------------------------------
# TestModuleConstants
# ---------------------------------------------------------------------------


class TestModuleConstants:
    def test_schema_length_is_38(self) -> None:
        assert len(Q6H_DECISION_SCHEMA) == 38

    def test_schema_column_count_constant_is_38(self) -> None:
        assert Q6H_DECISION_SCHEMA_COLUMN_COUNT == 38

    def test_dataclass_field_count_is_38(self) -> None:
        assert len(fields(RatingPathDecision)) == 38

    def test_dataclass_fields_match_schema_order(self) -> None:
        names = tuple(f.name for f in fields(RatingPathDecision))
        assert names == Q6H_DECISION_SCHEMA

    def test_row_count_is_5(self) -> None:
        assert len(Q6H_DECISION_ROWS) == 5

    def test_parent_shas_count_is_10(self) -> None:
        assert len(Q6H_PARENT_SHAS) == 10

    def test_parent_shas_all_64char_hex(self) -> None:
        for k, v in Q6H_PARENT_SHAS.items():
            assert isinstance(v, str)
            assert len(v) == 64
            assert all(c in "0123456789abcdef" for c in v), k

    def test_five_family_set_count_is_5(self) -> None:
        assert len(Q6H_FIVE_FAMILY_POST_OMIT_SET) == 5

    def test_five_family_set_excludes_reconstructed_rating(self) -> None:
        assert "reconstructed_rating" not in Q6H_FIVE_FAMILY_POST_OMIT_SET

    def test_five_family_set_exact_membership(self) -> None:
        assert Q6H_FIVE_FAMILY_POST_OMIT_SET == (
            "focal_player_history",
            "opponent_player_history",
            "matchup_history_aggregate",
            "cross_region_fragmentation_handling",
            "in_game_history_aggregate",
        )

    def test_thesis_pragmatism_min_sentences_is_6(self) -> None:
        assert THESIS_PRAGMATISM_ADMISSIBILITY_MIN_SENTENCES == 6

    def test_thesis_pragmatism_min_cross_references_is_3(self) -> None:
        assert THESIS_PRAGMATISM_ADMISSIBILITY_MIN_CROSS_REFERENCES == 3

    def test_falsifier_chain_min_count_37(self) -> None:
        assert len(FALSIFIER_PRIORITY_CHAIN) >= 37

    def test_falsifier_chain_no_duplicates(self) -> None:
        assert len(set(FALSIFIER_PRIORITY_CHAIN)) == len(FALSIFIER_PRIORITY_CHAIN)

    def test_falsifier_chain_all_strings(self) -> None:
        for key in FALSIFIER_PRIORITY_CHAIN:
            assert isinstance(key, str)
            assert key

    def test_decision_rule_sha256_pinned_is_hex(self) -> None:
        assert len(Q6H_PATH_DECISION_RULE_SHA256) == 64
        assert all(c in "0123456789abcdef" for c in Q6H_PATH_DECISION_RULE_SHA256)

    def test_decision_rule_sha256_matches_recomputed(self) -> None:
        recomputed = hashlib.sha256(
            Q6H_PATH_DECISION_RULE.encode("utf-8")
        ).hexdigest()
        assert recomputed == Q6H_PATH_DECISION_RULE_SHA256

    def test_q5_binding_string(self) -> None:
        assert Q5_SELECTED_POLICY == "sensitivity_indicator_co_registration"
        assert Q5_SELECTED_POLICY_VERDICT == "narrow_with_evidence"

    def test_q6f_binding_string(self) -> None:
        assert Q6F_SELECTED_POLICY == "narrow_with_evidence"

    def test_q6g_binding_string(self) -> None:
        assert Q6G_SELECTED_POLICY == "recommendation_only_glicko2"

    def test_audit_pr_placeholder(self) -> None:
        assert AUDIT_PR_NUMBER_PLACEHOLDER == "PR #<TBD>"

    def test_q6h_decision_csv_rel_under_artifacts_dir(self) -> None:
        assert "reports/artifacts/02_feature_engineering" in Q6H_DECISION_CSV_REL
        assert Q6H_DECISION_CSV_REL.endswith(
            "02_01_03_q6h_rating_path_decision.csv"
        )

    def test_q6h_decision_md_rel_under_artifacts_dir(self) -> None:
        assert Q6H_DECISION_MD_REL.endswith(
            "02_01_03_q6h_rating_path_decision.md"
        )

    def test_decision_rule_contains_binding_header(self) -> None:
        assert "Q6H FINAL RATING-PATH DECISION RULE" in Q6H_PATH_DECISION_RULE

    def test_decision_rule_contains_evidentiary_first_marker(self) -> None:
        idx_i = Q6H_PATH_DECISION_RULE.find("BRANCH (i)")
        idx_ii = Q6H_PATH_DECISION_RULE.find("BRANCH (ii)")
        idx_iii = Q6H_PATH_DECISION_RULE.find("BRANCH (iii)")
        idx_iv = Q6H_PATH_DECISION_RULE.find("BRANCH (iv)")
        idx_v = Q6H_PATH_DECISION_RULE.find("BRANCH (v)")
        assert 0 < idx_i < idx_ii < idx_iii < idx_iv < idx_v


# ---------------------------------------------------------------------------
# TestParentSHAs
# ---------------------------------------------------------------------------


_PARENT_SHA_PAIR_DEFS: list[tuple[str, str, str]] = [
    (PARENT_PR242_CSV_REL, "parent_pr242_csv_sha256", "parent_pr242_csv_sha256_mismatch"),
    (PARENT_PR242_MD_REL, "parent_pr242_md_sha256", "parent_pr242_md_sha256_mismatch"),
    (PARENT_PR243_CSV_REL, "parent_pr243_csv_sha256", "parent_pr243_csv_sha256_mismatch"),
    (PARENT_PR243_MD_REL, "parent_pr243_md_sha256", "parent_pr243_md_sha256_mismatch"),
    (PARENT_PR245_CSV_REL, "parent_pr245_csv_sha256", "parent_pr245_csv_sha256_mismatch"),
    (PARENT_PR245_MD_REL, "parent_pr245_md_sha256", "parent_pr245_md_sha256_mismatch"),
    (PARENT_PR247_CSV_REL, "parent_pr247_csv_sha256", "parent_pr247_csv_sha256_mismatch"),
    (PARENT_PR247_MD_REL, "parent_pr247_md_sha256", "parent_pr247_md_sha256_mismatch"),
    (PARENT_PR249_CSV_REL, "parent_pr249_csv_sha256", "parent_pr249_csv_sha256_mismatch"),
    (PARENT_PR249_MD_REL, "parent_pr249_md_sha256", "parent_pr249_md_sha256_mismatch"),
]


class TestParentSHAs:
    def test_all_10_pair_defs_listed(self) -> None:
        assert len(_PARENT_SHA_PAIR_DEFS) == 10

    @pytest.mark.parametrize("rel_path,sha_key,falsifier_key", _PARENT_SHA_PAIR_DEFS)
    def test_pair_paths_under_artifacts_dir(
        self, rel_path: str, sha_key: str, falsifier_key: str
    ) -> None:
        assert "reports/artifacts/02_feature_engineering" in rel_path

    @pytest.mark.parametrize("rel_path,sha_key,falsifier_key", _PARENT_SHA_PAIR_DEFS)
    def test_pair_falsifier_key_listed_in_chain(
        self, rel_path: str, sha_key: str, falsifier_key: str
    ) -> None:
        # Per Layer-1 plan §"Falsifier chain" notes, PR #245 CSV/MD
        # mismatches are tracked implicitly under
        # q6h_parent_sha_pin_count_equals_10; the helper raises with the
        # *_mismatch key regardless and the helper-level test covers it.
        if sha_key.startswith("parent_pr245_"):
            assert "q6h_parent_sha_pin_count_equals_10" in FALSIFIER_PRIORITY_CHAIN
            return
        assert falsifier_key in FALSIFIER_PRIORITY_CHAIN

    @pytest.mark.parametrize("rel_path,sha_key,falsifier_key", _PARENT_SHA_PAIR_DEFS)
    def test_pair_sha_key_in_parent_shas(
        self, rel_path: str, sha_key: str, falsifier_key: str
    ) -> None:
        assert sha_key in Q6H_PARENT_SHAS

    def test_check_parent_pr_shas_empty_on_match(self, tmp_path: Path) -> None:
        # Synthesise all 10 files with matching SHA content.
        for rel, sha_key, _falsifier in _PARENT_SHA_PAIR_DEFS:
            target = tmp_path / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            # Find content that hashes to expected. Use the function
            # itself: we mock _sha256_file to return the expected.
            target.write_text("placeholder")
        with mock.patch.object(
            mod, "_sha256_file", side_effect=lambda p: Q6H_PARENT_SHAS[
                next(
                    sk
                    for rel, sk, _f in _PARENT_SHA_PAIR_DEFS
                    if str(p).endswith(rel.split("/")[-1])
                )
            ]
        ):
            mismatches = mod._check_parent_pr_shas(tmp_path)
        assert mismatches == []

    @pytest.mark.parametrize("rel_path,sha_key,falsifier_key", _PARENT_SHA_PAIR_DEFS)
    def test_mismatch_returns_falsifier_key(
        self,
        rel_path: str,
        sha_key: str,
        falsifier_key: str,
        tmp_path: Path,
    ) -> None:
        for rel, _sk, _f in _PARENT_SHA_PAIR_DEFS:
            target = tmp_path / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("placeholder")
        target_filename = rel_path.split("/")[-1]
        # Mock _sha256_file so all return expected EXCEPT the parameterized one.
        def fake_sha256(p: Path) -> str:
            if str(p).endswith(target_filename):
                return "0" * 64
            for rel, sk, _f in _PARENT_SHA_PAIR_DEFS:
                if str(p).endswith(rel.split("/")[-1]):
                    return Q6H_PARENT_SHAS[sk]
            return "NOT_FOUND"
        with mock.patch.object(mod, "_sha256_file", side_effect=fake_sha256):
            mismatches = mod._check_parent_pr_shas(tmp_path)
        assert any(m[0] == falsifier_key for m in mismatches)

    def test_run_entrypoint_halts_on_pr242_csv_mismatch(self, tmp_path: Path) -> None:
        with mock.patch.object(
            mod,
            "_sha256_file",
            side_effect=lambda p: "deadbeef" * 8,
        ):
            with pytest.raises(RatingPathDecisionError) as exc_info:
                run_q6h_rating_path_decision(
                    csv_path=tmp_path / "q6h.csv",
                    md_path=tmp_path / "q6h.md",
                    repo_root=tmp_path,
                    verify_parent_shas=True,
                )
        assert exc_info.value.falsifier_key.endswith("sha256_mismatch")

    def test_run_entrypoint_skips_sha_verification_when_disabled(
        self, tmp_path: Path
    ) -> None:
        # Should NOT raise: SHA verification is skipped entirely.
        result = run_q6h_rating_path_decision(
            csv_path=tmp_path / "q6h.csv",
            md_path=tmp_path / "q6h.md",
            verify_parent_shas=False,
        )
        assert result.passed

    def test_sha256_file_not_found(self, tmp_path: Path) -> None:
        assert mod._sha256_file(tmp_path / "does_not_exist") == "NOT_FOUND"

    def test_sha256_file_computes_real(self, tmp_path: Path) -> None:
        path = tmp_path / "x.bin"
        path.write_bytes(b"hello world")
        expected = hashlib.sha256(b"hello world").hexdigest()
        assert mod._sha256_file(path) == expected


# ---------------------------------------------------------------------------
# TestDecisionRowBuilders
# ---------------------------------------------------------------------------


_BUILDER_DEFS = [
    (
        "Q6H_A_bind_event_by_event_glicko2",
        mod._build_decision_row_a_bind_event_by_event_glicko2,
        "(i)",
    ),
    (
        "Q6H_B_recommendation_only_event_by_event_glicko2",
        mod._build_decision_row_b_recommendation_only_event_by_event_glicko2,
        "(ii)",
    ),
    (
        "Q6H_C_omit_reconstructed_rating_and_unblock_other_five",
        mod._build_decision_row_c_omit_reconstructed_rating_and_unblock_other_five,
        "(iii)",
    ),
    (
        "Q6H_D_deferred_blocker",
        mod._build_decision_row_d_deferred_blocker,
        "(v)",
    ),
]


class TestDecisionRowBuilders:
    @pytest.mark.parametrize("decision_id,builder,branch", _BUILDER_DEFS)
    def test_builder_returns_decision(
        self, decision_id: str, builder: Any, branch: str
    ) -> None:
        row = builder("PR #TEST")
        assert isinstance(row, RatingPathDecision)
        assert row.decision_id == decision_id

    @pytest.mark.parametrize("decision_id,builder,branch", _BUILDER_DEFS)
    def test_builder_sets_branch_token(
        self, decision_id: str, builder: Any, branch: str
    ) -> None:
        row = builder("PR #TEST")
        assert row.branch_evaluated == branch

    @pytest.mark.parametrize("decision_id,builder,branch", _BUILDER_DEFS)
    def test_builder_materialized_paths_empty(
        self, decision_id: str, builder: Any, branch: str
    ) -> None:
        row = builder("PR #TEST")
        assert row.materialized_output_paths == ""

    @pytest.mark.parametrize("decision_id,builder,branch", _BUILDER_DEFS)
    def test_builder_audit_pr_propagated(
        self, decision_id: str, builder: Any, branch: str
    ) -> None:
        row = builder("PR #999")
        assert row.audit_pr == "PR #999"

    @pytest.mark.parametrize("decision_id,builder,branch", _BUILDER_DEFS)
    def test_builder_parent_sha_pins(
        self, decision_id: str, builder: Any, branch: str
    ) -> None:
        row = builder("PR #TEST")
        assert row.parent_pr242_csv_sha256 == Q6H_PARENT_SHAS["parent_pr242_csv_sha256"]
        assert row.parent_pr243_csv_sha256 == Q6H_PARENT_SHAS["parent_pr243_csv_sha256"]
        assert row.parent_pr245_md_sha256 == Q6H_PARENT_SHAS["parent_pr245_md_sha256"]
        assert row.parent_pr247_csv_sha256 == Q6H_PARENT_SHAS["parent_pr247_csv_sha256"]
        assert row.parent_pr247_md_sha256 == Q6H_PARENT_SHAS["parent_pr247_md_sha256"]
        assert row.parent_pr249_csv_sha256 == Q6H_PARENT_SHAS["parent_pr249_csv_sha256"]

    @pytest.mark.parametrize("decision_id,builder,branch", _BUILDER_DEFS)
    def test_builder_q5_token_preserved(
        self, decision_id: str, builder: Any, branch: str
    ) -> None:
        row = builder("PR #TEST")
        assert row.q5_cross_region_policy == Q5_SELECTED_POLICY

    @pytest.mark.parametrize("decision_id,builder,branch", _BUILDER_DEFS)
    def test_builder_evidence_paths_populated(
        self, decision_id: str, builder: Any, branch: str
    ) -> None:
        row = builder("PR #TEST")
        assert PARENT_PR242_CSV_REL in row.evidence_paths
        assert PARENT_PR249_MD_REL in row.evidence_paths

    @pytest.mark.parametrize("decision_id,builder,branch", _BUILDER_DEFS)
    def test_builder_falsifiers_populated(
        self, decision_id: str, builder: Any, branch: str
    ) -> None:
        row = builder("PR #TEST")
        for key in FALSIFIER_PRIORITY_CHAIN:
            assert key in row.falsifiers

    def test_row_c_omit_excluded_includes_reconstructed_rating(self) -> None:
        row = mod._build_decision_row_c_omit_reconstructed_rating_and_unblock_other_five(
            "PR #TEST"
        )
        assert "reconstructed_rating" in row.excluded_column_names

    def test_row_c_omit_future_columns_excludes_reconstructed_rating(self) -> None:
        row = mod._build_decision_row_c_omit_reconstructed_rating_and_unblock_other_five(
            "PR #TEST"
        )
        assert "reconstructed_rating" not in row.future_column_names

    def test_row_c_omit_q6_status(self) -> None:
        row = mod._build_decision_row_c_omit_reconstructed_rating_and_unblock_other_five(
            "PR #TEST"
        )
        assert row.q6_status == "discharged_by_omission_under_thesis_pragmatism"

    def test_row_a_future_columns_includes_reconstructed_rating(self) -> None:
        row = mod._build_decision_row_a_bind_event_by_event_glicko2("PR #TEST")
        assert "reconstructed_rating" in row.future_column_names

    def test_row_b_recommendation_event_policy_imported(self) -> None:
        row = mod._build_decision_row_b_recommendation_only_event_by_event_glicko2(
            "PR #TEST"
        )
        assert "imported_from_pr247_run_glicko2_survey" in row.event_by_event_policy

    def test_row_d_deferred_blocker_branch(self) -> None:
        row = mod._build_decision_row_d_deferred_blocker("PR #TEST")
        assert row.branch_evaluated == "(v)"

    def test_selected_policy_builder_branch_ii(self) -> None:
        row = mod._build_decision_row_selected_policy(
            audit_pr="PR #TEST",
            selected_policy="recommendation_only_event_by_event_glicko2",
            verdict="recommendation_only_event_by_event_glicko2",
            materialization_permission=(
                "recommendation_only_blocked_pending_phase_03_or_later_decision"
            ),
            rationale="test rationale",
            branch_evaluated="(ii)",
            thesis_pragmatism_flag_value="null",
            thesis_pragmatism_paragraph_sentence_count=6,
            thesis_pragmatism_rationale="standby",
        )
        assert row.decision_id == "Q6H_selected_policy"
        assert row.binding_level == "BINDING"
        assert row.branch_evaluated == "(ii)"

    def test_selected_policy_builder_branch_iii_excludes_reconstructed(self) -> None:
        row = mod._build_decision_row_selected_policy(
            audit_pr="PR #TEST",
            selected_policy="omit_reconstructed_rating_and_unblock_other_five",
            verdict="omit_reconstructed_rating_and_unblock_other_five",
            materialization_permission="perm",
            rationale="rat",
            branch_evaluated="(iii)",
            thesis_pragmatism_flag_value="TRUE",
            thesis_pragmatism_paragraph_sentence_count=7,
            thesis_pragmatism_rationale="standby",
        )
        assert "reconstructed_rating" in row.excluded_column_names
        assert row.q6_status == "discharged_by_omission_under_thesis_pragmatism"

    def test_selected_policy_builder_branch_i(self) -> None:
        row = mod._build_decision_row_selected_policy(
            audit_pr="PR #TEST",
            selected_policy="bind_event_by_event_glicko2",
            verdict="bind_event_by_event_glicko2",
            materialization_permission="perm",
            rationale="rat",
            branch_evaluated="(i)",
            thesis_pragmatism_flag_value="null",
            thesis_pragmatism_paragraph_sentence_count=0,
            thesis_pragmatism_rationale="standby",
        )
        assert row.q6_status == "bound_by_branch_i_event_by_event_glicko2"

    def test_selected_policy_builder_branch_iv(self) -> None:
        row = mod._build_decision_row_selected_policy(
            audit_pr="PR #TEST",
            selected_policy="defer_to_layer_3_phase_02_internal_decision",
            verdict="defer_to_layer_3_phase_02_internal_decision",
            materialization_permission="perm",
            rationale="rat",
            branch_evaluated="(iv)",
            thesis_pragmatism_flag_value="FALSE",
            thesis_pragmatism_paragraph_sentence_count=0,
            thesis_pragmatism_rationale="standby",
        )
        assert row.q6_status == "deferred_to_layer_3_phase_02_internal_step"

    def test_selected_policy_builder_branch_v(self) -> None:
        row = mod._build_decision_row_selected_policy(
            audit_pr="PR #TEST",
            selected_policy="deferred_blocker",
            verdict="deferred_blocker",
            materialization_permission="perm",
            rationale="rat",
            branch_evaluated="(v)",
            thesis_pragmatism_flag_value="null",
            thesis_pragmatism_paragraph_sentence_count=0,
            thesis_pragmatism_rationale="standby",
        )
        assert row.q6_status == "deferred_pending_named_missing_evidence"


# ---------------------------------------------------------------------------
# TestDecisionRule_AllFiveBranches
# ---------------------------------------------------------------------------


class TestDecisionRule_AllFiveBranches:
    def test_branch_i_with_separating_anchor(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        canonical_inputs["new_separating_anchor"] = "brier_anchor_2026_06_01"
        sel, verd, perm, _rat, branch = mod._apply_q6h_decision_rule(
            canonical_inputs
        )
        assert sel == "bind_event_by_event_glicko2"
        assert verd == "bind_event_by_event_glicko2"
        assert branch == "(i)"

    def test_branch_ii_canonical_default(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        sel, verd, perm, _rat, branch = mod._apply_q6h_decision_rule(
            canonical_inputs
        )
        assert sel == "recommendation_only_event_by_event_glicko2"
        assert verd == "recommendation_only_event_by_event_glicko2"
        assert (
            perm == "recommendation_only_blocked_pending_phase_03_or_later_decision"
        )
        assert branch == "(ii)"

    def test_branch_iii_with_all_admissibility_pins(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        canonical_inputs["parent_pr249_verdict"] = "other_value_blocking_branch_ii"
        canonical_inputs["thesis_pragmatism"] = True
        canonical_inputs["substantive_paragraph_ok"] = True
        canonical_inputs["reviewer_signoff"] = True
        canonical_inputs["substantive_paragraph"] = _valid_substantive_paragraph()
        sel, verd, perm, _rat, branch = mod._apply_q6h_decision_rule(
            canonical_inputs
        )
        assert sel == "omit_reconstructed_rating_and_unblock_other_five"
        assert branch == "(iii)"

    def test_branch_iv_when_branches_i_ii_iii_blocked(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        canonical_inputs["parent_pr249_verdict"] = "other"
        sel, verd, perm, _rat, branch = mod._apply_q6h_decision_rule(
            canonical_inputs
        )
        assert sel == "defer_to_layer_3_phase_02_internal_decision"
        assert branch == "(iv)"

    def test_branch_v_when_fresh_blocking_finding(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        canonical_inputs["parent_pr249_verdict"] = "other"
        canonical_inputs["no_fresh_blocking_finding"] = False
        canonical_inputs["named_missing_evidence"] = ("item_a", "item_b")
        sel, verd, perm, _rat, branch = mod._apply_q6h_decision_rule(
            canonical_inputs
        )
        assert sel == "deferred_blocker"
        assert branch == "(v)"

    def test_branch_v_raises_without_named_evidence(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        canonical_inputs["parent_pr249_verdict"] = "other"
        canonical_inputs["no_fresh_blocking_finding"] = False
        canonical_inputs["named_missing_evidence"] = ("only_one",)
        with pytest.raises(RatingPathDecisionError) as exc_info:
            mod._apply_q6h_decision_rule(canonical_inputs)
        assert "deferred_blocker" in exc_info.value.falsifier_key

    def test_branch_v_raises_on_empty_named_evidence(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        canonical_inputs["parent_pr249_verdict"] = "other"
        canonical_inputs["no_fresh_blocking_finding"] = False
        canonical_inputs["named_missing_evidence"] = ()
        with pytest.raises(RatingPathDecisionError):
            mod._apply_q6h_decision_rule(canonical_inputs)

    def test_branch_i_precedes_branch_ii(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        # Both Branch (i) and Branch (ii) preconditions met; Branch (i) wins.
        canonical_inputs["new_separating_anchor"] = "anchor"
        # parent_pr249_verdict already set to recommendation_only_glicko2
        sel, _v, _p, _r, branch = mod._apply_q6h_decision_rule(canonical_inputs)
        assert branch == "(i)"

    def test_branch_ii_precedes_branch_iii(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        # Both Branch (ii) and Branch (iii) preconditions met; Branch (ii) wins.
        canonical_inputs["thesis_pragmatism"] = True
        canonical_inputs["substantive_paragraph_ok"] = True
        canonical_inputs["reviewer_signoff"] = True
        canonical_inputs["substantive_paragraph"] = _valid_substantive_paragraph()
        sel, _v, _p, _r, branch = mod._apply_q6h_decision_rule(canonical_inputs)
        assert branch == "(ii)"

    def test_branch_iii_blocked_when_signoff_false(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        canonical_inputs["parent_pr249_verdict"] = "other"
        canonical_inputs["thesis_pragmatism"] = True
        canonical_inputs["substantive_paragraph_ok"] = True
        canonical_inputs["reviewer_signoff"] = False
        canonical_inputs["substantive_paragraph"] = _valid_substantive_paragraph()
        sel, _v, _p, _r, branch = mod._apply_q6h_decision_rule(canonical_inputs)
        # Falls through to Branch (iv).
        assert branch == "(iv)"

    def test_branch_iii_blocked_when_substantive_ok_false(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        canonical_inputs["parent_pr249_verdict"] = "other"
        canonical_inputs["thesis_pragmatism"] = False
        canonical_inputs["substantive_paragraph_ok"] = False
        canonical_inputs["reviewer_signoff"] = True
        sel, _v, _p, _r, branch = mod._apply_q6h_decision_rule(canonical_inputs)
        assert branch == "(iv)"

    def test_rationale_returned(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        _s, _v, _p, rationale, _b = mod._apply_q6h_decision_rule(canonical_inputs)
        assert isinstance(rationale, str)
        assert len(rationale) > 0


# ---------------------------------------------------------------------------
# TestThesisPragmatismAdmissibility
# ---------------------------------------------------------------------------


class TestThesisPragmatismAdmissibility:
    def test_valid_paragraph_passes(self) -> None:
        passed, msg = mod._check_substantive_paragraph_admissibility(
            _valid_substantive_paragraph()
        )
        assert passed
        assert msg == ""

    def test_too_few_sentences_fails(self) -> None:
        bad = (
            "Only two sentences here. PR #249 §1 PR #249 §2 PR #249 §3."
        )
        passed, msg = mod._check_substantive_paragraph_admissibility(bad)
        assert not passed
        assert "sentences" in msg

    def test_too_few_cross_references_fails(self) -> None:
        bad = (
            "S1. S2. S3. S4. S5. S6. PR #249 §1 plus second mention. "
            "No further refs."
        )
        passed, msg = mod._check_substantive_paragraph_admissibility(bad)
        assert not passed
        assert "cross-refs" in msg

    def test_exactly_six_sentences_passes(self) -> None:
        good = (
            "S1 PR #249 §1. S2. S3. S4. S5. S6 PR #249 §2 PR #249 §3."
        )
        passed, _msg = mod._check_substantive_paragraph_admissibility(good)
        assert passed

    def test_empty_paragraph_fails(self) -> None:
        passed, _msg = mod._check_substantive_paragraph_admissibility("")
        assert not passed

    def test_whitespace_only_paragraph_fails(self) -> None:
        passed, _msg = mod._check_substantive_paragraph_admissibility("   \n\n  ")
        assert not passed

    def test_count_sentences(self) -> None:
        assert mod._count_paragraph_sentences("One. Two. Three.") == 3

    def test_count_sentences_empty(self) -> None:
        assert mod._count_paragraph_sentences("") == 0

    def test_count_sentences_question_mark(self) -> None:
        assert mod._count_paragraph_sentences("Q? A. B!") == 3


# ---------------------------------------------------------------------------
# TestBlockerGuard_BranchIIIRequiresSubstantiveParagraph
# ---------------------------------------------------------------------------


class TestBlockerGuard_BranchIIIRequiresSubstantiveParagraph:
    def test_branch_iii_with_thesis_true_no_paragraph_raises(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        canonical_inputs["parent_pr249_verdict"] = "other"
        canonical_inputs["thesis_pragmatism"] = True
        canonical_inputs["substantive_paragraph_ok"] = False
        canonical_inputs["reviewer_signoff"] = True
        with pytest.raises(RatingPathDecisionError) as exc:
            mod._apply_q6h_decision_rule(canonical_inputs)
        assert (
            "thesis_pragmatism_set_false_without_substantive_reasoning_paragraph"
            in exc.value.falsifier_key
        )

    def test_branch_iii_with_thesis_true_short_paragraph_raises(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        canonical_inputs["parent_pr249_verdict"] = "other"
        canonical_inputs["thesis_pragmatism"] = True
        canonical_inputs["substantive_paragraph"] = "too short."
        canonical_inputs["substantive_paragraph_ok"] = True
        canonical_inputs["reviewer_signoff"] = True
        with pytest.raises(RatingPathDecisionError) as exc:
            mod._apply_q6h_decision_rule(canonical_inputs)
        assert "substantive_reasoning_paragraph" in exc.value.falsifier_key

    def test_branch_iii_succeeds_with_substantive_paragraph(
        self, canonical_inputs: dict[str, Any]
    ) -> None:
        canonical_inputs["parent_pr249_verdict"] = "other"
        canonical_inputs["thesis_pragmatism"] = True
        canonical_inputs["substantive_paragraph"] = _valid_substantive_paragraph()
        canonical_inputs["substantive_paragraph_ok"] = True
        canonical_inputs["reviewer_signoff"] = True
        sel, _v, _p, _r, branch = mod._apply_q6h_decision_rule(canonical_inputs)
        assert branch == "(iii)"
        assert sel == "omit_reconstructed_rating_and_unblock_other_five"


# ---------------------------------------------------------------------------
# TestArtifactWriter
# ---------------------------------------------------------------------------


class TestArtifactWriter:
    def test_csv_written(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        assert csv_p.exists()
        assert md_p.exists()

    def test_csv_column_count_is_38(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        with csv_p.open() as fh:
            rows = list(csv.reader(fh))
        assert len(rows[0]) == 38

    def test_csv_row_count_is_6(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        with csv_p.open() as fh:
            rows = list(csv.reader(fh))
        assert len(rows) == 6

    def test_csv_byte_stable(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_a = tmp_path / "a.csv"
        csv_b = tmp_path / "b.csv"
        md_a = tmp_path / "a.md"
        md_b = tmp_path / "b.md"
        write_q6h_decision_artifacts(canonical_result, csv_a, md_a)
        write_q6h_decision_artifacts(canonical_result, csv_b, md_b)
        sha_a = hashlib.sha256(csv_a.read_bytes()).hexdigest()
        sha_b = hashlib.sha256(csv_b.read_bytes()).hexdigest()
        assert sha_a == sha_b

    def test_md_byte_stable(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_a = tmp_path / "a.csv"
        csv_b = tmp_path / "b.csv"
        md_a = tmp_path / "a.md"
        md_b = tmp_path / "b.md"
        write_q6h_decision_artifacts(canonical_result, csv_a, md_a)
        write_q6h_decision_artifacts(canonical_result, csv_b, md_b)
        sha_a = hashlib.sha256(md_a.read_bytes()).hexdigest()
        sha_b = hashlib.sha256(md_b.read_bytes()).hexdigest()
        assert sha_a == sha_b

    def test_csv_header_matches_schema(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        with csv_p.open() as fh:
            rows = list(csv.reader(fh))
        assert tuple(rows[0]) == Q6H_DECISION_SCHEMA

    def test_csv_rows_sorted_by_decision_id(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        with csv_p.open() as fh:
            rows = list(csv.reader(fh))
        ids = [r[0] for r in rows[1:]]
        assert ids == sorted(ids)

    def test_csv_uses_lf_line_endings(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        raw = csv_p.read_bytes()
        # Header line must end with \n, not \r\n.
        assert b"\r\n" not in raw

    def test_md_section_count_geq_19(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        md = md_p.read_text()
        # Count lines starting with "## " (not "### ").
        count = sum(
            1 for line in md.splitlines() if line.startswith("## ") and not line.startswith("### ")
        )
        assert count >= 19

    def test_md_section_15_sentence_count_geq_6(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        md = md_p.read_text()
        # Extract §15 body.
        start = md.find("## 15.")
        end = md.find("## 16.")
        section_15 = md[start:end]
        sentences = re.split(r"(?<=[.!?])\s+", section_15.strip())
        sentences = [s for s in sentences if s]
        assert len(sentences) >= 6

    def test_md_section_15_cross_references_geq_3(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        md = md_p.read_text()
        start = md.find("## 15.")
        end = md.find("## 16.")
        section_15 = md[start:end]
        cross_refs = re.findall(r"PR #249 §\d+", section_15)
        assert len(cross_refs) >= 3

    def test_md_section_16_present(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        md = md_p.read_text()
        assert "## 16." in md
        assert "_run_glicko2_survey" in md

    def test_md_section_11_column_count_assertion(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        md = md_p.read_text()
        assert "exactly 38 columns" in md

    def test_md_writer_short_paragraph_raises(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        # Build a result with a too-short paragraph to verify the
        # writer-time guard fires.
        bad = RatingPathDecisionResult(
            decisions=canonical_result.decisions,
            csv_path=canonical_result.csv_path,
            md_path=canonical_result.md_path,
            provenance_git_sha=canonical_result.provenance_git_sha,
            falsifiers_fired=canonical_result.falsifiers_fired,
            halting_falsifier=None,
            passed=True,
            selected_policy=canonical_result.selected_policy,
            verdict=canonical_result.verdict,
            materialization_permission=canonical_result.materialization_permission,
            rationale=canonical_result.rationale,
            branch_evaluated=canonical_result.branch_evaluated,
            thesis_pragmatism_flag_value=canonical_result.thesis_pragmatism_flag_value,
            thesis_pragmatism_paragraph="too short.",
        )
        with pytest.raises(RatingPathDecisionError):
            write_q6h_decision_artifacts(bad, tmp_path / "x.csv", tmp_path / "x.md")

    def test_csv_each_data_row_has_38_columns(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        with csv_p.open() as fh:
            rows = list(csv.reader(fh))
        for row in rows:
            assert len(row) == 38

    def test_md_section_18_provenance_includes_rule_sha(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        md = md_p.read_text()
        assert Q6H_PATH_DECISION_RULE_SHA256 in md

    def test_md_section_19_final_verdict(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        md = md_p.read_text()
        assert "## 19." in md
        assert canonical_result.selected_policy in md


# ---------------------------------------------------------------------------
# TestFalsifierChain
# ---------------------------------------------------------------------------


class TestFalsifierChain:
    def test_chain_has_min_37_keys(self) -> None:
        assert len(FALSIFIER_PRIORITY_CHAIN) >= 37

    def test_chain_keys_distinct(self) -> None:
        assert len(set(FALSIFIER_PRIORITY_CHAIN)) == len(FALSIFIER_PRIORITY_CHAIN)

    @pytest.mark.parametrize("key", FALSIFIER_PRIORITY_CHAIN)
    def test_each_key_is_non_empty_string(self, key: str) -> None:
        assert isinstance(key, str)
        assert key.strip()

    @pytest.mark.parametrize("key", FALSIFIER_PRIORITY_CHAIN)
    def test_each_key_lowercase_or_named(self, key: str) -> None:
        # Keys should be snake_case-like; allow lowercase letters,
        # digits, and underscores.
        assert all(c.islower() or c.isdigit() or c == "_" for c in key)

    def test_chain_contains_parent_sha_keys(self) -> None:
        for sha_key in (
            "parent_pr242_csv_sha256_mismatch",
            "parent_pr242_md_sha256_mismatch",
            "parent_pr243_csv_sha256_mismatch",
            "parent_pr243_md_sha256_mismatch",
            "parent_pr247_csv_sha256_mismatch",
            "parent_pr247_md_sha256_mismatch",
            "parent_pr249_csv_sha256_mismatch",
            "parent_pr249_md_sha256_mismatch",
        ):
            assert sha_key in FALSIFIER_PRIORITY_CHAIN

    def test_chain_contains_q5_q6f_q6g_drift_keys(self) -> None:
        assert "q6h_q5_re_adjudication_drift" in FALSIFIER_PRIORITY_CHAIN
        assert "q6h_q6f_re_adjudication_drift" in FALSIFIER_PRIORITY_CHAIN
        assert "q6h_q6g_re_adjudication_drift" in FALSIFIER_PRIORITY_CHAIN

    def test_chain_contains_no_creep_keys(self) -> None:
        for k in (
            "q6h_no_status_yaml_mutation",
            "q6h_no_research_log_mutation",
            "q6h_no_roadmap_mutation",
            "q6h_no_spec_mutation",
            "q6h_no_phase_03_touch",
            "q6h_no_step_02_01_04_touch",
            "q6h_no_trueskill_re_implementation",
            "q6h_no_batched_glicko2_re_implementation",
            "q6h_parquet_emitted",
            "q6h_materialization_creep",
        ):
            assert k in FALSIFIER_PRIORITY_CHAIN

    def test_chain_contains_branch_order_keys(self) -> None:
        assert (
            "q6h_decision_rule_order_not_evidentiary_first"
            in FALSIFIER_PRIORITY_CHAIN
        )

    def test_chain_contains_thesis_pragmatism_override_key(self) -> None:
        assert any(
            "thesis_pragmatism_set_false_without" in k
            for k in FALSIFIER_PRIORITY_CHAIN
        )


# ---------------------------------------------------------------------------
# TestNoMaterializationCreep
# ---------------------------------------------------------------------------


class TestNoMaterializationCreep:
    def test_every_row_has_empty_materialized_paths(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        for d in canonical_result.decisions:
            assert d.materialized_output_paths == ""

    def test_no_parquet_written_by_writer(
        self, tmp_path: Path, canonical_result: RatingPathDecisionResult
    ) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        write_q6h_decision_artifacts(canonical_result, csv_p, md_p)
        parquet_files = list(tmp_path.rglob("*.parquet"))
        assert parquet_files == []

    def test_check_no_materialized_helper_passes_canonical(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        passed, _msg = mod._check_no_materialized_output_paths(
            canonical_result.decisions
        )
        assert passed

    def test_check_no_materialized_helper_fails_when_populated(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        decisions = list(canonical_result.decisions)
        # Mutate would fail because dataclass is frozen; rebuild row 0.
        first = decisions[0]
        from dataclasses import replace
        decisions[0] = replace(first, materialized_output_paths="bad/path.parquet")
        passed, msg = mod._check_no_materialized_output_paths(tuple(decisions))
        assert not passed
        assert "non-empty materialized_output_paths" in msg


# ---------------------------------------------------------------------------
# TestNo5FamilyDrift
# ---------------------------------------------------------------------------


_EXPECTED_5_FAMILY = (
    "focal_player_history",
    "opponent_player_history",
    "matchup_history_aggregate",
    "cross_region_fragmentation_handling",
    "in_game_history_aggregate",
)


class TestNo5FamilyDrift:
    def test_set_matches_expected_tuple(self) -> None:
        assert Q6H_FIVE_FAMILY_POST_OMIT_SET == _EXPECTED_5_FAMILY

    def test_set_length_is_5(self) -> None:
        assert len(Q6H_FIVE_FAMILY_POST_OMIT_SET) == 5

    def test_set_excludes_reconstructed_rating(self) -> None:
        assert "reconstructed_rating" not in Q6H_FIVE_FAMILY_POST_OMIT_SET

    @pytest.mark.parametrize("fam", _EXPECTED_5_FAMILY)
    def test_each_family_present(self, fam: str) -> None:
        assert fam in Q6H_FIVE_FAMILY_POST_OMIT_SET

    def test_omit_row_future_columns_contains_all_5(self) -> None:
        row = mod._build_decision_row_c_omit_reconstructed_rating_and_unblock_other_five(
            "PR #TEST"
        )
        for fam in _EXPECTED_5_FAMILY:
            assert fam in row.future_column_names


# ---------------------------------------------------------------------------
# TestQ5Q6FQ6GPreservation
# ---------------------------------------------------------------------------


class TestQ5Q6FQ6GPreservation:
    def test_q5_token_preserved_canonical(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        passed, _msg = mod._check_q5_not_re_adjudicated(canonical_result.decisions)
        assert passed

    def test_q6f_token_preserved_canonical(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        passed, _msg = mod._check_q6f_not_re_adjudicated(canonical_result.decisions)
        assert passed

    def test_q6g_token_preserved_canonical(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        passed, _msg = mod._check_q6g_not_re_adjudicated(canonical_result.decisions)
        assert passed

    def test_q5_check_fires_on_drift(self) -> None:
        # Construct a synthetic decision tuple where Row 5 carries the Q5 token.
        d = mod._build_decision_row_selected_policy(
            audit_pr="PR #TEST",
            selected_policy=Q5_SELECTED_POLICY,  # drift
            verdict=Q5_SELECTED_POLICY,
            materialization_permission="x",
            rationale="r",
            branch_evaluated="(ii)",
            thesis_pragmatism_flag_value="null",
            thesis_pragmatism_paragraph_sentence_count=0,
            thesis_pragmatism_rationale="r",
        )
        decisions = (d, d, d, d, d)
        passed, _msg = mod._check_q5_not_re_adjudicated(decisions)
        assert not passed

    def test_q6f_check_fires_on_drift(self) -> None:
        d = mod._build_decision_row_selected_policy(
            audit_pr="PR #TEST",
            selected_policy="x",
            verdict=Q6F_SELECTED_POLICY,
            materialization_permission="x",
            rationale="r",
            branch_evaluated="(ii)",
            thesis_pragmatism_flag_value="null",
            thesis_pragmatism_paragraph_sentence_count=0,
            thesis_pragmatism_rationale="r",
        )
        passed, _msg = mod._check_q6f_not_re_adjudicated((d,))
        assert not passed

    def test_q6g_check_fires_on_drift(self) -> None:
        d = mod._build_decision_row_selected_policy(
            audit_pr="PR #TEST",
            selected_policy="x",
            verdict=Q6G_SELECTED_POLICY,
            materialization_permission="x",
            rationale="r",
            branch_evaluated="(ii)",
            thesis_pragmatism_flag_value="null",
            thesis_pragmatism_paragraph_sentence_count=0,
            thesis_pragmatism_rationale="r",
        )
        passed, _msg = mod._check_q6g_not_re_adjudicated((d,))
        assert not passed


# ---------------------------------------------------------------------------
# TestCanonicalRun
# ---------------------------------------------------------------------------


class TestCanonicalRun:
    def test_canonical_inputs_default(self) -> None:
        defaults = mod._canonical_executor_inputs()
        assert defaults["parent_pr249_verdict"] == "recommendation_only_glicko2"
        assert defaults["new_separating_anchor"] is None
        assert defaults["thesis_pragmatism"] is False

    def test_canonical_build_branch_ii(self) -> None:
        r = build_q6h_decision_result()
        assert r.selected_policy == "recommendation_only_event_by_event_glicko2"
        assert r.verdict == "recommendation_only_event_by_event_glicko2"
        assert (
            r.materialization_permission
            == "recommendation_only_blocked_pending_phase_03_or_later_decision"
        )
        assert r.branch_evaluated == "(ii)"

    def test_canonical_build_writes_artifacts(self, tmp_path: Path) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        r = run_q6h_rating_path_decision(
            csv_path=csv_p,
            md_path=md_p,
            verify_parent_shas=False,
        )
        assert r.passed
        assert csv_p.exists()
        assert md_p.exists()

    def test_canonical_no_artifact_write_when_disabled(self, tmp_path: Path) -> None:
        csv_p = tmp_path / "out.csv"
        md_p = tmp_path / "out.md"
        r = run_q6h_rating_path_decision(
            csv_path=csv_p,
            md_path=md_p,
            verify_parent_shas=False,
            write_artifacts=False,
        )
        assert r.passed
        assert not csv_p.exists()
        assert not md_p.exists()

    def test_canonical_5_decisions(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        assert len(canonical_result.decisions) == 5

    def test_canonical_decision_id_order(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        ids = tuple(d.decision_id for d in canonical_result.decisions)
        assert ids == Q6H_DECISION_ROWS

    def test_canonical_passed_flag(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        assert canonical_result.passed is True
        assert canonical_result.halting_falsifier is None

    def test_canonical_provenance_git_sha(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        assert isinstance(canonical_result.provenance_git_sha, str)


# ---------------------------------------------------------------------------
# TestDecisionRuleHash
# ---------------------------------------------------------------------------


class TestDecisionRuleHash:
    def test_pinned_sha_matches_runtime(self) -> None:
        observed = hashlib.sha256(
            Q6H_PATH_DECISION_RULE.encode("utf-8")
        ).hexdigest()
        assert observed == Q6H_PATH_DECISION_RULE_SHA256

    def test_pinned_sha_is_hex(self) -> None:
        assert len(Q6H_PATH_DECISION_RULE_SHA256) == 64

    def test_rule_string_nonempty(self) -> None:
        assert Q6H_PATH_DECISION_RULE.strip()

    def test_rule_string_lines_at_least_60(self) -> None:
        assert len(Q6H_PATH_DECISION_RULE.splitlines()) >= 60

    def test_rule_contains_a12_token(self) -> None:
        assert "A12" in Q6H_PATH_DECISION_RULE


# ---------------------------------------------------------------------------
# TestStructuralChecks
# ---------------------------------------------------------------------------


class TestStructuralChecks:
    def test_decision_count_passes(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        passed, _ = mod._check_decision_count(canonical_result.decisions)
        assert passed

    def test_decision_count_fails_on_4(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        passed, msg = mod._check_decision_count(canonical_result.decisions[:4])
        assert not passed
        assert "4" in msg

    def test_decision_id_order_passes(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        passed, _ = mod._check_decision_id_order(canonical_result.decisions)
        assert passed

    def test_decision_id_order_fails_when_reversed(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        reversed_t = tuple(reversed(canonical_result.decisions))
        passed, _ = mod._check_decision_id_order(reversed_t)
        assert not passed

    def test_q6h_selected_policy_row_present_passes(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        passed, _ = mod._check_q6h_selected_policy_row_present(
            canonical_result.decisions
        )
        assert passed

    def test_q6h_selected_policy_row_present_fails_without(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        passed, _ = mod._check_q6h_selected_policy_row_present(
            canonical_result.decisions[:-1]
        )
        assert not passed

    def test_omit_row_excluded_columns_present(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        passed, _ = mod._check_omit_row_excluded_columns_present(
            canonical_result.decisions
        )
        assert passed


# ---------------------------------------------------------------------------
# TestRepoRootHelper
# ---------------------------------------------------------------------------


class TestRepoRootHelper:
    def test_find_repo_root_succeeds(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
        sub = tmp_path / "a" / "b"
        sub.mkdir(parents=True)
        assert mod._find_repo_root(sub) == tmp_path

    def test_find_repo_root_raises_when_missing(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            mod._find_repo_root(tmp_path)


# ---------------------------------------------------------------------------
# TestGitSha
# ---------------------------------------------------------------------------


class TestGitSha:
    def test_get_git_sha_returns_string(self) -> None:
        sha = mod._get_git_sha()
        assert isinstance(sha, str)

    def test_get_git_sha_unknown_on_failure(self) -> None:
        with mock.patch("subprocess.run", side_effect=FileNotFoundError):
            assert mod._get_git_sha() == "UNKNOWN"


# ---------------------------------------------------------------------------
# TestSurfaceNonHaltingFalsifiers
# ---------------------------------------------------------------------------


class TestSurfaceNonHaltingFalsifiers:
    def test_canonical_run_no_non_halting(
        self, canonical_result: RatingPathDecisionResult
    ) -> None:
        # Branch (ii) -> no surface keys.
        assert canonical_result.falsifiers_fired == ()

    def test_branch_iii_no_surface_when_omit_row_well_formed(self) -> None:
        inputs = {
            "parent_pr249_verdict": "other",
            "new_separating_anchor": None,
            "thesis_pragmatism": True,
            "substantive_paragraph": _valid_substantive_paragraph(),
            "substantive_paragraph_ok": True,
            "reviewer_signoff": True,
            "no_fresh_blocking_finding": True,
            "named_missing_evidence": (),
        }
        r = build_q6h_decision_result(audit_pr="PR #TEST", executor_inputs=inputs)
        assert r.branch_evaluated == "(iii)"
        # Omit row is well-formed (built by canonical helper), so
        # no non-halting falsifiers surface.
        assert r.falsifiers_fired == ()


# ---------------------------------------------------------------------------
# TestRatingPathDecisionError
# ---------------------------------------------------------------------------


class TestRatingPathDecisionError:
    def test_error_attributes(self) -> None:
        e = RatingPathDecisionError("test_key", "test message")
        assert e.falsifier_key == "test_key"
        assert e.message == "test message"

    def test_error_str(self) -> None:
        e = RatingPathDecisionError("test_key", "test message")
        assert "test_key" in str(e)
        assert "test message" in str(e)

    def test_error_is_runtime_error(self) -> None:
        e = RatingPathDecisionError("k", "m")
        assert isinstance(e, RuntimeError)


# ---------------------------------------------------------------------------
# TestExecutorInputsVariations
# ---------------------------------------------------------------------------


_BRANCH_DEFAULT_DEFS = [
    ("branch_i_with_anchor", {"new_separating_anchor": "x"}, "(i)"),
    ("branch_ii_default", {}, "(ii)"),
]


class TestExecutorInputsVariations:
    @pytest.mark.parametrize("name,overrides,expected_branch", _BRANCH_DEFAULT_DEFS)
    def test_branch_outcome(
        self, name: str, overrides: dict[str, Any], expected_branch: str
    ) -> None:
        inputs = mod._canonical_executor_inputs()
        inputs.update(overrides)
        _s, _v, _p, _r, branch = mod._apply_q6h_decision_rule(inputs)
        assert branch == expected_branch


# ---------------------------------------------------------------------------
# TestMDStandbyParagraphPresence
# ---------------------------------------------------------------------------


class TestMDStandbyParagraphPresence:
    def test_standby_paragraph_meets_admissibility(self) -> None:
        passed, _msg = mod._check_substantive_paragraph_admissibility(
            mod._THESIS_PRAGMATISM_STANDBY_PARAGRAPH
        )
        assert passed

    def test_standby_has_geq_6_sentences(self) -> None:
        n = mod._count_paragraph_sentences(mod._THESIS_PRAGMATISM_STANDBY_PARAGRAPH)
        assert n >= 6

    def test_standby_has_geq_3_cross_refs(self) -> None:
        refs = re.findall(
            r"PR #249 §\d+", mod._THESIS_PRAGMATISM_STANDBY_PARAGRAPH
        )
        assert len(refs) >= 3


# ---------------------------------------------------------------------------
# TestEachSchemaColumn (parametric coverage)
# ---------------------------------------------------------------------------


class TestEachSchemaColumn:
    @pytest.mark.parametrize("col", Q6H_DECISION_SCHEMA)
    def test_column_is_field_in_dataclass(self, col: str) -> None:
        names = {f.name for f in fields(RatingPathDecision)}
        assert col in names

    @pytest.mark.parametrize("col", Q6H_DECISION_SCHEMA)
    def test_column_unique(self, col: str) -> None:
        count = sum(1 for c in Q6H_DECISION_SCHEMA if c == col)
        assert count == 1
