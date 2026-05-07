---
category: A
branch: phase02/roadmap-stubs-feature-registry
base_ref: master
date: 2026-05-06
planner_model: claude-opus-4-7
dataset: null  # plan touches all three locked datasets — see Scope
phase: "02"
pipeline_section: "02_01"  # Pre-Game vs In-Game Boundary (per docs/PHASES.md §Phase 02)
phase_step: "02_01_01 (per-dataset; ROADMAP stub only — see T01–T03)"
pr_title: "feat(phase02): add ROADMAP stubs for per-dataset feature-family registry (Step 02_01_01)"
version_bump: "3.46.0 → 3.47.0 (minor; Category A feat — per .claude/rules/git-workflow.md §PR Creation Flow step 2)"
invariants_touched: [I3, I5, I6, I7, I8, I9, I10]
source_artifacts:
  - .claude/rules/data-analysis-lineage.md
  - .claude/scientific-invariants.md
  - docs/TAXONOMY.md
  - docs/PHASES.md
  - docs/templates/step_template.yaml
  - docs/templates/planner_output_contract.md
  - docs/templates/plan_template.md
  - reports/specs/02_00_feature_input_contract.md
  - reports/specs/02_01_leakage_audit_protocol.md
  - reports/specs/02_02_feature_engineering_plan.md
  - reports/specs/02_03_temporal_feature_audit_protocol.md
  - reports/research_log.md
  - planning/README.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/PHASE_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PHASE_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv
critique_required: true
research_log_ref: null  # No research_log entries in this PR — see §3.4 Justification for status/log discipline
---

# Plan: Phase 02 — ROADMAP stubs for per-dataset feature-family registry (Step 02_01_01, three datasets)

## Scope

This plan adds a **single ROADMAP stub** to each of the three locked datasets — sc2egset, aoestats, aoe2companion — that declares Step `02_01_01` as a future per-dataset feature-family registry creation step under Phase 02 — Pipeline Section `02_01` (Pre-Game vs In-Game Boundary, per `docs/PHASES.md`). Each stub references CROSS-02-00-v3.0.1, CROSS-02-01-v1.0.1, CROSS-02-02-v1.0.1, and CROSS-02-03-v1.0.1 by their locked spec/version identifiers (see Assumption A8); declares the planned (not-yet-created) sandbox notebook path; encodes the assumption / sanity check / falsifier / stop conditions required by `.claude/rules/data-analysis-lineage.md`; and describes the registry's planned shape as future-work language only. **No notebooks, generated artifacts, raw data edits, model training, status YAML edits, research_log entries, or thesis-chapter prose are produced or modified by this PR.**

Each dataset receives an independent stub. The three stubs are coordinated through CROSS-02-02-v1.0.1 / CROSS-02-03-v1.0.1 (shared protocol), but each dataset's `02_01_01` step is dataset-scoped per `docs/PHASES.md` §Phase scope.

## Problem Statement

PR #209 (merged at `ef3fc627be1793c135711b8bc3715ecda7490cf7` on 2026-05-05) and PR #210 (post-merge) created and locked the four cross-dataset Phase 02 contracts:

- CROSS-02-00-v3.0.1 (input contract — VIEWs, grain, anchors, encoding protocol, classification);
- CROSS-02-01-v1.0.1 (post-materialization / pre-training leakage audit gate);
- CROSS-02-02-v1.0.1 (feature-engineering plan — feature families, prediction settings, grains, source labels, leakage-check declarations, cold-start gates, proposed Phase 02 ROADMAP steps);
- CROSS-02-03-v1.0.1 (design-time temporal feature audit protocol — D1–D15 audit dimensions, future audit artifact schema).

CROSS-02-02-v1.0.1 §12.1 names a "feature-family registry skeleton" as the first concrete Phase 02 step ("Per-dataset registry of declared feature families from §6 / §7 / §8 … notebook scaffold + one validation module per `.claude/rules/data-analysis-lineage.md`; no feature values produced"). The contracts do **not** themselves commit ROADMAP entries — per CROSS-02-02-v1.0.1 §12 "[the proposals] are **not** dataset ROADMAP edits. CROSS-02-02 does not touch any dataset ROADMAP. A future PR (separate from this T03 step) may convert a proposal into an executed ROADMAP step with explicit user approval and a separate commit."

This PR is that "future PR." It performs the ROADMAP-stub-only step, gated to the first sequential step (Step 1) of the `.claude/rules/data-analysis-lineage.md` non-batching sequence: *"1. ROADMAP stub only."* No notebook scaffold, no validation module, no artifacts, no status updates, no research_log entry — those belong to future PRs.

The current Phase 02 placeholder text in each dataset ROADMAP ("Pipeline Sections: see `docs/PHASES.md`. Steps to be defined when Phase 01 gate is met. **Mandatory entry requirement (added 2026-04-21 per WP-2):** …") is preserved as a paragraph (not deleted) inside the new `## Phase 02 — Feature Engineering` section, which gains a Pipeline Section subheading and the Step `02_01_01` YAML stub under it.

## Assumptions & unknowns

- **Assumption A1 (Step numbering).** The first per-dataset Phase 02 step is `02_01_01` under Pipeline Section `02_01` (Pre-Game vs In-Game Boundary). Source: `docs/PHASES.md` §Phase 02 row `02_01`; `docs/TAXONOMY.md` §Step ("`{PHASE}_{PIPELINE_SECTION}_{STEP}` with zero-padded two-digit components"). The `02_01` Pipeline Section is the canonical home of the registry per the manual's own §2 "Pre-Game vs In-Game Boundary" — the registry is precisely the tool that makes the per-family pre-game / in-game / blocked classification machine-readable.
- **Assumption A2 (Existing placeholders).** Each ROADMAP currently has `## Phase 02 — Feature Engineering (placeholder)` with the WP-2 mandatory-entry-requirement paragraph and **no** Pipeline Section heading and **no** Step YAML blocks. This was verified by reading lines 1905–1910 (sc2egset), 1748–1753 (aoestats), 1416–1421 (aoe2companion). The PR removes the `(placeholder)` qualifier from the Phase 02 heading and adds a `### Pipeline Section 02_01 — Pre-Game vs In-Game Boundary` subheading containing one Step YAML block. The WP-2 mandatory-entry-requirement paragraph is preserved verbatim under the new Pipeline Section subheading (it remains binding).
- **Assumption A3 (No status edits).** Per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical work" steps 1 vs 8 ("ROADMAP stub only" vs "Then research_log / STEP_STATUS / manifest") and per the precedent of the 2026-05-06 root research_log CROSS entry ("**No `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` edits**"), the new Step `02_01_01` is **not** added to any STEP_STATUS.yaml in this PR. STEP_STATUS rows land only after a future PR's notebook scaffold is reviewed and committed (sequence step 8 of the non-batching rule). PHASE_STATUS.yaml continues to read `02: not_started` for all three datasets — correct, because no Phase 02 step has yet started.
- **Assumption A4 (No research_log entries).** Per the same non-batching-rule sequence (step 1 — ROADMAP stub only), no per-dataset `research_log.md` entries and no root `reports/research_log.md` CROSS entry are added by this PR. A future PR that delivers the notebook scaffold + one validation module produces the first research_log entry for `02_01_01`.
- **Assumption A5 (Sandbox path).** Per `docs/TAXONOMY.md` §"Sandbox notebooks", the canonical notebook path for Step `02_01_01` is `sandbox/<game>/<dataset>/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_<slug>.py`. This file is **declared as planned metadata only** in the ROADMAP stub. It is **not** created in this PR. The exact slug is named "feature_family_registry_skeleton" to match CROSS-02-02-v1.0.1 §12.1 wording.
- **Assumption A6 (Version bump).** Per `.claude/rules/git-workflow.md` §"PR Creation Flow" step 2, "minor for feat/refactor/docs" applies. Branch prefix is `phase02/...`; the PR is Category A (Phase work) per `docs/TAXONOMY.md` §Category. `pyproject.toml` is bumped 3.46.0 → 3.47.0 and `CHANGELOG.md`'s `[Unreleased]` is rolled to `[3.47.0] — 2026-05-06 (PR #N: phase02/roadmap-stubs-feature-registry)`.
- **Assumption A7 (Branch naming convention).** This PR's branch is `phase02/roadmap-stubs-feature-registry`. `docs/TAXONOMY.md` §Category maps Category A to the canonical `feat/` prefix; `phase02/` is therefore non-canonical taxonomy-wise. The `phase02/` prefix is intentionally inherited as a project-specific phase-work convention from PR #209 (`phase02/feature-engineering-readiness`) and PR #210, both already merged. This plan treats `phase02/` as an accepted local phase-work branch prefix by precedent rather than as a taxonomy rewrite — `docs/TAXONOMY.md` is **not** edited in this PR (out per §"Out of scope" line 514). The `git-workflow.md` minor-version-bump rule still applies because the substantive work category is `feat`.
- **Assumption A8 (Spec/version identifier discipline).** Each of the four cross-Phase-02 specs has both a `spec_id` field and a `version` field in its YAML frontmatter. Two specs (CROSS-02-00, CROSS-02-01) carry `spec_id` and `version` that coincide — `spec_id: CROSS-02-00-v3.0.1` / `version: CROSS-02-00-v3.0.1`, and `spec_id: CROSS-02-01-v1.0.1` / `version: CROSS-02-01-v1.0.1` — so they are unambiguous. Two specs (CROSS-02-02, CROSS-02-03) carry the bare-major form in `spec_id` and the patch-locked form in `version` — `spec_id: CROSS-02-02-v1` with `version: CROSS-02-02-v1.0.1`, and `spec_id: CROSS-02-03-v1` with `version: CROSS-02-03-v1.0.1`. In this plan, the four strings `CROSS-02-00-v3.0.1`, `CROSS-02-01-v1.0.1`, `CROSS-02-02-v1.0.1`, `CROSS-02-03-v1.0.1` are the project-canonical reference form ("locked spec/version identifiers"); for CROSS-02-00 and CROSS-02-01 they coincide with the `spec_id` field, and for CROSS-02-02 and CROSS-02-03 they coincide with the `version` field by patch-lineage convention. Where this plan previously used the phrase "spec_id literal" / "spec_id literals", read it as "locked spec/version identifier" / "locked spec/version identifiers" — the distinction between the `spec_id` and `version` frontmatter fields is a versioning-convention artifact, not a lineage break.
- **Unknown U1.** The exact PR number is unknown until `gh pr create` runs — the CHANGELOG entry will use `(PR #N: …)` and `N` will be filled at PR-creation time per existing precedent (e.g., the 2026-05-06 root research_log entry references "PR #209"). Resolved by: parent session at PR-creation step (post-execution).
- **Unknown U2.** Whether the existing `## Phase 02 — Feature Engineering (placeholder)` heading should be renamed to `## Phase 02 — Feature Engineering` (drop "(placeholder)") or kept verbatim is an editorial micro-decision. Default in this plan: drop "(placeholder)" because the section now contains a real Pipeline Section subheading and a Step YAML block — it is no longer a placeholder. Resolved by: user acceptance of the plan.

