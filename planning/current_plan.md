---
title: "SC2 tracker eligibility framing for Chapter 4 (TQ-02 + TQ-01) — BOOTSTRAP STUB"
category: F
branch: thesis/sc2-tracker-eligibility-section-4-3
date: 2026-05-17
planner_model: claude-opus-4-7
branch_prefix: thesis/
branch_name: thesis/sc2-tracker-eligibility-section-4-3
pr_title: "docs(thesis): add SC2 tracker eligibility framing for Chapter 4"
base_ref: "master @ 0a933be6"
base_commit: 0a933be6
created_date: 2026-05-17
dataset: sc2egset
phase: "02 (tracker eligibility scope only — no Phase 02 closure)"
pipeline_section: "n/a (Category F thesis prose; consumes prior Phase 01/02 evidence)"
step: "n/a (Category F prose update; no Step closure claimed)"
target_version: "TBD (filled by planner-science)"
version_current: "3.52.2"
version_bump_type: "TBD (filled by planner-science)"
critique_required: true
invariants_touched: []
stub: true
research_log_ref: null
---

# Plan: SC2 tracker eligibility framing for Chapter 4 — BOOTSTRAP STUB

> **Bootstrap stub only.** This file exists to anchor the draft PR. The full Category F plan is being authored by `@planner-science` and will overwrite this stub before any implementation step runs. Every section below is a placeholder.

## Scope

Stub. Full scope will be authored by `@planner-science`. Intended deliverable: a controlled Category F thesis prose update covering **TQ-02** (NEW §4.3.x SC2 tracker eligibility subsection in `thesis/chapters/04_data_and_methodology.md`) and **TQ-01** (repair of the stale §4.3.2 paragraph asserting SC2EGSet Step 01_03_05 was not implemented). Both rows derive from `thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md` §11 / §12 (PR #217 at master `0a933be6`).

## Problem Statement

Stub. Full problem statement will be authored by `@planner-science`. Outline: the existing draft of `thesis/chapters/04_data_and_methodology.md` §4.3.2 still asserts Step 01_03_05 was not implemented; the step landed 2026-05-05 with GATE-14A6 outcome `narrowed`, and the chapter must catch up. Additionally, the chapter lacks a tracker-eligibility subsection enumerating the 5+7+3 eligibility breakdown and the per-row caveats.

## Literature Context

Stub. Full literature context will be authored by `@planner-science`. Outline: the SC2EGSet paper [Bialecki2023] for tracker-event semantics; tracker_events fixture introduced in SC2 Patch 2.0.8; Invariant I3 + Amendment 2 (tracker features never pre-game); CROSS-02-01-v1.0.1 post-materialization audit gate.

## Assumptions & Unknowns

Stub. Full assumptions will be authored by `@planner-science`. Initial expected items: (a) all evidence artifacts cited remain on disk after PR #216/#217 merge; (b) Pass-2 literature verification for any new external citation is required before writer-thesis drafts.

## Execution Steps

Stub. Full execution-step decomposition will be authored by `@planner-science`. Expected outline (subject to planner revision):

- **T00** — draft PR + planning commit (this bootstrap commit + the planner-authored plan replacing this stub)
- **T01** — reviewer-deep + reviewer-adversarial on the plan
- **T02** — writer-thesis drafts §4.3.x + repairs §4.3.2 (only after T01 passes and user approves)
- **T03** — reviewer-deep on drafted prose
- **T04** — reviewer-adversarial on drafted prose
- **T05** — CHANGELOG + version bump
- **T06** — PR body refresh + mark ready

## File Manifest

Stub. Full manifest will be authored by `@planner-science`. Tentative allowed files for implementation:
- `thesis/chapters/04_data_and_methodology.md` (T02)
- `CHANGELOG.md` (T05)
- `pyproject.toml` (T05)
- `planning/current_plan.md` (planner-replaced from this stub; reviewer fixes if any)
- `planning/current_plan.critique.md` (only if reviewer-adversarial output is committed)

Forbidden in this PR: dataset artifacts, notebooks, code, specs, ROADMAPs, status YAMLs, research logs, other thesis chapters, Phase 03 files, AoE2 Phase 02 files.

## Gate Condition

Stub. Full gate condition will be authored by `@planner-science`. Expected gates: (a) §4.3.x exists in `04_data_and_methodology.md`; (b) §4.3.2 stale wording removed; (c) version bumped per Cat-F policy; (d) reviewer-deep + reviewer-adversarial both PASS; (e) no thesis chapter outside `04_data_and_methodology.md` modified; (f) no forbidden file touched.

## Open Questions

Stub. Open questions will be enumerated by `@planner-science` after evidence review. Likely candidates: section numbering choice (§4.3.3 vs §4.3.x?), exact tracker-row enumeration depth in prose, whether to introduce a `[POP:]`-style tag for blocked tracker rows.

## Status

`@planner-science` is currently authoring the full plan content. No implementation has started. No thesis chapter file has been touched. No dataset artifact, spec, status YAML, ROADMAP, research log, notebook, code, or raw data has been touched.
