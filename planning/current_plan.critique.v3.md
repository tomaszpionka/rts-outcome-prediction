# Adversarial Review — Round 3 (Final)

**Plan:** `planning/current_plan.md` (R2 + 5 R2 fixes)
**Round:** R3 of 3 (final)
**Reviewer:** reviewer-adversarial (R3)
**Date:** 2026-04-18

## R2 fix verification

- **[FIX-VERIFIED] R2-WARNING-1** — 9 `matches_long_raw.yaml` occurrences inspected; all 6 I7-citation sites now carry full path (`data/db/schemas/views/...` or absolute `src/rts_predict/...`). 3 non-I7 contexts (manifest, research_log, gate immutability) acceptably bare.
- **[FIX-VERIFIED] R2-WARNING-2** — A2b (NEW) spells out aoestats mapping: `p_profile_id → player_id`, `p_civ → faction`, `p_winner → won (TARGET, POST_GAME_HISTORICAL-but-acceptable-here)`. Slot-bias 52.27% acknowledged.
- **[FIX-VERIFIED] R2-WARNING-3** — Cell 17 pins DuckDB DESCRIBE tuple `(column_name, column_type, null, key, default, extra)`; index 2 is null flag; `nullable = (row[2] == 'YES')`. No off-by-one.
- **[FIX-VERIFIED] R2-NOTE-2** — Polymorphic-column design rationale one-sentence present (substrate simplicity + game-conditional encoding inside feature extractors).
- **[FIX-VERIFIED] R2-NOTE-4** — Non-halt rationale present (TRY_CAST failure = upstream data issue, not pipeline bug; Phase 02 decides NULL-anchor handling).

## R3 findings (sweep)

### R3-NOTE-1 — Cell 17 redundant DESCRIBE call
Cell 15 writes `describe_table_rows` into validation JSON; Cell 17 independently re-queries `DESCRIBE`. Harmless but reusable. No correctness issue.

### R3-NOTE-2 — Cell 15 DuckDBPyType JSON serialization
`describe_rows[i][1]` (column_type field) may be `DuckDBPyType` not `str` — `json.dumps` may fail. Risk low (fires immediately); executor will notice. Plan could pin `[str(x) for x in row]`.

### R3-NOTE-3 — Cosmetic: sibling-PR rollback pattern inheritance
Halt-predicate rollback (R1-WARNING-3 fix) is sc2egset-local. Whether aoestats / aoec sibling PRs inherit the pattern is implicit. Out of scope for this PR.

## No new BLOCKER-grade issues. No contradictions introduced by R2 fixes.

## Lens summary

- Temporal discipline: **SOUND**
- Feature engineering: **SOUND**
- Thesis defensibility: **STRONG** (aoestats `p_winner`-as-target acknowledgment defuses likely examiner question)
- Cross-game comparability: **MAINTAINED**

## Weakest link

**R3-NOTE-2** — DuckDBPyType JSON serialization. Cosmetic; not a methodology risk.

## VERDICT: APPROVE_WITH_WARNINGS

Plan is execution-ready. All R1 BLOCKERs closed (R2). All R2 findings verified (R3). 2 cosmetic R3-NOTEs do not block execution — executor picks up at notebook level. **Proceed to execution.**
