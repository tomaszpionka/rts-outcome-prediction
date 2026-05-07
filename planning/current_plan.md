---
category: A
branch: phase02/sc2egset-feature-registry-scaffold
base_ref: master
base_commit: 6e220ad989ce715bb1f016ac6f76252c346c7a86
date: 2026-05-07
planner_model: claude-opus-4-7
dataset: sc2egset
phase: "02"
pipeline_section: "02_01"
phase_step: "02_01_01 — Feature-family registry skeleton (sc2egset) — notebook scaffold + one validation module only"
pr_title: "feat(phase02): SC2EGSet 02_01_01 notebook scaffold + validation module"
version_bump: "3.47.0 → 3.48.0 (minor; Category A feat — per .claude/rules/git-workflow.md §PR Creation Flow step 2)"
invariants_touched: [I3, I5, I6, I7, I8, I9]
source_artifacts:
  - .claude/rules/data-analysis-lineage.md
  - .claude/rules/git-workflow.md
  - .claude/scientific-invariants.md
  - docs/TAXONOMY.md
  - docs/PHASES.md
  - docs/templates/notebook_template.yaml
  - docs/templates/planner_output_contract.md
  - docs/templates/plan_template.md
  - docs/templates/step_template.yaml
  - planning/README.md
  - reports/specs/02_00_feature_input_contract.md
  - reports/specs/02_01_leakage_audit_protocol.md
  - reports/specs/02_02_feature_engineering_plan.md
  - reports/specs/02_03_temporal_feature_audit_protocol.md
  - sandbox/README.md
  - sandbox/jupytext.toml
  - sandbox/notebook_config.toml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv
  - CHANGELOG.md
  - pyproject.toml
critique_required: false
research_log_ref: null
---

# Plan: SC2EGSet Step 02_01_01 — Notebook scaffold + one validation module (first empirical Phase 02 PR)

## Scope

This plan creates the first empirical implementation PR for Phase 02 — Pipeline Section `02_01` (Pre-Game vs In-Game Boundary), Step `02_01_01` (Feature-family registry skeleton — sc2egset). It implements only step 2 of the `.claude/rules/data-analysis-lineage.md` non-batching sequence ("Notebook scaffold + one validation module"). It does not implement steps 3–9: no generated registry artifacts (CSV/MD), no `research_log.md` entry, no `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` edits, no reviewer-adversarial gate, and no continuation to Step `02_01_02`.

The PR delivers exactly one notebook pair (`.py` + `.ipynb`) under `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/`, executes it, captures the cell outputs (six PASS assertions for the validation module), and stops. The version bump and CHANGELOG roll are committed separately.

## Problem Statement

PR #211 (merged at master commit `6e220ad989ce715bb1f016ac6f76252c346c7a86`, version `3.47.0`) added the ROADMAP stub for SC2EGSet Step `02_01_01`. Per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical work", the ROADMAP stub is sequence step 1; this PR is sequence step 2 ("Notebook scaffold + one validation module"). Sequence step 2 is the only subsequent step performed in this PR — steps 3–9 are forbidden here by the same rule.

The validation module verifies six structural constraints on the planned 26-row registry skeleton (22 model-input candidates + 1 sanity-gate row + 3 explicitly blocked rows). The module is encoded as in-notebook `assert` statements; if any assertion fails the notebook execution halts. All six assertions must PASS for the gate to be cleared. No registry artifact is produced even if all six PASS — artifact generation is a future PR.

## Assumptions & unknowns

- **A1 (Step numbering and notebook path).** Step `02_01_01` lives under Pipeline Section `02_01` (Pre-Game vs In-Game Boundary) per `docs/PHASES.md` §Phase 02. The canonical sandbox path per `docs/TAXONOMY.md` §"Sandbox notebooks" and the locked ROADMAP stub is `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` paired with the `.ipynb` form. Both files are committed (sandbox/README.md Hard Rule 4: "Always stage both .ipynb and .py").

