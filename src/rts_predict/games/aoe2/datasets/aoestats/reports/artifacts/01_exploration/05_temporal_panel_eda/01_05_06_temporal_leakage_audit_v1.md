# Temporal Leakage Audit v1 -- aoestats

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Step:** 01_05_06

## Q7.1 Future-data check (B1 fix: non-vacuous)

Cohort players with post-reference rows: 235,610
*(These are FUTURE matches for those players, NOT used in PSI reference edges.)*
Gate count (vacuous schema check): 0

## Q7.2 POST_GAME / TARGET token scan

Feature list scanned: ['focal_old_rating', 'avg_elo', 'faction', 'opponent_faction', 'mirror', 'p0_is_unrated', 'p1_is_unrated', 'map']
POST_GAME tokens found: []
TARGET tokens found: []

## Q7.3 Reference window assertion

REF_START = 2022-08-29, REF_END = 2022-10-27, REF_PATCH = 66692: PASSED

## Q7.4 canonical_slot readiness (M6 fix)

canonical_slot present: False
[PRE-canonical_slot] flag active: True
Phase 06 per-slot tagging check: FAILED: 133 per-slot rows missing [PRE-canonical_slot] tag

**AMENDMENT 2026-04-19 (BACKLOG F6 backfill):** The Q7.4 FAILED sub-check above reflects pre-backfill state only. Per `research_log.md` 2026-04-19 BACKLOG F6 entry, 30 per-slot rows were back-tagged `[PRE-canonical_slot]` (15 quarters × 2 features), bringing the post-backfill tagged-rows total to 136. Further resolution 2026-04-20 via PR #185 (BACKLOG F1 + W4) landed the full `canonical_slot VARCHAR` column on `matches_history_minimal`, flipping `canonical_slot present: False → True` at the VIEW level and transitioning the `[PRE-canonical_slot]` flag protocol from ACTIVE to HISTORICAL (per spec §9). AO-R04 RESOLVED resolution cites this audit; the Q7.4 FAILED line is retained as the historical pre-backfill record.

## Overall verdict

**PASS**
