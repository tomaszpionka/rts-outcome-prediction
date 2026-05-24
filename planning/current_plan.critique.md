---
reviewer_role: reviewer-adversarial
reviewer_model: claude-opus-4-7[1m]
reviewer_date: 2026-05-24
plan_base_ref: f378f6f4ac37783e08dfcbe922d0c60b522a272a
plan_branch: feat/sc2egset-02-01-03-history-scaffold
plan_step: "02_01_03 (Layer-1 scaffold + ONE validation module planning)"
plan_category: A
planning_pr: "PR #240"
verdict: APPROVE-WITH-NITS
blockers: 0
nits: 7
---

## Verdict

**APPROVE-WITH-NITS.** The Layer-1 plan describing the Layer-2 scaffold + ONE validation module execution PR for SC2EGSet Step `02_01_03` is methodology-defensible. The non-batching sequence step 2 ("scaffold + ONE validator") is the correct atomic unit for this stage; the PR #232 → PR #233 → PR #234 tranche-1 precedent is mirrored faithfully; the validator's 16-priority falsifier chain is non-vacuous and operates on registry-text and designed-column-tuple inputs available at scaffold time without requiring materialization. The unknowns U1–U6 (cross-region policy choice, rating algorithm, view-vs-raw, materialization SQL, post-materialization audit, closure) are correctly DEFERRED to successor PRs without compromising the scaffold's scientific defensibility.

Seven non-blocking nits should be addressed before the Layer-2 PR opens. None of them rises to a blocker. None require a Layer-1 plan redraft; each is a one- or two-line targeted edit at the relevant T-step or in the suggested-edit list communicated to the Layer-2 executor.

## Per-challenge findings

| # | Challenge | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Scaffold is next atomic unit (vs adjudication-first) | **STILL-CORRECT** | `git log` shows PR #232 (ROADMAP stub `6447399a`) → PR #233 (scaffold `b83c8e9a`) → PR #234 (adjudication `bc5cc8e5`); same ordering applies to tranche-2. Plan Problem Statement cites this precedent verbatim. |
| 2 | Adjudication-first prerequisite? | **NO-PREREQUISITE** | Registry CSV rows 7–12 loadable as-is; `cross_region_fragmentation_handling` row carries `allowed_with_caveat` (no policy commitment needed at scaffold layer); `reconstructed_rating` row carries `G-CS-4` (no rating-model commitment needed). Plan U1/U2 correctly defer the unbound choices. |
| 3 | Validator meaningful at scaffold stage | **MEANINGFUL** | T03 step 3's 16-entry falsifier priority list is composed of registry-membership checks, registry-row text-equality checks (prediction_setting, temporal_anchor, cutoff-rule strict-<, status, cold-start gate set), registry-row text-substring checks (tracker source prefix), and designed-column-tuple checks (post-game tokens, IN_GAME_HISTORICAL subset). All 16 operate on inputs present at scaffold time (registry CSV + notebook-supplied tuples). None requires materialized output. |
| 4 | Six-family enforcement | **ALL-PRESENT** | T03 step 3 priority list covers all 7 required rejections: missing family (1), extra family (2), wrong prediction_setting (7), in_game_snapshot aliased to a tranche-2 ID (4), blocked_or_deferred aliased (5), pre_game aliased (3), direct tracker_events_raw source (10). |
| 5 | `in_game_history_aggregate` framing | **OK** | T06 step 3 "Three concepts distinguished" markdown cell explicitly disambiguates `history_enriched_pre_game` (over PRIOR matches, strict-<) from `in_game_snapshot` (over target-match events, deferred to Step 02_01_04) from `IN_GAME_HISTORICAL` columns (per CROSS-02-00 §5.4, retained for prior-match aggregation use). T01 step 11 binds the column tuple to the §5.4-retained set `("APM","SQ","supplyCappedPercent","header_elapsedGameLoops")`. |
| 6 | `matches_history_minimal` documentation | **PRESENT (procedural)** | T06 step 3 dedicated markdown cell documents MHM consumption. Plan A8 enforces this via reviewer reading rather than runtime markdown linting; Open Question 1 correctly justifies this choice. ROADMAP `method:` line 2326 (verified) names only `matches_flat_clean` + `player_history_all`, so the MHM gap the plan addresses is real. |
| 7 | Strict-< at scaffold stage | **OK** | T02 step 5 (`_check_cutoff_rule_is_strict`) operates on registry row text `allowed_cutoff_rule` field plus a forbidden-operator substring check on `<=`/`==`/`>=`. It does NOT claim to runtime-check actual SQL semantics. The scaffold layer has no SQL to check. |
| 8 | Materialization/audit deferred | **ALL-DEFERRED** | Plan §Out of scope explicitly defers: materialization SQL, Parquet artifact, CROSS-02-01 leakage audit, §10 verdict re-run, cross-region policy choice, rating algorithm choice, K/m/α empirical thresholds, Phase 03, Step 02_01_04, Step closure, dataset research_log append, AoE2, cleaning-layer YAML, spec patches. |
| 9 | Phase 03 remains barred | **YES** | PHASE_STATUS.yaml frozen at Phase 02 = in_progress; T01–T09 produce no Phase 03 artifact; §Out of scope explicit; §File Manifest confirms PHASE_STATUS.yaml not touched. |
| 10 | File manifest / version | **OK with counting nit N1** | Verified PR #233 (`b83c8e9a` stat block) shipped 7 execution files + 2 planning files = 9 total. Plan §File Manifest claims "8 deliverable + 1 inherited" which is a miscount (double-counts current_plan.md). Version 3.71.0 → 3.72.0 minor; consistent with PR #233's 3.67.0 → 3.68.0 minor bump pattern. |
| 11 | Blockers + nits | **NONE blockers / 7 nits** | See sections below. |