## Literature context

The plan is methodology-bearing only at the structural level — it adds ROADMAP stubs that future steps will execute against. The methodology that the registry will eventually encode is grounded in:

- **Kuhn & Johnson (2019), *Feature Engineering and Selection* (Chapman & Hall/CRC), Ch. 2** — the discipline of declaring a feature's source, grain, and prediction-time admissibility before computing it. CROSS-02-02-v1.0.1 §13.1 carries this declaration discipline; the registry mechanizes it per dataset.
- **López de Prado (2018), *Advances in Financial Machine Learning*, Ch. 3** — strict temporal cutoffs (`history_time < target_time` strict `<`) for time-aware feature construction; the equality form is forbidden because a same-anchor-time row is not strictly prior history. CROSS-02-00-v3.0.1 §3.3 enforces this rule for all three datasets; CROSS-02-03-v1.0.1 D5 audits it design-time. [`history_time < target_time`].
- **Hofmann et al. (2024), MIT MMLU/RTS prediction literature on cold-start handling for sparse rating-system data** — the discipline of expressing cold starts as gates (smoothing prior, threshold flag, missingness indicator) rather than as magic constants. CROSS-02-02-v1.0.1 §9 declares six cold-start gates G-CS-1 through G-CS-6; the registry must declare the gate per family without committing a numeric value. [`OPINION` — gate vs constant framing is project-specific to per-fold derivation discipline; the underlying smoothing methods are standard.]
- **Phase 01 close-out evidence (`thesis/pass2_evidence/phase01_closeout_summary.md`)** — Phase 01 → Phase 02 entry conditions; AoE2 source-specific labels (aoestats Tier 4; aoe2companion ID 6 + ID 18 mixed-mode; ID 6 = `rm_1v1` ranked candidate; ID 18 = `qp_rm_1v1` quickplay/matchmaking-derived); GATE-14A6 outcome `narrowed`; SC2 tracker eligibility CSV is the authoritative SC2 in-game-snapshot constraint. The registry stubs propagate these labels verbatim.

The stubs in this PR encode these references as forward-looking declarations only; no measurement is performed.

## Execution Steps

### T01 — Add Phase 02 ROADMAP stub for sc2egset (Step 02_01_01)

**Objective:** Replace the existing `## Phase 02 — Feature Engineering (placeholder)` section in the sc2egset ROADMAP with a `## Phase 02 — Feature Engineering` section that contains the WP-2 mandatory-entry-requirement paragraph (preserved in meaning, with its stale `CROSS-02-01-v1` / `CROSS-02-00-v1` references updated to the currently-locked `CROSS-02-01-v1.0.1` / `CROSS-02-00-v3.0.1` strings — see step 3) and a `### Pipeline Section 02_01 — Pre-Game vs In-Game Boundary` subheading, under which a single Step `02_01_01` YAML block declares the future feature-family registry skeleton step. The block must reference all four locked specs by their locked spec/version identifiers (per Assumption A8), name (but **not** create) the sandbox notebook path, and encode the assumption / sanity check / falsifier / stop conditions required by `.claude/rules/data-analysis-lineage.md`.

**Instructions:**
1. Read `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` lines 1905–1912 (the current Phase 02 placeholder block) verbatim.
2. Read `docs/templates/step_template.yaml` to confirm the canonical step-YAML field set.
3. In the same file, replace the existing six lines starting at line 1905 (`## Phase 02 — Feature Engineering (placeholder)` through the trailing `---` separator above `## Phase 03`) with a new block that contains:
   - `## Phase 02 — Feature Engineering` (drop the `(placeholder)` qualifier — the section is no longer a placeholder).
   - The 2026-04-21 WP-2 mandatory-entry-requirement paragraph **preserved in meaning, with its spec citations updated to the currently-locked patch successors**. Specifically, the verbatim 2026-04-21 paragraph cites `CROSS-02-01-v1` (the original lock string) and `CROSS-02-00-v1` (the original input-contract lock string). Replace `CROSS-02-01-v1, LOCKED 2026-04-21` with `CROSS-02-01-v1.0.1, LOCKED 2026-05-06 (patch successor of CROSS-02-01-v1, LOCKED 2026-04-21)`, and replace `(CROSS-02-00-v1)` with `(CROSS-02-00-v3.0.1)`. Do **not** leave both the old and new version strings in the same paragraph for the same spec — pick the locked patch successor and drop the bare-major form. All other wording in the paragraph (including "WP-2", the four enumerated audit checks, "verdict = PASS is required for 02_01 exit", the v1-enforcement clause, and the "Protocol is reused (not re-gated) by 02_03 and 02_06" closing sentence) is preserved verbatim. The paragraph remains binding even after this PR.
   - A new sentence appended after that paragraph: "Reuse of the CROSS-02-01-v1.0.1 audit protocol by Pipeline Sections 02_03 and 02_06 follows CROSS-02-01-v1.0.1 §6. The design-time companion gate is `reports/specs/02_03_temporal_feature_audit_protocol.md` (CROSS-02-03-v1.0.1, LOCKED 2026-05-06); the design-time feature-family plan is `reports/specs/02_02_feature_engineering_plan.md` (CROSS-02-02-v1.0.1, LOCKED 2026-05-06)."
   - A `### Pipeline Section 02_01 — Pre-Game vs In-Game Boundary` subheading (per `docs/PHASES.md` §Phase 02 row `02_01`).
   - A single fenced YAML block (Step `02_01_01`) populated as specified in §"Step YAML content (sc2egset)" below.
