---
plan: plan_sc2egset_01_04_01.md
reviewer: reviewer-adversarial
date: 2026-04-16
verdict: PROCEED WITH FIXES
blockers: 1
warnings: 4
---

# Adversarial Critique — sc2egset 01_04_01 Data Cleaning

## Verdict: PROCEED WITH FIXES

One hard blocker: the R03 MMR exclusion filter breaks the two-player-per-replay invariant. Must be fixed before T09 execution. Four warnings, two of moderate severity.

---

## BLOCKER F01 — R03 row-level MMR filter orphans player rows (T09)

**Location:** T09 `matches_flat_clean` VIEW, `WHERE mf.MMR >= 0` predicate

**Issue:** The plan applies `WHERE mf.MMR >= 0` as a row-level filter in `matches_flat_clean`. This filters individual player rows, not replays. If one player in a 1v1 has MMR < 0, their row is excluded but their opponent's row survives — producing a single-player "match" row in the clean VIEW. All downstream joins and feature pivots assume exactly 2 rows per replay_id. Orphaned rows silently corrupt the dataset.

**Fix:** Change the exclusion to replay-level. In the `true_1v1_decisive` CTE (or a new `mmr_valid` CTE added before T09's final SELECT), add:

```sql
mmr_valid AS (
  SELECT replay_id
  FROM matches_flat
  GROUP BY replay_id
  HAVING COUNT(*) FILTER (WHERE MMR < 0) = 0
)
```

Then join `matches_flat_clean` against `mmr_valid` on `replay_id` so that any replay with at least one MMR<0 player is excluded entirely. The CONSORT count should record how many replays (not rows) were excluded at this step.

**Impact:** Without this fix, `matches_flat_clean` contains orphaned rows. Any downstream feature engineering that pivots on (replay_id, playerID) will produce corrupted wide-format rows. Thesis-grade integrity failure.

---

## WARNING W02 — details_gameSpeed and gd_gameSpeed are CONSTANT columns retained in VIEW (T09)

**Location:** T09 `matches_flat_clean` column list, details_gameSpeed / gd_gameSpeed

**Issue:** Per 01_03_01, these columns are constant across the entire dataset. Retaining them wastes column slots, and their inclusion may confuse thesis readers or downstream pipeline steps that assume all VIEW columns carry information.

**Recommendation:** Exclude both from `matches_flat_clean` and document them in the cleaning registry under a "constant — excluded" rule. Add a validation assertion `COUNT(DISTINCT details_gameSpeed) = 1` in T11 to confirm.

---

## WARNING W03 — gd_isBlizzardMap vs details_isBlizzardMap duplication not verified (T09)

**Location:** T09 column list — both `gd_isBlizzardMap` and `details_isBlizzardMap` may refer to the same underlying fact

**Issue:** The plan includes both columns without verifying whether they are identical. If they are duplicates (same values for every row), including both violates DRY and may inflate apparent feature dimensionality.

**Fix:** Add a pre-VIEW query in T01 or T09: `SELECT COUNT(*) FROM matches_flat WHERE gd_isBlizzardMap != details_isBlizzardMap`. If the count is zero, keep only one column (prefer the details_ prefix for consistency with other columns) and exclude the duplicate.

---

## WARNING W04 — regexp_extract returns '' not NULL on no match (T01, T05)

**Location:** T01 `matches_flat` VIEW definition; T11 post-cleaning validation check for NULL replay_ids

**Issue:** DuckDB's `regexp_extract(filename, '...', 1)` returns an empty string `''` when the pattern does not match — not NULL. The plan's validation check (`WHERE replay_id IS NULL`) will therefore miss non-matching filenames, giving a false-negative quality pass.

**Fix:** In T01, wrap the extraction: `NULLIF(regexp_extract(filename, '([0-9a-f]{32})\.SC2Replay\.json', 1), '')` to convert empty-string misses to NULL. Update T11's validation to assert `COUNT(*) WHERE replay_id IS NULL = 0`.

---

## WARNING W05 — APM=0 flagged but APM is an IN-GAME metric (T06)

**Location:** T06 Rule R06, `matches_flat_clean` FLAG column for APM=0

**Issue:** The plan correctly identifies APM as an IN-GAME metric excluded by I3. However, T06 then proposes adding an `apm_zero_flag` column to `matches_flat_clean`. Adding any APM-derived column to the clean VIEW contradicts the I3 exclusion stated in T09.

**Fix:** Either (a) keep the APM=0 investigation in a notebook cell for documentation only — do not add `apm_zero_flag` to `matches_flat_clean` — or (b) produce a separate investigative notebook/artifact. The clean VIEW should contain no APM-related columns. Ensure T09's column list explicitly excludes APM, SQ, supplyCappedPercent, elapsedGameLoops.

---

## Summary of required changes

| ID | Severity | Location | Action |
|----|----------|----------|--------|
| F01 | BLOCKER | T09 VIEW | Change R03 to replay-level exclusion via `mmr_valid` CTE |
| W02 | WARNING | T09 column list | Remove constant gameSpeed columns; add V assertion |
| W03 | WARNING | T01/T09 | Verify gd_isBlizzardMap == details_isBlizzardMap; drop duplicate |
| W04 | WARNING | T01, T11 | Use `NULLIF(regexp_extract(...), '')` to catch empty-string misses |
| W05 | WARNING | T06, T09 | Drop `apm_zero_flag` from clean VIEW; investigation only |
