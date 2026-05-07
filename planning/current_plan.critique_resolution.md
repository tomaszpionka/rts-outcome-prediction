---
critique_of: planning/current_plan.md
critique_file: planning/current_plan.critique.md
plan_branch: phase02/roadmap-stubs-feature-registry
resolution_role: planner-science (amendment author)
resolution_model: claude-opus-4-7
resolution_date: 2026-05-06
verdict_at_resolution: PASS (5/5 REQUIRED FIXES applied)
---

# Critique resolution — Phase 02 ROADMAP-stubs PR

`planning/current_plan.critique.md` returned `PASS-WITH-FIXES` with five
REQUIRED FIXES and ten WARNINGS. This file records resolution of the five
REQUIRED FIXES. WARNINGS are catalogued at the bottom for transparency;
they remain at the executor's discretion (the critique itself classed them
as cosmetic / discretionary, not gating).

## REQUIRED FIXES — resolution

1. **`slot_identity_consistency` registry classification source.**
   Resolved by amending T01's Step YAML `description` field
   (`current_plan.md` lines 123–133 area) to declare
   `sanity_gate_not_model_input` as a registry-introduced classification
   derived from the CSV's `notes_for_phase02` + `eligibility_scope`
   columns and PR #208 Phase 02 guidance, while explicitly recording that
   the CSV's `status_in_game_snapshot` value remains
   `eligible_for_phase02_now` and is NOT being reclassified at the CSV
   layer. T04 §5 mechanical check still fires (the registry-level
   classification text appears in the SC2 ROADMAP) but no longer
   misrepresents the CSV vocabulary. Amendment also propagates to
   §"Critique instruction" item 5.

2. **`spec_id` literal vs `version` literal framing.**
   Resolved by adding Assumption A8 to §"Assumptions & unknowns"
   documenting that CROSS-02-00 / CROSS-02-01 carry coinciding
   `spec_id` and `version` fields, while CROSS-02-02 / CROSS-02-03 carry
   the bare-major form in `spec_id` and the patch-locked form in
   `version`; the four canonical strings the plan cites correspond to
   the `version` field for CROSS-02-02 / CROSS-02-03 and to the
   `spec_id` field for CROSS-02-00 / CROSS-02-01. Every prior occurrence
   of the phrase "spec_id literal" / "spec_id literals" was swept and
   replaced with "locked spec/version identifier" / "locked spec/version
   identifiers". This is a documentation-only change; no spec frontmatter
   or citation string is altered.

3. **WP-2 paragraph version-string conflict.**
   Resolved by changing T01 step 3, T02 step 2, and T03 step 2 from
   "preserve verbatim" to "preserve in meaning, with `CROSS-02-01-v1,
   LOCKED 2026-04-21` updated to `CROSS-02-01-v1.0.1, LOCKED 2026-05-06
   (patch successor of CROSS-02-01-v1, LOCKED 2026-04-21)` and
   `(CROSS-02-00-v1)` updated to `(CROSS-02-00-v3.0.1)`". After edit, no
   paragraph in any of the three ROADMAPs carries both the bare-major
   and patch-locked form for the same spec. A new §"Critique instruction"
   item 8 explicitly flags this property for reviewer-deep
   post-execution.

4. **Reviewer routing — plan instruction contradicts active rule.**
   Resolved by rewriting §"Gate Condition" items 4 and 5 (lines 523–524)
   and §"Critique instruction" header + lead paragraph (lines 562–564)
   to dispatch reviewer-deep, not reviewer-adversarial.
   Reviewer-adversarial is now escalated only if reviewer-deep raises an
   unresolved methodology BLOCKER, per
   `.claude/rules/data-analysis-lineage.md` §"Agent and model routing
   discipline" final paragraph. The earlier in-plan parenthetical
   ("applies only to PR #209") was removed because the rule's wording
   pins to the "active Phase 02 readiness PR" — which this is.

5. **Branch prefix non-canonical for Category A.**
   Resolved by adding Assumption A7 to §"Assumptions & unknowns"
   documenting that `phase02/roadmap-stubs-feature-registry` is
   non-canonical taxonomy-wise (`docs/TAXONOMY.md` §Category maps
   Category A to `feat/`) but is intentionally inherited as a
   project-specific phase-work convention from PR #209 / PR #210
   precedent. The branch is **not** renamed; `docs/TAXONOMY.md` is
   **not** edited. The `git-workflow.md` minor-version-bump rule still
   applies because the substantive work category is `feat`.

## Re-review

Reviewer-deep does not need to be re-run on this amendment. All five
fixes are mechanical edits at the documentation layer — none introduces
a new methodology claim, changes a feature-family classification rule,
or relaxes a temporal-cutoff invariant. The amended plan's diff against
the pre-amendment plan is text-only (Assumption A7 + A8 inserted; six
"spec_id literal" phrases swept; one `description` clause clarified;
three WP-2 instructions rewritten; one Gate Condition item rewritten;
one Critique instruction section rewritten). The post-execution
reviewer-deep pass on the T01–T05 diff remains the gate per
`.claude/rules/data-analysis-lineage.md`.

## Implementation gate

Implementation (T01–T05 dispatch) remains BLOCKED until this resolution
file and the amended `planning/current_plan.md` are committed to
`phase02/roadmap-stubs-feature-registry`. After the amendment commit
lands, T01 may be dispatched.

## WARNINGS (catalogued; not gated by this resolution)

The critique's ten WARNINGS (W1 `predecessors` list shape; W2
`predecessors` plural for SC2; W3 `pyproject.toml` version line
non-fragile reference; W4 grep-pattern Unicode robustness; W5
`pipeline_section` field shape vs Phase 01 precedent; W6 `phase` field
shape vs Phase 01 precedent; W7 `manual_reference` "Section 2" vs "§2";
W8 OQ3 conditional-branch should fold into T05; W9
`gate.artifact_check` "NOT APPLICABLE" wording; W10 `thesis_mapping` §4.5
existence) are not gated by this resolution. The critique itself classed
them as cosmetic / discretionary. Executor may apply them inline during
T01 / T02 / T03 / T05 if doing so does not expand the diff scope; the
mechanical check rules in T04 are written to PASS regardless of which
WARNING resolutions are applied.
