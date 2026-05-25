---
category: A
branch: feat/sc2egset-02-01-03-history-cross-region-adjudication
title: "SC2EGSet Step 02_01_03 — Q5 cross-region retention-measurement successor adjudication (Layer-1 planning PR)"
phase: "02 — Feature Engineering"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
step_number: "02_01_03"
dataset: "sc2egset"
predecessors:
  - "PR #242 — Step 02_01_03 source/anchor/cold-start adjudication (merged on master e372e7b66be66b6026fb3bc39f51d1975da0b8b1; Q5 cross_region + Q6 rating both deferred_blocker)"
  - "PR #241 — Step 02_01_03 scaffold + ONE validator (merged on master 3c6709bf; validator SHA-256 b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904)"
  - "PR #240 — Layer-1 scaffold plan (merged 33e3c681)"
  - "PR #239 — ROADMAP stub (merged f378f6f4)"
  - "PR #237 — Step 02_01_02 closure (merged a16d78c2)"
  - "PR #236 — Step 02_01_02 materialization + first non-vacuous CROSS-02-01 audit (merged 39298c0a)"
  - "PR #234 — Step 02_01_02 tranche-1 source/anchor/race adjudication (merged 93240b19; precedent for adjudication CSV+MD shape)"
  - "01_05_10 cross-region history impact (W=30 FAIL on disk; sequencing predecessor)"
  - "01_04_05 cross-region annotation (adds `is_cross_region_fragmented` to player_history_all VIEW)"
base_ref: e372e7b66be66b6026fb3bc39f51d1975da0b8b1
date: 2026-05-24
planner_model: claude-opus-4-7[1m]
critique_required: true
critique_path: "planning/current_plan.critique.md"
gate_reviewer: "reviewer-adversarial (Category A pre-execution gate; round 4 of 4 with user-authorized one-round override of the 3-round cap — FINAL round; rounds 1, 2, and 3 returned HOLD; this revision is a strict mechanical B4 count-contradiction fix on top of the R3 plan with NO methodology change)"
planning_pr_scope: "Layer-1 (exactly 2 files) — planning/current_plan.md + planning/current_plan.critique.md. NO Q5 successor adjudication CSV/MD, NO source module, NO test, NO notebook edits, NO feature materialization, NO ROADMAP edits, NO status YAML edits, NO research_log entry, NO CHANGELOG/pyproject/INDEX edits in this Layer-1 PR (those land in the future Layer-2 PR), NO spec or cleaning-layer YAML edits, NO thesis/docs/.claude/data/notebooks/AoE2 edits, NO Step 02_01_04 start, NO Phase 03 start, NO baseline modeling, NO Q6 rating-family adjudication work (deferred to a separate future planning round)."
future_execution_pr_scope: |
  Future Layer-2 Q5-only successor adjudication PR = 11 final tracked files:
    9 deliverable/execution files:
      1. sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.py
      2. sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.ipynb
      3. src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py
      4. tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_cross_region_retention.py
      5. src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.csv
      6. src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.md
      7. planning/INDEX.md
      8. CHANGELOG.md
      9. pyproject.toml
    + 2 inherited planning files already in the branch:
      10. planning/current_plan.md
      11. planning/current_plan.critique.md
version_bump_planned: "Layer-1 PR — version-neutral (planning-only). Future Layer-2 successor adjudication PR planned bump: minor 3.73.0 → 3.74.0 (feat-family per .claude/rules/git-workflow.md — adds a new adjudicator module + new successor adjudication artifact pair; no materialized feature data). Round-1 reviewer-adversarial accepted this rationale; record verbatim in the [3.74.0] CHANGELOG block per T08 step 1."
invariants_touched: [I3, I6, I7, I8, I9, I10]
source_artifacts:
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv (PR #242 parent; Q5/Q6 deferred_blocker rows; this PR's parent_pr242_csv_sha256 anchor)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md (PR #242 parent MD; this PR's parent_pr242_md_sha256 anchor)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/cross_region_history_impact_sc2egset.md (01_05_10 W=30 FAIL evidence; primary retention measurement anchor; SHA to be captured at Layer-2 write time)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/cross_region_history_impact_sc2egset.json (01_05_10 JSON; numeric anchors verified on-disk: n_cross_region_nicknames=246, median_rolling30_undercount_games=16.0, p95_rolling30_undercount_games=29.0, mmr_spearman_rho_point=0.1384, mmr_spearman_rho_bootstrap_ci_high=0.2913, n_players_with_mmr=157; NOTE: the JSON does NOT include `n_player_match_pairs` or `n_distinct_toon_ids` — those 32,031 and 1,923 anchors live ONLY in the MD §3.3 table at line 398, and were computed by 01_05_10 MD SQL 3 as a nickname-anchored join over PHA rows, NOT as a toon_id-membership query; see NIT-C resolution below)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_05_cross_region_annotation.md (1,923 cross-region toon_ids; cleaning-layer step that adds `is_cross_region_fragmented` to player_history_all VIEW per §1; §7 enumerates 3 strategies on lines 200-216: strategy 1 'Safe-subset filter: WHERE NOT is_cross_region_fragmented — restricts history to non-fragmented players' on lines 203-208, strategy 2 'Dual feature paths' on lines 210-212, strategy 3 'Sensitivity indicator' on lines 214-216)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_04_cross_region_nicknames.csv (246 cross-region nickname inventory)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/06_decision_gates/risk_register_sc2egset.md (SC-R01 MEDIUM IDENTITY entry; ~12% migration rate accepted bias)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md §2 (I2 Branch (iii) region-scoped toon_id decision; declared cross-scope tolerance)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv (row 11 = cross_region_fragmentation_handling family; SHA 320b8b018982f12539a34512421f1b34359bb825f0d1410687492dfe5c6fed1f)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py (PR #241 scaffold; _check_cross_region_caveat helper at line 479; SHA b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py (PR #242 adjudicator module; format precedent for the Q5 successor module)"
  - "tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_enriched_pre_game_source_layer.py (PR #242 mirrored tests; pattern precedent)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md lines 2274-2523 (Step 02_01_03 block; line 2356 cites CROSS-02-02 §6.2 row 5 / RISK-20 three-option enumeration; lines 2504-2508 codify the halt_predicate that this PR is designed to lift)"
  - "reports/specs/02_02_feature_engineering_plan.md §6.2 row 5 line 242 (cross_region_fragmentation_handling 3-option enumeration; the on-disk verbatim wording in the Source column is `player_history_all.is_cross_region_fragmented (CROSS-02-00 §5.4)` and in the Constraint column is 'Phase 02 must implement one of: (a) strict-exclusion sensitivity arm, (b) dual feature paths (with vs without filter), or (c) sensitivity indicator co-registered alongside the history features.' — see NIT-A re-attribution below); §9.1 G-CS-1..G-CS-6 (no magic numbers); §10 G-L-1..G-L-9 (leakage falsifiers)"
  - "reports/specs/02_00_feature_input_contract.md §5.4 (sc2egset PH IN_GAME_HISTORICAL columns); §3.3 strict-less-than rule"
  - "reports/specs/02_01_leakage_audit_protocol.md §2.1/§2.2/§2.3/§2.4"
  - "reports/specs/02_03_temporal_feature_audit_protocol.md §6.2 (history_enriched_pre_game prediction-setting rules); §10 D1-D15 verdicts"
  - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml (38-col schema; `is_cross_region_fragmented` declared at line 214 with NOTES on lines 220-226 prescribing `WHERE NOT is_cross_region_fragmented` over PHA rolling-window history; provenance.scope = 'All replays (no 1v1/decisive filter)' — see NIT-A re-attribution: the consolidated paraphrase 'Phase 02 rolling features over `player_id_worldwide` should apply `WHERE NOT is_cross_region_fragmented` as safe-subset filter, OR use dual feature paths, OR use as sensitivity indicator' lives ONLY in PHA YAML NOTES lines 220-226, NOT in 01_04_05 §7)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml (`match_id` = 'sc2egset::' || replay_id at lines 11-19; `player_id` = toon_id at line 31; `started_at` TIMESTAMP via TRY_CAST at lines 21-30)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml (30-col schema; row_count=44418; does NOT carry `is_cross_region_fragmented` — that column lives on player_history_all per 01_04_05; MFC primary keys are `replay_id` (line 12) and `toon_id` (line 24), NOT `match_id`/`player_id`)"
  - ".claude/scientific-invariants.md (I3 temporal+normalization; I5 symmetry; I6 SQL provenance; I7 no magic numbers; I8 cross-game; I9 step-derived conclusions; I10 relative-path)"
  - ".claude/ml-protocol.md (three leakage failure modes — rolling, h2h, co-occurring matches)"
  - ".claude/rules/data-analysis-lineage.md (non-batching rule; halt-before-artifact; required structure for every empirical analysis)"
  - ".claude/rules/git-workflow.md"
  - ".claude/rules/python-code.md (UPPER_SNAKE constants; _QUERY suffix; mirrored test layout)"
  - ".claude/rules/sql-data.md (replay_id canonical; view-vs-raw discipline)"
  - "docs/TAXONOMY.md / docs/PHASES.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml (no 02_01_03 row yet — must remain so)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml (02_01 = complete)"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml (Phase 02 = in_progress; Phase 03 = not_started)"
  - "CHANGELOG.md (current [3.73.0] block describes PR #242)"
  - "pyproject.toml (current version = 3.73.0)"
non_batching_sequence_position: "Step 3.5 of the lineage (Q5 cross-region retention adjudication — a refinement of the PR #242 adjudication that resolves one of its two deferred_blocker rows). Sits between PR #242 (general adjudication; sequence step 3) and the future materialization-execution plan (sequence step 4). Q6 rating-family adjudication is split off into a separate future planning round (sequence step 3.6 by convention) — see Open Questions OQ1."
q5_q6_separation_rationale: "Outcome B selected over Outcome A per analysis above. Q5 evidence = read-only DuckDB SQL probes against the existing 01_05_10 measurement substrate (246 nicknames, 1923 toon_ids, 32031 (player,match) pairs from MD §3.3); 3-option enumeration is pre-pinned by CROSS-02-02 §6.2 row 5. Q6 evidence = literature comparison + likely offline replay-fold pilot for ≥1 of 5 candidate families (no-rating / rolling baseline / Elo / Glicko / Glicko-2 / TrueSkill); N-X3 strengthened gate requires ≥1 repo path + ≥1 citation per binding branch. Bundling would (a) produce a ~12-16-row CSV (~2× PR #242 size); (b) couple unrelated evidence chains in violation of non-batching rule sequence step 5; (c) risk a partial upgrade that re-creates the MATERIALIZATION BLOCKED state. Splitting preserves the option to keep Q6 deferred while clearing Q5."
deep_research_disclaimer: "External literature/web searches will be required at Layer-2 ONLY to verify any rating-system citations that surface in Q5 sensitivity-arm rationale (none expected). Q6-specific rating literature is OUT OF SCOPE for this PR. Repo artifacts remain source of truth."
round2_blocker_resolutions:
  - "B1 (column location on PHA not MFC): resolved by re-anchoring every probe and every binding row to `player_history_all.is_cross_region_fragmented` (line 214 in player_history_all.yaml). MFC verified to have 30 columns and NO `is_cross_region_fragmented` (`grep -cE \"^- name: \" matches_flat_clean.yaml` = 30). PHA verified at 38 cols with the column declared at line 214 and notes at lines 220-226."
  - "B2 (MFC join keys are `replay_id`/`toon_id`, not `match_id`/`player_id`): resolved by replacing every `mfc.match_id` with `mfc.replay_id` and every `mfc.player_id` with `mfc.toon_id`. MHM join updated to `target.match_id = 'sc2egset::' || mfc.replay_id` (single-prefix on MFC's unprefixed key) and `target.player_id = mfc.toon_id`."
  - "B3 (filter HISTORY-rows-on-PHA, not TARGET-rows-on-MFC): resolved by committing explicitly to the prescribed semantics: `WHERE NOT ph.is_cross_region_fragmented` is applied to PHA history rows BEFORE aggregation. The alternative `WHERE NOT mfc.is_cross_region_fragmented` (which would drop target predictions) is now explicitly OUT OF SCOPE."
round2_nit_resolutions:
  - "N1 (parent_decision_id is SCHEMA EXTENSION, not inheritance): T01 step 4 now labels `parent_decision_id` as a NEW field introduced by this successor PR — back-fillable into PR #242 via future cosmetic chore (NOT in scope here). Confirmed via `grep -c parent_decision_id <pr242 csv>` = 0."
  - "N2 (version-bump rationale acceptable; record verbatim): frontmatter `version_bump_planned` field expanded with the round-1 reviewer's acceptance note; T08 step 1 records the bump rationale verbatim in the [3.74.0] CHANGELOG block."
  - "N3 (Q5C provisional recommendation defensive note): T05 step 4 reworded as 'PROVISIONAL pending probe results'; the executor MUST report the per-family retention table FIRST and the verdict EMERGES from the table. New A14 (verdict-emergence discipline) added to §Assumptions. T05 step 4's wording strengthened so the pre-bound `sensitivity_indicator_co_registration` recommendation cannot be silently rubber-stamped."
  - "N4 (single-prefix join key): dissolved by B2 fix — `'sc2egset::' || mfc.replay_id` (single prefix on MFC's unprefixed `replay_id`) is canonical."
round3_blocker_resolution:
  - "B4 (HELPER_TO_FALSIFIER_KEY count vs FALSIFIER_PRIORITY_CHAIN count contradiction): resolved. The authoritative counts are `len(HELPER_TO_FALSIFIER_KEY) == 31` and `len(FALSIFIER_PRIORITY_CHAIN) == 31`. Arithmetic provenance (R4-final): 25 entries after promoting `materialization_creep` + `decision_count_drift` from chain-only to mapping + 4 NIT-B SHA helpers + 2 NIT-D split helpers (structured-field check + SQL byte-scan check) = 31. The `TestPriorityChainReferencesMapping` test is rewritten to use set equality / containment + the exact-count assertion (`assert set(FALSIFIER_PRIORITY_CHAIN) == set(HELPER_TO_FALSIFIER_KEY.values())` AND `assert len(FALSIFIER_PRIORITY_CHAIN) == len(set(FALSIFIER_PRIORITY_CHAIN)) == len(HELPER_TO_FALSIFIER_KEY) == 31`). T03 and T04 Verifications assert `len(HELPER_TO_FALSIFIER_KEY) == 31 AND len(FALSIFIER_PRIORITY_CHAIN) == 31 AND set(FALSIFIER_PRIORITY_CHAIN) == set(HELPER_TO_FALSIFIER_KEY.values()) AND len(set(FALSIFIER_PRIORITY_CHAIN)) == 31`. The module-import guard codifies all 4 invariants at module load (T01 step 6 Verification) so any drift fails BEFORE any test runs."
round3_nit_resolutions:
  - "NIT-A (verbatim quote misattribution): re-attributed. The consolidated paraphrase 'Phase 02 rolling features over `player_id_worldwide` should apply `WHERE NOT is_cross_region_fragmented` as safe-subset filter, OR use dual feature paths, OR use as sensitivity indicator' is sourced from `player_history_all.yaml` NOTES lines 220-226 ONLY (confirmed by on-disk read). When citing `01_04_05 §7`, this plan now quotes the actual on-disk strategy-1 wording from lines 203-208: 'Safe-subset filter: WHERE NOT is_cross_region_fragmented — restricts history to non-fragmented players; cleanest rolling-window estimates but reduces the training population to 7,716 / 44,817 rows = 17.2% of the corpus'. When citing `02_02_feature_engineering_plan.md` §6.2 row 5 line 242, this plan now quotes the actual on-disk Source-column wording (`player_history_all.is_cross_region_fragmented (CROSS-02-00 §5.4)`) and the actual on-disk Constraint-column wording ('Phase 02 must implement one of: (a) strict-exclusion sensitivity arm, (b) dual feature paths (with vs without filter), or (c) sensitivity indicator co-registered alongside the history features.'). Literature Context section + T05 Q5A binding rationale notes updated. The future verbatim-quote falsifier in T03 helpers checks each quote against the EXACT file/line source actually quoted."
  - "NIT-B (missing SHA constants for round-2 load-bearing artifacts): resolved by adding 4 new EXPECTED_*_SHA256 module constants in T01 step 3 with planner-computed 64-char lowercase hex values pinned in-plan (so the Layer-2 executor does NOT have to re-derive them). 4 new helpers in T03 + 4 new keys in HELPER_TO_FALSIFIER_KEY + 4 new positions early in FALSIFIER_PRIORITY_CHAIN + 4 new tests in T06 + 4 new CSV provenance columns. HELPER_TO_FALSIFIER_KEY and FALSIFIER_PRIORITY_CHAIN are 31 entries each (B4 + NIT-B + NIT-D arithmetic — see B4 resolution above)."
  - "NIT-C (probe anchor semantics — toon_id vs nickname): resolved. The R2 `_CROSS_REGION_BASE_PROBE_QUERY` joined PHA against `cross_region_nicks` on lowercase nickname AND claimed expected count 32,031, but 32,031 in 01_05_10 MD §3.3 was computed by SQL 3 as a nickname-anchored join (the same idiom). T03 keeps the nickname-anchored probe as the 01_05_10 EQUIVALENCE probe with expected count 32,031 (its falsifier key `cross_region_nickname_anchor_count_drift`) AND adds a SEPARATE toon_id-membership BINDING probe (the form prescribed by Q5's downstream filter semantics — `WHERE ph.is_cross_region_fragmented = TRUE` reaches every cross-region PHA history row, with its own expected count pinned at Layer-2 write time as `EXPECTED_PHA_CROSS_REGION_TOONID_MEMBERSHIP_COUNT: int`; its falsifier key `cross_region_toon_id_anchor_count_drift`). The dataclass schema gains a new field `cross_region_anchor_semantics: str` ∈ {`'toon_id_based'`, `'nickname_based'`, `'both'`} populated per per-option row to make the binding explicit. The plan states BINDING vs EXPLORATORY: binding probe = toon_id-membership, exploratory probe = nickname-join. The 32,031 expectation is shared ONLY by the nickname-anchored probe."
  - "NIT-D (vacuous text-presence falsifier under negation): resolved by replacing the substring check with a structured dataclass field `history_row_filter_on_pha_applied: str` ∈ ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED = frozenset({'yes', 'no', 'not_applicable'}). New helper `_check_history_row_filter_on_pha_field_valid` validates the field value AND cross-checks consistency with `selected_policy` (Q5A = 'yes'; Q5B = 'yes'; Q5C = 'no'; Q5_selected_policy = derived from chosen policy; Q5_per_family_impact_summary = 'not_applicable'). The old vacuous substring assertion is REMOVED from the prose part of falsifier #24. The SQL byte-scan portion (reject `mfc.is_cross_region_fragmented` as a WHERE predicate) is KEPT (it is non-vacuous). T06 `TestHistoryRowFilterFieldStructured` covers valid/invalid value cases AND Q5A-with-'no' (inconsistent → halt) AND Q5C-with-'yes' (inconsistent → halt) AND correct combos."
round4_blocker_resolution:
  - "R4 (B4-only mechanical fix on top of R3): the count contradiction between (frontmatter + T01 step 6 + T01 step 7 + T03 heading) claiming 29 and (T03 body + T04 + T06 + Gate Condition + CHANGELOG) claiming 31 is resolved by adopting 31 EVERYWHERE for HELPER_TO_FALSIFIER_KEY and FALSIFIER_PRIORITY_CHAIN. The R3 planner monologue at T03 (former lines 899-924) that left the count decision to the reviewer is DELETED and replaced with the decisive statement 'The 31-entry mapping and 31-entry priority chain are authoritative. See module-import verification below.' A new module-import mechanical verification (T01 step 6 Verification + module-level `assert` block per the POST_GAME_TOKEN_SCOPED_FIELDS.isdisjoint(POST_GAME_TOKEN_EXEMPT_FIELDS) precedent) catches drift at import time, not test time. T06 `TestHelperToFalsifierKeyMappingExactCount` asserts the 31/31 invariants explicitly. No methodology change; no new falsifier; no SQL probe change; no manifest change; no scope change. R1 (B1/B2/B3), R2 (N1/N3), and R3 (NIT-A/B/C/D) fixes preserved without regression."
---

## Scope

This is a **Layer-1 planning PR**. It commits ONLY two files:

- `planning/current_plan.md` (this document)
- `planning/current_plan.critique.md` (produced by reviewer-adversarial in a separate dispatch)

This plan describes the **future Layer-2 Q5-only successor adjudication execution PR** on branch
`feat/sc2egset-02-01-03-history-cross-region-adjudication`. The future Layer-2 PR has an
**11-file final tracked diff** — **9 deliverable/execution files** (notebook pair `.py` +
`.ipynb`, adjudicator source module, mirrored test file, successor adjudication CSV + MD
artifact pair, `planning/INDEX.md`, `CHANGELOG.md`, `pyproject.toml`) **plus the 2 inherited
planning files** carried forward from this Layer-1 PR.

The future Layer-2 PR is **Q5-only**. It produces ONE successor adjudication CSV+MD artifact
pair that resolves (or explicitly narrows / re-defers) the Q5 `cross_region_fragmentation_handling`
deferred_blocker row from the PR #242 parent CSV using read-only DuckDB retention probes that
**read `is_cross_region_fragmented` from `player_history_all`** (per 01_04_05 §1 + PHA schema
YAML line 214) and apply the canonical operationalization (filter HISTORY rows before
aggregation, per CROSS-02-02 §6.2 row 5 + 01_04_05 §7 strategy 1 + PHA YAML NOTES lines
220-226). The PR #242 CSV/MD remain **byte-unchanged**; the new artifact pair carries SHA-256
provenance anchors to PR #242 (`parent_pr242_csv_sha256`, `parent_pr242_md_sha256`,
`parent_pr242_artifact_sha256`) and provides the row data the future materialization plan
will consume in place of the PR #242 deferred row.