- **A2 (Notebook scope — scaffold + one validation module only).** Per `.claude/rules/data-analysis-lineage.md` §"Notebook discipline": "The first notebook pass should be a scaffold plus one validation module only. Do not use the first pass to generate all final artifacts." The notebook implements: frontmatter cell, imports cell, paths cell, in-memory registry skeleton definition cells, one validation module — six assertions V-1 through V-6 — and a Conclusion markdown cell. This is a filesystem/CSV-only notebook (Pattern B per sandbox/README.md); no DuckDB connection is opened. Cell 04 (DuckDB setup) and the cleanup cell are omitted accordingly.

- **A3 (Registry skeleton row count and composition — 26 rows total).** The skeleton lists exactly 26 rows derived as follows:

  **5 `pre_game` rows** (CROSS-02-02-v1.0.1 §6.1, treating each spec line as one registry row):
  1. `sc2egset.pre_game.focal_race_with_opponent_race_pair` — NOTE: CROSS-02-02-v1.0.1 §6.1 lists focal_race and opponent_race as a single feature-family line ("focal_race/opponent_race pair"). V-1 treats this as ONE registry row (not two). The executor must not split it into two rows.
  2. `sc2egset.pre_game.map_type_encoded`
  3. `sc2egset.pre_game.patch_version_encoded`
  4. `sc2egset.pre_game.matchup_encoded`
  5. `sc2egset.pre_game.is_mmr_missing_flag`

  **6 `history_enriched_pre_game` rows** (CROSS-02-02-v1.0.1 §6.2):
  1. `sc2egset.history_enriched_pre_game.focal_player_history`
  2. `sc2egset.history_enriched_pre_game.opponent_player_history`
  3. `sc2egset.history_enriched_pre_game.matchup_history_aggregate`
  4. `sc2egset.history_enriched_pre_game.reconstructed_rating`
  5. `sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling` — CONTEXT flag per CROSS-02-00-v3.0.1 §5.4; `candidate_leakage_modes = ''`; `per_player_construction = 'non_per_player'`
  6. `sc2egset.history_enriched_pre_game.in_game_history_aggregate`

  **4 `in_game_snapshot` model-input rows** (tracker CSV `eligible_for_phase02_now`, excluding slot_identity_consistency):
  From `tracker_events_feature_eligibility.csv` — rows where `status_in_game_snapshot = eligible_for_phase02_now` excluding `slot_identity_consistency`.

  **7 `in_game_snapshot` allowed-with-caveat rows** (tracker CSV `eligible_with_caveat`):
  From tracker CSV — rows where `status_in_game_snapshot = eligible_with_caveat`.

  **1 sanity-gate row**: `sc2egset.in_game_snapshot.slot_identity_consistency` — registry-introduced classification `sanity_gate_not_model_input`. The upstream CSV value remains `eligible_for_phase02_now`; the registry-layer reclassification derives from the CSV `notes_for_phase02` field and PR #208 Phase 02 guidance.

  **3 blocked rows** (tracker CSV `blocked_until_additional_validation`): `mind_control_event_count`, `army_centroid_at_cutoff_snapshot`, `playerstats_cumulative_economy_fields`.

  Total: 5 + 6 + 4 + 7 + 1 + 3 = 26. V-1 asserts this partition explicitly.

- **A4 (Tracker CSV is the authoritative SC2 in_game_snapshot eligibility source).** The notebook reads `tracker_events_feature_eligibility.csv` and filters by `status_in_game_snapshot` column (not `status_pre_game` and not `planned_for_phase02`). Eligible: `{eligible_for_phase02_now, eligible_with_caveat}` (12 rows). Blocked: `{blocked_until_additional_validation}` (3 rows). Total: 15 rows. V-3 checks membership against this column specifically.

