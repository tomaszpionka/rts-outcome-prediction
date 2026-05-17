---
title: "Phase 01/02 Writing Readiness Audit (cross-dataset) — amended with existing-draft conformance audit"
category: E
branch: thesis/phase01-phase02-writing-readiness-audit
date: 2026-05-17
planner_model: claude-opus-4-7
branch_prefix: thesis/
branch_name: thesis/phase01-phase02-writing-readiness-audit
pr_title: "docs(thesis): Phase 01/02 writing readiness audit (cross-dataset; sc2egset+aoestats+aoe2companion) — amended with existing-draft conformance audit"
base_ref: "master @ e45ca996"
base_commit: e45ca996
created_date: 2026-05-17
dataset: multi
phase: "01+02"
pipeline_section: "n/a (cross-dataset, multi-phase audit)"
step: "n/a (Category E docs-only audit; no Step closure claimed)"
target_version: "3.52.2"
version_current: "3.52.1"
version_bump_type: "patch (Category E docs-only extension)"
critique_required: false
invariants_touched: []
source_artifacts:
  # Specs (LOCKED Phase 02 contract triplet + quad)
  - reports/specs/02_00_feature_input_contract.md
  - reports/specs/02_01_leakage_audit_protocol.md
  - reports/specs/02_02_feature_engineering_plan.md
  - reports/specs/02_03_temporal_feature_audit_protocol.md
  # Methodology + rules
  - CHANGELOG.md
  - planning/INDEX.md
  - planning/README.md
  - .claude/scientific-invariants.md
  - .claude/rules/data-analysis-lineage.md
  - .claude/rules/thesis-writing.md
  - docs/PHASES.md
  - docs/templates/plan_template.md
  - docs/templates/planner_output_contract.md
  # Existing audit (extended in this amendment)
  - thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md
  # Thesis tracking
  - thesis/WRITING_STATUS.md
  - thesis/THESIS_STRUCTURE.md
  - thesis/chapters/REVIEW_QUEUE.md
  # Thesis draft chapters (newly added for amendment conformance audit)
  - thesis/chapters/01_introduction.md
  - thesis/chapters/02_theoretical_background.md
  - thesis/chapters/03_related_work.md
  - thesis/chapters/04_data_and_methodology.md
  - thesis/chapters/05_experiments_and_results.md
  - thesis/chapters/06_discussion.md
  - thesis/chapters/07_conclusions.md
  # Pass-2 evidence consulted
  - thesis/pass2_evidence/phase01_closeout_summary.md
  - thesis/pass2_evidence/phase02_readiness_hardening.md
  - thesis/pass2_evidence/methodology_risk_register.md
  - thesis/pass2_evidence/notebook_regeneration_manifest.md
  - thesis/pass2_evidence/claim_evidence_matrix.md
  - thesis/pass2_evidence/cleanup_flag_ledger.md
  - thesis/pass2_evidence/aoe2_ladder_provenance_audit.md
  - thesis/pass2_evidence/cross_dataset_comparability_matrix.md
  - thesis/pass2_evidence/sec_4_1_crosswalk.md
  - thesis/pass2_evidence/sec_4_2_crosswalk.md
  - thesis/pass2_evidence/audit_cleanup_summary.md
  - thesis/pass2_evidence/literature_verification_log.md
  - thesis/pass2_evidence/reviewer_gate_report.md
  - thesis/pass2_evidence/dependency_lineage_audit.md
  - thesis/plans/writing_protocol.md
  # Per-dataset Phase 01/02 status YAMLs and ROADMAPs
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/PIPELINE_SECTION_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/PHASE_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PIPELINE_SECTION_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PHASE_STATUS.yaml
  # Phase 01 exploration trees (already cited; reaffirmed)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/ (full tree)
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/ (full tree)
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/ (full tree)
  # Phase 02 SC2EGSet provisional registry artifact (PR #216)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md
prior_executed_tasks:
  - id: T01
    description: "Authored 9-section audit at thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md (565 lines)"
    commit: b8716095
    status: complete
  - id: T02
    description: "CHANGELOG entry [3.52.1] — 2026-05-17 added"
    commit: faa6077d
    status: complete
  - id: T03
    description: "pyproject.toml version bumped 3.52.0 → 3.52.1"
    commit: faa6077d
    status: complete
  - id: T04
    description: "Reviewer-deep pass completed"
    verdict: PASS-WITH-NOTES (zero BLOCKERs)
    status: complete
