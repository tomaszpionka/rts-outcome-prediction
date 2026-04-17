# Critique audit trail — aoec 01_04_02 plan

**Plan:** `planning/current_plan.md` (Category A, branch `feat/01-04-02-aoe2companion`)
**Date:** 2026-04-17
**Cap:** 3 rounds of adversarial review (per user standing directive)
**Final verdict:** APPROVE_FOR_EXECUTION (round 3)

---

## Round 1 — Q1-Q5 framework adversarial

**Scope:** Default proposals vs alternatives for the 5 open questions in the plan (schema YAML authoring, OOS DDL form, ROADMAP closure, missingness flag introduction, additional `*_imputed` flags).

**Verdict:** Lock defaults for Q1, Q2, Q3, Q5. **Override Q4 to HYBRID** — rename `rating_imputed` → `rating_was_null` (cross-dataset alignment with sc2egset `is_mmr_missing` and aoestats `is_unrated`; at cleaning-time nothing has been imputed).

**Patches applied (3):**
1. **Q4 rename** — `rating_imputed` → `rating_was_null` (replace_all across plan + parallel renames `hideCivs_imputed`, `country_imputed`, `team_imputed` → `*_was_null`)
2. **T02/T03 execution-order constraint note** — T02 (PIPELINE_SECTION_STATUS bump) MUST run AFTER T03 (ROADMAP append) to avoid window where status closes section before ROADMAP entry exists
3. **Cell 31 `provenance.notes` harmonisation marker** — documents cross-dataset I8 vocabulary deferral within the YAML itself (not just planning history)

---

## Round 2 — Full-plan adversarial

**Scope:** Scope statement, Problem Statement, Assumptions, Literature, Execution Steps T01-T04, File Manifest, Gate Condition, Out-of-scope.

**Verdict:** REQUIRE_REVISION_BEFORE_EXECUTION. 3 BLOCKER (F1, F2, F5), 4 WARNING (F3, F4, F7, F8), 3 NOTE (F11, F12, F13).

**All 10 patches applied:**

| ID | Severity | Issue | Fix |
|----|----------|-------|-----|
| F1 | BLOCKER | Cell 31 row_multiplicity claim needed cross-reference to upstream 01_04_01 DDL CTE | Added "Upstream CTE: see ...01_04_01_data_cleaning.py lines 478-571 (HAVING COUNT(*)=2 + R03 complementarity filter)" |
| F2 | BLOCKER | `country` rate inconsistency between research_log (13.37%) and ledger (2.2486%) | Added Reconciliation notes subsection in T04 |
| F3 | WARNING | research_log incorrectly grouped `difficulty` (n_distinct=3, RETAIN_AS_IS) with constants (mod, status, n_distinct=1, DROP) | Added Reconciliation notes subsection in T04 |
| F4 | WARNING | Cell 11 row-count assertions hardcoded 61,062,392 / 264,132,745 (I7 violation) | Replaced with `ledger_val("matches_1v1_clean", "matchId", "n_total")` derivation |
| F5 | BLOCKER | Cell 31 `excluded_columns` instruction said "all 7 newly-dropped + 2 prior I3" without enumeration (fragile for executor) | Enumerated 9 entries explicitly with reason annotations |
| F6 | WARNING | Cell 13 retained-column list doesn't include `is_null_cluster` sanity check | Added `assert "is_null_cluster" in CREATE_MATCHES_1V1_CLEAN_V2_SQL` |
| F7 | WARNING | Cell 23 zero-null filter discipline not specified — risk of false positive on `country` (n_null=1373052) and `name` (n_null=37) | Added explicit `ledger.loc[(view==X) & (n_null==0), "column"]` filter + sanity print + sanity assert |
| F8 | WARNING | Q3 still listed as Open Question; needed lock before T02 | Added Q3 LOCKED RESOLUTION block with `STEP_STATUS.yaml:87` and `PIPELINE_SECTION_STATUS.yaml:46, 50` line refs |
| F11 | NOTE | Q5 enumeration omitted `team_was_null` while Out-of-Scope included it | Made Q5 + Resolutions + Out-of-Scope all enumerate 3 cols (hideCivs, country, team); arithmetic 51 cols not 48 if all 4 added |
| F12 | NOTE | `leaderboards_raw.yaml`/`profiles_raw.yaml` field-corrections not in Out-of-Scope (round-1 finding had flagged stale `row_count: 0`) | Appended OOS bullet for these YAML field corrections |
| F13 | NOTE | Literature claim "van Buuren 2018 / 80% drop threshold" was folk reading | Softened: "80% community-heuristic boundary is approximate, not a hard threshold from the cited source" |

---

## Round 3 — Verification pass

**Scope:** Verify the 10 round-2 fixes were correctly applied; look for new issues introduced by patches; final scope/methodology check.

**Verdict:** **APPROVE_FOR_EXECUTION**

- All 10 round-2 fixes verified APPLIED_CORRECTLY
- 3 NEW observations at NOTE level only (no BLOCKER, no WARNING):
  - **N1** — Resolutions vs Open questions sections both list Q1-Q5 (intentional discovery trail; Resolutions section authority is implicit but plan order suggests it supersedes Open questions)
  - **N2** — Line 104 says "25 cells" but Cells 1-32 enumerated; line 171 acknowledges range "25-32 cells execute" — doc inconsistency, no methodology risk
  - **N3** — Cell 26 / Cell 31 / Reconciliation notes rates all internally consistent (15,999,234 / 61,062,392 = 26.20%; 2.25% / 8.30% match)

**Plan is locked. Executor dispatch authorized.**

---

## Cross-round consistency

- **Cap respected:** 3 rounds executed; no further adversarial rounds permitted per user "up to 3 rounds" directive.
- **Round 1 + Round 2 + Round 3 patches:** 13 total text edits across plan (3 round-1 + 10 round-2). No structural redesign required.
- **Plan length:** 516 lines (initial) → 533 lines (after round-2 patches; round-3 verification added no edits).
- **Validator:** `scripts/hooks/check_planning_drift.py` passes after all edits.

---

## Locked resolutions (final)

- **Q1:** Author `matches_1v1_clean.yaml` from scratch with PROSE-FORMAT notes (aoestats convention)
- **Q2:** Documentation-only OOS for leaderboards_raw + profiles_raw; no DDL changes
- **Q3:** Bump PIPELINE_SECTION_STATUS 01_04 → complete; PHASE_STATUS stays in_progress
- **Q4 (HYBRID):** Add missingness-indicator flag named `rating_was_null` (NOT `rating_imputed`)
- **Q5:** Defer hideCivs/country/team `*_was_null` flags to Phase 02; matches_1v1_clean = 48 cols

---

**Next step:** Parent dispatches executor for T01 (notebook authoring), T03 (ROADMAP append — note Q3 LOCKED), T02 (STATUS bump — runs AFTER T03 per round-1 patch), T04 (research_log entry).
