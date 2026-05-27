---
plan_role: planner-science (Round 2)
plan_model: claude-opus-4-7[1m]
plan_date: 2026-05-27
plan_layer: 1
chosen_outcome: A1
category: A
branch: feat/sc2egset-02-01-03b-omit-closure-roadmap-stub
base_ref: 28bfc89fae56e88bd4c039077d7971496d5f1b1c
date: 2026-05-27
planner_model: claude-opus-4-7[1m]
dataset: sc2egset
phase: "02"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
step: "02_01_99 (Layer-1 ROADMAP-only stub design for omit-closure follow-up)"
non_batching_sequence_position: "Step 1 of 9 (ROADMAP stub only) — first planning unit for the new Step 02_01_99 lineage segment (omit-closure follow-up to Step 02_01_03's Q6H Branch (ii) verdict)."
critique_required: true
critique_required_before_execution: true
critique_reviewer: reviewer-adversarial
gate_reviewer: "reviewer-adversarial (Category A pre-execution gate)"
adversarial_round_cap: "3 rounds total (planning-side); Round 1 consumed on the rejected direct-narrowing plan; Round 2 begins on this plan; Round 3 reserved for unresolved BLOCKERs."
adversarial_cap_symmetry: "Same 3-round cap applies to execution-side review per feedback_adversarial_cap_execution.md."
parent_planning_pr: "PR #250 (Q6H Layer-1; merged at master f37efed1)"
parent_execution_pr: "PR #251 (Q6H Layer-2; merged at master 28bfc89f)"
planning_pr: "PR #252"
planning_pr_version_bump: "none (Layer-1 planning-only; 2 files)"
planning_pr_scope: "Layer-1 (2 files only) — planning/current_plan.md + planning/current_plan.critique.md. NO ROADMAP edit, NO pyproject bump, NO CHANGELOG entry, NO planning/INDEX.md archive, NO status YAML flip, NO research_log entry, NO artifact, NO source/test/notebook touch. NO Q6H artifact mutation. NO Step 02_01_03 scope narrowing."
future_layer2_pr: "PR #<TBD-A1-LAYER-2>"
future_layer2_version_bump: "3.78.0 → 3.79.0 (minor; feat-family per .claude/rules/git-workflow.md)"
future_layer2_file_count: 4
future_layer2_pr_scope: "Layer-2 ROADMAP-only stub (4 files) — ROADMAP.md (insert Step 02_01_99 block) + pyproject.toml (3.78.0 → 3.79.0) + CHANGELOG.md (new [3.79.0] block) + planning/INDEX.md (archive Layer-1 PR; promote Layer-2 PR). NO new artifact, NO module, NO notebook, NO test, NO status YAML flip, NO research_log entry, NO source touch."
phase_status_at_plan_time: "Phase 02 in_progress (Pipeline Section 02_01 in_progress); Phase 03 not_started"
step_status_at_plan_time: "02_01_01 complete; 02_01_02 complete; 02_01_03 in_progress (Q6/Q6F/Q6G/Q6H adjudication chain merged but step not closed); 02_01_99 NOT YET DECLARED (this plan declares it)"
non_batching_compliance: "Strictly compliant with .claude/rules/data-analysis-lineage.md §Non-batching rule. This Layer-1 PR is sequence step 1 (ROADMAP stub plan only). The future Layer-2 PR is the ROADMAP-stub artifact (still effectively sequence step 1 — only the ROADMAP block is created; the omit-closure artifact remains a separate future PR per the #238 → #239 precedent). Scaffold (sequence step 2), execute+report (step 3), user review (4), commit (5), next validator (6), artifacts (7), research_log / STEP_STATUS (8), and reviewer-deep (9) are deferred to SEPARATE successor PRs."
source_artifacts:
  # PR #251 Q6H Layer-2 closure artifacts (the immediate parent — defines §17 two-path admission and standby §15 paragraph)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.md
  - src/rts_predict/games/sc2/datasets/sc2egset/decide_history_rating_path.py
  # PR #249 Q6G implementation-proof artifacts (the rating-engine evidence cited in §15 standby paragraph)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.md
  # PR #247 Q6F survey artifacts
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.md
  # PR #245 Q6 rating-reconstruction successor adjudication
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.md
  # PR #243 Q5 cross-region successor adjudication
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.md
  # PR #242 Step 02_01_03 source/anchor/cold-start adjudication
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md
  # Closed Step 02_01_01 catalog (defines the 6 history families authoritatively)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv
  # Specs (provenance bond targets)
  - reports/specs/02_00_feature_input_contract.md
  - reports/specs/02_01_leakage_audit_protocol.md
  - reports/specs/02_02_feature_engineering_plan.md
  - reports/specs/02_03_temporal_feature_audit_protocol.md
  # Closure-relevant status YAMLs (READ; byte-unchanged in this PR and the future Layer-2 PR)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml
  # Dataset ROADMAP (the future Layer-2 PR inserts Step 02_01_99 block after Step 02_01_03 block at approximately line 2523 (re-grep at Layer-2 dispatch time))
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
  # Dataset research log (READ only; no entry added by this Layer-1 or the Layer-2 ROADMAP-stub PR per non-batching rule sequence step 1)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
  # Round-1 rejection input
  - planning/current_plan.md  # (Round-1 plan, to be overwritten by this Round-2 plan)
  - planning/current_plan.critique.md  # (Round-1 critique HOLD with R1-B1 / R1-B2 / R1-B3)
  # Rules / invariants / protocols
  - .claude/scientific-invariants.md
  - .claude/ml-protocol.md
  - .claude/rules/data-analysis-lineage.md
  - .claude/rules/git-workflow.md
  - .claude/rules/python-code.md
  - docs/PHASES.md
  - docs/TAXONOMY.md
  - docs/templates/planner_output_contract.md
  - docs/templates/plan_template.md
invariants_touched:
  - "I3 (temporal discipline — strict history_time < target_time; future omit-closure artifact cites this as the rationale for the 5-family unblock criterion)"
  - "I6 (SQL provenance — future omit-closure artifact MD must embed verbatim queries for any count/distribution it reports)"
  - "I7 (no magic numbers / no magic gates — Branch (iii) preconditions are evidentiary admissibility criteria, not magic booleans; the substantive paragraph + reviewer sign-off pins prevent boolean-driven closure)"
  - "I9 (research pipeline discipline — Step 02_01_99 conclusions derive only from its own future artifacts and from completed predecessor steps' artifacts, including the merged Q6H artifact)"
  - "I10 (raw data provenance / relative-path convention — the future omit-closure artifact uses relative paths in all SHA pins)"
research_log_ref: null  # No research_log entry in this Layer-1 PR per non-batching rule sequence step 1. The omit-closure artifact PR (3 PRs downstream) will produce the closure entry.
---

# Plan: SC2EGSet Step 02_01_99 — Rating Omit-Closure Follow-Up (Outcome A1)

## Scope

This is a **Layer-1 planning-only PR** that authors the planning record for a **new Step lineage segment `02_01_99`** — the *omit-closure follow-up* to Step 02_01_03's Q6H verdict. The future Layer-2 execution PR (planned by this Layer-1 plan) will insert ONE ROADMAP yaml block declaring `02_01_99` immediately after the existing Step 02_01_03 block (approximately line 2523 of `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`; re-grep at Layer-2 dispatch time). The new ROADMAP block will declare the omit-closure follow-up's preconditions, scope, evidence anchors, and gate predicates — it will **NOT** narrow Step 02_01_03's 6-family declaration, **NOT** emit the omit-closure CSV/MD artifact pair, **NOT** add a decision module or test, and **NOT** flip any status YAML.