research_log_ref: null
---

# Plan: Phase 01/02 Writing Readiness Audit (cross-dataset; sc2egset + aoestats + aoe2companion) — amended

## Scope

This PR delivers a single audit document — `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` — that (a) maps existing on-disk Phase 01 and Phase 02 evidence to thesis sections, ranks sections by drafting safety, and enumerates claims that MUST NOT appear in the thesis until their evidence exists (T01, completed at commit `b8716095`); and (b) **additionally compares the existing draft thesis prose under `thesis/chapters/` against current repository evidence after PR #216 merge**, enumerating the resulting backlog of corrections and a writing-agent task queue (T05–T07, this amendment). The audit is cross-dataset (sc2egset + aoestats + aoe2companion) and cross-phase (Phase 01 = complete for all three datasets; Phase 02 = SC2EGSet Step 02_01_01 provisional artifact emitted at `validated_through = V-9` per PR #216, aoestats and aoe2companion Phase 02 = ROADMAP stubs only). No methodology spec, status YAML, ROADMAP, notebook, or generated dataset artifact is changed; no thesis chapter prose is touched.

The PR is **Category E (docs-only)**. The deliverable is a Pass-2 evidence-track audit that will be consumed by future Category F writing PRs and by `@planner-science` when scoping any Phase 02 ROADMAP work.

**Amendment context (added 2026-05-17, target_version 3.52.2):** T01–T04 already delivered the 9 mapping sections of the audit document, an associated CHANGELOG/version bump to 3.52.1, and a reviewer-deep PASS-WITH-NOTES verdict (zero blockers). The user has now extended the audit's required scope: in addition to mapping evidence to *possible* thesis sections, the audit must also compare the **existing draft thesis prose** under `thesis/chapters/01_introduction.md` through `07_conclusions.md` against current repository evidence after PR #216 (provisional SC2EGSet V-9 registry artifact) merged. This amendment ADDS three new sections to the existing audit (one conformance audit section + two tables) and a corresponding version bump to 3.52.2. The conformance audit is read-only against thesis draft chapters; no chapter prose is modified. The plan amendment itself is committed to `planning/current_plan.md` and (if needed) `planning/current_plan.critique.md`; no thesis files are touched in the amendment commit.

## Execution Steps

### T01 — Write the audit document  [COMPLETED — commit b8716095]

**Objective:** Author `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` per the 9-section specification produced in the planning chat.

**Status:** Complete (565 lines, 9 sections). Frozen for this amendment except for **append-only** additions per T06 / T07 below.

---

### T02 — Update CHANGELOG.md  [COMPLETED — commit faa6077d]

**Status:** Complete. `[3.52.1] — 2026-05-17` block landed. This amendment will add a separate `[3.52.2]` block in T08 below.

---

### T03 — Bump pyproject.toml version  [COMPLETED — commit faa6077d]

**Status:** Complete (3.52.0 → 3.52.1). T08 of this amendment will bump 3.52.1 → 3.52.2.

---

### T04 — Reviewer-deep pass  [COMPLETED — verdict PASS-WITH-NOTES, zero blockers]

**Status:** Complete. T08 of this amendment will dispatch a fresh reviewer-deep gate covering the §10/§11/§12 append + CHANGELOG/version bump.

---

### T05 — Read existing draft chapters and pass2_evidence files; build the conformance evidence matrix in scratch space

**Objective:** Produce a per-chapter, per-section evidence inventory in scratch space (NOT in any thesis file, NOT in the audit document yet) that catalogues every claim in the existing draft prose whose conformance to current repository evidence needs verification. Output is a reading-and-classification deliverable that T06 will consume to author the audit §10 (conformance section).

**Instructions:**
1. Read every existing draft chapter file in full:
   - `thesis/chapters/01_introduction.md` (105 lines)
   - `thesis/chapters/02_theoretical_background.md` (233 lines)
   - `thesis/chapters/03_related_work.md` (193 lines)
   - `thesis/chapters/04_data_and_methodology.md` (408 lines)
   - `thesis/chapters/05_experiments_and_results.md` (77 lines — placeholders)
   - `thesis/chapters/06_discussion.md` (39 lines — placeholders)
   - `thesis/chapters/07_conclusions.md` (29 lines — placeholders)
