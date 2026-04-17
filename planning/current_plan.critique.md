---
verdict: REVISE_BEFORE_EXECUTION
plan_reviewed: planning/current_plan.md
revision_reviewed: 1
reviewer_model: claude-opus-4-7[1m]
date: 2026-04-17
findings:
  - id: WARNING-1
    severity: WARNING
    title: "team1_wins type label oscillates BIGINT vs BOOLEAN within a single plan"
    description: |
      §1 line 92 says "team1_wins (target, BIGINT/BOOLEAN)" (ambiguous slash);
      DDL purpose comment (line 109) says "BOOLEAN; 0/1 strict"; Self-check
      item 1 says "team1_wins BIGINT". Empirical type is BOOLEAN per
      ledger row 22 + DDL `p1.winner AS team1_wins`. If executor copies BIGINT
      into matches_1v1_clean.yaml, schema YAML will declare wrong type.
      Pick BOOLEAN consistently.
    investigated_concern: A
  - id: WARNING-2
    severity: WARNING
    title: "Per-DS sentinel rates lack inline denominators"
    description: |
      §1 cites n_sentinel/pct without inline row-count denominators
      (17,814,947 matches_1v1_clean; 107,626,399 player_history_all). Reader
      must cross-reference Assumptions section. Editorial; add denominators
      inline for auditability.
    investigated_concern: A
  - id: WARNING-3
    severity: WARNING
    title: "§3.6 SQL comments contain hardcoded expected counts; risks executor regression"
    description: |
      Lines 334-337 print expected NULLIF counts as comment literals (4730/188/118/5937).
      Plan disclaims I7-parameterization but executor reading the comments may
      hardcode the constants. Replace literals with placeholder phrasing.
    investigated_concern: B
  - id: WARNING-4
    severity: WARNING
    title: "§4 ROADMAP step block has nested triple-backtick fences"
    description: |
      §4 wraps the step-block content in ```yaml ... ``` AND the inner block
      itself uses ```yaml fences. Nesting is invalid markdown. Add clarification
      sentence telling executor to skip the outer plan-typography fence.
    investigated_concern: A
  - id: NOTE-1
    severity: NOTE
    title: "DS-AOESTATS-04 DROP rationale doesn't explicitly cite ledger RETAIN_AS_IS override"
    description: |
      Plan recommends DROP_COLUMN; ledger says RETAIN_AS_IS. The constants-detection
      branch (W7 fix from 01_04_01 framework) overrides rate-based recommendations
      when n_distinct=1, but this is implicit. Add explicit citation.
    investigated_concern: A
  - id: NOTE-2
    severity: NOTE
    title: "Self-check item 1 propagates the BIGINT label error"
    description: "One-word fix; align with WARNING-1."
    investigated_concern: A
  - id: NOTE-3
    severity: NOTE
    title: "§3.4 should add team1_wins data_type='BOOLEAN' assertion"
    description: |
      The 3 new is_unrated columns get type assertions but the prediction target
      team1_wins doesn't. Given WARNING-1's confusion, an explicit BOOLEAN
      assertion would catch any executor type-mistake.
    investigated_concern: A

verified_correct:
  - "DS-AOESTATS-01: ledger rows 12/13 (team_0/1_elo) confirm n_sentinel=0 in matches_1v1_clean — matches plan RETAIN_AS_IS via F1"
  - "DS-AOESTATS-02: ledger rows 16/20/34 confirm n_sentinel=4730/188/5937 — matches plan §1, §3.5, §3.6 figures verbatim"
  - "DS-AOESTATS-03: ledger row 11 confirms n_sentinel=118 in matches_1v1_clean (3-row delta from raw n_zero=121 explained by 1v1 filter)"
  - "DS-AOESTATS-04: ledger row 9 confirms n_distinct=1.0 in cleaned scope — DROP rationale defensible (modulo NOTE-1)"
  - "DS-AOESTATS-08: ledger rows 4/7 (leaderboard, num_players) confirm n_distinct=1.0 with rec=DROP_COLUMN"
  - "I9 / I3 phase boundary: plan modifies only VIEW DDL; raw tables untouched; is_unrated derives from PRE_GAME old_rating; NULLIF on PRE_GAME values introduces no leakage"
  - "I8 cross-dataset vocabulary: plan Q3 explicitly KEEPS prose-format notes; defers harmonization to CROSS PR"
  - "Forbidden columns: §3.3 split into 3.3a/b/c per sc2egset v2 pattern; final 20-col list contains no I3 violations"
  - "Symmetry: §3.2 explicitly states sc2egset I5 doesn't apply; substitutes aoestats analog (no-duplicate game_id, p0_winner XOR p1_winner, team1_wins=p1_winner)"
  - "STEP_STATUS / PIPELINE_SECTION_STATUS: §6 includes WARNING-5 lesson (grep ROADMAP for 01_04_03+); per-dataset scope respected"

locked_decisions_check:
  Q1_NULLIF_plus_flag: pass
  Q2_DROP_raw_match_type: pass
  Q3_KEEP_prose_format_notes: pass
  Q4_runtime_computed_subgroup: pass

v2_fixes_applied_by_parent:
  WARNING-1: §1 line 92 corrected to "BOOLEAN — verified per ledger row 22 + DDL p1.winner AS team1_wins"; DDL comments unchanged (already BOOLEAN); Self-check item 1 corrected.
  WARNING-2: §1 DS-AOESTATS-02/03/04 rates now cite inline denominators (17,814,947 / 107,626,399).
  WARNING-3: §3.6 SQL comments rewritten as placeholders ("expected_p0_unrated (loaded from ledger row 16)"); literals removed; I7 intent explicit.
  WARNING-4: §4 added explicit fence guidance for executor (copy from `### Step 01_04_02` through closing ` ``` `; skip outer plan-typography fence).
  NOTE-1: §1 DS-AOESTATS-04 cell now explicitly cites the constants-detection branch (W7) as overriding ledger RETAIN_AS_IS when n_distinct=1.
  NOTE-2: Self-check item 1 fixed to "team1_wins BOOLEAN".
  NOTE-3: §3.4 information_schema query now includes team1_wins; expects 4 rows all BOOLEAN.