4. Do **not** modify any other line in the file.
5. Do **not** create the notebook file at `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`. The path appears only as `notebook_path` metadata inside the Step YAML.

**Step YAML content (sc2egset):**

The YAML block must populate these fields (every field literal — do not paraphrase the cited locked spec/version identifiers per Assumption A8; the strings `CROSS-02-00-v3.0.1`, `CROSS-02-01-v1.0.1`, `CROSS-02-02-v1.0.1`, `CROSS-02-03-v1.0.1` must each appear at least once verbatim):

```yaml
step_number: "02_01_01"
name: "Feature-family registry skeleton (sc2egset)"
description: >-
  Per-dataset declaration of Phase 02 candidate feature families for sc2egset:
  family_id, prediction_setting (pre_game / history_enriched_pre_game /
  in_game_snapshot / blocked_or_deferred), source_table_or_event_family,
  source_grain, model_input_grain, temporal_anchor, allowed_cutoff_rule,
  candidate_leakage_modes, cold_start_handling, status. Registry is a
  planning / catalog artifact; no feature value is computed. Constrained by
  reports/specs/02_00_feature_input_contract.md (CROSS-02-00-v3.0.1),
  reports/specs/02_01_leakage_audit_protocol.md (CROSS-02-01-v1.0.1),
  reports/specs/02_02_feature_engineering_plan.md (CROSS-02-02-v1.0.1) §6,
  and reports/specs/02_03_temporal_feature_audit_protocol.md
  (CROSS-02-03-v1.0.1) D1–D15. SC2 in_game_snapshot families are bound by
  src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv:
  only rows with status_in_game_snapshot ∈ {eligible_for_phase02_now,
  eligible_with_caveat} may be declared (12 of 15 rows); the three
  blocked_until_additional_validation rows (mind_control_event_count,
  army_centroid_at_cutoff_snapshot, playerstats_cumulative_economy_fields)
  remain excluded. The slot_identity_consistency row is recorded by the
  CSV as status_in_game_snapshot = eligible_for_phase02_now with
  notes_for_phase02 = "feature-engineering sanity gate; not a model input"
  and eligibility_scope = "structural validity check: per-replay assertion
  …"; the Phase 02 registry MUST therefore represent it as a registry-level
  classification sanity_gate_not_model_input — a registry-introduced
  classification derived from the CSV's notes_for_phase02 + eligibility_scope
  fields and the PR #208 Phase 02 guidance, not a verbatim CSV
  status_in_game_snapshot value. The CSV's status_in_game_snapshot value
  for that row remains eligible_for_phase02_now and is NOT being
  reclassified at the CSV layer. Tracker-derived features are never
  pre-game (Invariant I3; Amendment 2 of PR #208). NOT DELIVERED IN THIS
  ROADMAP-STUB PR — this entry only declares the future step per
  .claude/rules/data-analysis-lineage.md §"Non-batching rule for empirical
  work" sequence step 1.
phase: "02 -- Feature Engineering"
pipeline_section: "02_01 -- Pre-Game vs In-Game Boundary"
manual_reference: "02_FEATURE_ENGINEERING_MANUAL.md, Section 2"
dataset: "sc2egset"
question: >-
  Which Phase 02 candidate feature families exist for sc2egset, declared
  per CROSS-02-02-v1.0.1 §6, and what is each family's CROSS-02-03-v1.0.1
  D1–D15 design-time disposition (allowed / allowed_with_caveat /
  blocked_until_validation / sanity_gate_not_model_input)?
method: >-
  Read CROSS-02-02-v1.0.1 §6 sc2egset feature-family rows and
  tracker_events_feature_eligibility.csv; emit a per-family registry row
  per CROSS-02-03-v1.0.1 §3 audit-object schema; classify each row
  according to CROSS-02-03-v1.0.1 §4 D1–D15 with N/A for inapplicable
  dimensions; record D13 SC2-tracker-eligibility verdicts directly from
  the CSV without re-derivation; produce a planning-only catalog. No
  feature value, no notebook output, no encoder fit. The notebook
  scaffold + one validation module that materialize this registry are
  produced by a SEPARATE FUTURE PR per .claude/rules/data-analysis-lineage.md
  §"Non-batching rule" sequence steps 2–9; THIS PR delivers only step 1
  (ROADMAP stub).
stratification: >-
  Per family: dataset_tag = sc2egset; prediction_setting; source event
  family. SC2 races (Prot / Terr / Zerg / Rand) are stratification axes
  declared at the family level (see RISK-26 — Random race semantics) but
  not encoded as registry rows here.
predecessors: "01_06_04"
notebook_path: >-
  sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py
inputs:
  duckdb_tables:
    - "matches_history_minimal"
    - "player_history_all"
  schema_yamls:
    - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml"
    - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml"
  prior_artifacts:
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/06_decision_gates/modeling_readiness_sc2egset.md"
  external_references:
    - "reports/specs/02_00_feature_input_contract.md (CROSS-02-00-v3.0.1)"
    - "reports/specs/02_01_leakage_audit_protocol.md (CROSS-02-01-v1.0.1)"
    - "reports/specs/02_02_feature_engineering_plan.md (CROSS-02-02-v1.0.1) §6"
    - "reports/specs/02_03_temporal_feature_audit_protocol.md (CROSS-02-03-v1.0.1) §3 / §4 D1–D15"
    - ".claude/rules/data-analysis-lineage.md"
    - ".claude/scientific-invariants.md (I3, I5, I6, I7, I8, I9, I10)"
outputs:
  data_artifacts:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_sc2egset.csv"
  report:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_sc2egset.md"
reproducibility: >-
  All registry rows derived from CROSS-02-02-v1.0.1 §6 and the tracker
  CSV at the cited path; no magic constants (Invariant I7); cold-start
  handling expressed as gate categories per CROSS-02-02-v1.0.1 §9
  (G-CS-1 through G-CS-6) — no numeric pseudocount m, threshold K,
  smoothing strength α, or imputation constant is declared at this layer.
scientific_invariants_applied:
  - number: "3"
    how_upheld: >-
      Every history-feature family in the registry declares
      allowed_cutoff_rule "history_time < target_time" (strict; per
      CROSS-02-00-v3.0.1 §3.3). Every in_game_snapshot family declares
      "event.loop <= cutoff_loop". No tracker-derived family is declared
      with prediction_setting pre_game or history_enriched_pre_game
      (Amendment 2 of PR #208).
  - number: "5"
    how_upheld: >-
      Every per-player family declares symmetric focal_* / opponent_*
      construction; none commits a slot-asymmetric definition. RISK-24 is
      cited; the data-dependent slot-assignment falsifier is enumerated.
  - number: "6"
    how_upheld: >-
      Registry rows trace to CROSS-02-00-v3.0.1 §5 column classifications
      and the tracker CSV verbatim; no value is paraphrased.
  - number: "7"
    how_upheld: >-
      No magic numbers. Every cold-start gate is declared as a category;
      every numeric value (window length, cutoff_loop, threshold K,
      pseudocount m, smoothing strength α) is deferred to a per-dataset
      Phase 02 ROADMAP step that derives it empirically from training
      folds or cites prior literature.
  - number: "8"
    how_upheld: >-
      Every per-dataset polymorphic vocabulary (race / civ, map,
      leaderboard) carries the dataset_tag = 'sc2egset' partition note;
      no encoder is declared as fit cross-dataset.
  - number: "9"
    how_upheld: >-
      Registry is read-only against Phase 01 outputs; no model is built;
      no source-stratified evaluation claim is encoded yet.
  - number: "10"
    how_upheld: >-
      No raw-table or feature-table filename is declared with an absolute
      path; lineage uses the same relative-path convention used by the
      Phase 01 raw tables.
gate:
  artifact_check: >-
    NOT APPLICABLE TO THIS ROADMAP-STUB PR. The artifact_check fires only
    after the future scaffold-and-validation PR materializes the registry
    CSV + MD; at that point the predicate is "the planned CSV and MD
    exist at the declared paths and are non-empty."
  continue_predicate: >-
    A future PR may begin Step 02_01_02 (or the next 02_01 step in the
    ROADMAP) only after this Step 02_01_01 has reached its CSV + MD
    artifact-check at a future PR, the CROSS-02-01-v1.0.1
    post-materialization audit gate has been re-run for any feature
    column the registry triggers materialization of, and a per-family
    CROSS-02-03-v1.0.1 §10 verdict is recorded for every registry row.
  halt_predicate: >-
    Halt before generating any registry artifact if any of the following
    hold (per .claude/rules/data-analysis-lineage.md §"Stop conditions"):
      - any sc2egset tracker-derived row is declared with
        prediction_setting pre_game or history_enriched_pre_game
        (Invariant I3 violation; Amendment 2 of PR #208 violation);
      - any blocked_until_additional_validation tracker row from
        tracker_events_feature_eligibility.csv (mind_control_event_count,
        army_centroid_at_cutoff_snapshot, playerstats_cumulative_economy_fields)
        appears in the registry as an eligible candidate;
      - any history-derived row lacks the strict history_time < target_time
        cutoff against the per-dataset anchor (sc2egset:
        ph.details_timeUTC < target.started_at);
      - any in_game_snapshot row uses event.loop > cutoff_loop or expresses
        the cutoff only in seconds without a corresponding loop value
        (V1 lps caveat);
      - any cold-start row pins a numeric pseudocount, threshold, or
        smoothing constant without a fold-aware empirical derivation or
        literature citation (Invariant I7);
      - the future notebook scaffold attempts to batch ROADMAP +
        notebook + artifact + next step in one execution, contrary to
        the non-batching rule.
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > §4.5 Feature engineering plan (sc2egset registry)"
research_log_entry: >-
  NOT REQUIRED FOR THIS ROADMAP-STUB PR per .claude/rules/data-analysis-lineage.md
  §"Non-batching rule" sequence (step 1 — ROADMAP stub only — does not
  produce a research_log entry). Required on the future scaffold-and-
  validation PR per the standard step-completion protocol; entry goes
  into src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md.
```

