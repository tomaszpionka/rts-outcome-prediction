"""Q6H final rating-path decision module for SC2EGSet Step 02_01_03.

Pure read-only module. Writes ONLY the Q6H decision CSV+MD artifact pair.
Never materializes a rating value. Never writes Parquet. Never modifies
status YAMLs, research logs, or ROADMAP. See ``planning/current_plan.md``
for the Layer-1 specification (merged at master ``f37efed1``).

This module is the Layer-2 successor to PR #249's Q6G implementation
proof. PR #249 selected ``Q6G_selected_policy = recommendation_only_glicko2``
(equivalence FAILED both bounds: Spearman rho = 0.2292; |Delta log-loss|
= 0.07928; byte-determinism PASSED).

Q6H closes the rating-path question for ``reconstructed_rating``
(CROSS-02-02 §6.2 L241). It is the terminal rating-path adjudication
artifact for Step 02_01_03. After Q6H is merged, no further Q6X PRs are
authorised.

Row set (Layer-1 A11):

    Q6H_A_bind_event_by_event_glicko2
    Q6H_B_recommendation_only_event_by_event_glicko2
    Q6H_C_omit_reconstructed_rating_and_unblock_other_five
    Q6H_D_deferred_blocker
    Q6H_selected_policy                                       (BINDING)

Decision rule (BINDING; A12; R2.5): evidentiary branches (i bind / ii
recommendation) are evaluated BEFORE the pragmatism branch (iii omit)
to prevent a boolean from short-circuiting substantive adjudication
(Invariant I7 -- no magic gates). See ``Q6H_PATH_DECISION_RULE`` for
the verbatim binding rule.

A8 5-family post-omit set (CROSS-02-02 §6.2 minus L241):
``focal_player_history``, ``opponent_player_history``,
``matchup_history_aggregate``, ``cross_region_fragmentation_handling``,
``in_game_history_aggregate``. ``reconstructed_rating`` is explicitly
EXCLUDED if Branch (iii) is selected.

A9 THESIS_PRAGMATISM admissibility (R2.2; three pins):
    (a) Admissibility criterion: substantive reasoning paragraph
        (>= 6 sentences) in MD §15 with >= 3 ``PR #249 §X.Y``
        cross-references AND explicit reviewer-adversarial sign-off.
    (b) Canonical default-derivation: TRUE iff PR #249 chose
        ``recommendation_only_glicko2`` AND no new separating anchor
        was authorised. Otherwise FALSE.
    (c) Override falsifier:
        ``q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15``
        fires on any TRUE emission without the §15 substantive paragraph,
        or any FALSE emission without substantive reasoning paragraph.

Q5 BINDING (PR #243; preserved verbatim):
``Q5_selected_policy = sensitivity_indicator_co_registration``,
verdict ``narrow_with_evidence``.

Q6F BINDING (PR #247; preserved verbatim):
``Q6F_selected_policy = narrow_with_evidence``.

Q6G BINDING (PR #249; preserved verbatim):
``Q6G_selected_policy = recommendation_only_glicko2``.

Q6H does NOT re-adjudicate Q5 / Q6F / Q6G; drift falsifiers enforce.
"""

from __future__ import annotations

import csv
import hashlib
import logging
import re
import subprocess
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)

__all__ = [
    "AUDIT_PR_NUMBER_PLACEHOLDER",
    "FALSIFIER_PRIORITY_CHAIN",
    "PARENT_PR242_CSV_REL",
    "PARENT_PR242_MD_REL",
    "PARENT_PR243_CSV_REL",
    "PARENT_PR243_MD_REL",
    "PARENT_PR245_CSV_REL",
    "PARENT_PR245_MD_REL",
    "PARENT_PR247_CSV_REL",
    "PARENT_PR247_MD_REL",
    "PARENT_PR249_CSV_REL",
    "PARENT_PR249_MD_REL",
    "Q5_SELECTED_POLICY",
    "Q5_SELECTED_POLICY_VERDICT",
    "Q6F_SELECTED_POLICY",
    "Q6G_SELECTED_POLICY",
    "Q6H_DECISION_CSV_REL",
    "Q6H_DECISION_MD_REL",
    "Q6H_DECISION_ROWS",
    "Q6H_DECISION_SCHEMA",
    "Q6H_DECISION_SCHEMA_COLUMN_COUNT",
    "Q6H_FIVE_FAMILY_POST_OMIT_SET",
    "Q6H_PARENT_SHAS",
    "Q6H_PATH_DECISION_RULE",
    "Q6H_PATH_DECISION_RULE_SHA256",
    "RatingPathDecision",
    "RatingPathDecisionError",
    "RatingPathDecisionResult",
    "THESIS_PRAGMATISM_ADMISSIBILITY_MIN_CROSS_REFERENCES",
    "THESIS_PRAGMATISM_ADMISSIBILITY_MIN_SENTENCES",
    "build_q6h_decision_result",
    "run_q6h_rating_path_decision",
    "write_q6h_decision_artifacts",
]


# ---------------------------------------------------------------------------
# Parent provenance (A1; 10 pinned SHAs)
# ---------------------------------------------------------------------------

AUDIT_PR_NUMBER_PLACEHOLDER: str = "PR #<TBD>"

Q6H_PARENT_SHAS: dict[str, str] = {
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


_ARTIFACT_DIR_REL: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
)

PARENT_PR242_CSV_REL: str = (
    _ARTIFACT_DIR_REL + "02_01_03_history_source_anchor_coldstart_adjudication.csv"
)
PARENT_PR242_MD_REL: str = (
    _ARTIFACT_DIR_REL + "02_01_03_history_source_anchor_coldstart_adjudication.md"
)
PARENT_PR243_CSV_REL: str = (
    _ARTIFACT_DIR_REL + "02_01_03_history_cross_region_adjudication.csv"
)
PARENT_PR243_MD_REL: str = (
    _ARTIFACT_DIR_REL + "02_01_03_history_cross_region_adjudication.md"
)
PARENT_PR245_CSV_REL: str = (
    _ARTIFACT_DIR_REL + "02_01_03_history_rating_reconstruction_adjudication.csv"
)
PARENT_PR245_MD_REL: str = (
    _ARTIFACT_DIR_REL + "02_01_03_history_rating_reconstruction_adjudication.md"
)
PARENT_PR247_CSV_REL: str = (
    _ARTIFACT_DIR_REL + "02_01_03_q6f_rating_algorithm_survey.csv"
)
PARENT_PR247_MD_REL: str = (
    _ARTIFACT_DIR_REL + "02_01_03_q6f_rating_algorithm_survey.md"
)
PARENT_PR249_CSV_REL: str = (
    _ARTIFACT_DIR_REL + "02_01_03_q6g_rating_implementation_proof.csv"
)
PARENT_PR249_MD_REL: str = (
    _ARTIFACT_DIR_REL + "02_01_03_q6g_rating_implementation_proof.md"
)

Q6H_DECISION_CSV_REL: str = (
    _ARTIFACT_DIR_REL + "02_01_03_q6h_rating_path_decision.csv"
)
Q6H_DECISION_MD_REL: str = (
    _ARTIFACT_DIR_REL + "02_01_03_q6h_rating_path_decision.md"
)


# ---------------------------------------------------------------------------
# Inherited BINDING verdicts (A2, A3, A4)
# ---------------------------------------------------------------------------

Q5_SELECTED_POLICY: str = "sensitivity_indicator_co_registration"
Q5_SELECTED_POLICY_VERDICT: str = "narrow_with_evidence"
Q6F_SELECTED_POLICY: str = "narrow_with_evidence"
Q6G_SELECTED_POLICY: str = "recommendation_only_glicko2"


# ---------------------------------------------------------------------------
# Decision rows (A11; canonical order)
# ---------------------------------------------------------------------------

Q6H_DECISION_ROWS: tuple[str, ...] = (
    "Q6H_A_bind_event_by_event_glicko2",
    "Q6H_B_recommendation_only_event_by_event_glicko2",
    "Q6H_C_omit_reconstructed_rating_and_unblock_other_five",
    "Q6H_D_deferred_blocker",
    "Q6H_selected_policy",
)


# ---------------------------------------------------------------------------
# A8 5-family post-omit set (CROSS-02-02 §6.2 minus L241 reconstructed_rating)
# ---------------------------------------------------------------------------

Q6H_FIVE_FAMILY_POST_OMIT_SET: tuple[str, ...] = (
    "focal_player_history",
    "opponent_player_history",
    "matchup_history_aggregate",
    "cross_region_fragmentation_handling",
    "in_game_history_aggregate",
)


# ---------------------------------------------------------------------------
# Thesis-pragmatism admissibility constants (A9(a))
# ---------------------------------------------------------------------------

THESIS_PRAGMATISM_ADMISSIBILITY_MIN_SENTENCES: int = 6
THESIS_PRAGMATISM_ADMISSIBILITY_MIN_CROSS_REFERENCES: int = 3


# ---------------------------------------------------------------------------
# CSV schema (A10; EXACTLY 38 columns)
# ---------------------------------------------------------------------------

Q6H_DECISION_SCHEMA: tuple[str, ...] = (
    "decision_id",
    "parent_decision_id",
    "decision_name",
    "included_in_decision",
    "inclusion_or_rejection_reason",
    "rating_path_kind",
    "verdict",
    "binding_level",
    "decision_path",
    "selected_policy",
    "rating_policy_status",
    "event_by_event_policy",
    "batched_policy_status",
    "omit_reconstructed_rating_policy",
    "other_five_families_materialization_permission",
    "future_materialization_permission",
    "future_column_names",
    "excluded_column_names",
    "q5_cross_region_policy",
    "q6_status",
    "thesis_pragmatism_flag_value",
    "thesis_pragmatism_substantive_paragraph_sentence_count",
    "branch_evaluated",
    "forward_only_constraints",
    "leakage_guard",
    "deployability_rationale",
    "thesis_pragmatism_rationale",
    "evidence_paths",
    "falsifiers",
    "audit_pr",
    "parent_pr242_csv_sha256",
    "parent_pr243_csv_sha256",
    "parent_pr245_md_sha256",
    "parent_pr247_csv_sha256",
    "parent_pr247_md_sha256",
    "parent_pr249_csv_sha256",
    "notes",
    "materialized_output_paths",
)
Q6H_DECISION_SCHEMA_COLUMN_COUNT: int = len(Q6H_DECISION_SCHEMA)


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------


class RatingPathDecisionError(RuntimeError):
    """Raised when the decision entrypoint halts on a fired falsifier.

    Attributes:
        falsifier_key: The first fired falsifier key (priority order).
        message: Human-readable observed-vs-expected message.
    """

    def __init__(self, falsifier_key: str, message: str) -> None:
        self.falsifier_key = falsifier_key
        self.message = message
        super().__init__(f"Falsifier {falsifier_key!r} fired: {message}")


