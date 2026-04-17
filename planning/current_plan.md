---
category: A
branch: fix/01-04-null-audit
date: 2026-04-17
planner_model: claude-opus-4-7[1m]
phase: "01"
pipeline_section: "01_04"
step: "01_04_02"
dataset: aoe2companion
game: aoe2
predecessor_step: "01_04_01"
predecessor_pr: "Merged 2026-04-17 (aoec missingness audit; PR #134/135 + revisions)"
template_pr: "PR #142 (sc2egset 01_04_02 — pattern-establisher) + PR #144 (aoestats 01_04_02 — first replication)"
sandbox_notebook: "sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py"
artifacts_target: "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/"
critique_required: true
research_log_ref: "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md#2026-04-17-phase-01-step-01_04_02-data-cleaning-execution"
invariants_touched: ["I3", "I5", "I6", "I7", "I8", "I9", "I10"]
source_artifacts:
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.json"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md (Step 01_04_01 block, lines 674-887, decisions_surfaced DS-AOEC-01..08)"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/player_history_all.yaml (current; to be UPDATED)"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/matches_long_raw.yaml (sibling reference; UNTOUCHED)"
  - "sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_01_data_cleaning.py (current VIEW DDL — matches_1v1_clean, player_history_all, ratings_clean)"
  - "sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py (template — PR #144; mirror cell structure)"
  - "src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/matches_1v1_clean.yaml (template format — prose-format notes vocabulary)"
  - "sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py (precedent — PR #142)"
---

# Plan: Step 01_04_02 — Data Cleaning Execution (act on DS-AOEC-01..08)

## Scope

