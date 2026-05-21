---
title: "SC2EGSet Phase-02 Step 02_01_01 — PM-1 §10 verdict-audit evidence persistence (does NOT close 02_01_01)"
category: A
branch: feat/sc2egset-02-01-01-section10-audit-persistence
base_ref: 5c7ef380d181276bc2f7d4c14b4427e336af781e
date: 2026-05-21
version_bump: "3.63.0 → 3.64.0"
planner_model: user-directed (planner-science revision after reviewer-adversarial APPROVE-WITH-CONDITIONS, reviewer-adversarial bounded check APPROVE-WITH-NITS)
dataset: sc2egset
phase: "02"
pipeline_section: "02_01"
invariants_touched: [I3, I6, I7, I9, I10]
source_artifacts:
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/specs/02_03_temporal_feature_audit_protocol.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/specs/02_01_leakage_audit_protocol.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
  - src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py
  - sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.py
critique_required: true
critique_file: planning/current_plan.critique.md
research_log_ref: src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
---

# Plan: SC2EGSet Step 02_01_01 — PM-1 §10 verdict-audit evidence persistence

## Scope

This plan covers persistence of the PR #228 PM-1 §10 verdict-audit result as
on-disk evidence (a 23-column CSV and a companion MD), plus a single per-dataset
`research_log.md` entry, plus the planning/release-tail conformance updates.
**This PR persists evidence but does NOT close Step `02_01_01`.** The validator,
the validator tests, the registry CSV/MD, the status YAMLs, the ROADMAP, the
INVARIANTS, the locked specs, and the root `reports/research_log.md` are all
FROZEN. No feature column is materialized.

Step closure is deliberately deferred to a separate later PR with explicit
`STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` flips
and a fresh reviewer-adversarial methodology gate.

## Problem Statement

PR #228 (merged at master `5c7ef380`) introduced
`validate_registry_section10_verdicts(...)` and its tests, and executed the
PM-1 §10 verdict audit inside the jupytext-paired notebook at
`sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.py`.
The audit passed in memory (`passed=True`, `rows_audited=26`,
`halting_falsifier=None`, 0/0/0 drift counts, `materialized_column_count=0`),
but the result was NOT persisted to disk. Per
`.claude/rules/data-analysis-lineage.md` "Artifact discipline", an in-memory
validator pass is not citable evidence until it is recorded on disk through
canonical lineage; the artifact must derive from the same upstream notebook
that produced the in-memory result, and the on-disk encoding must be byte-
equivalent to a re-run of the validator against the same frozen inputs.

This PR closes the lineage loop for the PM-1 increment by persisting the
audit as a CSV+MD artifact pair and appending a single per-dataset
`research_log.md` entry. It does NOT advance Step `02_01_01` toward closure
in the status-derivation chain.

## Assumptions & unknowns

- **Assumption (A-1):** The PR #228 validator code (`validate_registry_section10_verdicts.py`)
  and its tests are FROZEN by this PR. Any drift halts via `PERSIST` falsifier.
- **Assumption (A-2):** The registry CSV (26 rows, 14 columns, includes `block`)
  and the tracker eligibility CSV are FROZEN by this PR. Hashes captured in the
  persisted artifact will detect post-merge drift.
- **Assumption (A-3):** `materialized_column_count = 0` holds at the
  catalog-only registry layer; clause-2 of the ROADMAP `continue_predicate`
  is vacuously satisfied for this audit only (see §5 of the artifact MD).
- **Assumption (A-4):** The deterministic timestamp convention
  (`audit_executed_at_utc_date` = UTC `YYYY-MM-DD`; `git_sha` separate) is
  sufficient for reproducibility per Invariant I6.
- **Unknown:** None remain. All scientific decisions are inherited from the
  PR #228 reviewer-adversarial Round-1/Round-2 baseline.

## Literature context

Not applicable. This is a design-time evidence-persistence increment over a
locked internal specification (CROSS-02-03-v1.0.1 §10) and a frozen registry
artifact. No external literature is required to justify persistence; the
methodology was already approved in PR #228.

## Execution Steps

### T01 — Parent: materialize approved plan and critique to GitHub (THIS PR)

**Objective:** Make the approved chat plan and the conditions-satisfied
critique inspectable in GitHub before any artifact-writing executor runs.

**Instructions:**
1. From master HEAD `5c7ef380`, create branch
   `feat/sc2egset-02-01-01-section10-audit-persistence`.
2. Write this file (`planning/current_plan.md`).
3. Write `planning/current_plan.critique.md` with the latest
   APPROVE-WITH-NITS verdict, all 10 condition results, 5 nits, and the
   materialization-prerequisite-resolved addendum.
4. Commit only the two planning files
   (`chore(plan): materialize PM-1 evidence-persistence plan for review`).
5. Push and open a **draft** PR; do NOT request review or merge.

**Verification:**
- `git diff --name-only master..HEAD` lists exactly two files:
  `planning/current_plan.md`, `planning/current_plan.critique.md`.
- `gh pr view <N> --json isDraft` returns `{"isDraft": true}`.

**File scope:**
- `planning/current_plan.md`
- `planning/current_plan.critique.md`

**Read scope:**
- All §Repo evidence anchors below (READ ONLY).

---

### T02 — Executor (later turn): add notebook artifact-write cell + banner update

**Objective:** Add exactly ONE artifact-write cell to the existing PR #228
notebook and update ONE banner markdown cell to reflect that the §10 verdict
audit is now persisted on disk while Step `02_01_01` remains open.

**Instructions:**
1. Open the jupytext source at
   `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.py`.