## Blockers

**None.** The Layer-1 plan is methodology-defensible and the Layer-2 execution it describes mirrors the verified PR #232 → #233 → #234 sequence. The unknowns U1–U6 are correctly deferred to successor PRs; the validator's 16-priority falsifier chain is non-vacuous and operates on registry-text + designed-column-tuple inputs that exist at scaffold time; the MHM gap is correctly documented as scaffold prose; the strict-< gate is correctly a registry-text check (not a runtime SQL check).

## Nits (non-blocking; address during Layer-2 execution T05/T06/T07)

- **N1 — File manifest miscount (cosmetic).** Plan §File Manifest says "8 deliverable + 1 inherited" (Layer-2 PR). Actual tally: scaffold .py + scaffold .ipynb + validator + test + INDEX + CHANGELOG + pyproject = 7 deliverable; current_plan.md + current_plan.critique.md = 2 inherited. Total = 9. PR #233 stat block confirms: "9 files (2 planning + 7 execution)". Fix in T07 prose: "7 deliverable files + 2 inherited planning files = 9-file Layer-2 PR".

- **N2 — Cold-start gate set rigour (registry-bound vs spec-bound).** Plan Open Question 2 articulates the tension: CROSS-02-02 §9 enumerates G-CS-2..G-CS-6, but the registry CSV rows 7–12 use only G-CS-2/3/4/5. The plan's recommendation (strict registry-bound `{G-CS-2..G-CS-5}`) is defensible but creates a fragile coupling: if the materialization PR introduces a G-CS-6 cold-start row (per ROADMAP method lines 2334–2338 which DO enumerate G-CS-6 as the fold-aware fit gate), the validator will reject. Recommendation: keep strict but add an inline code comment citing ROADMAP lines 2334–2338 and explicitly noting "G-CS-6 is a materialization-time fit gate, not a registry-time gate; if a future PR adds G-CS-6 to a registry row, update this set". This makes the coupling intentional, not accidental.

- **N3 — `cross_region_caveat_missing` priority ordering ambiguity.** T05 test 13 (`TestCrossRegionCaveatMissing`) acknowledges that removing the cross-region row triggers EITHER `missing_families_in_tranche` OR `cross_region_caveat_missing` "whichever fires first by priority". Per T03 step 3 priority list, `missing_families_in_tranche` (item 1) outranks `cross_region_caveat_missing` (item 13); the test must assert the priority-1 falsifier deterministically. The plan's "in (X, Y)" assertion is too loose — make it `== "missing_families_in_tranche"` and add a SEPARATE test that keeps the row but flips `status` to assert `cross_region_caveat_missing`. (The plan already specifies the second case in the "separately:" clause; tighten the first assertion.)

- **N4 — `IN_GAME_HISTORICAL` runtime falsifier scope risk.** Open Question 4 surfaces this: T03 step 12 implements `_check_in_game_history_aggregate_columns` as a hard runtime falsifier that rejects any column outside the §5.4-retained set. If CROSS-02-00 §5.4 is later amended (e.g., a future PR re-classifies a column as IN_GAME_HISTORICAL), the validator and the constant `IN_GAME_HISTORICAL_AGGREGATED_COLUMNS` must be updated in lockstep. Recommendation: keep the runtime check (it is methodologically correct for a scaffold layer to enforce the current §5.4 contract) but add a docstring-level note: "If CROSS-02-00 §5.4 is amended, update `IN_GAME_HISTORICAL_AGGREGATED_COLUMNS` to match before regenerating any scaffold". This is a maintainability hedge, not a defensibility flaw.