**Verification:**
- `git diff master -- src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md | grep -c '02_01_01'` returns ≥ 1.
- `grep -F 'CROSS-02-00-v3.0.1' src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`, `grep -F 'CROSS-02-01-v1.0.1' …`, `grep -F 'CROSS-02-02-v1.0.1' …`, `grep -F 'CROSS-02-03-v1.0.1' …` each return ≥ 1 hit (all four locked spec/version identifiers per Assumption A8 appear verbatim).
- `grep -F 'tracker_events_feature_eligibility.csv' src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` returns ≥ 1 hit.
- `grep -F 'history_time < target_time' src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` returns ≥ 1 hit.
- `grep -F 'event.loop <= cutoff_loop' src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` returns ≥ 1 hit.
- `grep -F 'tracker-derived features are never pre-game' src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md || grep -F 'tracker-derived family' …` returns ≥ 1 hit (paraphrase variants are acceptable so long as the constraint is stated).
- `git status --porcelain src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` returns empty (no status / log edits).
- `find sandbox/sc2/sc2egset/02_feature_engineering -type f 2>/dev/null` returns empty (no notebook created).
- `find src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering -type f 2>/dev/null` returns empty (no artifact created).
- Pre-commit hooks (ruff, mypy) pass — they have no `.py` to lint here, but are still triggered.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (Update — replace the existing Phase 02 placeholder section with a stubbed Phase 02 → 02_01 → 02_01_01 block).

**Read scope:** (none — files are listed in `source_artifacts` frontmatter and read by all tasks; this section is for sibling-task outputs only, of which there are none.)

**Executor model required:** **Opus** (recommended).

**Rationale for model choice:** Per `.claude/rules/data-analysis-lineage.md` §"Agent and model routing discipline": "Use Opus execution … when the implementation step itself requires subtle reasoning about temporal leakage, source semantics … tracker-event interpretation, cold-start gates, or thesis-facing methodological claims." This stub encodes (i) tracker-CSV-derived in_game_snapshot eligibility, (ii) the strict-`<` history cutoff and `event.loop <= cutoff_loop` in-game cutoff with the V1 loops-per-second caveat, (iii) Invariant I3 / I5 / I7 / I8 commitments, (iv) RISK-20 / RISK-24 / RISK-26 hooks, and (v) the explicit declaration that this is a step-1-of-9 entry per the non-batching rule. A Sonnet executor would risk paraphrasing methodologically-load-bearing strings (e.g., "tracker-derived features are never pre-game") or eliding the verbatim locked spec/version identifiers per Assumption A8.

---

### T02 — Add Phase 02 ROADMAP stub for aoestats (Step 02_01_01)

**Objective:** Replace the existing `## Phase 02 — Feature Engineering (placeholder)` section in the aoestats ROADMAP with a structurally identical block to T01's (Pipeline Section `02_01` subheading + Step `02_01_01` YAML), specialized to aoestats: the registry covers CROSS-02-02-v1.0.1 §7 feature families; the WP-2 mandatory-entry-requirement paragraph is preserved verbatim; the AoE2 source-label vocabulary "aoestats Tier 4" / "source label `leaderboard='random_map'`" / "queue semantics unverified" is encoded; the `in_game_snapshot` setting is declared **not supported** for aoestats per CROSS-02-02-v1.0.1 §3.2; the per-dataset history anchor is `started_timestamp` per CROSS-02-00-v3.0.1 §3.2; the DuckDB session must run with `SET TimeZone = 'UTC'` per CROSS-02-00-v3.0.1 §3.3.