2. Read every pass-2 evidence file that informs the conformance comparison:
   - `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` (existing 9 sections — the §10/§11/§12 append target)
   - `thesis/pass2_evidence/phase01_closeout_summary.md`
   - `thesis/pass2_evidence/phase02_readiness_hardening.md`
   - `thesis/pass2_evidence/methodology_risk_register.md`
   - `thesis/pass2_evidence/notebook_regeneration_manifest.md`
   - `thesis/pass2_evidence/claim_evidence_matrix.md`
   - `thesis/pass2_evidence/sec_4_1_crosswalk.md` + `sec_4_2_crosswalk.md`
   - `thesis/pass2_evidence/cross_dataset_comparability_matrix.md`
   - `thesis/pass2_evidence/aoe2_ladder_provenance_audit.md`
   - `thesis/pass2_evidence/audit_cleanup_summary.md`
   - `thesis/pass2_evidence/dependency_lineage_audit.md`
   - `thesis/pass2_evidence/literature_verification_log.md`
   - `thesis/pass2_evidence/reviewer_gate_report.md`
   - `thesis/pass2_evidence/cleanup_flag_ledger.md`
3. Read every locked CROSS-02 spec (CROSS-02-00-v3.0.1, CROSS-02-01-v1.0.1, CROSS-02-02-v1.0.1, CROSS-02-03-v1.0.1) at `reports/specs/02_0*.md`.
4. Read the SC2EGSet provisional V-9 registry artifact (CSV + MD) at `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
5. Read the active dataset state files: `PHASE_STATUS.yaml`, `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `ROADMAP.md`, `research_log.md` for sc2egset, aoestats, aoe2companion.
6. Read `thesis/WRITING_STATUS.md`, `thesis/THESIS_STRUCTURE.md`, `thesis/chapters/REVIEW_QUEUE.md`, `thesis/plans/writing_protocol.md`.
7. Build a scratch-space classification of every load-bearing claim found in the chapter prose. Use the six categories the user has specified (also enumerated in T06 below):
   - C1 Safe-and-supported (evidence exists; claim aligns)
   - C2 Stale / numerically outdated (evidence has moved; claim has not)
   - C3 Overclaims (claim asserts a closure or completeness not justified by evidence)
   - C4 Claims requiring caveats (claim is materially correct but missing a binding qualifier)
   - C5 Missing claims to add (current evidence supports a claim that no chapter currently makes)
   - C6 Exact proposed edits (proposed replacement for problematic wording, with evidence citation)
8. For each claim, capture the exact `file:line` location in the chapter file, the current wording (verbatim or summary), the relevant evidence artifact path, and the proposed category.
9. Halt and report (NOT proceed to T06) if any of the halt conditions in §Halt conditions specific to this amendment apply.

**Verification:**
- Scratch-space classification covers at minimum every chapter file from 01 through 07 (chapters 05–07 are expected to be "no draft prose" — record that explicitly).
- For Chapter 4, every drafted subsection (§4.1.1, §4.1.2.1, §4.1.2.2, §4.1.3, §4.1.4, §4.2.1, §4.2.2, §4.2.3, §4.4.4, §4.4.5, §4.4.6) appears in the classification with at least one row per drafted paragraph carrying a load-bearing claim.
- Every cited evidence artifact path is verified to exist on disk (`ls` spot-check at minimum for the 12 most-cited paths).
- Output is delivered as a chat report to the parent session — NOT written to any file. The parent session captures it for T06 use.

**File scope (writes):**
- (none — read-only deliverable in chat)

**Read scope:**
- All files listed in Instructions 1–6 above.

**Model routing:** **Opus required.** Methodology-load-bearing reading + cross-referencing existing draft claims against post-PR #216 evidence. Subtle reasoning about overclaim risk (e.g., distinguishing "Phase 02 ready" from "Step 02_01_01 closed" from "provisional V-9 artifact emitted"), distinguishing F4 closure language from F5 parity language, and recognizing AoE2 source-label discipline violations across chapters that previously underwent T11/T12/T13 cleanups.

**Stop condition:** Halt before T06 if (a) any cited draft chapter cannot be found on disk; (b) any pass-2 evidence file cited as input is empty or unreadable; (c) the conformance classification produces a category-C3 (overclaim) finding that requires methodology-level resolution before drafting the audit append.

---

### T06 — Append the "Existing draft conformance audit" section to the audit document

**Objective:** Append a new §10 ("Existing draft conformance audit") to `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md`, enumerating the six categories C1–C6 the user has specified, populated from the T05 scratch-space classification.

