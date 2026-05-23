---
category: A
branch: feat/sc2egset-02-01-02-pre-game-materialization
base_ref: 93240b19a7dc75e4a9c74d2c392f0c25091bc3ea
date: 2026-05-23
planner_model: claude-opus-4-7[1m]
dataset: sc2egset
phase: "02"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
step: "02_01_02 (materialization-execution planning; precedes the Layer-2 materialization PR)"
non_batching_sequence_position: >-
  Materialization-execution planning unit. Inserted between PR #234 adjudication
  (sequence step 3 of 9, executed via "execute and report") and the future
  Layer-2 materialization PR (sequence steps 7-8: artifact generation + status
  YAML / research_log / manifest updates). Does NOT advance the 9-step sequence
  on its own; it specifies inputs frozen by PR #234 so the Layer-2 PR resolves
  ONLY the materialization SQL + post-mat audit + closure decision.
critique_required_before_execution: true
critique_reviewer: reviewer-adversarial
gate_reviewer: "reviewer-adversarial (Category A pre-execution gate)"
chat_second_pass_required_before_materialization: true
planning_pr: "PR #235"
source_artifacts:
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.md
  - sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.py
  - src/rts_predict/games/sc2/datasets/sc2egset/validate_pre_game_feature_materialization.py
  - src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_pre_game_source_layer.py
  - tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_pre_game_feature_materialization.py
  - src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml
  - reports/specs/02_00_feature_input_contract.md  (CROSS-02-00-v3.0.1)
  - reports/specs/02_01_leakage_audit_protocol.md  (CROSS-02-01-v1.0.1)
  - reports/specs/02_02_feature_engineering_plan.md  (CROSS-02-02-v1.0.1)
  - reports/specs/02_03_temporal_feature_audit_protocol.md  (CROSS-02-03-v1.0.1)
  - thesis/pass2_evidence/methodology_risk_register.md  (RISK-20/24/26)
  - .claude/scientific-invariants.md
  - .claude/ml-protocol.md
  - .claude/rules/data-analysis-lineage.md
  - .claude/rules/sql-data.md
  - .claude/rules/python-code.md
  - .claude/rules/git-workflow.md
---

# Plan — SC2EGSet Step 02_01_02 pre_game materialization-execution (Category A)

## Scope

