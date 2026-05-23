---
category: A
branch: chore/sc2egset-02-01-02-formal-closure
base_ref: 39298c0afd3a23bfbd4603415314af784a672952
date: 2026-05-24
planner_model: claude-opus-4-7[1m]
dataset: sc2egset
phase: "02"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
step: "02_01_02 (U2.B formal closure planning)"
non_batching_sequence_position: "Step 8 of 9 (research_log / STEP_STATUS / manifest closure) — emitted as a separate planning unit per merged Layer-1 plan §OQ1 U2.B and PR #229 → PR #230 precedent."
critique_required_before_execution: true
critique_reviewer: reviewer-adversarial
gate_reviewer: "reviewer-adversarial (Category A pre-execution gate)"
planning_pr: "PR #237"
source_artifacts:
  # PR #236 evidence (materialization + first non-vacuous audit; closure-justifying inputs)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.md
  - src/rts_predict/games/sc2/datasets/sc2egset/materialize_pre_game_features.py
  - tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_pre_game_features.py
  - sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.py
  # Frozen Layer-1 + Layer-2 lineage authorising U2.B
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json
  # Specs (provenance bond targets)
  - reports/specs/02_00_feature_input_contract.md  # CROSS-02-00-v3.0.1
  - reports/specs/02_01_leakage_audit_protocol.md  # CROSS-02-01-v1.0.1 §5 gate condition
  - reports/specs/02_02_feature_engineering_plan.md  # CROSS-02-02-v1.0.1
  - reports/specs/02_03_temporal_feature_audit_protocol.md  # CROSS-02-03-v1.0.1 §6.1 anchor classification
  # Closure-relevant status YAMLs (read; one is mutated; two stay byte-unchanged)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml
  # Dataset ROADMAP (the 02_01_02 stub; cited verbatim in §Literature Context; NOT edited)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md  # lines 2099–2300 contain the 02_01_02 stub
  # Dataset research log (target of T02 closure entry; baseline state of PR #236 entry preserved)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
  # Closure precedent (PR #229 → PR #230 evidence-then-closure pattern)
  - CHANGELOG.md  # [3.64.0] (PR #229 evidence) and [3.65.0] (PR #230 closure)
  # Methodology / rule sources
  - .claude/scientific-invariants.md
  - .claude/ml-protocol.md
  - .claude/rules/data-analysis-lineage.md
  - .claude/rules/git-workflow.md
  - planning/INDEX.md
  - docs/PHASES.md
  - docs/TAXONOMY.md
---

# Plan — SC2EGSet Step 02_01_02 U2.B formal closure (Category A)

## Scope

Category A — Phase work, planning-only formal-closure unit. Phase 02 → Pipeline Section 02_01 → Step `02_01_02` (U2.B formal closure planning). This planning unit is non-empirical: it specifies a future execution PR that flips ONE row in `STEP_STATUS.yaml` and appends ONE closure entry to the dataset's `research_log.md`. No artifact, no source, no test, no notebook, no spec, no ROADMAP body, no cleaning-layer YAML is touched in either layer.