- **N5 — §10 re-run gate silence (Open Question 5).** ROADMAP `continue_predicate` (line 2464+) requires either a re-executed §10 audit OR a non-vacuous justification before tranche-3 (the in_game_snapshot tranche). The scaffold neither re-runs nor records a placeholder decision. Plan §Out of scope correctly defers this to the materialization PR. Recommendation: T06 step 3 should add ONE sentence to the "Cross-region adjudication DEFERRED" or "Closing" cell: "§10 verdict-audit re-run vs justification decision: DEFERRED to materialization PR per ROADMAP `continue_predicate` (lines 2464+)". This makes the deferral explicit in the notebook rather than implicit in the plan.

- **N6 — Test count target.** Plan recommends ≥30 with stretch ≥35. Tranche-1 achieved 31. T05's 17 test classes naturally land in that range. No action; the target is fine.

- **N7 — `source_table_or_event_family == "matches_flat"` vs operational `matches_flat_clean`.** Plan A3 binds the validator to `matches_flat` (registry-recorded source). U3 correctly defers the view-vs-raw layer resolution to the tranche-2 adjudication PR (analogous to PR #234 which resolved the same tranche-1 question). Registry rows 7–12 all carry `source_table_or_event_family=matches_flat`. The validator's registry-bound stance is defensible. No action.

## Recommendation

**APPROVE-WITH-NITS.** The Layer-1 plan is methodology-defensible. The Layer-2 executor should incorporate nits N1–N5 as targeted in-place edits during T05/T06/T07 execution; nits N6–N7 require no action (acknowledgements that the plan's current choices are defensible).

The Layer-2 execution PR is expected to ship **7 execution files** (scaffold .py + .ipynb pair, validator module, test file, INDEX, CHANGELOG, pyproject) + **2 inherited planning files** (current_plan.md, current_plan.critique.md) = **9 files total**. Version bump `3.71.0 → 3.72.0` (minor; feat). Coverage target ≥95% on the validator module. Test count target ≥30 (stretch ≥35). Reviewer routing: `@reviewer-deep` mandatory; `@reviewer-adversarial` conditional on a reviewer-deep methodology BLOCKER (per `.claude/rules/data-analysis-lineage.md` — the scaffold materializes nothing and writes no artifact).

## Reviewer credentials

- **Role**: reviewer-adversarial (methodology examiner; read-only)
- **Model**: claude-opus-4-7[1m]
- **Date**: 2026-05-24
- **Inputs read**: full plan body (`/tmp/planner_output_layer3.md` lines 1–744); ROADMAP Step 02_01_03 block (`src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` lines 2274–2523); registry CSV rows 7–12; tranche-1 validator (`src/rts_predict/games/sc2/datasets/sc2egset/validate_pre_game_feature_materialization.py`, 644 LOC); PR #233 commit stat (`b83c8e9a`); git log for sequence verification (PR #232 → #233 → #234 ordering); `pyproject.toml` current version.
- **Lenses applied**: temporal discipline (Invariants I3, I4), statistical methodology (I8 — N/A for scaffold), feature engineering (I2, I5, I7), thesis defensibility (examiner simulation), cross-game comparability (I8 — N/A for SC2-only scaffold).
- **Verdict resolution**: 11 challenges adjudicated; 0 blockers; 7 non-blocking nits; APPROVE-WITH-NITS.
- **Rounds**: 1 of 3 used (per `feedback_adversarial_cap_execution.md` 3-round symmetric cap).

## Manifest-count clarification addendum (post-review N1 application)

**N1 was applied before merge.** Four contradictory phrases in `planning/current_plan.md` (Scope L47, Execution Steps L278, File Manifest L600, Gate Condition L628) that referenced "exactly 8 files" / "8 deliverable" / "T01-T08 produce the 8" / "8 deliverable + 1 inherited" have been corrected to the consistent contract: **7 execution files + 2 inherited planning files = 9 total** for the future Layer-2 PR. The frontmatter `future_execution_pr_scope` field (L35) was already correct and required no edit. The four corrections are pure-wording (no scientific scope change, no falsifier-order change, no T-step renaming, no Open Questions change). Nits N2–N7 remain unchanged and are addressable as targeted in-place edits during Layer-2 T05/T06/T07 execution.