Category A — Phase work, planning-only materialization-execution unit. Phase 02 → Pipeline Section 02_01 → Step `02_01_02` (materialization-execution planning round). Branch `feat/sc2egset-02-01-02-pre-game-materialization` from master @ `93240b19a7dc75e4a9c74d2c392f0c25091bc3ea` (pyproject 3.69.0; PR #234 merged 2026-05-23).

**Layer-1 diff for THIS planning PR = exactly 2 files:** `planning/current_plan.md` and `planning/current_plan.critique.md`. NO `current_plan.critique_resolution.md` is produced in Layer 1; the reviewer-adversarial pre-execution gate emits the critique only. The parent (orchestrator) must clear any stale `planning/current_plan.md`, `planning/current_plan.critique.md`, and `planning/current_plan.critique_resolution.md` before `Write`.

The plan body describes the **future** Layer-2 materialization-execution PR that this planning unit authorises (i.e., the next planner-science → reviewer-adversarial → executor cycle's `current_plan.md` payload), specifying exactly which feature columns, source/anchor binding, projection SQL, encoding policy, post-mat audit, tests, falsifiers, gate, closure decision, and ChatGPT review scope the future PR will deliver. The plan is deliberately NOT itself a materialization. Materialization is the **next** session after this one's reviewer-adversarial APPROVE, gated on a mandatory ChatGPT second-pass leakage review over the projection SQL embedded in this plan body.

**Out of scope here (deferred to later sessions):**
- Producing any Parquet feature file or audit JSON/MD (Layer 2's work, not Layer 1's).
- The 6 `history_enriched_pre_game` and 11 `in_game_snapshot` families (deferred to 02_01_03+ per ROADMAP stub at line 2117-2121 and the `data-analysis-lineage.md` Non-batching rule).
- Phase 03 chronological-hold-out anchor binding (PR #234 Q2(b) is RECOMMENDATION ONLY; Phase 03 planning binds).
- Any spec or cleaning-layer YAML patch (PR #234 proposed CROSS-02-02 §6.1 minor amendment is a future-PR target).
- Any AoE2 work, any thesis chapter prose, any docs/.claude edit.

## Problem Statement

PR #234 (merged at `93240b19`) executed the source/anchor/race-column adjudication, persisting a 3-row CSV + 8-section MD (`02_01_02_source_anchor_race_adjudication.{csv,md}`) under `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`. The three coupled decisions PR #233's scaffold deferred to the second-pass are now BINDING repo inputs:

- **Q1 (source layer) = `matches_flat_clean`** (cleaned-raw view, 1v1-scoped natively). DuckDB confirms: `SELECT COUNT(*) FROM matches_flat_clean` = 44,418; `SELECT COUNT(DISTINCT replay_id) FROM matches_flat_clean` = 22,209. Self-join cardinality (PR #234 CSV row 2) = 44,418. The source carries all required tranche-1 columns natively: `race VARCHAR`, `metadata_mapName VARCHAR`, `metadata_gameVersion VARCHAR`, `is_mmr_missing BOOLEAN`, `replay_id VARCHAR`, `toon_id VARCHAR`, `details_timeUTC VARCHAR` (per `matches_flat_clean.yaml:11-177`).
- **Q2(a) Phase-02 row-identity = `started_at TIMESTAMP` from MHM** (BINDING). MHM `started_at` is `TRY_CAST(matches_flat_clean.details_timeUTC AS TIMESTAMP)` per `matches_history_minimal.yaml:21-30`. The join expression to bring `started_at` onto an MFC row is `CONCAT('sc2egset::', mfc.replay_id) = mhm.match_id AND mfc.toon_id = mhm.player_id` (PR #234 §2 verbatim peek; join cardinality = 44,418). `details_timeUTC VARCHAR` is retained as a provenance column only — *never used in filters*. **Per CROSS-02-00 §5.1 line 360, `started_at` is classified CONTEXT, not PRE_GAME**: it is a row-identity anchor used for downstream JOIN / Phase-03 ordering convenience; it is NOT a model feature. Per PR #234 adjudication Q2(a) the projected anchor carries `use_as_window_bound = false`, `use_as_row_identity = true`; per Q2(b) the Phase-03 chronological-hold-out binding is a RECOMMENDATION ONLY (Phase 03 planning binds).
- **Q2(b) Phase-03 chronological-hold-out anchor = `started_at TIMESTAMP`** RECOMMENDATION ONLY (NON-BINDING; Phase 03 planning binds). The Layer-2 plan body does NOT bind Phase 03; it merely projects `started_at` onto the feature table for Phase 03 ordering convenience (no `<` filter).
- **Q3 = RATIFY** the cleaning-layer convention (`race` is the PRE_GAME analytical canon per `matches_long_raw.yaml:101-103` and `matches_history_minimal.yaml:52-53`; `selectedRace` excluded). DuckDB confirms MFC `race` vocabulary = `{Prot=16121, Terr=12770, Zerg=15527}` (3-value, no Random); MFC `selectedRace` vocabulary = `{Prot=15841, Rand=10, Random=1110, Terr=12502, Zerg=14955}` (5-value, includes the 1,120 Random player-rows ≈ 555 matches). RISK-26 compliance = `documented_gap`; the gap is documented in PR #234 MD §8 (CROSS-02-02 §6.1 minor amendment PROPOSED as a future-PR target, NOT applied here).

**Cutoff semantics.** Per `CROSS-02-03 §6.1` (verbatim line 235-242): a `pre_game` family "reads only static pre-match attributes of game T plus historical aggregates over games strictly prior to T." For the 5 tranche-1 families which are all *static game-T attributes* (`allowed_cutoff_rule = snapshot_at_match_start` per registry CSV rows 2-6; CROSS-02-02 §6.1 cutoff cell = "none (game-T attribute)"), **no strict-`<` filter applies**. The anchor `started_at` is a row-identity timestamp, not a window bound. Leak-freedom rests on the triad: (i) only game-T pre-game columns are read, (ii) POST-GAME token absence (CROSS-02-01 §2.2), (iii) non-tracker source (Invariant I3).

**The output Parquet has 11 columns, partitioned into three semantic roles** (this partition is the **only** valid framing for examiner-facing prose; all counts/JSON fields below are derived from it):

| Role | Count | Columns | Treated as model features? |
|------|-------|---------|----------------------------|
| Projected identity | 3 | `focal_match_id`, `focal_player`, `opponent_player` | NO — lineage / split keys only |
| Projected context (Phase-02 row-identity anchor; CROSS-02-00 §5.1 = CONTEXT) | 1 | `started_at` | NO — row-identity anchor only; use_as_window_bound = false (PR #234 Q2(a)); Phase-03 binding RECOMMENDATION only (PR #234 Q2(b)); never consumed as a numeric/categorical feature |
| Audited PRE_GAME features | **7** | `focal_race`, `opponent_race`, `race_pair`, `map_type`, `patch_version`, `focal_is_mmr_missing`, `opponent_is_mmr_missing` | YES — these are the **exactly 7** members of `features_audited` per CROSS-02-01 §3 / §5 |

**Examiner-facing clarity sentence (must appear verbatim in the audit JSON `notes` and the audit MD §1):** "`started_at` is projected as a row-identity anchor only (CROSS-02-00 §5.1 = CONTEXT; PR #234 Q2(a) use_as_window_bound = false) and is excluded from `features_audited`."

The 7 audited columns are exactly the Phase 02 *materialised feature columns* declared in CROSS-02-01 §3 / §5 (`features_audited` is a flat list of feature column names; identity and context anchors are NOT feature columns and are NOT counted). The 3 identity columns and the 1 context anchor are documented separately in the audit JSON via two non-feature carriers (`projected_identity_columns` and `projected_context_columns`) and reiterated in the audit MD §1 / §4, but they MUST NOT be counted in `features_audited` and MUST NOT be described as model features anywhere (constraints from user revision; PR #234 Q2(a) adjudication; CROSS-02-00 §5.1 classification).

**Why this is a materialization-execution planning round (not the Layer-2 PR itself).** Per `.claude/rules/data-analysis-lineage.md` "Non-batching rule for empirical work" (sequence 1-9) the empirical Step must follow: 1 ROADMAP stub (PR #232), 2 scaffold + 1 validator (PR #233), 3 execute + report (PR #234 adjudication), 4 user review (this turn's planning), 5 commit (Layer-2 plan + critique), 6 next validation module (Layer-2 materialization), 7 generate artifacts (Layer-2 materialization), 8 research_log / STEP_STATUS / manifest (Layer-2 closure or a separate closure PR — to be decided in §Closure Decision below), 9 reviewer-deep. THIS PR sits at sequence step 4-5: user-review of PR #234's findings + commit a plan that resolves all remaining decisions for steps 6-9. The Layer-2 PR will execute steps 6-8 in one PR (justified below in §Execution Steps), then reviewer-adversarial runs as the final gate.

**The OPEN methodological decisions that THIS planning unit resolves on Layer-1 (recorded as plan-body specifications, not file mutations):**

1. **Exact feature columns** to project and their dtypes (justified against the 9-column scaffold tuple).
2. **Exact projection SQL** (CTE structure, focal/opponent self-join keys, output column list, filter predicates) — specific enough for an out-of-band ChatGPT second-pass leakage review.
3. **Encoding policy** (raw categorical retention vs integer encoding now vs deferral to Phase 03 fold-aware encoders).
4. **Exact CROSS-02-01 post-materialization audit** (`features_audited` = the 7 PRE_GAME feature columns; cutoff structural check is vacuous-with-justification because no `<` filter applies for tranche-1; POST-GAME token absence; normalization fit-scope; reference-window assertion; verdict).
5. **Closure decision** — does the Layer-2 PR flip STEP_STATUS to add `02_01_02: complete` (and re-derive PIPELINE_SECTION_STATUS `02_01 = in_progress` per the YAML header rule), OR is closure deferred to a separate closure PR (parallel to PR #229 §10 evidence-only → PR #230 closure pattern)?

Resolving all five in writing prevents the Layer-2 PR from batching methodological adjudication with materialization (the failure mode `.claude/rules/data-analysis-lineage.md` was authored to prevent), and frees the Layer-2 reviewer-adversarial gate to focus on execution correctness rather than methodology defensibility.

## Assumptions & Unknowns

- **Assumption (scope discipline).** This Layer-1 planning PR has a 2-file diff and authorises ONE Layer-2 materialization-execution PR. Closure may either ride with Layer 2 (see §Closure Decision) or land in a separate Layer-3 closure PR. Phase 03 is NOT authorised.
- **Assumption (PR #234 bindings frozen).** Q1 = MFC; Q2(a) = `started_at TIMESTAMP` (BINDING for row-identity / use_as_window_bound = false); Q3 = RATIFY (`race`, not `selectedRace`); CROSS-02-02 §6.1 amendment proposed only. Future re-adjudication is out of scope; if the future Layer-2 executor finds that any binding fails an executable check, HALT and route to a new planner-science round (`.claude/rules/data-analysis-lineage.md` Stop Conditions).
- **Assumption (cutoff semantics).** Per CROSS-02-03 §6.1, NO `history_time < target_time` strict-`<` filter is required for the 5 tranche-1 static game-T attributes. The Phase-02 anchor is a row-identity timestamp, not a window bound. The Layer-2 projection SQL contains NO `WHERE` predicate on `started_at` other than the trivial NOT NULL implicit in the join. The CROSS-02-01 §2.1 structural check is therefore *not vacuously satisfied* (it must report a structural verdict: "no strict-`<` filter required; tranche is game-T static attributes; verdict = pass-by-design") — recorded with justification text, not skipped.
- **Assumption (cleaning-layer trust).** The PR #234 RATIFY decision binds the Layer-2 PR to read `race` and `is_mmr_missing` directly from `matches_flat_clean`, and `metadata_mapName` / `metadata_gameVersion` from `matches_flat_clean` (not from `matches_flat` even though the registry rows 4-5 cite `matches_flat`). The MFC view is the *cleaned* projection over MF; the registry CSV's column `source_table_or_event_family = matches_flat` is the *upstream* table, and MFC inherits those columns natively. The Layer-2 PR records this binding explicitly in the projection MD and the audit MD (see T05 §2 paragraph quoting `matches_flat_clean.yaml:178-189` provenance block verbatim per N2); the registry CSV is NOT amended (registry binding is preserved at the upstream-source-table level; the materialization layer is free to read the cleaned view containing that column).
- **Assumption (no spec amendment).** PR #234's MD §8 proposed CROSS-02-02 §6.1 amendment is NOT applied. RISK-26 compliance remains `documented_gap`. If reviewer-adversarial demands the amendment as a blocker, the response is to spawn a *separate* Category E spec-only amendment PR — NOT to bundle it into Layer 2.
- **Assumption (version bumps).** This Layer-1 planning PR does NOT bump `pyproject.toml`. The future Layer-2 PR is `feat` minor `3.69.0 → 3.70.0` (Cat A; new on-disk feature artifact + audit pair + validator module + tests + research_log).

### Unknowns

- **U1. Encoder policy (raw retention vs integer encoding now).** Default proposed = RETAIN RAW CATEGORICAL STRINGS and BOOLEAN — defer encoders to Phase 03/04 fold-aware fitting (Invariant I3 normalization leakage; CROSS-02-02 §9.1 G-CS-6 "train-fold-only fit"). Alternative = integer-encode now with vocabulary pinned to the train fold (impossible without Phase 03 splits). Resolution: default to RAW; document the deferral.
- **U2. Closure decision — single Layer-2 PR vs separate closure PR.** Two options:
  - **U2.A (closure rides Layer 2):** the materialization PR adds `02_01_02: complete` to STEP_STATUS, re-derives PIPELINE_SECTION_STATUS `02_01 = in_progress` (PR #230 disclosed this is intended behaviour), and the per-dataset research_log entry. Mirrors *no precedent* — Step 02_01_01 had closure as a *separate* PR (PR #230) after evidence persistence (PR #229).
  - **U2.B (separate closure PR):** the Layer-2 PR persists feature Parquet + audit JSON/MD + research_log entry but does NOT flip STEP_STATUS; closure is a separate PR-3 with `closure_status: closed` token, `leakage_audit_state: post_materialization_pass` field. Mirrors the PR #229 → PR #230 precedent.
  - Default proposed = **U2.B** (separate closure PR). Justification: the non-batching rule's step 8 ("research_log / STEP_STATUS / manifest") explicitly separates research_log from STEP_STATUS as separate increments; PR #229 + PR #230 demonstrated the pattern. The reviewer-adversarial Layer-2 gate evaluates *only* the materialization correctness; closure is a separate methodological decision (does the audit JSON's `features_audited != []` + verdict = PASS justify Step closure given the registry's catalog-only status?). This planning round commits to U2.B unless reviewer-adversarial pushes back during Layer-1 critique.
- **U3. ChatGPT second-pass timing.** Two options:
  - **U3.A (chat second-pass runs during this Layer-1 cycle, BEFORE the planning PR merges).** This PR's body is sufficient for ChatGPT to review the projection SQL (explicit CTE shown below in §Execution Steps). User submits to ChatGPT; ChatGPT verdict embedded in the critique resolution or added as a third file `planning/current_plan.chatgpt_review.md` (the prompt explicitly forbids creating critique_resolution; the chatgpt_review file is a separate artifact). After ChatGPT clears, this planning PR merges; Layer 2 begins.
  - **U3.B (chat second-pass runs AFTER this planning PR merges, BEFORE Layer-2 executor begins).** Planning PR merges first; user submits to ChatGPT; the Layer-2 plan body adds the ChatGPT verdict as a quoted block in the new `planning/current_plan.md`; reviewer-adversarial Layer-2 gate verifies the verdict is present.
  - Default proposed = **U3.A**. Justification: the ChatGPT review is about the *projection SQL*, which lives in THIS plan body. Reviewing the SQL after this plan merges duplicates effort (the SQL is already final at Layer-1 merge time, by design). The deliverable for U3.A is a 1-2 paragraph user-relayed ChatGPT verdict pasted into the chat (this planning session does NOT itself author a `chatgpt_review.md` file — the user pastes the verdict into the next planning-or-execution session's chat). If ChatGPT raises issues, this Layer-1 plan is amended via a follow-up planner-science turn before merge.

### Documented (no longer UNKNOWN)

- **DOCUMENTED-1 (CROSS-02-02 §6.1 amendment).** Proposed in PR #234 MD §8; NOT applied here. If reviewer-adversarial Layer-1 critique demands the amendment as a blocker for Layer 2, the response is a separate Category E spec-only PR (NOT bundled into Layer 2). The Layer-2 PR cites RISK-26 compliance as `documented_gap` per PR #234's recorded decision.
- **DOCUMENTED-2 (PR #234 CSV non-determinism).** Provenance drift (git_sha) dominates; `EXECUTED_AT_UTC_DATE` is a hard-coded constant (line 105 of adjudicator); content SHAs are stable. No hygiene PR needed. Layer-2 audit JSON will exhibit the same pattern by design — recorded in the Layer-2 plan body as expected behaviour.
- **DOCUMENTED-3 (registry CSV `source_table_or_event_family` cell).** Registry rows 2, 5, 6 cite `replay_players_raw` (race-pair, matchup, is_mmr_missing); rows 3, 4 cite `matches_flat` (map, patch). The Layer-2 PR reads all 5 columns from `matches_flat_clean` (the cleaned 1v1-scoped view) — *the cleaned view inherits these columns from the cited upstream source*. The registry's source_table cell is preserved at the *upstream* level (the registry is not amended); the materialization-layer binding (MFC) is recorded in the Layer-2 audit MD §2 only, with the `matches_flat_clean.yaml:178-189` provenance block quoted verbatim (see T05 below; N2 implementation).

### Defered (NOT this PR; NOT Layer 2)

- The 6 `history_enriched_pre_game` families (Steps 02_01_03+); Phase-03 hold-out anchor binding; tracker-derived in-game families (Steps 02_01_04+); Phase 03 splits; AoE2 work; thesis chapter prose.

## Literature Context

This unit is a planning-only materialization-execution preparation; it introduces no empirical or literature claim and asserts no new finding. Governing repo sources cited verbatim or by anchor:

- **Scientific invariants** (`.claude/scientific-invariants.md`): I3 (no feature at game T from time T or later — vacuously satisfied for static game-T attributes per CROSS-02-03 §6.1, with explicit justification text in the audit MD); I5 (symmetric player treatment via MFC self-join on `(replay_id, toon_id)`); I6 (every reported count/distribution has verbatim SQL in the audit MD); I7 (no magic numbers — all constants module-level UPPER_SNAKE); I8 (cross-game pre-game categories at level of abstraction applicable to both games — race, map, matchup, missingness flag); I9 (Step references only completed predecessor artifacts: PR #229/#230/#233/#234); I10 (relative-path provenance in all artifact metadata).
- **Locked Phase-02 specs.**
  - **CROSS-02-00-v3.0.1 §3.1** (canonical cross-dataset anchor = `started_at TIMESTAMP` on MHM); **§3.2** (per-dataset raw anchor = `details_timeUTC VARCHAR` for sc2egset; retained as provenance); **§3.3** (UTC session discipline — issue `SET TimeZone = 'UTC'` at notebook open per Concern 6); **§5.1** (MHM column classification line 360 verbatim: `started_at TIMESTAMP = CONTEXT` "I3 temporal anchor; TRY_CAST from details_timeUTC"; line 363 `faction VARCHAR = PRE_GAME`; line 365 `won BOOLEAN = TARGET`; line 366 `duration_seconds BIGINT = POST_GAME_HISTORICAL`).
  - **CROSS-02-01-v1.0.1 §2.1** (cutoff structural check — explicit pass-by-design for static game-T attributes); **§2.2** (POST-GAME token absence — `won`, `result`, `duration_seconds`, `is_decisive_result`, etc.); **§2.3** (normalization fit-scope — `training_fold_only` value used; vacuously true on raw categorical retention because no normalizer was fit); **§3** (JSON schema — see §Execution Steps for the full populated JSON; `features_audited` is a flat list of PRE_GAME feature column names); **§4** (execution timing — audit runs AFTER materialization; recorded in audit MD); **§5** (gate condition — `features_audited` non-empty + `verdict = PASS` + JSON + MD present; `features_audited` carries ONLY feature columns, not identity or context anchors).
  - **CROSS-02-02-v1.0.1 §6.1** (sc2egset `pre_game` candidate families: race / opponent_race / matchup / map / patch / `is_mmr_missing` as missingness flag; "use the missingness flag, not the MMR scalar"; MMR scalar forbidden because 83.95% missing — confirmed empirically: 37,290 / 44,418 = 83.95% TRUE); **§9.1 G-CS-1** (no magic pseudocount for pre_game families — satisfied trivially because no smoothing constant is used); **§9.1 G-CS-6** (train-fold-only fit — satisfied trivially because no encoder is fit).
  - **CROSS-02-03-v1.0.1 §6.1** (pre_game cutoff = "none (game-T attribute)"; no `<` filter applies); **§5.3** (full-replay aggregate exclusion — not applicable, no aggregates).
- **Cleaning-layer schema YAMLs.**
  - `matches_flat_clean.yaml:11-177` (28 cols; `race PRE_GAME`, `is_mmr_missing BOOLEAN PRE_GAME`, `metadata_mapName PRE_GAME`, `metadata_gameVersion CONTEXT`, `details_timeUTC VARCHAR CONTEXT`, `result VARCHAR TARGET` — the target column to EXCLUDE; row_count = 44,418); `matches_flat_clean.yaml:178-189` (provenance block — `source_tables: [replay_players_raw, replays_meta_raw, player_history_all]`; `join_key: NULLIF(regexp_extract(filename, '([0-9a-f]{32})\.SC2Replay\.json', 1), '') AS replay_id`; `filter: true_1v1_decisive CTE`; `scope: True 1v1 decisive replays only. 22,209 replays, 44,418 rows`; `created_by: sandbox/.../01_04_02_data_cleaning_execution.py`).
  - `matches_history_minimal.yaml:21-30, 42-53` (9 cols; `match_id = sc2egset::<32-hex>`, `started_at TIMESTAMP`, `player_id`, `faction PRE_GAME` derived from `race` not `selectedRace`).
  - `matches_long_raw.yaml:100-103` (`selectedRace` explicitly excluded; reason: "Pre-game menu selection (includes 'Random'); race (actual played race) used instead.").
- **Methodology risk register.** RISK-20 line 375 (cross-region fragmentation; the flag is a `history_enriched_pre_game` concern — NOT tranche-1; deferred to 02_01_03+); RISK-24 line 445 (focal/opponent slot asymmetry — mitigated by MFC self-join on `(replay_id, toon_id)` per PR #234 Q1 rationale); RISK-26 line 479 (Random race semantics — compliance = `documented_gap` per PR #234 Q3 RATIFY).
- **Lineage rules** (`.claude/rules/data-analysis-lineage.md`). "Non-batching rule for empirical work" (1-9 sequence; halt on assumption unreviewed / falsifier fails / source semantics unclear). "Feature-engineering discipline" (every family declares: dataset / source table / prediction setting / grain / temporal anchor / cutoff rule / leakage falsifier / cold-start behavior / lineage artifact). "Temporal leakage discipline" (history features use `history_time < target_time`; in-game features use `event.loop <= cutoff_loop`; tracker features never pre_game). "Stop conditions" (halt before artifact generation on any of 8 listed conditions).
- **SQL/data rules** (`.claude/rules/sql-data.md`). `replay_id` canonical join key (`regexp_extract(filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1)`); `matches_flat = 2-rows-per-game → COUNT(DISTINCT replay_id)`; SQL appears verbatim in audit MD (Invariant I6); CTEs over nested subqueries.
- **Python rules** (`.claude/rules/python-code.md`). Module-level UPPER_SNAKE constants, `_QUERY` suffix on SQL constants, sklearn Pipelines over manual fit/transform, fit scalers on training split only, feature functions pure and stateless, random seed 42 from `config.py`.
- **ML protocol** (`.claude/ml-protocol.md`). The three leakage failure modes (rolling aggregates including target; head-to-head including target; co-occurring-match position including target) — vacuously inapplicable to static game-T attributes but recorded in the audit MD as "tranche-1 static attributes; failure modes 1-3 are non-applicable; verdict per CROSS-02-03 §6.1".

[OPINION] The choice to insert a materialization-execution planning unit between PR #234's adjudication and the eventual Layer-2 materialization PR is grounded in the non-batching rule + the fact that the projection SQL is itself a thesis-citable methodological commitment requiring out-of-band Claude/ChatGPT review.

## Execution Steps

> **All tasks below are for the FUTURE Layer-2 materialization-execution PR**, on the new branch `feat/sc2egset-02-01-02-pre-game-materialization`, after this plan is approved and the user submits the projection SQL below to ChatGPT for a second-pass leakage review (U3.A default). The Layer-2 PR creates ONE feature Parquet artifact + ONE audit JSON + ONE audit MD + research_log entry + version bump + CHANGELOG entry + planning INDEX update under `reports/artifacts/` and `src/`, persists ZERO unexpected feature columns, runs ZERO Phase-03 work, writes ZERO ROADMAP edits, writes ZERO spec/YAML patches.
>
> The plan body MUST distinguish:
> - **This turn's diff (Layer 1):** exactly 2 files — `planning/current_plan.md` + `planning/current_plan.critique.md`.
> - **Future Layer-2 PR diff:** the manifest in §File Manifest below — 11 entries added/updated on top of Layer 1 (12 manifest rows, 11 distinct files because the paired notebook is 1 logical update across 2 jupytext-paired files counted as 2 entries; on-disk total when Layer 2 lands = 13 files = 2 from Layer 1 + 11 distinct files from Layer 2).
> - **Future Layer-3 closure PR (U2.B default; separate planner-science round):** 3-4 files only (status YAMLs + closure-only research_log entry + CHANGELOG note).

### T01 — Update the existing scaffold notebook to execute materialization

Sandbox notebook path: `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.{py,ipynb}` (UPDATE the existing PR #233 scaffold; jupytext py:percent paired). Add new cells after the existing scaffold cells (KEEP all existing cells unchanged for lineage); the new cells run the materialization + post-mat audit.

Cell additions (no `def`/`class`/lambda in cells per sandbox/README.md; cells ≤ 50 lines):

1. **Banner update cell** (markdown). Promote the existing "SCAFFOLD + ONE VALIDATION MODULE" banner to "MATERIALIZATION + POST-MAT AUDIT (non-batching sequence steps 6-8 of 9)". Make explicit: this notebook NOW persists feature Parquet (11 projected columns = 3 identity + 1 context anchor + 7 audited features) + audit JSON/MD; it does NOT flip STEP_STATUS (closure is U2.B separate PR per plan); it does NOT touch ROADMAP body, specs, or cleaning YAMLs. Include the examiner-clarity sentence verbatim: "`started_at` is projected as a row-identity anchor only (CROSS-02-00 §5.1 = CONTEXT; PR #234 Q2(a) use_as_window_bound = false) and is excluded from `features_audited`."
2. **Imports cell** (code). Add `materialize_pre_game_features` (new public entry point in the renamed `materialize_pre_game_features.py` module — see T02). Issue `SET TimeZone = 'UTC'` at the first DuckDB connection per CROSS-02-00 §3.3.
3. **PR #234 frozen-inputs context cell** (markdown). Quote PR #234 CSV row 2-4 (Q1/Q2(a)/Q3 chosen values) verbatim. Restate the column-role partition: 3 identity, 1 context anchor (`started_at`), 7 audited features. Cite PR #234 CSV's 11 SHA-256 columns as the provenance bond.
4. **Materialization call cell** (code). Invoke `materialize_pre_game_features(duckdb_path, output_parquet_path, registry_csv_path)` → returns a `MaterializationResult` dataclass with `(parquet_path: Path, row_count: int, column_names: tuple[str, ...], halting_falsifier: str | None)`. Print: `passed`, `row_count` (expected 44,418), `len(column_names)` (expected 11 — the 11 projected columns; partition stated below), `parquet_path`. Assert `row_count == 44418`, `column_names == EXPECTED_OUTPUT_COLUMNS`, `halting_falsifier is None`.
5. **Audit call cell** (code). Invoke `run_post_materialization_audit(parquet_path, audit_json_path, audit_md_path, dataset='sc2egset', phase_02_step='02_01_02')` → returns `AuditResult` dataclass with `(verdict: str, features_audited: tuple[str, ...], projected_context_columns: tuple[str, ...], projected_identity_columns: tuple[str, ...], halting_falsifier: str | None)`. Print verdict, `features_audited`, `projected_context_columns`, `projected_identity_columns`. **Assert `verdict == 'PASS'`, `len(features_audited) == 7` (the exactly 7 PRE_GAME feature columns), `features_audited == EXPECTED_AUDITED_FEATURE_COLUMNS`, `projected_context_columns == ("started_at",)`, `projected_identity_columns == ("focal_match_id", "focal_player", "opponent_player")`, `halting_falsifier is None`.** Also assert `set(features_audited).isdisjoint(set(projected_context_columns) | set(projected_identity_columns))` — the three role partitions are mutually exclusive.
6. **Closing cell** (markdown). State: feature Parquet (11 projected columns: 3 identity + 1 context anchor + 7 audited features) persisted at `<path>`; audit JSON+MD persisted at `02_01_02/leakage_audit_sc2egset.{json,md}`; PR #230 audit unchanged (`features_audited == []` historical record at `02_01_01/leakage_audit_sc2egset.json` is unchanged — distinct artifact at distinct path); STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS not flipped (closure deferred to U2.B PR). ROADMAP body untouched. Repeat the examiner-clarity sentence about `started_at`.

**Constraints.** No `print()` of large dataframes (per `feedback_notebook_print_vs_logger` user memory: `print()` for exploration is fine; logger for one-liner diagnostics). No DuckDB `CREATE`/`INSERT`/`COPY`/`to_parquet` from within cells — those calls live in T02 module functions. Sandbox notebook only runs the public entry points; all materialization SQL lives in `materialize_pre_game_features.py`.

### T02 — Author the materialization module

Module path: `src/rts_predict/games/sc2/datasets/sc2egset/materialize_pre_game_features.py` (NEW). Conventions match existing modules (`validate_pre_game_feature_materialization.py`, `adjudicate_pre_game_source_layer.py`): `from __future__ import annotations`, `logging.getLogger(__name__)`, frozen `@dataclass(frozen=True)`, ONE public `materialize_pre_game_features` entrypoint, ONE public `run_post_materialization_audit` entrypoint, private `_check_*` and `_render_*` helpers, module-level UPPER_SNAKE constants (Invariant I7), named SQL constants with `_QUERY` suffix (Python rules).

Module-level constants:

- `EXPECTED_MFC_ROW_COUNT: int = 44418`
- `EXPECTED_OUTPUT_ROW_COUNT: int = 44418`
- `EXPECTED_OUTPUT_COLUMN_COUNT: int = 11` (3 identity + 1 context anchor + 7 audited features; see partition below)
- `EXPECTED_AUDITED_FEATURE_COLUMN_COUNT: int = 7` (PRE_GAME feature columns audited by CROSS-02-01 §3 / §5; excludes 3 identity + 1 context anchor by design)
- `EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID: int = 22209`
- `EXPECTED_IS_MMR_MISSING_TRUE_COUNT: int = 37290` (83.95% TRUE per CROSS-02-02 §6.1; assertion for sanity-check halt)
- `EXPECTED_IS_MMR_MISSING_FALSE_COUNT: int = 7128`
- `EXPECTED_RACE_VOCABULARY: frozenset[str] = frozenset({"Prot", "Terr", "Zerg"})` (RATIFY: 3-value race; no `selectedRace`)
- `EXPECTED_MAP_DISTINCT_COUNT: int = 181`
- `EXPECTED_PATCH_DISTINCT_COUNT: int = 46`
- `PROJECTED_IDENTITY_COLUMNS: tuple[str, ...] = ("focal_match_id", "focal_player", "opponent_player")` (3 cols; non-feature carriers; never enter `features_audited`)
- `PROJECTED_CONTEXT_COLUMNS: tuple[str, ...] = ("started_at",)` (1 col; CROSS-02-00 §5.1 line 360 = CONTEXT; PR #234 Q2(a) `use_as_window_bound = false, use_as_row_identity = true`; PR #234 Q2(b) Phase-03 recommendation only; never enters `features_audited`; never described as a model feature anywhere)
- `EXPECTED_AUDITED_FEATURE_COLUMNS: tuple[str, ...] = ("focal_race", "opponent_race", "race_pair", "map_type", "patch_version", "focal_is_mmr_missing", "opponent_is_mmr_missing")` (the exactly 7 PRE_GAME feature columns audited by CROSS-02-01 §3 / §5; these are the contents of `features_audited` in the audit JSON)
- `EXPECTED_OUTPUT_COLUMNS: tuple[str, ...] = PROJECTED_IDENTITY_COLUMNS + PROJECTED_CONTEXT_COLUMNS + EXPECTED_AUDITED_FEATURE_COLUMNS` (11 cols total: `(focal_match_id, focal_player, opponent_player, started_at, focal_race, opponent_race, race_pair, map_type, patch_version, focal_is_mmr_missing, opponent_is_mmr_missing)`; differs from PR #233 scaffold's 9-column tuple by adding the 3 identity + 1 context anchor and dropping `focal_matchup`/`opponent_matchup` in favour of a single `race_pair` symmetric token)
- `_POST_GAME_TOKENS: frozenset[str] = frozenset({"won", "result", "outcome", "winner", "is_decisive_result", "duration_seconds", "is_duration_suspicious", "loss", "match_result", "final_state", "post_game", "win"})` (reuses the scaffold validator's tokens plus MFC-specific POST_GAME columns).
- `_ALLOWED_SOURCE_TABLES: frozenset[str] = frozenset({"matches_flat_clean", "matches_history_minimal"})` — the audit module enforces that the projection SQL reads ONLY these tables, never tracker / PH / raw.
- `DATASET_TAG: str = "sc2egset"`
- `PHASE_02_STEP: str = "02_01_02"`
- `LINEAGE_POSITION: str = "artifact #5 in the 5-artifact lineage for Step 02_01_02 readiness (after: PR #229 §10 design-time verdict pair; PR #230 vacuous CROSS-02-01 audit pair; PR #233 scaffold + 1 validator; PR #234 adjudication artifact pair; this materialization + post-mat audit)."`

Named SQL constants (the **complete materialization SQL**, sufficient for ChatGPT review):

```sql
-- _MATERIALIZATION_QUERY: produces 44,418 rows × 11 cols
-- Tranche-1 pre_game feature materialization for sc2egset Step 02_01_02.
-- Source layer = matches_flat_clean (PR #234 Q1 binding; 44,418 rows × 28 cols).
-- Anchor = started_at TIMESTAMP via MHM join (PR #234 Q2(a) binding; row-identity only,
--          NOT used as a filter — CROSS-02-03 §6.1; CROSS-02-00 §5.1 line 360 = CONTEXT;
--          use_as_window_bound = false; use_as_row_identity = true).
-- Race column = race (PR #234 Q3 RATIFY; cleaning-layer convention).
-- Focal/opponent symmetric self-join on (replay_id, toon_id) per Invariant I5.

WITH mfc_focal AS (
    SELECT
        mfc.replay_id          AS focal_replay_id,
        mfc.toon_id            AS focal_toon_id,
        mfc.race               AS focal_race,
        mfc.is_mmr_missing     AS focal_is_mmr_missing,
        mfc.metadata_mapName   AS map_type,
        mfc.metadata_gameVersion AS patch_version
    FROM matches_flat_clean mfc
),
mfc_opponent AS (
    SELECT
        mfc.replay_id          AS opp_replay_id,
        mfc.toon_id            AS opponent_toon_id,
        mfc.race               AS opponent_race,
        mfc.is_mmr_missing     AS opponent_is_mmr_missing
    FROM matches_flat_clean mfc
),
mfc_paired AS (
    SELECT
        f.focal_replay_id,
        f.focal_toon_id,
        o.opponent_toon_id,
        f.focal_race,
        o.opponent_race,
        f.focal_is_mmr_missing,
        o.opponent_is_mmr_missing,
        f.map_type,
        f.patch_version
    FROM mfc_focal f
    JOIN mfc_opponent o
        ON f.focal_replay_id = o.opp_replay_id
        AND f.focal_toon_id  <> o.opponent_toon_id
),
mhm_anchor AS (
    SELECT
        match_id,
        player_id,
        started_at
    FROM matches_history_minimal
)
SELECT
    CONCAT('sc2egset::', p.focal_replay_id)     AS focal_match_id,
    p.focal_toon_id                              AS focal_player,
    p.opponent_toon_id                           AS opponent_player,
    a.started_at                                 AS started_at,
    p.focal_race                                 AS focal_race,
    p.opponent_race                              AS opponent_race,
    CONCAT(p.focal_race, '_vs_', p.opponent_race) AS race_pair,
    p.map_type                                   AS map_type,
    p.patch_version                              AS patch_version,
    p.focal_is_mmr_missing                       AS focal_is_mmr_missing,
    p.opponent_is_mmr_missing                    AS opponent_is_mmr_missing
FROM mfc_paired p
JOIN mhm_anchor a
    ON a.match_id  = CONCAT('sc2egset::', p.focal_replay_id)
    AND a.player_id = p.focal_toon_id
ORDER BY a.started_at, p.focal_replay_id, p.focal_toon_id
;
```

Sanity-check queries (each verbatim in audit MD; result asserted in module against the EXPECTED_* constants above):

```sql
-- _OUTPUT_ROW_COUNT_QUERY: must equal 44418
SELECT COUNT(*) FROM materialized_pre_game_features;

-- _OUTPUT_DISTINCT_FOCAL_MATCH_ID_QUERY: must equal 22209 (each match yields 2 focal rows)
SELECT COUNT(DISTINCT focal_match_id) FROM materialized_pre_game_features;

-- _FOCAL_ROWS_PER_MATCH_QUERY: must return 22209 rows, each with cnt=2
SELECT focal_match_id, COUNT(*) AS cnt
FROM materialized_pre_game_features
GROUP BY 1
HAVING COUNT(*) != 2;
-- expected: zero rows returned (every match has exactly 2 focal rows)

-- _SYMMETRY_CHECK_QUERY: focal/opponent swap reproduces the sibling row
SELECT COUNT(*) FROM materialized_pre_game_features m1
JOIN materialized_pre_game_features m2
    ON m1.focal_match_id = m2.focal_match_id
    AND m1.focal_player  = m2.opponent_player
    AND m1.opponent_player = m2.focal_player
WHERE m1.focal_race           != m2.opponent_race
   OR m1.opponent_race        != m2.focal_race
   OR m1.focal_is_mmr_missing != m2.opponent_is_mmr_missing
   OR m1.opponent_is_mmr_missing != m2.focal_is_mmr_missing
   OR m1.map_type             != m2.map_type
   OR m1.patch_version        != m2.patch_version
   OR m1.started_at           != m2.started_at;
-- expected: 0 (perfect focal/opponent symmetry per Invariant I5)

-- _NO_NULL_FEATURE_QUERY: feature columns must not be NULL after cleaning-view normalisation
SELECT
    COUNT(*) FILTER (WHERE focal_race IS NULL) AS null_focal_race,
    COUNT(*) FILTER (WHERE opponent_race IS NULL) AS null_opp_race,
    COUNT(*) FILTER (WHERE race_pair IS NULL) AS null_race_pair,
    COUNT(*) FILTER (WHERE map_type IS NULL) AS null_map,
    COUNT(*) FILTER (WHERE patch_version IS NULL) AS null_patch,
    COUNT(*) FILTER (WHERE focal_is_mmr_missing IS NULL) AS null_focal_mmr_missing,
    COUNT(*) FILTER (WHERE opponent_is_mmr_missing IS NULL) AS null_opp_mmr_missing,
    COUNT(*) FILTER (WHERE started_at IS NULL) AS null_started_at
FROM materialized_pre_game_features;
-- expected: all 8 columns return 0

-- _RACE_VOCAB_QUERY: must return exactly {Prot, Terr, Zerg}; no Random / no Rand
SELECT focal_race, COUNT(*) FROM materialized_pre_game_features GROUP BY 1 ORDER BY 1;

-- _IS_MMR_MISSING_DIST_QUERY: must match CROSS-02-02 §6.1 (37,290 TRUE / 7,128 FALSE)
SELECT focal_is_mmr_missing, COUNT(*) FROM materialized_pre_game_features
GROUP BY 1 ORDER BY 1;

-- _STARTED_AT_TIMESTAMP_TYPE_QUERY: must report TIMESTAMP
DESCRIBE materialized_pre_game_features;
```

Public API:

```python
@dataclass(frozen=True)
class MaterializationResult:
    parquet_path: Path
    row_count: int
    column_names: tuple[str, ...]
    distinct_focal_match_id_count: int
    distinct_focal_player_count: int
    race_vocabulary: frozenset[str]
    is_mmr_missing_true_count: int
    is_mmr_missing_false_count: int
    distinct_map_count: int
    distinct_patch_count: int
    materialized_output_paths: tuple[str, ...]   # non-empty for this module
    halting_falsifier: str | None

@dataclass(frozen=True)
class AuditResult:
    spec_version: str  # "CROSS-02-01-v1"
    dataset: str       # "sc2egset"
    phase_02_step: str # "02_01_02"
    audit_date: str    # ISO date
    future_leak_count: int
    post_game_token_violations: int
    normalization_fit_scope: str             # "training_fold_only"
    target_encoding_fold_awareness: str      # "N/A_no_target_encoding"
    cutoff_time_filter_structural_check: str # "pass" (justified — see audit MD)
    reference_window_assertion: str          # "pass" (Phase-01 ref_start/ref_end)
    features_audited: tuple[str, ...]        # EXACTLY the 7 PRE_GAME feature columns
                                             # (focal_race, opponent_race, race_pair,
                                             # map_type, patch_version,
                                             # focal_is_mmr_missing, opponent_is_mmr_missing);
                                             # excludes 3 identity + 1 context anchor by design
    projected_context_columns: tuple[str, ...]  # ("started_at",) — non-feature carrier per
                                                # CROSS-02-00 §5.1 = CONTEXT, PR #234 Q2(a);
                                                # never enters features_audited
    projected_identity_columns: tuple[str, ...] # ("focal_match_id", "focal_player",
                                                # "opponent_player") — non-feature carriers
    verdict: str                             # "PASS"
    artifact_json_path: str
    artifact_md_path: str
    halting_falsifier: str | None

def materialize_pre_game_features(
    duckdb_path: Path | str,
    output_parquet_path: Path | str,
    registry_csv_path: Path | str,
) -> MaterializationResult: ...

def run_post_materialization_audit(
    parquet_path: Path | str,
    audit_json_path: Path | str,
    audit_md_path: Path | str,
    dataset: str = "sc2egset",
    phase_02_step: str = "02_01_02",
) -> AuditResult: ...

# Private helpers (illustrative):
def _execute_materialization_sql(con: duckdb.DuckDBPyConnection) -> None: ...
def _export_to_parquet(con: duckdb.DuckDBPyConnection, output_parquet_path: Path) -> None: ...
def _run_sanity_check_queries(con: duckdb.DuckDBPyConnection) -> dict[str, Any]: ...
def _check_falsifiers_materialization(sanity_results: dict[str, Any]) -> str | None: ...
def _render_audit_json(audit: AuditResult, out_path: Path) -> None: ...
def _render_audit_md(audit: AuditResult, sanity_results: dict[str, Any], out_path: Path) -> None: ...
def _check_post_game_token_absence(parquet_path: Path, sql: str) -> int: ...
def _check_source_table_allowlist(con: duckdb.DuckDBPyConnection) -> int: ...
def _partition_columns_by_role(column_names: tuple[str, ...]) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]: ...  # returns (identity, context, audited_features) using the EXPECTED_* tuples
def _sha256_file(path: Path) -> str: ...
def _get_git_sha() -> str: ...
```

**Materialization mechanics.** `_execute_materialization_sql` creates a temporary view `materialized_pre_game_features` (DuckDB session-scoped; does NOT persist to the on-disk DuckDB file). `_export_to_parquet` writes that view to the canonical Parquet path via `COPY (SELECT * FROM materialized_pre_game_features) TO '<path>' (FORMAT PARQUET, COMPRESSION 'ZSTD', ROW_GROUP_SIZE 100000)`. The DuckDB file at `src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb` is opened READ-ONLY for materialization (the read-only access still permits TEMP VIEW creation in the session).

**Provenance.** Audit JSON includes the SHA-256 of the materialized Parquet file, of `materialize_pre_game_features.py`, of `02_01_02_source_anchor_race_adjudication.csv`/`.md` (PR #234 binding artifacts), of the 4 spec files, of the 2 cleaning-layer YAMLs, of the registry CSV, of the methodology risk register, and the current git SHA — provenance pattern copied from the PR #234 adjudicator module. JSON also records `lineage_position`, `audit_pr`, `executed_at_utc_date`.

### T03 — One test file

Test path: `tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_pre_game_features.py` (NEW; mirrored tree per Python rules). Coverage target ≥ 95% (`fail_under = 95` per pyproject.toml).

Tests (synthetic `tmp_path` DuckDB fixtures + real-DB `pytest.mark.skipif` smoke):

1. **Frozen-dataclass shape.** `MaterializationResult` and `AuditResult` are immutable; required fields present; `materialized_output_paths != ()`; `AuditResult.features_audited`, `projected_context_columns`, `projected_identity_columns` all present as tuples.
2. **Row count exact.** Synthetic MFC with N=10 fake replays → `row_count == 20`; `distinct_focal_match_id_count == 10`.
3. **Symmetry exact (Invariant I5).** Every match yields exactly 2 rows; focal/opponent swap reproduces sibling.
4. **Race vocabulary RATIFY enforcement.** Synthetic MFC with `race ∈ {Prot, Terr, Zerg}` only → no Random; if synthetic MFC injects `selectedRace = 'Random'`, materialization IGNORES it (only `race` is projected).
5. **POST-GAME token absence (CROSS-02-01 §2.2).** Synthetic projection that accidentally selects `result` → audit module HALTS with `post_game_token_present` halting falsifier.
6. **Source table allowlist (Invariant I3 + non-tracker).** Synthetic projection that joins `tracker_events_raw` → audit module HALTS with `unexpected_source_table`.
7. **No `selectedRace` column in output.** Output column set is exactly `EXPECTED_OUTPUT_COLUMNS`; `selectedRace` is NEVER projected.
8. **No scalar MMR/rating column in output.** Audit `_check_no_scalar_skill_column` rejects any column matching `FORBIDDEN_SKILL_TOKENS` from the existing scaffold validator (`mmr, rating, elo, glicko, skill, mu, sigma`); `is_mmr_missing` is allowed via the existing `APPROVED_MMR_MISSINGNESS_TOKENS` allowlist.
9. **MMR-missingness count assertion.** Real-DB skipif: `is_mmr_missing_true_count == 37290` AND `is_mmr_missing_false_count == 7128` (sanity-check halt if drifts).
10. **Map and patch n_distinct.** Real-DB skipif: `distinct_map_count == 181`, `distinct_patch_count == 46`.
11. **Audit JSON schema — exactly 7 audited PRE_GAME feature columns.** `verdict == 'PASS'`, `len(features_audited) == 7`, `features_audited == EXPECTED_AUDITED_FEATURE_COLUMNS = ("focal_race", "opponent_race", "race_pair", "map_type", "patch_version", "focal_is_mmr_missing", "opponent_is_mmr_missing")`, all schema fields present per CROSS-02-01 §3.
12. **PR #234 binding hash check.** Audit JSON contains `02_01_02_source_anchor_race_adjudication_csv_sha256` matching the on-disk hash; if mismatch → `pr234_binding_hash_mismatch` halting falsifier.
13. **Closure-non-claim check.** Audit JSON `notes` field contains the explicit "Step 02_01_02 NOT closed by this PR; closure deferred to a separate PR per planning U2.B" string.
14. **PR #230 vacuous audit preservation.** Test asserts that the on-disk file `02_01_01/leakage_audit_sc2egset.json` remains byte-unchanged after running the Layer-2 materialization (the new `02_01_02/leakage_audit_sc2egset.json` is a separate artifact at a separate path).
15. **Reproducibility on rerun.** Two consecutive materialization runs over the same DuckDB / git SHA produce identical Parquet bytes (modulo provenance fields in the audit JSON: `git_sha` and the rendered audit MD body, which are expected to drift on a different commit).
16. **Stale path rejection.** Following the existing scaffold-validator pattern (`STALE_REGISTRY_FILENAME_FRAGMENT` rejection), the materialization module rejects `output_parquet_path` strings containing `_sc2egset` filename fragment.
17. **Real-DB smoke (skipif).** Full materialization end-to-end: `passed == True`, row_count = 44,418, `verdict == 'PASS'`, both Parquet + JSON + MD files present at canonical paths after the call.
18. **Column-role partition mutual exclusion (NEW per revision constraint 5).** Audit `projected_context_columns == ("started_at",)`, `projected_identity_columns == ("focal_match_id", "focal_player", "opponent_player")`, and the three role tuples are mutually disjoint sets: `set(features_audited) & set(projected_context_columns) == set()`; `set(features_audited) & set(projected_identity_columns) == set()`; `set(projected_context_columns) & set(projected_identity_columns) == set()`. Their union equals `set(EXPECTED_OUTPUT_COLUMNS)` (= 11 columns).
19. **Examiner-clarity sentence presence (NEW per revision constraint 6).** Audit JSON `notes` field contains the exact substring "`started_at` is projected as a row-identity anchor only" AND "excluded from `features_audited`"; audit MD §1 contains the same sentence verbatim. If either substring is missing → `examiner_clarity_sentence_missing` halting falsifier.

### T04 — Update existing scaffold validator + test (consume scaffold validator for back-compat regression)

The existing `validate_pre_game_feature_materialization.py` and its test file (PR #233) are NOT modified except to be invoked from T01's notebook for back-compat (the scaffold validator confirms the design contract is preserved; the materialization module confirms the materialised output matches the contract). The Layer-2 PR runs both in the notebook to maintain lineage.

**(N1 implementation, per revision constraint 7-N1):** The existing scaffold validator at `src/rts_predict/games/sc2/datasets/sc2egset/validate_pre_game_feature_materialization.py` is re-invoked over the new 11-tuple `EXPECTED_OUTPUT_COLUMNS` and is expected to PASS unchanged. The scaffold validator's column-name checks are allowlist-based (boundary-aware POST_GAME token equality on the `_POST_GAME_TOKENS` frozenset and boundary-aware forbidden-skill token equality on `FORBIDDEN_SKILL_TOKENS` minus the `APPROVED_MMR_MISSINGNESS_TOKENS` allowlist); they reject *extra families* and *forbidden tokens*, not *extra columns*. There is no hard-coded 9-tuple assertion anywhere in the scaffold validator that would conflict with the 11-tuple materialization output. The Layer-2 executor must read `validate_pre_game_feature_materialization.py` lines 170-200 before invoking, to confirm this empirically; if any line in the scaffold validator does contain a hard-coded 9-tuple shape assertion (it currently does not, per planner-science review), the Layer-2 PR halts and routes to a new planner-science round for scaffold-validator update — NOT silently mutating the scaffold validator.

If any test in `test_validate_pre_game_feature_materialization.py` requires update to accommodate the renamed 9-column → 11-column scaffold tuple, that update is the only allowed change. Justification: the scaffold tuple `DESIGNED_COLUMN_NAMES` in the notebook (lines 150-160) is the user-visible source of truth for column names; T01 updates that tuple to match the materialization module's `EXPECTED_OUTPUT_COLUMNS` (11 cols, including the 3 identity columns `focal_match_id, focal_player, opponent_player` and the context anchor `started_at`). The scaffold validator's allowlist check (`_check_is_mmr_missing_is_flag_not_skill`) re-validates that `focal_is_mmr_missing` and `opponent_is_mmr_missing` remain in `APPROVED_MMR_MISSINGNESS_TOKENS`.

### T05 — Artifact emission (the ONLY new on-disk feature outputs)

Paths:

- **Parquet feature table:** `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet` (44,418 rows × 11 cols = 3 identity + 1 context anchor + 7 audited features; ZSTD compression; 100,000-row groups).
- **Audit JSON:** `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json` (CROSS-02-01-v1.0.1 §3 schema; `features_audited` = exactly 7 PRE_GAME feature columns; verdict = PASS).
- **Audit MD:** `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.md` (8 sections with verbatim peek SQL per Invariant I6 — see below).

**Decision on Parquet path.** Use the `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/` directory (same as the registry CSV + the §10 verdict audit + the PR #234 adjudication CSV) for the feature Parquet, AND the `reports/artifacts/02_01_02/` directory for the leakage audit JSON+MD. The two-directory split mirrors PR #230's precedent for the catalog-only audit at `02_01_01/leakage_audit_sc2egset.{json,md}`. NOT using a separate `data_artifacts/` directory — no such directory exists in the repo.

**Audit JSON content** (populated per CROSS-02-01 §3 schema):

```json
{
  "spec_version": "CROSS-02-01-v1",
  "dataset": "sc2egset",
  "phase_02_step": "02_01_02",
  "audit_date": "<ISO YYYY-MM-DD at execution>",
  "future_leak_count": 0,
  "post_game_token_violations": 0,
  "normalization_fit_scope": "training_fold_only",
  "target_encoding_fold_awareness": "N/A_no_target_encoding",
  "cutoff_time_filter_structural_check": "pass",
  "reference_window_assertion": "pass",
  "features_audited": [
    "focal_race",
    "opponent_race",
    "race_pair",
    "map_type",
    "patch_version",
    "focal_is_mmr_missing",
    "opponent_is_mmr_missing"
  ],
  "projected_context_columns": ["started_at"],
  "projected_identity_columns": ["focal_match_id", "focal_player", "opponent_player"],
  "verdict": "PASS",
  "audit_pr": "PR #<N>",
  "lineage_position": "artifact #5 in the 5-artifact lineage for Step 02_01_02 readiness",
  "pr_234_binding_csv_sha256": "<sha>",
  "pr_234_binding_md_sha256": "<sha>",
  "feature_parquet_sha256": "<sha>",
  "materialize_module_sha256": "<sha>",
  "registry_csv_sha256": "<sha>",
  "methodology_risk_register_sha256": "<sha>",
  "matches_flat_clean_yaml_sha256": "<sha>",
  "matches_history_minimal_yaml_sha256": "<sha>",
  "matches_long_raw_yaml_sha256": "<sha>",
  "spec_02_00_sha256": "<sha>", "spec_02_01_sha256": "<sha>",
  "spec_02_02_sha256": "<sha>", "spec_02_03_sha256": "<sha>",
  "provenance_git_sha": "<sha>",
  "notes": "Step 02_01_02 NOT closed by this PR; closure deferred to a separate PR per planning U2.B (PR #229 -> PR #230 precedent). PIPELINE_SECTION_STATUS 02_01 = complete remains derived from STEP_STATUS until a future PR adds 02_01_02 to STEP_STATUS, at which point YAML-derivation re-derives 02_01 = in_progress (intended behaviour, pre-disclosed in PR #230 CHANGELOG Notes). cutoff_time_filter_structural_check = pass is justified BY DESIGN for the 5 tranche-1 static game-T attributes per CROSS-02-03 §6.1; no strict-< filter applies; the anchor started_at is a row-identity column not a window bound. normalization_fit_scope = training_fold_only is vacuously satisfied because no encoder/scaler was fit at this layer -- raw categorical strings and BOOLEAN values are retained for Phase 03 fold-aware encoder fitting (Invariant I3 normalization-leakage discipline; CROSS-02-02 §9.1 G-CS-6). PR #230 audit JSON at 02_01_01/leakage_audit_sc2egset.json remains byte-unchanged (features_audited == [] historical record preserved at distinct path). EXAMINER-CLARITY: `started_at` is projected as a row-identity anchor only (CROSS-02-00 §5.1 line 360 = CONTEXT; PR #234 Q2(a) use_as_window_bound = false, use_as_row_identity = true; PR #234 Q2(b) Phase-03 chronological-hold-out binding is RECOMMENDATION ONLY) and is excluded from `features_audited`. The 11 output columns partition into 3 projected identity columns (`focal_match_id`, `focal_player`, `opponent_player`), 1 projected context anchor (`started_at`), and 7 audited PRE_GAME feature columns (the exact contents of `features_audited` above). Only the 7 audited columns are model features; the 3 identity columns are lineage / split keys; the 1 context anchor is a row-identity anchor never consumed as a numeric/categorical feature."
}
```

**Audit MD content** (8 sections; SQL verbatim per Invariant I6):

- **§1 Non-overclaim disclaimer.** Step 02_01_02 not closed by this PR (closure deferred). Feature Parquet persisted (11 projected columns: 3 identity + 1 context anchor + 7 audited features). PR #230 audit JSON at distinct path is unchanged. CROSS-02-01 §5 gate condition mechanically satisfied: `features_audited != []` (= 7 PRE_GAME feature columns), verdict = PASS, JSON+MD present. **Examiner-clarity sentence (verbatim):** "`started_at` is projected as a row-identity anchor only (CROSS-02-00 §5.1 line 360 = CONTEXT; PR #234 Q2(a) use_as_window_bound = false) and is excluded from `features_audited`."
- **§2 Materialization SQL + source-binding justification.** The full `_MATERIALIZATION_QUERY` from T02, verbatim. **(N2 implementation, per revision constraint 7-N2):** Immediately after the SQL block, include a 1-paragraph "registry-cell upstream-source → MFC cleaned-view binding" justification quoting `matches_flat_clean.yaml:178-189` verbatim:
  > ```yaml
  > provenance:
  >   source_tables:
  >   - replay_players_raw
  >   - replays_meta_raw
  >   - player_history_all
  >   join_key: NULLIF(regexp_extract(filename, '([0-9a-f]{32})\.SC2Replay\.json', 1),
  >     '') AS replay_id
  >   filter: true_1v1_decisive CTE (exactly 2 players, 1 Win + 1 Loss); mmr_valid CTE
  >     (no MMR<0 player in replay)
  >   scope: True 1v1 decisive replays only. 22,209 replays, 44,418 rows (2 per replay).
  >   created_by: sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py
  >   addendum_by: sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_02_duration_augmentation.py
  > ```
  >
  > The registry CSV (`02_01_01_feature_family_registry.csv`) rows 2, 5, 6 cite `replay_players_raw` (race-pair, matchup, is_mmr_missing) and rows 3, 4 cite `matches_flat` (map, patch) as the *upstream* `source_table_or_event_family`. The Layer-2 materialization reads ALL 5 columns from `matches_flat_clean` (the cleaned 1v1-scoped VIEW). This is consistent: per the `matches_flat_clean.yaml:178-189` provenance block above, MFC is a cleaned + 1v1-scoped projection over `[replay_players_raw, replays_meta_raw, player_history_all]`. The 1v1 cleaning filter (`true_1v1_decisive` CTE: exactly 2 players, 1 Win + 1 Loss) reduces upstream `matches_flat` (89,944 rows) to `matches_flat_clean` (44,418 rows = 22,209 1v1 replays × 2 rows). The registry's `source_table_or_event_family` cell preserves the *upstream* table binding (the registry is NOT amended by this PR); the materialization-layer binding to the cleaned VIEW is recorded here in the audit MD §2 as the authoritative location. The cleaned view inherits the cited upstream columns natively. This binding is consistent with PR #234 Q1 adjudication (`matches_flat_clean` ratified as the source layer).
- **§3 Sanity-check SQL + results.** All 7 sanity-check queries from T02, verbatim, each followed by `-- Result: <value>` per Invariant I6. Empirical results: `COUNT(*) = 44418`, `COUNT(DISTINCT focal_match_id) = 22209`, focal-rows-per-match check returns 0 violating rows, symmetry check = 0, no NULL feature columns, race vocab = `{Prot, Terr, Zerg}` (no Random — matches RATIFY), `is_mmr_missing` distribution `(False=7128, True=37290)`.
- **§4 Cutoff structural check + anchor-classification reiteration.** CROSS-02-03 §6.1 verbatim quote on tranche-1 static-game-T-attribute exemption. Verdict = pass-by-design with justification ≥ 100 words. Explicit statement: the anchor `started_at` is projected onto the feature table as a row-identity column for downstream ordering (Phase 03 convenience); the materialization SQL does NOT use `started_at` as a window-bound filter; if any future Phase-02 step adds history-derived features, those will use the strict-`<` filter per CROSS-02-01 §2.1. **Anchor-classification reiteration:** per CROSS-02-00 §5.1 line 360, `started_at` is CONTEXT (not PRE_GAME); per PR #234 Q2(a) the projected anchor's `use_as_window_bound = false`, `use_as_row_identity = true`; per PR #234 Q2(b) the Phase-03 chronological-hold-out binding is a RECOMMENDATION ONLY (Phase 03 planning binds). Therefore `started_at` is documented in `projected_context_columns` (JSON field) and is excluded from `features_audited` — the 7 audited PRE_GAME feature columns enumerated in §1 are exactly the audited set, with no anchor.
- **§5 POST-GAME token absence.** `_POST_GAME_TOKENS` frozenset listed verbatim. Audit applies boundary-aware token equality (mirrors the existing scaffold validator's pattern) to every column name in the materialized Parquet; result = 0 hits. Audit also applies substring containment to the materialization SQL text (literal source-table allowlist check `_ALLOWED_SOURCE_TABLES`); result = no tracker / no PH / no raw read.
- **§6 Normalization fit-scope.** `training_fold_only` is the spec-permitted value; vacuously satisfied because no encoder/scaler is fit at this layer. Raw categorical strings (`focal_race, opponent_race, race_pair, map_type, patch_version`) and BOOLEAN (`focal_is_mmr_missing, opponent_is_mmr_missing`) retained for Phase 03 fold-aware fitting (CROSS-02-02 §9.1 G-CS-6). The 7-features framing is reiterated: only these 7 PRE_GAME columns are subject to encoding decisions; `started_at` is excluded because it is a CONTEXT anchor (not a feature to be encoded).
- **§7 Reference-window assertion.** sc2egset ref_start=2022-08-29 / ref_end=2022-12-31 per `leakage_audit_sc2egset.json` Phase-01 file (CROSS-02-01 §2.4). The materialization output spans `started_at MIN = 2016-01-07 / MAX = 2024-12-01` (per PR #234 MD §3) — strictly larger than the reference window. Verdict = pass (no contraction of the reference window has occurred at the materialization layer; Phase 03 will sub-sample the reference window).
- **§8 Non-substitution + lineage + Phase-03 NON-binding.** This audit does NOT replace PR #229 §10 design-time verdicts, does NOT replace PR #230 vacuous catalog-only audit, does NOT replace PR #234 adjudication. The Phase-03 RECOMMENDATION from PR #234 Q2(b) (`started_at TIMESTAMP` for chronological hold-out) is projected here as a column for downstream convenience; the binding decision remains with Phase 03 planning. CROSS-02-02 §6.1 minor amendment (proposed in PR #234 §8) remains PROPOSED only — NOT applied here.

### T06 — Per-dataset research_log entry

Path: `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` — APPEND-ONLY new entry at the top per template at `docs/templates/research_log_entry_template.yaml`. Required sections per `.claude/ml-protocol.md` line 56-60: What, Why, How (reproducibility), Findings, Decisions taken, Decisions deferred, Thesis mapping, Open questions / follow-ups. Optional sections used: What this means, Acknowledged trade-offs, Scope notes.

Entry content highlights:

- **Category:** A (science / Phase 02 / materialization)
- **Branch:** `feat/sc2egset-02-01-02-pre-game-materialization`
- **PR:** PR #<N>
- **Step scope:** Step 02_01_02 — first materialization of the 5 tranche-1 pre_game families; Step closure NOT claimed (deferred to U2.B PR).
- **closure_status:** `still_open`
- **leakage_audit_state:** `post_materialization_pass`
- **What:** Persisted 02_01_02 Parquet feature table (44,418 rows × 11 projected cols = 3 identity + 1 context anchor + 7 audited PRE_GAME feature cols) + CROSS-02-01-v1.0.1 post-materialization audit JSON+MD (`features_audited` = exactly 7 PRE_GAME feature columns; verdict = PASS). `started_at` is projected as a row-identity anchor only (CROSS-02-00 §5.1 = CONTEXT) and is excluded from `features_audited`.
- **Why:** First non-vacuous CROSS-02-01 audit; satisfies CROSS-02-01 §5 gate condition mechanically (features_audited non-empty + verdict = PASS + JSON+MD present); preserves PR #230 vacuous-catalog audit at its distinct path.
- **How (reproducibility):** notebook path, module path, validator paths, registry CSV SHA-256, PR #234 binding CSV+MD SHA-256, deterministic UTC date, git_sha.
- **Findings:** all sanity checks pass; race vocab = {Prot, Terr, Zerg} per RATIFY; is_mmr_missing distribution = 7128/37290; 181 maps; 46 patches; symmetry check 0; row count exactly 44,418; column-role partition exactly mutually disjoint (3 identity + 1 context + 7 audited features).
- **What this means:** Step 02_01_02 has now produced its first feature artifact + first non-vacuous leakage audit; the next 02_01 step (history_enriched_pre_game, Step 02_01_03+) remains DEFERRED.
- **Decisions taken:** RATIFY (per PR #234); 11 projected output columns (3 identity + 1 context anchor + 7 audited features); raw categorical retention (no encoding now); separate closure PR (U2.B).
- **Decisions deferred:** Step closure (separate PR); spec amendments proposed in PR #234 §8; Phase 03; history families.
- **Thesis mapping:** Chapter 4 §4.5 (feature engineering plan) — citable as the first non-vacuous CROSS-02-01 audit row.
- **Open questions / follow-ups:** schedule formal closure PR (separate planner-science round); decide whether 02_01_03 may begin before formal closure (likely yes per the same pattern as 02_01_01 → 02_01_02).
- **Scope notes:** does NOT touch root `reports/research_log.md`; does NOT touch ROADMAP body; does NOT touch any spec or cleaning-layer YAML.

### T07 — Release tail + scope verification (Layer-2)

- `pyproject.toml` 3.69.0 → 3.70.0 (feat minor per git-workflow rule "minor for feat"; new on-disk feature artifact + audit pair + module + tests + research_log entry).
- `CHANGELOG.md` `[Unreleased]` → `[3.70.0] — <YYYY-MM-DD> (PR #<N>: feat/sc2egset-02-01-02-pre-game-materialization)`. Added: feature Parquet, audit JSON, audit MD, module, tests, research_log entry, notebook update. Notes: Step 02_01_02 NOT closed (deferred); PR #230 vacuous audit unchanged at distinct path; PR #234 adjudication artifacts SHA-256 bonded.
- `planning/INDEX.md`: archive line update for PR #234 (already merged at `93240b19`); new Active line for this PR.
- Final scope check: tracked diff = exactly the 11 entries in the Layer-2 manifest below (= 11 distinct files; the paired notebook is 1 logical update with 2 manifest rows for the `.py` and `.ipynb` jupytext pair); no extra file; no STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS flip; no spec/YAML edit; no ROADMAP body edit; no Phase-03 file.

### Falsifiers (Layer-2 validator + reviewer enforce; any fired falsifier HALTS the Layer-2 PR before commit)

- **F-row-count-mismatch.** `COUNT(*) FROM materialized_pre_game_features != EXPECTED_OUTPUT_ROW_COUNT` (44,418). Halts; routes to a new planner-science round.
- **F-focal-rows-per-match-violation.** `_FOCAL_ROWS_PER_MATCH_QUERY` returns any row (cnt != 2 for any focal_match_id).
- **F-symmetry-violation.** `_SYMMETRY_CHECK_QUERY` returns non-zero (Invariant I5).
- **F-null-feature.** Any non-identity feature column has NULL count > 0.
- **F-race-vocabulary-drift.** `_RACE_VOCAB_QUERY` returns any value not in `EXPECTED_RACE_VOCABULARY = {Prot, Terr, Zerg}`. (RATIFY enforcement: Random must not leak in via `selectedRace`.)
- **F-is-mmr-missing-distribution-drift.** TRUE/FALSE counts diverge from `(37290, 7128)`. Tight tolerance: cause to halt unless DuckDB file changed.
- **F-map-distinct-drift.** `distinct_map_count != EXPECTED_MAP_DISTINCT_COUNT` (181).
- **F-patch-distinct-drift.** `distinct_patch_count != EXPECTED_PATCH_DISTINCT_COUNT` (46).
- **F-selectedRace-projected.** Output column set contains `selectedRace` or any column with substring `selected_race`. (RATIFY enforcement.)
- **F-post-game-token-projected.** Boundary-aware token equality detects any POST_GAME token in `EXPECTED_OUTPUT_COLUMNS` (CROSS-02-01 §2.2).
- **F-scalar-mmr-projected.** Boundary-aware token equality detects any column matching `FORBIDDEN_SKILL_TOKENS` from the existing scaffold validator (mmr, rating, elo, glicko, skill, mu, sigma) — except the approved missingness flags.
- **F-tracker-source-read.** The materialization SQL text contains substring `tracker_events_raw` or `player_history_all` — outside `_ALLOWED_SOURCE_TABLES`.
- **F-history-window-leakage.** The materialization SQL contains `<` or `<=` between two timestamp columns (no history window allowed for tranche-1). (Sanity guard against accidental `WHERE started_at < ...`.)
- **F-unexpected-source-table.** The audit module's source-table allowlist check finds a join to a table not in `_ALLOWED_SOURCE_TABLES`.
- **F-pr234-binding-hash-mismatch.** The on-disk SHA-256 of `02_01_02_source_anchor_race_adjudication.csv` differs from the value recorded in the audit JSON (provenance bond falsifier).
- **F-features-audited-empty.** `len(features_audited) == 0` (the gate failure that PR #230 deliberately admitted via §5(a) vacuity; CANNOT recur here).
- **F-features-audited-not-7 (NEW per revision constraint 5).** `len(features_audited) != 7` OR `set(features_audited) != set(EXPECTED_AUDITED_FEATURE_COLUMNS)`. Tighter than F-features-audited-empty: this enforces the exact 7-tuple and prevents accidental inclusion of identity columns or the context anchor.
- **F-context-column-counted-as-feature (NEW per revision constraint 5).** `started_at IN features_audited` OR any identity column in `features_audited`. Forbids treating `started_at` (CONTEXT per CROSS-02-00 §5.1) or any identity column as a model feature. Mutually-disjoint role-partition guard.
- **F-audit-verdict-not-pass.** `verdict != "PASS"`.
- **F-encoder-fit.** Any sklearn `Pipeline.fit_transform` call or any `df.mean()` / `df.std()` before split (CROSS-02-01 §2.3). Vacuously satisfied if no encoder is fit (raw retention policy).
- **F-status-flip.** The diff touches `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` (closure deferred to U2.B PR; if reviewer-adversarial chooses U2.A this falsifier is suspended for that decision).
- **F-roadmap-body-edit.** The diff touches the ROADMAP body (any line not in the Step 02_01_02 stub block already committed; the stub itself remains untouched).
- **F-spec-amendment.** The diff touches any `reports/specs/*` file or any `data/db/schemas/views/*.yaml` file.
- **F-phase03-creep.** Any Phase 03 file or content (e.g., `03_*` directory or `Phase 03` non-marker prose) appears in the diff.
- **F-pr230-audit-mutated.** `02_01_01/leakage_audit_sc2egset.json` differs byte-wise from the master version (the historical vacuous audit is at a distinct path; must remain unchanged).
- **F-closure-overclaim.** Audit JSON `notes` field omits the "Step 02_01_02 NOT closed by this PR" string (under U2.B); changelog or research_log overclaims Step closure.
- **F-examiner-clarity-sentence-missing (NEW per revision constraint 6).** Audit JSON `notes` does NOT contain both substrings: "`started_at` is projected as a row-identity anchor only" AND "excluded from `features_audited`"; OR audit MD §1 does not contain the verbatim sentence.
- **F-batching.** The PR diff includes any Step 02_01_03+ content, any Phase 03 content, any spec patch, any cleaning-layer YAML patch — batching beyond the materialization scope.

### T08 — Mandatory ChatGPT second-pass leakage review (REQUIRED — see U3.A)

The Layer-1 plan body contains the complete `_MATERIALIZATION_QUERY` (T02 above), sufficient for ChatGPT review. **This planning PR satisfies the chat-second-pass review prerequisite by providing the SQL in writing**, but does NOT itself execute the review. The user submits the SQL to ChatGPT (with a leakage-review prompt summarising: source = MFC, anchor = started_at TIMESTAMP via MHM join, RATIFY race column, focal/opponent symmetric self-join on `(replay_id, toon_id)`, no `<` filter applies per CROSS-02-03 §6.1, 11 output columns = 3 identity + 1 context anchor + 7 audited features); ChatGPT verdict relayed back to the user.

**If ChatGPT raises a blocker**, the response is a focused-revision planner-science turn to this Layer-1 plan (NOT a separate PR), then re-merge of Layer 1 with the updated SQL. If ChatGPT APPROVES, Layer-2 execution begins.

This chat review is DISTINCT from the reviewer-adversarial Layer-2 gate; both must clear. The Layer-2 plan body MUST cite the ChatGPT verdict (with date + summary) in its `## Open Questions` section as a reference (per N3, see Gate Condition 12 below — the verdict is **quoted verbatim with its ISO date**, not summarised).

## File Manifest

| File | Action | Layer |
|------|--------|-------|
| `planning/current_plan.md` | Create (this plan) | 1 (this turn — 2-file diff) |
| `planning/current_plan.critique.md` | Create (reviewer-adversarial pre-execution gate output) | 1 (this turn) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.py` | Update (append materialization + audit cells; preserve scaffold cells for lineage) | 2 (future) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.ipynb` | Update (jupytext-paired notebook) | 2 (future) |
| `src/rts_predict/games/sc2/datasets/sc2egset/materialize_pre_game_features.py` | Create (materialization + audit module) | 2 (future) |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_pre_game_features.py` | Create (mirrored-tree test file; 19 tests) | 2 (future) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet` | Create (44,418 rows × 11 projected cols = 3 identity + 1 context anchor + 7 audited features; ZSTD; 100k row-groups) | 2 (future) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json` | Create (CROSS-02-01-v1.0.1 §3 schema; non-vacuous; `features_audited` = exactly 7 PRE_GAME feature columns; verdict = PASS) | 2 (future) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.md` | Create (8-section MD; verbatim SQL per Invariant I6) | 2 (future) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` | Update (append new entry at top per ml-protocol template) | 2 (future) |
| `planning/INDEX.md` | Update (archive PR #234; new Active line for PR #<N>) | 2 (future) |
| `CHANGELOG.md` | Update (`[Unreleased]` → `[3.70.0]`) | 2 (future) |
| `pyproject.toml` | Update (3.69.0 → 3.70.0) | 2 (future) |

**File-count arithmetic (N4 implementation, per revision constraint 7-N4):**

- **Layer-1 tracked diff = exactly 2 distinct files** (`planning/current_plan.md` + `planning/current_plan.critique.md`).
- **Layer-2 tracked diff = 11 distinct files** added/updated on top of Layer 1, presented as **12 manifest rows above** because the jupytext-paired notebook is 1 logical update split across 2 paired files (`.py` + `.ipynb` rows are the same notebook in two formats):
  - 1 paired notebook (counts as 2 manifest rows = `.py` row + `.ipynb` row; the jupytext pre-commit hook keeps them in sync).
  - 5 fresh creates: `materialize_pre_game_features.py` module, `test_materialize_pre_game_features.py`, `02_01_02_pre_game_features.parquet`, `02_01_02/leakage_audit_sc2egset.json`, `02_01_02/leakage_audit_sc2egset.md`.
  - 4 updates: `research_log.md`, `planning/INDEX.md`, `CHANGELOG.md`, `pyproject.toml`.
  - Sum = 1 (paired) + 5 (creates) + 4 (updates) = **10 distinct files added/updated by Layer 2** — wait, recounting: 2 manifest rows for the 1 paired notebook = 2 distinct on-disk files (each paired notebook is genuinely 2 on-disk files); plus 5 creates; plus 4 updates = **11 distinct on-disk files added/updated in Layer 2**.
- **On-disk total when Layer 2 lands on the branch = 13 files** = 2 (Layer 1) + 11 (Layer 2 distinct on-disk files).
- NO `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` flip (closure deferred to U2.B PR); NO `reports/specs/*` patch; NO cleaning-layer YAML patch; NO ROADMAP body edit; NO Phase 03 file.

**U2.B closure PR (Layer 3; separate planner-science round; described for completeness only — NOT this plan's scope):** 4 files: `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` (add `02_01_02: complete`), `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` (re-derive `02_01 = in_progress` per the YAML header rule — pre-disclosed in PR #230 Notes), `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (closure entry: `closure_status: closed`), `CHANGELOG.md` + `pyproject.toml` (patch bump 3.70.0 → 3.70.1 since closure is governance-only with no new artifact).

## Gate Condition

The Layer-2 materialization-execution PR is mergeable iff ALL of:

1. `materialize_pre_game_features(...)` returns `result.passed = True` (`halting_falsifier is None`); `row_count == 44418`; `column_names == EXPECTED_OUTPUT_COLUMNS` (11 projected cols = 3 identity + 1 context anchor + 7 audited features); `materialized_output_paths != ()` (the Parquet path).
2. `run_post_materialization_audit(...)` returns `verdict == 'PASS'`; **`len(features_audited) == 7`** (exactly the 7 PRE_GAME feature columns: `focal_race, opponent_race, race_pair, map_type, patch_version, focal_is_mmr_missing, opponent_is_mmr_missing`); `features_audited == EXPECTED_AUDITED_FEATURE_COLUMNS`; `projected_context_columns == ("started_at",)`; `projected_identity_columns == ("focal_match_id", "focal_player", "opponent_player")`; role tuples are mutually disjoint; `halting_falsifier is None`.
3. `pytest tests/ -v` green (test count includes the 19 new tests in `test_materialize_pre_game_features.py`); coverage ≥ 95% (`fail_under = 95`); ruff + mypy clean (pre-commit hooks).
4. jupytext `.py` / `.ipynb` pair in sync (jupytext pre-commit hook); BOTH staged.
5. The final tracked diff matches the Layer-2 manifest EXACTLY (11 distinct on-disk files added/updated on top of the 2 in Layer 1; 12 manifest rows because the paired notebook spans 2 rows). No STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS flip. No spec / YAML edit. No ROADMAP body edit. No Phase-03 file.
6. The new audit JSON at `02_01_02/leakage_audit_sc2egset.json` has `features_audited` = exactly the 7 PRE_GAME feature columns AND `verdict == 'PASS'`; the historical audit JSON at `02_01_01/leakage_audit_sc2egset.json` remains byte-identical to its master version.
7. The Parquet file `02_01_02_pre_game_features.parquet` exists; `COUNT(*) FROM ... = 44418`; `COUNT(DISTINCT focal_match_id) = 22209`; 11 columns matching `EXPECTED_OUTPUT_COLUMNS`.
8. The audit MD §2 contains the verbatim `_MATERIALIZATION_QUERY` (per Invariant I6) AND the verbatim quote of `matches_flat_clean.yaml:178-189` provenance block (per N2) AND the registry-cell upstream-source → MFC cleaned-view binding paragraph.
9. The audit MD §1 contains the explicit "Step 02_01_02 NOT closed by this PR; closure deferred to a separate PR per planning U2.B" non-overclaim statement AND the examiner-clarity sentence verbatim: "`started_at` is projected as a row-identity anchor only (CROSS-02-00 §5.1 line 360 = CONTEXT; PR #234 Q2(a) use_as_window_bound = false) and is excluded from `features_audited`."
10. PR #229 §10 verdict-audit CSV+MD untouched; PR #230 leakage JSON+MD untouched; PR #234 adjudication CSV+MD untouched; registry CSV+MD untouched.
11. The reviewer-adversarial Layer-2 critique gate is satisfied (recorded in `planning/current_plan.critique.md` on the new branch's planning PR).
12. **(N3 implementation, per revision constraint 7-N3):** The user has relayed the ChatGPT second-pass verdict (default U3.A: relayed during Layer 1 before merge). The Layer-2 plan body's `## Open Questions` section contains the **ChatGPT verdict quoted verbatim** (not summarised) inside a Markdown blockquote, prefixed with the verdict's ISO YYYY-MM-DD date and the model identifier (e.g., "> [2026-05-2X — GPT-5 leakage review]: <verbatim verdict text>"). Reviewer-adversarial Layer-2 gate verifies BOTH that the blockquote exists AND that it carries an ISO date in the YYYY-MM-DD format. If the verdict is summarised rather than quoted verbatim, this gate item FAILS.
13. `pyproject.toml` version bumped 3.69.0 → 3.70.0; `CHANGELOG.md` `[Unreleased]` → `[3.70.0]`.

## Open Questions

- **OQ1 (DOCUMENTED — U2.B selected; reviewer-adversarial may override).** Closure decision = separate closure PR (U2.B). Justification: PR #229 → PR #230 precedent; non-batching sequence step 8 separates research_log from STEP_STATUS as separate increments; reviewer-adversarial Layer-2 gate evaluates materialization correctness, not closure governance. If reviewer-adversarial Layer-1 critique blocks on this (e.g., "the artifact-check predicate in the ROADMAP stub at line 2233-2239 says 'the artifact_check fires only after the future scaffold-and-materialization PR materializes the feature table + the NON-vacuous CROSS-02-01 audit pair' — implying closure can ride Layer 2"), the response is to amend U2.B → U2.A in a focused-revision planner-science turn and rerun reviewer-adversarial. Default remains U2.B unless overridden.

- **OQ2 (DOCUMENTED — U3.A selected).** ChatGPT second-pass timing = during Layer 1 (before Layer-1 merge). Justification: the projection SQL is final at Layer-1 merge time by design; submitting to ChatGPT before Layer-1 merge avoids duplicate review later. The deliverable for U3.A is a 1-2 paragraph user-relayed verdict pasted into the next planning/execution session's chat. If ChatGPT raises issues, this Layer-1 plan is amended.

- **OQ3 (DOCUMENTED — RATIFY).** Race column = `race` (PR #234 Q3 RATIFY); RISK-26 compliance = `documented_gap`. The 1,120 Random player-rows (10 `Rand` + 1,110 normalised-to-`Random` in `selectedRace`) eventually played `Prot/Terr/Zerg` — that played race IS what `race` carries. RISK-26's literal reading would prefer `selectedRace`; the cleaning-layer convention prefers `race`. PR #234 chose RATIFY; this materialization plan honours it. Any future re-litigation requires a new planner-science round + a CROSS-02-02 §6.1 minor amendment PR.

- **OQ4 (DEFERRED to Layer 3 / future planner-science).** Step closure (U2.B) PR scope: status YAMLs + closure-only research_log + version bump (3.70.0 → 3.70.1; patch bump per git-workflow rule because closure adds no new artifact). NOT this plan; NOT Layer 2.

- **OQ5 (DEFERRED to 02_01_03+ planner-science).** History-tranche kickoff: 6 `history_enriched_pre_game` families inherit Source layer = MFC (likely) but ADD `player_history_all` for prior history rows; anchor = `details_timeUTC < target.started_at` strict-`<` per CROSS-02-00 §3.2 + CROSS-02-03 §5.1; cold-start gate G-CS-2..G-CS-5 (CROSS-02-02 §9.1). NOT this plan.

- **OQ6 (DEFERRED to thesis).** Chapter 4 §4.5 citation of the materialization artifact alongside the audit artifact: not authored by this PR; a future Category F thesis writing PR consumes the lineage when chapter 4 §4.5 is drafted. The research_log entry in T06 is the citable source.

- **OQ7 (Layer-2 nit — for reviewer-adversarial Layer-1 attention).** Should the Layer-2 PR include `SET TimeZone = 'UTC'` (CROSS-02-00 §3.3) at the first DuckDB connection in the materialization module's `materialize_pre_game_features` entry point? Default YES — recorded in T01 cell 2 (notebook side) AND in `materialize_pre_game_features` (module side). Reviewer should verify both placements.

### ChatGPT second-pass leakage review verdict (U3.A; resolves OQ2)

> [2026-05-23 — GPT-5.2 Thinking leakage review]: APPROVE. I reviewed the exact `_MATERIALIZATION_QUERY` in PR #235. It projects only static game-T columns from `matches_flat_clean` plus `started_at` from `matches_history_minimal` as a row-identity anchor, contains no target or post-game columns, reads no tracker tables, applies no history-window `<` or `<=` filter, excludes `selectedRace`, and preserves focal/opponent symmetry at the materialized grain. Non-blocking caveat: this approval assumes PR #234 Q3 remains binding — i.e. `race` is accepted under the repo’s documented-gap convention — and that `focal_match_id`, `focal_player`, `opponent_player`, and `started_at` remain excluded from downstream model features.

## Out of Scope

- The 6 `history_enriched_pre_game` families (Step 02_01_03+).
- The 11 `in_game_snapshot` families (Step 02_01_04+ per registry rows 13-24).
- Any tracker-derived feature work (deferred per Invariant I3 + the eligibility CSV constraints).
- Step closure of 02_01_02 (deferred to U2.B Layer-3 PR per OQ1).
- Phase 03 (and any 02_02..02_08) work.
- Any `STEP_STATUS` / `PIPELINE_SECTION_STATUS` / `PHASE_STATUS` flip (closure-only deliverable).
- Any spec amendment (CROSS-02-02 §6.1 minor amendment proposed in PR #234 §8 remains future-PR target).
- Any cleaning-layer YAML edit (`matches_long_raw.yaml`, `matches_history_minimal.yaml`, `matches_flat_clean.yaml`).
- Any thesis chapter / bib / appendix / docs / .claude / AoE2 edit.
- Any encoder/scaler fit (deferred to Phase 03/04 fold-aware fitting).

## Evidence-distinctness ledger (must remain true post-PR)

- **PR #229 §10 design-time verdict audit pair** (`02_01_01_section10_verdict_audit.{csv,md}`): per-family DESIGN-TIME verdicts (26 rows); NOT a leakage clearance; NOT a materialization.
- **PR #230 CROSS-02-01 vacuous audit pair** (`02_01_01/leakage_audit_sc2egset.{json,md}`): `features_audited = []`; PASS-by-vacuity per §5(a); NOT a substitute for the post-materialization audit; remains at distinct path (`02_01_01/...`) and remains byte-identical after Layer 2.
- **PR #233 scaffold + 1 validator** (`02_01_02_pre_game_feature_materialization.{py,ipynb}` + `validate_pre_game_feature_materialization.py`): notebook scaffold + one structural validator; persists nothing; not a leakage clearance.
- **PR #234 adjudication artifact pair** (`02_01_02_source_anchor_race_adjudication.{csv,md}`): 3-decision adjudication recording source-layer / anchor / race-column choices and proposed spec amendments; persists ONE artifact pair; NOT a leakage clearance; NOT a materialization; PR #234 = artifact #4 of 5 in the lineage.
- **THIS plan's eventual Layer-2 PR**: materializes the 5 tranche-1 pre_game families (**11 output columns = 3 identity + 1 context anchor + 7 audited PRE_GAME features**); runs the post-materialization CROSS-02-01 audit; emits `02_01_02/leakage_audit_sc2egset.{json,md}` with `features_audited` = the exactly 7 PRE_GAME feature columns + verdict = PASS; emits feature Parquet; updates research_log + version + CHANGELOG + planning/INDEX. **lineage_position = artifact #5 of 5**. Does NOT close Step 02_01_02 (closure deferred to a separate Layer-3 PR per U2.B). `started_at` is projected as a row-identity anchor only (CROSS-02-00 §5.1 = CONTEXT) and is excluded from `features_audited`.
- **Future Layer-3 closure PR (NOT authorised by this plan)**: flips STEP_STATUS / re-derives PIPELINE_SECTION_STATUS / PHASE_STATUS; appends closure entry to research_log; version patch bump.

All five (six counting the future closure) evidence types are DISTINCT; THIS PR adds the 5th (non-vacuous audit + materialization Parquet) without overclaiming any of the others' coverage.

---

## Pipeline-section-status drift question

**`PIPELINE_SECTION_STATUS 02_01 = complete` remains correct after PR #234 (NOT a drift defect).** Evidence (unchanged from prior plans; reproduced for executor reference):

- `STEP_STATUS.yaml:1-12` header: "Pipeline section is complete when ALL its steps are complete. Pipeline section is in_progress when ANY step is in_progress or complete."
- `STEP_STATUS.yaml:196-200` shows `02_01_01` as the only `02_01_*` entry with status `complete`. No `02_01_02` row.
- Per the header rule, `02_01_01` complete + no `02_01_02` row → ALL steps complete → `02_01 = complete`. Mechanically derived correctly.
- Pre-disclosed in PR #230 CHANGELOG `[3.65.0] Notes` and re-acknowledged in PR #232 `[3.67.0] Notes` + PR #234 `[3.69.0] Notes` (line 56 of the CHANGELOG above).

**This materialization-execution plan continues the precedent:** under U2.B (default), the Layer-2 PR does NOT add `02_01_02` to STEP_STATUS, so `02_01 = complete` remains correct after Layer 2. Under U2.B Layer-3 closure PR, `02_01_02` is added to STEP_STATUS with status `complete` — and per the YAML header rule, **both** `02_01_01` and `02_01_02` are complete → `02_01` remains `complete` (NOT re-derived as `in_progress`). Outcome C is not warranted.

Note correction to PR #230 Notes language: PR #230 disclosed re-derivation to `in_progress` would occur if a future PR adds a successor with status `in_progress`. If the successor lands with status `complete` directly (as proposed here), the section stays `complete`. The re-derivation-to-`in_progress` scenario is conditional on the successor's status, not its existence.

---

## Critique gate (Category A)

This is a Category A plan; per `.claude/rules/data-analysis-lineage.md` "Agent and model routing discipline" and per CLAUDE.md Categories A/F protocol, **adversarial critique is required before any execution begins.**

A full `@reviewer-adversarial` pre-execution gate runs over THIS Layer-1 plan body. If the verdict is APPROVE or APPROVE-WITH-NITS with zero blockers, the parent materialises Layer-1 (2 files only). The parent (orchestrator) is responsible for clearing any stale `planning/current_plan.md`, `planning/current_plan.critique.md`, and `planning/current_plan.critique_resolution.md` before `Write`. The Layer-1 PR itself does not author a critique-resolution artifact.

For THIS focused revision: a lightweight reviewer-adversarial pass over the revised feature-count / anchor framing only is sufficient (the prior full critique returned HOLD-WITH-BLOCKERS on these specific points; the other sections are unchanged and were either APPROVED or nit-only). If the lightweight pass returns APPROVE / APPROVE-WITH-NITS with zero blockers, the parent materialises Layer-1.

---

## Self-check — assumptions I most want `@reviewer-adversarial` to challenge

In rough order of brittleness (top 5):

1. **The 7-audited-feature framing (post-revision).** I'm asserting that `features_audited` is exactly the 7 PRE_GAME feature columns (`focal_race`, `opponent_race`, `race_pair`, `map_type`, `patch_version`, `focal_is_mmr_missing`, `opponent_is_mmr_missing`) — no anchor, no identity. The 11 projected columns partition as 3 identity + 1 context anchor (`started_at`) + 7 audited features. Strong pushback: "CROSS-02-01 §3 / §5 doesn't explicitly forbid including a CONTEXT column in `features_audited`; if PR #234 Q2(a) classifies `started_at` as 'projected row-identity anchor', why not record it as a member of `features_audited` with a clarifying field?" My defence: CROSS-02-00 §5.1 line 360 classifies `started_at` as CONTEXT (not PRE_GAME); CROSS-02-01 §3 / §5 `features_audited` is the list of *materialised feature columns* under audit; PR #234 Q2(a) per the merged adjudication binds `use_as_window_bound = false` AND `use_as_row_identity = true` — neither of those tokens is "model feature". Including `started_at` in `features_audited` would either redefine the semantics of `features_audited` (becoming "all projected columns" rather than "PRE_GAME feature columns under leakage audit") or implicitly upgrade `started_at` from CONTEXT to PRE_GAME, neither of which is authorised. The role partition with separate JSON carriers (`projected_context_columns`, `projected_identity_columns`) keeps the JSON semantics unambiguous: `features_audited` is the canonical list of model features; the other two are documentation-only carriers for the projected non-feature columns. The user's revision constraint explicitly forbade Option Y (8-with-distinguished-anchor); the chosen Option X is exactly the framing above. Reviewer should verify the JSON shape (flat list of 7 strings; no nested structure inside `features_audited`).

2. **U2.B (separate closure PR) vs U2.A (closure rides Layer 2).** I'm defaulting to U2.B. Strong pushback: "the ROADMAP stub at line 2233-2239 explicitly says the artifact_check fires only after the future scaffold-and-materialization PR materializes the feature table + the NON-vacuous CROSS-02-01 audit pair — implying closure can and should ride with materialization." My defence: PR #229 → PR #230 precedent + the non-batching sequence step 8 separating research_log from STEP_STATUS. The ROADMAP stub uses "future PR" (singular) but the lineage rule documents step 8 as separate. Reviewer should pick: U2.B preserves the precedent's clean separation; U2.A simplifies execution by 1 PR. Both defensible; default is U2.B unless reviewer chooses U2.A.

3. **U3.A (chat second-pass DURING Layer 1) vs U3.B (chat second-pass AFTER Layer-1 merge).** I'm defaulting to U3.A. Strong pushback: "you're inserting an out-of-band review into the planner-science gate sequence; the reviewer-adversarial Layer-1 gate should run first, and chat second-pass is the Layer-2 gate." My defence: the projection SQL is the artifact under review; it lives in the Layer-1 plan body; reviewing the SQL after Layer-1 merges duplicates effort. Reviewer should pick.

4. **No `<` filter on `started_at`.** I'm projecting `started_at` onto the feature table WITHOUT any temporal filter, per CROSS-02-03 §6.1's exemption for static game-T attributes. Strong pushback: "this looks like leakage at first glance — `started_at` IS the target match's timestamp; projecting it onto a pre-game feature row could telegraph to a model that the row's target match starts at T." My defence: `started_at` is CLASSIFIED as CONTEXT per CROSS-02-00 §5.1 (verbatim row 4 of §5.1 sc2egset MHM table) — it's a context column, not a pre-game feature. The model can use it as an ordering key but MUST NOT consume it as a numeric feature (Phase 03 ordering convention will exclude it from the feature matrix); critically, this revision's audit JSON excludes `started_at` from `features_audited` (post-revision invariant) and the F-context-column-counted-as-feature falsifier enforces this. The materialization includes it for downstream JOIN convenience; the audit MD §4 documents this explicitly. Reviewer should verify.

5. **DOCUMENTED-3 (registry source_table mismatch).** Registry rows 2-6 cite `replay_players_raw` (race-pair, matchup, is_mmr_missing) and `matches_flat` (map, patch). My materialization reads ALL 5 columns from `matches_flat_clean` (the cleaned 1v1-scoped view). Strong pushback: "you're silently breaking the registry's source_table_or_event_family contract." My defence: MFC inherits from MF + RPM via `01_04_02_data_cleaning_execution.py` per `matches_flat_clean.yaml:178-189` (provenance.source_tables = [replay_players_raw, replays_meta_raw, player_history_all]). MFC is a cleaned + 1v1-scoped projection over those very tables. The registry's source_table cell is the *upstream* source; the materialization-layer binding (MFC) is the cleaned view. The Layer-2 audit MD §2 documents this in writing with the verbatim YAML provenance block (N2 implementation). Reviewer should pick: silently allow the source-layer abstraction OR require a separate Category E spec/registry amendment PR before Layer 2.

Sources:
- (No external web sources — all references are repo files cited inline. The CROSS-02-00 §5.1 anchor classification was verified at `reports/specs/02_00_feature_input_contract.md` line 360 during this revision; the `matches_flat_clean.yaml:178-189` provenance block was verified during this revision.)