**Instructions:**
1. Read `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` lines 1748–1755 (the current Phase 02 placeholder block).
2. In the same file, replace those lines with the same shape as T01's replacement (`## Phase 02 — Feature Engineering` → WP-2 paragraph preserved in meaning with its `CROSS-02-01-v1, LOCKED 2026-04-21` reference updated to `CROSS-02-01-v1.0.1, LOCKED 2026-05-06 (patch successor of CROSS-02-01-v1, LOCKED 2026-04-21)` and its `(CROSS-02-00-v1)` reference updated to `(CROSS-02-00-v3.0.1)` per the same procedure as T01 step 3, with no paragraph carrying both the bare-major and the patch-locked form for the same spec → CROSS-02-02 / CROSS-02-03 reference sentence → `### Pipeline Section 02_01 — Pre-Game vs In-Game Boundary` → fenced YAML block).
3. The Step `02_01_01` YAML block specializes T01's block as follows:
   - `name: "Feature-family registry skeleton (aoestats)"`.
   - `dataset: "aoestats"`.
   - `description` cites CROSS-02-02-v1.0.1 **§7** (not §6); cites the four locked spec/version identifiers (per Assumption A8) verbatim; declares `in_game_snapshot` setting **NOT supported for aoestats** (citing CROSS-02-02-v1.0.1 §3.2 and the empirical absence of in-game replay telemetry); declares the AoE2 source label "aoestats 1v1 Random Map records (source label `leaderboard='random_map'`; queue semantics unverified against upstream API documentation; Tier 4)"; carries the explicit "aoestats MUST NOT be called unqualified ranked ladder" sentence verbatim; cites the aoestats-only `canonical_slot` requirement on `matches_history_minimal` (CROSS-02-00-v3.0.1 §5.2) for focal/opponent projection.
   - `predecessors: "01_06_04"` (the aoestats Phase 01 modeling-readiness exit step is `01_06_04` per `STEP_STATUS.yaml`).
   - `notebook_path: sandbox/aoe2/aoestats/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` (declared only — **not created**).
   - `inputs.duckdb_tables: ["matches_history_minimal", "player_history_all"]`.
   - `inputs.schema_yamls`: the two aoestats VIEW yamls per CROSS-02-00-v3.0.1 §2.2.
   - `inputs.prior_artifacts`: `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/06_decision_gates/modeling_readiness_aoestats.md`.
   - `inputs.external_references`: same four spec citations as T01 (CROSS-02-00-v3.0.1, CROSS-02-01-v1.0.1, CROSS-02-02-v1.0.1, CROSS-02-03-v1.0.1) plus `.claude/rules/data-analysis-lineage.md` and `.claude/scientific-invariants.md`. Drop the SC2 tracker CSV reference (not applicable to aoestats).
   - `outputs.data_artifacts` and `outputs.report`: planned paths `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_aoestats.csv` and `.md`, both prefixed `(planned, NOT created in this PR)`.
   - `scientific_invariants_applied`: same set as T01 (I3, I5, I6, I7, I8, I9, I10), with the I3 entry citing `ph.started_timestamp < target.started_at` and the DuckDB UTC session discipline `SET TimeZone = 'UTC'` from CROSS-02-00-v3.0.1 §3.3; the I8 entry encoding the `dataset_tag = 'aoestats'` partition.
   - `gate.halt_predicate` enumerates aoestats-specific stop conditions:
     - any aoestats family declared with `prediction_setting = in_game_snapshot` (structurally not supported per CROSS-02-02-v1.0.1 §3.2);
     - aoestats called unqualified ranked ladder (Tier 4 violation; D14 violation);
     - `new_rating` (POST_GAME) declared as a `pre_game` or `history_enriched_pre_game` feature;
     - `old_rating` declared as unconditional PRE_GAME (it is `CONDITIONAL_PRE_GAME` per CROSS-02-00-v3.0.1 §5.5; pre-game iff `leaderboard = 'random_map' AND (time_since_prior_match_days < 7 OR time_since_prior_match_days IS NULL)`);
     - any history-derived row lacks the strict `ph.started_timestamp < target.started_at` cutoff;
     - the DuckDB session for any future cross-column TIMESTAMPTZ ↔ TIMESTAMP comparison is not declared as `SET TimeZone = 'UTC'`;
     - any cold-start row pins a numeric pseudocount, threshold, or smoothing constant without empirical derivation (Invariant I7);
     - the future notebook scaffold attempts to batch ROADMAP + notebook + artifact + next step (non-batching-rule violation).
   - `thesis_mapping: ["Chapter 4 -- Data and Methodology > §4.5 Feature engineering plan (aoestats registry)"]`.
   - `research_log_entry`: same future-PR-only language as T01, pointing to `src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md`.
4. The four locked spec/version identifiers (`CROSS-02-00-v3.0.1`, `CROSS-02-01-v1.0.1`, `CROSS-02-02-v1.0.1`, `CROSS-02-03-v1.0.1`) — interpreted per Assumption A8 — must each appear verbatim ≥ 1 time in the new block.
5. The phrases "aoestats Tier 4", "aoestats MUST NOT be called unqualified ranked ladder", and "history_time < target_time" must each appear verbatim ≥ 1 time.
6. Do **not** modify any other line in the file.
7. Do **not** create the notebook file or any artifact path.

**Verification:**
- `git diff master -- src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md | grep -c '02_01_01'` ≥ 1.
- `grep -F 'CROSS-02-00-v3.0.1' src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md && grep -F 'CROSS-02-01-v1.0.1' … && grep -F 'CROSS-02-02-v1.0.1' … && grep -F 'CROSS-02-03-v1.0.1' …` all succeed.
- `grep -F 'aoestats Tier 4' src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` succeeds.
- `grep -F 'unqualified ranked ladder' src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` succeeds.
- `grep -F "leaderboard='random_map'" src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` succeeds.
- `grep -F 'history_time < target_time' src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` succeeds.
- `grep -F "SET TimeZone = 'UTC'" src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` succeeds.
- `grep -F 'in_game_snapshot' src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md | grep -i -E 'not supported|structurally unavailable'` succeeds (i.e., the in_game_snapshot exclusion is stated).
- `git status --porcelain src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml src/rts_predict/games/aoe2/datasets/aoestats/reports/PIPELINE_SECTION_STATUS.yaml src/rts_predict/games/aoe2/datasets/aoestats/reports/PHASE_STATUS.yaml src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md` returns empty.
- `find sandbox/aoe2/aoestats/02_feature_engineering -type f 2>/dev/null` empty.
- `find src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/02_feature_engineering -type f 2>/dev/null` empty.

**File scope:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` (Update).

**Read scope:** (none — independent of T01 / T03; the three ROADMAP edits are parallelizable.)

**Executor model required:** **Opus** (recommended).

**Rationale for model choice:** Per `.claude/rules/data-analysis-lineage.md` §"Agent and model routing discipline": "Use Opus execution … when the implementation step itself requires subtle reasoning about … source semantics, data-generating process, SQL window semantics … cold-start gates, or thesis-facing methodological claims." aoestats specifically requires (i) the Tier-4 source-label discipline (D14 falsifier text), (ii) the `old_rating` CONDITIONAL_PRE_GAME branch (CROSS-02-00-v3.0.1 §5.5), (iii) the DuckDB UTC session discipline (TIMESTAMPTZ ↔ TIMESTAMP comparison), and (iv) the structural `in_game_snapshot` non-support — paraphrasing any of these is a methodology regression.

---

### T03 — Add Phase 02 ROADMAP stub for aoe2companion (Step 02_01_01)

**Objective:** Replace the existing `## Phase 02 — Feature Engineering (placeholder)` section in the aoe2companion ROADMAP with a structurally identical block to T01's, specialized to aoe2companion: the registry covers CROSS-02-02-v1.0.1 §8 feature families; the WP-2 mandatory-entry-requirement paragraph is preserved verbatim; the AoE2 source-label vocabulary "aoe2companion mixed-mode" / "ID 6 = `rm_1v1` ranked candidate" / "ID 18 = `qp_rm_1v1` quickplay/matchmaking-derived" / "ID 6 + ID 18 = aoe2companion mixed-mode, NOT ranked-only" is encoded; the `in_game_snapshot` setting is declared **not supported** for aoe2companion per CROSS-02-02-v1.0.1 §3.2; the per-dataset history anchor is `started` per CROSS-02-00-v3.0.1 §3.2.