**Q6 rating-family adjudication is explicitly OUT of scope for this PR.** Q6 remains
`deferred_blocker` and continues to block materialization. A separate future planning round
will address Q6 per the rationale recorded in the frontmatter and Open Questions OQ1.

This PR explicitly does NOT materialize any feature value, does NOT write any Parquet, does NOT
run the CROSS-02-01-v1.0.1 post-materialization leakage audit, does NOT touch any status YAML,
does NOT append a `research_log.md` entry, does NOT close Step 02_01_03, does NOT begin Step
02_01_04, does NOT begin Phase 03, does NOT re-execute the CROSS-02-03 §10 verdict audit, does
NOT edit any spec or cleaning-layer YAML, does NOT edit the ROADMAP, does NOT re-edit the
PR #242 adjudication module / test / notebook / CSV / MD (all byte-unchanged anchors), does
NOT re-edit the PR #241 scaffold validator (byte-unchanged anchor).

## Problem Statement

PR #242 (merged on master `e372e7b6`) adjudicated 8 coupled questions for the
`history_enriched_pre_game` tranche, of which **Q5** (`cross_region_fragmentation_handling`
operationalization per RISK-20) and **Q6** (`rating_policy` model family for
`reconstructed_rating` per G-CS-4) closed as `verdict=deferred_blocker` /
`binding_level=deferred_blocker`. The PR #242 MD §13 hard-stops materialization until both are
upgraded to one of `bind_now` / `ratify_with_evidence` / `extend_with_evidence` /
`narrow_with_evidence` in a successor adjudication PR.

**Q5 is the empirically-tighter and lineage-richer of the two**:

- CROSS-02-02 §6.2 row 5 (`reports/specs/02_02_feature_engineering_plan.md` line 242)
  pre-enumerates three operationalization options in the Constraint column with the actual
  on-disk wording: "Phase 02 must implement one of: (a) strict-exclusion sensitivity arm,
  (b) dual feature paths (with vs without filter), or (c) sensitivity indicator co-registered
  alongside the history features." The Source column names the column as
  `` `player_history_all.is_cross_region_fragmented` (CROSS-02-00 §5.4) `` — the column lives
  on the **history view (PHA)**, NOT on the **target/cleaning view (MFC)**.
- The 01_05_10 cross-region history impact artifact (`cross_region_history_impact_sc2egset.{md,json}`,
  W=30 FAIL verdict; on-disk JSON anchors: `n_cross_region_nicknames=246`,
  `median_rolling30_undercount_games=16.0`, `p95_rolling30_undercount_games=29.0`,
  `mmr_spearman_rho_bootstrap_ci_high=0.2913`, `n_players_with_mmr=157`; MD-only anchors at
  §3.3 line 398: `1,923 distinct toon_ids`, `32,031 (player, match) pairs`) is already on disk
  and was authored as the Phase-01 evidence substrate that this Phase-02 retention adjudication
  is designed to consume.
- The cleaning-layer step 01_04_05 (`01_04_05_cross_region_annotation.md` §1) added
  `is_cross_region_fragmented` BOOLEAN as the 38th projected column of `player_history_all`
  (NOT of `matches_flat_clean` — MFC remains a 30-column view per `matches_flat_clean.yaml`
  schema_version `30-col (ADDENDUM: duration added 2026-04-18)`, row_count 44418). Per-option
  retention counts for Q5 can be computed with read-only SQL against `player_history_all`
  (history rows; source-of-truth for `is_cross_region_fragmented`) joined to
  `matches_history_minimal` (target rows; canonical `started_at` anchor) using
  `'sc2egset::' || ph.replay_id` for the prefixed match key.

**The canonical retention semantics is filter-HISTORY-rows, not filter-TARGET-rows.** Two
on-disk passages anchor this:

- **`player_history_all.yaml` NOTES lines 220-226** (verbatim consolidated paraphrase, source of
  the often-misattributed quote per NIT-A re-attribution):

  > Phase 02 rolling features over `player_id_worldwide` should apply
  > `WHERE NOT is_cross_region_fragmented` as safe-subset filter, OR use dual feature paths,
  > OR use as sensitivity indicator.

- **`01_04_05_cross_region_annotation.md` §7 strategy 1 lines 203-208** (verbatim actual
  on-disk wording, NOT the consolidated paraphrase above):

  > Safe-subset filter: `WHERE NOT is_cross_region_fragmented` — restricts history to
  > non-fragmented players; cleanest rolling-window estimates but reduces the training
  > population to 7,716 / 44,817 rows = 17.2% of the corpus (tournament players are
  > over-represented among the 1,923 flagged toons; see §4 flag distribution). This is a
  > material data loss; strategy (2) or (3) are usually preferable for non-catastrophic
  > bias levels.

- **`02_02_feature_engineering_plan.md` §6.2 row 5 line 242 Source column** (verbatim):

  > `player_history_all.is_cross_region_fragmented` (CROSS-02-00 §5.4)

- **`02_02_feature_engineering_plan.md` §6.2 row 5 line 242 Constraint column** (verbatim):

  > Per RISK-20 / Phase 01 W=30 FAIL verdict, Phase 02 must not hard-code a retention
  > percentage for `WHERE NOT is_cross_region_fragmented` filtering. Phase 02 must implement
  > one of: (a) strict-exclusion sensitivity arm, (b) dual feature paths (with vs without
  > filter), or (c) sensitivity indicator co-registered alongside the history features.
  > The choice is deferred to a Phase 02 ROADMAP step that empirically measures retention.

All four passages **prescribe filtering applied to PHA (history) rows BEFORE aggregation** —
they do NOT prescribe filtering applied to MFC (target) rows. The two filter sites have
different semantics:

| Filter site | Effect on training/predicted set | Effect on history depth |
|---|---|---|
| **PHA (HISTORY)** — `WHERE NOT ph.is_cross_region_fragmented` BEFORE aggregation | unchanged (every target row is still predicted) | reduced for affected players (their cross-region historical entries are dropped from the aggregate window) |
| MFC (TARGET) — `WHERE NOT mfc.is_cross_region_fragmented` over target rows (NOT in scope; the column does not exist on MFC; even if it did, this is not one of the three CROSS-02-02 options) | reduced (cross-region targets dropped from training/predicted set) | unchanged for kept rows |

This plan binds the PHA-history-row site as the only semantics evaluated. The MFC-target-row
alternative is NOT one of the CROSS-02-02 three options and is explicitly OUT OF SCOPE; if
that alternative ever becomes relevant, it belongs in a different adjudication.

**Q6 is intentionally OUT of scope**:

- CROSS-02-02 §9.2 explicitly does not commit "a specific Bayesian-smoothing functional form" or
  "an imputation strategy for missing rating values".
- The N-X3 strengthened gate inherited from PR #242 requires ≥1 repo path + ≥1 primary-source
  citation per binding family branch, plus forward-only-wording + cold-start + missingness-handling
  language in notes. Currently no repo-path evidence exists for any of {no-rating / rolling
  baseline / Elo / Glicko / Glicko-2 / TrueSkill}; satisfying N-X3 for a `bind_now` verdict
  almost certainly requires an offline replay-fold backtest pilot — a Phase-02 modeling surface
  not appropriate for a single planning round bundled with cross-region measurement.

Bundling Q5+Q6 would violate the non-batching rule's sequence-step-5 boundary and produce a
~12-16-row CSV that adversarial review at the PR #242 scale (8 rows × 33 columns) already
exercised hard enough. **Splitting Q5 first** clears one of the two `MATERIALIZATION BLOCKED`
rows with the easier evidence chain and preserves the option to either bind Q6 later (with a
dedicated planning round) or document continued deferral as a calibrated decision rather than
a residual default.

## Assumptions & Unknowns

### Assumptions (BINDING for the future Layer-2 PR)

A1. **PR #242 byte-unchanged.** The adjudication CSV, MD, adjudicator module, test file, and
  notebook from PR #242 are byte-unchanged in this branch. The Layer-2 PR re-asserts their
  SHA-256s as `parent_pr242_*_sha256` provenance constants in every new CSV row.

A2. **PR #241 scaffold validator byte-unchanged.** SHA-256
  `b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904` is re-asserted as
  `pr241_scaffold_validator_module_sha256` in every new CSV row.

A3. **01_05_10 substrate is the authoritative cross-region measurement anchor.** The Layer-2 PR
  reads (in the notebook only, via the adjudicator module) the same `replay_players_raw` /
  `player_history_all` / `matches_history_minimal` / `matches_flat_clean` tables that 01_05_10
  measured and reproduces the 246-nickname / 1,923-toon_id / 32,031 (player,match) pair
  invariant within the same DuckDB; the new artifact does NOT re-derive these from raw replays.
  See NIT-C resolution: the 32,031 anchor is nickname-anchored (per 01_05_10 SQL 3); the new
  toon_id-membership binding probe has its own (TBD-at-Layer-2) expected count.

A4. **Three options are pre-enumerated by CROSS-02-02 §6.2 row 5** (line 242 of
  `02_02_feature_engineering_plan.md`). The Layer-2 adjudicator evaluates exactly
  `{strict_exclusion, dual_feature_path, sensitivity_indicator_co_registration}` and does not
  invent a fourth option. Each option gets its own per-family-impact row in the successor CSV.
  A4 explicitly excludes the MFC-target-row drop alternative (see Problem Statement table).

A5. **Canonical strict-< filter (B-X2 inherited).** Every SQL probe uses
  `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at` (NOT bare CAST) per
  `matches_history_minimal.yaml`. This is the same canonical form as PR #242's
  `STRICT_LT_HISTORY_FILTER` and is re-asserted as `STRICT_LT_HISTORY_FILTER` in the new
  adjudicator module.

A6. **Adjudicator module path.**
  `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py`
  (mirroring the PR #242 `adjudicate_history_enriched_pre_game_source_layer.py` filename pattern,
  scoped to the Q5 successor surface). Public entrypoint
  `adjudicate_history_cross_region_retention(...) -> CrossRegionAdjudicationResult` writes CSV
  + MD via two helpers (`_write_csv`, `_write_md`); never writes Parquet; never mutates the
  DuckDB; never edits any prior on-disk artifact.

A7. **Mirrored test path.**
  `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_cross_region_retention.py`
  per `python-code.md` mirrored-tree convention.

A8. **Coverage gate.** ≥95% line coverage on the adjudicator module (PR #234 / PR #241 / PR #242
  precedent; matches `[tool.coverage.report] fail_under = 95` in `pyproject.toml`).

A9. **Notebook discipline.** Jupytext `py:percent` `.py` canonical + paired `.ipynb` (outputs
  cleared); no `def`/`class`/`lambda` in cells; all logic imported from the adjudicator module;
  `print()` only for read-only DuckDB exploration; `logging.getLogger(__name__)` for diagnostics.
  Per `feedback_notebook_iterative_testing.md`, every notebook cell declares its hypothesis +
  falsifier inline before executing.

A10. **CSV/MD provenance.** Every CSV row carries `provenance_git_sha` (resolved at write time),
  `pr241_scaffold_validator_module_sha256`, `parent_pr242_csv_sha256`, `parent_pr242_md_sha256`,
  `parent_pr242_artifact_sha256` (which equals the hash of the CSV+MD pair concatenated), and
  per-input SHA-256s (registry CSV, methodology risk register, 4 CROSS-02-NN specs, 3
  cleaning-layer YAMLs, 01_05_10 MD+JSON, DuckDB path) **PLUS the 4 NIT-B added SHAs:
  `player_history_all_yaml_sha256`, `step_01_04_05_md_sha256`, `matches_flat_clean_yaml_sha256`,
  `cross_02_02_spec_sha256`**. The MD reproduces every SQL probe and its result verbatim
  (Invariant I6); SHA-256 fields are 64-char lowercase hex with no `NOT_FOUND` placeholder.
  **The verdict EMERGES from the per-family retention table — it is not pre-bound by the
  planner. T05 step 4's recommendation is provisional.**

A11. **Per-option × per-family retention table is the central evidence object.** The successor
  artifact decomposes each of the three options into per-family retention counts (history-rows-kept,
  history-rows-dropped, players-affected, matches-affected) for each of the 6 history families
  (`focal_player_history`, `opponent_player_history`, `matchup_history_aggregate`,
  `reconstructed_rating`, `cross_region_fragmentation_handling`, `in_game_history_aggregate`).
  The table is the empirical substrate for the Q5 verdict; without it the verdict is
  unjustifiable.

A12. **Q6 frozen.** The Layer-2 PR makes ZERO edits to any Q6-related artifact, no Q6 row in the
  new CSV, no Q6 wording in the new MD except a one-line statement that Q6 remains
  `deferred_blocker` and is out of scope for this PR. The PR #242 Q6 row remains the
  authoritative Q6 record.

