---
title: "SC2 tracker eligibility framing for Chapter 4 (TQ-02 + TQ-01)"
category: F
branch: thesis/sc2-tracker-eligibility-section-4-3
date: 2026-05-17
planner_model: claude-opus-4-7
branch_prefix: thesis/
branch_name: thesis/sc2-tracker-eligibility-section-4-3
pr_title: "docs(thesis): add SC2 tracker eligibility framing for Chapter 4"
pr_number: 218
base_ref: "master @ 0a933be6"
base_commit: 0a933be6
created_date: 2026-05-17
dataset: sc2egset
phase: "02 — tracker eligibility scope only; NO Phase 02 closure"
pipeline_section: "n/a (Category F thesis prose; consumes prior Phase 01 §01_03 + Phase 02 §02_01 evidence)"
step: "n/a (Category F prose update; no Step closure claimed)"
target_version: "3.53.0"
version_current: "3.52.2"
version_bump_type: "minor (Category F docs prose addition per .claude/rules/git-workflow.md §Version)"
critique_required: true
invariants_touched:
  - I3   # No feature for game T may use information from game T or later — tracker features are in-game-snapshot only (Amendment 2 of PR #208); the plan enforces but does not modify this invariant.
  - I6   # All analytical results must be reported alongside derivation — every numerical claim in the future prose must trace to artifact:line. The plan enforces but does not modify this invariant.
  - I7   # No magic numbers — counts (5, 7, 3, 12, 15) must trace to artifact rows. The plan enforces but does not modify this invariant.
research_log_ref: null  # Category F prose; no per-dataset research_log entry created by this plan. WRITING_STATUS.md Chapter 4 row update is the equivalent for thesis work.
prior_executed_tasks:
  - id: T00
    commit: df7b2613
    description: "Bootstrap draft PR + planning stub. No thesis prose touched. No dataset artifacts touched."
source_artifacts:
  # Required-claim evidence anchors (12, in order)
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/01_03_05_tracker_events_semantic_validation.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/01_03_05_tracker_events_semantic_validation.json
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md
  - .claude/scientific-invariants.md
  - reports/specs/02_01_leakage_audit_protocol.md
  - thesis/pass2_evidence/phase02_readiness_hardening.md
  - thesis/pass2_evidence/methodology_risk_register.md
  - thesis/pass2_evidence/phase01_closeout_summary.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md
  - thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md
  # Plan-context artifacts
  - thesis/chapters/04_data_and_methodology.md
  - thesis/chapters/REVIEW_QUEUE.md
  - thesis/WRITING_STATUS.md
  - thesis/THESIS_STRUCTURE.md
  - thesis/references.bib
  - thesis/plans/writing_protocol.md
  - .claude/rules/thesis-writing.md
  - .claude/rules/data-analysis-lineage.md
  - .claude/author-style-brief-pl.md
  - docs/PHASES.md
  - docs/TAXONOMY.md
  - docs/templates/plan_template.md
  - docs/templates/planner_output_contract.md
  - reports/specs/02_00_feature_input_contract.md
  - reports/specs/02_02_feature_engineering_plan.md
  - reports/specs/02_03_temporal_feature_audit_protocol.md
---

# Plan: SC2 tracker eligibility framing for Chapter 4 (TQ-02 + TQ-01)

## Scope

This is a **Category F (thesis writing) plan**. Single deliverable file: `thesis/chapters/04_data_and_methodology.md`. Two coupled prose edits in §4.3, both routed verbatim from `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` §11 (Draft correction backlog) + §12 (Writing agent task queue, TQ-01 + TQ-02):

- **TQ-02 (NEW subsection).** Insert a new SC2-tracker-eligibility subsection after the existing §4.3.2 prose. Recommended slot: `### 4.3.3 Walidacja semantyczna strumienia tracker_events_raw (Step 01_03_05; GATE-14A6 — narrowed)`, with the current §4.3.3 (`AoE2-specific features`) renumbered to §4.3.4. Final numbering is an Open Question for the user (§ Open Questions below).
- **TQ-01 (PARAGRAPH REPAIR).** Rewrite the single existing paragraph at line 331 of §4.3.2 that asserts Step 01_03_05 *"nie została zrealizowana w obecnej iteracji"*. The repaired paragraph must state Step 01_03_05 IS complete (`completed_at: 2026-05-05`) and forward-refer to the new §4.3.3 for the eligibility scope.

Both edits share the same evidence base and resolve together (audit §10.2 row 1, §10.5 row 2, §10.6 row 1+4, §11 row 1+4, §12 TQ-01+TQ-02). Coupling them in one PR avoids leaving §4.3.2 stale during a multi-PR sequence.

No other Chapter 4 section is touched. No other thesis chapter is touched. No dataset artifact, spec, status YAML, ROADMAP, notebook, code file, or research log is touched.

## Problem Statement

Two interlocking gaps in `thesis/chapters/04_data_and_methodology.md` §4.3 cause an examiner-visible defect:

1. **§4.3.2 is empirically false.** The chapter's only prose paragraph for the SC2 tracker stream (line 331) asserts Step 01_03_05 *"nie została zrealizowana w obecnej iteracji"*. This was true when drafted, but the step landed on 2026-05-05 (PR #208) with `STEP_STATUS.yaml` recording `status: complete`, `completed_at: "2026-05-05"`. The paragraph is now stale-by-date and contradicts a merged Phase 01 artifact. Audit §10.2 row 1 (severity: HIGH), §11 row 1 (severity: HIGH), §12 TQ-01.

2. **§4.3 lacks a tracker eligibility subsection.** Step 01_03_05 produced `tracker_events_feature_eligibility.csv` (15 feature families, with explicit `status_pre_game`, `status_in_game_snapshot`, `eligibility_scope`, `caveat`, and `blocking_reason_if_blocked` columns) and the markdown report `01_03_05_tracker_events_semantic_validation.md` declaring `gate_14a6_decision = narrowed` (NOT `closed`). The methodology chapter must give this artifact a defensible textual home so future §4.4 in-game feature work can cite it. Audit §10.5 row 2 (severity: HIGH), §11 row 4 (severity: HIGH for the per-row scope sub-claim), §12 TQ-02.

The risk profile is examiner-facing: an examiner reading §4.3.2 today will see a methodology chapter that claims an absent validation step, then look at the repository and find that step demonstrably executed. This invites a credibility cascade across the methodology chapter. The risk is mitigated, not eliminated, by the audit's pre-Pass-2 capture in §10.2 — but until the prose itself is repaired, the chapter is failing its own evidence base.

The two edits are coupled because §4.3.2 contains a forward-reference to "przyszłego zamknięcia walidacji semantycznej" — the repair text MUST point readers to the new §4.3.3 for the eligibility scope, not just delete the obsolete sentence. Splitting TQ-01 and TQ-02 into separate PRs would leave §4.3.2 with a dangling forward-reference and trigger a second writer-thesis dispatch for trivial textual reconciliation.

## Literature Context

This is a data-fed methodology section grounded in repository evidence; the literature surface is narrow but non-trivial. The plan's literature context lists three categories.

### Primary external citations (already in `thesis/references.bib`)