**Instructions:**
1. Read `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` lines 1416–1423 (the current Phase 02 placeholder block).
2. In the same file, replace those lines with the same shape as T01's / T02's replacement, applying the same WP-2 paragraph version-reference update (replace `CROSS-02-01-v1, LOCKED 2026-04-21` → `CROSS-02-01-v1.0.1, LOCKED 2026-05-06 (patch successor of CROSS-02-01-v1, LOCKED 2026-04-21)`; replace `(CROSS-02-00-v1)` → `(CROSS-02-00-v3.0.1)`) so no paragraph carries both the bare-major and patch-locked form for the same spec.
3. The Step `02_01_01` YAML block specializes as follows:
   - `name: "Feature-family registry skeleton (aoe2companion)"`.
   - `dataset: "aoe2companion"`.
   - `description` cites CROSS-02-02-v1.0.1 **§8** (not §6 or §7); cites the four locked spec/version identifiers (per Assumption A8) verbatim; declares `in_game_snapshot` setting **NOT supported for aoe2companion** (citing CROSS-02-02-v1.0.1 §3.2); declares the source label "aoe2companion 1v1 Random Map records combining ranked (`rm_1v1`, `internalLeaderboardId = 6`, ~54M `leaderboard_raw` rows) and quickplay/matchmaking (`qp_rm_1v1`, `internalLeaderboardId = 18`, ~7M `leaderboard_raw` rows; external API unavailable 2026-04-26)" and the explicit "aoe2companion mixed-mode (ID 6 + ID 18) is NOT ranked-only" qualifier; declares the stratification-vs-feature distinction for `internalLeaderboardId` per CROSS-02-02-v1.0.1 §8.4.
   - `predecessors: "01_06_04"` (the aoe2companion Phase 01 modeling-readiness exit step is `01_06_04` per `STEP_STATUS.yaml`).
   - `notebook_path: sandbox/aoe2/aoe2companion/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` (declared only — **not created**).
   - `inputs.duckdb_tables: ["matches_history_minimal", "player_history_all"]` (note: `matches_history_minimal` is materialized as a TABLE for aoe2companion per CROSS-02-00-v3.0.1 §2.3 DuckDB-1.5.1 bug workaround — semantics identical to a VIEW).
   - `inputs.schema_yamls`: the two aoe2companion VIEW yamls per CROSS-02-00-v3.0.1 §2.3.
   - `inputs.prior_artifacts`: `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/06_decision_gates/modeling_readiness_aoe2companion.md`.
   - `inputs.external_references`: same four spec citations as T01 / T02 plus the lineage rule and invariants. Drop the SC2 tracker CSV reference.
   - `outputs.data_artifacts` and `outputs.report`: planned paths `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_aoe2companion.csv` and `.md`, both prefixed `(planned, NOT created in this PR)`.
   - `scientific_invariants_applied`: same set as T01 (I3, I5, I6, I7, I8, I9, I10), with the I3 entry citing `ph.started < target.started_at` and the I8 entry encoding the `dataset_tag = 'aoe2companion'` partition; the I9 entry must explicitly cite source-stratified evaluation by `internalLeaderboardId ∈ {6, 18}` per CROSS-02-02-v1.0.1 §8.4.
   - `gate.halt_predicate` enumerates aoe2companion-specific stop conditions:
     - any aoe2companion family declared with `prediction_setting = in_game_snapshot` (structurally not supported);
     - the aoe2companion combined ID 6 + ID 18 scope called ranked-only (D14 violation);
     - the ID-18 quickplay/matchmaking qualifier dropped (D14 violation);
     - `internalLeaderboardId` declared as a generic categorical model input rather than a stratification / sensitivity control (CROSS-02-02-v1.0.1 §8.4 violation; D12 violation);
     - any history-derived row lacks the strict `ph.started < target.started_at` cutoff;
     - any cold-start row pins a numeric pseudocount, threshold, or smoothing constant without empirical derivation (Invariant I7);
     - rating reconstruction declared as silently merging ID 6 and ID 18 scopes (CROSS-02-02-v1.0.1 §8.3 — three different families: within ID 6, within ID 18, combined);
     - the future notebook scaffold attempts to batch ROADMAP + notebook + artifact + next step.
   - `thesis_mapping: ["Chapter 4 -- Data and Methodology > §4.5 Feature engineering plan (aoe2companion registry)"]`.
   - `research_log_entry`: same future-PR-only language as T01, pointing to `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md`.
4. The four locked spec/version identifiers (per Assumption A8) must each appear verbatim ≥ 1 time.
5. The phrases "aoe2companion mixed-mode", "rm_1v1", "qp_rm_1v1", and "history_time < target_time" must each appear verbatim ≥ 1 time. The phrase "ranked-only" must appear ≥ 1 time, in the negative form ("NOT ranked-only" or equivalent — i.e., the falsifier text, not as a positive claim).
6. Do **not** modify any other line in the file.
7. Do **not** create the notebook file or any artifact path.

**Verification:**
- `git diff master -- src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md | grep -c '02_01_01'` ≥ 1.
- `grep -F 'CROSS-02-00-v3.0.1' src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md && grep -F 'CROSS-02-01-v1.0.1' … && grep -F 'CROSS-02-02-v1.0.1' … && grep -F 'CROSS-02-03-v1.0.1' …` all succeed.
- `grep -F 'aoe2companion mixed-mode' src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` succeeds.
- `grep -F 'rm_1v1' src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` succeeds.
- `grep -F 'qp_rm_1v1' src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` succeeds.
- `grep -i 'NOT ranked-only\|not ranked-only\|is not ranked-only' src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` succeeds.
- `grep -F 'history_time < target_time' src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` succeeds.
- `grep -F 'in_game_snapshot' src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md | grep -i -E 'not supported|structurally unavailable'` succeeds.
- `git status --porcelain src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PIPELINE_SECTION_STATUS.yaml src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PHASE_STATUS.yaml src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md` returns empty.
- `find sandbox/aoe2/aoe2companion/02_feature_engineering -type f 2>/dev/null` empty.
- `find src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/02_feature_engineering -type f 2>/dev/null` empty.

**File scope:**
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` (Update).

**Read scope:** (none — independent of T01 / T02.)

**Executor model required:** **Opus** (recommended).

**Rationale for model choice:** Same as T02 — the source-label vocabulary is methodologically load-bearing (mixed-mode vs ranked-only is the highest-stakes AoE2 source-label distinction in the entire thesis), and the stratification-vs-feature distinction for `internalLeaderboardId` (CROSS-02-02-v1.0.1 §8.4 / D12) requires careful framing.

---

### T04 — Cross-stub consistency check (read-only; mechanical)

**Objective:** Verify that the three ROADMAP stubs added by T01 / T02 / T03 are structurally consistent and that no out-of-scope file was modified. Produce a textual consistency report (returned in chat / written to `.github/tmp/t04_consistency_report.txt`) summarizing the findings; do **not** create any new tracked file. This task is a sanity check, not an artifact-producing step.

**Instructions:**
1. Run `git diff --name-only master...HEAD` and confirm the changed-file set is exactly:
   - `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
   - `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md`
   - `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md`
   - `pyproject.toml` (T05)
   - `CHANGELOG.md` (T05)
   - `planning/current_plan.md` (this plan, written by parent)
   - `planning/current_plan.critique.md` (reviewer-adversarial output, written before execution)
   No other path may appear in `git diff --name-only`.
2. Run `git diff master -- '*STEP_STATUS.yaml' '*PIPELINE_SECTION_STATUS.yaml' '*PHASE_STATUS.yaml' '*research_log.md' 'sandbox/' 'src/rts_predict/games/*/datasets/*/reports/artifacts/02_feature_engineering/' 'src/rts_predict/games/*/datasets/*/data/' 'thesis/'` and confirm the diff is empty.
3. For each of the three modified ROADMAPs, confirm:
   - The Step `02_01_01` block is well-formed YAML inside a fenced code block.
   - All four locked spec/version identifiers (`CROSS-02-00-v3.0.1`, `CROSS-02-01-v1.0.1`, `CROSS-02-02-v1.0.1`, `CROSS-02-03-v1.0.1`) — interpreted per Assumption A8 — appear verbatim.
   - The phrase `history_time < target_time` appears.
   - No magic numeric pseudocount / threshold / smoothing constant appears in the block (Invariant I7 — verify by `grep -E 'pseudocount = [0-9]|threshold = [0-9]|smoothing = [0-9]|alpha = [0-9.]|m = [0-9.]'` returning no match — the registry must speak only in gate categories).
   - The block does **not** contain the word "ranked" without an immediately following qualifier ("ranked candidate", "NOT ranked-only", or equivalent) for the AoE2 stubs (T02, T03). This is a tighter form of the D14 falsifier.
4. Confirm the SC2 stub (T01) explicitly excludes the three blocked tracker families by name: `mind_control_event_count`, `army_centroid_at_cutoff_snapshot`, `playerstats_cumulative_economy_fields` (i.e., `grep -F` each name against the SC2 ROADMAP returns ≥ 1 hit each, **inside a stop-condition / halt-predicate / blocked-list context** — paraphrasing is not acceptable here because these family ids are themselves the load-bearing exclusion list).
5. Confirm the SC2 stub (T01) explicitly classifies `slot_identity_consistency` as `sanity_gate_not_model_input` (not as a regular `eligible_for_phase02_now` model-input row).
6. Write a short (≤ 60 lines) consistency report to `.github/tmp/t04_consistency_report.txt` listing every check above with PASS / FAIL. Return its contents in the chat at task completion.
7. Do **not** edit any of the three ROADMAP files. If any check fails, halt and report — do not patch.