---

# Adversarial Review Round 1 — aoestats 01_04_02 plan

## Verdict: REVISE_BEFORE_EXECUTION

The plan is methodologically defensible — all 4 user-locked decisions correctly encoded, ledger evidence cited matches the corrected post-PR #140 ledger CSV verbatim, I3/I9 phase boundary respected, prose-format `notes:` vocabulary preserved per Q3, asymmetry-from-sc2egset items explicitly addressed. **No BLOCKER findings.** Verdict is REVISE only because of WARNING-1 (concrete type-attribute inconsistency that, if executor copies the wrong wording into the schema YAML, would write `team1_wins: BIGINT` when empirical type is BOOLEAN). Remaining warnings and notes are editorial-quality fixes.

## Per-concern verification

### Concern A — Per-DS resolution defensibility against ledger evidence

Spot-checked all 8 DS rows against `01_04_01_missingness_ledger.csv`:
- DS-01 (team_0_elo, team_1_elo): n_sentinel=0 confirmed ✓
- DS-02 (p0/p1_old_rating, old_rating): 4730/188/5937 confirmed ✓
- DS-03 (avg_elo): 118 confirmed (3-row delta from raw 121 explained by 1v1 filter) ✓
- DS-04 (raw_match_type): n_distinct=1.0 in scope confirmed; DROP defensible (see NOTE-1)
- DS-05 (team1_wins): BOOLEAN per ledger; **WARNING-1, NOTE-2, NOTE-3** flag inconsistent labeling
- DS-06 (winner): n_null=0 confirmed ✓
- DS-07 (overviews_raw): not in ledger (out-of-scope) ✓
- DS-08 (leaderboard, num_players): n_distinct=1.0 with DROP_COLUMN confirmed ✓

### Concern B — Phase boundary (I9) and temporal discipline (I3)

- No raw modifications proposed ✓
- is_unrated derivation inherits PRE_GAME provenance from old_rating ✓
- NULLIF on PRE_GAME values: no temporal leakage ✓
- See **WARNING-3** for SQL-comment hardcoded counts (I7 intent correct, wording at risk)

### Concern C — Schema YAML vocabulary preservation

- Q3 KEEP prose-format explicitly locked (line 676) ✓
- §5 cells 26/27 mandate prose-format ✓
- Cross-dataset divergence acknowledged + deferred to CROSS PR ✓

### Concern D — Forbidden column adherence

- §3.3 split into 3.3a (newly dropped) + 3.3b (PRs #138/#139 verify-still-absent) + 3.3c (player_history_all retained) ✓
- Final 20-col list contains no I3 violations ✓

### Concern E — STEP_STATUS / PIPELINE_SECTION_STATUS closure

- §6 includes ROADMAP grep requirement per WARNING-5 lesson ✓
- Per-dataset scope respected (aoestats only) ✓
- ROADMAP inspection confirms no 01_04_03+ pre-listed ✓

### Concern F — Cross-dataset symmetry discipline

- §3.2 explicitly states sc2egset I5 doesn't apply (1-row-per-match) ✓
- Aoestats analog (target consistency: p0_winner XOR p1_winner, team1_wins=p1_winner) provided ✓

## Path to APPROVE

Apply the 4 WARNING + 3 NOTE fixes (all editorial; no logic changes). After fixes, plan moves to APPROVE on round 2.