- `[Bialecki2023]` — *"SC2EGSet: StarCraft II Esport Replay and Game-state Dataset"* (`references.bib:5`). The corpus paper for the dataset whose tracker stream is the subject of this subsection. MUST be cited in the new §4.3.3 opening sentence.
- `[BlizzardS2Protocol]` — *"s2protocol: Python library to decode StarCraft II replay protocols"* (`references.bib:780-783`); note field records *"tracker events introduced in protocol version 2.0.8"*. MUST be cited at the first mention of `tracker_events_raw` provenance and at the V3 fixed-point caveat (the s2protocol README is the source of the `scoreValueFoodUsed` divide-by-4096 convention).

No new external citations are anticipated. The writer-thesis dispatch (T02) is forbidden from inventing external citations without WebSearch verification per `.claude/rules/thesis-writing.md` Literature Search Protocol; if a Pass-2 reviewer flags a missing reference, it is added in a follow-up sweep, not in this PR.

### Repository-internal anchors (NOT external citations — referenced as artifact paths or invariant IDs)

- **Invariant I3** (`.claude/scientific-invariants.md` §Temporal discipline): *"No feature for game T may use information from game T or later"*. The plan enforces I3 in the future prose: tracker-derived features are NEVER pre-game.
- **Amendment 2 of PR #208** (verbatim wording at `thesis/pass2_evidence/phase02_readiness_hardening.md:294`; corroborating at `thesis/pass2_evidence/methodology_risk_register.md:399` and `:404`; I3 source at `.claude/scientific-invariants.md:131`): *"Tracker-derived feature families remain NEVER pre-game (Amendment 2 / Invariant I3): every row in the eligibility CSV carries `status_pre_game = not_applicable_to_pre_game`. Programmatic assertions in V7 and V8 enforce this."*. The new §4.3.3 MUST state this verbatim or near-verbatim in Polish. (Reviewer-deep fix: original draft cited `sc2egset/reports/INVARIANTS.md:97` which does not contain Amendment-2 wording.)
- **CROSS-02-01-v1.0.1** (`reports/specs/02_01_leakage_audit_protocol.md`, LOCKED 2026-04-26): the mandatory post-materialization leakage audit. The new §4.3.3 MUST contain a non-supersession statement explicitly noting that GATE-14A6 narrowing does NOT excuse any materialized tracker feature from CROSS-02-01-v1.0.1.
- **GATE-14A6** (`thesis/pass2_evidence/phase02_readiness_hardening.md` §14A.6 POST-VALIDATION UPDATE). Outcome: `narrowed`. The new §4.3.3 cites this gate by name.
- **RISK-21** (`thesis/pass2_evidence/methodology_risk_register.md:392-405`). Post-PR-#208 status: `MITIGATED-NARROWED`. Wording recommendation in line 404 of the risk register provides a defensible English template that the writer-thesis Polish prose may adapt.

### Pass-2 verification flag

Any external citation the writer-thesis chooses to add beyond `[Bialecki2023]` and `[BlizzardS2Protocol]` MUST carry an inline `[REVIEW: Pass-2 — <reason>]` flag and be enumerated in the Chat Handoff Summary, per `.claude/rules/thesis-writing.md` Literature Search Protocol §4–§6. The plan does NOT pre-authorize any specific external citation beyond the two listed above.

## Assumptions & Unknowns

- **Assumption A1.** Step 01_03_05 evidence artifacts (`01_03_05_tracker_events_semantic_validation.md`, `.json`, `tracker_events_feature_eligibility.csv`) remain on disk at the cited paths after PR #216 / PR #217 merge to master @ `0a933be6`. **Verified 2026-05-17** by direct file read.
- **Assumption A2.** The 5 + 7 + 3 partition of `status_in_game_snapshot` matches the contract `gate_14a6_decision = narrowed` AND `initial_phase02_subset_ready = True`. **Verified 2026-05-17** by `awk` tabulation of the CSV — 5 eligible_for_phase02_now (rows 5,7,9,13,14) + 7 eligible_with_caveat (rows 1,2,3,4,6,8,10) + 3 blocked_until_additional_validation (rows 11,12,15) = 15 = total data rows.
- **Assumption A3.** `slot_identity_consistency` is classified as a sanity gate (NOT a model input) per the `notes_for_phase02` column. **Verified 2026-05-17** — CSV row 14 `notes_for_phase02 = "feature-engineering sanity gate; not a model input"` AND PR #208 body verbatim repeats this.
- **Assumption A4.** The 3 blocked families are named `mind_control_event_count`, `army_centroid_at_cutoff_snapshot`, `playerstats_cumulative_economy_fields`. **Verified 2026-05-17** — CSV rows 11, 12, 15 AND `01_03_05_tracker_events_semantic_validation.md:16` lists them verbatim.
- **Assumption A5.** The PR will NOT add any new bibkey to `thesis/references.bib`. `[Bialecki2023]` and `[BlizzardS2Protocol]` already exist; no novel external reference is required. If writer-thesis discovers a needed reference during drafting, the dispatch instructions require it to plant a `[NEEDS CITATION]` flag and defer the bib-entry add to Pass-2 (per `.claude/rules/thesis-writing.md` Literature Search Protocol §6).
- **Unknown U1.** Final subsection numbering. The dispatch and the audit both name the slot "§4.3.x" without committing. Recommended default: `### 4.3.3` (the new subsection) with `### 4.3.3 AoE2-specific features` → `### 4.3.4`. Alternative: insert as labelled prose block inside §4.3.2 with no number bump. Resolution: USER DECISION (Open Question Q-A below) before T01 dispatch finalizes.
- **Unknown U2.** Whether to issue a one-line repair to `thesis/WRITING_STATUS.md` line 75 (currently asserts "Step 01_03_05 not yet scheduled"). The line is stale; updating it is in writer-thesis's allowed Write scope per the writing-protocol §1. Recommended default: include the one-line WRITING_STATUS update in T02 scope and the file in the manifest (it is the canonical place to record the status delta and is co-located with the prose change). Resolution: USER DECISION (Open Question Q-B below).
- **Unknown U3.** Whether to update `thesis/chapters/REVIEW_QUEUE.md` with a Pending row for the new §4.3.3. This is REQUIRED by `.claude/rules/thesis-writing.md` Pass-1 step 8. Resolved: YES — REVIEW_QUEUE.md update is in T02 scope and the file is in the manifest.
- **Unknown U4.** Whether to consider extracting the V3 fixed-point divide-by-4096 caveat (PlayerStats `scoreValueFoodUsed`) into the new subsection. The CSV `caveat` column records it on rows 3 (`supply_used_at_cutoff_snapshot`) and 4 (`food_used_max_history`). Recommended default: include the caveat as one half-sentence inside the per-row scope summary, NOT as a standalone paragraph. The audit's TQ-02 routing supports this depth. Resolution: writer-thesis discretion within the dispatch's "must justify" list (T02 dispatch specifies "per-row scope and caveat must be acknowledged, but exhaustive per-field enumeration is not required").

## Execution Steps

Six tasks (T01–T06). T00 (bootstrap draft PR + stub commit) is already complete at commit `df7b2613` — recorded in `prior_executed_tasks` frontmatter. Tasks are NOT parallel-safe: T02 depends on T01 verdicts; T03 + T04 depend on T02; T05 + T06 depend on T03 + T04.

---

### T01 — Reviewer-deep + reviewer-adversarial concurrent review of THIS plan

