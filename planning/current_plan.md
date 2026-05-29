---
title: "SC2EGSet Step 02_01_03 formal closure (Layer-1 planning PR)"
category: C
branch: chore/sc2egset-02-01-03-formal-closure
base_ref: master
base_sha: 5a62fc768a099eb73e449db081fdbac70a68a98e
draft_pr_files:
  - planning/current_plan.md
  - planning/current_plan.critique.md
future_execution_files:
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
  - pyproject.toml
  - CHANGELOG.md
  - planning/INDEX.md
future_execution_file_count: 5
reviewer_adversarial_verdict: APPROVE-WITH-NITS, 0 blockers, HIGH confidence (nits incorporated into this plan)
date: "2026-05-29"
---

## Scope

Author a Category C Layer-1 closure planning artifact for SC2EGSet Step 02_01_03 after PR #259 (merged at master `5a62fc76`) materialized the five-family Parquet (44,418 × 28; 22,209 distinct `focal_match_id`) and the first non-vacuous CROSS-02-01 audit pair (`verdict = PASS`, `features_audited_count = 24`) but deliberately left closure deferred.

This planning PR writes only `planning/current_plan.md` + `planning/current_plan.critique.md`. A SEPARATE Layer-2 execution PR will perform:
- a single `STEP_STATUS.yaml` row addition for `02_01_03`;
- a dataset `research_log.md` closure entry **prepended** above the PR #259 `still_open` entry (preserving it byte-shifted only);
- a patch version bump 3.82.0 → 3.82.1;
- a `CHANGELOG.md [3.82.1]` block;
- a `planning/INDEX.md` archive flip of PR #259.

Future Layer-2 execution file count: **5**.

Step 02_01_04 and Phase 03 remain BARRED by this planning PR and by the future closure execution PR.

## Problem Statement

Three structural facts force formal closure:

1. **STEP_STATUS.yaml header rule violation.** STEP_STATUS.yaml lines 1–11 declare verbatim: "Derived from ROADMAP.md step definitions. If this file disagrees with the ROADMAP, this file is wrong." Repo state today:
   - ROADMAP §"Step 02_01_03" (lines 2274–2618, with the `materialization_scope_amendment_post_pr_255` token) declares Step `02_01_03` with the five-family scope (`focal_player_history`, `opponent_player_history`, `matchup_history_aggregate`, `cross_region_fragmentation_handling`, `in_game_history_aggregate`; `reconstructed_rating` excluded).
   - ROADMAP §"Step 02_01_99" (lines 2622–2849) declares the ROADMAP-only follow-up stub for the rating omit-closure lineage segment.
   - STEP_STATUS.yaml stops at `02_01_02: complete` (lines 200–204). No `02_01_03` row; no `02_01_99` row.
   - Per the YAML header rule, STEP_STATUS.yaml is currently wrong relative to ROADMAP for `02_01_03`.

2. **PR #259 baseline carries `closure_status: still_open`** in dataset `research_log.md` (line 12, verified verbatim). That entry's own §"What this means" reads: "Status YAML flips … are deferred to a separate U2.B-style closure PR (per PR #237 precedent). The next 02_01 step … remains DEFERRED; Phase 03 is NOT started."

3. **CROSS-02-01 §5 gate is mechanically cleared** by PR #259 (`features_audited` length 24 + `verdict = PASS` + JSON/MD at spec-named paths under `reports/artifacts/02_01_03/`). The materialization evidence justifying closure exists on disk at master `5a62fc76`.

## Assumptions & Unknowns