**Verification:**
- `cat .github/tmp/t04_consistency_report.txt` shows every check with PASS verdict.
- `git diff master -- '*STEP_STATUS.yaml' '*PIPELINE_SECTION_STATUS.yaml' '*PHASE_STATUS.yaml' '*research_log.md' 'sandbox/' 'src/rts_predict/games/*/datasets/*/reports/artifacts/02_feature_engineering/' 'src/rts_predict/games/*/datasets/*/data/' 'thesis/'` is empty.
- `git status --porcelain` shows only the six expected files (three ROADMAPs + pyproject.toml + CHANGELOG.md + planning/) plus `.github/tmp/t04_consistency_report.txt` (which is gitignored or deleted before commit).
- T01 / T02 / T03 verification commands all succeeded.

**File scope:**
- `.github/tmp/t04_consistency_report.txt` (Create — ephemeral; deleted before commit per `.claude/rules/git-workflow.md` precedent of `.github/tmp/` cleanup).

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (T01 output)
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` (T02 output)
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` (T03 output)

**Executor model required:** **Sonnet** is sufficient.

**Rationale for model choice:** This task is mechanical: it runs `git diff` and `grep` and tallies PASS/FAIL. The methodological judgments are already encoded in T01–T03; T04 only verifies that the encoding survived the edit. Per `.claude/rules/data-analysis-lineage.md`: "Use `@executor` on Sonnet when the task is mechanically specified and the plan already resolves the scientific/methodological decisions."

---

### T05 — Version bump and CHANGELOG update

**Objective:** Bump `pyproject.toml` from 3.46.0 to 3.47.0 and roll the `CHANGELOG.md` `[Unreleased]` section into a `[3.47.0] — 2026-05-06 (PR #N: phase02/roadmap-stubs-feature-registry)` block, per `.claude/rules/git-workflow.md` §"PR Creation Flow" steps 2–5. The placeholder `#N` is filled at PR-creation time by the parent session.

**Instructions:**
1. Edit `pyproject.toml` line 3 from `version = "3.46.0"` to `version = "3.47.0"`. Do not modify any other line in `pyproject.toml`.
2. Edit `CHANGELOG.md`: locate the `## [Unreleased]` section near the top of the file. Promote it to `## [3.47.0] — 2026-05-06 (PR #N: phase02/roadmap-stubs-feature-registry)` with the following short content under it:
   - Under `### Added`: "Per-dataset Phase 02 ROADMAP stubs declaring Step `02_01_01` (feature-family registry skeleton) for sc2egset, aoestats, and aoe2companion. Each stub references CROSS-02-00-v3.0.1, CROSS-02-01-v1.0.1, CROSS-02-02-v1.0.1, and CROSS-02-03-v1.0.1 verbatim; declares (does not create) the sandbox notebook path; encodes assumption / sanity check / falsifier / halt conditions per `.claude/rules/data-analysis-lineage.md` §'Non-batching rule for empirical work' sequence step 1."
   - Under `### Notes`: "No notebooks, generated artifacts, raw data, status YAMLs, research_log entries, thesis chapters, or model-training code were created or modified by this PR. STEP_STATUS / research_log entries land in a future PR per the non-batching rule sequence step 8."
3. Add a new empty `## [Unreleased]` section above `## [3.47.0]` with placeholder subheadings `### Added`, `### Changed`, `### Fixed`, `### Removed` (per `.claude/rules/git-workflow.md` step 5).
4. Confirm pre-commit hooks (ruff, mypy) pass on the diff. They have no `.py` to lint here, so they should pass trivially.

**Verification:**
- `grep '^version = ' pyproject.toml` returns `version = "3.47.0"`.
- `grep -F '[3.47.0] — 2026-05-06' CHANGELOG.md` succeeds.
- `grep -F '[Unreleased]' CHANGELOG.md` returns at least one hit (the new empty Unreleased above `[3.47.0]`).
- `git diff master -- pyproject.toml CHANGELOG.md | wc -l` is small (< 50 lines).

**File scope:**
- `pyproject.toml` (Update — version line only).
- `CHANGELOG.md` (Update — promote Unreleased to 3.47.0 + add new empty Unreleased).

**Read scope:** (none.)

**Executor model required:** **Sonnet** is sufficient.

**Rationale for model choice:** Mechanical version-bump and changelog roll per established repo precedent. No methodological reasoning required.

---

## File Manifest

| File | Action |
|------|--------|
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | Update (T01 — replace Phase 02 placeholder with stubbed 02_01_01 entry) |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` | Update (T02 — same shape, aoestats specialization) |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` | Update (T03 — same shape, aoe2companion specialization) |
| `.github/tmp/t04_consistency_report.txt` | Create (T04 — ephemeral; deleted before commit) |
| `pyproject.toml` | Update (T05 — version 3.46.0 → 3.47.0) |
| `CHANGELOG.md` | Update (T05 — promote Unreleased to [3.47.0]; add new empty Unreleased) |
| `planning/current_plan.md` | Update (parent session writes this plan after user approval — this is repo-standard, not executor-task scope) |
| `planning/current_plan.critique.md` | Create (reviewer-adversarial; before execution) |

**Files NOT in this manifest (and therefore forbidden):**
- Any `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, or `PHASE_STATUS.yaml` (status YAML edits — explicitly out per Assumption A3).
- Any per-dataset `research_log.md` or root `reports/research_log.md` (out per Assumption A4).
- Any `.py` or `.ipynb` under `sandbox/` (no notebook is created; out per `data-analysis-lineage.md` step 1).
- Any file under `src/rts_predict/games/<game>/datasets/<dataset>/reports/artifacts/02_feature_engineering/` (no artifact is created).
- Any file under `src/rts_predict/games/<game>/datasets/<dataset>/data/` (no raw data or DuckDB modification).
- Any file under `thesis/` (no thesis chapter prose).
- Any locked spec at `reports/specs/02_00_*.md`, `reports/specs/02_01_*.md`, `reports/specs/02_02_*.md`, `reports/specs/02_03_*.md`, or `reports/specs/02_04_*.{json,md}` (the four locked contracts and the cross-spec consistency report are out — they remain at their post-PR-#210 LOCKED state).
- Any change to `scripts/validate_phase02_readiness_contracts.py`.
- Any change to `.claude/rules/data-analysis-lineage.md`, `.claude/scientific-invariants.md`, `docs/PHASES.md`, `docs/TAXONOMY.md`, `docs/INDEX.md`, or any other root-level methodology file.

## Gate Condition

The PR is mergeable when **all** of the following hold:

1. T01–T05 verification commands all return PASS.
2. T04 consistency report shows every check PASS, and `.github/tmp/t04_consistency_report.txt` is deleted before the final commit (per `.claude/rules/git-workflow.md` precedent of `.github/tmp/` cleanup).
3. `git diff --name-only master...HEAD` is exactly `{src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md, src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md, src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md, pyproject.toml, CHANGELOG.md, planning/current_plan.md, planning/current_plan.critique.md}` — no other path appears.
4. Reviewer-deep critique exists at `planning/current_plan.critique.md` before T01–T05 execution begins. Reviewer-deep is the active plan-side and final-review gate for this PR per `.claude/rules/data-analysis-lineage.md` §"Agent and model routing discipline" final paragraph ("for this active Phase 02 readiness PR, do not invoke reviewer-adversarial unless the plan is amended or reviewer-deep raises a BLOCKER requiring adversarial methodology review"). Reviewer-adversarial is escalated **only if** reviewer-deep raises an unresolved methodology BLOCKER on the amended plan or on the post-execution diff.
5. Reviewer-deep final-review pass returns PASS or PASS-WITH-NOTES on the post-execution diff. (If reviewer-deep raises a methodology BLOCKER at final review, dispatch reviewer-adversarial per the same rule paragraph.)
6. Pre-commit hooks (ruff, mypy) pass on every commit. With zero `.py` files in the diff this is mechanical, but the hook runs anyway.
7. `pyproject.toml` shows `version = "3.47.0"`. `CHANGELOG.md` shows `## [3.47.0] — 2026-05-06 (PR #N: phase02/roadmap-stubs-feature-registry)`.
8. PHASE_STATUS.yaml continues to read `02: not_started` for all three datasets — this remains correct because no Phase 02 step has yet started.

## Out of scope

The following items are **explicitly out of scope** and may not be touched by any executor task:

- **No notebook creation.** `sandbox/<game>/<dataset>/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_<slug>.{py,ipynb}` is referenced **only as planned metadata** in the ROADMAP stubs. It is **not** created in this PR. Notebook scaffold lands in a future PR per `data-analysis-lineage.md` sequence step 2.
- **No notebook scaffold.** Even an empty scaffold is out — sequence step 2 belongs to the next PR.
- **No validation module.** Sequence step 2 of the non-batching rule belongs to the next PR.
- **No feature generation.** No feature column is computed, materialized, or persisted.
- **No artifact generation.** No `*.csv`, `*.json`, `*.parquet`, or `*.md` artifact under `reports/artifacts/02_feature_engineering/` is created. The two declared output paths (`02_01_01_feature_family_registry_<dataset>.csv` and `.md`) are explicitly prefixed `(planned, NOT created in this PR)` in every Step YAML.
- **No raw data edits.** No changes to `data/` directories under any dataset.
- **No model training, encoder fit, or scaler fit.**
- **No status YAML edits.** No changes to `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, or `PHASE_STATUS.yaml` for any dataset (per Assumption A3 — sequence step 8 belongs to a future PR).
- **No `research_log.md` edits.** Neither root nor per-dataset (per Assumption A4 — sequence step 8).
- **No thesis-chapter prose.** No edits under `thesis/chapters/` or `thesis/`.
- **No `thesis/pass2_evidence/` edits.** The pre-existing pass-2 evidence files remain untouched.
- **No locked-spec edits.** None of CROSS-02-00-v3.0.1, CROSS-02-01-v1.0.1, CROSS-02-02-v1.0.1, CROSS-02-03-v1.0.1, or the `02_04_cross_spec_consistency_report.{json,md}` is amended. They remain at their post-PR-#210 LOCKED state.
- **No validator regeneration.** `scripts/validate_phase02_readiness_contracts.py` is not run; the cross-spec consistency report remains the PR-#209-recorded `head_sha` `e3cf8923` PASS-state evidence.
- **No DuckDB schema change.** No new VIEW or TABLE.
- **No tracker-CSV edit.** `tracker_events_feature_eligibility.csv` is read-only.
- **No new spec.** No `reports/specs/02_05_*.md` or beyond is created in this PR.
- **No second Phase 02 step.** This PR creates `02_01_01` only — not `02_01_02`, `02_02_01`, `02_03_01`, or any later step. Subsequent steps (per CROSS-02-02-v1.0.1 §12.1 proposed sequence: scaffold per dataset, SC2 tracker snapshot validation slice, cold-start measurement, leakage audit dry-run, feature table generation only after approved validations) each get their own future PR.

## Open questions

- **OQ1.** Should the SC2 stub's `description` enumerate the 12 in-scope tracker families by name, or only cite the CSV path and leave enumeration to the future scaffold notebook?
  Resolves by: user decision before T01 execution. Default in this plan: name only the **3 blocked** families verbatim (per T04 §4 mechanical check) and the 1 sanity-gate row by name; cite the CSV path for the 12 in-scope families without enumerating them. Rationale: the 3 blocked families are the load-bearing exclusion list (any silent re-inclusion is a methodology regression), the sanity-gate row is the only family with a special non-model-input verdict, and the 12 in-scope families belong to the future registry artifact, not the ROADMAP-stub level.
- **OQ2.** Should the AoE2 stubs co-cite each other, or each stand alone?
  Resolves by: user decision. Default: each stands alone (Phase scope is dataset-scoped per `docs/PHASES.md` §"Phase scope" — "Two datasets under the same game are treated as independent entities; they do not share ROADMAPs, Pipeline Sections, or Steps"). Cross-AoE2 comparisons live in the cross-game thesis chapter and the cross-dataset `reports/research_log.md`, not in dataset ROADMAPs.
- **OQ3.** The `## [Unreleased]` section in `CHANGELOG.md` may already contain content from in-flight work since PR #210. Should T05 preserve that content under the new `[3.47.0]` heading or roll only the stubs-add line into it?
  Resolves by: executor reads `CHANGELOG.md` Unreleased state immediately before T05 — if Unreleased is empty, T05 inserts the two-bullet content described in T05 step 2; if Unreleased already has content, T05 preserves it under `[3.47.0]` and prepends the two new bullets at the top of the Unreleased-being-promoted block. Default behavior is "preserve existing Unreleased content" — destructive overwrite is forbidden.

---

## Critique instruction (per `.claude/rules/data-analysis-lineage.md` §"Agent and model routing discipline")

For this Phase 02 readiness PR, the active plan-side and final-review gate is **reviewer-deep**, not reviewer-adversarial. The dispatch rule is `.claude/rules/data-analysis-lineage.md` §"Agent and model routing discipline" final paragraph: "For this active Phase 02 readiness PR, do not invoke reviewer-adversarial unless the plan is amended or reviewer-deep raises a BLOCKER requiring adversarial methodology review." Dispatch reviewer-deep to produce `planning/current_plan.critique.md` against this plan. Reviewer-adversarial is escalated **only if** reviewer-deep raises an unresolved methodology BLOCKER on the amended plan or on the post-execution diff. Reviewer-deep should specifically pressure-test:

1. **The Step number is `02_01_01`.** Pipeline Section `02_01` (Pre-Game vs In-Game Boundary) is the canonical home of a feature-family registry per the `02_FEATURE_ENGINEERING_MANUAL.md` §2 mapping in `docs/PHASES.md`, but reviewer-deep should consider whether a pre-`02_01` "Phase 02 readiness check" stub (zero-step `02_00` style) is methodologically more honest. The plan's default is `02_01_01` because (i) `docs/PHASES.md` lists exactly eight Pipeline Sections `02_01`–`02_08` for Phase 02 — there is no `02_00` — and (ii) CROSS-02-02-v1.0.1 §12.1 places the "feature-family registry skeleton" as the first concrete Phase 02 step under `02_01`. If reviewer-deep disagrees, an amended plan must justify creating a new `02_00` Pipeline Section in `docs/PHASES.md`, which is itself an out-of-scope change.
2. **The non-batching discipline holds.** Verify that the three ROADMAP edits do not accidentally smuggle scaffold content (validation modules, sanity-check code, artifact paths populated as if produced) — they must remain pure declarations.
3. **The four locked spec/version identifiers appear verbatim.** A paraphrased identifier (e.g., dropping the `-v3.0.1` suffix) is a methodology regression because it severs the lineage chain to the locked contract quartet. Per Assumption A8, the four canonical strings are `CROSS-02-00-v3.0.1`, `CROSS-02-01-v1.0.1`, `CROSS-02-02-v1.0.1`, `CROSS-02-03-v1.0.1`; for CROSS-02-02 / CROSS-02-03 these correspond to the `version` frontmatter field (the `spec_id` field is the bare-major form), and that distinction is documented rather than smoothed over.
4. **AoE2 source-label discipline holds across both AoE2 stubs.** aoestats Tier 4; aoe2companion mixed-mode (ID 6 + ID 18) is not ranked-only; ID 18 quickplay/matchmaking qualifier is preserved.
5. **SC2 tracker discipline holds.** The 3 blocked families are named verbatim as exclusions; the 1 sanity-gate row (`slot_identity_consistency`) is registered as a registry-level `sanity_gate_not_model_input` classification — explicitly derived from the CSV's `notes_for_phase02` + `eligibility_scope` fields, not from `status_in_game_snapshot` (which the CSV records as `eligible_for_phase02_now` for that row); tracker-derived families never enter `pre_game` or `history_enriched_pre_game`.
6. **No magic numbers.** Cold-start handling is expressed only in gate categories per CROSS-02-02-v1.0.1 §9 — no numeric pseudocount / threshold / smoothing constant appears anywhere in the three ROADMAP stubs.
7. **The `notebook_path` paths are declared but not created.** `find sandbox/ -path '*02_feature_engineering*'` returns empty post-execution.
8. **The WP-2 paragraph carries exactly one version string per spec.** No paragraph in any of the three ROADMAPs after edit cites both `CROSS-02-01-v1` and `CROSS-02-01-v1.0.1` for the same spec; same for `CROSS-02-00-v1` vs `CROSS-02-00-v3.0.1`.
