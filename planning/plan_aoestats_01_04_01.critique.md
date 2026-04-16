---
plan: plan_aoestats_01_04_01.md
reviewer: reviewer-adversarial
date: 2026-04-16
verdict: PROCEED WITH FIXES
blockers: 0
warnings: 3
---

# Adversarial Critique — aoestats 01_04_01 Data Cleaning

## Verdict: PROCEED WITH FIXES

No hard blockers. The most significant issue is a potential I5 (symmetric player treatment) violation in the wide-format VIEW design. Requires explicit documentation and mitigation before execution proceeds. Three warnings in total.

---

## WARNING W01 — team=1 assignment is NOT random; wide-format pivot may violate I5 (T06)

**Location:** T06 `matches_1v1_clean` VIEW, wide-format pivot via `p0`/`p1` CTEs

**Issue:** The plan assigns `p0` (team=0) as one player slot and `p1` (team=1) as the other in the wide-format VIEW. From the 01_02_06 EDA artifact, team=1 wins **51.9%** of matches, and the elo_diff distribution is asymmetric: team=1 wins have mean elo_diff of **-18.48** vs. **-0.37** for team=0 wins. This is statistically significant and indicates team assignment is NOT random — it correlates with match outcome.

**Consequence under I5:** I5 requires symmetric player treatment (no privileged player slot). If `p0`/`p1` are used as feature slot labels in downstream modelling without randomisation, the model will learn the team-assignment signal, not match skill. This is a data leakage risk that cannot be fixed in 01_04 alone — but the VIEW design must not bake in the asymmetry.

**Minimum required action for 01_04:**
1. Add a note in the VIEW DDL comment and in the artifact JSON documenting the team-assignment bias finding.
2. Add a boolean column `team1_wins` (or a randomised `player_slot` indicator) to the VIEW to make the asymmetry explicit rather than implicit.
3. Add a research_log entry documenting that downstream feature engineering (01_05+) MUST apply player-slot randomisation before using `p0_*` / `p1_*` column pairs as symmetric features.

**This does not require restructuring the VIEW**, but the bias must be surfaced explicitly and flagged for Phase 02.

---

## WARNING W02 — same-team game_ids silently dropped by INNER JOIN pivot (T06)

**Location:** T06 `matches_1v1_clean` VIEW, INNER JOIN between `p0` and `p1` CTEs

**Issue:** If `players_raw` contains rows where both players are on the same team (team=0+team=0 or team=1+team=1), the INNER JOIN drops those matches silently — neither appears in the exclusion log, nor does the CONSORT count capture them.

**Fix:** Add a pre-join check: `SELECT game_id FROM players_raw GROUP BY game_id HAVING COUNT(DISTINCT team) < 2` and assert the result is empty. If non-zero, add an explicit exclusion rule with a Rule ID and count. Document in the artifact JSON.

---

## WARNING W03 — p99.9 Winsorization threshold is hard-coded without embedded percentile query (T05 ratings → aoe2companion cross-reference)

**Location:** T05 temporal NULL stratification — not directly applicable here. This warning is about the ratings_clean Winsorization that aoestats does NOT need, but the plan should explicitly confirm that ratings_raw does not exist in aoestats (it does not — confirmed by schema YAMLs).

**Clarification needed:** The plan does not reference `ratings_raw` because aoestats has no separate ratings table. This is correct. However, T07's post-cleaning validation should assert `ratings_raw` absence to make this explicit and prevent confusion in thesis write-up.

**Severity:** Low — cosmetic documentation gap.

---

## Summary

| ID | Severity | Location | Action |
|----|----------|----------|--------|
| W01 | WARNING (high) | T06 VIEW design | Document team=1 bias; add explicit column or note; research_log entry |
| W02 | WARNING (medium) | T06 INNER JOIN | Assert no same-team games before JOIN; add to CONSORT if non-zero |
| W03 | WARNING (low) | T07 validation | Assert `ratings_raw` absence in aoestats schema |