**Branch (proposed).** `chore/sc2egset-02-01-02-formal-closure` from master @ `39298c0afd3a23bfbd4603415314af784a672952` (pyproject `3.70.0`; PR #236 merged 2026-05-23 at `39298c0a`). The `chore/` prefix follows the closure precedent shape (PR #229 → PR #230 closure used `feat/` historically because the closure carried new on-disk artifacts; the present closure carries NO new on-disk artifact under U2.B, so the diff is governance-only — see §Open Questions OQ-Branch for the chore/ vs feat/ adjudication ask).

**Layer-1 diff for THIS planning PR = exactly 2 files:** `planning/current_plan.md` and `planning/current_plan.critique.md`. The parent (orchestrator) must clear any stale `planning/current_plan.md`, `planning/current_plan.critique.md`, and `planning/current_plan.critique_resolution.md` before `Write`.

**Layer-2 diff for the FUTURE closure execution PR = 6 files** (planning files persist into the closure PR's own diff per repo convention; see §File Manifest). NO `PIPELINE_SECTION_STATUS.yaml` flip; NO `PHASE_STATUS.yaml` flip; NO ROADMAP body edit; NO spec / cleaning-layer YAML edit; NO root `reports/research_log.md` edit; NO Phase-03 file; NO Step `02_01_03+` file; NO new artifact / source / test / notebook.

**Pointer to the future execution-PR scope.** The Layer-2 PR is dispatched after this Layer-1 planning PR merges and after reviewer-adversarial returns APPROVE or APPROVE-WITH-NITS (zero blockers). The Layer-2 plan body is THIS document (the closure-execution plan is mechanical enough that a single planner-science round captures it; no separate Layer-2 plan is needed — Layer-2 executor reads this current_plan.md directly per planning/INDEX.md Agent routing table).

**Out of scope** (deferred to later sessions):
- The 6 `history_enriched_pre_game` families (Steps `02_01_03+`); Phase-03 hold-out anchor binding; tracker-derived in-game families (Steps `02_01_04+`); Phase 03 splits.
- Any spec / cleaning-layer YAML / ROADMAP body edit. PR #234's MD §8 proposed CROSS-02-02 §6.1 amendment remains a future Category E spec-only PR target.
- Any AoE2 work, any thesis chapter prose, any docs / `.claude/` edit.
- Re-running the CROSS-02-01 post-materialization audit. PR #236's audit JSON+MD already satisfies §5(a/b/c); regeneration is forbidden by the lineage rule (artifact is current).

## Problem Statement

A separate closure PR exists because the non-batching rule in `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical work" enumerates steps 1–9 of an empirical Step, with step 8 explicitly being "Then research_log / STEP_STATUS / manifest" — a distinct increment from step 7 ("Only after all validation modules pass, generate artifacts"). The repository has already adopted this separation as a binding convention via the PR #229 → PR #230 precedent for Step `02_01_01`:

- PR #229 (`feat/sc2egset-02-01-01-section10-audit-persistence`, merged 2026-05-21 at `a14dc547`, CHANGELOG `[3.64.0]`): persisted §10 verdict-audit evidence (CSV+MD); explicitly recorded `closure_status: still_open` and froze status YAMLs (`This PR persists evidence but does NOT close Step 02_01_01.`).
- PR #230 (`feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit`, merged 2026-05-22 at `0c45c490`, CHANGELOG `[3.65.0]`): emitted the zero-materialization CROSS-02-01 artifact pair AND added `02_01_01: complete` to `STEP_STATUS.yaml`; recorded `closure_status: closed`; flipped `PIPELINE_SECTION_STATUS` and `PHASE_STATUS` mechanically.

The merged Layer-1 plan for PR #236 (`planning/current_plan.md` on master before this turn) explicitly selected option **U2.B (separate closure PR)** at its §Open Questions OQ1 (lines 644–645 of that historical plan): closure rides a separate, later PR mirroring the PR #229 → PR #230 evidence-then-closure precedent. PR #236's CHANGELOG `[3.70.0] Notes` re-asserts the same: `Step 02_01_02 closure is deferred to a separate U2.B closure PR per the merged Layer-1 plan`; PR #236's research_log entry carries `closure_status: still_open` and `materialization_state: materialized` with the explicit clause `Step 02_01_02 is NOT closed by this PR.`.

This planning unit specifies the U2.B closure PR. Mechanically: PR #236 has already cleared the CROSS-02-01-v1.0.1 §5 gate condition (`verdict = PASS`, `len(features_audited) = 7`, JSON+MD present at the spec-named path `02_01_02/leakage_audit_sc2egset.{json,md}`). The closure PR's sole substantive change is to record this fact in the status-chain by adding `02_01_02: complete` to `STEP_STATUS.yaml` and writing the per-dataset closure entry to `research_log.md`. Every other repo path remains byte-unchanged.

The reviewer-adversarial Layer-1 critique gate evaluates the closure PR's *governance* — does the closure overclaim any methodological scope it should not? — rather than its empirical content (which is the unchanged PR #236 evidence).

## Assumptions & Unknowns

- **Assumption (PR #236 evidence frozen).** All PR #236 artifacts are taken as authoritative inputs and remain byte-unchanged by the future closure PR:
  - Audit JSON `verdict = PASS`, `len(features_audited) = 7`, `features_audited = ["focal_race", "opponent_race", "race_pair", "map_type", "patch_version", "focal_is_mmr_missing", "opponent_is_mmr_missing"]`, `projected_context_columns = ["started_at"]`, `projected_identity_columns = ["focal_match_id", "focal_player", "opponent_player"]`, `audit_pr = "PR #236"`, the examiner-clarity sentence verbatim in `notes`.
  - Audit MD carries the 8 spec sections from CROSS-02-01 §3 (top non-overclaim disclaimer, materialization SQL + source-binding justification, sanity-check SQL, cutoff structural check + anchor-classification reiteration, POST-GAME token absence, normalization fit-scope, reference-window assertion, non-substitution + lineage).
  - Feature Parquet at `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet` = 44,418 rows × 11 cols (= 3 identity + 1 context anchor + 7 audited PRE_GAME features).
- **Assumption (`PIPELINE_SECTION_STATUS.yaml` byte-unchanged).** Per the YAML header rule at `STEP_STATUS.yaml:4-8` and `PIPELINE_SECTION_STATUS.yaml:10-13` ("Pipeline section is complete when ALL its steps are complete"), adding `02_01_02: complete` to `STEP_STATUS.yaml` does NOT re-derive `02_01` to a different status: both `02_01_01` and `02_01_02` will be `complete`, so the derived value remains `complete`. The current line `"02_01": ... status: complete` (lines 51–54) is therefore byte-identical post-closure. See §Status derivation analysis below for the full step-by-step.
- **Assumption (`PHASE_STATUS.yaml` byte-unchanged).** Phase 02 has 8 canonical Pipeline Sections per `docs/PHASES.md` lines 112–124 (`02_01` through `02_08`). After this closure, only `02_01` is complete; `02_02 … 02_08` are not started. The derivation rule `Phase is complete when ALL its pipeline sections are complete; Phase is in_progress when ANY pipeline section is in_progress or complete` (`PIPELINE_SECTION_STATUS.yaml:5-8`) yields Phase 02 = `in_progress` — already the current value (line 24). Byte-unchanged.
- **Assumption (ROADMAP body byte-unchanged).** The Step `02_01_02` stub block (lines 2099–2300 of `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`) was committed in PR #232 and remains intact through PR #233, PR #234, PR #235, PR #236. The closure PR does NOT edit it. Closure is a *status-chain* claim recorded in `STEP_STATUS.yaml`, not a ROADMAP-body re-authoring claim.
- **Assumption (root `reports/research_log.md` untouched).** Per `.claude/ml-protocol.md` lines 51–54, the root research log is for CROSS entries only (multi-dataset/multi-game decisions). The 02_01_02 closure is a single-dataset status flip and is recorded ONLY in the per-dataset research log. PR #230 set this precedent explicitly (`per-dataset closure is a single-dataset status flip, not a cross-dataset decision, per .claude/ml-protocol.md lines 51-54`).
- **Assumption (no Phase-03 work; no Step `02_01_03` start).** This closure does NOT authorise Phase 03 work; it does NOT start Step `02_01_03`. Step `02_01_02` closure is the *necessary* gate for a future planner-science session to design Step `02_01_03+` (history_enriched_pre_game tranche), but the closure itself authorises nothing beyond the YAML row + research_log entry.
- **Assumption (PR #236 research_log entry untouched).** The current top entry in `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (the PR #236 entry with `closure_status: still_open`, `materialization_state: materialized`, `leakage_audit_state: post_materialization_pass`) is a historical record. The closure PR appends a NEW reverse-chronological top entry above it; the PR #236 entry remains byte-identical. The closure-entry baseline (still_open) is preserved as on-disk evidence of the deliberate non-closure decision in PR #236.
- **Assumption (version policy).** Patch bump `3.70.0 → 3.70.1` per `.claude/rules/git-workflow.md` line 25 (`patch for fix/test/chore`). The closure PR has branch prefix `chore/` (governance-only; no new artifact / source / test). PR #230 used a minor bump (`3.64.0 → 3.65.0`) because it created two NEW on-disk audit artifacts under `02_01_01/`; the present closure creates ZERO new on-disk artifacts (the audit JSON+MD at `02_01_02/` already exist on master via PR #236). Patch is the correct increment.
- **Assumption (planning files persist into the closure PR's tracked diff).** Per repository convention (PR #229 CHANGELOG `[3.64.0]` Changed: `planning/current_plan.md + planning/current_plan.critique.md — already committed in PR #229`), the planning files do NOT clear off master between PRs. They are overwritten by the next planner-science round's Layer-1 PR. The closure PR carries them in its own diff because it shares the same branch as this Layer-1 PR (`chore/sc2egset-02-01-02-formal-closure`). See §File Manifest for the explicit row.

### Unknowns

- **U-Branch (branch-name category dispute).** Should the closure PR use `chore/` (governance / no new artifact) or `feat/` (Phase 02 / Cat A)? Default proposed = **`chore/`**. Justification: `.claude/rules/git-workflow.md` ties branch prefix to version-bump category (`minor for feat/refactor/docs, patch for fix/test/chore`); the closure has no new artifact / source / test and is patch-class. PR #230 used `feat/` because it created new artifact files; the present closure does NOT, so the analogue is `chore/`. Reviewer-adversarial may pick `feat/` if it judges the underlying Cat A semantic to outweigh the git-workflow alignment. If reviewer-adversarial requires `feat/`, the version bump becomes `3.70.0 → 3.71.0` (minor) and the CHANGELOG block name is `[3.71.0]`. Either outcome is internally consistent; default is `chore/` + patch `3.70.1`.
- **U-Date (`completed_at` date convention).** Three candidate ISO dates: (i) `"2026-05-23"` (PR #236 audit date; the date the closure-justifying evidence was created); (ii) `"2026-05-24"` (today's date; the date the closure-PR plan is authored); (iii) the closure-PR's eventual merge date (unknown at planning time; would require a post-merge YAML edit). Default proposed = **(i) `"2026-05-23"`**. Justification: PR #230's `02_01_01` row was set with `completed_at: "2026-04-19"`, which was the date of the underlying §10 audit evidence — NOT the PR #230 merge date (2026-05-22). The repo's existing `completed_at` values throughout `STEP_STATUS.yaml` track the evidence date, not the YAML-flip date. PR #236's audit JSON has `audit_date: "2026-05-23"` and the audit JSON is the closure-justifying evidence; therefore `completed_at: "2026-05-23"` is the consistent choice. Reviewer-adversarial may demand (ii) or (iii); recommend (i).
- **U-PlanningBranchScope (does the planning-files row in the future closure PR's manifest reuse the same branch or open a new chore branch?).** Default proposed = **reuse the same branch** (`chore/sc2egset-02-01-02-formal-closure`). The Layer-1 planning PR and the Layer-2 execution PR share one branch; planning files are committed in Layer 1 and persist into Layer 2's tracked diff (standard repo pattern, confirmed by PR #229's CHANGELOG `[3.64.0]` Changed entry). No new branch is opened for execution. If reviewer-adversarial prefers two branches (Layer-1 planning branch + Layer-2 execution branch, with the planning files moved across), that's a heavier workflow with no precedent for this kind of governance-only closure; default declines that option.

### Documented (no longer UNKNOWN)

- **DOCUMENTED-U2.B-Selected.** The U2.A vs U2.B adjudication was already resolved in favour of U2.B by the merged Layer-1 plan §Open Questions OQ1 (lines 644–645 of the historical PR #235 plan body). PR #236 honoured U2.B (`closure_status: still_open`). This planning unit is the U2.B closure round; it is no longer an open question.
- **DOCUMENTED-Phase03-Not-Started.** Phase 03 remains `not_started` (`PHASE_STATUS.yaml:25-27`). The closure PR does NOT authorise Phase 03. Step `02_01_03` planning may begin after this closure PR merges (likely yes per the same pattern as 02_01_01 → 02_01_02), but is itself a separate planner-science round and is out of scope here.
- **DOCUMENTED-Audit-Date-Convention.** PR #230 used the evidence date (2026-04-19) not the merge date (2026-05-22) for `completed_at`. The same convention applies here.

### Deferred (NOT this PR; NOT the closure execution PR)

- Step `02_01_03+` (history_enriched_pre_game tranche; 6 families); Step `02_01_04+` (in_game_snapshot tranche; 11 families); Phase 03 (and any 02_02..02_08) work; AoE2 work; thesis chapter prose.
- CROSS-02-02 §6.1 minor amendment proposed in PR #234 MD §8 — remains a future Category E spec-only PR target. Not applied by closure.

## Literature Context

This unit is a planning-only governance closure; it introduces no empirical or literature claim and asserts no new finding. Governing repo sources cited verbatim or by anchor:

- **Scientific invariants** (`.claude/scientific-invariants.md`).
  - **I9 (research pipeline discipline).** Lines 261–296 — `A step's conclusions must derive only from its own artifacts and all prior steps' artifacts.` The closure entry's conclusions are bounded to PR #236 artifacts (the Parquet, the audit JSON+MD), the registry CSV from PR #216, and the PR #229–#234 lineage — all on disk; all lower-numbered. No future-step knowledge is referenced. No content-level claim beyond what PR #236 already records.
  - **I3, I5, I7, I10** are vacuously satisfied because this PR mutates no data, no feature code, no SQL. They are recorded for completeness.
- **ML protocol** (`.claude/ml-protocol.md`).
  - Lines 51–54 (per-dataset vs root research_log discipline): `Per-dataset logs live at src/rts_predict/games/<game>/datasets/<dataset>/reports/research_log.md. Write all dataset-specific experiment entries there — never to the root reports/research_log.md.` This closure is a single-dataset status flip → per-dataset only.
  - Lines 56–60 (research_log entry template required sections for Category A): `What, Why, How (reproducibility), Findings, Decisions taken, Decisions deferred, Thesis mapping, Open questions / follow-ups. Optional sections: What this means, Acknowledged trade-offs.` The closure entry uses every required section + the optional `What this means` and `Scope notes`.
- **CROSS-02-01-v1.0.1 §5 gate condition** (`reports/specs/02_01_leakage_audit_protocol.md` lines 137–147):
  > Pipeline Section 02_01 exit requires all three of the following conditions:
  > (a) Every feature column materialized in 02_01 appears in `features_audited` in the audit artifact.
  > (b) `verdict = "PASS"` in the audit artifact JSON.
  > (c) Both the JSON artifact and the sibling Markdown report are present at the prescribed path (`reports/artifacts/02_01_*/leakage_audit_<dataset>.json` and `.md`).
  > A missing audit artifact OR `verdict != "PASS"` blocks 02_01 exit.

  PR #236 cleared all three: (a) `features_audited` contains all 7 PRE_GAME feature columns materialized in PR #236 (no other features were materialized in PR #236); (b) `verdict = PASS`; (c) both files present at `02_01_02/leakage_audit_sc2egset.{json,md}`.
- **ROADMAP `continue_predicate` for Step 02_01_02** (`src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` lines 2240–2249, quoted verbatim):
  > A future PR may begin Step 02_01_03 (the next 02_01 materialization step -- history_enriched_pre_game tranche) only after this Step 02_01_02 has reached its artifact-check at a future PR, the CROSS-02-01-v1.0.1 post-materialization audit has returned a NON-vacuous PASS (future_leak_count = 0, post_game_token_violations = 0 over a non-empty features_audited), and a per-family CROSS-02-03-v1.0.1 section 10 verdict consistent with the materialized columns is recorded. The §10 design-time verdict audit (PR #229) is a distinct artifact and does NOT substitute for this post-materialization CROSS-02-01 audit (PR #230 evidence remains distinct from PR #229 evidence).

  Three clauses parsed:
  - **Clause-A (artifact-check predicate at the materialization PR).** Cleared by PR #236 (`reports/artifacts/02_01_02/leakage_audit_sc2egset.{json,md}` present at the spec-named path; the audit JSON has `features_audited != []` with `verdict = PASS`; the Parquet exists at the planned path).
  - **Clause-B (non-vacuous PASS).** Cleared by PR #236 (`future_leak_count = 0`, `post_game_token_violations = 0`, `features_audited` carries 7 non-empty members).
  - **Clause-C (per-family §10 verdict consistent with the materialized columns).** Cleared by PR #229 §10 evidence-audit CSV+MD persisting design-time verdicts for all 26 registry rows including all 5 tranche-1 families (rows 2–6); PR #236 audit MD §2 records the registry-cell upstream-source → MFC cleaned-view binding verbatim, and the materialized columns map directly to those 5 registry rows.

  All three clauses on disk; the artifact-check predicate (the leftmost subject of the ROADMAP stub) is satisfied. This is the on-disk justification for adding `02_01_02: complete` to `STEP_STATUS.yaml`.
- **PR #229 → PR #230 closure precedent** (`CHANGELOG.md` [3.64.0] and [3.65.0]):
  - PR #229: evidence persistence; `closure_status: still_open`; status YAMLs frozen.
  - PR #230: closure-only PR; `closure_status: closed`; status YAMLs flipped; new closure entry in dataset research_log; pyproject + CHANGELOG bumped. `Step 02_01_01 closure at the catalog-only layer requires no notebook; emitting one would falsify the lineage.` (PR #230 CHANGELOG Notes).
- **Lineage rules** (`.claude/rules/data-analysis-lineage.md` Non-batching rule for empirical work, sequence steps 1–9):
  > 1. ROADMAP stub only.  2. Notebook scaffold + one validation module.  3. Execute and report.  4. User review.  5. Commit.  6. Next validation module.  7. Only after all validation modules pass, generate artifacts.  8. Then research_log / STEP_STATUS / manifest.  9. Then reviewer-deep.

  PR #232 = step 1; PR #233 = step 2; PR #234 = step 3 (adjudication); PR #235 = step 4 + 5 (user review of PR #234 + commit of Layer-1 plan); PR #236 = steps 6 + 7 (materialization execution = next validator + artifact generation, batched as Layer-2 per the Layer-1 plan's authorisation). This closure PR = step 8 (research_log / STEP_STATUS / manifest). Step 9 (reviewer-deep) follows on the closure PR's merge.
- **Git workflow** (`.claude/rules/git-workflow.md` lines 11, 25):
  > Branches: `feat/` `fix/` `refactor/` `docs/` `test/` `chore/` — conventional prefixes.
  > Version: minor for feat/refactor/docs, patch for fix/test/chore.

  `chore/` + patch is the consistent choice for a governance-only closure with no new artifact / source / test.
- **Planning index** (`planning/INDEX.md`).
  - Current Active line = PR #236 (`feat/sc2egset-02-01-02-pre-game-materialization-execution`). To be archived at master merge commit `39298c0afd3a23bfbd4603415314af784a672952` with the PR #236 summary already in its CHANGELOG `[3.70.0]` block.
  - New Active line = `chore/sc2egset-02-01-02-formal-closure` (this turn's planning PR + the subsequent closure execution PR share the branch).

[OPINION] The decision to emit the closure as a separate PR rather than batching it into PR #236 is the conservative reading of the non-batching rule + the PR #229 → PR #230 precedent. The cost is one extra PR; the benefit is a clean separation between materialization correctness (PR #236, audited by reviewer-adversarial on materialization scope) and closure governance (this closure PR, audited by reviewer-adversarial on whether closure overclaims any scope it should not). Reviewer-adversarial is free to challenge this in §Open Questions OQ-Branch.

## Execution Steps

> **All tasks below are for the FUTURE closure execution PR**, on the branch `chore/sc2egset-02-01-02-formal-closure`, after this plan is approved and the reviewer-adversarial Layer-1 pre-execution critique returns APPROVE / APPROVE-WITH-NITS (zero blockers). The closure PR creates ZERO new artifacts / source / tests / notebooks; updates ONE YAML row; appends ONE research_log entry; updates `planning/INDEX.md` + `CHANGELOG.md` + `pyproject.toml` per the standard release tail. NO ROADMAP body edit; NO spec / cleaning-layer YAML edit; NO root research_log edit; NO Phase-03 file; NO Step `02_01_03+` file.

> The Layer-1 diff (this turn) = exactly 2 files: `planning/current_plan.md` + `planning/current_plan.critique.md`.
> The Layer-2 diff (future closure execution PR) = 6 files: `STEP_STATUS.yaml`, dataset `research_log.md`, `planning/INDEX.md`, `CHANGELOG.md`, `pyproject.toml`, planning files carried over.

### T01 — Flip `STEP_STATUS.yaml` (add the `02_01_02` row)

File: `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`.

Operation: APPEND a new YAML key under `steps:` after the existing `"02_01_01":` block (line 196–199). The closure_at date follows U-Date default = PR #236 audit date.

Exact YAML target (verbatim; the `name:` field text is taken from the ROADMAP stub at line 2099 verbatim — `First pre_game feature-family materialization (sc2egset)`):

```yaml
"02_01_02":
  name: "First pre_game feature-family materialization (sc2egset)"
  pipeline_section: "02_01"
  status: complete
  completed_at: "2026-05-23"
```

Important notes for the executor:
- The `name:` text is the ROADMAP stub's canonical `name` field (line 2103 of ROADMAP: `name: "First pre_game feature-family materialization (sc2egset)"`). DO NOT paraphrase; quote verbatim.
- The `pipeline_section:` value is `"02_01"` (string-quoted, matching the convention used for `02_01_01` row at line 198).
- The `completed_at:` value is `"2026-05-23"` (PR #236 audit date) per U-Date default. If reviewer-adversarial chooses U-Date (ii), use `"2026-05-24"`.
- No other key in this file may be changed.
- No comment is added (the file's existing comments at top — `# Step-level execution status for sc2egset.` etc. — remain byte-unchanged).

Falsifier on this task: F-step-status-row-inconsistent-with-ROADMAP — the `name:` and `pipeline_section:` fields must match the ROADMAP stub byte-exactly.

### T02 — Append closure entry to dataset `research_log.md`

File: `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`.

Operation: APPEND-ONLY a new reverse-chronological entry at the top (above the current PR #236 entry which starts at line 5 with `## 2026-05-23 — Materialize Step 02_01_02 pre_game tranche-1 Parquet + first non-vacuous CROSS-02-01 audit`). The PR #236 entry remains byte-identical (this is the `closure_status: still_open` baseline historical record).

Entry template (reverse-chronological top entry; the PR-number placeholder `PR #<N>` is filled at PR creation time; the date `2026-05-XX` is filled with the closure PR's open date; per ml-protocol all required Category A sections present):

```markdown
## 2026-05-XX — Formal closure of Step 02_01_02 (U2.B; status YAML flip; no new artifact)

- **Category:** A (science / Phase 02 / step closure)
- **Dataset:** sc2egset
- **Branch:** `chore/sc2egset-02-01-02-formal-closure`
- **PR:** `PR #<N>`
- **Step scope:** Step `02_01_02` — formal closure via STEP_STATUS row addition; no new on-disk artifact is created by this PR.
- step: 02_01_02
- closure_status: `closed`
- materialization_state: `materialized`
- leakage_audit_state: `post_materialization_pass`
- status_yaml_state: `complete`
- **What:** Add `"02_01_02": complete` row to `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` (the only mutating YAML); record evidence pointers to PR #236's Parquet (44,418 rows × 11 cols at `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet`) and audit JSON+MD at `reports/artifacts/02_01_02/leakage_audit_sc2egset.{json,md}` (verdict=PASS, len(features_audited)=7). No new on-disk artifact is created by this PR.
- **Why:** Discharges step 8 of 9 of the `.claude/rules/data-analysis-lineage.md` non-batching sequence for empirical work (research_log / STEP_STATUS / manifest) as a separate PR per the merged Layer-1 plan §OQ1 (U2.B). CROSS-02-01-v1.0.1 §5 gate condition was mechanically cleared by PR #236 (non-empty `features_audited` (=7) + verdict PASS + JSON/MD present at the spec-named path); the ROADMAP `continue_predicate` three-clause read (artifact-check + non-vacuous PASS + per-family §10 verdict consistency) is satisfied on disk by PR #216 (registry) + PR #229 (§10 evidence) + PR #236 (materialization + audit). The closure rides a separate PR per the PR #229 → PR #230 precedent.
- **How (reproducibility):** No notebook (closure-only PR; emitting one would falsify the lineage — see PR #230 precedent). Evidence pointers: PR #236 audit JSON at `02_01_02/leakage_audit_sc2egset.json` with `verdict=PASS`, `audit_pr=PR #236`, `feature_parquet_sha256=24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39`, `provenance_git_sha=51288130d3614cd5ea12b4fcb32ce946cb3ebc24`. Master HEAD at closure PR open = `39298c0afd3a23bfbd4603415314af784a672952` (PR #236 merge commit).
- **Findings:** Step `02_01_02` is closed; the `02_01` pipeline section remains `complete` (per `STEP_STATUS.yaml:4-8` and `PIPELINE_SECTION_STATUS.yaml:10-13` derivation rule — ALL its steps are complete: `02_01_01` and `02_01_02`); Phase 02 remains `in_progress` (only 1 of 8 canonical pipeline sections complete per `docs/PHASES.md` lines 112–124); Phase 03 remains `not_started`.
- **What this means:** PIPELINE_SECTION_STATUS.yaml `02_01 = complete` remains correct after this closure (NOT a re-derivation to `in_progress` — both children are `complete`); PHASE_STATUS.yaml byte-unchanged; root `reports/research_log.md` untouched; Step `02_01_03` NOT started; Phase 03 NOT started. This closure does NOT authorise any Step `02_01_03+` or Phase 03 work; it only opens the gate for a future planner-science session to design `02_01_03`.
- **Decisions taken:** `completed_at = "2026-05-23"` (PR #236 audit date per the PR #230 precedent of evidence-date convention); patch version bump 3.70.0 → 3.70.1 because closure adds no new on-disk artifact (chore-class diff); branch prefix `chore/` (governance-only / no new artifact); single-dataset closure recorded ONLY in per-dataset research log (per `.claude/ml-protocol.md` lines 51-54); PR #236 entry preserved byte-unchanged (still_open historical record).
- **Decisions deferred:** Step `02_01_03` planning (a future planner-science session may begin after this closure merges); Phase 03 planning; CROSS-02-02 §6.1 minor amendment proposed in PR #234 §8 (future Category E spec-only PR target); thesis Chapter 4 §4.5 prose update (future Category F thesis writing PR target consuming the now-closed Step 02_01_02 lineage).
- **Thesis mapping:** Chapter 4 §4.5 (feature engineering plan) — citable as the formal closure row for Step 02_01_02 alongside PR #229 (§10 evidence), PR #230 (vacuous CROSS-02-01 audit for 02_01_01), PR #233 (scaffold), PR #234 (source/anchor/race adjudication), PR #236 (first non-vacuous CROSS-02-01 audit). The closure entry is the citable "Step 02_01_02 closed" lineage row.
- **Open questions / follow-ups:** schedule the Step `02_01_03` planner-science round (separate planning PR; will read the now-closed `02_01_02` row as its predecessor); confirm whether a §10-style design-time per-family verdict audit must be re-run for any history_enriched_pre_game families before Step `02_01_03` materialization (likely yes per PR #229 precedent); future-PR target for CROSS-02-02 §6.1 minor amendment.
- **Acknowledged trade-offs:** the closure-only PR creates no on-disk artifact; the only durable repo evidence of the closure decision is the STEP_STATUS row + this research_log entry + the CHANGELOG block. The audit pair at `02_01_02/leakage_audit_sc2egset.{json,md}` remains the on-disk leakage-clearance evidence (created by PR #236, not by this PR).
- **Scope notes:** does NOT touch the ROADMAP body / specs / cleaning-layer YAMLs / artifacts / tests / sandbox / module files / root `reports/research_log.md` / Phase 03 directories / Step 02_01_03 paths / AoE2 paths / thesis chapters / bib / appendix / docs / `.claude/`. The PR #236 research_log entry (currently top of file) is preserved byte-unchanged as a deliberate historical record of the still_open baseline before this closure.
```

Falsifiers on this task: F-research-log-missing-still-open-baseline-entry (PR #236 entry must remain byte-identical with `closure_status: still_open`); F-closure-entry-overclaims-phase-03-or-step-02-01-03 (the entry MUST NOT claim Phase 03 has started, MUST NOT claim Step 02_01_03 has started, MUST NOT claim any spec / ROADMAP / cleaning-YAML mutation).

### T03 — Update `planning/INDEX.md` archive + active

File: `planning/INDEX.md`.

Two edits:
- **Archive line for PR #236.** Move the current `## Active plan` PR #236 entry (lines 3–4 of `planning/INDEX.md`) into the `## Archive` table as the topmost row. The archive row's `Merged PR` cell = `#236 (merged 2026-05-23 at master 39298c0a)`. The summary cell reuses the current Active-line summary verbatim (the materialization-execution Layer-2 description); for the closure context the explicit non-closure language remains accurate.
- **New Active line for the closure PR.** Replace the `## Active plan` block with:

```markdown
## Active plan
- chore/sc2egset-02-01-02-formal-closure (2026-05-24) — Category A: U2.B formal closure of SC2EGSet Step 02_01_02 (Layer-1 planning + Layer-2 execution; shared branch). STEP_STATUS.yaml row added (`"02_01_02": complete; completed_at: "2026-05-23"`). Dataset `research_log.md` carries a closure entry (`closure_status: closed`; `leakage_audit_state: post_materialization_pass`). NO new on-disk artifact created; NO ROADMAP/spec/cleaning-YAML/source/test/notebook edit; NO root research_log touch; NO Phase-03 / Step 02_01_03 work. PIPELINE_SECTION_STATUS.yaml byte-unchanged (`02_01` remains `complete` — both children `02_01_01` and `02_01_02` are now `complete`). PHASE_STATUS.yaml byte-unchanged (Phase 02 `in_progress`; Phase 03 `not_started`). Patch version bump 3.70.0 → 3.70.1 (chore; no new artifact).
```

Notes for the executor:
- The archive table preserves the existing column structure (`Branch | Date | Category | Description | Plan file | Merged PR`) — see lines 8–9 of `planning/INDEX.md` for the header.
- PR #236's archive row goes BEFORE the existing PR #235 row (reverse-chronological by merge date is the existing convention).
- Do NOT touch any other archive row.

Falsifier on this task: F-active-line-overclaims-phase-03 (the new Active line MUST NOT include any Phase-03 language); F-archive-merge-sha-wrong (the PR #236 archive row MUST cite `39298c0a` exactly as the merge commit).

### T04 — Append `CHANGELOG.md` `[3.70.1]` block

File: `CHANGELOG.md`.

Operation: Move the `[Unreleased]` block (currently empty headers at lines 12–20) into a new `[3.70.1]` section between `[Unreleased]` and `[3.70.0]`. Leave `[Unreleased]` with empty `Added/Changed/Fixed/Removed` headers.

Exact `[3.70.1]` block target:

```markdown
## [3.70.1] — 2026-05-XX (PR #<N>: chore/sc2egset-02-01-02-formal-closure)

### Changed

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` — added `"02_01_02": complete` row (`name: "First pre_game feature-family materialization (sc2egset)"`, `pipeline_section: "02_01"`, `completed_at: "2026-05-23"`). Status-chain flip only.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` — append-only closure entry at top (`closure_status: closed`; `leakage_audit_state: post_materialization_pass`; PR #<N>). PR #236 baseline entry (`closure_status: still_open`) preserved byte-unchanged.
- `planning/INDEX.md` — PR #236 archived (merged 2026-05-23 at master `39298c0a`); new Active line for `chore/sc2egset-02-01-02-formal-closure`.
- `pyproject.toml` — version 3.70.0 → 3.70.1.

### Notes

- Formal closure of Step `02_01_02` (U2.B per merged PR #235 Layer-1 plan §OQ1). NO new on-disk artifact created. NO Parquet, NO audit, NO spec, NO source, NO test, NO notebook, NO cleaning-layer YAML, NO ROADMAP body, NO root `reports/research_log.md` edit.
- `PIPELINE_SECTION_STATUS.yaml` byte-unchanged: `02_01` remains `complete` per the YAML header rule "Pipeline section is complete when ALL its steps are complete." Both `02_01_01` and `02_01_02` are now `complete`; ALL steps in 02_01 are complete; the derived value is unchanged from the existing `complete`. **Reconciliation with PR #236 audit JSON `notes`.** The PR #236 audit JSON `notes` field on master (byte-frozen) reads: "PIPELINE_SECTION_STATUS 02_01 = complete remains derived from STEP_STATUS until a future PR adds 02_01_02 to STEP_STATUS, at which point YAML-derivation re-derives 02_01 = in_progress (intended behaviour, pre-disclosed in PR #230 CHANGELOG Notes)." That sentence was conditioned on the successor landing with status `in_progress` (the typical scaffold-style path); this closure lands the successor directly with status `complete`, so the more-specific "ALL steps complete" clause of the derivation rule dominates and re-derivation yields `complete`. PR #232 and PR #234 plan bodies anticipated this exact case ("if the successor lands with status `complete` directly, the section stays `complete`"). The PR #236 audit JSON is NOT amended by this PR; the reconciliation is recorded here in the closure CHANGELOG Notes as the authoritative location.
- `PHASE_STATUS.yaml` byte-unchanged: Phase 02 remains `in_progress` (only 1 of 8 canonical pipeline sections complete per `docs/PHASES.md`); Phase 03 remains `not_started`.
- Closure rides a separate PR per the PR #229 → PR #230 evidence-then-closure precedent. PR #229 §10 verdict-audit pair, PR #230 vacuous catalog audit pair, PR #233 scaffold validator, PR #234 source/anchor/race adjudication, PR #235 Layer-1 plan, and PR #236 materialization + first non-vacuous CROSS-02-01 audit remain byte-unchanged at their distinct paths.
- Step `02_01_03` NOT started; Phase 03 NOT started; baseline modelling NOT started.
- Patch bump per `.claude/rules/git-workflow.md` (chore; closure adds no new on-disk artifact).
- `completed_at = "2026-05-23"` uses the PR #236 audit date per the PR #230 precedent (evidence-date convention; `STEP_STATUS.yaml` lines 21–195 consistently use evidence dates not merge dates).
```

Falsifier on this task: F-changelog-version-mismatch (the version literal in the CHANGELOG header MUST match `pyproject.toml` post-bump); F-changelog-overclaims-phase-03 (the Notes block MUST explicitly assert Phase 03 NOT started AND Step 02_01_03 NOT started).

### T05 — Bump `pyproject.toml` version

File: `pyproject.toml`.

Operation: change line 3 from `version = "3.70.0"` to `version = "3.70.1"`. No other line touched.

Falsifier on this task: F-version-bump-incorrect (must be exactly `3.70.1`; if reviewer-adversarial chooses U-Branch (ii) `feat/`, this becomes `3.71.0`).

### T06 — Critique gate (lightweight reviewer-adversarial Layer-1 pre-execution)

Per `.claude/rules/data-analysis-lineage.md` Agent and model routing discipline and per CLAUDE.md Category A protocol, **adversarial critique is required before any execution begins.**

A reviewer-adversarial pre-execution gate runs over THIS Layer-1 plan body. Lightweight scope is justified because:
- This is a governance-only closure with no empirical content.
- The PR #236 evidence the closure rests on already cleared reviewer-adversarial during PR #235 Layer-1 + PR #236 Layer-2 critique gates (the audit pair is byte-frozen and was the subject of the PR #236 ChatGPT second-pass APPROVE verdict).
- The closure governance is the ONLY methodological novelty here; the relevant decision (U2.B) is already on master via PR #235 (the historical Layer-1 plan §OQ1).

Required reviewer-adversarial coverage:
1. Does the closure overclaim Phase 03 / Step 02_01_03 / any spec amendment / any cleaning-layer YAML mutation? (Must be NO on all four.)
2. Is the `completed_at` date consistent with the closure precedent (U-Date default = `"2026-05-23"`)?
3. Is the version-bump category consistent with the diff scope (U-Branch default = `chore/` + patch `3.70.1`)?
4. Are PR #236 evidence pointers (verdict, features_audited count, audit_pr field, examiner-clarity sentence) cited correctly?
5. Is the assertion that `PIPELINE_SECTION_STATUS.yaml` stays byte-unchanged genuinely correct under the YAML header rule? (See §Status derivation analysis below for the step-by-step.)

If reviewer-adversarial returns APPROVE or APPROVE-WITH-NITS with zero blockers → Layer-1 PR merges → Layer-2 executor dispatched immediately on the same branch.

If reviewer-adversarial returns HOLD-WITH-BLOCKERS → focused-revision planner-science turn → re-run reviewer-adversarial.

### T07 — Final scope check (pre-merge / post-execution)

Before merging the closure PR, verify:
- `git diff <base_ref>..HEAD --name-only` returns EXACTLY: `planning/current_plan.md`, `planning/current_plan.critique.md`, `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`, `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`, `planning/INDEX.md`, `CHANGELOG.md`, `pyproject.toml`. Nothing else.
- `git diff <base_ref>..HEAD -- src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` is EMPTY.
- `git diff <base_ref>..HEAD -- src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` is EMPTY.
- `git diff <base_ref>..HEAD -- src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` is EMPTY.
- `git diff <base_ref>..HEAD -- src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/` is EMPTY.
- `git diff <base_ref>..HEAD -- reports/specs/` is EMPTY.
- `git diff <base_ref>..HEAD -- src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/` is EMPTY.
- `git diff <base_ref>..HEAD -- reports/research_log.md` is EMPTY (root research log untouched).
- `git diff <base_ref>..HEAD -- tests/` is EMPTY (no test added or modified).
- `git diff <base_ref>..HEAD -- sandbox/` is EMPTY (no notebook touched).
- Pre-commit hooks pass (jupytext sync vacuous; ruff/mypy vacuous because no `.py` touched).
- The new top entry of `research_log.md` contains all required Category A sections per `.claude/ml-protocol.md` lines 56–60.
- `STEP_STATUS.yaml` post-flip parses as valid YAML; the new `"02_01_02"` key sits under `steps:` and has all 4 required fields (`name`, `pipeline_section`, `status`, `completed_at`).
- Reviewer-deep is NOT required; this is governance-only. Final gate = reviewer-adversarial Layer-2 pass (Category A protocol per CLAUDE.md Plan / Execute Workflow table).

## File Manifest

**Layer 1 (this turn's draft planning PR) — exactly 2 files:**

| File | Action | Layer |
|------|--------|-------|
| `planning/current_plan.md` | Create (this plan) | 1 (this turn — 2-file diff) |
| `planning/current_plan.critique.md` | Create (reviewer-adversarial pre-execution gate output) | 1 (this turn) |

**Layer 2 (future closure execution PR) — exactly 6 distinct files** (5 modified + the 2 planning files carry over from Layer 1; final closure-PR tracked diff = 6 entries because the closure PR's diff is computed against `base_ref = 39298c0afd3a23bfbd4603415314af784a672952`):

| File | Action | Layer |
|------|--------|-------|
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` | Update (add `"02_01_02": complete` row; see T01) | 2 (future) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` | Update (append closure entry at top; see T02; PR #236 baseline entry preserved byte-unchanged) | 2 (future) |
| `planning/INDEX.md` | Update (archive PR #236 at `39298c0a`; new Active line; see T03) | 2 (future) |
| `CHANGELOG.md` | Update (`[Unreleased]` → `[3.70.1]`; see T04) | 2 (future) |
| `pyproject.toml` | Update (`3.70.0` → `3.70.1`; see T05) | 2 (future) |
| `planning/current_plan.md` + `planning/current_plan.critique.md` | Carry over from Layer 1 (committed in Layer 1; persist into Layer 2's tracked diff because the branch is shared per PR #229 → PR #230 precedent) | 1+2 |

**Total Layer-2 tracked diff against `base_ref` = 7 entries** (counting the 2 planning files explicitly per repo convention; PR #229 CHANGELOG `[3.64.0]` Changed entry sets this precedent).

**Explicitly NOT in either layer's manifest** (byte-unchanged; gate-condition falsifiers will fire on any drift):
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` — byte-unchanged. `02_01` remains `complete` per the YAML header rule + derivation (see §Status derivation analysis).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` — byte-unchanged. Phase 02 remains `in_progress`; Phase 03 remains `not_started`.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` — byte-unchanged. The 02_01_02 stub block from PR #232 (lines 2099–2300) remains intact.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json` — byte-unchanged (PR #236 frozen evidence).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.md` — byte-unchanged (PR #236 frozen evidence).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet` — byte-unchanged (PR #236 frozen evidence).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.{json,md}` — byte-unchanged (PR #230 historical vacuous audit pair at distinct path).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.{csv,md}` — byte-unchanged (PR #234 adjudication artifacts).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.{csv,md}` — byte-unchanged (PR #229 §10 evidence).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.{csv,md}` — byte-unchanged (PR #216 registry).
- `src/rts_predict/games/sc2/datasets/sc2egset/materialize_pre_game_features.py` and `tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_pre_game_features.py` — byte-unchanged (PR #236 source + tests).
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_pre_game_source_layer.py`, `validate_pre_game_feature_materialization.py`, `validate_registry_section10_verdicts.py` and their tests — byte-unchanged (PR #233/#234/#228 source + tests).
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.{py,ipynb}` and `02_01_02_source_anchor_race_adjudication.{py,ipynb}` and `02_01_01_registry_section10_verdict_audit.{py,ipynb}` and `02_01_01_feature_family_registry_skeleton.{py,ipynb}` — byte-unchanged.
- `reports/specs/02_00_feature_input_contract.md`, `02_01_leakage_audit_protocol.md`, `02_02_feature_engineering_plan.md`, `02_03_temporal_feature_audit_protocol.md` — byte-unchanged.
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml`, `matches_history_minimal.yaml`, `matches_long_raw.yaml` — byte-unchanged.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` — byte-unchanged.
- `reports/research_log.md` (root) — byte-unchanged.
- `thesis/`, `docs/`, `.claude/`, `src/rts_predict/games/aoe2/` and all other paths — byte-unchanged.

## Gate Condition

The closure execution PR is mergeable iff ALL of:

1. The final tracked diff matches the closure manifest EXACTLY: `STEP_STATUS.yaml`, dataset `research_log.md`, `planning/INDEX.md`, `CHANGELOG.md`, `pyproject.toml`, plus the 2 planning files (`planning/current_plan.md`, `planning/current_plan.critique.md`). 7 entries total in `git diff <base_ref>..HEAD --name-only`. No extra file.
2. `STEP_STATUS.yaml` adds exactly the `"02_01_02": complete` row with the canonical `name:` (matching ROADMAP line 2103 verbatim), `pipeline_section: "02_01"`, and `completed_at: "2026-05-23"` (or `"2026-05-24"` under U-Date (ii)).
3. `PIPELINE_SECTION_STATUS.yaml` is byte-unchanged. (Falsifier F-pipeline-section-status-yaml-changed-without-derivation-justification.)
4. `PHASE_STATUS.yaml` is byte-unchanged. (Falsifier F-phase-status-starts-phase-03 + F-phase-status-changed-without-justification.)
5. `ROADMAP.md` is byte-unchanged. (Falsifier F-roadmap-body-edit.)
6. Dataset `research_log.md` has the new closure entry at top with `closure_status: closed`, `leakage_audit_state: post_materialization_pass`, `materialization_state: materialized`, `status_yaml_state: complete`, and all required Category A sections per `.claude/ml-protocol.md` lines 56–60.
7. The PR #236 baseline entry (`closure_status: still_open`) at lines 5–32 of the pre-closure file is byte-identical post-closure. (Falsifier F-research-log-missing-still-open-baseline-entry.)
8. `pyproject.toml` version = `3.70.1` AND `CHANGELOG.md` carries a new `[3.70.1] — <YYYY-MM-DD> (PR #<N>: chore/sc2egset-02-01-02-formal-closure)` section. (Falsifier F-version-bump-incorrect + F-changelog-version-mismatch.)
9. `planning/INDEX.md` archives PR #236 at master merge commit `39298c0a` AND promotes `chore/sc2egset-02-01-02-formal-closure` to the Active line. (Falsifier F-archive-merge-sha-wrong.)
10. NO artifact / source / test / notebook / spec / cleaning-layer YAML / ROADMAP body / `INVARIANTS.md` / root `reports/research_log.md` edit. The diff is governance-only. (Falsifier F-any-artifact-source-test-notebook-spec-or-roadmap-change.)
11. NO Phase 03 file edited or created. NO Step `02_01_03+` file edited or created. NO baseline modelling content. (Falsifier F-phase03-creep.)
12. The closure entry text does NOT claim Step `02_01_03` has started, does NOT claim Phase 03 has started, does NOT claim any spec amendment is applied. (Falsifier F-closure-entry-overclaims-phase-03-or-step-02-01-03.)
13. The reviewer-adversarial Layer-1 pre-execution critique gate has returned APPROVE / APPROVE-WITH-NITS with zero blockers (recorded in `planning/current_plan.critique.md`).
14. The reviewer-adversarial Layer-2 final closure gate (post-execution) returns APPROVE / APPROVE-WITH-NITS with zero blockers (per CLAUDE.md Plan / Execute Workflow table — Category A final review is reviewer-adversarial).

### Falsifiers (Layer-1 reviewer-adversarial + Layer-2 reviewer-adversarial enforce; any fired falsifier HALTS the closure PR before commit)

- **F-pr236-audit-missing.** `reports/artifacts/02_01_02/leakage_audit_sc2egset.json` not present on master @ `39298c0a` → closure rests on missing evidence → ABORT and route to a new planner-science round. (Asserts the closure-justifying evidence exists on disk; precondition for closure.)
- **F-pr236-audit-verdict-not-PASS.** Audit JSON `verdict != "PASS"` → ABORT.
- **F-features-audited-not-7.** Audit JSON `len(features_audited) != 7` OR `set(features_audited) != set(["focal_race", "opponent_race", "race_pair", "map_type", "patch_version", "focal_is_mmr_missing", "opponent_is_mmr_missing"])` → ABORT.
- **F-materialization-artifact-missing.** `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet` not present on master → ABORT.
- **F-row-count-not-44418.** Parquet row count != 44,418 → ABORT.
- **F-research-log-missing-still-open-baseline-entry.** The PR #236 entry at lines 5–32 of `research_log.md` is byte-mutated (any change other than the new top entry inserted ABOVE it) → ABORT.
- **F-step-status-row-inconsistent-with-ROADMAP.** The `name:` value in the new STEP_STATUS row does not match the ROADMAP stub's canonical `name:` field byte-exactly → ABORT.
- **F-pipeline-section-status-yaml-changed-without-derivation-justification.** `PIPELINE_SECTION_STATUS.yaml` is not byte-identical → ABORT. (See §Status derivation analysis below for why it MUST be byte-identical under the YAML header rule.)
- **F-phase-status-starts-phase-03.** `PHASE_STATUS.yaml` Phase 03 status changed from `not_started` → ABORT.
- **F-phase-status-changed-without-justification.** Any non-Phase-03 status changed in `PHASE_STATUS.yaml` → ABORT.
- **F-any-artifact-source-test-notebook-spec-or-roadmap-change.** Any file under `reports/artifacts/`, `src/rts_predict/games/sc2/datasets/sc2egset/` (except the 3 named status YAMLs), `tests/`, `sandbox/`, `reports/specs/`, `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/`, or `ROADMAP.md` is touched → ABORT.
- **F-root-research-log-touched.** `reports/research_log.md` (the root cross-dataset log) differs from master → ABORT.
- **F-closure-entry-overclaims-phase-03-or-step-02-01-03.** The closure research_log entry contains any of: "Phase 03 started", "02_01_03 started", "baseline modelling started", "spec amended", "ROADMAP amended" (other than as negated statements) → ABORT.
- **F-version-bump-incorrect.** `pyproject.toml` version != `3.70.1` under U-Branch default (or `3.71.0` under U-Branch (ii)) → ABORT.
- **F-changelog-version-mismatch.** `CHANGELOG.md` `[X.Y.Z]` literal does not match `pyproject.toml` → ABORT.
- **F-archive-merge-sha-wrong.** `planning/INDEX.md` archive row for PR #236 does not cite `39298c0a` → ABORT.
- **F-active-line-overclaims-phase-03.** New Active line in `planning/INDEX.md` mentions Phase 03 → ABORT.
- **F-batching.** The PR diff includes any Step `02_01_03+` content, any Phase 03 content, any spec patch, any cleaning-layer YAML patch — batching beyond the closure scope → ABORT.
- **F-pr230-audit-mutated.** `02_01_01/leakage_audit_sc2egset.{json,md}` differs byte-wise from master → ABORT (historical vacuous audit at distinct path preserved).
- **F-pr234-adjudication-mutated.** `02_01_02_source_anchor_race_adjudication.{csv,md}` differs byte-wise from master → ABORT.
- **F-pr229-section10-mutated.** `02_01_01_section10_verdict_audit.{csv,md}` differs byte-wise from master → ABORT.

## Open Questions

- **OQ-Branch (DOCUMENTED — `chore/` selected; reviewer-adversarial may override).** Branch-name category = `chore/` (governance-only / no new artifact). Justification: `.claude/rules/git-workflow.md` line 25 pegs version-bump category to branch prefix (`patch for fix/test/chore`); the closure has no new artifact / source / test and is patch-class. PR #230 used `feat/` because it created two NEW on-disk audit artifacts under `02_01_01/`; the present closure creates ZERO new on-disk artifacts (the audit JSON+MD at `02_01_02/` already exist on master via PR #236). Default = `chore/` + patch `3.70.1`. If reviewer-adversarial picks `feat/`, the version bump becomes `3.70.0 → 3.71.0` (minor) and the CHANGELOG block is `[3.71.0]`. Both internally consistent; `chore/` recommended. **Needs reviewer-adversarial adjudication.**

- **OQ-Date (DOCUMENTED — PR #236 audit date `"2026-05-23"` selected).** `completed_at` field convention. Three candidates: (i) `"2026-05-23"` (PR #236 audit date / closure-justifying evidence date); (ii) `"2026-05-24"` (today's planning date); (iii) the closure-PR's merge date (unknown at planning time; would require a post-merge YAML edit). Default = (i). Justification: PR #230 set `02_01_01` row to `"2026-04-19"` (the §10 audit evidence date), NOT the PR #230 merge date (2026-05-22). The repo convention throughout `STEP_STATUS.yaml` is the evidence date, not the YAML-flip date. PR #236 audit `audit_date = "2026-05-23"`. Default = (i) `"2026-05-23"`. **Needs reviewer-adversarial adjudication.**

- **OQ-PipelineSectionStatusByteUnchanged (DOCUMENTED — yes; reviewer-adversarial may inspect closely).** Should `PIPELINE_SECTION_STATUS.yaml` genuinely stay byte-unchanged given the YAML header rule's ambiguity? Default = yes (byte-unchanged). See §Status derivation analysis below for the step-by-step. **Reviewer-adversarial may want to verify the derivation arithmetic.**

- **OQ-PlanningBranchScope (DOCUMENTED — reuse same branch).** Default = reuse `chore/sc2egset-02-01-02-formal-closure` for both Layer-1 planning and Layer-2 execution. The 2 planning files persist into Layer 2's tracked diff per PR #229 → PR #230 precedent.

- **OQ-Step02_01_03-Authorization (DOCUMENTED — not authorised by this PR).** This closure does NOT authorise Step `02_01_03` work. A future planner-science session may begin `02_01_03` after this PR merges; the gate is opened, not the work started.

- **OQ-Thesis-Citation (DEFERRED to thesis Cat F PR).** Chapter 4 §4.5 citation of the now-closed Step 02_01_02 lineage: not authored by this PR; a future Category F thesis writing PR consumes the lineage when Chapter 4 §4.5 is updated. The closure research_log entry is the citable source.

## Status derivation analysis

This analysis explains step-by-step why each of the three status YAMLs ends up at the values asserted in §Assumptions.

### Why adding `02_01_02: complete` to `STEP_STATUS.yaml` is now honest

CROSS-02-01-v1.0.1 §5 gate condition (`reports/specs/02_01_leakage_audit_protocol.md` lines 137–147) requires three sub-conditions for Pipeline Section 02_01 exit:

> (a) Every feature column materialized in 02_01 appears in `features_audited` in the audit artifact.
> (b) `verdict = "PASS"` in the audit artifact JSON.
> (c) Both the JSON artifact and the sibling Markdown report are present at the prescribed path.

PR #236's on-disk state clears all three:
- **(a) cleared.** All 7 PRE_GAME feature columns materialized in PR #236 appear in `features_audited`. The audit JSON's `features_audited = ["focal_race", "opponent_race", "race_pair", "map_type", "patch_version", "focal_is_mmr_missing", "opponent_is_mmr_missing"]` is exactly the set of materialised feature columns (the 3 identity + 1 context anchor columns are recorded separately in `projected_identity_columns` / `projected_context_columns` and are NOT model features per CROSS-02-00 §5.1).
- **(b) cleared.** Audit JSON `verdict = "PASS"`.
- **(c) cleared.** JSON at `02_01_02/leakage_audit_sc2egset.json` (4,364 bytes); MD at `02_01_02/leakage_audit_sc2egset.md` (12,307 bytes).

The ROADMAP `continue_predicate` (lines 2240–2249) three-clause read is also satisfied (see §Literature Context). Therefore Step 02_01_02 has met the conditions to be recorded as `complete` in `STEP_STATUS.yaml`.

### Why `PIPELINE_SECTION_STATUS.yaml` `02_01` remains `complete` (byte-unchanged)

The header rule in `PIPELINE_SECTION_STATUS.yaml` lines 10–13:

> Pipeline section is complete when ALL its steps are complete.
> Pipeline section is in_progress when ANY step is in_progress or complete.
> Pipeline section is not_started when NO step has started.

Current state of Pipeline Section `02_01` per `STEP_STATUS.yaml`:
- `02_01_01`: `complete` (lines 196–199; set by PR #230).
- (No `02_01_02` row.)

Under the header rule, when there's only ONE child step and it's `complete`, ALL steps are complete → section is `complete`. This is the current value at `PIPELINE_SECTION_STATUS.yaml:51-54`.

Post-closure state:
- `02_01_01`: `complete`.
- `02_01_02`: `complete` (newly added by this closure PR).

Under the header rule: BOTH children are `complete` → ALL steps are complete → section is `complete`. Byte-identical to the current value.

Note: the header rule line 11 (`in_progress when ANY step is in_progress or complete`) does NOT trigger here because the more specific rule on line 10 (`complete when ALL its steps are complete`) takes precedence. The PR #230 CHANGELOG `[3.65.0]` Notes lines 140–141 disclosed a different scenario — when a successor step lands with status `in_progress`, the derivation would re-derive `02_01 = in_progress`. That is NOT this PR's scenario; here the successor lands directly with status `complete`, so the section stays `complete`.

This is corroborated by PR #235's Layer-1 plan (lines 689–700 of the historical `planning/current_plan.md`):

> Note correction to PR #230 Notes language: PR #230 disclosed re-derivation to `in_progress` would occur if a future PR adds a successor with status `in_progress`. If the successor lands with status `complete` directly (as proposed here), the section stays `complete`. The re-derivation-to-`in_progress` scenario is conditional on the successor's status, not its existence.

Therefore `PIPELINE_SECTION_STATUS.yaml` MUST remain byte-unchanged by this closure PR. If reviewer-adversarial demands a different reading, the falsifier F-pipeline-section-status-yaml-changed-without-derivation-justification fires.

### Why `PHASE_STATUS.yaml` Phase 02 remains `in_progress` (byte-unchanged)

The header rule in `PHASE_STATUS.yaml` lines 9–12 + `PIPELINE_SECTION_STATUS.yaml` lines 5–8:

> Phase is complete when ALL its pipeline sections are complete.
> Phase is in_progress when ANY pipeline section is in_progress or complete.
> Phase is not_started when NO pipeline section has started.

Per `docs/PHASES.md` lines 112–124, Phase 02 has 8 canonical Pipeline Sections: `02_01` through `02_08`. Only `02_01` is currently listed in `PIPELINE_SECTION_STATUS.yaml` (the file's comment at lines 18–21 explicitly states: `Only Phase 01 pipeline sections are listed here. … Pipeline sections are added incrementally as Phases activate, not pre-populated.` — i.e., 02_01 is the first Phase-02 section listed).

Current state: `02_01 = complete`; `02_02..02_08` not yet listed (treated as `not_started` per the canonical Phase list rule). Per the header rule (`in_progress when ANY pipeline section is in_progress or complete`), Phase 02 = `in_progress`. That is the current value at `PHASE_STATUS.yaml:24`.

Post-closure state: `02_01 = complete` (unchanged); `02_02..02_08` still not listed. Per the header rule, Phase 02 remains `in_progress`. Byte-identical.

Therefore `PHASE_STATUS.yaml` MUST remain byte-unchanged by this closure PR.

### Why `PHASE_STATUS.yaml` Phase 03 remains `not_started`

Phase 03 is a downstream gate; it does NOT depend on Phase 02 closure. Per `docs/PHASES.md` lines 128–146, Phase 03 has 9 Pipeline Sections (`03_01..03_09`), none of which is started. Per the header rule (`not_started when NO pipeline section has started`), Phase 03 = `not_started`. That is the current value at `PHASE_STATUS.yaml:27`.

Closing Step `02_01_02` does NOT add any Phase-03 pipeline-section row. Phase 03 byte-unchanged.

### Explicit rejection

This closure PR does NOT:
- start Step `02_01_03` (no `02_01_03` row added to `STEP_STATUS.yaml`; no notebook scaffold; no validator; no Phase-02 history_enriched_pre_game materialization);
- start Phase 03 (no Pipeline Section row added to `PIPELINE_SECTION_STATUS.yaml`; no temporal-splitting work; no baseline-modelling work);
- run baseline modelling (no `tests/` for splitting / baselines; no notebook under `sandbox/sc2/sc2egset/03_*/`; no Phase-03 ROADMAP edit).

## Self-check

Top 3 things I most want `@reviewer-adversarial` to challenge (in priority order):

1. **Category routing — Cat A (Phase work / status closure) vs Cat C/E (chore / docs only).** I'm classifying this closure as Category A because:
   - It is part of the Phase 02 work for sc2egset.
   - It mutates `STEP_STATUS.yaml` and appends a research_log entry — both are Phase-work outputs per the Phase 02 ROADMAP and the data-analysis-lineage non-batching sequence step 8.
   - CLAUDE.md Plan / Execute Workflow table sets Category A's `Read before planning` as "scientific-invariants.md, docs/PHASES.md, active dataset ROADMAP.md" — which I read.

   **Strong pushback:** "This PR has no empirical content; it's pure governance / docs. The diff is 3 status/index files + 2 metadata files (CHANGELOG, pyproject) + 2 planning files. Why not Cat C (chore) or Cat E (docs only)?"

   **My defence:** Category determines (a) branch prefix, (b) version-bump policy, (c) reviewer routing. The user has historically classified the analogous PR #230 closure as Cat A (closure of 02_01_01) even though its substantive diff was 2 hand-written stubs + status YAMLs + research_log. The science / governance distinction is upstream of the diff scope: this PR records a methodological conclusion (Step 02_01_02 is closed because PR #236's CROSS-02-01 audit cleared §5(a/b/c)) — a Phase-02 finding. That is Category A by intent even if the file-shape is governance-mechanical.

   However, the **branch prefix** decision is decoupled from category: `chore/` reflects the diff shape; `feat/` would reflect category-A semantic. PR #230 chose `feat/` and minor bump for the same kind of work because it created new on-disk artifacts. The present closure creates no new on-disk artifacts, so `chore/` + patch is the consistent choice. Reviewer-adversarial should pick: (i) keep Cat A + `chore/` + patch `3.70.1` (recommended); (ii) Cat A + `feat/` + minor `3.71.0` (consistent with PR #230's branch choice); (iii) Cat C + `chore/` + patch `3.70.1` (reclassify the category to match the diff).

2. **`completed_at` date — 2026-05-23 (audit date) vs 2026-05-24 (today / closure-PR open date) vs the closure-PR's eventual merge date.** I'm defaulting to **2026-05-23** because the PR #230 precedent set `02_01_01` row to `2026-04-19` (the §10 audit evidence date), NOT the PR #230 merge date (2026-05-22). The repo convention throughout `STEP_STATUS.yaml` lines 21–195 uses evidence dates.

   **Strong pushback:** "The `completed_at` field literally means 'when was the step completed.' If PR #236 didn't claim closure (which it didn't — it explicitly set `closure_status: still_open`), then the step wasn't 'completed' until the closure PR merges. Use the closure-PR merge date or the closure-PR open date."

   **My defence:** Two readings of `completed_at` exist: (A) the date when the closure-justifying *evidence* became durable (PR #236 audit date = 2026-05-23); (B) the date when the closure *YAML row* was written (closure-PR date). The repo's existing values are all (A) — see PR #230's `02_01_01` row using `2026-04-19` not `2026-05-22`. Picking (B) here would break the precedent. Reviewer-adversarial may demand (B) on stricter reading. If so, the YAML target adjusts to `"2026-05-24"` (closure-PR open date is today per the planning-PR date) — at the cost of breaking the precedent.

3. **`PIPELINE_SECTION_STATUS.yaml` byte-unchanged claim — is the YAML header rule's "complete when ALL steps complete" genuinely unambiguous?** I'm asserting byte-unchanged because BOTH `02_01_01` and `02_01_02` will be `complete` post-closure, so ALL steps are complete → section is `complete`. PR #235's Layer-1 plan (lines 689–700) corroborates this reading.

   **Strong pushback:** "The header rule reads 'complete when ALL its steps are complete.' Currently there's 1 step (`02_01_01: complete`); ALL 1/1 = complete. Post-closure there are 2 steps both complete; ALL 2/2 = complete. Both yield `complete`. But the header *also* says 'in_progress when ANY step is in_progress or complete.' Two interpretations of these conjoined rules: (A) the longer-matching condition wins (mine); (B) the first-matching condition in document order wins (would yield `in_progress` post-closure because the 'ANY step complete' rule appears before the 'ALL steps complete' rule in document order). Or (C) the conditions are mutually exclusive and 'ALL complete' is a subset of 'ANY complete' (would prefer the more-specific 'ALL complete' rule). YAML doesn't formally define rule precedence."

   **My defence:** (C) is the standard reading; (A) is its synonym. PR #230 disclosed the re-derivation behaviour explicitly: "If a future PR adds a successor step (e.g., `02_01_02`) to STEP_STATUS with status `in_progress`, the derivation chain will re-derive `02_01 = in_progress`." The qualifying "with status `in_progress`" is dispositive — the YAML header rule must be reading "ALL complete" as the dominant clause. PR #235's plan corroborates. Reviewer-adversarial should verify by reading the YAML header rule itself.

   If reviewer-adversarial concludes the YAML header rule is genuinely ambiguous, the conservative remedy is to leave `PIPELINE_SECTION_STATUS.yaml` byte-unchanged (the present default) AND add a one-line CHANGELOG note explaining the derivation. The aggressive remedy is to amend `PIPELINE_SECTION_STATUS.yaml` to add an explicit `02_01` re-derivation comment — but this would be a one-line edit, NOT a status change, and would still keep `02_01 = complete`. Default: byte-unchanged.

Other items I do NOT want `@reviewer-adversarial` to dwell on (already documented elsewhere):
- U2.B vs U2.A — already resolved on master via PR #235 §OQ1.
- Phase 03 / Step 02_01_03 authorization — already negated explicitly throughout this plan.
- Spec amendment scope — CROSS-02-02 §6.1 minor amendment remains future-PR target; not applied here.

Sources:
- (No external web sources — all references are repo files cited inline. The CROSS-02-01-v1.0.1 §5 gate condition was verified at `reports/specs/02_01_leakage_audit_protocol.md` lines 137–147 during this planning round; the PR #236 audit JSON was verified at `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json`; the ROADMAP 02_01_02 stub `continue_predicate` was verified at `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` lines 2240–2249; the PR #230 closure precedent was verified at `CHANGELOG.md` lines 122–145.)