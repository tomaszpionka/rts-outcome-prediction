---
verdict: REVISE_BEFORE_EXECUTION
plan_reviewed: planning/current_plan.md
revision_reviewed: 1
reviewer_model: claude-opus-4-7[1m]
date: 2026-04-17
findings:
  - id: BLOCKER-1
    severity: BLOCKER
    title: "DS-SC2-01 MMR DDL prose internally inconsistent (NULLIF + DROP simultaneously)"
    description: |
      §1 line 86 says "Convert MMR=0 to NULL via NULLIF inside ... SELECT lists,
      then drop the resulting MMR column" but lines 96-97 say "remove `mf.MMR`
      from SELECT; keep `CASE WHEN mf.MMR = 0 THEN TRUE ELSE FALSE END AS
      is_mmr_missing` (already present)". If MMR is dropped, NULLIF is
      unnecessary; matches_flat is unchanged so `mf.MMR` is still readable in
      the CASE expression. Pick one path and write the literal final SELECT.
    investigated_concern: A
  - id: BLOCKER-2
    severity: BLOCKER
    title: "matches_flat_clean column count contradicts itself (30 vs 28)"
    description: |
      §2 line 387 states "49 cols → 30 cols (drop 19)" but lines 397-399 self-correct
      to 21 drops → 28 cols. §3.6, §4 ROADMAP gate, and Gate Condition all use 28.
      Fix line 387; delete the recount-scratch.
    investigated_concern: A
  - id: BLOCKER-3
    severity: BLOCKER
    title: "Forbidden-column assertion list (§3.3) inflates beyond 21 drops"
    description: |
      §3.3 conflates two categories: 21 newly-dropped cols + columns that were
      never SELECTed in matches_flat_clean (gd_gameSpeed, gd_isBlizzardMap,
      4 colour cols, etc.). cleaning_registry would double-count. Restructure
      into (3.3a) newly-dropped and (3.3b) verify-still-absent-from-prior-PRs.
    investigated_concern: D
  - id: BLOCKER-4
    severity: BLOCKER
    title: "is_decisive_result derived from POST-GAME with no I3-defensible justification"
    description: |
      §1 DS-SC2-04 adds `(mf.result IN ('Win','Loss')) AS is_decisive_result` to
      player_history_all. `result` is POST-GAME of game T. Adding a post-game-
      derived flag to player_history_all is technically defensible because
      player_history_all is the historical-features input, but the plan does
      not state Phase 02 must filter `match_time < T` before aggregating. Risk:
      Phase 02 implementer writes `mean(is_decisive_result)` over a window
      including T, leaking target. Fix: add explicit notes='POST_GAME_HISTORICAL
      — must be filtered match_time < T before aggregation' to the new
      is_decisive_result schema row.
    investigated_concern: B
  - id: BLOCKER-5
    severity: BLOCKER
    title: "is_apm_unparseable derivation has same I3 risk as is_decisive_result"
    description: |
      APM is correctly classified IN_GAME_HISTORICAL. The new
      `is_apm_unparseable = (mf.APM = 0)` flag inherits IN_GAME provenance
      and must carry the same notes='IN_GAME_HISTORICAL — filter match_time
      < T before aggregation' label.
    investigated_concern: B
  - id: WARNING-1
    severity: WARNING
    title: "DS-SC2-09 has circular justification"
    description: |
      "The planner's override here applies the same logic that DS-SC2-10 (APM)
      and DS-SC2-09 (handicap) were left non-binding for" — references
      DS-SC2-09 inside DS-SC2-09's own justification. Rewrite to cite DS-SC2-08
      (constants policy) rather than itself.
    investigated_concern: A
  - id: WARNING-2
    severity: WARNING
    title: "DS-SC2-04 deferral framing weak; should explicitly cite B6"
    description: |
      Plan §1 DS-SC2-04 cites Manual §4.2 for the override but does not name
      the audit's B6 deferral mechanism that makes the override admissible.
      Strengthen the rationale by citing B6 framework explicitly.
    investigated_concern: A
  - id: WARNING-3
    severity: WARNING
    title: "Schema YAML format unspecified"
    description: |
      §5 cell 26 says "Mirror player_history_all YAML structure" but the
      template at docs/templates/duckdb_schema_template.yaml uses a different
      shape (Section A with `value:` / `required:` markers). Plan must declare
      which is canonical for matches_flat_clean.yaml.
    investigated_concern: E
  - id: WARNING-4
    severity: WARNING
    title: "Schema YAML lacks explicit add/drop manifest with column ordering"
    description: |
      §6 line 691 cell 25 specifies the ops on player_history_all.yaml but not
      the literal final 37-col list or ordering of new columns. For YAML diff
      review, ordering matters.
    investigated_concern: E
  - id: WARNING-5
    severity: WARNING
    title: "PIPELINE_SECTION_STATUS closure not documented vs ROADMAP"
    description: |
      §6 closure of 01_04 is on planner judgement against Manual §4 sections.
      Prior revert (commit 7d0463d) closed 01_04 prematurely. Plan should cite
      ROADMAP cross-check explicitly + reference why the prior reversion no
      longer applies.
    investigated_concern: F
  - id: NOTE-1
    severity: NOTE
    title: "§2 lines 389-399 contain visible scratch-recount work"
    description: "Replace with cleaned final breakdown."
    investigated_concern: A
  - id: NOTE-2
    severity: NOTE
    title: "§1 DS-SC2-08 line 252 contains visible self-correction"
    description: "Cleanup the recount prose; cite the verified count of 12 directly."
    investigated_concern: A

