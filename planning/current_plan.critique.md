# Critique: SC2EGSet Step 02_02_01 ROADMAP-only stub (Layer-1 planning PR)

**Reviewer-adversarial verdict:** APPROVE-WITH-NITS
**Blockers:** none
**Confidence:** HIGH
**Date:** 2026-05-29
**Base SHA:** `2c9080ae0d02e8733f60b974ef9f0c0ced36c849`
**Predecessor PR:** #262 (merged 2026-05-29)

This critique gates the Category A Layer-1 planning PR for SC2EGSet Pipeline
Section `02_02 — Symmetry & Difference Features`. The companion plan in
`current_plan.md` proposes a **two-PR sequence on branch
`feat/sc2egset-02-02-01-roadmap-stub`**:

- THIS Layer-1 planning PR: two files only
  (`planning/current_plan.md` + `planning/current_plan.critique.md`).
- FUTURE Layer-2 execution PR (same branch): four files only
  (ROADMAP.md + planning/INDEX.md + CHANGELOG.md + pyproject.toml),
  inserting one `### Step 02_02_01` ROADMAP block and bumping version to
  `3.83.0`. NO feature materialization in either PR.

## Lens assessments

- **Temporal discipline:** SOUND. Plan declares Invariant I3 inheritance
  from `02_01_03`; future ROADMAP block's halt-clause bars target-game and
  future-match leakage explicitly (item 10). Item 11 requires byte-stable
  upstream artifacts on every future 02_02 PR.
- **Statistical methodology:** N/A — ROADMAP-stub PR; no metric / model /
  fold computed.
- **Feature engineering:** SOUND in scope after nit application. I5
  inheritance correctly declared; difference-feature semantics aligned with
  Bradley-Terry per manual §3 L47.
- **Thesis defensibility:** STRONG. Non-batching rule explicitly cited;
  precedent ladder (PR #232 / #239 / #253 / #255 / #257 / #259 / #262)
  named per claim; the §02_01_03 amendment back-reference at
  ROADMAP L2837-L2849 is preserved verbatim.
- **Cross-game comparability:** MAINTAINED — `02_02` is dataset-agnostic
  per `docs/PHASES.md`; SC2EGSet stub uses race-only terminology and does
  not pre-empt AoE2 civilization vocabulary.

## Adjudication outcomes (planner choices, all approved)

- **Outcome A** (ROADMAP-only stub planning PR). B (direct execution),
  C (start Phase 03), D (reopen 02_01), E (PIPELINE_SECTION_STATUS first),
  F (hold) rejected on repo evidence.
- **Position:** insert new `### Step 02_02_01` block AFTER existing
  `### Step 02_01_99` (and its L2837-L2849 amendment back-reference),
  BEFORE `## Phase 03 — Splitting & Baselines (placeholder)` at L2853.
- **Predecessor:** `predecessors: "02_01_03"` single-string scalar
  matching Phase 02 ROADMAP idiom (L2360, L2691).
- **PIPELINE_SECTION_STATUS `02_02` row:** DEFER to a future post-stub PR
  per PR #230 precedent (the `02_01` row first landed at-step-closure of
  02_01_01, not at-stub-open).
- **Version bump:** minor `3.82.1 → 3.83.0` per three precedents
  (PR #232: 3.66.0 → 3.67.0; PR #239: 3.70.1 → 3.71.0; PR #253:
  3.78.0 → 3.79.0 — all minor for ROADMAP-only stubs on `feat/` branches).
  Bump lands in Layer-2, not Layer-1.
- **02_01_99 stub fate:** retain in place; deletion would break the
  amendment back-reference at L2837-L2849 (verified inside 02_01_99 block).

## Strong endorsements

1. **Outcome-E defer logic correctly reads PR #230 precedent.** The
   header derivation rule does NOT fire on ROADMAP-only stubs (verified
   against scientific-invariants.md L259-L295 / I9 research pipeline
   discipline).