Apply VIEW DDL changes to act on **all 8 cleaning decisions (DS-AOEC-01..08)** surfaced by the 01_04_01 missingness audit, mirroring the aoestats 01_04_02 pattern (PR #144). Modify VIEW DDL for `matches_1v1_clean` and `player_history_all` via `CREATE OR REPLACE` (no raw table changes per Invariant I9). Produce CONSORT column-flow + cleaning registry + post-cleaning assertion battery + schema YAML files. **aoe2companion only** — this is the third and final dataset in the three-PR Option A sequence (sc2egset PR #142 → aoestats PR #144 → aoec PR THIS).

## Problem Statement

The 01_04_01 missingness audit produced an empirical ledger (74 rows × 17 cols across 2 VIEWs) and surfaced 8 cleaning decisions for downstream resolution. Per Manual §4 + the established pattern from PR #142 (sc2egset) and PR #144 (aoestats), these decisions must be ACTED on by 01_04_02 via VIEW DDL modifications. Without this step:

1. `matches_1v1_clean` retains 7 columns that have no defensible analytical role: 4 high-NULL columns (`server` 97%, `scenario` 100%, `modDataset` 100%, `password` 78% — DS-AOEC-01), 1 schema-evolution column (`antiquityMode` 60% — DS-AOEC-02), and 2 zero-information constants (`mod`, `status` — DS-AOEC-03b constants-detection override).
2. The MAR primary feature `rating` (~26.20% NULL in matches_1v1_clean) has no missingness-as-signal flag exposed; Phase 02 imputation cannot distinguish "imputed" from "originally observed" without a `rating_was_null` indicator (DS-AOEC-04 / Rule S4 exception per van Buuren 2018).
3. The `player_history_all` VIEW retains the constant column `status` (n_distinct=1, always 'player') — DS-AOEC-03b.
4. The CONSORT column-count + cleaning registry required by Manual §4.1 + §4.3 is not produced.
5. No `matches_1v1_clean.yaml` schema YAML exists for the aoec dataset (only `player_history_all.yaml` and `matches_long_raw.yaml` are present); the prediction-target VIEW lacks formal schema documentation.
6. The two non-VIEW raw tables `leaderboards_raw` (singleton 2-row reference) and `profiles_raw` (7 dead columns, 100% NULL) lack a formal out-of-analytical-scope declaration in the cleaning registry (DS-AOEC-08).

The pipeline cannot transition `01_04` from `in_progress` → `complete` without this work. Phase 02 (Feature Engineering) cannot begin until `01` closes per `docs/PHASES.md`.

## Assumptions & unknowns

**Assumptions (confirmed by reading source artifacts):**

1. **Ledger empirical evidence is authoritative.** All thresholds in this plan derive from `01_04_01_missingness_ledger.csv` rows (per I7), not from prose narrative. Specifically:
   - `matches_1v1_clean` row count = 61,062,392 (asserted in 01_04_01 notebook; matches every ledger `n_total` for matches_1v1_clean).
   - `player_history_all` row count = 264,132,745 (asserted in 01_04_01 notebook; matches every ledger `n_total` for player_history_all).
   - `matches_1v1_clean` has 54 columns post-01_04_01 (53 from matches_raw projection + `is_null_cluster` derived; ledger has 54 rows for this VIEW).
   - `player_history_all` has 20 columns post-01_04_01 (ledger has 20 rows for this VIEW).
2. **Row counts are unchanged by 01_04_02.** This is a column-only cleaning step; CONSORT-row tables list the same row counts pre/post (asserted in Cell 18 of the notebook).
3. **No `matches_1v1_clean.yaml` exists yet for aoec.** Verified via `ls data/db/schemas/views/` — only `matches_long_raw.yaml` and `player_history_all.yaml` are present. This step CREATES `matches_1v1_clean.yaml`.
4. **Current `player_history_all.yaml` uses prose-format `notes:` vocabulary** (e.g., `"IDENTITY. Temporal join key for feature computation."`) — already consistent with the aoestats convention. Per the user's locked Q3 decision from PR #144, this PR KEEPS that vocabulary; cross-dataset I8 vocabulary harmonization (sc2egset single-token vs aoec/aoestats prose) is deferred to a CROSS PR after all three dataset 01_04_02 PRs land.
5. **DuckDB connection idempotence.** `get_notebook_db("aoe2", "aoe2companion", read_only=False)` returns a writable connection at `data/db/db.duckdb` (per `aoe2/config.py`). The notebook can be re-run safely; `CREATE OR REPLACE VIEW` is idempotent.
6. **The `rating` column in matches_1v1_clean is already filtered to `>= 0` upstream** (per the ledger row `n_sentinel=0` justification quoted from 01_03_03 + this audit: "matches_1v1_clean VIEW asserts `rating >= 0` upstream, so the -1 sentinel is filtered before the audit sees it"). Therefore **NO `NULLIF(rating, -1)` is needed in 01_04_02**; only the `rating_was_null` BOOLEAN flag is added to expose the existing NULL pattern as missingness-as-signal for Phase 02 (DS-AOEC-04).
7. **DS-AOEC-03b is the binding override for `mod` and `status` in matches_1v1_clean.** The ledger shows both with `recommendation=DROP_COLUMN / mechanism=N/A` and `n_distinct=1` — the constants-detection branch overrides the otherwise low-NULL RETAIN_AS_IS spec entries. `difficulty` (n_distinct=3 per ledger) is NOT a constant and stays RETAIN_AS_IS.
8. **`hideCivs` stays in `matches_1v1_clean` as a flag-for-imputation column** (DS-AOEC-02). At 37.18% NULL it falls in the 5–40% FLAG_FOR_IMPUTATION band per van Buuren 2018 / Schafer & Graham 2002. **No `hideCivs_was_null` flag column is added in 01_04_02** — Phase 02 will materialise the indicator alongside its imputation. The current step retains the column verbatim and documents the deferral in the cleaning registry. (This matches how `country` is treated.)
9. **DS-AOEC-07 (target NULLs in player_history_all)** is documentation-only here — the ~0.0073% (n=19,251) NULL `won` rows in player_history_all are NOT physically excluded in the VIEW DDL. The cleaning rule is documented in the registry, and Phase 02 feature computation must apply the WHERE filter at the rolling-window level (Rule S2: never impute the target).
10. **DS-AOEC-08 (`leaderboards_raw` + `profiles_raw`) is documentation-only.** No `DROP TABLE` statements are issued — these tables are simply declared out-of-analytical-scope in the cleaning registry. The raw tables remain on disk per I9.
11. **`ratings_clean` is NOT modified by 01_04_02.** The 01_04_01 step created `ratings_clean` as a Winsorized projection of `ratings_raw`; no DS-AOEC decision touches this VIEW. It is left intact.

**Unknowns (NOT decided here — flagged as Open Questions):**

- Whether to author `matches_1v1_clean.yaml` from scratch with PROSE-FORMAT notes (aoestats convention) or to defer schema YAML authoring to a separate PR. (Q1)
- Whether to formally document `leaderboards_raw` + `profiles_raw` out-of-analytical-scope only in the cleaning registry / research_log, or also drop the schema YAMLs / add DROP TABLE comments. (Q2)
- Whether ROADMAP 01_04 should close (PIPELINE_SECTION_STATUS=complete) after 01_04_02 or whether additional 01_04_03+ steps are pre-listed. (Q3)
- Whether the `rating_was_null` BOOLEAN flag is added in 01_04_02 (this plan's recommendation) or deferred entirely to Phase 02. (Q4)
- Whether `hideCivs` and `country` should also receive `*_was_null` flag columns in 01_04_02 alongside `rating_was_null` (consistency vs. minimal-DDL-change tradeoff). (Q5)

## Literature context

Same canonical citations as 01_04_01 + sc2egset 01_04_02 (PR #142) + aoestats 01_04_02 (PR #144):

- **Rubin, D.B. (1976).** Inference and missing data. *Biometrika* 63(3), 581–592. — MCAR/MAR/MNAR taxonomy carried forward from 01_04_01; underwrites the per-column `mechanism` field in the ledger.
- **Little, R.J. & Rubin, D.B. (2019).** *Statistical Analysis with Missing Data*, 3rd ed. Wiley. — Authoritative mechanism classification.
- **van Buuren, S. (2018).** *Flexible Imputation of Missing Data*, 2nd ed. CRC Press. — Rule S4 (high-missingness columns where imputation is widely considered indefensible per the missing-data literature, e.g., van Buuren 2018 Ch. 1.3 + Little & Rubin 2019 §1) underwrites DS-AOEC-01 (server/scenario/modDataset/password). The 80% community-heuristic boundary is approximate, not a hard threshold from the cited source. Warning against rigid global thresholds underwrites the non-binding nature of CONVERT_SENTINEL_TO_NULL recommendations where `carries_semantic_content=True`.
- **Schafer, J.L. & Graham, J.W. (2002).** Missing Data: Our View of the State of the Art. *Psychological Methods* 7(2), 147–177. — <5% MCAR boundary citation underwrites the RETAIN_AS_IS recommendations for low-rate game-settings columns (DS-AOEC-03).
- **Sambasivan, N. et al. (2021).** Everyone wants to do the model work, not the data work: Data Cascades in High-Stakes AI. *CHI '21*. — Surface decisions explicitly rather than deferring; underwrites the cleaning registry approach.
- **Liu, X. et al. (2020).** CONSORT-AI extension for clinical-trial reports. *BMJ* 370. — Column-count flow tables (CONSORT before/after).
- **Jeanselme, V. et al. (2024).** Participant Flow Diagrams for Health Equity in AI. *JBI* 152. — Subgroup impact reporting in the post-cleaning artifact.
- **scikit-learn v1.8 documentation.** `sklearn.impute.MissingIndicator` doctrine — missingness-as-signal principle for Phase 02; underwrites the `rating_was_null` BOOLEAN flag (DS-AOEC-04).
- **Manual `01_DATA_EXPLORATION_MANUAL.md` §4.1 (cleaning registry), §4.2 (non-destructive), §4.3 (CONSORT impact), §4.4 (post-validation).**

No new citations introduced — this PR continues the 01_04_01 + 01_04_02 framework. [OPINION]: The literature in this plan is treated as a stable corpus carried across the three-dataset Option A sequence; no per-dataset citation drift is expected.

## Execution Steps

### T01 — Author the 01_04_02 paired notebook (data cleaning execution)

**Objective:** Create the jupytext-paired Python+ipynb notebook that executes all 8 DS-AOEC resolutions, replaces the two analytical VIEWs via `CREATE OR REPLACE`, runs the full assertion battery, and emits the post-cleaning validation JSON + MD artifacts. Mirror the aoestats PR #144 cell structure (25 cells) with aoec-specific adaptations.

**Instructions:**

1. **Create the paired notebook file** at the absolute path `/Users/tomaszpionka/Projects/rts-outcome-prediction/sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py` using the same jupytext header used in `sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py`. Pair the `.ipynb` from the `.py` via the project's `sandbox/jupytext.toml`. Cell structure (25 cells; mirror aoestats):

   - **Cell 1 (markdown):** Title + step header with step scope, invariants applied (I3, I5, I6, I7, I9, I10), predecessor (01_04_01), date 2026-04-17, ROADMAP ref 01_04_02.
   - **Cell 2 (code) — Imports:** `import json`, `from pathlib import Path`, `import pandas as pd`, `import yaml`, `from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir, setup_notebook_logging`, `logger = setup_notebook_logging()`.
   - **Cell 3 (markdown) + Cell 4 (code) — DuckDB connection (writable):** `db = get_notebook_db("aoe2", "aoe2companion", read_only=False); con = db.con`. Note in markdown: "WARNING: Close all read-only notebook connections to this DB before running."
   - **Cell 5 (markdown) + Cell 6 (code) — Load 01_04_01 ledger (empirical evidence base, I7):** `reports_dir = get_reports_dir("aoe2", "aoe2companion")`; `ledger_path = reports_dir / "artifacts" / "01_exploration" / "04_cleaning" / "01_04_01_missingness_ledger.csv"`; `ledger = pd.read_csv(ledger_path)`. Print row count, columns, and the relevant `view`,`column`,`n_null`,`n_sentinel`,`pct_missing_total`,`n_distinct`,`mechanism`,`recommendation` slice. Define a `ledger_val(view, col, field)` helper (copy from aoestats notebook). Extract per-column counts at runtime — these go into expected_* variables for the assertion battery (Cell 17). For aoec, the relevant ledger pulls are:
     - `expected_rating_null_clean = int(ledger_val("matches_1v1_clean", "rating", "n_null"))`  (≈ 15,999,234)
     - `expected_rating_null_hist = int(ledger_val("player_history_all", "rating", "n_null"))`  (≈ 104,676,152)
     - `expected_won_null_hist = int(ledger_val("player_history_all", "won", "n_null"))`  (≈ 19,251 — DS-AOEC-07 target NULL count)
   - **Cell 7 (markdown) + Cell 8 (code) — Per-DS resolution log (DS-AOEC-01..08 documentation only):** Build `ds_resolutions` list of 8 dicts (one per DS), each with `id`, `column(s)`, `views`, `ledger_rate` (computed via `ledger_val(...)`), `recommendation`, `decision`, `ddl_effect`. Print each as `f"  {r['id']} ({r['column']}): {r['decision']}"`. No SQL execution in this cell.
   - **Cell 9 (markdown) + Cell 10 (code) — Pre-cleaning column counts (CONSORT before):** `pre_clean_cols = con.execute("DESCRIBE matches_1v1_clean").df()`; `pre_hist_cols = con.execute("DESCRIBE player_history_all").df()`. Reference constants `COLS_BEFORE_CLEAN = 54`, `COLS_BEFORE_HIST = 20` (from 01_04_01 ledger row counts). Print + record reference.
   - **Cell 11 (code) — Pre-cleaning row counts (CONSORT before):** `expected_clean_rows = int(ledger_val("matches_1v1_clean", "matchId", "n_total"))`; `expected_hist_rows = int(ledger_val("player_history_all", "matchId", "n_total"))`. Then `SELECT COUNT(*), COUNT(DISTINCT matchId) FROM matches_1v1_clean`; `SELECT COUNT(*) FROM player_history_all`. Assert `== expected_clean_rows` (≈ 61,062,392) and `== expected_hist_rows` (≈ 264,132,745). Both expected counts are ledger-derived per I7 — NO inline magic numbers. (Improvement over PR #144 aoestats Cell 6 which hardcoded counts directly.)
   - **Cell 12 (markdown) + Cell 13 (code) — Define matches_1v1_clean v2 DDL.** Build `CREATE_MATCHES_1V1_CLEAN_V2_SQL` as a triple-quoted Python string. Critical column changes vs. the 01_04_01 54-column DDL (see Section 3.1 below for full SELECT list):
     - **DROP 7 columns:** `server`, `scenario`, `modDataset`, `password` (DS-AOEC-01); `antiquityMode` (DS-AOEC-02); `mod`, `status` (DS-AOEC-03b constants override).
     - **ADD 1 column:** `(rating IS NULL) AS rating_was_null` (BOOLEAN; DS-AOEC-04 missingness-as-signal flag).
     - **No NULLIF needed** — `rating` is already filtered to `>= 0` upstream; `won` is already `BOOLEAN` and zero-NULL via R03; no sentinel-encoded ratings (unlike aoestats `old_rating=0`).
     - All other columns retained verbatim from the 01_04_01 DDL: identity (`matchId`, `profileId`, `started`, `name`, `filename`), R03/R02-derived (`is_null_cluster`, target `won`), low-NULL game settings (`map`, `difficulty`, `startingAge`, `fullTechTree`, `allowCheats`, `empireWarsMode`, `endingAge`, `gameMode`, `lockSpeed`, `lockTeams`, `mapSize`, `population`, `recordGame`, `regicideMode`, `gameVariant`, `resources`, `sharedExploration`, `speed`, `speedFactor`, `suddenDeathMode`, `civilizationSet`, `teamPositions`, `teamTogether`, `treatyLength`, `turboMode`, `victory`, `revealMap`), MAR-flag-for-imputation (`hideCivs`, `country`), other context (`leaderboard`, `internalLeaderboardId`, `privacy`, `rating`, `color`, `colorHex`, `slot`, `team`, `shared`, `verified`, `civ`).
     - Net: 54 - 7 + 1 = **48 columns.** Preserve the original WHERE/CTE structure (subquery IN approach for the won-complementarity filter — do NOT change the join logic; only adjust the SELECT list).
     - **Cell 13 sanity assertion (per round-2 F6):** `assert "is_null_cluster" in CREATE_MATCHES_1V1_CLEAN_V2_SQL` to prevent silent regression of the R03/R02-derived flag.
   - **Cell 14 (code) — Replace matches_1v1_clean VIEW.** `con.execute(CREATE_MATCHES_1V1_CLEAN_V2_SQL)`.
   - **Cell 15 (markdown) + Cell 16 (code) — Define + replace player_history_all v2 DDL.** Changes vs. the 01_04_01 20-column DDL: **DROP 1 column** (`status` — DS-AOEC-03b constants override). **No additions, no NULLIF.** Net: 20 - 1 = **19 columns.** All other columns retained verbatim. `won` is RETAINED (DS-AOEC-07 documents the EXCLUDE_TARGET_NULL_ROWS rule but does not enforce it physically — Rule S2 is enforced at Phase 02 feature-computation time). `rating`, `country`, `team` retain their FLAG_FOR_IMPUTATION recommendations as deferred-to-Phase-02 metadata.
   - **Cell 17 (markdown) + Cell 18 (code) — Post-cleaning column counts (CONSORT after).** `post_clean_cols = con.execute("DESCRIBE matches_1v1_clean").df()`; `post_hist_cols = con.execute("DESCRIBE player_history_all").df()`. Assert `len(post_clean_cols) == 48` and `len(post_hist_cols) == 19`. Print column names.
   - **Cell 19 (code) — Forbidden-column assertions (Section 3.3a/b/c).**
     - **3.3a (newly dropped in 01_04_02):** `forbidden_clean_new = {"server", "scenario", "modDataset", "password", "antiquityMode", "mod", "status"}`; `forbidden_hist_new = {"status"}`. Assert `forbidden_clean_new & set(post_clean_cols.column_name) == set()` and same for hist.
     - **3.3b (pre-existing I3 exclusions — POST-GAME):** `forbidden_clean_prior = {"ratingDiff", "finished"}`. Assert absent.
     - **3.3c (player_history_all RETAINED):** `required_hist_present = {"won", "rating", "country", "team"}`. Assert present.
   - **Cell 20 (code) — New-column assertion (Section 3.4):** Verify `rating_was_null` is in `post_clean_cols` and is `BOOLEAN` type via `information_schema.columns`. Assert `len(r_bool) == 1` and `data_type == "BOOLEAN"`.
   - **Cell 21 (code) — Zero-NULL identity assertions (Section 3.1):**
     - `matches_1v1_clean`: `matchId`, `started`, `profileId`, `won` must all be 0-NULL. R03 guarantees `won` (50/50 complementarity). Use `COUNT(*) FILTER (WHERE col IS NULL) = 0`.
     - `player_history_all`: `matchId`, `profileId`, `started` must be 0-NULL. (`won` is NOT asserted zero-NULL here — DS-AOEC-07 documents the ~19,251 NULLs.)
   - **Cell 22 (code) — Target consistency assertion (Section 3.2 — aoec analog of R03):** `SELECT matchId, COUNT(*) AS n, COUNT(*) FILTER (WHERE won=TRUE) AS n_true, COUNT(*) FILTER (WHERE won=FALSE) AS n_false FROM matches_1v1_clean GROUP BY matchId HAVING n != 2 OR n_true != 1 OR n_false != 1`. Assert result has 0 rows (R03 invariant: each match has exactly one TRUE + one FALSE).
   - **Cell 23 (code) — No-new-NULLs assertion (Section 3.5):** For each KEPT column in either VIEW that had `n_null=0` per the 01_04_01 ledger, assert `n_null` still = 0. Use the dynamic discovery pattern from aoestats Cell 16. **Explicit filter discipline (per round-2 F7):** `zero_null_cols_clean = ledger.loc[(ledger.view == "matches_1v1_clean") & (ledger.n_null == 0), "column"].tolist()`; same for hist. Iterate ONLY those columns when building `null_checks` SQL. Add sanity prints: `print(f"Zero-null columns to assert: {len(zero_null_cols_clean)} in clean, {len(zero_null_cols_hist)} in hist")` and sanity asserts: `assert "country" not in zero_null_cols_clean and "name" not in zero_null_cols_clean` (both have non-zero `n_null` per ledger; if they appear in this set, the filter is broken). **Skip new columns:** `rating_was_null` is allowed to have any NULL count (it derives from `rating IS NULL`).
   - **Cell 24 (code) — rating_was_null flag consistency (Section 3.6):** Assert `(SELECT COUNT(*) FROM matches_1v1_clean WHERE rating_was_null = TRUE) == (SELECT COUNT(*) FROM matches_1v1_clean WHERE rating IS NULL)`. Cross-check this count against `expected_rating_null_clean` from the ledger; assert within `±1` row (per I7 tolerance from aoestats PR #144).
   - **Cell 25 (code) — Post-cleaning row counts (CONSORT after) + invariant.** Re-run row counts; assert unchanged from Cell 11 values.
   - **Cell 26 (code) — Subgroup impact summary (Section 3.9, Jeanselme et al. 2024):** Build `subgroup_impact` list: each entry has `affected_column`, `source_decision`, `subgroup_most_affected`, `impact`. For aoec specifically:
     - `server` dropped: `~97.39% of rows had NULL server; subgroup with non-NULL server (~2.6% of rows) loses information that no other column carries`.
     - `scenario`/`modDataset` dropped: `100% NULL — no subgroup loses anything`.
     - `password` dropped: `77.57% NULL; subgroup with non-NULL (password-protected lobby) information lost; deemed not predictive for ranked 1v1`.
     - `antiquityMode` dropped: `60% NULL (schema-evolution boundary); pre-patch matches lose this flag; mid-patch matches retain only via downstream patch-stratification`.
     - `mod`/`status` dropped: `Constants — no subgroup affected (zero information content)`.
     - `rating_was_null` added: `~26.20% of matches_1v1_clean rows have rating IS NULL (unrated focal player); flag preserves rated/unrated signal for Phase 02`.
   - **Cell 27 (code) — Cleaning registry (Section 3.10):** Build `cleaning_registry_new` list of 6+ rules: `drop_high_null_columns_clean`, `drop_schema_evolution_columns_clean`, `drop_constants_clean`, `drop_constants_hist`, `add_rating_was_null_flag_clean`, `declare_leaderboards_profiles_oos`. Each rule: `rule_id`, `condition`, `action`, `justification`, `impact`. Print summary.
   - **Cell 28 (code) — Build and write artifact JSON (Section 3.10 / I6):** `validation_artifact = { ... }` per the aoestats Cell 21 pattern, including `step`, `dataset="aoe2companion"`, `generated_date="2026-04-17"`, `cleaning_registry`, `consort_flow_columns` (with `cols_before/dropped/added/modified/after` per VIEW), `consort_flow_matches`, `subgroup_impact`, `validation_assertions` (boolean dict), `sql_queries` (verbatim DDL + assertion SQL), `decisions_resolved`, `ledger_derived_expected_values`. Verify `all_pass = all(validation_artifact["validation_assertions"].values())`; raise `AssertionError` listing failed keys if any. Write to `reports_dir / "artifacts" / "01_exploration" / "04_cleaning" / "01_04_02_post_cleaning_validation.json"`.
   - **Cell 29 (code) — Build and write markdown report:** Mirror aoestats Cell 22. Tables for: per-DS resolutions, cleaning registry (new rules), CONSORT column-count flow, CONSORT match-count flow, subgroup impact, validation results. Write to `reports_dir / "artifacts" / "01_exploration" / "04_cleaning" / "01_04_02_post_cleaning_validation.md"`.
   - **Cell 30 (code) — Update player_history_all schema YAML.** `schema_dir = reports_dir.parent / "data" / "db" / "schemas" / "views"`; `pha_yaml_path = schema_dir / "player_history_all.yaml"`. Build `HIST_COL_NOTES` dict using PROSE-FORMAT (preserve current aoec convention; see `player_history_all.yaml` lines 17–128 for current style). For each column in the post-cleaning DESCRIBE output (19 columns; `status` removed), assemble `columns_yaml_hist` with `name`, `type`, `nullable`, `description`, `notes`. Build `invariants_block_hist` with I3/I5/I6/I9/I10 entries. Build `pha_yaml_content` with `table`, `dataset="aoe2companion"`, `game="aoe2"`, `object_type="view"`, `step="01_04_02"`, `row_count=int(post_hist_rows[0])`, `describe_artifact`, `generated_date="2026-04-17"`, `columns`, `provenance` (with `source_tables=["matches_raw"]`, `filter`, `scope`, `created_by`, `excluded_columns` listing `status` (DS-AOEC-03b constant), `ratingDiff` (POST-GAME I3), `finished` (POST-GAME I3)), `invariants`. Write via `yaml.dump(..., default_flow_style=False, allow_unicode=True, sort_keys=False)`.
   - **Cell 31 (code) — Create matches_1v1_clean schema YAML (NEW).** `mvc_yaml_path = schema_dir / "matches_1v1_clean.yaml"`. Build `CLEAN_COL_NOTES` dict using PROSE-FORMAT (mirror aoestats `matches_1v1_clean.yaml` style; see lines 17–125 of that file). For each of the 48 post-cleaning columns, define a `(notes, description)` tuple. Critical entries:
     - `matchId`: notes = `"IDENTITY. Primary key; R03 1v1 complementarity invariant (each match has exactly one TRUE + one FALSE won row)."`; description = `"Match identifier from matches_raw."`.
     - `started`: notes = `"CONTEXT. I3: Downstream feature queries MUST filter player_history_all by ph.started < this value."`.
     - `won`: notes = `"TARGET. Primary prediction label. BOOLEAN strict TRUE/FALSE; zero NULLs by R03 complementarity (F1 zero-missingness override)."`.
     - `rating`: notes = `"PRE_GAME. Player ELO rating before the match. ~26.20% NULL in scope (DS-AOEC-04 / Rule S4 primary feature exception per van Buuren 2018). The matches_1v1_clean VIEW asserts rating >= 0 upstream so the -1 sentinel is filtered before this VIEW; n_sentinel=0 in the audit reflects upstream filtering. Phase 02 imputation strategy: median-within-leaderboard + see rating_was_null companion flag for missingness-as-signal preservation."`.
     - `rating_was_null`: notes = `"PRE_GAME. Indicator flag for unrated/missing-rating players (rating IS NULL). Derives from rating; safe as feature without temporal filter. New in 01_04_02 per DS-AOEC-04 (sklearn MissingIndicator pattern)."`; description = `"TRUE if this row had NULL rating before any Phase 02 imputation. BOOLEAN."`.
     - `is_null_cluster`: notes = `"CONTEXT. R04 schema-era boundary flag — TRUE when 10 game-settings columns are simultaneously NULL. Spans entire date range, <0.02% of rows; informational only."`.
     - `country`: notes = `"IDENTITY / CONTEXT. Player attribute; potential demographic feature. ~2.25% NULL in scope (rate < 5% Schafer & Graham 2002 boundary; ledger recommendation RETAIN_AS_IS). Player_history_all rate (~8.30%) crosses the FLAG band — Phase 02 chooses per-VIEW strategy ('Unknown' category encoding or country_was_null indicator). NOT pre-materialised at cleaning time per cross-dataset convention (sc2egset / aoestats add flags only for primary features)."`.
     - `hideCivs`: notes = `"PRE_GAME. Schema-evolution column (patch-dependent visibility setting). ~37.18% NULL (DS-AOEC-02 FLAG_FOR_IMPUTATION per ledger). Phase 02 will materialise the imputation method AND its companion indicator (if chosen). NOT pre-materialised at cleaning time per cross-dataset convention (sc2egset isInClan, aoestats deferred non-primary flags)."`.
     - `team`: notes = `"CONTEXT. Team number; sentinel 255 per matches_raw schema YAML notes. ~2.00% NULL (rate < 5% Schafer & Graham 2002 boundary; RETAIN_AS_IS)."`.
     - `filename`: notes = `"IDENTITY / PROVENANCE. Invariant I10: relative path only."`.
     - All other low-NULL game settings: notes = `"PRE_GAME. Game setting; <X% NULL per ledger (Schafer & Graham 2002 < 5% MCAR boundary)."` with X taken from the ledger.
     Build `invariants_block_clean` with I3/I5/I6/I7/I9/I10. Build `mvc_yaml_content` with `table`, `dataset`, `game`, `object_type="view"`, `step="01_04_02"`, `row_count=int(post_clean_rows[0])`, `describe_artifact`, `generated_date="2026-04-17"`, `columns=columns_yaml_clean`, `provenance` (with `source_tables=["matches_raw"]`, `filter` describing the R01 + R02 + R03 + R04 cascade, `scope="Ranked 1v1 decisive matches only (internalLeaderboardId IN (6, 18) AND profileId != -1, deduplicated, won-complementary)."`, `row_multiplicity="2 rows per match (player-row-oriented; one row per player). NOT 1-row-per-match like aoestats. Upstream CTE: see sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_01_data_cleaning.py lines 478-571 (HAVING COUNT(*)=2 + R03 complementarity filter)."`, `notes="Vocabulary style aligned with aoestats (prose-format per-column notes); cross-dataset harmonisation with sc2egset (single-token notes + provenance_categories invariant) deferred to a CROSS PR after all three dataset 01_04_02 PRs land (per Q3 lock from PR #144)."`, `created_by`, **`excluded_columns` enumerated explicitly per round-2 F5:** `[{"name": "server", "reason": "DS-AOEC-01, MNAR 97.39% NULL"}, {"name": "scenario", "reason": "DS-AOEC-01, MAR 100% NULL"}, {"name": "modDataset", "reason": "DS-AOEC-01, MAR 100% NULL"}, {"name": "password", "reason": "DS-AOEC-01, MAR 77.57% NULL"}, {"name": "antiquityMode", "reason": "DS-AOEC-02, MAR 60.06% NULL (schema-evolution)"}, {"name": "mod", "reason": "DS-AOEC-03b, n_distinct=1 constant"}, {"name": "status", "reason": "DS-AOEC-03b, n_distinct=1 constant"}, {"name": "ratingDiff", "reason": "Prior I3 exclusion, POST-GAME"}, {"name": "finished", "reason": "Prior I3 exclusion, POST-GAME"}]`), `invariants`. Write via `yaml.dump`.
   - **Cell 32 (code) — Close DuckDB connection + final summary print.** `db.close()`. Print CONSORT column-count flow (54→48, 20→19), CONSORT row-count flow (61,062,392 unchanged; 264,132,745 unchanged), `rating_was_null` flag count (matches `expected_rating_null_clean`), all_pass status, artifact paths, and PENDING items (STEP_STATUS, PIPELINE_SECTION_STATUS, ROADMAP, research_log).

2. **Pair the notebook** by running once via the parent (jupytext sync produces `01_04_02_data_cleaning_execution.ipynb` from the `.py`).

3. **All SQL constants and ledger lookups** must use the runtime `ledger_val(...)` helper. **No magic numbers** for counts or percentages in code — every `expected_*` value is derived from the ledger CSV. (The plan may cite ledger numbers as expected guidance; the notebook code derives them.)

**Verification:**

- `source .venv/bin/activate && poetry run jupytext --execute /Users/tomaszpionka/Projects/rts-outcome-prediction/sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py` runs end-to-end with no `AssertionError`.
- All 25-32 cells execute; final summary prints `All assertions pass: True`.
- `01_04_02_post_cleaning_validation.json` and `01_04_02_post_cleaning_validation.md` exist on disk under `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/`.
- `matches_1v1_clean.yaml` exists under `src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/` with exactly 48 column entries + invariants block.
- `player_history_all.yaml` updated with 19 columns (status removed) + step="01_04_02".
- `con.execute("DESCRIBE matches_1v1_clean").df()` returns 48 rows; `con.execute("DESCRIBE player_history_all").df()` returns 19 rows.
- `validation_artifact["all_assertions_pass"] is True`.

**File scope:**
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py` (CREATE)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.ipynb` (CREATE — jupytext-paired)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.json` (CREATE)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.md` (CREATE)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/player_history_all.yaml` (UPDATE — drop status entry, bump step, refresh invariants)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/matches_1v1_clean.yaml` (CREATE)

**Read scope:**
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv` (read at notebook runtime — empirical evidence base, I7)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_01_data_cleaning.py` (read by author for current DDL reference; not read at runtime)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py` (template reference for cell structure)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/matches_1v1_clean.yaml` (template reference for prose-format YAML structure)

---

### T02 — Update STEP_STATUS.yaml + PIPELINE_SECTION_STATUS.yaml

**Execution order constraint (per round-1 adversarial review):** This task MUST run AFTER T03 (ROADMAP append). Otherwise there is a window where `PIPELINE_SECTION_STATUS.yaml` marks `01_04` as `complete` but `ROADMAP.md`'s last 01_04 step is still `01_04_01` — internally inconsistent for any concurrent reader. Order: T01 (notebook) → T03 (ROADMAP append) → T02 (STATUS bump) → T04 (research_log). Or commit T02 + T03 atomically.

**Objective:** Reflect the completion of step 01_04_02 in the dataset's status registries. Per the derivation chain `STEP_STATUS.yaml -> PIPELINE_SECTION_STATUS.yaml -> PHASE_STATUS.yaml`, the step entry must be added before the pipeline-section entry can be derived as `complete`.

**Instructions:**

1. **Append a new entry to STEP_STATUS.yaml** under `steps:` (after the existing `01_04_01` entry):
   ```yaml
   "01_04_02":
     name: "Data Cleaning Execution"
     pipeline_section: "01_04"
     status: complete
     completed_at: "2026-04-17"
   ```

2. **If the user confirms there are no pre-listed 01_04_03+ steps in ROADMAP** (Q3): **bump the `01_04` pipeline section in PIPELINE_SECTION_STATUS.yaml** from `in_progress` → `complete` (the derivation rule fires when ALL steps in the section are complete). If ROADMAP lists 01_04_03+ steps without `complete` status, KEEP `01_04: in_progress` (this is the safe default; do not over-bump).

3. **Do NOT bump PHASE_STATUS.yaml.** Phase 01 stays `in_progress` because pipeline sections 01_05 and 01_06 are still `not_started` (per the existing PIPELINE_SECTION_STATUS).

**Verification:**

- `cat /Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml | grep "01_04_02"` returns the new entry.
- If pipeline section is bumped: `grep "01_04" /Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PIPELINE_SECTION_STATUS.yaml` shows `status: complete`.
- `grep "01" /Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PHASE_STATUS.yaml` shows `01: in_progress` (unchanged).

**File scope:**
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml` (UPDATE)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PIPELINE_SECTION_STATUS.yaml` (UPDATE — conditional on Q3)

**Read scope:**
- (none — depends only on T01 completion)

---

### T03 — Append Step 01_04_02 block to ROADMAP.md

**Objective:** Document the step formally in the per-dataset ROADMAP so future contributors and reviewers can trace the decision lineage from 01_04_01 (audit) to 01_04_02 (execution). Mirror the structure of the existing 01_04_01 step block (lines 674–887 of `reports/ROADMAP.md`).

**Instructions:**

1. **Add a new H3-level Step block** at `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` immediately after the 01_04_01 block (after line 887, before the `---` separator that precedes Phase 02). Use this YAML-in-fenced-block structure (mirroring 01_04_01):

   ```markdown
   ### Step 01_04_02 — Data Cleaning Execution (act on DS-AOEC-01..08)

   ```yaml
   step_number: "01_04_02"
   name: "Data Cleaning Execution (act on DS-AOEC-01..08)"
   description: >
     Apply VIEW DDL changes implementing all 8 cleaning decisions surfaced
     by the 01_04_01 missingness audit. Replaces matches_1v1_clean and
     player_history_all VIEWs via CREATE OR REPLACE (no raw table changes
     per Invariant I9). Produces post-cleaning validation artifact (JSON+MD),
     creates matches_1v1_clean.yaml schema, updates player_history_all.yaml.
     ratings_clean VIEW unchanged.
   phase: "01 — Data Exploration"
   pipeline_section: "01_04 — Data Cleaning"
   manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 4 (Cleaning)"
   dataset: "aoe2companion"
   question: >
     What concrete VIEW DDL implements DS-AOEC-01..08, and does the
     post-cleaning state satisfy all I3/I5/I6/I7/I9/I10 invariants?
   method: >
     Per-DS resolution: 7 columns dropped from matches_1v1_clean (4 high-NULL
     per Rule S4, 1 schema-evolution per Rule S4 cost-benefit, 2 constants
     via constants-detection override); 1 column added to matches_1v1_clean
     (rating_was_null BOOLEAN flag, sklearn MissingIndicator pattern for the
     primary feature exception per van Buuren 2018 Rule S4); 1 column
     dropped from player_history_all (status constant). Post-cleaning
     assertion battery covers zero-NULL identity, R03 complementarity,
     forbidden-column absence, new-column type, and rating_was_null flag
     consistency (within ±1 row of ledger expected count per I7).
   predecessors:
     - "01_04_01"
   methodology_citations:
     - "Rubin, D.B. (1976). Inference and missing data. Biometrika, 63(3)."
     - "van Buuren, S. (2018). Flexible Imputation of Missing Data, 2nd ed."
     - "Schafer, J.L. & Graham, J.W. (2002). Missing data: Our view of the state of the art."
     - "Liu, X. et al. (2020). CONSORT-AI extension. BMJ 370."
     - "Jeanselme, V. et al. (2024). Participant Flow Diagrams for Health Equity in AI."
     - "Sambasivan, N. et al. (2021). Data Cascades. CHI '21."
     - "scikit-learn v1.8 documentation. sklearn.impute.MissingIndicator."
   notebook_path: "sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py"
   inputs:
     duckdb_views:
       - "matches_1v1_clean (54 cols, 61,062,392 rows — pre-01_04_02 state)"
       - "player_history_all (20 cols, 264,132,745 rows — pre-01_04_02 state)"
     prior_artifacts:
       - "artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv"
       - "artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json"
   outputs:
     duckdb_views:
       - "matches_1v1_clean (48 cols, 61,062,392 rows — post-01_04_02; -7 / +1)"
       - "player_history_all (19 cols, 264,132,745 rows — post-01_04_02; -1 / +0)"
       - "ratings_clean (unchanged)"
     schema_yamls:
       - "data/db/schemas/views/matches_1v1_clean.yaml (NEW — 48 cols + invariants block; prose-format notes)"
       - "data/db/schemas/views/player_history_all.yaml (UPDATED — 19 cols; status removed; step bumped to 01_04_02)"
     data_artifacts:
       - "artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.json"
       - "artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.md"
   reproducibility: >
     All SQL DDL + assertion SQL stored verbatim in
     01_04_02_post_cleaning_validation.json under sql_queries.
     ledger_derived_expected_values block records the runtime-derived
     I7 expected counts. Notebook re-runs deterministically via
     CREATE OR REPLACE VIEW (idempotent).
   key_findings_carried_forward:
     - "DS-AOEC-01 resolved: server/scenario/modDataset/password DROPPED from matches_1v1_clean per Rule S4 (van Buuren 2018)."
     - "DS-AOEC-02 resolved: antiquityMode DROPPED (60.06% NULL, 40-80% non-primary band); hideCivs RETAINED with FLAG_FOR_IMPUTATION deferred to Phase 02."
     - "DS-AOEC-03b resolved: mod (matches_1v1_clean) + status (both VIEWs) DROPPED via constants-detection override."
     - "DS-AOEC-04 resolved: rating RETAINED in matches_1v1_clean; rating_was_null BOOLEAN flag ADDED (sklearn MissingIndicator pattern; Phase 02 imputation: median-within-leaderboard)."
     - "DS-AOEC-05 deferred: country FLAG_FOR_IMPUTATION; Phase 02 strategy TBD."
     - "DS-AOEC-06 resolved: won in matches_1v1_clean RETAIN_AS_IS (zero NULLs by R03)."
     - "DS-AOEC-07 documented: won in player_history_all has ~19,251 NULLs (0.0073%); EXCLUDE_TARGET_NULL_ROWS rule documented in cleaning registry; physical exclusion deferred to Phase 02 feature-computation per Rule S2."
     - "DS-AOEC-08 documented: leaderboards_raw (singleton 2-row reference) + profiles_raw (7 dead columns) FORMALLY DECLARED OUT-OF-ANALYTICAL-SCOPE in cleaning registry."
   scientific_invariants_applied:
     - number: "3"
       how_upheld: >
         No new POST-GAME columns introduced. ratingDiff and finished
         remain excluded (verified by Section 3.3b assertion).
         rating_was_null derives from the PRE_GAME rating column only.
     - number: "5"
       how_upheld: >
         matches_1v1_clean retains player-row orientation (2 rows per match).
         No slot-asymmetry introduced; both player rows treated identically.
     - number: "6"
       how_upheld: >
         All DDL + assertion SQL stored verbatim in JSON sql_queries.
     - number: "7"
       how_upheld: >
         All expected counts loaded at runtime from
         01_04_01_missingness_ledger.csv via ledger_val() helper. No
         magic numbers in notebook code. Plan cites ledger values as
         expected guidance; notebook derives them.
     - number: "9"
       how_upheld: >
         Raw tables UNTOUCHED. Only VIEW DDL changes via CREATE OR REPLACE.
         leaderboards_raw + profiles_raw declared out-of-scope but not
         dropped (no DROP TABLE statements).
     - number: "10"
       how_upheld: >
         No filename derivation changes. The aoec raw tables already
         satisfy I10 from 01_02_02 ingestion.
   gate:
     artifact_check: >
       JSON exists at the path above with all keys: cleaning_registry,
       consort_flow_columns, consort_flow_matches, subgroup_impact,
       validation_assertions (all True), sql_queries, decisions_resolved,
       ledger_derived_expected_values. MD report exists with 6 tables.
       matches_1v1_clean.yaml exists with 48 column entries + invariants.
       player_history_all.yaml updated with 19 columns + step="01_04_02".
     continue_predicate: >
       Notebook executes end-to-end with all assertions PASS.
       DESCRIBE matches_1v1_clean returns 48 columns; DESCRIBE
       player_history_all returns 19 columns. Row counts unchanged.
       STEP_STATUS.yaml has 01_04_02: complete.
     halt_predicate: >
       Any AssertionError in notebook; any forbidden column present;
       row count change; rating_was_null inconsistent with rating IS NULL;
       validation_assertions has any False value.
   research_log_entry: >
     Required on completion: full CONSORT column-flow tables, 8 DS
     resolutions, ledger-derived expected counts, artifact paths.
   ```
   ```

2. **Do NOT pre-list 01_04_03+ steps.** Per project convention, future steps are appended only when activated.

**Verification:**

- `grep "01_04_02" /Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` returns the new step block header.
- The block follows the same YAML-in-fenced-code structure as 01_04_01.

**File scope:**
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` (UPDATE — append Step 01_04_02 block)

**Read scope:**
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` (lines 674–887 — 01_04_01 block as template)

---

### T04 — Append research_log entry

**Objective:** Document the step's findings in the per-dataset research_log.md per the standing requirement (CLAUDE.md: "After Category A step: Update the active dataset's research_log.md"). Cross-reference the aoestats research_log entry for cross-dataset consistency.

**Instructions:**

1. **Prepend a new dated entry** (reverse-chronological order convention) to `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md` immediately after the existing `2026-04-17 — [Phase 01 / Step 01_04_01]` block. Use this template (mirror the aoestats research_log entry at `src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md` lines 11–53 for structure):

   ```markdown
   ## 2026-04-17 — [Phase 01 / Step 01_04_02] Data Cleaning Execution

   **Category:** A (science)
   **Dataset:** aoe2companion
   **Branch:** feat/01-04-02-aoe2companion
   **Step scope:** Acts on all 8 cleaning decisions (DS-AOEC-01..08) surfaced by 01_04_01. Modifies VIEW DDL for matches_1v1_clean and player_history_all via CREATE OR REPLACE (no raw table changes per Invariant I9). Produces post-cleaning validation artifact (JSON+MD), creates matches_1v1_clean.yaml (NEW), updates player_history_all.yaml. All counts loaded from 01_04_01 ledger at runtime (I7).

   ### Reconciliation notes (vs prior 01_04_01 research_log entry — per round-2 F2/F3)

   - **`country` rate** — Prior 01_04_01 entry cited `country | 13.37%` based on a Pass-1 raw rate. Authoritative ledger row 50 shows `matches_1v1_clean.country | 2.2486%` (1,373,052 / 61,062,392). Authoritative ledger row 72 shows `player_history_all.country | 8.305%`. The 01_04_02 schema YAML and registry use the ledger values.
   - **`difficulty` constant status** — Prior 01_04_01 entry incorrectly grouped `difficulty` with `mod, status` constants for DROP. Authoritative ledger row 11 shows `difficulty,VARCHAR,n_distinct=3.0,RETAIN_AS_IS`. The 01_04_02 DDL retains `difficulty` per the ledger; only `mod` (n_distinct=1) and `status` (n_distinct=1) are constants for DROP per DS-AOEC-03b.

   ### CONSORT column-count flow

   - matches_1v1_clean: 54 → 48 cols (drop 7: server/scenario/modDataset/password/antiquityMode/mod/status; add 1: rating_was_null; modify 0)
   - player_history_all: 20 → 19 cols (drop 1: status; add 0; modify 0)

   ### CONSORT row-count flow (column-only — no row changes)

   - matches_1v1_clean: 61,062,392 rows / 30,531,196 matches (unchanged)
   - player_history_all: 264,132,745 rows (unchanged)

   ### 8 DS resolutions

   - **DS-AOEC-01:** server/scenario/modDataset/password DROPPED per Rule S4 (van Buuren 2018; rates 97/100/100/78%)
   - **DS-AOEC-02:** antiquityMode DROPPED (60.06%, 40-80% non-primary band); hideCivs RETAINED with FLAG_FOR_IMPUTATION (37.18%, 5-40% band) deferred to Phase 02
   - **DS-AOEC-03:** Low-NULL game settings group RETAIN_AS_IS (rates < 5% Schafer & Graham 2002 boundary)
   - **DS-AOEC-03b:** mod (matches_1v1_clean) + status (both VIEWs) DROPPED via constants-detection override (n_distinct=1)
   - **DS-AOEC-04:** rating RETAINED in matches_1v1_clean; rating_was_null BOOLEAN flag ADDED (DS-AOEC-04 / Rule S4 primary feature exception; sklearn MissingIndicator pattern)
   - **DS-AOEC-05:** country FLAG_FOR_IMPUTATION (~2.25% in matches_1v1_clean / ~8.30% in player_history_all); Phase 02 strategy TBD ('Unknown' encoding or country_was_null indicator)
   - **DS-AOEC-06:** won in matches_1v1_clean RETAIN_AS_IS (zero NULLs by R03 complementarity; F1 zero-missingness override)
   - **DS-AOEC-07:** won in player_history_all DOCUMENTED as EXCLUDE_TARGET_NULL_ROWS (~19,251 NULLs / 0.0073%); physical exclusion deferred to Phase 02 feature-computation per Rule S2
   - **DS-AOEC-08:** leaderboards_raw (singleton 2-row) + profiles_raw (7 dead columns) FORMALLY DECLARED OUT-OF-ANALYTICAL-SCOPE in cleaning registry (no DDL change, no DROP TABLE)

   ### Ledger-derived expected counts (I7)

   - rating IS NULL in matches_1v1_clean: 15,999,234 (asserted within ±1 row)
   - rating IS NULL in player_history_all: 104,676,152 (informational; no assertion since not modified by 01_04_02)
   - won IS NULL in player_history_all: 19,251 (DS-AOEC-07 documented count; no physical exclusion)

   ### Artifacts produced / updated

   - `reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.json` (NEW)
   - `reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.md` (NEW)
   - `data/db/schemas/views/matches_1v1_clean.yaml` (NEW — 48 cols + invariants block; prose-format notes)
   - `data/db/schemas/views/player_history_all.yaml` (UPDATED — 19 cols; status removed; step bumped to 01_04_02)

   ### Status updates

   - STEP_STATUS.yaml: 01_04_02 → complete (2026-04-17)
   - PIPELINE_SECTION_STATUS.yaml: 01_04 → complete (conditional on Q3 — no 01_04_03+ steps pre-listed)
   - PHASE_STATUS.yaml: phase 01 stays in_progress (01_05 + 01_06 still not_started)

   ### Cross-dataset note

   Third and final dataset in the three-PR Option A sequence:
   - sc2egset 01_04_02 (PR #142, MERGED) — pattern-establisher, single-token notes vocabulary
   - aoestats 01_04_02 (PR #144, MERGED) — first replication, prose-format notes vocabulary
   - **aoec 01_04_02 (THIS PR)** — final replication, prose-format notes vocabulary (matches aoestats per Q3 locked decision)

   Cross-dataset I8 vocabulary harmonization (sc2egset single-token vs aoec/aoestats prose) deferred to a CROSS PR after this lands.
   ```

**Verification:**

- `grep "2026-04-17.*01_04_02" /Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md` returns the new entry header.
- Entry appears before the existing `2026-04-17 — [Phase 01 / Step 01_04_01]` block (reverse-chronological).

**File scope:**
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md` (UPDATE — prepend new entry)

**Read scope:**
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md` (cross-dataset reference for entry structure)

---

## File Manifest

| File | Action |
|------|--------|
| `/Users/tomaszpionka/Projects/rts-outcome-prediction/sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py` | Create |
| `/Users/tomaszpionka/Projects/rts-outcome-prediction/sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.ipynb` | Create (jupytext-paired) |
| `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.json` | Create |
| `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.md` | Create |
| `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/matches_1v1_clean.yaml` | Create |
| `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/player_history_all.yaml` | Update |
| `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml` | Update |
| `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PIPELINE_SECTION_STATUS.yaml` | Update (conditional on Q3) |
| `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` | Update (append 01_04_02 block) |
| `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md` | Update (prepend entry) |

## Gate Condition

12-criterion checklist (adapted from aoestats PR #144):

1. Notebook `01_04_02_data_cleaning_execution.py` executes end-to-end without `AssertionError`.
2. All assertions PASS:
   - **Zero-NULL identity asserts** — matches_1v1_clean: matchId/started/profileId/won; player_history_all: matchId/profileId/started.
   - **R03 complementarity** — every match in matches_1v1_clean has exactly one TRUE + one FALSE won row; the violating-match query returns 0 rows.
   - **Forbidden cols absent** — Section 3.3a (newly dropped: server/scenario/modDataset/password/antiquityMode/mod/status from matches_1v1_clean; status from player_history_all). Section 3.3b (prior I3: ratingDiff/finished still absent from both VIEWs). Section 3.3c (player_history_all RETAINED: won/rating/country/team still present).
   - **New flag col present + correct type** — `rating_was_null` in matches_1v1_clean is BOOLEAN.
   - **rating_was_null flag count consistency** — `COUNT(rating_was_null=TRUE) == COUNT(rating IS NULL)` AND matches `expected_rating_null_clean` from ledger within ±1 row (per I7).
3. CONSORT column-count flow recorded in `01_04_02_post_cleaning_validation.json`: `{"matches_1v1_clean": {"cols_before": 54, "cols_dropped": 7, "cols_added": 1, "cols_modified": 0, "cols_after": 48}, "player_history_all": {"cols_before": 20, "cols_dropped": 1, "cols_added": 0, "cols_modified": 0, "cols_after": 19}}`.
4. Cleaning registry (Manual §4.1) updated with 6 new rules in `validation_artifact["cleaning_registry"]`.
5. `source .venv/bin/activate && poetry run pytest tests/ -v` passes (current count 489/489 — no new tests added, but no regressions).
6. `source .venv/bin/activate && poetry run ruff check src/ tests/` PASS (notebook is in `sandbox/`, not `src/`; only YAML changes touch `src/`).
7. `source .venv/bin/activate && poetry run mypy src/rts_predict/` PASS.
8. No VIEW DDL changes outside scope (raw tables UNTOUCHED per I9; `ratings_clean` UNTOUCHED).
9. PHASE_STATUS.yaml unchanged (Phase 01 stays `in_progress`).
10. Cross-dataset I8 vocabulary parity: prose-format `notes:` preserved in both updated/created YAMLs (matches aoestats convention; no sc2egset single-token migration).
11. All 8 DS resolutions backed by 01_04_01 ledger CSV evidence (every `ds_resolutions[i]["ledger_rate"]` derives from a `ledger_val(...)` call).
12. Reviewer-adversarial critique (`planning/current_plan.critique.md`) produced and addressed before execution begins (Category A requirement per `docs/templates/planner_output_contract.md`).

## Out of scope

- **Feature engineering** (Phase 02). The `rating_was_null` flag is a missingness-as-signal indicator, not an imputed value. Phase 02 owns median-within-leaderboard imputation for `rating`, country encoding, and any conditional/multivariate imputation.
- **Imputation execution.** No `IMPUTE` or median-fill SQL is run in 01_04_02. The flag column makes Phase 02's job easier but does not perform imputation.
- **Raw table modifications.** No `DROP TABLE`, no `ALTER TABLE` against `matches_raw`, `ratings_raw`, `leaderboards_raw`, or `profiles_raw`. Per I9.
- **`leaderboards_raw` and `profiles_raw` removal.** DS-AOEC-08 is documentation-only; the tables remain on disk and are simply declared out-of-analytical-scope in the cleaning registry. No DROP TABLE statements.
- **`ratings_clean` VIEW changes.** No DS-AOEC decision touches this VIEW; it remains as built by 01_04_01.
- **`matches_long_raw` VIEW changes.** This is the canonical long skeleton from 01_04_00; no DS-AOEC decision touches it.
- **Cross-dataset I8 vocabulary harmonization.** Sc2egset uses single-token notes; aoec/aoestats use prose-format. Harmonization deferred to a CROSS PR after all three dataset 01_04_02 PRs land.
- **PHASE_STATUS.yaml bump.** Phase 01 stays `in_progress`; pipeline sections 01_05 + 01_06 are still `not_started`.
- **`hideCivs_was_null`, `country_was_null`, `team_was_null` flag columns.** Only `rating_was_null` is added in 01_04_02. The other FLAG_FOR_IMPUTATION columns receive their flags during Phase 02 imputation, not now. (See Q5 for user override.)
- **Physical exclusion of NULL-target rows from player_history_all** (DS-AOEC-07). The 19,251 NULL-`won` rows are documented in the cleaning registry but NOT physically removed; Rule S2 is enforced at Phase 02 feature-computation time.
- **Per-day or per-month re-validation of the 8 DS resolutions.** The 01_04_01 ledger is treated as authoritative; if the raw data is re-ingested, 01_04_01 must re-run before 01_04_02 re-runs.
- **`leaderboards_raw.yaml` and `profiles_raw.yaml` field corrections** (e.g., stale `row_count: 0` in `leaderboards_raw.yaml`, dead-column annotations in `profiles_raw.yaml`). DS-AOEC-08 is documentation-only in the cleaning registry; no schema YAML field edits in this PR. Stale fields tracked for a future schema-refresh chore.

## Resolutions (round 1 + round 2 adversarial)

- **Q1 LOCKED:** Author `matches_1v1_clean.yaml` from scratch with PROSE-FORMAT notes (aoestats convention; locked Q3 from PR #144).
- **Q2 LOCKED:** Documentation-only OOS declaration in cleaning registry + research_log; no DDL changes; no DROP TABLE.
- **Q3 LOCKED:** Bump `01_04` → `complete` in `PIPELINE_SECTION_STATUS.yaml` (no 01_04_03+ steps planned; verified `STEP_STATUS.yaml:87` no future 01_04 entries; verified `PIPELINE_SECTION_STATUS.yaml:46, 50` 01_05 + 01_06 still `not_started` so PHASE_STATUS.yaml stays `in_progress`).
- **Q4 LOCKED (HYBRID per round-1 F4):** Add the missingness-indicator flag in 01_04_02, named `rating_was_null` (NOT `rating_imputed` — at materialisation time nothing has been imputed; cross-dataset alignment with sc2egset `is_mmr_missing` and aoestats `is_unrated`). Phase 02 contract: this flag is a frozen-at-cleaning-time observation, never overwritten by any imputation step.
- **Q5 LOCKED:** Defer `hideCivs_was_null`, `country_was_null`, `team_was_null` to Phase 02. Only `rating_was_null` (primary feature per Rule S4) is added in 01_04_02. matches_1v1_clean column count = 48 (NOT 50).

## Open questions

- **Q1 (schema YAML authoring scope) — resolves by: user decision before T01 starts.** `matches_1v1_clean.yaml` does not yet exist for aoec. Confirm we author it from scratch in 01_04_02 with PROSE-FORMAT notes (aoestats convention, locked Q3 from PR #144) — i.e., per-column `notes:` is a sentence/paragraph leading with provenance category prefix (e.g., `"PRE_GAME. Player ELO rating before the match. ~26.20% NULL ..."`), NOT sc2egset single-token notes (`"PRE_GAME"`).
- **Q2 (out-of-analytical-scope DDL form) — resolves by: user decision before T01 starts.** `leaderboards_raw` (2-row reference) and `profiles_raw` (7 dead columns) — confirm formal out-of-analytical-scope declaration in the plan + cleaning registry + research_log only (no DDL changes, no DROP TABLE statements). The schema YAMLs at `data/db/schemas/raw/leaderboards_raw.yaml` and `data/db/schemas/raw/profiles_raw.yaml` remain on disk unchanged.
- **Q3 (ROADMAP closure) — resolves by: user decision before T02.** Does pipeline section `01_04` close after 01_04_02 (PIPELINE_SECTION_STATUS=complete), or are there pre-listed 01_04_03+ entries to check first? Current STEP_STATUS.yaml has only 01_04_00 and 01_04_01; no 01_04_03+ entries are listed in ROADMAP.md (search confirmed). Default proposal: **bump 01_04 → complete** in T02. User override: keep `in_progress` if planning a 01_04_03 (e.g., post-cleaning EDA refresh).
- **Q4 (rating_was_null flag introduction) — resolves by: user decision before T01.** Confirm DS-AOEC-04 maps to **adding the `rating_was_null` BOOLEAN flag in 01_04_02** (this plan's recommendation, per sklearn MissingIndicator + the sc2egset PR #142 `mmr_is_zero` precedent). User override: defer to Phase 02 entirely (no DDL change in 01_04_02 for `rating`). The aoestats analog `is_unrated` was added in PR #144 because it converts a sentinel; aoec's `rating` already has NULL not 0, so the flag is purely a missingness indicator without NULLIF.
- **Q5 (additional `*_was_null` flags) — resolves by: user decision before T01.** Should `hideCivs_was_null`, `country_was_null`, AND `team_was_null` BOOLEAN flag columns be added in 01_04_02 alongside `rating_was_null` (consistency with the missingness-as-signal principle for all FLAG_FOR_IMPUTATION columns), or deferred to Phase 02 (minimal-DDL-change in 01_04_02; only the primary feature gets a flag now)? **Default proposal: defer hideCivs, country, and team flags to Phase 02** (they are not "primary features" per DS-AOEC; only `rating` has primary-feature status per Rule S4). If user picks "add all 4 flags now," the matches_1v1_clean column count becomes 54 - 7 + 4 = **51 cols** (not 48), and the assertion in Cell 18 must be updated.

---

**Critique reminder:** Category A plan — adversarial critique is required before execution begins. The parent session must dispatch reviewer-adversarial to produce `planning/current_plan.critique.md` covering Scope, Problem Statement, Assumptions & unknowns, Literature context, Execution Steps, File Manifest, Gate Condition, Out of scope, and Open Questions. Critique must be addressed (or explicitly accepted) before T01 starts.