- **A1 (Outcome A is justified).** PR #237 → PR #236 precedent (research_log.md L35–L114) shows separate U2.B closure PRs as standard for Phase-02 materialization-then-closure sequences. Direct execution (B), starting 02_01_04 (C), starting Phase 03 (D), additional fix PR (E), or hold (F) are all inappropriate: PR #259's audit was non-vacuous PASS; the 02_01_99 stub already merged at PR #253; the omit-closure decision artifact already merged at PR #255; no new evidence is required to flip status. **No methodology defect** in PR #259's artifact on master `5a62fc76` was identified by reviewer-adversarial.
- **A2 (`02_01_99` DO_NOT_ADD a STEP_STATUS row).** See §Open Questions OQ1 for the binding rationale, reinforced by the reviewer-adversarial nit confirming PR #255 added no STEP_STATUS row.
- **A3 (`completed_at = "2026-05-28"`).** Mirrors the PR #237 → PR #236 evidence-date convention (`git show a16d78c2` confirmed PR #237 used PR #236 evidence date `2026-05-23`). PR #259 audit JSON L5 records `"audit_date": "2026-05-28"`; PR #259 dataset research_log entry header (L5) is dated `2026-05-28`. The closure PR's CHANGELOG header will use closure-PR merge date `2026-05-29` (distinct from `completed_at`).
- **A4 (patch bump 3.82.0 → 3.82.1).** Per `.claude/rules/git-workflow.md` L25 "patch for fix/test/chore"; closure adds no on-disk artifact (no Parquet, no audit, no notebook, no module, no test). Matches PR #237 `3.70.0 → 3.70.1` precedent.
- **A5 (Branch name `chore/sc2egset-02-01-03-formal-closure`).** Mirrors PR #237's `chore/sc2egset-02-01-02-formal-closure` slug substitution.
- **A6 (PIPELINE_SECTION_STATUS.yaml + PHASE_STATUS.yaml byte-unchanged).** Master state (verified): `02_01: complete` (PIPELINE_SECTION_STATUS.yaml line 54); Phase 02 `in_progress`, Phase 03 `not_started` (PHASE_STATUS.yaml lines 22–23). Adding the 02_01_03 row RESTORES (rather than disturbs) the STEP_STATUS-derives-from-ROADMAP invariant; PIPELINE_SECTION_STATUS / PHASE_STATUS already reflect the target end-state.
- **A7 (No root `reports/research_log.md` edit).** Per CLAUDE.md "After Category A step: Update the active dataset's `research_log.md`" — root research_log is not updated for sub-phase step closures.
- **A8 (Append-only-safe research_log prepend).** The `_check_dataset_research_log_evidence_present` function in `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_rating_reconstruction.py` (lines 1178–1212) performs presence-only substring search, NOT byte-position validation. Prepending the new closure entry above the PR #259 still_open entry is safe under this validator, provided every PR #245-era evidence token remains present somewhere in the file (the still_open entry retains them verbatim because it is line-offset-shifted, not edited).

## Literature Context

Three repo precedents bind this plan:

- **PR #237 (`a16d78c2`, merged 2026-05-24)** — direct precedent. U2.B closure PR for Step 02_01_02. 5-file diff: STEP_STATUS.yaml + dataset research_log.md (closure entry prepended above PR #236 still_open entry) + CHANGELOG.md [3.70.1] + pyproject.toml (3.70.0 → 3.70.1) + planning/INDEX.md. `completed_at = "2026-05-23"` (PR #236 audit-evidence date, NOT PR #237 merge date). NO ROADMAP / NO PIPELINE_SECTION_STATUS / NO PHASE_STATUS / NO root research_log / NO artifact / NO source / NO test / NO notebook. Branch `chore/sc2egset-02-01-02-formal-closure`. Research_log header: "Formal closure of Step 02_01_02 (U2.B; status YAML flip; no new artifact)".
- **PR #230 → PR #229 (`0c45c490` ← `a14dc547`, merged 2026-05-21 / 2026-05-22)** — second-order vacuous-closure precedent. PR #229 persisted evidence with `closure_status: still_open`; PR #230 added STEP_STATUS row `02_01_01: complete` plus the PIPELINE_SECTION_STATUS `02_01: complete` flip and PHASE_STATUS Phase 02 `not_started → in_progress`. Distinguishes 02_01_03 closure from 02_01_01: section/phase rows already flipped during PR #230, so 02_01_03 closure leaves them byte-unchanged.
- **PR #255 (`52f9c108`, merged 2026-05-28)** — omit-closure decision artifact PR for the rating reconstruction Q-chain. Critically, PR #255 produced `02_01_99_rating_omit_closure.{csv,md}` artifacts but did NOT add any STEP_STATUS row (planning/INDEX.md L14: "NO STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS flip"). The Q-chain decision-artifact PRs #242, #243, #245, #247, #249, #251 likewise produced no STEP_STATUS rows. This is the binding precedent for the OQ1 02_01_99 DO_NOT_ADD decision.

## Execution Steps

The FUTURE Layer-2 closure execution PR (NOT this Layer-1 planning PR) will execute these steps:

**T01 — Branch + version bump.** Create `chore/sc2egset-02-01-03-formal-closure` off master `5a62fc76`. Edit `pyproject.toml` line 3: `version = "3.82.0"` → `version = "3.82.1"`. Commit as a single chore commit.

**T02 — STEP_STATUS.yaml: append exactly ONE row.** Append below the existing `02_01_02` block (currently lines 200–204) the single block:

    "02_01_03":
      name: "History-enriched pre_game feature-family materialization (sc2egset)"
      pipeline_section: "02_01"
      status: complete
      completed_at: "2026-05-28"

Field shape mirrors lines 200–204 verbatim (the on-disk `02_01_02` block at master `5a62fc76` already contains `pipeline_section: "02_01"` at line 202, so the future closure PR matches that shape). NO `02_01_99` row is added (see OQ1).