**Objective:** Subject this plan to combined adversarial + structural review before any writer-thesis dispatch. Category F + thesis-claim-load-bearing prose REQUIRES `reviewer-adversarial` per `docs/templates/planner_output_contract.md` line 33 and `.claude/rules/data-analysis-lineage.md` §Agent and model routing discipline.

**Instructions:**
1. Parent session writes this plan's content to `planning/current_plan.md` verbatim (overwriting the bootstrap stub at `df7b2613`); commits with message `docs(planning): replace SC2 tracker eligibility section 4.3 bootstrap stub with full plan`; pushes.
2. Parent session dispatches `@reviewer-deep` to audit this plan for structural correctness, spec compliance, invariant tracing, completeness of the file manifest, completeness of the required-claim surface, completeness of the forbidden-claim surface, and conformance to `docs/templates/planner_output_contract.md`. Reviewer-deep output goes to chat.
3. In parallel, parent session dispatches `@reviewer-adversarial` (Mode A — plan review) to stress-test the plan's methodology defensibility: GATE-14A6 `narrowed` framing, non-supersession of CROSS-02-01-v1.0.1, the 5+7+3+1 framing's faithfulness to the artifact, the absence of any pre-game tracker promotion, and the absence of any Phase 02 / Step 02_01_01 closure overclaim. Reviewer-adversarial output goes to chat; parent session persists to `planning/current_plan.critique.md` via the Write tool.
4. Parent session reads both critiques. If either reviewer raises a BLOCKER, the plan is revised (back to planner-science in a fresh session) and T01 is re-run. If both verdicts are PROCEED or REVISE-MINOR (and revisions can be applied in-place without methodological redesign), proceed to user-approval gate.
5. **User-approval gate** (no dispatch — human decision). User reads both critiques + the plan; either approves T02 dispatch or requests plan revision.

**Verification:**
- `git log --oneline -1` after step 1 shows the planning commit; `git diff master..HEAD --name-only` lists only `planning/current_plan.md` (and, after step 3, `planning/current_plan.critique.md`).
- Reviewer-deep verdict file or chat output exists, with explicit PROCEED / REVISE / REJECT decision.
- Reviewer-adversarial verdict persisted at `planning/current_plan.critique.md`, with explicit Mode A verdict per `docs/templates/plan_critique_template.md`.
- User has explicitly approved T02 dispatch.

**File scope (writes):**
- `planning/current_plan.md` (full overwrite of bootstrap stub)
- `planning/current_plan.critique.md` (parent-persisted from reviewer-adversarial chat output)

**Read scope:**
- All `source_artifacts` listed in frontmatter
- `docs/templates/plan_critique_template.md`

**Model routing:**
- Planner-science: Opus (this plan).
- Reviewer-deep: per `.claude/agents/reviewer-deep.md` defaults (Opus, max effort).
- Reviewer-adversarial: per `.claude/agents/reviewer-adversarial.md` defaults (Opus, max effort).

**Stop condition:**
- Halt if reviewer-deep raises a STRUCTURAL BLOCKER (e.g., evidence-anchor mismatch, missing required section, frontmatter schema violation).
- Halt if reviewer-adversarial raises a METHODOLOGY BLOCKER (e.g., the 5+7+3 framing is incorrect, the non-supersession statement is missing or wrong, a forbidden-claim line is wrong).
- Halt if both reviewers PROCEED but the user does not approve T02 dispatch.

---

### T02 — Writer-thesis drafts §4.3.x + repairs §4.3.2 (post user-approval)

**Objective:** Execute the audit's TQ-02 + TQ-01 against `thesis/chapters/04_data_and_methodology.md`. New subsection drafted; stale paragraph repaired; WRITING_STATUS + REVIEW_QUEUE updated. No file outside the allowed manifest is touched.

**Instructions:**
1. Fresh session (per writer-thesis dispatch protocol; never reuse the planner-science session).
2. Parent session dispatches `@writer-thesis` with the dispatch prompt assembled per `## Hard constraints for writer-thesis dispatch` below. The dispatch prompt MUST include verbatim:
   - The 12 required-claim anchors (from `## Required claim surface` below).
   - The forbidden-claim list (from `## Forbidden claims for writer-thesis` below).
   - The exact allowed-files manifest (from `## File Manifest` below).
   - The exact insertion point (between line 331 and line 333 of the chapter file) and the exact paragraph to repair (line 331, the single Polish paragraph starting `**Status walidacji semantycznej strumienia ...**`).
   - The §4.3.x heading numbering decision (recommended: `### 4.3.3`, renumber existing `### 4.3.3 AoE2-specific features` to `### 4.3.4`; pending Open Question Q-A resolution).
   - The "must justify / must contrast / must cite" lists below.
   - The voice note: "argumentative, not descriptive."
   - The Pass-1 step sequence per `.claude/rules/thesis-writing.md` (Data variant — sections fed by Phase artifacts; the new §4.3.3 is data-fed via Phase 01 Step 01_03_05; the §4.3.2 repair is data-fed via the same evidence).
3. Writer-thesis drafts the new §4.3.3 subsection (Polish, academic register per `.claude/author-style-brief-pl.md`) and rewrites the §4.3.2 stale paragraph. Both edits occur in the same writer-thesis session; the chapter file is the single touchpoint for prose.
4. Writer-thesis runs the Critical Review Checklist — Data variant (per `.claude/rules/thesis-writing.md` §"Critical Review Checklist"): numerical consistency (every count traces to artifact), claim-evidence alignment, derivation traceability (every threshold has empirical or cited justification), scope honesty (no generalization beyond the dataset), and missing-context flag planting.
5. Writer-thesis plants inline `[REVIEW:]` / `[NEEDS CITATION]` flags wherever Pass-2 verification is needed (e.g., V3 fixed-point divide-by-4096 SC2EGSet decoder convention if the writer chooses to mention it; per-family caveat depth choices the writer makes that exceed plan guidance).
6. Writer-thesis updates `thesis/WRITING_STATUS.md` Chapter 4 row: status note appended documenting that §4.3.2 has been repaired and §4.3.3 has been added; line 75 ("§4.4 in-game feature subsection CANNOT reach FINAL status until SC2 tracker_events semantic validation executes (Step 01_03_05, not yet scheduled)") rewritten to reflect that Step 01_03_05 IS complete and GATE-14A6 outcome is `narrowed` (line 75 update is conditional on Open Question Q-B resolution; if Q-B = NO, skip this clause).
7. Writer-thesis adds a Pending row to `thesis/chapters/REVIEW_QUEUE.md` for §4.3.3 (and a separate Pending row or amendment for the §4.3.2 repair, depending on REVIEW_QUEUE convention).
8. Writer-thesis produces the Chat Handoff Summary per `.claude/rules/thesis-writing.md` §"Chat Handoff Summary Format" (Data variant): list of inline flags, list of artifact-traced numbers, list of self-discovered references (if any beyond `[Bialecki2023]` + `[BlizzardS2Protocol]`), questions for Pass-2.
9. Parent session reviews the diff; if it touches any file outside the manifest, HALT and dispatch a follow-up writer-thesis correction.
10. Parent commits with `git commit -F .github/tmp/commit.txt` per memory; suggested message: `docs(thesis): add §4.3.3 SC2 tracker eligibility (Step 01_03_05 narrowed); repair §4.3.2 paragraph (TQ-01 + TQ-02)`. Push.