2. Add ONE new cell at the end (after the existing gate-assertions cell,
   before the closure-statement cell). The cell must use plain top-level
   statements only (no `def` / `class` / `lambda`). Order of operations
   inside the cell:
   a. Derive deterministic values: `audit_executed_at_utc_date` via
      `datetime.now(UTC).strftime("%Y-%m-%d")`; `git_sha` via
      `subprocess.run(["git", "rev-parse", "HEAD"], …)`; three SHA-256
      digests over raw file bytes (`validate_registry_section10_verdicts.py`,
      `02_01_01_feature_family_registry.csv`, `tracker_events_feature_eligibility.csv`).
   b. Build the 26-row DataFrame in the stable 23-column order (see §Artifact
      CSV schema).
   c. Write CSV via
      `df.to_csv(path, index=False, encoding="utf-8", lineterminator="\n")`.
   d. Run the PERSIST byte-equivalence check (see §Persistence byte-equivalence
      check). HALT on failure.
   e. Render MD per §Artifact MD structure and write via
      `Path(path).write_text(content, encoding="utf-8")`.
   f. `print(...)` a closure summary listing both artifact paths and
      `PERSIST PASS: persisted CSV byte-equivalent on reload modulo {audit_executed_at_utc_date, git_sha}`.
3. Update the front-matter banner markdown cell: replace the existing line
   `NO artifact written` with two lines:
   `artifact persisted in evidence-persistence PR — 02_01_01_section10_verdict_audit.{csv,md}`
   and
   `Step 02_01_01 STILL OPEN; status YAMLs intentionally NOT flipped`.
4. Run `jupytext --sync 02_01_01_registry_section10_verdict_audit.py` to
   refresh the paired `.ipynb`.

**Verification:**
- Notebook diff is EXACTLY 1 added cell + 1 banner markdown edit.
  `git diff --stat sandbox/.../02_01_01_registry_section10_verdict_audit.py`
  must show only the cells touched.
- Both artifact files exist at the declared paths and contain 26 data rows
  (CSV) and the 8 required MD sections.
- PERSIST byte-equivalence check passes.

**File scope:**
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.py`
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.ipynb`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py` (READ ONLY, FROZEN)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv` (READ ONLY, FROZEN)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv` (READ ONLY, FROZEN)

---

### T03 — Executor (later turn): write the two artifact files

**Objective:** Persist the 23-column CSV and 8-section MD to the declared
artifact paths through the notebook (NOT through any side-channel script).

**Instructions:**
- The artifact files are produced by re-executing the notebook from T02.
  No separate script is added.
- The CSV must satisfy all determinism rules (§Artifact CSV schema).
- The MD must include §1 non-closure disclaimer at the top, §2 provenance,
  §3 aggregate result, §4 falsifier roll-call (F-1, F-1a, F-1b, F-2, F-3,
  F-4, F-5, F-6, F-7, PERSIST — each "did not fire"), §5 ROADMAP
  `continue_predicate` verbatim + three-clause table, §6 methodology lineage,
  §7 per-row compact table, §8 cited code/SQL block.

**Verification:**
- `wc -l <csv>` reports 27 lines (header + 26 data rows).
- `grep -c '^| ' <md>` shows the per-row table has 26+ data rows.
- `grep "audit_pr.*PR #229" <csv>` matches (literal, no placeholder).
- `grep -c "did not fire" <md>` ≥ 10 (one per falsifier roll-call row).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.md`

**Read scope:**
- All T02 outputs (the updated notebook).

---

### T04 — Executor (later turn): append per-dataset research_log.md entry

**Objective:** Append a single per-dataset `research_log.md` entry that
records the persistence increment and uses the two distinct non-closure
tokens.

**Instructions:**
1. Open
   `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`.
2. Insert ONE new entry above the existing 2026-05-16 PR #216 entry
   (reverse-chronological). The entry must include:
   - Header: ISO date `YYYY-MM-DD`, `[Phase 02 / Step 02_01_01]`,
     title `"Persist PM-1 §10 verdict-audit evidence (Step 02_01_01 still open)"`.
   - Category: A.
   - Dataset: sc2egset.
   - Branch `feat/sc2egset-02-01-01-section10-audit-persistence` + PR number `PR #229` (draft PR already exists; written directly, no post-open substitution).
   - `closure_status: still_open`
   - `evidence_persistence_state: section10_verdict_audit_persisted_step_open`
   - What: PR #228 validated PM-1 in memory; this PR persists the evidence
     to disk.
   - Why: data-analysis-lineage rule — in-memory passes are not citable
     evidence.
   - How: notebook path, validator path, two input CSV paths, three SHA-256
     hashes, deterministic UTC date, `git_sha`.
   - Findings: 0 drifts, 0 hits, halting_falsifier=None, PERSIST did not fire.
   - What this means: clause-3 satisfied on disk; clause-2 vacuous (see
     verbatim wording in §Research log update plan below); clause-1 from
     PR #216; Step `02_01_01` remains OPEN; the §10 audit increment did NOT
     advance overall closure; status YAMLs deliberately frozen.
   - Decisions taken: persist at catalog-only layer; deterministic
     `audit_executed_at_utc_date` (not runtime timestamp); freeze status YAMLs,
     ROADMAP, INVARIANTS, registry, validator, validator tests; explicitly
     do NOT reuse PR #216's `closure_status: partial` token (rationale:
     PR #216's `partial` denoted "validators V-1..V-9 are partial coverage
     toward closure"; this entry denotes "no closure progress claim at all"
     and the two epistemic states must not collide).
   - Decisions deferred: status-chain triad mutation; ROADMAP amendment;
     `02_01_02` start; Phase 03 work; reviewer-deep closure-decision audit.
   - Thesis mapping: Chapter 4 §4.5 — citable as secondary lineage row only.
   - Open questions / follow-ups: schedule formal closure PR (separate
     planner-science → reviewer-adversarial → executor cycle); decide
     whether `02_01_02` planning may begin before/after closure PR
     (deferred to a later read-only planning session).
   - Acknowledged trade-offs: evidence persistence inflates the artifact
     directory with a CSV mirroring the validator's in-memory output;
     justified by lineage discipline.

