# Adversarial Review — Round 1

**Plan:** `planning/current_plan.md` — Step 01_04_03 sc2egset minimal history VIEW
**Category:** A (Phase work)
**Date:** 2026-04-18
**Reviewer:** reviewer-adversarial (R1)

## Invariant compliance (pre-execution)

- **#3 (temporal < T):** AT RISK — R1-WARNING-1 (string lex ordering across heterogeneous ISO precision).
- **#5 (symmetric treatment):** VIOLATED — R1-BLOCKER-3 (symmetry assertion false-passes under race NULL).
- **#6 (reproducibility):** AT RISK — R1-WARNING-4, R1-WARNING-6.
- **#7 (no magic numbers):** VIOLATED — R1-WARNING-5 (unprovenance'd `32`/`42`).
- **#8 (cross-game protocol):** BROKEN — R1-BLOCKER-2 (3-way dtype split).
- **#9 (pipeline discipline):** RESPECTED.

---

## Findings

### R1-BLOCKER-1 — Race vocabulary contract empirically wrong
Plan asserts `'Protoss'/'Zerg'/'Terran'` (lines 66, 480, 644). Empirical: sc2egset ships `Prot`/`Terr`/`Zerg` 4-char abbreviations, documented in `matches_flat_clean.yaml` line 58 itself. Schema YAML, research_log, MD report will ship a false claim. Fix: use `Prot/Terr/Zerg` OR add a documented expansion step (also subject to R1-BLOCKER-5 harmonization).

### R1-BLOCKER-2 — Cross-dataset dtype harmonization is already broken
Sibling VIEWs at 01_04_02 use 3 incompatible time types:
- sc2egset `details_timeUTC`: VARCHAR
- aoestats `started_timestamp`: TIMESTAMP WITH TIME ZONE
- aoe2companion `started`: TIMESTAMP

The plan's "identical dtypes" claim and A2 assumption ("Phase 02 owns type unification") cannot hold against the committed reality. Either cast in this VIEW, or drop the "identical dtypes" claim. As written, a thesis examiner has a fatal I8 question.

### R1-BLOCKER-3 — Symmetry SQL broken under three-valued logic
`SYMMETRY_I5_ANALOG_SQL` uses `= … AND …` then `NOT (...)`. SQL `NULL = NULL` → NULL. `WHERE NOT (NULL)` excludes the row → asymmetric-but-NULL rows silently PASS. `faction` is nullable upstream (`race` explicitly `nullable: true`). Contract bug; empirical luck (current null-count=0) hides it. Fix: `IS DISTINCT FROM` for nullable comparisons.

### R1-BLOCKER-4 — Misplaced Elo/Glicko/TrueSkill citations
Plan cites Elo (1978), Glickman (1999, 2012), Herbrich et al. (2006), Mitrović (2024) as "methodology citations" for a DuckDB projection VIEW. These are Phase 02 backtest methodology, not Phase 01_04 cleaning. Violates I9 (research pipeline discipline). Thesis examiner: *"Why does your cleaning step cite rating papers?"* — no good answer. Keep Elo/Glicko only as downstream-consumer context, cite cleaning-stage references (manual §4.2, §4.4, van Buuren 2018, Schafer & Graham 2002) as methodology.

### R1-BLOCKER-5 — Faction polymorphism contract silently unachievable
sc2egset: 3 values / 4-char. aoestats: 50+ civilizations / full names. aoe2companion: similar. UNION ALL produces a column whose values are ontologically different under one name (race vs civ). Plan's "I8 satisfied at column-name level" is a fig leaf. Minimum fix: declare `faction` per-dataset polymorphic in schema YAML + document explicit non-naive-join warning. Or defer column until Phase 02.