The 2-file Layer-1 diff: `planning/current_plan.md` + `planning/current_plan.critique.md`. No code, no version bump, no CHANGELOG, no INDEX archive, no status YAML flip, no research_log entry, no spec edit. The future Layer-2 ROADMAP-stub PR is a 4-file diff: `ROADMAP.md` + `pyproject.toml` (3.78.0 → 3.79.0) + `CHANGELOG.md` (new [3.79.0] block) + `planning/INDEX.md` (archive Layer-1, promote Layer-2). Step 02_01_03 remains in_progress with its 6-family declaration byte-unchanged until a separate downstream omit-closure artifact PR (3 PRs forward, following the #238 → #239 → #240 → #241 → #242 precedent) emits the closure artifact and authorises ROADMAP narrowing.

Explicit "no execution" guarantees in this Layer-1 PR:

- NO mutation of the Q6H artifact pair (`02_01_03_q6h_rating_path_decision.{csv,md}`) — Q6H Branch (ii) verdict stands; §15 standby paragraph is preserved byte-unchanged; §17 two-path admission is preserved byte-unchanged.
- NO mutation of the Q6H decision module (`decide_history_rating_path.py`) — `Q6H_PATH_DECISION_RULE`, `Q6H_FIVE_FAMILY_POST_OMIT_SET`, `FALSIFIER_PRIORITY_CHAIN`, and the override falsifier `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15` are preserved byte-unchanged.
- NO re-adjudication of Q5 / Q6F / Q6G / Q6H — all four BINDING verdicts are preserved; the omit-closure follow-up *invokes* the Q6H §15 standby paragraph under explicit Branch (iii) gating, it does NOT replace the Q6H verdict.
- NO ROADMAP edit in this Layer-1 PR (the Layer-2 ROADMAP-stub PR will insert the 02_01_99 block; Step 02_01_03's 6-family declaration at lines approximately 2274-2523 (re-grep at Layer-2 dispatch time) is preserved).
- NO Phase 03 / Step 02_01_04 work; NO baseline modeling; NO feature materialization; NO AoE2; NO thesis chapter prose.

## Problem Statement

PR #251 (merged at master 28bfc89f) closed the Q6H rating-path decision under the canonical Layer-2 default (A9(b)): Branch (ii) reached the verdict; `Q6H_selected_policy = recommendation_only_event_by_event_glicko2`; `materialization_permission = recommendation_only_blocked_pending_phase_03_or_later_decision`. The Q6H artifact §17 (Non-Substitution Statement) explicitly admits two downstream paths for closing Step 02_01_03:

> "Step 02_01_03 closure is deferred to a future PR (Layer-3 materialization or omit-closure follow-up)."

The §15 substantive paragraph was rendered as a "standby paragraph" — meaning the ≥6-sentence reasoning content with ≥3 `PR #249 §X.Y` cross-references exists in the artifact and survives the override falsifier `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15`, but the canonical Layer-2 default A9(b) sets `thesis_pragmatism = FALSE` (because PR #249 chose `recommendation_only_glicko2` and Branch (ii) is satisfied). Branch (iii) `omit_reconstructed_rating_and_unblock_other_five` therefore was NOT reached in the canonical Q6H run. The Branch (iii) preconditions (per the Q6H decision rule, lines 457-481 of `decide_history_rating_path.py`) are:

1. Branches (i) AND (ii) are both blocked.
2. `thesis_pragmatism == TRUE` (must be deliberately elevated; canonical default per A9(b) is FALSE).
3. `substantive_paragraph_ok == TRUE` (≥6 sentences AND ≥3 `PR #249 §X.Y` cross-references in MD §15).
4. `reviewer_signoff == TRUE` (explicit reviewer-adversarial sign-off elevating thesis_pragmatism to TRUE; default FALSE).

The omit-closure follow-up's job is to: (a) re-evaluate Q6H Branch (iii) preconditions with `thesis_pragmatism` elevated to TRUE under explicit reviewer-adversarial sign-off; (b) emit a NEW artifact (separate from Q6H) recording the elevation with full evidence trace; (c) authorise downstream 5-family ROADMAP narrowing of Step 02_01_03 (a SEPARATE later PR after the omit-closure artifact merges); (d) unblock Step 02_01_03 closure under the 5-family scope. This is NOT a re-adjudication of Q6H (the Branch (ii) verdict stands; the standby §15 paragraph is *invoked*, not rewritten); it is a NEW decision artifact that elevates the standby paragraph under explicit Branch (iii) gating.

Branch (iii) is also NOT a "Q6X PR" — the Q6 → Q6F → Q6G → Q6H chain is closed (Q6H is "the terminal rating-path adjudication artifact for Step 02_01_03. After Q6H is merged, no further Q6X PRs are authorised", per `decide_history_rating_path.py` lines 13-16). The omit-closure follow-up is the Layer-3 *closure-side* path admitted by Q6H §17, distinct from both the Q6X adjudication path (closed at Q6H) and from the Layer-3 materialization path (which remains the alternative §17-admitted route).

**Why this corrected Round-2 path resolves the Round-1 HOLD blockers:**

- **R1-B1 (Scope amendment authority unproven)** is resolved by declaring a **NEW Step lineage segment `02_01_99`** rather than amending Step 02_01_03's 6-family declaration in place. Step 02_01_03's existing ROADMAP block (lines 2274-2523) remains byte-unchanged in this PR and in the future Layer-2 ROADMAP-stub PR. The 5-family narrowing question is deferred to a separate downstream PR that lands AFTER the omit-closure artifact merges, at which point the narrowing has both (a) artifact authority (the merged omit-closure decision row) and (b) Branch (iii) authorisation (the Branch (iii) `other_five_families_materialization_permission` literal). No "scope amendment authority" is claimed here — only a new Step is being declared.

- **R1-B2 (Silent Q6 closure)** is resolved by making Branch (iii) gating EXPLICIT in the future omit-closure artifact (the 3-PR-downstream artifact, not this Layer-1 plan and not the Layer-2 ROADMAP-stub). The Branch (iii) preconditions are enumerated as ROADMAP `gate.halt_predicate` clauses in the Step 02_01_99 block; the omit-closure artifact will (a) record the elevation of `thesis_pragmatism` from FALSE to TRUE with reviewer-adversarial sign-off evidence, (b) re-verify the ≥6-sentence + ≥3-cross-reference content of Q6H §15, and (c) emit a new decision row with `Q6H_omit_closure_verdict = omit_reconstructed_rating_and_unblock_other_five`. No "silent closure" — every Branch (iii) precondition is observable as a row field and grep-able as a falsifier name.

- **R1-B3 (Non-batching / lineage defect)** is resolved by adopting the canonical "ROADMAP stub → scaffold → adjudication artifact" lineage ladder (precedent: PR #238 → PR #239 → PR #240/#241 → PR #242 for Step 02_01_03 itself). This Layer-1 PR is sequence step 1 of 9 (ROADMAP stub PLAN only). The future Layer-2 ROADMAP-stub PR (4 files) is still effectively sequence step 1 (only the ROADMAP block is created). A separate downstream PR will scaffold the omit-closure validator notebook (sequence step 2); another will execute and report (step 3); another will emit the artifact (step 7); another will close Step 02_01_03 under the 5-family scope (step 8). At no point does any PR batch ROADMAP + notebook + artifact + next Step in one execution.

**Why A1 (ROADMAP-only stub Layer-1) was chosen over A2 (direct artifact PR) and C (blocked-state note):**

- **A2 rejected** because it collapses 3 PRs into 1, batching ROADMAP-stub + scaffold + adjudication artifact in one execution — re-creating exactly the non-batching violation (R1-B3) that caused the Round-1 HOLD. The repo has NO precedent for an "artifact-first" path for closure follow-ups; every Step 02_01_03 sub-artifact (Q1-Q5 in PR #242, Q5 successor in PR #243, Q6 in PR #245, Q6F in PR #247, Q6G in PR #249, Q6H in PR #251) followed the canonical ladder. Choosing A2 would invent a new lineage pattern without precedent and lose the explicit "ROADMAP-stub adversarial review surface" that PR #238 established.
- **C rejected** because Q6H §17 explicitly admits omit-closure as ONE of the two downstream paths. The omit-closure path IS methodologically admissible — only the Branch (iii) Layer-2 evidence (explicit `thesis_pragmatism = TRUE` elevation under reviewer-adversarial sign-off) is missing, and that evidence is exactly what the future omit-closure artifact PR (3 PRs downstream) will supply. Marking Step 02_01_03 as "blocked until Phase 03" would either (a) over-narrow the §17 admission to a single path (Layer-3 materialization), violating Q6H's two-path admission, or (b) leave Step 02_01_03 effectively unclosable for the duration of Phase 02, blocking Step 02_01_04 (in_game_snapshot tranche). Reserve C only if A1 fails Round-2 adversarial review.

## Assumptions & Unknowns

### Binding assumptions (A1-A20)

- **A1 (BINDING) — Parent SHA pins (10 keys, byte-unchanged from PR #251):**
  - `parent_pr242_csv_sha256`: `f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b`
  - `parent_pr242_md_sha256`: `fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d`
  - `parent_pr243_csv_sha256`: `29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424`
  - `parent_pr243_md_sha256`: `026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719`
  - `parent_pr245_csv_sha256`: `703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0`
  - `parent_pr245_md_sha256`: `7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419`
  - `parent_pr247_csv_sha256`: `249e5591c6505b748fe3d371284a72d8f4620f57dbe9628c908ec2fbf097c8ed`
  - `parent_pr247_md_sha256`: `4b49bee405bf87d4b8920b188e2c38d185ecc077b532d64a8bdd5a90cdf143f2`
  - `parent_pr249_csv_sha256`: `1d9ee22e0523e640181fa0a7a7d2680467a267eefa376fec903f58094118b82f`
  - `parent_pr249_md_sha256`: `8beed3ba6491afb6ba72ee2718b1364c9a2577b26c82237b735d219ccfdc0ea1`
  - **PLUS** the new PR #251 Q6H artifact pins (to be re-verified at Layer-2 execution time by `sha256sum` against master HEAD):
    - `parent_pr251_csv_sha256` (Q6H decision CSV) — computed at Layer-2 dispatch
    - `parent_pr251_md_sha256` (Q6H decision MD) — computed at Layer-2 dispatch
    - `parent_pr251_module_sha256` (Q6H decision module `decide_history_rating_path.py`) — computed at Layer-2 dispatch
- **A2 (BINDING) — Q6H lineage preservation:** The Q6H artifact pair (`02_01_03_q6h_rating_path_decision.{csv,md}`) and the Q6H decision module (`decide_history_rating_path.py`) are READ-ONLY parent provenance for Step 02_01_99. No file under `02_01_03_q6h_*` is mutated in this Layer-1 PR or in the future Layer-2 ROADMAP-stub PR.
- **A3 (BINDING) — No in-place Q6H artifact mutation:** Q6H Branch (ii) verdict (`selected_policy = recommendation_only_event_by_event_glicko2`) stands. Q6H §15 standby paragraph is preserved byte-unchanged. Q6H §17 two-path admission is preserved byte-unchanged. The omit-closure follow-up *invokes* the §15 standby paragraph under Branch (iii) gating, it does not rewrite it.
- **A4 (BINDING) — Branch (iii) precondition enumeration (4 pins):** The future omit-closure artifact (3 PRs downstream) must satisfy ALL of:
  - (a) Branches (i) AND (ii) are both blocked. Operationally, the omit-closure artifact reads Q6H §19's `Branch evaluated: (ii)` and records that Branch (ii) is blocked NOT by Q6H's evidentiary failure but by the explicit Layer-2 election to treat the recommendation_only verdict as insufficient for materialization scope — a methodological choice authorised by the omit-closure follow-up's own scope.
  - (b) `thesis_pragmatism == TRUE` — elevated from the canonical FALSE default via explicit Layer-2 election; the elevation MUST be recorded in the omit-closure artifact's row data with an explicit `thesis_pragmatism_elevation_rationale` column.
  - (c) `substantive_paragraph_ok == TRUE` — re-verifies that Q6H §15 contains ≥6 sentences AND ≥3 `PR #249 §X.Y` cross-references; this is a re-verification of EXISTING content in the byte-unchanged Q6H §15, not new content.
  - (d) `reviewer_signoff == TRUE` — the omit-closure artifact PR's reviewer-adversarial gate must explicitly sign off on the §15 paragraph's admissibility under the elevated `thesis_pragmatism = TRUE` condition; the sign-off is recorded in the omit-closure artifact MD §N (specific section TBD by the omit-closure artifact PR's plan).
- **A5 (BINDING) — 5-family set canonical reference:** The 5 families unblocked under Branch (iii) are exactly the members of `Q6H_FIVE_FAMILY_POST_OMIT_SET` (defined in `decide_history_rating_path.py`; asserted at module load to have exactly 5 entries and to NOT contain `reconstructed_rating`):
  1. `focal_player_history`
  2. `opponent_player_history`
  3. `matchup_history_aggregate`
  4. `cross_region_fragmentation_handling`
  5. `in_game_history_aggregate`
  The omit-closure artifact MUST cite this canonical reference; no alternative 5-family set is admissible. The excluded sixth family is `reconstructed_rating` (CROSS-02-02 §6.2 L241).
- **A6 (BINDING) — No spec mutation:** No CROSS-02-00 / CROSS-02-01 / CROSS-02-02 / CROSS-02-03 spec file is modified by this Layer-1 PR or by the future Layer-2 ROADMAP-stub PR. The omit-closure artifact PR (3 PRs downstream) may NOT mutate specs either; if a spec amendment is required, it is recorded as an Open Question for a separate Category E docs PR.
- **A7 (BINDING) — No status YAML mutation:** No `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, or `PHASE_STATUS.yaml` flip in this Layer-1 PR or in the future Layer-2 ROADMAP-stub PR. The closure flip happens in a separate downstream Step 02_01_03 closure PR that lands AFTER the omit-closure artifact merges.
- **A8 (BINDING) — No research_log entry:** Per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule" sequence step 1, no entry is added to `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` by this Layer-1 PR or by the future Layer-2 ROADMAP-stub PR. The closure entry happens with the closure PR (sequence step 8).
- **A9 (BINDING) — Future Layer-2 version bump:** `3.78.0 → 3.79.0` in `pyproject.toml`, minor bump per `.claude/rules/git-workflow.md` (feat-family). Precedent: PR #239 (the analogous Step 02_01_03 ROADMAP-stub Layer-2) bumped `3.70.1 → 3.71.0`.
- **A10 (BINDING) — No Q6X PR:** Q6 → Q6F → Q6G → Q6H is closed. Step 02_01_99 is NOT a Q6X PR; it is the Layer-3 closure-side path admitted by Q6H §17. The future ROADMAP block MUST NOT contain any "Q6I" / "Q7" / similar Q-token; the block is named "Step 02_01_99 — Omit-closure follow-up to Q6H Branch (iii)" or equivalent (final wording subject to reviewer-adversarial review).
- **A11 (BINDING) — Sub-step token naming:** Per `docs/TAXONOMY.md`, Step numbers are `{PHASE}_{PIPELINE_SECTION}_{STEP}` zero-padded two-digit (the TAXONOMY example `01_01_99` confirms `99` is in-bounds). The canonical sub-step token for this new lineage segment is **`02_01_99`** — taxonomy-conformant within the documented two-digit numeric schema, with `99` conventionally reserved for late-in-section closure follow-ups. **Rationale:** the original Round-2 proposal `02_01_03b` (suffix `b`) was non-precedented in this repo and would have required a separate Category E `docs/TAXONOMY.md` amendment to codify the suffix; reviewer-adversarial Round-2 nit R2-N2 recommended `02_01_99` as the cheaper taxonomy-conformant alternative and the recommendation was accepted in a bounded post-Round-2 correction (2026-05-27). **Branch-name deviation (recorded):** the git branch `feat/sc2egset-02-01-03b-omit-closure-roadmap-stub` was created BEFORE the R2-N2 nit substitution and is retained for git-history continuity (renaming a branch mid-PR would require closing/reopening PR #252 with attendant churn). The on-disk ROADMAP `step_number`, future filenames, and all forward-looking references use the canonical `02_01_99` token; only the branch slug retains the historical `02-01-03b` hyphenated form. The future Layer-2 PR's title and commit message similarly use `02_01_99` as the step token but inherit the same branch slug.
- **A12 (BINDING) — No materialization, no Parquet:** This Layer-1 PR and the future Layer-2 ROADMAP-stub PR materialize NO feature value, write NO Parquet artifact, run NO CROSS-02-01 leakage audit. The omit-closure artifact PR (3 PRs downstream) ALSO materializes no feature value and writes no Parquet — it emits only a CSV/MD decision artifact pair. Materialization remains BLOCKED until a SEPARATE Phase-03 materialization PR (out of scope for this whole 02_01_99 lineage segment).
- **A13 (BINDING) — Round-1 plan supersession:** The Round-1 `planning/current_plan.md` (the rejected direct-narrowing plan) is OVERWRITTEN by this Round-2 plan. The Round-1 critique HOLD is preserved as the first record in `planning/current_plan.critique.md` so the lineage of the Round-1 → Round-2 reset is auditable.
- **A14 (BINDING) — Adversarial round cap:** 3 rounds total on the planning side per `feedback_adversarial_cap_execution.md`. Round 1 was consumed on the rejected direct-narrowing plan. Round 2 begins on this corrected plan. Round 3 is reserved for unresolved BLOCKERs from Round 2.
- **A15 (BINDING) — Adversarial cap symmetry:** The same 3-round cap applies to execution-side review per `feedback_adversarial_cap_execution.md`.
- **A16 (BINDING) — No ROADMAP narrowing in this PR:** Step 02_01_03's 6-family declaration (ROADMAP lines approximately 2274-2523 (re-grep at Layer-2 dispatch time)) remains byte-unchanged in this Layer-1 PR and in the future Layer-2 ROADMAP-stub PR. The narrowing-to-5 question is deferred to a separate downstream PR that lands AFTER the omit-closure artifact merges; at that point the narrowing has explicit Branch (iii) authority.
- **A17 (BINDING) — Plan word budget:** ~800-1200 lines of plan content per the Round-2 prompt's word budget guidance, comparable to the PR #250 plan density (994 lines).
- **A18 (BINDING) — Required `##` sections per `feedback_plan_required_sections.md`:** Scope, Problem Statement, Assumptions & Unknowns, Literature Context, Execution Steps, File Manifest, Gate Condition, Open Questions, Out of scope. The pre-commit hook validates these section headers.
- **A19 (BINDING) — No batching in Layer-2 PR:** The future Layer-2 PR is ROADMAP-stub-only (4 files; no notebook scaffold, no validator, no artifact). The scaffold + validator (sequence step 2) is a SEPARATE successor Layer-1 + Layer-2 PR pair; the omit-closure artifact (sequence step 7) is yet another SEPARATE successor Layer-1 + Layer-2 PR pair. Lineage ladder length for Step 02_01_99: minimum 6 PRs (this Layer-1, Layer-2 ROADMAP-stub, scaffold Layer-1, scaffold Layer-2, artifact Layer-1, artifact Layer-2) plus the eventual Step 02_01_03 closure PR.
- **A20 (BINDING) — Q6H §17 verbatim citation as authority basis:** The Q6H §17 sentence "Step 02_01_03 closure is deferred to a future PR (Layer-3 materialization or omit-closure follow-up)" is the verbatim authority cited in the future Layer-2 ROADMAP block's `question` and `method` fields as the justification for declaring Step 02_01_99. The future omit-closure artifact MD §1 (Summary) MUST also cite this verbatim.

### Unknowns (U1-U5)

- **U1:** The exact line range for the ROADMAP block insertion. Per current ROADMAP at master 28bfc89f, Step 02_01_03 block ends at approximately line 2523 and the next heading is `## Phase 03 — Splitting & Baselines (placeholder)` at approximately line 2527 (line numbers may drift before Layer-2 execution; the Layer-2 executor MUST re-grep `## Phase 03` and insert the new Step 02_01_99 block immediately above it). Resolves at Layer-2 execution time via `grep -n "## Phase 03" ROADMAP.md`.
- **U2 (RESOLVED 2026-05-27 per R2-N2 nit):** The final canonical sub-step token is **`02_01_99`** — taxonomy-conformant per `docs/TAXONOMY.md` `01_01_99` example. The original Round-2 proposal `02_01_03b` was rejected in favour of `02_01_99` in a bounded post-Round-2 correction. See A11 for the full rationale and the recorded branch-name deviation.
- **U3:** Whether the omit-closure artifact (3 PRs downstream) inherits the Q6H 38-column schema (R2.3) verbatim or extends it to record the `thesis_pragmatism_elevation_rationale` and `reviewer_signoff_evidence` columns. Resolves at the omit-closure artifact's own Layer-1 plan time (out of scope here; flagged in OQ2).
- **U4:** Whether the omit-closure artifact PR's reviewer-adversarial sign-off (Branch (iii) precondition (d)) is recorded inline in the artifact MD or in a separate `planning/current_plan.critique.md` review record. Resolves at the omit-closure artifact's own Layer-1 plan time (flagged in OQ3).
- **U5:** Whether the 5-family ROADMAP narrowing (the PR AFTER the omit-closure artifact) edits the existing Step 02_01_03 block in place OR adds a new "Step 02_01_03c — 5-family materialization scope" block. Resolves at that downstream PR's own Layer-1 plan time (flagged in OQ4).

### Acknowledged limitations (L1-L4)

- **L1:** The canonical token `02_01_99` is taxonomy-conformant (within the documented `01-99` two-digit range per `docs/TAXONOMY.md` `01_01_99` example) and requires NO `docs/TAXONOMY.md` amendment. The Round-2 provisional proposal `02_01_03b` (suffix `b`) was non-precedented and was retired in favour of `02_01_99` per R2-N2 nit; the branch slug `feat/sc2egset-02-01-03b-omit-closure-roadmap-stub` is retained for git-history continuity (recorded branch-name deviation; see A11).
- **L2:** The omit-closure follow-up lineage segment is LONG (6+ PRs minimum). This is a consequence of strict non-batching compliance and is acknowledged as a trade-off against execution speed. The trade-off was already implicitly accepted by the 7-PR Step 02_01_03 lineage (#238, #239, #240, #241, #242, #243, #245, #247, #249, #251).
- **L3:** The omit-closure path does NOT resolve the Phase-03 rating decision; the `reconstructed_rating` family remains BLOCKED until a future Phase-03 PR makes the rating decision (either re-binding rating per a future separating anchor or accepting the omission permanently as a thesis-pragmatism decision). The omit-closure follow-up's scope is strictly: unblock the 5 non-rating families for Phase-02 closure under Branch (iii).
- **L4:** This plan does NOT bind a Step 02_01_03 closure date. Closure happens at the LATER of: (a) the omit-closure artifact PR merge, (b) the 5-family ROADMAP narrowing PR merge, (c) a separate STEP_STATUS flip PR merge. The whole closure sequence is a follow-on lineage segment with its own planning cadence.

## Literature Context

### Internal authority (repo-internal artifacts and rules)

- **PR #251 Q6H decision MD §17 (Non-Substitution Statement):** verbatim cited as the authority for declaring Step 02_01_99. The §17 sentence "Step 02_01_03 closure is deferred to a future PR (Layer-3 materialization or omit-closure follow-up)" admits BOTH downstream paths; this plan declares the omit-closure path.
- **PR #251 Q6H decision MD §15 (Thesis-Pragmatism Rationale standby paragraph):** the ≥6-sentence + ≥3-`PR #249 §X.Y`-cross-reference paragraph that is invoked under Branch (iii) when `thesis_pragmatism` is elevated to TRUE.
- **PR #251 Q6H decision module (`decide_history_rating_path.py`) `Q6H_PATH_DECISION_RULE` Branch (iii) literal (lines 457-481):** verbatim cited as the source of the 4 Branch (iii) preconditions.
- **PR #251 Q6H decision module `Q6H_FIVE_FAMILY_POST_OMIT_SET` constant (lines 581-587, asserted to have exactly 5 entries; `reconstructed_rating` MUST NOT appear):** verbatim cited as the canonical 5-family set under Branch (iii).
- **PR #251 Q6H decision module override falsifier `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15` (lines 546-548):** cited as the safeguard that prevents the §15 standby paragraph from being removed by the omit-closure follow-up.
- **PR #249 Q6G implementation-proof MD §15 (rating-period limitations):** evidence anchor for the Branch (iii) thesis-pragmatism elevation rationale (long `rating_period_days = 30` vs short toon span 0.88 d).
- **PR #247 Q6F survey MD §11:** evidence anchor for Glicko-2 vs TrueSkill CI overlap (~0.9% of mid-range; no separating anchor authorised — supports Branch (i) remaining blocked).
- **PR #243 Q5 cross-region adjudication:** evidence anchor for `Q5_selected_policy = sensitivity_indicator_co_registration` (BINDING; preserved verbatim).
- **PR #242 Step 02_01_03 source/anchor/cold-start adjudication:** evidence anchor for the 6-family scope baseline.
- **`.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical work":** the rule that mandates the multi-PR lineage ladder; cited in `gate.halt_predicate` for the future Layer-2 ROADMAP-stub block.
- **`.claude/rules/data-analysis-lineage.md` §"Stop conditions":** cited as the halt-before-artifact gate for the future omit-closure artifact PR.
- **`.claude/scientific-invariants.md` §I3 (temporal discipline), §I7 (no magic numbers / no magic gates), §I9 (research pipeline discipline), §I10 (raw data provenance):** the invariants the future omit-closure artifact MUST uphold.
- **`docs/TAXONOMY.md` Step schema (lines 81-110):** the convention the future Step 02_01_99 ROADMAP block MUST conform to (fenced YAML matching `docs/templates/step_template.yaml`).
- **`docs/PHASES.md`:** the canonical Phase list; Step 02_01_99 is in Pipeline Section `02_01 — Pre-Game vs In-Game Boundary` of Phase 02.

### Precedent 3-PR ladder for Step 02_01_03 (the pattern this plan mirrors)

- **PR #238 (Layer-1 planning):** ROADMAP-stub plan. 2-file diff (`planning/current_plan.md` + `planning/current_plan.critique.md`). Reviewer-adversarial APPROVE-WITH-NITS, 0 blockers, 6 nits.
- **PR #239 (Layer-2 ROADMAP-stub):** Inserts Step 02_01_03 yaml block into ROADMAP. Version bump 3.70.1 → 3.71.0. 6-file diff.
- **PR #240 (Layer-1 planning):** Scaffold + ONE validation module plan. 2-file diff.
- **PR #241 (Layer-2 scaffold):** Scaffold .py + .ipynb + ONE validator + ONE test file. Version bump 3.71.0 → 3.72.0. 7-file diff.
- **PR #242 (Layer-2 adjudication artifact):** First adjudication artifact (8-coupled-decisions Q1-Q8 across 6 tranche-2 families). Version bump 3.72.0 → 3.73.0. 9-file diff.
- Subsequent successors (#243, #245, #247, #249, #251) each followed the same Layer-1-plan → Layer-2-execution pattern.

This plan adopts the same precedent for Step 02_01_99: this Layer-1 PR is the analog of PR #238 (ROADMAP-stub planning); the future Layer-2 PR is the analog of PR #239 (ROADMAP-stub execution); subsequent successor PRs analogous to PR #240/#241 (scaffold) and PR #242 (first artifact) will follow.

### External literature (not load-bearing for this Layer-1 plan)

- **Glickman (2012)** — cited in PR #249 as the source of `rating_period_days = 30` for Glicko-2 batched form. NOT cited in this Layer-1 plan (the omit-closure path does not implement a rating algorithm; the §15 standby paragraph already cites Glickman via the PR #249 lineage). The omit-closure artifact (3 PRs downstream) MAY cite Glickman if its rationale requires it.

## Execution Steps

The Execution Steps below describe the FUTURE Layer-2 ROADMAP-stub execution PR (the one that creates the actual ROADMAP block + version bump + CHANGELOG + INDEX archive). This Layer-1 planning PR itself has NO execution steps in the operational sense — its only "execution" is the act of authoring `planning/current_plan.md` (this file) and dispatching reviewer-adversarial for `planning/current_plan.critique.md`. The Layer-1 PR is a planning artifact, not an execution artifact.

### T01 — Create execution branch and verify pre-execution state

**Objective:** Branch off master HEAD pinned at `28bfc89fae56e88bd4c039077d7971496d5f1b1c`; verify that the Round-1 plan and Round-2 plan are both present in `planning/current_plan.md` (with Round-2 having overwritten Round-1) and that the critique file contains BOTH the Round-1 HOLD record AND the Round-2 reviewer-adversarial APPROVE/HOLD verdict before proceeding.

**Instructions:**
1. Run `git fetch origin master` and verify HEAD SHA is `28bfc89fae56e88bd4c039077d7971496d5f1b1c` (or whatever HEAD is at Layer-2 dispatch time; pin the actual SHA in the PR description).
2. Use the EXISTING branch `feat/sc2egset-02-01-03b-omit-closure-roadmap-stub` (the Layer-1 PR #252 branch; the hyphenated `02-01-03b` slug is the recorded branch-name deviation per A11 / OQ1 resolution — on-disk references use `02_01_99`, only the branch slug retains the historical `02-01-03b` hyphenated form). Run `git checkout feat/sc2egset-02-01-03b-omit-closure-roadmap-stub && git pull --ff-only` (assumes Layer-1 PR #252 has merged to master and the branch is up-to-date). Do NOT rename the branch.
3. Verify `pyproject.toml` version reads `3.78.0` (`grep '^version' pyproject.toml` should output `version = "3.78.0"`).
4. Verify `planning/current_plan.md` contains the Round-2 plan content (this file's content).
5. Verify `planning/current_plan.critique.md` contains the reviewer-adversarial Round-2 verdict (APPROVE or APPROVE-WITH-NITS, 0 blockers). If verdict is HOLD with BLOCKERs, HALT and re-plan per `.claude/rules/data-analysis-lineage.md` §"Stop conditions".
6. Verify NO existing branch `feat/sc2egset-02-01-03b-*` is on `origin/*` (`gh pr list --search 'in:title 02-01-03b' --state all --json number,title` should return `[]` at dispatch time).
7. Verify the Q6H artifact pair exists and is byte-unchanged from PR #251 master merge: `sha256sum src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.{csv,md}` MUST match the PR #251 merge SHAs (re-derive at dispatch time).

**Verification:**
- `git branch --show-current` outputs `feat/sc2egset-02-01-03b-omit-closure-roadmap-stub` (the recorded branch-name deviation; on-disk ROADMAP `step_number` is `02_01_99`).
- `git rev-parse HEAD` outputs `28bfc89fae56e88bd4c039077d7971496d5f1b1c` (or current master).
- All 8 Q6H falsifier-style file integrity checks pass.
- The Round-1 critique HOLD record is preserved in `planning/current_plan.critique.md` (auditable).

**File scope:** None (no file writes in T01; only branch creation and verification).

**Read scope:**
- `planning/current_plan.md` (this Round-2 plan)
- `planning/current_plan.critique.md` (Round-2 critique)
- `pyproject.toml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.csv`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.md`

**Routing:** Sonnet executor sufficient (mechanical verification).

---

### T02 — Insert Step 02_01_99 ROADMAP yaml block

**Objective:** Insert ONE new fenced YAML block declaring Step 02_01_99 immediately after the existing Step 02_01_03 block (currently ends at line ~2523) and immediately before the `## Phase 03 — Splitting & Baselines (placeholder)` heading (currently line ~2527). The block declares the omit-closure follow-up's scope, preconditions, evidence anchors, halt gates, and gate-continuation predicate. The block DOES NOT mutate Step 02_01_03's existing 6-family declaration.

**Instructions:**
1. Re-grep `grep -n "## Phase 03" src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` to determine the current line of the `## Phase 03 — Splitting & Baselines (placeholder)` heading. The insertion point is immediately above this line.
2. Insert the new fenced YAML block. The block MUST follow the schema in `docs/templates/step_template.yaml` (mandatory fields: `step_number`, `name`, `description`, `phase`, `pipeline_section`, `manual_reference`, `dataset`, `question`, `method`, `stratification`, `predecessors`, `notebook_path`, `inputs`, `outputs`, `reproducibility`, `scientific_invariants_applied`, `gate`, `thesis_mapping`, `research_log_entry`).
3. **`step_number`:** `"02_01_99"` (or OQ1-resolved alternative).
4. **`name`:** `"Rating omit-closure follow-up to Step 02_01_03 Q6H Branch (iii) (sc2egset)"`.
5. **`description`:** Must cite Q6H §17 verbatim as authority basis; must enumerate the 4 Branch (iii) preconditions; must declare the 5-family post-omit set verbatim from `Q6H_FIVE_FAMILY_POST_OMIT_SET`; must declare that NO feature value is materialized; must include the non-batching disclaimer "NO ARTIFACT is emitted in this ROADMAP-stub PR — this entry only declares the future step per `.claude/rules/data-analysis-lineage.md` 'Non-batching rule for empirical work' sequence step 1; the omit-closure decision artifact + scaffold + validator are produced by SEPARATE FUTURE PRs (sequence steps 2-7)."
6. **`phase`:** `"02 — Feature Engineering"`.
7. **`pipeline_section`:** `"02_01 — Pre-Game vs In-Game Boundary"`.
8. **`manual_reference`:** `"02_FEATURE_ENGINEERING_MANUAL.md, Section 2"`.
9. **`dataset`:** `"sc2egset"`.
10. **`question`:** Verbatim: `"Under the Q6H §17 two-path admission (omit-closure or Layer-3 materialization), is the omit-closure path methodologically admissible under the 4 Branch (iii) preconditions enumerated in decide_history_rating_path.py lines 457-481, with thesis_pragmatism elevated to TRUE under explicit reviewer-adversarial sign-off, the Q6H §15 standby paragraph re-verified as ≥6 sentences AND ≥3 PR #249 §X.Y cross-references, and Branches (i) and (ii) recorded as blocked for materialization-scope purposes?"`
11. **`method`:** Describe the future omit-closure artifact PR's method: (a) read Q6H artifact pair byte-unchanged; (b) re-verify §15 sentence count (≥6) and cross-reference count (≥3); (c) record explicit `thesis_pragmatism = TRUE` elevation with rationale; (d) obtain explicit reviewer-adversarial sign-off in `planning/current_plan.critique.md`; (e) emit a CSV/MD decision artifact pair recording the elevation and the 5-family unblock; (f) NO Parquet, NO CROSS-02-01 audit, NO feature materialization. Reference the precedent: the lineage ladder mirrors PR #238 → #239 → #240 → #241 → #242 for Step 02_01_03 itself.
12. **`stratification`:** None (omit-closure is a single decision artifact, not a feature aggregation; analogous to PR #251 Q6H stratification = `"per family: dataset_tag = sc2egset; prediction_setting = history_enriched_pre_game; Q6H is not a feature aggregation"`).
13. **`predecessors`:** `"02_01_03"` (the closing of the Q6H chain is the predecessor; the omit-closure follow-up is a successor).
14. **`notebook_path`:** `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_omit_closure_decision.py` (placeholder; final path subject to OQ1 token resolution).
15. **`inputs.duckdb_tables`:** `[]` (no DuckDB tables; this is a metadata-level decision artifact).
16. **`inputs.schema_yamls`:** `[]`.
17. **`inputs.prior_artifacts`:** The 10 Q6H parent SHAs (PR #242/#243/#245/#247/#249) PLUS the 3 new PR #251 Q6H artifacts (CSV/MD/module). Listed verbatim per A1.
18. **`inputs.external_references`:** The internal authority list from §Literature Context above (Q6H §17, §15, decision module Branch (iii) literal, FIVE_FAMILY_POST_OMIT_SET constant, override falsifier).
19. **`outputs.data_artifacts`:** `["(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_omit_closure_decision.csv"]`.
20. **`outputs.report`:** `["(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_omit_closure_decision.md"]`.
21. **`reproducibility`:** Every column in the future omit-closure CSV traces to either the Q6H decision module's Branch (iii) literal or the Q6H §15 paragraph; every count/distribution embedded in the MD must include its derivation. The Branch (iii) elevation rationale must include explicit reviewer-adversarial sign-off SHA. Seed 42 convention.
22. **`scientific_invariants_applied`:** I3, I6, I7, I9, I10 (the 5 invariants from frontmatter `invariants_touched`).
23. **`gate.artifact_check`:** Not applicable to this ROADMAP-stub PR; fires after the future omit-closure artifact PR materializes the CSV+MD pair.
24. **`gate.continue_predicate`:** A future PR may begin Step 02_01_03 closure (separate PR; out of scope for Step 02_01_99 itself) only after Step 02_01_99 has reached its artifact-check, the 5-family ROADMAP narrowing PR has merged (separate downstream PR), and a STEP_STATUS flip PR has merged. Cite the Q6H override falsifier as the safeguard against silent §15 paragraph removal.
25. **`gate.halt_predicate`:** Enumerate the Branch (iii) preconditions as halt clauses: halt before generating the omit-closure artifact if (a) Q6H §15 sentence count drops below 6; (b) Q6H §15 cross-reference count drops below 3; (c) the override falsifier `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15` would fire; (d) `Q6H_FIVE_FAMILY_POST_OMIT_SET` count ≠ 5 or contains `reconstructed_rating`; (e) Q6H artifact pair SHAs do not match PR #251 merge SHAs; (f) reviewer-adversarial sign-off is missing from the omit-closure artifact PR's `planning/current_plan.critique.md`; (g) the omit-closure artifact PR attempts to mutate Q6H artifact bytes (Q5/Q6F/Q6G/Q6H re-adjudication ban); (h) the omit-closure artifact PR attempts a 5-family ROADMAP narrowing (the narrowing is a SEPARATE downstream PR); (i) the omit-closure artifact PR attempts a STEP_STATUS flip (the flip is a SEPARATE downstream PR); (j) the future scaffold attempts to batch ROADMAP + notebook + artifact + next step (non-batching rule).
26. **`thesis_mapping`:** `["Chapter 4 — Data and Methodology > §4.5 Feature engineering plan (sc2egset rating omit-closure decision)"]`.
27. **`research_log_entry`:** Verbatim NON-batching disclaimer: `"NOT REQUIRED FOR THIS ROADMAP-STUB PR per .claude/rules/data-analysis-lineage.md 'Non-batching rule' sequence (step 1 — ROADMAP stub only — produces no research_log entry). Required on the future omit-closure artifact PR per the standard step-completion protocol; entry goes into src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md."`
28. After insertion, validate the new block parses as YAML (e.g., via `python -c "import yaml; yaml.safe_load(open('ROADMAP.md').read().split('```yaml')[N].split('```')[0])"` where N is the block index).

**Verification:**
- `grep -n '^step_number: "02_01_99"' src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` returns exactly 1 line (the new step number).
- `grep -n '^step_number: "02_01_03"' src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` returns exactly 1 line (the existing Step 02_01_03 step number is preserved byte-unchanged).
- `git diff src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` shows ONLY insertions in the new block range (no deletions, no modifications to lines 2274-2523 of the existing Step 02_01_03 block).
- The new block is fenced with triple-backtick yaml/triple-backtick markers and is parseable as YAML.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.md` (for §17 and §15 verbatim citations)
- `src/rts_predict/games/sc2/datasets/sc2egset/decide_history_rating_path.py` (for `Q6H_FIVE_FAMILY_POST_OMIT_SET` and Branch (iii) literal citations)
- `docs/templates/step_template.yaml` (schema reference)

**Routing:** Opus execution required. The block authors a methodologically subtle ROADMAP stub with explicit Branch (iii) precondition enumeration and §17 verbatim citation; Sonnet executor risks mis-paraphrasing the Q6H authority basis or omitting a Branch (iii) precondition. The block content is load-bearing for the reviewer-adversarial Round 1 gate.

---

### T03 — Append CHANGELOG entry

**Objective:** Add a new `[3.79.0]` section to `CHANGELOG.md` recording the Step 02_01_99 ROADMAP stub insertion; move any `[Unreleased]` content into the new versioned section per the `.claude/ml-protocol.md` CHANGELOG conventions.

**Instructions:**
1. Read current `CHANGELOG.md` head; identify the existing `[3.78.0]` entry (PR #251 Q6H Layer-2) and any `[Unreleased]` block.
2. Insert a new `## [3.79.0] — 2026-05-<DD> (PR #<PR_NUMBER>: feat/sc2egset-02-01-03b-omit-closure-roadmap-stub)` section immediately above `[3.78.0]`. `<DD>` is the Layer-2 PR open date; `<PR_NUMBER>` is the Layer-2 PR number resolved at PR creation time.
3. The new section groups changes by `Added` (the Step 02_01_99 ROADMAP block; the Layer-1 planning record archived in planning/INDEX.md; the §17 two-path admission as authority basis; the 4 Branch (iii) preconditions enumerated as halt gates) and `Changed` (none; no existing file other than ROADMAP.md, pyproject.toml, CHANGELOG.md, planning/INDEX.md is modified).
4. Notes block: Verbatim non-batching disclaimer "ROADMAP-stub only per `.claude/rules/data-analysis-lineage.md` §Non-batching rule sequence step 1. No artifact, no notebook, no scaffold, no validator, no test, no module, no status YAML flip, no research_log entry. Step 02_01_03 closure deferred to a separate downstream PR after the omit-closure artifact merges."
5. Move any `[Unreleased]` block content into the new `[3.79.0]` section per `.claude/ml-protocol.md`; leave `[Unreleased]` empty or absent.

**Verification:**
- `grep -n '^## \[3.79.0\]' CHANGELOG.md` returns exactly 1 line.
- `grep -n '^## \[3.78.0\]' CHANGELOG.md` returns exactly 1 line (the existing PR #251 entry is preserved).
- `grep -n '^## \[Unreleased\]' CHANGELOG.md` either returns 0 lines OR returns 1 line with empty content under it (no uncommitted changes).

**File scope:**
- `CHANGELOG.md`

**Read scope:**
- `CHANGELOG.md` (current state)
- `.claude/ml-protocol.md` (CHANGELOG format)

**Routing:** Sonnet executor sufficient (mechanical CHANGELOG insertion).

---

### T04 — Bump version in pyproject.toml

**Objective:** Bump `pyproject.toml` `version` field from `3.78.0` to `3.79.0` per `.claude/rules/git-workflow.md` (minor bump for feat-family branch prefix).

**Instructions:**
1. Read `pyproject.toml`; locate the `version = "3.78.0"` line in the `[project]` (or `[tool.poetry]`) table.
2. Replace with `version = "3.79.0"`.
3. Do NOT modify any other field in `pyproject.toml`; do NOT modify `poetry.lock`.

**Verification:**
- `grep '^version' pyproject.toml` outputs exactly `version = "3.79.0"`.
- `git diff pyproject.toml` shows exactly 1 line changed (the version line); no other diffs.

**File scope:**
- `pyproject.toml`

**Read scope:**
- `pyproject.toml`

**Routing:** Sonnet executor sufficient (mechanical version bump).

---

### T05 — Archive PR #251 in planning/INDEX.md; promote Layer-1 PR to active

**Objective:** Move the PR #251 active row in `planning/INDEX.md` into the archive table (with the actual merge SHA and date); promote the new Layer-1 planning PR `feat/sc2egset-02-01-03b-omit-closure-roadmap-stub` to the active row.

**Instructions:**
1. Read current `planning/INDEX.md`; identify the active row for `feat/sc2egset-02-01-03-q6h-rating-path-decision` (PR #251, currently `draft`).
2. Replace the active row's `draft` status with `merged 2026-05-26 at master 28bfc89f`; move the row into the archive table at the top of the archive section.
3. Insert a new active row for `feat/sc2egset-02-01-03b-omit-closure-roadmap-stub` (Layer-1 planning) at the top of the active table. The active row description: `"Layer-1 planning PR for SC2EGSet Step 02_01_99 — rating omit-closure follow-up to Step 02_01_03 Q6H Branch (iii). Authors planning/current_plan.md + planning/current_plan.critique.md. Round 1 HOLD on rejected direct-narrowing plan (R1-B1 scope amendment authority unproven, R1-B2 silent Q6 closure, R1-B3 non-batching defect); Round 2 reset to ROADMAP-only stub Layer-1 plan per the canonical PR #238 → #239 → #240 → #241 → #242 ladder precedent. 2-file diff. NO artifact, NO module, NO scaffold, NO test, NO source/notebook touch, NO pyproject bump, NO CHANGELOG entry, NO planning/INDEX.md archive, NO status YAML flip, NO research_log entry."`. PR number is the Layer-1 PR number (resolved at PR creation time).
4. Do NOT modify any other archive row.

**Verification:**
- `grep -n 'feat/sc2egset-02-01-03-q6h-rating-path-decision' planning/INDEX.md` returns at most 1 line (the archive row); the previous active row is removed.
- `grep -n 'feat/sc2egset-02-01-03b-omit-closure-roadmap-stub' planning/INDEX.md` returns at least 1 line (the new active row).

**File scope:**
- `planning/INDEX.md`

**Read scope:**
- `planning/INDEX.md` (current state)

**Routing:** Sonnet executor sufficient (mechanical INDEX rewrite).

---

### T06 — Final-verification sweep

**Objective:** Run a final sweep of falsifier-style checks before committing to ensure the 4-file diff is mechanically complete and no out-of-scope file was touched.

**Instructions:**
1. Run `git status --short` and verify EXACTLY 4 files are modified: `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`, `pyproject.toml`, `CHANGELOG.md`, `planning/INDEX.md`. No other file should appear.
2. Run `git diff --stat` and verify the 4 file change counts are reasonable (ROADMAP.md: ~80-120 lines added for the new block; pyproject.toml: 1 line changed; CHANGELOG.md: ~10-15 lines added; planning/INDEX.md: 2 lines moved + 1 line added).
3. Verify the Q6H artifact pair and decision module SHAs are byte-unchanged from PR #251 merge:
   - `sha256sum src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.csv` matches PR #251 merge SHA.
   - `sha256sum src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.md` matches PR #251 merge SHA.
   - `sha256sum src/rts_predict/games/sc2/datasets/sc2egset/decide_history_rating_path.py` matches PR #251 merge SHA.
4. Verify Step 02_01_03's 6-family declaration is byte-unchanged: `grep -c 'reconstructed_rating' src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` should equal the PR #251 merge count (no addition, no removal). The 6-family lines (approximately within ROADMAP lines 2274-2523; re-grep at Layer-2 dispatch time) are NOT modified.
5. Verify NO status YAML mutation: `git diff src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` returns empty.
6. Verify NO research_log mutation: `git diff src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md reports/research_log.md` returns empty.
7. Verify NO spec mutation: `git diff reports/specs/` returns empty.
8. Verify NO source/test/notebook mutation: `git diff src/rts_predict/ tests/ sandbox/` returns empty (except for the ROADMAP.md change which is `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`).
9. Verify pre-commit hooks pass: `git add <files> && git commit --dry-run` (or stage and check `pre-commit run --all-files`). Expected hooks: `feedback_plan_required_sections.md` validator (validates `planning/current_plan.md` ## sections; this Layer-1 PR's plan must have all required ## sections); ruff (no Python files in this PR); mypy (no Python files in this PR).

**Verification:**
- All 9 sweep checks PASS (none of the falsifier-style conditions fire).
- If ANY check fails, HALT and fix before T07.

**File scope:** None (verification only; no file writes).

**Read scope:** All 4 modified files + the Q6H artifact pair + the decision module + the status YAMLs + the research_log + the specs + the source/test/notebook trees (for diff checks).

**Routing:** Sonnet executor sufficient (mechanical verification).

---

### T07 — Reviewer-adversarial Round 1 gate (execution-side)

**Objective:** Dispatch reviewer-adversarial agent for the execution-side Round 1 review of the 4-file Layer-2 ROADMAP-stub diff. Per `feedback_adversarial_cap_execution.md`, the execution-side cap is 3 rounds (symmetric with planning-side). This is execution-side Round 1.

**Instructions:**
1. Dispatch reviewer-adversarial with: `base_ref = 28bfc89fae56e88bd4c039077d7971496d5f1b1c`, `planning_file = planning/current_plan.md`, `critique_file = planning/current_plan.critique.md`, scope = "Layer-2 ROADMAP-stub execution-side adversarial review".
2. Reviewer-adversarial reads: (a) `planning/current_plan.md` (this Round-2 plan); (b) `planning/current_plan.critique.md` (planning-side critique chain); (c) the 4-file Layer-2 diff; (d) the Q6H artifact pair (READ-ONLY; verify SHAs match); (e) the Step 02_01_03 existing ROADMAP block (READ-ONLY; verify byte-unchanged).
3. Reviewer-adversarial produces verdict: APPROVE / APPROVE-WITH-NITS / HOLD-WITH-BLOCKERS.
4. If APPROVE or APPROVE-WITH-NITS (0 blockers): proceed to T08.
5. If HOLD-WITH-BLOCKERS: HALT; record blockers in `planning/current_plan.critique.md` as "Execution-side Round 1 HOLD"; iterate (Round 2 execution-side, max 3 rounds total; if all 3 rounds HOLD, escalate to user).

**Verification:**
- Reviewer-adversarial verdict recorded in `planning/current_plan.critique.md`.
- Verdict is APPROVE or APPROVE-WITH-NITS (0 blockers); otherwise T08 is blocked.

**File scope:**
- `planning/current_plan.critique.md` (reviewer-adversarial appends Round 1 execution-side verdict)

**Read scope:**
- All 4 Layer-2 diff files + Q6H artifact pair + Step 02_01_03 ROADMAP block + planning/current_plan.md + planning/current_plan.critique.md

**Routing:** Reviewer-adversarial agent (Opus).

---

### T08 — Commit, push, create PR

**Objective:** Stage the 4-file diff, commit with a conventional commit message, push the branch, and create the PR.

**Instructions:**
1. Stage the 4 files: `git add src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md pyproject.toml CHANGELOG.md planning/INDEX.md`. Do NOT use `git add -A` or `git add .`.
2. Write the commit message to `.github/tmp/commit.txt` (per `feedback_git_commit_format.md`; heredocs break in zsh). Commit message format:
   ```
   feat(sc2egset): Step 02_01_99 ROADMAP-only stub for rating omit-closure follow-up

   ROADMAP-only stub for Step 02_01_99 — the omit-closure follow-up to Step
   02_01_03's Q6H Branch (iii) admitted under Q6H §17. Inserts a single new
   yaml block declaring the omit-closure follow-up's preconditions, scope,
   evidence anchors, and gate predicates. Does NOT mutate Step 02_01_03's
   6-family declaration. Does NOT emit the omit-closure artifact. Mirrors the
   PR #238 → #239 → #240 → #241 → #242 ladder precedent.

   Version bump 3.78.0 → 3.79.0 (minor; feat-family per .claude/rules/git-workflow.md).
   4-file diff. NO artifact, NO module, NO scaffold, NO test. NO Q6H artifact
   mutation. NO Step 02_01_03 scope narrowing. NO status YAML flip. NO
   research_log entry. Non-batching compliant.

   Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
   ```
3. Commit with `git commit -F .github/tmp/commit.txt`.
4. Push with `git push -u origin feat/sc2egset-02-01-03b-omit-closure-roadmap-stub`. (HALT — `git push` requires explicit user approval per CLAUDE.md permissions. Wait for user `ok` before pushing.)
5. Write the PR body to `.github/tmp/pr.txt` (per `feedback_pr_body_file.md`). PR body must include:
   - **Summary** (3 bullets): authority basis (Q6H §17 two-path admission); 4-file scope; mirrors #238 → #239 → #240 → #241 → #242 ladder precedent.
   - **Resolution of Round-1 HOLD blockers**: R1-B1 / R1-B2 / R1-B3 each addressed by the new Step lineage segment approach.
   - **Test plan** (markdown checklist): pre-commit hooks pass; 4-file diff verified; Q6H artifact pair SHAs byte-unchanged; Step 02_01_03 6-family declaration byte-unchanged; status YAMLs byte-unchanged; research_log byte-unchanged; specs byte-unchanged.
6. Create PR: `gh pr create --title "feat(sc2egset): Step 02_01_99 ROADMAP-only stub for rating omit-closure follow-up" --body-file .github/tmp/pr.txt --base master --head feat/sc2egset-02-01-03b-omit-closure-roadmap-stub`. Save the PR number for T09 final-gate reference. Delete `.github/tmp/pr.txt` per `feedback_pr_body_cleanup.md`.

**Verification:**
- `git log --oneline -1` shows the new commit at HEAD with the conventional commit message.
- `git status` is clean (no untracked or modified files).
- PR is open and visible: `gh pr view <PR_NUMBER> --json url,state,title` returns the new PR's URL, OPEN state, and correct title.
- `.github/tmp/pr.txt` is deleted.

**File scope:**
- `.github/tmp/commit.txt` (transient; auto-deleted by hook or manually after commit)
- `.github/tmp/pr.txt` (transient; deleted after PR creation)

**Read scope:** None (commit/push/PR creation is mechanical).

**Routing:** Sonnet executor sufficient (mechanical commit/push/PR creation; the substantive work is in T01-T07).

---

### T09 — Final gate: re-resolve HEAD; reviewer-adversarial complete-diff review; merge

**Objective:** Per `feedback_final_gate_complete_diff.md`, the final gate MUST review the complete diff to HEAD (not an intermediate commit). If commits land on the PR branch after T07's Round-1 gate, re-dispatch reviewer-adversarial with the new base..HEAD diff.

**Instructions:**
1. `git fetch origin master` and re-resolve `base_ref` to current master HEAD SHA (may have drifted since T01).
2. `git fetch origin feat/sc2egset-02-01-03b-omit-closure-roadmap-stub` and verify the PR branch HEAD is the T08 commit (no intermediate commits added).
3. If new commits landed: re-dispatch reviewer-adversarial with the new base..HEAD diff (Round 2 execution-side; max 3 rounds total). If no new commits: the T07 Round-1 verdict stands.
4. If reviewer-adversarial APPROVE: merge with `gh pr merge <PR_NUMBER> --merge --delete-branch` (squash merge if repo convention; check `gh repo view --json mergeCommitAllowed,squashMergeAllowed`). (HALT — merge requires explicit user approval. Wait for user `ok`.)
5. After merge: verify `git log --oneline master | head -1` shows the new merge commit; verify the new master HEAD SHA is recorded for the next planning round.

**Verification:**
- Reviewer-adversarial Round-2 execution-side verdict (if invoked): APPROVE.
- PR merged to master.
- Branch deleted from origin.
- New master HEAD SHA recorded for the next planning round.

**File scope:** None (merge is a github operation; no file writes).

**Read scope:** Same as T07 (entire base..HEAD diff).

**Routing:** Reviewer-adversarial agent for re-review (if needed); user for merge approval.

---

## File Manifest

### This Layer-1 PR (EXACTLY 2 files)

| File | Action |
|------|--------|
| `planning/current_plan.md` | Rewrite (Round-2 plan; overwrites Round-1) |
| `planning/current_plan.critique.md` | Rewrite (preserves Round-1 HOLD record; adds Round-2 critique) |

### Future Layer-2 PR (EXACTLY 4 files)

| File | Action |
|------|--------|
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | Update (insert Step 02_01_99 YAML block after line ~2523, immediately above `## Phase 03 — Splitting & Baselines (placeholder)`) |
| `pyproject.toml` | Update (version `3.78.0` → `3.79.0`) |
| `CHANGELOG.md` | Update (new `[3.79.0]` section above `[3.78.0]`) |
| `planning/INDEX.md` | Update (archive Layer-1 PR; promote Layer-2 PR to active) |

### Forbidden files (NOT touched in this Layer-1 OR in the future Layer-2 ROADMAP-stub PR)

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.csv` (Q6H artifact — READ ONLY)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.md` (Q6H artifact — READ ONLY; §15 standby paragraph and §17 two-path admission preserved byte-unchanged)
- `src/rts_predict/games/sc2/datasets/sc2egset/decide_history_rating_path.py` (Q6H decision module — READ ONLY; `Q6H_PATH_DECISION_RULE`, `Q6H_FIVE_FAMILY_POST_OMIT_SET`, `FALSIFIER_PRIORITY_CHAIN`, override falsifier preserved byte-unchanged)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6{g,f,5}_*.{csv,md}` (Q6G/Q6F/Q5 artifacts — READ ONLY)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` (status YAML — NO FLIP)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` (status YAML — NO FLIP)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` (status YAML — NO FLIP)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (per-dataset research log — NO ENTRY)
- `reports/research_log.md` (root research log — NO ENTRY)
- `reports/specs/02_00_feature_input_contract.md` (spec — NO MUTATION)
- `reports/specs/02_01_leakage_audit_protocol.md` (spec — NO MUTATION)
- `reports/specs/02_02_feature_engineering_plan.md` (spec — NO MUTATION)
- `reports/specs/02_03_temporal_feature_audit_protocol.md` (spec — NO MUTATION)
- `sandbox/sc2/sc2egset/02_feature_engineering/**` (no scaffold, no notebook in this Layer-2)
- `tests/rts_predict/games/sc2/datasets/sc2egset/**` (no test in this Layer-2)
- `src/rts_predict/games/sc2/datasets/sc2egset/decide_*.py` (no new module in this Layer-2)
- `docs/TAXONOMY.md` (out of scope; if `02_01_99` suffix needs codification, separate Category E docs PR)
- `docs/PHASES.md` (out of scope)
- `.claude/scientific-invariants.md` (out of scope)
- `.claude/rules/data-analysis-lineage.md` (out of scope)
- Any file under `src/rts_predict/games/aoe2/**` (AoE2 — out of scope)
- Any file under `thesis/**` (thesis prose — out of scope)

## Gate Condition

Reviewer-adversarial-runnable predicates for the future Layer-2 ROADMAP-stub PR. Each predicate is binary (PASS/FAIL) and observable from the post-merge master state.

### G-ART — Artifact preservation (Q6H byte-unchanged)

- `sha256sum src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.csv` matches PR #251 merge SHA (re-derived at gate time).
- `sha256sum src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.md` matches PR #251 merge SHA.
- `sha256sum src/rts_predict/games/sc2/datasets/sc2egset/decide_history_rating_path.py` matches PR #251 merge SHA.

### G-METH — Methodological scope discipline

- The new ROADMAP block `step_number` is `"02_01_99"` (or OQ1-resolved alternative); the existing Step 02_01_03 `step_number = "02_01_03"` is preserved byte-unchanged.
- The new ROADMAP block cites Q6H §17 verbatim as authority basis.
- The new ROADMAP block enumerates ALL 4 Branch (iii) preconditions in `gate.halt_predicate` clauses.
- The new ROADMAP block declares the 5-family post-omit set as exactly the members of `Q6H_FIVE_FAMILY_POST_OMIT_SET` (5 entries; `reconstructed_rating` excluded).
- The new ROADMAP block's `description` includes the verbatim non-batching disclaimer.
- Q5 / Q6F / Q6G / Q6H BINDING verdicts are NOT re-adjudicated anywhere in the new block.
- Step 02_01_03's existing 6-family declaration (lines approximately 2274-2523 (re-grep at Layer-2 dispatch time) of the current ROADMAP) is byte-unchanged.

### G-SCHEMA — ROADMAP block schema compliance

- The new YAML block has all 19 mandatory fields per `docs/templates/step_template.yaml`.
- The new YAML block parses as YAML (e.g., via `python -c "import yaml; yaml.safe_load(<block>)"`).
- The new YAML block's `predecessors` field references Step 02_01_03 (the closing of the Q6H chain).
- The new YAML block's `phase` is `"02 — Feature Engineering"` and `pipeline_section` is `"02_01 — Pre-Game vs In-Game Boundary"`.

### G-NOCRP — Non-creep / non-recurrence

- `git diff base..HEAD -- src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` returns empty (NO status YAML flip).
- `git diff base..HEAD -- src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md reports/research_log.md` returns empty (NO research_log entry).
- `git diff base..HEAD -- reports/specs/` returns empty (NO spec mutation).
- `git diff base..HEAD -- src/rts_predict/ tests/ sandbox/` shows ONLY the ROADMAP.md change (no new source, no new test, no new notebook).
- `git diff base..HEAD -- '*.parquet' '*.json'` returns empty (NO Parquet, NO leakage-audit JSON).
- `git diff base..HEAD --name-only` shows EXACTLY 4 files: `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`, `pyproject.toml`, `CHANGELOG.md`, `planning/INDEX.md`.

### G-TEST — Pre-commit hooks pass

- `feedback_plan_required_sections.md` validator passes on `planning/current_plan.md` (this Round-2 plan has all 9 required `##` sections).
- `ruff check src/ tests/` passes (no Python file modified in the Layer-2 PR).
- `mypy src/rts_predict/` passes (no Python file modified).
- `pytest tests/ -v` passes (no test added, no source modified that would change test results).

## Open Questions

- **OQ1 — Sub-step token naming (RESOLVED 2026-05-27 per R2-N2 nit).** The canonical sub-step token is `02_01_99` — taxonomy-conformant per `docs/TAXONOMY.md` (the `01_01_99` example proves `99` is in-bounds). The Round-2 provisional proposal `02_01_03b` was rejected in favour of `02_01_99` because suffix `b` would have required a separate Category E `docs/TAXONOMY.md` amendment. The branch slug `feat/sc2egset-02-01-03b-omit-closure-roadmap-stub` is retained for git-history continuity (recorded branch-name deviation); the on-disk ROADMAP `step_number`, future filenames, and all forward-looking references use `02_01_99`. See A11 for the full rationale.

- **OQ2 — Omit-closure artifact schema (deferred to the artifact's own Layer-1 plan).** The future omit-closure CSV artifact (3 PRs downstream) needs a schema. ALTERNATIVES: (a) inherit the Q6H 38-column schema verbatim; (b) extend the 38-column schema with `thesis_pragmatism_elevation_rationale` and `reviewer_signoff_evidence` columns (40-column schema); (c) define a new minimal schema specific to omit-closure (e.g., 12-15 columns). **Resolves by:** the omit-closure artifact's own Layer-1 plan (3 PRs downstream), via the same planner-science + reviewer-adversarial process. Out of scope for this Layer-1 PR.

- **OQ3 — Reviewer-adversarial sign-off recording.** Branch (iii) precondition (d) requires explicit reviewer-adversarial sign-off elevating `thesis_pragmatism` to TRUE. ALTERNATIVES: (a) record sign-off inline in the omit-closure artifact MD §N (sign-off SHA + date + reviewer agent identity); (b) record sign-off in `planning/current_plan.critique.md` of the omit-closure artifact PR (sign-off lives in the planning layer, artifact MD cites the critique file path). **Resolves by:** the omit-closure artifact's own Layer-1 plan. Out of scope for this Layer-1 PR.

- **OQ4 — 5-family ROADMAP narrowing mechanics.** Once the omit-closure artifact merges, the Step 02_01_03 ROADMAP block MUST be narrowed from 6 families to 5 families (excluding `reconstructed_rating`). ALTERNATIVES: (a) edit the existing Step 02_01_03 block in place (replace `6` → `5`, remove `reconstructed_rating` from the family list at lines approximately 2274-2523 (re-grep at Layer-2 dispatch time), add a citation to the omit-closure artifact); (b) add a new "Step 02_01_03c — 5-family materialization scope" block that supersedes Step 02_01_03's 6-family declaration; the existing 6-family declaration is preserved with a `superseded_by` annotation. **Resolves by:** the 5-family narrowing PR's own Layer-1 plan (4 PRs downstream). Out of scope for this Layer-1 PR.

- **OQ5 — Step 02_01_03 closure-PR sequencing.** Closure of Step 02_01_03 (STEP_STATUS flip to `complete`) happens AFTER both the omit-closure artifact PR and the 5-family narrowing PR merge. ALTERNATIVES: (a) closure happens in the 5-family narrowing PR (bundled status flip); (b) closure happens in a separate dedicated closure PR (analogous to PR #237 for Step 02_01_02). PR #237 precedent strongly favours (b) — closure is governance with a distinct review surface. **Resolves by:** the closure PR's own Layer-1 plan (5 PRs downstream). Out of scope.

- **OQ6 — Phase 03 rating decision deferral.** The Phase-03 rating decision (whether to bind a rating, re-survey rating algorithms, or accept permanent omission) remains BLOCKED until Phase 03 starts. The omit-closure follow-up does NOT resolve the Phase-03 question; it only authorises the Phase-02 5-family unblock. **Resolves by:** Phase 03 work (out of scope for the entire Step 02_01_99 lineage segment).

- **OQ7 — Branch (iii) precondition (a) reframing semantics (R2-N1 telegraph).** Q6H Branch (iii)'s decision rule (`Q6H_PATH_DECISION_RULE` in `decide_history_rating_path.py` lines 457-481) reads literally "IF branches (i) AND (ii) are both blocked AND thesis_pragmatism == TRUE AND substantive_paragraph_ok == TRUE AND reviewer_signoff == TRUE". The decision module's original semantics of "blocked" was *evidence-deficient* (Branch (i) blocked because no new separating anchor exists; Branch (ii) blocked because PR #249's verdict did not stand on its own merits). However, in the future omit-closure artifact PR (3 PRs downstream from this Layer-1), Q6H Branch (ii) actually REACHED a verdict (`recommendation_only_event_by_event_glicko2`) — it is not evidence-deficient. The omit-closure artifact will therefore RECORD Branch (ii) as "blocked NOT by Q6H's evidentiary failure but by the explicit Layer-2 election to treat the `recommendation_only` verdict as insufficient for materialization scope" (i.e., blocked-by-Layer-2-election, not blocked-by-evidence-deficit). **This is a wording/traceability bridge that EXPANDS the decision-rule's literal "blocked" semantics to admit two distinct sub-types (evidence-deficit vs Layer-2-election). It is NOT a new Q6X loop, NOT a Q6H re-adjudication, and NOT a silent rewrite of the decision rule.** The omit-closure artifact MD §N MUST: (a) cite Q6H §17 verbatim as authority basis; (b) record the elevation of `thesis_pragmatism = TRUE` with explicit rationale referencing PR #249 + PR #251 evidence; (c) explicitly distinguish the two "blocked" sub-types in a dedicated section; (d) note the override falsifier `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15` preserves Q6H §15 byte-unchanged; (e) include a "Branch (iii) precondition (a) interpretation" sub-section explaining the wording/traceability bridge. **Resolves by:** the omit-closure artifact's own Layer-1 plan (3 PRs downstream); the planner-science round for that PR is responsible for the precise wording. Flagged here per R2-N1 so the future planner-science round is on notice.

## Out of scope

- **Phase 03 work** — baseline modeling, temporal splitting, baseline hierarchy (Dummy → Elo → LR), all deferred. Phase 03 may not begin until Phase 02 has all 8 pipeline sections complete; currently only 02_01 is in_progress (1 of 8) and only 02_01_01 + 02_01_02 are complete (2 steps in section 02_01). Phase 02 closure is many PRs away.
- **Step 02_01_04 (in_game_snapshot tranche)** — the in-game-snapshot feature families (11 families bound to tracker events) are deferred to a separate Step 02_01_04 lineage segment after Step 02_01_03 closes.
- **Step 02_01_03 closure (STEP_STATUS flip)** — handled by a separate downstream closure PR after both the omit-closure artifact PR and the 5-family ROADMAP narrowing PR merge. Out of scope for this Layer-1 PR and for the future Layer-2 ROADMAP-stub PR.
- **5-family ROADMAP narrowing** — handled by a separate downstream PR that lands AFTER the omit-closure artifact merges. The narrowing has explicit Branch (iii) authority once the omit-closure artifact merges; before then, Step 02_01_03's 6-family declaration is preserved.
- **Omit-closure decision artifact (CSV/MD pair)** — handled by a separate downstream Layer-1 + Layer-2 PR pair (analogous to the PR #240/#241 scaffold + PR #242 first-artifact precedent for Step 02_01_03 itself). Out of scope for this Layer-1 ROADMAP-stub-planning PR.
- **Scaffold + validator notebook for omit-closure decision** — handled by a separate downstream Layer-1 + Layer-2 PR pair (analogous to PR #240/#241 for Step 02_01_03). Out of scope.
- **CROSS-02-01 post-materialization leakage audit** — the omit-closure follow-up materializes NO feature value; there is no Parquet to audit; CROSS-02-01 audit does NOT apply. The CROSS-02-01 audit applies only to the eventual Phase-03 materialization PR (out of scope for the entire Step 02_01_99 lineage segment).
- **Q5 / Q6F / Q6G / Q6H re-adjudication** — Q5/Q6F/Q6G/Q6H are BINDING. The omit-closure follow-up *invokes* the Q6H §15 standby paragraph under Branch (iii) gating; it does NOT replace, rewrite, or re-adjudicate any of the four bound verdicts. The drift falsifiers `q6h_q5_re_adjudication_drift`, `q6h_q6f_re_adjudication_drift`, `q6h_q6g_re_adjudication_drift` enforce this for Q6H; analogous falsifiers in the omit-closure artifact (3 PRs downstream) enforce non-drift for Q6H itself.
- **Q6X PR (Q6I, Q6J, …)** — Q6 → Q6F → Q6G → Q6H is closed. Step 02_01_99 is NOT a Q6X PR; it is the Layer-3 closure-side path admitted by Q6H §17.
- **AoE2 work** — the entire Step 02_01_99 lineage segment is SC2EGSet-only. AoE2 history-enriched pre-game feature work has its own ROADMAP (under `src/rts_predict/games/aoe2/datasets/<dataset>/reports/`) and is on its own planning timeline.
- **Thesis chapter prose** — Step 02_01_99 is a methodology decision artifact; it does NOT write or edit any thesis chapter file (`thesis/chapters/*.tex` or `thesis/chapters/*.md`). The chapter 4 §4.5 mapping is for future thesis-writing PRs.
- **STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS flips** — out of scope for this Layer-1 PR and for the future Layer-2 ROADMAP-stub PR. Closure flips are separate downstream PRs.
- **Research log entries** — out of scope for this Layer-1 PR and for the future Layer-2 ROADMAP-stub PR per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule" sequence step 1. The closure entry happens with the closure PR.
- **Spec mutations (CROSS-02-00, CROSS-02-01, CROSS-02-02, CROSS-02-03)** — all 4 specs preserved byte-unchanged. If a spec amendment is required by the omit-closure follow-up's findings, it is a SEPARATE Category E docs PR.
- **`docs/TAXONOMY.md` amendment for sub-step suffix codification** — if OQ1 resolves to a non-precedented suffix and the user wants to codify it, this is a SEPARATE Category E docs PR (out of scope for this Layer-1 PR).
- **Direct 5-family ROADMAP narrowing in this PR (the Round-1 plan's defect)** — REJECTED in Round 2 per R1-B1 / R1-B2 / R1-B3 resolution. The narrowing is a SEPARATE downstream PR with explicit Branch (iii) authority post-omit-closure-merge.
- **Direct omit-closure artifact emission in this PR (the A2 alternative)** — REJECTED in Round 2 per non-batching rule R1-B3 resolution. The artifact is a SEPARATE downstream PR.
- **Blocked-state note on Step 02_01_03 (the C alternative)** — REJECTED in Round 2 per Q6H §17 two-path admission; the omit-closure path IS methodologically admissible.

---

## Critique gate notice

This is a Category A plan. Adversarial critique is required before execution begins. The parent session MUST dispatch reviewer-adversarial to produce `planning/current_plan.critique.md` (Round 2 review). The Round 1 HOLD record (R1-B1, R1-B2, R1-B3) is preserved in the critique file as the first record so the Round-1 → Round-2 reset lineage is auditable.

Per `feedback_adversarial_cap_execution.md`, the 3-round adversarial cap is symmetric — Round 1 was consumed on the rejected direct-narrowing plan; Round 2 begins on this corrected plan; Round 3 is reserved for unresolved BLOCKERs.

For execution-side review (after T08 commits the Layer-2 diff), the same 3-round cap applies. T07 dispatches execution-side Round 1; if HOLD, iterate up to Round 3.