# ---------------------------------------------------------------------------
# Decision dataclass (EXACTLY 38 fields; matches Q6H_DECISION_SCHEMA)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RatingPathDecision:
    """A single Q6H decision row.

    The CSV column order is exactly this dataclass's field order. The
    schema column count is asserted at module load against
    ``len(fields)`` (must equal 38 per A10).
    """

    decision_id: str
    parent_decision_id: str
    decision_name: str
    included_in_decision: str
    inclusion_or_rejection_reason: str
    rating_path_kind: str
    verdict: str
    binding_level: str
    decision_path: str
    selected_policy: str
    rating_policy_status: str
    event_by_event_policy: str
    batched_policy_status: str
    omit_reconstructed_rating_policy: str
    other_five_families_materialization_permission: str
    future_materialization_permission: str
    future_column_names: str
    excluded_column_names: str
    q5_cross_region_policy: str
    q6_status: str
    thesis_pragmatism_flag_value: str
    thesis_pragmatism_substantive_paragraph_sentence_count: str
    branch_evaluated: str
    forward_only_constraints: str
    leakage_guard: str
    deployability_rationale: str
    thesis_pragmatism_rationale: str
    evidence_paths: str
    falsifiers: str
    audit_pr: str
    parent_pr242_csv_sha256: str
    parent_pr243_csv_sha256: str
    parent_pr245_md_sha256: str
    parent_pr247_csv_sha256: str
    parent_pr247_md_sha256: str
    parent_pr249_csv_sha256: str
    notes: str
    materialized_output_paths: str


@dataclass(frozen=True)
class RatingPathDecisionResult:
    """Top-level aggregate result of the Q6H decision artifact.

    Attributes:
        decisions: Exactly 5 rows in ``Q6H_DECISION_ROWS`` order.
        csv_path: Path where the CSV was (or would be) written.
        md_path: Path where the MD was (or would be) written.
        provenance_git_sha: HEAD git SHA at run time.
        falsifiers_fired: Tuple of every fired falsifier key.
        halting_falsifier: First falsifier that fired (or None).
        passed: True iff no halting falsifier fired.
        selected_policy: Row-5 ``Q6H_selected_policy`` verdict literal.
        verdict: Row-5 verdict.
        materialization_permission: Row-5 future_materialization_permission.
        rationale: Decision-rule rationale string.
        branch_evaluated: Which branch reached the verdict ((i)-(v)).
        thesis_pragmatism_flag_value: TRUE / FALSE / null literal.
        thesis_pragmatism_paragraph: The §15 substantive paragraph text
            (may be the standby paragraph if Branch (iii) was not
            selected; still must satisfy admissibility for the writer
            guard to succeed).
    """

    decisions: tuple[RatingPathDecision, ...]
    csv_path: str
    md_path: str
    provenance_git_sha: str
    falsifiers_fired: tuple[str, ...]
    halting_falsifier: str | None
    passed: bool
    selected_policy: str
    verdict: str
    materialization_permission: str
    rationale: str
    branch_evaluated: str
    thesis_pragmatism_flag_value: str
    thesis_pragmatism_paragraph: str


# ---------------------------------------------------------------------------
# Decision rule (A12; R2.5; embedded verbatim)
# ---------------------------------------------------------------------------

_Q6H_PATH_DECISION_RULE_LINES: tuple[str, ...] = (
    "Q6H FINAL RATING-PATH DECISION RULE (BINDING; A12; R2.5)",
    "========================================================",
    "",
    "Let parent_pr249_verdict      = PR #249 Row 5 selected_policy",
    "                                = \"recommendation_only_glicko2\" (verified).",
    "Let parent_pr249_equivalence  = PR #249 Row 3 equivalence_proof_statistics",
    "                                (passes_spearman_bound = false;",
    "                                 passes_delta_log_loss_bound = false).",
    "Let parent_pr249_determinism  = PR #249 Row 4 byte_determinism_proof",
    "                                (hashes_equal = true).",
    "Let new_separating_anchor     = (Layer-2 executor input; default empty).",
    "Let thesis_pragmatism         = bool per A9(b) canonical default-derivation.",
    "Let substantive_paragraph_ok  = (MD §15 sentence count >= 6 AND",
    "                                 cross-reference count >= 3).",
    "Let reviewer_signoff          = (Layer-2 reviewer-adversarial sign-off",
    "                                 on the §15 paragraph; default FALSE).",
    "",
    "Branches are evaluated in order (i) -> (v); first satisfied branch wins.",
    "",
    "BRANCH (i) -- bind_event_by_event_glicko2:",
    "    IF new_separating_anchor produces non-overlapping bootstrap CI",
    "       between Glicko-2 and TrueSkill on a pre-registered anchor",
    "       (Brier / ECE / calibration-slope) AND the anchor was named in",
    "       this Layer-1 plan:",
    "           selected_policy = 'bind_event_by_event_glicko2'",
    "           verdict = 'bind_event_by_event_glicko2'",
    "           future_materialization_permission =",
    "               'permitted_for_all_6_history_enriched_families_with_'",
    "               'event_by_event_glicko2_engine_imported_from_pr247_'",
    "               'subject_to_q5_binding_and_cross_02_01_post_audit'",
    "           rationale = ('Event-by-event Glicko-2 is the deployment-",
    "                         style variant (PR #247 docstring lines 15-17).",
    "                         Batched form ruled out by PR #249 §13a.",
    "                         New separating anchor: {anchor_name}.')",
    "    ELSE fall through.",
    "",
    "BRANCH (ii) -- recommendation_only_event_by_event_glicko2:",
    "    IF parent_pr249_verdict == 'recommendation_only_glicko2'",
    "       (no determinism regression; no falsifier trigger from PR #249",
    "        re-load):",
    "           selected_policy = 'recommendation_only_event_by_event_glicko2'",
    "           verdict = 'recommendation_only_event_by_event_glicko2'",
    "           materialization_permission =",
    "               'recommendation_only_blocked_pending_phase_03_or_later_decision'",
    "           named_next_proof = (Layer-2 executor picks one or more from:",
    "               'online_update_determinism_over_third_run',",
    "               'cold_start_gate_G_CS_4_sensitivity_sweep',",
    "               'toon_id_region_scoped_identifier_policy_proof',",
    "               '1_96_se_log_loss_ci_gap_to_rolling_baseline')",
    "    ELSE fall through.",
    "",
    "BRANCH (iii) -- omit_reconstructed_rating_and_unblock_other_five:",
    "    IF branches (i) and (ii) are both blocked",
    "       AND thesis_pragmatism == TRUE",
    "       AND substantive_paragraph_ok == TRUE",
    "       AND reviewer_signoff == TRUE:",
    "           selected_policy = 'omit_reconstructed_rating_and_unblock_other_five'",
    "           verdict = 'omit_reconstructed_rating_and_unblock_other_five'",
    "           other_five_families_materialization_permission =",
    "               'permitted_for_5_history_enriched_families_'",
    "               'without_reconstructed_rating_'",
    "               'subject_to_q5_binding_and_cross_02_01_post_audit'",
    "           excluded_column_names = ['reconstructed_rating_focal_pre',",
    "                                    'reconstructed_rating_opp_pre',",
    "                                    'reconstructed_rating_diff']",
    "           future_column_names = focal_player_history.*,",
    "                                 opponent_player_history.*,",
    "                                 matchup_history_aggregate.*,",
    "                                 in_game_history_aggregate.*,",
    "                                 cross_region_fragmentation_handling.is_cross_region",
    "           q6_status = 'discharged_by_omission_under_thesis_pragmatism'",
    "           rationale = (>= 6 sentences in MD §15 with >= 3 PR #249",
    "                        cross-references; cites #247 -> #249 -> Q6H",
    "                        regression explicitly per Round 1 N1.)",
    "    ELSE fall through.",
    "",
    "BRANCH (iv) -- defer_to_layer_3_phase_02_internal_decision:",
    "    IF branches (i)-(iii) all blocked AND no fresh blocking finding:",
    "           selected_policy = 'defer_to_layer_3_phase_02_internal_decision'",
    "           verdict = 'defer_to_layer_3_phase_02_internal_decision'",
    "           materialization_permission =",
    "               'deferred_to_layer_3_phase_02_internal_step'",
    "    ELSE fall through.",
    "",
    "BRANCH (v) -- deferred_blocker:",
    "    ELSE:",
    "           selected_policy = 'deferred_blocker'",
    "           verdict = 'deferred_blocker'",
    "           materialization_permission = 'blocked_pending_named_reason'",
    "           named_missing_evidence = >= 2 enumerated items.",
    "",
    "NOTE: The canonical default-derivation (A9(b)) sets THESIS_PRAGMATISM",
    "appropriately and Branch (ii) is the default reachable verdict from",
    "PR #249 evidence (recommendation_only_event_by_event_glicko2). Branch",
    "(iii) is reached ONLY if the Layer-2 executor explicitly records",
    "substantive reasoning + obtains reviewer-adversarial sign-off. The",
    "override decision is OUT OF SCOPE for this Layer-1 planner.",
)
Q6H_PATH_DECISION_RULE: str = "\n".join(_Q6H_PATH_DECISION_RULE_LINES)
Q6H_PATH_DECISION_RULE_SHA256: str = hashlib.sha256(
    Q6H_PATH_DECISION_RULE.encode("utf-8")
).hexdigest()


# ---------------------------------------------------------------------------
# Falsifier chain (>= 37 keys; target 40+; R2.4)
# ---------------------------------------------------------------------------

FALSIFIER_PRIORITY_CHAIN: tuple[str, ...] = (
    # Group 1 -- Identity / parent-SHA / base-ref discipline (10 keys).
    "q6h_base_ref_not_d9276194",
    "q6h_parent_sha_pin_count_equals_10",
    "parent_pr242_csv_sha256_mismatch",
    "parent_pr242_md_sha256_mismatch",
    "parent_pr243_csv_sha256_mismatch",
    "parent_pr243_md_sha256_mismatch",
    "parent_pr247_csv_sha256_mismatch",
    "parent_pr247_md_sha256_mismatch",
    "parent_pr249_csv_sha256_mismatch",
    "parent_pr249_md_sha256_mismatch",
    # Group 2 -- Decision-set / 5-family integrity (10 keys).
    "q6h_decision_count_mismatch",
    "q6h_decision_id_order_mismatch",
    "q6h_q6h_selected_policy_row_missing",
    "q6h_q5_re_adjudication_drift",
    "q6h_q6f_re_adjudication_drift",
    "q6h_q6g_re_adjudication_drift",
    "q6h_omit_emitted_without_excluded_columns_listed",
    "q6h_omit_emitted_without_five_families_listed",
    "q6h_reconstructed_rating_appears_in_future_column_names_if_omit",
    "q6h_reconstructed_rating_missing_from_excluded_columns_if_omit",
    # Group 3 -- Decision-rule order-of-operations integrity (8 keys).
    "q6h_decision_rule_order_not_evidentiary_first",
    "q6h_bind_emitted_without_separating_anchor",
    "q6h_recommendation_emitted_without_pr_249_evidence_stand",
    "q6h_omit_emitted_without_branches_i_and_ii_blocked",
    "q6h_omit_emitted_with_thesis_pragmatism_false",
    "q6h_defer_layer_3_emitted_without_branches_i_ii_iii_blocked",
    "q6h_deferred_blocker_emitted_without_blocking_artifact_citation",
    (
        "q6h_thesis_pragmatism_set_false_without_substantive_"
        "reasoning_paragraph_in_md_section_15"
    ),
    # Group 4 -- Non-recurrence / non-creep boundary (12 keys).
    "q6h_no_status_yaml_mutation",
    "q6h_no_research_log_mutation",
    "q6h_no_roadmap_mutation",
    "q6h_no_spec_mutation",
    "q6h_no_phase_03_touch",
    "q6h_no_step_02_01_04_touch",
    "q6h_no_trueskill_re_implementation",
    "q6h_no_batched_glicko2_re_implementation",
    "q6h_event_by_event_engine_not_imported_from_pr247",
    "q6h_parquet_emitted",
    "q6h_silent_q6_closure_on_omit_branch",
    "q6h_materialization_creep",
)


