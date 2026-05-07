---
category: A
branch: phase02/sc2egset-feature-registry-scaffold
branch_note: "Non-canonical prefix (project precedent from PRs #209-#211, phase02/ rather than feat/). Substantive category remains A/feat; minor version bump applies."
base_ref: master
base_commit: 6e220ad989ce715bb1f016ac6f76252c346c7a86
date: 2026-05-07
dataset: sc2egset
phase: "02"
pipeline_section: "02_01"
step: "02_01_01"
step_name: "Feature-family registry skeleton (sc2egset)"
pr_title: "feat(phase02): SC2EGSet 02_01_01 notebook scaffold + validation module"
version_current: "3.47.0"
version_target: "3.48.0"
version_bump_type: "minor (Category A feat)"
invariants_touched: [I3, I5, I6, I7, I8, I9]
reviewer_gate: "reviewer-deep"
reviewer_adversarial: "only if reviewer-deep raises methodology BLOCKER"
critique_required: false
lineage_sequence_step: 2
---

# Plan: SC2EGSet Step 02_01_01 — Feature-family registry scaffold (notebook scaffold + one validation module)

## Status

PR #211 is already merged at master commit `6e220ad989ce715bb1f016ac6f76252c346c7a86`
(version 3.47.0). That PR delivered the ROADMAP stub for Step 02_01_01 (lineage sequence
step 1). This plan starts from master at version 3.47.0. Do NOT re-merge PR #211.

The current branch `phase02/sc2egset-feature-registry-scaffold` does not yet exist; it is
created from master at the start of implementation.

Active dataset step registry: Step 02_01_01 is **not present** — no entry exists for
this step. The last recorded step is `01_06_04` (completed 2026-04-19). Step 02_01_01
status is therefore not started. Adding an entry to the step registry and updating
associated status files is deferred to a subsequent artifacts/log/status/manifest PR.

---

## Scope

This PR implements lineage sequence step 2 only ("Notebook scaffold + one validation
module") per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical
work."

**Delivered in this PR:**
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` (jupytext .py:percent source)
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb` (paired .ipynb)
- One validation module at: `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`

**Explicitly NOT in this PR (deferred):**
- No generated CSV/MD registry artifact
- No STEP_STATUS.yaml edit (deferred)
- No PIPELINE_SECTION_STATUS.yaml edit (deferred)
- No PHASE_STATUS.yaml edit (deferred)
- No research_log.md entry — per-dataset or cross-dataset (deferred)
- No notebook_regeneration_manifest.md entry (deferred)
- No thesis evidence files
- No aoestats or aoe2companion edits
- No raw data edits
- No model training or encoder fitting
- Step 02_01_01 completion status: NOT complete after this PR. Completion requires a
  subsequent "artifacts/log/status/manifest" PR after reviewed execution of all
  validation modules.

---

## Problem Statement

PR #211 (merged at master commit `6e220ad989ce715bb1f016ac6f76252c346c7a86`, version
3.47.0) added the ROADMAP stub for SC2EGSet Step 02_01_01. Per
`.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical work", the
ROADMAP stub is sequence step 1; this PR is sequence step 2 ("Notebook scaffold + one
validation module"). Sequence step 2 is the only step performed in this PR — steps 3–9
are forbidden here by the same rule.

The validation module verifies six structural constraints on the planned 26-row registry
skeleton (22 model-input candidates + 1 sanity-gate row + 3 explicitly blocked rows),
as V-1 through V-6 assertions via `validate_registry_skeleton()`. If any assertion fails
the notebook execution halts. All six assertions must PASS for the gate to be cleared.
No registry artifact is produced even if all six PASS — artifact generation is deferred
to a future PR.

---

## Assumptions & Unknowns

- **A1 (Step numbering and notebook path).** Step `02_01_01` lives under Pipeline
  Section `02_01` (Pre-Game vs In-Game Boundary) per `docs/PHASES.md` §Phase 02. The
  canonical sandbox path is
  `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
  paired with the `.ipynb` form. Both files are committed.

