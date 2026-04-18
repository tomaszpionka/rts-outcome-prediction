# Adversarial Review — Round 2

**Plan:** `planning/current_plan.md` R2
**Round:** R2 of up to 3
**Reviewer:** reviewer-adversarial (R2)
**Date:** 2026-04-18

## Invariant compliance (R2)

- **#3:** RESPECTED (TIMESTAMP cast verified empirically).
- **#5:** RESPECTED (IS DISTINCT FROM validated empirically).
- **#6:** AT RISK — R2-WARNING-3.
- **#7:** AT RISK — R2-WARNING-1 (citation path wrong).
- **#8:** AT RISK — R2-WARNING-2 (aoestats sibling mapping unannotated).
- **#9:** RESPECTED.

## R1 findings — fix verification

- **R1-BLOCKER-1 (race vocabulary):** FIX-VERIFIED. `Prot/Terr/Zerg` now consistent in all 6 plan sites.
- **R1-BLOCKER-2 (dtype split):** FIX-VERIFIED. `TRY_CAST` empirically handles all 3 observed ISO-8601 variants; `typeof()` returns TIMESTAMP.
- **R1-BLOCKER-3 (NULL-unsafe symmetry):** FIX-VERIFIED. Empirical probes: broken-swap → 2 violations; both-NULL-faction symmetric → 0; one-side-NULL → 2.
- **R1-BLOCKER-4 (misplaced citations):** FIX-VERIFIED. Elo/Glicko/TrueSkill in "downstream-consumer context" only; methodology citations are cleaning-stage.
- **R1-BLOCKER-5 (polymorphic faction):** FIX-VERIFIED. Explicit per-dataset vocabulary contract in schema YAML. Thesis defensibility survives as R2-NOTE-2.

---

## New findings (R2)

### R2-WARNING-1 `[NEW]` — I7 citation path is wrong
Plan cites "matches_long_raw.yaml join_key regex `[0-9a-f]{32}`" at 4 sites (lines 254, 313, 392-393, 498-499). The file lives at `data/db/schemas/views/matches_long_raw.yaml`, NOT `schemas/raw/`. An executor grepping `raw/` finds nothing. Pattern also exists at `matches_flat_clean.yaml:159` and `player_history_all.yaml:217`. Fix: pin full path in every citation site.

### R2-WARNING-2 `[NEW]` — aoestats sibling contract mapping unannotated
Plan's A2 and I8 prose commit aoestats sibling PR to emit 2-rows-per-match TIMESTAMP contract but does NOT map aoestats `p0_*`/`p1_*` → (player_id, faction, won). Worst friction: `aoestats.p0_winner` / `p1_winner` are marked `POST_GAME_HISTORICAL` in the aoestats YAML — used as TARGET derivation here, but a future executor won't know which column sources `won`. Fix: one-line mapping table in A2 or I8 prose.

### R2-WARNING-3 `[NEW]` — DESCRIBE row index ambiguous (cell 17)
Plan cell 17 pseudocode: `nullable = (row[col_index_of_null_flag] == 'YES')`. DuckDB `DESCRIBE` returns tuples `(column_name, column_type, null, key, default, extra)` — flag is at index 2, values `'YES'`/`'NO'`. Plan leaves `col_index_of_null_flag` symbolic. Two executors will write two different YAMLs. Fix: pin `row[2] == 'YES'` with inline cite, OR mandate `cursor.description` by-name resolution.

### R2-NOTE-1 — `regexp_extract(...) = ''` semantics uncited
Line 505 asserts DuckDB `regexp_extract` returns `''` on no-match. True in practice but not cited. Cosmetic.

### R2-NOTE-2 — Polymorphic-column design rationale thin
Examiner will ask: *"If consumers MUST game-condition, why UNION ALL at all?"* Plan's answer is "explicit polymorphism contract." Legitimate but thin — one sentence explaining design choice (substrate simplicity / single-projection pipeline) strengthens defensibility.

### R2-NOTE-3 — Gate #2 dtype order / DDL order consistent (no finding).

### R2-NOTE-4 — `null_started_at > 0` non-halt rationale absent
Gate #2 reports null count but does not halt. Defensible (upstream-data issue, not pipeline bug) but plan is silent on rationale. One sentence in Gate prose would close.

### R2-NOTE-5 — SQL literals are complete and pastable (no finding).

### R2-NOTE-6 — Phase 02 citation boundary clean (no finding).

## Persisting findings

- **R2-WARNING-4 `[PERSISTS]`** — A2 contract aspirational until sibling PR ships. Plan relies on "each sibling PR's gate" + DuckDB hard-type-error to catch deviations. Fragile but acceptable — mitigation exists.

---

## Weakest link (R2)

**R2-WARNING-1** — misrouted I7 citation. Executor friction guaranteed.

## Verdict

**VERDICT: APPROVE_WITH_WARNINGS**

R1 BLOCKERs all FIX-VERIFIED. 3 new WARNINGs + 2 NOTEs — all executor-friction, ~15-min patch. R3 available if user wants clean APPROVE.