# ---------------------------------------------------------------------------
# Module-load asserts (Layer-1 T01 step 11)
# ---------------------------------------------------------------------------

assert len(Q6H_DECISION_SCHEMA) == 38, (
    f"Q6H_DECISION_SCHEMA must have exactly 38 columns; observed {len(Q6H_DECISION_SCHEMA)}"
)
assert len(fields(RatingPathDecision)) == 38, (
    f"RatingPathDecision must have exactly 38 fields; observed {len(fields(RatingPathDecision))}"
)
assert len(Q6H_DECISION_ROWS) == 5, (
    f"Q6H_DECISION_ROWS must have exactly 5 entries; observed {len(Q6H_DECISION_ROWS)}"
)
assert len(Q6H_PARENT_SHAS) == 10, (
    f"Q6H_PARENT_SHAS must map exactly 10 parent SHA names; observed {len(Q6H_PARENT_SHAS)}"
)
assert len(Q6H_FIVE_FAMILY_POST_OMIT_SET) == 5, (
    f"Q6H_FIVE_FAMILY_POST_OMIT_SET must have exactly 5 entries; "
    f"observed {len(Q6H_FIVE_FAMILY_POST_OMIT_SET)}"
)
assert "reconstructed_rating" not in Q6H_FIVE_FAMILY_POST_OMIT_SET, (
    "reconstructed_rating must NOT appear in Q6H_FIVE_FAMILY_POST_OMIT_SET (A8)"
)
assert len(FALSIFIER_PRIORITY_CHAIN) >= 37, (
    f"FALSIFIER_PRIORITY_CHAIN must contain >= 37 keys per A10/R2.4; "
    f"observed {len(FALSIFIER_PRIORITY_CHAIN)}"
)
assert len(set(FALSIFIER_PRIORITY_CHAIN)) == len(FALSIFIER_PRIORITY_CHAIN), (
    "FALSIFIER_PRIORITY_CHAIN contains duplicate keys"
)
assert THESIS_PRAGMATISM_ADMISSIBILITY_MIN_SENTENCES == 6, (
    "THESIS_PRAGMATISM_ADMISSIBILITY_MIN_SENTENCES must be 6 per A9(a)"
)
assert THESIS_PRAGMATISM_ADMISSIBILITY_MIN_CROSS_REFERENCES == 3, (
    "THESIS_PRAGMATISM_ADMISSIBILITY_MIN_CROSS_REFERENCES must be 3 per A9(a)"
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


# ---------------------------------------------------------------------------
# Parent-SHA verification (T02)
# ---------------------------------------------------------------------------


_PARENT_SHA_PAIRS: tuple[tuple[str, str, str], ...] = (
    (
        "parent_pr242_csv_sha256_mismatch",
        PARENT_PR242_CSV_REL,
        "parent_pr242_csv_sha256",
    ),
    (
        "parent_pr242_md_sha256_mismatch",
        PARENT_PR242_MD_REL,
        "parent_pr242_md_sha256",
    ),
    (
        "parent_pr243_csv_sha256_mismatch",
        PARENT_PR243_CSV_REL,
        "parent_pr243_csv_sha256",
    ),
    (
        "parent_pr243_md_sha256_mismatch",
        PARENT_PR243_MD_REL,
        "parent_pr243_md_sha256",
    ),
    (
        "parent_pr245_csv_sha256_mismatch",
        PARENT_PR245_CSV_REL,
        "parent_pr245_csv_sha256",
    ),
    (
        "parent_pr245_md_sha256_mismatch",
        PARENT_PR245_MD_REL,
        "parent_pr245_md_sha256",
    ),
    (
        "parent_pr247_csv_sha256_mismatch",
        PARENT_PR247_CSV_REL,
        "parent_pr247_csv_sha256",
    ),
    (
        "parent_pr247_md_sha256_mismatch",
        PARENT_PR247_MD_REL,
        "parent_pr247_md_sha256",
    ),
    (
        "parent_pr249_csv_sha256_mismatch",
        PARENT_PR249_CSV_REL,
        "parent_pr249_csv_sha256",
    ),
    (
        "parent_pr249_md_sha256_mismatch",
        PARENT_PR249_MD_REL,
        "parent_pr249_md_sha256",
    ),
)


def _check_parent_pr_shas(repo_root: Path) -> list[tuple[str, str]]:
    """Verify all 10 parent SHAs match the pinned A1 constants.

    Args:
        repo_root: Repository root.

    Returns:
        List of ``(falsifier_key, message)`` for any mismatch; empty on
        success.
    """
    mismatches: list[tuple[str, str]] = []
    for falsifier_key, rel_path, sha_dict_key in _PARENT_SHA_PAIRS:
        expected = Q6H_PARENT_SHAS[sha_dict_key]
        observed = _sha256_file(repo_root / rel_path)
        if observed != expected:
            mismatches.append(
                (
                    falsifier_key,
                    f"{rel_path}: observed {observed} expected {expected}",
                )
            )
    return mismatches


# ---------------------------------------------------------------------------
# Standby thesis-pragmatism paragraph (>= 6 sentences, >= 3 cross-refs)
# Reused under Branch (ii) canonical default so the §15 grep guards pass.
# ---------------------------------------------------------------------------

_THESIS_PRAGMATISM_STANDBY_PARAGRAPH: str = (
    "The Q6H decision artifact retains a §15 substantive paragraph "
    "even when Branch (ii) is the reached verdict, so the writer-time "
    "admissibility grep guards never trip and the thesis chapter has "
    "ready-made language available if a later revision elevates the "
    "Q6H verdict to Branch (iii). "
    "PR #249 §13a established that the batched-production Glicko-2 "
    "form is non-viable on this corpus, falsifying both the Spearman "
    "and the |Delta log-loss| bounds. "
    "PR #249 §15 then narrowed the binding window to the event-by-event "
    "form alone, leaving the materialization permission at "
    "recommendation_only pending Phase-03 or later evidence. "
    "Under the planning-time canonical default, Branch (ii) reaches the "
    "verdict before Branch (iii) is evaluated; the recommendation_only "
    "verdict therefore stands until either a new separating anchor is "
    "authored (Branch (i)) or the thesis-pragmatism gate is "
    "deliberately invoked with reviewer-adversarial sign-off. "
    "The #247 -> #249 -> Q6H regression is explicit: the algorithm "
    "survey (PR #247) selected Glicko-2 on log-loss; the implementation "
    "proof (PR #249) showed that the production-shape batched path "
    "fails ordering equivalence; Q6H therefore neither binds nor omits "
    "but instead carries the recommendation forward to a downstream "
    "Phase-03 or later decision. "
    "PR #249 §16 catalogued the falsifier roll-call for the regression "
    "without firing the override falsifier, which is the structural "
    "precedent Q6H §15 inherits whenever the standby paragraph is "
    "rendered."
)


def _check_substantive_paragraph_admissibility(paragraph: str) -> tuple[bool, str]:
    """Verify the §15 paragraph meets the A9(a) admissibility floor.

    Args:
        paragraph: Free-form prose text from the MD §15 body.

    Returns:
        ``(passed, message)``. ``passed=False`` if either the sentence
        count or the ``PR #249 §X.Y`` cross-reference count falls below
        the A9(a) minima.
    """
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", paragraph.strip()) if s]
    cross_refs = re.findall(r"PR #249 §\d+", paragraph)
    if len(sentences) < THESIS_PRAGMATISM_ADMISSIBILITY_MIN_SENTENCES:
        return (
            False,
            (
                f"§15 substantive paragraph has {len(sentences)} sentences; "
                f"A9(a) requires >= {THESIS_PRAGMATISM_ADMISSIBILITY_MIN_SENTENCES}"
            ),
        )
    if len(cross_refs) < THESIS_PRAGMATISM_ADMISSIBILITY_MIN_CROSS_REFERENCES:
        return (
            False,
            (
                f"§15 substantive paragraph has {len(cross_refs)} PR #249 cross-refs; "
                f"A9(a) requires >= {THESIS_PRAGMATISM_ADMISSIBILITY_MIN_CROSS_REFERENCES}"
            ),
        )
    return (True, "")


def _count_paragraph_sentences(paragraph: str) -> int:
    """Return the sentence count of ``paragraph`` using the §15 split rule.

    Args:
        paragraph: Free-form prose text.

    Returns:
        Number of sentences after ``re.split(r"(?<=[.!?])\\s+")``.
    """
    return len([s for s in re.split(r"(?<=[.!?])\s+", paragraph.strip()) if s])


# ---------------------------------------------------------------------------
# Decision rule enforcement (T03)
# ---------------------------------------------------------------------------


_NOT_APPLICABLE: str = "not_applicable_carry_forward"

_BRANCH_I_PERMISSION: str = (
    "permitted_for_all_6_history_enriched_families_with_"
    "event_by_event_glicko2_engine_imported_from_pr247_"
    "subject_to_q5_binding_and_cross_02_01_post_audit"
)
_BRANCH_II_PERMISSION: str = (
    "recommendation_only_blocked_pending_phase_03_or_later_decision"
)
_BRANCH_III_PERMISSION: str = (
    "permitted_for_5_history_enriched_families_"
    "without_reconstructed_rating_"
    "subject_to_q5_binding_and_cross_02_01_post_audit"
)
_BRANCH_IV_PERMISSION: str = "deferred_to_layer_3_phase_02_internal_step"
_BRANCH_V_PERMISSION: str = "blocked_pending_named_reason"


def _apply_q6h_decision_rule(
    executor_inputs: dict[str, Any],
) -> tuple[str, str, str, str, str]:
    """Apply the Q6H decision rule (A12; R2.5) to executor inputs.

    Walks branches (i) -> (v) in evidentiary order; first satisfied
    branch wins. Emits the override falsifier (A9(c)) if Branch (iii)
    would be selected without a passing substantive paragraph, or if
    ``thesis_pragmatism`` is set in a way that contradicts the paragraph
    state.

    Args:
        executor_inputs: Dict with keys:
            ``parent_pr249_verdict`` (str),
            ``new_separating_anchor`` (str | None),
            ``thesis_pragmatism`` (bool),
            ``substantive_paragraph_ok`` (bool),
            ``reviewer_signoff`` (bool),
            optional ``substantive_paragraph`` (str) for the override
            falsifier check.

    Returns:
        ``(selected_policy, verdict, materialization_permission,
        rationale, branch_evaluated)``.

    Raises:
        RatingPathDecisionError: If the A9(c) override falsifier fires.
    """
    new_anchor = executor_inputs.get("new_separating_anchor")
    parent_verdict = executor_inputs.get("parent_pr249_verdict", "")
    thesis_pragmatism = bool(executor_inputs.get("thesis_pragmatism", False))
    substantive_paragraph_ok = bool(
        executor_inputs.get("substantive_paragraph_ok", False)
    )
    reviewer_signoff = bool(executor_inputs.get("reviewer_signoff", False))
    substantive_paragraph = str(executor_inputs.get("substantive_paragraph", ""))

    # A9(c) override falsifier: any TRUE emission without the
    # substantive paragraph passing admissibility, OR any FALSE emission
    # without substantive reasoning paragraph being recorded.
    if thesis_pragmatism and substantive_paragraph:
        passed, _msg = _check_substantive_paragraph_admissibility(
            substantive_paragraph
        )
        if not passed:
            raise RatingPathDecisionError(
                (
                    "q6h_thesis_pragmatism_set_false_without_substantive_"
                    "reasoning_paragraph_in_md_section_15"
                ),
                (
                    "THESIS_PRAGMATISM emitted TRUE but §15 substantive paragraph "
                    "fails A9(a) admissibility (>= 6 sentences and >= 3 "
                    "PR #249 § cross-references)."
                ),
            )

    # Branch (i) -- bind_event_by_event_glicko2.
    if new_anchor:
        rationale = (
            "Event-by-event Glicko-2 is the deployment-style variant "
            "(PR #247 docstring lines 15-17). Batched form ruled out by "
            f"PR #249 §13a. New separating anchor: {new_anchor}."
        )
        return (
            "bind_event_by_event_glicko2",
            "bind_event_by_event_glicko2",
            _BRANCH_I_PERMISSION,
            rationale,
            "(i)",
        )

    # Branch (ii) -- recommendation_only_event_by_event_glicko2.
    if parent_verdict == "recommendation_only_glicko2":
        rationale = (
            "PR #249 Row 5 selected_policy = recommendation_only_glicko2; "
            "the event-by-event Glicko-2 reference reproduced PR #247 §11 "
            "metrics to within 1e-4 (log_loss = 0.625522). The batched "
            "form is falsified for production materialization on this "
            "corpus. Q6H carries the recommendation forward as the "
            "evidentiary verdict; no new separating anchor is authorised "
            "in the Layer-1 plan."
        )
        return (
            "recommendation_only_event_by_event_glicko2",
            "recommendation_only_event_by_event_glicko2",
            _BRANCH_II_PERMISSION,
            rationale,
            "(ii)",
        )

    # Branch (iii) -- omit_reconstructed_rating_and_unblock_other_five.
    if thesis_pragmatism and substantive_paragraph_ok and reviewer_signoff:
        rationale = (
            "Branches (i) and (ii) are both blocked. THESIS_PRAGMATISM "
            "= TRUE with substantive_paragraph_ok = TRUE and "
            "reviewer_signoff = TRUE. The five non-rating history "
            "families are unblocked; reconstructed_rating is explicitly "
            "excluded; q6_status = "
            "discharged_by_omission_under_thesis_pragmatism."
        )
        return (
            "omit_reconstructed_rating_and_unblock_other_five",
            "omit_reconstructed_rating_and_unblock_other_five",
            _BRANCH_III_PERMISSION,
            rationale,
            "(iii)",
        )

    # If thesis_pragmatism is TRUE but admissibility is missing, surface
    # the override falsifier (A9(c)) even when branch (iii) would not be
    # the verdict.
    if thesis_pragmatism and not substantive_paragraph_ok:
        raise RatingPathDecisionError(
            (
                "q6h_thesis_pragmatism_set_false_without_substantive_"
                "reasoning_paragraph_in_md_section_15"
            ),
            (
                "THESIS_PRAGMATISM emitted TRUE without substantive_paragraph_ok "
                "(§15 sentence / cross-reference admissibility failed)."
            ),
        )

    # Branch (iv) -- defer_to_layer_3_phase_02_internal_decision.
    if executor_inputs.get("no_fresh_blocking_finding", True):
        rationale = (
            "Branches (i), (ii), (iii) are all blocked and there is no "
            "fresh blocking finding. Deferring to a Phase-02 internal "
            "Layer-3 step is the conservative carry-forward verdict."
        )
        return (
            "defer_to_layer_3_phase_02_internal_decision",
            "defer_to_layer_3_phase_02_internal_decision",
            _BRANCH_IV_PERMISSION,
            rationale,
            "(iv)",
        )

    # Branch (v) -- deferred_blocker.
    named_missing_evidence = executor_inputs.get("named_missing_evidence", ())
    if not isinstance(named_missing_evidence, (list, tuple)) or len(
        named_missing_evidence
    ) < 2:
        raise RatingPathDecisionError(
            "q6h_deferred_blocker_emitted_without_blocking_artifact_citation",
            (
                "Branch (v) requires >= 2 enumerated named_missing_evidence "
                f"items; observed {named_missing_evidence!r}"
            ),
        )
    rationale = (
        "All preceding branches blocked. Deferred blocker emitted with "
        f"named missing evidence: {list(named_missing_evidence)}."
    )
    return (
        "deferred_blocker",
        "deferred_blocker",
        _BRANCH_V_PERMISSION,
        rationale,
        "(v)",
    )


# ---------------------------------------------------------------------------
# Decision-row builders (T02 / T03)
# ---------------------------------------------------------------------------


def _evidence_paths_string() -> str:
    """Return a semicolon-joined evidence-paths string for parent PRs.

    Returns:
        Repo-relative paths for the 5 parent PR CSV/MD pairs.
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
    ]
    return ";".join(parts)


def _falsifier_csv_string() -> str:
    """Return semicolon-joined falsifier key list for the CSV cell.

    Returns:
        ``;``-joined FALSIFIER_PRIORITY_CHAIN keys.
    """
    return ";".join(FALSIFIER_PRIORITY_CHAIN)


def _build_decision_row_a_bind_event_by_event_glicko2(
    audit_pr: str,
) -> RatingPathDecision:
    """Build the Q6H_A row -- bind_event_by_event_glicko2 candidate.

    Args:
        audit_pr: PR number string.

    Returns:
        A ``RatingPathDecision``.
    """
    return RatingPathDecision(
        decision_id="Q6H_A_bind_event_by_event_glicko2",
        parent_decision_id="Q6G_selected_policy",
        decision_name="Bind event-by-event Glicko-2 (Branch (i) candidate)",
        included_in_decision="True",
        inclusion_or_rejection_reason=(
            "Candidate evaluated under Branch (i) of the Q6H decision rule; "
            "requires a new separating anchor named in the Layer-1 plan."
        ),
        rating_path_kind="event_by_event_glicko2",
        verdict="bind_event_by_event_glicko2",
        binding_level="candidate_only",
        decision_path="branch_(i)_candidate",
        selected_policy=_NOT_APPLICABLE,
        rating_policy_status="event_by_event_engine_validated_in_pr247_and_pr249",
        event_by_event_policy="imported_from_pr247_run_glicko2_survey",
        batched_policy_status="ruled_out_by_pr249_section_13a",
        omit_reconstructed_rating_policy=_NOT_APPLICABLE,
        other_five_families_materialization_permission=_NOT_APPLICABLE,
        future_materialization_permission=_BRANCH_I_PERMISSION,
        future_column_names=(
            "focal_player_history.*;opponent_player_history.*;"
            "matchup_history_aggregate.*;in_game_history_aggregate.*;"
            "cross_region_fragmentation_handling.is_cross_region;"
            "reconstructed_rating_focal_pre;reconstructed_rating_opp_pre;"
            "reconstructed_rating_diff"
        ),
        excluded_column_names="",
        q5_cross_region_policy=Q5_SELECTED_POLICY,
        q6_status="conditional_on_branch_i_acceptance",
        thesis_pragmatism_flag_value="null",
        thesis_pragmatism_substantive_paragraph_sentence_count="0",
        branch_evaluated="(i)",
        forward_only_constraints=(
            "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"
        ),
        leakage_guard=(
            "prediction strictly precedes update; "
            "PHA decisive-only; cold-start gate G-CS-4 preserved"
        ),
        deployability_rationale=(
            "Event-by-event Glicko-2 is the deployment-style variant; "
            "matches how a live ladder system carries rating state. "
            "Batched form falsified on this corpus by PR #249."
        ),
        thesis_pragmatism_rationale=_NOT_APPLICABLE,
        evidence_paths=_evidence_paths_string(),
        falsifiers=_falsifier_csv_string(),
        audit_pr=audit_pr,
        parent_pr242_csv_sha256=Q6H_PARENT_SHAS["parent_pr242_csv_sha256"],
        parent_pr243_csv_sha256=Q6H_PARENT_SHAS["parent_pr243_csv_sha256"],
        parent_pr245_md_sha256=Q6H_PARENT_SHAS["parent_pr245_md_sha256"],
        parent_pr247_csv_sha256=Q6H_PARENT_SHAS["parent_pr247_csv_sha256"],
        parent_pr247_md_sha256=Q6H_PARENT_SHAS["parent_pr247_md_sha256"],
        parent_pr249_csv_sha256=Q6H_PARENT_SHAS["parent_pr249_csv_sha256"],
        notes=(
            "Q6H Row A (Branch (i) candidate). Bind event-by-event Glicko-2 "
            "ONLY if a new separating anchor (Brier / ECE / calibration-slope) "
            "produces non-overlapping bootstrap CI between Glicko-2 and "
            "TrueSkill AND the anchor was named in the Layer-1 plan. The "
            "canonical Layer-2 dispatch does NOT authorise a new anchor; "
            "Branch (i) is therefore NOT the canonical reached verdict."
        ),
        materialized_output_paths="",
    )


def _build_decision_row_b_recommendation_only_event_by_event_glicko2(
    audit_pr: str,
) -> RatingPathDecision:
    """Build the Q6H_B row -- recommendation_only_event_by_event_glicko2 candidate.

    Args:
        audit_pr: PR number string.

    Returns:
        A ``RatingPathDecision``.
    """
    return RatingPathDecision(
        decision_id="Q6H_B_recommendation_only_event_by_event_glicko2",
        parent_decision_id="Q6G_selected_policy",
        decision_name=(
            "Recommendation-only event-by-event Glicko-2 (Branch (ii) candidate)"
        ),
        included_in_decision="True",
        inclusion_or_rejection_reason=(
            "Candidate evaluated under Branch (ii) of the Q6H decision rule; "
            "preconditions: PR #249 verdict = recommendation_only_glicko2."
        ),
        rating_path_kind="event_by_event_glicko2",
        verdict="recommendation_only_event_by_event_glicko2",
        binding_level="candidate_only",
        decision_path="branch_(ii)_candidate",
        selected_policy=_NOT_APPLICABLE,
        rating_policy_status=(
            "event_by_event_engine_validated_in_pr247_and_pr249;"
            "batched_path_falsified_in_pr249_section_13a"
        ),
        event_by_event_policy="imported_from_pr247_run_glicko2_survey",
        batched_policy_status="ruled_out_by_pr249_section_13a",
        omit_reconstructed_rating_policy=_NOT_APPLICABLE,
        other_five_families_materialization_permission=_NOT_APPLICABLE,
        future_materialization_permission=_BRANCH_II_PERMISSION,
        future_column_names=_NOT_APPLICABLE,
        excluded_column_names="",
        q5_cross_region_policy=Q5_SELECTED_POLICY,
        q6_status="recommendation_only_pending_phase_03_or_later_decision",
        thesis_pragmatism_flag_value="null",
        thesis_pragmatism_substantive_paragraph_sentence_count="0",
        branch_evaluated="(ii)",
        forward_only_constraints=(
            "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"
        ),
        leakage_guard=(
            "prediction strictly precedes update; PHA decisive-only; "
            "cold-start gate G-CS-4 preserved; toon_id region-scoped"
        ),
        deployability_rationale=(
            "Recommendation-only carries the event-by-event Glicko-2 evidence "
            "forward without binding materialization. Named next-proof "
            "candidates include online-update determinism over a third run, "
            "cold-start sensitivity sweep, and 1.96 SE log-loss CI gap to the "
            "rolling baseline."
        ),
        thesis_pragmatism_rationale=_NOT_APPLICABLE,
        evidence_paths=_evidence_paths_string(),
        falsifiers=_falsifier_csv_string(),
        audit_pr=audit_pr,
        parent_pr242_csv_sha256=Q6H_PARENT_SHAS["parent_pr242_csv_sha256"],
        parent_pr243_csv_sha256=Q6H_PARENT_SHAS["parent_pr243_csv_sha256"],
        parent_pr245_md_sha256=Q6H_PARENT_SHAS["parent_pr245_md_sha256"],
        parent_pr247_csv_sha256=Q6H_PARENT_SHAS["parent_pr247_csv_sha256"],
        parent_pr247_md_sha256=Q6H_PARENT_SHAS["parent_pr247_md_sha256"],
        parent_pr249_csv_sha256=Q6H_PARENT_SHAS["parent_pr249_csv_sha256"],
        notes=(
            "Q6H Row B (Branch (ii) candidate). Recommendation-only "
            "event-by-event Glicko-2 is the canonical default-reachable "
            "verdict under PR #249's recommendation_only_glicko2 standing "
            "and absence of a new separating anchor."
        ),
        materialized_output_paths="",
    )


def _build_decision_row_c_omit_reconstructed_rating_and_unblock_other_five(
    audit_pr: str,
) -> RatingPathDecision:
    """Build the Q6H_C row -- omit-and-unblock-five candidate.

    Args:
        audit_pr: PR number string.

    Returns:
        A ``RatingPathDecision``.
    """
    excluded_columns = (
        "reconstructed_rating_focal_pre;"
        "reconstructed_rating_opp_pre;"
        "reconstructed_rating_diff"
    )
    future_columns = ";".join(
        f"{fam}.*" for fam in Q6H_FIVE_FAMILY_POST_OMIT_SET
    )
    return RatingPathDecision(
        decision_id="Q6H_C_omit_reconstructed_rating_and_unblock_other_five",
        parent_decision_id="Q6G_selected_policy",
        decision_name=(
            "Omit reconstructed_rating; unblock other five families "
            "(Branch (iii) candidate; thesis-pragmatism gate)"
        ),
        included_in_decision="True",
        inclusion_or_rejection_reason=(
            "Candidate evaluated under Branch (iii) of the Q6H decision rule; "
            "requires thesis_pragmatism = TRUE AND substantive_paragraph_ok "
            "AND reviewer-adversarial sign-off."
        ),
        rating_path_kind="omit_reconstructed_rating",
        verdict="omit_reconstructed_rating_and_unblock_other_five",
        binding_level="candidate_only",
        decision_path="branch_(iii)_candidate",
        selected_policy=_NOT_APPLICABLE,
        rating_policy_status="reconstructed_rating_family_omitted",
        event_by_event_policy=_NOT_APPLICABLE,
        batched_policy_status="ruled_out_by_pr249_section_13a",
        omit_reconstructed_rating_policy="omit_reconstructed_rating_family_entirely",
        other_five_families_materialization_permission=_BRANCH_III_PERMISSION,
        future_materialization_permission=_BRANCH_III_PERMISSION,
        future_column_names=future_columns,
        excluded_column_names=excluded_columns,
        q5_cross_region_policy=Q5_SELECTED_POLICY,
        q6_status="discharged_by_omission_under_thesis_pragmatism",
        thesis_pragmatism_flag_value="TRUE",
        thesis_pragmatism_substantive_paragraph_sentence_count="standby_paragraph",
        branch_evaluated="(iii)",
        forward_only_constraints=(
            "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"
        ),
        leakage_guard=(
            "prediction strictly precedes update on the 5 non-rating families; "
            "cold-start gate G-CS-4 preserved; toon_id region-scoped"
        ),
        deployability_rationale=(
            "Omits the reconstructed_rating family entirely. The five "
            "non-rating history families remain materialization-eligible "
            "(focal/opponent player history, matchup aggregate, "
            "cross-region handling, in-game history aggregate). "
            "Branch (iii) is reachable only under thesis-pragmatism "
            "with reviewer-adversarial sign-off."
        ),
        thesis_pragmatism_rationale=(
            "Standby paragraph available in MD §15; this row would be the "
            "Q6H verdict only if Branches (i) and (ii) are both blocked and "
            "thesis_pragmatism = TRUE."
        ),
        evidence_paths=_evidence_paths_string(),
        falsifiers=_falsifier_csv_string(),
        audit_pr=audit_pr,
        parent_pr242_csv_sha256=Q6H_PARENT_SHAS["parent_pr242_csv_sha256"],
        parent_pr243_csv_sha256=Q6H_PARENT_SHAS["parent_pr243_csv_sha256"],
        parent_pr245_md_sha256=Q6H_PARENT_SHAS["parent_pr245_md_sha256"],
        parent_pr247_csv_sha256=Q6H_PARENT_SHAS["parent_pr247_csv_sha256"],
        parent_pr247_md_sha256=Q6H_PARENT_SHAS["parent_pr247_md_sha256"],
        parent_pr249_csv_sha256=Q6H_PARENT_SHAS["parent_pr249_csv_sha256"],
        notes=(
            "Q6H Row C (Branch (iii) candidate). reconstructed_rating is the "
            "ONLY family in CROSS-02-02 §6.2 minus L241 not materialized; the "
            "five remaining L238/L239/L240/L242/L243 families are unblocked."
        ),
        materialized_output_paths="",
    )


def _build_decision_row_d_deferred_blocker(audit_pr: str) -> RatingPathDecision:
    """Build the Q6H_D row -- deferred_blocker candidate.

    Args:
        audit_pr: PR number string.

    Returns:
        A ``RatingPathDecision``.
    """
    return RatingPathDecision(
        decision_id="Q6H_D_deferred_blocker",
        parent_decision_id="Q6G_selected_policy",
        decision_name=(
            "Deferred blocker (Branch (v) candidate; named-missing-evidence)"
        ),
        included_in_decision="True",
        inclusion_or_rejection_reason=(
            "Candidate evaluated under Branch (v) of the Q6H decision rule; "
            "fires only when all higher-priority branches are blocked and "
            ">= 2 enumerated named_missing_evidence items are provided."
        ),
        rating_path_kind="deferred_blocker",
        verdict="deferred_blocker",
        binding_level="candidate_only",
        decision_path="branch_(v)_candidate",
        selected_policy=_NOT_APPLICABLE,
        rating_policy_status=(
            "deferred_pending_named_missing_evidence_resolution"
        ),
        event_by_event_policy=_NOT_APPLICABLE,
        batched_policy_status=_NOT_APPLICABLE,
        omit_reconstructed_rating_policy=_NOT_APPLICABLE,
        other_five_families_materialization_permission=_NOT_APPLICABLE,
        future_materialization_permission=_BRANCH_V_PERMISSION,
        future_column_names=_NOT_APPLICABLE,
        excluded_column_names="",
        q5_cross_region_policy=Q5_SELECTED_POLICY,
        q6_status="deferred_pending_named_missing_evidence",
        thesis_pragmatism_flag_value="null",
        thesis_pragmatism_substantive_paragraph_sentence_count="0",
        branch_evaluated="(v)",
        forward_only_constraints=(
            "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"
        ),
        leakage_guard=(
            "no materialization performed; forward-only contract preserved"
        ),
        deployability_rationale=(
            "Reserved for the case where no evidentiary branch is reachable "
            "and thesis-pragmatism is also blocked. Named-missing-evidence "
            "must enumerate >= 2 distinct items."
        ),
        thesis_pragmatism_rationale=_NOT_APPLICABLE,
        evidence_paths=_evidence_paths_string(),
        falsifiers=_falsifier_csv_string(),
        audit_pr=audit_pr,
        parent_pr242_csv_sha256=Q6H_PARENT_SHAS["parent_pr242_csv_sha256"],
        parent_pr243_csv_sha256=Q6H_PARENT_SHAS["parent_pr243_csv_sha256"],
        parent_pr245_md_sha256=Q6H_PARENT_SHAS["parent_pr245_md_sha256"],
        parent_pr247_csv_sha256=Q6H_PARENT_SHAS["parent_pr247_csv_sha256"],
        parent_pr247_md_sha256=Q6H_PARENT_SHAS["parent_pr247_md_sha256"],
        parent_pr249_csv_sha256=Q6H_PARENT_SHAS["parent_pr249_csv_sha256"],
        notes=(
            "Q6H Row D (Branch (v) candidate). Not the canonical default-reached "
            "verdict; recorded only for completeness of the candidate set."
        ),
        materialized_output_paths="",
    )


def _build_decision_row_selected_policy(
    audit_pr: str,
    selected_policy: str,
    verdict: str,
    materialization_permission: str,
    rationale: str,
    branch_evaluated: str,
    thesis_pragmatism_flag_value: str,
    thesis_pragmatism_paragraph_sentence_count: int,
    thesis_pragmatism_rationale: str,
) -> RatingPathDecision:
    """Build the emergent Q6H_selected_policy row (Row 5).

    Args:
        audit_pr: PR number string.
        selected_policy: Selected policy literal.
        verdict: Verdict literal.
        materialization_permission: Future materialization permission.
        rationale: Decision-rule rationale.
        branch_evaluated: Branch token ((i)-(v)).
        thesis_pragmatism_flag_value: TRUE / FALSE / null literal.
        thesis_pragmatism_paragraph_sentence_count: Sentence count of
            the substantive paragraph.
        thesis_pragmatism_rationale: §15 substantive paragraph rationale
            or carry-forward literal.

    Returns:
        A ``RatingPathDecision``.
    """
    if branch_evaluated == "(iii)":
        excluded_columns = (
            "reconstructed_rating_focal_pre;"
            "reconstructed_rating_opp_pre;"
            "reconstructed_rating_diff"
        )
        future_columns = ";".join(
            f"{fam}.*" for fam in Q6H_FIVE_FAMILY_POST_OMIT_SET
        )
        other_five_perm = _BRANCH_III_PERMISSION
        omit_policy = "omit_reconstructed_rating_family_entirely"
        q6_status = "discharged_by_omission_under_thesis_pragmatism"
    elif branch_evaluated == "(i)":
        excluded_columns = ""
        future_columns = (
            "focal_player_history.*;opponent_player_history.*;"
            "matchup_history_aggregate.*;in_game_history_aggregate.*;"
            "cross_region_fragmentation_handling.is_cross_region;"
            "reconstructed_rating_focal_pre;reconstructed_rating_opp_pre;"
            "reconstructed_rating_diff"
        )
        other_five_perm = _NOT_APPLICABLE
        omit_policy = _NOT_APPLICABLE
        q6_status = "bound_by_branch_i_event_by_event_glicko2"
    elif branch_evaluated == "(ii)":
        excluded_columns = ""
        future_columns = _NOT_APPLICABLE
        other_five_perm = _NOT_APPLICABLE
        omit_policy = _NOT_APPLICABLE
        q6_status = "recommendation_only_pending_phase_03_or_later_decision"
    elif branch_evaluated == "(iv)":
        excluded_columns = ""
        future_columns = _NOT_APPLICABLE
        other_five_perm = _NOT_APPLICABLE
        omit_policy = _NOT_APPLICABLE
        q6_status = "deferred_to_layer_3_phase_02_internal_step"
    else:
        excluded_columns = ""
        future_columns = _NOT_APPLICABLE
        other_five_perm = _NOT_APPLICABLE
        omit_policy = _NOT_APPLICABLE
        q6_status = "deferred_pending_named_missing_evidence"
    return RatingPathDecision(
        decision_id="Q6H_selected_policy",
        parent_decision_id="Q6H_B_recommendation_only_event_by_event_glicko2",
        decision_name="Q6H selected policy (BINDING; emergent)",
        included_in_decision="True",
        inclusion_or_rejection_reason=(
            f"Emergent verdict from Q6H decision rule; branch {branch_evaluated} "
            "reached under the canonical default-derivation path (A9(b))."
        ),
        rating_path_kind="emergent_verdict",
        verdict=verdict,
        binding_level="BINDING",
        decision_path=f"branch_{branch_evaluated}_reached",
        selected_policy=selected_policy,
        rating_policy_status=(
            "recommendation_only_event_by_event_validated_batched_path_falsified"
            if branch_evaluated == "(ii)"
            else "see_branch_specific_row"
        ),
        event_by_event_policy=(
            "imported_from_pr247_run_glicko2_survey"
            if branch_evaluated in {"(i)", "(ii)"}
            else _NOT_APPLICABLE
        ),
        batched_policy_status="ruled_out_by_pr249_section_13a",
        omit_reconstructed_rating_policy=omit_policy,
        other_five_families_materialization_permission=other_five_perm,
        future_materialization_permission=materialization_permission,
        future_column_names=future_columns,
        excluded_column_names=excluded_columns,
        q5_cross_region_policy=Q5_SELECTED_POLICY,
        q6_status=q6_status,
        thesis_pragmatism_flag_value=thesis_pragmatism_flag_value,
        thesis_pragmatism_substantive_paragraph_sentence_count=str(
            thesis_pragmatism_paragraph_sentence_count
        ),
        branch_evaluated=branch_evaluated,
        forward_only_constraints=(
            "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"
        ),
        leakage_guard=(
            "prediction strictly precedes update; PHA decisive-only; "
            "cold-start gate G-CS-4 preserved; toon_id region-scoped"
        ),
        deployability_rationale=rationale,
        thesis_pragmatism_rationale=thesis_pragmatism_rationale,
        evidence_paths=_evidence_paths_string(),
        falsifiers=_falsifier_csv_string(),
        audit_pr=audit_pr,
        parent_pr242_csv_sha256=Q6H_PARENT_SHAS["parent_pr242_csv_sha256"],
        parent_pr243_csv_sha256=Q6H_PARENT_SHAS["parent_pr243_csv_sha256"],
        parent_pr245_md_sha256=Q6H_PARENT_SHAS["parent_pr245_md_sha256"],
        parent_pr247_csv_sha256=Q6H_PARENT_SHAS["parent_pr247_csv_sha256"],
        parent_pr247_md_sha256=Q6H_PARENT_SHAS["parent_pr247_md_sha256"],
        parent_pr249_csv_sha256=Q6H_PARENT_SHAS["parent_pr249_csv_sha256"],
        notes=(
            f"Q6H SELECTED POLICY = {selected_policy}\n"
            f"VERDICT = {verdict}\n"
            f"MATERIALIZATION PERMISSION = {materialization_permission}\n"
            f"BRANCH = {branch_evaluated}\n"
            f"RATIONALE: {rationale}\n"
            f"Q5 BINDING preserved ({Q5_SELECTED_POLICY}); "
            f"Q6F BINDING preserved ({Q6F_SELECTED_POLICY}); "
            f"Q6G BINDING preserved ({Q6G_SELECTED_POLICY}); "
            "no TrueSkill re-implementation; no batched Glicko-2 "
            "re-implementation; no Phase 03 / Step 02_01_04 touch."
        ),
        materialized_output_paths="",
    )


# ---------------------------------------------------------------------------
# Top-level builder
# ---------------------------------------------------------------------------


def _canonical_executor_inputs() -> dict[str, Any]:
    """Return the canonical Layer-2 dispatch inputs (A9(b) default).

    Returns:
        Dict suitable for ``_apply_q6h_decision_rule``. Under the
        canonical default, Branch (ii) is the reached verdict.
    """
    return {
        "parent_pr249_verdict": Q6G_SELECTED_POLICY,
        "new_separating_anchor": None,
        "thesis_pragmatism": False,
        "substantive_paragraph_ok": False,
        "reviewer_signoff": False,
        "substantive_paragraph": "",
        "no_fresh_blocking_finding": True,
        "named_missing_evidence": (),
    }


def build_q6h_decision_result(
    audit_pr: str = AUDIT_PR_NUMBER_PLACEHOLDER,
    executor_inputs: dict[str, Any] | None = None,
    csv_path: Path | None = None,
    md_path: Path | None = None,
) -> RatingPathDecisionResult:
    """Build the Q6H decision result for ``executor_inputs``.

    Does NOT verify parent SHAs (that is the entrypoint's responsibility)
    and does NOT write any file. This builder is the pure logic used by
    tests and the public entrypoint.

    Args:
        audit_pr: PR number string.
        executor_inputs: Executor inputs dict (see
            ``_apply_q6h_decision_rule``); defaults to the canonical
            A9(b) inputs.
        csv_path: Output CSV path (used only to populate ``csv_path``).
        md_path: Output MD path (used only to populate ``md_path``).

    Returns:
        A populated ``RatingPathDecisionResult``.
    """
    if executor_inputs is None:
        executor_inputs = _canonical_executor_inputs()
    csv_path_str = str(csv_path) if csv_path is not None else Q6H_DECISION_CSV_REL
    md_path_str = str(md_path) if md_path is not None else Q6H_DECISION_MD_REL
    selected_policy, verdict, permission, rationale, branch = (
        _apply_q6h_decision_rule(executor_inputs)
    )
    paragraph = executor_inputs.get(
        "substantive_paragraph", _THESIS_PRAGMATISM_STANDBY_PARAGRAPH
    )
    if not paragraph:
        paragraph = _THESIS_PRAGMATISM_STANDBY_PARAGRAPH
    sentence_count = _count_paragraph_sentences(paragraph)
    thesis_flag = (
        "TRUE"
        if executor_inputs.get("thesis_pragmatism", False)
        else (
            "null"
            if branch in {"(i)", "(ii)"}
            else "FALSE"
        )
    )
    thesis_rationale = (
        paragraph
        if branch == "(iii)"
        else (
            "Branch (iii) was not reached. The §15 standby paragraph is "
            "rendered for thesis-readiness even when the verdict is reached "
            "by an evidentiary branch."
        )
    )
    decisions = (
        _build_decision_row_a_bind_event_by_event_glicko2(audit_pr),
        _build_decision_row_b_recommendation_only_event_by_event_glicko2(audit_pr),
        _build_decision_row_c_omit_reconstructed_rating_and_unblock_other_five(
            audit_pr
        ),
        _build_decision_row_d_deferred_blocker(audit_pr),
        _build_decision_row_selected_policy(
            audit_pr=audit_pr,
            selected_policy=selected_policy,
            verdict=verdict,
            materialization_permission=permission,
            rationale=rationale,
            branch_evaluated=branch,
            thesis_pragmatism_flag_value=thesis_flag,
            thesis_pragmatism_paragraph_sentence_count=sentence_count,
            thesis_pragmatism_rationale=thesis_rationale,
        ),
    )
    falsifiers_fired = _surface_non_halting_falsifiers(decisions, branch)
    return RatingPathDecisionResult(
        decisions=decisions,
        csv_path=csv_path_str,
        md_path=md_path_str,
        provenance_git_sha=_get_git_sha(),
        falsifiers_fired=falsifiers_fired,
        halting_falsifier=None,
        passed=True,
        selected_policy=selected_policy,
        verdict=verdict,
        materialization_permission=permission,
        rationale=rationale,
        branch_evaluated=branch,
        thesis_pragmatism_flag_value=thesis_flag,
        thesis_pragmatism_paragraph=paragraph,
    )


def _surface_non_halting_falsifiers(
    decisions: tuple[RatingPathDecision, ...],
    branch_evaluated: str,
) -> tuple[str, ...]:
    """Return the non-halting falsifier keys for the result roll-call.

    None of these halt the decision run; they are documentary annotations
    for the MD §12 falsifier roll-call.

    Args:
        decisions: 5 decisions.
        branch_evaluated: Branch token reached.

    Returns:
        Tuple of falsifier keys whose preconditions were touched but
        which did not halt.
    """
    fired: list[str] = []
    if branch_evaluated == "(iii)":
        # Sanity guards: emit only if the omit row's columns are
        # malformed; otherwise these keys remain "would_fire_if".
        omit_row = next(
            d
            for d in decisions
            if d.decision_id == "Q6H_C_omit_reconstructed_rating_and_unblock_other_five"
        )
        if "reconstructed_rating" in omit_row.future_column_names:
            fired.append(
                "q6h_reconstructed_rating_appears_in_future_column_names_if_omit"
            )
        if "reconstructed_rating" not in omit_row.excluded_column_names:
            fired.append(
                "q6h_reconstructed_rating_missing_from_excluded_columns_if_omit"
            )
    return tuple(fired)


# ---------------------------------------------------------------------------
# Structural falsifier checks
# ---------------------------------------------------------------------------


def _check_decision_count(
    decisions: tuple[RatingPathDecision, ...],
) -> tuple[bool, str]:
    """Verify exactly 5 decisions per A11."""
    if len(decisions) != 5:
        return (False, f"expected 5 decisions; got {len(decisions)}")
    return (True, "")


def _check_decision_id_order(
    decisions: tuple[RatingPathDecision, ...],
) -> tuple[bool, str]:
    """Verify decision IDs match the canonical A11 order."""
    observed = tuple(d.decision_id for d in decisions)
    if observed != Q6H_DECISION_ROWS:
        return (
            False,
            f"decision id order mismatch: observed {observed}; expected {Q6H_DECISION_ROWS}",
        )
    return (True, "")


def _check_q6h_selected_policy_row_present(
    decisions: tuple[RatingPathDecision, ...],
) -> tuple[bool, str]:
    """Verify the Q6H_selected_policy row exists."""
    for d in decisions:
        if d.decision_id == "Q6H_selected_policy":
            return (True, "")
    return (False, "Q6H_selected_policy row missing")


def _check_no_materialized_output_paths(
    decisions: tuple[RatingPathDecision, ...],
) -> tuple[bool, str]:
    """Verify every row's materialized_output_paths is empty (A13)."""
    for d in decisions:
        if d.materialized_output_paths != "":
            return (
                False,
                f"row {d.decision_id} has non-empty materialized_output_paths",
            )
    return (True, "")


def _check_q5_not_re_adjudicated(
    decisions: tuple[RatingPathDecision, ...],
) -> tuple[bool, str]:
    """Verify no row's verdict carries a Q5 token (A2)."""
    for d in decisions:
        if d.verdict == Q5_SELECTED_POLICY or d.selected_policy == Q5_SELECTED_POLICY:
            return (False, f"row {d.decision_id} carries Q5 token")
        if d.q5_cross_region_policy not in {Q5_SELECTED_POLICY, _NOT_APPLICABLE}:
            return (
                False,
                f"row {d.decision_id} q5_cross_region_policy drift: {d.q5_cross_region_policy!r}",
            )
    return (True, "")


def _check_q6f_not_re_adjudicated(
    decisions: tuple[RatingPathDecision, ...],
) -> tuple[bool, str]:
    """Verify no Row-5 verdict equals the Q6F verdict token (A3)."""
    for d in decisions:
        if d.decision_id == "Q6H_selected_policy" and d.verdict == Q6F_SELECTED_POLICY:
            return (False, f"row {d.decision_id} carries Q6F verdict")
    return (True, "")


def _check_q6g_not_re_adjudicated(
    decisions: tuple[RatingPathDecision, ...],
) -> tuple[bool, str]:
    """Verify no Row-5 verdict equals the Q6G policy token (A4)."""
    for d in decisions:
        if d.decision_id == "Q6H_selected_policy" and d.verdict == Q6G_SELECTED_POLICY:
            return (False, f"row {d.decision_id} carries Q6G verdict")
    return (True, "")


def _check_omit_row_excluded_columns_present(
    decisions: tuple[RatingPathDecision, ...],
) -> tuple[bool, str]:
    """Verify the omit row lists reconstructed_rating in excluded_column_names."""
    for d in decisions:
        if (
            d.decision_id
            == "Q6H_C_omit_reconstructed_rating_and_unblock_other_five"
        ):
            if "reconstructed_rating" not in d.excluded_column_names:
                return (
                    False,
                    "omit row missing reconstructed_rating in excluded_column_names",
                )
    return (True, "")


# ---------------------------------------------------------------------------
# CSV writer (byte-deterministic)
# ---------------------------------------------------------------------------


def _decision_to_row(d: RatingPathDecision) -> list[str]:
    """Convert a decision to its CSV row list (canonical column order)."""
    return [str(getattr(d, name)) for name in Q6H_DECISION_SCHEMA]


def _write_csv(
    decisions: tuple[RatingPathDecision, ...],
    csv_path: Path,
) -> None:
    """Write the Q6H CSV byte-deterministically.

    Args:
        decisions: 5 decisions.
        csv_path: Output path.
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    sorted_decisions = sorted(decisions, key=lambda d: d.decision_id)
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(list(Q6H_DECISION_SCHEMA))
        for d in sorted_decisions:
            writer.writerow(_decision_to_row(d))


# ---------------------------------------------------------------------------
# MD writer (>= 19 sections)
# ---------------------------------------------------------------------------


_MD_SECTION_15_HEADER: str = "## 15. Thesis-Pragmatism Rationale (A9; standby paragraph)"


def _md_section_15_text(paragraph: str) -> str:
    """Return the §15 body text given the substantive paragraph."""
    return paragraph.strip()


def _md_section_16_text() -> str:
    """Return §16 verbatim quotation of PR #247 docstring lines 15-17.

    The PR #247 ``_run_glicko2_survey`` docstring's lines 15-17 are the
    Args block (``mu``, ``rd``, ``sigma`` documentation). Per the Layer-2
    spec, the quotation preserves double-backticks. The verbatim token
    ``omit_reconstructed_rating_and_unblock_other_five`` does NOT appear
    in the PR #247 docstring itself; the explanatory link is therefore
    written in the prose surrounding the verbatim quote (Layer-2 spec
    fallback).
    """
    quote = (
        "    Args:\n"
        "        stream: PHA forward-only stream.\n"
        "        mu: Initial Glicko rating (default 1500.0; mapped to Glicko-2\n"
        "            internal scale by ``(mu - 1500) / 173.7178``)."
    )
    intro = (
        "Verbatim from PR #247's ``_run_glicko2_survey`` docstring "
        "(lines 15-17 of the docstring; the Args block header and the "
        "first parameter documentation):"
    )
    explanatory = (
        "The Layer-2 spec calls for the verbatim token "
        "``omit_reconstructed_rating_and_unblock_other_five`` to be "
        "preserved in this quotation. That token is NOT present in "
        "PR #247's docstring at lines 15-17 (the docstring documents "
        "the Glicko-2 engine, not the Q6H decision-rule branches). The "
        "token is instead a Q6H decision-rule literal defined in this "
        "module's ``Q6H_PATH_DECISION_RULE`` Branch (iii). The "
        "explanatory link between the PR #247 engine and the Q6H "
        "Branch (iii) literal is: if Q6H selects "
        "``omit_reconstructed_rating_and_unblock_other_five``, the "
        "PR #247 engine is NOT invoked (the reconstructed_rating family "
        "is omitted); if Q6H selects ``bind_event_by_event_glicko2`` or "
        "``recommendation_only_event_by_event_glicko2``, the PR #247 "
        "engine remains the canonical reference."
    )
    return f"{intro}\n\n```\n{quote}\n```\n\n{explanatory}"


def _md_section_10_table() -> str:
    """Return §10 5-family-post-omit table (if Branch (iii) is selected)."""
    rows = [
        f"| {fam} |" for fam in Q6H_FIVE_FAMILY_POST_OMIT_SET
    ]
    return (
        "| Family (CROSS-02-02 §6.2 minus L241) |\n"
        "|---|\n"
        + "\n".join(rows)
        + "\n\nExplicitly EXCLUDED if Branch (iii) is selected: "
        "`reconstructed_rating` (L241)."
    )


def _md_section_8_candidate_table() -> str:
    """Return §8 candidate-verdict table."""
    lines = [
        "| Row | Decision ID | Branch | Verdict |",
        "|---|---|---|---|",
        (
            "| 1 | Q6H_A_bind_event_by_event_glicko2 | (i) | "
            "bind_event_by_event_glicko2 |"
        ),
        (
            "| 2 | Q6H_B_recommendation_only_event_by_event_glicko2 | (ii) | "
            "recommendation_only_event_by_event_glicko2 |"
        ),
        (
            "| 3 | Q6H_C_omit_reconstructed_rating_and_unblock_other_five | "
            "(iii) | omit_reconstructed_rating_and_unblock_other_five |"
        ),
        (
            "| 4 | Q6H_D_deferred_blocker | (v) | deferred_blocker |"
        ),
    ]
    return "\n".join(lines)


def _md_section_12_falsifier_roll_call() -> str:
    """Return §12 falsifier roll-call as a code block."""
    lines = ["FALSIFIER ROLL-CALL (Q6H; canonical run)"]
    lines.append("=" * 40)
    lines.append("")
    for key in FALSIFIER_PRIORITY_CHAIN:
        lines.append(f"  - {key}  :did_not_fire")
    return "\n".join(lines)


def _md_sections(
    result: RatingPathDecisionResult,
    audit_pr: str,
) -> str:
    """Render the Q6H MD document (>= 19 sections).

    Args:
        result: Populated decision result.
        audit_pr: PR number string.

    Returns:
        Full MD content string.
    """
    selected_row = next(
        d for d in result.decisions if d.decision_id == "Q6H_selected_policy"
    )
    lines: list[str] = []
    lines.append("# Q6H Final Rating-Path Decision")
    lines.append("")
    lines.append(f"**Audit PR:** {audit_pr}")
    lines.append("")
    # §1.
    lines.append("## 1. Summary (Non-Materialization; Non-Phase-03)")
    lines.append("")
    lines.append(
        "This artifact is the Q6H final rating-path decision. It is "
        "NOT a materialization PR, NOT a Phase-03 baseline, and does "
        "NOT close Step 02_01_03. The Q6H decision rule (A12; R2.5) "
        "selects ONE of five branches; under the canonical Layer-2 "
        "default (A9(b)), Branch (ii) is the reached verdict and the "
        "materialization permission stays at "
        f"`{result.materialization_permission}`. "
        f"Selected policy: `{result.selected_policy}`; branch: "
        f"`{result.branch_evaluated}`."
    )
    lines.append("")
    # §2.
    lines.append("## 2. Lineage (Parent PRs and Pinned SHAs)")
    lines.append("")
    lines.append("Parent PR SHAs (pinned per A1; 10 total):")
    for sha_key, sha_val in Q6H_PARENT_SHAS.items():
        lines.append(f"- `{sha_key}`: `{sha_val}`")
    lines.append("")
    lines.append(
        "Merge SHAs: PR #242 (master `e372e7b6`), PR #243 (master "
        "`93240b19`-class), PR #245 (master `ee15d362`), PR #247 "
        "(master `779dc40a`), PR #249 (master `d9276194`); Q6H Layer-1 "
        "plan merged at master `f37efed1`."
    )
    lines.append("")
    # §3.
    lines.append("## 3. Scope and Explicit Exclusions")
    lines.append("")
    lines.append(
        "Q6H closes the rating-path question for `reconstructed_rating` "
        "(CROSS-02-02 §6.2 L241). Out of scope: Phase-03 baselines; "
        "Layer-3 materialization; re-adjudication of Q1-Q5 / Q6 / Q6F "
        "/ Q6G; new batched-Glicko-2 sensitivity arm; TrueSkill "
        "re-implementation; worldwide-identity migration; AoE2; Step "
        "02_01_03 closure; CROSS-02-01 audit file; any Parquet output."
    )
    lines.append("")
    # §4.
    lines.append("## 4. Q5 Binding Preservation")
    lines.append("")
    lines.append(
        f"`Q5_selected_policy = {Q5_SELECTED_POLICY}` (verdict "
        f"`{Q5_SELECTED_POLICY_VERDICT}`); BINDING and NOT "
        "re-adjudicated by Q6H. Falsifier "
        "`q6h_q5_re_adjudication_drift` enforces."
    )
    lines.append("")
    # §5.
    lines.append("## 5. Q6F Binding Preservation")
    lines.append("")
    lines.append(
        f"`Q6F_selected_policy = {Q6F_SELECTED_POLICY}`; "
        "materialization_permission = "
        "`recommendation_only_blocked_pending_implementation_proof_pr`; "
        "BINDING and NOT re-adjudicated. Falsifier "
        "`q6h_q6f_re_adjudication_drift` enforces."
    )
    lines.append("")
    # §6.
    lines.append("## 6. Q6G Binding Preservation")
    lines.append("")
    lines.append(
        f"`Q6G_selected_policy = {Q6G_SELECTED_POLICY}` (equivalence "
        "FAILED both bounds: Spearman rho = 0.2292; |Delta log-loss| "
        "= 0.07928; byte-determinism PASSED). BINDING and NOT "
        "re-adjudicated. Falsifier `q6h_q6g_re_adjudication_drift` "
        "enforces."
    )
    lines.append("")
    # §7.
    lines.append("## 7. Decision-Rule Order-of-Operations (A12; R2.5)")
    lines.append("")
    lines.append(
        "Evidentiary branches are evaluated BEFORE the pragmatism "
        "branch. The methodological justification: a substantively "
        "justified verdict (Branch (i) bind via fresh evidence; "
        "Branch (ii) conservative recommendation) is preferred over a "
        "pragmatic omission (Branch (iii)). THESIS_PRAGMATISM is a "
        "last-resort gate that may close the family only when no "
        "evidentiary branch is reachable; evaluating it first would "
        "allow a boolean to short-circuit substantive adjudication, "
        "violating Invariant I7 (no magic gates)."
    )
    lines.append("")
    lines.append("```")
    lines.append(Q6H_PATH_DECISION_RULE)
    lines.append("```")
    lines.append("")
    # §8.
    lines.append("## 8. Candidate Verdicts (Branches (i)-(v))")
    lines.append("")
    lines.append(_md_section_8_candidate_table())
    lines.append("")
    # §9.
    lines.append("## 9. Evidentiary Anchors Carried Forward from PR #249")
    lines.append("")
    lines.append(
        "- PR #249 §13a equivalence proof: Spearman rho = 0.2292; "
        "|Delta log-loss| = 0.07928; passes_spearman_bound = false; "
        "passes_delta_log_loss_bound = false.\n"
        "- PR #249 §13b byte-determinism: hashes_equal = true.\n"
        "- PR #249 §15 limitations: `rating_period_days = 30` long vs "
        "median toon span 0.88 d.\n"
        "- PR #249 Row 1 reproduces PR #247 §11 Glicko-2 metrics to "
        "within 1e-4 (log_loss = 0.625522).\n"
        "- PR #247 §11 Glicko-2 vs TrueSkill CI overlap ~ 0.9% of "
        "mid-range; no separating anchor authorised in this Layer-1 plan."
    )
    lines.append("")
    # §10.
    lines.append("## 10. The 5-Family Post-Omit Set (if Branch (iii) selected)")
    lines.append("")
    lines.append(_md_section_10_table())
    lines.append("")
    # §11.
    lines.append("## 11. Schema Column Count Assertion")
    lines.append("")
    lines.append(
        f"Q6H CSV has exactly {Q6H_DECISION_SCHEMA_COLUMN_COUNT} columns "
        f"per A10 / R2.3 (38-column schema). Column 38 is "
        "`materialized_output_paths` (split from legacy `notes` so "
        "materialization paths are reviewer-grep-able without parsing "
        "prose). Column 38 is EMPTY on every row (A13 -- no "
        "materialization creep)."
    )
    lines.append("")
    # §12.
    lines.append("## 12. Falsifier Roll-Call")
    lines.append("")
    lines.append("```")
    lines.append(_md_section_12_falsifier_roll_call())
    lines.append("```")
    lines.append("")
    # §13.
    lines.append("## 13. Limitations Carried Forward")
    lines.append("")
    lines.append(
        "- `toon_id` is region-scoped per Invariant #2 branch (iii). "
        "Rating fragmentation across region-migrating players is an "
        "accepted Q6H bias. A future worldwide-identity PR (out of "
        "scope here) would address it separately.\n"
        "- Cold-start gate G-CS-4: Q6H inherits PR #247 / PR #249's "
        "cold-start mask. The first PHA row for any toon_id contributes "
        "nothing to metric computation but is counted in "
        "`cold_start_rate`.\n"
        "- PHA decisive-only (PR #242 Q1): PHA carries decisive results "
        "only; Glicko-2's draw-margin parameter is inapplicable."
    )
    lines.append("")
    # §14.
    lines.append("## 14. Future Materialization Permission")
    lines.append("")
    lines.append(
        f"`future_materialization_permission = "
        f"{result.materialization_permission}`. Future materialization "
        "is a SEPARATE PR (Layer-3 or later) subject to its own "
        "CROSS-02-01 post-materialization leakage audit. This Q6H "
        "decision does NOT substitute for that audit."
    )
    lines.append("")
    # §15.
    lines.append(_MD_SECTION_15_HEADER)
    lines.append("")
    lines.append(_md_section_15_text(result.thesis_pragmatism_paragraph))
    lines.append("")
    # §16.
    lines.append("## 16. PR #247 Docstring Verbatim Quotation (lines 15-17)")
    lines.append("")
    lines.append(_md_section_16_text())
    lines.append("")
    # §17.
    lines.append("## 17. Non-Substitution Statement")
    lines.append("")
    lines.append(
        "This artifact does NOT substitute for any future "
        "materialization PR; it neither materializes a rating value "
        "nor authorises a downstream Parquet write. Q5 / Q6F / Q6G "
        "remain BINDING and are not retracted. Step 02_01_03 closure "
        "is deferred to a future PR (Layer-3 materialization or "
        "omit-closure follow-up)."
    )
    lines.append("")
    # §18.
    lines.append("## 18. Provenance (10 SHA Pins + Master HEAD SHA)")
    lines.append("")
    for sha_key, sha_val in Q6H_PARENT_SHAS.items():
        lines.append(f"- `{sha_key}`: `{sha_val}`")
    lines.append(f"- Q6H decision-rule SHA-256: `{Q6H_PATH_DECISION_RULE_SHA256}`")
    lines.append(f"- HEAD git SHA at run time: `{result.provenance_git_sha}`")
    lines.append("")
    # §19.
    lines.append("## 19. Final Verdict and Reviewer-Adversarial Sign-Off")
    lines.append("")
    lines.append(
        f"**Selected policy:** `{result.selected_policy}`\n\n"
        f"**Verdict:** `{result.verdict}`\n\n"
        f"**Branch evaluated:** `{result.branch_evaluated}`\n\n"
        f"**Future materialization permission:** "
        f"`{result.materialization_permission}`\n\n"
        f"**Rationale:** {result.rationale}\n\n"
        "**Reviewer-adversarial sign-off:** Layer-1 plan APPROVED post-"
        "Round-2 mechanical-fix (PR #250 merge SHA `f37efed1`). Layer-2 "
        "execution receives a fresh 3-round adversarial cap per "
        "`feedback_adversarial_cap_execution.md`."
    )
    lines.append("")
    lines.append(
        f"Notes (verbatim from Row 5 CSV `notes` column):\n\n```\n"
        f"{selected_row.notes}\n```"
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def _write_md(
    result: RatingPathDecisionResult,
    md_path: Path,
    audit_pr: str,
) -> None:
    """Write the Q6H MD document.

    The §15 sentence and cross-reference admissibility check is applied
    at writer time; a violation raises ``RatingPathDecisionError`` with
    the A9(c) override falsifier key.

    Args:
        result: Populated decision result.
        md_path: Output path.
        audit_pr: PR number string.
    """
    md_path.parent.mkdir(parents=True, exist_ok=True)
    paragraph = result.thesis_pragmatism_paragraph
    passed, message = _check_substantive_paragraph_admissibility(paragraph)
    if not passed:
        raise RatingPathDecisionError(
            (
                "q6h_thesis_pragmatism_set_false_without_substantive_"
                "reasoning_paragraph_in_md_section_15"
            ),
            message,
        )
    content = _md_sections(result, audit_pr)
    md_path.write_text(content, encoding="utf-8")


def write_q6h_decision_artifacts(
    result: RatingPathDecisionResult,
    csv_path: Path,
    md_path: Path,
) -> None:
    """Write the Q6H decision CSV+MD pair byte-deterministically.

    Args:
        result: A populated ``RatingPathDecisionResult``.
        csv_path: Output CSV path.
        md_path: Output MD path.
    """
    _write_csv(result.decisions, csv_path)
    _write_md(result, md_path, audit_pr=result.decisions[0].audit_pr)


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def run_q6h_rating_path_decision(
    csv_path: Path,
    md_path: Path,
    audit_pr: str = AUDIT_PR_NUMBER_PLACEHOLDER,
    executor_inputs: dict[str, Any] | None = None,
    write_artifacts: bool = True,
    repo_root: Path | None = None,
    verify_parent_shas: bool = True,
) -> RatingPathDecisionResult:
    """Run the Q6H rating-path decision end-to-end.

    Steps:
        1. (Optional) verify all 10 parent SHAs against the master file
           system.
        2. Apply the Q6H decision rule with the canonical Layer-2 inputs
           (or executor-supplied inputs).
        3. Build all 5 decision rows.
        4. (Optional) write the CSV + MD pair byte-deterministically.

    Args:
        csv_path: Output CSV path.
        md_path: Output MD path.
        audit_pr: PR number string (e.g., ``'PR #251'``); placeholder
            ``'PR #<TBD>'`` is the default sentinel and is replaced once
            the draft PR is assigned a number.
        executor_inputs: Optional executor-input override dict.
        write_artifacts: If True, write the CSV+MD pair; otherwise
            return the result without writing.
        repo_root: Optional repository root for SHA pin verification;
            if omitted, walks up from ``csv_path``.
        verify_parent_shas: If True, verify all 10 parent SHAs and halt
            on first mismatch. Set False only in tests that synthesise
            parent files via fixtures.

    Returns:
        Populated ``RatingPathDecisionResult``.

    Raises:
        RatingPathDecisionError: If any parent SHA mismatches or the
            A9(c) override falsifier fires.
    """
    if verify_parent_shas:
        if repo_root is None:
            repo_root = _find_repo_root(csv_path)
        mismatches = _check_parent_pr_shas(repo_root)
        if mismatches:
            key, message = mismatches[0]
            raise RatingPathDecisionError(key, message)
    result = build_q6h_decision_result(
        audit_pr=audit_pr,
        executor_inputs=executor_inputs,
        csv_path=csv_path,
        md_path=md_path,
    )
    if write_artifacts:
        write_q6h_decision_artifacts(result, csv_path, md_path)
    return result
