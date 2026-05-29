# Critique: SC2EGSet Step 02_01_03 formal closure (Layer-1 planning PR)

**Reviewer-adversarial verdict:** APPROVE-WITH-NITS
**Blockers:** none
**Confidence:** HIGH
**Rationale:** All load-bearing planner claims verified on HEAD `5a62fc76`: PR #237 used evidence-date precedent (2026-05-23), the append-only validator is presence-only, the audit JSON contains all cited tokens at the cited values, Q-chain and PR #253/#255 PRs leave no STEP_STATUS rows, and PIPELINE_SECTION_STATUS / PHASE_STATUS already reflect target end-state. Closure is the correct atomic unit; no methodology defect in the artifact requires a fix PR before closure.

## Nits incorporated

### N1 — Precedent-mirroring wording

Originally the plan said "mirrors PR #237 verbatim shape" for the STEP_STATUS row. Master `STEP_STATUS.yaml` lines 200–204 (the on-disk 02_01_02 block) already include `pipeline_section: "02_01"`. Plan re-worded to "mirrors lines 200–204 verbatim shape" to remove the historical-precedent ambiguity. The proposed 02_01_03 row's 5 fields (`name`, `pipeline_section`, `status`, `completed_at`) match the master 02_01_02 block field-for-field.

### N2 — Date-token discipline

`completed_at = "2026-05-28"` mirrors PR #237 precedent verified by `git show a16d78c2` (PR #237 STEP_STATUS row used `completed_at: "2026-05-23"`, the PR #236 evidence date, not the PR #237 merge date 2026-05-24). The closure-PR CHANGELOG header `[3.82.1] — 2026-05-29` uses the closure-PR merge-date convention, distinct from `completed_at`. The plan now spells out this distinction in T03 + T04 and again in §Assumptions A3 and §OQ2.

### N3 — 02_01_99 precedent clarity

ROADMAP §02_01_99 lines 2622–2849 explicitly mark the step as a forward-declaring stub whose `gate.artifact_check` "NOT APPLICABLE TO THIS ROADMAP-STUB PR". STEP_STATUS.yaml at HEAD contains zero `02_01_99` mentions (verified). The DO_NOT_ADD decision is reinforced in §OQ1 with the Q-chain precedent (PRs #242, #243, #245, #247, #249, #251 all produced no STEP_STATUS rows) and the PR #255 precedent (the 02_01_99 omit-closure artifact PR itself added no STEP_STATUS row).

### N4 — Research_log prepend safety

The append-only validator `_check_dataset_research_log_evidence_present` (`adjudicate_history_rating_reconstruction.py` lines 1178–1212) performs **presence-only substring search**, NOT byte-position or offset validation. Prepending the new closure entry above the PR #259 still_open entry is therefore safe under this validator. The plan now cites the function name and line range explicitly in §Assumptions A8 and §Gate Condition item 9.

### N5 — PIPELINE_SECTION_STATUS "byte-unchanged" claim

The reviewer-adversarial flagged that master `5a62fc76` carries `02_01: complete` despite STEP_STATUS having no `02_01_03` row — i.e., the derivation invariant was effectively violated at the time PR #259 merged. The plan now treats the future closure's 02_01_03 row addition as RESTORING (not disturbing) the invariant, and adds OQ4 to record the ambiguity for future maintainer attention without pre-deciding it.

### N6 — 5-file scope completeness

No `INVARIANTS.md`, `docs/PHASES.md` cell, `thesis/WRITING_STATUS.md`, or `thesis/chapters/REVIEW_QUEUE.md` touch is required for step-level closure (only phase-level closure triggers WRITING_STATUS check per CLAUDE.md "Progress Tracking"). The 5-file scope (STEP_STATUS.yaml + dataset research_log.md + pyproject.toml + CHANGELOG.md + planning/INDEX.md) is correct and minimal.

## Risks not addressed by this plan

- **R1 — Future audit re-run sensitivity.** If a future re-run of the PR #259 materialization on a different DuckDB hash produces a different Parquet SHA, the closure entry's `row_count` / `distinct_focal_match_count` would still hold but the SHA-256 provenance bonds would diverge. This is by design — the audit is re-runnable; the row count is content-stable.
- **R2 — Q-chain / 02_01_99 future revisit.** If a maintainer later decides 02_01_99 deserves its own status row, that requires a separate Layer-1 + Layer-2 plan pair; the present plan deliberately does NOT pre-decide that question (§OQ5).
- **R3 — PIPELINE_SECTION_STATUS derivation ambiguity.** §OQ4 records the historical inconsistency but does not propose to edit the section/phase YAMLs in the future closure PR. A separate governance review may revisit derivation semantics.

## Confidence assessment

HIGH for the 5-file scope, the DO_NOT_ADD 02_01_99 decision, the `completed_at = "2026-05-28"` date, the patch bump, and the prepend-above-still_open research_log placement. MEDIUM only on OQ4 (PIPELINE_SECTION_STATUS derivation), which the plan deliberately punts to a future governance review.