- **A5 (Temporal cutoff rules — strict `<` for history; `<=` for in-game snapshot).** Per CROSS-02-00-v3.0.1 §3.3 and `.claude/scientific-invariants.md` §3: `history_time < target_time` (strict inequality) for every history-derived family; `event.loop <= cutoff_loop` for every in_game_snapshot family. Tracker-derived families never declare `prediction_setting = pre_game` or `history_enriched_pre_game` (Amendment 2 of PR #208; Invariant I3). V-2 enforces all three rules.

- **A6 (Cold-start declared as gate categories only — no magic numbers).** Per Invariant I7 and CROSS-02-02-v1.0.1 §9, every cold-start handling field on every model-input row is one of `G-CS-1` through `G-CS-6` — no numeric pseudocount, threshold, smoothing strength, or imputation constant is declared. V-4 enforces this.

- **A7 (Per-player symmetry — focal/opponent construction).** Per Invariant I5, the registry uses a `per_player_construction` field (a registry-introduced label not present verbatim in the spec text, in the same way `sanity_gate_not_model_input` is a registry-introduced classification for `slot_identity_consistency`). Allowed values: `focal_opponent_symmetric` (for per-player families), `non_per_player` (for match-level families such as `map_type_encoded`, `patch_version_encoded`, `matchup_encoded`, `is_mmr_missing_flag`, `cross_region_fragmentation_handling`), `""` (for blocked / sanity-gate rows where symmetry is not applicable). V-5 enforces this.

- **A8 (Dataset tag — sc2egset).** Per Invariant I8, every row carries `dataset_tag = "sc2egset"`. V-6 enforces this.

- **A9 (Notebook is filesystem/CSV-only — no DuckDB).** This is a planning/catalog notebook. It reads `tracker_events_feature_eligibility.csv` and constructs the skeleton from in-notebook literal constants derived from CROSS-02-02-v1.0.1 §6. No DuckDB connection, no SELECT, no file write to `reports/` artifacts paths.

- **A10 (Reviewer-deep is the gate; reviewer-adversarial only on BLOCKER).** Per `.claude/rules/data-analysis-lineage.md` §"Agent and model routing discipline" closing paragraph. `critique_required: false` is set in frontmatter intentionally. This is a deliberate departure from the Category A default and is justified by the data-analysis-lineage.md exception for Phase 02 readiness work.

- **A11 (Version bump 3.47.0 → 3.48.0).** Per `.claude/rules/git-workflow.md` §"PR Creation Flow" step 2, minor bump for feat. `pyproject.toml` 3.47.0 → 3.48.0.

- **A12 (Two-commit topology on the same branch).** Exactly two commits on `phase02/sc2egset-feature-registry-scaffold`: **C1 (T06)** — notebook pair only. **C2 (T07)** — release/changelog only. Split required per Correction 3.

### Resolved questions

- **OQ1 RESOLVED:** `feature_family_id` uses dataset-prefixed form `sc2egset.<prediction_setting>.<family>`. See A3 for the full enumeration.
- **OQ2 RESOLVED:** `cross_region_fragmentation_handling` declared under `history_enriched_pre_game` (CROSS-02-02-v1.0.1 §6.2 placement). `candidate_leakage_modes = ''` (CONTEXT flag per CROSS-02-00-v3.0.1 §5.4).
- **OQ3 RESOLVED:** Notebook frontmatter `Commit` field populated with `6e220ad` at T02 creation time. Does NOT auto-update on re-runs.

## Open Questions

None. All open questions (OQ1–OQ3) are resolved in Assumptions above. No unresolved questions remain at plan-write time.

## Literature context

- **Kuhn & Johnson (2019), *Feature Engineering and Selection*, Ch. 2** — declare feature source, grain, and prediction-time admissibility before computing. V-1 and V-3 verify this declaration is present.
- **Lopez de Prado (2018), *Advances in Financial Machine Learning*, Ch. 3** — strict temporal cutoffs (`history_time < target_time`). V-2 enforces this.
- **CROSS-02-02-v1.0.1 §9 (cold-start gate vocabulary)** — gate-only cold-start treatment. V-4 enforces gate-only encoding.

## Hypothesis / measurement claim / falsifier

- **Assumption being tested.** The 26-row in-memory registry skeleton satisfies six structural invariants drawn from CROSS-02-02-v1.0.1 §6, CROSS-02-00-v3.0.1 §3.3 / §5.4, CROSS-02-03-v1.0.1 §4 D1–D15, and scientific-invariants.md I3 / I5 / I6 / I7 / I8 / I9.
- **Measurement claim.** None. No feature value, encoder fit, model output, or DuckDB row count is measured.
- **Sanity check.** V-1 through V-6 as six independent `assert` statements over the in-memory skeleton.
- **Falsifier.** Any `AssertionError` raised during T04 execution. Halt before progressing to T05–T08.
- **Expected artifact / report.** Notebook execution outputs only (six PASS lines printed to stdout). No CSV/MD artifact written.
- **Lineage source.** CROSS-02-02-v1.0.1 §6; CROSS-02-00-v3.0.1 §3.3; CROSS-02-03-v1.0.1 §4 D1–D15; `tracker_events_feature_eligibility.csv`; scientific-invariants.md I3/I5/I6/I7/I8/I9.
- **Downstream decision.** All six PASS → future PR may proceed to sequence step 6 (next validation module). Any FAIL → halt; reviewer-deep engaged; methodology BLOCKER → reviewer-adversarial.

## Execution Steps

### T01 — Create sandbox directories only

**Objective:** Create empty Phase 02 / Pipeline Section 02_01 sandbox subdirectory tree.

**Instructions:**
1. `mkdir -p sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary`
2. Verify directory exists and is empty.
3. Do not add `.gitkeep`, `__init__.py`, or any other file.

**File scope (writes):** directory only
**Executor:** Sonnet (mechanical mkdir)

---

### T02 — Author `.py:percent` notebook scaffold + one validation module

**Objective:** Create `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` in `.py:percent` jupytext format with 16 cells.

**Cell layout:**
1. (markdown) Frontmatter per notebook_template.yaml — Phase 02, Section 02_01, Step 02_01_01, Question from ROADMAP stub, Invariants I3/I5/I6/I7/I8/I9, Commit = `6e220ad`.
2. (code) Imports: `logging`, `csv`, `re`, `pathlib.Path`, `rts_predict.common.notebook_utils.get_reports_dir, setup_notebook_logging`; `logger = setup_notebook_logging()`. No DuckDB import.
3. (code) Paths cell: define `TRACKER_CSV = get_reports_dir("sc2", "sc2egset") / "artifacts" / "01_exploration" / "03_profiling" / "tracker_events_feature_eligibility.csv"`. Log path. Do NOT call `ARTIFACTS_DIR.mkdir()` — no artifacts dir created.
4. (markdown) Hypothesis / falsifier / stop-condition declaration per data-analysis-lineage.md §"Required structure".
5. (code) Read tracker CSV into list of dicts. Filter by `status_in_game_snapshot` column (not `status_pre_game`, not `planned_for_phase02`) for eligible rows. Enumerate blocked rows. Print counts.
6. (markdown) Skeleton declaration narrative — 26 rows, breakdown.
7. (code) Define `SKELETON: list[dict]` as literal list of 26 dicts per A3 enumeration. Each dict has: `feature_family_id` (dataset-prefixed per OQ1), `dataset_tag = "sc2egset"`, `prediction_setting`, `source_table_or_event_family`, `source_grain`, `model_input_grain`, `target_grain`, `temporal_anchor`, `allowed_cutoff_rule`, `candidate_leakage_modes`, `cold_start_handling` (G-CS-N for model-input; `""` for blocked/sanity-gate), `status`, `per_player_construction` (registry-introduced label: `focal_opponent_symmetric` / `non_per_player` / `""`). Print `len(SKELETON)`.
8. (markdown) Validation module narrative — six checks V-1..V-6; states which §3 fields are covered and which are deferred: "V-1..V-6 cover schema fields {feature_family_id, dataset_tag, prediction_setting, temporal_anchor, allowed_cutoff_rule, cold_start_handling, per_player_construction}; fields {source_table_or_event_family, source_grain, model_input_grain, target_grain, candidate_leakage_modes, status} are deferred to future validation modules per data-analysis-lineage.md sequence step 6."
9. (code) V-1: assert len(SKELETON) == 26, partition counts (22+1+3), feature_family_id uniqueness. Print "V-1 PASS".
10. (code) V-2: assert temporal cutoffs — history strict `<` (not `<=`); in_game_snapshot uses `event.loop <= cutoff_loop`; no tracker-derived row in `{pre_game, history_enriched_pre_game}`. Print "V-2 PASS".
11. (code) V-3: read tracker CSV, build eligible set from `status_in_game_snapshot in {eligible_for_phase02_now, eligible_with_caveat}` (12 rows); build blocked set from `status_in_game_snapshot = blocked_until_additional_validation` (3 rows). Assert bidirectionally: every in_game_snapshot skeleton row's family is in eligible set; every blocked skeleton row's family is in blocked CSV set; and every blocked CSV family is in the blocked skeleton set. Print "V-3 PASS".
12. (code) V-4: assert every model-input row cold_start_handling matches `^G-CS-[1-6]$`; every blocked/sanity-gate row cold_start_handling is `""` or `"N/A"`. Print "V-4 PASS".
13. (code) V-5: assert every row's per_player_construction is in `{focal_opponent_symmetric, non_per_player, ""}`. Print "V-5 PASS".
14. (code) V-6: assert all `dataset_tag == "sc2egset"`. Print "V-6 PASS".
15. (code) Summary print block: six PASS lines + row count + deferral note.
16. (markdown) Conclusion per notebook_template.yaml cell_conclusion: "Artifacts produced: NONE — registry CSV/MD deferred to a future PR. Thesis mapping: Chapter 4 §4.5 Feature engineering plan (sc2egset registry). Follow-ups: next validation module in a future PR."

**Constraints:**
- No `def` / `class` / `lambda` outside `src/rts_predict/`
- Every code cell <= 50 lines
- No DuckDB import or connection
- Frontmatter Commit = `6e220ad`
- SKELETON rows derived from CROSS-02-02-v1.0.1 §6 + tracker CSV verbatim — no invented values

**File scope (writes):**
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`

**Executor:** Opus required (tracker semantics, slot_identity_consistency classification, cold-start gate selection per family, I5 symmetry labeling — all require subtle methodology reasoning per data-analysis-lineage.md §"Agent and model routing discipline")

---

### T03 — Sync paired `.ipynb` via `jupytext --sync`

**Instructions:**
1. `source .venv/bin/activate && poetry run jupytext --sync sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
2. Verify both `.py` and `.ipynb` exist.
3. Run `jupytext --check` on the `.py` to confirm pairing: `poetry run jupytext --check sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`.

**File scope (writes):**
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb`

**Executor:** Sonnet (mechanical)

---

### T04 — Execute notebook in-place; halt on AssertionError

**Instructions:**
1. `source .venv/bin/activate && poetry run jupyter nbconvert --to notebook --execute --inplace sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb --ExecutePreprocessor.timeout=300`
2. If `AssertionError` raised: **HALT. Do not fix the assertion. Report the failing V-N and offending row(s) to the parent session.**
3. On success: verify stdout contains six PASS lines (V-1..V-6).
4. Re-sync pair: `poetry run jupytext --sync sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb`
5. Verify `git status` shows only the two notebook pair files modified — no files under `reports/artifacts/02_feature_engineering/`.

**File scope (writes):**
- Both notebook pair files (outputs populated)

**Executor:** Sonnet. HALT protocol applies strictly.

---

### T05 — Repo-standard checks

**Instructions:**
1. `source .venv/bin/activate && poetry run ruff check sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` — expect 0 issues.
2. `poetry run jupytext --check sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` — expect exit code 0.
3. `poetry run pytest tests/ -v` — sanity check for regressions in existing test tree. This PR adds zero new tests; the validation logic lives in notebook cells per data-analysis-lineage.md sequence step 2. Expect all existing tests to pass.
4. mypy: check `pyproject.toml` to confirm whether sandbox is in mypy scope; if excluded, note that and skip; if included, run `poetry run mypy sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` and expect 0 errors.

**Executor:** Sonnet (mechanical check invocations)

---

### T06 — Implementation checkpoint commit (notebook pair only)

**Instructions:**
1. Confirm branch: `git branch --show-current` = `phase02/sc2egset-feature-registry-scaffold`.
2. Before staging: add one bullet under `[Unreleased] / Added` in `CHANGELOG.md` to describe the notebook scaffold (so T07 does not roll an empty release block). Bullet text: `- SC2EGSet Step 02_01_01 paired notebook scaffold + one validation module (V-1..V-6) for feature-family registry skeleton; no registry CSV/MD artifact generated (deferred).`
3. Stage **only** the two notebook pair files and the CHANGELOG pre-fill:
   - `git add sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
   - `git add sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb`
   - `git add CHANGELOG.md`
4. Verify `git status` — only those three files staged. If `pyproject.toml` appears staged, unstage it.
5. Write commit message to `.github/tmp/commit.txt`:

```
feat(phase02): add SC2EGSet 02_01_01 notebook scaffold + V1-V6 validation module

- Adds sandbox notebook pair for SC2EGSet Step 02_01_01 (Feature-family registry skeleton): scaffold + one validation module per .claude/rules/data-analysis-lineage.md non-batching sequence step 2.
- In-memory 26-row registry skeleton: 5 pre_game + 6 history_enriched_pre_game + 4 in_game_snapshot model-input + 7 in_game_snapshot with-caveat + 1 sanity-gate (slot_identity_consistency) + 3 blocked.
- V-1 row count + partitions; V-2 temporal cutoffs (history strict <, in-game <=, tracker-never-pre-game); V-3 tracker CSV eligibility membership (bidirectional, status_in_game_snapshot column); V-4 cold-start gate-only (G-CS-1..G-CS-6); V-5 per-player symmetry; V-6 dataset_tag.
- No registry CSV/MD artifact produced (sequence step 7 deferred).
- No STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS edits.
- No research_log entries.
- Version bump and CHANGELOG roll committed separately (next commit).
```

6. Commit: `git commit -F .github/tmp/commit.txt`
7. Verify `git log -1 --name-only` shows exactly 3 files: `.py`, `.ipynb`, `CHANGELOG.md`.

**File scope (writes):** notebook pair + CHANGELOG [Unreleased] pre-fill + `.github/tmp/commit.txt`
**Executor:** Sonnet

---

### T07 — Version bump + CHANGELOG roll + draft PR creation

**Instructions:**
1. Edit `pyproject.toml` line 3: `version = "3.47.0"` → `version = "3.48.0"`.
2. Edit `CHANGELOG.md`: roll `[Unreleased]` → `[3.48.0] — 2026-05-07 (PR #N: phase02/sc2egset-feature-registry-scaffold)`; insert a new empty `[Unreleased]` block with empty Added/Changed/Fixed/Removed sub-headers at the top.
3. Stage `pyproject.toml` and `CHANGELOG.md` only. Verify no other files staged.
4. Write commit message to `.github/tmp/commit.txt`:
```
chore(release): bump version to 3.48.0

Roll [Unreleased] into [3.48.0] for PR #N: phase02/sc2egset-feature-registry-scaffold.
```
5. Commit: `git commit -F .github/tmp/commit.txt`
6. Push branch: `git push -u origin phase02/sc2egset-feature-registry-scaffold` (pause for push approval per CLAUDE.md permissions).
7. Write PR body to `.github/tmp/pr.txt` per `.github/pull_request_template.md`. Summary: two commits, 26-row skeleton breakdown, V-1..V-6 PASS condition. Test plan checkboxes:
   - [x] nbconvert execute succeeded; six PASS lines in cell outputs
   - [x] ruff check clean
   - [x] jupytext --check clean
   - [x] pytest tests/ -v all pass
   - [x] T06 commit = notebook pair + CHANGELOG pre-fill only; T07 commit = pyproject.toml + CHANGELOG roll only
   - [x] No artifacts under reports/artifacts/02_feature_engineering/
   - [x] No STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS edits
   - [x] No research_log edits
   - [ ] Replace CHANGELOG PR #N with actual PR number after PR creation
   - [ ] Final reviewer-deep gate
8. Open as draft: `gh pr create --draft --title "feat(phase02): SC2EGSet 02_01_01 notebook scaffold + validation module" --body-file .github/tmp/pr.txt --base master`. Capture PR number N.

**File scope (writes):** `pyproject.toml`, `CHANGELOG.md`, `.github/tmp/commit.txt`, `.github/tmp/pr.txt`
**Executor:** Sonnet (push requires user approval)

---

### T08 — PR-number substitution + push + final reviewer-deep gate + mark ready

**Instructions:**
1. Replace `PR #N:` in `CHANGELOG.md` [3.48.0] heading with the actual PR number captured at T07.
2. Stage `CHANGELOG.md` only. Commit via `.github/tmp/commit.txt`:
```
chore(release): substitute PR number in CHANGELOG [3.48.0] entry

Replaces PR #N placeholder with the actual number from gh pr create at T07.
```
3. Push: `git push origin phase02/sc2egset-feature-registry-scaffold`.
4. Dispatch `@reviewer-deep` with the PR URL and `base_ref = master`.
5. If reviewer-deep PASS → `gh pr ready <pr-number>`.
6. If reviewer-deep raises methodology BLOCKER → parent session dispatches `@reviewer-adversarial`.
7. Clean up: `rm -f .github/tmp/pr.txt .github/tmp/commit.txt`.

**Executor:** Sonnet for substitution commit and cleanup; @reviewer-deep for gate; methodology BLOCKER forwarded to parent session.

---

## File Manifest

### Implementation checkpoint commit (T06)

| File | Action |
|------|--------|
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` | Create |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb` | Create |
| `CHANGELOG.md` | Update ([Unreleased] / Added pre-fill) |

### Release / wrap-up commit (T07)

| File | Action |
|------|--------|
| `pyproject.toml` | Update (3.47.0 → 3.48.0) |
| `CHANGELOG.md` | Update ([Unreleased] rolled to [3.48.0]) |

### PR-number substitution commit (T08)

| File | Action |
|------|--------|
| `CHANGELOG.md` | Update (PR #N → actual number) |

### Ephemeral

| File | Action |
|------|--------|
| `.github/tmp/commit.txt` | Create then delete |
| `.github/tmp/pr.txt` | Create then delete |

---

## Assumptions / falsifiers / sanity checks table

| ID | Assumption | Sanity check | Falsifier | Source |
|----|-----------|--------------|-----------|--------|
| V-1 | Skeleton has exactly 26 rows; partition = 22+1+3; feature_family_id unique | `len(SKELETON)==26`, partition counts, `len({r["feature_family_id"]...})==26` | Any count mismatch | A3; CROSS-02-02 §6; tracker CSV |
| V-2 | History strict `<`; in_game_snapshot `<=`; tracker-never-pre-game | Three asserts per cutoff rule and prediction_setting | Any violation of temporal discipline | A5; CROSS-02-00 §3.3; I3; PR #208 Amendment 2 |
| V-3 | Tracker CSV eligibility membership — bidirectional, against `status_in_game_snapshot` column | Build eligible set and blocked set from CSV; assert skeleton in_game_snapshot rows subset of eligible; assert skeleton blocked rows == CSV blocked set | Any in_game_snapshot row not in CSV eligible; any blocked set mismatch | A4; tracker CSV |
| V-4 | Cold-start gate-only encoding | `^G-CS-[1-6]$` for model-input; `""` or `"N/A"` for blocked/sanity-gate | Any magic number or non-gate value | A6; I7; CROSS-02-02 §9 |
| V-5 | Per-player symmetry | `per_player_construction in {focal_opponent_symmetric, non_per_player, ""}` | Any value outside allowed set | A7; I5 |
| V-6 | dataset_tag = "sc2egset" for all rows | `assert all(r["dataset_tag"]=="sc2egset")` | Any row with wrong or missing tag | A8; I8 |

Note: V-1..V-6 cover schema fields `{feature_family_id, dataset_tag, prediction_setting, temporal_anchor, allowed_cutoff_rule, cold_start_handling, per_player_construction}`. Fields `{source_table_or_event_family, source_grain, model_input_grain, target_grain, candidate_leakage_modes, status}` are deferred to future validation modules per data-analysis-lineage.md sequence step 6.

---

## Execution report requirements

- What was measured: six structural assertions over the in-memory 26-row skeleton. No feature values. No DuckDB queries.
- What was not measured: source_table_or_event_family consistency (D2/D7), grain reconciliation (D3), cold-start numeric values (D11), focal/opponent numeric semantics (D10), per-family SQL window correctness.
- What assumptions remain unvalidated: numeric cold-start parameter values, fixed-point scaling for food/supply tracker rows, lps caveat for 5-min snapshot cutoff.
- Whether result supports downstream: PASS → supports next validation module PR. FAIL → halt.
- Whether halting required: No (all six PASS expected). Any AssertionError is a halt event.

---

## Explicit deferral list

- Sequence step 6 (next validation module) — separate future PR
- Sequence step 7 (registry CSV + MD artifact generation) — separate future PR after all validation modules pass
- Sequence step 8 (research_log.md, STEP_STATUS.yaml, PIPELINE_SECTION_STATUS.yaml, PHASE_STATUS.yaml, manifest update) — separate future PR
- aoestats and aoe2companion Step 02_01_01 scaffolds — parallel-but-independent dataset PRs
- Step 02_01_02 and all subsequent Phase 02 / 03+ steps
- Numeric cold-start values, fixed-point scaling resolution, lps caveat resolution
- Any encoder fit, model train, evaluation, thesis prose

---

## Allowed / Forbidden files

### ALLOWED (writable)
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/` (directory + notebook pair)
- `pyproject.toml` (T07 only — version line)
- `CHANGELOG.md` (T06 pre-fill, T07 roll, T08 substitution)
- `.github/tmp/commit.txt`, `.github/tmp/pr.txt` (ephemeral)

### FORBIDDEN
- Any file under `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
- `reports/research_log.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
- `reports/specs/02_0*` (LOCKED)
- `src/rts_predict/games/aoe2/` (out of scope)
- `tests/` (no new tests)
- `src/rts_predict/` (no source code changes)
- `docs/`, `thesis/`, `.claude/`, `planning/` (no edits mid-execution)
- Any `.duckdb` file
- `data/` (raw data immutable)

---

## Gate Condition

All eight must hold:

1. V-1 through V-6 all PASS in notebook cell outputs.
2. No generated registry CSV/MD artifacts (`git log -p master..HEAD -- src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/` returns empty).
3. No dataset status YAML edits.
4. No `research_log.md` edits.
5. Notebook pair complete and committed.
6. T06 commit contains notebook pair + CHANGELOG pre-fill only; no `pyproject.toml`.
7. T07 commit contains only `pyproject.toml` + `CHANGELOG.md` roll; no notebook files.
8. Final reviewer-deep PASS. Reviewer-adversarial only if reviewer-deep raises unresolved methodology BLOCKER.

---

## Critique-gate instruction

**reviewer-deep is the primary gate for this PR.** reviewer-adversarial is NOT invoked upfront. Per `.claude/rules/data-analysis-lineage.md` §"Agent and model routing discipline" closing paragraph: "For this active Phase 02 readiness PR, do not invoke reviewer-adversarial unless the plan is amended or reviewer-deep raises a BLOCKER requiring adversarial methodology review."

`critique_required: false` is set in frontmatter intentionally — no `planning/current_plan.critique.md` is produced before execution. The reviewer-deep verdict (PASS-WITH-NOTES, 2026-05-07) is recorded in `planning/current_plan.critique.md` as a post-review record only.

After T08 reviewer-deep gate:
- PASS → mark PR ready, proceed to merge.
- Methodology BLOCKER → dispatch `@reviewer-adversarial`; produce `planning/current_plan.critique.md`.
- Non-methodology BLOCKER (lint, taxonomy, file scope) → `@executor` or `@planner-science` addresses per category.

---

## Out of scope

Step 02_01_02 and all subsequent Phase 02/03/04/05/06/07 steps. aoestats and aoe2companion scaffolds. Registry artifact generation. Status YAML updates. research_log entries. Any source-code edit under `src/rts_predict/`. Thesis prose. Spec edits. ROADMAP edits. Any push to remote `origin/master`. Model training. Encoder fits.