A13. **Three-round adversarial cap applies symmetrically** (per memory
  `feedback_adversarial_cap_execution.md`). Round 4 of 4 on the plan side (this round is the
  FINAL plan-side round, run under explicit user-authorized one-round override of the standard
  3-round cap for a mechanical B4-only fix); round 1 of 3 will separately apply on the
  execution side.

A14. **Verdict-emergence discipline (round-2 N3 binding).** The planner's recommended verdict
  in T05 step 4 is **provisional**. The Layer-2 executor MUST:
  - Run all probes FIRST and report the per-family retention table BEFORE selecting any policy.
  - The verdict is computed from the table, not pre-bound from the plan.
  - If the table contradicts the provisional recommendation (e.g.,
    `_SENSITIVITY_INDICATOR_FLAG_NONDEGENERACY_QUERY` shows a non-trivial NULL count, or
    `_STRICT_EXCLUSION_HISTORY_FILTER_RETENTION_QUERY` shows a retention loss within a
    notebook-declared tolerance), the executor MUST escalate to the planner BEFORE writing the
    artifacts (per `data-analysis-lineage.md` "Stop conditions").
  - The recommended verdict CANNOT be rubber-stamped without surfacing the per-family table
    in the notebook output.

A15. **PHA is the source-of-truth for `is_cross_region_fragmented` (round-2 B1 binding).**
  Every reference to the column in module constants, SQL probes, decision-row scope strings,
  rationale prose, and test fixtures resolves to `player_history_all.is_cross_region_fragmented`.
  No probe, no row, and no rationale references `matches_flat_clean.is_cross_region_fragmented`
  (which does not exist — MFC is a 30-column view). The Q5 successor module's only `mfc.*`
  references are for the join keys `mfc.replay_id` and `mfc.toon_id` (the canonical MFC
  primary keys per `matches_flat_clean.yaml` lines 12 and 24).

A16. **MFC join keys are `replay_id` / `toon_id`, MHM keys are `match_id` / `player_id`
  (round-2 B2 binding).** Every MFC ↔ MHM join uses:
  `target.match_id = 'sc2egset::' || mfc.replay_id` AND `target.player_id = mfc.toon_id`.
  Every PHA ↔ MHM join uses:
  `target.match_id = 'sc2egset::' || ph.replay_id` AND `target.player_id = ph.toon_id`.
  Single-prefix on the unprefixed MFC / PHA `replay_id`; never double-prefix.

A17. **The Q5 retention filter is applied to HISTORY rows on PHA, not to TARGET rows on MFC
  (round-2 B3 binding).** Per CROSS-02-02 §6.2 row 5 + 01_04_05 §7 strategy 1 + PHA YAML NOTES
  lines 220-226 (each quoted verbatim from its actual on-disk location in §Literature Context),
  the canonical operationalization is `WHERE NOT ph.is_cross_region_fragmented` applied to PHA
  history rows BEFORE per-family aggregation. Filtering target rows on MFC (e.g.,
  `WHERE NOT mfc.is_cross_region_fragmented`) is NOT one of the three CROSS-02-02 options and
  is OUT OF SCOPE.

A18. **(NEW round-3 NIT-B) Source-artifact SHA pinning for the round-2 load-bearing files.**
  Four source files load-bearing to round-2 B1/B3 fixes have their SHA-256 pinned at planner
  time and frozen as module constants. The Layer-2 executor's helpers re-compute the hashes
  at run time and halt on any drift. Pinned values (computed via
  `shasum -a 256 <path>` on master HEAD `e372e7b6` at planner-time 2026-05-24):
  - `player_history_all.yaml` = `7962dd910e0b72419e35a9895689cd4ae6a51c2be0bc6e5e0fe4a0ceb8f207d0`
  - `01_04_05_cross_region_annotation.md` = `7bac26fd69952509a9dac323436e074902ca8ba9e0bac64021ad04de7f5dc9fe`
  - `matches_flat_clean.yaml` = `9f76c1912624535b7b7ac0d2fb767fd4b9791a1d808bf73f747416d557d6cb1f`
  - `02_02_feature_engineering_plan.md` (`reports/specs/`) = `86af792370272e611f048aae0c48c9cc595eb4b44c1db38c0bb4ecea0ff1b289`
  If any of these files is touched between Layer-1 merge and Layer-2 execution, the executor
  must HALT, re-read the changed file, re-verify the round-2 B1/B3 binding rationale still
  holds, then re-pin and re-PR. This is the same drift-discipline as the existing PR #242
  parent SHAs.

A19. **(NEW round-3 NIT-C) Probe anchor semantics are explicit and machine-readable.**
  The successor CSV gains a new dataclass field
  `cross_region_anchor_semantics: str ∈ ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS = frozenset({'toon_id_based', 'nickname_based', 'both'})`.
  Each per-option decision row populates this field per the binding probe used. The new
  toon_id-membership BINDING probe (`_CROSS_REGION_TOONID_MEMBERSHIP_BASE_PROBE_QUERY`)
  computes `COUNT(*) FROM player_history_all ph WHERE ph.toon_id IN (SELECT DISTINCT toon_id FROM player_history_all WHERE is_cross_region_fragmented = TRUE)`;
  its expected count is `EXPECTED_PHA_CROSS_REGION_TOONID_MEMBERSHIP_COUNT: int`,
  pinned at Layer-2 write time (Invariant I7 — derive once from live DuckDB, then pin). The
  EQUIVALENCE probe (`_CROSS_REGION_NICKNAME_ANCHOR_PROBE_QUERY`) replicates 01_05_10 MD
  §3.3 SQL 3 nickname-join idiom and asserts the 32,031 anchor. The 32,031 expectation is
  shared ONLY by the nickname-anchored probe; the toon_id-membership probe has its own
  independent expectation. Falsifier keys `cross_region_nickname_anchor_count_drift` and
  `cross_region_toon_id_anchor_count_drift` are independent.

A20. **(NEW round-3 NIT-D) `history_row_filter_on_pha_applied` is a structured field, not a
  prose substring.** The dataclass gains
  `history_row_filter_on_pha_applied: str ∈ ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED = frozenset({'yes', 'no', 'not_applicable'})`.
  Falsifier `_check_history_row_filter_on_pha_field_valid` (key
  `history_row_filter_on_pha_field_invalid`) asserts the field is in the allowed set AND
  enforces consistency with `selected_policy`:
  - Q5A (`strict_exclusion`) → `history_row_filter_on_pha_applied = "yes"` (required)
  - Q5B (`dual_feature_path`) → `history_row_filter_on_pha_applied = "yes"` (required)
  - Q5C (`sensitivity_indicator_co_registration`) → `history_row_filter_on_pha_applied = "no"` (required) — OR `"not_applicable"` is also allowed for Q5C since the option does not apply any filter; the planner BINDS `"no"` for Q5C as the more informative value
  - Q5_selected_policy → derived from chosen policy (mirror Q5A/Q5B/Q5C consistency)
  - Q5_per_family_impact_summary → `"not_applicable"` (no per-option commitment)

  The old vacuous substring assertion that required the prose `"history-row filter on PHA"`
  in every `retention_measurement_summary` is REMOVED. The SQL byte-scan portion of falsifier
  #24 (reject `mfc.is_cross_region_fragmented` as a WHERE predicate) is KEPT — that scan IS
  non-vacuous.