**T03 — Dataset `research_log.md` closure entry prepended above PR #259 `still_open` entry.** Insert a new section between line 3 (`---`) and line 5 (`## 2026-05-28 — Materialize Step 02_01_03 …`). The PR #259 entry remains byte-identical content; only its line offsets shift. Required tokens (all to appear verbatim in the new entry header bullets):

- `closure_status:` `closed`
- `materialization_state:` `materialized`
- `leakage_audit_state:` `post_materialization_pass`
- `status_yaml_state:` `complete`
- `features_audited_count:` `24`
- `row_count:` `44418`
- `distinct_focal_match_count:` `22209`
- `artifact:` `02_01_03_history_enriched_pre_game_features.parquet`
- `leakage_audit:` `reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}`
- explicit safeguard sentences: "Excluded family `reconstructed_rating` per PR #255 omit-closure"; the five-family list; "Step 02_01_04 NOT started; Phase 03 NOT started."

Header: `## 2026-05-29 — Formal closure of Step 02_01_03 (U2.B; status YAML flip; no new artifact)`. Sub-headings mirror PR #237's verbatim structure (research_log.md L51–L113): What / Why / How (reproducibility) / Findings / Decisions taken / Decisions deferred / Thesis mapping / Open questions / follow-ups / Scope notes. The §Why must cite the `completed_at = "2026-05-28"` convention text and the PR #237 precedent.

**T04 — `CHANGELOG.md [3.82.1]` block.** Insert below `[Unreleased]` (line 12) and above `[3.82.0]` (line 22): a new `## [3.82.1] — 2026-05-29 (PR #<TBD>: chore/sc2egset-02-01-03-formal-closure)` block. PR number placeholder `<TBD>` is filled by a follow-up housekeeping commit before merge (mirroring the `f0a3f551` chore commit "normalize PR #<TBD> placeholders to PR #260").

**T05 — `planning/INDEX.md` archive flip.** Archive PR #259 at merge SHA `5a62fc76` into the Archive table; promote the new chore branch to the Active plan line. Use the verbatim row format from planning/INDEX.md L10 (the PR #260 chore archive row) as template.

## File Manifest

### THIS Layer-1 planning PR (exactly 2 files; ONLY after reviewer approval):
- `planning/current_plan.md`
- `planning/current_plan.critique.md`

### Future Layer-2 execution PR (exactly 5 files):
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
- `pyproject.toml`
- `CHANGELOG.md`
- `planning/INDEX.md`