- **A2 (Notebook scope — scaffold + one validation module only).** Per
  `.claude/rules/data-analysis-lineage.md` §"Notebook discipline": "The first notebook
  pass should be a scaffold plus one validation module only. Do not use the first pass
  to generate all final artifacts." The notebook implements frontmatter, imports, paths,
  hypothesis/falsifier, tracker CSV read, skeleton declaration, validation module call,
  and conclusion. No DuckDB connection opened.

- **A3 (Registry skeleton row count and composition — 26 rows total).** The skeleton
  lists exactly 26 rows derived as follows:

  **5 `pre_game` rows** (CROSS-02-02-v1.0.1 §6.1, treating focal_race/opponent_race as
  ONE row):
  1. `sc2egset.pre_game.focal_race_with_opponent_race_pair`
  2. `sc2egset.pre_game.map_type_encoded`
  3. `sc2egset.pre_game.patch_version_encoded`
  4. `sc2egset.pre_game.matchup_encoded`
  5. `sc2egset.pre_game.is_mmr_missing_flag`

  **6 `history_enriched_pre_game` rows** (CROSS-02-02-v1.0.1 §6.2):
  1. `sc2egset.history_enriched_pre_game.focal_player_history`
  2. `sc2egset.history_enriched_pre_game.opponent_player_history`
  3. `sc2egset.history_enriched_pre_game.matchup_history_aggregate`
  4. `sc2egset.history_enriched_pre_game.reconstructed_rating`
  5. `sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling` — CONTEXT
     flag; does not hard-code a retention percentage; `status = allowed_with_caveat`
  6. `sc2egset.history_enriched_pre_game.in_game_history_aggregate`

  **4 `in_game_snapshot` model-input rows** (tracker CSV `eligible_for_phase02_now`
  excluding `slot_identity_consistency`): `count_units_built_by_cutoff_loop`,
  `count_units_killed_by_cutoff_loop`, `morph_count_by_cutoff_loop`,
  `building_construction_count_by_cutoff_loop`.

  **7 `in_game_snapshot` allowed_with_caveat rows** (tracker CSV `eligible_with_caveat`):
  `minerals_collection_rate_history_mean`, `army_value_at_5min_snapshot`,
  `supply_used_at_cutoff_snapshot`, `food_used_max_history`,
  `time_to_first_expansion_loop`, `count_units_lost_by_cutoff_loop`,
  `count_upgrades_by_cutoff_loop`.

  **1 sanity_gate row**: `sc2egset.in_game_snapshot.slot_identity_consistency`
  — `status = sanity_gate_not_model_input`.

  **3 blocked rows**: `mind_control_event_count`, `army_centroid_at_cutoff_snapshot`,
  `playerstats_cumulative_economy_fields` — `status = blocked_until_additional_validation`.

  Total: 5 + 6 + 4 + 7 + 1 + 3 = 26 rows.

- **A4 (Tracker CSV is the authoritative SC2 in_game_snapshot eligibility source).**
  The notebook reads `tracker_events_feature_eligibility.csv` and filters by
  `status_in_game_snapshot` column. Eligible: `{eligible_for_phase02_now,
  eligible_with_caveat}` (12 rows). Blocked: `{blocked_until_additional_validation}`
  (3 rows). Total: 15 rows.