**Verification:**
- `git diff src/.../sc2egset/reports/research_log.md | grep -E "(^\+)" | wc -l` shows the new entry was added.
- `grep -c "closure_status: still_open" src/.../sc2egset/reports/research_log.md` ≥ 1.
- `grep -c "evidence_persistence_state: section10_verdict_audit_persisted_step_open" src/.../sc2egset/reports/research_log.md` ≥ 1.
- Root `reports/research_log.md` diff is empty (`git diff reports/research_log.md` returns nothing).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`

**Read scope:**
- All T02 and T03 outputs.

---

### T05 — Executor (later turn): release-tail (CHANGELOG + pyproject + planning/INDEX.md)

**Objective:** Apply the conventional `feat/` minor-version bump and update
the planning index.

**Instructions:**
1. `pyproject.toml`: `version = "3.63.0"` → `version = "3.64.0"`.
2. `CHANGELOG.md`: move the (currently empty) `[Unreleased]` block contents
   into a new versioned section
   `## [3.64.0] — YYYY-MM-DD (PR #229: feat/sc2egset-02-01-01-section10-audit-persistence)`
   immediately above `## [3.63.0]`. Re-emit empty `[Unreleased]` with the
   four standard sub-headers `### Added`, `### Changed`, `### Fixed`, `### Removed`.
   Inside `[3.64.0]`:
   - `### Added`: new artifact CSV; new artifact MD; new per-dataset
     `research_log.md` entry.
   - `### Changed`: notebook pair (`.py` + `.ipynb`) — one artifact-write
     cell + one banner edit; `planning/INDEX.md` archive #228 + set new
     Active.
   - `### Notes`: include the **verbatim non-closure disclaimer** ("This PR
     persists evidence but does NOT close Step `02_01_01`."); include the
     **verbatim clause-2 wording** ("No materialized-column audit is
     applicable at the catalog-only registry layer (materialized_column_count=0);
     this becomes non-vacuous once Step 02_01_02 materializes the first
     feature column per 02_01_leakage_audit_protocol.md §4 lines 117–121.");
     include the frozen-files list (validator, tests, registry CSV/MD,
     status YAMLs, ROADMAP, INVARIANTS, root research_log).
3. `planning/INDEX.md`: archive PR #228 with
   `#228 (merged 2026-05-21 at master 5c7ef380)` and set Active to
   `feat/sc2egset-02-01-01-section10-audit-persistence (YYYY-MM-DD) — Category A: SC2EGSet Phase-02 Step 02_01_01 PM-1 §10 verdict-audit evidence persistence; persist CSV+MD + per-dataset research_log entry; status YAMLs / ROADMAP / INVARIANTS / registry / validator / tests / root research_log frozen; Step 02_01_01 NOT closed`.
4. Commit boundary: single `feat(sc2egset): …` commit (preferred) OR
   `feat(...)` + `chore(release): bump version to 3.64.0` (per PR #228
   precedent at `996ed0af`). No `--amend`. No force-push.

**Verification:**
- `grep '"3.64.0"' pyproject.toml` matches.
- `grep "^## \[3.64.0\]" CHANGELOG.md` matches.
- `grep "^- feat/sc2egset-02-01-01-section10-audit-persistence" planning/INDEX.md` matches.
- `grep "^| feat/sc2egset-02-01-01-section10-verdict-audit" planning/INDEX.md` matches in the Archive table with PR #228.

**File scope:**
- `pyproject.toml`
- `CHANGELOG.md`
- `planning/INDEX.md`

**Read scope:**
- All T02–T04 outputs.

---

### T06 — Executor (later turn): update existing draft PR #229 body and mark ready when complete

**Objective:** Update the body of the existing draft PR #229 with the final
T02..T05 execution summary and validation report; mark the PR ready for
review only after the diff and validation are complete. Do NOT open a new PR.

Context: Draft PR #229 (open, mergeable) already exists on branch
`feat/sc2egset-02-01-01-section10-audit-persistence`. The PR number is
known before any artifact is written, so `audit_pr` is the literal
`PR #229` everywhere — no placeholder, no post-open substitution.

**Instructions:**
1. Write the updated PR body to `.github/tmp/pr.txt` per
   `.claude/rules/git-workflow.md`. The body must cover: this
   planning-correction commit; the T02..T05 execution diff (notebook
   cell + 2 artifacts + per-dataset research_log + release tail);
   the validation report (PERSIST PASS line, pytest + coverage
   result, 10-file diff manifest from `git diff --name-only master..HEAD`).
2. Run `gh pr edit 229 --body-file .github/tmp/pr.txt`.
3. Delete `.github/tmp/pr.txt`.
4. Run `source .venv/bin/activate && poetry run pytest tests/ -v --cov --cov-report=term-missing | tee coverage.txt` and verify pass + coverage ≥ 95%; delete `coverage.txt` after verifying.
5. Mark PR #229 ready for review ONLY after the execution diff is complete,
   the validation report is attached to the body, and reviewer-deep is
   queued or has passed: `gh pr ready 229` (or via the GitHub UI).

**Verification:**
- `gh pr view 229 --json isDraft,state,headRefName` returns the expected
  state (`isDraft=true` until step 5 completes; `state=OPEN` throughout;
  `headRefName=feat/sc2egset-02-01-01-section10-audit-persistence`).
- `ls .github/tmp/pr.txt` returns "no such file" after step 3.
- No `gh pr create` is invoked anywhere in T06.

**File scope:**
- `.github/tmp/pr.txt` (transient, deleted in step 3)

**Read scope:**
- All T02–T05 outputs.

## File Manifest

This Manifest covers the FULL approved increment (T01..T06). T01 (THIS PR)
modifies ONLY the two planning files. T02..T06 are executed in a later
turn on the same branch.

| File | Action | Phase |
|------|--------|-------|
| `planning/current_plan.md` | Rewrite | T01 (this PR) |
| `planning/current_plan.critique.md` | Rewrite | T01 (this PR) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.py` | Update | T02 (later) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.ipynb` | Update | T02 (later) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv` | Create | T03 (later) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.md` | Create | T03 (later) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` | Update | T04 (later) |
| `planning/INDEX.md` | Update | T05 (later) |
| `CHANGELOG.md` | Update | T05 (later) |
| `pyproject.toml` | Update | T05 (later) |

Total expected diff: **10 files**.

## Gate Condition

For T01 (THIS DRAFT PR) only:
- `git diff --name-only master..HEAD` lists exactly two files
  (`planning/current_plan.md`, `planning/current_plan.critique.md`).
- The draft PR is open and is NOT requested for review or merge.

For the FULL increment (T01..T06, evaluated by reviewer-deep at PR ready-state):
- `git diff --name-only master..HEAD` lists exactly the 10 files above.
- `git diff --name-only master..HEAD -- <forbidden>` is empty for every
  path in the forbidden list.
- The notebook diff contains exactly 1 added cell + 1 banner markdown edit.
- The persisted CSV has exactly 26 data rows; the feature-family ID set is
  identical to the frozen registry's 26-ID set.
- The PERSIST byte-equivalence check passes ("PERSIST PASS: persisted CSV
  byte-equivalent on reload modulo {audit_executed_at_utc_date, git_sha}").
- `pytest tests/ -v --cov` passes with coverage ≥ 95%.
- The artifact MD has §1 non-closure disclaimer at the top and the
  falsifier roll-call lists F-1, F-1a, F-1b, F-2, F-3, F-4, F-5, F-6, F-7,
  PERSIST each marked "did not fire".
- No prose anywhere in the PR claims Step `02_01_01` is closed, Phase 02
  is active or complete, or `02_01_02` is authorized to start.

## Out of scope

- Step `02_01_01` closure (status-chain triad flip + ROADMAP entry +
  reviewer-adversarial closure audit) — deferred to a separate later PR.
- Any `02_01_02` work (registry-row materialization audit, post-materialization
  audit gate re-run, feature-column production).
- Phase 03 work (splitting, baselines, features, models).
- Bibliography / appendix / thesis-chapter work.
- Validator and validator-test modification (frozen by PR #228; PERSIST
  falsifier guards against drift).
- Root `reports/research_log.md` modification (per-dataset only, per
  `.claude/ml-protocol.md`).
- AoE2 codepath modification.
- Any DuckDB / Parquet / materialized feature output.

## Open questions

- None remain for T01 (this draft PR).
- Operational: at what point does the closure PR get scheduled?
  Resolved by: separate later planner-science → reviewer-adversarial cycle,
  after at least one user-approved sleep on this draft PR's content.

---

# §1 Boundary and non-closure disclaimer (load-bearing)

**This PR persists evidence but does NOT close Step `02_01_01`.**

The PR does NOT claim:
- Step `02_01_01` is closed.
- **Phase 02 activation.**
- **Step `02_01_02` authorization.**
- **Phase 03 start.**
- Feature matrix existence.
- Model readiness.

Closure of Step `02_01_01` requires an independent later increment that:
1. Flips `STEP_STATUS.yaml: 02_01_01 → complete`.
2. Satisfies the ROADMAP `continue_predicate` three-clause gate in writing.
3. Lands a separate closure PR with a fresh reviewer-adversarial methodology
   approval.

The §10 audit increment evidenced by this PR is necessary but not sufficient
for closure.

The PR explicitly does NOT update: `STEP_STATUS.yaml`,
`PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`, `ROADMAP.md`,
`INVARIANTS.md`, the registry CSV, the registry MD, the validator module,
the validator tests, the root `reports/research_log.md`, the locked specs,
AoE2 paths, `tests/**`, `thesis/**`, `data/**`, `notebooks/**`,
`.github/workflows/**`, `Makefile`, or `scripts/**`.

# §2 Repo evidence (anchors)

- Validator (FROZEN): `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py`
  (merged in PR #228 → master `5c7ef380`).
- Validator tests (FROZEN): `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_section10_verdicts.py`.
- Audit notebook scaffold: `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.{py,ipynb}`.
- Registry CSV (FROZEN, 26 rows, 14 columns including `block`):
  `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv`.
- Registry MD (FROZEN):
  `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md`.
- Tracker eligibility CSV (FROZEN):
  `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv`.
- ROADMAP `continue_predicate` (verbatim, lines 2060–2066): "A future PR may
  begin Step 02_01_02 (or the next 02_01 step in the ROADMAP) only after
  this Step 02_01_01 has reached its CSV + MD artifact-check at a future PR,
  the CROSS-02-01-v1.0.1 post-materialization audit gate has been re-run
  for any feature column the registry triggers materialization of, and a
  per-family CROSS-02-03-v1.0.1 §10 verdict is recorded for every registry
  row."
- Status YAMLs (FROZEN; Phase 02 = `not_started`).
- Locked specs (FROZEN, cited):
  `src/rts_predict/games/sc2/datasets/sc2egset/reports/specs/02_03_temporal_feature_audit_protocol.md` (CROSS-02-03-v1.0.1 §10);
  `src/rts_predict/games/sc2/datasets/sc2egset/reports/specs/02_01_leakage_audit_protocol.md` (§4 lines 117–121, Materialization definition).
- Prior PR #216 partial-token precedent (NOT reused):
  `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
  first entry uses `closure_status: partial` — this PR deliberately uses
  distinct tokens (see §Research log update plan).
- Release-tail state: `pyproject.toml` `version = "3.63.0"`; `CHANGELOG.md`
  `[Unreleased]` empty; `planning/INDEX.md` Active still points to PR #228
  (to be archived in T05).

# §3 Why this is not batching

Per `.claude/rules/data-analysis-lineage.md` "Non-batching rule":
- Validator was reviewed, written, tested, and merged in PR #228
  (steps 1–6 of the empirical sequence).
- The §10 audit was executed in the merged notebook with all assertions
  passing (step 7 in-memory).
- THIS PR completes step 7 (artifact write) and step 8 (per-dataset
  `research_log.md` entry) of the same sequence for the same PM-1 increment.
- Step 9 (reviewer-deep) is the final gate after PR open (per §Reviewer
  routing).
- No `02_01_02`, no Phase 03, no thesis, no closure work is initiated.

This is the smallest atomic persistence unit that preserves canonical
notebook → artifact lineage.

# §4 Forbidden files and actions (load-bearing)

Zero diff allowed on:

```
reports/research_log.md  # root CROSS log
src/rts_predict/games/aoe2/**
src/rts_predict/games/sc2/datasets/sc2egset/data/**
tests/**
src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py
src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml
src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml
src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/specs/**
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md
thesis/**
data/**
notebooks/**
.github/workflows/**
Makefile
scripts/**
```

Forbidden actions:
- Mutating the validator or its tests.
- Flipping any status YAML (`STEP_STATUS`, `PIPELINE_SECTION_STATUS`, `PHASE_STATUS`).
- Amending `ROADMAP.md`, `INVARIANTS.md`, or any locked spec under `reports/specs/`.
- Writing the root `reports/research_log.md`.
- Emitting DuckDB / Parquet / materialized feature outputs.
- Adding any new test.
- Writing more than one notebook cell + one banner markdown edit.
- Claiming closure / Phase 02 activation / `02_01_02` authorization
  **anywhere in prose** (artifact MD, research_log, CHANGELOG, PR body, commit
  messages).
- Using `git commit --amend`, `git push --force`, `--no-verify`, or
  `--no-gpg-sign`.

# §5 Artifact CSV schema (load-bearing)

File path:
`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv`

**23 columns**, **26 data rows**, in this stable order:

1. `feature_family_id`
2. `dataset_tag`
3. `prediction_setting`
4. `registry_recorded_status`
5. `derived_section10_verdict`
6. `equality_token`
7. `stricter_drift_flag`
8. `looser_drift_flag`
9. `independent_trigger_hits` (pipe-separated)
10. `triggers_fired` (pipe-separated)
11. `rule_path`
12. `materialized_column_count` (always `0`)
13. `halting_falsifier` (empty string if `None`)
14. `audit_executed_at_utc_date` (`YYYY-MM-DD`)
15. `validator_module` (repo-relative path)
16. `validator_module_sha256`
17. `source_pr` (literal `PR #228`)
18. `audit_pr` (literal `PR #229` — draft PR exists before artifact generation; no placeholder, no substitution)
19. `registry_csv_sha256`
20. `tracker_csv_sha256`
21. `spec_revision_cross_02_03` (literal `CROSS-02-03-v1.0.1`)
22. `git_sha` (40-character)
23. `block` (mirrors the registry CSV `block` column for joinability)

Determinism rules:
- 26 data rows.
- Row order is identical to the frozen registry row order.
- UTF-8 encoding.
- `lineterminator="\n"`.
- `index=False`.
- Reload uses `pd.read_csv(..., dtype=str, keep_default_na=False)`.
- Empty strings for absent values — never `null`, never `nan`.
- SHA-256 hashes computed over raw on-disk file bytes (no normalization).
- `audit_executed_at_utc_date` computed via `datetime.now(UTC).strftime("%Y-%m-%d")` — date only, never `HH:MM:SS`.
- `git_sha` is a separate column from `audit_executed_at_utc_date`.

# §6 Audit-PR lifecycle (load-bearing — addresses nit 3)

Draft PR #229 (branch `feat/sc2egset-02-01-01-section10-audit-persistence`)
is already open when this plan is materialized. Because the PR exists
BEFORE any artifact is written:

- `audit_pr` is the literal string `PR #229` everywhere it appears
  (artifact CSV row, artifact MD §2 provenance block, per-dataset
  `research_log.md` entry, `CHANGELOG.md` `[3.64.0]` section header).
- No placeholder token (`PR #<TBD>` or equivalent) is ever written to disk.
- No post-`gh pr create` substitution pass is required.
- No amend-commit pass is required (the artifact CSV/MD is written once,
  with the final PR number already in place).

The PR body is updated in T06 via `gh pr edit 229 --body-file ...` after
T02..T05 execution. PR #229 remains DRAFT after this planning-correction
commit and through T02..T05; it is marked ready for review only after the
execution diff and validation report are complete (see T06 and §13
Reviewer routing).

# §7 Artifact MD structure (load-bearing)

File path:
`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.md`

Sections (in order):

- **§1 Non-closure disclaimer (TOP).** Verbatim: "This artifact persists
  evidence but does NOT close Step `02_01_01`. Closure requires a separate
  later increment that flips `STEP_STATUS.yaml`, satisfies the ROADMAP
  `continue_predicate` three-clause gate in writing, and lands a separate
  closure PR. Phase 02 is `not_started` per `PHASE_STATUS.yaml` and is not
  advanced by this PR."
- **§2 Provenance.** `audit_executed_at_utc_date` (YYYY-MM-DD), `git_sha`,
  `validator_module` + `validator_module_sha256`, `registry_csv_sha256`,
  `tracker_csv_sha256`, `spec_revision_cross_02_03` (=`CROSS-02-03-v1.0.1`),
  `source_pr = PR #228`, `audit_pr = PR #229` (literal, per §6 — no placeholder).
  One bullet per field, repo-relative paths.
- **§3 Aggregate result.** `passed=True`, `rows_audited=26`,
  `halting_falsifier=None`, `len(stricter_drifts)=0`, `len(looser_drifts)=0`,
  `len(independent_trigger_hits)=0`, `materialized_column_count=0`.
- **§4 Falsifier roll-call table.** One row per falsifier, each marked
  "did not fire":
  - F-1 (overall bidirectional EQUALITY).
  - F-1a (stricter drift).
  - F-1b (looser drift).
  - F-2 (independent §10.2 trigger on allowed/caveat row).
  - F-3 (post-game token in `allowed_cutoff_rule`).
  - F-4 (invalid cutoff operator on history row).
  - F-5 (D13 tracker contradiction).
  - F-6 (slot-identity gate misuse).
  - F-7 (controlled-vocab drift).
  - PERSIST (persistence byte-equivalence).
- **§5 ROADMAP `continue_predicate` verbatim + three-clause analysis.**
  Print the ROADMAP `continue_predicate` block verbatim (from `ROADMAP.md`
  lines 2060–2066). Then a three-row table:
  - **Clause 1** ("Step 02_01_01 has reached its CSV + MD artifact-check at
    a future PR") — SATISFIED for the registry CSV/MD by PR #216
    (provisional artifact); the new PM-1 evidence artifact is incremental
    and does NOT itself satisfy clause 1.
  - **Clause 2** ("CROSS-02-01-v1.0.1 post-materialization audit gate has
    been re-run for any feature column the registry triggers
    materialization of") — VACUOUSLY SATISFIED at the catalog-only registry
    layer. **Verbatim wording (REQUIRED, do NOT paraphrase):**

    > No materialized-column audit is applicable at the catalog-only registry layer (materialized_column_count=0); this becomes non-vacuous once Step 02_01_02 materializes the first feature column per 02_01_leakage_audit_protocol.md §4 lines 117–121.

  - **Clause 3** ("per-family CROSS-02-03-v1.0.1 §10 verdict is recorded
    for every registry row") — SATISFIED in memory by PR #228 + PERSISTED
    ON DISK by THIS PR for all 26 rows.
  - **Closure status remains OPEN** — clause-1 is satisfied; clause-3 is
    satisfied as of this PR; the three-clause gate is now positioned to be
    closed only by a later explicit closure PR with status-YAML flips.
- **§6 Methodology lineage.**
  - Spec source: `02_03_temporal_feature_audit_protocol.md` §10
    (CROSS-02-03-v1.0.1, LOCKED 2026-05-06);
    `02_01_leakage_audit_protocol.md` §4 lines 117–121 (Materialization).
  - Validator: `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py` (frozen by PR #228).
  - Notebook: `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.py`
    (artifact-write cell added in this PR).
  - Tests: `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_section10_verdicts.py` (frozen by PR #228; the PERSIST byte-equivalence check substitutes for re-run inside this PR).
- **§7 Per-row compact table.** 26 rows with columns
  `feature_family_id`, `prediction_setting`, `registry_recorded_status`,
  `derived_section10_verdict`, `equality_token`, `block`. (Full 23-column
  data lives in the CSV; this MD is the human-readable summary.)
- **§8 Cited code/SQL block.** Include the verbatim signature of
  `validate_registry_section10_verdicts(registry_csv_path: Path, tracker_csv_path: Path) -> RegistryVerdictAuditResult`
  and the exact notebook call site (5–10 lines). Reference the validator
  file path + line range (Invariant I6).

The MD must NOT include: closure claims, Phase 02 activation claims,
`02_01_02` next-step claims, ROADMAP edit proposals, status-YAML proposals.

# §8 Notebook update plan (load-bearing)

Constraints:
- Add **EXACTLY ONE** new cell (artifact-write cell).
- Update **EXACTLY ONE** banner markdown cell (front-matter "NO artifact
  written" → two-line replacement, see T02).
- All other cells unchanged. Jupytext-paired `.ipynb` mirror synced.
- All logic in plain top-level statements: **no inline `def`, `class`, or
  `lambda`**. (The frozen validator already lives in `src/`; no new helper
  module is added.)
- The artifact-write cell uses `pandas.DataFrame.to_csv` for the CSV and
  `Path.write_text` for the MD, both with explicit UTF-8 encoding and
  `lineterminator="\n"` for byte determinism.
- The cell writes BOTH artifacts atomically: derive deterministic values →
  build DataFrame → write CSV → reload + rerun validator (PERSIST check) →
  write MD → print closure summary.

No DuckDB connection is opened. No Parquet file is written. No path outside
`reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`
is touched.

Banner change (front-matter cell):
- DELETE the line containing `NO artifact written`.
- ADD two replacement lines:
  - `artifact persisted in evidence-persistence PR — 02_01_01_section10_verdict_audit.{csv,md}`
  - `Step 02_01_01 STILL OPEN; status YAMLs intentionally NOT flipped`

# §9 Research log update plan (load-bearing)

Target: **per-dataset only**, at
`src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`.

Root `reports/research_log.md` is FORBIDDEN (per
`.claude/ml-protocol.md:51-54`).

Required fields in the new reverse-chronological entry (inserted above the
2026-05-16 PR #216 entry):

- ISO date (`YYYY-MM-DD`); Phase 02 / Step 02_01_01 tag; title "Persist PM-1
  §10 verdict-audit evidence (Step 02_01_01 still open)".
- Category: A.
- Dataset: sc2egset.
- Branch: `feat/sc2egset-02-01-01-section10-audit-persistence`.
- PR: `PR #229` (draft PR already exists; written directly, no substitution).
- **`closure_status: still_open`** (deliberately distinct from PR #216's
  `partial`).
- **`evidence_persistence_state: section10_verdict_audit_persisted_step_open`**.
- What: PR #228 validated PM-1 in memory inside the notebook; this PR
  persists the evidence to disk as a 26-row CSV + companion MD + this
  research_log entry.
- Why: `.claude/rules/data-analysis-lineage.md` Artifact discipline — an
  in-memory pass is not citable evidence until recorded on disk through
  canonical lineage.
- How: notebook path; validator path; two input CSV paths
  (registry + tracker); three SHA-256 hashes captured in the artifact;
  deterministic UTC date + `git_sha`.
- Findings: all 26 rows EQUAL modulo synonym; 0 stricter drifts;
  0 looser drifts; 0 independent §10.2 trigger hits; halting_falsifier=None;
  materialized_column_count=0; PERSIST byte-equivalence falsifier did not
  fire.
- What this means: clause-3 of the ROADMAP `continue_predicate` (per-family
  §10 verdict recorded for every registry row) is satisfied on disk;
  clause-1 was satisfied by PR #216;
  **clause-2 wording (REQUIRED VERBATIM, do NOT paraphrase):**

  > No materialized-column audit is applicable at the catalog-only registry layer (materialized_column_count=0); this becomes non-vacuous once Step 02_01_02 materializes the first feature column per 02_01_leakage_audit_protocol.md §4 lines 117–121.

  Step `02_01_01` remains OPEN; the §10 audit increment did NOT advance
  overall step closure; closure requires a separate later PR with explicit
  status-YAML flips and reviewer-adversarial approval.
- **Decisions taken (REQUIRED — explicit non-reuse of PR #216 `partial` token):**
  Persist evidence at the catalog-only layer; use deterministic
  `audit_executed_at_utc_date` (not runtime timestamp); deliberately freeze
  status YAMLs, ROADMAP, INVARIANTS, registry CSV/MD, validator, validator
  tests; **explicitly do NOT reuse PR #216's `closure_status: partial` token.**
  Rationale: PR #216's `partial` denoted "validators V-1..V-9 are partial
  coverage toward closure"; this entry denotes "no closure progress claim
  at all" and the two epistemic states must not collide.
- Decisions deferred: status YAMLs / ROADMAP triad mutation; `02_01_02`
  start; Phase 03 work; reviewer-deep closure-decision audit.
- Thesis mapping: Chapter 4 §4.5 — citable as secondary lineage row only;
  does NOT enable a Phase 02 leakage-clearance claim on its own.
- Open questions / follow-ups: schedule formal Step 02_01_01 closure PR
  (separate planner-science → reviewer-adversarial → executor cycle).
- Acknowledged trade-offs: evidence persistence inflates the artifact
  directory with a CSV that exactly mirrors the validator's in-memory
  output; justified by lineage discipline.

# §10 Persistence byte-equivalence falsifier (PERSIST) (load-bearing)

Inside the notebook artifact-write cell, after the CSV is first written:

1. Reload the just-written CSV with
   `pd.read_csv(..., dtype=str, keep_default_na=False)`.
2. Rerun `validate_registry_section10_verdicts(registry_csv_path, tracker_csv_path)`
   on the same frozen registry + tracker inputs to obtain a fresh
   `RegistryVerdictAuditResult`.
3. Re-encode the fresh result into the same 23-column DataFrame using the
   same code path that produced the CSV (in-cell, deterministic).
4. Compare row-by-row, column-by-column, byte-equivalent modulo ONLY:
   - `audit_executed_at_utc_date` (date can differ across UTC-day boundaries;
     must be identical within a single execution),
   - `git_sha` (allowed to differ pre/post PR open if the audited commit
     differs).

   Note: `audit_pr` is NOT in the allowed-drift set. PR #229 is known
   before artifact generation and is written deterministically as the
   literal `PR #229`; a re-run in the same notebook session must reproduce
   the same string. Any drift in `audit_pr` HALTs PERSIST.
5. If any other column differs, **HALT — PERSIST falsifier fired**;
   do NOT commit the artifact; raise `AssertionError` with a row-level diff
   print.

Success print:
`PERSIST PASS: persisted CSV byte-equivalent on reload modulo {audit_executed_at_utc_date, git_sha}`.

Reload assertions:
- `len(reloaded) == 26`.
- Column set equal to the written columns set.
- Rerun yields `passed=True`, `rows_audited=26`, `halting_falsifier=None`,
  identical `stricter_drifts` / `looser_drifts` / `independent_trigger_hits`
  content.

# §11 Falsifiers (consolidated, all halt-on-detection)

Inherited from PR #228 + PERSIST new in this PR:

- **F-1** (overall bidirectional EQUALITY) — HALT.
- **F-1a** (stricter drift) — HALT.
- **F-1b** (looser drift) — HALT.
- **F-2** (independent §10.2 trigger on allowed/caveat row) — HALT.
- **F-3** (post-game token in `allowed_cutoff_rule`) — HALT.
- **F-4** (invalid cutoff operator on history row) — HALT.
- **F-5** (D13 tracker contradiction) — HALT.
- **F-6** (slot-identity gate misuse) — HALT.
- **F-7** (controlled-vocab drift) — HALT.
- **PERSIST** (persistence byte-equivalence) — HALT (new in this PR).

Structural halt-on-detection conditions (executor MUST verify before commit):

- Validator file diff non-empty.
- Validator tests file diff non-empty.
- Any frozen status YAML / ROADMAP / INVARIANTS / registry CSV / registry
  MD / specs diff non-empty.
- Root `reports/research_log.md` diff non-empty.
- Any AoE2 path diff non-empty.
- Any `tests/**` diff non-empty.
- Any Phase-03 path diff non-empty.
- Any DuckDB / Parquet / materialized feature output produced.
- Notebook diff exceeds 1 added cell + 1 banner markdown edit.
- Artifact MD lacks verbatim `validate_registry_section10_verdicts`
  aggregate-result summary.
- Persisted CSV row count ≠ 26.
- Feature-family ID set in persisted CSV differs from frozen registry's
  26-ID set.
- Any prose anywhere in the PR claims Step `02_01_01` is closed, Phase 02
  is active or complete, or `02_01_02` is authorized.

# §12 Version and release plan (load-bearing)

- `pyproject.toml`: `version = "3.63.0"` → `version = "3.64.0"`.
- `CHANGELOG.md`: move `[Unreleased]` into a new `## [3.64.0] — YYYY-MM-DD
  (PR #229: feat/sc2egset-02-01-01-section10-audit-persistence)` block;
  re-emit `[Unreleased]` empty with the four standard sub-headers (`### Added`,
  `### Changed`, `### Fixed`, `### Removed`).
- `planning/INDEX.md`: archive PR #228 in the Archive table with
  `#228 (merged 2026-05-21 at master 5c7ef380)`; set Active to the new
  persistence branch.

Justification: `feat/` prefix per `.claude/rules/git-workflow.md` ⇒ minor
version bump; Category A evidence-persistence work is more than a chore.

# §13 Reviewer routing and materialization-prerequisite (load-bearing — addresses nit 2)

Explicit, ordered sequence (DO NOT reorder; DO NOT collapse):

- **PR #229 remains DRAFT after this planning-correction commit and
  through T02..T05.** It is marked ready for review (via `gh pr ready 229`
  or the GitHub UI) ONLY after T06 attaches the execution diff and
  validation report to the body, and `@reviewer-deep` is queued or has
  passed.
- **Step A — Planning-only draft PR (THIS PR):** Parent materializes the
  approved chat plan to `planning/current_plan.md` and the approved
  conditions-satisfied critique to `planning/current_plan.critique.md`,
  commits, and opens a **draft** PR on branch
  `feat/sc2egset-02-01-01-section10-audit-persistence`. No execution. No
  artifact files. No notebook diff. No research_log diff. No release tail.
- **Step B — User / ChatGPT reviews the draft planning PR via GitHub
  connector.** This is the materialization prerequisite: the executor
  cannot proceed until the plan is on the branch and the draft PR is
  inspectable.
- **Step C — Approved-execution turn:** After explicit user approval,
  `@executor` (Sonnet, mechanically specified) continues on the SAME
  branch and implements T02..T06 in order. The executor MUST verify the
  PERSIST byte-equivalence check passes before committing the CSV, and
  MUST verify the 10-file diff manifest before opening the PR for ready
  state.
- **Step D — Final gate after PR is ready-for-review:** `@reviewer-deep` —
  mechanical/structural review of the diff against this materialized plan.
  Reviewer-adversarial is NOT required again unless reviewer-deep raises a
  methodology BLOCKER (the methodology was already double-gated for
  PR #228; the remaining risk for this PR is mechanical / structural —
  schema completeness, MD wording, token discipline, forbidden-path zero
  diff, byte-equivalence).

# §14 Risks

- **R-1** Closure scope creep. Mitigation: non-closure language repeated in
  4 loci (artifact MD §1, research_log entry, CHANGELOG `### Notes`, PR
  body); reviewer-deep will reject any prose drift.
- **R-2** Hash determinism drift across machines. Mitigation: SHA-256 over
  raw on-disk bytes (no normalization); PERSIST falsifier validates
  in-cell.
- **R-3** Token collision with PR #216's `closure_status: partial`.
  Mitigation: distinct tokens (`still_open` + `section10_verdict_audit_persisted_step_open`)
  plus explicit prose in the research_log entry naming PR #216.
- **R-4** Notebook diff inflates beyond 1 cell + banner. Mitigation:
  structural halt; executor `git diff --stat sandbox/...` pre-commit.
- **R-5** Release-tail slip (the gap that produced PR #228's
  `chore(release)` follow-up commit `996ed0af`). Mitigation: explicit
  10-file manifest in §File Manifest; reviewer-deep verifies all three
  release-tail files in T05.
- **R-6** Validator-vs-registry semantic drift post-merge. Mitigation:
  `validator_module_sha256`, `registry_csv_sha256`, `tracker_csv_sha256`,
  `spec_revision_cross_02_03` columns let any future audit detect
  staleness without rerunning the validator.
- **R-7** Framing re-litigation in next adversarial review. Mitigation:
  the framing anchors to PR #228's already-approved
  `planning/current_plan.critique.md` Round-1 / Round-2 baseline.

# §15 Open questions / blockers

No blockers remain for the draft planning PR (this PR, T01). Execution
(T02..T06) requires explicit user approval in a later turn.

Operational follow-ups for a later planning cycle:
- Schedule the formal Step 02_01_01 closure PR (separate planner-science →
  reviewer-adversarial → executor cycle).
- Decide whether `02_01_02` planning may begin before or after the formal
  closure PR (deferred to a later read-only planning session).