### Forbidden in future Layer-2 execution (must NOT appear in diff):
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (already records 02_01_03 + 02_01_99; PR #257 amendment is sufficient)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` (02_01 already complete; derivation rule unchanged)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` (Phase 02 stays in_progress; Phase 03 stays not_started)
- `reports/research_log.md` (root)
- any source `.py`, test `.py`, notebook `.py`/`.ipynb`, artifact (Parquet/CSV/MD/JSON), spec under `reports/specs/`, cleaning-layer YAML under `data/db/schemas/`
- any AoE2 path under `src/rts_predict/games/aoe2/**`
- any thesis chapter, bib, appendix under `thesis/**`
- any `docs/**`, `.claude/**`, or `data/**` path
- `INVARIANTS.md`

## Gate Condition

The future Layer-2 closure PR's reviewer gate is satisfied iff ALL of:

1. `STEP_STATUS.yaml` contains exactly ONE new block keyed `"02_01_03"` with `status: complete`, `completed_at: "2026-05-28"`, `name: "History-enriched pre_game feature-family materialization (sc2egset)"`, `pipeline_section: "02_01"`. No `"02_01_99"` block is added.
2. Dataset `research_log.md` lines 5–32 (the PR #259 `still_open` entry) preserved byte-for-byte (no content edit; only line-offset shift). A new `closure_status: closed` entry sits ABOVE it.
3. `CHANGELOG.md [3.82.1]` block exists with header `## [3.82.1] — 2026-05-29 (PR #N: chore/sc2egset-02-01-03-formal-closure)` (where N is the assigned PR number, swept from `<TBD>`).
4. `pyproject.toml` records `version = "3.82.1"`.
5. `planning/INDEX.md` Archive table contains a PR #259 row at SHA `5a62fc76`; the new chore branch is on the Active plan line.
6. Repo HEAD diff size = exactly 5 files (no more, no less).
7. `PIPELINE_SECTION_STATUS.yaml` + `PHASE_STATUS.yaml` + `ROADMAP.md` + every audit artifact under `reports/artifacts/02_01_03/` + the Parquet at `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_features.parquet` are byte-identical to their master `5a62fc76` state.
8. `git log master..HEAD --stat` shows exactly 2 commits (closure content commit + chore release-bump commit per `.claude/rules/git-workflow.md` L29).
9. The PR #245 evidence tokens validated by `_check_dataset_research_log_evidence_present` (lines 1178–1212) remain present in the dataset research_log (the still_open entry retains them; the new closure entry need not duplicate them).

## Open Questions

- **OQ1 — 02_01_99 STEP_STATUS row: DO_NOT_ADD.** Binding rationale: ROADMAP §"Step 02_01_99" L2627–L2650 declares it as ROADMAP-only stub. Its `outputs.data_artifacts` lists `02_01_99_omit_closure_decision.csv` and `.md` as "(planned, NOT created in this PR)" (L2721, L2723). Its `gate.artifact_check` (L2762–L2776): "NOT APPLICABLE TO THIS ROADMAP-STUB PR. The artifact_check fires only after the future omit-closure artifact PR materializes the CSV + MD decision pair." That follow-up artifact PR was PR #255, which produced `02_01_99_rating_omit_closure.{csv,md}` and added NO STEP_STATUS row (planning/INDEX.md L14: "NO STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS flip"). The Q-chain decision-artifact PRs #242, #243, #245, #247, #249, #251 likewise add no STEP_STATUS rows. 02_01_99 is structurally identical: a decision-artifact sub-step of 02_01_03's adjudication chain, not an independent materialization step. Adding a `02_01_99` row would invent a closure semantics no precedent supports. The STEP_STATUS header rule "derived from ROADMAP" means rows track materialization-bearing steps, not lineage stubs. 02_01_99 continues to live in ROADMAP as a documented declaration; STEP_STATUS does not mirror every ROADMAP block. **Reviewer-adversarial concurred (HIGH confidence).**

- **OQ2 — CHANGELOG.md [3.82.1] header date 2026-05-29.** Convention is closure-PR merge date (mirroring PR #237 L35 header date 2026-05-24 = PR #237 merge date), distinct from `completed_at = "2026-05-28"` (audit-evidence date). The plan resolves this in T03 + T04.

- **OQ3 — CHANGELOG PR number placeholder.** Per repo housekeeping convention, open PR, then sweep `PR #<TBD>` → `PR #N` in a follow-up housekeeping commit before merge (mirrors the `f0a3f551` chore commit "normalize PR #<TBD> placeholders to PR #260"). The placeholder sweep is part of the future closure execution PR's git history but does not change the 5-file diff envelope.

- **OQ4 — Was PIPELINE_SECTION_STATUS `02_01: complete` strictly correct after PR #259?** Reviewer-adversarial nit. At master `5a62fc76`, PIPELINE_SECTION_STATUS `02_01: complete` exists despite STEP_STATUS having no `02_01_03` row. Either (a) PIPELINE_SECTION_STATUS pre-anticipated the 02_01_03 row addition (matching the PR #230 path where section-row flipped before 02_01_01 step-row had a `complete` row), or (b) the derivation invariant was effectively violated at master `5a62fc76`. This planning PR treats the future closure's 02_01_03 row addition as RESTORING the invariant; it does NOT propose to edit PIPELINE_SECTION_STATUS in the closure PR. A future maintainer may wish to revisit derivation semantics in a separate governance review; this plan does NOT pre-decide that question.

- **OQ5 — 02_01_99 future closure path.** If a future maintainer decides 02_01_99 should be closed independently (rather than living in 02_01_03's lineage), it would require its own separate Layer-1 + Layer-2 plan pair. This plan does NOT pre-decide that question.

---

### Sources verified on master `5a62fc76`

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` (header L1–L11; 02_01_02 block L200–L204)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` (`02_01: complete` L54)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` (Phase 02 `in_progress` / Phase 03 `not_started` L22–L23)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (§02_01_03 L2274–L2618; §02_01_99 L2622–L2849)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (PR #259 entry L5–L32; PR #237 closure header L35; PR #229/#230 closure pattern L171+)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.json` (`verdict=PASS`, `features_audited_count=24`, `row_count=44418`, `distinct_focal_match_count=22209`, `audit_date="2026-05-28"`)
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_rating_reconstruction.py` (`_check_dataset_research_log_evidence_present` L1178–L1212; presence-only validation)
- `.claude/rules/git-workflow.md` (L25 "patch for fix/test/chore"; L29 two-commit pattern)
- `.claude/scientific-invariants.md`
- `.claude/ml-protocol.md`
- `.claude/rules/data-analysis-lineage.md`
- `docs/PHASES.md`
- `docs/TAXONOMY.md`
- `planning/INDEX.md` (PR #260 chore archive row L10; PR #255 archive L14)
- `CHANGELOG.md` (top order [Unreleased] → [3.82.0] → [3.81.1] → [3.81.0])
- PR #237 STEP_STATUS row via `git show a16d78c2` (`completed_at: "2026-05-23"` precedent — evidence-date, NOT merge-date)