- **A5 (Temporal cutoff rules — strict `<` for history; `<=` for in-game snapshot).**
  Per CROSS-02-00-v3.0.1 §3.3 and `.claude/scientific-invariants.md` §I3:
  `history_time < target_time` (strict inequality) for every history-derived family;
  `event.loop <= cutoff_loop` for every in_game_snapshot family. Tracker-derived
  families never declare `prediction_setting = pre_game` or
  `history_enriched_pre_game` (Amendment 2 of PR #208; Invariant I3). V-6 and V-5
  enforce these rules.

- **A6 (Cold-start declared as gate categories only — no magic numbers).** Per
  Invariant I7 and CROSS-02-02-v1.0.1 §9, every cold-start handling field on every
  model-input row is one of `G-CS-1` through `G-CS-6` — no numeric pseudocount,
  threshold, smoothing strength, or imputation constant is declared.

- **A7 (Validation module is a separate Python source file, not inline notebook
  asserts).** `validate_registry_skeleton.py` lives at
  `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py` and
  exposes one function `validate_registry_skeleton(skeleton, tracker_csv_path)`. The
  notebook calls it; results are printed by the notebook cell.

- **A8 (Reviewer-deep is the gate; reviewer-adversarial only on BLOCKER).**
  `critique_required: false` is set in frontmatter intentionally per
  data-analysis-lineage.md exception for Phase 02 readiness work.

- **A9 (Version bump 3.47.0 → 3.48.0).** Per `.claude/rules/git-workflow.md`
  §"PR Creation Flow" step 2, minor bump for feat.

- **A10 (OQ1 resolved): `feature_family_id` uses dataset-prefixed form
  `sc2egset.<prediction_setting>.<family>`.**

- **A11 (OQ2 resolved): `cross_region_fragmentation_handling` declared under
  `history_enriched_pre_game` (CROSS-02-02-v1.0.1 §6.2 placement).**

- **A12 (OQ3 resolved): Notebook frontmatter `Commit` field populated with short hash
  at scaffold creation time. Does NOT auto-update on re-runs.**

### Open Unknowns

None. All open questions (OQ1–OQ3) are resolved in Assumptions above.

---

## Literature Context

- **Kuhn & Johnson (2019), *Feature Engineering and Selection*, Ch. 2** — declare
  feature source, grain, and prediction-time admissibility before computing. V-1 and
  V-2 verify this declaration is present and correctly structured.
- **Lopez de Prado (2018), *Advances in Financial Machine Learning*, Ch. 3** — strict
  temporal cutoffs (`history_time < target_time`). V-6 enforces this for
  `history_enriched_pre_game` families.
- **CROSS-02-02-v1.0.1 §9 (cold-start gate vocabulary)** — gate-only cold-start
  treatment; no magic numbers per Invariant I7.

---

## Commit Granularity

Three commits, in order:

1. **Planning commit** (already done at HEAD `cba28e30`): `planning/current_plan.md`
   only — `docs(planning): plan sc2egset feature registry scaffold`

2. **Scaffold commit**: notebook pair (`.py` + `.ipynb`) + validation module
   (`validate_registry_skeleton.py`) only. Commit message:
   `feat(phase02): add SC2EGSet 02_01_01 notebook scaffold + validate_registry_skeleton`

3. **Release commit**: `pyproject.toml` (3.47.0 → 3.48.0) + `CHANGELOG.md`
   ([Unreleased] → [3.48.0]) only. Commit message:
   `chore(release): bump version to 3.48.0`

Do not combine scaffold and release commits. Do not add version bump to scaffold commit.
Do not add generated artifacts to any commit.

---

## Execution Steps

### T01 — Create sandbox directory tree

- `mkdir -p sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary`
- No files inside; no `.gitkeep`
- Executor: Sonnet

---

### T02 — Author validation module: validate_registry_skeleton.py

- Path: `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`
- Purpose: standalone Python module with one function
  `validate_registry_skeleton(skeleton: list[dict], tracker_csv_path) -> None` that runs
  V-1 through V-6 assertions and raises `AssertionError` with a descriptive message on
  failure.
- No pandas required; skeleton is `list[dict]`
- Module reads `tracker_events_feature_eligibility.csv` path as a parameter (passed in
  by the notebook)
- No file I/O other than reading the CSV
- No `print()` calls inside the module itself; notebook cells call the function and print
  results
- Must have a module-level docstring per CROSS-02-03-v1.0.1 audit protocol binding
- Executor: **Opus required** (tracker semantics, slot_identity_consistency
  classification, cold-start gate logic)

---

### T03 — Author .py:percent notebook scaffold

- Path: `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
- Cell layout per `docs/templates/notebook_template.yaml`:

  **Cell 1 (markdown): frontmatter**
  - Phase 02, Pipeline Section 02_01, Step 02_01_01
  - Question from ROADMAP Step 02_01_01 `question` field (verbatim): "Which Phase 02
    candidate feature families exist for sc2egset, declared per CROSS-02-02-v1.0.1 §6,
    and what is each family's CROSS-02-03-v1.0.1 D1–D15 design-time disposition
    (allowed / allowed_with_caveat / blocked_until_validation /
    sanity_gate_not_model_input)?"
  - Invariants I3/I5/I6/I7/I8/I9
  - Commit = short hash at scaffold creation HEAD (does NOT auto-update on reruns)

  **Cell 2 (code): imports**
  - `logging`, `csv`, `pathlib.Path`
  - `from rts_predict.common.notebook_utils import get_reports_dir, setup_notebook_logging`
  - `from rts_predict.games.sc2.datasets.sc2egset.validate_registry_skeleton import validate_registry_skeleton`
  - `logger = setup_notebook_logging()`

  **Cell 3 (code): paths**
  - Define `TRACKER_CSV` path via
    `get_reports_dir("sc2", "sc2egset") / "artifacts" / "01_exploration" / "03_profiling" / "tracker_events_feature_eligibility.csv"`
  - Do NOT call `ARTIFACTS_DIR.mkdir()` — no artifact dir created
  - Log paths

  **Cell 4 (markdown): Hypothesis / Falsifier / Stop-condition declaration block**
  - Per `.claude/rules/data-analysis-lineage.md` §"Required structure for every
    empirical analysis": assumption being tested, measurement claim, sanity check,
    falsifier, expected artifact or report, lineage source, downstream decision

  **Cell 5 (code): Read tracker CSV**
  - Read tracker CSV into list of dicts
  - Print counts by `status_in_game_snapshot`

  **Cell 6 (markdown): Registry skeleton declaration narrative**
  - 26 rows breakdown: 5 pre_game + 6 history_enriched_pre_game + 4 in_game_snapshot
    eligible_now model-inputs + 7 eligible_with_caveat + 1 sanity_gate + 3 blocked

  **Cell 7 (code): Define SKELETON**
  - Define `SKELETON: list[dict]` as literal list of 26 dicts
  - `feature_family_id` format = `sc2egset.<prediction_setting>.<family>`
  - Each dict has exactly: `feature_family_id`, `dataset_tag`, `prediction_setting`,
    `source_table_or_event_family`, `source_grain`, `model_input_grain`, `target_grain`,
    `temporal_anchor`, `allowed_cutoff_rule`, `candidate_leakage_modes`,
    `cold_start_handling`, `status`, `per_player_construction`
  - Print `len(SKELETON)`

  **Cell 8 (markdown): Validation module intro**
  - States which §3 schema fields V-1..V-6 cover and which are deferred

  **Cell 9 (code): Call validate_registry_skeleton**
  - Call `validate_registry_skeleton(SKELETON, tracker_csv_path=TRACKER_CSV)`
  - If no exception, print "validate_registry_skeleton: ALL PASS (V-1 through V-6)"

  **Cell 10 (markdown): Conclusion**
  - Explicitly state: "No report artifacts produced in this scaffold PR; planned future
    CSV/MD artifacts are deferred to a subsequent artifacts PR after reviewed execution
    of all validation modules."

- Constraints:
  - No `def`/`class`/`lambda` in cells
  - Every code cell ≤ 50 lines
  - No feature values materialized
  - No file writes

- Executor: **Opus required**

---

### T04 — Sync paired .ipynb

- `jupytext --sync sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
- Verify both `.py` and `.ipynb` exist
- Executor: Sonnet

---

### T05 — Execute notebook; halt on AssertionError

- `jupyter nbconvert --to notebook --execute --inplace ...ipynb --ExecutePreprocessor.timeout=300`
- If any `AssertionError` raised: **HALT. Do not fix. Report failing V-N and offending
  row(s) to parent session.**
- On success: verify cell outputs contain "ALL PASS (V-1 through V-6)"
- Re-sync pair after execution
- Verify `git status` shows only notebook pair + validation module (no artifacts under
  `reports/`)
- Executor: Sonnet; halt protocol strict

---

### T06 — Run repo-standard checks

- `ruff check` on the validation module and notebook `.py`
- `jupytext --check` on the notebook `.py`
- `pytest tests/ -v --cov --cov-report=term-missing | tee coverage.txt` — read and
  verify ≥ 95% coverage; if coverage drops below 95%, add tests for the validation
  module before proceeding. Test file path if needed:
  `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`
- Delete `coverage.txt` after verification
- Executor: Sonnet

---

### T07 — Scaffold commit

- Stage only: notebook `.py`, notebook `.ipynb`, validation module `.py`
- If coverage check in T06 required new tests, include the test file in this commit too
- Write commit message to `.github/tmp/commit.txt` (never heredoc — breaks in zsh).
  Content:

```
feat(phase02): add SC2EGSet 02_01_01 notebook scaffold + validate_registry_skeleton

Implements lineage sequence step 2 (scaffold + one validation module) for
SC2EGSet Step 02_01_01 (Feature-family registry skeleton).

- 26-row in-memory registry skeleton: 5 pre_game + 6 history_enriched_pre_game
  + 4 in_game_snapshot eligible_now + 7 eligible_with_caveat + 1 sanity_gate
  + 3 blocked.
- validate_registry_skeleton V-1..V-6: schema integrity, tracker split counts,
  blocked families, slot_identity_consistency gate, tracker-never-pre-game,
  history strict-< with sc2egset details_timeUTC provenance.
- No CSV/MD artifacts, no STEP_STATUS/PHASE_STATUS edits, no research_log entry,
  no manifest update — all deferred to subsequent PR after reviewed execution.

Binds: CROSS-02-00-v3.0.1, CROSS-02-01-v1.0.1, CROSS-02-02-v1.0.1, CROSS-02-03-v1.0.1.
```

- `git commit -F .github/tmp/commit.txt`
- Verify `git log -1 --name-only` contains only the scaffold files (+ any test file if
  needed)
- Executor: Sonnet

---

### T08 — Release commit

- Edit `pyproject.toml`: `version = "3.47.0"` → `version = "3.48.0"` (single source;
  no `__init__.py`)
- Edit `CHANGELOG.md`:
  - Roll `[Unreleased]` → `[3.48.0] — 2026-05-07 (PR #N: phase02/sc2egset-feature-registry-scaffold)`
    where N = actual PR number at wrap-up time
  - Insert new empty `[Unreleased]` block at top with Added/Changed/Fixed/Removed
    sub-headers
  - Populate `[3.48.0]` Added section with one bullet summarising notebook scaffold
    + V-1..V-6
- Stage only `pyproject.toml` and `CHANGELOG.md`
- Write commit message to `.github/tmp/commit.txt`:

```
chore(release): bump version to 3.48.0

Roll [Unreleased] into [3.48.0] for phase02/sc2egset-feature-registry-scaffold.
```

- `git commit -F .github/tmp/commit.txt`
- Verify `git log -1 --name-only` shows only `pyproject.toml` and `CHANGELOG.md`
- Executor: Sonnet

---

### T09 — Push, draft PR, PR-number substitution, reviewer-deep gate

- `git push -u origin phase02/sc2egset-feature-registry-scaffold`
- Write PR body to `.github/tmp/pr.txt` per `.github/pull_request_template.md`
- `gh pr create --draft --title "feat(phase02): SC2EGSet 02_01_01 notebook scaffold + validation module" --body-file .github/tmp/pr.txt --base master`
- Capture PR number N; substitute `PR #N` in `CHANGELOG.md` [3.48.0] heading; commit
  substitution as `chore(release): substitute PR number in CHANGELOG [3.48.0]`; push
- Dispatch `@reviewer-deep` with PR URL and `base_ref = master`
- If reviewer-deep PASS → `gh pr ready <N>` then clean up `.github/tmp/`
- If reviewer-deep BLOCKER methodology → parent session dispatches
  `@reviewer-adversarial`
- Executor: Sonnet for mechanics; reviewer-deep for gate

---

## Validation Module Specification

### validate_registry_skeleton(skeleton, tracker_csv_path) — V-1 through V-6

The function signature is:
`def validate_registry_skeleton(skeleton: list[dict], tracker_csv_path) -> None`

Raises `AssertionError` with a descriptive message on any failure.

**V-1 — Schema integrity**
- Assert skeleton has exactly the 13 required columns (no missing, no extra):
  `feature_family_id`, `dataset_tag`, `prediction_setting`,
  `source_table_or_event_family`, `source_grain`, `model_input_grain`, `target_grain`,
  `temporal_anchor`, `allowed_cutoff_rule`, `candidate_leakage_modes`,
  `cold_start_handling`, `status`, `per_player_construction`
- Assert `prediction_setting` ∈
  `{pre_game, history_enriched_pre_game, in_game_snapshot, blocked_or_deferred}`
  for every row
- Assert `status` ∈ `{allowed, allowed_with_caveat, sanity_gate_not_model_input,
  blocked_until_additional_validation}` for every row
- Assert `feature_family_id` is non-null, non-empty, unique across all rows
- Assert every `feature_family_id` starts with `sc2egset.` (dataset-prefixed per OQ1)
- Assert no row has a materialized feature-value column (column count == 13 exactly)

**V-2 — Tracker eligibility split counts**
- Read tracker CSV, count rows by `status_in_game_snapshot` column
- Assert exactly: `eligible_for_phase02_now` = 5, `eligible_with_caveat` = 7,
  `blocked_until_additional_validation` = 3 (total = 15)
- Raise with descriptive message if any count differs

**V-3 — Blocked tracker families remain blocked**
- Assert that in the skeleton, the families `mind_control_event_count`,
  `army_centroid_at_cutoff_snapshot`, and `playerstats_cumulative_economy_fields`
  all have `status = blocked_until_additional_validation`
- Assert none of them have `prediction_setting` ∈
  `{pre_game, history_enriched_pre_game, in_game_snapshot}` with a model-input status

**V-4 — slot_identity_consistency registry classification**
- Assert the skeleton row for `slot_identity_consistency` has
  `status = sanity_gate_not_model_input`
- Assert this is a registry-level classification (add docstring explaining: "The
  upstream tracker CSV marks slot_identity_consistency as eligible_for_phase02_now;
  the registry reclassifies it as sanity_gate_not_model_input based on the CSV
  notes_for_phase02 field and PR #208 Phase 02 guidance. This is a
  registry-introduced classification, not a modification of the CSV.")
- Assert the CSV row for `slot_identity_consistency` still reads
  `status_in_game_snapshot = eligible_for_phase02_now` (i.e., the CSV is not modified)

**V-5 — Zero tracker-derived rows in pre_game or history_enriched_pre_game**
- Define TRACKER_EVENT_FAMILIES from the tracker CSV (all rows, regardless of status)
- Assert no skeleton row whose `source_table_or_event_family` is a tracker event family
  has `prediction_setting ∈ {pre_game, history_enriched_pre_game}`
- Raise naming the violating row(s) if any

**V-6 — History rows use strict < and sc2egset details_timeUTC provenance**
- For every row with `prediction_setting = history_enriched_pre_game`:
  - Assert `allowed_cutoff_rule` contains `<` and does NOT contain `<=` (strict
    inequality only)
  - Assert `temporal_anchor` is `details_timeUTC` (the sc2egset-specific provenance
    anchor, not the cross-dataset alias `started_at`)
  - Assert `allowed_cutoff_rule` does NOT include the current match's final state or
    any post-outcome value
- Raise with the specific row and offending field on any failure

---

## Open Questions

None. All open questions (OQ1–OQ3) are resolved in Assumptions above:

- **OQ1 (resolved)**: `feature_family_id` = `sc2egset.<prediction_setting>.<family>`.
  Do NOT encode status in the ID.
- **OQ2 (resolved)**: `cross_region_fragmentation_handling` stays under
  `history_enriched_pre_game` as a CONTEXT / sensitivity-gate handling row. It must
  not hard-code a retention percentage or be treated as a regular model-input.
- **OQ3 (resolved)**: Notebook frontmatter `Commit` field = short hash at scaffold
  creation HEAD. Does NOT auto-update on re-runs.

---

## File Manifest

| Commit | Files |
|--------|-------|
| Planning (done) | `planning/current_plan.md` |
| Scaffold | `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`, `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb`, `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py` |
| Release | `pyproject.toml`, `CHANGELOG.md` |
| PR-number substitution | `CHANGELOG.md` |

---

## Gate Condition

All must hold for merge:

1. Notebook executed; cell outputs show "ALL PASS (V-1 through V-6)"
2. No CSV/MD artifacts under `reports/artifacts/02_feature_engineering/` in any commit
3. No STEP_STATUS.yaml / PIPELINE_SECTION_STATUS.yaml / PHASE_STATUS.yaml edits
   (all deferred)
4. No research_log.md edits (deferred)
5. No notebook_regeneration_manifest.md edits (deferred)
6. Scaffold commit contains only notebook pair + validation module (+ any needed test
   file)
7. Release commit contains only `pyproject.toml` + `CHANGELOG.md`
8. `pyproject.toml` version = 3.48.0; CHANGELOG `[3.48.0]` has actual PR number
   (not `#N`)
9. `ruff check` clean; `jupytext --check` clean; `pytest` ≥ 95% coverage
10. Final reviewer-deep PASS. Reviewer-adversarial only if reviewer-deep raises
    unresolved methodology BLOCKER.

---

## Reviewer Gate

- **Primary gate**: `@reviewer-deep` (Opus) at T09 after PR is created
- **Reviewer-adversarial**: invoked ONLY if reviewer-deep raises an unresolved
  methodology BLOCKER
- Do not invoke reviewer-adversarial upfront or by default
- No `planning/current_plan.critique.md` required before execution (per
  data-analysis-lineage.md exception for Phase 02 readiness work)

---

## Deferral List

Explicitly NOT in this PR:

- Registry CSV artifact at
  `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`
- Registry MD artifact
- Additional validation modules (D2, D3, D6, D8, D9, D10, D11, D12, D15)
- STEP_STATUS.yaml row for `02_01_01` (deferred)
- PIPELINE_SECTION_STATUS.yaml row for `02_01` (deferred)
- PHASE_STATUS.yaml `phases."02".status` update (deferred)
- Per-dataset research_log.md entry (deferred)
- `thesis/pass2_evidence/notebook_regeneration_manifest.md` row (deferred)
- aoestats Step 02_01_01 scaffold
- aoe2companion Step 02_01_01 scaffold
- Step 02_01_01 completion (requires a subsequent artifacts/log/status/manifest PR)
- Any thesis chapter prose

---

## Forbidden Files

Executor must HALT if `git status` lists any of:

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/**`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
- `reports/research_log.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
- `reports/specs/02_0*.md`
- `src/rts_predict/games/aoe2/**`
- `thesis/**`
- `.claude/**`
- `docs/**`
- `data/**`