**Instructions:**
1. Confirm the T05 scratch-space classification is reviewed and accepted by the parent session (do NOT proceed if any T05 halt condition triggered).
2. Append a new top-level `## 10. Existing draft conformance audit` heading to `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` at line 562 (immediately before the existing `**End of audit document.**` line — relocate that line to the end of the new content).
3. Under §10, populate six sub-subsections — one per category, with `### 10.1` through `### 10.6` numbering:
   - **§10.1 Safe-and-supported claims.** Brief enumeration of chapters/sections whose drafted claims align with current evidence after PR #216 merge. Cite the evidence-source artifact for each. Examples expected: §1.1 50-civ DLC-roster hedge (post-T12); §4.1.1 SC2EGSet date range 2016–2024 (Tabela 4.4a); §4.1.2.1 aoestats Tier 4 source-label discipline; §4.1.2.2 aoe2companion mixed-mode (RISK-01/02/03 mitigated); §4.2.2 I2 5-branch identity resolution; §4.4.4 candidate-list within-game framing (PR-TG1); §4.4.5 ICC ANOVA values + estimator-choice defence; §4.4.6 `[PRE-canonical_slot]` flag scope.
   - **§10.2 Stale / numerically outdated claims.** Enumerate claims where evidence has changed since the chapter prose was written. At minimum:
     - `04_data_and_methodology.md` §4.3.2 lines ~330–331 — claim that Step 01_03_05 "nie została zrealizowana w obecnej iteracji"; evidence: Step 01_03_05 complete 2026-05-05 per `phase01_closeout_summary.md` + PR #208 + GATE-14A6 outcome `narrowed`.
     - Any chapter location citing EsportsBench v7.0 or v9.0 (Pass-2 local-closure already moved to v8.0 / cutoff 2025-12-31 per §2.5.5 + §3.2.4 row notes in `WRITING_STATUS.md`). The audit must report exact `grep` results for "v7.0", "v8.0", "v9.0", "2025-09-30", "2025-12-31", "2026-03-31" across `02_theoretical_background.md`, `03_related_work.md` to confirm whether any stale citation remains.
     - Any other stale numeric claim surfaced by T05.
   - **§10.3 Overclaims.** Enumerate **forbidden-claim risk** locations where chapter prose currently asserts (or in placeholder comments invites future drafters to assert) closures or completenesses that the existing audit §8 Forbidden-Claims list (F1–F18) prohibits. At minimum verify:
     - No chapter currently claims "Phase 02 closure" / "Step 02_01_01 closure" / "final feature catalog" (F3/F4).
     - No chapter currently claims "leakage-free materialized features" (F7/F8).
     - No chapter currently claims "model-ready feature matrix" (F3).
     - No chapter currently claims "cross-game generalizability" without the four-confound disclaimer (RQ3 hedge per T12).
     - No chapter currently asserts "tabular vs GNN" conclusions (F2).
     - Placeholder comments in `05_experiments_and_results.md`, `06_discussion.md`, `07_conclusions.md` are advisory only and do NOT count as overclaims; record them as "future-PR risk anchors."
   - **§10.4 Claims requiring caveats.** Enumerate locations where the draft prose is materially correct but missing a binding qualifier. At minimum:
     - SC2EGSet registry provisional V-9 caveat (if §4.5 is drafted in any future Category-F PR, MUST cite as provisional alongside CROSS-02-01-v1.0.1 — currently absent from chapter prose entirely; cross-listed in §10.5).
     - CROSS-02-01-v1.0.1 post-materialization audit binding (currently described abstractly in §4.4.4 candidate-list framing; the binding-for-Phase-02 language is not yet present anywhere).
     - AoE2 Phase 02 = ROADMAP stubs only (chapter prose does not yet say this; future §4.5 drafter must include).
     - AoE2 source-label discipline (already mostly applied; spot-check §4.1.2.2 vs §4.1.4 for any residual unqualified "ranked ladder" wording).
     - SC2 tracker scope narrowed not closed (GATE-14A6 `narrowed`; verify §4.3.2 + §4.4 do not say "closed").
   - **§10.5 Missing claims to add.** Enumerate claims that current evidence supports but no chapter currently makes. At minimum:
     - PR #216 provisional registry artifact existence + status `partial_coverage_v9_baseline`.
     - V-1..V-9 validation baseline mechanical coverage + the per-row "structural guard against future drift" framing for V-9.
     - `notebook_regeneration_manifest.md` row `partial_coverage_v9_baseline` token.
     - Deferred-dimension table (D2, D3, D4-in_game, D5-in_game, D6-full, D8, D9 — resolved at materialization step 02_01_02 via CROSS-02-01 post-materialization audit).
     - Non-supersession disclaimer (registry's `validated_through = V-9` does NOT excuse a materialized column from CROSS-02-01-v1.0.1).
   - **§10.6 Exact proposed edits.** For every row across §10.1–§10.5 that requires a chapter edit, list a structured row containing: (a) `file path` (chapter file repo-relative); (b) `section heading` (the §X.Y heading or "NEW section §X.Y" if absent); (c) `current problematic wording` (verbatim quote, or "absent" for missing-claim rows); (d) `recommended replacement claim` (precise wording for the writing agent to draft); (e) `evidence citation` (artifact path supporting the replacement); (f) `severity` (BLOCKER / HIGH / MEDIUM / LOW); (g) `writing agent to handle it` (one of: writer-thesis, planner-science-then-writer-thesis, defer-to-Phase-02-completion).
4. Apply ISO `YYYY-MM-DD` dates everywhere.
5. Apply repo-relative paths everywhere.
6. Move the existing `**End of audit document.**` line to the end of the new content; do NOT delete it.

**Verification:**
- `wc -l thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` shows a meaningful line-count increase reflecting six sub-subsections of conformance content.
- `grep -n "^## 10\. " thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` returns exactly 1 line.
- `grep -nE "^### 10\.[1-6] " thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` returns exactly 6 lines.
- Every `evidence citation` field in §10.6 resolves to an existing on-disk path (spot-check ≥ 6 random rows via `ls`).
- `**End of audit document.**` appears exactly once and at the file end (`tail -1` confirms).
- No `[REVIEW:]`, `[NEEDS CITATION]`, `[UNVERIFIED:]`, `[OPINION]`, or `[NEEDS JUSTIFICATION]` flag appears in the new §10 content (this is pass-2 evidence consolidation, not thesis prose requiring flag-driven validation).

**File scope (writes):**
- `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` (append §10)

**Read scope:**
- Same as T05 read scope; the parent session reuses the T05 reading rather than re-fetching.

**Model routing:** **Opus required.** Methodology-load-bearing prose; subtle reasoning about overclaim risk (especially §10.3 + §10.4); per-row routing decisions across writing agents in §10.6. A Sonnet executor risks misclassifying a "claim requiring caveat" as a "stale claim" or miscatalogising a forbidden-claim risk as an overclaim.

**Stop condition:** Halt before §11 / §12 (T07) if (a) any §10.6 row cannot be backed by an existing on-disk evidence artifact; (b) any §10.6 row would silently introduce thesis prose (this section is an evidence-track audit, not a thesis chapter draft); (c) any §10.6 row would direct a touch of `thesis/chapters/*.md`.

---

### T07 — Append the two required tables (§11 Draft correction backlog, §12 Writing agent task queue) to the audit document

**Objective:** Append a new §11 ("Draft correction backlog") and a new §12 ("Writing agent task queue") immediately after §10. Both tables are populated from the T06 §10.6 rows plus the T05 scratch-space classification; this task is the explicit per-row routing decision, not a re-classification.

**Instructions:**
1. Confirm T06 §10 is reviewed and accepted by the parent session.
2. Append `## 11. Draft correction backlog` immediately after §10. The section opens with a brief 2–3 sentence paragraph clarifying that this table is the actionable consequence of the §10 conformance audit, that every row routes to a future PR, that no row authorises edits in this PR (which is Category E docs-only), and that aoestats/aoe2companion-specific rows must preserve source-label discipline. Then a single table follows with the columns specified below.
3. **Draft correction backlog (table 11.A) — required columns:**
   - `thesis_file` (repo-relative path)
   - `section` (§X.Y heading)
   - `issue_type` (one of: stale, overclaim, missing-caveat, missing-claim, source-label-violation)
   - `severity` (BLOCKER / HIGH / MEDIUM / LOW)
   - `current_claim` (verbatim quote, or "absent" for missing-claim rows)
   - `corrected_claim` (precise replacement wording)
   - `evidence_source` (artifact path or paths; repo-relative)
   - `reviewer_required` (one of: reviewer, reviewer-deep, reviewer-adversarial)
   - `writing_agent_handoff_note` (one or two sentences explaining what the writing agent must NOT do; e.g., "Do NOT close GATE-14A6 narrative without re-reading `phase02_readiness_hardening.md` §14A.6" or "Do NOT introduce v9.0 EsportsBench citation without WebFetch verification of HuggingFace commit log")
4. Append `## 12. Writing agent task queue` immediately after §11. The section opens with a brief 2–3 sentence paragraph clarifying that each task in the queue corresponds to one or more rows of §11, that every task names the writing agent that handles it, that every task names the forbidden claims (typically a subset of §8 Forbidden Claims F1–F18), and that the queue is the authoritative routing artifact for any future Category-F drafting PR scoped against PR #216 evidence.
5. **Writing agent task queue (table 12.A) — required columns:**
   - `task_id` (TQ-01, TQ-02, ...)
   - `agent_to_use` (one of: writer-thesis, planner-science-then-writer-thesis, defer)
   - `target_thesis_file_or_section` (e.g., `thesis/chapters/04_data_and_methodology.md` §4.5 NEW, or `thesis/chapters/04_data_and_methodology.md` §4.3.2 lines ~330–331)
   - `allowed_evidence_sources` (semicolon-separated artifact paths)
   - `forbidden_claims` (semicolon-separated F-numbers from existing audit §8, optionally with extra row-specific prohibitions)
   - `reviewer_routing` (one of: reviewer, reviewer-deep, reviewer-adversarial)
   - `expected_output` (one or two sentences describing the PR deliverable)
6. Apply ISO `YYYY-MM-DD` dates everywhere; apply repo-relative paths everywhere; keep `**End of audit document.**` exactly once at the file end.

**Verification:**
- `grep -nE "^## (11|12)\. " thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` returns exactly 2 lines.
- Draft correction backlog (§11) has ≥ 1 row for every chapter file in which §10 surfaced an overclaim, stale claim, or missing-caveat finding.
- Writing agent task queue (§12) is non-empty.
- Every row of §12 (`agent_to_use`) names a concrete agent (`writer-thesis` etc.) and a non-empty `forbidden_claims` cell (at minimum one F-number).
- Every `evidence_source` cell across §11 and §12 resolves to an existing on-disk path (spot-check ≥ 6 random rows).
- No row in either table cites a thesis file outside `thesis/chapters/` for editing (audit content lives in `thesis/pass2_evidence/`; the audit document IS the spec for future writing PRs).

**File scope (writes):**
- `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` (append §11 + §12)

**Read scope:**
- Same as T05 / T06; the parent session reuses the prior reads.

**Model routing:** **Opus required.** Per-row routing of writing agents + per-row forbidden-claim enforcement is methodology-load-bearing. A row routed to `writer-thesis` that should have been routed to `planner-science-then-writer-thesis` (e.g., the §4.5 NEW section, where methodology design must precede prose) would invite a future overclaim PR. A row missing a forbidden-claim cell would underconstrain the writing agent and risk reintroducing F-numbers.

**Stop condition:** Halt before T08 if (a) any backlog row lacks `evidence_source`; (b) any task-queue row lacks `forbidden_claims`; (c) any row would touch `thesis/chapters/*.md` in this PR.

---

### T08 — CHANGELOG entry + version bump 3.52.1 → 3.52.2 + reviewer-deep gate

**Objective:** Record the amendment under `[3.52.2] — 2026-05-17` and dispatch reviewer-deep for final gate.

**Instructions:**
1. Move existing `[Unreleased]` empty headers down.
2. Add a new `[3.52.2] — 2026-05-17 (PR #217 amendment: docs/thesis-phase01-phase02-writing-readiness-audit)` block under `Added` with one bullet: "Existing-draft conformance audit appended to `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` as §10 (six-category conformance comparison of existing draft chapter prose against post-PR #216 repository evidence) + §11 (Draft correction backlog) + §12 (Writing agent task queue). Category E docs-only extension; no thesis chapter prose modified."
3. Reset `[Unreleased]` with empty `Added` / `Changed` / `Fixed` / `Removed` headers.
4. Edit `pyproject.toml` `version = "3.52.1"` → `version = "3.52.2"`.
5. Parent session dispatches `@reviewer-deep` with diff base ref `e45ca996` and plan path `planning/current_plan.md`. Reviewer verifies: (a) only the 3 files in §File Manifest below have been touched in this PR amendment commit (`thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md`, `CHANGELOG.md`, `pyproject.toml`); (b) the audit document carries §10 + §11 + §12 with the required structure; (c) `git diff master..HEAD --name-only | grep -E "^thesis/chapters/"` returns empty; (d) no methodology spec under `reports/specs/`, no status YAML, no ROADMAP, no research log, no notebook, no generated dataset artifact has been modified across the entire PR; (e) the version bump + CHANGELOG entry match the branch name.

**Verification:**
- `head -50 CHANGELOG.md` shows the new `[3.52.2] — 2026-05-17` block with the bullet, `[Unreleased]` reset, and `[3.52.1] — 2026-05-17` block preserved beneath.
- `grep "^version" pyproject.toml` shows `version = "3.52.2"`.
- Reviewer-deep returns `PASS` or `PASS-WITH-NOTES` with zero `BLOCKER`s.
- `git diff master..HEAD --name-only | grep -E "^thesis/chapters/"` returns empty (no chapter prose modified across the entire PR).

**File scope (writes):**
- `CHANGELOG.md` (update for amendment block)
- `pyproject.toml` (version bump 3.52.1 → 3.52.2)

**Read scope:**
- `planning/current_plan.md`
- All files listed in §File Manifest below
- `git diff e45ca996..HEAD`

**Model routing:** Sonnet sufficient for the CHANGELOG/version mechanical edits. Reviewer-deep is the gate (per Category E review-routing convention).

**Stop condition:** Halt before merge if reviewer-deep returns any `BLOCKER`.

---

## Hard constraints for execution

- The audit is NOT itself thesis prose. It lives under `thesis/pass2_evidence/` and is consumed by future writing PRs.
- The audit MUST NOT modify any thesis chapter file under `thesis/chapters/`. The conformance audit is a read-only comparison.
- The thesis-writing agent (or any prose-drafting agent) will be used ONLY AFTER this amended audit is reviewed and merged. The first writing PR that consumes this audit MUST cite the relevant rows from §11 (Draft correction backlog) and §12 (Writing agent task queue) verbatim in its plan's `source_artifacts`.
- Any future writing prompt MUST include the relevant rows from §11 and §12; the writing agent must be configured with the explicit `forbidden_claims` list from its assigned §12 row.
- If existing draft files cannot be found at the expected paths during T05, the executor MUST halt and report exact `find` / `ls` / `grep` commands used (e.g., `ls -la thesis/chapters/`, `find . -name "01_introduction.md"`).
- This PR's amendment commit MUST NOT touch any file outside the §File Manifest below. In particular: no chapter file, no spec file, no ROADMAP, no STATUS YAML, no research log, no notebook, no generated dataset artifact.
- ISO `YYYY-MM-DD` dates everywhere. Repo-relative paths everywhere. No emoji.

---

## Halt conditions specific to this amendment

The executor MUST halt and report (not silently proceed) if any of the following obtains during T05, T06, or T07:

1. A draft chapter file cited in the conformance audit cannot be found on disk (e.g., `thesis/chapters/04_data_and_methodology.md` returns "No such file or directory"). Report the exact `find` / `ls` commands used.
2. An evidence artifact cited as the corrected source cannot be found on disk (e.g., a deferred-dimension reference to `reports/specs/02_03_temporal_feature_audit_protocol.md` fails). Report the exact `ls` / `grep` used.
3. A recommended-replacement claim in §10.6 / §11 cannot be supported by a specific evidence-artifact path (e.g., the claim "Step 02_01_01 closure deferred" must cite the ROADMAP `continue_predicate` clause text, not paraphrase it).
4. The conformance audit would silently introduce thesis prose into the audit document beyond the agreed-on six categories + two tables (e.g., a §10 paragraph that reads as draftable chapter content rather than as a per-row classification). The audit document is Pass-2 evidence, not chapter prose.
5. Any task in T05 / T06 / T07 would touch a thesis chapter file (`thesis/chapters/*.md`). The amendment is read-only against chapter prose.
6. Any task would attempt to modify a methodology spec (`reports/specs/*`), status YAML (`*STATUS.yaml`), ROADMAP, research log, sandbox notebook, or generated dataset artifact under `reports/<dataset>/artifacts/`.
7. T05 surfaces a category-C3 (overclaim) finding that requires methodology-level resolution before drafting the audit append (e.g., an existing chapter paragraph silently asserts Phase 02 closure). Halt and escalate; do not auto-correct in §10.6 without parent-session confirmation.

---

## File Manifest

| File | Action |
|------|--------|
| `planning/current_plan.md` | Update (this amendment) |
| `planning/current_plan.critique.md` | Create or Update only if material risk remains after this amendment (see Section 4 of the planner output for whether the critique block is required) |
| `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` | Update (append §10 conformance audit + §11 backlog table + §12 queue table; existing §1–§9 frozen) |
| `CHANGELOG.md` | Update (new `[3.52.2]` block; `[3.52.1]` block preserved beneath) |
| `pyproject.toml` | Update (version 3.52.1 → 3.52.2) |

## Gate Condition

- `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` carries §1–§12 (existing §1–§9 unchanged plus new §10 conformance audit + §11 Draft correction backlog table + §12 Writing agent task queue table) and cites only artifacts that exist on disk.
- `**End of audit document.**` appears exactly once and at the file end.
- `CHANGELOG.md` carries the new `[3.52.2]` block with the amendment bullet; `[3.52.1] — 2026-05-17` block preserved beneath; `[Unreleased]` is reset.
- `pyproject.toml` `version = "3.52.2"`.
- No file outside the manifest is touched (`git diff e45ca996..HEAD --name-only | wc -l` ≤ 5 across the entire PR: `phase01_phase02_writing_readiness_audit.md`, `CHANGELOG.md`, `pyproject.toml` plus `planning/current_plan.md` and optionally `planning/current_plan.critique.md`).
- No thesis chapter prose under `thesis/chapters/` is modified across the entire PR (verifiable via `git diff master..HEAD --name-only | grep -E "^thesis/chapters/"` returns empty).
- No methodology spec under `reports/specs/` is modified.
- No status YAML (`*STATUS.yaml`), ROADMAP, or research log is modified.
- No notebook under `sandbox/` is modified or executed.
- No generated dataset artifact under `src/rts_predict/games/<game>/datasets/<dataset>/reports/artifacts/` is modified.
- §11 Draft correction backlog has at least one row per chapter found to have an overclaim, stale claim, or missing-caveat issue surfaced in §10.
- §12 Writing agent task queue is non-empty; every row routes to a named agent (e.g., `writer-thesis`) with explicit `forbidden_claims` (at minimum one F-number from §8 of the existing audit).
- `@reviewer-deep` returns `PASS` or `PASS-WITH-NOTES` with zero `BLOCKER`s.

## Out of scope

- Editing thesis chapter prose. The conformance audit is a read-only comparison; chapter rewrites belong to future Category F PRs ranked by §11 + §12 of the audit.
- Drafting any new thesis prose. The audit's §10/§11/§12 content is evidence-track classification, NOT thesis drafting.
- Drafting §4.5 (Phase 02 registry methodology subsection). This is a downstream Category F PR per §9.1 of the existing audit; this Category E amendment only catalogues the missing-claim row for it.
- Updating `thesis/WRITING_STATUS.md`. The audit does not flip any section's drafting state.
- Updating `thesis/chapters/REVIEW_QUEUE.md`. Pass-2 entries belong to drafted chapter sections; the audit (including the amendment) is itself a pass-2 evidence document.
- Touching `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` for any dataset. No phase or step state changes.
- Adding new spec versions or amending CROSS-02-00 / CROSS-02-01 / CROSS-02-02 / CROSS-02-03.
- Generating any new dataset artifact or modifying `notebook_regeneration_manifest.md` status rows.
- Re-running reviewer-deep against the T01–T04 deliverables (already verdicted PASS-WITH-NOTES at commit `faa6077d`). Reviewer-deep for T08 audits the amendment delta only.
- Adversarial critique. Category E plans do not require `@reviewer-adversarial` (see `docs/templates/planner_output_contract.md` §"Conditional requirements by category"). The amendment's conformance audit is read-only against thesis chapters; it does not introduce or modify methodology claims.

## Open questions

The amendment introduces only one genuine planning-time methodology call that may benefit from user confirmation before T06 executes; the others are operational and resolved by the §10.6 routing decisions themselves.

- **Q1 [RESOLVED 2026-05-17 by user].** Placeholder-only chapters `thesis/chapters/05_experiments_and_results.md`, `thesis/chapters/06_discussion.md`, and `thesis/chapters/07_conclusions.md` are NOT overclaim blockers. Include them in §11 (Draft correction backlog) as `issue_type = missing-claim` rows with `severity = LOW` and `agent_to_use = defer`. Future writing PRs may activate them only after Phase 03 evidence exists. T07 implementation must honor this resolution verbatim.
