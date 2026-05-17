---
title: "Phase 02 registry methodology framing for Chapter 4 §4.5 (TQ-03)"
category: F
branch: thesis/phase02-registry-methodology-section-4-5
date: 2026-05-17
planner_model: claude-opus-4-7
branch_prefix: thesis/
branch_name: thesis/phase02-registry-methodology-section-4-5
pr_title: "docs(thesis): add Phase 02 registry methodology framing for Chapter 4"
pr_number: 219
base_ref: "master @ f1add6ce"
base_commit: f1add6ce
created_date: 2026-05-17
dataset: sc2egset
phase: "02 — provisional registry methodology framing only; NO Phase 02 closure"
pipeline_section: "n/a (Category F thesis prose; consumes prior Phase 02 §02_01 provisional registry artifact)"
step: "n/a (Category F prose update; no Step closure claimed)"
target_version: "3.54.0"
version_current: "3.53.0"
version_bump_type: "minor (Category F docs prose addition per .claude/rules/git-workflow.md:14)"
critique_required: true
invariants_touched: [I3, I5, I6, I7, I8]
prior_executed_tasks:
  - T00: "Draft PR + bootstrap stub planning/current_plan.md (commit 1ffb4df1) — complete"
source_artifacts:
  - docs/TAXONOMY.md
  - docs/PHASES.md
  - docs/INDEX.md
  - .claude/rules/thesis-writing.md
  - .claude/rules/data-analysis-lineage.md
  - .claude/scientific-invariants.md
  - .claude/author-style-brief-pl.md
  - docs/templates/plan_template.md
  - docs/templates/planner_output_contract.md
  - CLAUDE.md
  - thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md
  - thesis/WRITING_STATUS.md
  - thesis/THESIS_STRUCTURE.md
  - thesis/chapters/REVIEW_QUEUE.md
  - thesis/references.bib
  - thesis/chapters/04_data_and_methodology.md
  - thesis/pass2_evidence/notebook_regeneration_manifest.md
  - thesis/pass2_evidence/phase02_readiness_hardening.md
  - thesis/pass2_evidence/methodology_risk_register.md
  - thesis/pass2_evidence/phase01_closeout_summary.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/PHASE_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PHASE_STATUS.yaml
  - reports/specs/02_00_feature_input_contract.md
  - reports/specs/02_01_leakage_audit_protocol.md
  - reports/specs/02_02_feature_engineering_plan.md
  - reports/specs/02_03_temporal_feature_audit_protocol.md
research_log_ref: null
---

# Plan: Phase 02 registry methodology framing for Chapter 4 §4.5 (TQ-03)

This plan replaces the bootstrap stub at commit `1ffb4df1`. T00 (draft PR bootstrap + stub) is already complete. Tasks T01–T06 below carry execution forward.

## Scope

Add a NEW thesis subsection §4.5 to `thesis/chapters/04_data_and_methodology.md` that gives an examiner-defensible textual home to the SC2EGSet Phase 02 provisional feature-family registry artifact emitted by PR #216 (CSV + MD at `validated_through = V-9`, manifest token `partial_coverage_v9_baseline`, with the deferred-dimension table and non-supersession-of-CROSS-02-01-v1.0.1 statement carried verbatim). The deliverable is bounded to: (a) inserting one new subsection §4.5 after Chapter 4 line 428 (within §4.4.6 closing paragraph) with a `---` separator, (b) appending one Chapter 4 row to `thesis/WRITING_STATUS.md`, (c) appending one Pending entry to `thesis/chapters/REVIEW_QUEUE.md`, (d) one `[3.54.0]` CHANGELOG block + `pyproject.toml` bump, (e) PR-body refresh + `gh pr ready 219`. The workstream is routed verbatim from `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` §11 row 5 + §12 TQ-03 (audit landed on master at `f1add6ce`).

## Problem Statement

`thesis/chapters/04_data_and_methodology.md` currently has no §4.5 section: Chapter 4 ends at line 428 (closing paragraph of §4.4.6 `[PRE-canonical_slot]` flag). PR #216 (merged into master) landed a provisional feature-family registry artifact for SC2EGSet under `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`, but the thesis methodology chapter does not yet acknowledge its existence, name its boundaries, or warn the examiner against reading it as a feature catalog or as Phase 02 closure. The §10.5 missing-claim row and §11 / §12 TQ-03 of the writing-readiness audit identify this gap as MEDIUM severity (HIGH for the per-dataset asymmetry sub-claim). Adding §4.5 must NOT (i) flip any STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS YAML, (ii) modify `docs/TAXONOMY.md`, (iii) claim Step 02_01_01 closure, (iv) claim final feature catalog, (v) claim leakage-free materialized features, (vi) claim aoestats / aoe2companion Phase 02 parity, (vii) claim any model-ready matrix.

Critical terminology constraint. The phrase "registry artifact" is NOT a formal taxonomy unit in `docs/TAXONOMY.md` (verified — grep `"registry artifact"` returned no match; only the formal "artifact" definition exists as a Step output under `## The three-level work hierarchy`). The future §4.5 Polish prose must define the deliverable as *prowizoryczny artefakt rejestru rodzin cech* (provisional feature-family registry artifact) / *rejestr rodzin cech* (feature-family registry) without implying a new repo taxonomy unit, and without editing `docs/TAXONOMY.md` (default no-touch; reviewer-deep may flag a TAXONOMY revision but the plan does NOT pre-approve one).

## Literature context

The §4.5 prose stays inside the repository's own evidence surface plus one external citation already in `thesis/references.bib`. No new bib entries are required.