A21. **(NEW round-4 B4-only mechanical) Authoritative counts.** `HELPER_TO_FALSIFIER_KEY` and
  `FALSIFIER_PRIORITY_CHAIN` each contain **exactly 31 entries**; their value-set is equal
  (`set(FALSIFIER_PRIORITY_CHAIN) == set(HELPER_TO_FALSIFIER_KEY.values())`); the chain has no
  duplicates (`len(set(FALSIFIER_PRIORITY_CHAIN)) == 31`). The 31 = 25 (post-B4 mapping
  promotion) + 4 (NIT-B SHAs) + 2 (NIT-D structured-field + SQL-byte-scan split) arithmetic
  is authoritative; no alternative count is permitted. All four invariants are asserted at
  module-import time (via top-level `assert` statements per the
  `POST_GAME_TOKEN_SCOPED_FIELDS.isdisjoint(POST_GAME_TOKEN_EXEMPT_FIELDS)` precedent inherited
  from PR #242) so any drift fails BEFORE any test runs and BEFORE any artifact is written.

### Unknowns (DEFERRED with explicit gating)

U1. **Final Q5 verdict.** The Layer-2 PR may converge to any of:
  - `bind_now` / `binding_for_materialization` with one of the three policies selected and
    quantitative retention evidence per-family,
  - `narrow_with_evidence` (e.g., "select option (c) sensitivity-indicator co-registration as a
    BIND for materialization scope and option (a) strict-exclusion as a Phase-03 sensitivity
    arm"),
  - `deferred_recommendation` (rare; only if the measurement reveals a previously-unanticipated
    blocker — e.g., a fourth necessary option),
  - continued `deferred_blocker` (with strictly stronger evidence-required language than PR #242).

  The Layer-2 PR does NOT pre-commit to the verdict; the verdict emerges from the per-family
  retention table (per A14).

U2. **Magnitude tolerance for retention loss.** Per Invariant I7 (no magic numbers) the
  Layer-2 PR will NOT hard-code a "≥X% retention required" threshold. The decision rationale
  must be either (a) literature-cited or (b) compared against the W=30 noise-floor √30 ≈ 5.5
  precedent that 01_05_10 already grounds in literature (Hollander & Wolfe 1999 §11.2). The
  per-family retention numbers + their 01_05_10 noise-floor comparisons together drive the
  verdict; no scalar tolerance is committed.

U3. **G-CS-5 per-source cold-start enumeration row.** Q4 in PR #242 binds G-CS-2/3/4/5 as
  scaffold registry gates with G-CS-6 deferred to materialization. The Q5 verdict may produce a
  GCS-5 row count update if the selected option changes the cold-start cohort (e.g.,
  `strict_exclusion` raises the cold-start row count by removing players' historical PHA
  entries from the aggregate window — reducing prior-match counts at target time below the
  cold-start threshold). The Layer-2 PR may emit one auxiliary GCS-5-impact row in the
  successor CSV; this is NOT a Q4 re-adjudication — the PR #242 Q4 row remains the binding Q4
  record.

U4. **Phase 03 sensitivity-arm declaration.** If the verdict is `narrow_with_evidence` /
  `sensitivity_indicator_co_registration`, the Phase 03 sensitivity-arm protocol is RECORDED in
  the successor CSV (one row) but is NOT executed; Phase 03 work remains forbidden.

U5. **Materialization SQL.** The exact materialization projection SQL for the
  `cross_region_fragmentation_handling` family is DEFERRED to the future materialization PR.
  The Q5 successor CSV records the BINDING per-option per-family retention counts; the SQL
  skeleton is recorded only as a pseudocode pattern in the MD §rationale.

U6. **Q6 rating-family adjudication.** Explicitly DEFERRED to a separate future planning round.
  See Open Questions OQ1.

U7. **Step closure.** A U2.B-style closure PR (adding `02_01_03: complete` to `STEP_STATUS.yaml`
  and the closure entry to dataset `research_log.md`) remains DEFERRED to a separate
  post-materialization closure PR per PR #237 precedent.

U8. **AoE2 cross-game decisions.** This is a sc2egset-scoped successor adjudication.
  CROSS-02-00 cross-game decisions are RATIFIED-by-citation only; no new cross-game commitment.

U9. **PHA history-row anchor count.** The smoke-falsifier anchor for total PHA rows passing
  the `STRICT_LT_HISTORY_FILTER` over all 6 history families is TBD at Layer-2 write time
  (replaces the round-1 MFC-target-row 44418 anchor). The Layer-2 executor will compute the
  anchor from a one-time read-only probe over the current DuckDB during T01 and pin it as
  `EXPECTED_PHA_STRICT_LT_HISTORY_ROW_COUNT: int` per Invariant I7 (the constant must be
  derived from the live DuckDB and committed with provenance, NOT inserted as a magic number
  from this Layer-1 plan).

U10. **(NEW round-3 NIT-C) PHA toon_id-membership count anchor.** The new binding probe's
  expected count is TBD at Layer-2 write time:
  `EXPECTED_PHA_CROSS_REGION_TOONID_MEMBERSHIP_COUNT: int`. It is computed once via the
  toon_id-membership form (`SELECT COUNT(*) FROM player_history_all ph WHERE ph.toon_id IN
  (SELECT DISTINCT toon_id FROM player_history_all WHERE is_cross_region_fragmented = TRUE)`)
  on the live DuckDB, then pinned. It is conceptually distinct from the nickname-anchored
  32,031 count and may not equal 32,031 (the two probes may differ slightly if any
  cross-region toon_id has a PHA row where `LOWER(nickname)` is not in the cross-region
  nickname set, or vice versa — a subtle edge case the executor must verify in the
  T07 notebook output before pinning).

## Literature Context

This is a methodology-scaffolding adjudication PR. The literature context is the project's own
normative documents (cited verbatim in `source_artifacts`) plus the cross-spec invariants in
`.claude/scientific-invariants.md`.

**Verbatim spec passages anchoring the round-2 B3 filter-semantics binding (round-3 NIT-A
re-attribution: each quote is now sourced from its actual on-disk location and quoted byte-for-byte
from that location, not paraphrased across files):**

> [Source: `02_02_feature_engineering_plan.md` §6.2 row 5 line 242, Source column, verbatim]
>
> `player_history_all.is_cross_region_fragmented` (CROSS-02-00 §5.4)

> [Source: `02_02_feature_engineering_plan.md` §6.2 row 5 line 242, Constraint column, verbatim]
>
> Per RISK-20 / Phase 01 W=30 FAIL verdict, Phase 02 must not hard-code a retention percentage
> for `WHERE NOT is_cross_region_fragmented` filtering. Phase 02 must implement one of:
> (a) strict-exclusion sensitivity arm, (b) dual feature paths (with vs without filter), or
> (c) sensitivity indicator co-registered alongside the history features. The choice is
> deferred to a Phase 02 ROADMAP step that empirically measures retention.

> [Source: `01_04_05_cross_region_annotation.md` §7 strategy 1, lines 203-208, verbatim]
>
> Safe-subset filter: `WHERE NOT is_cross_region_fragmented` — restricts history to
> non-fragmented players; cleanest rolling-window estimates but reduces the training population
> to 7,716 / 44,817 rows = 17.2% of the corpus (tournament players are over-represented among
> the 1,923 flagged toons; see §4 flag distribution). This is a material data loss; strategy
> (2) or (3) are usually preferable for non-catastrophic bias levels.

> [Source: `01_04_05_cross_region_annotation.md` §7 strategies 2 and 3, lines 210-216,
> verbatim]
>
> 2. **Dual feature paths:** Compute rolling-window features for all players, then add
>    `is_cross_region_fragmented` as a covariate in the model. The model learns to adjust
>    for the known fragmentation bias.
>
> 3. **Sensitivity indicator:** Use the flag to partition evaluation metrics by
>    `is_cross_region_fragmented` and report differential model performance. Documents
>    remaining bias for the thesis.

> [Source: `player_history_all.yaml` NOTES lines 220-226, verbatim — this is the ONLY
> on-disk source for the consolidated paraphrase below; it does NOT appear in 01_04_05 §7
> in this consolidated form]
>
> Phase 02 rolling features over `player_id_worldwide` should apply
> `WHERE NOT is_cross_region_fragmented` as safe-subset filter, OR use dual feature paths,
> OR use as sensitivity indicator. Blanket flag (no handle-length filter) by design — false
> positives bounded by short-handle count (see 01_04_05 §6 conservatism argument). Empirical
> grounding from WP-3 (01_05_10): median_rolling30_undercount=16, p95=29 on flagged toons.
> Derivation in 01_04_05 artifact.

> [Source: `01_04_05_cross_region_annotation.md` §1 — the PHA column declaration]
>
> This step adds `is_cross_region_fragmented` BOOLEAN to `player_history_all` VIEW so Phase 02
> consumers can operationalize the accepted-bias framing without re-deriving the cross-region
> set per query.

All four passages prescribe the filter on the HISTORY view (PHA). None prescribe filtering
target rows on MFC. The Q5 successor module binds to the prescribed semantics only; the
MFC-target-row alternative is OUT OF SCOPE per A4 + A17.

**Must-justify list (methodological choices needing alternatives-considered paragraphs in the
future MD):**

- selection of `strict_exclusion` vs `dual_feature_path` vs `sensitivity_indicator_co_registration`
  per CROSS-02-02 §6.2 row 5 (verbatim Constraint-column wording above);
- decision to read `is_cross_region_fragmented` from `player_history_all` (per
  `player_history_all.yaml` line 214 + 01_04_05 §1 → PHA is the unique source-of-truth)
  versus the now-rejected (round-1 B1) alternative of reading from `matches_flat_clean` —
  MFC does NOT carry this column (verified `grep -n is_cross_region_fragmented
  matches_flat_clean.yaml` returns empty);
- decision to apply the filter to HISTORY rows on PHA (`WHERE NOT ph.is_cross_region_fragmented`
  before aggregation) versus the now-rejected (round-1 B3) alternative of filtering TARGET
  rows on MFC — neither 01_04_05 §7 strategy 1 (verbatim above) nor CROSS-02-02 §6.2 row 5
  Constraint column (verbatim above) enumerates the TARGET-row filter as one of the three
  options;
- decision to compute retention impact per-family (6 families × 3 options) versus a single
  global retention number;
- decision to use the 01_05_10 √30 ≈ 5.5 noise-floor as the comparator rather than a fresh
  literature-cited tolerance;
- **(NEW round-3 NIT-C) decision to use a toon_id-membership probe as the BINDING base
  count and reserve the nickname-anchored 01_05_10-equivalence probe (which yields 32,031)
  as the EXPLORATORY 01_05_10-equivalence check.** Justification: the downstream Q5 filter
  predicate is `WHERE ph.is_cross_region_fragmented = TRUE` (column-driven, anchored on the
  derived `toon_id`-membership flag), so the binding count must use the same idiom; the
  nickname-anchored count from 01_05_10 SQL 3 is conceptually equivalent but slightly less
  precise (it joins on lowercase nickname, which can drift if any PHA row's nickname casing
  diverges from `replay_players_raw`).

**Must-contrast list (claims needing literature comparison):**

- the 12% migration rate (SC-R01 in `risk_register_sc2egset.md`) vs the 23.5% nickname-level
  migration in 01_05_10 §3.1 (these are NOT contradictory — they count different cardinalities;
  the Layer-2 MD must state both and explain the difference);
- median-undercount 16 / p95-undercount 29 against the W=30 noise-floor √30 ≈ 5.5 (already
  cited from Hollander & Wolfe 1999 §11.2);
- per-option retention numbers against the I2-Branch-(iii) accepted-bias framing in
  `INVARIANTS.md` §2.

**Must-cite list (key references — verify presence in `thesis/references.bib` at Layer-2 write
time; if a citation is missing, escalate or downgrade the claim):**

- Hollander & Wolfe 1999 §11.2 (already used by 01_05_10; verify bib presence);
- de Prado 2018 Ch. 7 (normalization leakage; already cited in scientific-invariants.md I3);
- Arlot & Celisse 2010 (split methodology; already cited in I3).

None of these become Q5 binding citations on their own; they appear only as comparator
substrate in the rationale. The Q5 verdict itself is driven by the empirical retention table,
not by literature.

External web search is NOT expected for this PR; if a citation surfaces that isn't yet in
`thesis/references.bib`, the Layer-2 executor must escalate.

**Expected length.** The future Layer-2 MD is expected to run ~450-750 lines (between the
PR #234 MD at ~250 lines and the PR #242 MD at ~240 lines, plus the additional per-option ×
per-family retention table, the two-probe binding/exploratory split per NIT-C, and the
structured `history_row_filter_on_pha_applied` table per NIT-D). Voice: argumentative — every
per-option row must defend its inclusion against the alternatives, not merely describe its
retention number.

## Execution Steps

Each task below describes work to be performed by the future Layer-2 executor. T01-T08 produce
the **9 deliverable/execution files**; T09 is the Layer-2 final-gate dispatch. **None of
T01-T09 executes at this Layer-1 PR.**

### T01 — Adjudicator module: dataclasses, constants, schema constants

**Objective:** Define module-level constants, the `CrossRegionAdjudicationResult` frozen
dataclass, and the `CrossRegionAdjudicationDecision` frozen dataclass. No magic numbers
(Invariant I7).

**Instructions:**

1. Create `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py`.
2. Re-import `HISTORY_TRANCHE2_FAMILY_IDS`, `EXPECTED_TRANCHE2_COUNT`,
   `IN_GAME_HISTORICAL_AGGREGATED_COLUMNS`, `STRICT_LT_HISTORY_FILTER`,
   `POST_GAME_TOKENS`, `POST_GAME_TOKEN_SCOPED_FIELDS`, `POST_GAME_TOKEN_EXEMPT_FIELDS`,
   and `EXPECTED_PR241_VALIDATOR_SHA256` from the PR #241 validator module and the PR #242
   adjudicator module. Do NOT re-declare any of these constants — single source of truth.

3. Declare new module-level constants:
   - `Q5_DECISION_IDS: tuple[str, ...] = ("Q5A_strict_exclusion_retention", "Q5B_dual_feature_path_retention", "Q5C_sensitivity_indicator_retention", "Q5_selected_policy", "Q5_per_family_impact_summary")` — exactly 5 rows. `len(Q5_DECISION_IDS) == 5`.
   - `Q5_OPTION_NAMES: tuple[str, ...] = ("strict_exclusion", "dual_feature_path", "sensitivity_indicator_co_registration")`.
   - `EXPECTED_CROSS_REGION_NICKNAME_COUNT: int = 246` (anchor from 01_05_10 §3.1 + JSON `n_cross_region_nicknames`).
   - `EXPECTED_CROSS_REGION_TOON_ID_COUNT: int = 1923` (anchor from 01_04_05 + 01_05_10 MD §3.3).
   - `EXPECTED_CROSS_REGION_PLAYER_MATCH_PAIR_COUNT_NICKNAME_ANCHORED: int = 32031` (round-3 NIT-C rename — anchor from 01_05_10 MD §3.3 line 398; semantically a NICKNAME-anchored count, NOT a toon_id-membership count; bound only by the EQUIVALENCE probe).
   - `EXPECTED_PHA_CROSS_REGION_TOONID_MEMBERSHIP_COUNT: int` — TBD at Layer-2 write time via `_CROSS_REGION_TOONID_MEMBERSHIP_BASE_PROBE_QUERY` against the live DuckDB; pinned per Invariant I7 (round-3 NIT-C binding; this is the BINDING base probe expected count).
   - `EXPECTED_PHA_STRICT_LT_HISTORY_ROW_COUNT: int` — TBD at Layer-2 write time via a one-time read-only probe; pinned per Invariant I7 (round-2 U9 binding; replaces the round-1 MFC-target-row 44418 anchor).
   - `ALLOWED_Q5_VERDICTS: frozenset[str] = frozenset({"bind_now", "narrow_with_evidence", "deferred_recommendation", "deferred_blocker"})`.
   - `ALLOWED_Q5_BINDING_LEVELS: frozenset[str] = frozenset({"binding_for_materialization", "recommendation_only", "deferred_blocker"})`.
   - `CROSS_REGION_COLUMN_SOURCE_TABLE: str = "player_history_all"` (round-2 B1/A15 binding — single source-of-truth column declaration).
   - `CROSS_REGION_COLUMN_NAME: str = "is_cross_region_fragmented"`.
   - `ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS: frozenset[str] = frozenset({"toon_id_based", "nickname_based", "both"})` (round-3 NIT-C / A19 binding).
   - `ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED: frozenset[str] = frozenset({"yes", "no", "not_applicable"})` (round-3 NIT-D / A20 binding).
   - `PARENT_PR242_CSV_REL: str = "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv"`.
   - `PARENT_PR242_MD_REL: str = "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md"`.
   - `EXPECTED_PARENT_PR242_CSV_SHA256: str` and `EXPECTED_PARENT_PR242_MD_SHA256: str` — captured at Layer-2 write time via `shasum -a 256` (constants set to the verified 64-char lowercase hex; mismatch is a halting falsifier per T03).
   - `EXPECTED_01_05_10_MD_SHA256: str` and `EXPECTED_01_05_10_JSON_SHA256: str` — captured at Layer-2 write time.
   - **(NEW round-3 NIT-B) — 4 pinned SHA-256 module constants for the round-2-load-bearing source files. These are hardcoded at planner time (NOT TBD-at-Layer-2-write-time) so the executor does not have to re-derive them.** Pinned values per A18:
     - `EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256: str = "7962dd910e0b72419e35a9895689cd4ae6a51c2be0bc6e5e0fe4a0ceb8f207d0"`
     - `EXPECTED_01_04_05_MD_SHA256: str = "7bac26fd69952509a9dac323436e074902ca8ba9e0bac64021ad04de7f5dc9fe"`
     - `EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256: str = "9f76c1912624535b7b7ac0d2fb767fd4b9791a1d808bf73f747416d557d6cb1f"`
     - `EXPECTED_CROSS_02_02_SPEC_SHA256: str = "86af792370272e611f048aae0c48c9cc595eb4b44c1db38c0bb4ecea0ff1b289"`
     Each is a 64-char lowercase hex string (verified at planner-time 2026-05-24 on master HEAD `e372e7b66be66b6026fb3bc39f51d1975da0b8b1`). If any of these source files is touched between Layer-1 merge and Layer-2 execution, the matching helper in T03 halts; the executor must re-pin the constant and re-verify the round-2 B1/B3 binding rationale per A18.
   - `Q5_SUCCESSOR_CSV_REL: str = "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.csv"`.
   - `Q5_SUCCESSOR_MD_REL: str = "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.md"`.

4. Declare `CrossRegionAdjudicationDecision` frozen dataclass with the **28-field schema**
   (final CSV column count = 28 dataclass fields + `notes` = 29 columns; `wc -l` on the CSV =
   `6` = 1 header + 5 rows). Fields:
   - `decision_id: str` (one of Q5_DECISION_IDS)
   - `parent_decision_id: str` (literal `"Q5_cross_region_policy"` — **NEW field introduced by this successor PR per round-2 N1 fix; back-fillable into PR #242 via a future cosmetic chore PR, NOT in scope here**; verified `grep -c parent_decision_id <PR #242 CSV>` = 0)
   - `decision_name: str`
   - `verdict: str` (one of ALLOWED_Q5_VERDICTS)
   - `binding_level: str` (one of ALLOWED_Q5_BINDING_LEVELS)
   - `scope: str` (literal `"sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling"` for the per-option rows; `"all_six_history_enriched_pre_game_families"` for the per-family-impact summary)
   - `selected_policy: str` (one of Q5_OPTION_NAMES or `""` for evaluation-only rows)
   - `rejected_options: str` (newline-joined; for the Q5_selected_policy row only)
   - `cross_region_policy: str` (mirror of selected_policy for downstream materialization SQL keying; `""` for evaluation rows)
   - `cross_region_retention_counts: str` (JSON-string keyed by family_id with `{history_rows_kept, history_rows_dropped, retention_pct}` triples — round-2 B3 binding: counts are over PHA HISTORY ROWS, NOT MFC target rows; populated for the 3 per-option evaluation rows)
   - `cross_region_affected_players: int` (per-option distinct PHA `toon_id` count)
   - `cross_region_affected_matches: int` (per-option distinct MHM `match_id` count)
   - **`cross_region_anchor_semantics: str` (NEW round-3 NIT-C / A19 — one of ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS; binds the probe semantics per row)**
   - **`history_row_filter_on_pha_applied: str` (NEW round-3 NIT-D / A20 — one of ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED; structured machine-readable replacement for the round-2 vacuous substring assertion)**
   - `retention_measurement_summary: str` (one-sentence prose summary; mandatory; the round-2 verbatim-substring requirement is REPLACED by the structured `history_row_filter_on_pha_applied` field per A20)
   - `evidence_paths: str` (newline-joined repo paths; ≥3 paths required for any `bind_now`/`narrow_with_evidence` verdict)
   - `falsifiers: str` (newline-joined `helper_name:status` pairs; mirrors PR #242 format)
   - `audit_pr: str` (literal `"PR #<successor-PR-number>"` — set at Layer-2 PR-open time)
   - `pr241_scaffold_validator_module_sha256: str`
   - `parent_pr242_csv_sha256: str`
   - `parent_pr242_md_sha256: str`
   - `parent_pr242_artifact_sha256: str` (SHA-256 of the concatenated CSV+MD byte stream)
   - `provenance_01_05_10_md_sha256: str` (anchor to the 01_05_10 evidence)
   - **`player_history_all_yaml_sha256: str` (NEW round-3 NIT-B / A18)**
   - **`step_01_04_05_md_sha256: str` (NEW round-3 NIT-B / A18)**
   - **`matches_flat_clean_yaml_sha256: str` (NEW round-3 NIT-B / A18)**
   - **`cross_02_02_spec_sha256: str` (NEW round-3 NIT-B / A18)**
   - `materialized_output_paths: str` (always literal `""` — this is an adjudication, not a materialization)
   - + `notes: str` (free-text rationale; column 29)

5. Declare `CrossRegionAdjudicationResult` frozen dataclass with fields
   `decisions: tuple[CrossRegionAdjudicationDecision, ...]`, `csv_path: Path`, `md_path: Path`,
   `provenance_git_sha: str`.

6. Add explicit `FALSIFIER_PRIORITY_CHAIN: tuple[str, ...]` module-level constant ordering all
   halting falsifiers (per PR #242 round-3 N-R3-C precedent — module-level not in-function).
   See T04 step 2 for the full **31-entry** chain (per A21).

   **Module-import mechanical verification (round-4 B4 — caught at import time, NOT test
   time).** Immediately after `FALSIFIER_PRIORITY_CHAIN` and `HELPER_TO_FALSIFIER_KEY` are
   declared at module level, add the following four top-level `assert` statements (placed at
   module-load scope, mirroring the
   `POST_GAME_TOKEN_SCOPED_FIELDS.isdisjoint(POST_GAME_TOKEN_EXEMPT_FIELDS)` precedent
   inherited from PR #242 — so any drift in the count or duplicate or orphan chain entry
   raises `AssertionError` at `import` time and fails BEFORE any test runs and BEFORE any
   artifact is written):

   ```python
   # Module-import mechanical verification (round-4 B4 invariants; per A21).
   # These run at module load — drift fails before any test runs and before any artifact is written.
   assert len(HELPER_TO_FALSIFIER_KEY) == 31, "B4 invariant: helper count drifted"
   assert len(FALSIFIER_PRIORITY_CHAIN) == 31, "B4 invariant: chain count drifted"
   assert len(set(FALSIFIER_PRIORITY_CHAIN)) == 31, "B4 invariant: chain duplicates"
   assert set(FALSIFIER_PRIORITY_CHAIN) <= set(HELPER_TO_FALSIFIER_KEY.values()), \
       "B4 invariant: orphan chain entries"
   ```

   These four assertions are EQUIVALENT to T06's `TestHelperToFalsifierKeyMappingExactCount`
   + rewritten `TestPriorityChainReferencesMapping` but execute at module-import time so
   `python -c "import rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_cross_region_retention"`
   alone catches the drift.

7. Add explicit `HELPER_TO_FALSIFIER_KEY: dict[str, str]` literal table mapping each `_check_*`
   helper name to its falsifier key (per PR #242 round-3 N-X1 precedent). The mapping has
   **exactly 31 entries** per A21 (arithmetic: 25 entries post-B4 mapping promotion + 4 NIT-B
   SHA helpers + 2 NIT-D split helpers = 31). See T03 for the complete enumerated list and
   T04 for the chain ordering.

**Verification:** the module loads cleanly via
`python -c "from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_cross_region_retention import HISTORY_TRANCHE2_FAMILY_IDS, STRICT_LT_HISTORY_FILTER, Q5_DECISION_IDS, CROSS_REGION_COLUMN_SOURCE_TABLE, ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS, ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED, EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256, EXPECTED_01_04_05_MD_SHA256, EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256, EXPECTED_CROSS_02_02_SPEC_SHA256, HELPER_TO_FALSIFIER_KEY, FALSIFIER_PRIORITY_CHAIN; assert len(Q5_DECISION_IDS) == 5; assert 'strict_exclusion' not in STRICT_LT_HISTORY_FILTER; assert CROSS_REGION_COLUMN_SOURCE_TABLE == 'player_history_all'; assert ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS == frozenset({'toon_id_based','nickname_based','both'}); assert ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED == frozenset({'yes','no','not_applicable'}); assert len(EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256) == 64 and all(c in '0123456789abcdef' for c in EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256); assert len(HELPER_TO_FALSIFIER_KEY) == 31; assert len(FALSIFIER_PRIORITY_CHAIN) == 31; assert len(set(FALSIFIER_PRIORITY_CHAIN)) == 31; assert set(FALSIFIER_PRIORITY_CHAIN) <= set(HELPER_TO_FALSIFIER_KEY.values())"` runs without exception.

The four count/uniqueness/containment assertions above are ALSO enforced at module-import
time by the top-level `assert` block in step 6 — so even a bare
`python -c "import rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_cross_region_retention"`
will raise `AssertionError` on any drift, before any test runs.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_history_enriched_pre_game_materialization.py`
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_enriched_pre_game_source_layer.py`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml` (verify line 214 column name + lines 220-226 notes)
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml` (verify 30-col schema + absence of `is_cross_region_fragmented`)

### T02 — Adjudicator module: SQL probe constants (round-2 B1+B2+B3 + round-3 NIT-C two-probe rewrite)

**Objective:** Declare the read-only SQL probe constants (named per `python-code.md` `_QUERY`
suffix; UPPER_SNAKE_CASE) that drive the per-option × per-family retention measurements. All
probes read `is_cross_region_fragmented` from PHA (not MFC), apply the filter to HISTORY rows
(not TARGET rows), and use MFC's canonical `replay_id` / `toon_id` keys + MHM's canonical
`'sc2egset::'`-prefixed `match_id` (per A15, A16, A17). Round-3 NIT-C: TWO base probes —
one BINDING (toon_id-membership) and one EQUIVALENCE (nickname-anchored, replicating
01_05_10 SQL 3).

**Instructions:**

1. Declare `_CROSS_REGION_TOONID_MEMBERSHIP_BASE_PROBE_QUERY: str` (round-3 NIT-C — BINDING
   probe). Computes the toon_id-membership count: every PHA history row whose `toon_id` is
   in the set of cross-region toon_ids (anchored by the derived `is_cross_region_fragmented`
   flag itself). SQL (canonical; verbatim — no f-strings):

   ```sql
   -- BINDING base probe (round-3 NIT-C; anchor: toon_id-membership; expected count
   -- pinned at Layer-2 write time as EXPECTED_PHA_CROSS_REGION_TOONID_MEMBERSHIP_COUNT)
   SELECT COUNT(*) AS n_pha_rows_toonid_membership_anchored
   FROM player_history_all ph
   WHERE ph.toon_id IN (
     SELECT DISTINCT toon_id
     FROM player_history_all
     WHERE is_cross_region_fragmented = TRUE
   )
   ```

   Falsifier `cross_region_toon_id_anchor_count_drift`: halts if observed count differs from
   `EXPECTED_PHA_CROSS_REGION_TOONID_MEMBERSHIP_COUNT`. The expected count is TBD at Layer-2
   write time (U10).

2. Declare `_CROSS_REGION_NICKNAME_ANCHOR_PROBE_QUERY: str` (round-3 NIT-C — EQUIVALENCE
   probe). Replicates the 01_05_10 MD §3.3 SQL 3 idiom (nickname-anchored join over PHA) and
   asserts the 32,031 anchor. SQL (canonical; verbatim — no f-strings):

   ```sql
   -- EQUIVALENCE base probe (round-3 NIT-C; anchor: lowercase nickname; expected count
   -- 32031 per 01_05_10 MD §3.3 line 398; this probe is EXPLORATORY/equivalence-check,
   -- NOT the binding probe). Replicates 01_05_10 SQL 3 idiom verbatim.
   WITH cross_region_nicks AS (
     SELECT LOWER(nickname) AS nick
     FROM replay_players_raw
     GROUP BY 1
     HAVING COUNT(DISTINCT region) > 1
   )
   SELECT
     (SELECT COUNT(*) FROM cross_region_nicks) AS n_cross_region_nicknames,
     (SELECT COUNT(DISTINCT ph.toon_id)
        FROM player_history_all ph
        WHERE ph.is_cross_region_fragmented = TRUE) AS n_cross_region_toon_ids,
     (SELECT COUNT(*)
        FROM player_history_all ph
        INNER JOIN cross_region_nicks crn ON LOWER(ph.nickname) = crn.nick
        WHERE ph.details_timeUTC IS NOT NULL) AS n_player_match_pairs_nickname_anchored
   ```

   Falsifier `cross_region_nickname_anchor_count_drift`: halts if any of the 3 counts
   differs from `(EXPECTED_CROSS_REGION_NICKNAME_COUNT,
   EXPECTED_CROSS_REGION_TOON_ID_COUNT, EXPECTED_CROSS_REGION_PLAYER_MATCH_PAIR_COUNT_NICKNAME_ANCHORED)` =
   `(246, 1923, 32031)`. **The 32,031 expectation is shared ONLY by this nickname-anchored
   probe.** The toon_id-membership BINDING probe in step 1 has its own independent expected
   count (which may differ slightly from 32,031 — see U10).

3. Declare `_STRICT_EXCLUSION_HISTORY_FILTER_RETENTION_QUERY: str` — per-family retention under
   option (a). **Round-2 B3 binding: filter `WHERE NOT ph.is_cross_region_fragmented` is
   applied to PHA HISTORY rows BEFORE aggregation; NO `mfc.is_cross_region_fragmented` filter
   anywhere.** For each of the 6 history families, count
   `(history_rows_kept, history_rows_dropped, players_affected, matches_affected)`. SQL pattern:

   ```sql
   WITH base AS (
     SELECT
       target.match_id      AS target_match_id,        -- 'sc2egset::' || mfc.replay_id
       target.player_id     AS target_player,          -- mfc.toon_id
       target.started_at,                              -- TIMESTAMP via TRY_CAST
       ph.replay_id         AS history_replay_id,
       ph.toon_id           AS history_toon_id,
       ph.details_timeUTC   AS history_time,
       ph.is_cross_region_fragmented AS history_is_xr,
       <family_specific_columns from ph>
     FROM matches_flat_clean mfc
     JOIN matches_history_minimal target
       ON target.match_id  = 'sc2egset::' || mfc.replay_id      -- A16
      AND target.player_id = mfc.toon_id                         -- A16
     LEFT JOIN player_history_all ph
       ON ph.toon_id = mfc.toon_id
      AND TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at  -- A5
   )
   SELECT
     '<family_id>' AS family_id,
     COUNT(*) FILTER (WHERE history_is_xr = FALSE) AS history_rows_kept,
     COUNT(*) FILTER (WHERE history_is_xr = TRUE)  AS history_rows_dropped,
     COUNT(DISTINCT history_toon_id) FILTER (WHERE history_is_xr = TRUE) AS players_affected,
     COUNT(DISTINCT target_match_id) FILTER (WHERE history_is_xr = TRUE) AS matches_affected
   FROM base
   GROUP BY family_id
   ```

   Falsifier `strict_exclusion_history_filter_retention_smoke_failed`: halts if
   `history_rows_kept + history_rows_dropped != EXPECTED_PHA_STRICT_LT_HISTORY_ROW_COUNT` for
   any family (round-2 U9 binding).

4. Declare `_DUAL_FEATURE_PATH_RETENTION_QUERY: str` — option (b): no history rows dropped,
   but per-family the materialized columns split into `xr_*` and `nonxr_*` PHA-history-derived
   variants. All joins use A16 keys. Filter is again applied to PHA history rows per A17:
   one CTE splits PHA rows on `ph.is_cross_region_fragmented` and computes per-target-match
   per-branch counts.

5. Declare `_SENSITIVITY_INDICATOR_RETENTION_QUERY: str` — option (c): no history rows
   dropped, no per-family branch split; a single `is_cross_region_fragmented` flag is
   co-registered from PHA at the target-time anchor. Probe verifies the flag is non-degenerate
   on PHA AND target-time-anchored (Invariant I3). The co-registration semantics is "for each
   target row, project the maximum or boolean-OR of `ph.is_cross_region_fragmented` over the
   player's strictly-prior PHA history window per `STRICT_LT_HISTORY_FILTER`".

6. Declare `_FAMILY_LEVEL_IMPACT_QUERY: str` — produces the per-family-impact summary row's
   `cross_region_retention_counts` JSON payload by stacking the three per-option probes. All
   probes operate on PHA history rows (B3); JSON keys are family_ids; values are
   `{history_rows_kept, history_rows_dropped, retention_pct}` triples.

7. Every query uses `STRICT_LT_HISTORY_FILTER` for any join over `player_history_all` (B-X2
   inherited canonical form); the literal string `ph.details_timeUTC < target.started_at`
   (bare lex form) MUST NOT appear in any executable site (declare `STRICT_LT_FILTER_ROADMAP_RAW`
   for the provenance-only constant per PR #242 round-3 N-X1 precedent; falsifier
   `strict_lt_filter_divergence` byte-scans the module).

8. **Round-2 B1 binding — no `mfc.is_cross_region_fragmented` anywhere.** Every executable
   SQL string in the module must satisfy `grep -E "mfc\.is_cross_region_fragmented"` = 0
   lines. Falsifier `_check_no_mfc_cross_region_column_reference` (key
   `mfc_cross_region_column_referenced`) byte-scans the module.

9. **Round-2 B3 + round-3 NIT-D binding — no `mfc.is_cross_region_fragmented` as a filter
   predicate.** The SQL byte-scan portion of falsifier
   `_check_q5_filter_target_is_pha_history_sql` (key
   `q5_filter_target_is_pha_history_violated_sql`) ensures every WHERE clause referencing
   `is_cross_region_fragmented` anchors on the `ph.` alias (NOT on `mfc.`). The R2 vacuous
   prose-substring assertion is REMOVED; structured `history_row_filter_on_pha_applied` field
   handles the decision-row semantics per NIT-D / A20.

**Verification:**
- `grep -E "ph\.details_timeUTC\s*<\s*target\.started_at" src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` returns ONLY the named constant `STRICT_LT_FILTER_ROADMAP_RAW`'s declaration line.
- `grep -E "mfc\.is_cross_region_fragmented" src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` returns 0 hits.
- `grep -E "mfc\.match_id|mfc\.player_id" src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` returns 0 hits.
- `grep -E "'sc2egset::' \|\| mfc\.replay_id" src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` returns ≥ 1 hit.
- `grep -E "WHERE NOT ph\.is_cross_region_fragmented|FILTER \(WHERE history_is_xr" src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` returns ≥ 1 hit.
- `grep -E "ph\.toon_id IN \(\s*SELECT DISTINCT toon_id\s+FROM player_history_all\s+WHERE is_cross_region_fragmented = TRUE" src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` returns ≥ 1 hit (round-3 NIT-C BINDING probe).
- `grep -E "INNER JOIN cross_region_nicks crn ON LOWER\(ph\.nickname\) = crn\.nick" src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` returns ≥ 1 hit (round-3 NIT-C EQUIVALENCE probe).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_05_cross_region_annotation.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/cross_region_history_impact_sc2egset.md` (verify §3.3 line 398 32,031 anchor + SQL 3 nickname-anchored idiom)
- `reports/specs/02_02_feature_engineering_plan.md`

### T03 — Adjudicator module: halting falsifier helpers (31 helpers total)

**Objective:** Implement every `_check_*` helper named in `HELPER_TO_FALSIFIER_KEY`. Each helper
is a pure function returning a value the public entrypoint consumes; halting is the
entrypoint's responsibility (helpers never raise).

**The 31-entry mapping and 31-entry priority chain are authoritative. See module-import
verification at T01 step 6.** Every falsifier in the priority chain has:

1. A helper implementation in this T03 (or a documented inline check in T04);
2. A mapping entry in `HELPER_TO_FALSIFIER_KEY`;
3. At least one positive or negative test in T06 (unless explicitly marked non-testable with
   justification in the helper docstring).

**Instructions — the complete 31-helper enumeration (post-B4 + NIT-B + NIT-C + NIT-D, per
A21 arithmetic 25 + 4 + 2 = 31):**

1. `_check_parent_pr242_csv_sha256(csv_path: Path) -> str | None` — halting key `parent_pr242_csv_sha256_mismatch`.
2. `_check_parent_pr242_md_sha256(md_path: Path) -> str | None` — key `parent_pr242_md_sha256_mismatch`.
3. `_check_pr241_validator_sha256(validator_path: Path) -> str | None` — key `pr241_sha256_mismatch`.
4. `_check_01_05_10_evidence_sha256_md(md_path: Path) -> str | None` — key `cross_region_01_05_10_md_sha256_mismatch`.
5. `_check_01_05_10_evidence_sha256_json(json_path: Path) -> str | None` — key `cross_region_01_05_10_json_sha256_mismatch`.
6. **(NEW round-3 NIT-B)** `_check_player_history_all_yaml_sha256(yaml_path: Path) -> str | None` — re-computes `shasum -a 256` on `player_history_all.yaml`; returns None on match against `EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256`, else returns observed digest; key `player_history_all_yaml_sha256_mismatch`. Rationale: round-2 B1/A15 binding rationale hinges on PHA's line-214 column declaration + lines 220-226 NOTES; silent drift would invalidate the binding.
7. **(NEW round-3 NIT-B)** `_check_step_01_04_05_md_sha256(md_path: Path) -> str | None` — key `step_01_04_05_md_sha256_mismatch`. Rationale: round-2 B3 binding rationale hinges on §7 strategy 1 wording at lines 203-208; silent drift would invalidate the binding.
8. **(NEW round-3 NIT-B)** `_check_matches_flat_clean_yaml_sha256(yaml_path: Path) -> str | None` — key `matches_flat_clean_yaml_sha256_mismatch`. Rationale: round-2 B1 binding rationale hinges on MFC's 30-col schema + absence of `is_cross_region_fragmented`; silent drift would invalidate the binding.
9. **(NEW round-3 NIT-B)** `_check_cross_02_02_spec_sha256(md_path: Path) -> str | None` — key `cross_02_02_spec_sha256_mismatch`. Rationale: round-2 B3 binding rationale hinges on §6.2 row 5 line 242 Source/Constraint columns; silent drift would invalidate the binding.
10. `_check_no_mfc_cross_region_column_reference(module_path: Path) -> tuple[str, ...]` — byte-scans the module for `mfc.is_cross_region_fragmented`; key `mfc_cross_region_column_referenced` (round-2 B1).
11. `_check_cross_region_toonid_anchor_count_drift(con: duckdb.DuckDBPyConnection) -> int` (round-3 NIT-C BINDING probe) — runs `_CROSS_REGION_TOONID_MEMBERSHIP_BASE_PROBE_QUERY`; halts if count differs from `EXPECTED_PHA_CROSS_REGION_TOONID_MEMBERSHIP_COUNT`; key `cross_region_toon_id_anchor_count_drift`.
12. `_check_cross_region_nickname_anchor_count_drift(con: duckdb.DuckDBPyConnection) -> tuple[int, int, int]` (round-3 NIT-C EQUIVALENCE probe) — runs `_CROSS_REGION_NICKNAME_ANCHOR_PROBE_QUERY`; asserts the 246/1923/32031 anchor counts; key `cross_region_nickname_anchor_count_drift`. **32,031 is bound here only.**
13. `_check_strict_lt_filter_divergence(module_path: Path) -> tuple[str, ...]` — byte-scans for bare `ph.details_timeUTC < target.started_at` outside `STRICT_LT_FILTER_ROADMAP_RAW`; key `strict_lt_filter_divergence`.
14. **(NEW round-3 B4 — promoted from chain-only to mapping)** `_check_decision_count(decisions: tuple[CrossRegionAdjudicationDecision, ...]) -> int` — asserts `len(decisions) == 5`; key `decision_count_drift`.
15. `_check_q5_three_options_enumerated(decisions: tuple[...]) -> tuple[str, ...]` — asserts the three per-option rows are exactly `Q5_OPTION_NAMES` (no fourth option, explicitly no `mfc_target_row_drop` per A4); key `q5_three_options_not_enumerated`.
16. `_check_strict_exclusion_history_filter_retention_smoke(con: duckdb.DuckDBPyConnection) -> tuple[tuple[str, int, int], ...]` — runs `_STRICT_EXCLUSION_HISTORY_FILTER_RETENTION_QUERY` per family; returns triples; key `strict_exclusion_history_filter_retention_smoke_failed` (round-2 B3 + U9).
17. `_check_dual_feature_path_branches_nondegenerate(con: duckdb.DuckDBPyConnection) -> tuple[str, ...]` — key `dual_feature_path_branch_degenerate`.
18. `_check_sensitivity_indicator_flag_nondegenerate(con: duckdb.DuckDBPyConnection) -> tuple[int, int]` — key `sensitivity_indicator_flag_degenerate`.
19. `_check_sensitivity_indicator_anchor_target_time(decision_row: CrossRegionAdjudicationDecision) -> bool` — asserts the sensitivity-indicator row notes contain `"anchored at target.started_at"` and do NOT contain any POST_GAME_TOKEN in `POST_GAME_TOKEN_SCOPED_FIELDS`; key `sensitivity_indicator_post_game_token_in_scoped_field`.
20. `_check_q5_evidence_sufficiency(decisions: tuple[...]) -> tuple[str, ...]` — for `bind_now`/`narrow_with_evidence` rows asserts `evidence_paths` has ≥3 paths matching `^(src/|reports/|sandbox/|thesis/|tests/|docs/|\.claude/)`; for `deferred_blocker` asserts `notes` contains `"deferred_blocker because:"`; key `q5_evidence_sufficiency_violated`.
21. `_check_q5_no_post_game_token_in_scoped_fields(decisions: tuple[...]) -> tuple[tuple[str, str], ...]` — scans scoped fields for POST_GAME_TOKENS; key `q5_post_game_token_in_scoped_field`. `POST_GAME_TOKEN_EXEMPT_FIELDS` exempted.
22. `_check_q5_no_direct_target_match_outcome(decisions: tuple[...]) -> bool` — asserts no decision row's scoped fields reference target-match `result`/`winner`/`won`/`outcome`/`final_state`; key `q5_direct_target_match_outcome_referenced`.
23. `_check_q5_no_future_match_leakage(decisions: tuple[...]) -> bool` — key `q5_future_match_leakage_referenced`.
24. `_check_q5_no_global_batch_fit(decisions: tuple[...]) -> bool` — key `q5_global_batch_fit_referenced`.
25. `_check_q5_no_phase_03_baseline_creep(decisions: tuple[...]) -> bool` — key `q5_phase_03_baseline_creep`.
26. **(NEW round-3 B4 — promoted from chain-only to mapping)** `_check_materialization_creep(decisions: tuple[...]) -> bool` — asserts every decision row's `materialized_output_paths == ""`; key `materialization_creep`.
27. `_check_no_status_yaml_change(repo_root: Path) -> bool` — key `status_yaml_drift`.
28. `_check_no_research_log_change(repo_root: Path) -> bool` — key `research_log_drift`.
29. `_check_no_q6_artifact_change(decisions: tuple[...]) -> bool` — asserts no decision row's `parent_decision_id == "Q6_rating_policy"` AND no Q6 wording outside the one-line disclaimer; key `q6_scope_creep`.
30. **(NEW round-3 NIT-D — replaces the R2 vacuous text-presence falsifier)** `_check_history_row_filter_on_pha_field_valid(decisions: tuple[...]) -> tuple[str, ...]` — TWO assertions per decision row:
    - the `history_row_filter_on_pha_applied` value is in `ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED`;
    - the value is consistent with `selected_policy`:
      - if `selected_policy == "strict_exclusion"` then required `"yes"`
      - if `selected_policy == "dual_feature_path"` then required `"yes"`
      - if `selected_policy == "sensitivity_indicator_co_registration"` then required `"no"` (the planner BINDS `"no"` for Q5C; the spec also allows `"not_applicable"` but the planner-mandated value is `"no"`)
      - if `selected_policy == ""` and `decision_id == "Q5_per_family_impact_summary"` then required `"not_applicable"`
      - for the Q5_selected_policy row, the value must match whichever policy is chosen (derived consistency)
    - key `history_row_filter_on_pha_field_invalid`.
31. **(NEW round-3 NIT-D — the SQL byte-scan portion KEPT from R2 falsifier #24)** `_check_q5_filter_target_is_pha_history_sql(module_path: Path) -> tuple[str, ...]` — byte-scans the module for any `WHERE.*is_cross_region_fragmented` predicate and ensures it is anchored on `ph.` alias (NOT on `mfc.`); key `q5_filter_target_is_pha_history_violated_sql`. The OLD R2 prose-substring assertion is REMOVED (superseded by helper #30's structured-field check).

**Verification:** `python -c "from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_cross_region_retention import HELPER_TO_FALSIFIER_KEY, FALSIFIER_PRIORITY_CHAIN; assert len(HELPER_TO_FALSIFIER_KEY) == 31; assert len(FALSIFIER_PRIORITY_CHAIN) == 31; assert set(FALSIFIER_PRIORITY_CHAIN) == set(HELPER_TO_FALSIFIER_KEY.values()); assert len(set(FALSIFIER_PRIORITY_CHAIN)) == len(FALSIFIER_PRIORITY_CHAIN)"` runs without exception. (Note: per T01 step 6 the same invariants are also enforced at module-import time, so any drift fails BEFORE this verification command runs.)

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py`

### T04 — Adjudicator module: public entrypoint + 31-entry priority chain

**Objective:** Wire the helpers into the public entrypoint, in deterministic priority order;
halt on first failure with the human-readable falsifier key from `HELPER_TO_FALSIFIER_KEY`.

**Instructions:**

1. Implement `adjudicate_history_cross_region_retention(registry_csv_path: Path, parent_pr242_csv_path: Path, parent_pr242_md_path: Path, pr241_validator_path: Path, evidence_md_path: Path, evidence_json_path: Path, player_history_all_yaml_path: Path, step_01_04_05_md_path: Path, matches_flat_clean_yaml_path: Path, cross_02_02_spec_path: Path, duckdb_path: Path, csv_output_path: Path, md_output_path: Path, provenance_git_sha: str) -> CrossRegionAdjudicationResult`. Note the four added NIT-B path arguments.

2. Define `FALSIFIER_PRIORITY_CHAIN` ordering (module-level constant; never in-function; per PR #242 round-3 N-R3-C precedent; **31 entries total** per A21):
   1. `parent_pr242_csv_sha256_mismatch`
   2. `parent_pr242_md_sha256_mismatch`
   3. `pr241_sha256_mismatch`
   4. `cross_region_01_05_10_md_sha256_mismatch`
   5. `cross_region_01_05_10_json_sha256_mismatch`
   6. **(NEW round-3 NIT-B)** `player_history_all_yaml_sha256_mismatch`
   7. **(NEW round-3 NIT-B)** `step_01_04_05_md_sha256_mismatch`
   8. **(NEW round-3 NIT-B)** `matches_flat_clean_yaml_sha256_mismatch`
   9. **(NEW round-3 NIT-B)** `cross_02_02_spec_sha256_mismatch`
   10. `mfc_cross_region_column_referenced` (round-2 B1 — earliest module-byte-scan)
   11. `cross_region_toon_id_anchor_count_drift` (round-3 NIT-C BINDING probe)
   12. `cross_region_nickname_anchor_count_drift` (round-3 NIT-C EQUIVALENCE probe)
   13. `strict_lt_filter_divergence`
   14. **(NEW round-3 B4 — promoted)** `decision_count_drift`
   15. `q5_three_options_not_enumerated`
   16. `strict_exclusion_history_filter_retention_smoke_failed`
   17. `dual_feature_path_branch_degenerate`
   18. `sensitivity_indicator_flag_degenerate`
   19. `sensitivity_indicator_post_game_token_in_scoped_field`
   20. `q5_evidence_sufficiency_violated`
   21. `q5_post_game_token_in_scoped_field`
   22. `q5_direct_target_match_outcome_referenced`
   23. `q5_future_match_leakage_referenced`
   24. `q5_global_batch_fit_referenced`
   25. `q5_phase_03_baseline_creep`
   26. **(NEW round-3 NIT-D structured-field check)** `history_row_filter_on_pha_field_invalid`
   27. **(NEW round-3 NIT-D SQL byte-scan; round-2 B3 inherited)** `q5_filter_target_is_pha_history_violated_sql`
   28. **(NEW round-3 B4 — promoted)** `materialization_creep`
   29. `status_yaml_drift`
   30. `research_log_drift`
   31. `q6_scope_creep`

3. Helpers run strictly in `FALSIFIER_PRIORITY_CHAIN` order; on first non-pass, the entrypoint
   raises `Q5AdjudicationFalsifierError` with `falsifier_key` + `observed` + `expected`.

4. Helpers 1-13 run before any decision-row assembly (module-level byte scans + SHA verifications
   + DuckDB anchor probes). Helpers 14-31 run after decision-row assembly but before
   write-to-disk.

5. CSV is written via `_write_csv` (csv module; quoting=QUOTE_MINIMAL; deterministic field
   order = dataclass field order). MD is written via `_write_md` (jinja-free f-strings; every
   SQL probe + numeric result quoted verbatim per Invariant I6).

6. The entrypoint resolves `provenance_git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"])` at call time if the caller does not pass it.

**Verification:**
- running the entrypoint against synthetic fixtures (per T06) produces a 5-row CSV with `wc -l == 6`;
- `len(FALSIFIER_PRIORITY_CHAIN) == 31` and `len(HELPER_TO_FALSIFIER_KEY) == 31`;
- `set(FALSIFIER_PRIORITY_CHAIN) == set(HELPER_TO_FALSIFIER_KEY.values())`;
- `len(set(FALSIFIER_PRIORITY_CHAIN)) == len(FALSIFIER_PRIORITY_CHAIN)` (no duplicate chain entries).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py`

### T05 — Per-decision binding (the substantive Q5 content)

**Objective:** Pre-author the decision rows the entrypoint must produce, verbatim, with
**provisional** recommended verdicts. **Round-2 N3 binding: the verdict EMERGES from the
per-family retention table — the executor MUST report the table BEFORE selecting any policy
and MUST escalate to the planner if the table contradicts the provisional recommendation.**

**Instructions for the executor:**

1. **Q5A_strict_exclusion_retention** — evaluation row for option (a):
   - `verdict = "deferred_recommendation"`
   - `binding_level = "recommendation_only"`
   - `scope = "sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling"`
   - `selected_policy = ""`
   - `cross_region_policy = "strict_exclusion"`
   - `cross_region_anchor_semantics = "toon_id_based"` (round-3 NIT-C / A19)
   - `history_row_filter_on_pha_applied = "yes"` (round-3 NIT-D / A20)
   - `cross_region_retention_counts` populated from `_STRICT_EXCLUSION_HISTORY_FILTER_RETENTION_QUERY` execution (round-2 B3: counts measure PHA HISTORY rows kept/dropped under `WHERE NOT ph.is_cross_region_fragmented` applied BEFORE aggregation)
   - `cross_region_affected_players` = DuckDB-returned distinct PHA `toon_id` count
   - `cross_region_affected_matches` = DuckDB-returned distinct MHM `match_id` count
   - `retention_measurement_summary` = "Strict exclusion (`WHERE NOT ph.is_cross_region_fragmented` applied to PHA HISTORY rows BEFORE aggregation, per round-2 B3 binding) drops X PHA history rows / Y players / Z target matches at the aggregation layer; retention pct per family: {focal_player_history: A%, opponent_player_history: B%, ...}." (X/Y/Z/A%/B% are TODOs at the Layer-1 plan stage; Layer-2 executor fills them from real DuckDB output)
   - `notes` includes:
     - **VERBATIM CROSS-02-02 §6.2 row 5 line 242 Source-column quote** (round-3 NIT-A — exact on-disk wording): `` `player_history_all.is_cross_region_fragmented` (CROSS-02-00 §5.4) `` — anchors the column source to PHA;
     - **VERBATIM CROSS-02-02 §6.2 row 5 line 242 Constraint-column quote** (round-3 NIT-A): "Phase 02 must implement one of: (a) strict-exclusion sensitivity arm, (b) dual feature paths (with vs without filter), or (c) sensitivity indicator co-registered alongside the history features."
     - **VERBATIM 01_04_05 §7 strategy 1 lines 203-208 quote** (round-3 NIT-A — exact on-disk wording): "Safe-subset filter: `WHERE NOT is_cross_region_fragmented` — restricts history to non-fragmented players; cleanest rolling-window estimates but reduces the training population to 7,716 / 44,817 rows = 17.2% of the corpus..."
     - **VERBATIM PHA YAML NOTES lines 220-226 quote** (round-3 NIT-A — the only on-disk source of the consolidated paraphrase): "Phase 02 rolling features over `player_id_worldwide` should apply `WHERE NOT is_cross_region_fragmented` as safe-subset filter, OR use dual feature paths, OR use as sensitivity indicator..."
     - rationale comparing retention loss against 01_05_10 W=30 noise-floor √30 ≈ 5.5 (Hollander & Wolfe 1999 §11.2);
     - explicit per-family count attribution;
     - explicit statement "no target-match outcome read; no future matches read; no global batch fit; deterministic SQL probe via `_STRICT_EXCLUSION_HISTORY_FILTER_RETENTION_QUERY`";
     - explicit reference to RISK-20 in `risk_register_sc2egset.md` (SC-R01 row) and to the
       `methodology_risk_register.md` path-discrepancy note (OQ2);
     - explicit non-substitution language: "this row replaces the empirical part of PR #242 Q5 only; the binding policy is the Q5_selected_policy row".

2. **Q5B_dual_feature_path_retention** — evaluation row for option (b):
   - symmetric to Q5A but with per-family `xr_branch_count` / `nonxr_branch_count` counts measured over PHA history rows
   - `cross_region_anchor_semantics = "toon_id_based"`
   - `history_row_filter_on_pha_applied = "yes"` (both arms filter, with within-region and cross-region splits)
   - `retention_measurement_summary` notes that history-row retention is 100% but per-branch sparsity may produce degenerate sub-features

3. **Q5C_sensitivity_indicator_retention** — evaluation row for option (c):
   - history-row retention is 100% (no PHA rows dropped); measurement adds a single `is_cross_region_fragmented` flag co-registered alongside the 6 history feature columns, projected from PHA at the target-time anchor per `STRICT_LT_HISTORY_FILTER`.
   - `cross_region_retention_counts` is `{"all_six_families": {"history_rows_kept": <pha_count>, "history_rows_dropped": 0, "retention_pct": 100.0}}`
   - `cross_region_anchor_semantics = "toon_id_based"`
   - `history_row_filter_on_pha_applied = "no"` (round-3 NIT-D / A20 — no filter applied; co-registration only)
   - `retention_measurement_summary` describes co-registration semantics without using the round-2 vacuous substring (NIT-D replaces it with the structured field above)

4. **Q5_selected_policy** — the binding row:
   - `verdict` = ONE of `"bind_now"` / `"narrow_with_evidence"` / `"deferred_recommendation"` / `"deferred_blocker"` — chosen by the executor AFTER running probes and reporting the per-family retention table per A14. **The planner's recommended verdict is provisional `narrow_with_evidence`** with `selected_policy = "sensitivity_indicator_co_registration"` (option (c)), `rejected_options = "strict_exclusion\ndual_feature_path"`, and provisional rationale: option (c) preserves full history-row retention while honoring the 01_05_10 FAIL verdict by providing the sensitivity-arm input the Phase 03 model can use to stratify; option (a) discards `history_rows_dropped` PHA rows whose cardinality the probe will quantify; option (b) introduces per-branch PHA sparsity that defeats the smoothing motivation of `matchup_history_aggregate` (G-CS-3).
   - **Round-2 N3 binding: this recommendation is PROVISIONAL. The Layer-2 executor MUST:**
     - **report the per-family retention table FIRST (from the three per-option probes) in the notebook output;**
     - **the verdict is computed from the table, not pre-bound from this plan;**
     - **if the probe shows option (c) introduces a `> 0` retention loss, the executor MUST downgrade to `deferred_blocker` and halt before write;**
     - **if the probe shows option (a) introduces a retention loss within (e.g.) 1× the W=30 noise-floor √30 ≈ 5.5, the executor MUST re-evaluate the provisional recommendation and MAY escalate to the planner;**
     - **the executor CANNOT silently rubber-stamp the provisional recommendation.**
   - `binding_level = "binding_for_materialization"` if `verdict == "bind_now"`; `"recommendation_only"` if `narrow_with_evidence`; `"deferred_blocker"` if `deferred_blocker`.
   - `selected_policy = <one of Q5_OPTION_NAMES>` or `""` for deferred verdicts.
   - `cross_region_anchor_semantics = "toon_id_based"`
   - `history_row_filter_on_pha_applied` = mirror of chosen `selected_policy`'s field value (or `"not_applicable"` if `verdict in {"deferred_recommendation", "deferred_blocker"}`)
   - `notes` includes:
     - per-option rejection rationale citing the per-family retention table verbatim;
     - explicit "MATERIALIZATION GATE" statement;
     - **explicit "VERDICT EMERGED FROM TABLE" attestation per A14;**
     - explicit acknowledgment that the MFC-target-row drop alternative is OUT OF SCOPE per A4 + A17.
   - `evidence_paths` includes (≥3): the 01_05_10 MD, 01_05_10 JSON, 01_04_05 cross-region annotation MD, risk register MD, CROSS-02-02 spec, parent PR #242 CSV, and **the 4 round-3 NIT-B source files** (PHA YAML, 01_04_05 MD, MFC YAML, CROSS-02-02 spec).

5. **Q5_per_family_impact_summary** — derived summary row:
   - `verdict = "ratify_with_evidence"`
   - `binding_level = "binding_for_materialization"`
   - `scope = "all_six_history_enriched_pre_game_families"`
   - `cross_region_anchor_semantics = "both"` (carries data from both probes)
   - `history_row_filter_on_pha_applied = "not_applicable"` (round-3 NIT-D / A20)
   - `cross_region_retention_counts` carries the JSON payload combining the three per-option probes per family. Round-2 B3: all retention counts in this JSON are over PHA HISTORY ROWS.

**Verification:**
- the 5 row IDs match `Q5_DECISION_IDS` exactly;
- the SQL probe results in `cross_region_retention_counts` match the values reproduced verbatim in the MD §evidence;
- the chosen `verdict` in `Q5_selected_policy` is one of `ALLOWED_Q5_VERDICTS`;
- every per-option row's `cross_region_anchor_semantics` is in `ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS` (asserted by NIT-C);
- every per-option row's `history_row_filter_on_pha_applied` is in `ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED` AND consistent with `selected_policy` (asserted by helper #30 / NIT-D);
- the MD §rationale contains the FOUR verbatim quotes per NIT-A re-attribution (CROSS-02-02 line 242 Source column + CROSS-02-02 line 242 Constraint column + 01_04_05 §7 strategy 1 lines 203-208 + PHA YAML NOTES lines 220-226).

**File scope:**
- (decision content authored at execution time; substrate is the adjudicator module + SQL probes from T01-T04)

**Read scope:**
- All PR #242 / 01_05_10 / 01_04_05 / spec / PHA YAML / MFC YAML paths in `source_artifacts`

### T06 — Mirrored test file

**Objective:** Achieve ≥95% line coverage on the adjudicator module with synthetic `tmp_path`
fixtures + optional real-DB `skipif` smoke tests; test every falsifier branch.

**Instructions:**

1. Create `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_cross_region_retention.py`.

2. Synthetic fixture column-name constants (round-2 B1+B2 binding):
   - `MFC_COLUMNS` = 30 columns; NO `is_cross_region_fragmented`, NO `match_id`, NO `player_id`.
   - `PHA_COLUMNS` = 38 columns, INCLUDING `is_cross_region_fragmented` at the same projected position as the live YAML.
   - `MHM_COLUMNS` = including `match_id` (prefixed `sc2egset::<32-char-hex>`) and `player_id` (= `toon_id`).

3. Test classes (per PR #234/#241/#242 precedent + round-3 NIT-A/B/C/D additions):
   - `TestParentPR242SHAVerification` — 2 pass + 2 mismatch
   - `TestPR241SHAVerification` — 1 pass + 1 mismatch
   - `TestCrossRegion0105_10Verification` — 2 pass + 2 mismatch
   - **(NEW round-3 NIT-B)** `TestPlayerHistoryAllYamlSHAVerification` — 1 pass (live file SHA matches `EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256`) + 1 mismatch (tampered fixture halts)
   - **(NEW round-3 NIT-B)** `TestStep0104_05MdSHAVerification` — 1 pass + 1 mismatch
   - **(NEW round-3 NIT-B)** `TestMatchesFlatCleanYamlSHAVerification` — 1 pass + 1 mismatch
   - **(NEW round-3 NIT-B)** `TestCross0202SpecSHAVerification` — 1 pass + 1 mismatch
   - **(NEW round-3 NIT-C)** `TestCrossRegionToonIdAnchorCountDrift` — 1 pass + 1 drift (BINDING probe)
   - **(NEW round-3 NIT-C)** `TestCrossRegionNicknameAnchorCountDrift` — 1 pass (asserts 246/1923/32031) + 1 drift (EQUIVALENCE probe) + 1 explicit semantic-binding test (assert `EXPECTED_CROSS_REGION_PLAYER_MATCH_PAIR_COUNT_NICKNAME_ANCHORED == 32031` AND the toon_id-membership BINDING probe's expected count is a separate constant)
   - `TestStrictLtFilterDivergence` — 1 pass + 1 drift
   - `TestExactFiveDecisionsPresent` — 1 pass + 1 halt (only 4 rows)
   - `TestQ5ThreeOptionsEnumerated` — 1 pass + 1 halt (only 2 options) + 1 halt (fourth option `mfc_target_row_drop` injected per A4)
   - `TestStrictExclusionHistoryFilterRetentionSmoke` — 1 pass + 1 halt
   - `TestDualFeaturePathBranchesNondegenerate` — 1 pass + 1 halt
   - `TestSensitivityIndicatorFlagNondegenerate` — 1 pass + 1 (TRUE=0 on PHA) + 1 (FALSE=0 on PHA)
   - `TestSensitivityIndicatorAnchorTargetTime` — 1 pass + 1 halt
   - `TestQ5EvidenceSufficiency` — 4 cases
   - `TestQ5PostGameTokenInScopedField` — 3 cases
   - `TestQ5NoDirectTargetMatchOutcome` — 1 pass + 1 halt
   - `TestQ5NoFutureMatchLeakage` — 1 pass + 1 halt
   - `TestQ5NoGlobalBatchFit` — 1 pass + 1 halt
   - `TestQ5NoPhase03BaselineCreep` — 1 pass + 1 halt
   - `TestNoMaterializedOutputPath` — 1 pass + 1 halt (key `materialization_creep` per B4 promotion)
   - **(NEW round-3 B4)** `TestDecisionCountDrift` — 1 pass + 1 halt (key `decision_count_drift` per B4 promotion)
   - `TestNoStatusYamlChange` — 1 pass + 1 halt
   - `TestNoResearchLogChange` — 1 pass + 1 halt
   - `TestNoQ6ArtifactChange` — 3 cases
   - `TestNoMfcCrossRegionColumnReference` — 1 pass + 2 halt variants (round-2 B1)
   - **(NEW round-3 NIT-D — structured-field replacement)** `TestHistoryRowFilterFieldStructured`:
     - 1 pass — valid value `"yes"` with consistent `selected_policy == "strict_exclusion"`;
     - 1 pass — valid value `"no"` with consistent `selected_policy == "sensitivity_indicator_co_registration"`;
     - 1 pass — valid value `"not_applicable"` with `decision_id == "Q5_per_family_impact_summary"`;
     - 1 halt — invalid value `"foo"` (not in ALLOWED set);
     - 1 halt — inconsistent combo: Q5A (`selected_policy == "strict_exclusion"`) with `history_row_filter_on_pha_applied == "no"`;
     - 1 halt — inconsistent combo: Q5C (`selected_policy == "sensitivity_indicator_co_registration"`) with `history_row_filter_on_pha_applied == "yes"`;
     - 1 pass — Q5_selected_policy row's value matches the bound policy.
   - **(NEW round-3 NIT-D — SQL byte-scan KEPT)** `TestQ5FilterTargetIsPhaHistorySql`:
     - 1 pass (every WHERE-clause predicate on `is_cross_region_fragmented` is anchored on `ph.` alias);
     - 1 halt (synthetic module with `WHERE NOT mfc.is_cross_region_fragmented` injected).
   - `TestVerdictEmergedFromTableAttestation` — 2 cases (round-2 N3)
   - **(round-4 B4 — asserts 31 invariants)** `TestHelperToFalsifierKeyMappingExactCount` — asserts `len(HELPER_TO_FALSIFIER_KEY) == 31` AND `len(FALSIFIER_PRIORITY_CHAIN) == 31` AND `len(set(FALSIFIER_PRIORITY_CHAIN)) == 31` AND `set(FALSIFIER_PRIORITY_CHAIN) <= set(HELPER_TO_FALSIFIER_KEY.values())`.
   - **(round-4 B4 rewritten)** `TestPriorityChainReferencesMapping`:
     ```python
     def test_chain_subset_of_mapping_values() -> None:
         assert set(FALSIFIER_PRIORITY_CHAIN) <= set(HELPER_TO_FALSIFIER_KEY.values())
     def test_chain_no_duplicates() -> None:
         assert len(FALSIFIER_PRIORITY_CHAIN) == len(set(FALSIFIER_PRIORITY_CHAIN))
     def test_mapping_and_chain_set_equality() -> None:
         assert set(FALSIFIER_PRIORITY_CHAIN) == set(HELPER_TO_FALSIFIER_KEY.values())
     def test_exact_count_31() -> None:
         assert len(HELPER_TO_FALSIFIER_KEY) == 31
         assert len(FALSIFIER_PRIORITY_CHAIN) == 31
         assert len(set(FALSIFIER_PRIORITY_CHAIN)) == 31
     ```
   - `TestForbiddenTokensExemptFieldsList` — 1 case
   - `TestDeterministicCsvSchema` — asserts CSV header = exactly **29 columns** (28 dataclass fields + `notes`, post-NIT-B+C+D field additions), row count = 5, byte-identical across runs.
   - `TestParentDecisionIdIsSchemaExtension` (round-2 N1) — 2 cases
   - `TestRealDBSmoke` — `@pytest.mark.skipif(not DUCKDB_AT_DEFAULT_PATH)` real-DB smoke; runs entrypoint against `data/db/db.duckdb` and asserts: 3 nickname-anchored anchor counts (246/1923/32031), the toon_id-membership BINDING count matches its (Layer-2-pinned) constant, per-family retention plausibility, MFC column-name set does NOT include `is_cross_region_fragmented`, all 4 NIT-B source-file SHAs match their pinned constants.

4. Real-DB smoke fixture: read-only `duckdb.connect(str(DUCKDB_PATH), read_only=True)`.

**Verification:** `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_cross_region_retention.py -v --cov=rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_cross_region_retention --cov-report=term-missing` reports ≥95% line coverage; all tests pass.

**File scope:**
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_cross_region_retention.py`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml`

### T07 — Sandbox notebook pair

**Objective:** Produce the jupytext-paired `.py` + `.ipynb` driver notebook that calls the
adjudicator module's public entrypoint against the real DuckDB and writes the CSV+MD artifacts.

**Instructions:**

1. Create `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.py` (jupytext `py:percent` canonical).

2. Banner cell declares hypothesis + falsifier per `feedback_notebook_iterative_testing.md`:
   - H1 (Q5A): strict-exclusion drops a measurable fraction of PHA HISTORY ROWS; F1: anchor drift → halt.
   - H2 (Q5B): dual-feature-path branches are non-degenerate; F2: degenerate branch → halt.
   - H3 (Q5C): sensitivity-indicator flag is non-degenerate; F3: degenerate flag → halt.
   - H4 (round-2 B1+B3): live MFC has 30 cols and lacks `is_cross_region_fragmented`; PHA has 38 cols with it; F4: any DESCRIBE on MFC returning `is_cross_region_fragmented` → halt.
   - H5 (round-2 N3): per-family retention table appears in notebook output BEFORE verdict cell; F5: verdict cell runs first → halt.
   - **H6 (round-3 NIT-B): all 4 source-file SHAs match the pinned constants; F6: any drift → halt + re-pin instructions.**
   - **H7 (round-3 NIT-C): the toon_id-membership BINDING probe's count and the nickname-anchored EQUIVALENCE probe's 32,031 count are both reported; F7: either probe's count drifts from its independent pinned constant → halt with separate diagnostic messages.**

3. Cell 2: open DuckDB read-only at `data/db/db.duckdb`; **run the 4 NIT-B SHA verifications first** (`shasum -a 256` on each of the 4 source files, assert against pinned constants); on any drift, print the new hex + re-pin instructions and halt.

4. Cell 3: `DESCRIBE matches_flat_clean` and assert 30 columns AND `is_cross_region_fragmented` NOT in it; `DESCRIBE player_history_all` and assert 38 columns AND `is_cross_region_fragmented` IS in it (F4).

5. **(round-3 NIT-C)** Cell 4: run the EQUIVALENCE probe (`_CROSS_REGION_NICKNAME_ANCHOR_PROBE_QUERY`); print and assert the 246/1923/32031 anchor counts.

6. **(NEW round-3 NIT-C)** Cell 5: run the BINDING probe (`_CROSS_REGION_TOONID_MEMBERSHIP_BASE_PROBE_QUERY`); print the toon_id-membership count; on FIRST run, print "PINNING — record this value as `EXPECTED_PHA_CROSS_REGION_TOONID_MEMBERSHIP_COUNT` in the adjudicator module and re-run"; on SUBSEQUENT runs, assert against the pinned constant.

7. (round-2 N3) Cell 6: run the three per-option probes (Q5A/Q5B/Q5C); `print()` the per-family retention table BEFORE any verdict cell.

8. Cell 7: import `adjudicate_history_cross_region_retention`; call it with all required paths (including the 4 NIT-B source-file paths added to the entrypoint signature per T04 step 1).

9. Cell 8: print the returned `CrossRegionAdjudicationResult.decisions` table; print `provenance_git_sha`; print the populated structured fields `cross_region_anchor_semantics` and `history_row_filter_on_pha_applied` per row to verify NIT-C and NIT-D bindings.

10. Cell 9: assert the written CSV has `wc -l == 6` (1 header + 5 rows) and 29 columns; assert MD contains §non-substitution disclaimer + §13 materialization-blocked-or-unblocked statement + §14 no-step-closure claim + 4 verbatim spec quotes per NIT-A.

11. No `def` / `class` / `lambda` in cells; `print()` only for read-only exploration.

12. Generate the paired `.ipynb` via `jupytext --to ipynb` after the `.py` is finalized.

**Verification:** `source .venv/bin/activate && poetry run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.ipynb` completes without exception; the 2 generated artifacts (CSV+MD) appear at the declared paths; both have non-zero size.

**File scope:**
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.py`
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.ipynb`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.csv`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.md`

**Read scope:**
- All PR #242 / 01_05_10 / 01_04_05 / risk-register / spec / schema-YAML paths

### T08 — Manifest housekeeping (CHANGELOG, pyproject, INDEX)

**Objective:** Produce the 3 housekeeping edits the Layer-2 PR requires for merge.

**Instructions:**

1. Append to `CHANGELOG.md` `[Unreleased]` block under `Added`:
   - "feat(sc2egset): Q5 cross-region retention-measurement successor adjudication (Layer-2; resolves PR #242 Q5_cross_region_policy `deferred_blocker` row)."
   - "Adjudicator module + mirrored test file (≥95% coverage) + jupytext notebook pair + 5-row 29-column successor adjudication CSV + §1-§14 successor MD."
   - "Falsifier priority chain: 31 entries (round-3 B4 promoted `materialization_creep` + `decision_count_drift` from chain-only to mapping; round-3 NIT-B added 4 SHA helpers for `player_history_all.yaml` + `01_04_05_cross_region_annotation.md` + `matches_flat_clean.yaml` + `02_02_feature_engineering_plan.md`; round-3 NIT-C added 2 base probes — toon_id-membership BINDING + nickname-anchored EQUIVALENCE; round-3 NIT-D added structured `history_row_filter_on_pha_applied` field + split R2 falsifier #24 into structured-field + SQL-byte-scan; round-4 added module-import-time assertions of the 31/31/31/subset invariants); HELPER_TO_FALSIFIER_KEY mapping has 31 entries; B-X2 canonical TRY_CAST + B-X1 scoped POST_GAME token inherited from PR #242."
   - "Column-location discipline: `is_cross_region_fragmented` is sourced from `player_history_all` (38-col PHA) only; MFC has 30 columns and does NOT carry the column (round-2 B1 binding)."
   - "Filter-semantics discipline: `WHERE NOT ph.is_cross_region_fragmented` is applied to PHA HISTORY rows BEFORE aggregation per CROSS-02-02 §6.2 row 5 + 01_04_05 §7 strategy 1 + PHA YAML NOTES lines 220-226; MFC-target-row filtering is OUT OF SCOPE (round-2 B3 binding)."
   - "Quote-attribution discipline (round-3 NIT-A): the consolidated paraphrase prescribing `WHERE NOT is_cross_region_fragmented` as safe-subset filter / dual feature paths / sensitivity indicator is sourced from `player_history_all.yaml` NOTES lines 220-226 ONLY; 01_04_05 §7 contains a 3-strategy enumeration with distinct on-disk wording at lines 200-216; CROSS-02-02 §6.2 row 5 Constraint column contains the 3-option enumeration at line 242 with distinct on-disk wording."
   - "Probe-semantics discipline (round-3 NIT-C): BINDING probe = toon_id-membership (`WHERE ph.toon_id IN (SELECT DISTINCT toon_id WHERE is_cross_region_fragmented = TRUE)`); EQUIVALENCE probe = nickname-anchored (replicates 01_05_10 SQL 3 idiom, yields 32,031). Each probe has its own independent expected count. `cross_region_anchor_semantics` field disambiguates per row."
   - "Filter-applied discipline (round-3 NIT-D): `history_row_filter_on_pha_applied: str ∈ {'yes', 'no', 'not_applicable'}` is a structured machine-readable field; the R2 vacuous prose-substring check is REMOVED; the SQL byte-scan portion is KEPT."
   - "MATERIALIZATION still BLOCKED: PR #242 Q6_rating_policy remains `deferred_blocker`; this PR resolves only Q5."
   - "Version-bump rationale (round-2 N2 acceptance from reviewer-adversarial round 1): minor 3.73.0 → 3.74.0 — feat-family per git-workflow.md — adds a new adjudicator module + new successor adjudication artifact pair; no materialized feature data."

2. Bump `pyproject.toml` version `3.73.0 → 3.74.0` (minor; feat-family per git-workflow.md).

3. Move `[Unreleased]` block contents into a new `[3.74.0] — 2026-MM-DD (PR #<successor-PR>: feat/sc2egset-02-01-03-history-cross-region-adjudication)` block in `CHANGELOG.md`; leave `[Unreleased]` empty with Added/Changed/Fixed/Removed headers.

4. Update `planning/INDEX.md`:
   - Move the current Active row (PR #242 Layer-2) into the Archive table.
   - Add a new Active row for THIS Layer-2 PR.

5. Verify `wc -l` of the successor CSV = 6 (1 header + 5 rows); verify `wc -c` of every SHA-256 field is exactly 64; verify no `NOT_FOUND` token appears in any CSV cell.

**Verification:** `git diff --stat` shows exactly 9 deliverable files + 2 inherited planning files; `grep -c '^[a-f0-9]\{64\}$'` on the successor CSV returns the expected count.

**File scope:**
- `CHANGELOG.md`
- `pyproject.toml`
- `planning/INDEX.md`

### T09 — Layer-2 final-gate dispatch

**Objective:** Dispatch reviewer-adversarial as the Layer-2 final gate before the PR is marked
ready-for-review.

**Instructions:**

1. Compute the base ref: master HEAD at the moment the Layer-2 PR is opened.
2. Dispatch reviewer-adversarial with arguments:
   - `plan_path = planning/current_plan.md`
   - `base_ref = <Layer-2 base HEAD>`
   - `head_ref = HEAD`
3. Reviewer-adversarial reads the plan + the full diff (base..HEAD), verifies every hard-stop, returns APPROVE / APPROVE-WITH-NITS / HOLD.
4. If HOLD with blockers, the Layer-2 executor applies the requested edits and re-dispatches (3-round adversarial cap on execution side; per `feedback_adversarial_cap_execution.md`).
5. If APPROVE / APPROVE-WITH-NITS with 0 blockers, the Layer-2 PR may be marked ready-for-review.
6. The Layer-2 PR does NOT auto-merge.

**Verification:** reviewer-adversarial returns one of `APPROVE` / `APPROVE-WITH-NITS` / `HOLD`.

**File scope:** none (process-only step).

## File Manifest

**This Layer-1 planning PR — exactly 2 files:**

1. `planning/current_plan.md` (this document)
2. `planning/current_plan.critique.md` (produced by reviewer-adversarial in a separate dispatch)

**Future Layer-2 successor adjudication execution PR — 11 final tracked files (9 deliverable + 2 inherited planning):**

| # | Path | Action |
|---|------|--------|
| 1 | `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.py` | create |
| 2 | `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.ipynb` | create |
| 3 | `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` | create |
| 4 | `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_cross_region_retention.py` | create |
| 5 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.csv` | create |
| 6 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.md` | create |
| 7 | `planning/INDEX.md` | edit (archive Active → add new Active) |
| 8 | `CHANGELOG.md` | edit (append [Unreleased] entries, move to [3.74.0]) |
| 9 | `pyproject.toml` | edit (3.73.0 → 3.74.0) |
| 10 | `planning/current_plan.md` | inherited (this Layer-1 PR) |
| 11 | `planning/current_plan.critique.md` | inherited (this Layer-1 PR) |

**Files explicitly NOT touched by the future Layer-2 PR (every byte unchanged):**

- All PR #242 artifacts: `02_01_03_history_source_anchor_coldstart_adjudication.{csv,md}`,
  `adjudicate_history_enriched_pre_game_source_layer.py`,
  `test_adjudicate_history_enriched_pre_game_source_layer.py`,
  `02_01_03_history_enriched_pre_game_feature_materialization.{py,ipynb}` (PR #241 scaffold notebook).
- PR #241 validator module: `validate_history_enriched_pre_game_materialization.py`.
- All `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` rows.
- Per-dataset `research_log.md` (no new entry).
- Root `reports/research_log.md`.
- `ROADMAP.md` (Step 02_01_03 block byte-unchanged).
- `INVARIANTS.md`.
- All spec files in `reports/specs/` (including `02_02_feature_engineering_plan.md` — its
  SHA is asserted by the new NIT-B helper, not edited).
- All cleaning-layer schema YAMLs in `data/db/schemas/` (including `player_history_all.yaml`
  and `matches_flat_clean.yaml` — their SHAs are asserted by new NIT-B helpers, not edited).
- All `thesis/`, `docs/`, `.claude/`, `data/`, AoE2 paths.

## Gate Condition

The future Layer-2 PR may be marked ready-for-review only when ALL of the following hold:

1. The 9 deliverable files exist at the declared paths.
2. `wc -l` of `02_01_03_history_cross_region_adjudication.csv` equals 6 (1 header + 5 rows).
3. CSV has exactly **29 columns** (28 dataclass fields + `notes`; updated from R2's 23 columns due to NIT-B's 4 SHA columns + NIT-C's `cross_region_anchor_semantics` field + NIT-D's `history_row_filter_on_pha_applied` field).
4. Every CSV SHA-256 cell is 64-char lowercase hex; no `NOT_FOUND` token in any cell.
5. `materialized_output_paths` is empty in every CSV row.
6. The MD contains: §1 non-substitution disclaimer; §2-§6 per-decision rows (5 rows); §7 parent PR #242 lineage; §8 SQL-probe verbatim block (Invariant I6) including verbatim `WHERE NOT ph.is_cross_region_fragmented` history-row filter showing PHA anchoring per round-2 B3 AND verbatim `_CROSS_REGION_TOONID_MEMBERSHIP_BASE_PROBE_QUERY` + `_CROSS_REGION_NICKNAME_ANCHOR_PROBE_QUERY` per round-3 NIT-C; §9 per-family retention table; §10 evidence-paths block; §11 falsifier roll-call listing all 31 entries; §12 explicit non-substitution statement; §13 materialization-blocked-or-unblocked statement; §14 no-step-closure claim; ZERO Phase-03 claim; ZERO Step 02_01_04 reference; **§rationale contains the FOUR verbatim quotes per round-3 NIT-A re-attribution: (a) CROSS-02-02 §6.2 row 5 line 242 Source column, (b) CROSS-02-02 §6.2 row 5 line 242 Constraint column, (c) 01_04_05 §7 strategy 1 lines 203-208, (d) PHA YAML NOTES lines 220-226**.
7. `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_cross_region_retention.py -v --cov=rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_cross_region_retention --cov-report=term-missing` returns ≥95% line coverage; all tests pass.
8. `source .venv/bin/activate && poetry run ruff check src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_cross_region_retention.py` passes.
9. `source .venv/bin/activate && poetry run mypy src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` passes.
10. The full project test suite plus pre-commit hooks pass on the final Layer-2 commit.
11. `git diff master --stat` for the Layer-2 branch shows exactly the 11 files in the manifest.
12. Reviewer-adversarial round-N returns 0 blockers (within the 3-round cap).
13. No status YAML change; no `research_log.md` change; no ROADMAP change.
14. PR #242 artifacts, PR #241 scaffold validator, and all spec/schema/cleaning-layer files are byte-unchanged.
15. `grep -E "mfc\.is_cross_region_fragmented" src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` returns 0 hits.
16. `grep -E "mfc\.match_id|mfc\.player_id" src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` returns 0 hits; `grep -E "'sc2egset::' \|\| mfc\.replay_id" src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` returns ≥ 1 hit.
17. `grep -E "WHERE NOT ph\.is_cross_region_fragmented" src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_cross_region_retention.py` returns ≥ 1 hit; the MD §rationale contains the FOUR verbatim spec quotes per item 6.
18. The notebook output and the MD §evidence section both contain the per-family retention table BEFORE the verdict is recorded; the `Q5_selected_policy` row's `notes` field contains the literal "VERDICT EMERGED FROM TABLE" attestation phrase.
19. `parent_decision_id` is labelled in the MD §schema-extension-disclosure as a NEW field introduced by this successor PR; `grep -c parent_decision_id <PR #242 CSV>` returns 0.
20. **(round-3 B4 / round-4 mechanical fix)** `len(HELPER_TO_FALSIFIER_KEY) == 31 AND len(FALSIFIER_PRIORITY_CHAIN) == 31 AND set(FALSIFIER_PRIORITY_CHAIN) == set(HELPER_TO_FALSIFIER_KEY.values()) AND len(set(FALSIFIER_PRIORITY_CHAIN)) == len(FALSIFIER_PRIORITY_CHAIN)`. These four invariants are ALSO enforced at module-import time via top-level `assert` statements (per T01 step 6) so any drift fails BEFORE any test runs.
21. **(NEW round-3 NIT-A)** The MD §rationale contains the FOUR verbatim spec quotes attributed to their actual on-disk locations: CROSS-02-02 §6.2 row 5 line 242 Source column + line 242 Constraint column + 01_04_05 §7 strategy 1 lines 203-208 + PHA YAML NOTES lines 220-226. No quote is mis-attributed across files.
22. **(NEW round-3 NIT-B)** `shasum -a 256` on each of the 4 source files (`player_history_all.yaml`, `01_04_05_cross_region_annotation.md`, `matches_flat_clean.yaml`, `02_02_feature_engineering_plan.md`) matches the pinned `EXPECTED_*_SHA256` constants in the adjudicator module; the 4 NEW CSV provenance columns (`player_history_all_yaml_sha256`, `step_01_04_05_md_sha256`, `matches_flat_clean_yaml_sha256`, `cross_02_02_spec_sha256`) are present on every CSV row and contain 64-char lowercase hex strings matching the pinned constants. No `NOT_FOUND` value in any of the 4 new columns.
23. **(NEW round-3 NIT-C)** The adjudicator module contains BOTH `_CROSS_REGION_TOONID_MEMBERSHIP_BASE_PROBE_QUERY` (BINDING) and `_CROSS_REGION_NICKNAME_ANCHOR_PROBE_QUERY` (EQUIVALENCE) as separate module-level constants. Each has its own helper, its own expected-count constant (`EXPECTED_PHA_CROSS_REGION_TOONID_MEMBERSHIP_COUNT` for BINDING, the 246/1923/32031 triple for EQUIVALENCE), its own falsifier key (`cross_region_toon_id_anchor_count_drift` vs `cross_region_nickname_anchor_count_drift`), its own test class. The 32,031 expectation appears ONLY in the EQUIVALENCE probe context. Every per-option CSV row carries `cross_region_anchor_semantics ∈ {"toon_id_based", "nickname_based", "both"}`.
24. **(NEW round-3 NIT-D)** Every per-option CSV row carries `history_row_filter_on_pha_applied ∈ {"yes", "no", "not_applicable"}` with values consistent with `selected_policy` (Q5A = "yes", Q5B = "yes", Q5C = "no", Q5_selected_policy = mirror of chosen policy, Q5_per_family_impact_summary = "not_applicable"). The R2 vacuous prose-substring check is REMOVED from the adjudicator module; the SQL byte-scan check is KEPT as a separate helper (helper #31 / key `q5_filter_target_is_pha_history_violated_sql`).

## Open Questions

OQ1. **Q6 rating-family adjudication — separate future planning round.** Q6 remains `deferred_blocker`. Next planning round evaluates 5 candidate families (no-rating / rolling baseline / Elo / Glicko / Glicko-2 / TrueSkill) against the N-X3 strengthened gate. Should NOT begin until this Q5 successor PR is merged.

OQ2. **`methodology_risk_register.md` path mismatch.** PR #242 frontmatter and the ROADMAP reference `methodology_risk_register.md`; on-disk path is `06_decision_gates/risk_register_sc2egset.md`. Documentation-only; future cosmetic chore.

OQ3. **CHANGELOG `20 entries` vs actual 21 inconsistency in PR #242.** Future cosmetic chore.

OQ4. **Q5 verdict — `bind_now` vs `narrow_with_evidence` vs continued `deferred_blocker`.** Planner's PROVISIONAL recommended verdict is `narrow_with_evidence` with `selected_policy = "sensitivity_indicator_co_registration"`. Per A14, the recommendation is PROVISIONAL and executor MUST report the per-family retention table BEFORE selecting any policy.

OQ5. **Phase-03 sensitivity-arm reservation.** If Q5 binds option (c), the Phase 03 sensitivity-arm protocol is RECORDED in `Q5_per_family_impact_summary` row but not executed.

OQ6. **`parent_decision_id` back-fill into PR #242 CSV — future cosmetic chore.** Verified `grep -c parent_decision_id <PR #242 CSV>` = 0.

OQ7. **(NEW round-3 NIT-C) Equivalence between toon_id-membership and nickname-anchored counts.** The two probes may yield slightly different counts (e.g., if any cross-region toon_id has a PHA row whose `LOWER(nickname)` is not in `cross_region_nicks`, or vice versa due to nickname-case drift between `replay_players_raw` and `player_history_all`). The Layer-2 executor must report both counts and document any divergence in the MD §evidence. If divergence > 0, the executor must flag it as a sub-finding (not a blocker — both probes are honest measurements; the toon_id-membership form is BINDING per A19).

OQ8. **(NEW round-3 NIT-D) Q5C `history_row_filter_on_pha_applied` value — `"no"` vs `"not_applicable"`.** Both values are semantically defensible for the sensitivity-indicator option: `"no"` says "the option does not apply a filter"; `"not_applicable"` says "the concept of filter does not apply to this option". The planner BINDS `"no"` for Q5C as more informative. If the executor or reviewer-adversarial round 3 prefers `"not_applicable"`, the helper #30 consistency rule is one-line edit.

## Out of scope

- Q6 rating-family adjudication (see OQ1).
- Q5/Q6 materialization.
- Any ROADMAP edit.
- Any status YAML flip.
- Any `research_log.md` entry.
- Any spec / cleaning-layer YAML / `INVARIANTS.md` edit.
- Any Phase 03 work.
- Any Step 02_01_04 work.
- Any AoE2 / `thesis/` / `docs/` / `.claude/` / `data/` edit.
- The CHANGELOG `20-vs-21` off-by-one fix (OQ3).
- The `methodology_risk_register.md` path-discrepancy fix (OQ2).
- The `parent_decision_id` back-fill into PR #242 CSV (OQ6).
- The MFC-target-row filter alternative `WHERE NOT mfc.is_cross_region_fragmented` (round-2 B3).
- Re-deriving the 4 NIT-B source files (their SHAs are PINNED at planner-time; if any source file changes between Layer-1 merge and Layer-2 execution, the Layer-2 executor halts via the new NIT-B helpers and the planner re-issues).
- Adopting any count other than 31 for `HELPER_TO_FALSIFIER_KEY` / `FALSIFIER_PRIORITY_CHAIN` (round-4 B4 mechanical fix; the 25 + 4 + 2 = 31 arithmetic per A21 is authoritative and is enforced at module-import time).

## Critique instruction

**For Category A, adversarial critique is required before execution. Dispatch
reviewer-adversarial to produce `planning/current_plan.critique.md`. This is round 4 of 4 on
the plan side, run under explicit user-authorized one-round override of the standard 3-round
cap for a mechanical B4-only fix on top of the R3 plan. Round 1 returned HOLD with 3 BLOCKERS
(B1/B2/B3) + 4 NITS (N1/N2/N3/N4); all resolved in round 2. Round 2 returned HOLD with 1
BLOCKER (B4) + 4 NITS (NIT-A/B/C/D); all resolved in round 3 (verdict-narrative). Round 3
returned HOLD with B4-recurrence (count contradiction between 29 sites and 31 sites in the
same plan) + 3 NITS (X1/X2/X3 — all the same internal count contradiction); this round-4
revision is a strict mechanical fix that adopts 31 EVERYWHERE, deletes the planner
reconciliation monologue at the former T03 lines 899-924, adds module-import mechanical
verification (T01 step 6), and adds 31-asserting test scaffolding (T06). NO methodology
change; NO new falsifier; NO SQL probe change; NO scope change. If reviewer-adversarial R4
returns HOLD, planning STOPS permanently for this attempt.**

## Self-check against R4 B4-only mechanical fix

- Every count claim about `HELPER_TO_FALSIFIER_KEY` / `FALSIFIER_PRIORITY_CHAIN` says 31 (frontmatter `round3_blocker_resolution` rewritten; frontmatter `round3_nit_resolutions` NIT-B bullet rewritten; T01 step 6 — 31 + assert block; T01 step 7 — exactly 31 entries; T01 step 7 narrative; T01 Verification — 4 assertions added; T03 heading — 31 helpers total; T03 lead-in paragraph — 31-entry mapping authoritative; T03 helper-enumeration prelude — 31-helper enumeration; T03 final Verification — 31; T04 step 2 — 31; T04 Verification — 31; T06 `TestHelperToFalsifierKeyMappingExactCount` + `TestPriorityChainReferencesMapping` — 31; Gate Condition #20 — 31; CHANGELOG bullet — 31).
- Reconciliation monologue at T03 (former lines 899-924 in the R3 file containing "Wait — that's 31 enumerated helpers but I claimed 29", "Let me reconcile", "if reviewer-adversarial round 3 prefers collapsing", "The plan defaults to the two-helper / 31-entry form for maximum dispatchability", "the Layer-2 executor collapses to 30") DELETED in its entirety; replaced with the decisive lead-in paragraph "The 31-entry mapping and 31-entry priority chain are authoritative. See module-import verification at T01 step 6." The plan no longer asks the reviewer to choose a count.
- Module-import mechanical verification added at T01 step 6 (four top-level `assert` statements asserting `len(HELPER_TO_FALSIFIER_KEY) == 31`, `len(FALSIFIER_PRIORITY_CHAIN) == 31`, `len(set(FALSIFIER_PRIORITY_CHAIN)) == 31`, `set(FALSIFIER_PRIORITY_CHAIN) <= set(HELPER_TO_FALSIFIER_KEY.values())`, placed at module-load scope per the `POST_GAME_TOKEN_SCOPED_FIELDS.isdisjoint(POST_GAME_TOKEN_EXEMPT_FIELDS)` precedent) so drift fails BEFORE any test runs. T01 step 6 also notes the import-time enforcement explicitly.
- T03 lead-in paragraph adds the explicit invariant: every falsifier in the priority chain has (1) a helper implementation or documented inline check, (2) a mapping entry in `HELPER_TO_FALSIFIER_KEY`, (3) at least one positive or negative test in T06.
- T06 updated: `TestHelperToFalsifierKeyMappingExactCount` asserts `== 31` for both `len(HELPER_TO_FALSIFIER_KEY)` and `len(FALSIFIER_PRIORITY_CHAIN)` (no `29`); `TestPriorityChainReferencesMapping` includes the 4 set/length assertions including `test_exact_count_31` that asserts the 31 invariant.
- Gate Condition #20 already says 31; verified and preserved; cross-reference to T01 step 6 module-import verification added.
- CHANGELOG bullet in T08 step 1 already says "Falsifier priority chain: 31 entries"; extended with one-line round-4 acknowledgment of the module-import-time assertion of the 31/31/31/subset invariants.
- 29 references at lines 632, 1148, 1197, 1222, 1317 (now in their new positions in this revised plan) are CSV column counts (28 dataclass fields + `notes`), NOT helper/chain counts — they correctly stay at 29 per NIT-B + NIT-C + NIT-D field additions.
- Frontmatter `gate_reviewer` field updated to acknowledge round 4 of 4 with user-authorized one-round override; A13 updated; new `round4_blocker_resolution` block added documenting the R4 mechanical fix and explicitly stating no methodology change.
- New A21 in §Assumptions codifies the authoritative 31 counts and the module-import-time enforcement.
- §Out of scope gains a final bullet forbidding any count other than 31 for `HELPER_TO_FALSIFIER_KEY` / `FALSIFIER_PRIORITY_CHAIN`.
- All R3 NIT-A/B/C/D content preserved without regression: NIT-A four verbatim quotes intact (Literature Context + T05 step 1 + Gate Condition #21); NIT-B 4 pinned SHA constants (A18 / T01 step 3 / T03 helpers 6-9 / T06 tests / Gate Condition #22) intact; NIT-C two-probe split (A19 / T01 step 3 / T02 steps 1-2 / T03 helpers 11-12 / T06 / OQ7 / Gate Condition #23) intact; NIT-D structured field (A20 / T01 step 3 / T01 step 4 / T03 helpers 30-31 / T06 / OQ8 / Gate Condition #24) intact.
- All R1 (B1/B2/B3) + R2 (N1/N3) fixes preserved without regression: B1 (A15 / Gate #15) intact; B2 (A16 / Gate #16) intact; B3 (A17 / T03 helper 31 / Gate #17) intact; N1 (T01 step 4 / OQ6 / Gate #19) intact; N3 (A14 / T05 step 4 / OQ4 / Gate #18) intact.

