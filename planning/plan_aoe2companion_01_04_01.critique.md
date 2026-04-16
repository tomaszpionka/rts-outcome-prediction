---
plan: plan_aoe2companion_01_04_01.md
reviewer: reviewer-adversarial
date: 2026-04-16
verdict: PROCEED WITH FIXES
blockers: 2
warnings: 1
---

# Adversarial Critique — aoe2companion 01_04_01 Data Cleaning

## Verdict: PROCEED WITH FIXES

Two blockers must be resolved before execution. The overall cleaning strategy is sound.

---

## BLOCKER F01 — rowid non-determinism in deduplication CTEs (T02, T03, T06)

**Location:** T02 duplicate analysis CTE, T03 won-complement check CTE, T06 `matches_1v1_clean` VIEW definition

**Issue:** The deduplication logic uses `ORDER BY rowid` inside `ROW_NUMBER() OVER (...)`. In DuckDB, `rowid` is not accessible in subquery context and the behaviour is undefined when used inside window functions. This makes deduplication non-reproducible: different query runs may produce different "first" rows.

**Fix:** Replace `ORDER BY rowid` with `ORDER BY started` in all deduplication window function calls. The `started` column (timestamp) provides a deterministic, semantically meaningful tie-break (earliest event wins).

**Impact:** Without this fix, T06's VIEW is non-deterministic. All downstream artifacts built on `matches_1v1_clean` would be unreproducible, violating I6.

---

## BLOCKER F02 — V2 I3 validation checks non-existent columns (T07)

**Location:** T07 post-cleaning validation, check V2

**Issue:** V2 asserts that POST-GAME columns (`new_rating`, `newRating`, `rating_after`) do not appear in `matches_1v1_clean`. None of these columns exist in aoe2companion's schema. The actual POST-GAME columns that must be excluded to satisfy I3 are `ratingDiff` and `finished` (both confirmed PRE/POST-GAME boundary columns per 01_03_03 research log). V2 as written will always pass vacuously, providing zero I3 protection.

**Fix:** Replace V2's column list with the actual aoe2companion POST-GAME columns: assert that `ratingDiff` and `finished` are **not** present in the VIEW's column list, or alternatively assert that the VIEW's column list is an explicit allowlist.

**Impact:** Without this fix, `matches_1v1_clean` may silently include POST-GAME leakage, violating I3. This is a thesis-grade integrity failure.

---

## WARNING W01 — NULL co-occurrence cluster (T04): flag-only justification needs documentation

**Location:** T04, Rule R04

**Issue:** The plan flags the 10-column simultaneous-NULL cluster without excluding those rows. The justification (temporal schema change) is plausible but not verified empirically. The plan does not include a query to confirm the temporal pattern (e.g., `GROUP BY DATE_TRUNC('month', started)` to see whether NULLs concentrate in a specific time window).

**Recommendation:** Before marking R04 as flag-only, add a temporal stratification query in T04 to confirm the NULL cluster is schema-change-era and not random. If it is random, the justification for flag-only (rather than exclude) weakens. Document the empirical result in the artifact JSON.

**Severity:** Non-blocking — the flag-only treatment is defensible if temporal concentration is confirmed.

---

## Summary of required changes

| ID | Severity | Location | Action |
|----|----------|----------|--------|
| F01 | BLOCKER | T02, T03, T06 | Replace `ORDER BY rowid` → `ORDER BY started` |
| F02 | BLOCKER | T07 V2 | Change checked columns to `ratingDiff`, `finished` |
| W01 | WARNING | T04 | Add temporal stratification query; document result |