verified_correct:
  - "DS-SC2-01..03 ledger rows support DROP per Rule S4 (MMR 83.95%/83.65%, highestLeague 72.04%/72.16%, clanTag 73.93%/74.10%)"
  - "DS-SC2-04 ledger row confirms n_sentinel=26 with rec=EXCLUDE_TARGET_NULL_ROWS — plan's RETAIN+flag is documented planner override (defensible per Manual §4.2 indicator-column pattern)"
  - "DS-SC2-08 ledger has exactly 12 go_* constant rows in matches_flat_clean"
  - "DS-SC2-09 handicap ledger row confirms 2 anomalies in 44,418/44,817 at 0.0045%; original rec=CONVERT_SENTINEL_TO_NULL with B6 non-binding flag"
  - "DS-SC2-10 APM ledger row confirms 1,132 sentinels at 2.53% in player_history_all only"
  - "Symmetry assertion §3.2 well-defined; pattern reused from 01_04_01"
  - "No raw table modifications proposed (Assumption explicitly excludes)"
  - "matches_flat_clean stays PRE_GAME-only per I3 (APM/SQ/supplyCappedPercent/header_elapsedGameLoops absent in current DDL and final list)"
  - "Math is correct: 49-21=28; 51-16+2=37"
  - "Prior PR commit messages a98b3b6 and 19a70fd referenced and verified — POST-GAME and IN-GAME removals from prior PRs are stable"

locked_decisions_check:
  user_approved_DS_SC2_01_to_10: pass
---

# Adversarial Review — sc2egset 01_04_02 plan

## Verdict: REVISE_BEFORE_EXECUTION

The plan is structurally sound and the empirical evidence supports nearly every per-DS resolution against the ledger CSV. **5 BLOCKERs prevent execution as written:**
- 2 methodology issues (BLOCKER-4/5: I3 risk on the new POST_GAME and IN_GAME flag columns added to player_history_all)
- 2 specification defects (BLOCKER-2: column-count contradiction; BLOCKER-3: inflated forbidden-column assertion list)
- 1 DDL ambiguity (BLOCKER-1: MMR drop+NULLIF prose internally inconsistent)

All are fixable with localized edits to §1, §2, §3.3, §5 cells 25-26, §6 — no scope expansion, no new audit work, no new census passes.

The user-locked DS-SC2-01..10 decisions stand on solid ledger evidence. The plan's overrides of audit recommendations (DS-SC2-04 EXCLUDE→RETAIN+flag; DS-SC2-09 NULLIF→DROP) are documented and defensible, but DS-SC2-04 should explicitly cite the audit's B6 deferral mechanism (WARNING-2).

## Path to APPROVE

1. **BLOCKER-1:** Rewrite §1 DS-SC2-01 DDL prose: drop `mf.MMR` from SELECT; derive `is_mmr_missing` from `mf.MMR = 0` (matches_flat unchanged). No NULLIF.
2. **BLOCKER-2:** Fix §2 line 387 from "49 → 30 (drop 19)" to "49 → 28 (drop 21)". Delete scratch-recount prose at lines 397-399.
3. **BLOCKER-3:** Restructure §3.3 into (3.3a) newly-dropped (21 cols matches_flat_clean / 16 cols player_history_all) and (3.3b) verify-still-absent-from-prior-PRs (defense-in-depth, not counted in cleaning_registry).
4. **BLOCKER-4:** Add `notes: POST_GAME_HISTORICAL — filter match_time < T before aggregation` to the new `is_decisive_result` schema entry; document the new provenance category in player_history_all.yaml invariants block.
5. **BLOCKER-5:** Add `notes: IN_GAME_HISTORICAL — filter match_time < T before aggregation` to `is_apm_unparseable` schema entry.

After these 5 fixes, verdict moves to APPROVE. WARNINGs (5) and NOTEs (2) are non-blocking but recommend folding in the same revision pass for cleaner audit trail.

## Reproducibility note

This review verified ground truth by direct file reads against the plan + 01_04_01 ledger CSV. All claims about ledger row contents (MMR sentinel rates, go_* constants count, handicap anomalies) are inspectable.