**"Must justify" list (writer-thesis MUST include alternatives-considered paragraphs for):**
- Why the new subsection numbering is §4.3.3 (vs. an in-§4.3.2 labelled block with no number). The writer's chosen rationale traces back to Open Question Q-A's resolution.
- Why the new subsection cites the 5+7+3 partition without enumerating all 15 rows table-style. (Alternative: a Table-4.X row enumeration. The plan's recommended default is prose-with-counts, deferring a per-row table to a future PR if any §4.4 in-game subsection materializes; reduces table count and stays close to the audit's TQ-02 wording.)
- Why the new subsection does NOT include a "preview" of which of the 12 planned-yes families will be materialized in Phase 02. (Alternative: list expected materialization scope. The plan's rationale: F3 forbidden-claim — final feature catalog — is unrecoverable until Step 02_01_02 materializes the columns and CROSS-02-01-v1.0.1 audits them.)
- Why the V3 fixed-point divide-by-4096 SC2EGSet decoder convention is mentioned (if mentioned). (Alternative: omit and defer to Step 02_01_02 prose. The plan's rationale: a half-sentence acknowledgement preserves the audit's per-row scope/caveat surface without escalating to a separate paragraph; the writer's decision is bounded by Unknown U4.)

**"Must contrast" list (writer-thesis MUST contrast the chosen framing against at least one explicit alternative):**
- GATE-14A6 `narrowed` vs. `closed`. The new subsection must explicitly contrast these two outcomes and justify why `narrowed` is the correct framing (3 of 15 candidate tracker families remain `blocked_until_additional_validation`).
- "Tracker features as in-game-snapshot only" vs. "tracker features as pre-game candidates". The new subsection must explicitly state that the latter framing is permanently forbidden under Invariant I3 / Amendment 2.
- Step 01_03_05 completion vs. Step 02_01_01 closure. The new subsection (and the repaired §4.3.2) must explicitly distinguish these — Step 01_03_05 completing does NOT close Step 02_01_01 (which is still gated by CROSS-02-01-v1.0.1 post-materialization audit per F4 + F7).

**"Must cite" list (writer-thesis MUST cite the following sources at the specified loci):**
- `[Bialecki2023]` — at the opening sentence of §4.3.3 (provenance of the SC2EGSet tracker stream).
- `[BlizzardS2Protocol]` — at the first technical reference to tracker_events_raw (provenance of the protocol-2.0.8 introduction; also at any V3 fixed-point caveat if writer chooses to surface it).
- `tracker_events_feature_eligibility.csv` — at the 15-row count and the 5+7+3 breakdown (artifact path per the chapter's existing convention).
- `01_03_05_tracker_events_semantic_validation.md` — at the GATE-14A6 `narrowed` claim (artifact path per the chapter's existing convention).
- `thesis/pass2_evidence/phase02_readiness_hardening.md` §14A.6 — at the gate-name first occurrence.
- `.claude/scientific-invariants.md` I3 + the dataset's `INVARIANTS.md` (Amendment 2) — at the "tracker features never pre-game" claim.
- `reports/specs/02_01_leakage_audit_protocol.md` (CROSS-02-01-v1.0.1) — at the non-supersession statement.

**Expected length:** Per THESIS_STRUCTURE.md §4.3.2 bullet expectations and the audit's TQ-02 routing depth, the new §4.3.3 should be **~3–6k characters of Polish prose** (one to two paragraphs of framing + one paragraph enumerating the 5+7+3 partition with per-row scope/caveat acknowledgement + one paragraph carrying the non-supersession statement + the Invariant-I3/Amendment-2 statement). The §4.3.2 repair is a **paragraph-scale rewrite** (~600–1000 characters of Polish prose) replacing the existing line 331 paragraph with one that acknowledges Step 01_03_05 completion and forward-refers to §4.3.3.

**Voice note:** Argumentative, not descriptive. Per `.claude/author-style-brief-pl.md`, the new prose must operate at the chapter's existing register (academic Polish, hedged, peer-citable). It must NOT simply transcribe the audit's correction backlog — it must integrate the eligibility framing into the chapter's existing methodology argument.

**Verification:**
- `git diff master..HEAD --name-only` after T02 commit lists ONLY: `planning/current_plan.md`, `planning/current_plan.critique.md`, `thesis/chapters/04_data_and_methodology.md`, `thesis/chapters/REVIEW_QUEUE.md`, and (conditional on Q-B) `thesis/WRITING_STATUS.md`. Any file outside this list triggers HALT.
- `grep -nE "^### 4\\.3" thesis/chapters/04_data_and_methodology.md` after T02 shows 4 subsections (§4.3.1, §4.3.2, §4.3.3 [new], §4.3.4 [renumbered AoE2]) per recommended default.
- `grep -nE "nie została zrealizowana" thesis/chapters/04_data_and_methodology.md` returns 0 matches after T02.
- `grep -nE "GATE-14A6|narrowed|tracker_events_feature_eligibility" thesis/chapters/04_data_and_methodology.md` returns at least one match per token.
- Chat Handoff Summary present in chat output.

**File scope (writes):**
- `thesis/chapters/04_data_and_methodology.md` (in-place edit: §4.3.2 paragraph rewrite + new §4.3.3 insert + §4.3.3 → §4.3.4 renumber)
- `thesis/chapters/REVIEW_QUEUE.md` (append Pending row(s))
- `thesis/WRITING_STATUS.md` (conditional on Q-B; one-line Chapter 4 row update)

**Read scope:**
- All `source_artifacts` listed in frontmatter
- `planning/current_plan.md` (this file)
- `planning/current_plan.critique.md` (the T01 reviewer-adversarial verdict)

**Model routing:**
- Writer-thesis: Opus, max effort, default permission scope per `.claude/agents/writer-thesis.md`. Opus is REQUIRED — this prose is methodology-load-bearing.

**Stop condition:**
- Halt if writer-thesis attempts to write any file outside the allowed manifest (e.g., a `reports/**` artifact, a spec file, a status YAML, a ROADMAP, a research log, a notebook, or a code file).
- Halt if writer-thesis attempts to remove an existing `[REVIEW:]` flag from §4.3.1 or §4.3.3 (AoE2, post-renumber §4.3.4) — those flags are out of scope and removal would leak the plan's bounded edit.
- Halt if writer-thesis writes prose that violates any of the 12 forbidden claims below.
- Halt if writer-thesis adds a new external citation without WebSearch verification (per `.claude/rules/thesis-writing.md` Literature Search Protocol §1–§5).

---

### T03 — Reviewer-deep on the drafted prose

**Objective:** Verify the structural correctness of the writer-thesis draft. This is a Mode-B-style review focused on scope discipline, claim-evidence alignment, numerical consistency, and invariant tracing.

**Instructions:**
1. Parent session dispatches `@reviewer-deep` with explicit handoff: path to `planning/current_plan.md`, the `base_ref` (master @ `0a933be6`), and the diff scope.
2. Reviewer-deep verifies:
   - **Scope.** `git diff master..HEAD --name-only` lists ONLY the files in the allowed manifest.
   - **Claim-evidence alignment.** Every numerical claim (15, 12, 5, 7, 3, 1, dates) traces back to a specific artifact line.
   - **Required-claim surface.** All 12 required claims appear in the new §4.3.3 prose (or, where appropriate, in the repaired §4.3.2 paragraph).
   - **Forbidden-claim surface.** None of the 12 forbidden claims appear.
   - **Invariant tracing.** Invariant I3 + Amendment 2 are correctly cited; CROSS-02-01-v1.0.1 non-supersession is correctly framed.
   - **Bibkey integrity.** Every cited bibkey resolves in `thesis/references.bib`.
   - **Voice consistency.** Prose matches the surrounding §4.3 register; no anglicized phrasing.
3. Reviewer-deep emits chat output with PROCEED / REVISE / REJECT verdict.

**Verification:**
- Reviewer-deep verdict in chat with explicit decision.
- If REVISE, writer-thesis is re-dispatched (in the parent session) with the specific revision instructions; T03 re-runs.
- If REJECT, plan is revised back at the T01 level.

**File scope (writes):** None (reviewer-deep is read-only).

**Read scope:**
- `thesis/chapters/04_data_and_methodology.md` (post-T02 state)
- `thesis/chapters/REVIEW_QUEUE.md` (post-T02 state)
- `thesis/WRITING_STATUS.md` (post-T02 state if Q-B = YES)
- All `source_artifacts` from frontmatter
- `planning/current_plan.md`

**Model routing:**
- Reviewer-deep: per `.claude/agents/reviewer-deep.md` defaults (Opus, max effort).

**Stop condition:**
- Halt if reviewer-deep raises a STRUCTURAL BLOCKER. Resolve before T04 / T05.

---

### T04 — Reviewer-adversarial on the drafted prose

**Objective:** Stress-test the drafted prose for thesis-defensibility. Mode-C review per `.claude/agents/reviewer-adversarial.md`. This is the second adversarial pass (the first was T01 against the plan); the cap of 3 rounds applies per memory file `feedback_adversarial_cap_execution.md` (symmetric to plan-side cap).

**Instructions:**
1. Parent session dispatches `@reviewer-adversarial` (Mode C — draft review). Reviewer cannot Write/Edit per platform constraint; output goes to chat.
2. Reviewer-adversarial verifies:
   - **GATE-14A6 framing.** Is the `narrowed` wording faithful to the artifact? Does the prose accidentally suggest `closed`?
   - **Non-supersession of CROSS-02-01-v1.0.1.** Is the statement explicit? Does it survive an examiner's interpretation of "validated subset = leakage-free"?
   - **Tracker-pre-game prohibition.** Is Amendment 2 / Invariant I3 cited verbatim or in a defensibly-equivalent Polish formulation? Could an examiner read the prose as suggesting tracker features could ever be pre-game?
   - **No promotion of blocked rows.** Are the 3 blocked families enumerated without any suggestion they may be promoted in the future of this thesis?
   - **No Phase 02 / Step 02_01_01 closure overclaim.** Does the prose suggest, even by implication, that Phase 02 or Step 02_01_01 is closed?
   - **Sanity-gate framing.** Is `slot_identity_consistency` correctly described as a sanity gate (NOT a model input)? Is the distinction defensible?
   - **Per-row scope/caveat surface.** Does the prose acknowledge the `eligibility_scope` and `caveat` columns without enumerating all rows (which would be premature)?
   - **External citation defensibility.** Did writer-thesis add any citation that would not survive Pass-2 WebSearch verification?
3. Reviewer-adversarial emits chat output with Mode-C verdict per `docs/templates/plan_critique_template.md` (or its draft-review equivalent).

**Verification:**
- Reviewer-adversarial verdict in chat with explicit decision.
- If BLOCKER: writer-thesis is re-dispatched with the specific BLOCKER fixes; T03 + T04 re-run.
- 3-round adversarial cap: if a 3rd round still BLOCKERS, escalate to user for plan-level redesign.

**File scope (writes):** None (reviewer-adversarial is read-only).

**Read scope:**
- `thesis/chapters/04_data_and_methodology.md` (post-T02 state)
- All `source_artifacts` from frontmatter
- `planning/current_plan.md`
- `planning/current_plan.critique.md`

**Model routing:**
- Reviewer-adversarial: per `.claude/agents/reviewer-adversarial.md` defaults (Opus, max effort).

**Stop condition:**
- Halt if reviewer-adversarial raises a METHODOLOGY BLOCKER. Resolve before T05.
- Hard cap: 3 adversarial rounds. If unresolved after round 3, escalate to user.

---

### T05 — CHANGELOG `[3.53.0]` block + version bump `3.52.2 → 3.53.0`

**Objective:** Record the prose change in the project changelog and bump the version. Per `.claude/rules/git-workflow.md` §Version: minor bump for feat/refactor/docs (this is a docs PR).

**Instructions:**
1. Parent session dispatches `@executor` (Sonnet — mechanical task, plan resolves the scientific decisions).
2. Executor adds a new `## [3.53.0] — 2026-05-17` block at the top of `CHANGELOG.md` under `## [Unreleased]` (or in the canonical project location). Block summarizes: TQ-01 paragraph repair + TQ-02 new §4.3.3 subsection; references PR #218; cites the audit §11 row 1 + row 4 as the source backlog.
3. Executor bumps `pyproject.toml` `version = "3.52.2"` → `version = "3.53.0"`.
4. Executor commits with message `chore(release): bump to 3.53.0 (Cat-F prose: SC2 tracker eligibility §4.3.3 + §4.3.2 repair)`. Push.

**Verification:**
- `grep -nE "^## \\[3\\.53\\.0\\]" CHANGELOG.md` returns one match.
- `grep -nE "^version = " pyproject.toml` shows `3.53.0`.
- `git diff master..HEAD --name-only` lists only the manifest files PLUS `CHANGELOG.md` + `pyproject.toml`.

**File scope (writes):**
- `CHANGELOG.md`
- `pyproject.toml`

**Read scope:**
- `thesis/chapters/04_data_and_methodology.md`
- `.claude/rules/git-workflow.md`
- `pyproject.toml`
- `CHANGELOG.md`

**Model routing:**
- Executor: Sonnet (mechanical task; plan resolves all decisions).

**Stop condition:**
- Halt if `.claude/rules/git-workflow.md` does NOT support a minor bump for Category F (verify before executing — if rule is patch-only for docs, fall back to `3.52.3`).
- Halt if any file outside the manifest is touched.

---

### T06 — PR body refresh + `gh pr ready 218`

**Objective:** Update the PR #218 body to reflect the final scope (drop the "STUB" framing); transition draft → ready for review.

**Instructions:**
1. Parent session writes the PR body to `.github/tmp/pr.txt` per memory `feedback_pr_body_file.md`. Body summarizes: TQ-01 + TQ-02 deliverable; required-claim surface; forbidden-claim surface; CHANGELOG/version bump; reviewer routing.
2. Parent session runs `gh pr edit 218 --body-file .github/tmp/pr.txt`.
3. Parent session runs `gh pr ready 218`.
4. Parent session removes `.github/tmp/pr.txt` per memory `feedback_pr_body_cleanup.md`.
5. No commit (PR-body edit is a remote-side change).

**Verification:**
- `gh pr view 218 --json isDraft` returns `{"isDraft": false}`.
- `gh pr view 218 --json body` returns the new body (no "STUB" tokens).
- `.github/tmp/pr.txt` does NOT exist on disk.

**File scope (writes):**
- `.github/tmp/pr.txt` (created then removed in the same task)

**Read scope:**
- `thesis/chapters/04_data_and_methodology.md`
- `planning/current_plan.md`
- `planning/current_plan.critique.md`

**Model routing:**
- Executor: Sonnet (mechanical task).

**Stop condition:**
- Halt if `gh pr ready 218` fails (likely because of unresolved review comments — surface to user).

## Required claim surface

Every claim below MUST appear in the new §4.3.3 prose (or, where indicated by `[repair-§4.3.2]`, in the repaired §4.3.2 paragraph), traced verbatim to the cited evidence path. Writer-thesis dispatch prompt MUST include this section verbatim.

| # | Claim | Evidence path | Notes |
|---|---|---|---|
| 1 | Step 01_03_05 IS complete (`completed_at: 2026-05-05`) | `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml:82-86` | `[repair-§4.3.2]` AND new §4.3.3 opening sentence. |
| 2 | GATE-14A6 outcome is `narrowed`, NOT `closed` | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/01_03_05_tracker_events_semantic_validation.md:11`; `.json` field `gate_14a6_decision = "narrowed"` | new §4.3.3 must state both the affirmative `narrowed` AND the negative `NOT closed`. |
| 3 | Initial Phase 02 SC2 tracker planned subset is ready under recorded `eligibility_scope` / `caveat` constraints | `01_03_05_tracker_events_semantic_validation.md:12` (`initial_phase02_subset_ready: True`); `tracker_events_feature_eligibility.csv` columns `eligibility_scope` and `caveat` | new §4.3.3 — must acknowledge per-row scope/caveat surface without exhaustive enumeration. |
| 4 | Tracker-derived SC2 features are NEVER pre-game (Invariant I3 + Amendment 2 per PR #208) | `.claude/scientific-invariants.md:131` (I3); `thesis/pass2_evidence/phase02_readiness_hardening.md:294` (Amendment 2 verbatim); `thesis/pass2_evidence/methodology_risk_register.md:399,404` (corroborating); `tracker_events_feature_eligibility.csv` 15/15 rows with `status_pre_game = not_applicable_to_pre_game` | new §4.3.3 — must be stated verbatim or near-verbatim, and explicitly cited to Invariant I3 + Amendment 2. |
| 5 | 12 planned-yes tracker families are eligible or caveated (5 `eligible_for_phase02_now` + 7 `eligible_with_caveat`) | `tracker_events_feature_eligibility.csv` grouped by `status_in_game_snapshot` | new §4.3.3 — counts MUST trace to the artifact. |
| 6 | 3 tracker families remain `blocked_until_additional_validation`: `mind_control_event_count`, `army_centroid_at_cutoff_snapshot`, `playerstats_cumulative_economy_fields` | `tracker_events_feature_eligibility.csv` rows 11, 12, 15 | new §4.3.3 — enumerate by name; brief one-clause reason per family (V4 sparse / V6 decoder + Amendment-5 source-confirmation gap / V3 cumulative-economy blocked). |
| 7 | `slot_identity_consistency` is a sanity gate, NOT a model input | `tracker_events_feature_eligibility.csv` row 14 `notes_for_phase02 = "feature-engineering sanity gate; not a model input"` | new §4.3.3 — explicitly distinguished from the 4 other `eligible_for_phase02_now` rows. |
| 8 | This does NOT close full tracker scope | `01_03_05_tracker_events_semantic_validation.md:14` (`full_tracker_scope_closed_predicate_satisfied: False`); `methodology_risk_register.md:399` (`MITIGATED-NARROWED, NOT fully resolved`) | new §4.3.3 — must be stated explicitly. |
| 9 | This does NOT imply Phase 02 closure | `PHASE_STATUS.yaml` (sc2egset Phase 02 = `not_started`); F4 in audit §8 | new §4.3.3 OR `[repair-§4.3.2]`. Implicit form acceptable if the surrounding §4.3 prose carries enough context; explicit form preferred. |
| 10 | This does NOT imply Step 02_01_01 closure | F4 in audit §8; SC2EGSet only carries provisional registry at `partial_coverage_v9_baseline` per PR #216 | new §4.3.3 — explicit form REQUIRED (Step 02_01_01 closure is a load-bearing examiner-vulnerable claim). |
| 11 | This does NOT imply leakage-free materialized features | F7 in audit §8 | new §4.3.3 non-supersession statement. |
| 12 | CROSS-02-01-v1.0.1 post-materialization audit remains mandatory for materialized features | `reports/specs/02_01_leakage_audit_protocol.md` (LOCKED 2026-04-26) | new §4.3.3 non-supersession statement — cite spec by name. |

## Forbidden claims for writer-thesis

Writer-thesis dispatch prompt MUST include this section verbatim. Each forbidden claim cross-references the F-number from `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` §8 where applicable.

| # | Forbidden claim | Cross-reference |
|---|---|---|
| 1 | "SC2 tracker scope is closed" / "full tracker scope is validated" / "tracker semantic validation is complete" (without `narrowed` qualifier) | F9 |
| 2 | Any claim that tracker-derived features can be pre-game features | F16 (permanently forbidden — Invariant I3 / Amendment 2) |
| 3 | Promotion of any `blocked_until_additional_validation` row (`mind_control_event_count`, `army_centroid_at_cutoff_snapshot`, `playerstats_cumulative_economy_fields`) to eligible status | F9 |
| 4 | Final feature catalog claim ("the Phase 02 feature catalog contains [N] features across [K] families") | F3 |
| 5 | Phase 02 closure claim ("Phase 02 is complete", "Phase 02 is ready", "Phase 02 is closed") for any dataset | F4 |
| 6 | Step 02_01_01 closure claim ("Step 02_01_01 is closed", "Step 02_01_01 is complete") | F4 |
| 7 | Leakage-free materialized features claim ("our features are leakage-free", "no leakage in the materialized feature set") | F7 |
| 8 | Post-materialization audit clearance claim ("CROSS-02-01-v1.0.1 has cleared the Phase 02 feature set") | F8 |
| 9 | Model-ready feature matrix claim ("we have a model-ready feature matrix") | F3 |
| 10 | Any model result, accuracy, F1, AUC, Brier, log-loss number | F1 |
| 11 | Any tabular-vs-GNN performance conclusion | F2 |
| 12 | Cross-game generalizability claim (beyond the bounded four-confound framing already in §1.3 / §1.4 / Tabela 4.4) | F1, F5 |

## File Manifest

### Allowed writes

| File | Action | By task | Notes |
|------|--------|---------|-------|
| `planning/current_plan.md` | Rewrite | T01 | Full overwrite of bootstrap stub. |
| `planning/current_plan.critique.md` | Create | T01 | Parent-persisted from reviewer-adversarial chat output. |
| `thesis/chapters/04_data_and_methodology.md` | Update (in-place) | T02 | (a) Repair line 331 paragraph; (b) insert new §4.3.3 between line 331 and current line 333; (c) renumber current §4.3.3 to §4.3.4 (conditional on Q-A resolution). |
| `thesis/chapters/REVIEW_QUEUE.md` | Update (append) | T02 | Pending row(s) for §4.3.3 + §4.3.2 repair. |
| `thesis/WRITING_STATUS.md` | Update (line-scoped) | T02 | Chapter 4 row status note + line 75 stale-sentence repair. Conditional on Q-B = YES. |
| `CHANGELOG.md` | Update (append) | T05 | `[3.53.0]` block under `[Unreleased]`. |
| `pyproject.toml` | Update (line-scoped) | T05 | `version = "3.52.2"` → `version = "3.53.0"`. |
| `.github/tmp/pr.txt` | Create then remove | T06 | Created for `gh pr edit --body-file`; removed after PR body update per memory. |

### Forbidden writes (HALT if touched)

| File | Why forbidden |
|------|---------------|
| `thesis/chapters/01_introduction.md` | Out of scope — TQ-02 is §4.3 only. |
| `thesis/chapters/02_theoretical_background.md` | Out of scope. (Note: audit §10.2 row 2 covers an EsportsBench drift in §2.5.5 — that is TQ-04, not this PR.) |
| `thesis/chapters/03_related_work.md` | Out of scope. (Note: audit §10.2 row 2 covers EsportsBench drift in §3.2.4 and §3.5 — TQ-04, not this PR.) |
| `thesis/chapters/04_data_and_methodology.md` §4.1.*, §4.2.*, §4.4.*, §4.5, §4.6 | Out of scope — TQ-02 is §4.3 only. |
| `thesis/chapters/05_experiments_and_results.md` | Audit TQ-06 deferred. |
| `thesis/chapters/06_discussion.md` | Audit TQ-07 deferred. |
| `thesis/chapters/07_conclusions.md` | Audit TQ-08 deferred. |
| `thesis/references.bib` | No new bibkey required (all needed bibkeys already exist). |
| `thesis/pass2_evidence/**` | Out of scope — this PR consumes pass2_evidence; does not modify it. |
| `thesis/THESIS_STRUCTURE.md` | Out of scope — section spec is unchanged; only the chapter prose is added. |
| `thesis/THESIS_WRITING_MANUAL.md` | Out of scope. |
| `src/rts_predict/games/<game>/datasets/<dataset>/reports/STEP_STATUS.yaml` | Forbidden under data-analysis-lineage rule §Artifact discipline. |
| `src/rts_predict/games/<game>/datasets/<dataset>/reports/PHASE_STATUS.yaml` | Same. |
| `src/rts_predict/games/<game>/datasets/<dataset>/reports/PIPELINE_SECTION_STATUS.yaml` | Same. |
| `src/rts_predict/games/<game>/datasets/<dataset>/reports/ROADMAP.md` | Same. |
| `src/rts_predict/games/<game>/datasets/<dataset>/reports/research_log.md` | Same. |
| `src/rts_predict/games/<game>/datasets/<dataset>/reports/INVARIANTS.md` | Same. |
| `src/rts_predict/games/<game>/datasets/<dataset>/reports/artifacts/**` | Same — generated artifacts are immutable per Invariant I9 / lineage rule. |
| `sandbox/**` | Same — notebooks are out of scope for Category F. |
| `reports/research_log.md` (CROSS index) | Out of scope. |
| `reports/specs/**` | Out of scope — specs LOCKED. |
| `src/**/*.py`, `tests/**/*.py` | Out of scope — no code change. |
| `.claude/**` (rules, agents, scientific-invariants) | Out of scope — invariants and rules are not modified. |
| `docs/**` (PHASES.md, TAXONOMY.md, templates, manuals) | Out of scope. |

## Gate Condition

The plan is COMPLETE and PR #218 may merge when ALL of the following are observable:

1. `planning/current_plan.md` matches this plan content verbatim; `planning/current_plan.critique.md` contains the T01 reviewer-adversarial verdict with explicit PROCEED disposition (or REVISE that was satisfied and re-reviewed).
2. `git diff master..HEAD --name-only` (after T05) lists EXACTLY: `planning/current_plan.md`, `planning/current_plan.critique.md`, `thesis/chapters/04_data_and_methodology.md`, `thesis/chapters/REVIEW_QUEUE.md`, `CHANGELOG.md`, `pyproject.toml`, and conditionally `thesis/WRITING_STATUS.md` (if Q-B = YES). No other files.
3. `grep -nE "^### 4\\.3" thesis/chapters/04_data_and_methodology.md` shows the new §4.3.3 in correct sequence with the renumbered §4.3.4 (conditional on Q-A = recommended default).
4. `grep -nE "nie została zrealizowana" thesis/chapters/04_data_and_methodology.md` returns 0 matches.
5. The new §4.3.3 contains all 12 required-claim anchors (verified by reviewer-deep T03).
6. The new §4.3.3 contains NONE of the 12 forbidden claims (verified by reviewer-adversarial T04).
7. `pyproject.toml` shows `version = "3.53.0"`; `CHANGELOG.md` contains a `## [3.53.0]` block dated 2026-05-17.
8. `gh pr view 218 --json isDraft` returns `{"isDraft": false}`; CI checks pass.
9. Reviewer-adversarial T04 final verdict is PROCEED (or REVISE-MINOR with revisions applied and re-reviewed within the 3-round cap).
10. User has confirmed PR #218 is mergeable.

## Halt conditions specific to this PR

In addition to the generic data-analysis-lineage and thesis-writing rule halts, halt this plan immediately if any of the following occur:

- **HALT-1.** Any of the 12 required-claim anchors becomes unsupported by repo evidence (e.g., if a downstream PR re-opens `tracker_events_feature_eligibility.csv` row counts).
- **HALT-2.** Writer-thesis (T02) attempts to write outside §4.3 of `thesis/chapters/04_data_and_methodology.md` (other §4.x or other chapters), or attempts to write any file outside the allowed manifest.
- **HALT-3.** Any prose suggests "closed" / "complete" / "final" / "validated" where only `narrowed` / `provisional` / `under recorded eligibility scope` is supported by the evidence base.
- **HALT-4.** Reviewer-adversarial (T01 or T04) raises a METHODOLOGY BLOCKER that cannot be resolved within the 3-round cap.
- **HALT-5.** Writer-thesis adds any external citation beyond `[Bialecki2023]` and `[BlizzardS2Protocol]` without WebSearch verification (per `.claude/rules/thesis-writing.md` Literature Search Protocol). Deferring such a citation to Pass-2 with a `[NEEDS CITATION]` flag is acceptable; embedding it verbatim is not.
- **HALT-6.** `git diff master..HEAD --name-only` after T02 lists any file outside the allowed manifest.
- **HALT-7.** Any attempt to modify a spec file (`reports/specs/02_0*.md`), a status YAML, a ROADMAP, a research log (dataset or root), a dataset artifact, a sandbox notebook, a `.py` code file, or any file under `.claude/`.
- **HALT-8.** Verification step (e.g., reviewer-deep T03) discovers a numerical mismatch between the prose and the artifact (e.g., the prose says "14 rows" instead of "15 rows", or "4 eligible" instead of "5 eligible").
- **HALT-9.** Open Question Q-A (subsection numbering) is not resolved by the user before T02 dispatch.
- **HALT-10.** Open Question Q-B (WRITING_STATUS line 75 repair) is not resolved by the user before T02 dispatch.

## Hard constraints for writer-thesis dispatch

The T02 dispatch prompt MUST include all of the following, verbatim, in addition to the standard `.claude/rules/thesis-writing.md` Pass-1 Data-variant sequence and the `.claude/author-style-brief-pl.md` voice constraints.

1. **Allowed files (write):** `thesis/chapters/04_data_and_methodology.md`, `thesis/chapters/REVIEW_QUEUE.md`, and (conditional on Q-B) `thesis/WRITING_STATUS.md`. No other writes.
2. **Forbidden files (write):** all files in the "Forbidden writes" table above. The full forbidden list MUST appear in the dispatch prompt.
3. **Stop conditions:** all 10 HALT conditions above MUST appear in the dispatch prompt.
4. **Insertion point:** new §4.3.3 inserted after line 331 (end of §4.3.2's stale paragraph, which is being rewritten) and before current line 333 (current §4.3.3 heading, which is being renumbered to §4.3.4).
5. **Repair target:** the single Polish paragraph at line 331, starting `**Status walidacji semantycznej strumienia tracker_events_raw.**`, MUST be rewritten in-place (not deleted-and-replaced from a separate paragraph) to acknowledge Step 01_03_05 completion and forward-refer to the new §4.3.3.
6. **Heading numbering:** `### 4.3.3 Walidacja semantyczna strumienia tracker_events_raw (Step 01_03_05; GATE-14A6 — narrowed)` (or close Polish equivalent). Renumber current `### 4.3.3 AoE2-specific features` → `### 4.3.4 AoE2-specific features`. Conditional on Q-A resolution.
7. **12 required-claim anchors** (`## Required claim surface` table above) MUST appear verbatim in the dispatch prompt.
8. **12 forbidden-claim items** (`## Forbidden claims for writer-thesis` table above) MUST appear verbatim in the dispatch prompt.
9. **Expected length:** ~3–6k characters Polish for the new §4.3.3; ~600–1000 characters Polish for the §4.3.2 paragraph repair. Total prose delta ~3.5–7k characters.
10. **"Must justify / must contrast / must cite" lists** from the T02 specification above MUST be replicated verbatim in the dispatch prompt.
11. **No new bibkey added without WebSearch verification.** `[Bialecki2023]` and `[BlizzardS2Protocol]` are the only pre-authorized external citations.
12. **Inline-flag discipline:** writer-thesis MUST plant `[REVIEW:]` or `[NEEDS CITATION]` flags for any Pass-2-required verification. Inline-flag counts MUST appear in the Chat Handoff Summary.
13. **Chat Handoff Summary required** per `.claude/rules/thesis-writing.md` §"Chat Handoff Summary Format" (Data variant).

## Out of scope

- Audit TQ-03 (NEW §4.5 Phase 02 registry methodology subsection) — separate future PR (audit §9.1).
- Audit TQ-04 (EsportsBench version harmonization in §2.5.5, §3.2.4, §3.5) — separate future PR.
- Audit TQ-05 (aoestats interface-CSV row-count clarification in §4.1.4) — separate future PR.
- Audit TQ-06, TQ-07, TQ-08 (Chapters 5, 6, 7) — deferred per Q1 resolution in audit §10.6.
- Any modification to dataset `STEP_STATUS.yaml`, `PHASE_STATUS.yaml`, `ROADMAP.md`, `research_log.md`, `INVARIANTS.md`, or any `reports/<dataset>/artifacts/**` file.
- Any modification to `reports/specs/**` (LOCKED).
- Any sandbox notebook execution.
- Any `.py` code file or `tests/` change.
- Any `.claude/**` (rules, agents, scientific-invariants) change.
- Any new bibkey in `thesis/references.bib` without prior WebSearch verification.
- Any thesis chapter outside `04_data_and_methodology.md`.
- Any §4.x subsection inside `04_data_and_methodology.md` other than §4.3 (specifically, §4.3.2 paragraph repair + new §4.3.3 insert + §4.3.3 → §4.3.4 renumber).

## Open Questions

Each question must be resolved by the user before T01 review can finalize (or before T02 dispatch if Q-A/Q-B are still open after T01).

- **Q-A — Subsection numbering for the new tracker-eligibility prose.** Options: (a) `### 4.3.3 Walidacja semantyczna strumienia tracker_events_raw (Step 01_03_05; GATE-14A6 — narrowed)`, renumber current §4.3.3 (AoE2) → §4.3.4 [PLAN-RECOMMENDED DEFAULT]; (b) insert as labelled prose block inside §4.3.2 with no number change; (c) other (specify). **Recommended:** (a). Resolves: USER DECISION before T01 dispatch.
- **Q-B — Update `thesis/WRITING_STATUS.md` line 75 in T02.** Line 75 currently asserts "Step 01_03_05, not yet scheduled" — stale by date. Options: (a) include the one-line repair in T02 scope and the file in the manifest [PLAN-RECOMMENDED DEFAULT]; (b) defer to a separate sweep PR. **Recommended:** (a). Co-locating the update with the prose change reduces the risk of WRITING_STATUS drifting against the chapter file. Resolves: USER DECISION before T01 dispatch.
- **Q-C — Whether to surface the V3 fixed-point divide-by-4096 SC2EGSet decoder convention in the new §4.3.3.** Options: (a) half-sentence acknowledgement inside the per-row caveat surface [PLAN-RECOMMENDED DEFAULT — bounded by Unknown U4]; (b) standalone paragraph; (c) omit entirely and defer to Step 02_01_02 prose. **Recommended:** (a). Resolves: writer-thesis discretion within the dispatch's "must justify" item; no user gate needed unless the writer asks.
- **Q-D — Version-bump policy verification.** This plan assumes minor bump (`3.52.2` → `3.53.0`) per the writer's reading of `.claude/rules/git-workflow.md` ("minor for feat/refactor/docs"). If the rule has been amended to patch-only for docs-only changes (e.g., Cat E vs Cat F distinction), fall back to `3.52.3`. Resolves: parent session check against the live rule before T05 dispatch.
- **Q-E — Whether the eligibility-CSV per-row enumeration belongs in a table inside §4.3.3.** Options: (a) prose-with-counts (NO table) [PLAN-RECOMMENDED DEFAULT — matches audit TQ-02 routing depth]; (b) inline summary table listing all 15 rows; (c) inline table listing only the 3 blocked rows. **Recommended:** (a). Tables are a future PR commitment (TQ-03 §4.5 may carry tabular forms); §4.3.3 stays prose to minimize the per-touch table surface that examiners can challenge. Resolves: writer-thesis discretion within the dispatch's expected-length envelope.

---

## Note for parent session — critique requirement

This is a **Category F plan**. Per `docs/templates/planner_output_contract.md` and `.claude/rules/data-analysis-lineage.md` §Agent-and-model-routing-discipline, adversarial critique is REQUIRED before execution begins. Parent session MUST:

1. Persist this plan content to `planning/current_plan.md` (overwriting bootstrap stub `df7b2613`).
2. Dispatch `@reviewer-deep` (structural correctness, spec compliance, invariant tracing) AND `@reviewer-adversarial` (Mode A — plan review; methodology defensibility) in PARALLEL.
3. Persist reviewer-adversarial chat output to `planning/current_plan.critique.md` via the Write tool (reviewer-adversarial cannot write files due to platform `disallowedTools: Write, Edit`).
4. Wait for user approval before dispatching writer-thesis (T02).
5. Do NOT dispatch writer-thesis directly from this planning session. T02 occurs in a fresh execution session per `thesis/plans/writing_protocol.md` §6.4.

**Per critique-instruction policy (planner_output_contract line 17–21):**

> "For Category A or F, adversarial critique is required before execution. Dispatch reviewer-adversarial to produce `planning/current_plan.critique.md`."