Internal evidence: (a) the registry CSV + MD pair at `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/` (PR #216 emission, 26 data rows × 14 columns including the appended `block` column); (b) the manifest token vocabulary at `thesis/pass2_evidence/notebook_regeneration_manifest.md:12` and the PR-216 row at line 73; (c) the four LOCKED Phase 02 specs (CROSS-02-00-v3.0.1, CROSS-02-01-v1.0.1, CROSS-02-02-v1.0.1, CROSS-02-03-v1.0.1) defining the input contract / post-materialization audit / engineering plan / design-time audit dimensions D1–D15; (d) the audit document `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` §10.4 row 2 / §10.5 rows 1+3+4+5 / §10.6 row 5 / §11 row 5 / §12 TQ-03 (routing source); (e) `thesis/pass2_evidence/methodology_risk_register.md` RISK-21 wording for tracker-derived feature handling.

External citation: `[Bialecki2023]` (already in `thesis/references.bib:5` — Białecki et al. 2023, *SC2EGSet: StarCraft II Esport Replay and Game-state Dataset*, Scientific Data 10(1):600, DOI 10.1038/s41597-023-02510-7). Cited at most once in §4.5 to identify the underlying corpus. No other external citation is load-bearing; the framing is internal-evidence-anchored because the registry artifact is a within-repo emission, not a literature claim.

Cross-reference posture. §4.5 must connect back to §4.3.3 "Walidacja semantyczna strumienia `tracker_events_raw` (Step 01_03_05; GATE-14A6 — narrowed)" (Chapter 4 lines 333–351, drafted in PR #218) at the locus where in-game-snapshot families enter the registry. The cross-reference is **read-only against §4.3.3** — the writer-thesis must NOT promote any of the 3 `blocked_until_additional_validation` tracker families (`mind_control_event_count`, `army_centroid_at_cutoff_snapshot`, `playerstats_cumulative_economy_fields`) into §4.5 prose as Phase-02-ready, and must NOT collapse the GATE-14A6 outcome from `narrowed` to `closed`. The 3 blocked rows appear in the registry CSV (rows 25–27) only with `status = blocked_until_additional_validation` and `block = gate_and_blocked`; that classification is the only allowed framing in §4.5.

[OPINION] Polish title — **user-resolved (P01, 2026-05-17).** The approved title is:

**`## 4.5 Rejestr rodzin cech Phase 02 — prowizoryczny artefakt walidowany do V-9`**

This is a Chapter 4 **top-level numbered section** (two hashes `##`), sibling to §4.1, §4.2, §4.3, §4.4 — NOT a child subsection of §4.4.6 (which would be `### 4.5`). The title intentionally avoids `skeleton` to satisfy FC19. The phrase "prowizoryczny artefakt rejestru rodzin cech" is descriptive prose, not a formal TAXONOMY unit. No `docs/TAXONOMY.md` edit is required or authorized.

## Assumptions & unknowns

- **Assumption:** Master HEAD at planning-author time is `f1add6ce` (PR #217 audit merge). PR #219 HEAD is `1ffb4df1` (T00 bootstrap commit). No intervening master merges land between plan acceptance (post-T01) and writer-thesis dispatch (T02). If a master merge lands between T01 and T02 that touches `04_data_and_methodology.md`, `WRITING_STATUS.md`, `notebook_regeneration_manifest.md`, the registry CSV/MD, or any Phase 02 status YAML, T02 halts pending plan-side review.
- **Assumption:** The registry CSV at `02_01_01_feature_family_registry.csv` remains at 27 lines (1 header + 26 data) and 14 columns. The registry MD at `02_01_01_feature_family_registry.md` retains the `validated_through = V-9`, `closure_status = partial`, `manifest_status_token = partial_coverage_v9_baseline`, and non-supersession lines exactly as read at planning time. Writer-thesis verifies these line-level invariants before drafting.
- **Assumption:** `thesis/pass2_evidence/notebook_regeneration_manifest.md` retains line 12 (token definition) and line 73 (PR #216 row) unchanged. Writer-thesis verifies.
- **Assumption:** SC2EGSet `STEP_STATUS.yaml` does NOT acquire a `02_01_01` entry between T01 and T02. SC2EGSet `PIPELINE_SECTION_STATUS.yaml` does NOT acquire a `02_01` entry. SC2EGSet `PHASE_STATUS.yaml` Phase 02 stays `not_started`. aoestats + aoe2companion `PHASE_STATUS.yaml` Phase 02 both stay `not_started`. Writer-thesis verifies all three datasets' Phase 02 status at draft time.
- **Assumption:** No AoE2 Phase 02 ROADMAP execution begins between plan-author time and writer-thesis dispatch. If aoestats or aoe2companion `02_01_01` is materialized, the §4.5 per-dataset asymmetry claim must be re-scoped — halt and re-plan.
- **Unknown:** Final Polish title for §4.5. Resolves at: writer-thesis chooses among the three candidates in Literature context; default = (1). reviewer-adversarial verifies the chosen title carries the provisional + V-9 anchors.
- **Unknown:** Whether the writer-thesis draft will inline the deferred-dimension table or summarize it in prose. Plan-side decision: inline the table verbatim from registry MD lines 44–56 (the 11-row table) inside §4.5, because the audit §10.5 row 4 explicitly names "explicit enumeration" as the missing claim. reviewer-deep verifies inline table parity with registry MD.
- **Unknown:** Whether the §4.5 prose enumerates all 26 registry rows. Plan-side decision: do NOT enumerate all rows; cite the 5 + 6 + 4 + 7 + 4 = 26 block distribution from registry MD §"Row counts by block" (lines 117–124) and pick at most 1 example per block as a representative anchor. reviewer-deep verifies no row-by-row enumeration.
- **Unknown:** Whether the §4.5 prose modifies the `thesis/THESIS_STRUCTURE.md` outline. Plan-side decision: NO — THESIS_STRUCTURE.md is OUT OF SCOPE for this PR (the §4.5 row is added to `WRITING_STATUS.md` only). A separate Cat E PR may later sync THESIS_STRUCTURE.md if user requests; for this PR THESIS_STRUCTURE.md stays untouched.

## Required claim surface

The 21 claim anchors below are verbatim from the dispatch and verified anchor-by-anchor against on-disk evidence (Section 2 of the planner's chat output). The future §4.5 prose MUST carry each anchor. writer-thesis dispatch (T02) MUST receive this list verbatim in its prompt; reviewer-deep (T03) verifies every anchor is present in the drafted prose; reviewer-adversarial (T04) stress-tests the framing.

**Terminology (anchors 1–2)**
1. A Step artifact is a notebook-produced output under `reports/artifacts/`, NOT a new taxonomy unit. Evidence: `docs/TAXONOMY.md` §"The three-level work hierarchy" (lines 17–110) and §"Operational terms" (lines 166–203); "registry artifact" string is absent from TAXONOMY.md.
2. The SC2EGSet `02_01_01_feature_family_registry.csv` + `.md` files are the **provisional feature-family registry artifacts** (Polish: *prowizoryczny artefakt rejestru rodzin cech*). Evidence: registry MD line 1 title.

**Shape and content (anchors 3–7)**
3. The registry has **26 data rows** and **14 columns**: 13 required registry columns + appended `block` column. Evidence: registry CSV line count = 27; header line 1 lists `feature_family_id,dataset_tag,prediction_setting,source_table_or_event_family,source_grain,model_input_grain,target_grain,temporal_anchor,allowed_cutoff_rule,candidate_leakage_modes,cold_start_handling,status,per_player_construction,block`.
4. The registry contains feature-family **declarations**, NOT feature **values**. Evidence: registry MD line 1 verbatim; no row in the CSV contains a numeric or boolean value, only declaration strings.
5. The registry is NOT a model-ready feature matrix. Evidence: registry MD §"Step 02_01_01 closure status — partial" lines 69–80.
6. The registry is NOT a final feature catalog. Evidence: registry MD line 1 verbatim "provisional, validated through V-9".
7. The registry is NOT a replacement for feature materialization. Evidence: registry MD §"Non-supersession of the post-materialization audit" lines 58–67.

**Validators and provisional status (anchors 8–10)**
8. `validated_through = V-9` means V-1..V-9 structural validators passed at the **registry-skeleton layer**. Evidence: registry MD §"What V-1..V-9 mechanically enforce" table at lines 20–28; provenance row at line 100.
9. V-9 is a structural guard on `per_player_construction = "symmetric"` for model-input rows. Evidence: registry MD lines 28–36 verbatim "V-9 admits exactly one non-blocked token (`symmetric`). It is a structural guard against future drift, not a violation detector against the current 26-row skeleton".
10. The artifact is provisional with `manifest_status_token = partial_coverage_v9_baseline` (verbatim). Evidence: `thesis/pass2_evidence/notebook_regeneration_manifest.md:12` token definition + line 73 PR-216 row binding.

**Non-closure invariants (anchors 11–14)**
11. Step 02_01_01 remains OPEN. Evidence: `STEP_STATUS.yaml` contains no `02_01_01` entry (only `01_01_01` through `01_06_04`); registry MD line 76 verbatim "STEP_STATUS.yaml is unchanged".
12. Pipeline Section 02_01 remains NOT complete. Evidence: `PIPELINE_SECTION_STATUS.yaml` lists only `01_01..01_06` (line 51 comment: "Pipeline sections for Phases 02-06 added when those Phases become active").
13. Phase 02 remains NOT complete. Evidence: `PHASE_STATUS.yaml` lines 22–24 `"02": status: not_started`.
14. STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS were intentionally **not flipped** by PR #216. Evidence: registry MD §"Step 02_01_01 closure status — partial" lines 69–80 explicit non-flip wording.

**Deferred dimensions and CROSS-02-01 non-supersession (anchors 15–19)**
15. Deferred dimensions include D2, D3, D4-in_game, D5_in_game, D6-full, D8, D9, D10-sub-2, D12, D14, D15 (as represented in the registry MD companion). Evidence: registry MD table at lines 44–56 enumerates all 11 dimensions; the writer-thesis MUST inline this table verbatim (or reformat as a thesis-typeset table preserving the same 4 columns "Dim / Title / Status here / Commitment path" and all 11 rows).
16. D2/D3/D4-in_game/D5-in_game/D6-full/D8/D9 are resolved through materialization + CROSS-02-01-v1.0.1 audit, NOT more registry-layer validators. Evidence: registry MD lines 82–92 verbatim under §"Commitment path for resolving deferred dimensions before thesis defense".
17. D10-sub-2 / D12 / D14 / D15 are N/A for SC2EGSet at this stage or are AoE2-side. Evidence: registry MD rows 53–56 of the deferred-dimension table.
18. CROSS-02-01-v1.0.1 post-materialization audit remains MANDATORY for any tracker-derived or aggregate column the registry triggers materialization of. Evidence: registry MD §"Non-supersession" lines 58–67; spec `reports/specs/02_01_leakage_audit_protocol.md:3` `status: LOCKED`.
19. The registry's `validated_through = V-9` status does NOT excuse a materialized column from CROSS-02-01-v1.0.1. Evidence: registry MD lines 64–67 verbatim.

**Cross-game asymmetry (anchor 20)**
20. AoE2 Phase 02 is NOT yet comparable: aoestats and aoe2companion have ROADMAP stubs only, no registry artifact. Evidence: aoestats `PHASE_STATUS.yaml` Phase 02 `not_started`; aoe2companion `PHASE_STATUS.yaml` Phase 02 `not_started`; aoestats ROADMAP line 1748+ Phase 02 stub with verbatim "NOT DELIVERED IN THIS ROADMAP-STUB PR" language at the `02_01_01` description.

**Cross-reference to §4.3.3 (anchor 21)**
21. §4.5 must connect back to §4.3.3 (tracker eligibility) WITHOUT promoting blocked tracker families (`mind_control_event_count`, `army_centroid_at_cutoff_snapshot`, `playerstats_cumulative_economy_fields`). Evidence: §4.3.3 already lives at chapter 4 lines 333–351; the 3 blocked families appear in registry CSV rows 25–27 carrying `status = blocked_until_additional_validation` + `block = gate_and_blocked`; §4.3.3 line 339 already cross-references the registry MD.

## Forbidden claims for writer-thesis

Verbatim from dispatch + cross-referenced to Forbidden Claims F1–F18 in `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` §8. writer-thesis prompt MUST embed this list verbatim. reviewer-deep + reviewer-adversarial verify every entry holds in the drafted prose.

| # | Forbidden phrasing | Audit cross-ref |
|---|--------------------|-----------------|
| FC1 | "Phase 02 complete" or any equivalent | F4 (Step/Phase closure) |
| FC2 | "Step 02_01_01 closed" / "Step 02_01_01 jest zamknięty" | F4 |
| FC3 | "Final feature catalog" / "ostateczny katalog cech" | F3 |
| FC4 | "Leakage-free features" / "cechy wolne od wycieku" | F7 |
| FC5 | "Model-ready matrix" / "macierz gotowa dla modelu" | F3 |
| FC6 | "Feature values computed" / "wartości cech wyliczone" | F3 / F7 |
| FC7 | "CROSS-02-01 already satisfied" / "CROSS-02-01 już spełniony" | F7 / F8 |
| FC8 | "AoE2 Phase 02 parity" / "parytet faz 02 dla AoE2" | F5 |
| FC9 | "Registry artifact is a taxonomy unit" / treating *artefakt rejestru* as a new TAXONOMY term | TAXONOMY |
| FC10 | "V-1..V-9 cover all D1–D15" or any totalizing-validator claim | CROSS-02-03 / registry MD |
| FC11 | General "additional V-N validators are unnecessary" — only the audit-permitted framing "the adjudicated stopping rule halted further registry-layer validators before this provisional artifact" (or equivalent Polish wording) is allowed | registry MD §"Commitment path" lines 82–92 |
| FC12 | Promoting any of the 3 `blocked_until_additional_validation` tracker families as Phase-02-ready | RISK-21 + registry CSV rows 25–27 |
| FC13 | Collapsing GATE-14A6 outcome from `narrowed` to `closed` | §4.3.3 line 349 + WRITING_STATUS.md line 75 (DO NOT MODIFY) |
| FC14 | Any model-performance / accuracy / Brier / log-loss numeric claim | F1 |
| FC15 | Any tabular-vs-GNN claim or any model-comparison conclusion | F2 |
| FC16 | Any unqualified "ranked ladder" framing for aoestats or for the aoe2companion combined ID 6 + ID 18 scope | F10 / F11; AoE2 source-label discipline in `.claude/scientific-invariants.md` AoE2 section |
| FC17 | Any Friedman-omnibus-at-N=2 cross-game claim | F15 |
| FC18 | Any claim that flips a STATUS YAML or that requires a STATUS YAML flip to be true | repository state |
| FC19 | Registry-skeleton vs registry terminological consistency. Within §4.5, use ONE form consistently (e.g., *"rejestr rodzin cech (poziom V-9)"* OR *"artefakt rejestru rodzin cech na poziomie V-9"*); do NOT alternate. The approved chapter title avoids "skeleton" to enforce this discipline at the heading level. | P01 approved |
| FC20 | No "covers all D1–D15" cross-reference leakage. Forbid Polish equivalents *"pokrywa wszystkie wymiary D1–D15"* / *"adresuje wszystkie wymiary projektowe"*. Allowed phrasing: "mechanically enforces a subset of D1–D15 (D1, D5/D6 history-side, D7, D10-sub-1, D11, D13, D15); defers D2, D3, D4-in_game, D5-in_game, D6-full, D8, D9 to materialization + CROSS-02-01-v1.0.1; declares D10-sub-2, D12, D14, D15 as N/A or AoE2-side". | P01 approved |
| FC21 | No implicit "Phase 02 ready" framing via cross-reference composition. Forbid Polish verbs *"zapewniona"*, *"zabezpieczona"*, *"gotowa"*, *"kompletna"* (or English "ready", "complete", "secured", "ensured") when describing Phase 02 status. | P01 approved |
| FC22 | No "provisional" phrasing with positive valence implying near-completion. Polish *"prowizoryczny"* MUST be paired at first usage with a structural disqualifier ("satisfies clause 1 only of the 3-clause continue_predicate"). Do NOT use alongside *"bliskie ukończenia"* / *"prawie gotowe"* / *"wstępne"*. | P01 approved |
| FC23 | `partial_coverage_v9_baseline` must NOT be translated. The manifest token is a code-level identifier; gloss in Polish as *"token statusu `partial_coverage_v9_baseline`"* or *"określenie statusu w manifeście"*, NOT *"token częściowego pokrycia poziomu V-9"*. Elevated from OQ6. | P01 approved |
| FC24 | Prevent F-numbering drift recurrence. F1–F18 are canonical from audit §8. §4.5 prose MAY cite the audit in a footnote but MUST NOT renumber / refactor / re-label; use `audit §8 row F-N` format verbatim. | P01 approved |

## Halt conditions specific to this PR

Verbatim from dispatch (preserved in plan as load-bearing constraint).

- Halt if planner cannot reconcile "registry artifact" with TAXONOMY terminology. **Resolved at planning time:** TAXONOMY.md does NOT define "registry artifact"; §4.5 prose uses *prowizoryczny artefakt rejestru rodzin cech* / *rejestr rodzin cech* as descriptive Polish, not a taxonomy term. No TAXONOMY.md edit.
- Halt if §4.5 prose would require editing `docs/TAXONOMY.md`. **Resolved at planning time:** §4.5 does NOT require a TAXONOMY edit. If reviewer-deep or reviewer-adversarial discovers a TAXONOMY-edit need at T03/T04, T04b halts and re-plans (does not silently amend TAXONOMY.md).
- Halt if STATUS YAML semantics require a flip. **Resolved at planning time:** the prose explicitly carries non-closure anchors (11–14); no flip is required.
- Halt if reviewer-adversarial finds the provisional framing indefensible. T01 verdict gates T02; T04 verdict gates T04b/T05; if either round finds the framing indefensible, halt and re-plan.
- Halt if writer-thesis attempts to write outside §4.5 + minimal cross-reference scope. T03 verifies file scope; only the 5 files in the File Manifest may be touched.
- Halt if any prose implies closure / finality. T03 verifies all 24 forbidden-claim items (FC1–FC24).
- Halt if any of the 21 required-claim anchors is NOT supported by repo evidence. Verified at planning time (Section 2 of planner's chat output, all 21 SUPPORTED). T02 verifies again before drafting.
- Halt if `02_01_01_feature_family_registry.csv` shape ≠ 26 data rows × 14 columns. Verified at planning time (`wc -l` = 27; header has 14 fields). T02 re-verifies before drafting.
- Halt if PHASE_STATUS / PIPELINE_SECTION_STATUS / STEP_STATUS shows any closure (Phase 02 / section 02_01 / step 02_01_01) for SC2EGSet. Verified at planning time (all three uphold non-closure). T02 re-verifies before drafting.
- Halt if AoE2 PHASE_STATUS shows Phase 02 = `in_progress` or `complete` for aoestats or aoe2companion. Verified at planning time (both `not_started`). T02 re-verifies before drafting.

## Hard constraints for writer-thesis dispatch

These are non-negotiable. T02 dispatch prompt MUST embed all of the following.

- **Insertion locus.** New §4.5 is inserted into `thesis/chapters/04_data_and_methodology.md` after line 428 (closing paragraph of §4.4.6) with a blank line + `---` separator + blank line + the approved heading `## 4.5 Rejestr rodzin cech Phase 02 — prowizoryczny artefakt walidowany do V-9`. No edits to lines 1–428. No edits to any line after the new §4.5 block (there are no lines after 428 currently; the chapter ends at 428). **Chapter 4 top-level numbered sections use `##`.** §4.5 must be a sibling top-level section after §4.4, not a child subsection of §4.4.6. The writer-thesis validation must grep for `^## 4\.5`.
- **File scope per T02.** Only the 5 files in the File Manifest may be touched: `thesis/chapters/04_data_and_methodology.md`, `thesis/WRITING_STATUS.md`, `thesis/chapters/REVIEW_QUEUE.md`, `CHANGELOG.md` (T05 only), `pyproject.toml` (T05 only). Writer-thesis touches the first three at T02; T05 touches the last two.
- **No THESIS_STRUCTURE.md edit.** Out of scope for this PR.
- **No `docs/TAXONOMY.md` edit.** Out of scope unless reviewer-deep mandates at T03; default = no-touch.
- **No `thesis/pass2_evidence/**` edit.** All Pass-2 evidence files are read-only inputs to T02.
- **No other chapter file edit.** §4.5 lives entirely inside Chapter 4; no edits to chapters 01–03 or 05–07.
- **No status-YAML / ROADMAP / research-log / spec / notebook / agent / `.claude/` rule edit.**
- **No bib entry add.** `[Bialecki2023]` already at `thesis/references.bib:5`. No new bibkey required.
- **Length target.** §4.5 prose between **5,000 and 7,500 polskich znaków** including spaces (matches the §4.3.3 reference length of ~6,600 znaków drafted in PR #218). 4 bolded subsections recommended, mirroring §4.3.3 paragraph rhythm: (a) *Status artefaktu i prowizoryczność* (anchors 1–2, 5–7, 10), (b) *Co rejestr zawiera, a czego nie zawiera* (anchors 3–4, 8–9), (c) *Wymiary odroczone i nie-zastępowanie audytu post-materializacyjnego* (anchors 15–19), (d) *Asymetria fazy 02 między korpusami i powiązanie z §4.3.3* (anchors 11–14, 20–21). Length is a soft target; writer-thesis may deviate ±20% if the argument requires it.
- **Voice and register.** Argumentative, not descriptive (per `.claude/author-style-brief-pl.md` §"Cechy do świadomej korekty" — przejście z opisowego na argumentacyjne). Bezosobowy rejestr akademicki (przeprowadzono, zaobserwowano, stwierdzono). Inline `[REVIEW: ...]` flags are PERMITTED for genuine Pass-2 verification needs only; do NOT plant flags as drafting placeholders.
- **Must justify (alternatives-considered paragraphs).** (i) Why include §4.5 now rather than wait for materialization step 02_01_02. Alternative considered: defer §4.5 entirely to a post-materialization PR. Rejection rationale: PR #216 emitted a Pass-2 visible artifact (`partial_coverage_v9_baseline` token in `notebook_regeneration_manifest.md`); leaving §4.5 absent would leave the manifest token unanchored in the thesis methodology chapter. (ii) Why the registry sits at validator level V-9 rather than V-10 or higher. Alternative considered: continue adding registry-layer validators until all D1–D15 are mechanically covered. Rejection rationale: registry MD §"Commitment path" lines 82–92 explicitly route the deferred dimensions to materialization + CROSS-02-01-v1.0.1, not to further registry-layer validators. (iii) Why a CROSS-02-01 mandatory cross-reference is needed inside §4.5 rather than relying on §4.3.3 / §4.4.4 cross-references. Alternative considered: place CROSS-02-01 framing only in the §4.4.x audit-methodology section. Rejection rationale: registry MD §"Non-supersession" lines 58–67 explicitly attach the CROSS-02-01 mandatoriness to the registry artifact itself; the bond is registry-local, not audit-local.
- **Must contrast (literature comparison).** Not applicable in load-bearing form for §4.5 (the section is internal-evidence-anchored, not literature-anchored). One half-paragraph may compare the *feature-registry* design pattern to the broader *feature-store* / *feature-registry* concept enumerated in audit §6.4 (Tecton / Feast / Databricks-tier feature stores), but only as one sentence at most, and only to underline that the SC2EGSet registry is a methodological discipline artifact, NOT a feature-store implementation. No bibkey is added for this comparison (audit §6.4 itself does not gate-keep external references for this PR).
- **Must cite (key references).** One external citation: `[Bialecki2023]` for the SC2EGSet corpus identifier, cited at most once. Six internal cross-references (path-form, not bibkey-form): (a) registry CSV path; (b) registry MD path; (c) `thesis/pass2_evidence/notebook_regeneration_manifest.md` (token); (d) `reports/specs/02_01_leakage_audit_protocol.md` (CROSS-02-01-v1.0.1); (e) `reports/specs/02_03_temporal_feature_audit_protocol.md` (CROSS-02-03-v1.0.1 dimensions); (f) Chapter 4 §4.3.3 (tracker eligibility cross-ref).
- **Numerical-consistency discipline (per `.claude/rules/thesis-writing.md` Critical Review Checklist Data variant).** Every numeric claim traces to a repo artifact path verbatim. Counts to assert: 26 data rows; 14 columns; 13 required columns + 1 appended `block`; 5 + 6 + 4 + 7 + 4 block distribution; 11 deferred-dimension rows in the inline table (rows for D2, D3, D4-in_game, D5-in_game, D6-full, D8, D9, D10-sub-2, D12, D14, D15). NO numeric values beyond these counts may appear (no percentages, no validator pass-rates, no row IDs except up to 3 representative example feature-family IDs, one each from `pre_game`, `history_enriched_pre_game`, `in_game_now`; NEVER from `gate_and_blocked` for the 3 blocked tracker rows).
- **REVIEW_QUEUE.md entry shape.** One new Pending row added to `thesis/chapters/REVIEW_QUEUE.md` §"Pending Pass 2 reviews" with: section path (§4.5), drafted-date (2026-05-17), flag count (likely 0 if no `[REVIEW:]` flags planted; otherwise the actual count), Pass-2 verification questions if any (e.g., whether §4.5's CROSS-02-01 cross-reference language matches the audit-protocol spec wording).
- **WRITING_STATUS.md entry shape.** One new row added to the "Chapter 4 — Data and Methodology" table after the existing §4.4.6 / §4.3.2 / §4.3.3 rows: `| §4.5 ... | DRAFTED | Phase 02 (PR #216 SC2EGSet provisional registry artifact) | Drafted 2026-05-17. Provisional framing; non-supersession verbatim. ~X.X k znaków polskich. N [REVIEW] flags. ... |`. DO NOT modify the existing line 75 GATE-14A6 wording for §4.3.3 row. DO NOT modify any other WRITING_STATUS.md row.

## Reviewer-specific concerns

**reviewer-deep at T01 (plan review) + T03 (drafted-prose review) must verify:**
- Terminology does not contradict `docs/TAXONOMY.md` — specifically, *prowizoryczny artefakt rejestru rodzin cech* is descriptive Polish, not a new taxonomy unit; no `docs/TAXONOMY.md` edit is proposed.
- All numeric claims (26 data rows, 14 columns, 13 + 1 split, 5+6+4+7+4 block distribution, 11 deferred-dimension table rows) trace to the registry CSV / MD verbatim.
- Deferred-dimension prose / table matches registry MD lines 44–56 verbatim (rows + columns).
- STATUS-YAML no-touch is framed correctly in the drafted prose — non-closure is asserted, but the prose does NOT claim that any YAML *should* be flipped or *will* be flipped at a specific later date (those forward claims belong in research_log / ROADMAP, not in the thesis methodology chapter).
- AoE2 Phase 02 stubs-only claim is accurate — drafted prose names aoestats ROADMAP line 1748+ stub and aoe2companion ROADMAP Phase 02 stub, with both `PHASE_STATUS.yaml` Phase 02 = `not_started`.
- File scope is bounded to the 5 manifest files; no other thesis chapter or repo file is touched.
- Bibkeys: only `[Bialecki2023]` cited externally, with no new bib entry added.

**reviewer-adversarial at T01 (plan review) + T04 (drafted-prose review) must stress-test the following 6 examiner scenarios verbatim:**
- **Scenario A — "isn't this just a final feature catalog?"** Defence anchor: registry MD line 1 "provisional, validated through V-9"; registry CSV declares family strings, not values; the `status` column carries `allowed_with_caveat` / `sanity_gate_not_model_input` / `blocked_until_additional_validation` for many rows. Forbidden-claim list FC3 / FC5 / FC6 govern.
- **Scenario B — "if V-9 passed, why is Step still open?"** Defence anchor: registry MD §"Step 02_01_01 closure status — partial" lines 69–80 verbatim — the `continue_predicate` for Step 02_01_01 is a 3-clause conjunction; V-9 satisfies clause 1 (artifact-check) only. Clauses 2 and 3 (CROSS-02-01-v1.0.1 post-materialization re-run; per-family CROSS-02-03-v1.0.1 §10 verdicts) remain unsatisfied. Audit §8 F4 governs.
- **Scenario C — "why write about Phase 02 before materializing features?"** Defence anchor: PR #216 emitted a Pass-2-visible artifact (`partial_coverage_v9_baseline` in `notebook_regeneration_manifest.md`); the thesis must give the manifest token a textual home. The drafted prose explicitly frames §4.5 as methodology-discipline, NOT results — no model-performance claim, no materialized-feature claim, no leakage-clearance claim. Audit §8 F1 / F7 / F8 govern.
- **Scenario D — "why not do AoE2 registry first?"** Defence anchor: aoestats + aoe2companion `PHASE_STATUS.yaml` Phase 02 = `not_started`; aoestats ROADMAP line 1748+ Step `02_01_01` carries verbatim "NOT DELIVERED IN THIS ROADMAP-STUB PR". The §4.5 per-dataset asymmetry anchor (20) explicitly names the asymmetry and forbids parity claims (FC8 / F5). Sequencing is a workstream decision, not a parity claim.
- **Scenario E — "does this leak future info?"** Defence anchor: a registry artifact is a declaration set, not a materialized value set; the CSV contains no observation-level numbers from any game T. Invariant I3 (no feature for game T uses information from game T or later) is structurally inapplicable to the artifact under audit. The post-materialization CROSS-02-01-v1.0.1 audit is invoked verbatim as mandatory for any later materialization.
- **Scenario F — "are you hiding unresolved D-dimensions under a provisional label?"** Defence anchor: the deferred-dimension table (anchor 15, 11 rows) is inlined verbatim. Each deferred dimension has an explicit commitment path per registry MD lines 82–92 — D2/D3/D4-in_game/D5-in_game/D6-full/D8/D9 → materialization + CROSS-02-01-v1.0.1; D10-sub-2/D12/D14/D15 → N/A for SC2EGSet or AoE2-side. The "provisional" framing is transparently load-bearing, not a hiding device. FC10 / FC11 govern.

## Execution Steps

T00 is complete (bootstrap commit `1ffb4df1`). Tasks T01–T06 below carry execution forward. Every task that produces or modifies content commits + pushes per the PR-first rule; T01 critique persistence and T04 critique persistence are explicit commits; T05 is the release commit; T06 makes the PR ready via the GitHub API only (no commit).

---

### T01 — reviewer-deep + reviewer-adversarial review of THIS plan (parallel)

**Objective:** Gate the plan content itself before any drafting begins. reviewer-deep verifies structural and scope-discipline correctness; reviewer-adversarial verifies methodological defensibility against the 6 examiner scenarios.

**Instructions:**
1. Parent session dispatches `@reviewer-deep` and `@reviewer-adversarial` in parallel, both reading `planning/current_plan.md` (this file, post-replacement) at branch `thesis/phase02-registry-methodology-section-4-5` HEAD.
2. `@reviewer-deep` prompt MUST include: (a) the 21 required-claim anchors verbatim from §"Required claim surface"; (b) the 24 forbidden-claim items verbatim from §"Forbidden claims for writer-thesis" (FC1–FC24; FC19–FC24 added by P01 post-T01); (c) the 9 halt conditions verbatim from §"Halt conditions specific to this PR"; (d) the 9 hard constraints verbatim from §"Hard constraints for writer-thesis dispatch"; (e) the 7 reviewer-deep checks verbatim from §"Reviewer-specific concerns"; (f) the file scope (5 allowed files) verbatim from §File Manifest. **Note: T01 already completed with FC1–FC18; FC19–FC24 fold into T03 dispatch.**
3. `@reviewer-adversarial` prompt MUST include: (a) all of (a)–(d) above; (b) the 6 examiner scenarios verbatim from §"Reviewer-specific concerns"; (c) instruction to stress-test the provisional framing — does it survive examination?
4. Both reviewers return a combined verdict (PASS / PASS-WITH-NOTES / REQUIRE-REVISION / BLOCK). Parent session aggregates verdicts. If reviewer-adversarial returns BLOCK or REQUIRE-REVISION, halt and re-plan. If reviewer-deep returns BLOCK or REQUIRE-REVISION but reviewer-adversarial passes, parent decides whether to re-plan or proceed with deep-review fixes embedded into the plan. Combined verdict requires user approval before T02.
5. Persist the reviewer-adversarial output to `planning/current_plan.critique.md` as the load-bearing critique artifact (reviewer-adversarial is responsible for writing this file per its agent contract). Commit both reviewer outputs in one commit: `docs(planning): reviewer-deep + reviewer-adversarial verdicts for PR 219 plan`. Push to PR #219.
6. HALT FOR USER APPROVAL before any T02 dispatch.

**Verification:**
- `planning/current_plan.critique.md` exists at HEAD and carries the reviewer-adversarial verdict + the 6 examiner-scenario stress tests.
- A separate reviewer-deep verdict file (path: `planning/current_plan.reviewer-deep.md` — optional; or inline notes within `current_plan.critique.md` under a "reviewer-deep findings" appendix) records reviewer-deep verdicts.
- User confirms in chat: "Plan approved, dispatch writer-thesis."

**File scope:**
- `planning/current_plan.critique.md` (reviewer-adversarial writes)
- `planning/current_plan.reviewer-deep.md` (reviewer-deep writes, optional path)

**Read scope:**
- `planning/current_plan.md` (this file post-replacement)
- All 36 source_artifacts listed in frontmatter

**Model routing:** reviewer-deep = Opus (sub-agent default per `.claude/rules/data-analysis-lineage.md` agent-routing discipline; structural correctness + spec compliance + invariant tracing). reviewer-adversarial = Opus (methodology-defensibility check; required for Cat F per `docs/templates/planner_output_contract.md`).

**Stop condition:** Halt for user approval. Do NOT proceed to T02 without explicit user confirmation in chat.

---

### T02 — writer-thesis drafts §4.5 (after T01 PASS + user approval)

**Objective:** Draft the new §4.5 subsection of Chapter 4 carrying all 21 required-claim anchors and avoiding all 24 forbidden claims (FC1–FC24; FC19–FC24 user-approved at P01). Update WRITING_STATUS.md (new §4.5 row) and REVIEW_QUEUE.md (new Pending row).

**Instructions:**
1. Parent session re-verifies (one-line bash each) immediately before T02 dispatch: (a) registry CSV line count = 27 and column count = 14; (b) registry MD `validated_through = V-9` and `manifest_status_token = partial_coverage_v9_baseline` still present; (c) `STEP_STATUS.yaml` does NOT contain `02_01_01`; (d) `PIPELINE_SECTION_STATUS.yaml` does NOT list `02_01`; (e) `PHASE_STATUS.yaml` Phase 02 = `not_started`; (f) aoestats + aoe2companion `PHASE_STATUS.yaml` Phase 02 both = `not_started`; (g) `thesis/pass2_evidence/notebook_regeneration_manifest.md` line 12 + line 73 unchanged; (h) Chapter 4 ends at line 428.
2. If any verification fails, HALT and re-plan. Do NOT dispatch writer-thesis.
3. Parent session dispatches `@writer-thesis` (Opus required — methodology-load-bearing) with the following embedded verbatim in the prompt:
   - The 21 required-claim anchors from §"Required claim surface".
   - The 24 forbidden-claim items from §"Forbidden claims for writer-thesis" (FC1–FC24, including user-approved FC19–FC24 from P01).
   - The 9 halt conditions from §"Halt conditions specific to this PR".
   - The 9 hard constraints from §"Hard constraints for writer-thesis dispatch", including: insertion locus (after Chapter 4 line 428 + `---` separator + approved `## 4.5` heading), file scope (3 files this task touches; CHANGELOG + pyproject.toml deferred to T05), length target (5,000–7,500 znaków), voice register (argumentative, bezosobowy akademicki polski), 4 bolded-subsection structure (a)/(b)/(c)/(d).
   - The 3 alternatives-considered paragraphs from §"Must justify".
   - The 1 external citation `[Bialecki2023]` (no new bibkey).
   - The 6 internal cross-references (paths).
   - The numerical-consistency discipline: 26 data rows, 14 columns, 13 + 1 split, 5+6+4+7+4 block distribution, 11 deferred-dimension table rows; max 3 representative feature-family IDs cited (one per non-blocked block); NEVER from `gate_and_blocked`.
   - Polish title: user-approved (P01, 2026-05-17) = `## 4.5 Rejestr rodzin cech Phase 02 — prowizoryczny artefakt walidowany do V-9` (top-level `##` heading; no `skeleton` wording; no alternative titles permitted).
   - WRITING_STATUS.md row shape from §"Hard constraints".
   - REVIEW_QUEUE.md entry shape from §"Hard constraints".
   - DO NOT modify WRITING_STATUS.md line 75 (GATE-14A6 wording for §4.3.3 row).
   - DO NOT touch `docs/TAXONOMY.md`, any `thesis/pass2_evidence/**` file, any other thesis chapter, any STATUS YAML, any ROADMAP, any research_log, any spec, any notebook, any agent file, any `.claude/` rule.
   - **Envelope tightenings (P01-approved, mandatory for T02 dispatch):**
     1. **Cited-as-of-SHA HTML comment discipline** (PR #218 precedent). At the top of §4.5 insert: `<!-- Cited-as-of-SHA: master @ f1add6ce -->` + `<!-- Registry CSV: <SHA-at-T02-time> -->` + `<!-- Registry MD: <SHA-at-T02-time> -->` + `<!-- notebook_regeneration_manifest.md: <SHA-at-T02-time> -->`. Populate the SHAs at T02 time by running `git log --format="%H" -1 -- <file-path>` for each artifact file.
     2. **4-vs-3 `gate_and_blocked` row disambiguation.** When citing the block distribution, state explicitly: "`gate_and_blocked` has 4 rows total; 3 are `blocked_until_additional_validation`, 1 is the `slot_identity_consistency` sanity gate (not a model-blocking row)."
     3. **"Provisional" glossing discipline.** At first usage of *prowizoryczny*, pair it with the structural disqualifier: "satisfies clause 1 only of the 3-clause continue_predicate". Forbid synonymy with "preliminary/draft/interim/near-final".
     4. **Why §4.5 lives in Chapter 4 (methodology) not Chapter 5 (results).** Include one explicit sentence rationale (e.g., the registry is a declaration artifact — a methodological discipline commitment — not an empirical result or a materialised feature value).
     5. **No temporal-progression framing for AoE2 asymmetry.** Use "differential per-dataset progress profile"; forbid "lagging", "behind", "pending", "will catch up", "priorities".
     6. **Registry-skeleton vs registry terminological consistency** per FC19 (one form only throughout §4.5).
     7. **F-number citation discipline** per FC24 (use `audit §8 row F-N` verbatim; do not renumber).
4. After writer-thesis completes drafting, commit + push: `docs(thesis): add Chapter 4 §4.5 Phase 02 registry methodology framing (provisional, V-9)`.
5. Run Chat Handoff Summary per `.claude/rules/thesis-writing.md` §"Chat Handoff Summary Format" Data-fed sections variant.

**Verification:**
- `git diff master -- thesis/chapters/04_data_and_methodology.md` shows additions only after line 428 (no edits to lines 1–428).
- `git diff master -- thesis/WRITING_STATUS.md` shows exactly one new row added in the Chapter 4 table; line 75 (GATE-14A6 wording) byte-identical to master.
- `git diff master -- thesis/chapters/REVIEW_QUEUE.md` shows exactly one new Pending entry.
- No file outside the 3-file scope (T02 portion of the Manifest) is touched.
- `grep -c "partial_coverage_v9_baseline" thesis/chapters/04_data_and_methodology.md` returns ≥ 1.
- `grep -c "validated_through = V-9" thesis/chapters/04_data_and_methodology.md` returns ≥ 1 (or the Polish phrasing equivalent if writer-thesis chose to localize the validator name — reviewer-deep verifies localization is faithful).
- `grep -cE "(Step 02_01_01.*(closed|zamknięt)|(zamknięt|closed).*Step 02_01_01)" thesis/chapters/04_data_and_methodology.md` returns 0 (forbidden-claim FC2 holds).
- `wc -m` on the §4.5 prose extracted from chapter file is in the 5,000–7,500 range (soft target ± 20%).

**File scope (T02 writes):**
- `thesis/chapters/04_data_and_methodology.md`
- `thesis/WRITING_STATUS.md`
- `thesis/chapters/REVIEW_QUEUE.md`

**Read scope (T02 reads):**
- All 36 source_artifacts in frontmatter (writer-thesis reads the evidence; T02 does NOT re-read every Pass-2 evidence document but DOES read the registry CSV, registry MD, manifest, audit §10.4–§12, registry research log entry, all four LOCKED Phase 02 specs, Chapter 4 in full, `.claude/author-style-brief-pl.md`, `.claude/rules/thesis-writing.md`).

**Model routing:** writer-thesis = Opus (methodology-load-bearing per `.claude/rules/data-analysis-lineage.md`).

**Stop condition:** writer-thesis draft committed + pushed to PR #219. Chat Handoff Summary produced.

---

### T03 — reviewer-deep on drafted §4.5 prose

**Objective:** Verify drafted prose against the 7 reviewer-deep checks listed in §"Reviewer-specific concerns".

**Instructions:**
1. Parent session dispatches `@reviewer-deep` against the drafted prose at PR #219 HEAD (post-T02 commit).
2. reviewer-deep prompt MUST include: (a) the 21 required-claim anchors verbatim; (b) the 24 forbidden-claim items verbatim (FC1–FC24; FC19–FC24 user-approved at P01); (c) the 9 hard constraints verbatim; (d) the 7 reviewer-deep checks verbatim from §"Reviewer-specific concerns".
3. reviewer-deep returns verdict (PASS / PASS-WITH-NOTES / REQUIRE-REVISION / BLOCK) with per-anchor + per-forbidden-claim accounting.
4. If REQUIRE-REVISION or BLOCK, T04b fixes; otherwise proceed to T04.

**Verification:**
- reviewer-deep output cites all 21 anchors as PRESENT in the drafted prose.
- reviewer-deep output cites all 24 forbidden claims as ABSENT in the drafted prose.
- reviewer-deep output cites all 7 reviewer-deep checks as PASS.
- File scope verified by `git diff` against the 3 manifest files only.

**File scope:** (no writes — review only; verdict persisted in chat or in `planning/current_plan.t03.md` if parent chooses)

**Read scope:**
- `thesis/chapters/04_data_and_methodology.md` (post-T02 HEAD)
- `thesis/WRITING_STATUS.md` (post-T02 HEAD)
- `thesis/chapters/REVIEW_QUEUE.md` (post-T02 HEAD)
- Registry CSV / MD (evidence verification)
- Manifest file (evidence verification)

**Model routing:** reviewer-deep = Opus.

**Stop condition:** verdict produced. Halt for parent decision (T04 directly if PASS or PASS-WITH-NOTES; T04b first if REQUIRE-REVISION).

---

### T04 — reviewer-adversarial on drafted §4.5 prose (6 examiner scenarios)

**Objective:** Stress-test the drafted prose against the 6 examiner scenarios (A–F) listed in §"Reviewer-specific concerns".

**Instructions:**
1. Parent session dispatches `@reviewer-adversarial` against drafted prose at PR #219 HEAD (post-T02 commit, post-T03 fixes if any).
2. reviewer-adversarial prompt MUST include: (a) the 21 required-claim anchors verbatim; (b) the 24 forbidden-claim items verbatim (FC1–FC24; FC19–FC24 user-approved at P01); (c) the 6 examiner scenarios verbatim from §"Reviewer-specific concerns"; (d) explicit instruction to attempt the most aggressive examiner reading — does the provisional framing survive?; (e) **two additional P01-approved sentence-surface checks:**
   - **Sentence-level upgrade-in-meaning check.** Scan every sentence for paraphrases that subtly upgrade "provisional → effectively complete", "narrowed → effectively closed", "deferred → handled". These upgrades are NOT covered by grep-based forbidden-phrase checks and must be detected manually.
   - **Cross-reference reading test.** Read §4.3.3 + §4.5 as a continuous narrative. Verify that no sentence in §4.5, *combined with* §4.3.3, produces an implicit "Phase 02 is ready" claim. The two sections must compose without leaking readiness.
3. reviewer-adversarial returns per-scenario verdict + overall verdict (PASS / PASS-WITH-NOTES / REQUIRE-REVISION / BLOCK). Per `.claude/rules/data-analysis-lineage.md` agent-routing discipline, the 3-round adversarial cap applies symmetrically — if T04 returns REQUIRE-REVISION twice in a row after T04b fixes, escalate to user; if T04 returns BLOCK, halt and re-plan.
4. Persist verdict to `planning/current_plan.critique.md` (append to T01 critique under a new `## T04 — drafted-prose adversarial review` heading). Commit: `docs(planning): reviewer-adversarial verdict on §4.5 drafted prose (PR 219)`.

**Verification:**
- `planning/current_plan.critique.md` carries the T04 per-scenario stress test + overall verdict.
- Each of the 6 examiner scenarios is named verbatim in the critique.
- The defence anchor for each scenario is cited verbatim from the drafted prose (line-anchored).

**File scope:**
- `planning/current_plan.critique.md` (append-only)

**Read scope:** same as T03.

**Model routing:** reviewer-adversarial = Opus.

**Stop condition:** verdict produced + committed + pushed. Halt for parent decision.

---

### T04b — mechanical fix-up (conditional on T03 / T04 verdicts)

**Objective:** Apply mechanical fixes if T03 or T04 returns REQUIRE-REVISION with bounded, mechanical-edit findings (e.g., one forbidden phrase to remove, one anchor to add back, one numeric to align).

**Instructions:**
1. Skip T04b if both T03 and T04 return PASS or PASS-WITH-NOTES.
2. If T03 returns REQUIRE-REVISION: writer-thesis (Sonnet permitted — fix is mechanical) applies the bounded fix in `thesis/chapters/04_data_and_methodology.md` (and possibly `thesis/WRITING_STATUS.md` if numeric counts need re-counting). Commit: `docs(thesis): T04b mechanical fix for §4.5 per T03 reviewer-deep verdict`.
3. If T04 returns REQUIRE-REVISION: writer-thesis (Opus required — methodology defensibility) applies the bounded fix. Commit: `docs(thesis): T04b mechanical fix for §4.5 per T04 reviewer-adversarial verdict`.
4. Re-dispatch T03 and/or T04 against the post-fix HEAD. If the re-dispatch returns REQUIRE-REVISION a second time, escalate to user per the 3-round adversarial cap.
5. If T03 or T04 returns BLOCK at any round, halt and re-plan.

**Verification:**
- `git diff HEAD~1` shows only the mechanical fix (no scope creep).
- Re-dispatched T03 and/or T04 returns PASS or PASS-WITH-NOTES.

**File scope:**
- `thesis/chapters/04_data_and_methodology.md` (if §4.5 prose fix)
- `thesis/WRITING_STATUS.md` (if WRITING_STATUS row fix)
- `thesis/chapters/REVIEW_QUEUE.md` (if REVIEW_QUEUE entry fix)

**Read scope:** same as T03.

**Model routing:** writer-thesis on Sonnet (for T03-bound fixes — mechanical) OR Opus (for T04-bound fixes — methodology-defensibility).

**Stop condition:** T03 and T04 both PASS / PASS-WITH-NOTES after at most 2 fix-up rounds. Otherwise escalate to user.

---

### T05 — CHANGELOG `[3.54.0]` block + version bump 3.53.0 → 3.54.0

**Objective:** Land the release entry per `.claude/rules/git-workflow.md`. Minor bump because Category F docs prose addition.

**Instructions:**
1. Update `CHANGELOG.md`: move `[Unreleased]` content (currently empty per inspection at line 12) into a new `## [3.54.0] — 2026-05-17 (PR #219: thesis/phase02-registry-methodology-section-4-5)` block under the existing `## [Unreleased]` header. Block content (1 line each):
   - **Added:** `thesis/chapters/04_data_and_methodology.md` — NEW §4.5 "Rejestr rodzin cech Phase 02 — prowizoryczny artefakt walidowany do V-9" carrying the SC2EGSet provisional feature-family registry artifact (PR #216) at `validated_through = V-9` with manifest token `partial_coverage_v9_baseline`, deferred-dimension table (11 rows), non-supersession of CROSS-02-01-v1.0.1 post-materialization audit, and per-dataset Phase 02 asymmetry framing. Routed from `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` §11 row 5 / §12 TQ-03.
   - **Added:** `thesis/WRITING_STATUS.md` — one Chapter 4 row for §4.5 (status DRAFTED).
   - **Added:** `thesis/chapters/REVIEW_QUEUE.md` — one Pending Pass 2 entry for §4.5.
2. Update `pyproject.toml` line 3: `version = "3.53.0"` → `version = "3.54.0"`.
3. Leave `[Unreleased]` empty with `Added/Changed/Fixed/Removed` headers per git-workflow §4.
4. Commit: `chore(release): bump version to 3.54.0`. Push to PR #219.

**Verification:**
- `grep -n "## \[3.54.0\]" CHANGELOG.md` returns one match.
- `grep "^version" pyproject.toml` returns `version = "3.54.0"`.
- `[Unreleased]` block is empty with Added/Changed/Fixed/Removed headers preserved.
- pre-commit hooks (ruff, mypy) pass — neither runs on this PR's content (no .py files modified) but the hook framework runs; if hooks fail for unrelated reasons, diagnose and fix per `.claude/rules/git-workflow.md`.

**File scope:**
- `CHANGELOG.md`
- `pyproject.toml`

**Read scope:**
- `CHANGELOG.md` (read current state to choose insertion point)
- `pyproject.toml` (read current version)

**Model routing:** executor on Sonnet (mechanical version bump + CHANGELOG entry; plan resolves all decisions).

**Stop condition:** version bumped + CHANGELOG block added + committed + pushed.

---

### T06 — PR body refresh + `gh pr ready 219`

**Objective:** Mark PR #219 ready for merge after writing the final PR body via the `.github/tmp/pr.txt` discipline.

**Instructions:**
1. Write final PR body content to `.github/tmp/pr.txt` per `.claude/rules/git-workflow.md` PR Body Format. Sections: `## Summary` (4–5 bullets — what was added, evidence anchors, non-supersession discipline, scope discipline), `## Motivation` (audit §11 row 5 + §12 TQ-03 routing; PR #216 manifest token requires textual anchor), `## Test plan` (checkable items: §4.5 inserted; anchors present; forbidden phrases absent; status-YAML untouched; TAXONOMY.md untouched; pre-commit hooks pass), footer line per template.
2. `gh pr edit 219 --body-file .github/tmp/pr.txt`. Verify body update via `gh pr view 219 --json body`.
3. `gh pr ready 219`. Verify draft state flipped via `gh pr view 219 --json isDraft`.
4. `rm -f .github/tmp/pr.txt` per memory `feedback_pr_body_cleanup` (after PR creation cleanup).
5. NO commit at T06 (PR body and ready-flip are GitHub-API operations, not git operations).

**Verification:**
- `gh pr view 219 --json isDraft` returns `{"isDraft":false}`.
- `gh pr view 219 --json body` returns a body containing the four sections (Summary / Motivation / Test plan / footer).
- `.github/tmp/pr.txt` removed after PR body update.

**File scope:**
- `.github/tmp/pr.txt` (created then removed within T06)

**Read scope:**
- `CHANGELOG.md` (post-T05 HEAD — pull bullet text for Summary)
- `thesis/chapters/04_data_and_methodology.md` (verify §4.5 final form)
- `planning/current_plan.md` (this plan — anchors + scope)
- `planning/current_plan.critique.md` (T01 + T04 critique outcomes for Summary mention)

**Model routing:** executor on Sonnet (mechanical PR body authoring + GitHub API calls).

**Stop condition:** PR #219 is marked ready; user notified.

---

## File Manifest

Allowed file touches across T01–T06. Every file touched by any task is listed exactly once; no other file may be modified, created, or deleted.

| File | Action | Task(s) |
|------|--------|---------|
| `planning/current_plan.md` | Rewrite (this file replaces the bootstrap stub) | planner-science (this output) |
| `planning/current_plan.critique.md` | Create (T01) + Update (T04 append) | T01 (reviewer-adversarial), T04 (reviewer-adversarial) |
| `planning/current_plan.reviewer-deep.md` | Create (optional; reviewer-deep T01 verdict) | T01 (reviewer-deep, optional path) |
| `thesis/chapters/04_data_and_methodology.md` | Update (NEW §4.5 inserted after line 428; lines 1–428 byte-identical to master) | T02, T04b (if revision required) |
| `thesis/WRITING_STATUS.md` | Update (one row added to Chapter 4 table; line 75 byte-identical to master) | T02, T04b (if revision required) |
| `thesis/chapters/REVIEW_QUEUE.md` | Update (one Pending entry added) | T02, T04b (if revision required) |
| `CHANGELOG.md` | Update (new `[3.54.0]` block + cleared `[Unreleased]`) | T05 |
| `pyproject.toml` | Update (`version = "3.54.0"`) | T05 |
| `.github/tmp/pr.txt` | Create then delete within T06 | T06 |

**Forbidden file touches** (any modification triggers BLOCK at reviewer-deep or reviewer-adversarial gates):
- `docs/TAXONOMY.md` (default no-touch; reviewer-deep may flag a need, but the default plan posture is no-touch)
- `docs/PHASES.md`, `docs/INDEX.md`, `docs/templates/**`
- `thesis/THESIS_STRUCTURE.md`
- `thesis/pass2_evidence/**` (all 14+ files — read-only inputs)
- `thesis/references.bib` (no new bibkey)
- Any other `thesis/chapters/*.md` (01, 02, 03, 05, 06, 07)
- Any `reports/specs/**` file
- Any STATUS YAML (`STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`) for any dataset
- Any `ROADMAP.md` for any dataset
- Any `research_log.md` for any dataset (including the SC2EGSet log at the registry-artifact entry)
- Any `INVARIANTS.md` for any dataset
- Any notebook (`sandbox/**/*.py`, `sandbox/**/*.ipynb`)
- Any code under `src/**`
- Any agent definition under `.claude/agents/**`
- Any rule under `.claude/rules/**`
- Any registry artifact CSV / MD (the artifacts themselves — read-only inputs)
- Any data file under `data/` or `raw/`

## Gate Condition

PR #219 may be merged when ALL of the following observable conditions hold:

- **Chapter 4 §4.5 exists.** `grep -nE "^## 4\.5" thesis/chapters/04_data_and_methodology.md` returns exactly one match at line > 428.
- **All 21 required-claim anchors are PRESENT in §4.5 prose.** Verified by reviewer-deep at T03 with per-anchor accounting; recorded in T03 verdict.
- **All 24 forbidden-claim phrasings are ABSENT in §4.5 prose (FC1–FC24).** Verified by reviewer-deep at T03 and reviewer-adversarial at T04 with per-item accounting.
- **The 6 reviewer-adversarial examiner scenarios all return defensible verdicts** (PASS or PASS-WITH-NOTES). Recorded in T04 critique.
- **WRITING_STATUS.md carries one new Chapter 4 §4.5 row** with status DRAFTED; line 75 (GATE-14A6 wording for §4.3.3) byte-identical to master.
- **REVIEW_QUEUE.md carries one new Pending entry** for §4.5.
- **No file outside the File Manifest is touched.** Verified by `git diff master --name-only` returning a subset of the 8 manifest paths (+ `planning/current_plan.md` itself).
- **`docs/TAXONOMY.md` is byte-identical to master.** Verified by `git diff master -- docs/TAXONOMY.md` returning empty.
- **No STATUS YAML is flipped.** Verified by `git diff master -- src/rts_predict/games/*/datasets/*/reports/PHASE_STATUS.yaml src/rts_predict/games/*/datasets/*/reports/PIPELINE_SECTION_STATUS.yaml src/rts_predict/games/*/datasets/*/reports/STEP_STATUS.yaml` returning empty.
- **No registry artifact is modified.** Verified by `git diff master -- src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.{csv,md}` returning empty.
- **Version bumped to 3.54.0** in `pyproject.toml`; `[3.54.0]` CHANGELOG block present; `[Unreleased]` empty with headers.
- **PR #219 is no longer a draft.** `gh pr view 219 --json isDraft` returns `{"isDraft":false}`.

## Out of scope

- THESIS_STRUCTURE.md — does not include §4.5 currently; updating it is OUT OF SCOPE for this PR. A separate Cat E PR may sync it later if user requests.
- `docs/TAXONOMY.md` — default no-touch; the term *prowizoryczny artefakt rejestru rodzin cech* is descriptive Polish, not a new taxonomy unit.
- Materialization Step 02_01_02 — does not exist yet; out of scope. No claim that this PR triggers its execution.
- CROSS-02-01-v1.0.1 post-materialization audit re-run — cannot occur until at least one feature column is materialized. Out of scope.
- aoestats and aoe2companion `02_01_01` registry artifacts — out of scope. The §4.5 prose names their absence per anchor 20; the prose does NOT promise their delivery on any date.
- §4.3.2 stale-paragraph repair — already executed in PR #218 (audit §10.2 row C2.1). Out of scope for this PR.
- §4.4.3 leakage audit subsection — separate audit PR (audit §9.4); out of scope.
- §4.4.4 within-game / cross-game subsection enhancements — separate audit PR; out of scope.
- Population-scope harmonization sweep (audit §9.3) — separate PR; out of scope.
- Any new bibkey or any modification to `thesis/references.bib`.
- Any new external citation beyond `[Bialecki2023]`.
- Pass-2 verification of registry MD wording against the CROSS-02-03 spec — implicit-load. The plan asserts the registry MD inlines the dimension definitions consistently with CROSS-02-03-v1.0.1 §4 (spec rows for D1–D15 verified at planning time); writer-thesis does NOT re-verify against the spec at draft time.

## Open questions

- **OQ1 — Polish title choice.** **RESOLVED (P01, 2026-05-17).** User-approved title: `## 4.5 Rejestr rodzin cech Phase 02 — prowizoryczny artefakt walidowany do V-9`. No alternative titles. No `skeleton` wording. See §"Resolved user decisions before T02".
- **OQ2 — Whether to inline the deferred-dimension table or summarize it.** Plan-side decision: inline verbatim (11-row table from registry MD lines 44–56). Resolves at: writer-thesis follows plan default; reviewer-deep at T03 verifies inline-table parity with registry MD.
- **OQ3 — Whether to enumerate all 26 registry rows.** Plan-side decision: do NOT enumerate; cite the 5+6+4+7+4 block distribution and pick at most 1 example per non-blocked block. Resolves at: writer-thesis follows plan default; reviewer-deep at T03 verifies no row-by-row enumeration.
- **OQ4 — Whether the §4.5 prose modifies `thesis/THESIS_STRUCTURE.md`.** Resolved at planning time: NO; THESIS_STRUCTURE.md is OUT OF SCOPE for this PR. A separate Cat E PR may sync it later if user requests. reviewer-deep at T03 verifies no THESIS_STRUCTURE.md edit attempt.
- **OQ5 — Polish-language rendering of `validated_through = V-9`.** Two options: (i) keep the English literal `validated_through = V-9` as a code-level identifier; (ii) gloss in Polish as *zwalidowany do poziomu V-9* with the code-level identifier in parentheses. Resolves at: writer-thesis chooses; reviewer-deep at T03 verifies localization fidelity. Default = (ii).
- **OQ6 — Polish-language rendering of `partial_coverage_v9_baseline`.** **RESOLVED and ELEVATED TO FC23 (P01, 2026-05-17).** `partial_coverage_v9_baseline` must remain verbatim in §4.5 prose. Do NOT translate this token into Polish. Gloss in Polish as *"token statusu `partial_coverage_v9_baseline`"* or *"określenie statusu w manifeście"*; NOT *"token częściowego pokrycia poziomu V-9"*. This is now a forbidden-claim item (FC23) — see §"Forbidden claims for writer-thesis".
- **OQ7 — Whether to record a `research_log` entry for §4.5 drafting.** Per `.claude/rules/thesis-writing.md` Category F flow + `ARCHITECTURE.md` Progress Tracking, Cat F does NOT require a `research_log.md` update (Cat F updates `REVIEW_QUEUE.md` and `WRITING_STATUS.md`). Resolved at planning time: NO research_log entry; the registry-artifact research_log entry at sc2egset `research_log.md:5` already records the artifact emission. reviewer-deep at T03 verifies no research_log touch.

---

## Resolved user decisions before T02

All items below were resolved and approved by the user in P01 (2026-05-17) and are now binding constraints on T02 dispatch and all subsequent tasks.

**OQ1 resolved — Polish title (no skeleton wording).**
Approved title verbatim: `## 4.5 Rejestr rodzin cech Phase 02 — prowizoryczny artefakt walidowany do V-9`
- `##` = two hashes; top-level Chapter 4 section, sibling to §4.1–§4.4, NOT a child of §4.4.6.
- The title intentionally avoids `skeleton` to satisfy FC19.
- The phrase "prowizoryczny artefakt rejestru rodzin cech" is descriptive prose, not a formal TAXONOMY unit.
- No `docs/TAXONOMY.md` edit is required or authorized.
- writer-thesis validation must grep for `^## 4\.5`; any result for `^### 4\.5` is a FAIL.

**OQ6 resolved — manifest token verbatim (elevated to FC23).**
- `partial_coverage_v9_baseline` must remain verbatim in §4.5 prose.
- Do NOT translate this token into Polish.
- Gloss as *"token statusu `partial_coverage_v9_baseline`"* or *"określenie statusu w manifeście"*; NOT *"token częściowego pokrycia poziomu V-9"*.
- This token is now FC23 in the forbidden-claims list.

**FC19–FC24 approved** for fold-in to T02 writer-thesis dispatch prompt and T03/T04 reviewer prompts. See §"Forbidden claims for writer-thesis" table rows FC19–FC24 for verbatim text.

**9 envelope tightenings approved** — 7 for T02, 2 for T04:

*For T02 dispatch (7):*
1. Cited-as-of-SHA HTML comment discipline — anchor §4.5 to `master @ f1add6ce` + registry CSV/MD/manifest SHAs at T02 time.
2. 4-vs-3 `gate_and_blocked` row disambiguation — state explicitly: 4 rows total; 3 are `blocked_until_additional_validation`; 1 is `slot_identity_consistency` sanity gate (not a model-blocking row).
3. "Provisional" glossing discipline at first usage with structural disqualifier ("satisfies clause 1 only of the 3-clause continue_predicate"); forbid synonymy with "preliminary/draft/interim/near-final".
4. Why §4.5 lives in Chapter 4 (methodology) not Chapter 5 (results) — one-sentence rationale required.
5. No temporal-progression framing for AoE2 asymmetry — use "differential per-dataset progress profile"; forbid "lagging", "behind", "pending", "will catch up", "priorities".
6. Registry-skeleton vs registry terminological consistency per FC19.
7. F-number citation discipline per FC24.

*For T04 reviewer-adversarial dispatch (2):*
8. Sentence-level surface check for upgrade-in-meaning: scan every sentence for paraphrases that subtly upgrade "provisional → effectively complete", "narrowed → effectively closed", "deferred → handled".
9. Cross-reference reading test: read §4.3.3 + §4.5 as continuous narrative; verify no sentence in §4.5 combined with §4.3.3 produces implicit "Phase 02 is ready" claim.

**Cited-as-of-SHA HTML comment discipline approved** — anchors §4.5 to `master @ f1add6ce` + registry artifact SHAs at T02 time (per PR #218 precedent).

**writer-thesis remains NOT invoked** at planning time. T02 has not started.

---

## Critique instruction

For Category F, adversarial critique is required before execution. After this plan replaces the bootstrap stub, the parent session must dispatch `@reviewer-adversarial` AND `@reviewer-deep` in parallel (T01) to produce `planning/current_plan.critique.md` (reviewer-adversarial) and optional `planning/current_plan.reviewer-deep.md` (reviewer-deep). Both reviewers receive the 21 required-claim anchors, 18 forbidden-claim items, 9 halt conditions, 9 hard constraints, and the 6 examiner-scenario stress tests embedded in their prompts verbatim. Halt for user approval before T02.