### R1-WARNING-1 — VARCHAR started_at lex ordering breaks I3
`details_timeUTC` has 7 distinct lengths (22–28 chars) across sub-second precision variants. Lex ordering on ISO-8601 strings is **not** chronologically faithful across mixed fractional digit counts. Plan's `ORDER BY p.started_at` and Phase 02 consumer claim ("temporal anchor for rating loops") are broken. Subsumed by R1-BLOCKER-2 if TIMESTAMP cast happens here.

### R1-WARNING-2 — aoestats sibling ships 1-row-per-match
aoestats `matches_1v1_clean.yaml` line 135 explicitly: *"row_multiplicity: 1 row per match"*. 2-row-per-match contract requires aoestats sibling PR to UNION ALL two SELECTs (swap p0/p1). Feasible but (a) not yet acknowledged in the contract prose, (b) aoestats has a `team1_wins ~52.27% slot asymmetry` warning — naive p0/p1 swap introduces slot bias sc2egset's self-join does not have. Plan should acknowledge this asymmetry in the cross-dataset contract prose.

### R1-WARNING-3 — PIPELINE_SECTION_STATUS flip-flop has no rollback
T01 flips 01_04 → in_progress; T03 flips back. T02 failure leaves 01_04 stuck in_progress with no recovery plan. Halt predicate describes scientific conditions but not status rollback. Fix: document manual rollback step in Halt, or defer the flip to post-T02 success.

### R1-WARNING-4 — Schema YAML `<from DESCRIBE>` placeholders undefined at runtime
Cell 17 writes YAML with literal `nullable: <from DESCRIBE>`. Plan doesn't specify how the notebook converts these to boolean values. Different executors produce different YAML → I6 violated. Fix: spell out the DESCRIBE → boolean translation in cell 17 (pseudocode or named helper).

### R1-WARNING-5 — Magic numbers 32 / 42 in gate predicate
PREFIX_CHECK_SQL uses `length == len('sc2egset::') + 32` (= 42). The `32` comes from replay_id hex length. No citation in the plan. I7 requires every threshold to cite empirical evidence / literature. `matches_long_raw.yaml` join_key regex `[0-9a-f]{32}` is the citation; plan must reference it in PREFIX_CHECK_SQL comment or schema YAML notes.

### R1-WARNING-6 — ORDER BY determinism claim is partially misleading
VIEW ORDER BY is evaluated at query time in DuckDB, not stored. Plan's I6 claim "deterministic sample output" holds for sc2egset alone but cannot guarantee reproducibility under `CREATE TABLE t AS SELECT ... FROM view LIMIT 10` without explicit ORDER BY at the consumer. Minor — reword the I6 invariant claim.

### R1-WARNING-7 — Single-writer lock hazard unacknowledged
`notebook_utils.py` line 119: *"If read_only=False, the caller must close the connection before invoking any CLI commands that write to the same database."* Plan's cell 18 closes the connection but does not explicitly forbid parallel CLI writes during T02. Minor add.

### R1-NOTE-1 — Manual section numbers correct.
### R1-NOTE-2 — notebook_utils imports signatures verified.
### R1-NOTE-3 — Row-count arithmetic 44,418 / 22,209 / 2 empirically correct.
### R1-NOTE-4 — Upstream YAML immutability is aspirational (not mechanized gate).
### R1-NOTE-5 — "No tests" defensible for DDL-only step.

---

## Weakest link

**R1-BLOCKER-2** — dtype asymmetry sinks the I8 "common contract" claim at thesis defense.

## Examiner's questions (not answered by current plan)

1. Why does `faction` combine 3-char SC2 abbreviations and full AoE2 civ names?
2. You claim "identical dtypes" — your siblings ship TIMESTAMPTZ and TIMESTAMP. Explain.
3. Demonstrate a NULL-faction row is caught as a symmetry violation.
4. Why does a cleaning step cite rating papers?
5. Prove VARCHAR lex-ordering across 7 sub-second formats is chronologically faithful.

## Verdict

**VERDICT: REQUIRE_REVISION** — 5 BLOCKERs, 7 WARNINGs, 5 NOTEs.