2. **Position decision preserves the §02_01_03 amendment back-reference
   byte-unchanged.** Block ends at L2849 closing line + L2851 `---`
   separator; insertion point is well-defined.
3. **Invariant I5 correctly identified at L156-L170** with the exact
   slot-bias reasoning (`P(A wins | A focal) = 1 - P(B wins | B focal)`).
4. **Manual §3 verified at L43-L59.** Header reads "Symmetry in Pairwise
   Prediction Demands Difference Features" — both `symmetric` and
   `difference` are manual vocabulary; "Symmetry & Difference Features"
   pipeline name (`docs/PHASES.md` L115) is accurate.
5. **The 12-item future ROADMAP content list cleanly mirrors the
   §02_01_03 block schema** (verified via grep at ROADMAP L2622-L2849).
6. **Plan formatting hook compliance.** All 8 required `##` headings
   present (Scope, Problem Statement, Assumptions & Unknowns,
   Literature Context, Execution Steps, File Manifest, Gate Condition,
   Open Questions) — verified.

## Non-blocking nits (4) — all applied to `current_plan.md`

- **N1 (drop AoE2 leakage `civilization`):** SC2EGSet uses `race`
  exclusively. The future ROADMAP item 9 originally read
  "race/civilization-pair encoded interactions"; rewritten to
  "race-pair encoded interactions". `civilization` token removed
  from plan body entirely.
- **N2 (annotate 02_02 vs 02_05 scope boundary):** Race-pair encoded
  interactions are the canonical 02_05 (Categorical Encoding &
  Interactions) family per manual §6 L133. Future ROADMAP item 9
  annotates the family as "candidate; may defer to 02_05 — Categorical
  Encoding & Interactions"; OQ6 and A13 record the deferred adjudication.
- **N3 (no hard-coded row-count gate at Layer-1):** Future ROADMAP gate
  item 11 no longer binds a literal `44,418` row count; rewritten to
  "row count equal to the measured row count of the `02_01_03` Parquet
  artifact, re-measured by Layer-2 execution rather than hard-coded."
  A6 mirror-updated to remove binding row claim.
- **N4 (read 02_03 temporal spec at Layer-1):** L1.1 read list now
  explicitly includes `reports/specs/02_03_temporal_feature_audit_protocol.md`;
  future ROADMAP item 7 carries the spec into `external_references` with
  scoped-out annotation so the stub's halt-clauses do not silently
  encroach on `02_03`.

## Reasoning per challenge

1. **Is `02_02_01` the next atomic unit?** APPROVE. 02_01_99 retention
   is correct; it exists as a documented ROADMAP-only stub with zero
   STEP_STATUS row (I9 research-pipeline discipline preserved — its
   conclusions derive from its own back-reference to 02_01_03).
   Deletion would mutate the §02_01_03 amendment lineage. Opening 02_02
   does not require closure of 02_01_99 because section ordering is
   independent of decision-lineage siblings.
2. **Phase 03 barrier discipline.** APPROVE. Future ROADMAP item 5
   explicitly BARS Phase 03 and Step 02_02_02+. Item 10 enumerates
   "Phase 03 split-derived features (no split exists yet)" as a hard
   exclusion. No silent Phase-03 opening.
3. **ROADMAP-only stub discipline.** APPROVE. Layer-2 4-file manifest
   matches PR #232, #239, #253 precedents file-for-file (ROADMAP.md +
   INDEX.md + CHANGELOG.md + pyproject.toml).
4. **Predecessor token.** APPROVE. Every Phase 02 ROADMAP step at
   L2158, L2360, L2691 uses single-string predecessor scalar.
   `"02_01_03"` is methodologically correct (the closing step that
   produces the canonical history-enriched Parquet input).
5. **Symmetry/difference scope correctness.** APPROVE-WITH-NITS
   (N1+N2 applied). Manual §3 verified; both "symmetric" and
   "difference" are manual vocab. Invariant I5 covers slot bias.
   Cross-region indicator handling per PR #243/#255 carries a
   sensitivity indicator co-registered with difference features — not
   a difference-feature input itself. A8 wording correct.
6. **PIPELINE_SECTION_STATUS Outcome-E.** APPROVE. PR #230 added
   `02_01: complete` row at-step-closure (not at-step-open) — defer
   logic for `02_02` row is sound.
7. **Version bump policy.** APPROVE. Three precedents follow
   `X.Y.Z → X.(Y+1).0` pattern for ROADMAP-only stubs on `feat/`
   branches. Proposed `3.82.1 → 3.83.0` matches.
8. **Layer-2 4-file manifest exhaustive.** APPROVE. No additional
   `reports/*.yaml`, `docs/PROGRESS.md`, or indexing file appears in
   precedent stub PRs.
9. **No data-analysis-lineage rule violations.** APPROVE. ROADMAP-only
   stub cannot trigger any value materialization downstream; precedent
   stubs all conformed.
10. **02_01_99 amendment back-reference dependency.** VERIFIED ON
    DISK — the back-reference at L2837-L2849 lives INSIDE the 02_01_99
    block. Deleting that block would orphan the back-reference.
    Retention required.
11. **Plan formatting hook compliance.** APPROVE. All 8 required `##`
    headings present and verified.
12. **Frontmatter validity.** APPROVE. YAML frontmatter parses cleanly;
    `target_version_bump: "3.82.1 -> 3.83.0"` is quoted scalar; pattern
    matches PR #239 / PR #253 plan frontmatter precedent.
13. The 12-item future ROADMAP content list duplicates plan content
    (correct — the plan SHOULD declare what the Layer-2 stub will
    say). No contradiction with the 02_02 spec; the spec specifies
    feature families that the stub item 9 declares as "planned."
14. Invariant IDs I3, I5, I6, I7, I8, I9, I10 verified in
    `.claude/scientific-invariants.md` (universal invariant space
    1-10 inclusive).
15. APPROVE-WITH-NITS — N1 applied; `civilization` is AoE2 terminology
    (spec L319-L320). SC2EGSet uses `race` exclusively (spec L224).
16. APPROVE-WITH-NITS — N4 applied; 02_03 spec now in L1.1 reads and
    in future ROADMAP `external_references`.

## Files verified during review

- `/Users/tomaszpionka/Projects/rts-outcome-prediction/.claude/scientific-invariants.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/docs/PHASES.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/docs/ml_experiment_lifecycle/02_FEATURE_ENGINEERING_MANUAL.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/reports/specs/02_02_feature_engineering_plan.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/reports/specs/02_03_temporal_feature_audit_protocol.md`
  (re-confirmed at Layer-1 per N4)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
  (L2622-L2879 — 02_01_99 block + Phase 03 placeholder boundary)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md`
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
  (02_01_03 complete L205-L209; no 02_02 row)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
  (02_01 complete L51-L54; no 02_02 row)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`
  (Phase 02 in_progress; Phase 03 not_started)

## Weakest link / strongest defensibility risk

The strongest risk pre-nit was **N1/N2** — the future ROADMAP item 9
originally mixed `civilization` (AoE2-only terminology) into an SC2EGSet
stub and opened race-pair interaction encoding (canonical 02_05 example
per manual §6 L133). Both are wording fixes, not architectural problems,
but uncorrected they would create cross-game terminology drift and
weaken the 02_02-vs-02_05 boundary. Both applied.

## Recommended next step

**Materialize the Layer-1 draft PR** (this critique recommends approval
with the four wording nits applied to `current_plan.md`). The draft PR
must keep the diff scoped to exactly:

- `planning/current_plan.md`
- `planning/current_plan.critique.md`

No ROADMAP edit, no status YAML, no research_log, no CHANGELOG, no
pyproject, no INDEX, no source/test/notebook/artifact change in this
Layer-1 PR. Layer-2 execution (the actual ROADMAP-stub edit) runs in a
separate execution prompt on the same branch.
